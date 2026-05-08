from __future__ import annotations

from dataclasses import dataclass, field

from hakari_bench.viewer.leaderboard import LeaderboardRow
from hakari_bench.viewer.state import FilterState
from hakari_bench.viewer.text_match import active_filter_terms, text_matches_filter_terms


FILTER_NONE_VALUE = "__none_selected__"
FilterOption = tuple[str, str]


@dataclass(frozen=True)
class FilterContext:
    dim_options: list[FilterOption] = field(default_factory=list)
    quant_options: list[FilterOption] = field(default_factory=list)
    dtype_options: list[FilterOption] = field(default_factory=list)
    attn_options: list[FilterOption] = field(default_factory=list)
    prompt_options: list[FilterOption] = field(default_factory=list)
    selected_dims: set[str] = field(default_factory=set)
    selected_quants: set[str] = field(default_factory=set)
    selected_dtypes: set[str] = field(default_factory=set)
    selected_attn: set[str] = field(default_factory=set)
    selected_prompts: set[str] = field(default_factory=set)
    model_filter_terms: tuple[str, ...] = ()

    def is_visible(self, row: LeaderboardRow) -> bool:
        return not (
            bool(self.model_filter_terms and not model_name_matches_filter_terms(row.model_name, self.model_filter_terms))
            or dim_bucket(row.embedding_dim) not in self.selected_dims
            or quant_bucket(row.quantization) not in self.selected_quants
            or dtype_bucket(row.dtype) not in self.selected_dtypes
            or attn_bucket(row.attn_implementation) not in self.selected_attn
            or prompt_bucket(row.prompt_summary) not in self.selected_prompts
        )

    def ordered_selected_dims(self) -> list[str]:
        return ordered_selected_values(self.dim_options, self.selected_dims)

    def ordered_selected_quants(self) -> list[str]:
        return ordered_selected_values(self.quant_options, self.selected_quants)

    def ordered_selected_dtypes(self) -> list[str]:
        return ordered_selected_values(self.dtype_options, self.selected_dtypes)

    def ordered_selected_attn(self) -> list[str]:
        return ordered_selected_values(self.attn_options, self.selected_attn)

    def ordered_selected_prompts(self) -> list[str]:
        return ordered_selected_values(self.prompt_options, self.selected_prompts)


def row_filter_context(rows: list[LeaderboardRow], filter_state: FilterState) -> FilterContext:
    dim_options = dim_filter_options(rows)
    quant_options = quant_filter_options(rows)
    dtype_options = dtype_filter_options(rows)
    attn_options = attn_filter_options(rows)
    prompt_options = prompt_filter_options(rows)
    return FilterContext(
        dim_options=dim_options,
        quant_options=quant_options,
        dtype_options=dtype_options,
        attn_options=attn_options,
        prompt_options=prompt_options,
        selected_dims=selected_filter_values(
            options=dim_options,
            selected=filter_state.dim_filters,
            filters_active=filter_state.filters_active,
        ),
        selected_quants=selected_filter_values(
            options=quant_options,
            selected=filter_state.quant_filters,
            filters_active=filter_state.filters_active,
        ),
        selected_dtypes=selected_filter_values(
            options=dtype_options,
            selected=filter_state.dtype_filters,
            filters_active=filter_state.filters_active,
        ),
        selected_attn=selected_filter_values(
            options=attn_options,
            selected=filter_state.attn_filters,
            filters_active=filter_state.filters_active,
        ),
        selected_prompts=selected_filter_values(
            options=prompt_options,
            selected=filter_state.prompt_filters,
            filters_active=filter_state.filters_active,
        ),
        model_filter_terms=active_model_filter_terms(filter_state.model_filter),
    )


def visible_row_count(rows: list[LeaderboardRow], context: FilterContext) -> int:
    return sum(1 for row in rows if context.is_visible(row))


def active_model_filter_terms(model_filter: str) -> tuple[str, ...]:
    return active_filter_terms(model_filter)


def model_name_matches_filter_terms(model_name: str, terms: tuple[str, ...]) -> bool:
    return text_matches_filter_terms(model_name, terms)


def task_name_matches_filter_terms(task_name: str, terms: tuple[str, ...]) -> bool:
    return text_matches_filter_terms(task_name, terms)


def dim_filter_options(rows: list[LeaderboardRow]) -> list[FilterOption]:
    buckets = {dim_bucket(row.embedding_dim) for row in rows}
    return sorted(
        ((bucket, dim_bucket_label(bucket)) for bucket in buckets),
        key=lambda item: dim_bucket_sort_key(item[0]),
    )


