"""Shared leaderboard-result construction from normalized query state.

Both the legacy htmx HTML routes and the JSON API build a ``LeaderboardResult``
from the same normalized query state. Keep that mapping in one place so the two
surfaces never drift.
"""

from __future__ import annotations

from typing import cast

from hakari_bench.viewer.config import ViewerConfig
from hakari_bench.viewer.leaderboard import (
    LeaderboardResult,
    LeaderboardService,
    ScoreTarget,
    SortDirection,
)
from hakari_bench.viewer.state import (
    FilterState,
    QueryState,
    filter_state_from_query,
    optional_query_string,
    parameter_bounds,
    query_string,
    query_values,
    task_length_bounds,
)
from hakari_bench.viewer.config import ScoreAggregation
from hakari_bench.viewer.variant_display import variant_display_flags_from_query


def build_leaderboard_result(
    *,
    duckdb_path,
    viewer_config: ViewerConfig,
    state_query: QueryState,
) -> tuple[LeaderboardResult, str, str, FilterState]:
    """Resolve a normalized query state into a leaderboard result.

    Returns the result alongside the effective sort, direction, and filter state
    so callers can reflect those back in URLs and UI controls.
    """

    view = query_string(state_query["view"])
    sort = query_string(state_query["sort"])
    direction = query_string(state_query["direction"])
    target = query_string(state_query.get("target", "all"))
    score = query_string(state_query.get("score", "micro"))
    score_metric = query_string(state_query.get("metric", "ndcg@10"))
    group = optional_query_string(state_query.get("group"))
    selected_benchmarks = tuple(query_values(state_query.get("bench")))
    display_flags = variant_display_flags_from_query(state_query)
    filter_state = filter_state_from_query(state_query)
    params_bounds = parameter_bounds(filter_state)
    length_bounds = task_length_bounds(filter_state)
    service = LeaderboardService(duckdb_path=duckdb_path, config=viewer_config)
    result = service.get_leaderboard(
        view,
        sort=sort,
        direction=cast(SortDirection, direction),
        score_target=cast(ScoreTarget, target),
        score_aggregation=cast(ScoreAggregation, score),
        score_metric=score_metric,
        score_group_name=group,
        include_quantization_variants=display_flags.quantization,
        include_truncate_variants=display_flags.truncate,
        include_rescore_variants=display_flags.rescore,
        include_other_variants=display_flags.other,
        language_filters=filter_state.language_filters,
        show_task_scores=state_query.get("task_scores") == "1",
        show_task_z_scores=state_query.get("task_z_scores") == "1",
        show_task_ranks=state_query.get("task_ranks") == "1",
        show_other_columns=state_query.get("other_columns") == "1",
        rank_filtered=filter_state.rank_filtered,
        model_filter=filter_state.model_filter,
        task_filter=filter_state.task_filter,
        dim_filters=filter_state.dim_filters if filter_state.filters_active else (),
        quant_filters=filter_state.quant_filters if filter_state.filters_active else (),
        commercial_filters=filter_state.commercial_filters if filter_state.filters_active else (),
        model_type_filters=filter_state.model_type_filters if filter_state.filters_active else (),
        dtype_filters=filter_state.dtype_filters if filter_state.filters_active else (),
        attn_filters=filter_state.attn_filters if filter_state.filters_active else (),
        prompt_filters=filter_state.prompt_filters if filter_state.filters_active else (),
        active_params_min_millions=params_bounds["active_min_millions"],
        active_params_max_millions=params_bounds["active_max_millions"],
        total_params_min_millions=params_bounds["total_min_millions"],
        total_params_max_millions=params_bounds["total_max_millions"],
        query_min_chars=length_bounds["query_min_chars"],
        query_max_chars=length_bounds["query_max_chars"],
        document_min_chars=length_bounds["document_min_chars"],
        document_max_chars=length_bounds["document_max_chars"],
        selected_benchmarks=selected_benchmarks,
    )
    return result, sort, direction, filter_state
