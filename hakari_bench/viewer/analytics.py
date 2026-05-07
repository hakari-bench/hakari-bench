from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any

import duckdb


@dataclass(frozen=True)
class ViewerSummary:
    model_count: int = 0
    benchmark_count: int = 0
    task_count: int = 0
    language_count: int = 0
    base_result_count: int = 0
    variant_result_count: int = 0
    latest_finished_at_utc: str | None = None


@dataclass(frozen=True)
class VariantAnalysisRow:
    model_name: str
    variant_name: str
    embedding_dim: int | None
    quantization: str | None
    task_count: int
    mean_score_100: float
    base_delta_percent: float | None


@dataclass(frozen=True)
class RerankDiagnosticRow:
    benchmark: str
    task_count: int
    query_coverage_percent: float | None
    relevant_coverage_percent: float | None
    mean_lift_points: float | None
    rerank_top_k: int | None
    candidate_source: str | None
    candidate_ranking: str | None
    bm25_source: str | None


@dataclass(frozen=True)
class DatasetDiagnosticRow:
    benchmark: str
    task_count: int
    language_count: int
    category_count: int
    base_rows: int
    saturated_rows: int
    saturation_percent: float | None
    mean_query_count: float | None
    mean_document_count: float | None
    mean_query_chars: float | None
    mean_document_chars: float | None


