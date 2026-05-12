from __future__ import annotations

import csv
import hashlib
import os
from collections.abc import Sequence
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Literal

import numpy as np

from hakari_bench.bm25 import BM25Config, evaluate_bm25_task
from hakari_bench.datasets import DatasetRegistry, EvalTask, resolve_eval_tasks
from hakari_bench.evaluation import LoadedIrDataset, evaluate_dense_task, evaluate_reranker_task, load_ir_dataset
from hakari_bench.metrics import (
    DEFAULT_ACCURACY_K,
    DEFAULT_MAP_K,
    DEFAULT_MRR_K,
    DEFAULT_NDCG_K,
    DEFAULT_PRECISION_RECALL_K,
)
from sentence_transformers.base.evaluation import BaseEvaluator

CorpusPolicy = Literal["full", "sampled_candidates"]
BM25Source = Literal["dataset", "computed"]


_METRIC_SUFFIXES = tuple(
    [f"accuracy@{k}" for k in DEFAULT_ACCURACY_K]
    + [item for k in DEFAULT_PRECISION_RECALL_K for item in (f"precision@{k}", f"recall@{k}")]
    + [f"mrr@{k}" for k in DEFAULT_MRR_K]
    + [f"ndcg@{k}" for k in DEFAULT_NDCG_K]
    + [f"map@{k}" for k in DEFAULT_MAP_K]
)


@dataclass(frozen=True)
class HakariNanoTarget:
    """Select HAKARI-Bench Nano tasks for SentenceTransformers training evaluators.

    Args:
        dataset: Built-in HAKARI dataset name or Hugging Face dataset id, for example
            ``"NanoMIRACL"`` or ``"hakari-bench/NanoCoIR"``.
        collection: Built-in HAKARI collection name. Use either ``dataset`` or
            ``collection``, not both.
        splits: Optional split/task names scoped to this target, for example
            ``["en"]`` for the English NanoMIRACL split.
        tasks: Pre-resolved tasks. This is primarily useful for tests and custom
            embedding applications that already own task construction.

    This mirrors the dataset selection style used by the HAKARI-Bench CLI while
    making per-target split selection explicit for training code.
    """

    dataset: str | None = None
    collection: str | None = None
    splits: tuple[str, ...] | list[str] = ()
    tasks: tuple[EvalTask, ...] | list[EvalTask] = field(default_factory=tuple)

    def __post_init__(self) -> None:
        object.__setattr__(self, "splits", tuple(self.splits))
        object.__setattr__(self, "tasks", tuple(self.tasks))
        selectors = sum(1 for value in (self.dataset, self.collection) if value is not None)
        if self.tasks:
            return
        if selectors != 1:
            raise ValueError("HakariNanoTarget requires exactly one of dataset, collection, or pre-resolved tasks.")


TargetSpec = Sequence[HakariNanoTarget | str] | None


def resolve_hakari_nano_targets(
    targets: TargetSpec = None,
    *,
    registry: DatasetRegistry | None = None,
) -> list[EvalTask]:
    """Resolve SentenceTransformers evaluator targets into HAKARI ``EvalTask`` objects."""

    registry = registry or DatasetRegistry.load_builtin()
    normalized_targets = _normalize_targets(targets)
    tasks: list[EvalTask] = []
    for target in normalized_targets:
        if target.tasks:
            tasks.extend(target.tasks)
            continue
        tasks.extend(
            resolve_eval_tasks(
                registry=registry,
                dataset_values=[target.dataset] if target.dataset is not None else [],
                collection_values=[target.collection] if target.collection is not None else [],
                split_values=list(target.splits),
            )
        )
    return _dedupe_tasks(tasks)


