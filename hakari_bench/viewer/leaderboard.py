from __future__ import annotations

from collections import defaultdict
from dataclasses import dataclass, replace
from functools import lru_cache
import math
from pathlib import Path
import re
from typing import Any, Iterable, Literal

import duckdb
from pydantic import BaseModel, ConfigDict, Field
import yaml

from hakari_bench.viewer.config import (
    CLEAR_SCOPE_NAME,
    CUSTOM_SCOPE_NAME,
    LanguageFilterMode,
    OverallConfig,
    ScoreAggregation,
    ScoreGroupConfig,
    ViewerConfig,
    normalize_benchmark_selection_values,
)
from hakari_bench.viewer.data import TaskResultRow, TaskResultsRepository, _table_exists
from hakari_bench.viewer.model_types import (
    is_bm25_model,
    is_reranker_model,
    model_type_filter_key,
)
from hakari_bench.viewer.observability import log_event, timed_operation
from hakari_bench.viewer.text_match import (
    active_filter_terms,
    text_matches_filter_terms,
)
from hakari_bench.viewer.variant_display import VariantDisplayFlags, include_variant_row

SortDirection = Literal["asc", "desc"]
ScoreTarget = Literal["all", "reranking", "reranking_without_safeguard"]
DEFAULT_MODEL_CARDS_PATH = Path("config/model_cards")


@dataclass(frozen=True)
class ModelCardParameters:
    active_parameters: int | None = None
    total_parameters: int | None = None
    max_seq_length: int | None = None
    late_interaction_query_length: int | None = None
    late_interaction_document_length: int | None = None
    late_interaction_query_prefix: str | None = None
    late_interaction_document_prefix: str | None = None
    late_interaction_query_expansion: bool | None = None
    late_interaction_attend_to_expansion_tokens: bool | None = None
    language_support_category: str | None = None
    language_support_languages: tuple[str, ...] = ()
    language_support_marker: str | None = None
    links: dict[str, Any] | None = None
    license: dict[str, Any] | None = None


@dataclass(frozen=True)
class LanguageFilterPolicy:
    default_mode: LanguageFilterMode = "languages"
    default_allowed_languages: tuple[str, ...] = ()
    modes_by_benchmark: dict[str, LanguageFilterMode] | None = None
    allowed_languages_by_benchmark: dict[str, tuple[str, ...]] | None = None


@dataclass(frozen=True)
class TaskScore:
    model_name: str
    benchmark: str
    dataset_id: str
    dataset_name: str
    split_name: str
    task_name: str
    task_key: str
    score: float
    active_parameters: int | None
    total_parameters: int | None
    max_seq_length: int | None
    model_type: str | None = None
    language: str | None = None
    languages: tuple[str, ...] = ()
    primary_languages: tuple[str, ...] = ()
    dtype: str | None = None
    attn_implementation: str | None = None
    prompt_summary: str | None = None
    trust_remote_code: bool | None = None
    embedding_variant_name: str | None = None
    embedding_dim: int | None = None
    quantization: str | None = None
    source_model_name: str | None = None
    query_mean_chars: float | None = None
    document_mean_chars: float | None = None
    late_interaction_query_length: int | None = None
    late_interaction_document_length: int | None = None
    late_interaction_query_prefix: str | None = None
    late_interaction_document_prefix: str | None = None
    late_interaction_query_expansion: bool | None = None
    late_interaction_attend_to_expansion_tokens: bool | None = None


class LeaderboardRow(BaseModel):
    model_config = ConfigDict(frozen=True)

    borda_rank: float
    mean_rank: float
    model_name: str
    model_type: str | None = None
    borda_score: float
    borda_score_z: float | None = None
    mean_score: float
    mean_score_z: float | None = None
    macro_mean: float | None = None
    macro_mean_z: float | None = None
    micro_mean: float | None = None
    micro_mean_z: float | None = None
    task_count: int
    active_parameters: int | None = None
    total_parameters: int | None = None
    max_seq_length: int | None = None
    dtype: str | None = None
    attn_implementation: str | None = None
    prompt_summary: str | None = None
    trust_remote_code: bool | None = None
    embedding_variant_name: str | None = None
    embedding_dim: int | None = None
    quantization: str | None = None
    source_model_name: str | None = None
    base_score_delta_percent: float | None = None
    late_interaction_query_length: int | None = None
    late_interaction_document_length: int | None = None
    late_interaction_query_prefix: str | None = None
    late_interaction_document_prefix: str | None = None
    late_interaction_query_expansion: bool | None = None
    late_interaction_attend_to_expansion_tokens: bool | None = None
    language_support_category: str | None = None
    language_support_languages: tuple[str, ...] = ()
    language_support_marker: str | None = None
    links: dict[str, Any] | None = None
    license: dict[str, Any] | None = None
    metric_values: dict[str, float] = Field(default_factory=dict)
    metric_z_values: dict[str, float] = Field(default_factory=dict)
    metric_rank_values: dict[str, float] = Field(default_factory=dict)
    metric_sort_values: dict[str, float] = Field(default_factory=dict)


class ScoreGroup(BaseModel):
    model_config = ConfigDict(frozen=True)

    name: str
    label: str


class LanguageOption(BaseModel):
    model_config = ConfigDict(frozen=True)

    code: str
    label: str
    task_count: int


class LeaderboardResult(BaseModel):
    model_config = ConfigDict(frozen=True)

    view_name: str
    view_label: str
    is_overall: bool
    score_target: ScoreTarget = "all"
    score_aggregation: ScoreAggregation = "micro"
    selected_score_metric: str = "ndcg@10"
    available_score_metrics: list[str] = Field(default_factory=lambda: ["ndcg@10"])
    expected_tasks: int
    rows: list[LeaderboardRow]
    available_views: list[str]
    available_view_labels: dict[str, str]
    include_quantization_variants: bool = False
    include_truncate_variants: bool = False
    include_rescore_variants: bool = False
    include_other_variants: bool = False
    show_task_scores: bool = False
    show_task_z_scores: bool = False
    show_task_ranks: bool = False
    rank_filtered: bool = False
    task_filter: str = ""
    score_groups: list[ScoreGroup]
    selected_score_group: ScoreGroup | None = None
    metric_columns: list[str]
    metric_column_labels: dict[str, str] = Field(default_factory=dict)
    metric_column_doc_keys: dict[str, str] = Field(default_factory=dict)
    available_languages: list[LanguageOption] = Field(default_factory=list)
    selected_languages: tuple[str, ...] = ()
    selected_benchmarks: tuple[str, ...] = ()


SORT_COLUMNS = {
    "borda_rank",
    "mean_rank",
    "model_name",
    "borda_score",
    "mean_score",
    "macro_mean",
    "micro_mean",
    "task_count",
    "active_parameters",
    "total_parameters",
    "max_seq_length",
    "embedding_dim",
    "quantization",
    "base_score_delta_percent",
}


