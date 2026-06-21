from __future__ import annotations

from pathlib import Path
from typing import Any, Literal

import yaml
from pydantic import BaseModel, ConfigDict, Field


ScoreGroupKey = Literal["task_key", "dataset_name", "dataset_id", "split_name", "benchmark", "task_name"]
LanguageFilterMode = Literal["languages", "primary_language"]
ScoreAggregation = Literal["macro", "micro"]
CUSTOM_SCOPE_NAME = "Custom"
CLEAR_SCOPE_NAME = "Clear"
BENCHMARK_SELECTION_SEPARATOR = ":"


class ScoreGroupConfig(BaseModel):
    model_config = ConfigDict(frozen=True, extra="forbid", strict=True)

    name: str
    label: str | None = None
    group_by: ScoreGroupKey = "task_name"

    @property
    def display_label(self) -> str:
        return self.label or self.name


class BenchmarkConfig(BaseModel):
    model_config = ConfigDict(frozen=True, extra="forbid", strict=True)

    name: str
    label: str | None = None
    matches: list[str] = Field(default_factory=list)
    include_in_overall: bool = True
    excluded_tasks: list[str] = Field(default_factory=list)
    score_groups: list[ScoreGroupConfig] = Field(default_factory=list)
    language_filter_mode: LanguageFilterMode = "languages"
    language_page_languages: list[str] = Field(default_factory=list)
    task_labels: dict[str, str] = Field(default_factory=dict)

    @property
    def display_label(self) -> str:
        return self.label or self.name

    @property
    def match_patterns(self) -> list[str]:
        return self.matches or [self.name]

    @property
    def resolved_score_groups(self) -> list[ScoreGroupConfig]:
        if self.score_groups:
            return self.score_groups
        return [ScoreGroupConfig(name="task", label="Tasks", group_by="task_name")]


class OverallBenchmarkConfig(BaseModel):
    model_config = ConfigDict(frozen=True, extra="forbid", strict=True)

    name: str
    group_by: ScoreGroupKey | None = None


class OverallConfig(BaseModel):
    model_config = ConfigDict(frozen=True, extra="forbid", strict=True)

    name: str = "Overall"
    label: str = "Overall"
    benchmarks: list[str | OverallBenchmarkConfig] = Field(default_factory=list)

    @property
    def benchmark_components(self) -> list[OverallBenchmarkConfig]:
        return [
            OverallBenchmarkConfig(name=component) if isinstance(component, str) else component
            for component in self.benchmarks
        ]

    @property
    def benchmark_names(self) -> list[str]:
        return [component.name for component in self.benchmark_components]


