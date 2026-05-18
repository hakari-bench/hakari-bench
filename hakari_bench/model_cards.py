from __future__ import annotations

import argparse
import json
import math
from dataclasses import dataclass
from pathlib import Path
from typing import Any

import yaml

from hakari_bench.models import ModelLoadConfig, collect_model_metadata, load_model


@dataclass(frozen=True)
class ModelCardOverrides:
    display_name: str | None = None
    source_name: str | None = None
    source_revision: str | None = None
    source_revision_requested: str | None = None
    total_parameters: int | None = None
    trainable_parameters: int | None = None
    input_embedding_parameters: int | None = None
    active_parameters: int | None = None
    max_seq_length: int | None = None


def parse_truncate_dims(values: list[str] | None, *, model_type: str) -> list[int] | None:
    if not values:
        if model_type == "dense":
            raise ValueError("dense model cards require --truncate-dims. Use --truncate-dims none for unsupported models.")
        return None
    normalized = [value.strip().lower() for value in values]
    if normalized == ["none"]:
        return None
    if "none" in normalized:
        raise ValueError("--truncate-dims none cannot be combined with numeric dimensions.")
    dims = sorted({int(value) for value in normalized})
    if any(dim <= 0 for dim in dims):
        raise ValueError("--truncate-dims values must be positive integers.")
    return dims


def build_model_card_from_loaded_model(
    *,
    model_id: str,
    model_type: str,
    truncate_dims: list[int] | None,
    overrides: ModelCardOverrides,
    model_revision: str | None = None,
    dtype: str = "bf16",
    attn_implementation: str | None = None,
    flash_attn2: bool = False,
    device: str | None = None,
    trust_remote_code: bool = False,
    remote_code_approved: bool = False,
    model_max_seq_length: int | None = None,
    target: dict[str, Any] | None = None,
) -> dict[str, Any]:
    model_name = overrides.source_name or model_id
    loaded_model = load_model(
        ModelLoadConfig(
            model_name_or_path=model_name,
            model_type=model_type,
            model_revision=model_revision,
            dtype=dtype,
            attn_implementation=attn_implementation,
            flash_attn2=flash_attn2,
            device=device,
            trust_remote_code=trust_remote_code,
            max_seq_length=model_max_seq_length,
        )
    )
    args = argparse.Namespace(
        model=model_name,
        model_id=model_id,
        model_type=model_type,
        model_revision=model_revision,
        model_source={"type": "huggingface", "name": model_name},
        dtype=dtype,
        device=device,
        trust_remote_code=trust_remote_code,
        attn_implementation=attn_implementation,
        flash_attn2=flash_attn2,
    )
    metadata = collect_model_metadata(loaded_model, args)
    return model_card_from_metadata(
        metadata,
        truncate_dims=truncate_dims,
        overrides=overrides,
        target=target,
        remote_code_approved=remote_code_approved,
    )


def model_card_from_metadata(
    metadata: dict[str, Any],
    *,
    truncate_dims: list[int] | None,
    overrides: ModelCardOverrides,
    target: dict[str, Any] | None = None,
    remote_code_approved: bool = False,
) -> dict[str, Any]:
    model_id = str(metadata.get("id") or metadata.get("model_id") or "")
    if not model_id:
        raise ValueError("Model metadata must include a non-empty id.")
    source = _source_payload(metadata.get("source"), model_id=model_id, overrides=overrides)
    parameters = {
        "total": _override_or_metadata(overrides.total_parameters, metadata.get("total_parameters")),
        "trainable": _override_or_metadata(overrides.trainable_parameters, metadata.get("trainable_parameters")),
        "input_embedding": _override_or_metadata(
            overrides.input_embedding_parameters,
            metadata.get("embedding_parameters"),
        ),
        "active": _override_or_metadata(overrides.active_parameters, metadata.get("active_parameters")),
    }
    runtime = {
        "max_seq_length": _override_or_metadata(overrides.max_seq_length, metadata.get("max_seq_length")),
        "dtype": _clean_scalar(metadata.get("dtype")),
        "trust_remote_code": _clean_scalar(metadata.get("trust_remote_code")),
        "remote_code_approved": True if remote_code_approved and metadata.get("trust_remote_code") is True else None,
        "attn_implementation": _clean_scalar(metadata.get("attn_implementation")),
        "backend_library": _clean_scalar(metadata.get("backend_library")),
        "similarity_fn_name": _clean_scalar(metadata.get("similarity_fn_name")),
    }
    card: dict[str, Any] = {
        "id": model_id,
        "source": source,
        "method": _clean_scalar(metadata.get("method")),
        "parameters": _drop_none(parameters),
        "embedding": {"truncate_dims": truncate_dims},
        "runtime": _drop_none(runtime),
    }
    if target:
        card["target"] = _drop_empty(target)
    if overrides.display_name is not None:
        card["display_name"] = overrides.display_name
    return _drop_none(card)


