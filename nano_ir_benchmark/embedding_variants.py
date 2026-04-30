from __future__ import annotations

from typing import Any


def parse_embedding_variants(values: list[str] | None) -> list[dict[str, Any]]:
    variants: list[dict[str, Any]] = []
    seen_names: set[str] = set()
    current_kind: str | None = None
    for value in values or []:
        for token in _split_tokens(value):
            variant, current_kind = _parse_embedding_variant(token, current_kind=current_kind)
            name = str(variant["name"])
            if name in seen_names:
                raise ValueError(f"Duplicate embedding variant: {name}")
            seen_names.add(name)
            variants.append(variant)
    return variants


def _split_tokens(value: str) -> list[str]:
    return [token.strip() for token in value.split(",") if token.strip()]


def _parse_embedding_variant(token: str, *, current_kind: str | None = None) -> tuple[dict[str, Any], str]:
    if token.startswith("truncate:"):
        dim_value = token.split(":", 1)[1]
    elif token.startswith("truncate="):
        dim_value = token.split("=", 1)[1]
    elif token.startswith("truncate_dim:"):
        dim_value = token.split(":", 1)[1]
    elif token.startswith("truncate_dim="):
        dim_value = token.split("=", 1)[1]
    elif current_kind == "truncate" and _is_integer_token(token):
        dim_value = token
    else:
        raise ValueError(
            f"Unsupported embedding variant '{token}'. Supported syntax: truncate:DIM or truncate:DIM,DIM"
        )

    return _truncate_variant(token=token, dim_value=dim_value), "truncate"


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
        "transform": {
            "type": "truncate",
            "algorithm": "dimension_slice",
            "parameters": {"dim": dim},
        },
    }
