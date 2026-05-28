from __future__ import annotations

import importlib
import importlib.metadata
import platform
import sys
from dataclasses import dataclass
from functools import lru_cache
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
    dense_cls = getattr(importlib.import_module("pylate.models"), "Dense")
    original = getattr(dense_cls, "from_sentence_transformers", None)
    if original is None or getattr(original, "_hakari_missing_activation_patch", False):
        return

    def from_sentence_transformers(dense: Any) -> Any:
        try:
            return original(dense)
        except KeyError as exc:
            if exc.args != ("activation_function",):
                raise
        config = dense.get_config_dict()
        config.setdefault("activation_function", "torch.nn.Identity")
        activation = config["activation_function"]
        if isinstance(activation, str):
            import_from_string = getattr(importlib.import_module("sentence_transformers.util"), "import_from_string")
            config["activation_function"] = import_from_string(activation)()
        model = dense_cls(**config)
        model.load_state_dict(dense.state_dict())
        return model

    from_sentence_transformers._hakari_missing_activation_patch = True  # type: ignore[attr-defined]
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
    ) -> None:
        super().__init__()
        self.model_name_or_path = model_name_or_path
        self.tokenizer = tokenizer
        self.backbone = backbone
        self.projection = projection
        self.query_prefix = query_prefix
        self.document_prefix = document_prefix
        self.query_length = query_length
        self.document_length = document_length
        self.do_query_expansion = None
        self.attend_to_expansion_tokens = None
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
        **_: Any,
    ) -> torch.Tensor | Any:
        del show_progress_bar
        sentences = [inputs] if isinstance(inputs, str) else list(inputs)
        batches: list[torch.Tensor] = []
        for start in range(0, len(sentences), batch_size):
            batch = self._encode_batch(sentences[start : start + batch_size])
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
        return self._encode_with_role(
            inputs,
            prefix=self.query_prefix,
            max_length=self.query_length,
            **kwargs,
        )

    def encode_document(self, inputs: list[str] | str, **kwargs: Any) -> torch.Tensor | Any:
        return self._encode_with_role(
            inputs,
            prefix=self.document_prefix,
            max_length=self.document_length,
            **kwargs,
        )

    def _encode_with_role(
        self,
        inputs: list[str] | str,
        *,
        prefix: str | None,
        max_length: int | None,
        batch_size: int = 32,
        show_progress_bar: bool | None = None,
        convert_to_numpy: bool = True,
        convert_to_tensor: bool = False,
        **_: Any,
    ) -> torch.Tensor | Any:
        del show_progress_bar
        sentences = [inputs] if isinstance(inputs, str) else list(inputs)
        if prefix:
            sentences = [prefix + sentence for sentence in sentences]
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
