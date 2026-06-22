from __future__ import annotations

from dataclasses import dataclass
import math

from hakari_bench.viewer.config import (
    CLEAR_SCOPE_NAME,
    CUSTOM_SCOPE_NAME,
    ScoreAggregation,
    ViewerConfig,
    normalize_benchmark_selection_values,
)
from hakari_bench.viewer.leaderboard import LeaderboardResult, SORT_COLUMNS
from hakari_bench.viewer.variant_display import variant_display_flags_from_values


QueryValue = str | list[str]
QueryState = dict[str, QueryValue]

RESULT_VIEW_VALUES = {"table", "chart"}
PLOT_SCORE_FIELDS = {"borda_score", "macro_mean", "micro_mean"}
PLOT_NONE_FIELD = "none"
PLOT_AXIS_FIELDS = {
    "active_parameters",
    "active_parameters_linear",
    "total_parameters",
    "total_parameters_linear",
    "max_seq_length",
    "embedding_dim",
    "quantization",
    "sparse_query_dims",
    "sparse_document_dims",
}
PLOT_ENCODING_FIELDS = {*PLOT_AXIS_FIELDS, PLOT_NONE_FIELD}


@dataclass(frozen=True)
class FilterState:
    model_filter: str = ""
    task_filter: str = ""
    rank_filtered: bool = False
    language_filters: tuple[str, ...] = ()
    filters_active: bool = False
    dim_filters: tuple[str, ...] = ()
    quant_filters: tuple[str, ...] = ()
    model_type_filters: tuple[str, ...] = ()
    dtype_filters: tuple[str, ...] = ()
    attn_filters: tuple[str, ...] = ()
    prompt_filters: tuple[str, ...] = ()
    active_params_min: str = ""
    active_params_max: str = ""
    total_params_min: str = ""
    total_params_max: str = ""
    query_len_min: str = ""
    query_len_max: str = ""
    doc_len_min: str = ""
    doc_len_max: str = ""

    @property
    def has_parameter_filters(self) -> bool:
        return bool(
            self.active_params_min
            or self.active_params_max
            or self.total_params_min
            or self.total_params_max
        )

    @property
    def has_task_length_filters(self) -> bool:
        return bool(self.query_len_min or self.query_len_max or self.doc_len_min or self.doc_len_max)


