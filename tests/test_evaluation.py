from __future__ import annotations

import argparse
import json
from pathlib import Path

import numpy as np
import pytest
import torch
from scipy import sparse

import nano_ir_benchmark.evaluation as evaluation_module
from nano_ir_benchmark.datasets import EvalTask, NanoDatasetSpec
from nano_ir_benchmark.evaluation import (
    LoadedIrDataset,
    QuantizedEmbeddingMatrix,
    evaluate_dense_task,
    evaluate_reranker_task,
)
from nano_ir_benchmark.results import TaskRunResult, build_all_payload, result_path_for_task, run_or_load_task, safe_path_part


def _pipeline_variant(name: str, *steps: dict[str, object]) -> dict[str, object]:
    return {"name": name, "transform": {"type": "pipeline", "steps": list(steps)}}


def _truncate_step(dim: int) -> dict[str, object]:
    return {"type": "truncate", "algorithm": "dimension_slice", "parameters": {"dim": dim}}


def _sparse_max_active_dims_step(max_active_dims: int, *, target: str = "query_and_corpus") -> dict[str, object]:
    return {
        "type": "sparse_max_active_dims",
        "algorithm": "top_abs_values_per_row",
        "parameters": {"max_active_dims": max_active_dims, "target": target},
    }


def _quantize_step(
    precision: str,
    *,
    target: str = "corpus",
    calibration_sample_size: int | None = None,
) -> dict[str, object]:
    parameters: dict[str, object] = {
        "precision": precision,
        "target": target,
        "method": "corpus_only" if target == "corpus" else "query_and_corpus",
    }
    if precision in {"int8", "uint8"}:
        parameters["calibration"] = "corpus_sample" if calibration_sample_size is not None else "corpus"
    if calibration_sample_size is not None:
        parameters["calibration_sample_size"] = calibration_sample_size
        parameters["calibration_sample_seed"] = 13
    return {
        "type": "quantize",
        "algorithm": "sentence_transformers_embedding_quantization",
        "parameters": parameters,
    }


def _quantize_code_step(precision: str) -> dict[str, object]:
    parameters: dict[str, object] = {
        "precision": precision,
        "target": "query_and_corpus",
        "method": "query_and_corpus",
        "calibration": "corpus",
        "score_representation": "quantized_code_float32",
    }
    return {
        "type": "quantize",
        "algorithm": "sentence_transformers_embedding_quantization",
        "parameters": parameters,
    }


def _usearch_step(precision: str, *, rescore: bool = False) -> dict[str, object]:
    parameters: dict[str, object] = {
        "precision": precision,
        "target": "query_and_corpus",
        "method": "query_and_corpus",
        "score_representation": "usearch_exact_rescore" if rescore else "usearch_exact",
    }
    if precision in {"int8", "uint8"}:
        parameters["calibration"] = "corpus"
    return {
        "type": "quantize",
        "algorithm": "sentence_transformers_embedding_quantization",
        "parameters": parameters,
    }


def _toy_task() -> EvalTask:
    spec = NanoDatasetSpec(
        name="ToyData",
        dataset_id="toy/data",
        corpus_config="corpus",
        queries_config="queries",
        qrels_config="qrels",
        candidate_config="bm25",
    )
    return EvalTask(dataset=spec, split_name="test", task_name="test")


def _toy_dataset() -> LoadedIrDataset:
    return LoadedIrDataset(
        queries={"q1": "cat query", "q2": "dog query"},
        corpus={"d1": "cat doc", "d2": "dog doc", "d3": "other doc"},
        qrels={"q1": {"d1"}, "q2": {"d2"}},
        candidates={"q1": ["d3", "d1"], "q2": ["d2", "d1"]},
        evaluator_name="ToyData_test",
    )


def _toy_dataset_without_candidates() -> LoadedIrDataset:
    dataset = _toy_dataset()
    return LoadedIrDataset(
        queries=dataset.queries,
        corpus=dataset.corpus,
        qrels=dataset.qrels,
        candidates=None,
        evaluator_name=dataset.evaluator_name,
    )


class FakeDenseModel:
    similarity_fn_name = "dot"
    prompts = {"query": "query: ", "document": "document: "}
    default_prompt_name = None

    def __init__(self) -> None:
        self.query_calls: list[dict[str, object]] = []
        self.document_calls: list[dict[str, object]] = []

    def encode_query(self, sentences: list[str], **kwargs: object) -> np.ndarray:
        self.query_calls.append({"sentences": sentences, **kwargs})
        return np.array([[1.0, 0.0], [0.0, 1.0]])

    def encode_document(self, sentences: list[str], **kwargs: object) -> np.ndarray:
        self.document_calls.append({"sentences": sentences, **kwargs})
        return np.array([[1.0, 0.0], [0.0, 1.0], [-1.0, 0.0]])


class FakeScaleSensitiveDenseModel:
    similarity_fn_name = "dot"

    def encode_query(self, sentences: list[str], **kwargs: object) -> np.ndarray:
        return np.array([[1.0, 0.0]], dtype=np.float32)

    def encode_document(self, sentences: list[str], **kwargs: object) -> np.ndarray:
        return np.array([[1.0, 0.0], [10.0, 1.0]], dtype=np.float32)


def _scale_sensitive_dataset() -> LoadedIrDataset:
    return LoadedIrDataset(
        queries={"q1": "scale query"},
        corpus={"d1": "relevant same direction", "d2": "larger norm distractor"},
        qrels={"q1": {"d1"}},
        candidates=None,
        evaluator_name="ScaleToy_test",
    )


class FakeTaskDenseModel:
    similarity_fn_name = "dot"

    def __init__(self) -> None:
        self.calls: list[dict[str, object]] = []

    def encode_query(self, sentences: list[str], **kwargs: object) -> np.ndarray:
        raise AssertionError("encode_query should not be used when an explicit task is configured")

    def encode_document(self, sentences: list[str], **kwargs: object) -> np.ndarray:
        raise AssertionError("encode_document should not be used when an explicit task is configured")

    def encode(self, sentences: list[str], **kwargs: object) -> np.ndarray:
        self.calls.append({"sentences": sentences, **kwargs})
        if len(sentences) == 2:
            return np.array([[1.0, 0.0], [0.0, 1.0]])
        return np.array([[1.0, 0.0], [0.0, 1.0], [-1.0, 0.0]])


class FakeSparseModel:
    similarity_fn_name = "dot"

    def encode_query(self, sentences: list[str], **kwargs: object) -> sparse.csr_matrix:
        return sparse.csr_matrix([[1.0, 0.0, 0.0, 2.0], [0.0, 3.0, 0.0, 0.0]])

    def encode_document(self, sentences: list[str], **kwargs: object) -> sparse.csr_matrix:
        return sparse.csr_matrix(
            [[1.0, 0.0, 0.0, 1.0], [0.0, 2.0, 0.0, 0.0], [0.0, 0.0, 4.0, 0.0]]
        )


