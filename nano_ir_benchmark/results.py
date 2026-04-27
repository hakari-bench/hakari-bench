from __future__ import annotations

import json
import re
import time
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Callable

import numpy as np

from nano_ir_benchmark.bm25 import bm25_config_from_args, evaluate_bm25_task
from nano_ir_benchmark.datasets import EvalTask
from nano_ir_benchmark.evaluation import LoadedIrDataset, evaluate_dense_task, evaluate_reranker_task

TIMING_KEYS = [
    "query_embedding_seconds",
    "corpus_embedding_seconds",
    "score_and_topk_seconds",
    "metric_compute_seconds",
    "pure_compute_seconds",
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

    dataset = dataset_loader(task)
    started_at = datetime.now(timezone.utc)
    start = time.perf_counter()
    if args.model_type == "bm25":
        evaluation = evaluate_bm25_task(
            dataset=dataset,
            config=bm25_config_from_args(args),
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
            truncate_dim=args.truncate_dim,
        )
    elapsed = time.perf_counter() - start
    finished_at = datetime.now(timezone.utc)

    aggregate_metric_value = aggregate_metric_value_for(evaluation.metrics, args.aggregate_metric)
    payload = {
        "generated_at_utc": datetime.now(timezone.utc).isoformat(),
        "model": model_metadata,
        "environment": environment,
        "target": {
            "dataset_name": task.dataset_name,
            "dataset_id": task.dataset_id,
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
            "truncate_dim": args.truncate_dim,
            "candidate_subset_name": args.candidate_subset_name if args.model_type == "reranker" else None,
            "rerank_top_n": args.rerank_top_n if args.model_type == "reranker" else None,
        },
        "evaluation": {
            "started_at_utc": started_at.isoformat(),
            "finished_at_utc": finished_at.isoformat(),
            "evaluated_at_utc": finished_at.isoformat(),
            "duration_seconds_excluding_dataset_load": float(evaluation.timing.get("pure_compute_seconds", elapsed)),
            "wall_seconds": float(elapsed),
            "aggregate_metric": args.aggregate_metric,
            "aggregate_metric_value": aggregate_metric_value,
            "cache_hit": False,
            "timing": evaluation.timing,
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
) -> dict[str, Any]:
    aggregate_values: list[float] = []
    timing_all = {key: 0.0 for key in TIMING_KEYS}
    timing_this_run = {key: 0.0 for key in TIMING_KEYS}
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
        splits.append(
            {
                "dataset_name": result.task.dataset_name,
                "dataset_id": result.task.dataset_id,
                "split_name": result.task.split_name,
                "task_name": result.task.task_name,
                "cache_hit": result.cache_hit,
                "result_path": str(result.output_path),
                "aggregate_metric": evaluation.get("aggregate_metric"),
                "aggregate_metric_value": aggregate_value,
                "evaluated_at_utc": evaluation.get("evaluated_at_utc"),
            }
        )
    splits.sort(key=lambda item: (str(item["dataset_id"]), str(item["task_name"])))
    return {
        "generated_at_utc": datetime.now(timezone.utc).isoformat(),
        "model": model_metadata,
        "environment": environment,
        "cli_args": vars(args),
        "aggregate_metric": args.aggregate_metric,
        "totals": {
            "target_count": len({entry["dataset_id"] for entry in splits}),
            "split_count": len(splits),
            "cache_hit_count": sum(1 for result in results if result.cache_hit),
            "evaluated_count": sum(1 for result in results if not result.cache_hit),
            "aggregate_metric_mean": float(np.mean(aggregate_values)) if aggregate_values else None,
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
