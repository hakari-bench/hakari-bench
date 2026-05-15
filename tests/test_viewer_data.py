from __future__ import annotations

import logging
from pathlib import Path

import duckdb
import pytest

from hakari_bench.viewer.data import TaskResultRecord, TaskResultsRepository, _task_results_order_by
from hakari_bench.viewer.variant_display import VariantDisplayFlags


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


def test_task_results_repository_can_return_lightweight_rows_for_hot_path(tmp_path: Path) -> None:
    db_path = tmp_path / "results.duckdb"
    _write_task_results(
        db_path,
        [
            ("model/a", "BenchA", "bench/a", "BenchA", None, "a1", "a1", 0.90, 10, 12, 8192),
        ],
        include_embedding_variant_columns=False,
        dataset_metadata_rows=[("BenchA", "bench/a", "BenchA", None, "a1", "a1", "ja", ["ja"])],
    )

    rows = TaskResultsRepository(db_path).fetch_task_result_rows(
        benchmarks=["BenchA"],
        include_embedding_variants=False,
    )

    assert rows[0].model_name == "model/a"
    assert rows[0].task_key == "a1"
    assert rows[0].languages == ("ja",)
    assert rows[0].prompt_summary == "model default"
    assert not isinstance(rows[0], TaskResultRecord)


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


def test_task_results_repository_pushes_variant_display_flags_into_sql(tmp_path: Path) -> None:
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
            (
                "model/a",
                "BenchA",
                "bench/a",
                "BenchA",
                None,
                "a1",
                "a1",
                0.83,
                10,
                12,
                8192,
                "truncate_dim_384",
                384,
                None,
            ),
            (
                "model/a",
                "BenchA",
                "bench/a",
                "BenchA",
                None,
                "a1",
                "a1",
                0.82,
                10,
                12,
                8192,
                "truncate_dim_256_quantize_int8_docs",
                256,
                "int8",
            ),
            (
                "model/a",
                "BenchA",
                "bench/a",
                "BenchA",
                None,
                "a1",
                "a1",
                0.81,
                10,
                12,
                8192,
                "binary_rescore",
                768,
                "binary",
            ),
            (
                "model/a",
                "BenchA",
                "bench/a",
                "BenchA",
                None,
                "a1",
                "a1",
                0.75,
                10,
                12,
                8192,
                "custom_variant",
                2048,
                None,
            ),
        ],
        include_embedding_variant_columns=True,
    )

    quantization_records = TaskResultsRepository(db_path).fetch_task_results(
        benchmarks=["BenchA"],
        include_embedding_variants=True,
        variant_display_flags=VariantDisplayFlags(quantization=True),
    )
    cross_variant_records = TaskResultsRepository(db_path).fetch_task_results(
        benchmarks=["BenchA"],
        include_embedding_variants=True,
        variant_display_flags=VariantDisplayFlags(quantization=True, truncate=True),
    )
    rescore_records = TaskResultsRepository(db_path).fetch_task_results(
        benchmarks=["BenchA"],
        include_embedding_variants=True,
        variant_display_flags=VariantDisplayFlags(rescore=True),
    )
    other_records = TaskResultsRepository(db_path).fetch_task_results(
        benchmarks=["BenchA"],
        include_embedding_variants=True,
        variant_display_flags=VariantDisplayFlags(other=True),
    )

    assert [(record.embedding_variant_name, record.quantization) for record in quantization_records] == [
        (None, None),
        ("quantize_uint8_docs", "uint8"),
    ]
    assert [(record.embedding_variant_name, record.quantization) for record in cross_variant_records] == [
        (None, None),
        ("quantize_uint8_docs", "uint8"),
        ("truncate_dim_256_quantize_int8_docs", "int8"),
        ("truncate_dim_384", None),
    ]
    assert [record.embedding_variant_name for record in rescore_records] == [None, "binary_rescore"]
    assert [record.embedding_variant_name for record in other_records] == [None, "custom_variant"]


