from __future__ import annotations

import os
import time
from pathlib import Path

import duckdb

from nano_ir_benchmark.viewer.config import load_viewer_config
from nano_ir_benchmark.viewer.app import create_app
from nano_ir_benchmark.viewer.leaderboard import LeaderboardService, TaskScore, compute_leaderboard_rows
from nano_ir_benchmark.viewer.store import DuckDbLocation, LocalDuckDbStore


def test_viewer_config_excludes_jmteb_from_overall() -> None:
    config = load_viewer_config()

    assert "NanoJMTEB" in config.view_names
    assert "NanoJMTEB" not in config.overall.benchmarks
    assert "NanoRTEB" in config.overall.benchmarks


def test_overall_leaderboard_requires_all_configured_benchmark_tasks(tmp_path: Path) -> None:
    db_path = tmp_path / "results.duckdb"
    _write_task_results(
        db_path,
        [
            ("model/a", "BenchA", "a1", 0.90, 10, 12, 8192),
            ("model/a", "BenchA", "a2", 0.80, 10, 12, 8192),
            ("model/a", "BenchB", "b1", 0.70, 10, 12, 8192),
            ("model/b", "BenchA", "a1", 0.95, 20, 24, 4096),
            ("model/b", "BenchA", "a2", 0.75, 20, 24, 4096),
            ("model/b", "BenchB", "b1", 0.65, 20, 24, 4096),
            ("model/incomplete", "BenchA", "a1", 1.00, 30, 36, 2048),
        ],
    )
    config_dir = tmp_path / "config"
    config_dir.mkdir()
    (config_dir / "benchmarks.yaml").write_text(
        """
benchmarks:
  - name: BenchA
  - name: BenchB
  - name: NanoJMTEB
    include_in_overall: false
""".strip(),
        encoding="utf-8",
    )
    (config_dir / "overall.yaml").write_text(
        """
name: Overall
label: Overall
benchmarks:
  - BenchA
  - BenchB
""".strip(),
        encoding="utf-8",
    )

    service = LeaderboardService(duckdb_path=db_path, config=load_viewer_config(config_dir))
    result = service.get_leaderboard("Overall")

    assert [row.model_name for row in result.rows] == ["model/a", "model/b"]
    assert result.rows[0].task_count == 3
    assert result.rows[0].macro_mean == 77.5
    assert result.rows[0].micro_mean == 80.0


def test_individual_leaderboard_uses_simple_task_mean() -> None:
    rows = compute_leaderboard_rows(
        [
            TaskScore("model/a", "BenchA", "a1", 0.50, None, None, None),
            TaskScore("model/a", "BenchA", "a2", 0.70, None, None, None),
            TaskScore("model/b", "BenchA", "a1", 0.80, None, None, None),
            TaskScore("model/b", "BenchA", "a2", 0.20, None, None, None),
        ],
        is_overall=False,
    )

    by_model = {row.model_name: row for row in rows}
    assert by_model["model/a"].mean_score == 60.0
    assert by_model["model/a"].macro_mean is None
    assert by_model["model/a"].micro_mean is None


def test_local_duckdb_store_copies_newer_source_on_page_load(tmp_path: Path) -> None:
    source = tmp_path / "source.duckdb"
    local = tmp_path / "local.duckdb"
    source.write_bytes(b"old")
    store = LocalDuckDbStore(DuckDbLocation(local_path=local, source_path=source))

    assert store.ensure_current() is True
    assert local.read_bytes() == b"old"

    time.sleep(0.01)
    source.write_bytes(b"new")
    os.utime(source, None)

    assert store.ensure_current() is True
    assert local.read_bytes() == b"new"


def test_viewer_leaderboard_endpoint_renders_htmx_table(tmp_path: Path) -> None:
    from fastapi.testclient import TestClient

    db_path = tmp_path / "results.duckdb"
    _write_task_results(
        db_path,
        [
            ("model/a", "BenchA", "a1", 0.90, 10, 12, 8192),
            ("model/b", "BenchA", "a1", 0.80, 20, 24, 4096),
        ],
    )
    config_dir = tmp_path / "config"
    config_dir.mkdir()
    (config_dir / "benchmarks.yaml").write_text("benchmarks:\n  - name: BenchA\n", encoding="utf-8")
    (config_dir / "overall.yaml").write_text("name: Overall\nlabel: Overall\nbenchmarks:\n  - BenchA\n", encoding="utf-8")

    app = create_app(store=LocalDuckDbStore(DuckDbLocation(local_path=db_path)), config_dir=config_dir)
    response = TestClient(app).get("/leaderboard?view=Overall&sort=borda_rank&direction=asc")

    assert response.status_code == 200
    assert "Macro Mean" in response.text
    assert "model/a" in response.text
    assert 'hx-get="/leaderboard?' in response.text


def _write_task_results(db_path: Path, rows: list[tuple[str, str, str, float, int, int, int]]) -> None:
    con = duckdb.connect(str(db_path))
    try:
        con.execute(
            """
            CREATE TABLE task_results (
                model_name VARCHAR,
                benchmark VARCHAR,
                task_key VARCHAR,
                score DOUBLE,
                active_parameters BIGINT,
                total_parameters BIGINT,
                max_seq_length INTEGER
            )
            """
        )
        con.executemany("INSERT INTO task_results VALUES (?, ?, ?, ?, ?, ?, ?)", rows)
    finally:
        con.close()
