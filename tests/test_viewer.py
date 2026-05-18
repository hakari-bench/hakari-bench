from __future__ import annotations

import logging
import os
import re
import time
from pathlib import Path

import duckdb
import pytest

from hakari_bench.viewer.app import (
    _fmt_max_len,
    _metric_column_label,
    _metric_column_labels,
    _rounded_z_score,
    _view_group,
    _z_score_bucket_class,
    create_app,
    render_table_head,
)
from hakari_bench.viewer.config import BenchmarkConfig, OverallConfig, ViewerConfig, load_viewer_config
from hakari_bench.viewer.data import CURRENT_DUCKDB_SCHEMA_VERSION
from hakari_bench.viewer.leaderboard import LeaderboardService, TaskScore, _clear_task_score_cache, compute_leaderboard_rows
from hakari_bench.viewer.model_display import model_cell_views
from hakari_bench.viewer.store import (
    DuckDbLocation,
    HuggingFaceDuckDbSource,
    LocalDuckDbStore,
    resolve_duckdb_location,
)
from hakari_bench.viewer.variant_display import VariantDisplayFlags


def test_viewer_config_uses_curated_overall_benchmarks_in_display_order() -> None:
    config = load_viewer_config()
    language_nanomteb_benchmarks = [
        "NanoMTEB-Dutch",
        "NanoMTEB-French",
        "NanoMTEB-German",
        "NanoJMTEB-v2",
        "NanoMTEB-Korean",
        "NanoFaMTEB-v2",
        "NanoMTEB-Polish",
        "NanoRuMTEB",
        "NanoMTEB-Scandinavian",
        "NanoMTEB-Spanish",
        "NanoMTEB-Thai",
        "NanoVNMTEB",
        "NanoMTEB-Misc",
    ]
    expected_overall_benchmarks = [
        "NanoMMTEB-v2",
        "NanoRTEB",
        "MNanoBEIR",
        "NanoBIRCO",
        "NanoMLDR",
        "NanoLongEmbed",
        "NanoDAPFAM",
        "NanoCoIR",
        "NanoIFIR",
        "NanoLaw",
        "NanoMedical",
        "NanoRARb",
        "NanoBRIGHT",
        "NanoCodeRAG",
        "NanoChemTEB",
        "NanoR2MED",
        "NanoBuiltBench",
        "NanoCMTEB",
        "NanoIndicQA",
        "NanoMuPLeR",
    ]

    assert config.overall.benchmark_names == expected_overall_benchmarks
    grouped_overall = config.overall_for_view("OverallGrouped")
    assert grouped_overall is not None
    assert [component.name for component in grouped_overall.benchmark_components] == [
        "MNanoBEIR",
        "NanoRTEB",
        "NanoMMTEB-v2",
        "NanoBIRCO",
        "NanoMLDR",
        "NanoLongEmbed",
        "NanoDAPFAM",
        "NanoCoIR",
        "NanoIFIR",
        "NanoLaw",
        "NanoMedical",
        "NanoRARb",
        "NanoBRIGHT",
        "NanoCodeRAG",
        "NanoChemTEB",
        "NanoR2MED",
        "NanoBuiltBench",
        "NanoCMTEB",
        "NanoIndicQA",
        "NanoMuPLeR",
        "NanoMTEB-v2",
        *language_nanomteb_benchmarks,
        "NanoMIRACL",
    ]
    assert [component.group_by for component in grouped_overall.benchmark_components] == [
        "task_name",
        "task_name",
        "task_name",
        "benchmark",
        "benchmark",
        "benchmark",
        "benchmark",
        "task_name",
        "benchmark",
        "benchmark",
        "benchmark",
        "benchmark",
        "benchmark",
        "benchmark",
        "benchmark",
        "benchmark",
        "benchmark",
        "benchmark",
        "benchmark",
        "benchmark",
        "benchmark",
        *["benchmark"] * len(language_nanomteb_benchmarks),
        "benchmark",
    ]
    assert config.view_names[: len(expected_overall_benchmarks) + 2] == [
        "Overall",
        "OverallGrouped",
        *expected_overall_benchmarks,
    ]
    assert "NanoCodeSearchNet" not in config.view_names
    assert "NanoBIRCO" in config.view_names
    assert "NanoDAPFAM" in config.view_names
    assert all(benchmark in config.view_names for benchmark in language_nanomteb_benchmarks)
    assert all(benchmark not in config.overall.benchmark_names for benchmark in language_nanomteb_benchmarks)
    assert "NanoCMTEB" in config.view_names
    assert "NanoCMTEB" in config.overall.benchmark_names
    nano_law = config.benchmark_for_view("NanoLaw")
    assert nano_law is not None
    assert "NanoAILACasedocs" in nano_law.excluded_tasks
    mnanobeir = config.benchmark_for_view("MNanoBEIR")
    assert mnanobeir is not None
    assert [group.name for group in mnanobeir.resolved_score_groups] == ["task_mean", "lang_mean"]
    assert mnanobeir.language_filter_mode == "primary_language"
    nano_miracl = config.benchmark_for_view("NanoMIRACL")
    assert nano_miracl is not None
    assert nano_miracl.language_filter_mode == "primary_language"


def test_core_benchmark_view_group_only_contains_primary_core_benchmarks() -> None:
    assert _view_group("NanoMMTEB-v2") == "Core benchmarks"
    assert _view_group("MNanoBEIR") == "Core benchmarks"
    assert _view_group("NanoRTEB") == "Core benchmarks"
    assert _view_group("NanoMLDR") == "Domain-specific"
    assert _view_group("NanoLongEmbed") == "Domain-specific"
    assert _view_group("NanoBIRCO") == "Domain-specific"


def test_language_specific_view_group_includes_official_language_mteb_families() -> None:
    assert _view_group("NanoMTEB-Dutch") == "Language-specific"
    assert _view_group("NanoJMTEB-v2") == "Language-specific"
    assert _view_group("NanoFaMTEB-v2") == "Language-specific"
    assert _view_group("NanoRuMTEB") == "Language-specific"
    assert _view_group("NanoVNMTEB") == "Language-specific"
    assert _view_group("NanoCMTEB") == "Language-specific"
    assert _view_group("NanoIndicQA") == "Domain-specific"
    assert _view_group("NanoMuPLeR") == "Domain-specific"
    assert _view_group("NanoChemTEB") == "Domain-specific"
    assert _view_group("NanoMIRACL") == "Domain-specific"


def test_leaderboard_service_reads_precomputed_rows_when_available(tmp_path: Path) -> None:
    db_path = tmp_path / "results.duckdb"
    con = duckdb.connect(str(db_path))
    try:
        con.execute(
            """
            CREATE TABLE viewer_leaderboard_rows (
                view_name VARCHAR,
                score_target VARCHAR,
                include_quantization_variants BOOLEAN,
                include_truncate_variants BOOLEAN,
                include_rescore_variants BOOLEAN,
                include_other_variants BOOLEAN,
                expected_tasks INTEGER,
                borda_rank DOUBLE,
                mean_rank DOUBLE,
                model_name VARCHAR,
                borda_score DOUBLE,
                mean_score DOUBLE,
                macro_mean DOUBLE,
                micro_mean DOUBLE,
                task_count INTEGER,
                active_parameters BIGINT,
                total_parameters BIGINT,
                max_seq_length INTEGER,
                dtype VARCHAR,
                attn_implementation VARCHAR,
                prompt_summary VARCHAR,
                trust_remote_code BOOLEAN,
                embedding_variant_name VARCHAR,
                embedding_dim INTEGER,
                quantization VARCHAR,
                source_model_name VARCHAR,
                base_score_delta_percent DOUBLE
            )
            """
        )
        con.execute(
            "INSERT INTO viewer_leaderboard_rows VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
            [
                "Overall",
                "all",
                True,
                False,
                False,
                False,
                3,
                1.0,
                1.0,
                "model/a (768 dims, int8)",
                99.0,
                98.0,
                98.0,
                97.0,
                3,
                10,
                12,
                8192,
                "bf16",
                "flash_attention_2",
                "model default",
                True,
                "int8",
                768,
                "int8",
                "model/a",
                -1.0,
            ],
        )
        con.execute(
            """
            CREATE TABLE viewer_leaderboard_language_options (
                view_name VARCHAR,
                score_target VARCHAR,
                include_quantization_variants BOOLEAN,
                include_truncate_variants BOOLEAN,
                include_rescore_variants BOOLEAN,
                include_other_variants BOOLEAN,
                code VARCHAR,
                label VARCHAR,
                task_count INTEGER
            )
            """
        )
        con.executemany(
            "INSERT INTO viewer_leaderboard_language_options VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)",
            [
                ["Overall", "all", True, False, False, False, "ar", "AR", 3],
                ["Overall", "all", True, False, False, False, "en", "EN", 8],
                ["Overall", "all", True, False, False, False, "ja", "Japanese", 3],
            ],
        )
    finally:
        con.close()
    config = ViewerConfig(
        benchmarks=[BenchmarkConfig(name="BenchA")],
        overalls=[OverallConfig(name="Overall", label="Overall", benchmarks=["BenchA"])],
    )

    result = LeaderboardService(duckdb_path=db_path, config=config).get_leaderboard(
        "Overall",
        include_quantization_variants=True,
    )

    assert result.expected_tasks == 3
    assert result.rows[0].model_name == "model/a (768 dims, int8)"
    assert result.rows[0].borda_score == 99.0
    assert result.rows[0].embedding_variant_name == "int8"
    assert [(option.code, option.label, option.task_count) for option in result.available_languages] == [
        ("en", "EN", 8),
        ("ar", "AR", 3),
        ("ja", "Japanese", 3),
    ]


def test_viewer_config_rejects_unknown_group_by(tmp_path: Path) -> None:
    config_dir = tmp_path / "config"
    config_dir.mkdir()
    (config_dir / "benchmarks.yaml").write_text(
        """
benchmarks:
  - name: BenchA
    score_groups:
      - name: invalid
        group_by: language
""".strip(),
        encoding="utf-8",
    )
    (config_dir / "overall.yaml").write_text(
        """
name: Overall
label: Overall
benchmarks:
  - BenchA
""".strip(),
        encoding="utf-8",
    )

    with pytest.raises(ValueError, match="language"):
        load_viewer_config(config_dir)


def test_viewer_config_loads_benchmark_match_patterns(tmp_path: Path) -> None:
    config_dir = tmp_path / "config"
    config_dir.mkdir()
    (config_dir / "benchmarks.yaml").write_text(
        """
benchmarks:
  - name: BenchA
    matches:
      - uploaded/bench-a
""".strip(),
        encoding="utf-8",
    )
    (config_dir / "overall.yaml").write_text(
        """
name: Overall
label: Overall
benchmarks:
  - BenchA
""".strip(),
        encoding="utf-8",
    )

    config = load_viewer_config(config_dir)

    assert config.benchmarks[0].match_patterns == ["uploaded/bench-a"]


def test_index_renders_summary_cards_and_analysis_navigation(tmp_path: Path) -> None:
    from fastapi.testclient import TestClient

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
    (config_dir / "overall.yaml").write_text("name: Overall\nlabel: Overall\nbenchmarks:\n  - BenchA\n", encoding="utf-8")

    app = create_app(store=LocalDuckDbStore(DuckDbLocation(local_path=db_path)), config_dir=config_dir)
    response = TestClient(app).get("/")

    assert response.status_code == 200
    assert "<title>HAKARI-bench leaderboard</title>" in response.text
    assert "HAKARI-bench leaderboard" in response.text
    assert '<p class="text-sm font-medium text-cyan-700">HAKARI-bench leaderboard</p>' not in response.text
    assert (
        "🚧 WIP: This leaderboard is currently under active implementation, "
        "so specifications and data may change significantly."
    ) in response.text
    assert "DuckDB:" not in response.text
    assert str(db_path) not in response.text
    assert "Benchmark coverage" in response.text
    assert "Models" in response.text
    assert re.search(r'<link rel="stylesheet" href="/assets/app\.css\?v=[0-9a-f]{12}">', response.text)
    assert re.search(r'<link rel="icon" type="image/png" href="/assets/favicon\.png\?v=[0-9a-f]{12}">', response.text)
    assert (
        '<meta name="htmx-config" content=\'{"allowEval":false,"allowScriptTags":false,'
        '"includeIndicatorStyles":false}\'>'
    ) in response.text
    assert re.search(r'<script src="/assets/htmx\.min\.js\?v=[0-9a-f]{12}"></script>', response.text)
    assert re.search(r'<script src="/assets/viewer\.js\?v=[0-9a-f]{12}" defer></script>', response.text)
    assert "<script>" not in response.text
    assert "window.__hakariApplyHashQueryState" not in response.text
    assert 'id="leaderboard-loading-toast"' in response.text
    assert "leaderboard-loading-toast fixed bottom-4 right-4" in response.text
    assert 'role="status"' in response.text
    assert 'aria-live="polite"' in response.text
    assert "Loading leaderboard..." in response.text
    assert 'id="hakari-global-tooltip"' in response.text
    assert 'role="tooltip"' in response.text
    assert 'hx-indicator="#leaderboard-loading-toast"' in response.text
    assert 'hx-sync="#leaderboard-panel:replace"' in response.text
    assert "https://cdn.tailwindcss.com" not in response.text
    assert "https://unpkg.com/htmx.org" not in response.text
    assert 'hx-get="/leaderboard?view=Overall' in response.text

    leaderboard_response = TestClient(app).get("/leaderboard?view=BenchA")
    assert leaderboard_response.status_code == 200
    assert "Analysis views" in leaderboard_response.text
    assert "Variant impact" in leaderboard_response.text
    assert "Reranking diagnostics" in leaderboard_response.text
    assert "Dataset diagnostics" in leaderboard_response.text
    assert 'hx-get="/analysis?panel=variants&amp;view=BenchA"' in leaderboard_response.text
    assert 'data-testid="summary-card-models"' in response.text


