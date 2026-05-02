from __future__ import annotations

import argparse
import json
import time
from datetime import datetime, timezone
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
from nano_ir_benchmark.embedding_variants import default_dense_quantized_embedding_variants, parse_embedding_variants
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
        "--sparse-max-active-dims",
        type=int,
        default=None,
        help="Limit active sparse dimensions per embedding when using --model-type sparse.",
    )
    evaluate.add_argument(
        "--embedding-variant",
        dest="embedding_variant_values",
        action="append",
        default=[],
        help=(
            "Derived embedding evaluation spec. Repeat or comma-separate. "
            "Current syntax: truncate:DIM, quantize:PRECISION for exact usearch quantized search, "
            "quantize-docs:PRECISION for docs-only quantization, "
            "quantize-both:PRECISION for query+docs quantization, "
            "quantize-code:PRECISION for raw scalar code scoring, "
            "quantize-sample:PRECISION:SAMPLE_SIZE for sample-calibrated scalar quantization, "
            "or usearch[:|-rescore:]PRECISION for exact usearch search. "
            "Quantized variants are supported for dense models only. "
            "Example: --embedding-variant truncate:256,truncate:128 --embedding-variant quantize:int8,ubinary"
        ),
    )
    evaluate.add_argument(
        "--embedding-variant-cross",
        dest="embedding_variant_cross_values",
        action="append",
        nargs="+",
        default=[],
        metavar="SPEC",
        help=(
            "Cross product of derived embedding specs, normalized into pipeline variants. "
            "Example: --embedding-variant-cross truncate:256,128,64 quantize:int8,ubinary"
        ),
    )
    evaluate.add_argument(
        "--no-quantize",
        action="store_true",
        help="Disable automatic dense usearch int8/binary quantized variants.",
    )

    evaluate.add_argument(
        "--dataset",
        action="append",
        default=None,
        help="Dataset name/id. Repeat or pass comma-separated values.",
    )
    evaluate.add_argument("--collection", action="append", default=[], help="Dataset collection name.")
    evaluate.add_argument("--split", action="append", default=[], help="Split/task name. Repeat or comma-separate.")
    evaluate.add_argument("--dataset-revision", default=None, help="Hugging Face dataset revision to evaluate.")

    evaluate.add_argument("--batch-size", type=int, default=32)
    evaluate.add_argument("--show-progress", action="store_true")
    evaluate.add_argument("--query-prompt", default=None)
    evaluate.add_argument("--corpus-prompt", default=None)
    evaluate.add_argument("--query-prompt-name", default=None)
    evaluate.add_argument("--corpus-prompt-name", default=None)
    evaluate.add_argument("--query-task", default=None)
    evaluate.add_argument("--corpus-task", default=None)
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
    build_bm25.add_argument("--dataset-revision", default=None, help="Hugging Face dataset revision to build from.")
    build_bm25.add_argument("--output-dir", default="output/bm25")
    build_bm25.add_argument("--override", action="store_true")
    build_bm25.add_argument("--show-progress", action="store_true")
    _add_bm25_args(build_bm25)

    web = subparsers.add_parser("web", help="Run the Nano IR benchmark result viewer.")
    web.add_argument("--host", default="127.0.0.1", help="Bind host. Use 0.0.0.0 to allow remote access.")
    web.add_argument("--port", type=int, default=8000)
    web.add_argument("--data-dir", default="output/viewer", help="Local viewer data/cache directory.")
    web.add_argument("--duckdb-path", default=None, help="Local DuckDB path. Defaults to DATA_DIR/nano_ir_bench.duckdb.")
    web.add_argument(
        "--source-output-dir",
        default="../nano_ir_bench/output",
        help="Source benchmark output directory containing results/nano_ir_bench.duckdb.",
    )
    web.add_argument("--source-duckdb-path", default=None, help="Explicit source DuckDB path to copy from.")
    web.add_argument("--viewer-config-dir", default="config/viewer", help="Viewer YAML config directory.")
    return parser


