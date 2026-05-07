from __future__ import annotations

from dataclasses import dataclass
from typing import Mapping


@dataclass(frozen=True)
class VariantDisplayFlags:
    quantization: bool = False
    truncate: bool = False
    rescore: bool = False
    other: bool = False

    @property
    def any_enabled(self) -> bool:
        return self.quantization or self.truncate or self.rescore or self.other


def variant_display_flags_from_values(
    *,
    variants: bool = False,
    quantization: bool = False,
    truncate: bool = False,
    rescore: bool = False,
    other: bool = False,
) -> VariantDisplayFlags:
    if variants:
        return VariantDisplayFlags(quantization=True, truncate=True, rescore=True, other=True)
    return VariantDisplayFlags(
        quantization=quantization,
        truncate=truncate,
        rescore=rescore,
        other=other,
    )


def variant_display_flags_from_query(query: Mapping[str, object]) -> VariantDisplayFlags:
    return VariantDisplayFlags(
        quantization=query.get("quantization") == "1",
        truncate=query.get("truncate") == "1",
        rescore=query.get("rescore") == "1",
        other=query.get("other_variant") == "1",
    )


def include_variant_row(
    *,
    embedding_variant_name: str | None,
    quantization: str | None,
    flags: VariantDisplayFlags,
) -> bool:
    if embedding_variant_name is None:
        return True

    category = variant_category(embedding_variant_name=embedding_variant_name, quantization=quantization)
    if category.rescore:
        return flags.rescore
    if category.quantization or category.truncate:
        return (not category.quantization or flags.quantization) and (not category.truncate or flags.truncate)
    return flags.other


@dataclass(frozen=True)
class VariantCategory:
    quantization: bool = False
    truncate: bool = False
    rescore: bool = False


def variant_category(*, embedding_variant_name: str, quantization: str | None) -> VariantCategory:
    normalized_name = embedding_variant_name.lower()
    return VariantCategory(
        quantization=quantization is not None or "quantize" in normalized_name,
        truncate="truncate" in normalized_name,
        rescore="rescore" in normalized_name,
    )
