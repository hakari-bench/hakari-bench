from __future__ import annotations

import argparse
import json
import sys
import types
from pathlib import Path

import numpy as np
import pytest
import torch
from scipy import sparse

import hakari_bench.evaluation as evaluation_module
from hakari_bench.datasets import EvalTask, NanoDatasetSpec
from hakari_bench.evaluation import (
    LoadedIrDataset,
    QuantizedEmbeddingMatrix,
    candidate_safeguard_metadata,
    evaluate_dense_task,
    evaluate_late_interaction_task,
    evaluate_reranker_task,
    load_ir_dataset,
)
from hakari_bench.results import TaskRunResult, build_run_summary_payload, result_path_for_task, run_or_load_task, safe_path_part


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


def _cuda_test_device_is_usable() -> bool:
    if not torch.cuda.is_available():
        return False
    try:
        torch.empty((1,), dtype=torch.float32, device="cuda")
        torch.cuda.synchronize()
    except RuntimeError:
        torch.cuda.empty_cache()
        return False
    return True


CUDA_TEST_DEVICE_IS_USABLE = _cuda_test_device_is_usable()


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


def test_candidate_safeguard_metadata_identifies_rank101_positive() -> None:
    candidates = {
        "q1": [f"d{i:03d}" for i in range(100)] + ["d120"],
        "q2": [f"x{i:03d}" for i in range(100)],
        "q3": [f"y{i:03d}" for i in range(50)],
    }

    metadata = candidate_safeguard_metadata(
        candidates=candidates,
        qrels={"q1": {"d120"}, "q2": {"x010"}, "q3": {"y049"}},
    )

    assert metadata["policy"] == "RRF top-100 plus optional safeguard positive at rank 101"
    assert metadata["candidate_count_100"] == 1
    assert metadata["candidate_count_101"] == 1
    assert metadata["safeguard_query_count"] == 1
    assert metadata["safeguard_corpus_ids_by_query"] == {"q1": "d120"}


def test_load_ir_dataset_can_restrict_corpus_to_candidate_documents(monkeypatch: pytest.MonkeyPatch) -> None:
    task = _toy_task()
    calls: list[tuple[str, str]] = []

    def fake_load_dataset(dataset_id: str, config_name: str, *, split: str, revision: str | None = None) -> list[dict[str, object]]:
        assert dataset_id == "toy/data"
        assert split == "test"
        assert revision == "abc123"
        calls.append((config_name, split))
        if config_name == "bm25":
            return [{"query-id": "q1", "corpus-ids": ["d1", "d3"]}]
        if config_name == "corpus":
            return [
                {"_id": "d1", "text": "candidate doc"},
                {"_id": "d2", "text": "non candidate doc"},
                {"_id": "d3", "text": "candidate doc 2"},
            ]
        if config_name == "queries":
            return [{"_id": "q1", "text": "query"}]
        if config_name == "qrels":
            return [{"query-id": "q1", "corpus-id": "d2"}]
        raise AssertionError(config_name)

    monkeypatch.setitem(sys.modules, "datasets", types.SimpleNamespace(load_dataset=fake_load_dataset))

    dataset = load_ir_dataset(
        task,
        candidate_subset_name="bm25",
        revision="abc123",
        restrict_corpus_to_candidates=True,
    )

    assert dataset.corpus == {"d1": "candidate doc", "d3": "candidate doc 2"}
    assert dataset.qrels == {"q1": {"d2"}}
    assert dataset.candidates == {"q1": ["d1", "d3"]}
    assert calls == [("queries", "test"), ("qrels", "test"), ("bm25", "test"), ("corpus", "test")]


def test_load_ir_dataset_forces_redownload_for_local_dataset_paths(
    monkeypatch: pytest.MonkeyPatch,
    tmp_path: Path,
) -> None:
    task = EvalTask(
        dataset=NanoDatasetSpec(name="NanoLocal", dataset_id=str(tmp_path), candidate_config="reranking_hybrid"),
        split_name="test",
        task_name="test",
    )
    force_redownload = object()
    calls: list[tuple[str, object | None]] = []

    def fake_load_dataset(
        dataset_id: str,
        config_name: str,
        *,
        split: str,
        revision: str | None = None,
        download_mode: object | None = None,
    ) -> list[dict[str, object]]:
        assert dataset_id == str(tmp_path)
        assert split == "test"
        assert revision is None
        calls.append((config_name, download_mode))
        if config_name == "reranking_hybrid":
            return [{"query-id": "q1", "corpus-ids": ["d1"]}]
        if config_name == "corpus":
            return [{"_id": "d1", "text": "candidate doc"}]
        if config_name == "queries":
            return [{"_id": "q1", "text": "query"}]
        if config_name == "qrels":
            return [{"query-id": "q1", "corpus-id": "d1"}]
        raise AssertionError(config_name)

    monkeypatch.setitem(
        sys.modules,
        "datasets",
        types.SimpleNamespace(
            load_dataset=fake_load_dataset,
            DownloadMode=types.SimpleNamespace(FORCE_REDOWNLOAD=force_redownload),
        ),
    )

    dataset = load_ir_dataset(task, candidate_subset_name="reranking_hybrid")

    assert dataset.candidates == {"q1": ["d1"]}
    assert calls == [
        ("queries", force_redownload),
        ("qrels", force_redownload),
        ("reranking_hybrid", force_redownload),
        ("corpus", force_redownload),
    ]


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


class FakeMultiProcessDenseModel(FakeDenseModel):
    def __init__(self) -> None:
        super().__init__()
        self.started_devices: list[str] | None = None
        self.stopped_pool: dict[str, object] | None = None

    def start_multi_process_pool(self, target_devices: list[str] | None = None) -> dict[str, object]:
        self.started_devices = target_devices
        return {"target_devices": target_devices, "processes": []}

    def stop_multi_process_pool(self, pool: dict[str, object]) -> None:
        self.stopped_pool = pool

    def encode_query(
        self,
        sentences: list[str],
        *,
        pool: dict[str, object] | None = None,
        chunk_size: int | None = None,
        **kwargs: object,
    ) -> np.ndarray:
        self.query_calls.append({"sentences": sentences, "pool": pool, "chunk_size": chunk_size, **kwargs})
        return np.array([[1.0, 0.0], [0.0, 1.0]])

    def encode_document(
        self,
        sentences: list[str],
        *,
        pool: dict[str, object] | None = None,
        chunk_size: int | None = None,
        **kwargs: object,
    ) -> np.ndarray:
        self.document_calls.append({"sentences": sentences, "pool": pool, "chunk_size": chunk_size, **kwargs})
        return np.array([[1.0, 0.0], [0.0, 1.0], [-1.0, 0.0]])


class FakeCudaDenseModel:
    similarity_fn_name = "dot"
    prompts = {"query": "query: ", "document": "document: "}
    default_prompt_name = None
    device = torch.device("cuda")

    def __init__(self) -> None:
        self.query_calls: list[dict[str, object]] = []
        self.document_calls: list[dict[str, object]] = []

    def encode_query(self, sentences: list[str], **kwargs: object) -> np.ndarray | torch.Tensor:
        self.query_calls.append({"sentences": sentences, **kwargs})
        if kwargs.get("convert_to_tensor"):
            return torch.tensor([[1.0, 0.0], [0.0, 1.0]], dtype=torch.float32)
        return np.array([[1.0, 0.0], [0.0, 1.0]], dtype=np.float32)

    def encode_document(self, sentences: list[str], **kwargs: object) -> np.ndarray | torch.Tensor:
        self.document_calls.append({"sentences": sentences, **kwargs})
        if kwargs.get("convert_to_tensor"):
            return torch.tensor([[1.0, 0.0], [0.0, 1.0], [-1.0, 0.0]], dtype=torch.float32)
        return np.array([[1.0, 0.0], [0.0, 1.0], [-1.0, 0.0]], dtype=np.float32)


class FakeCudaLateInteractionModel:
    similarity_fn_name = "dot"
    device = torch.device("cuda")

    def __init__(self) -> None:
        self.query_calls: list[dict[str, object]] = []
        self.document_calls: list[dict[str, object]] = []

    def encode_query(self, sentences: list[str], **kwargs: object) -> np.ndarray | torch.Tensor:
        self.query_calls.append({"sentences": sentences, **kwargs})
        values = np.array(
            [
                [[1.0, 0.0], [0.0, 1.0]],
                [[-1.0, 0.0], [0.0, -1.0]],
            ],
            dtype=np.float32,
        )
        if kwargs.get("convert_to_tensor"):
            return torch.from_numpy(values)
        return values

    def encode_document(self, sentences: list[str], **kwargs: object) -> np.ndarray | torch.Tensor:
        self.document_calls.append({"sentences": sentences, **kwargs})
        values = np.array(
            [
                [[1.0, 0.0], [0.0, 1.0]],
                [[-1.0, 0.0], [0.0, -1.0]],
                [[0.0, 1.0], [1.0, 0.0]],
            ],
            dtype=np.float32,
        )
        if kwargs.get("convert_to_tensor"):
            return torch.from_numpy(values)
        return values


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


class FakeCudaSentenceTransformersSparseModel(FakeSentenceTransformersSparseModel):
    device = torch.device("cuda")


class FakeReranker:
    def predict(self, pairs: list[list[str]], **kwargs: object) -> list[float]:
        return [1.0 if tuple(pair) in {("cat query", "cat doc"), ("dog query", "dog doc")} else 0.0 for pair in pairs]


