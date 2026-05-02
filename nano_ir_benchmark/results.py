from __future__ import annotations

import json
import re
import time
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Callable

import numpy as np

from nano_ir_benchmark.bm25 import (
    bm25_config_from_args,
    bm25_config_payload,
    collect_bm25_metadata,
    evaluate_bm25_task,
    resolve_bm25_config_for_queries,
)
from nano_ir_benchmark.datasets import EvalTask, resolve_dataset_revision
from nano_ir_benchmark.evaluation import LoadedIrDataset, evaluate_dense_task, evaluate_reranker_task

TIMING_KEYS = [
    "query_embedding_seconds",
    "corpus_embedding_seconds",
    "score_and_topk_seconds",
    "metric_compute_seconds",
    "embedding_variant_score_and_topk_seconds",
    "embedding_variant_metric_compute_seconds",
    "pure_compute_seconds",
]
AGGREGATED_CONFIG_KEYS = [
    "batch_size",
    "aggregate_metric",
    "query_prompt",
    "corpus_prompt",
    "query_prompt_name",
    "corpus_prompt_name",
    "query_task",
    "corpus_task",
]
PROMPT_CONFIG_KEYS = [
    "query_prompt",
    "corpus_prompt",
    "query_prompt_name",
    "corpus_prompt_name",
    "query_task",
    "corpus_task",
]


@dataclass(frozen=True)
class TaskRunResult:
    task: EvalTask
    cache_hit: bool
    output_path: Path
    payload: dict[str, Any]


def safe_path_part(value: str) -> str:
    normalized = value.strip().strip("/\\").replace("\\", "/")
    normalized = normalized.replace("/", "__")
    normalized = re.sub(r"[^A-Za-z0-9._-]+", "_", normalized)
    normalized = normalized.strip("._")
    return normalized or "value"


def result_path_for_task(*, output_dir: Path, model_name_or_path: str, task: EvalTask) -> Path:
    return (
        output_dir
        / safe_path_part(model_name_or_path)
        / safe_path_part(task.dataset_id)
        / f"{safe_path_part(task.task_name)}.json"
    )


def model_output_dir(*, output_dir: Path, model_name_or_path: str) -> Path:
    return output_dir / safe_path_part(model_name_or_path)


