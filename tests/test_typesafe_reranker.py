from __future__ import annotations

import json
import math
import threading
from pathlib import Path
from types import SimpleNamespace
from typing import Any

import pytest

from hakari_bench.cli import parse_args, _warn_if_missing_attention_implementation
from hakari_bench.evaluation import LoadedIrDataset, evaluate_reranker_task
from hakari_bench.datasets import EvalTask, NanoDatasetSpec
from hakari_bench.models import ModelLoadConfig, TypeSafeRerankerAdapter, collect_model_metadata, load_model
from hakari_bench.results import read_result_json, run_or_load_task


class FakeHttp:
    def __init__(self, *, scores: dict[str, float] | None = None, status: int = 200) -> None:
        self.calls: list[dict[str, Any]] = []
        self.scores = scores or {}
        self.status = status

    def request(self, method: str, url: str, **kwargs: Any) -> Any:
        payload = json.loads(kwargs["body"])
        self.calls.append({"method": method, "url": url, "payload": payload, **kwargs})
        state = payload["state"]
        documents = state.get("documents", {"relevant": state.get("document")})
        return SimpleNamespace(
            status=self.status,
            data=json.dumps({
                "model": "jev-1.13.0",
                "answers": {
                    key: {"type": "noul", "noul": self.scores.get(documents[key], 0.5)}
                    for key in payload["questions"]
                },
                "usage": {"input_tokens": 100, "output_tokens": 5},
            }).encode(),
        )


@pytest.fixture
def http(monkeypatch: pytest.MonkeyPatch) -> FakeHttp:
    monkeypatch.setenv("TYPESAFE_API_KEY", "test-secret")
    fake = FakeHttp(scores={"answer": 0.9, "noise": 0.1})
    monkeypatch.setattr("hakari_bench.models.urllib3.PoolManager", lambda **_: fake)
    monkeypatch.setattr("hakari_bench.models._import_auto_tokenizer", lambda: SimpleNamespace(
        from_pretrained=lambda *a, **kw: SimpleNamespace(
            model_max_length=kw.get("model_max_length"),
            encode=lambda text, **kw: [] if text.startswith("{") else text.split(),
        ),
    ))
    return fake


@pytest.mark.parametrize("mode,count", [("pointwise", 3), ("listwise", 1)])
def test_modes_send_expected_state_and_keep_ties_in_input_order(http: FakeHttp, mode: str, count: int) -> None:
    model = TypeSafeRerankerAdapter(model_name="jev-1.13.0", mode=mode)
    ranked = model.rank("question", ["noise", "answer", "answer"])
    assert [item["corpus_id"] for item in ranked] == [1, 2, 0]
    assert len(http.calls) == count
    for call in http.calls:
        assert call["payload"]["model"] == "jev-1.13.0"
        assert call["payload"]["state"]["query"] == "question"
        assert call["headers"]["Authorization"] == "Bearer test-secret"
        if mode == "pointwise":
            assert set(call["payload"]["state"]) == {"query", "document"}
            assert len(call["payload"]["questions"]) == 1
            assert call["payload"]["questions"]["relevant"]["instructions"] == (
                "Does this candidate document help answer the query? "
                "Prefer passages that contain the specific facts needed."
            )
        else:
            assert list(call["payload"]["state"]["documents"].values()) == ["noise", "answer", "answer"]
            for key, question in call["payload"]["questions"].items():
                assert f"`documents.{key}`" in question["instructions"]
    metadata = model.metadata()
    assert metadata["mode"] == mode
    if mode == "pointwise":
        assert metadata["instructions_template"] == http.calls[0]["payload"]["questions"]["relevant"]["instructions"]
    assert metadata["resolved_models"] == ["jev-1.13.0"]
    assert metadata["usage"]["input_tokens"] == count * 100
    assert metadata["usage"]["requests"] == count
    assert "test-secret" not in json.dumps(metadata)
    model.reset_task_statistics()
    assert model.metadata()["usage"]["requests"] == 0
    assert model.rank("question", []) == []
    assert len(http.calls) == count


