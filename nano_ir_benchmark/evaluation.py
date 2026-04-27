from __future__ import annotations

import time
from dataclasses import dataclass
from typing import Any

import numpy as np
import torch
from scipy import sparse

from nano_ir_benchmark.datasets import EvalTask
from nano_ir_benchmark.metrics import compute_ir_metrics


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


def load_ir_dataset(task: EvalTask, *, candidate_subset_name: str | None = None) -> LoadedIrDataset:
    from datasets import load_dataset

    corpus_dataset = load_dataset(task.dataset_id, task.dataset.corpus_config, split=task.split_name)
    queries_dataset = load_dataset(task.dataset_id, task.dataset.queries_config, split=task.split_name)
    qrels_dataset = load_dataset(task.dataset_id, task.dataset.qrels_config, split=task.split_name)

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

    candidates = _load_candidates(task, candidate_subset_name=candidate_subset_name)
    return LoadedIrDataset(
        queries=queries,
        corpus=corpus,
        qrels=qrels,
        candidates=candidates,
        evaluator_name=task.evaluator_name,
    )


def _load_candidates(task: EvalTask, *, candidate_subset_name: str | None) -> dict[str, list[str]] | None:
    if candidate_subset_name is None:
        return None
    try:
        from datasets import load_dataset

        rows = load_dataset(task.dataset_id, candidate_subset_name, split=task.split_name)
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
    truncate_dim: int | None,
) -> TaskEvaluation:
    query_ids = list(dataset.queries)
    corpus_ids = list(dataset.corpus)
    query_texts = [dataset.queries[query_id] for query_id in query_ids]
    corpus_texts = [dataset.corpus[corpus_id] for corpus_id in corpus_ids]

    query_start = time.perf_counter()
    query_embeddings = _encode(
        model,
        role="query",
        sentences=query_texts,
        batch_size=batch_size,
        show_progress=show_progress,
        prompt=query_prompt,
        prompt_name=query_prompt_name,
        truncate_dim=truncate_dim,
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
        truncate_dim=truncate_dim,
    )
    corpus_seconds = time.perf_counter() - corpus_start

    score_start = time.perf_counter()
    score_name = _score_name(getattr(model, "similarity_fn_name", "cosine"))
    rankings = _rank_by_similarity(
        query_ids=query_ids,
        corpus_ids=corpus_ids,
        query_embeddings=query_embeddings,
        corpus_embeddings=corpus_embeddings,
        score_name=score_name,
    )
    score_seconds = time.perf_counter() - score_start

    metric_start = time.perf_counter()
    metrics = compute_ir_metrics(
        rankings=rankings,
        qrels=dataset.qrels,
        evaluator_name=dataset.evaluator_name,
        score_name=score_name,
    )
    metric_seconds = time.perf_counter() - metric_start

    return TaskEvaluation(
        metrics=metrics,
        timing={
            "query_embedding_seconds": float(query_seconds),
            "corpus_embedding_seconds": float(corpus_seconds),
            "score_and_topk_seconds": float(score_seconds),
            "metric_compute_seconds": float(metric_seconds),
            "pure_compute_seconds": float(query_seconds + corpus_seconds + score_seconds + metric_seconds),
        },
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
    *,
    role: str,
    sentences: list[str],
    batch_size: int,
    show_progress: bool,
    prompt: str | None,
    prompt_name: str | None,
    truncate_dim: int | None,
) -> Any:
    encode_fn = getattr(model, "encode_query" if role == "query" else "encode_document", None)
    if encode_fn is None:
        encode_fn = model.encode

    kwargs: dict[str, Any] = {"batch_size": batch_size, "show_progress_bar": show_progress}
    if prompt is not None:
        kwargs["prompt"] = prompt
    elif prompt_name is not None:
        kwargs["prompt_name"] = prompt_name
    if truncate_dim is not None:
        kwargs["truncate_dim"] = truncate_dim

    try:
        return encode_fn(sentences, convert_to_numpy=True, **kwargs)
    except TypeError:
        return encode_fn(sentences, **kwargs)


def _predict_scores(model: Any, *, pairs: list[tuple[str, str]], batch_size: int, show_progress: bool) -> list[float]:
    if not pairs:
        return []
    raw_scores = model.predict(pairs, batch_size=batch_size, show_progress_bar=show_progress)
    if isinstance(raw_scores, torch.Tensor):
        raw_scores = raw_scores.detach().cpu().float().numpy()
    return [float(score) for score in np.asarray(raw_scores).reshape(-1).tolist()]


def _to_numpy_float32(embeddings: Any) -> np.ndarray:
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
    if sparse.issparse(query_embeddings) or sparse.issparse(corpus_embeddings):
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


def _rank_sparse(
    *,
    query_ids: list[str],
    corpus_ids: list[str],
    query_embeddings: Any,
    corpus_embeddings: Any,
    score_name: str,
) -> dict[str, list[str]]:
    query_matrix = sparse.csr_matrix(query_embeddings)
    corpus_matrix = sparse.csr_matrix(corpus_embeddings)
    if query_matrix.shape[1] < corpus_matrix.shape[1]:
        query_matrix.resize((query_matrix.shape[0], corpus_matrix.shape[1]))
    elif corpus_matrix.shape[1] < query_matrix.shape[1]:
        corpus_matrix.resize((corpus_matrix.shape[0], query_matrix.shape[1]))
    if score_name == "cosine":
        query_matrix = _sparse_l2_normalize(query_matrix)
        corpus_matrix = _sparse_l2_normalize(corpus_matrix)
    scores = (query_matrix @ corpus_matrix.T).toarray()
    return _scores_to_rankings(query_ids=query_ids, corpus_ids=corpus_ids, scores=scores)


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
    return sparse.diags(inv_norms) @ matrix
