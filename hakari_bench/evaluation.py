from __future__ import annotations

import inspect
import os
import re
import sys
import time
from dataclasses import dataclass, field
from collections.abc import Iterator, Mapping, Sequence
from typing import Any, Literal, cast

import numpy as np
import torch
from scipy import sparse
from tqdm.auto import tqdm

from hakari_bench.datasets import EvalTask
from hakari_bench.defaults import DEFAULT_CANDIDATE_RANKING, DEFAULT_RERANK_TOP_K
from hakari_bench.embedding_matrix import QuantizedEmbeddingMatrix
from hakari_bench.metrics import compute_ir_metrics
from hakari_bench.scoring import candidate_coverage_for_qrels
from hakari_bench.scoring import rank_candidate_subset_by_similarity

QuantizationPrecision = Literal["int8", "binary"]
TORCH_SCORE_REPRESENTATION = "torch_exact"
TORCH_RESCORE_SCORE_REPRESENTATION = "torch_exact_rescore"
QUANTIZED_CANDIDATE_TOP_K = 100
LATE_INTERACTION_RANKING_DEPTH = 100
QUANTIZED_RESCORE_SCORE_REPRESENTATIONS = {
    TORCH_RESCORE_SCORE_REPRESENTATION,
}
TOP_RANKING_ARTIFACT_DEPTH = 100


@dataclass(frozen=True)
class LoadedIrDataset:
    queries: dict[str, str]
    corpus: Mapping[str, str]
    qrels: dict[str, set[str]]
    candidates: dict[str, list[str]] | None
    evaluator_name: str


class _LazyCorpusById(Mapping[str, str]):
    def __init__(self, dataset: Any, ids: set[str]) -> None:
        self._dataset = dataset
        self._max_text_chars = _reranker_document_max_chars()
        ids_only = dataset.select_columns(["_id"]) if hasattr(dataset, "select_columns") else dataset
        self._index_by_id: dict[str, int] = {}
        for index, row in enumerate(ids_only):
            row_id = str(row["_id"])
            if row_id in ids:
                self._index_by_id[row_id] = index

    def __getitem__(self, key: str) -> str:
        index = self._index_by_id[key]
        return self._text_at(index)

    def __iter__(self) -> Iterator[str]:
        return iter(self._index_by_id)

    def __len__(self) -> int:
        return len(self._index_by_id)

    def _text_at(self, index: int) -> str:
        text = str(self._dataset[int(index)]["text"])
        if self._max_text_chars is not None and len(text) > self._max_text_chars:
            return text[: self._max_text_chars]
        return text


def _reranker_document_max_chars() -> int | None:
    raw = os.environ.get("HAKARI_RERANKER_DOCUMENT_MAX_CHARS")
    if raw is None or not raw.strip():
        return None
    try:
        value = int(raw)
    except ValueError:
        return None
    return value if value > 0 else None


@dataclass(frozen=True)
class TaskEvaluation:
    metrics: dict[str, float]
    timing: dict[str, float]
    embedding_conversion: dict[str, Any] = field(default_factory=dict)
    embedding_evaluations: list[dict[str, Any]] = field(default_factory=list)
    rerank_metrics: dict[str, float] = field(default_factory=dict)
    reranking_evaluations: list[dict[str, Any]] = field(default_factory=list)
    rerank_aggregate_metric_value: float | None = None
    top_rankings: list[dict[str, Any]] = field(default_factory=list)


def load_ir_dataset(
    task: EvalTask,
    *,
    candidate_subset_name: str | None = None,
    revision: str | None = None,
    restrict_corpus_to_candidates: bool = False,
) -> LoadedIrDataset:
    from datasets import load_dataset

    queries_dataset = load_dataset(task.dataset_id, task.dataset.queries_config, split=task.split_name, revision=revision)
    qrels_dataset = load_dataset(task.dataset_id, task.dataset.qrels_config, split=task.split_name, revision=revision)
    candidates = _load_candidates(task, candidate_subset_name=candidate_subset_name, revision=revision)

    candidate_corpus_ids: set[str] | None = None
    if restrict_corpus_to_candidates and candidates is not None:
        candidate_corpus_ids = {corpus_id for corpus_ids in candidates.values() for corpus_id in corpus_ids}

    corpus_dataset = load_dataset(task.dataset_id, task.dataset.corpus_config, split=task.split_name, revision=revision)

    if candidate_corpus_ids is not None:
        corpus: Mapping[str, str] = _LazyCorpusById(corpus_dataset, candidate_corpus_ids)
    else:
        corpus = {str(row["_id"]): str(row["text"]) for row in corpus_dataset if str(row.get("text", ""))}
    queries = {str(row["_id"]): str(row["text"]) for row in queries_dataset if str(row.get("text", ""))}

    qrels: dict[str, set[str]] = {}
    for row in qrels_dataset:
        query_id = str(row["query-id"])
        corpus_ids = row.get("corpus-id")
        qrels.setdefault(query_id, set())
        if isinstance(corpus_ids, list):
            qrels[query_id].update(str(corpus_id) for corpus_id in corpus_ids)
        else:
            qrels[query_id].add(str(corpus_ids))

    return LoadedIrDataset(
        queries=queries,
        corpus=corpus,
        qrels=qrels,
        candidates=candidates,
        evaluator_name=task.evaluator_name,
    )


def _load_candidates(
    task: EvalTask,
    *,
    candidate_subset_name: str | None,
    revision: str | None,
) -> dict[str, list[str]] | None:
    if candidate_subset_name is None:
        return None
    try:
        from datasets import load_dataset

        rows = load_dataset(task.dataset_id, candidate_subset_name, split=task.split_name, revision=revision)
    except Exception:
        return None
    candidates: dict[str, list[str]] = {}
    for row in rows:
        candidates[str(row["query-id"])] = [str(corpus_id) for corpus_id in row["corpus-ids"]]
    return candidates


def evaluate_dense_task(
    *,
    model: Any,
    dataset: LoadedIrDataset,
    batch_size: int,
    show_progress: bool,
    query_prompt: str | None,
    corpus_prompt: str | None,
    query_prompt_name: str | None,
    corpus_prompt_name: str | None,
    query_task: str | None = None,
    corpus_task: str | None = None,
    truncate_dim: int | None = None,
    truncate_sparse_query_max_dims: int | None = None,
    truncate_sparse_docs_max_dims: int | None = None,
    embedding_variants: list[dict[str, Any]] | None = None,
    aggregate_metric: str = "ndcg@10",
    score_device: str = "auto",
    rerank_top_n: int | None = DEFAULT_RERANK_TOP_K,
    candidate_ranking_name: str | None = DEFAULT_CANDIDATE_RANKING,
    encode_devices: list[str] | None = None,
    encode_chunk_size: int | None = None,
    encode_pool: dict[str, Any] | None = None,
    metric_names: Sequence[str] | None = None,
) -> TaskEvaluation:
    query_ids = list(dataset.queries)
    corpus_ids = list(dataset.corpus)
    query_texts = [dataset.queries[query_id] for query_id in query_ids]
    corpus_texts = [dataset.corpus[corpus_id] for corpus_id in corpus_ids]
    force_cpu_scoring = score_device == "cpu"
    force_cuda_scoring = score_device == "cuda"
    prefer_tensor_embeddings = not force_cpu_scoring and (
        force_cuda_scoring
        or _model_prefers_tensor_scoring(model)
        or _embedding_variants_use_torch_quantized_scoring(embedding_variants or [])
    )

    owns_encode_pool = encode_pool is None
    if encode_pool is None:
        encode_pool = start_encode_pool(model, encode_devices)
    try:
        query_start = time.perf_counter()
        query_embeddings = _encode(
            model,
            role="query",
            sentences=query_texts,
            batch_size=batch_size,
            show_progress=show_progress,
            prompt=query_prompt,
            prompt_name=query_prompt_name,
            task=query_task,
            truncate_dim=truncate_dim,
            prefer_tensor=prefer_tensor_embeddings,
            score_device=score_device,
            encode_pool=encode_pool,
            encode_chunk_size=encode_chunk_size,
        )
        query_seconds = time.perf_counter() - query_start

        corpus_start = time.perf_counter()
        corpus_embeddings = _encode(
            model,
            role="document",
            sentences=corpus_texts,
            batch_size=batch_size,
            show_progress=show_progress,
            prompt=corpus_prompt,
            prompt_name=corpus_prompt_name,
            task=corpus_task,
            truncate_dim=truncate_dim,
            prefer_tensor=prefer_tensor_embeddings,
            score_device=score_device,
            encode_pool=encode_pool,
            encode_chunk_size=encode_chunk_size,
        )
        corpus_seconds = time.perf_counter() - corpus_start
    finally:
        if owns_encode_pool:
            stop_encode_pool(model, encode_pool)
    query_embeddings = _move_embeddings_for_score_device(query_embeddings, score_device=score_device)
    corpus_embeddings = _move_embeddings_for_score_device(corpus_embeddings, score_device=score_device)
    base_postprocess_steps = _base_sparse_truncation_steps(
        truncate_sparse_query_max_dims=truncate_sparse_query_max_dims,
        truncate_sparse_docs_max_dims=truncate_sparse_docs_max_dims,
    )
    if base_postprocess_steps:
        query_embeddings, corpus_embeddings = _apply_embedding_pipeline_pair(
            query_embeddings=query_embeddings,
            corpus_embeddings=corpus_embeddings,
            steps=base_postprocess_steps,
        )

    preferred_score_name = _score_name(getattr(model, "similarity_fn_name", "cosine"))
    base_scoring = _score_embedding_distances(
        query_ids=query_ids,
        corpus_ids=corpus_ids,
        qrels=dataset.qrels,
        evaluator_name=dataset.evaluator_name,
        query_embeddings=query_embeddings,
        corpus_embeddings=corpus_embeddings,
        preferred_score_name=preferred_score_name,
        variant_name=None,
        aggregate_metric=aggregate_metric,
        candidates=dataset.candidates,
        rerank_top_n=rerank_top_n,
        candidate_ranking_name=candidate_ranking_name,
        metric_names=metric_names,
    )
    score_seconds = float(base_scoring["score_seconds"])
    metric_seconds = float(base_scoring["metric_seconds"])
    base_timing = {
        "query_embedding_seconds": float(query_seconds),
        "corpus_embedding_seconds": float(corpus_seconds),
        "score_and_topk_seconds": float(score_seconds),
        "metric_compute_seconds": float(metric_seconds),
        "pure_compute_seconds": float(query_seconds + corpus_seconds + score_seconds + metric_seconds),
    }
    embedding_conversion = {
        "query": _embedding_conversion_payload(
            text_count=len(query_texts),
            batch_size=batch_size,
            seconds=query_seconds,
        ),
        "docs": _embedding_conversion_payload(
            text_count=len(corpus_texts),
            batch_size=batch_size,
            seconds=corpus_seconds,
        ),
    }
    embedding_evaluations = [
        _embedding_evaluation_payload(
            name="base",
            transform=_postprocess_transform(base_postprocess_steps),
            embedding_dimensions=_embedding_dimensions(query_embeddings, corpus_embeddings),
            embedding_metadata=_embedding_metadata(query_embeddings, corpus_embeddings),
            scoring=base_scoring,
            timing=base_timing,
            aggregate_metric=aggregate_metric,
        )
    ]
    top_rankings = list(cast(list[dict[str, Any]], base_scoring["top_rankings"]))

    variant_score_seconds = 0.0
    variant_metric_seconds = 0.0
    for variant in embedding_variants or []:
        noop_truncate_dim = _noop_truncate_variant_dim(
            variant=variant,
            query_embeddings=query_embeddings,
            corpus_embeddings=corpus_embeddings,
        )
        if noop_truncate_dim is not None:
            _warn_skipped_noop_truncate_variant(variant_name=str(variant["name"]), dim=noop_truncate_dim)
            continue
        variant_query_embeddings, variant_corpus_embeddings = _apply_embedding_variant_pair(
            query_embeddings=query_embeddings,
            corpus_embeddings=corpus_embeddings,
            variant=variant,
        )
        variant_scoring = _score_embedding_distances(
            query_ids=query_ids,
            corpus_ids=corpus_ids,
            qrels=dataset.qrels,
            evaluator_name=dataset.evaluator_name,
            query_embeddings=variant_query_embeddings,
            corpus_embeddings=variant_corpus_embeddings,
            preferred_score_name=preferred_score_name,
            variant_name=str(variant["name"]),
            aggregate_metric=aggregate_metric,
            candidates=dataset.candidates,
            rerank_top_n=rerank_top_n,
            candidate_ranking_name=candidate_ranking_name,
            metric_names=metric_names,
        )
        variant_score_elapsed = float(variant_scoring["score_seconds"])
        variant_score_seconds += variant_score_elapsed

        variant_metric_elapsed = float(variant_scoring["metric_seconds"])
        variant_metric_seconds += variant_metric_elapsed
        top_rankings.extend(cast(list[dict[str, Any]], variant_scoring["top_rankings"]))
        embedding_evaluations.append(
            _embedding_evaluation_payload(
                name=str(variant["name"]),
                transform=dict(variant["transform"]),
                embedding_dimensions=_embedding_dimensions(variant_query_embeddings, variant_corpus_embeddings),
                embedding_metadata=_embedding_metadata(variant_query_embeddings, variant_corpus_embeddings),
                scoring=variant_scoring,
                timing={
                    "query_embedding_seconds": 0.0,
                    "corpus_embedding_seconds": 0.0,
                    "score_and_topk_seconds": float(variant_score_elapsed),
                    "metric_compute_seconds": float(variant_metric_elapsed),
                    "pure_compute_seconds": float(variant_score_elapsed + variant_metric_elapsed),
                },
                aggregate_metric=aggregate_metric,
            )
        )

    return TaskEvaluation(
        metrics=cast(dict[str, float], base_scoring["metrics"]),
        rerank_metrics=cast(dict[str, float], base_scoring["rerank_metrics"]),
        reranking_evaluations=[cast(dict[str, Any], base_scoring["reranking_evaluation"])],
        rerank_aggregate_metric_value=cast(float | None, base_scoring["rerank_aggregate_metric_value"]),
        timing={
            "query_embedding_seconds": float(query_seconds),
            "corpus_embedding_seconds": float(corpus_seconds),
            "score_and_topk_seconds": float(score_seconds),
            "metric_compute_seconds": float(metric_seconds),
            "embedding_variant_score_and_topk_seconds": float(variant_score_seconds),
            "embedding_variant_metric_compute_seconds": float(variant_metric_seconds),
            "pure_compute_seconds": float(
                query_seconds + corpus_seconds + score_seconds + metric_seconds + variant_score_seconds + variant_metric_seconds
            ),
        },
        embedding_conversion=embedding_conversion,
        embedding_evaluations=embedding_evaluations,
        top_rankings=top_rankings,
    )


