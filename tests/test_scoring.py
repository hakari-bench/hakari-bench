from __future__ import annotations

import numpy as np
import pytest

from hakari_bench.scoring import candidate_coverage_for_qrels, rank_candidate_subset_by_similarity


def test_rank_candidate_subset_scores_only_deduped_candidate_rows() -> None:
    calls: list[tuple[list[str], tuple[int, ...], tuple[int, ...]]] = []

    def rank_by_similarity(*, query_ids, corpus_ids, query_embeddings, corpus_embeddings, score_name):
        assert score_name == "dot"
        calls.append((list(corpus_ids), tuple(query_embeddings.shape), tuple(corpus_embeddings.shape)))
        return {query_ids[0]: list(reversed(corpus_ids))}

    rankings = rank_candidate_subset_by_similarity(
        query_ids=["q1", "q2"],
        corpus_ids=["d1", "d2", "d3"],
        query_embeddings=np.array([[1.0, 0.0], [0.0, 1.0]], dtype=np.float32),
        corpus_embeddings=np.array(
            [
                [1.0, 0.0],
                [0.0, 1.0],
                [-1.0, 0.0],
            ],
            dtype=np.float32,
        ),
        candidates={"q1": ["d3", "d1", "d3", "missing", "d2"], "q2": ["missing", "d2", "d1"]},
        score_name="dot",
        rerank_top_n=2,
        rank_by_similarity=rank_by_similarity,
    )

    assert rankings == {"q1": ["d1", "d3"], "q2": ["d1", "d2"]}
    assert calls == [
        (["d3", "d1"], (1, 2), (2, 2)),
        (["d2", "d1"], (1, 2), (2, 2)),
    ]


def test_rank_candidate_subset_rejects_non_positive_top_n() -> None:
    with pytest.raises(ValueError, match="rerank_top_n must be positive"):
        rank_candidate_subset_by_similarity(
            query_ids=["q1"],
            corpus_ids=["d1"],
            query_embeddings=np.array([[1.0]], dtype=np.float32),
            corpus_embeddings=np.array([[1.0]], dtype=np.float32),
            candidates={"q1": ["d1"]},
            score_name="dot",
            rerank_top_n=0,
            rank_by_similarity=lambda **kwargs: {"q1": ["d1"]},
        )


def test_candidate_coverage_for_qrels_counts_top_k_relevance_recall() -> None:
    coverage = candidate_coverage_for_qrels(
        qrels={
            "q1": {"d1", "d2"},
            "q2": {"d3"},
            "q3": set(),
        },
        candidates={
            "q1": ["d9", "d1", "d1", "d2"],
            "q2": ["d4", "d5"],
        },
        top_k=2,
    )

    assert coverage == {
        "top_k": 2,
        "query_count": 3,
        "query_with_relevance_count": 2,
        "covered_query_count": 1,
        "query_coverage": 0.5,
        "relevant_count": 3,
        "covered_relevant_count": 1,
        "relevant_coverage": 1 / 3,
    }