def test_viewer_serves_static_assets_from_assets_dir(tmp_path: Path) -> None:
    from fastapi.testclient import TestClient

    db_path = tmp_path / "results.duckdb"
    config_dir = tmp_path / "config"
    config_dir.mkdir()
    (config_dir / "benchmarks.yaml").write_text("benchmarks:\n  - name: BenchA\n", encoding="utf-8")
    (config_dir / "overall.yaml").write_text("name: Overall\nlabel: Overall\nbenchmarks:\n  - BenchA\n", encoding="utf-8")
    app = create_app(store=LocalDuckDbStore(DuckDbLocation(local_path=db_path)), config_dir=config_dir)
    client = TestClient(app)

    response = client.get("/assets/favicon.png")

    assert response.status_code == 200
    assert response.headers["content-type"].startswith("image/png")
    assert response.content.startswith(b"\x89PNG\r\n\x1a\n")

    css_response = client.get("/assets/app.css")
    assert css_response.status_code == 200
    assert css_response.headers["content-type"].startswith("text/css")
    assert "prefers-color-scheme:dark" in css_response.text
    assert "color-scheme:light dark" in css_response.text
    assert ".leaderboard-loading-toast.htmx-request" in css_response.text
    assert "hakari-leaderboard-spin" in css_response.text
    assert "[data-leaderboard-pending=true]" in css_response.text
    assert ".global-tooltip" in css_response.text
    assert "z-index:1000" in css_response.text

    htmx_response = client.get("/assets/htmx.min.js")
    assert htmx_response.status_code == 200
    assert "htmx" in htmx_response.text

    viewer_js_response = client.get("/assets/viewer.js")
    assert viewer_js_response.status_code == 200
    assert "javascript" in viewer_js_response.headers["content-type"]
    assert "window.__hakariApplyHashQueryState" in viewer_js_response.text
    assert "window.__hakariSyncHashQueryStateToParent" in viewer_js_response.text
    assert "window.__hakariSetLeaderboardPending" in viewer_js_response.text
    assert "window.__hakariShowTooltip" in viewer_js_response.text
    assert "window.__hakariHideTooltip" in viewer_js_response.text
    assert "window.__hakariPositionTooltip" in viewer_js_response.text
    assert "window.__hakariBindModelDetails" in viewer_js_response.text
    assert "setTimeout(() =>" in viewer_js_response.text
    assert ", 1000);" in viewer_js_response.text
    assert "const queryString = mergedStateQueryString();" in viewer_js_response.text
    assert 'window.parent.postMessage({ queryString: "", hash: hashValue }, "https://huggingface.co")' in viewer_js_response.text
    assert 'panel.setAttribute("hx-get", "/leaderboard?" + queryString);' in viewer_js_response.text
    assert 'document.addEventListener("htmx:beforeRequest"' in viewer_js_response.text
    assert 'document.addEventListener("htmx:afterRequest"' in viewer_js_response.text
    assert 'document.addEventListener("htmx:sendAbort"' in viewer_js_response.text
    assert 'document.addEventListener("htmx:pushedIntoHistory"' in viewer_js_response.text
    assert 'document.addEventListener("htmx:replacedInHistory"' in viewer_js_response.text
    assert 'document.addEventListener("htmx:afterSwap"' in viewer_js_response.text

    legacy_favicon_response = client.get("/favicon.png")
    assert legacy_favicon_response.status_code == 200
    assert legacy_favicon_response.headers["content-type"].startswith("image/png")
    assert legacy_favicon_response.content.startswith(b"\x89PNG\r\n\x1a\n")

    browser_default_favicon_response = client.get("/favicon.ico")
    assert browser_default_favicon_response.status_code == 200
    assert browser_default_favicon_response.headers["content-type"].startswith("image/png")
    assert browser_default_favicon_response.content == response.content


