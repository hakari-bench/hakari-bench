from __future__ import annotations

import inspect
import time
from dataclasses import dataclass, field
from typing import Any, Literal, cast

import numpy as np
import torch
from scipy import sparse

from nano_ir_benchmark.datasets import EvalTask
from nano_ir_benchmark.metrics import compute_ir_metrics

QuantizationPrecision = Literal["int8", "uint8", "binary", "ubinary"]


@dataclass(frozen=True)
class LoadedIrDataset:
    queries: dict[str, str]
    corpus: dict[str, str]
    qrels: dict[str, set[str]]
    candidates: dict[str, list[str]] | None
    evaluator_name: str


@dataclass(frozen=True)
class TaskEvaluation:
    metrics: dict[str, float]
    timing: dict[str, float]
    embedding_conversion: dict[str, Any] = field(default_factory=dict)
    embedding_evaluations: list[dict[str, Any]] = field(default_factory=list)


@dataclass(frozen=True)
class EmbeddingEncodeRequest:
    role: str
    sentences: list[str]
    batch_size: int
    show_progress: bool
    prompt: str | None
    prompt_name: str | None
    task: str | None
    truncate_dim: int | None


@dataclass(frozen=True)
class EmbeddingPostprocessPlan:
    steps: list[dict[str, Any]]

    @property
    def transform(self) -> dict[str, Any]:
        if not self.steps:
            return {"type": "identity", "algorithm": "none", "parameters": {}}
        return {"type": "pipeline", "steps": self.steps}


@dataclass(frozen=True)
class QuantizedEmbeddingMatrix:
    values: np.ndarray
    precision: str
    original_dim: int
    algorithm: str
    method: str
    side: str
    ranges_source: str | None = None
    ranges: np.ndarray | None = None

    @property
    def shape(self) -> tuple[int, ...]:
        return self.values.shape

    @property
    def dtype(self) -> np.dtype:
        return self.values.dtype


@dataclass(frozen=True)
class QuantizedSparseEmbeddingMatrix:
    matrix: sparse.csr_matrix
    precision: str
    original_dim: int
    algorithm: str
    method: str
    side: str
    score_representation: str
    ranges_source: str | None = None
    value_range: tuple[float, float] | None = None

    @property
    def shape(self) -> tuple[int, ...]:
        return self.matrix.shape

    @property
    def dtype(self) -> np.dtype:
        return self.matrix.dtype


def load_ir_dataset(
    task: EvalTask,
    *,
    candidate_subset_name: str | None = None,
    revision: str | None = None,
) -> LoadedIrDataset:
    from datasets import load_dataset

    corpus_dataset = load_dataset(task.dataset_id, task.dataset.corpus_config, split=task.split_name, revision=revision)
    queries_dataset = load_dataset(task.dataset_id, task.dataset.queries_config, split=task.split_name, revision=revision)
    qrels_dataset = load_dataset(task.dataset_id, task.dataset.qrels_config, split=task.split_name, revision=revision)

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

    candidates = _load_candidates(task, candidate_subset_name=candidate_subset_name, revision=revision)
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
) -> TaskEvaluation:
    query_ids = list(dataset.queries)
    corpus_ids = list(dataset.corpus)
    query_texts = [dataset.queries[query_id] for query_id in query_ids]
    corpus_texts = [dataset.corpus[corpus_id] for corpus_id in corpus_ids]

    query_start = time.perf_counter()
    query_embeddings = _encode(
        model,
        EmbeddingEncodeRequest(
            role="query",
            sentences=query_texts,
            batch_size=batch_size,
            show_progress=show_progress,
            prompt=query_prompt,
            prompt_name=query_prompt_name,
            task=query_task,
            truncate_dim=truncate_dim,
        ),
    )
    query_seconds = time.perf_counter() - query_start

    corpus_start = time.perf_counter()
    corpus_embeddings = _encode(
        model,
        EmbeddingEncodeRequest(
            role="document",
            sentences=corpus_texts,
            batch_size=batch_size,
            show_progress=show_progress,
            prompt=corpus_prompt,
            prompt_name=corpus_prompt_name,
            task=corpus_task,
            truncate_dim=truncate_dim,
        ),
    )
    corpus_seconds = time.perf_counter() - corpus_start

    base_postprocess = _build_base_embedding_postprocess_plan(
        truncate_sparse_query_max_dims=truncate_sparse_query_max_dims,
        truncate_sparse_docs_max_dims=truncate_sparse_docs_max_dims,
    )
    if base_postprocess.steps:
        query_embeddings, corpus_embeddings = _apply_embedding_pipeline_pair(
            query_embeddings=query_embeddings,
            corpus_embeddings=corpus_embeddings,
            steps=base_postprocess.steps,
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
            transform=base_postprocess.transform,
            embedding_dimensions=_embedding_dimensions(query_embeddings, corpus_embeddings),
            embedding_metadata=_embedding_metadata(query_embeddings, corpus_embeddings),
            scoring=base_scoring,
            timing=base_timing,
            aggregate_metric=aggregate_metric,
        )
    ]

    variant_score_seconds = 0.0
    variant_metric_seconds = 0.0
    for variant in embedding_variants or []:
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
        )
        variant_score_elapsed = float(variant_scoring["score_seconds"])
        variant_score_seconds += variant_score_elapsed

        variant_metric_elapsed = float(variant_scoring["metric_seconds"])
        variant_metric_seconds += variant_metric_elapsed
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
    )


