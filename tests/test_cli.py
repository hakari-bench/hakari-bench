from __future__ import annotations

from nano_ir_benchmark.cli import parse_args


def test_parse_args_defaults_to_dense_bf16_nanobeir() -> None:
    args = parse_args(["evaluate", "--model", "hotchpotch/model"])

    assert args.command == "evaluate"
    assert args.model_type == "dense"
    assert args.dtype == "bf16"
    assert args.dataset == ["sentence-transformers/NanoBEIR-en"]
    assert args.output_dir == "output/results"


def test_parse_args_accepts_prompt_and_reranker_options() -> None:
    args = parse_args(
        [
            "evaluate",
            "--model",
            "hotchpotch/reranker",
            "--model-type",
            "reranker",
            "--query-prompt-name",
            "query",
            "--corpus-prompt",
            "passage: ",
            "--rerank-top-n",
            "50",
        ]
    )

    assert args.model_type == "reranker"
    assert args.query_prompt_name == "query"
    assert args.corpus_prompt == "passage: "
    assert args.rerank_top_n == 50


def test_parse_args_does_not_mix_default_dataset_into_collection() -> None:
    args = parse_args(["evaluate", "--model", "hotchpotch/model", "--collection", "MNanoBEIR"])

    assert args.dataset == []
    assert args.collection == ["MNanoBEIR"]
