from __future__ import annotations

import os
import time
from pathlib import Path

import duckdb

from nano_ir_benchmark.viewer.app import _fmt_max_len, _metric_column_label, create_app
from nano_ir_benchmark.viewer.config import load_viewer_config
from nano_ir_benchmark.viewer.leaderboard import LeaderboardService, TaskScore, compute_leaderboard_rows
from nano_ir_benchmark.viewer.store import DuckDbLocation, LocalDuckDbStore


def test_viewer_config_uses_curated_overall_benchmarks_in_display_order() -> None:
    config = load_viewer_config()

    assert config.overall.benchmarks == [
        "NanoMMTEB",
        "NanoRTEB",
        "MNanoBEIR",
        "NanoMLDR",
        "NanoLongEmbed",
        "NanoCoIR",
    ]
    assert config.view_names[:7] == [
        "Overall",
        "NanoMMTEB",
        "NanoRTEB",
        "MNanoBEIR",
        "NanoMLDR",
        "NanoLongEmbed",
        "NanoCoIR",
    ]
    assert "NanoJMTEB" in config.view_names
    assert "NanoJMTEB" not in config.overall.benchmarks
    mnanobeir = config.benchmark_for_view("MNanoBEIR")
    assert mnanobeir is not None
    assert [group.name for group in mnanobeir.resolved_score_groups] == ["task_mean", "lang_mean"]


def test_overall_leaderboard_requires_all_configured_benchmark_tasks(tmp_path: Path) -> None:
    db_path = tmp_path / "results.duckdb"
    _write_task_results(
        db_path,
        [
            ("model/a", "BenchA", "bench/a", "BenchA", "a1", "a1", "BenchA::a1", 0.90, 10, 12, 8192),
            ("model/a", "BenchA", "bench/a", "BenchA", "a2", "a2", "BenchA::a2", 0.80, 10, 12, 8192),
            ("model/a", "BenchB", "bench/b", "BenchB", "b1", "b1", "BenchB::b1", 0.70, 10, 12, 8192),
            ("model/b", "BenchA", "bench/a", "BenchA", "a1", "a1", "BenchA::a1", 0.95, 20, 24, 4096),
            ("model/b", "BenchA", "bench/a", "BenchA", "a2", "a2", "BenchA::a2", 0.75, 20, 24, 4096),
            ("model/b", "BenchB", "bench/b", "BenchB", "b1", "b1", "BenchB::b1", 0.65, 20, 24, 4096),
            ("model/incomplete", "BenchA", "bench/a", "BenchA", "a1", "a1", "BenchA::a1", 1.00, 30, 36, 2048),
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
            TaskScore("model/a", "BenchA", "bench/a", "BenchA", "a1", "a1", "a1", 0.50, None, None, None),
            TaskScore("model/a", "BenchA", "bench/a", "BenchA", "a2", "a2", "a2", 0.70, None, None, None),
            TaskScore("model/b", "BenchA", "bench/a", "BenchA", "a1", "a1", "a1", 0.80, None, None, None),
            TaskScore("model/b", "BenchA", "bench/a", "BenchA", "a2", "a2", "a2", 0.20, None, None, None),
        ],
        is_overall=False,
    )

    by_model = {row.model_name: row for row in rows}
    assert by_model["model/a"].mean_score == 60.0
    assert by_model["model/a"].macro_mean is None
    assert by_model["model/a"].micro_mean is None
    assert by_model["model/a"].metric_values == {}


def test_leaderboard_uses_competition_rank_for_ties() -> None:
    scores = [1.0, 0.9, 0.8, 0.7, 0.6, 0.5, 0.4, 0.3, 0.3, 0.1]
    rows = compute_leaderboard_rows(
        [
            TaskScore(
                f"model/{index}",
                "BenchA",
                "bench/a",
                "BenchA",
                "a1",
                "a1",
                "a1",
                score,
                None,
                None,
                None,
            )
            for index, score in enumerate(scores, start=1)
        ],
        is_overall=False,
    )

    ranks_by_model = {row.model_name: row.mean_rank for row in rows}
    assert ranks_by_model["model/8"] == 8
    assert ranks_by_model["model/9"] == 8
    assert ranks_by_model["model/10"] == 10