class FakeLateInteractionModel:
    def __init__(self) -> None:
        self.calls: list[dict[str, object]] = []

    def encode(self, sentences: list[str], **kwargs: object) -> list[np.ndarray]:
        self.calls.append({"sentences": sentences, **kwargs})
        if kwargs["is_query"]:
            return [
                np.array([[1.0, 0.0], [0.5, 0.0]], dtype=np.float32),
                np.array([[0.0, 1.0], [0.0, 0.5]], dtype=np.float32),
            ]
        return [
            np.array([[1.0, 0.0]], dtype=np.float32),
            np.array([[0.0, 1.0]], dtype=np.float32),
            np.array([[-1.0, 0.0]], dtype=np.float32),
        ]


class FakeRenamedTextLengthLateInteractionModel(FakeLateInteractionModel):
    def _input_length(self, sentence: str) -> int:
        return len(sentence)

    def encode(self, sentences: list[str], **kwargs: object) -> list[np.ndarray]:
        text_length = getattr(self, "_text_length")
        assert [text_length(sentence) for sentence in sentences] == [len(sentence) for sentence in sentences]
        return super().encode(sentences, **kwargs)


class FakeRankReranker:
    def rank(self, query: str, documents: list[str], **kwargs: object) -> list[dict[str, object]]:
        del kwargs
        scored = [
            (index, 1.0 if document.startswith(query.split()[0]) else 0.0)
            for index, document in enumerate(documents)
        ]
        return [
            {"corpus_id": index, "score": score}
            for index, score in sorted(scored, key=lambda item: (-item[1], item[0]))
        ]


class FakeCallableReranker:
    def __call__(self, pairs: list[list[str]], **kwargs: object) -> list[float]:
        del kwargs
        return [1.0 if tuple(pair) in {("cat query", "cat doc"), ("dog query", "dog doc")} else 0.0 for pair in pairs]


class FakeTiePredictReranker:
    def predict(self, pairs: list[list[str]], **kwargs: object) -> list[float]:
        del kwargs
        return [0.0 for _pair in pairs]


class FakePredictAndRankReranker:
    def __init__(self) -> None:
        self.predict_calls: list[dict[str, object]] = []
        self.rank_calls: list[dict[str, object]] = []

    def predict(self, pairs: list[list[str]], **kwargs: object) -> list[float]:
        self.predict_calls.append({"pairs": pairs, **kwargs})
        return [1.0 if tuple(pair) in {("cat query", "cat doc"), ("dog query", "dog doc")} else 0.0 for pair in pairs]

    def rank(self, query: str, documents: list[str], **kwargs: object) -> list[dict[str, object]]:
        self.rank_calls.append({"query": query, "documents": documents, **kwargs})
        return [{"corpus_id": index, "score": 0.0} for index, _document in enumerate(documents)]


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
    assert result.metrics["ToyData_test_dot_acc@100"] == pytest.approx(1.0)
    assert set(result.metrics) == {"ToyData_test_dot_ndcg@10", "ToyData_test_dot_acc@100"}
    assert model.query_calls[0]["sentences"] == ["cat query", "dog query"]
    assert "prompt" not in model.query_calls[0]
    assert "prompt_name" not in model.query_calls[0]


def test_evaluate_dense_task_requests_tensor_embeddings_for_cuda_models_by_default() -> None:
    model = FakeCudaDenseModel()

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

    assert model.query_calls[0]["convert_to_tensor"] is True
    assert model.document_calls[0]["convert_to_tensor"] is True
    assert result.embedding_evaluations[0]["embedding_metadata"]["query"]["device"] == "cpu"
    assert result.metrics["ToyData_test_dot_ndcg@10"] == pytest.approx(1.0)


def test_evaluate_dense_task_score_device_cpu_uses_numpy_embeddings_for_cuda_models() -> None:
    model = FakeCudaDenseModel()

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
        score_device="cpu",
    )

    assert model.query_calls[0]["convert_to_numpy"] is True
    assert model.document_calls[0]["convert_to_numpy"] is True
    assert "device" not in result.embedding_evaluations[0]["embedding_metadata"]["query"]
    assert result.metrics["ToyData_test_dot_ndcg@10"] == pytest.approx(1.0)


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


def test_evaluate_dense_task_warns_and_skips_noop_truncate_variants(capsys) -> None:
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
        embedding_variants=[_pipeline_variant("truncate_dim_2", _truncate_step(2))],
    )

    assert [item["name"] for item in result.embedding_evaluations] == ["base"]
    captured = capsys.readouterr()
    assert "warning: skipping embedding variant truncate_dim_2" in captured.err
    assert "truncate dimension 2 matches the base embedding dimension" in captured.err


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
            _quantized_variant("int8", "int8"),
            _quantized_variant("binary", "binary"),
            _quantized_variant("int8_rescore", "int8", rescore=True),
            _quantized_variant("binary_rescore", "binary", rescore=True),
        ],
    )

    assert len(model.query_calls) == 1
    assert len(model.document_calls) == 1
    assert "precision" not in model.query_calls[0]
    assert "precision" not in model.document_calls[0]

    assert [item["name"] for item in result.embedding_evaluations] == [
        "base",
        "int8",
        "binary",
        "int8_rescore",
        "binary_rescore",
    ]
    int8_eval = result.embedding_evaluations[1]
    assert int8_eval["aggregate_metric_value"] == pytest.approx(1.0)
    assert int8_eval["best_score"] == pytest.approx(1.0)
    assert int8_eval["best_distance"] == "dot"
    assert [item["distance"] for item in int8_eval["distance_evaluations"]] == ["dot", "cosine"]
    assert int8_eval["embedding_dimensions"] == {"dim": 2}
    assert int8_eval["embedding_metadata"]["dimension_format"] == "single_vector"
    assert int8_eval["embedding_metadata"]["query"]["quantization"]["score_representation"] == "torch_exact"
    assert int8_eval["embedding_metadata"]["corpus"]["quantization"] == {
        "precision": "int8",
        "algorithm": "sentence_transformers_embedding_quantization",
        "ranges_source": "corpus",
        "original_dim": 2,
        "stored_dim": 2,
        "score_representation": "torch_exact",
        "method": "query_and_corpus",
        "side": "corpus",
        "rounding": "truncate",
        "search_backend": "torch",
        "search_device": "cpu",
        "search_exact": True,
        "candidate_top_k": 100,
        "rescore": False,
    }

    binary_eval = result.embedding_evaluations[2]
    assert binary_eval["aggregate_metric_value"] == pytest.approx(1.0)
    assert [item["distance"] for item in binary_eval["distance_evaluations"]] == ["dot", "cosine"]
    assert binary_eval["embedding_dimensions"] == {"dim": 2}
    assert binary_eval["embedding_metadata"]["dimension_format"] == "binary_bit_vector"
    assert binary_eval["embedding_metadata"]["corpus"]["quantization"]["precision"] == "binary"
    assert binary_eval["embedding_metadata"]["corpus"]["quantization"]["score_representation"] == "torch_exact"
    assert "ToyData_test_dot_binary_ndcg@10" in binary_eval["metrics"]

    int8_rescore_eval = result.embedding_evaluations[3]
    assert int8_rescore_eval["aggregate_metric_value"] == pytest.approx(1.0)
    assert int8_rescore_eval["embedding_metadata"]["corpus"]["quantization"]["score_representation"] == (
        "torch_exact_rescore"
    )
    assert int8_rescore_eval["embedding_metadata"]["corpus"]["quantization"]["candidate_top_k"] == 100
    assert int8_rescore_eval["embedding_metadata"]["corpus"]["quantization"]["rescore"] is True
    assert "ToyData_test_dot_int8_rescore_ndcg@10" in int8_rescore_eval["metrics"]

    binary_rescore_eval = result.embedding_evaluations[4]
    assert binary_rescore_eval["aggregate_metric_value"] == pytest.approx(1.0)
    assert binary_rescore_eval["embedding_metadata"]["corpus"]["quantization"]["score_representation"] == (
        "torch_exact_rescore"
    )
    assert binary_rescore_eval["embedding_metadata"]["corpus"]["quantization"]["candidate_top_k"] == 100
    assert binary_rescore_eval["embedding_metadata"]["corpus"]["quantization"]["rescore"] is True
    assert "ToyData_test_dot_binary_rescore_ndcg@10" in binary_rescore_eval["metrics"]


def test_quantize_int8_uses_sentence_transformers_truncating_bucket_cast() -> None:
    query_embeddings = np.array([[0.492]], dtype=np.float32)
    corpus_embeddings = np.array([[0.0], [1.0], [0.492]], dtype=np.float32)

    _query_result, corpus_quantized = evaluation_module._quantize_embedding_pair(
        query_embeddings=query_embeddings,
        corpus_embeddings=corpus_embeddings,
        precision="int8",
        algorithm="sentence_transformers_embedding_quantization",
        target="query_and_corpus",
    )

    # SentenceTransformers quantize_embeddings casts bucket values directly to
    # int8 rather than rounding to nearest. Keep parity so benchmark variants
    # do not look better than the library's documented scalar quantization.
    assert corpus_quantized.values[:, 0].tolist() == [-128, 126, -2]
    assert corpus_quantized.rounding == "truncate"


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


def test_embedding_pipeline_can_l2_normalize_dense_embeddings() -> None:
    query_embeddings = np.array([[3.0, 4.0], [0.0, 0.0]], dtype=np.float32)
    corpus_embeddings = np.array([[0.0, 5.0], [12.0, 5.0]], dtype=np.float32)

    normalized_query, normalized_corpus = evaluation_module._apply_embedding_pipeline_pair(
        query_embeddings=query_embeddings,
        corpus_embeddings=corpus_embeddings,
        steps=[_normalize_step()],
    )

    np.testing.assert_allclose(normalized_query[0], np.array([0.6, 0.8], dtype=np.float32), atol=1e-6)
    np.testing.assert_allclose(normalized_query[1], np.array([0.0, 0.0], dtype=np.float32), atol=1e-6)
    np.testing.assert_allclose(
        np.linalg.norm(normalized_corpus, axis=1),
        np.ones(2, dtype=np.float32),
        atol=1e-6,
    )