class ViewerConfig(BaseModel):
    model_config = ConfigDict(frozen=True, extra="forbid", strict=True)

    benchmarks: list[BenchmarkConfig]
    overalls: list[OverallConfig]

    @property
    def overall(self) -> OverallConfig:
        return self.overalls[0]

    @property
    def view_names(self) -> list[str]:
        return [*(overall.name for overall in self.overalls), *(benchmark.name for benchmark in self.benchmarks)]

    @property
    def benchmark_names(self) -> list[str]:
        return [benchmark.name for benchmark in self.benchmarks]

    def benchmarks_for_view(self, view_name: str) -> list[str]:
        if view_name == CLEAR_SCOPE_NAME:
            return []
        overall = self.overall_for_view(view_name)
        if overall is not None:
            return overall.benchmark_names
        if any(benchmark.name == view_name for benchmark in self.benchmarks):
            return [view_name]
        raise ValueError(f"Unknown viewer benchmark: {view_name}")

    def overall_for_view(self, view_name: str) -> OverallConfig | None:
        for overall in self.overalls:
            if overall.name == view_name:
                return overall
        return None

    def benchmark_for_view(self, view_name: str) -> BenchmarkConfig | None:
        for benchmark in self.benchmarks:
            if benchmark.name == view_name:
                return benchmark
        return None

    def label_for_view(self, view_name: str) -> str:
        if view_name in {CUSTOM_SCOPE_NAME, CLEAR_SCOPE_NAME}:
            return view_name
        overall = self.overall_for_view(view_name)
        if overall is not None:
            return overall.label
        for benchmark in self.benchmarks:
            if benchmark.name == view_name:
                return benchmark.display_label
        return view_name

    def overall_for_selected_benchmarks(
        self, *, name: str, label: str, benchmark_names: list[str]
    ) -> OverallConfig:
        return self.overall_for_selected_benchmark_keys(name=name, label=label, selection_keys=benchmark_names)

    def overall_for_selected_benchmark_keys(
        self, *, name: str, label: str, selection_keys: list[str]
    ) -> OverallConfig:
        component_by_benchmark: dict[str, OverallBenchmarkConfig] = {}
        for overall in self.overalls:
            for component in overall.benchmark_components:
                if component.name not in component_by_benchmark or component.group_by is not None:
                    component_by_benchmark[component.name] = component
        components: list[str | OverallBenchmarkConfig] = [
            self.component_for_selection_key(selection_key)
            or component_by_benchmark.get(benchmark_name_from_selection_key(selection_key), OverallBenchmarkConfig(name=selection_key))
            for selection_key in selection_keys
        ]
        return OverallConfig(name=name, label=label, benchmarks=components)

    def component_for_selection_key(self, selection_key: str) -> OverallBenchmarkConfig | None:
        benchmark_name, group_name = split_benchmark_selection_key(selection_key)
        benchmark = self.benchmark_for_view(benchmark_name)
        if benchmark is None:
            return None
        if group_name is None:
            if benchmark.name == "MNanoBEIR":
                default_group = benchmark.resolved_score_groups[0]
                return OverallBenchmarkConfig(name=benchmark.name, group_by=default_group.group_by)
            return OverallBenchmarkConfig(name=benchmark.name)
        for group in benchmark.resolved_score_groups:
            if group.name == group_name:
                return OverallBenchmarkConfig(name=benchmark.name, group_by=group.group_by)
        return None

    def selection_key_for_component(self, component: OverallBenchmarkConfig) -> str:
        benchmark = self.benchmark_for_view(component.name)
        if benchmark is None:
            return component.name
        if benchmark.name != "MNanoBEIR":
            return benchmark.name
        for group in benchmark.resolved_score_groups:
            if group.group_by == (component.group_by or group.group_by):
                return benchmark_selection_key(benchmark.name, group.name)
        return benchmark_selection_key(benchmark.name, benchmark.resolved_score_groups[0].name)

    def selection_keys_for_overall(self, overall: OverallConfig) -> list[str]:
        return [self.selection_key_for_component(component) for component in overall.benchmark_components]


def load_viewer_config(config_dir: Path = Path("config/viewer")) -> ViewerConfig:
    benchmarks_path = config_dir / "benchmarks.yaml"
    overall_path = config_dir / "overall.yaml"
    benchmarks_payload = yaml.safe_load(benchmarks_path.read_text(encoding="utf-8"))
    overall_payload = yaml.safe_load(overall_path.read_text(encoding="utf-8"))

    benchmarks = [BenchmarkConfig.model_validate(item) for item in benchmarks_payload.get("benchmarks", [])]
    configured_names = {benchmark.name for benchmark in benchmarks}
    overalls = _load_overalls(overall_payload)
    missing = [
        name
        for overall in overalls
        for name in overall.benchmark_names
        if name not in configured_names
    ]
    if missing:
        raise ValueError(f"Unknown overall benchmark(s): {', '.join(missing)}")
    return ViewerConfig(benchmarks=benchmarks, overalls=overalls)


def _load_overalls(payload: dict[str, Any]) -> list[OverallConfig]:
    if "overalls" in payload:
        return [OverallConfig.model_validate(item) for item in payload["overalls"]]
    return [OverallConfig.model_validate(payload)]


def normalize_benchmark_selection_values(values: list[str] | None, viewer_config: ViewerConfig) -> list[str]:
    if values is None:
        return []
    selected: list[str] = []
    selected_index_by_benchmark: dict[str, int] = {}
    for value in values:
        if not value:
            continue
        component = viewer_config.component_for_selection_key(value)
        if component is None:
            continue
        selection_key = viewer_config.selection_key_for_component(component)
        benchmark_name = component.name
        existing_index = selected_index_by_benchmark.get(benchmark_name)
        if existing_index is not None:
            selected.pop(existing_index)
            selected_index_by_benchmark = {
                benchmark_name_from_selection_key(key): index
                for index, key in enumerate(selected)
            }
        selected_index_by_benchmark[benchmark_name] = len(selected)
        selected.append(selection_key)
    return selected


def benchmark_name_from_selection_key(selection_key: str) -> str:
    return split_benchmark_selection_key(selection_key)[0]


def benchmark_selection_key(benchmark_name: str, group_name: str) -> str:
    return f"{benchmark_name}{BENCHMARK_SELECTION_SEPARATOR}{group_name}"


def split_benchmark_selection_key(selection_key: str) -> tuple[str, str | None]:
    benchmark_name, separator, group_name = selection_key.partition(BENCHMARK_SELECTION_SEPARATOR)
    return benchmark_name, group_name if separator and group_name else None