def normalize_query_state(
    *,
    viewer_config: ViewerConfig,
    view: str,
    sort: str,
    direction: str,
    target: str = "all",
    score: str = "micro",
    group: str | None,
    variants: bool,
    quantization: bool,
    truncate: bool,
    rescore: bool,
    other_variant: bool,
    filters: bool,
    dim_filter: list[str] | None,
    quant_filter: list[str] | None,
    dtype_filter: list[str] | None,
    attn_filter: list[str] | None,
    prompt_filter: list[str] | None,
    model_type_filter: list[str] | None = None,
    lang_filter: list[str] | None = None,
    bench: list[str] | None = None,
    model_filter: str,
    rank_filtered: bool = False,
    task_scores: bool = False,
    task_z_scores: bool = False,
    task_ranks: bool = False,
    task_filter: str = "",
    active_params_min: str = "",
    active_params_max: str = "",
    total_params_min: str = "",
    total_params_max: str = "",
    query_len_min: str = "",
    query_len_max: str = "",
    doc_len_min: str = "",
    doc_len_max: str = "",
    metric: str = "ndcg@10",
    result_view: str = "table",
    chart_y: str = "borda_score",
    chart_x: str = "active_parameters",
    chart_color: str = "embedding_dim",
) -> QueryState:
    view = _normalized_view_name(view)
    selected_benchmarks = _normalized_benchmark_values(bench, viewer_config)
    if view == CLEAR_SCOPE_NAME:
        view = CUSTOM_SCOPE_NAME
    if selected_benchmarks:
        view = CUSTOM_SCOPE_NAME
    if view not in [*viewer_config.view_names, CUSTOM_SCOPE_NAME, CLEAR_SCOPE_NAME]:
        view = viewer_config.overall.name
    if sort not in SORT_COLUMNS and not sort.startswith("metric:"):
        sort = "borda_rank"
    if direction not in {"asc", "desc"}:
        direction = "asc"
    if target not in {"all", "reranking", "reranking_without_safeguard"}:
        target = "all"
    result_view = result_view if result_view in RESULT_VIEW_VALUES else "table"
    chart_y = chart_y if chart_y in PLOT_SCORE_FIELDS else "borda_score"
    chart_x = chart_x if chart_x in PLOT_AXIS_FIELDS else "active_parameters"
    chart_color = chart_color if chart_color in PLOT_ENCODING_FIELDS else "embedding_dim"
    if "quantization" in {chart_x, chart_color}:
        quantization = True
    score_aggregation: ScoreAggregation = "macro" if score == "macro" else "micro"
    display_flags = variant_display_flags_from_values(
        variants=variants,
        quantization=quantization,
        truncate=truncate,
        rescore=rescore,
        other=other_variant,
    )
    task_filter = task_filter.strip()
    query: QueryState = {"view": view, "sort": sort, "direction": direction}
    if result_view != "table":
        query["result_view"] = result_view
    if chart_y != "borda_score":
        query["chart_y"] = chart_y
    if chart_x != "active_parameters":
        query["chart_x"] = chart_x
    if chart_color != "embedding_dim":
        query["chart_color"] = chart_color
    empty_custom_scope = view == CUSTOM_SCOPE_NAME and not selected_benchmarks
    if view == CUSTOM_SCOPE_NAME and selected_benchmarks:
        query["bench"] = selected_benchmarks
    if target != "all":
        query["target"] = target
    if score_aggregation != "micro":
        query["score"] = score_aggregation
    if metric and metric != "ndcg@10":
        query["metric"] = metric.strip().casefold()
    if group:
        query["group"] = group
    if task_scores or task_filter or task_ranks:
        query["task_scores"] = "1"
    if task_z_scores:
        query["task_z_scores"] = "1"
    if task_ranks:
        query["task_ranks"] = "1"
    if display_flags.quantization:
        query["quantization"] = "1"
    if display_flags.truncate:
        query["truncate"] = "1"
    if display_flags.rescore:
        query["rescore"] = "1"
    if display_flags.other:
        query["other_variant"] = "1"
    language_filters = _normalized_query_values(lang_filter)
    if view == "Overall (EN)":
        language_filters = ["en"]
    active_params_min = _normalized_numeric_bound(active_params_min)
    active_params_max = _normalized_numeric_bound(active_params_max)
    total_params_min = _normalized_numeric_bound(total_params_min)
    total_params_max = _normalized_numeric_bound(total_params_max)
    query_len_min = _normalized_numeric_bound(query_len_min)
    query_len_max = _normalized_numeric_bound(query_len_max)
    doc_len_min = _normalized_numeric_bound(doc_len_min)
    doc_len_max = _normalized_numeric_bound(doc_len_max)
    has_parameter_filters = bool(active_params_min or active_params_max or total_params_min or total_params_max)
    has_task_length_filters = bool(query_len_min or query_len_max or doc_len_min or doc_len_max)
    if language_filters:
        query["lang_filter"] = language_filters
    if empty_custom_scope:
        query.pop("lang_filter", None)
    if filters or has_parameter_filters or has_task_length_filters:
        query["filters"] = "1"
        query["dim_filter"] = _normalized_query_values(dim_filter)
        query["quant_filter"] = _normalized_query_values(quant_filter)
        query["model_type_filter"] = _normalized_model_type_filter_values(model_type_filter)
        query["dtype_filter"] = _normalized_query_values(dtype_filter)
        query["attn_filter"] = _normalized_query_values(attn_filter)
        query["prompt_filter"] = _normalized_query_values(prompt_filter)
        if active_params_min:
            query["active_params_min"] = active_params_min
        if active_params_max:
            query["active_params_max"] = active_params_max
        if total_params_min:
            query["total_params_min"] = total_params_min
        if total_params_max:
            query["total_params_max"] = total_params_max
        if query_len_min:
            query["query_len_min"] = query_len_min
        if query_len_max:
            query["query_len_max"] = query_len_max
        if doc_len_min:
            query["doc_len_min"] = doc_len_min
        if doc_len_max:
            query["doc_len_max"] = doc_len_max
    model_filter = model_filter.strip()
    if model_filter:
        query["model_filter"] = model_filter
    if task_filter:
        query["task_filter"] = task_filter
    if rank_filtered:
        query["rank_filtered"] = "1"
    return query


def _normalized_view_name(view: str) -> str:
    aliases = {
        "All": "Overall",
        "Group": "Overall",
    }
    return aliases.get(view, view)


