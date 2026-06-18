from __future__ import annotations

import argparse
import json
import re
import sys
import time
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from hakari_bench.bm25 import (
    BM25BuildResult,
    bm25_config_name,
    bm25_config_from_args,
    bm25_config_payload,
    collect_bm25_metadata,
    run_or_load_bm25_task,
)
from hakari_bench.batch import (
    BatchIndex,
    BatchMetadata,
    DEFAULT_BATCH_WORKSPACE_ROOT,
    PrecomputedDenseEmbeddingModel,
    batch_index_path,
    cleanup_batch_download_files,
    collect_openai_batch_embeddings,
    collect_openai_batch_task_embeddings,
    load_batch_index,
    load_batch_metadata,
    refresh_openai_batch_files,
    register_openai_embedding_task_batches,
    wait_for_openai_batch,
)
from hakari_bench.cli_schema import BuildCandidatesParamsJson, EvaluateParamsJson
from hakari_bench.task_docs import validate_task_docs
from hakari_bench.datasets import DatasetRegistry, EvalTask, resolve_eval_tasks
from hakari_bench.defaults import DEFAULT_CANDIDATE_RANKING, DEFAULT_RERANK_TOP_K
from hakari_bench.embedding_variants import (
    TORCH_RESCORE_SCORE_REPRESENTATION,
    TORCH_SCORE_REPRESENTATION,
    dense_embedding_variants,
    parse_embedding_variants,
    sparse_embedding_variants,
)
from hakari_bench.evaluation import LoadedIrDataset, load_ir_dataset, start_encode_pool, stop_encode_pool
from hakari_bench.model_cards import load_model_cards, write_evaluation_model_card
from hakari_bench.models import (
    ModelLoadConfig,
    collect_model_metadata,
    collect_runtime_environment,
    load_model,
)
from hakari_bench.results import (
    TaskRunResult,
    build_run_summary_payload,
    existing_result_path_for_task,
    read_result_json,
    result_path_for_task,
    run_or_load_task,
    safe_path_part,
)

MISSING_ATTENTION_IMPLEMENTATION_WARNING = (
    "warning: no attention implementation was specified. Pass --attn-implementation "
    "(for example, sdpa or flash_attention_2) or --flash-attn2 when appropriate. "
    "Benchmark inference can be long, and the model's officially recommended attention "
    "implementation can be substantially faster."
)
DEFAULT_RESULTS_DIR = "output/hakari-results"


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="HAKARI-Bench runner")
    subparsers = parser.add_subparsers(dest="command", required=True)

    evaluate = subparsers.add_parser("evaluate", help="Evaluate a model on Nano-style IR datasets.")
    evaluate_methods = evaluate.add_subparsers(dest="model_type", required=True)
    dense = evaluate_methods.add_parser("dense", help="Evaluate a dense embedding model.")
    _add_evaluate_model_args(dense)
    _add_evaluate_runtime_args(dense)
    _add_embedding_variant_args(dense)
    _add_dataset_args(dense, action="evaluate")
    _add_prompt_args(dense)
    _add_candidate_args(dense)
    _add_output_args(dense, results_default=DEFAULT_RESULTS_DIR)

    sparse = evaluate_methods.add_parser("sparse", help="Evaluate a sparse embedding model.")
    _add_evaluate_model_args(sparse)
    _add_evaluate_runtime_args(sparse)
    _add_sparse_args(sparse)
    _add_embedding_variant_args(sparse)
    _add_dataset_args(sparse, action="evaluate")
    _add_prompt_args(sparse)
    _add_candidate_args(sparse)
    _add_output_args(sparse, results_default=DEFAULT_RESULTS_DIR)

    reranker = evaluate_methods.add_parser("reranker", help="Evaluate a reranker model.")
    _add_evaluate_model_args(reranker)
    _add_evaluate_runtime_args(reranker)
    _add_dataset_args(reranker, action="evaluate")
    _add_reranker_args(reranker)
    _add_candidate_args(reranker)
    _add_output_args(reranker, results_default=DEFAULT_RESULTS_DIR)

    late_interaction = evaluate_methods.add_parser("late-interaction", help="Evaluate a late-interaction model.")
    _add_evaluate_model_args(late_interaction)
    _add_evaluate_runtime_args(late_interaction)
    _add_embedding_variant_args(late_interaction)
    _add_dataset_args(late_interaction, action="evaluate")
    _add_prompt_args(late_interaction)
    _add_late_interaction_args(late_interaction)
    _add_candidate_args(late_interaction)
    _add_output_args(late_interaction, results_default=DEFAULT_RESULTS_DIR)

    bm25 = evaluate_methods.add_parser("bm25", help="Evaluate BM25 rankings.")
    _add_params_arg(bm25)
    bm25.add_argument("--model", default=None, help="Display/storage model id for BM25 result metadata.")
    _add_dataset_args(bm25, action="evaluate")
    _add_candidate_args(bm25, candidate_default="bm25")
    _add_output_args(bm25, results_default=DEFAULT_RESULTS_DIR)
    _add_bm25_args(bm25, include_source=True)

    from_model_card = evaluate_methods.add_parser(
        "from-model-card",
        help="Evaluate a model using static HAKARI model-card metadata.",
    )
    from_model_card.add_argument(
        "--model-card",
        type=Path,
        required=True,
        help="Path to a single model-card YAML file.",
    )
    _add_params_arg(from_model_card)
    _add_evaluate_runtime_args(from_model_card)
    _add_sparse_args(from_model_card)
    _add_embedding_variant_args(from_model_card)
    _add_dataset_args(from_model_card, action="evaluate")
    _add_prompt_args(from_model_card)
    _add_candidate_args(from_model_card)
    _add_reranker_args(from_model_card)
    _add_late_interaction_args(from_model_card)
    _add_output_args(from_model_card, results_default=DEFAULT_RESULTS_DIR)

    build_candidates = subparsers.add_parser(
        "build-candidates",
        help="Build candidate ranking files for Nano-style datasets.",
    )
    candidate_methods = build_candidates.add_subparsers(dest="candidate_method", required=True)
    build_bm25 = candidate_methods.add_parser("bm25", help="Build BM25 candidate files.")
    _add_params_arg(build_bm25)
    _add_dataset_args(build_bm25, action="build")
    build_bm25.add_argument("--candidates-dir", default="output/candidates/bm25")
    build_bm25.add_argument("--overwrite", action="store_true")
    build_bm25.add_argument("--show-progress", action="store_true")
    _add_bm25_args(build_bm25)

    batch = subparsers.add_parser("batch", help="Register, fetch, and materialize batch inference jobs.")
    batch_methods = batch.add_subparsers(dest="batch_model_type", required=True)
    batch_dense = batch_methods.add_parser("dense", help="Batch workflow for dense embedding models.")
    batch_dense_actions = batch_dense.add_subparsers(dest="batch_action", required=True)

    batch_dense_register = batch_dense_actions.add_parser("register", help="Create and submit a dense batch job.")
    _add_batch_common_args(batch_dense_register)
    batch_dense_register.add_argument("--provider", choices=["openai"], default="openai")
    batch_dense_register.add_argument("--model", required=True)
    _add_dataset_args(batch_dense_register, action="evaluate")
    _add_prompt_args(batch_dense_register)
    _add_execution_args(batch_dense_register)
    _add_openai_batch_args(batch_dense_register)
    batch_dense_register.add_argument("--results-dir", default=DEFAULT_RESULTS_DIR)
    batch_dense_register.add_argument("--result-format", default="json.xz", choices=["json.xz", "json"])
    batch_dense_register.add_argument("--overwrite", action="store_true")

    batch_dense_fetch = batch_dense_actions.add_parser("fetch", help="Refresh batch status and download output files.")
    _add_batch_common_args(batch_dense_fetch)
    _add_openai_batch_auth_args(batch_dense_fetch)
    batch_dense_fetch.add_argument("--wait", action="store_true", help="Poll until the batch reaches a terminal state.")
    batch_dense_fetch.add_argument("--poll-seconds", type=int, default=900)

    batch_dense_materialize = batch_dense_actions.add_parser(
        "materialize",
        help="Build normal per-task result JSON from completed dense batch output.",
    )
    _add_batch_common_args(batch_dense_materialize)
    _add_embedding_variant_args(batch_dense_materialize)
    _add_candidate_args(batch_dense_materialize)
    _add_output_args(batch_dense_materialize, results_default=DEFAULT_RESULTS_DIR)

    batch_dense_process = batch_dense_actions.add_parser(
        "process",
        help="Fetch completed task batches, materialize results, and remove downloaded provider files.",
    )
    _add_batch_common_args(batch_dense_process)
    _add_openai_batch_auth_args(batch_dense_process)
    _add_embedding_variant_args(batch_dense_process)
    _add_candidate_args(batch_dense_process)
    _add_output_args(batch_dense_process, results_default=DEFAULT_RESULTS_DIR)
    batch_dense_process.add_argument(
        "--keep-downloaded-batch-files",
        action="store_true",
        help="Keep downloaded provider output/error JSONL files after successful materialization.",
    )

    web = subparsers.add_parser("web", help="Run the HAKARI-Bench result viewer.")
    web.add_argument("--host", default="127.0.0.1", help="Bind host. Use 0.0.0.0 to allow remote access.")
    web.add_argument("--port", type=int, default=8000)
    web.add_argument("--data-dir", default="output/viewer", help="Local viewer data/cache directory.")
    web.add_argument("--duckdb-path", default=None, help="Local DuckDB path. Defaults to DATA_DIR/hakari_bench.duckdb.")
    web.add_argument(
        "--source-results-dir",
        default=None,
        help="Source benchmark results directory containing hakari_bench.duckdb.",
    )
    web.add_argument("--source-duckdb-path", default=None, help="Explicit source DuckDB path to copy from.")
    web.add_argument("--hf-dataset-repo-id", default=None, help="Hugging Face dataset repo containing the viewer DuckDB.")
    web.add_argument("--hf-dataset-path", default=None, help="DuckDB file path inside the Hugging Face dataset repo.")
    web.add_argument("--hf-dataset-revision", default=None, help="Hugging Face dataset revision to download.")
    web.add_argument("--viewer-config-dir", default="config/viewer", help="Viewer YAML config directory.")

    validate_docs = subparsers.add_parser(
        "validate-task-docs",
        aliases=["validate-benchmark-docs", "validation-benchmark-docs"],
        help="Validate machine-readable task documentation metadata.",
    )
    validate_docs.add_argument(
        "--docs-root",
        type=Path,
        default=Path("task_docs/docs"),
        help="Task docs root used when no explicit paths are supplied.",
    )
    validate_docs.add_argument(
        "--metadata-root",
        type=Path,
        default=Path("task_docs/metadata"),
        help="Task metadata JSON root.",
    )
    validate_docs.add_argument(
        "paths",
        nargs="*",
        type=Path,
        help="Optional Markdown files or directories to validate. Defaults to all task docs under --docs-root.",
    )
    return parser


def _add_params_arg(parser: argparse.ArgumentParser) -> None:
    parser.add_argument("--params-json", default=None, help="Structured JSON parameters for this command.")


