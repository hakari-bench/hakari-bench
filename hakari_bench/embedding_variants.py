from __future__ import annotations

import copy
from itertools import product
from typing import Any

QUANTIZED_PRECISIONS = {"int8", "binary"}
TORCH_SCORE_REPRESENTATION = "torch_exact"
TORCH_RESCORE_SCORE_REPRESENTATION = "torch_exact_rescore"
NORMALIZE_TOKENS = {"normalize", "l2-normalize", "l2_normalize"}
SPARSE_QUERY_MAX_ACTIVE_DIMS_PREFIXES = (
    "sparse-query-max-active-dims:",
    "sparse_query_max_active_dims:",
)
SPARSE_QUERY_MAX_ACTIVE_DIMS_EQUALS_PREFIXES = tuple(
    prefix.replace(":", "=") for prefix in SPARSE_QUERY_MAX_ACTIVE_DIMS_PREFIXES
)
SPARSE_DOCUMENT_MAX_ACTIVE_DIMS_PREFIXES = (
    "sparse-document-max-active-dims:",
    "sparse_document_max_active_dims:",
)
SPARSE_DOCUMENT_MAX_ACTIVE_DIMS_EQUALS_PREFIXES = tuple(
    prefix.replace(":", "=") for prefix in SPARSE_DOCUMENT_MAX_ACTIVE_DIMS_PREFIXES
)


def parse_embedding_variants(
    values: list[str] | None,
    cross_values: list[list[str]] | None = None,
) -> list[dict[str, Any]]:
    variants: list[dict[str, Any]] = []
    seen_names: set[str] = set()

    def add_variant(variant: dict[str, Any]) -> None:
        name = str(variant["name"])
        if name in seen_names:
            raise ValueError(f"Duplicate embedding variant: {name}")
        seen_names.add(name)
        variants.append(variant)

    current_kind: str | None = None
    for value in values or []:
        parsed_variants, current_kind = _parse_embedding_variant_value(value, current_kind=current_kind)
        for variant in parsed_variants:
            add_variant(variant)
    for cross_group in cross_values or []:
        for variant in _parse_embedding_variant_cross(cross_group):
            add_variant(variant)
    return variants


def default_dense_quantized_embedding_variants() -> list[dict[str, Any]]:
    return parse_embedding_variants(["int8,binary", "rescore:int8,binary"])


def default_sparse_truncation_embedding_variants() -> list[dict[str, Any]]:
    return parse_embedding_variants(
        None,
        [
            [
                "sparse-query-max-active-dims:8,16,24,32",
                "sparse-document-max-active-dims:64,128,256,512",
            ]
        ],
    )


def dense_embedding_variants(
    values: list[str] | None,
    cross_values: list[list[str]] | None = None,
    *,
    include_defaults: bool = True,
) -> list[dict[str, Any]]:
    variants = parse_embedding_variants(values, cross_values)
    if not include_defaults:
        return variants

    truncate_dims = _truncate_dims_from_variants(variants)
    default_variants = default_dense_quantized_embedding_variants()
    auto_variants = [
        *default_variants,
        *_default_truncate_embedding_variants(truncate_dims),
        *_default_truncate_quantized_embedding_variants(truncate_dims),
    ]
    return _dedupe_variants([*variants, *auto_variants])


def sparse_embedding_variants(
    values: list[str] | None,
    cross_values: list[list[str]] | None = None,
    *,
    include_defaults: bool = True,
) -> list[dict[str, Any]]:
    variants = parse_embedding_variants(values, cross_values)
    if not include_defaults:
        return variants
    return _dedupe_variants([*variants, *default_sparse_truncation_embedding_variants()])


def _default_truncate_embedding_variants(dims: list[int]) -> list[dict[str, Any]]:
    if not dims:
        return []
    return parse_embedding_variants(["truncate:" + ",".join(str(dim) for dim in dims)])


def _default_truncate_quantized_embedding_variants(dims: list[int]) -> list[dict[str, Any]]:
    variants: list[dict[str, Any]] = []
    for dim in dims:
        truncate_spec = f"truncate:{dim}"
        variants.extend(
            parse_embedding_variants(
                None,
                [
                    [truncate_spec, "int8,binary"],
                    [truncate_spec, "rescore:int8,binary"],
                ],
            )
        )
    return variants


def _truncate_dims_from_variants(variants: list[dict[str, Any]]) -> list[int]:
    dims: list[int] = []
    seen: set[int] = set()
    for variant in variants:
        for step in _pipeline_steps(variant):
            if step.get("type") != "truncate":
                continue
            parameters = step.get("parameters")
            if not isinstance(parameters, dict):
                continue
            dim = parameters.get("dim")
            if not isinstance(dim, int) or dim in seen:
                continue
            seen.add(dim)
            dims.append(dim)
    return dims


def _dedupe_variants(variants: list[dict[str, Any]]) -> list[dict[str, Any]]:
    deduped: list[dict[str, Any]] = []
    seen_names: set[str] = set()
    for variant in variants:
        name = str(variant["name"])
        if name in seen_names:
            continue
        seen_names.add(name)
        deduped.append(variant)
    return deduped


