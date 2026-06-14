from __future__ import annotations

from typing import Any

from hakari_bench.models import ModelLoadConfig


class QuantizedSentenceTransformerBackend:
    def __init__(self, model: Any, *, backend: str, model_kwargs: dict[str, Any]) -> None:
        self.model = model
        self.backend = backend
        self.model_kwargs = dict(model_kwargs)

    def __getattr__(self, name: str) -> Any:
        return getattr(self.model, name)

    def encode(self, sentences: Any, **kwargs: Any) -> Any:
        return self.model.encode(sentences, **kwargs)

    def encode_query(self, sentences: Any, **kwargs: Any) -> Any:
        if hasattr(self.model, "encode_query"):
            return self.model.encode_query(sentences, **kwargs)
        return self.model.encode(sentences, **kwargs)

    def encode_document(self, sentences: Any, **kwargs: Any) -> Any:
        if hasattr(self.model, "encode_document"):
            return self.model.encode_document(sentences, **kwargs)
        return self.model.encode(sentences, **kwargs)

    def metadata(self) -> dict[str, Any]:
        return {
            "backend_library": "sentence-transformers",
            "sentence_transformers_backend": self.backend,
            "model_kwargs": self.model_kwargs,
        }


def load_model(config: ModelLoadConfig) -> QuantizedSentenceTransformerBackend:
    from sentence_transformers import SentenceTransformer

    kwargs = dict(config.model_loader_kwargs or {})
    backend = str(kwargs.pop("backend"))
    model_kwargs = dict(kwargs.pop("model_kwargs", {}))
    if kwargs:
        names = ", ".join(sorted(kwargs))
        raise ValueError(f"Unsupported loader kwargs: {names}")

    model = SentenceTransformer(
        config.model_name_or_path,
        backend=backend,
        device=config.device,
        revision=config.model_revision,
        trust_remote_code=config.trust_remote_code,
        model_kwargs=model_kwargs,
    )
    if config.max_seq_length is not None:
        model.max_seq_length = config.max_seq_length
    return QuantizedSentenceTransformerBackend(model, backend=backend, model_kwargs=model_kwargs)
