from __future__ import annotations

from pathlib import Path

import yaml
from pydantic import BaseModel, ConfigDict, Field


class BenchmarkConfig(BaseModel):
    model_config = ConfigDict(frozen=True)

    name: str
    label: str | None = None
    include_in_overall: bool = True

    @property
    def display_label(self) -> str:
        return self.label or self.name


class OverallConfig(BaseModel):
    model_config = ConfigDict(frozen=True)

    name: str = "Overall"
    label: str = "Overall"
    benchmarks: list[str] = Field(default_factory=list)


class ViewerConfig(BaseModel):
    model_config = ConfigDict(frozen=True)

    benchmarks: list[BenchmarkConfig]
    overall: OverallConfig

    @property
    def view_names(self) -> list[str]:
        return [self.overall.name, *(benchmark.name for benchmark in self.benchmarks)]

    def benchmarks_for_view(self, view_name: str) -> list[str]:
        if view_name == self.overall.name:
            return self.overall.benchmarks
        if any(benchmark.name == view_name for benchmark in self.benchmarks):
            return [view_name]
        raise ValueError(f"Unknown viewer benchmark: {view_name}")

    def label_for_view(self, view_name: str) -> str:
        if view_name == self.overall.name:
            return self.overall.label
        for benchmark in self.benchmarks:
            if benchmark.name == view_name:
                return benchmark.display_label
        return view_name


def load_viewer_config(config_dir: Path = Path("config/viewer")) -> ViewerConfig:
    benchmarks_path = config_dir / "benchmarks.yaml"
    overall_path = config_dir / "overall.yaml"
    benchmarks_payload = yaml.safe_load(benchmarks_path.read_text(encoding="utf-8"))
    overall_payload = yaml.safe_load(overall_path.read_text(encoding="utf-8"))

    benchmarks = [BenchmarkConfig.model_validate(item) for item in benchmarks_payload.get("benchmarks", [])]
    configured_names = {benchmark.name for benchmark in benchmarks}
    overall = OverallConfig.model_validate(overall_payload)
    missing = [name for name in overall.benchmarks if name not in configured_names]
    if missing:
        raise ValueError(f"Unknown overall benchmark(s): {', '.join(missing)}")
    return ViewerConfig(benchmarks=benchmarks, overall=overall)
