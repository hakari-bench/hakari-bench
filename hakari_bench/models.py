from __future__ import annotations

import asyncio
import copy
import hashlib
import importlib
import importlib.metadata
import inspect
import math
import os
import platform
import string
import sys
from concurrent.futures import ThreadPoolExecutor
from dataclasses import dataclass
from functools import lru_cache
from pathlib import Path
from threading import Lock, Thread
from typing import Any

import numpy as np
import orjson
import torch
import urllib3

from hakari_bench.model_protocols import validate_model_capabilities

try:
    HfApi: Any = getattr(importlib.import_module("huggingface_hub"), "HfApi")
except Exception:  # pragma: no cover
    HfApi = None


@dataclass(frozen=True)
class ModelLoadConfig:
    model_name_or_path: str
    model_type: str = "dense"
    model_loader: str | None = None
    model_loader_kwargs: dict[str, Any] | None = None
    model_revision: str | None = None
    dtype: str = "bf16"
    attn_implementation: str | None = None
    flash_attn2: bool = False
    device: str | None = None
    trust_remote_code: bool = False
    max_seq_length: int | None = None
    cross_encoder_kwargs: dict[str, Any] | None = None
    late_interaction_query_length: int | None = None
    late_interaction_document_length: int | None = None
    late_interaction_query_prefix: str | None = None
    late_interaction_document_prefix: str | None = None
    late_interaction_do_query_expansion: bool | None = None
    late_interaction_attend_to_expansion_tokens: bool | None = None


def resolve_torch_dtype(dtype: str) -> torch.dtype:
    if dtype == "bf16":
        return torch.bfloat16
    if dtype == "fp16":
        return torch.float16
    if dtype == "fp32":
        return torch.float32
    raise ValueError(f"Unsupported dtype: {dtype}")


def resolve_attn_implementation(*, attn_implementation: str | None, flash_attn2: bool) -> str | None:
    if flash_attn2:
        if attn_implementation is not None and attn_implementation != "flash_attention_2":
            raise ValueError("Both --flash-attn2 and --attn-implementation were provided with conflicting values.")
        return "flash_attention_2"
    return attn_implementation


def _model_kwargs(config: ModelLoadConfig) -> dict[str, Any]:
    kwargs: dict[str, Any] = {"torch_dtype": resolve_torch_dtype(config.dtype)}
    attn_implementation = resolve_attn_implementation(
        attn_implementation=config.attn_implementation,
        flash_attn2=config.flash_attn2,
    )
    if attn_implementation is not None:
        kwargs["attn_implementation"] = attn_implementation
    return kwargs


@lru_cache(maxsize=512)
def resolve_model_revision(model_id: str, requested_revision: str | None = None) -> dict[str, Any]:
    payload: dict[str, Any] = {
        "requested": requested_revision,
        "resolved": None,
        "source": "huggingface_hub",
    }
    if HfApi is None:
        payload["error"] = "huggingface_hub is not installed."
        return payload
    try:
        info = HfApi().model_info(repo_id=model_id, revision=requested_revision)
    except Exception as exc:
        payload["error"] = f"{type(exc).__name__}: {exc}"
        return payload

    sha = getattr(info, "sha", None)
    if sha is None:
        payload["error"] = "Model revision SHA was not returned by Hugging Face Hub."
    else:
        payload["resolved"] = str(sha)
    return payload


def _import_sentence_transformer() -> Any:
    return getattr(importlib.import_module("sentence_transformers"), "SentenceTransformer")


def _import_sparse_encoder() -> Any:
    return getattr(importlib.import_module("sentence_transformers.sparse_encoder"), "SparseEncoder")


def _import_cross_encoder() -> Any:
    return getattr(importlib.import_module("sentence_transformers"), "CrossEncoder")


def _import_pylate_colbert() -> Any:
    return getattr(importlib.import_module("pylate.models"), "ColBERT")


def _patch_pylate_dense_missing_activation_function() -> None:
    try:
        dense_cls = getattr(importlib.import_module("pylate.models"), "Dense")
    except ModuleNotFoundError:
        return
    original = getattr(dense_cls, "from_sentence_transformers", None)
    if original is None or getattr(original, "_hakari_missing_activation_patch", False):
        return

    def from_sentence_transformers(dense: Any) -> Any:
        try:
            return original(dense)
        except KeyError as exc:
            if exc.args != ("activation_function",):
                raise
        config = getattr(dense, "get_config_dict")()
        config.setdefault("activation_function", "torch.nn.Identity")
        activation = config["activation_function"]
        if isinstance(activation, str):
            import_from_string = getattr(importlib.import_module("sentence_transformers.util"), "import_from_string")
            config["activation_function"] = import_from_string(activation)()
        model = dense_cls(**config)
        model.load_state_dict(dense.state_dict())
        return model

    setattr(from_sentence_transformers, "_hakari_missing_activation_patch", True)
    dense_cls.from_sentence_transformers = staticmethod(from_sentence_transformers)


def _patch_pylate_text_length_compat(model: Any) -> None:
    """Bridge the SentenceTransformers 5.4 input-length method rename for PyLate."""
    if callable(getattr(model, "_text_length", None)):
        return
    input_length = getattr(model, "_input_length", None)
    if callable(input_length):
        model._text_length = input_length


def _import_auto_tokenizer() -> Any:
    return getattr(importlib.import_module("transformers"), "AutoTokenizer")


def _import_auto_model() -> Any:
    return getattr(importlib.import_module("transformers"), "AutoModel")


class ColbertLateInteractionAdapter(torch.nn.Module):
    similarity_fn_name = "dot"

    def __init__(
        self,
        *,
        model_name_or_path: str,
        tokenizer: Any,
        backbone: torch.nn.Module,
        projection: torch.nn.Module | None,
        device: str | None,
        query_prefix: str | None = None,
        document_prefix: str | None = None,
        query_length: int | None = None,
        document_length: int | None = None,
        do_query_expansion: bool | None = None,
        attend_to_expansion_tokens: bool | None = None,
    ) -> None:
        super().__init__()
        self.model_name_or_path = model_name_or_path
        self.tokenizer = tokenizer
        self.backbone = backbone
        self.projection = projection
        self.query_prefix = "[unused0]" if query_prefix is None else query_prefix
        self.document_prefix = "[unused1]" if document_prefix is None else document_prefix
        self.query_prefix_id = _late_interaction_prefix_id(tokenizer, self.query_prefix)
        self.document_prefix_id = _late_interaction_prefix_id(tokenizer, self.document_prefix)
        self.query_length = query_length or 32
        self.document_length = document_length or 180
        self.do_query_expansion = True if do_query_expansion is None else do_query_expansion
        self.attend_to_expansion_tokens = False if attend_to_expansion_tokens is None else attend_to_expansion_tokens
        if not self.do_query_expansion:
            self.attend_to_expansion_tokens = False
        mask_token_id = getattr(tokenizer, "mask_token_id", None)
        if mask_token_id is not None:
            tokenizer.pad_token_id = mask_token_id
        self.skiplist = [
            token_id
            for token_id in (_convert_token_to_id(tokenizer, token) for token in string.punctuation)
            if isinstance(token_id, int) and token_id >= 0
        ]
        self.max_seq_length = document_length or _tokenizer_default_max_length(tokenizer)
        self._target_device = torch.device(device) if device is not None else _first_module_device(self)
        if device is not None:
            self.to(self._target_device)

    @classmethod
    def from_pretrained(
        cls,
        model_name_or_path: str,
        *,
        device: str | None,
        revision: str | None,
        trust_remote_code: bool,
        model_kwargs: dict[str, Any],
        query_prefix: str | None = None,
        document_prefix: str | None = None,
        query_length: int | None = None,
        document_length: int | None = None,
        do_query_expansion: bool | None = None,
        attend_to_expansion_tokens: bool | None = None,
    ) -> ColbertLateInteractionAdapter:
        tokenizer = _import_auto_tokenizer().from_pretrained(
            model_name_or_path,
            revision=revision,
            trust_remote_code=trust_remote_code,
        )
        backbone = _import_auto_model().from_pretrained(
            model_name_or_path,
            revision=revision,
            trust_remote_code=trust_remote_code,
            **model_kwargs,
        )
        projection = _load_colbert_projection_from_hub(
            model_name_or_path,
            revision=revision,
            device=torch.device(device) if device is not None else None,
            dtype=model_kwargs.get("torch_dtype"),
        )
        return cls(
            model_name_or_path=model_name_or_path,
            tokenizer=tokenizer,
            backbone=backbone,
            projection=projection,
            device=device,
            query_prefix=query_prefix,
            document_prefix=document_prefix,
            query_length=query_length,
            document_length=document_length,
            do_query_expansion=do_query_expansion,
            attend_to_expansion_tokens=attend_to_expansion_tokens,
        )

    @property
    def device(self) -> torch.device:
        return _first_module_device(self) or self._target_device or torch.device("cpu")

    def encode(
        self,
        inputs: list[str] | str,
        *,
        batch_size: int = 32,
        show_progress_bar: bool | None = None,
        convert_to_numpy: bool = True,
        convert_to_tensor: bool = False,
        is_query: bool = True,
        **kwargs: Any,
    ) -> Any:
        return self._encode_with_role(
            inputs,
            prefix_id=self.query_prefix_id if is_query else self.document_prefix_id,
            max_length=self.query_length if is_query else self.document_length,
            is_query=is_query,
            batch_size=batch_size,
            show_progress_bar=show_progress_bar,
            convert_to_numpy=convert_to_numpy,
            convert_to_tensor=convert_to_tensor,
            **kwargs,
        )

    def encode_query(self, inputs: list[str] | str, **kwargs: Any) -> torch.Tensor | Any:
        return self._encode_with_role(
            inputs,
            prefix_id=self.query_prefix_id,
            max_length=self.query_length,
            is_query=True,
            **kwargs,
        )

    def encode_document(self, inputs: list[str] | str, **kwargs: Any) -> torch.Tensor | Any:
        return self._encode_with_role(
            inputs,
            prefix_id=self.document_prefix_id,
            max_length=self.document_length,
            is_query=False,
            **kwargs,
        )

    def _encode_with_role(
        self,
        inputs: list[str] | str,
        *,
        prefix_id: int | None,
        max_length: int | None,
        is_query: bool,
        batch_size: int = 32,
        show_progress_bar: bool | None = None,
        convert_to_numpy: bool = True,
        convert_to_tensor: bool = False,
        **_: Any,
    ) -> Any:
        del show_progress_bar
        input_was_string = isinstance(inputs, str)
        sentences = [inputs] if isinstance(inputs, str) else list(inputs)
        embeddings: list[torch.Tensor] = []
        for start in range(0, len(sentences), batch_size):
            embeddings.extend(
                self._encode_batch(
                    sentences[start : start + batch_size],
                    max_length=max_length,
                    prefix_id=prefix_id,
                    is_query=is_query,
                )
            )
        if convert_to_numpy and not convert_to_tensor:
            result: Any = [embedding.detach().cpu().float().numpy() for embedding in embeddings]
        else:
            result = embeddings
        return result[0] if input_was_string else result

    def _encode_batch(
        self,
        sentences: list[str],
        *,
        max_length: int | None = None,
        prefix_id: int | None = None,
        is_query: bool = True,
    ) -> list[torch.Tensor]:
        tokenizer_kwargs: dict[str, Any] = {
            "truncation": True,
            "return_tensors": "pt",
        }
        resolved_max_length = max_length or self.max_seq_length
        if resolved_max_length is not None:
            tokenizer_kwargs["max_length"] = resolved_max_length - 1 if prefix_id is not None else resolved_max_length
        if is_query and self.do_query_expansion:
            tokenizer_kwargs["padding"] = "max_length"
        else:
            tokenizer_kwargs["padding"] = True
        tokenized = self.tokenizer(sentences, **tokenizer_kwargs)
        if prefix_id is not None:
            tokenized["input_ids"] = _insert_late_interaction_prefix_token(tokenized["input_ids"], prefix_id)
            tokenized["attention_mask"] = _insert_late_interaction_prefix_token(tokenized["attention_mask"], 1)
            if "token_type_ids" in tokenized:
                tokenized["token_type_ids"] = _insert_late_interaction_prefix_token(tokenized["token_type_ids"], 0)
        if is_query and self.attend_to_expansion_tokens:
            tokenized["attention_mask"].fill_(1)
        tokenized = {
            key: value.to(self.device) if isinstance(value, torch.Tensor) else value for key, value in tokenized.items()
        }
        with torch.inference_mode():
            outputs = self.backbone(**tokenized)
            token_embeddings = _last_hidden_state(outputs)
            if self.projection is not None:
                token_embeddings = self.projection(token_embeddings)
            token_embeddings = torch.nn.functional.normalize(token_embeddings.float(), p=2, dim=-1)
        attention_mask = tokenized.get("attention_mask")
        input_ids = tokenized.get("input_ids")
        if not isinstance(attention_mask, torch.Tensor) or not isinstance(input_ids, torch.Tensor):
            return [embedding for embedding in token_embeddings]
        if is_query and self.do_query_expansion:
            masks = torch.ones_like(input_ids, dtype=torch.bool)
        else:
            masks = attention_mask.bool()
            if not is_query and self.skiplist:
                masks = torch.logical_and(masks, _skiplist_mask(input_ids, self.skiplist))
        return [embedding[mask] for embedding, mask in zip(token_embeddings, masks)]

    def _output_dim(self) -> int:
        if isinstance(self.projection, torch.nn.Linear):
            return int(self.projection.out_features)
        config = getattr(self.backbone, "config", None)
        hidden_size = getattr(config, "hidden_size", None)
        if hidden_size is not None:
            return int(hidden_size)
        return 0