class LeaderboardService:
    def __init__(
        self,
        *,
        duckdb_path: Path,
        config: ViewerConfig,
        use_precomputed: bool = True,
        model_cards_path: Path | None = DEFAULT_MODEL_CARDS_PATH,
    ) -> None:
        self.config = config
        self.duckdb_path = duckdb_path
        self.use_precomputed = use_precomputed
        self.task_results_repository = TaskResultsRepository(duckdb_path)
        self.model_card_parameters = _load_model_card_parameters(model_cards_path)

    def get_leaderboard(
        self,
        view_name: str,
        *,
        sort: str = "borda_rank",
        direction: SortDirection = "asc",
        score_target: ScoreTarget = "all",
        score_aggregation: ScoreAggregation = "micro",
        score_metric: str = "ndcg@10",
        score_group_name: str | None = None,
        include_quantization_variants: bool = False,
        include_truncate_variants: bool = False,
        include_rescore_variants: bool = False,
        include_other_variants: bool = False,
        language_filters: tuple[str, ...] = (),
        show_task_scores: bool = False,
        show_task_z_scores: bool = False,
        show_task_ranks: bool = False,
        rank_filtered: bool = False,
        model_filter: str = "",
        task_filter: str = "",
        dim_filters: tuple[str, ...] = (),
        quant_filters: tuple[str, ...] = (),
        model_type_filters: tuple[str, ...] = (),
        dtype_filters: tuple[str, ...] = (),
        attn_filters: tuple[str, ...] = (),
        prompt_filters: tuple[str, ...] = (),
        active_params_min_millions: float | None = None,
        active_params_max_millions: float | None = None,
        total_params_min_millions: float | None = None,
        total_params_max_millions: float | None = None,
        query_min_chars: float | None = None,
        query_max_chars: float | None = None,
        document_min_chars: float | None = None,
        document_max_chars: float | None = None,
        selected_benchmarks: tuple[str, ...] = (),
    ) -> LeaderboardResult:
        with timed_operation(
            "viewer.leaderboard.request",
            view=view_name,
            sort=sort,
            direction=direction,
            score_target=score_target,
            show_task_scores=show_task_scores,
        ) as request_timing:
            model_filter_terms = active_filter_terms(model_filter)
            task_filter_terms = active_filter_terms(task_filter, min_length=2)
            ranking_model_filter_terms = model_filter_terms if rank_filtered else ()
            ranking_task_filter_terms = task_filter_terms if rank_filtered else ()
            ranking_dim_filters = dim_filters if rank_filtered else ()
            ranking_quant_filters = quant_filters if rank_filtered else ()
            ranking_model_type_filters = model_type_filters if rank_filtered else ()
            ranking_dtype_filters = dtype_filters if rank_filtered else ()
            ranking_attn_filters = attn_filters if rank_filtered else ()
            ranking_prompt_filters = prompt_filters if rank_filtered else ()
            has_rank_facet_filters = _has_facet_filters(
                dim_filters=ranking_dim_filters,
                quant_filters=ranking_quant_filters,
                model_type_filters=ranking_model_type_filters,
                dtype_filters=ranking_dtype_filters,
                attn_filters=ranking_attn_filters,
                prompt_filters=ranking_prompt_filters,
            )
            view_name, overall, benchmarks = self._resolve_scope(
                view_name, selected_benchmarks=selected_benchmarks
            )
            available_score_metrics = (
                self.task_results_repository.fetch_score_metric_options()
            )
            selected_score_metric = _normalize_score_metric(
                score_metric, available_score_metrics
            )
            is_overall = overall is not None
            selected_benchmark_names = (
                tuple(self.config.selection_keys_for_overall(overall))
                if overall is not None
                else tuple(benchmarks)
            )
            request_timing["benchmark_count"] = len(benchmarks)
            request_timing["score_aggregation"] = score_aggregation
            score_groups = (
                [] if is_overall else _score_groups_for_view(self.config, view_name)
            )
            selected_score_group = _select_score_group(score_groups, score_group_name)
            include_flags = VariantDisplayFlags(
                quantization=include_quantization_variants,
                truncate=include_truncate_variants,
                rescore=include_rescore_variants,
                other=include_other_variants,
            )
            language_filter_policy = _language_filter_policy_for_view(
                self.config, view_name, overall=overall
            )
            available_views = _available_view_names(self.config)
            available_view_labels = {
                view: self.config.label_for_view(view)
                for view in available_views
            }
            if not benchmarks:
                empty_view_name = CUSTOM_SCOPE_NAME if view_name == CUSTOM_SCOPE_NAME else CLEAR_SCOPE_NAME
                return LeaderboardResult(
                    view_name=empty_view_name,
                    view_label=self.config.label_for_view(empty_view_name),
                    is_overall=True,
                    score_target=score_target,
                    score_aggregation=score_aggregation,
                    selected_score_metric=selected_score_metric,
                    available_score_metrics=available_score_metrics,
                    expected_tasks=0,
                    rows=[],
                    available_views=available_views,
                    available_view_labels=available_view_labels,
                    include_quantization_variants=include_quantization_variants,
                    include_truncate_variants=include_truncate_variants,
                    include_rescore_variants=include_rescore_variants,
                    include_other_variants=include_other_variants,
                    show_task_scores=False,
                    show_task_z_scores=False,
                    show_task_ranks=False,
                    rank_filtered=rank_filtered,
                    task_filter="",
                    score_groups=[],
                    metric_columns=[],
                    available_languages=[],
                    selected_languages=(),
                    selected_benchmarks=(),
                )
            has_length_filters = _has_task_length_filters(
                query_min_chars=query_min_chars,
                query_max_chars=query_max_chars,
                document_min_chars=document_min_chars,
                document_max_chars=document_max_chars,
            )
            has_parameter_filters = _has_parameter_filters(
                active_params_min_millions=active_params_min_millions,
                active_params_max_millions=active_params_max_millions,
                total_params_min_millions=total_params_min_millions,
                total_params_max_millions=total_params_max_millions,
            )
            if (
                self.use_precomputed
                and not language_filters
                and not show_task_scores
                and not show_task_z_scores
                and not show_task_ranks
                and not ranking_model_filter_terms
                and not has_rank_facet_filters
                and not task_filter.strip()
                and not has_parameter_filters
                and not has_length_filters
                and selected_score_metric == "ndcg@10"
                and view_name != CUSTOM_SCOPE_NAME
                and _language_filter_policy_supports_precomputed(language_filter_policy)
                and (overall is None or score_aggregation == "micro")
            ):
                precomputed = _load_precomputed_leaderboard_rows(
                    duckdb_path=self.duckdb_path,
                    view_name=view_name,
                    score_target=score_target,
                    score_aggregation=score_aggregation,
                    variant_flags=include_flags,
                )
                if precomputed is not None:
                    rows, expected_tasks, available_languages = precomputed
                    rows = _with_model_card_parameters_for_leaderboard_rows(
                        rows, self.model_card_parameters
                    )
                    sorted_rows = sort_rows(rows, sort=sort, direction=direction)
                    request_timing["task_score_count"] = None
                    request_timing["leaderboard_row_count"] = len(sorted_rows)
                    request_timing["precomputed"] = True
                    return LeaderboardResult(
                        view_name=view_name,
                        view_label=self.config.label_for_view(view_name),
                        is_overall=is_overall,
                        score_target=score_target,
                        score_aggregation=score_aggregation,
                        selected_score_metric=selected_score_metric,
                        available_score_metrics=available_score_metrics,
                        expected_tasks=expected_tasks,
                        rows=sorted_rows,
                        available_views=available_views,
                        available_view_labels=available_view_labels,
                        include_quantization_variants=include_quantization_variants,
                        include_truncate_variants=include_truncate_variants,
                        include_rescore_variants=include_rescore_variants,
                        include_other_variants=include_other_variants,
                        show_task_scores=False,
                        show_task_z_scores=False,
                        show_task_ranks=False,
                        task_filter="",
                        score_groups=[
                            ScoreGroup(name=group.name, label=group.display_label)
                            for group in score_groups
                        ],
                        selected_score_group=(
                            ScoreGroup(
                                name=selected_score_group.name,
                                label=selected_score_group.display_label,
                            )
                            if selected_score_group is not None
                            else None
                        ),
                        metric_columns=[],
                        available_languages=available_languages,
                        selected_languages=(),
                        selected_benchmarks=selected_benchmark_names,
                    )
            with timed_operation(
                "viewer.leaderboard.phase", operation="load_task_scores", view=view_name
            ) as phase_timing:
                rows = self._load_task_scores(
                    benchmarks,
                    score_target=score_target,
                    score_metric=selected_score_metric,
                    include_quantization_variants=include_quantization_variants,
                    include_truncate_variants=include_truncate_variants,
                    include_rescore_variants=include_rescore_variants,
                    include_other_variants=include_other_variants,
                )
                phase_timing["task_score_count"] = len(rows)
            rows = _exclude_configured_tasks(rows, self.config)
            if _score_metric_cutoff(selected_score_metric) == 100:
                rows = _exclude_bm25_task_scores(rows)
            if ranking_model_filter_terms:
                with timed_operation(
                    "viewer.leaderboard.phase",
                    operation="filter_models",
                    view=view_name,
                ) as phase_timing:
                    rows = _filter_rows_by_model_terms(rows, ranking_model_filter_terms)
                    phase_timing["task_score_count"] = len(rows)
                    phase_timing["term_count"] = len(ranking_model_filter_terms)
            if has_length_filters:
                with timed_operation(
                    "viewer.leaderboard.phase",
                    operation="filter_task_lengths",
                    view=view_name,
                ) as phase_timing:
                    rows = _filter_rows_by_task_lengths(
                        rows,
                        query_min_chars=query_min_chars,
                        query_max_chars=query_max_chars,
                        document_min_chars=document_min_chars,
                        document_max_chars=document_max_chars,
                    )
                    phase_timing["task_score_count"] = len(rows)
            if has_parameter_filters:
                with timed_operation(
                    "viewer.leaderboard.phase",
                    operation="filter_parameters",
                    view=view_name,
                ) as phase_timing:
                    rows = _filter_rows_by_parameters(
                        rows,
                        active_params_min_millions=active_params_min_millions,
                        active_params_max_millions=active_params_max_millions,
                        total_params_min_millions=total_params_min_millions,
                        total_params_max_millions=total_params_max_millions,
                    )
                    phase_timing["task_score_count"] = len(rows)
            if has_rank_facet_filters:
                with timed_operation(
                    "viewer.leaderboard.phase",
                    operation="filter_facets",
                    view=view_name,
                ) as phase_timing:
                    rows = _filter_rows_by_facets(
                        rows,
                        dim_filters=ranking_dim_filters,
                        quant_filters=ranking_quant_filters,
                        model_type_filters=ranking_model_type_filters,
                        dtype_filters=ranking_dtype_filters,
                        attn_filters=ranking_attn_filters,
                        prompt_filters=ranking_prompt_filters,
                    )
                    phase_timing["task_score_count"] = len(rows)
            available_languages = _language_options(
                rows,
                policy=language_filter_policy,
            )
            selected_languages = _selected_languages(
                language_filters, available_languages
            )
            if selected_languages:
                with timed_operation(
                    "viewer.leaderboard.phase",
                    operation="filter_languages",
                    view=view_name,
                ) as phase_timing:
                    rows = _filter_rows_by_languages(
                        rows, selected_languages, policy=language_filter_policy
                    )
                    phase_timing["task_score_count"] = len(rows)
                    phase_timing["language_count"] = len(selected_languages)
            if ranking_task_filter_terms:
                with timed_operation(
                    "viewer.leaderboard.phase", operation="filter_tasks", view=view_name
                ) as phase_timing:
                    rows = _filter_rows_by_task_terms(rows, ranking_task_filter_terms)
                    phase_timing["task_score_count"] = len(rows)
                    phase_timing["term_count"] = len(ranking_task_filter_terms)
            metric_score_group = selected_score_group
            should_show_task_scores = (
                show_task_scores or show_task_ranks or bool(ranking_task_filter_terms)
            )
            if overall is not None and not ranking_task_filter_terms:
                with timed_operation(
                    "viewer.leaderboard.phase",
                    operation="aggregate_overall",
                    view=view_name,
                ) as phase_timing:
                    rows = _aggregate_overall_scores(
                        rows, overall, score_aggregation=score_aggregation
                    )
                    metric_score_group = _overall_metric_score_group(
                        overall, score_aggregation=score_aggregation
                    )
                    if metric_score_group is None:
                        metric_score_group = _custom_single_component_metric_score_group(
                            self.config,
                            overall,
                        )
                    phase_timing["task_score_count"] = len(rows)
            elif selected_score_group is not None:
                with timed_operation(
                    "viewer.leaderboard.phase",
                    operation="aggregate_score_group",
                    view=view_name,
                ) as phase_timing:
                    rows = _aggregate_benchmark_score_group_scores(
                        rows, selected_score_group
                    )
                    phase_timing["task_score_count"] = len(rows)
            if should_show_task_scores and metric_score_group is None:
                metric_score_group = ScoreGroupConfig(
                    name="task_scores", label="Task Scores", group_by="task_key"
                )
            with timed_operation(
                "viewer.leaderboard.phase", operation="metric_columns", view=view_name
            ) as phase_timing:
                metric_columns = (
                    _metric_columns(rows, metric_score_group)
                    if should_show_task_scores and metric_score_group is not None
                    else []
                )
                if not ranking_task_filter_terms:
                    metric_columns = _filter_metric_columns(
                        rows, metric_score_group, metric_columns, task_filter
                    )
                metric_column_labels = _metric_column_label_overrides(
                    rows=rows,
                    score_group=metric_score_group,
                    metric_columns=metric_columns,
                    config=self.config,
                )
                metric_column_doc_keys = _metric_column_doc_keys(
                    rows=rows,
                    score_group=metric_score_group,
                    metric_columns=metric_columns,
                )
                phase_timing["metric_column_count"] = len(metric_columns)
            with timed_operation(
                "viewer.leaderboard.phase", operation="compute_rows", view=view_name
            ) as phase_timing:
                leaderboard_rows = compute_leaderboard_rows(
                    rows,
                    is_overall=is_overall,
                    score_group=metric_score_group,
                    metric_columns=metric_columns,
                    show_task_z_scores=show_task_z_scores,
                    show_task_ranks=show_task_ranks,
                    use_task_mean_for_overall=bool(ranking_task_filter_terms),
                    overall_score_aggregation=score_aggregation,
                )
                leaderboard_rows = _with_model_card_parameters_for_leaderboard_rows(
                    leaderboard_rows,
                    self.model_card_parameters,
                )
                sort_key = (
                    "mean_score"
                    if ranking_task_filter_terms
                    and sort in {"macro_mean", "micro_mean"}
                    else sort
                )
                sorted_rows = sort_rows(
                    leaderboard_rows, sort=sort_key, direction=direction
                )
                phase_timing["leaderboard_row_count"] = len(sorted_rows)
            request_timing["task_score_count"] = len(rows)
            request_timing["leaderboard_row_count"] = len(sorted_rows)
            return LeaderboardResult(
                view_name=view_name,
                view_label=self.config.label_for_view(view_name),
                is_overall=is_overall,
                score_target=score_target,
                score_aggregation=score_aggregation,
                selected_score_metric=selected_score_metric,
                available_score_metrics=available_score_metrics,
                expected_tasks=len({row.task_key for row in rows}),
                rows=sorted_rows,
                available_views=available_views,
                available_view_labels=available_view_labels,
                include_quantization_variants=include_quantization_variants,
                include_truncate_variants=include_truncate_variants,
                include_rescore_variants=include_rescore_variants,
                include_other_variants=include_other_variants,
                show_task_scores=should_show_task_scores,
                show_task_z_scores=show_task_z_scores,
                show_task_ranks=show_task_ranks,
                rank_filtered=rank_filtered,
                task_filter=task_filter.strip(),
                score_groups=[
                    ScoreGroup(name=group.name, label=group.display_label)
                    for group in score_groups
                ],
                selected_score_group=(
                    ScoreGroup(
                        name=selected_score_group.name,
                        label=selected_score_group.display_label,
                    )
                    if selected_score_group is not None
                    else None
                ),
                metric_columns=metric_columns,
                metric_column_labels=metric_column_labels,
                metric_column_doc_keys=metric_column_doc_keys,
                available_languages=available_languages,
                selected_languages=selected_languages,
                selected_benchmarks=selected_benchmark_names,
            )

    def _resolve_scope(
        self, view_name: str, *, selected_benchmarks: tuple[str, ...]
    ) -> tuple[str, OverallConfig | None, list[str]]:
        if view_name == CLEAR_SCOPE_NAME:
            return CLEAR_SCOPE_NAME, OverallConfig(name=CLEAR_SCOPE_NAME, label=CLEAR_SCOPE_NAME, benchmarks=[]), []
        if view_name == CUSTOM_SCOPE_NAME and not selected_benchmarks:
            return CUSTOM_SCOPE_NAME, OverallConfig(name=CUSTOM_SCOPE_NAME, label=CUSTOM_SCOPE_NAME, benchmarks=[]), []
        if selected_benchmarks:
            selection_keys = normalize_benchmark_selection_values(list(selected_benchmarks), self.config)
            if not selection_keys:
                return CUSTOM_SCOPE_NAME, OverallConfig(name=CUSTOM_SCOPE_NAME, label=CUSTOM_SCOPE_NAME, benchmarks=[]), []
            overall = self.config.overall_for_selected_benchmark_keys(
                name=CUSTOM_SCOPE_NAME,
                label=CUSTOM_SCOPE_NAME,
                selection_keys=selection_keys,
            )
            return CUSTOM_SCOPE_NAME, overall, overall.benchmark_names
        overall = self.config.overall_for_view(view_name)
        if overall is not None:
            return view_name, overall, overall.benchmark_names
        benchmarks = self.config.benchmarks_for_view(view_name)
        return view_name, None, benchmarks

    def _load_task_scores(
        self,
        benchmarks: list[str],
        *,
        score_target: ScoreTarget,
        score_metric: str,
        include_quantization_variants: bool,
        include_truncate_variants: bool,
        include_rescore_variants: bool,
        include_other_variants: bool,
    ) -> list[TaskScore]:
        include_any_variants = (
            include_quantization_variants
            or include_truncate_variants
            or include_rescore_variants
            or include_other_variants
        )
        variant_flags = VariantDisplayFlags(
            quantization=include_quantization_variants,
            truncate=include_truncate_variants,
            rescore=include_rescore_variants,
            other=include_other_variants,
        )
        duckdb_path, duckdb_mtime_ns, duckdb_size = _duckdb_cache_identity(
            self.duckdb_path
        )
        cache_before = _cached_task_scores.cache_info()
        task_scores = list(
            _cached_task_scores(
                duckdb_path,
                duckdb_mtime_ns,
                duckdb_size,
                tuple(benchmarks),
                score_target,
                score_metric,
                include_any_variants,
                variant_flags.quantization,
                variant_flags.truncate,
                variant_flags.rescore,
                variant_flags.other,
            )
        )
        cache_after = _cached_task_scores.cache_info()
        log_event(
            "viewer.leaderboard.cache",
            operation="load_task_scores",
            hit=cache_after.hits > cache_before.hits,
            size=cache_after.currsize,
            task_score_count=len(task_scores),
        )
        return _with_model_card_parameters_for_task_scores(
            task_scores, self.model_card_parameters
        )


