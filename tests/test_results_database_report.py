from __future__ import annotations

import json
import math
import hashlib
from pathlib import Path
import sys

import duckdb
import pytest
from pydantic import ValidationError

from hakari_bench.viewer.config import BenchmarkConfig, OverallConfig, ViewerConfig
from hakari_bench.warehouse_schema import (
    DatasetMetadataRow,
    MetricLongRow,
    RetrievalRankingRow,
    TaskDiagnosticRow,
    TaskResultRow,
)
from scripts import build_results_database_and_report as report


def test_nanomteb_japanese_is_a_ranked_benchmark() -> None:
    assert "NanoJMTEB-v2" in report.TARGET_BENCHMARKS
    assert report.benchmark_name("hakari-bench/NanoJMTEB-v2", "NanoJMTEB-v2") == "NanoJMTEB-v2"


def test_nanorteb_is_a_ranked_benchmark() -> None:
    assert "NanoRTEB" in report.TARGET_BENCHMARKS
    assert report.benchmark_name("hakari-bench/NanoRTEB", "NanoRTEB") == "NanoRTEB"


def test_nanolongembed_is_a_ranked_benchmark() -> None:
    assert "NanoLongEmbed" in report.TARGET_BENCHMARKS
    assert report.benchmark_name("hakari-bench/NanoLongEmbed", "NanoLongEmbed") == "NanoLongEmbed"


def test_nanocoir_is_a_ranked_benchmark() -> None:
    assert "NanoCoIR" in report.TARGET_BENCHMARKS
    assert report.benchmark_name("hakari-bench/NanoCoIR", "NanoCoIR") == "NanoCoIR"


def test_insert_duckdb_rows_loads_rows_in_chunks() -> None:
    con = duckdb.connect()
    try:
        con.execute("CREATE TABLE sample (name VARCHAR, score DOUBLE)")

        report._insert_duckdb_rows(con, "sample", ("name", "score"), iter(()), chunk_size=1)
        report._insert_duckdb_rows(
            con,
            "sample",
            ("name", "score"),
            (("a", 0.1), ("b", 0.2), ("c", 0.3)),
            chunk_size=2,
        )

        assert con.execute("SELECT name, score FROM sample ORDER BY name").fetchall() == [
            ("a", 0.1),
            ("b", 0.2),
            ("c", 0.3),
        ]
    finally:
        con.close()


def test_read_json_reads_utf8_bytes(tmp_path: Path) -> None:
    path = tmp_path / "payload.json"
    path.write_text(json.dumps({"name": "日本語", "score": 0.42}), encoding="utf-8")

    assert report._read_json(path) == {"name": "日本語", "score": 0.42}


def test_read_json_falls_back_for_non_standard_json_numbers(tmp_path: Path) -> None:
    path = tmp_path / "payload.json"
    path.write_text('{"score": NaN}', encoding="utf-8")

    assert math.isnan(report._read_json(path)["score"])


def test_nanomteb_chinese_is_a_ranked_benchmark() -> None:
    assert "NanoCMTEB" in report.TARGET_BENCHMARKS
    assert report.benchmark_name("hakari-bench/NanoCMTEB", "NanoCMTEB") == "NanoCMTEB"


def test_new_nano_benchmarks_are_ranked_benchmarks() -> None:
    assert "NanoBIRCO" in report.TARGET_BENCHMARKS
    assert "NanoDAPFAM" in report.TARGET_BENCHMARKS
    assert report.benchmark_name("hakari-bench/NanoBIRCO", "NanoBIRCO") == "NanoBIRCO"
    assert report.benchmark_name("hakari-bench/NanoDAPFAM", "NanoDAPFAM") == "NanoDAPFAM"


def test_int_or_none_ignores_non_finite_numbers() -> None:
    assert report._int_or_none(math.inf) is None
    assert report._int_or_none(-math.inf) is None
    assert report._int_or_none(math.nan) is None


def test_language_specific_nanomteb_benchmarks_are_ranked_separately() -> None:
    language_benchmarks = [
        "NanoMTEB-Dutch",
        "NanoMTEB-French",
        "NanoMTEB-German",
        "NanoJMTEB-v2",
        "NanoMTEB-Korean",
        "NanoFaMTEB-v2",
        "NanoMTEB-Polish",
        "NanoRuMTEB",
        "NanoMTEB-Scandinavian",
        "NanoMTEB-Spanish",
        "NanoMTEB-Thai",
        "NanoVNMTEB",
        "NanoMTEB-Misc",
    ]

    for benchmark in language_benchmarks:
        assert benchmark in report.TARGET_BENCHMARKS
        assert report.benchmark_name(f"hakari-bench/{benchmark}", benchmark) == benchmark


def test_benchmark_name_uses_yaml_match_patterns_and_prefers_longest_match() -> None:
    benchmark_configs = [
        BenchmarkConfig(name="NanoMTEB", matches=["NanoMTEB"]),
        BenchmarkConfig(name="NanoMTEB-Dutch", matches=["NanoMTEB-Dutch"]),
        BenchmarkConfig(name="CustomBench", matches=["uploaded/custom-dataset"]),
        BenchmarkConfig(name="MNanoBEIR", matches=["NanoBEIR"]),
    ]

    assert (
        report.benchmark_name(
            "hakari-bench/NanoMTEB-Dutch",
            "NanoMTEB-Dutch",
            benchmark_configs=benchmark_configs,
        )
        == "NanoMTEB-Dutch"
    )
    assert (
        report.benchmark_name(
            "uploaded/custom-dataset",
            "arbitrary-name",
            benchmark_configs=benchmark_configs,
        )
        == "CustomBench"
    )
    assert (
        report.benchmark_name(
            "hakari-bench/NanoBEIR-en",
            "NanoBEIR-en",
            benchmark_configs=benchmark_configs,
        )
        == "MNanoBEIR"
    )


def test_load_results_uses_yaml_benchmark_matches(tmp_path: Path) -> None:
    model_dir = tmp_path / "model"
    task_path = model_dir / "uploaded__custom-dataset" / "task.json"
    task_path.parent.mkdir(parents=True)
    task_path.write_text(
        json.dumps(
            {
                "model": {"id": "example/model"},
                "target": {
                    "dataset_id": "uploaded/custom-dataset",
                    "dataset_name": "custom-name",
                    "task_name": "task",
                },
                "evaluation": {"aggregate_metric_value": 0.5},
            }
        ),
        encoding="utf-8",
    )

    rows, _, _, _, _, _ = report.load_results(
        tmp_path,
        benchmark_configs=[BenchmarkConfig(name="CustomBench", matches=["uploaded/custom-dataset"])],
    )

    assert len(rows) == 1
    assert rows[0].benchmark == "CustomBench"