def evaluate_reranker_task(
    *,
    model: Any,
    dataset: LoadedIrDataset,
    batch_size: int,
    show_progress: bool,
    rerank_top_n: int,
) -> TaskEvaluation:
    if dataset.candidates is None:
        raise ValueError("Reranker evaluation requires a candidate subset such as bm25.")

    score_start = time.perf_counter()
    rankings: dict[str, list[str]] = {}
    for query_id, query_text in dataset.queries.items():
        candidate_ids = [doc_id for doc_id in dataset.candidates.get(query_id, []) if doc_id in dataset.corpus]
        candidate_ids = candidate_ids[:rerank_top_n]
        pairs = [(query_text, dataset.corpus[doc_id]) for doc_id in candidate_ids]
        scores = _predict_scores(model, pairs=pairs, batch_size=batch_size, show_progress=show_progress)
        ranked = sorted(zip(candidate_ids, scores), key=lambda item: (-float(item[1]), item[0]))
        rankings[query_id] = [doc_id for doc_id, _score in ranked]
    score_seconds = time.perf_counter() - score_start

    metric_start = time.perf_counter()
    metrics = compute_ir_metrics(
        rankings=rankings,
        qrels=dataset.qrels,
        evaluator_name=dataset.evaluator_name,
        score_name="reranker",
    )
    metric_seconds = time.perf_counter() - metric_start
    return TaskEvaluation(
        metrics=metrics,
        timing={
            "query_embedding_seconds": 0.0,
            "corpus_embedding_seconds": 0.0,
            "score_and_topk_seconds": float(score_seconds),
            "metric_compute_seconds": float(metric_seconds),
            "pure_compute_seconds": float(score_seconds + metric_seconds),
        },
    )


def _encode(
    model: Any,
    request: EmbeddingEncodeRequest,
) -> Any:
    encode_fn = None
    if request.task is None:
        encode_fn = getattr(model, "encode_query" if request.role == "query" else "encode_document", None)
    if encode_fn is None:
        encode_fn = model.encode

    kwargs: dict[str, Any] = {"batch_size": request.batch_size, "show_progress_bar": request.show_progress}
    if request.prompt is not None:
        kwargs["prompt"] = request.prompt
    elif request.prompt_name is not None:
        kwargs["prompt_name"] = request.prompt_name
    if request.task is not None:
        kwargs["task"] = request.task
    if request.truncate_dim is not None:
        kwargs["truncate_dim"] = request.truncate_dim

    if _accepts_encode_parameter(encode_fn, "convert_to_sparse_tensor"):
        sparse_kwargs: dict[str, Any] = {
            "convert_to_tensor": True,
            "convert_to_sparse_tensor": True,
        }
        if _accepts_encode_parameter(encode_fn, "save_to_cpu"):
            sparse_kwargs["save_to_cpu"] = True
        return encode_fn(request.sentences, **sparse_kwargs, **kwargs)

    try:
        return encode_fn(request.sentences, convert_to_numpy=True, **kwargs)
    except TypeError:
        return encode_fn(request.sentences, **kwargs)


