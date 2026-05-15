from __future__ import annotations

from collections import defaultdict
from dataclasses import dataclass
from functools import lru_cache
from pathlib import Path
from typing import Any, Iterable, Literal

import duckdb
from pydantic import BaseModel, ConfigDict, Field

from hakari_bench.viewer.config import OverallConfig, ScoreGroupConfig, ViewerConfig
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


class LeaderboardRow(BaseModel):
    model_config = ConfigDict(frozen=True)

    borda_rank: float
    mean_rank: float
    model_name: str
    borda_score: float
    mean_score: float
    macro_mean: float | None = None
    micro_mean: float | None = None
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
    task_filter: str = ""
    score_groups: list[ScoreGroup]
    selected_score_group: ScoreGroup | None = None
    metric_columns: list[str]
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
        task_filter: str = "",
    ) -> LeaderboardResult:
        with timed_operation(
            "viewer.leaderboard.request",
            view=view_name,
            sort=sort,
            direction=direction,
            score_target=score_target,
            show_task_scores=show_task_scores,
        ) as request_timing:
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
            if self.use_precomputed and not language_filters and not show_task_scores and not task_filter.strip():
                precomputed = _load_precomputed_leaderboard_rows(
                    duckdb_path=self.duckdb_path,
                    view_name=view_name,
                    score_target=score_target,
                    variant_flags=include_flags,
                )
                if precomputed is not None:
                    rows, expected_tasks = precomputed
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
                        task_filter="",
                        score_groups=[ScoreGroup(name=group.name, label=group.display_label) for group in score_groups],
                        selected_score_group=(
                            ScoreGroup(name=selected_score_group.name, label=selected_score_group.display_label)
                            if selected_score_group is not None
                            else None
                        ),
                        metric_columns=[],
                        available_languages=[],
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
            available_languages = _language_options(rows)
            selected_languages = _selected_languages(language_filters, available_languages)
            if selected_languages:
                with timed_operation("viewer.leaderboard.phase", operation="filter_languages", view=view_name) as phase_timing:
                    rows = _filter_rows_by_languages(rows, selected_languages)
                    phase_timing["task_score_count"] = len(rows)
                    phase_timing["language_count"] = len(selected_languages)
            metric_score_group = selected_score_group
            if overall is not None:
                with timed_operation("viewer.leaderboard.phase", operation="aggregate_overall", view=view_name) as phase_timing:
                    rows = _aggregate_overall_scores(rows, overall)
                    metric_score_group = _overall_metric_score_group(overall)
                    phase_timing["task_score_count"] = len(rows)
            if show_task_scores and metric_score_group is None:
                metric_score_group = ScoreGroupConfig(name="task_scores", label="Task Scores", group_by="task_key")
            with timed_operation("viewer.leaderboard.phase", operation="metric_columns", view=view_name) as phase_timing:
                metric_columns = _metric_columns(rows, metric_score_group) if show_task_scores and metric_score_group is not None else []
                metric_columns = _filter_metric_columns(rows, metric_score_group, metric_columns, task_filter)
                phase_timing["metric_column_count"] = len(metric_columns)
            with timed_operation("viewer.leaderboard.phase", operation="compute_rows", view=view_name) as phase_timing:
                leaderboard_rows = compute_leaderboard_rows(
                    rows,
                    is_overall=is_overall,
                    score_group=metric_score_group,
                    metric_columns=metric_columns,
                )
                sorted_rows = sort_rows(leaderboard_rows, sort=sort, direction=direction)
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
                show_task_scores=show_task_scores,
                task_filter=task_filter.strip(),
                score_groups=[ScoreGroup(name=group.name, label=group.display_label) for group in score_groups],
                selected_score_group=(
                    ScoreGroup(name=selected_score_group.name, label=selected_score_group.display_label)
                    if selected_score_group is not None
                    else None
                ),
                metric_columns=metric_columns,
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
    return tuple(_task_scores_from_records(records, include_any_variants=include_any_variants, variant_flags=variant_flags))


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
) -> tuple[list[LeaderboardRow], int] | None:
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
    finally:
        con.close()
    if not rows:
        return None
    expected_tasks = int(rows[0][0])
    return [
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
    ], expected_tasks


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
                )
            )
        timing["task_score_count"] = len(task_scores)
    return task_scores


def compute_leaderboard_rows(
    rows: list[TaskScore],
    *,
    is_overall: bool,
    score_group: ScoreGroupConfig | None = None,
    metric_columns: list[str] | None = None,
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
        mean_score = macro_mean if is_overall else micro_mean
        metric_values = _metric_values(model_rows, score_group=score_group, metric_columns=metric_columns or [])
        leaderboard_rows.append(
            LeaderboardRow(
                borda_rank=0.0,
                mean_rank=0.0,
                model_name=model_name,
                borda_score=_mean(borda_scores[model_name]),
                mean_score=mean_score,
                macro_mean=macro_mean if is_overall else None,
                micro_mean=micro_mean if is_overall else None,
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
    if metric_key is not None and not any(metric_key in row.metric_values for row in rows):
        metric_key = None
    sort_key = sort if sort in SORT_COLUMNS else "borda_rank"
    reverse = direction == "desc" and (metric_key is not None or sort in SORT_COLUMNS)

    def key(row: LeaderboardRow) -> tuple[int, Any, float, str]:
        value = row.metric_values.get(metric_key) if metric_key is not None else getattr(row, sort_key)
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


def _language_options(rows: list[TaskScore]) -> list[LanguageOption]:
    task_keys_by_language: dict[str, set[str]] = defaultdict(set)
    for row in rows:
        for language in row.languages:
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


def _filter_rows_by_languages(rows: list[TaskScore], selected_languages: tuple[str, ...]) -> list[TaskScore]:
    selected = set(selected_languages)
    return [row for row in rows if selected.intersection(row.languages)]


def _language_label(language: str) -> str:
    return language.upper() if 2 <= len(language) <= 3 else language


def _score_groups_for_view(config: ViewerConfig, view_name: str) -> list[ScoreGroupConfig]:
    benchmark = config.benchmark_for_view(view_name)
    return benchmark.resolved_score_groups if benchmark is not None else []


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