def test_task_results_repository_logs_duckdb_query_and_record_transform_timing(
    tmp_path: Path,
    caplog: pytest.LogCaptureFixture,
) -> None:
    db_path = tmp_path / "results.duckdb"
    _write_task_results(
        db_path,
        [
            ("model/a", "BenchA", "bench/a", "BenchA", None, "a1", "a1", 0.90, 10, 12, 8192, None, 768, None),
        ],
        include_embedding_variant_columns=True,
    )

    with caplog.at_level(logging.INFO, logger="hakari_bench.viewer"):
        records = TaskResultsRepository(db_path).fetch_task_results(
            benchmarks=["BenchA"],
            include_embedding_variants=False,
        )

    assert len(records) == 1
    messages = [record.getMessage() for record in caplog.records]
    assert any(
        "viewer.duckdb.query" in message
        and "operation=fetch_task_results" in message
        and "row_count=1" in message
        for message in messages
    )
    assert any(
        "viewer.transform" in message
        and "operation=fetch_task_results.records" in message
        and "deduped_row_count=1" in message
        for message in messages
    )


def test_task_results_repository_reads_runtime_option_columns_when_present(tmp_path: Path) -> None:
    db_path = tmp_path / "results.duckdb"
    _write_task_results(
        db_path,
        [
            (
                "model/e5",
                "BenchA",
                "bench/a",
                "BenchA",
                None,
                "a1",
                "a1",
                0.90,
                10,
                12,
                8192,
                "bf16",
                "flash_attention_2",
                "query: ",
                "passage: ",
                None,
                None,
                None,
                None,
                False,
            ),
            (
                "model/gemma",
                "BenchA",
                "bench/a",
                "BenchA",
                None,
                "a1",
                "a1",
                0.80,
                20,
                24,
                2048,
                "bf16",
                "sdpa",
                None,
                None,
                "query",
                "document",
                None,
                None,
                True,
            ),
        ],
        include_embedding_variant_columns=False,
        include_runtime_option_columns=True,
    )

    records = TaskResultsRepository(db_path).fetch_task_results(
        benchmarks=["BenchA"],
        include_embedding_variants=False,
    )

    assert records[0].dtype == "bf16"
    assert records[0].attn_implementation == "flash_attention_2"
    assert records[0].query_prompt == "query: "
    assert records[0].document_prompt == "passage: "
    assert records[0].prompt_summary == "explicit prefixes"
    assert records[0].trust_remote_code is False
    assert records[1].attn_implementation == "sdpa"
    assert records[1].query_prompt_name == "query"
    assert records[1].document_prompt_name == "document"
    assert records[1].prompt_summary == "prompt names"
    assert records[1].trust_remote_code is True


def test_task_results_repository_reads_dataset_languages_when_present(tmp_path: Path) -> None:
    db_path = tmp_path / "results.duckdb"
    _write_task_results(
        db_path,
        [
            ("model/a", "BenchA", "bench/a", "BenchA", None, "a1", "task-ja", 0.90, 10, 12, 8192),
            ("model/a", "BenchA", "bench/a", "BenchA", None, "a2", "task-multi", 0.80, 10, 12, 8192),
        ],
        include_embedding_variant_columns=False,
        dataset_metadata_rows=[
            ("BenchA", "bench/a", "BenchA", None, "a1", "task-ja", "ja", ["ja"]),
            ("BenchA", "bench/a", "BenchA", None, "a2", "task-multi", "multilingual", ["en", "ja"]),
        ],
    )

    records = TaskResultsRepository(db_path).fetch_task_results(
        benchmarks=["BenchA"],
        include_embedding_variants=False,
    )

    assert [(record.task_key, record.language, record.languages) for record in records] == [
        ("task-ja", "ja", ["ja"]),
        ("task-multi", "multilingual", ["en", "ja"]),
    ]


def test_task_results_repository_prefers_materialized_viewer_task_results(tmp_path: Path) -> None:
    db_path = tmp_path / "results.duckdb"
    _write_task_results(
        db_path,
        [
            ("model/a", "BenchA", "bench/a", "BenchA", None, "a1", "task-ja", 0.90, 10, 12, 8192),
        ],
        include_embedding_variant_columns=False,
        dataset_metadata_rows=[("BenchA", "bench/a", "BenchA", None, "a1", "task-ja", "metadata-ja", ["metadata-ja"])],
    )
    con = duckdb.connect(str(db_path))
    try:
        con.execute(
            """
            CREATE TABLE viewer_task_results AS
            SELECT
                model_name,
                benchmark,
                dataset_id,
                dataset_name,
                COALESCE(split_name, '') AS split_name,
                task_name,
                task_key,
                score,
                'viewer-ja' AS language,
                ['viewer-ja']::VARCHAR[] AS languages,
                active_parameters,
                total_parameters,
                max_seq_length,
                NULL AS dtype,
                NULL AS attn_implementation,
                NULL AS query_prompt,
                NULL AS document_prompt,
                NULL AS query_prompt_name,
                NULL AS document_prompt_name,
                NULL AS query_encode_task,
                NULL AS document_encode_task,
                NULL AS trust_remote_code,
                NULL AS embedding_variant_name,
                NULL AS embedding_dim,
                NULL AS quantization
            FROM task_results
            """
        )
    finally:
        con.close()

    records = TaskResultsRepository(db_path).fetch_task_results(
        benchmarks=["BenchA"],
        include_embedding_variants=False,
    )

    assert [(record.task_key, record.language, record.languages) for record in records] == [
        ("task-ja", "viewer-ja", ["viewer-ja"])
    ]