def run_or_load_task(
    *,
    task: EvalTask,
    model: Any,
    args: Any,
    environment: dict[str, Any],
    model_metadata: dict[str, Any],
    dataset_loader: Callable[[EvalTask], LoadedIrDataset],
) -> TaskRunResult:
    output_path = result_path_for_task(output_dir=Path(args.output_dir), model_name_or_path=args.model, task=task)
    if output_path.exists() and not args.override:
        return TaskRunResult(
            task=task,
            cache_hit=True,
            output_path=output_path,
            payload=json.loads(output_path.read_text(encoding="utf-8")),
        )

    total_start = time.perf_counter()
    dataset_load_started_at = datetime.now(timezone.utc)
    dataset_load_start = time.perf_counter()
    dataset = dataset_loader(task)
    dataset_load_seconds = time.perf_counter() - dataset_load_start
    dataset_load_finished_at = datetime.now(timezone.utc)
    started_at = datetime.now(timezone.utc)
    start = time.perf_counter()
    bm25_payload: dict[str, Any] | None = None
    payload_model_metadata = model_metadata
    if args.model_type == "bm25":
        raw_bm25_config = bm25_config_from_args(args)
        bm25_source = "dataset_candidate_subset" if dataset.candidates is not None else "computed_bm25s"
        bm25_candidate_subset_name = (
            args.candidate_subset_name if dataset.candidates is not None else None
        )
        bm25_config = (
            raw_bm25_config
            if dataset.candidates is not None
            else resolve_bm25_config_for_queries(raw_bm25_config, dataset.queries)
        )
        bm25_payload = bm25_config_payload(
            bm25_config,
            source=bm25_source,
            candidate_subset_name=bm25_candidate_subset_name,
        )
        payload_model_metadata = collect_bm25_metadata(
            args,
            config=bm25_config,
            source=bm25_source,
            candidate_subset_name=bm25_candidate_subset_name,
        )
        evaluation = evaluate_bm25_task(
            dataset=dataset,
            config=bm25_config,
        )
    elif args.model_type == "reranker":
        evaluation = evaluate_reranker_task(
            model=model,
            dataset=dataset,
            batch_size=args.batch_size,
            show_progress=args.show_progress,
            rerank_top_n=args.rerank_top_n,
        )
    else:
        evaluation = evaluate_dense_task(
            model=model,
            dataset=dataset,
            batch_size=args.batch_size,
            show_progress=args.show_progress,
            query_prompt=args.query_prompt,
            corpus_prompt=args.corpus_prompt,
            query_prompt_name=args.query_prompt_name,
            corpus_prompt_name=args.corpus_prompt_name,
            query_task=getattr(args, "query_task", None),
            corpus_task=getattr(args, "corpus_task", None),
            truncate_dim=args.truncate_dim,
            embedding_variants=getattr(args, "embedding_variants", []),
            aggregate_metric=args.aggregate_metric,
        )
    elapsed = time.perf_counter() - start
    finished_at = datetime.now(timezone.utc)
    total_elapsed = time.perf_counter() - total_start

    aggregate_metric_value = aggregate_metric_value_for(evaluation.metrics, args.aggregate_metric)
    dataset_revision = resolve_dataset_revision(
        task.dataset_id,
        requested_revision=getattr(args, "dataset_revision", None),
    )
    payload = {
        "generated_at_utc": datetime.now(timezone.utc).isoformat(),
        "model": payload_model_metadata,
        "environment": environment,
        "target": {
            "dataset_name": task.dataset_name,
            "dataset_id": task.dataset_id,
            "dataset_revision": dataset_revision,
            "split_name": task.split_name,
            "task_name": task.task_name,
            "corpus_config": task.dataset.corpus_config,
            "queries_config": task.dataset.queries_config,
            "qrels_config": task.dataset.qrels_config,
            "candidate_config": task.dataset.candidate_config,
        },
        "config": {
            "batch_size": args.batch_size,
            "aggregate_metric": args.aggregate_metric,
            "show_progress": args.show_progress,
            "query_prompt": args.query_prompt,
            "corpus_prompt": args.corpus_prompt,
            "query_prompt_name": args.query_prompt_name,
            "corpus_prompt_name": args.corpus_prompt_name,
            "query_task": getattr(args, "query_task", None),
            "corpus_task": getattr(args, "corpus_task", None),
            "truncate_dim": args.truncate_dim,
            "embedding_variants": getattr(args, "embedding_variants", []),
            "dataset_revision": getattr(args, "dataset_revision", None),
            "candidate_subset_name": args.candidate_subset_name if args.model_type in {"bm25", "reranker"} else None,
            "rerank_top_n": args.rerank_top_n if args.model_type == "reranker" else None,
            "bm25": bm25_payload,
        },
        "evaluation": {
            "dataset_load_started_at_utc": dataset_load_started_at.isoformat(),
            "dataset_load_finished_at_utc": dataset_load_finished_at.isoformat(),
            "dataset_load_seconds": float(dataset_load_seconds),
            "started_at_utc": started_at.isoformat(),
            "finished_at_utc": finished_at.isoformat(),
            "evaluated_at_utc": finished_at.isoformat(),
            "duration_seconds_excluding_dataset_load": float(evaluation.timing.get("pure_compute_seconds", elapsed)),
            "duration_seconds_including_dataset_load": float(total_elapsed),
            "wall_seconds": float(elapsed),
            "aggregate_metric": args.aggregate_metric,
            "aggregate_metric_value": aggregate_metric_value,
            "cache_hit": False,
            "timing": evaluation.timing,
            "embedding_conversion": evaluation.embedding_conversion,
            "embedding_evaluations": evaluation.embedding_evaluations,
        },
        "metrics": evaluation.metrics,
    }
    _write_json(output_path, payload)
    return TaskRunResult(task=task, cache_hit=False, output_path=output_path, payload=payload)


def aggregate_metric_value_for(metrics: dict[str, float], suffix: str) -> float:
    suffix = suffix.lower()
    values = [value for key, value in metrics.items() if key.lower().endswith(suffix)]
    if not values:
        raise ValueError(f"No metric ending with '{suffix}' found. Available metrics: {sorted(metrics)}")
    return float(np.mean(values))