def _accepts_encode_parameter(encode_fn: Any, name: str) -> bool:
    try:
        return name in inspect.signature(encode_fn).parameters
    except (TypeError, ValueError):
        return False


def _embedding_conversion_payload(*, text_count: int, batch_size: int, seconds: float) -> dict[str, int | float | None]:
    seconds = float(seconds)
    return {
        "text_count": int(text_count),
        "batch_size": int(batch_size),
        "seconds": seconds,
        "texts_per_second": float(text_count / seconds) if seconds > 0.0 else None,
    }


def _predict_scores(model: Any, *, pairs: list[tuple[str, str]], batch_size: int, show_progress: bool) -> list[float]:
    if not pairs:
        return []
    raw_scores = model.predict(pairs, batch_size=batch_size, show_progress_bar=show_progress)
    if isinstance(raw_scores, torch.Tensor):
        raw_scores = raw_scores.detach().cpu().float().numpy()
    return [float(score) for score in np.asarray(raw_scores).reshape(-1).tolist()]


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
) -> dict[str, Any]:
    distance_evaluations: list[dict[str, Any]] = []
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
        )
        metric_elapsed = time.perf_counter() - metric_start
        metric_seconds += metric_elapsed

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
    return {
        "distance_evaluations": distance_evaluations,
        "metrics": best["metrics"],
        "aggregate_metric_value": best["aggregate_metric_value"],
        "best_score": best["aggregate_metric_value"],
        "best_distance": best["distance"],
        "best_score_name": best["score_name"],
        "score_seconds": score_seconds,
        "metric_seconds": metric_seconds,
    }


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


def _build_base_embedding_postprocess_plan(
    *,
    truncate_sparse_query_max_dims: int | None,
    truncate_sparse_docs_max_dims: int | None,
) -> EmbeddingPostprocessPlan:
    steps: list[dict[str, Any]] = []
    if truncate_sparse_query_max_dims is not None:
        steps.append(_truncate_sparse_max_dims_step(max_dims=truncate_sparse_query_max_dims, target="query"))
    if truncate_sparse_docs_max_dims is not None:
        steps.append(_truncate_sparse_max_dims_step(max_dims=truncate_sparse_docs_max_dims, target="corpus"))
    return EmbeddingPostprocessPlan(steps=steps)


def _truncate_sparse_max_dims_step(*, max_dims: int, target: str) -> dict[str, Any]:
    return {
        "type": "truncate_sparse_max_dims",
        "algorithm": "top_abs_values_per_row",
        "parameters": {"max_dims": int(max_dims), "target": target},
    }


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
        precision = str(step.get("parameters", {}).get("precision"))
        target = str(step.get("parameters", {}).get("target") or "corpus")
        return _quantize_embedding_pair(
            query_embeddings=query_embeddings,
            corpus_embeddings=corpus_embeddings,
            precision=precision,
            target=target,
            algorithm=str(step.get("algorithm") or "sentence_transformers_embedding_quantization"),
        )
    raise ValueError(f"Unsupported embedding variant pipeline step: {step_type}")


def _truncate_embeddings(embeddings: Any, dim: int) -> Any:
    if dim <= 0:
        raise ValueError("Truncate dimension must be positive.")
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


def _limit_sparse_active_dims(embeddings: Any, *, max_active_dims: int) -> sparse.csr_matrix:
    if max_active_dims <= 0:
        raise ValueError("Sparse truncation max dims must be positive.")
    if not _is_sparse_embedding(embeddings):
        raise ValueError("Sparse truncation variants are only supported for sparse embeddings.")

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