def test_torch_dense_rank_by_similarity_does_not_convert_to_numpy(monkeypatch) -> None:
    def fail_to_numpy(embeddings):
        raise AssertionError(f"Unexpected NumPy conversion for {type(embeddings).__name__}")

    monkeypatch.setattr(evaluation_module, "_to_numpy_float32", fail_to_numpy)
    query_embeddings = torch.tensor([[1.0, 0.0], [0.0, 1.0]], dtype=torch.float32)
    corpus_embeddings = torch.tensor([[0.0, 1.0], [1.0, 0.0], [-1.0, 0.0]], dtype=torch.float32)

    rankings = evaluation_module._rank_by_similarity(
        query_ids=["q1", "q2"],
        corpus_ids=["d2", "d1", "d3"],
        query_embeddings=query_embeddings,
        corpus_embeddings=corpus_embeddings,
        score_name="dot",
    )

    assert rankings["q1"] == ["d1", "d2", "d3"]
    assert rankings["q2"] == ["d2", "d1", "d3"]


def test_candidate_subset_rank_by_similarity_scores_only_candidate_documents() -> None:
    rankings = evaluation_module._rank_candidate_subset_by_similarity(
        query_ids=["q1", "q2"],
        corpus_ids=["d1", "d2", "d3"],
        query_embeddings=np.array([[1.0, 0.0], [0.0, 1.0]], dtype=np.float32),
        corpus_embeddings=np.array(
            [
                [1.0, 0.0],
                [0.0, 1.0],
                [-1.0, 0.0],
            ],
            dtype=np.float32,
        ),
        candidates={"q1": ["d3", "d1"], "q2": ["d1", "d2"]},
        score_name="dot",
        rerank_top_n=2,
    )

    assert rankings == {"q1": ["d1", "d3"], "q2": ["d2", "d1"]}


@pytest.mark.filterwarnings("ignore:Sparse CSR tensor support is in beta state.*:UserWarning")
def test_candidate_subset_rank_by_similarity_supports_torch_sparse_csr() -> None:
    rankings = evaluation_module._rank_candidate_subset_by_similarity(
        query_ids=["q1", "q2"],
        corpus_ids=["d1", "d2", "d3"],
        query_embeddings=torch.tensor([[1.0, 0.0], [0.0, 1.0]]).to_sparse_csr(),
        corpus_embeddings=torch.tensor(
            [
                [1.0, 0.0],
                [0.0, 1.0],
                [-1.0, 0.0],
            ],
            dtype=torch.float32,
        ).to_sparse_csr(),
        candidates={"q1": ["d3", "d1"], "q2": ["d1", "d2"]},
        score_name="dot",
        rerank_top_n=2,
    )

    assert rankings == {"q1": ["d1", "d3"], "q2": ["d2", "d1"]}


@pytest.mark.skipif(not CUDA_TEST_DEVICE_IS_USABLE, reason="CUDA is not available or cannot allocate a test tensor")
def test_cuda_dense_rank_by_similarity_keeps_scoring_on_cuda(monkeypatch) -> None:
    def fail_to_numpy(embeddings):
        raise AssertionError(f"Unexpected NumPy conversion for {type(embeddings).__name__}")

    monkeypatch.setattr(evaluation_module, "_to_numpy_float32", fail_to_numpy)
    query_embeddings = torch.tensor([[1.0, 0.0]], dtype=torch.float32, device="cuda")
    corpus_embeddings = torch.tensor([[0.0, 1.0], [1.0, 0.0]], dtype=torch.float32, device="cuda")

    rankings = evaluation_module._rank_by_similarity(
        query_ids=["q1"],
        corpus_ids=["d2", "d1"],
        query_embeddings=query_embeddings,
        corpus_embeddings=corpus_embeddings,
        score_name="dot",
    )

    assert rankings["q1"] == ["d1", "d2"]


def test_embedding_pipeline_keeps_torch_normalize_on_device() -> None:
    query_embeddings = torch.tensor([[3.0, 4.0], [0.0, 0.0]], dtype=torch.float32)
    corpus_embeddings = torch.tensor([[0.0, 5.0], [12.0, 5.0]], dtype=torch.float32)

    normalized_query, normalized_corpus = evaluation_module._apply_embedding_pipeline_pair(
        query_embeddings=query_embeddings,
        corpus_embeddings=corpus_embeddings,
        steps=[_normalize_step()],
    )

    assert isinstance(normalized_query, torch.Tensor)
    assert isinstance(normalized_corpus, torch.Tensor)
    assert normalized_query.device == query_embeddings.device
    assert normalized_corpus.device == corpus_embeddings.device
    torch.testing.assert_close(normalized_query[0], torch.tensor([0.6, 0.8]))
    torch.testing.assert_close(normalized_query[1], torch.tensor([0.0, 0.0]))
    torch.testing.assert_close(torch.linalg.vector_norm(normalized_corpus, dim=1), torch.ones(2))


def test_embedding_pipeline_normalizes_before_quantization_rescore_sources() -> None:
    query_embeddings = np.array([[3.0, 4.0]], dtype=np.float32)
    corpus_embeddings = np.array([[0.0, 5.0], [12.0, 5.0]], dtype=np.float32)

    query_quantized, corpus_quantized = evaluation_module._apply_embedding_pipeline_pair(
        query_embeddings=query_embeddings,
        corpus_embeddings=corpus_embeddings,
        steps=[
            _normalize_step(),
            _quantized_step("int8", rescore=True),
        ],
    )

    assert query_quantized.score_representation == "torch_exact_rescore"
    assert corpus_quantized.score_representation == "torch_exact_rescore"
    assert query_quantized.source_values is not None
    assert corpus_quantized.source_values is not None
    np.testing.assert_allclose(
        np.linalg.norm(evaluation_module._to_numpy_float32(query_quantized.source_values), axis=1),
        [1.0],
        atol=1e-6,
    )
    np.testing.assert_allclose(
        np.linalg.norm(evaluation_module._to_numpy_float32(corpus_quantized.source_values), axis=1),
        [1.0, 1.0],
        atol=1e-6,
    )


