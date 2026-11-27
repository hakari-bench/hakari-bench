from __future__ import annotations

import dataclasses
import hashlib
import json
import lzma
import os
from pathlib import Path
from typing import Any

import duckdb
import pytest

from scripts import build_results_database_and_report as report


def _ranking(kind: str, variant: str | None, score_name: str, query_id: str, corpus_ids: list[str]) -> dict[str, Any]:
    return {
        "name": variant or "base",
        "ranking_kind": kind,
        "embedding_variant_name": variant,
        "distance": "cosine",
        "score_name": score_name,
        "query_id": query_id,
        "corpus_ids": corpus_ids,
        "safeguard_policy": "RRF top-100 plus optional safeguard positive at rank 101" if kind != "retrieval" else None,
        "safeguard_corpus_id": "d2" if kind != "retrieval" and query_id == "q1" else None,
    }


def _payload(*, score: float = 0.42, model_id: str = "example/model") -> dict[str, Any]:
    return {
        "model": {"id": model_id, "total_parameters": 10, "active_parameters": None},
        "environment": {"package_versions": {"torch": "2.0"}},
        "target": {
            "dataset_name": "NanoMIRACL",
            "dataset_id": "hakari-bench/NanoMIRACL",
            "split_name": "en",
            "task_name": "en",
        },
        "evaluation": {
            "aggregate_metric": "ndcg@10",
            "aggregate_metric_value": score,
            "embedding_evaluations": [
                {"name": "base", "aggregate_metric": "ndcg@10", "aggregate_metric_value": score, "best_score_name": "cosine"},
                {
                    "name": "truncate:2",
                    "aggregate_metric": "ndcg@10",
                    "aggregate_metric_value": 0.3,
                    "best_score_name": "truncate:2_cosine",
                },
            ],
            "reranking_evaluations": [
                {"name": "bm25_top_100", "best_score_name": "cosine_bm25_top100_rerank", "aggregate_metric_value": 0.7}
            ],
        },
        "metrics": {"NanoMIRACL_en_cosine_ndcg@10": score},
        "rerank_metrics": {"NanoMIRACL_en_cosine_bm25_top100_rerank_ndcg@10": 0.7},
        "artifacts": {
            "top_rankings": {
                "schema_version": 2,
                "top_k": 100,
                "qrels": [
                    {"query_id": "q1", "relevant_corpus_ids": ["d2"]},
                    {"query_id": "q2", "relevant_corpus_ids": ["d4"]},
                ],
                "rankings": [
                    _ranking("retrieval", None, "cosine", "q1", ["d1", "d2"]),
                    _ranking("retrieval", None, "cosine", "q2", ["d4", "d3"]),
                    _ranking("retrieval", None, "dot", "q1", ["d2", "d1"]),
                    _ranking("retrieval", "truncate:2", "truncate:2_cosine", "q1", ["d1", "d2"]),
                    _ranking("retrieval", "truncate:2", "truncate:2_cosine", "q2", ["d3", "d4"]),
                    _ranking("candidate_rerank", None, "cosine_bm25_top100_rerank", "q1", ["d2", "d1"]),
                    _ranking("candidate_rerank", None, "cosine_bm25_top100_rerank", "q2", ["d3", "d4"]),
                    _ranking(
                        "candidate_rerank", "truncate:2", "truncate:2_cosine_bm25_top100_rerank", "q1", ["d2", "d1"]
                    ),
                ],
            }
        },
    }


