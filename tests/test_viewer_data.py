from __future__ import annotations

from pathlib import Path

import duckdb

from nano_ir_benchmark.viewer.data import TaskResultRecord, TaskResultsRepository


def test_task_results_repository_returns_pydantic_records_and_base_rows_by_default(tmp_path: Path) -> None:
    db_path = tmp_path / "results.duckdb"
    _write_task_results(
        db_path,
        [
            ("model/a", "BenchA", "bench/a", "BenchA", None, "a1", "a1", 0.90, 10, 12, 8192, None, 768, None),
            (
                "model/a",
                "BenchA",
                "bench/a",
                "BenchA",
                None,
                "a1",
                "a1",
                0.80,
                10,
                12,
                8192,
                "quantize_uint8_docs",
                768,
                "uint8",
            ),
            ("model/b", "BenchA", "bench/a", "BenchA", "split", "a1", "a1", None, 20, 24, 4096, None, 512, None),
            ("model/c", "BenchB", "bench/b", "BenchB", "split", "b1", "b1", 0.70, 30, 36, 2048, None, 256, None),
        ],
        include_embedding_variant_columns=True,
    )

    records = TaskResultsRepository(db_path).fetch_task_results(
        benchmarks=["BenchA"],
        include_embedding_variants=False,
    )

    assert records == [
        TaskResultRecord(
            model_name="model/a",
            benchmark="BenchA",
            dataset_id="bench/a",
            dataset_name="BenchA",
            split_name="",
            task_name="a1",
            task_key="a1",
            score=0.90,
            active_parameters=10,
            total_parameters=12,
            max_seq_length=8192,
            embedding_variant_name=None,
            embedding_dim=768,
            quantization=None,
        )
    ]


def test_task_results_repository_reads_legacy_schema_without_variant_columns(tmp_path: Path) -> None:
    db_path = tmp_path / "results.duckdb"
    _write_task_results(
        db_path,
        [
            ("model/a", "BenchA", "bench/a", "BenchA", None, "a1", "a1", 0.90, 10, 12, 8192),
        ],
        include_embedding_variant_columns=False,
    )

    records = TaskResultsRepository(db_path).fetch_task_results(
        benchmarks=["BenchA"],
        include_embedding_variants=False,
    )

    assert records[0].embedding_variant_name is None
    assert records[0].embedding_dim is None
    assert records[0].quantization is None


def test_task_results_repository_can_fetch_embedding_variant_rows_when_requested(tmp_path: Path) -> None:
    db_path = tmp_path / "results.duckdb"
    _write_task_results(
        db_path,
        [
            ("model/a", "BenchA", "bench/a", "BenchA", None, "a1", "a1", 0.90, 10, 12, 8192, None, 768, None),
            (
                "model/a",
                "BenchA",
                "bench/a",
                "BenchA",
                None,
                "a1",
                "a1",
                0.80,
                10,
                12,
                8192,
                "quantize_uint8_docs",
                768,
                "uint8",
            ),
        ],
        include_embedding_variant_columns=True,
    )

    records = TaskResultsRepository(db_path).fetch_task_results(
        benchmarks=["BenchA"],
        include_embedding_variants=True,
    )

    assert [(record.embedding_variant_name, record.quantization) for record in records] == [
        (None, None),
        ("quantize_uint8_docs", "uint8"),
    ]


def _write_task_results(
    db_path: Path,
    rows: list[tuple],
    *,
    include_embedding_variant_columns: bool,
) -> None:
    con = duckdb.connect(str(db_path))
    try:
        variant_columns = (
            [
                "embedding_variant_name VARCHAR",
                "embedding_dim INTEGER",
                "quantization VARCHAR",
            ]
            if include_embedding_variant_columns
            else []
        )
        columns = [
            "model_name VARCHAR",
            "benchmark VARCHAR",
            "dataset_id VARCHAR",
            "dataset_name VARCHAR",
            "split_name VARCHAR",
            "task_name VARCHAR",
            "task_key VARCHAR",
            "score DOUBLE",
            "active_parameters BIGINT",
            "total_parameters BIGINT",
            "max_seq_length INTEGER",
            *variant_columns,
        ]
        con.execute(f"CREATE TABLE task_results ({', '.join(columns)})")
        placeholders = ", ".join("?" for _ in rows[0])
        con.executemany(f"INSERT INTO task_results VALUES ({placeholders})", rows)
    finally:
        con.close()
