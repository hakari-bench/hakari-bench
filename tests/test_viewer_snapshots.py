from pathlib import Path
from typing import Any

import duckdb
import pytest

from hakari_bench.viewer.config import BenchmarkConfig, OverallConfig, ViewerConfig
from hakari_bench.viewer.leaderboard import LeaderboardService
from test_viewer import _write_task_results


@pytest.mark.parametrize("languages", [(), ("en", "category:code"), ("category:code", "en")])
@pytest.mark.parametrize("target", ["all", "reranking"])
def test_initial_snapshot_matches_dynamic_and_survives_service_restart(
    tmp_path: Path, monkeypatch, target: str, languages: tuple[str, ...]
) -> None:
    path = tmp_path / "results.duckdb"
    _write_task_results(
        path,
        [
            (
                "model/a",
                "BenchA",
                "bench/a",
                "BenchA",
                "a1",
                "a1",
                "BenchA::a1",
                0.9,
                10,
                12,
                8192,
            ),
            (
                "model/b",
                "BenchA",
                "bench/a",
                "BenchA",
                "a1",
                "a1",
                "BenchA::a1",
                0.8,
                10,
                12,
                8192,
            ),
        ],
    )
    with duckdb.connect(str(path)) as con:
        con.execute(
            "INSERT INTO viewer_task_results SELECT * REPLACE ('reranking' AS score_target) FROM viewer_task_results"
        )
    config = ViewerConfig(
        benchmarks=[BenchmarkConfig(name="BenchA")],
        overalls=[OverallConfig(benchmarks=["BenchA"])],
    )
    options: dict[str, Any] = dict(
        score_target=target,
        language_filters=languages,
        score_aggregation="macro",
        column_mode="grouped",
        show_task_scores=True,
    )
    dynamic = LeaderboardService(
        duckdb_path=path, config=config, use_precomputed=False
    ).get_leaderboard("Overall", **options)
    first = LeaderboardService(duckdb_path=path, config=config).get_leaderboard(
        "Overall", **options
    )
    assert len(first.rows) == 2
    assert first == dynamic
    assert path.with_suffix(".leaderboard-cache.duckdb").exists()

    def fail(*args, **kwargs):
        raise AssertionError("Snapshot hit must not load task scores")

    monkeypatch.setattr(LeaderboardService, "_load_task_scores", fail)
    second = LeaderboardService(duckdb_path=path, config=config).get_leaderboard(
        "Overall", **options
    )
    assert second == dynamic
    second.rows.clear()
    assert (
        LeaderboardService(duckdb_path=path, config=config).get_leaderboard(
            "Overall", **options
        )
        == dynamic
    )
    # Changing source data or aggregation configuration must bypass old snapshots.
    with duckdb.connect(str(path)) as con:
        con.execute("UPDATE viewer_task_results SET score = 0.7")
    with pytest.raises(AssertionError):
        LeaderboardService(duckdb_path=path, config=config).get_leaderboard(
            "Overall", **options
        )


def test_snapshot_configuration_invalidation_and_filter_fallback(
    tmp_path: Path, monkeypatch
) -> None:
    path = tmp_path / "results.duckdb"
    _write_task_results(
        path,
        [
            (
                "model/a",
                "BenchA",
                "bench/a",
                "BenchA",
                "a1",
                "a1",
                "BenchA::a1",
                0.9,
                10,
                12,
                8192,
            )
        ],
    )
    config = ViewerConfig(
        benchmarks=[BenchmarkConfig(name="BenchA")],
        overalls=[OverallConfig(benchmarks=["BenchA"])],
    )
    service = LeaderboardService(duckdb_path=path, config=config)
    options: dict[str, Any] = dict(
        score_aggregation="macro", column_mode="grouped", show_task_scores=True
    )
    service.get_leaderboard("Overall", **options)

    def fail(*args, **kwargs):
        raise AssertionError("Dynamic path")

    monkeypatch.setattr(LeaderboardService, "_load_task_scores", fail)
    changed = config.model_copy(
        update={"benchmarks": [BenchmarkConfig(name="BenchA", excluded_tasks=["a1"])]}
    )
    with pytest.raises(AssertionError):
        LeaderboardService(duckdb_path=path, config=changed).get_leaderboard(
            "Overall", **options
        )
    for filters in (
        {"language_filters": ("en",)},
        {"rank_filtered": True, "model_filter": "model/a"},
        {"include_quantization_variants": True},
        {"task_filter": "a1"},
    ):
        with pytest.raises(AssertionError):
            service.get_leaderboard("Overall", **options, **filters)
    service.model_card_parameters.clear()
    with pytest.raises(AssertionError):
        service.get_leaderboard("Overall", **options)