def collect_model_cards_from_results(
    results_dir: Path,
    *,
    exclude_model_substrings: list[str] | None = None,
    exclude_model_ids: list[str] | None = None,
    existing_cards: dict[str, dict[str, Any]] | None = None,
) -> dict[str, dict[str, Any]]:
    excluded_ids = set(exclude_model_ids or [])
    excluded_substrings = [item.lower() for item in exclude_model_substrings or []]
    existing_cards = existing_cards or {}
    metadata_by_model: dict[str, dict[str, Any]] = {}
    truncate_dims_by_model: dict[str, set[int]] = {}
    datasets_by_model: dict[str, set[str]] = {}
    for result_path in sorted(results_dir.glob("*/*/*.json")):
        payload = _read_json(result_path)
        if not isinstance(payload, dict):
            continue
        model = payload.get("model")
        if not isinstance(model, dict):
            continue
        model_id = str(model.get("id") or _model_id_from_result_path(results_dir, result_path))
        if _excluded_model(model_id, excluded_ids=excluded_ids, excluded_substrings=excluded_substrings):
            continue
        method = str(model.get("method") or "")
        if method == "bm25":
            continue
        if model_id not in metadata_by_model or _metadata_completeness(model) > _metadata_completeness(metadata_by_model[model_id]):
            metadata_by_model[model_id] = model
        truncate_dims_by_model.setdefault(model_id, set()).update(_truncate_dims_from_result_payload(payload))
        target = payload.get("target")
        dataset_id = target.get("dataset_id") if isinstance(target, dict) else None
        if isinstance(dataset_id, str) and dataset_id:
            datasets_by_model.setdefault(model_id, set()).add(dataset_id)

    cards: dict[str, dict[str, Any]] = {}
    for model_id in sorted(metadata_by_model):
        existing_card = existing_cards.get(model_id)
        metadata = _merge_existing_card_metadata(metadata_by_model[model_id], existing_card)
        truncate_dims = sorted(truncate_dims_by_model.get(model_id, set())) or None
        generated_card = model_card_from_metadata(
            metadata,
            truncate_dims=truncate_dims,
            overrides=ModelCardOverrides(),
            target=_drop_empty({"datasets": sorted(datasets_by_model.get(model_id, set()))}),
        )
        cards[model_id] = _merge_existing_card_fields(generated_card, existing_card)
    return cards


def write_model_card(card: dict[str, Any], *, output_dir: Path, overwrite: bool) -> Path:
    model_id = card.get("id")
    if not isinstance(model_id, str) or not model_id:
        raise ValueError("Model card requires a non-empty string id.")
    output_dir.mkdir(parents=True, exist_ok=True)
    output_path = output_dir / f"{safe_model_card_stem(model_id)}.yaml"
    if output_path.exists() and not overwrite:
        raise FileExistsError(f"Model card already exists: {output_path}")
    output_path.write_text(yaml.safe_dump(card, sort_keys=False, allow_unicode=False), encoding="utf-8")
    return output_path


