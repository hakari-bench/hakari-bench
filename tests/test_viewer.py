from __future__ import annotations

import csv
import logging
import os
import re
import time
from pathlib import Path

import duckdb
from fastapi.testclient import TestClient
import pytest

from hakari_bench.datasets import DatasetRegistry, resolve_dataset_splits, _task_name_for_split
from hakari_bench.viewer.app import (
    _database_footer_label,
    _fmt_max_len,
    _fmt_params,
    _metric_column_label,
    _metric_column_labels,
    _rounded_z_score,
    _view_group,
    _z_score_bucket_class,
    create_app,
    render_display_controls,
    render_tabs,
    render_leaderboard_csv,
    render_page,
    render_table_body,
    render_table_head,
)
from hakari_bench.viewer.analytics import ViewerSummary
from hakari_bench.viewer.config import BenchmarkConfig, OverallConfig, ViewerConfig, load_viewer_config
from hakari_bench.viewer.data import CURRENT_DUCKDB_SCHEMA_VERSION
from hakari_bench.viewer.filters import row_filter_context
from hakari_bench.viewer.leaderboard import (
    LeaderboardResult,
    LeaderboardRow,
    LeaderboardService,
    TaskScore,
    _clear_task_score_cache,
    compute_leaderboard_rows,
)
from hakari_bench.viewer import store as viewer_store
from hakari_bench.viewer.model_display import model_cell_views
from hakari_bench.viewer.store import (
    DuckDbLocation,
    HuggingFaceDuckDbSource,
    LocalDuckDbStore,
    resolve_duckdb_location,
)
from hakari_bench.viewer.state import FilterState
from hakari_bench.viewer.variant_display import VariantDisplayFlags


def test_viewer_config_uses_core_and_overall_scope_views() -> None:
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
    core_benchmarks = [
        "MNanoBEIR",
        "NanoMMTEB-v2",
        "NanoRTEB",
        "NanoMLDR",
        "NanoBRIGHT",
        "NanoCoIR",
    ]
    core_en_benchmarks = [
        "MNanoBEIR",
        "NanoRTEB",
        "NanoMLDR",
        "NanoMIRACL",
        "NanoBRIGHT",
        "NanoCoIR",
        "NanoMTEB-v2",
    ]
    all_benchmarks = [benchmark.name for benchmark in config.benchmarks]

    assert config.overall.name == "Overall"
    assert config.overall.label == "Overall"
    overall = config.overall
    assert overall.benchmark_names == all_benchmarks
    assert [component.group_by for component in overall.benchmark_components[:3]] == [
        None,
        None,
        "task_name",
    ]
    core_overall = config.overall_for_view("Core")
    assert core_overall is not None
    assert core_overall.benchmark_names == core_benchmarks
    assert [component.group_by for component in core_overall.benchmark_components] == [
        "task_name",
        None,
        None,
        None,
        None,
        None,
    ]
    core_en_overall = config.overall_for_view("Core (EN)")
    assert core_en_overall is not None
    assert core_en_overall.benchmark_names == core_en_benchmarks
    assert [component.group_by for component in core_en_overall.benchmark_components] == [
        "task_name",
        None,
        None,
        None,
        None,
        None,
        None,
    ]
    assert config.view_names[: len(all_benchmarks) + 3] == [
        "Overall",
        "Core",
        "Core (EN)",
        *all_benchmarks,
    ]
    assert "NanoCodeSearchNet" not in config.view_names
    assert "NanoBIRCO" in config.view_names
    assert "NanoDAPFAM" in config.view_names
    assert all(benchmark in config.view_names for benchmark in language_nanomteb_benchmarks)
    assert all(benchmark in overall.benchmark_names for benchmark in language_nanomteb_benchmarks)
    assert all(benchmark not in core_overall.benchmark_names for benchmark in language_nanomteb_benchmarks)
    assert "NanoMIRACL" in overall.benchmark_names
    assert "NanoMIRACL" not in core_overall.benchmark_names
    assert "NanoCMTEB" in config.view_names
    assert "NanoCMTEB" in overall.benchmark_names
    nano_cmteb = config.benchmark_for_view("NanoCMTEB")
    assert nano_cmteb is not None
    assert nano_cmteb.language_page_languages == ["zh"]
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
    language_page_languages = {
        benchmark.name: benchmark.language_page_languages
        for benchmark in config.benchmarks
        if benchmark.name.startswith("NanoMTEB-") or benchmark.name in {"NanoJMTEB-v2", "NanoFaMTEB-v2", "NanoRuMTEB", "NanoVNMTEB"}
    }
    assert language_page_languages == {
        "NanoMTEB-Dutch": ["nl"],
        "NanoMTEB-French": ["fr"],
        "NanoMTEB-German": ["de"],
        "NanoJMTEB-v2": ["ja"],
        "NanoMTEB-Korean": ["ko"],
        "NanoFaMTEB-v2": ["fa"],
        "NanoMTEB-Polish": ["pl"],
        "NanoRuMTEB": ["ru"],
        "NanoMTEB-Scandinavian": ["da", "no", "sv"],
        "NanoMTEB-Spanish": ["es"],
        "NanoMTEB-Thai": ["th"],
        "NanoVNMTEB": ["vi"],
        "NanoMTEB-v2": ["en"],
        "NanoMTEB-Misc": [],
    }
    nanomteb_misc = config.benchmark_for_view("NanoMTEB-Misc")
    assert nanomteb_misc is not None
    assert nanomteb_misc.task_labels == {
        "2022_fa": "NeuCLIR2022-fa",
        "2022_ru": "NeuCLIR2022-ru",
        "2022_zh": "NeuCLIR2022-zh",
        "cite_ru": "RuSciBench-cite-ru",
        "cocite_ru": "RuSciBench-cocite-ru",
        "en": "EuroPIRQ-en",
        "fi": "EuroPIRQ-fi",
        "pt": "EuroPIRQ-pt",
        "wmt19_de_fr": "CLSD-WMT19-de-fr",
        "wmt19_fr_de": "CLSD-WMT19-fr-de",
        "wmt21_de_fr": "CLSD-WMT21-de-fr",
        "wmt21_fr_de": "CLSD-WMT21-fr-de",
    }


def test_primary_language_view_benchmarks_define_primary_languages() -> None:
    config = load_viewer_config(Path("config/viewer"))
    registry = DatasetRegistry.load_builtin()

    missing: list[str] = []
    for benchmark in config.benchmarks:
        if benchmark.language_filter_mode != "primary_language":
            continue
        try:
            collection = registry.get_collection(benchmark.name)
        except KeyError:
            dataset_names = [benchmark.name]
        else:
            dataset_names = list(collection.datasets)
        for dataset_name in dataset_names:
            dataset = registry.get_dataset(dataset_name)
            for split_name in resolve_dataset_splits(dataset):
                task_name = _task_name_for_split(dataset, split_name)
                metadata = dataset.metadata_for_task(split_name=split_name, task_name=task_name)
                if not metadata.get("primary_languages"):
                    missing.append(f"{benchmark.name}/{dataset.name}/{task_name}")

    assert missing == []


