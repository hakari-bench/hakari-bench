from __future__ import annotations

import orjson
import pytest

from examples.custom_backends.tei_embedding import TeiEmbeddingBackend, load_model
from hakari_bench.models import ModelLoadConfig


class _FakeResponse:
    def __init__(self, *, status: int, payload: object) -> None:
        self.status = status
        self.data = orjson.dumps(payload)


class _FakeHttp:
    def __init__(self) -> None:
        self.requests: list[dict[str, object]] = []

    def request(self, method: str, url: str, *, body: bytes, headers: dict[str, str], timeout: float) -> _FakeResponse:
        payload = orjson.loads(body)
        self.requests.append(
            {
                "method": method,
                "url": url,
                "payload": payload,
                "headers": headers,
                "timeout": timeout,
            }
        )
        data = [
            {"object": "embedding", "index": index, "embedding": [float(index), 1.0]}
            for index, _ in enumerate(payload["input"])
        ]
        return _FakeResponse(status=200, payload={"object": "list", "data": data, "model": payload["model"]})


def test_tei_backend_batches_requests_and_applies_role_prompts() -> None:
    http = _FakeHttp()
    model = TeiEmbeddingBackend(
        endpoint="http://tei.test/",
        model="Qwen/Qwen3-Embedding-4B",
        http=http,  # type: ignore[arg-type]
    )

    query_embeddings = model.encode_query(["q1", "q2", "q3"], batch_size=2, dimensions=1024)
    document_embeddings = model.encode_document(["d1"], batch_size=2)

    assert query_embeddings.shape == (3, 2)
    assert document_embeddings.shape == (1, 2)
    assert [request["url"] for request in http.requests] == [
        "http://tei.test/v1/embeddings",
        "http://tei.test/v1/embeddings",
        "http://tei.test/v1/embeddings",
    ]
    assert http.requests[0]["payload"] == {
        "model": "Qwen/Qwen3-Embedding-4B",
        "input": [
            "Instruct: Given a web search query, retrieve relevant passages that answer the query\nQuery:q1",
            "Instruct: Given a web search query, retrieve relevant passages that answer the query\nQuery:q2",
        ],
        "dimensions": 1024,
    }
    assert http.requests[1]["payload"] == {
        "model": "Qwen/Qwen3-Embedding-4B",
        "input": ["Instruct: Given a web search query, retrieve relevant passages that answer the query\nQuery:q3"],
        "dimensions": 1024,
    }
    assert http.requests[2]["payload"] == {"model": "Qwen/Qwen3-Embedding-4B", "input": ["d1"]}


def test_tei_backend_allows_prompt_and_truncate_dim_overrides() -> None:
    http = _FakeHttp()
    model = TeiEmbeddingBackend(
        endpoint="http://tei.test",
        model="Qwen/Qwen3-Embedding-4B",
        prompts={"search": "Search: ", "passage": "Passage: "},
        query_prompt_name="search",
        document_prompt_name="passage",
        http=http,  # type: ignore[arg-type]
    )

    model.encode_query(["q"], prompt="Custom: ", truncate_dim=512)
    model.encode_document(["d"], prompt="")

    assert http.requests[0]["payload"] == {
        "model": "Qwen/Qwen3-Embedding-4B",
        "input": ["Custom: q"],
        "dimensions": 512,
    }
    assert http.requests[1]["payload"] == {"model": "Qwen/Qwen3-Embedding-4B", "input": ["d"]}


def test_load_model_requires_endpoint_and_dense_model_type() -> None:
    with pytest.raises(ValueError, match="endpoint"):
        load_model(ModelLoadConfig(model_name_or_path="Qwen/Qwen3-Embedding-4B", model_loader_kwargs={}))

    with pytest.raises(ValueError, match="dense"):
        load_model(
            ModelLoadConfig(
                model_name_or_path="Qwen/Qwen3-Embedding-4B",
                model_type="reranker",
                model_loader_kwargs={"endpoint": "http://tei.test"},
            )
        )


def test_tei_backend_raises_actionable_http_error() -> None:
    class FailingHttp:
        def request(self, *_: object, **__: object) -> _FakeResponse:
            return _FakeResponse(status=500, payload={"error": "boom"})

    model = TeiEmbeddingBackend(
        endpoint="http://tei.test",
        model="Qwen/Qwen3-Embedding-4B",
        http=FailingHttp(),  # type: ignore[arg-type]
    )

    with pytest.raises(RuntimeError, match="HTTP 500"):
        model.encode_query(["q"])
