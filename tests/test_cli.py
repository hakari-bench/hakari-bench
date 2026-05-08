from __future__ import annotations

import argparse
import json

from hakari_bench.cli import build_parser, parse_args
from hakari_bench.datasets import EvalTask, NanoDatasetSpec
from hakari_bench.results import TaskRunResult


def _pipeline_variant(name: str, *steps: dict[str, object]) -> dict[str, object]:
    return {"name": name, "transform": {"type": "pipeline", "steps": list(steps)}}


def _truncate_step(dim: int) -> dict[str, object]:
    return {"type": "truncate", "algorithm": "dimension_slice", "parameters": {"dim": dim}}


def _normalize_step() -> dict[str, object]:
    return {"type": "normalize", "algorithm": "l2", "parameters": {}}


def _truncate_sparse_max_dims_step(max_dims: int, *, target: str = "query") -> dict[str, object]:
    return {
        "type": "truncate_sparse_max_dims",
        "algorithm": "top_abs_values_per_row",
        "parameters": {"max_dims": max_dims, "target": target},
    }


def _quantized_step(precision: str, *, rescore: bool = False, device: str | None = None) -> dict[str, object]:
    parameters: dict[str, object] = {
        "precision": precision,
        "target": "query_and_corpus",
        "method": "query_and_corpus",
        "score_representation": "torch_exact_rescore" if rescore else "torch_exact",
    }
    if precision == "int8":
        parameters["calibration"] = "corpus"
    if device is not None:
        parameters["search_device"] = device
    return {
        "type": "quantize",
        "algorithm": "sentence_transformers_embedding_quantization",
        "parameters": parameters,
    }


def _quantized_variant(
    name: str,
    precision: str,
    *,
    rescore: bool = False,
    device: str | None = None,
) -> dict[str, object]:
    return _pipeline_variant(name, _normalize_step(), _quantized_step(precision, rescore=rescore, device=device))


def _default_dense_quantized_variants() -> list[dict[str, object]]:
    return [
        _quantized_variant("int8", "int8"),
        _quantized_variant("binary", "binary"),
        _quantized_variant("int8_rescore", "int8", rescore=True),
        _quantized_variant("binary_rescore", "binary", rescore=True),
    ]


def _truncate_quantized_variants(*dims: int) -> list[dict[str, object]]:
    variants: list[dict[str, object]] = []
    for dim in dims:
        variants.extend(
            [
                _pipeline_variant(f"truncate_dim_{dim}_int8", _truncate_step(dim), _normalize_step(), _quantized_step("int8")),
                _pipeline_variant(
                    f"truncate_dim_{dim}_binary",
                    _truncate_step(dim),
                    _normalize_step(),
                    _quantized_step("binary"),
                ),
                _pipeline_variant(
                    f"truncate_dim_{dim}_int8_rescore",
                    _truncate_step(dim),
                    _normalize_step(),
                    _quantized_step("int8", rescore=True),
                ),
                _pipeline_variant(
                    f"truncate_dim_{dim}_binary_rescore",
                    _truncate_step(dim),
                    _normalize_step(),
                    _quantized_step("binary", rescore=True),
                ),
            ]
        )
    return variants


def test_parse_args_defaults_to_dense_bf16_nanobeir() -> None:
    args = parse_args(["evaluate", "dense", "--model", "hotchpotch/model"])

    assert args.command == "evaluate"
    assert args.model_type == "dense"
    assert args.model_id == "hotchpotch/model"
    assert args.model_source == {"type": "huggingface", "name": "hotchpotch/model"}
    assert args.dtype == "bf16"
    assert args.retrieval_score_device == "auto"
    assert args.dataset == ["hakari-bench/NanoBEIR-en"]
    assert args.results_dir == "output/results"
    assert args.embedding_variants == _default_dense_quantized_variants()


def test_parse_args_normalizes_local_model_alias() -> None:
    args = parse_args(["evaluate", "dense", "--model", "/local_model_A/", "--model-alias", "model_A"])

    assert args.model == "/local_model_A/"
    assert args.model_alias == "model_A"
    assert args.model_id == "local/model_A"
    assert args.model_source == {"type": "local_path", "path": "/local_model_A"}


def test_parse_args_preserves_namespaced_local_model_alias() -> None:
    args = parse_args(["evaluate", "dense", "--model", "/local_model_A/", "--model-alias", "local/model_A"])

    assert args.model_id == "local/model_A"


def test_evaluate_dense_help_excludes_bm25_options(capsys) -> None:
    try:
        build_parser().parse_args(["evaluate", "dense", "--help"])
    except SystemExit as exc:
        assert exc.code == 0
    else:
        raise AssertionError("Expected --help to exit.")
    help_text = capsys.readouterr().out

    assert "--bm25-top-k" not in help_text
    assert "--bm25-tokenizer" not in help_text
    assert "--reranker-init-kwargs-json" not in help_text