class ViewerAnalyticsRepository:
    def __init__(self, duckdb_path: Path) -> None:
        self.duckdb_path = duckdb_path

    def fetch_summary(self) -> ViewerSummary:
        if not self.duckdb_path.exists():
            return ViewerSummary()
        con = duckdb.connect(str(self.duckdb_path), read_only=True)
        try:
            if not _table_exists(con, "task_results"):
                return ViewerSummary()
            task_columns = _table_columns(con, "task_results")
            finished_expr = _coalesce_existing_columns(
                task_columns,
                ["finished_at_utc", "evaluated_at_utc", "started_at_utc"],
            )
            latest = _first_value(con.execute(f"SELECT max({finished_expr}) FROM task_results").fetchone()) if finished_expr != "NULL" else None
            base_count_expr = (
                "count(*) FILTER (WHERE embedding_variant_name IS NULL)"
                if "embedding_variant_name" in task_columns
                else "count(*)"
            )
            variant_count_expr = (
                "count(*) FILTER (WHERE embedding_variant_name IS NOT NULL)"
                if "embedding_variant_name" in task_columns
                else "0"
            )
            task_counts = con.execute(
                f"""
                SELECT
                    count(DISTINCT model_name),
                    count(DISTINCT benchmark),
                    count(DISTINCT task_key),
                    {base_count_expr},
                    {variant_count_expr}
                FROM task_results
                """
            ).fetchone() or (0, 0, 0, 0, 0)
            language_count = 0
            if _table_exists(con, "dataset_metadata"):
                metadata_columns = _table_columns(con, "dataset_metadata")
                if "languages" in metadata_columns:
                    language_count = int(
                        _first_value(
                            con.execute(
                                """
                                SELECT count(DISTINCT item.language)
                                FROM dataset_metadata, unnest(languages) AS item(language)
                                WHERE item.language IS NOT NULL AND item.language != ''
                                """
                            ).fetchone()
                        )
                        or 0
                    )
                elif "language" in metadata_columns:
                    language_count = int(
                        _first_value(
                            con.execute(
                                "SELECT count(DISTINCT language) FROM dataset_metadata WHERE language IS NOT NULL AND language != ''"
                            ).fetchone()
                        )
                        or 0
                    )
            return ViewerSummary(
                model_count=int(task_counts[0] or 0),
                benchmark_count=int(task_counts[1] or 0),
                task_count=int(task_counts[2] or 0),
                language_count=language_count,
                base_result_count=int(task_counts[3] or 0),
                variant_result_count=int(task_counts[4] or 0),
                latest_finished_at_utc=str(latest) if latest else None,
            )
        finally:
            con.close()

    def fetch_variant_analysis(
        self,
        *,
        benchmarks: list[str],
        include_rescore: bool = False,
        include_truncate: bool = False,
    ) -> list[VariantAnalysisRow]:
        if not self.duckdb_path.exists() or not benchmarks:
            return []
        con = duckdb.connect(str(self.duckdb_path), read_only=True)
        try:
            if not _table_exists(con, "task_results"):
                return []
            columns = _table_columns(con, "task_results")
            required = {"model_name", "benchmark", "task_key", "score", "embedding_variant_name"}
            if not required.issubset(columns):
                return []
            embedding_dim_expr = "tr.embedding_dim" if "embedding_dim" in columns else "NULL"
            quantization_expr = "tr.quantization" if "quantization" in columns else "NULL"
            where, params = _benchmark_where_clause("tr.benchmark", benchmarks)
            rescore_filter = "" if include_rescore else "AND lower(tr.embedding_variant_name) NOT LIKE '%rescore%'"
            truncate_filter = "" if include_truncate else "AND lower(tr.embedding_variant_name) NOT LIKE '%truncate%'"
            query = f"""
                WITH base AS (
                    SELECT model_name, benchmark, task_key, score AS base_score
                    FROM task_results
                    WHERE embedding_variant_name IS NULL
                )
                SELECT
                    tr.model_name,
                    tr.embedding_variant_name,
                    {embedding_dim_expr} AS embedding_dim,
                    {quantization_expr} AS quantization,
                    count(*) AS task_count,
                    avg(tr.score) * 100.0 AS mean_score_100,
                    avg((tr.score - base.base_score) / nullif(base.base_score, 0.0)) * 100.0 AS base_delta_percent
                FROM task_results AS tr
                JOIN base
                  ON base.model_name = tr.model_name
                 AND base.benchmark = tr.benchmark
                 AND base.task_key = tr.task_key
                WHERE tr.embedding_variant_name IS NOT NULL
                  {rescore_filter}
                  {truncate_filter}
                  AND {where}
                GROUP BY 1, 2, 3, 4
                ORDER BY tr.model_name, tr.embedding_variant_name, embedding_dim, quantization
            """
            return [
                VariantAnalysisRow(
                    model_name=str(row[0]),
                    variant_name=str(row[1]),
                    embedding_dim=_int_or_none(row[2]),
                    quantization=_str_or_none(row[3]),
                    task_count=int(row[4]),
                    mean_score_100=float(row[5]),
                    base_delta_percent=_float_or_none(row[6]),
                )
                for row in con.execute(query, params).fetchall()
            ]
        finally:
            con.close()

    def fetch_rerank_diagnostics(self, *, benchmarks: list[str]) -> list[RerankDiagnosticRow]:
        if not self.duckdb_path.exists() or not benchmarks:
            return []
        con = duckdb.connect(str(self.duckdb_path), read_only=True)
        try:
            if not _table_exists(con, "task_diagnostics"):
                return []
            columns = _table_columns(con, "task_diagnostics")
            required = {"benchmark", "task_key"}
            if not required.issubset(columns):
                return []
            where, params = _benchmark_where_clause("benchmark", benchmarks)
            query = f"""
                SELECT
                    benchmark,
                    count(DISTINCT task_key) AS task_count,
                    avg(query_coverage) * 100.0 AS query_coverage_percent,
                    avg(relevant_coverage) * 100.0 AS relevant_coverage_percent,
                    avg(rerank_lift) * 100.0 AS mean_lift_points,
                    max(rerank_top_k) AS rerank_top_k,
                    min(candidate_source) AS candidate_source,
                    min(candidate_ranking) AS candidate_ranking,
                    min(bm25_source) AS bm25_source
                FROM task_diagnostics
                WHERE {where}
                GROUP BY benchmark
                ORDER BY benchmark
            """
            return [
                RerankDiagnosticRow(
                    benchmark=str(row[0]),
                    task_count=int(row[1]),
                    query_coverage_percent=_float_or_none(row[2]),
                    relevant_coverage_percent=_float_or_none(row[3]),
                    mean_lift_points=_float_or_none(row[4]),
                    rerank_top_k=_int_or_none(row[5]),
                    candidate_source=_str_or_none(row[6]),
                    candidate_ranking=_str_or_none(row[7]),
                    bm25_source=_str_or_none(row[8]),
                )
                for row in con.execute(query, params).fetchall()
            ]
        finally:
            con.close()

    def fetch_dataset_diagnostics(self, *, benchmarks: list[str]) -> list[DatasetDiagnosticRow]:
        if not self.duckdb_path.exists() or not benchmarks:
            return []
        con = duckdb.connect(str(self.duckdb_path), read_only=True)
        try:
            if not _table_exists(con, "dataset_metadata") or not _table_exists(con, "task_results"):
                return []
            metadata_columns = _table_columns(con, "dataset_metadata")
            task_columns = _table_columns(con, "task_results")
            if "benchmark" not in metadata_columns or "task_key" not in metadata_columns:
                return []
            language_expr = "language" if "language" in metadata_columns else "NULL"
            category_expr = "category" if "category" in metadata_columns else "NULL"
            query_count_expr = "query_count" if "query_count" in metadata_columns else "NULL"
            document_count_expr = "document_count" if "document_count" in metadata_columns else "NULL"
            query_chars_expr = "query_mean_chars" if "query_mean_chars" in metadata_columns else "NULL"
            document_chars_expr = "document_mean_chars" if "document_mean_chars" in metadata_columns else "NULL"
            saturation_join = ""
            saturation_select = "0 AS base_rows, 0 AS saturated_rows, NULL AS saturation_percent"
            if {"benchmark", "task_key", "score", "embedding_variant_name"}.issubset(task_columns):
                saturation_join = """
                    LEFT JOIN (
                        SELECT
                            benchmark,
                            count(*) FILTER (WHERE embedding_variant_name IS NULL) AS base_rows,
                            count(*) FILTER (WHERE embedding_variant_name IS NULL AND score >= 0.95) AS saturated_rows
                        FROM task_results
                        GROUP BY benchmark
                    ) AS sat USING (benchmark)
                """
                saturation_select = """
                    coalesce(max(sat.base_rows), 0) AS base_rows,
                    coalesce(max(sat.saturated_rows), 0) AS saturated_rows,
                    100.0 * coalesce(max(sat.saturated_rows), 0) / nullif(coalesce(max(sat.base_rows), 0), 0) AS saturation_percent
                """
            where, params = _benchmark_where_clause("dm.benchmark", benchmarks)
            query = f"""
                SELECT
                    dm.benchmark,
                    count(DISTINCT dm.task_key) AS task_count,
                    count(DISTINCT {language_expr}) FILTER (WHERE {language_expr} IS NOT NULL AND {language_expr} != '') AS language_count,
                    count(DISTINCT {category_expr}) FILTER (WHERE {category_expr} IS NOT NULL AND {category_expr} != '') AS category_count,
                    {saturation_select},
                    avg({query_count_expr}) AS mean_query_count,
                    avg({document_count_expr}) AS mean_document_count,
                    avg({query_chars_expr}) AS mean_query_chars,
                    avg({document_chars_expr}) AS mean_document_chars
                FROM dataset_metadata AS dm
                {saturation_join}
                WHERE {where}
                GROUP BY dm.benchmark
                ORDER BY dm.benchmark
            """
            return [
                DatasetDiagnosticRow(
                    benchmark=str(row[0]),
                    task_count=int(row[1]),
                    language_count=int(row[2] or 0),
                    category_count=int(row[3] or 0),
                    base_rows=int(row[4] or 0),
                    saturated_rows=int(row[5] or 0),
                    saturation_percent=_float_or_none(row[6]),
                    mean_query_count=_float_or_none(row[7]),
                    mean_document_count=_float_or_none(row[8]),
                    mean_query_chars=_float_or_none(row[9]),
                    mean_document_chars=_float_or_none(row[10]),
                )
                for row in con.execute(query, params).fetchall()
            ]
        finally:
            con.close()