def test_listwise_gets_all_candidates_despite_evaluator_batch_size(http: FakeHttp) -> None:
    model = TypeSafeRerankerAdapter(model_name="jev-1.13.0", mode="listwise")
    ids = [f"doc.{i}/odd" for i in range(101)]
    dataset = LoadedIrDataset(
        queries={"q": "question"}, corpus={key: "answer" if key == ids[0] else "noise" for key in ids},
        qrels={"q": {ids[0], ids[-1]}}, candidates={"q": ids}, evaluator_name="Test",
    )
    result = evaluate_reranker_task(
        model=model, dataset=dataset, batch_size=2, show_progress=False, rerank_top_n=100,
    )
    assert len(http.calls) == 1
    assert len(http.calls[0]["payload"]["questions"]) == 100
    assert len(result.top_rankings[0]["rankings"]["q"]) == 100
    # The ideal uses all qrels, including positives outside the shortlist.
    assert result.metrics["Test_reranker_ndcg@10"] == pytest.approx(1 / (1 + 1 / math.log2(3)))


def test_pointwise_ties_do_not_depend_on_request_completion_order(http: FakeHttp, monkeypatch: pytest.MonkeyPatch) -> None:
    request = http.request
    second_finished = threading.Event()

    def reversed_completion(method: str, url: str, **kwargs: Any) -> Any:
        text = json.loads(kwargs["body"])["state"]["document"]
        if text == "first":
            assert second_finished.wait(5)
        response = request(method, url, **kwargs)
        if text == "second":
            second_finished.set()
        return response

    monkeypatch.setattr(http, "request", reversed_completion)
    model = TypeSafeRerankerAdapter(model_name="jev-1.13.0", mode="pointwise", max_concurrency=2)
    assert [item["corpus_id"] for item in model.rank("q", ["first", "second"])] == [0, 1]


@pytest.mark.parametrize("score", [-0.1, 1.1, None, True, "0.5", float("nan")])
def test_invalid_scores_fail_without_producing_rankings(http: FakeHttp, score: Any) -> None:
    http.scores["bad"] = score
    model = TypeSafeRerankerAdapter(model_name="jev-1.13.0")
    with pytest.raises(ValueError, match="Noul|invalid JSON"):
        model.rank("q", ["bad"])


@pytest.mark.parametrize("status", [401, 422, 429, 529])
def test_http_errors_fail_without_fallback(http: FakeHttp, status: int) -> None:
    http.status = status
    model = TypeSafeRerankerAdapter(model_name="jev-1.13.0")
    with pytest.raises(RuntimeError, match=f"HTTP {status}"):
        model.rank("q", ["answer"])
    retries = http.calls[0]["retries"]
    assert retries.is_retry("POST", 429)
    assert retries.is_retry("POST", 529)
    assert not retries.is_retry("POST", 422)
    assert retries.respect_retry_after_header


@pytest.mark.parametrize("mode", ["pointwise", "listwise"])
def test_cli_modes_identity_and_builtin_loader(http: FakeHttp, mode: str, capsys: pytest.CaptureFixture[str]) -> None:
    args = parse_args([
        "evaluate", "reranker", "--model", "jev-1.13.0", "--model-loader", "typesafe",
        "--typesafe-mode", mode,
    ])
    assert args.model_loader_kwargs["mode"] == mode
    assert args.model_id == "typesafe/jev"
    assert args.model_source == {"type": "typesafe", "name": "jev-1.13.0"}
    _warn_if_missing_attention_implementation(args)
    assert not capsys.readouterr().err
    model = load_model(ModelLoadConfig(
        model_name_or_path=args.model, model_type="reranker", model_loader=args.model_loader,
        model_loader_kwargs=args.model_loader_kwargs,
    ))
    assert model.metadata()["mode"] == mode


@pytest.mark.parametrize("options", [
    ["evaluate", "dense", "--model", "jev", "--model-loader", "typesafe"],
    ["evaluate", "reranker", "--model", "jev", "--typesafe-mode", "pointwise"],
    ["evaluate", "reranker", "--model", "jev", "--model-loader", "typesafe", "--typesafe-mode", "bad"],
])
def test_cli_rejects_incompatible_options(options: list[str]) -> None:
    with pytest.raises(SystemExit):
        parse_args(options)


