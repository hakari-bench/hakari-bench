from __future__ import annotations

import argparse
import json
from collections import defaultdict
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import duckdb


TARGET_BENCHMARKS = [
    "MNanoBEIR",
    "NanoJMTEB",
    "NanoRTEB",
    "NanoMTEB",
    "NanoMMTEB",
    "NanoMIRACL",
    "NanoMLDR",
    "NanoLongEmbed",
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
]
VIEWS = ["Overall", *TARGET_BENCHMARKS]


@dataclass(frozen=True)
class TaskResult:
    model_dir: str
    model_name: str
    benchmark: str
    dataset_id: str
    dataset_revision: str | None
    dataset_revision_requested: str | None
    dataset_name: str
    split_name: str | None
    task_name: str
    task_key: str
    score: float
    aggregate_metric: str | None
    result_path: str
    active_parameters: int | None
    total_parameters: int | None
    max_seq_length: int | None
    dtype: str | None
    attn_implementation: str | None
    torch_version: str | None
    transformers_version: str | None
    sentence_transformers_version: str | None
    started_at_utc: str | None
    finished_at_utc: str | None
    evaluated_at_utc: str | None
    duration_seconds_including_dataset_load: float | None
    wall_seconds: float | None
    embedding_variant_name: str | None = None
    embedding_dim: int | None = None
    quantization: str | None = None


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--results-dir", type=Path, default=Path("output/results"))
    parser.add_argument("--duckdb-path", type=Path, default=Path("output/results/nano_ir_bench.duckdb"))
    parser.add_argument("--html-output", type=Path, required=True)
    args = parser.parse_args()

    rows, runs, metric_rows = load_results(args.results_dir)
    base_rows = [row for row in rows if row.embedding_variant_name is None]
    standings, borda_rows = compute_standings(base_rows)
    write_duckdb(args.duckdb_path, runs=runs, rows=rows, metric_rows=metric_rows, standings=standings, borda_rows=borda_rows)
    write_html(args.html_output, duckdb_path=args.duckdb_path, rows=base_rows, runs=runs, standings=standings)


