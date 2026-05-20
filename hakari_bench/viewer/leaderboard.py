from __future__ import annotations

from collections import defaultdict
from dataclasses import dataclass
from functools import lru_cache
import math
from pathlib import Path
from typing import Any, Iterable, Literal

import duckdb
from pydantic import BaseModel, ConfigDict, Field

from hakari_bench.viewer.config import LanguageFilterMode, OverallConfig, ScoreGroupConfig, ViewerConfig
from hakari_bench.viewer.data import TaskResultRow, TaskResultsRepository, _table_exists
from hakari_bench.viewer.observability import log_event, timed_operation
from hakari_bench.viewer.text_match import active_filter_terms, text_matches_filter_terms
from hakari_bench.viewer.variant_display import VariantDisplayFlags, include_variant_row

SortDirection = Literal["asc", "desc"]
ScoreTarget = Literal["all", "reranking"]


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


class LeaderboardRow(BaseModel):
    model_config = ConfigDict(frozen=True)

    borda_rank: float
    mean_rank: float
    model_name: str
    model_type: str | None = None
    borda_score: float
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
    metric_values: dict[str, float] = Field(default_factory=dict)
    metric_z_values: dict[str, float] = Field(default_factory=dict)
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
    rank_filtered: bool = False
    task_filter: str = ""
    score_groups: list[ScoreGroup]
    selected_score_group: ScoreGroup | None = None
    metric_columns: list[str]
    metric_column_labels: dict[str, str] = Field(default_factory=dict)
    available_languages: list[LanguageOption] = Field(default_factory=list)
    selected_languages: tuple[str, ...] = ()


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
    def __init__(self, *, duckdb_path: Path, config: ViewerConfig, use_precomputed: bool = True) -> None:
        self.config = config
        self.duckdb_path = duckdb_path
        self.use_precomputed = use_precomputed
        self.task_results_repository = TaskResultsRepository(duckdb_path)

    def get_leaderboard(
        self,
        view_name: str,
        *,
        sort: str = "borda_rank",
        direction: SortDirection = "asc",
        score_target: ScoreTarget = "all",
        score_group_name: str | None = None,
        include_quantization_variants: bool = False,
        include_truncate_variants: bool = False,
        include_rescore_variants: bool = False,
        include_other_variants: bool = False,
        language_filters: tuple[str, ...] = (),
        show_task_scores: bool = False,
        show_task_z_scores: bool = False,
        rank_filtered: bool = False,
        model_filter: str = "",
        task_filter: str = "",
        dim_filters: tuple[str, ...] = (),
        quant_filters: tuple[str, ...] = (),
        dtype_filters: tuple[str, ...] = (),
        attn_filters: tuple[str, ...] = (),
        prompt_filters: tuple[str, ...] = (),
        query_min_chars: float | None = None,
        query_max_chars: float | None = None,
        document_min_chars: float | None = None,
        document_max_chars: float | None = None,
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
            task_filter_terms = active_filter_terms(task_filter)
            ranking_model_filter_terms = model_filter_terms if rank_filtered else ()
            ranking_task_filter_terms = task_filter_terms if rank_filtered else ()
            ranking_dim_filters = dim_filters if rank_filtered else ()
            ranking_quant_filters = quant_filters if rank_filtered else ()
            ranking_dtype_filters = dtype_filters if rank_filtered else ()
            ranking_attn_filters = attn_filters if rank_filtered else ()
            ranking_prompt_filters = prompt_filters if rank_filtered else ()
            has_rank_facet_filters = _has_facet_filters(
                dim_filters=ranking_dim_filters,
                quant_filters=ranking_quant_filters,
                dtype_filters=ranking_dtype_filters,
                attn_filters=ranking_attn_filters,
                prompt_filters=ranking_prompt_filters,
            )
            overall = self.config.overall_for_view(view_name)
            benchmarks = self.config.benchmarks_for_view(view_name)
            is_overall = overall is not None
            request_timing["benchmark_count"] = len(benchmarks)
            score_groups = [] if is_overall else _score_groups_for_view(self.config, view_name)
            selected_score_group = _select_score_group(score_groups, score_group_name)
            include_flags = VariantDisplayFlags(
                quantization=include_quantization_variants,
                truncate=include_truncate_variants,
                rescore=include_rescore_variants,
                other=include_other_variants,
            )
            language_filter_mode = _language_filter_mode_for_view(self.config, view_name)
            has_length_filters = _has_task_length_filters(
                query_min_chars=query_min_chars,
                query_max_chars=query_max_chars,
                document_min_chars=document_min_chars,
                document_max_chars=document_max_chars,
            )
            if (
                self.use_precomputed
                and not language_filters
                and not show_task_scores
                and not show_task_z_scores
                and not ranking_model_filter_terms
                and not has_rank_facet_filters
                and not task_filter.strip()
                and not has_length_filters
                and language_filter_mode == "languages"
            ):
                precomputed = _load_precomputed_leaderboard_rows(
                    duckdb_path=self.duckdb_path,
                    view_name=view_name,
                    score_target=score_target,
                    variant_flags=include_flags,
                )
                if precomputed is not None:
                    rows, expected_tasks, available_languages = precomputed
                    sorted_rows = sort_rows(rows, sort=sort, direction=direction)
                    request_timing["task_score_count"] = None
                    request_timing["leaderboard_row_count"] = len(sorted_rows)
                    request_timing["precomputed"] = True
                    return LeaderboardResult(
                        view_name=view_name,
                        view_label=self.config.label_for_view(view_name),
                        is_overall=is_overall,
                        score_target=score_target,
                        expected_tasks=expected_tasks,
                        rows=sorted_rows,
                        available_views=self.config.view_names,
                        available_view_labels={view: self.config.label_for_view(view) for view in self.config.view_names},
                        include_quantization_variants=include_quantization_variants,
                        include_truncate_variants=include_truncate_variants,
                        include_rescore_variants=include_rescore_variants,
                        include_other_variants=include_other_variants,
                        show_task_scores=False,
                        show_task_z_scores=False,
                        task_filter="",
                        score_groups=[ScoreGroup(name=group.name, label=group.display_label) for group in score_groups],
                        selected_score_group=(
                            ScoreGroup(name=selected_score_group.name, label=selected_score_group.display_label)
                            if selected_score_group is not None
                            else None
                        ),
                        metric_columns=[],
                        available_languages=available_languages,
                        selected_languages=(),
                    )
            with timed_operation("viewer.leaderboard.phase", operation="load_task_scores", view=view_name) as phase_timing:
                rows = self._load_task_scores(
                    benchmarks,
                    score_target=score_target,
                    include_quantization_variants=include_quantization_variants,
                    include_truncate_variants=include_truncate_variants,
                    include_rescore_variants=include_rescore_variants,
                    include_other_variants=include_other_variants,
                )
                phase_timing["task_score_count"] = len(rows)
            rows = _exclude_configured_tasks(rows, self.config)
            if ranking_model_filter_terms:
                with timed_operation("viewer.leaderboard.phase", operation="filter_models", view=view_name) as phase_timing:
                    rows = _filter_rows_by_model_terms(rows, ranking_model_filter_terms)
                    phase_timing["task_score_count"] = len(rows)
                    phase_timing["term_count"] = len(ranking_model_filter_terms)
            if has_length_filters:
                with timed_operation("viewer.leaderboard.phase", operation="filter_task_lengths", view=view_name) as phase_timing:
                    rows = _filter_rows_by_task_lengths(
                        rows,
                        query_min_chars=query_min_chars,
                        query_max_chars=query_max_chars,
                        document_min_chars=document_min_chars,
                        document_max_chars=document_max_chars,
                    )
                    phase_timing["task_score_count"] = len(rows)
            if has_rank_facet_filters:
                with timed_operation("viewer.leaderboard.phase", operation="filter_facets", view=view_name) as phase_timing:
                    rows = _filter_rows_by_facets(
                        rows,
                        dim_filters=ranking_dim_filters,
                        quant_filters=ranking_quant_filters,
                        dtype_filters=ranking_dtype_filters,
                        attn_filters=ranking_attn_filters,
                        prompt_filters=ranking_prompt_filters,
                    )
                    phase_timing["task_score_count"] = len(rows)
            available_languages = _language_options(rows, mode=language_filter_mode)
            selected_languages = _selected_languages(language_filters, available_languages)
            if selected_languages:
                with timed_operation("viewer.leaderboard.phase", operation="filter_languages", view=view_name) as phase_timing:
                    rows = _filter_rows_by_languages(rows, selected_languages, mode=language_filter_mode)
                    phase_timing["task_score_count"] = len(rows)
                    phase_timing["language_count"] = len(selected_languages)
            if ranking_task_filter_terms:
                with timed_operation("viewer.leaderboard.phase", operation="filter_tasks", view=view_name) as phase_timing:
                    rows = _filter_rows_by_task_terms(rows, ranking_task_filter_terms)
                    phase_timing["task_score_count"] = len(rows)
                    phase_timing["term_count"] = len(ranking_task_filter_terms)
            metric_score_group = selected_score_group
            should_show_task_scores = show_task_scores or bool(ranking_task_filter_terms)
            if overall is not None and not ranking_task_filter_terms:
                with timed_operation("viewer.leaderboard.phase", operation="aggregate_overall", view=view_name) as phase_timing:
                    rows = _aggregate_overall_scores(rows, overall)
                    metric_score_group = _overall_metric_score_group(overall)
                    phase_timing["task_score_count"] = len(rows)
            elif selected_score_group is not None:
                with timed_operation("viewer.leaderboard.phase", operation="aggregate_score_group", view=view_name) as phase_timing:
                    rows = _aggregate_benchmark_score_group_scores(rows, selected_score_group)
                    phase_timing["task_score_count"] = len(rows)
            if should_show_task_scores and metric_score_group is None:
                metric_score_group = ScoreGroupConfig(name="task_scores", label="Task Scores", group_by="task_key")
            with timed_operation("viewer.leaderboard.phase", operation="metric_columns", view=view_name) as phase_timing:
                metric_columns = _metric_columns(rows, metric_score_group) if should_show_task_scores and metric_score_group is not None else []
                if not ranking_task_filter_terms:
                    metric_columns = _filter_metric_columns(rows, metric_score_group, metric_columns, task_filter)
                metric_column_labels = _metric_column_label_overrides(
                    rows=rows,
                    score_group=metric_score_group,
                    metric_columns=metric_columns,
                    config=self.config,
                )
                phase_timing["metric_column_count"] = len(metric_columns)
            with timed_operation("viewer.leaderboard.phase", operation="compute_rows", view=view_name) as phase_timing:
                leaderboard_rows = compute_leaderboard_rows(
                    rows,
                    is_overall=is_overall,
                    score_group=metric_score_group,
                    metric_columns=metric_columns,
                    show_task_z_scores=show_task_z_scores,
                    use_task_mean_for_overall=bool(ranking_task_filter_terms),
                )
                sort_key = "mean_score" if ranking_task_filter_terms and sort in {"macro_mean", "micro_mean"} else sort
                sorted_rows = sort_rows(leaderboard_rows, sort=sort_key, direction=direction)
                phase_timing["leaderboard_row_count"] = len(sorted_rows)
            request_timing["task_score_count"] = len(rows)
            request_timing["leaderboard_row_count"] = len(sorted_rows)
            return LeaderboardResult(
                view_name=view_name,
                view_label=self.config.label_for_view(view_name),
                is_overall=is_overall,
                score_target=score_target,
                expected_tasks=len({row.task_key for row in rows}),
                rows=sorted_rows,
                available_views=self.config.view_names,
                available_view_labels={view: self.config.label_for_view(view) for view in self.config.view_names},
                include_quantization_variants=include_quantization_variants,
                include_truncate_variants=include_truncate_variants,
                include_rescore_variants=include_rescore_variants,
                include_other_variants=include_other_variants,
                show_task_scores=should_show_task_scores,
                show_task_z_scores=show_task_z_scores,
                rank_filtered=rank_filtered,
                task_filter=task_filter.strip(),
                score_groups=[ScoreGroup(name=group.name, label=group.display_label) for group in score_groups],
                selected_score_group=(
                    ScoreGroup(name=selected_score_group.name, label=selected_score_group.display_label)
                    if selected_score_group is not None
                    else None
                ),
                metric_columns=metric_columns,
                metric_column_labels=metric_column_labels,
                available_languages=available_languages,
                selected_languages=selected_languages,
            )

    def _load_task_scores(
        self,
        benchmarks: list[str],
        *,
        score_target: ScoreTarget,
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
        duckdb_path, duckdb_mtime_ns, duckdb_size = _duckdb_cache_identity(self.duckdb_path)
        cache_before = _cached_task_scores.cache_info()
        task_scores = list(
            _cached_task_scores(
                duckdb_path,
                duckdb_mtime_ns,
                duckdb_size,
                tuple(benchmarks),
                score_target,
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
        return task_scores


def _load_task_scores_uncached(
    *,
    duckdb_path: Path,
    benchmarks: tuple[str, ...],
    score_target: ScoreTarget,
    include_any_variants: bool,
    variant_flags: VariantDisplayFlags,
) -> tuple[TaskScore, ...]:
    records = TaskResultsRepository(duckdb_path).fetch_task_result_rows(
        benchmarks=list(benchmarks),
        score_target=score_target,
        include_embedding_variants=include_any_variants,
        variant_display_flags=variant_flags,
    )
    task_scores = _task_scores_from_records(records, include_any_variants=include_any_variants, variant_flags=variant_flags)
    if score_target == "all":
        task_scores = _exclude_reranker_task_scores(task_scores)
    return tuple(task_scores)


@lru_cache(maxsize=64)
def _cached_task_scores(
    duckdb_path: str,
    duckdb_mtime_ns: int,
    duckdb_size: int,
    benchmarks: tuple[str, ...],
    score_target: ScoreTarget,
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
                LanguageOption(code=str(row[0]), label=str(row[1]), task_count=int(row[2]))
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
        rows = [row for row in rows if not _is_reranker_model(model_name=str(row[3]), model_type=None)]
    if not rows:
        return None
    expected_tasks = int(rows[0][0])
    return (
        [
            LeaderboardRow(
                borda_rank=float(row[1]),
                mean_rank=float(row[2]),
                model_name=str(row[3]),
                borda_score=float(row[4]),
                mean_score=float(row[5]),
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
        ],
        expected_tasks,
        language_options,
    )


def _duckdb_cache_identity(duckdb_path: Path) -> tuple[str, int, int]:
    resolved_path = duckdb_path.resolve()
    try:
        stat_result = resolved_path.stat()
    except FileNotFoundError:
        return str(resolved_path), 0, 0
    return str(resolved_path), stat_result.st_mtime_ns, stat_result.st_size


def _task_scores_from_records(
    records: list[TaskResultRow],
    *,
    include_any_variants: bool,
    variant_flags: VariantDisplayFlags,
) -> list[TaskScore]:
    task_scores: list[TaskScore] = []
    with timed_operation("viewer.leaderboard.phase", operation="filter_variant_records") as timing:
        filtered_records = [
            record
            for record in records
            if include_variant_row(
                embedding_variant_name=record.embedding_variant_name,
                quantization=record.quantization,
                flags=variant_flags,
            )
        ]
        timing["record_count"] = len(records)
        timing["filtered_record_count"] = len(filtered_records)
    with timed_operation("viewer.leaderboard.phase", operation="display_model_names") as timing:
        model_names = _record_display_model_names(filtered_records, include_variant_details=include_any_variants)
        timing["record_count"] = len(filtered_records)
    with timed_operation("viewer.leaderboard.phase", operation="build_task_scores") as timing:
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
                )
            )
        timing["task_score_count"] = len(task_scores)
    return task_scores


def _exclude_reranker_task_scores(rows: list[TaskScore]) -> list[TaskScore]:
    return [row for row in rows if not _is_reranker_model(model_name=row.source_model_name or row.model_name, model_type=row.model_type)]


def _is_reranker_model(*, model_name: str, model_type: str | None) -> bool:
    if model_type is not None:
        normalized_type = model_type.strip().casefold().replace("_", "-")
        if normalized_type in {"reranker", "cross-encoder", "crossencoder", "cross-encoder-reranker"}:
            return True
    normalized_name = model_name.casefold()
    return normalized_name.startswith("cross-encoder/") or "reranker" in normalized_name


def compute_leaderboard_rows(
    rows: list[TaskScore],
    *,
    is_overall: bool,
    score_group: ScoreGroupConfig | None = None,
    metric_columns: list[str] | None = None,
    show_task_z_scores: bool = False,
    use_task_mean_for_overall: bool = False,
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
        model_name for model_name, task_keys in task_keys_by_model.items() if task_keys == expected_tasks
    }
    complete_rows = [row for row in rows if row.model_name in complete_models]
    borda_scores = _borda_scores(complete_rows)
    metric_columns = metric_columns or []
    z_values_by_model = (
        _metric_z_values_by_model(complete_rows, score_group=score_group, metric_columns=metric_columns)
        if show_task_z_scores and metric_columns
        else {}
    )
    aggregate_z_values_by_model = _aggregate_z_values_by_model(complete_rows, is_overall=is_overall) if show_task_z_scores else {}

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
        mean_score = micro_mean if use_task_mean_for_overall else macro_mean if is_overall else micro_mean
        metric_values = _metric_values(model_rows, score_group=score_group, metric_columns=metric_columns)
        metric_z_values = z_values_by_model.get(model_name, {})
        aggregate_z_values = aggregate_z_values_by_model.get(model_name, {})
        leaderboard_rows.append(
            LeaderboardRow(
                borda_rank=0.0,
                mean_rank=0.0,
                model_name=model_name,
                model_type=first.model_type,
                borda_score=_mean(borda_scores[model_name]),
                mean_score=mean_score,
                mean_score_z=aggregate_z_values.get("mean_score"),
                macro_mean=macro_mean if is_overall else None,
                macro_mean_z=aggregate_z_values.get("macro_mean") if is_overall else None,
                micro_mean=micro_mean if is_overall else None,
                micro_mean_z=aggregate_z_values.get("micro_mean") if is_overall else None,
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
                metric_values=metric_values,
                metric_z_values=metric_z_values,
                metric_sort_values=metric_z_values if show_task_z_scores else metric_values,
            )
        )

    borda_rank_by_model = _rank_desc((row.model_name, row.borda_score) for row in leaderboard_rows)
    mean_rank_by_model = _rank_desc((row.model_name, row.mean_score) for row in leaderboard_rows)
    ranked_rows = [
        row.model_copy(update={"borda_rank": borda_rank_by_model[row.model_name], "mean_rank": mean_rank_by_model[row.model_name]})
        for row in leaderboard_rows
    ]
    return _with_base_score_delta_percent(ranked_rows)


def sort_rows(rows: list[LeaderboardRow], *, sort: str, direction: SortDirection) -> list[LeaderboardRow]:
    metric_key = sort.removeprefix("metric:") if sort.startswith("metric:") else None
    if metric_key is not None and not any(metric_key in row.metric_sort_values or metric_key in row.metric_values for row in rows):
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
            score = 100.0 if model_count <= 1 else 100.0 * (model_count - rank) / (model_count - 1)
            scores_by_model[row.model_name].append(score)
    return scores_by_model


def _rank_desc(items: Iterable[tuple[str, float]]) -> dict[str, float]:
    sorted_items = sorted(items, key=lambda item: (-item[1], item[0]))
    ranks: dict[str, float] = {}
    index = 0
    while index < len(sorted_items):
        end = index + 1
        while end < len(sorted_items) and sorted_items[end][1] == sorted_items[index][1]:
            end += 1
        rank = float(index + 1)
        for model_name, _ in sorted_items[index:end]:
            ranks[model_name] = rank
        index = end
    return ranks


def _group_by_benchmark(rows: list[TaskScore]) -> dict[str, list[TaskScore]]:
    grouped: dict[str, list[TaskScore]] = defaultdict(list)
    for row in rows:
        grouped[row.benchmark].append(row)
    return grouped


def _aggregate_overall_scores(rows: list[TaskScore], overall: OverallConfig) -> list[TaskScore]:
    component_by_benchmark = {component.name: component for component in overall.benchmark_components}
    if not any(component.group_by is not None for component in component_by_benchmark.values()):
        return rows

    expected_raw_tasks: dict[str, set[str]] = defaultdict(set)
    raw_tasks_by_model_benchmark: dict[tuple[str, str], set[str]] = defaultdict(set)
    for row in rows:
        expected_raw_tasks[row.benchmark].add(row.task_key)
        raw_tasks_by_model_benchmark[(row.model_name, row.benchmark)].add(row.task_key)

    aggregate_inputs: dict[tuple[str, str, str], list[TaskScore]] = defaultdict(list)
    for row in rows:
        component = component_by_benchmark[row.benchmark]
        model_benchmark = (row.model_name, row.benchmark)
        if raw_tasks_by_model_benchmark[model_benchmark] != expected_raw_tasks[row.benchmark]:
            continue
        aggregate_key = _score_group_key(row, component.group_by or "task_key")
        aggregate_inputs[(row.model_name, row.benchmark, aggregate_key)].append(row)

    aggregated: list[TaskScore] = []
    for (model_name, benchmark, aggregate_key), aggregate_rows in aggregate_inputs.items():
        first = aggregate_rows[0]
        aggregated.append(
            TaskScore(
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
                languages=tuple(sorted({language for row in aggregate_rows for language in row.languages})),
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
                document_mean_chars=_mean_optional(row.document_mean_chars for row in aggregate_rows),
            )
        )
    return aggregated


def _aggregate_benchmark_score_group_scores(rows: list[TaskScore], score_group: ScoreGroupConfig) -> list[TaskScore]:
    expected_raw_tasks: dict[str, set[str]] = defaultdict(set)
    raw_tasks_by_model_benchmark: dict[tuple[str, str], set[str]] = defaultdict(set)
    for row in rows:
        expected_raw_tasks[row.benchmark].add(row.task_key)
        raw_tasks_by_model_benchmark[(row.model_name, row.benchmark)].add(row.task_key)

    aggregate_inputs: dict[tuple[str, str, str], list[TaskScore]] = defaultdict(list)
    for row in rows:
        model_benchmark = (row.model_name, row.benchmark)
        if raw_tasks_by_model_benchmark[model_benchmark] != expected_raw_tasks[row.benchmark]:
            continue
        aggregate_key = _score_group_key(row, score_group.group_by)
        aggregate_inputs[(row.model_name, row.benchmark, aggregate_key)].append(row)

    aggregated: list[TaskScore] = []
    for (model_name, benchmark, aggregate_key), aggregate_rows in aggregate_inputs.items():
        first = aggregate_rows[0]
        aggregated.append(
            TaskScore(
                model_name=model_name,
                model_type=first.model_type,
                benchmark=benchmark,
                dataset_id=aggregate_key if score_group.group_by == "dataset_id" else first.dataset_id,
                dataset_name=aggregate_key if score_group.group_by == "dataset_name" else first.dataset_name,
                split_name=aggregate_key if score_group.group_by == "split_name" else first.split_name,
                task_name=aggregate_key if score_group.group_by == "task_name" else first.task_name,
                task_key=aggregate_key if score_group.group_by == "task_key" else f"{benchmark}::{score_group.group_by}::{aggregate_key}",
                score=_mean(row.score for row in aggregate_rows),
                language=first.language,
                languages=tuple(sorted({language for row in aggregate_rows for language in row.languages})),
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
                document_mean_chars=_mean_optional(row.document_mean_chars for row in aggregate_rows),
            )
        )
    return aggregated


def _with_base_score_delta_percent(rows: list[LeaderboardRow]) -> list[LeaderboardRow]:
    base_score_by_source_model = {
        row.source_model_name: row.mean_score
        for row in rows
        if row.source_model_name is not None and row.embedding_variant_name is None and row.mean_score != 0.0
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


def _exclude_configured_tasks(rows: list[TaskScore], config: ViewerConfig) -> list[TaskScore]:
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


def _language_options(rows: list[TaskScore], *, mode: LanguageFilterMode = "languages") -> list[LanguageOption]:
    task_keys_by_language: dict[str, set[str]] = defaultdict(set)
    for row in rows:
        for language in _language_codes_for_row(row, mode=mode):
            task_keys_by_language[language].add(row.task_key)
    return [
        LanguageOption(code=language, label=_language_label(language), task_count=len(task_keys))
        for language, task_keys in sorted(
            task_keys_by_language.items(),
            key=lambda item: (-len(item[1]), item[0]),
        )
    ]


def _selected_languages(language_filters: tuple[str, ...], options: list[LanguageOption]) -> tuple[str, ...]:
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
) -> list[TaskScore]:
    selected = set(selected_languages)
    return [row for row in rows if selected.intersection(_language_codes_for_row(row, mode=mode))]


def _filter_rows_by_model_terms(rows: list[TaskScore], terms: tuple[str, ...]) -> list[TaskScore]:
    if not terms:
        return rows
    return [row for row in rows if text_matches_filter_terms(row.model_name, terms)]


def _filter_rows_by_task_terms(rows: list[TaskScore], terms: tuple[str, ...]) -> list[TaskScore]:
    if not terms:
        return rows
    return [row for row in rows if _task_row_matches_filter_terms(row, terms)]


def _has_facet_filters(
    *,
    dim_filters: tuple[str, ...],
    quant_filters: tuple[str, ...],
    dtype_filters: tuple[str, ...],
    attn_filters: tuple[str, ...],
    prompt_filters: tuple[str, ...],
) -> bool:
    return any((dim_filters, quant_filters, dtype_filters, attn_filters, prompt_filters))


def _filter_rows_by_facets(
    rows: list[TaskScore],
    *,
    dim_filters: tuple[str, ...],
    quant_filters: tuple[str, ...],
    dtype_filters: tuple[str, ...],
    attn_filters: tuple[str, ...],
    prompt_filters: tuple[str, ...],
) -> list[TaskScore]:
    selected_dims = set(dim_filters)
    selected_quants = set(quant_filters)
    selected_dtypes = set(dtype_filters)
    selected_attn = set(attn_filters)
    selected_prompts = set(prompt_filters)
    return [
        row
        for row in rows
        if (not selected_dims or _dim_bucket(row.embedding_dim) in selected_dims)
        and (not selected_quants or _quant_bucket(row.quantization) in selected_quants)
        and (not selected_dtypes or _dtype_bucket(row.dtype) in selected_dtypes)
        and (not selected_attn or _attn_bucket(row.attn_implementation) in selected_attn)
        and (not selected_prompts or _prompt_bucket(row.prompt_summary) in selected_prompts)
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


def _language_codes_for_row(row: TaskScore, *, mode: LanguageFilterMode) -> tuple[str, ...]:
    if mode == "primary_language":
        language = _primary_language_for_row(row)
        return (language,) if language else ()
    return row.languages


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
    return any(value is not None for value in (query_min_chars, query_max_chars, document_min_chars, document_max_chars))


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
        if _length_value_matches(row.query_mean_chars, minimum=query_min_chars, maximum=query_max_chars)
        and _length_value_matches(row.document_mean_chars, minimum=document_min_chars, maximum=document_max_chars)
    ]


def _length_value_matches(value: float | None, *, minimum: float | None, maximum: float | None) -> bool:
    if minimum is None and maximum is None:
        return True
    if value is None:
        return False
    if minimum is not None and value < minimum:
        return False
    return maximum is None or value <= maximum


def _language_label(language: str) -> str:
    return language.upper() if 2 <= len(language) <= 3 else language


def _score_groups_for_view(config: ViewerConfig, view_name: str) -> list[ScoreGroupConfig]:
    benchmark = config.benchmark_for_view(view_name)
    return benchmark.resolved_score_groups if benchmark is not None else []


def _language_filter_mode_for_view(config: ViewerConfig, view_name: str) -> LanguageFilterMode:
    benchmark = config.benchmark_for_view(view_name)
    return benchmark.language_filter_mode if benchmark is not None else "languages"


def _overall_metric_score_group(overall: OverallConfig) -> ScoreGroupConfig | None:
    if not any(component.group_by is not None for component in overall.benchmark_components):
        return None
    return ScoreGroupConfig(name="grouped_tasks", label="Grouped Tasks", group_by="task_key")


def _record_display_model_names(records: list[TaskResultRow], *, include_variant_details: bool) -> list[str]:
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


def _metric_columns(rows: list[TaskScore], score_group: ScoreGroupConfig | None) -> list[str]:
    if score_group is None:
        return []
    return sorted({_score_group_key(row, score_group.group_by) for row in rows})


def _filter_metric_columns(
    rows: list[TaskScore],
    score_group: ScoreGroupConfig | None,
    columns: list[str],
    task_filter: str,
) -> list[str]:
    terms = active_filter_terms(task_filter)
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
        if any(text_matches_filter_terms(label, terms) for label in labels_by_column.get(column, {column}))
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
    return {column: next(iter(labels)) for column, labels in labels_by_column.items() if len(labels) == 1}


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
        values_by_column[_score_group_key(row, score_group.group_by)].append(row.score * 100.0)
    return {column: _mean(values_by_column[column]) for column in metric_columns if values_by_column[column]}


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
        values = [columns[column] for columns in base_model_column_values.values() if column in columns]
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


def _aggregate_z_values_by_model(rows: list[TaskScore], *, is_overall: bool) -> dict[str, dict[str, float]]:
    aggregate_values = _aggregate_values_by_model(rows, is_overall=is_overall)
    base_aggregate_values = _aggregate_values_by_model(
        [row for row in rows if row.embedding_variant_name is None],
        is_overall=is_overall,
    )
    stats_by_column: dict[str, tuple[float, float]] = {}
    for column in ("mean_score", "macro_mean", "micro_mean"):
        values = [columns[column] for columns in base_aggregate_values.values() if column in columns]
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


def _aggregate_values_by_model(rows: list[TaskScore], *, is_overall: bool) -> dict[str, dict[str, float]]:
    values_by_model: dict[str, dict[str, float]] = {}
    for model_name, model_rows in _group_by_model(rows).items():
        micro_mean = _mean(row.score * 100.0 for row in model_rows)
        benchmark_means = [
            _mean(row.score * 100.0 for row in benchmark_rows)
            for benchmark_rows in _group_by_benchmark(model_rows).values()
        ]
        macro_mean = _mean(benchmark_means)
        mean_score = macro_mean if is_overall else micro_mean
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
        values_by_model_column[(row.model_name, _score_group_key(row, score_group.group_by))].append(row.score)
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