def test_torch_int8_rescore_reranks_candidates_with_source_float_embeddings() -> None:
    ranges = torch.tensor([[0.0, 0.0], [1.0, 1.0]], dtype=torch.float32)
    query_quantized = QuantizedEmbeddingMatrix(
        values=torch.tensor([[-102, -102]], dtype=torch.int8),
        precision="int8",
        original_dim=2,
        algorithm="sentence_transformers_embedding_quantization",
        method="query_and_corpus",
        side="query",
        ranges_source="corpus",
        ranges=ranges,
        rounding="truncate",
        score_representation="torch_exact",
    )
    corpus_quantized = QuantizedEmbeddingMatrix(
        values=torch.tensor([[-102, -102], [-128, -128]], dtype=torch.int8),
        precision="int8",
        original_dim=2,
        algorithm="sentence_transformers_embedding_quantization",
        method="query_and_corpus",
        side="corpus",
        ranges_source="corpus",
        ranges=ranges,
        rounding="truncate",
        score_representation="torch_exact",
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
        score_representation="torch_exact_rescore",
        source_values=torch.tensor([[0.1, 0.1]], dtype=torch.float32),
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
        score_representation="torch_exact_rescore",
        source_values=torch.tensor([[0.1, 0.1], [0.0, 0.0]], dtype=torch.float32),
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


def test_torch_int8_ranks_by_quantized_code_dot_product() -> None:
    torch_query = QuantizedEmbeddingMatrix(
        values=torch.tensor([[-102, -102]], dtype=torch.int8),
        precision="int8",
        original_dim=2,
        algorithm="sentence_transformers_embedding_quantization",
        method="query_and_corpus",
        side="query",
        ranges_source="corpus",
        ranges=torch.tensor([[0.0, 0.0], [1.0, 1.0]], dtype=torch.float32),
        rounding="truncate",
        score_representation="torch_exact",
    )
    torch_corpus = QuantizedEmbeddingMatrix(
        values=torch.tensor([[-102, -102], [-128, -128]], dtype=torch.int8),
        precision="int8",
        original_dim=2,
        algorithm="sentence_transformers_embedding_quantization",
        method="query_and_corpus",
        side="corpus",
        ranges_source="corpus",
        ranges=torch.tensor([[0.0, 0.0], [1.0, 1.0]], dtype=torch.float32),
        rounding="truncate",
        score_representation="torch_exact",
    )

    torch_rankings = evaluation_module._rank_by_similarity(
        query_ids=["q1"],
        corpus_ids=["d1", "d2"],
        query_embeddings=torch_query,
        corpus_embeddings=torch_corpus,
        score_name="cosine",
    )

    assert torch_rankings == {"q1": ["d2", "d1"]}
    metadata = evaluation_module._quantization_metadata(torch_corpus)
    assert metadata["search_backend"] == "torch"
    assert metadata["search_device"] == "cpu"


def test_torch_binary_ranks_like_numpy_hamming_distance() -> None:
    query_embeddings = torch.tensor([[1.0, -1.0]], dtype=torch.float32)
    corpus_embeddings = torch.tensor([[1.0, -1.0], [-1.0, 1.0]], dtype=torch.float32)

    torch_query, torch_corpus = evaluation_module._quantize_embedding_pair(
        query_embeddings=query_embeddings,
        corpus_embeddings=corpus_embeddings,
        precision="binary",
        target="query_and_corpus",
        algorithm="sentence_transformers_embedding_quantization",
        score_representation="torch_exact",
    )
    rankings = evaluation_module._rank_by_similarity(
        query_ids=["q1"],
        corpus_ids=["d1", "d2"],
        query_embeddings=torch_query,
        corpus_embeddings=torch_corpus,
        score_name="dot",
    )

    assert rankings["q1"] == ["d1", "d2"]
    assert isinstance(torch_query.values, torch.Tensor)
    assert torch_query.values.shape == (1, 2)
    assert evaluation_module._quantization_metadata(torch_corpus)["binary_encoding"] == "unpacked_bits"


def test_torch_sparse_rank_by_similarity_does_not_convert_to_scipy(monkeypatch) -> None:
    def fail_to_scipy(embeddings):
        raise AssertionError(f"Unexpected SciPy conversion for {type(embeddings).__name__}")

    monkeypatch.setattr(evaluation_module, "_to_scipy_csr_matrix", fail_to_scipy)
    query_embeddings = torch.tensor([[1.0, 0.0, 2.0], [0.0, 3.0, 0.0]], dtype=torch.float32).to_sparse()
    corpus_embeddings = torch.tensor(
        [[1.0, 0.0, 1.0], [0.0, 2.0, 0.0], [0.0, 0.0, 4.0]], dtype=torch.float32
    ).to_sparse()

    rankings = evaluation_module._rank_by_similarity(
        query_ids=["q1", "q2"],
        corpus_ids=["d1", "d2", "d3"],
        query_embeddings=query_embeddings,
        corpus_embeddings=corpus_embeddings,
        score_name="dot",
    )

    assert rankings["q1"] == ["d3", "d1", "d2"]
    assert rankings["q2"] == ["d2", "d1", "d3"]


def test_torch_sparse_truncation_does_not_convert_to_scipy(monkeypatch) -> None:
    def fail_to_scipy(embeddings):
        raise AssertionError(f"Unexpected SciPy conversion for {type(embeddings).__name__}")

    monkeypatch.setattr(evaluation_module, "_to_scipy_csr_matrix", fail_to_scipy)
    embeddings = torch.tensor([[1.0, 0.0, -3.0], [0.0, 2.0, 4.0]], dtype=torch.float32).to_sparse()

    limited = evaluation_module._limit_sparse_active_dims(embeddings, max_active_dims=1)

    assert isinstance(limited, torch.Tensor)
    assert limited.is_sparse
    torch.testing.assert_close(
        limited.to_dense(),
        torch.tensor([[0.0, 0.0, -3.0], [0.0, 0.0, 4.0]], dtype=torch.float32),
    )


def test_torch_late_interaction_rank_by_similarity_uses_maxsim_without_numpy(monkeypatch) -> None:
    def fail_to_numpy(embeddings):
        raise AssertionError(f"Unexpected NumPy conversion for {type(embeddings).__name__}")

    monkeypatch.setattr(evaluation_module, "_to_numpy_float32", fail_to_numpy)
    query_embeddings = torch.tensor(
        [
            [[1.0, 0.0], [0.0, 1.0]],
            [[-1.0, 0.0], [0.0, -1.0]],
        ],
        dtype=torch.float32,
    )
    corpus_embeddings = torch.tensor(
        [
            [[1.0, 0.0], [0.0, 1.0]],
            [[-1.0, 0.0], [0.0, -1.0]],
            [[0.0, 1.0], [1.0, 0.0]],
        ],
        dtype=torch.float32,
    )

    rankings = evaluation_module._rank_by_similarity(
        query_ids=["q1", "q2"],
        corpus_ids=["d1", "d2", "d3"],
        query_embeddings=query_embeddings,
        corpus_embeddings=corpus_embeddings,
        score_name="dot",
    )

    assert rankings["q1"] == ["d1", "d3", "d2"]
    assert rankings["q2"] == ["d2", "d1", "d3"]


def test_numpy_late_interaction_rank_by_similarity_uses_maxsim() -> None:
    query_embeddings = np.array(
        [
            [[1.0, 0.0], [0.0, 1.0]],
            [[-1.0, 0.0], [0.0, -1.0]],
        ],
        dtype=np.float32,
    )
    corpus_embeddings = np.array(
        [
            [[1.0, 0.0], [0.0, 1.0]],
            [[-1.0, 0.0], [0.0, -1.0]],
            [[0.0, 1.0], [1.0, 0.0]],
        ],
        dtype=np.float32,
    )

    rankings = evaluation_module._rank_by_similarity(
        query_ids=["q1", "q2"],
        corpus_ids=["d1", "d2", "d3"],
        query_embeddings=query_embeddings,
        corpus_embeddings=corpus_embeddings,
        score_name="dot",
    )

    assert rankings["q1"] == ["d1", "d3", "d2"]
    assert rankings["q2"] == ["d2", "d1", "d3"]


def test_evaluate_dense_task_score_device_cpu_uses_numpy_late_interaction_embeddings() -> None:
    model = FakeCudaLateInteractionModel()

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
        score_device="cpu",
    )

    assert model.query_calls[0]["convert_to_numpy"] is True
    assert model.document_calls[0]["convert_to_numpy"] is True
    assert result.metrics["ToyData_test_dot_ndcg@10"] == pytest.approx(1.0)


@pytest.mark.skipif(not CUDA_TEST_DEVICE_IS_USABLE, reason="CUDA is not available or cannot allocate a test tensor")
def test_cuda_quantized_search_keeps_values_on_cuda() -> None:
    query_embeddings = torch.tensor([[1.0, 0.0]], dtype=torch.float32, device="cuda")
    corpus_embeddings = torch.tensor([[1.0, 0.0], [0.0, 1.0]], dtype=torch.float32, device="cuda")

    cuda_query, cuda_corpus = evaluation_module._quantize_embedding_pair(
        query_embeddings=query_embeddings,
        corpus_embeddings=corpus_embeddings,
        precision="int8",
        target="query_and_corpus",
        algorithm="sentence_transformers_embedding_quantization",
        score_representation="torch_exact",
        search_device="cuda",
    )
    rankings = evaluation_module._rank_by_similarity(
        query_ids=["q1"],
        corpus_ids=["d1", "d2"],
        query_embeddings=cuda_query,
        corpus_embeddings=cuda_corpus,
        score_name="dot",
    )

    assert isinstance(cuda_query.values, torch.Tensor)
    assert isinstance(cuda_corpus.values, torch.Tensor)
    assert cuda_query.values.device.type == "cuda"
    assert cuda_corpus.values.device.type == "cuda"
    assert rankings["q1"] == ["d1", "d2"]
    assert evaluation_module._quantization_metadata(cuda_corpus)["search_device"].startswith("cuda")


def test_torch_rescore_retrieves_top_100_quantized_candidates(monkeypatch) -> None:
    candidate_counts: list[int] = []

    def fake_rescore_torch_quantized_candidates(
        *,
        query_ids,
        corpus_ids,
        candidate_indices,
        query_embeddings,
        corpus_embeddings,
        score_name,
        final_count,
    ):
        _ = query_embeddings, corpus_embeddings, score_name
        candidate_counts.append(int(candidate_indices.shape[1]))
        return {str(query_ids[0]): [str(corpus_id) for corpus_id in corpus_ids[:final_count]]}

    monkeypatch.setattr(
        evaluation_module,
        "_rescore_torch_quantized_candidates",
        fake_rescore_torch_quantized_candidates,
    )
    query_quantized = QuantizedEmbeddingMatrix(
        values=torch.tensor([[127, 127]], dtype=torch.int8),
        precision="int8",
        original_dim=2,
        algorithm="sentence_transformers_embedding_quantization",
        method="query_and_corpus",
        side="query",
        ranges_source="corpus",
        ranges=torch.tensor([[0.0, 0.0], [1.0, 1.0]], dtype=torch.float32),
        rounding="truncate",
        score_representation="torch_exact_rescore",
        source_values=torch.tensor([[1.0, 1.0]], dtype=torch.float32),
    )
    corpus_values = torch.tensor([[127, 127], [0, 0]], dtype=torch.int8).repeat(75, 1)
    corpus_quantized = QuantizedEmbeddingMatrix(
        values=corpus_values,
        precision="int8",
        original_dim=2,
        algorithm="sentence_transformers_embedding_quantization",
        method="query_and_corpus",
        side="corpus",
        ranges_source="corpus",
        ranges=torch.tensor([[0.0, 0.0], [1.0, 1.0]], dtype=torch.float32),
        rounding="truncate",
        score_representation="torch_exact_rescore",
        source_values=corpus_values.to(torch.float32),
    )

    evaluation_module._rank_by_similarity(
        query_ids=["q1"],
        corpus_ids=[f"d{index}" for index in range(150)],
        query_embeddings=query_quantized,
        corpus_embeddings=corpus_quantized,
        score_name="dot",
    )

    assert candidate_counts == [100]
    assert evaluation_module._quantization_metadata(corpus_quantized)["candidate_top_k"] == 100
    assert evaluation_module._quantization_metadata(corpus_quantized)["rescore"] is True


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
            _quantized_variant("int8", "int8"),
            _pipeline_variant("truncate_dim_1_binary", _truncate_step(1), _normalize_step(), _quantized_step("binary")),
        ],
    )

    # This guards the intended low-compute shape: every derived evaluation,
    # including cross variants, must go through the same post-encode pipeline
    # path instead of adding transform-specific branches or extra model encodes.
    assert len(model.query_calls) == 1
    assert len(model.document_calls) == 1
    assert pipeline_calls == [["truncate"], ["normalize", "quantize"], ["truncate", "normalize", "quantize"]]


def test_evaluate_dense_task_requests_tensor_embeddings_for_torch_quantized_variants() -> None:
    model = FakeDenseModel()

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
        embedding_variants=[_quantized_variant("int8", "int8")],
    )

    assert model.query_calls[0]["convert_to_tensor"] is True
    assert model.document_calls[0]["convert_to_tensor"] is True


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