def _add_evaluate_model_args(parser: argparse.ArgumentParser) -> None:
    _add_params_arg(parser)
    parser.add_argument("--model", default=None, help="Hugging Face model id or local model path.")
    parser.add_argument("--model-alias", default=None, help="Display/storage alias for a local model path.")
    parser.add_argument("--model-revision", default=None, help="Hugging Face model revision to evaluate.")
    parser.add_argument(
        "--model-loader",
        default=None,
        help=(
            "Optional built-in or custom model loader. Use 'openai' for OpenAI embeddings, or module:function "
            "for a custom callable that receives ModelLoadConfig and returns an object matching the "
            "evaluation method's duck-typed interface."
        ),
    )
    parser.add_argument(
        "--model-loader-kwargs-json",
        default=None,
        help="JSON object of custom model loader kwargs available as ModelLoadConfig.model_loader_kwargs.",
    )


def _add_evaluate_runtime_args(parser: argparse.ArgumentParser) -> None:
    parser.add_argument("--dtype", default="bf16", choices=["bf16", "fp16", "fp32"])
    parser.add_argument("--attn-implementation", default=None)
    parser.add_argument("--flash-attn2", action="store_true")
    parser.add_argument("--device", default=None)
    parser.add_argument(
        "--retrieval-score-device",
        default="auto",
        choices=["auto", "cpu", "cuda"],
        help=(
            "Device policy for post-encode retrieval score/top-k matrix work. "
            "Use cpu or cuda to force supported matrix work onto that device."
        ),
    )
    parser.add_argument(
        "--encode-devices",
        action="append",
        default=None,
        help=(
            "SentenceTransformers encode devices for multi-process inference. "
            "Repeat or comma-separate, for example: cuda:0,cuda:1."
        ),
    )
    parser.add_argument(
        "--encode-chunk-size",
        type=int,
        default=None,
        help="Optional SentenceTransformers multi-process encode chunk size.",
    )
    parser.add_argument("--trust-remote-code", action="store_true")
    parser.add_argument("--model-max-seq-length", type=int, default=None)
    parser.add_argument("--truncate-dim", type=int, default=None)


def _add_sparse_args(parser: argparse.ArgumentParser) -> None:
    parser.add_argument(
        "--sparse-query-max-active-dims",
        type=int,
        default=None,
        help="Post-encode maximum active sparse dimensions per query embedding.",
    )
    parser.add_argument(
        "--sparse-document-max-active-dims",
        type=int,
        default=None,
        help="Post-encode maximum active sparse dimensions per document embedding.",
    )


def _add_embedding_variant_args(parser: argparse.ArgumentParser) -> None:
    parser.add_argument(
        "--embedding-variant",
        dest="embedding_variant_values",
        action="append",
        default=[],
        help=(
            "Derived embedding evaluation spec. Repeat or comma-separate. "
            "Current syntax: truncate:DIM, sparse-query-max-active-dims:DIM, "
            "sparse-document-max-active-dims:DIM, normalize, int8, binary, "
            "rescore:int8, rescore:binary, int8-rescore, or binary-rescore. "
            "Dense runs automatically include full-dim quantized/rescore variants; "
            "explicit truncate:DIM also expands to truncate x quantized/rescore variants. "
            "Sparse runs automatically include query/document max-active-dims grid variants."
        ),
    )
    parser.add_argument(
        "--embedding-variant-grid",
        dest="embedding_variant_grid_values",
        action="append",
        nargs="+",
        default=[],
        metavar="SPEC",
        help=(
            "Grid product of derived embedding specs, normalized into pipeline variants. "
            "Example: --embedding-variant-grid truncate:256,128,64 int8,binary"
        ),
    )
    parser.add_argument(
        "--no-default-embedding-variants",
        action="store_true",
        help=(
            "Disable automatic dense int8/binary quantized and top-100 rescore variants, "
            "including truncate x quantized/rescore expansion, and automatic sparse "
            "query/document max-active-dims grid variants."
        ),
    )


def _add_dataset_args(parser: argparse.ArgumentParser, *, action: str) -> None:
    verb = "evaluate" if action == "evaluate" else "build from"
    parser.add_argument(
        "--all",
        action="store_true",
        help=f"{verb.capitalize()} all built-in datasets. Existing outputs are still skipped unless --overwrite is set.",
    )
    parser.add_argument(
        "--dataset",
        action="append",
        default=None,
        help="Dataset name/id. Repeat or pass comma-separated values.",
    )
    parser.add_argument("--collection", action="append", default=[], help="Dataset collection name.")
    parser.add_argument("--split", action="append", default=[], help="Split/task name. Repeat or comma-separate.")
    parser.add_argument(
        "--evaluation-scope",
        choices=("standard", "all"),
        default="standard",
        help=(
            "Task inclusion scope. 'standard' skips tasks marked include_by_default: false unless --split is used; "
            "'all' includes extended tasks as well."
        ),
    )
    parser.add_argument("--dataset-revision", default=None, help=f"Hugging Face dataset revision to {verb}.")


def _add_execution_args(parser: argparse.ArgumentParser) -> None:
    parser.add_argument("--batch-size", type=int, default=32)
    parser.add_argument("--show-progress", action="store_true")


def _add_prompt_args(parser: argparse.ArgumentParser) -> None:
    parser.add_argument("--query-prompt", default=None)
    parser.add_argument("--document-prompt", default=None)
    parser.add_argument("--query-prompt-name", default=None)
    parser.add_argument("--document-prompt-name", default=None)
    parser.add_argument("--query-encode-task", default=None)
    parser.add_argument("--document-encode-task", default=None)
    parser.add_argument(
        "--encode-kwargs-json",
        default=None,
        help="JSON object of extra kwargs passed to query and document encode calls.",
    )
    parser.add_argument(
        "--query-encode-kwargs-json",
        default=None,
        help="JSON object of extra kwargs passed only to query encode calls.",
    )
    parser.add_argument(
        "--document-encode-kwargs-json",
        default=None,
        help="JSON object of extra kwargs passed only to document encode calls.",
    )


def _add_reranker_args(parser: argparse.ArgumentParser) -> None:
    parser.add_argument(
        "--reranker-init-kwargs-json",
        default=None,
        help="JSON object of extra constructor kwargs for SentenceTransformers CrossEncoder reranker models.",
    )
    parser.add_argument(
        "--reranker-inference-kwargs-json",
        default=None,
        help="JSON object of extra kwargs passed to reranker rank/predict calls.",
    )


def _add_candidate_args(
    parser: argparse.ArgumentParser,
    *,
    candidate_default: str = DEFAULT_CANDIDATE_RANKING,
) -> None:
    parser.add_argument("--candidate-ranking", default=candidate_default)
    parser.add_argument("--rerank-top-k", type=int, default=DEFAULT_RERANK_TOP_K)


def _add_late_interaction_args(parser: argparse.ArgumentParser) -> None:
    parser.add_argument("--late-interaction-query-length", type=int, default=None)
    parser.add_argument("--late-interaction-document-length", type=int, default=None)
    parser.add_argument("--late-interaction-query-prefix", default=None)
    parser.add_argument("--late-interaction-document-prefix", default=None)
    parser.add_argument("--late-interaction-attend-to-expansion-tokens", action="store_true", default=None)
    parser.add_argument("--late-interaction-exact-doc-batch-size", type=int, default=128)
    parser.add_argument("--late-interaction-exact-query-batch-size", type=int, default=8)


def _add_output_args(parser: argparse.ArgumentParser, *, results_default: str) -> None:
    _add_execution_args(parser)
    parser.add_argument("--results-dir", default=results_default)
    parser.add_argument(
        "--result-format",
        default="json.xz",
        choices=["json.xz", "json"],
        help="Per-task result file format. Defaults to compressed JSON payloads in .json.xz files.",
    )
    parser.add_argument("--overwrite", action="store_true")
    parser.add_argument("--primary-metric", default="ndcg@10")


def _add_batch_common_args(parser: argparse.ArgumentParser) -> None:
    parser.add_argument("--target", required=True, help="Stable local batch workspace target name.")
    parser.add_argument("--workspace-root", default=DEFAULT_BATCH_WORKSPACE_ROOT)


def _add_openai_batch_auth_args(parser: argparse.ArgumentParser) -> None:
    parser.add_argument("--dotenv-path", default=".env")
    parser.add_argument("--api-key-env", default="OPENAI_API_KEY")
    parser.add_argument("--base-url", default=None)
    parser.add_argument("--organization", default=None)
    parser.add_argument("--project", default=None)


def _add_openai_batch_args(parser: argparse.ArgumentParser) -> None:
    _add_openai_batch_auth_args(parser)
    parser.add_argument("--max-input-tokens", type=int, default=8100)
    parser.add_argument("--max-request-tokens", type=int, default=290_000)
    parser.add_argument(
        "--max-embedding-inputs",
        type=int,
        default=50_000,
        help="Maximum embedding inputs per OpenAI batch. The OpenAI embeddings batch limit is 50,000.",
    )


