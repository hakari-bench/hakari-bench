"""Helpers for HAKARI model-card generation and validation.

The canonical model-card schema and workflow live in ``docs/model_cards.md``.
Keep behavior changes here and user-facing schema guidance there in sync.
"""

from __future__ import annotations

import argparse
import json
import lzma
import math
import re
from dataclasses import dataclass
from pathlib import Path
from typing import Any

import yaml

from hakari_bench.models import ModelLoadConfig, collect_model_metadata, load_model


MODEL_CARD_METHODS = frozenset({"dense", "sparse", "reranker", "late-interaction", "bm25"})
MODEL_CARD_DOCS_PATH = "docs/model_cards.md"

_LANGUAGE_SUPPORT_CLASSIFICATION_POLICY = (
    "model identity first; use broad score evidence only for models without explicit language identity"
)
_LANGUAGE_SUPPORT_BENCHMARKS = ["NanoMIRACL", "MNanoBEIR"]
_HIGH_NON_ENGLISH_SCORE_THRESHOLD = 0.6
_MIN_LANGUAGE_SUPPORT_EVIDENCE_LANGUAGES = 8
_NANOBEIR_LANGUAGE_RE = re.compile(r"(?:^|/)NanoBEIR-([a-z]{2,3})(?:$|[,_/.-])")
_LANGUAGE_CODE_RE = re.compile(r"^[a-z]{2,3}$")
_PROMPT_KEYS = (
    "query_prompt",
    "document_prompt",
    "query_prompt_name",
    "document_prompt_name",
    "query_encode_task",
    "document_encode_task",
)
_LATE_INTERACTION_KEYS = (
    "architecture",
    "scoring",
    "query_prefix",
    "document_prefix",
    "query_length",
    "document_length",
    "do_query_expansion",
    "attend_to_expansion_tokens",
)

_LANGUAGE_FAMILIES = {
    "ar": "semitic",
    "de": "germanic",
    "en": "germanic",
    "es": "romance",
    "fr": "romance",
    "it": "romance",
    "no": "germanic",
    "pt": "romance",
    "sv": "germanic",
    "ja": "japonic",
    "ko": "koreanic",
    "zh": "sinitic",
    "th": "kra-dai",
    "vi": "austroasiatic",
    "ru": "slavic",
    "sr": "slavic",
    "bn": "indo-aryan",
    "fa": "iranian",
    "fi": "finnic",
    "hi": "indo-aryan",
    "id": "austronesian",
    "sw": "bantu",
    "te": "dravidian",
    "yo": "volta-niger",
}


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
    method = validate_model_card_method(metadata.get("method"), model_id=model_id)
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
        "method": method,
        "parameters": _drop_none(parameters),
        "embedding": {"truncate_dims": truncate_dims},
        "runtime": _drop_none(runtime),
    }
    prompts = metadata.get("prompts")
    if isinstance(prompts, dict):
        prompt_payload = _prompt_card_payload(prompts)
        if prompt_payload:
            card["prompts"] = prompt_payload
    late_interaction = metadata.get("late_interaction")
    if isinstance(late_interaction, dict):
        card["late_interaction"] = _drop_none(
            {
                "architecture": _clean_scalar(late_interaction.get("architecture")),
                "scoring": _clean_scalar(late_interaction.get("scoring")),
                "query_prefix": _clean_scalar(late_interaction.get("query_prefix")),
                "document_prefix": _clean_scalar(late_interaction.get("document_prefix")),
                "query_length": _int_or_none(late_interaction.get("query_length")),
                "document_length": _int_or_none(late_interaction.get("document_length")),
                "do_query_expansion": _clean_scalar(late_interaction.get("do_query_expansion")),
                "attend_to_expansion_tokens": _clean_scalar(late_interaction.get("attend_to_expansion_tokens")),
            }
        )
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
    infer_language_support: bool = False,
) -> dict[str, dict[str, Any]]:
    excluded_ids = set(exclude_model_ids or [])
    excluded_substrings = [item.lower() for item in exclude_model_substrings or []]
    existing_cards = existing_cards or {}
    metadata_by_model: dict[str, dict[str, Any]] = {}
    truncate_dims_by_model: dict[str, set[int]] = {}
    datasets_by_model: dict[str, set[str]] = {}
    prompts_by_model: dict[str, list[dict[str, Any]]] = {}
    late_interaction_by_model: dict[str, list[dict[str, Any]]] = {}
    language_scores_by_model: dict[str, dict[str, list[float]]] = {}
    for result_path in _result_json_paths(results_dir):
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
        prompts = _prompts_from_result_payload(payload)
        if prompts:
            prompts_by_model.setdefault(model_id, []).append(prompts)
        late_interaction = _late_interaction_from_result_payload(payload)
        if late_interaction:
            late_interaction_by_model.setdefault(model_id, []).append(late_interaction)
        target = payload.get("target")
        dataset_id = target.get("dataset_id") if isinstance(target, dict) else None
        if isinstance(dataset_id, str) and dataset_id:
            datasets_by_model.setdefault(model_id, set()).add(dataset_id)
        if infer_language_support:
            language_score = _language_score_from_result_payload(payload)
            if language_score is not None:
                language, score = language_score
                language_scores_by_model.setdefault(model_id, {}).setdefault(language, []).append(score)

    cards: dict[str, dict[str, Any]] = {}
    for model_id in sorted(metadata_by_model):
        existing_card = existing_cards.get(model_id)
        metadata = _merge_existing_card_metadata(metadata_by_model[model_id], existing_card)
        prompts = _stable_mapping_from_results(prompts_by_model.get(model_id, []), keys=_PROMPT_KEYS)
        if prompts:
            metadata["prompts"] = prompts
        late_interaction = _stable_mapping_from_results(
            late_interaction_by_model.get(model_id, []),
            keys=_LATE_INTERACTION_KEYS,
        )
        if late_interaction:
            metadata["late_interaction"] = late_interaction
        truncate_dims = sorted(truncate_dims_by_model.get(model_id, set())) or None
        generated_card = model_card_from_metadata(
            metadata,
            truncate_dims=truncate_dims,
            overrides=ModelCardOverrides(),
            target=_drop_empty({"datasets": sorted(datasets_by_model.get(model_id, set()))}),
        )
        if infer_language_support and not _has_language_support(existing_card):
            language_support = infer_language_support_from_scores(
                model_id=model_id,
                language_scores=language_scores_by_model.get(model_id, {}),
            )
            if language_support is not None:
                generated_card["language_support"] = language_support
        cards[model_id] = _merge_existing_card_fields(generated_card, existing_card)
    return cards