class OpenAIEmbeddingAdapter:
    similarity_fn_name = "cosine"
    max_seq_length = 8100

    _BASE_DIMENSIONS = {
        "text-embedding-3-small": 1536,
        "text-embedding-3-large": 3072,
    }

    def __init__(
        self,
        *,
        model_name: str,
        api_key_env: str = "OPENAI_API_KEY",
        dotenv_path: str | None = ".env",
        load_dotenv: bool = True,
        base_url: str | None = None,
        organization: str | None = None,
        project: str | None = None,
        timeout: float | None = None,
        max_retries: int | None = None,
        max_input_tokens: int = 8100,
        truncate_input_tokens: bool = True,
        max_request_tokens: int = 290_000,
        max_concurrency: int = 4,
        encoding_model: str | None = None,
    ) -> None:
        if max_input_tokens <= 0:
            raise ValueError("OpenAI max_input_tokens must be positive.")
        if max_request_tokens <= 0:
            raise ValueError("OpenAI max_request_tokens must be positive.")
        if max_concurrency <= 0:
            raise ValueError("OpenAI max_concurrency must be positive.")
        self.model_name_or_path = model_name
        self.model_name = model_name
        self.api_key_env = api_key_env
        self.dotenv_path = dotenv_path
        self.load_dotenv = load_dotenv
        self.base_url = base_url
        self.organization = organization
        self.project = project
        self.timeout = timeout
        self.max_retries = max_retries
        self.max_seq_length = int(max_input_tokens)
        self.truncate_input_tokens = bool(truncate_input_tokens)
        self.max_request_tokens = int(max_request_tokens)
        self.max_concurrency = int(max_concurrency)
        self.encoding_model = encoding_model or model_name
        self.default_prompt_name = None
        self.prompts = None
        self._encoding: Any | None = None

    @property
    def base_dimensions(self) -> int | None:
        return self._BASE_DIMENSIONS.get(self.model_name)

    def encode_query(self, sentences: list[str] | str, **kwargs: Any) -> Any:
        return self.encode(sentences, **kwargs)

    def encode_document(self, sentences: list[str] | str, **kwargs: Any) -> Any:
        return self.encode(sentences, **kwargs)

    def encode(
        self,
        sentences: list[str] | str,
        *,
        batch_size: int = 32,
        show_progress_bar: bool | None = None,
        convert_to_numpy: bool = True,
        convert_to_tensor: bool = False,
        truncate_dim: int | None = None,
        dimensions: int | None = None,
        prompt: str | None = None,
        prompt_name: str | None = None,
        task: str | None = None,
        **_: Any,
    ) -> Any:
        return _run_async_from_sync(
            self.aencode(
                sentences,
                batch_size=batch_size,
                show_progress_bar=show_progress_bar,
                convert_to_numpy=convert_to_numpy,
                convert_to_tensor=convert_to_tensor,
                truncate_dim=truncate_dim,
                dimensions=dimensions,
                prompt=prompt,
                prompt_name=prompt_name,
                task=task,
            )
        )

    async def aencode_query(self, sentences: list[str] | str, **kwargs: Any) -> Any:
        return await self.aencode(sentences, **kwargs)

    async def aencode_document(self, sentences: list[str] | str, **kwargs: Any) -> Any:
        return await self.aencode(sentences, **kwargs)

    async def aencode(
        self,
        sentences: list[str] | str,
        *,
        batch_size: int = 32,
        show_progress_bar: bool | None = None,
        convert_to_numpy: bool = True,
        convert_to_tensor: bool = False,
        truncate_dim: int | None = None,
        dimensions: int | None = None,
        prompt: str | None = None,
        prompt_name: str | None = None,
        task: str | None = None,
        **_: Any,
    ) -> Any:
        del task
        if batch_size <= 0:
            raise ValueError("OpenAI embedding batch_size must be positive.")
        if prompt_name is not None:
            raise ValueError("OpenAI embedding adapter does not support prompt_name; pass an explicit prompt string.")
        requested_dimensions = dimensions if dimensions is not None else truncate_dim
        self._validate_dimensions(requested_dimensions)

        input_was_string = isinstance(sentences, str)
        raw_texts = [sentences] if input_was_string else list(sentences)
        texts = [str(sentence) for sentence in raw_texts]
        if prompt is not None:
            texts = [f"{prompt}{text}" for text in texts]

        prepared = self._prepare_inputs(texts)
        ranges = list(self._request_ranges(prepared, batch_size=batch_size))
        vectors = await self._fetch_embedding_batches(
            prepared=prepared,
            ranges=ranges,
            show_progress_bar=bool(show_progress_bar),
        )

        array = np.asarray(vectors, dtype=np.float32)
        if requested_dimensions is not None:
            array = _truncate_and_l2_normalize_array(array, dim=requested_dimensions)
        if convert_to_tensor:
            result: Any = torch.as_tensor(array)
        elif convert_to_numpy:
            result = array
        else:
            result = array.tolist()
        return result[0] if input_was_string else result

    def metadata(self) -> dict[str, Any]:
        return {
            "backend_library": "openai",
            "provider": "openai",
            "api_endpoint": "/v1/embeddings",
            "model": self.model_name,
            "base_dimensions": self.base_dimensions,
            "max_input_tokens": self.max_seq_length,
            "truncate_input_tokens": self.truncate_input_tokens,
            "max_request_tokens": self.max_request_tokens,
            "max_concurrency": self.max_concurrency,
            "encoding_model": self.encoding_model,
            "dimension_reduction": "full_embedding_prefix_l2_normalize",
            "dotenv_path": self.dotenv_path if self.load_dotenv else None,
            "api_key_env": self.api_key_env,
            "base_url": self.base_url,
            "organization": self.organization,
            "project": self.project,
        }

    async def _fetch_embedding_batches(
        self,
        *,
        prepared: list[tuple[str, int]],
        ranges: list[tuple[int, int]],
        show_progress_bar: bool,
    ) -> list[list[float]]:
        if not ranges:
            return []
        client = self._async_client()
        semaphore = asyncio.Semaphore(self.max_concurrency)
        progress = None
        if show_progress_bar:
            tqdm = getattr(importlib.import_module("tqdm.auto"), "tqdm")
            progress = tqdm(total=len(ranges), desc="OpenAI embedding batches")
        try:
            tasks = [
                asyncio.create_task(
                    self._fetch_embedding_batch(
                        client=client,
                        semaphore=semaphore,
                        prepared=prepared,
                        start=start,
                        end=end,
                    )
                )
                for start, end in ranges
            ]
            batches_by_start: dict[int, list[list[float]]] = {}
            for task in asyncio.as_completed(tasks):
                start, vectors = await task
                batches_by_start[start] = vectors
                if progress is not None:
                    progress.update(1)
            ordered_vectors: list[list[float]] = []
            for start, _end in ranges:
                ordered_vectors.extend(batches_by_start[start])
            return ordered_vectors
        finally:
            if progress is not None:
                progress.close()
            close = getattr(client, "close", None)
            if callable(close):
                result = close()
                if inspect.isawaitable(result):
                    await result

    async def _fetch_embedding_batch(
        self,
        *,
        client: Any,
        semaphore: asyncio.Semaphore,
        prepared: list[tuple[str, int]],
        start: int,
        end: int,
    ) -> tuple[int, list[list[float]]]:
        request_kwargs: dict[str, Any] = {
            "model": self.model_name,
            "input": [text for text, _token_count in prepared[start:end]],
        }
        async with semaphore:
            response = await client.embeddings.create(**request_kwargs)
        return start, [list(item.embedding) for item in response.data]

    def _async_client(self) -> Any:
        client_cls = getattr(importlib.import_module("openai"), "AsyncOpenAI")
        return client_cls(**self._client_kwargs())

    def _client_kwargs(self) -> dict[str, Any]:
        if self.load_dotenv and self.dotenv_path:
            _load_dotenv_file(Path(self.dotenv_path))
        kwargs: dict[str, Any] = {}
        api_key = os.environ.get(self.api_key_env)
        if api_key:
            kwargs["api_key"] = api_key
        if self.base_url is not None:
            kwargs["base_url"] = self.base_url
        if self.organization is not None:
            kwargs["organization"] = self.organization
        if self.project is not None:
            kwargs["project"] = self.project
        if self.timeout is not None:
            kwargs["timeout"] = self.timeout
        if self.max_retries is not None:
            kwargs["max_retries"] = self.max_retries
        return kwargs

    def _tokenizer(self) -> Any:
        if self._encoding is not None:
            return self._encoding
        tiktoken = importlib.import_module("tiktoken")
        try:
            self._encoding = tiktoken.encoding_for_model(self.encoding_model)
        except KeyError:
            self._encoding = tiktoken.get_encoding("cl100k_base")
        return self._encoding

    def _prepare_inputs(self, texts: list[str]) -> list[tuple[str, int]]:
        encoding = self._tokenizer()
        prepared: list[tuple[str, int]] = []
        for text in texts:
            tokens = encoding.encode(text, disallowed_special=())
            if len(tokens) > self.max_seq_length:
                if not self.truncate_input_tokens:
                    raise ValueError(
                        f"OpenAI embedding input has {len(tokens)} tokens, exceeding the "
                        f"{self.max_seq_length} token limit for {self.model_name}."
                    )
                tokens = tokens[: self.max_seq_length]
                text = str(encoding.decode(tokens))
            prepared.append((text, len(tokens)))
        return prepared

    def _request_ranges(self, prepared: list[tuple[str, int]], *, batch_size: int) -> list[tuple[int, int]]:
        ranges: list[tuple[int, int]] = []
        start = 0
        while start < len(prepared):
            token_total = 0
            end = start
            while end < len(prepared) and end - start < batch_size:
                next_tokens = prepared[end][1]
                if end > start and token_total + next_tokens > self.max_request_tokens:
                    break
                token_total += next_tokens
                end += 1
            ranges.append((start, end))
            start = end
        return ranges

    def _validate_dimensions(self, dimensions: int | None) -> None:
        if dimensions is None:
            return
        if not isinstance(dimensions, int) or dimensions <= 0:
            raise ValueError("OpenAI embedding dimensions/truncate_dim must be a positive integer.")
        base_dimensions = self.base_dimensions
        if base_dimensions is not None and dimensions > base_dimensions:
            raise ValueError(
                f"OpenAI embedding dimensions={dimensions} exceeds {self.model_name} base dimension {base_dimensions}."
            )