def load_results(results_dir: Path) -> tuple[list[TaskResult], list[dict[str, Any]], list[dict[str, Any]]]:
    rows: list[TaskResult] = []
    runs: list[dict[str, Any]] = []
    metric_rows: list[dict[str, Any]] = []

    for all_path in sorted(results_dir.glob("*/all.json")):
        payload = json.loads(all_path.read_text(encoding="utf-8"))
        model = payload.get("model", {})
        environment = payload.get("environment", {})
        package_versions = environment.get("package_versions", {})
        totals = payload.get("totals", {})
        model_dir = all_path.parent.name
        model_name = str(model.get("name_or_path") or model_dir)
        runs.append(
            {
                "model_dir": model_dir,
                "model_name": model_name,
                "all_json_path": str(all_path),
                "generated_at_utc": payload.get("generated_at_utc"),
                "started_at_utc": payload.get("run", {}).get("started_at_utc"),
                "finished_at_utc": payload.get("run", {}).get("finished_at_utc"),
                "target_count": totals.get("target_count"),
                "split_count": totals.get("split_count"),
                "cache_hit_count": totals.get("cache_hit_count"),
                "evaluated_count": totals.get("evaluated_count"),
                "aggregate_metric_mean": totals.get("aggregate_metric_mean"),
                "active_parameters": model.get("active_parameters"),
                "total_parameters": model.get("total_parameters"),
                "max_seq_length": model.get("max_seq_length"),
                "dtype": model.get("dtype"),
                "attn_implementation": model.get("attn_implementation"),
                "torch_version": package_versions.get("torch"),
                "transformers_version": package_versions.get("transformers"),
                "sentence_transformers_version": package_versions.get("sentence-transformers"),
            }
        )
    for result_path in sorted(results_dir.glob("*/*/*.json")):
        task_payload = json.loads(result_path.read_text(encoding="utf-8"))
        target = task_payload.get("target", {})
        if not isinstance(target, dict):
            continue
        benchmark = benchmark_name(target.get("dataset_id"), target.get("dataset_name"))
        if benchmark not in TARGET_BENCHMARKS:
            continue
        evaluation = task_payload.get("evaluation", {})
        if not isinstance(evaluation, dict):
            continue
        score = evaluation.get("aggregate_metric_value")
        if not isinstance(score, int | float):
            continue
        model = task_payload.get("model", {})
        environment = task_payload.get("environment", {})
        package_versions = environment.get("package_versions", {}) if isinstance(environment, dict) else {}
        model_dir = result_path.relative_to(results_dir).parts[0]
        model_name = str(model.get("name_or_path") or model_dir) if isinstance(model, dict) else model_dir
        dataset_id = str(target.get("dataset_id") or "")
        dataset_revision = _dataset_revision_value(target.get("dataset_revision"), key="resolved")
        dataset_revision_requested = _dataset_revision_value(target.get("dataset_revision"), key="requested")
        task_name = str(target.get("task_name") or target.get("split_name") or "")
        task_key = f"{benchmark}::{dataset_id}::{task_name}"
        common: dict[str, Any] = {
            "model_dir": model_dir,
            "model_name": model_name,
            "benchmark": benchmark,
            "dataset_id": dataset_id,
            "dataset_revision": dataset_revision,
            "dataset_revision_requested": dataset_revision_requested,
            "dataset_name": str(target.get("dataset_name") or ""),
            "split_name": target.get("split_name"),
            "task_name": task_name,
            "task_key": task_key,
            "result_path": str(result_path),
            "active_parameters": _int_or_none(model.get("active_parameters")) if isinstance(model, dict) else None,
            "total_parameters": _int_or_none(model.get("total_parameters")) if isinstance(model, dict) else None,
            "max_seq_length": _int_or_none(model.get("max_seq_length")) if isinstance(model, dict) else None,
            "dtype": model.get("dtype") if isinstance(model, dict) else None,
            "attn_implementation": model.get("attn_implementation") if isinstance(model, dict) else None,
            "torch_version": package_versions.get("torch"),
            "transformers_version": package_versions.get("transformers"),
            "sentence_transformers_version": package_versions.get("sentence-transformers"),
            "started_at_utc": evaluation.get("started_at_utc"),
            "finished_at_utc": evaluation.get("finished_at_utc"),
            "evaluated_at_utc": evaluation.get("evaluated_at_utc"),
            "duration_seconds_including_dataset_load": _float_or_none(
                evaluation.get("duration_seconds_including_dataset_load")
            ),
            "wall_seconds": _float_or_none(evaluation.get("wall_seconds")),
        }
        embedding_evaluations = _embedding_evaluations(
            evaluation.get("embedding_evaluations") or task_payload.get("embedding_evaluations")
        )
        base_embedding = _embedding_evaluation_named(embedding_evaluations, "base")
        rows.append(
            TaskResult(
                **common,
                score=float(score),
                aggregate_metric=evaluation.get("aggregate_metric"),
                embedding_dim=_embedding_dim(base_embedding),
                quantization=_quantization_precision(base_embedding),
            )
        )
        for embedding_evaluation in embedding_evaluations:
            variant_name = embedding_evaluation.get("name")
            if not isinstance(variant_name, str) or variant_name == "base":
                continue
            variant_score = embedding_evaluation.get("aggregate_metric_value")
            if not isinstance(variant_score, int | float):
                continue
            rows.append(
                TaskResult(
                    **common,
                    score=float(variant_score),
                    aggregate_metric=embedding_evaluation.get("aggregate_metric") or evaluation.get("aggregate_metric"),
                    embedding_variant_name=variant_name,
                    embedding_dim=_embedding_dim(embedding_evaluation),
                    quantization=_quantization_precision(embedding_evaluation),
                )
            )
        for metric_name, metric_value in task_payload.get("metrics", {}).items():
            if isinstance(metric_value, int | float):
                metric_rows.append(
                    {
                        "model_dir": model_dir,
                        "model_name": model_name,
                        "benchmark": benchmark,
                        "dataset_id": dataset_id,
                        "task_name": task_name,
                        "metric_name": metric_name,
                        "metric_value": float(metric_value),
                        "result_path": str(result_path),
                    }
                )

    return rows, runs, metric_rows


def benchmark_name(dataset_id: Any, dataset_name: Any) -> str:
    value = f"{dataset_id or ''}/{dataset_name or ''}"
    if "NanoBEIR" in value:
        return "MNanoBEIR"
    for name in TARGET_BENCHMARKS[1:]:
        if name in value:
            return name
    return "Other"


def _embedding_evaluations(value: Any) -> list[dict[str, Any]]:
    if not isinstance(value, list):
        return []
    return [item for item in value if isinstance(item, dict)]