def _add_bm25_args(parser: argparse.ArgumentParser) -> None:
    parser.add_argument("--top-k", type=int, default=100, help="Number of BM25 candidates per query.")
    parser.add_argument(
        "--bm25-tokenizer",
        default=None,
        choices=[
            "regex",
            "whitespace",
            "transformer",
            "stemmer",
            "english_regex",
            "english_porter",
            "english_porter_stop",
            "wordseg",
        ],
    )
    parser.add_argument("--bm25-tokenizer-name", default=None)
    parser.add_argument("--bm25-stemmer-algorithm", default="english")
    parser.add_argument("--bm25-k1", type=float, default=1.5)
    parser.add_argument("--bm25-b", type=float, default=0.75)


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = build_parser()
    args = parser.parse_args(argv)
    if args.command == "evaluate":
        has_explicit_embedding_variants = bool(args.embedding_variant_values or args.embedding_variant_cross_values)
        try:
            args.embedding_variants = parse_embedding_variants(
                args.embedding_variant_values,
                args.embedding_variant_cross_values,
            )
        except ValueError as exc:
            parser.error(str(exc))
        if args.model_type == "dense" and not args.no_quantize and not has_explicit_embedding_variants:
            args.embedding_variants = default_dense_quantized_embedding_variants()
        if args.model_type == "sparse" and _embedding_variants_use_quantization(args.embedding_variants):
            parser.error(
                "--model-type sparse does not support quantized embedding variants. "
                "Use sparse max-active-dims variants instead."
            )
        delattr(args, "embedding_variant_values")
        delattr(args, "embedding_variant_cross_values")
    if args.command == "evaluate" and args.sparse_max_active_dims is not None:
        if args.model_type != "sparse":
            parser.error("--sparse-max-active-dims requires --model-type sparse.")
        if args.sparse_max_active_dims <= 0:
            parser.error("--sparse-max-active-dims must be positive.")
    if args.command == "evaluate" and args.dataset is None and not args.collection:
        args.dataset = ["hakari-bench/NanoBEIR-en"]
    elif args.command == "evaluate" and args.dataset is None:
        args.dataset = []
    if args.command == "evaluate" and args.model_type == "bm25" and args.model is None:
        args.model = f"bm25/{bm25_config_name(bm25_config_from_args(args))}"
    if args.command == "evaluate" and args.model_type != "bm25" and args.model is None:
        parser.error("--model is required unless --model-type bm25 is used.")
    if args.command == "build-bm25" and args.dataset is None and not args.collection:
        args.dataset = ["hakari-bench/NanoBEIR-en"]
    elif args.command == "build-bm25" and args.dataset is None:
        args.dataset = []
    return args


def _embedding_variants_use_quantization(variants: list[dict[str, Any]]) -> bool:
    return any(_embedding_variant_uses_quantization(variant) for variant in variants)


def _embedding_variant_uses_quantization(variant: dict[str, Any]) -> bool:
    transform = variant.get("transform")
    if not isinstance(transform, dict):
        return False
    if transform.get("type") == "quantize":
        return True
    steps = transform.get("steps")
    if not isinstance(steps, list):
        return False
    return any(isinstance(step, dict) and step.get("type") == "quantize" for step in steps)


def run_evaluate(args: argparse.Namespace) -> dict[str, Any]:
    run_started_at = datetime.now(timezone.utc)
    run_start = time.perf_counter()
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

    run_finished_at = datetime.now(timezone.utc)
    all_payload = build_all_payload(
        args=args,
        environment=environment,
        model_metadata=model_metadata,
        results=results,
        run_started_at_utc=run_started_at.isoformat(),
        run_finished_at_utc=run_finished_at.isoformat(),
        run_wall_seconds=float(time.perf_counter() - run_start),
    )
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
                "dataset_revision": result.payload.get("target", {}).get("dataset_revision"),
                "split_name": result.task.split_name,
                "task_name": result.task.task_name,
                "cache_hit": result.cache_hit,
                "result_path": str(result.output_path),
                "bm25": result.payload.get("config"),
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


def run_web(args: argparse.Namespace) -> None:
    from nano_ir_benchmark.viewer.app import create_app
    from nano_ir_benchmark.viewer.store import LocalDuckDbStore, resolve_duckdb_location

    import uvicorn

    location = resolve_duckdb_location(
        data_dir=Path(args.data_dir),
        duckdb_path=Path(args.duckdb_path) if args.duckdb_path else None,
        source_output_dir=Path(args.source_output_dir) if args.source_output_dir else None,
        source_duckdb_path=Path(args.source_duckdb_path) if args.source_duckdb_path else None,
    )
    store = LocalDuckDbStore(location)
    store.ensure_current()
    app = create_app(store=store, config_dir=Path(args.viewer_config_dir))
    print(f"Serving Nano IR benchmark viewer on http://{args.host}:{args.port}")
    print(f"Local DuckDB: {location.local_path}")
    if location.source_path is not None:
        print(f"Source DuckDB: {location.source_path}")
    uvicorn.run(app, host=args.host, port=args.port)


def _load_dataset_for_args(args: argparse.Namespace, task: EvalTask) -> LoadedIrDataset:
    model_type = getattr(args, "model_type", None)
    candidate_subset_name = (
        (getattr(args, "candidate_subset_name", None) or task.dataset.candidate_config)
        if model_type in {"bm25", "reranker"}
        else None
    )
    return load_ir_dataset(
        task,
        candidate_subset_name=candidate_subset_name,
        revision=getattr(args, "dataset_revision", None),
    )


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
    if args.command == "web":
        run_web(args)
        return
    raise ValueError(f"Unsupported command: {args.command}")


if __name__ == "__main__":
    main()