def test_benchmark_view_groups_follow_viewer_information_architecture() -> None:
    assert _view_group("All") == "Scope presets"
    assert _view_group("Core") == "Scope presets"
    assert _view_group("Core (EN)") == "Scope presets"
    assert _view_group("Clear") == "Scope presets"
    assert _view_group("Custom") == "Scope presets"
    assert _view_group("Group") == "Scope presets"
    assert _view_group("NanoMMTEB-v2") == "Nano suites"
    assert _view_group("NanoMTEB-Dutch") == "Nano suites"
    assert _view_group("NanoJMTEB-v2") == "Nano suites"
    assert _view_group("NanoFaMTEB-v2") == "Nano suites"
    assert _view_group("NanoRuMTEB") == "Nano suites"
    assert _view_group("NanoVNMTEB") == "Nano suites"
    assert _view_group("NanoCMTEB") == "Nano suites"
    assert _view_group("MNanoBEIR") == "Nano suites"
    assert _view_group("NanoRTEB") == "Nano suites"
    assert _view_group("NanoMIRACL") == "Nano suites"
    assert _view_group("NanoMLDR") == "Nano suites"
    assert _view_group("NanoIndicQA") == "Nano suites"
    assert _view_group("NanoMuPLeR") == "Nano suites"
    assert _view_group("NanoCoIR") == "Nano suites"
    assert _view_group("NanoCodeRAG") == "Nano suites"
    assert _view_group("NanoBRIGHT") == "Nano suites"
    assert _view_group("NanoLaw") == "Nano suites"
    assert _view_group("NanoLongEmbed") == "Nano suites"
    assert _view_group("NanoBIRCO") == "Nano suites"
    assert _view_group("NanoDAPFAM") == "Nano suites"
    assert _view_group("NanoChemTEB") == "Nano suites"


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
                None,
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
            "INSERT INTO viewer_leaderboard_rows VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
            [
                "Overall",
                "all",
                True,
                False,
                False,
                False,
                3,
                2.0,
                2.0,
                "cross-encoder/example-reranker",
                88.0,
                87.0,
                87.0,
                86.0,
                3,
                10,
                12,
                8192,
                "bf16",
                None,
                "model default",
                False,
                None,
                None,
                None,
                "cross-encoder/example-reranker",
                None,
            ],
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
                3.0,
                3.0,
                "bm25",
                44.0,
                43.0,
                43.0,
                42.0,
                3,
                0,
                0,
                None,
                None,
                None,
                "model default",
                False,
                None,
                None,
                None,
                "bm25",
                None,
            ],
        )
        con.execute(
            "INSERT INTO viewer_leaderboard_rows VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
            [
                "Overall",
                "reranking",
                True,
                False,
                False,
                False,
                3,
                1.0,
                1.0,
                "model/reranker-output",
                90.0,
                89.0,
                89.0,
                88.0,
                3,
                10,
                12,
                8192,
                "bf16",
                None,
                "model default",
                False,
                None,
                None,
                None,
                "model/reranker-output",
                None,
            ],
        )
        con.execute(
            "INSERT INTO viewer_leaderboard_rows VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
            [
                "Overall",
                "reranking",
                True,
                False,
                False,
                False,
                3,
                2.0,
                2.0,
                "bm25",
                44.0,
                43.0,
                43.0,
                42.0,
                3,
                0,
                0,
                None,
                None,
                None,
                "model default",
                False,
                None,
                None,
                None,
                "bm25",
                None,
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
    model_cards_dir = tmp_path / "model_cards"
    model_cards_dir.mkdir()
    (model_cards_dir / "model__a.yaml").write_text(
        """
id: model/a
parameters:
  total: 1234
  active: 123
runtime:
  max_seq_length: 2048
""".strip(),
        encoding="utf-8",
    )

    service = LeaderboardService(duckdb_path=db_path, config=config, model_cards_path=model_cards_dir)
    result = service.get_leaderboard(
        "Overall",
        score_aggregation="micro",
        include_quantization_variants=True,
    )
    reranking_result = service.get_leaderboard(
        "Overall",
        score_target="reranking",
        score_aggregation="micro",
        include_quantization_variants=True,
    )

    assert result.expected_tasks == 3
    assert [row.model_name for row in result.rows] == ["model/a (768 dims, int8)", "bm25"]
    assert result.rows[0].model_name == "model/a (768 dims, int8)"
    assert result.rows[0].borda_score == 99.0
    assert result.rows[0].active_parameters == 123
    assert result.rows[0].total_parameters == 12
    assert result.rows[0].max_seq_length == 8192
    assert result.rows[0].embedding_variant_name == "int8"
    assert [row.model_name for row in reranking_result.rows] == ["model/reranker-output", "bm25"]
    assert reranking_result.rows[1].mean_score == 42.0
    assert [(option.code, option.label, option.task_count) for option in result.available_languages] == [
        ("en", "EN", 8),
        ("ar", "AR", 3),
        ("ja", "Japanese", 3),
    ]


def test_leaderboard_service_backfills_task_result_parameters_from_model_cards(tmp_path: Path) -> None:
    db_path = tmp_path / "results.duckdb"
    _write_task_results(
        db_path,
        [
            ("model/a", "BenchA", "bench/a", "BenchA", "a1", "a1", "BenchA::a1", 0.90, None, None, None),
            ("model/a", "BenchA", "bench/a", "BenchA", "a2", "a2", "BenchA::a2", 0.80, None, None, None),
        ],
    )
    model_cards_dir = tmp_path / "model_cards"
    model_cards_dir.mkdir()
    (model_cards_dir / "model__a.yaml").write_text(
        """
id: model/a
parameters:
  total: 456
  active: 123
runtime:
  max_seq_length: 2048
""".strip(),
        encoding="utf-8",
    )
    config = ViewerConfig(benchmarks=[BenchmarkConfig(name="BenchA")], overalls=[])

    result = LeaderboardService(
        duckdb_path=db_path,
        config=config,
        model_cards_path=model_cards_dir,
    ).get_leaderboard("BenchA")

    assert result.rows[0].active_parameters == 123
    assert result.rows[0].total_parameters == 456
    assert result.rows[0].max_seq_length == 2048


def test_leaderboard_service_backfills_language_support_from_model_cards(tmp_path: Path) -> None:
    db_path = tmp_path / "results.duckdb"
    _write_task_results(
        db_path,
        [
            ("model/a", "BenchA", "bench/a", "BenchA", "a1", "a1", "BenchA::a1", 0.90, None, None, None),
            ("model/a", "BenchA", "bench/a", "BenchA", "a2", "a2", "BenchA::a2", 0.80, None, None, None),
        ],
    )
    model_cards_dir = tmp_path / "model_cards"
    model_cards_dir.mkdir()
    (model_cards_dir / "model__a.yaml").write_text(
        """
id: model/a
language_support:
  category: english_plus
  languages:
    - ja
    - en
  marker: JP
""".strip(),
        encoding="utf-8",
    )
    config = ViewerConfig(benchmarks=[BenchmarkConfig(name="BenchA")], overalls=[])

    result = LeaderboardService(
        duckdb_path=db_path,
        config=config,
        model_cards_path=model_cards_dir,
    ).get_leaderboard("BenchA")

    assert result.rows[0].language_support_category == "english_plus"
    assert result.rows[0].language_support_languages == ("ja", "en")
    assert result.rows[0].language_support_marker == "JP"


def test_leaderboard_service_backfills_late_interaction_metadata_from_model_cards(tmp_path: Path) -> None:
    db_path = tmp_path / "results.duckdb"
    _write_task_results(
        db_path,
        [
            (
                "mixedbread-ai/mxbai-edge-colbert-v0-17m",
                "BenchA",
                "bench/a",
                "BenchA",
                "a1",
                "a1",
                "BenchA::a1",
                0.90,
                None,
                None,
                None,
            ),
            (
                "mixedbread-ai/mxbai-edge-colbert-v0-17m",
                "BenchA",
                "bench/a",
                "BenchA",
                "a2",
                "a2",
                "BenchA::a2",
                0.80,
                None,
                None,
                None,
            ),
        ],
    )
    model_cards_dir = tmp_path / "model_cards"
    model_cards_dir.mkdir()
    (model_cards_dir / "mixedbread-ai__mxbai-edge-colbert-v0-17m.yaml").write_text(
        """
id: mixedbread-ai/mxbai-edge-colbert-v0-17m
method: late-interaction
late_interaction:
  query_length: 48
  document_length: 512
  do_query_expansion: false
  attend_to_expansion_tokens: false
""".strip(),
        encoding="utf-8",
    )
    config = ViewerConfig(benchmarks=[BenchmarkConfig(name="BenchA")], overalls=[])

    result = LeaderboardService(
        duckdb_path=db_path,
        config=config,
        model_cards_path=model_cards_dir,
    ).get_leaderboard("BenchA")

    assert result.rows[0].late_interaction_query_length == 48
    assert result.rows[0].late_interaction_document_length == 512
    assert result.rows[0].late_interaction_query_expansion is False
    assert result.rows[0].late_interaction_attend_to_expansion_tokens is False


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


def test_index_renders_leaderboard_without_analysis_navigation(tmp_path: Path) -> None:
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
    config = load_viewer_config(config_dir)

    app = create_app(store=LocalDuckDbStore(DuckDbLocation(local_path=db_path)), config_dir=config_dir)
    response = TestClient(app).get("/")

    assert response.status_code == 200
    assert "<title>HAKARI-Bench leaderboard</title>" in response.text
    assert "HAKARI-Bench leaderboard" in response.text
    assert '<h1 class="flex min-w-0 items-center gap-2 text-2xl font-semibold">' in response.text
    assert '<img src="/assets/favicon.png?' in response.text
    assert 'alt="" aria-hidden="true" class="h-8 w-8 shrink-0">' in response.text
    assert 'id="hakari-docs-link"' in response.text
    assert 'href="/docs/"' in response.text
    assert 'aria-label="Open documentation"' in response.text
    assert 'data-icon="book-open"' in response.text
    assert 'id="hakari-theme-toggle"' in response.text
    assert 'aria-label="Toggle color theme"' in response.text
    assert 'data-icon="moon"' in response.text
    assert 'data-icon="sun"' in response.text
    assert '<p class="text-sm font-medium text-cyan-700">HAKARI-Bench leaderboard</p>' not in response.text
    assert (
        "🚧 WIP: This leaderboard is currently under active implementation, "
        "so specifications and data may change significantly."
    ) in response.text
    assert "DuckDB:" not in response.text
    assert f"database: local / {db_path}" in response.text
    assert "Benchmark coverage" not in response.text
    assert 'data-icon="bar-chart-3"' not in response.text
    assert 'data-testid="summary-card-models"' not in response.text
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
    assert "leaderboard-initial-loading border border-zinc-200 bg-white" in response.text
    assert 'id="leaderboard-loading-toast"' in response.text
    assert "leaderboard-loading-toast fixed bottom-4 right-4" in response.text
    assert "px-4 py-3" in response.text
    assert response.text.count('class="loading-spinner" aria-hidden="true"') == 2
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
    assert "<footer" in response.text
    assert '<footer class="mx-auto max-w-[1600px] border-t border-zinc-200 px-4 py-2 text-[11px] text-zinc-500 sm:px-6">' in response.text
    footer_html = response.text.split("<footer", 1)[1]
    assert "HAKARI-Bench leaderboard" not in footer_html
    assert "[overflow-wrap:anywhere]" in response.text
    assert response.text.index('id="leaderboard-panel"') < response.text.index("<footer")

    leaderboard_response = TestClient(app).get("/leaderboard?view=BenchA")
    assert leaderboard_response.status_code == 200
    assert "Analysis views" not in leaderboard_response.text
    assert 'class="border-t border-zinc-200 px-3 py-3 text-sm text-zinc-600"' not in leaderboard_response.text
    assert 'id="analysis-panel"' not in leaderboard_response.text
    assert "Variant impact" not in leaderboard_response.text
    assert "Reranking diagnostics" not in leaderboard_response.text
    assert "Dataset diagnostics" not in leaderboard_response.text
    assert 'hx-get="/analysis?' not in leaderboard_response.text
    assert "leaderboard-table-scroll" in leaderboard_response.text
    assert TestClient(app).get("/analysis").status_code == 404

    page_with_latest = render_page(
        viewer_config=config,
        duckdb_path=db_path,
        summary=ViewerSummary(latest_finished_at_utc="2026-05-22T20:27:54.839377+00:00"),
        database_label=f"database: local / {db_path}",
    )
    assert "Latest update: 2026-05-22T20:27:54(UTC)" in page_with_latest
    assert 'data-icon="calendar-days"' in page_with_latest
    assert page_with_latest.split("</header>", 1)[0].find("Latest update:") == -1
    assert page_with_latest.index("<footer") < page_with_latest.index("Latest update:")
    assert f"database: local / {db_path}" in page_with_latest
    assert "Latest result:" not in page_with_latest

    remote_db_path = tmp_path / "remote.duckdb"
    remote_db_path.write_bytes(b"remote duckdb")
    remote_store = LocalDuckDbStore(
        DuckDbLocation(
            local_path=remote_db_path,
            hf_source=HuggingFaceDuckDbSource(repo_id="org/dataset", filename="duckdb/hakari_bench.duckdb"),
        )
    )
    assert _database_footer_label(remote_store) == "database: remote / 365e94b76ce1"


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
    assert ":root.dark" in css_response.text
    assert "JetBrains Mono" in css_response.text
    assert ".theme-toggle" in css_response.text
    assert ".leaderboard-initial-loading" in css_response.text
    assert "min-height:clamp(18rem,42vh,28rem)" in css_response.text
    assert "padding:4rem 1.5rem" in css_response.text
    assert ".leaderboard-loading-toast.htmx-request" in css_response.text
    assert "background-color:color-mix(in srgb,var(--hakari-surface) 90%,transparent)" in css_response.text
    assert "padding:.75rem 1rem" in css_response.text
    assert ".loading-spinner" in css_response.text
    assert "hakari-leaderboard-spin" in css_response.text
    assert "--hakari-radius-lg:8px" in css_response.text
    assert "border-radius:var(--hakari-radius-lg)" in css_response.text
    assert 'nav[aria-label="Leaderboard configuration"]' in css_response.text
    assert "border-color:transparent" in css_response.text
    assert ".leaderboard-table-scroll{--hakari-model-col-width" in css_response.text
    assert "border-color:var(--hakari-border)" in css_response.text
    assert "[data-leaderboard-pending=true]" in css_response.text
    assert "button[data-leaderboard-pending=true]:after" not in css_response.text
    assert "content:\"\";display:inline-block;height:.55rem" not in css_response.text
    assert ".global-tooltip" in css_response.text
    assert ".model-tooltip" not in css_response.text
    assert ".doc-summary-trigger{background-color:transparent" in css_response.text
    assert ".doc-summary-trigger:hover" in css_response.text
    assert ".leaderboard-col-model{box-sizing:border-box;left:0" in css_response.text
    assert "overflow:hidden;width:var(--hakari-model-col-width)" in css_response.text
    assert ".borda-score-bar{position:absolute;-webkit-appearance:none;-moz-appearance:none;appearance:none" in css_response.text
    assert "top:2px;bottom:2px;left:2px;border:0;display:block;width:calc(100% - 2px);height:calc(100% - 4px)" in css_response.text
    assert "background-color:transparent;color:var(--hakari-accent);opacity:.1;pointer-events:none" in css_response.text
    assert ":root.dark .borda-score-bar{opacity:.16}" in css_response.text
    assert ":root:not(.light) .borda-score-bar{opacity:.16}" in css_response.text
    assert ".leaderboard-col-model:hover .borda-score-bar,.leaderboard-row:hover .borda-score-bar{opacity:.3}" in css_response.text
    assert ".borda-score-bar::-webkit-progress-value{background-color:var(--hakari-accent);border-radius:0 4px 4px 0}" in css_response.text
    assert ".borda-score-bar::-moz-progress-bar{background-color:var(--hakari-accent);border-radius:0 4px 4px 0}" in css_response.text
    assert ".leaderboard-row:hover>td{background-color:color-mix" in css_response.text
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
    assert "window.__hakariApplyTheme" in viewer_js_response.text
    assert "window.__hakariBindThemeToggle" in viewer_js_response.text
    assert "window.__hakariSyncThemeToggle" in viewer_js_response.text
    assert 'window.matchMedia("(prefers-color-scheme: dark)")' in viewer_js_response.text
    assert "window.__hakariShowTooltip" in viewer_js_response.text
    assert "window.__hakariHideTooltip" in viewer_js_response.text
    assert "window.__hakariPositionTooltip" in viewer_js_response.text
    assert "renderCompactModelTooltip" not in viewer_js_response.text
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
    assert "object-src 'none'" in response.headers["content-security-policy"]
    assert "frame-src 'none'" in response.headers["content-security-policy"]
    assert "form-action 'self'" in response.headers["content-security-policy"]
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
    assert "Leaderboard view" not in response.text
    assert 'data-icon="layers"' not in response.text
    assert 'class="border px-2 py-1 text-[0.8125rem] leading-tight border-cyan-700 bg-cyan-50 text-cyan-900"' in response.text
    assert 'class="border px-3 py-1.5 text-sm' not in response.text
    assert response.text.index("Retrieval") < response.text.index("Benchmark scope")
    assert response.text.index("Benchmark scope") < response.text.index("Efficiency variants")
    assert "lg:grid-cols-2" in response.text
    assert "Scope presets" not in response.text
    assert "Nano suites" not in response.text
    assert "Choose the evaluation mode first" not in response.text
    assert "Language-focused MTEB/MMTEB-style Nano suites" not in response.text
    assert "Overall" in response.text
    assert "Shows every benchmark family available in the viewer." in response.text
    assert "Retrieval" in response.text
    assert "Reranking" in response.text
    assert 'data-icon="search"' in response.text
    assert 'data-icon="list-ordered"' in response.text
    assert "Safeguard positives" not in response.text
    assert 'id="help-summary-modal"' in response.text
    assert 'class="help-summary-trigger' in response.text
    assert 'data-help-title="Benchmark scope: Overall"' in response.text
    assert 'class="control-button-group inline-flex items-center border text-[0.8125rem] leading-tight' in response.text
    assert "Overall is the default and broadest leaderboard scope." in response.text
    assert 'class="doc-summary-trigger' in response.text
    assert 'data-icon="book-open"' in response.text
    assert 'data-icon="circle-help"' in response.text
    assert 'data-icon="question-mark"' not in response.text
    doc_trigger_html = response.text.split('class="doc-summary-trigger', 1)[1].split("</button>", 1)[0]
    assert 'data-icon="book-open"' in doc_trigger_html
    assert "<circle" not in doc_trigger_html
    assert "border border-zinc-300" not in doc_trigger_html
    assert "hover:bg-cyan-50" not in doc_trigger_html
    assert "hover:border-cyan-600" not in doc_trigger_html
    assert 'data-icon="circle-help"' not in doc_trigger_html
    assert "full-corpus retrieval results" in response.text
    assert "shared candidate set" in response.text
    assert 'data-leaderboard-control="true"' in response.text
    assert response.text.count('hx-indicator="#leaderboard-loading-toast"') >= 6
    assert response.text.count('hx-sync="#leaderboard-panel:replace"') >= 6
    assert (
        'hx-get="/leaderboard?view=NanoMTEB-Japanese&amp;sort=borda_rank&amp;direction=asc'
        '&amp;group=task&amp;task_z_scores=0&amp;target=reranking"'
    ) in response.text
    scope_section = response.text.split("Benchmark scope", 1)[1].split("Efficiency variants", 1)[0]
    assert "MTEB-Japanese" in scope_section
    assert "RTEB" in scope_section
    assert "Medical" in scope_section
    assert "Multilingual retrieval" not in response.text
    assert "Code retrieval" not in response.text
    assert "Specialized domains" not in response.text
    assert "leaderboard-col-model sticky" in response.text
    assert "leaderboard-col-rank" in response.text
    assert "leaderboard-col-borda sticky" not in response.text
    assert "leaderboard-col-mean sticky" not in response.text
    assert "z-20" in response.text


def test_leaderboard_clear_scope_returns_empty_table_and_resets_language(tmp_path: Path) -> None:
    db_path = tmp_path / "results.duckdb"
    _write_task_results(
        db_path,
        [
            ("model/a", "BenchA", "bench/a", "BenchA", "a1", "a1", "a1", 0.90, 10, 12, 8192),
        ],
        dataset_metadata_rows=[("BenchA", "bench/a", "BenchA", "a1", "a1", "a1", "en", ["en"])],
    )
    config_dir = tmp_path / "config"
    config_dir.mkdir()
    (config_dir / "benchmarks.yaml").write_text(
        "benchmarks:\n  - name: BenchA\n  - name: BenchB\n",
        encoding="utf-8",
    )
    (config_dir / "overall.yaml").write_text(
        """
overalls:
  - name: Overall
    label: Overall
    benchmarks:
      - BenchA
  - name: Core
    label: Core
    benchmarks:
      - BenchA
  - name: Core (EN)
    label: Core (EN)
    benchmarks:
      - BenchB
""".strip(),
        encoding="utf-8",
    )
    service = LeaderboardService(duckdb_path=db_path, config=load_viewer_config(config_dir))

    result = service.get_leaderboard("Clear", language_filters=("ja",))
    empty_custom_result = service.get_leaderboard("Custom", selected_benchmarks=(), language_filters=("ja",))

    assert result.view_name == "Clear"
    assert result.view_label == "Clear"
    assert result.is_overall
    assert result.selected_benchmarks == ()
    assert result.expected_tasks == 0
    assert result.rows == []
    assert result.selected_languages == ()
    assert empty_custom_result.view_name == "Custom"
    assert empty_custom_result.view_label == "Custom"
    assert empty_custom_result.is_overall
    assert empty_custom_result.selected_benchmarks == ()
    assert empty_custom_result.expected_tasks == 0
    assert empty_custom_result.rows == []
    assert empty_custom_result.selected_languages == ()


def test_custom_benchmark_selection_aggregates_selected_benchmarks(tmp_path: Path) -> None:
    db_path = tmp_path / "results.duckdb"
    _write_task_results(
        db_path,
        [
            ("model/a", "BenchA", "bench/a", "BenchA", "a1", "a1", "a1", 0.90, 10, 12, 8192),
            ("model/a", "BenchB", "bench/b", "BenchB", "b1", "b1", "b1", 0.70, 10, 12, 8192),
            ("model/a", "BenchC", "bench/c", "BenchC", "c1", "c1", "c1", 0.10, 10, 12, 8192),
            ("model/b", "BenchA", "bench/a", "BenchA", "a1", "a1", "a1", 0.80, 10, 12, 8192),
            ("model/b", "BenchB", "bench/b", "BenchB", "b1", "b1", "b1", 0.40, 10, 12, 8192),
            ("model/b", "BenchC", "bench/c", "BenchC", "c1", "c1", "c1", 0.95, 10, 12, 8192),
        ],
    )
    config_dir = tmp_path / "config"
    config_dir.mkdir()
    (config_dir / "benchmarks.yaml").write_text(
        "benchmarks:\n  - name: BenchA\n  - name: BenchB\n  - name: BenchC\n",
        encoding="utf-8",
    )
    (config_dir / "overall.yaml").write_text(
        "name: Overall\nlabel: Overall\nbenchmarks:\n  - BenchA\n  - BenchB\n  - BenchC\n",
        encoding="utf-8",
    )
    service = LeaderboardService(duckdb_path=db_path, config=load_viewer_config(config_dir))

    result = service.get_leaderboard("Custom", selected_benchmarks=("BenchA", "BenchB"))

    assert result.view_name == "Custom"
    assert result.view_label == "Custom"
    assert result.is_overall
    assert result.selected_benchmarks == ("BenchA", "BenchB")
    assert result.expected_tasks == 2
    assert [row.model_name for row in result.rows] == ["model/a", "model/b"]
    assert result.rows[0].mean_score == pytest.approx(80.0)
    assert result.rows[1].mean_score == pytest.approx(60.0)


def test_custom_mnanobeir_selection_uses_task_or_language_grouping(tmp_path: Path) -> None:
    db_path = tmp_path / "results.duckdb"
    _write_task_results(
        db_path,
        [
            ("model/a", "MNanoBEIR", "NanoBEIR-en", "NanoBEIR-en", "en", "arguana", "en-arguana", 0.90, 10, 12, 8192),
            ("model/a", "MNanoBEIR", "NanoBEIR-en", "NanoBEIR-en", "en", "fever", "en-fever", 0.90, 10, 12, 8192),
            ("model/a", "MNanoBEIR", "NanoBEIR-ja", "NanoBEIR-ja", "ja", "arguana", "ja-arguana", 0.10, 10, 12, 8192),
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
        """
overalls:
  - name: Overall
    label: Overall
    benchmarks:
      - name: MNanoBEIR
        group_by: task_name
""".strip(),
        encoding="utf-8",
    )
    service = LeaderboardService(duckdb_path=db_path, config=load_viewer_config(config_dir))

    task_result = service.get_leaderboard(
        "Custom",
        selected_benchmarks=("MNanoBEIR:task_mean",),
        score_aggregation="macro",
    )
    lang_result = service.get_leaderboard(
        "Custom",
        selected_benchmarks=("MNanoBEIR:lang_mean",),
        score_aggregation="macro",
    )

    assert task_result.selected_benchmarks == ("MNanoBEIR:task_mean",)
    assert lang_result.selected_benchmarks == ("MNanoBEIR:lang_mean",)
    assert task_result.rows[0].mean_score == pytest.approx(70.0)
    assert lang_result.rows[0].mean_score == pytest.approx(50.0)


def test_benchmark_scope_buttons_toggle_custom_selection_and_reset_languages() -> None:
    result = LeaderboardResult(
        view_name="Overall",
        view_label="Overall",
        is_overall=True,
        expected_tasks=0,
        rows=[],
        available_views=["Overall", "Core", "Core (EN)", "BenchA", "BenchB", "BenchC"],
        available_view_labels={
            "Overall": "Overall",
            "Core": "Core",
            "Core (EN)": "Core (EN)",
            "BenchA": "BenchA",
            "BenchB": "BenchB",
            "BenchC": "BenchC",
        },
        selected_benchmarks=("BenchA", "BenchB"),
        score_groups=[],
        metric_columns=[],
    )

    html = render_tabs(
        result=result,
        sort="borda_rank",
        direction="asc",
        filter_state=FilterState(language_filters=("ja",)),
    )

    assert "Core (EN)" in html
    assert "Clear" in html
    assert 'class="benchmark-scope-divider mb-2 border-t border-zinc-200" aria-hidden="true"' in html
    assert 'hx-get="/leaderboard?view=Core&amp;sort=borda_rank&amp;direction=asc' in html
    core_en_button = html.split(">Core (EN)</button>", 1)[0].rsplit("<button", 1)[1]
    clear_button = html.split(">Clear</span>", 1)[0].rsplit("<button", 1)[1]
    assert "view=Core+%28EN%29" in core_en_button
    assert "lang_filter=en" in core_en_button
    assert 'data-icon="eraser"' in clear_button
    assert 'data-icon="rotate-ccw"' not in clear_button
    assert 'hx-get="/leaderboard?view=Custom&amp;sort=borda_rank&amp;direction=asc' in clear_button
    assert "lang_filter=" not in clear_button
    assert "border-cyan-700" not in clear_button
    assert html.index(">Clear</span>") < html.index("benchmark-scope-divider") < html.index('data-benchmark-toggle="BenchA"')
    bench_a_button = re.search(r'<button[^>]+data-benchmark-toggle="BenchA"[^>]+>', html)
    bench_c_button = re.search(r'<button[^>]+data-benchmark-toggle="BenchC"[^>]+>', html)
    assert bench_a_button is not None
    assert bench_c_button is not None
    bench_a_html = bench_a_button.group(0)
    bench_c_html = bench_c_button.group(0)
    assert "view=Custom" in bench_a_html
    assert "lang_filter=ja" in bench_a_html
    assert "bench=BenchB" in bench_a_html
    assert "bench=BenchA" not in bench_a_html
    assert "view=Custom" in bench_c_html
    assert "lang_filter=ja" in bench_c_html
    assert "bench=BenchA" in bench_c_html
    assert "bench=BenchB" in bench_c_html
    assert "bench=BenchC" in bench_c_html


def test_display_controls_preserve_custom_benchmark_selection() -> None:
    result = LeaderboardResult(
        view_name="Custom",
        view_label="Custom",
        is_overall=True,
        expected_tasks=0,
        rows=[],
        available_views=["Overall", "Core", "MNanoBEIR", "NanoJMTEB-v2"],
        available_view_labels={
            "Overall": "Overall",
            "Core": "Core",
            "MNanoBEIR": "MNanoBEIR",
            "NanoJMTEB-v2": "JMTEB-v2",
        },
        selected_benchmarks=("MNanoBEIR:task_mean", "NanoJMTEB-v2"),
        score_groups=[],
        metric_columns=[],
    )

    html = render_display_controls(
        result=result,
        sort="borda_rank",
        direction="asc",
        filter_state=FilterState(language_filters=("ja",)),
    )
    column_form = html.split('id="column-controls"', 1)[1].split("</form>", 1)[0]

    assert 'name="view" value="Custom"' in column_form
    assert 'name="bench" value="MNanoBEIR:task_mean"' in column_form
    assert 'name="bench" value="NanoJMTEB-v2"' in column_form
    assert 'name="lang_filter" value="ja"' in column_form


def test_mnanobeir_scope_buttons_are_exclusive_in_combined_scopes() -> None:
    result = LeaderboardResult(
        view_name="Overall",
        view_label="Overall",
        is_overall=True,
        expected_tasks=0,
        rows=[],
        available_views=["Overall", "Core", "MNanoBEIR", "BenchA"],
        available_view_labels={
            "Overall": "Overall",
            "Core": "Core",
            "MNanoBEIR": "MNanoBEIR",
            "BenchA": "BenchA",
        },
        selected_benchmarks=("MNanoBEIR:task_mean", "BenchA"),
        score_groups=[],
        metric_columns=[],
    )

    html = render_tabs(
        result=result,
        sort="borda_rank",
        direction="asc",
        filter_state=FilterState(),
    )

    task_button = re.search(r'<button[^>]+data-benchmark-toggle="MNanoBEIR:task_mean"[^>]+>', html)
    lang_button = re.search(r'<button[^>]+data-benchmark-toggle="MNanoBEIR:lang_mean"[^>]+>', html)
    assert task_button is not None
    assert lang_button is not None
    lang_html = lang_button.group(0)
    task_group_html = html[: task_button.start()].rsplit('<span class="control-button-group', 1)[1].split(">", 1)[0]
    lang_group_html = html[: lang_button.start()].rsplit('<span class="control-button-group', 1)[1].split(">", 1)[0]
    assert "border-cyan-700" in task_group_html
    assert "border-cyan-700" not in lang_group_html
    assert "bench=MNanoBEIR%3Alang_mean" in lang_html
    assert "bench=MNanoBEIR%3Atask_mean" not in lang_html
    assert "bench=BenchA" in lang_html
    assert 'data-help-title="Benchmark scope: NanoBEIR(task)"' in html
    assert 'data-help-title="Benchmark scope: NanoBEIR(lang)"' in html
    assert "Averages the multilingual NanoBEIR matrix by BEIR source task." in html
    assert "Averages the multilingual NanoBEIR matrix by language dataset." in html
    assert "MNanoBEIR is a language x task benchmark matrix" in html
    assert "Showing every language-task cell as an individual benchmark scope would make the picker hard to scan" in html


def test_leaderboard_target_reranking_uses_default_hybrid_rerank_scores(tmp_path: Path) -> None:
    from fastapi.testclient import TestClient

    db_path = tmp_path / "results.duckdb"
    _write_task_results(
        db_path,
        [
            ("model/a", "BenchA", "bench/a", "BenchA", "a1", "a1", "BenchA::a1", 0.90, 10, 12, 8192),
            ("model/b", "BenchA", "bench/a", "BenchA", "a1", "a1", "BenchA::a1", 0.80, 10, 12, 8192),
            ("bm25", "BenchA", "bench/a", "BenchA", "a1", "a1", "BenchA::a1", 0.60, 0, 0, None),
            ("model/a", "BenchA", "bench/a", "BenchA", "a2", "a2", "BenchA::a2", 0.40, 10, 12, 8192),
            ("model/b", "BenchA", "bench/a", "BenchA", "a2", "a2", "BenchA::a2", 0.30, 10, 12, 8192),
            ("bm25", "BenchA", "bench/a", "BenchA", "a2", "a2", "BenchA::a2", 0.10, 0, 0, None),
        ],
        task_diagnostics_rows=[
            ("model/a", "BenchA", "bench/a", "a1", "BenchA::a1", 0.90, 0.20, -0.70, "available", 101, "dataset_candidate_subset", "reranking_hybrid", "dataset", 1.0, 1.0),
            ("model/b", "BenchA", "bench/a", "a1", "BenchA::a1", 0.80, 0.90, 0.10, "available", 101, "dataset_candidate_subset", "reranking_hybrid", "dataset", 1.0, 1.0),
            ("model/a", "BenchA", "bench/a", "a2", "BenchA::a2", 0.40, 0.20, -0.20, "available", 101, "dataset_candidate_subset", "reranking_hybrid", "dataset", 1.0, 1.0),
            ("model/b", "BenchA", "bench/a", "a2", "BenchA::a2", 0.30, 0.90, 0.60, "available", 101, "dataset_candidate_subset", "reranking_hybrid", "dataset", 1.0, 1.0),
        ],
    )
    config_dir = tmp_path / "config"
    config_dir.mkdir()
    (config_dir / "benchmarks.yaml").write_text("benchmarks:\n  - name: BenchA\n", encoding="utf-8")
    (config_dir / "overall.yaml").write_text("name: Overall\nlabel: Overall\nbenchmarks:\n  - BenchA\n", encoding="utf-8")

    service = LeaderboardService(duckdb_path=db_path, config=load_viewer_config(config_dir))

    all_result = service.get_leaderboard("BenchA")
    rerank_result = service.get_leaderboard("BenchA", score_target="reranking")

    assert [row.model_name for row in all_result.rows] == ["model/a", "model/b", "bm25"]
    assert all_result.rows[0].mean_score == pytest.approx(65.0)
    assert [row.model_name for row in rerank_result.rows] == ["model/b", "bm25", "model/a"]
    assert rerank_result.rows[0].mean_score == pytest.approx(90.0)
    assert rerank_result.rows[1].mean_score == pytest.approx(35.0)
    assert rerank_result.score_target == "reranking"

    app = create_app(store=LocalDuckDbStore(DuckDbLocation(local_path=db_path)), config_dir=config_dir)
    response = TestClient(app).get("/leaderboard?view=BenchA&target=reranking")

    assert response.status_code == 200
    assert "target=reranking" in response.text
    assert 'data-icon="list-ordered"' in response.text
    assert "Reranking" in response.text
    assert "Safeguard positives" in response.text
    assert 'type="checkbox" class="h-4 w-4 accent-cyan-700" checked' in response.text
    assert "target=reranking_without_safeguard" in response.text
    assert 'data-help-title="Safeguard positives"' in response.text
    assert "RRF over BM25 and dense candidate rankings" in response.text
    assert "top-100 hybrid candidates" in response.text
    assert "optional rank-101 safeguard positive" in response.text
    assert "usually produced by BM25" not in response.text
    assert response.text.index("model/b") < response.text.index("bm25") < response.text.index("model/a")


def test_leaderboard_target_reranking_can_include_embedding_variants(tmp_path: Path) -> None:
    from fastapi.testclient import TestClient

    db_path = tmp_path / "results.duckdb"
    _write_task_results(
        db_path,
        [
            ("model/a", "BenchA", "bench/a", "BenchA", "a1", "a1", "BenchA::a1", 0.90, 10, 12, 8192, None, 768, None),
            (
                "model/a",
                "BenchA",
                "bench/a",
                "BenchA",
                "a1",
                "a1",
                "BenchA::a1",
                0.80,
                10,
                12,
                8192,
                "quantize_uint8_docs",
                768,
                "uint8",
            ),
        ],
        include_embedding_variant_columns=True,
    )
    con = duckdb.connect(str(db_path))
    try:
        con.execute(
            """
            INSERT INTO viewer_task_results
            SELECT * REPLACE ('reranking' AS score_target, 0.95 AS score)
            FROM viewer_task_results
            """
        )
    finally:
        con.close()
    config_dir = tmp_path / "config"
    config_dir.mkdir()
    (config_dir / "benchmarks.yaml").write_text("benchmarks:\n  - name: BenchA\n", encoding="utf-8")
    (config_dir / "overall.yaml").write_text("name: Overall\nlabel: Overall\nbenchmarks:\n  - BenchA\n", encoding="utf-8")

    service = LeaderboardService(duckdb_path=db_path, config=load_viewer_config(config_dir))
    result = service.get_leaderboard("BenchA", score_target="reranking", include_quantization_variants=True)

    assert [row.model_name for row in result.rows] == ["model/a (768 dims)", "model/a (768 dims, uint8)"]

    app = create_app(store=LocalDuckDbStore(DuckDbLocation(local_path=db_path)), config_dir=config_dir)
    response = TestClient(app).get("/leaderboard?view=BenchA&target=reranking&quantization=1")

    assert response.status_code == 200
    assert 'name="quantization" value="1" class="h-4 w-4 accent-cyan-700" checked' in response.text
    assert "&quot;ranking_model_name&quot;:&quot;model/a (768 dims, uint8)&quot;" in response.text


def test_leaderboard_target_all_excludes_reranker_models(tmp_path: Path) -> None:
    db_path = tmp_path / "results.duckdb"
    _write_task_results(
        db_path,
        [
            ("model/a", "BenchA", "bench/a", "BenchA", "a1", "a1", "BenchA::a1", 0.90, 10, 12, 8192),
            ("model/a", "BenchA", "bench/a", "BenchA", "a2", "a2", "BenchA::a2", 0.80, 10, 12, 8192),
            ("cross-encoder/example-reranker", "BenchA", "bench/a", "BenchA", "a1", "a1", "BenchA::a1", 0.70, 10, 12, 8192),
            ("cross-encoder/example-reranker", "BenchA", "bench/a", "BenchA", "a2", "a2", "BenchA::a2", 0.60, 10, 12, 8192),
        ],
        task_diagnostics_rows=[
            ("cross-encoder/example-reranker", "BenchA", "bench/a", "a1", "BenchA::a1", 0.70, 0.95, 0.25, "available", 101, "dataset_candidate_subset", "reranking_hybrid", "dataset", 1.0, 1.0),
            ("cross-encoder/example-reranker", "BenchA", "bench/a", "a2", "BenchA::a2", 0.60, 0.85, 0.25, "available", 101, "dataset_candidate_subset", "reranking_hybrid", "dataset", 1.0, 1.0),
        ],
    )
    config = ViewerConfig(
        benchmarks=[BenchmarkConfig(name="BenchA")],
        overalls=[OverallConfig(name="Overall", label="Overall", benchmarks=["BenchA"])],
    )
    service = LeaderboardService(duckdb_path=db_path, config=config)

    all_result = service.get_leaderboard("BenchA")
    rerank_result = service.get_leaderboard("BenchA", score_target="reranking")

    assert [row.model_name for row in all_result.rows] == ["model/a"]
    assert all_result.expected_tasks == 2
    assert [row.model_name for row in rerank_result.rows] == ["cross-encoder/example-reranker"]
    assert rerank_result.rows[0].mean_score == pytest.approx(90.0)


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
        score_metric: str = "ndcg@10",
        include_embedding_variants: bool,
        variant_display_flags: VariantDisplayFlags | None = None,
    ):
        nonlocal fetch_count
        fetch_count += 1
        return original_fetch(
            self,
                benchmarks=benchmarks,
                score_target=score_target,
                score_metric=score_metric,
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
        score_metric: str = "ndcg@10",
        include_embedding_variants: bool,
        variant_display_flags: VariantDisplayFlags | None = None,
    ):
        nonlocal fetch_count
        fetch_count += 1
        return original_fetch(
            self,
                benchmarks=benchmarks,
                score_target=score_target,
                score_metric=score_metric,
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
        con.execute(f"INSERT INTO viewer_task_results VALUES ({', '.join('?' for _ in row)})", row)
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
    result = service.get_leaderboard("Overall", score_aggregation="macro")

    assert [row.model_name for row in result.rows] == ["model/a", "model/b"]
    assert result.rows[0].task_count == 2
    assert result.rows[0].macro_mean == 77.5
    assert result.rows[0].micro_mean == 77.5


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
    assert "Task facets" in response.text
    assert "Language multi-select" not in response.text
    assert "max-h-72" in response.text
    assert "language-more-summary flex cursor-pointer list-none items-center gap-1.5" in response.text
    assert "More languages" in response.text
    assert 'data-language-page="ja"' in response.text
    assert (
        'hx-push-url="/?view=BenchA&amp;sort=borda_rank&amp;direction=asc&amp;group=task'
        '&amp;task_z_scores=0&amp;lang_filter=en"'
    ) in response.text
    assert 'aria-label="Task facets"' in response.text
    assert 'data-shown-count="2"' in response.text
    assert 'data-icon="search"' in response.text
    assert "Retrieval" in response.text
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
    result = service.get_leaderboard("OverallGrouped", score_aggregation="macro", show_task_scores=True)

    assert result.expected_tasks == 2
    assert [row.model_name for row in result.rows] == ["model/a", "model/b"]
    by_model = {row.model_name: row for row in result.rows}
    assert by_model["model/a"].task_count == 2
    assert by_model["model/a"].borda_score == 50.0
    assert by_model["model/b"].borda_score == 50.0
    assert by_model["model/a"].micro_mean == 70.0
    assert by_model["model/a"].macro_mean == 70.0
    assert result.metric_columns == [
        "BenchMean",
        "BenchTask",
    ]
    assert by_model["model/a"].metric_values == {
        "BenchMean": 80.0,
        "BenchTask": 60.0,
    }

    from fastapi.testclient import TestClient

    app = create_app(store=LocalDuckDbStore(DuckDbLocation(local_path=db_path)), config_dir=config_dir)
    response = TestClient(app).get("/leaderboard?view=OverallGrouped&score=macro&task_scores=1")

    assert response.status_code == 200
    assert "Overall Grouped" in response.text
    assert "BenchMean" in response.text
    assert "BenchTask" in response.text
    assert "metric%3ABenchTask" in response.text


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
            (
                "model/a",
                "BenchA",
                "bench/a",
                "BenchA",
                "a1",
                "a1",
                "a1",
                0.74,
                10,
                12,
                8192,
                "sparse_query_max_active_dims_32_sparse_document_max_active_dims_256",
                2048,
                None,
            ),
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
    ranked_facet_result = service.get_leaderboard(
        "BenchA",
        include_quantization_variants=True,
        include_truncate_variants=True,
        rank_filtered=True,
        dim_filters=("384",),
        quant_filters=("__none__",),
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
    assert [row.model_name for row in truncate_result.rows] == [
        "model/a (768 dims)",
        "model/a (512 dims)",
        "model/a (384 dims)",
        "model/b (512 dims)",
    ]
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
    assert [row.model_name for row in ranked_facet_result.rows] == ["model/a (384 dims)"]
    assert ranked_facet_result.expected_tasks == 1
    assert ranked_facet_result.rank_filtered is True
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
    default_response = TestClient(app).get("/leaderboard?view=BenchA")
    assert default_response.status_code == 200
    assert '<details id="filter-controls-panel" class="border border-zinc-200 bg-white">' in default_response.text
    assert "Advanced filters" not in default_response.text
    assert 'id="facet-filters"' not in default_response.text

    response = TestClient(app).get("/leaderboard?view=BenchA&quantization=1&model_filter=model%2Fb")

    assert response.status_code == 200
    assert "Table display" in response.text
    assert 'data-icon="table-properties"' in response.text
    assert "<span>STD</span>" in response.text
    assert "Efficiency variants" in response.text
    assert 'data-icon="git-compare-arrows"' in response.text
    assert ">Sparse pruning</span>" in response.text
    assert "Other variants" not in response.text
    assert 'data-help-title="Efficiency variants"' in response.text
    assert "Dims includes truncated dense embedding rows and uses short labels such as 512d or 512d &lt;- 1024" in response.text
    assert "Quantization includes compressed numeric formats such as int8 and binary." in response.text
    assert "Sparse pruning includes sparse encoder pruning variants" in response.text
    assert "Model family" in response.text
    assert 'id="model-type-controls"' in response.text
    assert 'data-icon="shapes"' in response.text
    assert response.text.index("Table display") < response.text.index("Efficiency variants")
    assert response.text.index("Efficiency variants") < response.text.index("Refine results")
    assert response.text.index("Table display") < response.text.index("Refine results")
    assert response.text.index("Refine results") < response.text.index("Model family") < response.text.index('id="model-filter-input"')
    assert 'name="model_type_filter" value="__none_selected__"' in response.text
    assert "Refine results" in response.text
    assert 'data-icon="filter"' in response.text
    assert '<details id="filter-controls-panel" class="border border-zinc-200 bg-white" open>' in response.text
    assert 'refine-results-summary flex cursor-pointer list-none items-center justify-between gap-2 p-2' in response.text
    assert 'data-icon="chevron-right"' in response.text
    assert "Advanced filters" not in response.text
    assert "Efficiency filters" in response.text
    assert "Run metadata" in response.text
    assert 'data-filter-detail="dim_filter"' in response.text
    assert 'data-filter-icon="ruler"' in response.text
    assert 'data-filter-detail="quant_filter"' in response.text
    assert 'data-filter-icon="binary"' in response.text
    assert 'data-filter-detail="model_type_filter"' not in response.text
    assert 'summary class="filter-detail-summary flex cursor-pointer list-none items-center px-2 py-1 text-[0.8125rem] font-medium text-zinc-800"' in response.text
    assert "grid-cols-2" in response.text
    assert "sm:grid-cols-3" in response.text
    assert response.text.count(">All</button>") == 5
    assert response.text.count(">None</button>") == 5
    assert 'id="column-controls"' in response.text
    assert 'id="variant-controls"' in response.text
    assert 'id="filter-controls"' in response.text
    assert 'id="facet-filters"' not in response.text
    assert 'from:input[type=' not in response.text
    assert 'hx-trigger="change, submit"' in response.text
    assert 'hx-include="#display-controls"' not in response.text
    assert 'data-icon="list-filter"' not in response.text
    assert ">Dims</span>" in response.text
    assert "Truncate dims" not in response.text
    assert response.text.index(">Dims</span>") < response.text.index(">Quantization</span>")
    assert "Rescore" in response.text
    assert 'id="model-filter-input"' in response.text
    assert 'name="model_filter"' in response.text
    assert 'id="model-filter-input" type="search" name="model_filter" value="model/b"\n                       class="viewer-text-input' in response.text
    assert ">Model</span>" in response.text
    assert ">Model name</span>" not in response.text
    assert "Filters leaderboard rows by model name." in response.text
    assert "jina bge keeps rows whose model name contains jina or bge" in response.text
    assert ">Task</span>" in response.text
    assert 'id="task-filter-input" type="search" name="task_filter"' in response.text
    assert 'name="query_len_min" value=""\n               class="viewer-text-input' in response.text
    assert ">Task name</span>" not in response.text
    assert "Filters task columns and task rows by benchmark" in response.text
    assert "arguana fever keeps task columns or task rows whose identifiers contain arguana or fever" in response.text
    assert "Short task names such as nq also work" in response.text
    assert "Recalculate ranks from filters" in response.text
    assert "Borda ranks, mean ranks, and visible means are recalculated" in response.text
    assert "Apply text filters" not in response.text
    assert 'class="refine-results-actions flex flex-wrap items-center gap-2"' in response.text
    assert 'data-icon="sigma"' in response.text
    assert 'class="mb-2 flex flex-wrap items-center justify-end gap-2"' not in response.text
    assert (
        response.text.index('data-icon="shapes"')
        < response.text.index('data-icon="cpu"')
        < response.text.index('class="refine-results-actions flex flex-wrap items-center gap-2"')
        < response.text.index('data-icon="sigma"')
    )
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
    assert 'name="dim_filter" value="256" class="h-4 w-4 accent-cyan-700" checked' not in response.text
    assert 'name="quant_filter" value="__none__" class="h-4 w-4 accent-cyan-700" checked' in response.text

    base_head = render_table_head(result=base_result, sort="borda_rank", direction="asc")
    quantization_head = render_table_head(result=quantization_result, sort="borda_rank", direction="asc")
    score_desc_head = render_table_head(result=base_result, sort="borda_score", direction="desc")
    assert ">Quant</span>" not in base_head
    assert ">Quant</span>" in quantization_head
    assert " ▲" not in base_head
    assert " ▼" not in base_head
    assert 'data-icon="arrow-down-narrow-wide"' in base_head
    assert 'data-icon="arrow-down-up"' not in base_head
    assert 'data-icon="arrow-down-wide-narrow"' in score_desc_head
    assert base_head.count('data-sort-active="true"') == 1
    assert 'data-sort-active="false"' not in base_head
    assert 'data-sort-active="true"' in base_head
    assert 'data-sort-direction="asc"' in base_head

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

    ranked_facet_response = TestClient(app).get(
        "/leaderboard?view=BenchA&quantization=1&truncate=1"
        "&filters=1&dim_filter=384&quant_filter=__none__&rank_filtered=1"
    )

    assert ranked_facet_response.status_code == 200
    assert "&quot;ranking_model_name&quot;:&quot;model/a (384 dims)&quot;" in ranked_facet_response.text
    assert "&quot;ranking_model_name&quot;:&quot;model/a (256 dims, int8)&quot;" not in ranked_facet_response.text
    assert "&quot;ranking_model_name&quot;:&quot;model/a (768 dims, uint8)&quot;" not in ranked_facet_response.text
    assert 'data-filter-hidden="true"' not in ranked_facet_response.text

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
    assert "Δ vs Base" in rescore_response.text

    other_variant_response = TestClient(app).get("/leaderboard?view=BenchA&other_variant=1")

    assert other_variant_response.status_code == 200
    assert 'name="other_variant" value="1" class="h-4 w-4 accent-cyan-700" checked' in other_variant_response.text
    assert "Δ vs Base" in other_variant_response.text


def test_viewer_dedupes_noop_truncate_variants_in_favor_of_original_rows(tmp_path: Path) -> None:
    from fastapi.testclient import TestClient

    db_path = tmp_path / "results.duckdb"
    _write_task_results(
        db_path,
        [
            ("model/a", "BenchA", "bench/a", "BenchA", "a1", "a1", "a1", 0.90, 10, 12, 8192, None, 384, None),
            (
                "model/a",
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
                "truncate_dim_384",
                384,
                None,
            ),
            ("model/a", "BenchA", "bench/a", "BenchA", "a1", "a1", "a1", 0.80, 10, 12, 8192, "int8", 384, "int8"),
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
                "truncate_dim_384_quantize_int8_docs",
                384,
                "int8",
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
        include_quantization_variants=True,
        include_truncate_variants=True,
    )

    assert [row.model_name for row in result.rows] == ["model/a (384 dims)", "model/a (384 dims, int8)"]
    assert {row.embedding_variant_name for row in result.rows} == {None, "int8"}

    app = create_app(store=LocalDuckDbStore(DuckDbLocation(local_path=db_path)), config_dir=config_dir)
    response = TestClient(app).get("/leaderboard?view=BenchA&quantization=1&truncate=1")

    assert response.status_code == 200
    assert "384d &lt;- 384" not in response.text
    assert "truncate_dim_384" not in response.text


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
    assert 'data-model-tooltip="true"' not in response.text
    assert "model-detail-trigger tooltip-trigger tooltip-delay" not in response.text
    assert "&quot;dtype&quot;:&quot;bf16&quot;" in response.text
    assert "&quot;attention&quot;:&quot;flash_attention_2&quot;" in response.text
    assert "&quot;trust_remote_code&quot;:true" in response.text
    assert "&quot;model_url&quot;:&quot;https://huggingface.co/jinaai/jina-embeddings-v5-text-nano&quot;" in response.text
    assert "Model Details" in response.text
    assert '<a id="model-detail-title"' in response.text
    assert 'target="_blank" rel="noopener noreferrer"' in response.text
    assert "<script>" not in response.text

    ranked_facet_response = client.get(
        "/leaderboard?view=BenchA&quantization=1&filters=1&rank_filtered=1"
        "&dim_filter=768&quant_filter=__none__"
        "&dtype_filter=bf16&attn_filter=flash_attention_2&prompt_filter=model_default"
    )

    assert ranked_facet_response.status_code == 200
    assert "&quot;ranking_model_name&quot;:&quot;jinaai/jina-embeddings-v5-text-nano (768 dims)&quot;" in ranked_facet_response.text
    assert "&quot;ranking_model_name&quot;:&quot;jinaai/jina-embeddings-v5-text-nano (768 dims, binary)&quot;" not in ranked_facet_response.text
    assert "&quot;ranking_model_name&quot;:&quot;Qwen/jina-embeddings-v5-text-nano (768 dims)&quot;" not in ranked_facet_response.text
    assert 'data-filter-hidden="true"' not in ranked_facet_response.text

    viewer_js_response = client.get("/assets/viewer.js")
    assert "JSON.parse" in viewer_js_response.text
    assert "renderCompactModelTooltip" not in viewer_js_response.text
    assert "Language" in viewer_js_response.text
    assert "model_url" in viewer_js_response.text
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

    ranked_response = TestClient(app).get("/leaderboard?view=BenchA&model_filter=GeMmA%20qwen&rank_filtered=1")

    assert ranked_response.status_code == 200
    assert 'name="rank_filtered" value="1" class="h-4 w-4 accent-cyan-700" checked' in ranked_response.text
    assert "google/gemma-embed" in ranked_response.text
    assert "Qwen/Qwen3-Embedding" in ranked_response.text
    assert "other/model" not in ranked_response.text
    assert 'data-filter-hidden="true"' not in ranked_response.text


def test_task_filter_recomputes_ranking_population_without_task_columns(tmp_path: Path) -> None:
    db_path = tmp_path / "results.duckdb"
    _write_task_results(
        db_path,
        [
            ("model/a", "BenchA", "bench/a", "BenchA", "en", "marco", "marco", 0.20, 10, 12, 8192),
            ("model/a", "BenchA", "bench/a", "BenchA", "en", "fever", "fever", 0.95, 10, 12, 8192),
            ("model/b", "BenchA", "bench/a", "BenchA", "en", "marco", "marco", 0.80, 10, 12, 8192),
            ("model/b", "BenchA", "bench/a", "BenchA", "en", "fever", "fever", 0.30, 10, 12, 8192),
        ],
    )
    config_dir = tmp_path / "config"
    config_dir.mkdir()
    (config_dir / "benchmarks.yaml").write_text("benchmarks:\n  - name: BenchA\n", encoding="utf-8")
    (config_dir / "overall.yaml").write_text("name: Overall\nlabel: Overall\nbenchmarks:\n  - BenchA\n", encoding="utf-8")
    service = LeaderboardService(duckdb_path=db_path, config=load_viewer_config(config_dir))

    full_result = service.get_leaderboard("BenchA")
    filtered_result = service.get_leaderboard("BenchA", task_filter="marco")
    ranked_filtered_result = service.get_leaderboard("BenchA", task_filter="marco", rank_filtered=True)

    assert [row.model_name for row in full_result.rows] == ["model/a", "model/b"]
    assert [row.model_name for row in filtered_result.rows] == ["model/a", "model/b"]
    assert filtered_result.expected_tasks == 2
    assert filtered_result.metric_columns == []
    assert [row.model_name for row in ranked_filtered_result.rows] == ["model/b", "model/a"]
    assert ranked_filtered_result.expected_tasks == 1
    assert ranked_filtered_result.rank_filtered is True
    assert [(row.model_name, row.task_count, row.mean_score, row.borda_score) for row in ranked_filtered_result.rows] == [
        ("model/b", 1, pytest.approx(80.0), pytest.approx(100.0)),
        ("model/a", 1, pytest.approx(20.0), pytest.approx(0.0)),
    ]
    assert ranked_filtered_result.metric_columns == ["marco"]


def test_overall_task_filter_renders_single_task_mean_column(tmp_path: Path) -> None:
    db_path = tmp_path / "results.duckdb"
    _write_task_results(
        db_path,
        [
            ("model/a", "BenchA", "bench/a", "BenchA", "en", "marco", "BenchA::marco", 0.20, 10, 12, 8192),
            ("model/a", "BenchB", "bench/b", "BenchB", "en", "marco", "BenchB::marco", 0.90, 10, 12, 8192),
            ("model/b", "BenchA", "bench/a", "BenchA", "en", "marco", "BenchA::marco", 0.80, 10, 12, 8192),
            ("model/b", "BenchB", "bench/b", "BenchB", "en", "marco", "BenchB::marco", 0.30, 10, 12, 8192),
        ],
    )
    config_dir = tmp_path / "config"
    config_dir.mkdir()
    (config_dir / "benchmarks.yaml").write_text("benchmarks:\n  - name: BenchA\n  - name: BenchB\n", encoding="utf-8")
    (config_dir / "overall.yaml").write_text("name: Overall\nlabel: Overall\nbenchmarks:\n  - BenchA\n  - BenchB\n", encoding="utf-8")
    service = LeaderboardService(duckdb_path=db_path, config=load_viewer_config(config_dir))

    result = service.get_leaderboard("Overall", task_filter="marco", rank_filtered=True)
    head = render_table_head(result=result, sort="borda_rank", direction="asc")
    body = render_table_body(result=result)

    assert result.is_overall is True
    assert [(row.model_name, row.mean_score, row.macro_mean, row.micro_mean) for row in result.rows] == [
        ("model/a", pytest.approx(55.0), pytest.approx(55.0), pytest.approx(55.0)),
        ("model/b", pytest.approx(55.0), pytest.approx(55.0), pytest.approx(55.0)),
    ]
    assert "Macro Mean" not in head
    assert "Micro Mean" not in head
    assert "Mean Score" in head
    assert body.count(">55.00</td>") >= 2


def test_leaderboard_table_keeps_model_name_as_leftmost_sticky_column(tmp_path: Path) -> None:
    db_path = tmp_path / "results.duckdb"
    long_task = "legal_bench_corporate_lobbying"
    _write_task_results(
        db_path,
        [
            ("org/model-a", "BenchA", "bench/a", "BenchA", long_task, long_task, long_task, 0.90, 10, 12, 8192),
            ("org/model-b", "BenchA", "bench/a", "BenchA", long_task, long_task, long_task, 0.80, 20, 24, 4096),
        ],
    )
    config_dir = tmp_path / "config"
    config_dir.mkdir()
    (config_dir / "benchmarks.yaml").write_text("benchmarks:\n  - name: BenchA\n", encoding="utf-8")
    (config_dir / "overall.yaml").write_text("name: Overall\nlabel: Overall\nbenchmarks:\n  - BenchA\n", encoding="utf-8")
    service = LeaderboardService(duckdb_path=db_path, config=load_viewer_config(config_dir))
    result = service.get_leaderboard("BenchA", show_task_scores=True)

    head = render_table_head(result=result, sort="borda_rank", direction="asc")
    body = render_table_body(result=result)

    assert head.index("Model Name") < head.index("Borda")
    assert body.index("model-a") < body.index(">1</td>")
    assert 'data-column-key="model_name"' in head
    assert (
        'data-column-key="model_name" class="bg-zinc-100 py-1 text-xs font-semibold text-zinc-600 '
        'text-left px-2 uppercase leaderboard-col-model sticky z-20'
    ) in head
    assert (
        'data-column-key="borda_rank" class="bg-zinc-100 py-1 text-xs font-semibold text-zinc-600 '
        'text-left px-2 uppercase leaderboard-col-rank'
    ) in head
    assert (
        'data-column-key="mean_rank" class="bg-zinc-100 py-1 text-xs font-semibold text-zinc-600 '
        'text-left px-2 uppercase leaderboard-col-rank'
    ) in head
    assert (
        '<span class="min-w-0 text-left leading-tight block max-w-full truncate tooltip-trigger cursor-pointer" '
        f'data-metric-column-full-name="{long_task}"'
    ) in head
    assert body.count('class="borda-score-bar"') == 2
    assert 'class="borda-score-bar" value="100.00" max="100"' in body
    assert 'class="borda-score-bar" value="0.00" max="100"' in body


def test_leaderboard_model_name_borda_score_bar_handles_one_visible_filtered_row(tmp_path: Path) -> None:
    db_path = tmp_path / "results.duckdb"
    _write_task_results(
        db_path,
        [
            ("org/model-a", "BenchA", "bench/a", "BenchA", "task-a", "task-a", "task-a", 0.90, 10, 12, 8192),
            ("org/model-b", "BenchA", "bench/a", "BenchA", "task-a", "task-a", "task-a", 0.80, 20, 24, 4096),
        ],
    )
    config_dir = tmp_path / "config"
    config_dir.mkdir()
    (config_dir / "benchmarks.yaml").write_text("benchmarks:\n  - name: BenchA\n", encoding="utf-8")
    (config_dir / "overall.yaml").write_text("name: Overall\nlabel: Overall\nbenchmarks:\n  - BenchA\n", encoding="utf-8")
    service = LeaderboardService(duckdb_path=db_path, config=load_viewer_config(config_dir))
    result = service.get_leaderboard("BenchA", show_task_scores=True)
    filter_context = row_filter_context(result.rows, FilterState(filters_active=True, model_filter="model-a"))

    body = render_table_body(result=result, filter_context=filter_context)

    assert body.count('class="borda-score-bar"') == 1
    assert 'class="borda-score-bar" value="100.00" max="100"' in body
    assert body.count('data-filter-hidden="true"') == 1


def test_leaderboard_model_name_borda_score_bar_scales_to_visible_max_score() -> None:
    result = LeaderboardResult(
        view_name="BenchA",
        view_label="Bench A",
        is_overall=False,
        expected_tasks=1,
        rows=[
            LeaderboardRow(
                borda_rank=1,
                mean_rank=1,
                model_name="model/top",
                borda_score=88.10,
                mean_score=88.10,
                task_count=1,
            ),
            LeaderboardRow(
                borda_rank=2,
                mean_rank=2,
                model_name="model/middle",
                borda_score=44.05,
                mean_score=44.05,
                task_count=1,
            ),
            LeaderboardRow(
                borda_rank=3,
                mean_rank=3,
                model_name="model/bottom",
                borda_score=3.30,
                mean_score=3.30,
                task_count=1,
            ),
        ],
        available_views=["BenchA"],
        available_view_labels={"BenchA": "Bench A"},
        score_groups=[],
        metric_columns=[],
    )

    body = render_table_body(result=result)
    filtered_body = render_table_body(
        result=result,
        filter_context=row_filter_context(result.rows, FilterState(filters_active=True, model_filter="middle")),
    )

    assert 'class="borda-score-bar" value="100.00" max="100"' in body
    assert 'class="borda-score-bar" value="50.00" max="100"' in body
    assert 'class="borda-score-bar" value="3.75" max="100"' in body
    assert filtered_body.count('class="borda-score-bar"') == 1
    assert 'class="borda-score-bar" value="100.00" max="100"' in filtered_body


def test_leaderboard_model_name_borda_score_bar_handles_no_visible_filtered_rows(tmp_path: Path) -> None:
    db_path = tmp_path / "results.duckdb"
    _write_task_results(
        db_path,
        [
            ("org/model-a", "BenchA", "bench/a", "BenchA", "task-a", "task-a", "task-a", 0.90, 10, 12, 8192),
            ("org/model-b", "BenchA", "bench/a", "BenchA", "task-a", "task-a", "task-a", 0.80, 20, 24, 4096),
        ],
    )
    config_dir = tmp_path / "config"
    config_dir.mkdir()
    (config_dir / "benchmarks.yaml").write_text("benchmarks:\n  - name: BenchA\n", encoding="utf-8")
    (config_dir / "overall.yaml").write_text("name: Overall\nlabel: Overall\nbenchmarks:\n  - BenchA\n", encoding="utf-8")
    service = LeaderboardService(duckdb_path=db_path, config=load_viewer_config(config_dir))
    result = service.get_leaderboard("BenchA", show_task_scores=True)
    filter_context = row_filter_context(result.rows, FilterState(filters_active=True, model_filter="missing-model"))

    body = render_table_body(result=result, filter_context=filter_context)

    assert 'class="borda-score-bar"' not in body
    assert body.count('data-filter-hidden="true"') == 2


def test_leaderboard_model_name_cell_omits_language_marker_and_keeps_language_details(tmp_path: Path) -> None:
    db_path = tmp_path / "results.duckdb"
    _write_task_results(
        db_path,
        [
            ("model/en-ja", "BenchA", "bench/a", "BenchA", "task-a", "task-a", "task-a", 0.90, 10, 12, 8192),
            ("model/multi", "BenchA", "bench/a", "BenchA", "task-a", "task-a", "task-a", 0.80, 20, 24, 4096),
            ("model/en", "BenchA", "bench/a", "BenchA", "task-a", "task-a", "task-a", 0.70, 30, 36, 2048),
        ],
    )
    model_cards_dir = tmp_path / "model_cards"
    model_cards_dir.mkdir()
    (model_cards_dir / "model__en-ja.yaml").write_text(
        """
id: model/en-ja
language_support:
  category: english_plus
  languages:
    - ja
    - en
  marker: JP
""".strip(),
        encoding="utf-8",
    )
    (model_cards_dir / "model__multi.yaml").write_text(
        """
id: model/multi
language_support:
  category: multilingual
""".strip(),
        encoding="utf-8",
    )
    (model_cards_dir / "model__en.yaml").write_text(
        """
id: model/en
language_support:
  category: english_only
  languages:
    - en
""".strip(),
        encoding="utf-8",
    )
    config = ViewerConfig(benchmarks=[BenchmarkConfig(name="BenchA")], overalls=[])
    result = LeaderboardService(
        duckdb_path=db_path,
        config=config,
        model_cards_path=model_cards_dir,
    ).get_leaderboard("BenchA")

    body = render_table_body(result=result)

    assert 'data-language-support-category=' not in body
    assert "language-support-marker" not in body
    assert 'data-icon="languages"' not in body
    assert ">JP</span>" not in body
    assert ">EN</span>" not in body
    assert "&quot;language_support_label&quot;:&quot;ja, en&quot;" in body
    assert "&quot;language_support_label&quot;:&quot;Multilingual&quot;" in body
    assert "&quot;language_support_label&quot;:&quot;English only&quot;" in body
    assert "border-cyan-200 bg-cyan-50" not in body


def test_leaderboard_table_hides_sparse_dimension_values() -> None:
    result = LeaderboardResult(
        view_name="BenchA",
        view_label="Bench A",
        is_overall=False,
        expected_tasks=1,
        rows=[
            LeaderboardRow(
                borda_rank=1,
                mean_rank=1,
                model_name="org/sparse-encoder",
                model_type="sparse",
                borda_score=100,
                mean_score=100,
                task_count=1,
                embedding_dim=30000,
            )
        ],
        available_views=["BenchA"],
        available_view_labels={"BenchA": "Bench A"},
        score_groups=[],
        metric_columns=[],
    )

    body = render_table_body(result=result)

    assert "30,000" not in body
    assert ">sparse</span>" in body
    assert '<tr class="leaderboard-row odd:bg-white even:bg-zinc-50">' in body
    assert '<td class="leaderboard-col-model sticky z-10' in body
    assert '<td class="leaderboard-col-rank px-2 py-1 text-left tabular-nums">' in body
    assert "leaderboard-col-borda sticky" not in body
    assert "leaderboard-col-mean sticky" not in body
    assert '<td class="px-2 py-1 text-left tabular-nums">' in body


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
    assert "Run metadata" in response.text
    assert 'data-icon="cpu"' in response.text
    assert 'data-filter-detail="attn_filter"' in response.text
    assert 'data-filter-detail="dtype_filter"' in response.text
    assert 'data-filter-detail="prompt_filter"' in response.text
    assert 'data-filter-icon="scan-eye"' in response.text
    assert 'data-filter-icon="type"' in response.text
    assert 'data-filter-icon="message-square-text"' in response.text
    assert ">Attention</span>" in response.text
    assert ">Dtype</span>" in response.text
    assert ">Prompt</span>" in response.text
    assert 'data-column-key="attn_implementation"' not in response.text
    assert 'data-column-key="dtype"' not in response.text
    assert 'data-column-key="prompt_summary"' not in response.text
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
            ("model/a", "NanoMMTEB-v2", "NanoMMTEB-v2", "NanoMMTEB-v2", "mmteb", "mmteb", "mmteb", 0.65, 10, 12, 8192),
            ("model/b", "NanoMMTEB-v2", "NanoMMTEB-v2", "NanoMMTEB-v2", "mmteb", "mmteb", "mmteb", 0.55, 20, 24, 4096),
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
  - name: NanoMMTEB-v2
""".strip(),
        encoding="utf-8",
    )
    (config_dir / "overall.yaml").write_text(
        "name: Overall\nlabel: Overall\nbenchmarks:\n  - MNanoBEIR\n  - NanoMMTEB-v2\n",
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
    mmteb_response = TestClient(app).get("/leaderboard?view=NanoMMTEB-v2&task_scores=1")

    assert response.status_code == 200
    assert mmteb_response.status_code == 200
    assert "M-BEIR(task)" in response.text
    assert "M-BEIR(lang)" in response.text
    assert "MMTEB-v2" in response.text
    lang_scope_section = response.text.split("Benchmark scope", 1)[1].split("Table display", 1)[0]
    mmteb_scope_section = mmteb_response.text.split("Benchmark scope", 1)[1].split("Table display", 1)[0]
    for scope_section in [lang_scope_section, mmteb_scope_section]:
        scope_positions = [
            scope_section.index("M-BEIR(task)"),
            scope_section.index("M-BEIR(lang)"),
            scope_section.rindex("MMTEB-v2"),
        ]
        assert scope_positions == sorted(scope_positions)
    assert "Task Mean" not in response.text
    assert 'aria-label="Score groups"' not in response.text
    assert "group=task_mean" in response.text
    assert "group=lang_mean" in response.text
    assert ">Tasks</span>" in response.text
    assert "Task score columns" not in response.text
    assert 'name="task_scores" value="1" class="h-4 w-4 accent-cyan-700" checked' in response.text
    assert "Mean Score" in response.text
    assert ">BEIR-ja</span>" in response.text
    assert "w-[5.5rem] min-w-[5.5rem] max-w-[5.5rem]" in response.text
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


def test_primary_language_pages_use_metadata_primary_languages_first(tmp_path: Path) -> None:
    db_path = tmp_path / "results.duckdb"
    rows = [
        (
            "model/a",
            "MNanoBEIR",
            "hakari-bench/NanoBEIR-no",
            "NanoBEIR-norwegian",
            "nfcorpus",
            "nfcorpus",
            "MNanoBEIR::NanoBEIR-no::nfcorpus",
            0.90,
            10,
            12,
            8192,
        ),
        (
            "model/a",
            "NanoMTEB-Misc",
            "hakari-bench/NanoMTEB-Misc",
            "NanoMTEB-Misc",
            "wmt19_de_fr",
            "wmt19_de_fr",
            "NanoMTEB-Misc::wmt19_de_fr",
            0.80,
            10,
            12,
            8192,
        ),
    ]
    metadata_rows = [
        (
            "MNanoBEIR",
            "hakari-bench/NanoBEIR-no",
            "NanoBEIR-norwegian",
            "nfcorpus",
            "nfcorpus",
            "MNanoBEIR::NanoBEIR-no::nfcorpus",
            "multilingual",
            ["en", "no", "da"],
            ["no"],
        ),
        (
            "NanoMTEB-Misc",
            "hakari-bench/NanoMTEB-Misc",
            "NanoMTEB-Misc",
            "wmt19_de_fr",
            "wmt19_de_fr",
            "NanoMTEB-Misc::wmt19_de_fr",
            "multilingual",
            ["en", "de", "fr"],
            ["de", "fr"],
        ),
    ]
    _write_task_results(db_path, rows, dataset_metadata_rows=metadata_rows)
    config_dir = tmp_path / "config"
    config_dir.mkdir()
    (config_dir / "benchmarks.yaml").write_text(
        """
benchmarks:
  - name: MNanoBEIR
    language_filter_mode: primary_language
  - name: NanoMTEB-Misc
    language_filter_mode: primary_language
""".strip(),
        encoding="utf-8",
    )
    (config_dir / "overall.yaml").write_text(
        "name: Overall\nlabel: Overall\nbenchmarks:\n  - MNanoBEIR\n  - NanoMTEB-Misc\n",
        encoding="utf-8",
    )

    service = LeaderboardService(duckdb_path=db_path, config=load_viewer_config(config_dir))
    result = service.get_leaderboard("Overall")
    en_result = service.get_leaderboard("Overall", language_filters=("en",))
    no_result = service.get_leaderboard("Overall", language_filters=("no",))
    de_result = service.get_leaderboard("Overall", language_filters=("de",))
    fr_result = service.get_leaderboard("Overall", language_filters=("fr",))

    assert [(option.code, option.task_count) for option in result.available_languages] == [
        ("de", 1),
        ("fr", 1),
        ("no", 1),
    ]
    assert en_result.selected_languages == ()
    assert no_result.selected_languages == ("no",)
    assert no_result.expected_tasks == 1
    assert de_result.selected_languages == ("de",)
    assert de_result.expected_tasks == 1
    assert fr_result.selected_languages == ("fr",)
    assert fr_result.expected_tasks == 1


def test_overall_language_pages_use_component_language_policy(tmp_path: Path) -> None:
    db_path = tmp_path / "results.duckdb"
    rows = []
    metadata_rows = []
    for benchmark, dataset_name, primary_language, languages, score in [
        ("MNanoBEIR", "NanoBEIR-en", "en", ["en"], 0.10),
        ("MNanoBEIR", "NanoBEIR-no", "multilingual", ["no", "en", "da"], 0.90),
        ("NanoMTEB-v2", "NanoMTEB-v2", "en", ["en"], 0.30),
        ("NanoMTEB-Dutch", "NanoMTEB-Dutch", "multilingual", ["nl", "en"], 0.80),
    ]:
        task_name = "nfcorpus" if benchmark == "MNanoBEIR" else dataset_name
        task_key = f"{benchmark}::{dataset_name}::{task_name}"
        rows.append(
            (
                "model/a",
                benchmark,
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
                benchmark,
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
  - name: NanoMTEB-v2
    language_page_languages: [en]
  - name: NanoMTEB-Dutch
    language_page_languages: [nl]
""".strip(),
        encoding="utf-8",
    )
    (config_dir / "overall.yaml").write_text(
        """
overalls:
  - name: All
    label: All
    benchmarks:
      - MNanoBEIR
      - NanoMTEB-v2
      - NanoMTEB-Dutch
""".strip(),
        encoding="utf-8",
    )

    service = LeaderboardService(duckdb_path=db_path, config=load_viewer_config(config_dir))
    result = service.get_leaderboard("All")
    en_result = service.get_leaderboard("All", language_filters=("en",))

    assert [(option.code, option.task_count) for option in result.available_languages] == [
        ("en", 2),
        ("nl", 1),
        ("no", 1),
    ]
    assert en_result.selected_languages == ("en",)
    assert en_result.expected_tasks == 2
    assert en_result.rows[0].task_count == 2
    assert en_result.rows[0].mean_score == 20.0


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


def test_language_specific_benchmark_pages_use_configured_language_page_languages(tmp_path: Path) -> None:
    db_path = tmp_path / "results.duckdb"
    rows = []
    metadata_rows = []
    for split_name, language, languages, score in [
        ("dutch_only", "nl", ["nl"], 0.40),
        ("dutch_cross", "multilingual", ["en", "nl"], 0.80),
        ("zh_only", "zh", ["zh"], 0.50),
        ("zh_cross", "multilingual", ["zh", "ja"], 0.70),
        ("scandinavian_en", "multilingual", ["no", "en", "de"], 0.60),
        ("scandinavian_sv", "sv", ["sv"], 0.90),
    ]:
        benchmark = "NanoMTEB-Dutch" if split_name.startswith("dutch") else "NanoCMTEB"
        if split_name.startswith("scandinavian"):
            benchmark = "NanoMTEB-Scandinavian"
        task_key = f"{benchmark}::{split_name}"
        rows.append(
            (
                "model/a",
                benchmark,
                f"hakari-bench/{benchmark}",
                benchmark,
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
                benchmark,
                f"hakari-bench/{benchmark}",
                benchmark,
                split_name,
                split_name,
                task_key,
                language,
                languages,
            )
        )
    _write_task_results(db_path, rows, dataset_metadata_rows=metadata_rows)
    config_dir = tmp_path / "config"
    config_dir.mkdir()
    (config_dir / "benchmarks.yaml").write_text(
        """
benchmarks:
  - name: NanoCMTEB
    language_page_languages: [zh]
  - name: NanoMTEB-Dutch
    language_page_languages: [nl]
  - name: NanoMTEB-Scandinavian
    language_page_languages: [da, "no", sv]
""".strip(),
        encoding="utf-8",
    )
    (config_dir / "overall.yaml").write_text(
        "name: Overall\nlabel: Overall\nbenchmarks:\n  - NanoCMTEB\n  - NanoMTEB-Dutch\n  - NanoMTEB-Scandinavian\n",
        encoding="utf-8",
    )

    service = LeaderboardService(duckdb_path=db_path, config=load_viewer_config(config_dir))
    dutch = service.get_leaderboard("NanoMTEB-Dutch")
    dutch_en = service.get_leaderboard("NanoMTEB-Dutch", language_filters=("en",))
    dutch_nl = service.get_leaderboard("NanoMTEB-Dutch", language_filters=("nl",))
    cmteb = service.get_leaderboard("NanoCMTEB")
    cmteb_ja = service.get_leaderboard("NanoCMTEB", language_filters=("ja",))
    cmteb_zh = service.get_leaderboard("NanoCMTEB", language_filters=("zh",))
    scandinavian = service.get_leaderboard("NanoMTEB-Scandinavian")

    assert [(option.code, option.task_count) for option in dutch.available_languages] == [("nl", 2)]
    assert dutch_en.selected_languages == ()
    assert dutch_en.expected_tasks == 2
    assert dutch_nl.selected_languages == ("nl",)
    assert dutch_nl.expected_tasks == 2
    assert [(option.code, option.task_count) for option in cmteb.available_languages] == [("zh", 2)]
    assert cmteb_ja.selected_languages == ()
    assert cmteb_zh.selected_languages == ("zh",)
    assert cmteb_zh.expected_tasks == 2
    assert [(option.code, option.task_count) for option in scandinavian.available_languages] == [("no", 1), ("sv", 1)]


def test_task_score_display_can_show_all_tasks_and_filter_task_columns(tmp_path: Path) -> None:
    from fastapi.testclient import TestClient

    db_path = tmp_path / "results.duckdb"
    _write_task_results(
        db_path,
        [
            ("model/a", "BenchA", "bench/a", "BenchA", "NanoArguAna", "arguana", "bench::arguana", 0.90, 10, 12, 8192),
            ("model/a", "BenchA", "bench/a", "BenchA", "NanoFEVER", "fever", "bench::fever", 0.80, 10, 12, 8192),
            ("model/a", "BenchA", "bench/a", "BenchA", "NanoNQ", "nq", "bench::nq", 0.50, 10, 12, 8192),
            ("model/b", "BenchA", "bench/a", "BenchA", "NanoArguAna", "arguana", "bench::arguana", 0.70, 10, 12, 8192),
            ("model/b", "BenchA", "bench/a", "BenchA", "NanoFEVER", "fever", "bench::fever", 0.60, 10, 12, 8192),
            ("model/b", "BenchA", "bench/a", "BenchA", "NanoNQ", "nq", "bench::nq", 0.40, 10, 12, 8192),
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
    assert full_result.metric_columns == ["arguana", "fever", "nq"]
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

    nq_response = TestClient(app).get("/leaderboard?view=BenchA&task_scores=1&task_filter=nq")

    assert nq_response.status_code == 200
    assert 'value="nq"' in nq_response.text
    assert ">nq</span>" in nq_response.text
    assert ">arguana</span>" not in nq_response.text
    assert ">fever</span>" not in nq_response.text


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
    mean_only_result = service.get_leaderboard(
        "BenchA",
        include_truncate_variants=True,
        show_task_z_scores=True,
    )
    mean_only_rows_by_name = {row.model_name: row for row in mean_only_result.rows}

    assert mean_only_result.show_task_scores is False
    assert mean_only_result.show_task_z_scores is True
    assert mean_only_result.metric_columns == []
    assert mean_only_rows_by_name["model/a"].mean_score_z == pytest.approx(1.0)
    assert mean_only_rows_by_name["model/b"].mean_score_z == pytest.approx(-1.0)
    assert mean_only_rows_by_name["model/a"].metric_z_values == {}

    result = service.get_leaderboard(
        "BenchA",
        include_truncate_variants=True,
        show_task_scores=True,
        show_task_z_scores=True,
    )
    rows_by_name = {row.model_name: row for row in result.rows}

    assert result.show_task_scores is True
    assert result.show_task_z_scores is True
    assert rows_by_name["model/a"].mean_score_z == pytest.approx(1.0)
    assert rows_by_name["model/b"].mean_score_z == pytest.approx(-1.0)
    assert rows_by_name["model/a"].metric_values["arguana"] == 90.0
    assert rows_by_name["model/a"].metric_z_values["arguana"] == pytest.approx(1.0)
    assert rows_by_name["model/b"].metric_z_values["arguana"] == pytest.approx(-1.0)
    variant_row = next(row for row in result.rows if row.embedding_variant_name == "truncate_dim_256")
    assert variant_row.mean_score_z == pytest.approx(0.27)
    assert variant_row.metric_z_values["arguana"] == pytest.approx(0.27)
    assert "fever" not in variant_row.metric_z_values

    app = create_app(store=LocalDuckDbStore(DuckDbLocation(local_path=db_path)), config_dir=config_dir)
    response = TestClient(app).get("/leaderboard?view=BenchA&truncate=1&task_z_scores=1")

    assert response.status_code == 200
    assert "Table display" in response.text
    assert "<span>STD</span>" in response.text
    assert "Task std display" not in response.text
    assert 'name="task_z_scores" value="1" class="h-4 w-4 accent-cyan-700" checked' in response.text
    assert "task-z-score task-z-pos-100" in response.text
    assert "task-z-score task-z-neg-100" in response.text
    assert '<span class="task-z-score-delta">+1.00σ</span>' in response.text
    assert "metric%3Aarguana" not in response.text

    task_column_response = TestClient(app).get("/leaderboard?view=BenchA&truncate=1&task_scores=1&task_z_scores=1")
    assert task_column_response.status_code == 200
    assert "task-z-score task-z-pos-025" in task_column_response.text
    assert '<span class="task-z-score-value">90.00</span>' in task_column_response.text
    assert '<span class="task-z-score-value">82.70</span>' in task_column_response.text
    assert '<span class="task-z-score-delta">+0.27σ</span>' in task_column_response.text

    ranked_std_response = TestClient(app).get(
        "/leaderboard?view=BenchA&truncate=1&task_scores=1&task_z_scores=1&task_ranks=1"
    )
    assert ranked_std_response.status_code == 200
    assert '<span class="task-rank-label">[1]</span>' in ranked_std_response.text
    assert "task-z-score-with-rank" in ranked_std_response.text
    assert '<span class="task-z-score-value">90.00</span>' in ranked_std_response.text
    assert '<span class="task-z-score-delta">+1.00σ</span>' in ranked_std_response.text


def test_task_rank_display_uses_per_task_average_ranks(tmp_path: Path) -> None:
    db_path = tmp_path / "results.duckdb"
    _write_task_results(
        db_path,
        [
            ("model/a", "BenchA", "bench/a", "BenchA", "arguana", "arguana", "arguana", 0.90, 10, 12, 8192),
            ("model/b", "BenchA", "bench/a", "BenchA", "arguana", "arguana", "arguana", 0.80, 10, 12, 8192),
            ("model/c", "BenchA", "bench/a", "BenchA", "arguana", "arguana", "arguana", 0.80, 10, 12, 8192),
            ("model/d", "BenchA", "bench/a", "BenchA", "arguana", "arguana", "arguana", 0.70, 10, 12, 8192),
        ],
    )
    config_dir = tmp_path / "config"
    config_dir.mkdir()
    (config_dir / "benchmarks.yaml").write_text("benchmarks:\n  - name: BenchA\n", encoding="utf-8")
    (config_dir / "overall.yaml").write_text("name: Overall\nlabel: Overall\nbenchmarks:\n  - BenchA\n", encoding="utf-8")

    service = LeaderboardService(duckdb_path=db_path, config=load_viewer_config(config_dir))
    result = service.get_leaderboard("BenchA", show_task_scores=True, show_task_ranks=True)
    rows_by_name = {row.model_name: row for row in result.rows}

    assert result.show_task_scores is True
    assert result.show_task_ranks is True
    assert rows_by_name["model/a"].metric_rank_values["arguana"] == 1
    assert rows_by_name["model/b"].metric_rank_values["arguana"] == 2.5
    assert rows_by_name["model/c"].metric_rank_values["arguana"] == 2.5
    assert rows_by_name["model/d"].metric_rank_values["arguana"] == 4

    response = TestClient(create_app(store=LocalDuckDbStore(DuckDbLocation(local_path=db_path)), config_dir=config_dir)).get(
        "/leaderboard?view=BenchA&task_ranks=1"
    )

    assert response.status_code == 200
    assert "<span>Task ranks</span>" in response.text
    assert 'name="task_scores" value="1" class="h-4 w-4 accent-cyan-700" checked' in response.text
    assert 'name="task_ranks" value="1" class="h-4 w-4 accent-cyan-700" checked' in response.text
    assert 'name="task_scores" value="1"' in response.text
    assert '<span class="task-rank-label">[1]</span>' not in response.text
    assert '<span class="task-rank-label">[T2]</span>' not in response.text
    assert '<span class="task-rank-score-value">' not in response.text
    assert '>1</td>' in response.text
    assert '>T2</td>' in response.text
    assert '>4</td>' in response.text
    assert ">2.5</td>" not in response.text
    assert "sort=metric%3Aarguana" in response.text


def test_std_display_applies_to_overall_macro_and_micro_means(tmp_path: Path) -> None:
    from fastapi.testclient import TestClient

    db_path = tmp_path / "results.duckdb"
    _write_task_results(
        db_path,
        [
            ("model/a", "BenchA", "bench/a", "BenchA", "a1", "a1", "a1", 0.90, 10, 12, 8192),
            ("model/a", "BenchA", "bench/a", "BenchA", "a2", "a2", "a2", 0.90, 10, 12, 8192),
            ("model/a", "BenchB", "bench/b", "BenchB", "b1", "b1", "b1", 0.50, 10, 12, 8192),
            ("model/b", "BenchA", "bench/a", "BenchA", "a1", "a1", "a1", 0.70, 20, 24, 4096),
            ("model/b", "BenchA", "bench/a", "BenchA", "a2", "a2", "a2", 0.70, 20, 24, 4096),
            ("model/b", "BenchB", "bench/b", "BenchB", "b1", "b1", "b1", 0.50, 20, 24, 4096),
            (
                "model/a",
                "BenchA",
                "bench/a",
                "BenchA",
                "a1",
                "a1",
                "a1",
                0.85,
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
                "a2",
                "a2",
                "a2",
                0.85,
                10,
                12,
                8192,
                "truncate_dim_256",
                256,
                None,
            ),
            (
                "model/a",
                "BenchB",
                "bench/b",
                "BenchB",
                "b1",
                "b1",
                "b1",
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
    (config_dir / "benchmarks.yaml").write_text("benchmarks:\n  - name: BenchA\n  - name: BenchB\n", encoding="utf-8")
    (config_dir / "overall.yaml").write_text(
        "name: Overall\nlabel: Overall\nbenchmarks:\n  - BenchA\n  - BenchB\n",
        encoding="utf-8",
    )

    service = LeaderboardService(duckdb_path=db_path, config=load_viewer_config(config_dir))
    result = service.get_leaderboard(
        "Overall",
        score_aggregation="micro",
        include_truncate_variants=True,
        show_task_z_scores=True,
    )
    rows_by_name = {row.model_name: row for row in result.rows}

    assert rows_by_name["model/a"].macro_mean == pytest.approx(70.0)
    assert rows_by_name["model/a"].micro_mean == pytest.approx(76.6666666667)
    assert rows_by_name["model/a"].macro_mean_z == pytest.approx(1.0)
    assert rows_by_name["model/a"].micro_mean_z == pytest.approx(1.0)
    assert rows_by_name["model/b"].macro_mean_z == pytest.approx(-1.0)
    assert rows_by_name["model/b"].micro_mean_z == pytest.approx(-1.0)
    variant_row = next(row for row in result.rows if row.embedding_variant_name == "truncate_dim_256")
    assert variant_row.macro_mean == pytest.approx(67.5)
    assert variant_row.micro_mean == pytest.approx(73.3333333333)
    assert variant_row.macro_mean_z == pytest.approx(0.5)
    assert variant_row.micro_mean_z == pytest.approx(0.5)

    app = create_app(store=LocalDuckDbStore(DuckDbLocation(local_path=db_path)), config_dir=config_dir)
    response = TestClient(app).get("/leaderboard?view=Overall&score=micro&truncate=1&task_z_scores=1")

    assert response.status_code == 200
    assert "Macro Mean" in response.text
    assert "Micro Mean" in response.text
    assert '<span class="task-z-score-value">70.00</span>' in response.text
    assert '<span class="task-z-score-value">76.67</span>' in response.text
    assert '<span class="task-z-score-value">67.50</span>' in response.text
    assert '<span class="task-z-score-value">73.33</span>' in response.text
    assert '<span class="task-z-score-delta">+1.00σ</span>' in response.text
    assert '<span class="task-z-score-delta">+0.50σ</span>' in response.text


def test_std_display_is_default_off_and_can_be_enabled_without_task_columns(tmp_path: Path) -> None:
    from fastapi.testclient import TestClient

    db_path = tmp_path / "results.duckdb"
    _write_task_results(
        db_path,
        [
            ("model/a", "BenchA", "bench/a", "BenchA", "a1", "a1", "a1", 0.90, 10, 12, 8192),
            ("model/a", "BenchA", "bench/a", "BenchA", "a2", "a2", "a2", 0.50, 10, 12, 8192),
            ("model/b", "BenchA", "bench/a", "BenchA", "a1", "a1", "a1", 0.70, 20, 24, 4096),
            ("model/b", "BenchA", "bench/a", "BenchA", "a2", "a2", "a2", 0.50, 20, 24, 4096),
        ],
    )
    config_dir = tmp_path / "config"
    config_dir.mkdir()
    (config_dir / "benchmarks.yaml").write_text("benchmarks:\n  - name: BenchA\n", encoding="utf-8")
    (config_dir / "overall.yaml").write_text("name: Overall\nlabel: Overall\nbenchmarks:\n  - BenchA\n", encoding="utf-8")
    app = create_app(store=LocalDuckDbStore(DuckDbLocation(local_path=db_path)), config_dir=config_dir)
    client = TestClient(app)

    default_response = client.get("/leaderboard?view=BenchA")

    assert default_response.status_code == 200
    assert 'name="task_scores" value="1" class="h-4 w-4 accent-cyan-700">' in default_response.text
    assert 'name="task_z_scores" value="1" class="h-4 w-4 accent-cyan-700" checked' not in default_response.text
    assert '<input type="hidden" name="task_z_scores" value="0">' in default_response.text
    assert "task-z-score" not in default_response.text
    assert "metric%3Aa1" not in default_response.text

    enabled_response = client.get("/leaderboard?view=BenchA&task_z_scores=1")

    assert enabled_response.status_code == 200
    assert 'name="task_z_scores" value="1" class="h-4 w-4 accent-cyan-700" checked' in enabled_response.text
    assert '<span class="task-z-score-delta">+1.00σ</span>' in enabled_response.text
    assert "task_z_scores=1" in enabled_response.text


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
            assert css_source.count(selector) == 3


def test_task_z_score_heatmap_css_uses_intuitive_positive_negative_colors() -> None:
    css_source = Path("hakari_bench/viewer/assets/app.tailwind.css").read_text(encoding="utf-8")

    assert re.search(r"\.task-z-score\s*{[^}]*border: 1px solid rgb\(29 27 24 / 0\.14\);", css_source, flags=re.DOTALL)
    assert re.search(r"\.task-z-score\s*{[^}]*border-radius: var\(--hakari-radius-sm\);", css_source, flags=re.DOTALL)
    assert re.search(r"\.task-z-score-value\s*{[^}]*font-size: 0\.8125rem;", css_source, flags=re.DOTALL)
    assert re.search(r"\.task-z-score-delta\s*{[^}]*font-size: 0\.5625rem;", css_source, flags=re.DOTALL)
    assert re.search(r"\.task-z-score-value\s*{[^}]*font-weight: 400;", css_source, flags=re.DOTALL)
    assert re.search(r"\.task-z-score-delta\s*{[^}]*font-weight: 400;", css_source, flags=re.DOTALL)
    assert re.search(r"\.task-z-score\s*{[^}]*border-color: rgb\(241 251 255 / 0\.22\);", css_source, flags=re.DOTALL)
    assert re.search(r"\.task-z-pos-025\s*{\s*background-color: #eaf6ef;", css_source)
    assert re.search(r"\.task-z-pos-200\s*{\s*background-color: #2f704d;", css_source)
    assert re.search(r"\.task-z-neg-025\s*{\s*background-color: #f7ebe4;", css_source)
    assert re.search(r"\.task-z-neg-200\s*{\s*background-color: #733126;", css_source)
    assert re.search(r'\.task-z-pos-025\s*{\s*background-color: theme\("colors\.emerald\.950"\);', css_source)
    assert re.search(r'\.task-z-pos-200\s*{\s*background-color: theme\("colors\.emerald\.300"\);', css_source)
    assert re.search(r'\.task-z-neg-150\s*{\s*background-color: theme\("colors\.rose\.500"\);', css_source)
    assert re.search(r'\.task-z-neg-175\s*{\s*background-color: theme\("colors\.rose\.600"\);', css_source)
    assert re.search(r'\.task-z-neg-200\s*{\s*background-color: theme\("colors\.rose\.700"\);', css_source)


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


def test_leaderboard_service_can_rank_by_non_default_metric(tmp_path: Path) -> None:
    db_path = tmp_path / "results.duckdb"
    rows = [
        ("model/a", "BenchA", "bench/a", "BenchA", "t1", "t1", "BenchA::t1", 0.90, 10, 12, 8192),
        ("model/b", "BenchA", "bench/a", "BenchA", "t1", "t1", "BenchA::t1", 0.80, 20, 24, 8192),
    ]
    _write_task_results(db_path, rows)
    _write_metric_tables(
        db_path,
        [
            ("model/a", "BenchA", "bench/a", "BenchA", "t1", "BenchA::t1", "BenchA_t1_cosine_acc@1", 0.10, "a.json"),
            ("model/b", "BenchA", "bench/a", "BenchA", "t1", "BenchA::t1", "BenchA_t1_cosine_acc@1", 0.95, "b.json"),
            ("model/a", "BenchA", "bench/a", "BenchA", "t1", "BenchA::t1", "BenchA_t1_cosine_acc@3", 0.20, "a.json"),
            ("model/a", "BenchA", "bench/a", "BenchA", "t1", "BenchA::t1", "BenchA_t1_cosine_acc@5", 0.30, "a.json"),
            ("model/a", "BenchA", "bench/a", "BenchA", "t1", "BenchA::t1", "BenchA_t1_cosine_acc@10", 0.40, "a.json"),
            ("model/a", "BenchA", "bench/a", "BenchA", "t1", "BenchA::t1", "BenchA_t1_cosine_acc@100", 0.90, "a.json"),
            ("model/a", "BenchA", "bench/a", "BenchA", "t1", "BenchA::t1", "BenchA_t1_cosine_ndcg@100", 0.70, "a.json"),
            ("model/a", "BenchA", "bench/a", "BenchA", "t1", "BenchA::t1", "BenchA_t1_cosine_precision@1", 0.20, "a.json"),
            ("model/a", "BenchA", "bench/a", "BenchA", "t1", "BenchA::t1", "BenchA_t1_cosine_precision@10", 0.40, "a.json"),
            ("model/a", "BenchA", "bench/a", "BenchA", "t1", "BenchA::t1", "BenchA_t1_cosine_recall@1", 0.20, "a.json"),
            ("model/a", "BenchA", "bench/a", "BenchA", "t1", "BenchA::t1", "BenchA_t1_cosine_recall@10", 0.40, "a.json"),
            ("model/a", "BenchA", "bench/a", "BenchA", "t1", "BenchA::t1", "BenchA_t1_cosine_recall@100", 0.95, "a.json"),
            ("model/a", "BenchA", "bench/a", "BenchA", "t1", "BenchA::t1", "BenchA_t1_cosine_mrr@10", 0.50, "a.json"),
            ("model/a", "BenchA", "bench/a", "BenchA", "t1", "BenchA::t1", "BenchA_t1_cosine_map@100", 0.60, "a.json"),
        ],
    )
    config_dir = tmp_path / "config"
    config_dir.mkdir()
    (config_dir / "benchmarks.yaml").write_text("benchmarks:\n  - name: BenchA\n", encoding="utf-8")
    (config_dir / "overall.yaml").write_text("name: Overall\nlabel: Overall\nbenchmarks:\n  - BenchA\n", encoding="utf-8")

    result = LeaderboardService(duckdb_path=db_path, config=load_viewer_config(config_dir)).get_leaderboard(
        "BenchA",
        score_metric="acc@1",
    )

    assert result.selected_score_metric == "acc@1"
    assert result.available_score_metrics == [
        "ndcg@10",
        "ndcg@100",
        "recall@10",
        "recall@100",
        "acc@1",
        "acc@10",
        "acc@100",
        "mrr@10",
        "map@100",
    ]
    assert [row.model_name for row in result.rows] == ["model/b", "model/a"]
    assert result.rows[0].mean_score == pytest.approx(95.0)

    app = create_app(store=LocalDuckDbStore(DuckDbLocation(local_path=db_path)), config_dir=config_dir)
    response = TestClient(app).get("/leaderboard?view=BenchA&metric=acc@1")

    assert response.status_code == 200
    assert "Score metric" in response.text
    assert "Acc@1" in response.text
    assert response.text.index("nDCG@10") < response.text.index("nDCG@100")
    assert response.text.index("nDCG@100") < response.text.index("Recall@10") < response.text.index("Recall@100")
    assert response.text.index("Recall@100") < response.text.index("Acc@1") < response.text.index("Acc@10")
    assert response.text.index("Acc@10") < response.text.index("Acc@100") < response.text.index("MRR@10")
    assert response.text.index("MRR@10") < response.text.index("MAP@100")
    assert "nDCG@10" in response.text
    assert "Acc@3" not in response.text
    assert "Acc@5" not in response.text
    assert "Precision@10" not in response.text
    assert "Precision@1\n" not in response.text
    assert "Recall@1\n" not in response.text


def test_leaderboard_service_excludes_bm25_only_for_cutoff_100_metrics(tmp_path: Path) -> None:
    db_path = tmp_path / "results.duckdb"
    rows = [
        ("bm25", "BenchA", "bench/a", "BenchA", "t1", "t1", "BenchA::t1", 0.50, 0, 0, 0),
        ("model/a", "BenchA", "bench/a", "BenchA", "t1", "t1", "BenchA::t1", 0.60, 10, 12, 8192),
    ]
    _write_task_results(db_path, rows)
    _write_metric_tables(
        db_path,
        [
            ("bm25", "BenchA", "bench/a", "BenchA", "t1", "BenchA::t1", "BenchA_t1_bm25_dataset_subset_map@100", 0.99, "bm25.json"),
            ("model/a", "BenchA", "bench/a", "BenchA", "t1", "BenchA::t1", "BenchA_t1_cosine_map@100", 0.10, "a.json"),
            ("bm25", "BenchA", "bench/a", "BenchA", "t1", "BenchA::t1", "BenchA_t1_bm25_dataset_subset_acc@1", 0.20, "bm25.json"),
            ("model/a", "BenchA", "bench/a", "BenchA", "t1", "BenchA::t1", "BenchA_t1_cosine_acc@1", 0.90, "a.json"),
        ],
    )
    config_dir = tmp_path / "config"
    config_dir.mkdir()
    (config_dir / "benchmarks.yaml").write_text("benchmarks:\n  - name: BenchA\n", encoding="utf-8")
    (config_dir / "overall.yaml").write_text("name: Overall\nlabel: Overall\nbenchmarks:\n  - BenchA\n", encoding="utf-8")
    service = LeaderboardService(duckdb_path=db_path, config=load_viewer_config(config_dir))

    cutoff_100 = service.get_leaderboard("BenchA", score_metric="map@100")
    cutoff_1 = service.get_leaderboard("BenchA", score_metric="acc@1")

    assert [row.model_name for row in cutoff_100.rows] == ["model/a"]
    assert [row.model_name for row in cutoff_1.rows] == ["model/a", "bm25"]


def test_leaderboard_service_recalculates_ranking_with_model_type_filter(tmp_path: Path) -> None:
    db_path = tmp_path / "results.duckdb"
    _write_task_results(
        db_path,
        [
            ("model/dense", "BenchA", "bench/a", "BenchA", "t1", "t1", "BenchA::t1", 0.95, 10, 12, 8192),
            ("bm25", "BenchA", "bench/a", "BenchA", "t1", "t1", "BenchA::t1", 0.80, 0, 0, 0),
            ("org/sparse-encoder", "BenchA", "bench/a", "BenchA", "t1", "t1", "BenchA::t1", 0.70, 20, 24, 8192),
        ],
    )
    config_dir = tmp_path / "config"
    config_dir.mkdir()
    (config_dir / "benchmarks.yaml").write_text("benchmarks:\n  - name: BenchA\n", encoding="utf-8")
    (config_dir / "overall.yaml").write_text("name: Overall\nlabel: Overall\nbenchmarks:\n  - BenchA\n", encoding="utf-8")

    result = LeaderboardService(duckdb_path=db_path, config=load_viewer_config(config_dir)).get_leaderboard(
        "BenchA",
        rank_filtered=True,
        model_type_filters=("sparse",),
    )

    assert [row.model_name for row in result.rows] == ["bm25", "org/sparse-encoder"]


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
    assert "Task string length" not in response.text
    assert ">Length</span>" in response.text
    assert "Query length ≤" in response.text
    assert "Document length ≤" in response.text
    assert 'data-help-title="Length filters"' in response.text
    assert "Length filters operate at the task level using average text length metadata" in response.text
    assert "Tasks without length metadata are excluded when any bound is set." in response.text
    assert "Query string <=" not in response.text
    assert "Doc string <=" not in response.text
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
    assert _metric_column_label("NanoBIRCO::NanoBIRCO") == "NanoBIRCO"
    assert _metric_column_label("NanoMMTEB::NanoArguAna") == "NanoMMTEB::NanoArguAna"
    assert _metric_column_label("NanoBRIGHT::NanoBRIGHTFooBar") == "NanoBRIGHT::FooBar"
    assert _metric_column_label("NanoBRIGHT::NanoBRIGHT") == "NanoBRIGHT"
    assert _metric_column_label("NanoBrightAops", parent_label="NanoBRIGHT") == "Aops"
    assert _metric_column_label("NanoBRIGHT", parent_label="NanoBRIGHT") == "NanoBRIGHT"
    assert _metric_column_label("MNanoBEIR::hakari-bench/NanoBEIR-ar::arguana") == "NanoBEIR-ar::arguana"


def test_task_score_column_headers_strip_repeated_suite_prefix_from_subtask() -> None:
    result = LeaderboardResult(
        view_name="NanoBRIGHT",
        view_label="NanoBRIGHT",
        is_overall=False,
        expected_tasks=1,
        rows=[],
        available_views=["NanoBRIGHT"],
        available_view_labels={"NanoBRIGHT": "NanoBRIGHT"},
        score_groups=[],
        metric_columns=["NanoBRIGHT::NanoBRIGHTFooBar", "NanoBRIGHT::NanoBRIGHT"],
    )

    head = render_table_head(result=result, sort="borda_rank", direction="asc")

    assert '<span class="block w-full truncate">NanoBRIGHT</span>' in head
    assert '<span class="block max-w-full truncate font-normal">FooBar</span>' in head
    assert '<span class="block max-w-full truncate font-normal">NanoBRIGHTFooBar</span>' not in head


def test_task_score_column_headers_strip_view_prefix_from_single_task_name() -> None:
    result = LeaderboardResult(
        view_name="NanoBRIGHT",
        view_label="NanoBRIGHT",
        is_overall=False,
        expected_tasks=1,
        rows=[],
        available_views=["NanoBRIGHT"],
        available_view_labels={"NanoBRIGHT": "NanoBRIGHT"},
        score_groups=[],
        metric_columns=["NanoBrightAops"],
    )

    head = render_table_head(result=result, sort="borda_rank", direction="asc")

    assert 'data-tooltip="Task score column for this benchmark task. Display: Aops.' in head
    assert '>Aops</span>' in head
    assert '>BrightAops</span>' not in head


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


def test_task_score_column_headers_use_viewer_task_label_overrides(tmp_path: Path) -> None:
    db_path = tmp_path / "results.duckdb"
    _write_task_results(
        db_path,
        [
            ("model/a", "NanoMTEB-Misc", "hakari-bench/NanoMTEB-Misc", "NanoMTEB-Misc", "en", "en", "misc-en", 0.80, 10, 12, 8192),
            ("model/a", "NanoMTEB-Misc", "hakari-bench/NanoMTEB-Misc", "NanoMTEB-Misc", "fi", "fi", "misc-fi", 0.70, 10, 12, 8192),
            ("model/b", "NanoMTEB-Misc", "hakari-bench/NanoMTEB-Misc", "NanoMTEB-Misc", "en", "en", "misc-en", 0.60, 20, 24, 4096),
            ("model/b", "NanoMTEB-Misc", "hakari-bench/NanoMTEB-Misc", "NanoMTEB-Misc", "fi", "fi", "misc-fi", 0.50, 20, 24, 4096),
        ],
    )
    config_dir = tmp_path / "config"
    config_dir.mkdir()
    (config_dir / "benchmarks.yaml").write_text(
        """
benchmarks:
  - name: NanoMTEB-Misc
    task_labels:
      en: EuroPIRQ-en
      fi: EuroPIRQ-fi
""".strip(),
        encoding="utf-8",
    )
    (config_dir / "overall.yaml").write_text(
        "name: Overall\nlabel: Overall\nbenchmarks:\n  - NanoMTEB-Misc\n",
        encoding="utf-8",
    )

    service = LeaderboardService(duckdb_path=db_path, config=load_viewer_config(config_dir))
    result = service.get_leaderboard("NanoMTEB-Misc", show_task_scores=True)

    assert result.metric_columns == ["en", "fi"]
    assert result.metric_column_labels == {"en": "EuroPIRQ-en", "fi": "EuroPIRQ-fi"}

    from fastapi.testclient import TestClient

    app = create_app(store=LocalDuckDbStore(DuckDbLocation(local_path=db_path)), config_dir=config_dir)
    response = TestClient(app).get("/leaderboard?view=NanoMTEB-Misc&task_scores=1")

    assert response.status_code == 200
    assert ">EuroPIRQ-en</span>" in response.text
    assert ">EuroPIRQ-fi</span>" in response.text
    assert 'data-metric-column-full-name="en"' in response.text


def test_task_score_column_headers_shorten_dataset_task_keys_and_keep_full_name(tmp_path: Path) -> None:
    db_path = tmp_path / "results.duckdb"
    task_rows = [
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
            "hakari-bench/NanoBEIR-ar",
            "NanoBEIR-ar",
            "ar",
            "climatefever",
            "MNanoBEIR::hakari-bench/NanoBEIR-ar::climatefever",
            0.82,
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
            "hakari-bench/NanoBEIR-ar",
            "NanoBEIR-ar",
            "ar",
            "climatefever",
            "MNanoBEIR::hakari-bench/NanoBEIR-ar::climatefever",
            0.62,
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
    ]
    _write_task_results(
        db_path,
        task_rows,
        dataset_metadata_rows=[
            (benchmark, dataset_id, dataset_name, split_name, task_name, task_key, split_name, [split_name], [split_name])
            for (
                _model_name,
                benchmark,
                dataset_id,
                dataset_name,
                split_name,
                task_name,
                task_key,
                _score,
                _active_parameters,
                _total_parameters,
                _max_seq_length,
            ) in task_rows
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
      - name: task_mean
        label: Task Mean
        group_by: task_name
""".strip(),
        encoding="utf-8",
    )
    (config_dir / "overall.yaml").write_text("name: Overall\nlabel: Overall\nbenchmarks:\n  - MNanoBEIR\n", encoding="utf-8")

    from fastapi.testclient import TestClient

    app = create_app(store=LocalDuckDbStore(DuckDbLocation(local_path=db_path)), config_dir=config_dir)
    response = TestClient(app).get("/leaderboard?view=MNanoBEIR&group=task_key&task_scores=1")

    assert response.status_code == 200
    assert 'scope="colgroup"' not in response.text
    assert '<span class="block w-full truncate">NanoBEIR-ar</span>' in response.text
    assert '<span class="block w-full truncate">NanoBEIR-ja</span>' in response.text
    assert '<span class="block max-w-full truncate font-normal">arguana</span>' in response.text
    assert (
        '<span class="block max-w-full truncate font-normal">climatefever</span>'
        in response.text
    )
    assert "Task Key column. Scores are averaged per model over the raw benchmark rows" in response.text
    assert (
        'data-metric-column-full-name="MNanoBEIR::hakari-bench/NanoBEIR-ar::arguana"'
        in response.text
    )
    assert 'class="doc-summary-trigger' in response.text

    filtered_result = LeaderboardService(duckdb_path=db_path, config=load_viewer_config(config_dir)).get_leaderboard(
        "MNanoBEIR",
        score_group_name="task_mean",
        show_task_scores=True,
        language_filters=("ja",),
    )
    assert filtered_result.metric_columns == ["arguana"]
    assert filtered_result.metric_column_doc_keys == {"arguana": "MNanoBEIR::NanoBEIR-ja::arguana"}

    filtered_response = TestClient(app).get(
        "/leaderboard?view=MNanoBEIR&group=task_mean&task_scores=1&lang_filter=ja"
    )
    assert filtered_response.status_code == 200
    assert 'data-doc-title="MNanoBEIR / NanoBEIR-ja / NanoArguAna"' in filtered_response.text
    assert 'data-doc-title="MNanoBEIR / NanoBEIR-ar / NanoArguAna"' not in filtered_response.text


def test_max_len_uses_compact_k_display_for_1k_and_above() -> None:
    assert _fmt_max_len(512) == "512"
    assert _fmt_max_len(1_023) == "1,023"
    assert _fmt_max_len(1_024) == "1K"
    assert _fmt_max_len(1_535) == "1K"
    assert _fmt_max_len(1_536) == "2K"
    assert _fmt_max_len(4_096) == "4K"
    assert _fmt_max_len(8_192) == "8K"
    assert _fmt_max_len(None) == ""


def test_parameter_counts_use_compact_rounded_display() -> None:
    assert _fmt_params(None) == ""
    assert _fmt_params(310_300_000) == "310M"
    assert _fmt_params(310_500_000) == "311M"
    assert _fmt_params(999_499_999) == "999M"
    assert _fmt_params(1_320_000_000) == "1.32B"
    assert _fmt_params(1_325_000_000) == "1.33B"
    assert _fmt_params(27_330_000_000) == "27.3B"
    assert _fmt_params(27_350_000_000) == "27.4B"
    assert _fmt_params(101_300_000_000) == "101B"


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


def test_local_duckdb_store_skips_hf_source_check_within_ttl(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    downloaded = tmp_path / "hf-cache.duckdb"
    downloaded.write_bytes(b"hf")
    local = tmp_path / "viewer" / "hakari_bench.duckdb"
    calls: list[HuggingFaceDuckDbSource] = []
    now = 1000.0

    def fake_download(source: HuggingFaceDuckDbSource) -> Path:
        calls.append(source)
        return downloaded

    def fake_monotonic() -> float:
        return now

    monkeypatch.setattr("hakari_bench.viewer.store._download_hf_duckdb", fake_download)
    monkeypatch.setattr("hakari_bench.viewer.store.monotonic", fake_monotonic)
    source = HuggingFaceDuckDbSource(repo_id="hakari-bench/leaderboard_database")
    store = LocalDuckDbStore(DuckDbLocation(local_path=local, hf_source=source))

    assert store.ensure_current() is True
    assert store.ensure_current() is False
    assert calls == [source]
    assert local.read_bytes() == b"hf"


def test_local_duckdb_store_refreshes_hf_source_after_ttl(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    downloaded = tmp_path / "hf-cache.duckdb"
    downloaded.write_bytes(b"hf-old")
    local = tmp_path / "viewer" / "hakari_bench.duckdb"
    calls: list[HuggingFaceDuckDbSource] = []
    now = 1000.0

    def fake_download(source: HuggingFaceDuckDbSource) -> Path:
        calls.append(source)
        return downloaded

    def fake_monotonic() -> float:
        return now

    monkeypatch.setattr("hakari_bench.viewer.store._download_hf_duckdb", fake_download)
    monkeypatch.setattr("hakari_bench.viewer.store.monotonic", fake_monotonic)
    source = HuggingFaceDuckDbSource(repo_id="hakari-bench/leaderboard_database")
    store = LocalDuckDbStore(DuckDbLocation(local_path=local, hf_source=source))

    assert store.ensure_current() is True

    now += 601.0
    time.sleep(0.01)
    downloaded.write_bytes(b"hf-new")
    os.utime(downloaded, None)

    assert store.ensure_current() is True
    assert calls == [source, source]
    assert local.read_bytes() == b"hf-new"


def test_download_hf_duckdb_uses_remote_latest_cache_metadata(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    cache_path = tmp_path / "remote_latest_hakari_bench.duckdb"
    metadata_path = tmp_path / "remote_latest_hakari_bench.duckdb.metadata.json"
    downloaded = tmp_path / "hf-cache.duckdb"
    downloaded.write_bytes(b"remote-db")
    source = HuggingFaceDuckDbSource(repo_id="hakari-bench/leaderboard_database")
    calls: list[HuggingFaceDuckDbSource] = []

    def fake_download(download_source: HuggingFaceDuckDbSource) -> Path:
        calls.append(download_source)
        return downloaded

    monkeypatch.setenv(viewer_store.REMOTE_LATEST_DUCKDB_PATH_ENV, str(cache_path))
    monkeypatch.setenv(viewer_store.REMOTE_LATEST_DUCKDB_METADATA_PATH_ENV, str(metadata_path))
    monkeypatch.setattr(
        viewer_store,
        "_fetch_hf_duckdb_metadata",
        lambda _source: {"etag": "etag-1", "commit_hash": "commit-1", "size": len(b"remote-db")},
    )
    monkeypatch.setattr(viewer_store, "_download_hf_duckdb_to_hub_cache", fake_download)

    assert viewer_store._download_hf_duckdb(source) == cache_path
    assert cache_path.read_bytes() == b"remote-db"
    assert viewer_store._download_hf_duckdb(source) == cache_path
    assert calls == [source]


def test_download_hf_duckdb_falls_back_to_existing_remote_latest_cache(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    cache_path = tmp_path / "remote_latest_hakari_bench.duckdb"
    cache_path.write_bytes(b"cached-db")
    source = HuggingFaceDuckDbSource(repo_id="hakari-bench/leaderboard_database")

    def fake_download(_source: HuggingFaceDuckDbSource) -> Path:
        raise RuntimeError("network unavailable")

    monkeypatch.setenv(viewer_store.REMOTE_LATEST_DUCKDB_PATH_ENV, str(cache_path))
    monkeypatch.setattr(viewer_store, "_fetch_hf_duckdb_metadata", lambda _source: {})
    monkeypatch.setattr(viewer_store, "_download_hf_duckdb_to_hub_cache", fake_download)

    assert viewer_store._download_hf_duckdb(source) == cache_path
    assert cache_path.read_bytes() == b"cached-db"


def test_local_duckdb_store_skips_copy_when_source_content_matches(tmp_path: Path) -> None:
    source = tmp_path / "source.duckdb"
    local = tmp_path / "viewer" / "hakari_bench.duckdb"
    source.write_bytes(b"same")
    local.parent.mkdir()
    local.write_bytes(b"same")
    os.utime(local, (1, 1))
    os.utime(source, (2, 2))
    store = LocalDuckDbStore(DuckDbLocation(local_path=local, source_path=source))

    assert store.ensure_current() is False
    assert local.stat().st_mtime == 1


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
    assert 'href="/leaderboard.csv?view=Overall' in response.text
    assert "Download CSV" in response.text
    assert 'data-icon="file-spreadsheet"' in response.text
    assert 'aria-label="Download visible leaderboard as CSV"' in response.text


def test_leaderboard_csv_exports_visible_scores_and_model_metadata(tmp_path: Path) -> None:
    from fastapi.testclient import TestClient

    db_path = tmp_path / "results.duckdb"
    _write_task_results(
        db_path,
        [
            (
                "org/model-a",
                "BenchA",
                "bench/a",
                "BenchA",
                "split",
                "arguana",
                "arguana",
                0.90,
                10,
                12,
                1024,
                "bf16",
                "flash_attention_2",
                None,
                None,
                "query",
                None,
                None,
                None,
                True,
                None,
                1024,
                None,
            ),
            (
                "org/model-a",
                "BenchA",
                "bench/a",
                "BenchA",
                "split",
                "arguana",
                "arguana",
                0.82,
                10,
                12,
                1024,
                "bf16",
                "flash_attention_2",
                None,
                None,
                "query",
                None,
                None,
                None,
                True,
                "truncate_dim_512",
                512,
                None,
            ),
            (
                "org/hidden-model",
                "BenchA",
                "bench/a",
                "BenchA",
                "split",
                "arguana",
                "arguana",
                0.70,
                20,
                24,
                2048,
                "fp32",
                None,
                None,
                None,
                None,
                None,
                None,
                None,
                False,
                None,
                768,
                "int8",
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
    response = TestClient(app).get(
        "/leaderboard.csv?view=BenchA&truncate=1&task_scores=1&task_z_scores=1&model_filter=model-a"
    )

    assert response.status_code == 200
    assert response.headers["content-type"].startswith("text/csv")
    assert 'filename="hakari_bench_BenchA_all.csv"' in response.headers["content-disposition"]
    rows = list(csv.DictReader(response.text.splitlines()))

    assert len(rows) == 2
    assert "arguana" in rows[0]
    assert "arguana σ" not in rows[0]
    assert "hidden-model" not in response.text
    assert rows[0]["Model Name"] == "model-a"
    assert rows[0]["Full Model Name"] == "org/model-a"
    assert rows[0]["Ranking Model Name"] == "org/model-a (1024 dims)"
    assert rows[0]["Embedding Dims"] == "1024"
    assert rows[0]["Original Embedding Dims"] == "1024"
    assert rows[0]["Truncated Embedding Dims"] == ""
    assert rows[0]["Variant Label"] == ""
    assert rows[0]["Variant Category"] == ""
    assert rows[0]["DType"] == "bf16"
    assert rows[0]["Attention Implementation"] == "flash_attention_2"
    assert rows[0]["Prompt"] == "prompt names"
    assert rows[0]["Trust Remote Code"] == "true"

    truncated = next(row for row in rows if row["Truncated Embedding Dims"] == "512")
    assert truncated["Model Name"] == "model-a"
    assert truncated["Ranking Model Name"] == "org/model-a (512 dims)"
    assert truncated["Embedding Dims"] == "512"
    assert truncated["Original Embedding Dims"] == "1024"
    assert truncated["Embedding Variant"] == "truncate_dim_512"
    assert truncated["Variant Label"] == "512d <- 1024"
    assert truncated["Variant Category"] == "truncate"


def test_leaderboard_csv_exports_short_variant_labels_and_categories() -> None:
    result = LeaderboardResult(
        view_name="BenchA",
        view_label="Bench A",
        is_overall=False,
        expected_tasks=1,
        rows=[
            LeaderboardRow(
                borda_rank=1,
                mean_rank=1,
                model_name="org/sparse-model",
                source_model_name="org/sparse-model",
                model_type="sparse",
                borda_score=100,
                mean_score=100,
                task_count=1,
                embedding_dim=105879,
            ),
            LeaderboardRow(
                borda_rank=2,
                mean_rank=2,
                model_name=(
                    "org/sparse-model "
                    "(sparse_query_max_active_dims_32_sparse_document_max_active_dims_256)"
                ),
                source_model_name="org/sparse-model",
                model_type="sparse",
                borda_score=95,
                mean_score=95,
                task_count=1,
                embedding_dim=105879,
                embedding_variant_name="sparse_query_max_active_dims_32_sparse_document_max_active_dims_256",
                base_score_delta_percent=-5.0,
            ),
            LeaderboardRow(
                borda_rank=3,
                mean_rank=3,
                model_name="org/dense-model (512 dims, int8)",
                source_model_name="org/dense-model",
                borda_score=90,
                mean_score=90,
                task_count=1,
                embedding_dim=512,
                quantization="int8",
                embedding_variant_name="truncate_dim_512_int8_rescore",
                base_score_delta_percent=-10.0,
            ),
        ],
        available_views=["BenchA"],
        available_view_labels={"BenchA": "Bench A"},
        include_rescore_variants=True,
        include_other_variants=True,
        score_groups=[],
        metric_columns=[],
    )

    rows = list(csv.DictReader(render_leaderboard_csv(result=result).splitlines()))

    assert rows[0]["Variant Label"] == ""
    assert rows[0]["Variant Category"] == ""
    assert rows[1]["Variant Label"] == "q32d d256d"
    assert rows[1]["Variant Category"] == "sparse active dims"
    assert rows[1]["Embedding Variant"] == "sparse_query_max_active_dims_32_sparse_document_max_active_dims_256"
    assert rows[1]["Base Score Delta Percent"] == "-5"
    assert rows[2]["Variant Label"] == "512d"
    assert rows[2]["Variant Category"] == "truncate + quantization + rescore"
    assert rows[2]["Quantization"] == "int8"


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
    response = TestClient(app).get("/?view=MNanoBEIR&group=lang_mean&sort=metric:NanoBEIR-ja&direction=desc&task_z_scores=0")

    assert response.status_code == 200
    assert '<link rel="canonical" href="/">' in response.text
    assert (
        'hx-get="/leaderboard?view=MNanoBEIR&amp;sort=metric%3ANanoBEIR-ja&amp;direction=desc'
        '&amp;group=lang_mean&amp;task_z_scores=0"'
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
            "primary_languages VARCHAR[]",
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
                language=metadata_by_task.get((row[1], row[2], row[4], row[5], row[6]), (None, [], [], None, None))[0],
                languages=metadata_by_task.get((row[1], row[2], row[4], row[5], row[6]), (None, [], [], None, None))[1],
                primary_languages=metadata_by_task.get((row[1], row[2], row[4], row[5], row[6]), (None, [], [], None, None))[2],
                query_mean_chars=metadata_by_task.get((row[1], row[2], row[4], row[5], row[6]), (None, [], [], None, None))[3],
                document_mean_chars=metadata_by_task.get((row[1], row[2], row[4], row[5], row[6]), (None, [], [], None, None))[4],
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


def _metadata_by_task(
    rows: list[tuple],
) -> dict[tuple[str, str, str, str, str], tuple[str | None, list[str], list[str], float | None, float | None]]:
    metadata = {}
    for row in rows:
        benchmark, dataset_id, _dataset_name, split_name, task_name, task_key, language, languages, *lengths = row
        primary_languages = lengths[0] if len(lengths) >= 1 and isinstance(lengths[0], list) else []
        length_offset = 1 if primary_languages else 0
        query_mean_chars = lengths[length_offset] if len(lengths) >= length_offset + 1 else None
        document_mean_chars = lengths[length_offset + 1] if len(lengths) >= length_offset + 2 else None
        metadata[(benchmark, dataset_id, split_name, task_name, task_key)] = (
            language,
            languages,
            primary_languages,
            query_mean_chars,
            document_mean_chars,
        )
    return metadata


def _write_metric_tables(db_path: Path, rows: list[tuple], *, score_target: str = "all") -> None:
    con = duckdb.connect(str(db_path))
    try:
        con.execute(
            """
            CREATE TABLE dim_metric (
                metric_id BIGINT,
                metric_name VARCHAR,
                metric_family VARCHAR,
                cutoff INTEGER
            )
            """
        )
        metric_names = sorted({row[6] for row in rows})
        for metric_id, metric_name in enumerate(metric_names, start=1):
            family, cutoff = metric_name.rsplit("@", 1)
            con.execute(
                "INSERT INTO dim_metric VALUES (?, ?, ?, ?)",
                [metric_id, metric_name, family.rsplit("_", 1)[-1], int(cutoff)],
            )
        con.execute(
            """
            CREATE TABLE fact_metric_score (
                metric_id BIGINT,
                model_dir VARCHAR,
                model_name VARCHAR,
                benchmark VARCHAR,
                dataset_id VARCHAR,
                task_name VARCHAR,
                metric_value DOUBLE,
                result_path VARCHAR,
                score_target VARCHAR,
                embedding_variant_name VARCHAR
            )
            """
        )
        con.execute(
            """
            CREATE TABLE fact_task_score (
                model_dir VARCHAR,
                model_name VARCHAR,
                benchmark VARCHAR,
                dataset_id VARCHAR,
                dataset_name VARCHAR,
                split_name VARCHAR,
                task_name VARCHAR,
                task_key VARCHAR,
                score_target VARCHAR,
                score DOUBLE,
                active_parameters BIGINT,
                total_parameters BIGINT,
                max_seq_length INTEGER,
                dtype VARCHAR,
                attn_implementation VARCHAR,
                query_prompt VARCHAR,
                document_prompt VARCHAR,
                query_prompt_name VARCHAR,
                document_prompt_name VARCHAR,
                query_encode_task VARCHAR,
                document_encode_task VARCHAR,
                trust_remote_code BOOLEAN,
                embedding_variant_name VARCHAR,
                embedding_dim INTEGER,
                quantization VARCHAR,
                result_path VARCHAR
            )
            """
        )
        metric_id_by_name = {name: index for index, name in enumerate(metric_names, start=1)}
        inserted_task_scores: set[tuple[str, str, str, str, str]] = set()
        for model_name, benchmark, dataset_id, dataset_name, task_name, task_key, metric_name, metric_value, result_path in rows:
            con.execute(
                "INSERT INTO fact_metric_score VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
                [
                    metric_id_by_name[metric_name],
                    model_name.replace("/", "__"),
                    model_name,
                    benchmark,
                    dataset_id,
                    task_name,
                    metric_value,
                    result_path,
                    score_target,
                    None,
                ],
            )
            task_key_tuple = (model_name, benchmark, dataset_id, task_name, result_path)
            if task_key_tuple in inserted_task_scores:
                continue
            inserted_task_scores.add(task_key_tuple)
            con.execute(
                "INSERT INTO fact_task_score VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
                [
                    model_name.replace("/", "__"),
                    model_name,
                    benchmark,
                    dataset_id,
                    dataset_name,
                    "",
                    task_name,
                    task_key,
                    score_target,
                    0.0,
                    10,
                    12,
                    8192,
                    None,
                    None,
                    None,
                    None,
                    None,
                    None,
                    None,
                    None,
                    None,
                    None,
                    None,
                    None,
                    result_path,
                ],
            )
    finally:
        con.close()


def _viewer_task_result_row(
    row: tuple,
    *,
    language: str | None,
    languages: list[str],
    primary_languages: list[str] | None = None,
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
        primary_languages or [],
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
        if row[7] == "all" and row[24] is None
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
            or candidate_ranking != "reranking_hybrid"
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


def test_frame_ancestors_keeps_valid_https_and_keyword_tokens(monkeypatch: pytest.MonkeyPatch) -> None:
    from hakari_bench.viewer import app as viewer_app

    monkeypatch.setenv(
        "HAKARI_BENCH_VIEWER_FRAME_ANCESTORS",
        "'self' https://huggingface.co https://*.huggingface.co",
    )
    assert (
        viewer_app._frame_ancestors()
        == "'self' https://huggingface.co https://*.huggingface.co"
    )


def test_frame_ancestors_rejects_unsafe_token(monkeypatch: pytest.MonkeyPatch) -> None:
    from hakari_bench.viewer import app as viewer_app

    monkeypatch.setenv(
        "HAKARI_BENCH_VIEWER_FRAME_ANCESTORS",
        "https://huggingface.co javascript:alert(1)",
    )
    assert viewer_app._frame_ancestors() == viewer_app.DEFAULT_FRAME_ANCESTORS


def test_frame_ancestors_rejects_crlf_token(monkeypatch: pytest.MonkeyPatch) -> None:
    from hakari_bench.viewer import app as viewer_app

    monkeypatch.setenv(
        "HAKARI_BENCH_VIEWER_FRAME_ANCESTORS",
        "https://huggingface.co\r\nContent-Type: text/html",
    )
    assert viewer_app._frame_ancestors() == viewer_app.DEFAULT_FRAME_ANCESTORS