class FakeSentenceTransformersSparseModel:
    similarity_fn_name = "dot"

    def __init__(self) -> None:
        self.query_calls: list[dict[str, object]] = []
        self.document_calls: list[dict[str, object]] = []

    def encode_query(
        self,
        sentences: list[str],
        *,
        batch_size: int,
        show_progress_bar: bool,
        convert_to_tensor: bool = True,
        convert_to_sparse_tensor: bool = True,
        save_to_cpu: bool = False,
        max_active_dims: int | None = None,
    ) -> torch.Tensor:
        self.query_calls.append(
            {
                "sentences": sentences,
                "batch_size": batch_size,
                "show_progress_bar": show_progress_bar,
                "convert_to_tensor": convert_to_tensor,
                "convert_to_sparse_tensor": convert_to_sparse_tensor,
                "save_to_cpu": save_to_cpu,
                "max_active_dims": max_active_dims,
            }
        )
        return torch.tensor([[1.0, 0.0, 0.0, 2.0], [0.0, 3.0, 0.0, 0.0]]).to_sparse()

    def encode_document(
        self,
        sentences: list[str],
        *,
        batch_size: int,
        show_progress_bar: bool,
        convert_to_tensor: bool = True,
        convert_to_sparse_tensor: bool = True,
        save_to_cpu: bool = False,
        max_active_dims: int | None = None,
    ) -> torch.Tensor:
        self.document_calls.append(
            {
                "sentences": sentences,
                "batch_size": batch_size,
                "show_progress_bar": show_progress_bar,
                "convert_to_tensor": convert_to_tensor,
                "convert_to_sparse_tensor": convert_to_sparse_tensor,
                "save_to_cpu": save_to_cpu,
                "max_active_dims": max_active_dims,
            }
        )
        return torch.tensor([[1.0, 0.0, 0.0, 1.0], [0.0, 2.0, 0.0, 0.0], [0.0, 0.0, 4.0, 0.0]]).to_sparse()


class FakeReranker:
    def predict(self, pairs: list[tuple[str, str]], **kwargs: object) -> list[float]:
        return [1.0 if pair in {("cat query", "cat doc"), ("dog query", "dog doc")} else 0.0 for pair in pairs]


def test_evaluate_dense_task_uses_default_prompt_config_when_not_overridden() -> None:
    model = FakeDenseModel()

    result = evaluate_dense_task(
        model=model,
        dataset=_toy_dataset(),
        batch_size=8,
        show_progress=False,
        query_prompt=None,
        corpus_prompt=None,
        query_prompt_name=None,
        corpus_prompt_name=None,
        truncate_dim=None,
    )

    assert result.metrics["ToyData_test_dot_ndcg@10"] == pytest.approx(1.0)
    assert model.query_calls[0]["sentences"] == ["cat query", "dog query"]
    assert "prompt" not in model.query_calls[0]
    assert "prompt_name" not in model.query_calls[0]


def test_evaluate_dense_task_explicit_prompts_take_precedence() -> None:
    model = FakeDenseModel()

    evaluate_dense_task(
        model=model,
        dataset=_toy_dataset(),
        batch_size=4,
        show_progress=False,
        query_prompt="Q: ",
        corpus_prompt="D: ",
        query_prompt_name="query",
        corpus_prompt_name="document",
        truncate_dim=None,
    )

    assert model.query_calls[0]["prompt"] == "Q: "
    assert "prompt_name" not in model.query_calls[0]
    assert model.document_calls[0]["prompt"] == "D: "
    assert "prompt_name" not in model.document_calls[0]


def test_evaluate_dense_task_explicit_tasks_use_generic_encode() -> None:
    model = FakeTaskDenseModel()

    result = evaluate_dense_task(
        model=model,
        dataset=_toy_dataset(),
        batch_size=4,
        show_progress=False,
        query_prompt=None,
        corpus_prompt=None,
        query_prompt_name=None,
        corpus_prompt_name=None,
        query_task="retrieval",
        corpus_task="retrieval",
        truncate_dim=None,
    )

    assert result.metrics["ToyData_test_dot_ndcg@10"] == pytest.approx(1.0)
    assert model.calls[0]["task"] == "retrieval"
    assert model.calls[1]["task"] == "retrieval"


def test_evaluate_dense_task_scores_embedding_variants_without_extra_encoding() -> None:
    model = FakeDenseModel()

    result = evaluate_dense_task(
        model=model,
        dataset=_toy_dataset(),
        batch_size=4,
        show_progress=False,
        query_prompt=None,
        corpus_prompt=None,
        query_prompt_name=None,
        corpus_prompt_name=None,
        truncate_dim=None,
        embedding_variants=[_pipeline_variant("truncate_dim_1", _truncate_step(1))],
    )

    assert len(model.query_calls) == 1
    assert len(model.document_calls) == 1
    assert "truncate_dim" not in model.query_calls[0]
    assert result.metrics["ToyData_test_dot_ndcg@10"] == pytest.approx(1.0)
    assert result.embedding_evaluations[0]["name"] == "base"
    assert result.embedding_evaluations[0]["embedding_dimensions"] == {"dim": 2}
    assert result.embedding_evaluations[0]["embedding_metadata"] == {
        "representation_type": "dense",
        "dimension_format": "single_vector",
        "dimensions": {"dim": 2},
        "query": {"shape": [2, 2]},
        "corpus": {"shape": [3, 2]},
    }
    assert result.embedding_evaluations[0]["best_distance"] == "dot"
    assert result.embedding_evaluations[0]["best_score"] == pytest.approx(1.0)
    assert [item["distance"] for item in result.embedding_evaluations[0]["distance_evaluations"]] == [
        "dot",
        "cosine",
    ]
    assert result.embedding_evaluations[1]["name"] == "truncate_dim_1"
    assert result.embedding_evaluations[1]["transform"]["steps"][0]["parameters"] == {"dim": 1}
    assert result.embedding_evaluations[1]["embedding_dimensions"] == {"dim": 1}
    assert result.embedding_evaluations[1]["embedding_metadata"]["dimensions"] == {"dim": 1}
    assert result.embedding_evaluations[1]["aggregate_metric_value"] < 1.0
    assert "ToyData_test_dot_truncate_dim_1_ndcg@10" in result.embedding_evaluations[1]["metrics"]


def test_evaluate_dense_task_records_query_and_docs_conversion_speed() -> None:
    result = evaluate_dense_task(
        model=FakeDenseModel(),
        dataset=_toy_dataset(),
        batch_size=4,
        show_progress=False,
        query_prompt=None,
        corpus_prompt=None,
        query_prompt_name=None,
        corpus_prompt_name=None,
        truncate_dim=None,
    )

    query_conversion = result.embedding_conversion["query"]
    assert query_conversion["text_count"] == 2
    assert query_conversion["batch_size"] == 4
    assert query_conversion["seconds"] == pytest.approx(result.timing["query_embedding_seconds"])
    assert query_conversion["texts_per_second"] == pytest.approx(
        query_conversion["text_count"] / query_conversion["seconds"]
    )

    docs_conversion = result.embedding_conversion["docs"]
    assert docs_conversion["text_count"] == 3
    assert docs_conversion["batch_size"] == 4
    assert docs_conversion["seconds"] == pytest.approx(result.timing["corpus_embedding_seconds"])
    assert docs_conversion["texts_per_second"] == pytest.approx(
        docs_conversion["text_count"] / docs_conversion["seconds"]
    )


