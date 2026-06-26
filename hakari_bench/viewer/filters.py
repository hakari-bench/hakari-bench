from __future__ import annotations

from dataclasses import dataclass, field

from hakari_bench.viewer.leaderboard import LeaderboardRow
from hakari_bench.viewer.model_types import MODEL_TYPE_FILTER_LABELS, MODEL_TYPE_FILTER_ORDER, model_type_filter_key
from hakari_bench.viewer.state import FilterState
from hakari_bench.viewer.text_match import active_filter_terms, text_matches_filter_terms


FILTER_NONE_VALUE = "__none_selected__"
DIM_FILTER_RANGE_PREFIX = "lte:"
DIM_FILTER_MIN_RANGE_PREFIX = "gte:"
DIM_FILTER_POINT_VALUES = (32, 64, 128, 256, 384, 512, 768, 1024, 1536, 2048, 2560)
FilterOption = tuple[str, str]


@dataclass(frozen=True)
class FilterContext:
    dim_options: list[FilterOption] = field(default_factory=list)
    quant_options: list[FilterOption] = field(default_factory=list)
    commercial_options: list[FilterOption] = field(default_factory=list)
    dtype_options: list[FilterOption] = field(default_factory=list)
    attn_options: list[FilterOption] = field(default_factory=list)
    prompt_options: list[FilterOption] = field(default_factory=list)
    model_type_options: list[FilterOption] = field(default_factory=list)
    selected_dims: set[str] = field(default_factory=set)
    selected_dim_filters: tuple[str, ...] = ()
    selected_quants: set[str] = field(default_factory=set)
    selected_commercial: set[str] = field(default_factory=set)
    selected_dtypes: set[str] = field(default_factory=set)
    selected_attn: set[str] = field(default_factory=set)
    selected_prompts: set[str] = field(default_factory=set)
    selected_model_types: set[str] = field(default_factory=set)
    model_filter_terms: tuple[str, ...] = ()

    def is_visible(self, row: LeaderboardRow) -> bool:
        return not (
            bool(self.model_filter_terms and not model_name_matches_filter_terms(row.model_name, self.model_filter_terms))
            or not dim_filter_matches(row.embedding_dim, self.selected_dims, self.selected_dim_filters)
            or quant_bucket(row.quantization) not in self.selected_quants
            or commercial_bucket(row.license) not in self.selected_commercial
            or dtype_bucket(row.dtype) not in self.selected_dtypes
            or attn_bucket(row.attn_implementation) not in self.selected_attn
            or prompt_bucket(row.prompt_summary) not in self.selected_prompts
            or model_type_bucket(row.model_name, row.model_type) not in self.selected_model_types
        )

    def ordered_selected_dims(self) -> list[str]:
        if self.selected_dim_filters:
            return list(self.selected_dim_filters)
        return ordered_selected_values(self.dim_options, self.selected_dims)

    def ordered_selected_quants(self) -> list[str]:
        return ordered_selected_values(self.quant_options, self.selected_quants)

    def ordered_selected_commercial(self) -> list[str]:
        return ordered_selected_values(self.commercial_options, self.selected_commercial)

    def ordered_selected_dtypes(self) -> list[str]:
        return ordered_selected_values(self.dtype_options, self.selected_dtypes)

    def ordered_selected_attn(self) -> list[str]:
        return ordered_selected_values(self.attn_options, self.selected_attn)

    def ordered_selected_prompts(self) -> list[str]:
        return ordered_selected_values(self.prompt_options, self.selected_prompts)

    def ordered_selected_model_types(self) -> list[str]:
        return ordered_selected_values(self.model_type_options, self.selected_model_types)