def _load_model_card_parameters(
    model_cards_path: Path | None,
) -> dict[str, ModelCardParameters]:
    if model_cards_path is None:
        return {}
    state = _model_cards_cache_state(model_cards_path)
    if state is None:
        return {}
    return _cached_model_card_parameters(str(model_cards_path.resolve()), state)


def _model_cards_cache_state(
    model_cards_path: Path,
) -> tuple[tuple[str, int, int], ...] | None:
    if not model_cards_path.exists():
        return None
    return tuple(
        (str(path.resolve()), path.stat().st_mtime_ns, path.stat().st_size)
        for path in _model_card_yaml_paths(model_cards_path)
    )


@lru_cache(maxsize=16)
def _cached_model_card_parameters(
    model_cards_path: str,
    state: tuple[tuple[str, int, int], ...],
) -> dict[str, ModelCardParameters]:
    del state
    cards = _load_viewer_model_cards(Path(model_cards_path))
    parameters_by_model: dict[str, ModelCardParameters] = {}
    for model_id, card in cards.items():
        parameters = card.get("parameters")
        runtime = card.get("runtime")
        if not isinstance(parameters, dict):
            parameters = {}
        if not isinstance(runtime, dict):
            runtime = {}
        late_interaction = _late_interaction_card_section(card)
        language_support = _language_support_card_section(card)
        parameters_by_model[model_id] = ModelCardParameters(
            active_parameters=_int_or_none(parameters.get("active")),
            total_parameters=_int_or_none(parameters.get("total")),
            max_seq_length=_int_or_none(runtime.get("max_seq_length")),
            late_interaction_query_length=_int_or_none(
                late_interaction.get("query_length")
            ),
            late_interaction_document_length=_int_or_none(
                late_interaction.get("document_length")
            ),
            late_interaction_query_prefix=_str_or_none(
                late_interaction.get("query_prefix")
            ),
            late_interaction_document_prefix=_str_or_none(
                late_interaction.get("document_prefix")
            ),
            late_interaction_query_expansion=_bool_or_none(
                late_interaction.get(
                    "do_query_expansion", late_interaction.get("query_expansion")
                )
            ),
            late_interaction_attend_to_expansion_tokens=_bool_or_none(
                late_interaction.get("attend_to_expansion_tokens")
            ),
            language_support_category=_str_or_none(language_support.get("category")),
            language_support_languages=_str_tuple(language_support.get("languages")),
            language_support_marker=_str_or_none(language_support.get("marker")),
            links=_links_card_section(card),
            license=_license_card_section(card),
        )
    return parameters_by_model


def _load_viewer_model_cards(model_cards_path: Path) -> dict[str, dict[str, Any]]:
    cards: dict[str, dict[str, Any]] = {}
    for card_path in _model_card_yaml_paths(model_cards_path):
        payload = yaml.safe_load(card_path.read_text(encoding="utf-8")) or {}
        if not isinstance(payload, dict):
            continue
        if isinstance(payload.get("id"), str):
            cards[str(payload["id"])] = payload
            continue
        models = payload.get("models", [])
        if not isinstance(models, list):
            continue
        for item in models:
            if isinstance(item, dict) and isinstance(item.get("id"), str):
                cards[str(item["id"])] = item
    return cards


def _model_card_yaml_paths(model_cards_path: Path) -> list[Path]:
    if model_cards_path.is_dir():
        return sorted(
            path
            for pattern in ("*.yaml", "*.yml")
            for path in model_cards_path.glob(pattern)
            if path.is_file()
        )
    return [model_cards_path]


def _late_interaction_card_section(card: dict[str, Any]) -> dict[str, Any]:
    section = card.get("late_interaction")
    if isinstance(section, dict):
        return section
    params = card.get("params")
    if isinstance(params, dict) and isinstance(params.get("late_interaction"), dict):
        return params["late_interaction"]
    return {}


def _language_support_card_section(card: dict[str, Any]) -> dict[str, Any]:
    section = card.get("language_support")
    return section if isinstance(section, dict) else {}


def _links_card_section(card: dict[str, Any]) -> dict[str, Any] | None:
    section = card.get("links")
    if not isinstance(section, dict):
        return None
    normalized: dict[str, Any] = {}
    for key in ("huggingface", "github"):
        url = _str_or_none(section.get(key))
        if url and url.strip():
            normalized[key] = url.strip()
    papers = []
    if isinstance(section.get("papers"), list):
        for paper in section["papers"]:
            if not isinstance(paper, dict):
                continue
            title = _str_or_none(paper.get("title"))
            url = _str_or_none(paper.get("url"))
            if title and title.strip() and url and url.strip():
                papers.append({"title": title.strip(), "url": url.strip()})
    if papers:
        normalized["papers"] = papers
    return normalized or None


def _license_card_section(card: dict[str, Any]) -> dict[str, Any] | None:
    section = card.get("license")
    if not isinstance(section, dict):
        return None
    normalized: dict[str, Any] = {}
    for key in ("id", "label", "type", "commercial_use", "source", "source_url"):
        value = _str_or_none(section.get(key))
        if value and value.strip():
            normalized[key] = value.strip()
    return normalized or None


def _with_model_card_parameters_for_task_scores(
    rows: list[TaskScore],
    parameters_by_model: dict[str, ModelCardParameters],
) -> list[TaskScore]:
    if not parameters_by_model:
        return rows
    return [
        replace(
            row,
            active_parameters=row.active_parameters
            if row.active_parameters is not None
            else _model_card_parameters(row, parameters_by_model).active_parameters,
            total_parameters=row.total_parameters
            if row.total_parameters is not None
            else _model_card_parameters(row, parameters_by_model).total_parameters,
            max_seq_length=row.max_seq_length
            if row.max_seq_length is not None
            else _model_card_parameters(row, parameters_by_model).max_seq_length,
            late_interaction_query_length=row.late_interaction_query_length
            if row.late_interaction_query_length is not None
            else _model_card_parameters(
                row, parameters_by_model
            ).late_interaction_query_length,
            late_interaction_document_length=row.late_interaction_document_length
            if row.late_interaction_document_length is not None
            else _model_card_parameters(
                row, parameters_by_model
            ).late_interaction_document_length,
            late_interaction_query_prefix=row.late_interaction_query_prefix
            if row.late_interaction_query_prefix is not None
            else _model_card_parameters(
                row, parameters_by_model
            ).late_interaction_query_prefix,
            late_interaction_document_prefix=row.late_interaction_document_prefix
            if row.late_interaction_document_prefix is not None
            else _model_card_parameters(
                row, parameters_by_model
            ).late_interaction_document_prefix,
            late_interaction_query_expansion=row.late_interaction_query_expansion
            if row.late_interaction_query_expansion is not None
            else _model_card_parameters(
                row, parameters_by_model
            ).late_interaction_query_expansion,
            late_interaction_attend_to_expansion_tokens=row.late_interaction_attend_to_expansion_tokens
            if row.late_interaction_attend_to_expansion_tokens is not None
            else _model_card_parameters(
                row, parameters_by_model
            ).late_interaction_attend_to_expansion_tokens,
        )
        for row in rows
    ]