def build_all_payload(
    *,
    args: Any,
    environment: dict[str, Any],
    model_metadata: dict[str, Any],
    results: list[TaskRunResult],
    run_started_at_utc: str | None = None,
    run_finished_at_utc: str | None = None,
    run_wall_seconds: float | None = None,
) -> dict[str, Any]:
    aggregate_values: list[float] = []
    timing_all = {key: 0.0 for key in TIMING_KEYS}
    timing_this_run = {key: 0.0 for key in TIMING_KEYS}
    dataset_load_seconds_all = 0.0
    dataset_load_seconds_this_run = 0.0
    duration_excluding_load_all = 0.0
    duration_excluding_load_this_run = 0.0
    duration_including_load_all = 0.0
    duration_including_load_this_run = 0.0
    wall_seconds_all = 0.0
    wall_seconds_this_run = 0.0
    splits: list[dict[str, Any]] = []
    for result in results:
        evaluation = result.payload.get("evaluation", {})
        aggregate_value = evaluation.get("aggregate_metric_value")
        if isinstance(aggregate_value, int | float):
            aggregate_values.append(float(aggregate_value))
        timing = evaluation.get("timing", {})
        if isinstance(timing, dict):
            for key in TIMING_KEYS:
                value = timing.get(key)
                if isinstance(value, int | float):
                    timing_all[key] += float(value)
                    if not result.cache_hit:
                        timing_this_run[key] += float(value)
        dataset_load_seconds = _numeric(evaluation.get("dataset_load_seconds"))
        duration_excluding_load = _numeric(evaluation.get("duration_seconds_excluding_dataset_load"))
        duration_including_load = _numeric(
            evaluation.get("duration_seconds_including_dataset_load"),
            fallback=evaluation.get("wall_seconds"),
        )
        wall_seconds = _numeric(evaluation.get("wall_seconds"))
        dataset_load_seconds_all += dataset_load_seconds or 0.0
        duration_excluding_load_all += duration_excluding_load or 0.0
        duration_including_load_all += duration_including_load or 0.0
        wall_seconds_all += wall_seconds or 0.0
        if not result.cache_hit:
            dataset_load_seconds_this_run += dataset_load_seconds or 0.0
            duration_excluding_load_this_run += duration_excluding_load or 0.0
            duration_including_load_this_run += duration_including_load or 0.0
            wall_seconds_this_run += wall_seconds or 0.0
        splits.append(
            {
                "dataset_name": result.task.dataset_name,
                "dataset_id": result.task.dataset_id,
                "dataset_revision": result.payload.get("target", {}).get("dataset_revision"),
                "split_name": result.task.split_name,
                "task_name": result.task.task_name,
                "cache_hit": result.cache_hit,
                "result_path": str(result.output_path),
                "dataset_load_started_at_utc": evaluation.get("dataset_load_started_at_utc"),
                "dataset_load_finished_at_utc": evaluation.get("dataset_load_finished_at_utc"),
                "started_at_utc": evaluation.get("started_at_utc"),
                "finished_at_utc": evaluation.get("finished_at_utc"),
                "evaluated_at_utc": evaluation.get("evaluated_at_utc"),
                "dataset_load_seconds": dataset_load_seconds,
                "duration_seconds_excluding_dataset_load": duration_excluding_load,
                "duration_seconds_including_dataset_load": duration_including_load,
                "wall_seconds": wall_seconds,
                "aggregate_metric": evaluation.get("aggregate_metric"),
                "aggregate_metric_value": aggregate_value,
                "config": _summarize_split_config(result.payload.get("config")),
                "embedding_conversion": evaluation.get("embedding_conversion"),
                "embedding_evaluations": _summarize_embedding_evaluations(evaluation.get("embedding_evaluations")),
                "bm25": result.payload.get("config", {}).get("bm25"),
            }
        )
    splits.sort(key=lambda item: (str(item["dataset_id"]), str(item["task_name"])))
    generated_at_utc = datetime.now(timezone.utc).isoformat()
    resolved_run_finished_at_utc = run_finished_at_utc or generated_at_utc
    resolved_model_metadata = _consistent_task_model_metadata(results) or model_metadata
    return {
        "generated_at_utc": generated_at_utc,
        "run": {
            "started_at_utc": run_started_at_utc,
            "finished_at_utc": resolved_run_finished_at_utc,
            "evaluated_at_utc": resolved_run_finished_at_utc,
            "wall_seconds": run_wall_seconds,
        },
        "model": resolved_model_metadata,
        "environment": environment,
        "cli_args": vars(args),
        "config": _aggregate_split_configs(args=args, results=results),
        "aggregate_metric": args.aggregate_metric,
        "totals": {
            "target_count": len({entry["dataset_id"] for entry in splits}),
            "split_count": len(splits),
            "cache_hit_count": sum(1 for result in results if result.cache_hit),
            "evaluated_count": sum(1 for result in results if not result.cache_hit),
            "aggregate_metric_mean": float(np.mean(aggregate_values)) if aggregate_values else None,
            "dataset_load_seconds_this_run": dataset_load_seconds_this_run,
            "dataset_load_seconds_all_splits": dataset_load_seconds_all,
            "duration_seconds_excluding_dataset_load_this_run": duration_excluding_load_this_run,
            "duration_seconds_excluding_dataset_load_all_splits": duration_excluding_load_all,
            "duration_seconds_including_dataset_load_this_run": duration_including_load_this_run,
            "duration_seconds_including_dataset_load_all_splits": duration_including_load_all,
            "wall_seconds_this_run": wall_seconds_this_run,
            "wall_seconds_all_splits": wall_seconds_all,
            "timing_seconds_this_run": timing_this_run,
            "timing_seconds_all_splits": timing_all,
        },
        "splits": splits,
    }


