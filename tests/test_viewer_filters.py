from __future__ import annotations

from hakari_bench.viewer.filters import (
    FILTER_NONE_VALUE,
    FilterContext,
    active_model_filter_terms,
    row_filter_context,
    visible_row_count,
)
from hakari_bench.viewer.leaderboard import LeaderboardRow
from hakari_bench.viewer.state import FilterState


def test_row_filter_context_defaults_to_all_available_facets_when_filters_are_inactive() -> None:
    context = row_filter_context(
        _rows(),
        FilterState(filters_active=False, dim_filters=(FILTER_NONE_VALUE,), quant_filters=(FILTER_NONE_VALUE,)),
    )

    assert context.dim_options == [("384", "384 dims"), ("768", "768 dims"), ("__unknown__", "Unknown")]
    assert context.quant_options == [("__none__", "Original"), ("binary", "binary"), ("int8", "int8")]
    assert context.selected_dims == {"384", "768", "__unknown__"}
    assert context.selected_quants == {"__none__", "binary", "int8"}


def test_row_filter_context_keeps_empty_selection_as_none_when_filters_are_active() -> None:
    context = row_filter_context(_rows(), FilterState(filters_active=True, dim_filters=(FILTER_NONE_VALUE,)))

    assert context.selected_dims == set()
    assert visible_row_count(_rows(), context) == 0


def test_visible_row_count_uses_same_context_as_row_visibility() -> None:
    rows = _rows()
    context = row_filter_context(
        rows,
        FilterState(
            model_filter="jina",
            filters_active=True,
            dim_filters=("768",),
            quant_filters=("binary",),
            dtype_filters=("bf16",),
            attn_filters=("sdpa",),
            prompt_filters=("model_default",),
        ),
    )

    assert [row.model_name for row in rows if context.is_visible(row)] == ["jina/b"]
    assert visible_row_count(rows, context) == 1


def test_short_model_filter_terms_do_not_hide_rows() -> None:
    context = row_filter_context(_rows(), FilterState(model_filter="ji"))

    assert active_model_filter_terms("ji") == ()
    assert visible_row_count(_rows(), context) == 4


def test_filter_context_can_order_selected_values_for_query_payloads() -> None:
    context = FilterContext(
        dim_options=[("384", "384 dims"), ("768", "768 dims")],
        quant_options=[("__none__", "Original"), ("binary", "binary")],
        dtype_options=[],
        attn_options=[],
        prompt_options=[],
        selected_dims={"768", "384"},
        selected_quants={"binary"},
    )

    assert context.ordered_selected_dims() == ["384", "768"]
    assert context.ordered_selected_quants() == ["binary"]


def _rows() -> list[LeaderboardRow]:
    return [
        _row("jina/a", embedding_dim=768, quantization=None, dtype="bf16", attn="sdpa", prompt=None),
        _row("jina/b", embedding_dim=768, quantization="binary", dtype="bf16", attn="sdpa", prompt=None),
        _row("other/c", embedding_dim=384, quantization="int8", dtype=None, attn=None, prompt="prompt names"),
        _row("unknown/d", embedding_dim=None, quantization=None, dtype=None, attn=None, prompt=None),
    ]


def _row(
    model_name: str,
    *,
    embedding_dim: int | None,
    quantization: str | None,
    dtype: str | None,
    attn: str | None,
    prompt: str | None,
) -> LeaderboardRow:
    return LeaderboardRow(
        borda_rank=1,
        mean_rank=1,
        model_name=model_name,
        borda_score=100,
        mean_score=100,
        task_count=1,
        embedding_dim=embedding_dim,
        quantization=quantization,
        dtype=dtype,
        attn_implementation=attn,
        prompt_summary=prompt,
    )