def sample_ir_dataset(
    dataset: LoadedIrDataset,
    *,
    query_limit: int | None = None,
    query_sample_seed: int = 13,
    corpus_policy: CorpusPolicy = "full",
) -> LoadedIrDataset:
    """Return a deterministic query-capped IR dataset for training-time evaluation.

    ``corpus_policy="full"`` keeps the original corpus and should be used for
    comparable benchmark evaluation. ``"sampled_candidates"`` keeps only qrels
    positives plus candidate documents for sampled queries; it is intended for
    smoke training checks, not leaderboard-comparable scores.
    """

    if query_limit is not None and query_limit <= 0:
        raise ValueError("query_limit must be positive.")
    if corpus_policy not in {"full", "sampled_candidates"}:
        raise ValueError(f"Unsupported corpus_policy: {corpus_policy!r}.")

    query_ids = list(dataset.queries)
    if query_limit is not None and query_limit < len(query_ids):
        selected_query_ids = _stable_sample_query_ids(
            query_ids,
            query_limit=query_limit,
            query_sample_seed=query_sample_seed,
            evaluator_name=dataset.evaluator_name,
        )
        selected = set(selected_query_ids)
        ordered_query_ids = [query_id for query_id in query_ids if query_id in selected]
    else:
        ordered_query_ids = query_ids

    queries = {query_id: dataset.queries[query_id] for query_id in ordered_query_ids}
    qrels = {query_id: set(dataset.qrels.get(query_id, set())) for query_id in ordered_query_ids}
    candidates = None
    if dataset.candidates is not None:
        candidates = {
            query_id: [doc_id for doc_id in dataset.candidates.get(query_id, []) if doc_id in dataset.corpus]
            for query_id in ordered_query_ids
        }
    corpus = dataset.corpus
    if corpus_policy == "sampled_candidates":
        corpus_ids: set[str] = set()
        for query_id in ordered_query_ids:
            corpus_ids.update(doc_id for doc_id in qrels.get(query_id, set()) if doc_id in dataset.corpus)
            if candidates is not None:
                corpus_ids.update(candidates.get(query_id, []))
        corpus = {doc_id: dataset.corpus[doc_id] for doc_id in dataset.corpus if doc_id in corpus_ids}

    return LoadedIrDataset(
        queries=queries,
        corpus=corpus,
        qrels=qrels,
        candidates=candidates,
        evaluator_name=dataset.evaluator_name,
    )


class _HakariNanoBaseEvaluator(BaseEvaluator):
    def __init__(
        self,
        *,
        targets: TargetSpec,
        name: str,
        aggregate_key: str,
        primary_metric: str,
        batch_size: int,
        show_progress_bar: bool,
        candidate_ranking: str | None,
        dataset_revision: str | None,
        query_limit: int | None,
        query_sample_seed: int,
        corpus_policy: CorpusPolicy,
        write_csv: bool,
    ) -> None:
        super().__init__()
        self.name = name
        self.aggregate_key = aggregate_key
        self.primary_metric_suffix = primary_metric
        self.primary_metric = f"{self.name}_{self.aggregate_key}_{self.primary_metric_suffix}"
        self.batch_size = batch_size
        self.show_progress_bar = show_progress_bar
        self.candidate_ranking = candidate_ranking
        self.dataset_revision = dataset_revision
        self.query_limit = query_limit
        self.query_sample_seed = query_sample_seed
        self.corpus_policy = corpus_policy
        self.write_csv = write_csv
        self.tasks = resolve_hakari_nano_targets(targets)

    def _load_dataset(self, task: EvalTask) -> LoadedIrDataset:
        dataset = load_ir_dataset(
            task,
            candidate_subset_name=self.candidate_ranking,
            revision=self.dataset_revision,
        )
        return sample_ir_dataset(
            dataset,
            query_limit=self.query_limit,
            query_sample_seed=self.query_sample_seed,
            corpus_policy=self.corpus_policy,
        )

    def _finalize(
        self,
        *,
        model: Any,
        metrics: list[dict[str, float]],
        output_path: str | None,
        epoch: int,
        steps: int,
    ) -> dict[str, float]:
        results: dict[str, float] = {}
        for task_metrics in metrics:
            results.update(task_metrics)
        aggregated = _aggregate_metrics(metrics)
        prefixed_aggregated = {f"{self.name}_{self.aggregate_key}_{key}": value for key, value in aggregated.items()}
        results.update(prefixed_aggregated)
        if self.primary_metric not in results:
            raise ValueError(
                f"Primary metric {self.primary_metric!r} was not produced. "
                f"Available metrics: {sorted(results)}"
            )
        _store_metrics_if_available(self, model, prefixed_aggregated, epoch, steps)
        if output_path is not None and self.write_csv:
            _append_csv_row(
                output_path=output_path,
                filename=f"{self.name}_{self.aggregate_key}_results.csv",
                row={"epoch": epoch, "steps": steps, self.primary_metric: results[self.primary_metric]},
            )
        return results

    def get_config_dict(self) -> dict[str, Any]:
        return {
            "targets": [_task_config(task) for task in self.tasks],
            "aggregate_key": self.aggregate_key,
            "primary_metric": self.primary_metric_suffix,
            "batch_size": self.batch_size,
            "candidate_ranking": self.candidate_ranking,
            "dataset_revision": self.dataset_revision,
            "query_limit": self.query_limit,
            "query_sample_seed": self.query_sample_seed,
            "corpus_policy": self.corpus_policy,
        }


