from __future__ import annotations

from nano_ir_benchmark.cli import parse_args


def test_parse_args_defaults_to_dense_bf16_nanobeir() -> None:
    args = parse_args(["evaluate", "--model", "hotchpotch/model"])

    assert args.command == "evaluate"
    assert args.model_type == "dense"
    assert args.dtype == "bf16"
    assert args.dataset == ["sentence-transformers/NanoBEIR-en"]
    assert args.output_dir == "output/results"


def test_parse_args_allows_bm25_evaluation_without_model_name() -> None:
    args = parse_args(
        [
            "evaluate",
            "--model-type",
            "bm25",
            "--bm25-tokenizer",
            "english_porter_stop",
        ]
    )

    assert args.model == "bm25/bm25s-okapi-english_porter_stop"
    assert args.bm25_tokenizer == "english_porter_stop"


def test_parse_args_accepts_wordseg_bm25_tokenizer() -> None:
    args = parse_args(
        [
            "evaluate",
            "--model-type",
            "bm25",
            "--bm25-tokenizer",
            "wordseg",
            "--bm25-tokenizer-name",
            "ja",
        ]
    )

    assert args.model == "bm25/bm25s-okapi-wordseg-ja"
    assert args.bm25_tokenizer == "wordseg"
    assert args.bm25_tokenizer_name == "ja"


def test_parse_args_accepts_build_bm25_options() -> None:
    args = parse_args(
        [
            "build-bm25",
            "--dataset",
            "NanoMLDR",
            "--split",
            "ja",
            "--top-k",
            "50",
            "--bm25-tokenizer",
            "stemmer",
            "--bm25-stemmer-algorithm",
            "french",
        ]
    )

    assert args.command == "build-bm25"
    assert args.dataset == ["NanoMLDR"]
    assert args.split == ["ja"]
    assert args.top_k == 50
    assert args.bm25_tokenizer == "stemmer"
    assert args.bm25_stemmer_algorithm == "french"


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
