from __future__ import annotations

from pathlib import Path
from typing import Any, Iterable

import duckdb
from pydantic import BaseModel, ConfigDict, Field

from hakari_bench.viewer.task_names import (
    canonical_split_name,
    canonical_task_name,
)


class TaskResultRecord(BaseModel):
    """Typed DTO for the DuckDB `task_results` rows used by the viewer."""

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


class TaskResultsRepository:
    def __init__(self, duckdb_path: Path) -> None:
        self.duckdb_path = duckdb_path

    def fetch_task_results(
        self,
        *,
        benchmarks: list[str],
        score_target: str = "all",
        include_embedding_variants: bool,
    ) -> list[TaskResultRecord]:
        """Fetch leaderboard source rows from the canonical `task_results` table.

        The viewer ranks task-level aggregate scores, so this query intentionally
        reads only the columns needed to build `TaskScore` objects. It filters out
        NULL scores because they cannot participate in ranking, and it fetches
        only base embedding rows unless the caller explicitly needs variant rows.
        Older DuckDB files may not have variant columns, so those fields are
        selected as NULL when absent.
        """

        if not self.duckdb_path.exists() or not benchmarks:
            return []
        con = duckdb.connect(str(self.duckdb_path), read_only=True)
        try:
            columns = _table_columns(con, "task_results")
            metadata_columns = _table_columns(con, "dataset_metadata") if _table_exists(con, "dataset_metadata") else set()
            diagnostic_columns = _table_columns(con, "task_diagnostics") if _table_exists(con, "task_diagnostics") else set()
            metadata_join = "LEFT JOIN dataset_metadata AS dm ON dm.task_key = tr.task_key" if metadata_columns else ""
            diagnostic_join = ""
            score_expr = "tr.score"
            target_filter = ""
            if score_target == "reranking" and {"model_name", "benchmark", "task_key", "rerank_score"}.issubset(diagnostic_columns):
                diagnostic_join = """
                    JOIN task_diagnostics AS td
                      ON td.model_name = tr.model_name
                     AND td.benchmark = tr.benchmark
                     AND td.task_key = tr.task_key
                """
                score_expr = "td.rerank_score"
                target_filter = """
                  AND td.rerank_score IS NOT NULL
                  AND (td.rerank_status IS NULL OR td.rerank_status = 'available')
                  AND (td.candidate_ranking IS NULL OR td.candidate_ranking = 'bm25')
                  AND (td.rerank_top_k IS NULL OR td.rerank_top_k = 100)
                """
            elif score_target == "reranking":
                return []
            language_expr = "dm.language" if "language" in metadata_columns else "NULL"
            languages_expr = "dm.languages" if "languages" in metadata_columns else "NULL"
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
            variant_order = (
                ", tr.embedding_variant_name IS NOT NULL, tr.embedding_variant_name"
                if "embedding_variant_name" in columns
                else ""
            )
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
                FROM task_results AS tr
                {metadata_join}
                {diagnostic_join}
                WHERE tr.benchmark IN ({placeholders})
                  AND {score_expr} IS NOT NULL
                  {variant_filter}
                  {target_filter}
                ORDER BY tr.benchmark, tr.dataset_id, tr.task_name, tr.model_name{variant_order}
            """
            cursor = con.execute(query, benchmarks)
            field_names = [str(description[0]) for description in cursor.description]
            return _dedupe_task_result_records(_task_result_record(field_names, row) for row in cursor.fetchall())
        finally:
            con.close()


def _task_result_record(field_names: list[str], row: tuple[Any, ...]) -> TaskResultRecord:
    payload = dict(zip(field_names, row, strict=True))
    benchmark = str(payload["benchmark"])
    raw_task_name = str(payload["task_name"])
    task_name = canonical_task_name(benchmark, raw_task_name)
    payload["split_name"] = canonical_split_name(benchmark, payload.get("split_name"))
    payload["task_name"] = task_name
    payload["languages"] = _normalized_languages(payload.get("languages"), payload.get("language"))
    return TaskResultRecord.model_validate(payload)


def _dedupe_task_result_records(records: Iterable[TaskResultRecord]) -> list[TaskResultRecord]:
    deduped: dict[tuple[str, str, str, str | None, int | None, str | None], TaskResultRecord] = {}
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


def _table_columns(con: duckdb.DuckDBPyConnection, table: str) -> set[str]:
    return {str(row[0]) for row in con.execute(f"DESCRIBE {table}").fetchall()}


def _table_exists(con: duckdb.DuckDBPyConnection, table: str) -> bool:
    row = con.execute(
        "SELECT count(*) FROM information_schema.tables WHERE table_name = ?",
        [table],
    )
    count = row.fetchone()
    return bool(count[0]) if count is not None else False


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