def test_evaluate_dense_task_records_cosine_and_dot_and_adopts_best_distance() -> None:
    result = evaluate_dense_task(
        model=FakeScaleSensitiveDenseModel(),
        dataset=_scale_sensitive_dataset(),
        batch_size=4,
        show_progress=False,
        query_prompt=None,
        corpus_prompt=None,
        query_prompt_name=None,
        corpus_prompt_name=None,
        truncate_dim=None,
    )

    base = result.embedding_evaluations[0]
    assert [item["distance"] for item in base["distance_evaluations"]] == ["dot", "cosine"]
    distance_values = {item["distance"]: item["aggregate_metric_value"] for item in base["distance_evaluations"]}
    assert distance_values["dot"] < distance_values["cosine"]
    assert base["best_distance"] == "cosine"
    assert base["best_score_name"] == "cosine"
    assert base["best_score"] == pytest.approx(distance_values["cosine"])
    assert base["aggregate_metric_value"] == pytest.approx(distance_values["cosine"])
    assert result.metrics == base["metrics"]
    assert "ScaleToy_test_cosine_ndcg@10" in result.metrics


def test_evaluate_dense_task_quantizes_embedding_variants_after_encoding() -> None:
    model = FakeDenseModel()

    result = evaluate_dense_task(
        model=model,
        dataset=_toy_dataset(),
        batch_size=4,
        show_progress=False,
        query_prompt=None,
        corpus_prompt=None,
        query_prompt_name=None,
        corpus_prompt_name=None,
        truncate_dim=None,
        embedding_variants=[
            _pipeline_variant("quantize_int8_docs", _quantize_step("int8")),
            _pipeline_variant("quantize_ubinary_docs", _quantize_step("ubinary")),
        ],
    )

    assert len(model.query_calls) == 1
    assert len(model.document_calls) == 1
    assert "precision" not in model.query_calls[0]
    assert "precision" not in model.document_calls[0]

    assert [item["name"] for item in result.embedding_evaluations] == [
        "base",
        "quantize_int8_docs",
        "quantize_ubinary_docs",
    ]
    int8_eval = result.embedding_evaluations[1]
    assert int8_eval["aggregate_metric_value"] == pytest.approx(1.0)
    assert int8_eval["best_score"] == pytest.approx(1.0)
    assert int8_eval["best_distance"] == "dot"
    assert [item["distance"] for item in int8_eval["distance_evaluations"]] == ["dot", "cosine"]
    assert int8_eval["embedding_dimensions"] == {"dim": 2}
    assert int8_eval["embedding_metadata"]["dimension_format"] == "single_vector"
    assert "value_dtype" not in int8_eval["embedding_metadata"]["query"]
    assert "quantization" not in int8_eval["embedding_metadata"]["query"]
    assert int8_eval["embedding_metadata"]["corpus"]["quantization"] == {
        "precision": "int8",
        "algorithm": "sentence_transformers_embedding_quantization",
        "ranges_source": "corpus",
        "original_dim": 2,
        "stored_dim": 2,
        "score_representation": "dequantized_float32",
        "method": "corpus_only",
        "side": "corpus",
        "rounding": "truncate",
    }

    ubinary_eval = result.embedding_evaluations[2]
    assert ubinary_eval["aggregate_metric_value"] == pytest.approx(1.0)
    assert [item["distance"] for item in ubinary_eval["distance_evaluations"]] == ["dot", "cosine"]
    assert ubinary_eval["embedding_dimensions"] == {"dim": 2, "query_stored_dim": 2, "corpus_stored_dim": 1}
    assert ubinary_eval["embedding_metadata"]["dimension_format"] == "mixed_single_and_packed_binary_vector"
    assert ubinary_eval["embedding_metadata"]["query"]["shape"] == [2, 2]
    assert "value_dtype" not in ubinary_eval["embedding_metadata"]["query"]
    assert "quantization" not in ubinary_eval["embedding_metadata"]["query"]
    assert ubinary_eval["embedding_metadata"]["corpus"]["shape"] == [3, 1]
    assert ubinary_eval["embedding_metadata"]["corpus"]["value_dtype"] == "uint8"
    assert ubinary_eval["embedding_metadata"]["corpus"]["quantization"] == {
        "precision": "ubinary",
        "algorithm": "sentence_transformers_embedding_quantization",
        "original_dim": 2,
        "stored_dim": 1,
        "score_representation": "unpacked_sign_float32",
        "method": "corpus_only",
        "side": "corpus",
    }
    assert "ToyData_test_dot_quantize_ubinary_docs_ndcg@10" in ubinary_eval["metrics"]


def test_quantize_int8_defaults_to_corpus_only_and_keeps_query_float() -> None:
    # Query embeddings are evaluation inputs and are cheap to keep at full
    # precision. The default quantization path should therefore quantize only
    # corpus/document vectors and record that method in JSON metadata.
    query_embeddings = np.array([[10.0, -10.0]], dtype=np.float32)
    corpus_embeddings = np.array([[1.0, -1.0], [-1.0, 1.0]], dtype=np.float32)

    query_result, corpus_quantized = evaluation_module._quantize_embedding_pair(
        query_embeddings=query_embeddings,
        corpus_embeddings=corpus_embeddings,
        precision="int8",
        algorithm="sentence_transformers_embedding_quantization",
    )

    assert query_result is query_embeddings
    assert corpus_quantized.ranges_source == "corpus"
    assert corpus_quantized.method == "corpus_only"
    assert corpus_quantized.side == "corpus"
    assert corpus_quantized.values.tolist() == [[126, -128], [-128, 126]]
    np.testing.assert_allclose(
        evaluation_module._to_numpy_float32(query_result),
        query_embeddings,
        atol=1e-6,
    )
    np.testing.assert_allclose(
        evaluation_module._to_numpy_float32(corpus_quantized),
        corpus_embeddings,
        atol=0.01,
    )


def test_quantize_int8_uses_sentence_transformers_truncating_bucket_cast() -> None:
    query_embeddings = np.array([[0.492]], dtype=np.float32)
    corpus_embeddings = np.array([[0.0], [1.0], [0.492]], dtype=np.float32)

    _query_result, corpus_quantized = evaluation_module._quantize_embedding_pair(
        query_embeddings=query_embeddings,
        corpus_embeddings=corpus_embeddings,
        precision="int8",
        algorithm="sentence_transformers_embedding_quantization",
    )

    # SentenceTransformers quantize_embeddings casts bucket values directly to
    # int8 rather than rounding to nearest. Keep parity so benchmark variants
    # do not look better than the library's documented scalar quantization.
    assert corpus_quantized.values[:, 0].tolist() == [-128, 126, -2]
    assert corpus_quantized.rounding == "truncate"


