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


def test_task_results_repository_rejects_schema_three_without_text_length_columns(tmp_path: Path) -> None:
    db_path = tmp_path / "results.duckdb"
    _write_viewer_task_results(
        db_path,
        [
            ("model/a", "BenchA", "bench/a", "BenchA", None, "a1", "a1", 0.90, 10, 12, 8192),
        ],
        schema_version="3",
        include_text_length_columns=False,
    )

    with pytest.raises(RuntimeError, match="schema version 3 is unsupported"):
        TaskResultsRepository(db_path).fetch_task_result_rows(
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


def test_task_results_repository_can_fetch_non_default_metric_scores(tmp_path: Path) -> None:
    db_path = tmp_path / "results.duckdb"
    _write_viewer_task_results(
        db_path,
        [
            ("model/a", "BenchA", "bench/a", "BenchA", None, "a1", "a1", 0.90, 10, 12, 8192),
            ("model/b", "BenchA", "bench/a", "BenchA", None, "a1", "a1", 0.80, 20, 24, 8192),
        ],
    )
    _write_metric_tables(
        db_path,
        [
            ("model/a", "BenchA", "bench/a", "a1", "a1", "BenchA_a1_cosine_acc@1", 0.20, "a.json"),
            ("model/b", "BenchA", "bench/a", "a1", "a1", "BenchA_a1_cosine_acc@1", 0.95, "b.json"),
        ],
    )

    rows = TaskResultsRepository(db_path).fetch_task_result_rows(
        benchmarks=["BenchA"],
        include_embedding_variants=False,
        score_metric="acc@1",
    )

    assert [(row.model_name, row.score) for row in rows] == [("model/a", 0.20), ("model/b", 0.95)]


def test_task_results_repository_limits_display_metric_options_to_research_focused_set(tmp_path: Path) -> None:
    db_path = tmp_path / "results.duckdb"
    _write_viewer_task_results(
        db_path,
        [
            ("model/a", "BenchA", "bench/a", "BenchA", None, "a1", "a1", 0.90, 10, 12, 8192),
        ],
    )
    _write_metric_tables(
        db_path,
        [
            ("model/a", "BenchA", "bench/a", "a1", "a1", "BenchA_a1_cosine_acc@1", 0.20, "a.json"),
            ("model/a", "BenchA", "bench/a", "a1", "a1", "BenchA_a1_cosine_acc@3", 0.30, "a.json"),
            ("model/a", "BenchA", "bench/a", "a1", "a1", "BenchA_a1_cosine_acc@5", 0.40, "a.json"),
            ("model/a", "BenchA", "bench/a", "a1", "a1", "BenchA_a1_cosine_acc@10", 0.50, "a.json"),
            ("model/a", "BenchA", "bench/a", "a1", "a1", "BenchA_a1_cosine_acc@100", 0.90, "a.json"),
            ("model/a", "BenchA", "bench/a", "a1", "a1", "BenchA_a1_cosine_precision@1", 0.20, "a.json"),
            ("model/a", "BenchA", "bench/a", "a1", "a1", "BenchA_a1_cosine_precision@10", 0.50, "a.json"),
            ("model/a", "BenchA", "bench/a", "a1", "a1", "BenchA_a1_cosine_recall@1", 0.20, "a.json"),
            ("model/a", "BenchA", "bench/a", "a1", "a1", "BenchA_a1_cosine_recall@10", 0.50, "a.json"),
            ("model/a", "BenchA", "bench/a", "a1", "a1", "BenchA_a1_cosine_mrr@10", 0.70, "a.json"),
            ("model/a", "BenchA", "bench/a", "a1", "a1", "BenchA_a1_cosine_map@100", 0.80, "a.json"),
        ],
    )

    assert TaskResultsRepository(db_path).fetch_score_metric_options() == [
        "ndcg@10",
        "acc@1",
        "acc@10",
        "acc@100",
        "precision@10",
        "recall@10",
        "mrr@10",
        "map@100",
    ]


def test_task_results_repository_uses_rerank_metrics_for_reranking_target(tmp_path: Path) -> None:
    db_path = tmp_path / "results.duckdb"
    _write_viewer_task_results(
        db_path,
        [
            ("cross-encoder/reranker", "BenchA", "bench/a", "BenchA", None, "a1", "a1", 0.90, 10, 12, 8192),
        ],
    )
    _write_metric_tables(
        db_path,
        [
            ("cross-encoder/reranker", "BenchA", "bench/a", "a1", "a1", "BenchA_a1_cosine_acc@1", 0.20, "r.json"),
            (
                "cross-encoder/reranker",
                "BenchA",
                "bench/a",
                "a1",
                "a1",
                "BenchA_a1_cosine_reranking_hybrid_top12_rerank_acc@1",
                0.85,
                "r.json",
            ),
        ],
        score_target="reranking",
    )

    rows = TaskResultsRepository(db_path).fetch_task_result_rows(
        benchmarks=["BenchA"],
        include_embedding_variants=False,
        score_target="reranking",
        score_metric="acc@1",
    )

    assert [(row.model_name, row.score) for row in rows] == [("cross-encoder/reranker", 0.85)]


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
    truncate_records = TaskResultsRepository(db_path).fetch_task_results(
        benchmarks=["BenchA"],
        include_embedding_variants=True,
        variant_display_flags=VariantDisplayFlags(truncate=True),
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
        ("truncate_dim_256_quantize_int8_docs", "int8"),
    ]
    assert [(record.embedding_variant_name, record.quantization) for record in truncate_records] == [
        (None, None),
        ("truncate_dim_384", None),
        ("truncate_dim_256_quantize_int8_docs", "int8"),
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


def test_task_results_repository_reads_optional_model_type_column(tmp_path: Path) -> None:
    db_path = tmp_path / "results.duckdb"
    _write_viewer_task_results(
        db_path,
        [
            ("model/sparse", "BenchA", "bench/a", "BenchA", None, "a1", "task-ja", 0.90, 10, 12, 8192),
        ],
        include_model_type_column=True,
        row_model_types=["sparse"],
    )

    records = TaskResultsRepository(db_path).fetch_task_result_rows(
        benchmarks=["BenchA"],
        include_embedding_variants=False,
    )

    assert [(record.model_name, record.model_type) for record in records] == [("model/sparse", "sparse")]


def test_task_results_repository_reads_task_text_length_metadata(tmp_path: Path) -> None:
    db_path = tmp_path / "results.duckdb"
    _write_viewer_task_results(
        db_path,
        [
            ("model/a", "BenchA", "bench/a", "BenchA", None, "a1", "task-ja", 0.90, 10, 12, 8192),
        ],
        rows_override_text_lengths=[(512.5, 1536.0)],
    )

    records = TaskResultsRepository(db_path).fetch_task_result_rows(
        benchmarks=["BenchA"],
        include_embedding_variants=False,
    )

    assert records[0].query_mean_chars == pytest.approx(512.5)
    assert records[0].document_mean_chars == pytest.approx(1536.0)


def test_task_results_repository_falls_back_to_dataset_metadata_for_text_lengths(tmp_path: Path) -> None:
    db_path = tmp_path / "results.duckdb"
    con = duckdb.connect(str(db_path))
    try:
        con.execute("CREATE TABLE meta_database (schema_version VARCHAR)")
        con.execute("INSERT INTO meta_database VALUES (?)", [CURRENT_DUCKDB_SCHEMA_VERSION])
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
        )
        con.execute(f"CREATE TABLE viewer_task_results ({', '.join(columns)})")
        con.execute(
            f"INSERT INTO viewer_task_results VALUES ({', '.join('?' for _ in columns)})",
            ("model/a", "BenchA", "bench/a", "BenchA", "", "a1", "task-ja", "all", 0.90, "ja", ["ja"], 10, 12, 8192),
        )
        con.execute(
            """
            CREATE TABLE dataset_metadata (
                benchmark VARCHAR,
                dataset_id VARCHAR,
                task_key VARCHAR,
                query_mean_chars DOUBLE,
                document_mean_chars DOUBLE
            )
            """
        )
        con.execute("INSERT INTO dataset_metadata VALUES (?, ?, ?, ?, ?)", ("BenchA", "bench/a", "task-ja", 640.0, 2048.0))
    finally:
        con.close()

    records = TaskResultsRepository(db_path).fetch_task_result_rows(
        benchmarks=["BenchA"],
        include_embedding_variants=False,
    )

    assert records[0].query_mean_chars == pytest.approx(640.0)
    assert records[0].document_mean_chars == pytest.approx(2048.0)


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
    rows_override_text_lengths: list[tuple[float | None, float | None]] | None = None,
    schema_version: str = CURRENT_DUCKDB_SCHEMA_VERSION,
    include_text_length_columns: bool = True,
    include_model_type_column: bool = False,
    row_model_types: list[str | None] | None = None,
) -> None:
    con = duckdb.connect(str(db_path))
    try:
        con.execute("CREATE TABLE meta_database (schema_version VARCHAR)")
        con.execute("INSERT INTO meta_database VALUES (?)", [schema_version])
        columns = [
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
        ]
        if include_model_type_column:
            columns.insert(1, "model_type VARCHAR")
        if include_text_length_columns:
            columns.extend(
                [
                    "query_mean_chars DOUBLE",
                    "document_mean_chars DOUBLE",
                ]
            )
        con.execute(f"CREATE TABLE viewer_task_results ({', '.join(columns)})")
        normalized_rows = []
        for index, row in enumerate(rows):
            language, languages = (
                rows_override_languages[index]
                if rows_override_languages is not None
                else (None, [])
            )
            query_mean_chars, document_mean_chars = (
                rows_override_text_lengths[index]
                if rows_override_text_lengths is not None
                else (None, None)
            )
            normalized_row = _viewer_task_result_row(
                row,
                language=language,
                languages=languages,
                query_mean_chars=query_mean_chars,
                document_mean_chars=document_mean_chars,
            )
            if not include_text_length_columns:
                normalized_row = normalized_row[:-2]
            if include_model_type_column:
                model_type = row_model_types[index] if row_model_types is not None else None
                normalized_row = (normalized_row[0], model_type, *normalized_row[1:])
            normalized_rows.append(normalized_row)
        placeholders = ", ".join("?" for _ in columns)
        con.executemany(f"INSERT INTO viewer_task_results VALUES ({placeholders})", normalized_rows)
    finally:
        con.close()


