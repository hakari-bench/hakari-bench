from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

from nano_ir_benchmark.bm25 import (
    BM25BuildResult,
    bm25_config_name,
    bm25_config_from_args,
    collect_bm25_metadata,
    run_or_load_bm25_task,
)
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
    safe_path_part,
    write_all_payload,
)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Nano IR benchmark runner")
    subparsers = parser.add_subparsers(dest="command", required=True)

    evaluate = subparsers.add_parser("evaluate", help="Evaluate a model on Nano-style IR datasets.")
    evaluate.add_argument("--model", default=None, help="Hugging Face model id or local model path.")
    evaluate.add_argument(
        "--model-type",
        default="dense",
        choices=["dense", "sparse", "reranker", "late-interaction", "bm25"],
    )
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
    _add_bm25_args(evaluate)

    build_bm25 = subparsers.add_parser("build-bm25", help="Build BM25 candidate files for Nano-style datasets.")
    build_bm25.add_argument(
        "--dataset",
        action="append",
        default=None,
        help="Dataset name/id. Repeat or pass comma-separated values.",
    )
    build_bm25.add_argument("--collection", action="append", default=[], help="Dataset collection name.")
    build_bm25.add_argument("--split", action="append", default=[], help="Split/task name. Repeat or comma-separate.")
    build_bm25.add_argument("--output-dir", default="output/bm25")
    build_bm25.add_argument("--override", action="store_true")
    build_bm25.add_argument("--show-progress", action="store_true")
    _add_bm25_args(build_bm25)
    return parser


def _add_bm25_args(parser: argparse.ArgumentParser) -> None:
    parser.add_argument("--top-k", type=int, default=100, help="Number of BM25 candidates per query.")
    parser.add_argument(
        "--bm25-tokenizer",
        default="regex",
        choices=[
            "regex",
            "whitespace",
            "transformer",
            "stemmer",
            "english_regex",
            "english_porter",
            "english_porter_stop",
        ],
    )
    parser.add_argument("--bm25-tokenizer-name", default=None)
    parser.add_argument("--bm25-stemmer-algorithm", default="english")
    parser.add_argument("--bm25-k1", type=float, default=1.5)
    parser.add_argument("--bm25-b", type=float, default=0.75)


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = build_parser()
    args = parser.parse_args(argv)
    if args.command == "evaluate" and args.dataset is None and not args.collection:
        args.dataset = ["sentence-transformers/NanoBEIR-en"]
    elif args.command == "evaluate" and args.dataset is None:
        args.dataset = []
    if args.command == "evaluate" and args.model_type == "bm25" and args.model is None:
        args.model = f"bm25/{bm25_config_name(bm25_config_from_args(args))}"
    if args.command == "evaluate" and args.model_type != "bm25" and args.model is None:
        parser.error("--model is required unless --model-type bm25 is used.")
    if args.command == "build-bm25" and args.dataset is None and not args.collection:
        args.dataset = ["sentence-transformers/NanoBEIR-en"]
    elif args.command == "build-bm25" and args.dataset is None:
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
    if args.model_type == "bm25":
        model_metadata = collect_bm25_metadata(args)
    elif pending_tasks:
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
        if model is None and args.model_type != "bm25":
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


def run_build_bm25(args: argparse.Namespace) -> dict[str, Any]:
    registry = DatasetRegistry.load_builtin()
    tasks = resolve_eval_tasks(
        registry=registry,
        dataset_values=args.dataset,
        collection_values=args.collection,
        split_values=args.split,
    )
    config = bm25_config_from_args(args)
    results: list[BM25BuildResult] = []
    for task in tasks:
        dataset = _load_dataset_for_args(args, task)
        results.append(run_or_load_bm25_task(task=task, dataset=dataset, args=args, config=config))

    payload = {
        "generated_at_utc": results[-1].payload.get("generated_at_utc") if results else None,
        "output_dir": args.output_dir,
        "config": {
            "bm25": vars(args),
        },
        "totals": {
            "split_count": len(results),
            "cache_hit_count": sum(1 for result in results if result.cache_hit),
            "evaluated_count": sum(1 for result in results if not result.cache_hit),
        },
        "splits": [
            {
                "dataset_name": result.task.dataset_name,
                "dataset_id": result.task.dataset_id,
                "split_name": result.task.split_name,
                "task_name": result.task.task_name,
                "cache_hit": result.cache_hit,
                "result_path": str(result.output_path),
            }
            for result in results
        ],
    }
    config_name = safe_path_part(bm25_config_name(config))
    all_path = Path(args.output_dir) / config_name / "all.json"
    all_path.parent.mkdir(parents=True, exist_ok=True)
    all_path.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
    print(
        json.dumps(
            {
                "all_json": str(all_path),
                "evaluated_count": payload["totals"]["evaluated_count"],
                "cache_hit_count": payload["totals"]["cache_hit_count"],
            },
            ensure_ascii=False,
            indent=2,
        )
    )
    return payload


def _load_dataset_for_args(args: argparse.Namespace, task: EvalTask) -> LoadedIrDataset:
    candidate_subset_name = args.candidate_subset_name if getattr(args, "model_type", None) == "reranker" else None
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
    if args.command == "build-bm25":
        run_build_bm25(args)
        return
    raise ValueError(f"Unsupported command: {args.command}")


if __name__ == "__main__":
    main()
