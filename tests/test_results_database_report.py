from __future__ import annotations

import json
from pathlib import Path

from scripts import build_results_database_and_report as report


def test_nanojmteb_is_a_ranked_benchmark() -> None:
    assert "NanoJMTEB" in report.TARGET_BENCHMARKS
    assert report.benchmark_name("hotchpotch/NanoJMTEB", "NanoJMTEB") == "NanoJMTEB"


def test_nanorteb_is_a_ranked_benchmark() -> None:
    assert "NanoRTEB" in report.TARGET_BENCHMARKS
    assert report.benchmark_name("hotchpotch/NanoRTEB", "NanoRTEB") == "NanoRTEB"


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
    assert len(metric_rows) == 1