def _write_result(path: Path, payload: dict[str, Any] | str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    text = payload if isinstance(payload, str) else json.dumps(payload)
    if path.name.endswith(".json.xz"):
        with lzma.open(path, "wt", encoding="utf-8") as file:
            file.write(text)
    else:
        path.write_text(text, encoding="utf-8")


def _results_tree(tmp_path: Path) -> Path:
    results_dir = tmp_path / "results"
    _write_result(results_dir / "example__model" / "hakari-bench__NanoMIRACL" / "en.json.xz", _payload())
    # Large enough to exercise the streaming fallback reader when uncached.
    big = _payload(model_id="example/big")
    big["artifacts"]["top_rankings"]["padding"] = "x" * (report.FULL_PARSE_RESULT_JSON_MAX_BYTES + 1)
    _write_result(results_dir / "example__big" / "hakari-bench__NanoMIRACL" / "en.json", big)
    return results_dir


def _comparable(payload: tuple[Any, ...]) -> tuple[Any, ...]:
    rows, runs, metric_rows, diagnostic_rows, dataset_metadata_rows, ranking_rows = payload[:6]
    return (
        sorted(rows, key=repr),
        sorted(runs, key=repr),
        sorted(metric_rows, key=repr),
        sorted(diagnostic_rows, key=repr),
        sorted(dataset_metadata_rows, key=repr),
        sorted(ranking_rows, key=repr),
        payload[6] if len(payload) > 6 else None,
    )


def _forbid_result_parsing(monkeypatch: pytest.MonkeyPatch) -> None:
    def fail(*args: Any, **kwargs: Any) -> Any:
        raise AssertionError("warm extract cache should not parse result JSON")

    for name in (
        "_decompress_result_bytes",
        "_read_result_summary_payload_with_sha256",
        "_read_result_json_from_summary",
        "_read_result_json",
    ):
        monkeypatch.setattr(report, name, fail)


@pytest.mark.parametrize("workers", [1, 2])
def test_result_extract_cache_matches_uncached_rows(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch, workers: int
) -> None:
    results_dir = _results_tree(tmp_path)
    cache_dir = tmp_path / "cache"
    kwargs: dict[str, Any] = {
        "model_cards_path": None,
        "include_source_hashes": True,
        "result_selection_workers": workers,
        "result_row_workers": workers,
    }

    uncached = report.load_results(results_dir, **kwargs)
    cold = report.load_results(results_dir, result_cache_dir=cache_dir, **kwargs)
    assert list((cache_dir).rglob("*.json.zlib"))
    with monkeypatch.context() as patch:
        _forbid_result_parsing(patch)
        warm = report.load_results(results_dir, result_cache_dir=cache_dir, **kwargs)

    assert _comparable(cold) == _comparable(uncached)
    assert _comparable(warm) == _comparable(uncached)
    assert any(row.score_target == "reranking_without_safeguard" for row in uncached[2])


def test_streaming_duckdb_with_extract_cache_matches_uncached_build(tmp_path: Path) -> None:
    results_dir = _results_tree(tmp_path)
    cache_dir = tmp_path / "cache"
    benchmark_configs = report.load_benchmark_configs()
    paths = {name: tmp_path / f"{name}.duckdb" for name in ("uncached", "cold", "warm")}
    for name, db_path in paths.items():
        report.write_duckdb_streaming_results(
            results_dir,
            db_path,
            benchmark_configs=benchmark_configs,
            model_cards_path=None,
            result_cache_dir=None if name == "uncached" else cache_dir,
        )

    def table_rows(db_path: Path) -> dict[str, list[tuple[Any, ...]]]:
        con = duckdb.connect(str(db_path), read_only=True)
        try:
            tables = [row[0] for row in con.execute("SELECT table_name FROM duckdb_tables() ORDER BY 1").fetchall()]
            result = {}
            for table in tables:
                columns = [
                    row[0]
                    for row in con.execute(
                        "SELECT column_name FROM duckdb_columns() WHERE table_name = ? ORDER BY column_index", [table]
                    ).fetchall()
                    if row[0] not in {"loaded_at_utc", "last_successful_batch_id", "batch_id", "created_at_utc"}
                    and not row[0].endswith("_at_utc")
                ]
                select = ", ".join(f'"{column}"' for column in columns)
                result[table] = sorted(con.execute(f'SELECT {select} FROM "{table}"').fetchall(), key=repr)
            return result
        finally:
            con.close()

    uncached = table_rows(paths["uncached"])
    assert table_rows(paths["cold"]) == uncached
    assert table_rows(paths["warm"]) == uncached
    assert uncached["fact_task_score"]


def test_result_extract_cache_reparses_changed_file(tmp_path: Path) -> None:
    results_dir = tmp_path / "results"
    path = results_dir / "example__model" / "hakari-bench__NanoMIRACL" / "en.json.xz"
    cache_dir = tmp_path / "cache"
    _write_result(path, _payload(score=0.42))
    first = report.load_results(results_dir, model_cards_path=None, result_cache_dir=cache_dir)
    _write_result(path, _payload(score=0.55))
    stat = path.stat()
    os.utime(path, ns=(stat.st_atime_ns, stat.st_mtime_ns + 1_000_000))

    second = report.load_results(results_dir, model_cards_path=None, result_cache_dir=cache_dir)

    assert first[0][0].score == pytest.approx(0.42)
    assert second[0][0].score == pytest.approx(0.55)


def test_result_extract_cache_applies_current_model_cards(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    results_dir = _results_tree(tmp_path)
    cache_dir = tmp_path / "cache"
    model_cards_path = tmp_path / "model_cards.yaml"

    def write_card(active: int) -> None:
        model_cards_path.write_text(
            f"""
models:
  - id: example/model
    method: dense
    parameters:
      total: 10
      input_embedding: {10 - active}
      active: {active}
""".strip(),
            encoding="utf-8",
        )

    write_card(4)
    first = report.load_results(results_dir, model_cards_path=model_cards_path, result_cache_dir=cache_dir)
    write_card(5)
    with monkeypatch.context() as patch:
        _forbid_result_parsing(patch)
        second = report.load_results(results_dir, model_cards_path=model_cards_path, result_cache_dir=cache_dir)

    def active(payload: tuple[Any, ...]) -> set[int | None]:
        return {row.active_parameters for row in payload[0] if row.model_name == "example/model"}

    assert active(first) == {4}
    assert active(second) == {5}


def test_result_extract_cache_skips_legacy_non_standard_json(tmp_path: Path) -> None:
    results_dir = tmp_path / "results"
    path = results_dir / "example__model" / "hakari-bench__NanoMIRACL" / "en.json"
    payload = _payload()
    payload["evaluation"]["wall_seconds"] = float("nan")
    _write_result(path, json.dumps(payload))
    cache_dir = tmp_path / "cache"

    uncached = report.load_results(results_dir, model_cards_path=None)
    cached = report.load_results(results_dir, model_cards_path=None, result_cache_dir=cache_dir)

    assert repr(_comparable(cached)) == repr(_comparable(uncached))
    assert not list(cache_dir.rglob("*.json.zlib"))


def test_result_extract_cache_does_not_cache_sidecar_rankings(tmp_path: Path) -> None:
    results_dir = tmp_path / "results"
    path = results_dir / "example__model" / "hakari-bench__NanoMIRACL" / "en.json"
    payload = _payload()
    sidecar = payload["artifacts"]["top_rankings"]
    payload["artifacts"]["top_rankings"] = {"schema_version": 2, "path": "en.rankings.json"}
    _write_result(path, payload)
    (path.parent / "en.rankings.json").write_text(json.dumps(sidecar), encoding="utf-8")
    cache_dir = tmp_path / "cache"

    uncached = report.load_results(results_dir, model_cards_path=None)
    cached = report.load_results(results_dir, model_cards_path=None, result_cache_dir=cache_dir)

    assert _comparable(cached) == _comparable(uncached)
    assert uncached[2]
    payload_sha256 = hashlib.sha256(path.read_bytes()).hexdigest()
    assert report._load_result_extract(cache_dir, payload_sha256) is None


def test_resolve_result_cache_dir_prefers_flag_then_env(monkeypatch: pytest.MonkeyPatch, tmp_path: Path) -> None:
    monkeypatch.setenv(report.RESULT_CACHE_DIR_ENV, str(tmp_path / "env"))
    assert report.resolve_result_cache_dir(tmp_path / "flag", disabled=False) == tmp_path / "flag"
    assert report.resolve_result_cache_dir(None, disabled=False) == tmp_path / "env"
    assert report.resolve_result_cache_dir(tmp_path / "flag", disabled=True) is None
    monkeypatch.delenv(report.RESULT_CACHE_DIR_ENV)
    assert report.resolve_result_cache_dir(None, disabled=False) == report.DEFAULT_RESULT_CACHE_DIR


def test_resolve_warehouse_build_plan_disables_result_cache() -> None:
    args = report.build_arg_parser().parse_args(["--no-result-cache"])
    assert report.resolve_warehouse_build_plan(args).result_cache_dir is None


def test_parallel_viewer_mart_rows_match_serial_order(tmp_path: Path) -> None:
    results_dir = tmp_path / "results"
    for model_index, score in enumerate((0.4, 0.6, 0.5)):
        for split_name in ("en", "ja"):
            payload = _payload(score=score, model_id=f"example/model-{model_index}")
            payload["target"] = {
                "dataset_name": "NanoMLDR",
                "dataset_id": "hakari-bench/NanoMLDR",
                "split_name": split_name,
                "task_name": split_name,
            }
            _write_result(
                results_dir / f"example__model-{model_index}" / "hakari-bench__NanoMLDR" / f"{split_name}.json",
                payload,
            )
    viewer_config = report.load_viewer_config(report.DEFAULT_VIEWER_CONFIG_DIR)
    db_path = tmp_path / "mart.duckdb"
    report.write_duckdb_streaming_results(
        results_dir,
        db_path,
        benchmark_configs=viewer_config.benchmarks,
        model_cards_path=None,
    )
    view_names = report._viewer_leaderboard_mart_view_names(viewer_config)

    serial = report._viewer_leaderboard_mart_rows_from_cached_records(
        db_path, viewer_config=viewer_config, view_names=view_names, workers=1
    )
    parallel = report._viewer_leaderboard_mart_rows_from_cached_records(
        db_path, viewer_config=viewer_config, view_names=view_names, workers=3
    )

    assert serial[0]
    assert parallel == serial



def _metric_row(index: int, value: Any) -> Any:
    # model_construct skips validation so tests can inject values the Arrow
    # schema cannot represent.
    return report.MetricLongRow.model_construct(
        model_dir="m",
        model_name="m",
        benchmark="b",
        dataset_id="d",
        task_name="t",
        metric_name=f"metric_{index}",
        metric_value=value,
        result_path="p",
        score_target="all",
        embedding_variant_name=None,
    )


def _streaming_schemas() -> tuple[duckdb.DuckDBPyConnection, Any]:
    con = duckdb.connect()
    report._create_task_results_table(con, "task_results_raw")
    report._create_metrics_long_table(con, "metrics_long_raw")
    schemas = report._streaming_arrow_schemas(con)
    assert schemas is not None
    return con, schemas


def test_columnarize_processed_rows_keeps_rows_when_values_do_not_fit_schema() -> None:
    _, schemas = _streaming_schemas()
    processed = report.ProcessedResultRows(
        rows=[],
        run_accumulators={},
        metric_rows=[_metric_row(0, 1.5), _metric_row(1, 2)],
        diagnostic_rows=[],
        dataset_metadata_rows=[],
        ranking_rows=[],
    )
    columnar = report._columnarize_processed_rows(processed, schemas)
    assert columnar.metric_rows == []
    assert columnar.metric_table is not None
    assert columnar.metric_table.column("metric_value").to_pylist() == [1.5, 2.0]

    bad = dataclasses.replace(processed, metric_rows=[_metric_row(0, "not-a-number")])
    fallback = report._columnarize_processed_rows(bad, schemas)
    assert fallback.metric_rows == bad.metric_rows
    assert fallback.metric_table is None


def test_ordered_insert_buffer_preserves_arrival_order_across_rows_and_tables() -> None:
    con, schemas = _streaming_schemas()
    buffer = report._OrderedInsertBuffer("metrics_long_raw", report.METRIC_LONG_COLUMNS)
    buffer.add_table(report._rows_to_arrow_table([_metric_row(0, 0.0), _metric_row(1, 1.0)], schemas.metrics_long))
    buffer.add_rows([_metric_row(2, 2.0)])
    buffer.add_table(report._rows_to_arrow_table([_metric_row(3, 3.0)], schemas.metrics_long))
    assert buffer.row_count == 4

    buffer.flush(con)

    assert con.execute("SELECT metric_name, metric_value FROM metrics_long_raw").fetchall() == [
        ("metric_0", 0.0),
        ("metric_1", 1.0),
        ("metric_2", 2.0),
        ("metric_3", 3.0),
    ]
    assert buffer.row_count == 0


@pytest.mark.parametrize("use_cache", [False, True])
def test_selected_result_sha256_covers_bytes_after_compressed_stream(tmp_path: Path, use_cache: bool) -> None:
    results_dir = tmp_path / "results"
    path = results_dir / "example__model" / "hakari-bench__NanoMIRACL" / "en.json.xz"
    _write_result(path, _payload())
    with path.open("ab") as file:
        file.write(b"\0" * 4096 + b"trailing bytes after the xz stream")

    selected = report._selected_result_json(
        path,
        results_dir=results_dir,
        source_priority=0,
        benchmark_configs=report.load_benchmark_configs(),
        target_benchmarks=set(report.target_benchmark_names(report.load_benchmark_configs())),
        exclude_model_names=set(),
        result_cache_dir=tmp_path / "cache" if use_cache else None,
    )

    assert selected is not None
    assert selected.payload_sha256 == hashlib.sha256(path.read_bytes()).hexdigest()
    assert selected.payload_sha256 == report._payload_sha256(str(path))


def test_result_extract_cache_handles_artifacts_before_evaluation(tmp_path: Path) -> None:
    results_dir = tmp_path / "results"
    payload = _payload()
    reordered = {"artifacts": payload.pop("artifacts"), **payload}
    _write_result(results_dir / "example__model" / "hakari-bench__NanoMIRACL" / "en.json.xz", reordered)
    cache_dir = tmp_path / "cache"

    uncached = report.load_results(results_dir, model_cards_path=None)
    cached = report.load_results(results_dir, model_cards_path=None, result_cache_dir=cache_dir)

    assert uncached[2]
    assert _comparable(cached) == _comparable(uncached)
    assert list(cache_dir.rglob("*.json.zlib"))


def test_result_extract_cache_reuses_content_when_only_mtime_changes(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    results_dir = _results_tree(tmp_path)
    cache_dir = tmp_path / "cache"
    first = report.load_results(results_dir, model_cards_path=None, result_cache_dir=cache_dir)
    for path in results_dir.rglob("*.json*"):
        stat = path.stat()
        os.utime(path, ns=(stat.st_atime_ns, stat.st_mtime_ns + 5_000_000_000))

    with monkeypatch.context() as patch:
        _forbid_result_parsing(patch)
        patch.setattr(report, "_read_result_extract_stream", lambda *args, **kwargs: pytest.fail("should reuse extract"))
        second = report.load_results(results_dir, model_cards_path=None, result_cache_dir=cache_dir)

    assert _comparable(second) == _comparable(first)