def _split_tokens(value: str) -> list[str]:
    return [token.strip() for token in value.split(",") if token.strip()]


def _parse_embedding_variant_value(
    value: str,
    *,
    current_kind: str | None = None,
) -> tuple[list[dict[str, Any]], str | None]:
    variants: list[dict[str, Any]] = []
    for token in _split_tokens(value):
        variant, current_kind = _parse_embedding_variant(token, current_kind=current_kind)
        variants.append(variant)
    return variants, current_kind


def _parse_embedding_variant_cross(values: list[str]) -> list[dict[str, Any]]:
    if len(values) < 2:
        raise ValueError("--embedding-variant-grid requires at least two variant specs.")

    variant_groups: list[list[dict[str, Any]]] = []
    for value in values:
        variants, _current_kind = _parse_embedding_variant_value(value)
        if not variants:
            raise ValueError("--embedding-variant-grid received an empty variant spec.")
        variant_groups.append(variants)

    crossed: list[dict[str, Any]] = []
    for variant_tuple in product(*variant_groups):
        name_parts = [str(variant["name"]) for variant in variant_tuple]
        steps: list[dict[str, Any]] = []
        for variant in variant_tuple:
            steps.extend(copy.deepcopy(_pipeline_steps(variant)))
        crossed.append(_pipeline_variant(name_parts, steps))
    return crossed


def _parse_embedding_variant(token: str, *, current_kind: str | None = None) -> tuple[dict[str, Any], str]:
    if token in NORMALIZE_TOKENS:
        return _normalize_variant(), "normalize"
    elif token.startswith("normalize:") or token.startswith("normalize="):
        algorithm = token.split(":", 1)[1] if ":" in token else token.split("=", 1)[1]
        if algorithm != "l2":
            raise ValueError(f"Embedding variant '{token}' has unsupported normalize algorithm {algorithm!r}.")
        return _normalize_variant(), "normalize"
    elif token.startswith("truncate:"):
        dim_value = token.split(":", 1)[1]
        return _truncate_variant(token=token, dim_value=dim_value), "truncate"
    elif token.startswith("truncate="):
        dim_value = token.split("=", 1)[1]
        return _truncate_variant(token=token, dim_value=dim_value), "truncate"
    elif token.startswith("truncate_dim:"):
        dim_value = token.split(":", 1)[1]
        return _truncate_variant(token=token, dim_value=dim_value), "truncate"
    elif token.startswith("truncate_dim="):
        dim_value = token.split("=", 1)[1]
        return _truncate_variant(token=token, dim_value=dim_value), "truncate"
    elif current_kind == "truncate" and _is_integer_token(token):
        dim_value = token
        return _truncate_variant(token=token, dim_value=dim_value), "truncate"
    elif token.startswith(SPARSE_QUERY_MAX_ACTIVE_DIMS_PREFIXES):
        dim_value = token.split(":", 1)[1]
        return _truncate_sparse_max_dims_variant(
            token=token,
            dim_value=dim_value,
            target="query",
        ), "sparse_max_active_dims:query"
    elif token.startswith(SPARSE_QUERY_MAX_ACTIVE_DIMS_EQUALS_PREFIXES):
        dim_value = token.split("=", 1)[1]
        return _truncate_sparse_max_dims_variant(
            token=token,
            dim_value=dim_value,
            target="query",
        ), "sparse_max_active_dims:query"
    elif token.startswith(SPARSE_DOCUMENT_MAX_ACTIVE_DIMS_PREFIXES):
        dim_value = token.split(":", 1)[1]
        return _truncate_sparse_max_dims_variant(
            token=token,
            dim_value=dim_value,
            target="corpus",
        ), "sparse_max_active_dims:corpus"
    elif token.startswith(SPARSE_DOCUMENT_MAX_ACTIVE_DIMS_EQUALS_PREFIXES):
        dim_value = token.split("=", 1)[1]
        return _truncate_sparse_max_dims_variant(
            token=token,
            dim_value=dim_value,
            target="corpus",
        ), "sparse_max_active_dims:corpus"
    elif (
        current_kind is not None
        and current_kind.startswith("sparse_max_active_dims:")
        and _is_integer_token(token)
    ):
        dim_value = token
        target = current_kind.split(":", 1)[1]
        return _truncate_sparse_max_dims_variant(token=token, dim_value=dim_value, target=target), current_kind
    elif token.startswith("rescore:"):
        precision = token.split(":", 1)[1]
        return _quantize_variant(token=token, precision=precision, rescore=True), "quantize:rescore"
    elif token.startswith("rescore="):
        precision = token.split("=", 1)[1]
        return _quantize_variant(token=token, precision=precision, rescore=True), "quantize:rescore"
    elif current_kind == "quantize:rescore" and token in QUANTIZED_PRECISIONS:
        return _quantize_variant(token=token, precision=token, rescore=True), current_kind
    elif token in QUANTIZED_PRECISIONS:
        return _quantize_variant(token=token, precision=token, rescore=False), "quantize:no_rescore"
    elif token.endswith("-rescore") or token.endswith("_rescore"):
        precision = token.rsplit("-", 1)[0] if token.endswith("-rescore") else token.rsplit("_", 1)[0]
        return _quantize_variant(token=token, precision=precision, rescore=True), "quantize:rescore"
    else:
        raise ValueError(
            "Unsupported embedding variant "
            f"'{token}'. Supported syntax: truncate:DIM, sparse-query-max-active-dims:DIM, "
            "sparse-document-max-active-dims:DIM, "
            "normalize, int8, binary, rescore:int8, rescore:binary, int8-rescore, "
            "or binary-rescore"
        )