def test_cli_mode_from_loader_kwargs_and_alias() -> None:
    defaults = parse_args([
        "evaluate", "reranker", "--model", "jev-1.13.0", "--model-loader", "typesafe",
    ])
    assert defaults.typesafe_mode == "listwise"
    assert defaults.model_loader_kwargs["mode"] == "listwise"
    assert defaults.model_id == "typesafe/jev"
    args = parse_args([
        "evaluate", "reranker", "--model", "jev-1.13.0", "--model-loader", "typesafe",
        "--model-loader-kwargs-json", '{"mode":"pointwise"}',
    ])
    assert args.model_id == "typesafe/jev"
    args = parse_args([
        "evaluate", "reranker", "--model", "jev-1.13.0", "--model-loader", "typesafe",
        "--model-alias", "experiment/jev", "--typesafe-mode", "listwise",
    ])
    assert args.model_id == "experiment/jev"


@pytest.mark.parametrize("mode", ["pointwise", "listwise"])
def test_result_usage_is_per_task_and_cache_does_not_call_api(
    http: FakeHttp, monkeypatch: pytest.MonkeyPatch, tmp_path: Path, split_tokenizer: list[str], mode: str,
) -> None:
    monkeypatch.setattr("hakari_bench.results.resolve_dataset_revision", lambda *a, **kw: {})
    args = parse_args([
        "evaluate", "reranker", "--model", "jev-1.13.0", "--model-loader", "typesafe",
        "--typesafe-mode", mode, "--results-dir", str(tmp_path),
    ])
    if mode == "listwise":
        _limit_documents(http, monkeypatch, 1)
    custom = "Does {document} directly answer `query`?"
    model = TypeSafeRerankerAdapter(
        model_name=args.model, mode=mode,
        task_instructions={"Test/one": custom} if mode == "listwise" else None,
    )
    initial_metadata = collect_model_metadata(model, args)
    dataset = LoadedIrDataset(
        queries={"q": "question"}, corpus={"a": "answer", "b": "noise"},
        qrels={"q": {"a"}}, candidates={"q": ["b", "a"]}, evaluator_name="Test",
    )
    tasks = [EvalTask(
        dataset=NanoDatasetSpec(name="Test", dataset_id="test/data"),
        split_name=name, task_name=name,
    ) for name in ("one", "two")]
    results = []
    for task in tasks:
        result = run_or_load_task(
            task=task, model=model, args=args, environment={}, model_metadata=initial_metadata,
            dataset_loader=lambda _: dataset,
        )
        results.append(result)
        payload = read_result_json(result.output_path)
        metadata = payload["model"]["backend_metadata"]
        assert metadata["resolved_models"] == ["jev-1.13.0"]
        assert metadata["instruction_task"] == f"Test/{task.task_name}"
        if mode == "listwise":
            assert metadata["instructions_template"] == (custom if task.task_name == "one" else model.INSTRUCTIONS)
        assert metadata["usage"]["requests"] == 2
        assert metadata["usage"]["input_tokens"] == 200
        assert payload["config"]["model_loader_kwargs"]["mode"] == mode
        if mode == "listwise":
            trace = metadata["listwise_splitting"]["queries"][0]
            assert trace["status"] == "merged"
            assert trace["events"][0]["chunk_document_counts"] == [1, 1]
            assert len(metadata["listwise_splitting"]["queries"]) == 1
            assert metadata["usage"]["max_tokens_errors"] == 1
        assert "test-secret" not in json.dumps(payload)
    expected_calls = 6 if mode == "listwise" else 4
    assert len(http.calls) == expected_calls
    cached = run_or_load_task(
        task=tasks[0], model=model, args=args, environment={}, model_metadata=initial_metadata,
        dataset_loader=lambda _: pytest.fail("Cached task must not load dataset"),
    )
    assert cached.cache_hit
    assert len(http.calls) == expected_calls
    assert results[0].payload["model"]["backend_metadata"]["usage"]["requests"] == 2
    assert initial_metadata["backend_metadata"]["usage"]["requests"] == 0


@pytest.mark.parametrize("change", [
    {"answers": {}}, {"answers": {"doc_0": {"type": "score", "noul": 0.5}}},
    {"usage": {}}, {"model": None},
])
def test_malformed_responses_fail(http: FakeHttp, monkeypatch: pytest.MonkeyPatch, change: dict[str, Any]) -> None:
    request = http.request

    def changed(method: str, url: str, **kwargs: Any) -> Any:
        response = request(method, url, **kwargs)
        payload = json.loads(response.data)
        payload.update(change)
        response.data = json.dumps(payload).encode()
        return response

    monkeypatch.setattr(http, "request", changed)
    model = TypeSafeRerankerAdapter(model_name="jev-1.13.0")
    with pytest.raises(ValueError):
        model.rank("q", ["answer"])


