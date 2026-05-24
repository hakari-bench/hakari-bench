from __future__ import annotations

from collections.abc import Callable
from typing import Any

from hakari_bench.embedding_matrix import take_embedding_rows

SimilarityRanker = Callable[..., dict[str, list[str]]]


def rank_candidate_subset_by_similarity(
    *,
    query_ids: list[str],
    corpus_ids: list[str],
    query_embeddings: Any,
    corpus_embeddings: Any,
    candidates: dict[str, list[str]],
    score_name: str,
    rerank_top_n: int | None,
    rank_by_similarity: SimilarityRanker,
) -> dict[str, list[str]]:
    if rerank_top_n is not None and rerank_top_n <= 0:
        raise ValueError("rerank_top_n must be positive.")
    corpus_index_by_id = {corpus_id: index for index, corpus_id in enumerate(corpus_ids)}
    rankings: dict[str, list[str]] = {}
    for query_index, query_id in enumerate(query_ids):
        candidate_indices: list[int] = []
        candidate_ids: list[str] = []
        seen: set[str] = set()
        for candidate_id in candidates.get(query_id, []):
            if candidate_id in seen:
                continue
            corpus_index = corpus_index_by_id.get(candidate_id)
            if corpus_index is None:
                continue
            seen.add(candidate_id)
            candidate_indices.append(corpus_index)
            candidate_ids.append(candidate_id)
            if rerank_top_n is not None and len(candidate_ids) >= rerank_top_n:
                break
        if not candidate_ids:
            rankings[query_id] = []
            continue
        ranked = rank_by_similarity(
            query_ids=[query_id],
            corpus_ids=candidate_ids,
            query_embeddings=take_embedding_rows(query_embeddings, [query_index]),
            corpus_embeddings=take_embedding_rows(corpus_embeddings, candidate_indices),
            score_name=score_name,
        )
        rankings[query_id] = ranked[query_id]
    return rankings


def candidate_coverage_for_qrels(
    *,
    qrels: dict[str, set[str]],
    candidates: dict[str, list[str]],
    top_k: int,
) -> dict[str, int | float | None]:
    if top_k <= 0:
        raise ValueError("top_k must be positive.")
    query_with_relevance_count = 0
    covered_query_count = 0
    relevant_count = 0
    covered_relevant_count = 0
    for query_id, relevant_ids in qrels.items():
        if not relevant_ids:
            continue
        query_with_relevance_count += 1
        relevant_count += len(relevant_ids)
        candidate_ids = _deduped_top_k(candidates.get(query_id, []), top_k=top_k)
        covered_ids = relevant_ids.intersection(candidate_ids)
        if covered_ids:
            covered_query_count += 1
            covered_relevant_count += len(covered_ids)
    return {
        "top_k": int(top_k),
        "query_count": len(qrels),
        "query_with_relevance_count": query_with_relevance_count,
        "covered_query_count": covered_query_count,
        "query_coverage": (
            covered_query_count / query_with_relevance_count if query_with_relevance_count else None
        ),
        "relevant_count": relevant_count,
        "covered_relevant_count": covered_relevant_count,
        "relevant_coverage": covered_relevant_count / relevant_count if relevant_count else None,
    }


def _deduped_top_k(values: list[str], *, top_k: int) -> set[str]:
    seen: set[str] = set()
    for value in values:
        if value in seen:
            continue
        seen.add(value)
        if len(seen) >= top_k:
            break
    return seen
