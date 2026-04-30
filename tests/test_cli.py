from __future__ import annotations

import argparse

from nano_ir_benchmark.cli import parse_args
from nano_ir_benchmark.datasets import EvalTask, NanoDatasetSpec


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


def test_parse_args_does_not_mix_default_dataset_into_collection() -> None:
    args = parse_args(["evaluate", "--model", "hotchpotch/model", "--collection", "MNanoBEIR"])

    assert args.dataset == []
    assert args.collection == ["MNanoBEIR"]


def test_load_dataset_for_args_uses_candidate_subset_for_bm25(monkeypatch) -> None:
    from nano_ir_benchmark.cli import _load_dataset_for_args

    calls: list[str | None] = []

    def fake_load_ir_dataset(task: EvalTask, *, candidate_subset_name: str | None = None) -> object:
        _ = task
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
        argparse.Namespace(model_type="bm25", candidate_subset_name="bm25"),
        task,
    )

    assert calls == ["bm25"]