def _with_model_card_parameters_for_leaderboard_rows(
    rows: list[LeaderboardRow],
    parameters_by_model: dict[str, ModelCardParameters],
) -> list[LeaderboardRow]:
    if not parameters_by_model:
        return rows
    updated_rows = []
    for row in rows:
        parameters = _model_card_parameters(row, parameters_by_model)
        updated_rows.append(
            row.model_copy(
                update={
                    "active_parameters": row.active_parameters
                    if row.active_parameters is not None
                    else parameters.active_parameters,
                    "total_parameters": row.total_parameters
                    if row.total_parameters is not None
                    else parameters.total_parameters,
                    "max_seq_length": row.max_seq_length
                    if row.max_seq_length is not None
                    else parameters.max_seq_length,
                    "late_interaction_query_length": row.late_interaction_query_length
                    if row.late_interaction_query_length is not None
                    else parameters.late_interaction_query_length,
                    "late_interaction_document_length": row.late_interaction_document_length
                    if row.late_interaction_document_length is not None
                    else parameters.late_interaction_document_length,
                    "late_interaction_query_prefix": row.late_interaction_query_prefix
                    if row.late_interaction_query_prefix is not None
                    else parameters.late_interaction_query_prefix,
                    "late_interaction_document_prefix": row.late_interaction_document_prefix
                    if row.late_interaction_document_prefix is not None
                    else parameters.late_interaction_document_prefix,
                    "late_interaction_query_expansion": row.late_interaction_query_expansion
                    if row.late_interaction_query_expansion is not None
                    else parameters.late_interaction_query_expansion,
                    "late_interaction_attend_to_expansion_tokens": row.late_interaction_attend_to_expansion_tokens
                    if row.late_interaction_attend_to_expansion_tokens is not None
                    else parameters.late_interaction_attend_to_expansion_tokens,
                    "language_support_category": row.language_support_category
                    if row.language_support_category is not None
                    else parameters.language_support_category,
                    "language_support_languages": row.language_support_languages
                    or parameters.language_support_languages,
                    "language_support_marker": row.language_support_marker
                    if row.language_support_marker is not None
                    else parameters.language_support_marker,
                    "links": row.links if row.links is not None else parameters.links,
                    "license": row.license if row.license is not None else parameters.license,
                }
            )
        )
    return updated_rows


def _model_card_parameters(
    row: TaskScore | LeaderboardRow,
    parameters_by_model: dict[str, ModelCardParameters],
) -> ModelCardParameters:
    model_name = row.source_model_name or row.model_name
    return parameters_by_model.get(model_name, ModelCardParameters())


def _int_or_none(value: Any) -> int | None:
    if isinstance(value, bool) or value is None:
        return None
    if isinstance(value, int):
        return value
    try:
        return int(value)
    except (TypeError, ValueError):
        return None


def _str_or_none(value: Any) -> str | None:
    return value if isinstance(value, str) else None


def _bool_or_none(value: Any) -> bool | None:
    return value if isinstance(value, bool) else None


def _str_tuple(value: Any) -> tuple[str, ...]:
    if not isinstance(value, list):
        return ()
    return tuple(item for item in value if isinstance(item, str) and item)


def _load_task_scores_uncached(
    *,
    duckdb_path: Path,
    benchmarks: tuple[str, ...],
    score_target: ScoreTarget,
    score_metric: str,
    include_any_variants: bool,
    variant_flags: VariantDisplayFlags,
) -> tuple[TaskScore, ...]:
    records = TaskResultsRepository(duckdb_path).fetch_task_result_rows(
        benchmarks=list(benchmarks),
        score_target=score_target,
        score_metric=score_metric,
        include_embedding_variants=include_any_variants,
        variant_display_flags=variant_flags,
    )
    task_scores = _task_scores_from_records(
        records, include_any_variants=include_any_variants, variant_flags=variant_flags
    )
    if score_target == "all":
        task_scores = _exclude_reranker_task_scores(task_scores)
    elif score_target == "reranking":
        if _score_metric_cutoff(score_metric) != 100:
            task_scores = _append_bm25_reranking_baseline(
                task_scores,
                duckdb_path=duckdb_path,
                benchmarks=benchmarks,
                score_metric=score_metric,
            )
    return tuple(task_scores)


@lru_cache(maxsize=64)
def _cached_task_scores(
    duckdb_path: str,
    duckdb_mtime_ns: int,
    duckdb_size: int,
    benchmarks: tuple[str, ...],
    score_target: ScoreTarget,
    score_metric: str,
    include_any_variants: bool,
    include_quantization_variants: bool,
    include_truncate_variants: bool,
    include_rescore_variants: bool,
    include_other_variants: bool,
) -> tuple[TaskScore, ...]:
    del duckdb_mtime_ns, duckdb_size
    return _load_task_scores_uncached(
        duckdb_path=Path(duckdb_path),
        benchmarks=benchmarks,
        score_target=score_target,
        score_metric=score_metric,
        include_any_variants=include_any_variants,
        variant_flags=VariantDisplayFlags(
            quantization=include_quantization_variants,
            truncate=include_truncate_variants,
            rescore=include_rescore_variants,
            other=include_other_variants,
        ),
    )


def _clear_task_score_cache() -> None:
    _cached_task_scores.cache_clear()


def _load_precomputed_leaderboard_rows(
    *,
    duckdb_path: Path,
    view_name: str,
    score_target: ScoreTarget,
    score_aggregation: ScoreAggregation,
    variant_flags: VariantDisplayFlags,
) -> tuple[list[LeaderboardRow], int, list[LanguageOption]] | None:
    if not duckdb_path.exists():
        return None
    con = duckdb.connect(str(duckdb_path), read_only=True)
    try:
        if not _table_exists(con, "viewer_leaderboard_rows"):
            return None
        rows = con.execute(
            """
            SELECT
                expected_tasks,
                borda_rank,
                mean_rank,
                model_name,
                borda_score,
                mean_score,
                macro_mean,
                micro_mean,
                task_count,
                active_parameters,
                total_parameters,
                max_seq_length,
                dtype,
                attn_implementation,
                prompt_summary,
                trust_remote_code,
                embedding_variant_name,
                embedding_dim,
                quantization,
                source_model_name,
                base_score_delta_percent
            FROM viewer_leaderboard_rows
            WHERE view_name = ?
              AND score_target = ?
              AND include_quantization_variants = ?
              AND include_truncate_variants = ?
              AND include_rescore_variants = ?
              AND include_other_variants = ?
            """,
            [
                view_name,
                score_target,
                variant_flags.quantization,
                variant_flags.truncate,
                variant_flags.rescore,
                variant_flags.other,
            ],
        ).fetchall()
        language_options: list[LanguageOption] = []
        if _table_exists(con, "viewer_leaderboard_language_options"):
            language_options = [
                LanguageOption(
                    code=str(row[0]), label=str(row[1]), task_count=int(row[2])
                )
                for row in con.execute(
                    """
                    SELECT code, label, task_count
                    FROM viewer_leaderboard_language_options
                    WHERE view_name = ?
                      AND score_target = ?
                      AND include_quantization_variants = ?
                      AND include_truncate_variants = ?
                      AND include_rescore_variants = ?
                      AND include_other_variants = ?
                    ORDER BY task_count DESC, lower(label), code
                    """,
                    [
                        view_name,
                        score_target,
                        variant_flags.quantization,
                        variant_flags.truncate,
                        variant_flags.rescore,
                        variant_flags.other,
                    ],
                ).fetchall()
            ]
    finally:
        con.close()
    if score_target == "all":
        rows = [
            row
            for row in rows
            if not _is_reranker_model(model_name=str(row[3]), model_type=None)
        ]
    elif score_target == "reranking" and not _precomputed_rows_include_bm25(rows):
        return None
    if not rows:
        return None
    expected_tasks = int(rows[0][0])
    leaderboard_rows = [
        LeaderboardRow(
            borda_rank=float(row[1]),
            mean_rank=float(row[2]),
            model_name=str(row[3]),
            borda_score=float(row[4]),
            mean_score=_precomputed_mean_score(
                stored_mean_score=float(row[5]),
                macro_mean=float(row[6]) if row[6] is not None else None,
                micro_mean=float(row[7]) if row[7] is not None else None,
                score_aggregation=score_aggregation,
            ),
            macro_mean=float(row[6]) if row[6] is not None else None,
            micro_mean=float(row[7]) if row[7] is not None else None,
            task_count=int(row[8]),
            active_parameters=int(row[9]) if row[9] is not None else None,
            total_parameters=int(row[10]) if row[10] is not None else None,
            max_seq_length=int(row[11]) if row[11] is not None else None,
            dtype=str(row[12]) if row[12] is not None else None,
            attn_implementation=str(row[13]) if row[13] is not None else None,
            prompt_summary=str(row[14]) if row[14] is not None else None,
            trust_remote_code=bool(row[15]) if row[15] is not None else None,
            embedding_variant_name=str(row[16]) if row[16] is not None else None,
            embedding_dim=int(row[17]) if row[17] is not None else None,
            quantization=str(row[18]) if row[18] is not None else None,
            source_model_name=str(row[19]) if row[19] is not None else None,
            base_score_delta_percent=float(row[20]) if row[20] is not None else None,
        )
        for row in rows
    ]
    mean_rank_by_model = _rank_desc((row.model_name, row.mean_score) for row in leaderboard_rows)
    leaderboard_rows = [
        row.model_copy(update={"mean_rank": mean_rank_by_model[row.model_name]})
        for row in leaderboard_rows
    ]
    return (leaderboard_rows, expected_tasks, language_options)


def _precomputed_mean_score(
    *,
    stored_mean_score: float,
    macro_mean: float | None,
    micro_mean: float | None,
    score_aggregation: ScoreAggregation,
) -> float:
    if score_aggregation == "micro" and micro_mean is not None:
        return micro_mean
    if score_aggregation == "macro" and macro_mean is not None:
        return macro_mean
    return stored_mean_score


def _duckdb_cache_identity(duckdb_path: Path) -> tuple[str, int, int]:
    resolved_path = duckdb_path.resolve()
    try:
        stat_result = resolved_path.stat()
    except FileNotFoundError:
        return str(resolved_path), 0, 0
    return str(resolved_path), stat_result.st_mtime_ns, stat_result.st_size


def _append_bm25_reranking_baseline(
    task_scores: list[TaskScore],
    *,
    duckdb_path: Path,
    benchmarks: tuple[str, ...],
    score_metric: str = "ndcg@10",
) -> list[TaskScore]:
    if not task_scores:
        return task_scores
    bm25_records = TaskResultsRepository(duckdb_path).fetch_task_result_rows(
        benchmarks=list(benchmarks),
        score_target="all",
        score_metric=score_metric,
        include_embedding_variants=False,
        variant_display_flags=VariantDisplayFlags(),
    )
    bm25_scores = _task_scores_from_records(
        bm25_records,
        include_any_variants=False,
        variant_flags=VariantDisplayFlags(),
    )
    return _append_missing_bm25_task_scores(task_scores, bm25_scores)


def _append_missing_bm25_task_scores(
    task_scores: list[TaskScore], candidate_scores: list[TaskScore]
) -> list[TaskScore]:
    existing_keys = {_task_score_identity(row) for row in task_scores}
    rows = list(task_scores)
    for row in candidate_scores:
        if not _is_bm25_model(
            model_name=row.source_model_name or row.model_name,
            model_type=row.model_type,
        ):
            continue
        key = _task_score_identity(row)
        if key in existing_keys:
            continue
        rows.append(row)
        existing_keys.add(key)
    return rows


def _task_score_identity(
    row: TaskScore,
) -> tuple[str, str, str, str, str, str, str | None, str | None]:
    return (
        row.source_model_name or row.model_name,
        row.benchmark,
        row.dataset_id,
        row.split_name,
        row.task_name,
        row.task_key,
        row.embedding_variant_name,
        row.quantization,
    )


def _precomputed_rows_include_bm25(rows: list[tuple[Any, ...]]) -> bool:
    return any(
        _is_bm25_model(model_name=str(row[19] or row[3]), model_type=None)
        for row in rows
    )