def test_task_results_repository_reads_score_target_from_materialized_viewer_table(tmp_path: Path) -> None:
    db_path = tmp_path / "results.duckdb"
    con = duckdb.connect(str(db_path))
    try:
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
                active_parameters BIGINT,
                total_parameters BIGINT,
                max_seq_length INTEGER,
                dtype VARCHAR,
                attn_implementation VARCHAR,
                query_prompt VARCHAR,
                document_prompt VARCHAR,
                query_prompt_name VARCHAR,
                document_prompt_name VARCHAR,
                query_encode_task VARCHAR,
                document_encode_task VARCHAR,
                trust_remote_code BOOLEAN,
                embedding_variant_name VARCHAR,
                embedding_dim INTEGER,
                quantization VARCHAR
            )
            """
        )
        con.executemany(
            "INSERT INTO viewer_task_results VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
            [
                (
                    "model/a",
                    "BenchA",
                    "bench/a",
                    "BenchA",
                    "",
                    "a1",
                    "task-a1",
                    "all",
                    0.80,
                    "ja",
                    ["ja"],
                    10,
                    12,
                    8192,
                    None,
                    None,
                    None,
                    None,
                    None,
                    None,
                    None,
                    None,
                    None,
                    None,
                    768,
                    None,
                ),
                (
                    "model/a",
                    "BenchA",
                    "bench/a",
                    "BenchA",
                    "",
                    "a1",
                    "task-a1",
                    "reranking",
                    0.92,
                    "ja",
                    ["ja"],
                    10,
                    12,
                    8192,
                    None,
                    None,
                    None,
                    None,
                    None,
                    None,
                    None,
                    None,
                    None,
                    None,
                    768,
                    None,
                ),
            ],
        )
    finally:
        con.close()

    records = TaskResultsRepository(db_path).fetch_task_results(
        benchmarks=["BenchA"],
        score_target="reranking",
        include_embedding_variants=False,
    )

    assert [(record.task_key, record.score) for record in records] == [("task-a1", 0.92)]


def test_materialized_viewer_task_results_do_not_add_query_time_order_by() -> None:
    assert _task_results_order_by("viewer_task_results", {"embedding_variant_name"}) == ""
    assert _task_results_order_by("task_results", {"embedding_variant_name"}).startswith("ORDER BY")


def _write_task_results(
    db_path: Path,
    rows: list[tuple],
    *,
    include_embedding_variant_columns: bool,
    include_runtime_option_columns: bool = False,
    dataset_metadata_rows: list[tuple] | None = None,
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
        runtime_columns = (
            [
                "dtype VARCHAR",
                "attn_implementation VARCHAR",
                "query_prompt VARCHAR",
                "document_prompt VARCHAR",
                "query_prompt_name VARCHAR",
                "document_prompt_name VARCHAR",
                "query_encode_task VARCHAR",
                "document_encode_task VARCHAR",
                "trust_remote_code BOOLEAN",
            ]
            if include_runtime_option_columns
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
            *runtime_columns,
            *variant_columns,
        ]
        con.execute(f"CREATE TABLE task_results ({', '.join(columns)})")
        placeholders = ", ".join("?" for _ in rows[0])
        con.executemany(f"INSERT INTO task_results VALUES ({placeholders})", rows)
        if dataset_metadata_rows is not None:
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
                    languages VARCHAR[]
                )
                """
            )
            con.executemany(
                "INSERT INTO dataset_metadata VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
                dataset_metadata_rows,
            )
    finally:
        con.close()