def _quantize_embedding_pair(
    *,
    query_embeddings: Any,
    corpus_embeddings: Any,
    precision: str,
    target: str = "corpus",
    algorithm: str,
) -> tuple[Any, Any]:
    if _is_sparse_embedding(query_embeddings) or _is_sparse_embedding(corpus_embeddings):
        return _quantize_sparse_embedding_pair(
            query_embeddings=query_embeddings,
            corpus_embeddings=corpus_embeddings,
            precision=precision,
            target=target,
            algorithm=algorithm,
        )
    if precision not in {"int8", "uint8", "binary", "ubinary"}:
        raise ValueError(f"Unsupported quantization precision: {precision}")
    precision_literal = cast(QuantizationPrecision, precision)
    target = _normalize_quantization_target(target)
    method = "corpus_only" if target == "corpus" else "query_and_corpus"

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
    if precision_literal in {"int8", "uint8"}:
        if corpus_matrix.shape[0] == 0:
            raise ValueError("Cannot calibrate quantized embeddings from an empty corpus.")
        # Strict evaluation should not adapt quantization buckets to the eval
        # queries. Use corpus-only ranges, then clip query outliers to prevent
        # numpy int8/uint8 casts from wrapping values outside those ranges.
        ranges = np.vstack((np.min(corpus_matrix, axis=0), np.max(corpus_matrix, axis=0)))
        ranges_source = "corpus"

    original_dim = int(query_matrix.shape[1])
    if precision_literal in {"binary", "ubinary"}:
        corpus_values = _pack_binary_embeddings(corpus_matrix, precision=precision_literal)
        if target == "query_and_corpus":
            query_values = _pack_binary_embeddings(query_matrix, precision=precision_literal)
        else:
            query_values = None
    else:
        if ranges is None:
            raise ValueError(f"Missing scalar quantization ranges for precision: {precision_literal}")
        corpus_values = _quantize_scalar_embeddings(corpus_matrix, precision=precision_literal, ranges=ranges)
        if target == "query_and_corpus":
            query_values = _quantize_scalar_embeddings(query_matrix, precision=precision_literal, ranges=ranges)
        else:
            query_values = None
    corpus_quantized = QuantizedEmbeddingMatrix(
        values=corpus_values,
        precision=precision_literal,
        original_dim=original_dim,
        algorithm=algorithm,
        method=method,
        side="corpus",
        ranges_source=ranges_source,
        ranges=ranges.astype(np.float32, copy=True) if ranges is not None else None,
    )
    if query_values is None:
        return query_embeddings, corpus_quantized
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
        ),
        corpus_quantized,
    )


def _quantize_sparse_embedding_pair(
    *,
    query_embeddings: Any,
    corpus_embeddings: Any,
    precision: str,
    target: str,
    algorithm: str,
) -> tuple[Any, Any]:
    if precision not in {"int8", "uint8", "binary", "ubinary"}:
        raise ValueError(f"Unsupported quantization precision: {precision}")
    precision_literal = cast(QuantizationPrecision, precision)
    target = _normalize_quantization_target(target)
    method = "corpus_only" if target == "corpus" else "query_and_corpus"

    query_matrix = _to_scipy_csr_matrix(query_embeddings)
    corpus_matrix = _to_scipy_csr_matrix(corpus_embeddings)
    if query_matrix.shape[1] != corpus_matrix.shape[1]:
        raise ValueError(
            f"Cannot quantize query dimension {query_matrix.shape[1]} with corpus dimension {corpus_matrix.shape[1]}."
        )

    value_range = None
    if precision_literal in {"int8", "uint8"}:
        if corpus_matrix.nnz == 0:
            raise ValueError("Cannot calibrate quantized sparse embeddings from a corpus with no non-zero values.")
        value_range = (float(np.min(corpus_matrix.data)), float(np.max(corpus_matrix.data)))

    corpus_quantized = _quantize_sparse_matrix(
        corpus_matrix,
        precision=precision_literal,
        algorithm=algorithm,
        method=method,
        side="corpus",
        value_range=value_range,
    )
    if target == "corpus":
        return query_embeddings, corpus_quantized
    return (
        _quantize_sparse_matrix(
            query_matrix,
            precision=precision_literal,
            algorithm=algorithm,
            method=method,
            side="query",
            value_range=value_range,
        ),
        corpus_quantized,
    )