def _add_bm25_args(parser: argparse.ArgumentParser, *, include_source: bool = False) -> None:
    if include_source:
        parser.add_argument(
            "--bm25-source",
            choices=["dataset", "computed"],
            default="dataset",
            help="Use dataset candidate subset by default; use computed to recompute with bm25s.",
        )
    parser.add_argument("--bm25-top-k", type=int, default=100, help="Number of BM25 candidates per query.")
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
    parser.add_argument("--bm25-tokenizer-model", default=None)
    parser.add_argument("--bm25-wordseg-language", default=None)
    parser.add_argument("--bm25-stemmer-language", default="english")
    parser.add_argument("--bm25-k1", type=float, default=1.5)
    parser.add_argument("--bm25-b", type=float, default=0.75)


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = build_parser()
    raw_argv = list(sys.argv[1:] if argv is None else argv)
    provided_options = _provided_options(raw_argv)
    args = parser.parse_args(raw_argv)
    if args.command == "evaluate":
        try:
            _apply_evaluate_params_json(args)
            if args.model_type == "from-model-card":
                _apply_model_card_args(args, provided_options=provided_options)
        except ValueError as exc:
            parser.error(str(exc))
        _apply_model_identity(args)
        _bridge_new_evaluate_args(args)
        try:
            args.encode_devices = _comma_separated_values(getattr(args, "encode_devices", None), "--encode-devices")
        except ValueError as exc:
            parser.error(str(exc))
        if args.encode_chunk_size is not None and args.encode_chunk_size <= 0:
            parser.error("--encode-chunk-size must be positive.")
        if args.encode_chunk_size is not None and not args.encode_devices:
            parser.error("--encode-chunk-size requires --encode-devices.")
        if args.model_type != "dense" and args.encode_devices:
            parser.error("--encode-devices requires evaluate dense.")
        try:
            if args.model_type == "dense":
                args.embedding_variants = dense_embedding_variants(
                    args.embedding_variant_values,
                    args.embedding_variant_grid_values,
                    include_defaults=not args.no_default_embedding_variants,
                    normalize_truncate=getattr(args, "model_loader", None) == "openai",
                )
            elif args.model_type == "sparse":
                args.embedding_variants = sparse_embedding_variants(
                    args.embedding_variant_values,
                    args.embedding_variant_grid_values,
                    include_defaults=not args.no_default_embedding_variants,
                )
            else:
                args.embedding_variants = parse_embedding_variants(
                    args.embedding_variant_values,
                    args.embedding_variant_grid_values,
                )
        except ValueError as exc:
            parser.error(str(exc))
        _apply_score_device_to_quantized_variants(args.embedding_variants, score_device=args.retrieval_score_device)
        if args.model_type != "dense" and _embedding_variants_use_quantization(args.embedding_variants):
            parser.error(
                f"evaluate {args.model_type} does not support quantized embedding variants. "
                "Quantized embedding variants are supported for dense models only."
            )
        delattr(args, "embedding_variant_values")
        delattr(args, "embedding_variant_grid_values")
        try:
            args.model_loader_kwargs = _parse_json_object_arg(
                getattr(args, "model_loader_kwargs_json", None),
                option_name="--model-loader-kwargs-json",
            )
            args.encode_kwargs = _parse_json_object_arg(
                getattr(args, "encode_kwargs_json", None),
                option_name="--encode-kwargs-json",
            )
            args.query_encode_kwargs = _parse_json_object_arg(
                getattr(args, "query_encode_kwargs_json", None),
                option_name="--query-encode-kwargs-json",
            )
            args.document_encode_kwargs = _parse_json_object_arg(
                getattr(args, "document_encode_kwargs_json", None),
                option_name="--document-encode-kwargs-json",
            )
            args.cross_encoder_kwargs = _parse_json_object_arg(
                getattr(args, "reranker_init_kwargs_json", None),
                option_name="--reranker-init-kwargs-json",
            )
            args.reranker_score_kwargs = _parse_json_object_arg(
                getattr(args, "reranker_inference_kwargs_json", None),
                option_name="--reranker-inference-kwargs-json",
            )
        except ValueError as exc:
            parser.error(str(exc))
        for attr in (
            "model_loader_kwargs_json",
            "encode_kwargs_json",
            "query_encode_kwargs_json",
            "document_encode_kwargs_json",
        ):
            if hasattr(args, attr):
                delattr(args, attr)
        if hasattr(args, "reranker_init_kwargs_json"):
            delattr(args, "reranker_init_kwargs_json")
        if hasattr(args, "reranker_inference_kwargs_json"):
            delattr(args, "reranker_inference_kwargs_json")
        if args.model_type != "reranker" and (args.cross_encoder_kwargs or args.reranker_score_kwargs):
            parser.error("--reranker-init-kwargs-json and --reranker-inference-kwargs-json require evaluate reranker.")
        if args.model_type == "bm25" and (args.model_loader is not None or args.model_loader_kwargs):
            parser.error("--model-loader and --model-loader-kwargs-json are not supported for evaluate bm25.")
        if args.model_loader is None and args.model_loader_kwargs:
            parser.error("--model-loader-kwargs-json requires --model-loader.")
        if args.model_loader == "openai" and args.model_type != "dense":
            parser.error("--model-loader openai requires evaluate dense.")
        if args.model_loader == "openai" and args.encode_devices:
            parser.error("--encode-devices is not supported with --model-loader openai.")
    if args.command == "build-candidates":
        try:
            _apply_build_candidates_params_json(args)
        except ValueError as exc:
            parser.error(str(exc))
    if args.command == "batch":
        if args.batch_model_type != "dense":
            parser.error("Only batch dense is supported.")
        if args.batch_action == "register":
            _bridge_new_batch_register_args(args)
            try:
                args.encode_kwargs = _parse_json_object_arg(
                    getattr(args, "encode_kwargs_json", None),
                    option_name="--encode-kwargs-json",
                )
                args.query_encode_kwargs = _parse_json_object_arg(
                    getattr(args, "query_encode_kwargs_json", None),
                    option_name="--query-encode-kwargs-json",
                )
                args.document_encode_kwargs = _parse_json_object_arg(
                    getattr(args, "document_encode_kwargs_json", None),
                    option_name="--document-encode-kwargs-json",
                )
            except ValueError as exc:
                parser.error(str(exc))
            if args.encode_kwargs or args.query_encode_kwargs or args.document_encode_kwargs:
                parser.error("batch dense register currently supports explicit prompts only, not encode kwargs.")
            for attr in ("encode_kwargs_json", "query_encode_kwargs_json", "document_encode_kwargs_json"):
                if hasattr(args, attr):
                    delattr(args, attr)
            _validate_all_target_args(args, parser)
            _validate_evaluation_scope_arg(args, parser)
            if args.dataset is None and not args.collection:
                args.dataset = [] if args.all else ["hakari-bench/NanoBEIR-en"]
            elif args.dataset is None:
                args.dataset = []
            if args.batch_size <= 0:
                parser.error("--batch-size must be positive.")
            if args.max_input_tokens <= 0:
                parser.error("--max-input-tokens must be positive.")
            if args.max_request_tokens <= 0:
                parser.error("--max-request-tokens must be positive.")
            if args.max_embedding_inputs <= 0:
                parser.error("--max-embedding-inputs must be positive.")
        elif args.batch_action == "fetch":
            if args.poll_seconds <= 0:
                parser.error("--poll-seconds must be positive.")
        elif args.batch_action in {"materialize", "process"}:
            try:
                args.embedding_variants = dense_embedding_variants(
                    args.embedding_variant_values,
                    args.embedding_variant_grid_values,
                    include_defaults=not args.no_default_embedding_variants,
                    normalize_truncate=True,
                )
            except ValueError as exc:
                parser.error(str(exc))
            _apply_score_device_to_quantized_variants(args.embedding_variants, score_device="auto")
            delattr(args, "embedding_variant_values")
            delattr(args, "embedding_variant_grid_values")
            _bridge_new_batch_materialize_args(args)
            if args.rerank_top_k is not None and args.rerank_top_k <= 0:
                parser.error("--rerank-top-k must be positive.")
    if args.command == "evaluate":
        truncate_sparse_values = {
            "--sparse-query-max-active-dims": getattr(args, "sparse_query_max_active_dims", None),
            "--sparse-document-max-active-dims": getattr(args, "sparse_document_max_active_dims", None),
        }
        if any(value is not None for value in truncate_sparse_values.values()) and args.model_type != "sparse":
            parser.error("Sparse truncation options require evaluate sparse.")
        for option_name, value in truncate_sparse_values.items():
            if value is not None and value <= 0:
                parser.error(f"{option_name} must be positive.")
    if args.command == "evaluate" and getattr(args, "rerank_top_k", None) is not None and args.rerank_top_k <= 0:
        parser.error("--rerank-top-k must be positive.")
    if args.command == "evaluate" and args.model_type == "late-interaction":
        if args.embedding_variants and not _late_interaction_embedding_variants_are_supported(args.embedding_variants):
            parser.error("evaluate late-interaction supports only truncate embedding variants.")
        if args.truncate_dim is not None:
            parser.error("--truncate-dim is not supported with evaluate late-interaction.")
        if args.late_interaction_exact_doc_batch_size <= 0:
            parser.error("--late-interaction-exact-doc-batch-size must be positive.")
        if args.late_interaction_exact_query_batch_size <= 0:
            parser.error("--late-interaction-exact-query-batch-size must be positive.")
    if args.command == "evaluate":
        _validate_all_target_args(args, parser)
        _validate_evaluation_scope_arg(args, parser)
    if args.command == "evaluate" and args.dataset is None and not args.collection:
        args.dataset = [] if args.all else ["hakari-bench/NanoBEIR-en"]
    elif args.command == "evaluate" and args.dataset is None:
        args.dataset = []
    if args.command == "evaluate" and args.model_type == "bm25":
        _validate_bm25_source_args(args, parser)
    if args.command == "evaluate" and args.model_type == "bm25" and args.model is None:
        args.model = _default_bm25_model_id(args)
        args.model_id = args.model
        args.model_source = {"type": "bm25", "name": args.model}
    if args.command == "evaluate" and args.model_type != "bm25" and args.model is None:
        parser.error("--model is required unless evaluate bm25 is used.")
    if args.command == "build-candidates":
        _bridge_new_bm25_args(args)
        args.output_dir = args.candidates_dir
        args.override = args.overwrite
        _validate_all_target_args(args, parser)
        _validate_evaluation_scope_arg(args, parser)
    if args.command == "build-candidates" and args.dataset is None and not args.collection:
        args.dataset = [] if args.all else ["hakari-bench/NanoBEIR-en"]
    elif args.command == "build-candidates" and args.dataset is None:
        args.dataset = []
    return args


def _bridge_new_batch_register_args(args: argparse.Namespace) -> None:
    args.all = getattr(args, "all", False)
    args.collection = getattr(args, "collection", [])
    args.split = getattr(args, "split", [])
    args.evaluation_scope = getattr(args, "evaluation_scope", "standard")
    args.query_prompt = getattr(args, "query_prompt", None)
    args.document_prompt = getattr(args, "document_prompt", None)


def _bridge_new_batch_materialize_args(args: argparse.Namespace) -> None:
    args.model_type = "dense"
    args.output_dir = getattr(args, "results_dir", DEFAULT_RESULTS_DIR)
    args.result_format = getattr(args, "result_format", "json.xz")
    args.override = getattr(args, "overwrite", False)
    args.aggregate_metric = getattr(args, "primary_metric", "ndcg@10")
    args.show_progress = getattr(args, "show_progress", False)
    args.batch_size = getattr(args, "batch_size", 32)
    args.truncate_dim = None
    args.truncate_sparse_query_max_dims = None
    args.truncate_sparse_docs_max_dims = None
    args.score_device = "auto"
    args.encode_devices = None
    args.encode_chunk_size = None
    args.encode_kwargs = {}
    args.query_encode_kwargs = {}
    args.document_encode_kwargs = {}
    args.query_prompt = None
    args.corpus_prompt = None
    args.query_prompt_name = None
    args.corpus_prompt_name = None
    args.query_task = None
    args.corpus_task = None
    args.candidate_subset_name = getattr(args, "candidate_ranking", DEFAULT_CANDIDATE_RANKING)
    args.rerank_top_n = getattr(args, "rerank_top_k", DEFAULT_RERANK_TOP_K)