def _task_scores_from_records(
    records: list[TaskResultRow],
    *,
    include_any_variants: bool,
    variant_flags: VariantDisplayFlags,
) -> list[TaskScore]:
    task_scores: list[TaskScore] = []
    with timed_operation(
        "viewer.leaderboard.phase", operation="filter_variant_records"
    ) as timing:
        filtered_records = [
            record
            for record in records
            if include_variant_row(
                embedding_variant_name=record.embedding_variant_name,
                quantization=record.quantization,
                flags=variant_flags,
            )
        ]
        filtered_records = _drop_noop_truncate_duplicate_records(filtered_records)
        timing["record_count"] = len(records)
        timing["filtered_record_count"] = len(filtered_records)
    with timed_operation(
        "viewer.leaderboard.phase", operation="display_model_names"
    ) as timing:
        model_names = _record_display_model_names(
            filtered_records, include_variant_details=include_any_variants
        )
        timing["record_count"] = len(filtered_records)
    with timed_operation(
        "viewer.leaderboard.phase", operation="build_task_scores"
    ) as timing:
        for record, model_name in zip(filtered_records, model_names, strict=True):
            task_scores.append(
                TaskScore(
                    model_name=model_name,
                    model_type=record.model_type,
                    benchmark=record.benchmark,
                    dataset_id=record.dataset_id,
                    dataset_name=record.dataset_name,
                    split_name=record.split_name,
                    task_name=record.task_name,
                    task_key=record.task_key,
                    score=record.score,
                    language=record.language,
                    languages=tuple(record.languages),
                    primary_languages=tuple(record.primary_languages),
                    active_parameters=record.active_parameters,
                    total_parameters=record.total_parameters,
                    max_seq_length=record.max_seq_length,
                    dtype=record.dtype,
                    attn_implementation=record.attn_implementation,
                    prompt_summary=record.prompt_summary,
                    trust_remote_code=record.trust_remote_code,
                    embedding_variant_name=record.embedding_variant_name,
                    embedding_dim=record.embedding_dim,
                    quantization=record.quantization,
                    source_model_name=record.model_name,
                    query_mean_chars=record.query_mean_chars,
                    document_mean_chars=record.document_mean_chars,
                    late_interaction_query_length=record.late_interaction_query_length,
                    late_interaction_document_length=record.late_interaction_document_length,
                    late_interaction_query_prefix=record.late_interaction_query_prefix,
                    late_interaction_document_prefix=record.late_interaction_document_prefix,
                    late_interaction_query_expansion=record.late_interaction_query_expansion,
                    late_interaction_attend_to_expansion_tokens=record.late_interaction_attend_to_expansion_tokens,
                )
            )
        timing["task_score_count"] = len(task_scores)
    return task_scores


def _exclude_reranker_task_scores(rows: list[TaskScore]) -> list[TaskScore]:
    return [
        row
        for row in rows
        if not _is_reranker_model(
            model_name=row.source_model_name or row.model_name,
            model_type=row.model_type,
        )
    ]


def _drop_noop_truncate_duplicate_records(
    records: list[TaskResultRow],
) -> list[TaskResultRow]:
    original_keys = {
        _noop_truncate_duplicate_key(record)
        for record in records
        if _truncate_dim_from_variant_name(record.embedding_variant_name) is None
    }
    if not original_keys:
        return records
    return [
        record
        for record in records
        if not (
            _noop_truncate_dim(record) is not None
            and _noop_truncate_duplicate_key(record) in original_keys
        )
    ]


def _noop_truncate_duplicate_key(record: TaskResultRow) -> tuple[Any, ...]:
    return (
        record.model_name,
        record.model_type,
        record.benchmark,
        record.dataset_id,
        record.split_name,
        record.task_key,
        record.dtype,
        record.attn_implementation,
        record.prompt_summary,
        record.trust_remote_code,
        record.embedding_dim,
        record.quantization,
    )


def _noop_truncate_dim(record: TaskResultRow) -> int | None:
    truncate_dim = _truncate_dim_from_variant_name(record.embedding_variant_name)
    if (
        truncate_dim is None
        or record.embedding_dim is None
        or truncate_dim != record.embedding_dim
    ):
        return None
    return truncate_dim


def _truncate_dim_from_variant_name(variant_name: str | None) -> int | None:
    match = re.search(r"(?:^|_)truncate_dim_(\d+)(?:_|$)", variant_name or "")
    if match is None:
        return None
    return int(match.group(1))


def _is_reranker_model(*, model_name: str, model_type: str | None) -> bool:
    return is_reranker_model(model_name=model_name, model_type=model_type)


def _is_bm25_model(*, model_name: str, model_type: str | None) -> bool:
    return is_bm25_model(model_name=model_name, model_type=model_type)


def _exclude_bm25_task_scores(rows: list[TaskScore]) -> list[TaskScore]:
    return [
        row
        for row in rows
        if not _is_bm25_model(
            model_name=row.source_model_name or row.model_name,
            model_type=row.model_type,
        )
    ]


def _normalize_score_metric(score_metric: str, available_metrics: list[str]) -> str:
    metric = score_metric.strip().casefold()
    return metric if metric in set(available_metrics) else "ndcg@10"


def _score_metric_cutoff(score_metric: str) -> int | None:
    _, separator, cutoff = score_metric.partition("@")
    if not separator or not cutoff.isdigit():
        return None
    return int(cutoff)


def compute_leaderboard_rows(
    rows: list[TaskScore],
    *,
    is_overall: bool,
    score_group: ScoreGroupConfig | None = None,
    metric_columns: list[str] | None = None,
    show_task_z_scores: bool = False,
    show_task_ranks: bool = False,
    use_task_mean_for_overall: bool = False,
    overall_score_aggregation: ScoreAggregation = "micro",
) -> list[LeaderboardRow]:
    expected_tasks = {row.task_key for row in rows}
    if not expected_tasks:
        return []

    rows_by_model: dict[str, list[TaskScore]] = defaultdict(list)
    task_keys_by_model: dict[str, set[str]] = defaultdict(set)
    for row in rows:
        rows_by_model[row.model_name].append(row)
        task_keys_by_model[row.model_name].add(row.task_key)

    complete_models = {
        model_name
        for model_name, task_keys in task_keys_by_model.items()
        if task_keys == expected_tasks
    }
    complete_rows = [row for row in rows if row.model_name in complete_models]
    borda_scores = _borda_scores(complete_rows)
    borda_score_z_values = (
        _borda_score_z_values(borda_scores=borda_scores, rows=complete_rows)
        if show_task_z_scores
        else {}
    )
    metric_columns = metric_columns or []
    z_values_by_model = (
        _metric_z_values_by_model(
            complete_rows, score_group=score_group, metric_columns=metric_columns
        )
        if show_task_z_scores and metric_columns
        else {}
    )
    aggregate_z_values_by_model = (
        _aggregate_z_values_by_model(
            complete_rows,
            is_overall=is_overall,
            overall_score_aggregation=overall_score_aggregation,
        )
        if show_task_z_scores
        else {}
    )
    metric_rank_values_by_model = (
        _metric_rank_values_by_model(
            complete_rows, score_group=score_group, metric_columns=metric_columns
        )
        if show_task_ranks and metric_columns
        else {}
    )

    leaderboard_rows: list[LeaderboardRow] = []
    for model_name in sorted(complete_models):
        model_rows = rows_by_model[model_name]
        first = model_rows[0]
        micro_mean = _mean(row.score * 100.0 for row in model_rows)
        benchmark_means = [
            _mean(row.score * 100.0 for row in benchmark_rows)
            for benchmark_rows in _group_by_benchmark(model_rows).values()
        ]
        macro_mean = _mean(benchmark_means)
        mean_score = (
            micro_mean
            if use_task_mean_for_overall
            or (is_overall and overall_score_aggregation == "micro")
            else macro_mean
            if is_overall
            else micro_mean
        )
        metric_values = _metric_values(
            model_rows, score_group=score_group, metric_columns=metric_columns
        )
        metric_z_values = z_values_by_model.get(model_name, {})
        metric_rank_values = metric_rank_values_by_model.get(model_name, {})
        aggregate_z_values = aggregate_z_values_by_model.get(model_name, {})
        leaderboard_rows.append(
            LeaderboardRow(
                borda_rank=0.0,
                mean_rank=0.0,
                model_name=model_name,
                model_type=first.model_type,
                borda_score=_mean(borda_scores[model_name]),
                borda_score_z=borda_score_z_values.get(model_name),
                mean_score=mean_score,
                mean_score_z=aggregate_z_values.get("mean_score"),
                macro_mean=macro_mean if is_overall else None,
                macro_mean_z=aggregate_z_values.get("macro_mean")
                if is_overall
                else None,
                micro_mean=micro_mean if is_overall else None,
                micro_mean_z=aggregate_z_values.get("micro_mean")
                if is_overall
                else None,
                task_count=len({row.task_key for row in model_rows}),
                active_parameters=first.active_parameters,
                total_parameters=first.total_parameters,
                max_seq_length=first.max_seq_length,
                dtype=first.dtype,
                attn_implementation=first.attn_implementation,
                prompt_summary=first.prompt_summary,
                trust_remote_code=first.trust_remote_code,
                embedding_variant_name=first.embedding_variant_name,
                embedding_dim=first.embedding_dim,
                quantization=first.quantization,
                source_model_name=first.source_model_name,
                late_interaction_query_length=first.late_interaction_query_length,
                late_interaction_document_length=first.late_interaction_document_length,
                late_interaction_query_prefix=first.late_interaction_query_prefix,
                late_interaction_document_prefix=first.late_interaction_document_prefix,
                late_interaction_query_expansion=first.late_interaction_query_expansion,
                late_interaction_attend_to_expansion_tokens=first.late_interaction_attend_to_expansion_tokens,
                metric_values=metric_values,
                metric_z_values=metric_z_values,
                metric_rank_values=metric_rank_values,
                metric_sort_values=metric_rank_values
                if show_task_ranks
                else metric_z_values
                if show_task_z_scores
                else metric_values,
            )
        )

    borda_rank_by_model = _rank_desc(
        (row.model_name, row.borda_score) for row in leaderboard_rows
    )
    mean_rank_by_model = _rank_desc(
        (row.model_name, row.mean_score) for row in leaderboard_rows
    )
    ranked_rows = [
        row.model_copy(
            update={
                "borda_rank": borda_rank_by_model[row.model_name],
                "mean_rank": mean_rank_by_model[row.model_name],
            }
        )
        for row in leaderboard_rows
    ]
    return _with_base_score_delta_percent(ranked_rows)


def sort_rows(
    rows: list[LeaderboardRow], *, sort: str, direction: SortDirection
) -> list[LeaderboardRow]:
    metric_key = sort.removeprefix("metric:") if sort.startswith("metric:") else None
    if metric_key is not None and not any(
        metric_key in row.metric_sort_values or metric_key in row.metric_values
        for row in rows
    ):
        metric_key = None
    sort_key = sort if sort in SORT_COLUMNS else "borda_rank"
    reverse = direction == "desc" and (metric_key is not None or sort in SORT_COLUMNS)

    def key(row: LeaderboardRow) -> tuple[int, Any, float, str]:
        value = (
            row.metric_sort_values.get(metric_key, row.metric_values.get(metric_key))
            if metric_key is not None
            else getattr(row, sort_key)
        )
        missing = value is None
        normalized = str(value).lower() if isinstance(value, str) else value
        return (1 if missing else 0, normalized, row.borda_rank, row.model_name.lower())

    return sorted(rows, key=key, reverse=reverse)