def evaluate_reranker_task(
    *,
    model: Any,
    dataset: LoadedIrDataset,
    batch_size: int,
    show_progress: bool,
    rerank_top_n: int | None,
    candidate_ranking_name: str | None = DEFAULT_CANDIDATE_RANKING,
    aggregate_metric: str = "ndcg@10",
    score_kwargs: dict[str, Any] | None = None,
    metric_names: Sequence[str] | None = None,
) -> TaskEvaluation:
    if dataset.candidates is None:
        raise ValueError("Reranker evaluation requires a candidate subset such as bm25.")

    candidate_label = _candidate_ranking_score_label(candidate_ranking_name)
    effective_rerank_top_n = _effective_rerank_top_n(dataset.candidates, rerank_top_n)
    score_start = time.perf_counter()
    if _can_score_reranker_pairs(model):
        rankings = _rank_all_with_reranker_model(
            model,
            dataset=dataset,
            batch_size=batch_size,
            show_progress=show_progress,
            rerank_top_n=rerank_top_n,
            score_kwargs=score_kwargs or {},
        )
    else:
        rankings = {}
        for query_id, query_text in dataset.queries.items():
            candidate_ids = [doc_id for doc_id in dataset.candidates.get(query_id, []) if doc_id in dataset.corpus]
            if rerank_top_n is not None:
                candidate_ids = candidate_ids[:rerank_top_n]
            rankings[query_id] = _rank_with_reranker_model(
                model,
                query=query_text,
                candidate_ids=candidate_ids,
                documents=[dataset.corpus[doc_id] for doc_id in candidate_ids],
                batch_size=batch_size,
                show_progress=show_progress,
                score_kwargs=score_kwargs or {},
            )
    score_seconds = time.perf_counter() - score_start

    metric_start = time.perf_counter()
    metrics = compute_ir_metrics(
        rankings=rankings,
        qrels=dataset.qrels,
        evaluator_name=dataset.evaluator_name,
        score_name="reranker",
        metric_names=metric_names,
    )
    metric_seconds = time.perf_counter() - metric_start
    candidate_coverage = (
        candidate_coverage_for_qrels(
            qrels=dataset.qrels,
            candidates=dataset.candidates,
            top_k=effective_rerank_top_n,
        )
        if effective_rerank_top_n is not None
        else None
    )
    reranking_name = (
        f"{candidate_label}_top_{effective_rerank_top_n}" if effective_rerank_top_n is not None else f"{candidate_label}_all"
    )
    return TaskEvaluation(
        metrics=metrics,
        rerank_metrics=metrics,
        reranking_evaluations=[
            {
                "name": reranking_name,
                "source": "dataset_candidate_subset",
                "status": "available",
                "rerank_top_n": int(effective_rerank_top_n) if effective_rerank_top_n is not None else None,
                "aggregate_metric": aggregate_metric,
                "aggregate_metric_value": _aggregate_metric_value_for(metrics, aggregate_metric),
                "best_score": _aggregate_metric_value_for(metrics, aggregate_metric),
                "best_distance": "reranker",
                "best_score_name": "reranker",
                "metrics": metrics,
                "candidate_coverage": candidate_coverage,
            }
        ],
        rerank_aggregate_metric_value=_aggregate_metric_value_for(metrics, aggregate_metric),
        timing={
            "query_embedding_seconds": 0.0,
            "corpus_embedding_seconds": 0.0,
            "score_and_topk_seconds": float(score_seconds),
            "metric_compute_seconds": float(metric_seconds),
            "pure_compute_seconds": float(score_seconds + metric_seconds),
        },
        top_rankings=[
            top_ranking_payload(
                name="reranker",
                ranking_kind="candidate_rerank",
                embedding_variant_name=None,
                distance="reranker",
                score_name="reranker",
                rankings=rankings,
            )
        ],
    )


def evaluate_late_interaction_task(
    *,
    model: Any,
    dataset: LoadedIrDataset,
    batch_size: int,
    show_progress: bool,
    query_prompt: str | None,
    corpus_prompt: str | None,
    query_prompt_name: str | None,
    corpus_prompt_name: str | None,
    device: str | None,
    exact_doc_batch_size: int = 128,
    exact_query_batch_size: int = 8,
    aggregate_metric: str = "ndcg@10",
    embedding_variants: list[dict[str, Any]] | None = None,
) -> TaskEvaluation:
    if exact_doc_batch_size <= 0:
        raise ValueError("Late-interaction exact doc batch size must be positive.")
    if exact_query_batch_size <= 0:
        raise ValueError("Late-interaction exact query batch size must be positive.")

    query_ids = list(dataset.queries)
    corpus_ids = list(dataset.corpus)
    query_texts = [dataset.queries[query_id] for query_id in query_ids]
    corpus_texts = [dataset.corpus[corpus_id] for corpus_id in corpus_ids]

    query_start = time.perf_counter()
    query_embeddings = _encode_late_interaction(
        model,
        sentences=query_texts,
        batch_size=batch_size,
        show_progress=show_progress,
        prompt=query_prompt,
        prompt_name=query_prompt_name,
        is_query=True,
    )
    query_seconds = time.perf_counter() - query_start

    corpus_start = time.perf_counter()
    corpus_embeddings = _encode_late_interaction(
        model,
        sentences=corpus_texts,
        batch_size=batch_size,
        show_progress=show_progress,
        prompt=corpus_prompt,
        prompt_name=corpus_prompt_name,
        is_query=False,
    )
    corpus_seconds = time.perf_counter() - corpus_start

    ranking_depth = min(LATE_INTERACTION_RANKING_DEPTH, len(corpus_ids))
    score_start = time.perf_counter()
    rankings = _rank_late_interaction_exact_maxsim(
        query_ids=query_ids,
        corpus_ids=corpus_ids,
        query_embeddings=query_embeddings,
        corpus_embeddings=corpus_embeddings,
        top_k=ranking_depth,
        doc_batch_size=exact_doc_batch_size,
        query_batch_size=exact_query_batch_size,
        device=device,
        show_progress=show_progress,
    )
    score_seconds = time.perf_counter() - score_start
    index_payload = {
        "backend": "exact",
        "library": "torch",
        "index_type": "none",
        "ranking_depth": ranking_depth,
        "exact_doc_batch_size": exact_doc_batch_size,
        "exact_query_batch_size": exact_query_batch_size,
        "timing": {
            "index_build_or_load_seconds": 0.0,
            "retrieve_seconds": float(score_seconds),
        },
    }
    score_name = "late_interaction_exact_maxsim"
    distance_name = "exact_maxsim"

    metric_start = time.perf_counter()
    metrics = compute_ir_metrics(
        rankings=rankings,
        qrels=dataset.qrels,
        evaluator_name=dataset.evaluator_name,
        score_name=score_name,
    )
    metric_seconds = time.perf_counter() - metric_start
    aggregate_metric_value = _aggregate_metric_value_for(metrics, aggregate_metric)

    base_timing = {
        "query_embedding_seconds": float(query_seconds),
        "corpus_embedding_seconds": float(corpus_seconds),
        "score_and_topk_seconds": float(score_seconds),
        "metric_compute_seconds": float(metric_seconds),
        "embedding_variant_score_and_topk_seconds": 0.0,
        "embedding_variant_metric_compute_seconds": 0.0,
        "pure_compute_seconds": float(query_seconds + corpus_seconds + score_seconds + metric_seconds),
    }
    embedding_evaluation = _embedding_evaluation_payload(
        name="base",
        transform={"type": "identity", "algorithm": "none", "parameters": {}},
        embedding_dimensions=_embedding_dimensions(query_embeddings, corpus_embeddings),
        embedding_metadata=_embedding_metadata(query_embeddings, corpus_embeddings),
        scoring={
            "distance_evaluations": [
                {
                    "distance": distance_name,
                    "score_name": score_name,
                    "aggregate_metric": aggregate_metric,
                    "aggregate_metric_value": aggregate_metric_value,
                    "metrics": metrics,
                    "timing": {
                        "score_and_topk_seconds": float(score_seconds),
                        "metric_compute_seconds": float(metric_seconds),
                        "pure_compute_seconds": float(score_seconds + metric_seconds),
                    },
                }
            ],
            "metrics": metrics,
            "aggregate_metric_value": aggregate_metric_value,
            "best_score": aggregate_metric_value,
            "best_distance": distance_name,
            "best_score_name": score_name,
        },
        timing=base_timing,
        aggregate_metric=aggregate_metric,
    )
    embedding_evaluation["index"] = index_payload
    embedding_evaluations = [embedding_evaluation]
    top_rankings = [
        top_ranking_payload(
            name="base",
            ranking_kind="retrieval",
            embedding_variant_name=None,
            distance=distance_name,
            score_name=score_name,
            rankings=rankings,
        )
    ]

    variant_score_seconds = 0.0
    variant_metric_seconds = 0.0
    for variant in embedding_variants or []:
        variant_name = str(variant["name"])
        noop_truncate_dim = _noop_truncate_variant_dim(
            variant=variant,
            query_embeddings=query_embeddings,
            corpus_embeddings=corpus_embeddings,
        )
        if noop_truncate_dim is not None:
            _warn_skipped_noop_truncate_variant(variant_name=variant_name, dim=noop_truncate_dim)
            continue
        variant_query_embeddings, variant_corpus_embeddings = _apply_embedding_variant_pair(
            query_embeddings=query_embeddings,
            corpus_embeddings=corpus_embeddings,
            variant=variant,
        )
        variant_score_start = time.perf_counter()
        variant_rankings = _rank_late_interaction_exact_maxsim(
            query_ids=query_ids,
            corpus_ids=corpus_ids,
            query_embeddings=variant_query_embeddings,
            corpus_embeddings=variant_corpus_embeddings,
            top_k=ranking_depth,
            doc_batch_size=exact_doc_batch_size,
            query_batch_size=exact_query_batch_size,
            device=device,
            show_progress=show_progress,
        )
        variant_score_elapsed = time.perf_counter() - variant_score_start
        variant_score_seconds += variant_score_elapsed

        variant_metric_start = time.perf_counter()
        variant_score_name = f"{score_name}_{variant_name}"
        variant_metrics = compute_ir_metrics(
            rankings=variant_rankings,
            qrels=dataset.qrels,
            evaluator_name=dataset.evaluator_name,
            score_name=variant_score_name,
        )
        variant_metric_elapsed = time.perf_counter() - variant_metric_start
        variant_metric_seconds += variant_metric_elapsed
        variant_aggregate_metric_value = _aggregate_metric_value_for(variant_metrics, aggregate_metric)
        variant_evaluation = _embedding_evaluation_payload(
            name=variant_name,
            transform=dict(variant["transform"]),
            embedding_dimensions=_embedding_dimensions(variant_query_embeddings, variant_corpus_embeddings),
            embedding_metadata=_embedding_metadata(variant_query_embeddings, variant_corpus_embeddings),
            scoring={
                "distance_evaluations": [
                    {
                        "distance": distance_name,
                        "score_name": variant_score_name,
                        "aggregate_metric": aggregate_metric,
                        "aggregate_metric_value": variant_aggregate_metric_value,
                        "metrics": variant_metrics,
                        "timing": {
                            "score_and_topk_seconds": float(variant_score_elapsed),
                            "metric_compute_seconds": float(variant_metric_elapsed),
                            "pure_compute_seconds": float(variant_score_elapsed + variant_metric_elapsed),
                        },
                    }
                ],
                "metrics": variant_metrics,
                "aggregate_metric_value": variant_aggregate_metric_value,
                "best_score": variant_aggregate_metric_value,
                "best_distance": distance_name,
                "best_score_name": variant_score_name,
            },
            timing={
                "query_embedding_seconds": 0.0,
                "corpus_embedding_seconds": 0.0,
                "score_and_topk_seconds": float(variant_score_elapsed),
                "metric_compute_seconds": float(variant_metric_elapsed),
                "pure_compute_seconds": float(variant_score_elapsed + variant_metric_elapsed),
            },
            aggregate_metric=aggregate_metric,
        )
        variant_evaluation["index"] = {
            **index_payload,
            "timing": {
                "index_build_or_load_seconds": 0.0,
                "retrieve_seconds": float(variant_score_elapsed),
            },
        }
        embedding_evaluations.append(variant_evaluation)
        top_rankings.append(
            top_ranking_payload(
                name=variant_name,
                ranking_kind="retrieval",
                embedding_variant_name=variant_name,
                distance=distance_name,
                score_name=variant_score_name,
                rankings=variant_rankings,
            )
        )

    return TaskEvaluation(
        metrics=metrics,
        timing={
            "query_embedding_seconds": float(query_seconds),
            "corpus_embedding_seconds": float(corpus_seconds),
            "score_and_topk_seconds": float(score_seconds),
            "metric_compute_seconds": float(metric_seconds),
            "embedding_variant_score_and_topk_seconds": float(variant_score_seconds),
            "embedding_variant_metric_compute_seconds": float(variant_metric_seconds),
            "pure_compute_seconds": float(
                query_seconds
                + corpus_seconds
                + score_seconds
                + metric_seconds
                + variant_score_seconds
                + variant_metric_seconds
            ),
        },
        embedding_conversion={
            "query": _embedding_conversion_payload(
                text_count=len(query_texts),
                batch_size=batch_size,
                seconds=query_seconds,
            ),
            "docs": _embedding_conversion_payload(
                text_count=len(corpus_texts),
                batch_size=batch_size,
                seconds=corpus_seconds,
            ),
        },
        embedding_evaluations=embedding_evaluations,
        top_rankings=top_rankings,
    )


def _encode_late_interaction(
    model: Any,
    *,
    sentences: list[str],
    batch_size: int,
    show_progress: bool,
    prompt: str | None,
    prompt_name: str | None,
    is_query: bool,
) -> Any:
    kwargs: dict[str, Any] = {
        "batch_size": batch_size,
        "show_progress_bar": show_progress,
        "is_query": is_query,
    }
    if prompt is not None:
        kwargs["prompt"] = prompt
    elif prompt_name is not None:
        kwargs["prompt_name"] = prompt_name
    _ensure_late_interaction_encode_compat(model)
    return model.encode(sentences, **kwargs)


def _ensure_late_interaction_encode_compat(model: Any) -> None:
    if hasattr(model, "_text_length") or not hasattr(model, "_input_length"):
        return
    try:
        setattr(model, "_text_length", getattr(model, "_input_length"))
    except Exception:
        return