def _table_columns(con: duckdb.DuckDBPyConnection, table: str) -> set[str]:
    return {str(row[0]) for row in con.execute(f"DESCRIBE {table}").fetchall()}


def _table_exists(con: duckdb.DuckDBPyConnection, table: str) -> bool:
    row = con.execute(
        "SELECT count(*) FROM information_schema.tables WHERE table_name = ?",
        [table],
    ).fetchone()
    return bool(row[0]) if row is not None else False


def _first_value(row: tuple[Any, ...] | None) -> Any:
    return row[0] if row is not None else None


def _benchmark_where_clause(column: str, benchmarks: list[str]) -> tuple[str, list[str]]:
    placeholders = ", ".join("?" for _ in benchmarks)
    return f"{column} IN ({placeholders})", benchmarks


def _coalesce_existing_columns(columns: set[str], candidates: list[str]) -> str:
    existing = [column for column in candidates if column in columns]
    if not existing:
        return "NULL"
    if len(existing) == 1:
        return existing[0]
    return f"coalesce({', '.join(existing)})"


def _float_or_none(value: Any) -> float | None:
    return float(value) if isinstance(value, int | float) else None


def _int_or_none(value: Any) -> int | None:
    return int(value) if isinstance(value, int) else None


def _str_or_none(value: Any) -> str | None:
    return str(value) if isinstance(value, str) and value else None
