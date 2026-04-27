from __future__ import annotations

import pytest

from nano_ir_benchmark.bm25 import (
    BM25Config,
    evaluate_bm25_task,
    rank_bm25_candidates,
    rankings_to_candidate_rows,
    tokenize_texts,
)
from nano_ir_benchmark.evaluation import LoadedIrDataset


def test_rank_bm25_candidates_uses_bm25s_okapi() -> None:
    corpus = {
        "d1": "red apple fruit",
        "d2": "blue car engine",
        "d3": "apple pie recipe",
    }
    queries = {"q1": "apple"}

    rankings = rank_bm25_candidates(
        corpus=corpus,
        queries=queries,
        config=BM25Config(
            tokenizer="regex",
            top_k=2,
            show_progress=False,
        ),
    )

    assert set(rankings["q1"]) == {"d1", "d3"}


def test_tokenize_texts_supports_basic_tokenizers() -> None:
    assert tokenize_texts(["BM25-based retrieval works."], tokenizer="regex") == [
        ["bm25", "based", "retrieval", "works"]
    ]
    assert tokenize_texts(["BM25-based retrieval works."], tokenizer="whitespace") == [
        ["bm25-based", "retrieval", "works."]
    ]
    assert tokenize_texts(["BM25-based retrieval works."], tokenizer="english_regex") == [
        ["bm25", "based", "retrieval", "works"]
    ]


def test_tokenize_texts_supports_english_porter_stop() -> None:
    assert tokenize_texts(["The running runners run in the park."], tokenizer="english_porter_stop") == [
        ["run", "runner", "run", "park"]
    ]


def test_tokenize_texts_supports_pystemmer() -> None:
    assert tokenize_texts(["running runners"], tokenizer="stemmer", stemmer_algorithm="english") == [
        ["run", "runner"]
    ]


def test_rankings_to_candidate_rows_preserves_query_ids() -> None:
    rows = rankings_to_candidate_rows({"q1": ["d2", "d1"]})

    assert rows == [{"query-id": "q1", "corpus-ids": ["d2", "d1"]}]


def test_evaluate_bm25_task_returns_ir_metrics() -> None:
    dataset = LoadedIrDataset(
        queries={"q1": "cat fish", "q2": "dog bone"},
        corpus={"d1": "cat likes fish", "d2": "dog likes bone", "d3": "other"},
        qrels={"q1": {"d1"}, "q2": {"d2"}},
        candidates=None,
        evaluator_name="Toy",
    )

    result = evaluate_bm25_task(
        dataset=dataset,
        config=BM25Config(tokenizer="regex", top_k=3, show_progress=False),
    )

    assert result.metrics["Toy_bm25_bm25s_okapi_ndcg@10"] == pytest.approx(1.0)
    assert result.timing["score_and_topk_seconds"] >= 0.0
