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


def test_api_leaderboard_returns_filter_facets_and_total(tmp_path: Path) -> None:
    client = _build_client(tmp_path)
    payload = client.get("/api/leaderboard?view=Overall").json()
    assert payload["total_row_count"] == 2
    assert set(payload["filter_facets"]).issuperset(
        {"dim", "quant", "commercial", "model_type", "dtype", "attn", "prompt"}
    )
    assert "model_type" in payload["filter_selected"]


def test_api_leaderboard_model_text_filter_hides_rows(tmp_path: Path) -> None:
    client = _build_client(tmp_path)
    payload = client.get("/api/leaderboard?view=Overall&model_filter=model/a").json()
    assert payload["total_row_count"] == 2
    model_names = [row["model_name"] for row in payload["rows"]]
    assert model_names == ["model/a"]


def test_api_leaderboard_preserves_legacy_query_params(tmp_path: Path) -> None:
    client = _build_client(tmp_path)
    response = client.get("/api/leaderboard?view=BenchA&score=macro&metric=recall@10")
    assert response.status_code == 200
    payload = response.json()
    assert payload["view_name"] == "BenchA"
    assert payload["score_aggregation"] == "macro"


def test_serve_frontend_mounts_spa_over_html_routes(tmp_path: Path) -> None:
    db_path = tmp_path / "results.duckdb"
    _write_task_results(
        db_path,
        [("model/a", "BenchA", "bench/a", "BenchA", "a1", "a1", "a1", 0.90, 10, 12, 8192)],
        dataset_metadata_rows=[("BenchA", "bench/a", "BenchA", "a1", "a1", "a1", "en", ["en"])],
    )
    config_dir = tmp_path / "config"
    config_dir.mkdir()
    (config_dir / "benchmarks.yaml").write_text("benchmarks:\n  - name: BenchA\n", encoding="utf-8")
    (config_dir / "overall.yaml").write_text(
        "name: Overall\nlabel: Overall\nbenchmarks:\n  - BenchA\n", encoding="utf-8"
    )
    dist = tmp_path / "dist"
    (dist / "assets").mkdir(parents=True)
    (dist / "index.html").write_text("<!doctype html><title>React SPA</title>", encoding="utf-8")
    (dist / "assets" / "app.js").write_text("export const x = 1;", encoding="utf-8")

    app = create_app(
        store=LocalDuckDbStore(DuckDbLocation(local_path=db_path)),
        config_dir=config_dir,
        serve_frontend=True,
        frontend_dist=dist,
    )
    client = TestClient(app)

    root = client.get("/")
    assert root.status_code == 200
    assert "React SPA" in root.text
    assert "unsafe-inline" in root.headers["content-security-policy"]
    # SPA fallback for the docs route too.
    assert "React SPA" in client.get("/docs/benchmark-tasks/anything").text
    # Built assets are served under /static.
    assert client.get("/static/assets/app.js").status_code == 200
    # The JSON API still works alongside the SPA.
    assert client.get("/api/config").status_code == 200


def test_api_docs_index_and_group(tmp_path: Path) -> None:
    db_path = tmp_path / "results.duckdb"
    _write_task_results(
        db_path,
        [("model/a", "BenchA", "bench/a", "BenchA", "a1", "a1", "a1", 0.90, 10, 12, 8192)],
        dataset_metadata_rows=[("BenchA", "bench/a", "BenchA", "a1", "a1", "a1", "en", ["en"])],
    )
    config_dir = tmp_path / "config"
    config_dir.mkdir()
    (config_dir / "benchmarks.yaml").write_text("benchmarks:\n  - name: BenchA\n", encoding="utf-8")
    (config_dir / "overall.yaml").write_text(
        "name: Overall\nlabel: Overall\nbenchmarks:\n  - BenchA\n", encoding="utf-8"
    )
    docs_dir = tmp_path / "docs"
    (docs_dir / "BenchA").mkdir(parents=True)
    (docs_dir / "BenchA" / "index.md").write_text("# BenchA\n\nOverview text.\n", encoding="utf-8")

    app = create_app(
        store=LocalDuckDbStore(DuckDbLocation(local_path=db_path)),
        config_dir=config_dir,
        docs_dir=docs_dir,
    )
    client = TestClient(app)

    index = client.get("/api/docs").json()
    assert any(group["title"] == "BenchA" for group in index["groups"])

    group = client.get("/api/docs/benchmark-tasks/BenchA").json()
    assert group["title"] == "BenchA"
    assert "Overview text." in group["html"]

    assert client.get("/api/docs/benchmark-tasks/Missing").status_code == 404