def _rank_late_interaction_exact_maxsim(
    *,
    query_ids: list[str],
    corpus_ids: list[str],
    query_embeddings: Any,
    corpus_embeddings: Any,
    top_k: int,
    doc_batch_size: int,
    query_batch_size: int,
    device: str | None,
    show_progress: bool = False,
) -> dict[str, list[str]]:
    if top_k <= 0:
        raise ValueError("Exact MaxSim top-k must be positive.")
    if doc_batch_size <= 0:
        raise ValueError("Exact MaxSim doc batch size must be positive.")
    if query_batch_size <= 0:
        raise ValueError("Exact MaxSim query batch size must be positive.")
    score_device = torch.device(device or ("cuda" if torch.cuda.is_available() else "cpu"))
    query_tensors = [_to_late_interaction_tensor(embedding, device=score_device) for embedding in query_embeddings]
    all_scores = torch.empty((len(query_ids), len(corpus_ids)), dtype=torch.float32)
    doc_ranges = range(0, len(corpus_ids), doc_batch_size)
    for doc_start in tqdm(doc_ranges, desc="Exact MaxSim document batches", disable=not show_progress):
        doc_end = min(doc_start + doc_batch_size, len(corpus_ids))
        batch_doc_embeddings = [
            _to_late_interaction_tensor(embedding, device=score_device)
            for embedding in corpus_embeddings[doc_start:doc_end]
        ]
        for query_start in range(0, len(query_ids), query_batch_size):
            query_end = min(query_start + query_batch_size, len(query_ids))
            scores = _exact_maxsim_scores_for_queries(
                query_tensors[query_start:query_end],
                batch_doc_embeddings,
            )
            all_scores[query_start:query_end, doc_start:doc_end] = scores

    rankings: dict[str, list[str]] = {}
    for query_index, query_id in enumerate(query_ids):
        query_scores = all_scores[query_index].tolist()
        ranked_indices = sorted(range(len(corpus_ids)), key=lambda index: (-query_scores[index], corpus_ids[index]))
        rankings[query_id] = [corpus_ids[index] for index in ranked_indices[:top_k]]
    return rankings


def _to_late_interaction_tensor(embedding: Any, *, device: torch.device) -> torch.Tensor:
    if isinstance(embedding, torch.Tensor):
        tensor = embedding.detach()
        if tensor.dtype is torch.bfloat16:
            tensor = tensor.float()
        return tensor.to(device=device, dtype=torch.float32)
    return torch.as_tensor(np.asarray(embedding), dtype=torch.float32, device=device)


def _exact_maxsim_scores_for_queries(
    query_embeddings: list[torch.Tensor],
    document_embeddings: list[torch.Tensor],
) -> torch.Tensor:
    if not query_embeddings:
        return torch.empty((0, len(document_embeddings)), dtype=torch.float32)
    if not document_embeddings:
        return torch.empty((len(query_embeddings), 0), dtype=torch.float32)
    for query_embedding in query_embeddings:
        if query_embedding.ndim != 2:
            raise ValueError(f"Query late-interaction embedding must be 2D, got shape {tuple(query_embedding.shape)}.")

    padded_queries = torch.nn.utils.rnn.pad_sequence(query_embeddings, batch_first=True, padding_value=0.0)
    padded_docs = torch.nn.utils.rnn.pad_sequence(document_embeddings, batch_first=True, padding_value=0.0)
    query_lengths = torch.as_tensor([query.shape[0] for query in query_embeddings], device=padded_queries.device)
    doc_lengths = torch.as_tensor([document.shape[0] for document in document_embeddings], device=padded_docs.device)
    query_positions = torch.arange(padded_queries.shape[1], device=padded_queries.device)
    doc_positions = torch.arange(padded_docs.shape[1], device=padded_docs.device)
    valid_query_tokens = query_positions.unsqueeze(0) < query_lengths.unsqueeze(1)
    valid_doc_tokens = doc_positions.unsqueeze(0) < doc_lengths.unsqueeze(1)

    with torch.no_grad():
        scores = torch.einsum("bth,qsh->bqts", padded_docs, padded_queries)
        scores = scores.masked_fill(~valid_doc_tokens[:, None, :, None], -torch.inf)
        maxsim = scores.max(dim=2).values
        maxsim = maxsim.masked_fill(~valid_query_tokens[None, :, :], 0.0)
        return maxsim.sum(dim=2).T.detach().cpu()


def _encode(
    model: Any,
    *,
    role: str,
    sentences: list[str],
    batch_size: int,
    show_progress: bool,
    prompt: str | None,
    prompt_name: str | None,
    task: str | None,
    truncate_dim: int | None,
    prefer_tensor: bool = False,
    score_device: str = "auto",
    encode_pool: dict[str, Any] | None = None,
    encode_chunk_size: int | None = None,
) -> Any:
    encode_fn = None if task is not None else getattr(model, "encode_query" if role == "query" else "encode_document", None)
    if encode_fn is None:
        encode_fn = model.encode

    kwargs: dict[str, Any] = {"batch_size": batch_size, "show_progress_bar": show_progress}
    if prompt is not None:
        kwargs["prompt"] = prompt
    elif prompt_name is not None:
        kwargs["prompt_name"] = prompt_name
    if task is not None:
        kwargs["task"] = task
    if truncate_dim is not None:
        kwargs["truncate_dim"] = truncate_dim
    if encode_pool is not None:
        if not _accepts_encode_parameter(encode_fn, "pool"):
            raise ValueError(
                "Multi-process SentenceTransformers encode was requested, but the selected encode method "
                f"does not accept a 'pool' parameter for {role} embeddings."
            )
        kwargs["pool"] = encode_pool
        if encode_chunk_size is not None:
            if not _accepts_encode_parameter(encode_fn, "chunk_size"):
                raise ValueError(
                    "Multi-process SentenceTransformers encode was requested with --encode-chunk-size, "
                    f"but the selected encode method does not accept a 'chunk_size' parameter for {role} embeddings."
                )
            kwargs["chunk_size"] = encode_chunk_size

    if _accepts_encode_parameter(encode_fn, "convert_to_sparse_tensor"):
        if encode_pool is not None:
            raise ValueError("Multi-process encode is not supported for sparse tensor encoding.")
        sparse_kwargs: dict[str, Any] = {
            "convert_to_tensor": True,
            "convert_to_sparse_tensor": True,
        }
        if _accepts_encode_parameter(encode_fn, "save_to_cpu"):
            sparse_kwargs["save_to_cpu"] = score_device == "cpu" or (
                score_device != "cuda" and not _model_prefers_tensor_scoring(model)
            )
        return encode_fn(sentences, **sparse_kwargs, **kwargs)

    if prefer_tensor:
        try:
            return encode_fn(sentences, convert_to_tensor=True, **kwargs)
        except TypeError:
            pass

    try:
        return encode_fn(sentences, convert_to_numpy=True, **kwargs)
    except TypeError:
        return encode_fn(sentences, **kwargs)


def start_encode_pool(model: Any, encode_devices: list[str] | None) -> dict[str, Any] | None:
    if not encode_devices:
        return None
    start_pool = getattr(model, "start_multi_process_pool", None)
    if not callable(start_pool):
        raise ValueError(
            "Multi-process SentenceTransformers encode was requested, but the loaded model does not provide "
            "start_multi_process_pool()."
        )
    return cast(dict[str, Any], start_pool(target_devices=encode_devices))


def stop_encode_pool(model: Any, encode_pool: dict[str, Any] | None) -> None:
    if encode_pool is None:
        return
    stop_pool = getattr(model, "stop_multi_process_pool", None)
    if not callable(stop_pool):
        raise ValueError(
            "Multi-process SentenceTransformers encode was started, but the loaded model does not provide "
            "stop_multi_process_pool()."
        )
    stop_pool(encode_pool)


def _move_embeddings_for_score_device(embeddings: Any, *, score_device: str) -> Any:
    if score_device != "cuda":
        return embeddings
    if not torch.cuda.is_available():
        raise ValueError("CUDA score_device was requested, but torch.cuda.is_available() is false.")
    device = torch.device("cuda")
    if isinstance(embeddings, torch.Tensor):
        return embeddings.to(device=device)
    if sparse.issparse(embeddings):
        return _to_torch_sparse_coo_matrix(embeddings, device=device)
    if isinstance(embeddings, np.ndarray):
        return torch.as_tensor(embeddings, dtype=torch.float32, device=device)
    return embeddings


def _accepts_encode_parameter(encode_fn: Any, name: str) -> bool:
    try:
        return name in inspect.signature(encode_fn).parameters
    except (TypeError, ValueError):
        return False


def _model_prefers_tensor_scoring(model: Any) -> bool:
    device_type = _model_device_type(model)
    return device_type is not None and device_type != "cpu"


def _model_device_type(model: Any) -> str | None:
    for attr_name in ("device", "_target_device"):
        device_type = _device_type(getattr(model, attr_name, None))
        if device_type is not None:
            return device_type

    parameters = getattr(model, "parameters", None)
    if callable(parameters):
        try:
            first_parameter = next(iter(parameters()))
        except StopIteration:
            return None
        except Exception:
            return None
        return _device_type(getattr(first_parameter, "device", None))
    return None


def _device_type(value: Any) -> str | None:
    if value is None:
        return None
    try:
        return torch.device(value).type
    except (TypeError, RuntimeError, ValueError):
        pass
    device_type = getattr(value, "type", None)
    return str(device_type) if device_type is not None else None


def _embedding_variants_use_torch_quantized_scoring(variants: list[dict[str, Any]]) -> bool:
    return any(_embedding_variant_uses_torch_quantized_scoring(variant) for variant in variants)


def _embedding_variant_uses_torch_quantized_scoring(variant: dict[str, Any]) -> bool:
    transform = variant.get("transform")
    if not isinstance(transform, dict):
        return False
    steps = transform.get("steps")
    if not isinstance(steps, list):
        return False
    for step in steps:
        if not isinstance(step, dict) or step.get("type") != "quantize":
            continue
        parameters = step.get("parameters", {})
        if not isinstance(parameters, dict):
            continue
        score_representation = _normalize_quantized_dense_score_representation(
            cast(str | None, parameters.get("score_representation"))
        )
        if score_representation in {TORCH_SCORE_REPRESENTATION, TORCH_RESCORE_SCORE_REPRESENTATION}:
            return True
    return False


def _embedding_conversion_payload(*, text_count: int, batch_size: int, seconds: float) -> dict[str, int | float | None]:
    seconds = float(seconds)
    return {
        "text_count": int(text_count),
        "batch_size": int(batch_size),
        "seconds": seconds,
        "texts_per_second": float(text_count / seconds) if seconds > 0.0 else None,
    }


def _can_score_reranker_pairs(model: Any) -> bool:
    return callable(getattr(model, "predict", None)) or callable(model)


def _rank_all_with_reranker_model(
    model: Any,
    *,
    dataset: LoadedIrDataset,
    batch_size: int,
    show_progress: bool,
    rerank_top_n: int | None,
    score_kwargs: dict[str, Any] | None = None,
) -> dict[str, list[str]]:
    if dataset.candidates is None:
        return {}
    rankings: dict[str, list[str]] = {}
    for query_id, query_text in dataset.queries.items():
        candidate_ids = [doc_id for doc_id in dataset.candidates.get(query_id, []) if doc_id in dataset.corpus]
        if rerank_top_n is not None:
            candidate_ids = candidate_ids[:rerank_top_n]
        query_scores: list[float] = []
        pair_chunk_size = min(max(batch_size, 1), 32)
        for offset in range(0, len(candidate_ids), pair_chunk_size):
            candidate_chunk = candidate_ids[offset : offset + pair_chunk_size]
            pairs = [[query_text, dataset.corpus[doc_id]] for doc_id in candidate_chunk]
            chunk_scores = _predict_scores(
                model,
                pairs=pairs,
                batch_size=batch_size,
                show_progress=show_progress,
                score_kwargs=score_kwargs,
            )
            if len(chunk_scores) != len(pairs):
                raise ValueError(f"Reranker returned {len(chunk_scores)} scores for {len(pairs)} query-document pairs.")
            query_scores.extend(float(score) for score in chunk_scores)
        ranked = sorted(zip(candidate_ids, query_scores, strict=True), key=lambda item: -float(item[1]))
        rankings[query_id] = [doc_id for doc_id, _score in ranked]
    return rankings


def _rank_with_reranker_model(
    model: Any,
    *,
    query: str,
    candidate_ids: list[str],
    documents: list[str],
    batch_size: int,
    show_progress: bool,
    score_kwargs: dict[str, Any] | None = None,
) -> list[str]:
    if not candidate_ids:
        return []
    score_kwargs = score_kwargs or {}

    rank_fn = getattr(model, "rank", None)
    if callable(rank_fn):
        raw_rankings = _call_with_supported_kwargs(
            rank_fn,
            query,
            documents,
            top_k=None,
            return_documents=False,
            batch_size=batch_size,
            show_progress_bar=show_progress,
            **score_kwargs,
        )
        parsed = _parse_rank_results(raw_rankings, candidate_ids=candidate_ids)
        if parsed:
            return parsed

    pairs = [[query, document] for document in documents]
    scores = _predict_scores(
        model,
        pairs=pairs,
        batch_size=batch_size,
        show_progress=show_progress,
        score_kwargs=score_kwargs,
    )
    ranked = sorted(zip(candidate_ids, scores, strict=True), key=lambda item: -float(item[1]))
    return [doc_id for doc_id, _score in ranked]


def _parse_rank_results(raw_rankings: Any, *, candidate_ids: list[str]) -> list[str]:
    if raw_rankings is None:
        return []
    parsed: list[tuple[str, float | None, int]] = []
    for position, item in enumerate(list(raw_rankings)):
        if isinstance(item, dict):
            raw_corpus_id = item.get("corpus_id")
            raw_score = item.get("score")
        else:
            raw_corpus_id = getattr(item, "corpus_id", None)
            raw_score = getattr(item, "score", None)
        doc_id = _candidate_id_from_rank_corpus_id(raw_corpus_id, candidate_ids=candidate_ids)
        if doc_id is None:
            continue
        score = float(raw_score) if isinstance(raw_score, int | float) else None
        parsed.append((doc_id, score, position))
    if not parsed:
        return []
    if any(score is not None for _doc_id, score, _position in parsed):
        parsed.sort(key=lambda item: (-(float("-inf") if item[1] is None else float(item[1])), item[0]))
    else:
        parsed.sort(key=lambda item: item[2])
    return [doc_id for doc_id, _score, _position in parsed]


def _candidate_id_from_rank_corpus_id(raw_corpus_id: Any, *, candidate_ids: list[str]) -> str | None:
    if isinstance(raw_corpus_id, int):
        return candidate_ids[raw_corpus_id] if 0 <= raw_corpus_id < len(candidate_ids) else None
    if isinstance(raw_corpus_id, str):
        if raw_corpus_id in candidate_ids:
            return raw_corpus_id
        if raw_corpus_id.isdigit():
            index = int(raw_corpus_id)
            return candidate_ids[index] if 0 <= index < len(candidate_ids) else None
    return None


def _predict_scores(
    model: Any,
    *,
    pairs: list[list[str]],
    batch_size: int,
    show_progress: bool,
    score_kwargs: dict[str, Any] | None = None,
) -> list[float]:
    if not pairs:
        return []
    score_kwargs = score_kwargs or {}
    predict_fn = getattr(model, "predict", None)
    if callable(predict_fn):
        raw_scores = _call_with_supported_kwargs(
            predict_fn,
            pairs,
            batch_size=batch_size,
            show_progress_bar=show_progress,
            **score_kwargs,
        )
    elif callable(model):
        raw_scores = _call_with_supported_kwargs(
            model,
            pairs,
            batch_size=batch_size,
            show_progress_bar=show_progress,
            **score_kwargs,
        )
    else:
        raise ValueError("Reranker model must expose rank, predict, or be callable.")
    if isinstance(raw_scores, torch.Tensor):
        raw_scores = raw_scores.detach().cpu().float().numpy()
    return [float(score) for score in np.asarray(raw_scores).reshape(-1).tolist()]