def _quantize_sparse_matrix(
    matrix: sparse.csr_matrix,
    *,
    precision: QuantizationPrecision,
    algorithm: str,
    method: str,
    side: str,
    value_range: tuple[float, float] | None,
) -> QuantizedSparseEmbeddingMatrix:
    matrix = matrix.copy().astype(np.float32)
    ranges_source = None
    score_representation = "sparse_float32"
    if precision in {"int8", "uint8"}:
        if value_range is None:
            raise ValueError(f"Missing sparse quantization value range for precision: {precision}")
        starts = value_range[0]
        step = (value_range[1] - value_range[0]) / 255
        if step == 0:
            step = 1.0
        buckets = (matrix.data - starts) / step
        if precision == "uint8":
            matrix.data = np.rint(np.clip(buckets, 0, 255)).astype(np.uint8)
        else:
            matrix.data = np.rint(np.clip(buckets - 128, -128, 127)).astype(np.int8)
        ranges_source = "corpus"
        score_representation = "dequantized_sparse_float32"
    elif precision in {"binary", "ubinary"}:
        matrix.data = np.ones_like(matrix.data, dtype=np.uint8 if precision == "ubinary" else np.int8)
        score_representation = "sparse_nonzero_indicator_float32"

    return QuantizedSparseEmbeddingMatrix(
        matrix=matrix,
        precision=precision,
        original_dim=int(matrix.shape[1]),
        algorithm=algorithm,
        method=method,
        side=side,
        score_representation=score_representation,
        ranges_source=ranges_source,
        value_range=value_range,
    )


def _normalize_quantization_target(target: str) -> str:
    normalized = target.strip().lower().replace("-", "_")
    if normalized in {"corpus", "document", "documents", "doc", "docs", "corpus_only"}:
        return "corpus"
    if normalized in {"both", "query_and_corpus", "query_corpus", "query_and_document", "query_and_docs"}:
        return "query_and_corpus"
    raise ValueError(f"Unsupported quantization target: {target}")


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
    if precision == "uint8":
        return np.rint(np.clip(buckets, 0, 255)).astype(np.uint8)
    if precision == "int8":
        return np.rint(np.clip(buckets - 128, -128, 127)).astype(np.int8)
    raise ValueError(f"Unsupported scalar quantization precision: {precision}")


def _pack_binary_embeddings(embeddings: np.ndarray, *, precision: QuantizationPrecision) -> np.ndarray:
    packed = np.packbits(embeddings > 0, axis=1)
    if precision == "ubinary":
        return packed
    if precision == "binary":
        return (packed.astype(np.int16) - 128).astype(np.int8)
    raise ValueError(f"Unsupported binary quantization precision: {precision}")


def _dequantize_scalar_embeddings(embeddings: QuantizedEmbeddingMatrix) -> np.ndarray:
    if embeddings.precision not in {"int8", "uint8"}:
        raise ValueError(f"Cannot scalar-dequantize precision: {embeddings.precision}")
    if embeddings.ranges is None:
        raise ValueError(f"Quantized {embeddings.precision} embeddings are missing dequantization ranges.")
    starts = embeddings.ranges[0, :]
    steps = (embeddings.ranges[1, :] - embeddings.ranges[0, :]) / 255
    steps = np.where(steps == 0, 1, steps)
    buckets = embeddings.values.astype(np.float32)
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
    if representation_type == "sparse":
        return "sparse_vector"
    if representation_type == "late_interaction":
        return "multi_vector"
    return "single_vector"


def _embedding_side_metadata(embeddings: Any) -> dict[str, Any]:
    metadata: dict[str, Any] = {"shape": _shape_list(embeddings)}
    if _is_quantized_embedding_matrix(embeddings) or _is_quantized_sparse_embedding_matrix(embeddings):
        metadata["value_dtype"] = str(embeddings.dtype)
        metadata["quantization"] = _quantization_metadata(embeddings)
    if _is_sparse_embedding(embeddings):
        metadata.update(_sparse_embedding_stats(embeddings))
    return metadata


def _quantization_metadata(embeddings: QuantizedEmbeddingMatrix | QuantizedSparseEmbeddingMatrix) -> dict[str, Any]:
    if isinstance(embeddings, QuantizedSparseEmbeddingMatrix):
        score_representation = embeddings.score_representation
    else:
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
    if isinstance(embeddings, QuantizedSparseEmbeddingMatrix) and embeddings.value_range is not None:
        quantization["value_range"] = list(embeddings.value_range)
    return quantization


