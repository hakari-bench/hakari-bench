from __future__ import annotations

import numpy as np

from hakari_bench.datasets import EvalTask, NanoDatasetSpec
from hakari_bench.evaluation import LoadedIrDataset
from hakari_bench.sentence_transformers import (
    HakariNanoBM25Evaluator,
    HakariNanoEmbeddingEvaluator,
    HakariNanoRerankerEvaluator,
    HakariNanoTarget,
    resolve_hakari_nano_targets,
    sample_ir_dataset,
)


def _toy_dataset() -> LoadedIrDataset:
    return LoadedIrDataset(
        queries={"q1": "cat query", "q2": "dog query", "q3": "bird query"},
        corpus={
            "d1": "cat document",
            "d2": "dog document",
            "d3": "bird document",
            "d4": "candidate distractor",
            "d5": "unused document",
        },
        qrels={"q1": {"d1"}, "q2": {"d2"}, "q3": {"d3"}},
        candidates={"q1": ["d4", "d1"], "q2": ["d2", "d4"], "q3": ["d3", "d4"]},
        evaluator_name="ToyData_test",
    )


class FakeDenseModel:
    similarity_fn_name = "dot"

    def encode_query(self, sentences: list[str], **_: object) -> np.ndarray:
        vectors = {
            "cat query": [1.0, 0.0, 0.0],
            "dog query": [0.0, 1.0, 0.0],
            "bird query": [0.0, 0.0, 1.0],
        }
        return np.asarray([vectors[sentence] for sentence in sentences], dtype=np.float32)

    def encode_document(self, sentences: list[str], **_: object) -> np.ndarray:
        vectors = {
            "cat document": [1.0, 0.0, 0.0],
            "dog document": [0.0, 1.0, 0.0],
            "bird document": [0.0, 0.0, 1.0],
            "candidate distractor": [-1.0, 0.0, 0.0],
            "unused document": [0.0, -1.0, 0.0],
        }
        return np.asarray([vectors[sentence] for sentence in sentences], dtype=np.float32)


class FakeReranker:
    def predict(self, pairs: list[tuple[str, str]], **_: object) -> list[float]:
        return [1.0 if "document" in document and query.split()[0] in document else 0.0 for query, document in pairs]


def test_resolve_hakari_nano_targets_supports_per_dataset_splits() -> None:
    tasks = resolve_hakari_nano_targets(
        [
            HakariNanoTarget(dataset="NanoMIRACL", splits=["en"]),
            HakariNanoTarget(dataset="NanoCoIR"),
            HakariNanoTarget(dataset="NanoMMTEB-v2"),
        ]
    )

    assert tasks[0].dataset_name == "NanoMIRACL"
    assert tasks[0].split_name == "en"
    assert tasks[0].task_name == "en"
    assert sum(1 for task in tasks if task.dataset_name == "NanoCoIR") == 10
    assert sum(1 for task in tasks if task.dataset_name == "NanoMMTEB-v2") == 18


def test_sample_ir_dataset_is_deterministic_and_can_reduce_corpus_to_sampled_candidates() -> None:
    dataset = _toy_dataset()

    sampled = sample_ir_dataset(
        dataset,
        query_limit=2,
        query_sample_seed=7,
        corpus_policy="sampled_candidates",
    )
    sampled_again = sample_ir_dataset(
        dataset,
        query_limit=2,
        query_sample_seed=7,
        corpus_policy="sampled_candidates",
    )

    assert sampled.queries == sampled_again.queries
    assert len(sampled.queries) == 2
    assert set(sampled.qrels) == set(sampled.queries)
    assert set(sampled.candidates or {}) == set(sampled.queries)
    expected_doc_ids = set().union(*sampled.qrels.values(), *(sampled.candidates or {}).values())
    assert set(sampled.corpus) == expected_doc_ids


def test_embedding_evaluator_returns_st_compatible_metrics(monkeypatch) -> None:
    task = _toy_task()
    monkeypatch.setattr(
        "hakari_bench.sentence_transformers.evaluators.load_ir_dataset",
        lambda *_args, **_kwargs: _toy_dataset(),
    )

    evaluator = HakariNanoEmbeddingEvaluator(
        targets=[HakariNanoTarget(dataset="ToyData", tasks=[task])],
        batch_size=2,
        query_limit=2,
        query_sample_seed=3,
    )

    results = evaluator(FakeDenseModel())

    assert evaluator.primary_metric == "HakariNano_mean_ndcg@10"
    assert results[evaluator.primary_metric] == 1.0
    assert any(key.startswith("ToyData_test_") for key in results)


def test_reranker_evaluator_uses_bm25_candidates(monkeypatch) -> None:
    task = _toy_task()
    monkeypatch.setattr(
        "hakari_bench.sentence_transformers.evaluators.load_ir_dataset",
        lambda *_args, **_kwargs: _toy_dataset(),
    )

    evaluator = HakariNanoRerankerEvaluator(
        targets=[HakariNanoTarget(dataset="ToyData", tasks=[task])],
        batch_size=2,
        rerank_top_k=2,
    )

    results = evaluator(FakeReranker())

    assert evaluator.primary_metric == "HakariNano_R2_mean_ndcg@10"
    assert results[evaluator.primary_metric] == 1.0


def test_bm25_evaluator_runs_without_model(monkeypatch) -> None:
    task = _toy_task()
    monkeypatch.setattr(
        "hakari_bench.sentence_transformers.evaluators.load_ir_dataset",
        lambda *_args, **_kwargs: _toy_dataset(),
    )

    evaluator = HakariNanoBM25Evaluator(
        targets=[HakariNanoTarget(dataset="ToyData", tasks=[task])],
        bm25_source="dataset",
        bm25_top_k=2,
    )

    results = evaluator()

    assert evaluator.primary_metric == "HakariNanoBM25_mean_ndcg@10"
    assert 0.0 < results[evaluator.primary_metric] <= 1.0


def _toy_task() -> EvalTask:
    dataset = NanoDatasetSpec(
        name="ToyData",
        dataset_id="toy/data",
        corpus_config="corpus",
        queries_config="queries",
        qrels_config="qrels",
        candidate_config="bm25",
        splits=["test"],
    )
    return EvalTask(dataset=dataset, split_name="test", task_name="test")
