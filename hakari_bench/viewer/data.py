from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Iterable, TypeVar

import duckdb
from pydantic import BaseModel, ConfigDict, Field

from hakari_bench.viewer.observability import timed_operation
from hakari_bench.viewer.task_names import (
    canonical_split_name,
    canonical_task_name,
)
from hakari_bench.viewer.variant_display import VariantDisplayFlags


CURRENT_DUCKDB_SCHEMA_VERSION = "4"
REQUIRED_VIEWER_TABLES = ("meta_database", "viewer_task_results")
REQUIRED_VIEWER_TASK_RESULT_COLUMNS = {
    "model_name",
    "benchmark",
    "dataset_id",
    "dataset_name",
    "split_name",
    "task_name",
    "task_key",
    "score_target",
    "score",
    "language",
    "languages",
    "active_parameters",
    "total_parameters",
    "max_seq_length",
}


class TaskResultRecord(BaseModel):
    """Typed DTO for DuckDB `viewer_task_results` rows used by the viewer."""

    model_config = ConfigDict(frozen=True, strict=True, extra="forbid")

    model_name: str
    benchmark: str
    dataset_id: str
    dataset_name: str
    split_name: str
    task_name: str
    task_key: str
    score: float
    language: str | None = None
    languages: list[str] = Field(default_factory=list)
    active_parameters: int | None = None
    total_parameters: int | None = None
    max_seq_length: int | None = None
    dtype: str | None = None
    attn_implementation: str | None = None
    query_prompt: str | None = None
    document_prompt: str | None = None
    query_prompt_name: str | None = None
    document_prompt_name: str | None = None
    query_encode_task: str | None = None
    document_encode_task: str | None = None
    trust_remote_code: bool | None = None
    embedding_variant_name: str | None = None
    embedding_dim: int | None = None
    quantization: str | None = None

    @property
    def prompt_summary(self) -> str:
        has_explicit_prompt = bool(self.query_prompt or self.document_prompt)
        has_prompt_name = bool(self.query_prompt_name or self.document_prompt_name)
        has_encode_task = bool(self.query_encode_task or self.document_encode_task)
        if has_explicit_prompt:
            return "explicit prefixes"
        if has_prompt_name and has_encode_task:
            return "prompt names + encode tasks"
        if has_prompt_name:
            return "prompt names"
        if has_encode_task:
            return "encode tasks"
        return "model default"


@dataclass(frozen=True, slots=True)
class TaskResultRow:
    """Lightweight viewer row for leaderboard hot paths."""

    model_name: str
    benchmark: str
    dataset_id: str
    dataset_name: str
    split_name: str
    task_name: str
    task_key: str
    score: float
    language: str | None = None
    languages: tuple[str, ...] = ()
    active_parameters: int | None = None
    total_parameters: int | None = None
    max_seq_length: int | None = None
    dtype: str | None = None
    attn_implementation: str | None = None
    query_prompt: str | None = None
    document_prompt: str | None = None
    query_prompt_name: str | None = None
    document_prompt_name: str | None = None
    query_encode_task: str | None = None
    document_encode_task: str | None = None
    trust_remote_code: bool | None = None
    embedding_variant_name: str | None = None
    embedding_dim: int | None = None
    quantization: str | None = None

    @property
    def prompt_summary(self) -> str:
        has_explicit_prompt = bool(self.query_prompt or self.document_prompt)
        has_prompt_name = bool(self.query_prompt_name or self.document_prompt_name)
        has_encode_task = bool(self.query_encode_task or self.document_encode_task)
        if has_explicit_prompt:
            return "explicit prefixes"
        if has_prompt_name and has_encode_task:
            return "prompt names + encode tasks"
        if has_prompt_name:
            return "prompt names"
        if has_encode_task:
            return "encode tasks"
        return "model default"


TTaskResultItem = TypeVar("TTaskResultItem", TaskResultRecord, TaskResultRow)