def test_quantize_int8_can_calibrate_from_corpus_sample() -> None:
    query_embeddings = np.array([[10.0]], dtype=np.float32)
    corpus_embeddings = np.array([[0.0], [1.0], [10.0]], dtype=np.float32)

    _query_result, corpus_quantized = evaluation_module._quantize_embedding_pair(
        query_embeddings=query_embeddings,
        corpus_embeddings=corpus_embeddings,
        precision="int8",
        algorithm="sentence_transformers_embedding_quantization",
        calibration_sample_size=2,
        calibration_sample_seed=1,
    )

    np.testing.assert_allclose(corpus_quantized.ranges, np.array([[0.0], [1.0]], dtype=np.float32))
    assert corpus_quantized.ranges_source == "corpus_sample"
    assert corpus_quantized.calibration_sample_size == 2
    assert corpus_quantized.calibration_sample_seed == 1
    assert corpus_quantized.values[:, 0].tolist() == [-128, 126, 127]


def test_quantize_int8_query_and_corpus_mode_clips_query_outliers() -> None:
    # Explicit query_and_corpus mode keeps the old symmetric quantization
    # behavior. Query outliers still must be clipped against corpus-derived
    # ranges rather than wrapped by numpy int8 casts.
    query_embeddings = np.array([[10.0, -10.0]], dtype=np.float32)
    corpus_embeddings = np.array([[1.0, -1.0], [-1.0, 1.0]], dtype=np.float32)

    query_quantized, corpus_quantized = evaluation_module._quantize_embedding_pair(
        query_embeddings=query_embeddings,
        corpus_embeddings=corpus_embeddings,
        precision="int8",
        algorithm="sentence_transformers_embedding_quantization",
        target="query_and_corpus",
    )

    assert query_quantized.ranges_source == "corpus"
    assert corpus_quantized.ranges_source == "corpus"
    assert query_quantized.method == "query_and_corpus"
    assert query_quantized.side == "query"
    assert corpus_quantized.method == "query_and_corpus"
    assert corpus_quantized.side == "corpus"
    assert query_quantized.values.tolist() == [[127, -128]]
    assert corpus_quantized.values.tolist() == [[126, -128], [-128, 126]]
    np.testing.assert_allclose(
        evaluation_module._to_numpy_float32(query_quantized),
        np.array([[1.0, -1.0]], dtype=np.float32),
        atol=1e-6,
    )


def test_quantized_code_scoring_ranks_without_dequantizing_scalar_embeddings() -> None:
    ranges = np.array([[0.0, 0.0], [1.0, 1.0]], dtype=np.float32)
    query_quantized = QuantizedEmbeddingMatrix(
        values=np.array([[-102, -102]], dtype=np.int8),
        precision="int8",
        original_dim=2,
        algorithm="sentence_transformers_embedding_quantization",
        method="query_and_corpus",
        side="query",
        ranges_source="corpus",
        ranges=ranges,
        rounding="truncate",
        score_representation="quantized_code_float32",
    )
    corpus_quantized = QuantizedEmbeddingMatrix(
        values=np.array([[-102, -102], [-128, -128]], dtype=np.int8),
        precision="int8",
        original_dim=2,
        algorithm="sentence_transformers_embedding_quantization",
        method="query_and_corpus",
        side="corpus",
        ranges_source="corpus",
        ranges=ranges,
        rounding="truncate",
        score_representation="quantized_code_float32",
    )

    rankings = evaluation_module._rank_by_similarity(
        query_ids=["q1"],
        corpus_ids=["d1", "d2"],
        query_embeddings=query_quantized,
        corpus_embeddings=corpus_quantized,
        score_name="dot",
    )

    # In dequantized space d1 is closer to q1, but raw int8 code dot product
    # promotes the all-low bucket d2. This locks the diagnostic code-score path
    # to the stored quantized values rather than the float reconstruction.
    assert rankings["q1"] == ["d2", "d1"]


def test_usearch_int8_rescore_reranks_candidates_with_source_float_embeddings() -> None:
    ranges = np.array([[0.0, 0.0], [1.0, 1.0]], dtype=np.float32)
    query_quantized = QuantizedEmbeddingMatrix(
        values=np.array([[-102, -102]], dtype=np.int8),
        precision="int8",
        original_dim=2,
        algorithm="sentence_transformers_embedding_quantization",
        method="query_and_corpus",
        side="query",
        ranges_source="corpus",
        ranges=ranges,
        rounding="truncate",
        score_representation="usearch_exact",
    )
    corpus_quantized = QuantizedEmbeddingMatrix(
        values=np.array([[-102, -102], [-128, -128]], dtype=np.int8),
        precision="int8",
        original_dim=2,
        algorithm="sentence_transformers_embedding_quantization",
        method="query_and_corpus",
        side="corpus",
        ranges_source="corpus",
        ranges=ranges,
        rounding="truncate",
        score_representation="usearch_exact",
    )
    no_rescore_rankings = evaluation_module._rank_by_similarity(
        query_ids=["q1"],
        corpus_ids=["d1", "d2"],
        query_embeddings=query_quantized,
        corpus_embeddings=corpus_quantized,
        score_name="dot",
    )

    query_rescore = QuantizedEmbeddingMatrix(
        values=query_quantized.values,
        precision="int8",
        original_dim=2,
        algorithm="sentence_transformers_embedding_quantization",
        method="query_and_corpus",
        side="query",
        ranges_source="corpus",
        ranges=ranges,
        rounding="truncate",
        score_representation="usearch_exact_rescore",
        source_values=np.array([[0.1, 0.1]], dtype=np.float32),
    )
    corpus_rescore = QuantizedEmbeddingMatrix(
        values=corpus_quantized.values,
        precision="int8",
        original_dim=2,
        algorithm="sentence_transformers_embedding_quantization",
        method="query_and_corpus",
        side="corpus",
        ranges_source="corpus",
        ranges=ranges,
        rounding="truncate",
        score_representation="usearch_exact_rescore",
        source_values=np.array([[0.1, 0.1], [0.0, 0.0]], dtype=np.float32),
    )
    rescore_rankings = evaluation_module._rank_by_similarity(
        query_ids=["q1"],
        corpus_ids=["d1", "d2"],
        query_embeddings=query_rescore,
        corpus_embeddings=corpus_rescore,
        score_name="dot",
    )

    assert no_rescore_rankings["q1"] == ["d2", "d1"]
    assert rescore_rankings["q1"] == ["d1", "d2"]


def test_usearch_binary_ranks_by_hamming_distance() -> None:
    query_embeddings = np.array([[1.0, -1.0]], dtype=np.float32)
    corpus_embeddings = np.array([[1.0, -1.0], [-1.0, 1.0]], dtype=np.float32)

    query_quantized, corpus_quantized = evaluation_module._quantize_embedding_pair(
        query_embeddings=query_embeddings,
        corpus_embeddings=corpus_embeddings,
        precision="binary",
        target="query_and_corpus",
        algorithm="sentence_transformers_embedding_quantization",
        score_representation="usearch_exact",
    )
    rankings = evaluation_module._rank_by_similarity(
        query_ids=["q1"],
        corpus_ids=["d1", "d2"],
        query_embeddings=query_quantized,
        corpus_embeddings=corpus_quantized,
        score_name="dot",
    )

    assert rankings["q1"] == ["d1", "d2"]


