from __future__ import annotations

import argparse
import json
from pathlib import Path

import numpy as np
import pytest
from scipy import sparse

from nano_ir_benchmark.datasets import EvalTask, NanoDatasetSpec
from nano_ir_benchmark.evaluation import LoadedIrDataset, evaluate_dense_task, evaluate_reranker_task
from nano_ir_benchmark.results import build_all_payload, result_path_for_task, run_or_load_task, safe_path_part


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
        embedding_variants=[
            {
                "name": "truncate_dim_1",
                "transform": {
                    "type": "truncate",
                    "algorithm": "dimension_slice",
                    "parameters": {"dim": 1},
                },
            }
        ],
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
    assert result.embedding_evaluations[1]["name"] == "truncate_dim_1"
    assert result.embedding_evaluations[1]["transform"]["parameters"] == {"dim": 1}
    assert result.embedding_evaluations[1]["embedding_dimensions"] == {"dim": 1}
    assert result.embedding_evaluations[1]["embedding_metadata"]["dimensions"] == {"dim": 1}
    assert result.embedding_evaluations[1]["aggregate_metric_value"] < 1.0
    assert "ToyData_test_dot_truncate_dim_1_ndcg@10" in result.embedding_evaluations[1]["metrics"]


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
    assert base["embedding_metadata"]["query"]["density"] == pytest.approx(3 / 8)
    assert base["embedding_metadata"]["corpus"]["shape"] == [3, 4]
    assert base["embedding_metadata"]["corpus"]["nnz_total"] == 4
    assert base["embedding_metadata"]["corpus"]["nnz_max"] == 2


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
        embedding_variants=[
            {
                "name": "truncate_dim_1",
                "transform": {
                    "type": "truncate",
                    "algorithm": "dimension_slice",
                    "parameters": {"dim": 1},
                },
            }
        ],
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
    assert split_variants[1]["embedding_dimensions"] == {"dim": 1}
    assert "metrics" not in split_variants[1]


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
    assert payload["totals"]["duration_seconds_including_dataset_load_this_run"] == pytest.approx(
        result.payload["evaluation"]["duration_seconds_including_dataset_load"]
    )


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