def _call_with_supported_kwargs(fn: Any, *args: Any, **kwargs: Any) -> Any:
    try:
        signature = inspect.signature(fn)
    except (TypeError, ValueError):
        return fn(*args, **kwargs)
    if any(parameter.kind is inspect.Parameter.VAR_KEYWORD for parameter in signature.parameters.values()):
        return fn(*args, **kwargs)
    supported_kwargs = {key: value for key, value in kwargs.items() if key in signature.parameters}
    return fn(*args, **supported_kwargs)


def _embedding_evaluation_payload(
    *,
    name: str,
    transform: dict[str, Any],
    embedding_dimensions: dict[str, int | None],
    embedding_metadata: dict[str, Any] | None,
    scoring: dict[str, Any],
    timing: dict[str, float],
    aggregate_metric: str,
) -> dict[str, Any]:
    payload = {
        "name": name,
        "transform": transform,
        "embedding_dimensions": embedding_dimensions,
        "aggregate_metric": aggregate_metric,
        "aggregate_metric_value": scoring["aggregate_metric_value"],
        "best_score": scoring["best_score"],
        "best_distance": scoring["best_distance"],
        "best_score_name": scoring["best_score_name"],
        "distance_evaluations": scoring["distance_evaluations"],
        "metrics": scoring["metrics"],
        "timing": timing,
    }
    if embedding_metadata is not None:
        payload["embedding_metadata"] = embedding_metadata
    if "reranking_evaluation" in scoring:
        payload["reranking_evaluation"] = scoring["reranking_evaluation"]
    return payload


def _aggregate_metric_value_for(metrics: dict[str, float], suffix: str) -> float:
    suffix = suffix.lower()
    values = [value for key, value in metrics.items() if key.lower().endswith(suffix)]
    if not values:
        raise ValueError(f"No metric ending with '{suffix}' found. Available metrics: {sorted(metrics)}")
    return float(np.mean(values))


def _score_embedding_distances(
    *,
    query_ids: list[str],
    corpus_ids: list[str],
    qrels: dict[str, set[str]],
    evaluator_name: str,
    query_embeddings: Any,
    corpus_embeddings: Any,
    preferred_score_name: str,
    variant_name: str | None,
    aggregate_metric: str,
    candidates: dict[str, list[str]] | None = None,
    rerank_top_n: int | None = DEFAULT_RERANK_TOP_K,
    candidate_ranking_name: str | None = DEFAULT_CANDIDATE_RANKING,
    metric_names: Sequence[str] | None = None,
) -> dict[str, Any]:
    distance_evaluations: list[dict[str, Any]] = []
    rerank_distance_evaluations: list[dict[str, Any]] = []
    rerank_metrics_by_distance: list[dict[str, float]] = []
    top_rankings: list[dict[str, Any]] = []
    effective_rerank_top_n = rerank_top_n if candidates is None else _effective_rerank_top_n(candidates, rerank_top_n)
    candidate_coverage = (
        candidate_coverage_for_qrels(qrels=qrels, candidates=candidates, top_k=effective_rerank_top_n)
        if candidates is not None and effective_rerank_top_n is not None
        else None
    )
    score_seconds = 0.0
    metric_seconds = 0.0
    for distance in _distance_names(preferred_score_name):
        metric_score_name = _metric_score_name(distance=distance, variant_name=variant_name)

        score_start = time.perf_counter()
        rankings = _rank_by_similarity(
            query_ids=query_ids,
            corpus_ids=corpus_ids,
            query_embeddings=query_embeddings,
            corpus_embeddings=corpus_embeddings,
            score_name=distance,
        )
        score_elapsed = time.perf_counter() - score_start
        score_seconds += score_elapsed

        metric_start = time.perf_counter()
        metrics = compute_ir_metrics(
            rankings=rankings,
            qrels=qrels,
            evaluator_name=evaluator_name,
            score_name=metric_score_name,
            metric_names=metric_names,
        )
        metric_elapsed = time.perf_counter() - metric_start
        metric_seconds += metric_elapsed
        top_rankings.append(
            top_ranking_payload(
                name=variant_name or "base",
                ranking_kind="retrieval",
                embedding_variant_name=variant_name,
                distance=distance,
                score_name=metric_score_name,
                rankings=rankings,
            )
        )

        if candidates is not None:
            candidate_label = _candidate_ranking_score_label(candidate_ranking_name)
            rerank_score_name = f"{metric_score_name}_{candidate_label}_top{effective_rerank_top_n}_rerank"
            rerank_metric_start = time.perf_counter()
            rerank_rankings = _rank_candidate_subset_by_similarity(
                query_ids=query_ids,
                corpus_ids=corpus_ids,
                query_embeddings=query_embeddings,
                corpus_embeddings=corpus_embeddings,
                candidates=candidates,
                score_name=distance,
                rerank_top_n=rerank_top_n,
            )
            rerank_metrics = compute_ir_metrics(
                rankings=rerank_rankings,
                qrels=qrels,
                evaluator_name=evaluator_name,
                score_name=rerank_score_name,
                metric_names=metric_names,
            )
            rerank_metric_elapsed = time.perf_counter() - rerank_metric_start
            metric_seconds += rerank_metric_elapsed
            rerank_aggregate_metric_value = _aggregate_metric_value_for(rerank_metrics, aggregate_metric)
            top_rankings.append(
                top_ranking_payload(
                    name=variant_name or "base",
                    ranking_kind="candidate_rerank",
                    embedding_variant_name=variant_name,
                    distance=distance,
                    score_name=rerank_score_name,
                    rankings=rerank_rankings,
                )
            )
            rerank_distance_evaluations.append(
                {
                    "distance": distance,
                    "score_name": rerank_score_name,
                    "aggregate_metric": aggregate_metric,
                    "aggregate_metric_value": rerank_aggregate_metric_value,
                    "metrics": rerank_metrics,
                    "timing": {
                        "score_and_topk_seconds": 0.0,
                        "metric_compute_seconds": float(rerank_metric_elapsed),
                        "pure_compute_seconds": float(rerank_metric_elapsed),
                    },
                }
            )
            rerank_metrics_by_distance.append(rerank_metrics)

        aggregate_metric_value = _aggregate_metric_value_for(metrics, aggregate_metric)
        distance_evaluations.append(
            {
                "distance": distance,
                "score_name": metric_score_name,
                "aggregate_metric": aggregate_metric,
                "aggregate_metric_value": aggregate_metric_value,
                "metrics": metrics,
                "timing": {
                    "score_and_topk_seconds": float(score_elapsed),
                    "metric_compute_seconds": float(metric_elapsed),
                    "pure_compute_seconds": float(score_elapsed + metric_elapsed),
                },
            }
        )

    best = max(distance_evaluations, key=lambda item: float(item["aggregate_metric_value"]))
    reranking_evaluation = _candidate_reranking_evaluation(
        rerank_distance_evaluations,
        rerank_top_n=effective_rerank_top_n,
        aggregate_metric=aggregate_metric,
        candidate_coverage=candidate_coverage,
        candidate_ranking_name=candidate_ranking_name,
    )
    return {
        "distance_evaluations": distance_evaluations,
        "metrics": best["metrics"],
        "aggregate_metric_value": best["aggregate_metric_value"],
        "best_score": best["aggregate_metric_value"],
        "best_distance": best["distance"],
        "best_score_name": best["score_name"],
        "rerank_metrics": _merge_metric_dicts(rerank_metrics_by_distance),
        "rerank_aggregate_metric_value": reranking_evaluation.get("aggregate_metric_value"),
        "reranking_evaluation": reranking_evaluation,
        "top_rankings": top_rankings,
        "score_seconds": score_seconds,
        "metric_seconds": metric_seconds,
    }


def top_ranking_payload(
    *,
    name: str,
    ranking_kind: str,
    embedding_variant_name: str | None,
    distance: str,
    score_name: str,
    rankings: dict[str, list[str]],
    top_k: int = TOP_RANKING_ARTIFACT_DEPTH,
) -> dict[str, Any]:
    return {
        "name": name,
        "ranking_kind": ranking_kind,
        "embedding_variant_name": embedding_variant_name,
        "distance": distance,
        "score_name": score_name,
        "rankings": {query_id: corpus_ids[:top_k] for query_id, corpus_ids in rankings.items()},
    }


def _rank_candidate_subset_by_similarity(
    *,
    query_ids: list[str],
    corpus_ids: list[str],
    query_embeddings: Any,
    corpus_embeddings: Any,
    candidates: dict[str, list[str]],
    score_name: str,
    rerank_top_n: int | None,
) -> dict[str, list[str]]:
    return rank_candidate_subset_by_similarity(
        query_ids=query_ids,
        corpus_ids=corpus_ids,
        query_embeddings=query_embeddings,
        corpus_embeddings=corpus_embeddings,
        candidates=candidates,
        score_name=score_name,
        rerank_top_n=rerank_top_n,
        rank_by_similarity=_rank_by_similarity,
    )


def _effective_rerank_top_n(candidates: dict[str, list[str]] | None, requested_top_n: int | None) -> int | None:
    if requested_top_n is not None:
        return requested_top_n
    if not candidates:
        return None
    max_count = 0
    for candidate_ids in candidates.values():
        seen: set[str] = set()
        for candidate_id in candidate_ids:
            seen.add(str(candidate_id))
        max_count = max(max_count, len(seen))
    return max_count or None


def _candidate_reranking_evaluation(
    distance_evaluations: list[dict[str, Any]],
    *,
    rerank_top_n: int | None,
    aggregate_metric: str,
    candidate_coverage: dict[str, int | float | None] | None = None,
    candidate_ranking_name: str | None = DEFAULT_CANDIDATE_RANKING,
) -> dict[str, Any]:
    candidate_label = _candidate_ranking_score_label(candidate_ranking_name)
    name = f"{candidate_label}_top_{rerank_top_n}" if rerank_top_n is not None else f"{candidate_label}_all"
    if not distance_evaluations:
        return {
            "name": name,
            "source": "dataset_candidate_subset",
            "status": "skipped",
            "reason": "candidate_subset_unavailable",
            "rerank_top_n": int(rerank_top_n) if rerank_top_n is not None else None,
        }
    best = max(distance_evaluations, key=lambda item: float(item["aggregate_metric_value"]))
    payload = {
        "name": name,
        "source": "dataset_candidate_subset",
        "status": "available",
        "rerank_top_n": int(rerank_top_n) if rerank_top_n is not None else None,
        "aggregate_metric": aggregate_metric,
        "aggregate_metric_value": best["aggregate_metric_value"],
        "best_score": best["aggregate_metric_value"],
        "best_distance": best["distance"],
        "best_score_name": best["score_name"],
        "distance_evaluations": distance_evaluations,
        "metrics": best["metrics"],
    }
    if candidate_coverage is not None:
        payload["candidate_coverage"] = candidate_coverage
    return payload


def _candidate_ranking_score_label(candidate_ranking_name: str | None) -> str:
    label = (candidate_ranking_name or "candidate").strip().lower()
    label = re.sub(r"[^a-z0-9]+", "_", label).strip("_")
    return label or "candidate"


def _merge_metric_dicts(metrics_by_distance: list[dict[str, float]]) -> dict[str, float]:
    merged: dict[str, float] = {}
    for metrics in metrics_by_distance:
        merged.update(metrics)
    return merged


def _distance_names(preferred_score_name: str) -> list[str]:
    names: list[str] = []
    for score_name in (preferred_score_name, "cosine", "dot"):
        if score_name in {"cosine", "dot"} and score_name not in names:
            names.append(score_name)
    return names or ["cosine", "dot"]


def _metric_score_name(*, distance: str, variant_name: str | None) -> str:
    if variant_name is None:
        return distance
    return f"{distance}_{variant_name}"


def _base_sparse_truncation_steps(
    *,
    truncate_sparse_query_max_dims: int | None,
    truncate_sparse_docs_max_dims: int | None,
) -> list[dict[str, Any]]:
    steps: list[dict[str, Any]] = []
    if truncate_sparse_query_max_dims is not None:
        steps.append(_truncate_sparse_max_dims_step(max_dims=truncate_sparse_query_max_dims, target="query"))
    if truncate_sparse_docs_max_dims is not None:
        steps.append(_truncate_sparse_max_dims_step(max_dims=truncate_sparse_docs_max_dims, target="corpus"))
    return steps


def _truncate_sparse_max_dims_step(*, max_dims: int, target: str) -> dict[str, Any]:
    return {
        "type": "truncate_sparse_max_dims",
        "algorithm": "top_abs_values_per_row",
        "parameters": {"max_dims": int(max_dims), "target": target},
    }


def _postprocess_transform(steps: list[dict[str, Any]]) -> dict[str, Any]:
    if not steps:
        return {"type": "identity", "algorithm": "none", "parameters": {}}
    return {"type": "pipeline", "steps": steps}


def _apply_embedding_variant_pair(
    *,
    query_embeddings: Any,
    corpus_embeddings: Any,
    variant: dict[str, Any],
) -> tuple[Any, Any]:
    transform = variant.get("transform", {})
    if transform.get("type") != "pipeline":
        raise ValueError(f"Unsupported embedding variant transform: {transform.get('type')}")
    steps = transform.get("steps")
    if not isinstance(steps, list) or not steps:
        raise ValueError("Embedding variant pipeline must contain at least one step.")
    return _apply_embedding_pipeline_pair(
        query_embeddings=query_embeddings,
        corpus_embeddings=corpus_embeddings,
        steps=steps,
    )


def _noop_truncate_variant_dim(
    *,
    variant: dict[str, Any],
    query_embeddings: Any,
    corpus_embeddings: Any,
) -> int | None:
    transform = variant.get("transform", {})
    if transform.get("type") != "pipeline":
        return None
    steps = transform.get("steps")
    if not isinstance(steps, list) or not steps:
        return None

    query_dim = _embedding_dimension(query_embeddings)
    corpus_dim = _embedding_dimension(corpus_embeddings)
    if query_dim is None or corpus_dim is None or query_dim != corpus_dim:
        return None

    truncate_dims: list[int] = []
    for step in steps:
        if step.get("type") != "truncate":
            continue
        parameters = step.get("parameters")
        if not isinstance(parameters, dict):
            return None
        dim = parameters.get("dim")
        if not isinstance(dim, int):
            return None
        truncate_dims.append(dim)
    if truncate_dims and all(dim == query_dim for dim in truncate_dims):
        return query_dim
    return None


def _warn_skipped_noop_truncate_variant(*, variant_name: str, dim: int) -> None:
    print(
        f"warning: skipping embedding variant {variant_name}: "
        f"truncate dimension {dim} matches the base embedding dimension, so it would duplicate the original result.",
        file=sys.stderr,
    )