def write_evaluation_model_card(*, args: Any, model_metadata: dict[str, Any]) -> Path:
    model_id = str(model_metadata.get("id") or getattr(args, "model_id"))
    output_dir = Path(getattr(args, "output_dir")) / safe_model_card_stem(model_id)
    card = model_card_from_metadata(
        model_metadata,
        truncate_dims=_truncate_dims_from_embedding_variants(getattr(args, "embedding_variants", [])),
        overrides=ModelCardOverrides(),
        target=target_from_args(args),
    )
    return write_model_card(card, output_dir=output_dir, overwrite=True)


def load_model_cards(model_cards_path: Path | None) -> dict[str, dict[str, Any]]:
    if model_cards_path is None or not model_cards_path.exists():
        return {}
    cards: dict[str, dict[str, Any]] = {}
    for card_path in model_card_yaml_paths(model_cards_path):
        for model_id, card in _load_model_card_yaml(card_path).items():
            if model_id in cards:
                raise ValueError(f"Duplicate model card id {model_id!r}: {card_path}")
            cards[model_id] = card
    return cards


def model_card_yaml_paths(model_cards_path: Path) -> list[Path]:
    if model_cards_path.is_dir():
        return sorted(
            path
            for pattern in ("*.yaml", "*.yml")
            for path in model_cards_path.glob(pattern)
            if path.is_file()
        )
    return [model_cards_path]


def safe_model_card_stem(model_id: str) -> str:
    return model_id.replace("/", "__")


def target_from_args(args: Any) -> dict[str, Any]:
    return _drop_empty(
        {
            "datasets": list(getattr(args, "dataset", None) or []),
            "collections": list(getattr(args, "collection", None) or []),
            "splits": list(getattr(args, "split", None) or []),
            "dataset_revision": getattr(args, "dataset_revision", None),
        }
    )


def _load_model_card_yaml(model_cards_path: Path) -> dict[str, dict[str, Any]]:
    payload = yaml.safe_load(model_cards_path.read_text(encoding="utf-8")) or {}
    if not isinstance(payload, dict):
        raise ValueError(f"Model cards YAML must contain a mapping: {model_cards_path}")
    if isinstance(payload.get("id"), str):
        return {str(payload["id"]): payload}
    models = payload.get("models", [])
    if not isinstance(models, list):
        raise ValueError(f"Model cards YAML 'models' must be a list: {model_cards_path}")
    cards: dict[str, dict[str, Any]] = {}
    for item in models:
        if not isinstance(item, dict):
            raise ValueError(f"Model card entries must be mappings: {model_cards_path}")
        model_id = item.get("id")
        if not isinstance(model_id, str) or not model_id:
            raise ValueError(f"Model card entries require a non-empty string id: {model_cards_path}")
        cards[model_id] = item
    return cards


def _source_payload(source: Any, *, model_id: str, overrides: ModelCardOverrides) -> dict[str, Any]:
    payload = dict(source) if isinstance(source, dict) else {"type": "huggingface", "name": model_id}
    payload.setdefault("type", "huggingface")
    payload["name"] = overrides.source_name or payload.get("name") or model_id
    if overrides.source_revision is not None:
        payload["revision"] = overrides.source_revision
    if overrides.source_revision_requested is not None:
        payload["revision_requested"] = overrides.source_revision_requested
    return _drop_none(payload)


def _override_or_metadata(override: int | None, value: Any) -> int | None:
    return override if override is not None else _int_or_none(value)


def _int_or_none(value: Any) -> int | None:
    if isinstance(value, bool) or value is None:
        return None
    if isinstance(value, int):
        return value
    if isinstance(value, float):
        if not math.isfinite(value):
            return None
        return int(value)
    try:
        return int(value)
    except (TypeError, ValueError):
        return None


def _clean_scalar(value: Any) -> Any:
    if isinstance(value, float) and not math.isfinite(value):
        return None
    return value


def _drop_none(payload: dict[str, Any]) -> dict[str, Any]:
    return {key: value for key, value in payload.items() if value is not None}


def _drop_empty(payload: dict[str, Any]) -> dict[str, Any]:
    return {key: value for key, value in payload.items() if value not in (None, [], {})}


def _read_json(path: Path) -> Any:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return None


