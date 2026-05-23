from __future__ import annotations

import importlib
import importlib.metadata
import json
import platform
import string
import sys
from dataclasses import dataclass
from functools import lru_cache
from pathlib import Path
from typing import Any

import torch

try:
    HfApi: Any = getattr(importlib.import_module("huggingface_hub"), "HfApi")
except Exception:  # pragma: no cover
    HfApi = None


@dataclass(frozen=True)
class ModelLoadConfig:
    model_name_or_path: str
    model_type: str = "dense"
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


def _can_fallback_to_colbert_adapter(exc: Exception) -> bool:
    return isinstance(exc, KeyError) and exc.args == ("activation_function",)


def _import_auto_tokenizer() -> Any:
    return getattr(importlib.import_module("transformers"), "AutoTokenizer")


def _import_auto_model() -> Any:
    return getattr(importlib.import_module("transformers"), "AutoModel")


def _token_id_or_none(tokenizer: Any, token: str | None) -> int | None:
    if not token:
        return None
    try:
        token_id = tokenizer.convert_tokens_to_ids(token)
    except Exception:
        return None
    unk_token_id = getattr(tokenizer, "unk_token_id", None)
    if token_id is None or token_id == unk_token_id:
        return None
    return int(token_id)


def _insert_prefix_token(tokenized: dict[str, torch.Tensor], prefix_id: int) -> dict[str, torch.Tensor]:
    result = dict(tokenized)
    input_ids = result["input_ids"]
    prefix = torch.full((input_ids.shape[0], 1), int(prefix_id), dtype=input_ids.dtype, device=input_ids.device)
    result["input_ids"] = torch.cat([input_ids[:, :1], prefix, input_ids[:, 1:]], dim=1)
    attention_mask = result.get("attention_mask")
    if isinstance(attention_mask, torch.Tensor):
        attention_prefix = torch.ones(
            (attention_mask.shape[0], 1), dtype=attention_mask.dtype, device=attention_mask.device
        )
        result["attention_mask"] = torch.cat([attention_mask[:, :1], attention_prefix, attention_mask[:, 1:]], dim=1)
    token_type_ids = result.get("token_type_ids")
    if isinstance(token_type_ids, torch.Tensor):
        type_prefix = torch.zeros((token_type_ids.shape[0], 1), dtype=token_type_ids.dtype, device=token_type_ids.device)
        result["token_type_ids"] = torch.cat([token_type_ids[:, :1], type_prefix, token_type_ids[:, 1:]], dim=1)
    return result


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
        do_query_expansion: bool = False,
        attend_to_expansion_tokens: bool = False,
        skiplist_words: list[str] | None = None,
    ) -> None:
        super().__init__()
        self.model_name_or_path = model_name_or_path
        self.tokenizer = tokenizer
        self.backbone = backbone
        self.projection = projection
        self.max_seq_length = _tokenizer_default_max_length(tokenizer)
        self.query_prefix = query_prefix
        self.document_prefix = document_prefix
        self.query_prefix_id = _token_id_or_none(tokenizer, query_prefix)
        self.document_prefix_id = _token_id_or_none(tokenizer, document_prefix)
        self.query_length = query_length or 32
        self.document_length = document_length or self.max_seq_length or 180
        self.do_query_expansion = do_query_expansion
        self.attend_to_expansion_tokens = attend_to_expansion_tokens
        self.skiplist = {
            token_id
            for token_id in (_token_id_or_none(tokenizer, word) for word in (skiplist_words or list(string.punctuation)))
            if token_id is not None
        }
        mask_token_id = getattr(tokenizer, "mask_token_id", None)
        if mask_token_id is not None:
            try:
                tokenizer.pad_token_id = mask_token_id
            except Exception:
                pass
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
        metadata = _load_colbert_metadata_from_hub(model_name_or_path, revision=revision)
        if query_prefix is None:
            query_prefix = _metadata_str(metadata, "query_token_id") or _metadata_str(metadata, "query_token")
        if document_prefix is None:
            document_prefix = _metadata_str(metadata, "doc_token_id") or _metadata_str(metadata, "doc_token")
        if query_length is None:
            query_length = _metadata_int(metadata, "query_maxlen")
        if document_length is None:
            document_length = _metadata_int(metadata, "doc_maxlen")
        if do_query_expansion is None:
            do_query_expansion = bool(metadata.get("do_query_expansion", False))
        if attend_to_expansion_tokens is None:
            attend_to_expansion_tokens = bool(metadata.get("attend_to_mask_tokens", False))
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
        max_length: int | None = None,
        is_query: bool | None = None,
        **_: Any,
    ) -> torch.Tensor | Any:
        del show_progress_bar
        if is_query is not None:
            return self._encode_with_role(
                inputs,
                role="query" if is_query else "document",
                batch_size=batch_size,
                convert_to_numpy=convert_to_numpy,
                convert_to_tensor=convert_to_tensor,
            )
        sentences = [inputs] if isinstance(inputs, str) else list(inputs)
        batches: list[torch.Tensor] = []
        for start in range(0, len(sentences), batch_size):
            batch = self._encode_batch(sentences[start : start + batch_size], max_length=max_length)
            if convert_to_numpy and not convert_to_tensor:
                batch = batch.cpu()
            batches.append(batch)
        result_device = self.device if convert_to_tensor or not convert_to_numpy else torch.device("cpu")
        result = _pad_late_interaction_batches(batches, device=result_device, dim=self._output_dim())
        if convert_to_tensor:
            return result
        if convert_to_numpy:
            return result.detach().cpu().numpy()
        return result

    def encode_query(self, inputs: list[str] | str, **kwargs: Any) -> torch.Tensor | Any:
        return self._encode_with_role(inputs, role="query", **kwargs)

    def encode_document(self, inputs: list[str] | str, **kwargs: Any) -> torch.Tensor | Any:
        return self._encode_with_role(inputs, role="document", **kwargs)

    def _encode_with_role(self, inputs: list[str] | str, *, role: str, **kwargs: Any) -> torch.Tensor | Any:
        input_was_string = isinstance(inputs, str)
        sentences = [inputs] if isinstance(inputs, str) else list(inputs)
        batch_size = int(kwargs.pop("batch_size", 32))
        convert_to_numpy = bool(kwargs.pop("convert_to_numpy", True))
        convert_to_tensor = bool(kwargs.pop("convert_to_tensor", False))
        kwargs.pop("show_progress_bar", None)
        del kwargs

        encoded: list[torch.Tensor] = []
        for start in range(0, len(sentences), batch_size):
            encoded.extend(self._encode_role_batch(sentences[start : start + batch_size], role=role))
        if convert_to_numpy and not convert_to_tensor:
            result: Any = [embedding.detach().cpu().numpy() for embedding in encoded]
        else:
            result = encoded
        return result[0] if input_was_string else result

    def _encode_batch(self, sentences: list[str], *, max_length: int | None = None) -> torch.Tensor:
        tokenizer_kwargs: dict[str, Any] = {
            "padding": True,
            "truncation": True,
            "return_tensors": "pt",
        }
        resolved_max_length = max_length or self.max_seq_length
        if resolved_max_length is not None:
            tokenizer_kwargs["max_length"] = resolved_max_length
        tokenized = self.tokenizer(sentences, **tokenizer_kwargs)
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
        if isinstance(attention_mask, torch.Tensor):
            token_embeddings = token_embeddings * attention_mask.unsqueeze(-1).to(dtype=token_embeddings.dtype)
        return token_embeddings

    def _encode_role_batch(self, sentences: list[str], *, role: str) -> list[torch.Tensor]:
        is_query = role == "query"
        max_length = self.query_length if is_query else self.document_length
        prefix_id = self.query_prefix_id if is_query else self.document_prefix_id
        tokenizer_max_length = max_length - 1 if prefix_id is not None else max_length
        padding: bool | str = "max_length" if is_query and self.do_query_expansion else True
        tokenized = self.tokenizer(
            sentences,
            padding=padding,
            truncation=True,
            max_length=tokenizer_max_length,
            return_tensors="pt",
        )
        if prefix_id is not None:
            tokenized = _insert_prefix_token(tokenized, prefix_id)
        if is_query and self.attend_to_expansion_tokens and isinstance(tokenized.get("attention_mask"), torch.Tensor):
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

        input_ids = tokenized["input_ids"]
        attention_mask = tokenized.get("attention_mask", torch.ones_like(input_ids)).bool()
        if is_query:
            if self.do_query_expansion:
                masks = torch.ones_like(input_ids, dtype=torch.bool)
            else:
                masks = attention_mask
        else:
            skiplist_mask = torch.ones_like(input_ids, dtype=torch.bool)
            for token_id in self.skiplist:
                skiplist_mask &= input_ids != token_id
            masks = attention_mask & skiplist_mask
        return [embedding[mask].detach() for embedding, mask in zip(token_embeddings, masks)]

    def _output_dim(self) -> int:
        if isinstance(self.projection, torch.nn.Linear):
            return int(self.projection.out_features)
        config = getattr(self.backbone, "config", None)
        hidden_size = getattr(config, "hidden_size", None)
        if hidden_size is not None:
            return int(hidden_size)
        return 0