def test_evaluate_dense_task_scores_query_truncate_sparse_max_dims_variants_without_extra_encoding() -> None:
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
            _pipeline_variant("truncate_sparse_query_max_dims_1", _truncate_sparse_max_dims_step(1)),
        ],
    )

    assert len(model.query_calls) == 1
    assert len(model.document_calls) == 1
    variant = result.embedding_evaluations[1]
    assert variant["name"] == "truncate_sparse_query_max_dims_1"
    assert variant["embedding_dimensions"] == {"dim": 4}
    assert variant["embedding_metadata"]["representation_type"] == "sparse"
    assert variant["embedding_metadata"]["query"]["nnz_total"] == 2
    assert variant["embedding_metadata"]["query"]["nnz_max"] == 1
    assert variant["embedding_metadata"]["corpus"]["nnz_total"] == 4
    assert variant["embedding_metadata"]["corpus"]["nnz_max"] == 2
    assert "ToyData_test_dot_truncate_sparse_query_max_dims_1_ndcg@10" in variant["metrics"]


def test_evaluate_dense_task_scores_query_and_docs_truncate_sparse_max_dims_variants() -> None:
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
                "truncate_sparse_query_max_dims_1_truncate_sparse_docs_max_dims_1",
                _truncate_sparse_max_dims_step(1, target="query"),
                _truncate_sparse_max_dims_step(1, target="corpus"),
            ),
        ],
    )

    assert len(model.query_calls) == 1
    assert len(model.document_calls) == 1
    variant = result.embedding_evaluations[1]
    assert variant["name"] == "truncate_sparse_query_max_dims_1_truncate_sparse_docs_max_dims_1"
    assert variant["embedding_metadata"]["query"]["nnz_total"] == 2
    assert variant["embedding_metadata"]["query"]["nnz_max"] == 1
    assert variant["embedding_metadata"]["corpus"]["nnz_total"] == 3
    assert variant["embedding_metadata"]["corpus"]["nnz_max"] == 1


def test_evaluate_dense_task_rejects_quantized_sparse_embedding_variants_after_encoding() -> None:
    model = FakeSentenceTransformersSparseModel()

    with pytest.raises(ValueError, match="not supported for sparse embeddings"):
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
            embedding_variants=[
                _quantized_variant("int8", "int8"),
            ],
        )


def test_evaluate_dense_task_truncates_sparse_active_dims_after_encoding() -> None:
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
        truncate_sparse_query_max_dims=1,
        truncate_sparse_docs_max_dims=1,
    )

    assert model.query_calls[0]["max_active_dims"] is None
    assert model.document_calls[0]["max_active_dims"] is None
    base = result.embedding_evaluations[0]
    assert base["transform"] == {
        "type": "pipeline",
        "steps": [
            _truncate_sparse_max_dims_step(1, target="query"),
            _truncate_sparse_max_dims_step(1, target="corpus"),
        ],
    }
    assert base["embedding_metadata"]["query"]["nnz_total"] == 2
    assert base["embedding_metadata"]["query"]["nnz_max"] == 1
    assert base["embedding_metadata"]["corpus"]["nnz_total"] == 3
    assert base["embedding_metadata"]["corpus"]["nnz_max"] == 1


def test_evaluate_dense_task_keeps_sparse_encoder_outputs_on_device_for_cuda_models() -> None:
    model = FakeCudaSentenceTransformersSparseModel()

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
    )

    assert model.query_calls[0]["save_to_cpu"] is False
    assert model.document_calls[0]["save_to_cpu"] is False


def test_evaluate_dense_task_score_device_cpu_saves_sparse_encoder_outputs_to_cpu() -> None:
    model = FakeCudaSentenceTransformersSparseModel()

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
        score_device="cpu",
    )

    assert model.query_calls[0]["save_to_cpu"] is True
    assert model.document_calls[0]["save_to_cpu"] is True


def test_evaluate_reranker_task_uses_candidate_top_n() -> None:
    result = evaluate_reranker_task(
        model=FakeReranker(),
        dataset=_toy_dataset(),
        batch_size=2,
        show_progress=False,
        rerank_top_n=1,
    )

    assert result.metrics["ToyData_test_reranker_ndcg@10"] == pytest.approx(0.5)


def test_evaluate_reranker_task_supports_rank_api() -> None:
    result = evaluate_reranker_task(
        model=FakeRankReranker(),
        dataset=_toy_dataset(),
        batch_size=2,
        show_progress=False,
        rerank_top_n=2,
    )

    assert result.metrics["ToyData_test_reranker_ndcg@10"] == pytest.approx(1.0)


def test_evaluate_reranker_task_scores_predict_pairs_per_query_before_rank_api() -> None:
    model = FakePredictAndRankReranker()

    result = evaluate_reranker_task(
        model=model,
        dataset=_toy_dataset(),
        batch_size=2,
        show_progress=False,
        rerank_top_n=2,
    )

    assert result.metrics["ToyData_test_reranker_ndcg@10"] == pytest.approx(1.0)
    assert len(model.predict_calls) == 2
    assert model.predict_calls[0]["pairs"] == [
        ["cat query", "other doc"],
        ["cat query", "cat doc"],
    ]
    assert model.predict_calls[1]["pairs"] == [
        ["dog query", "dog doc"],
        ["dog query", "cat doc"],
    ]
    assert model.predict_calls[0]["batch_size"] == 2
    assert model.predict_calls[1]["batch_size"] == 2
    assert model.rank_calls == []


def test_evaluate_reranker_task_preserves_candidate_order_for_predict_ties() -> None:
    result = evaluate_reranker_task(
        model=FakeTiePredictReranker(),
        dataset=_toy_dataset(),
        batch_size=2,
        show_progress=False,
        rerank_top_n=2,
    )

    assert result.top_rankings[0]["rankings"] == {"q1": ["d3", "d1"], "q2": ["d2", "d1"]}


def test_evaluate_reranker_task_supports_callable_api() -> None:
    result = evaluate_reranker_task(
        model=FakeCallableReranker(),
        dataset=_toy_dataset(),
        batch_size=2,
        show_progress=False,
        rerank_top_n=2,
    )

    assert result.metrics["ToyData_test_reranker_ndcg@10"] == pytest.approx(1.0)


def test_evaluate_late_interaction_task_can_score_exact_maxsim() -> None:
    model = FakeLateInteractionModel()

    result = evaluate_late_interaction_task(
        model=model,
        dataset=_toy_dataset(),
        batch_size=2,
        show_progress=False,
        query_prompt=None,
        corpus_prompt="doc: ",
        query_prompt_name="query",
        corpus_prompt_name=None,
        exact_doc_batch_size=2,
        exact_query_batch_size=2,
        device="cpu",
        aggregate_metric="ndcg@10",
    )

    assert result.metrics["ToyData_test_late_interaction_exact_maxsim_ndcg@10"] == pytest.approx(1.0)
    assert model.calls[0]["is_query"] is True
    assert model.calls[0]["prompt_name"] == "query"
    assert model.calls[1]["is_query"] is False
    assert model.calls[1]["prompt"] == "doc: "
    assert result.embedding_conversion["query"]["text_count"] == 2
    assert result.embedding_conversion["docs"]["text_count"] == 3
    base = result.embedding_evaluations[0]
    assert base["best_distance"] == "exact_maxsim"
    assert base["best_score_name"] == "late_interaction_exact_maxsim"
    assert base["embedding_metadata"]["representation_type"] == "late_interaction"
    assert base["embedding_metadata"]["dimension_format"] == "multi_vector"
    assert base["embedding_metadata"]["dimensions"] == {"dim": 2}
    assert base["index"] == {
        "backend": "exact",
        "library": "torch",
        "index_type": "none",
        "ranking_depth": 3,
        "exact_doc_batch_size": 2,
        "exact_query_batch_size": 2,
        "timing": {
            "index_build_or_load_seconds": pytest.approx(0.0),
            "retrieve_seconds": pytest.approx(result.timing["score_and_topk_seconds"]),
        },
    }


def test_evaluate_late_interaction_task_aliases_pylate_renamed_text_length() -> None:
    model = FakeRenamedTextLengthLateInteractionModel()

    result = evaluate_late_interaction_task(
        model=model,
        dataset=_toy_dataset(),
        batch_size=2,
        show_progress=False,
        query_prompt=None,
        corpus_prompt=None,
        query_prompt_name=None,
        corpus_prompt_name=None,
        exact_doc_batch_size=2,
        exact_query_batch_size=2,
        device="cpu",
        aggregate_metric="ndcg@10",
    )

    assert result.metrics["ToyData_test_late_interaction_exact_maxsim_ndcg@10"] == pytest.approx(1.0)
    assert getattr(model, "_text_length")("abc") == 3


def test_evaluate_late_interaction_task_truncates_variants_after_single_encode() -> None:
    model = FakeLateInteractionModel()

    result = evaluate_late_interaction_task(
        model=model,
        dataset=_toy_dataset(),
        batch_size=2,
        show_progress=False,
        query_prompt=None,
        corpus_prompt=None,
        query_prompt_name=None,
        corpus_prompt_name=None,
        exact_doc_batch_size=2,
        exact_query_batch_size=2,
        device="cpu",
        aggregate_metric="ndcg@10",
        embedding_variants=[_pipeline_variant("truncate_dim_1", _truncate_step(1))],
    )

    assert len(model.calls) == 2
    assert [item["name"] for item in result.embedding_evaluations] == ["base", "truncate_dim_1"]
    truncate_eval = result.embedding_evaluations[1]
    assert truncate_eval["embedding_dimensions"] == {"dim": 1}
    assert truncate_eval["embedding_metadata"]["representation_type"] == "late_interaction"
    assert truncate_eval["embedding_metadata"]["dimensions"] == {"dim": 1}
    assert "ToyData_test_late_interaction_exact_maxsim_truncate_dim_1_ndcg@10" in truncate_eval["metrics"]
    assert truncate_eval["reranking_evaluation"]["status"] == "available"
    assert (
        truncate_eval["reranking_evaluation"]["best_score_name"]
        == "late_interaction_exact_maxsim_truncate_dim_1_reranking_hybrid_top2_rerank"
    )