def infer_language_support_from_scores(
    *,
    model_id: str,
    language_scores: dict[str, list[float]],
) -> dict[str, Any] | None:
    """Build a conservative ``language_support`` suggestion from benchmark scores.

    This is a bootstrap helper for ``scripts/generate_model_cards.py --from-results``.
    The model-card policy in ``docs/model_cards.md`` still treats manually reviewed
    model identity as authoritative.
    """
    language_means = _language_mean_scores(language_scores)
    if len(language_means) < _MIN_LANGUAGE_SUPPORT_EVIDENCE_LANGUAGES:
        return None
    english_score = language_means.get("en")
    non_english_scores = [score for language, score in language_means.items() if language != "en"]
    non_english_mean = _mean(non_english_scores)
    high_non_english_languages = [
        language
        for language, score in language_means.items()
        if language != "en" and score >= _HIGH_NON_ENGLISH_SCORE_THRESHOLD
    ]
    high_non_english_families = {
        _LANGUAGE_FAMILIES.get(language, language) for language in high_non_english_languages
    }
    category, languages, reason = _language_support_identity_hint(model_id)
    if category is None:
        category, languages, reason = _language_support_score_hint(
            english_score=english_score,
            non_english_mean=non_english_mean,
            high_non_english_language_count=len(high_non_english_languages),
        )
    if category is None:
        return None

    evidence = {
        "benchmarks": list(_LANGUAGE_SUPPORT_BENCHMARKS),
        "score_target": "all",
        "classification_policy": _LANGUAGE_SUPPORT_CLASSIFICATION_POLICY,
        "classification_reason": reason,
        "high_non_english_score_threshold": _HIGH_NON_ENGLISH_SCORE_THRESHOLD,
        "high_non_english_language_count": len(high_non_english_languages),
        "high_non_english_family_count": len(high_non_english_families),
        "evaluated_language_count": len(language_means),
    }
    if english_score is not None:
        evidence["english_score"] = round(english_score, 3)
    if non_english_mean is not None:
        evidence["non_english_mean_score"] = round(non_english_mean, 3)

    language_support: dict[str, Any] = {"category": category, "evidence": evidence}
    if category != "multilingual":
        language_support["languages"] = languages or ["en"]
    return language_support


