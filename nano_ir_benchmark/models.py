from __future__ import annotations

import importlib
import importlib.metadata
import platform
import sys
from dataclasses import dataclass
from typing import Any

import torch


@dataclass(frozen=True)
class ModelLoadConfig:
    model_name_or_path: str
    model_type: str = "dense"
    dtype: str = "bf16"
    attn_implementation: str | None = None
    flash_attn2: bool = False
    device: str | None = None
    trust_remote_code: bool = False
    max_seq_length: int | None = None


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


def _import_sentence_transformer() -> Any:
    return getattr(importlib.import_module("sentence_transformers"), "SentenceTransformer")


def _import_sparse_encoder() -> Any:
    return getattr(importlib.import_module("sentence_transformers.sparse_encoder"), "SparseEncoder")


def _import_cross_encoder() -> Any:
    return getattr(importlib.import_module("sentence_transformers"), "CrossEncoder")


def load_model(config: ModelLoadConfig) -> Any:
    if config.model_type == "late-interaction":
        raise NotImplementedError("Late-interaction models are reserved for a future adapter.")

    model_kwargs = _model_kwargs(config)
    if config.model_type == "dense":
        model = _import_sentence_transformer()(
            config.model_name_or_path,
            device=config.device,
            trust_remote_code=config.trust_remote_code,
            model_kwargs=model_kwargs,
        )
        _set_max_seq_length(model, config.max_seq_length)
        return model

    if config.model_type == "sparse":
        model = _import_sparse_encoder()(
            config.model_name_or_path,
            device=config.device,
            trust_remote_code=config.trust_remote_code,
            model_kwargs=model_kwargs,
        )
        _set_max_seq_length(model, config.max_seq_length)
        return model

    if config.model_type == "reranker":
        kwargs: dict[str, Any] = {
            "device": config.device,
            "trust_remote_code": config.trust_remote_code,
            "model_kwargs": model_kwargs,
        }
        if config.max_seq_length is not None:
            kwargs["max_length"] = config.max_seq_length
        return _import_cross_encoder()(config.model_name_or_path, **kwargs)

    raise ValueError(f"Unsupported model type: {config.model_type}")


def _set_max_seq_length(model: Any, max_seq_length: int | None) -> None:
    if max_seq_length is not None and hasattr(model, "max_seq_length"):
        model.max_seq_length = max_seq_length


def collect_runtime_environment() -> dict[str, Any]:
    return {
        "python": sys.version,
        "platform": platform.platform(),
        "package_versions": {
            package: _version_or_none(package)
            for package in ["torch", "transformers", "sentence-transformers", "datasets", "numpy", "scipy"]
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
    total_parameters, trainable_parameters, transformer_parameters = _parameter_counts(model)
    return {
        "model_type": args.model_type,
        "name_or_path": args.model,
        "device": args.device,
        "dtype": args.dtype,
        "attn_implementation": resolve_attn_implementation(
            attn_implementation=args.attn_implementation,
            flash_attn2=args.flash_attn2,
        ),
        "trust_remote_code": args.trust_remote_code,
        "backend_library": "sentence-transformers",
        "max_seq_length": getattr(model, "max_seq_length", getattr(model, "max_length", None)),
        "similarity_fn_name": str(getattr(model, "similarity_fn_name", "")) or None,
        "prompts": getattr(model, "prompts", None),
        "default_prompt_name": getattr(model, "default_prompt_name", None),
        "total_parameters": total_parameters,
        "trainable_parameters": trainable_parameters,
        "transformer_parameters": transformer_parameters,
        "active_parameters": transformer_parameters or total_parameters,
    }


def _parameter_counts(model: Any) -> tuple[int | None, int | None, int | None]:
    named_parameters = _named_parameters(model)
    if named_parameters is None:
        return None, None, None
    total = 0
    trainable = 0
    transformer = 0
    for name, parameter in named_parameters:
        count = int(parameter.numel())
        total += count
        if parameter.requires_grad:
            trainable += count
        lowered = name.lower()
        if any(marker in lowered for marker in ["transformer", "auto_model", "encoder.layer", "backbone"]):
            transformer += count
    return total, trainable, transformer if transformer else None


def _named_parameters(model: Any) -> list[tuple[str, torch.nn.Parameter]] | None:
    candidate = model
    if not hasattr(candidate, "named_parameters") and hasattr(model, "model"):
        candidate = model.model
    if not hasattr(candidate, "named_parameters"):
        return None
    return list(candidate.named_parameters())
