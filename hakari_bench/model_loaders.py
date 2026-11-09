"""Custom model loaders for model-specific benchmark compatibility issues.

The mxbai v2 loader preserves relevance instructions during long-input
truncation and bounds padded batches without reducing the model context.

The safe Japanese sparse loader exists because Japanese `BertJapaneseTokenizer`
uses native MeCab/fugashi tokenization before Hugging Face truncation is applied.
Very long raw benchmark documents can therefore crash the native tokenizer
process before `max_seq_length` has a chance to shorten token IDs. The wrapper
keeps Sentence Transformers `SparseEncoder` loading intact and only applies a
pre-tokenizer character limit to raw query/document strings.
"""

from __future__ import annotations

import importlib
from dataclasses import replace
from collections.abc import Sequence
from typing import Any

import numpy as np
import torch

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


class MxbaiRerankV2Adapter:
    """Preserve the checkpoint's relevance prompt when truncating long pairs.

    Native CrossEncoder chat-template truncation can remove the final relevance
    instruction. Keep short inputs identical and reserve the checkpoint suffix
    for overflowing inputs, as the author's mxbai-rerank package does.
    """

    def __init__(self, model: Any, *, max_batch_tokens: int = 131072) -> None:
        self.model = model
        self.tokenizer = model.tokenizer
        self.max_seq_length = int(model.max_seq_length)
        if max_batch_tokens <= 0:
            raise ValueError("max_batch_tokens must be positive.")
        if self.tokenizer.padding_side != "left":
            raise ValueError("mxbai-rerank-v2 requires left padding.")
        self.max_batch_tokens = max_batch_tokens
        marker = "HAKARI_DOCUMENT_PLACEHOLDER_7d0c93"
        template = self._render("", marker)
        if template.count(marker) != 1:
            raise ValueError("Expected the mxbai-rerank-v2 query/document chat template.")
        self._suffix_ids = self._encode(template.split(marker)[1])
        self._query_budget = (self.max_seq_length - len(self._encode(self._render("", "")))) * 3 // 4
        if self._query_budget <= 0:
            raise ValueError("Model context is too short for the relevance template.")
        self.reset_task_statistics()

    def reset_task_statistics(self) -> None:
        self.oom_retries = 0
        self.truncated_pairs = 0
        self.truncated_queries = 0

    def __getattr__(self, name: str) -> Any:
        return getattr(self.model, name)

    def __getitem__(self, index: int) -> Any:
        return self.model[index]

    def _render(self, query: str, document: str) -> str:
        return self.tokenizer.apply_chat_template(
            [{"role": "query", "content": query}, {"role": "document", "content": document}],
            tokenize=False,
        )

    def _encode(self, text: str, limit: int | None = None) -> list[int]:
        kwargs = {} if limit is None else {"truncation": True, "max_length": limit}
        return self.tokenizer(text, add_special_tokens=False, **kwargs)["input_ids"]

    def prepare_pair(self, pair: Sequence[str]) -> list[int]:
        query, document = pair
        ids = self._encode(self._render(query, document), self.max_seq_length + 1)
        if len(ids) <= self.max_seq_length:
            return ids
        self.truncated_pairs += 1
        # Also leave room for the document when a query itself is oversized.
        query_ids = self._encode(query, self._query_budget + 1)
        if len(query_ids) > self._query_budget:
            self.truncated_queries += 1
            query = self.tokenizer.decode(query_ids[: self._query_budget], skip_special_tokens=False)
            ids = self._encode(self._render(query, document), self.max_seq_length + 1)
            if len(ids) <= self.max_seq_length:
                return ids
        return ids[: self.max_seq_length - len(self._suffix_ids)] + self._suffix_ids

    @torch.inference_mode()
    def predict(
        self, pairs: Sequence[Sequence[str]], *, batch_size: int = 32, show_progress_bar: bool = False
    ) -> np.ndarray:
        if batch_size <= 0:
            raise ValueError("batch_size must be positive.")
        self.model.eval()
        encoded = [self.prepare_pair(pair) for pair in pairs]
        ordered = sorted(range(len(encoded)), key=lambda index: len(encoded[index]), reverse=True)
        scores = np.empty(len(encoded), dtype=np.float32)
        offset = 0
        while offset < len(ordered):
            width = len(encoded[ordered[offset]])
            count = min(batch_size, max(1, self.max_batch_tokens // width))
            indices = ordered[offset : offset + count]
            scores[indices] = self._score_batch([encoded[index] for index in indices])
            offset += len(indices)
        if not np.isfinite(scores).all():
            raise ValueError("mxbai-rerank-v2 returned non-finite scores.")
        return scores

    def _score_batch(self, encoded: list[list[int]]) -> np.ndarray:
        try:
            return self._forward_batch(encoded)
        except torch.OutOfMemoryError:
            if len(encoded) == 1:
                raise
        # Leave the exception scope so its traceback releases GPU tensors.
        self.oom_retries += 1
        torch.cuda.empty_cache()
        middle = len(encoded) // 2
        return np.concatenate([self._score_batch(encoded[:middle]), self._score_batch(encoded[middle:])])

    def _forward_batch(self, encoded: list[list[int]]) -> np.ndarray:
        features = self.tokenizer.pad(
            [{"input_ids": ids, "attention_mask": [1] * len(ids)} for ids in encoded],
            padding=True,
            return_tensors="pt",
        )
        features = {key: value.to(self.model.device) for key, value in features.items()}
        features.update(logits_to_keep=1, use_cache=False)
        return self.model.forward(features)["scores"].detach().float().cpu().numpy().reshape(-1)

    def metadata(self) -> dict[str, Any]:
        return {
            "backend_library": "sentence-transformers",
            "compatibility": "mxbai_v2_preserve_relevance_suffix",
            "max_batch_tokens": self.max_batch_tokens,
            "max_seq_length": self.max_seq_length,
            "query_token_budget": self._query_budget,
            "suffix_tokens": len(self._suffix_ids),
            "logits_to_keep": 1,
            "use_cache": False,
            "oom_retries": self.oom_retries,
            "truncated_pairs": self.truncated_pairs,
            "truncated_queries": self.truncated_queries,
        }


def load_mxbai_rerank_v2(config: ModelLoadConfig) -> MxbaiRerankV2Adapter:
    """Load the native CrossEncoder with safe long-input preprocessing."""
    from hakari_bench.models import load_model

    if config.model_type != "reranker":
        raise ValueError("load_mxbai_rerank_v2 supports reranker evaluation only.")
    kwargs = dict(config.model_loader_kwargs or {})
    max_batch_tokens = int(kwargs.pop("max_batch_tokens", 131072))
    if kwargs:
        raise ValueError(f"Unsupported mxbai-rerank-v2 loader kwargs: {', '.join(sorted(kwargs))}")
    model = load_model(replace(config, model_loader=None, model_loader_kwargs=None))
    return MxbaiRerankV2Adapter(model, max_batch_tokens=max_batch_tokens)