def _apply_embedding_pipeline_pair(
    *,
    query_embeddings: Any,
    corpus_embeddings: Any,
    steps: list[dict[str, Any]],
) -> tuple[Any, Any]:
    # Keep every derived evaluation on this single post-encode pipeline path.
    # Cross variants such as truncate+quantize should reuse the one model
    # inference result and add only the minimal transform work needed per step.
    current_query_embeddings = query_embeddings
    current_corpus_embeddings = corpus_embeddings
    for step in steps:
        current_query_embeddings, current_corpus_embeddings = _apply_embedding_pipeline_step_pair(
            query_embeddings=current_query_embeddings,
            corpus_embeddings=current_corpus_embeddings,
            step=step,
        )
    return current_query_embeddings, current_corpus_embeddings


def _apply_embedding_pipeline_step_pair(
    *,
    query_embeddings: Any,
    corpus_embeddings: Any,
    step: dict[str, Any],
) -> tuple[Any, Any]:
    step_type = step.get("type")
    if step_type == "truncate":
        dim = int(step.get("parameters", {}).get("dim"))
        return _truncate_embeddings(query_embeddings, dim), _truncate_embeddings(corpus_embeddings, dim)
    if step_type == "normalize":
        algorithm = str(step.get("algorithm") or "l2")
        if algorithm != "l2":
            raise ValueError(f"Unsupported normalize algorithm: {algorithm}")
        return _normalize_embeddings(query_embeddings), _normalize_embeddings(corpus_embeddings)
    if step_type == "truncate_sparse_max_dims":
        max_dims = int(step.get("parameters", {}).get("max_dims"))
        target = str(step.get("parameters", {}).get("target") or "query_and_corpus")
        if target == "query":
            return (
                _limit_sparse_active_dims(query_embeddings, max_active_dims=max_dims),
                corpus_embeddings,
            )
        if target == "corpus":
            return (
                query_embeddings,
                _limit_sparse_active_dims(corpus_embeddings, max_active_dims=max_dims),
            )
        if target != "query_and_corpus":
            raise ValueError(f"Unsupported sparse truncation target: {target}")
        return (
            _limit_sparse_active_dims(query_embeddings, max_active_dims=max_dims),
            _limit_sparse_active_dims(corpus_embeddings, max_active_dims=max_dims),
        )
    if step_type == "quantize":
        parameters = step.get("parameters", {})
        precision = str(parameters.get("precision"))
        target = str(parameters.get("target") or "query_and_corpus")
        score_representation = parameters.get("score_representation")
        search_device = parameters.get("search_device")
        return _quantize_embedding_pair(
            query_embeddings=query_embeddings,
            corpus_embeddings=corpus_embeddings,
            precision=precision,
            target=target,
            algorithm=str(step.get("algorithm") or "sentence_transformers_embedding_quantization"),
            score_representation=str(score_representation) if score_representation is not None else None,
            search_device=str(search_device) if search_device is not None else None,
        )
    raise ValueError(f"Unsupported embedding variant pipeline step: {step_type}")


def _truncate_embeddings(embeddings: Any, dim: int) -> Any:
    if dim <= 0:
        raise ValueError("Truncate dimension must be positive.")
    if _is_late_interaction_embedding(embeddings):
        return _truncate_late_interaction_embeddings(embeddings, dim)
    if sparse.issparse(embeddings):
        if dim > embeddings.shape[1]:
            raise ValueError(f"Cannot truncate embeddings with dimension {embeddings.shape[1]} to {dim}.")
        return embeddings[:, :dim]
    if isinstance(embeddings, torch.Tensor):
        if dim > embeddings.shape[1]:
            raise ValueError(f"Cannot truncate embeddings with dimension {embeddings.shape[1]} to {dim}.")
        return embeddings[:, :dim]
    matrix = np.asarray(embeddings)
    if dim > matrix.shape[1]:
        raise ValueError(f"Cannot truncate embeddings with dimension {matrix.shape[1]} to {dim}.")
    return matrix[:, :dim]


def _truncate_late_interaction_embeddings(embeddings: Any, dim: int) -> Any:
    if isinstance(embeddings, list | tuple):
        return [_truncate_late_interaction_embedding(embedding, dim) for embedding in embeddings]
    return _truncate_late_interaction_embedding(embeddings, dim)


def _truncate_late_interaction_embedding(embedding: Any, dim: int) -> Any:
    shape = _shape_list(embedding)
    if len(shape) < 2:
        raise ValueError(f"Late-interaction embeddings must be at least 2D, got shape {shape}.")
    embedding_dim = int(shape[-1])
    if dim > embedding_dim:
        raise ValueError(f"Cannot truncate late-interaction embeddings with dimension {embedding_dim} to {dim}.")
    if isinstance(embedding, torch.Tensor):
        return embedding[..., :dim]
    matrix = np.asarray(embedding)
    return matrix[..., :dim]


def _normalize_embeddings(embeddings: Any) -> Any:
    if _is_torch_sparse_embedding(embeddings):
        return _torch_sparse_l2_normalize(embeddings)
    if _is_sparse_embedding(embeddings):
        return _sparse_l2_normalize(_to_scipy_csr_matrix(embeddings))
    if isinstance(embeddings, torch.Tensor):
        return _torch_l2_normalize(embeddings.detach().float())
    return _l2_normalize(_to_numpy_float32(embeddings))


def _limit_sparse_active_dims(embeddings: Any, *, max_active_dims: int) -> Any:
    if max_active_dims <= 0:
        raise ValueError("Sparse truncation max dims must be positive.")
    if not _is_sparse_embedding(embeddings):
        raise ValueError("Sparse truncation variants are only supported for sparse embeddings.")
    if _is_torch_sparse_embedding(embeddings):
        return _limit_torch_sparse_active_dims(embeddings, max_active_dims=max_active_dims)

    matrix = _to_scipy_csr_matrix(embeddings)
    if matrix.shape[0] == 0 or matrix.nnz == 0:
        return matrix.copy()

    indptr = matrix.indptr
    selected_indices: list[np.ndarray] = []
    selected_data: list[np.ndarray] = []
    new_indptr = [0]
    for row_index in range(matrix.shape[0]):
        start = int(indptr[row_index])
        end = int(indptr[row_index + 1])
        row_indices = matrix.indices[start:end]
        row_data = matrix.data[start:end]
        if row_data.size > max_active_dims:
            order = np.lexsort((row_indices, -np.abs(row_data)))
            keep = np.sort(order[:max_active_dims])
            row_indices = row_indices[keep]
            row_data = row_data[keep]
        selected_indices.append(row_indices)
        selected_data.append(row_data)
        new_indptr.append(new_indptr[-1] + int(row_data.size))

    indices = np.concatenate(selected_indices) if selected_indices else np.array([], dtype=matrix.indices.dtype)
    data = np.concatenate(selected_data) if selected_data else np.array([], dtype=matrix.data.dtype)
    return sparse.csr_matrix((data, indices, np.asarray(new_indptr, dtype=matrix.indptr.dtype)), shape=matrix.shape)


def _limit_torch_sparse_active_dims(embeddings: torch.Tensor, *, max_active_dims: int) -> torch.Tensor:
    matrix = _to_torch_sparse_coo_matrix(embeddings)
    if matrix.shape[0] == 0 or matrix._nnz() == 0:
        return matrix.clone()

    row_indices = matrix.indices()[0]
    col_indices = matrix.indices()[1]
    values = matrix.values()
    selected_indices: list[torch.Tensor] = []
    selected_values: list[torch.Tensor] = []
    for row_index in range(int(matrix.shape[0])):
        row_mask = row_indices == row_index
        row_positions = torch.nonzero(row_mask, as_tuple=False).flatten()
        if row_positions.numel() > max_active_dims:
            row_cols = col_indices.index_select(0, row_positions)
            row_values = values.index_select(0, row_positions)
            column_order = torch.argsort(row_cols, stable=True)
            row_positions = row_positions.index_select(0, column_order)
            row_values = row_values.index_select(0, column_order)
            value_order = torch.argsort(torch.abs(row_values), descending=True, stable=True)[:max_active_dims]
            row_positions = torch.sort(row_positions.index_select(0, value_order)).values
        selected_indices.append(matrix.indices().index_select(1, row_positions))
        selected_values.append(values.index_select(0, row_positions))

    if selected_indices:
        indices = torch.cat(selected_indices, dim=1)
        limited_values = torch.cat(selected_values, dim=0)
    else:
        indices = torch.empty((2, 0), dtype=torch.long, device=matrix.device)
        limited_values = torch.empty((0,), dtype=values.dtype, device=matrix.device)
    return torch.sparse_coo_tensor(
        indices,
        limited_values,
        size=tuple(int(dimension) for dimension in matrix.shape),
        device=matrix.device,
    ).coalesce()


def _quantize_embedding_pair(
    *,
    query_embeddings: Any,
    corpus_embeddings: Any,
    precision: str,
    target: str = "query_and_corpus",
    algorithm: str,
    score_representation: str | None = None,
    search_device: str | None = None,
) -> tuple[Any, Any]:
    score_representation = _normalize_quantized_dense_score_representation(score_representation)
    if _is_sparse_embedding(query_embeddings) or _is_sparse_embedding(corpus_embeddings):
        raise ValueError("Quantized embedding variants are not supported for sparse embeddings.")
    if precision not in {"int8", "binary"}:
        raise ValueError(f"Unsupported quantization precision: {precision}")
    precision_literal = cast(QuantizationPrecision, precision)
    target = _normalize_quantization_target(target)
    if target != "query_and_corpus":
        raise ValueError("Quantized search requires query_and_corpus quantization.")
    if score_representation in {TORCH_SCORE_REPRESENTATION, TORCH_RESCORE_SCORE_REPRESENTATION}:
        if precision_literal not in {"int8", "binary"}:
            raise ValueError("Quantized search scoring requires int8 or binary quantization.")
    if score_representation in {TORCH_SCORE_REPRESENTATION, TORCH_RESCORE_SCORE_REPRESENTATION}:
        return _quantize_torch_embedding_pair(
            query_embeddings=query_embeddings,
            corpus_embeddings=corpus_embeddings,
            precision=precision_literal,
            algorithm=algorithm,
            score_representation=score_representation,
            search_device=search_device,
        )
    method = "query_and_corpus"

    query_matrix = _to_numpy_float32(query_embeddings)
    corpus_matrix = _to_numpy_float32(corpus_embeddings)
    if query_matrix.ndim != 2 or corpus_matrix.ndim != 2:
        raise ValueError("Quantized embedding variants require 2D dense embeddings.")
    if query_matrix.shape[1] != corpus_matrix.shape[1]:
        raise ValueError(
            f"Cannot quantize query dimension {query_matrix.shape[1]} with corpus dimension {corpus_matrix.shape[1]}."
        )

    ranges = None
    ranges_source = None
    if precision_literal == "int8":
        if corpus_matrix.shape[0] == 0:
            raise ValueError("Cannot calibrate quantized embeddings from an empty corpus.")
        calibration_matrix = corpus_matrix
        ranges_source = "corpus"
        # Strict evaluation should not adapt quantization buckets to the eval
        # queries. Use corpus-only ranges, then clip query outliers to prevent
        # numpy int8 casts from wrapping values outside those ranges.
        ranges = np.vstack((np.min(calibration_matrix, axis=0), np.max(calibration_matrix, axis=0)))

    original_dim = int(query_matrix.shape[1])
    if precision_literal == "binary":
        corpus_values = _pack_binary_embeddings(corpus_matrix, precision=precision_literal)
        query_values = _pack_binary_embeddings(query_matrix, precision=precision_literal)
    else:
        if ranges is None:
            raise ValueError(f"Missing scalar quantization ranges for precision: {precision_literal}")
        corpus_values = _quantize_scalar_embeddings(corpus_matrix, precision=precision_literal, ranges=ranges)
        query_values = _quantize_scalar_embeddings(query_matrix, precision=precision_literal, ranges=ranges)
    corpus_quantized = QuantizedEmbeddingMatrix(
        values=corpus_values,
        precision=precision_literal,
        original_dim=original_dim,
        algorithm=algorithm,
        method=method,
        side="corpus",
        ranges_source=ranges_source,
        ranges=ranges.astype(np.float32, copy=True) if ranges is not None else None,
        rounding="truncate" if precision_literal == "int8" else None,
        score_representation=score_representation,
        source_values=corpus_matrix.astype(np.float32, copy=True)
        if score_representation in QUANTIZED_RESCORE_SCORE_REPRESENTATIONS
        else None,
    )
    return (
        QuantizedEmbeddingMatrix(
            values=query_values,
            precision=precision_literal,
            original_dim=original_dim,
            algorithm=algorithm,
            method=method,
            side="query",
            ranges_source=ranges_source,
            ranges=ranges.astype(np.float32, copy=True) if ranges is not None else None,
            rounding="truncate" if precision_literal == "int8" else None,
            score_representation=score_representation,
            source_values=query_matrix.astype(np.float32, copy=True)
            if score_representation in QUANTIZED_RESCORE_SCORE_REPRESENTATIONS
            else None,
        ),
        corpus_quantized,
    )


def _quantize_torch_embedding_pair(
    *,
    query_embeddings: Any,
    corpus_embeddings: Any,
    precision: QuantizationPrecision,
    algorithm: str,
    score_representation: str,
    search_device: str | None,
) -> tuple[QuantizedEmbeddingMatrix, QuantizedEmbeddingMatrix]:
    method = "query_and_corpus"
    device = _resolve_torch_search_device(query_embeddings, corpus_embeddings, search_device=search_device)
    query_matrix = _to_torch_float32(query_embeddings, device=device)
    corpus_matrix = _to_torch_float32(corpus_embeddings, device=device)
    if query_matrix.ndim != 2 or corpus_matrix.ndim != 2:
        raise ValueError("Quantized embedding variants require 2D dense embeddings.")
    if query_matrix.shape[1] != corpus_matrix.shape[1]:
        raise ValueError(
            f"Cannot quantize query dimension {query_matrix.shape[1]} with corpus dimension {corpus_matrix.shape[1]}."
        )

    ranges = None
    ranges_source = None
    if precision == "int8":
        if corpus_matrix.shape[0] == 0:
            raise ValueError("Cannot calibrate quantized embeddings from an empty corpus.")
        ranges_source = "corpus"
        ranges = torch.stack((torch.min(corpus_matrix, dim=0).values, torch.max(corpus_matrix, dim=0).values))

    original_dim = int(query_matrix.shape[1])
    binary_encoding = None
    if precision == "binary":
        corpus_values = _pack_binary_embeddings_torch(corpus_matrix)
        query_values = _pack_binary_embeddings_torch(query_matrix)
        binary_encoding = "unpacked_bits"
    else:
        if ranges is None:
            raise ValueError(f"Missing scalar quantization ranges for precision: {precision}")
        corpus_values = _quantize_scalar_embeddings_torch(corpus_matrix, precision=precision, ranges=ranges)
        query_values = _quantize_scalar_embeddings_torch(query_matrix, precision=precision, ranges=ranges)

    corpus_quantized = QuantizedEmbeddingMatrix(
        values=corpus_values,
        precision=precision,
        original_dim=original_dim,
        algorithm=algorithm,
        method=method,
        side="corpus",
        ranges_source=ranges_source,
        ranges=ranges.detach().clone() if ranges is not None else None,
        rounding="truncate" if precision == "int8" else None,
        score_representation=score_representation,
        source_values=corpus_matrix.detach().clone()
        if score_representation in QUANTIZED_RESCORE_SCORE_REPRESENTATIONS
        else None,
        binary_encoding=binary_encoding,
    )
    return (
        QuantizedEmbeddingMatrix(
            values=query_values,
            precision=precision,
            original_dim=original_dim,
            algorithm=algorithm,
            method=method,
            side="query",
            ranges_source=ranges_source,
            ranges=ranges.detach().clone() if ranges is not None else None,
            rounding="truncate" if precision == "int8" else None,
            score_representation=score_representation,
            source_values=query_matrix.detach().clone()
            if score_representation in QUANTIZED_RESCORE_SCORE_REPRESENTATIONS
            else None,
            binary_encoding=binary_encoding,
        ),
        corpus_quantized,
    )