def test_embedded_initial_snapshot_avoids_dynamic_load(
    tmp_path: Path, monkeypatch
) -> None:
    from hakari_bench.viewer.snapshots import build_initial_snapshots

    path = tmp_path / "results.duckdb"
    _write_task_results(
        path,
        [
            (
                "model/a",
                "BenchA",
                "bench/a",
                "BenchA",
                "a1",
                "a1",
                "BenchA::a1",
                0.9,
                10,
                12,
                8192,
            )
        ],
    )
    config = ViewerConfig(
        benchmarks=[BenchmarkConfig(name="BenchA")],
        overalls=[OverallConfig(benchmarks=["BenchA"])],
    )
    build_initial_snapshots(path, config)

    def fail(*args, **kwargs):
        raise AssertionError("Embedded snapshot must avoid task loading")

    monkeypatch.setattr(LeaderboardService, "_load_task_scores", fail)
    result = LeaderboardService(duckdb_path=path, config=config).get_leaderboard(
        "Overall",
        score_aggregation="macro",
        column_mode="grouped",
        show_task_scores=True,
        sort="model_name",
        direction="desc",
    )
    assert [row.model_name for row in result.rows] == ["model/a"]
    assert not path.with_suffix(".leaderboard-cache.duckdb").exists()


@pytest.mark.parametrize("target", ["all", "reranking"])
def test_english_snapshot_keeps_code_and_recalculates_eligible_models(tmp_path: Path, monkeypatch, target: str) -> None:
    from hakari_bench.viewer.snapshots import build_initial_snapshots

    path = tmp_path / "results.duckdb"
    rows = [
        (model, "BenchA", "bench/a", "BenchA", task, task, f"BenchA::{task}", score, 10, 12, 8192)
        for model, tasks, score in (("model/full", ("en", "code", "ja"), .8), ("model/english", ("en", "code"), .9))
        for task in tasks
    ]
    _write_task_results(path, rows)
    with duckdb.connect(str(path)) as con:
        con.execute("UPDATE viewer_task_results SET language = split_name, languages = [split_name], category = CASE WHEN split_name = 'code' THEN 'code' ELSE 'natural_language' END")
        con.execute("INSERT INTO viewer_task_results SELECT * REPLACE ('reranking' AS score_target) FROM viewer_task_results")
    config = ViewerConfig(benchmarks=[BenchmarkConfig(name="BenchA")], overalls=[OverallConfig(benchmarks=["BenchA"])])
    options: dict[str, Any] = dict(score_target=target, score_aggregation="macro", column_mode="grouped", show_task_scores=True, language_filters=("en", "category:code"))
    expected = LeaderboardService(duckdb_path=path, config=config, use_precomputed=False).get_leaderboard("Overall", **options)
    assert expected.selected_languages == ("en", "category:code")
    assert {row.model_name for row in expected.rows} == {"model/full", "model/english"}
    assert expected.rows[0].model_name == "model/english"
    assert expected.rows[0].task_count == 1  # One grouped benchmark contribution.
    build_initial_snapshots(path, config)

    def fail(*args, **kwargs):
        raise AssertionError("English must use its embedded snapshot")

    monkeypatch.setattr(LeaderboardService, "_load_task_scores", fail)
    assert LeaderboardService(duckdb_path=path, config=config).get_leaderboard("Overall", **options) == expected


def test_english_warmup_does_not_block_cached_multilingual(tmp_path: Path, monkeypatch) -> None:
    from concurrent.futures import ThreadPoolExecutor
    import threading

    path = tmp_path / "results.duckdb"
    _write_task_results(path, [("model/a", "BenchA", "bench/a", "BenchA", "a1", "a1", "BenchA::a1", .9, 10, 12, 8192)])
    config = ViewerConfig(benchmarks=[BenchmarkConfig(name="BenchA")], overalls=[OverallConfig(benchmarks=["BenchA"])])
    service = LeaderboardService(duckdb_path=path, config=config)
    options: dict[str, Any] = dict(score_aggregation="macro", column_mode="grouped", show_task_scores=True)
    expected = service.get_leaderboard("Overall", **options)
    started, release = threading.Event(), threading.Event()
    original = LeaderboardService._load_task_scores

    def blocked(*args, **kwargs):
        started.set()
        assert release.wait(10)
        return original(*args, **kwargs)

    monkeypatch.setattr(LeaderboardService, "_load_task_scores", blocked)
    with ThreadPoolExecutor(max_workers=2) as executor:
        english = executor.submit(service.get_leaderboard, "Overall", **options, language_filters=("en", "category:code"))
        try:
            assert started.wait(5)
            multilingual = executor.submit(service.get_leaderboard, "Overall", **options)
            assert multilingual.result(timeout=3) == expected
        finally:
            release.set()
        english.result(timeout=5)
