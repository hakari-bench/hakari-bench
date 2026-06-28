from __future__ import annotations

from pathlib import Path

from fastapi.testclient import TestClient

from hakari_bench.viewer.app import create_app
from hakari_bench.viewer.store import DuckDbLocation, LocalDuckDbStore

from tests.test_viewer import _write_task_results


def _build_client(tmp_path: Path) -> TestClient:
    db_path = tmp_path / "results.duckdb"
    _write_task_results(
        db_path,
        [
            ("model/a", "BenchA", "bench/a", "BenchA", "a1", "a1", "a1", 0.90, 10, 12, 8192),
            ("model/b", "BenchA", "bench/a", "BenchA", "a1", "a1", "a1", 0.80, 10, 12, 8192),
        ],
        dataset_metadata_rows=[("BenchA", "bench/a", "BenchA", "a1", "a1", "a1", "en", ["en"])],
    )
    config_dir = tmp_path / "config"
    config_dir.mkdir()
    (config_dir / "benchmarks.yaml").write_text("benchmarks:\n  - name: BenchA\n", encoding="utf-8")
    (config_dir / "overall.yaml").write_text(
        "name: Overall\nlabel: Overall\nbenchmarks:\n  - BenchA\n", encoding="utf-8"
    )
    app = create_app(store=LocalDuckDbStore(DuckDbLocation(local_path=db_path)), config_dir=config_dir)
    return TestClient(app)


def test_api_config_returns_scope_and_defaults(tmp_path: Path) -> None:
    client = _build_client(tmp_path)
    response = client.get("/api/config")
    assert response.status_code == 200
    payload = response.json()
    assert payload["clear_scope"] == "Clear"
    assert payload["defaults"]["view"] == "Overall"
    preset_names = [preset["name"] for preset in payload["scope"]["presets"]]
    assert preset_names == ["Overall", "Overall (EN)", "Clear"]
    suite_keys = [suite["selection_key"] for suite in payload["scope"]["suites"]]
    assert "BenchA" in suite_keys
    assert payload["links"]["github"].endswith("hakari-bench/hakari-bench")


def test_api_leaderboard_returns_rows_as_json(tmp_path: Path) -> None:
    client = _build_client(tmp_path)
    response = client.get("/api/leaderboard?view=Overall&sort=borda_score&direction=desc")
    assert response.status_code == 200
    payload = response.json()
    assert payload["view_name"] == "Overall"
    assert payload["effective_sort"] == "borda_score"
    assert payload["effective_direction"] == "desc"
    model_names = [row["model_name"] for row in payload["rows"]]
    assert model_names == ["model/a", "model/b"]
    assert payload["rows"][0]["borda_score"] >= payload["rows"][1]["borda_score"]


def test_api_leaderboard_csv_is_downloadable(tmp_path: Path) -> None:
    client = _build_client(tmp_path)
    response = client.get("/api/leaderboard.csv?view=Overall")
    assert response.status_code == 200
    assert response.headers["content-type"].startswith("text/csv")
    assert "attachment" in response.headers["content-disposition"]
    assert "model/a" in response.text


def test_api_leaderboard_preserves_legacy_query_params(tmp_path: Path) -> None:
    client = _build_client(tmp_path)
    response = client.get("/api/leaderboard?view=BenchA&score=macro&metric=recall@10")
    assert response.status_code == 200
    payload = response.json()
    assert payload["view_name"] == "BenchA"
    assert payload["score_aggregation"] == "macro"
