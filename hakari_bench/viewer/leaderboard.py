from __future__ import annotations

from collections import defaultdict
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Iterable, Literal

from pydantic import BaseModel, ConfigDict, Field

from hakari_bench.viewer.config import OverallConfig, ScoreGroupConfig, ViewerConfig
from hakari_bench.viewer.data import TaskResultRecord, TaskResultsRepository

SortDirection = Literal["asc", "desc"]


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
    embedding_variant_name: str | None = None
    embedding_dim: int | None = None
    quantization: str | None = None


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
    embedding_dim: int | None = None
    quantization: str | None = None
    metric_values: dict[str, float] = Field(default_factory=dict)


class ScoreGroup(BaseModel):
    model_config = ConfigDict(frozen=True)

    name: str
    label: str


class LeaderboardResult(BaseModel):
    model_config = ConfigDict(frozen=True)

    view_name: str
    view_label: str
    is_overall: bool
    expected_tasks: int
    rows: list[LeaderboardRow]
    available_views: list[str]
    available_view_labels: dict[str, str]
    include_quantization_variants: bool = False
    include_truncate_variants: bool = False
    include_other_variants: bool = False
    score_groups: list[ScoreGroup]
    selected_score_group: ScoreGroup | None = None
    metric_columns: list[str]


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
}


class LeaderboardService:
    def __init__(self, *, duckdb_path: Path, config: ViewerConfig) -> None:
        self.config = config
        self.task_results_repository = TaskResultsRepository(duckdb_path)

    def get_leaderboard(
        self,
        view_name: str,
        *,
        sort: str = "borda_rank",
        direction: SortDirection = "asc",
        score_group_name: str | None = None,
        include_quantization_variants: bool = False,
        include_truncate_variants: bool = False,
        include_other_variants: bool = False,
    ) -> LeaderboardResult:
        overall = self.config.overall_for_view(view_name)
        benchmarks = self.config.benchmarks_for_view(view_name)
        is_overall = overall is not None
        score_groups = [] if is_overall else _score_groups_for_view(self.config, view_name)
        selected_score_group = _select_score_group(score_groups, score_group_name)
        rows = self._load_task_scores(
            benchmarks,
            include_quantization_variants=include_quantization_variants,
            include_truncate_variants=include_truncate_variants,
            include_other_variants=include_other_variants,
        )
        rows = _exclude_configured_tasks(rows, self.config)
        if overall is not None:
            rows = _aggregate_overall_scores(rows, overall)
        metric_columns = _metric_columns(rows, selected_score_group) if selected_score_group is not None else []
        leaderboard_rows = compute_leaderboard_rows(
            rows,
            is_overall=is_overall,
            score_group=selected_score_group,
            metric_columns=metric_columns,
        )
        return LeaderboardResult(
            view_name=view_name,
            view_label=self.config.label_for_view(view_name),
            is_overall=is_overall,
            expected_tasks=len({row.task_key for row in rows}),
            rows=sort_rows(leaderboard_rows, sort=sort, direction=direction),
            available_views=self.config.view_names,
            available_view_labels={view: self.config.label_for_view(view) for view in self.config.view_names},
            include_quantization_variants=include_quantization_variants,
            include_truncate_variants=include_truncate_variants,
            include_other_variants=include_other_variants,
            score_groups=[ScoreGroup(name=group.name, label=group.display_label) for group in score_groups],
            selected_score_group=(
                ScoreGroup(name=selected_score_group.name, label=selected_score_group.display_label)
                if selected_score_group is not None
                else None
            ),
            metric_columns=metric_columns,
        )

    def _load_task_scores(
        self,
        benchmarks: list[str],
        *,
        include_quantization_variants: bool,
        include_truncate_variants: bool,
        include_other_variants: bool,
    ) -> list[TaskScore]:
        task_scores: list[TaskScore] = []
        include_any_variants = include_quantization_variants or include_truncate_variants or include_other_variants
        records = self.task_results_repository.fetch_task_results(
            benchmarks=benchmarks,
            include_embedding_variants=include_any_variants,
        )
        filtered_records = [
            record
            for record in records
            if _include_variant_row(
                embedding_variant_name=record.embedding_variant_name,
                quantization=record.quantization,
                include_quantization_variants=include_quantization_variants,
                include_truncate_variants=include_truncate_variants,
                include_other_variants=include_other_variants,
            )
        ]
        model_names = _record_display_model_names(filtered_records, include_variant_details=include_any_variants)
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
                    active_parameters=record.active_parameters,
                    total_parameters=record.total_parameters,
                    max_seq_length=record.max_seq_length,
                    embedding_variant_name=record.embedding_variant_name,
                    embedding_dim=record.embedding_dim,
                    quantization=record.quantization,
                )
            )
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
                embedding_dim=first.embedding_dim,
                quantization=first.quantization,
                metric_values=metric_values,
            )
        )

    borda_rank_by_model = _rank_desc((row.model_name, row.borda_score) for row in leaderboard_rows)
    mean_rank_by_model = _rank_desc((row.model_name, row.mean_score) for row in leaderboard_rows)
    return [
        row.model_copy(update={"borda_rank": borda_rank_by_model[row.model_name], "mean_rank": mean_rank_by_model[row.model_name]})
        for row in leaderboard_rows
    ]


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
                active_parameters=first.active_parameters,
                total_parameters=first.total_parameters,
                max_seq_length=first.max_seq_length,
                embedding_variant_name=first.embedding_variant_name,
                embedding_dim=first.embedding_dim,
                quantization=first.quantization,
            )
        )
    return aggregated


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


def _score_groups_for_view(config: ViewerConfig, view_name: str) -> list[ScoreGroupConfig]:
    benchmark = config.benchmark_for_view(view_name)
    return benchmark.resolved_score_groups if benchmark is not None else []


def _record_display_model_names(records: list[TaskResultRecord], *, include_variant_details: bool) -> list[str]:
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


def _include_variant_row(
    *,
    embedding_variant_name: str | None,
    quantization: str | None,
    include_quantization_variants: bool,
    include_truncate_variants: bool,
    include_other_variants: bool,
) -> bool:
    if embedding_variant_name is None:
        return True
    normalized_name = embedding_variant_name.lower()
    is_quantization = quantization is not None or "quantize" in normalized_name
    is_truncate = "truncate" in normalized_name
    is_other = not is_quantization and not is_truncate
    return (
        (include_quantization_variants and is_quantization)
        or (include_truncate_variants and is_truncate)
        or (include_other_variants and is_other)
    )


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