def filter_state_from_query(query: QueryState) -> FilterState:
    return FilterState(
        model_filter=str(query.get("model_filter", "")),
        task_filter=str(query.get("task_filter", "")),
        rank_filtered=query.get("rank_filtered") == "1",
        language_filters=tuple(query_values(query.get("lang_filter"))),
        filters_active=query.get("filters") == "1",
        dim_filters=tuple(query_values(query.get("dim_filter"))),
        quant_filters=tuple(query_values(query.get("quant_filter"))),
        model_type_filters=tuple(query_values(query.get("model_type_filter"))),
        dtype_filters=tuple(query_values(query.get("dtype_filter"))),
        attn_filters=tuple(query_values(query.get("attn_filter"))),
        prompt_filters=tuple(query_values(query.get("prompt_filter"))),
        active_params_min=str(query.get("active_params_min", "")),
        active_params_max=str(query.get("active_params_max", "")),
        total_params_min=str(query.get("total_params_min", "")),
        total_params_max=str(query.get("total_params_max", "")),
        query_len_min=str(query.get("query_len_min", "")),
        query_len_max=str(query.get("query_len_max", "")),
        doc_len_min=str(query.get("doc_len_min", "")),
        doc_len_max=str(query.get("doc_len_max", "")),
    )


def state_payload(
    *,
    result: LeaderboardResult,
    sort: str,
    direction: str,
    filter_state: FilterState | None = None,
) -> QueryState:
    filter_state = filter_state or FilterState()
    query_payload: QueryState = {"view": result.view_name, "sort": sort, "direction": direction}
    if result.score_target != "all":
        query_payload["target"] = result.score_target
    if result.score_aggregation != "micro":
        query_payload["score"] = result.score_aggregation
    if result.selected_score_metric != "ndcg@10":
        query_payload["metric"] = result.selected_score_metric
    if result.selected_score_group is not None:
        query_payload["group"] = result.selected_score_group.name
    selected_benchmarks = getattr(result, "selected_benchmarks", ())
    if result.view_name == CUSTOM_SCOPE_NAME and selected_benchmarks:
        query_payload["bench"] = list(selected_benchmarks)
    if result.show_task_scores:
        query_payload["task_scores"] = "1"
    if result.show_task_z_scores:
        query_payload["task_z_scores"] = "1"
    else:
        query_payload["task_z_scores"] = "0"
    if result.show_task_ranks:
        query_payload["task_ranks"] = "1"
    if result.include_quantization_variants:
        query_payload["quantization"] = "1"
    if result.include_truncate_variants:
        query_payload["truncate"] = "1"
    if result.include_rescore_variants:
        query_payload["rescore"] = "1"
    if result.include_other_variants:
        query_payload["other_variant"] = "1"
    if filter_state.model_filter:
        query_payload["model_filter"] = filter_state.model_filter
    if filter_state.task_filter:
        query_payload["task_filter"] = filter_state.task_filter
    if filter_state.rank_filtered:
        query_payload["rank_filtered"] = "1"
    if filter_state.language_filters:
        query_payload["lang_filter"] = list(filter_state.language_filters)
    if filter_state.filters_active or filter_state.has_parameter_filters or filter_state.has_task_length_filters:
        query_payload["filters"] = "1"
        query_payload["dim_filter"] = list(filter_state.dim_filters)
        query_payload["quant_filter"] = list(filter_state.quant_filters)
        query_payload["model_type_filter"] = list(filter_state.model_type_filters)
        query_payload["dtype_filter"] = list(filter_state.dtype_filters)
        query_payload["attn_filter"] = list(filter_state.attn_filters)
        query_payload["prompt_filter"] = list(filter_state.prompt_filters)
        if filter_state.active_params_min:
            query_payload["active_params_min"] = filter_state.active_params_min
        if filter_state.active_params_max:
            query_payload["active_params_max"] = filter_state.active_params_max
        if filter_state.total_params_min:
            query_payload["total_params_min"] = filter_state.total_params_min
        if filter_state.total_params_max:
            query_payload["total_params_max"] = filter_state.total_params_max
        if filter_state.query_len_min:
            query_payload["query_len_min"] = filter_state.query_len_min
        if filter_state.query_len_max:
            query_payload["query_len_max"] = filter_state.query_len_max
        if filter_state.doc_len_min:
            query_payload["doc_len_min"] = filter_state.doc_len_min
        if filter_state.doc_len_max:
            query_payload["doc_len_max"] = filter_state.doc_len_max
    return query_payload


