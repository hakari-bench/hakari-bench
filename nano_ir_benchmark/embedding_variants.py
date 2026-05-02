from __future__ import annotations

import copy
from itertools import product
from typing import Any

QUANTIZE_PRECISIONS = {"int8", "uint8", "binary", "ubinary"}
QUANTIZE_TARGETS = {"corpus", "query_and_corpus"}
TRUNCATE_SPARSE_QUERY_MAX_DIMS_PREFIXES = (
    "truncate-sparse-query-max-dims:",
    "truncate_sparse_query_max_dims:",
    "truncate-query-sparse-max-dims:",
    "truncate_query_sparse_max_dims:",
    "truncate-sparse-query-topk:",
    "truncate_sparse_query_topk:",
)
TRUNCATE_SPARSE_QUERY_MAX_DIMS_EQUALS_PREFIXES = tuple(
    prefix.replace(":", "=") for prefix in TRUNCATE_SPARSE_QUERY_MAX_DIMS_PREFIXES
)
TRUNCATE_SPARSE_DOCS_MAX_DIMS_PREFIXES = (
    "truncate-sparse-docs-max-dims:",
    "truncate_sparse_docs_max_dims:",
    "truncate-sparse-corpus-max-dims:",
    "truncate_sparse_corpus_max_dims:",
    "truncate-docs-sparse-max-dims:",
    "truncate_docs_sparse_max_dims:",
    "truncate-corpus-sparse-max-dims:",
    "truncate_corpus_sparse_max_dims:",
    "truncate-sparse-docs-topk:",
    "truncate_sparse_docs_topk:",
    "truncate-sparse-corpus-topk:",
    "truncate_sparse_corpus_topk:",
)
TRUNCATE_SPARSE_DOCS_MAX_DIMS_EQUALS_PREFIXES = tuple(
    prefix.replace(":", "=") for prefix in TRUNCATE_SPARSE_DOCS_MAX_DIMS_PREFIXES
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
        raise ValueError("--embedding-variant-cross requires at least two variant specs.")

    variant_groups: list[list[dict[str, Any]]] = []
    for value in values:
        variants, _current_kind = _parse_embedding_variant_value(value)
        if not variants:
            raise ValueError("--embedding-variant-cross received an empty variant spec.")
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
    if token.startswith("truncate:"):
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
    elif token.startswith(TRUNCATE_SPARSE_QUERY_MAX_DIMS_PREFIXES):
        dim_value = token.split(":", 1)[1]
        return _truncate_sparse_max_dims_variant(
            token=token,
            dim_value=dim_value,
            target="query",
        ), "truncate_sparse_max_dims:query"
    elif token.startswith(TRUNCATE_SPARSE_QUERY_MAX_DIMS_EQUALS_PREFIXES):
        dim_value = token.split("=", 1)[1]
        return _truncate_sparse_max_dims_variant(
            token=token,
            dim_value=dim_value,
            target="query",
        ), "truncate_sparse_max_dims:query"
    elif token.startswith(TRUNCATE_SPARSE_DOCS_MAX_DIMS_PREFIXES):
        dim_value = token.split(":", 1)[1]
        return _truncate_sparse_max_dims_variant(
            token=token,
            dim_value=dim_value,
            target="corpus",
        ), "truncate_sparse_max_dims:corpus"
    elif token.startswith(TRUNCATE_SPARSE_DOCS_MAX_DIMS_EQUALS_PREFIXES):
        dim_value = token.split("=", 1)[1]
        return _truncate_sparse_max_dims_variant(
            token=token,
            dim_value=dim_value,
            target="corpus",
        ), "truncate_sparse_max_dims:corpus"
    elif (
        current_kind is not None
        and current_kind.startswith("truncate_sparse_max_dims:")
        and _is_integer_token(token)
    ):
        dim_value = token
        target = current_kind.split(":", 1)[1]
        return _truncate_sparse_max_dims_variant(
            token=token,
            dim_value=dim_value,
            target=target,
        ), current_kind
    elif token.startswith(("quantize-docs:", "quantize_docs:", "quantize-corpus:", "quantize_corpus:")):
        precision = token.split(":", 1)[1]
        return _quantize_variant(token=token, precision=precision, target="corpus"), "quantize:corpus"
    elif token.startswith(("quantize-docs=", "quantize_docs=", "quantize-corpus=", "quantize_corpus=")):
        precision = token.split("=", 1)[1]
        return _quantize_variant(token=token, precision=precision, target="corpus"), "quantize:corpus"
    elif token.startswith(("quantize-both:", "quantize_both:", "quantize-query-corpus:", "quantize_query_corpus:")):
        precision = token.split(":", 1)[1]
        return _quantize_variant(token=token, precision=precision, target="query_and_corpus"), "quantize:query_and_corpus"
    elif token.startswith(("quantize-both=", "quantize_both=", "quantize-query-corpus=", "quantize_query_corpus=")):
        precision = token.split("=", 1)[1]
        return _quantize_variant(token=token, precision=precision, target="query_and_corpus"), "quantize:query_and_corpus"
    elif token.startswith("quantize:"):
        precision = token.split(":", 1)[1]
        return _quantize_variant(token=token, precision=precision, target="corpus"), "quantize:corpus"
    elif token.startswith("quantize="):
        precision = token.split("=", 1)[1]
        return _quantize_variant(token=token, precision=precision, target="corpus"), "quantize:corpus"
    elif current_kind is not None and current_kind.startswith("quantize:") and token in QUANTIZE_PRECISIONS:
        target = current_kind.split(":", 1)[1]
        if target not in QUANTIZE_TARGETS:
            raise ValueError(f"Unsupported quantization target in parser state: {target}")
        return _quantize_variant(token=token, precision=token, target=target), current_kind
    else:
        raise ValueError(
            "Unsupported embedding variant "
            f"'{token}'. Supported syntax: truncate:DIM, truncate-sparse-query-max-dims:DIM, "
            "truncate-sparse-docs-max-dims:DIM, quantize:PRECISION, or quantize-both:PRECISION"
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


def _truncate_sparse_max_dims_variant(
    *,
    token: str,
    dim_value: str,
    target: str,
) -> dict[str, Any]:
    try:
        max_dims = int(dim_value)
    except ValueError as exc:
        raise ValueError(f"Embedding variant '{token}' has a non-integer sparse max dims value.") from exc
    if max_dims <= 0:
        raise ValueError(f"Embedding variant '{token}' must use a positive sparse max dims value.")
    if target not in {"query", "corpus"}:
        raise ValueError(f"Embedding variant '{token}' has unsupported sparse max dims target {target!r}.")

    name_prefix = {
        "query": "truncate_sparse_query_max_dims",
        "corpus": "truncate_sparse_docs_max_dims",
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
    return {"type": "pipeline", "steps": list(steps)}


def _pipeline_variant(name_parts: list[str], steps: list[dict[str, Any]]) -> dict[str, Any]:
    return {"name": "_".join(name_parts), "transform": _pipeline_transform(*steps)}


def _pipeline_steps(variant: dict[str, Any]) -> list[dict[str, Any]]:
    transform = variant.get("transform", {})
    if transform.get("type") != "pipeline":
        raise ValueError(f"Embedding variant {variant.get('name')!r} is not a pipeline variant.")
    steps = transform.get("steps")
    if not isinstance(steps, list) or not steps:
        raise ValueError(f"Embedding variant {variant.get('name')!r} has no pipeline steps.")
    return steps


def _quantize_variant(*, token: str, precision: str, target: str) -> dict[str, Any]:
    if precision not in QUANTIZE_PRECISIONS:
        raise ValueError(
            f"Embedding variant '{token}' has unsupported quantization precision {precision!r}. "
            f"Supported precisions are: {', '.join(sorted(QUANTIZE_PRECISIONS))}."
        )
    if target not in QUANTIZE_TARGETS:
        raise ValueError(
            f"Embedding variant '{token}' has unsupported quantization target {target!r}. "
            f"Supported targets are: {', '.join(sorted(QUANTIZE_TARGETS))}."
        )

    method = "corpus_only" if target == "corpus" else "query_and_corpus"
    suffix = "docs" if target == "corpus" else "both"
    parameters: dict[str, Any] = {"precision": precision, "target": target, "method": method}
    if precision in {"int8", "uint8"}:
        parameters["calibration"] = "corpus"

    return {
        "name": f"quantize_{precision}_{suffix}",
        "transform": _pipeline_transform(
            {
                "type": "quantize",
                "algorithm": "sentence_transformers_embedding_quantization",
                "parameters": parameters,
            }
        ),
    }
