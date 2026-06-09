from __future__ import annotations

from typing import Any

import numpy as np

from hakari_bench.models import ModelLoadConfig


class DummyEmbeddingBackend:
    similarity_fn_name = "dot"

    def __init__(self, *, scale: float = 1.0, backend_name: str = "dummy") -> None:
        self.scale = float(scale)
        self.backend_name = backend_name
        self.query_calls: list[dict[str, Any]] = []
        self.document_calls: list[dict[str, Any]] = []

    def encode_query(self, sentences: list[str], **kwargs: Any) -> np.ndarray:
        self.query_calls.append({"sentences": sentences, **kwargs})
        return self._encode(sentences, role="query")

    def encode_document(self, sentences: list[str], **kwargs: Any) -> np.ndarray:
        self.document_calls.append({"sentences": sentences, **kwargs})
        return self._encode(sentences, role="document")

    def metadata(self) -> dict[str, Any]:
        return {
            "backend_library": "hakari-dummy",
            "backend_name": self.backend_name,
            "scale": self.scale,
        }

    def _encode(self, sentences: list[str], *, role: str) -> np.ndarray:
        vectors = [_text_vector(sentence, role=role) for sentence in sentences]
        return np.asarray(vectors, dtype=np.float32) * self.scale


class DummyRerankerBackend:
    def __init__(self, *, positive_token: str = "relevant") -> None:
        self.positive_token = positive_token
        self.predict_calls: list[dict[str, Any]] = []

    def predict(self, pairs: list[list[str]], **kwargs: Any) -> list[float]:
        self.predict_calls.append({"pairs": pairs, **kwargs})
        return [
            1.0 if self.positive_token.lower() in f"{query} {document}".lower() else 0.0
            for query, document in pairs
        ]

    def metadata(self) -> dict[str, Any]:
        return {"backend_library": "hakari-dummy", "positive_token": self.positive_token}


def load_model(config: ModelLoadConfig) -> Any:
    kwargs = dict(config.model_loader_kwargs or {})
    if config.model_type in {"dense", "sparse"}:
        return DummyEmbeddingBackend(**kwargs)
    if config.model_type == "reranker":
        return DummyRerankerBackend(**kwargs)
    raise ValueError(f"Dummy backend does not implement {config.model_type!r}.")


def _text_vector(text: str, *, role: str) -> list[float]:
    normalized = text.lower()
    cat_score = float("cat" in normalized)
    dog_score = float("dog" in normalized)
    if role == "document" and "distractor" in normalized:
        return [-1.0, -1.0]
    return [cat_score, dog_score]