def _bridge_new_evaluate_args(args: argparse.Namespace) -> None:
    if not hasattr(args, "embedding_variant_values"):
        args.embedding_variant_values = []
    if not hasattr(args, "embedding_variant_grid_values"):
        args.embedding_variant_grid_values = []
    if not hasattr(args, "no_default_embedding_variants"):
        args.no_default_embedding_variants = False
    args.model = getattr(args, "model", None)
    args.model_alias = getattr(args, "model_alias", None)
    args.model_revision = getattr(args, "model_revision", None)
    args.model_loader = getattr(args, "model_loader", None)
    args.model_loader_kwargs = getattr(args, "model_loader_kwargs", {})
    args.all = getattr(args, "all", False)
    args.dtype = getattr(args, "dtype", "bf16")
    args.trust_remote_code = getattr(args, "trust_remote_code", False)
    args.truncate_dim = getattr(args, "truncate_dim", None)
    args.encode_devices = getattr(args, "encode_devices", None)
    args.encode_chunk_size = getattr(args, "encode_chunk_size", None)
    args.retrieval_score_device = getattr(args, "retrieval_score_device", "auto")
    args.score_device = getattr(args, "retrieval_score_device", "auto")
    args.query_prompt = getattr(args, "query_prompt", None)
    args.document_prompt = getattr(args, "document_prompt", None)
    args.query_prompt_name = getattr(args, "query_prompt_name", None)
    args.document_prompt_name = getattr(args, "document_prompt_name", None)
    args.query_encode_task = getattr(args, "query_encode_task", None)
    args.document_encode_task = getattr(args, "document_encode_task", None)
    args.encode_kwargs = getattr(args, "encode_kwargs", {})
    args.query_encode_kwargs = getattr(args, "query_encode_kwargs", {})
    args.document_encode_kwargs = getattr(args, "document_encode_kwargs", {})
    args.corpus_prompt = getattr(args, "document_prompt", None)
    args.corpus_prompt_name = getattr(args, "document_prompt_name", None)
    args.evaluation_scope = getattr(args, "evaluation_scope", "standard")
    args.query_task = getattr(args, "query_encode_task", None)
    args.corpus_task = getattr(args, "document_encode_task", None)
    args.candidate_subset_name = getattr(args, "candidate_ranking", DEFAULT_CANDIDATE_RANKING)
    args.rerank_top_n = getattr(args, "rerank_top_k", DEFAULT_RERANK_TOP_K)
    args.truncate_sparse_query_max_dims = getattr(args, "sparse_query_max_active_dims", None)
    args.truncate_sparse_docs_max_dims = getattr(args, "sparse_document_max_active_dims", None)
    args.output_dir = getattr(args, "results_dir", DEFAULT_RESULTS_DIR)
    args.result_format = getattr(args, "result_format", "json.xz")
    args.override = getattr(args, "overwrite", False)
    args.save_top_rankings = True
    args.aggregate_metric = getattr(args, "primary_metric", "ndcg@10")
    _bridge_new_bm25_args(args)


def _bridge_new_bm25_args(args: argparse.Namespace) -> None:
    args.all = getattr(args, "all", False)
    args.evaluation_scope = getattr(args, "evaluation_scope", "standard")
    args.top_k = getattr(args, "bm25_top_k", 100)
    args.bm25_source = getattr(args, "bm25_source", "dataset")
    args.bm25_tokenizer_name = getattr(args, "bm25_wordseg_language", None) or getattr(
        args,
        "bm25_tokenizer_model",
        None,
    )
    args.bm25_stemmer_algorithm = getattr(args, "bm25_stemmer_language", "english")


def _apply_model_card_args(args: argparse.Namespace, *, provided_options: set[str]) -> None:
    model_card_path = getattr(args, "model_card", None)
    if model_card_path is None:
        raise ValueError("--model-card is required.")
    cards = load_model_cards(Path(model_card_path))
    if len(cards) != 1:
        raise ValueError("--model-card must point to exactly one model card.")
    card = next(iter(cards.values()))
    method = card.get("method")
    if method not in {"dense", "sparse", "reranker", "late-interaction"}:
        raise ValueError("model card method must be one of dense, sparse, reranker, or late-interaction.")
    args.model_type = str(method)
    model_id = _string_param(card.get("id"), "model_card.id")
    source = card.get("source")
    source_name = source.get("name") if isinstance(source, dict) else None
    args.model = str(source_name or model_id)
    args.model_alias = model_id
    args.model_revision = _model_card_revision(source)
    if isinstance(source, dict) and source.get("type") == "openai":
        args.model_loader = "openai"
    runtime = card.get("runtime")
    if isinstance(runtime, dict):
        _apply_model_card_runtime(args, runtime, provided_options=provided_options)
    prompts = card.get("prompts")
    if isinstance(prompts, dict):
        _apply_model_card_prompts(args, prompts, provided_options=provided_options)
    late_interaction = card.get("late_interaction")
    if method == "late-interaction" and isinstance(late_interaction, dict):
        _apply_model_card_late_interaction(args, late_interaction, provided_options=provided_options)
    _validate_model_card_remote_code(card=card, source=source, runtime=runtime)
    target = card.get("target")
    if isinstance(target, dict):
        if not args.all:
            if args.dataset is None and target.get("datasets") is not None:
                args.dataset = _string_list_param(target["datasets"], "model_card.target.datasets")
            if not args.collection and target.get("collections") is not None:
                args.collection = _string_list_param(target["collections"], "model_card.target.collections")
            if not args.split and target.get("splits") is not None:
                args.split = _string_list_param(target["splits"], "model_card.target.splits")
            if getattr(args, "evaluation_scope", "standard") == "standard" and target.get("evaluation_scope") is not None:
                args.evaluation_scope = _string_param(target["evaluation_scope"], "model_card.target.evaluation_scope")
        if getattr(args, "dataset_revision", None) is None and target.get("dataset_revision") is not None:
            args.dataset_revision = _optional_string_param(target["dataset_revision"], "model_card.target.dataset_revision")
    embedding = card.get("embedding")
    if isinstance(embedding, dict) and not args.embedding_variant_values and not args.embedding_variant_grid_values:
        truncate_dims = embedding.get("truncate_dims")
        if isinstance(truncate_dims, list):
            args.embedding_variant_values = [f"truncate:{_optional_positive_int_param(dim, 'model_card.embedding.truncate_dims')}" for dim in truncate_dims]


def _model_card_revision(source: Any) -> str | None:
    if not isinstance(source, dict):
        return None
    requested = source.get("revision_requested")
    if requested is not None:
        return str(requested)
    revision = source.get("revision")
    return str(revision) if revision is not None else None


def _provided_options(argv: list[str]) -> set[str]:
    return {item.split("=", 1)[0] for item in argv if item.startswith("--")}


def _apply_model_card_runtime(args: argparse.Namespace, runtime: dict[str, Any], *, provided_options: set[str]) -> None:
    if runtime.get("dtype") is not None and "--dtype" not in provided_options:
        args.dtype = _optional_string_param(runtime["dtype"], "model_card.runtime.dtype")
    if runtime.get("attn_implementation") is not None and "--attn-implementation" not in provided_options:
        args.attn_implementation = _optional_string_param(
            runtime["attn_implementation"],
            "model_card.runtime.attn_implementation",
        )
    if runtime.get("trust_remote_code") is not None and "--trust-remote-code" not in provided_options:
        args.trust_remote_code = _bool_param(runtime["trust_remote_code"], "model_card.runtime.trust_remote_code")
    if runtime.get("max_seq_length") is not None and "--model-max-seq-length" not in provided_options:
        args.model_max_seq_length = _optional_positive_int_param(
            runtime["max_seq_length"],
            "model_card.runtime.max_seq_length",
        )


_FULL_HF_REVISION_SHA_RE = re.compile(r"^[0-9a-f]{40}$")


def _apply_model_card_prompts(args: argparse.Namespace, prompts: dict[str, Any], *, provided_options: set[str]) -> None:
    option_map = {
        "query_prompt": "--query-prompt",
        "document_prompt": "--document-prompt",
        "query_prompt_name": "--query-prompt-name",
        "document_prompt_name": "--document-prompt-name",
        "query_encode_task": "--query-encode-task",
        "document_encode_task": "--document-encode-task",
    }
    for key, option in option_map.items():
        if prompts.get(key) is not None and option not in provided_options:
            setattr(args, key, _optional_string_param(prompts[key], f"model_card.prompts.{key}"))


def _apply_model_card_late_interaction(
    args: argparse.Namespace,
    late_interaction: dict[str, Any],
    *,
    provided_options: set[str],
) -> None:
    int_options = {
        "query_length": ("late_interaction_query_length", "--late-interaction-query-length"),
        "document_length": ("late_interaction_document_length", "--late-interaction-document-length"),
    }
    for key, (attr, option) in int_options.items():
        if late_interaction.get(key) is not None and option not in provided_options:
            setattr(args, attr, _optional_positive_int_param(late_interaction[key], f"model_card.late_interaction.{key}"))
    string_options = {
        "query_prefix": ("late_interaction_query_prefix", "--late-interaction-query-prefix"),
        "document_prefix": ("late_interaction_document_prefix", "--late-interaction-document-prefix"),
    }
    for key, (attr, option) in string_options.items():
        if late_interaction.get(key) is not None and option not in provided_options:
            setattr(args, attr, _optional_string_param(late_interaction[key], f"model_card.late_interaction.{key}"))
    if late_interaction.get("do_query_expansion") is not None:
        args.late_interaction_do_query_expansion = _bool_param(
            late_interaction["do_query_expansion"],
            "model_card.late_interaction.do_query_expansion",
        )
    if (
        late_interaction.get("attend_to_expansion_tokens") is not None
        and "--late-interaction-attend-to-expansion-tokens" not in provided_options
    ):
        args.late_interaction_attend_to_expansion_tokens = _bool_param(
            late_interaction["attend_to_expansion_tokens"],
            "model_card.late_interaction.attend_to_expansion_tokens",
        )


def _validate_model_card_remote_code(*, card: dict[str, Any], source: Any, runtime: Any) -> None:
    if not isinstance(runtime, dict) or runtime.get("trust_remote_code") is not True:
        return
    if runtime.get("remote_code_approved") is not True:
        model_id = card.get("id", "<unknown>")
        raise ValueError(
            f"model card {model_id!r} sets runtime.trust_remote_code=true; "
            "set runtime.remote_code_approved=true after reviewing the pinned Hugging Face code."
        )
    revision = _model_card_revision(source)
    if revision is None or _FULL_HF_REVISION_SHA_RE.fullmatch(revision) is None:
        model_id = card.get("id", "<unknown>")
        raise ValueError(
            f"model card {model_id!r} sets runtime.trust_remote_code=true; "
            "source.revision must be a full 40-character Hugging Face revision SHA."
        )


def _validate_bm25_source_args(args: argparse.Namespace, parser: argparse.ArgumentParser) -> None:
    if getattr(args, "bm25_source", "dataset") != "dataset":
        return
    if getattr(args, "bm25_tokenizer", None) is not None:
        parser.error("--bm25-tokenizer requires --bm25-source computed.")
    if getattr(args, "bm25_tokenizer_model", None) is not None:
        parser.error("--bm25-tokenizer-model requires --bm25-source computed.")
    if getattr(args, "bm25_wordseg_language", None) is not None:
        parser.error("--bm25-wordseg-language requires --bm25-source computed.")


def _default_bm25_model_id(args: argparse.Namespace) -> str:
    if getattr(args, "bm25_source", "dataset") == "computed":
        return f"bm25/{bm25_config_name(bm25_config_from_args(args))}"
    candidate_name = safe_path_part(getattr(args, "candidate_subset_name", "bm25") or "bm25")
    if candidate_name == "bm25":
        return "bm25"
    return f"bm25/dataset-{candidate_name}"


def _apply_model_identity(args: argparse.Namespace) -> None:
    if args.model_type == "bm25":
        model = getattr(args, "model", None)
        if model:
            args.model_id = model
            args.model_source = {"type": "bm25", "name": model}
        return
    model = getattr(args, "model", None)
    alias = getattr(args, "model_alias", None)
    if not model:
        return
    if getattr(args, "model_loader", None) == "openai":
        args.model_id = alias or model
        args.model_source = {"type": "openai", "name": model}
        return
    is_local = _is_local_model_path(model)
    args.model_id = _model_id_for(model, alias=alias, is_local=is_local)
    args.model_source = _model_source_for(model, is_local=is_local, revision=args.model_revision)