class TaskResultsRepository:
    def __init__(self, duckdb_path: Path) -> None:
        self.duckdb_path = duckdb_path

    def fetch_task_results(
        self,
        *,
        benchmarks: list[str],
        score_target: str = "all",
        include_embedding_variants: bool,
        variant_display_flags: VariantDisplayFlags | None = None,
    ) -> list[TaskResultRecord]:
        """Fetch leaderboard source rows from `viewer_task_results`.

        The viewer ranks task-level aggregate scores, so this query intentionally
        reads only the columns needed to build `TaskScore` objects. It filters out
        NULL scores because they cannot participate in ranking, and it fetches
        only base embedding rows unless the caller explicitly needs variant rows.
        """

        return self._fetch_task_result_items(
            benchmarks=benchmarks,
            score_target=score_target,
            include_embedding_variants=include_embedding_variants,
            variant_display_flags=variant_display_flags,
            item_factory=_task_result_record,
            transform_operation="fetch_task_results.records",
        )

    def fetch_task_result_rows(
        self,
        *,
        benchmarks: list[str],
        score_target: str = "all",
        include_embedding_variants: bool,
        variant_display_flags: VariantDisplayFlags | None = None,
    ) -> list[TaskResultRow]:
        return self._fetch_task_result_items(
            benchmarks=benchmarks,
            score_target=score_target,
            include_embedding_variants=include_embedding_variants,
            variant_display_flags=variant_display_flags,
            item_factory=_task_result_row,
            transform_operation="fetch_task_result_rows.records",
        )

    def _fetch_task_result_items(
        self,
        *,
        benchmarks: list[str],
        score_target: str,
        include_embedding_variants: bool,
        variant_display_flags: VariantDisplayFlags | None,
        item_factory: Callable[[list[str], tuple[Any, ...]], TTaskResultItem],
        transform_operation: str,
    ) -> list[TTaskResultItem]:
        if not self.duckdb_path.exists() or not benchmarks:
            return []
        with timed_operation("viewer.duckdb.connection", operation="fetch_task_results"):
            con = duckdb.connect(str(self.duckdb_path), read_only=True)
        try:
            with timed_operation("viewer.duckdb.schema", operation="fetch_task_results"):
                _validate_current_schema(con)
                columns = _table_columns(con, "viewer_task_results")
                missing_columns = REQUIRED_VIEWER_TASK_RESULT_COLUMNS - columns
                if missing_columns:
                    raise RuntimeError(
                        "DuckDB viewer_task_results is missing required columns: "
                        + ", ".join(sorted(missing_columns))
                    )
            score_expr = "tr.score"
            target_filter = "AND tr.score_target = ?"
            query_params: list[Any] = list(benchmarks)
            query_params.append(score_target)
            language_expr = "tr.language"
            languages_expr = "tr.languages"
            variant_name_expr = _column_or_null(columns, "embedding_variant_name")
            embedding_dim_expr = _column_or_null(columns, "embedding_dim")
            quantization_expr = _column_or_null(columns, "quantization")
            dtype_expr = _column_or_null(columns, "dtype")
            attn_expr = _column_or_null(columns, "attn_implementation")
            query_prompt_expr = _column_or_null(columns, "query_prompt")
            document_prompt_expr = _column_or_null(columns, "document_prompt")
            query_prompt_name_expr = _column_or_null(columns, "query_prompt_name")
            document_prompt_name_expr = _column_or_null(columns, "document_prompt_name")
            query_encode_task_expr = _column_or_null(columns, "query_encode_task")
            document_encode_task_expr = _column_or_null(columns, "document_encode_task")
            trust_remote_code_expr = _column_or_null(columns, "trust_remote_code")
            variant_filter = ""
            if "embedding_variant_name" in columns and (score_target == "reranking" or not include_embedding_variants):
                variant_filter = "AND tr.embedding_variant_name IS NULL"
            elif "embedding_variant_name" in columns and variant_display_flags is not None:
                variant_filter = _variant_filter_sql(columns, variant_display_flags)
            placeholders = ", ".join("?" for _ in benchmarks)
            query = f"""
                SELECT
                    tr.model_name,
                    tr.benchmark,
                    tr.dataset_id,
                    tr.dataset_name,
                    COALESCE(tr.split_name, '') AS split_name,
                    tr.task_name,
                    tr.task_key,
                    {score_expr} AS score,
                    {language_expr} AS language,
                    {languages_expr} AS languages,
                    tr.active_parameters,
                    tr.total_parameters,
                    tr.max_seq_length,
                    {dtype_expr} AS dtype,
                    {attn_expr} AS attn_implementation,
                    {query_prompt_expr} AS query_prompt,
                    {document_prompt_expr} AS document_prompt,
                    {query_prompt_name_expr} AS query_prompt_name,
                    {document_prompt_name_expr} AS document_prompt_name,
                    {query_encode_task_expr} AS query_encode_task,
                    {document_encode_task_expr} AS document_encode_task,
                    {trust_remote_code_expr} AS trust_remote_code,
                    {variant_name_expr} AS embedding_variant_name,
                    {embedding_dim_expr} AS embedding_dim,
                    {quantization_expr} AS quantization
                FROM viewer_task_results AS tr
                WHERE tr.benchmark IN ({placeholders})
                  AND {score_expr} IS NOT NULL
                  {variant_filter}
                  {target_filter}
            """
            with timed_operation(
                "viewer.duckdb.query",
                operation="fetch_task_results",
                benchmark_count=len(benchmarks),
                include_embedding_variants=include_embedding_variants,
                score_target=score_target,
                variant_flags=_variant_flags_label(variant_display_flags),
            ) as timing:
                cursor = con.execute(query, query_params)
                field_names = [str(description[0]) for description in cursor.description]
                rows = cursor.fetchall()
                timing["row_count"] = len(rows)
            with timed_operation(
                "viewer.transform",
                operation=transform_operation,
                row_count=len(rows),
            ) as timing:
                records = _dedupe_task_result_records(item_factory(field_names, row) for row in rows)
                timing["deduped_row_count"] = len(records)
                return records
        finally:
            with timed_operation("viewer.duckdb.connection_close", operation="fetch_task_results"):
                con.close()