def test_evaluate_late_interaction_task_records_candidate_reranking_metrics() -> None:
    result = evaluate_late_interaction_task(
        model=FakeLateInteractionModel(),
        dataset=_toy_dataset(),
        batch_size=2,
        show_progress=False,
        query_prompt=None,
        corpus_prompt=None,
        query_prompt_name=None,
        corpus_prompt_name=None,
        exact_doc_batch_size=2,
        exact_query_batch_size=2,
        device="cpu",
        aggregate_metric="ndcg@10",
        rerank_top_n=1,
        candidate_ranking_name="bm25",
    )

    assert result.metrics["ToyData_test_late_interaction_exact_maxsim_ndcg@10"] == pytest.approx(1.0)
    assert result.rerank_aggregate_metric_value == pytest.approx(0.5)
    assert result.reranking_evaluations[0]["status"] == "available"
    assert result.reranking_evaluations[0]["rerank_top_n"] == 1
    assert result.reranking_evaluations[0]["aggregate_metric_value"] == pytest.approx(0.5)
    assert result.reranking_evaluations[0]["best_score_name"] == "late_interaction_exact_maxsim_bm25_top1_rerank"
    assert result.reranking_evaluations[0]["candidate_coverage"] == {
        "top_k": 1,
        "query_count": 2,
        "query_with_relevance_count": 2,
        "covered_query_count": 1,
        "query_coverage": 0.5,
        "relevant_count": 2,
        "covered_relevant_count": 1,
        "relevant_coverage": 0.5,
    }
    assert (
        result.rerank_metrics["ToyData_test_late_interaction_exact_maxsim_bm25_top1_rerank_ndcg@10"]
        == pytest.approx(0.5)
    )
    assert (
        result.rerank_metrics["ToyData_test_late_interaction_exact_maxsim_bm25_top1_rerank_acc@100"]
        == pytest.approx(0.5)
    )
    assert result.embedding_evaluations[0]["reranking_evaluation"]["status"] == "available"
    assert any(ranking["ranking_kind"] == "candidate_rerank" for ranking in result.top_rankings)


def test_evaluate_late_interaction_task_skips_candidate_reranking_without_candidates() -> None:
    result = evaluate_late_interaction_task(
        model=FakeLateInteractionModel(),
        dataset=_toy_dataset_without_candidates(),
        batch_size=2,
        show_progress=False,
        query_prompt=None,
        corpus_prompt=None,
        query_prompt_name=None,
        corpus_prompt_name=None,
        exact_doc_batch_size=2,
        exact_query_batch_size=2,
        device="cpu",
        aggregate_metric="ndcg@10",
        rerank_top_n=100,
        candidate_ranking_name="bm25",
    )

    assert result.rerank_metrics == {}
    assert result.rerank_aggregate_metric_value is None
    assert result.reranking_evaluations == [
        {
            "name": "bm25_top_100",
            "source": "dataset_candidate_subset",
            "status": "skipped",
            "reason": "candidate_subset_unavailable",
            "rerank_top_n": 100,
        }
    ]


def test_evaluate_dense_task_records_bm25_top_n_reranking_metrics() -> None:
    result = evaluate_dense_task(
        model=FakeDenseModel(),
        dataset=_toy_dataset(),
        batch_size=2,
        show_progress=False,
        query_prompt=None,
        corpus_prompt=None,
        query_prompt_name=None,
        corpus_prompt_name=None,
        truncate_dim=None,
        rerank_top_n=1,
        candidate_ranking_name="bm25",
    )

    assert result.metrics["ToyData_test_dot_ndcg@10"] == pytest.approx(1.0)
    assert result.rerank_aggregate_metric_value == pytest.approx(0.5)
    assert result.reranking_evaluations[0]["status"] == "available"
    assert result.reranking_evaluations[0]["rerank_top_n"] == 1
    assert result.reranking_evaluations[0]["aggregate_metric_value"] == pytest.approx(0.5)
    assert result.reranking_evaluations[0]["best_score_name"] == "dot_bm25_top1_rerank"
    assert result.reranking_evaluations[0]["candidate_coverage"] == {
        "top_k": 1,
        "query_count": 2,
        "query_with_relevance_count": 2,
        "covered_query_count": 1,
        "query_coverage": 0.5,
        "relevant_count": 2,
        "covered_relevant_count": 1,
        "relevant_coverage": 0.5,
    }
    assert result.rerank_metrics["ToyData_test_dot_bm25_top1_rerank_ndcg@10"] == pytest.approx(0.5)
    assert result.rerank_metrics["ToyData_test_dot_bm25_top1_rerank_acc@100"] == pytest.approx(0.5)


def test_evaluate_dense_task_skips_bm25_reranking_without_candidates() -> None:
    result = evaluate_dense_task(
        model=FakeDenseModel(),
        dataset=_toy_dataset_without_candidates(),
        batch_size=2,
        show_progress=False,
        query_prompt=None,
        corpus_prompt=None,
        query_prompt_name=None,
        corpus_prompt_name=None,
        truncate_dim=None,
        rerank_top_n=100,
        candidate_ranking_name="bm25",
    )

    assert result.metrics["ToyData_test_dot_ndcg@10"] == pytest.approx(1.0)
    assert result.rerank_metrics == {}
    assert result.rerank_aggregate_metric_value is None
    assert result.reranking_evaluations == [
        {
            "name": "bm25_top_100",
            "source": "dataset_candidate_subset",
            "status": "skipped",
            "reason": "candidate_subset_unavailable",
            "rerank_top_n": 100,
        }
    ]


def test_result_path_layout() -> None:
    path = result_path_for_task(
        output_dir=Path("output/results"),
        model_id="local/bekko-model",
        task=_toy_task(),
    )

    assert path == Path("output/results/local__bekko-model/toy__data/test.json")
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
    output_path = result_path_for_task(output_dir=tmp_path, model_id=args.model, task=task)
    output_path.parent.mkdir(parents=True)
    output_path.write_text(json.dumps({"metrics": {"cached": 1.0}}), encoding="utf-8")

    result = run_or_load_task(
        task=task,
        model=FakeDenseModel(),
        args=args,
        environment={"package_versions": {}},
        model_metadata={"id": "hotchpotch/model"},
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
        model_metadata={"id": "hotchpotch/model"},
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
        "hakari_bench.results.resolve_dataset_revision",
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
        model_metadata={"id": "hotchpotch/model"},
        dataset_loader=lambda _: _toy_dataset(),
    )

    assert result.payload["target"]["dataset_revision"] == {
        "requested": "main",
        "resolved": "toy/data@sha",
        "source": "huggingface_hub",
    }
    manifest = result.payload["experiment_manifest"]
    assert manifest["schema_version"] == 2
    assert set(manifest) == {"schema_version", "fingerprint_sha256"}
    assert len(manifest["fingerprint_sha256"]) == 64


def test_run_or_load_task_records_task_metadata(tmp_path: Path) -> None:
    spec = NanoDatasetSpec(
        name="ToyData",
        dataset_id="toy/data",
        metadata={
            "language": "en",
            "category": "natural_language",
            "short_description": "Toy dataset.",
            "description": "Toy dataset metadata.",
        },
        task_metadata={
            "test": {
                "language": "en",
                "category": "natural_language",
                "short_description": "Toy task.",
                "description": "Toy task metadata.",
                "citation_keys": ["toy2024"],
            }
        },
    )
    task = EvalTask(dataset=spec, split_name="test", task_name="test")
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
        model_metadata={"id": "hotchpotch/model"},
        dataset_loader=lambda _: _toy_dataset(),
    )

    assert "metadata" not in result.payload["target"]


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
        model_metadata={"id": "hotchpotch/model"},
        dataset_loader=lambda _: _toy_dataset(),
    )

    assert "embedding_variants" not in result.payload["config"]
    embedding_evaluations = result.payload["evaluation"]["embedding_evaluations"]
    assert [item["name"] for item in embedding_evaluations] == ["base", "truncate_dim_1"]
    assert embedding_evaluations[1]["aggregate_metric"] == "ndcg@10"
    assert embedding_evaluations[1]["aggregate_metric_value"] < 1.0
    assert embedding_evaluations[1]["best_distance"] in {"dot", "cosine"}
    assert [item["distance"] for item in embedding_evaluations[1]["distance_evaluations"]] == ["dot", "cosine"]
    assert "metrics" not in embedding_evaluations[0]
    assert set(result.payload["metrics"]) == {"ToyData_test_dot_ndcg@10", "ToyData_test_dot_acc@100"}

    run_summary_payload = build_run_summary_payload(
        args=args,
        environment={"package_versions": {}},
        model_metadata={"id": "hotchpotch/model"},
        results=[result],
    )
    split_variants = run_summary_payload["splits"][0]["embedding_evaluations"]
    assert [item["name"] for item in split_variants] == ["base", "truncate_dim_1"]
    assert split_variants[0]["embedding_dimensions"] == {"dim": 2}
    assert split_variants[0]["embedding_metadata"]["representation_type"] == "dense"
    assert split_variants[0]["best_distance"] == "dot"
    assert [item["distance"] for item in split_variants[0]["distance_evaluations"]] == ["dot", "cosine"]
    assert "metrics" not in split_variants[0]["distance_evaluations"][0]
    assert split_variants[1]["embedding_dimensions"] == {"dim": 1}
    assert "metrics" not in split_variants[1]