def _is_local_model_path(value: str) -> bool:
    return value.startswith(("/", "./", "../", "~")) or Path(value).exists()


def _model_id_for(model: str, *, alias: str | None, is_local: bool) -> str:
    if alias is not None:
        normalized_alias = alias.strip().strip("/\\")
        if not normalized_alias:
            raise ValueError("--model-alias must not be empty.")
        return normalized_alias if "/" in normalized_alias else f"local/{normalized_alias}"
    if is_local:
        path = Path(model).expanduser()
        basename = path.name or path.parent.name or "model"
        return f"local/{safe_path_part(basename)}"
    return model


def _model_source_for(model: str, *, is_local: bool, revision: str | None = None) -> dict[str, str]:
    if is_local:
        path = Path(model).expanduser().resolve(strict=False)
        return {"type": "local_path", "path": str(path)}
    source = {"type": "huggingface", "name": model}
    if revision is not None:
        source["revision_requested"] = revision
    return source


def _apply_evaluate_params_json(args: argparse.Namespace) -> None:
    raw = getattr(args, "params_json", None)
    if raw is None:
        return
    payload = _parse_evaluate_params_json(raw)
    _apply_model_params(args, _params_section(payload, "model"))
    _apply_target_params(args, _params_section(payload, "target"))
    _apply_runtime_params(args, _params_section(payload, "runtime"))
    _apply_output_params(args, _params_section(payload, "output"))
    _apply_prompt_params(args, _params_section(payload, "prompts"))
    _apply_reranker_params(args, _params_section(payload, "reranker"))
    _apply_sparse_params(args, _params_section(payload, "sparse"))
    _apply_embedding_params(args, _params_section(payload, "embedding"))
    _apply_bm25_params(args, _params_section(payload, "bm25"))
    _apply_late_interaction_params(args, _params_section(payload, "late_interaction"))


def _apply_build_candidates_params_json(args: argparse.Namespace) -> None:
    raw = getattr(args, "params_json", None)
    if raw is None:
        return
    payload = _parse_build_candidates_params_json(raw)
    _apply_target_params(args, _params_section(payload, "target"))
    _apply_build_candidates_output_params(args, _params_section(payload, "output"))
    _apply_bm25_params(args, _params_section(payload, "bm25"))


def _parse_evaluate_params_json(raw: str) -> dict[str, Any]:
    try:
        return EvaluateParamsJson.model_validate_json(raw).model_dump(exclude_none=True)
    except ValueError as exc:
        raise ValueError(f"--params-json is invalid: {exc}") from exc


def _parse_build_candidates_params_json(raw: str) -> dict[str, Any]:
    try:
        return BuildCandidatesParamsJson.model_validate_json(raw).model_dump(exclude_none=True)
    except ValueError as exc:
        raise ValueError(f"--params-json is invalid: {exc}") from exc


def _params_section(payload: dict[str, Any], key: str) -> dict[str, Any]:
    value = payload.get(key)
    if value is None:
        return {}
    if not isinstance(value, dict):
        raise ValueError(f"params.{key} must be a JSON object.")
    return value


def _reject_unknown_keys(value: dict[str, Any], *, allowed: set[str], path: str) -> None:
    unknown = sorted(set(value) - allowed)
    if unknown:
        raise ValueError(f"{path} contains unknown key(s): {', '.join(unknown)}")


def _apply_model_params(args: argparse.Namespace, value: dict[str, Any]) -> None:
    _reject_unknown_keys(value, allowed={"source", "alias", "revision", "loader", "loader_kwargs"}, path="params.model")
    if "source" in value:
        args.model = _string_param(value["source"], "params.model.source")
    if "alias" in value:
        args.model_alias = _string_param(value["alias"], "params.model.alias")
    if "revision" in value:
        args.model_revision = _optional_string_param(value["revision"], "params.model.revision")
    if "loader" in value:
        args.model_loader = _optional_string_param(value["loader"], "params.model.loader")
    if "loader_kwargs" in value:
        args.model_loader_kwargs_json = json.dumps(_dict_param(value["loader_kwargs"], "params.model.loader_kwargs"))


def _apply_target_params(args: argparse.Namespace, value: dict[str, Any]) -> None:
    _reject_unknown_keys(
        value,
        allowed={"all", "datasets", "collections", "splits", "evaluation_scope", "dataset_revision"},
        path="params.target",
    )
    if "all" in value:
        args.all = _bool_param(value["all"], "params.target.all")
    if "datasets" in value:
        args.dataset = _string_list_param(value["datasets"], "params.target.datasets")
    if "collections" in value:
        args.collection = _string_list_param(value["collections"], "params.target.collections")
    if "splits" in value:
        args.split = _string_list_param(value["splits"], "params.target.splits")
    if "evaluation_scope" in value:
        args.evaluation_scope = _string_param(value["evaluation_scope"], "params.target.evaluation_scope")
    if "dataset_revision" in value:
        args.dataset_revision = _optional_string_param(value["dataset_revision"], "params.target.dataset_revision")


def _apply_runtime_params(args: argparse.Namespace, value: dict[str, Any]) -> None:
    _reject_unknown_keys(
        value,
        allowed={
            "batch_size",
            "dtype",
            "attn_implementation",
            "flash_attn2",
            "device",
            "retrieval_score_device",
            "encode_devices",
            "encode_chunk_size",
            "trust_remote_code",
            "model_max_seq_length",
            "truncate_dim",
            "show_progress",
        },
        path="params.runtime",
    )
    for key in ("dtype", "attn_implementation", "device", "retrieval_score_device"):
        if key in value:
            setattr(args, key, _optional_string_param(value[key], f"params.runtime.{key}"))
    if "encode_devices" in value:
        args.encode_devices = _string_list_param(value["encode_devices"], "params.runtime.encode_devices")
    for key in ("flash_attn2", "trust_remote_code", "show_progress"):
        if key in value:
            setattr(args, key, _bool_param(value[key], f"params.runtime.{key}"))
    for key in ("batch_size", "encode_chunk_size", "model_max_seq_length", "truncate_dim"):
        if key in value:
            setattr(args, key, _optional_positive_int_param(value[key], f"params.runtime.{key}"))


def _apply_output_params(args: argparse.Namespace, value: dict[str, Any]) -> None:
    _reject_unknown_keys(
        value,
        allowed={"results_dir", "candidates_dir", "result_format", "overwrite"},
        path="params.output",
    )
    if "results_dir" in value:
        args.results_dir = _string_param(value["results_dir"], "params.output.results_dir")
    if "candidates_dir" in value:
        args.candidates_dir = _string_param(value["candidates_dir"], "params.output.candidates_dir")
    if "result_format" in value:
        args.result_format = _string_param(value["result_format"], "params.output.result_format")
    if "overwrite" in value:
        args.overwrite = _bool_param(value["overwrite"], "params.output.overwrite")


def _apply_build_candidates_output_params(args: argparse.Namespace, value: dict[str, Any]) -> None:
    _reject_unknown_keys(value, allowed={"candidates_dir", "overwrite"}, path="params.output")
    if "candidates_dir" in value:
        args.candidates_dir = _string_param(value["candidates_dir"], "params.output.candidates_dir")
    if "overwrite" in value:
        args.overwrite = _bool_param(value["overwrite"], "params.output.overwrite")


def _apply_prompt_params(args: argparse.Namespace, value: dict[str, Any]) -> None:
    _reject_unknown_keys(
        value,
        allowed={
            "query_prompt",
            "document_prompt",
            "query_prompt_name",
            "document_prompt_name",
            "query_encode_task",
            "document_encode_task",
            "encode_kwargs",
            "query_encode_kwargs",
            "document_encode_kwargs",
        },
        path="params.prompts",
    )
    for key in (
        "query_prompt",
        "document_prompt",
        "query_prompt_name",
        "document_prompt_name",
        "query_encode_task",
        "document_encode_task",
    ):
        if key in value:
            setattr(args, key, _optional_string_param(value[key], f"params.prompts.{key}"))
    for key in ("encode_kwargs", "query_encode_kwargs", "document_encode_kwargs"):
        if key in value:
            setattr(args, f"{key}_json", json.dumps(_dict_param(value[key], f"params.prompts.{key}")))


def _apply_reranker_params(args: argparse.Namespace, value: dict[str, Any]) -> None:
    _reject_unknown_keys(value, allowed={"init_kwargs", "inference_kwargs", "candidate_ranking", "rerank_top_k"}, path="params.reranker")
    if "init_kwargs" in value:
        args.reranker_init_kwargs_json = json.dumps(_dict_param(value["init_kwargs"], "params.reranker.init_kwargs"))
    if "inference_kwargs" in value:
        args.reranker_inference_kwargs_json = json.dumps(_dict_param(value["inference_kwargs"], "params.reranker.inference_kwargs"))
    if "candidate_ranking" in value:
        args.candidate_ranking = _optional_string_param(value["candidate_ranking"], "params.reranker.candidate_ranking")
    if "rerank_top_k" in value:
        args.rerank_top_k = _optional_positive_int_param(value["rerank_top_k"], "params.reranker.rerank_top_k")


def _apply_sparse_params(args: argparse.Namespace, value: dict[str, Any]) -> None:
    _reject_unknown_keys(value, allowed={"query_max_active_dims", "document_max_active_dims"}, path="params.sparse")
    if "query_max_active_dims" in value:
        args.sparse_query_max_active_dims = _optional_positive_int_param(value["query_max_active_dims"], "params.sparse.query_max_active_dims")
    if "document_max_active_dims" in value:
        args.sparse_document_max_active_dims = _optional_positive_int_param(
            value["document_max_active_dims"],
            "params.sparse.document_max_active_dims",
        )


def _apply_embedding_params(args: argparse.Namespace, value: dict[str, Any]) -> None:
    _reject_unknown_keys(value, allowed={"variants", "variant_grid", "default_variants"}, path="params.embedding")
    if "variants" in value:
        args.embedding_variant_values = _string_list_param(value["variants"], "params.embedding.variants")
    if "variant_grid" in value:
        args.embedding_variant_grid_values = _grid_param(value["variant_grid"], "params.embedding.variant_grid")
    if "default_variants" in value:
        args.no_default_embedding_variants = not _bool_param(value["default_variants"], "params.embedding.default_variants")


def _apply_bm25_params(args: argparse.Namespace, value: dict[str, Any]) -> None:
    _reject_unknown_keys(
        value,
        allowed={"source", "top_k", "tokenizer", "tokenizer_model", "wordseg_language", "stemmer_language", "k1", "b"},
        path="params.bm25",
    )
    if "source" in value:
        args.bm25_source = _string_param(value["source"], "params.bm25.source")
    if "top_k" in value:
        args.bm25_top_k = _optional_positive_int_param(value["top_k"], "params.bm25.top_k")
    for key, attr in {
        "tokenizer": "bm25_tokenizer",
        "tokenizer_model": "bm25_tokenizer_model",
        "wordseg_language": "bm25_wordseg_language",
        "stemmer_language": "bm25_stemmer_language",
    }.items():
        if key in value:
            setattr(args, attr, _optional_string_param(value[key], f"params.bm25.{key}"))
    for key, attr in {"k1": "bm25_k1", "b": "bm25_b"}.items():
        if key in value:
            setattr(args, attr, _float_param(value[key], f"params.bm25.{key}"))


