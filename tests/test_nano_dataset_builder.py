from __future__ import annotations

import json
from pathlib import Path

import pyarrow as pa
import pyarrow.parquet as pq
import yaml

from hakari_bench.bm25 import BM25Config
from hakari_bench.nano_dataset_builder import (
    build_nano_dataset_from_local_source,
    build_nano_dataset_from_rows,
)


def _write_parquet(path: Path, rows: list[dict[str, object]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    pq.write_table(pa.Table.from_pylist(rows), path)


def _read_parquet(path: Path) -> list[dict[str, object]]:
    return pq.read_table(path).to_pylist()


def test_build_nano_dataset_from_rows_writes_flat_subset_layout_yaml_and_bm25(tmp_path: Path) -> None:
    output_dir = tmp_path / "NanoExample"
    config_dir = tmp_path / "config" / "datasets"

    result = build_nano_dataset_from_rows(
        output_dir=output_dir,
        dataset_name="NanoExample",
        dataset_id="hakari-bench/NanoExample",
        split_name="NanoToy",
        corpus_rows=[
            {"_id": "d-pos", "title": "Positive", "text": "unmatched relevant document"},
            {"_id": "d-neg", "title": "", "text": "query-term hard negative"},
            {"_id": "d-fill", "title": "Filler", "text": "generic filler"},
        ],
        query_rows=[
            {"_id": "q1", "query": "query-term"},
            {"_id": "q2", "query": "missing positive"},
        ],
        qrels_rows=[
            {"query-id": "q1", "corpus-id": "d-pos", "score": 1},
            {"query-id": "q1", "corpus-id": "d-neg", "score": 0},
            {"query-id": "q2", "corpus-id": "missing-doc", "score": 1},
        ],
        dataset_config_dir=config_dir,
        query_limit=10,
        doc_limit=10,
        bm25_config=BM25Config(tokenizer="whitespace", top_k=1),
    )

    assert result.split_name == "NanoToy"
    assert result.queries == 1
    assert result.corpus == 3
    assert result.qrels == 1
    assert result.source_non_positive_qrels == 1
    assert result.forced_doc_count == 1

    assert (output_dir / "corpus" / "NanoToy.parquet").exists()
    assert (output_dir / "queries" / "NanoToy.parquet").exists()
    assert (output_dir / "qrels" / "NanoToy.parquet").exists()
    assert (output_dir / "bm25" / "NanoToy.parquet").exists()

    assert _read_parquet(output_dir / "qrels" / "NanoToy.parquet") == [
        {"query-id": "q1", "corpus-id": "d-pos"}
    ]
    assert [row["_id"] for row in _read_parquet(output_dir / "corpus" / "NanoToy.parquet")] == [
        "d-pos",
        "d-neg",
        "d-fill",
    ]
    bm25_rows = _read_parquet(output_dir / "bm25" / "NanoToy.parquet")
    assert bm25_rows == [{"query-id": "q1", "corpus-ids": ["d-pos"]}]

    readme = (output_dir / "README.md").read_text(encoding="utf-8")
    assert "config_name: bm25" in readme
    assert "path: bm25/NanoToy.parquet" in readme
    assert "[HAKARI-Bench](https://github.com/hakari-bench/hakari-bench)" in readme
    assert "## Split Statistics" in readme
    assert "| NanoToy | 1 | 3 | 1 |" in readme
    assert "## Candidate Quality" in readme
    assert "| NanoToy | whitespace | 100.00 | n/a | n/a | 100.00% | n/a | n/a | n/a | n/a |" in readme
    assert "{{" not in readme
    assert "Template Fill Checklist" not in readme

    config = yaml.safe_load((config_dir / "nanoexample.yaml").read_text(encoding="utf-8"))
    assert config["name"] == "NanoExample"
    assert config["dataset_id"] == "hakari-bench/NanoExample"
    assert config["splits"] == ["NanoToy"]
    assert config["corpus_config"] == "corpus"
    assert config["queries_config"] == "queries"
    assert config["qrels_config"] == "qrels"
    assert config["candidate_config"] == "reranking_hybrid"


def test_build_nano_dataset_from_rows_can_preserve_duplicate_texts(tmp_path: Path) -> None:
    output_dir = tmp_path / "NanoExample"

    result = build_nano_dataset_from_rows(
        output_dir=output_dir,
        dataset_name="NanoExample",
        dataset_id="hakari-bench/NanoExample",
        split_name="NanoDuplicates",
        corpus_rows=[
            {"_id": "d1", "text": "parallel passage"},
            {"_id": "d2", "text": "parallel passage"},
        ],
        query_rows=[
            {"_id": "q1", "query": "parallel query"},
            {"_id": "q2", "query": "parallel query"},
        ],
        qrels_rows=[
            {"query-id": "q1", "corpus-id": "d1", "score": 1},
            {"query-id": "q2", "corpus-id": "d2", "score": 1},
        ],
        query_limit=10,
        doc_limit=10,
        bm25_config=BM25Config(tokenizer="whitespace", top_k=2),
        metadata={
            "source_subset_count": 2,
            "source_selected_query_count": 2,
            "source_corpus_order_policy": "round-robin test policy",
        },
        dedupe_query_texts=False,
        dedupe_doc_texts=False,
    )

    assert result.queries == 2
    assert result.corpus == 2
    assert result.qrels == 2
    assert [row["_id"] for row in _read_parquet(output_dir / "queries" / "NanoDuplicates.parquet")] == ["q1", "q2"]
    assert [row["_id"] for row in _read_parquet(output_dir / "corpus" / "NanoDuplicates.parquet")] == ["d1", "d2"]

    metadata = json.loads((output_dir / "metadata" / "NanoDuplicates.json").read_text(encoding="utf-8"))
    assert metadata["dedupe_query_texts"] is False
    assert metadata["dedupe_doc_texts"] is False
    assert metadata["source_subset_count"] == 2
    assert metadata["source_selected_query_count"] == 2
    assert metadata["source_corpus_order_policy"] == "round-robin test policy"


def test_build_nano_dataset_from_rows_records_bm25_candidate_coverage(tmp_path: Path) -> None:
    output_dir = tmp_path / "NanoCoverage"

    build_nano_dataset_from_rows(
        output_dir=output_dir,
        dataset_name="NanoCoverage",
        dataset_id="hakari-bench/NanoCoverage",
        split_name="NanoToy",
        corpus_rows=[
            {"_id": "d-pos", "text": "rare positive"},
            {"_id": "d-neg", "text": "query token"},
        ],
        query_rows=[{"_id": "q1", "query": "query token"}],
        qrels_rows=[{"query-id": "q1", "corpus-id": "d-pos", "score": 1}],
        query_limit=10,
        doc_limit=10,
        bm25_config=BM25Config(tokenizer="whitespace", top_k=1),
    )

    metadata = json.loads((output_dir / "metadata" / "NanoToy.json").read_text(encoding="utf-8"))
    assert metadata["bm25"]["candidate_coverage"] == {
        "top_k": 1,
        "query_count": 1,
        "query_with_relevance_count": 1,
        "covered_query_count": 1,
        "query_coverage": 1.0,
        "relevant_count": 1,
        "covered_relevant_count": 1,
        "relevant_coverage": 1.0,
    }

    readme = (output_dir / "README.md").read_text(encoding="utf-8")
    assert (
        "| Nano split | BM25 tokenizer | BM25 nDCG@10 | Dense nDCG@10 | Hybrid nDCG@10 | "
        "BM25 Recall@100 | Dense Recall@100 | Hybrid Recall@100 | Hybrid candidates | Safeguard positives |"
    ) in readme
    assert "| NanoToy | whitespace | 100.00 | n/a | n/a | 100.00% | n/a | n/a | n/a | n/a |" in readme


def test_build_nano_dataset_from_local_source_supports_nested_mteb_layout(tmp_path: Path) -> None:
    source_dir = tmp_path / "source"
    _write_parquet(
        source_dir / "SourceTask" / "corpus" / "test.parquet",
        [
            {"id": "d1", "title": "Needle", "text": "needle document"},
            {"id": "d2", "title": "Other", "text": "other document"},
        ],
    )
    _write_parquet(
        source_dir / "SourceTask" / "queries" / "test.parquet",
        [{"id": "q1", "question": "needle"}],
    )
    _write_parquet(
        source_dir / "SourceTask" / "qrels" / "test.parquet",
        [
            {"query_id": "q1", "doc_id": "d1", "score": 2},
            {"query_id": "q1", "doc_id": "d2", "score": -1},
        ],
    )

    result = build_nano_dataset_from_local_source(
        source_dir=source_dir,
        output_dir=tmp_path / "NanoLocal",
        dataset_name="NanoLocal",
        dataset_id="hakari-bench/NanoLocal",
        source_split_name="SourceTask",
        split_name="NanoSourceTask",
        query_limit=10,
        doc_limit=10,
        bm25_config=BM25Config(tokenizer="whitespace", top_k=2),
    )

    assert result.split_name == "NanoSourceTask"
    assert result.queries == 1
    assert result.corpus == 2
    assert result.qrels == 1
    assert result.source_non_positive_qrels == 1