class GeminiEmbeddingAdapter:
    similarity_fn_name = "cosine"
    max_seq_length = 8100
    token_count_offset = 1

    _BASE_DIMENSIONS = {
        "gemini-embedding-2": 3072,
    }

    def __init__(
        self,
        *,
        model_name: str,
        project: str | None = None,
        location: str = "global",
        api_version: str = "v1",
        max_input_tokens: int = 8100,
        truncate_input_tokens: bool = True,
        max_concurrency: int = 4,
        output_dimensionality: int | None = None,
    ) -> None:
        if max_input_tokens <= 0:
            raise ValueError("Gemini max_input_tokens must be positive.")
        if max_concurrency <= 0:
            raise ValueError("Gemini max_concurrency must be positive.")
        self.model_name_or_path = model_name
        self.model_name = model_name
        self.project = project
        self.location = location
        self.api_version = api_version
        self.max_seq_length = int(max_input_tokens)
        self.truncate_input_tokens = bool(truncate_input_tokens)
        self.max_concurrency = int(max_concurrency)
        self.output_dimensionality = output_dimensionality
        self.default_prompt_name = None
        self.prompts = None
        self._local_tokenizer: Any | None = None
        self._validate_dimensions(output_dimensionality)

    @property
    def base_dimensions(self) -> int | None:
        return self._BASE_DIMENSIONS.get(self.model_name)

    def encode_query(self, sentences: list[str] | str, **kwargs: Any) -> Any:
        return self.encode(sentences, **kwargs)

    def encode_document(self, sentences: list[str] | str, **kwargs: Any) -> Any:
        return self.encode(sentences, **kwargs)

    def encode(
        self,
        sentences: list[str] | str,
        *,
        batch_size: int = 32,
        show_progress_bar: bool | None = None,
        convert_to_numpy: bool = True,
        convert_to_tensor: bool = False,
        truncate_dim: int | None = None,
        dimensions: int | None = None,
        prompt: str | None = None,
        prompt_name: str | None = None,
        task: str | None = None,
        **_: Any,
    ) -> Any:
        return _run_async_from_sync(
            self.aencode(
                sentences,
                batch_size=batch_size,
                show_progress_bar=show_progress_bar,
                convert_to_numpy=convert_to_numpy,
                convert_to_tensor=convert_to_tensor,
                truncate_dim=truncate_dim,
                dimensions=dimensions,
                prompt=prompt,
                prompt_name=prompt_name,
                task=task,
            )
        )

    async def aencode_query(self, sentences: list[str] | str, **kwargs: Any) -> Any:
        return await self.aencode(sentences, **kwargs)

    async def aencode_document(self, sentences: list[str] | str, **kwargs: Any) -> Any:
        return await self.aencode(sentences, **kwargs)

    async def aencode(
        self,
        sentences: list[str] | str,
        *,
        batch_size: int = 32,
        show_progress_bar: bool | None = None,
        convert_to_numpy: bool = True,
        convert_to_tensor: bool = False,
        truncate_dim: int | None = None,
        dimensions: int | None = None,
        prompt: str | None = None,
        prompt_name: str | None = None,
        task: str | None = None,
        **_: Any,
    ) -> Any:
        del task
        if batch_size <= 0:
            raise ValueError("Gemini embedding batch_size must be positive.")
        if prompt_name is not None:
            raise ValueError("Gemini embedding adapter does not support prompt_name; pass an explicit prompt string.")
        requested_dimensions = dimensions if dimensions is not None else truncate_dim
        self._validate_dimensions(requested_dimensions)

        input_was_string = isinstance(sentences, str)
        raw_texts = [sentences] if input_was_string else list(sentences)
        texts = [str(sentence) for sentence in raw_texts]
        if prompt is not None:
            texts = [f"{prompt}{text}" for text in texts]
        prepared = self._prepare_inputs(texts)
        ranges = [(start, start + 1) for start in range(len(prepared))]
        vectors = await self._fetch_embedding_batches(
            prepared=prepared,
            ranges=ranges,
            show_progress_bar=bool(show_progress_bar),
        )

        array = np.asarray(vectors, dtype=np.float32)
        if requested_dimensions is not None:
            array = _truncate_and_l2_normalize_array(array, dim=requested_dimensions)
        if convert_to_tensor:
            result: Any = torch.as_tensor(array)
        elif convert_to_numpy:
            result = array
        else:
            result = array.tolist()
        return result[0] if input_was_string else result

    def metadata(self) -> dict[str, Any]:
        return {
            "backend_library": "google-genai",
            "provider": "gemini",
            "api_endpoint": "models.embed_content",
            "model": self.model_name,
            "base_dimensions": self.base_dimensions,
            "max_input_tokens": self.max_seq_length,
            "truncate_input_tokens": self.truncate_input_tokens,
            "max_concurrency": self.max_concurrency,
            "project": self.project,
            "location": self.location,
            "api_version": self.api_version,
            "output_dimensionality": self.output_dimensionality,
            "dimension_reduction": "full_embedding_prefix_l2_normalize",
            "tokenizer": "gemma2_sentencepiece",
            "token_count_policy": "len(gemma2.encode(text)) + 1",
            "token_count_offset": self.token_count_offset,
        }

    async def _fetch_embedding_batches(
        self,
        *,
        prepared: list[str],
        ranges: list[tuple[int, int]],
        show_progress_bar: bool,
    ) -> list[list[float]]:
        if not ranges:
            return []
        client = self._client()
        semaphore = asyncio.Semaphore(self.max_concurrency)
        progress = None
        if show_progress_bar:
            tqdm = getattr(importlib.import_module("tqdm.auto"), "tqdm")
            progress = tqdm(total=len(ranges), desc="Gemini embedding batches")
        try:
            tasks = [
                asyncio.create_task(
                    self._fetch_embedding_batch(
                        client=client,
                        semaphore=semaphore,
                        prepared=prepared,
                        start=start,
                        end=end,
                    )
                )
                for start, end in ranges
            ]
            batches_by_start: dict[int, list[list[float]]] = {}
            for task in asyncio.as_completed(tasks):
                start, vectors = await task
                batches_by_start[start] = vectors
                if progress is not None:
                    progress.update(1)
            ordered_vectors: list[list[float]] = []
            for start, _end in ranges:
                ordered_vectors.extend(batches_by_start[start])
            return ordered_vectors
        finally:
            if progress is not None:
                progress.close()

    async def _fetch_embedding_batch(
        self,
        *,
        client: Any,
        semaphore: asyncio.Semaphore,
        prepared: list[str],
        start: int,
        end: int,
    ) -> tuple[int, list[list[float]]]:
        async with semaphore:
            response = await asyncio.to_thread(
                client.models.embed_content,
                model=self.model_name,
                contents=self._content_from_text(prepared[start]),
                config=self._embed_config(),
            )
        embeddings = getattr(response, "embeddings", None) or []
        if len(embeddings) != 1:
            raise ValueError(f"Gemini embedding API returned {len(embeddings)} embeddings for one input.")
        return start, [list(embeddings[0].values)]

    def _client(self) -> Any:
        genai = importlib.import_module("google.genai")
        types = importlib.import_module("google.genai.types")
        kwargs: dict[str, Any] = {
            "vertexai": True,
            "location": self.location,
            "http_options": types.HttpOptions(api_version=self.api_version),
        }
        if self.project is not None:
            kwargs["project"] = self.project
        return genai.Client(**kwargs)

    def _embed_config(self) -> Any:
        types = importlib.import_module("google.genai.types")
        kwargs: dict[str, Any] = {"auto_truncate": self.truncate_input_tokens}
        if self.output_dimensionality is not None:
            kwargs["output_dimensionality"] = self.output_dimensionality
        return types.EmbedContentConfig(**kwargs)

    def _content_from_text(self, text: str) -> Any:
        types = importlib.import_module("google.genai.types")
        return types.Content(parts=[types.Part(text=text)], role="user")

    def _prepare_inputs(self, texts: list[str]) -> list[str]:
        tokenizer = self._tokenizer()
        token_budget = max(0, self.max_seq_length - self.token_count_offset)
        prepared: list[str] = []
        for text in texts:
            text = str(text)
            tokens = list(tokenizer.encode(text))
            effective_tokens = len(tokens) + self.token_count_offset
            if effective_tokens > self.max_seq_length:
                if not self.truncate_input_tokens:
                    raise ValueError(
                        f"Gemini embedding input has {effective_tokens} tokens, exceeding the "
                        f"{self.max_seq_length} token limit for {self.model_name}."
                    )
                tokens = tokens[:token_budget]
                text = str(tokenizer.decode(tokens))
            prepared.append(text)
        return prepared

    def _tokenizer(self) -> Any:
        if self._local_tokenizer is None:
            self._local_tokenizer = _gemini_embedding_tokenizer()
        return self._local_tokenizer

    def _validate_dimensions(self, dimensions: int | None) -> None:
        if dimensions is None:
            return
        if not isinstance(dimensions, int) or dimensions <= 0:
            raise ValueError("Gemini embedding dimensions/truncate_dim must be a positive integer.")
        base_dimensions = self.base_dimensions
        if base_dimensions is not None and dimensions > base_dimensions:
            raise ValueError(
                f"Gemini embedding dimensions={dimensions} exceeds {self.model_name} base dimension {base_dimensions}."
            )