def write_all_payload(*, output_dir: Path, model_name_or_path: str, payload: dict[str, Any]) -> Path:
    path = model_output_dir(output_dir=output_dir, model_name_or_path=model_name_or_path) / "all.json"
    _write_json(path, payload)
    return path


def _write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")


def _numeric(value: Any, *, fallback: Any = None) -> float | None:
    if isinstance(value, int | float):
        return float(value)
    if isinstance(fallback, int | float):
        return float(fallback)
    return None


def _summarize_split_config(value: Any) -> dict[str, Any]:
    if not isinstance(value, dict):
        return {}
    return {key: value.get(key) for key in AGGREGATED_CONFIG_KEYS}


def _aggregate_split_configs(*, args: Any, results: list[TaskRunResult]) -> dict[str, Any]:
    summaries = {key: _summarize_config_value(results, key) for key in AGGREGATED_CONFIG_KEYS}
    payload = {
        "source": "per_split_result_config",
        "batch_size": _representative_config_value(summaries["batch_size"], getattr(args, "batch_size", None)),
        "aggregate_metric": _representative_config_value(
            summaries["aggregate_metric"],
            getattr(args, "aggregate_metric", None),
        ),
        "prompt_summary": {key: summaries[key] for key in PROMPT_CONFIG_KEYS},
    }
    for key in PROMPT_CONFIG_KEYS:
        payload[key] = _representative_config_value(summaries[key], getattr(args, key, None))
    return payload


def _representative_config_value(summary: dict[str, Any], fallback: Any) -> Any:
    if summary.get("consistent"):
        return summary.get("value")
    return fallback


def _summarize_config_value(results: list[TaskRunResult], key: str) -> dict[str, Any]:
    values_by_identity: dict[str, dict[str, Any]] = {}
    for result in results:
        config = result.payload.get("config")
        value = config.get(key) if isinstance(config, dict) else None
        identity = json.dumps(value, ensure_ascii=False, sort_keys=True)
        entry = values_by_identity.setdefault(identity, {"value": value, "count": 0})
        entry["count"] += 1
    values = sorted(values_by_identity.values(), key=lambda item: (-int(item["count"]), json.dumps(item["value"], ensure_ascii=False)))
    consistent = len(values) == 1
    return {
        "consistent": consistent,
        "value": values[0]["value"] if consistent and values else None,
        "values": values,
    }


def _summarize_embedding_evaluations(value: Any) -> list[dict[str, Any]]:
    if not isinstance(value, list):
        return []
    summaries: list[dict[str, Any]] = []
    for item in value:
        if not isinstance(item, dict):
            continue
        summaries.append(
            {
                "name": item.get("name"),
                "transform": item.get("transform"),
                "embedding_dimensions": item.get("embedding_dimensions"),
                "embedding_metadata": item.get("embedding_metadata"),
                "aggregate_metric": item.get("aggregate_metric"),
                "aggregate_metric_value": item.get("aggregate_metric_value"),
                "best_score": item.get("best_score"),
                "best_distance": item.get("best_distance"),
                "best_score_name": item.get("best_score_name"),
                "distance_evaluations": _summarize_distance_evaluations(item.get("distance_evaluations")),
            }
        )
    return summaries


def _summarize_distance_evaluations(value: Any) -> list[dict[str, Any]]:
    if not isinstance(value, list):
        return []
    summaries: list[dict[str, Any]] = []
    for item in value:
        if not isinstance(item, dict):
            continue
        summaries.append(
            {
                "distance": item.get("distance"),
                "score_name": item.get("score_name"),
                "aggregate_metric": item.get("aggregate_metric"),
                "aggregate_metric_value": item.get("aggregate_metric_value"),
                "timing": item.get("timing"),
            }
        )
    return summaries


def _consistent_task_model_metadata(results: list[TaskRunResult]) -> dict[str, Any] | None:
    task_models = [result.payload.get("model") for result in results if isinstance(result.payload.get("model"), dict)]
    if not task_models:
        return None
    first = task_models[0]
    if all(model == first for model in task_models):
        return first
    return None