class HakariNanoEmbeddingEvaluator(_HakariNanoBaseEvaluator):
    """Evaluate dense or sparse SentenceTransformers models on HAKARI Nano IR tasks.

    The evaluator follows the SentenceTransformers ``BaseEvaluator`` contract and
    can be passed to ``SentenceTransformerTrainer`` or ``SparseEncoderTrainer``.
    It reuses HAKARI-Bench scoring, so metrics match the benchmark CLI.

    See also:
        - https://sbert.net/docs/package_reference/sentence_transformer/trainer.html
        - https://sbert.net/docs/package_reference/sparse_encoder/trainer.html
        - https://github.com/huggingface/sentence-transformers/blob/main/sentence_transformers/sentence_transformer/evaluation/nano_beir.py
        - https://github.com/huggingface/sentence-transformers/blob/main/sentence_transformers/sparse_encoder/evaluation/sparse_nano_beir.py
    """

    def __init__(
        self,
        targets: TargetSpec = None,
        *,
        name: str = "HakariNano",
        aggregate_key: str = "mean",
        primary_metric: str = "ndcg@10",
        batch_size: int = 32,
        show_progress_bar: bool = False,
        candidate_ranking: str | None = "bm25",
        dataset_revision: str | None = None,
        query_limit: int | None = None,
        query_sample_seed: int = 13,
        corpus_policy: CorpusPolicy = "full",
        query_prompt: str | None = None,
        document_prompt: str | None = None,
        query_prompt_name: str | None = None,
        document_prompt_name: str | None = None,
        query_encode_task: str | None = None,
        document_encode_task: str | None = None,
        truncate_dim: int | None = None,
        sparse_query_max_active_dims: int | None = None,
        sparse_document_max_active_dims: int | None = None,
        embedding_variants: list[dict[str, Any]] | None = None,
        retrieval_score_device: str = "auto",
        rerank_top_k: int = 100,
        write_csv: bool = False,
    ) -> None:
        super().__init__(
            targets=targets,
            name=name,
            aggregate_key=aggregate_key,
            primary_metric=primary_metric,
            batch_size=batch_size,
            show_progress_bar=show_progress_bar,
            candidate_ranking=candidate_ranking,
            dataset_revision=dataset_revision,
            query_limit=query_limit,
            query_sample_seed=query_sample_seed,
            corpus_policy=corpus_policy,
            write_csv=write_csv,
        )
        self.query_prompt = query_prompt
        self.document_prompt = document_prompt
        self.query_prompt_name = query_prompt_name
        self.document_prompt_name = document_prompt_name
        self.query_encode_task = query_encode_task
        self.document_encode_task = document_encode_task
        self.truncate_dim = truncate_dim
        self.sparse_query_max_active_dims = sparse_query_max_active_dims
        self.sparse_document_max_active_dims = sparse_document_max_active_dims
        self.embedding_variants = list(embedding_variants or [])
        self.retrieval_score_device = retrieval_score_device
        self.rerank_top_k = rerank_top_k

    def __call__(
        self,
        model: Any,
        output_path: str | None = None,
        epoch: int = -1,
        steps: int = -1,
        *_args: Any,
        **_kwargs: Any,
    ) -> dict[str, float]:
        task_metrics: list[dict[str, float]] = []
        for task in self.tasks:
            dataset = self._load_dataset(task)
            evaluation = evaluate_dense_task(
                model=model,
                dataset=dataset,
                batch_size=self.batch_size,
                show_progress=self.show_progress_bar,
                query_prompt=self.query_prompt,
                corpus_prompt=self.document_prompt,
                query_prompt_name=self.query_prompt_name,
                corpus_prompt_name=self.document_prompt_name,
                query_task=self.query_encode_task,
                corpus_task=self.document_encode_task,
                truncate_dim=self.truncate_dim,
                truncate_sparse_query_max_dims=self.sparse_query_max_active_dims,
                truncate_sparse_docs_max_dims=self.sparse_document_max_active_dims,
                embedding_variants=self.embedding_variants,
                aggregate_metric=self.primary_metric_suffix,
                score_device=self.retrieval_score_device,
                rerank_top_n=self.rerank_top_k,
            )
            task_metrics.append(evaluation.metrics)
        return self._finalize(model=model, metrics=task_metrics, output_path=output_path, epoch=epoch, steps=steps)


