from __future__ import annotations

from typing import Any, Iterable, Protocol, Sequence, cast

import numpy as np
import orjson
import urllib3

from hakari_bench.models import ModelLoadConfig


DEFAULT_QWEN3_PROMPTS = {
    "query": "Instruct: Given a web search query, retrieve relevant passages that answer the query\nQuery:",
    "document": "",
}


class _HttpClient(Protocol):
    def request(
        self,
        method: str,
        url: str,
        *,
        body: bytes,
        headers: dict[str, str],
        timeout: float,
    ) -> Any: ...


class TeiEmbeddingBackend:
    similarity_fn_name = "dot"

    def __init__(
        self,
        *,
        endpoint: str,
        model: str,
        prompts: dict[str, str] | None = None,
        query_prompt: str | None = None,
        document_prompt: str | None = None,
        query_prompt_name: str | None = "query",
        document_prompt_name: str | None = "document",
        timeout: float = 120.0,
        api_key: str | None = None,
        http: _HttpClient | None = None,
        similarity_fn_name: str = "dot",
    ) -> None:
        if not endpoint:
            raise ValueError("TEI endpoint is required.")
        if not model:
            raise ValueError("TEI model is required.")
        if not similarity_fn_name:
            raise ValueError("similarity_fn_name is required.")
        self.endpoint = endpoint.rstrip("/")
        self.model = model
        self.similarity_fn_name = similarity_fn_name
        self.prompts = dict(prompts or DEFAULT_QWEN3_PROMPTS)
        self.query_prompt = query_prompt
        self.document_prompt = document_prompt
        self.query_prompt_name = query_prompt_name
        self.document_prompt_name = document_prompt_name
        self.timeout = float(timeout)
        self.api_key = api_key
        self._http = http or urllib3.PoolManager()

    def encode_query(
        self,
        sentences: Sequence[str] | str,
        *,
        batch_size: int = 32,
        prompt: str | None = None,
        prompt_name: str | None = None,
        dimensions: int | None = None,
        truncate_dim: int | None = None,
        **_: Any,
    ) -> np.ndarray:
        resolved_prompt = self._resolve_prompt(
            explicit_prompt=prompt,
            explicit_prompt_name=prompt_name,
            default_prompt=self.query_prompt,
            default_prompt_name=self.query_prompt_name,
        )
        return self._encode(
            sentences,
            batch_size=batch_size,
            prompt=resolved_prompt,
            dimensions=dimensions or truncate_dim,
        )

    def encode_document(
        self,
        sentences: Sequence[str] | str,
        *,
        batch_size: int = 32,
        prompt: str | None = None,
        prompt_name: str | None = None,
        dimensions: int | None = None,
        truncate_dim: int | None = None,
        **_: Any,
    ) -> np.ndarray:
        resolved_prompt = self._resolve_prompt(
            explicit_prompt=prompt,
            explicit_prompt_name=prompt_name,
            default_prompt=self.document_prompt,
            default_prompt_name=self.document_prompt_name,
        )
        return self._encode(
            sentences,
            batch_size=batch_size,
            prompt=resolved_prompt,
            dimensions=dimensions or truncate_dim,
        )

    def metadata(self) -> dict[str, Any]:
        return {
            "backend_library": "text-embeddings-inference",
            "api": "openai_embeddings",
            "endpoint": self.endpoint,
            "model": self.model,
            "prompts": self.prompts,
            "query_prompt_name": self.query_prompt_name,
            "document_prompt_name": self.document_prompt_name,
            "similarity_fn_name": self.similarity_fn_name,
            "timeout": self.timeout,
        }

    def _resolve_prompt(
        self,
        *,
        explicit_prompt: str | None,
        explicit_prompt_name: str | None,
        default_prompt: str | None,
        default_prompt_name: str | None,
    ) -> str:
        if explicit_prompt is not None:
            return explicit_prompt
        prompt_name = explicit_prompt_name if explicit_prompt_name is not None else default_prompt_name
        if prompt_name is not None:
            return self.prompts.get(prompt_name, "")
        return default_prompt or ""

    def _encode(
        self,
        sentences: Sequence[str] | str,
        *,
        batch_size: int,
        prompt: str,
        dimensions: int | None,
    ) -> np.ndarray:
        texts = _normalize_sentences(sentences)
        if batch_size <= 0:
            raise ValueError("batch_size must be positive.")
        if not texts:
            return np.empty((0, int(dimensions or 0)), dtype=np.float32)

        vectors: list[list[float]] = []
        for batch in _batched(texts, batch_size):
            payload: dict[str, Any] = {
                "model": self.model,
                "input": [f"{prompt}{text}" for text in batch],
            }
            if dimensions is not None:
                payload["dimensions"] = int(dimensions)
            vectors.extend(self._request_embeddings(payload))
        return np.asarray(vectors, dtype=np.float32)

    def _request_embeddings(self, payload: dict[str, Any]) -> list[list[float]]:
        headers = {"Content-Type": "application/json"}
        if self.api_key:
            headers["Authorization"] = f"Bearer {self.api_key}"
        response = self._http.request(
            "POST",
            f"{self.endpoint}/v1/embeddings",
            body=orjson.dumps(payload),
            headers=headers,
            timeout=self.timeout,
        )
        status = int(getattr(response, "status", 0))
        data = bytes(getattr(response, "data", b""))
        if status >= 400:
            raise RuntimeError(f"TEI embeddings request failed with HTTP {status}: {data[:500].decode(errors='replace')}")
        parsed = orjson.loads(data)
        if not isinstance(parsed, dict):
            raise RuntimeError("TEI embeddings response was not a JSON object.")
        rows = parsed.get("data")
        if not isinstance(rows, list):
            raise RuntimeError("TEI embeddings response did not contain a data list.")
        embeddings: list[list[float]] = []
        for row in sorted(rows, key=_embedding_row_index):
            if not isinstance(row, dict):
                raise RuntimeError("TEI embeddings response contained an invalid embedding row.")
            row_payload = cast(dict[str, Any], row)
            embedding = row_payload.get("embedding")
            if not isinstance(embedding, list):
                raise RuntimeError("TEI embeddings response contained an invalid embedding row.")
            embeddings.append(embedding)
        return embeddings


def load_model(config: ModelLoadConfig) -> TeiEmbeddingBackend:
    kwargs = dict(config.model_loader_kwargs or {})
    endpoint = str(kwargs.pop("endpoint", kwargs.pop("api_endpoint", kwargs.pop("base_url", ""))))
    model = str(kwargs.pop("model", config.model_name_or_path))
    if config.model_type != "dense":
        raise ValueError("TEI embedding backend only implements dense evaluation.")
    return TeiEmbeddingBackend(endpoint=endpoint, model=model, **kwargs)


def _normalize_sentences(sentences: Sequence[str] | str) -> list[str]:
    if isinstance(sentences, str):
        return [sentences]
    return [str(sentence) for sentence in sentences]


def _batched(values: Sequence[str], batch_size: int) -> Iterable[list[str]]:
    for start in range(0, len(values), batch_size):
        yield list(values[start : start + batch_size])


def _embedding_row_index(row: object) -> int:
    if not isinstance(row, dict):
        return 0
    row_payload = cast(dict[str, Any], row)
    index = row_payload.get("index", 0)
    return int(index) if isinstance(index, int | str) else 0
