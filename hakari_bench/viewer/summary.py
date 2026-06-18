from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any

import duckdb

from hakari_bench.viewer.observability import timed_operation
from hakari_bench.viewer.sql import table_columns, table_exists


SUMMARY_QUERY_TABLES = {"meta_database", "viewer_task_results"}


@dataclass(frozen=True)
class ViewerSummary:
    model_count: int = 0
    benchmark_count: int = 0
    task_count: int = 0
    language_count: int = 0
    base_result_count: int = 0
    variant_result_count: int = 0
    latest_finished_at_utc: str | None = None


class ViewerSummaryRepository:
    def __init__(self, duckdb_path: Path) -> None:
        self.duckdb_path = duckdb_path

    def fetch_summary(self) -> ViewerSummary:
        if not self.duckdb_path.exists():
            return ViewerSummary()
        with timed_operation("viewer.duckdb.connection", operation="fetch_summary"):
            con = duckdb.connect(str(self.duckdb_path), read_only=True)
        try:
            if not _table_exists(con, "viewer_task_results"):
                return ViewerSummary()
            columns = _table_columns(con, "viewer_task_results")
            if not {"model_name", "benchmark", "task_key", "score_target"}.issubset(
                columns
            ):
                return ViewerSummary()
            variant_column = (
                "embedding_variant_name"
                if "embedding_variant_name" in columns
                else None
            )
            base_count_expr = (
                "count(*) FILTER (WHERE embedding_variant_name IS NULL)"
                if variant_column is not None
                else "count(*)"
            )
            variant_count_expr = (
                "count(*) FILTER (WHERE embedding_variant_name IS NOT NULL)"
                if variant_column is not None
                else "0"
            )
            with timed_operation(
                "viewer.duckdb.query", operation="fetch_summary.counts"
            ) as timing:
                count_row = con.execute(
                    f"""
                    SELECT
                        count(DISTINCT model_name),
                        count(DISTINCT benchmark),
                        count(DISTINCT task_key),
                        {base_count_expr},
                        {variant_count_expr}
                    FROM viewer_task_results
                    WHERE score_target = 'all'
                    """  # nosec B608
                ).fetchone()
                timing["row_count"] = 1 if count_row is not None else 0
            with timed_operation(
                "viewer.duckdb.query", operation="fetch_summary.languages"
            ) as timing:
                language_count = _fetch_language_count(con, columns)
                timing["row_count"] = 1
            return ViewerSummary(
                model_count=_int_value(count_row, 0),
                benchmark_count=_int_value(count_row, 1),
                task_count=_int_value(count_row, 2),
                language_count=language_count,
                base_result_count=_int_value(count_row, 3),
                variant_result_count=_int_value(count_row, 4),
                latest_finished_at_utc=_fetch_built_at_utc(con),
            )
        finally:
            with timed_operation(
                "viewer.duckdb.connection_close", operation="fetch_summary"
            ):
                con.close()


def _fetch_language_count(con: duckdb.DuckDBPyConnection, columns: set[str]) -> int:
    if "languages" in columns:
        row = con.execute(
            """
            SELECT count(DISTINCT item.language)
            FROM viewer_task_results, unnest(languages) AS item(language)
            WHERE score_target = 'all'
              AND item.language IS NOT NULL
              AND item.language != ''
            """
        ).fetchone()
        return int(row[0] or 0) if row is not None else 0
    if "language" in columns:
        row = con.execute(
            """
            SELECT count(DISTINCT language)
            FROM viewer_task_results
            WHERE score_target = 'all'
              AND language IS NOT NULL
              AND language != ''
            """
        ).fetchone()
        return int(row[0] or 0) if row is not None else 0
    return 0


def _fetch_built_at_utc(con: duckdb.DuckDBPyConnection) -> str | None:
    if not _table_exists(con, "meta_database"):
        return None
    columns = _table_columns(con, "meta_database")
    if "built_at_utc" not in columns:
        return None
    row = con.execute("SELECT max(built_at_utc) FROM meta_database").fetchone()
    value = row[0] if row is not None else None
    return str(value) if value else None


def _int_value(row: tuple[Any, ...] | None, index: int) -> int:
    if row is None:
        return 0
    return int(row[index] or 0)


def _table_columns(con: duckdb.DuckDBPyConnection, table: str) -> set[str]:
    return table_columns(con, table, allowed_tables=SUMMARY_QUERY_TABLES)


def _table_exists(con: duckdb.DuckDBPyConnection, table: str) -> bool:
    return table_exists(con, table, allowed_tables=SUMMARY_QUERY_TABLES)