class HakariNanoRerankerEvaluator(_HakariNanoBaseEvaluator):
    """Evaluate a SentenceTransformers ``CrossEncoder`` reranker on HAKARI Nano tasks.

    The evaluator reranks the selected candidate subset, usually BM25, and follows
    the same ``BaseEvaluator`` shape as SentenceTransformers'
    ``CrossEncoderNanoBEIREvaluator``.

    See also:
        - https://sbert.net/docs/package_reference/cross_encoder/trainer.html
        - https://github.com/huggingface/sentence-transformers/blob/main/sentence_transformers/cross_encoder/evaluation/nano_beir.py
    """

    def __init__(
        self,
        targets: TargetSpec = None,
        *,
        name: str | None = None,
        aggregate_key: str = "mean",
        primary_metric: str = "ndcg@10",
        batch_size: int = 32,
        show_progress_bar: bool = False,
        candidate_ranking: str = "bm25",
        dataset_revision: str | None = None,
        query_limit: int | None = None,
        query_sample_seed: int = 13,
        corpus_policy: CorpusPolicy = "full",
        rerank_top_k: int = 100,
        inference_kwargs: dict[str, Any] | None = None,
        write_csv: bool = False,
    ) -> None:
        self.rerank_top_k = rerank_top_k
        evaluator_name = name or f"HakariNano_R{rerank_top_k}"
        super().__init__(
            targets=targets,
            name=evaluator_name,
            aggregate_key=aggregate_key,
            primary_metric=primary_metric,
            batch_size=batch_size,
            show_progress_bar=show_progress_bar,
            candidate_ranking=candidate_ranking,
            dataset_revision=dataset_revision,
            query_limit=query_limit,
            query_sample_seed=query_sample_seed,
            corpus_policy=corpus_policy,
            write_csv=write_csv,
        )
        self.inference_kwargs = dict(inference_kwargs or {})

    def __call__(
        self,
        model: Any,
        output_path: str | None = None,
        epoch: int = -1,
        steps: int = -1,
        *_args: Any,
        **_kwargs: Any,
    ) -> dict[str, float]:
        task_metrics: list[dict[str, float]] = []
        for task in self.tasks:
            dataset = self._load_dataset(task)
            evaluation = evaluate_reranker_task(
                model=model,
                dataset=dataset,
                batch_size=self.batch_size,
                show_progress=self.show_progress_bar,
                rerank_top_n=self.rerank_top_k,
                aggregate_metric=self.primary_metric_suffix,
                score_kwargs=self.inference_kwargs,
            )
            task_metrics.append(evaluation.metrics)
        return self._finalize(model=model, metrics=task_metrics, output_path=output_path, epoch=epoch, steps=steps)


