from __future__ import annotations

import json
import lzma
from pathlib import Path

import duckdb

from scripts import generate_results_pr_template as template


def test_generate_pr_template_summarizes_overall_scores_from_xz_results(tmp_path: Path) -> None:
    result_dir = tmp_path / "Example__model"
    _write_result(
        result_dir / "hakari-bench__NanoBEIR-en" / "arguana.json.xz",
        dataset_name="NanoBEIR-en",
        dataset_id="hakari-bench/NanoBEIR-en",
        task_name="arguana",
        score=0.6,
    )
    _write_result(
        result_dir / "hakari-bench__NanoBEIR-ja" / "arguana.json.xz",
        dataset_name="NanoBEIR-ja",
        dataset_id="hakari-bench/NanoBEIR-ja",
        task_name="arguana",
        score=0.8,
    )
    _write_result(
        result_dir / "hakari-bench__NanoRTEB" / "task-a.json.xz",
        dataset_name="NanoRTEB",
        dataset_id="hakari-bench/NanoRTEB",
        task_name="task-a",
        score=0.4,
    )
    _write_result(
        result_dir / "hakari-bench__NanoCoIR" / "task-b.json.xz",
        dataset_name="NanoCoIR",
        dataset_id="hakari-bench/NanoCoIR",
        task_name="task-b",
        score=0.5,
    )

    rendered = template.generate_pr_template(result_dir, repo_path="PROJECT_ROOT/hakari-results/Example__model")

    assert "| Overall nDCG@10 | 0.5333 |" in rendered
    assert "| MNanoBEIR | 0.7000 | 1 | 2 |" in rendered
    assert "| NanoRTEB | 0.4000 | 1 | 1 |" in rendered
    assert "| NanoCoIR | 0.5000 | 1 | 1 |" in rendered
    assert "| Result files | 4 total, 4 `.json.xz` |" in rendered
    assert "| Target path | `PROJECT_ROOT/hakari-results/Example__model` |" in rendered
    assert "| torch | `2.9.0` |" in rendered


def test_result_json_paths_accepts_compressed_and_plain_json(tmp_path: Path) -> None:
    (tmp_path / "a.json").write_text("{}", encoding="utf-8")
    (tmp_path / "b.json.gz").write_bytes(b"")
    (tmp_path / "c.json.xz").write_bytes(b"")
    (tmp_path / "d.txt").write_text("", encoding="utf-8")

    assert [path.name for path in template.result_json_paths(tmp_path)] == [
        "a.json",
        "b.json.gz",
        "c.json.xz",
    ]


def test_generate_pr_template_adds_duckdb_comparison_table(tmp_path: Path) -> None:
    result_dir = tmp_path / "Example__model"
    _write_result(
        result_dir / "hakari-bench__NanoBEIR-en" / "arguana.json.xz",
        dataset_name="NanoBEIR-en",
        dataset_id="hakari-bench/NanoBEIR-en",
        task_name="arguana",
        score=0.6,
    )
    _write_result(
        result_dir / "hakari-bench__NanoBEIR-ja" / "arguana.json.xz",
        dataset_name="NanoBEIR-ja",
        dataset_id="hakari-bench/NanoBEIR-ja",
        task_name="arguana",
        score=0.8,
    )
    _write_result(
        result_dir / "hakari-bench__NanoRTEB" / "task-a.json.xz",
        dataset_name="NanoRTEB",
        dataset_id="hakari-bench/NanoRTEB",
        task_name="task-a",
        score=0.4,
    )

    duckdb_path = tmp_path / "results.duckdb"
    con = duckdb.connect(str(duckdb_path))
    con.execute(
        """
        CREATE TABLE task_results (
            model_name VARCHAR,
            benchmark VARCHAR,
            dataset_id VARCHAR,
            dataset_name VARCHAR,
            task_name VARCHAR,
            task_key VARCHAR,
            score DOUBLE,
            aggregate_metric VARCHAR,
            embedding_variant_name VARCHAR,
            embedding_dim INTEGER,
            quantization VARCHAR
        )
        """
    )
    for model_name, variant, dim, scores in [
        ("Example/model", None, 768, [0.6, 0.8, 0.4]),
        ("Other/better", None, 1024, [0.9, 0.9, 0.7]),
        ("Other/better", "truncate_dim_512", 512, [0.95, 0.95, 0.75]),
        ("bm25", None, None, [0.2, 0.3, 0.1]),
    ]:
        for dataset_id, dataset_name, task_name, score in [
            ("hakari-bench/NanoBEIR-en", "NanoBEIR-en", "arguana", scores[0]),
            ("hakari-bench/NanoBEIR-ja", "NanoBEIR-ja", "arguana", scores[1]),
            ("hakari-bench/NanoRTEB", "NanoRTEB", "task-a", scores[2]),
        ]:
            con.execute(
                """
                INSERT INTO task_results VALUES (?, ?, ?, ?, ?, ?, ?, 'ndcg@10', ?, ?, NULL)
                """,
                [
                    model_name,
                    "MNanoBEIR" if "NanoBEIR" in dataset_id else "NanoRTEB",
                    dataset_id,
                    dataset_name,
                    task_name,
                    task_name,
                    score,
                    variant,
                    dim,
                ],
            )
    con.close()

    rendered = template.generate_pr_template(
        result_dir,
        repo_path="PROJECT_ROOT/hakari-results/Example__model",
        comparison_duckdb_path=duckdb_path,
        comparison_models=["Other/better", "bm25"],
    )

    comparison_index = rendered.index("## DuckDB Nano-set Comparison")
    overall_index = rendered.index("## Overall nDCG@10")
    assert comparison_index < overall_index
    assert "| Overall component | Example/model (768 dims) | Other/better (512 dims) | bm25 |" in rendered
    assert "| Overall | 0.5500 | **0.8500** | 0.1750 |" in rendered
    assert "| MNanoBEIR | 0.7000 | **0.9500** | 0.2500 |" in rendered
    assert "| NanoRTEB | 0.4000 | **0.7500** | 0.1000 |" in rendered


def _write_result(
    path: Path,
    *,
    dataset_name: str,
    dataset_id: str,
    task_name: str,
    score: float,
) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    payload = {
        "generated_at_utc": "2026-06-01T00:00:00+00:00",
        "model": {
            "method": "dense",
            "id": "Example/model",
            "source": {"name": "Example/model", "revision": "abc123"},
            "device": "cuda:0",
            "dtype": "bf16",
            "attn_implementation": "sdpa",
            "trust_remote_code": False,
            "max_seq_length": 8192,
        },
        "environment": {
            "python": "3.12.0",
            "platform": "Linux",
            "package_versions": {
                "torch": "2.9.0",
                "transformers": "4.57.0",
                "sentence-transformers": "5.4.0",
                "datasets": "4.8.0",
            },
            "cuda": {
                "is_available": True,
                "cuda_version": "12.8",
                "devices": [{"index": 0, "name": "Test GPU"}],
            },
        },
        "target": {
            "dataset_name": dataset_name,
            "dataset_id": dataset_id,
            "task_name": task_name,
            "dataset_revision": {"resolved": "dataset-sha"},
        },
        "config": {
            "batch_size": 16,
            "dataset_revision": "dataset-sha",
            "candidate_ranking": "reranking_hybrid",
        },
        "evaluation": {
            "aggregate_metric": "ndcg@10",
            "aggregate_metric_value": score,
            "evaluated_at_utc": "2026-06-01T00:01:00+00:00",
        },
    }
    with lzma.open(path, "wt", encoding="utf-8") as file:
        json.dump(payload, file)
