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
    rerank_top_n: int,
    rank_by_similarity: SimilarityRanker,
) -> dict[str, list[str]]:
    if rerank_top_n <= 0:
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
            if len(candidate_ids) >= rerank_top_n:
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
