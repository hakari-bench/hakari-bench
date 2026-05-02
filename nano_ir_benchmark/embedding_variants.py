from __future__ import annotations

import copy
from itertools import product
from typing import Any

USEARCH_PRECISIONS = {"int8", "binary"}
USEARCH_SCORE_REPRESENTATION = "usearch_exact"
USEARCH_RESCORE_SCORE_REPRESENTATION = "usearch_exact_rescore"
NUMPY_SCORE_REPRESENTATION = "numpy_exact"
NUMPY_RESCORE_SCORE_REPRESENTATION = "numpy_exact_rescore"
TORCH_SCORE_REPRESENTATION = "torch_exact"
TORCH_RESCORE_SCORE_REPRESENTATION = "torch_exact_rescore"
NORMALIZE_TOKENS = {"normalize", "l2-normalize", "l2_normalize"}
SPARSE_MAX_ACTIVE_DIMS_PREFIXES = (
    "sparse-max-active-dims:",
    "sparse_max_active_dims:",
    "max-active-dims:",
    "max_active_dims:",
    "sparse-topk:",
    "sparse_topk:",
)
SPARSE_MAX_ACTIVE_DIMS_EQUALS_PREFIXES = tuple(prefix.replace(":", "=") for prefix in SPARSE_MAX_ACTIVE_DIMS_PREFIXES)
SPARSE_QUERY_MAX_ACTIVE_DIMS_PREFIXES = (
    "sparse-query-max-active-dims:",
    "sparse_query_max_active_dims:",
    "query-sparse-max-active-dims:",
    "query_sparse_max_active_dims:",
    "query-max-active-dims:",
    "query_max_active_dims:",
    "sparse-query-topk:",
    "sparse_query_topk:",
)
SPARSE_QUERY_MAX_ACTIVE_DIMS_EQUALS_PREFIXES = tuple(
    prefix.replace(":", "=") for prefix in SPARSE_QUERY_MAX_ACTIVE_DIMS_PREFIXES
)
SPARSE_DOCS_MAX_ACTIVE_DIMS_PREFIXES = (
    "sparse-docs-max-active-dims:",
    "sparse_docs_max_active_dims:",
    "sparse-corpus-max-active-dims:",
    "sparse_corpus_max_active_dims:",
    "docs-sparse-max-active-dims:",
    "docs_sparse_max_active_dims:",
    "corpus-sparse-max-active-dims:",
    "corpus_sparse_max_active_dims:",
    "docs-max-active-dims:",
    "docs_max_active_dims:",
    "corpus-max-active-dims:",
    "corpus_max_active_dims:",
    "sparse-docs-topk:",
    "sparse_docs_topk:",
    "sparse-corpus-topk:",
    "sparse_corpus_topk:",
)
SPARSE_DOCS_MAX_ACTIVE_DIMS_EQUALS_PREFIXES = tuple(
    prefix.replace(":", "=") for prefix in SPARSE_DOCS_MAX_ACTIVE_DIMS_PREFIXES
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
    return parse_embedding_variants(["usearch:int8,binary", "usearch-rescore:int8,binary"])


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
        return _sparse_max_active_dims_variant(
            token=token,
            dim_value=dim_value,
            target="query",
        ), "sparse_max_active_dims:query"
    elif token.startswith(SPARSE_QUERY_MAX_ACTIVE_DIMS_EQUALS_PREFIXES):
        dim_value = token.split("=", 1)[1]
        return _sparse_max_active_dims_variant(
            token=token,
            dim_value=dim_value,
            target="query",
        ), "sparse_max_active_dims:query"
    elif token.startswith(SPARSE_DOCS_MAX_ACTIVE_DIMS_PREFIXES):
        dim_value = token.split(":", 1)[1]
        return _sparse_max_active_dims_variant(
            token=token,
            dim_value=dim_value,
            target="corpus",
        ), "sparse_max_active_dims:corpus"
    elif token.startswith(SPARSE_DOCS_MAX_ACTIVE_DIMS_EQUALS_PREFIXES):
        dim_value = token.split("=", 1)[1]
        return _sparse_max_active_dims_variant(
            token=token,
            dim_value=dim_value,
            target="corpus",
        ), "sparse_max_active_dims:corpus"
    elif token.startswith(SPARSE_MAX_ACTIVE_DIMS_PREFIXES):
        dim_value = token.split(":", 1)[1]
        return _sparse_max_active_dims_variant(
            token=token,
            dim_value=dim_value,
            target="query_and_corpus",
        ), "sparse_max_active_dims:query_and_corpus"
    elif token.startswith(SPARSE_MAX_ACTIVE_DIMS_EQUALS_PREFIXES):
        dim_value = token.split("=", 1)[1]
        return _sparse_max_active_dims_variant(
            token=token,
            dim_value=dim_value,
            target="query_and_corpus",
        ), "sparse_max_active_dims:query_and_corpus"
    elif current_kind is not None and current_kind.startswith("sparse_max_active_dims:") and _is_integer_token(token):
        dim_value = token
        target = current_kind.split(":", 1)[1]
        return _sparse_max_active_dims_variant(token=token, dim_value=dim_value, target=target), current_kind
    elif token.startswith("usearch-rescore:"):
        precision = token.split(":", 1)[1]
        return _usearch_variant(token=token, precision=precision, rescore=True), "usearch:rescore"
    elif token.startswith("usearch:"):
        precision = token.split(":", 1)[1]
        return _usearch_variant(token=token, precision=precision, rescore=False), "usearch:no_rescore"
    elif token.startswith("numpy-rescore:"):
        precision = token.split(":", 1)[1]
        return _numpy_variant(token=token, precision=precision, rescore=True), "numpy:rescore"
    elif token.startswith("numpy:"):
        precision = token.split(":", 1)[1]
        return _numpy_variant(token=token, precision=precision, rescore=False), "numpy:no_rescore"
    elif token.startswith("torch-rescore:"):
        precision = token.split(":", 1)[1]
        return _torch_variant(token=token, precision=precision, rescore=True), "torch:rescore"
    elif token.startswith("torch:"):
        precision = token.split(":", 1)[1]
        return _torch_variant(token=token, precision=precision, rescore=False), "torch:no_rescore"
    elif token.startswith("cuda-rescore:"):
        precision = token.split(":", 1)[1]
        return _torch_variant(token=token, precision=precision, rescore=True, name_prefix="cuda", device="cuda"), "cuda:rescore"
    elif token.startswith("cuda:"):
        precision = token.split(":", 1)[1]
        return _torch_variant(token=token, precision=precision, rescore=False, name_prefix="cuda", device="cuda"), "cuda:no_rescore"
    elif current_kind is not None and current_kind.startswith("usearch:") and token in USEARCH_PRECISIONS:
        rescore = current_kind.split(":", 1)[1] == "rescore"
        return _usearch_variant(token=token, precision=token, rescore=rescore), current_kind
    elif current_kind is not None and current_kind.startswith("numpy:") and token in USEARCH_PRECISIONS:
        rescore = current_kind.split(":", 1)[1] == "rescore"
        return _numpy_variant(token=token, precision=token, rescore=rescore), current_kind
    elif current_kind is not None and current_kind.startswith("torch:") and token in USEARCH_PRECISIONS:
        rescore = current_kind.split(":", 1)[1] == "rescore"
        return _torch_variant(token=token, precision=token, rescore=rescore), current_kind
    elif current_kind is not None and current_kind.startswith("cuda:") and token in USEARCH_PRECISIONS:
        rescore = current_kind.split(":", 1)[1] == "rescore"
        return _torch_variant(token=token, precision=token, rescore=rescore, name_prefix="cuda", device="cuda"), current_kind
    else:
        raise ValueError(
            "Unsupported embedding variant "
            f"'{token}'. Supported syntax: truncate:DIM, sparse-max-active-dims:DIM, "
            "normalize, usearch:PRECISION, usearch-rescore:PRECISION, numpy:PRECISION, "
            "numpy-rescore:PRECISION, torch:PRECISION, torch-rescore:PRECISION, cuda:PRECISION, "
            "or cuda-rescore:PRECISION"
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


def _sparse_max_active_dims_variant(*, token: str, dim_value: str, target: str) -> dict[str, Any]:
    try:
        max_active_dims = int(dim_value)
    except ValueError as exc:
        raise ValueError(f"Embedding variant '{token}' has a non-integer sparse max active dims value.") from exc
    if max_active_dims <= 0:
        raise ValueError(f"Embedding variant '{token}' must use a positive sparse max active dims value.")
    if target not in {"query", "corpus", "query_and_corpus"}:
        raise ValueError(f"Embedding variant '{token}' has unsupported sparse max active dims target {target!r}.")

    name_prefix = {
        "query": "sparse_query_max_active_dims",
        "corpus": "sparse_docs_max_active_dims",
        "query_and_corpus": "sparse_max_active_dims",
    }[target]
    return {
        "name": f"{name_prefix}_{max_active_dims}",
        "transform": _pipeline_transform(
            {
                "type": "sparse_max_active_dims",
                "algorithm": "top_abs_values_per_row",
                "parameters": {"max_active_dims": max_active_dims, "target": target},
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
    if precision not in USEARCH_PRECISIONS:
        raise ValueError(
            f"Embedding variant '{token}' has unsupported usearch precision {precision!r}. "
            f"Supported usearch precisions are: {', '.join(sorted(USEARCH_PRECISIONS))}."
        )
    score_representation = USEARCH_RESCORE_SCORE_REPRESENTATION if rescore else USEARCH_SCORE_REPRESENTATION
    parameters: dict[str, Any] = {
        "precision": precision,
        "target": "query_and_corpus",
        "method": "query_and_corpus",
        "score_representation": score_representation,
    }
    if precision == "int8":
        parameters["calibration"] = "corpus"

    name = f"usearch_{precision}_rescore" if rescore else f"usearch_{precision}"
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


def _usearch_variant(*, token: str, precision: str, rescore: bool) -> dict[str, Any]:
    return _quantize_variant(token=token, precision=precision, rescore=rescore)


def _numpy_variant(*, token: str, precision: str, rescore: bool) -> dict[str, Any]:
    if precision not in USEARCH_PRECISIONS:
        raise ValueError(
            f"Embedding variant '{token}' has unsupported numpy precision {precision!r}. "
            f"Supported numpy precisions are: {', '.join(sorted(USEARCH_PRECISIONS))}."
        )
    score_representation = NUMPY_RESCORE_SCORE_REPRESENTATION if rescore else NUMPY_SCORE_REPRESENTATION
    parameters: dict[str, Any] = {
        "precision": precision,
        "target": "query_and_corpus",
        "method": "query_and_corpus",
        "score_representation": score_representation,
    }
    if precision == "int8":
        parameters["calibration"] = "corpus"

    name = f"numpy_{precision}_rescore" if rescore else f"numpy_{precision}"
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


def _torch_variant(
    *,
    token: str,
    precision: str,
    rescore: bool,
    name_prefix: str = "torch",
    device: str | None = None,
) -> dict[str, Any]:
    if precision not in USEARCH_PRECISIONS:
        raise ValueError(
            f"Embedding variant '{token}' has unsupported torch precision {precision!r}. "
            f"Supported torch precisions are: {', '.join(sorted(USEARCH_PRECISIONS))}."
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
    if device is not None:
        parameters["search_device"] = device

    name = f"{name_prefix}_{precision}_rescore" if rescore else f"{name_prefix}_{precision}"
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