def _embedding_evaluation_named(items: list[dict[str, Any]], name: str) -> dict[str, Any] | None:
    for item in items:
        if item.get("name") == name:
            return item
    return None


def _embedding_dim(item: dict[str, Any] | None) -> int | None:
    if item is None:
        return None
    dimensions = item.get("embedding_dimensions")
    if not isinstance(dimensions, dict):
        return None
    return _int_or_none(dimensions.get("dim"))


def _quantization_precision(item: dict[str, Any] | None) -> str | None:
    if item is None:
        return None
    metadata = item.get("embedding_metadata")
    if isinstance(metadata, dict):
        for key in ("query", "corpus"):
            side = metadata.get(key)
            if not isinstance(side, dict):
                continue
            quantization = side.get("quantization")
            if isinstance(quantization, dict) and quantization.get("precision"):
                return str(quantization["precision"])
    transform = item.get("transform")
    if isinstance(transform, dict):
        for step in transform.get("steps", []):
            if isinstance(step, dict) and step.get("type") == "quantize" and step.get("parameters"):
                parameters = step["parameters"]
                if isinstance(parameters, dict) and parameters.get("precision"):
                    return str(parameters["precision"])
    return None


def compute_standings(rows: list[TaskResult]) -> tuple[dict[str, list[dict[str, Any]]], list[dict[str, Any]]]:
    standings: dict[str, list[dict[str, Any]]] = {}
    all_borda_rows: list[dict[str, Any]] = []
    for view in VIEWS:
        view_rows = rows if view == "Overall" else [row for row in rows if row.benchmark == view]
        expected_task_count = len({row.task_key for row in view_rows})
        counts_by_model: dict[str, int] = defaultdict(int)
        rows_by_model: dict[str, list[TaskResult]] = defaultdict(list)
        for row in view_rows:
            counts_by_model[row.model_name] += 1
            rows_by_model[row.model_name].append(row)
        complete_models = sorted(model for model, count in counts_by_model.items() if count == expected_task_count)
        complete_set = set(complete_models)
        complete_rows = [row for row in view_rows if row.model_name in complete_set]
        task_rows: dict[str, list[TaskResult]] = defaultdict(list)
        for row in complete_rows:
            task_rows[row.task_key].append(row)

        borda_by_model: dict[str, list[float]] = defaultdict(list)
        for task_key, task_group in task_rows.items():
            ranked = ranks_desc([(row.model_name, row.score) for row in task_group])
            n_models = len(ranked)
            rank_by_model = {model: rank for model, rank in ranked}
            for row in task_group:
                rank = rank_by_model[row.model_name]
                borda = 100.0 if n_models <= 1 else 100.0 * (n_models - rank) / (n_models - 1)
                borda_by_model[row.model_name].append(borda)
                all_borda_rows.append(
                    {
                        "view_name": view,
                        "model_name": row.model_name,
                        "benchmark": row.benchmark,
                        "task_key": task_key,
                        "rank": rank,
                        "model_count": n_models,
                        "borda_score": borda,
                        "score": row.score,
                    }
                )

        model_rows: list[dict[str, Any]] = []
        for model_name in complete_models:
            model_task_rows = rows_by_model[model_name]
            score_mean = mean(row.score for row in model_task_rows)
            borda_score = mean(borda_by_model[model_name])
            first = model_task_rows[0]
            model_rows.append(
                {
                    "view": view,
                    "model": model_name,
                    "task_count": len(model_task_rows),
                    "mean_score": score_mean * 100.0,
                    "borda_score": borda_score,
                    "active_parameters": first.active_parameters,
                    "total_parameters": first.total_parameters,
                    "max_seq_length": first.max_seq_length,
                    "dtype": first.dtype,
                    "attn_implementation": first.attn_implementation,
                    "torch_version": first.torch_version,
                    "transformers_version": first.transformers_version,
                    "sentence_transformers_version": first.sentence_transformers_version,
                }
            )
        apply_rank(model_rows, value_key="mean_score", rank_key="score_rank")
        apply_rank(model_rows, value_key="borda_score", rank_key="borda_rank")
        model_rows.sort(key=lambda item: (item["borda_rank"], item["score_rank"], item["model"]))
        standings[view] = model_rows
    return standings, all_borda_rows