def write_model_card(card: dict[str, Any], *, output_dir: Path, overwrite: bool) -> Path:
    model_id = card.get("id")
    if not isinstance(model_id, str) or not model_id:
        raise ValueError("Model card requires a non-empty string id.")
    card = dict(card)
    card["method"] = validate_model_card_method(card.get("method"), model_id=model_id)
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
        _metadata_with_evaluation_args(model_metadata, args),
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


def validate_model_card_method(value: Any, *, model_id: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise ValueError(f"Model card {model_id!r} requires a non-empty method.")
    method = value.strip().casefold().replace("_", "-")
    if method not in MODEL_CARD_METHODS:
        allowed = ", ".join(sorted(MODEL_CARD_METHODS))
        raise ValueError(f"Model card {model_id!r} has unsupported method {value!r}; expected one of: {allowed}.")
    return method


_ALLOWED_LINK_KEYS = ("huggingface", "github", "papers")


def validate_model_card_links(links: Any) -> dict[str, Any]:
    """Validate and normalize an optional model-card ``links`` section.

    The section may carry a single ``huggingface`` URL, a single ``github``
    URL, and a list of ``papers`` where every paper pairs a ``title`` with a
    ``url``. Every field is optional. Empty fields are dropped from the
    returned mapping so absent links are simply omitted from the card.
    """
    if not isinstance(links, dict):
        raise ValueError("Model card links must be a mapping.")
    unknown = sorted(set(links) - set(_ALLOWED_LINK_KEYS))
    if unknown:
        raise ValueError(f"Unknown model card link keys: {', '.join(unknown)}")
    normalized: dict[str, Any] = {}
    for key in ("huggingface", "github"):
        url = links.get(key)
        if url is None:
            continue
        if not isinstance(url, str) or not url.strip():
            raise ValueError(f"Model card link {key!r} must be a non-empty string URL.")
        normalized[key] = url.strip()
    papers = links.get("papers")
    if papers is not None:
        normalized_papers = _validate_link_papers(papers)
        if normalized_papers:
            normalized["papers"] = normalized_papers
    return normalized


def _validate_link_papers(papers: Any) -> list[dict[str, str]]:
    if not isinstance(papers, list):
        raise ValueError("Model card link 'papers' must be a list.")
    normalized: list[dict[str, str]] = []
    for paper in papers:
        if not isinstance(paper, dict):
            raise ValueError("Each model card paper must be a mapping with title and url.")
        unknown = sorted(set(paper) - {"title", "url"})
        if unknown:
            raise ValueError(f"Unknown model card paper keys: {', '.join(unknown)}")
        title = paper.get("title")
        url = paper.get("url")
        if not isinstance(title, str) or not title.strip():
            raise ValueError("Each model card paper requires a non-empty title.")
        if not isinstance(url, str) or not url.strip():
            raise ValueError("Each model card paper requires a non-empty url.")
        normalized.append({"title": title.strip(), "url": url.strip()})
    return normalized


def target_from_args(args: Any) -> dict[str, Any]:
    return _drop_empty(
        {
            "datasets": list(getattr(args, "dataset", None) or []),
            "collections": list(getattr(args, "collection", None) or []),
            "splits": list(getattr(args, "split", None) or []),
            "evaluation_scope": getattr(args, "evaluation_scope", None),
            "dataset_revision": getattr(args, "dataset_revision", None),
        }
    )


def _load_model_card_yaml(model_cards_path: Path) -> dict[str, dict[str, Any]]:
    payload = yaml.safe_load(model_cards_path.read_text(encoding="utf-8")) or {}
    if not isinstance(payload, dict):
        raise ValueError(f"Model cards YAML must contain a mapping: {model_cards_path}")
    if isinstance(payload.get("id"), str):
        model_id = str(payload["id"])
        validate_model_card_method(payload.get("method"), model_id=model_id)
        return {model_id: payload}
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
        validate_model_card_method(item.get("method"), model_id=model_id)
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


def _prompt_card_payload(prompts: dict[str, Any]) -> dict[str, Any]:
    return {
        key: value
        for key in _PROMPT_KEYS
        for value in [_clean_scalar(prompts.get(key))]
        if isinstance(value, str) and (value or key.endswith("_prompt"))
    }


def _drop_none(payload: dict[str, Any]) -> dict[str, Any]:
    return {key: value for key, value in payload.items() if value is not None}


def _drop_empty(payload: dict[str, Any]) -> dict[str, Any]:
    return {key: value for key, value in payload.items() if value not in (None, [], {})}


def _read_json(path: Path) -> Any:
    try:
        if path.name.endswith(".json.xz"):
            with lzma.open(path, "rt", encoding="utf-8") as file:
                return json.load(file)
        return json.loads(path.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, lzma.LZMAError, UnicodeDecodeError):
        return None


def _language_score_from_result_payload(payload: dict[str, Any]) -> tuple[str, float] | None:
    language = _language_from_result_target(payload.get("target"))
    if language is None:
        return None
    score = _aggregate_score_from_result_payload(payload)
    if score is None:
        return None
    return language, score


def _language_from_result_target(target: Any) -> str | None:
    if not isinstance(target, dict):
        return None
    candidates = [
        target.get("dataset_name"),
        target.get("dataset_id"),
    ]
    for candidate in candidates:
        if not isinstance(candidate, str):
            continue
        match = _NANOBEIR_LANGUAGE_RE.search(candidate)
        if match is not None:
            return match.group(1)
    dataset_name = target.get("dataset_name")
    if dataset_name == "NanoMIRACL":
        for key in ("task_name", "split_name"):
            value = target.get(key)
            if isinstance(value, str) and _LANGUAGE_CODE_RE.fullmatch(value):
                return value
    return None


def _aggregate_score_from_result_payload(payload: dict[str, Any]) -> float | None:
    evaluation = payload.get("evaluation")
    if not isinstance(evaluation, dict):
        return None
    return _finite_float_or_none(evaluation.get("aggregate_metric_value"))


def _language_mean_scores(language_scores: dict[str, list[float]]) -> dict[str, float]:
    means: dict[str, float] = {}
    for language, scores in language_scores.items():
        mean_score = _mean(scores)
        if mean_score is not None:
            means[language] = mean_score
    return means


def _mean(values: list[float]) -> float | None:
    finite_values = [value for value in values if math.isfinite(value)]
    if not finite_values:
        return None
    return sum(finite_values) / len(finite_values)


def _finite_float_or_none(value: Any) -> float | None:
    if isinstance(value, bool) or value is None:
        return None
    try:
        parsed = float(value)
    except (TypeError, ValueError):
        return None
    return parsed if math.isfinite(parsed) else None


def _language_support_identity_hint(model_id: str) -> tuple[str | None, list[str] | None, str | None]:
    lowered = model_id.casefold()
    if any(token in lowered for token in ("multilingual", "bilingual", "bge-m3", "mmarco")):
        return "multilingual", None, "model_identity_multilingual_or_bilingual"
    if any(token in lowered for token in ("japanese", "ruri")):
        return "english_plus", ["ja", "en"], "model_identity_japanese_or_ruri"
    if any(token in lowered for token in ("english", "-en-", "-en.", "-en_", "/all-minilm", "/all-mpnet")):
        return "english_only", ["en"], "model_identity_english_only"
    return None, None, None


def _language_support_score_hint(
    *,
    english_score: float | None,
    non_english_mean: float | None,
    high_non_english_language_count: int,
) -> tuple[str | None, list[str] | None, str | None]:
    if non_english_mean is not None and (
        high_non_english_language_count >= 4
        or non_english_mean >= 0.55
        or (high_non_english_language_count >= 3 and non_english_mean >= 0.4)
    ):
        return "multilingual", None, "broad_multilingual_score_evidence"
    if (
        english_score is not None
        and english_score >= 0.45
        and (non_english_mean is None or non_english_mean <= 0.4)
        and high_non_english_language_count <= 1
    ):
        return "english_only", ["en"], "score_evidence_english_only"
    return None, None, None


def _result_json_paths(results_dir: Path) -> list[Path]:
    return sorted(
        path
        for path in results_dir.glob("*/*/*")
        if path.is_file() and path.name.endswith((".json", ".json.xz"))
    )


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
    base_dim = _base_embedding_dim_from_embedding_evaluations(embedding_evaluations)
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
            if parsed_dim is not None and parsed_dim != base_dim:
                dims.add(parsed_dim)
    return dims


def _base_embedding_dim_from_embedding_evaluations(embedding_evaluations: list[Any]) -> int | None:
    for item in embedding_evaluations:
        if not isinstance(item, dict) or item.get("name") != "base":
            continue
        embedding_dimensions = item.get("embedding_dimensions")
        if isinstance(embedding_dimensions, dict):
            dim = _int_or_none(embedding_dimensions.get("dim"))
            if dim is not None:
                return dim
        embedding_metadata = item.get("embedding_metadata")
        dimensions = embedding_metadata.get("dimensions") if isinstance(embedding_metadata, dict) else None
        if isinstance(dimensions, dict):
            dim = _int_or_none(dimensions.get("dim"))
            if dim is not None:
                return dim
    return None


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


def _metadata_with_evaluation_args(metadata: dict[str, Any], args: Any) -> dict[str, Any]:
    enriched = dict(metadata)
    prompts = _prompt_card_payload(
        {
            "query_prompt": getattr(args, "query_prompt", None),
            "document_prompt": getattr(args, "corpus_prompt", getattr(args, "document_prompt", None)),
            "query_prompt_name": getattr(args, "query_prompt_name", None),
            "document_prompt_name": getattr(args, "corpus_prompt_name", getattr(args, "document_prompt_name", None)),
            "query_encode_task": getattr(args, "query_task", getattr(args, "query_encode_task", None)),
            "document_encode_task": getattr(args, "corpus_task", getattr(args, "document_encode_task", None)),
        }
    )
    if prompts:
        enriched["prompts"] = prompts
    if validate_model_card_method(enriched.get("method"), model_id=str(enriched.get("id") or "")) == "late-interaction":
        late_interaction = _drop_none(
            {
                "scoring": "maxsim",
                "query_prefix": getattr(args, "late_interaction_query_prefix", None),
                "document_prefix": getattr(args, "late_interaction_document_prefix", None),
                "query_length": _int_or_none(getattr(args, "late_interaction_query_length", None)),
                "document_length": _int_or_none(getattr(args, "late_interaction_document_length", None)),
                "do_query_expansion": getattr(args, "late_interaction_do_query_expansion", None),
                "attend_to_expansion_tokens": getattr(args, "late_interaction_attend_to_expansion_tokens", None),
            }
        )
        if late_interaction:
            existing_late_interaction = enriched.get("late_interaction")
            base_late_interaction = dict(existing_late_interaction) if isinstance(existing_late_interaction, dict) else {}
            enriched["late_interaction"] = {**base_late_interaction, **late_interaction}
    return enriched


def _prompts_from_result_payload(payload: dict[str, Any]) -> dict[str, Any]:
    config = payload.get("config")
    if not isinstance(config, dict):
        return {}
    return _prompt_card_payload(config)


def _late_interaction_from_result_payload(payload: dict[str, Any]) -> dict[str, Any]:
    config = payload.get("config")
    if not isinstance(config, dict):
        return {}
    late_interaction = config.get("late_interaction")
    if not isinstance(late_interaction, dict):
        return {}
    payload = {
        "architecture": _clean_scalar(late_interaction.get("architecture")),
        "scoring": _normalize_late_interaction_scoring(late_interaction.get("scoring")),
        "query_prefix": _clean_scalar(late_interaction.get("query_prefix")),
        "document_prefix": _clean_scalar(late_interaction.get("document_prefix")),
        "query_length": _int_or_none(late_interaction.get("query_length")),
        "document_length": _int_or_none(late_interaction.get("document_length")),
        "do_query_expansion": _clean_scalar(late_interaction.get("do_query_expansion")),
        "attend_to_expansion_tokens": _clean_scalar(late_interaction.get("attend_to_expansion_tokens")),
    }
    return _drop_none(payload)


def _normalize_late_interaction_scoring(value: Any) -> Any:
    if value == "exact_maxsim":
        return "maxsim"
    return _clean_scalar(value)


def _stable_mapping_from_results(
    values: list[dict[str, Any]],
    *,
    keys: tuple[str, ...],
) -> dict[str, Any]:
    stable: dict[str, Any] = {}
    for key in keys:
        present_values = [item[key] for item in values if key in item]
        if not present_values:
            continue
        first = present_values[0]
        if all(value == first for value in present_values):
            stable[key] = first
    return stable


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
    if isinstance(existing_card.get("prompts"), dict) and not isinstance(merged.get("prompts"), dict):
        merged["prompts"] = existing_card["prompts"]
    if isinstance(existing_card.get("late_interaction"), dict) and not isinstance(merged.get("late_interaction"), dict):
        merged["late_interaction"] = existing_card["late_interaction"]
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
    if isinstance(existing_card.get("prompts"), dict):
        merged["prompts"] = existing_card["prompts"]
    if isinstance(existing_card.get("late_interaction"), dict):
        merged["late_interaction"] = existing_card["late_interaction"]
    for key, value in existing_card.items():
        if key not in merged:
            merged[key] = value
    if "language_support" in existing_card:
        merged["language_support"] = existing_card["language_support"]
    return merged


def _has_language_support(card: dict[str, Any] | None) -> bool:
    return isinstance(card, dict) and isinstance(card.get("language_support"), dict)
