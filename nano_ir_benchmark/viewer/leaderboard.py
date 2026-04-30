from __future__ import annotations

from collections import defaultdict
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Iterable, Literal

import duckdb
from pydantic import BaseModel, ConfigDict, Field

from nano_ir_benchmark.viewer.config import ScoreGroupConfig, ViewerConfig

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
}


class LeaderboardService:
    def __init__(self, *, duckdb_path: Path, config: ViewerConfig) -> None:
        self.duckdb_path = duckdb_path
        self.config = config

    def get_leaderboard(
        self,
        view_name: str,
        *,
        sort: str = "borda_rank",
        direction: SortDirection = "asc",
        score_group_name: str | None = None,
    ) -> LeaderboardResult:
        benchmarks = self.config.benchmarks_for_view(view_name)
        is_overall = view_name == self.config.overall.name
        score_groups = [] if is_overall else _score_groups_for_view(self.config, view_name)
        selected_score_group = _select_score_group(score_groups, score_group_name)
        rows = self._load_task_scores(benchmarks)
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
            score_groups=[ScoreGroup(name=group.name, label=group.display_label) for group in score_groups],
            selected_score_group=(
                ScoreGroup(name=selected_score_group.name, label=selected_score_group.display_label)
                if selected_score_group is not None
                else None
            ),
            metric_columns=metric_columns,
        )

    def _load_task_scores(self, benchmarks: list[str]) -> list[TaskScore]:
        if not self.duckdb_path.exists():
            return []
        placeholders = ", ".join("?" for _ in benchmarks)
        query = f"""
            SELECT
                model_name,
                benchmark,
                dataset_id,
                dataset_name,
                COALESCE(split_name, '') AS split_name,
                task_name,
                task_key,
                score,
                active_parameters,
                total_parameters,
                max_seq_length
            FROM task_results
            WHERE benchmark IN ({placeholders})
              AND score IS NOT NULL
        """
        con = duckdb.connect(str(self.duckdb_path), read_only=True)
        try:
            result = con.execute(query, benchmarks).fetchall()
        finally:
            con.close()
        return [
            TaskScore(
                model_name=str(row[0]),
                benchmark=str(row[1]),
                dataset_id=str(row[2]),
                dataset_name=str(row[3]),
                split_name=str(row[4]),
                task_name=str(row[5]),
                task_key=str(row[6]),
                score=float(row[7]),
                active_parameters=_int_or_none(row[8]),
                total_parameters=_int_or_none(row[9]),
                max_seq_length=_int_or_none(row[10]),
            )
            for row in result
        ]


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


def _score_groups_for_view(config: ViewerConfig, view_name: str) -> list[ScoreGroupConfig]:
    benchmark = config.benchmark_for_view(view_name)
    return benchmark.resolved_score_groups if benchmark is not None else []


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


def _int_or_none(value: object) -> int | None:
    return int(value) if isinstance(value, int | float) else None