def test_parse_args_accepts_structured_params_json() -> None:
    args = parse_args(
        [
            "evaluate",
            "dense",
            "--params-json",
            (
                '{"model":{"source":"/local_model_A/","alias":"model_A"},'
                '"target":{"collections":["MNanoBEIR"]},'
                '"runtime":{"batch_size":16,"dtype":"fp16",'
                '"encode_devices":["cuda:0","cuda:1"],"encode_chunk_size":64},'
                '"output":{"results_dir":"output/custom","overwrite":true}}'
            ),
        ]
    )

    assert args.model == "/local_model_A/"
    assert args.model_id == "local/model_A"
    assert args.collection == ["MNanoBEIR"]
    assert args.dataset == []
    assert args.batch_size == 16
    assert args.dtype == "fp16"
    assert args.encode_devices == ["cuda:0", "cuda:1"]
    assert args.encode_chunk_size == 64
    assert args.results_dir == "output/custom"
    assert args.overwrite is True


def test_parse_args_accepts_dense_encode_devices() -> None:
    args = parse_args(
        [
            "evaluate",
            "dense",
            "--model",
            "hotchpotch/model",
            "--encode-devices",
            "cuda:0,cuda:1",
            "--encode-chunk-size",
            "128",
        ]
    )

    assert args.encode_devices == ["cuda:0", "cuda:1"]
    assert args.encode_chunk_size == 128


def test_parse_args_rejects_unknown_params_json_key() -> None:
    try:
        parse_args(["evaluate", "dense", "--params-json", '{"model":{"source":"hotchpotch/model"},"unknown":{}}'])
    except SystemExit as exc:
        assert exc.code == 2
    else:
        raise AssertionError("Expected unknown params JSON keys to be rejected.")


def test_parse_args_rejects_unknown_nested_params_json_key() -> None:
    try:
        parse_args(
            [
                "evaluate",
                "dense",
                "--params-json",
                '{"model":{"source":"hotchpotch/model"},"runtime":{"batch_size":16,"unknown":true}}',
            ]
        )
    except SystemExit as exc:
        assert exc.code == 2
    else:
        raise AssertionError("Expected unknown nested params JSON keys to be rejected.")


def test_parse_args_rejects_invalid_params_json_values() -> None:
    try:
        parse_args(
            [
                "evaluate",
                "dense",
                "--params-json",
                '{"model":{"source":"hotchpotch/model"},"runtime":{"dtype":"float16","batch_size":true}}',
            ]
        )
    except SystemExit as exc:
        assert exc.code == 2
    else:
        raise AssertionError("Expected invalid params JSON values to be rejected.")


def test_parser_uses_hakari_bench_identity() -> None:
    parser = build_parser()

    assert parser.description == "HAKARI-Bench runner"
    assert "HAKARI-Bench" in parser.format_help()


def test_parse_args_web_defaults_to_hakari_bench_paths() -> None:
    args = parse_args(["web"])

    assert args.duckdb_path is None
    assert args.source_results_dir == "../hakari-bench/output/results"


def test_parse_args_defaults_to_quantized_variants_on_cpu() -> None:
    args = parse_args(["evaluate", "dense", "--model", "hotchpotch/model", "--device", "cpu"])

    assert args.embedding_variants == _default_dense_quantized_variants()


def test_parse_args_defaults_to_quantized_variants_on_cuda() -> None:
    args = parse_args(["evaluate", "dense", "--model", "hotchpotch/model", "--device", "cuda"])

    assert args.embedding_variants == _default_dense_quantized_variants()


def test_parse_args_score_device_cpu_forces_cpu_quantized_matrix_work() -> None:
    args = parse_args(
        ["evaluate", "dense", "--model", "hotchpotch/model", "--device", "cuda", "--retrieval-score-device", "cpu"]
    )

    assert args.retrieval_score_device == "cpu"
    assert args.embedding_variants == [
        _quantized_variant("int8", "int8", device="cpu"),
        _quantized_variant("binary", "binary", device="cpu"),
        _quantized_variant("int8_rescore", "int8", rescore=True, device="cpu"),
        _quantized_variant("binary_rescore", "binary", rescore=True, device="cpu"),
    ]


def test_parse_args_score_device_cuda_forces_cuda_quantized_matrix_work() -> None:
    args = parse_args(
        ["evaluate", "dense", "--model", "hotchpotch/model", "--device", "cpu", "--retrieval-score-device", "cuda"]
    )

    assert args.retrieval_score_device == "cuda"
    assert args.embedding_variants == [
        _quantized_variant("int8", "int8", device="cuda"),
        _quantized_variant("binary", "binary", device="cuda"),
        _quantized_variant("int8_rescore", "int8", rescore=True, device="cuda"),
        _quantized_variant("binary_rescore", "binary", rescore=True, device="cuda"),
    ]


def test_parse_args_can_disable_default_dense_quantized_variants() -> None:
    args = parse_args(["evaluate", "dense", "--model", "hotchpotch/model", "--no-default-embedding-variants"])

    assert args.embedding_variants == []