def _apply_late_interaction_params(args: argparse.Namespace, value: dict[str, Any]) -> None:
    _reject_unknown_keys(
        value,
        allowed={
            "query_length",
            "document_length",
            "query_prefix",
            "document_prefix",
            "attend_to_expansion_tokens",
            "exact_document_batch_size",
            "exact_query_batch_size",
        },
        path="params.late_interaction",
    )
    if "query_length" in value:
        args.late_interaction_query_length = _optional_positive_int_param(value["query_length"], "params.late_interaction.query_length")
    if "document_length" in value:
        args.late_interaction_document_length = _optional_positive_int_param(value["document_length"], "params.late_interaction.document_length")
    if "query_prefix" in value:
        args.late_interaction_query_prefix = _optional_string_param(value["query_prefix"], "params.late_interaction.query_prefix")
    if "document_prefix" in value:
        args.late_interaction_document_prefix = _optional_string_param(value["document_prefix"], "params.late_interaction.document_prefix")
    if "attend_to_expansion_tokens" in value:
        args.late_interaction_attend_to_expansion_tokens = _bool_param(
            value["attend_to_expansion_tokens"],
            "params.late_interaction.attend_to_expansion_tokens",
        )
    if "exact_document_batch_size" in value:
        args.late_interaction_exact_doc_batch_size = _optional_positive_int_param(
            value["exact_document_batch_size"],
            "params.late_interaction.exact_document_batch_size",
        )
    if "exact_query_batch_size" in value:
        args.late_interaction_exact_query_batch_size = _optional_positive_int_param(
            value["exact_query_batch_size"],
            "params.late_interaction.exact_query_batch_size",
        )


def _string_param(value: Any, path: str) -> str:
    if not isinstance(value, str) or not value:
        raise ValueError(f"{path} must be a non-empty string.")
    return value


def _optional_string_param(value: Any, path: str) -> str | None:
    if value is None:
        return None
    return _string_param(value, path)


def _string_list_param(value: Any, path: str) -> list[str]:
    if not isinstance(value, list) or not all(isinstance(item, str) and item for item in value):
        raise ValueError(f"{path} must be a list of non-empty strings.")
    return value


def _comma_separated_values(value: list[str] | None, option_name: str) -> list[str] | None:
    if value is None:
        return None
    values: list[str] = []
    for item in value:
        for part in item.split(","):
            part = part.strip()
            if not part:
                raise ValueError(f"{option_name} must contain only non-empty values.")
            values.append(part)
    return values or None


def _grid_param(value: Any, path: str) -> list[list[str]]:
    if not isinstance(value, list):
        raise ValueError(f"{path} must be a list of string lists.")
    grid: list[list[str]] = []
    for index, item in enumerate(value):
        grid.append(_string_list_param(item, f"{path}[{index}]"))
    return grid


def _dict_param(value: Any, path: str) -> dict[str, Any]:
    if not isinstance(value, dict):
        raise ValueError(f"{path} must be a JSON object.")
    return value


def _bool_param(value: Any, path: str) -> bool:
    if not isinstance(value, bool):
        raise ValueError(f"{path} must be a boolean.")
    return value


def _optional_positive_int_param(value: Any, path: str) -> int | None:
    if value is None:
        return None
    if not isinstance(value, int) or value <= 0:
        raise ValueError(f"{path} must be a positive integer.")
    return value


def _float_param(value: Any, path: str) -> float:
    if not isinstance(value, int | float):
        raise ValueError(f"{path} must be a number.")
    return float(value)


def _embedding_variants_use_quantization(variants: list[dict[str, Any]]) -> bool:
    return any(_embedding_variant_uses_quantization(variant) for variant in variants)


def _apply_score_device_to_quantized_variants(variants: list[dict[str, Any]], *, score_device: str) -> None:
    if score_device == "auto":
        return
    for variant in variants:
        for step in _embedding_variant_steps(variant):
            if step.get("type") != "quantize":
                continue
            parameters = step.get("parameters")
            if not isinstance(parameters, dict):
                continue
            if parameters.get("score_representation") not in {
                TORCH_SCORE_REPRESENTATION,
                TORCH_RESCORE_SCORE_REPRESENTATION,
            }:
                continue
            parameters["search_device"] = score_device


def _embedding_variant_uses_quantization(variant: dict[str, Any]) -> bool:
    return any(step.get("type") == "quantize" for step in _embedding_variant_steps(variant))


def _embedding_variant_steps(variant: dict[str, Any]) -> list[dict[str, Any]]:
    transform = variant.get("transform")
    if not isinstance(transform, dict):
        return []
    if transform.get("type") == "quantize":
        return [transform]
    steps = transform.get("steps")
    if not isinstance(steps, list):
        return []
    return [step for step in steps if isinstance(step, dict)]


def _parse_json_object_arg(value: str | None, *, option_name: str) -> dict[str, Any]:
    if value is None:
        return {}
    try:
        parsed = json.loads(value)
    except json.JSONDecodeError as exc:
        raise ValueError(f"{option_name} must be a valid JSON object: {exc}") from exc
    if not isinstance(parsed, dict):
        raise ValueError(f"{option_name} must be a JSON object.")
    return parsed


def _validate_all_target_args(args: argparse.Namespace, parser: argparse.ArgumentParser) -> None:
    if not getattr(args, "all", False):
        return
    if getattr(args, "dataset", None):
        parser.error("--all cannot be combined with --dataset.")
    if getattr(args, "collection", None):
        parser.error("--all cannot be combined with --collection.")
    if getattr(args, "split", None):
        parser.error("--all cannot be combined with --split.")


def _validate_evaluation_scope_arg(args: argparse.Namespace, parser: argparse.ArgumentParser) -> None:
    if getattr(args, "evaluation_scope", "standard") not in {"standard", "all"}:
        parser.error("--evaluation-scope must be one of: standard, all.")


def _dataset_values_for_args(args: argparse.Namespace, registry: DatasetRegistry) -> list[str]:
    if getattr(args, "all", False):
        return registry.dataset_names()
    return args.dataset


def _existing_readable_result_path(
    *,
    output_dir: Path,
    model_id: str,
    task: EvalTask,
    result_format: str | None,
) -> Path | None:
    path = existing_result_path_for_task(
        output_dir=output_dir,
        model_id=model_id,
        task=task,
        result_format=result_format,
    )
    if path is None:
        return None
    try:
        read_result_json(path)
    except Exception:
        return None
    return path


def run_batch(args: argparse.Namespace) -> dict[str, Any]:
    if args.batch_model_type != "dense":
        raise ValueError("Only batch dense is supported.")
    if args.batch_action == "register":
        return run_batch_dense_register(args)
    if args.batch_action == "fetch":
        return run_batch_dense_fetch(args)
    if args.batch_action == "process":
        return run_batch_dense_process(args)
    if args.batch_action == "materialize":
        return run_batch_dense_materialize(args)
    raise ValueError(f"Unsupported batch action: {args.batch_action}")


def run_batch_dense_register(args: argparse.Namespace) -> dict[str, Any]:
    registry = DatasetRegistry.load_builtin()
    tasks = resolve_eval_tasks(
        registry=registry,
        dataset_values=_dataset_values_for_args(args, registry),
        collection_values=args.collection,
        split_values=args.split,
        evaluation_scope=args.evaluation_scope,
    )
    if args.provider != "openai":
        raise ValueError(f"Unsupported dense batch provider: {args.provider}")
    workspace_root = Path(args.workspace_root)
    index_path = batch_index_path(target=args.target, workspace_root=workspace_root)
    if index_path.exists() and not args.overwrite:
        raise FileExistsError(f"Batch index already exists: {index_path}. Use --overwrite to replace it.")
    output_dir = Path(args.results_dir)
    task_groups: list[dict[str, Any]] = []
    skipped_existing_results: list[dict[str, Any]] = []
    for task in tasks:
        existing_result = _existing_readable_result_path(
            output_dir=output_dir,
            model_id=args.model,
            task=task,
            result_format=args.result_format,
        )
        if existing_result is not None and not args.overwrite:
            skipped_existing_results.append(
                {
                    "dataset_id": task.dataset_id,
                    "dataset_name": task.dataset_name,
                    "split_name": task.split_name,
                    "task_name": task.task_name,
                    "task_key": f"{task.dataset_id}::{task.split_name}",
                    "result_path": str(existing_result),
                }
            )
            continue
        dataset = _load_dataset_for_args(args, task)
        metadatas = register_openai_embedding_task_batches(
            target=args.target,
            workspace_root=workspace_root,
            model=args.model,
            task=task,
            dataset=dataset,
            batch_size=args.batch_size,
            max_input_tokens=args.max_input_tokens,
            max_request_tokens=args.max_request_tokens,
            max_embedding_inputs=args.max_embedding_inputs,
            query_prompt=args.query_prompt,
            document_prompt=args.document_prompt,
            dataset_revision=getattr(args, "dataset_revision", None),
            dotenv_path=args.dotenv_path,
            api_key_env=args.api_key_env,
            base_url=args.base_url,
            organization=args.organization,
            project=args.project,
            overwrite=args.overwrite,
        )
        task_payload = dict(metadatas[0].tasks[0]) if metadatas else {
            "dataset_id": task.dataset_id,
            "dataset_name": task.dataset_name,
            "split_name": task.split_name,
            "task_name": task.task_name,
            "task_key": f"{task.dataset_id}::{task.split_name}",
        }
        task_groups.append(
            {
                **task_payload,
                "batches": [
                    {
                        "target": metadata.target,
                        "metadata_path": str(metadata.metadata_path),
                        "batch_id": metadata.batch_id,
                        "status": metadata.status,
                        "embedding_input_count": metadata.embedding_input_count,
                    }
                    for metadata in metadatas
                ],
            }
        )
    index = BatchIndex(
        schema_version=1,
        provider=args.provider,
        model_type="dense",
        model=args.model,
        target=args.target,
        workspace_path=workspace_root / safe_path_part(args.target),
        index_path=index_path,
        tasks=task_groups,
        skipped_existing_results=skipped_existing_results,
        dataset_revision=getattr(args, "dataset_revision", None),
        config={
            "batch_size": args.batch_size,
            "max_input_tokens": args.max_input_tokens,
            "max_request_tokens": args.max_request_tokens,
            "max_embedding_inputs": args.max_embedding_inputs,
            "query_prompt": args.query_prompt,
            "document_prompt": args.document_prompt,
            "results_dir": str(output_dir),
            "result_format": args.result_format,
            "dimension_reduction": "full_embedding_prefix_l2_normalize",
        },
        api={
            "endpoint": "/v1/embeddings",
            "completion_window": "24h",
            "input_purpose": "batch",
        },
    )
    index.write()
    payload = {
        "target": args.target,
        "provider": args.provider,
        "model": args.model,
        "index_path": str(index.index_path),
        "registered_task_count": len(task_groups),
        "registered_batch_count": sum(len(group["batches"]) for group in task_groups),
        "skipped_existing_result_count": len(skipped_existing_results),
        "embedding_input_count": sum(
            int(batch["embedding_input_count"]) for group in task_groups for batch in group["batches"]
        ),
    }
    print(json.dumps(payload, ensure_ascii=False, indent=2))
    return payload


