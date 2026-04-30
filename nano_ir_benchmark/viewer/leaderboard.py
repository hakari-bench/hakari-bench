from __future__ import annotations

from collections import defaultdict
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Iterable, Literal

import duckdb
from pydantic import BaseModel, ConfigDict

from nano_ir_benchmark.viewer.config import ViewerConfig

SortDirection = Literal["asc", "desc"]


@dataclass(frozen=True)
class TaskScore:
    model_name: str
    benchmark: str
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


class LeaderboardResult(BaseModel):
    model_config = ConfigDict(frozen=True)

    view_name: str
    view_label: str
    is_overall: bool
    expected_tasks: int
    rows: list[LeaderboardRow]
    available_views: list[str]


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
    ) -> LeaderboardResult:
        benchmarks = self.config.benchmarks_for_view(view_name)
        rows = self._load_task_scores(benchmarks)
        leaderboard_rows = compute_leaderboard_rows(rows, is_overall=view_name == self.config.overall.name)
        return LeaderboardResult(
            view_name=view_name,
            view_label=self.config.label_for_view(view_name),
            is_overall=view_name == self.config.overall.name,
            expected_tasks=len({row.task_key for row in rows}),
            rows=sort_rows(leaderboard_rows, sort=sort, direction=direction),
            available_views=self.config.view_names,
        )

    def _load_task_scores(self, benchmarks: list[str]) -> list[TaskScore]:
        if not self.duckdb_path.exists():
            return []
        placeholders = ", ".join("?" for _ in benchmarks)
        query = f"""
            SELECT
                model_name,
                benchmark,
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
                task_key=str(row[2]),
                score=float(row[3]),
                active_parameters=_int_or_none(row[4]),
                total_parameters=_int_or_none(row[5]),
                max_seq_length=_int_or_none(row[6]),
            )
            for row in result
        ]


def compute_leaderboard_rows(rows: list[TaskScore], *, is_overall: bool) -> list[LeaderboardRow]:
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
            )
        )

    borda_rank_by_model = _rank_desc((row.model_name, row.borda_score) for row in leaderboard_rows)
    mean_rank_by_model = _rank_desc((row.model_name, row.mean_score) for row in leaderboard_rows)
    return [
        row.model_copy(update={"borda_rank": borda_rank_by_model[row.model_name], "mean_rank": mean_rank_by_model[row.model_name]})
        for row in leaderboard_rows
    ]


def sort_rows(rows: list[LeaderboardRow], *, sort: str, direction: SortDirection) -> list[LeaderboardRow]:
    sort_key = sort if sort in SORT_COLUMNS else "borda_rank"
    reverse = direction == "desc"

    def key(row: LeaderboardRow) -> tuple[int, Any, float, str]:
        value = getattr(row, sort_key)
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
        average_rank = (index + 1 + end) / 2.0
        for model_name, _ in sorted_items[index:end]:
            ranks[model_name] = average_rank
        index = end
    return ranks


def _group_by_benchmark(rows: list[TaskScore]) -> dict[str, list[TaskScore]]:
    grouped: dict[str, list[TaskScore]] = defaultdict(list)
    for row in rows:
        grouped[row.benchmark].append(row)
    return grouped


def _mean(values: Iterable[float]) -> float:
    vals = list(values)
    return sum(vals) / len(vals) if vals else 0.0


def _int_or_none(value: object) -> int | None:
    return int(value) if isinstance(value, int | float) else None
