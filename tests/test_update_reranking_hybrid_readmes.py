from __future__ import annotations

from pathlib import Path

import pyarrow as pa
import pyarrow.parquet as pq

from scripts.update_reranking_hybrid_readmes import (
    parse_remote_readme,
    ranking_metrics,
    render_readme,
    source_links_for_dataset,
)


def _write_parquet(path: Path, rows: list[dict[str, object]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    pq.write_table(pa.Table.from_pylist(rows), path)


def test_ranking_metrics_compute_ndcg_and_recall_at_100() -> None:
    ndcg, recall = ranking_metrics(
        {"q1": ["d2", "d1"], "q2": ["d3"]},
        {"q1": {"d1"}, "q2": {"d3", "d4"}},
    )

    assert round(ndcg, 4) == 0.622
    assert recall == 0.75


def test_render_readme_orders_dense_quality_columns_and_omits_dataset_info(tmp_path: Path) -> None:
    dataset_dir = tmp_path / "NanoToy"
    _write_parquet(dataset_dir / "queries" / "toy.parquet", [{"_id": "q1", "text": "short query"}])
    _write_parquet(
        dataset_dir / "corpus" / "toy.parquet",
        [
            {"_id": "d1", "text": "positive document"},
            {"_id": "d2", "text": "negative document"},
        ],
    )
    _write_parquet(dataset_dir / "qrels" / "toy.parquet", [{"query-id": "q1", "corpus-id": "d1"}])
    _write_parquet(dataset_dir / "bm25" / "toy.parquet", [{"query-id": "q1", "corpus-ids": ["d2", "d1"]}])
    _write_parquet(
        dataset_dir / "harrier_oss_v1_270m" / "toy.parquet",
        [{"query-id": "q1", "corpus-ids": ["d1", "d2"]}],
    )
    _write_parquet(
        dataset_dir / "reranking_hybrid" / "toy.parquet",
        [{"query-id": "q1", "corpus-ids": ["d1", "d2"]}],
    )
    metadata = {
        "source_dataset": "hakari-bench/NanoToy",
        "splits": {
            "toy": {
                "bm25": {"resolved_tokenizer": "wordseg", "auto_detected_language": "ja"},
                "reranking_hybrid": {
                    "safeguard_positive_count": 0,
                    "limited_by_corpus_size_count": 0,
                },
            }
        },
    }
    remote_readme = """---
dataset_info:
- config_name: corpus
language:
- ja
tags:
- old-tag
---

# NanoToy

Remote overview.

## Source Links

- [hakari-bench/NanoToy](https://huggingface.co/datasets/hakari-bench/NanoToy)

## License

Remote license.
"""

    readme = render_readme(
        dataset_dir=dataset_dir,
        dataset_name="NanoToy",
        metadata=metadata,
        remote_readme=remote_readme,
    )

    frontmatter = readme.split("---", maxsplit=2)[1]
    assert "dataset_info" not in frontmatter
    assert "language:\n- ja" in frontmatter
    assert "old-tag" in frontmatter
    assert "Dense means `microsoft/harrier-oss-v1-270m`" in readme
    assert (
        "| Nano split | BM25 tokenizer | BM25 nDCG@10 | Dense nDCG@10 | Hybrid nDCG@10 | "
        "BM25 Recall@100 | Dense Recall@100 | Hybrid Recall@100 | Hybrid candidates | Safeguard positives |"
    ) in readme
    assert "| toy | wordseg@ja | 63.09 | 100.00 | 100.00 | 100.00 | 100.00 | 100.00 | 2 | 0 |" in readme
    assert "Remote overview." in readme
    assert "Remote license." in readme


def test_parse_remote_readme_extracts_sections_and_normalizes_hakari_link() -> None:
    parsed = parse_remote_readme(
        """---
language:
- en
---
# Nano

Run with [HAKARI-Bench](https://github.com/hotchpotch/hakari-bench).

## Source Links

- https://example.com/source

## License

Use upstream licenses.
"""
    )

    assert parsed.frontmatter["language"] == ["en"]
    assert parsed.overview == ""
    assert parsed.source_links == ["- https://example.com/source"]
    assert parsed.license_text == "Use upstream licenses."


def test_source_links_for_nanobeir_adds_original_source_when_remote_is_self_only() -> None:
    links = source_links_for_dataset(
        dataset_name="NanoBEIR-ja",
        source_dataset="hakari-bench/NanoBEIR-ja",
        remote_source_links=[
            "- Final dataset: [hakari-bench/NanoBEIR-ja](https://huggingface.co/datasets/hakari-bench/NanoBEIR-ja)"
        ],
    )

    assert links == [
        "- Original dataset: [LiquidAI/NanoBEIR-ja](https://huggingface.co/datasets/LiquidAI/NanoBEIR-ja)",
        "- Final dataset: [hakari-bench/NanoBEIR-ja](https://huggingface.co/datasets/hakari-bench/NanoBEIR-ja)",
    ]