def test_run_or_load_task_records_embedding_model_reranking_evaluations(tmp_path: Path) -> None:
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
        embedding_variants=[],
        candidate_subset_name="bm25",
        rerank_top_n=1,
        aggregate_metric="ndcg@10",
        override=False,
    )

    result = run_or_load_task(
        task=task,
        model=FakeDenseModel(),
        args=args,
        environment={"package_versions": {}},
        model_metadata={"id": "hotchpotch/model"},
        dataset_loader=lambda _: _toy_dataset(),
    )

    evaluation = result.payload["evaluation"]
    assert evaluation["aggregate_metric_value"] == pytest.approx(1.0)
    assert evaluation["rerank_aggregate_metric_value"] == pytest.approx(0.5)
    assert evaluation["reranking_evaluations"][0]["best_score_name"] == "dot_bm25_top1_rerank"
    assert result.payload["rerank_metrics"]["ToyData_test_dot_bm25_top1_rerank_ndcg@10"] == pytest.approx(0.5)
    assert result.payload["config"]["candidate_ranking"] == "bm25"
    assert result.payload["config"]["rerank_top_k"] == 1

    run_summary_payload = build_run_summary_payload(
        args=args,
        environment={"package_versions": {}},
        model_metadata={"id": "hotchpotch/model"},
        results=[result],
    )

    assert run_summary_payload["totals"]["aggregate_metric_mean"] == pytest.approx(1.0)
    assert run_summary_payload["totals"]["rerank_aggregate_metric_mean"] == pytest.approx(0.5)
    assert run_summary_payload["splits"][0]["rerank_aggregate_metric_value"] == pytest.approx(0.5)
    assert run_summary_payload["splits"][0]["reranking_evaluations"][0]["status"] == "available"
    assert "metrics" not in run_summary_payload["splits"][0]["reranking_evaluations"][0]["distance_evaluations"][0]


def test_run_or_load_task_records_late_interaction_reranking_evaluations(tmp_path: Path) -> None:
    task = _toy_task()
    args = argparse.Namespace(
        output_dir=str(tmp_path),
        model="hotchpotch/colbert-model",
        model_type="late-interaction",
        batch_size=2,
        show_progress=False,
        query_prompt=None,
        corpus_prompt=None,
        query_prompt_name=None,
        corpus_prompt_name=None,
        query_task=None,
        corpus_task=None,
        truncate_dim=None,
        embedding_variants=[],
        candidate_subset_name="bm25",
        rerank_top_n=1,
        aggregate_metric="ndcg@10",
        late_interaction_query_length=None,
        late_interaction_document_length=None,
        late_interaction_query_prefix=None,
        late_interaction_document_prefix=None,
        late_interaction_attend_to_expansion_tokens=None,
        late_interaction_exact_doc_batch_size=2,
        late_interaction_exact_query_batch_size=2,
        device="cpu",
        override=False,
    )

    result = run_or_load_task(
        task=task,
        model=FakeLateInteractionModel(),
        args=args,
        environment={"package_versions": {}},
        model_metadata={"id": "hotchpotch/colbert-model", "method": "late-interaction"},
        dataset_loader=lambda _: _toy_dataset(),
    )

    evaluation = result.payload["evaluation"]
    assert evaluation["aggregate_metric_value"] == pytest.approx(1.0)
    assert evaluation["rerank_aggregate_metric_value"] == pytest.approx(0.5)
    assert (
        evaluation["reranking_evaluations"][0]["best_score_name"]
        == "late_interaction_exact_maxsim_bm25_top1_rerank"
    )
    assert (
        result.payload["rerank_metrics"]["ToyData_test_late_interaction_exact_maxsim_bm25_top1_rerank_ndcg@10"]
        == pytest.approx(0.5)
    )
    assert result.payload["config"]["candidate_ranking"] == "bm25"
    assert result.payload["config"]["rerank_top_k"] == 1
    assert result.payload["evaluation"]["timing"]["reranking_score_and_topk_seconds"] >= 0.0

    run_summary_payload = build_run_summary_payload(
        args=args,
        environment={"package_versions": {}},
        model_metadata={"id": "hotchpotch/colbert-model", "method": "late-interaction"},
        results=[result],
    )

    assert run_summary_payload["totals"]["rerank_aggregate_metric_mean"] == pytest.approx(0.5)
    assert run_summary_payload["splits"][0]["reranking_evaluations"][0]["status"] == "available"


def test_run_or_load_task_defaults_to_all_available_rerank_candidates(tmp_path: Path) -> None:
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
        embedding_variants=[],
        candidate_subset_name="bm25",
        rerank_top_n=None,
        aggregate_metric="ndcg@10",
        override=False,
    )

    result = run_or_load_task(
        task=task,
        model=FakeDenseModel(),
        args=args,
        environment={"package_versions": {}},
        model_metadata={"id": "hotchpotch/model"},
        dataset_loader=lambda _: _toy_dataset(),
    )

    reranking = result.payload["evaluation"]["reranking_evaluations"][0]
    assert result.payload["config"]["rerank_top_k"] is None
    assert reranking["name"] == "bm25_top_2"
    assert reranking["rerank_top_n"] == 2
    assert reranking["candidate_coverage"]["top_k"] == 2
    assert reranking["best_score_name"] == "dot_bm25_top2_rerank"


def test_run_or_load_task_embeds_top100_rankings_in_task_json(tmp_path: Path) -> None:
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
        embedding_variants=[],
        candidate_subset_name="bm25",
        rerank_top_n=1,
        aggregate_metric="ndcg@10",
        override=False,
    )

    result = run_or_load_task(
        task=task,
        model=FakeDenseModel(),
        args=args,
        environment={"package_versions": {}},
        model_metadata={"id": "hotchpotch/model"},
        dataset_loader=lambda _: _toy_dataset(),
    )

    artifact = result.payload["artifacts"]["top_rankings"]

    assert artifact["top_k"] == 100
    assert "path" not in artifact
    assert artifact["schema_version"] == 2
    assert artifact["target"]["task_name"] == "test"
    assert artifact["qrels"] == [
        {"query_id": "q1", "relevant_corpus_ids": ["d1"]},
        {"query_id": "q2", "relevant_corpus_ids": ["d2"]},
    ]
    assert artifact["rankings"][0] == {
        "name": "base",
        "ranking_kind": "retrieval",
        "embedding_variant_name": None,
        "distance": "dot",
        "score_name": "dot",
        "query_id": "q1",
        "corpus_ids": ["d1", "d2", "d3"],
    }
    assert {
        "name": "base",
        "ranking_kind": "candidate_rerank",
        "embedding_variant_name": None,
        "distance": "dot",
        "score_name": "dot_bm25_top1_rerank",
        "query_id": "q1",
        "corpus_ids": ["d3"],
    } in artifact["rankings"]
    assert "metadata" not in result.payload["target"]
    assert "embedding_variants" not in result.payload["config"]
    assert result.payload["experiment_manifest"] == {
        "schema_version": 2,
        "fingerprint_sha256": result.payload["experiment_manifest"]["fingerprint_sha256"],
    }
    base_eval = result.payload["evaluation"]["embedding_evaluations"][0]
    assert "metrics" not in base_eval
    assert "metrics" not in base_eval["distance_evaluations"][0]
    assert "metrics" not in base_eval["reranking_evaluation"]
    assert "metrics" not in base_eval["reranking_evaluation"]["distance_evaluations"][0]
    assert set(result.payload["metrics"]) == {"ToyData_test_dot_ndcg@10", "ToyData_test_dot_acc@100"}


def test_run_or_load_task_embeds_top100_rankings_by_default_and_removes_stale_sidecar(tmp_path: Path) -> None:
    task = _toy_task()
    stale_path = tmp_path / "hotchpotch__model" / "toy__data" / "rankings" / "test.top100.json"
    stale_path.parent.mkdir(parents=True)
    stale_path.write_text("stale", encoding="utf-8")
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
        embedding_variants=[],
        candidate_subset_name="bm25",
        rerank_top_n=1,
        aggregate_metric="ndcg@10",
        override=True,
    )

    result = run_or_load_task(
        task=task,
        model=FakeDenseModel(),
        args=args,
        environment={"package_versions": {}},
        model_metadata={"id": "hotchpotch/model"},
        dataset_loader=lambda _: _toy_dataset(),
    )

    assert result.payload["artifacts"]["top_rankings"]["schema_version"] == 2
    assert "rankings" in result.payload["artifacts"]["top_rankings"]
    assert not stale_path.exists()


def test_run_or_load_task_records_score_device(tmp_path: Path) -> None:
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
        truncate_sparse_query_max_dims=None,
        truncate_sparse_docs_max_dims=None,
        embedding_variants=[],
        candidate_subset_name="bm25",
        rerank_top_n=100,
        aggregate_metric="ndcg@10",
        score_device="cpu",
        override=False,
    )

    result = run_or_load_task(
        task=task,
        model=FakeCudaDenseModel(),
        args=args,
        environment={"package_versions": {}},
        model_metadata={"id": "hotchpotch/model"},
        dataset_loader=lambda _: _toy_dataset(),
    )

    assert result.payload["config"]["retrieval_score_device"] == "cpu"
    base_metadata = result.payload["evaluation"]["embedding_evaluations"][0]["embedding_metadata"]
    assert "device" not in base_metadata["query"]


