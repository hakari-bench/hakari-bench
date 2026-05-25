from __future__ import annotations

import sys

from scripts import build_all_reranking_hybrid_nano_datasets as build_all
from scripts import build_reranking_hybrid_nano_dataset as build_one


def test_single_dataset_builder_defaults_to_top500_sources_and_rrf100(monkeypatch) -> None:
    monkeypatch.setattr(sys, "argv", ["build_reranking_hybrid_nano_dataset.py"])

    args = build_one.parse_args()

    assert args.bm25_top_k == 500
    assert args.dense_top_k == 500
    assert args.hybrid_top_k == 100
    assert args.rrf_k == 100


def test_all_dataset_builder_defaults_to_top500_sources_and_rrf100(monkeypatch) -> None:
    monkeypatch.setattr(sys, "argv", ["build_all_reranking_hybrid_nano_datasets.py"])

    args = build_all.parse_args()

    assert args.bm25_top_k == 500
    assert args.dense_top_k == 500
    assert args.hybrid_top_k == 100
    assert args.rrf_k == 100


def test_rrf_hybrid_keeps_top100_when_positive_is_present() -> None:
    query_ids = ["q1"]
    corpus_ids = [f"d{i:03d}" for i in range(150)]
    bm25 = {"q1": corpus_ids[:100]}
    dense = {"q1": corpus_ids[:100]}

    rankings, metadata = build_one.rrf_hybrid_rankings(
        query_ids=query_ids,
        corpus_ids=corpus_ids,
        qrels={"q1": {"d050"}},
        bm25_rankings=bm25,
        dense_rankings=dense,
        top_k=100,
        rrf_k=100,
        seed=1,
        split="toy",
    )

    assert len(rankings["q1"]) == 100
    assert "d050" in rankings["q1"]
    assert metadata["candidate_count_max"] == 100
    assert metadata["safeguard_positive_count"] == 0
    assert metadata["construction_policy"] == "RRF top-100 plus optional safeguard positive at rank 101"


def test_rrf_hybrid_appends_positive_at_rank101_only_when_missing() -> None:
    query_ids = ["q1"]
    corpus_ids = [f"d{i:03d}" for i in range(150)]
    bm25 = {"q1": corpus_ids[:100]}
    dense = {"q1": corpus_ids[:100]}

    rankings, metadata = build_one.rrf_hybrid_rankings(
        query_ids=query_ids,
        corpus_ids=corpus_ids,
        qrels={"q1": {"d120"}},
        bm25_rankings=bm25,
        dense_rankings=dense,
        top_k=100,
        rrf_k=100,
        seed=1,
        split="toy",
    )

    assert len(rankings["q1"]) == 101
    assert rankings["q1"][:100] == corpus_ids[:100]
    assert rankings["q1"][100] == "d120"
    assert metadata["candidate_count_max"] == 101
    assert metadata["safeguard_positive_count"] == 1
    assert metadata["additions"] == [
        {
            "query_id": "q1",
            "reason": "missing_positive_in_rrf_top_100",
            "corpus_id": "d120",
            "rank": 101,
        }
    ]


def test_rrf_hybrid_small_corpus_covers_positive_without_safeguard() -> None:
    query_ids = ["q1"]
    corpus_ids = [f"d{i:03d}" for i in range(50)]
    bm25 = {"q1": corpus_ids}
    dense = {"q1": list(reversed(corpus_ids))}

    rankings, metadata = build_one.rrf_hybrid_rankings(
        query_ids=query_ids,
        corpus_ids=corpus_ids,
        qrels={"q1": {"d049"}},
        bm25_rankings=bm25,
        dense_rankings=dense,
        top_k=100,
        rrf_k=100,
        seed=1,
        split="toy",
    )

    assert len(rankings["q1"]) == 50
    assert "d049" in rankings["q1"]
    assert metadata["safeguard_positive_count"] == 0
    assert metadata["limited_by_corpus_size_count"] == 1


def test_audit_dataset_forces_redownload_for_written_local_files(monkeypatch, tmp_path) -> None:
    calls = []

    def fake_load_dataset(dataset_id, config_name, *, split, download_mode=None):
        assert dataset_id == str(tmp_path)
        assert split == "toy"
        calls.append((config_name, download_mode))
        if config_name == "corpus":
            return [{"_id": "d1"}, {"_id": "d2"}]
        if config_name == "queries":
            return [{"_id": "q1"}]
        if config_name == "qrels":
            return [{"query-id": "q1", "corpus-id": "d1"}]
        if config_name == build_one.HYBRID_CONFIG_NAME:
            return [{"query-id": "q1", "corpus-ids": ["d2", "d1"]}]
        raise AssertionError(config_name)

    monkeypatch.setattr(build_one, "load_dataset", fake_load_dataset)

    build_one.audit_dataset(
        output_dir=tmp_path,
        splits=["toy"],
        metadata={
            "splits": {
                "toy": {
                    build_one.HYBRID_CONFIG_NAME: {
                        "query_coverage": 1.0,
                    }
                }
            }
        },
    )

    assert calls == [
        ("corpus", build_one.DownloadMode.FORCE_REDOWNLOAD),
        ("queries", build_one.DownloadMode.FORCE_REDOWNLOAD),
        ("qrels", build_one.DownloadMode.FORCE_REDOWNLOAD),
        (build_one.HYBRID_CONFIG_NAME, build_one.DownloadMode.FORCE_REDOWNLOAD),
    ]