def _write_metric_tables(db_path: Path, rows: list[tuple], *, score_target: str = "all") -> None:
    con = duckdb.connect(str(db_path))
    try:
        con.execute(
            """
            CREATE TABLE dim_metric (
                metric_id BIGINT,
                metric_name VARCHAR,
                metric_family VARCHAR,
                cutoff INTEGER
            )
            """
        )
        metric_names = sorted({row[5] for row in rows})
        for metric_id, metric_name in enumerate(metric_names, start=1):
            family, cutoff = metric_name.rsplit("@", 1)
            family = family.rsplit("_", 1)[-1]
            con.execute(
                "INSERT INTO dim_metric VALUES (?, ?, ?, ?)",
                [metric_id, metric_name, family, int(cutoff)],
            )
        con.execute(
            """
            CREATE TABLE fact_metric_score (
                metric_id BIGINT,
                model_dir VARCHAR,
                model_name VARCHAR,
                benchmark VARCHAR,
                dataset_id VARCHAR,
                task_name VARCHAR,
                metric_value DOUBLE,
                result_path VARCHAR,
                score_target VARCHAR,
                embedding_variant_name VARCHAR
            )
            """
        )
        con.execute(
            """
            CREATE TABLE fact_task_score (
                model_dir VARCHAR,
                model_name VARCHAR,
                benchmark VARCHAR,
                dataset_id VARCHAR,
                dataset_name VARCHAR,
                split_name VARCHAR,
                task_name VARCHAR,
                task_key VARCHAR,
                score_target VARCHAR,
                score DOUBLE,
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
                quantization VARCHAR,
                result_path VARCHAR
            )
            """
        )
        metric_id_by_name = {name: index for index, name in enumerate(metric_names, start=1)}
        for model_name, benchmark, dataset_id, task_name, task_key, metric_name, metric_value, result_path in rows:
            con.execute(
                "INSERT INTO fact_metric_score VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
                [
                    metric_id_by_name[metric_name],
                    model_name.replace("/", "__"),
                    model_name,
                    benchmark,
                    dataset_id,
                    task_name,
                    metric_value,
                    result_path,
                    score_target,
                    None,
                ],
            )
            con.execute(
                "INSERT INTO fact_task_score VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
                [
                    model_name.replace("/", "__"),
                    model_name,
                    benchmark,
                    dataset_id,
                    benchmark,
                    "",
                    task_name,
                    task_key,
                    score_target,
                    0.0,
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
                    None,
                    None,
                    result_path,
                ],
            )
    finally:
        con.close()


def _viewer_task_result_row(
    row: tuple,
    *,
    language: str | None,
    languages: list[str],
    query_mean_chars: float | None = None,
    document_mean_chars: float | None = None,
) -> tuple:
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
        query_mean_chars,
        document_mean_chars,
    )