def quant_filter_options(rows: list[LeaderboardRow]) -> list[FilterOption]:
    buckets = {quant_bucket(row.quantization) for row in rows}
    return sorted(
        ((bucket, quant_bucket_label(bucket)) for bucket in buckets),
        key=lambda item: quant_bucket_sort_key(item[0]),
    )


def dtype_filter_options(rows: list[LeaderboardRow]) -> list[FilterOption]:
    buckets = {dtype_bucket(row.dtype) for row in rows}
    return sorted(
        ((bucket, dtype_bucket_label(bucket)) for bucket in buckets),
        key=lambda item: dtype_bucket_sort_key(item[0]),
    )


def attn_filter_options(rows: list[LeaderboardRow]) -> list[FilterOption]:
    buckets = {attn_bucket(row.attn_implementation) for row in rows}
    return sorted(
        ((bucket, attn_bucket_label(bucket)) for bucket in buckets),
        key=lambda item: attn_bucket_sort_key(item[0]),
    )


def prompt_filter_options(rows: list[LeaderboardRow]) -> list[FilterOption]:
    buckets = {prompt_bucket(row.prompt_summary) for row in rows}
    return sorted(
        ((bucket, prompt_bucket_label(bucket)) for bucket in buckets),
        key=lambda item: prompt_bucket_sort_key(item[0]),
    )


def selected_filter_values(
    *,
    options: list[FilterOption],
    selected: tuple[str, ...],
    filters_active: bool,
) -> set[str]:
    available = {value for value, _ in options}
    if not filters_active:
        return available
    if not selected:
        return available
    return {value for value in selected if value in available}


def ordered_selected_values(options: list[FilterOption], selected_values: set[str]) -> list[str]:
    return [value for value, _ in options if value in selected_values]


def dim_bucket(value: int | None) -> str:
    if value is None:
        return "__unknown__"
    if value >= 1025:
        return "1025+"
    return str(value)


def dim_bucket_label(bucket: str) -> str:
    if bucket == "__unknown__":
        return "Unknown"
    if bucket == "1025+":
        return "1025~ dims"
    return f"{int(bucket):,} dims"


def dim_bucket_sort_key(bucket: str) -> tuple[int, int]:
    if bucket == "__unknown__":
        return (1, 0)
    if bucket == "1025+":
        return (0, 1025)
    return (0, int(bucket))


def quant_bucket(value: str | None) -> str:
    return value or "__none__"


def quant_bucket_label(bucket: str) -> str:
    return "Original" if bucket == "__none__" else bucket


def quant_bucket_sort_key(bucket: str) -> tuple[int, str]:
    return (0, "") if bucket == "__none__" else (1, bucket)


def dtype_bucket(value: str | None) -> str:
    return value or "__unknown__"


def dtype_bucket_label(bucket: str) -> str:
    return "Unknown" if bucket == "__unknown__" else bucket.upper()


def dtype_bucket_sort_key(bucket: str) -> tuple[int, str]:
    return (1, "") if bucket == "__unknown__" else (0, bucket)


def dtype_label(value: str | None) -> str:
    return "" if value is None else value.upper()


def attn_bucket(value: str | None) -> str:
    return value or "__unknown__"


def attn_bucket_label(bucket: str) -> str:
    return "Unknown" if bucket == "__unknown__" else attn_label(bucket)


def attn_bucket_sort_key(bucket: str) -> tuple[int, str]:
    order = {"flash_attention_2": "0", "sdpa": "1", "__unknown__": "9"}
    return (1 if bucket == "__unknown__" else 0, order.get(bucket, bucket))


def attn_label(value: str | None) -> str:
    if value is None:
        return ""
    labels = {
        "flash_attention_2": "FA2",
        "sdpa": "SDPA",
    }
    return labels.get(value, value)


def prompt_bucket(value: str | None) -> str:
    if value is None:
        return "model_default"
    return value.replace(" + ", "_").replace(" ", "_")


def prompt_bucket_label(bucket: str) -> str:
    labels = {
        "explicit_prefixes": "Explicit prefixes",
        "prompt_names": "Prompt names",
        "prompt_names_encode_tasks": "Prompt names + encode tasks",
        "encode_tasks": "Encode tasks",
        "model_default": "Model default",
    }
    return labels.get(bucket, bucket.replace("_", " ").title())


def prompt_bucket_sort_key(bucket: str) -> tuple[int, str]:
    order = {
        "explicit_prefixes": "0",
        "prompt_names": "1",
        "prompt_names_encode_tasks": "2",
        "encode_tasks": "3",
        "model_default": "4",
    }
    return (0, order.get(bucket, bucket))


def prompt_label(value: str | None) -> str:
    return prompt_bucket_label(prompt_bucket(value))