def _task_result_payload(field_names: list[str], row: tuple[Any, ...]) -> dict[str, Any]:
    payload = dict(zip(field_names, row, strict=True))
    benchmark = str(payload["benchmark"])
    raw_task_name = str(payload["task_name"])
    task_name = canonical_task_name(benchmark, raw_task_name)
    payload["split_name"] = canonical_split_name(benchmark, payload.get("split_name"))
    payload["task_name"] = task_name
    payload["languages"] = _normalized_languages(payload.get("languages"), payload.get("language"))
    return payload


def _task_result_record(field_names: list[str], row: tuple[Any, ...]) -> TaskResultRecord:
    payload = _task_result_payload(field_names, row)
    return TaskResultRecord.model_validate(payload)


def _task_result_row(field_names: list[str], row: tuple[Any, ...]) -> TaskResultRow:
    payload = _task_result_payload(field_names, row)
    return TaskResultRow(
        model_name=str(payload["model_name"]),
        benchmark=str(payload["benchmark"]),
        dataset_id=str(payload["dataset_id"]),
        dataset_name=str(payload["dataset_name"]),
        split_name=str(payload["split_name"]),
        task_name=str(payload["task_name"]),
        task_key=str(payload["task_key"]),
        score=float(payload["score"]),
        language=payload["language"] if isinstance(payload["language"], str) else None,
        languages=tuple(payload["languages"]),
        active_parameters=_int_payload_value(payload.get("active_parameters")),
        total_parameters=_int_payload_value(payload.get("total_parameters")),
        max_seq_length=_int_payload_value(payload.get("max_seq_length")),
        dtype=payload["dtype"] if isinstance(payload["dtype"], str) else None,
        attn_implementation=payload["attn_implementation"] if isinstance(payload["attn_implementation"], str) else None,
        query_prompt=payload["query_prompt"] if isinstance(payload["query_prompt"], str) else None,
        document_prompt=payload["document_prompt"] if isinstance(payload["document_prompt"], str) else None,
        query_prompt_name=payload["query_prompt_name"] if isinstance(payload["query_prompt_name"], str) else None,
        document_prompt_name=payload["document_prompt_name"] if isinstance(payload["document_prompt_name"], str) else None,
        query_encode_task=payload["query_encode_task"] if isinstance(payload["query_encode_task"], str) else None,
        document_encode_task=payload["document_encode_task"] if isinstance(payload["document_encode_task"], str) else None,
        trust_remote_code=payload["trust_remote_code"] if isinstance(payload["trust_remote_code"], bool) else None,
        embedding_variant_name=payload["embedding_variant_name"] if isinstance(payload["embedding_variant_name"], str) else None,
        embedding_dim=_int_payload_value(payload.get("embedding_dim")),
        quantization=payload["quantization"] if isinstance(payload["quantization"], str) else None,
    )


