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
    experiment_fingerprint: str | None = None
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
            self.experiment_fingerprint,
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


class TaskDiagnosticRow(WarehouseModel):
    model_dir: str
    model_name: str
    benchmark: str
    dataset_id: str
    task_name: str
    task_key: str
    result_path: str
    base_score: float
    rerank_score: float | None = None
    rerank_lift: float | None = None
    rerank_status: str | None = None
    rerank_top_k: int | None = None
    candidate_source: str | None = None
    candidate_ranking: str | None = None
    bm25_source: str | None = None
    query_coverage: float | None = None
    relevant_coverage: float | None = None
    covered_query_count: int | None = None
    query_with_relevance_count: int | None = None
    covered_relevant_count: int | None = None
    relevant_count: int | None = None
    dataset_load_seconds: float | None = None
    query_embedding_seconds: float | None = None
    corpus_embedding_seconds: float | None = None
    score_and_topk_seconds: float | None = None
    metric_compute_seconds: float | None = None
    pure_compute_seconds: float | None = None
    wall_seconds: float | None = None
    duration_seconds_including_dataset_load: float | None = None

    def duckdb_values(self) -> tuple[object, ...]:
        return (
            self.model_dir,
            self.model_name,
            self.benchmark,
            self.dataset_id,
            self.task_name,
            self.task_key,
            self.result_path,
            self.base_score,
            self.rerank_score,
            self.rerank_lift,
            self.rerank_status,
            self.rerank_top_k,
            self.candidate_source,
            self.candidate_ranking,
            self.bm25_source,
            self.query_coverage,
            self.relevant_coverage,
            self.covered_query_count,
            self.query_with_relevance_count,
            self.covered_relevant_count,
            self.relevant_count,
            self.dataset_load_seconds,
            self.query_embedding_seconds,
            self.corpus_embedding_seconds,
            self.score_and_topk_seconds,
            self.metric_compute_seconds,
            self.pure_compute_seconds,
            self.wall_seconds,
            self.duration_seconds_including_dataset_load,
        )


class DatasetMetadataRow(WarehouseModel):
    benchmark: str
    dataset_id: str
    dataset_name: str
    split_name: str | None = None
    task_name: str
    task_key: str
    language: str | None = None
    category: str | None = None
    short_description: str | None = None
    citation_count: int | None = None
    reference_count: int | None = None
    has_bibtex: bool | None = None
    query_count: int | None = None
    document_count: int | None = None
    query_mean_chars: float | None = None
    document_mean_chars: float | None = None

    def duckdb_values(self) -> tuple[object, ...]:
        return (
            self.benchmark,
            self.dataset_id,
            self.dataset_name,
            self.split_name,
            self.task_name,
            self.task_key,
            self.language,
            self.category,
            self.short_description,
            self.citation_count,
            self.reference_count,
            self.has_bibtex,
            self.query_count,
            self.document_count,
            self.query_mean_chars,
            self.document_mean_chars,
        )
