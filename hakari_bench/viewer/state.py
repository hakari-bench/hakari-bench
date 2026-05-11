from __future__ import annotations

from dataclasses import dataclass

from hakari_bench.viewer.config import ViewerConfig
from hakari_bench.viewer.leaderboard import LeaderboardResult, SORT_COLUMNS
from hakari_bench.viewer.variant_display import variant_display_flags_from_values


QueryValue = str | list[str]
QueryState = dict[str, QueryValue]


@dataclass(frozen=True)
class FilterState:
    model_filter: str = ""
    task_filter: str = ""
    language_filters: tuple[str, ...] = ()
    filters_active: bool = False
    dim_filters: tuple[str, ...] = ()
    quant_filters: tuple[str, ...] = ()
    dtype_filters: tuple[str, ...] = ()
    attn_filters: tuple[str, ...] = ()
    prompt_filters: tuple[str, ...] = ()


def normalize_query_state(
    *,
    viewer_config: ViewerConfig,
    view: str,
    sort: str,
    direction: str,
    target: str = "all",
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
    lang_filter: list[str] | None = None,
    model_filter: str,
    task_scores: bool = False,
    task_filter: str = "",
) -> QueryState:
    if view not in viewer_config.view_names:
        view = viewer_config.overall.name
    if sort not in SORT_COLUMNS and not sort.startswith("metric:"):
        sort = "borda_rank"
    if direction not in {"asc", "desc"}:
        direction = "asc"
    if target not in {"all", "reranking"}:
        target = "all"
    display_flags = variant_display_flags_from_values(
        variants=variants,
        quantization=quantization,
        truncate=truncate,
        rescore=rescore,
        other=other_variant,
    )
    task_filter = task_filter.strip()
    query: QueryState = {"view": view, "sort": sort, "direction": direction}
    if target != "all":
        query["target"] = target
    if group:
        query["group"] = group
    if task_scores or task_filter:
        query["task_scores"] = "1"
    if display_flags.quantization:
        query["quantization"] = "1"
    if display_flags.truncate:
        query["truncate"] = "1"
    if display_flags.rescore:
        query["rescore"] = "1"
    if display_flags.other:
        query["other_variant"] = "1"
    language_filters = _normalized_query_values(lang_filter)
    if language_filters:
        query["lang_filter"] = language_filters
    if filters:
        query["filters"] = "1"
        query["dim_filter"] = _normalized_query_values(dim_filter)
        query["quant_filter"] = _normalized_query_values(quant_filter)
        query["dtype_filter"] = _normalized_query_values(dtype_filter)
        query["attn_filter"] = _normalized_query_values(attn_filter)
        query["prompt_filter"] = _normalized_query_values(prompt_filter)
    model_filter = model_filter.strip()
    if model_filter:
        query["model_filter"] = model_filter
    if task_filter:
        query["task_filter"] = task_filter
    return query


def filter_state_from_query(query: QueryState) -> FilterState:
    return FilterState(
        model_filter=str(query.get("model_filter", "")),
        task_filter=str(query.get("task_filter", "")),
        language_filters=tuple(query_values(query.get("lang_filter"))),
        filters_active=query.get("filters") == "1",
        dim_filters=tuple(query_values(query.get("dim_filter"))),
        quant_filters=tuple(query_values(query.get("quant_filter"))),
        dtype_filters=tuple(query_values(query.get("dtype_filter"))),
        attn_filters=tuple(query_values(query.get("attn_filter"))),
        prompt_filters=tuple(query_values(query.get("prompt_filter"))),
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
    if result.selected_score_group is not None:
        query_payload["group"] = result.selected_score_group.name
    if result.show_task_scores:
        query_payload["task_scores"] = "1"
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
    if filter_state.language_filters:
        query_payload["lang_filter"] = list(filter_state.language_filters)
    if filter_state.filters_active:
        query_payload["filters"] = "1"
        query_payload["dim_filter"] = list(filter_state.dim_filters)
        query_payload["quant_filter"] = list(filter_state.quant_filters)
        query_payload["dtype_filter"] = list(filter_state.dtype_filters)
        query_payload["attn_filter"] = list(filter_state.attn_filters)
        query_payload["prompt_filter"] = list(filter_state.prompt_filters)
    return query_payload


def active_filter_hidden_fields(filter_state: FilterState) -> list[tuple[str, str]]:
    if not filter_state.filters_active:
        return [("lang_filter", value) for value in filter_state.language_filters]
    fields = [("lang_filter", value) for value in filter_state.language_filters]
    fields.append(("filters", "1"))
    fields.extend(("dim_filter", value) for value in filter_state.dim_filters)
    fields.extend(("quant_filter", value) for value in filter_state.quant_filters)
    fields.extend(("dtype_filter", value) for value in filter_state.dtype_filters)
    fields.extend(("attn_filter", value) for value in filter_state.attn_filters)
    fields.extend(("prompt_filter", value) for value in filter_state.prompt_filters)
    return fields


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
