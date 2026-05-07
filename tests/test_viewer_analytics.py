from __future__ import annotations

from pathlib import Path

import duckdb
import pytest

from hakari_bench.viewer.analytics import ViewerAnalyticsRepository


def test_viewer_summary_counts_base_variant_tasks_and_latest_timestamp(tmp_path: Path) -> None:
    db_path = tmp_path / "results.duckdb"
    _write_analytics_db(db_path)

    summary = ViewerAnalyticsRepository(db_path).fetch_summary()

    assert summary.model_count == 2
    assert summary.benchmark_count == 2
    assert summary.task_count == 3
    assert summary.language_count == 2
    assert summary.base_result_count == 6
    assert summary.variant_result_count == 4
    assert summary.latest_finished_at_utc == "2026-01-02T00:00:00Z"


def test_variant_analysis_aggregates_base_relative_delta_by_variant(tmp_path: Path) -> None:
    db_path = tmp_path / "results.duckdb"
    _write_analytics_db(db_path)

    rows = ViewerAnalyticsRepository(db_path).fetch_variant_analysis(benchmarks=["BenchA"])

    assert [(row.model_name, row.variant_name, row.embedding_dim, row.quantization) for row in rows] == [
        ("model/a", "binary", 768, "binary"),
        ("model/a", "truncate_dim_384", 384, None),
    ]
    by_variant = {row.variant_name: row for row in rows}
    assert by_variant["binary"].task_count == 2
    assert by_variant["binary"].mean_score_100 == pytest.approx(75.0)
    assert by_variant["binary"].base_delta_percent == pytest.approx(-16.6666666667)
    assert by_variant["truncate_dim_384"].base_delta_percent == pytest.approx(-5.5555555556)
    assert "binary_rescore" not in by_variant

    rows_with_rescore = ViewerAnalyticsRepository(db_path).fetch_variant_analysis(
        benchmarks=["BenchA"],
        include_rescore=True,
    )

    assert "binary_rescore" in {row.variant_name for row in rows_with_rescore}


def test_rerank_diagnostics_aggregate_candidate_coverage_and_lift(tmp_path: Path) -> None:
    db_path = tmp_path / "results.duckdb"
    _write_analytics_db(db_path)

    rows = ViewerAnalyticsRepository(db_path).fetch_rerank_diagnostics(benchmarks=["BenchA", "BenchB"])

    assert [(row.benchmark, row.task_count) for row in rows] == [("BenchA", 2), ("BenchB", 1)]
    bench_a = rows[0]
    assert bench_a.query_coverage_percent == pytest.approx(75.0)
    assert bench_a.relevant_coverage_percent == pytest.approx(50.0)
    assert bench_a.mean_lift_points == pytest.approx(2.5)
    assert bench_a.candidate_source == "dataset_candidate_subset"
    assert bench_a.candidate_ranking == "bm25"


def test_dataset_diagnostics_report_language_category_and_saturation(tmp_path: Path) -> None:
    db_path = tmp_path / "results.duckdb"
    _write_analytics_db(db_path)

    rows = ViewerAnalyticsRepository(db_path).fetch_dataset_diagnostics(benchmarks=["BenchA", "BenchB"])

    assert [(row.benchmark, row.task_count, row.language_count, row.category_count) for row in rows] == [
        ("BenchA", 2, 2, 2),
        ("BenchB", 1, 1, 1),
    ]
    bench_a = rows[0]
    assert bench_a.base_rows == 4
    assert bench_a.saturated_rows == 1
    assert bench_a.saturation_percent == pytest.approx(25.0)
    assert bench_a.mean_query_count == pytest.approx(150.0)
    assert bench_a.mean_document_count == pytest.approx(7500.0)