def _model_id_from_result_path(results_dir: Path, result_path: Path) -> str:
    return result_path.relative_to(results_dir).parts[0].replace("__", "/")


def _excluded_model(model_id: str, *, excluded_ids: set[str], excluded_substrings: list[str]) -> bool:
    lowered = model_id.lower()
    return model_id in excluded_ids or any(item in lowered for item in excluded_substrings)


def _metadata_completeness(metadata: dict[str, Any]) -> int:
    keys = (
        "source",
        "total_parameters",
        "trainable_parameters",
        "embedding_parameters",
        "active_parameters",
        "max_seq_length",
        "dtype",
    )
    return sum(1 for key in keys if metadata.get(key) is not None)


def _truncate_dims_from_result_payload(payload: dict[str, Any]) -> set[int]:
    evaluation = payload.get("evaluation")
    embedding_evaluations = evaluation.get("embedding_evaluations") if isinstance(evaluation, dict) else None
    if not isinstance(embedding_evaluations, list):
        embedding_evaluations = payload.get("embedding_evaluations")
    if not isinstance(embedding_evaluations, list):
        return set()
    dims: set[int] = set()
    for item in embedding_evaluations:
        if not isinstance(item, dict):
            continue
        transform = item.get("transform")
        steps = transform.get("steps") if isinstance(transform, dict) else None
        if not isinstance(steps, list):
            continue
        for step in steps:
            if not isinstance(step, dict) or step.get("type") != "truncate":
                continue
            parameters = step.get("parameters")
            dim = parameters.get("dim") if isinstance(parameters, dict) else None
            parsed_dim = _int_or_none(dim)
            if parsed_dim is not None:
                dims.add(parsed_dim)
    return dims


def _truncate_dims_from_embedding_variants(embedding_variants: Any) -> list[int] | None:
    if not isinstance(embedding_variants, list):
        return None
    dims: set[int] = set()
    for variant in embedding_variants:
        if not isinstance(variant, dict):
            continue
        dims.update(_truncate_dims_from_transform(variant.get("transform")))
    return sorted(dims) or None


def _truncate_dims_from_transform(transform: Any) -> set[int]:
    if not isinstance(transform, dict):
        return set()
    steps = transform.get("steps")
    if not isinstance(steps, list):
        steps = [transform]
    dims: set[int] = set()
    for step in steps:
        if not isinstance(step, dict) or step.get("type") != "truncate":
            continue
        parameters = step.get("parameters")
        dim = parameters.get("dim") if isinstance(parameters, dict) else None
        parsed_dim = _int_or_none(dim)
        if parsed_dim is not None:
            dims.add(parsed_dim)
    return dims


def _merge_existing_card_metadata(metadata: dict[str, Any], existing_card: dict[str, Any] | None) -> dict[str, Any]:
    if existing_card is None:
        return metadata
    merged = dict(metadata)
    parameters = existing_card.get("parameters")
    if isinstance(parameters, dict):
        mapping = {
            "total": "total_parameters",
            "trainable": "trainable_parameters",
            "input_embedding": "embedding_parameters",
            "active": "active_parameters",
        }
        for card_key, metadata_key in mapping.items():
            if merged.get(metadata_key) is None and parameters.get(card_key) is not None:
                merged[metadata_key] = parameters[card_key]
    runtime = existing_card.get("runtime")
    if isinstance(runtime, dict) and merged.get("max_seq_length") is None:
        merged["max_seq_length"] = runtime.get("max_seq_length")
    return merged


def _merge_existing_card_fields(generated_card: dict[str, Any], existing_card: dict[str, Any] | None) -> dict[str, Any]:
    if existing_card is None:
        return generated_card
    merged = dict(generated_card)
    existing_runtime = existing_card.get("runtime")
    generated_runtime = merged.get("runtime")
    if isinstance(existing_runtime, dict) and isinstance(generated_runtime, dict):
        for key in ("remote_code_approved",):
            if key in existing_runtime and key not in generated_runtime:
                generated_runtime[key] = existing_runtime[key]
    for key, value in existing_card.items():
        if key not in merged:
            merged[key] = value
    return merged
