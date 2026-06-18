from __future__ import annotations

import asyncio
import importlib
import importlib.metadata
import inspect
import os
import platform
import string
import sys
from dataclasses import dataclass
from functools import lru_cache
from pathlib import Path
from threading import Thread
from typing import Any

import numpy as np
import torch

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
