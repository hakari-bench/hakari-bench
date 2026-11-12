"""Use native ST6 role tokenization for pplx-embed-v2-late checkpoints.

Requires sentence-transformers >=6 and transformers >=5.4. Import lazily so
installations using the supported ST5 baseline can still import other examples.
"""
from __future__ import annotations

from typing import Any

from hakari_bench.models import ModelLoadConfig, resolve_torch_dtype


class NativeMultiVectorBackend:
    def __init__(self, config: ModelLoadConfig) -> None:
        # ST6-only class; the supported ST5 baseline used for type checking lacks it.
        from sentence_transformers import MultiVectorEncoder  # ty: ignore[unresolved-import]

        self.model = MultiVectorEncoder(
            config.model_name_or_path,
            revision=config.model_revision,
            device=config.device,
            model_kwargs={
                "dtype": resolve_torch_dtype(config.dtype),
                "attn_implementation": config.attn_implementation,
            },
        )
        first = self.model[0]
        self.query_length = first.query_length
        self.document_length = first.document_length
        self.max_seq_length = self.document_length
        self.query_prefix = self.model.prompts["query"]
        self.document_prefix = self.model.prompts["document"]
        self.do_query_expansion = bool(first.query_expansion)
        self.attend_to_expansion_tokens = False

    def __getattr__(self, name: str) -> Any:
        return getattr(self.model, name)

    def encode(
        self, sentences: list[str], *, is_query: bool,
        batch_size: int = 8, show_progress_bar: bool = False, **kwargs: Any,
    ) -> Any:
        method = self.model.encode_query if is_query else self.model.encode_document
        return method(
            sentences, batch_size=batch_size, show_progress_bar=show_progress_bar,
            convert_to_numpy=True, **kwargs,
        )

    def metadata(self) -> dict[str, Any]:
        return {
            "backend_library": "sentence-transformers",
            "encoder_class": "MultiVectorEncoder",
            "marker_placement": "native checkpoint first-position markers",
            "query_length": self.query_length,
            "document_length": self.document_length,
            "query_expansion": None,
        }


def load_model(config: ModelLoadConfig) -> NativeMultiVectorBackend:
    return NativeMultiVectorBackend(config)