def test_individual_leaderboard_adds_metric_columns_from_score_group(tmp_path: Path) -> None:
    db_path = tmp_path / "results.duckdb"
    _write_task_results(
        db_path,
        [
            ("model/a", "MNanoBEIR", "NanoBEIR-ja", "NanoBEIR-ja", "NanoArguAna", "arguana", "ja-arguana", 0.80, 10, 12, 8192),
            ("model/a", "MNanoBEIR", "NanoBEIR-ja", "NanoBEIR-ja", "NanoFEVER", "fever", "ja-fever", 0.60, 10, 12, 8192),
            ("model/a", "MNanoBEIR", "NanoBEIR-en", "NanoBEIR-en", "NanoArguAna", "arguana", "en-arguana", 0.70, 10, 12, 8192),
            ("model/a", "MNanoBEIR", "NanoBEIR-en", "NanoBEIR-en", "NanoFEVER", "fever", "en-fever", 0.50, 10, 12, 8192),
            ("model/b", "MNanoBEIR", "NanoBEIR-ja", "NanoBEIR-ja", "NanoArguAna", "arguana", "ja-arguana", 0.50, 20, 24, 4096),
            ("model/b", "MNanoBEIR", "NanoBEIR-ja", "NanoBEIR-ja", "NanoFEVER", "fever", "ja-fever", 0.40, 20, 24, 4096),
            ("model/b", "MNanoBEIR", "NanoBEIR-en", "NanoBEIR-en", "NanoArguAna", "arguana", "en-arguana", 0.60, 20, 24, 4096),
            ("model/b", "MNanoBEIR", "NanoBEIR-en", "NanoBEIR-en", "NanoFEVER", "fever", "en-fever", 0.30, 20, 24, 4096),
        ],
    )
    config_dir = tmp_path / "config"
    config_dir.mkdir()
    (config_dir / "benchmarks.yaml").write_text(
        """
benchmarks:
  - name: MNanoBEIR
    score_groups:
      - name: task_mean
        label: Task Mean
        group_by: task_name
      - name: lang_mean
        label: Lang Mean
        group_by: dataset_name
""".strip(),
        encoding="utf-8",
    )
    (config_dir / "overall.yaml").write_text(
        "name: Overall\nlabel: Overall\nbenchmarks:\n  - MNanoBEIR\n",
        encoding="utf-8",
    )

    service = LeaderboardService(duckdb_path=db_path, config=load_viewer_config(config_dir))
    task_result = service.get_leaderboard("MNanoBEIR", score_group_name="task_mean")
    lang_result = service.get_leaderboard("MNanoBEIR", score_group_name="lang_mean", sort="metric:NanoBEIR-ja")

    assert task_result.metric_columns == ["arguana", "fever"]
    assert task_result.rows[0].metric_values["arguana"] == 75.0
    assert lang_result.metric_columns == ["NanoBEIR-en", "NanoBEIR-ja"]
    lang_by_model = {row.model_name: row for row in lang_result.rows}
    assert lang_by_model["model/a"].metric_values["NanoBEIR-ja"] == 70.0

    from fastapi.testclient import TestClient

    app = create_app(store=LocalDuckDbStore(DuckDbLocation(local_path=db_path)), config_dir=config_dir)
    response = TestClient(app).get("/leaderboard?view=MNanoBEIR&group=lang_mean&sort=metric:NanoBEIR-ja")

    assert response.status_code == 200
    assert "Task Mean" in response.text
    assert "Lang Mean" in response.text
    assert "Mean Score" in response.text
    assert ">BEIR-ja</span>" in response.text
    assert "[overflow-wrap:anywhere]" in response.text
    assert "w-[4.75rem] min-w-[4.75rem] max-w-[4.75rem]" in response.text
    assert "metric%3ANanoBEIR-ja" in response.text
    assert 'hx-push-url="/?view=MNanoBEIR&amp;sort=metric%3ANanoBEIR-ja' in response.text


def test_metric_column_label_omits_nano_prefix_only_for_display() -> None:
    assert _metric_column_label("NanoAILAStatutes") == "AILAStatutes"
    assert _metric_column_label("NanoBEIR-ja") == "BEIR-ja"
    assert _metric_column_label("NanoWikipediaRetrievalMultilingual") == "WikipediaRetrievalMultilingual"
    assert _metric_column_label("arguana") == "arguana"


def test_max_len_is_formatted_with_grouping_separator() -> None:
    assert _fmt_max_len(8192) == "8,192"
    assert _fmt_max_len(None) == ""


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
            ("model/a", "BenchA", "bench/a", "BenchA", "a1", "a1", "BenchA::a1", 0.90, 10, 12, 8192),
            ("model/b", "BenchA", "bench/a", "BenchA", "a1", "a1", "BenchA::a1", 0.80, 20, 24, 4096),
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


def test_viewer_page_uses_query_state_and_canonical_url(tmp_path: Path) -> None:
    from fastapi.testclient import TestClient

    db_path = tmp_path / "results.duckdb"
    _write_task_results(
        db_path,
        [
            ("model/a", "MNanoBEIR", "NanoBEIR-ja", "NanoBEIR-ja", "NanoArguAna", "arguana", "ja-arguana", 0.80, 10, 12, 8192),
            ("model/b", "MNanoBEIR", "NanoBEIR-ja", "NanoBEIR-ja", "NanoArguAna", "arguana", "ja-arguana", 0.70, 20, 24, 4096),
        ],
    )
    config_dir = tmp_path / "config"
    config_dir.mkdir()
    (config_dir / "benchmarks.yaml").write_text(
        """
benchmarks:
  - name: MNanoBEIR
    score_groups:
      - name: lang_mean
        label: Lang Mean
        group_by: dataset_name
""".strip(),
        encoding="utf-8",
    )
    (config_dir / "overall.yaml").write_text(
        "name: Overall\nlabel: Overall\nbenchmarks:\n  - MNanoBEIR\n",
        encoding="utf-8",
    )

    app = create_app(store=LocalDuckDbStore(DuckDbLocation(local_path=db_path)), config_dir=config_dir)
    response = TestClient(app).get("/?view=MNanoBEIR&group=lang_mean&sort=metric:NanoBEIR-ja&direction=desc")

    assert response.status_code == 200
    assert '<link rel="canonical" href="/">' in response.text
    assert (
        'hx-get="/leaderboard?view=MNanoBEIR&amp;sort=metric%3ANanoBEIR-ja&amp;direction=desc&amp;group=lang_mean"'
        in response.text
    )


def _write_task_results(
    db_path: Path,
    rows: list[tuple[str, str, str, str, str, str, str, float, int, int, int]],
) -> None:
    con = duckdb.connect(str(db_path))
    try:
        con.execute(
            """
            CREATE TABLE task_results (
                model_name VARCHAR,
                benchmark VARCHAR,
                dataset_id VARCHAR,
                dataset_name VARCHAR,
                split_name VARCHAR,
                task_name VARCHAR,
                task_key VARCHAR,
                score DOUBLE,
                active_parameters BIGINT,
                total_parameters BIGINT,
                max_seq_length INTEGER
            )
            """
        )
        con.executemany("INSERT INTO task_results VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", rows)
    finally:
        con.close()