def _is_integer_token(token: str) -> bool:
    return token.isdigit() or (token.startswith("+") and token[1:].isdigit())


def _truncate_variant(*, token: str, dim_value: str) -> dict[str, Any]:
    try:
        dim = int(dim_value)
    except ValueError as exc:
        raise ValueError(f"Embedding variant '{token}' has a non-integer truncate dimension.") from exc
    if dim <= 0:
        raise ValueError(f"Embedding variant '{token}' must use a positive truncate dimension.")

    return {
        "name": f"truncate_dim_{dim}",
        "transform": _pipeline_transform(
            {
                "type": "truncate",
                "algorithm": "dimension_slice",
                "parameters": {"dim": dim},
            }
        ),
    }


def _normalize_variant() -> dict[str, Any]:
    return {
        "name": "normalize",
        "transform": _pipeline_transform(_normalize_step()),
    }


def _normalize_step() -> dict[str, Any]:
    return {
        "type": "normalize",
        "algorithm": "l2",
        "parameters": {},
    }


def _truncate_sparse_max_dims_variant(*, token: str, dim_value: str, target: str) -> dict[str, Any]:
    try:
        max_dims = int(dim_value)
    except ValueError as exc:
        raise ValueError(f"Embedding variant '{token}' has a non-integer sparse max dims value.") from exc
    if max_dims <= 0:
        raise ValueError(f"Embedding variant '{token}' must use a positive sparse max dims value.")
    if target not in {"query", "corpus"}:
        raise ValueError(f"Embedding variant '{token}' has unsupported sparse max dims target {target!r}.")

    name_prefix = {
        "query": "sparse_query_max_active_dims",
        "corpus": "sparse_document_max_active_dims",
    }[target]
    return {
        "name": f"{name_prefix}_{max_dims}",
        "transform": _pipeline_transform(
            {
                "type": "truncate_sparse_max_dims",
                "algorithm": "top_abs_values_per_row",
                "parameters": {"max_dims": max_dims, "target": target},
            }
        ),
    }


def _pipeline_transform(*steps: dict[str, Any]) -> dict[str, Any]:
    # Normalize every CLI shorthand into this shape so evaluation has one
    # low-overhead post-encode pipeline path for single and cross variants.
    return {"type": "pipeline", "steps": _dedupe_adjacent_normalize_steps(list(steps))}


def _pipeline_variant(name_parts: list[str], steps: list[dict[str, Any]]) -> dict[str, Any]:
    return {"name": "_".join(name_parts), "transform": _pipeline_transform(*steps)}


def _dedupe_adjacent_normalize_steps(steps: list[dict[str, Any]]) -> list[dict[str, Any]]:
    deduped: list[dict[str, Any]] = []
    for step in steps:
        if deduped and _is_normalize_step(deduped[-1]) and _is_normalize_step(step):
            continue
        deduped.append(step)
    return deduped


def _is_normalize_step(step: dict[str, Any]) -> bool:
    return step.get("type") == "normalize"


def _pipeline_steps(variant: dict[str, Any]) -> list[dict[str, Any]]:
    transform = variant.get("transform", {})
    if transform.get("type") != "pipeline":
        raise ValueError(f"Embedding variant {variant.get('name')!r} is not a pipeline variant.")
    steps = transform.get("steps")
    if not isinstance(steps, list) or not steps:
        raise ValueError(f"Embedding variant {variant.get('name')!r} has no pipeline steps.")
    return steps


def _quantize_variant(
    *,
    token: str,
    precision: str,
    rescore: bool,
) -> dict[str, Any]:
    if precision not in QUANTIZED_PRECISIONS:
        raise ValueError(
            f"Embedding variant '{token}' has unsupported quantized precision {precision!r}. "
            f"Supported quantized precisions are: {', '.join(sorted(QUANTIZED_PRECISIONS))}."
        )
    score_representation = TORCH_RESCORE_SCORE_REPRESENTATION if rescore else TORCH_SCORE_REPRESENTATION
    parameters: dict[str, Any] = {
        "precision": precision,
        "target": "query_and_corpus",
        "method": "query_and_corpus",
        "score_representation": score_representation,
    }
    if precision == "int8":
        parameters["calibration"] = "corpus"

    name = f"{precision}_rescore" if rescore else precision
    return {
        "name": name,
        "transform": _pipeline_transform(
            _normalize_step(),
            {
                "type": "quantize",
                "algorithm": "sentence_transformers_embedding_quantization",
                "parameters": parameters,
            }
        ),
    }