def test_evaluate_dense_task_uses_single_pipeline_path_for_all_embedding_variants(monkeypatch) -> None:
    model = FakeDenseModel()
    pipeline_calls: list[list[str]] = []
    original_apply_pipeline = evaluation_module._apply_embedding_pipeline_pair

    def apply_pipeline_spy(*, query_embeddings, corpus_embeddings, steps):
        pipeline_calls.append([str(step["type"]) for step in steps])
        return original_apply_pipeline(
            query_embeddings=query_embeddings,
            corpus_embeddings=corpus_embeddings,
            steps=steps,
        )

    monkeypatch.setattr(evaluation_module, "_apply_embedding_pipeline_pair", apply_pipeline_spy)

    evaluation_module.evaluate_dense_task(
        model=model,
        dataset=_toy_dataset(),
        batch_size=4,
        show_progress=False,
        query_prompt=None,
        corpus_prompt=None,
        query_prompt_name=None,
        corpus_prompt_name=None,
        truncate_dim=None,
        embedding_variants=[
            _pipeline_variant("truncate_dim_1", _truncate_step(1)),
            _pipeline_variant("quantize_int8_docs", _quantize_step("int8")),
            _pipeline_variant("truncate_dim_1_quantize_ubinary_docs", _truncate_step(1), _quantize_step("ubinary")),
        ],
    )

    # This guards the intended low-compute shape: every derived evaluation,
    # including cross variants, must go through the same post-encode pipeline
    # path instead of adding transform-specific branches or extra model encodes.
    assert len(model.query_calls) == 1
    assert len(model.document_calls) == 1
    assert pipeline_calls == [["truncate"], ["quantize"], ["truncate", "quantize"]]


def test_evaluate_dense_task_records_sparse_embedding_metadata() -> None:
    result = evaluate_dense_task(
        model=FakeSparseModel(),
        dataset=_toy_dataset(),
        batch_size=4,
        show_progress=False,
        query_prompt=None,
        corpus_prompt=None,
        query_prompt_name=None,
        corpus_prompt_name=None,
        truncate_dim=None,
    )

    base = result.embedding_evaluations[0]
    assert base["embedding_dimensions"] == {"dim": 4}
    assert base["embedding_metadata"]["representation_type"] == "sparse"
    assert base["embedding_metadata"]["dimension_format"] == "sparse_vector"
    assert base["embedding_metadata"]["dimensions"] == {"dim": 4}
    assert base["embedding_metadata"]["query"]["shape"] == [2, 4]
    assert base["embedding_metadata"]["query"]["nnz_total"] == 3
    assert base["embedding_metadata"]["query"]["nnz_mean"] == pytest.approx(1.5)
    assert base["embedding_metadata"]["query"]["nnz_median"] == pytest.approx(1.5)
    assert base["embedding_metadata"]["query"]["density"] == pytest.approx(3 / 8)
    assert base["embedding_metadata"]["corpus"]["shape"] == [3, 4]
    assert base["embedding_metadata"]["corpus"]["nnz_total"] == 4
    assert base["embedding_metadata"]["corpus"]["nnz_median"] == pytest.approx(1.0)
    assert base["embedding_metadata"]["corpus"]["nnz_max"] == 2


def test_evaluate_dense_task_requests_sparse_tensor_output_for_sparse_encoder() -> None:
    model = FakeSentenceTransformersSparseModel()

    result = evaluate_dense_task(
        model=model,
        dataset=_toy_dataset(),
        batch_size=4,
        show_progress=False,
        query_prompt=None,
        corpus_prompt=None,
        query_prompt_name=None,
        corpus_prompt_name=None,
        truncate_dim=None,
    )

    assert result.metrics["ToyData_test_dot_ndcg@10"] == pytest.approx(1.0)
    assert model.query_calls[0]["convert_to_tensor"] is True
    assert model.query_calls[0]["convert_to_sparse_tensor"] is True
    assert model.query_calls[0]["save_to_cpu"] is True
    assert model.document_calls[0]["convert_to_tensor"] is True
    assert model.document_calls[0]["convert_to_sparse_tensor"] is True
    assert model.document_calls[0]["save_to_cpu"] is True
    base = result.embedding_evaluations[0]
    assert base["embedding_metadata"]["representation_type"] == "sparse"
    assert base["embedding_metadata"]["dimension_format"] == "sparse_vector"
    assert base["embedding_metadata"]["query"]["nnz_total"] == 3
    assert base["embedding_metadata"]["query"]["nnz_median"] == pytest.approx(1.5)
    assert base["embedding_metadata"]["corpus"]["nnz_total"] == 4
    assert base["embedding_metadata"]["corpus"]["nnz_median"] == pytest.approx(1.0)


def test_evaluate_dense_task_scores_sparse_max_active_dims_variants_without_extra_encoding() -> None:
    model = FakeSentenceTransformersSparseModel()

    result = evaluate_dense_task(
        model=model,
        dataset=_toy_dataset(),
        batch_size=4,
        show_progress=False,
        query_prompt=None,
        corpus_prompt=None,
        query_prompt_name=None,
        corpus_prompt_name=None,
        truncate_dim=None,
        embedding_variants=[
            _pipeline_variant("sparse_max_active_dims_1", _sparse_max_active_dims_step(1)),
        ],
    )

    assert len(model.query_calls) == 1
    assert len(model.document_calls) == 1
    variant = result.embedding_evaluations[1]
    assert variant["name"] == "sparse_max_active_dims_1"
    assert variant["embedding_dimensions"] == {"dim": 4}
    assert variant["embedding_metadata"]["representation_type"] == "sparse"
    assert variant["embedding_metadata"]["query"]["nnz_total"] == 2
    assert variant["embedding_metadata"]["query"]["nnz_max"] == 1
    assert variant["embedding_metadata"]["corpus"]["nnz_total"] == 3
    assert variant["embedding_metadata"]["corpus"]["nnz_max"] == 1
    assert "ToyData_test_dot_sparse_max_active_dims_1_ndcg@10" in variant["metrics"]


def test_evaluate_dense_task_scores_query_and_docs_sparse_max_active_dims_variants() -> None:
    model = FakeSentenceTransformersSparseModel()

    result = evaluate_dense_task(
        model=model,
        dataset=_toy_dataset(),
        batch_size=4,
        show_progress=False,
        query_prompt=None,
        corpus_prompt=None,
        query_prompt_name=None,
        corpus_prompt_name=None,
        truncate_dim=None,
        embedding_variants=[
            _pipeline_variant(
                "sparse_query_max_active_dims_1_sparse_docs_max_active_dims_1",
                _sparse_max_active_dims_step(1, target="query"),
                _sparse_max_active_dims_step(1, target="corpus"),
            ),
        ],
    )

    assert len(model.query_calls) == 1
    assert len(model.document_calls) == 1
    variant = result.embedding_evaluations[1]
    assert variant["name"] == "sparse_query_max_active_dims_1_sparse_docs_max_active_dims_1"
    assert variant["embedding_metadata"]["query"]["nnz_total"] == 2
    assert variant["embedding_metadata"]["query"]["nnz_max"] == 1
    assert variant["embedding_metadata"]["corpus"]["nnz_total"] == 3
    assert variant["embedding_metadata"]["corpus"]["nnz_max"] == 1


