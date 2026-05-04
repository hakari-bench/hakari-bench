from __future__ import annotations

from pathlib import Path
from typing import Any, Iterable

import duckdb
from pydantic import BaseModel, ConfigDict

from hakari_bench.viewer.task_names import (
    canonical_split_name,
    canonical_task_key,
    canonical_task_name,
    is_legacy_task_alias,
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
    active_parameters: int | None = None
    total_parameters: int | None = None
    max_seq_length: int | None = None
    embedding_variant_name: str | None = None
    embedding_dim: int | None = None
    quantization: str | None = None
    uses_legacy_task_alias: bool = False


class TaskResultsRepository:
    def __init__(self, duckdb_path: Path) -> None:
        self.duckdb_path = duckdb_path

    def fetch_task_results(
        self,
        *,
        benchmarks: list[str],
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
            variant_name_expr = _column_or_null(columns, "embedding_variant_name")
            embedding_dim_expr = _column_or_null(columns, "embedding_dim")
            quantization_expr = _column_or_null(columns, "quantization")
            variant_filter = (
                ""
                if include_embedding_variants or "embedding_variant_name" not in columns
                else "AND embedding_variant_name IS NULL"
            )
            placeholders = ", ".join("?" for _ in benchmarks)
            query = f"""
                SELECT
                    model_name,
                    benchmark,
                    dataset_id,
                    dataset_name,
                    COALESCE(split_name, '') AS split_name,
                    task_name,
                    task_key,
                    score,
                    active_parameters,
                    total_parameters,
                    max_seq_length,
                    {variant_name_expr} AS embedding_variant_name,
                    {embedding_dim_expr} AS embedding_dim,
                    {quantization_expr} AS quantization
                FROM task_results
                WHERE benchmark IN ({placeholders})
                  AND score IS NOT NULL
                  {variant_filter}
                ORDER BY benchmark, dataset_id, task_name, model_name, embedding_variant_name IS NOT NULL, embedding_variant_name
            """
            cursor = con.execute(query, benchmarks)
            field_names = [str(description[0]) for description in cursor.description]
            return _dedupe_task_result_records(_task_result_record(field_names, row) for row in cursor.fetchall())
        finally:
            con.close()


def _task_result_record(field_names: list[str], row: tuple[Any, ...]) -> TaskResultRecord:
    payload = dict(zip(field_names, row, strict=True))
    benchmark = str(payload["benchmark"])
    dataset_id = str(payload["dataset_id"])
    raw_task_name = str(payload["task_name"])
    task_name = canonical_task_name(benchmark, raw_task_name)
    uses_legacy_task_alias = is_legacy_task_alias(benchmark, raw_task_name)
    payload["split_name"] = canonical_split_name(benchmark, payload.get("split_name"))
    payload["task_name"] = task_name
    payload["uses_legacy_task_alias"] = uses_legacy_task_alias
    if uses_legacy_task_alias:
        payload["task_key"] = canonical_task_key(benchmark=benchmark, dataset_id=dataset_id, task_name=task_name)
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
        if current is None or (current.uses_legacy_task_alias and not record.uses_legacy_task_alias):
            deduped[key] = record
    return list(deduped.values())


def _table_columns(con: duckdb.DuckDBPyConnection, table: str) -> set[str]:
    return {str(row[0]) for row in con.execute(f"DESCRIBE {table}").fetchall()}


def _column_or_null(columns: set[str], column: str) -> str:
    return column if column in columns else "NULL"
