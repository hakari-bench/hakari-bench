from __future__ import annotations

import re
from collections.abc import Iterable, Sequence
from dataclasses import dataclass
from pathlib import Path
from typing import Annotated

import yaml
from pydantic import BaseModel, ConfigDict, Field, ValidationError, field_validator
from pydantic.types import StringConstraints


BENCHMARK_TASK_METADATA_RE = re.compile(
    r"<!-- benchmark-task-metadata:v1 -->\s*```yaml\n(.*?)\n```",
    re.DOTALL,
)

NonEmptyStr = Annotated[str, StringConstraints(strip_whitespace=True, min_length=1)]
UnitScore = Annotated[float, Field(ge=0.0, le=1.0)]
NonNegativeFloat = Annotated[float, Field(ge=0.0)]
NonNegativeInt = Annotated[int, Field(ge=0)]


class BenchmarkDocsModel(BaseModel):
    model_config = ConfigDict(extra="forbid")


class SourceResearchMetadata(BenchmarkDocsModel):
    primary_source_type: NonEmptyStr
    paper_pdf_or_html_checked: bool
    no_paper_note: NonEmptyStr | None = None
    paper_url: NonEmptyStr | None = None
    additional_source_urls: list[NonEmptyStr] | None = None
    note: NonEmptyStr | None = None
    no_fulltext_note: NonEmptyStr | None = None


class CountMetadata(BenchmarkDocsModel):
    queries: NonNegativeInt
    documents: NonNegativeInt
    positive_qrels: NonNegativeInt


class PositivesPerQueryMetadata(BenchmarkDocsModel):
    average: NonNegativeFloat
    min: NonNegativeInt
    median: NonNegativeFloat
    max: NonNegativeInt
    multi_positive_queries: NonNegativeInt
    multi_positive_query_percent: Annotated[float, Field(ge=0.0, le=100.0)] | None = None


class TextStatsCharsMetadata(BenchmarkDocsModel):
    query_mean: NonNegativeFloat
    document_mean: NonNegativeFloat


class BM25Metadata(BenchmarkDocsModel):
    ndcg_at_10: UnitScore
    hit_at_10: UnitScore
    source: NonEmptyStr
    original_paper_en_ndcg_at_10: NonNegativeFloat | None = None
    original_paper_en_recall_at_100: NonNegativeFloat | None = None
    dureader_paper_cmedqa_bm25_mrr_at_10: NonNegativeFloat | None = None
    dureader_paper_cmedqa_bm25_recall_at_1: NonNegativeFloat | None = None
    dureader_paper_cmedqa_bm25_recall_at_50: NonNegativeFloat | None = None


class LeakageRiskMetadata(BenchmarkDocsModel):
    source_dataset: NonEmptyStr
    risk: NonEmptyStr
    recommended_filter: NonEmptyStr
    source_train_queries_reported_by_coir: NonNegativeInt | None = None
    source_test_queries_reported_by_coir: NonNegativeInt | None = None
    source_dev_queries_reported_by_coir: NonNegativeInt | None = None
    source_corpus_size_reported_by_coderag_bench: NonNegativeInt | None = None


class LeakageAuditMetadata(BenchmarkDocsModel):
    source_dataset: NonEmptyStr
    source_train_rows_scanned: NonNegativeInt
    nano_query_rows: NonNegativeInt
    normalized_exact_query_matches: NonNegativeInt
    normalized_exact_positive_matches: NonNegativeInt
    high_shingle_query_matches: NonNegativeInt
    high_shingle_positive_matches: NonNegativeInt
    risk: NonEmptyStr
    normalized_exact_query_positive_matches: NonNegativeInt | None = None


class SyntheticDataMetadata(BenchmarkDocsModel):
    document_generation: NonEmptyStr
    question_generation: NonEmptyStr
    answerability: NonEmptyStr
    hard_negatives: NonEmptyStr | None = None


class LearningMetadata(BenchmarkDocsModel):
    original_train_split: NonEmptyStr
    evaluation_split_origin: NonEmptyStr
    train_eval_overlap_audit: NonEmptyStr
    leakage_note: NonEmptyStr
    useful_training_data: list[NonEmptyStr]
    synthetic_data: SyntheticDataMetadata
    multi_positive_training: NonEmptyStr
    leakage_risk: LeakageRiskMetadata | None = None
    leakage_audit: LeakageAuditMetadata | None = None


class SourceUrlMetadata(BenchmarkDocsModel):
    label: NonEmptyStr
    url: NonEmptyStr


class LinkMetadata(BenchmarkDocsModel):
    nano_dataset: NonEmptyStr
    source_urls: list[SourceUrlMetadata]
    source_notes: list[NonEmptyStr] | None = None


