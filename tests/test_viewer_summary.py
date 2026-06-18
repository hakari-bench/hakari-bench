from __future__ import annotations

from pathlib import Path

import duckdb

from hakari_bench.viewer.summary import ViewerSummaryRepository


def test_viewer_summary_counts_rows_from_viewer_task_results(tmp_path: Path) -> None:
    db_path = tmp_path / "results.duckdb"
    _write_summary_db(db_path)

    summary = ViewerSummaryRepository(db_path).fetch_summary()

    assert summary.model_count == 2
    assert summary.benchmark_count == 2
    assert summary.task_count == 3
    assert summary.language_count == 2
    assert summary.base_result_count == 6
    assert summary.variant_result_count == 4
    assert summary.latest_finished_at_utc == "2026-01-02T00:00:00Z"


def test_viewer_summary_returns_empty_summary_when_database_is_missing(
    tmp_path: Path,
) -> None:
    summary = ViewerSummaryRepository(tmp_path / "missing.duckdb").fetch_summary()

    assert summary.model_count == 0
    assert summary.latest_finished_at_utc is None


def _write_summary_db(db_path: Path) -> None:
    con = duckdb.connect(str(db_path))
    try:
        con.execute(
            """
            CREATE TABLE meta_database (
                schema_version VARCHAR,
                compatibility_level VARCHAR,
                built_at_utc VARCHAR,
                source_result_count INTEGER,
                model_cards_path VARCHAR,
                model_cards_sha256 VARCHAR
            )
            """
        )
        con.execute(
            "INSERT INTO meta_database VALUES (?, ?, ?, ?, ?, ?)",
            ["8", "8", "2026-01-02T00:00:00Z", 10, None, None],
        )
        con.execute(
            """
            CREATE TABLE viewer_task_results (
                model_name VARCHAR,
                benchmark VARCHAR,
                dataset_id VARCHAR,
                dataset_name VARCHAR,
                split_name VARCHAR,
                task_name VARCHAR,
                task_key VARCHAR,
                score_target VARCHAR,
                score DOUBLE,
                language VARCHAR,
                languages VARCHAR[],
                primary_languages VARCHAR[],
                embedding_variant_name VARCHAR
            )
            """
        )
        con.executemany(
            "INSERT INTO viewer_task_results VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
            [
                (
                    "model/a",
                    "BenchA",
                    "bench/a",
                    "BenchA",
                    "",
                    "t1",
                    "BenchA::t1",
                    "all",
                    0.90,
                    "en",
                    ["en"],
                    ["en"],
                    None,
                ),
                (
                    "model/a",
                    "BenchA",
                    "bench/a",
                    "BenchA",
                    "",
                    "t2",
                    "BenchA::t2",
                    "all",
                    0.90,
                    "ja",
                    ["ja"],
                    ["ja"],
                    None,
                ),
                (
                    "model/b",
                    "BenchA",
                    "bench/a",
                    "BenchA",
                    "",
                    "t1",
                    "BenchA::t1",
                    "all",
                    0.95,
                    "en",
                    ["en"],
                    ["en"],
                    None,
                ),
                (
                    "model/b",
                    "BenchA",
                    "bench/a",
                    "BenchA",
                    "",
                    "t2",
                    "BenchA::t2",
                    "all",
                    0.60,
                    "ja",
                    ["ja"],
                    ["ja"],
                    None,
                ),
                (
                    "model/a",
                    "BenchA",
                    "bench/a",
                    "BenchA",
                    "",
                    "t1",
                    "BenchA::t1",
                    "all",
                    0.80,
                    "en",
                    ["en"],
                    ["en"],
                    "binary",
                ),
                (
                    "model/a",
                    "BenchA",
                    "bench/a",
                    "BenchA",
                    "",
                    "t2",
                    "BenchA::t2",
                    "all",
                    0.70,
                    "ja",
                    ["ja"],
                    ["ja"],
                    "binary",
                ),
                (
                    "model/a",
                    "BenchA",
                    "bench/a",
                    "BenchA",
                    "",
                    "t1",
                    "BenchA::t1",
                    "all",
                    0.82,
                    "en",
                    ["en"],
                    ["en"],
                    "binary_rescore",
                ),
                (
                    "model/a",
                    "BenchA",
                    "bench/a",
                    "BenchA",
                    "",
                    "t1",
                    "BenchA::t1",
                    "all",
                    0.85,
                    "en",
                    ["en"],
                    ["en"],
                    "truncate_dim_384",
                ),
                (
                    "model/a",
                    "BenchB",
                    "bench/b",
                    "BenchB",
                    "",
                    "t3",
                    "BenchB::t3",
                    "all",
                    0.50,
                    "en",
                    ["en"],
                    ["en"],
                    None,
                ),
                (
                    "model/b",
                    "BenchB",
                    "bench/b",
                    "BenchB",
                    "",
                    "t3",
                    "BenchB::t3",
                    "all",
                    0.60,
                    "en",
                    ["en"],
                    ["en"],
                    None,
                ),
            ],
        )
    finally:
        con.close()
