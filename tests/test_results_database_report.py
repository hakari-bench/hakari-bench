from __future__ import annotations

import asyncio
import gzip
import json
import lzma
import math
import hashlib
from pathlib import Path
import sys
from typing import Any, cast

import duckdb
import pytest
from pydantic import ValidationError

from hakari_bench.viewer.config import BenchmarkConfig, OverallConfig, ScoreGroupConfig, ViewerConfig
from hakari_bench.warehouse_schema import (
    DatasetMetadataRow,
    MetricLongRow,
    RetrievalRankingRow,
    TaskDiagnosticRow,
    TaskResultRow,
)
from scripts import build_results_database_and_report as report


def test_nanomteb_japanese_is_a_ranked_benchmark() -> None:
    assert "NanoJMTEB-v2" in report.TARGET_BENCHMARKS
    assert report.benchmark_name("hakari-bench/NanoJMTEB-v2", "NanoJMTEB-v2") == "NanoJMTEB-v2"


def test_nanorteb_is_a_ranked_benchmark() -> None:
    assert "NanoRTEB" in report.TARGET_BENCHMARKS
    assert report.benchmark_name("hakari-bench/NanoRTEB", "NanoRTEB") == "NanoRTEB"


def test_nanolongembed_is_a_ranked_benchmark() -> None:
    assert "NanoLongEmbed" in report.TARGET_BENCHMARKS
    assert report.benchmark_name("hakari-bench/NanoLongEmbed", "NanoLongEmbed") == "NanoLongEmbed"


def test_nanocoir_is_a_ranked_benchmark() -> None:
    assert "NanoCoIR" in report.TARGET_BENCHMARKS
    assert report.benchmark_name("hakari-bench/NanoCoIR", "NanoCoIR") == "NanoCoIR"


def test_linux_physical_cpu_count_from_cpuinfo_counts_hyperthreaded_cores() -> None:
    cpuinfo = "\n\n".join(
        "\n".join(
            [
                f"processor\t: {processor}",
                "physical id\t: 0",
                f"core id\t\t: {processor % 16}",
            ]
        )
        for processor in range(32)
    )

    assert report._physical_cpu_count_from_linux_cpuinfo(cpuinfo) == 16


