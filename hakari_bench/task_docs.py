from __future__ import annotations

import json
import re
from collections.abc import Iterable, Sequence
from dataclasses import dataclass
from pathlib import Path
from typing import Annotated

import yaml
from pydantic import AliasChoices, BaseModel, ConfigDict, Field, ValidationError, field_validator
from pydantic.types import StringConstraints


TASK_METADATA_RE = re.compile(
    r"<!-- benchmark-task-metadata:v1 -->\s*```yaml\n(.*?)\n```",
    re.DOTALL,
)
DEFAULT_TASK_DOCS_ROOT = Path("task_docs/docs")
DEFAULT_TASK_METADATA_ROOT = Path("task_docs/metadata")

NonEmptyStr = Annotated[str, StringConstraints(strip_whitespace=True, min_length=1)]
UnitScore = Annotated[float, Field(ge=0.0, le=1.0)]
NonNegativeFloat = Annotated[float, Field(ge=0.0)]
NonNegativeInt = Annotated[int, Field(ge=0)]


class TaskDocsModel(BaseModel):
    model_config = ConfigDict(extra="forbid", populate_by_name=True)


class SourceResearchMetadata(TaskDocsModel):
    primary_source_type: NonEmptyStr
    paper_pdf_or_html_checked: bool
    no_paper_note: NonEmptyStr | None = None
    paper_url: NonEmptyStr | None = None
    additional_source_urls: list[NonEmptyStr] | None = None
    note: NonEmptyStr | None = None
    no_fulltext_note: NonEmptyStr | None = None


class CountMetadata(TaskDocsModel):
    queries: NonNegativeInt
    documents: NonNegativeInt
    positive_qrels: NonNegativeInt


class PositivesPerQueryMetadata(TaskDocsModel):
    average: NonNegativeFloat
    min: NonNegativeInt
    median: NonNegativeFloat
    max: NonNegativeInt
    multi_positive_queries: NonNegativeInt
    multi_positive_query_percent: Annotated[float, Field(ge=0.0, le=100.0)] | None = None


class TextStatsCharsMetadata(TaskDocsModel):
    query_mean: NonNegativeFloat
    document_mean: NonNegativeFloat
    query_median: NonNegativeFloat | None = None
    query_max: NonNegativeInt | None = None
    document_median: NonNegativeFloat | None = None
    document_max: NonNegativeInt | None = None


class BM25Metadata(TaskDocsModel):
    ndcg_at_10: UnitScore
    hit_at_10: UnitScore
    source: NonEmptyStr
    original_paper_en_ndcg_at_10: NonNegativeFloat | None = None
    original_paper_en_recall_at_100: NonNegativeFloat | None = None
    dureader_paper_cmedqa_bm25_mrr_at_10: NonNegativeFloat | None = None
    dureader_paper_cmedqa_bm25_recall_at_1: NonNegativeFloat | None = None
    dureader_paper_cmedqa_bm25_recall_at_50: NonNegativeFloat | None = None


class CandidateSubsetMetricsMetadata(TaskDocsModel):
    config: NonEmptyStr
    label: NonEmptyStr
    source: NonEmptyStr
    top_k: NonNegativeInt
    ndcg_at_10: UnitScore
    hit_at_10: UnitScore
    recall_at_100: UnitScore
    candidate_count_min: NonNegativeInt
    candidate_count_max: NonNegativeInt
    candidate_count_mean: NonNegativeFloat
    query_count: NonNegativeInt
    query_coverage: UnitScore
    relevant_coverage_at_100: UnitScore
    safeguard_positive_rows: NonNegativeInt | None = None
    rows_with_101_candidates: NonNegativeInt | None = None


class CandidateSubsetsMetadata(TaskDocsModel):
    bm25: CandidateSubsetMetricsMetadata | None = None
    dense: CandidateSubsetMetricsMetadata | None = None
    reranking_hybrid: CandidateSubsetMetricsMetadata | None = None


class LeakageRiskMetadata(TaskDocsModel):
    source_dataset: NonEmptyStr
    risk: NonEmptyStr
    recommended_filter: NonEmptyStr
    source_train_queries_reported_by_coir: NonNegativeInt | None = None
    source_test_queries_reported_by_coir: NonNegativeInt | None = None
    source_dev_queries_reported_by_coir: NonNegativeInt | None = None
    source_corpus_size_reported_by_coderag_bench: NonNegativeInt | None = None


class LeakageAuditMetadata(TaskDocsModel):
    source_dataset: NonEmptyStr
    source_train_rows_scanned: NonNegativeInt
    nano_query_rows: NonNegativeInt
    normalized_exact_query_matches: NonNegativeInt
    normalized_exact_positive_matches: NonNegativeInt
    high_shingle_query_matches: NonNegativeInt
    high_shingle_positive_matches: NonNegativeInt
    risk: NonEmptyStr
    normalized_exact_query_positive_matches: NonNegativeInt | None = None


class SyntheticDataMetadata(TaskDocsModel):
    document_generation: NonEmptyStr
    question_generation: NonEmptyStr
    answerability: NonEmptyStr
    hard_negatives: NonEmptyStr | None = None


class LearningMetadata(TaskDocsModel):
    original_train_split: NonEmptyStr
    evaluation_split_origin: NonEmptyStr
    train_eval_overlap_audit: NonEmptyStr
    leakage_note: NonEmptyStr
    useful_training_data: list[NonEmptyStr]
    synthetic_data: SyntheticDataMetadata
    multi_positive_training: NonEmptyStr
    leakage_risk: LeakageRiskMetadata | None = None
    leakage_audit: LeakageAuditMetadata | None = None


