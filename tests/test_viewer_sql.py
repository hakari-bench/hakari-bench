from __future__ import annotations

from pathlib import Path

import duckdb
import pytest

from hakari_bench.viewer.sql import (
    column_or_null,
    coalesce_existing_columns,
    qualified_column,
    quote_identifier,
    table_columns,
    table_exists,
)


def test_sql_identifier_helpers_quote_known_good_identifiers() -> None:
    columns = {"benchmark", "score"}

    assert quote_identifier("task_results", allowed={"task_results"}) == '"task_results"'
    assert qualified_column("tr", "score", allowed_columns=columns) == '"tr"."score"'
    assert column_or_null(columns, "benchmark", alias="tr") == '"tr"."benchmark"'
    assert column_or_null(columns, "missing", alias="tr") == "NULL"
    assert coalesce_existing_columns(columns, ["finished_at_utc", "benchmark"], alias="tr") == '"tr"."benchmark"'


def test_sql_identifier_helpers_reject_untrusted_identifiers() -> None:
    with pytest.raises(ValueError, match="not allowlisted"):
        quote_identifier("task_results", allowed={"dataset_metadata"})
    with pytest.raises(ValueError, match="Invalid SQL identifier"):
        quote_identifier("task_results; DROP TABLE task_results")
    with pytest.raises(ValueError, match="Invalid SQL identifier"):
        qualified_column("tr; DROP TABLE task_results", "score", allowed_columns={"score"})
    with pytest.raises(ValueError, match="not allowlisted"):
        qualified_column("tr", "score", allowed_columns={"benchmark"})


def test_table_introspection_uses_allowlisted_identifiers(tmp_path: Path) -> None:
    db_path = tmp_path / "results.duckdb"
    con = duckdb.connect(str(db_path))
    try:
        con.execute("CREATE TABLE task_results (benchmark VARCHAR, score DOUBLE)")

        assert table_exists(con, "task_results", allowed_tables={"task_results"}) is True
        assert table_columns(con, "task_results", allowed_tables={"task_results"}) == {"benchmark", "score"}
        with pytest.raises(ValueError, match="not allowlisted"):
            table_exists(con, "task_results", allowed_tables={"dataset_metadata"})
        with pytest.raises(ValueError, match="Invalid SQL identifier"):
            table_columns(con, "task_results; DROP TABLE task_results", allowed_tables=None)
    finally:
        con.close()
