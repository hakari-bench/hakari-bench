from __future__ import annotations

import pytest

from hakari_bench.bm25 import BM25Config
import hakari_bench.nano_bm25_rebuild as nano_bm25_rebuild
from hakari_bench.nano_bm25_rebuild import rebuild_bm25_candidate_rows


def test_rebuild_bm25_candidate_rows_forces_positives_and_records_full_coverage() -> None:
    result = rebuild_bm25_candidate_rows(
        corpus_rows=[
            {"_id": "d-pos", "text": "unmatched positive"},
            {"_id": "d-neg", "text": "query token"},
        ],
        query_rows=[{"_id": "q1", "text": "query token"}],
        qrels_rows=[{"query-id": "q1", "corpus-id": "d-pos"}],
        split_name="NanoToy",
        bm25_config=BM25Config(tokenizer="whitespace", top_k=1),
    )

    assert result.candidate_rows == [{"query-id": "q1", "corpus-ids": ["d-pos"]}]
    assert result.qrels_rows is None
    assert result.metadata["bm25"]["forced_doc_count"] == 1
    assert result.metadata["bm25"]["candidate_coverage"]["query_coverage"] == 1.0
    assert result.metadata["bm25"]["candidate_coverage"]["relevant_coverage"] == 1.0


def test_rebuild_bm25_candidate_rows_rejects_qrels_above_candidate_cap() -> None:
    with pytest.raises(ValueError, match="above BM25 top_k=1"):
        rebuild_bm25_candidate_rows(
            corpus_rows=[
                {"_id": "d1", "text": "one"},
                {"_id": "d2", "text": "two"},
            ],
            query_rows=[{"_id": "q1", "text": "one"}],
            qrels_rows=[
                {"query-id": "q1", "corpus-id": "d1"},
                {"query-id": "q1", "corpus-id": "d2"},
            ],
            split_name="NanoOverCap",
            bm25_config=BM25Config(tokenizer="whitespace", top_k=1),
        )


def test_rebuild_bm25_candidate_rows_can_cap_qrels_to_candidate_top_k() -> None:
    result = rebuild_bm25_candidate_rows(
        corpus_rows=[
            {"_id": "d1", "text": "one"},
            {"_id": "d2", "text": "two"},
        ],
        query_rows=[{"_id": "q1", "text": "one"}],
        qrels_rows=[
            {"query-id": "q1", "corpus-id": "d1"},
            {"query-id": "q1", "corpus-id": "d2"},
        ],
        split_name="NanoCapped",
        bm25_config=BM25Config(tokenizer="whitespace", top_k=1),
        cap_qrels_to_top_k=True,
    )

    assert result.qrels_rows == [{"query-id": "q1", "corpus-id": "d1"}]
    assert result.metadata["qrels_selection"] == {
        "qrels_per_query_cap": 1,
        "removed_qrels_over_cap": 1,
        "qrels_cap_policy": "positive qrels are capped per query to the BM25 candidate top_k",
    }
    assert result.metadata["bm25"]["candidate_coverage"]["relevant_coverage"] == 1.0


def test_rebuild_bm25_candidate_rows_records_resolved_auto_tokenizer(monkeypatch: pytest.MonkeyPatch) -> None:
    def resolve_config(config: BM25Config, queries: dict[str, str]) -> BM25Config:
        assert config.tokenizer is None
        assert queries == {"q1": "query token"}
        return BM25Config(
            tokenizer="whitespace",
            top_k=1,
            auto_selected=True,
            auto_detected_language="en",
            auto_detection_language_counts={"en": 1},
            auto_detection_sample_size=1,
        )

    monkeypatch.setattr(nano_bm25_rebuild, "resolve_bm25_config_for_queries", resolve_config)

    result = rebuild_bm25_candidate_rows(
        corpus_rows=[
            {"_id": "d-pos", "text": "query token"},
            {"_id": "d-neg", "text": "other"},
        ],
        query_rows=[{"_id": "q1", "text": "query token"}],
        qrels_rows=[{"query-id": "q1", "corpus-id": "d-pos"}],
        split_name="NanoResolved",
        bm25_config=BM25Config(tokenizer=None, top_k=1),
    )

    config = result.metadata["bm25"]["config"]
    assert config["tokenizer"] == "whitespace"
    assert config["auto_selected"] is True
    assert config["auto_detected_language"] == "en"