@pytest.mark.parametrize("kwargs", [
    {"mode": "typo"}, {"max_concurrency": 0}, {"max_concurrency": 1.5},
    {"max_retries": -1}, {"timeout": 0}, {"unknown": True},
    {"split_state_token_budget": 0}, {"split_request_token_budget": -1},
])
def test_loader_rejects_invalid_settings(http: FakeHttp, kwargs: dict[str, Any]) -> None:
    with pytest.raises(ValueError):
        load_model(ModelLoadConfig(
            model_name_or_path="jev-1.13.0", model_type="reranker", model_loader="typesafe",
            model_loader_kwargs=kwargs,
        ))


def test_missing_key_fails_before_network(http: FakeHttp, monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.delenv("TYPESAFE_API_KEY")
    with pytest.raises(ValueError, match="TYPESAFE_API_KEY"):
        TypeSafeRerankerAdapter(model_name="jev-1.13.0", dotenv_path=None)
    assert not http.calls


def test_params_json_mode_and_conflicting_cli_mode() -> None:
    params = json.dumps({"model": {"source": "jev-1.13.0", "loader": "typesafe", "loader_kwargs": {"mode": "pointwise"}}})
    args = parse_args(["evaluate", "reranker", "--params-json", params])
    assert args.model_id == "typesafe/jev"
    with pytest.raises(SystemExit):
        parse_args(["evaluate", "reranker", "--params-json", params, "--typesafe-mode", "listwise"])


@pytest.fixture
def split_tokenizer(monkeypatch: pytest.MonkeyPatch) -> list[str]:
    texts: list[str] = []

    class Tokenizer:
        def encode(self, text: str, **kwargs: Any) -> list[int]:
            assert kwargs["truncation"] is False
            assert kwargs["add_special_tokens"] is False
            texts.append(text)
            # Ignore scaffolding in these controlled budget tests.
            return [] if text.startswith("{") else [1] * len(text.split())

    monkeypatch.setattr("hakari_bench.models._import_auto_tokenizer", lambda: SimpleNamespace(
        from_pretrained=lambda *a, **kw: Tokenizer(),
    ))
    return texts


def _limit_documents(http: FakeHttp, monkeypatch: pytest.MonkeyPatch, maximum: int) -> None:
    request = http.request

    def limited(method: str, url: str, **kwargs: Any) -> Any:
        response = request(method, url, **kwargs)
        if len(json.loads(kwargs["body"])["questions"]) > maximum:
            response.status = 400
            response.data = b'{"detail":{"error_type":"max_tokens_exceeded"}}'
        return response

    monkeypatch.setattr(http, "request", limited)


@pytest.mark.parametrize("count,budget,expected", [
    (100, 2000, [50, 50]), (100, 1200, [33, 33, 34]),
    (101, 2000, [50, 51]), (83, 2000, [41, 42]), (2, 2000, [1, 1]),
])
def test_listwise_splits_balanced_counts_and_merges_all_scores(
    http: FakeHttp, monkeypatch: pytest.MonkeyPatch, split_tokenizer: list[str],
    count: int, budget: int, expected: list[int], capsys: pytest.CaptureFixture[str],
) -> None:
    documents = [f"entry{i} " + "word " * 29 for i in range(count)]
    http.scores = {text: i / count for i, text in enumerate(documents)}
    _limit_documents(http, monkeypatch, max(expected))
    model = TypeSafeRerankerAdapter(
        model_name="jev-1.13.0", split_state_token_budget=budget, split_request_token_budget=100000,
    )
    ranked = model.rank("q", documents)
    assert [item["corpus_id"] for item in ranked] == list(reversed(range(count)))
    preemptive = count * 30 > budget
    successful_calls = http.calls if preemptive else http.calls[1:]
    assert [len(call["payload"]["questions"]) for call in successful_calls] == expected
    sent = [doc for call in successful_calls for doc in call["payload"]["state"]["documents"].values()]
    assert sorted(sent) == sorted(documents)
    assert all(text in split_tokenizer for text in documents)
    splitting = model.metadata()["listwise_splitting"]
    trace = splitting["queries"][0]
    assert splitting["tokenizer"] == "jhu-clsp/mmBERT-base"
    assert trace["original_document_count"] == count
    assert trace["events"][0]["chunk_document_counts"] == expected
    reason = "estimated_token_budget" if preemptive else "max_tokens_exceeded"
    assert trace["events"][0]["reason"] == reason
    assert len(trace["final_chunks"]) == len(expected)
    assert model.metadata()["usage"]["max_tokens_errors"] == (0 if preemptive else 1)
    assert reason in capsys.readouterr().err
    for chunk, call in zip(trace["final_chunks"], successful_calls, strict=True):
        actual_indices = [int(key.removeprefix("doc_")) for key in call["payload"]["questions"]]
        assert actual_indices == chunk["document_indices"]
        if len(actual_indices) > 3:
            assert actual_indices != sorted(actual_indices)
            assert actual_indices != sorted(actual_indices, reverse=True)
        assert chunk["estimated_tokens"]["state_plus_longest_question"] <= chunk["state_token_budget"]
    snapshot = model.metadata()
    model.reset_task_statistics()
    assert model.metadata()["listwise_splitting"]["queries"] == []
    assert len(snapshot["listwise_splitting"]["queries"]) == 1


def test_repeated_overflow_splits_further_and_preserves_ties(
    http: FakeHttp, monkeypatch: pytest.MonkeyPatch, split_tokenizer: list[str],
) -> None:
    _limit_documents(http, monkeypatch, 21)
    documents = ["duplicate"] * 83
    model = TypeSafeRerankerAdapter(model_name="jev-1.13.0")
    assert [item["corpus_id"] for item in model.rank("q", documents)] == list(range(83))
    trace = model.metadata()["listwise_splitting"]["queries"][0]
    assert [len(c["document_indices"]) for c in trace["final_chunks"]] == [20, 21, 21, 21]
    assert len(trace["events"]) == 3
    assert sorted(i for c in trace["final_chunks"] for i in c["document_indices"]) == list(range(83))
    assert model.metadata()["usage"]["max_tokens_errors"] == 3
    assert [event["state_token_budget"] for event in trace["events"]] == [13000, 6500, 6500]


def test_partition_balances_token_lengths_as_well_as_document_counts(
    http: FakeHttp, monkeypatch: pytest.MonkeyPatch, split_tokenizer: list[str],
) -> None:
    _limit_documents(http, monkeypatch, 2)
    documents = ["x " * size for size in (100, 90, 10, 1)]
    model = TypeSafeRerankerAdapter(model_name="jev-1.13.0")
    model.rank("q", documents)
    chunks = model.metadata()["listwise_splitting"]["queries"][0]["final_chunks"]
    assert sorted(sum(len(documents[i].split()) for i in c["document_indices"]) for c in chunks) == [100, 101]


def test_single_document_overflow_stops_without_truncation(
    http: FakeHttp, monkeypatch: pytest.MonkeyPatch, split_tokenizer: list[str],
) -> None:
    _limit_documents(http, monkeypatch, 0)
    model = TypeSafeRerankerAdapter(model_name="jev-1.13.0")
    with pytest.raises(RuntimeError, match="single document"):
        model.rank("q", ["unmodified document"])
    assert len(http.calls) == 1
    assert http.calls[0]["payload"]["state"]["documents"] == {"doc_0": "unmodified document"}


def test_other_400_errors_do_not_split(
    http: FakeHttp, monkeypatch: pytest.MonkeyPatch,
) -> None:
    http.status = 400
    model = TypeSafeRerankerAdapter(model_name="jev-1.13.0")
    with pytest.raises(RuntimeError, match="HTTP 400"):
        model.rank("q", ["a", "b"])
    assert len(http.calls) == 1
    assert model.metadata()["listwise_splitting"]["queries"] == []


@pytest.mark.parametrize("name,revision,expected_revision", [
    ("jhu-clsp/mmBERT-base", None, TypeSafeRerankerAdapter.SPLIT_TOKENIZER_REVISION),
    ("another/tokenizer", None, None), ("another/tokenizer", "custom-rev", "custom-rev"),
])
def test_configurable_tokenizer_counts_past_8k_without_truncation(
    http: FakeHttp, monkeypatch: pytest.MonkeyPatch, name: str, revision: str | None, expected_revision: str | None,
) -> None:
    loads = []

    def load(tokenizer_name: str, **kwargs: Any) -> Any:
        loads.append((tokenizer_name, kwargs))
        assert kwargs["model_max_length"] == 65536
        return SimpleNamespace(model_max_length=65536, encode=lambda text, **kw: list(range(9000)))

    monkeypatch.setattr("hakari_bench.models._import_auto_tokenizer", lambda: SimpleNamespace(from_pretrained=load))
    model = load_model(ModelLoadConfig(
        model_name_or_path="jev-1.13.0", model_type="reranker", model_loader="typesafe",
        model_loader_kwargs={"split_tokenizer_name": name, "split_tokenizer_revision": revision},
    ))
    assert model._split_token_length("long document") == 9000
    assert loads[0][0] == name
    assert loads[0][1]["revision"] == expected_revision
    metadata = model.metadata()["listwise_splitting"]
    assert metadata["tokenizer"] == name
    assert metadata["tokenizer_max_length"] == 65536


def test_each_chunk_fits_budget_including_overhead(
    http: FakeHttp, monkeypatch: pytest.MonkeyPatch, split_tokenizer: list[str],
) -> None:
    # Dividing the parent estimate by the budget suggests 2 chunks, but each
    # child repeats 30 tokens of query/question overhead, requiring 3 chunks.
    model = TypeSafeRerankerAdapter(model_name="jev-1.13.0", split_state_token_budget=100)
    monkeypatch.setattr(model, "_estimate_listwise_tokens", lambda query, indices, lengths: {
        "state_plus_longest_question": sum(lengths[i] for i in indices) + 30,
        "request": sum(lengths[i] for i in indices) + 30,
    })
    model.rank("q", ["word " * 20 for _ in range(8)])
    chunks = model.metadata()["listwise_splitting"]["queries"][0]["final_chunks"]
    assert [len(c["document_indices"]) for c in chunks] == [2, 3, 3]
    assert all(c["estimated_tokens"]["state_plus_longest_question"] <= 100 for c in chunks)
    assert len(http.calls) == 3


def test_single_document_above_estimated_budget_is_not_truncated_or_sent(http: FakeHttp) -> None:
    model = TypeSafeRerankerAdapter(model_name="jev-1.13.0", split_state_token_budget=2)
    with pytest.raises(RuntimeError, match="single document"):
        model.rank("q", ["one two three"])
    assert http.calls == []

@pytest.mark.parametrize("workers", [None, 2])
def test_listwise_parallel_queries_preserve_rankings_and_usage(
    http: FakeHttp, monkeypatch: pytest.MonkeyPatch, workers: int | None,
) -> None:
    count = workers or 4
    barrier = threading.Barrier(count)
    request = http.request
    active = 0
    peak = 0
    lock = threading.Lock()

    def concurrent_request(method: str, url: str, **kwargs: Any) -> Any:
        nonlocal active, peak
        with lock:
            active += 1
            peak = max(peak, active)
        try:
            barrier.wait(timeout=5)
            return request(method, url, **kwargs)
        finally:
            with lock:
                active -= 1

    monkeypatch.setattr(http, "request", concurrent_request)
    model = TypeSafeRerankerAdapter(model_name="jev-latest", max_concurrency=workers)
    dataset = LoadedIrDataset(
        queries={f"q{i}": f"question {i}" for i in range(count * 2)},
        corpus={"a": "answer", "b": "noise"},
        qrels={f"q{i}": {"a"} for i in range(count * 2)},
        candidates={f"q{i}": ["a", "b"] for i in range(count * 2)}, evaluator_name="Parallel",
    )
    result = evaluate_reranker_task(
        model=model, dataset=dataset, batch_size=32, show_progress=False, rerank_top_n=None,
    )
    assert peak == count
    rankings = result.top_rankings[0]["rankings"]
    assert list(rankings) == list(dataset.queries)
    assert all(ranking == ["a", "b"] for ranking in rankings.values())
    metadata = model.metadata()
    assert metadata["max_concurrency"] == count
    assert metadata["query_concurrency"] == count
    assert metadata["usage"]["requests"] == count * 2
    assert metadata["usage"]["input_tokens"] == count * 200


def test_pointwise_keeps_twenty_workers_and_sequential_queries(http: FakeHttp) -> None:
    model = TypeSafeRerankerAdapter(model_name="jev-latest", mode="pointwise")
    assert model.max_concurrency == 20
    assert model.query_concurrency == 1


def test_task_instruction_exact_full_name_and_reset(http: FakeHttp) -> None:
    custom = "Does {document} directly answer `query`?"
    model = TypeSafeRerankerAdapter(
        model_name="jev-latest", task_instructions={"NanoBEIR-en/msmarco": custom},
    )
    model.configure_task("NanoBEIR-en/msmarco")
    model.rank("q", ["answer"])
    assert http.calls[-1]["payload"]["questions"]["doc_0"]["instructions"] == "Does `documents.doc_0` directly answer `query`?"
    assert model.metadata()["instructions_template"] == custom
    assert model.metadata()["instruction_task"] == "NanoBEIR-en/msmarco"
    model.configure_task("Other/msmarco")
    model.rank("q", ["answer"])
    assert model.metadata()["instructions_template"] == model.INSTRUCTIONS
    assert model.metadata()["instruction_source"] == "default"


def test_task_instruction_cli_full_match_warning(capsys: pytest.CaptureFixture[str]) -> None:
    from hakari_bench.cli import _warn_unmatched_typesafe_tasks
    args = parse_args([
        "evaluate", "reranker", "--model", "jev-latest", "--model-loader", "typesafe",
        "--typesafe-task-instructions-json", '{"msmarco":"Does {document} answer `query`?"}',
    ])
    task = EvalTask(dataset=NanoDatasetSpec(name="NanoBEIR-en", dataset_id="test/data"), split_name="msmarco", task_name="msmarco")
    _warn_unmatched_typesafe_tasks(args, [task])
    assert "msmarco" in capsys.readouterr().err
    args.model_loader_kwargs["task_instructions"] = {"NanoBEIR-en/msmarco": "Does {document} answer `query`?"}
    _warn_unmatched_typesafe_tasks(args, [task])
    assert capsys.readouterr().err == ""

@pytest.mark.parametrize("mode", ["pointwise", "listwise"])
@pytest.mark.parametrize("limit", [4000, 2, None])
def test_document_token_truncation_keeps_ids_and_records_counts(
    http: FakeHttp, monkeypatch: pytest.MonkeyPatch, mode: str, limit: int | None,
) -> None:
    class Tokenizer:
        def encode(self, text: str, **kwargs: Any) -> list[str]:
            return text.split()

        def decode(self, tokens: list[str], **kwargs: Any) -> str:
            return " ".join(tokens)

    monkeypatch.setattr("hakari_bench.models._import_auto_tokenizer", lambda: SimpleNamespace(from_pretrained=lambda *a, **kw: Tokenizer()))
    kwargs: dict[str, Any] = {} if limit == 4000 else {"document_max_tokens": limit}
    model = TypeSafeRerankerAdapter(model_name="jev-latest", mode=mode, **kwargs)
    original = "word " * 4001
    documents = ["answer", original, original]
    result = model.rank("question stays unchanged", documents)
    assert sorted(r["corpus_id"] for r in result) == [0, 1, 2]
    sent = []
    for call in http.calls:
        state = call["payload"]["state"]
        assert state["query"] == "question stays unchanged"
        sent.extend(state["documents"].values() if mode == "listwise" else [state["document"]])
    assert len(sent) == 3
    assert sorted(len(s.split()) for s in sent) == [1, limit or 4001, limit or 4001]
    assert documents[1] == original
    metadata = model.metadata()["document_truncation"]
    assert metadata["max_tokens"] == limit
    assert metadata["truncated_documents"] == (2 if limit else 0)
    if limit:
        assert metadata["events"][0]["document_index"] == 1
        assert metadata["events"][0]["original_tokens"] == 4001
        assert metadata["events"][0]["sent_tokens"] == limit
    model.reset_task_statistics()
    assert model.metadata()["document_truncation"]["truncated_documents"] == 0


@pytest.mark.parametrize("limit", [0, -1, True, 1.5])
def test_invalid_document_token_limit(http: FakeHttp, limit: Any) -> None:
    with pytest.raises(ValueError, match="document_max_tokens"):
        TypeSafeRerankerAdapter(model_name="jev-latest", document_max_tokens=limit)


def test_typesafe_static_card_selects_hosted_loader() -> None:
    args = parse_args([
        "evaluate", "from-model-card", "--model-card", "config/model_cards/typesafe__jev.yaml",
        "--dataset", "NanoMIRACL", "--split", "ja",
    ])
    assert args.model == "jev-1.13.0"
    assert args.model_id == "typesafe/jev"
    assert args.model_loader == "typesafe"
    assert args.model_type == "reranker"
    assert args.model_loader_kwargs["mode"] == "listwise"
    assert args.model_max_seq_length is None
