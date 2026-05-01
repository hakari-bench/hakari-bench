from __future__ import annotations

import json
from pathlib import Path

import duckdb

from scripts import build_results_database_and_report as report


def test_nanojmteb_is_a_ranked_benchmark() -> None:
    assert "NanoJMTEB" in report.TARGET_BENCHMARKS
    assert report.benchmark_name("hotchpotch/NanoJMTEB", "NanoJMTEB") == "NanoJMTEB"


def test_nanorteb_is_a_ranked_benchmark() -> None:
    assert "NanoRTEB" in report.TARGET_BENCHMARKS
    assert report.benchmark_name("hotchpotch/NanoRTEB", "NanoRTEB") == "NanoRTEB"


def test_nanolongembed_is_a_ranked_benchmark() -> None:
    assert "NanoLongEmbed" in report.TARGET_BENCHMARKS
    assert report.benchmark_name("hotchpotch/NanoLongEmbed", "NanoLongEmbed") == "NanoLongEmbed"


def test_nanocoir_is_a_ranked_benchmark() -> None:
    assert "NanoCoIR" in report.TARGET_BENCHMARKS
    assert report.benchmark_name("hotchpotch/NanoCoIR", "NanoCoIR") == "NanoCoIR"


def test_load_results_reads_task_json_not_only_all_json(tmp_path: Path) -> None:
    model_dir = tmp_path / "model"
    task_path = model_dir / "hotchpotch__NanoJMTEB" / "NanoJaCWIR.json"
    task_path.parent.mkdir(parents=True)
    task_path.write_text(
        json.dumps(
            {
                "model": {
                    "name_or_path": "example/model",
                    "active_parameters": 3,
                    "total_parameters": 5,
                    "max_seq_length": 8192,
                    "dtype": "bf16",
                    "attn_implementation": "flash_attention_2",
                },
                "environment": {
                    "package_versions": {
                        "torch": "2.9.1",
                        "transformers": "4.57.6",
                        "sentence-transformers": "5.4.1",
                    }
                },
                "target": {
                    "dataset_name": "NanoJMTEB",
                    "dataset_id": "hotchpotch/NanoJMTEB",
                    "dataset_revision": {
                        "requested": None,
                        "resolved": "dataset-sha",
                        "source": "huggingface_hub",
                    },
                    "split_name": "NanoJaCWIR",
                    "task_name": "NanoJaCWIR",
                },
                "evaluation": {
                    "aggregate_metric": "ndcg@10",
                    "aggregate_metric_value": 0.42,
                    "evaluated_at_utc": "2026-04-29T00:00:00+00:00",
                },
                "metrics": {"NanoJaCWIR_ndcg@10": 0.42},
            }
        ),
        encoding="utf-8",
    )
    (model_dir / "all.json").write_text(
        json.dumps(
            {
                "model": {"name_or_path": "example/model"},
                "environment": {"package_versions": {}},
                "totals": {"split_count": 0},
                "splits": [],
            }
        ),
        encoding="utf-8",
    )

    rows, _, metric_rows = report.load_results(tmp_path)

    assert len(rows) == 1
    assert rows[0].benchmark == "NanoJMTEB"
    assert rows[0].score == 0.42
    assert rows[0].dataset_revision == "dataset-sha"
    assert rows[0].active_parameters == 3
    assert rows[0].total_parameters == 5
    assert len(metric_rows) == 1


def test_render_html_includes_total_parameters_column() -> None:
    html = report.render_html(data_json=json.dumps({"views": {}, "summary": {"skipped": []}}))

    assert "Total Params" in html


def test_load_results_adds_embedding_variant_rows(tmp_path: Path) -> None:
    model_dir = tmp_path / "model"
    task_path = model_dir / "hotchpotch__NanoJMTEB" / "NanoJaCWIR.json"
    task_path.parent.mkdir(parents=True)
    task_path.write_text(
        json.dumps(
            {
                "model": {"name_or_path": "example/model"},
                "environment": {"package_versions": {}},
                "target": {
                    "dataset_name": "NanoJMTEB",
                    "dataset_id": "hotchpotch/NanoJMTEB",
                    "split_name": "NanoJaCWIR",
                    "task_name": "NanoJaCWIR",
                },
                "evaluation": {"aggregate_metric": "ndcg@10", "aggregate_metric_value": 0.42},
                "embedding_evaluations": [
                    {
                        "name": "base",
                        "aggregate_metric": "ndcg@10",
                        "aggregate_metric_value": 0.42,
                        "embedding_dimensions": {"dim": 768},
                    },
                    {
                        "name": "truncate_dim_512_quantize_uint8_docs",
                        "aggregate_metric": "ndcg@10",
                        "aggregate_metric_value": 0.40,
                        "embedding_dimensions": {"dim": 512},
                        "embedding_metadata": {
                            "corpus": {
                                "quantization": {
                                    "precision": "uint8",
                                    "original_dim": 512,
                                    "stored_dim": 512,
                                }
                            }
                        },
                    },
                ],
                "metrics": {"NanoJaCWIR_ndcg@10": 0.42},
            }
        ),
        encoding="utf-8",
    )
    (model_dir / "all.json").write_text(
        json.dumps({"model": {"name_or_path": "example/model"}, "environment": {"package_versions": {}}, "totals": {}}),
        encoding="utf-8",
    )

    rows, _, _ = report.load_results(tmp_path)

    assert [(row.embedding_variant_name, row.score, row.embedding_dim, row.quantization) for row in rows] == [
        (None, 0.42, 768, None),
        ("truncate_dim_512_quantize_uint8_docs", 0.40, 512, "uint8"),
    ]


def test_write_duckdb_persists_dataset_revision(tmp_path: Path) -> None:
    row = report.TaskResult(
        model_dir="model",
        model_name="example/model",
        benchmark="NanoJMTEB",
        dataset_id="hotchpotch/NanoJMTEB",
        dataset_revision="dataset-sha",
        dataset_revision_requested="main",
        dataset_name="NanoJMTEB",
        split_name="NanoJaCWIR",
        task_name="NanoJaCWIR",
        task_key="NanoJMTEB::hotchpotch/NanoJMTEB::NanoJaCWIR",
        score=0.42,
        aggregate_metric="ndcg@10",
        result_path="result.json",
        active_parameters=3,
        total_parameters=5,
        max_seq_length=8192,
        dtype="bf16",
        attn_implementation="flash_attention_2",
        torch_version="2.9.1",
        transformers_version="4.57.6",
        sentence_transformers_version="5.4.1",
        started_at_utc=None,
        finished_at_utc=None,
        evaluated_at_utc=None,
        duration_seconds_including_dataset_load=None,
        wall_seconds=None,
    )
    standings, borda_rows = report.compute_standings([row])
    db_path = tmp_path / "results.duckdb"

    report.write_duckdb(
        db_path,
        runs=[
            {
                "model_dir": "model",
                "model_name": "example/model",
            }
        ],
        rows=[row],
        metric_rows=[
            {
                "model_dir": "model",
                "model_name": "example/model",
                "benchmark": "NanoJMTEB",
                "dataset_id": "hotchpotch/NanoJMTEB",
                "task_name": "NanoJaCWIR",
                "metric_name": "NanoJaCWIR_ndcg@10",
                "metric_value": 0.42,
                "result_path": "result.json",
            }
        ],
        standings=standings,
        borda_rows=borda_rows,
    )

    con = duckdb.connect(str(db_path))
    try:
        assert con.execute("SELECT dataset_revision, dataset_revision_requested FROM task_results").fetchone() == (
            "dataset-sha",
            "main",
        )
    finally:
        con.close()