def load_model(config: ModelLoadConfig) -> Any:
    model_kwargs = _model_kwargs(config)
    attn_implementation = resolve_attn_implementation(
        attn_implementation=config.attn_implementation,
        flash_attn2=config.flash_attn2,
    )
    if config.model_type == "late-interaction":
        colbert_config = _load_colbert_sentence_transformers_config(
            config.model_name_or_path,
            revision=config.model_revision,
        )
        query_length = _resolve_late_interaction_int(
            explicit=config.late_interaction_query_length,
            metadata=colbert_config,
            key="query_length",
        )
        document_length = _resolve_late_interaction_int(
            explicit=config.late_interaction_document_length,
            metadata=colbert_config,
            key="document_length",
        )
        query_prefix = _resolve_late_interaction_str(
            explicit=config.late_interaction_query_prefix,
            metadata=colbert_config,
            key="query_prefix",
        )
        document_prefix = _resolve_late_interaction_str(
            explicit=config.late_interaction_document_prefix,
            metadata=colbert_config,
            key="document_prefix",
        )
        do_query_expansion = _resolve_late_interaction_bool(
            explicit=config.late_interaction_do_query_expansion,
            metadata=colbert_config,
            key="do_query_expansion",
        )
        if do_query_expansion is None:
            do_query_expansion = False
        attend_to_expansion_tokens = _resolve_late_interaction_bool(
            explicit=config.late_interaction_attend_to_expansion_tokens,
            metadata=colbert_config,
            key="attend_to_expansion_tokens",
        )
        kwargs: dict[str, Any] = {
            "device": config.device,
            "revision": config.model_revision,
            "trust_remote_code": config.trust_remote_code,
            "model_kwargs": model_kwargs,
        }
        if query_length is not None:
            kwargs["query_length"] = query_length
        if document_length is not None:
            kwargs["document_length"] = document_length
        if query_prefix is not None:
            kwargs["query_prefix"] = query_prefix
        if document_prefix is not None:
            kwargs["document_prefix"] = document_prefix
        kwargs["do_query_expansion"] = do_query_expansion
        if attend_to_expansion_tokens is not None:
            kwargs["attend_to_expansion_tokens"] = attend_to_expansion_tokens
        try:
            model = _import_pylate_colbert()(config.model_name_or_path, **kwargs)
        except Exception as exc:
            if not _can_fallback_to_colbert_adapter(exc):
                raise
            model = ColbertLateInteractionAdapter.from_pretrained(
                config.model_name_or_path,
                device=config.device,
                revision=config.model_revision,
                trust_remote_code=config.trust_remote_code,
                model_kwargs=model_kwargs,
                query_prefix=query_prefix,
                document_prefix=document_prefix,
                query_length=query_length,
                document_length=document_length,
                do_query_expansion=do_query_expansion,
                attend_to_expansion_tokens=attend_to_expansion_tokens,
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
        return model

    raise ValueError(f"Unsupported model type: {config.model_type}")


def _tokenizer_default_max_length(tokenizer: Any) -> int | None:
    model_max_length = getattr(tokenizer, "model_max_length", None)
    if not isinstance(model_max_length, int):
        return None
    if model_max_length > 1_000_000:
        return None
    return model_max_length


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
    revision: str | None = None,
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


def _load_colbert_metadata_from_hub(model_name_or_path: str, *, revision: str | None) -> dict[str, Any]:
    try:
        hf_hub_download = getattr(importlib.import_module("huggingface_hub"), "hf_hub_download")
        metadata_path = hf_hub_download(model_name_or_path, "artifact.metadata", revision=revision)
        with open(metadata_path, encoding="utf-8") as handle:
            payload = json.load(handle)
        return payload if isinstance(payload, dict) else {}
    except Exception:
        return {}


def _load_colbert_sentence_transformers_config(model_name_or_path: str, *, revision: str | None) -> dict[str, Any]:
    local_config = Path(model_name_or_path) / "config_sentence_transformers.json"
    try:
        if local_config.is_file():
            with local_config.open(encoding="utf-8") as handle:
                payload = json.load(handle)
        else:
            hf_hub_download = getattr(importlib.import_module("huggingface_hub"), "hf_hub_download")
            config_path = hf_hub_download(
                model_name_or_path,
                "config_sentence_transformers.json",
                revision=revision,
            )
            with open(config_path, encoding="utf-8") as handle:
                payload = json.load(handle)
    except Exception:
        return {}
    if not isinstance(payload, dict):
        return {}
    if not _looks_like_colbert_sentence_transformers_config(payload):
        return {}
    return payload


def _looks_like_colbert_sentence_transformers_config(payload: dict[str, Any]) -> bool:
    if str(payload.get("model_type", "")).lower() == "colbert":
        return True
    if str(payload.get("similarity_fn_name", "")).lower() == "maxsim":
        return True
    return any(
        key in payload
        for key in [
            "query_prefix",
            "document_prefix",
            "query_length",
            "document_length",
            "do_query_expansion",
            "attend_to_expansion_tokens",
        ]
    )


def _metadata_str(metadata: dict[str, Any], key: str) -> str | None:
    value = metadata.get(key)
    return value if isinstance(value, str) and value else None


def _metadata_int(metadata: dict[str, Any], key: str) -> int | None:
    value = metadata.get(key)
    if isinstance(value, int):
        return value
    return None


def _metadata_bool(metadata: dict[str, Any], key: str) -> bool | None:
    value = metadata.get(key)
    if isinstance(value, bool):
        return value
    return None


def _resolve_late_interaction_str(*, explicit: str | None, metadata: dict[str, Any], key: str) -> str | None:
    if explicit is not None:
        return explicit
    return _metadata_str(metadata, key)


def _resolve_late_interaction_int(*, explicit: int | None, metadata: dict[str, Any], key: str) -> int | None:
    if explicit is not None:
        return explicit
    return _metadata_int(metadata, key)


def _resolve_late_interaction_bool(*, explicit: bool | None, metadata: dict[str, Any], key: str) -> bool | None:
    if explicit is not None:
        return explicit
    return _metadata_bool(metadata, key)


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
        "backend_library": "pylate" if args.model_type == "late-interaction" else "sentence-transformers",
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
