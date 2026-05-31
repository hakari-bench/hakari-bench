from __future__ import annotations

from hakari_bench.viewer.variant_display import (
    VariantDisplayFlags,
    include_variant_row,
    variant_display_flags_from_query,
    variant_display_flags_from_values,
)


def test_variant_display_flags_are_explicit_query_state_not_filter_inference() -> None:
    flags = variant_display_flags_from_query(
        {
            "quantization": "1",
            "filters": "1",
            "dim_filter": ["32", "64", "128"],
            "quant_filter": ["binary", "int8"],
        }
    )

    assert flags == VariantDisplayFlags(quantization=True)


def test_legacy_variants_flag_enables_all_variant_display_flags() -> None:
    assert variant_display_flags_from_values(variants=True) == VariantDisplayFlags(
        quantization=True,
        truncate=True,
        rescore=True,
        other=True,
    )


def test_quantization_only_excludes_truncate_quantization_cross_variant() -> None:
    flags = VariantDisplayFlags(quantization=True)

    assert include_variant_row(
        embedding_variant_name=None,
        quantization=None,
        flags=flags,
    )
    assert include_variant_row(
        embedding_variant_name="quantize_uint8_docs",
        quantization="uint8",
        flags=flags,
    )
    assert not include_variant_row(
        embedding_variant_name="truncate_dim_256_quantize_int8_docs",
        quantization="int8",
        flags=flags,
    )


def test_truncate_only_excludes_truncate_quantization_cross_variant() -> None:
    flags = VariantDisplayFlags(truncate=True)

    assert include_variant_row(
        embedding_variant_name="truncate_dim_384",
        quantization=None,
        flags=flags,
    )
    assert not include_variant_row(
        embedding_variant_name="truncate_dim_256_quantize_int8_docs",
        quantization="int8",
        flags=flags,
    )


def test_cross_variant_requires_quantization_and_truncate_flags() -> None:
    flags = VariantDisplayFlags(quantization=True, truncate=True)

    assert include_variant_row(
        embedding_variant_name="truncate_dim_256_quantize_int8_docs",
        quantization="int8",
        flags=flags,
    )


def test_rescore_is_not_included_by_quantization_flag() -> None:
    assert not include_variant_row(
        embedding_variant_name="binary_rescore",
        quantization="binary",
        flags=VariantDisplayFlags(quantization=True),
    )
    assert include_variant_row(
        embedding_variant_name="binary_rescore",
        quantization="binary",
        flags=VariantDisplayFlags(rescore=True),
    )