def _borda_scores(rows: list[TaskScore]) -> dict[str, list[float]]:
    by_task: dict[str, list[TaskScore]] = defaultdict(list)
    for row in rows:
        by_task[row.task_key].append(row)

    scores_by_model: dict[str, list[float]] = defaultdict(list)
    for task_rows in by_task.values():
        rank_by_model = _rank_desc((row.model_name, row.score) for row in task_rows)
        model_count = len(rank_by_model)
        for row in task_rows:
            rank = rank_by_model[row.model_name]
            score = (
                100.0
                if model_count <= 1
                else 100.0 * (model_count - rank) / (model_count - 1)
            )
            scores_by_model[row.model_name].append(score)
    return scores_by_model


def _borda_score_z_values(
    *,
    borda_scores: dict[str, list[float]],
    rows: list[TaskScore],
) -> dict[str, float]:
    aggregate_scores = {
        model_name: _mean(scores)
        for model_name, scores in borda_scores.items()
        if scores
    }
    base_model_names = {
        row.model_name
        for row in rows
        if row.embedding_variant_name is None
    }
    base_scores = [
        score
        for model_name, score in aggregate_scores.items()
        if model_name in base_model_names
    ]
    stddev = _population_stddev(base_scores)
    if stddev is None or stddev <= 0.0:
        return {}
    mean = _mean(base_scores)
    return {
        model_name: (score - mean) / stddev
        for model_name, score in aggregate_scores.items()
    }


def _rank_desc(items: Iterable[tuple[str, float]]) -> dict[str, float]:
    sorted_items = sorted(items, key=lambda item: (-item[1], item[0]))
    ranks: dict[str, float] = {}
    index = 0
    while index < len(sorted_items):
        end = index + 1
        while (
            end < len(sorted_items) and sorted_items[end][1] == sorted_items[index][1]
        ):
            end += 1
        rank = float(index + 1)
        for model_name, _ in sorted_items[index:end]:
            ranks[model_name] = rank
        index = end
    return ranks


def _average_rank_desc(items: Iterable[tuple[str, float]]) -> dict[str, float]:
    sorted_items = sorted(items, key=lambda item: (-item[1], item[0]))
    ranks: dict[str, float] = {}
    index = 0
    while index < len(sorted_items):
        end = index + 1
        while (
            end < len(sorted_items) and sorted_items[end][1] == sorted_items[index][1]
        ):
            end += 1
        rank = (index + 1 + end) / 2
        for model_name, _ in sorted_items[index:end]:
            ranks[model_name] = float(rank)
        index = end
    return ranks


def _group_by_benchmark(rows: list[TaskScore]) -> dict[str, list[TaskScore]]:
    grouped: dict[str, list[TaskScore]] = defaultdict(list)
    for row in rows:
        grouped[row.benchmark].append(row)
    return grouped


def _aggregate_overall_scores(
    rows: list[TaskScore],
    overall: OverallConfig,
    *,
    score_aggregation: ScoreAggregation,
) -> list[TaskScore]:
    component_by_benchmark = {
        component.name: component for component in overall.benchmark_components
    }
    if score_aggregation == "micro":
        return rows

    expected_raw_tasks: dict[str, set[str]] = defaultdict(set)
    raw_tasks_by_model_benchmark: dict[tuple[str, str], set[str]] = defaultdict(set)
    for row in rows:
        expected_raw_tasks[row.benchmark].add(row.task_key)
        raw_tasks_by_model_benchmark[(row.model_name, row.benchmark)].add(row.task_key)

    complete_inputs: dict[tuple[str, str], list[TaskScore]] = defaultdict(list)
    for row in rows:
        component = component_by_benchmark[row.benchmark]
        model_benchmark = (row.model_name, row.benchmark)
        if (
            raw_tasks_by_model_benchmark[model_benchmark]
            != expected_raw_tasks[row.benchmark]
        ):
            continue
        complete_inputs[(row.model_name, component.name)].append(row)

    aggregated: list[TaskScore] = []
    for (model_name, benchmark), benchmark_rows in complete_inputs.items():
        component = component_by_benchmark[benchmark]
        score_rows = benchmark_rows
        if component.group_by is not None:
            group_inputs: dict[str, list[TaskScore]] = defaultdict(list)
            for row in benchmark_rows:
                group_inputs[_score_group_key(row, component.group_by)].append(row)
            score_rows = [
                _aggregate_task_score_rows(
                    model_name=model_name,
                    benchmark=benchmark,
                    aggregate_key=group_key,
                    aggregate_rows=group_rows,
                )
                for group_key, group_rows in group_inputs.items()
            ]
        aggregated.append(
            _aggregate_task_score_rows(
                model_name=model_name,
                benchmark=benchmark,
                aggregate_key=benchmark,
                aggregate_rows=score_rows,
            )
        )
    return aggregated


def _aggregate_task_score_rows(
    *,
    model_name: str,
    benchmark: str,
    aggregate_key: str,
    aggregate_rows: list[TaskScore],
) -> TaskScore:
    first = aggregate_rows[0]
    return TaskScore(
        model_name=model_name,
        model_type=first.model_type,
        benchmark=benchmark,
        dataset_id=benchmark,
        dataset_name=benchmark,
        split_name="",
        task_name=aggregate_key,
        task_key=f"{benchmark}::{aggregate_key}",
        score=_mean(row.score for row in aggregate_rows),
        language=first.language,
        languages=tuple(
            sorted({language for row in aggregate_rows for language in row.languages})
        ),
        primary_languages=tuple(
            sorted(
                {
                    language
                    for row in aggregate_rows
                    for language in row.primary_languages
                }
            )
        ),
        active_parameters=first.active_parameters,
        total_parameters=first.total_parameters,
        max_seq_length=first.max_seq_length,
        dtype=first.dtype,
        attn_implementation=first.attn_implementation,
        prompt_summary=first.prompt_summary,
        trust_remote_code=first.trust_remote_code,
        embedding_variant_name=first.embedding_variant_name,
        embedding_dim=first.embedding_dim,
        quantization=first.quantization,
        source_model_name=first.source_model_name,
        query_mean_chars=_mean_optional(row.query_mean_chars for row in aggregate_rows),
        document_mean_chars=_mean_optional(
            row.document_mean_chars for row in aggregate_rows
        ),
        late_interaction_query_length=first.late_interaction_query_length,
        late_interaction_document_length=first.late_interaction_document_length,
        late_interaction_query_prefix=first.late_interaction_query_prefix,
        late_interaction_document_prefix=first.late_interaction_document_prefix,
        late_interaction_query_expansion=first.late_interaction_query_expansion,
        late_interaction_attend_to_expansion_tokens=first.late_interaction_attend_to_expansion_tokens,
    )


def _aggregate_benchmark_score_group_scores(
    rows: list[TaskScore], score_group: ScoreGroupConfig
) -> list[TaskScore]:
    expected_raw_tasks: dict[str, set[str]] = defaultdict(set)
    raw_tasks_by_model_benchmark: dict[tuple[str, str], set[str]] = defaultdict(set)
    for row in rows:
        expected_raw_tasks[row.benchmark].add(row.task_key)
        raw_tasks_by_model_benchmark[(row.model_name, row.benchmark)].add(row.task_key)

    aggregate_inputs: dict[tuple[str, str, str], list[TaskScore]] = defaultdict(list)
    for row in rows:
        model_benchmark = (row.model_name, row.benchmark)
        if (
            raw_tasks_by_model_benchmark[model_benchmark]
            != expected_raw_tasks[row.benchmark]
        ):
            continue
        aggregate_key = _score_group_key(row, score_group.group_by)
        aggregate_inputs[(row.model_name, row.benchmark, aggregate_key)].append(row)

    aggregated: list[TaskScore] = []
    for (
        model_name,
        benchmark,
        aggregate_key,
    ), aggregate_rows in aggregate_inputs.items():
        first = aggregate_rows[0]
        aggregated.append(
            TaskScore(
                model_name=model_name,
                model_type=first.model_type,
                benchmark=benchmark,
                dataset_id=aggregate_key
                if score_group.group_by == "dataset_id"
                else first.dataset_id,
                dataset_name=aggregate_key
                if score_group.group_by == "dataset_name"
                else first.dataset_name,
                split_name=aggregate_key
                if score_group.group_by == "split_name"
                else first.split_name,
                task_name=aggregate_key
                if score_group.group_by == "task_name"
                else first.task_name,
                task_key=aggregate_key
                if score_group.group_by == "task_key"
                else f"{benchmark}::{score_group.group_by}::{aggregate_key}",
                score=_mean(row.score for row in aggregate_rows),
                language=first.language,
                languages=tuple(
                    sorted(
                        {
                            language
                            for row in aggregate_rows
                            for language in row.languages
                        }
                    )
                ),
                primary_languages=tuple(
                    sorted(
                        {
                            language
                            for row in aggregate_rows
                            for language in row.primary_languages
                        }
                    )
                ),
                active_parameters=first.active_parameters,
                total_parameters=first.total_parameters,
                max_seq_length=first.max_seq_length,
                dtype=first.dtype,
                attn_implementation=first.attn_implementation,
                prompt_summary=first.prompt_summary,
                trust_remote_code=first.trust_remote_code,
                embedding_variant_name=first.embedding_variant_name,
                embedding_dim=first.embedding_dim,
                quantization=first.quantization,
                source_model_name=first.source_model_name,
                query_mean_chars=_mean_optional(
                    row.query_mean_chars for row in aggregate_rows
                ),
                document_mean_chars=_mean_optional(
                    row.document_mean_chars for row in aggregate_rows
                ),
                late_interaction_query_length=first.late_interaction_query_length,
                late_interaction_document_length=first.late_interaction_document_length,
                late_interaction_query_prefix=first.late_interaction_query_prefix,
                late_interaction_document_prefix=first.late_interaction_document_prefix,
                late_interaction_query_expansion=first.late_interaction_query_expansion,
                late_interaction_attend_to_expansion_tokens=first.late_interaction_attend_to_expansion_tokens,
            )
        )
    return aggregated


def _with_base_score_delta_percent(rows: list[LeaderboardRow]) -> list[LeaderboardRow]:
    base_score_by_source_model = {
        row.source_model_name: row.mean_score
        for row in rows
        if row.source_model_name is not None
        and row.embedding_variant_name is None
        and row.mean_score != 0.0
    }
    return [
        row.model_copy(
            update={
                "base_score_delta_percent": _base_score_delta_percent(
                    score=row.mean_score,
                    base_score=(
                        base_score_by_source_model.get(row.source_model_name)
                        if row.source_model_name is not None
                        else None
                    ),
                    embedding_variant_name=row.embedding_variant_name,
                )
            }
        )
        for row in rows
    ]


def _base_score_delta_percent(
    *,
    score: float,
    base_score: float | None,
    embedding_variant_name: str | None,
) -> float | None:
    if embedding_variant_name is None or base_score is None:
        return None
    return 100.0 * (score - base_score) / base_score


def _exclude_configured_tasks(
    rows: list[TaskScore], config: ViewerConfig
) -> list[TaskScore]:
    excluded_by_benchmark = {
        benchmark.name: set(benchmark.excluded_tasks)
        for benchmark in config.benchmarks
        if benchmark.excluded_tasks
    }
    if not excluded_by_benchmark:
        return rows
    return [
        row
        for row in rows
        if row.task_name not in excluded_by_benchmark.get(row.benchmark, set())
        and row.task_key not in excluded_by_benchmark.get(row.benchmark, set())
    ]


