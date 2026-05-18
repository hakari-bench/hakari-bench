from __future__ import annotations

from collections.abc import Collection
import re

import duckdb


_SQL_IDENTIFIER_RE = re.compile(r"^[A-Za-z_][A-Za-z0-9_]*$")


def quote_identifier(identifier: str, *, allowed: Collection[str] | None = None) -> str:
    """Quote a SQL identifier after validating it against syntax and an optional allowlist."""

    if allowed is not None and identifier not in allowed:
        raise ValueError(f"SQL identifier is not allowlisted: {identifier}")
    if not _SQL_IDENTIFIER_RE.fullmatch(identifier):
        raise ValueError(f"Invalid SQL identifier: {identifier}")
    return f'"{identifier}"'


def qualified_column(alias: str, column: str, *, allowed_columns: Collection[str]) -> str:
    quoted_alias = quote_identifier(alias)
    quoted_column = quote_identifier(column, allowed=allowed_columns)
    return f"{quoted_alias}.{quoted_column}"


def column_or_null(columns: Collection[str], column: str, *, alias: str | None = None) -> str:
    if column not in columns:
        return "NULL"
    if alias is None:
        return quote_identifier(column, allowed=columns)
    return qualified_column(alias, column, allowed_columns=columns)


def coalesce_existing_columns(columns: Collection[str], candidates: list[str], *, alias: str | None = None) -> str:
    existing = [column_or_null(columns, column, alias=alias) for column in candidates if column in columns]
    if not existing:
        return "NULL"
    if len(existing) == 1:
        return existing[0]
    return f"coalesce({', '.join(existing)})"


def table_columns(
    con: duckdb.DuckDBPyConnection,
    table: str,
    *,
    allowed_tables: Collection[str] | None,
) -> set[str]:
    table_expr = quote_identifier(table, allowed=allowed_tables)
    return {str(row[0]) for row in con.execute(f"DESCRIBE {table_expr}").fetchall()}


def table_exists(
    con: duckdb.DuckDBPyConnection,
    table: str,
    *,
    allowed_tables: Collection[str] | None,
) -> bool:
    quote_identifier(table, allowed=allowed_tables)
    row = con.execute(
        "SELECT count(*) FROM information_schema.tables WHERE table_name = ?",
        [table],
    ).fetchone()
    return bool(row[0]) if row is not None else False