def ranks_desc(items: list[tuple[str, float]]) -> list[tuple[str, float]]:
    sorted_items = sorted(items, key=lambda item: (-item[1], item[0]))
    ranks: list[tuple[str, float]] = []
    index = 0
    while index < len(sorted_items):
        end = index + 1
        while end < len(sorted_items) and sorted_items[end][1] == sorted_items[index][1]:
            end += 1
        average_rank = (index + 1 + end) / 2.0
        ranks.extend((model, average_rank) for model, _ in sorted_items[index:end])
        index = end
    return ranks


def apply_rank(rows: list[dict[str, Any]], *, value_key: str, rank_key: str) -> None:
    ranked = ranks_desc([(row["model"], float(row[value_key])) for row in rows])
    rank_by_model = {model: rank for model, rank in ranked}
    for row in rows:
        row[rank_key] = rank_by_model[row["model"]]


def write_duckdb(
    db_path: Path,
    *,
    runs: list[dict[str, Any]],
    rows: list[TaskResult],
    metric_rows: list[dict[str, Any]],
    standings: dict[str, list[dict[str, Any]]],
    borda_rows: list[dict[str, Any]],
) -> None:
    db_path.parent.mkdir(parents=True, exist_ok=True)
    con = duckdb.connect(str(db_path))
    try:
        for table in ["runs", "task_results", "metrics_long", "model_scores", "borda_task_scores"]:
            con.execute(f"DROP TABLE IF EXISTS {table}")
        con.execute(
            """
            CREATE TABLE runs (
                model_dir VARCHAR, model_name VARCHAR, all_json_path VARCHAR,
                generated_at_utc VARCHAR, started_at_utc VARCHAR, finished_at_utc VARCHAR,
                target_count INTEGER, split_count INTEGER, cache_hit_count INTEGER, evaluated_count INTEGER,
                aggregate_metric_mean DOUBLE, active_parameters BIGINT, total_parameters BIGINT,
                max_seq_length INTEGER, dtype VARCHAR, attn_implementation VARCHAR,
                torch_version VARCHAR, transformers_version VARCHAR, sentence_transformers_version VARCHAR
            )
            """
        )
        con.executemany(
            "INSERT INTO runs VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
            [
                (
                    item.get("model_dir"),
                    item.get("model_name"),
                    item.get("all_json_path"),
                    item.get("generated_at_utc"),
                    item.get("started_at_utc"),
                    item.get("finished_at_utc"),
                    item.get("target_count"),
                    item.get("split_count"),
                    item.get("cache_hit_count"),
                    item.get("evaluated_count"),
                    item.get("aggregate_metric_mean"),
                    item.get("active_parameters"),
                    item.get("total_parameters"),
                    item.get("max_seq_length"),
                    item.get("dtype"),
                    item.get("attn_implementation"),
                    item.get("torch_version"),
                    item.get("transformers_version"),
                    item.get("sentence_transformers_version"),
                )
                for item in runs
            ],
        )
        con.execute(
            """
            CREATE TABLE task_results (
                model_dir VARCHAR, model_name VARCHAR, benchmark VARCHAR,
                dataset_id VARCHAR, dataset_revision VARCHAR, dataset_revision_requested VARCHAR,
                dataset_name VARCHAR, split_name VARCHAR, task_name VARCHAR, task_key VARCHAR,
                score DOUBLE, score_100 DOUBLE, aggregate_metric VARCHAR, result_path VARCHAR,
                active_parameters BIGINT, total_parameters BIGINT, max_seq_length INTEGER, dtype VARCHAR,
                embedding_variant_name VARCHAR, embedding_dim INTEGER, quantization VARCHAR,
                attn_implementation VARCHAR, torch_version VARCHAR, transformers_version VARCHAR,
                sentence_transformers_version VARCHAR, started_at_utc VARCHAR, finished_at_utc VARCHAR,
                evaluated_at_utc VARCHAR, duration_seconds_including_dataset_load DOUBLE, wall_seconds DOUBLE
            )
            """
        )
        con.executemany(
            "INSERT INTO task_results VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
            [
                (
                    row.model_dir,
                    row.model_name,
                    row.benchmark,
                    row.dataset_id,
                    row.dataset_revision,
                    row.dataset_revision_requested,
                    row.dataset_name,
                    row.split_name,
                    row.task_name,
                    row.task_key,
                    row.score,
                    row.score * 100.0,
                    row.aggregate_metric,
                    row.result_path,
                    row.active_parameters,
                    row.total_parameters,
                    row.max_seq_length,
                    row.dtype,
                    row.embedding_variant_name,
                    row.embedding_dim,
                    row.quantization,
                    row.attn_implementation,
                    row.torch_version,
                    row.transformers_version,
                    row.sentence_transformers_version,
                    row.started_at_utc,
                    row.finished_at_utc,
                    row.evaluated_at_utc,
                    row.duration_seconds_including_dataset_load,
                    row.wall_seconds,
                )
                for row in rows
            ],
        )
        con.execute(
            """
            CREATE TABLE metrics_long (
                model_dir VARCHAR, model_name VARCHAR, benchmark VARCHAR,
                dataset_id VARCHAR, task_name VARCHAR, metric_name VARCHAR, metric_value DOUBLE, result_path VARCHAR
            )
            """
        )
        con.executemany(
            "INSERT INTO metrics_long VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
            [
                (
                    row.get("model_dir"),
                    row.get("model_name"),
                    row.get("benchmark"),
                    row.get("dataset_id"),
                    row.get("task_name"),
                    row.get("metric_name"),
                    row.get("metric_value"),
                    row.get("result_path"),
                )
                for row in metric_rows
            ],
        )
        score_rows = [row for view_rows in standings.values() for row in view_rows]
        con.execute(
            """
            CREATE TABLE model_scores (
                view_name VARCHAR, model_name VARCHAR, task_count INTEGER,
                mean_score DOUBLE, score_rank DOUBLE, borda_score DOUBLE, borda_rank DOUBLE,
                active_parameters BIGINT, total_parameters BIGINT, max_seq_length INTEGER, dtype VARCHAR,
                attn_implementation VARCHAR, torch_version VARCHAR, transformers_version VARCHAR,
                sentence_transformers_version VARCHAR
            )
            """
        )
        con.executemany(
            "INSERT INTO model_scores VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
            [
                (
                    row.get("view"),
                    row.get("model"),
                    row.get("task_count"),
                    row.get("mean_score"),
                    row.get("score_rank"),
                    row.get("borda_score"),
                    row.get("borda_rank"),
                    row.get("active_parameters"),
                    row.get("total_parameters"),
                    row.get("max_seq_length"),
                    row.get("dtype"),
                    row.get("attn_implementation"),
                    row.get("torch_version"),
                    row.get("transformers_version"),
                    row.get("sentence_transformers_version"),
                )
                for row in score_rows
            ],
        )
        con.execute(
            """
            CREATE TABLE borda_task_scores (
                view_name VARCHAR, model_name VARCHAR, benchmark VARCHAR, task_key VARCHAR,
                rank DOUBLE, model_count INTEGER, borda_score DOUBLE, score DOUBLE
            )
            """
        )
        con.executemany(
            "INSERT INTO borda_task_scores VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
            [
                (
                    row.get("view_name"),
                    row.get("model_name"),
                    row.get("benchmark"),
                    row.get("task_key"),
                    row.get("rank"),
                    row.get("model_count"),
                    row.get("borda_score"),
                    row.get("score"),
                )
                for row in borda_rows
            ],
        )
    finally:
        con.close()