def test_parse_args_no_default_keeps_explicit_truncate_variants_only() -> None:
    args = parse_args(
        [
            "evaluate",
            "dense",
            "--model",
            "hotchpotch/model",
            "--no-default-embedding-variants",
            "--embedding-variant",
            "truncate:256",
        ]
    )

    assert args.embedding_variants == [
        _pipeline_variant("truncate_dim_256", _truncate_step(256)),
    ]


def test_parse_args_does_not_add_default_quantized_variants_to_sparse_models() -> None:
    args = parse_args(
        [
            "evaluate",
            "sparse",
            "--model",
            "naver/splade-v3",
        ]
    )

    assert args.embedding_variants == []


def test_parse_args_accepts_late_interaction_options() -> None:
    args = parse_args(
        [
            "evaluate",
            "late-interaction",
            "--model",
            "lightonai/GTE-ModernColBERT-v1",
            "--late-interaction-query-length",
            "64",
            "--late-interaction-document-length",
            "300",
            "--late-interaction-query-prefix",
            "[QueryMarker]",
            "--late-interaction-document-prefix",
            "[DocumentMarker]",
            "--late-interaction-attend-to-expansion-tokens",
            "--late-interaction-exact-doc-batch-size",
            "16",
            "--late-interaction-exact-query-batch-size",
            "4",
            "--embedding-variant",
            "truncate:96,64",
        ]
    )

    assert args.model_type == "late-interaction"
    assert args.late_interaction_query_length == 64
    assert args.late_interaction_document_length == 300
    assert args.late_interaction_query_prefix == "[QueryMarker]"
    assert args.late_interaction_document_prefix == "[DocumentMarker]"
    assert args.late_interaction_attend_to_expansion_tokens is True
    assert args.late_interaction_exact_doc_batch_size == 16
    assert args.late_interaction_exact_query_batch_size == 4
    assert args.embedding_variants == [
        _pipeline_variant("truncate_dim_96", _truncate_step(96)),
        _pipeline_variant("truncate_dim_64", _truncate_step(64)),
    ]


def test_parse_args_adds_default_quantized_variants_when_variants_are_explicit() -> None:
    args = parse_args(
        [
            "evaluate",
            "dense",
            "--model",
            "hotchpotch/model",
            "--embedding-variant",
            "truncate:256",
        ]
    )

    assert args.embedding_variants == [
        _pipeline_variant("truncate_dim_256", _truncate_step(256)),
        *_default_dense_quantized_variants(),
        *_truncate_quantized_variants(256),
    ]


def test_parse_args_allows_bm25_evaluation_without_model_name() -> None:
    args = parse_args(
        [
            "evaluate",
            "bm25",
            "--bm25-source",
            "computed",
            "--bm25-tokenizer",
            "english_porter_stop",
        ]
    )

    assert args.model == "bm25/bm25s-okapi-english_porter_stop"
    assert args.model_id == "bm25/bm25s-okapi-english_porter_stop"
    assert args.bm25_tokenizer == "english_porter_stop"
    assert args.truncate_dim is None
    assert args.trust_remote_code is False
    assert args.query_prompt is None
    assert args.document_prompt is None
    assert args.query_prompt_name is None
    assert args.document_prompt_name is None


def test_parse_args_defaults_bm25_tokenizer_to_auto_when_omitted() -> None:
    args = parse_args(["evaluate", "bm25"])

    assert args.model == "bm25/dataset-bm25"
    assert args.bm25_source == "dataset"
    assert args.bm25_tokenizer is None


def test_parse_args_accepts_wordseg_bm25_tokenizer() -> None:
    args = parse_args(
        [
            "evaluate",
            "bm25",
            "--bm25-source",
            "computed",
            "--bm25-tokenizer",
            "wordseg",
            "--bm25-wordseg-language",
            "ja",
        ]
    )

    assert args.model == "bm25/bm25s-okapi-wordseg-ja"
    assert args.bm25_tokenizer == "wordseg"
    assert args.bm25_wordseg_language == "ja"


def test_parse_args_rejects_bm25_tokenizer_with_dataset_source() -> None:
    try:
        parse_args(["evaluate", "bm25", "--bm25-tokenizer", "english_porter_stop"])
    except SystemExit as exc:
        assert exc.code == 2
    else:
        raise AssertionError("Expected dataset-source BM25 evaluation to reject tokenizer options.")


def test_parse_args_accepts_build_bm25_options() -> None:
    args = parse_args(
        [
            "build-candidates",
            "bm25",
            "--dataset",
            "NanoMLDR",
            "--split",
            "ja",
            "--bm25-top-k",
            "50",
            "--bm25-tokenizer",
            "stemmer",
            "--bm25-stemmer-language",
            "french",
        ]
    )

    assert args.command == "build-candidates"
    assert args.candidate_method == "bm25"
    assert args.dataset == ["NanoMLDR"]
    assert args.split == ["ja"]
    assert args.bm25_top_k == 50
    assert args.bm25_tokenizer == "stemmer"
    assert args.bm25_stemmer_language == "french"