def test_main_builds_duckdb_without_static_html_report(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    results_dir = tmp_path / "results"
    task_path = results_dir / "model" / "hakari-bench__NanoJMTEB-v2" / "ja_cwir.json"
    task_path.parent.mkdir(parents=True)
    task_path.write_text(
        json.dumps(
            {
                "model": {"id": "example/model"},
                "target": {
                    "dataset_name": "NanoJMTEB-v2",
                    "dataset_id": "hakari-bench/NanoJMTEB-v2",
                    "split_name": "ja_cwir",
                    "task_name": "ja_cwir",
                },
                "evaluation": {"aggregate_metric": "ndcg@10", "aggregate_metric_value": 0.42},
                "metrics": {"ja_cwir_ndcg@10": 0.42},
            }
        ),
        encoding="utf-8",
    )
    db_path = tmp_path / "hakari_bench.duckdb"
    html_path = tmp_path / "report.html"
    monkeypatch.setattr(
        sys,
        "argv",
        [
            "build_results_database_and_report.py",
            "--results-dir",
            str(results_dir),
            "--duckdb-path",
            str(db_path),
        ],
    )

    report.main()

    assert db_path.exists()
    assert not html_path.exists()


def test_load_results_reuses_unchanged_incremental_duckdb_rows(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    results_dir = tmp_path / "results"
    task_path = results_dir / "model" / "hakari-bench__NanoJMTEB-v2" / "ja_cwir.json"
    task_path.parent.mkdir(parents=True)
    task_path.write_text(
        json.dumps(
            {
                "model": {"id": "example/model"},
                "target": {
                    "dataset_name": "NanoJMTEB-v2",
                    "dataset_id": "hakari-bench/NanoJMTEB-v2",
                    "split_name": "ja_cwir",
                    "task_name": "ja_cwir",
                },
                "evaluation": {"aggregate_metric": "ndcg@10", "aggregate_metric_value": 0.42},
                "metrics": {"ja_cwir_ndcg@10": 0.42},
            }
        ),
        encoding="utf-8",
    )
    rows, runs, metric_rows, diagnostic_rows, dataset_metadata_rows, ranking_rows = report.load_results(results_dir)
    db_path = tmp_path / "hakari_bench.duckdb"
    report.write_duckdb(
        db_path,
        runs=runs,
        rows=rows,
        metric_rows=metric_rows,
        diagnostic_rows=diagnostic_rows,
        dataset_metadata_rows=dataset_metadata_rows,
        ranking_rows=ranking_rows,
        standings={},
        borda_rows=[],
    )
    monkeypatch.setattr(
        report,
        "_read_json",
        lambda path: pytest.fail(f"unchanged incremental cache should not parse {path}"),
    )

    cached_rows, cached_runs, cached_metric_rows, cached_diagnostic_rows, cached_dataset_metadata_rows, cached_ranking_rows = (
        report.load_results(results_dir, incremental_db_path=db_path)
    )

    assert cached_rows == rows
    assert cached_runs == runs
    assert cached_metric_rows == metric_rows
    assert cached_diagnostic_rows == diagnostic_rows
    assert cached_dataset_metadata_rows == dataset_metadata_rows
    assert cached_ranking_rows == []


def test_main_incremental_noops_when_sources_are_unchanged(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    results_dir = tmp_path / "results"
    task_path = results_dir / "model" / "hakari-bench__NanoJMTEB-v2" / "ja_cwir.json"
    task_path.parent.mkdir(parents=True)
    task_path.write_text(
        json.dumps(
            {
                "model": {"id": "example/model"},
                "target": {
                    "dataset_name": "NanoJMTEB-v2",
                    "dataset_id": "hakari-bench/NanoJMTEB-v2",
                    "split_name": "ja_cwir",
                    "task_name": "ja_cwir",
                },
                "evaluation": {"aggregate_metric": "ndcg@10", "aggregate_metric_value": 0.42},
                "metrics": {"ja_cwir_ndcg@10": 0.42},
            }
        ),
        encoding="utf-8",
    )
    rows, runs, metric_rows, diagnostic_rows, dataset_metadata_rows, ranking_rows = report.load_results(results_dir)
    db_path = tmp_path / "hakari_bench.duckdb"
    report.write_duckdb(
        db_path,
        runs=runs,
        rows=rows,
        metric_rows=metric_rows,
        diagnostic_rows=diagnostic_rows,
        dataset_metadata_rows=dataset_metadata_rows,
        ranking_rows=ranking_rows,
        standings={},
        borda_rows=[],
    )
    monkeypatch.setattr(
        report,
        "write_duckdb",
        lambda *args, **kwargs: pytest.fail("unchanged incremental build should not rewrite DuckDB"),
    )
    monkeypatch.setattr(
        sys,
        "argv",
        [
            "build_results_database_and_report.py",
            "--incremental",
            "--results-dir",
            str(results_dir),
            "--duckdb-path",
            str(db_path),
        ],
    )

    report.main()


def test_load_results_incremental_parses_only_changed_sources(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    results_dir = tmp_path / "results"
    first_path = results_dir / "model" / "hakari-bench__NanoJMTEB-v2" / "ja_cwir.json"
    second_path = results_dir / "model" / "hakari-bench__NanoJMTEB-v2" / "ja_nfcorpus.json"
    first_path.parent.mkdir(parents=True)
    for task_path, score in ((first_path, 0.42), (second_path, 0.24)):
        task_path.write_text(
            json.dumps(
                {
                    "model": {"id": "example/model"},
                    "target": {
                        "dataset_name": "NanoJMTEB-v2",
                        "dataset_id": "hakari-bench/NanoJMTEB-v2",
                        "split_name": task_path.stem,
                        "task_name": task_path.stem,
                    },
                    "evaluation": {"aggregate_metric": "ndcg@10", "aggregate_metric_value": score},
                    "metrics": {f"{task_path.stem}_ndcg@10": score},
                }
            ),
            encoding="utf-8",
        )
    rows, runs, metric_rows, diagnostic_rows, dataset_metadata_rows, ranking_rows = report.load_results(results_dir)
    db_path = tmp_path / "hakari_bench.duckdb"
    report.write_duckdb(
        db_path,
        runs=runs,
        rows=rows,
        metric_rows=metric_rows,
        diagnostic_rows=diagnostic_rows,
        dataset_metadata_rows=dataset_metadata_rows,
        ranking_rows=ranking_rows,
        standings={},
        borda_rows=[],
    )
    second_path.write_text(
        json.dumps(
            {
                "model": {"id": "example/model"},
                "target": {
                    "dataset_name": "NanoJMTEB-v2",
                    "dataset_id": "hakari-bench/NanoJMTEB-v2",
                    "split_name": "ja_nfcorpus",
                    "task_name": "ja_nfcorpus",
                },
                "evaluation": {"aggregate_metric": "ndcg@10", "aggregate_metric_value": 0.9},
                "metrics": {"ja_nfcorpus_ndcg@10": 0.9},
            }
        ),
        encoding="utf-8",
    )
    original_read_json = report._read_json

    def read_changed_only(path: Path) -> object:
        if path == first_path:
            pytest.fail("unchanged source should be reused from the incremental DuckDB cache")
        return original_read_json(path)

    monkeypatch.setattr(report, "_read_json", read_changed_only)

    cached_rows, cached_runs, cached_metric_rows, _, _, _ = report.load_results(
        results_dir,
        incremental_db_path=db_path,
    )

    scores_by_task = {row.task_name: row.score for row in cached_rows}
    metric_scores_by_task = {row.task_name: row.metric_value for row in cached_metric_rows}
    assert scores_by_task == {"ja_cwir": 0.42, "ja_nfcorpus": 0.9}
    assert metric_scores_by_task == {"ja_cwir": 0.42, "ja_nfcorpus": 0.9}
    assert cached_runs[0]["aggregate_metric_mean"] == pytest.approx(0.66)


def test_load_results_incremental_parses_only_added_sources(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    base_dir = tmp_path / "base"
    added_dir = tmp_path / "added"
    existing_path = base_dir / "model_A" / "hakari-bench__NanoJMTEB-v2" / "ja_cwir.json"
    added_path = added_dir / "model_B" / "hakari-bench__NanoJMTEB-v2" / "ja_cwir.json"
    _write_minimal_task_result(
        existing_path,
        model_id="example/model_A",
        task_name="ja_cwir",
        score=0.42,
    )
    rows, runs, metric_rows, diagnostic_rows, dataset_metadata_rows, ranking_rows = report.load_results(base_dir)
    db_path = tmp_path / "hakari_bench.duckdb"
    report.write_duckdb(
        db_path,
        runs=runs,
        rows=rows,
        metric_rows=metric_rows,
        diagnostic_rows=diagnostic_rows,
        dataset_metadata_rows=dataset_metadata_rows,
        ranking_rows=ranking_rows,
        standings={},
        borda_rows=[],
    )
    _write_minimal_task_result(
        added_path,
        model_id="example/model_B",
        task_name="ja_cwir",
        score=0.84,
    )
    original_read_json = report._read_json

    def read_added_only(path: Path) -> object:
        if path == existing_path:
            pytest.fail("unchanged existing source should be reused from the incremental DuckDB cache")
        return original_read_json(path)

    monkeypatch.setattr(report, "_read_json", read_added_only)

    cached_rows, cached_runs, cached_metric_rows, cached_diagnostic_rows, _, _ = report.load_results(
        [added_dir, base_dir],
        incremental_db_path=db_path,
    )

    assert [(row.model_name, row.score) for row in cached_rows] == [
        ("example/model_A", 0.42),
        ("example/model_B", 0.84),
    ]
    assert [(row.model_name, row.metric_value) for row in cached_metric_rows] == [
        ("example/model_A", 0.42),
        ("example/model_B", 0.84),
    ]
    assert [(row.model_name, row.base_score) for row in cached_diagnostic_rows] == [
        ("example/model_A", 0.42),
        ("example/model_B", 0.84),
    ]
    assert [(run["model_name"], run["aggregate_metric_mean"]) for run in cached_runs] == [
        ("example/model_A", 0.42),
        ("example/model_B", 0.84),
    ]


def test_main_appends_results_dir_to_existing_duckdb_without_reading_existing_json(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    base_dir = tmp_path / "base"
    added_dir = tmp_path / "added"
    existing_path = base_dir / "model_A" / "hakari-bench__NanoJMTEB-v2" / "ja_cwir.json"
    added_path = added_dir / "model_B" / "hakari-bench__NanoJMTEB-v2" / "ja_cwir.json"
    _write_minimal_task_result(
        existing_path,
        model_id="example/model_A",
        task_name="ja_cwir",
        score=0.42,
    )
    rows, runs, metric_rows, diagnostic_rows, dataset_metadata_rows, ranking_rows = report.load_results(base_dir)
    db_path = tmp_path / "hakari_bench.duckdb"
    report.write_duckdb(
        db_path,
        runs=runs,
        rows=rows,
        metric_rows=metric_rows,
        diagnostic_rows=diagnostic_rows,
        dataset_metadata_rows=dataset_metadata_rows,
        ranking_rows=ranking_rows,
        standings={},
        borda_rows=[],
    )
    _write_minimal_task_result(
        added_path,
        model_id="example/model_B",
        task_name="ja_cwir",
        score=0.84,
    )
    original_read_json = report._read_json

    def read_added_only(path: Path) -> object:
        if path == existing_path:
            pytest.fail("append mode should not read existing result JSON")
        return original_read_json(path)

    monkeypatch.setattr(report, "_read_json", read_added_only)
    monkeypatch.setattr(
        sys,
        "argv",
        [
            "build_results_database_and_report.py",
            "--append-results-dir",
            str(added_dir),
            "--duckdb-path",
            str(db_path),
        ],
    )

    report.main()

    con = duckdb.connect(str(db_path), read_only=True)
    try:
        assert con.execute(
            "SELECT model_name, score FROM task_results ORDER BY model_name"
        ).fetchall() == [
            ("example/model_A", 0.42),
            ("example/model_B", 0.84),
        ]
        assert con.execute("SELECT count(*) FROM source_load_state").fetchone() == (2,)
        assert con.execute(
            "SELECT source_count, changed_count FROM ingestion_batches ORDER BY finished_at_utc"
        ).fetchall()[-1] == (2, 1)
        assert con.execute(
            "SELECT model_name, score FROM viewer_task_results ORDER BY model_name"
        ).fetchall() == [
            ("example/model_A", 0.42),
            ("example/model_B", 0.84),
        ]
    finally:
        con.close()


def test_load_results_merges_multiple_results_dirs_by_argument_order(tmp_path: Path) -> None:
    preferred_dir = tmp_path / "preferred"
    fallback_dir = tmp_path / "fallback"
    _write_minimal_task_result(
        preferred_dir / "model_A" / "hakari-bench__NanoJMTEB-v2" / "ja_cwir.json",
        model_id="example/model_A",
        task_name="ja_cwir",
        score=0.80,
    )
    _write_minimal_task_result(
        fallback_dir / "model_A" / "hakari-bench__NanoJMTEB-v2" / "ja_cwir.json",
        model_id="example/model_A",
        task_name="ja_cwir",
        score=0.20,
    )
    _write_minimal_task_result(
        fallback_dir / "model_B" / "hakari-bench__NanoJMTEB-v2" / "ja_cwir.json",
        model_id="example/model_B",
        task_name="ja_cwir",
        score=0.60,
    )

    rows, runs, metric_rows, diagnostic_rows, dataset_metadata_rows, ranking_rows = report.load_results(
        [preferred_dir, fallback_dir]
    )

    assert ranking_rows == []
    assert len(diagnostic_rows) == 2
    assert len(dataset_metadata_rows) == 1
    assert [(row.model_dir, row.score) for row in rows] == [("model_A", 0.80), ("model_B", 0.60)]
    assert rows[0].result_path == str(preferred_dir / "model_A" / "hakari-bench__NanoJMTEB-v2" / "ja_cwir.json")
    assert [(row.model_dir, row.metric_value) for row in metric_rows] == [("model_A", 0.80), ("model_B", 0.60)]
    assert [(run["model_dir"], run["aggregate_metric_mean"]) for run in runs] == [("model_A", 0.80), ("model_B", 0.60)]


def test_load_results_reversing_multiple_results_dirs_changes_duplicate_winner(tmp_path: Path) -> None:
    first_dir = tmp_path / "first"
    second_dir = tmp_path / "second"
    _write_minimal_task_result(
        first_dir / "model_A" / "hakari-bench__NanoJMTEB-v2" / "ja_cwir.json",
        model_id="example/model_A",
        task_name="ja_cwir",
        score=0.80,
    )
    _write_minimal_task_result(
        second_dir / "model_A" / "hakari-bench__NanoJMTEB-v2" / "ja_cwir.json",
        model_id="example/model_A",
        task_name="ja_cwir",
        score=0.20,
    )

    rows, *_ = report.load_results([second_dir, first_dir])

    assert [(row.model_dir, row.score) for row in rows] == [("model_A", 0.20)]
    assert rows[0].result_path == str(second_dir / "model_A" / "hakari-bench__NanoJMTEB-v2" / "ja_cwir.json")


def test_load_results_can_let_later_results_dirs_overwrite_duplicate_tasks(tmp_path: Path) -> None:
    base_dir = tmp_path / "base"
    override_dir = tmp_path / "override"
    _write_minimal_task_result(
        base_dir / "model_A" / "hakari-bench__NanoJMTEB-v2" / "ja_cwir.json",
        model_id="example/model_A",
        task_name="ja_cwir",
        score=0.80,
    )
    _write_minimal_task_result(
        override_dir / "model_A" / "hakari-bench__NanoJMTEB-v2" / "ja_cwir.json",
        model_id="example/model_A",
        task_name="ja_cwir",
        score=0.20,
    )

    rows, runs, metric_rows, diagnostic_rows, *_ = report.load_results(
        [base_dir, override_dir],
        duplicate_result_policy="last-wins",
    )

    assert [(row.model_dir, row.score) for row in rows] == [("model_A", 0.20)]
    assert rows[0].result_path == str(override_dir / "model_A" / "hakari-bench__NanoJMTEB-v2" / "ja_cwir.json")
    assert [(row.model_dir, row.metric_value) for row in metric_rows] == [("model_A", 0.20)]
    assert [(row.model_dir, row.base_score) for row in diagnostic_rows] == [("model_A", 0.20)]
    assert [(run["model_dir"], run["aggregate_metric_mean"]) for run in runs] == [("model_A", 0.20)]


def test_main_can_overwrite_duplicate_results_from_later_results_dirs(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    base_dir = tmp_path / "base"
    override_dir = tmp_path / "override"
    _write_minimal_task_result(
        base_dir / "model_A" / "hakari-bench__NanoJMTEB-v2" / "ja_cwir.json",
        model_id="example/model_A",
        task_name="ja_cwir",
        score=0.80,
    )
    _write_minimal_task_result(
        override_dir / "model_A" / "hakari-bench__NanoJMTEB-v2" / "ja_cwir.json",
        model_id="example/model_A",
        task_name="ja_cwir",
        score=0.20,
    )
    db_path = tmp_path / "hakari_bench.duckdb"
    monkeypatch.setattr(
        sys,
        "argv",
        [
            "build_results_database_and_report.py",
            "--results-dir",
            str(base_dir),
            "--results-dir",
            str(override_dir),
            "--overwrite-result-duplicates",
            "--duckdb-path",
            str(db_path),
        ],
    )

    report.main()

    con = duckdb.connect(str(db_path), read_only=True)
    try:
        assert con.execute("SELECT model_name, score, result_path FROM task_results").fetchall() == [
            (
                "example/model_A",
                0.20,
                str(override_dir / "model_A" / "hakari-bench__NanoJMTEB-v2" / "ja_cwir.json"),
            )
        ]
        assert con.execute("SELECT source_result_count FROM meta_database").fetchone() == (1,)
    finally:
        con.close()


def test_load_results_deduplicates_multiple_results_dirs_by_model_name_not_model_dir(tmp_path: Path) -> None:
    preferred_dir = tmp_path / "preferred"
    fallback_dir = tmp_path / "fallback"
    _write_minimal_task_result(
        preferred_dir / "foobar_exp128__foobar__final" / "hakari-bench__NanoJMTEB-v2" / "ja_cwir.json",
        model_id="foobar_exp128",
        task_name="ja_cwir",
        score=0.80,
    )
    _write_minimal_task_result(
        fallback_dir / "tmp__other_training_path" / "hakari-bench__NanoJMTEB-v2" / "ja_cwir.json",
        model_id="foobar_exp128",
        task_name="ja_cwir",
        score=0.20,
    )
    _write_minimal_task_result(
        fallback_dir / "tmp__other_training_path" / "hakari-bench__NanoJMTEB-v2" / "ja_nfcorpus.json",
        model_id="foobar_exp128",
        task_name="ja_nfcorpus",
        score=0.60,
    )

    rows, runs, metric_rows, diagnostic_rows, *_ = report.load_results([preferred_dir, fallback_dir])

    assert [(row.task_name, row.model_dir, row.model_name, row.score) for row in rows] == [
        ("ja_cwir", "foobar_exp128__foobar__final", "foobar_exp128", 0.80),
        ("ja_nfcorpus", "tmp__other_training_path", "foobar_exp128", 0.60),
    ]
    assert [(row.task_name, row.model_name, row.metric_value) for row in metric_rows] == [
        ("ja_cwir", "foobar_exp128", 0.80),
        ("ja_nfcorpus", "foobar_exp128", 0.60),
    ]
    assert [(row.task_name, row.model_name, row.base_score) for row in diagnostic_rows] == [
        ("ja_cwir", "foobar_exp128", 0.80),
        ("ja_nfcorpus", "foobar_exp128", 0.60),
    ]
    assert [(run["model_name"], run["split_count"], run["aggregate_metric_mean"]) for run in runs] == [
        ("foobar_exp128", 2, pytest.approx(0.70)),
    ]


def test_load_results_can_filter_model_names(tmp_path: Path) -> None:
    _write_minimal_task_result(
        tmp_path / "hotchpotch__bekko-embedding-pico-beta-unir-v7" / "hakari-bench__NanoJMTEB-v2" / "ja_cwir.json",
        model_id="hotchpotch/bekko-embedding-pico-beta-unir-v7",
        task_name="ja_cwir",
        score=0.80,
    )
    _write_minimal_task_result(
        tmp_path / "hotchpotch__bekko-embedding-pico-beta-unir-v9-GOR" / "hakari-bench__NanoJMTEB-v2" / "ja_cwir.json",
        model_id="hotchpotch/bekko-embedding-pico-beta-unir-v9-GOR",
        task_name="ja_cwir",
        score=0.70,
    )
    _write_minimal_task_result(
        tmp_path / "example__other-model" / "hakari-bench__NanoJMTEB-v2" / "ja_cwir.json",
        model_id="example/other-model",
        task_name="ja_cwir",
        score=0.60,
    )

    rows, runs, *_ = report.load_results(
        tmp_path,
        exclude_model_names={"hotchpotch/bekko-embedding-pico-beta-unir-v9-GOR"},
    )

    assert [row.model_name for row in rows] == [
        "example/other-model",
        "hotchpotch/bekko-embedding-pico-beta-unir-v7",
    ]
    assert [run["model_name"] for run in runs] == [
        "example/other-model",
        "hotchpotch/bekko-embedding-pico-beta-unir-v7",
    ]


def test_load_results_reads_task_json_as_source(tmp_path: Path) -> None:
    model_dir = tmp_path / "model"
    task_path = model_dir / "hakari-bench__NanoJMTEB-v2" / "ja_cwir.json"
    task_path.parent.mkdir(parents=True)
    ranking_path = task_path.parent / "rankings" / "ja_cwir.top100.json"
    ranking_path.parent.mkdir(parents=True)
    task_path.write_text(
        json.dumps(
            {
                "model": {
                    "id": "example/model",
                    "source": {
                        "type": "huggingface",
                        "name": "example/model",
                        "revision_requested": "main",
                        "revision": "model-sha",
                    },
                    "active_parameters": 3,
                    "total_parameters": 5,
                    "max_seq_length": 8192,
                    "dtype": "bf16",
                    "attn_implementation": "flash_attention_2",
                    "trust_remote_code": True,
                },
                "config": {
                    "query_prompt": "query: ",
                    "document_prompt": "passage: ",
                    "query_prompt_name": None,
                    "document_prompt_name": None,
                    "query_encode_task": None,
                    "document_encode_task": None,
                },
                "environment": {
                    "package_versions": {
                        "torch": "2.9.1",
                        "transformers": "4.57.6",
                        "sentence-transformers": "5.4.1",
                    }
                },
                "experiment_manifest": {"fingerprint_sha256": "abc123"},
                "target": {
                    "dataset_name": "NanoJMTEB-v2",
                    "dataset_id": "hakari-bench/NanoJMTEB-v2",
                    "dataset_revision": {
                        "requested": None,
                        "resolved": "dataset-sha",
                        "source": "huggingface_hub",
                    },
                    "split_name": "ja_cwir",
                    "task_name": "ja_cwir",
                },
                "evaluation": {
                    "aggregate_metric": "ndcg@10",
                    "aggregate_metric_value": 0.42,
                    "evaluated_at_utc": "2026-04-29T00:00:00+00:00",
                },
                "metrics": {"ja_cwir_ndcg@10": 0.42},
                "artifacts": {
                    "top_rankings": {
                        "schema_version": 1,
                        "top_k": 100,
                        "path": "rankings/ja_cwir.top100.json",
                    }
                },
            }
        ),
        encoding="utf-8",
    )
    ranking_path.write_text(
        json.dumps(
            {
                "schema_version": 1,
                "top_k": 100,
                "target": {
                    "dataset_name": "NanoJMTEB-v2",
                    "dataset_id": "hakari-bench/NanoJMTEB-v2",
                    "split_name": "ja_cwir",
                    "task_name": "ja_cwir",
                },
                "rankings": [
                    {
                        "name": "base",
                        "ranking_kind": "retrieval",
                        "embedding_variant_name": None,
                        "distance": "dot",
                        "score_name": "dot",
                        "query_id": "q1",
                        "corpus_ids": ["d1", "d2"],
                    }
                ],
            }
        ),
        encoding="utf-8",
    )

    default_rows, _, _, _, _, default_ranking_rows = report.load_results(tmp_path)
    rows, _, metric_rows, diagnostic_rows, dataset_metadata_rows, ranking_rows = report.load_results(
        tmp_path,
        include_retrieval_rankings=True,
    )

    assert len(default_rows) == 1
    assert default_ranking_rows == []
    assert len(rows) == 1
    assert rows[0].benchmark == "NanoJMTEB-v2"
    assert rows[0].dataset_id == "hakari-bench/NanoJMTEB-v2"
    assert rows[0].dataset_name == "NanoJMTEB-v2"
    assert rows[0].score == 0.42
    assert rows[0].dataset_revision == "dataset-sha"
    assert rows[0].model_revision == "model-sha"
    assert rows[0].model_revision_requested == "main"
    assert rows[0].experiment_fingerprint == "abc123"
    assert rows[0].active_parameters == 3
    assert rows[0].total_parameters == 5
    assert rows[0].query_prompt == "query: "
    assert rows[0].document_prompt == "passage: "
    assert rows[0].trust_remote_code is True
    assert len(metric_rows) == 1
    assert len(diagnostic_rows) == 1
    assert diagnostic_rows[0].base_score == 0.42
    assert len(dataset_metadata_rows) == 1
    assert dataset_metadata_rows[0].language == "ja"
    assert dataset_metadata_rows[0].languages == ["ja"]
    assert dataset_metadata_rows[0].category == "natural_language"
    assert dataset_metadata_rows[0].reference_count is not None
    assert dataset_metadata_rows[0].query_count == 200
    assert [row.rank for row in ranking_rows] == [1, 2]
    assert ranking_rows[0].ranking_path == str(ranking_path)
    assert ranking_rows[0].query_id == "q1"
    assert ranking_rows[0].corpus_id == "d1"


def _write_minimal_task_result(path: Path, *, model_id: str, task_name: str, score: float) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(
            {
                "model": {"id": model_id},
                "target": {
                    "dataset_name": "NanoJMTEB-v2",
                    "dataset_id": "hakari-bench/NanoJMTEB-v2",
                    "split_name": task_name,
                    "task_name": task_name,
                },
                "evaluation": {"aggregate_metric": "ndcg@10", "aggregate_metric_value": score},
                "metrics": {f"{task_name}_ndcg@10": score},
            }
        ),
        encoding="utf-8",
    )


def test_task_result_row_schema_rejects_unknown_fields() -> None:
    with pytest.raises(ValidationError, match="unexpected"):
        TaskResultRow.model_validate(
            {
                "model_dir": "model",
                "model_name": "example/model",
                "benchmark": "NanoJMTEB-v2",
                "dataset_id": "hakari-bench/NanoJMTEB-v2",
                "dataset_name": "NanoJMTEB-v2",
                "task_name": "ja_cwir",
                "task_key": "NanoJMTEB-v2::hakari-bench/NanoJMTEB-v2::ja_cwir",
                "score": 0.42,
                "result_path": "result.json",
                "unexpected": True,
            }
        )


def test_load_results_allows_missing_model_revision_for_existing_results(tmp_path: Path) -> None:
    model_dir = tmp_path / "model"
    task_path = model_dir / "hakari-bench__NanoJMTEB-v2" / "ja_cwir.json"
    task_path.parent.mkdir(parents=True)
    task_path.write_text(
        json.dumps(
            {
                "model": {"id": "example/model"},
                "target": {
                    "dataset_name": "NanoJMTEB-v2",
                    "dataset_id": "hakari-bench/NanoJMTEB-v2",
                    "split_name": "ja_cwir",
                    "task_name": "ja_cwir",
                },
                "evaluation": {"aggregate_metric": "ndcg@10", "aggregate_metric_value": 0.42},
                "metrics": {"ja_cwir_ndcg@10": 0.42},
            }
        ),
        encoding="utf-8",
    )

    rows, *_ = report.load_results(tmp_path)

    assert len(rows) == 1
    assert rows[0].model_revision is None
    assert rows[0].model_revision_requested is None


def test_metric_long_row_schema_exports_duckdb_values() -> None:
    row = MetricLongRow(
        model_dir="model",
        model_name="example/model",
        benchmark="NanoJMTEB-v2",
        dataset_id="hakari-bench/NanoJMTEB-v2",
        task_name="ja_cwir",
        metric_name="ja_cwir_ndcg@10",
        metric_value=0.42,
        result_path="result.json",
    )

    assert row.duckdb_values() == (
        "model",
        "example/model",
        "NanoJMTEB-v2",
        "hakari-bench/NanoJMTEB-v2",
        "ja_cwir",
        "ja_cwir_ndcg@10",
        0.42,
        "result.json",
    )


def test_retrieval_ranking_row_schema_exports_duckdb_values() -> None:
    row = RetrievalRankingRow(
        model_dir="model",
        model_name="example/model",
        benchmark="NanoJMTEB-v2",
        dataset_id="hakari-bench/NanoJMTEB-v2",
        dataset_revision="dataset-sha",
        dataset_name="NanoJMTEB-v2",
        split_name="ja_cwir",
        task_name="ja_cwir",
        task_key="NanoJMTEB-v2::hakari-bench/NanoJMTEB-v2::ja_cwir",
        result_path="result.json",
        ranking_path="rankings/ja_cwir.top100.json",
        ranking_name="base",
        ranking_kind="retrieval",
        embedding_variant_name=None,
        distance="dot",
        score_name="dot",
        query_id="q1",
        rank=1,
        corpus_id="d1",
    )

    assert row.duckdb_values() == (
        "model",
        "example/model",
        "NanoJMTEB-v2",
        "hakari-bench/NanoJMTEB-v2",
        "dataset-sha",
        "NanoJMTEB-v2",
        "ja_cwir",
        "ja_cwir",
        "NanoJMTEB-v2::hakari-bench/NanoJMTEB-v2::ja_cwir",
        "result.json",
        "rankings/ja_cwir.top100.json",
        "base",
        "retrieval",
        None,
        "dot",
        "dot",
        "q1",
        1,
        "d1",
    )


def test_load_results_extracts_task_diagnostics(tmp_path: Path) -> None:
    task_dir = tmp_path / "model" / "hakari-bench__NanoJMTEB-v2"
    task_dir.mkdir(parents=True)
    (task_dir / "ja_cwir.json").write_text(
        json.dumps(
            {
                "model": {"id": "example/model"},
                "environment": {"package_versions": {}},
                "target": {
                    "dataset_name": "NanoJMTEB-v2",
                    "dataset_id": "hakari-bench/NanoJMTEB-v2",
                    "split_name": "ja_cwir",
                    "task_name": "ja_cwir",
                },
                "config": {
                    "candidate_ranking": "bm25",
                    "rerank_top_k": 100,
                    "bm25": {"source": "dataset_candidate_subset"},
                },
                "evaluation": {
                    "aggregate_metric": "ndcg@10",
                    "aggregate_metric_value": 0.42,
                    "rerank_aggregate_metric_value": 0.50,
                    "dataset_load_seconds": 0.25,
                    "wall_seconds": 2.0,
                    "duration_seconds_including_dataset_load": 2.25,
                    "timing": {
                        "query_embedding_seconds": 0.5,
                        "corpus_embedding_seconds": 1.0,
                        "score_and_topk_seconds": 0.3,
                        "metric_compute_seconds": 0.2,
                        "pure_compute_seconds": 2.0,
                    },
                    "reranking_evaluations": [
                        {
                            "source": "dataset_candidate_subset",
                            "status": "available",
                            "candidate_coverage": {
                                "query_coverage": 0.75,
                                "relevant_coverage": 0.60,
                                "covered_query_count": 3,
                                "query_with_relevance_count": 4,
                                "covered_relevant_count": 6,
                                "relevant_count": 10,
                            },
                        }
                    ],
                },
                "metrics": {"ja_cwir_ndcg@10": 0.42},
            }
        ),
        encoding="utf-8",
    )

    _, _, _, diagnostic_rows, _, _ = report.load_results(tmp_path)

    assert len(diagnostic_rows) == 1
    row = diagnostic_rows[0]
    assert row.rerank_lift == pytest.approx(0.08)
    assert row.candidate_ranking == "bm25"
    assert row.bm25_source == "dataset_candidate_subset"
    assert row.query_coverage == 0.75
    assert row.relevant_coverage == 0.60
    assert row.score_and_topk_seconds == 0.3


def test_load_results_builds_runs_from_task_json(tmp_path: Path) -> None:
    task_dir = tmp_path / "local__model_A" / "hakari-bench__NanoJMTEB-v2"
    task_dir.mkdir(parents=True)
    (task_dir / "ja_cwir.json").write_text(
        json.dumps(
            {
                "generated_at_utc": "2026-05-04T00:00:00+00:00",
                "model": {
                    "id": "local/model_A",
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
                    "dataset_name": "NanoJMTEB-v2",
                    "dataset_id": "hakari-bench/NanoJMTEB-v2",
                    "split_name": "ja_cwir",
                    "task_name": "ja_cwir",
                },
                "evaluation": {
                    "aggregate_metric": "ndcg@10",
                    "aggregate_metric_value": 0.42,
                    "started_at_utc": "2026-05-04T00:00:01+00:00",
                    "finished_at_utc": "2026-05-04T00:00:03+00:00",
                },
                "metrics": {"ja_cwir_ndcg@10": 0.42},
            }
        ),
        encoding="utf-8",
    )

    rows, runs, _, _, _, _ = report.load_results(tmp_path)

    assert len(rows) == 1
    assert runs == [
        {
            "model_dir": "local__model_A",
            "model_name": "local/model_A",
            "generated_at_utc": "2026-05-04T00:00:00+00:00",
            "started_at_utc": "2026-05-04T00:00:01+00:00",
            "finished_at_utc": "2026-05-04T00:00:03+00:00",
            "target_count": 1,
            "split_count": 1,
            "cache_hit_count": None,
            "evaluated_count": None,
            "aggregate_metric_mean": 0.42,
            "active_parameters": 3,
            "total_parameters": 5,
            "max_seq_length": 8192,
            "dtype": "bf16",
            "attn_implementation": "flash_attention_2",
            "torch_version": "2.9.1",
            "transformers_version": "4.57.6",
            "sentence_transformers_version": "5.4.1",
        }
    ]


def test_render_html_includes_total_parameters_column() -> None:
    html = report.render_html(data_json=json.dumps({"views": {}, "summary": {"skipped": []}}))

    assert "Total Params" in html


def test_load_results_adds_embedding_variant_rows(tmp_path: Path) -> None:
    model_dir = tmp_path / "model"
    task_path = model_dir / "hakari-bench__NanoJMTEB-v2" / "ja_cwir.json"
    task_path.parent.mkdir(parents=True)
    task_path.write_text(
        json.dumps(
            {
                "model": {"id": "example/model"},
                "environment": {"package_versions": {}},
                "target": {
                    "dataset_name": "NanoJMTEB-v2",
                    "dataset_id": "hakari-bench/NanoJMTEB-v2",
                    "split_name": "ja_cwir",
                    "task_name": "ja_cwir",
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
                "metrics": {"ja_cwir_ndcg@10": 0.42},
            }
        ),
        encoding="utf-8",
    )
    rows, _, _, _, _, _ = report.load_results(tmp_path)

    assert [(row.embedding_variant_name, row.score, row.embedding_dim, row.quantization) for row in rows] == [
        (None, 0.42, 768, None),
        ("truncate_dim_512_quantize_uint8_docs", 0.40, 512, "uint8"),
    ]


def test_write_duckdb_persists_dataset_revision(tmp_path: Path) -> None:
    row = report.TaskResult(
        model_dir="model",
        model_name="example/model",
        benchmark="NanoJMTEB-v2",
        dataset_id="hakari-bench/NanoJMTEB-v2",
        dataset_revision="dataset-sha",
        dataset_revision_requested="main",
        model_revision="model-sha",
        model_revision_requested="main",
        dataset_name="NanoJMTEB-v2",
        split_name="ja_cwir",
        task_name="ja_cwir",
        task_key="NanoJMTEB-v2::hakari-bench/NanoJMTEB-v2::ja_cwir",
        score=0.42,
        aggregate_metric="ndcg@10",
        result_path="result.json",
        active_parameters=3,
        total_parameters=5,
        max_seq_length=8192,
        dtype="bf16",
        attn_implementation="flash_attention_2",
        query_prompt="query: ",
        document_prompt="passage: ",
        query_prompt_name=None,
        document_prompt_name=None,
        query_encode_task=None,
        document_encode_task=None,
        trust_remote_code=True,
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
                "benchmark": "NanoJMTEB-v2",
                "dataset_id": "hakari-bench/NanoJMTEB-v2",
                "task_name": "ja_cwir",
                "metric_name": "ja_cwir_ndcg@10",
                "metric_value": 0.42,
                "result_path": "result.json",
            }
        ],
        ranking_rows=[
            {
                "model_dir": "model",
                "model_name": "example/model",
                "benchmark": "NanoJMTEB-v2",
                "dataset_id": "hakari-bench/NanoJMTEB-v2",
                "dataset_revision": "dataset-sha",
                "dataset_name": "NanoJMTEB-v2",
                "split_name": "ja_cwir",
                "task_name": "ja_cwir",
                "task_key": "NanoJMTEB-v2::hakari-bench/NanoJMTEB-v2::ja_cwir",
                "result_path": "result.json",
                "ranking_path": "rankings/ja_cwir.top100.json",
                "ranking_name": "base",
                "ranking_kind": "retrieval",
                "embedding_variant_name": None,
                "distance": "dot",
                "score_name": "dot",
                "query_id": "q1",
                "rank": 1,
                "corpus_id": "d1",
            }
        ],
        standings=standings,
        borda_rows=borda_rows,
    )

    con = duckdb.connect(str(db_path))
    try:
        run_columns = [row[1] for row in con.execute("PRAGMA table_info('runs')").fetchall()]
        assert run_columns == [
            "model_dir",
            "model_name",
            "generated_at_utc",
            "started_at_utc",
            "finished_at_utc",
            "target_count",
            "split_count",
            "cache_hit_count",
            "evaluated_count",
            "aggregate_metric_mean",
            "active_parameters",
            "total_parameters",
            "max_seq_length",
            "dtype",
            "attn_implementation",
            "torch_version",
            "transformers_version",
            "sentence_transformers_version",
        ]
        assert con.execute(
            "SELECT dataset_revision, dataset_revision_requested, model_revision, model_revision_requested FROM task_results"
        ).fetchone() == ("dataset-sha", "main", "model-sha", "main")
        assert con.execute(
            """
            SELECT query_prompt, document_prompt, query_prompt_name, document_prompt_name,
                   query_encode_task, document_encode_task, trust_remote_code
            FROM task_results
            """
        ).fetchone() == ("query: ", "passage: ", None, None, None, None, True)
        assert con.execute(
            """
            SELECT model_name, benchmark, task_key, score, language, languages
            FROM viewer_task_results
            """
        ).fetchone() == ("example/model", "NanoJMTEB-v2", "NanoJMTEB-v2::hakari-bench/NanoJMTEB-v2::ja_cwir", 0.42, None, None)
        assert con.execute("SELECT base_score FROM task_diagnostics").fetchone() is None
        assert con.execute("SELECT query_id, rank, corpus_id FROM retrieval_rankings").fetchone() == ("q1", 1, "d1")
    finally:
        con.close()


def test_write_duckdb_materializes_task_score_targets(tmp_path: Path) -> None:
    row = report.TaskResult(
        model_dir="model",
        model_name="example/model",
        benchmark="NanoJMTEB-v2",
        dataset_id="hakari-bench/NanoJMTEB-v2",
        dataset_name="NanoJMTEB-v2",
        split_name="ja_cwir",
        task_name="ja_cwir",
        task_key="NanoJMTEB-v2::hakari-bench/NanoJMTEB-v2::ja_cwir",
        score=0.42,
        aggregate_metric="ndcg@10",
        result_path="result.json",
    )
    diagnostic_row = TaskDiagnosticRow(
        model_dir="model",
        model_name="example/model",
        benchmark="NanoJMTEB-v2",
        dataset_id="hakari-bench/NanoJMTEB-v2",
        task_name="ja_cwir",
        task_key="NanoJMTEB-v2::hakari-bench/NanoJMTEB-v2::ja_cwir",
        result_path="result.json",
        base_score=0.42,
        rerank_score=0.50,
        rerank_lift=0.08,
        rerank_status="available",
        rerank_top_k=100,
        candidate_source="dataset_candidate_subset",
        candidate_ranking="bm25",
    )
    standings, borda_rows = report.compute_standings([row])
    db_path = tmp_path / "results.duckdb"

    report.write_duckdb(
        db_path,
        runs=[{"model_dir": "model", "model_name": "example/model"}],
        rows=[row],
        metric_rows=[
            {
                "model_dir": "model",
                "model_name": "example/model",
                "benchmark": "NanoJMTEB-v2",
                "dataset_id": "hakari-bench/NanoJMTEB-v2",
                "task_name": "ja_cwir",
                "metric_name": "ja_cwir_ndcg@10",
                "metric_value": 0.42,
                "result_path": "result.json",
            }
        ],
        diagnostic_rows=[diagnostic_row],
        standings=standings,
        borda_rows=borda_rows,
    )

    con = duckdb.connect(str(db_path))
    try:
        assert con.execute(
            """
            SELECT score_target, score, candidate_ranking, rerank_top_k, embedding_variant_name
            FROM fact_task_score
            ORDER BY score_target
            """
        ).fetchall() == [
            ("all", 0.42, None, None, None),
            ("reranking", 0.50, "bm25", 100, None),
        ]
        assert con.execute(
            """
            SELECT score_target, score
            FROM viewer_task_results
            ORDER BY score_target
            """
        ).fetchall() == [("all", 0.42), ("reranking", 0.50)]
    finally:
        con.close()


def test_write_duckdb_materializes_canonical_dimensions(tmp_path: Path) -> None:
    base_row = report.TaskResult(
        model_dir="model",
        model_name="example/model",
        benchmark="NanoJMTEB-v2",
        dataset_id="hakari-bench/NanoJMTEB-v2",
        dataset_name="NanoJMTEB-v2",
        split_name="ja_cwir",
        task_name="ja_cwir",
        task_key="NanoJMTEB-v2::hakari-bench/NanoJMTEB-v2::ja_cwir",
        score=0.42,
        aggregate_metric="ndcg@10",
        result_path="result.json",
        active_parameters=3,
        total_parameters=5,
        max_seq_length=8192,
        dtype="bf16",
        embedding_dim=768,
    )
    variant_row = base_row.model_copy(
        update={
            "score": 0.40,
            "embedding_variant_name": "truncate_dim_512_quantize_uint8_docs",
            "embedding_dim": 512,
            "quantization": "uint8",
        }
    )
    metadata_row = DatasetMetadataRow(
        benchmark="NanoJMTEB-v2",
        dataset_id="hakari-bench/NanoJMTEB-v2",
        dataset_name="NanoJMTEB-v2",
        split_name="ja_cwir",
        task_name="ja_cwir",
        task_key="NanoJMTEB-v2::hakari-bench/NanoJMTEB-v2::ja_cwir",
        language="ja",
        languages=["ja"],
        category="natural_language",
        query_count=200,
        document_count=500,
    )
    standings, borda_rows = report.compute_standings([base_row])
    db_path = tmp_path / "results.duckdb"

    report.write_duckdb(
        db_path,
        runs=[{"model_dir": "model", "model_name": "example/model"}],
        rows=[base_row, variant_row],
        metric_rows=[
            {
                "model_dir": "model",
                "model_name": "example/model",
                "benchmark": "NanoJMTEB-v2",
                "dataset_id": "hakari-bench/NanoJMTEB-v2",
                "task_name": "ja_cwir",
                "metric_name": "ja_cwir_ndcg@10",
                "metric_value": 0.42,
                "result_path": "result.json",
            }
        ],
        dataset_metadata_rows=[metadata_row],
        standings=standings,
        borda_rows=borda_rows,
    )

    con = duckdb.connect(str(db_path))
    try:
        assert con.execute(
            "SELECT model_id, model_dir, model_name, active_parameters, total_parameters FROM dim_model"
        ).fetchall() == [(1, "model", "example/model", 3, 5)]
        assert con.execute(
            """
            SELECT task_id, benchmark, dataset_id, task_key, language, category, query_count, document_count
            FROM dim_task
            """
        ).fetchall() == [
            (
                1,
                "NanoJMTEB-v2",
                "hakari-bench/NanoJMTEB-v2",
                "NanoJMTEB-v2::hakari-bench/NanoJMTEB-v2::ja_cwir",
                "ja",
                "natural_language",
                200,
                500,
            )
        ]
        assert con.execute(
            """
            SELECT variant_id, variant_key, embedding_variant_name, embedding_dim, quantization, is_base
            FROM dim_variant
            ORDER BY variant_id
            """
        ).fetchall() == [
            (1, "base:768:none", None, 768, None, True),
            (
                2,
                "truncate_dim_512_quantize_uint8_docs:512:uint8",
                "truncate_dim_512_quantize_uint8_docs",
                512,
                "uint8",
                False,
            ),
        ]
    finally:
        con.close()


def test_write_duckdb_records_source_load_state_and_changed_count(tmp_path: Path) -> None:
    result_path = tmp_path / "model" / "hakari-bench__NanoJMTEB-v2" / "ja_cwir.json"
    result_path.parent.mkdir(parents=True)
    result_path.write_text('{"score": 0.42}', encoding="utf-8")
    row = report.TaskResult(
        model_dir="model",
        model_name="example/model",
        benchmark="NanoJMTEB-v2",
        dataset_id="hakari-bench/NanoJMTEB-v2",
        dataset_name="NanoJMTEB-v2",
        split_name="ja_cwir",
        task_name="ja_cwir",
        task_key="NanoJMTEB-v2::hakari-bench/NanoJMTEB-v2::ja_cwir",
        score=0.42,
        aggregate_metric="ndcg@10",
        result_path=str(result_path),
    )
    standings, borda_rows = report.compute_standings([row])
    db_path = tmp_path / "results.duckdb"

    def write_once() -> None:
        report.write_duckdb(
            db_path,
            runs=[{"model_dir": "model", "model_name": "example/model"}],
            rows=[row],
            metric_rows=[
                {
                    "model_dir": "model",
                    "model_name": "example/model",
                    "benchmark": "NanoJMTEB-v2",
                    "dataset_id": "hakari-bench/NanoJMTEB-v2",
                    "task_name": "ja_cwir",
                    "metric_name": "ja_cwir_ndcg@10",
                    "metric_value": 0.42,
                    "result_path": str(result_path),
                }
            ],
            standings=standings,
            borda_rows=borda_rows,
            batch_id="test-batch",
            loaded_at_utc="2026-05-15T00:00:00+00:00",
        )

    write_once()
    expected_hash = hashlib.sha256(result_path.read_bytes()).hexdigest()
    con = duckdb.connect(str(db_path))
    try:
        assert con.execute(
            "SELECT result_path, payload_sha256, last_successful_batch_id FROM source_load_state"
        ).fetchall() == [(str(result_path), expected_hash, "test-batch")]
        assert con.execute("SELECT source_count, changed_count FROM ingestion_batches").fetchone() == (1, 1)
    finally:
        con.close()

    write_once()
    con = duckdb.connect(str(db_path))
    try:
        assert con.execute("SELECT source_count, changed_count FROM ingestion_batches").fetchone() == (1, 0)
    finally:
        con.close()


def test_write_duckdb_records_schema_metadata_and_result_extensions(tmp_path: Path) -> None:
    result_path = tmp_path / "model" / "hakari-bench__NanoJMTEB-v2" / "ja_cwir.json"
    result_path.parent.mkdir(parents=True)
    result_path.write_text(
        json.dumps(
            {
                "model": {"id": "example/model"},
                "target": {"dataset_id": "hakari-bench/NanoJMTEB-v2"},
                "evaluation": {"aggregate_metric_value": 0.42},
                "future_payload": {"kept": True},
            }
        ),
        encoding="utf-8",
    )
    row = report.TaskResult(
        model_dir="model",
        model_name="example/model",
        benchmark="NanoJMTEB-v2",
        dataset_id="hakari-bench/NanoJMTEB-v2",
        dataset_name="NanoJMTEB-v2",
        split_name="ja_cwir",
        task_name="ja_cwir",
        task_key="NanoJMTEB-v2::hakari-bench/NanoJMTEB-v2::ja_cwir",
        score=0.42,
        aggregate_metric="ndcg@10",
        result_path=str(result_path),
    )
    standings, borda_rows = report.compute_standings([row])
    db_path = tmp_path / "results.duckdb"

    def write_database(*, include_result_extensions: bool) -> None:
        report.write_duckdb(
            db_path,
            runs=[{"model_dir": "model", "model_name": "example/model"}],
            rows=[row],
            metric_rows=[
                {
                    "model_dir": "model",
                    "model_name": "example/model",
                    "benchmark": "NanoJMTEB-v2",
                    "dataset_id": "hakari-bench/NanoJMTEB-v2",
                    "task_name": "ja_cwir",
                    "metric_name": "ja_cwir_ndcg@10",
                    "metric_value": 0.42,
                    "result_path": str(result_path),
                }
            ],
            standings=standings,
            borda_rows=borda_rows,
            batch_id="schema-test",
            loaded_at_utc="2026-05-15T00:00:00+00:00",
            include_result_extensions=include_result_extensions,
        )

    write_database(include_result_extensions=False)
    con = duckdb.connect(str(db_path))
    try:
        assert con.execute("SELECT count(*) FROM result_extensions").fetchone() == (0,)
    finally:
        con.close()

    write_database(include_result_extensions=True)

    con = duckdb.connect(str(db_path))
    try:
        assert con.execute("SELECT schema_version, compatibility_level FROM meta_database").fetchone() == (
            report.WAREHOUSE_SCHEMA_VERSION,
            "current",
        )
        assert con.execute("SELECT schema_version, migration_name FROM schema_change_log").fetchone() == (
            report.WAREHOUSE_SCHEMA_VERSION,
            "create_current_warehouse_schema",
        )
        assert con.execute(
            "SELECT result_path, field_path, value_json, discovered_batch_id FROM result_extensions"
        ).fetchall() == [
            (str(result_path), "$.future_payload", '{"kept":true}', "schema-test"),
        ]
    finally:
        con.close()


def test_write_duckdb_materializes_metric_dimension_and_fact(tmp_path: Path) -> None:
    row = report.TaskResult(
        model_dir="model",
        model_name="example/model",
        benchmark="NanoJMTEB-v2",
        dataset_id="hakari-bench/NanoJMTEB-v2",
        dataset_name="NanoJMTEB-v2",
        split_name="ja_cwir",
        task_name="ja_cwir",
        task_key="NanoJMTEB-v2::hakari-bench/NanoJMTEB-v2::ja_cwir",
        score=0.42,
        aggregate_metric="ndcg@10",
        result_path="result.json",
    )
    standings, borda_rows = report.compute_standings([row])
    db_path = tmp_path / "results.duckdb"

    report.write_duckdb(
        db_path,
        runs=[{"model_dir": "model", "model_name": "example/model"}],
        rows=[row],
        metric_rows=[
            {
                "model_dir": "model",
                "model_name": "example/model",
                "benchmark": "NanoJMTEB-v2",
                "dataset_id": "hakari-bench/NanoJMTEB-v2",
                "task_name": "ja_cwir",
                "metric_name": "ja_cwir_ndcg@10",
                "metric_value": 0.42,
                "result_path": "result.json",
            },
            {
                "model_dir": "model",
                "model_name": "example/model",
                "benchmark": "NanoJMTEB-v2",
                "dataset_id": "hakari-bench/NanoJMTEB-v2",
                "task_name": "ja_cwir",
                "metric_name": "ja_cwir_recall@100",
                "metric_value": 0.80,
                "result_path": "result.json",
            },
        ],
        standings=standings,
        borda_rows=borda_rows,
    )

    con = duckdb.connect(str(db_path))
    try:
        assert con.execute(
            "SELECT metric_id, metric_name, metric_family, cutoff FROM dim_metric ORDER BY metric_id"
        ).fetchall() == [
            (1, "ja_cwir_ndcg@10", "ndcg", 10),
            (2, "ja_cwir_recall@100", "recall", 100),
        ]
        assert con.execute(
            """
            SELECT metric_id, model_name, benchmark, task_name, metric_value
            FROM fact_metric_score
            ORDER BY metric_id
            """
        ).fetchall() == [
            (1, "example/model", "NanoJMTEB-v2", "ja_cwir", 0.42),
            (2, "example/model", "NanoJMTEB-v2", "ja_cwir", 0.80),
        ]
    finally:
        con.close()


def test_write_duckdb_materializes_viewer_filter_values(tmp_path: Path) -> None:
    row = report.TaskResult(
        model_dir="model",
        model_name="example/model",
        benchmark="NanoJMTEB-v2",
        dataset_id="hakari-bench/NanoJMTEB-v2",
        dataset_name="NanoJMTEB-v2",
        split_name="ja_cwir",
        task_name="ja_cwir",
        task_key="NanoJMTEB-v2::hakari-bench/NanoJMTEB-v2::ja_cwir",
        score=0.42,
        aggregate_metric="ndcg@10",
        result_path="result.json",
    )
    diagnostic_row = TaskDiagnosticRow(
        model_dir="model",
        model_name="example/model",
        benchmark="NanoJMTEB-v2",
        dataset_id="hakari-bench/NanoJMTEB-v2",
        task_name="ja_cwir",
        task_key="NanoJMTEB-v2::hakari-bench/NanoJMTEB-v2::ja_cwir",
        result_path="result.json",
        base_score=0.42,
        rerank_score=0.50,
        rerank_status="available",
        rerank_top_k=100,
        candidate_ranking="bm25",
    )
    standings, borda_rows = report.compute_standings([row])
    db_path = tmp_path / "results.duckdb"

    report.write_duckdb(
        db_path,
        runs=[{"model_dir": "model", "model_name": "example/model"}],
        rows=[row],
        metric_rows=[
            {
                "model_dir": "model",
                "model_name": "example/model",
                "benchmark": "NanoJMTEB-v2",
                "dataset_id": "hakari-bench/NanoJMTEB-v2",
                "task_name": "ja_cwir",
                "metric_name": "ja_cwir_ndcg@10",
                "metric_value": 0.42,
                "result_path": "result.json",
            }
        ],
        diagnostic_rows=[diagnostic_row],
        standings=standings,
        borda_rows=borda_rows,
    )

    con = duckdb.connect(str(db_path))
    try:
        assert con.execute(
            """
            SELECT filter_name, value, label, row_count, sort_key
            FROM viewer_filter_values
            WHERE filter_name IN ('target', 'benchmark', 'model', 'variant')
            ORDER BY filter_name, sort_key
            """
        ).fetchall() == [
            ("benchmark", "NanoJMTEB-v2", "NanoJMTEB-v2", 2, "NanoJMTEB-v2"),
            ("model", "example/model", "example/model", 2, "example/model"),
            ("target", "all", "All", 1, "0:all"),
            ("target", "reranking", "Reranking", 1, "1:reranking"),
            ("variant", "base", "Base", 2, "0:base"),
        ]
    finally:
        con.close()


def test_build_viewer_leaderboard_mart_materializes_display_modes(tmp_path: Path) -> None:
    base_row = report.TaskResult(
        model_dir="model",
        model_name="example/model",
        benchmark="BenchA",
        dataset_id="bench/a",
        dataset_name="BenchA",
        split_name="task1",
        task_name="task1",
        task_key="BenchA::bench/a::task1",
        score=0.42,
        aggregate_metric="ndcg@10",
        result_path="result.json",
        embedding_dim=384,
    )
    variant_row = base_row.model_copy(
        update={
            "score": 0.40,
            "embedding_variant_name": "int8",
            "quantization": "int8",
        }
    )
    db_path = tmp_path / "results.duckdb"
    report.write_duckdb(
        db_path,
        runs=[{"model_dir": "model", "model_name": "example/model"}],
        rows=[base_row, variant_row],
        metric_rows=[
            {
                "model_dir": "model",
                "model_name": "example/model",
                "benchmark": "BenchA",
                "dataset_id": "bench/a",
                "task_name": "task1",
                "metric_name": "task1_ndcg@10",
                "metric_value": 0.42,
                "result_path": "result.json",
            }
        ],
        dataset_metadata_rows=[
            DatasetMetadataRow(
                benchmark="BenchA",
                dataset_id="bench/a",
                dataset_name="BenchA",
                split_name="task1",
                task_name="task1",
                task_key="BenchA::bench/a::task1",
                language="en",
                languages=["en"],
            )
        ],
        standings={},
        borda_rows=[],
    )
    viewer_config = ViewerConfig(
        benchmarks=[BenchmarkConfig(name="BenchA")],
        overalls=[OverallConfig(name="Overall", label="Overall", benchmarks=["BenchA"])],
    )

    report.build_viewer_leaderboard_mart(db_path, viewer_config=viewer_config, view_names=["Overall"])

    con = duckdb.connect(str(db_path))
    try:
        assert con.execute(
            """
            SELECT view_name, score_target, include_quantization_variants, model_name, mean_score, expected_tasks
            FROM viewer_leaderboard_rows
            WHERE view_name = 'Overall'
              AND score_target = 'all'
              AND include_quantization_variants IN (false, true)
              AND include_truncate_variants = false
              AND include_rescore_variants = false
              AND include_other_variants = false
            ORDER BY include_quantization_variants, model_name
            """
        ).fetchall() == [
            ("Overall", "all", False, "example/model", 42.0, 1),
            ("Overall", "all", True, "example/model (384 dims)", 42.0, 1),
            ("Overall", "all", True, "example/model (384 dims, int8)", 40.0, 1),
        ]
        assert con.execute(
            """
            SELECT view_name, score_target, include_quantization_variants, code, label, task_count
            FROM viewer_leaderboard_language_options
            WHERE view_name = 'Overall'
              AND score_target = 'all'
              AND include_quantization_variants = true
              AND include_truncate_variants = false
              AND include_rescore_variants = false
              AND include_other_variants = false
            """
        ).fetchall() == [("Overall", "all", True, "en", "EN", 1)]
    finally:
        con.close()


def test_export_duckdb_tables_to_parquet_writes_canonical_tables(tmp_path: Path) -> None:
    row = report.TaskResult(
        model_dir="model",
        model_name="example/model",
        benchmark="NanoJMTEB-v2",
        dataset_id="hakari-bench/NanoJMTEB-v2",
        dataset_revision=None,
        dataset_revision_requested=None,
        dataset_name="NanoJMTEB-v2",
        split_name="ja_cwir",
        task_name="ja_cwir",
        task_key="NanoJMTEB-v2::hakari-bench/NanoJMTEB-v2::ja_cwir",
        score=0.42,
        aggregate_metric="ndcg@10",
        result_path="result.json",
        active_parameters=None,
        total_parameters=None,
        max_seq_length=None,
        dtype=None,
        attn_implementation=None,
        query_prompt=None,
        document_prompt=None,
        query_prompt_name=None,
        document_prompt_name=None,
        query_encode_task=None,
        document_encode_task=None,
        trust_remote_code=None,
        torch_version=None,
        transformers_version=None,
        sentence_transformers_version=None,
        started_at_utc=None,
        finished_at_utc=None,
        evaluated_at_utc=None,
        duration_seconds_including_dataset_load=None,
        wall_seconds=None,
    )
    standings, borda_rows = report.compute_standings([row])
    db_path = tmp_path / "results.duckdb"
    parquet_dir = tmp_path / "parquet"
    report.write_duckdb(
        db_path,
        runs=[{"model_dir": "model", "model_name": "example/model"}],
        rows=[row],
        metric_rows=[
            {
                "model_dir": "model",
                "model_name": "example/model",
                "benchmark": "NanoJMTEB-v2",
                "dataset_id": "hakari-bench/NanoJMTEB-v2",
                "task_name": "ja_cwir",
                "metric_name": "ja_cwir_ndcg@10",
                "metric_value": 0.42,
                "result_path": "result.json",
            }
        ],
        standings=standings,
        borda_rows=borda_rows,
    )

    report.export_duckdb_tables_to_parquet(db_path, parquet_dir)

    assert sorted(path.name for path in parquet_dir.glob("*.parquet")) == [
        "borda_task_scores.parquet",
        "dataset_metadata.parquet",
        "dim_metric.parquet",
        "dim_model.parquet",
        "dim_task.parquet",
        "dim_variant.parquet",
        "fact_metric_score.parquet",
        "fact_task_score.parquet",
        "ingestion_batches.parquet",
        "meta_database.parquet",
        "metrics_long.parquet",
        "model_scores.parquet",
        "result_extensions.parquet",
        "retrieval_rankings.parquet",
        "runs.parquet",
        "schema_change_log.parquet",
        "source_load_state.parquet",
        "task_diagnostics.parquet",
        "task_results.parquet",
        "viewer_filter_values.parquet",
        "viewer_leaderboard_language_options.parquet",
        "viewer_leaderboard_rows.parquet",
        "viewer_task_results.parquet",
    ]
    con = duckdb.connect()
    try:
        assert con.execute(f"SELECT model_name, score FROM read_parquet('{parquet_dir / 'task_results.parquet'}')").fetchone() == (
            "example/model",
            0.42,
        )
    finally:
        con.close()
