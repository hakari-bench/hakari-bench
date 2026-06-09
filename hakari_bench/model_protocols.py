from __future__ import annotations

from collections.abc import Sequence
from typing import Any, Protocol


class DenseEmbeddingModel(Protocol):
    similarity_fn_name: str

    def encode(self, sentences: Sequence[str], **kwargs: Any) -> Any: ...


class RoleAwareEmbeddingModel(Protocol):
    def encode_query(self, sentences: Sequence[str], **kwargs: Any) -> Any: ...

    def encode_document(self, sentences: Sequence[str], **kwargs: Any) -> Any: ...


class RerankerModel(Protocol):
    def predict(self, pairs: Sequence[Sequence[str]], **kwargs: Any) -> Sequence[float]: ...


class LateInteractionModel(Protocol):
    def encode(self, sentences: Sequence[str], *, is_query: bool, **kwargs: Any) -> Any: ...


def validate_model_capabilities(model: Any, *, model_type: str) -> None:
    if model_type in {"dense", "sparse"}:
        has_role_encode = callable(getattr(model, "encode_query", None)) and callable(
            getattr(model, "encode_document", None)
        )
        if has_role_encode or callable(getattr(model, "encode", None)):
            return
        raise TypeError(
            f"{model_type} model backends must expose encode(sentences, **kwargs) or both "
            "encode_query(sentences, **kwargs) and encode_document(sentences, **kwargs)."
        )

    if model_type == "late-interaction":
        if callable(getattr(model, "encode", None)):
            return
        raise TypeError("late-interaction model backends must expose encode(sentences, is_query=..., **kwargs).")

    if model_type == "reranker":
        if callable(getattr(model, "rank", None)) or callable(getattr(model, "predict", None)) or callable(model):
            return
        raise TypeError("reranker model backends must expose rank(...), predict(...), or be callable.")

    raise ValueError(f"Unsupported model type: {model_type}")