def test_parse_args_accepts_build_bm25_params_json() -> None:
    args = parse_args(
        [
            "build-candidates",
            "bm25",
            "--params-json",
            json.dumps(
                {
                    "target": {"datasets": ["NanoMLDR"], "splits": ["ja"]},
                    "output": {"candidates_dir": "output/custom-candidates", "overwrite": True},
                    "bm25": {"top_k": 50, "tokenizer": "wordseg", "wordseg_language": "ja"},
                }
            ),
        ]
    )

    assert args.command == "build-candidates"
    assert args.candidate_method == "bm25"
    assert args.dataset == ["NanoMLDR"]
    assert args.split == ["ja"]
    assert args.candidates_dir == "output/custom-candidates"
    assert args.output_dir == "output/custom-candidates"
    assert args.overwrite is True
    assert args.override is True
    assert args.bm25_top_k == 50
    assert args.bm25_tokenizer == "wordseg"
    assert args.bm25_wordseg_language == "ja"


def test_parse_args_rejects_build_bm25_output_results_dir_params_json() -> None:
    try:
        parse_args(
            [
                "build-candidates",
                "bm25",
                "--params-json",
                json.dumps({"output": {"results_dir": "output/results"}}),
            ]
        )
    except SystemExit as exc:
        assert exc.code == 2
    else:
        raise AssertionError("Expected build-candidates params JSON to reject results_dir.")


def test_parse_args_rejects_build_bm25_source_params_json() -> None:
    try:
        parse_args(
            [
                "build-candidates",
                "bm25",
                "--params-json",
                json.dumps({"bm25": {"source": "computed"}}),
            ]
        )
    except SystemExit as exc:
        assert exc.code == 2
    else:
        raise AssertionError("Expected build-candidates params JSON to reject bm25.source.")


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
            "reranker",
            "--model",
            "hotchpotch/reranker",
            "--reranker-init-kwargs-json",
            '{"prompts":{"retrieval":"Retrieve relevant passages"},"default_prompt_name":"retrieval"}',
            "--reranker-inference-kwargs-json",
            '{"prompt_name":"retrieval"}',
            "--rerank-top-k",
            "50",
        ]
    )

    assert args.model_type == "reranker"
    assert args.cross_encoder_kwargs == {
        "prompts": {"retrieval": "Retrieve relevant passages"},
        "default_prompt_name": "retrieval",
    }
    assert args.reranker_score_kwargs == {"prompt_name": "retrieval"}
    assert args.rerank_top_k == 50


def test_parse_args_rejects_cross_encoder_kwargs_for_dense_model() -> None:
    try:
        parse_args(
            [
                "evaluate",
                "dense",
                "--model",
                "hotchpotch/model",
                "--reranker-init-kwargs-json",
                '{"default_prompt_name":"query"}',
            ]
        )
    except SystemExit as exc:
        assert exc.code == 2
    else:
        raise AssertionError("Expected cross encoder kwargs to require reranker model type.")


def test_parse_args_rejects_non_positive_rerank_top_n() -> None:
    try:
        parse_args(
            [
                "evaluate",
                "reranker",
                "--model",
                "hotchpotch/reranker",
                "--rerank-top-k",
                "0",
            ]
        )
    except SystemExit as exc:
        assert exc.code == 2
    else:
        raise AssertionError("Expected --rerank-top-k 0 to be rejected.")


def test_parse_args_accepts_query_and_docs_truncate_sparse_max_dims() -> None:
    args = parse_args(
        [
            "evaluate",
            "sparse",
            "--model",
            "naver/splade-v3",
            "--sparse-query-max-active-dims",
            "32",
            "--sparse-document-max-active-dims",
            "128",
        ]
    )

    assert args.model_type == "sparse"
    assert args.sparse_query_max_active_dims == 32
    assert args.sparse_document_max_active_dims == 128


def test_parse_args_rejects_sparse_query_max_active_dims_for_dense_model() -> None:
    try:
        parse_args(
            [
                "evaluate",
                "dense",
                "--model",
                "hotchpotch/model",
                "--sparse-query-max-active-dims",
                "128",
            ]
        )
    except SystemExit as exc:
        assert exc.code == 2
    else:
        raise AssertionError("Expected --sparse-query-max-active-dims to require evaluate sparse.")


def test_parse_args_rejects_legacy_sparse_max_active_dims_alias() -> None:
    try:
        parse_args(
            [
                "evaluate",
                "sparse",
                "--model",
                "naver/splade-v3",
                "--sparse-max-active-dims",
                "128",
            ]
        )
    except SystemExit as exc:
        assert exc.code == 2
    else:
        raise AssertionError("Expected legacy sparse max active dims option to be rejected.")