def row_filter_context(rows: list[LeaderboardRow], filter_state: FilterState) -> FilterContext:
    dim_options = dim_filter_options(rows)
    quant_options = quant_filter_options(rows)
    commercial_options = commercial_filter_options(rows)
    dtype_options = dtype_filter_options(rows)
    attn_options = attn_filter_options(rows)
    prompt_options = prompt_filter_options(rows)
    model_type_options = model_type_filter_options(rows)
    return FilterContext(
        dim_options=dim_options,
        quant_options=quant_options,
        commercial_options=commercial_options,
        dtype_options=dtype_options,
        attn_options=attn_options,
        prompt_options=prompt_options,
        model_type_options=model_type_options,
        selected_dims=selected_dim_filter_values(
            options=dim_options,
            selected=filter_state.dim_filters,
            filters_active=filter_state.filters_active,
        ),
        selected_dim_filters=filter_state.dim_filters if filter_state.filters_active else (),
        selected_quants=selected_filter_values(
            options=quant_options,
            selected=filter_state.quant_filters,
            filters_active=filter_state.filters_active,
        ),
        selected_commercial=selected_filter_values(
            options=commercial_options,
            selected=filter_state.commercial_filters,
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
        selected_model_types=selected_filter_values(
            options=model_type_options,
            selected=filter_state.model_type_filters,
            filters_active=filter_state.filters_active,
        ),
        model_filter_terms=active_model_filter_terms(filter_state.model_filter),
    )


def visible_row_count(rows: list[LeaderboardRow], context: FilterContext) -> int:
    return sum(1 for row in rows if context.is_visible(row))


def active_model_filter_terms(model_filter: str) -> tuple[str, ...]:
    return active_filter_terms(model_filter)


def active_task_filter_terms(task_filter: str) -> tuple[str, ...]:
    return active_filter_terms(task_filter, min_length=2)


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


def commercial_filter_options(rows: list[LeaderboardRow]) -> list[FilterOption]:
    buckets = {commercial_bucket(row.license) for row in rows}
    return [
        (bucket, commercial_bucket_label(bucket))
        for bucket in ("commercial", "non_commercial", "not_applicable", "unknown")
        if bucket in buckets
    ]


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


def model_type_filter_options(rows: list[LeaderboardRow]) -> list[FilterOption]:
    buckets = {model_type_bucket(row.model_name, row.model_type) for row in rows}
    return [
        (bucket, MODEL_TYPE_FILTER_LABELS[bucket])
        for bucket in MODEL_TYPE_FILTER_ORDER
        if bucket in buckets
    ]


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


def selected_dim_filter_values(
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
    exact_values = {value for value in selected if value in available}
    range_values = {
        value
        for value in available
        if any(dim_filter_bucket_matches(value, selected_value) for selected_value in selected)
    }
    return exact_values | range_values


def ordered_selected_values(options: list[FilterOption], selected_values: set[str]) -> list[str]:
    return [value for value, _ in options if value in selected_values]


def dim_filter_matches(value: int | None, selected_values: set[str], selected_filters: tuple[str, ...] = ()) -> bool:
    if not selected_values:
        return False
    if selected_filters:
        return _dim_filter_values_match(value=value, selected_filters=selected_filters)
    return dim_bucket(value) in selected_values


def _dim_filter_values_match(*, value: int | None, selected_filters: tuple[str, ...]) -> bool:
    if FILTER_NONE_VALUE in selected_filters:
        return False
    bucket = dim_bucket(value)
    exact_filters = [
        selected
        for selected in selected_filters
        if not selected.startswith(DIM_FILTER_MIN_RANGE_PREFIX) and not selected.startswith(DIM_FILTER_RANGE_PREFIX)
    ]
    if bucket in exact_filters:
        return True
    min_bounds = [
        bound
        for selected in selected_filters
        if selected.startswith(DIM_FILTER_MIN_RANGE_PREFIX)
        for bound in [_dim_filter_bound(selected, prefix=DIM_FILTER_MIN_RANGE_PREFIX)]
        if bound is not None
    ]
    max_bounds = [
        bound
        for selected in selected_filters
        if selected.startswith(DIM_FILTER_RANGE_PREFIX)
        for bound in [_dim_filter_bound(selected, prefix=DIM_FILTER_RANGE_PREFIX)]
        if bound is not None
    ]
    if not min_bounds and not max_bounds:
        return False
    if value is None:
        return False
    if min_bounds and value < max(min_bounds):
        return False
    if max_bounds and value > min(max_bounds):
        return False
    return True


def _dim_filter_value_matches(*, value: int | None, bucket: str, selected_value: str) -> bool:
    if selected_value == bucket:
        return True
    if selected_value.startswith(DIM_FILTER_MIN_RANGE_PREFIX):
        bound = _dim_filter_bound(selected_value, prefix=DIM_FILTER_MIN_RANGE_PREFIX)
        return value is not None and bound is not None and value >= bound
    if not selected_value.startswith(DIM_FILTER_RANGE_PREFIX):
        return False
    bound = _dim_filter_bound(selected_value, prefix=DIM_FILTER_RANGE_PREFIX)
    return value is not None and bound is not None and value <= bound


def dim_filter_bucket_matches(bucket: str, selected_value: str) -> bool:
    if selected_value == bucket:
        return True
    if selected_value.startswith(DIM_FILTER_MIN_RANGE_PREFIX):
        bound = _dim_filter_bound(selected_value, prefix=DIM_FILTER_MIN_RANGE_PREFIX)
        if bound is None:
            return False
        if bucket == "__unknown__":
            return False
        if bucket == "1025+":
            return True
        return int(bucket) >= bound
    if not selected_value.startswith(DIM_FILTER_RANGE_PREFIX):
        return False
    bound = _dim_filter_bound(selected_value, prefix=DIM_FILTER_RANGE_PREFIX)
    if bound is None:
        return False
    if bucket == "__unknown__":
        return False
    if bucket == "1025+":
        return bound >= 1025
    return int(bucket) <= bound


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


def _dim_filter_bound(value: str, *, prefix: str) -> int | None:
    raw_bound = value.removeprefix(prefix)
    try:
        return int(raw_bound)
    except ValueError:
        return None


def quant_bucket(value: str | None) -> str:
    return value or "__none__"


def quant_bucket_label(bucket: str) -> str:
    return "Original" if bucket == "__none__" else bucket


def quant_bucket_sort_key(bucket: str) -> tuple[int, str]:
    return (0, "") if bucket == "__none__" else (1, bucket)


def commercial_bucket(license_metadata: dict[str, object] | None) -> str:
    commercial_use = ""
    if isinstance(license_metadata, dict):
        commercial_use = str(license_metadata.get("commercial_use") or "")
    if commercial_use in {"allowed", "permitted_with_terms"}:
        return "commercial"
    if commercial_use == "not_allowed":
        return "non_commercial"
    if commercial_use == "not_applicable":
        return "not_applicable"
    return "unknown"


def commercial_bucket_label(bucket: str) -> str:
    labels = {
        "commercial": "Commercial",
        "non_commercial": "Non-commercial",
        "not_applicable": "N/A",
        "unknown": "Unknown",
    }
    return labels.get(bucket, bucket)


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


def model_type_bucket(model_name: str, model_type: str | None) -> str:
    return model_type_filter_key(model_name=model_name, model_type=model_type)


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