def test_viewer_responses_include_security_headers(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    from fastapi.testclient import TestClient

    db_path = tmp_path / "results.duckdb"
    config_dir = tmp_path / "config"
    config_dir.mkdir()
    (config_dir / "benchmarks.yaml").write_text("benchmarks:\n  - name: BenchA\n", encoding="utf-8")
    (config_dir / "overall.yaml").write_text("name: Overall\nlabel: Overall\nbenchmarks:\n  - BenchA\n", encoding="utf-8")
    monkeypatch.setenv(
        "HAKARI_BENCH_VIEWER_FRAME_ANCESTORS",
        "https://huggingface.co https://*.huggingface.co https://example.com",
    )
    app = create_app(store=LocalDuckDbStore(DuckDbLocation(local_path=db_path)), config_dir=config_dir)
    client = TestClient(app)

    response = client.get("/")

    assert response.status_code == 200
    assert response.headers["x-content-type-options"] == "nosniff"
    assert response.headers["referrer-policy"] == "strict-origin-when-cross-origin"
    assert "camera=()" in response.headers["permissions-policy"]
    assert "microphone=()" in response.headers["permissions-policy"]
    assert "geolocation=()" in response.headers["permissions-policy"]
    assert "default-src 'self'" in response.headers["content-security-policy"]
    assert "script-src 'self'" in response.headers["content-security-policy"]
    assert "style-src 'self'" in response.headers["content-security-policy"]
    assert "'unsafe-inline'" not in response.headers["content-security-policy"]
    assert "img-src 'self' data:" in response.headers["content-security-policy"]
    assert (
        "frame-ancestors https://huggingface.co https://*.huggingface.co https://example.com"
        in response.headers["content-security-policy"]
    )
    assert "x-frame-options" not in response.headers

    asset_response = client.get("/assets/app.css")
    assert asset_response.status_code == 200
    assert asset_response.headers["content-security-policy"] == response.headers["content-security-policy"]


def test_leaderboard_renders_grouped_benchmark_picker_and_sticky_columns(tmp_path: Path) -> None:
    from fastapi.testclient import TestClient

    db_path = tmp_path / "results.duckdb"
    _write_task_results(
        db_path,
        [
            ("model/a", "NanoMTEB-Japanese", "bench/a", "BenchA", "a1", "a1", "a1", 0.90, 10, 12, 8192),
            ("model/b", "NanoMTEB-Japanese", "bench/a", "BenchA", "a1", "a1", "a1", 0.80, 10, 12, 8192),
        ],
    )
    config_dir = tmp_path / "config"
    config_dir.mkdir()
    (config_dir / "benchmarks.yaml").write_text(
        "benchmarks:\n  - name: NanoMTEB-Japanese\n  - name: NanoRTEB\n  - name: NanoMedical\n",
        encoding="utf-8",
    )
    (config_dir / "overall.yaml").write_text(
        "name: Overall\nlabel: Overall\nbenchmarks:\n  - NanoMTEB-Japanese\n",
        encoding="utf-8",
    )

    app = create_app(store=LocalDuckDbStore(DuckDbLocation(local_path=db_path)), config_dir=config_dir)
    response = TestClient(app).get("/leaderboard?view=NanoMTEB-Japanese")

    assert response.status_code == 200
    assert "Benchmark groups" in response.text
    assert response.text.index("Target") < response.text.index("Overall")
    assert 'data-testid="primary-benchmark-column"' in response.text
    primary_column = response.text.split('data-testid="primary-benchmark-column"', 1)[1].split('data-testid="secondary-benchmark-column"', 1)[0]
    assert "Target" in primary_column
    assert "Overall" in primary_column
    assert "Core benchmarks" in primary_column
    assert "All" in response.text
    assert "Reranking" in response.text
    assert "data-tooltip=" in response.text
    assert "data-tooltip-placement=\"left\"" in response.text
    assert "full-corpus retrieval nDCG@10" in response.text
    assert "BM25 top-100 reranking nDCG@10" in response.text
    assert 'data-leaderboard-control="true"' in response.text
    assert response.text.count('hx-indicator="#leaderboard-loading-toast"') >= 6
    assert response.text.count('hx-sync="#leaderboard-panel:replace"') >= 6
    assert 'hx-get="/leaderboard?view=NanoMTEB-Japanese&amp;sort=borda_rank&amp;direction=asc&amp;group=task&amp;target=reranking"' in response.text
    assert "Language-specific" in response.text
    assert "Domain-specific" in response.text
    assert "sticky left-0" in response.text
    assert "z-20" in response.text


def test_leaderboard_target_reranking_uses_bm25_top100_rerank_scores(tmp_path: Path) -> None:
    from fastapi.testclient import TestClient

    db_path = tmp_path / "results.duckdb"
    _write_task_results(
        db_path,
        [
            ("model/a", "BenchA", "bench/a", "BenchA", "a1", "a1", "BenchA::a1", 0.90, 10, 12, 8192),
            ("model/b", "BenchA", "bench/a", "BenchA", "a1", "a1", "BenchA::a1", 0.80, 10, 12, 8192),
            ("model/a", "BenchA", "bench/a", "BenchA", "a2", "a2", "BenchA::a2", 0.40, 10, 12, 8192),
            ("model/b", "BenchA", "bench/a", "BenchA", "a2", "a2", "BenchA::a2", 0.30, 10, 12, 8192),
        ],
        task_diagnostics_rows=[
            ("model/a", "BenchA", "bench/a", "a1", "BenchA::a1", 0.90, 0.20, -0.70, "available", 100, "dataset_candidate_subset", "bm25", "dataset", 1.0, 1.0),
            ("model/b", "BenchA", "bench/a", "a1", "BenchA::a1", 0.80, 0.90, 0.10, "available", 100, "dataset_candidate_subset", "bm25", "dataset", 1.0, 1.0),
            ("model/a", "BenchA", "bench/a", "a2", "BenchA::a2", 0.40, 0.20, -0.20, "available", 100, "dataset_candidate_subset", "bm25", "dataset", 1.0, 1.0),
            ("model/b", "BenchA", "bench/a", "a2", "BenchA::a2", 0.30, 0.90, 0.60, "available", 100, "dataset_candidate_subset", "bm25", "dataset", 1.0, 1.0),
        ],
    )
    config_dir = tmp_path / "config"
    config_dir.mkdir()
    (config_dir / "benchmarks.yaml").write_text("benchmarks:\n  - name: BenchA\n", encoding="utf-8")
    (config_dir / "overall.yaml").write_text("name: Overall\nlabel: Overall\nbenchmarks:\n  - BenchA\n", encoding="utf-8")

    service = LeaderboardService(duckdb_path=db_path, config=load_viewer_config(config_dir))

    all_result = service.get_leaderboard("BenchA")
    rerank_result = service.get_leaderboard("BenchA", score_target="reranking")

    assert [row.model_name for row in all_result.rows] == ["model/a", "model/b"]
    assert all_result.rows[0].mean_score == pytest.approx(65.0)
    assert [row.model_name for row in rerank_result.rows] == ["model/b", "model/a"]
    assert rerank_result.rows[0].mean_score == pytest.approx(90.0)
    assert rerank_result.score_target == "reranking"

    app = create_app(store=LocalDuckDbStore(DuckDbLocation(local_path=db_path)), config_dir=config_dir)
    response = TestClient(app).get("/leaderboard?view=BenchA&target=reranking")

    assert response.status_code == 200
    assert "target=reranking" in response.text
    assert response.text.index("model/b") < response.text.index("model/a")


def test_leaderboard_service_logs_request_and_phase_timing(
    tmp_path: Path,
    caplog: pytest.LogCaptureFixture,
) -> None:
    db_path = tmp_path / "results.duckdb"
    _write_task_results(
        db_path,
        [
            ("model/a", "BenchA", "bench/a", "BenchA", "a1", "a1", "BenchA::a1", 0.90, 10, 12, 8192),
            ("model/b", "BenchA", "bench/a", "BenchA", "a1", "a1", "BenchA::a1", 0.80, 10, 12, 8192),
        ],
    )
    config_dir = tmp_path / "config"
    config_dir.mkdir()
    (config_dir / "benchmarks.yaml").write_text("benchmarks:\n  - name: BenchA\n", encoding="utf-8")
    (config_dir / "overall.yaml").write_text("name: Overall\nlabel: Overall\nbenchmarks:\n  - BenchA\n", encoding="utf-8")
    service = LeaderboardService(duckdb_path=db_path, config=load_viewer_config(config_dir))

    with caplog.at_level(logging.INFO, logger="hakari_bench.viewer"):
        result = service.get_leaderboard("BenchA")

    assert len(result.rows) == 2
    messages = [record.getMessage() for record in caplog.records]
    assert any(
        "viewer.leaderboard.phase" in message
        and "operation=load_task_scores" in message
        and "task_score_count=2" in message
        for message in messages
    )
    assert any(
        "viewer.leaderboard.request" in message
        and "view=BenchA" in message
        and "leaderboard_row_count=2" in message
        for message in messages
    )


def test_leaderboard_service_does_not_validate_pydantic_records_on_hot_path(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    from hakari_bench.viewer.data import TaskResultRecord

    db_path = tmp_path / "results.duckdb"
    _write_task_results(
        db_path,
        [
            ("model/a", "BenchA", "bench/a", "BenchA", "a1", "a1", "BenchA::a1", 0.90, 10, 12, 8192),
            ("model/b", "BenchA", "bench/a", "BenchA", "a1", "a1", "BenchA::a1", 0.80, 10, 12, 8192),
        ],
    )
    config_dir = tmp_path / "config"
    config_dir.mkdir()
    (config_dir / "benchmarks.yaml").write_text("benchmarks:\n  - name: BenchA\n", encoding="utf-8")
    (config_dir / "overall.yaml").write_text("name: Overall\nlabel: Overall\nbenchmarks:\n  - BenchA\n", encoding="utf-8")

    def fail_model_validate(*args: object, **kwargs: object) -> None:
        msg = "Pydantic validation should not run on the leaderboard hot path"
        raise AssertionError(msg)

    monkeypatch.setattr(TaskResultRecord, "model_validate", fail_model_validate)

    result = LeaderboardService(duckdb_path=db_path, config=load_viewer_config(config_dir)).get_leaderboard("BenchA")

    assert [row.model_name for row in result.rows] == ["model/a", "model/b"]


def test_leaderboard_service_reuses_task_score_cache_across_instances(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    from hakari_bench.viewer.data import TaskResultsRepository

    _clear_task_score_cache()
    db_path = tmp_path / "results.duckdb"
    _write_task_results(
        db_path,
        [
            ("model/a", "BenchA", "bench/a", "BenchA", "a1", "a1", "BenchA::a1", 0.90, 10, 12, 8192),
            ("model/b", "BenchA", "bench/a", "BenchA", "a1", "a1", "BenchA::a1", 0.80, 10, 12, 8192),
        ],
    )
    config_dir = tmp_path / "config"
    config_dir.mkdir()
    (config_dir / "benchmarks.yaml").write_text("benchmarks:\n  - name: BenchA\n", encoding="utf-8")
    (config_dir / "overall.yaml").write_text("name: Overall\nlabel: Overall\nbenchmarks:\n  - BenchA\n", encoding="utf-8")
    config = load_viewer_config(config_dir)
    fetch_count = 0
    original_fetch = TaskResultsRepository.fetch_task_result_rows

    def counted_fetch(
        self: TaskResultsRepository,
        *,
        benchmarks: list[str],
        score_target: str = "all",
        include_embedding_variants: bool,
        variant_display_flags: VariantDisplayFlags | None = None,
    ):
        nonlocal fetch_count
        fetch_count += 1
        return original_fetch(
            self,
            benchmarks=benchmarks,
            score_target=score_target,
            include_embedding_variants=include_embedding_variants,
            variant_display_flags=variant_display_flags,
        )

    monkeypatch.setattr(TaskResultsRepository, "fetch_task_result_rows", counted_fetch)

    first = LeaderboardService(duckdb_path=db_path, config=config).get_leaderboard("BenchA")
    second = LeaderboardService(duckdb_path=db_path, config=config).get_leaderboard("BenchA")

    assert [row.model_name for row in first.rows] == ["model/a", "model/b"]
    assert [row.model_name for row in second.rows] == ["model/a", "model/b"]
    assert fetch_count == 1
    _clear_task_score_cache()


def test_leaderboard_service_cache_invalidates_when_duckdb_file_changes(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    from hakari_bench.viewer.data import TaskResultsRepository

    _clear_task_score_cache()
    db_path = tmp_path / "results.duckdb"
    _write_task_results(
        db_path,
        [
            ("model/a", "BenchA", "bench/a", "BenchA", "a1", "a1", "BenchA::a1", 0.90, 10, 12, 8192),
            ("model/b", "BenchA", "bench/a", "BenchA", "a1", "a1", "BenchA::a1", 0.80, 10, 12, 8192),
        ],
    )
    config_dir = tmp_path / "config"
    config_dir.mkdir()
    (config_dir / "benchmarks.yaml").write_text("benchmarks:\n  - name: BenchA\n", encoding="utf-8")
    (config_dir / "overall.yaml").write_text("name: Overall\nlabel: Overall\nbenchmarks:\n  - BenchA\n", encoding="utf-8")
    config = load_viewer_config(config_dir)
    fetch_count = 0
    original_fetch = TaskResultsRepository.fetch_task_result_rows

    def counted_fetch(
        self: TaskResultsRepository,
        *,
        benchmarks: list[str],
        score_target: str = "all",
        include_embedding_variants: bool,
        variant_display_flags: VariantDisplayFlags | None = None,
    ):
        nonlocal fetch_count
        fetch_count += 1
        return original_fetch(
            self,
            benchmarks=benchmarks,
            score_target=score_target,
            include_embedding_variants=include_embedding_variants,
            variant_display_flags=variant_display_flags,
        )

    monkeypatch.setattr(TaskResultsRepository, "fetch_task_result_rows", counted_fetch)

    first = LeaderboardService(duckdb_path=db_path, config=config).get_leaderboard("BenchA")
    con = duckdb.connect(str(db_path))
    try:
        row = _viewer_task_result_row(
            ("model/c", "BenchA", "bench/a", "BenchA", "a1", "a1", "BenchA::a1", 0.70, 30, 36, 2048),
            language=None,
            languages=[],
        )
        con.execute(
            "INSERT INTO viewer_task_results VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
            row,
        )
    finally:
        con.close()
    os.utime(db_path)
    second = LeaderboardService(duckdb_path=db_path, config=config).get_leaderboard("BenchA")

    assert len(first.rows) == 2
    assert len(second.rows) == 3
    assert fetch_count == 2
    _clear_task_score_cache()


def test_leaderboard_endpoint_logs_request_and_render_timing(
    tmp_path: Path,
    caplog: pytest.LogCaptureFixture,
) -> None:
    from fastapi.testclient import TestClient

    db_path = tmp_path / "results.duckdb"
    _write_task_results(
        db_path,
        [
            ("model/a", "BenchA", "bench/a", "BenchA", "a1", "a1", "BenchA::a1", 0.90, 10, 12, 8192),
            ("model/b", "BenchA", "bench/a", "BenchA", "a1", "a1", "BenchA::a1", 0.80, 10, 12, 8192),
        ],
    )
    config_dir = tmp_path / "config"
    config_dir.mkdir()
    (config_dir / "benchmarks.yaml").write_text("benchmarks:\n  - name: BenchA\n", encoding="utf-8")
    (config_dir / "overall.yaml").write_text("name: Overall\nlabel: Overall\nbenchmarks:\n  - BenchA\n", encoding="utf-8")
    app = create_app(store=LocalDuckDbStore(DuckDbLocation(local_path=db_path)), config_dir=config_dir)

    with caplog.at_level(logging.INFO, logger="hakari_bench.viewer"):
        response = TestClient(app).get("/leaderboard?view=BenchA")

    assert response.status_code == 200
    messages = [record.getMessage() for record in caplog.records]
    assert any(
        "viewer.http.request" in message
        and "route=leaderboard" in message
        and "leaderboard_row_count=2" in message
        for message in messages
    )
    assert any("viewer.render" in message and "operation=render_leaderboard" in message for message in messages)


def test_leaderboard_endpoint_uses_gzip_for_large_html_responses(tmp_path: Path) -> None:
    from fastapi.testclient import TestClient

    db_path = tmp_path / "results.duckdb"
    _write_task_results(
        db_path,
        [
            (f"model/{index}", "BenchA", "bench/a", "BenchA", "a1", "a1", "BenchA::a1", 0.90, 10, 12, 8192)
            for index in range(20)
        ],
    )
    config_dir = tmp_path / "config"
    config_dir.mkdir()
    (config_dir / "benchmarks.yaml").write_text("benchmarks:\n  - name: BenchA\n", encoding="utf-8")
    (config_dir / "overall.yaml").write_text("name: Overall\nlabel: Overall\nbenchmarks:\n  - BenchA\n", encoding="utf-8")
    app = create_app(store=LocalDuckDbStore(DuckDbLocation(local_path=db_path)), config_dir=config_dir)

    response = TestClient(app).get("/leaderboard?view=BenchA", headers={"Accept-Encoding": "gzip"})

    assert response.status_code == 200
    assert response.headers["content-encoding"] == "gzip"


def test_viewer_config_rejects_unknown_yaml_keys(tmp_path: Path) -> None:
    config_dir = tmp_path / "config"
    config_dir.mkdir()
    (config_dir / "benchmarks.yaml").write_text(
        """
benchmarks:
  - name: BenchA
    typo: true
""".strip(),
        encoding="utf-8",
    )
    (config_dir / "overall.yaml").write_text(
        """
name: Overall
label: Overall
benchmarks:
  - BenchA
""".strip(),
        encoding="utf-8",
    )

    with pytest.raises(ValueError, match="typo"):
        load_viewer_config(config_dir)


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


def test_leaderboard_language_filter_recomputes_ranking_for_matching_tasks(tmp_path: Path) -> None:
    db_path = tmp_path / "results.duckdb"
    _write_task_results(
        db_path,
        [
            ("model/a", "BenchA", "bench/a", "BenchA", "en", "task-en", "task-en", 0.90, 10, 12, 8192),
            ("model/a", "BenchA", "bench/a", "BenchA", "ja", "task-ja", "task-ja", 0.40, 10, 12, 8192),
            ("model/b", "BenchA", "bench/a", "BenchA", "en", "task-en", "task-en", 0.80, 20, 24, 4096),
            ("model/b", "BenchA", "bench/a", "BenchA", "ja", "task-ja", "task-ja", 0.95, 20, 24, 4096),
        ],
        dataset_metadata_rows=[
            ("BenchA", "bench/a", "BenchA", "en", "task-en", "task-en", "en", ["en"]),
            ("BenchA", "bench/a", "BenchA", "ja", "task-ja", "task-ja", "ja", ["ja"]),
        ],
    )
    config_dir = tmp_path / "config"
    config_dir.mkdir()
    (config_dir / "benchmarks.yaml").write_text("benchmarks:\n  - name: BenchA\n", encoding="utf-8")
    (config_dir / "overall.yaml").write_text("name: Overall\nlabel: Overall\nbenchmarks:\n  - BenchA\n", encoding="utf-8")

    service = LeaderboardService(duckdb_path=db_path, config=load_viewer_config(config_dir))
    result = service.get_leaderboard("BenchA", language_filters=("ja",))

    assert result.expected_tasks == 1
    assert result.selected_languages == ("ja",)
    assert [(option.code, option.task_count) for option in result.available_languages] == [("en", 1), ("ja", 1)]
    assert [row.model_name for row in result.rows] == ["model/b", "model/a"]
    assert [row.task_count for row in result.rows] == [1, 1]


def test_viewer_renders_language_pages_and_scrollable_language_filter(tmp_path: Path) -> None:
    from fastapi.testclient import TestClient

    db_path = tmp_path / "results.duckdb"
    rows = []
    metadata_rows = []
    for index, lang in enumerate(["en", "ja", "de", "fr", "es", "ko", "th", "vi", "pl", "ru", "zh", "ar", "fa"]):
        task_key = f"task-{lang}"
        rows.append(("model/a", "BenchA", "bench/a", "BenchA", lang, task_key, task_key, 0.50 + index / 100, 10, 12, 8192))
        rows.append(("model/b", "BenchA", "bench/a", "BenchA", lang, task_key, task_key, 0.40 + index / 100, 20, 24, 4096))
        metadata_rows.append(("BenchA", "bench/a", "BenchA", lang, task_key, task_key, lang, [lang]))
    _write_task_results(db_path, rows, dataset_metadata_rows=metadata_rows)
    config_dir = tmp_path / "config"
    config_dir.mkdir()
    (config_dir / "benchmarks.yaml").write_text("benchmarks:\n  - name: BenchA\n", encoding="utf-8")
    (config_dir / "overall.yaml").write_text("name: Overall\nlabel: Overall\nbenchmarks:\n  - BenchA\n", encoding="utf-8")

    app = create_app(store=LocalDuckDbStore(DuckDbLocation(local_path=db_path)), config_dir=config_dir)
    response = TestClient(app).get("/leaderboard?view=BenchA&lang_filter=ja")

    assert response.status_code == 200
    assert "Language pages" in response.text
    assert "Languages (13)" in response.text
    assert "max-h-72" in response.text
    assert 'name="lang_filter" value="ja" class="h-4 w-4 accent-cyan-700" checked' in response.text
    assert 'hx-push-url="/?view=BenchA&amp;sort=borda_rank&amp;direction=asc&amp;group=task&amp;lang_filter=en"' in response.text
    assert 'data-language-page="ja"' in response.text
    assert 'data-shown-count="2"' in response.text
    assert "2 shown / 2 complete models / 1 tasks" in response.text


def test_grouped_overall_uses_configured_mean_units_before_borda(tmp_path: Path) -> None:
    db_path = tmp_path / "results.duckdb"
    _write_task_results(
        db_path,
        [
            ("model/a", "BenchTask", "bench/task-ja", "BenchTask-ja", "ja", "task1", "task-ja-1", 0.80, 10, 12, 8192),
            ("model/a", "BenchTask", "bench/task-en", "BenchTask-en", "en", "task1", "task-en-1", 0.60, 10, 12, 8192),
            ("model/a", "BenchTask", "bench/task-ja", "BenchTask-ja", "ja", "task2", "task-ja-2", 0.50, 10, 12, 8192),
            ("model/a", "BenchMean", "bench/mean", "BenchMean", "m1", "m1", "mean-1", 0.90, 10, 12, 8192),
            ("model/a", "BenchMean", "bench/mean", "BenchMean", "m2", "m2", "mean-2", 0.70, 10, 12, 8192),
            ("model/b", "BenchTask", "bench/task-ja", "BenchTask-ja", "ja", "task1", "task-ja-1", 0.60, 20, 24, 4096),
            ("model/b", "BenchTask", "bench/task-en", "BenchTask-en", "en", "task1", "task-en-1", 0.40, 20, 24, 4096),
            ("model/b", "BenchTask", "bench/task-ja", "BenchTask-ja", "ja", "task2", "task-ja-2", 0.90, 20, 24, 4096),
            ("model/b", "BenchMean", "bench/mean", "BenchMean", "m1", "m1", "mean-1", 0.50, 20, 24, 4096),
            ("model/b", "BenchMean", "bench/mean", "BenchMean", "m2", "m2", "mean-2", 0.50, 20, 24, 4096),
            ("model/incomplete", "BenchTask", "bench/task-ja", "BenchTask-ja", "ja", "task1", "task-ja-1", 1.00, 30, 36, 2048),
            ("model/incomplete", "BenchTask", "bench/task-en", "BenchTask-en", "en", "task1", "task-en-1", 1.00, 30, 36, 2048),
            ("model/incomplete", "BenchTask", "bench/task-ja", "BenchTask-ja", "ja", "task2", "task-ja-2", 1.00, 30, 36, 2048),
            ("model/incomplete", "BenchMean", "bench/mean", "BenchMean", "m1", "m1", "mean-1", 1.00, 30, 36, 2048),
        ],
    )
    config_dir = tmp_path / "config"
    config_dir.mkdir()
    (config_dir / "benchmarks.yaml").write_text(
        """
benchmarks:
  - name: BenchTask
  - name: BenchMean
""".strip(),
        encoding="utf-8",
    )
    (config_dir / "overall.yaml").write_text(
        """
overalls:
  - name: Overall
    label: Overall
    benchmarks:
      - BenchTask
      - BenchMean
  - name: OverallGrouped
    label: Overall Grouped
    benchmarks:
      - name: BenchTask
        group_by: task_name
      - name: BenchMean
        group_by: benchmark
""".strip(),
        encoding="utf-8",
    )

    service = LeaderboardService(duckdb_path=db_path, config=load_viewer_config(config_dir))
    assert service.get_leaderboard("Overall").metric_columns == []
    result = service.get_leaderboard("OverallGrouped", show_task_scores=True)

    assert result.expected_tasks == 3
    assert [row.model_name for row in result.rows] == ["model/a", "model/b"]
    by_model = {row.model_name: row for row in result.rows}
    assert by_model["model/a"].task_count == 3
    assert by_model["model/a"].borda_score == 100 * 2 / 3
    assert by_model["model/b"].borda_score == 100 / 3
    assert by_model["model/a"].micro_mean == (70 + 50 + 80) / 3
    assert by_model["model/a"].macro_mean == 70.0
    assert result.metric_columns == [
        "BenchMean::BenchMean",
        "BenchTask::task1",
        "BenchTask::task2",
    ]
    assert by_model["model/a"].metric_values == {
        "BenchMean::BenchMean": 80.0,
        "BenchTask::task1": 70.0,
        "BenchTask::task2": 50.0,
    }

    from fastapi.testclient import TestClient

    app = create_app(store=LocalDuckDbStore(DuckDbLocation(local_path=db_path)), config_dir=config_dir)
    response = TestClient(app).get("/leaderboard?view=OverallGrouped&task_scores=1")

    assert response.status_code == 200
    assert "Overall Grouped" in response.text
    assert "BenchMean::BenchMean" in response.text
    assert "BenchTask::task1" in response.text
    assert "BenchTask::task2" in response.text
    assert "metric%3ABenchTask%3A%3Atask1" in response.text


def test_configured_excluded_tasks_are_not_used_in_leaderboards(tmp_path: Path) -> None:
    db_path = tmp_path / "results.duckdb"
    _write_task_results(
        db_path,
        [
            ("model/a", "BenchA", "bench/a", "BenchA", "keep", "keep", "BenchA::keep", 0.90, 10, 12, 8192),
            ("model/a", "BenchA", "bench/a", "BenchA", "drop", "drop", "BenchA::drop", 0.10, 10, 12, 8192),
            ("model/a", "BenchB", "bench/b", "BenchB", "b1", "b1", "BenchB::b1", 0.80, 10, 12, 8192),
            ("model/b", "BenchA", "bench/a", "BenchA", "keep", "keep", "BenchA::keep", 0.70, 20, 24, 4096),
            ("model/b", "BenchA", "bench/a", "BenchA", "drop", "drop", "BenchA::drop", 1.00, 20, 24, 4096),
            ("model/b", "BenchB", "bench/b", "BenchB", "b1", "b1", "BenchB::b1", 0.60, 20, 24, 4096),
        ],
    )
    config_dir = tmp_path / "config"
    config_dir.mkdir()
    (config_dir / "benchmarks.yaml").write_text(
        """
benchmarks:
  - name: BenchA
    excluded_tasks:
      - drop
  - name: BenchB
""".strip(),
        encoding="utf-8",
    )
    (config_dir / "overall.yaml").write_text(
        """
overalls:
  - name: Overall
    label: Overall
    benchmarks:
      - BenchA
      - BenchB
  - name: OverallGrouped
    label: Overall Grouped
    benchmarks:
      - name: BenchA
        group_by: benchmark
      - name: BenchB
        group_by: benchmark
""".strip(),
        encoding="utf-8",
    )

    service = LeaderboardService(duckdb_path=db_path, config=load_viewer_config(config_dir))
    bench_result = service.get_leaderboard("BenchA", show_task_scores=True)
    overall_result = service.get_leaderboard("Overall")
    grouped_result = service.get_leaderboard("OverallGrouped")

    assert bench_result.expected_tasks == 1
    assert bench_result.metric_columns == ["keep"]
    assert bench_result.rows[0].model_name == "model/a"
    assert overall_result.expected_tasks == 2
    assert overall_result.rows[0].micro_mean == 85.0
    assert grouped_result.expected_tasks == 2
    assert grouped_result.rows[0].micro_mean == 85.0


def test_viewer_can_include_embedding_variants_in_ranking(tmp_path: Path) -> None:
    from fastapi.testclient import TestClient

    db_path = tmp_path / "results.duckdb"
    _write_task_results(
        db_path,
        [
            ("model/a", "BenchA", "bench/a", "BenchA", "a1", "a1", "a1", 0.90, 10, 12, 8192, None, 768, None),
            ("model/a", "BenchA", "bench/a", "BenchA", "a1", "a1", "a1", 0.80, 10, 12, 8192, "quantize_uint8_docs", 768, "uint8"),
            ("model/a", "BenchA", "bench/a", "BenchA", "a1", "a1", "a1", 0.83, 10, 12, 8192, "truncate_dim_384", 384, None),
            ("model/a", "BenchA", "bench/a", "BenchA", "a1", "a1", "a1", 0.85, 10, 12, 8192, "truncate_dim_512", 512, None),
            ("model/a", "BenchA", "bench/a", "BenchA", "a1", "a1", "a1", 0.82, 10, 12, 8192, "truncate_dim_256_quantize_int8_docs", 256, "int8"),
            ("model/a", "BenchA", "bench/a", "BenchA", "a1", "a1", "a1", 0.81, 10, 12, 8192, "binary_rescore", 768, "binary"),
            ("model/a", "BenchA", "bench/a", "BenchA", "a1", "a1", "a1", 0.75, 10, 12, 8192, "custom_variant", 2048, None),
            ("model/b", "BenchA", "bench/a", "BenchA", "a1", "a1", "a1", 0.70, 20, 24, 4096, None, 512, None),
        ],
        include_embedding_variant_columns=True,
    )
    config_dir = tmp_path / "config"
    config_dir.mkdir()
    (config_dir / "benchmarks.yaml").write_text("benchmarks:\n  - name: BenchA\n", encoding="utf-8")
    (config_dir / "overall.yaml").write_text("name: Overall\nlabel: Overall\nbenchmarks:\n  - BenchA\n", encoding="utf-8")

    service = LeaderboardService(duckdb_path=db_path, config=load_viewer_config(config_dir))
    base_result = service.get_leaderboard("BenchA")
    quantization_result = service.get_leaderboard("BenchA", include_quantization_variants=True)
    truncate_result = service.get_leaderboard("BenchA", include_truncate_variants=True)
    all_variant_result = service.get_leaderboard(
        "BenchA",
        include_quantization_variants=True,
        include_truncate_variants=True,
    )
    rescore_result = service.get_leaderboard("BenchA", include_rescore_variants=True)
    other_variant_result = service.get_leaderboard("BenchA", include_other_variants=True)

    assert [row.model_name for row in base_result.rows] == ["model/a", "model/b"]
    assert [row.model_name for row in quantization_result.rows] == [
        "model/a (768 dims)",
        "model/a (768 dims, uint8)",
        "model/b (512 dims)",
    ]
    assert all("rescore" not in row.model_name for row in quantization_result.rows)
    assert all("256 dims" not in row.model_name for row in quantization_result.rows)
    assert [row.model_name for row in truncate_result.rows] == [
        "model/a (768 dims)",
        "model/a (512 dims)",
        "model/a (384 dims)",
        "model/b (512 dims)",
    ]
    assert all("int8" not in row.model_name for row in truncate_result.rows)
    assert [row.model_name for row in all_variant_result.rows] == [
        "model/a (768 dims)",
        "model/a (512 dims)",
        "model/a (384 dims)",
        "model/a (256 dims, int8)",
        "model/a (768 dims, uint8)",
        "model/b (512 dims)",
    ]
    assert all_variant_result.rows[3].embedding_dim == 256
    assert all_variant_result.rows[3].quantization == "int8"
    delta_by_model = {row.model_name: row.base_score_delta_percent for row in quantization_result.rows}
    assert delta_by_model == {
        "model/a (768 dims)": None,
        "model/a (768 dims, uint8)": pytest.approx(-11.1111111111),
        "model/b (512 dims)": None,
    }
    assert [row.model_name for row in rescore_result.rows] == [
        "model/a (768 dims)",
        "model/a (768 dims, binary)",
        "model/b (512 dims)",
    ]
    assert [row.model_name for row in other_variant_result.rows] == [
        "model/a (768 dims)",
        "model/a (2048 dims)",
        "model/b (512 dims)",
    ]

    app = create_app(store=LocalDuckDbStore(DuckDbLocation(local_path=db_path)), config_dir=config_dir)
    response = TestClient(app).get("/leaderboard?view=BenchA&quantization=1&model_filter=model%2Fb")

    assert response.status_code == 200
    assert "Display:" not in response.text
    assert "Columns:" in response.text
    assert "Include variants:" in response.text
    assert "Other variants" in response.text
    assert "Filters:" in response.text
    assert '<div class="mt-3 flex flex-wrap items-start gap-3">' in response.text
    assert ">Dims</summary>" in response.text
    assert ">Quantization</summary>" in response.text
    assert "grid-cols-2" in response.text
    assert "sm:grid-cols-3" in response.text
    assert response.text.count(">All</button>") == 5
    assert response.text.count(">None</button>") == 5
    assert 'id="column-controls"' in response.text
    assert 'id="variant-controls"' in response.text
    assert 'id="filter-controls"' in response.text
    assert 'id="facet-filters"' in response.text
    assert 'from:input[type=' not in response.text
    assert 'hx-trigger="change, submit"' in response.text
    assert 'hx-include="#display-controls"' not in response.text
    assert "Truncate dims" in response.text
    assert "Rescore" in response.text
    assert 'id="model-filter-input"' in response.text
    assert 'name="model_filter"' in response.text
    assert "Apply" in response.text
    assert 'value="model/b"' in response.text
    assert "&quot;ranking_model_name&quot;:&quot;model/a (768 dims, uint8)&quot;" in response.text
    assert "model/a" in response.text
    assert "bg-cyan-50" in response.text
    assert "768d" in response.text
    assert "bg-amber-50" in response.text
    assert "uint8" in response.text
    assert "binary_rescore" not in response.text
    assert "Δ vs Base" in response.text
    assert "-11.1%" in response.text
    assert "-8.9%" not in response.text
    assert 'data-filter-hidden="true"' in response.text
    assert "Dims" in response.text
    assert "Quantization" in response.text
    assert "delay:700ms" not in response.text
    assert "<script>" not in response.text
    assert "htmx:afterSwap" not in response.text
    assert "window.__hakariRestoreModelFilterFocus" not in response.text
    assert 'name="dim_filter" value="512" class="h-4 w-4 accent-cyan-700" checked' in response.text
    assert 'name="quant_filter" value="__none__" class="h-4 w-4 accent-cyan-700" checked' in response.text

    base_head = render_table_head(result=base_result, sort="borda_rank", direction="asc")
    quantization_head = render_table_head(result=quantization_result, sort="borda_rank", direction="asc")
    assert ">Quantization</span>" not in base_head
    assert ">Quantization</span>" in quantization_head

    short_filter_response = TestClient(app).get("/leaderboard?view=BenchA&quantization=1&model_filter=mo")

    assert short_filter_response.status_code == 200
    assert 'value="mo"' in short_filter_response.text
    assert 'data-filter-hidden="true"' not in short_filter_response.text

    facet_response = TestClient(app).get(
        "/leaderboard?view=BenchA&quantization=1&truncate=1&other_variant=1"
        "&filters=1&dim_filter=768&dim_filter=1025%2B&quant_filter=uint8"
    )

    assert facet_response.status_code == 200
    assert 'name="other_variant" value="1" class="h-4 w-4 accent-cyan-700" checked' in facet_response.text
    assert 'name="dim_filter" value="768" class="h-4 w-4 accent-cyan-700" checked' in facet_response.text
    assert 'name="dim_filter" value="512" class="h-4 w-4 accent-cyan-700" checked' not in facet_response.text
    assert "1025~ dims" in facet_response.text
    assert 'name="quant_filter" value="uint8" class="h-4 w-4 accent-cyan-700" checked' in facet_response.text
    assert 'name="quant_filter" value="__none__" class="h-4 w-4 accent-cyan-700" checked' not in facet_response.text
    assert "dim_filter=768" in facet_response.text
    assert "dim_filter=1025%2B" in facet_response.text
    assert "quant_filter=uint8" in facet_response.text
    assert 'data-filter-hidden="true"' in facet_response.text

    explicit_truncate_off_response = TestClient(app).get(
        "/leaderboard?view=BenchA&filters=1&dim_filter=384&quant_filter=__none__"
    )

    assert explicit_truncate_off_response.status_code == 200
    assert 'name="truncate" value="1" class="h-4 w-4 accent-cyan-700" checked' not in explicit_truncate_off_response.text
    assert "384 dims" not in explicit_truncate_off_response.text

    explicit_quantization_off_response = TestClient(app).get(
        "/leaderboard?view=BenchA&filters=1&dim_filter=768&quant_filter=uint8"
    )

    assert explicit_quantization_off_response.status_code == 200
    assert (
        'name="quantization" value="1" class="h-4 w-4 accent-cyan-700" checked'
        not in explicit_quantization_off_response.text
    )
    assert ">uint8</td>" not in explicit_quantization_off_response.text

    rescore_response = TestClient(app).get("/leaderboard?view=BenchA&rescore=1")

    assert rescore_response.status_code == 200
    assert 'name="rescore" value="1" class="h-4 w-4 accent-cyan-700" checked' in rescore_response.text
    assert "binary_rescore" in rescore_response.text
    assert "Δ vs Base" not in rescore_response.text


def test_base_score_delta_percent_can_be_positive() -> None:
    rows = compute_leaderboard_rows(
        [
            TaskScore(
                "model/a (768 dims)",
                "BenchA",
                "bench/a",
                "BenchA",
                "a1",
                "a1",
                "a1",
                0.50,
                None,
                None,
                None,
                source_model_name="model/a",
            ),
            TaskScore(
                "model/a (768 dims, uint8)",
                "BenchA",
                "bench/a",
                "BenchA",
                "a1",
                "a1",
                "a1",
                0.55,
                None,
                None,
                None,
                embedding_variant_name="quantize_uint8_docs",
                embedding_dim=768,
                quantization="uint8",
                source_model_name="model/a",
            ),
            TaskScore(
                "model/a (768 dims)",
                "BenchA",
                "bench/a",
                "BenchA",
                "a2",
                "a2",
                "a2",
                0.50,
                None,
                None,
                None,
                source_model_name="model/a",
            ),
            TaskScore(
                "model/a (768 dims, uint8)",
                "BenchA",
                "bench/a",
                "BenchA",
                "a2",
                "a2",
                "a2",
                0.55,
                None,
                None,
                None,
                embedding_variant_name="quantize_uint8_docs",
                embedding_dim=768,
                quantization="uint8",
                source_model_name="model/a",
            ),
        ],
        is_overall=False,
    )

    by_model = {row.model_name: row for row in rows}

    assert by_model["model/a (768 dims)"].base_score_delta_percent is None
    assert by_model["model/a (768 dims, uint8)"].base_score_delta_percent == pytest.approx(10.0)


def test_variant_display_names_stay_unique_when_dimension_and_quantization_collide(tmp_path: Path) -> None:
    db_path = tmp_path / "results.duckdb"
    _write_task_results(
        db_path,
        [
            ("model/a", "BenchA", "bench/a", "BenchA", "a1", "a1", "a1", 0.90, 10, 12, 8192, None, 768, None),
            (
                "model/a",
                "BenchA",
                "bench/a",
                "BenchA",
                "a1",
                "a1",
                "a1",
                0.80,
                10,
                12,
                8192,
                "quantize_int8_docs",
                768,
                "int8",
            ),
            (
                "model/a",
                "BenchA",
                "bench/a",
                "BenchA",
                "a1",
                "a1",
                "a1",
                0.70,
                10,
                12,
                8192,
                "truncate_sparse_query_max_dims_8_truncate_sparse_docs_max_dims_64_quantize_int8_docs",
                768,
                "int8",
            ),
            ("model/b", "BenchA", "bench/a", "BenchA", "a1", "a1", "a1", 0.60, 20, 24, 4096, None, 512, None),
        ],
        include_embedding_variant_columns=True,
    )
    config_dir = tmp_path / "config"
    config_dir.mkdir()
    (config_dir / "benchmarks.yaml").write_text("benchmarks:\n  - name: BenchA\n", encoding="utf-8")
    (config_dir / "overall.yaml").write_text("name: Overall\nlabel: Overall\nbenchmarks:\n  - BenchA\n", encoding="utf-8")

    service = LeaderboardService(duckdb_path=db_path, config=load_viewer_config(config_dir))
    quantization_result = service.get_leaderboard("BenchA", include_quantization_variants=True)
    cross_variant_result = service.get_leaderboard(
        "BenchA",
        include_quantization_variants=True,
        include_truncate_variants=True,
    )

    assert [row.model_name for row in quantization_result.rows] == [
        "model/a (768 dims)",
        "model/a (768 dims, int8)",
        "model/b (512 dims)",
    ]
    assert [row.model_name for row in cross_variant_result.rows] == [
        "model/a (768 dims)",
        "model/a (768 dims, int8, quantize_int8_docs)",
        "model/a (768 dims, int8, truncate_sparse_query_max_dims_8_truncate_sparse_docs_max_dims_64_quantize_int8_docs)",
        "model/b (512 dims)",
    ]
    assert all(row.borda_score >= 0.0 for row in cross_variant_result.rows)


def test_variant_suffix_is_not_repeated_in_rendered_model_label(tmp_path: Path) -> None:
    from fastapi.testclient import TestClient

    db_path = tmp_path / "results.duckdb"
    _write_task_results(
        db_path,
        [
            (
                "jinaai/jina-embeddings-v5-text-nano",
                "BenchA",
                "bench/a",
                "BenchA",
                "a1",
                "a1",
                "a1",
                0.90,
                10,
                12,
                8192,
                "bf16",
                "flash_attention_2",
                None,
                None,
                None,
                None,
                None,
                None,
                True,
                None,
                768,
                None,
            ),
            (
                "jinaai/jina-embeddings-v5-text-nano",
                "BenchA",
                "bench/a",
                "BenchA",
                "a1",
                "a1",
                "a1",
                0.80,
                10,
                12,
                8192,
                "bf16",
                "flash_attention_2",
                None,
                None,
                None,
                None,
                None,
                None,
                True,
                "binary",
                768,
                "binary",
            ),
            (
                "Qwen/jina-embeddings-v5-text-nano",
                "BenchA",
                "bench/a",
                "BenchA",
                "a1",
                "a1",
                "a1",
                0.70,
                20,
                24,
                4096,
                "fp32",
                "sdpa",
                None,
                None,
                "query",
                "document",
                None,
                None,
                False,
                None,
                768,
                None,
            ),
        ],
        include_embedding_variant_columns=True,
        include_runtime_option_columns=True,
    )
    config_dir = tmp_path / "config"
    config_dir.mkdir()
    (config_dir / "benchmarks.yaml").write_text("benchmarks:\n  - name: BenchA\n", encoding="utf-8")
    (config_dir / "overall.yaml").write_text("name: Overall\nlabel: Overall\nbenchmarks:\n  - BenchA\n", encoding="utf-8")

    app = create_app(store=LocalDuckDbStore(DuckDbLocation(local_path=db_path)), config_dir=config_dir)
    client = TestClient(app)
    response = client.get("/leaderboard?view=BenchA&quantization=1")

    assert response.status_code == 200
    assert "jinaai/jina-embeddings-v5-text-nano (768 dims, binary, binary)" not in response.text
    assert "jinaai/jina-embeddings-v5-text-nano" in response.text
    assert "Qwen/jina-embeddings-v5-text-nano" in response.text
    assert "768 dims" in response.text
    assert "binary" in response.text
    assert ">remote code<" not in response.text
    assert 'data-model-metadata="' in response.text
    assert "&quot;dtype&quot;:&quot;bf16&quot;" in response.text
    assert "&quot;attention&quot;:&quot;flash_attention_2&quot;" in response.text
    assert "&quot;trust_remote_code&quot;:true" in response.text
    assert "Model Details" in response.text
    assert "<script>" not in response.text

    viewer_js_response = client.get("/assets/viewer.js")
    assert "JSON.parse" in viewer_js_response.text
    assert "window.__hakariBindModelDetails" in viewer_js_response.text
    assert 'event.target.id === "model-detail-modal"' in viewer_js_response.text
    assert "modal.close();" in viewer_js_response.text


def test_model_cell_views_shorten_names_unless_short_name_collides() -> None:
    unique = compute_leaderboard_rows(
        [
            TaskScore(
                "jinaai/jina-embeddings-v5-text-nano",
                "BenchA",
                "bench/a",
                "BenchA",
                "a1",
                "a1",
                "a1",
                0.90,
                10,
                12,
                8192,
                dtype="bf16",
                attn_implementation="flash_attention_2",
                prompt_summary="model default",
                trust_remote_code=True,
                embedding_dim=768,
            )
        ],
        is_overall=False,
    )
    unique_views = model_cell_views(unique)

    assert unique_views[unique[0].model_name].display_name == "jina-embeddings-v5-text-nano"
    assert unique_views[unique[0].model_name].metadata["model_name"] == "jinaai/jina-embeddings-v5-text-nano"
    assert unique_views[unique[0].model_name].metadata["dtype"] == "bf16"
    assert unique_views[unique[0].model_name].metadata["attention"] == "flash_attention_2"
    assert unique_views[unique[0].model_name].metadata["trust_remote_code"] is True

    colliding = compute_leaderboard_rows(
        [
            TaskScore(
                "jinaai/jina-embeddings-v5-text-nano",
                "BenchA",
                "bench/a",
                "BenchA",
                "a1",
                "a1",
                "a1",
                0.90,
                None,
                None,
                None,
            ),
            TaskScore(
                "other/jina-embeddings-v5-text-nano",
                "BenchA",
                "bench/a",
                "BenchA",
                "a1",
                "a1",
                "a1",
                0.80,
                None,
                None,
                None,
            ),
        ],
        is_overall=False,
    )
    colliding_views = model_cell_views(colliding)

    assert colliding_views[colliding[0].model_name].display_name == "jinaai/jina-embeddings-v5-text-nano"
    assert colliding_views[colliding[1].model_name].display_name == "other/jina-embeddings-v5-text-nano"


def test_model_filter_matches_any_whitespace_separated_token_case_insensitively(tmp_path: Path) -> None:
    from fastapi.testclient import TestClient

    db_path = tmp_path / "results.duckdb"
    _write_task_results(
        db_path,
        [
            ("google/gemma-embed", "BenchA", "bench/a", "BenchA", "a1", "a1", "a1", 0.90, 10, 12, 8192),
            ("Qwen/Qwen3-Embedding", "BenchA", "bench/a", "BenchA", "a1", "a1", "a1", 0.80, 10, 12, 8192),
            ("other/model", "BenchA", "bench/a", "BenchA", "a1", "a1", "a1", 0.70, 10, 12, 8192),
        ],
    )
    config_dir = tmp_path / "config"
    config_dir.mkdir()
    (config_dir / "benchmarks.yaml").write_text("benchmarks:\n  - name: BenchA\n", encoding="utf-8")
    (config_dir / "overall.yaml").write_text("name: Overall\nlabel: Overall\nbenchmarks:\n  - BenchA\n", encoding="utf-8")

    app = create_app(store=LocalDuckDbStore(DuckDbLocation(local_path=db_path)), config_dir=config_dir)
    response = TestClient(app).get("/leaderboard?view=BenchA&model_filter=GeMmA%20qwen")

    assert response.status_code == 200
    assert 'value="GeMmA qwen"' in response.text
    assert "google/gemma-embed" in response.text
    assert "Qwen/Qwen3-Embedding" in response.text
    assert "other/model" in response.text
    assert response.text.count('data-filter-hidden="true"') == 1


def test_viewer_renders_and_filters_runtime_options(tmp_path: Path) -> None:
    from fastapi.testclient import TestClient

    db_path = tmp_path / "results.duckdb"
    _write_task_results(
        db_path,
        [
            (
                "intfloat/multilingual-e5-small",
                "BenchA",
                "bench/a",
                "BenchA",
                "a1",
                "a1",
                "a1",
                0.90,
                10,
                12,
                512,
                "bf16",
                "flash_attention_2",
                "query: ",
                "passage: ",
                None,
                None,
                None,
                None,
                False,
            ),
            (
                "google/embeddinggemma-300m",
                "BenchA",
                "bench/a",
                "BenchA",
                "a1",
                "a1",
                "a1",
                0.80,
                20,
                24,
                2048,
                "bf16",
                "sdpa",
                None,
                None,
                "query",
                "document",
                None,
                None,
                False,
            ),
            (
                "jinaai/jina-embeddings-v5-text-small",
                "BenchA",
                "bench/a",
                "BenchA",
                "a1",
                "a1",
                "a1",
                0.70,
                30,
                36,
                8192,
                "bf16",
                "flash_attention_2",
                None,
                None,
                "query",
                "document",
                "retrieval",
                "retrieval",
                True,
            ),
        ],
        include_runtime_option_columns=True,
    )
    config_dir = tmp_path / "config"
    config_dir.mkdir()
    (config_dir / "benchmarks.yaml").write_text("benchmarks:\n  - name: BenchA\n", encoding="utf-8")
    (config_dir / "overall.yaml").write_text("name: Overall\nlabel: Overall\nbenchmarks:\n  - BenchA\n", encoding="utf-8")

    app = create_app(store=LocalDuckDbStore(DuckDbLocation(local_path=db_path)), config_dir=config_dir)
    response = TestClient(app).get(
        "/leaderboard?view=BenchA&filters=1&attn_filter=flash_attention_2&prompt_filter=explicit_prefixes"
    )

    assert response.status_code == 200
    assert "Runtime" in response.text
    assert ">Attention</summary>" in response.text
    assert ">Dtype</summary>" in response.text
    assert ">Prompt</summary>" in response.text
    assert ">Attention</span>" not in response.text
    assert ">Dtype</span>" not in response.text
    assert ">Prompt</span>" not in response.text
    assert ">FA2</td>" not in response.text
    assert ">SDPA</td>" not in response.text
    assert ">BF16</td>" not in response.text
    assert "Explicit prefixes" in response.text
    assert "Prompt names" in response.text
    assert "Prompt names + encode tasks" in response.text
    assert ">remote code<" not in response.text
    assert 'name="attn_filter" value="flash_attention_2" class="h-4 w-4 accent-cyan-700" checked' in response.text
    assert 'name="prompt_filter" value="explicit_prefixes" class="h-4 w-4 accent-cyan-700" checked' in response.text
    assert 'data-shown-count="1"' in response.text
    assert response.text.count('data-filter-hidden="true"') == 2
    assert "intfloat/multilingual-e5-small" in response.text
    assert "google/embeddinggemma-300m" in response.text


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
            ("model/b", "MNanoBEIR", "NanoBEIR-ja", "NanoBEIR-ja", "NanoArguAna", "arguana", "ja-arguana", 0.50, 20, 24, 4096),
            ("model/b", "MNanoBEIR", "NanoBEIR-ja", "NanoBEIR-ja", "NanoFEVER", "fever", "ja-fever", 0.40, 20, 24, 4096),
            ("model/b", "MNanoBEIR", "NanoBEIR-en", "NanoBEIR-en", "NanoArguAna", "arguana", "en-arguana", 0.60, 20, 24, 4096),
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
    hidden_result = service.get_leaderboard("MNanoBEIR", score_group_name="task_mean")
    task_result = service.get_leaderboard("MNanoBEIR", score_group_name="task_mean", show_task_scores=True)
    lang_result = service.get_leaderboard(
        "MNanoBEIR",
        score_group_name="lang_mean",
        sort="metric:NanoBEIR-ja",
        show_task_scores=True,
    )

    assert hidden_result.metric_columns == []
    assert task_result.metric_columns == ["arguana", "fever"]
    assert task_result.rows[0].mean_score == 67.5
    assert task_result.rows[0].metric_values["arguana"] == 75.0
    assert lang_result.metric_columns == ["NanoBEIR-en", "NanoBEIR-ja"]
    lang_by_model = {row.model_name: row for row in lang_result.rows}
    assert lang_by_model["model/a"].mean_score == 70.0
    assert lang_by_model["model/a"].metric_values["NanoBEIR-ja"] == 70.0

    from fastapi.testclient import TestClient

    app = create_app(store=LocalDuckDbStore(DuckDbLocation(local_path=db_path)), config_dir=config_dir)
    response = TestClient(app).get(
        "/leaderboard?view=MNanoBEIR&group=lang_mean&task_scores=1&sort=metric:NanoBEIR-ja"
    )

    assert response.status_code == 200
    assert "Task Mean" in response.text
    assert "Lang Mean" in response.text
    assert "Task score columns" in response.text
    assert 'name="task_scores" value="1" class="h-4 w-4 accent-cyan-700" checked' in response.text
    assert "Mean Score" in response.text
    assert ">BEIR-ja</span>" in response.text
    assert "[overflow-wrap:anywhere]" in response.text
    assert "w-[4.75rem] min-w-[4.75rem] max-w-[4.75rem]" in response.text
    assert "metric%3ANanoBEIR-ja" in response.text
    assert 'hx-push-url="/?view=MNanoBEIR&amp;sort=metric%3ANanoBEIR-ja' in response.text


def test_mnanobeir_language_pages_use_dataset_primary_language(tmp_path: Path) -> None:
    db_path = tmp_path / "results.duckdb"
    rows = []
    metadata_rows = []
    for dataset_name, primary_language, languages, score in [
        ("NanoBEIR-en", "en", ["en"], 0.10),
        ("NanoBEIR-de", "multilingual", ["de", "en"], 0.90),
        ("NanoBEIR-ja", "ja", ["ja"], 0.50),
    ]:
        for task_name in ["arguana", "fever"]:
            task_key = f"{dataset_name}::{task_name}"
            rows.append(
                (
                    "model/a",
                    "MNanoBEIR",
                    dataset_name,
                    dataset_name,
                    task_name,
                    task_name,
                    task_key,
                    score,
                    10,
                    12,
                    8192,
                )
            )
            metadata_rows.append(
                (
                    "MNanoBEIR",
                    dataset_name,
                    dataset_name,
                    task_name,
                    task_name,
                    task_key,
                    primary_language,
                    languages,
                )
            )
    _write_task_results(db_path, rows, dataset_metadata_rows=metadata_rows)
    config_dir = tmp_path / "config"
    config_dir.mkdir()
    (config_dir / "benchmarks.yaml").write_text(
        """
benchmarks:
  - name: MNanoBEIR
    language_filter_mode: primary_language
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
    result = service.get_leaderboard("MNanoBEIR")
    en_result = service.get_leaderboard("MNanoBEIR", language_filters=("en",))

    assert [(option.code, option.task_count) for option in result.available_languages] == [
        ("de", 2),
        ("en", 2),
        ("ja", 2),
    ]
    assert en_result.selected_languages == ("en",)
    assert en_result.expected_tasks == 2
    assert en_result.rows[0].mean_score == 10.0


def test_split_language_pages_use_primary_split_language(tmp_path: Path) -> None:
    db_path = tmp_path / "results.duckdb"
    rows = []
    metadata_rows = []
    for split_name, primary_language, languages, score in [
        ("en", "en", ["en"], 0.10),
        ("yo", "multilingual", ["en", "sw", "yo"], 0.90),
    ]:
        task_key = f"NanoMIRACL::{split_name}"
        rows.append(
            (
                "model/a",
                "NanoMIRACL",
                "hakari-bench/NanoMIRACL",
                "NanoMIRACL",
                split_name,
                split_name,
                task_key,
                score,
                10,
                12,
                8192,
            )
        )
        metadata_rows.append(
            (
                "NanoMIRACL",
                "hakari-bench/NanoMIRACL",
                "NanoMIRACL",
                split_name,
                split_name,
                task_key,
                primary_language,
                languages,
            )
        )
    _write_task_results(db_path, rows, dataset_metadata_rows=metadata_rows)
    config_dir = tmp_path / "config"
    config_dir.mkdir()
    (config_dir / "benchmarks.yaml").write_text(
        """
benchmarks:
  - name: NanoMIRACL
    language_filter_mode: primary_language
""".strip(),
        encoding="utf-8",
    )
    (config_dir / "overall.yaml").write_text(
        "name: Overall\nlabel: Overall\nbenchmarks:\n  - NanoMIRACL\n",
        encoding="utf-8",
    )

    service = LeaderboardService(duckdb_path=db_path, config=load_viewer_config(config_dir))
    result = service.get_leaderboard("NanoMIRACL")
    yo_result = service.get_leaderboard("NanoMIRACL", language_filters=("yo",))

    assert [(option.code, option.task_count) for option in result.available_languages] == [
        ("en", 1),
        ("yo", 1),
    ]
    assert yo_result.selected_languages == ("yo",)
    assert yo_result.expected_tasks == 1
    assert yo_result.rows[0].mean_score == 90.0


def test_task_score_display_can_show_all_tasks_and_filter_task_columns(tmp_path: Path) -> None:
    from fastapi.testclient import TestClient

    db_path = tmp_path / "results.duckdb"
    _write_task_results(
        db_path,
        [
            ("model/a", "BenchA", "bench/a", "BenchA", "NanoArguAna", "arguana", "bench::arguana", 0.90, 10, 12, 8192),
            ("model/a", "BenchA", "bench/a", "BenchA", "NanoFEVER", "fever", "bench::fever", 0.80, 10, 12, 8192),
            ("model/b", "BenchA", "bench/a", "BenchA", "NanoArguAna", "arguana", "bench::arguana", 0.70, 10, 12, 8192),
            ("model/b", "BenchA", "bench/a", "BenchA", "NanoFEVER", "fever", "bench::fever", 0.60, 10, 12, 8192),
        ],
    )
    config_dir = tmp_path / "config"
    config_dir.mkdir()
    (config_dir / "benchmarks.yaml").write_text("benchmarks:\n  - name: BenchA\n", encoding="utf-8")
    (config_dir / "overall.yaml").write_text("name: Overall\nlabel: Overall\nbenchmarks:\n  - BenchA\n", encoding="utf-8")

    service = LeaderboardService(duckdb_path=db_path, config=load_viewer_config(config_dir))
    hidden_result = service.get_leaderboard("BenchA")
    full_result = service.get_leaderboard("BenchA", show_task_scores=True)
    filtered_result = service.get_leaderboard("BenchA", show_task_scores=True, task_filter="arguana qwen")

    assert hidden_result.metric_columns == []
    assert full_result.metric_columns == ["arguana", "fever"]
    assert filtered_result.metric_columns == ["arguana"]
    assert filtered_result.rows[0].metric_values["arguana"] == 90.0

    app = create_app(store=LocalDuckDbStore(DuckDbLocation(local_path=db_path)), config_dir=config_dir)
    response = TestClient(app).get("/leaderboard?view=BenchA&task_scores=1&task_filter=ARGUANA%20qw")

    assert response.status_code == 200
    assert 'id="task-filter-input"' in response.text
    assert 'name="task_filter"' in response.text
    assert 'value="ARGUANA qw"' in response.text
    assert ">arguana</span>" in response.text
    assert ">fever</span>" not in response.text
    assert "metric%3Aarguana" in response.text


def test_task_z_score_columns_use_base_variant_task_stddev(tmp_path: Path) -> None:
    from fastapi.testclient import TestClient

    db_path = tmp_path / "results.duckdb"
    _write_task_results(
        db_path,
        [
            ("model/a", "BenchA", "bench/a", "BenchA", "NanoArguAna", "arguana", "bench::arguana", 0.90, 10, 12, 8192),
            ("model/a", "BenchA", "bench/a", "BenchA", "NanoFEVER", "fever", "bench::fever", 0.50, 10, 12, 8192),
            ("model/b", "BenchA", "bench/a", "BenchA", "NanoArguAna", "arguana", "bench::arguana", 0.70, 20, 24, 4096),
            ("model/b", "BenchA", "bench/a", "BenchA", "NanoFEVER", "fever", "bench::fever", 0.50, 20, 24, 4096),
            (
                "model/a",
                "BenchA",
                "bench/a",
                "BenchA",
                "NanoArguAna",
                "arguana",
                "bench::arguana",
                0.827,
                10,
                12,
                8192,
                "truncate_dim_256",
                256,
                None,
            ),
            (
                "model/a",
                "BenchA",
                "bench/a",
                "BenchA",
                "NanoFEVER",
                "fever",
                "bench::fever",
                0.50,
                10,
                12,
                8192,
                "truncate_dim_256",
                256,
                None,
            ),
        ],
        include_embedding_variant_columns=True,
    )
    config_dir = tmp_path / "config"
    config_dir.mkdir()
    (config_dir / "benchmarks.yaml").write_text("benchmarks:\n  - name: BenchA\n", encoding="utf-8")
    (config_dir / "overall.yaml").write_text("name: Overall\nlabel: Overall\nbenchmarks:\n  - BenchA\n", encoding="utf-8")

    service = LeaderboardService(duckdb_path=db_path, config=load_viewer_config(config_dir))
    result = service.get_leaderboard(
        "BenchA",
        include_truncate_variants=True,
        show_task_z_scores=True,
    )
    rows_by_name = {row.model_name: row for row in result.rows}

    assert result.show_task_scores is True
    assert result.show_task_z_scores is True
    assert rows_by_name["model/a"].metric_values["arguana"] == 90.0
    assert rows_by_name["model/a"].metric_z_values["arguana"] == pytest.approx(1.0)
    assert rows_by_name["model/b"].metric_z_values["arguana"] == pytest.approx(-1.0)
    variant_row = next(row for row in result.rows if row.embedding_variant_name == "truncate_dim_256")
    assert variant_row.metric_z_values["arguana"] == pytest.approx(0.27)
    assert "fever" not in variant_row.metric_z_values

    app = create_app(store=LocalDuckDbStore(DuckDbLocation(local_path=db_path)), config_dir=config_dir)
    response = TestClient(app).get("/leaderboard?view=BenchA&truncate=1&task_z_scores=1")

    assert response.status_code == 200
    assert "Task std display" in response.text
    assert 'name="task_z_scores" value="1" class="h-4 w-4 accent-cyan-700" checked' in response.text
    assert "task-z-score task-z-pos-100" in response.text
    assert "task-z-score task-z-pos-025" in response.text
    assert "task-z-score task-z-neg-100" in response.text
    assert '<span class="task-z-score-value">90.00</span>' in response.text
    assert '<span class="task-z-score-value">82.70</span>' in response.text
    assert '<span class="task-z-score-delta">+1.00σ</span>' in response.text
    assert '<span class="task-z-score-delta">+0.27σ</span>' in response.text


def test_task_z_score_heatmap_uses_quarter_sigma_buckets() -> None:
    assert _rounded_z_score(0.12) == 0.0
    assert _rounded_z_score(0.13) == 0.25
    assert _rounded_z_score(0.27) == 0.25
    assert _rounded_z_score(0.38) == 0.5
    assert _rounded_z_score(1.62) == 1.5
    assert _rounded_z_score(1.63) == 1.75
    assert _rounded_z_score(2.9) == 2.0
    assert _rounded_z_score(-0.38) == -0.5

    assert _z_score_bucket_class(0.0) == "task-z-neutral"
    assert _z_score_bucket_class(0.25) == "task-z-pos-025"
    assert _z_score_bucket_class(1.75) == "task-z-pos-175"
    assert _z_score_bucket_class(-0.25) == "task-z-neg-025"
    assert _z_score_bucket_class(-2.0) == "task-z-neg-200"


def test_task_z_score_heatmap_css_defines_light_and_dark_buckets() -> None:
    css_source = Path("hakari_bench/viewer/assets/app.tailwind.css").read_text(encoding="utf-8")

    for direction in ("pos", "neg"):
        for bucket in ("025", "050", "075", "100", "125", "150", "175", "200"):
            selector = f".task-z-{direction}-{bucket}"
            assert css_source.count(selector) == 2


def test_task_z_score_heatmap_css_uses_intuitive_positive_negative_colors() -> None:
    css_source = Path("hakari_bench/viewer/assets/app.tailwind.css").read_text(encoding="utf-8")

    assert re.search(r'\.task-z-pos-025\s*{\s*background-color: theme\("colors\.emerald\.50"\);', css_source)
    assert re.search(r'\.task-z-pos-200\s*{\s*background-color: theme\("colors\.emerald\.700"\);', css_source)
    assert re.search(r'\.task-z-neg-025\s*{\s*background-color: theme\("colors\.rose\.50"\);', css_source)
    assert re.search(r'\.task-z-neg-200\s*{\s*background-color: theme\("colors\.rose\.700"\);', css_source)
    assert re.search(r'\.task-z-pos-025\s*{\s*background-color: theme\("colors\.emerald\.950"\);', css_source)
    assert re.search(r'\.task-z-pos-200\s*{\s*background-color: theme\("colors\.emerald\.300"\);', css_source)


def test_leaderboard_filters_tasks_by_query_and_document_mean_lengths(tmp_path: Path) -> None:
    db_path = tmp_path / "results.duckdb"
    rows = [
        ("model/a", "BenchA", "bench/a", "BenchA", "short", "short", "BenchA::short", 0.90, 10, 12, 8192),
        ("model/b", "BenchA", "bench/a", "BenchA", "short", "short", "BenchA::short", 0.70, 10, 12, 8192),
        ("model/a", "BenchA", "bench/a", "BenchA", "longq", "longq", "BenchA::longq", 0.20, 10, 12, 8192),
        ("model/b", "BenchA", "bench/a", "BenchA", "longq", "longq", "BenchA::longq", 0.95, 10, 12, 8192),
        ("model/a", "BenchA", "bench/a", "BenchA", "longd", "longd", "BenchA::longd", 0.30, 10, 12, 8192),
        ("model/b", "BenchA", "bench/a", "BenchA", "longd", "longd", "BenchA::longd", 0.85, 10, 12, 8192),
    ]
    _write_task_results(
        db_path,
        rows,
        dataset_metadata_rows=[
            ("BenchA", "bench/a", "BenchA", "short", "short", "BenchA::short", "en", ["en"], 500.0, 1500.0),
            ("BenchA", "bench/a", "BenchA", "longq", "longq", "BenchA::longq", "en", ["en"], 1200.0, 1500.0),
            ("BenchA", "bench/a", "BenchA", "longd", "longd", "BenchA::longd", "en", ["en"], 500.0, 2500.0),
        ],
    )
    config_dir = tmp_path / "config"
    config_dir.mkdir()
    (config_dir / "benchmarks.yaml").write_text("benchmarks:\n  - name: BenchA\n", encoding="utf-8")
    (config_dir / "overall.yaml").write_text("name: Overall\nlabel: Overall\nbenchmarks:\n  - BenchA\n", encoding="utf-8")

    result = LeaderboardService(duckdb_path=db_path, config=load_viewer_config(config_dir)).get_leaderboard(
        "BenchA",
        query_max_chars=1000,
        document_max_chars=2000,
        show_task_scores=True,
    )

    assert result.expected_tasks == 1
    assert result.metric_columns == ["short"]
    assert [row.model_name for row in result.rows] == ["model/a", "model/b"]
    assert result.rows[0].mean_score == pytest.approx(90.0)


def test_viewer_renders_and_applies_task_length_filters(tmp_path: Path) -> None:
    from fastapi.testclient import TestClient

    db_path = tmp_path / "results.duckdb"
    _write_task_results(
        db_path,
        [
            ("model/a", "BenchA", "bench/a", "BenchA", "short", "short", "BenchA::short", 0.90, 10, 12, 8192),
            ("model/b", "BenchA", "bench/a", "BenchA", "short", "short", "BenchA::short", 0.70, 10, 12, 8192),
            ("model/a", "BenchA", "bench/a", "BenchA", "long", "long", "BenchA::long", 0.10, 10, 12, 8192),
            ("model/b", "BenchA", "bench/a", "BenchA", "long", "long", "BenchA::long", 0.95, 10, 12, 8192),
        ],
        dataset_metadata_rows=[
            ("BenchA", "bench/a", "BenchA", "short", "short", "BenchA::short", "en", ["en"], 500.0, 1500.0),
            ("BenchA", "bench/a", "BenchA", "long", "long", "BenchA::long", "en", ["en"], 1200.0, 2500.0),
        ],
    )
    config_dir = tmp_path / "config"
    config_dir.mkdir()
    (config_dir / "benchmarks.yaml").write_text("benchmarks:\n  - name: BenchA\n", encoding="utf-8")
    (config_dir / "overall.yaml").write_text("name: Overall\nlabel: Overall\nbenchmarks:\n  - BenchA\n", encoding="utf-8")

    app = create_app(store=LocalDuckDbStore(DuckDbLocation(local_path=db_path)), config_dir=config_dir)
    response = TestClient(app).get(
        "/leaderboard?view=BenchA&task_scores=1&filters=1&query_len_max=1000&doc_len_max=2000"
    )

    assert response.status_code == 200
    assert "Task string length" in response.text
    assert "Task length" not in response.text
    assert 'data-tooltip="Filters tasks by average query and document string length in characters.' in response.text
    assert "Tasks missing length metadata are excluded when a bound is set." in response.text
    assert "border-cyan-700 bg-cyan-50" in response.text
    assert 'name="query_len_max" value="1000"' in response.text
    assert 'name="doc_len_max" value="2000"' in response.text
    assert ">short</span>" in response.text
    assert ">long</span>" not in response.text
    assert response.text.index("model/a") < response.text.index("model/b")

    ranking_response = TestClient(app).get("/leaderboard?view=BenchA&filters=1&query_len_max=1000&doc_len_max=2000")

    assert ranking_response.status_code == 200
    assert ranking_response.text.index("model/a") < ranking_response.text.index("model/b")
    assert "90.0" in ranking_response.text
    assert "52.5" not in ranking_response.text


def test_metric_column_label_omits_nano_prefix_only_for_display() -> None:
    assert _metric_column_label("NanoAILAStatutes") == "AILAStatutes"
    assert _metric_column_label("NanoBEIR-ja") == "BEIR-ja"
    assert _metric_column_label("NanoWikipediaRetrievalMultilingual") == "WikipediaRetrievalMultilingual"
    assert _metric_column_label("arguana") == "arguana"
    assert _metric_column_label("NanoBIRCO::NanoBIRCO") == "NanoBIRCO::NanoBIRCO"
    assert _metric_column_label("NanoMMTEB::NanoArguAna") == "NanoMMTEB::NanoArguAna"
    assert _metric_column_label("MNanoBEIR::hakari-bench/NanoBEIR-ar::arguana") == "NanoBEIR-ar::arguana"


def test_metric_column_labels_keep_full_name_when_short_labels_collide() -> None:
    columns = [
        "BenchA::hakari-bench/NanoBEIR-ar::arguana",
        "BenchB::other-owner/NanoBEIR-ar::arguana",
        "BenchA::hakari-bench/NanoBEIR-ja::arguana",
    ]

    assert _metric_column_labels(columns) == {
        "BenchA::hakari-bench/NanoBEIR-ar::arguana": "BenchA::hakari-bench/NanoBEIR-ar::arguana",
        "BenchB::other-owner/NanoBEIR-ar::arguana": "BenchB::other-owner/NanoBEIR-ar::arguana",
        "BenchA::hakari-bench/NanoBEIR-ja::arguana": "NanoBEIR-ja::arguana",
    }


def test_task_score_column_headers_shorten_dataset_task_keys_and_keep_full_name(tmp_path: Path) -> None:
    db_path = tmp_path / "results.duckdb"
    _write_task_results(
        db_path,
        [
            (
                "model/a",
                "MNanoBEIR",
                "hakari-bench/NanoBEIR-ar",
                "NanoBEIR-ar",
                "ar",
                "arguana",
                "MNanoBEIR::hakari-bench/NanoBEIR-ar::arguana",
                0.80,
                10,
                12,
                8192,
            ),
            (
                "model/a",
                "MNanoBEIR",
                "hakari-bench/NanoBEIR-ja",
                "NanoBEIR-ja",
                "ja",
                "arguana",
                "MNanoBEIR::hakari-bench/NanoBEIR-ja::arguana",
                0.70,
                10,
                12,
                8192,
            ),
            (
                "model/b",
                "MNanoBEIR",
                "hakari-bench/NanoBEIR-ar",
                "NanoBEIR-ar",
                "ar",
                "arguana",
                "MNanoBEIR::hakari-bench/NanoBEIR-ar::arguana",
                0.60,
                20,
                24,
                4096,
            ),
            (
                "model/b",
                "MNanoBEIR",
                "hakari-bench/NanoBEIR-ja",
                "NanoBEIR-ja",
                "ja",
                "arguana",
                "MNanoBEIR::hakari-bench/NanoBEIR-ja::arguana",
                0.50,
                20,
                24,
                4096,
            ),
        ],
    )
    config_dir = tmp_path / "config"
    config_dir.mkdir()
    (config_dir / "benchmarks.yaml").write_text(
        """
benchmarks:
  - name: MNanoBEIR
    score_groups:
      - name: task_key
        label: Task Key
        group_by: task_key
""".strip(),
        encoding="utf-8",
    )
    (config_dir / "overall.yaml").write_text("name: Overall\nlabel: Overall\nbenchmarks:\n  - MNanoBEIR\n", encoding="utf-8")

    from fastapi.testclient import TestClient

    app = create_app(store=LocalDuckDbStore(DuckDbLocation(local_path=db_path)), config_dir=config_dir)
    response = TestClient(app).get("/leaderboard?view=MNanoBEIR&group=task_key&task_scores=1")

    assert response.status_code == 200
    assert ">NanoBEIR-ar::arguana</span>" in response.text
    assert ">NanoBEIR-ja::arguana</span>" in response.text
    assert (
        'data-metric-column-full-name="MNanoBEIR::hakari-bench/NanoBEIR-ar::arguana"'
        in response.text
    )


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


def test_resolve_duckdb_location_defaults_to_hakari_bench_name(tmp_path: Path) -> None:
    location = resolve_duckdb_location(
        data_dir=tmp_path,
        duckdb_path=None,
        source_results_dir=None,
        source_duckdb_path=None,
    )

    assert location.local_path == tmp_path / "hakari_bench.duckdb"


def test_resolve_duckdb_location_uses_source_results_dir(tmp_path: Path) -> None:
    source_results_dir = tmp_path / "results"
    source_results_dir.mkdir()
    source_duckdb = source_results_dir / "hakari_bench.duckdb"
    source_duckdb.write_bytes(b"duckdb")

    location = resolve_duckdb_location(
        data_dir=tmp_path / "viewer",
        duckdb_path=None,
        source_results_dir=source_results_dir,
        source_duckdb_path=None,
    )

    assert location.source_path == source_duckdb


def test_resolve_duckdb_location_uses_environment_paths(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    local = tmp_path / "from-env.duckdb"
    source = tmp_path / "source.duckdb"
    source.write_bytes(b"duckdb")
    monkeypatch.setenv("HAKARI_BENCH_VIEWER_DUCKDB_PATH", str(local))
    monkeypatch.setenv("HAKARI_BENCH_VIEWER_SOURCE_DUCKDB_PATH", str(source))

    location = resolve_duckdb_location(
        data_dir=tmp_path / "viewer",
        duckdb_path=None,
        source_results_dir=None,
        source_duckdb_path=None,
    )

    assert location.local_path == local
    assert location.source_path == source
    assert location.hf_source is None


def test_resolve_duckdb_location_uses_hf_dataset_environment(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("HAKARI_BENCH_VIEWER_HF_DATASET_REPO_ID", "hakari-bench/leaderboard_database")
    monkeypatch.setenv("HAKARI_BENCH_VIEWER_HF_DATASET_PATH", "duckdb/hakari_bench.duckdb")
    monkeypatch.setenv("HAKARI_BENCH_VIEWER_HF_DATASET_REVISION", "main")

    location = resolve_duckdb_location(
        data_dir=tmp_path,
        duckdb_path=None,
        source_results_dir=None,
        source_duckdb_path=None,
    )

    assert location.local_path == tmp_path / "hakari_bench.duckdb"
    assert location.source_path is None
    assert location.hf_source == HuggingFaceDuckDbSource(
        repo_id="hakari-bench/leaderboard_database",
        filename="duckdb/hakari_bench.duckdb",
        revision="main",
    )


def test_local_duckdb_store_downloads_hf_dataset_source(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    downloaded = tmp_path / "hf-cache.duckdb"
    downloaded.write_bytes(b"hf")
    local = tmp_path / "viewer" / "hakari_bench.duckdb"
    calls: list[HuggingFaceDuckDbSource] = []

    def fake_download(source: HuggingFaceDuckDbSource) -> Path:
        calls.append(source)
        return downloaded

    monkeypatch.setattr("hakari_bench.viewer.store._download_hf_duckdb", fake_download)
    source = HuggingFaceDuckDbSource(
        repo_id="hakari-bench/leaderboard_database",
        filename="duckdb/hakari_bench.duckdb",
        revision="main",
    )
    store = LocalDuckDbStore(DuckDbLocation(local_path=local, hf_source=source))

    assert store.ensure_current() is True
    assert local.read_bytes() == b"hf"
    assert calls == [source]


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
    rows: list[tuple],
    *,
    include_embedding_variant_columns: bool = False,
    include_runtime_option_columns: bool = False,
    dataset_metadata_rows: list[tuple] | None = None,
    task_diagnostics_rows: list[tuple] | None = None,
) -> None:
    con = duckdb.connect(str(db_path))
    try:
        con.execute("CREATE TABLE meta_database (schema_version VARCHAR)")
        con.execute("INSERT INTO meta_database VALUES (?)", [CURRENT_DUCKDB_SCHEMA_VERSION])
        columns = (
            "model_name VARCHAR",
            "benchmark VARCHAR",
            "dataset_id VARCHAR",
            "dataset_name VARCHAR",
            "split_name VARCHAR",
            "task_name VARCHAR",
            "task_key VARCHAR",
            "score_target VARCHAR",
            "score DOUBLE",
            "language VARCHAR",
            "languages VARCHAR[]",
            "active_parameters BIGINT",
            "total_parameters BIGINT",
            "max_seq_length INTEGER",
            "dtype VARCHAR",
            "attn_implementation VARCHAR",
            "query_prompt VARCHAR",
            "document_prompt VARCHAR",
            "query_prompt_name VARCHAR",
            "document_prompt_name VARCHAR",
            "query_encode_task VARCHAR",
            "document_encode_task VARCHAR",
            "trust_remote_code BOOLEAN",
            "embedding_variant_name VARCHAR",
            "embedding_dim INTEGER",
            "quantization VARCHAR",
            "query_mean_chars DOUBLE",
            "document_mean_chars DOUBLE",
        )
        con.execute(
            f"""
            CREATE TABLE viewer_task_results (
                {", ".join(columns)}
            )
            """
        )
        metadata_by_task = _metadata_by_task(dataset_metadata_rows or [])
        normalized_rows = [
            _viewer_task_result_row(
                row,
                language=metadata_by_task.get((row[1], row[2], row[4], row[5], row[6]), (None, [], None, None))[0],
                languages=metadata_by_task.get((row[1], row[2], row[4], row[5], row[6]), (None, [], None, None))[1],
                query_mean_chars=metadata_by_task.get((row[1], row[2], row[4], row[5], row[6]), (None, [], None, None))[2],
                document_mean_chars=metadata_by_task.get((row[1], row[2], row[4], row[5], row[6]), (None, [], None, None))[3],
            )
            for row in rows
        ]
        normalized_rows.extend(_reranking_viewer_rows(normalized_rows, task_diagnostics_rows or []))
        placeholders = ", ".join("?" for _ in columns)
        if normalized_rows:
            con.executemany(f"INSERT INTO viewer_task_results VALUES ({placeholders})", normalized_rows)
        assert include_embedding_variant_columns or all(len(row) in {11, 20} for row in rows)
        assert include_runtime_option_columns or all(len(row) in {11, 14} for row in rows)
    finally:
        con.close()


def _metadata_by_task(rows: list[tuple]) -> dict[tuple[str, str, str, str, str], tuple[str | None, list[str], float | None, float | None]]:
    metadata = {}
    for row in rows:
        benchmark, dataset_id, _dataset_name, split_name, task_name, task_key, language, languages, *lengths = row
        query_mean_chars = lengths[0] if len(lengths) >= 1 else None
        document_mean_chars = lengths[1] if len(lengths) >= 2 else None
        metadata[(benchmark, dataset_id, split_name, task_name, task_key)] = (
            language,
            languages,
            query_mean_chars,
            document_mean_chars,
        )
    return metadata


def _viewer_task_result_row(
    row: tuple,
    *,
    language: str | None,
    languages: list[str],
    query_mean_chars: float | None = None,
    document_mean_chars: float | None = None,
) -> tuple:
    base = row[:11]
    remaining = row[11:]
    dtype = None
    attn_implementation = None
    query_prompt = None
    document_prompt = None
    query_prompt_name = None
    document_prompt_name = None
    query_encode_task = None
    document_encode_task = None
    trust_remote_code = None
    embedding_variant_name = None
    embedding_dim = None
    quantization = None
    if len(remaining) == 3:
        embedding_variant_name, embedding_dim, quantization = remaining
    elif len(remaining) == 9:
        (
            dtype,
            attn_implementation,
            query_prompt,
            document_prompt,
            query_prompt_name,
            document_prompt_name,
            query_encode_task,
            document_encode_task,
            trust_remote_code,
        ) = remaining
    elif len(remaining) == 12:
        (
            dtype,
            attn_implementation,
            query_prompt,
            document_prompt,
            query_prompt_name,
            document_prompt_name,
            query_encode_task,
            document_encode_task,
            trust_remote_code,
            embedding_variant_name,
            embedding_dim,
            quantization,
        ) = remaining
    elif len(remaining) == 0:
        pass
    else:
        raise AssertionError(f"Unexpected row shape: {row!r}")
    return (
        *base[:7],
        "all",
        base[7],
        language,
        languages,
        *base[8:11],
        dtype,
        attn_implementation,
        query_prompt,
        document_prompt,
        query_prompt_name,
        document_prompt_name,
        query_encode_task,
        document_encode_task,
        trust_remote_code,
        embedding_variant_name,
        embedding_dim,
        quantization,
        query_mean_chars,
        document_mean_chars,
    )


def _reranking_viewer_rows(base_rows: list[tuple], diagnostic_rows: list[tuple]) -> list[tuple]:
    base_by_task = {
        (row[0], row[1], row[2], row[5], row[6]): row
        for row in base_rows
        if row[7] == "all" and row[23] is None
    }
    reranking_rows = []
    for diagnostic in diagnostic_rows:
        (
            model_name,
            benchmark,
            dataset_id,
            task_name,
            task_key,
            _base_score,
            rerank_score,
            _rerank_lift,
            rerank_status,
            rerank_top_k,
            _candidate_source,
            candidate_ranking,
            _bm25_source,
            _query_coverage,
            _relevant_coverage,
        ) = diagnostic
        base_row = base_by_task.get((model_name, benchmark, dataset_id, task_name, task_key))
        if (
            base_row is None
            or rerank_score is None
            or rerank_status != "available"
            or rerank_top_k != 100
            or candidate_ranking != "bm25"
        ):
            continue
        reranking_rows.append(
            (
                *base_row[:7],
                "reranking",
                rerank_score,
                *base_row[9:],
            )
        )
    return reranking_rows