def test_default_result_worker_count_uses_physical_cores_minus_one(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(report, "_linux_physical_cpu_count", lambda: 16)

    assert report.default_result_worker_count() == 15


def test_default_result_worker_count_falls_back_to_available_logical_cpus(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setattr(report, "_linux_physical_cpu_count", lambda: None)
    monkeypatch.setattr(report, "_available_cpu_count", lambda: 8)

    assert report.default_result_worker_count() == 7


def test_resolve_result_worker_counts_uses_auto_default_when_unspecified() -> None:
    assert report.resolve_result_worker_counts(
        result_selection_workers=None,
        result_json_workers=None,
        result_row_workers=None,
        default_workers=15,
    ) == report.ResultWorkerCounts(selection=15, json=15, row=15)


def test_resolve_result_worker_counts_preserves_explicit_json_workers() -> None:
    assert report.resolve_result_worker_counts(
        result_selection_workers=None,
        result_json_workers=8,
        result_row_workers=None,
        default_workers=15,
    ) == report.ResultWorkerCounts(selection=15, json=8, row=1)


def test_resolve_result_worker_counts_preserves_explicit_row_workers() -> None:
    assert report.resolve_result_worker_counts(
        result_selection_workers=None,
        result_json_workers=None,
        result_row_workers=1,
        default_workers=15,
    ) == report.ResultWorkerCounts(selection=15, json=1, row=1)


def test_resolve_warehouse_build_plan_defaults_to_streamed_hakari_results() -> None:
    args = report.build_arg_parser().parse_args([])

    plan = report.resolve_warehouse_build_plan(args)

    assert plan.mode == "stream"
    assert plan.results_dirs == [Path("output/hakari-results")]
    assert plan.append_results_dirs == []
    assert plan.duckdb_path == Path("output/hakari-results/hakari_bench.duckdb")
    assert plan.duplicate_result_policy == "first-wins"


def test_resolve_warehouse_build_plan_selects_materialized_mode_for_html_output() -> None:
    args = report.build_arg_parser().parse_args(["--html-output", "report.html"])

    plan = report.resolve_warehouse_build_plan(args)

    assert plan.mode == "materialized"
    assert plan.html_output == Path("report.html")


def test_resolve_warehouse_build_plan_selects_explicit_materialized_mode() -> None:
    args = report.build_arg_parser().parse_args(["--materialize-results-in-python"])

    plan = report.resolve_warehouse_build_plan(args)

    assert plan.mode == "materialized"


def test_resolve_warehouse_build_plan_selects_append_mode() -> None:
    args = report.build_arg_parser().parse_args(
        [
            "--append-results-dir",
            "new_results",
            "--append-base-duckdb",
            "base.duckdb",
            "--append-output-duckdb",
            "merged.duckdb",
            "--model-name-override",
            "local/model_exp_122",
        ]
    )

    plan = report.resolve_warehouse_build_plan(args)

    assert plan.mode == "append"
    assert plan.results_dirs == []
    assert plan.append_results_dirs == [Path("new_results")]
    assert plan.duckdb_path == Path("merged.duckdb")
    assert plan.append_base_duckdb == Path("base.duckdb")
    assert plan.model_name_override == "local/model_exp_122"


def test_resolve_warehouse_build_plan_rejects_append_with_results_dir() -> None:
    args = report.build_arg_parser().parse_args(
        ["--append-results-dir", "new_results", "--results-dir", "base_results"]
    )

    with pytest.raises(ValueError, match="--append-results-dir cannot be combined with --results-dir"):
        report.resolve_warehouse_build_plan(args)


def test_resolve_warehouse_build_plan_rejects_append_output_without_base() -> None:
    args = report.build_arg_parser().parse_args(
        ["--append-results-dir", "new_results", "--append-output-duckdb", "merged.duckdb"]
    )

    with pytest.raises(ValueError, match="--append-output-duckdb requires --append-base-duckdb"):
        report.resolve_warehouse_build_plan(args)


def test_run_warehouse_build_stream_plan_uses_streaming_writer(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    args = report.build_arg_parser().parse_args(
        ["--stream-results-to-duckdb", "--results-dir", "results", "--duckdb-path", str(tmp_path / "out.duckdb")]
    )
    plan = report.resolve_warehouse_build_plan(args)
    viewer_config = ViewerConfig(
        benchmarks=[],
        overalls=[OverallConfig(name="Overall", label="Overall", benchmarks=[])],
    )
    calls: list[tuple[str, object]] = []

    monkeypatch.setattr(report, "load_viewer_config", lambda _path: viewer_config)
    monkeypatch.setattr(
        report,
        "write_duckdb_streaming_results",
        lambda results_dirs, db_path, **_: calls.append(("stream", (results_dirs, db_path))),
    )
    monkeypatch.setattr(report, "build_viewer_leaderboard_mart", lambda duckdb_path, **_: calls.append(("mart", duckdb_path)))
    monkeypatch.setattr(report, "load_results", lambda *_, **__: pytest.fail("stream plan should not materialize rows"))

    report.run_warehouse_build(plan, memory_monitor=report.MemoryMonitor(log_path=None))

    assert calls == [
        ("stream", ([Path("results")], tmp_path / "out.duckdb")),
        ("mart", tmp_path / "out.duckdb"),
    ]


def test_run_warehouse_build_append_plan_uses_shared_loader(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    duckdb_path = tmp_path / "base.duckdb"
    duckdb_path.write_bytes(b"base-db")
    args = report.build_arg_parser().parse_args(
        ["--append-results-dir", "added_results", "--duckdb-path", str(duckdb_path)]
    )
    plan = report.resolve_warehouse_build_plan(args)
    viewer_config = ViewerConfig(
        benchmarks=[],
        overalls=[OverallConfig(name="Overall", label="Overall", benchmarks=[])],
    )
    calls: list[tuple[str, object]] = []

    def load_for_plan(
        plan_arg: report.WarehouseBuildPlan,
        results_dirs: list[Path],
        *,
        benchmark_configs: list[BenchmarkConfig],
        memory_monitor: report.MemoryMonitor,
        incremental_db_path: Path | None = None,
        include_source_hashes: bool = False,
    ) -> report.LoadResultsPayloadWithSourceHashes:
        calls.append(
            (
                "load",
                (
                    plan_arg.mode,
                    results_dirs,
                    benchmark_configs,
                    incremental_db_path,
                    include_source_hashes,
                    isinstance(memory_monitor, report.MemoryMonitor),
                ),
            )
        )
        return [], [], [], [], [], [], {}

    monkeypatch.setattr(report, "load_viewer_config", lambda _path: viewer_config)
    monkeypatch.setattr(report, "_load_results_for_plan", load_for_plan)
    monkeypatch.setattr(report, "append_duckdb_results", lambda duckdb_path, **_: calls.append(("append", duckdb_path)))
    monkeypatch.setattr(report, "build_viewer_leaderboard_mart", lambda duckdb_path, **_: calls.append(("mart", duckdb_path)))

    report.run_warehouse_build(plan, memory_monitor=report.MemoryMonitor(log_path=None))

    assert calls == [
        (
            "load",
            (
                "append",
                [Path("added_results")],
                [],
                None,
                True,
                True,
            ),
        ),
        ("append", duckdb_path),
        ("mart", duckdb_path),
    ]


def test_run_warehouse_build_append_plan_copies_base_duckdb_to_output(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    base_db = tmp_path / "base.duckdb"
    output_db = tmp_path / "merged.duckdb"
    base_db.write_bytes(b"base-db")
    args = report.build_arg_parser().parse_args(
        [
            "--append-results-dir",
            "added_results",
            "--append-base-duckdb",
            str(base_db),
            "--append-output-duckdb",
            str(output_db),
        ]
    )
    plan = report.resolve_warehouse_build_plan(args)
    viewer_config = ViewerConfig(
        benchmarks=[],
        overalls=[OverallConfig(name="Overall", label="Overall", benchmarks=[])],
    )
    calls: list[tuple[str, object]] = []

    monkeypatch.setattr(report, "load_viewer_config", lambda _path: viewer_config)
    monkeypatch.setattr(report, "_load_results_for_plan", lambda *_, **__: ([], [], [], [], [], [], {}))
    monkeypatch.setattr(report, "append_duckdb_results", lambda duckdb_path, **_: calls.append(("append", duckdb_path)))
    monkeypatch.setattr(report, "build_viewer_leaderboard_mart", lambda duckdb_path, **_: calls.append(("mart", duckdb_path)))

    report.run_warehouse_build(plan, memory_monitor=report.MemoryMonitor(log_path=None))

    assert output_db.read_bytes() == b"base-db"
    assert calls == [
        ("append", output_db),
        ("mart", output_db),
    ]


def test_run_warehouse_build_append_plan_downloads_latest_when_target_duckdb_is_missing(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    downloaded_db = tmp_path / "downloaded.duckdb"
    output_db = tmp_path / "hakari_bench.duckdb"
    downloaded_db.write_bytes(b"latest-db")
    args = report.build_arg_parser().parse_args(
        [
            "--append-results-dir",
            "added_results",
            "--duckdb-path",
            str(output_db),
            "--append-hf-dataset-repo-id",
            "hakari-bench/viewer-data",
        ]
    )
    plan = report.resolve_warehouse_build_plan(args)
    viewer_config = ViewerConfig(
        benchmarks=[],
        overalls=[OverallConfig(name="Overall", label="Overall", benchmarks=[])],
    )

    monkeypatch.setattr(report, "load_viewer_config", lambda _path: viewer_config)
    monkeypatch.setattr(report, "_download_hf_duckdb", lambda source: downloaded_db)
    monkeypatch.setattr(report, "_load_results_for_plan", lambda *_, **__: ([], [], [], [], [], [], {}))
    monkeypatch.setattr(report, "append_duckdb_results", lambda *_args, **_kwargs: None)
    monkeypatch.setattr(report, "build_viewer_leaderboard_mart", lambda *_args, **_kwargs: None)

    report.run_warehouse_build(plan, memory_monitor=report.MemoryMonitor(log_path=None))

    assert output_db.read_bytes() == b"latest-db"


def test_model_name_override_rewrites_loaded_result_rows(tmp_path: Path) -> None:
    results_dir = tmp_path / "results"
    task_path = results_dir / "source_model" / "hakari-bench__NanoJMTEB-v2" / "ja_cwir.json"
    _write_minimal_task_result(
        task_path,
        model_id="source/model",
        task_name="ja_cwir",
        score=0.42,
    )

    rows, runs, metric_rows, diagnostic_rows, _, _ = report.load_results(
        results_dir,
        model_name_override="local/model_exp_122",
    )

    assert [(row.model_dir, row.model_name) for row in rows] == [
        ("source_model", "local/model_exp_122"),
    ]
    assert [(row.model_name, row.metric_value) for row in metric_rows] == [
        ("local/model_exp_122", 0.42),
    ]
    assert [(row.model_name, row.base_score) for row in diagnostic_rows] == [
        ("local/model_exp_122", 0.42),
    ]
    assert [(run["model_dir"], run["model_name"]) for run in runs] == [
        ("source_model", "local/model_exp_122"),
    ]


def test_selected_result_jsons_can_discard_summary_payload_after_selection(tmp_path: Path) -> None:
    result_path = tmp_path / "model_A" / "hakari-bench__NanoJMTEB-v2" / "ja_cwir.json"
    _write_minimal_task_result(
        result_path,
        model_id="example/model_A",
        task_name="ja_cwir",
        score=0.42,
    )

    selected = report._selected_result_jsons(
        tmp_path,
        benchmark_configs=[BenchmarkConfig(name="NanoJMTEB-v2", matches=["NanoJMTEB-v2"])],
        target_benchmarks={"NanoJMTEB-v2"},
        exclude_model_names=set(),
        retain_summary_payload=False,
    )

    assert len(selected) == 1
    assert selected[0].payload == {}
    assert selected[0].model_name == "example/model_A"
    assert selected[0].task_name == "ja_cwir"


def test_read_result_json_from_summary_rereads_when_payload_was_discarded(tmp_path: Path) -> None:
    result_path = tmp_path / "model_A" / "hakari-bench__NanoJMTEB-v2" / "ja_cwir.json"
    _write_minimal_task_result(
        result_path,
        model_id="example/model_A",
        task_name="ja_cwir",
        score=0.42,
    )
    large_payload = json.loads(result_path.read_text(encoding="utf-8"))
    large_payload["large_metadata"] = "x" * (report.FULL_PARSE_RESULT_JSON_MAX_BYTES + 1)
    result_path.write_text(json.dumps(large_payload), encoding="utf-8")

    payload = report._read_result_json_from_summary(
        result_path,
        payload={},
        include_retrieval_rankings=False,
    )

    assert payload is not None
    assert payload["model"]["id"] == "example/model_A"
    assert payload["evaluation"]["aggregate_metric_value"] == 0.42


def test_write_duckdb_streaming_results_discards_selection_payloads(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    retain_values: list[bool] = []

    def selected_result_jsons(*_: object, retain_summary_payload: bool = True, **__: object) -> list[report.SelectedResultJson]:
        retain_values.append(retain_summary_payload)
        return []

    monkeypatch.setattr(report, "_selected_result_jsons", selected_result_jsons)

    report.write_duckdb_streaming_results(
        tmp_path / "results",
        tmp_path / "stream.duckdb",
        benchmark_configs=[],
    )

    assert retain_values == [False]


def test_top_ranking_selection_context_matches_selected_metric_rankings() -> None:
    evaluation = {
        "reranking_evaluations": [{"best_score_name": "cosine_bm25_top100_rerank"}],
        "embedding_evaluations": [
            {"name": "base", "best_score_name": "cosine"},
            {"name": "int8", "best_score_name": "int8_cosine"},
        ],
    }
    embedding_evaluations = report._embedding_evaluations(evaluation["embedding_evaluations"])
    rankings = [
        {"ranking_kind": "retrieval", "score_name": "cosine", "embedding_variant_name": None},
        {"ranking_kind": "retrieval", "score_name": "wrong", "embedding_variant_name": None},
        {"ranking_kind": "candidate_rerank", "score_name": "cosine_bm25_top100_rerank"},
        {
            "ranking_kind": "candidate_rerank",
            "score_name": "int8_cosine_bm25_top100_rerank",
            "embedding_variant_name": "int8",
        },
        {
            "ranking_kind": "candidate_rerank",
            "score_name": "wrong_bm25_top100_rerank",
            "embedding_variant_name": "int8",
        },
    ]
    context = report._top_ranking_selection_context(
        evaluation=evaluation,
        embedding_evaluations=embedding_evaluations,
    )

    selected_with_context = [
        report._selected_metric_ranking(ranking, context)
        for ranking in rankings
        if report._selected_metric_ranking(ranking, context) is not None
    ]
    selected_existing = report._selected_metric_rankings(
        rankings,
        evaluation=evaluation,
        embedding_evaluations=embedding_evaluations,
    )

    assert selected_with_context == selected_existing


def test_small_result_json_from_summary_uses_full_parse(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    result_path = tmp_path / "result.json"
    result_path.write_text("{}", encoding="utf-8")
    calls: list[str] = []

    def fake_read_json(path: Path) -> dict[str, object]:
        calls.append(f"read:{path.name}")
        return {"target": {}, "evaluation": {}, "artifacts": {"top_rankings": {"rankings": []}}}

    def fake_stream(*args: object, **kwargs: object) -> None:
        calls.append("stream")
        return None

    monkeypatch.setattr(report, "_read_json", fake_read_json)
    monkeypatch.setattr(report, "_read_top_rankings_artifact_stream", fake_stream)

    payload = report._read_result_json_from_summary(
        result_path,
        payload={"target": {}, "evaluation": {}},
        include_retrieval_rankings=False,
    )

    assert payload == {"target": {}, "evaluation": {}, "artifacts": {"top_rankings": {"rankings": []}}}
    assert calls == [f"read:{result_path.name}"]


def test_large_result_json_from_summary_keeps_streaming_path(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    result_path = tmp_path / "result.json"
    result_path.write_bytes(b"{}")
    calls: list[str] = []

    monkeypatch.setattr(report, "FULL_PARSE_RESULT_JSON_MAX_BYTES", 1)

    def fake_stream(*args: object, **kwargs: object) -> dict[str, object]:
        calls.append("stream")
        return {"rankings": []}

    monkeypatch.setattr(report, "_read_top_rankings_artifact_stream", fake_stream)

    payload = report._read_result_json_from_summary(
        result_path,
        payload={"target": {}, "evaluation": {}},
        include_retrieval_rankings=False,
    )

    assert payload == {"target": {}, "evaluation": {}, "artifacts": {"top_rankings": {"rankings": []}}}
    assert calls == ["stream"]


def test_insert_duckdb_rows_loads_rows_in_chunks() -> None:
    con = duckdb.connect()
    try:
        con.execute("CREATE TABLE sample (name VARCHAR, score DOUBLE)")

        report._insert_duckdb_rows(con, "sample", ("name", "score"), iter(()), chunk_size=1)
        report._insert_duckdb_rows(
            con,
            "sample",
            ("name", "score"),
            (("a", 0.1), ("b", 0.2), ("c", 0.3)),
            chunk_size=2,
        )

        assert con.execute("SELECT name, score FROM sample ORDER BY name").fetchall() == [
            ("a", 0.1),
            ("b", 0.2),
            ("c", 0.3),
        ]
    finally:
        con.close()


def test_read_json_reads_utf8_bytes(tmp_path: Path) -> None:
    path = tmp_path / "payload.json"
    path.write_text(json.dumps({"name": "日本語", "score": 0.42}), encoding="utf-8")

    assert report._read_json(path) == {"name": "日本語", "score": 0.42}


def test_read_json_falls_back_for_non_standard_json_numbers(tmp_path: Path) -> None:
    path = tmp_path / "payload.json"
    path.write_text('{"score": NaN}', encoding="utf-8")

    assert math.isnan(report._read_json(path)["score"])


def test_read_json_reads_compressed_result_json(tmp_path: Path) -> None:
    payload = {"name": "compressed", "score": 0.42}
    gzip_path = tmp_path / "payload.json.gz"
    xz_path = tmp_path / "payload.json.xz"
    with gzip.open(gzip_path, "wt", encoding="utf-8") as file:
        json.dump(payload, file)
    with lzma.open(xz_path, "wt", encoding="utf-8") as file:
        json.dump(payload, file)

    assert report._read_json(gzip_path) == payload
    assert report._read_json(xz_path) == payload


def test_result_json_paths_include_compressed_result_json(tmp_path: Path) -> None:
    results_dir = tmp_path / "results"
    task_dir = results_dir / "model" / "hakari-bench__NanoMIRACL"
    task_dir.mkdir(parents=True)
    json_path = task_dir / "en.json"
    gzip_path = task_dir / "ja.json.gz"
    xz_path = task_dir / "ko.json.xz"
    ignored_path = task_dir / "notes.jsonl"
    for path in [json_path, gzip_path, xz_path, ignored_path]:
        path.write_text("{}", encoding="utf-8")

    assert report._result_json_paths(results_dir) == [json_path, gzip_path, xz_path]


def test_memory_monitor_writes_jsonl_samples(tmp_path: Path) -> None:
    log_path = tmp_path / "memory.jsonl"
    monitor = report.MemoryMonitor(log_path=log_path, sample_interval=1)

    monitor.sample("start", processed_count=0)
    monitor.maybe_sample("selected", processed_count=1)

    samples = [json.loads(line) for line in log_path.read_text(encoding="utf-8").splitlines()]
    assert [sample["label"] for sample in samples] == ["start", "selected"]
    assert samples[0]["processed_count"] == 0
    assert samples[1]["processed_count"] == 1
    assert isinstance(samples[1]["peak_rss_bytes"], int)


def test_ordered_async_bounded_map_preserves_input_order() -> None:
    async def run() -> list[int]:
        async def submit(value: int) -> int:
            await asyncio.sleep(0.01 * (3 - value))
            return value * 10

        return [
            result
            async for result in report._ordered_async_bounded_map(
                [1, 2, 3],
                submit,
                max_pending=2,
            )
        ]

    assert asyncio.run(run()) == [10, 20, 30]


def test_nanomteb_chinese_is_a_ranked_benchmark() -> None:
    assert "NanoCMTEB" in report.TARGET_BENCHMARKS
    assert report.benchmark_name("hakari-bench/NanoCMTEB", "NanoCMTEB") == "NanoCMTEB"


def test_new_nano_benchmarks_are_ranked_benchmarks() -> None:
    assert "NanoBIRCO" in report.TARGET_BENCHMARKS
    assert "NanoDAPFAM" in report.TARGET_BENCHMARKS
    assert report.benchmark_name("hakari-bench/NanoBIRCO", "NanoBIRCO") == "NanoBIRCO"
    assert report.benchmark_name("hakari-bench/NanoDAPFAM", "NanoDAPFAM") == "NanoDAPFAM"


def test_int_or_none_ignores_non_finite_numbers() -> None:
    assert report._int_or_none(math.inf) is None
    assert report._int_or_none(-math.inf) is None
    assert report._int_or_none(math.nan) is None


def test_language_specific_nanomteb_benchmarks_are_ranked_separately() -> None:
    language_benchmarks = [
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

    for benchmark in language_benchmarks:
        assert benchmark in report.TARGET_BENCHMARKS
        assert report.benchmark_name(f"hakari-bench/{benchmark}", benchmark) == benchmark


def test_benchmark_name_uses_yaml_match_patterns_and_prefers_longest_match() -> None:
    benchmark_configs = [
        BenchmarkConfig(name="NanoMTEB", matches=["NanoMTEB"]),
        BenchmarkConfig(name="NanoMTEB-Dutch", matches=["NanoMTEB-Dutch"]),
        BenchmarkConfig(name="CustomBench", matches=["uploaded/custom-dataset"]),
        BenchmarkConfig(name="MNanoBEIR", matches=["NanoBEIR"]),
    ]

    assert (
        report.benchmark_name(
            "hakari-bench/NanoMTEB-Dutch",
            "NanoMTEB-Dutch",
            benchmark_configs=benchmark_configs,
        )
        == "NanoMTEB-Dutch"
    )
    assert (
        report.benchmark_name(
            "uploaded/custom-dataset",
            "arbitrary-name",
            benchmark_configs=benchmark_configs,
        )
        == "CustomBench"
    )
    assert (
        report.benchmark_name(
            "hakari-bench/NanoBEIR-en",
            "NanoBEIR-en",
            benchmark_configs=benchmark_configs,
        )
        == "MNanoBEIR"
    )


def test_load_results_uses_yaml_benchmark_matches(tmp_path: Path) -> None:
    model_dir = tmp_path / "model"
    task_path = model_dir / "uploaded__custom-dataset" / "task.json"
    task_path.parent.mkdir(parents=True)
    task_path.write_text(
        json.dumps(
            {
                "model": {"id": "example/model"},
                "target": {
                    "dataset_id": "uploaded/custom-dataset",
                    "dataset_name": "custom-name",
                    "task_name": "task",
                },
                "evaluation": {"aggregate_metric_value": 0.5},
            }
        ),
        encoding="utf-8",
    )

    rows, _, _, _, _, _ = report.load_results(
        tmp_path,
        benchmark_configs=[BenchmarkConfig(name="CustomBench", matches=["uploaded/custom-dataset"])],
    )

    assert len(rows) == 1
    assert rows[0].benchmark == "CustomBench"

def test_main_builds_duckdb_without_static_html_report(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    results_dir = tmp_path / "results"
    task_path = results_dir / "model" / "hakari-bench__NanoJMTEB-v2" / "ja_cwir.json"
    task_path.parent.mkdir(parents=True)
    task_path.write_text(
        json.dumps(
            {
                "model": {"id": "example/model"},
                "target": {
                    "dataset_name": "NanoJMTEB-v2",
                    "dataset_id": "hakari-bench/NanoJMTEB-v2",
                    "split_name": "ja_cwir",
                    "task_name": "ja_cwir",
                },
                "evaluation": {"aggregate_metric": "ndcg@10", "aggregate_metric_value": 0.42},
                "metrics": {"ja_cwir_ndcg@10": 0.42},
            }
        ),
        encoding="utf-8",
    )
    db_path = tmp_path / "hakari_bench.duckdb"
    html_path = tmp_path / "report.html"
    monkeypatch.setattr(
        sys,
        "argv",
        [
            "build_results_database_and_report.py",
            "--results-dir",
            str(results_dir),
            "--duckdb-path",
            str(db_path),
        ],
    )

    report.main()

    assert db_path.exists()
    assert not html_path.exists()


def test_load_results_reuses_unchanged_incremental_duckdb_rows(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    results_dir = tmp_path / "results"
    task_path = results_dir / "model" / "hakari-bench__NanoJMTEB-v2" / "ja_cwir.json"
    task_path.parent.mkdir(parents=True)
    task_path.write_text(
        json.dumps(
            {
                "model": {"id": "example/model"},
                "target": {
                    "dataset_name": "NanoJMTEB-v2",
                    "dataset_id": "hakari-bench/NanoJMTEB-v2",
                    "split_name": "ja_cwir",
                    "task_name": "ja_cwir",
                },
                "evaluation": {"aggregate_metric": "ndcg@10", "aggregate_metric_value": 0.42},
                "metrics": {"ja_cwir_ndcg@10": 0.42},
            }
        ),
        encoding="utf-8",
    )
    rows, runs, metric_rows, diagnostic_rows, dataset_metadata_rows, ranking_rows = report.load_results(results_dir)
    db_path = tmp_path / "hakari_bench.duckdb"
    report.write_duckdb(
        db_path,
        runs=runs,
        rows=rows,
        metric_rows=metric_rows,
        diagnostic_rows=diagnostic_rows,
        dataset_metadata_rows=dataset_metadata_rows,
        ranking_rows=ranking_rows,
        standings={},
        borda_rows=[],
    )
    monkeypatch.setattr(
        report,
        "_read_json",
        lambda path: pytest.fail(f"unchanged incremental cache should not parse {path}"),
    )

    cached_rows, cached_runs, cached_metric_rows, cached_diagnostic_rows, cached_dataset_metadata_rows, cached_ranking_rows = (
        report.load_results(results_dir, incremental_db_path=db_path)
    )

    assert cached_rows == rows
    assert cached_runs == runs
    assert cached_metric_rows == metric_rows
    assert cached_diagnostic_rows == diagnostic_rows
    assert cached_dataset_metadata_rows == dataset_metadata_rows
    assert cached_ranking_rows == []


def test_read_top_rankings_stream_keeps_only_selected_metric_rankings(tmp_path: Path) -> None:
    path = tmp_path / "result.json"
    payload = {
        "evaluation": {
            "embedding_evaluations": [
                {"name": "base", "best_score_name": "cosine"},
            ],
            "reranking_evaluations": [
                {"best_score_name": "cosine_reranking_hybrid_top100_rerank"},
            ],
        }
    }
    path.write_text(
        json.dumps(
            {
                **payload,
                "artifacts": {
                    "top_rankings": {
                        "schema_version": 1,
                        "top_k": 100,
                        "qrels": [{"query_id": "q1", "relevant_corpus_ids": ["d1"]}],
                        "rankings": [
                            {
                                "ranking_kind": "retrieval",
                                "score_name": "dot",
                                "query_id": "q1",
                                "corpus_ids": ["d2"],
                            },
                            {
                                "ranking_kind": "retrieval",
                                "score_name": "cosine",
                                "query_id": "q1",
                                "corpus_ids": ["d1"],
                            },
                            {
                                "ranking_kind": "candidate_rerank",
                                "score_name": "cosine_reranking_hybrid_top100_rerank",
                                "query_id": "q1",
                                "corpus_ids": ["d1", "d2"],
                                "safeguard_corpus_id": "d2",
                            },
                        ],
                    }
                },
            }
        ),
        encoding="utf-8",
    )

    artifact = report._read_top_rankings_artifact_stream(
        path,
        payload=payload,
        include_retrieval_rankings=False,
    )

    assert artifact is not None
    assert artifact["qrels"] == [{"query_id": "q1", "relevant_corpus_ids": ["d1"]}]
    assert [row["score_name"] for row in artifact["rankings"]] == [
        "cosine",
        "cosine_reranking_hybrid_top100_rerank",
    ]
    assert artifact["rankings"][1]["safeguard_corpus_id"] == "d2"


def test_read_top_rankings_stream_handles_late_selection_fields(tmp_path: Path) -> None:
    path = tmp_path / "result.json"
    payload = {
        "evaluation": {
            "embedding_evaluations": [
                {"name": "base", "best_score_name": "cosine"},
            ],
        }
    }
    path.write_text(
        json.dumps(
            {
                **payload,
                "artifacts": {
                    "top_rankings": {
                        "qrels": [{"query_id": "q1", "relevant_corpus_ids": ["d1"]}],
                        "rankings": [
                            {
                                "query_id": "q1",
                                "corpus_ids": ["d1", "d2"],
                                "ranking_kind": "retrieval",
                                "score_name": "cosine",
                            },
                        ],
                    }
                },
            }
        ),
        encoding="utf-8",
    )

    artifact = report._read_top_rankings_artifact_stream(
        path,
        payload=payload,
        include_retrieval_rankings=False,
    )

    assert artifact is not None
    assert artifact["rankings"] == [
        {
            "query_id": "q1",
            "corpus_ids": ["d1", "d2"],
            "ranking_kind": "retrieval",
            "score_name": "cosine",
        }
    ]


def test_load_results_recomputes_viewer_metrics_from_top_ranking_artifact(tmp_path: Path) -> None:
    results_dir = tmp_path / "results"
    task_path = results_dir / "model" / "hakari-bench__NanoMIRACL" / "en.json"
    task_path.parent.mkdir(parents=True)
    top_rankings = {
        "schema_version": 2,
        "top_k": 100,
        "qrels": [
            {"query_id": "q1", "relevant_corpus_ids": ["d2"]},
            {"query_id": "q2", "relevant_corpus_ids": ["d4"]},
        ],
        "rankings": [
            {
                "name": "base",
                "ranking_kind": "retrieval",
                "embedding_variant_name": None,
                "distance": "cosine",
                "score_name": "cosine",
                "query_id": "q1",
                "corpus_ids": ["d1", "d2"],
            },
            {
                "name": "base",
                "ranking_kind": "retrieval",
                "embedding_variant_name": None,
                "distance": "cosine",
                "score_name": "cosine",
                "query_id": "q2",
                "corpus_ids": ["d4", "d3"],
            },
            {
                "name": "truncate:2",
                "ranking_kind": "retrieval",
                "embedding_variant_name": "truncate:2",
                "distance": "cosine",
                "score_name": "truncate:2_cosine",
                "query_id": "q1",
                "corpus_ids": ["d1", "d2"],
            },
            {
                "name": "truncate:2",
                "ranking_kind": "retrieval",
                "embedding_variant_name": "truncate:2",
                "distance": "cosine",
                "score_name": "truncate:2_cosine",
                "query_id": "q2",
                "corpus_ids": ["d3", "d4"],
            },
            {
                "name": "base",
                "ranking_kind": "candidate_rerank",
                "embedding_variant_name": None,
                "distance": "cosine",
                "score_name": "cosine_bm25_top100_rerank",
                "query_id": "q1",
                "corpus_ids": ["d2", "d1"],
                "safeguard_policy": "RRF top-100 plus optional safeguard positive at rank 101",
                "safeguard_corpus_id": "d2",
            },
            {
                "name": "base",
                "ranking_kind": "candidate_rerank",
                "embedding_variant_name": None,
                "distance": "cosine",
                "score_name": "cosine_bm25_top100_rerank",
                "query_id": "q2",
                "corpus_ids": ["d3", "d4"],
                "safeguard_policy": "RRF top-100 plus optional safeguard positive at rank 101",
            },
            {
                "name": "truncate:2",
                "ranking_kind": "candidate_rerank",
                "embedding_variant_name": "truncate:2",
                "distance": "cosine",
                "score_name": "truncate:2_cosine_bm25_top100_rerank",
                "query_id": "q1",
                "corpus_ids": ["d2", "d1"],
                "safeguard_policy": "RRF top-100 plus optional safeguard positive at rank 101",
                "safeguard_corpus_id": "d2",
            },
            {
                "name": "truncate:2",
                "ranking_kind": "candidate_rerank",
                "embedding_variant_name": "truncate:2",
                "distance": "cosine",
                "score_name": "truncate:2_cosine_bm25_top100_rerank",
                "query_id": "q2",
                "corpus_ids": ["d4", "d3"],
                "safeguard_policy": "RRF top-100 plus optional safeguard positive at rank 101",
            },
        ],
    }
    task_path.write_text(
        json.dumps(
            {
                "model": {"id": "example/model"},
                "target": {
                    "dataset_name": "NanoMIRACL",
                    "dataset_id": "hakari-bench/NanoMIRACL",
                    "split_name": "en",
                    "task_name": "en",
                },
                "evaluation": {
                    "aggregate_metric": "ndcg@10",
                    "aggregate_metric_value": 0.42,
                    "rerank_aggregate_metric_value": 0.70,
                    "embedding_evaluations": [
                        {
                            "name": "base",
                            "aggregate_metric": "ndcg@10",
                            "aggregate_metric_value": 0.42,
                            "best_score_name": "cosine",
                        },
                        {
                            "name": "truncate:2",
                            "aggregate_metric": "ndcg@10",
                            "aggregate_metric_value": 0.30,
                            "best_score_name": "truncate:2_cosine",
                        },
                    ],
                    "reranking_evaluations": [
                        {
                            "name": "bm25_top_100",
                            "best_score_name": "cosine_bm25_top100_rerank",
                            "aggregate_metric": "ndcg@10",
                            "aggregate_metric_value": 0.70,
                        }
                    ],
                },
                "metrics": {"NanoMIRACL_en_cosine_ndcg@10": 0.42, "NanoMIRACL_en_cosine_acc@100": 1.0},
                "rerank_metrics": {"NanoMIRACL_en_cosine_bm25_top100_rerank_ndcg@10": 0.70},
                "artifacts": {"top_rankings": top_rankings},
            }
        ),
        encoding="utf-8",
    )

    _, _, metric_rows, _, _, _ = report.load_results(results_dir)

    metric_values = {
        (row.score_target, row.embedding_variant_name, row.metric_name): row.metric_value
        for row in metric_rows
    }
    assert metric_values[("all", None, "en_cosine_acc@1")] == pytest.approx(0.5)
    assert metric_values[("all", None, "en_cosine_acc@10")] == pytest.approx(1.0)
    assert metric_values[("all", None, "en_cosine_acc@100")] == pytest.approx(1.0)
    assert metric_values[("all", None, "en_cosine_ndcg@10")] == pytest.approx((1 / math.log2(3) + 1) / 2)
    assert metric_values[("all", None, "en_cosine_ndcg@100")] == pytest.approx((1 / math.log2(3) + 1) / 2)
    assert metric_values[("all", None, "en_cosine_recall@100")] == pytest.approx(1.0)
    assert metric_values[("all", "truncate:2", "en_truncate:2_cosine_acc@10")] == pytest.approx(1.0)
    assert metric_values[("all", "truncate:2", "en_truncate:2_cosine_ndcg@100")] == pytest.approx(
        1 / math.log2(3)
    )
    assert metric_values[("all", "truncate:2", "en_truncate:2_cosine_recall@100")] == pytest.approx(1.0)
    assert metric_values[("reranking", None, "en_cosine_bm25_top100_rerank_acc@1")] == pytest.approx(0.5)
    assert metric_values[("reranking", None, "en_cosine_bm25_top100_rerank_acc@10")] == pytest.approx(1.0)
    assert metric_values[("reranking", None, "en_cosine_bm25_top100_rerank_ndcg@100")] == pytest.approx(
        (1 + 1 / math.log2(3)) / 2
    )
    assert metric_values[("reranking", None, "en_cosine_bm25_top100_rerank_recall@100")] == pytest.approx(1.0)
    assert metric_values[("reranking", "truncate:2", "en_truncate:2_cosine_bm25_top100_rerank_acc@1")] == pytest.approx(1.0)
    assert metric_values[("reranking", "truncate:2", "en_truncate:2_cosine_bm25_top100_rerank_acc@10")] == pytest.approx(1.0)
    assert metric_values[
        ("reranking", "truncate:2", "en_truncate:2_cosine_bm25_top100_rerank_recall@100")
    ] == pytest.approx(1.0)
    assert metric_values[
        ("reranking_without_safeguard", None, "en_cosine_bm25_top100_rerank_acc@1")
    ] == pytest.approx(0.0)
    assert metric_values[
        ("reranking_without_safeguard", None, "en_cosine_bm25_top100_rerank_acc@10")
    ] == pytest.approx(0.5)
    assert metric_values[
        ("reranking_without_safeguard", "truncate:2", "en_truncate:2_cosine_bm25_top100_rerank_acc@1")
    ] == pytest.approx(0.5)
    assert metric_values[
        ("reranking_without_safeguard", "truncate:2", "en_truncate:2_cosine_bm25_top100_rerank_recall@100")
    ] == pytest.approx(0.5)


def test_query_rankings_from_artifact_row_reuses_string_corpus_ids() -> None:
    corpus_ids = ["d1", "d2"]

    query_rankings = report._query_rankings_from_artifact_row(
        {"query_id": "q1", "corpus_ids": corpus_ids}
    )

    assert query_rankings == {"q1": ["d1", "d2"]}
    assert query_rankings["q1"] is corpus_ids


def test_query_rankings_from_artifact_row_converts_non_string_values() -> None:
    query_rankings = report._query_rankings_from_artifact_row(
        {"query_id": 1, "corpus_ids": [2, "d3"]}
    )

    assert query_rankings == {"1": ["2", "d3"]}


def test_load_results_parallel_json_workers_match_serial(tmp_path: Path) -> None:
    results_dir = tmp_path / "results"
    for task_name, score in [("en", 0.42), ("ja", 0.35)]:
        task_path = results_dir / "model" / "hakari-bench__NanoMIRACL" / f"{task_name}.json"
        task_path.parent.mkdir(parents=True, exist_ok=True)
        task_path.write_text(
            json.dumps(
                {
                    "model": {"id": "example/model"},
                    "target": {
                        "dataset_name": "NanoMIRACL",
                        "dataset_id": "hakari-bench/NanoMIRACL",
                        "split_name": task_name,
                        "task_name": task_name,
                    },
                    "evaluation": {
                        "aggregate_metric": "ndcg@10",
                        "aggregate_metric_value": score,
                        "reranking_evaluations": [
                            {
                                "name": "bm25_top_100",
                                "best_score_name": "cosine_bm25_top100_rerank",
                                "aggregate_metric": "ndcg@10",
                                "aggregate_metric_value": score + 0.1,
                            }
                        ],
                    },
                    "metrics": {f"NanoMIRACL_{task_name}_cosine_ndcg@10": score},
                    "rerank_metrics": {f"NanoMIRACL_{task_name}_cosine_bm25_top100_rerank_ndcg@10": score + 0.1},
                    "artifacts": {
                        "top_rankings": {
                            "schema_version": 2,
                            "top_k": 100,
                            "qrels": [{"query_id": "q1", "relevant_corpus_ids": ["d2"]}],
                            "rankings": [
                                {
                                    "name": "base",
                                    "ranking_kind": "candidate_rerank",
                                    "embedding_variant_name": None,
                                    "score_name": "cosine_bm25_top100_rerank",
                                    "query_id": "q1",
                                    "corpus_ids": ["d2", "d1"],
                                    "safeguard_corpus_id": "d2",
                                }
                            ],
                        }
                    },
                }
            ),
            encoding="utf-8",
        )

    serial = report.load_results(results_dir, result_json_workers=1)
    parallel = report.load_results(results_dir, result_json_workers=2)

    assert parallel == serial


def test_load_results_parallel_selection_workers_match_serial(tmp_path: Path) -> None:
    results_dir = tmp_path / "results"
    for task_name, score in [("en", 0.42), ("ja", 0.35)]:
        task_path = results_dir / "model" / "hakari-bench__NanoMIRACL" / f"{task_name}.json"
        task_path.parent.mkdir(parents=True, exist_ok=True)
        task_path.write_text(
            json.dumps(
                {
                    "model": {"id": "example/model"},
                    "target": {
                        "dataset_name": "NanoMIRACL",
                        "dataset_id": "hakari-bench/NanoMIRACL",
                        "split_name": task_name,
                        "task_name": task_name,
                    },
                    "evaluation": {
                        "aggregate_metric": "ndcg@10",
                        "aggregate_metric_value": score,
                    },
                    "metrics": {f"NanoMIRACL_{task_name}_cosine_ndcg@10": score},
                }
            ),
            encoding="utf-8",
        )

    serial = report.load_results(results_dir, result_selection_workers=1)
    parallel = report.load_results(results_dir, result_selection_workers=2)

    assert parallel == serial


def test_selected_result_json_records_payload_sha256(tmp_path: Path) -> None:
    results_dir = tmp_path / "results"
    task_path = results_dir / "model" / "hakari-bench__NanoMIRACL" / "en.json"
    task_path.parent.mkdir(parents=True)
    task_path.write_text(
        json.dumps(
            {
                "model": {"id": "example/model"},
                "target": {
                    "dataset_name": "NanoMIRACL",
                    "dataset_id": "hakari-bench/NanoMIRACL",
                    "split_name": "en",
                    "task_name": "en",
                },
                "evaluation": {"aggregate_metric": "ndcg@10", "aggregate_metric_value": 0.42},
                "metrics": {"NanoMIRACL_en_cosine_ndcg@10": 0.42},
                "artifacts": {"top_rankings": {"rankings": []}},
            }
        ),
        encoding="utf-8",
    )

    selected = report._selected_result_json(
        task_path,
        results_dir=results_dir,
        source_priority=0,
        benchmark_configs=report.load_benchmark_configs(),
        target_benchmarks=set(report.TARGET_BENCHMARKS),
        exclude_model_names=set(),
    )

    assert selected is not None
    assert selected.payload_sha256 == hashlib.sha256(task_path.read_bytes()).hexdigest()


def test_process_result_rows_worker_reuses_selected_summary_payload(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    selected = report.SelectedResultJson(
        result_path=tmp_path / "result.json",
        results_dir=tmp_path,
        source_priority=0,
        payload={
            "model": {"id": "example/model"},
            "target": {
                "dataset_name": "NanoMIRACL",
                "dataset_id": "hakari-bench/NanoMIRACL",
                "split_name": "en",
                "task_name": "en",
            },
            "evaluation": {
                "aggregate_metric": "ndcg@10",
                "aggregate_metric_value": 0.42,
            },
            "metrics": {"NanoMIRACL_en_cosine_ndcg@10": 0.42},
        },
        benchmark="NanoMIRACL",
        model_dir="model",
        model_name="example/model",
        dataset_id="hakari-bench/NanoMIRACL",
        task_name="en",
        task_key="NanoMIRACL::hakari-bench/NanoMIRACL::en",
        payload_sha256="abc123",
    )

    monkeypatch.setattr(
        report,
        "_read_result_json",
        lambda *args, **kwargs: pytest.fail("worker should not reread result JSON summary"),
    )

    def fake_from_summary(
        result_path: Path,
        *,
        payload: dict[str, object],
        include_retrieval_rankings: bool,
    ) -> dict[str, object]:
        assert result_path == selected.result_path
        assert payload is selected.payload
        assert include_retrieval_rankings is False
        return payload | {"from_selected_summary": True}

    monkeypatch.setattr(report, "_read_result_json_from_summary", fake_from_summary)

    def fake_process_result_rows(**kwargs: object) -> report.ProcessedResultRows:
        task_payload = cast(dict[str, Any], kwargs["task_payload"])
        assert isinstance(task_payload, dict)
        assert task_payload["from_selected_summary"] is True
        return report.ProcessedResultRows(
            rows=[],
            run_accumulators={},
            metric_rows=[],
            diagnostic_rows=[],
            dataset_metadata_rows=[],
            ranking_rows=[],
        )

    monkeypatch.setattr(report, "_process_result_rows", fake_process_result_rows)

    assert report._process_result_rows_worker(
        selected,
        include_retrieval_rankings=False,
        model_cards_path=None,
    ) == report.ProcessedResultRows(
        rows=[],
        run_accumulators={},
        metric_rows=[],
        diagnostic_rows=[],
        dataset_metadata_rows=[],
        ranking_rows=[],
    )


def test_load_results_parallel_row_workers_match_serial(tmp_path: Path) -> None:
    results_dir = tmp_path / "results"
    for task_name, score in [("en", 0.42), ("ja", 0.35)]:
        task_path = results_dir / "model" / "hakari-bench__NanoMIRACL" / f"{task_name}.json"
        task_path.parent.mkdir(parents=True, exist_ok=True)
        task_path.write_text(
            json.dumps(
                {
                    "model": {"id": "example/model"},
                    "target": {
                        "dataset_name": "NanoMIRACL",
                        "dataset_id": "hakari-bench/NanoMIRACL",
                        "split_name": task_name,
                        "task_name": task_name,
                    },
                    "evaluation": {
                        "aggregate_metric": "ndcg@10",
                        "aggregate_metric_value": score,
                        "embedding_evaluations": [
                            {
                                "name": "base",
                                "aggregate_metric": "ndcg@10",
                                "aggregate_metric_value": score,
                                "best_score_name": "cosine",
                            },
                            {
                                "name": "truncate:2",
                                "aggregate_metric": "ndcg@10",
                                "aggregate_metric_value": score - 0.05,
                                "best_score_name": "truncate:2_cosine",
                            },
                        ],
                        "reranking_evaluations": [
                            {
                                "name": "bm25_top_100",
                                "best_score_name": "cosine_bm25_top100_rerank",
                                "aggregate_metric": "ndcg@10",
                                "aggregate_metric_value": score + 0.1,
                            }
                        ],
                    },
                    "metrics": {f"NanoMIRACL_{task_name}_cosine_ndcg@10": score},
                    "rerank_metrics": {f"NanoMIRACL_{task_name}_cosine_bm25_top100_rerank_ndcg@10": score + 0.1},
                    "artifacts": {
                        "top_rankings": {
                            "schema_version": 2,
                            "top_k": 100,
                            "qrels": [{"query_id": "q1", "relevant_corpus_ids": ["d2"]}],
                            "rankings": [
                                {
                                    "name": "base",
                                    "ranking_kind": "retrieval",
                                    "embedding_variant_name": None,
                                    "score_name": "cosine",
                                    "query_id": "q1",
                                    "corpus_ids": ["d1", "d2"],
                                },
                                {
                                    "name": "base",
                                    "ranking_kind": "candidate_rerank",
                                    "embedding_variant_name": None,
                                    "score_name": "cosine_bm25_top100_rerank",
                                    "query_id": "q1",
                                    "corpus_ids": ["d2", "d1"],
                                    "safeguard_corpus_id": "d2",
                                },
                            ],
                        }
                    },
                }
            ),
            encoding="utf-8",
        )

    serial = report.load_results(results_dir, result_row_workers=1)
    parallel = report.load_results(results_dir, result_row_workers=2)

    assert parallel == serial


def test_write_duckdb_streaming_results_matches_materialized_build(tmp_path: Path) -> None:
    results_dir = tmp_path / "results"
    for task_name, score in [("en", 0.42), ("ja", 0.35)]:
        task_path = results_dir / "model" / "hakari-bench__NanoMIRACL" / f"{task_name}.json"
        task_path.parent.mkdir(parents=True, exist_ok=True)
        task_path.write_text(
            json.dumps(
                {
                    "model": {"id": "example/model"},
                    "target": {
                        "dataset_name": "NanoMIRACL",
                        "dataset_id": "hakari-bench/NanoMIRACL",
                        "split_name": task_name,
                        "task_name": task_name,
                    },
                    "evaluation": {
                        "aggregate_metric": "ndcg@10",
                        "aggregate_metric_value": score,
                        "embedding_evaluations": [
                            {
                                "name": "base",
                                "aggregate_metric": "ndcg@10",
                                "aggregate_metric_value": score,
                                "best_score_name": "cosine",
                            }
                        ],
                    },
                    "metrics": {f"NanoMIRACL_{task_name}_cosine_ndcg@10": score},
                    "artifacts": {
                        "top_rankings": {
                            "schema_version": 2,
                            "top_k": 100,
                            "qrels": [{"query_id": "q1", "relevant_corpus_ids": ["d2"]}],
                            "rankings": [
                                {
                                    "name": "base",
                                    "ranking_kind": "retrieval",
                                    "embedding_variant_name": None,
                                    "score_name": "cosine",
                                    "query_id": "q1",
                                    "corpus_ids": ["d1", "d2"],
                                }
                            ],
                        }
                    },
                }
            ),
            encoding="utf-8",
        )

    benchmark_configs = report.load_benchmark_configs()
    rows, runs, metric_rows, diagnostic_rows, dataset_metadata_rows, ranking_rows, source_hashes = report.load_results(
        results_dir,
        benchmark_configs=benchmark_configs,
        include_source_hashes=True,
    )
    materialized_db = tmp_path / "materialized.duckdb"
    report.write_duckdb(
        materialized_db,
        runs=runs,
        rows=rows,
        metric_rows=metric_rows,
        diagnostic_rows=diagnostic_rows,
        dataset_metadata_rows=dataset_metadata_rows,
        ranking_rows=ranking_rows,
        standings={},
        borda_rows=[],
        source_payload_sha256_by_path=source_hashes,
    )
    streaming_db = tmp_path / "streaming.duckdb"
    report.write_duckdb_streaming_results(
        results_dir,
        streaming_db,
        benchmark_configs=benchmark_configs,
        result_selection_workers=1,
        result_json_workers=1,
        result_row_workers=1,
        insert_chunk_size=1,
    )

    con = duckdb.connect()
    try:
        con.execute(f"ATTACH '{materialized_db}' AS materialized")
        con.execute(f"ATTACH '{streaming_db}' AS streaming")
        source_columns = "result_path, payload_sha256, canonical_key_hash"
        assert con.execute(
            f"""
            SELECT count(*)
            FROM (
                SELECT {source_columns} FROM materialized.source_load_state
                EXCEPT
                SELECT {source_columns} FROM streaming.source_load_state
            )
            """
        ).fetchone() == (0,)
        assert con.execute(
            f"""
            SELECT count(*)
            FROM (
                SELECT {source_columns} FROM streaming.source_load_state
                EXCEPT
                SELECT {source_columns} FROM materialized.source_load_state
            )
            """
        ).fetchone() == (0,)
        for table in [
            "runs",
            "task_results",
            "metrics_long",
            "task_diagnostics",
            "dataset_metadata",
            "viewer_task_results",
            "viewer_filter_values",
        ]:
            assert con.execute(
                f"SELECT count(*) FROM (SELECT * FROM materialized.{table} EXCEPT SELECT * FROM streaming.{table})"
            ).fetchone() == (0,)
            assert con.execute(
                f"SELECT count(*) FROM (SELECT * FROM streaming.{table} EXCEPT SELECT * FROM materialized.{table})"
            ).fetchone() == (0,)
        assert con.execute(
            """
            SELECT result_path
            FROM streaming.metrics_long
            """
        ).fetchall() == con.execute(
            """
            SELECT result_path
            FROM streaming.metrics_long
            ORDER BY result_path, metric_name, score_target, embedding_variant_name,
                     model_name, benchmark, dataset_id, task_name
            """
        ).fetchall()
    finally:
        con.close()


def test_compact_duckdb_database_preserves_live_tables(tmp_path: Path) -> None:
    db_path = tmp_path / "results.duckdb"
    con = duckdb.connect(str(db_path))
    try:
        con.execute("CREATE TABLE kept AS SELECT 1 AS id, 'ok' AS value")
        con.execute("CREATE TABLE discarded AS SELECT range AS id FROM range(1000)")
        con.execute("DROP TABLE discarded")
        con.execute("CHECKPOINT")
    finally:
        con.close()

    report._compact_duckdb_database(db_path)

    con = duckdb.connect(str(db_path), read_only=True)
    try:
        assert con.execute("SELECT * FROM kept").fetchall() == [(1, "ok")]
        assert con.execute(
            """
            SELECT table_name
            FROM duckdb_tables()
            WHERE database_name = current_database()
              AND schema_name = 'main'
            ORDER BY table_name
            """
        ).fetchall() == [("kept",)]
    finally:
        con.close()


def test_read_result_json_drops_unneeded_retrieval_rankings(tmp_path: Path) -> None:
    results_dir = tmp_path / "results"
    task_path = results_dir / "model" / "hakari-bench__NanoMIRACL" / "en.json"
    task_path.parent.mkdir(parents=True)
    task_path.write_text(
        json.dumps(
            {
                "model": {"id": "example/model"},
                "target": {
                    "dataset_name": "NanoMIRACL",
                    "dataset_id": "hakari-bench/NanoMIRACL",
                    "split_name": "en",
                    "task_name": "en",
                },
                "evaluation": {
                    "aggregate_metric": "ndcg@10",
                    "aggregate_metric_value": 0.42,
                    "embedding_evaluations": [
                        {
                            "name": "base",
                            "aggregate_metric": "ndcg@10",
                            "aggregate_metric_value": 0.42,
                            "best_score_name": "cosine",
                        }
                    ],
                    "reranking_evaluations": [
                        {
                            "name": "bm25_top_100",
                            "best_score_name": "cosine_bm25_top100_rerank",
                            "aggregate_metric": "ndcg@10",
                            "aggregate_metric_value": 0.70,
                        }
                    ],
                },
                "artifacts": {
                    "top_rankings": {
                        "schema_version": 2,
                        "top_k": 100,
                        "qrels": [{"query_id": "q1", "relevant_corpus_ids": ["d2"]}],
                        "rankings": [
                            {
                                "name": "base",
                                "ranking_kind": "retrieval",
                                "embedding_variant_name": None,
                                "score_name": "cosine",
                                "query_id": "q1",
                                "corpus_ids": ["d1", "d2"],
                            },
                            {
                                "name": "base",
                                "ranking_kind": "retrieval",
                                "embedding_variant_name": None,
                                "score_name": "dot",
                                "query_id": "q1",
                                "corpus_ids": ["d2", "d1"],
                            },
                            {
                                "name": "base",
                                "ranking_kind": "candidate_rerank",
                                "embedding_variant_name": None,
                                "score_name": "cosine_bm25_top100_rerank",
                                "query_id": "q1",
                                "corpus_ids": ["d2", "d1"],
                                "safeguard_corpus_id": "d2",
                            },
                        ],
                    }
                },
            }
        ),
        encoding="utf-8",
    )

    task_payload = report._read_result_json(
        task_path,
        include_retrieval_rankings=False,
    )
    assert task_payload is not None
    artifact = task_payload["artifacts"]["top_rankings"]
    assert artifact["qrels"] == [{"query_id": "q1", "relevant_corpus_ids": ["d2"]}]
    assert [(row["ranking_kind"], row["score_name"]) for row in artifact["rankings"]] == [
        ("retrieval", "cosine"),
        ("candidate_rerank", "cosine_bm25_top100_rerank"),
    ]

    task_payload_with_rankings = report._read_result_json(
        task_path,
        include_retrieval_rankings=True,
    )
    assert task_payload_with_rankings is not None
    full_artifact = task_payload_with_rankings["artifacts"]["top_rankings"]
    assert [row["score_name"] for row in full_artifact["rankings"]] == [
        "cosine",
        "dot",
        "cosine_bm25_top100_rerank",
    ]


def test_selected_result_json_uses_streaming_reader_for_result_payload(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    results_dir = tmp_path / "results"
    task_path = results_dir / "model" / "hakari-bench__NanoMIRACL" / "en.json.gz"
    task_path.parent.mkdir(parents=True)
    with gzip.open(task_path, "wt", encoding="utf-8") as file:
        json.dump(
            {
                "model": {"id": "example/model"},
                "target": {
                    "dataset_name": "NanoMIRACL",
                    "dataset_id": "hakari-bench/NanoMIRACL",
                    "split_name": "en",
                    "task_name": "en",
                },
                "evaluation": {"aggregate_metric": "ndcg@10", "aggregate_metric_value": 0.42},
                "metrics": {"NanoMIRACL_en_cosine_ndcg@10": 0.42},
                "artifacts": {"top_rankings": {"schema_version": 2, "top_k": 100, "qrels": [], "rankings": []}},
            },
            file,
        )
    monkeypatch.setattr(report, "_read_json", lambda path: pytest.fail(f"should stream {path}"))

    selected = report._selected_result_json(
        task_path,
        results_dir=results_dir,
        source_priority=0,
        benchmark_configs=report.load_benchmark_configs(),
        target_benchmarks=set(report.TARGET_BENCHMARKS),
        exclude_model_names=set(),
    )

    assert selected is not None
    assert selected.model_name == "example/model"


def test_main_incremental_noops_when_sources_are_unchanged(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    results_dir = tmp_path / "results"
    task_path = results_dir / "model" / "hakari-bench__NanoJMTEB-v2" / "ja_cwir.json"
    task_path.parent.mkdir(parents=True)
    task_path.write_text(
        json.dumps(
            {
                "model": {"id": "example/model"},
                "target": {
                    "dataset_name": "NanoJMTEB-v2",
                    "dataset_id": "hakari-bench/NanoJMTEB-v2",
                    "split_name": "ja_cwir",
                    "task_name": "ja_cwir",
                },
                "evaluation": {"aggregate_metric": "ndcg@10", "aggregate_metric_value": 0.42},
                "metrics": {"ja_cwir_ndcg@10": 0.42},
            }
        ),
        encoding="utf-8",
    )
    rows, runs, metric_rows, diagnostic_rows, dataset_metadata_rows, ranking_rows = report.load_results(results_dir)
    db_path = tmp_path / "hakari_bench.duckdb"
    report.write_duckdb(
        db_path,
        runs=runs,
        rows=rows,
        metric_rows=metric_rows,
        diagnostic_rows=diagnostic_rows,
        dataset_metadata_rows=dataset_metadata_rows,
        ranking_rows=ranking_rows,
        standings={},
        borda_rows=[],
    )
    monkeypatch.setattr(
        report,
        "write_duckdb",
        lambda *args, **kwargs: pytest.fail("unchanged incremental build should not rewrite DuckDB"),
    )
    monkeypatch.setattr(
        sys,
        "argv",
        [
            "build_results_database_and_report.py",
            "--incremental",
            "--results-dir",
            str(results_dir),
            "--duckdb-path",
            str(db_path),
        ],
    )

    report.main()


def test_load_results_incremental_parses_only_changed_sources(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    results_dir = tmp_path / "results"
    first_path = results_dir / "model" / "hakari-bench__NanoJMTEB-v2" / "ja_cwir.json"
    second_path = results_dir / "model" / "hakari-bench__NanoJMTEB-v2" / "ja_nfcorpus.json"
    first_path.parent.mkdir(parents=True)
    for task_path, score in ((first_path, 0.42), (second_path, 0.24)):
        task_path.write_text(
            json.dumps(
                {
                    "model": {"id": "example/model"},
                    "target": {
                        "dataset_name": "NanoJMTEB-v2",
                        "dataset_id": "hakari-bench/NanoJMTEB-v2",
                        "split_name": task_path.stem,
                        "task_name": task_path.stem,
                    },
                    "evaluation": {"aggregate_metric": "ndcg@10", "aggregate_metric_value": score},
                    "metrics": {f"{task_path.stem}_ndcg@10": score},
                }
            ),
            encoding="utf-8",
        )
    rows, runs, metric_rows, diagnostic_rows, dataset_metadata_rows, ranking_rows = report.load_results(results_dir)
    db_path = tmp_path / "hakari_bench.duckdb"
    report.write_duckdb(
        db_path,
        runs=runs,
        rows=rows,
        metric_rows=metric_rows,
        diagnostic_rows=diagnostic_rows,
        dataset_metadata_rows=dataset_metadata_rows,
        ranking_rows=ranking_rows,
        standings={},
        borda_rows=[],
    )
    second_path.write_text(
        json.dumps(
            {
                "model": {"id": "example/model"},
                "target": {
                    "dataset_name": "NanoJMTEB-v2",
                    "dataset_id": "hakari-bench/NanoJMTEB-v2",
                    "split_name": "ja_nfcorpus",
                    "task_name": "ja_nfcorpus",
                },
                "evaluation": {"aggregate_metric": "ndcg@10", "aggregate_metric_value": 0.9},
                "metrics": {"ja_nfcorpus_ndcg@10": 0.9},
            }
        ),
        encoding="utf-8",
    )
    original_read_json = report._read_json

    def read_changed_only(path: Path) -> object:
        if path == first_path:
            pytest.fail("unchanged source should be reused from the incremental DuckDB cache")
        return original_read_json(path)

    monkeypatch.setattr(report, "_read_json", read_changed_only)

    cached_rows, cached_runs, cached_metric_rows, _, _, _ = report.load_results(
        results_dir,
        incremental_db_path=db_path,
    )

    scores_by_task = {row.task_name: row.score for row in cached_rows}
    metric_scores_by_task = {row.task_name: row.metric_value for row in cached_metric_rows}
    assert scores_by_task == {"ja_cwir": 0.42, "ja_nfcorpus": 0.9}
    assert metric_scores_by_task == {"ja_cwir": 0.42, "ja_nfcorpus": 0.9}
    assert cached_runs[0]["aggregate_metric_mean"] == pytest.approx(0.66)


def test_load_results_incremental_parses_only_added_sources(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    base_dir = tmp_path / "base"
    added_dir = tmp_path / "added"
    existing_path = base_dir / "model_A" / "hakari-bench__NanoJMTEB-v2" / "ja_cwir.json"
    added_path = added_dir / "model_B" / "hakari-bench__NanoJMTEB-v2" / "ja_cwir.json"
    _write_minimal_task_result(
        existing_path,
        model_id="example/model_A",
        task_name="ja_cwir",
        score=0.42,
    )
    rows, runs, metric_rows, diagnostic_rows, dataset_metadata_rows, ranking_rows = report.load_results(base_dir)
    db_path = tmp_path / "hakari_bench.duckdb"
    report.write_duckdb(
        db_path,
        runs=runs,
        rows=rows,
        metric_rows=metric_rows,
        diagnostic_rows=diagnostic_rows,
        dataset_metadata_rows=dataset_metadata_rows,
        ranking_rows=ranking_rows,
        standings={},
        borda_rows=[],
    )
    _write_minimal_task_result(
        added_path,
        model_id="example/model_B",
        task_name="ja_cwir",
        score=0.84,
    )
    original_read_json = report._read_json

    def read_added_only(path: Path) -> object:
        if path == existing_path:
            pytest.fail("unchanged existing source should be reused from the incremental DuckDB cache")
        return original_read_json(path)

    monkeypatch.setattr(report, "_read_json", read_added_only)

    cached_rows, cached_runs, cached_metric_rows, cached_diagnostic_rows, _, _ = report.load_results(
        [added_dir, base_dir],
        incremental_db_path=db_path,
    )

    assert [(row.model_name, row.score) for row in cached_rows] == [
        ("example/model_A", 0.42),
        ("example/model_B", 0.84),
    ]
    assert [(row.model_name, row.metric_value) for row in cached_metric_rows] == [
        ("example/model_A", 0.42),
        ("example/model_B", 0.84),
    ]
    assert [(row.model_name, row.base_score) for row in cached_diagnostic_rows] == [
        ("example/model_A", 0.42),
        ("example/model_B", 0.84),
    ]
    assert [(run["model_name"], run["aggregate_metric_mean"]) for run in cached_runs] == [
        ("example/model_A", 0.42),
        ("example/model_B", 0.84),
    ]


def test_main_appends_results_dir_to_existing_duckdb_without_reading_existing_json(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    base_dir = tmp_path / "base"
    added_dir = tmp_path / "added"
    existing_path = base_dir / "model_A" / "hakari-bench__NanoJMTEB-v2" / "ja_cwir.json"
    added_path = added_dir / "model_B" / "hakari-bench__NanoJMTEB-v2" / "ja_cwir.json"
    _write_minimal_task_result(
        existing_path,
        model_id="example/model_A",
        task_name="ja_cwir",
        score=0.42,
    )
    rows, runs, metric_rows, diagnostic_rows, dataset_metadata_rows, ranking_rows = report.load_results(base_dir)
    db_path = tmp_path / "hakari_bench.duckdb"
    report.write_duckdb(
        db_path,
        runs=runs,
        rows=rows,
        metric_rows=metric_rows,
        diagnostic_rows=diagnostic_rows,
        dataset_metadata_rows=dataset_metadata_rows,
        ranking_rows=ranking_rows,
        standings={},
        borda_rows=[],
    )
    _write_minimal_task_result(
        added_path,
        model_id="example/model_B",
        task_name="ja_cwir",
        score=0.84,
    )
    original_read_json = report._read_json

    def read_added_only(path: Path) -> object:
        if path == existing_path:
            pytest.fail("append mode should not read existing result JSON")
        return original_read_json(path)

    monkeypatch.setattr(report, "_read_json", read_added_only)
    monkeypatch.setattr(
        sys,
        "argv",
        [
            "build_results_database_and_report.py",
            "--append-results-dir",
            str(added_dir),
            "--duckdb-path",
            str(db_path),
        ],
    )

    report.main()

    con = duckdb.connect(str(db_path), read_only=True)
    try:
        assert con.execute(
            "SELECT model_name, score FROM task_results ORDER BY model_name"
        ).fetchall() == [
            ("example/model_A", 0.42),
            ("example/model_B", 0.84),
        ]
        assert con.execute("SELECT count(*) FROM source_load_state").fetchone() == (2,)
        assert con.execute(
            "SELECT source_count, changed_count FROM ingestion_batches ORDER BY finished_at_utc"
        ).fetchall()[-1] == (2, 1)
        assert con.execute(
            "SELECT model_name, score FROM viewer_task_results ORDER BY model_name"
        ).fetchall() == [
            ("example/model_A", 0.42),
            ("example/model_B", 0.84),
        ]
    finally:
        con.close()


def test_load_results_merges_multiple_results_dirs_by_argument_order(tmp_path: Path) -> None:
    preferred_dir = tmp_path / "preferred"
    fallback_dir = tmp_path / "fallback"
    _write_minimal_task_result(
        preferred_dir / "model_A" / "hakari-bench__NanoJMTEB-v2" / "ja_cwir.json",
        model_id="example/model_A",
        task_name="ja_cwir",
        score=0.80,
    )
    _write_minimal_task_result(
        fallback_dir / "model_A" / "hakari-bench__NanoJMTEB-v2" / "ja_cwir.json",
        model_id="example/model_A",
        task_name="ja_cwir",
        score=0.20,
    )
    _write_minimal_task_result(
        fallback_dir / "model_B" / "hakari-bench__NanoJMTEB-v2" / "ja_cwir.json",
        model_id="example/model_B",
        task_name="ja_cwir",
        score=0.60,
    )

    rows, runs, metric_rows, diagnostic_rows, dataset_metadata_rows, ranking_rows = report.load_results(
        [preferred_dir, fallback_dir]
    )

    assert ranking_rows == []
    assert len(diagnostic_rows) == 2
    assert len(dataset_metadata_rows) == 1
    assert [(row.model_dir, row.score) for row in rows] == [("model_A", 0.80), ("model_B", 0.60)]
    assert rows[0].result_path == str(preferred_dir / "model_A" / "hakari-bench__NanoJMTEB-v2" / "ja_cwir.json")
    assert [(row.model_dir, row.metric_value) for row in metric_rows] == [("model_A", 0.80), ("model_B", 0.60)]
    assert [(run["model_dir"], run["aggregate_metric_mean"]) for run in runs] == [("model_A", 0.80), ("model_B", 0.60)]


def test_load_results_reversing_multiple_results_dirs_changes_duplicate_winner(tmp_path: Path) -> None:
    first_dir = tmp_path / "first"
    second_dir = tmp_path / "second"
    _write_minimal_task_result(
        first_dir / "model_A" / "hakari-bench__NanoJMTEB-v2" / "ja_cwir.json",
        model_id="example/model_A",
        task_name="ja_cwir",
        score=0.80,
    )
    _write_minimal_task_result(
        second_dir / "model_A" / "hakari-bench__NanoJMTEB-v2" / "ja_cwir.json",
        model_id="example/model_A",
        task_name="ja_cwir",
        score=0.20,
    )

    rows, *_ = report.load_results([second_dir, first_dir])

    assert [(row.model_dir, row.score) for row in rows] == [("model_A", 0.20)]
    assert rows[0].result_path == str(second_dir / "model_A" / "hakari-bench__NanoJMTEB-v2" / "ja_cwir.json")


def test_load_results_can_let_later_results_dirs_overwrite_duplicate_tasks(tmp_path: Path) -> None:
    base_dir = tmp_path / "base"
    override_dir = tmp_path / "override"
    _write_minimal_task_result(
        base_dir / "model_A" / "hakari-bench__NanoJMTEB-v2" / "ja_cwir.json",
        model_id="example/model_A",
        task_name="ja_cwir",
        score=0.80,
    )
    _write_minimal_task_result(
        override_dir / "model_A" / "hakari-bench__NanoJMTEB-v2" / "ja_cwir.json",
        model_id="example/model_A",
        task_name="ja_cwir",
        score=0.20,
    )

    rows, runs, metric_rows, diagnostic_rows, *_ = report.load_results(
        [base_dir, override_dir],
        duplicate_result_policy="last-wins",
    )

    assert [(row.model_dir, row.score) for row in rows] == [("model_A", 0.20)]
    assert rows[0].result_path == str(override_dir / "model_A" / "hakari-bench__NanoJMTEB-v2" / "ja_cwir.json")
    assert [(row.model_dir, row.metric_value) for row in metric_rows] == [("model_A", 0.20)]
    assert [(row.model_dir, row.base_score) for row in diagnostic_rows] == [("model_A", 0.20)]
    assert [(run["model_dir"], run["aggregate_metric_mean"]) for run in runs] == [("model_A", 0.20)]


def test_main_can_overwrite_duplicate_results_from_later_results_dirs(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    base_dir = tmp_path / "base"
    override_dir = tmp_path / "override"
    _write_minimal_task_result(
        base_dir / "model_A" / "hakari-bench__NanoJMTEB-v2" / "ja_cwir.json",
        model_id="example/model_A",
        task_name="ja_cwir",
        score=0.80,
    )
    _write_minimal_task_result(
        override_dir / "model_A" / "hakari-bench__NanoJMTEB-v2" / "ja_cwir.json",
        model_id="example/model_A",
        task_name="ja_cwir",
        score=0.20,
    )
    db_path = tmp_path / "hakari_bench.duckdb"
    monkeypatch.setattr(
        sys,
        "argv",
        [
            "build_results_database_and_report.py",
            "--results-dir",
            str(base_dir),
            "--results-dir",
            str(override_dir),
            "--overwrite-result-duplicates",
            "--duckdb-path",
            str(db_path),
        ],
    )

    report.main()

    con = duckdb.connect(str(db_path), read_only=True)
    try:
        assert con.execute("SELECT model_name, score, result_path FROM task_results").fetchall() == [
            (
                "example/model_A",
                0.20,
                str(override_dir / "model_A" / "hakari-bench__NanoJMTEB-v2" / "ja_cwir.json"),
            )
        ]
        assert con.execute("SELECT source_result_count FROM meta_database").fetchone() == (1,)
    finally:
        con.close()


def test_load_results_deduplicates_multiple_results_dirs_by_model_name_not_model_dir(tmp_path: Path) -> None:
    preferred_dir = tmp_path / "preferred"
    fallback_dir = tmp_path / "fallback"
    _write_minimal_task_result(
        preferred_dir / "foobar_exp128__foobar__final" / "hakari-bench__NanoJMTEB-v2" / "ja_cwir.json",
        model_id="foobar_exp128",
        task_name="ja_cwir",
        score=0.80,
    )
    _write_minimal_task_result(
        fallback_dir / "tmp__other_training_path" / "hakari-bench__NanoJMTEB-v2" / "ja_cwir.json",
        model_id="foobar_exp128",
        task_name="ja_cwir",
        score=0.20,
    )
    _write_minimal_task_result(
        fallback_dir / "tmp__other_training_path" / "hakari-bench__NanoJMTEB-v2" / "ja_nfcorpus.json",
        model_id="foobar_exp128",
        task_name="ja_nfcorpus",
        score=0.60,
    )

    rows, runs, metric_rows, diagnostic_rows, *_ = report.load_results([preferred_dir, fallback_dir])

    assert [(row.task_name, row.model_dir, row.model_name, row.score) for row in rows] == [
        ("ja_cwir", "foobar_exp128__foobar__final", "foobar_exp128", 0.80),
        ("ja_nfcorpus", "tmp__other_training_path", "foobar_exp128", 0.60),
    ]
    assert [(row.task_name, row.model_name, row.metric_value) for row in metric_rows] == [
        ("ja_cwir", "foobar_exp128", 0.80),
        ("ja_nfcorpus", "foobar_exp128", 0.60),
    ]
    assert [(row.task_name, row.model_name, row.base_score) for row in diagnostic_rows] == [
        ("ja_cwir", "foobar_exp128", 0.80),
        ("ja_nfcorpus", "foobar_exp128", 0.60),
    ]
    assert [(run["model_name"], run["split_count"], run["aggregate_metric_mean"]) for run in runs] == [
        ("foobar_exp128", 2, pytest.approx(0.70)),
    ]


def test_load_results_can_filter_model_names(tmp_path: Path) -> None:
    _write_minimal_task_result(
        tmp_path / "hotchpotch__bekko-embedding-pico-beta-unir-v7" / "hakari-bench__NanoJMTEB-v2" / "ja_cwir.json",
        model_id="hotchpotch/bekko-embedding-pico-beta-unir-v7",
        task_name="ja_cwir",
        score=0.80,
    )
    _write_minimal_task_result(
        tmp_path / "hotchpotch__bekko-embedding-pico-beta-unir-v9-GOR" / "hakari-bench__NanoJMTEB-v2" / "ja_cwir.json",
        model_id="hotchpotch/bekko-embedding-pico-beta-unir-v9-GOR",
        task_name="ja_cwir",
        score=0.70,
    )
    _write_minimal_task_result(
        tmp_path / "example__other-model" / "hakari-bench__NanoJMTEB-v2" / "ja_cwir.json",
        model_id="example/other-model",
        task_name="ja_cwir",
        score=0.60,
    )

    rows, runs, *_ = report.load_results(
        tmp_path,
        exclude_model_names={"hotchpotch/bekko-embedding-pico-beta-unir-v9-GOR"},
    )

    assert [row.model_name for row in rows] == [
        "example/other-model",
        "hotchpotch/bekko-embedding-pico-beta-unir-v7",
    ]
    assert [run["model_name"] for run in runs] == [
        "example/other-model",
        "hotchpotch/bekko-embedding-pico-beta-unir-v7",
    ]


def test_load_results_reads_task_json_as_source(tmp_path: Path) -> None:
    model_dir = tmp_path / "model"
    task_path = model_dir / "hakari-bench__NanoJMTEB-v2" / "ja_cwir.json"
    task_path.parent.mkdir(parents=True)
    ranking_path = task_path.parent / "rankings" / "ja_cwir.top100.json"
    ranking_path.parent.mkdir(parents=True)
    task_path.write_text(
        json.dumps(
            {
                "model": {
                    "id": "example/model",
                    "source": {
                        "type": "huggingface",
                        "name": "example/model",
                        "revision_requested": "main",
                        "revision": "model-sha",
                    },
                    "active_parameters": 3,
                    "total_parameters": 5,
                    "max_seq_length": 8192,
                    "dtype": "bf16",
                    "attn_implementation": "flash_attention_2",
                    "trust_remote_code": True,
                    "late_interaction": {"do_query_expansion": False},
                },
                "config": {
                    "query_prompt": "query: ",
                    "document_prompt": "passage: ",
                    "query_prompt_name": None,
                    "document_prompt_name": None,
                    "query_encode_task": None,
                    "document_encode_task": None,
                    "candidate_ranking": "reranking_hybrid",
                    "rerank_top_k": 100,
                },
                "environment": {
                    "package_versions": {
                        "torch": "2.9.1",
                        "transformers": "4.57.6",
                        "sentence-transformers": "5.4.1",
                    }
                },
                "experiment_manifest": {"fingerprint_sha256": "abc123"},
                "target": {
                    "dataset_name": "NanoJMTEB-v2",
                    "dataset_id": "hakari-bench/NanoJMTEB-v2",
                    "dataset_revision": {
                        "requested": None,
                        "resolved": "dataset-sha",
                        "source": "huggingface_hub",
                    },
                    "split_name": "ja_cwir",
                    "task_name": "ja_cwir",
                },
                "evaluation": {
                    "aggregate_metric": "ndcg@10",
                    "aggregate_metric_value": 0.42,
                    "rerank_aggregate_metric_value": 0.50,
                    "reranking_evaluations": [
                        {
                            "name": "reranking_hybrid_top_100",
                            "source": "dataset_candidate_subset",
                            "status": "available",
                            "rerank_top_n": 100,
                            "aggregate_metric": "ndcg@10",
                            "aggregate_metric_value": 0.50,
                            "best_score": 0.50,
                            "best_distance": "exact_maxsim",
                            "best_score_name": "late_interaction_exact_maxsim_reranking_hybrid_top100_rerank",
                            "candidate_coverage": {
                                "top_k": 100,
                                "query_count": 1,
                                "query_with_relevance_count": 1,
                                "covered_query_count": 1,
                                "query_coverage": 1.0,
                                "relevant_count": 1,
                                "covered_relevant_count": 1,
                                "relevant_coverage": 1.0,
                            },
                        }
                    ],
                    "late_interaction": {
                        "query_length": 48,
                        "document_length": 512,
                        "query_prefix": "[Q] ",
                        "document_prefix": "[D] ",
                        "attend_to_expansion_tokens": False,
                    },
                    "evaluated_at_utc": "2026-04-29T00:00:00+00:00",
                },
                "metrics": {"ja_cwir_ndcg@10": 0.42},
                "rerank_metrics": {
                    "ja_cwir_late_interaction_exact_maxsim_reranking_hybrid_top100_rerank_ndcg@10": 0.50,
                },
                "artifacts": {
                    "top_rankings": {
                        "schema_version": 1,
                        "top_k": 100,
                        "path": "rankings/ja_cwir.top100.json",
                    }
                },
            }
        ),
        encoding="utf-8",
    )
    ranking_path.write_text(
        json.dumps(
            {
                "schema_version": 1,
                "top_k": 100,
                "target": {
                    "dataset_name": "NanoJMTEB-v2",
                    "dataset_id": "hakari-bench/NanoJMTEB-v2",
                    "split_name": "ja_cwir",
                    "task_name": "ja_cwir",
                },
                "rankings": [
                    {
                        "name": "base",
                        "ranking_kind": "retrieval",
                        "embedding_variant_name": None,
                        "distance": "dot",
                        "score_name": "dot",
                        "query_id": "q1",
                        "corpus_ids": ["d1", "d2"],
                    }
                ],
            }
        ),
        encoding="utf-8",
    )

    default_rows, _, _, _, _, default_ranking_rows = report.load_results(tmp_path)
    rows, _, metric_rows, diagnostic_rows, dataset_metadata_rows, ranking_rows = report.load_results(
        tmp_path,
        include_retrieval_rankings=True,
    )

    assert len(default_rows) == 1
    assert default_ranking_rows == []
    assert len(rows) == 1
    assert rows[0].benchmark == "NanoJMTEB-v2"
    assert rows[0].dataset_id == "hakari-bench/NanoJMTEB-v2"
    assert rows[0].dataset_name == "NanoJMTEB-v2"
    assert rows[0].score == 0.42
    assert rows[0].dataset_revision == "dataset-sha"
    assert rows[0].model_revision == "model-sha"
    assert rows[0].model_revision_requested == "main"
    assert rows[0].experiment_fingerprint == "abc123"
    assert rows[0].active_parameters == 3
    assert rows[0].total_parameters == 5
    assert rows[0].query_prompt == "query: "
    assert rows[0].document_prompt == "passage: "
    assert rows[0].trust_remote_code is True
    assert rows[0].late_interaction_query_length == 48
    assert rows[0].late_interaction_document_length == 512
    assert rows[0].late_interaction_query_prefix == "[Q] "
    assert rows[0].late_interaction_document_prefix == "[D] "
    assert rows[0].late_interaction_query_expansion is False
    assert rows[0].late_interaction_attend_to_expansion_tokens is False
    assert len(metric_rows) == 2
    assert len(diagnostic_rows) == 1
    assert diagnostic_rows[0].base_score == 0.42
    assert diagnostic_rows[0].rerank_score == 0.50
    assert diagnostic_rows[0].rerank_status == "available"
    assert diagnostic_rows[0].rerank_top_k == 100
    assert diagnostic_rows[0].candidate_ranking == "reranking_hybrid"
    assert len(dataset_metadata_rows) == 1
    assert dataset_metadata_rows[0].language == "ja"
    assert dataset_metadata_rows[0].languages == ["ja"]
    assert dataset_metadata_rows[0].category == "natural_language"
    assert dataset_metadata_rows[0].reference_count is not None
    assert dataset_metadata_rows[0].query_count == 200
    assert [row.rank for row in ranking_rows] == [1, 2]
    assert ranking_rows[0].ranking_path == str(ranking_path)
    assert ranking_rows[0].query_id == "q1"
    assert ranking_rows[0].corpus_id == "d1"


def test_load_results_backfills_missing_parameters_from_model_card_yaml(tmp_path: Path) -> None:
    task_path = tmp_path / "jinaai__jina-embeddings-v3" / "hakari-bench__NanoBEIR-en" / "arguana.json"
    task_path.parent.mkdir(parents=True)
    model_cards_path = tmp_path / "model_cards.yaml"
    model_cards_path.write_text(
        """
models:
  - id: jinaai/jina-embeddings-v3
    source:
      type: huggingface
      name: jinaai/jina-embeddings-v3
      revision: ab036b023d30
    parameters:
      total: 572310396
      input_embedding: 256002048
      active: 316308348
""".strip(),
        encoding="utf-8",
    )
    task_path.write_text(
        json.dumps(
            {
                "model": {
                    "id": "jinaai/jina-embeddings-v3",
                    "source": {
                        "type": "huggingface",
                        "name": "jinaai/jina-embeddings-v3",
                        "revision": "ab036b023d30",
                    },
                    "total_parameters": 572310396,
                    "embedding_parameters": None,
                    "active_parameters": None,
                },
                "environment": {"package_versions": {}},
                "target": {
                    "dataset_name": "NanoBEIR-en",
                    "dataset_id": "hakari-bench/NanoBEIR-en",
                    "split_name": "arguana",
                    "task_name": "arguana",
                },
                "evaluation": {"aggregate_metric": "ndcg@10", "aggregate_metric_value": 0.42},
            }
        ),
        encoding="utf-8",
    )

    rows, runs, _, _, _, _ = report.load_results(tmp_path, model_cards_path=model_cards_path)

    assert rows[0].active_parameters == 316308348
    assert runs[0]["active_parameters"] == 316308348


def test_load_model_cards_reads_one_file_per_model_from_directory(tmp_path: Path) -> None:
    model_cards_dir = tmp_path / "model_cards"
    model_cards_dir.mkdir()
    (model_cards_dir / "BAAI__bge-m3.yaml").write_text(
        """
id: BAAI/bge-m3
source:
  type: huggingface
  name: BAAI/bge-m3
parameters:
  total: 568000000
  input_embedding: 250000000
  active: 318000000
""".strip(),
        encoding="utf-8",
    )
    (model_cards_dir / "jinaai__jina-embeddings-v3.yaml").write_text(
        """
id: jinaai/jina-embeddings-v3
parameters:
  total: 572310396
  input_embedding: 256002048
  active: 316308348
""".strip(),
        encoding="utf-8",
    )

    model_cards = report.load_model_cards(model_cards_dir)

    assert sorted(model_cards) == ["BAAI/bge-m3", "jinaai/jina-embeddings-v3"]
    assert model_cards["BAAI/bge-m3"]["parameters"]["active"] == 318000000


def test_model_cards_directory_state_changes_when_card_is_added(tmp_path: Path) -> None:
    model_cards_dir = tmp_path / "model_cards"
    model_cards_dir.mkdir()
    (model_cards_dir / "first.yaml").write_text(
        """
id: example/first
parameters:
  total: 10
  active: 4
""".strip(),
        encoding="utf-8",
    )
    initial_state = report._model_cards_state(model_cards_dir)
    (model_cards_dir / "second.yaml").write_text(
        """
id: example/second
parameters:
  total: 20
  active: 8
""".strip(),
        encoding="utf-8",
    )

    assert report._model_cards_state(model_cards_dir) != initial_state


def test_load_results_incremental_reparses_when_model_card_yaml_changes(tmp_path: Path) -> None:
    results_dir = tmp_path / "results"
    task_path = results_dir / "model" / "hakari-bench__NanoJMTEB-v2" / "ja_cwir.json"
    task_path.parent.mkdir(parents=True)
    model_cards_path = tmp_path / "model_cards.yaml"
    task_path.write_text(
        json.dumps(
            {
                "model": {
                    "id": "example/model",
                    "total_parameters": 10,
                    "active_parameters": None,
                },
                "target": {
                    "dataset_name": "NanoJMTEB-v2",
                    "dataset_id": "hakari-bench/NanoJMTEB-v2",
                    "split_name": "ja_cwir",
                    "task_name": "ja_cwir",
                },
                "evaluation": {"aggregate_metric": "ndcg@10", "aggregate_metric_value": 0.42},
            }
        ),
        encoding="utf-8",
    )
    model_cards_path.write_text(
        """
models:
  - id: example/model
    parameters:
      total: 10
      input_embedding: 6
      active: 4
""".strip(),
        encoding="utf-8",
    )
    rows, runs, metric_rows, diagnostic_rows, dataset_metadata_rows, ranking_rows = report.load_results(
        results_dir,
        model_cards_path=model_cards_path,
    )
    db_path = tmp_path / "hakari_bench.duckdb"
    report.write_duckdb(
        db_path,
        runs=runs,
        rows=rows,
        metric_rows=metric_rows,
        diagnostic_rows=diagnostic_rows,
        dataset_metadata_rows=dataset_metadata_rows,
        ranking_rows=ranking_rows,
        standings={},
        borda_rows=[],
        model_cards_path=model_cards_path,
    )
    model_cards_path.write_text(
        """
models:
  - id: example/model
    parameters:
      total: 10
      input_embedding: 5
      active: 5
""".strip(),
        encoding="utf-8",
    )

    updated_rows, updated_runs, _, _, _, _ = report.load_results(
        results_dir,
        incremental_db_path=db_path,
        model_cards_path=model_cards_path,
    )

    assert updated_rows[0].active_parameters == 5
    assert updated_runs[0]["active_parameters"] == 5


def test_model_card_metadata_fills_missing_parameter_fields_without_overwriting() -> None:
    model = {
        "id": "example/model",
        "total_parameters": 10,
        "active_parameters": 4,
        "embedding_parameters": None,
        "transformer_parameters": None,
    }
    model_cards = {
        "example/model": {
            "parameters": {
                "total": 10,
                "input_embedding": 6,
                "active": 4,
            },
        },
    }

    updated = report._with_model_card_metadata(model, model_cards=model_cards)

    assert updated["active_parameters"] == 4
    assert updated["embedding_parameters"] == 6
    assert updated["transformer_parameters"] == 4


def test_model_card_metadata_backfills_zero_total_parameters() -> None:
    model = {
        "id": "bm25",
        "total_parameters": None,
        "active_parameters": None,
        "embedding_parameters": None,
        "transformer_parameters": None,
    }
    model_cards = {
        "bm25": {
            "parameters": {
                "total": 0,
                "input_embedding": 0,
                "active": 0,
            },
        },
    }

    updated = report._with_model_card_metadata(model, model_cards=model_cards)

    assert updated["total_parameters"] == 0
    assert updated["active_parameters"] == 0
    assert updated["embedding_parameters"] == 0
    assert updated["transformer_parameters"] == 0


def test_model_card_metadata_uses_bm25_card_for_bm25_variants() -> None:
    model = {
        "id": "bm25/dataset-bm25",
        "method": "bm25",
        "source": {"type": "bm25", "name": "bm25/dataset-bm25"},
        "total_parameters": None,
        "active_parameters": None,
    }
    model_cards = {
        "bm25": {
            "parameters": {
                "total": 0,
                "input_embedding": 0,
                "active": 0,
            },
        },
    }

    updated = report._with_model_card_metadata(model, model_cards=model_cards)

    assert updated["total_parameters"] == 0
    assert updated["active_parameters"] == 0
    assert updated["embedding_parameters"] == 0
    assert updated["transformer_parameters"] == 0


def _write_minimal_task_result(path: Path, *, model_id: str, task_name: str, score: float) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(
            {
                "model": {"id": model_id},
                "target": {
                    "dataset_name": "NanoJMTEB-v2",
                    "dataset_id": "hakari-bench/NanoJMTEB-v2",
                    "split_name": task_name,
                    "task_name": task_name,
                },
                "evaluation": {"aggregate_metric": "ndcg@10", "aggregate_metric_value": score},
                "metrics": {f"{task_name}_ndcg@10": score},
            }
        ),
        encoding="utf-8",
    )


def test_task_result_row_schema_rejects_unknown_fields() -> None:
    with pytest.raises(ValidationError, match="unexpected"):
        TaskResultRow.model_validate(
            {
                "model_dir": "model",
                "model_name": "example/model",
                "benchmark": "NanoJMTEB-v2",
                "dataset_id": "hakari-bench/NanoJMTEB-v2",
                "dataset_name": "NanoJMTEB-v2",
                "task_name": "ja_cwir",
                "task_key": "NanoJMTEB-v2::hakari-bench/NanoJMTEB-v2::ja_cwir",
                "score": 0.42,
                "result_path": "result.json",
                "unexpected": True,
            }
        )


def test_load_results_allows_missing_model_revision_for_existing_results(tmp_path: Path) -> None:
    model_dir = tmp_path / "model"
    task_path = model_dir / "hakari-bench__NanoJMTEB-v2" / "ja_cwir.json"
    task_path.parent.mkdir(parents=True)
    task_path.write_text(
        json.dumps(
            {
                "model": {"id": "example/model"},
                "target": {
                    "dataset_name": "NanoJMTEB-v2",
                    "dataset_id": "hakari-bench/NanoJMTEB-v2",
                    "split_name": "ja_cwir",
                    "task_name": "ja_cwir",
                },
                "evaluation": {"aggregate_metric": "ndcg@10", "aggregate_metric_value": 0.42},
                "metrics": {"ja_cwir_ndcg@10": 0.42},
            }
        ),
        encoding="utf-8",
    )

    rows, *_ = report.load_results(tmp_path)

    assert len(rows) == 1
    assert rows[0].model_revision is None
    assert rows[0].model_revision_requested is None


def test_metric_long_row_schema_exports_duckdb_values() -> None:
    row = MetricLongRow(
        model_dir="model",
        model_name="example/model",
        benchmark="NanoJMTEB-v2",
        dataset_id="hakari-bench/NanoJMTEB-v2",
        task_name="ja_cwir",
        metric_name="ja_cwir_ndcg@10",
        metric_value=0.42,
        result_path="result.json",
    )

    assert row.duckdb_values() == (
        "model",
        "example/model",
        "NanoJMTEB-v2",
        "hakari-bench/NanoJMTEB-v2",
        "ja_cwir",
        "ja_cwir_ndcg@10",
        0.42,
        "result.json",
        "all",
        None,
    )


def test_retrieval_ranking_row_schema_exports_duckdb_values() -> None:
    row = RetrievalRankingRow(
        model_dir="model",
        model_name="example/model",
        benchmark="NanoJMTEB-v2",
        dataset_id="hakari-bench/NanoJMTEB-v2",
        dataset_revision="dataset-sha",
        dataset_name="NanoJMTEB-v2",
        split_name="ja_cwir",
        task_name="ja_cwir",
        task_key="NanoJMTEB-v2::hakari-bench/NanoJMTEB-v2::ja_cwir",
        result_path="result.json",
        ranking_path="rankings/ja_cwir.top100.json",
        ranking_name="base",
        ranking_kind="retrieval",
        embedding_variant_name=None,
        distance="dot",
        score_name="dot",
        query_id="q1",
        rank=1,
        corpus_id="d1",
    )

    assert row.duckdb_values() == (
        "model",
        "example/model",
        "NanoJMTEB-v2",
        "hakari-bench/NanoJMTEB-v2",
        "dataset-sha",
        "NanoJMTEB-v2",
        "ja_cwir",
        "ja_cwir",
        "NanoJMTEB-v2::hakari-bench/NanoJMTEB-v2::ja_cwir",
        "result.json",
        "rankings/ja_cwir.top100.json",
        "base",
        "retrieval",
        None,
        "dot",
        "dot",
        "q1",
        1,
        "d1",
    )


def test_load_results_extracts_task_diagnostics(tmp_path: Path) -> None:
    task_dir = tmp_path / "model" / "hakari-bench__NanoJMTEB-v2"
    task_dir.mkdir(parents=True)
    (task_dir / "ja_cwir.json").write_text(
        json.dumps(
            {
                "model": {"id": "example/model"},
                "environment": {"package_versions": {}},
                "target": {
                    "dataset_name": "NanoJMTEB-v2",
                    "dataset_id": "hakari-bench/NanoJMTEB-v2",
                    "split_name": "ja_cwir",
                    "task_name": "ja_cwir",
                },
                "config": {
                    "candidate_ranking": "bm25",
                    "rerank_top_k": 100,
                    "bm25": {"source": "dataset_candidate_subset"},
                },
                "evaluation": {
                    "aggregate_metric": "ndcg@10",
                    "aggregate_metric_value": 0.42,
                    "rerank_aggregate_metric_value": 0.50,
                    "dataset_load_seconds": 0.25,
                    "wall_seconds": 2.0,
                    "duration_seconds_including_dataset_load": 2.25,
                    "timing": {
                        "query_embedding_seconds": 0.5,
                        "corpus_embedding_seconds": 1.0,
                        "score_and_topk_seconds": 0.3,
                        "metric_compute_seconds": 0.2,
                        "pure_compute_seconds": 2.0,
                    },
                    "reranking_evaluations": [
                        {
                            "source": "dataset_candidate_subset",
                            "status": "available",
                            "candidate_coverage": {
                                "query_coverage": 0.75,
                                "relevant_coverage": 0.60,
                                "covered_query_count": 3,
                                "query_with_relevance_count": 4,
                                "covered_relevant_count": 6,
                                "relevant_count": 10,
                            },
                        }
                    ],
                },
                "metrics": {"ja_cwir_ndcg@10": 0.42},
            }
        ),
        encoding="utf-8",
    )

    _, _, _, diagnostic_rows, _, _ = report.load_results(tmp_path)

    assert len(diagnostic_rows) == 1
    row = diagnostic_rows[0]
    assert row.rerank_lift == pytest.approx(0.08)
    assert row.candidate_ranking == "bm25"
    assert row.bm25_source == "dataset_candidate_subset"
    assert row.query_coverage == 0.75
    assert row.relevant_coverage == 0.60
    assert row.score_and_topk_seconds == 0.3


def test_load_results_builds_runs_from_task_json(tmp_path: Path) -> None:
    task_dir = tmp_path / "local__model_A" / "hakari-bench__NanoJMTEB-v2"
    task_dir.mkdir(parents=True)
    (task_dir / "ja_cwir.json").write_text(
        json.dumps(
            {
                "generated_at_utc": "2026-05-04T00:00:00+00:00",
                "model": {
                    "id": "local/model_A",
                    "active_parameters": 3,
                    "total_parameters": 5,
                    "max_seq_length": 8192,
                    "dtype": "bf16",
                    "attn_implementation": "flash_attention_2",
                },
                "environment": {
                    "package_versions": {
                        "torch": "2.9.1",
                        "transformers": "4.57.6",
                        "sentence-transformers": "5.4.1",
                    }
                },
                "target": {
                    "dataset_name": "NanoJMTEB-v2",
                    "dataset_id": "hakari-bench/NanoJMTEB-v2",
                    "split_name": "ja_cwir",
                    "task_name": "ja_cwir",
                },
                "evaluation": {
                    "aggregate_metric": "ndcg@10",
                    "aggregate_metric_value": 0.42,
                    "started_at_utc": "2026-05-04T00:00:01+00:00",
                    "finished_at_utc": "2026-05-04T00:00:03+00:00",
                },
                "metrics": {"ja_cwir_ndcg@10": 0.42},
            }
        ),
        encoding="utf-8",
    )

    rows, runs, _, _, _, _ = report.load_results(tmp_path)

    assert len(rows) == 1
    assert runs == [
        {
            "model_dir": "local__model_A",
            "model_name": "local/model_A",
            "generated_at_utc": "2026-05-04T00:00:00+00:00",
            "started_at_utc": "2026-05-04T00:00:01+00:00",
            "finished_at_utc": "2026-05-04T00:00:03+00:00",
            "target_count": 1,
            "split_count": 1,
            "cache_hit_count": None,
            "evaluated_count": None,
            "aggregate_metric_mean": 0.42,
            "active_parameters": 3,
            "total_parameters": 5,
            "max_seq_length": 8192,
            "dtype": "bf16",
            "attn_implementation": "flash_attention_2",
            "torch_version": "2.9.1",
            "transformers_version": "4.57.6",
            "sentence_transformers_version": "5.4.1",
        }
    ]


def test_render_html_includes_total_parameters_column() -> None:
    html = report.render_html(data_json=json.dumps({"views": {}, "summary": {"skipped": []}}))

    assert "Total Params" in html


def test_load_results_adds_embedding_variant_rows(tmp_path: Path) -> None:
    model_dir = tmp_path / "model"
    task_path = model_dir / "hakari-bench__NanoJMTEB-v2" / "ja_cwir.json"
    task_path.parent.mkdir(parents=True)
    task_path.write_text(
        json.dumps(
            {
                "model": {"id": "example/model"},
                "environment": {"package_versions": {}},
                "target": {
                    "dataset_name": "NanoJMTEB-v2",
                    "dataset_id": "hakari-bench/NanoJMTEB-v2",
                    "split_name": "ja_cwir",
                    "task_name": "ja_cwir",
                },
                "evaluation": {"aggregate_metric": "ndcg@10", "aggregate_metric_value": 0.42},
                "embedding_evaluations": [
                    {
                        "name": "base",
                        "aggregate_metric": "ndcg@10",
                        "aggregate_metric_value": 0.42,
                        "embedding_dimensions": {"dim": 768},
                    },
                    {
                        "name": "truncate_dim_512_quantize_uint8_docs",
                        "aggregate_metric": "ndcg@10",
                        "aggregate_metric_value": 0.40,
                        "embedding_dimensions": {"dim": 512},
                        "embedding_metadata": {
                            "corpus": {
                                "quantization": {
                                    "precision": "uint8",
                                    "original_dim": 512,
                                    "stored_dim": 512,
                                }
                            }
                        },
                    },
                ],
                "metrics": {"ja_cwir_ndcg@10": 0.42},
            }
        ),
        encoding="utf-8",
    )
    rows, _, _, _, _, _ = report.load_results(tmp_path)

    assert [(row.embedding_variant_name, row.score, row.embedding_dim, row.quantization) for row in rows] == [
        (None, 0.42, 768, None),
        ("truncate_dim_512_quantize_uint8_docs", 0.40, 512, "uint8"),
    ]


def test_write_duckdb_persists_dataset_revision(tmp_path: Path) -> None:
    row = report.TaskResult(
        model_dir="model",
        model_name="example/model",
        benchmark="NanoJMTEB-v2",
        dataset_id="hakari-bench/NanoJMTEB-v2",
        dataset_revision="dataset-sha",
        dataset_revision_requested="main",
        model_revision="model-sha",
        model_revision_requested="main",
        dataset_name="NanoJMTEB-v2",
        split_name="ja_cwir",
        task_name="ja_cwir",
        task_key="NanoJMTEB-v2::hakari-bench/NanoJMTEB-v2::ja_cwir",
        score=0.42,
        aggregate_metric="ndcg@10",
        result_path="result.json",
        active_parameters=3,
        total_parameters=5,
        max_seq_length=8192,
        dtype="bf16",
        attn_implementation="flash_attention_2",
        query_prompt="query: ",
        document_prompt="passage: ",
        query_prompt_name=None,
        document_prompt_name=None,
        query_encode_task=None,
        document_encode_task=None,
        trust_remote_code=True,
        torch_version="2.9.1",
        transformers_version="4.57.6",
        sentence_transformers_version="5.4.1",
        started_at_utc=None,
        finished_at_utc=None,
        evaluated_at_utc=None,
        duration_seconds_including_dataset_load=None,
        wall_seconds=None,
    )
    standings, borda_rows = report.compute_standings([row])
    db_path = tmp_path / "results.duckdb"

    report.write_duckdb(
        db_path,
        runs=[
            {
                "model_dir": "model",
                "model_name": "example/model",
            }
        ],
        rows=[row],
        metric_rows=[
            {
                "model_dir": "model",
                "model_name": "example/model",
                "benchmark": "NanoJMTEB-v2",
                "dataset_id": "hakari-bench/NanoJMTEB-v2",
                "task_name": "ja_cwir",
                "metric_name": "ja_cwir_ndcg@10",
                "metric_value": 0.42,
                "result_path": "result.json",
            },
            {
                "model_dir": "model",
                "model_name": "example/model",
                "benchmark": "NanoJMTEB-v2",
                "dataset_id": "hakari-bench/NanoJMTEB-v2",
                "task_name": "ja_cwir",
                "metric_name": "ja_cwir_cosine_reranking_hybrid_top100_rerank_ndcg@10",
                "metric_value": 0.45,
                "result_path": "result.json",
                "score_target": "reranking_without_safeguard",
            },
        ],
        ranking_rows=[
            {
                "model_dir": "model",
                "model_name": "example/model",
                "benchmark": "NanoJMTEB-v2",
                "dataset_id": "hakari-bench/NanoJMTEB-v2",
                "dataset_revision": "dataset-sha",
                "dataset_name": "NanoJMTEB-v2",
                "split_name": "ja_cwir",
                "task_name": "ja_cwir",
                "task_key": "NanoJMTEB-v2::hakari-bench/NanoJMTEB-v2::ja_cwir",
                "result_path": "result.json",
                "ranking_path": "rankings/ja_cwir.top100.json",
                "ranking_name": "base",
                "ranking_kind": "retrieval",
                "embedding_variant_name": None,
                "distance": "dot",
                "score_name": "dot",
                "query_id": "q1",
                "rank": 1,
                "corpus_id": "d1",
            }
        ],
        standings=standings,
        borda_rows=borda_rows,
    )

    con = duckdb.connect(str(db_path))
    try:
        run_columns = [row[1] for row in con.execute("PRAGMA table_info('runs')").fetchall()]
        assert run_columns == [
            "model_dir",
            "model_name",
            "generated_at_utc",
            "started_at_utc",
            "finished_at_utc",
            "target_count",
            "split_count",
            "cache_hit_count",
            "evaluated_count",
            "aggregate_metric_mean",
            "active_parameters",
            "total_parameters",
            "max_seq_length",
            "dtype",
            "attn_implementation",
            "torch_version",
            "transformers_version",
            "sentence_transformers_version",
        ]
        assert con.execute(
            "SELECT dataset_revision, dataset_revision_requested, model_revision, model_revision_requested FROM task_results"
        ).fetchone() == ("dataset-sha", "main", "model-sha", "main")
        assert con.execute(
            """
            SELECT query_prompt, document_prompt, query_prompt_name, document_prompt_name,
                   query_encode_task, document_encode_task, trust_remote_code
            FROM task_results
            """
        ).fetchone() == ("query: ", "passage: ", None, None, None, None, True)
        assert con.execute(
            """
            SELECT model_name, benchmark, task_key, score, language, languages
            FROM viewer_task_results
            """
        ).fetchone() == ("example/model", "NanoJMTEB-v2", "NanoJMTEB-v2::hakari-bench/NanoJMTEB-v2::ja_cwir", 0.42, None, None)
        assert con.execute("SELECT base_score FROM task_diagnostics").fetchone() is None
        assert con.execute("SELECT query_id, rank, corpus_id FROM retrieval_rankings").fetchone() == ("q1", 1, "d1")
    finally:
        con.close()


def test_write_duckdb_materializes_task_score_targets(tmp_path: Path) -> None:
    row = report.TaskResult(
        model_dir="model",
        model_name="example/model",
        benchmark="NanoJMTEB-v2",
        dataset_id="hakari-bench/NanoJMTEB-v2",
        dataset_name="NanoJMTEB-v2",
        split_name="ja_cwir",
        task_name="ja_cwir",
        task_key="NanoJMTEB-v2::hakari-bench/NanoJMTEB-v2::ja_cwir",
        score=0.42,
        aggregate_metric="ndcg@10",
        result_path="result.json",
    )
    diagnostic_row = TaskDiagnosticRow(
        model_dir="model",
        model_name="example/model",
        benchmark="NanoJMTEB-v2",
        dataset_id="hakari-bench/NanoJMTEB-v2",
        task_name="ja_cwir",
        task_key="NanoJMTEB-v2::hakari-bench/NanoJMTEB-v2::ja_cwir",
        result_path="result.json",
        base_score=0.42,
        rerank_score=0.50,
        rerank_lift=0.08,
        rerank_status="available",
        rerank_top_k=101,
        candidate_source="dataset_candidate_subset",
        candidate_ranking="reranking_hybrid",
    )
    variant_row = row.model_copy(
        update={
            "score": 0.40,
            "embedding_variant_name": "truncate_dim_512_quantize_uint8_docs",
            "embedding_dim": 512,
            "quantization": "uint8",
        }
    )
    standings, borda_rows = report.compute_standings([row])
    db_path = tmp_path / "results.duckdb"

    report.write_duckdb(
        db_path,
        runs=[{"model_dir": "model", "model_name": "example/model"}],
        rows=[row, variant_row],
        metric_rows=[
            {
                "model_dir": "model",
                "model_name": "example/model",
                "benchmark": "NanoJMTEB-v2",
                "dataset_id": "hakari-bench/NanoJMTEB-v2",
                "task_name": "ja_cwir",
                "metric_name": "ja_cwir_ndcg@10",
                "metric_value": 0.42,
                "result_path": "result.json",
            },
            {
                "model_dir": "model",
                "model_name": "example/model",
                "benchmark": "NanoJMTEB-v2",
                "dataset_id": "hakari-bench/NanoJMTEB-v2",
                "task_name": "ja_cwir",
                "metric_name": "ja_cwir_cosine_reranking_hybrid_top100_rerank_ndcg@10",
                "metric_value": 0.45,
                "result_path": "result.json",
                "score_target": "reranking_without_safeguard",
            },
            {
                "model_dir": "model",
                "model_name": "example/model",
                "benchmark": "NanoJMTEB-v2",
                "dataset_id": "hakari-bench/NanoJMTEB-v2",
                "task_name": "ja_cwir",
                "metric_name": "ja_cwir_truncate_dim_512_quantize_uint8_docs_cosine_reranking_hybrid_top100_rerank_ndcg@10",
                "metric_value": 0.47,
                "result_path": "result.json",
                "score_target": "reranking",
                "embedding_variant_name": "truncate_dim_512_quantize_uint8_docs",
            },
            {
                "model_dir": "model",
                "model_name": "example/model",
                "benchmark": "NanoJMTEB-v2",
                "dataset_id": "hakari-bench/NanoJMTEB-v2",
                "task_name": "ja_cwir",
                "metric_name": "ja_cwir_truncate_dim_512_quantize_uint8_docs_cosine_reranking_hybrid_top100_rerank_ndcg@10",
                "metric_value": 0.44,
                "result_path": "result.json",
                "score_target": "reranking_without_safeguard",
                "embedding_variant_name": "truncate_dim_512_quantize_uint8_docs",
            },
        ],
        diagnostic_rows=[diagnostic_row],
        standings=standings,
        borda_rows=borda_rows,
    )

    con = duckdb.connect(str(db_path))
    try:
        assert con.execute(
            """
                SELECT score_target, score, candidate_ranking, rerank_top_k, embedding_variant_name
                FROM fact_task_score
                ORDER BY score_target, embedding_variant_name IS NOT NULL, embedding_variant_name
            """
        ).fetchall() == [
            ("all", 0.42, None, None, None),
            ("all", 0.40, None, None, "truncate_dim_512_quantize_uint8_docs"),
            ("reranking", 0.50, "reranking_hybrid", 101, None),
            ("reranking", 0.47, "reranking_hybrid", 100, "truncate_dim_512_quantize_uint8_docs"),
            ("reranking_without_safeguard", 0.45, "reranking_hybrid", 100, None),
            ("reranking_without_safeguard", 0.44, "reranking_hybrid", 100, "truncate_dim_512_quantize_uint8_docs"),
        ]
        assert con.execute(
            """
            SELECT score_target, score, embedding_variant_name
            FROM viewer_task_results
            ORDER BY score_target, embedding_variant_name IS NOT NULL, embedding_variant_name
            """
        ).fetchall() == [
            ("all", 0.42, None),
            ("all", 0.40, "truncate_dim_512_quantize_uint8_docs"),
            ("reranking", 0.50, None),
            ("reranking", 0.47, "truncate_dim_512_quantize_uint8_docs"),
            ("reranking_without_safeguard", 0.45, None),
            ("reranking_without_safeguard", 0.44, "truncate_dim_512_quantize_uint8_docs"),
        ]
        assert (
            con.execute(
                """
                SELECT label
                FROM viewer_filter_values
                WHERE filter_name = 'target' AND value = 'reranking_without_safeguard'
                """
            ).fetchone()
            == ("Reranking without safeguard",)
        )
    finally:
        con.close()


def test_write_duckdb_materializes_canonical_dimensions(tmp_path: Path) -> None:
    base_row = report.TaskResult(
        model_dir="model",
        model_name="example/model",
        benchmark="NanoJMTEB-v2",
        dataset_id="hakari-bench/NanoJMTEB-v2",
        dataset_name="NanoJMTEB-v2",
        split_name="ja_cwir",
        task_name="ja_cwir",
        task_key="NanoJMTEB-v2::hakari-bench/NanoJMTEB-v2::ja_cwir",
        score=0.42,
        aggregate_metric="ndcg@10",
        result_path="result.json",
        active_parameters=3,
        total_parameters=5,
        max_seq_length=8192,
        dtype="bf16",
        embedding_dim=768,
    )
    variant_row = base_row.model_copy(
        update={
            "score": 0.40,
            "embedding_variant_name": "truncate_dim_512_quantize_uint8_docs",
            "embedding_dim": 512,
            "quantization": "uint8",
        }
    )
    metadata_row = DatasetMetadataRow(
        benchmark="NanoJMTEB-v2",
        dataset_id="hakari-bench/NanoJMTEB-v2",
        dataset_name="NanoJMTEB-v2",
        split_name="ja_cwir",
        task_name="ja_cwir",
        task_key="NanoJMTEB-v2::hakari-bench/NanoJMTEB-v2::ja_cwir",
        language="ja",
        languages=["ja"],
        category="natural_language",
        query_count=200,
        document_count=500,
    )
    standings, borda_rows = report.compute_standings([base_row])
    db_path = tmp_path / "results.duckdb"

    report.write_duckdb(
        db_path,
        runs=[{"model_dir": "model", "model_name": "example/model"}],
        rows=[base_row, variant_row],
        metric_rows=[
            {
                "model_dir": "model",
                "model_name": "example/model",
                "benchmark": "NanoJMTEB-v2",
                "dataset_id": "hakari-bench/NanoJMTEB-v2",
                "task_name": "ja_cwir",
                "metric_name": "ja_cwir_ndcg@10",
                "metric_value": 0.42,
                "result_path": "result.json",
            }
        ],
        dataset_metadata_rows=[metadata_row],
        standings=standings,
        borda_rows=borda_rows,
    )

    con = duckdb.connect(str(db_path))
    try:
        assert con.execute(
            "SELECT model_id, model_dir, model_name, active_parameters, total_parameters FROM dim_model"
        ).fetchall() == [(1, "model", "example/model", 3, 5)]
        assert con.execute(
            """
            SELECT task_id, benchmark, dataset_id, task_key, language, category, query_count, document_count
            FROM dim_task
            """
        ).fetchall() == [
            (
                1,
                "NanoJMTEB-v2",
                "hakari-bench/NanoJMTEB-v2",
                "NanoJMTEB-v2::hakari-bench/NanoJMTEB-v2::ja_cwir",
                "ja",
                "natural_language",
                200,
                500,
            )
        ]
        assert con.execute(
            """
            SELECT variant_id, variant_key, embedding_variant_name, embedding_dim, quantization, is_base
            FROM dim_variant
            ORDER BY variant_id
            """
        ).fetchall() == [
            (1, "base:768:none", None, 768, None, True),
            (
                2,
                "truncate_dim_512_quantize_uint8_docs:512:uint8",
                "truncate_dim_512_quantize_uint8_docs",
                512,
                "uint8",
                False,
            ),
        ]
    finally:
        con.close()


def test_write_duckdb_records_source_load_state_and_changed_count(tmp_path: Path) -> None:
    result_path = tmp_path / "model" / "hakari-bench__NanoJMTEB-v2" / "ja_cwir.json"
    result_path.parent.mkdir(parents=True)
    result_path.write_text('{"score": 0.42}', encoding="utf-8")
    row = report.TaskResult(
        model_dir="model",
        model_name="example/model",
        benchmark="NanoJMTEB-v2",
        dataset_id="hakari-bench/NanoJMTEB-v2",
        dataset_name="NanoJMTEB-v2",
        split_name="ja_cwir",
        task_name="ja_cwir",
        task_key="NanoJMTEB-v2::hakari-bench/NanoJMTEB-v2::ja_cwir",
        score=0.42,
        aggregate_metric="ndcg@10",
        result_path=str(result_path),
    )
    standings, borda_rows = report.compute_standings([row])
    db_path = tmp_path / "results.duckdb"

    def write_once() -> None:
        report.write_duckdb(
            db_path,
            runs=[{"model_dir": "model", "model_name": "example/model"}],
            rows=[row],
            metric_rows=[
                {
                    "model_dir": "model",
                    "model_name": "example/model",
                    "benchmark": "NanoJMTEB-v2",
                    "dataset_id": "hakari-bench/NanoJMTEB-v2",
                    "task_name": "ja_cwir",
                    "metric_name": "ja_cwir_ndcg@10",
                    "metric_value": 0.42,
                    "result_path": str(result_path),
                }
            ],
            standings=standings,
            borda_rows=borda_rows,
            batch_id="test-batch",
            loaded_at_utc="2026-05-15T00:00:00+00:00",
        )

    write_once()
    expected_hash = hashlib.sha256(result_path.read_bytes()).hexdigest()
    con = duckdb.connect(str(db_path))
    try:
        assert con.execute(
            "SELECT result_path, payload_sha256, last_successful_batch_id FROM source_load_state"
        ).fetchall() == [(str(result_path), expected_hash, "test-batch")]
        assert con.execute("SELECT source_count, changed_count FROM ingestion_batches").fetchone() == (1, 1)
    finally:
        con.close()

    write_once()
    con = duckdb.connect(str(db_path))
    try:
        assert con.execute("SELECT source_count, changed_count FROM ingestion_batches").fetchone() == (1, 0)
    finally:
        con.close()


def test_write_duckdb_uses_precomputed_source_payload_hash(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    result_path = tmp_path / "model" / "hakari-bench__NanoJMTEB-v2" / "ja_cwir.json"
    result_path.parent.mkdir(parents=True)
    result_path.write_text('{"score": 0.42}', encoding="utf-8")
    row = report.TaskResult(
        model_dir="model",
        model_name="example/model",
        benchmark="NanoJMTEB-v2",
        dataset_id="hakari-bench/NanoJMTEB-v2",
        dataset_name="NanoJMTEB-v2",
        split_name="ja_cwir",
        task_name="ja_cwir",
        task_key="NanoJMTEB-v2::hakari-bench/NanoJMTEB-v2::ja_cwir",
        score=0.42,
        aggregate_metric="ndcg@10",
        result_path=str(result_path),
    )
    monkeypatch.setattr(report, "_payload_sha256", lambda path: pytest.fail(f"should reuse precomputed hash: {path}"))

    report.write_duckdb(
        tmp_path / "results.duckdb",
        runs=[{"model_dir": "model", "model_name": "example/model"}],
        rows=[row],
        metric_rows=[],
        standings={},
        borda_rows=[],
        source_payload_sha256_by_path={str(result_path): "precomputed-sha"},
    )

    con = duckdb.connect(str(tmp_path / "results.duckdb"))
    try:
        assert con.execute("SELECT payload_sha256 FROM source_load_state").fetchone() == ("precomputed-sha",)
    finally:
        con.close()


def test_write_duckdb_records_schema_metadata_and_result_extensions(tmp_path: Path) -> None:
    result_path = tmp_path / "model" / "hakari-bench__NanoJMTEB-v2" / "ja_cwir.json"
    result_path.parent.mkdir(parents=True)
    result_path.write_text(
        json.dumps(
            {
                "model": {"id": "example/model"},
                "target": {"dataset_id": "hakari-bench/NanoJMTEB-v2"},
                "evaluation": {"aggregate_metric_value": 0.42},
                "future_payload": {"kept": True},
            }
        ),
        encoding="utf-8",
    )
    row = report.TaskResult(
        model_dir="model",
        model_name="example/model",
        benchmark="NanoJMTEB-v2",
        dataset_id="hakari-bench/NanoJMTEB-v2",
        dataset_name="NanoJMTEB-v2",
        split_name="ja_cwir",
        task_name="ja_cwir",
        task_key="NanoJMTEB-v2::hakari-bench/NanoJMTEB-v2::ja_cwir",
        score=0.42,
        aggregate_metric="ndcg@10",
        result_path=str(result_path),
    )
    standings, borda_rows = report.compute_standings([row])
    db_path = tmp_path / "results.duckdb"

    def write_database(*, include_result_extensions: bool) -> None:
        report.write_duckdb(
            db_path,
            runs=[{"model_dir": "model", "model_name": "example/model"}],
            rows=[row],
            metric_rows=[
                {
                    "model_dir": "model",
                    "model_name": "example/model",
                    "benchmark": "NanoJMTEB-v2",
                    "dataset_id": "hakari-bench/NanoJMTEB-v2",
                    "task_name": "ja_cwir",
                    "metric_name": "ja_cwir_ndcg@10",
                    "metric_value": 0.42,
                    "result_path": str(result_path),
                }
            ],
            standings=standings,
            borda_rows=borda_rows,
            batch_id="schema-test",
            loaded_at_utc="2026-05-15T00:00:00+00:00",
            include_result_extensions=include_result_extensions,
        )

    write_database(include_result_extensions=False)
    con = duckdb.connect(str(db_path))
    try:
        assert con.execute("SELECT count(*) FROM result_extensions").fetchone() == (0,)
    finally:
        con.close()

    write_database(include_result_extensions=True)

    con = duckdb.connect(str(db_path))
    try:
        assert con.execute("SELECT schema_version, compatibility_level FROM meta_database").fetchone() == (
            report.WAREHOUSE_SCHEMA_VERSION,
            "current",
        )
        assert con.execute("SELECT schema_version, migration_name FROM schema_change_log").fetchone() == (
            report.WAREHOUSE_SCHEMA_VERSION,
            "create_current_warehouse_schema",
        )
        assert con.execute(
            "SELECT result_path, field_path, value_json, discovered_batch_id FROM result_extensions"
        ).fetchall() == [
            (str(result_path), "$.future_payload", '{"kept":true}', "schema-test"),
        ]
    finally:
        con.close()


def test_write_duckdb_materializes_metric_dimension_and_fact(tmp_path: Path) -> None:
    row = report.TaskResult(
        model_dir="model",
        model_name="example/model",
        benchmark="NanoJMTEB-v2",
        dataset_id="hakari-bench/NanoJMTEB-v2",
        dataset_name="NanoJMTEB-v2",
        split_name="ja_cwir",
        task_name="ja_cwir",
        task_key="NanoJMTEB-v2::hakari-bench/NanoJMTEB-v2::ja_cwir",
        score=0.42,
        aggregate_metric="ndcg@10",
        result_path="result.json",
    )
    standings, borda_rows = report.compute_standings([row])
    db_path = tmp_path / "results.duckdb"

    report.write_duckdb(
        db_path,
        runs=[{"model_dir": "model", "model_name": "example/model"}],
        rows=[row],
        metric_rows=[
            {
                "model_dir": "model",
                "model_name": "example/model",
                "benchmark": "NanoJMTEB-v2",
                "dataset_id": "hakari-bench/NanoJMTEB-v2",
                "task_name": "ja_cwir",
                "metric_name": "ja_cwir_ndcg@10",
                "metric_value": 0.42,
                "result_path": "result.json",
            },
            {
                "model_dir": "model",
                "model_name": "example/model",
                "benchmark": "NanoJMTEB-v2",
                "dataset_id": "hakari-bench/NanoJMTEB-v2",
                "task_name": "ja_cwir",
                "metric_name": "ja_cwir_recall@100",
                "metric_value": 0.80,
                "result_path": "result.json",
            },
        ],
        standings=standings,
        borda_rows=borda_rows,
    )

    con = duckdb.connect(str(db_path))
    try:
        assert con.execute(
            "SELECT metric_id, metric_name, metric_family, cutoff FROM dim_metric ORDER BY metric_id"
        ).fetchall() == [
            (1, "ja_cwir_ndcg@10", "ndcg", 10),
            (2, "ja_cwir_recall@100", "recall", 100),
        ]
        assert con.execute(
            """
            SELECT metric_id, model_name, benchmark, task_name, metric_value
            FROM fact_metric_score
            ORDER BY metric_id
            """
        ).fetchall() == [
            (1, "example/model", "NanoJMTEB-v2", "ja_cwir", 0.42),
            (2, "example/model", "NanoJMTEB-v2", "ja_cwir", 0.80),
        ]
    finally:
        con.close()


def test_write_duckdb_materializes_viewer_filter_values(tmp_path: Path) -> None:
    row = report.TaskResult(
        model_dir="model",
        model_name="example/model",
        benchmark="NanoJMTEB-v2",
        dataset_id="hakari-bench/NanoJMTEB-v2",
        dataset_name="NanoJMTEB-v2",
        split_name="ja_cwir",
        task_name="ja_cwir",
        task_key="NanoJMTEB-v2::hakari-bench/NanoJMTEB-v2::ja_cwir",
        score=0.42,
        aggregate_metric="ndcg@10",
        result_path="result.json",
    )
    diagnostic_row = TaskDiagnosticRow(
        model_dir="model",
        model_name="example/model",
        benchmark="NanoJMTEB-v2",
        dataset_id="hakari-bench/NanoJMTEB-v2",
        task_name="ja_cwir",
        task_key="NanoJMTEB-v2::hakari-bench/NanoJMTEB-v2::ja_cwir",
        result_path="result.json",
        base_score=0.42,
        rerank_score=0.50,
        rerank_status="available",
        rerank_top_k=101,
        candidate_ranking="reranking_hybrid",
    )
    standings, borda_rows = report.compute_standings([row])
    db_path = tmp_path / "results.duckdb"

    report.write_duckdb(
        db_path,
        runs=[{"model_dir": "model", "model_name": "example/model"}],
        rows=[row],
        metric_rows=[
            {
                "model_dir": "model",
                "model_name": "example/model",
                "benchmark": "NanoJMTEB-v2",
                "dataset_id": "hakari-bench/NanoJMTEB-v2",
                "task_name": "ja_cwir",
                "metric_name": "ja_cwir_ndcg@10",
                "metric_value": 0.42,
                "result_path": "result.json",
            }
        ],
        diagnostic_rows=[diagnostic_row],
        standings=standings,
        borda_rows=borda_rows,
    )

    con = duckdb.connect(str(db_path))
    try:
        assert con.execute(
            """
            SELECT filter_name, value, label, row_count, sort_key
            FROM viewer_filter_values
            WHERE filter_name IN ('target', 'benchmark', 'model', 'variant')
            ORDER BY filter_name, sort_key
            """
        ).fetchall() == [
            ("benchmark", "NanoJMTEB-v2", "NanoJMTEB-v2", 2, "NanoJMTEB-v2"),
            ("model", "example/model", "example/model", 2, "example/model"),
            ("target", "all", "All", 1, "0:all"),
            ("target", "reranking", "Reranking", 1, "1:reranking"),
            ("variant", "base", "Base", 2, "0:base"),
        ]
    finally:
        con.close()


def test_build_viewer_leaderboard_mart_materializes_display_modes(tmp_path: Path) -> None:
    base_row = report.TaskResult(
        model_dir="model",
        model_name="example/model",
        benchmark="BenchA",
        dataset_id="bench/a",
        dataset_name="BenchA",
        split_name="task1",
        task_name="task1",
        task_key="BenchA::bench/a::task1",
        score=0.42,
        aggregate_metric="ndcg@10",
        result_path="result.json",
        embedding_dim=384,
    )
    variant_row = base_row.model_copy(
        update={
            "score": 0.40,
            "embedding_variant_name": "int8",
            "quantization": "int8",
        }
    )
    db_path = tmp_path / "results.duckdb"
    report.write_duckdb(
        db_path,
        runs=[{"model_dir": "model", "model_name": "example/model"}],
        rows=[base_row, variant_row],
        metric_rows=[
            {
                "model_dir": "model",
                "model_name": "example/model",
                "benchmark": "BenchA",
                "dataset_id": "bench/a",
                "task_name": "task1",
                "metric_name": "task1_ndcg@10",
                "metric_value": 0.42,
                "result_path": "result.json",
            }
        ],
        dataset_metadata_rows=[
            DatasetMetadataRow(
                benchmark="BenchA",
                dataset_id="bench/a",
                dataset_name="BenchA",
                split_name="task1",
                task_name="task1",
                task_key="BenchA::bench/a::task1",
                language="en",
                languages=["en"],
            )
        ],
        standings={},
        borda_rows=[],
    )
    viewer_config = ViewerConfig(
        benchmarks=[
            BenchmarkConfig(
                name="BenchA",
                score_groups=[ScoreGroupConfig(name="dataset", label="Datasets", group_by="dataset_id")],
            )
        ],
        overalls=[OverallConfig(name="Overall", label="Overall", benchmarks=["BenchA"])],
    )

    report.build_viewer_leaderboard_mart(db_path, viewer_config=viewer_config, view_names=["Overall"])

    con = duckdb.connect(str(db_path))
    try:
        assert con.execute(
            """
            SELECT view_name, score_target, include_quantization_variants, model_name, mean_score, expected_tasks
            FROM viewer_leaderboard_rows
            WHERE view_name = 'Overall'
              AND score_target = 'all'
              AND include_quantization_variants IN (false, true)
              AND include_truncate_variants = false
              AND include_rescore_variants = false
              AND include_other_variants = false
            ORDER BY include_quantization_variants, model_name
            """
        ).fetchall() == [
            ("Overall", "all", False, "example/model", 42.0, 1),
            ("Overall", "all", True, "example/model (384 dims)", 42.0, 1),
            ("Overall", "all", True, "example/model (384 dims, int8)", 40.0, 1),
        ]
        assert con.execute(
            """
            SELECT view_name, score_target, include_quantization_variants, code, label, task_count
            FROM viewer_leaderboard_language_options
            WHERE view_name = 'Overall'
              AND score_target = 'all'
              AND include_quantization_variants = true
              AND include_truncate_variants = false
              AND include_rescore_variants = false
              AND include_other_variants = false
            """
        ).fetchall() == [("Overall", "all", True, "en", "EN", 1)]
    finally:
        con.close()


def test_build_viewer_leaderboard_mart_materializes_overall_en_scope(tmp_path: Path) -> None:
    en_row = report.TaskResult(
        model_dir="model",
        model_name="example/model",
        benchmark="BenchA",
        dataset_id="bench/a",
        dataset_name="BenchA",
        split_name="task-en",
        task_name="task-en",
        task_key="BenchA::bench/a::task-en",
        score=0.60,
        aggregate_metric="ndcg@10",
        result_path="en.json",
    )
    ja_row = en_row.model_copy(
        update={
            "split_name": "task-ja",
            "task_name": "task-ja",
            "task_key": "BenchA::bench/a::task-ja",
            "score": 0.40,
            "result_path": "ja.json",
        }
    )
    db_path = tmp_path / "results.duckdb"
    report.write_duckdb(
        db_path,
        runs=[{"model_dir": "model", "model_name": "example/model"}],
        rows=[en_row, ja_row],
        metric_rows=[
            {
                "model_dir": "model",
                "model_name": "example/model",
                "benchmark": "BenchA",
                "dataset_id": "bench/a",
                "task_name": "task-en",
                "metric_name": "task-en_ndcg@10",
                "metric_value": 0.60,
                "result_path": "en.json",
            },
            {
                "model_dir": "model",
                "model_name": "example/model",
                "benchmark": "BenchA",
                "dataset_id": "bench/a",
                "task_name": "task-ja",
                "metric_name": "task-ja_ndcg@10",
                "metric_value": 0.40,
                "result_path": "ja.json",
            },
        ],
        dataset_metadata_rows=[
            DatasetMetadataRow(
                benchmark="BenchA",
                dataset_id="bench/a",
                dataset_name="BenchA",
                split_name="task-en",
                task_name="task-en",
                task_key="BenchA::bench/a::task-en",
                language="en",
                languages=["en"],
                primary_languages=["en"],
            ),
            DatasetMetadataRow(
                benchmark="BenchA",
                dataset_id="bench/a",
                dataset_name="BenchA",
                split_name="task-ja",
                task_name="task-ja",
                task_key="BenchA::bench/a::task-ja",
                language="ja",
                languages=["ja"],
                primary_languages=["ja"],
            ),
        ],
        standings={},
        borda_rows=[],
    )
    viewer_config = ViewerConfig(
        benchmarks=[BenchmarkConfig(name="BenchA")],
        overalls=[
            OverallConfig(name="Overall", label="Overall", benchmarks=["BenchA"]),
            OverallConfig(name="Overall (EN)", label="Overall (EN)", benchmarks=["BenchA"]),
        ],
    )

    report.build_viewer_leaderboard_mart(
        db_path,
        viewer_config=viewer_config,
        view_names=["Overall", "Overall (EN)"],
    )

    con = duckdb.connect(str(db_path))
    try:
        assert con.execute(
            """
            SELECT view_name, expected_tasks, model_name, mean_score, task_count
            FROM viewer_leaderboard_rows
            WHERE score_target = 'all'
              AND include_quantization_variants = false
              AND include_truncate_variants = false
              AND include_rescore_variants = false
              AND include_other_variants = false
            ORDER BY view_name
            """
        ).fetchall() == [
            ("Overall", 2, "example/model", 50.0, 2),
            ("Overall (EN)", 1, "example/model", 60.0, 1),
        ]
    finally:
        con.close()


def test_cached_viewer_leaderboard_mart_rows_match_service_path(tmp_path: Path) -> None:
    def task_row(
        *,
        model_name: str,
        task_name: str,
        score: float,
        result_path: str,
        embedding_variant_name: str | None = None,
        embedding_dim: int | None = 384,
        quantization: str | None = None,
    ) -> report.TaskResult:
        return report.TaskResult(
            model_dir=model_name.replace("/", "__"),
            model_name=model_name,
            benchmark="BenchA",
            dataset_id="bench/a",
            dataset_name="BenchA",
            split_name=task_name,
            task_name=task_name,
            task_key=f"BenchA::bench/a::{task_name}",
            score=score,
            aggregate_metric="ndcg@10",
            result_path=result_path,
            active_parameters=1_000_000,
            total_parameters=2_000_000,
            max_seq_length=512,
            dtype="bf16",
            embedding_variant_name=embedding_variant_name,
            embedding_dim=embedding_dim,
            quantization=quantization,
        )

    rows: list[report.TaskResult] = []
    metric_rows: list[dict[str, object]] = []
    diagnostic_rows: list[TaskDiagnosticRow] = []
    dataset_metadata_rows: list[DatasetMetadataRow] = []
    for task_index, task_name in enumerate(["task1", "task2"], start=1):
        dataset_metadata_rows.append(
            DatasetMetadataRow(
                benchmark="BenchA",
                dataset_id="bench/a",
                dataset_name="BenchA",
                split_name=task_name,
                task_name=task_name,
                task_key=f"BenchA::bench/a::{task_name}",
                language="en",
                languages=["en"],
            )
        )
        for model_name, score in [
            ("example/dense", 0.40 + task_index * 0.01),
            ("bm25", 0.20 + task_index * 0.01),
            ("cross-encoder/tiny-reranker", 0.30 + task_index * 0.01),
        ]:
            row = task_row(
                model_name=model_name,
                task_name=task_name,
                score=score,
                result_path=f"{model_name}/{task_name}.json",
            )
            rows.append(row)
            diagnostic_rows.append(
                TaskDiagnosticRow(
                    model_dir=row.model_dir,
                    model_name=row.model_name,
                    benchmark=row.benchmark,
                    dataset_id=row.dataset_id,
                    task_name=row.task_name,
                    task_key=row.task_key,
                    result_path=row.result_path,
                    base_score=row.score,
                    rerank_score=row.score + 0.05,
                    rerank_status="available",
                    candidate_ranking="reranking_hybrid",
                )
            )
        for variant_name, quantization, score in [
            ("truncate_dim_256", None, 0.38 + task_index * 0.01),
            ("int8", "int8", 0.37 + task_index * 0.01),
            ("rescore:int8", "int8", 0.39 + task_index * 0.01),
        ]:
            variant = task_row(
                model_name="example/dense",
                task_name=task_name,
                score=score,
                result_path=f"example/dense/{task_name}.json",
                embedding_variant_name=variant_name,
                embedding_dim=256 if "truncate" in variant_name else 384,
                quantization=quantization,
            )
            rows.append(variant)
            metric_rows.append(
                {
                    "model_dir": variant.model_dir,
                    "model_name": variant.model_name,
                    "benchmark": variant.benchmark,
                    "dataset_id": variant.dataset_id,
                    "task_name": variant.task_name,
                    "metric_name": f"{task_name}_{variant_name}_reranking_hybrid_top100_rerank_ndcg@10",
                    "metric_value": variant.score + 0.04,
                    "result_path": variant.result_path,
                    "score_target": "reranking",
                    "embedding_variant_name": variant.embedding_variant_name,
                }
            )

    db_path = tmp_path / "results.duckdb"
    report.write_duckdb(
        db_path,
        runs=[{"model_dir": "model", "model_name": "example/dense"}],
        rows=rows,
        metric_rows=metric_rows,
        diagnostic_rows=diagnostic_rows,
        dataset_metadata_rows=dataset_metadata_rows,
        standings={},
        borda_rows=[],
    )
    viewer_config = ViewerConfig(
        benchmarks=[
            BenchmarkConfig(
                name="BenchA",
                score_groups=[ScoreGroupConfig(name="dataset", label="Datasets", group_by="dataset_id")],
            )
        ],
        overalls=[OverallConfig(name="Overall", label="Overall", benchmarks=["BenchA"])],
    )

    assert report._viewer_leaderboard_mart_rows_from_cached_records(
        db_path,
        viewer_config=viewer_config,
        view_names=["Overall", "BenchA"],
    ) == report._viewer_leaderboard_mart_rows_from_service(
        db_path,
        viewer_config=viewer_config,
        view_names=["Overall", "BenchA"],
    )


def test_export_duckdb_tables_to_parquet_writes_canonical_tables(tmp_path: Path) -> None:
    row = report.TaskResult(
        model_dir="model",
        model_name="example/model",
        benchmark="NanoJMTEB-v2",
        dataset_id="hakari-bench/NanoJMTEB-v2",
        dataset_revision=None,
        dataset_revision_requested=None,
        dataset_name="NanoJMTEB-v2",
        split_name="ja_cwir",
        task_name="ja_cwir",
        task_key="NanoJMTEB-v2::hakari-bench/NanoJMTEB-v2::ja_cwir",
        score=0.42,
        aggregate_metric="ndcg@10",
        result_path="result.json",
        active_parameters=None,
        total_parameters=None,
        max_seq_length=None,
        dtype=None,
        attn_implementation=None,
        query_prompt=None,
        document_prompt=None,
        query_prompt_name=None,
        document_prompt_name=None,
        query_encode_task=None,
        document_encode_task=None,
        trust_remote_code=None,
        torch_version=None,
        transformers_version=None,
        sentence_transformers_version=None,
        started_at_utc=None,
        finished_at_utc=None,
        evaluated_at_utc=None,
        duration_seconds_including_dataset_load=None,
        wall_seconds=None,
    )
    standings, borda_rows = report.compute_standings([row])
    db_path = tmp_path / "results.duckdb"
    parquet_dir = tmp_path / "parquet"
    report.write_duckdb(
        db_path,
        runs=[{"model_dir": "model", "model_name": "example/model"}],
        rows=[row],
        metric_rows=[
            {
                "model_dir": "model",
                "model_name": "example/model",
                "benchmark": "NanoJMTEB-v2",
                "dataset_id": "hakari-bench/NanoJMTEB-v2",
                "task_name": "ja_cwir",
                "metric_name": "ja_cwir_ndcg@10",
                "metric_value": 0.42,
                "result_path": "result.json",
            }
        ],
        standings=standings,
        borda_rows=borda_rows,
    )

    report.export_duckdb_tables_to_parquet(db_path, parquet_dir)

    assert sorted(path.name for path in parquet_dir.glob("*.parquet")) == [
        "borda_task_scores.parquet",
        "dataset_metadata.parquet",
        "dim_metric.parquet",
        "dim_model.parquet",
        "dim_task.parquet",
        "dim_variant.parquet",
        "fact_metric_score.parquet",
        "fact_task_score.parquet",
        "ingestion_batches.parquet",
        "meta_database.parquet",
        "metrics_long.parquet",
        "model_scores.parquet",
        "result_extensions.parquet",
        "retrieval_rankings.parquet",
        "runs.parquet",
        "schema_change_log.parquet",
        "source_load_state.parquet",
        "task_diagnostics.parquet",
        "task_results.parquet",
        "viewer_filter_values.parquet",
        "viewer_leaderboard_language_options.parquet",
        "viewer_leaderboard_rows.parquet",
        "viewer_task_results.parquet",
    ]
    con = duckdb.connect()
    try:
        assert con.execute(f"SELECT model_name, score FROM read_parquet('{parquet_dir / 'task_results.parquet'}')").fetchone() == (
            "example/model",
            0.42,
        )
    finally:
        con.close()


def _write_json_result(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with lzma.open(path, "wt", encoding="utf-8") as handle:
        json.dump(payload, handle)


def test_top_rankings_payload_reads_sidecar_within_result_dir(tmp_path: Path) -> None:
    result_path = tmp_path / "model" / "dataset" / "task.json.xz"
    result_path.parent.mkdir(parents=True, exist_ok=True)
    sidecar = result_path.parent / "task.rankings.json"
    sidecar.write_text(json.dumps({"rankings": [{"query_id": "q1"}]}), encoding="utf-8")
    artifact = {"path": "task.rankings.json"}

    payload = report._top_rankings_payload(artifact=artifact, result_path=result_path)

    assert payload == {"rankings": [{"query_id": "q1"}]}


def test_top_rankings_payload_rejects_parent_traversal(tmp_path: Path) -> None:
    secret = tmp_path / "secret.json"
    secret.write_text(json.dumps({"rankings": [{"query_id": "leak"}]}), encoding="utf-8")
    result_path = tmp_path / "model" / "dataset" / "task.json.xz"
    result_path.parent.mkdir(parents=True, exist_ok=True)
    artifact = {"path": "../../secret.json"}

    payload = report._top_rankings_payload(artifact=artifact, result_path=result_path)

    assert payload is None


def test_top_rankings_payload_rejects_absolute_path(tmp_path: Path) -> None:
    secret = tmp_path / "secret.json"
    secret.write_text(json.dumps({"rankings": [{"query_id": "leak"}]}), encoding="utf-8")
    result_path = tmp_path / "model" / "dataset" / "task.json.xz"
    result_path.parent.mkdir(parents=True, exist_ok=True)
    artifact = {"path": str(secret)}

    payload = report._top_rankings_payload(artifact=artifact, result_path=result_path)

    assert payload is None


def test_top_rankings_location_falls_back_on_unsafe_path(tmp_path: Path) -> None:
    result_path = tmp_path / "model" / "dataset" / "task.json.xz"
    result_path.parent.mkdir(parents=True, exist_ok=True)
    artifact = {"path": "../../secret.json"}

    location = report._top_rankings_location(artifact=artifact, result_path=result_path)

    assert location == result_path