def test_evaluate_dense_task_quantizes_sparse_embedding_variants_after_encoding() -> None:
    model = FakeSentenceTransformersSparseModel()

    result = evaluate_dense_task(
        model=model,
        dataset=_toy_dataset(),
        batch_size=4,
        show_progress=False,
        query_prompt=None,
        corpus_prompt=None,
        query_prompt_name=None,
        corpus_prompt_name=None,
        truncate_dim=None,
        embedding_variants=[
            _pipeline_variant("quantize_int8_docs", _quantize_step("int8")),
            _pipeline_variant("quantize_ubinary_docs", _quantize_step("ubinary")),
        ],
    )

    assert len(model.query_calls) == 1
    assert len(model.document_calls) == 1
    assert [item["name"] for item in result.embedding_evaluations] == [
        "base",
        "quantize_int8_docs",
        "quantize_ubinary_docs",
    ]

    int8_eval = result.embedding_evaluations[1]
    assert int8_eval["embedding_metadata"]["representation_type"] == "sparse"
    assert int8_eval["embedding_metadata"]["query"]["nnz_total"] == 3
    assert int8_eval["embedding_metadata"]["corpus"]["nnz_total"] == 4
    assert int8_eval["embedding_metadata"]["corpus"]["value_dtype"] == "int8"
    assert int8_eval["embedding_metadata"]["corpus"]["quantization"]["precision"] == "int8"
    assert int8_eval["embedding_metadata"]["corpus"]["quantization"]["ranges_source"] == "corpus"
    assert int8_eval["embedding_metadata"]["corpus"]["quantization"]["score_representation"] == (
        "dequantized_sparse_float32"
    )
    assert "ToyData_test_dot_quantize_int8_docs_ndcg@10" in int8_eval["metrics"]

    ubinary_eval = result.embedding_evaluations[2]
    assert ubinary_eval["embedding_metadata"]["corpus"]["value_dtype"] == "uint8"
    assert ubinary_eval["embedding_metadata"]["corpus"]["quantization"]["precision"] == "ubinary"
    assert ubinary_eval["embedding_metadata"]["corpus"]["quantization"]["score_representation"] == (
        "sparse_nonzero_indicator_float32"
    )
    assert "ToyData_test_dot_quantize_ubinary_docs_ndcg@10" in ubinary_eval["metrics"]


def test_evaluate_dense_task_passes_sparse_max_active_dims_to_sparse_encoder() -> None:
    model = FakeSentenceTransformersSparseModel()

    evaluate_dense_task(
        model=model,
        dataset=_toy_dataset(),
        batch_size=4,
        show_progress=False,
        query_prompt=None,
        corpus_prompt=None,
        query_prompt_name=None,
        corpus_prompt_name=None,
        truncate_dim=None,
        sparse_max_active_dims=64,
    )

    assert model.query_calls[0]["max_active_dims"] == 64
    assert model.document_calls[0]["max_active_dims"] == 64


def test_evaluate_reranker_task_uses_candidate_top_n() -> None:
    result = evaluate_reranker_task(
        model=FakeReranker(),
        dataset=_toy_dataset(),
        batch_size=2,
        show_progress=False,
        rerank_top_n=1,
    )

    assert result.metrics["ToyData_test_reranker_ndcg@10"] == pytest.approx(0.5)


def test_result_path_layout() -> None:
    path = result_path_for_task(
        output_dir=Path("output/results"),
        model_name_or_path="hotchpotch/bekko-model",
        task=_toy_task(),
    )

    assert path == Path("output/results/hotchpotch__bekko-model/toy__data/test.json")
    assert safe_path_part("/tmp/local model") == "tmp__local_model"


def test_run_or_load_task_skips_existing_json(tmp_path: Path) -> None:
    task = _toy_task()
    args = argparse.Namespace(
        output_dir=str(tmp_path),
        model="hotchpotch/model",
        model_type="dense",
        batch_size=2,
        show_progress=False,
        query_prompt=None,
        corpus_prompt=None,
        query_prompt_name=None,
        corpus_prompt_name=None,
        truncate_dim=None,
        candidate_subset_name="bm25",
        rerank_top_n=100,
        aggregate_metric="ndcg@10",
        override=False,
    )
    output_path = result_path_for_task(output_dir=tmp_path, model_name_or_path=args.model, task=task)
    output_path.parent.mkdir(parents=True)
    output_path.write_text(json.dumps({"metrics": {"cached": 1.0}}), encoding="utf-8")

    result = run_or_load_task(
        task=task,
        model=FakeDenseModel(),
        args=args,
        environment={"package_versions": {}},
        model_metadata={"name_or_path": "hotchpotch/model"},
        dataset_loader=lambda _: _toy_dataset(),
    )

    assert result.cache_hit is True
    assert result.payload["metrics"] == {"cached": 1.0}


def test_run_or_load_task_records_evaluation_timestamps_and_durations(tmp_path: Path) -> None:
    task = _toy_task()
    args = argparse.Namespace(
        output_dir=str(tmp_path),
        model="hotchpotch/model",
        model_type="dense",
        batch_size=2,
        show_progress=False,
        query_prompt=None,
        corpus_prompt=None,
        query_prompt_name=None,
        corpus_prompt_name=None,
        truncate_dim=None,
        candidate_subset_name="bm25",
        rerank_top_n=100,
        aggregate_metric="ndcg@10",
        override=False,
    )

    result = run_or_load_task(
        task=task,
        model=FakeDenseModel(),
        args=args,
        environment={"package_versions": {}},
        model_metadata={"name_or_path": "hotchpotch/model"},
        dataset_loader=lambda _: _toy_dataset(),
    )

    evaluation = result.payload["evaluation"]
    assert evaluation["dataset_load_started_at_utc"].endswith("+00:00")
    assert evaluation["dataset_load_finished_at_utc"].endswith("+00:00")
    assert evaluation["started_at_utc"].endswith("+00:00")
    assert evaluation["finished_at_utc"].endswith("+00:00")
    assert evaluation["evaluated_at_utc"] == evaluation["finished_at_utc"]
    assert evaluation["dataset_load_seconds"] >= 0.0
    assert evaluation["duration_seconds_excluding_dataset_load"] >= 0.0
    assert evaluation["duration_seconds_including_dataset_load"] >= evaluation["duration_seconds_excluding_dataset_load"]
    assert evaluation["embedding_conversion"]["query"]["text_count"] == 2
    assert evaluation["embedding_conversion"]["query"]["batch_size"] == 2
    assert evaluation["embedding_conversion"]["docs"]["text_count"] == 3
    assert evaluation["embedding_conversion"]["docs"]["batch_size"] == 2


