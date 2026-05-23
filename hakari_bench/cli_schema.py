from __future__ import annotations

from typing import Any, Literal

from pydantic import BaseModel, ConfigDict, Field, ValidationInfo, field_validator


class ParamsModel(BaseModel):
    model_config = ConfigDict(extra="forbid", strict=True)


def _validate_non_empty_strings(value: list[str], field_name: str) -> list[str]:
    if any(not item for item in value):
        raise ValueError(f"{field_name} must contain only non-empty strings.")
    return value


class ModelParams(ParamsModel):
    source: str | None = None
    alias: str | None = None
    revision: str | None = None


class TargetParams(ParamsModel):
    all: bool | None = None
    datasets: list[str] | None = None
    collections: list[str] | None = None
    splits: list[str] | None = None
    dataset_revision: str | None = None

    @field_validator("datasets", "collections", "splits")
    @classmethod
    def validate_string_lists(cls, value: list[str] | None, info: ValidationInfo) -> list[str] | None:
        return None if value is None else _validate_non_empty_strings(value, str(info.field_name))


class RuntimeParams(ParamsModel):
    batch_size: int | None = Field(default=None, gt=0)
    dtype: Literal["bf16", "fp16", "fp32"] | None = None
    attn_implementation: str | None = None
    flash_attn2: bool | None = None
    device: str | None = None
    retrieval_score_device: Literal["auto", "cpu", "cuda"] | None = None
    encode_devices: list[str] | None = None
    encode_chunk_size: int | None = Field(default=None, gt=0)
    trust_remote_code: bool | None = None
    model_max_seq_length: int | None = Field(default=None, gt=0)
    truncate_dim: int | None = Field(default=None, gt=0)
    show_progress: bool | None = None

    @field_validator("encode_devices")
    @classmethod
    def validate_encode_devices(cls, value: list[str] | None) -> list[str] | None:
        return None if value is None else _validate_non_empty_strings(value, "encode_devices")


class OutputParams(ParamsModel):
    results_dir: str | None = None
    candidates_dir: str | None = None
    overwrite: bool | None = None
    save_top_rankings: bool | None = None


class BuildCandidatesOutputParams(ParamsModel):
    candidates_dir: str | None = None
    overwrite: bool | None = None


class PromptParams(ParamsModel):
    query_prompt: str | None = None
    document_prompt: str | None = None
    query_prompt_name: str | None = None
    document_prompt_name: str | None = None
    query_encode_task: str | None = None
    document_encode_task: str | None = None


class RerankerParams(ParamsModel):
    init_kwargs: dict[str, Any] | None = None
    inference_kwargs: dict[str, Any] | None = None
    candidate_ranking: str | None = None
    rerank_top_k: int | None = Field(default=None, gt=0)


class SparseParams(ParamsModel):
    query_max_active_dims: int | None = Field(default=None, gt=0)
    document_max_active_dims: int | None = Field(default=None, gt=0)


class EmbeddingParams(ParamsModel):
    variants: list[str] | None = None
    variant_grid: list[list[str]] | None = None
    default_variants: bool | None = None

    @field_validator("variants")
    @classmethod
    def validate_variants(cls, value: list[str] | None, info: ValidationInfo) -> list[str] | None:
        return None if value is None else _validate_non_empty_strings(value, str(info.field_name))

    @field_validator("variant_grid")
    @classmethod
    def validate_variant_grid(cls, value: list[list[str]] | None) -> list[list[str]] | None:
        if value is None:
            return None
        for index, item in enumerate(value):
            _validate_non_empty_strings(item, f"variant_grid[{index}]")
        return value


class BM25Params(ParamsModel):
    source: Literal["dataset", "computed"] | None = None
    top_k: int | None = Field(default=None, gt=0)
    tokenizer: Literal[
        "regex",
        "whitespace",
        "transformer",
        "stemmer",
        "english_regex",
        "english_porter",
        "english_porter_stop",
        "wordseg",
    ] | None = None
    tokenizer_model: str | None = None
    wordseg_language: str | None = None
    stemmer_language: str | None = None
    k1: float | None = None
    b: float | None = None


class BuildCandidatesBM25Params(ParamsModel):
    top_k: int | None = Field(default=None, gt=0)
    tokenizer: Literal[
        "regex",
        "whitespace",
        "transformer",
        "stemmer",
        "english_regex",
        "english_porter",
        "english_porter_stop",
        "wordseg",
    ] | None = None
    tokenizer_model: str | None = None
    wordseg_language: str | None = None
    stemmer_language: str | None = None
    k1: float | None = None
    b: float | None = None


class LateInteractionParams(ParamsModel):
    query_length: int | None = Field(default=None, gt=0)
    document_length: int | None = Field(default=None, gt=0)
    query_prefix: str | None = None
    document_prefix: str | None = None
    do_query_expansion: bool | None = None
    attend_to_expansion_tokens: bool | None = None
    exact_document_batch_size: int | None = Field(default=None, gt=0)
    exact_query_batch_size: int | None = Field(default=None, gt=0)


class EvaluateParamsJson(ParamsModel):
    model: ModelParams | None = None
    target: TargetParams | None = None
    runtime: RuntimeParams | None = None
    output: OutputParams | None = None
    prompts: PromptParams | None = None
    reranker: RerankerParams | None = None
    sparse: SparseParams | None = None
    embedding: EmbeddingParams | None = None
    bm25: BM25Params | None = None
    late_interaction: LateInteractionParams | None = None


class BuildCandidatesParamsJson(ParamsModel):
    target: TargetParams | None = None
    output: BuildCandidatesOutputParams | None = None
    bm25: BuildCandidatesBM25Params | None = None