def _resolve_torch_search_device(
    query_embeddings: Any,
    corpus_embeddings: Any,
    *,
    search_device: str | None,
) -> torch.device:
    if search_device is not None:
        device = torch.device(search_device)
        if device.type == "cuda" and not torch.cuda.is_available():
            raise ValueError("CUDA quantized search was requested, but torch.cuda.is_available() is false.")
        return device
    if isinstance(query_embeddings, torch.Tensor):
        return query_embeddings.device
    if isinstance(corpus_embeddings, torch.Tensor):
        return corpus_embeddings.device
    return torch.device("cpu")


def _to_torch_float32(embeddings: Any, *, device: torch.device | None = None) -> torch.Tensor:
    if isinstance(embeddings, torch.Tensor):
        tensor = embeddings.detach()
        if device is not None:
            tensor = tensor.to(device=device)
        return tensor.float()
    return torch.as_tensor(np.asarray(embeddings), dtype=torch.float32, device=device)


def _quantize_scalar_embeddings_torch(
    embeddings: torch.Tensor,
    *,
    precision: QuantizationPrecision,
    ranges: torch.Tensor,
) -> torch.Tensor:
    starts = ranges[0, :]
    steps = (ranges[1, :] - ranges[0, :]) / 255
    steps = torch.where(steps == 0, torch.ones_like(steps), steps)
    buckets = (embeddings - starts) / steps
    if precision == "int8":
        return torch.clamp(buckets - 128, min=-128, max=127).to(torch.int8)
    raise ValueError(f"Unsupported scalar quantization precision: {precision}")


def _pack_binary_embeddings_torch(embeddings: torch.Tensor) -> torch.Tensor:
    return (embeddings > 0).to(torch.int8)


def _normalize_quantization_target(target: str) -> str:
    normalized = target.strip().lower().replace("-", "_")
    if normalized in {"both", "query_and_corpus", "query_corpus", "query_and_document", "query_and_docs"}:
        return "query_and_corpus"
    raise ValueError(f"Unsupported quantization target: {target}")


def _normalize_quantized_dense_score_representation(value: str | None) -> str | None:
    if value is None:
        return None
    normalized = value.strip().lower().replace("-", "_")
    if normalized == "torch_exact":
        return TORCH_SCORE_REPRESENTATION
    if normalized == "torch_exact_rescore":
        return TORCH_RESCORE_SCORE_REPRESENTATION
    raise ValueError(f"Unsupported quantized dense score representation: {value}")


def _quantize_scalar_embeddings(
    embeddings: np.ndarray,
    *,
    precision: QuantizationPrecision,
    ranges: np.ndarray,
) -> np.ndarray:
    starts = ranges[0, :]
    steps = (ranges[1, :] - ranges[0, :]) / 255
    steps = np.where(steps == 0, 1, steps)
    buckets = (embeddings - starts) / steps
    if precision == "int8":
        return np.clip(buckets - 128, -128, 127).astype(np.int8)
    raise ValueError(f"Unsupported scalar quantization precision: {precision}")


def _pack_binary_embeddings(embeddings: np.ndarray, *, precision: QuantizationPrecision) -> np.ndarray:
    packed = np.packbits(embeddings > 0, axis=1)
    if precision == "binary":
        return (packed.astype(np.int16) - 128).astype(np.int8)
    raise ValueError(f"Unsupported binary quantization precision: {precision}")


def _dequantize_scalar_embeddings(embeddings: QuantizedEmbeddingMatrix) -> np.ndarray:
    if embeddings.precision != "int8":
        raise ValueError(f"Cannot scalar-dequantize precision: {embeddings.precision}")
    if embeddings.ranges is None:
        raise ValueError(f"Quantized {embeddings.precision} embeddings are missing dequantization ranges.")
    ranges = _to_numpy_float32(embeddings.ranges)
    values = _quantized_values_numpy(embeddings)
    starts = ranges[0, :]
    steps = (ranges[1, :] - ranges[0, :]) / 255
    steps = np.where(steps == 0, 1, steps)
    buckets = values.astype(np.float32)
    if embeddings.precision == "int8":
        buckets = buckets + 128
    return buckets * steps + starts


def _embedding_dimensions(query_embeddings: Any, corpus_embeddings: Any) -> dict[str, int | None]:
    query_dim = _embedding_dimension(query_embeddings)
    corpus_dim = _embedding_dimension(corpus_embeddings)
    if query_dim == corpus_dim:
        dimensions = {"dim": query_dim}
    else:
        dimensions = {"query_dim": query_dim, "corpus_dim": corpus_dim}

    if _is_packed_binary_quantized(query_embeddings) or _is_packed_binary_quantized(corpus_embeddings):
        query_stored_dim = _stored_embedding_dimension(query_embeddings)
        corpus_stored_dim = _stored_embedding_dimension(corpus_embeddings)
        if query_stored_dim == corpus_stored_dim:
            dimensions["stored_dim"] = query_stored_dim
        else:
            dimensions["query_stored_dim"] = query_stored_dim
            dimensions["corpus_stored_dim"] = corpus_stored_dim
    return dimensions


def _embedding_metadata(query_embeddings: Any, corpus_embeddings: Any) -> dict[str, Any] | None:
    dimensions = _embedding_dimensions(query_embeddings, corpus_embeddings)
    representation_type = _embedding_representation_type(query_embeddings, corpus_embeddings)
    return {
        "representation_type": representation_type,
        "dimension_format": _dimension_format(
            query_embeddings=query_embeddings,
            corpus_embeddings=corpus_embeddings,
            representation_type=representation_type,
        ),
        "dimensions": dimensions,
        "query": _embedding_side_metadata(query_embeddings),
        "corpus": _embedding_side_metadata(corpus_embeddings),
    }


def _embedding_representation_type(query_embeddings: Any, corpus_embeddings: Any) -> str:
    if _is_sparse_embedding(query_embeddings) or _is_sparse_embedding(corpus_embeddings):
        return "sparse"
    if _is_late_interaction_embedding(query_embeddings) or _is_late_interaction_embedding(corpus_embeddings):
        return "late_interaction"
    query_shape = _shape_list(query_embeddings)
    corpus_shape = _shape_list(corpus_embeddings)
    if _is_late_interaction_shape(query_shape) or _is_late_interaction_shape(corpus_shape):
        return "late_interaction"
    return "dense"


def _dimension_format(*, query_embeddings: Any, corpus_embeddings: Any, representation_type: str) -> str:
    query_packed = _is_packed_binary_quantized(query_embeddings)
    corpus_packed = _is_packed_binary_quantized(corpus_embeddings)
    if query_packed and corpus_packed:
        return "packed_binary_vector"
    if query_packed or corpus_packed:
        return "mixed_single_and_packed_binary_vector"
    if _is_unpacked_binary_quantized(query_embeddings) and _is_unpacked_binary_quantized(corpus_embeddings):
        return "binary_bit_vector"
    if representation_type == "sparse":
        return "sparse_vector"
    if representation_type == "late_interaction":
        return "multi_vector"
    return "single_vector"


def _embedding_side_metadata(embeddings: Any) -> dict[str, Any]:
    metadata: dict[str, Any] = {"shape": _shape_list(embeddings)}
    if _is_late_interaction_embedding(embeddings):
        metadata.update(_late_interaction_embedding_stats(embeddings))
    if isinstance(embeddings, torch.Tensor):
        metadata["value_dtype"] = str(embeddings.dtype)
        metadata["device"] = str(embeddings.device)
    if _is_quantized_embedding_matrix(embeddings):
        metadata["value_dtype"] = str(embeddings.dtype)
        metadata["quantization"] = _quantization_metadata(embeddings)
    if _is_sparse_embedding(embeddings):
        metadata.update(_sparse_embedding_stats(embeddings))
    return metadata


def _quantization_metadata(embeddings: QuantizedEmbeddingMatrix) -> dict[str, Any]:
    score_representation = _quantized_score_representation(embeddings)
    quantization: dict[str, Any] = {
        "precision": embeddings.precision,
        "algorithm": embeddings.algorithm,
        "original_dim": embeddings.original_dim,
        "stored_dim": _stored_embedding_dimension(embeddings),
        "score_representation": score_representation,
        "method": embeddings.method,
        "side": embeddings.side,
    }
    if embeddings.ranges_source is not None:
        quantization["ranges_source"] = embeddings.ranges_source
    if embeddings.rounding is not None:
        quantization["rounding"] = embeddings.rounding
    if embeddings.binary_encoding is not None:
        quantization["binary_encoding"] = embeddings.binary_encoding
    if score_representation in {TORCH_SCORE_REPRESENTATION, TORCH_RESCORE_SCORE_REPRESENTATION}:
        quantization["search_backend"] = "torch"
        quantization["search_exact"] = True
        quantization["candidate_top_k"] = QUANTIZED_CANDIDATE_TOP_K
        quantization["rescore"] = score_representation == TORCH_RESCORE_SCORE_REPRESENTATION
        if isinstance(embeddings.values, torch.Tensor):
            quantization["search_device"] = str(embeddings.values.device)
    return quantization


def _sparse_embedding_stats(embeddings: Any) -> dict[str, Any]:
    shape = _shape_list(embeddings)
    row_count = int(shape[0]) if shape else 0
    total_size = int(np.prod(shape)) if shape else 0
    if sparse.issparse(embeddings):
        matrix = sparse.csr_matrix(embeddings)
        row_nnz = np.diff(matrix.indptr)
        nnz_total = int(matrix.nnz)
    elif _is_torch_sparse_embedding(embeddings):
        if not embeddings.is_sparse:
            matrix = _to_scipy_csr_matrix(embeddings)
            row_nnz = np.diff(matrix.indptr)
            nnz_total = int(matrix.nnz)
        else:
            coalesced = embeddings.coalesce()
            row_indices = (
                coalesced.indices()[0].detach().cpu().numpy()
                if coalesced._nnz()
                else np.array([], dtype=np.int64)
            )
            row_nnz = np.bincount(row_indices, minlength=row_count)
            nnz_total = int(coalesced._nnz())
    else:
        return {}

    return {
        "nnz_total": nnz_total,
        "nnz_mean": float(np.mean(row_nnz)) if row_count else 0.0,
        "nnz_median": float(np.median(row_nnz)) if row_count else 0.0,
        "nnz_max": int(np.max(row_nnz)) if row_count else 0,
        "density": float(nnz_total / total_size) if total_size else 0.0,
    }


def _is_sparse_embedding(embeddings: Any) -> bool:
    return sparse.issparse(embeddings) or _is_torch_sparse_embedding(embeddings)


def _is_torch_sparse_embedding(embeddings: Any) -> bool:
    return isinstance(embeddings, torch.Tensor) and (
        embeddings.is_sparse or bool(getattr(embeddings, "is_sparse_csr", False))
    )


def _to_scipy_csr_matrix(embeddings: Any) -> sparse.csr_matrix:
    if sparse.issparse(embeddings):
        return sparse.csr_matrix(embeddings)
    if not _is_torch_sparse_embedding(embeddings):
        raise TypeError(f"Expected a sparse embedding matrix, got {type(embeddings).__name__}.")

    tensor = embeddings.detach()
    if bool(getattr(tensor, "is_sparse_csr", False)):
        tensor = tensor.cpu()
        return sparse.csr_matrix(
            (
                tensor.values().float().numpy(),
                tensor.col_indices().numpy(),
                tensor.crow_indices().numpy(),
            ),
            shape=tuple(int(dimension) for dimension in tensor.shape),
        )

    coalesced = tensor.coalesce().cpu()
    shape = tuple(int(dimension) for dimension in coalesced.shape)
    if len(shape) == 1:
        indices = coalesced.indices()[0].numpy() if coalesced._nnz() else np.array([], dtype=np.int64)
        rows = np.zeros_like(indices)
        cols = indices
        matrix_shape = (1, shape[0])
    elif len(shape) == 2:
        indices = coalesced.indices().numpy() if coalesced._nnz() else np.empty((2, 0), dtype=np.int64)
        rows = indices[0]
        cols = indices[1]
        matrix_shape = shape
    else:
        raise ValueError(f"Sparse embedding matrix must be 1D or 2D, got shape {shape}.")
    values = coalesced.values().float().numpy() if coalesced._nnz() else np.array([], dtype=np.float32)
    return sparse.csr_matrix((values, (rows, cols)), shape=matrix_shape)


def _is_quantized_embedding_matrix(embeddings: Any) -> bool:
    return isinstance(embeddings, QuantizedEmbeddingMatrix)


def _quantized_values_numpy(embeddings: QuantizedEmbeddingMatrix) -> np.ndarray:
    values = embeddings.values
    if isinstance(values, torch.Tensor):
        return values.detach().cpu().numpy()
    return np.asarray(values)


def _is_scalar_quantized(embeddings: Any) -> bool:
    return _is_quantized_embedding_matrix(embeddings) and embeddings.precision == "int8"


def _is_packed_binary_quantized(embeddings: Any) -> bool:
    return (
        _is_quantized_embedding_matrix(embeddings)
        and embeddings.precision == "binary"
        and embeddings.binary_encoding != "unpacked_bits"
    )


def _is_unpacked_binary_quantized(embeddings: Any) -> bool:
    return (
        _is_quantized_embedding_matrix(embeddings)
        and embeddings.precision == "binary"
        and embeddings.binary_encoding == "unpacked_bits"
    )


def _quantized_score_representation(embeddings: QuantizedEmbeddingMatrix) -> str:
    if embeddings.score_representation is not None:
        return embeddings.score_representation
    if embeddings.precision == "int8":
        return "dequantized_float32"
    if embeddings.precision == "binary":
        return "unpacked_sign_float32"
    return "stored_values_float32"


def _is_late_interaction_shape(shape: list[int]) -> bool:
    return len(shape) >= 3


def _is_late_interaction_embedding(embeddings: Any) -> bool:
    if isinstance(embeddings, torch.Tensor | np.ndarray):
        return len(getattr(embeddings, "shape", ())) >= 3
    if not isinstance(embeddings, list | tuple) or not embeddings:
        return False
    first_shape = _shape_list(embeddings[0])
    return len(first_shape) == 2