def test_evaluate_dense_task_uses_sentence_transformer_multi_process_pool() -> None:
    model = FakeMultiProcessDenseModel()

    result = evaluate_dense_task(
        model=model,
        dataset=_toy_dataset(),
        batch_size=2,
        show_progress=False,
        query_prompt=None,
        corpus_prompt=None,
        query_prompt_name=None,
        corpus_prompt_name=None,
        embedding_variants=[],
        score_device="cpu",
        rerank_top_n=100,
        encode_devices=["cuda:0", "cuda:1"],
        encode_chunk_size=16,
    )

    assert result.metrics["ToyData_test_dot_ndcg@10"] == pytest.approx(1.0)
    assert model.started_devices == ["cuda:0", "cuda:1"]
    assert model.stopped_pool == {"target_devices": ["cuda:0", "cuda:1"], "processes": []}
    assert model.query_calls[0]["pool"] is model.stopped_pool
    assert model.document_calls[0]["pool"] is model.stopped_pool
    assert model.query_calls[0]["chunk_size"] == 16
    assert model.document_calls[0]["chunk_size"] == 16


def test_evaluate_dense_task_reuses_supplied_sentence_transformer_multi_process_pool() -> None:
    model = FakeMultiProcessDenseModel()
    pool = {"target_devices": ["cuda:0", "cuda:1"], "processes": []}

    result = evaluate_dense_task(
        model=model,
        dataset=_toy_dataset(),
        batch_size=2,
        show_progress=False,
        query_prompt=None,
        corpus_prompt=None,
        query_prompt_name=None,
        corpus_prompt_name=None,
        embedding_variants=[],
        score_device="cpu",
        rerank_top_n=100,
        encode_pool=pool,
        encode_chunk_size=16,
    )

    assert result.metrics["ToyData_test_dot_ndcg@10"] == pytest.approx(1.0)
    assert model.started_devices is None
    assert model.stopped_pool is None
    assert model.query_calls[0]["pool"] is pool
    assert model.document_calls[0]["pool"] is pool


def test_run_or_load_task_records_encode_devices(tmp_path: Path) -> None:
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
        truncate_sparse_query_max_dims=None,
        truncate_sparse_docs_max_dims=None,
        embedding_variants=[],
        candidate_subset_name="bm25",
        rerank_top_n=100,
        aggregate_metric="ndcg@10",
        score_device="cpu",
        encode_devices=["cuda:0", "cuda:1"],
        encode_chunk_size=16,
        override=False,
    )

    result = run_or_load_task(
        task=task,
        model=FakeMultiProcessDenseModel(),
        args=args,
        environment={"package_versions": {}},
        model_metadata={"id": "hotchpotch/model"},
        dataset_loader=lambda _: _toy_dataset(),
    )

    assert result.payload["config"]["encode_devices"] == ["cuda:0", "cuda:1"]
    assert result.payload["config"]["encode_chunk_size"] == 16


def test_run_or_load_task_records_truncate_sparse_max_dims(tmp_path: Path) -> None:
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
        truncate_sparse_query_max_dims=32,
        truncate_sparse_docs_max_dims=128,
        embedding_variants=[],
        candidate_subset_name="bm25",
        rerank_top_n=100,
        aggregate_metric="ndcg@10",
        score_device="auto",
        override=False,
    )
    model = FakeSentenceTransformersSparseModel()

    result = run_or_load_task(
        task=task,
        model=model,
        args=args,
        environment={"package_versions": {}},
        model_metadata={"id": "naver/splade-v3"},
        dataset_loader=lambda _: _toy_dataset(),
    )

    assert model.query_calls[0]["max_active_dims"] is None
    assert model.document_calls[0]["max_active_dims"] is None
    assert result.payload["config"]["sparse_query_max_active_dims"] == 32
    assert result.payload["config"]["sparse_document_max_active_dims"] == 128
    assert result.payload["config"]["sparse_truncation"] == {
        "algorithm": "top_abs_values_per_row",
        "query_max_active_dims": 32,
        "document_max_active_dims": 128,
        "source": "post_encode_pipeline",
    }

    run_summary_payload = build_run_summary_payload(
        args=args,
        environment={"package_versions": {}},
        model_metadata={"id": "naver/splade-v3"},
        results=[result],
    )
    assert run_summary_payload["config"]["sparse_query_max_active_dims"] == 32
    assert run_summary_payload["config"]["sparse_document_max_active_dims"] == 128
    assert run_summary_payload["config"]["sparse_truncation"] == {
        "algorithm": "top_abs_values_per_row",
        "query_max_active_dims": 32,
        "document_max_active_dims": 128,
        "source": "post_encode_pipeline",
    }
    assert run_summary_payload["splits"][0]["config"]["sparse_query_max_active_dims"] == 32
    assert run_summary_payload["splits"][0]["config"]["sparse_document_max_active_dims"] == 128


def test_build_run_summary_payload_includes_split_and_total_durations(tmp_path: Path) -> None:
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
        model_metadata={"id": "hotchpotch/model"},
        dataset_loader=lambda _: _toy_dataset(),
    )

    payload = build_run_summary_payload(
        args=args,
        environment={"package_versions": {}},
        model_metadata={"id": "hotchpotch/model"},
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


def test_build_run_summary_payload_aggregates_prompt_config_from_cached_splits(tmp_path: Path) -> None:
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
            "primary_metric": "ndcg@10",
            "query_prompt": "検索クエリ: ",
            "document_prompt": "検索文書: ",
            "query_prompt_name": None,
            "document_prompt_name": None,
            "query_encode_task": None,
            "document_encode_task": None,
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

    payload = build_run_summary_payload(
        args=args,
        environment={"package_versions": {}},
        model_metadata={"id": "cl-nagoya/ruri-v3-30m"},
        results=[result],
    )

    assert payload["cli_args"]["query_prompt"] is None
    assert payload["config"]["query_prompt"] == "検索クエリ: "
    assert payload["config"]["document_prompt"] == "検索文書: "
    assert payload["config"]["batch_size"] == 4
    assert payload["config"]["prompt_summary"]["query_prompt"] == {
        "consistent": True,
        "value": "検索クエリ: ",
        "values": [{"value": "検索クエリ: ", "count": 1}],
    }
    assert payload["splits"][0]["config"]["query_prompt"] == "検索クエリ: "
    assert payload["splits"][0]["config"]["document_prompt"] == "検索文書: "


def test_build_run_summary_payload_uses_task_model_metadata_when_consistent(tmp_path: Path) -> None:
    task = _toy_task()
    args = argparse.Namespace(
        output_dir=str(tmp_path),
        model="bm25/dataset-bm25",
        model_type="bm25",
        batch_size=2,
        show_progress=False,
        query_prompt=None,
        corpus_prompt=None,
        query_prompt_name=None,
        corpus_prompt_name=None,
        truncate_dim=None,
        candidate_subset_name="bm25",
        bm25_source="dataset",
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
        model_metadata={"id": "stale"},
        dataset_loader=lambda _: _toy_dataset(),
    )

    payload = build_run_summary_payload(
        args=args,
        environment={"package_versions": {}},
        model_metadata={"id": "stale"},
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
        bm25_source="computed",
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
        "hakari_bench.bm25._detect_language",
        lambda _: {"lang": "en", "score": 0.99},
    )

    result = run_or_load_task(
        task=task,
        model=None,
        args=args,
        environment={"package_versions": {}},
        model_metadata={"id": "bm25/bm25s-okapi-auto"},
        dataset_loader=lambda _: _toy_dataset_without_candidates(),
    )

    assert result.payload["config"]["bm25"]["algorithm"] == "okapi"
    assert result.payload["config"]["bm25"]["tokenizer"] == "english_porter_stop"
    assert result.payload["config"]["bm25"]["auto_selected"] is True
    assert result.payload["config"]["bm25"]["auto_detected_language"] == "en"
    assert result.payload["model"]["bm25"]["tokenizer"] == "english_porter_stop"


def test_run_or_load_task_records_bm25_candidate_subset_source(tmp_path: Path) -> None:
    task = _toy_task()
    args = argparse.Namespace(
        output_dir=str(tmp_path),
        model="bm25/dataset-bm25",
        model_type="bm25",
        batch_size=2,
        show_progress=False,
        query_prompt=None,
        corpus_prompt=None,
        query_prompt_name=None,
        corpus_prompt_name=None,
        truncate_dim=None,
        candidate_subset_name="bm25",
        bm25_source="dataset",
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
        model_metadata={"id": "bm25/bm25s-okapi-auto"},
        dataset_loader=lambda _: _toy_dataset(),
    )

    assert result.payload["config"]["candidate_ranking"] == "bm25"
    assert result.payload["config"]["bm25"]["source"] == "dataset_candidate_subset"
    assert result.payload["config"]["bm25"]["candidate_ranking"] == "bm25"
    assert result.payload["model"]["bm25"]["source"] == "dataset_candidate_subset"
    assert result.payload["evaluation"]["aggregate_metric_value"] == pytest.approx(0.5)


def test_run_or_load_task_requires_dataset_bm25_source_candidates(tmp_path: Path) -> None:
    task = _toy_task()
    args = argparse.Namespace(
        output_dir=str(tmp_path),
        model="bm25/dataset-bm25",
        model_type="bm25",
        batch_size=2,
        show_progress=False,
        query_prompt=None,
        corpus_prompt=None,
        query_prompt_name=None,
        corpus_prompt_name=None,
        truncate_dim=None,
        candidate_subset_name="bm25",
        bm25_source="dataset",
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

    with pytest.raises(ValueError, match="--bm25-source computed"):
        run_or_load_task(
            task=task,
            model=None,
            args=args,
            environment={"package_versions": {}},
            model_metadata={"id": "bm25/dataset-bm25"},
            dataset_loader=lambda _: _toy_dataset_without_candidates(),
        )