def _dedupe_task_result_records(records: Iterable[TTaskResultItem]) -> list[TTaskResultItem]:
    deduped: dict[tuple[str, str, str, str | None, int | None, str | None], TTaskResultItem] = {}
    for record in records:
        key = (
            record.model_name,
            record.benchmark,
            record.task_key,
            record.embedding_variant_name,
            record.embedding_dim,
            record.quantization,
        )
        current = deduped.get(key)
        if current is None:
            deduped[key] = record
    return list(deduped.values())


def _int_payload_value(value: Any) -> int | None:
    return int(value) if isinstance(value, int) else None


def _variant_filter_sql(columns: set[str], flags: VariantDisplayFlags) -> str:
    if not flags.any_enabled:
        return "AND tr.embedding_variant_name IS NULL"
    if flags == VariantDisplayFlags(quantization=True, truncate=True, rescore=True, other=True):
        return ""

    name = "lower(tr.embedding_variant_name)"
    quantization_category = f"({_column_or_null(columns, 'quantization')} IS NOT NULL OR {name} LIKE '%quantize%')"
    truncate_category = f"({name} LIKE '%truncate%')"
    rescore_category = f"({name} LIKE '%rescore%')"
    non_rescore = f"NOT {rescore_category}"
    clauses = ["tr.embedding_variant_name IS NULL"]
    if flags.rescore:
        clauses.append(rescore_category)
    quantize_or_truncate_clause = _quantize_or_truncate_variant_filter(
        flags=flags,
        quantization_category=quantization_category,
        truncate_category=truncate_category,
    )
    if quantize_or_truncate_clause:
        clauses.append(f"({non_rescore} AND {quantize_or_truncate_clause})")
    if flags.other:
        clauses.append(f"({non_rescore} AND NOT {quantization_category} AND NOT {truncate_category})")
    return "AND (" + " OR ".join(clauses) + ")"


def _quantize_or_truncate_variant_filter(
    *,
    flags: VariantDisplayFlags,
    quantization_category: str,
    truncate_category: str,
) -> str:
    if flags.quantization and flags.truncate:
        return f"({quantization_category} OR {truncate_category})"
    if flags.quantization:
        return f"({quantization_category} AND NOT {truncate_category})"
    if flags.truncate:
        return f"({truncate_category} AND NOT {quantization_category})"
    return ""


def _variant_flags_label(flags: VariantDisplayFlags | None) -> str:
    if flags is None:
        return "default"
    enabled = [
        name
        for name, is_enabled in (
            ("quantization", flags.quantization),
            ("truncate", flags.truncate),
            ("rescore", flags.rescore),
            ("other", flags.other),
        )
        if is_enabled
    ]
    return ",".join(enabled) if enabled else "base"


def _table_columns(con: duckdb.DuckDBPyConnection, table: str) -> set[str]:
    return {str(row[0]) for row in con.execute(f"DESCRIBE {table}").fetchall()}


def _table_exists(con: duckdb.DuckDBPyConnection, table: str) -> bool:
    row = con.execute(
        "SELECT count(*) FROM information_schema.tables WHERE table_name = ?",
        [table],
    )
    count = row.fetchone()
    return bool(count[0]) if count is not None else False


def _validate_current_schema(con: duckdb.DuckDBPyConnection) -> None:
    missing_tables = [table for table in REQUIRED_VIEWER_TABLES if not _table_exists(con, table)]
    if missing_tables:
        raise RuntimeError(
            "DuckDB file uses an unsupported schema; missing required current-schema tables: "
            + ", ".join(missing_tables)
        )
    row = con.execute("SELECT schema_version FROM meta_database LIMIT 1").fetchone()
    schema_version = str(row[0]) if row is not None and row[0] is not None else ""
    if schema_version != CURRENT_DUCKDB_SCHEMA_VERSION:
        raise RuntimeError(
            f"DuckDB schema version {schema_version or '<missing>'} is unsupported; "
            f"rebuild the database with schema version {CURRENT_DUCKDB_SCHEMA_VERSION}."
        )


def _column_or_null(columns: set[str], column: str) -> str:
    return f"tr.{column}" if column in columns else "NULL"


def _normalized_languages(value: Any, language: Any) -> list[str]:
    if isinstance(value, list):
        languages = [item for item in value if isinstance(item, str) and item]
        if languages:
            return languages
    if isinstance(language, str) and language:
        return [language]
    return []