def _late_interaction_embedding_stats(embeddings: Any) -> dict[str, Any]:
    token_counts: list[int] = []
    value_dtype = None
    for embedding in list(embeddings):
        shape = _shape_list(embedding)
        if len(shape) >= 2:
            token_counts.append(int(shape[0]))
        if value_dtype is None and hasattr(embedding, "dtype"):
            value_dtype = str(embedding.dtype)
    metadata: dict[str, Any] = {
        "sequence_count": len(embeddings),
        "token_count_min": int(np.min(token_counts)) if token_counts else 0,
        "token_count_mean": float(np.mean(token_counts)) if token_counts else 0.0,
        "token_count_median": float(np.median(token_counts)) if token_counts else 0.0,
        "token_count_max": int(np.max(token_counts)) if token_counts else 0,
    }
    if value_dtype is not None:
        metadata["value_dtype"] = value_dtype
    return metadata


def _embedding_dimension(embeddings: Any) -> int | None:
    if _is_quantized_embedding_matrix(embeddings):
        return int(embeddings.original_dim)
    if _is_late_interaction_embedding(embeddings):
        if isinstance(embeddings, torch.Tensor | np.ndarray):
            return int(embeddings.shape[-1])
        for embedding in embeddings:
            shape = _shape_list(embedding)
            if len(shape) >= 2:
                return int(shape[-1])
        return None
    shape = _shape_list(embeddings)
    if len(shape) < 2:
        return None
    return int(shape[1])


def _stored_embedding_dimension(embeddings: Any) -> int | None:
    shape = _shape_list(embeddings)
    if len(shape) < 2:
        return None
    return int(shape[1])


def _shape_list(embeddings: Any) -> list[int]:
    if _is_quantized_embedding_matrix(embeddings):
        return [int(dimension) for dimension in embeddings.values.shape]
    if isinstance(embeddings, list | tuple):
        if not embeddings:
            return [0]
        child_shapes = [_shape_list(embedding) for embedding in embeddings]
        if child_shapes and all(len(shape) == 2 for shape in child_shapes):
            token_counts = [shape[0] for shape in child_shapes]
            dims = {shape[1] for shape in child_shapes}
            if len(dims) == 1:
                return [len(child_shapes), max(token_counts), next(iter(dims))]
    shape = getattr(embeddings, "shape", None)
    if shape is None:
        try:
            shape = np.asarray(embeddings).shape
        except Exception:
            return []
    return [int(dimension) for dimension in shape]


def _to_numpy_float32(embeddings: Any) -> np.ndarray:
    if _is_scalar_quantized(embeddings):
        return _dequantize_scalar_embeddings(embeddings)
    if _is_packed_binary_quantized(embeddings):
        return _unpack_binary_quantized_embeddings_as_sign_float32(embeddings)
    if _is_quantized_embedding_matrix(embeddings):
        return _quantized_values_numpy(embeddings).astype(np.float32, copy=False)
    if isinstance(embeddings, torch.Tensor):
        if embeddings.dtype is torch.bfloat16:
            embeddings = embeddings.float()
        return embeddings.detach().cpu().numpy().astype(np.float32, copy=False)
    return np.asarray(embeddings, dtype=np.float32)


def _score_name(value: Any) -> str:
    if hasattr(value, "value"):
        value = value.value
    value = str(value or "cosine").lower()
    if "." in value:
        value = value.rsplit(".", 1)[-1]
    return value


def _uses_torch_quantized_scoring(query_embeddings: Any, corpus_embeddings: Any) -> bool:
    if not _is_quantized_embedding_matrix(query_embeddings) or not _is_quantized_embedding_matrix(corpus_embeddings):
        return False
    score_representations = {
        _quantized_score_representation(query_embeddings),
        _quantized_score_representation(corpus_embeddings),
    }
    return bool(score_representations & {TORCH_SCORE_REPRESENTATION, TORCH_RESCORE_SCORE_REPRESENTATION})


def _is_torch_dense_pair(query_embeddings: Any, corpus_embeddings: Any) -> bool:
    return (
        isinstance(query_embeddings, torch.Tensor)
        and isinstance(corpus_embeddings, torch.Tensor)
        and not _is_torch_sparse_embedding(query_embeddings)
        and not _is_torch_sparse_embedding(corpus_embeddings)
        and query_embeddings.ndim == 2
        and corpus_embeddings.ndim == 2
    )


def _is_torch_late_interaction_pair(query_embeddings: Any, corpus_embeddings: Any) -> bool:
    return (
        isinstance(query_embeddings, torch.Tensor)
        and isinstance(corpus_embeddings, torch.Tensor)
        and not _is_torch_sparse_embedding(query_embeddings)
        and not _is_torch_sparse_embedding(corpus_embeddings)
        and query_embeddings.ndim >= 3
        and corpus_embeddings.ndim >= 3
    )


def _is_numpy_late_interaction_pair(query_embeddings: Any, corpus_embeddings: Any) -> bool:
    return (
        isinstance(query_embeddings, np.ndarray)
        and isinstance(corpus_embeddings, np.ndarray)
        and query_embeddings.ndim >= 3
        and corpus_embeddings.ndim >= 3
    )


def _rank_by_similarity(
    *,
    query_ids: list[str],
    corpus_ids: list[str],
    query_embeddings: Any,
    corpus_embeddings: Any,
    score_name: str,
) -> dict[str, list[str]]:
    if score_name == "hamming" and (
        _is_packed_binary_quantized(query_embeddings) or _is_packed_binary_quantized(corpus_embeddings)
    ):
        return _rank_packed_binary(
            query_ids=query_ids,
            corpus_ids=corpus_ids,
            query_embeddings=query_embeddings,
            corpus_embeddings=corpus_embeddings,
        )

    if _uses_torch_quantized_scoring(query_embeddings, corpus_embeddings):
        return _rank_torch_quantized(
            query_ids=query_ids,
            corpus_ids=corpus_ids,
            query_embeddings=cast(QuantizedEmbeddingMatrix, query_embeddings),
            corpus_embeddings=cast(QuantizedEmbeddingMatrix, corpus_embeddings),
            score_name=score_name,
        )

    if _is_torch_late_interaction_pair(query_embeddings, corpus_embeddings):
        return _rank_torch_late_interaction(
            query_ids=query_ids,
            corpus_ids=corpus_ids,
            query_embeddings=cast(torch.Tensor, query_embeddings),
            corpus_embeddings=cast(torch.Tensor, corpus_embeddings),
            score_name=score_name,
        )

    if _is_numpy_late_interaction_pair(query_embeddings, corpus_embeddings):
        return _rank_numpy_late_interaction(
            query_ids=query_ids,
            corpus_ids=corpus_ids,
            query_embeddings=cast(np.ndarray, query_embeddings),
            corpus_embeddings=cast(np.ndarray, corpus_embeddings),
            score_name=score_name,
        )

    if _is_torch_dense_pair(query_embeddings, corpus_embeddings):
        return _rank_torch_dense(
            query_ids=query_ids,
            corpus_ids=corpus_ids,
            query_embeddings=cast(torch.Tensor, query_embeddings),
            corpus_embeddings=cast(torch.Tensor, corpus_embeddings),
            score_name=score_name,
        )

    if _is_sparse_embedding(query_embeddings) or _is_sparse_embedding(corpus_embeddings):
        if _is_torch_sparse_embedding(query_embeddings) or _is_torch_sparse_embedding(corpus_embeddings):
            return _rank_torch_sparse(
                query_ids=query_ids,
                corpus_ids=corpus_ids,
                query_embeddings=query_embeddings,
                corpus_embeddings=corpus_embeddings,
                score_name=score_name,
            )
        return _rank_sparse(
            query_ids=query_ids,
            corpus_ids=corpus_ids,
            query_embeddings=query_embeddings,
            corpus_embeddings=corpus_embeddings,
            score_name=score_name,
        )

    query_matrix = _to_numpy_float32(query_embeddings)
    corpus_matrix = _to_numpy_float32(corpus_embeddings)
    if score_name == "cosine":
        query_matrix = _l2_normalize(query_matrix)
        corpus_matrix = _l2_normalize(corpus_matrix)
        scores = query_matrix @ corpus_matrix.T
    elif score_name == "euclidean":
        scores = -np.linalg.norm(query_matrix[:, None, :] - corpus_matrix[None, :, :], axis=2)
    elif score_name == "manhattan":
        scores = -np.abs(query_matrix[:, None, :] - corpus_matrix[None, :, :]).sum(axis=2)
    else:
        scores = query_matrix @ corpus_matrix.T

    return _scores_to_rankings(query_ids=query_ids, corpus_ids=corpus_ids, scores=scores)


def _rank_torch_dense(
    *,
    query_ids: list[str],
    corpus_ids: list[str],
    query_embeddings: torch.Tensor,
    corpus_embeddings: torch.Tensor,
    score_name: str,
) -> dict[str, list[str]]:
    query_matrix = _to_torch_float32(query_embeddings)
    corpus_matrix = _to_torch_float32(corpus_embeddings, device=query_matrix.device)
    if score_name == "cosine":
        query_matrix = _torch_l2_normalize(query_matrix)
        corpus_matrix = _torch_l2_normalize(corpus_matrix)
        scores = query_matrix @ corpus_matrix.T
    elif score_name == "euclidean":
        scores = -torch.linalg.vector_norm(query_matrix[:, None, :] - corpus_matrix[None, :, :], dim=2)
    elif score_name == "manhattan":
        scores = -torch.sum(torch.abs(query_matrix[:, None, :] - corpus_matrix[None, :, :]), dim=2)
    else:
        scores = query_matrix @ corpus_matrix.T
    return _torch_scores_to_rankings(query_ids=query_ids, corpus_ids=corpus_ids, scores=scores)


def _rank_torch_late_interaction(
    *,
    query_ids: list[str],
    corpus_ids: list[str],
    query_embeddings: torch.Tensor,
    corpus_embeddings: torch.Tensor,
    score_name: str,
) -> dict[str, list[str]]:
    query_matrix = _to_torch_float32(query_embeddings)
    corpus_matrix = _to_torch_float32(corpus_embeddings, device=query_matrix.device)
    if query_matrix.shape[-1] != corpus_matrix.shape[-1]:
        raise ValueError(
            f"Cannot rank late-interaction embeddings with query dimension {query_matrix.shape[-1]} "
            f"and corpus dimension {corpus_matrix.shape[-1]}."
        )
    if score_name == "cosine":
        query_matrix = torch.nn.functional.normalize(query_matrix, p=2, dim=-1)
        corpus_matrix = torch.nn.functional.normalize(corpus_matrix, p=2, dim=-1)
    elif score_name != "dot":
        raise ValueError(f"Late-interaction scoring supports cosine or dot, got {score_name}.")

    if corpus_matrix.shape[0] == 0:
        scores = torch.empty((int(query_matrix.shape[0]), 0), dtype=torch.float32, device=query_matrix.device)
        return _torch_scores_to_rankings(query_ids=query_ids, corpus_ids=corpus_ids, scores=scores)

    rows: list[torch.Tensor] = []
    corpus_chunk_size = 1024
    for query_tokens in query_matrix:
        chunk_scores: list[torch.Tensor] = []
        for corpus_start in range(0, int(corpus_matrix.shape[0]), corpus_chunk_size):
            corpus_chunk = corpus_matrix[corpus_start : corpus_start + corpus_chunk_size]
            similarities = torch.einsum("ld,cmd->clm", query_tokens, corpus_chunk)
            chunk_scores.append(torch.max(similarities, dim=2).values.sum(dim=1))
        rows.append(torch.cat(chunk_scores, dim=0))
    scores = torch.stack(rows, dim=0) if rows else torch.empty((0, len(corpus_ids)), device=corpus_matrix.device)
    return _torch_scores_to_rankings(query_ids=query_ids, corpus_ids=corpus_ids, scores=scores)


def _rank_numpy_late_interaction(
    *,
    query_ids: list[str],
    corpus_ids: list[str],
    query_embeddings: np.ndarray,
    corpus_embeddings: np.ndarray,
    score_name: str,
) -> dict[str, list[str]]:
    query_matrix = _to_numpy_float32(query_embeddings)
    corpus_matrix = _to_numpy_float32(corpus_embeddings)
    if query_matrix.shape[-1] != corpus_matrix.shape[-1]:
        raise ValueError(
            f"Cannot rank late-interaction embeddings with query dimension {query_matrix.shape[-1]} "
            f"and corpus dimension {corpus_matrix.shape[-1]}."
        )
    if score_name == "cosine":
        query_matrix = _l2_normalize(query_matrix)
        corpus_matrix = _l2_normalize(corpus_matrix)
    elif score_name != "dot":
        raise ValueError(f"Late-interaction scoring supports cosine or dot, got {score_name}.")

    if corpus_matrix.shape[0] == 0:
        return _scores_to_rankings(
            query_ids=query_ids,
            corpus_ids=corpus_ids,
            scores=np.empty((query_matrix.shape[0], 0), dtype=np.float32),
        )

    corpus_chunk_size = 1024
    query_chunk_size = _numpy_late_interaction_query_chunk_size(
        query_matrix=query_matrix,
        corpus_matrix=corpus_matrix,
        corpus_chunk_size=corpus_chunk_size,
    )
    rows: list[np.ndarray] = []
    for query_start in range(0, int(query_matrix.shape[0]), query_chunk_size):
        query_chunk = query_matrix[query_start : query_start + query_chunk_size]
        corpus_scores: list[np.ndarray] = []
        for corpus_start in range(0, int(corpus_matrix.shape[0]), corpus_chunk_size):
            corpus_chunk = corpus_matrix[corpus_start : corpus_start + corpus_chunk_size]
            similarities = np.einsum("qld,cmd->qclm", query_chunk, corpus_chunk, optimize=True)
            corpus_scores.append(np.max(similarities, axis=3).sum(axis=2))
        rows.append(np.concatenate(corpus_scores, axis=1))
    scores = np.concatenate(rows, axis=0) if rows else np.empty((0, len(corpus_ids)), dtype=np.float32)
    return _scores_to_rankings(query_ids=query_ids, corpus_ids=corpus_ids, scores=scores)