def run_batch_dense_fetch(args: argparse.Namespace) -> dict[str, Any]:
    metadata = load_batch_metadata(target=args.target, workspace_root=Path(args.workspace_root))
    if metadata.provider != "openai":
        raise ValueError(f"Unsupported batch provider for fetch: {metadata.provider}")
    if args.wait:
        metadata = wait_for_openai_batch(
            metadata=metadata,
            poll_seconds=args.poll_seconds,
            dotenv_path=args.dotenv_path,
            api_key_env=args.api_key_env,
            base_url=args.base_url,
            organization=args.organization,
            project=args.project,
        )
    else:
        metadata = refresh_openai_batch_files(
            metadata=metadata,
            dotenv_path=args.dotenv_path,
            api_key_env=args.api_key_env,
            base_url=args.base_url,
            organization=args.organization,
            project=args.project,
        )
    payload = _batch_summary(metadata)
    print(json.dumps(payload, ensure_ascii=False, indent=2))
    return payload


def run_batch_dense_process(args: argparse.Namespace) -> dict[str, Any]:
    index = load_batch_index(target=args.target, workspace_root=Path(args.workspace_root))
    if index.provider != "openai":
        raise ValueError(f"Unsupported batch provider for process: {index.provider}")
    args.model = index.model
    args.model_id = index.model
    args.model_source = {"type": index.provider, "name": index.model}
    args.model_loader = f"{index.provider}-batch"
    args.model_revision = None
    args.dtype = "fp32"
    args.device = None
    args.attn_implementation = None
    args.flash_attn2 = False
    args.trust_remote_code = False
    args.model_max_seq_length = (index.config or {}).get("max_input_tokens")
    args.dataset_revision = index.dataset_revision

    environment = collect_runtime_environment()
    registry = DatasetRegistry.load_builtin()
    results: list[TaskRunResult] = []
    processed_count = 0
    pending_count = 0
    failed_count = 0
    skipped_existing_result_count = 0
    cleaned_file_count = 0
    for task_group in index.tasks:
        task = _task_from_batch_payload(registry, task_group)
        existing_result = _existing_readable_result_path(
            output_dir=Path(args.output_dir),
            model_id=index.model,
            task=task,
            result_format=args.result_format,
        )
        if existing_result is not None and not args.override:
            skipped_existing_result_count += 1
            continue
        metadatas = [BatchMetadata.from_path(Path(batch["metadata_path"])) for batch in task_group["batches"]]
        refreshed = [
            refresh_openai_batch_files(
                metadata=metadata,
                dotenv_path=args.dotenv_path,
                api_key_env=args.api_key_env,
                base_url=args.base_url,
                organization=args.organization,
                project=args.project,
                download_files=False,
            )
            for metadata in metadatas
        ]
        statuses = {metadata.status for metadata in refreshed}
        if statuses - {"completed"}:
            if statuses & {"failed", "cancelled", "expired"}:
                failed_count += 1
            else:
                pending_count += 1
            continue
        downloaded = [
            refresh_openai_batch_files(
                metadata=metadata,
                dotenv_path=args.dotenv_path,
                api_key_env=args.api_key_env,
                base_url=args.base_url,
                organization=args.organization,
                project=args.project,
                download_files=True,
            )
            for metadata in refreshed
        ]
        task_embeddings = collect_openai_batch_task_embeddings(downloaded)
        dataset = _load_dataset_for_args(args, task)
        result = _materialize_precomputed_batch_task(
            args=args,
            environment=environment,
            task=task,
            dataset=dataset,
            task_embeddings=task_embeddings,
            metadata=downloaded[0],
        )
        results.append(result)
        processed_count += 1
        if not args.keep_downloaded_batch_files and not result.cache_hit:
            for metadata in downloaded:
                cleaned_file_count += len(cleanup_batch_download_files(metadata))
    payload: dict[str, Any] = {
        "target": index.target,
        "provider": index.provider,
        "model": index.model,
        "processed_count": processed_count,
        "pending_count": pending_count,
        "failed_count": failed_count,
        "skipped_existing_result_count": skipped_existing_result_count,
        "cleaned_file_count": cleaned_file_count,
        "result_count": len(results),
        "index_path": str(index.index_path),
    }
    if results:
        summary = build_run_summary_payload(
            args=args,
            environment=environment,
            model_metadata=results[-1].payload.get("model", {}),
            results=results,
            run_started_at_utc=datetime.now(timezone.utc).isoformat(),
            run_finished_at_utc=datetime.now(timezone.utc).isoformat(),
            run_wall_seconds=0.0,
        )
        payload["primary_metric"] = args.aggregate_metric
        payload["primary_metric_mean"] = summary["totals"]["aggregate_metric_mean"]
    print(json.dumps(payload, ensure_ascii=False, indent=2))
    return payload


def run_batch_dense_materialize(args: argparse.Namespace) -> dict[str, Any]:
    metadata = load_batch_metadata(target=args.target, workspace_root=Path(args.workspace_root))
    if metadata.provider != "openai":
        raise ValueError(f"Unsupported batch provider for materialize: {metadata.provider}")
    embeddings_by_task = collect_openai_batch_embeddings(metadata=metadata)
    args.model = metadata.model
    args.model_id = metadata.model
    args.model_source = {"type": metadata.provider, "name": metadata.model}
    args.model_loader = f"{metadata.provider}-batch"
    args.model_loader_kwargs = {
        "batch_id": metadata.batch_id,
        "target": metadata.target,
        "workspace_path": str(metadata.workspace_path),
    }
    args.model_revision = None
    args.dtype = "fp32"
    args.device = None
    args.attn_implementation = None
    args.flash_attn2 = False
    args.trust_remote_code = False
    args.model_max_seq_length = (metadata.config or {}).get("max_input_tokens")
    args.dataset_revision = metadata.dataset_revision

    environment = collect_runtime_environment()
    registry = DatasetRegistry.load_builtin()
    tasks = [_task_from_batch_payload(registry, task_payload) for task_payload in metadata.tasks]
    results: list[TaskRunResult] = []
    model_metadata: dict[str, Any] | None = None
    for task in tasks:
        dataset = _load_dataset_for_args(args, task)
        task_embeddings = embeddings_by_task[f"{task.dataset_id}::{task.split_name}"]
        query_ids = list(dataset.queries)
        corpus_ids = list(dataset.corpus)
        if query_ids != task_embeddings["query_ids"]:
            raise ValueError(f"Query id order mismatch for {task.dataset_id}::{task.split_name}.")
        if corpus_ids != task_embeddings["corpus_ids"]:
            raise ValueError(f"Corpus id order mismatch for {task.dataset_id}::{task.split_name}.")
        model = PrecomputedDenseEmbeddingModel(
            query_embeddings=task_embeddings["query_embeddings"],
            corpus_embeddings=task_embeddings["corpus_embeddings"],
            model_name=metadata.model,
            max_seq_length=args.model_max_seq_length,
            backend_metadata={
                "provider": metadata.provider,
                "api_endpoint": (metadata.api or {}).get("endpoint"),
                "batch_id": metadata.batch_id,
                "batch_target": metadata.target,
                "input_file_id": metadata.input_file_id,
                "output_file_id": metadata.output_file_id,
                "dimension_reduction": (metadata.config or {}).get("dimension_reduction"),
            },
        )
        model_metadata = collect_model_metadata(model, args)
        results.append(
            run_or_load_task(
                task=task,
                model=model,
                args=args,
                environment=environment,
                model_metadata=model_metadata,
                dataset_loader=lambda _task, dataset=dataset: dataset,
            )
        )
    if model_metadata is None:
        raise ValueError("No batch tasks were materialized.")
    summary = build_run_summary_payload(
        args=args,
        environment=environment,
        model_metadata=model_metadata,
        results=results,
        run_started_at_utc=datetime.now(timezone.utc).isoformat(),
        run_finished_at_utc=datetime.now(timezone.utc).isoformat(),
        run_wall_seconds=0.0,
    )
    print(
        json.dumps(
            {
                "primary_metric": args.aggregate_metric,
                "primary_metric_mean": summary["totals"]["aggregate_metric_mean"],
                "evaluated_count": summary["totals"]["evaluated_count"],
                "cache_hit_count": summary["totals"]["cache_hit_count"],
            },
            ensure_ascii=False,
            indent=2,
        )
    )
    return summary


def _materialize_precomputed_batch_task(
    *,
    args: argparse.Namespace,
    environment: dict[str, Any],
    task: EvalTask,
    dataset: LoadedIrDataset,
    task_embeddings: dict[str, Any],
    metadata: BatchMetadata,
) -> TaskRunResult:
    query_ids = list(dataset.queries)
    corpus_ids = list(dataset.corpus)
    if query_ids != task_embeddings["query_ids"]:
        raise ValueError(f"Query id order mismatch for {task.dataset_id}::{task.split_name}.")
    if corpus_ids != task_embeddings["corpus_ids"]:
        raise ValueError(f"Corpus id order mismatch for {task.dataset_id}::{task.split_name}.")
    args.model_loader_kwargs = {
        "batch_id": metadata.batch_id,
        "target": metadata.target,
        "workspace_path": str(metadata.workspace_path),
    }
    model = PrecomputedDenseEmbeddingModel(
        query_embeddings=task_embeddings["query_embeddings"],
        corpus_embeddings=task_embeddings["corpus_embeddings"],
        model_name=metadata.model,
        max_seq_length=args.model_max_seq_length,
        backend_metadata={
            "provider": metadata.provider,
            "api_endpoint": (metadata.api or {}).get("endpoint"),
            "batch_id": metadata.batch_id,
            "batch_target": metadata.target,
            "input_file_id": metadata.input_file_id,
            "output_file_id": metadata.output_file_id,
            "dimension_reduction": (metadata.config or {}).get("dimension_reduction"),
        },
    )
    model_metadata = collect_model_metadata(model, args)
    return run_or_load_task(
        task=task,
        model=model,
        args=args,
        environment=environment,
        model_metadata=model_metadata,
        dataset_loader=lambda _task: dataset,
    )


def _task_from_batch_payload(registry: DatasetRegistry, payload: dict[str, Any]) -> EvalTask:
    spec = registry.get_dataset(str(payload["dataset_id"]))
    return EvalTask(
        dataset=spec,
        split_name=str(payload["split_name"]),
        task_name=str(payload["task_name"]),
    )


def _batch_summary(metadata: Any) -> dict[str, Any]:
    return {
        "target": metadata.target,
        "provider": metadata.provider,
        "model_type": metadata.model_type,
        "model": metadata.model,
        "status": metadata.status,
        "batch_id": metadata.batch_id,
        "input_file_id": metadata.input_file_id,
        "output_file_id": metadata.output_file_id,
        "error_file_id": metadata.error_file_id,
        "request_count": metadata.request_count,
        "embedding_input_count": metadata.embedding_input_count,
        "workspace_path": str(metadata.workspace_path),
        "metadata_path": str(metadata.metadata_path),
        "input_file_path": str(metadata.input_file_path),
        "output_file_path": str(metadata.output_file_path),
        "error_file_path": str(metadata.error_file_path),
    }