@lru_cache
def _gemini_embedding_tokenizer() -> Any:
    try:
        loader = importlib.import_module("google.genai._local_tokenizer_loader")
        return loader.get_sentencepiece("gemma2")
    except Exception as exc:
        raise RuntimeError(
            "Gemini embedding local tokenization requires google-genai with the "
            "Gemma2 SentencePiece tokenizer and sentencepiece installed."
        ) from exc


class TypeSafeMaxTokensError(RuntimeError):
    """The provider rejected the context; it did not report a token count."""


class TypeSafeRerankerAdapter:
    """Noul reranker with one request per pair or one shared state per query.

    Expose only rank: the evaluator's predict path chunks candidates, which
    would silently change the meaning of the listwise experiment.
    """

    INSTRUCTIONS = "Does {document} help answer `query`? Prefer passages with the specific facts needed."
    POINTWISE_INSTRUCTIONS = (
        "Does this candidate document help answer the query? "
        "Prefer passages that contain the specific facts needed."
    )
    CRITERIA = {
        "true": "Contains specific information that answers or is necessary for answering the query",
        "false": "Unrelated, only tangentially related, or lacks the needed facts",
    }
    SPLIT_TOKENIZER = "jhu-clsp/mmBERT-base"
    SPLIT_TOKENIZER_REVISION = "c5955035435e2bf121cde7f3c8863ef52ff35d82"
    SPLIT_TOKENIZER_MAX_LENGTH = 65536
    SPLIT_SHUFFLE_SEED = "hakari-typesafe-listwise-chunk-v1"

    def __init__(
        self,
        *,
        model_name: str,
        mode: str = "listwise",
        max_concurrency: int | None = None,
        timeout: float = 180.0,
        max_retries: int = 8,
        api_key_env: str = "TYPESAFE_API_KEY",
        dotenv_path: str | None = ".env",
        split_state_token_budget: int = 26000,
        split_request_token_budget: int = 48000,
        split_tokenizer_name: str = SPLIT_TOKENIZER,
        split_tokenizer_revision: str | None = None,
        task_instructions: dict[str, str] | None = None,
        document_max_tokens: int | None = 4000,
    ) -> None:
        if mode not in {"pointwise", "listwise"}:
            raise ValueError("TypeSafe mode must be 'pointwise' or 'listwise'.")
        if max_concurrency is None:
            max_concurrency = 4 if mode == "listwise" else 20
        if isinstance(max_concurrency, bool) or not isinstance(max_concurrency, int) or max_concurrency <= 0:
            raise ValueError("TypeSafe max_concurrency must be a positive integer.")
        if isinstance(max_retries, bool) or not isinstance(max_retries, int) or max_retries < 0:
            raise ValueError("TypeSafe max_retries must be a nonnegative integer.")
        if not math.isfinite(timeout) or timeout <= 0:
            raise ValueError("TypeSafe timeout must be positive and finite.")
        if not isinstance(split_tokenizer_name, str) or not split_tokenizer_name.strip():
            raise ValueError("TypeSafe split_tokenizer_name must be a nonempty string.")
        if split_tokenizer_revision is not None and (
            not isinstance(split_tokenizer_revision, str) or not split_tokenizer_revision.strip()
        ):
            raise ValueError("TypeSafe split_tokenizer_revision must be a nonempty string or null.")
        for name, value in (
            ("split_state_token_budget", split_state_token_budget),
            ("split_request_token_budget", split_request_token_budget),
        ):
            if isinstance(value, bool) or not isinstance(value, int) or value <= 0:
                raise ValueError(f"TypeSafe {name} must be a positive integer.")
        if task_instructions is not None and not isinstance(task_instructions, dict):
            raise ValueError("TypeSafe task_instructions must be an object.")
        for key, template in (task_instructions or {}).items():
            if not isinstance(key, str) or not key or not isinstance(template, str) or not template.strip():
                raise ValueError("TypeSafe task instructions require nonempty string keys and values.")
            if "{document}" not in template:
                raise ValueError("TypeSafe task instructions must include {document}.")
            try:
                template.format(document="`documents.doc_0`")
            except (KeyError, ValueError, IndexError, AttributeError) as exc:
                raise ValueError("TypeSafe instruction templates only support {document}.") from exc
        if task_instructions and mode != "listwise":
            raise ValueError("TypeSafe task instructions require listwise mode.")
        if document_max_tokens is not None and (
            isinstance(document_max_tokens, bool) or not isinstance(document_max_tokens, int) or document_max_tokens <= 0
        ):
            raise ValueError("TypeSafe document_max_tokens must be a positive integer or null.")
        self.document_max_tokens = document_max_tokens
        self.task_instructions = dict(task_instructions or {})
        self.instruction_task: str | None = None
        self.instructions_template = self.POINTWISE_INSTRUCTIONS if mode == "pointwise" else self.INSTRUCTIONS
        if dotenv_path:
            _load_dotenv_file(Path(dotenv_path))
        api_key = os.environ.get(api_key_env)
        if not api_key:
            raise ValueError(f"Set {api_key_env} to use the TypeSafe reranker.")
        self.model_name = model_name
        self.mode = mode
        self.max_concurrency = max_concurrency
        self.query_concurrency = max_concurrency if mode == "listwise" else 1
        self._tokenizer_lock = Lock()
        self.timeout = timeout
        self.max_retries = max_retries
        self.split_state_token_budget = split_state_token_budget
        self.split_request_token_budget = split_request_token_budget
        self.split_tokenizer_name = split_tokenizer_name
        self.split_tokenizer_revision = split_tokenizer_revision or (
            self.SPLIT_TOKENIZER_REVISION if split_tokenizer_name == self.SPLIT_TOKENIZER else None
        )
        self._split_tokenizer: Any = None
        self._api_key = api_key
        self._http = urllib3.PoolManager(maxsize=max_concurrency, block=True)
        self._lock = Lock()
        self.reset_task_statistics()

    def configure_task(self, full_task_name: str) -> None:
        """Select before starting a task's query workers; never match by suffix."""
        self.instruction_task = full_task_name
        default = self.POINTWISE_INSTRUCTIONS if self.mode == "pointwise" else self.INSTRUCTIONS
        self.instructions_template = self.task_instructions.get(full_task_name, default)

    def reset_task_statistics(self) -> None:
        """Called by the result writer before an uncached task."""
        with self._lock:
            self._usage = {"requests": 0, "retries": 0, "input_tokens": 0, "output_tokens": 0, "max_tokens_errors": 0}
            self._resolved_models: set[str] = set()
            self._split_queries: list[dict[str, Any]] = []
            self._rank_calls = 0
            self._truncation_events: list[dict[str, int]] = []

    def metadata(self) -> dict[str, Any]:
        with self._lock:
            return {
                "backend_library": "urllib3",
                "provider": "typesafe",
                "api_endpoint": "https://api.typesafe.ai/v1/systemone",
                "model": self.model_name,
                "mode": self.mode,
                "query_concurrency": self.query_concurrency,
                "primitive": "noul",
                "instructions_template": self.instructions_template,
                "instruction_task": self.instruction_task,
                "instruction_source": "task_override" if self.instruction_task in self.task_instructions else "default",
                "criteria": dict(self.CRITERIA),
                "max_concurrency": self.max_concurrency,
                "timeout": self.timeout,
                "max_retries": self.max_retries,
                "truncation": "document_token_prefix" if self.document_max_tokens is not None else "none",
                "document_truncation": {
                    "max_tokens": self.document_max_tokens,
                    "tokenizer": self.split_tokenizer_name,
                    "tokenizer_revision": self.split_tokenizer_revision,
                    "side": "right",
                    "scope": "candidate_occurrences_per_task",
                    "truncated_documents": len(self._truncation_events),
                    "events": copy.deepcopy(self._truncation_events),
                },
                "tie_break": "stable_input_order",
                "usage_scope": "task",
                "usage": dict(self._usage),
                "resolved_models": sorted(self._resolved_models),
                "listwise_splitting": {
                    "policy": "estimated_budget_then_halve_on_max_tokens_exceeded",
                    "tokenizer": self.split_tokenizer_name,
                    "tokenizer_revision": self.split_tokenizer_revision,
                    "tokenizer_max_length": self.SPLIT_TOKENIZER_MAX_LENGTH,
                    "estimates_are_provider_tokens": False,
                    "state_token_budget": self.split_state_token_budget,
                    "request_token_budget": self.split_request_token_budget,
                    "retry_budget_factor": 0.5,
                    "chunk_order": "deterministic_hash_shuffle",
                    "shuffle_seed": self.SPLIT_SHUFFLE_SEED,
                    "merge": "raw_noul_descending_stable_original_input_order",
                    "queries": copy.deepcopy(self._split_queries),
                },
            }

    def rank(self, query: str, documents: list[str]) -> list[dict[str, int]]:
        if not documents:
            return []
        with self._lock:
            query_index = self._rank_calls
            self._rank_calls += 1
        documents = self._truncate_documents(documents, query_index=query_index)
        if self.mode == "listwise":
            scores = self._score_listwise(query, documents, query_index=query_index)
        else:
            def score_document(document: str) -> float:
                return self._request(
                    state={"query": query, "document": document},
                    references={"relevant": "`document`"},
                )[0]

            with ThreadPoolExecutor(max_workers=self.max_concurrency) as executor:
                # map preserves input order regardless of network completion.
                scores = list(executor.map(score_document, documents))
        order = sorted(range(len(documents)), key=lambda index: -scores[index])
        # Return ordered indices without scores so the generic rank parser
        # preserves our tie order instead of re-sorting ties by corpus ID.
        return [{"corpus_id": index} for index in order]

    def _get_split_tokenizer(self) -> Any:
        # Caller holds _tokenizer_lock (tokenizer configuration is mutable).
        if self._split_tokenizer is None:
            self._split_tokenizer = _import_auto_tokenizer().from_pretrained(
                self.split_tokenizer_name, revision=self.split_tokenizer_revision,
                model_max_length=self.SPLIT_TOKENIZER_MAX_LENGTH, trust_remote_code=False,
            )
            self._split_tokenizer.model_max_length = self.SPLIT_TOKENIZER_MAX_LENGTH
        return self._split_tokenizer

    def _split_token_length(self, text: str) -> int:
        with self._tokenizer_lock:
            return len(self._get_split_tokenizer().encode(text, add_special_tokens=False, truncation=False, verbose=False))

    def _truncate_documents(self, documents: list[str], *, query_index: int) -> list[str]:
        if self.document_max_tokens is None:
            return documents
        prepared = []
        events = []
        for index, text in enumerate(documents):
            with self._tokenizer_lock:
                tokenizer = self._get_split_tokenizer()
                tokens = tokenizer.encode(text, add_special_tokens=False, truncation=False, verbose=False)
                original_tokens = len(tokens)
                if original_tokens > self.document_max_tokens:
                    tokens = tokens[:self.document_max_tokens]
                    while True:
                        text = tokenizer.decode(tokens, skip_special_tokens=True, clean_up_tokenization_spaces=False)
                        sent_tokens = len(tokenizer.encode(text, add_special_tokens=False, truncation=False, verbose=False))
                        if sent_tokens <= self.document_max_tokens:
                            break
                        # Decoding/re-encoding can change token boundaries.
                        tokens = tokens[:max(0, len(tokens) - max(1, sent_tokens - self.document_max_tokens))]
                    events.append({
                        "query_index": query_index, "document_index": index,
                        "original_tokens": original_tokens, "sent_tokens": sent_tokens,
                    })
                prepared.append(text)
        if events:
            with self._lock:
                self._truncation_events.extend(events)
            print(
                f"TypeSafe query {query_index}: truncated {len(events)} documents to "
                f"at most {self.document_max_tokens} {self.split_tokenizer_name} tokens.",
                file=sys.stderr,
            )
        return prepared

    def _estimate_listwise_tokens(self, query: str, indices: list[int], lengths: list[int]) -> dict[str, int]:
        # Count document bodies once and estimate JSON/question scaffolding.
        # These counts are a heuristic, not the provider's tokenization.
        state = {"query": query, "documents": {f"doc_{i}": "" for i in indices}}
        state_tokens = self._split_token_length(orjson.dumps(state).decode()) + sum(lengths[i] for i in indices)
        questions = [self._noul_question(f"`documents.doc_{i}`") for i in indices]
        question_lengths = [self._split_token_length(orjson.dumps(question).decode()) for question in questions]
        return {
            "state_plus_longest_question": state_tokens + max(question_lengths),
            "request": state_tokens + sum(question_lengths),
        }

    @staticmethod
    def _balanced_document_chunks(indices: list[int], lengths: list[int], count: int) -> list[list[int]]:
        base, remainder = divmod(len(indices), count)
        capacities = [base + (i >= count - remainder) for i in range(count)]
        chunks: list[list[int]] = [[] for _ in range(count)]
        totals = [0] * count
        # Longest first, then lowest current token load, under balanced count
        # quotas. Sorting each chunk restores the original candidate order.
        for index in sorted(indices, key=lambda i: (-lengths[i], i)):
            target = min(
                (i for i in range(count) if len(chunks[i]) < capacities[i]),
                key=lambda i: (totals[i], len(chunks[i]), i),
            )
            chunks[target].append(index)
            totals[target] += lengths[index]
        return [sorted(chunk) for chunk in chunks]

    def _shuffle_chunk(self, indices: list[int], query: str) -> list[int]:
        # Independent of document lengths and chunk-processing order. Original
        # indices remain the identity used to map every returned score back.
        query_hash = hashlib.sha256(query.encode()).hexdigest()
        return sorted(indices, key=lambda i: hashlib.sha256(
            f"{self.SPLIT_SHUFFLE_SEED}:{query_hash}:{i}".encode(),
        ).digest())

    def _score_listwise(self, query: str, documents: list[str], *, query_index: int) -> list[float]:
        scores = [0.0] * len(documents)
        lengths = [self._split_token_length(document) for document in documents]
        trace: dict[str, Any] | None = None

        def ensure_trace() -> dict[str, Any]:
            nonlocal trace
            if trace is None:
                trace = dict[str, Any](
                    query_index=query_index,
                    query_sha256=hashlib.sha256(query.encode()).hexdigest(),
                    original_document_count=len(documents), document_token_lengths=lengths,
                    events=[], final_chunks=[], status="running",
                )
                with self._lock:
                    self._split_queries.append(trace)
            return trace

        def fits(estimate: dict[str, int], state_budget: int, request_budget: int) -> bool:
            return (
                estimate["state_plus_longest_question"] <= state_budget
                and estimate["request"] <= request_budget
            )

        def split_chunk(
            indices: list[int], depth: int, state_budget: int, request_budget: int, reason: str,
        ) -> None:
            current_trace = ensure_trace()
            estimate = self._estimate_listwise_tokens(query, indices, lengths)
            if len(indices) == 1:
                current_trace["unsplittable_document_index"] = indices[0]
                raise TypeSafeMaxTokensError(
                    f"TypeSafe {reason} for a single document (index {indices[0]}) and query; "
                    f"estimated tokens {estimate} exceed the available context or budget "
                    f"({state_budget}/{request_budget}). Cannot split further after configured document preprocessing."
                )
            count = min(len(indices), max(
                2, math.ceil(estimate["state_plus_longest_question"] / state_budget),
                math.ceil(estimate["request"] / request_budget),
            ))
            # Check each child, because query and question overhead is repeated
            # and average length alone cannot guarantee a per-request budget.
            while True:
                chunks = [self._shuffle_chunk(chunk, query) for chunk in
                          self._balanced_document_chunks(indices, lengths, count)]
                estimates = [self._estimate_listwise_tokens(query, chunk, lengths) for chunk in chunks]
                if all(fits(value, state_budget, request_budget) for value in estimates) or count == len(indices):
                    break
                count += 1
            event = {
                "reason": reason, "error_type": reason if reason == "max_tokens_exceeded" else None,
                "depth": depth, "document_indices": indices, "estimated_tokens": estimate,
                "state_token_budget": state_budget, "request_token_budget": request_budget,
                "chunk_document_counts": [len(chunk) for chunk in chunks],
                "chunk_document_indices": chunks, "chunk_estimated_tokens": estimates,
            }
            current_trace["events"].append(event)
            print(
                f"TypeSafe listwise query {query_index}: {reason}; "
                f"splitting {len(indices)} documents into {event['chunk_document_counts']} "
                f"using {self.split_tokenizer_name} estimates, budgets "
                f"{state_budget}/{request_budget} (depth {depth}).",
                file=sys.stderr,
            )
            for chunk in chunks:
                score_chunk(chunk, depth + 1, state_budget, request_budget)

        def score_chunk(indices: list[int], depth: int, state_budget: int, request_budget: int) -> None:
            estimate = self._estimate_listwise_tokens(query, indices, lengths)
            if not fits(estimate, state_budget, request_budget):
                split_chunk(indices, depth, state_budget, request_budget, "estimated_token_budget")
                return
            keyed_documents = {f"doc_{i}": documents[i] for i in indices}
            try:
                chunk_scores = self._request(
                    state={"query": query, "documents": keyed_documents},
                    references={key: f"`documents.{key}`" for key in keyed_documents},
                )
            except TypeSafeMaxTokensError:
                split_chunk(indices, depth, max(1, state_budget // 2), max(1, request_budget // 2),
                            "max_tokens_exceeded")
                return
            for index, score in zip(indices, chunk_scores, strict=True):
                scores[index] = score
            if trace is not None:
                trace["final_chunks"].append({
                    "document_indices": indices, "depth": depth, "estimated_tokens": estimate,
                    "state_token_budget": state_budget, "request_token_budget": request_budget,
                })

        try:
            score_chunk(list(range(len(documents))), 0, self.split_state_token_budget, self.split_request_token_budget)
        except Exception:
            if trace is not None:
                trace["status"] = "failed"
            raise
        if trace is not None:
            trace["status"] = "merged"
        return scores

    def _noul_question(self, reference: str) -> dict[str, Any]:
        return {
            "type": "noul",
            "instructions": self.instructions_template.format(document=reference),
            "criteria": self.CRITERIA,
        }

    def _request(self, *, state: dict[str, Any], references: dict[str, str]) -> list[float]:
        payload = {
            "model": self.model_name,
            "state": state,
            "questions": {key: self._noul_question(reference) for key, reference in references.items()},
        }
        retries = urllib3.Retry(
            total=self.max_retries,
            allowed_methods=frozenset({"POST"}),
            status_forcelist=(429, 500, 502, 503, 504, 529),
            backoff_factor=0.5,
            backoff_jitter=0.2,
            respect_retry_after_header=True,
            raise_on_status=False,
        )
        response = self._http.request(
            "POST",
            "https://api.typesafe.ai/v1/systemone",
            body=orjson.dumps(payload),
            headers={"Content-Type": "application/json", "Authorization": f"Bearer {self._api_key}"},
            timeout=self.timeout,
            retries=retries,
            redirect=False,
        )
        if response.status != 200:
            try:
                error = orjson.loads(response.data)
            except orjson.JSONDecodeError:
                error = None
            detail = error.get("detail") if isinstance(error, dict) else None
            if response.status in {400, 422} and isinstance(detail, dict) and detail.get("error_type") == "max_tokens_exceeded":
                with self._lock:
                    self._usage["max_tokens_errors"] += 1
                raise TypeSafeMaxTokensError(f"TypeSafe request failed with HTTP {response.status}: max_tokens_exceeded.")
            raise RuntimeError(f"TypeSafe request failed with HTTP {response.status}.")
        try:
            data = orjson.loads(response.data)
        except orjson.JSONDecodeError as exc:
            raise ValueError("TypeSafe returned invalid JSON.") from exc
        if not isinstance(data, dict):
            raise ValueError("TypeSafe response must be an object.")
        answers = data.get("answers")
        if not isinstance(answers, dict) or set(answers) != set(references):
            raise ValueError("TypeSafe Noul answers must match every requested document exactly.")
        scores = []
        for key in references:
            answer = answers[key]
            value = answer.get("noul") if isinstance(answer, dict) else None
            if (
                not isinstance(answer, dict) or answer.get("type") != "noul"
                or isinstance(value, bool) or not isinstance(value, int | float)
                or not math.isfinite(value) or not 0 <= value <= 1
            ):
                raise ValueError(f"TypeSafe returned an invalid Noul answer for {key}.")
            scores.append(float(value))
        resolved_model = data.get("model")
        usage = data.get("usage")
        if not isinstance(resolved_model, str) or not resolved_model or not isinstance(usage, dict):
            raise ValueError("TypeSafe response is missing model or usage metadata.")
        for field in ("input_tokens", "output_tokens"):
            value = usage.get(field)
            if isinstance(value, bool) or not isinstance(value, int) or value < 0:
                raise ValueError(f"TypeSafe response has invalid {field} usage.")
        with self._lock:
            self._resolved_models.add(resolved_model)
            self._usage["requests"] += 1
            self._usage["retries"] += len(getattr(getattr(response, "retries", None), "history", ()))
            self._usage["input_tokens"] += usage["input_tokens"]
            self._usage["output_tokens"] += usage["output_tokens"]
        return scores


def load_typesafe_reranker_model(config: ModelLoadConfig) -> TypeSafeRerankerAdapter:
    if config.model_type != "reranker":
        raise ValueError("The built-in TypeSafe model loader supports evaluate reranker only.")
    if config.max_seq_length is not None:
        raise ValueError("TypeSafe uses document_max_tokens in --model-loader-kwargs-json, not --model-max-seq-length.")
    kwargs = dict(config.model_loader_kwargs or {})
    allowed = {
        "mode", "max_concurrency", "timeout", "max_retries", "api_key_env", "dotenv_path",
        "split_state_token_budget", "split_request_token_budget",
        "split_tokenizer_name", "split_tokenizer_revision", "task_instructions", "document_max_tokens",
    }
    unknown = sorted(set(kwargs) - allowed)
    if unknown:
        raise ValueError(f"Unsupported TypeSafe loader kwargs: {', '.join(unknown)}")
    return TypeSafeRerankerAdapter(model_name=config.model_name_or_path, **kwargs)


def load_openai_embedding_model(config: ModelLoadConfig) -> OpenAIEmbeddingAdapter:
    if config.model_type != "dense":
        raise ValueError("The built-in OpenAI model loader supports evaluate dense only.")
    kwargs = dict(config.model_loader_kwargs or {})
    allowed = {
        "api_key_env",
        "dotenv_path",
        "load_dotenv",
        "base_url",
        "organization",
        "project",
        "timeout",
        "max_retries",
        "max_input_tokens",
        "truncate_input_tokens",
        "max_request_tokens",
        "max_concurrency",
        "encoding_model",
    }
    unknown = sorted(set(kwargs) - allowed)
    if unknown:
        raise ValueError(f"Unsupported OpenAI loader kwargs: {', '.join(unknown)}")
    return OpenAIEmbeddingAdapter(model_name=config.model_name_or_path, **kwargs)


def load_gemini_embedding_model(config: ModelLoadConfig) -> GeminiEmbeddingAdapter:
    if config.model_type != "dense":
        raise ValueError("The built-in Gemini model loader supports evaluate dense only.")
    kwargs = dict(config.model_loader_kwargs or {})
    allowed = {
        "project",
        "location",
        "api_version",
        "max_input_tokens",
        "truncate_input_tokens",
        "max_concurrency",
        "output_dimensionality",
    }
    unknown = sorted(set(kwargs) - allowed)
    if unknown:
        raise ValueError(f"Unsupported Gemini loader kwargs: {', '.join(unknown)}")
    return GeminiEmbeddingAdapter(model_name=config.model_name_or_path, **kwargs)


def load_model(config: ModelLoadConfig) -> Any:
    if config.model_loader is not None:
        model = _load_custom_model(config)
        validate_model_capabilities(model, model_type=config.model_type)
        return model

    model_kwargs = _model_kwargs(config)
    attn_implementation = resolve_attn_implementation(
        attn_implementation=config.attn_implementation,
        flash_attn2=config.flash_attn2,
    )
    if config.model_type == "late-interaction":
        _patch_pylate_dense_missing_activation_function()
        kwargs: dict[str, Any] = {
            "device": config.device,
            "revision": config.model_revision,
            "trust_remote_code": config.trust_remote_code,
            "model_kwargs": model_kwargs,
        }
        if config.late_interaction_query_length is not None:
            kwargs["query_length"] = config.late_interaction_query_length
        if config.late_interaction_document_length is not None:
            kwargs["document_length"] = config.late_interaction_document_length
        if config.late_interaction_query_prefix is not None:
            kwargs["query_prefix"] = config.late_interaction_query_prefix
        if config.late_interaction_document_prefix is not None:
            kwargs["document_prefix"] = config.late_interaction_document_prefix
        if config.late_interaction_do_query_expansion is not None:
            kwargs["do_query_expansion"] = config.late_interaction_do_query_expansion
        if config.late_interaction_attend_to_expansion_tokens is not None:
            kwargs["attend_to_expansion_tokens"] = config.late_interaction_attend_to_expansion_tokens
        try:
            model = _import_pylate_colbert()(config.model_name_or_path, **kwargs)
        except (KeyError, TypeError) as exc:
            if not _is_pylate_sentence_transformers_module_conversion_error(exc):
                raise
            model = ColbertLateInteractionAdapter.from_pretrained(
                config.model_name_or_path,
                device=config.device,
                revision=config.model_revision,
                trust_remote_code=config.trust_remote_code,
                model_kwargs=model_kwargs,
                query_prefix=config.late_interaction_query_prefix,
                document_prefix=config.late_interaction_document_prefix,
                query_length=config.late_interaction_query_length,
                document_length=config.late_interaction_document_length,
                do_query_expansion=config.late_interaction_do_query_expansion,
                attend_to_expansion_tokens=config.late_interaction_attend_to_expansion_tokens,
            )
        _patch_pylate_text_length_compat(model)
        _set_model_dtype(model, config.dtype)
        _set_attn_implementation(model, attn_implementation)
        return model

    if config.model_type == "dense":
        model = _import_sentence_transformer()(
            config.model_name_or_path,
            device=config.device,
            revision=config.model_revision,
            trust_remote_code=config.trust_remote_code,
            model_kwargs=model_kwargs,
        )
        _set_model_dtype(model, config.dtype)
        _set_attn_implementation(model, attn_implementation)
        _set_max_seq_length(model, config.max_seq_length)
        return model

    if config.model_type == "sparse":
        model = _import_sparse_encoder()(
            config.model_name_or_path,
            device=config.device,
            revision=config.model_revision,
            trust_remote_code=config.trust_remote_code,
            model_kwargs=model_kwargs,
        )
        _set_model_dtype(model, config.dtype)
        _set_attn_implementation(model, attn_implementation)
        _set_max_seq_length(model, config.max_seq_length)
        return model

    if config.model_type == "reranker":
        kwargs: dict[str, Any] = dict(config.cross_encoder_kwargs or {})
        extra_model_kwargs = kwargs.pop("model_kwargs", None)
        if extra_model_kwargs is not None:
            if not isinstance(extra_model_kwargs, dict):
                raise ValueError("cross_encoder_kwargs.model_kwargs must be an object.")
            model_kwargs = {**model_kwargs, **extra_model_kwargs}
        kwargs.setdefault("device", config.device)
        kwargs.setdefault("revision", config.model_revision)
        kwargs.setdefault("trust_remote_code", config.trust_remote_code)
        kwargs["model_kwargs"] = model_kwargs
        if config.max_seq_length is not None and "max_length" not in kwargs:
            kwargs["max_length"] = config.max_seq_length
        model = _import_cross_encoder()(config.model_name_or_path, **kwargs)
        _set_model_dtype(model, config.dtype)
        _set_attn_implementation(model, attn_implementation)
        validate_model_capabilities(model, model_type=config.model_type)
        return model

    raise ValueError(f"Unsupported model type: {config.model_type}")


def _load_custom_model(config: ModelLoadConfig) -> Any:
    loader = config.model_loader
    if loader is None:
        raise ValueError("Custom model loader was requested without a loader path.")
    factory = _import_loader_factory(loader)
    return factory(config)


def _import_loader_factory(loader: str) -> Any:
    if loader == "openai":
        return load_openai_embedding_model
    if loader == "gemini":
        return load_gemini_embedding_model
    if loader == "typesafe":
        return load_typesafe_reranker_model
    module_name, separator, attr_name = loader.partition(":")
    if not separator or not module_name or not attr_name:
        raise ValueError("--model-loader must use 'module:function' syntax.")
    module = importlib.import_module(module_name)
    factory = getattr(module, attr_name)
    if not callable(factory):
        raise TypeError(f"Custom model loader {loader!r} is not callable.")
    return factory


def _run_async_from_sync(coro: Any) -> Any:
    try:
        asyncio.get_running_loop()
    except RuntimeError:
        return asyncio.run(coro)

    result: dict[str, Any] = {}
    error: dict[str, BaseException] = {}

    def run_in_thread() -> None:
        try:
            result["value"] = asyncio.run(coro)
        except BaseException as exc:
            error["value"] = exc

    thread = Thread(target=run_in_thread)
    thread.start()
    thread.join()
    if error:
        raise error["value"]
    return result.get("value")


def _truncate_and_l2_normalize_array(array: np.ndarray, *, dim: int) -> np.ndarray:
    if dim <= 0:
        raise ValueError("OpenAI embedding dimensions/truncate_dim must be a positive integer.")
    if array.ndim == 1:
        if dim > array.shape[0]:
            raise ValueError(f"Cannot truncate OpenAI embedding with dimension {array.shape[0]} to {dim}.")
        truncated = array[:dim]
        norm = float(np.linalg.norm(truncated))
        return truncated if norm == 0.0 else (truncated / norm).astype(np.float32, copy=False)
    if array.ndim != 2:
        raise ValueError(f"OpenAI embeddings must be 1D or 2D, got shape {list(array.shape)}.")
    if dim > array.shape[1]:
        raise ValueError(f"Cannot truncate OpenAI embeddings with dimension {array.shape[1]} to {dim}.")
    truncated = array[:, :dim]
    norms = np.linalg.norm(truncated, ord=2, axis=1, keepdims=True)
    return np.divide(
        truncated,
        norms,
        out=np.array(truncated, dtype=np.float32, copy=True),
        where=norms != 0.0,
    )


def _load_dotenv_file(path: Path) -> None:
    path = path.expanduser()
    if not path.exists() or not path.is_file():
        return
    for raw_line in path.read_text(encoding="utf-8").splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#"):
            continue
        if line.startswith("export "):
            line = line[len("export ") :].strip()
        key, separator, value = line.partition("=")
        if not separator:
            continue
        key = key.strip()
        if not key or key in os.environ:
            continue
        value = value.strip()
        if len(value) >= 2 and value[0] == value[-1] and value[0] in {"'", '"'}:
            value = value[1:-1]
        os.environ[key] = value


def _tokenizer_default_max_length(tokenizer: Any) -> int | None:
    model_max_length = getattr(tokenizer, "model_max_length", None)
    if not isinstance(model_max_length, int):
        return None
    if model_max_length > 1_000_000:
        return None
    return model_max_length


def _convert_token_to_id(tokenizer: Any, token: str) -> int | None:
    convert = getattr(tokenizer, "convert_tokens_to_ids", None)
    if not callable(convert):
        return None
    token_id = convert(token)
    return token_id if isinstance(token_id, int) else None


def _late_interaction_prefix_id(tokenizer: Any, prefix: str | None) -> int | None:
    if not prefix:
        return None
    return _convert_token_to_id(tokenizer, prefix)


def _insert_late_interaction_prefix_token(input_ids: torch.Tensor, prefix_id: int) -> torch.Tensor:
    prefix_tensor = torch.full(
        size=(input_ids.size(dim=0), 1),
        fill_value=prefix_id,
        dtype=input_ids.dtype,
        device=input_ids.device,
    )
    return torch.cat((input_ids[:, :1], prefix_tensor, input_ids[:, 1:]), dim=1)


def _skiplist_mask(input_ids: torch.Tensor, skiplist: list[int]) -> torch.Tensor:
    mask = torch.ones_like(input_ids, dtype=torch.bool)
    for token_id in skiplist:
        mask = torch.where(
            input_ids == token_id,
            torch.tensor(False, dtype=torch.bool, device=input_ids.device),
            mask,
        )
    return mask


def _first_module_device(module: torch.nn.Module) -> torch.device | None:
    try:
        parameter = next(module.parameters())
    except StopIteration:
        return None
    return parameter.device


def _last_hidden_state(outputs: Any) -> torch.Tensor:
    hidden = getattr(outputs, "last_hidden_state", None)
    if isinstance(hidden, torch.Tensor):
        return hidden
    if isinstance(outputs, torch.Tensor):
        return outputs
    if isinstance(outputs, (tuple, list)) and outputs and isinstance(outputs[0], torch.Tensor):
        return outputs[0]
    raise ValueError("ColBERT adapter could not find token embeddings in model output.")


def _pad_late_interaction_batches(
    batches: list[torch.Tensor],
    *,
    device: torch.device,
    dim: int,
) -> torch.Tensor:
    if not batches:
        return torch.empty((0, 0, dim), dtype=torch.float32, device=device)
    max_tokens = max(int(batch.shape[1]) for batch in batches)
    padded: list[torch.Tensor] = []
    for batch in batches:
        token_padding = max_tokens - int(batch.shape[1])
        if token_padding > 0:
            batch = torch.nn.functional.pad(batch, (0, 0, 0, token_padding))
        padded.append(batch)
    return torch.cat(padded, dim=0)


def _load_colbert_projection_from_hub(
    model_name_or_path: str,
    *,
    revision: str | None,
    device: torch.device | None,
    dtype: Any,
) -> torch.nn.Linear | None:
    try:
        hf_hub_download = getattr(importlib.import_module("huggingface_hub"), "hf_hub_download")
        safe_open = getattr(importlib.import_module("safetensors.torch"), "safe_open")
        model_path = hf_hub_download(model_name_or_path, "model.safetensors", revision=revision)
        with safe_open(model_path, framework="pt", device="cpu") as tensors:
            keys = set(tensors.keys())
            if "linear.weight" not in keys:
                return None
            weight = tensors.get_tensor("linear.weight")
            bias = tensors.get_tensor("linear.bias") if "linear.bias" in keys else None
    except Exception:
        return None

    projection = torch.nn.Linear(int(weight.shape[1]), int(weight.shape[0]), bias=bias is not None)
    with torch.no_grad():
        projection.weight.copy_(weight)
        if bias is not None and projection.bias is not None:
            projection.bias.copy_(bias)
    if dtype is not None and isinstance(dtype, torch.dtype):
        projection = projection.to(dtype=dtype)
    if device is not None:
        projection = projection.to(device=device)
    return projection


def _is_pylate_sentence_transformers_module_conversion_error(exc: Exception) -> bool:
    if isinstance(exc, KeyError) and exc.args == ("activation_function",):
        return True
    return isinstance(exc, TypeError) and "unexpected keyword argument" in str(exc)


def _set_model_dtype(model: Any, dtype: str) -> None:
    torch_dtype = resolve_torch_dtype(dtype)
    if isinstance(model, torch.nn.Module):
        model.to(dtype=torch_dtype)
        return
    inner_model = getattr(model, "model", None)
    if isinstance(inner_model, torch.nn.Module):
        inner_model.to(dtype=torch_dtype)


def _set_attn_implementation(model: Any, attn_implementation: str | None) -> None:
    if attn_implementation is None:
        return
    modules = model.modules() if isinstance(model, torch.nn.Module) else [model]
    for module in modules:
        config = getattr(module, "config", None)
        if config is None:
            continue
        try:
            setattr(config, "_attn_implementation", attn_implementation)
        except Exception:
            pass
        try:
            setattr(config, "attn_implementation", attn_implementation)
        except Exception:
            pass


def _set_max_seq_length(model: Any, max_seq_length: int | None) -> None:
    if max_seq_length is not None and hasattr(model, "max_seq_length"):
        model.max_seq_length = max_seq_length


def collect_runtime_environment() -> dict[str, Any]:
    return {
        "python": sys.version,
        "platform": platform.platform(),
        "package_versions": {
            package: _version_or_none(package)
            for package in [
                "torch",
                "transformers",
                "sentence-transformers",
                "datasets",
                "numpy",
                "scipy",
                "pylate",
            ]
        },
        "cuda": {
            "is_available": torch.cuda.is_available(),
            "cuda_version": getattr(torch.version, "cuda", None),
            "cudnn_version": torch.backends.cudnn.version() if torch.backends.cudnn.is_available() else None,
            "device_count": torch.cuda.device_count(),
            "devices": [
                {"index": index, "name": torch.cuda.get_device_name(index)}
                for index in range(torch.cuda.device_count())
            ]
            if torch.cuda.is_available()
            else [],
        },
    }


def _version_or_none(package: str) -> str | None:
    try:
        return importlib.metadata.version(package)
    except importlib.metadata.PackageNotFoundError:
        return None


def collect_model_metadata(model: Any, args: Any) -> dict[str, Any]:
    total_parameters, trainable_parameters, embedding_parameters = _parameter_counts(model)
    active_parameters = _active_parameter_count(
        total_parameters=total_parameters,
        embedding_parameters=embedding_parameters,
    )
    source = _model_source_with_revision(
        getattr(args, "model_source", {"type": "huggingface", "name": args.model}),
        requested_revision=getattr(args, "model_revision", None),
    )
    model_loader = getattr(args, "model_loader", None)
    backend_metadata = _custom_model_metadata(model)
    backend_payload = _backend_payload(args)
    payload: dict[str, Any] = {
        "method": args.model_type,
        "id": getattr(args, "model_id", args.model),
        "source": source,
        "device": args.device,
        "dtype": args.dtype,
        "attn_implementation": resolve_attn_implementation(
            attn_implementation=args.attn_implementation,
            flash_attn2=args.flash_attn2,
        ),
        "trust_remote_code": args.trust_remote_code,
        "backend_library": _backend_library_name(args, backend_metadata=backend_metadata),
        "max_seq_length": getattr(model, "max_seq_length", getattr(model, "max_length", None)),
        "similarity_fn_name": str(getattr(model, "similarity_fn_name", "")) or None,
        "prompts": getattr(model, "prompts", None),
        "default_prompt_name": getattr(model, "default_prompt_name", None),
        "total_parameters": total_parameters,
        "trainable_parameters": trainable_parameters,
        "embedding_parameters": embedding_parameters,
        "transformer_parameters": active_parameters,
        "active_parameters": active_parameters,
    }
    if backend_payload:
        payload["backend"] = backend_payload
    if model_loader is not None:
        payload["loader"] = model_loader
    if backend_metadata:
        payload["backend_metadata"] = _redact_sensitive_payload(backend_metadata)
    if backend_metadata.get("provider") == "typesafe":
        # These are provider-controlled and are not reported by the API.
        payload.update(device=None, dtype=None, attn_implementation=None)
    if args.model_type == "late-interaction":
        payload["late_interaction"] = {
            "architecture": "colbert",
            "scoring": "maxsim",
            "query_prefix": getattr(model, "query_prefix", None),
            "document_prefix": getattr(model, "document_prefix", None),
            "query_length": getattr(model, "query_length", None),
            "document_length": getattr(model, "document_length", None),
            "do_query_expansion": getattr(model, "do_query_expansion", None),
            "attend_to_expansion_tokens": getattr(model, "attend_to_expansion_tokens", None),
        }
    return payload


def _backend_library_name(args: Any, *, backend_metadata: dict[str, Any]) -> str:
    backend_library = backend_metadata.get("backend_library")
    if isinstance(backend_library, str) and backend_library:
        return backend_library
    if getattr(args, "model_loader", None) is not None:
        return "custom"
    return "pylate" if args.model_type == "late-interaction" else "sentence-transformers"


def _backend_payload(args: Any) -> dict[str, Any]:
    payload: dict[str, Any] = {
        "loader": getattr(args, "model_loader", None),
        "loader_kwargs": _redact_sensitive_payload(getattr(args, "model_loader_kwargs", {}) or {}),
    }
    if payload["loader"] is None and not payload["loader_kwargs"]:
        return {}
    return payload


def _custom_model_metadata(model: Any) -> dict[str, Any]:
    metadata_fn = getattr(model, "metadata", None)
    if not callable(metadata_fn):
        return {}
    metadata = metadata_fn()
    if not isinstance(metadata, dict):
        raise TypeError("model.metadata() must return a JSON-serializable object mapping.")
    return dict(metadata)


def _redact_sensitive_payload(value: Any) -> Any:
    if isinstance(value, dict):
        return {
            key: "<redacted>" if _is_sensitive_key(str(key)) else _redact_sensitive_payload(item)
            for key, item in value.items()
        }
    if isinstance(value, list):
        return [_redact_sensitive_payload(item) for item in value]
    return value


def _is_sensitive_key(key: str) -> bool:
    normalized = key.lower()
    if any(marker in normalized for marker in ("api_key", "apikey", "secret", "password", "credential")):
        return True
    token_keys = ("token", "access_token", "auth_token", "bearer_token", "api_token")
    return normalized in token_keys or any(normalized.endswith(f"_{token_key}") for token_key in token_keys)


def _model_source_with_revision(source: Any, *, requested_revision: str | None) -> Any:
    if not isinstance(source, dict):
        return source
    payload = dict(source)
    if payload.get("type") != "huggingface":
        return payload
    model_id = payload.get("name")
    if not isinstance(model_id, str) or not model_id:
        return payload
    requested = requested_revision if requested_revision is not None else payload.get("revision_requested")
    if requested is not None:
        payload["revision_requested"] = str(requested)
    elif "/" not in model_id:
        return payload

    revision = resolve_model_revision(model_id, requested_revision=str(requested) if requested is not None else None)
    resolved = revision.get("resolved")
    if resolved is not None:
        payload["revision"] = str(resolved)
    error = revision.get("error")
    if error is not None:
        payload["revision_error"] = str(error)
    return payload


def _parameter_counts(model: Any) -> tuple[int | None, int | None, int | None]:
    named_parameters = _named_parameters(model)
    if named_parameters is None:
        return None, None, None
    total = 0
    trainable = 0
    for name, parameter in named_parameters:
        count = int(parameter.numel())
        total += count
        if parameter.requires_grad:
            trainable += count
    return total, trainable, _embedding_parameter_count(model)


def _active_parameter_count(*, total_parameters: int | None, embedding_parameters: int | None) -> int | None:
    if total_parameters is None or embedding_parameters is None:
        return None
    if embedding_parameters > total_parameters:
        return None
    return total_parameters - embedding_parameters


def _embedding_parameter_count(model: Any) -> int | None:
    embedding = _input_embeddings(model)
    weight = getattr(embedding, "weight", None) if embedding is not None else None
    if weight is None:
        weight = _static_embedding_weight(model)
    if weight is None:
        return None
    if hasattr(weight, "numel"):
        return int(weight.numel())
    shape = getattr(weight, "shape", None)
    if shape is None:
        return None
    count = 1
    for dimension in shape:
        count *= int(dimension)
    return count


def _input_embeddings(model: Any) -> Any | None:
    for source in _input_embedding_sources(model):
        get_input_embeddings = getattr(source, "get_input_embeddings", None)
        if get_input_embeddings is None:
            continue
        try:
            embedding = get_input_embeddings()
        except Exception:
            continue
        if embedding is not None:
            return embedding
    return None


def _input_embedding_sources(model: Any) -> list[Any]:
    sources: list[Any] = []

    first_module = _first_sentence_transformer_module(model)
    if first_module is not None:
        sources.extend(
            source
            for source in [
                getattr(first_module, "auto_model", None),
                getattr(first_module, "model", None),
                first_module,
            ]
            if source is not None
        )

    model_attr = getattr(model, "model", None)
    sources.extend(
        source
        for source in [model_attr, getattr(model_attr, "auto_model", None), model]
        if source is not None
    )
    return sources


def _static_embedding_weight(model: Any) -> Any | None:
    first_module = _first_sentence_transformer_module(model)
    embedding = getattr(first_module, "embedding", None) if first_module is not None else None
    return getattr(embedding, "weight", None) if embedding is not None else None


def _first_sentence_transformer_module(model: Any) -> Any | None:
    try:
        return model[0]
    except Exception:
        return None


def _named_parameters(model: Any) -> list[tuple[str, torch.nn.Parameter]] | None:
    candidate = model
    if not hasattr(candidate, "named_parameters") and hasattr(model, "model"):
        candidate = model.model
    if not hasattr(candidate, "named_parameters"):
        return None
    return list(candidate.named_parameters())