def _write_analytics_db(db_path: Path) -> None:
    con = duckdb.connect(str(db_path))
    try:
        con.execute(
            """
            CREATE TABLE task_results (
                model_name VARCHAR,
                benchmark VARCHAR,
                dataset_id VARCHAR,
                dataset_name VARCHAR,
                split_name VARCHAR,
                task_name VARCHAR,
                task_key VARCHAR,
                score DOUBLE,
                embedding_variant_name VARCHAR,
                embedding_dim INTEGER,
                quantization VARCHAR,
                finished_at_utc VARCHAR
            )
            """
        )
        con.executemany(
            "INSERT INTO task_results VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
            [
                ("model/a", "BenchA", "bench/a", "BenchA", "", "t1", "BenchA::t1", 0.90, None, 768, None, "2026-01-01T00:00:00Z"),
                ("model/a", "BenchA", "bench/a", "BenchA", "", "t2", "BenchA::t2", 0.90, None, 768, None, "2026-01-01T00:00:00Z"),
                ("model/b", "BenchA", "bench/a", "BenchA", "", "t1", "BenchA::t1", 0.95, None, 512, None, "2026-01-02T00:00:00Z"),
                ("model/b", "BenchA", "bench/a", "BenchA", "", "t2", "BenchA::t2", 0.60, None, 512, None, "2026-01-02T00:00:00Z"),
                ("model/a", "BenchA", "bench/a", "BenchA", "", "t1", "BenchA::t1", 0.80, "binary", 768, "binary", "2026-01-01T00:00:00Z"),
                ("model/a", "BenchA", "bench/a", "BenchA", "", "t2", "BenchA::t2", 0.70, "binary", 768, "binary", "2026-01-01T00:00:00Z"),
                ("model/a", "BenchA", "bench/a", "BenchA", "", "t1", "BenchA::t1", 0.82, "binary_rescore", 768, "binary", "2026-01-01T00:00:00Z"),
                ("model/a", "BenchA", "bench/a", "BenchA", "", "t1", "BenchA::t1", 0.85, "truncate_dim_384", 384, None, "2026-01-01T00:00:00Z"),
                ("model/a", "BenchB", "bench/b", "BenchB", "", "t3", "BenchB::t3", 0.50, None, 768, None, "2026-01-01T00:00:00Z"),
                ("model/b", "BenchB", "bench/b", "BenchB", "", "t3", "BenchB::t3", 0.60, None, 512, None, "2026-01-02T00:00:00Z"),
            ],
        )
        con.execute(
            """
            CREATE TABLE dataset_metadata (
                benchmark VARCHAR,
                dataset_id VARCHAR,
                dataset_name VARCHAR,
                split_name VARCHAR,
                task_name VARCHAR,
                task_key VARCHAR,
                language VARCHAR,
                languages VARCHAR[],
                category VARCHAR,
                query_count INTEGER,
                document_count INTEGER,
                query_mean_chars DOUBLE,
                document_mean_chars DOUBLE
            )
            """
        )
        con.executemany(
            "INSERT INTO dataset_metadata VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
            [
                ("BenchA", "bench/a", "BenchA", "", "t1", "BenchA::t1", "en", ["en"], "natural_language", 100, 5000, 10.0, 200.0),
                ("BenchA", "bench/a", "BenchA", "", "t2", "BenchA::t2", "ja", ["ja"], "code", 200, 10000, 30.0, 400.0),
                ("BenchB", "bench/b", "BenchB", "", "t3", "BenchB::t3", "en", ["en"], "natural_language", 50, 1000, 20.0, 100.0),
            ],
        )
        con.execute(
            """
            CREATE TABLE task_diagnostics (
                model_name VARCHAR,
                benchmark VARCHAR,
                dataset_id VARCHAR,
                task_name VARCHAR,
                task_key VARCHAR,
                rerank_lift DOUBLE,
                rerank_status VARCHAR,
                rerank_top_k INTEGER,
                candidate_source VARCHAR,
                candidate_ranking VARCHAR,
                bm25_source VARCHAR,
                query_coverage DOUBLE,
                relevant_coverage DOUBLE
            )
            """
        )
        con.executemany(
            "INSERT INTO task_diagnostics VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
            [
                ("model/a", "BenchA", "bench/a", "t1", "BenchA::t1", 0.05, "available", 100, "dataset_candidate_subset", "bm25", "dataset", 1.00, 0.75),
                ("model/b", "BenchA", "bench/a", "t2", "BenchA::t2", 0.00, "available", 100, "dataset_candidate_subset", "bm25", "dataset", 0.50, 0.25),
                ("model/a", "BenchB", "bench/b", "t3", "BenchB::t3", 0.10, "available", 100, "computed_bm25s", "bm25", "computed", 1.00, 1.00),
            ],
        )
    finally:
        con.close()