class ReferenceMetadata(BenchmarkDocsModel):
    title: NonEmptyStr
    url: NonEmptyStr
    year: NonNegativeInt | None = None
    is_paper: bool
    doi: NonEmptyStr | None = None
    source_confidence: NonEmptyStr | None = None


class BenchmarkTaskMetadata(BenchmarkDocsModel):
    schema_version: int
    document_status: NonEmptyStr
    nano_set: NonEmptyStr
    backing_dataset: NonEmptyStr
    dataset_id: NonEmptyStr
    task_name: NonEmptyStr
    split_name: NonEmptyStr
    language: NonEmptyStr
    category: NonEmptyStr
    document_path: NonEmptyStr
    source_research: SourceResearchMetadata
    counts: CountMetadata
    positives_per_query: PositivesPerQueryMetadata
    text_stats_chars: TextStatsCharsMetadata
    bm25: BM25Metadata
    learning: LearningMetadata | None = None
    links: LinkMetadata | None = None
    references: list[ReferenceMetadata] | None = None
    source_dataset_id: NonEmptyStr | None = None
    source_task: NonEmptyStr | None = None
    example_count: NonNegativeInt | None = None

    @field_validator("schema_version")
    @classmethod
    def validate_schema_version(cls, value: int) -> int:
        if value != 1:
            raise ValueError("schema_version must be 1.")
        return value

    @field_validator("language", mode="before")
    @classmethod
    def normalize_yaml_boolean_language(cls, value: object) -> object:
        if isinstance(value, bool):
            return "yes" if value else "no"
        return value


class BenchmarkTaskMetadataDocument(BenchmarkDocsModel):
    benchmark_task_metadata: BenchmarkTaskMetadata


@dataclass(frozen=True)
class BenchmarkDocsValidationIssue:
    path: Path
    message: str


def load_benchmark_task_metadata(path: Path) -> BenchmarkTaskMetadata:
    return load_benchmark_task_metadata_document(path).benchmark_task_metadata


def load_benchmark_task_metadata_document(path: Path) -> BenchmarkTaskMetadataDocument:
    text = path.read_text(encoding="utf-8")
    match = BENCHMARK_TASK_METADATA_RE.search(text)
    if not match:
        raise ValueError("missing benchmark task metadata block")
    try:
        payload = yaml.safe_load(match.group(1))
    except yaml.YAMLError as exc:
        raise ValueError(f"invalid benchmark task metadata YAML: {exc}") from exc
    return BenchmarkTaskMetadataDocument.model_validate(payload)


def collect_benchmark_task_doc_paths(paths: Sequence[Path], *, docs_root: Path) -> list[Path]:
    if paths:
        return sorted(_expand_doc_paths(paths))
    return sorted(path for path in docs_root.rglob("*.md") if path.name != "index.md")


def validate_benchmark_task_docs(
    paths: Sequence[Path] = (),
    *,
    docs_root: Path = Path("docs/benchmark_tasks"),
    validate_document_paths: bool = True,
) -> tuple[list[BenchmarkTaskMetadata], list[BenchmarkDocsValidationIssue]]:
    metadata: list[BenchmarkTaskMetadata] = []
    issues: list[BenchmarkDocsValidationIssue] = []
    for path in collect_benchmark_task_doc_paths(paths, docs_root=docs_root):
        try:
            item = load_benchmark_task_metadata(path)
            if validate_document_paths:
                _validate_document_path(path=path, metadata=item)
        except (OSError, ValidationError, ValueError) as exc:
            issues.append(BenchmarkDocsValidationIssue(path=path, message=_format_validation_error(exc)))
            continue
        metadata.append(item)
    return metadata, issues


def _expand_doc_paths(paths: Sequence[Path]) -> Iterable[Path]:
    for path in paths:
        if path.is_dir():
            yield from (item for item in path.rglob("*.md") if item.name != "index.md")
        else:
            yield path


def _validate_document_path(*, path: Path, metadata: BenchmarkTaskMetadata) -> None:
    expected = _repo_relative_path(path)
    if metadata.document_path != expected:
        raise ValueError(f"document_path must be {expected!r}, got {metadata.document_path!r}")


def _repo_relative_path(path: Path) -> str:
    resolved = path.resolve()
    try:
        return resolved.relative_to(Path.cwd().resolve()).as_posix()
    except ValueError:
        return path.as_posix()


def _format_validation_error(exc: Exception) -> str:
    if isinstance(exc, ValidationError):
        messages: list[str] = []
        for error in exc.errors():
            loc = ".".join(str(part) for part in error["loc"])
            messages.append(f"{loc}: {error['msg']}")
        return "; ".join(messages)
    return str(exc)
