from __future__ import annotations

import argparse

from nano_ir_benchmark.cli import parse_args
from nano_ir_benchmark.datasets import EvalTask, NanoDatasetSpec


def _pipeline_variant(name: str, *steps: dict[str, object]) -> dict[str, object]:
    return {"name": name, "transform": {"type": "pipeline", "steps": list(steps)}}


def _truncate_step(dim: int) -> dict[str, object]:
    return {"type": "truncate", "algorithm": "dimension_slice", "parameters": {"dim": dim}}


def _quantize_step(precision: str, *, target: str = "corpus") -> dict[str, object]:
    parameters: dict[str, object] = {
        "precision": precision,
        "target": target,
        "method": "corpus_only" if target == "corpus" else "query_and_corpus",
    }
    if precision in {"int8", "uint8"}:
        parameters["calibration"] = "corpus"
    return {
        "type": "quantize",
        "algorithm": "sentence_transformers_embedding_quantization",
        "parameters": parameters,
    }


def test_parse_args_defaults_to_dense_bf16_nanobeir() -> None:
    args = parse_args(["evaluate", "--model", "hotchpotch/model"])

    assert args.command == "evaluate"
    assert args.model_type == "dense"
    assert args.dtype == "bf16"
    assert args.dataset == ["hakari-bench/NanoBEIR-en"]
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


def test_parse_args_defaults_bm25_tokenizer_to_auto_when_omitted() -> None:
    args = parse_args(["evaluate", "--model-type", "bm25"])

    assert args.model == "bm25/bm25s-okapi-auto"
    assert args.bm25_tokenizer is None


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


def test_parse_args_accepts_web_viewer_options() -> None:
    args = parse_args(["web", "--host", "0.0.0.0", "--port", "28090", "--data-dir", "output/viewer"])

    assert args.command == "web"
    assert args.host == "0.0.0.0"
    assert args.port == 28090
    assert args.data_dir == "output/viewer"


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
            "--query-task",
            "retrieval",
            "--corpus-task",
            "retrieval",
            "--corpus-prompt",
            "passage: ",
            "--rerank-top-n",
            "50",
        ]
    )

    assert args.model_type == "reranker"
    assert args.query_prompt_name == "query"
    assert args.query_task == "retrieval"
    assert args.corpus_task == "retrieval"
    assert args.corpus_prompt == "passage: "
    assert args.rerank_top_n == 50


def test_parse_args_accepts_dataset_revision() -> None:
    args = parse_args(
        [
            "evaluate",
            "--model",
            "hotchpotch/model",
            "--dataset",
            "NanoJMTEB",
            "--dataset-revision",
            "abc123",
        ]
    )

    assert args.dataset_revision == "abc123"


def test_parse_args_accepts_embedding_variants() -> None:
    args = parse_args(
        [
            "evaluate",
            "--model",
            "hotchpotch/model",
            "--embedding-variant",
            "truncate:256,truncate:128",
        ]
    )

    assert args.embedding_variants == [
        _pipeline_variant("truncate_dim_256", _truncate_step(256)),
        _pipeline_variant("truncate_dim_128", _truncate_step(128)),
    ]


def test_parse_args_accepts_compact_truncate_embedding_variants() -> None:
    args = parse_args(
        [
            "evaluate",
            "--model",
            "hotchpotch/model",
            "--embedding-variant",
            "truncate:512,256,128",
        ]
    )

    assert [variant["name"] for variant in args.embedding_variants] == [
        "truncate_dim_512",
        "truncate_dim_256",
        "truncate_dim_128",
    ]
    assert [variant["transform"]["steps"][0]["parameters"]["dim"] for variant in args.embedding_variants] == [
        512,
        256,
        128,
    ]


def test_parse_args_accepts_quantized_embedding_variants() -> None:
    args = parse_args(
        [
            "evaluate",
            "--model",
            "hotchpotch/model",
            "--embedding-variant",
            "quantize:int8,ubinary",
        ]
    )

    assert args.embedding_variants == [
        _pipeline_variant("quantize_int8_docs", _quantize_step("int8")),
        _pipeline_variant("quantize_ubinary_docs", _quantize_step("ubinary")),
    ]


def test_parse_args_accepts_explicit_query_and_corpus_quantized_embedding_variants() -> None:
    args = parse_args(
        [
            "evaluate",
            "--model",
            "hotchpotch/model",
            "--embedding-variant",
            "quantize-both:int8,ubinary",
        ]
    )

    assert args.embedding_variants == [
        _pipeline_variant("quantize_int8_both", _quantize_step("int8", target="query_and_corpus")),
        _pipeline_variant("quantize_ubinary_both", _quantize_step("ubinary", target="query_and_corpus")),
    ]


def test_parse_args_accepts_embedding_variant_cross_product() -> None:
    args = parse_args(
        [
            "evaluate",
            "--model",
            "hotchpotch/model",
            "--embedding-variant-cross",
            "truncate:256,128,64",
            "quantize:int8,ubinary",
        ]
    )

    # Cross product variants are normalized into the same pipeline shape as
    # single variants. This keeps evaluation on one code path instead of adding
    # a separate truncate x quantize branch.
    assert args.embedding_variants == [
        _pipeline_variant("truncate_dim_256_quantize_int8_docs", _truncate_step(256), _quantize_step("int8")),
        _pipeline_variant("truncate_dim_256_quantize_ubinary_docs", _truncate_step(256), _quantize_step("ubinary")),
        _pipeline_variant("truncate_dim_128_quantize_int8_docs", _truncate_step(128), _quantize_step("int8")),
        _pipeline_variant("truncate_dim_128_quantize_ubinary_docs", _truncate_step(128), _quantize_step("ubinary")),
        _pipeline_variant("truncate_dim_64_quantize_int8_docs", _truncate_step(64), _quantize_step("int8")),
        _pipeline_variant("truncate_dim_64_quantize_ubinary_docs", _truncate_step(64), _quantize_step("ubinary")),
    ]


def test_parse_args_does_not_mix_default_dataset_into_collection() -> None:
    args = parse_args(["evaluate", "--model", "hotchpotch/model", "--collection", "MNanoBEIR"])

    assert args.dataset == []
    assert args.collection == ["MNanoBEIR"]


def test_load_dataset_for_args_uses_candidate_subset_for_bm25(monkeypatch) -> None:
    from nano_ir_benchmark.cli import _load_dataset_for_args

    calls: list[str | None] = []

    def fake_load_ir_dataset(
        task: EvalTask,
        *,
        candidate_subset_name: str | None = None,
        revision: str | None = None,
    ) -> object:
        _ = task
        assert revision == "abc123"
        calls.append(candidate_subset_name)
        return object()

    monkeypatch.setattr("nano_ir_benchmark.cli.load_ir_dataset", fake_load_ir_dataset)
    task = EvalTask(
        dataset=NanoDatasetSpec(
            name="Toy",
            dataset_id="toy/data",
            corpus_config="corpus",
            queries_config="queries",
            qrels_config="qrels",
            candidate_config="bm25",
        ),
        split_name="test",
        task_name="test",
    )

    _load_dataset_for_args(
        argparse.Namespace(model_type="bm25", candidate_subset_name="bm25", dataset_revision="abc123"),
        task,
    )

    assert calls == ["bm25"]