def run_evaluate(args: argparse.Namespace) -> dict[str, Any]:
    run_started_at = datetime.now(timezone.utc)
    run_start = time.perf_counter()
    registry = DatasetRegistry.load_builtin()
    dataset_values = _dataset_values_for_args(args, registry)
    tasks = resolve_eval_tasks(
        registry=registry,
        dataset_values=dataset_values,
        collection_values=args.collection,
        split_values=args.split,
        evaluation_scope=args.evaluation_scope,
    )
    output_dir = Path(args.output_dir)
    pending_tasks = [
        task
        for task in tasks
        if args.override
        or existing_result_path_for_task(
            output_dir=output_dir,
            model_id=args.model_id,
            task=task,
            result_format=args.result_format,
        )
        is None
    ]
    environment = collect_runtime_environment()
    _warn_if_missing_attention_implementation(args)

    model: Any | None = None
    if args.model_type == "bm25":
        model_metadata = collect_bm25_metadata(args)
    elif pending_tasks:
        model = load_model(
            ModelLoadConfig(
                model_name_or_path=args.model,
                model_type=args.model_type,
                model_loader=args.model_loader,
                model_loader_kwargs=getattr(args, "model_loader_kwargs", {}),
                model_revision=args.model_revision,
                dtype=args.dtype,
                attn_implementation=args.attn_implementation,
                flash_attn2=args.flash_attn2,
                device=args.device,
                trust_remote_code=args.trust_remote_code,
                max_seq_length=args.model_max_seq_length,
                cross_encoder_kwargs=getattr(args, "cross_encoder_kwargs", {}),
                late_interaction_query_length=getattr(args, "late_interaction_query_length", None),
                late_interaction_document_length=getattr(args, "late_interaction_document_length", None),
                late_interaction_query_prefix=getattr(args, "late_interaction_query_prefix", None),
                late_interaction_document_prefix=getattr(args, "late_interaction_document_prefix", None),
                late_interaction_do_query_expansion=getattr(args, "late_interaction_do_query_expansion", None),
                late_interaction_attend_to_expansion_tokens=getattr(
                    args,
                    "late_interaction_attend_to_expansion_tokens",
                    None,
                ),
            )
        )
        model_metadata = collect_model_metadata(model, args)
    else:
        model_metadata = {
            "method": args.model_type,
            "id": args.model_id,
            "source": args.model_source,
            "device": args.device,
            "dtype": args.dtype,
            "trust_remote_code": args.trust_remote_code,
            "total_parameters": None,
            "trainable_parameters": None,
            "active_parameters": None,
        }

    results: list[TaskRunResult] = []
    encode_pool = None
    reranker_pool = None
    try:
        if model is not None and args.model_type == "dense" and args.encode_devices and pending_tasks:
            encode_pool = start_encode_pool(model, args.encode_devices)
            args.encode_pool = encode_pool
        if model is not None and args.model_type == "reranker" and pending_tasks:
            reranker_pool = _start_reranker_score_pool(model, args)
        for task in tasks:
            if (
                model is None
                and existing_result_path_for_task(
                    output_dir=output_dir,
                    model_id=args.model_id,
                    task=task,
                    result_format=args.result_format,
                )
                is not None
            ):
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
    finally:
        if encode_pool is not None:
            stop_encode_pool(model, encode_pool)
            args.encode_pool = None
        if reranker_pool is not None:
            _stop_reranker_score_pool(model, reranker_pool)
            args.reranker_runtime_score_kwargs = None

    if not pending_tasks and results and isinstance(results[0].payload.get("model"), dict):
        model_metadata = results[0].payload["model"]

    run_finished_at = datetime.now(timezone.utc)
    run_summary_payload = build_run_summary_payload(
        args=args,
        environment=environment,
        model_metadata=model_metadata,
        results=results,
        run_started_at_utc=run_started_at.isoformat(),
        run_finished_at_utc=run_finished_at.isoformat(),
        run_wall_seconds=float(time.perf_counter() - run_start),
    )
    if args.model_type != "bm25":
        write_evaluation_model_card(args=args, model_metadata=run_summary_payload["model"])
    print(
        json.dumps(
            {
                "primary_metric": args.aggregate_metric,
                "primary_metric_mean": run_summary_payload["totals"]["aggregate_metric_mean"],
                "evaluated_count": run_summary_payload["totals"]["evaluated_count"],
                "cache_hit_count": run_summary_payload["totals"]["cache_hit_count"],
            },
            ensure_ascii=False,
            indent=2,
        )
    )
    return run_summary_payload


def _warn_if_missing_attention_implementation(args: argparse.Namespace) -> None:
    if args.model_type == "bm25":
        return
    if getattr(args, "model_loader", None) == "openai":
        return
    if args.flash_attn2 or args.attn_implementation is not None:
        return
    print(MISSING_ATTENTION_IMPLEMENTATION_WARNING, file=sys.stderr)


def _start_reranker_score_pool(model: Any, args: argparse.Namespace) -> Any | None:
    score_kwargs = dict(getattr(args, "reranker_score_kwargs", {}) or {})
    args.reranker_runtime_score_kwargs = score_kwargs
    devices = score_kwargs.get("device")
    if not isinstance(devices, list) or not devices:
        return None

    start_pool = getattr(model, "start_multi_process_pool", None)
    if not callable(start_pool):
        return None

    pool = start_pool(target_devices=[str(device) for device in devices])
    runtime_score_kwargs = dict(score_kwargs)
    runtime_score_kwargs.pop("device", None)
    runtime_score_kwargs["pool"] = pool
    args.reranker_runtime_score_kwargs = runtime_score_kwargs
    return pool


def _stop_reranker_score_pool(model: Any, pool: Any) -> None:
    stop_pool = getattr(model, "stop_multi_process_pool", None)
    if callable(stop_pool):
        stop_pool(pool)


def run_build_bm25(args: argparse.Namespace) -> dict[str, Any]:
    registry = DatasetRegistry.load_builtin()
    dataset_values = _dataset_values_for_args(args, registry)
    tasks = resolve_eval_tasks(
        registry=registry,
        dataset_values=dataset_values,
        collection_values=args.collection,
        split_values=args.split,
        evaluation_scope=args.evaluation_scope,
    )
    config = bm25_config_from_args(args)
    results: list[BM25BuildResult] = []
    for task in tasks:
        dataset = _load_dataset_for_args(args, task)
        results.append(run_or_load_bm25_task(task=task, dataset=dataset, args=args, config=config))

    payload = {
        "generated_at_utc": results[-1].payload.get("generated_at_utc") if results else None,
        "candidates_dir": args.output_dir,
        "config": {
            "bm25": bm25_config_payload(config),
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
    print(
        json.dumps(
            {
                "candidate_config": config_name,
                "candidates_dir": args.output_dir,
                "evaluated_count": payload["totals"]["evaluated_count"],
                "cache_hit_count": payload["totals"]["cache_hit_count"],
            },
            ensure_ascii=False,
            indent=2,
        )
    )
    return payload


def run_web(args: argparse.Namespace) -> None:
    from hakari_bench.viewer.app import create_app
    from hakari_bench.viewer.store import LocalDuckDbStore, resolve_duckdb_location

    import uvicorn

    location = resolve_duckdb_location(
        data_dir=Path(args.data_dir),
        duckdb_path=Path(args.duckdb_path) if args.duckdb_path else None,
        source_results_dir=Path(args.source_results_dir) if args.source_results_dir else None,
        source_duckdb_path=Path(args.source_duckdb_path) if args.source_duckdb_path else None,
        hf_dataset_repo_id=args.hf_dataset_repo_id,
        hf_dataset_path=args.hf_dataset_path,
        hf_dataset_revision=args.hf_dataset_revision,
    )
    store = LocalDuckDbStore(location)
    store.start_background_sync()
    app = create_app(store=store, config_dir=Path(args.viewer_config_dir))
    print(f"Serving HAKARI-Bench viewer on http://{args.host}:{args.port}")
    print(f"Local DuckDB: {location.local_path}")
    if location.source_path is not None:
        print(f"Source DuckDB: {location.source_path}")
    if location.hf_source is not None:
        print(f"Source DuckDB: hf://datasets/{location.hf_source.repo_id}/{location.hf_source.filename}")
    uvicorn.run(app, host=args.host, port=args.port)


def _load_dataset_for_args(args: argparse.Namespace, task: EvalTask) -> LoadedIrDataset:
    model_type = getattr(args, "model_type", None)
    candidate_subset_name = (
        (getattr(args, "candidate_subset_name", None) or task.dataset.candidate_config)
        if model_type in {"dense", "sparse", "late-interaction", "bm25", "reranker"}
        else None
    )
    return load_ir_dataset(
        task,
        candidate_subset_name=candidate_subset_name,
        revision=getattr(args, "dataset_revision", None),
        restrict_corpus_to_candidates=model_type == "reranker",
    )


def _load_cached_task(*, args: argparse.Namespace, task: EvalTask) -> TaskRunResult:
    output_path = existing_result_path_for_task(
        output_dir=Path(args.output_dir),
        model_id=args.model_id,
        task=task,
        result_format=getattr(args, "result_format", None),
    )
    if output_path is None:
        output_path = result_path_for_task(
            output_dir=Path(args.output_dir),
            model_id=args.model_id,
            task=task,
            result_format=getattr(args, "result_format", None),
        )
    return TaskRunResult(
        task=task,
        cache_hit=True,
        output_path=output_path,
        payload=read_result_json(output_path),
    )


def _late_interaction_embedding_variants_are_supported(variants: list[dict[str, Any]]) -> bool:
    for variant in variants:
        transform = variant.get("transform", {})
        if transform.get("type") != "pipeline":
            return False
        steps = transform.get("steps")
        if not isinstance(steps, list) or not steps:
            return False
        if any(step.get("type") != "truncate" for step in steps):
            return False
    return True


def main(argv: list[str] | None = None) -> None:
    args = parse_args(argv)
    if args.command == "evaluate":
        run_evaluate(args)
        return
    if args.command == "build-candidates":
        run_build_bm25(args)
        return
    if args.command == "batch":
        run_batch(args)
        return
    if args.command == "web":
        run_web(args)
        return
    if args.command in {"validate-task-docs", "validate-benchmark-docs", "validation-benchmark-docs"}:
        run_validate_task_docs(args)
        return
    raise ValueError(f"Unsupported command: {args.command}")


def run_validate_task_docs(args: argparse.Namespace) -> None:
    metadata, issues = validate_task_docs(
        args.paths,
        docs_root=args.docs_root,
        metadata_root=args.metadata_root,
    )
    if issues:
        for issue in issues:
            print(f"{issue.path}: {issue.message}", file=sys.stderr)
        raise SystemExit(1)
    print(f"Validated {len(metadata)} task docs.")


if __name__ == "__main__":
    main()