def write_html(html_output: Path, *, duckdb_path: Path, rows: list[TaskResult], runs: list[dict[str, Any]], standings: dict[str, list[dict[str, Any]]]) -> None:
    html_output.parent.mkdir(parents=True, exist_ok=True)
    generated_at = datetime.now(timezone.utc).isoformat()
    data = {
        "generatedAt": generated_at,
        "duckdbPath": str(duckdb_path),
        "views": standings,
        "summary": {
            "taskResults": len(rows),
            "runs": len(runs),
            "completeModels": len(standings.get("Overall", [])),
            "benchmarks": [
                {"name": name, "tasks": len({row.task_key for row in rows if row.benchmark == name})}
                for name in TARGET_BENCHMARKS
            ],
            "skipped": [],
        },
    }
    data_json = json.dumps(data, ensure_ascii=False)
    html_output.write_text(render_html(data_json=data_json), encoding="utf-8")


def render_html(*, data_json: str) -> str:
    return f"""<!doctype html>
<html lang="ja">
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <title>Nano IR Benchmark Borda Report</title>
  <script src="https://cdn.jsdelivr.net/npm/@tailwindcss/browser@4"></script>
  <link rel="icon" href="/favicon.svg" type="image/svg+xml" />
</head>
<body class="bg-stone-50 text-stone-900 dark:bg-stone-950 dark:text-stone-100">
  <main class="mx-auto max-w-[1600px] px-5 py-8">
    <header class="mb-7 border-b border-stone-200 pb-5 dark:border-stone-800">
      <p class="text-sm font-medium text-sky-700 dark:text-sky-300">Nano IR benchmark report</p>
      <h1 class="mt-2 text-2xl font-semibold tracking-normal text-stone-950 dark:text-stone-50">Nano benchmark sortable Borda score matrix</h1>
      <p class="mt-3 max-w-5xl text-sm leading-6 text-stone-700 dark:text-stone-300">Completed benchmark results are loaded into DuckDB and summarized by Overall and each Nano benchmark group. Tables are sorted by Borda Score by default. Click any column heading to sort.</p>
    </header>

    <section class="mb-5 grid gap-3 sm:grid-cols-2 lg:grid-cols-4">
      <div class="border border-stone-200 bg-white p-4 dark:border-stone-800 dark:bg-stone-900">
        <div class="text-xs uppercase tracking-wide text-stone-500 dark:text-stone-400">Complete models</div>
        <div id="complete-models" class="mt-1 text-2xl font-semibold tabular-nums"></div>
      </div>
      <div class="border border-stone-200 bg-white p-4 dark:border-stone-800 dark:bg-stone-900">
        <div class="text-xs uppercase tracking-wide text-stone-500 dark:text-stone-400">Task results</div>
        <div id="task-results" class="mt-1 text-2xl font-semibold tabular-nums"></div>
      </div>
      <div class="border border-stone-200 bg-white p-4 dark:border-stone-800 dark:bg-stone-900">
        <div class="text-xs uppercase tracking-wide text-stone-500 dark:text-stone-400">DuckDB</div>
        <div id="duckdb-path" class="mt-1 text-sm font-medium tabular-nums"></div>
      </div>
      <div class="border border-stone-200 bg-white p-4 dark:border-stone-800 dark:bg-stone-900">
        <div class="text-xs uppercase tracking-wide text-stone-500 dark:text-stone-400">Generated UTC</div>
        <div id="generated-at" class="mt-1 text-sm font-medium tabular-nums"></div>
      </div>
    </section>

    <section class="mb-5">
      <div id="benchmark-chips" class="flex flex-wrap gap-2"></div>
    </section>

    <section class="mb-5">
      <div id="view-buttons" class="flex flex-wrap gap-2"></div>
    </section>

    <section class="mb-8">
      <div class="mb-3 flex flex-wrap items-end justify-between gap-3">
        <div>
          <h2 id="view-title" class="text-lg font-semibold text-stone-950 dark:text-stone-50"></h2>
          <p id="view-summary" class="mt-1 text-sm text-stone-600 dark:text-stone-400"></p>
        </div>
      </div>
      <div class="overflow-x-auto border border-stone-200 bg-white dark:border-stone-800 dark:bg-stone-950">
        <table id="ranked-table" class="min-w-full border-collapse">
          <thead id="table-head"></thead>
          <tbody id="table-body"></tbody>
        </table>
      </div>
    </section>

    <section class="border border-stone-200 bg-white p-4 text-sm leading-6 text-stone-700 dark:border-stone-800 dark:bg-stone-900 dark:text-stone-300">
      <h2 class="mb-2 text-base font-semibold text-stone-950 dark:text-stone-50">Definitions</h2>
      <p>Mean nDCG@10 is the average task score multiplied by 100. Borda Score is computed per task from score rank: <span class="font-mono text-stone-900 dark:text-stone-100">100 * (N - rank) / (N - 1)</span>, then averaged within the selected view. Only models with all tasks in the selected view are included in the ranking.</p>
      <div id="skipped" class="mt-3"></div>
    </section>
  </main>
  <script>
    const REPORT_DATA = {data_json};
    const columns = [
      {{ key: 'borda_rank', label: 'Borda Rank', type: 'number', direction: 'asc' }},
      {{ key: 'score_rank', label: 'Score Rank', type: 'number', direction: 'asc' }},
      {{ key: 'model', label: 'Model', type: 'text', direction: 'asc' }},
      {{ key: 'borda_score', label: 'Borda Score', type: 'number', direction: 'desc' }},
      {{ key: 'mean_score', label: 'Mean nDCG@10', type: 'number', direction: 'desc' }},
      {{ key: 'task_count', label: 'Tasks', type: 'number', direction: 'desc' }},
      {{ key: 'active_parameters', label: 'Active Params', type: 'number', direction: 'asc' }},
      {{ key: 'total_parameters', label: 'Total Params', type: 'number', direction: 'asc' }},
      {{ key: 'max_seq_length', label: 'Max Len', type: 'number', direction: 'desc' }},
      {{ key: 'attn_implementation', label: 'Attn', type: 'text', direction: 'asc' }},
      {{ key: 'torch_version', label: 'Torch', type: 'text', direction: 'asc' }},
      {{ key: 'transformers_version', label: 'Transformers', type: 'text', direction: 'asc' }}
    ];
    let currentView = 'Overall';
    let sortState = {{ key: 'borda_score', direction: 'desc' }};

    function fmtNumber(value, digits = 2) {{
      if (value === null || value === undefined || Number.isNaN(Number(value))) return '';
      return Number(value).toFixed(digits);
    }}

    function fmtRank(value) {{
      if (value === null || value === undefined) return '';
      return Number.isInteger(Number(value)) ? String(Number(value)) : Number(value).toFixed(1);
    }}

    function fmtParams(value) {{
      if (!value) return '';
      const n = Number(value);
      if (n >= 1_000_000_000) return (n / 1_000_000_000).toFixed(2) + 'B';
      if (n >= 1_000_000) return (n / 1_000_000).toFixed(1) + 'M';
      return n.toLocaleString();
    }}

    function cellValue(row, key) {{
      const value = row[key];
      if (value === null || value === undefined) return '';
      return value;
    }}

    function compareRows(a, b, column) {{
      const av = cellValue(a, column.key);
      const bv = cellValue(b, column.key);
      const aMissing = av === '';
      const bMissing = bv === '';
      if (aMissing && bMissing) return 0;
      if (aMissing) return 1;
      if (bMissing) return -1;
      let result;
      if (column.type === 'number') result = Number(av) - Number(bv);
      else result = String(av).toLocaleLowerCase().localeCompare(String(bv).toLocaleLowerCase(), 'ja');
      return sortState.direction === 'asc' ? result : -result;
    }}

    function renderSummary() {{
      document.getElementById('complete-models').textContent = REPORT_DATA.summary.completeModels;
      document.getElementById('task-results').textContent = REPORT_DATA.summary.taskResults.toLocaleString();
      document.getElementById('duckdb-path').textContent = REPORT_DATA.duckdbPath;
      document.getElementById('generated-at').textContent = REPORT_DATA.generatedAt;
      const chips = document.getElementById('benchmark-chips');
      chips.innerHTML = '';
      REPORT_DATA.summary.benchmarks.forEach((item) => {{
        const chip = document.createElement('span');
        chip.className = 'inline-flex items-center gap-1 border border-stone-300 bg-white px-2 py-1 text-xs text-stone-700 dark:border-stone-700 dark:bg-stone-900 dark:text-stone-300';
        chip.innerHTML = `<span>${{escapeHtml(item.name)}}</span><span class="font-mono text-stone-500 dark:text-stone-400">${{item.tasks}}</span>`;
        chips.appendChild(chip);
      }});
      const skipped = document.getElementById('skipped');
      skipped.innerHTML = REPORT_DATA.summary.skipped.length
        ? '<h3 class="mb-1 font-semibold text-stone-950 dark:text-stone-50">Skipped FA2 models</h3>' +
          REPORT_DATA.summary.skipped.map((item) => `<p><span class="font-medium">${{escapeHtml(item.model)}}</span>: ${{escapeHtml(item.reason)}}</p>`).join('')
        : '';
    }}

    function renderButtons() {{
      const container = document.getElementById('view-buttons');
      container.innerHTML = '';
      Object.keys(REPORT_DATA.views).forEach((view) => {{
        const button = document.createElement('button');
        button.type = 'button';
        button.className = view === currentView
          ? 'border border-sky-700 bg-sky-100 px-3 py-1.5 text-sm font-medium text-sky-900 dark:border-sky-300 dark:bg-sky-950 dark:text-sky-100'
          : 'border border-stone-300 bg-white px-3 py-1.5 text-sm text-stone-700 hover:border-sky-500 hover:text-sky-700 dark:border-stone-700 dark:bg-stone-900 dark:text-stone-300 dark:hover:border-sky-400 dark:hover:text-sky-300';
        button.textContent = view;
        button.addEventListener('click', () => {{
          currentView = view;
          sortState = {{ key: 'borda_score', direction: 'desc' }};
          render();
        }});
        container.appendChild(button);
      }});
    }}

    function renderTable() {{
      const head = document.getElementById('table-head');
      const body = document.getElementById('table-body');
      head.innerHTML = '';
      body.innerHTML = '';
      const tr = document.createElement('tr');
      columns.forEach((column) => {{
        const th = document.createElement('th');
        th.scope = 'col';
        const align = column.type === 'number' ? 'text-right' : 'text-left';
        th.className = `sticky top-0 z-10 bg-stone-100 px-3 py-2 text-xs font-semibold uppercase tracking-wide text-stone-600 dark:bg-stone-900 dark:text-stone-300 ${{align}}`;
        const button = document.createElement('button');
        button.type = 'button';
        button.className = `inline-flex w-full items-center gap-1 hover:text-sky-700 dark:hover:text-sky-300 ${{column.type === 'number' ? 'justify-end' : 'justify-start'}}`;
        button.textContent = column.label;
        const indicator = document.createElement('span');
        indicator.className = 'text-stone-400';
        indicator.textContent = sortState.key === column.key ? (sortState.direction === 'asc' ? '▲' : '▼') : '';
        button.appendChild(indicator);
        button.addEventListener('click', () => {{
          if (sortState.key === column.key) {{
            sortState.direction = sortState.direction === 'asc' ? 'desc' : 'asc';
          }} else {{
            sortState = {{ key: column.key, direction: column.direction }};
          }}
          renderTable();
        }});
        th.appendChild(button);
        tr.appendChild(th);
      }});
      head.appendChild(tr);

      const sortColumn = columns.find((column) => column.key === sortState.key) || columns[3];
      const rows = [...REPORT_DATA.views[currentView]].sort((a, b) => compareRows(a, b, sortColumn));
      rows.forEach((row) => {{
        const tr = document.createElement('tr');
        tr.className = 'border-b border-stone-200 odd:bg-white even:bg-stone-50 dark:border-stone-800 dark:odd:bg-stone-950 dark:even:bg-stone-900';
        columns.forEach((column) => {{
          const td = document.createElement('td');
          const align = column.type === 'number' ? 'text-right tabular-nums' : 'text-left';
          td.className = `whitespace-nowrap px-3 py-2 text-sm text-stone-700 dark:text-stone-300 ${{align}}`;
          if (column.key === 'model') td.className += ' font-medium text-stone-900 dark:text-stone-100';
          const value = row[column.key];
          if (column.key.endsWith('_rank')) td.textContent = fmtRank(value);
          else if (column.key === 'borda_score' || column.key === 'mean_score') td.textContent = fmtNumber(value);
          else if (column.key === 'active_parameters' || column.key === 'total_parameters') td.textContent = fmtParams(value);
          else if (column.type === 'number') td.textContent = value ?? '';
          else td.textContent = value ?? '';
          tr.appendChild(td);
        }});
        body.appendChild(tr);
      }});
    }}

    function render() {{
      renderButtons();
      const rows = REPORT_DATA.views[currentView];
      document.getElementById('view-title').textContent = currentView + ' ranked models';
      document.getElementById('view-summary').textContent = `${{rows.length}} complete models, default sorted by Borda Score`;
      renderTable();
    }}

    function escapeHtml(value) {{
      return String(value).replace(/[&<>"']/g, (char) => ({{'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}}[char]));
    }}

    renderSummary();
    render();
  </script>
</body>
</html>
"""


def mean(values: Any) -> float:
    vals = list(values)
    return sum(vals) / len(vals) if vals else 0.0


def _int_or_none(value: Any) -> int | None:
    return int(value) if isinstance(value, int | float) else None


def _float_or_none(value: Any) -> float | None:
    return float(value) if isinstance(value, int | float) else None


def _dataset_revision_value(value: Any, *, key: str) -> str | None:
    if isinstance(value, dict):
        item = value.get(key)
        return str(item) if item is not None else None
    if key == "resolved" and value is not None:
        return str(value)
    return None


if __name__ == "__main__":
    main()