def _language_options(
    rows: list[TaskScore],
    *,
    mode: LanguageFilterMode = "languages",
    allowed_languages: tuple[str, ...] = (),
    policy: LanguageFilterPolicy | None = None,
) -> list[LanguageOption]:
    task_keys_by_language: dict[str, set[str]] = defaultdict(set)
    for row in rows:
        for language in _language_codes_for_row(
            row, mode=mode, allowed_languages=allowed_languages, policy=policy
        ):
            task_keys_by_language[language].add(row.task_key)
    return [
        LanguageOption(
            code=language, label=_language_label(language), task_count=len(task_keys)
        )
        for language, task_keys in sorted(
            task_keys_by_language.items(),
            key=lambda item: (-len(item[1]), item[0]),
        )
    ]


def _selected_languages(
    language_filters: tuple[str, ...], options: list[LanguageOption]
) -> tuple[str, ...]:
    available = {option.code for option in options}
    selected = []
    for language in language_filters:
        if language in available and language not in selected:
            selected.append(language)
    return tuple(selected)


def _filter_rows_by_languages(
    rows: list[TaskScore],
    selected_languages: tuple[str, ...],
    *,
    mode: LanguageFilterMode = "languages",
    policy: LanguageFilterPolicy | None = None,
) -> list[TaskScore]:
    selected = set(selected_languages)
    return [
        row
        for row in rows
        if selected.intersection(_language_codes_for_row(row, mode=mode, policy=policy))
    ]


def _filter_rows_by_model_terms(
    rows: list[TaskScore], terms: tuple[str, ...]
) -> list[TaskScore]:
    if not terms:
        return rows
    return [row for row in rows if text_matches_filter_terms(row.model_name, terms)]


def _filter_rows_by_task_terms(
    rows: list[TaskScore], terms: tuple[str, ...]
) -> list[TaskScore]:
    if not terms:
        return rows
    return [row for row in rows if _task_row_matches_filter_terms(row, terms)]


def _has_facet_filters(
    *,
    dim_filters: tuple[str, ...],
    quant_filters: tuple[str, ...],
    model_type_filters: tuple[str, ...],
    dtype_filters: tuple[str, ...],
    attn_filters: tuple[str, ...],
    prompt_filters: tuple[str, ...],
) -> bool:
    return any(
        (
            dim_filters,
            quant_filters,
            model_type_filters,
            dtype_filters,
            attn_filters,
            prompt_filters,
        )
    )


def _filter_rows_by_facets(
    rows: list[TaskScore],
    *,
    dim_filters: tuple[str, ...],
    quant_filters: tuple[str, ...],
    model_type_filters: tuple[str, ...],
    dtype_filters: tuple[str, ...],
    attn_filters: tuple[str, ...],
    prompt_filters: tuple[str, ...],
) -> list[TaskScore]:
    selected_dims = set(dim_filters)
    selected_quants = set(quant_filters)
    selected_model_types = set(model_type_filters)
    selected_dtypes = set(dtype_filters)
    selected_attn = set(attn_filters)
    selected_prompts = set(prompt_filters)
    return [
        row
        for row in rows
        if (not selected_dims or _dim_bucket(row.embedding_dim) in selected_dims)
        and (not selected_quants or _quant_bucket(row.quantization) in selected_quants)
        and (
            not selected_model_types
            or model_type_filter_key(
                model_name=row.source_model_name or row.model_name,
                model_type=row.model_type,
            )
            in selected_model_types
        )
        and (not selected_dtypes or _dtype_bucket(row.dtype) in selected_dtypes)
        and (
            not selected_attn or _attn_bucket(row.attn_implementation) in selected_attn
        )
        and (
            not selected_prompts
            or _prompt_bucket(row.prompt_summary) in selected_prompts
        )
    ]


def _dim_bucket(value: int | None) -> str:
    if value is None:
        return "__unknown__"
    if value >= 1025:
        return "1025+"
    return str(value)


def _quant_bucket(value: str | None) -> str:
    return value or "__none__"


def _dtype_bucket(value: str | None) -> str:
    return value or "__unknown__"


def _attn_bucket(value: str | None) -> str:
    return value or "__unknown__"


def _prompt_bucket(value: str | None) -> str:
    if value is None:
        return "model_default"
    return value.replace(" + ", "_").replace(" ", "_")


def _task_row_matches_filter_terms(row: TaskScore, terms: tuple[str, ...]) -> bool:
    return any(
        text_matches_filter_terms(label, terms)
        for label in (
            row.task_name,
            row.task_key,
            row.dataset_name,
            row.dataset_id,
            row.split_name,
            row.benchmark,
        )
    )


def _language_codes_for_row(
    row: TaskScore,
    *,
    mode: LanguageFilterMode,
    allowed_languages: tuple[str, ...] = (),
    policy: LanguageFilterPolicy | None = None,
) -> tuple[str, ...]:
    if policy is not None:
        mode = (policy.modes_by_benchmark or {}).get(row.benchmark, policy.default_mode)
        allowed_languages = (policy.allowed_languages_by_benchmark or {}).get(
            row.benchmark,
            policy.default_allowed_languages,
        )
    if mode == "primary_language":
        languages = _primary_languages_for_row(row)
    else:
        languages = row.languages
    if not allowed_languages:
        return languages
    allowed = set(allowed_languages)
    return tuple(language for language in languages if language in allowed)


def _primary_languages_for_row(row: TaskScore) -> tuple[str, ...]:
    if row.primary_languages:
        return row.primary_languages
    language = _primary_language_for_row(row)
    return (language,) if language else ()


def _primary_language_for_row(row: TaskScore) -> str | None:
    if row.language and row.language != "multilingual":
        return row.language
    dataset_language = _dataset_name_language_suffix(row.dataset_name)
    if dataset_language:
        return dataset_language
    split_language = _language_code_from_text(row.split_name)
    if split_language:
        return split_language
    return row.languages[0] if row.languages else None


def _dataset_name_language_suffix(dataset_name: str) -> str | None:
    if "-" not in dataset_name:
        return None
    suffix = dataset_name.rsplit("-", 1)[-1].strip().lower()
    return suffix if 2 <= len(suffix) <= 3 and suffix.isalpha() else None


def _language_code_from_text(value: str) -> str | None:
    code = value.strip().lower()
    return code if 2 <= len(code) <= 3 and code.isalpha() else None


def _has_task_length_filters(
    *,
    query_min_chars: float | None,
    query_max_chars: float | None,
    document_min_chars: float | None,
    document_max_chars: float | None,
) -> bool:
    return any(
        value is not None
        for value in (
            query_min_chars,
            query_max_chars,
            document_min_chars,
            document_max_chars,
        )
    )


def _has_parameter_filters(
    *,
    active_params_min_millions: float | None,
    active_params_max_millions: float | None,
    total_params_min_millions: float | None,
    total_params_max_millions: float | None,
) -> bool:
    return any(
        value is not None
        for value in (
            active_params_min_millions,
            active_params_max_millions,
            total_params_min_millions,
            total_params_max_millions,
        )
    )


def _filter_rows_by_parameters(
    rows: list[TaskScore],
    *,
    active_params_min_millions: float | None,
    active_params_max_millions: float | None,
    total_params_min_millions: float | None,
    total_params_max_millions: float | None,
) -> list[TaskScore]:
    return [
        row
        for row in rows
        if _parameter_value_matches(
            row.active_parameters,
            minimum_millions=active_params_min_millions,
            maximum_millions=active_params_max_millions,
        )
        and _parameter_value_matches(
            row.total_parameters,
            minimum_millions=total_params_min_millions,
            maximum_millions=total_params_max_millions,
        )
    ]


def _parameter_value_matches(
    value: int | None,
    *,
    minimum_millions: float | None,
    maximum_millions: float | None,
) -> bool:
    if minimum_millions is None and maximum_millions is None:
        return True
    if value is None:
        return False
    value_millions = value / 1_000_000
    if minimum_millions is not None and value_millions < minimum_millions:
        return False
    return maximum_millions is None or value_millions <= maximum_millions


def _filter_rows_by_task_lengths(
    rows: list[TaskScore],
    *,
    query_min_chars: float | None,
    query_max_chars: float | None,
    document_min_chars: float | None,
    document_max_chars: float | None,
) -> list[TaskScore]:
    return [
        row
        for row in rows
        if _length_value_matches(
            row.query_mean_chars, minimum=query_min_chars, maximum=query_max_chars
        )
        and _length_value_matches(
            row.document_mean_chars,
            minimum=document_min_chars,
            maximum=document_max_chars,
        )
    ]


def _length_value_matches(
    value: float | None, *, minimum: float | None, maximum: float | None
) -> bool:
    if minimum is None and maximum is None:
        return True
    if value is None:
        return False
    if minimum is not None and value < minimum:
        return False
    return maximum is None or value <= maximum


def _language_label(language: str) -> str:
    return language.upper() if 2 <= len(language) <= 3 else language


def _score_groups_for_view(
    config: ViewerConfig, view_name: str
) -> list[ScoreGroupConfig]:
    benchmark = config.benchmark_for_view(view_name)
    return benchmark.resolved_score_groups if benchmark is not None else []


def _language_filter_mode_for_view(
    config: ViewerConfig, view_name: str
) -> LanguageFilterMode:
    benchmark = config.benchmark_for_view(view_name)
    return benchmark.language_filter_mode if benchmark is not None else "languages"


def _language_page_languages_for_view(
    config: ViewerConfig, view_name: str
) -> tuple[str, ...]:
    benchmark = config.benchmark_for_view(view_name)
    if benchmark is None:
        return ()
    return tuple(benchmark.language_page_languages)


def _language_filter_policy_for_view(
    config: ViewerConfig, view_name: str, *, overall: OverallConfig | None = None
) -> LanguageFilterPolicy:
    if overall is None:
        overall = config.overall_for_view(view_name)
    if overall is not None:
        benchmark_names = set(overall.benchmark_names)
        modes_by_benchmark: dict[str, LanguageFilterMode] = {
            benchmark.name: benchmark.language_filter_mode
            for benchmark in config.benchmarks
            if benchmark.name in benchmark_names
            and benchmark.language_filter_mode != "languages"
        }
        allowed_languages_by_benchmark = {
            benchmark.name: tuple(benchmark.language_page_languages)
            for benchmark in config.benchmarks
            if benchmark.name in benchmark_names and benchmark.language_page_languages
        }
        return LanguageFilterPolicy(
            modes_by_benchmark=modes_by_benchmark,
            allowed_languages_by_benchmark=allowed_languages_by_benchmark,
        )
    return LanguageFilterPolicy(
        default_mode=_language_filter_mode_for_view(config, view_name),
        default_allowed_languages=_language_page_languages_for_view(config, view_name),
    )


def _language_filter_policy_supports_precomputed(policy: LanguageFilterPolicy) -> bool:
    return (
        policy.default_mode == "languages"
        and not policy.default_allowed_languages
        and not policy.modes_by_benchmark
        and not policy.allowed_languages_by_benchmark
    )


def _available_view_names(config: ViewerConfig) -> list[str]:
    return [*config.view_names, CLEAR_SCOPE_NAME]


def _overall_metric_score_group(
    overall: OverallConfig, *, score_aggregation: ScoreAggregation
) -> ScoreGroupConfig | None:
    if not _overall_uses_grouped_components(
        overall, score_aggregation=score_aggregation
    ):
        return None
    return ScoreGroupConfig(
        name="benchmark_macro", label="Benchmark Macro", group_by="benchmark"
    )


