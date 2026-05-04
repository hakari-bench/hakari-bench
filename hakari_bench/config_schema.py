from __future__ import annotations

from typing import Any

from pydantic import BaseModel, ConfigDict, Field


class ConfigModel(BaseModel):
    model_config = ConfigDict(extra="forbid")


class DatasetConfigModel(ConfigModel):
    name: str
    dataset_id: str
    corpus_config: str = "corpus"
    queries_config: str = "queries"
    qrels_config: str = "qrels"
    candidate_config: str | None = "bm25"
    benchmark_kind: str = "nano"
    splits: list[str] | None = None
    split_mapping: dict[str, str] | None = None
    metadata: dict[str, Any] | None = None
    task_metadata: dict[str, dict[str, Any]] | None = None


class DatasetConfigFileModel(ConfigModel):
    datasets: list[DatasetConfigModel] = Field(default_factory=list)


class DatasetCollectionConfigModel(ConfigModel):
    name: str
    datasets: list[str | DatasetConfigModel]
    metadata: dict[str, Any] | None = None