def _numpy_late_interaction_query_chunk_size(
    *,
    query_matrix: np.ndarray,
    corpus_matrix: np.ndarray,
    corpus_chunk_size: int,
) -> int:
    target_bytes = 256 * 1024 * 1024
    bytes_per_score_block = int(query_matrix.shape[1]) * corpus_chunk_size * int(corpus_matrix.shape[1]) * 4
    if bytes_per_score_block <= 0:
        return 1
    return max(1, min(int(query_matrix.shape[0]), target_bytes // bytes_per_score_block))


def _rank_torch_quantized(
    *,
    query_ids: list[str],
    corpus_ids: list[str],
    query_embeddings: QuantizedEmbeddingMatrix,
    corpus_embeddings: QuantizedEmbeddingMatrix,
    score_name: str,
) -> dict[str, list[str]]:
    if query_embeddings.precision != corpus_embeddings.precision:
        raise ValueError(
            f"Cannot rank torch embeddings with query precision {query_embeddings.precision} "
            f"and corpus precision {corpus_embeddings.precision}."
        )
    if query_embeddings.original_dim != corpus_embeddings.original_dim:
        raise ValueError(
            f"Cannot rank torch embeddings with query dimension {query_embeddings.original_dim} "
            f"and corpus dimension {corpus_embeddings.original_dim}."
        )
    query_score_representation = _quantized_score_representation(query_embeddings)
    corpus_score_representation = _quantized_score_representation(corpus_embeddings)
    if query_score_representation != corpus_score_representation:
        raise ValueError(
            f"Cannot rank torch embeddings with query score representation {query_score_representation} "
            f"and corpus score representation {corpus_score_representation}."
        )

    final_count = min(len(corpus_ids), QUANTIZED_CANDIDATE_TOP_K)
    indices = _torch_quantized_candidate_indices(
        query_embeddings=query_embeddings,
        corpus_embeddings=corpus_embeddings,
        corpus_ids=corpus_ids,
        count=final_count,
    )
    if query_score_representation == TORCH_RESCORE_SCORE_REPRESENTATION:
        return _rescore_torch_quantized_candidates(
            query_ids=query_ids,
            corpus_ids=corpus_ids,
            candidate_indices=indices,
            query_embeddings=query_embeddings,
            corpus_embeddings=corpus_embeddings,
            score_name=score_name,
            final_count=final_count,
        )

    indices_cpu = indices.detach().cpu().numpy()
    rankings: dict[str, list[str]] = {}
    for query_index, query_id in enumerate(query_ids):
        rankings[query_id] = [corpus_ids[int(index)] for index in indices_cpu[query_index, :final_count]]
    return rankings


def _torch_quantized_candidate_indices(
    *,
    query_embeddings: QuantizedEmbeddingMatrix,
    corpus_embeddings: QuantizedEmbeddingMatrix,
    corpus_ids: list[str],
    count: int,
) -> torch.Tensor:
    query_values = _quantized_values_torch(query_embeddings)
    corpus_values = _quantized_values_torch(corpus_embeddings, device=query_values.device)
    if query_embeddings.precision == "int8":
        scores = query_values.float() @ corpus_values.float().T
        return _torch_top_k_indices_by_scores(scores=scores, corpus_ids=corpus_ids, count=count)
    if query_embeddings.precision == "binary":
        query_bits = query_values.float()
        corpus_bits = corpus_values.float()
        shared_bits = query_bits @ corpus_bits.T
        query_active_bits = torch.sum(query_bits, dim=1, keepdim=True)
        corpus_active_bits = torch.sum(corpus_bits, dim=1, keepdim=True).T
        distances = query_active_bits + corpus_active_bits - (2 * shared_bits)
        return _torch_top_k_indices_by_scores(scores=-distances, corpus_ids=corpus_ids, count=count)
    raise ValueError(f"Unsupported torch quantization precision: {query_embeddings.precision}")


def _quantized_values_torch(
    embeddings: QuantizedEmbeddingMatrix,
    *,
    device: torch.device | None = None,
) -> torch.Tensor:
    values = embeddings.values
    if isinstance(values, torch.Tensor):
        tensor = values.detach()
        return tensor.to(device=device) if device is not None else tensor
    return torch.as_tensor(values, device=device)


def _torch_top_k_indices_by_scores(*, scores: torch.Tensor, corpus_ids: list[str], count: int) -> torch.Tensor:
    if count <= 0 or scores.shape[0] == 0:
        return torch.empty((int(scores.shape[0]), 0), dtype=torch.long, device=scores.device)
    lexical_indices = torch.as_tensor(_corpus_lexical_indices(corpus_ids), dtype=torch.long, device=scores.device)
    lexical_scores = scores.index_select(1, lexical_indices)
    sorted_positions = torch.argsort(lexical_scores, dim=1, descending=True, stable=True)
    return lexical_indices[sorted_positions[:, :count]]


def _corpus_lexical_indices(corpus_ids: list[str]) -> np.ndarray:
    return np.argsort(np.asarray(corpus_ids)).astype(np.int64, copy=False)


def _rescore_torch_quantized_candidates(
    *,
    query_ids: list[str],
    corpus_ids: list[str],
    candidate_indices: torch.Tensor,
    query_embeddings: QuantizedEmbeddingMatrix,
    corpus_embeddings: QuantizedEmbeddingMatrix,
    score_name: str,
    final_count: int,
) -> dict[str, list[str]]:
    if query_embeddings.source_values is None or corpus_embeddings.source_values is None:
        raise ValueError("Torch quantized rescore requires source float embeddings.")
    query_matrix = _to_torch_float32(query_embeddings.source_values)
    corpus_matrix = _to_torch_float32(corpus_embeddings.source_values, device=query_matrix.device)
    if score_name == "cosine":
        query_matrix = _torch_l2_normalize(query_matrix)
        corpus_matrix = _torch_l2_normalize(corpus_matrix)

    rankings: dict[str, list[str]] = {}
    for query_index, query_id in enumerate(query_ids):
        candidates = candidate_indices[query_index]
        candidates = candidates[candidates >= 0].to(device=query_matrix.device, dtype=torch.long)
        if score_name == "euclidean":
            scores = -torch.linalg.vector_norm(corpus_matrix.index_select(0, candidates) - query_matrix[query_index], dim=1)
        elif score_name == "manhattan":
            scores = -torch.sum(torch.abs(corpus_matrix.index_select(0, candidates) - query_matrix[query_index]), dim=1)
        else:
            scores = corpus_matrix.index_select(0, candidates) @ query_matrix[query_index]
        candidates_cpu = candidates.detach().cpu().numpy().tolist()
        scores_cpu = scores.detach().cpu().numpy().tolist()
        ordered = sorted(
            zip(candidates_cpu, scores_cpu, strict=True),
            key=lambda item: (-float(item[1]), corpus_ids[int(item[0])]),
        )
        rankings[query_id] = [corpus_ids[int(index)] for index, _score in ordered[:final_count]]
    return rankings


def _rank_packed_binary(
    *,
    query_ids: list[str],
    corpus_ids: list[str],
    query_embeddings: Any,
    corpus_embeddings: Any,
) -> dict[str, list[str]]:
    if not _is_packed_binary_quantized(query_embeddings) or not _is_packed_binary_quantized(corpus_embeddings):
        raise ValueError("Packed binary ranking requires quantized binary query and corpus embeddings.")
    if query_embeddings.original_dim != corpus_embeddings.original_dim:
        raise ValueError(
            f"Cannot rank binary embeddings with query dimension {query_embeddings.original_dim} "
            f"and corpus dimension {corpus_embeddings.original_dim}."
        )

    query_bits = _unpack_binary_quantized_embeddings(query_embeddings)
    corpus_bits = _unpack_binary_quantized_embeddings(corpus_embeddings)
    distances = np.bitwise_xor(query_bits[:, None, :], corpus_bits[None, :, :]).sum(axis=2)
    scores = -distances.astype(np.float32)
    return _scores_to_rankings(query_ids=query_ids, corpus_ids=corpus_ids, scores=scores)


def _unpack_binary_quantized_embeddings(embeddings: QuantizedEmbeddingMatrix) -> np.ndarray:
    values = _quantized_values_numpy(embeddings)
    if embeddings.binary_encoding == "unpacked_bits":
        return values.astype(np.uint8, copy=False)[:, : embeddings.original_dim]
    packed = values
    if embeddings.precision == "binary":
        packed = (packed.astype(np.int16) + 128).astype(np.uint8)
    return np.unpackbits(packed, axis=1)[:, : embeddings.original_dim]


def _unpack_binary_quantized_embeddings_as_sign_float32(embeddings: QuantizedEmbeddingMatrix) -> np.ndarray:
    bits = _unpack_binary_quantized_embeddings(embeddings).astype(np.float32, copy=False)
    return bits * 2.0 - 1.0


def _rank_sparse(
    *,
    query_ids: list[str],
    corpus_ids: list[str],
    query_embeddings: Any,
    corpus_embeddings: Any,
    score_name: str,
) -> dict[str, list[str]]:
    query_matrix = _to_scipy_csr_matrix(query_embeddings)
    corpus_matrix = _to_scipy_csr_matrix(corpus_embeddings)
    if query_matrix.shape[1] < corpus_matrix.shape[1]:
        query_matrix.resize((query_matrix.shape[0], corpus_matrix.shape[1]))
    elif corpus_matrix.shape[1] < query_matrix.shape[1]:
        corpus_matrix.resize((corpus_matrix.shape[0], query_matrix.shape[1]))
    if score_name == "cosine":
        query_matrix = _sparse_l2_normalize(query_matrix)
        corpus_matrix = _sparse_l2_normalize(corpus_matrix)
    scores = (query_matrix @ corpus_matrix.T).tocsr()
    return _sparse_scores_to_rankings(query_ids=query_ids, corpus_ids=corpus_ids, scores=scores)


def _rank_torch_sparse(
    *,
    query_ids: list[str],
    corpus_ids: list[str],
    query_embeddings: Any,
    corpus_embeddings: Any,
    score_name: str,
) -> dict[str, list[str]]:
    device = query_embeddings.device if isinstance(query_embeddings, torch.Tensor) else corpus_embeddings.device
    query_matrix = _to_torch_sparse_coo_matrix(query_embeddings, device=device)
    corpus_matrix = _to_torch_sparse_coo_matrix(corpus_embeddings, device=device)
    if query_matrix.shape[1] < corpus_matrix.shape[1]:
        query_matrix = _resize_torch_sparse_columns(query_matrix, int(corpus_matrix.shape[1]))
    elif corpus_matrix.shape[1] < query_matrix.shape[1]:
        corpus_matrix = _resize_torch_sparse_columns(corpus_matrix, int(query_matrix.shape[1]))
    if score_name == "cosine":
        query_matrix = _torch_sparse_l2_normalize(query_matrix)
        corpus_matrix = _torch_sparse_l2_normalize(corpus_matrix)
    scores = torch.sparse.mm(query_matrix, corpus_matrix.transpose(0, 1)).to_dense()
    return _torch_scores_to_rankings(query_ids=query_ids, corpus_ids=corpus_ids, scores=scores)


def _sparse_scores_to_rankings(
    *,
    query_ids: list[str],
    corpus_ids: list[str],
    scores: sparse.csr_matrix,
) -> dict[str, list[str]]:
    rankings: dict[str, list[str]] = {}
    for query_index, query_id in enumerate(query_ids):
        row = scores.getrow(query_index)
        score_by_index = {int(index): float(score) for index, score in zip(row.indices, row.data, strict=True)}
        ordered_indices = sorted(
            range(len(corpus_ids)),
            key=lambda corpus_index: (-score_by_index.get(corpus_index, 0.0), corpus_ids[corpus_index]),
        )
        rankings[query_id] = [corpus_ids[index] for index in ordered_indices]
    return rankings


def _scores_to_rankings(*, query_ids: list[str], corpus_ids: list[str], scores: np.ndarray) -> dict[str, list[str]]:
    rankings: dict[str, list[str]] = {}
    for query_index, query_id in enumerate(query_ids):
        ordered_indices = sorted(
            range(len(corpus_ids)),
            key=lambda corpus_index: (-float(scores[query_index, corpus_index]), corpus_ids[corpus_index]),
        )
        rankings[query_id] = [corpus_ids[index] for index in ordered_indices]
    return rankings


def _torch_scores_to_rankings(*, query_ids: list[str], corpus_ids: list[str], scores: torch.Tensor) -> dict[str, list[str]]:
    indices = _torch_top_k_indices_by_scores(scores=scores, corpus_ids=corpus_ids, count=len(corpus_ids))
    indices_cpu = indices.detach().cpu().numpy()
    rankings: dict[str, list[str]] = {}
    for query_index, query_id in enumerate(query_ids):
        rankings[query_id] = [corpus_ids[int(index)] for index in indices_cpu[query_index]]
    return rankings


def _l2_normalize(matrix: np.ndarray) -> np.ndarray:
    norms = np.linalg.norm(matrix, axis=1, keepdims=True)
    norms[norms == 0.0] = 1.0
    return matrix / norms


def _torch_l2_normalize(matrix: torch.Tensor) -> torch.Tensor:
    norms = torch.linalg.vector_norm(matrix, dim=1, keepdim=True)
    norms = torch.where(norms == 0.0, torch.ones_like(norms), norms)
    return matrix / norms


def _to_torch_sparse_coo_matrix(embeddings: Any, *, device: torch.device | None = None) -> torch.Tensor:
    if isinstance(embeddings, torch.Tensor):
        tensor = embeddings.detach()
        if device is not None:
            tensor = tensor.to(device=device)
        if not _is_torch_sparse_embedding(tensor):
            tensor = tensor.to_sparse()
        if bool(getattr(tensor, "is_sparse_csr", False)):
            tensor = tensor.to_sparse_coo()
        if tensor.ndim != 2:
            raise ValueError(f"Sparse embedding matrix must be 2D, got shape {tuple(tensor.shape)}.")
        return tensor.coalesce().float()
    if not sparse.issparse(embeddings):
        raise TypeError(f"Expected a sparse embedding matrix, got {type(embeddings).__name__}.")

    matrix = sparse.coo_matrix(embeddings)
    indices = torch.as_tensor(np.vstack((matrix.row, matrix.col)), dtype=torch.long, device=device)
    values = torch.as_tensor(matrix.data, dtype=torch.float32, device=device)
    return torch.sparse_coo_tensor(indices, values, size=matrix.shape, device=device).coalesce()


def _resize_torch_sparse_columns(matrix: torch.Tensor, columns: int) -> torch.Tensor:
    if columns < matrix.shape[1]:
        raise ValueError(f"Cannot shrink sparse matrix from {matrix.shape[1]} to {columns} columns.")
    matrix = _to_torch_sparse_coo_matrix(matrix)
    return torch.sparse_coo_tensor(
        matrix.indices(),
        matrix.values(),
        size=(int(matrix.shape[0]), columns),
        device=matrix.device,
    ).coalesce()


def _torch_sparse_l2_normalize(matrix: torch.Tensor) -> torch.Tensor:
    matrix = _to_torch_sparse_coo_matrix(matrix)
    row_indices = matrix.indices()[0]
    values = matrix.values()
    row_square_sums = torch.zeros(int(matrix.shape[0]), dtype=values.dtype, device=values.device)
    row_square_sums.scatter_add_(0, row_indices, values * values)
    row_norms = torch.sqrt(row_square_sums)
    row_norms = torch.where(row_norms == 0.0, torch.ones_like(row_norms), row_norms)
    normalized_values = values / row_norms.index_select(0, row_indices)
    return torch.sparse_coo_tensor(
        matrix.indices(),
        normalized_values,
        size=tuple(int(dimension) for dimension in matrix.shape),
        device=matrix.device,
    ).coalesce()


def _sparse_l2_normalize(matrix: sparse.csr_matrix) -> sparse.csr_matrix:
    norms = np.sqrt(matrix.multiply(matrix).sum(axis=1)).A1
    inv_norms = np.ones_like(norms)
    nonzero = norms > 0.0
    inv_norms[nonzero] = 1.0 / norms[nonzero]
    return (sparse.diags(inv_norms) @ matrix).tocsr()
