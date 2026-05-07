from __future__ import annotations

import os
import time
from pathlib import Path

import duckdb
import pytest

from hakari_bench.viewer.app import _fmt_max_len, _metric_column_label, create_app
from hakari_bench.viewer.config import load_viewer_config
from hakari_bench.viewer.leaderboard import LeaderboardService, TaskScore, compute_leaderboard_rows
from hakari_bench.viewer.model_display import model_cell_views
from hakari_bench.viewer.store import DuckDbLocation, LocalDuckDbStore, resolve_duckdb_location


def test_viewer_config_uses_curated_overall_benchmarks_in_display_order() -> None:
    config = load_viewer_config()
    language_nanomteb_benchmarks = [
        "NanoMTEB-Dutch",
        "NanoMTEB-French",
        "NanoMTEB-German",
        "NanoMTEB-Japanese",
        "NanoMTEB-Korean",
        "NanoMTEB-Persian",
        "NanoMTEB-Polish",
        "NanoMTEB-Russian",
        "NanoMTEB-Scandinavian",
        "NanoMTEB-Spanish",
        "NanoMTEB-Thai",
        "NanoMTEB-Vietnamese",
        "NanoMTEB-Xlingual",
    ]
    expected_overall_benchmarks = [
        "NanoMMTEB",
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
    ]

    assert config.overall.benchmark_names == expected_overall_benchmarks
    grouped_overall = config.overall_for_view("OverallGrouped")
    assert grouped_overall is not None
    assert [component.name for component in grouped_overall.benchmark_components] == [
        "MNanoBEIR",
        "NanoRTEB",
        "NanoMMTEB",
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
        "NanoMTEB",
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
  - name: NanoMTEB-Japanese
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
    result = service.get_leaderboard("OverallGrouped")

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
    response = TestClient(app).get("/leaderboard?view=OverallGrouped")

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
    bench_result = service.get_leaderboard("BenchA")
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
    assert "Display:" in response.text
    assert "Other variants" in response.text
    assert "Filters:" in response.text
    assert '<div class="mt-3 flex flex-wrap items-start gap-3">' in response.text
    assert ">Dims</summary>" in response.text
    assert ">Quantization</summary>" in response.text
    assert "grid-cols-2" in response.text
    assert "sm:grid-cols-3" in response.text
    assert response.text.count(">All</button>") == 5
    assert response.text.count(">None</button>") == 5
    assert 'id="display-controls"' in response.text
    assert 'id="facet-filters"' in response.text
    assert 'from:input[type=' not in response.text
    assert 'hx-trigger="change, submit"' in response.text
    assert 'hx-include="#display-controls"' not in response.text
    assert "Truncate dims" in response.text
    assert "Rescore" in response.text
    assert 'id="model-filter-input"' in response.text
    assert 'name="model_filter"' in response.text
    assert 'value="model/b"' in response.text
    assert "&quot;ranking_model_name&quot;:&quot;model/a (768 dims, uint8)&quot;" in response.text
    assert "model/a" in response.text
    assert "bg-cyan-50" in response.text
    assert "768 dims" in response.text
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
    assert "htmx:afterSwap" in response.text
    assert "window.__hakariRestoreModelFilterFocus" in response.text
    assert 'name="dim_filter" value="512" class="h-4 w-4 accent-cyan-700" checked' in response.text
    assert 'name="quant_filter" value="__none__" class="h-4 w-4 accent-cyan-700" checked' in response.text

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
    response = TestClient(app).get("/leaderboard?view=BenchA&quantization=1")

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
    assert "JSON.parse" in response.text
    assert 'modal.addEventListener("click"' in response.text
    assert "if (event.target === modal) modal.close();" in response.text


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
) -> None:
    con = duckdb.connect(str(db_path))
    try:
        variant_columns = (
            [
                "embedding_variant_name VARCHAR",
                "embedding_dim INTEGER",
                "quantization VARCHAR",
            ]
            if include_embedding_variant_columns
            else []
        )
        runtime_columns = (
            [
                "dtype VARCHAR",
                "attn_implementation VARCHAR",
                "query_prompt VARCHAR",
                "document_prompt VARCHAR",
                "query_prompt_name VARCHAR",
                "document_prompt_name VARCHAR",
                "query_encode_task VARCHAR",
                "document_encode_task VARCHAR",
                "trust_remote_code BOOLEAN",
            ]
            if include_runtime_option_columns
            else []
        )
        columns = [
            "model_name VARCHAR",
            "benchmark VARCHAR",
            "dataset_id VARCHAR",
            "dataset_name VARCHAR",
            "split_name VARCHAR",
            "task_name VARCHAR",
            "task_key VARCHAR",
            "score DOUBLE",
            "active_parameters BIGINT",
            "total_parameters BIGINT",
            "max_seq_length INTEGER",
            *runtime_columns,
            *variant_columns,
        ]
        con.execute(
            f"""
            CREATE TABLE task_results (
                {", ".join(columns)}
            )
            """
        )
        placeholders = ", ".join("?" for _ in rows[0])
        con.executemany(f"INSERT INTO task_results VALUES ({placeholders})", rows)
    finally:
        con.close()
