"""Custom model loaders for model-specific benchmark compatibility issues.

The safe Japanese sparse loader exists because Japanese `BertJapaneseTokenizer`
uses native MeCab/fugashi tokenization before Hugging Face truncation is applied.
Very long raw benchmark documents can therefore crash the native tokenizer
process before `max_seq_length` has a chance to shorten token IDs. The wrapper
keeps Sentence Transformers `SparseEncoder` loading intact and only applies a
pre-tokenizer character limit to raw query/document strings.
"""

from __future__ import annotations

import importlib
from collections.abc import Sequence
from typing import Any

from hakari_bench.models import ModelLoadConfig, resolve_attn_implementation, resolve_torch_dtype


class PreTokenizerCharacterLimitSparseEncoder:
    def __init__(self, model: Any, *, max_input_chars: int) -> None:
        self.model = model
        self.max_input_chars = max_input_chars

    def __getattr__(self, name: str) -> Any:
        return getattr(self.model, name)

    def encode_query(
        self,
        sentences: str | Sequence[str],
        *,
        batch_size: int = 32,
        show_progress_bar: bool = False,
        convert_to_tensor: bool = True,
        convert_to_sparse_tensor: bool = True,
        save_to_cpu: bool = True,
        **kwargs: Any,
    ) -> Any:
        return self.model.encode_query(
            self._limit(sentences),
            batch_size=batch_size,
            show_progress_bar=show_progress_bar,
            convert_to_tensor=convert_to_tensor,
            convert_to_sparse_tensor=convert_to_sparse_tensor,
            save_to_cpu=save_to_cpu,
            **kwargs,
        )

    def encode_document(
        self,
        sentences: str | Sequence[str],
        *,
        batch_size: int = 32,
        show_progress_bar: bool = False,
        convert_to_tensor: bool = True,
        convert_to_sparse_tensor: bool = True,
        save_to_cpu: bool = True,
        **kwargs: Any,
    ) -> Any:
        return self.model.encode_document(
            self._limit(sentences),
            batch_size=batch_size,
            show_progress_bar=show_progress_bar,
            convert_to_tensor=convert_to_tensor,
            convert_to_sparse_tensor=convert_to_sparse_tensor,
            save_to_cpu=save_to_cpu,
            **kwargs,
        )

    def encode(self, sentences: str | Sequence[str], **kwargs: Any) -> Any:
        return self.model.encode(self._limit(sentences), **kwargs)

    def metadata(self) -> dict[str, Any]:
        return {
            "backend_library": "sentence-transformers",
            "compatibility": "pre_tokenizer_character_limit",
            "max_input_chars": self.max_input_chars,
            "reason": "avoid native Japanese tokenizer crashes on very long raw inputs before tokenizer truncation",
        }

    def _limit(self, sentences: str | Sequence[str]) -> str | list[str]:
        if isinstance(sentences, str):
            return sentences[: self.max_input_chars]
        return [
            sentence[: self.max_input_chars] if len(sentence) > self.max_input_chars else sentence
            for sentence in sentences
        ]


def load_safe_japanese_sparse_encoder(config: ModelLoadConfig) -> PreTokenizerCharacterLimitSparseEncoder:
    """Load a SparseEncoder with a raw text guard for Japanese tokenizers.

    Use this for Japanese SPLADE-style models that rely on
    `BertJapaneseTokenizer` with MeCab/fugashi. The guard is intentionally
    applied before tokenizer calls, because tokenizer-level truncation happens
    too late to avoid native crashes on very long raw inputs.
    """

    kwargs = dict(config.model_loader_kwargs or {})
    max_input_chars = int(kwargs.pop("max_input_chars", 8192))
    if kwargs:
        names = ", ".join(sorted(kwargs))
        raise ValueError(f"Unsupported loader kwargs for safe Japanese SparseEncoder: {names}")

    model_kwargs: dict[str, Any] = {"torch_dtype": resolve_torch_dtype(config.dtype)}
    attn_implementation = resolve_attn_implementation(
        attn_implementation=config.attn_implementation,
        flash_attn2=config.flash_attn2,
    )
    if attn_implementation is not None:
        model_kwargs["attn_implementation"] = attn_implementation

    sparse_encoder_cls = getattr(importlib.import_module("sentence_transformers.sparse_encoder"), "SparseEncoder")
    model = sparse_encoder_cls(
        config.model_name_or_path,
        device=config.device,
        revision=config.model_revision,
        trust_remote_code=config.trust_remote_code,
        model_kwargs=model_kwargs,
    )
    if config.max_seq_length is not None:
        model.max_seq_length = config.max_seq_length
    return PreTokenizerCharacterLimitSparseEncoder(model, max_input_chars=max_input_chars)