def _sparse_embedding_stats(embeddings: Any) -> dict[str, Any]:
    shape = _shape_list(embeddings)
    row_count = int(shape[0]) if shape else 0
    total_size = int(np.prod(shape)) if shape else 0
    if _is_quantized_sparse_embedding_matrix(embeddings):
        matrix = embeddings.matrix
        row_nnz = np.diff(matrix.indptr)
        nnz_total = int(matrix.nnz)
    elif sparse.issparse(embeddings):
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
    return sparse.issparse(embeddings) or _is_torch_sparse_embedding(embeddings) or _is_quantized_sparse_embedding_matrix(embeddings)


def _is_torch_sparse_embedding(embeddings: Any) -> bool:
    return isinstance(embeddings, torch.Tensor) and (
        embeddings.is_sparse or bool(getattr(embeddings, "is_sparse_csr", False))
    )


def _to_scipy_csr_matrix(embeddings: Any) -> sparse.csr_matrix:
    if _is_quantized_sparse_embedding_matrix(embeddings):
        return _dequantize_sparse_matrix(embeddings)
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


def _dequantize_sparse_matrix(embeddings: QuantizedSparseEmbeddingMatrix) -> sparse.csr_matrix:
    matrix = embeddings.matrix.copy()
    if embeddings.precision in {"binary", "ubinary"}:
        matrix.data = np.ones_like(matrix.data, dtype=np.float32)
        return matrix
    if embeddings.precision not in {"int8", "uint8"}:
        matrix.data = matrix.data.astype(np.float32, copy=False)
        return matrix
    if embeddings.value_range is None:
        raise ValueError(f"Quantized sparse {embeddings.precision} embeddings are missing value ranges.")
    starts = embeddings.value_range[0]
    step = (embeddings.value_range[1] - embeddings.value_range[0]) / 255
    if step == 0:
        step = 1.0
    buckets = matrix.data.astype(np.float32)
    if embeddings.precision == "int8":
        buckets = buckets + 128
    matrix.data = buckets * step + starts
    return matrix


def _is_quantized_embedding_matrix(embeddings: Any) -> bool:
    return isinstance(embeddings, QuantizedEmbeddingMatrix)


def _is_quantized_sparse_embedding_matrix(embeddings: Any) -> bool:
    return isinstance(embeddings, QuantizedSparseEmbeddingMatrix)


def _is_scalar_quantized(embeddings: Any) -> bool:
    return _is_quantized_embedding_matrix(embeddings) and embeddings.precision in {"int8", "uint8"}


def _is_packed_binary_quantized(embeddings: Any) -> bool:
    return _is_quantized_embedding_matrix(embeddings) and embeddings.precision in {"binary", "ubinary"}


def _quantized_score_representation(embeddings: QuantizedEmbeddingMatrix) -> str:
    if embeddings.precision in {"int8", "uint8"}:
        return "dequantized_float32"
    if embeddings.precision in {"binary", "ubinary"}:
        return "unpacked_sign_float32"
    return "stored_values_float32"


def _is_late_interaction_shape(shape: list[int]) -> bool:
    return len(shape) >= 3


def _embedding_dimension(embeddings: Any) -> int | None:
    if _is_quantized_embedding_matrix(embeddings):
        return int(embeddings.original_dim)
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
        return embeddings.values.astype(np.float32, copy=False)
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

    if _is_sparse_embedding(query_embeddings) or _is_sparse_embedding(corpus_embeddings):
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
    packed = embeddings.values
    if embeddings.precision == "binary":
        packed = (packed.astype(np.int16) + 128).astype(np.uint8)
    else:
        packed = packed.astype(np.uint8, copy=False)
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


def _l2_normalize(matrix: np.ndarray) -> np.ndarray:
    norms = np.linalg.norm(matrix, axis=1, keepdims=True)
    norms[norms == 0.0] = 1.0
    return matrix / norms


def _sparse_l2_normalize(matrix: sparse.csr_matrix) -> sparse.csr_matrix:
    norms = np.sqrt(matrix.multiply(matrix).sum(axis=1)).A1
    inv_norms = np.ones_like(norms)
    nonzero = norms > 0.0
    inv_norms[nonzero] = 1.0 / norms[nonzero]
    return (sparse.diags(inv_norms) @ matrix).tocsr()
