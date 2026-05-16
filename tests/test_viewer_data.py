from __future__ import annotations

import logging
from pathlib import Path

import duckdb
import pytest

from hakari_bench.viewer.data import CURRENT_DUCKDB_SCHEMA_VERSION, TaskResultRecord, TaskResultsRepository
from hakari_bench.viewer.variant_display import VariantDisplayFlags


def test_task_results_repository_returns_pydantic_records_and_base_rows_by_default(tmp_path: Path) -> None:
    db_path = tmp_path / "results.duckdb"
    _write_viewer_task_results(
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


def test_task_results_repository_rejects_missing_current_viewer_task_results(tmp_path: Path) -> None:
    db_path = tmp_path / "results.duckdb"
    con = duckdb.connect(str(db_path))
    try:
        con.execute("CREATE TABLE meta_database (schema_version VARCHAR)")
        con.execute("INSERT INTO meta_database VALUES (?)", [CURRENT_DUCKDB_SCHEMA_VERSION])
        con.execute("CREATE TABLE task_results (model_name VARCHAR, benchmark VARCHAR, task_key VARCHAR, score DOUBLE)")
    finally:
        con.close()

    with pytest.raises(RuntimeError, match="viewer_task_results"):
        TaskResultsRepository(db_path).fetch_task_results(
            benchmarks=["BenchA"],
            include_embedding_variants=False,
        )


def test_task_results_repository_rejects_old_schema_version(tmp_path: Path) -> None:
    db_path = tmp_path / "results.duckdb"
    _write_viewer_task_results(
        db_path,
        [
            ("model/a", "BenchA", "bench/a", "BenchA", None, "a1", "a1", 0.90, 10, 12, 8192),
        ],
        schema_version="2",
    )

    with pytest.raises(RuntimeError, match="schema version"):
        TaskResultsRepository(db_path).fetch_task_results(
            benchmarks=["BenchA"],
            include_embedding_variants=False,
        )


def test_task_results_repository_can_return_lightweight_rows_for_hot_path(tmp_path: Path) -> None:
    db_path = tmp_path / "results.duckdb"
    _write_viewer_task_results(
        db_path,
        [
            ("model/a", "BenchA", "bench/a", "BenchA", None, "a1", "a1", 0.90, 10, 12, 8192),
        ],
        rows_override_languages=[("ja", ["ja"])],
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
    _write_viewer_task_results(
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
    _write_viewer_task_results(
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
        ("truncate_dim_384", None),
        ("truncate_dim_256_quantize_int8_docs", "int8"),
    ]
    assert [record.embedding_variant_name for record in rescore_records] == [None, "binary_rescore"]
    assert [record.embedding_variant_name for record in other_records] == [None, "custom_variant"]


def test_task_results_repository_logs_duckdb_query_and_record_transform_timing(
    tmp_path: Path,
    caplog: pytest.LogCaptureFixture,
) -> None:
    db_path = tmp_path / "results.duckdb"
    _write_viewer_task_results(
        db_path,
        [
            ("model/a", "BenchA", "bench/a", "BenchA", None, "a1", "a1", 0.90, 10, 12, 8192, None, 768, None),
        ],
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
    _write_viewer_task_results(
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
    _write_viewer_task_results(
        db_path,
        [
            ("model/a", "BenchA", "bench/a", "BenchA", None, "a1", "task-ja", 0.90, 10, 12, 8192),
            ("model/a", "BenchA", "bench/a", "BenchA", None, "a2", "task-multi", 0.80, 10, 12, 8192),
        ],
        rows_override_languages=[
            ("ja", ["ja"]),
            ("multilingual", ["en", "ja"]),
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


def test_task_results_repository_reads_materialized_viewer_task_results(tmp_path: Path) -> None:
    db_path = tmp_path / "results.duckdb"
    _write_viewer_task_results(
        db_path,
        [
            ("model/a", "BenchA", "bench/a", "BenchA", None, "a1", "task-ja", 0.90, 10, 12, 8192),
        ],
        rows_override_languages=[("viewer-ja", ["viewer-ja"])],
    )

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
        con.execute("CREATE TABLE meta_database (schema_version VARCHAR)")
        con.execute("INSERT INTO meta_database VALUES (?)", [CURRENT_DUCKDB_SCHEMA_VERSION])
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


def _write_viewer_task_results(
    db_path: Path,
    rows: list[tuple],
    *,
    rows_override_languages: list[tuple[str, list[str]]] | None = None,
    schema_version: str = CURRENT_DUCKDB_SCHEMA_VERSION,
) -> None:
    con = duckdb.connect(str(db_path))
    try:
        con.execute("CREATE TABLE meta_database (schema_version VARCHAR)")
        con.execute("INSERT INTO meta_database VALUES (?)", [schema_version])
        columns = (
            "model_name VARCHAR",
            "benchmark VARCHAR",
            "dataset_id VARCHAR",
            "dataset_name VARCHAR",
            "split_name VARCHAR",
            "task_name VARCHAR",
            "task_key VARCHAR",
            "score_target VARCHAR",
            "score DOUBLE",
            "language VARCHAR",
            "languages VARCHAR[]",
            "active_parameters BIGINT",
            "total_parameters BIGINT",
            "max_seq_length INTEGER",
            "dtype VARCHAR",
            "attn_implementation VARCHAR",
            "query_prompt VARCHAR",
            "document_prompt VARCHAR",
            "query_prompt_name VARCHAR",
            "document_prompt_name VARCHAR",
            "query_encode_task VARCHAR",
            "document_encode_task VARCHAR",
            "trust_remote_code BOOLEAN",
            "embedding_variant_name VARCHAR",
            "embedding_dim INTEGER",
            "quantization VARCHAR",
        )
        con.execute(f"CREATE TABLE viewer_task_results ({', '.join(columns)})")
        normalized_rows = []
        for index, row in enumerate(rows):
            language, languages = (
                rows_override_languages[index]
                if rows_override_languages is not None
                else (None, [])
            )
            normalized_rows.append(_viewer_task_result_row(row, language=language, languages=languages))
        placeholders = ", ".join("?" for _ in columns)
        con.executemany(f"INSERT INTO viewer_task_results VALUES ({placeholders})", normalized_rows)
    finally:
        con.close()


def _viewer_task_result_row(row: tuple, *, language: str | None, languages: list[str]) -> tuple:
    base = row[:11]
    remaining = row[11:]
    dtype = None
    attn_implementation = None
    query_prompt = None
    document_prompt = None
    query_prompt_name = None
    document_prompt_name = None
    query_encode_task = None
    document_encode_task = None
    trust_remote_code = None
    embedding_variant_name = None
    embedding_dim = None
    quantization = None
    if len(remaining) == 3:
        embedding_variant_name, embedding_dim, quantization = remaining
    elif len(remaining) == 9:
        (
            dtype,
            attn_implementation,
            query_prompt,
            document_prompt,
            query_prompt_name,
            document_prompt_name,
            query_encode_task,
            document_encode_task,
            trust_remote_code,
        ) = remaining
    elif len(remaining) == 0:
        pass
    else:
        raise AssertionError(f"Unexpected row shape: {row!r}")
    return (
        *base[:7],
        "all",
        base[7],
        language,
        languages,
        *base[8:11],
        dtype,
        attn_implementation,
        query_prompt,
        document_prompt,
        query_prompt_name,
        document_prompt_name,
        query_encode_task,
        document_encode_task,
        trust_remote_code,
        embedding_variant_name,
        embedding_dim,
        quantization,
    )