class HakariNanoBM25Evaluator(_HakariNanoBaseEvaluator):
    """Evaluate BM25 baselines on HAKARI Nano tasks without a neural model."""

    def __init__(
        self,
        targets: TargetSpec = None,
        *,
        name: str = "HakariNanoBM25",
        aggregate_key: str = "mean",
        primary_metric: str = "ndcg@10",
        candidate_ranking: str = "bm25",
        dataset_revision: str | None = None,
        query_limit: int | None = None,
        query_sample_seed: int = 13,
        corpus_policy: CorpusPolicy = "full",
        bm25_source: BM25Source = "dataset",
        bm25_top_k: int = 100,
        bm25_tokenizer: str | None = None,
        bm25_tokenizer_name: str | None = None,
        bm25_stemmer_algorithm: str = "english",
        bm25_k1: float = 1.5,
        bm25_b: float = 0.75,
        show_progress_bar: bool = False,
        write_csv: bool = False,
    ) -> None:
        super().__init__(
            targets=targets,
            name=name,
            aggregate_key=aggregate_key,
            primary_metric=primary_metric,
            batch_size=0,
            show_progress_bar=show_progress_bar,
            candidate_ranking=candidate_ranking,
            dataset_revision=dataset_revision,
            query_limit=query_limit,
            query_sample_seed=query_sample_seed,
            corpus_policy=corpus_policy,
            write_csv=write_csv,
        )
        self.bm25_source = bm25_source
        self.bm25_config = BM25Config(
            tokenizer=bm25_tokenizer,
            tokenizer_name=bm25_tokenizer_name,
            stemmer_algorithm=bm25_stemmer_algorithm,
            top_k=bm25_top_k,
            k1=bm25_k1,
            b=bm25_b,
            show_progress=show_progress_bar,
        )

    def __call__(
        self,
        model: Any | None = None,
        output_path: str | None = None,
        epoch: int = -1,
        steps: int = -1,
        *_args: Any,
        **_kwargs: Any,
    ) -> dict[str, float]:
        task_metrics: list[dict[str, float]] = []
        source = "dataset_candidate_subset" if self.bm25_source == "dataset" else "computed_bm25s"
        for task in self.tasks:
            dataset = self._load_dataset(task)
            evaluation = evaluate_bm25_task(
                dataset=dataset,
                config=self.bm25_config,
                source=source,
            )
            task_metrics.append(evaluation.metrics)
        return self._finalize(model=model, metrics=task_metrics, output_path=output_path, epoch=epoch, steps=steps)


def _normalize_targets(
    targets: TargetSpec,
) -> list[HakariNanoTarget]:
    if targets is None:
        return [HakariNanoTarget(dataset="NanoBEIR-en")]
    normalized: list[HakariNanoTarget] = []
    for target in targets:
        normalized.append(HakariNanoTarget(dataset=target) if isinstance(target, str) else target)
    if not normalized:
        raise ValueError("At least one HAKARI Nano target is required.")
    return normalized


def _dedupe_tasks(tasks: list[EvalTask]) -> list[EvalTask]:
    deduped: list[EvalTask] = []
    seen: set[tuple[str, str]] = set()
    for task in tasks:
        key = (task.dataset_id, task.split_name)
        if key in seen:
            continue
        seen.add(key)
        deduped.append(task)
    if not deduped:
        raise ValueError("No HAKARI Nano evaluation tasks were resolved.")
    return deduped


def _stable_sample_query_ids(
    query_ids: list[str],
    *,
    query_limit: int,
    query_sample_seed: int,
    evaluator_name: str,
) -> set[str]:
    scored = [
        (
            hashlib.sha256(f"{query_sample_seed}\0{evaluator_name}\0{query_id}".encode("utf-8")).hexdigest(),
            query_id,
        )
        for query_id in query_ids
    ]
    return {query_id for _score, query_id in sorted(scored)[:query_limit]}


def _aggregate_metrics(metrics: list[dict[str, float]]) -> dict[str, float]:
    values: dict[str, list[float]] = {suffix: [] for suffix in _METRIC_SUFFIXES}
    for task_metrics in metrics:
        for key, value in task_metrics.items():
            suffix = _metric_suffix(key)
            if suffix is None:
                continue
            values[suffix].append(float(value))
    return {suffix: float(np.mean(items)) for suffix, items in values.items() if items}


def _metric_suffix(key: str) -> str | None:
    lowered = key.lower()
    for suffix in _METRIC_SUFFIXES:
        if lowered.endswith(suffix):
            return suffix
    return None


def _store_metrics_if_available(
    evaluator: _HakariNanoBaseEvaluator,
    model: Any,
    metrics: dict[str, float],
    epoch: int,
    steps: int,
) -> None:
    if model is None or not hasattr(model, "model_card_data"):
        return
    try:
        evaluator.store_metrics_in_model_card_data(model, metrics, epoch, steps)
    except Exception:
        return


def _append_csv_row(*, output_path: str, filename: str, row: dict[str, Any]) -> None:
    Path(output_path).mkdir(parents=True, exist_ok=True)
    csv_path = os.path.join(output_path, filename)
    exists = os.path.exists(csv_path)
    with open(csv_path, "a", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(row))
        if not exists:
            writer.writeheader()
        writer.writerow(row)


def _task_config(task: EvalTask) -> dict[str, Any]:
    return {
        "dataset_name": task.dataset_name,
        "dataset_id": task.dataset_id,
        "split_name": task.split_name,
        "task_name": task.task_name,
    }
