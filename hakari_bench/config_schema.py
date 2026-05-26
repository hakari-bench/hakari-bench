from __future__ import annotations

from typing import Any

from pydantic import BaseModel, ConfigDict, Field

from hakari_bench.defaults import DEFAULT_CANDIDATE_RANKING


class ConfigModel(BaseModel):
    model_config = ConfigDict(extra="forbid")


class EvaluationScopeConfigModel(ConfigModel):
    include_by_default: bool = True
    tags: list[str] = Field(default_factory=list)
    reason: str | None = None


class DatasetConfigModel(ConfigModel):
    name: str
    dataset_id: str
    corpus_config: str = "corpus"
    queries_config: str = "queries"
    qrels_config: str = "qrels"
    candidate_config: str | None = DEFAULT_CANDIDATE_RANKING
    benchmark_kind: str = "nano"
    splits: list[str] | None = None
    split_mapping: dict[str, str] | None = None
    evaluation_scope: EvaluationScopeConfigModel | None = None
    task_evaluation_scope: dict[str, EvaluationScopeConfigModel] | None = None
    metadata: dict[str, Any] | None = None
    task_metadata: dict[str, dict[str, Any]] | None = None


class DatasetConfigFileModel(ConfigModel):
    datasets: list[DatasetConfigModel] = Field(default_factory=list)


class DatasetCollectionConfigModel(ConfigModel):
    name: str
    datasets: list[str | DatasetConfigModel]
    metadata: dict[str, Any] | None = None
