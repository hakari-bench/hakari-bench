from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

from nano_ir_benchmark.datasets import DatasetRegistry, EvalTask, resolve_eval_tasks
from nano_ir_benchmark.evaluation import LoadedIrDataset, load_ir_dataset
from nano_ir_benchmark.models import (
    ModelLoadConfig,
    collect_model_metadata,
    collect_runtime_environment,
    load_model,
)
from nano_ir_benchmark.results import (
    TaskRunResult,
    build_all_payload,
    result_path_for_task,
    run_or_load_task,
    write_all_payload,
)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Nano IR benchmark runner")
    subparsers = parser.add_subparsers(dest="command", required=True)

    evaluate = subparsers.add_parser("evaluate", help="Evaluate a model on Nano-style IR datasets.")
    evaluate.add_argument("--model", required=True, help="Hugging Face model id or local model path.")
    evaluate.add_argument("--model-type", default="dense", choices=["dense", "sparse", "reranker", "late-interaction"])
    evaluate.add_argument("--dtype", default="bf16", choices=["bf16", "fp16", "fp32"])
    evaluate.add_argument("--attn-implementation", default=None)
    evaluate.add_argument("--flash-attn2", action="store_true")
    evaluate.add_argument("--device", default=None)
    evaluate.add_argument("--trust-remote-code", action="store_true")
    evaluate.add_argument("--model-max-seq-length", type=int, default=None)
    evaluate.add_argument("--truncate-dim", type=int, default=None)

    evaluate.add_argument(
        "--dataset",
        action="append",
        default=None,
        help="Dataset name/id. Repeat or pass comma-separated values.",
    )
    evaluate.add_argument("--collection", action="append", default=[], help="Dataset collection name.")
    evaluate.add_argument("--split", action="append", default=[], help="Split/task name. Repeat or comma-separate.")

    evaluate.add_argument("--batch-size", type=int, default=32)
    evaluate.add_argument("--show-progress", action="store_true")
    evaluate.add_argument("--query-prompt", default=None)
    evaluate.add_argument("--corpus-prompt", default=None)
    evaluate.add_argument("--query-prompt-name", default=None)
    evaluate.add_argument("--corpus-prompt-name", default=None)
    evaluate.add_argument("--candidate-subset-name", default="bm25")
    evaluate.add_argument("--rerank-top-n", type=int, default=100)
    evaluate.add_argument("--output-dir", default="output/results")
    evaluate.add_argument("--override", action="store_true")
    evaluate.add_argument("--aggregate-metric", default="ndcg@10")
    return parser


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    args = build_parser().parse_args(argv)
    if args.command == "evaluate" and args.dataset is None and not args.collection:
        args.dataset = ["sentence-transformers/NanoBEIR-en"]
    elif args.command == "evaluate" and args.dataset is None:
        args.dataset = []
    return args


def run_evaluate(args: argparse.Namespace) -> dict[str, Any]:
    registry = DatasetRegistry.load_builtin()
    tasks = resolve_eval_tasks(
        registry=registry,
        dataset_values=args.dataset,
        collection_values=args.collection,
        split_values=args.split,
    )
    output_dir = Path(args.output_dir)
    pending_tasks = [
        task
        for task in tasks
        if args.override or not result_path_for_task(output_dir=output_dir, model_name_or_path=args.model, task=task).exists()
    ]
    environment = collect_runtime_environment()

    model: Any | None = None
    if pending_tasks:
        model = load_model(
            ModelLoadConfig(
                model_name_or_path=args.model,
                model_type=args.model_type,
                dtype=args.dtype,
                attn_implementation=args.attn_implementation,
                flash_attn2=args.flash_attn2,
                device=args.device,
                trust_remote_code=args.trust_remote_code,
                max_seq_length=args.model_max_seq_length,
            )
        )
        model_metadata = collect_model_metadata(model, args)
    else:
        model_metadata = {
            "model_type": args.model_type,
            "name_or_path": args.model,
            "device": args.device,
            "dtype": args.dtype,
            "trust_remote_code": args.trust_remote_code,
            "total_parameters": None,
            "trainable_parameters": None,
            "active_parameters": None,
        }

    results: list[TaskRunResult] = []
    for task in tasks:
        if model is None and result_path_for_task(output_dir=output_dir, model_name_or_path=args.model, task=task).exists():
            results.append(_load_cached_task(args=args, task=task))
            continue
        if model is None:
            raise RuntimeError("Internal error: model was not loaded for a pending task.")
        results.append(
            run_or_load_task(
                task=task,
                model=model,
                args=args,
                environment=environment,
                model_metadata=model_metadata,
                dataset_loader=lambda eval_task: _load_dataset_for_args(args, eval_task),
            )
        )

    if not pending_tasks and results and isinstance(results[0].payload.get("model"), dict):
        model_metadata = results[0].payload["model"]

    all_payload = build_all_payload(args=args, environment=environment, model_metadata=model_metadata, results=results)
    all_path = write_all_payload(output_dir=output_dir, model_name_or_path=args.model, payload=all_payload)
    print(
        json.dumps(
            {
                "aggregate_metric": args.aggregate_metric,
                "aggregate_metric_mean": all_payload["totals"]["aggregate_metric_mean"],
                "all_json": str(all_path),
                "evaluated_count": all_payload["totals"]["evaluated_count"],
                "cache_hit_count": all_payload["totals"]["cache_hit_count"],
            },
            ensure_ascii=False,
            indent=2,
        )
    )
    return all_payload


def _load_dataset_for_args(args: argparse.Namespace, task: EvalTask) -> LoadedIrDataset:
    candidate_subset_name = args.candidate_subset_name if args.model_type == "reranker" else None
    return load_ir_dataset(task, candidate_subset_name=candidate_subset_name)


def _load_cached_task(*, args: argparse.Namespace, task: EvalTask) -> TaskRunResult:
    output_path = result_path_for_task(output_dir=Path(args.output_dir), model_name_or_path=args.model, task=task)
    return TaskRunResult(
        task=task,
        cache_hit=True,
        output_path=output_path,
        payload=json.loads(output_path.read_text(encoding="utf-8")),
    )


def main(argv: list[str] | None = None) -> None:
    args = parse_args(argv)
    if args.command == "evaluate":
        run_evaluate(args)
        return
    raise ValueError(f"Unsupported command: {args.command}")


if __name__ == "__main__":
    main()