class SourceUrlMetadata(TaskDocsModel):
    label: NonEmptyStr
    url: NonEmptyStr


class LinkMetadata(TaskDocsModel):
    nano_dataset: NonEmptyStr
    source_urls: list[SourceUrlMetadata]
    source_notes: list[NonEmptyStr] | None = None


class ReferenceMetadata(TaskDocsModel):
    title: NonEmptyStr
    url: NonEmptyStr
    year: NonNegativeInt | None = None
    is_paper: bool
    doi: NonEmptyStr | None = None
    source_confidence: NonEmptyStr | None = None


class TaskMetadata(TaskDocsModel):
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
    candidate_subsets: CandidateSubsetsMetadata | None = None
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


class TaskMetadataDocument(TaskDocsModel):
    task_metadata: TaskMetadata = Field(validation_alias=AliasChoices("task_metadata", "benchmark_task_metadata"))

    @property
    def benchmark_task_metadata(self) -> TaskMetadata:
        return self.task_metadata


@dataclass(frozen=True)
class TaskDocsValidationIssue:
    path: Path
    message: str


def task_metadata_json_path(
    path: Path,
    *,
    docs_root: Path = DEFAULT_TASK_DOCS_ROOT,
    metadata_root: Path = DEFAULT_TASK_METADATA_ROOT,
) -> Path:
    try:
        relative_path = path.resolve().relative_to(docs_root.resolve())
    except ValueError:
        try:
            relative_path = path.relative_to(docs_root)
        except ValueError:
            relative_path = path.name
    return metadata_root / Path(relative_path).with_suffix(".json")


def load_task_metadata(
    path: Path,
    *,
    docs_root: Path = DEFAULT_TASK_DOCS_ROOT,
    metadata_root: Path = DEFAULT_TASK_METADATA_ROOT,
) -> TaskMetadata:
    return load_task_metadata_document(
        path,
        docs_root=docs_root,
        metadata_root=metadata_root,
    ).task_metadata


def load_task_metadata_document(
    path: Path,
    *,
    docs_root: Path = DEFAULT_TASK_DOCS_ROOT,
    metadata_root: Path = DEFAULT_TASK_METADATA_ROOT,
    prefer_external: bool = True,
) -> TaskMetadataDocument:
    metadata_path = task_metadata_json_path(path, docs_root=docs_root, metadata_root=metadata_root)
    if prefer_external and metadata_path.exists():
        return load_task_metadata_json(metadata_path)

    text = path.read_text(encoding="utf-8")
    match = TASK_METADATA_RE.search(text)
    if match:
        try:
            payload = yaml.safe_load(match.group(1))
        except yaml.YAMLError as exc:
            raise ValueError(f"invalid task metadata YAML: {exc}") from exc
        return TaskMetadataDocument.model_validate(payload)

    if metadata_path.exists():
        return load_task_metadata_json(metadata_path)

    raise ValueError(f"missing task metadata JSON at {metadata_path} or embedded metadata block")


def load_task_metadata_json(path: Path) -> TaskMetadataDocument:
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        raise ValueError(f"invalid task metadata JSON: {exc}") from exc
    return TaskMetadataDocument.model_validate(payload)


def collect_task_doc_paths(paths: Sequence[Path], *, docs_root: Path) -> list[Path]:
    if paths:
        return sorted(_expand_doc_paths(paths))
    return sorted(path for path in docs_root.rglob("*.md") if path.name != "index.md")


def validate_task_docs(
    paths: Sequence[Path] = (),
    *,
    docs_root: Path = DEFAULT_TASK_DOCS_ROOT,
    metadata_root: Path = DEFAULT_TASK_METADATA_ROOT,
    validate_document_paths: bool = True,
) -> tuple[list[TaskMetadata], list[TaskDocsValidationIssue]]:
    metadata: list[TaskMetadata] = []
    issues: list[TaskDocsValidationIssue] = []
    for path in collect_task_doc_paths(paths, docs_root=docs_root):
        try:
            item = load_task_metadata(path, docs_root=docs_root, metadata_root=metadata_root)
            if validate_document_paths:
                _validate_document_path(path=path, metadata=item)
        except (OSError, ValidationError, ValueError) as exc:
            issues.append(TaskDocsValidationIssue(path=path, message=_format_validation_error(exc)))
            continue
        metadata.append(item)
    return metadata, issues


def _expand_doc_paths(paths: Sequence[Path]) -> Iterable[Path]:
    for path in paths:
        if path.is_dir():
            yield from (item for item in path.rglob("*.md") if item.name != "index.md")
        else:
            yield path


def _validate_document_path(*, path: Path, metadata: TaskMetadata) -> None:
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


BENCHMARK_TASK_METADATA_RE = TASK_METADATA_RE
DEFAULT_BENCHMARK_TASK_DOCS_ROOT = DEFAULT_TASK_DOCS_ROOT
DEFAULT_BENCHMARK_TASK_METADATA_ROOT = DEFAULT_TASK_METADATA_ROOT
BenchmarkDocsModel = TaskDocsModel
BenchmarkTaskMetadata = TaskMetadata
BenchmarkTaskMetadataDocument = TaskMetadataDocument
BenchmarkDocsValidationIssue = TaskDocsValidationIssue
benchmark_task_metadata_json_path = task_metadata_json_path
load_benchmark_task_metadata = load_task_metadata
load_benchmark_task_metadata_document = load_task_metadata_document
load_benchmark_task_metadata_json = load_task_metadata_json
collect_benchmark_task_doc_paths = collect_task_doc_paths
validate_benchmark_task_docs = validate_task_docs