def _custom_single_component_metric_score_group(
    config: ViewerConfig, overall: OverallConfig
) -> ScoreGroupConfig | None:
    if overall.name != CUSTOM_SCOPE_NAME or len(overall.benchmark_components) != 1:
        return None
    component = overall.benchmark_components[0]
    if component.group_by is None:
        return None
    benchmark = config.benchmark_for_view(component.name)
    if benchmark is not None:
        for group in benchmark.resolved_score_groups:
            if group.group_by == component.group_by:
                return group
    return ScoreGroupConfig(
        name=f"{component.name}_{component.group_by}",
        label=component.group_by.replace("_", " ").title(),
        group_by=component.group_by,
    )


def _overall_uses_grouped_components(
    overall: OverallConfig, *, score_aggregation: ScoreAggregation
) -> bool:
    return score_aggregation == "macro"


def _record_display_model_names(
    records: list[TaskResultRow], *, include_variant_details: bool
) -> list[str]:
    if not include_variant_details:
        return [record.model_name for record in records]

    base_names = [
        _display_model_name(
            record.model_name,
            embedding_dim=record.embedding_dim,
            quantization=record.quantization,
        )
        for record in records
    ]
    variant_names_by_display: dict[str, set[str]] = defaultdict(set)
    for record, base_name in zip(records, base_names, strict=True):
        variant_names_by_display[base_name].add(record.embedding_variant_name or "base")

    return [
        (
            _display_model_name(
                record.model_name,
                embedding_dim=record.embedding_dim,
                quantization=record.quantization,
                variant_name=record.embedding_variant_name or "base",
            )
            if len(variant_names_by_display[base_name]) > 1
            else base_name
        )
        for record, base_name in zip(records, base_names, strict=True)
    ]


def _display_model_name(
    model_name: str,
    *,
    embedding_dim: int | None,
    quantization: str | None,
    variant_name: str | None = None,
) -> str:
    details = []
    if embedding_dim is not None:
        details.append(f"{embedding_dim} dims")
    if quantization:
        details.append(quantization)
    if variant_name:
        details.append(variant_name)
    if not details:
        return model_name
    return f"{model_name} ({', '.join(details)})"


def _select_score_group(
    groups: list[ScoreGroupConfig],
    score_group_name: str | None,
) -> ScoreGroupConfig | None:
    if not groups:
        return None
    for group in groups:
        if group.name == score_group_name:
            return group
    return groups[0]


def _metric_columns(
    rows: list[TaskScore], score_group: ScoreGroupConfig | None
) -> list[str]:
    if score_group is None:
        return []
    return sorted({_score_group_key(row, score_group.group_by) for row in rows})


def _metric_column_doc_keys(
    *,
    rows: list[TaskScore],
    score_group: ScoreGroupConfig | None,
    metric_columns: list[str],
) -> dict[str, str]:
    if score_group is None or not metric_columns:
        return {}
    metric_column_set = set(metric_columns)
    candidates_by_column: dict[str, set[str]] = defaultdict(set)
    for row in rows:
        column = _score_group_key(row, score_group.group_by)
        if column not in metric_column_set:
            continue
        candidates_by_column[column].add(
            f"{row.benchmark}::{row.dataset_name}::{row.task_name}"
        )
    return {
        column: next(iter(candidates))
        for column, candidates in candidates_by_column.items()
        if len(candidates) == 1
    }


def _filter_metric_columns(
    rows: list[TaskScore],
    score_group: ScoreGroupConfig | None,
    columns: list[str],
    task_filter: str,
) -> list[str]:
    terms = active_filter_terms(task_filter, min_length=2)
    if not terms or score_group is None:
        return columns
    labels_by_column: dict[str, set[str]] = defaultdict(set)
    for row in rows:
        column = _score_group_key(row, score_group.group_by)
        labels_by_column[column].update(
            {
                column,
                row.task_name,
                row.task_key,
                row.dataset_name,
                row.dataset_id,
                row.benchmark,
            }
        )
    return [
        column
        for column in columns
        if any(
            text_matches_filter_terms(label, terms)
            for label in labels_by_column.get(column, {column})
        )
    ]


def _metric_column_label_overrides(
    *,
    rows: list[TaskScore],
    score_group: ScoreGroupConfig | None,
    metric_columns: list[str],
    config: ViewerConfig,
) -> dict[str, str]:
    if score_group is None or not metric_columns:
        return {}
    metric_column_set = set(metric_columns)
    labels_by_column: dict[str, set[str]] = defaultdict(set)
    for row in rows:
        column = _score_group_key(row, score_group.group_by)
        if column not in metric_column_set:
            continue
        benchmark_config = config.benchmark_for_view(row.benchmark)
        if benchmark_config is None or not benchmark_config.task_labels:
            continue
        label = (
            benchmark_config.task_labels.get(column)
            or benchmark_config.task_labels.get(row.task_name)
            or benchmark_config.task_labels.get(row.split_name)
            or benchmark_config.task_labels.get(row.task_key)
        )
        if label:
            labels_by_column[column].add(label)
    return {
        column: next(iter(labels))
        for column, labels in labels_by_column.items()
        if len(labels) == 1
    }


def _metric_values(
    rows: list[TaskScore],
    *,
    score_group: ScoreGroupConfig | None,
    metric_columns: list[str],
) -> dict[str, float]:
    if score_group is None:
        return {}
    values_by_column: dict[str, list[float]] = defaultdict(list)
    for row in rows:
        values_by_column[_score_group_key(row, score_group.group_by)].append(
            row.score * 100.0
        )
    return {
        column: _mean(values_by_column[column])
        for column in metric_columns
        if values_by_column[column]
    }


def _metric_z_values_by_model(
    rows: list[TaskScore],
    *,
    score_group: ScoreGroupConfig | None,
    metric_columns: list[str],
) -> dict[str, dict[str, float]]:
    if score_group is None:
        return {}
    model_column_values = _mean_metric_values_by_model(rows, score_group=score_group)
    base_model_column_values = _mean_metric_values_by_model(
        [row for row in rows if row.embedding_variant_name is None],
        score_group=score_group,
    )
    stats_by_column: dict[str, tuple[float, float]] = {}
    for column in metric_columns:
        values = [
            columns[column]
            for columns in base_model_column_values.values()
            if column in columns
        ]
        stddev = _population_stddev(values)
        if stddev is not None and stddev > 0.0:
            stats_by_column[column] = (_mean(values), stddev)
    return {
        model_name: {
            column: (value - mean) / stddev
            for column, value in columns.items()
            if column in stats_by_column
            for mean, stddev in [stats_by_column[column]]
        }
        for model_name, columns in model_column_values.items()
    }


def _metric_rank_values_by_model(
    rows: list[TaskScore],
    *,
    score_group: ScoreGroupConfig | None,
    metric_columns: list[str],
) -> dict[str, dict[str, float]]:
    if score_group is None:
        return {}
    metric_values_by_model = _mean_metric_values_by_model(rows, score_group=score_group)
    ranks_by_column: dict[str, dict[str, float]] = {}
    for column in metric_columns:
        ranks_by_column[column] = _average_rank_desc(
            (model_name, values[column])
            for model_name, values in metric_values_by_model.items()
            if column in values
        )
    ranks_by_model: dict[str, dict[str, float]] = defaultdict(dict)
    for column, ranks in ranks_by_column.items():
        for model_name, rank in ranks.items():
            ranks_by_model[model_name][column] = rank
    return ranks_by_model


def _aggregate_z_values_by_model(
    rows: list[TaskScore],
    *,
    is_overall: bool,
    overall_score_aggregation: ScoreAggregation,
) -> dict[str, dict[str, float]]:
    aggregate_values = _aggregate_values_by_model(
        rows,
        is_overall=is_overall,
        overall_score_aggregation=overall_score_aggregation,
    )
    base_aggregate_values = _aggregate_values_by_model(
        [row for row in rows if row.embedding_variant_name is None],
        is_overall=is_overall,
        overall_score_aggregation=overall_score_aggregation,
    )
    stats_by_column: dict[str, tuple[float, float]] = {}
    for column in ("mean_score", "macro_mean", "micro_mean"):
        values = [
            columns[column]
            for columns in base_aggregate_values.values()
            if column in columns
        ]
        stddev = _population_stddev(values)
        if stddev is not None and stddev > 0.0:
            stats_by_column[column] = (_mean(values), stddev)
    return {
        model_name: {
            column: (value - mean) / stddev
            for column, value in columns.items()
            if column in stats_by_column
            for mean, stddev in [stats_by_column[column]]
        }
        for model_name, columns in aggregate_values.items()
    }


def _aggregate_values_by_model(
    rows: list[TaskScore],
    *,
    is_overall: bool,
    overall_score_aggregation: ScoreAggregation,
) -> dict[str, dict[str, float]]:
    values_by_model: dict[str, dict[str, float]] = {}
    for model_name, model_rows in _group_by_model(rows).items():
        micro_mean = _mean(row.score * 100.0 for row in model_rows)
        benchmark_means = [
            _mean(row.score * 100.0 for row in benchmark_rows)
            for benchmark_rows in _group_by_benchmark(model_rows).values()
        ]
        macro_mean = _mean(benchmark_means)
        mean_score = (
            micro_mean
            if is_overall and overall_score_aggregation == "micro"
            else macro_mean
            if is_overall
            else micro_mean
        )
        values_by_model[model_name] = {"mean_score": mean_score}
        if is_overall:
            values_by_model[model_name]["macro_mean"] = macro_mean
            values_by_model[model_name]["micro_mean"] = micro_mean
    return values_by_model


def _group_by_model(rows: list[TaskScore]) -> dict[str, list[TaskScore]]:
    grouped: dict[str, list[TaskScore]] = defaultdict(list)
    for row in rows:
        grouped[row.model_name].append(row)
    return grouped


def _mean_metric_values_by_model(
    rows: list[TaskScore],
    *,
    score_group: ScoreGroupConfig,
) -> dict[str, dict[str, float]]:
    values_by_model_column: dict[tuple[str, str], list[float]] = defaultdict(list)
    for row in rows:
        values_by_model_column[
            (row.model_name, _score_group_key(row, score_group.group_by))
        ].append(row.score)
    values_by_model: dict[str, dict[str, float]] = defaultdict(dict)
    for (model_name, column), values in values_by_model_column.items():
        values_by_model[model_name][column] = _mean(values)
    return values_by_model


def _population_stddev(values: list[float]) -> float | None:
    if len(values) < 2:
        return None
    mean = _mean(values)
    return math.sqrt(sum((value - mean) ** 2 for value in values) / len(values))


def _score_group_key(row: TaskScore, group_by: str) -> str:
    if group_by == "task_key":
        return row.task_key
    if group_by == "dataset_name":
        return row.dataset_name
    if group_by == "dataset_id":
        return row.dataset_id
    if group_by == "split_name":
        return row.split_name
    if group_by == "benchmark":
        return row.benchmark
    return row.task_name


def _mean(values: Iterable[float]) -> float:
    vals = list(values)
    return sum(vals) / len(vals) if vals else 0.0


def _mean_optional(values: Iterable[float | None]) -> float | None:
    present_values = [value for value in values if value is not None]
    if not present_values:
        return None
    return sum(present_values) / len(present_values)
