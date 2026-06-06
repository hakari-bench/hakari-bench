from __future__ import annotations

import math

import pytest

from hakari_bench.metrics import compute_ir_metrics


def test_compute_ir_metrics_multiple_cutoffs_and_families() -> None:
    rankings = {
        "q1": ["d1", "d2", "d3", "d4"],
        "q2": ["d5", "d6", "d7", "d8"],
    }
    qrels = {
        "q1": {"d2", "d4"},
        "q2": {"d5"},
    }

    metrics = compute_ir_metrics(
        rankings=rankings,
        qrels=qrels,
        evaluator_name="Toy",
        score_name="cosine",
        metric_names=("acc@1", "acc@3", "precision@2", "recall@4", "mrr@3", "ndcg@3", "map@4"),
    )

    assert metrics["Toy_cosine_acc@1"] == pytest.approx(0.5)
    assert metrics["Toy_cosine_acc@3"] == pytest.approx(1.0)
    assert metrics["Toy_cosine_precision@2"] == pytest.approx((0.5 + 0.5) / 2)
    assert metrics["Toy_cosine_recall@4"] == pytest.approx(1.0)
    assert metrics["Toy_cosine_mrr@3"] == pytest.approx((0.5 + 1.0) / 2)
    q1_ndcg = (1 / math.log2(3)) / (1 + 1 / math.log2(3))
    assert metrics["Toy_cosine_ndcg@3"] == pytest.approx((q1_ndcg + 1.0) / 2)
    q1_map = ((1 / 2) + (2 / 4)) / 2
    assert metrics["Toy_cosine_map@4"] == pytest.approx((q1_map + 1.0) / 2)


def test_compute_ir_metrics_preserves_duplicate_ranking_semantics() -> None:
    rankings = {"q1": ["d1", "d1", "d2"]}
    qrels = {"q1": {"d1", "d2"}}

    metrics = compute_ir_metrics(
        rankings=rankings,
        qrels=qrels,
        evaluator_name="Toy",
        score_name="cosine",
        metric_names=("precision@3", "recall@3", "ndcg@3", "map@3"),
    )

    assert metrics["Toy_cosine_precision@3"] == pytest.approx(2 / 3)
    assert metrics["Toy_cosine_recall@3"] == pytest.approx(1.0)
    assert metrics["Toy_cosine_ndcg@3"] == pytest.approx((1 + 1 / math.log2(3) + 1 / math.log2(4)) / (1 + 1 / math.log2(3)))
    assert metrics["Toy_cosine_map@3"] == pytest.approx((1 + 2 / 2 + 3 / 3) / 2)