def active_filter_hidden_fields(filter_state: FilterState) -> list[tuple[str, str]]:
    if (
        not filter_state.filters_active
        and not filter_state.has_parameter_filters
        and not filter_state.has_task_length_filters
    ):
        return [("lang_filter", value) for value in filter_state.language_filters]
    fields = [("lang_filter", value) for value in filter_state.language_filters]
    fields.append(("filters", "1"))
    fields.extend(("dim_filter", value) for value in filter_state.dim_filters)
    fields.extend(("quant_filter", value) for value in filter_state.quant_filters)
    fields.extend(("model_type_filter", value) for value in filter_state.model_type_filters)
    fields.extend(("dtype_filter", value) for value in filter_state.dtype_filters)
    fields.extend(("attn_filter", value) for value in filter_state.attn_filters)
    fields.extend(("prompt_filter", value) for value in filter_state.prompt_filters)
    fields.extend(_parameter_hidden_fields(filter_state))
    fields.extend(_task_length_hidden_fields(filter_state))
    return fields


def parameter_bounds(filter_state: FilterState) -> dict[str, float | None]:
    return {
        "active_min_millions": numeric_filter_bound(filter_state.active_params_min),
        "active_max_millions": numeric_filter_bound(filter_state.active_params_max),
        "total_min_millions": numeric_filter_bound(filter_state.total_params_min),
        "total_max_millions": numeric_filter_bound(filter_state.total_params_max),
    }


def task_length_bounds(filter_state: FilterState) -> dict[str, float | None]:
    return {
        "query_min_chars": numeric_filter_bound(filter_state.query_len_min),
        "query_max_chars": numeric_filter_bound(filter_state.query_len_max),
        "document_min_chars": numeric_filter_bound(filter_state.doc_len_min),
        "document_max_chars": numeric_filter_bound(filter_state.doc_len_max),
    }


def query_values(value: QueryValue | None) -> list[str]:
    if value is None:
        return []
    if isinstance(value, list):
        return value
    return [value]


def query_string(value: QueryValue) -> str:
    return value[0] if isinstance(value, list) and value else str(value)


def optional_query_string(value: QueryValue | None) -> str | None:
    if value is None:
        return None
    return query_string(value)


def _normalized_query_values(values: list[str] | None) -> list[str]:
    if values is None:
        return []
    return [value for value in values if value]


def _normalized_benchmark_values(values: list[str] | None, viewer_config: ViewerConfig) -> list[str]:
    return normalize_benchmark_selection_values(_normalized_query_values(values), viewer_config)


def _normalized_model_type_filter_values(values: list[str] | None) -> list[str]:
    allowed = {"dense", "bm25", "sparse", "late-interaction", "reranker"}
    return [value for value in _normalized_query_values(values) if value in allowed]


def numeric_filter_bound(value: str) -> float | None:
    normalized = _normalized_numeric_bound(value)
    return float(normalized) if normalized else None


def _normalized_numeric_bound(value: str) -> str:
    value = value.strip()
    if not value:
        return ""
    try:
        number = float(value)
    except ValueError:
        return ""
    if not math.isfinite(number) or number < 0:
        return ""
    if number.is_integer():
        return str(int(number))
    return value


def _parameter_hidden_fields(filter_state: FilterState) -> list[tuple[str, str]]:
    fields = []
    if filter_state.active_params_min:
        fields.append(("active_params_min", filter_state.active_params_min))
    if filter_state.active_params_max:
        fields.append(("active_params_max", filter_state.active_params_max))
    if filter_state.total_params_min:
        fields.append(("total_params_min", filter_state.total_params_min))
    if filter_state.total_params_max:
        fields.append(("total_params_max", filter_state.total_params_max))
    return fields


def _task_length_hidden_fields(filter_state: FilterState) -> list[tuple[str, str]]:
    fields = []
    if filter_state.query_len_min:
        fields.append(("query_len_min", filter_state.query_len_min))
    if filter_state.query_len_max:
        fields.append(("query_len_max", filter_state.query_len_max))
    if filter_state.doc_len_min:
        fields.append(("doc_len_min", filter_state.doc_len_min))
    if filter_state.doc_len_max:
        fields.append(("doc_len_max", filter_state.doc_len_max))
    return fields
