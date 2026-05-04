from __future__ import annotations

from importlib.resources import as_file, files
from pathlib import Path
from typing import Any

import yaml
from pydantic import BaseModel, ConfigDict, Field


class ScoreGroupConfig(BaseModel):
    model_config = ConfigDict(frozen=True)

    name: str
    label: str | None = None
    group_by: str = "task_name"

    @property
    def display_label(self) -> str:
        return self.label or self.name


class BenchmarkConfig(BaseModel):
    model_config = ConfigDict(frozen=True)

    name: str
    label: str | None = None
    include_in_overall: bool = True
    excluded_tasks: list[str] = Field(default_factory=list)
    score_groups: list[ScoreGroupConfig] = Field(default_factory=list)

    @property
    def display_label(self) -> str:
        return self.label or self.name

    @property
    def resolved_score_groups(self) -> list[ScoreGroupConfig]:
        if self.score_groups:
            return self.score_groups
        return [ScoreGroupConfig(name="task", label="Tasks", group_by="task_name")]


class OverallBenchmarkConfig(BaseModel):
    model_config = ConfigDict(frozen=True)

    name: str
    group_by: str | None = None


class OverallConfig(BaseModel):
    model_config = ConfigDict(frozen=True)

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
    model_config = ConfigDict(frozen=True)

    benchmarks: list[BenchmarkConfig]
    overalls: list[OverallConfig]

    @property
    def overall(self) -> OverallConfig:
        return self.overalls[0]

    @property
    def view_names(self) -> list[str]:
        return [*(overall.name for overall in self.overalls), *(benchmark.name for benchmark in self.benchmarks)]

    def benchmarks_for_view(self, view_name: str) -> list[str]:
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
        overall = self.overall_for_view(view_name)
        if overall is not None:
            return overall.label
        for benchmark in self.benchmarks:
            if benchmark.name == view_name:
                return benchmark.display_label
        return view_name


def load_viewer_config(config_dir: Path = Path("config/viewer")) -> ViewerConfig:
    if config_dir == Path("config/viewer") and not config_dir.exists():
        config_root = files("hakari_bench").joinpath("config", "viewer")
        with as_file(config_root) as root:
            return load_viewer_config(root)

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
