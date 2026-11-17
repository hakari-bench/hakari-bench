from __future__ import annotations

from types import SimpleNamespace
from typing import Any

import numpy as np
import orjson
import pytest
import urllib3

import hakari_bench.vllm_reranker as vllm_reranker
from hakari_bench.vllm_reranker import VllmRerankerClient


class CharTokenizer:
    """One token per character, with a Qwen3-Reranker-shaped chat template."""

    def apply_chat_template(self, messages: list[dict[str, str]], tokenize: bool = False) -> str:
        assert tokenize is False
        by_role = {message["role"]: message["content"] for message in messages}
        instruction = by_role.get("system", "default")
        return f"<S>{instruction}|Q:{by_role['query']}|D: {by_role['document']}<E><A>"

    def __call__(self, text: str, add_special_tokens: bool = False, truncation: bool = False, max_length=None):
        ids = [ord(char) for char in text]
        if truncation:
            ids = ids[:max_length]
        return {"input_ids": ids}

    def decode(self, ids: list[int], skip_special_tokens: bool = False) -> str:
        return "".join(chr(token) for token in ids)


class FakeHttp:
    def __init__(self) -> None:
        self.payloads: list[dict[str, Any]] = []

    def request(self, method: str, url: str, *, body: bytes, headers: dict[str, str], timeout: float) -> Any:
        assert method == "POST" and url.endswith("/classify")
        payload = orjson.loads(body)
        self.payloads.append(payload)
        # Score each input by its length, returned out of order to check index handling.
        rows = [{"index": index, "probs": [float(len(ids))]} for index, ids in enumerate(payload["input"])]
        return SimpleNamespace(status=200, data=orjson.dumps({"data": rows[::-1]}))


def make_client(max_seq_length: int = 60, **kwargs: Any) -> tuple[VllmRerankerClient, FakeHttp]:
    http = FakeHttp()
    client = VllmRerankerClient(
        endpoint="http://server/",
        served_model="served",
        tokenizer=CharTokenizer(),
        max_seq_length=max_seq_length,
        prompts={"query": "find"},
        default_prompt_name="query",
        http=http,
        **kwargs,
    )
    return client, http


def text(ids: list[int]) -> str:
    return "".join(chr(token) for token in ids)


def test_short_pairs_match_the_full_template_and_default_prompt() -> None:
    client, _ = make_client()
    ids = client.prepare_pair("q", "doc", instruction="find")
    assert text(ids) == "<S>find|Q:q|D: doc<E><A>"
    assert client.truncated_pairs == 0


def test_long_documents_keep_prefix_query_and_suffix() -> None:
    client, _ = make_client()
    ids = client.prepare_pair("q", "x" * 500, instruction="find")
    assert len(ids) == 60
    assert text(ids).startswith("<S>find|Q:q|D: xxx")
    assert text(ids).endswith("x<E><A>")
    assert client.truncated_pairs == 1 and client.truncated_queries == 0


def test_oversized_queries_are_cut_to_leave_room_for_the_document() -> None:
    client, _ = make_client()
    ids = client.prepare_pair("y" * 500, "doc", instruction="find")
    rendered = text(ids)
    assert len(ids) <= 60 and rendered.endswith("|D: doc<E><A>")
    assert client.truncated_queries == 1


def test_document_pre_cut_gives_the_same_tokens(monkeypatch: pytest.MonkeyPatch) -> None:
    document = "abc " * 5000
    client, _ = make_client(max_seq_length=200)
    monkeypatch.setattr(vllm_reranker, "PRE_CUT_SAFETY_TOKENS", 1)
    with_cut = client.prepare_pair("q", document, instruction="find")
    monkeypatch.setattr(vllm_reranker, "PRE_CUT_CHARS_PER_TOKEN", 10**9)
    without_cut = client.prepare_pair("q", document, instruction="find")
    assert with_cut == without_cut


def test_predict_batches_by_tokens_and_keeps_pair_order() -> None:
    client, http = make_client(max_request_tokens=60, concurrency=2)
    pairs = [["q", "d" * size] for size in (1, 30, 5, 30)]
    scores = client.predict(pairs, batch_size=4)
    expected = [len(client.prepare_pair(q, d, instruction="find")) for q, d in pairs]
    np.testing.assert_array_equal(scores, np.asarray(expected, dtype=np.float32))
    assert all(sum(len(ids) for ids in payload["input"]) <= 60 or len(payload["input"]) == 1 for payload in http.payloads)
    assert all(payload["use_activation"] is False and payload["model"] == "served" for payload in http.payloads)
    assert client.metadata()["scored_pairs"] == 4


class DroppedOnceHttp(FakeHttp):
    def __init__(self) -> None:
        super().__init__()
        self.calls = 0

    def request(self, method: str, url: str, *, body: bytes, headers: dict[str, str], timeout: float) -> Any:
        self.calls += 1
        if self.calls == 1:
            raise urllib3.exceptions.ProtocolError("Connection aborted.")
        return super().request(method, url, body=body, headers=headers, timeout=timeout)


def test_classify_resends_after_a_dropped_connection() -> None:
    http = DroppedOnceHttp()
    client, _ = make_client()
    client._http = http
    scores = client.predict([["q", "d"]])
    assert http.calls == 2 and scores.shape == (1,)


def test_explicit_prompt_overrides_the_default() -> None:
    client, http = make_client()
    client.predict([["q", "d"]], prompt="other")
    assert text(http.payloads[0]["input"][0]).startswith("<S>other|")
