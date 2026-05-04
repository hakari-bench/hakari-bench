from __future__ import annotations

from pydantic import BaseModel, ConfigDict


class WarehouseModel(BaseModel):
    model_config = ConfigDict(frozen=True, extra="forbid")


class TaskResultRow(WarehouseModel):
    model_dir: str
    model_name: str
    benchmark: str
    dataset_id: str
    dataset_revision: str | None = None
    dataset_revision_requested: str | None = None
    dataset_name: str
    split_name: str | None = None
    task_name: str
    task_key: str
    score: float
    aggregate_metric: str | None = None
    result_path: str
    active_parameters: int | None = None
    total_parameters: int | None = None
    max_seq_length: int | None = None
    dtype: str | None = None
    attn_implementation: str | None = None
    torch_version: str | None = None
    transformers_version: str | None = None
    sentence_transformers_version: str | None = None
    started_at_utc: str | None = None
    finished_at_utc: str | None = None
    evaluated_at_utc: str | None = None
    duration_seconds_including_dataset_load: float | None = None
    wall_seconds: float | None = None
    embedding_variant_name: str | None = None
    embedding_dim: int | None = None
    quantization: str | None = None

    @property
    def score_100(self) -> float:
        return self.score * 100.0

    def duckdb_values(self) -> tuple[object, ...]:
        return (
            self.model_dir,
            self.model_name,
            self.benchmark,
            self.dataset_id,
            self.dataset_revision,
            self.dataset_revision_requested,
            self.dataset_name,
            self.split_name,
            self.task_name,
            self.task_key,
            self.score,
            self.score_100,
            self.aggregate_metric,
            self.result_path,
            self.active_parameters,
            self.total_parameters,
            self.max_seq_length,
            self.dtype,
            self.embedding_variant_name,
            self.embedding_dim,
            self.quantization,
            self.attn_implementation,
            self.torch_version,
            self.transformers_version,
            self.sentence_transformers_version,
            self.started_at_utc,
            self.finished_at_utc,
            self.evaluated_at_utc,
            self.duration_seconds_including_dataset_load,
            self.wall_seconds,
        )


class MetricLongRow(WarehouseModel):
    model_dir: str
    model_name: str
    benchmark: str
    dataset_id: str
    task_name: str
    metric_name: str
    metric_value: float
    result_path: str

    def duckdb_values(self) -> tuple[object, ...]:
        return (
            self.model_dir,
            self.model_name,
            self.benchmark,
            self.dataset_id,
            self.task_name,
            self.metric_name,
            self.metric_value,
            self.result_path,
        )