def test_run_or_load_task_records_dataset_revision(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    task = _toy_task()
    args = argparse.Namespace(
        output_dir=str(tmp_path),
        model="hotchpotch/model",
        model_type="dense",
        batch_size=2,
        show_progress=False,
        query_prompt=None,
        corpus_prompt=None,
        query_prompt_name=None,
        corpus_prompt_name=None,
        truncate_dim=None,
        candidate_subset_name="bm25",
        rerank_top_n=100,
        aggregate_metric="ndcg@10",
        dataset_revision="main",
        override=False,
    )
    monkeypatch.setattr(
        "nano_ir_benchmark.results.resolve_dataset_revision",
        lambda dataset_id, requested_revision=None: {
            "requested": requested_revision,
            "resolved": f"{dataset_id}@sha",
            "source": "huggingface_hub",
        },
    )

    result = run_or_load_task(
        task=task,
        model=FakeDenseModel(),
        args=args,
        environment={"package_versions": {}},
        model_metadata={"name_or_path": "hotchpotch/model"},
        dataset_loader=lambda _: _toy_dataset(),
    )

    assert result.payload["target"]["dataset_revision"] == {
        "requested": "main",
        "resolved": "toy/data@sha",
        "source": "huggingface_hub",
    }

    all_payload = build_all_payload(
        args=args,
        environment={"package_versions": {}},
        model_metadata={"name_or_path": "hotchpotch/model"},
        results=[result],
    )
    assert all_payload["splits"][0]["dataset_revision"]["resolved"] == "toy/data@sha"


def test_run_or_load_task_records_embedding_variant_evaluations(tmp_path: Path) -> None:
    task = _toy_task()
    args = argparse.Namespace(
        output_dir=str(tmp_path),
        model="hotchpotch/model",
        model_type="dense",
        batch_size=2,
        show_progress=False,
        query_prompt=None,
        corpus_prompt=None,
        query_prompt_name=None,
        corpus_prompt_name=None,
        truncate_dim=None,
        embedding_variants=[_pipeline_variant("truncate_dim_1", _truncate_step(1))],
        candidate_subset_name="bm25",
        rerank_top_n=100,
        aggregate_metric="ndcg@10",
        override=False,
    )

    result = run_or_load_task(
        task=task,
        model=FakeDenseModel(),
        args=args,
        environment={"package_versions": {}},
        model_metadata={"name_or_path": "hotchpotch/model"},
        dataset_loader=lambda _: _toy_dataset(),
    )

    assert result.payload["config"]["embedding_variants"] == args.embedding_variants
    embedding_evaluations = result.payload["evaluation"]["embedding_evaluations"]
    assert [item["name"] for item in embedding_evaluations] == ["base", "truncate_dim_1"]
    assert embedding_evaluations[1]["aggregate_metric"] == "ndcg@10"
    assert embedding_evaluations[1]["aggregate_metric_value"] < 1.0
    assert embedding_evaluations[1]["best_distance"] in {"dot", "cosine"}
    assert [item["distance"] for item in embedding_evaluations[1]["distance_evaluations"]] == ["dot", "cosine"]
    assert result.payload["metrics"] == embedding_evaluations[0]["metrics"]

    all_payload = build_all_payload(
        args=args,
        environment={"package_versions": {}},
        model_metadata={"name_or_path": "hotchpotch/model"},
        results=[result],
    )
    split_variants = all_payload["splits"][0]["embedding_evaluations"]
    assert [item["name"] for item in split_variants] == ["base", "truncate_dim_1"]
    assert split_variants[0]["embedding_dimensions"] == {"dim": 2}
    assert split_variants[0]["embedding_metadata"]["representation_type"] == "dense"
    assert split_variants[0]["best_distance"] == "dot"
    assert [item["distance"] for item in split_variants[0]["distance_evaluations"]] == ["dot", "cosine"]
    assert "metrics" not in split_variants[0]["distance_evaluations"][0]
    assert split_variants[1]["embedding_dimensions"] == {"dim": 1}
    assert "metrics" not in split_variants[1]


def test_run_or_load_task_records_sparse_max_active_dims(tmp_path: Path) -> None:
    task = _toy_task()
    args = argparse.Namespace(
        output_dir=str(tmp_path),
        model="naver/splade-v3",
        model_type="sparse",
        batch_size=2,
        show_progress=False,
        query_prompt=None,
        corpus_prompt=None,
        query_prompt_name=None,
        corpus_prompt_name=None,
        truncate_dim=None,
        sparse_max_active_dims=64,
        embedding_variants=[],
        candidate_subset_name="bm25",
        rerank_top_n=100,
        aggregate_metric="ndcg@10",
        override=False,
    )
    model = FakeSentenceTransformersSparseModel()

    result = run_or_load_task(
        task=task,
        model=model,
        args=args,
        environment={"package_versions": {}},
        model_metadata={"name_or_path": "naver/splade-v3"},
        dataset_loader=lambda _: _toy_dataset(),
    )

    assert model.query_calls[0]["max_active_dims"] == 64
    assert model.document_calls[0]["max_active_dims"] == 64
    assert result.payload["config"]["sparse_max_active_dims"] == 64

    all_payload = build_all_payload(
        args=args,
        environment={"package_versions": {}},
        model_metadata={"name_or_path": "naver/splade-v3"},
        results=[result],
    )
    assert all_payload["config"]["sparse_max_active_dims"] == 64
    assert all_payload["splits"][0]["config"]["sparse_max_active_dims"] == 64


def test_build_all_payload_includes_split_and_total_durations(tmp_path: Path) -> None:
    task = _toy_task()
    args = argparse.Namespace(
        output_dir=str(tmp_path),
        model="hotchpotch/model",
        model_type="dense",
        batch_size=2,
        show_progress=False,
        query_prompt=None,
        corpus_prompt=None,
        query_prompt_name=None,
        corpus_prompt_name=None,
        truncate_dim=None,
        candidate_subset_name="bm25",
        rerank_top_n=100,
        aggregate_metric="ndcg@10",
        override=False,
    )
    result = run_or_load_task(
        task=task,
        model=FakeDenseModel(),
        args=args,
        environment={"package_versions": {}},
        model_metadata={"name_or_path": "hotchpotch/model"},
        dataset_loader=lambda _: _toy_dataset(),
    )

    payload = build_all_payload(
        args=args,
        environment={"package_versions": {}},
        model_metadata={"name_or_path": "hotchpotch/model"},
        results=[result],
        run_started_at_utc="2026-04-27T00:00:00+00:00",
        run_finished_at_utc="2026-04-27T00:00:01+00:00",
        run_wall_seconds=1.0,
    )

    assert payload["run"]["started_at_utc"] == "2026-04-27T00:00:00+00:00"
    assert payload["run"]["finished_at_utc"] == "2026-04-27T00:00:01+00:00"
    assert payload["run"]["evaluated_at_utc"] == "2026-04-27T00:00:01+00:00"
    assert payload["run"]["wall_seconds"] == 1.0
    split = payload["splits"][0]
    assert split["started_at_utc"] == result.payload["evaluation"]["started_at_utc"]
    assert split["finished_at_utc"] == result.payload["evaluation"]["finished_at_utc"]
    assert split["dataset_load_seconds"] == result.payload["evaluation"]["dataset_load_seconds"]
    assert split["duration_seconds_including_dataset_load"] == result.payload["evaluation"][
        "duration_seconds_including_dataset_load"
    ]
    assert split["embedding_conversion"] == result.payload["evaluation"]["embedding_conversion"]
    assert payload["totals"]["duration_seconds_including_dataset_load_this_run"] == pytest.approx(
        result.payload["evaluation"]["duration_seconds_including_dataset_load"]
    )


def test_build_all_payload_aggregates_prompt_config_from_cached_splits(tmp_path: Path) -> None:
    task = _toy_task()
    args = argparse.Namespace(
        output_dir=str(tmp_path),
        model="cl-nagoya/ruri-v3-30m",
        model_type="dense",
        batch_size=8,
        show_progress=False,
        query_prompt=None,
        corpus_prompt=None,
        query_prompt_name=None,
        corpus_prompt_name=None,
        query_task=None,
        corpus_task=None,
        truncate_dim=None,
        candidate_subset_name="bm25",
        rerank_top_n=100,
        aggregate_metric="ndcg@10",
        override=False,
    )
    cached_payload = {
        "target": {"dataset_revision": {"resolved": "toy/data@sha"}},
        "config": {
            "batch_size": 4,
            "aggregate_metric": "ndcg@10",
            "query_prompt": "検索クエリ: ",
            "corpus_prompt": "検索文書: ",
            "query_prompt_name": None,
            "corpus_prompt_name": None,
            "query_task": None,
            "corpus_task": None,
        },
        "evaluation": {
            "aggregate_metric": "ndcg@10",
            "aggregate_metric_value": 1.0,
            "timing": {},
        },
    }
    result = TaskRunResult(
        task=task,
        cache_hit=True,
        output_path=tmp_path / "task.json",
        payload=cached_payload,
    )

    payload = build_all_payload(
        args=args,
        environment={"package_versions": {}},
        model_metadata={"name_or_path": "cl-nagoya/ruri-v3-30m"},
        results=[result],
    )

    assert payload["cli_args"]["query_prompt"] is None
    assert payload["config"]["query_prompt"] == "検索クエリ: "
    assert payload["config"]["corpus_prompt"] == "検索文書: "
    assert payload["config"]["batch_size"] == 4
    assert payload["config"]["prompt_summary"]["query_prompt"] == {
        "consistent": True,
        "value": "検索クエリ: ",
        "values": [{"value": "検索クエリ: ", "count": 1}],
    }
    assert payload["splits"][0]["config"]["query_prompt"] == "検索クエリ: "
    assert payload["splits"][0]["config"]["corpus_prompt"] == "検索文書: "


def test_build_all_payload_uses_task_model_metadata_when_consistent(tmp_path: Path) -> None:
    task = _toy_task()
    args = argparse.Namespace(
        output_dir=str(tmp_path),
        model="bm25/bm25s-okapi-auto",
        model_type="bm25",
        batch_size=2,
        show_progress=False,
        query_prompt=None,
        corpus_prompt=None,
        query_prompt_name=None,
        corpus_prompt_name=None,
        truncate_dim=None,
        candidate_subset_name="bm25",
        rerank_top_n=100,
        aggregate_metric="ndcg@10",
        override=False,
        bm25_tokenizer=None,
        bm25_tokenizer_name=None,
        bm25_stemmer_algorithm="english",
        bm25_k1=1.5,
        bm25_b=0.75,
        top_k=1,
    )
    result = run_or_load_task(
        task=task,
        model=None,
        args=args,
        environment={"package_versions": {}},
        model_metadata={"name_or_path": "stale"},
        dataset_loader=lambda _: _toy_dataset(),
    )

    payload = build_all_payload(
        args=args,
        environment={"package_versions": {}},
        model_metadata={"name_or_path": "stale"},
        results=[result],
    )

    assert payload["model"]["bm25"]["source"] == "dataset_candidate_subset"


def test_run_or_load_task_records_auto_bm25_config(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    task = _toy_task()
    args = argparse.Namespace(
        output_dir=str(tmp_path),
        model="bm25/bm25s-okapi-auto",
        model_type="bm25",
        batch_size=2,
        show_progress=False,
        query_prompt=None,
        corpus_prompt=None,
        query_prompt_name=None,
        corpus_prompt_name=None,
        truncate_dim=None,
        candidate_subset_name="bm25",
        rerank_top_n=100,
        aggregate_metric="ndcg@10",
        override=False,
        bm25_tokenizer=None,
        bm25_tokenizer_name=None,
        bm25_stemmer_algorithm="english",
        bm25_k1=1.5,
        bm25_b=0.75,
        top_k=3,
    )
    monkeypatch.setattr(
        "nano_ir_benchmark.bm25._detect_language",
        lambda _: {"lang": "en", "score": 0.99},
    )

    result = run_or_load_task(
        task=task,
        model=None,
        args=args,
        environment={"package_versions": {}},
        model_metadata={"name_or_path": "bm25/bm25s-okapi-auto"},
        dataset_loader=lambda _: _toy_dataset_without_candidates(),
    )

    assert result.payload["config"]["bm25"]["algorithm"] == "okapi"
    assert result.payload["config"]["bm25"]["tokenizer"] == "regex"
    assert result.payload["config"]["bm25"]["auto_selected"] is True
    assert result.payload["config"]["bm25"]["auto_detected_language"] == "en"
    assert result.payload["model"]["bm25"]["tokenizer"] == "regex"


def test_run_or_load_task_records_bm25_candidate_subset_source(tmp_path: Path) -> None:
    task = _toy_task()
    args = argparse.Namespace(
        output_dir=str(tmp_path),
        model="bm25/bm25s-okapi-auto",
        model_type="bm25",
        batch_size=2,
        show_progress=False,
        query_prompt=None,
        corpus_prompt=None,
        query_prompt_name=None,
        corpus_prompt_name=None,
        truncate_dim=None,
        candidate_subset_name="bm25",
        rerank_top_n=100,
        aggregate_metric="ndcg@10",
        override=False,
        bm25_tokenizer=None,
        bm25_tokenizer_name=None,
        bm25_stemmer_algorithm="english",
        bm25_k1=1.5,
        bm25_b=0.75,
        top_k=1,
    )

    result = run_or_load_task(
        task=task,
        model=None,
        args=args,
        environment={"package_versions": {}},
        model_metadata={"name_or_path": "bm25/bm25s-okapi-auto"},
        dataset_loader=lambda _: _toy_dataset(),
    )

    assert result.payload["config"]["candidate_subset_name"] == "bm25"
    assert result.payload["config"]["bm25"]["source"] == "dataset_candidate_subset"
    assert result.payload["config"]["bm25"]["candidate_subset_name"] == "bm25"
    assert result.payload["model"]["bm25"]["source"] == "dataset_candidate_subset"
    assert result.payload["evaluation"]["aggregate_metric_value"] == pytest.approx(0.5)