def test_parse_args_accepts_dataset_revision() -> None:
    args = parse_args(
        [
            "evaluate",
            "dense",
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
            "dense",
            "--model",
            "hotchpotch/model",
            "--embedding-variant",
            "truncate:256,truncate:128",
        ]
    )

    assert args.embedding_variants == [
        _pipeline_variant("truncate_dim_256", _truncate_step(256)),
        _pipeline_variant("truncate_dim_128", _truncate_step(128)),
        *_default_dense_quantized_variants(),
        *_truncate_quantized_variants(256, 128),
    ]


def test_parse_args_accepts_compact_truncate_embedding_variants() -> None:
    args = parse_args(
        [
            "evaluate",
            "dense",
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
        "int8",
        "binary",
        "int8_rescore",
        "binary_rescore",
        "truncate_dim_512_int8",
        "truncate_dim_512_binary",
        "truncate_dim_512_int8_rescore",
        "truncate_dim_512_binary_rescore",
        "truncate_dim_256_int8",
        "truncate_dim_256_binary",
        "truncate_dim_256_int8_rescore",
        "truncate_dim_256_binary_rescore",
        "truncate_dim_128_int8",
        "truncate_dim_128_binary",
        "truncate_dim_128_int8_rescore",
        "truncate_dim_128_binary_rescore",
    ]
    assert [variant["transform"]["steps"][0]["parameters"]["dim"] for variant in args.embedding_variants[:3]] == [
        512,
        256,
        128,
    ]


def test_parse_args_accepts_query_truncate_sparse_max_dims_embedding_variants() -> None:
    args = parse_args(
        [
            "evaluate",
            "sparse",
            "--model",
            "naver/splade-v3",
            "--embedding-variant",
            "sparse-query-max-active-dims:128,64",
        ]
    )

    assert args.embedding_variants == [
        _pipeline_variant("sparse_query_max_active_dims_128", _truncate_sparse_max_dims_step(128, target="query")),
        _pipeline_variant("sparse_query_max_active_dims_64", _truncate_sparse_max_dims_step(64, target="query")),
    ]


def test_parse_args_rejects_legacy_sparse_max_active_dims_embedding_variant() -> None:
    try:
        parse_args(
            [
                "evaluate",
                "sparse",
                "--model",
                "naver/splade-v3",
                "--embedding-variant",
                "sparse-max-active-dims:128",
            ]
        )
    except SystemExit as exc:
        assert exc.code == 2
    else:
        raise AssertionError("Expected legacy sparse max active dims embedding variant to be rejected.")


def test_parse_args_accepts_query_and_docs_truncate_sparse_max_dims_cross_product() -> None:
    args = parse_args(
        [
            "evaluate",
            "sparse",
            "--model",
            "naver/splade-v3",
            "--embedding-variant-grid",
            "sparse-query-max-active-dims:8,16,32",
            "sparse-document-max-active-dims:64,128,256",
        ]
    )

    assert args.embedding_variants == [
        _pipeline_variant(
            "sparse_query_max_active_dims_8_sparse_document_max_active_dims_64",
            _truncate_sparse_max_dims_step(8, target="query"),
            _truncate_sparse_max_dims_step(64, target="corpus"),
        ),
        _pipeline_variant(
            "sparse_query_max_active_dims_8_sparse_document_max_active_dims_128",
            _truncate_sparse_max_dims_step(8, target="query"),
            _truncate_sparse_max_dims_step(128, target="corpus"),
        ),
        _pipeline_variant(
            "sparse_query_max_active_dims_8_sparse_document_max_active_dims_256",
            _truncate_sparse_max_dims_step(8, target="query"),
            _truncate_sparse_max_dims_step(256, target="corpus"),
        ),
        _pipeline_variant(
            "sparse_query_max_active_dims_16_sparse_document_max_active_dims_64",
            _truncate_sparse_max_dims_step(16, target="query"),
            _truncate_sparse_max_dims_step(64, target="corpus"),
        ),
        _pipeline_variant(
            "sparse_query_max_active_dims_16_sparse_document_max_active_dims_128",
            _truncate_sparse_max_dims_step(16, target="query"),
            _truncate_sparse_max_dims_step(128, target="corpus"),
        ),
        _pipeline_variant(
            "sparse_query_max_active_dims_16_sparse_document_max_active_dims_256",
            _truncate_sparse_max_dims_step(16, target="query"),
            _truncate_sparse_max_dims_step(256, target="corpus"),
        ),
        _pipeline_variant(
            "sparse_query_max_active_dims_32_sparse_document_max_active_dims_64",
            _truncate_sparse_max_dims_step(32, target="query"),
            _truncate_sparse_max_dims_step(64, target="corpus"),
        ),
        _pipeline_variant(
            "sparse_query_max_active_dims_32_sparse_document_max_active_dims_128",
            _truncate_sparse_max_dims_step(32, target="query"),
            _truncate_sparse_max_dims_step(128, target="corpus"),
        ),
        _pipeline_variant(
            "sparse_query_max_active_dims_32_sparse_document_max_active_dims_256",
            _truncate_sparse_max_dims_step(32, target="query"),
            _truncate_sparse_max_dims_step(256, target="corpus"),
        ),
    ]


def test_parse_args_rejects_quantized_embedding_variants_for_sparse_model() -> None:
    rejected_specs = [
        "int8",
        "binary",
        "rescore:int8",
        "binary-rescore",
        "quantize:int8",
        "quantize-docs:int8",
        "quantize-both:int8",
        "quantize-code:int8",
        "quantize-sample:int8:128",
    ]

    for spec in rejected_specs:
        try:
            parse_args(
                [
                    "evaluate",
                    "sparse",
                    "--model",
                    "naver/splade-v3",
                    "--embedding-variant",
                    spec,
                ]
            )
        except SystemExit as exc:
            assert exc.code == 2
        else:
            raise AssertionError(f"Expected sparse model to reject quantized embedding variant {spec!r}.")


def test_parse_args_rejects_quantized_cross_embedding_variants_for_sparse_model() -> None:
    try:
        parse_args(
            [
                "evaluate",
                "sparse",
                "--model",
                "naver/splade-v3",
                "--embedding-variant-grid",
                "sparse-query-max-active-dims:128",
                "int8",
            ]
        )
    except SystemExit as exc:
        assert exc.code == 2
    else:
        raise AssertionError("Expected sparse model to reject quantized cross embedding variants.")


def test_parse_args_rejects_quantized_embedding_variants_for_all_non_dense_models() -> None:
    model_args_by_type = {
        "late-interaction": ["late-interaction", "--model", "hotchpotch/colbert-model"],
        "reranker": ["reranker", "--model", "hotchpotch/reranker"],
        "bm25": [],
    }

    for model_type, model_args in model_args_by_type.items():
        for spec in ["int8", "binary", "rescore:int8", "binary-rescore"]:
            try:
                parse_args(
                    [
                        "evaluate",
                        *model_args,
                        *(["bm25"] if model_type == "bm25" else []),
                        "--embedding-variant",
                        spec,
                    ]
                )
            except SystemExit as exc:
                assert exc.code == 2
            else:
                raise AssertionError(
                    f"Expected {model_type} model to reject quantized embedding variant {spec!r}."
                )


def test_parse_args_rejects_quantized_cross_embedding_variants_for_non_dense_models() -> None:
    try:
        parse_args(
            [
                "evaluate",
                "late-interaction",
                "--model",
                "hotchpotch/colbert-model",
                "--embedding-variant-grid",
                "truncate:128",
                "int8",
            ]
        )
    except SystemExit as exc:
        assert exc.code == 2
    else:
        raise AssertionError("Expected late-interaction model to reject quantized cross embedding variants.")


def test_parse_args_rejects_legacy_quantize_and_backend_prefixed_embedding_variants() -> None:
    rejected_specs = [
        "quantize:int8",
        "quantize-docs:int8",
        "quantize-both:int8",
        "quantize-code:int8",
        "quantize-sample:int8:128",
        "usearch:int8",
        "usearch-rescore:binary",
        "numpy:int8",
        "numpy-rescore:binary",
        "torch:int8",
        "torch-rescore:binary",
        "cuda:int8",
        "cuda-rescore:binary",
    ]

    for spec in rejected_specs:
        try:
            parse_args(
                [
                    "evaluate",
                    "dense",
                    "--model",
                    "hotchpotch/model",
                    "--embedding-variant",
                    spec,
                ]
            )
        except SystemExit as exc:
            assert exc.code == 2
        else:
            raise AssertionError(f"Expected legacy/backend-prefixed variant {spec!r} to be rejected.")


def test_parse_args_accepts_quantized_embedding_variants() -> None:
    args = parse_args(
        [
            "evaluate",
            "dense",
            "--model",
            "hotchpotch/model",
            "--embedding-variant",
            "int8,binary",
            "--embedding-variant",
            "rescore:int8,binary",
        ]
    )

    assert args.embedding_variants == [
        _quantized_variant("int8", "int8"),
        _quantized_variant("binary", "binary"),
        _quantized_variant("int8_rescore", "int8", rescore=True),
        _quantized_variant("binary_rescore", "binary", rescore=True),
    ]


def test_parse_args_accepts_suffix_rescore_quantized_embedding_variants() -> None:
    args = parse_args(
        [
            "evaluate",
            "dense",
            "--model",
            "hotchpotch/model",
            "--embedding-variant",
            "int8-rescore",
            "--embedding-variant",
            "binary_rescore",
        ]
    )

    assert args.embedding_variants == [
        _quantized_variant("int8_rescore", "int8", rescore=True),
        _quantized_variant("binary_rescore", "binary", rescore=True),
        _quantized_variant("int8", "int8"),
        _quantized_variant("binary", "binary"),
    ]


def test_parse_args_accepts_normalize_embedding_variant() -> None:
    args = parse_args(
        [
            "evaluate",
            "dense",
            "--model",
            "hotchpotch/model",
            "--embedding-variant",
            "normalize",
        ]
    )

    assert args.embedding_variants == [
        _pipeline_variant("normalize", _normalize_step()),
        *_default_dense_quantized_variants(),
    ]


def test_parse_args_default_dense_variants_fill_missing_explicit_quantized_variants() -> None:
    args = parse_args(
        [
            "evaluate",
            "dense",
            "--model",
            "hotchpotch/model",
            "--embedding-variant",
            "int8",
        ]
    )

    assert args.embedding_variants == _default_dense_quantized_variants()


def test_parse_args_dedupes_auto_truncate_quantized_variants_against_explicit_grid() -> None:
    args = parse_args(
        [
            "evaluate",
            "dense",
            "--model",
            "hotchpotch/model",
            "--embedding-variant",
            "truncate:128",
            "--embedding-variant-grid",
            "truncate:128",
            "int8",
        ]
    )

    assert args.embedding_variants == [
        _pipeline_variant("truncate_dim_128", _truncate_step(128)),
        _pipeline_variant("truncate_dim_128_int8", _truncate_step(128), _normalize_step(), _quantized_step("int8")),
        *_default_dense_quantized_variants(),
        _pipeline_variant(
            "truncate_dim_128_binary",
            _truncate_step(128),
            _normalize_step(),
            _quantized_step("binary"),
        ),
        _pipeline_variant(
            "truncate_dim_128_int8_rescore",
            _truncate_step(128),
            _normalize_step(),
            _quantized_step("int8", rescore=True),
        ),
        _pipeline_variant(
            "truncate_dim_128_binary_rescore",
            _truncate_step(128),
            _normalize_step(),
            _quantized_step("binary", rescore=True),
        ),
    ]


def test_parse_args_accepts_embedding_variant_cross_product() -> None:
    args = parse_args(
        [
            "evaluate",
            "dense",
            "--model",
            "hotchpotch/model",
            "--embedding-variant-grid",
            "truncate:256,128,64",
            "int8,binary",
        ]
    )

    # Cross product variants are normalized into the same pipeline shape as
    # single variants. This keeps evaluation on one code path instead of adding
    # a separate truncate x quantize branch.
    assert args.embedding_variants == [
        _pipeline_variant("truncate_dim_256_int8", _truncate_step(256), _normalize_step(), _quantized_step("int8")),
        _pipeline_variant("truncate_dim_256_binary", _truncate_step(256), _normalize_step(), _quantized_step("binary")),
        _pipeline_variant("truncate_dim_128_int8", _truncate_step(128), _normalize_step(), _quantized_step("int8")),
        _pipeline_variant("truncate_dim_128_binary", _truncate_step(128), _normalize_step(), _quantized_step("binary")),
        _pipeline_variant("truncate_dim_64_int8", _truncate_step(64), _normalize_step(), _quantized_step("int8")),
        _pipeline_variant("truncate_dim_64_binary", _truncate_step(64), _normalize_step(), _quantized_step("binary")),
        *_default_dense_quantized_variants(),
        _pipeline_variant("truncate_dim_256", _truncate_step(256)),
        _pipeline_variant("truncate_dim_128", _truncate_step(128)),
        _pipeline_variant("truncate_dim_64", _truncate_step(64)),
        _pipeline_variant(
            "truncate_dim_256_int8_rescore",
            _truncate_step(256),
            _normalize_step(),
            _quantized_step("int8", rescore=True),
        ),
        _pipeline_variant(
            "truncate_dim_256_binary_rescore",
            _truncate_step(256),
            _normalize_step(),
            _quantized_step("binary", rescore=True),
        ),
        _pipeline_variant(
            "truncate_dim_128_int8_rescore",
            _truncate_step(128),
            _normalize_step(),
            _quantized_step("int8", rescore=True),
        ),
        _pipeline_variant(
            "truncate_dim_128_binary_rescore",
            _truncate_step(128),
            _normalize_step(),
            _quantized_step("binary", rescore=True),
        ),
        _pipeline_variant(
            "truncate_dim_64_int8_rescore",
            _truncate_step(64),
            _normalize_step(),
            _quantized_step("int8", rescore=True),
        ),
        _pipeline_variant(
            "truncate_dim_64_binary_rescore",
            _truncate_step(64),
            _normalize_step(),
            _quantized_step("binary", rescore=True),
        ),
    ]


def test_parse_args_accepts_normalize_quantized_cross_product() -> None:
    args = parse_args(
        [
            "evaluate",
            "dense",
            "--model",
            "hotchpotch/model",
            "--embedding-variant-grid",
            "normalize",
            "int8,binary",
        ]
    )

    assert args.embedding_variants == [
        _pipeline_variant("normalize_int8", _normalize_step(), _quantized_step("int8")),
        _pipeline_variant("normalize_binary", _normalize_step(), _quantized_step("binary")),
        *_default_dense_quantized_variants(),
    ]


def test_parse_args_does_not_mix_default_dataset_into_collection() -> None:
    args = parse_args(["evaluate", "dense", "--model", "hotchpotch/model", "--collection", "MNanoBEIR"])

    assert args.dataset == []
    assert args.collection == ["MNanoBEIR"]


def test_load_dataset_for_args_uses_candidate_subset_for_candidate_aware_models(monkeypatch) -> None:
    from hakari_bench.cli import _load_dataset_for_args

    calls: list[tuple[str, str | None]] = []

    def fake_load_ir_dataset(
        task: EvalTask,
        *,
        candidate_subset_name: str | None = None,
        revision: str | None = None,
    ) -> object:
        _ = task
        assert revision == "abc123"
        calls.append((current_model_type, candidate_subset_name))
        return object()

    monkeypatch.setattr("hakari_bench.cli.load_ir_dataset", fake_load_ir_dataset)
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

    for current_model_type in ["dense", "sparse", "late-interaction", "bm25", "reranker"]:
        _load_dataset_for_args(
            argparse.Namespace(model_type=current_model_type, candidate_subset_name="bm25", dataset_revision="abc123"),
            task,
        )

    assert calls == [
        ("dense", "bm25"),
        ("sparse", "bm25"),
        ("late-interaction", "bm25"),
        ("bm25", "bm25"),
        ("reranker", "bm25"),
    ]


def test_run_evaluate_returns_run_summary_payload(monkeypatch, tmp_path) -> None:
    from hakari_bench.cli import run_evaluate

    task = EvalTask(
        dataset=NanoDatasetSpec(
            name="Toy",
            dataset_id="toy/data",
            corpus_config="corpus",
            queries_config="queries",
            qrels_config="qrels",
        ),
        split_name="test",
        task_name="test",
    )
    args = parse_args(["evaluate", "dense", "--model", "hotchpotch/model", "--results-dir", str(tmp_path)])

    monkeypatch.setattr("hakari_bench.cli.DatasetRegistry.load_builtin", lambda: object())
    monkeypatch.setattr("hakari_bench.cli.resolve_eval_tasks", lambda **_: [task])
    monkeypatch.setattr("hakari_bench.cli.collect_runtime_environment", lambda: {"package_versions": {}})
    monkeypatch.setattr("hakari_bench.cli.load_model", lambda _: object())
    monkeypatch.setattr(
        "hakari_bench.cli.collect_model_metadata",
        lambda _model, parsed_args: {
            "method": parsed_args.model_type,
            "id": parsed_args.model_id,
            "source": parsed_args.model_source,
        },
    )

    def fake_run_or_load_task(**kwargs) -> TaskRunResult:
        output_path = tmp_path / "hotchpotch__model" / "toy__data" / "test.json"
        return TaskRunResult(
            task=kwargs["task"],
            cache_hit=False,
            output_path=output_path,
            payload={
                "model": {"id": "hotchpotch/model"},
                "target": {"dataset_revision": {"resolved": "toy-sha"}},
                "config": {"batch_size": 32, "primary_metric": "ndcg@10"},
                "evaluation": {"aggregate_metric_value": 1.0, "timing": {}},
            },
        )

    monkeypatch.setattr("hakari_bench.cli.run_or_load_task", fake_run_or_load_task)

    summary = run_evaluate(args)

    assert summary["totals"]["evaluated_count"] == 1
    assert summary["totals"]["aggregate_metric_mean"] == 1.0


def test_run_build_bm25_returns_candidate_summary(monkeypatch, tmp_path) -> None:
    from hakari_bench.bm25 import BM25BuildResult
    from hakari_bench.cli import run_build_bm25

    task = EvalTask(
        dataset=NanoDatasetSpec(
            name="Toy",
            dataset_id="toy/data",
            corpus_config="corpus",
            queries_config="queries",
            qrels_config="qrels",
        ),
        split_name="test",
        task_name="test",
    )
    args = parse_args(["build-candidates", "bm25", "--candidates-dir", str(tmp_path), "--bm25-top-k", "10"])

    monkeypatch.setattr("hakari_bench.cli.DatasetRegistry.load_builtin", lambda: object())
    monkeypatch.setattr("hakari_bench.cli.resolve_eval_tasks", lambda **_: [task])
    monkeypatch.setattr("hakari_bench.cli._load_dataset_for_args", lambda _args, _task: object())

    def fake_run_or_load_bm25_task(**kwargs) -> BM25BuildResult:
        return BM25BuildResult(
            task=kwargs["task"],
            cache_hit=False,
            output_path=tmp_path / "bm25s-okapi-auto" / "toy__data" / "test.json",
            payload={"generated_at_utc": "2026-05-04T00:00:00+00:00", "config": {"top_k": 10}},
        )

    monkeypatch.setattr("hakari_bench.cli.run_or_load_bm25_task", fake_run_or_load_bm25_task)

    payload = run_build_bm25(args)

    assert payload["candidates_dir"] == str(tmp_path)
    assert "output_dir" not in payload
    assert payload["config"]["bm25"]["top_k"] == 10
    assert "override" not in payload["config"]["bm25"]
