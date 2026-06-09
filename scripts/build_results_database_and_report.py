from __future__ import annotations

import argparse
import asyncio
from contextlib import contextmanager
from concurrent.futures import ProcessPoolExecutor
import gzip
import hashlib
import json
import lzma
import math
import os
import resource
import shutil
import sys
from collections import defaultdict
from collections.abc import AsyncIterable, Awaitable, Callable, Iterable, Sequence
from dataclasses import dataclass, field, replace
from datetime import datetime, timezone
from itertools import islice, product
from pathlib import Path
from typing import Any, Literal, cast, overload

import duckdb
import ijson
import orjson
import pyarrow as pa

from hakari_bench.datasets import DatasetRegistry
from hakari_bench.metrics import compute_ir_metrics
from hakari_bench.model_cards import load_model_cards, model_card_yaml_paths
from hakari_bench.viewer.config import BenchmarkConfig, ViewerConfig, load_viewer_config
from hakari_bench.viewer.store import (
    DEFAULT_HF_DUCKDB_PATH,
    HuggingFaceDuckDbSource,
    _download_hf_duckdb,
)
from hakari_bench.viewer.leaderboard import (
    LeaderboardService,
    _aggregate_overall_scores,
    _aggregate_benchmark_score_group_scores,
    _append_missing_bm25_task_scores,
    _exclude_configured_tasks,
    _exclude_reranker_task_scores,
    _language_filter_mode_for_view,
    _language_options,
    _language_page_languages_for_view,
    _overall_metric_score_group,
    _score_groups_for_view,
    _select_score_group,
    _task_scores_from_records,
    compute_leaderboard_rows,
    sort_rows,
)
from hakari_bench.viewer.variant_display import VariantDisplayFlags
from hakari_bench.viewer.task_names import (
    canonical_metric_name,
    canonical_split_name,
    canonical_task_key,
    canonical_task_name,
)
from hakari_bench.warehouse_schema import (
    DatasetMetadataRow,
    MetricLongRow,
    RetrievalRankingRow,
    TaskDiagnosticRow,
    TaskResultRow,
)


DEFAULT_VIEWER_CONFIG_DIR = Path("config/viewer")
DEFAULT_MODEL_CARDS_PATH = Path("config/model_cards")
DuplicateResultPolicy = Literal["first-wins", "last-wins"]
WarehouseBuildMode = Literal["append", "stream", "materialized"]
AppendBaseDuckDb = Literal["latest"] | Path
RESULT_JSON_SUFFIXES = (".json", ".json.gz", ".json.xz")
FULL_PARSE_RESULT_JSON_MAX_BYTES = 128 * 1024
STREAM_RESULT_INSERT_CHUNK_SIZE = 10_000
DEFAULT_RESULTS_DIR = Path("output/hakari-results")
DEFAULT_DUCKDB_PATH = DEFAULT_RESULTS_DIR / "hakari_bench.duckdb"


@dataclass(frozen=True)
class ResultWorkerCounts:
    selection: int
    json: int
    row: int


@dataclass(frozen=True)
class WarehouseBuildPlan:
    mode: WarehouseBuildMode
    results_dirs: list[Path]
    append_results_dirs: list[Path]
    duckdb_path: Path
    append_base_duckdb: AppendBaseDuckDb | None
    append_hf_dataset_repo_id: str | None
    append_hf_dataset_path: str
    append_hf_dataset_revision: str | None
    html_output: Path | None
    viewer_config_dir: Path
    model_cards_path: Path | None
    parquet_output_dir: Path | None
    include_retrieval_rankings: bool
    include_result_extensions: bool
    incremental: bool
    duplicate_result_policy: DuplicateResultPolicy
    result_workers: ResultWorkerCounts
    exclude_model_names: set[str]
    model_name_override: str | None


def _physical_cpu_count_from_linux_cpuinfo(
    cpuinfo_text: str,
    *,
    allowed_processors: set[int] | None = None,
) -> int | None:
    cores: set[tuple[str, str]] = set()
    processor: int | None = None
    physical_id: str | None = None
    core_id: str | None = None

    def flush_record() -> None:
        nonlocal processor, physical_id, core_id
        if (
            processor is not None
            and physical_id is not None
            and core_id is not None
            and (allowed_processors is None or processor in allowed_processors)
        ):
            cores.add((physical_id, core_id))
        processor = None
        physical_id = None
        core_id = None

    for line in cpuinfo_text.splitlines():
        if not line.strip():
            flush_record()
            continue
        key, separator, value = line.partition(":")
        if not separator:
            continue
        key = key.strip()
        value = value.strip()
        if key == "processor":
            try:
                processor = int(value)
            except ValueError:
                processor = None
        elif key == "physical id":
            physical_id = value
        elif key == "core id":
            core_id = value
    flush_record()
    return len(cores) or None


def _available_cpu_count() -> int | None:
    process_cpu_count = getattr(os, "process_cpu_count", None)
    if process_cpu_count is not None:
        count = process_cpu_count()
        if count:
            return int(count)
    affinity = _sched_getaffinity(0)
    if affinity is not None:
        return len(affinity)
    return os.cpu_count()


def _sched_getaffinity(pid: int) -> set[int] | None:
    sched_getaffinity = getattr(os, "sched_getaffinity", None)
    if sched_getaffinity is None:
        return None
    return set(sched_getaffinity(pid))


def _linux_physical_cpu_count(cpuinfo_path: Path = Path("/proc/cpuinfo")) -> int | None:
    try:
        cpuinfo_text = cpuinfo_path.read_text(encoding="utf-8")
    except OSError:
        return None
    allowed_processors = _sched_getaffinity(0)
    return _physical_cpu_count_from_linux_cpuinfo(
        cpuinfo_text,
        allowed_processors=allowed_processors,
    )


def default_result_worker_count() -> int:
    cpu_count = _linux_physical_cpu_count() or _available_cpu_count() or 1
    return max(1, cpu_count - 1)


def resolve_result_worker_counts(
    *,
    result_selection_workers: int | None,
    result_json_workers: int | None,
    result_row_workers: int | None,
    default_workers: int | None = None,
) -> ResultWorkerCounts:
    default_workers = default_result_worker_count() if default_workers is None else max(1, default_workers)
    selection_workers = max(1, result_selection_workers) if result_selection_workers is not None else default_workers
    if result_row_workers is not None:
        return ResultWorkerCounts(
            selection=selection_workers,
            json=max(1, result_json_workers) if result_json_workers is not None else 1,
            row=max(1, result_row_workers),
        )
    if result_json_workers is not None:
        return ResultWorkerCounts(
            selection=selection_workers,
            json=max(1, result_json_workers),
            row=1,
        )
    return ResultWorkerCounts(
        selection=selection_workers,
        json=default_workers,
        row=default_workers,
    )


def load_benchmark_configs(config_dir: Path = DEFAULT_VIEWER_CONFIG_DIR) -> list[BenchmarkConfig]:
    return load_viewer_config(config_dir).benchmarks


def target_benchmark_names(benchmark_configs: Sequence[BenchmarkConfig]) -> list[str]:
    return [benchmark.name for benchmark in benchmark_configs]


TARGET_BENCHMARKS: list[str] = target_benchmark_names(load_benchmark_configs())
VIEWS = ["Overall", *TARGET_BENCHMARKS]
WAREHOUSE_SCHEMA_VERSION = "8"
WAREHOUSE_COMPATIBILITY_LEVEL = "current"
WAREHOUSE_TABLES = (
    "meta_database",
    "schema_change_log",
    "ingestion_batches",
    "source_load_state",
    "result_extensions",
    "runs",
    "dim_model",
    "dim_metric",
    "dim_task",
    "dim_variant",
    "task_results",
    "fact_task_score",
    "fact_metric_score",
    "metrics_long",
    "retrieval_rankings",
    "task_diagnostics",
    "dataset_metadata",
    "viewer_task_results",
    "viewer_filter_values",
    "viewer_leaderboard_rows",
    "viewer_leaderboard_language_options",
    "model_scores",
    "borda_task_scores",
)
TASK_RESULT_COLUMNS = (
    "model_dir",
    "model_name",
    "model_revision",
    "model_revision_requested",
    "benchmark",
    "dataset_id",
    "dataset_revision",
    "dataset_revision_requested",
    "dataset_name",
    "split_name",
    "task_name",
    "task_key",
    "score",
    "score_100",
    "aggregate_metric",
    "result_path",
    "experiment_fingerprint",
    "active_parameters",
    "total_parameters",
    "max_seq_length",
    "dtype",
    "embedding_variant_name",
    "embedding_dim",
    "quantization",
    "attn_implementation",
    "query_prompt",
    "document_prompt",
    "query_prompt_name",
    "document_prompt_name",
    "query_encode_task",
    "document_encode_task",
    "trust_remote_code",
    "late_interaction_query_length",
    "late_interaction_document_length",
    "late_interaction_query_prefix",
    "late_interaction_document_prefix",
    "late_interaction_query_expansion",
    "late_interaction_attend_to_expansion_tokens",
    "torch_version",
    "transformers_version",
    "sentence_transformers_version",
    "started_at_utc",
    "finished_at_utc",
    "evaluated_at_utc",
    "duration_seconds_including_dataset_load",
    "wall_seconds",
)
METRIC_LONG_COLUMNS = (
    "model_dir",
    "model_name",
    "benchmark",
    "dataset_id",
    "task_name",
    "metric_name",
    "metric_value",
    "result_path",
    "score_target",
    "embedding_variant_name",
)
VIEWER_RECOMPUTED_METRICS = (
    "nDCG@10",
    "nDCG@100",
    "recall@10",
    "recall@100",
    "acc@1",
    "acc@10",
    "acc@100",
    "mrr@10",
    "map@100",
)
TASK_DIAGNOSTIC_COLUMNS = (
    "model_dir",
    "model_name",
    "benchmark",
    "dataset_id",
    "task_name",
    "task_key",
    "result_path",
    "base_score",
    "rerank_score",
    "rerank_lift",
    "rerank_status",
    "rerank_top_k",
    "candidate_source",
    "candidate_ranking",
    "bm25_source",
    "query_coverage",
    "relevant_coverage",
    "covered_query_count",
    "query_with_relevance_count",
    "covered_relevant_count",
    "relevant_count",
    "dataset_load_seconds",
    "query_embedding_seconds",
    "corpus_embedding_seconds",
    "score_and_topk_seconds",
    "metric_compute_seconds",
    "pure_compute_seconds",
    "wall_seconds",
    "duration_seconds_including_dataset_load",
)
DATASET_METADATA_COLUMNS = (
    "benchmark",
    "dataset_id",
    "dataset_name",
    "split_name",
    "task_name",
    "task_key",
    "language",
    "languages",
    "primary_languages",
    "category",
    "short_description",
    "citation_count",
    "reference_count",
    "has_bibtex",
    "query_count",
    "document_count",
    "query_mean_chars",
    "document_mean_chars",
)
RETRIEVAL_RANKING_COLUMNS = (
    "model_dir",
    "model_name",
    "benchmark",
    "dataset_id",
    "dataset_revision",
    "dataset_name",
    "split_name",
    "task_name",
    "task_key",
    "result_path",
    "ranking_path",
    "ranking_name",
    "ranking_kind",
    "embedding_variant_name",
    "distance",
    "score_name",
    "query_id",
    "rank",
    "corpus_id",
)
SOURCE_LOAD_STATE_COLUMNS = (
    "result_path",
    "payload_sha256",
    "canonical_key_hash",
    "last_successful_batch_id",
    "loaded_at_utc",
)


TaskResult = TaskResultRow


def _chunks(iterable: Iterable[Sequence[Any]], size: int) -> Iterable[list[Sequence[Any]]]:
    iterator = iter(iterable)
    while chunk := list(islice(iterator, size)):
        yield chunk


def _insert_duckdb_rows(
    con: duckdb.DuckDBPyConnection,
    table_name: str,
    columns: Sequence[str],
    rows: Iterable[Sequence[Any]],
    *,
    chunk_size: int = 50_000,
) -> None:
    # Register Arrow chunks and let DuckDB ingest them in-process; Python
    # executemany is a major bottleneck for the hundreds of thousands of rows
    # emitted by full leaderboard builds.
    for chunk in _chunks(rows, chunk_size):
        arrow_table = pa.table(
            {column: [row[index] for row in chunk] for index, column in enumerate(columns)}
        )
        con.register("_hakari_insert_rows", arrow_table)
        try:
            column_sql = ", ".join(columns)
            con.execute(f"INSERT INTO {table_name} ({column_sql}) SELECT {column_sql} FROM _hakari_insert_rows")
        finally:
            con.unregister("_hakari_insert_rows")


def _read_json(path: Path) -> Any:
    with _open_json_bytes(path) as file:
        payload = file.read()
    try:
        return orjson.loads(payload)
    except orjson.JSONDecodeError:
        # Some legacy result JSON contains non-standard NaN/Infinity values.
        # Keep the fast path strict, but preserve compatibility for old runs.
        return json.loads(payload.decode("utf-8"))


def _open_json_bytes(path: Path) -> Any:
    if path.name.endswith(".json.gz"):
        return gzip.open(path, "rb")
    if path.name.endswith(".json.xz"):
        return lzma.open(path, "rb")
    return path.open("rb")


class _HashingReader:
    def __init__(self, file: Any) -> None:
        self.file = file
        self.digest = hashlib.sha256()

    def read(self, size: int = -1) -> bytes:
        data = self.file.read(size)
        if data:
            self.digest.update(data)
        return data

    def readinto(self, buffer: Any) -> int:
        count = self.file.readinto(buffer)
        if count:
            self.digest.update(memoryview(buffer)[:count])
        return count

    def readable(self) -> bool:
        return True

    def close(self) -> None:
        self.file.close()

    def __enter__(self) -> _HashingReader:
        return self

    def __exit__(self, *exc_info: object) -> None:
        self.close()

    def __getattr__(self, name: str) -> Any:
        return getattr(self.file, name)


@contextmanager
def _open_json_bytes_with_raw_sha256(path: Path) -> Any:
    raw_file = path.open("rb")
    hashing_file = _HashingReader(raw_file)
    if path.name.endswith(".json.gz"):
        stream = gzip.GzipFile(fileobj=cast(Any, hashing_file), mode="rb")
    elif path.name.endswith(".json.xz"):
        stream = lzma.LZMAFile(cast(Any, hashing_file), mode="rb")
    else:
        stream = hashing_file
    try:
        yield stream, hashing_file.digest
    finally:
        stream.close()


def _read_result_json(
    path: Path,
    *,
    include_retrieval_rankings: bool,
) -> dict[str, Any] | None:
    try:
        payload = _read_result_summary_json(path)
        artifact = _read_top_rankings_artifact_stream(
            path,
            payload=payload,
            include_retrieval_rankings=include_retrieval_rankings,
        )
        if artifact is not None:
            artifacts = dict(payload.get("artifacts", {}))
            artifacts["top_rankings"] = artifact
            payload["artifacts"] = artifacts
        return payload
    except (ijson.JSONError, UnicodeDecodeError, ValueError):
        payload = _read_json(path)
        if not isinstance(payload, dict):
            return None
        return _compact_result_payload(
            payload,
            include_retrieval_rankings=include_retrieval_rankings,
        )


def _read_result_json_from_summary(
    path: Path,
    *,
    payload: dict[str, Any],
    include_retrieval_rankings: bool,
) -> dict[str, Any] | None:
    if not payload:
        return _read_result_json(path, include_retrieval_rankings=include_retrieval_rankings)
    if not include_retrieval_rankings and _should_full_parse_result_json(path):
        try:
            full_payload = _read_json(path)
            if not isinstance(full_payload, dict):
                return None
            return _compact_result_payload(
                full_payload,
                include_retrieval_rankings=include_retrieval_rankings,
            )
        except (OSError, orjson.JSONDecodeError, json.JSONDecodeError, UnicodeDecodeError, ValueError):
            pass
    try:
        task_payload = dict(payload)
        artifact = _read_top_rankings_artifact_stream(
            path,
            payload=task_payload,
            include_retrieval_rankings=include_retrieval_rankings,
        )
        if artifact is not None:
            artifacts = dict(task_payload.get("artifacts", {}))
            artifacts["top_rankings"] = artifact
            task_payload["artifacts"] = artifacts
        return task_payload
    except (ijson.JSONError, UnicodeDecodeError, ValueError):
        return _read_result_json(path, include_retrieval_rankings=include_retrieval_rankings)


def _should_full_parse_result_json(path: Path) -> bool:
    try:
        return path.stat().st_size <= FULL_PARSE_RESULT_JSON_MAX_BYTES
    except OSError:
        return False


def _read_result_summary_payload(path: Path) -> dict[str, Any] | None:
    try:
        return _read_result_summary_json(path)
    except (ijson.JSONError, UnicodeDecodeError, ValueError):
        payload = _read_json(path)
        if not isinstance(payload, dict):
            return None
        summary_payload = dict(payload)
        summary_payload.pop("artifacts", None)
        return summary_payload


def _read_result_summary_payload_with_sha256(path: Path) -> tuple[dict[str, Any], str | None] | None:
    try:
        payload, payload_sha256 = _read_result_summary_json_with_sha256(path)
        return payload, payload_sha256
    except (ijson.JSONError, UnicodeDecodeError, ValueError):
        payload = _read_json(path)
        if not isinstance(payload, dict):
            return None
        summary_payload = dict(payload)
        summary_payload.pop("artifacts", None)
        return summary_payload, _payload_sha256(str(path))


class _JsonValueBuilder:
    def __init__(self) -> None:
        self._root: Any = None
        self._stack: list[list[Any]] = []

    def feed(self, event: str, value: Any) -> tuple[bool, Any]:
        if event == "start_map":
            container: dict[str, Any] = {}
            self._append(container)
            self._stack.append([container, None])
            return False, None
        if event == "start_array":
            container: list[Any] = []
            self._append(container)
            self._stack.append([container, None])
            return False, None
        if event == "map_key":
            if self._stack:
                self._stack[-1][1] = str(value)
            return False, None
        if event in {"string", "number", "boolean", "null"}:
            self._append(value)
            if not self._stack:
                return True, self._root
            return False, None
        if event in {"end_map", "end_array"}:
            if not self._stack:
                return True, self._root
            self._stack.pop()
            if not self._stack:
                return True, self._root
        return False, None

    def _append(self, value: Any) -> None:
        if not self._stack:
            self._root = value
            return
        parent, key = self._stack[-1]
        if isinstance(parent, list):
            parent.append(value)
            return
        if key is not None:
            parent[key] = value
            self._stack[-1][1] = None


def _read_result_summary_json(path: Path) -> dict[str, Any]:
    with _open_json_bytes(path) as file:
        return _read_result_summary_json_from_file(file)


def _read_result_summary_json_with_sha256(path: Path) -> tuple[dict[str, Any], str]:
    with _open_json_bytes_with_raw_sha256(path) as (file, digest):
        payload = _read_result_summary_json_from_file(file)
        for _ in iter(lambda: file.read(1024 * 1024), b""):
            pass
        return payload, digest.hexdigest()


def _read_result_summary_json_from_file(file: Any) -> dict[str, Any]:
    payload: dict[str, Any] = {}
    current_key: str | None = None
    builder: _JsonValueBuilder | None = None
    skipping_artifacts = False
    for prefix, event, value in ijson.parse(file, use_float=True):
        if prefix == "" and event == "start_map":
            continue
        if prefix == "" and event == "map_key":
            current_key = str(value)
            builder = None
            skipping_artifacts = current_key == "artifacts"
            continue
        if prefix == "" and event == "end_map":
            break
        if current_key is None or skipping_artifacts:
            continue
        if builder is None:
            builder = _JsonValueBuilder()
        done, result = builder.feed(event, value)
        if done:
            payload[current_key] = result
            current_key = None
            builder = None
    return payload


def _read_top_rankings_artifact_stream(
    path: Path,
    *,
    payload: dict[str, Any],
    include_retrieval_rankings: bool,
) -> dict[str, Any] | None:
    artifact: dict[str, Any] = {}
    qrels: list[Any] = []
    rankings: list[dict[str, Any]] = []
    qrel_builder: _JsonValueBuilder | None = None
    ranking_prefix = "artifacts.top_rankings.rankings.item"
    ranking_field_prefix = f"{ranking_prefix}."
    corpus_ids_prefix = f"{ranking_prefix}.corpus_ids"
    corpus_ids_item_prefix = f"{corpus_ids_prefix}.item"
    qrels_item_prefix = "artifacts.top_rankings.qrels.item"
    current_ranking: dict[str, Any] | None = None
    current_corpus_ids: list[Any] | None = None
    keep_current_ranking: bool | None = None
    collect_current_corpus_ids = False
    in_current_corpus_ids = False
    evaluation = payload.get("evaluation", {})
    if not isinstance(evaluation, dict):
        evaluation = {}
    embedding_evaluations = _embedding_evaluations(
        evaluation.get("embedding_evaluations") or payload.get("embedding_evaluations")
    )
    selection_context = _top_ranking_selection_context(
        evaluation=evaluation,
        embedding_evaluations=embedding_evaluations,
    )
    with _open_json_bytes(path) as file:
        for prefix, event, value in ijson.parse(file, use_float=True):
            if prefix in {
                "artifacts.top_rankings.schema_version",
                "artifacts.top_rankings.top_k",
                "artifacts.top_rankings.path",
            } and event in {"string", "number", "boolean", "null"}:
                artifact[prefix.rsplit(".", 1)[-1]] = value
                continue
            if qrel_builder is not None:
                done, qrel = qrel_builder.feed(event, value)
                if done:
                    qrels.append(qrel)
                    qrel_builder = None
                continue
            if prefix == qrels_item_prefix:
                if qrel_builder is None:
                    qrel_builder = _JsonValueBuilder()
                done, qrel = qrel_builder.feed(event, value)
                if done:
                    qrels.append(qrel)
                    qrel_builder = None
                continue
            if prefix == ranking_prefix and event == "start_map":
                current_ranking = {}
                current_corpus_ids = None
                keep_current_ranking = None
                collect_current_corpus_ids = False
                in_current_corpus_ids = False
                continue
            if current_ranking is None:
                continue
            if prefix == ranking_prefix and event == "end_map":
                if current_corpus_ids is not None:
                    current_ranking["corpus_ids"] = current_corpus_ids
                if keep_current_ranking is None:
                    keep_current_ranking = _keep_top_ranking_row(
                        current_ranking,
                        selection_context=selection_context,
                        include_retrieval_rankings=include_retrieval_rankings,
                    )
                if keep_current_ranking:
                    rankings.append(current_ranking)
                current_ranking = None
                current_corpus_ids = None
                keep_current_ranking = None
                collect_current_corpus_ids = False
                in_current_corpus_ids = False
                continue
            if prefix == corpus_ids_prefix and event == "start_array":
                fields_complete = _ranking_selection_fields_complete(current_ranking)
                if fields_complete:
                    keep_current_ranking = _keep_top_ranking_row(
                        current_ranking,
                        selection_context=selection_context,
                        include_retrieval_rankings=include_retrieval_rankings,
                    )
                collect_current_corpus_ids = not fields_complete or bool(keep_current_ranking)
                current_corpus_ids = [] if collect_current_corpus_ids else None
                in_current_corpus_ids = True
                continue
            if prefix == corpus_ids_prefix and event == "end_array":
                in_current_corpus_ids = False
                continue
            if in_current_corpus_ids:
                if collect_current_corpus_ids and prefix == corpus_ids_item_prefix and event in {
                    "string",
                    "number",
                    "boolean",
                    "null",
                }:
                    assert current_corpus_ids is not None
                    current_corpus_ids.append(value)
                continue
            if prefix.startswith(ranking_field_prefix) and event in {"string", "number", "boolean", "null"}:
                current_ranking[prefix[len(ranking_field_prefix) :]] = value
    if not qrels and not rankings and "path" not in artifact:
        return None
    artifact["qrels"] = qrels
    artifact["rankings"] = rankings
    return artifact


def _ranking_selection_fields_complete(ranking: dict[str, Any]) -> bool:
    return isinstance(ranking.get("ranking_kind"), str) and isinstance(ranking.get("score_name"), str)


@dataclass(frozen=True)
class TopRankingSelectionContext:
    retrieval_score_names: dict[str | None, str | None]
    best_rerank_score_name: str | None


def _top_ranking_selection_context(
    *,
    evaluation: dict[str, Any],
    embedding_evaluations: list[dict[str, Any]],
) -> TopRankingSelectionContext:
    return TopRankingSelectionContext(
        retrieval_score_names={
            _str_or_none(item.get("name")): _str_or_none(item.get("best_score_name"))
            for item in embedding_evaluations
            if isinstance(item, dict)
        },
        best_rerank_score_name=_best_rerank_score_name(evaluation),
    )


def _keep_top_ranking_row(
    ranking: Any,
    *,
    selection_context: TopRankingSelectionContext,
    include_retrieval_rankings: bool,
) -> bool:
    if not isinstance(ranking, dict):
        return False
    if include_retrieval_rankings:
        return True
    return _selected_metric_ranking(ranking, selection_context) is not None


@dataclass(frozen=True)
class SelectedResultJson:
    result_path: Path
    results_dir: Path
    source_priority: int
    payload: dict[str, Any]
    benchmark: str
    model_dir: str
    model_name: str
    dataset_id: str
    task_name: str
    task_key: str
    payload_sha256: str | None = None


@dataclass
class MemoryMonitor:
    log_path: Path | None = None
    sample_interval: int = 500
    _last_processed_count_by_label: dict[str, int] = field(default_factory=dict)

    def sample(self, label: str, *, processed_count: int | None = None) -> None:
        if self.log_path is None:
            return
        self.log_path.parent.mkdir(parents=True, exist_ok=True)
        row = {
            "timestamp_utc": datetime.now(timezone.utc).isoformat(),
            "label": label,
            "processed_count": processed_count,
            "current_rss_bytes": _current_rss_bytes(),
            "peak_rss_bytes": _peak_rss_bytes(),
        }
        with self.log_path.open("a", encoding="utf-8") as file:
            file.write(json.dumps(row, sort_keys=True) + "\n")

    def maybe_sample(self, label: str, *, processed_count: int) -> None:
        if self.log_path is None:
            return
        interval = max(1, self.sample_interval)
        last_processed_count = self._last_processed_count_by_label.get(label, -1)
        if (
            last_processed_count < 0
            or processed_count - last_processed_count >= interval
        ):
            self.sample(label, processed_count=processed_count)
            self._last_processed_count_by_label[label] = processed_count


def _current_rss_bytes() -> int | None:
    status_path = Path("/proc/self/status")
    if not status_path.exists():
        return None
    for line in status_path.read_text(encoding="utf-8").splitlines():
        if line.startswith("VmRSS:"):
            parts = line.split()
            if len(parts) >= 2 and parts[1].isdigit():
                return int(parts[1]) * 1024
    return None


def _peak_rss_bytes() -> int:
    peak = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
    return peak if sys.platform == "darwin" else peak * 1024


def build_arg_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--results-dir",
        type=Path,
        action="append",
        default=None,
        help=(
            "Benchmark result directory. May be supplied multiple times; when duplicate task JSON exists, "
            "earlier directories take priority."
        ),
    )
    parser.add_argument(
        "--overwrite-result-duplicates",
        action="store_true",
        help=(
            "When repeated --results-dir roots contain duplicate logical model-task results, "
            "let later directories overwrite earlier directories."
        ),
    )
    parser.add_argument(
        "--append-results-dir",
        type=Path,
        action="append",
        default=None,
        help=(
            "Append new benchmark result JSON from this directory into an existing DuckDB without scanning "
            "the original result roots. May be supplied multiple times."
        ),
    )
    parser.add_argument(
        "--append-base-duckdb",
        default=None,
        help=(
            "Base DuckDB to append into before writing --append-output-duckdb, "
            "or 'latest' to download the configured Hugging Face dataset DuckDB."
        ),
    )
    parser.add_argument(
        "--append-output-duckdb",
        type=Path,
        default=None,
        help="Write append results to a copy of --append-base-duckdb instead of updating the base DuckDB in place.",
    )
    parser.add_argument(
        "--append-hf-dataset-repo-id",
        default=None,
        help=(
            "Hugging Face dataset repo used when --append-base-duckdb=latest or when append mode needs "
            "to initialize a missing target DuckDB. Defaults to HAKARI_BENCH_VIEWER_HF_DATASET_REPO_ID."
        ),
    )
    parser.add_argument(
        "--append-hf-dataset-path",
        default=DEFAULT_HF_DUCKDB_PATH,
        help="DuckDB file path inside the Hugging Face dataset repo for --append-base-duckdb=latest.",
    )
    parser.add_argument(
        "--append-hf-dataset-revision",
        default=None,
        help="Optional Hugging Face dataset revision used when --append-base-duckdb=latest.",
    )
    parser.add_argument("--duckdb-path", type=Path, default=DEFAULT_DUCKDB_PATH)
    parser.add_argument(
        "--html-output",
        type=Path,
        default=None,
        help="Optional static HTML report path. DuckDB generation does not require this.",
    )
    parser.add_argument(
        "--viewer-config-dir",
        type=Path,
        default=DEFAULT_VIEWER_CONFIG_DIR,
        help="Directory containing viewer benchmark and overall YAML configuration.",
    )
    parser.add_argument(
        "--model-cards-path",
        type=Path,
        default=DEFAULT_MODEL_CARDS_PATH,
        help="Static model metadata YAML file or directory used to backfill missing result JSON metadata.",
    )
    parser.add_argument(
        "--parquet-output-dir",
        type=Path,
        default=None,
        help="Optional directory for Parquet snapshots of the canonical DuckDB tables.",
    )
    parser.add_argument(
        "--include-retrieval-rankings",
        action="store_true",
        help="Load optional top-ranking artifacts into retrieval_rankings. Disabled by default for faster viewer builds.",
    )
    parser.add_argument(
        "--include-result-extensions",
        action="store_true",
        help="Discover unknown top-level result JSON fields. Disabled by default for faster viewer builds.",
    )
    parser.add_argument(
        "--incremental",
        action="store_true",
        help="Reuse unchanged canonical rows from the existing DuckDB database when possible.",
    )
    parser.add_argument(
        "--stream-results-to-duckdb",
        action="store_true",
        help=(
            "Write parsed result rows to DuckDB in chunks instead of materializing all warehouse rows "
            "in Python memory. This is the default for builds without --html-output."
        ),
    )
    parser.add_argument(
        "--materialize-results-in-python",
        action="store_true",
        help="Use the legacy Python-materialized build path. This is mainly useful for static HTML output.",
    )
    parser.add_argument(
        "--memory-log-path",
        type=Path,
        default=None,
        help="Optional JSONL path for RSS/peak RSS samples while result JSON is selected and loaded.",
    )
    parser.add_argument(
        "--memory-log-interval",
        type=int,
        default=500,
        help="Number of parsed result JSON files between memory samples when --memory-log-path is set.",
    )
    parser.add_argument(
        "--result-selection-workers",
        type=int,
        default=None,
        help=(
            "Number of worker processes used to read result JSON summaries during candidate selection. "
            "Defaults to physical CPU cores minus one."
        ),
    )
    parser.add_argument(
        "--result-json-workers",
        type=int,
        default=None,
        help=(
            "Number of worker processes used to parse selected result JSON files. "
            "Defaults to physical CPU cores minus one when neither this option nor --result-row-workers is set. "
            "Use 1 for serial parsing."
        ),
    )
    parser.add_argument(
        "--result-row-workers",
        type=int,
        default=None,
        help=(
            "Number of worker processes used to parse selected result JSON and build per-file warehouse rows. "
            "Defaults to physical CPU cores minus one. When greater than 1, this supersedes --result-json-workers."
        ),
    )
    parser.add_argument(
        "--exclude-model-name",
        action="append",
        default=None,
        help="Model name to exclude from the generated DuckDB. May be supplied multiple times.",
    )
    parser.add_argument(
        "--model-name-override",
        default=None,
        help=(
            "Override model_name for loaded result JSON rows. Intended for local experiment paths such as "
            "local/model_exp_122; use only when the input dirs represent one logical model."
        ),
    )
    return parser


def resolve_warehouse_build_plan(args: argparse.Namespace) -> WarehouseBuildPlan:
    result_workers = resolve_result_worker_counts(
        result_selection_workers=args.result_selection_workers,
        result_json_workers=args.result_json_workers,
        result_row_workers=args.result_row_workers,
    )
    if args.append_results_dir:
        if args.results_dir is not None:
            raise ValueError("--append-results-dir cannot be combined with --results-dir")
        if args.overwrite_result_duplicates:
            raise ValueError("--append-results-dir cannot be combined with --overwrite-result-duplicates")
        if args.html_output is not None:
            raise ValueError("--append-results-dir does not support --html-output")
        if args.include_result_extensions:
            raise ValueError("--append-results-dir does not support --include-result-extensions")
        if args.append_output_duckdb is not None and args.append_base_duckdb is None:
            raise ValueError("--append-output-duckdb requires --append-base-duckdb")
        mode: WarehouseBuildMode = "append"
        results_dirs: list[Path] = []
        append_results_dirs = list(args.append_results_dir)
        append_base_duckdb = _append_base_duckdb_arg(args.append_base_duckdb)
        duckdb_path = args.append_output_duckdb or args.duckdb_path
    else:
        if args.stream_results_to_duckdb and args.html_output is not None:
            raise ValueError("--stream-results-to-duckdb cannot be combined with --html-output")
        if args.stream_results_to_duckdb and args.materialize_results_in_python:
            raise ValueError("--stream-results-to-duckdb cannot be combined with --materialize-results-in-python")
        mode = "materialized" if args.html_output is not None or args.materialize_results_in_python else "stream"
        results_dirs = list(args.results_dir or [DEFAULT_RESULTS_DIR])
        append_results_dirs = []
        append_base_duckdb = None
        duckdb_path = args.duckdb_path

    duplicate_result_policy: DuplicateResultPolicy = (
        "last-wins" if args.overwrite_result_duplicates else "first-wins"
    )
    return WarehouseBuildPlan(
        mode=mode,
        results_dirs=results_dirs,
        append_results_dirs=append_results_dirs,
        duckdb_path=duckdb_path,
        append_base_duckdb=append_base_duckdb,
        append_hf_dataset_repo_id=args.append_hf_dataset_repo_id,
        append_hf_dataset_path=args.append_hf_dataset_path,
        append_hf_dataset_revision=args.append_hf_dataset_revision,
        html_output=args.html_output,
        viewer_config_dir=args.viewer_config_dir,
        model_cards_path=args.model_cards_path,
        parquet_output_dir=args.parquet_output_dir,
        include_retrieval_rankings=args.include_retrieval_rankings,
        include_result_extensions=args.include_result_extensions,
        incremental=args.incremental,
        duplicate_result_policy=duplicate_result_policy,
        result_workers=result_workers,
        exclude_model_names=set(args.exclude_model_name or []),
        model_name_override=args.model_name_override,
    )


def _append_base_duckdb_arg(value: str | None) -> AppendBaseDuckDb | None:
    if value is None:
        return None
    if value == "latest":
        return "latest"
    return Path(value)


def run_warehouse_build(plan: WarehouseBuildPlan, *, memory_monitor: MemoryMonitor) -> None:
    viewer_config = load_viewer_config(plan.viewer_config_dir)
    benchmark_configs = viewer_config.benchmarks
    target_benchmarks = target_benchmark_names(benchmark_configs)
    if plan.mode == "append":
        _prepare_append_duckdb(plan)
        rows, _, metric_rows, diagnostic_rows, dataset_metadata_rows, ranking_rows, source_hashes = _load_results_for_plan(
            plan,
            plan.append_results_dirs,
            benchmark_configs=benchmark_configs,
            memory_monitor=memory_monitor,
            include_source_hashes=True,
        )
        append_duckdb_results(
            plan.duckdb_path,
            rows=rows,
            metric_rows=metric_rows,
            diagnostic_rows=diagnostic_rows,
            dataset_metadata_rows=dataset_metadata_rows,
            ranking_rows=ranking_rows,
            source_payload_sha256_by_path=source_hashes,
        )
        build_viewer_leaderboard_mart(
            plan.duckdb_path,
            viewer_config=viewer_config,
            view_names=[overall.name for overall in viewer_config.overalls],
        )
        if plan.parquet_output_dir is not None:
            export_duckdb_tables_to_parquet(plan.duckdb_path, plan.parquet_output_dir)
        memory_monitor.sample("complete")
        return
    # For deploy builds with no secondary artifacts requested, unchanged input
    # can return immediately after hash validation; rewriting the same DB would
    # dominate the incremental path.
    if (
        plan.incremental
        and plan.duplicate_result_policy == "first-wins"
        and plan.html_output is None
        and plan.parquet_output_dir is None
        and not plan.include_retrieval_rankings
        and not plan.include_result_extensions
        and _incremental_cache_current(
            _current_source_hashes(plan.results_dirs),
            plan.duckdb_path,
            model_cards_path=plan.model_cards_path,
        )
    ):
        memory_monitor.sample("incremental_cache_current")
        return
    if plan.mode == "stream":
        write_duckdb_streaming_results(
            plan.results_dirs,
            plan.duckdb_path,
            benchmark_configs=benchmark_configs,
            include_retrieval_rankings=plan.include_retrieval_rankings,
            model_cards_path=plan.model_cards_path,
            exclude_model_names=plan.exclude_model_names,
            model_name_override=plan.model_name_override,
            duplicate_result_policy=plan.duplicate_result_policy,
            memory_monitor=memory_monitor,
            result_selection_workers=plan.result_workers.selection,
            result_json_workers=plan.result_workers.json,
            result_row_workers=plan.result_workers.row,
            include_result_extensions=plan.include_result_extensions,
        )
        build_viewer_leaderboard_mart(
            plan.duckdb_path,
            viewer_config=viewer_config,
            view_names=[overall.name for overall in viewer_config.overalls],
        )
        if plan.parquet_output_dir is not None:
            export_duckdb_tables_to_parquet(plan.duckdb_path, plan.parquet_output_dir)
        memory_monitor.sample("complete")
        return

    rows, runs, metric_rows, diagnostic_rows, dataset_metadata_rows, ranking_rows, source_hashes = _load_results_for_plan(
        plan,
        plan.results_dirs,
        benchmark_configs=benchmark_configs,
        incremental_db_path=plan.duckdb_path if plan.incremental and plan.duplicate_result_policy == "first-wins" else None,
        memory_monitor=memory_monitor,
        include_source_hashes=True,
    )
    base_rows: list[TaskResultRow] = []
    standings: dict[str, list[dict[str, Any]]] = {}
    borda_rows: list[dict[str, Any]] = []
    if plan.html_output is not None:
        base_rows = [row for row in rows if row.embedding_variant_name is None]
        standings, borda_rows = compute_standings(base_rows, target_benchmarks=target_benchmarks)
    write_duckdb(
        plan.duckdb_path,
        runs=runs,
        rows=rows,
        metric_rows=metric_rows,
        diagnostic_rows=diagnostic_rows,
        dataset_metadata_rows=dataset_metadata_rows,
        ranking_rows=ranking_rows,
        standings=standings,
        borda_rows=borda_rows,
        include_result_extensions=plan.include_result_extensions,
        model_cards_path=plan.model_cards_path,
        source_payload_sha256_by_path=source_hashes,
    )
    build_viewer_leaderboard_mart(
        plan.duckdb_path,
        viewer_config=viewer_config,
        view_names=[overall.name for overall in viewer_config.overalls],
    )
    if plan.parquet_output_dir is not None:
        export_duckdb_tables_to_parquet(plan.duckdb_path, plan.parquet_output_dir)
    if plan.html_output is not None:
        write_html(
            plan.html_output,
            duckdb_path=plan.duckdb_path,
            rows=base_rows,
            runs=runs,
            standings=standings,
            target_benchmarks=target_benchmarks,
        )
    memory_monitor.sample("complete")


def _prepare_append_duckdb(plan: WarehouseBuildPlan) -> None:
    if plan.append_base_duckdb is None:
        if plan.duckdb_path.exists():
            return
        source = _resolve_latest_append_duckdb(plan)
    else:
        source = _resolve_append_base_duckdb(plan)
    if not source.exists():
        raise FileNotFoundError(f"Cannot append results because base DuckDB does not exist: {source}")
    if source.resolve() == plan.duckdb_path.resolve():
        return
    plan.duckdb_path.parent.mkdir(parents=True, exist_ok=True)
    temp_path = plan.duckdb_path.with_suffix(plan.duckdb_path.suffix + ".tmp")
    shutil.copy2(source, temp_path)
    temp_path.replace(plan.duckdb_path)


def _resolve_append_base_duckdb(plan: WarehouseBuildPlan) -> Path:
    if plan.append_base_duckdb == "latest":
        return _resolve_latest_append_duckdb(plan)
    if isinstance(plan.append_base_duckdb, Path):
        return plan.append_base_duckdb
    raise ValueError(f"Unsupported append base DuckDB: {plan.append_base_duckdb!r}")


def _resolve_latest_append_duckdb(plan: WarehouseBuildPlan) -> Path:
    repo_id = plan.append_hf_dataset_repo_id or os.getenv("HAKARI_BENCH_VIEWER_HF_DATASET_REPO_ID")
    if not repo_id:
        raise ValueError(
            "Appending to a missing DuckDB requires --append-hf-dataset-repo-id, "
            "--append-base-duckdb=latest with that repo id, or HAKARI_BENCH_VIEWER_HF_DATASET_REPO_ID"
        )
    return _download_hf_duckdb(
        HuggingFaceDuckDbSource(
            repo_id=repo_id,
            filename=plan.append_hf_dataset_path,
            revision=plan.append_hf_dataset_revision,
        )
    )


def main() -> None:
    parser = build_arg_parser()
    args = parser.parse_args()
    try:
        plan = resolve_warehouse_build_plan(args)
    except ValueError as exc:
        parser.error(str(exc))

    memory_monitor = MemoryMonitor(
        log_path=args.memory_log_path,
        sample_interval=args.memory_log_interval,
    )
    memory_monitor.sample("start", processed_count=0)
    run_warehouse_build(plan, memory_monitor=memory_monitor)


LoadResultsPayload = tuple[
    list[TaskResult],
    list[dict[str, Any]],
    list[MetricLongRow],
    list[TaskDiagnosticRow],
    list[DatasetMetadataRow],
    list[RetrievalRankingRow],
]
LoadResultsPayloadWithSourceHashes = tuple[
    list[TaskResult],
    list[dict[str, Any]],
    list[MetricLongRow],
    list[TaskDiagnosticRow],
    list[DatasetMetadataRow],
    list[RetrievalRankingRow],
    dict[str, str | None],
]


@overload
def _load_results_for_plan(
    plan: WarehouseBuildPlan,
    results_dir: Path | Sequence[Path],
    *,
    benchmark_configs: Sequence[BenchmarkConfig],
    memory_monitor: MemoryMonitor | None,
    incremental_db_path: Path | None = None,
    include_source_hashes: Literal[False] = False,
) -> LoadResultsPayload: ...


@overload
def _load_results_for_plan(
    plan: WarehouseBuildPlan,
    results_dir: Path | Sequence[Path],
    *,
    benchmark_configs: Sequence[BenchmarkConfig],
    memory_monitor: MemoryMonitor | None,
    incremental_db_path: Path | None = None,
    include_source_hashes: Literal[True],
) -> LoadResultsPayloadWithSourceHashes: ...


def _load_results_for_plan(
    plan: WarehouseBuildPlan,
    results_dir: Path | Sequence[Path],
    *,
    benchmark_configs: Sequence[BenchmarkConfig],
    memory_monitor: MemoryMonitor | None,
    incremental_db_path: Path | None = None,
    include_source_hashes: bool = False,
) -> LoadResultsPayload | LoadResultsPayloadWithSourceHashes:
    return load_results(
        results_dir,
        benchmark_configs=benchmark_configs,
        include_retrieval_rankings=plan.include_retrieval_rankings,
        incremental_db_path=incremental_db_path,
        model_cards_path=plan.model_cards_path,
        exclude_model_names=plan.exclude_model_names,
        model_name_override=plan.model_name_override,
        duplicate_result_policy=plan.duplicate_result_policy,
        memory_monitor=memory_monitor,
        result_selection_workers=plan.result_workers.selection,
        result_json_workers=plan.result_workers.json,
        result_row_workers=plan.result_workers.row,
        include_source_hashes=include_source_hashes,
    )


@overload
def load_results(
    results_dir: Path | Sequence[Path],
    *,
    benchmark_configs: Sequence[BenchmarkConfig] | None = None,
    include_retrieval_rankings: bool = False,
    incremental_db_path: Path | None = None,
    model_cards_path: Path | None = DEFAULT_MODEL_CARDS_PATH,
    exclude_model_names: set[str] | None = None,
    model_name_override: str | None = None,
    duplicate_result_policy: DuplicateResultPolicy = "first-wins",
    memory_monitor: MemoryMonitor | None = None,
    result_selection_workers: int = 1,
    result_json_workers: int = 1,
    result_row_workers: int = 1,
    include_source_hashes: Literal[False] = False,
) -> LoadResultsPayload: ...


@overload
def load_results(
    results_dir: Path | Sequence[Path],
    *,
    benchmark_configs: Sequence[BenchmarkConfig] | None = None,
    include_retrieval_rankings: bool = False,
    incremental_db_path: Path | None = None,
    model_cards_path: Path | None = DEFAULT_MODEL_CARDS_PATH,
    exclude_model_names: set[str] | None = None,
    model_name_override: str | None = None,
    duplicate_result_policy: DuplicateResultPolicy = "first-wins",
    memory_monitor: MemoryMonitor | None = None,
    result_selection_workers: int = 1,
    result_json_workers: int = 1,
    result_row_workers: int = 1,
    include_source_hashes: Literal[True] = True,
) -> LoadResultsPayloadWithSourceHashes: ...


def load_results(
    results_dir: Path | Sequence[Path],
    *,
    benchmark_configs: Sequence[BenchmarkConfig] | None = None,
    include_retrieval_rankings: bool = False,
    incremental_db_path: Path | None = None,
    model_cards_path: Path | None = DEFAULT_MODEL_CARDS_PATH,
    exclude_model_names: set[str] | None = None,
    model_name_override: str | None = None,
    duplicate_result_policy: DuplicateResultPolicy = "first-wins",
    memory_monitor: MemoryMonitor | None = None,
    result_selection_workers: int = 1,
    result_json_workers: int = 1,
    result_row_workers: int = 1,
    include_source_hashes: bool = False,
) -> LoadResultsPayload | LoadResultsPayloadWithSourceHashes:
    rows: list[TaskResult] = []
    run_accumulators: dict[str, dict[str, Any]] = {}
    metric_rows: list[MetricLongRow] = []
    diagnostic_rows: list[TaskDiagnosticRow] = []
    dataset_metadata_rows: list[DatasetMetadataRow] = []
    ranking_rows: list[RetrievalRankingRow] = []
    selected_result_path_filter: set[str] | None = None
    rebuild_runs_from_rows = False
    if duplicate_result_policy == "last-wins":
        # The incremental cache is keyed by source paths and payload hashes, not
        # by duplicate resolution policy. Rebuild so a policy change cannot keep
        # stale first-wins rows.
        incremental_db_path = None
    if incremental_db_path is not None and not include_retrieval_rankings:
        # Incremental reuse is keyed by source path and payload hash. Removed
        # paths fall back to the full parser so stale rows cannot leak into the
        # regenerated warehouse. Added paths can be parsed alongside changed
        # paths while unchanged rows are loaded from the previous DuckDB.
        current_hashes = _current_source_hashes(results_dir)
        previous_hashes = _read_previous_source_hashes(incremental_db_path)
        current_paths = set(current_hashes)
        previous_paths = set(previous_hashes)
        if (
            current_hashes
            and previous_paths.issubset(current_paths)
            and _incremental_cache_schema_compatible(incremental_db_path)
            and _model_cards_cache_current(incremental_db_path, model_cards_path=model_cards_path)
        ):
            changed_paths = {
                path
                for path in previous_paths
                if current_hashes.get(path) != previous_hashes[path]
            }
            added_paths = current_paths - previous_paths
            if not include_source_hashes and not changed_paths and not added_paths and (
                cached_results := _load_results_from_incremental_cache(
                    results_dir,
                    db_path=incremental_db_path,
                    include_retrieval_rankings=include_retrieval_rankings,
                    model_cards_path=model_cards_path,
                )
            ) is not None:
                return cached_results
            unchanged_paths = previous_paths - changed_paths
            cached_rows = _load_cached_warehouse_rows(
                incremental_db_path,
                result_paths=unchanged_paths,
                include_retrieval_rankings=False,
            )
            if cached_rows is not None:
                # Keep canonical rows for unchanged files and parse only the
                # changed JSON. Run summaries are rebuilt from the merged rows
                # because cached run aggregates no longer match after changes.
                rows, _, metric_rows, diagnostic_rows, dataset_metadata_rows, ranking_rows = cached_rows
                selected_result_path_filter = changed_paths | added_paths
                rebuild_runs_from_rows = True
    registry = DatasetRegistry.load_builtin()
    benchmark_configs = list(benchmark_configs or load_benchmark_configs())
    target_benchmarks = set(target_benchmark_names(benchmark_configs))
    model_cards = load_model_cards(model_cards_path)
    exclude_model_names = exclude_model_names or set()

    selected_results = _selected_result_jsons(
        results_dir,
        benchmark_configs=benchmark_configs,
        target_benchmarks=target_benchmarks,
        exclude_model_names=exclude_model_names,
        result_paths=selected_result_path_filter,
        duplicate_result_policy=duplicate_result_policy,
        include_retrieval_rankings=include_retrieval_rankings,
        memory_monitor=memory_monitor,
        result_selection_workers=result_selection_workers,
        model_name_override=model_name_override,
    )
    processed_result_count = 0
    for processed in _processed_result_rows(
        selected_results,
        registry=registry,
        model_cards=model_cards,
        model_cards_path=model_cards_path,
        include_retrieval_rankings=include_retrieval_rankings,
        result_json_workers=result_json_workers,
        result_row_workers=result_row_workers,
    ):
        if processed is None:
            continue
        processed_result_count += 1
        if memory_monitor is not None:
            memory_monitor.maybe_sample("result_json_loaded", processed_count=processed_result_count)
        _merge_run_accumulators(run_accumulators, processed.run_accumulators)
        rows.extend(processed.rows)
        metric_rows.extend(processed.metric_rows)
        diagnostic_rows.extend(processed.diagnostic_rows)
        dataset_metadata_rows.extend(processed.dataset_metadata_rows)
        ranking_rows.extend(processed.ranking_rows)

    deduped_rows = _dedupe_task_results(rows)
    if memory_monitor is not None:
        memory_monitor.sample("load_results_complete", processed_count=len(rows))
    result_payload = (
        deduped_rows,
        _runs_from_task_result_rows(deduped_rows) if rebuild_runs_from_rows else _runs_from_task_results(run_accumulators),
        _dedupe_metric_rows(metric_rows),
        _dedupe_task_diagnostic_rows(diagnostic_rows),
        _dedupe_dataset_metadata_rows(dataset_metadata_rows),
        _dedupe_retrieval_ranking_rows(ranking_rows),
    )
    if not include_source_hashes:
        return result_payload
    source_hashes: dict[str, str | None] = {
        str(selected.result_path): selected.payload_sha256
        for selected in selected_results
    }
    return (*result_payload, source_hashes)


@dataclass
class ProcessedResultRows:
    rows: list[TaskResult]
    run_accumulators: dict[str, dict[str, Any]]
    metric_rows: list[MetricLongRow]
    diagnostic_rows: list[TaskDiagnosticRow]
    dataset_metadata_rows: list[DatasetMetadataRow]
    ranking_rows: list[RetrievalRankingRow]


def _load_results_from_incremental_cache(
    results_dir: Path | Sequence[Path],
    *,
    db_path: Path,
    include_retrieval_rankings: bool,
    model_cards_path: Path | None,
) -> LoadResultsPayload | None:
    # Ranking artifacts can be much larger than the summary rows and may be
    # requested with different flags, so the cached fast path handles only the
    # default viewer warehouse.
    if include_retrieval_rankings or not db_path.exists():
        return None
    current_hashes = _current_source_hashes(results_dir)
    if not _incremental_cache_current(current_hashes, db_path, model_cards_path=model_cards_path):
        return None
    return _load_cached_warehouse_rows(
        db_path,
        result_paths=None,
        include_retrieval_rankings=include_retrieval_rankings,
    )


def _load_cached_warehouse_rows(
    db_path: Path,
    *,
    result_paths: set[str] | None,
    include_retrieval_rankings: bool,
) -> LoadResultsPayload | None:
    # result_paths=None means a fully unchanged build; otherwise only unchanged
    # source rows are loaded and changed files are parsed by load_results().
    con = duckdb.connect(str(db_path), read_only=True)
    try:
        required_tables = ("meta_database", "runs", "task_results", "metrics_long", "task_diagnostics", "dataset_metadata")
        if not all(_duckdb_table_exists(con, table) for table in required_tables):
            return None
        if con.execute("SELECT schema_version FROM meta_database").fetchone() != (WAREHOUSE_SCHEMA_VERSION,):
            return None
        rows = _filter_rows_by_result_path(_fetch_task_result_rows(con), result_paths)
        runs = _fetch_dict_rows(con, "runs")
        metric_rows = _fetch_model_rows(
            con,
            "metrics_long",
            MetricLongRow,
            METRIC_LONG_COLUMNS,
        )
        metric_rows = _filter_rows_by_result_path(metric_rows, result_paths)
        diagnostic_rows = _fetch_model_rows(
            con,
            "task_diagnostics",
            TaskDiagnosticRow,
            (
                "model_dir",
                "model_name",
                "benchmark",
                "dataset_id",
                "task_name",
                "task_key",
                "result_path",
                "base_score",
                "rerank_score",
                "rerank_lift",
                "rerank_status",
                "rerank_top_k",
                "candidate_source",
                "candidate_ranking",
                "bm25_source",
                "query_coverage",
                "relevant_coverage",
                "covered_query_count",
                "query_with_relevance_count",
                "covered_relevant_count",
                "relevant_count",
                "dataset_load_seconds",
                "query_embedding_seconds",
                "corpus_embedding_seconds",
                "score_and_topk_seconds",
                "metric_compute_seconds",
                "pure_compute_seconds",
                "wall_seconds",
                "duration_seconds_including_dataset_load",
            ),
        )
        diagnostic_rows = _filter_rows_by_result_path(diagnostic_rows, result_paths)
        dataset_metadata_rows = _fetch_model_rows(
            con,
            "dataset_metadata",
            DatasetMetadataRow,
            (
                "benchmark",
                "dataset_id",
                "dataset_name",
                "split_name",
                "task_name",
                "task_key",
                "language",
                "languages",
                "primary_languages",
                "category",
                "short_description",
                "citation_count",
                "reference_count",
                "has_bibtex",
                "query_count",
                "document_count",
                "query_mean_chars",
                "document_mean_chars",
            ),
        )
        ranking_rows: list[RetrievalRankingRow] = []
        if include_retrieval_rankings and _duckdb_table_exists(con, "retrieval_rankings"):
            ranking_rows = _filter_rows_by_result_path(
                _fetch_model_rows(
                    con,
                    "retrieval_rankings",
                    RetrievalRankingRow,
                    (
                        "model_dir",
                        "model_name",
                        "benchmark",
                        "dataset_id",
                        "dataset_revision",
                        "dataset_name",
                        "split_name",
                        "task_name",
                        "task_key",
                        "result_path",
                        "ranking_path",
                        "ranking_name",
                        "ranking_kind",
                        "embedding_variant_name",
                        "distance",
                        "score_name",
                        "query_id",
                        "rank",
                        "corpus_id",
                    ),
                ),
                result_paths,
            )
        return rows, runs, metric_rows, diagnostic_rows, dataset_metadata_rows, ranking_rows
    finally:
        con.close()


async def _ordered_async_bounded_map(
    items: Sequence[Any],
    submit: Callable[[Any], Awaitable[Any]],
    *,
    max_pending: int,
) -> AsyncIterable[Any]:
    next_submit_index = 0
    next_yield_index = 0
    pending: dict[asyncio.Task[Any], int] = {}
    completed: dict[int, Any] = {}
    pending_limit = max(1, max_pending)
    while next_submit_index < len(items) and len(pending) < pending_limit:
        task = asyncio.ensure_future(submit(items[next_submit_index]))
        pending[task] = next_submit_index
        next_submit_index += 1
    while pending:
        done, _ = await asyncio.wait(pending, return_when=asyncio.FIRST_COMPLETED)
        for task in done:
            result_index = pending.pop(task)
            completed[result_index] = task.result()
            while next_submit_index < len(items) and len(pending) < pending_limit:
                next_task = asyncio.ensure_future(submit(items[next_submit_index]))
                pending[next_task] = next_submit_index
                next_submit_index += 1
        while next_yield_index in completed:
            yield completed.pop(next_yield_index)
            next_yield_index += 1


def _iterate_async(async_iterable: AsyncIterable[Any]) -> Iterable[Any]:
    loop = asyncio.new_event_loop()
    previous_loop: asyncio.AbstractEventLoop | None
    try:
        previous_loop = asyncio.get_running_loop()
    except RuntimeError:
        previous_loop = None
    asyncio.set_event_loop(loop)
    iterator = async_iterable.__aiter__()
    try:
        while True:
            try:
                yield loop.run_until_complete(iterator.__anext__())
            except StopAsyncIteration:
                break
    finally:
        close = getattr(iterator, "aclose", None)
        if close is not None:
            loop.run_until_complete(close())
        loop.run_until_complete(loop.shutdown_asyncgens())
        loop.close()
        asyncio.set_event_loop(previous_loop)


async def _async_loaded_result_payloads(
    selected_results: Sequence[SelectedResultJson],
    *,
    include_retrieval_rankings: bool,
    workers: int,
) -> AsyncIterable[tuple[SelectedResultJson, dict[str, Any] | None]]:
    workers = max(1, workers)
    if workers == 1 or len(selected_results) <= 1:
        for selected_result in selected_results:
            yield (
                selected_result,
                _read_result_json_from_summary(
                    selected_result.result_path,
                    payload=selected_result.payload,
                    include_retrieval_rankings=include_retrieval_rankings,
                ),
            )
        return

    loop = asyncio.get_running_loop()
    with ProcessPoolExecutor(max_workers=workers) as executor:
        async def submit(selected_result: SelectedResultJson) -> tuple[SelectedResultJson, dict[str, Any] | None]:
            payload = await loop.run_in_executor(
                executor,
                _read_result_json_from_summary_worker,
                str(selected_result.result_path),
                selected_result.payload,
                include_retrieval_rankings,
            )
            return selected_result, payload

        async for item in _ordered_async_bounded_map(
            selected_results,
            submit,
            max_pending=workers * 2,
        ):
            yield item


def _read_result_json_worker(path: str, include_retrieval_rankings: bool) -> dict[str, Any] | None:
    return _read_result_json(Path(path), include_retrieval_rankings=include_retrieval_rankings)


def _read_result_json_from_summary_worker(
    path: str,
    payload: dict[str, Any],
    include_retrieval_rankings: bool,
) -> dict[str, Any] | None:
    return _read_result_json_from_summary(
        Path(path),
        payload=payload,
        include_retrieval_rankings=include_retrieval_rankings,
    )


def _processed_result_rows(
    selected_results: Sequence[SelectedResultJson],
    *,
    registry: DatasetRegistry,
    model_cards: dict[str, dict[str, Any]],
    model_cards_path: Path | None,
    include_retrieval_rankings: bool,
    result_json_workers: int,
    result_row_workers: int,
) -> Iterable[ProcessedResultRows | None]:
    yield from _iterate_async(
        _async_processed_result_rows(
            selected_results,
            registry=registry,
            model_cards=model_cards,
            model_cards_path=str(model_cards_path) if model_cards_path is not None else None,
            include_retrieval_rankings=include_retrieval_rankings,
            result_json_workers=result_json_workers,
            result_row_workers=result_row_workers,
        )
    )


async def _async_processed_result_rows(
    selected_results: Sequence[SelectedResultJson],
    *,
    registry: DatasetRegistry,
    model_cards: dict[str, dict[str, Any]],
    include_retrieval_rankings: bool,
    model_cards_path: str | None,
    result_json_workers: int,
    result_row_workers: int,
) -> AsyncIterable[ProcessedResultRows | None]:
    workers = max(1, result_row_workers)
    if workers == 1 or len(selected_results) <= 1:
        async for selected_result, task_payload in _async_loaded_result_payloads(
            selected_results,
            include_retrieval_rankings=include_retrieval_rankings,
            workers=result_json_workers,
        ):
            if task_payload is None:
                yield None
                continue
            yield _process_result_rows(
                selected_result=selected_result,
                task_payload=task_payload,
                registry=registry,
                model_cards=model_cards,
                include_retrieval_rankings=include_retrieval_rankings,
            )
        return

    loop = asyncio.get_running_loop()
    with ProcessPoolExecutor(max_workers=workers) as executor:
        async def submit(selected_result: SelectedResultJson) -> ProcessedResultRows | None:
            return await loop.run_in_executor(
                executor,
                _process_result_rows_worker,
                selected_result,
                include_retrieval_rankings,
                model_cards_path,
            )

        async for item in _ordered_async_bounded_map(
            selected_results,
            submit,
            max_pending=workers * 2,
        ):
            yield item


_WORKER_REGISTRY: DatasetRegistry | None = None
_WORKER_MODEL_CARDS: dict[str, dict[str, Any]] | None = None
_WORKER_MODEL_CARDS_PATH: str | None = None


def _worker_registry() -> DatasetRegistry:
    global _WORKER_REGISTRY
    if _WORKER_REGISTRY is None:
        _WORKER_REGISTRY = DatasetRegistry.load_builtin()
    return _WORKER_REGISTRY


def _worker_model_cards(model_cards_path: str | None) -> dict[str, dict[str, Any]]:
    global _WORKER_MODEL_CARDS, _WORKER_MODEL_CARDS_PATH
    if _WORKER_MODEL_CARDS is None or _WORKER_MODEL_CARDS_PATH != model_cards_path:
        _WORKER_MODEL_CARDS = load_model_cards(Path(model_cards_path) if model_cards_path is not None else None)
        _WORKER_MODEL_CARDS_PATH = model_cards_path
    return _WORKER_MODEL_CARDS


def _process_result_rows_worker(
    selected_result: SelectedResultJson,
    include_retrieval_rankings: bool,
    model_cards_path: str | None,
) -> ProcessedResultRows | None:
    task_payload = _read_result_json_from_summary(
        selected_result.result_path,
        payload=selected_result.payload,
        include_retrieval_rankings=include_retrieval_rankings,
    )
    if task_payload is None:
        return None
    return _process_result_rows(
        selected_result=selected_result,
        task_payload=task_payload,
        registry=_worker_registry(),
        model_cards=_worker_model_cards(model_cards_path),
        include_retrieval_rankings=include_retrieval_rankings,
    )


def _process_result_rows(
    *,
    selected_result: SelectedResultJson,
    task_payload: dict[str, Any],
    registry: DatasetRegistry,
    model_cards: dict[str, dict[str, Any]],
    include_retrieval_rankings: bool,
) -> ProcessedResultRows:
    rows: list[TaskResult] = []
    run_accumulators: dict[str, dict[str, Any]] = {}
    metric_rows: list[MetricLongRow] = []
    diagnostic_rows: list[TaskDiagnosticRow] = []
    dataset_metadata_rows: list[DatasetMetadataRow] = []
    ranking_rows: list[RetrievalRankingRow] = []
    result_path = selected_result.result_path
    target = task_payload["target"]
    benchmark = selected_result.benchmark
    evaluation = task_payload["evaluation"]
    config = task_payload.get("config", {})
    if not isinstance(config, dict):
        config = {}
    score = evaluation["aggregate_metric_value"]
    model = task_payload.get("model", {})
    if isinstance(model, dict):
        model = _with_model_card_metadata(model, model_cards=model_cards)
    environment = task_payload.get("environment", {})
    package_versions = environment.get("package_versions", {}) if isinstance(environment, dict) else {}
    experiment_manifest = task_payload.get("experiment_manifest", {})
    experiment_manifest = experiment_manifest if isinstance(experiment_manifest, dict) else {}
    model_dir = selected_result.model_dir
    model_name = selected_result.model_name
    model_source = model.get("source", {}) if isinstance(model, dict) else {}
    late_interaction = _late_interaction_metadata(model if isinstance(model, dict) else {}, evaluation)
    model_revision = _model_revision_value(model_source, key="revision")
    model_revision_requested = _model_revision_value(model_source, key="revision_requested")
    dataset_id = selected_result.dataset_id
    dataset_revision = _dataset_revision_value(target.get("dataset_revision"), key="resolved")
    dataset_revision_requested = _dataset_revision_value(target.get("dataset_revision"), key="requested")
    task_name = selected_result.task_name
    split_name = canonical_split_name(
        benchmark,
        str(target["split_name"]) if target.get("split_name") is not None else None,
    )
    task_key = selected_result.task_key
    _accumulate_run(
        run_accumulators,
        model_dir=model_dir,
        model_name=model_name,
        model=model if isinstance(model, dict) else {},
        package_versions=package_versions,
        target=target,
        evaluation=evaluation,
        generated_at_utc=task_payload.get("generated_at_utc"),
        score=float(score),
    )
    common: dict[str, Any] = {
        "model_dir": model_dir,
        "model_name": model_name,
        "model_revision": model_revision,
        "model_revision_requested": model_revision_requested,
        "benchmark": benchmark,
        "dataset_id": dataset_id,
        "dataset_revision": dataset_revision,
        "dataset_revision_requested": dataset_revision_requested,
        "dataset_name": str(target.get("dataset_name") or ""),
        "split_name": split_name,
        "task_name": task_name,
        "task_key": task_key,
        "result_path": str(result_path),
        "experiment_fingerprint": _str_or_none(experiment_manifest.get("fingerprint_sha256")),
        "active_parameters": _int_or_none(model.get("active_parameters")) if isinstance(model, dict) else None,
        "total_parameters": _int_or_none(model.get("total_parameters")) if isinstance(model, dict) else None,
        "max_seq_length": _int_or_none(model.get("max_seq_length")) if isinstance(model, dict) else None,
        "dtype": model.get("dtype") if isinstance(model, dict) else None,
        "attn_implementation": model.get("attn_implementation") if isinstance(model, dict) else None,
        "query_prompt": _str_or_none(config.get("query_prompt")),
        "document_prompt": _str_or_none(config.get("document_prompt")),
        "query_prompt_name": _str_or_none(config.get("query_prompt_name")),
        "document_prompt_name": _str_or_none(config.get("document_prompt_name")),
        "query_encode_task": _str_or_none(config.get("query_encode_task")),
        "document_encode_task": _str_or_none(config.get("document_encode_task")),
        "trust_remote_code": _bool_or_none(model.get("trust_remote_code")) if isinstance(model, dict) else None,
        "late_interaction_query_length": _int_or_none(late_interaction.get("query_length")),
        "late_interaction_document_length": _int_or_none(late_interaction.get("document_length")),
        "late_interaction_query_prefix": _str_or_none(late_interaction.get("query_prefix")),
        "late_interaction_document_prefix": _str_or_none(late_interaction.get("document_prefix")),
        "late_interaction_query_expansion": _bool_or_none(
            late_interaction.get("do_query_expansion", late_interaction.get("query_expansion"))
        ),
        "late_interaction_attend_to_expansion_tokens": _bool_or_none(
            late_interaction.get("attend_to_expansion_tokens")
        ),
        "torch_version": package_versions.get("torch"),
        "transformers_version": package_versions.get("transformers"),
        "sentence_transformers_version": package_versions.get("sentence-transformers"),
        "started_at_utc": evaluation.get("started_at_utc"),
        "finished_at_utc": evaluation.get("finished_at_utc"),
        "evaluated_at_utc": evaluation.get("evaluated_at_utc"),
        "duration_seconds_including_dataset_load": _float_or_none(
            evaluation.get("duration_seconds_including_dataset_load")
        ),
        "wall_seconds": _float_or_none(evaluation.get("wall_seconds")),
    }
    embedding_evaluations = _embedding_evaluations(
        evaluation.get("embedding_evaluations") or task_payload.get("embedding_evaluations")
    )
    base_embedding = _embedding_evaluation_named(embedding_evaluations, "base")
    rows.append(
        TaskResult(
            **common,
            score=float(score),
            aggregate_metric=evaluation.get("aggregate_metric"),
            embedding_dim=_embedding_dim(base_embedding),
            quantization=_quantization_precision(base_embedding),
        )
    )
    diagnostic_rows.append(
        _task_diagnostic_row(
            common=common,
            config=config,
            evaluation=evaluation,
            base_score=float(score),
        )
    )
    dataset_metadata_rows.append(_dataset_metadata_row(common=common, registry=registry))
    for embedding_evaluation in embedding_evaluations:
        variant_name = embedding_evaluation.get("name")
        if not isinstance(variant_name, str) or variant_name == "base":
            continue
        variant_score = embedding_evaluation.get("aggregate_metric_value")
        if not isinstance(variant_score, int | float):
            continue
        rows.append(
            TaskResult(
                **common,
                score=float(variant_score),
                aggregate_metric=embedding_evaluation.get("aggregate_metric") or evaluation.get("aggregate_metric"),
                embedding_variant_name=variant_name,
                embedding_dim=_embedding_dim(embedding_evaluation),
                quantization=_quantization_precision(embedding_evaluation),
            )
        )
    metric_rows.extend(
        _metric_rows_from_top_rankings(
            common=common,
            evaluation=evaluation,
            embedding_evaluations=embedding_evaluations,
            task_payload=task_payload,
            result_path=result_path,
        )
    )
    for metric_name, metric_value in task_payload.get("metrics", {}).items():
        if isinstance(metric_value, int | float):
            metric_rows.append(
                MetricLongRow(
                    model_dir=model_dir,
                    model_name=model_name,
                    benchmark=benchmark,
                    dataset_id=dataset_id,
                    task_name=task_name,
                    metric_name=canonical_metric_name(benchmark, metric_name),
                    metric_value=float(metric_value),
                    result_path=str(result_path),
                    score_target="all",
                    embedding_variant_name=None,
                )
            )
    for metric_name, metric_value in task_payload.get("rerank_metrics", {}).items():
        if isinstance(metric_value, int | float):
            metric_rows.append(
                MetricLongRow(
                    model_dir=model_dir,
                    model_name=model_name,
                    benchmark=benchmark,
                    dataset_id=dataset_id,
                    task_name=task_name,
                    metric_name=canonical_metric_name(benchmark, metric_name),
                    metric_value=float(metric_value),
                    result_path=str(result_path),
                    score_target="reranking",
                    embedding_variant_name=None,
                )
            )
    if include_retrieval_rankings:
        ranking_rows.extend(_retrieval_ranking_rows(common=common, task_payload=task_payload, result_path=result_path))
    return ProcessedResultRows(
        rows=rows,
        run_accumulators=run_accumulators,
        metric_rows=metric_rows,
        diagnostic_rows=diagnostic_rows,
        dataset_metadata_rows=dataset_metadata_rows,
        ranking_rows=ranking_rows,
    )


def _merge_run_accumulators(target: dict[str, dict[str, Any]], source: dict[str, dict[str, Any]]) -> None:
    for model_name, source_item in source.items():
        target_item = target.setdefault(
            model_name,
            {
                "model_dir": source_item["model_dir"],
                "model_name": source_item["model_name"],
                "generated_at_utc": None,
                "started_at_values": [],
                "finished_at_values": [],
                "targets": set(),
                "split_count": 0,
                "cache_hit_values": [],
                "scores": [],
                "active_parameters": source_item["active_parameters"],
                "total_parameters": source_item["total_parameters"],
                "max_seq_length": source_item["max_seq_length"],
                "dtype": source_item["dtype"],
                "attn_implementation": source_item["attn_implementation"],
                "torch_version": source_item["torch_version"],
                "transformers_version": source_item["transformers_version"],
                "sentence_transformers_version": source_item["sentence_transformers_version"],
            },
        )
        target_item["model_name"] = source_item["model_name"]
        target_item["generated_at_utc"] = _max_string(
            target_item.get("generated_at_utc"),
            source_item.get("generated_at_utc"),
        )
        target_item["started_at_values"].extend(source_item["started_at_values"])
        target_item["finished_at_values"].extend(source_item["finished_at_values"])
        target_item["targets"].update(source_item["targets"])
        target_item["split_count"] += source_item["split_count"]
        target_item["cache_hit_values"].extend(source_item["cache_hit_values"])
        target_item["scores"].extend(source_item["scores"])


def _filter_rows_by_result_path(rows: list[Any], result_paths: set[str] | None) -> list[Any]:
    if result_paths is None:
        return rows
    return [row for row in rows if row.result_path in result_paths]


def _current_source_hashes(results_dir: Path | Sequence[Path]) -> dict[str, str | None]:
    return {str(path): _payload_sha256(str(path)) for path in _result_json_paths(results_dir)}


def _result_json_paths(results_dir: Path | Sequence[Path]) -> list[Path]:
    paths: list[Path] = []
    for source_dir in _results_dirs(results_dir):
        paths.extend(path for path in sorted(source_dir.glob("*/*/*")) if _is_result_json_path(path))
    return sorted(paths)


def _is_result_json_path(path: Path) -> bool:
    return path.is_file() and path.name.endswith(RESULT_JSON_SUFFIXES)


def _incremental_cache_current(
    current_hashes: dict[str, str | None],
    db_path: Path,
    *,
    model_cards_path: Path | None = DEFAULT_MODEL_CARDS_PATH,
) -> bool:
    if not current_hashes or not db_path.exists():
        return False
    previous_hashes = _read_previous_source_hashes(db_path)
    if current_hashes != previous_hashes:
        return False
    return _incremental_cache_schema_compatible(db_path) and _model_cards_cache_current(
        db_path,
        model_cards_path=model_cards_path,
    )


def _incremental_cache_schema_compatible(db_path: Path) -> bool:
    if not db_path.exists():
        return False
    con = duckdb.connect(str(db_path), read_only=True)
    try:
        if (
            not _duckdb_table_exists(con, "meta_database")
            or not _duckdb_table_exists(con, "viewer_leaderboard_rows")
            or not _duckdb_table_exists(con, "viewer_leaderboard_language_options")
        ):
            return False
        return con.execute("SELECT schema_version FROM meta_database").fetchone() == (WAREHOUSE_SCHEMA_VERSION,)
    finally:
        con.close()


def _model_cards_cache_current(db_path: Path, *, model_cards_path: Path | None) -> bool:
    model_cards_state = _model_cards_state(model_cards_path)
    con = duckdb.connect(str(db_path), read_only=True)
    try:
        if not _duckdb_table_exists(con, "meta_database"):
            return False
        row = con.execute("SELECT model_cards_path, model_cards_sha256 FROM meta_database").fetchone()
        return row == model_cards_state
    finally:
        con.close()


def _fetch_task_result_rows(con: duckdb.DuckDBPyConnection) -> list[TaskResult]:
    columns = (
        "model_dir",
        "model_name",
        "model_revision",
        "model_revision_requested",
        "benchmark",
        "dataset_id",
        "dataset_revision",
        "dataset_revision_requested",
        "dataset_name",
        "split_name",
        "task_name",
        "task_key",
        "score",
        "aggregate_metric",
        "result_path",
        "experiment_fingerprint",
        "active_parameters",
        "total_parameters",
        "max_seq_length",
        "dtype",
        "attn_implementation",
        "query_prompt",
        "document_prompt",
        "query_prompt_name",
        "document_prompt_name",
        "query_encode_task",
        "document_encode_task",
        "trust_remote_code",
        "late_interaction_query_length",
        "late_interaction_document_length",
        "late_interaction_query_prefix",
        "late_interaction_document_prefix",
        "late_interaction_query_expansion",
        "late_interaction_attend_to_expansion_tokens",
        "torch_version",
        "transformers_version",
        "sentence_transformers_version",
        "started_at_utc",
        "finished_at_utc",
        "evaluated_at_utc",
        "duration_seconds_including_dataset_load",
        "wall_seconds",
        "embedding_variant_name",
        "embedding_dim",
        "quantization",
    )
    return _fetch_model_rows(con, "task_results", TaskResult, columns)


def _fetch_model_rows(
    con: duckdb.DuckDBPyConnection,
    table_name: str,
    model_class: type[TaskResult]
    | type[MetricLongRow]
    | type[TaskDiagnosticRow]
    | type[DatasetMetadataRow]
    | type[RetrievalRankingRow],
    columns: Sequence[str],
) -> Any:
    column_sql = ", ".join(columns)
    return [model_class.model_validate(dict(zip(columns, row, strict=True))) for row in con.execute(f"SELECT {column_sql} FROM {table_name}").fetchall()]


def _fetch_dict_rows(con: duckdb.DuckDBPyConnection, table_name: str) -> list[dict[str, Any]]:
    result = con.execute(f"SELECT * FROM {table_name}")
    columns = [description[0] for description in result.description]
    return [dict(zip(columns, row, strict=True)) for row in result.fetchall()]


def _selected_result_jsons(
    results_dir: Path | Sequence[Path],
    *,
    benchmark_configs: Sequence[BenchmarkConfig],
    target_benchmarks: set[str],
    exclude_model_names: set[str],
    result_paths: set[str] | None = None,
    duplicate_result_policy: DuplicateResultPolicy = "first-wins",
    include_retrieval_rankings: bool = False,
    memory_monitor: MemoryMonitor | None = None,
    result_selection_workers: int = 1,
    retain_summary_payload: bool = True,
    model_name_override: str | None = None,
) -> list[SelectedResultJson]:
    selected_by_task: dict[tuple[str, str, str, str], SelectedResultJson] = {}
    parsed_count = 0
    for source_priority, source_dir in enumerate(_results_dirs(results_dir)):
        source_paths = [
            result_path
            for result_path in _result_json_paths(source_dir)
            if result_paths is None or str(result_path) in result_paths
        ]
        for selected in _iterate_async(
            _async_selected_result_jsons(
                source_paths,
                results_dir=source_dir,
                source_priority=source_priority,
                benchmark_configs=benchmark_configs,
                target_benchmarks=target_benchmarks,
                exclude_model_names=exclude_model_names,
                workers=result_selection_workers,
            )
        ):
            parsed_count += 1
            if memory_monitor is not None:
                memory_monitor.maybe_sample("result_json_selected", processed_count=parsed_count)
            if selected is None:
                continue
            if model_name_override is not None:
                selected = replace(selected, model_name=model_name_override)
            key = (
                selected.model_name,
                selected.benchmark,
                selected.dataset_id,
                selected.task_key,
            )
            current = selected_by_task.get(key)
            if current is None or _prefer_selected_result_json(
                selected,
                current,
                duplicate_result_policy=duplicate_result_policy,
            ):
                selected_by_task[key] = selected if retain_summary_payload else _discard_selected_result_payload(selected)
    return sorted(
        selected_by_task.values(),
        key=lambda selected: (
            selected.model_name,
            selected.benchmark,
            selected.dataset_id,
            selected.task_name,
            str(selected.result_path),
        ),
    )


def _discard_selected_result_payload(selected: SelectedResultJson) -> SelectedResultJson:
    return replace(selected, payload={})


async def _async_selected_result_jsons(
    result_paths: Sequence[Path],
    *,
    results_dir: Path,
    source_priority: int,
    benchmark_configs: Sequence[BenchmarkConfig],
    target_benchmarks: set[str],
    exclude_model_names: set[str],
    workers: int,
) -> AsyncIterable[SelectedResultJson | None]:
    workers = max(1, workers)
    if workers == 1 or len(result_paths) <= 1:
        for result_path in result_paths:
            yield _selected_result_json(
                result_path,
                results_dir=results_dir,
                source_priority=source_priority,
                benchmark_configs=benchmark_configs,
                target_benchmarks=target_benchmarks,
                exclude_model_names=exclude_model_names,
            )
        return

    loop = asyncio.get_running_loop()
    with ProcessPoolExecutor(max_workers=workers) as executor:
        async def submit(result_path: Path) -> SelectedResultJson | None:
            return await loop.run_in_executor(
                executor,
                _selected_result_json_worker,
                str(result_path),
                str(results_dir),
                source_priority,
                list(benchmark_configs),
                set(target_benchmarks),
                set(exclude_model_names),
            )

        async for item in _ordered_async_bounded_map(
            result_paths,
            submit,
            max_pending=workers * 2,
        ):
            yield item


def _selected_result_json_worker(
    result_path: str,
    results_dir: str,
    source_priority: int,
    benchmark_configs: Sequence[BenchmarkConfig],
    target_benchmarks: set[str],
    exclude_model_names: set[str],
) -> SelectedResultJson | None:
    return _selected_result_json(
        Path(result_path),
        results_dir=Path(results_dir),
        source_priority=source_priority,
        benchmark_configs=benchmark_configs,
        target_benchmarks=target_benchmarks,
        exclude_model_names=exclude_model_names,
    )


def _results_dirs(results_dir: Path | Sequence[Path]) -> list[Path]:
    if isinstance(results_dir, Path):
        return [results_dir]
    return list(results_dir)


def _selected_result_json(
    result_path: Path,
    *,
    results_dir: Path,
    source_priority: int,
    benchmark_configs: Sequence[BenchmarkConfig],
    target_benchmarks: set[str],
    exclude_model_names: set[str],
) -> SelectedResultJson | None:
    summary = _read_result_summary_payload_with_sha256(result_path)
    if summary is None:
        return None
    task_payload, payload_sha256 = summary
    target = task_payload.get("target", {})
    if not isinstance(target, dict):
        return None
    benchmark = benchmark_name(
        target.get("dataset_id"),
        target.get("dataset_name"),
        benchmark_configs=benchmark_configs,
    )
    if benchmark not in target_benchmarks:
        return None
    evaluation = task_payload.get("evaluation", {})
    if not isinstance(evaluation, dict):
        return None
    score = evaluation.get("aggregate_metric_value")
    if not isinstance(score, int | float):
        return None
    model_dir = result_path.relative_to(results_dir).parts[0]
    model = task_payload.get("model", {})
    model_name = _model_name_from_payload(model, model_dir=model_dir)
    if model_name in exclude_model_names:
        return None
    dataset_id = str(target.get("dataset_id") or "")
    raw_task_name = str(target.get("task_name") or target.get("split_name") or "")
    task_name = canonical_task_name(benchmark, raw_task_name)
    task_key = canonical_task_key(benchmark=benchmark, dataset_id=dataset_id, task_name=task_name)
    return SelectedResultJson(
        result_path=result_path,
        results_dir=results_dir,
        source_priority=source_priority,
        payload=task_payload,
        benchmark=benchmark,
        model_dir=model_dir,
        model_name=model_name,
        dataset_id=dataset_id,
        task_name=task_name,
        task_key=task_key,
        payload_sha256=payload_sha256,
    )


def _prefer_selected_result_json(
    candidate: SelectedResultJson,
    current: SelectedResultJson,
    *,
    duplicate_result_policy: DuplicateResultPolicy,
) -> bool:
    if candidate.source_priority != current.source_priority:
        if duplicate_result_policy == "last-wins":
            return candidate.source_priority > current.source_priority
        return candidate.source_priority < current.source_priority
    return _selected_result_path_stem_matches_task(candidate) and not _selected_result_path_stem_matches_task(current)


def _selected_result_path_stem_matches_task(selected: SelectedResultJson) -> bool:
    return _result_task_stem(selected.result_path) == selected.task_name


def _compact_result_payload(
    task_payload: dict[str, Any],
    *,
    include_retrieval_rankings: bool,
) -> dict[str, Any]:
    if include_retrieval_rankings:
        return task_payload
    artifact = _top_rankings_artifact(task_payload)
    if artifact is None:
        return task_payload
    rankings = artifact.get("rankings")
    if not isinstance(rankings, list):
        return task_payload
    evaluation = task_payload.get("evaluation", {})
    if not isinstance(evaluation, dict):
        return task_payload
    embedding_evaluations = _embedding_evaluations(
        evaluation.get("embedding_evaluations") or task_payload.get("embedding_evaluations")
    )
    selected_rankings = [
        ranking
        for ranking, _, _ in _selected_metric_rankings(
            rankings,
            evaluation=evaluation,
            embedding_evaluations=embedding_evaluations,
        )
    ]
    compact_artifact = dict(artifact)
    compact_artifact["rankings"] = selected_rankings
    compact_artifacts = dict(task_payload.get("artifacts", {}))
    compact_artifacts["top_rankings"] = compact_artifact
    compact_payload = dict(task_payload)
    compact_payload["artifacts"] = compact_artifacts
    return compact_payload


def _result_task_stem(path: Path) -> str:
    name = path.name
    for suffix in RESULT_JSON_SUFFIXES:
        if name.endswith(suffix):
            return name[: -len(suffix)]
    return path.stem


def _model_name_from_payload(model: Any, *, model_dir: str) -> str:
    if not isinstance(model, dict):
        return model_dir
    return str(model.get("id") or model_dir)


def _metric_rows_from_top_rankings(
    *,
    common: dict[str, Any],
    evaluation: dict[str, Any],
    embedding_evaluations: list[dict[str, Any]],
    task_payload: dict[str, Any],
    result_path: Path,
) -> list[MetricLongRow]:
    artifact = _top_rankings_artifact(task_payload)
    if artifact is None:
        return []
    ranking_payload = _top_rankings_payload(artifact=artifact, result_path=result_path)
    if not isinstance(ranking_payload, dict):
        return []
    qrels = _qrels_from_ranking_payload(ranking_payload)
    if not qrels:
        return []
    rankings = ranking_payload.get("rankings")
    if not isinstance(rankings, list):
        return []

    selected_rankings = _selected_metric_rankings(
        rankings,
        evaluation=evaluation,
        embedding_evaluations=embedding_evaluations,
    )
    grouped_rankings: dict[tuple[str, str | None, str], dict[str, list[str]]] = {}
    for ranking, score_target, embedding_variant_name in selected_rankings:
        score_name = ranking.get("score_name")
        if not isinstance(score_name, str) or not score_name:
            continue
        query_rankings = _query_rankings_from_artifact_row(ranking)
        if not query_rankings:
            continue
        grouped_rankings.setdefault((score_target, embedding_variant_name, score_name), {}).update(query_rankings)
        if score_target == "reranking":
            no_safeguard_rankings = _query_rankings_without_safeguard_from_artifact_row(ranking)
            if no_safeguard_rankings:
                grouped_rankings.setdefault(
                    ("reranking_without_safeguard", embedding_variant_name, score_name),
                    {},
                ).update(no_safeguard_rankings)

    rows: list[MetricLongRow] = []
    for (score_target, embedding_variant_name, score_name), query_rankings in grouped_rankings.items():
        metrics = compute_ir_metrics(
            rankings=query_rankings,
            qrels=qrels,
            evaluator_name=str(common["task_name"]),
            score_name=score_name,
            metric_names=VIEWER_RECOMPUTED_METRICS,
        )
        for metric_name, metric_value in metrics.items():
            rows.append(
                MetricLongRow(
                    model_dir=str(common["model_dir"]),
                    model_name=str(common["model_name"]),
                    benchmark=str(common["benchmark"]),
                    dataset_id=str(common["dataset_id"]),
                    task_name=str(common["task_name"]),
                    metric_name=canonical_metric_name(str(common["benchmark"]), metric_name),
                    metric_value=float(metric_value),
                    result_path=str(result_path),
                    score_target=score_target,
                    embedding_variant_name=embedding_variant_name,
                )
            )
    return rows


def _qrels_from_ranking_payload(ranking_payload: dict[str, Any]) -> dict[str, set[str]]:
    rows = ranking_payload.get("qrels")
    if not isinstance(rows, list):
        return {}
    qrels: dict[str, set[str]] = {}
    for row in rows:
        if not isinstance(row, dict):
            continue
        query_id = row.get("query_id")
        relevant_corpus_ids = row.get("relevant_corpus_ids")
        if query_id is None or not isinstance(relevant_corpus_ids, list):
            continue
        qrels[str(query_id)] = {str(corpus_id) for corpus_id in relevant_corpus_ids}
    return qrels


def _selected_metric_rankings(
    rankings: list[Any],
    *,
    evaluation: dict[str, Any],
    embedding_evaluations: list[dict[str, Any]],
) -> list[tuple[dict[str, Any], str, str | None]]:
    context = _top_ranking_selection_context(
        evaluation=evaluation,
        embedding_evaluations=embedding_evaluations,
    )
    selected: list[tuple[dict[str, Any], str, str | None]] = []
    for ranking in rankings:
        if not isinstance(ranking, dict):
            continue
        selected_ranking = _selected_metric_ranking(ranking, context)
        if selected_ranking is not None:
            selected.append(selected_ranking)
    return selected


def _selected_metric_ranking(
    ranking: dict[str, Any],
    context: TopRankingSelectionContext,
) -> tuple[dict[str, Any], str, str | None] | None:
    ranking_kind = ranking.get("ranking_kind")
    embedding_variant_name = _str_or_none(ranking.get("embedding_variant_name"))
    if ranking_kind == "retrieval":
        variant_key = embedding_variant_name or "base"
        if (
            not context.retrieval_score_names
            or ranking.get("score_name") == context.retrieval_score_names.get(variant_key)
        ):
            return ranking, "all", embedding_variant_name
        return None
    if ranking_kind != "candidate_rerank":
        return None
    score_name = ranking.get("score_name")
    if not isinstance(score_name, str):
        return None
    if embedding_variant_name is None:
        if score_name == context.best_rerank_score_name:
            return ranking, "reranking", None
        return None
    retrieval_score_name = context.retrieval_score_names.get(embedding_variant_name)
    if retrieval_score_name is not None and _is_rerank_score_name_for_retrieval(
        score_name=score_name,
        retrieval_score_name=retrieval_score_name,
    ):
        return ranking, "reranking", embedding_variant_name
    return None


def _is_rerank_score_name_for_retrieval(*, score_name: str, retrieval_score_name: str) -> bool:
    return score_name.startswith(f"{retrieval_score_name}_") and score_name.endswith("_rerank")


def _best_rerank_score_name(evaluation: dict[str, Any]) -> str | None:
    reranking = _first_reranking_evaluation(evaluation.get("reranking_evaluations"))
    return _str_or_none(reranking.get("best_score_name"))


def _query_rankings_from_artifact_row(ranking: dict[str, Any]) -> dict[str, list[str]]:
    query_id = ranking.get("query_id")
    corpus_ids = ranking.get("corpus_ids")
    if query_id is None or not isinstance(corpus_ids, list):
        return {}
    query_id_text = query_id if isinstance(query_id, str) else str(query_id)
    if all(isinstance(corpus_id, str) for corpus_id in corpus_ids):
        return {query_id_text: corpus_ids}
    return {query_id_text: [str(corpus_id) for corpus_id in corpus_ids]}


def _query_rankings_without_safeguard_from_artifact_row(ranking: dict[str, Any]) -> dict[str, list[str]]:
    query_rankings = _query_rankings_from_artifact_row(ranking)
    if not query_rankings:
        return {}
    query_id, corpus_ids = next(iter(query_rankings.items()))
    safeguard_corpus_id = ranking.get("safeguard_corpus_id")
    if safeguard_corpus_id is None:
        if ranking.get("safeguard_policy") is None:
            return {}
        return query_rankings
    filtered = [corpus_id for corpus_id in corpus_ids if corpus_id != str(safeguard_corpus_id)]
    return {query_id: filtered}


def _retrieval_ranking_rows(
    *,
    common: dict[str, Any],
    task_payload: dict[str, Any],
    result_path: Path,
) -> list[RetrievalRankingRow]:
    artifact = _top_rankings_artifact(task_payload)
    if artifact is None:
        return []
    ranking_payload = _top_rankings_payload(artifact=artifact, result_path=result_path)
    rankings = ranking_payload.get("rankings") if isinstance(ranking_payload, dict) else None
    if not isinstance(rankings, list):
        return []

    rows: list[RetrievalRankingRow] = []
    for ranking in rankings:
        if not isinstance(ranking, dict):
            continue
        query_id = ranking.get("query_id")
        corpus_ids = ranking.get("corpus_ids")
        if query_id is None or not isinstance(corpus_ids, list):
            continue
        for rank_index, corpus_id in enumerate(corpus_ids, start=1):
            rows.append(
                RetrievalRankingRow(
                    model_dir=str(common["model_dir"]),
                    model_name=str(common["model_name"]),
                    benchmark=str(common["benchmark"]),
                    dataset_id=str(common["dataset_id"]),
                    dataset_revision=_str_or_none(common.get("dataset_revision")),
                    dataset_name=str(common["dataset_name"]),
                    split_name=_str_or_none(common.get("split_name")),
                    task_name=str(common["task_name"]),
                    task_key=str(common["task_key"]),
                    result_path=str(result_path),
                    ranking_path=str(_top_rankings_location(artifact=artifact, result_path=result_path)),
                    ranking_name=_str_or_none(ranking.get("name")),
                    ranking_kind=_str_or_none(ranking.get("ranking_kind")),
                    embedding_variant_name=_str_or_none(ranking.get("embedding_variant_name")),
                    distance=_str_or_none(ranking.get("distance")),
                    score_name=_str_or_none(ranking.get("score_name")),
                    query_id=str(query_id),
                    rank=rank_index,
                    corpus_id=str(corpus_id),
                )
            )
    return rows


def _top_rankings_artifact(task_payload: dict[str, Any]) -> dict[str, Any] | None:
    artifacts = task_payload.get("artifacts")
    if not isinstance(artifacts, dict):
        return None
    artifact = artifacts.get("top_rankings")
    if not isinstance(artifact, dict):
        return None
    path = artifact.get("path")
    rankings = artifact.get("rankings")
    if not isinstance(rankings, list) and (not isinstance(path, str) or not path):
        return None
    return artifact


def _top_rankings_payload(*, artifact: dict[str, Any], result_path: Path) -> dict[str, Any] | None:
    rankings = artifact.get("rankings")
    path = artifact.get("path")
    if isinstance(rankings, list) and (rankings or not isinstance(path, str) or not path):
        return artifact
    if not isinstance(path, str) or not path:
        return None
    ranking_path = result_path.parent / path
    if not ranking_path.exists():
        return None
    ranking_payload = _read_json(ranking_path)
    return ranking_payload if isinstance(ranking_payload, dict) else None


def _top_rankings_location(*, artifact: dict[str, Any], result_path: Path) -> Path:
    path = artifact.get("path")
    if isinstance(path, str) and path:
        return result_path.parent / path
    return result_path


def _with_model_card_metadata(model: dict[str, Any], *, model_cards: dict[str, dict[str, Any]]) -> dict[str, Any]:
    model_id = model.get("id")
    source = model.get("source")
    source_name = source.get("name") if isinstance(source, dict) else None
    card = model_cards.get(str(model_id or source_name or ""))
    if card is None:
        return model
    parameters = card.get("parameters")
    if not isinstance(parameters, dict):
        return model
    total_parameters = _int_or_none(model.get("total_parameters"))
    card_total_parameters = _int_or_none(parameters.get("total"))
    if total_parameters != card_total_parameters:
        return model
    active_parameters = _int_or_none(model.get("active_parameters"))
    card_active_parameters = _int_or_none(parameters.get("active"))
    if (
        active_parameters is not None
        and card_active_parameters is not None
        and active_parameters != card_active_parameters
    ):
        return model
    updated = dict(model)
    input_embedding_parameters = _int_or_none(parameters.get("input_embedding"))
    if active_parameters is None and card_active_parameters is not None:
        updated["active_parameters"] = card_active_parameters
    if _int_or_none(updated.get("embedding_parameters")) is None:
        updated["embedding_parameters"] = input_embedding_parameters
    if _int_or_none(updated.get("transformer_parameters")) is None and card_active_parameters is not None:
        updated["transformer_parameters"] = card_active_parameters
    if not isinstance(updated.get("late_interaction"), dict) and isinstance(card.get("late_interaction"), dict):
        updated["late_interaction"] = card["late_interaction"]
    return updated


def _accumulate_run(
    accumulators: dict[str, dict[str, Any]],
    *,
    model_dir: str,
    model_name: str,
    model: dict[str, Any],
    package_versions: dict[str, Any],
    target: dict[str, Any],
    evaluation: dict[str, Any],
    generated_at_utc: Any,
    score: float,
) -> None:
    accumulator = accumulators.setdefault(
        model_name,
        {
            "model_dir": model_dir,
            "model_name": model_name,
            "generated_at_utc": None,
            "started_at_values": [],
            "finished_at_values": [],
            "targets": set(),
            "split_count": 0,
            "cache_hit_values": [],
            "scores": [],
            "active_parameters": _int_or_none(model.get("active_parameters")),
            "total_parameters": _int_or_none(model.get("total_parameters")),
            "max_seq_length": _int_or_none(model.get("max_seq_length")),
            "dtype": model.get("dtype"),
            "attn_implementation": model.get("attn_implementation"),
            "torch_version": package_versions.get("torch"),
            "transformers_version": package_versions.get("transformers"),
            "sentence_transformers_version": package_versions.get("sentence-transformers"),
        },
    )
    accumulator["model_name"] = model_name
    accumulator["generated_at_utc"] = _max_string(accumulator.get("generated_at_utc"), generated_at_utc)
    _append_string(accumulator["started_at_values"], evaluation.get("started_at_utc"))
    _append_string(accumulator["finished_at_values"], evaluation.get("finished_at_utc"))
    dataset_id = target.get("dataset_id")
    if dataset_id is not None:
        accumulator["targets"].add(str(dataset_id))
    accumulator["split_count"] += 1
    if isinstance(evaluation.get("cache_hit"), bool):
        accumulator["cache_hit_values"].append(evaluation["cache_hit"])
    accumulator["scores"].append(score)


def _runs_from_task_results(accumulators: dict[str, dict[str, Any]]) -> list[dict[str, Any]]:
    runs: list[dict[str, Any]] = []
    for model_key in sorted(accumulators):
        item = accumulators[model_key]
        cache_hit_values = item["cache_hit_values"]
        cache_hit_count = sum(1 for value in cache_hit_values if value) if cache_hit_values else None
        evaluated_count = sum(1 for value in cache_hit_values if not value) if cache_hit_values else None
        scores = item["scores"]
        runs.append(
            {
                "model_dir": item["model_dir"],
                "model_name": item["model_name"],
                "generated_at_utc": item["generated_at_utc"],
                "started_at_utc": min(item["started_at_values"]) if item["started_at_values"] else None,
                "finished_at_utc": max(item["finished_at_values"]) if item["finished_at_values"] else None,
                "target_count": len(item["targets"]),
                "split_count": item["split_count"],
                "cache_hit_count": cache_hit_count,
                "evaluated_count": evaluated_count,
                "aggregate_metric_mean": float(sum(scores) / len(scores)) if scores else None,
                "active_parameters": item["active_parameters"],
                "total_parameters": item["total_parameters"],
                "max_seq_length": item["max_seq_length"],
                "dtype": item["dtype"],
                "attn_implementation": item["attn_implementation"],
                "torch_version": item["torch_version"],
                "transformers_version": item["transformers_version"],
                "sentence_transformers_version": item["sentence_transformers_version"],
            }
        )
    return runs


def _runs_from_task_result_rows(rows: Sequence[TaskResult]) -> list[dict[str, Any]]:
    # Partial incremental loads merge cached task rows with changed task rows,
    # so run aggregates must be derived from the merged canonical rows rather
    # than copied from the previous database.
    accumulators: dict[str, dict[str, Any]] = {}
    for row in rows:
        if row.embedding_variant_name is not None:
            continue
        accumulator = accumulators.setdefault(
            row.model_name,
            {
                "model_dir": row.model_dir,
                "model_name": row.model_name,
                "generated_at_utc": None,
                "started_at_values": [],
                "finished_at_values": [],
                "targets": set(),
                "split_count": 0,
                "cache_hit_values": [],
                "scores": [],
                "active_parameters": row.active_parameters,
                "total_parameters": row.total_parameters,
                "max_seq_length": row.max_seq_length,
                "dtype": row.dtype,
                "attn_implementation": row.attn_implementation,
                "torch_version": row.torch_version,
                "transformers_version": row.transformers_version,
                "sentence_transformers_version": row.sentence_transformers_version,
            },
        )
        accumulator["model_name"] = row.model_name
        _append_string(accumulator["started_at_values"], row.started_at_utc)
        _append_string(accumulator["finished_at_values"], row.finished_at_utc)
        accumulator["targets"].add(row.dataset_id)
        accumulator["split_count"] += 1
        accumulator["scores"].append(row.score)
    return _runs_from_task_results(accumulators)


def _append_string(values: list[str], value: Any) -> None:
    if isinstance(value, str):
        values.append(value)


def _max_string(current: Any, candidate: Any) -> str | None:
    values = [value for value in (current, candidate) if isinstance(value, str)]
    return max(values) if values else None


def benchmark_name(
    dataset_id: Any,
    dataset_name: Any,
    *,
    benchmark_configs: Sequence[BenchmarkConfig] | None = None,
) -> str:
    value = f"{dataset_id or ''}/{dataset_name or ''}"
    benchmark_configs = benchmark_configs or load_benchmark_configs()
    best_name: str | None = None
    best_match_length = -1
    for benchmark in benchmark_configs:
        for pattern in benchmark.match_patterns:
            if pattern in value and len(pattern) > best_match_length:
                best_name = benchmark.name
                best_match_length = len(pattern)
    if best_name is not None:
        return best_name
    return "Other"


def _dedupe_task_results(rows: list[TaskResult]) -> list[TaskResult]:
    deduped: dict[tuple[str, str, str, str, str | None, int | None, str | None], TaskResult] = {}
    for row in rows:
        key = (
            row.model_name,
            row.benchmark,
            row.dataset_id,
            row.task_key,
            row.embedding_variant_name,
            row.embedding_dim,
            row.quantization,
        )
        current = deduped.get(key)
        if current is None or _prefer_task_result(row, current):
            deduped[key] = row
    return list(deduped.values())


def _prefer_task_result(candidate: TaskResult, current: TaskResult) -> bool:
    return _result_path_stem_matches_task(candidate) and not _result_path_stem_matches_task(current)


def _result_path_stem_matches_task(row: TaskResult) -> bool:
    return _result_task_stem(Path(row.result_path)) == row.task_name


def _best_rerank_metrics(evaluation: dict[str, Any]) -> dict[str, Any]:
    reranking_evaluations = evaluation.get("reranking_evaluations")
    if not isinstance(reranking_evaluations, list):
        return {}
    for reranking_evaluation in reranking_evaluations:
        if not isinstance(reranking_evaluation, dict):
            continue
        best_score_name = reranking_evaluation.get("best_score_name")
        distance_evaluations = reranking_evaluation.get("distance_evaluations")
        if not isinstance(best_score_name, str) or not isinstance(distance_evaluations, list):
            continue
        for distance_evaluation in distance_evaluations:
            if not isinstance(distance_evaluation, dict) or distance_evaluation.get("score_name") != best_score_name:
                continue
            metrics = distance_evaluation.get("metrics")
            return metrics if isinstance(metrics, dict) else {}
    return {}


def _dedupe_metric_rows(rows: list[MetricLongRow]) -> list[MetricLongRow]:
    deduped: dict[tuple[Any, ...], MetricLongRow] = {}
    for row in rows:
        key = (
            row.model_name,
            row.benchmark,
            row.dataset_id,
            row.task_name,
            row.score_target,
            row.embedding_variant_name,
            row.metric_name,
        )
        current = deduped.get(key)
        if current is None or _prefer_metric_row(row, current):
            deduped[key] = row
    return list(deduped.values())


def _prefer_metric_row(candidate: MetricLongRow, current: MetricLongRow) -> bool:
    return _metric_result_path_stem_matches_task(candidate) and not _metric_result_path_stem_matches_task(current)


def _metric_result_path_stem_matches_task(row: MetricLongRow) -> bool:
    return _result_task_stem(Path(row.result_path)) == row.task_name


def _dedupe_task_diagnostic_rows(rows: list[TaskDiagnosticRow]) -> list[TaskDiagnosticRow]:
    deduped: dict[tuple[str, str, str, str], TaskDiagnosticRow] = {}
    for row in rows:
        key = (row.model_name, row.benchmark, row.dataset_id, row.task_key)
        current = deduped.get(key)
        if current is None or _diagnostic_result_path_stem_matches_task(row):
            deduped[key] = row
    return list(deduped.values())


def _diagnostic_result_path_stem_matches_task(row: TaskDiagnosticRow) -> bool:
    return _result_task_stem(Path(row.result_path)) == row.task_name


def _dedupe_dataset_metadata_rows(rows: list[DatasetMetadataRow]) -> list[DatasetMetadataRow]:
    deduped: dict[str, DatasetMetadataRow] = {}
    for row in rows:
        deduped[row.task_key] = row
    return list(deduped.values())


def _dedupe_retrieval_ranking_rows(rows: list[RetrievalRankingRow]) -> list[RetrievalRankingRow]:
    deduped: dict[tuple[Any, ...], RetrievalRankingRow] = {}
    for row in rows:
        deduped[row.duckdb_values()] = row
    return list(deduped.values())


def _dataset_metadata_row(*, common: dict[str, Any], registry: DatasetRegistry) -> DatasetMetadataRow:
    metadata = _metadata_for_common_task(common=common, registry=registry)
    query_stats = metadata.get("query_text_stats")
    query_stats = query_stats if isinstance(query_stats, dict) else {}
    document_stats = metadata.get("document_text_stats")
    document_stats = document_stats if isinstance(document_stats, dict) else {}
    citation_keys = metadata.get("citation_keys")
    references = metadata.get("references")
    return DatasetMetadataRow(
        benchmark=str(common["benchmark"]),
        dataset_id=str(common["dataset_id"]),
        dataset_name=str(common["dataset_name"]),
        split_name=_str_or_none(common.get("split_name")),
        task_name=str(common["task_name"]),
        task_key=str(common["task_key"]),
        language=_str_or_none(metadata.get("language")),
        languages=_metadata_languages(metadata),
        primary_languages=_metadata_primary_languages(metadata),
        category=_str_or_none(metadata.get("category")),
        short_description=_str_or_none(metadata.get("short_description")),
        citation_count=len(citation_keys) if isinstance(citation_keys, list) else None,
        reference_count=len(references) if isinstance(references, list) else None,
        has_bibtex=bool(metadata.get("bibtex")) if "bibtex" in metadata else None,
        query_count=_int_or_none(query_stats.get("count")),
        document_count=_int_or_none(document_stats.get("count")),
        query_mean_chars=_float_or_none(query_stats.get("mean_chars")),
        document_mean_chars=_float_or_none(document_stats.get("mean_chars")),
    )


def _metadata_for_common_task(*, common: dict[str, Any], registry: DatasetRegistry) -> dict[str, Any]:
    for dataset_key in (common.get("dataset_id"), common.get("dataset_name")):
        if not isinstance(dataset_key, str) or not dataset_key:
            continue
        try:
            dataset = registry.get_dataset(dataset_key)
        except KeyError:
            continue
        return dataset.metadata_for_task(
            split_name=str(common.get("split_name") or ""),
            task_name=str(common.get("task_name") or ""),
        )
    return {}


def _metadata_languages(metadata: dict[str, Any]) -> list[str]:
    languages = metadata.get("languages")
    if isinstance(languages, list):
        return [str(language) for language in languages if isinstance(language, str) and language]
    language = _str_or_none(metadata.get("language"))
    return [language] if language else []


def _metadata_primary_languages(metadata: dict[str, Any]) -> list[str]:
    primary_languages = metadata.get("primary_languages")
    if isinstance(primary_languages, list):
        return [str(language) for language in primary_languages if isinstance(language, str) and language]
    return []


def _task_diagnostic_row(
    *,
    common: dict[str, Any],
    config: dict[str, Any],
    evaluation: dict[str, Any],
    base_score: float,
) -> TaskDiagnosticRow:
    timing = evaluation.get("timing")
    timing = timing if isinstance(timing, dict) else {}
    reranking = _first_reranking_evaluation(evaluation.get("reranking_evaluations"))
    coverage_value = reranking.get("candidate_coverage")
    coverage: dict[str, Any] = coverage_value if isinstance(coverage_value, dict) else {}
    rerank_score = _float_or_none(evaluation.get("rerank_aggregate_metric_value"))
    if rerank_score is None:
        rerank_score = _float_or_none(reranking.get("aggregate_metric_value"))
    bm25_config = config.get("bm25")
    bm25_config = bm25_config if isinstance(bm25_config, dict) else {}
    rerank_top_k = _int_or_none(config.get("rerank_top_k"))
    if rerank_top_k is None:
        rerank_top_k = _int_or_none(reranking.get("rerank_top_k") or reranking.get("rerank_top_n"))
    return TaskDiagnosticRow(
        model_dir=str(common["model_dir"]),
        model_name=str(common["model_name"]),
        benchmark=str(common["benchmark"]),
        dataset_id=str(common["dataset_id"]),
        task_name=str(common["task_name"]),
        task_key=str(common["task_key"]),
        result_path=str(common["result_path"]),
        base_score=base_score,
        rerank_score=rerank_score,
        rerank_lift=rerank_score - base_score if rerank_score is not None else None,
        rerank_status=_str_or_none(reranking.get("status")),
        rerank_top_k=rerank_top_k,
        candidate_source=_str_or_none(reranking.get("source")),
        candidate_ranking=_str_or_none(config.get("candidate_ranking")),
        bm25_source=_str_or_none(bm25_config.get("source")),
        query_coverage=_float_or_none(coverage.get("query_coverage")),
        relevant_coverage=_float_or_none(coverage.get("relevant_coverage")),
        covered_query_count=_int_or_none(coverage.get("covered_query_count")),
        query_with_relevance_count=_int_or_none(coverage.get("query_with_relevance_count")),
        covered_relevant_count=_int_or_none(coverage.get("covered_relevant_count")),
        relevant_count=_int_or_none(coverage.get("relevant_count")),
        dataset_load_seconds=_float_or_none(evaluation.get("dataset_load_seconds")),
        query_embedding_seconds=_float_or_none(timing.get("query_embedding_seconds")),
        corpus_embedding_seconds=_float_or_none(timing.get("corpus_embedding_seconds")),
        score_and_topk_seconds=_float_or_none(timing.get("score_and_topk_seconds")),
        metric_compute_seconds=_float_or_none(timing.get("metric_compute_seconds")),
        pure_compute_seconds=_float_or_none(timing.get("pure_compute_seconds")),
        wall_seconds=_float_or_none(evaluation.get("wall_seconds")),
        duration_seconds_including_dataset_load=_float_or_none(
            evaluation.get("duration_seconds_including_dataset_load")
        ),
    )


def _first_reranking_evaluation(value: Any) -> dict[str, Any]:
    if not isinstance(value, list):
        return {}
    for item in value:
        if isinstance(item, dict):
            return item
    return {}


def _embedding_evaluations(value: Any) -> list[dict[str, Any]]:
    if not isinstance(value, list):
        return []
    return [item for item in value if isinstance(item, dict)]


def _embedding_evaluation_named(items: list[dict[str, Any]], name: str) -> dict[str, Any] | None:
    for item in items:
        if item.get("name") == name:
            return item
    return None


def _embedding_dim(item: dict[str, Any] | None) -> int | None:
    if item is None:
        return None
    dimensions = item.get("embedding_dimensions")
    if not isinstance(dimensions, dict):
        return None
    return _int_or_none(dimensions.get("dim"))


def _quantization_precision(item: dict[str, Any] | None) -> str | None:
    if item is None:
        return None
    metadata = item.get("embedding_metadata")
    if isinstance(metadata, dict):
        for key in ("query", "corpus"):
            side = metadata.get(key)
            if not isinstance(side, dict):
                continue
            quantization = side.get("quantization")
            if isinstance(quantization, dict) and quantization.get("precision"):
                return str(quantization["precision"])
    transform = item.get("transform")
    if isinstance(transform, dict):
        for step in transform.get("steps", []):
            if isinstance(step, dict) and step.get("type") == "quantize" and step.get("parameters"):
                parameters = step["parameters"]
                if isinstance(parameters, dict) and parameters.get("precision"):
                    return str(parameters["precision"])
    return None


def compute_standings(
    rows: list[TaskResult],
    *,
    target_benchmarks: Sequence[str] | None = None,
) -> tuple[dict[str, list[dict[str, Any]]], list[dict[str, Any]]]:
    standings: dict[str, list[dict[str, Any]]] = {}
    all_borda_rows: list[dict[str, Any]] = []
    views = ["Overall", *(target_benchmarks or TARGET_BENCHMARKS)]
    for view in views:
        view_rows = rows if view == "Overall" else [row for row in rows if row.benchmark == view]
        expected_task_count = len({row.task_key for row in view_rows})
        counts_by_model: dict[str, int] = defaultdict(int)
        rows_by_model: dict[str, list[TaskResult]] = defaultdict(list)
        for row in view_rows:
            counts_by_model[row.model_name] += 1
            rows_by_model[row.model_name].append(row)
        complete_models = sorted(model for model, count in counts_by_model.items() if count == expected_task_count)
        complete_set = set(complete_models)
        complete_rows = [row for row in view_rows if row.model_name in complete_set]
        task_rows: dict[str, list[TaskResult]] = defaultdict(list)
        for row in complete_rows:
            task_rows[row.task_key].append(row)

        borda_by_model: dict[str, list[float]] = defaultdict(list)
        for task_key, task_group in task_rows.items():
            ranked = ranks_desc([(row.model_name, row.score) for row in task_group])
            n_models = len(ranked)
            rank_by_model = {model: rank for model, rank in ranked}
            for row in task_group:
                rank = rank_by_model[row.model_name]
                borda = 100.0 if n_models <= 1 else 100.0 * (n_models - rank) / (n_models - 1)
                borda_by_model[row.model_name].append(borda)
                all_borda_rows.append(
                    {
                        "view_name": view,
                        "model_name": row.model_name,
                        "benchmark": row.benchmark,
                        "task_key": task_key,
                        "rank": rank,
                        "model_count": n_models,
                        "borda_score": borda,
                        "score": row.score,
                    }
                )

        model_rows: list[dict[str, Any]] = []
        for model_name in complete_models:
            model_task_rows = rows_by_model[model_name]
            score_mean = mean(row.score for row in model_task_rows)
            borda_score = mean(borda_by_model[model_name])
            first = model_task_rows[0]
            model_rows.append(
                {
                    "view": view,
                    "model": model_name,
                    "task_count": len(model_task_rows),
                    "mean_score": score_mean * 100.0,
                    "borda_score": borda_score,
                    "active_parameters": first.active_parameters,
                    "total_parameters": first.total_parameters,
                    "max_seq_length": first.max_seq_length,
                    "dtype": first.dtype,
                    "attn_implementation": first.attn_implementation,
                    "torch_version": first.torch_version,
                    "transformers_version": first.transformers_version,
                    "sentence_transformers_version": first.sentence_transformers_version,
                }
            )
        apply_rank(model_rows, value_key="mean_score", rank_key="score_rank")
        apply_rank(model_rows, value_key="borda_score", rank_key="borda_rank")
        model_rows.sort(key=lambda item: (item["borda_rank"], item["score_rank"], item["model"]))
        standings[view] = model_rows
    return standings, all_borda_rows


def ranks_desc(items: list[tuple[str, float]]) -> list[tuple[str, float]]:
    sorted_items = sorted(items, key=lambda item: (-item[1], item[0]))
    ranks: list[tuple[str, float]] = []
    index = 0
    while index < len(sorted_items):
        end = index + 1
        while end < len(sorted_items) and sorted_items[end][1] == sorted_items[index][1]:
            end += 1
        average_rank = (index + 1 + end) / 2.0
        ranks.extend((model, average_rank) for model, _ in sorted_items[index:end])
        index = end
    return ranks


def apply_rank(rows: list[dict[str, Any]], *, value_key: str, rank_key: str) -> None:
    ranked = ranks_desc([(row["model"], float(row[value_key])) for row in rows])
    rank_by_model = {model: rank for model, rank in ranked}
    for row in rows:
        row[rank_key] = rank_by_model[row["model"]]


def _create_runs_table(con: duckdb.DuckDBPyConnection) -> None:
    con.execute(
        """
        CREATE TABLE runs (
            model_dir VARCHAR, model_name VARCHAR,
            generated_at_utc VARCHAR, started_at_utc VARCHAR, finished_at_utc VARCHAR,
            target_count INTEGER, split_count INTEGER, cache_hit_count INTEGER, evaluated_count INTEGER,
            aggregate_metric_mean DOUBLE, active_parameters BIGINT, total_parameters BIGINT,
            max_seq_length INTEGER, dtype VARCHAR, attn_implementation VARCHAR,
            torch_version VARCHAR, transformers_version VARCHAR, sentence_transformers_version VARCHAR
        )
        """
    )


def _create_task_results_table(con: duckdb.DuckDBPyConnection, table_name: str = "task_results") -> None:
    con.execute(
        f"""
        CREATE TABLE {table_name} (
            model_dir VARCHAR, model_name VARCHAR,
            model_revision VARCHAR, model_revision_requested VARCHAR,
            benchmark VARCHAR,
            dataset_id VARCHAR, dataset_revision VARCHAR, dataset_revision_requested VARCHAR,
            dataset_name VARCHAR, split_name VARCHAR, task_name VARCHAR, task_key VARCHAR,
            score DOUBLE, score_100 DOUBLE, aggregate_metric VARCHAR, result_path VARCHAR,
            experiment_fingerprint VARCHAR,
            active_parameters BIGINT, total_parameters BIGINT, max_seq_length INTEGER, dtype VARCHAR,
            embedding_variant_name VARCHAR, embedding_dim INTEGER, quantization VARCHAR,
            attn_implementation VARCHAR,
            query_prompt VARCHAR, document_prompt VARCHAR, query_prompt_name VARCHAR, document_prompt_name VARCHAR,
            query_encode_task VARCHAR, document_encode_task VARCHAR, trust_remote_code BOOLEAN,
            late_interaction_query_length INTEGER,
            late_interaction_document_length INTEGER,
            late_interaction_query_prefix VARCHAR,
            late_interaction_document_prefix VARCHAR,
            late_interaction_query_expansion BOOLEAN,
            late_interaction_attend_to_expansion_tokens BOOLEAN,
            torch_version VARCHAR, transformers_version VARCHAR,
            sentence_transformers_version VARCHAR, started_at_utc VARCHAR, finished_at_utc VARCHAR,
            evaluated_at_utc VARCHAR, duration_seconds_including_dataset_load DOUBLE, wall_seconds DOUBLE
        )
        """
    )


def _create_metrics_long_table(con: duckdb.DuckDBPyConnection, table_name: str = "metrics_long") -> None:
    con.execute(
        f"""
        CREATE TABLE {table_name} (
            model_dir VARCHAR, model_name VARCHAR, benchmark VARCHAR,
            dataset_id VARCHAR, task_name VARCHAR, metric_name VARCHAR, metric_value DOUBLE,
            result_path VARCHAR, score_target VARCHAR, embedding_variant_name VARCHAR
        )
        """
    )


def _create_retrieval_rankings_table(con: duckdb.DuckDBPyConnection, table_name: str = "retrieval_rankings") -> None:
    con.execute(
        f"""
        CREATE TABLE {table_name} (
            model_dir VARCHAR, model_name VARCHAR, benchmark VARCHAR,
            dataset_id VARCHAR, dataset_revision VARCHAR, dataset_name VARCHAR,
            split_name VARCHAR, task_name VARCHAR, task_key VARCHAR,
            result_path VARCHAR, ranking_path VARCHAR, ranking_name VARCHAR,
            ranking_kind VARCHAR, embedding_variant_name VARCHAR, distance VARCHAR,
            score_name VARCHAR, query_id VARCHAR, rank INTEGER, corpus_id VARCHAR
        )
        """
    )


def _create_task_diagnostics_table(con: duckdb.DuckDBPyConnection, table_name: str = "task_diagnostics") -> None:
    con.execute(
        f"""
        CREATE TABLE {table_name} (
            model_dir VARCHAR, model_name VARCHAR, benchmark VARCHAR, dataset_id VARCHAR,
            task_name VARCHAR, task_key VARCHAR, result_path VARCHAR,
            base_score DOUBLE, rerank_score DOUBLE, rerank_lift DOUBLE,
            rerank_status VARCHAR, rerank_top_k INTEGER, candidate_source VARCHAR,
            candidate_ranking VARCHAR, bm25_source VARCHAR,
            query_coverage DOUBLE, relevant_coverage DOUBLE,
            covered_query_count INTEGER, query_with_relevance_count INTEGER,
            covered_relevant_count INTEGER, relevant_count INTEGER,
            dataset_load_seconds DOUBLE, query_embedding_seconds DOUBLE,
            corpus_embedding_seconds DOUBLE, score_and_topk_seconds DOUBLE,
            metric_compute_seconds DOUBLE, pure_compute_seconds DOUBLE,
            wall_seconds DOUBLE, duration_seconds_including_dataset_load DOUBLE
        )
        """
    )


def _create_dataset_metadata_table(con: duckdb.DuckDBPyConnection, table_name: str = "dataset_metadata") -> None:
    con.execute(
        f"""
        CREATE TABLE {table_name} (
            benchmark VARCHAR, dataset_id VARCHAR, dataset_name VARCHAR, split_name VARCHAR,
            task_name VARCHAR, task_key VARCHAR, language VARCHAR, languages VARCHAR[],
            primary_languages VARCHAR[], category VARCHAR,
            short_description VARCHAR, citation_count INTEGER, reference_count INTEGER,
            has_bibtex BOOLEAN, query_count INTEGER, document_count INTEGER,
            query_mean_chars DOUBLE, document_mean_chars DOUBLE
        )
        """
    )


def write_duckdb_streaming_results(
    results_dir: Path | Sequence[Path],
    db_path: Path,
    *,
    benchmark_configs: Sequence[BenchmarkConfig],
    include_retrieval_rankings: bool = False,
    model_cards_path: Path | None = DEFAULT_MODEL_CARDS_PATH,
    exclude_model_names: set[str] | None = None,
    model_name_override: str | None = None,
    duplicate_result_policy: DuplicateResultPolicy = "first-wins",
    memory_monitor: MemoryMonitor | None = None,
    result_selection_workers: int = 1,
    result_json_workers: int = 1,
    result_row_workers: int = 1,
    include_result_extensions: bool = False,
    insert_chunk_size: int = STREAM_RESULT_INSERT_CHUNK_SIZE,
) -> None:
    db_path.parent.mkdir(parents=True, exist_ok=True)
    target_benchmarks = set(target_benchmark_names(benchmark_configs))
    selected_results = _selected_result_jsons(
        results_dir,
        benchmark_configs=benchmark_configs,
        target_benchmarks=target_benchmarks,
        exclude_model_names=exclude_model_names or set(),
        duplicate_result_policy=duplicate_result_policy,
        include_retrieval_rankings=include_retrieval_rankings,
        memory_monitor=memory_monitor,
        result_selection_workers=result_selection_workers,
        retain_summary_payload=False,
        model_name_override=model_name_override,
    )
    loaded_at = datetime.now(timezone.utc).replace(microsecond=0).isoformat()
    source_rows = _source_load_state_rows_from_selected_results(
        selected_results,
        batch_id=None,
        loaded_at_utc=loaded_at,
    )
    resolved_batch_id = _source_batch_id(source_rows, loaded_at)
    source_rows = [row | {"last_successful_batch_id": resolved_batch_id} for row in source_rows]
    previous_source_hashes = _read_previous_source_hashes(db_path)
    changed_count = sum(1 for row in source_rows if previous_source_hashes.get(row["result_path"]) != row["payload_sha256"])
    model_cards_source_path, model_cards_sha256 = _model_cards_state(model_cards_path)
    registry = DatasetRegistry.load_builtin()
    model_cards = load_model_cards(model_cards_path)
    run_accumulators: dict[str, dict[str, Any]] = {}

    con = duckdb.connect(str(db_path))
    try:
        for table in WAREHOUSE_TABLES:
            con.execute(f"DROP TABLE IF EXISTS {table}")
        for table in (
            "task_results_raw",
            "metrics_long_raw",
            "retrieval_rankings_raw",
            "task_diagnostics_raw",
            "dataset_metadata_raw",
        ):
            con.execute(f"DROP TABLE IF EXISTS {table}")
        _create_schema_evolution_tables(
            con,
            source_rows=source_rows,
            batch_id=resolved_batch_id,
            loaded_at_utc=loaded_at,
            include_result_extensions=include_result_extensions,
            model_cards_path=model_cards_source_path,
            model_cards_sha256=model_cards_sha256,
        )
        _create_ingestion_state_tables(
            con,
            batch_id=resolved_batch_id,
            loaded_at_utc=loaded_at,
            source_rows=source_rows,
            changed_count=changed_count,
        )
        _create_runs_table(con)
        _create_task_results_table(con, "task_results_raw")
        _create_metrics_long_table(con, "metrics_long_raw")
        _create_retrieval_rankings_table(con, "retrieval_rankings_raw")
        _create_task_diagnostics_table(con, "task_diagnostics_raw")
        _create_dataset_metadata_table(con, "dataset_metadata_raw")

        buffers = _StreamingDuckDbBuffers(con=con, chunk_size=max(1, insert_chunk_size))
        processed_result_count = 0
        for processed in _processed_result_rows(
            selected_results,
            registry=registry,
            model_cards=model_cards,
            model_cards_path=model_cards_path,
            include_retrieval_rankings=include_retrieval_rankings,
            result_json_workers=result_json_workers,
            result_row_workers=result_row_workers,
        ):
            if processed is None:
                continue
            processed_result_count += 1
            if memory_monitor is not None:
                memory_monitor.maybe_sample("result_json_loaded", processed_count=processed_result_count)
            _merge_run_accumulators(run_accumulators, processed.run_accumulators)
            buffers.add(processed)
        buffers.flush()

        runs = _runs_from_task_results(run_accumulators)
        _insert_runs(con, runs)
        _materialize_streamed_result_tables(con)
        _create_metric_dimension_and_fact_tables(con)
        _create_fact_task_score_table(con)
        _create_canonical_dimension_tables(con)
        _create_viewer_task_results_table(con)
        _create_viewer_filter_values_table(con)
        _create_empty_viewer_leaderboard_rows_table(con)
        _create_empty_viewer_leaderboard_language_options_table(con)
        _create_empty_model_score_tables(con)
        for table in (
            "task_results_raw",
            "metrics_long_raw",
            "retrieval_rankings_raw",
            "task_diagnostics_raw",
            "dataset_metadata_raw",
        ):
            con.execute(f"DROP TABLE IF EXISTS {table}")
        if memory_monitor is not None:
            task_row = con.execute("SELECT count(*) FROM task_results").fetchone()
            memory_monitor.sample(
                "load_results_complete",
                processed_count=int(task_row[0]) if task_row is not None else processed_result_count,
            )
    finally:
        con.close()
    _compact_duckdb_database(db_path)


@dataclass
class _StreamingDuckDbBuffers:
    con: duckdb.DuckDBPyConnection
    chunk_size: int
    task_rows: list[TaskResult] = field(default_factory=list)
    metric_rows: list[MetricLongRow] = field(default_factory=list)
    diagnostic_rows: list[TaskDiagnosticRow] = field(default_factory=list)
    dataset_metadata_rows: list[DatasetMetadataRow] = field(default_factory=list)
    ranking_rows: list[RetrievalRankingRow] = field(default_factory=list)

    def add(self, processed: ProcessedResultRows) -> None:
        self.task_rows.extend(processed.rows)
        self.metric_rows.extend(processed.metric_rows)
        self.diagnostic_rows.extend(processed.diagnostic_rows)
        self.dataset_metadata_rows.extend(processed.dataset_metadata_rows)
        self.ranking_rows.extend(processed.ranking_rows)
        self.flush_ready()

    def flush_ready(self) -> None:
        if len(self.task_rows) >= self.chunk_size:
            self._flush_task_rows()
        if len(self.metric_rows) >= self.chunk_size:
            self._flush_metric_rows()
        if len(self.diagnostic_rows) >= self.chunk_size:
            self._flush_diagnostic_rows()
        if len(self.dataset_metadata_rows) >= self.chunk_size:
            self._flush_dataset_metadata_rows()
        if len(self.ranking_rows) >= self.chunk_size:
            self._flush_ranking_rows()

    def flush(self) -> None:
        self._flush_task_rows()
        self._flush_metric_rows()
        self._flush_diagnostic_rows()
        self._flush_dataset_metadata_rows()
        self._flush_ranking_rows()

    def _flush_task_rows(self) -> None:
        if not self.task_rows:
            return
        rows = self.task_rows
        self.task_rows = []
        _insert_duckdb_rows(self.con, "task_results_raw", TASK_RESULT_COLUMNS, (row.duckdb_values() for row in rows))

    def _flush_metric_rows(self) -> None:
        if not self.metric_rows:
            return
        rows = self.metric_rows
        self.metric_rows = []
        _insert_duckdb_rows(self.con, "metrics_long_raw", METRIC_LONG_COLUMNS, (row.duckdb_values() for row in rows))

    def _flush_diagnostic_rows(self) -> None:
        if not self.diagnostic_rows:
            return
        rows = self.diagnostic_rows
        self.diagnostic_rows = []
        _insert_duckdb_rows(self.con, "task_diagnostics_raw", TASK_DIAGNOSTIC_COLUMNS, (row.duckdb_values() for row in rows))

    def _flush_dataset_metadata_rows(self) -> None:
        if not self.dataset_metadata_rows:
            return
        rows = self.dataset_metadata_rows
        self.dataset_metadata_rows = []
        _insert_duckdb_rows(self.con, "dataset_metadata_raw", DATASET_METADATA_COLUMNS, (row.duckdb_values() for row in rows))

    def _flush_ranking_rows(self) -> None:
        if not self.ranking_rows:
            return
        rows = self.ranking_rows
        self.ranking_rows = []
        _insert_duckdb_rows(self.con, "retrieval_rankings_raw", RETRIEVAL_RANKING_COLUMNS, (row.duckdb_values() for row in rows))


def _source_load_state_rows_from_selected_results(
    selected_results: Sequence[SelectedResultJson],
    *,
    batch_id: str | None,
    loaded_at_utc: str,
) -> list[dict[str, Any]]:
    source_rows: list[dict[str, Any]] = []
    for selected in sorted(selected_results, key=lambda item: str(item.result_path)):
        result_path = str(selected.result_path)
        source_rows.append(
            {
                "result_path": result_path,
                "payload_sha256": selected.payload_sha256,
                "canonical_key_hash": hashlib.sha256(result_path.encode("utf-8")).hexdigest(),
                "last_successful_batch_id": batch_id,
                "loaded_at_utc": loaded_at_utc,
            }
        )
    return source_rows


def _insert_runs(con: duckdb.DuckDBPyConnection, runs: Sequence[dict[str, Any]]) -> None:
    _insert_duckdb_rows(
        con,
        "runs",
        (
            "model_dir",
            "model_name",
            "generated_at_utc",
            "started_at_utc",
            "finished_at_utc",
            "target_count",
            "split_count",
            "cache_hit_count",
            "evaluated_count",
            "aggregate_metric_mean",
            "active_parameters",
            "total_parameters",
            "max_seq_length",
            "dtype",
            "attn_implementation",
            "torch_version",
            "transformers_version",
            "sentence_transformers_version",
        ),
        (
            (
                item.get("model_dir"),
                item.get("model_name"),
                item.get("generated_at_utc"),
                item.get("started_at_utc"),
                item.get("finished_at_utc"),
                item.get("target_count"),
                item.get("split_count"),
                item.get("cache_hit_count"),
                item.get("evaluated_count"),
                item.get("aggregate_metric_mean"),
                item.get("active_parameters"),
                item.get("total_parameters"),
                item.get("max_seq_length"),
                item.get("dtype"),
                item.get("attn_implementation"),
                item.get("torch_version"),
                item.get("transformers_version"),
                item.get("sentence_transformers_version"),
            )
            for item in runs
        ),
    )


def _compact_duckdb_database(db_path: Path) -> None:
    if not db_path.exists():
        return
    compact_path = db_path.with_name(f"{db_path.name}.compact.{os.getpid()}.tmp")
    wal_path = db_path.with_name(f"{db_path.name}.wal")
    compact_wal_path = compact_path.with_name(f"{compact_path.name}.wal")
    compact_path.unlink(missing_ok=True)
    compact_wal_path.unlink(missing_ok=True)
    try:
        con = duckdb.connect(str(compact_path))
        try:
            con.execute(f"ATTACH '{db_path}' AS source_db (READ_ONLY)")
            table_names = [
                row[0]
                for row in con.execute(
                    """
                    SELECT table_name
                    FROM duckdb_tables()
                    WHERE database_name = 'source_db'
                      AND schema_name = 'main'
                    ORDER BY table_name
                    """
                ).fetchall()
            ]
            for table_name in table_names:
                escaped = table_name.replace('"', '""')
                con.execute(f'CREATE TABLE "{escaped}" AS SELECT * FROM source_db."{escaped}"')
            con.execute("CHECKPOINT")
        finally:
            con.close()
        os.replace(compact_path, db_path)
        wal_path.unlink(missing_ok=True)
    finally:
        compact_path.unlink(missing_ok=True)
        compact_wal_path.unlink(missing_ok=True)


def _result_path_stem_sql(column_name: str = "result_path") -> str:
    return f"regexp_replace(regexp_extract({column_name}, '[^/]+$'), '\\\\.json(\\\\.gz|\\\\.xz)?$', '')"


def _materialize_streamed_result_tables(con: duckdb.DuckDBPyConnection) -> None:
    task_columns = ", ".join(TASK_RESULT_COLUMNS)
    metric_columns = ", ".join(METRIC_LONG_COLUMNS)
    diagnostic_columns = ", ".join(TASK_DIAGNOSTIC_COLUMNS)
    metadata_columns = ", ".join(DATASET_METADATA_COLUMNS)
    ranking_columns = ", ".join(RETRIEVAL_RANKING_COLUMNS)
    task_stem = _result_path_stem_sql("result_path")
    # Keep long repeated path strings clustered. Without an explicit final
    # order, DuckDB may persist window-output rows in a scattered order, which
    # weakens dictionary compression and can make the warehouse hundreds of MiB
    # larger.
    con.execute(
        f"""
        CREATE TABLE task_results AS
        SELECT {task_columns}
        FROM (
            SELECT *,
                   row_number() OVER (
                       PARTITION BY model_name, benchmark, dataset_id, task_key,
                                    embedding_variant_name, embedding_dim, quantization
                       ORDER BY CASE WHEN {task_stem} = task_name THEN 0 ELSE 1 END, result_path
                   ) AS _rn
            FROM task_results_raw
        )
        WHERE _rn = 1
        ORDER BY result_path, model_name, benchmark, dataset_id, task_key,
                 embedding_variant_name, embedding_dim, quantization
        """
    )
    con.execute(
        f"""
        CREATE TABLE metrics_long AS
        SELECT {metric_columns}
        FROM (
            SELECT *,
                   row_number() OVER (
                       PARTITION BY model_name, benchmark, dataset_id, task_name,
                                    score_target, embedding_variant_name, metric_name
                       ORDER BY CASE WHEN {task_stem} = task_name THEN 0 ELSE 1 END, result_path
                   ) AS _rn
            FROM metrics_long_raw
        )
        WHERE _rn = 1
        ORDER BY result_path, metric_name, score_target, embedding_variant_name,
                 model_name, benchmark, dataset_id, task_name
        """
    )
    con.execute(
        f"""
        CREATE TABLE task_diagnostics AS
        SELECT {diagnostic_columns}
        FROM (
            SELECT *,
                   row_number() OVER (
                       PARTITION BY model_name, benchmark, dataset_id, task_key
                       ORDER BY CASE WHEN {task_stem} = task_name THEN 0 ELSE 1 END, result_path
                   ) AS _rn
            FROM task_diagnostics_raw
        )
        WHERE _rn = 1
        ORDER BY result_path, model_name, benchmark, dataset_id, task_key
        """
    )
    con.execute(
        f"""
        CREATE TABLE dataset_metadata AS
        SELECT {metadata_columns}
        FROM (
            SELECT *,
                   row_number() OVER (
                       PARTITION BY task_key
                       ORDER BY benchmark, dataset_id, task_name
                   ) AS _rn
            FROM dataset_metadata_raw
        )
        WHERE _rn = 1
        ORDER BY benchmark, dataset_id, task_name, task_key
        """
    )
    con.execute(
        f"""
        CREATE TABLE retrieval_rankings AS
        SELECT DISTINCT {ranking_columns}
        FROM retrieval_rankings_raw
        ORDER BY result_path, ranking_path, ranking_name, query_id, rank
        """
    )


def _create_empty_model_score_tables(con: duckdb.DuckDBPyConnection) -> None:
    con.execute(
        """
        CREATE TABLE model_scores (
            view_name VARCHAR, model_name VARCHAR, task_count INTEGER,
            mean_score DOUBLE, score_rank DOUBLE, borda_score DOUBLE, borda_rank DOUBLE,
            active_parameters BIGINT, total_parameters BIGINT, max_seq_length INTEGER, dtype VARCHAR,
            attn_implementation VARCHAR, torch_version VARCHAR, transformers_version VARCHAR,
            sentence_transformers_version VARCHAR
        )
        """
    )
    con.execute(
        """
        CREATE TABLE borda_task_scores (
            view_name VARCHAR, model_name VARCHAR, benchmark VARCHAR, task_key VARCHAR,
            rank DOUBLE, model_count INTEGER, borda_score DOUBLE, score DOUBLE
        )
        """
    )


def write_duckdb(
    db_path: Path,
    *,
    runs: list[dict[str, Any]],
    rows: list[TaskResult],
    metric_rows: Sequence[MetricLongRow | dict[str, Any]],
    ranking_rows: Sequence[RetrievalRankingRow | dict[str, Any]] = (),
    diagnostic_rows: Sequence[TaskDiagnosticRow | dict[str, Any]] = (),
    dataset_metadata_rows: Sequence[DatasetMetadataRow | dict[str, Any]] = (),
    standings: dict[str, list[dict[str, Any]]],
    borda_rows: list[dict[str, Any]],
    batch_id: str | None = None,
    loaded_at_utc: str | None = None,
    include_result_extensions: bool = False,
    model_cards_path: Path | None = DEFAULT_MODEL_CARDS_PATH,
    source_payload_sha256_by_path: dict[str, str | None] | None = None,
) -> None:
    db_path.parent.mkdir(parents=True, exist_ok=True)
    normalized_metric_rows = [
        row if isinstance(row, MetricLongRow) else MetricLongRow.model_validate(row)
        for row in metric_rows
    ]
    normalized_ranking_rows = [
        row if isinstance(row, RetrievalRankingRow) else RetrievalRankingRow.model_validate(row)
        for row in ranking_rows
    ]
    normalized_diagnostic_rows = [
        row if isinstance(row, TaskDiagnosticRow) else TaskDiagnosticRow.model_validate(row)
        for row in diagnostic_rows
    ]
    normalized_dataset_metadata_rows = [
        row if isinstance(row, DatasetMetadataRow) else DatasetMetadataRow.model_validate(row)
        for row in dataset_metadata_rows
    ]
    loaded_at = loaded_at_utc or datetime.now(timezone.utc).replace(microsecond=0).isoformat()
    source_rows = _source_load_state_rows(
        rows=rows,
        metric_rows=normalized_metric_rows,
        diagnostic_rows=normalized_diagnostic_rows,
        ranking_rows=normalized_ranking_rows,
        batch_id=batch_id,
        loaded_at_utc=loaded_at,
        payload_sha256_by_path=source_payload_sha256_by_path,
    )
    resolved_batch_id = batch_id or _source_batch_id(source_rows, loaded_at)
    source_rows = [row | {"last_successful_batch_id": resolved_batch_id} for row in source_rows]
    model_cards_source_path, model_cards_sha256 = _model_cards_state(model_cards_path)
    previous_source_hashes = _read_previous_source_hashes(db_path)
    changed_count = sum(1 for row in source_rows if previous_source_hashes.get(row["result_path"]) != row["payload_sha256"])
    con = duckdb.connect(str(db_path))
    try:
        for table in WAREHOUSE_TABLES:
            con.execute(f"DROP TABLE IF EXISTS {table}")
        _create_schema_evolution_tables(
            con,
            source_rows=source_rows,
            batch_id=resolved_batch_id,
            loaded_at_utc=loaded_at,
            include_result_extensions=include_result_extensions,
            model_cards_path=model_cards_source_path,
            model_cards_sha256=model_cards_sha256,
        )
        _create_ingestion_state_tables(
            con,
            batch_id=resolved_batch_id,
            loaded_at_utc=loaded_at,
            source_rows=source_rows,
            changed_count=changed_count,
        )
        con.execute(
            """
            CREATE TABLE runs (
                model_dir VARCHAR, model_name VARCHAR,
                generated_at_utc VARCHAR, started_at_utc VARCHAR, finished_at_utc VARCHAR,
                target_count INTEGER, split_count INTEGER, cache_hit_count INTEGER, evaluated_count INTEGER,
                aggregate_metric_mean DOUBLE, active_parameters BIGINT, total_parameters BIGINT,
                max_seq_length INTEGER, dtype VARCHAR, attn_implementation VARCHAR,
                torch_version VARCHAR, transformers_version VARCHAR, sentence_transformers_version VARCHAR
            )
            """
        )
        _insert_duckdb_rows(
            con,
            "runs",
            (
                "model_dir",
                "model_name",
                "generated_at_utc",
                "started_at_utc",
                "finished_at_utc",
                "target_count",
                "split_count",
                "cache_hit_count",
                "evaluated_count",
                "aggregate_metric_mean",
                "active_parameters",
                "total_parameters",
                "max_seq_length",
                "dtype",
                "attn_implementation",
                "torch_version",
                "transformers_version",
                "sentence_transformers_version",
            ),
            (
                (
                    item.get("model_dir"),
                    item.get("model_name"),
                    item.get("generated_at_utc"),
                    item.get("started_at_utc"),
                    item.get("finished_at_utc"),
                    item.get("target_count"),
                    item.get("split_count"),
                    item.get("cache_hit_count"),
                    item.get("evaluated_count"),
                    item.get("aggregate_metric_mean"),
                    item.get("active_parameters"),
                    item.get("total_parameters"),
                    item.get("max_seq_length"),
                    item.get("dtype"),
                    item.get("attn_implementation"),
                    item.get("torch_version"),
                    item.get("transformers_version"),
                    item.get("sentence_transformers_version"),
                )
                for item in runs
            ),
        )
        con.execute(
            """
            CREATE TABLE task_results (
                model_dir VARCHAR, model_name VARCHAR,
                model_revision VARCHAR, model_revision_requested VARCHAR,
                benchmark VARCHAR,
                dataset_id VARCHAR, dataset_revision VARCHAR, dataset_revision_requested VARCHAR,
                dataset_name VARCHAR, split_name VARCHAR, task_name VARCHAR, task_key VARCHAR,
                score DOUBLE, score_100 DOUBLE, aggregate_metric VARCHAR, result_path VARCHAR,
                experiment_fingerprint VARCHAR,
                active_parameters BIGINT, total_parameters BIGINT, max_seq_length INTEGER, dtype VARCHAR,
                embedding_variant_name VARCHAR, embedding_dim INTEGER, quantization VARCHAR,
                attn_implementation VARCHAR,
                query_prompt VARCHAR, document_prompt VARCHAR, query_prompt_name VARCHAR, document_prompt_name VARCHAR,
                query_encode_task VARCHAR, document_encode_task VARCHAR, trust_remote_code BOOLEAN,
                late_interaction_query_length INTEGER,
                late_interaction_document_length INTEGER,
                late_interaction_query_prefix VARCHAR,
                late_interaction_document_prefix VARCHAR,
                late_interaction_query_expansion BOOLEAN,
                late_interaction_attend_to_expansion_tokens BOOLEAN,
                torch_version VARCHAR, transformers_version VARCHAR,
                sentence_transformers_version VARCHAR, started_at_utc VARCHAR, finished_at_utc VARCHAR,
                evaluated_at_utc VARCHAR, duration_seconds_including_dataset_load DOUBLE, wall_seconds DOUBLE
            )
            """
        )
        _insert_duckdb_rows(
            con,
            "task_results",
            (
                "model_dir",
                "model_name",
                "model_revision",
                "model_revision_requested",
                "benchmark",
                "dataset_id",
                "dataset_revision",
                "dataset_revision_requested",
                "dataset_name",
                "split_name",
                "task_name",
                "task_key",
                "score",
                "score_100",
                "aggregate_metric",
                "result_path",
                "experiment_fingerprint",
                "active_parameters",
                "total_parameters",
                "max_seq_length",
                "dtype",
                "embedding_variant_name",
                "embedding_dim",
                "quantization",
                "attn_implementation",
                "query_prompt",
                "document_prompt",
                "query_prompt_name",
                "document_prompt_name",
                "query_encode_task",
                "document_encode_task",
                "trust_remote_code",
                "late_interaction_query_length",
                "late_interaction_document_length",
                "late_interaction_query_prefix",
                "late_interaction_document_prefix",
                "late_interaction_query_expansion",
                "late_interaction_attend_to_expansion_tokens",
                "torch_version",
                "transformers_version",
                "sentence_transformers_version",
                "started_at_utc",
                "finished_at_utc",
                "evaluated_at_utc",
                "duration_seconds_including_dataset_load",
                "wall_seconds",
            ),
            (row.duckdb_values() for row in rows),
        )
        con.execute(
            """
            CREATE TABLE metrics_long (
                model_dir VARCHAR, model_name VARCHAR, benchmark VARCHAR,
                dataset_id VARCHAR, task_name VARCHAR, metric_name VARCHAR, metric_value DOUBLE,
                result_path VARCHAR, score_target VARCHAR, embedding_variant_name VARCHAR
            )
            """
        )
        _insert_duckdb_rows(
            con,
            "metrics_long",
            (
                "model_dir",
                "model_name",
                "benchmark",
                "dataset_id",
                "task_name",
                "metric_name",
                "metric_value",
                "result_path",
                "score_target",
                "embedding_variant_name",
            ),
            (row.duckdb_values() for row in normalized_metric_rows),
        )
        _create_metric_dimension_and_fact_tables(con)
        con.execute(
            """
            CREATE TABLE retrieval_rankings (
                model_dir VARCHAR, model_name VARCHAR, benchmark VARCHAR,
                dataset_id VARCHAR, dataset_revision VARCHAR, dataset_name VARCHAR,
                split_name VARCHAR, task_name VARCHAR, task_key VARCHAR,
                result_path VARCHAR, ranking_path VARCHAR, ranking_name VARCHAR,
                ranking_kind VARCHAR, embedding_variant_name VARCHAR, distance VARCHAR,
                score_name VARCHAR, query_id VARCHAR, rank INTEGER, corpus_id VARCHAR
            )
            """
        )
        if normalized_ranking_rows:
            _insert_duckdb_rows(
                con,
                "retrieval_rankings",
                (
                    "model_dir",
                    "model_name",
                    "benchmark",
                    "dataset_id",
                    "dataset_revision",
                    "dataset_name",
                    "split_name",
                    "task_name",
                    "task_key",
                    "result_path",
                    "ranking_path",
                    "ranking_name",
                    "ranking_kind",
                    "embedding_variant_name",
                    "distance",
                    "score_name",
                    "query_id",
                    "rank",
                    "corpus_id",
                ),
                (row.duckdb_values() for row in normalized_ranking_rows),
            )
        con.execute(
            """
            CREATE TABLE task_diagnostics (
                model_dir VARCHAR, model_name VARCHAR, benchmark VARCHAR, dataset_id VARCHAR,
                task_name VARCHAR, task_key VARCHAR, result_path VARCHAR,
                base_score DOUBLE, rerank_score DOUBLE, rerank_lift DOUBLE,
                rerank_status VARCHAR, rerank_top_k INTEGER, candidate_source VARCHAR,
                candidate_ranking VARCHAR, bm25_source VARCHAR,
                query_coverage DOUBLE, relevant_coverage DOUBLE,
                covered_query_count INTEGER, query_with_relevance_count INTEGER,
                covered_relevant_count INTEGER, relevant_count INTEGER,
                dataset_load_seconds DOUBLE, query_embedding_seconds DOUBLE,
                corpus_embedding_seconds DOUBLE, score_and_topk_seconds DOUBLE,
                metric_compute_seconds DOUBLE, pure_compute_seconds DOUBLE,
                wall_seconds DOUBLE, duration_seconds_including_dataset_load DOUBLE
            )
            """
        )
        if normalized_diagnostic_rows:
            _insert_duckdb_rows(
                con,
                "task_diagnostics",
                (
                    "model_dir",
                    "model_name",
                    "benchmark",
                    "dataset_id",
                    "task_name",
                    "task_key",
                    "result_path",
                    "base_score",
                    "rerank_score",
                    "rerank_lift",
                    "rerank_status",
                    "rerank_top_k",
                    "candidate_source",
                    "candidate_ranking",
                    "bm25_source",
                    "query_coverage",
                    "relevant_coverage",
                    "covered_query_count",
                    "query_with_relevance_count",
                    "covered_relevant_count",
                    "relevant_count",
                    "dataset_load_seconds",
                    "query_embedding_seconds",
                    "corpus_embedding_seconds",
                    "score_and_topk_seconds",
                    "metric_compute_seconds",
                    "pure_compute_seconds",
                    "wall_seconds",
                    "duration_seconds_including_dataset_load",
                ),
                (row.duckdb_values() for row in normalized_diagnostic_rows),
            )
        _create_fact_task_score_table(con)
        con.execute(
            """
            CREATE TABLE dataset_metadata (
                benchmark VARCHAR, dataset_id VARCHAR, dataset_name VARCHAR, split_name VARCHAR,
                task_name VARCHAR, task_key VARCHAR, language VARCHAR, languages VARCHAR[],
                primary_languages VARCHAR[], category VARCHAR,
                short_description VARCHAR, citation_count INTEGER, reference_count INTEGER,
                has_bibtex BOOLEAN, query_count INTEGER, document_count INTEGER,
                query_mean_chars DOUBLE, document_mean_chars DOUBLE
            )
            """
        )
        if normalized_dataset_metadata_rows:
            _insert_duckdb_rows(
                con,
                "dataset_metadata",
                (
                    "benchmark",
                    "dataset_id",
                    "dataset_name",
                    "split_name",
                    "task_name",
                    "task_key",
                    "language",
                    "languages",
                    "primary_languages",
                    "category",
                    "short_description",
                    "citation_count",
                    "reference_count",
                    "has_bibtex",
                    "query_count",
                    "document_count",
                    "query_mean_chars",
                    "document_mean_chars",
                ),
                (row.duckdb_values() for row in normalized_dataset_metadata_rows),
            )
        _create_canonical_dimension_tables(con)
        _create_viewer_task_results_table(con)
        _create_viewer_filter_values_table(con)
        _create_empty_viewer_leaderboard_rows_table(con)
        _create_empty_viewer_leaderboard_language_options_table(con)
        score_rows = [row for view_rows in standings.values() for row in view_rows]
        con.execute(
            """
            CREATE TABLE model_scores (
                view_name VARCHAR, model_name VARCHAR, task_count INTEGER,
                mean_score DOUBLE, score_rank DOUBLE, borda_score DOUBLE, borda_rank DOUBLE,
                active_parameters BIGINT, total_parameters BIGINT, max_seq_length INTEGER, dtype VARCHAR,
                attn_implementation VARCHAR, torch_version VARCHAR, transformers_version VARCHAR,
                sentence_transformers_version VARCHAR
            )
            """
        )
        if score_rows:
            _insert_duckdb_rows(
                con,
                "model_scores",
                (
                    "view_name",
                    "model_name",
                    "task_count",
                    "mean_score",
                    "score_rank",
                    "borda_score",
                    "borda_rank",
                    "active_parameters",
                    "total_parameters",
                    "max_seq_length",
                    "dtype",
                    "attn_implementation",
                    "torch_version",
                    "transformers_version",
                    "sentence_transformers_version",
                ),
                (
                    (
                        row.get("view"),
                        row.get("model"),
                        row.get("task_count"),
                        row.get("mean_score"),
                        row.get("score_rank"),
                        row.get("borda_score"),
                        row.get("borda_rank"),
                        row.get("active_parameters"),
                        row.get("total_parameters"),
                        row.get("max_seq_length"),
                        row.get("dtype"),
                        row.get("attn_implementation"),
                        row.get("torch_version"),
                        row.get("transformers_version"),
                        row.get("sentence_transformers_version"),
                    )
                    for row in score_rows
                ),
            )
        con.execute(
            """
            CREATE TABLE borda_task_scores (
                view_name VARCHAR, model_name VARCHAR, benchmark VARCHAR, task_key VARCHAR,
                rank DOUBLE, model_count INTEGER, borda_score DOUBLE, score DOUBLE
            )
            """
        )
        if borda_rows:
            _insert_duckdb_rows(
                con,
                "borda_task_scores",
                (
                    "view_name",
                    "model_name",
                    "benchmark",
                    "task_key",
                    "rank",
                    "model_count",
                    "borda_score",
                    "score",
                ),
                (
                    (
                        row.get("view_name"),
                        row.get("model_name"),
                        row.get("benchmark"),
                        row.get("task_key"),
                        row.get("rank"),
                        row.get("model_count"),
                        row.get("borda_score"),
                        row.get("score"),
                    )
                    for row in borda_rows
                ),
            )
    finally:
        con.close()


def append_duckdb_results(
    db_path: Path,
    *,
    rows: Sequence[TaskResult],
    metric_rows: Sequence[MetricLongRow | dict[str, Any]],
    ranking_rows: Sequence[RetrievalRankingRow | dict[str, Any]] = (),
    diagnostic_rows: Sequence[TaskDiagnosticRow | dict[str, Any]] = (),
    dataset_metadata_rows: Sequence[DatasetMetadataRow | dict[str, Any]] = (),
    batch_id: str | None = None,
    loaded_at_utc: str | None = None,
    source_payload_sha256_by_path: dict[str, str | None] | None = None,
) -> None:
    if not db_path.exists():
        raise FileNotFoundError(f"Cannot append results because DuckDB does not exist: {db_path}")
    normalized_metric_rows = [
        row if isinstance(row, MetricLongRow) else MetricLongRow.model_validate(row)
        for row in metric_rows
    ]
    normalized_ranking_rows = [
        row if isinstance(row, RetrievalRankingRow) else RetrievalRankingRow.model_validate(row)
        for row in ranking_rows
    ]
    normalized_diagnostic_rows = [
        row if isinstance(row, TaskDiagnosticRow) else TaskDiagnosticRow.model_validate(row)
        for row in diagnostic_rows
    ]
    normalized_dataset_metadata_rows = [
        row if isinstance(row, DatasetMetadataRow) else DatasetMetadataRow.model_validate(row)
        for row in dataset_metadata_rows
    ]
    if not rows and not normalized_metric_rows and not normalized_diagnostic_rows and not normalized_ranking_rows:
        return
    loaded_at = loaded_at_utc or datetime.now(timezone.utc).replace(microsecond=0).isoformat()
    source_rows = _source_load_state_rows(
        rows=rows,
        metric_rows=normalized_metric_rows,
        diagnostic_rows=normalized_diagnostic_rows,
        ranking_rows=normalized_ranking_rows,
        batch_id=batch_id,
        loaded_at_utc=loaded_at,
        payload_sha256_by_path=source_payload_sha256_by_path,
    )
    resolved_batch_id = batch_id or _source_batch_id(source_rows, loaded_at)
    source_rows = [row | {"last_successful_batch_id": resolved_batch_id} for row in source_rows]
    con = duckdb.connect(str(db_path))
    try:
        _validate_appendable_duckdb(con)
        _ensure_append_rows_are_new(con, rows=rows, source_rows=source_rows)
        if rows:
            _insert_duckdb_rows(con, "task_results", TASK_RESULT_COLUMNS, (row.duckdb_values() for row in rows))
        if normalized_metric_rows:
            _insert_duckdb_rows(
                con,
                "metrics_long",
                METRIC_LONG_COLUMNS,
                (row.duckdb_values() for row in normalized_metric_rows),
            )
        if normalized_ranking_rows:
            _insert_duckdb_rows(
                con,
                "retrieval_rankings",
                RETRIEVAL_RANKING_COLUMNS,
                (row.duckdb_values() for row in normalized_ranking_rows),
            )
        if normalized_diagnostic_rows:
            _insert_duckdb_rows(
                con,
                "task_diagnostics",
                TASK_DIAGNOSTIC_COLUMNS,
                (row.duckdb_values() for row in normalized_diagnostic_rows),
            )
        for metadata_row in normalized_dataset_metadata_rows:
            con.execute("DELETE FROM dataset_metadata WHERE task_key = ?", [metadata_row.task_key])
        if normalized_dataset_metadata_rows:
            _insert_duckdb_rows(
                con,
                "dataset_metadata",
                DATASET_METADATA_COLUMNS,
                (row.duckdb_values() for row in normalized_dataset_metadata_rows),
            )
        if source_rows:
            _insert_duckdb_rows(
                con,
                "source_load_state",
                SOURCE_LOAD_STATE_COLUMNS,
                (
                    (
                        row["result_path"],
                        row["payload_sha256"],
                        row["canonical_key_hash"],
                        row["last_successful_batch_id"],
                        row["loaded_at_utc"],
                    )
                    for row in source_rows
                ),
            )
        source_count_row = con.execute("SELECT count(*) FROM source_load_state").fetchone()
        source_count = int(source_count_row[0]) if source_count_row is not None else 0
        con.execute(
            "INSERT INTO ingestion_batches VALUES (?, ?, ?, ?, ?, ?)",
            [resolved_batch_id, loaded_at, loaded_at, "success", source_count, len(source_rows)],
        )
        con.execute(
            "UPDATE meta_database SET built_at_utc = ?, source_result_count = ?",
            [loaded_at, source_count],
        )
        _rebuild_duckdb_cached_tables(con)
    finally:
        con.close()


def _validate_appendable_duckdb(con: duckdb.DuckDBPyConnection) -> None:
    required_tables = (
        "meta_database",
        "ingestion_batches",
        "source_load_state",
        "runs",
        "task_results",
        "metrics_long",
        "retrieval_rankings",
        "task_diagnostics",
        "dataset_metadata",
    )
    missing_tables = [table for table in required_tables if not _duckdb_table_exists(con, table)]
    if missing_tables:
        raise ValueError(f"Cannot append results because DuckDB is missing tables: {', '.join(missing_tables)}")
    if con.execute("SELECT schema_version FROM meta_database").fetchone() != (WAREHOUSE_SCHEMA_VERSION,):
        raise ValueError("Cannot append results because DuckDB schema version is incompatible")


def _ensure_append_rows_are_new(
    con: duckdb.DuckDBPyConnection,
    *,
    rows: Sequence[TaskResult],
    source_rows: Sequence[dict[str, Any]],
) -> None:
    duplicate_paths = [
        row["result_path"]
        for row in source_rows
        if con.execute("SELECT 1 FROM source_load_state WHERE result_path = ?", [row["result_path"]]).fetchone()
    ]
    if duplicate_paths:
        raise ValueError(f"Cannot append duplicate result paths: {', '.join(sorted(duplicate_paths))}")
    duplicate_tasks = []
    for row in rows:
        if row.embedding_variant_name is not None:
            continue
        if con.execute(
            """
            SELECT 1
            FROM task_results
            WHERE model_name = ?
              AND benchmark = ?
              AND dataset_id = ?
              AND task_key = ?
              AND embedding_variant_name IS NULL
            """,
            [row.model_name, row.benchmark, row.dataset_id, row.task_key],
        ).fetchone():
            duplicate_tasks.append(f"{row.model_name}::{row.task_key}")
    if duplicate_tasks:
        raise ValueError(f"Cannot append duplicate model-task results: {', '.join(sorted(duplicate_tasks))}")


def _rebuild_duckdb_cached_tables(con: duckdb.DuckDBPyConnection) -> None:
    for table in (
        "viewer_leaderboard_language_options",
        "viewer_leaderboard_rows",
        "viewer_filter_values",
        "viewer_task_results",
        "fact_task_score",
        "fact_metric_score",
        "dim_metric",
        "dim_variant",
        "dim_task",
        "dim_model",
        "runs",
    ):
        con.execute(f"DROP TABLE IF EXISTS {table}")
    _create_runs_table_from_task_results(con)
    _create_metric_dimension_and_fact_tables(con)
    _create_fact_task_score_table(con)
    _create_canonical_dimension_tables(con)
    _create_viewer_task_results_table(con)
    _create_viewer_filter_values_table(con)
    _create_empty_viewer_leaderboard_rows_table(con)
    _create_empty_viewer_leaderboard_language_options_table(con)
    if _duckdb_table_exists(con, "model_scores"):
        con.execute("DELETE FROM model_scores")
    if _duckdb_table_exists(con, "borda_task_scores"):
        con.execute("DELETE FROM borda_task_scores")


def _create_runs_table_from_task_results(con: duckdb.DuckDBPyConnection) -> None:
    con.execute(
        """
        CREATE TABLE runs AS
        SELECT
            min(model_dir) AS model_dir,
            model_name,
            NULL::VARCHAR AS generated_at_utc,
            min(started_at_utc) AS started_at_utc,
            max(finished_at_utc) AS finished_at_utc,
            count(DISTINCT dataset_id)::INTEGER AS target_count,
            count(*)::INTEGER AS split_count,
            NULL::INTEGER AS cache_hit_count,
            count(*)::INTEGER AS evaluated_count,
            avg(score) AS aggregate_metric_mean,
            max(active_parameters) AS active_parameters,
            max(total_parameters) AS total_parameters,
            max(max_seq_length) AS max_seq_length,
            max(dtype) AS dtype,
            max(attn_implementation) AS attn_implementation,
            max(torch_version) AS torch_version,
            max(transformers_version) AS transformers_version,
            max(sentence_transformers_version) AS sentence_transformers_version
        FROM task_results
        WHERE embedding_variant_name IS NULL
        GROUP BY model_name
        ORDER BY model_name
        """
    )


def _source_load_state_rows(
    *,
    rows: Sequence[TaskResult],
    metric_rows: Sequence[MetricLongRow],
    diagnostic_rows: Sequence[TaskDiagnosticRow],
    ranking_rows: Sequence[RetrievalRankingRow],
    batch_id: str | None,
    loaded_at_utc: str,
    payload_sha256_by_path: dict[str, str | None] | None = None,
) -> list[dict[str, Any]]:
    result_paths = {
        row.result_path
        for row in [*rows, *metric_rows, *diagnostic_rows, *ranking_rows]
        if row.result_path
    }
    source_rows: list[dict[str, Any]] = []
    for result_path in sorted(result_paths):
        payload_sha256 = (
            payload_sha256_by_path[result_path]
            if payload_sha256_by_path is not None and result_path in payload_sha256_by_path
            else _payload_sha256(result_path)
        )
        canonical_key_hash = hashlib.sha256(result_path.encode("utf-8")).hexdigest()
        source_rows.append(
            {
                "result_path": result_path,
                "payload_sha256": payload_sha256,
                "canonical_key_hash": canonical_key_hash,
                "last_successful_batch_id": batch_id,
                "loaded_at_utc": loaded_at_utc,
            }
        )
    return source_rows


def _payload_sha256(result_path: str) -> str | None:
    path = Path(result_path)
    if not path.exists() or not path.is_file():
        return None
    digest = hashlib.sha256()
    with path.open("rb") as file:
        for chunk in iter(lambda: file.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def _model_cards_state(model_cards_path: Path | None) -> tuple[str | None, str | None]:
    if model_cards_path is None or not model_cards_path.exists():
        return None, None
    if model_cards_path.is_file():
        return str(model_cards_path), hashlib.sha256(model_cards_path.read_bytes()).hexdigest()
    if not model_cards_path.is_dir():
        return None, None
    manifest = [
        (
            str(path.relative_to(model_cards_path)),
            hashlib.sha256(path.read_bytes()).hexdigest(),
        )
        for path in model_card_yaml_paths(model_cards_path)
    ]
    payload = json.dumps(manifest, sort_keys=True, separators=(",", ":"))
    return str(model_cards_path), hashlib.sha256(payload.encode("utf-8")).hexdigest()


def _source_batch_id(source_rows: Sequence[dict[str, Any]], loaded_at_utc: str) -> str:
    payload = json.dumps(
        [(row["result_path"], row["payload_sha256"]) for row in source_rows],
        sort_keys=True,
        separators=(",", ":"),
    )
    digest = hashlib.sha256(f"{loaded_at_utc}\n{payload}".encode("utf-8")).hexdigest()[:16]
    return f"batch-{digest}"


def _create_schema_evolution_tables(
    con: duckdb.DuckDBPyConnection,
    *,
    source_rows: Sequence[dict[str, Any]],
    batch_id: str,
    loaded_at_utc: str,
    include_result_extensions: bool = False,
    model_cards_path: str | None = None,
    model_cards_sha256: str | None = None,
) -> None:
    con.execute(
        """
        CREATE TABLE meta_database (
            schema_version VARCHAR,
            compatibility_level VARCHAR,
            built_at_utc VARCHAR,
            source_result_count INTEGER,
            model_cards_path VARCHAR,
            model_cards_sha256 VARCHAR
        )
        """
    )
    con.execute(
        "INSERT INTO meta_database VALUES (?, ?, ?, ?, ?, ?)",
        [
            WAREHOUSE_SCHEMA_VERSION,
            WAREHOUSE_COMPATIBILITY_LEVEL,
            loaded_at_utc,
            len(source_rows),
            model_cards_path,
            model_cards_sha256,
        ],
    )
    con.execute(
        """
        CREATE TABLE schema_change_log (
            schema_version VARCHAR,
            migration_name VARCHAR,
            applied_at_utc VARCHAR,
            parser_version VARCHAR,
            compatibility_level VARCHAR
        )
        """
    )
    con.execute(
        "INSERT INTO schema_change_log VALUES (?, ?, ?, ?, ?)",
        [
            WAREHOUSE_SCHEMA_VERSION,
            "create_current_warehouse_schema",
            loaded_at_utc,
            WAREHOUSE_SCHEMA_VERSION,
            WAREHOUSE_COMPATIBILITY_LEVEL,
        ],
    )
    con.execute(
        """
        CREATE TABLE result_extensions (
            result_path VARCHAR,
            field_path VARCHAR,
            value_json VARCHAR,
            discovered_batch_id VARCHAR,
            discovered_at_utc VARCHAR
        )
        """
    )
    if include_result_extensions and (
        extension_rows := _result_extension_rows(source_rows=source_rows, batch_id=batch_id, loaded_at_utc=loaded_at_utc)
    ):
        # Extension discovery re-reads every source JSON, so it stays opt-in for
        # offline schema audits instead of running during normal viewer deploys.
        _insert_duckdb_rows(
            con,
            "result_extensions",
            ("result_path", "field_path", "value_json", "discovered_batch_id", "discovered_at_utc"),
            extension_rows,
        )


KNOWN_RESULT_TOP_LEVEL_KEYS = frozenset(
    {
        "artifacts",
        "config",
        "embedding_evaluations",
        "environment",
        "evaluation",
        "experiment_manifest",
        "generated_at_utc",
        "metrics",
        "model",
        "rankings",
        "rerank_metrics",
        "target",
    }
)


def _result_extension_rows(
    *,
    source_rows: Sequence[dict[str, Any]],
    batch_id: str,
    loaded_at_utc: str,
) -> list[tuple[str, str, str, str, str]]:
    extension_rows: list[tuple[str, str, str, str, str]] = []
    for source_row in source_rows:
        result_path = source_row["result_path"]
        path = Path(result_path)
        if not path.exists() or not path.is_file():
            continue
        try:
            payload = _read_json(path)
        except (OSError, orjson.JSONDecodeError):
            continue
        if not isinstance(payload, dict):
            continue
        for key in sorted(set(payload) - KNOWN_RESULT_TOP_LEVEL_KEYS):
            extension_rows.append(
                (
                    result_path,
                    f"$.{key}",
                    json.dumps(payload[key], sort_keys=True, separators=(",", ":")),
                    batch_id,
                    loaded_at_utc,
                )
            )
    return extension_rows


def _read_previous_source_hashes(db_path: Path) -> dict[str, str | None]:
    if not db_path.exists():
        return {}
    con = duckdb.connect(str(db_path), read_only=True)
    try:
        if not _duckdb_table_exists(con, "source_load_state"):
            return {}
        return {
            str(result_path): payload_sha256
            for result_path, payload_sha256 in con.execute(
                "SELECT result_path, payload_sha256 FROM source_load_state"
            ).fetchall()
        }
    finally:
        con.close()


def _duckdb_table_exists(con: duckdb.DuckDBPyConnection, table_name: str) -> bool:
    row = con.execute(
        """
        SELECT count(*)
        FROM information_schema.tables
        WHERE table_name = ?
        """,
        [table_name],
    ).fetchone()
    return bool(row is not None and row[0])


def _create_ingestion_state_tables(
    con: duckdb.DuckDBPyConnection,
    *,
    batch_id: str,
    loaded_at_utc: str,
    source_rows: Sequence[dict[str, Any]],
    changed_count: int,
) -> None:
    con.execute(
        """
        CREATE TABLE ingestion_batches (
            batch_id VARCHAR,
            started_at_utc VARCHAR,
            finished_at_utc VARCHAR,
            status VARCHAR,
            source_count INTEGER,
            changed_count INTEGER
        )
        """
    )
    con.execute(
        "INSERT INTO ingestion_batches VALUES (?, ?, ?, ?, ?, ?)",
        [batch_id, loaded_at_utc, loaded_at_utc, "success", len(source_rows), changed_count],
    )
    con.execute(
        """
        CREATE TABLE source_load_state (
            result_path VARCHAR,
            payload_sha256 VARCHAR,
            canonical_key_hash VARCHAR,
            last_successful_batch_id VARCHAR,
            loaded_at_utc VARCHAR
        )
        """
    )
    if source_rows:
        _insert_duckdb_rows(
            con,
            "source_load_state",
            ("result_path", "payload_sha256", "canonical_key_hash", "last_successful_batch_id", "loaded_at_utc"),
            (
                (
                    row["result_path"],
                    row["payload_sha256"],
                    row["canonical_key_hash"],
                    row["last_successful_batch_id"],
                    row["loaded_at_utc"],
                )
                for row in source_rows
            ),
        )


def _create_canonical_dimension_tables(con: duckdb.DuckDBPyConnection) -> None:
    con.execute(
        """
        CREATE TABLE dim_model AS
        WITH model_values AS (
            SELECT
                model_dir,
                model_name,
                model_revision,
                model_revision_requested,
                max(active_parameters) AS active_parameters,
                max(total_parameters) AS total_parameters,
                max(max_seq_length) AS max_seq_length,
                max(dtype) AS dtype,
                max(attn_implementation) AS attn_implementation,
                max(torch_version) AS torch_version,
                max(transformers_version) AS transformers_version,
                max(sentence_transformers_version) AS sentence_transformers_version
            FROM task_results
            GROUP BY
                model_dir,
                model_name,
                model_revision,
                model_revision_requested
        )
        SELECT
            row_number() OVER (
                ORDER BY
                    model_name,
                    model_dir,
                    COALESCE(model_revision, ''),
                    COALESCE(model_revision_requested, '')
            ) AS model_id,
            *
        FROM model_values
        ORDER BY model_id
        """
    )
    con.execute(
        """
        CREATE TABLE dim_task AS
        WITH task_values AS (
            SELECT
                tr.benchmark,
                tr.dataset_id,
                max(tr.dataset_revision) AS dataset_revision,
                max(tr.dataset_revision_requested) AS dataset_revision_requested,
                max(tr.dataset_name) AS dataset_name,
                max(COALESCE(tr.split_name, '')) AS split_name,
                max(tr.task_name) AS task_name,
                tr.task_key,
                max(dm.language) AS language,
                any_value(dm.languages) AS languages,
                any_value(dm.primary_languages) AS primary_languages,
                max(dm.category) AS category,
                max(dm.short_description) AS short_description,
                max(dm.citation_count) AS citation_count,
                max(dm.reference_count) AS reference_count,
                bool_or(COALESCE(dm.has_bibtex, false)) AS has_bibtex,
                max(dm.query_count) AS query_count,
                max(dm.document_count) AS document_count,
                max(dm.query_mean_chars) AS query_mean_chars,
                max(dm.document_mean_chars) AS document_mean_chars
            FROM task_results AS tr
            LEFT JOIN dataset_metadata AS dm
              ON dm.benchmark = tr.benchmark
             AND dm.dataset_id = tr.dataset_id
             AND dm.task_key = tr.task_key
            GROUP BY
                tr.benchmark,
                tr.dataset_id,
                tr.task_key
        )
        SELECT
            row_number() OVER (
                ORDER BY benchmark, dataset_id, task_key
            ) AS task_id,
            *
        FROM task_values
        ORDER BY task_id
        """
    )
    con.execute(
        """
        CREATE TABLE dim_variant AS
        WITH variant_values AS (
            SELECT
                embedding_variant_name,
                embedding_dim,
                quantization,
                embedding_variant_name IS NULL AS is_base
            FROM task_results
            GROUP BY
                embedding_variant_name,
                embedding_dim,
                quantization
        )
        SELECT
            row_number() OVER (
                ORDER BY
                    embedding_variant_name IS NOT NULL,
                    COALESCE(embedding_variant_name, 'base'),
                    COALESCE(embedding_dim, -1),
                    COALESCE(quantization, '')
            ) AS variant_id,
            concat(
                COALESCE(embedding_variant_name, 'base'),
                ':',
                COALESCE(CAST(embedding_dim AS VARCHAR), 'unknown'),
                ':',
                COALESCE(quantization, 'none')
            ) AS variant_key,
            embedding_variant_name,
            embedding_dim,
            quantization,
            is_base
        FROM variant_values
        ORDER BY variant_id
        """
    )


def _create_metric_dimension_and_fact_tables(con: duckdb.DuckDBPyConnection) -> None:
    con.execute(
        """
        CREATE TABLE dim_metric AS
        WITH metric_values AS (
            SELECT DISTINCT
                metric_name,
                nullif(lower(regexp_extract(metric_name, '([A-Za-z]+)@[0-9]+$', 1)), '') AS metric_family,
                try_cast(regexp_extract(metric_name, '@([0-9]+)$', 1) AS INTEGER) AS cutoff
            FROM metrics_long
        )
        SELECT
            row_number() OVER (ORDER BY metric_name) AS metric_id,
            metric_name,
            metric_family,
            cutoff
        FROM metric_values
        ORDER BY metric_id
        """
    )
    con.execute(
        """
        CREATE TABLE fact_metric_score AS
        SELECT
            dm.metric_id,
            ml.model_dir,
            ml.model_name,
            ml.benchmark,
            ml.dataset_id,
            ml.task_name,
            ml.metric_value,
            ml.result_path,
            ml.score_target,
            ml.embedding_variant_name
        FROM metrics_long AS ml
        JOIN dim_metric AS dm
          ON dm.metric_name = ml.metric_name
        ORDER BY
            ml.benchmark,
            ml.dataset_id,
            ml.task_name,
            ml.model_name,
            ml.score_target,
            ml.embedding_variant_name,
            dm.metric_id
        """
    )


def _create_fact_task_score_table(con: duckdb.DuckDBPyConnection) -> None:
    con.execute(
        """
        CREATE TABLE fact_task_score AS
        SELECT *
        FROM (
        SELECT
            tr.model_dir,
            tr.model_name,
            tr.model_revision,
            tr.model_revision_requested,
            tr.benchmark,
            tr.dataset_id,
            tr.dataset_revision,
            tr.dataset_revision_requested,
            tr.dataset_name,
            tr.split_name,
            tr.task_name,
            tr.task_key,
            'all' AS score_target,
            tr.score,
            tr.score_100,
            tr.aggregate_metric,
            tr.result_path,
            tr.experiment_fingerprint,
            tr.active_parameters,
            tr.total_parameters,
            tr.max_seq_length,
            tr.dtype,
            tr.embedding_variant_name,
            tr.embedding_dim,
            tr.quantization,
            tr.attn_implementation,
            tr.query_prompt,
            tr.document_prompt,
            tr.query_prompt_name,
            tr.document_prompt_name,
            tr.query_encode_task,
            tr.document_encode_task,
            tr.trust_remote_code,
            tr.late_interaction_query_length,
            tr.late_interaction_document_length,
            tr.late_interaction_query_prefix,
            tr.late_interaction_document_prefix,
            tr.late_interaction_query_expansion,
            tr.late_interaction_attend_to_expansion_tokens,
            NULL::VARCHAR AS candidate_source,
            NULL::VARCHAR AS candidate_ranking,
            NULL::INTEGER AS rerank_top_k,
            NULL::VARCHAR AS rerank_status,
            tr.started_at_utc,
            tr.finished_at_utc,
            tr.evaluated_at_utc
        FROM task_results AS tr
        WHERE tr.score IS NOT NULL

        UNION ALL

        SELECT
            tr.model_dir,
            tr.model_name,
            tr.model_revision,
            tr.model_revision_requested,
            tr.benchmark,
            tr.dataset_id,
            tr.dataset_revision,
            tr.dataset_revision_requested,
            tr.dataset_name,
            tr.split_name,
            tr.task_name,
            tr.task_key,
            'reranking' AS score_target,
            td.rerank_score AS score,
            td.rerank_score * 100.0 AS score_100,
            tr.aggregate_metric,
            tr.result_path,
            tr.experiment_fingerprint,
            tr.active_parameters,
            tr.total_parameters,
            tr.max_seq_length,
            tr.dtype,
            tr.embedding_variant_name,
            tr.embedding_dim,
            tr.quantization,
            tr.attn_implementation,
            tr.query_prompt,
            tr.document_prompt,
            tr.query_prompt_name,
            tr.document_prompt_name,
            tr.query_encode_task,
            tr.document_encode_task,
            tr.trust_remote_code,
            tr.late_interaction_query_length,
            tr.late_interaction_document_length,
            tr.late_interaction_query_prefix,
            tr.late_interaction_document_prefix,
            tr.late_interaction_query_expansion,
            tr.late_interaction_attend_to_expansion_tokens,
            td.candidate_source,
            td.candidate_ranking,
            td.rerank_top_k,
            td.rerank_status,
            tr.started_at_utc,
            tr.finished_at_utc,
            tr.evaluated_at_utc
        FROM task_results AS tr
        JOIN task_diagnostics AS td
          ON td.model_dir = tr.model_dir
         AND td.model_name = tr.model_name
         AND td.benchmark = tr.benchmark
         AND td.task_key = tr.task_key
         AND td.result_path = tr.result_path
        WHERE tr.embedding_variant_name IS NULL
          AND td.rerank_score IS NOT NULL
          AND (td.rerank_status IS NULL OR td.rerank_status = 'available')
          AND (td.candidate_ranking IS NULL OR td.candidate_ranking = 'reranking_hybrid')

        UNION ALL

        SELECT
            tr.model_dir,
            tr.model_name,
            tr.model_revision,
            tr.model_revision_requested,
            tr.benchmark,
            tr.dataset_id,
            tr.dataset_revision,
            tr.dataset_revision_requested,
            tr.dataset_name,
            tr.split_name,
            tr.task_name,
            tr.task_key,
            'reranking' AS score_target,
            ml.metric_value AS score,
            ml.metric_value * 100.0 AS score_100,
            tr.aggregate_metric,
            tr.result_path,
            tr.experiment_fingerprint,
            tr.active_parameters,
            tr.total_parameters,
            tr.max_seq_length,
            tr.dtype,
            tr.embedding_variant_name,
            tr.embedding_dim,
            tr.quantization,
            tr.attn_implementation,
            tr.query_prompt,
            tr.document_prompt,
            tr.query_prompt_name,
            tr.document_prompt_name,
            tr.query_encode_task,
            tr.document_encode_task,
            tr.trust_remote_code,
            tr.late_interaction_query_length,
            tr.late_interaction_document_length,
            tr.late_interaction_query_prefix,
            tr.late_interaction_document_prefix,
            tr.late_interaction_query_expansion,
            tr.late_interaction_attend_to_expansion_tokens,
            'dataset_candidate_subset' AS candidate_source,
            'reranking_hybrid' AS candidate_ranking,
            try_cast(regexp_extract(ml.metric_name, '_top([0-9]+)_rerank_', 1) AS INTEGER) AS rerank_top_k,
            'available' AS rerank_status,
            tr.started_at_utc,
            tr.finished_at_utc,
            tr.evaluated_at_utc
        FROM task_results AS tr
        JOIN metrics_long AS ml
          ON ml.model_dir = tr.model_dir
         AND ml.model_name = tr.model_name
         AND ml.benchmark = tr.benchmark
         AND ml.dataset_id = tr.dataset_id
         AND ml.task_name = tr.task_name
         AND ml.result_path = tr.result_path
         AND ml.embedding_variant_name IS NOT DISTINCT FROM tr.embedding_variant_name
        JOIN dim_metric AS dm
          ON dm.metric_name = ml.metric_name
        WHERE tr.embedding_variant_name IS NOT NULL
          AND ml.score_target = 'reranking'
          AND dm.metric_family = nullif(lower(regexp_extract(COALESCE(tr.aggregate_metric, 'ndcg@10'), '([A-Za-z]+)@[0-9]+$', 1)), '')
          AND dm.cutoff = try_cast(regexp_extract(COALESCE(tr.aggregate_metric, 'ndcg@10'), '@([0-9]+)$', 1) AS INTEGER)

        UNION ALL

        SELECT
            tr.model_dir,
            tr.model_name,
            tr.model_revision,
            tr.model_revision_requested,
            tr.benchmark,
            tr.dataset_id,
            tr.dataset_revision,
            tr.dataset_revision_requested,
            tr.dataset_name,
            tr.split_name,
            tr.task_name,
            tr.task_key,
            'reranking_without_safeguard' AS score_target,
            ml.metric_value AS score,
            ml.metric_value * 100.0 AS score_100,
            tr.aggregate_metric,
            tr.result_path,
            tr.experiment_fingerprint,
            tr.active_parameters,
            tr.total_parameters,
            tr.max_seq_length,
            tr.dtype,
            tr.embedding_variant_name,
            tr.embedding_dim,
            tr.quantization,
            tr.attn_implementation,
            tr.query_prompt,
            tr.document_prompt,
            tr.query_prompt_name,
            tr.document_prompt_name,
            tr.query_encode_task,
            tr.document_encode_task,
            tr.trust_remote_code,
            tr.late_interaction_query_length,
            tr.late_interaction_document_length,
            tr.late_interaction_query_prefix,
            tr.late_interaction_document_prefix,
            tr.late_interaction_query_expansion,
            tr.late_interaction_attend_to_expansion_tokens,
            'dataset_candidate_subset' AS candidate_source,
            'reranking_hybrid' AS candidate_ranking,
            100 AS rerank_top_k,
            'available' AS rerank_status,
            tr.started_at_utc,
            tr.finished_at_utc,
            tr.evaluated_at_utc
        FROM task_results AS tr
        JOIN metrics_long AS ml
          ON ml.model_dir = tr.model_dir
         AND ml.model_name = tr.model_name
         AND ml.benchmark = tr.benchmark
         AND ml.dataset_id = tr.dataset_id
         AND ml.task_name = tr.task_name
         AND ml.result_path = tr.result_path
         AND ml.embedding_variant_name IS NOT DISTINCT FROM tr.embedding_variant_name
        JOIN dim_metric AS dm
          ON dm.metric_name = ml.metric_name
        WHERE ml.score_target = 'reranking_without_safeguard'
          AND dm.metric_family = nullif(lower(regexp_extract(COALESCE(tr.aggregate_metric, 'ndcg@10'), '([A-Za-z]+)@[0-9]+$', 1)), '')
          AND dm.cutoff = try_cast(regexp_extract(COALESCE(tr.aggregate_metric, 'ndcg@10'), '@([0-9]+)$', 1) AS INTEGER)
        ) AS scores
        ORDER BY
            benchmark,
            score_target,
            dataset_id,
            task_name,
            model_name,
            embedding_variant_name IS NOT NULL,
            embedding_variant_name
        """
    )


def _create_viewer_task_results_table(con: duckdb.DuckDBPyConnection) -> None:
    con.execute(
        """
        CREATE TABLE viewer_task_results AS
        SELECT
            fts.model_name,
            fts.benchmark,
            fts.dataset_id,
            fts.dataset_name,
            COALESCE(fts.split_name, '') AS split_name,
            fts.task_name,
            fts.task_key,
            fts.score_target,
            fts.score,
            dm.language,
            dm.languages,
            dm.primary_languages,
            fts.active_parameters,
            fts.total_parameters,
            fts.max_seq_length,
            fts.dtype,
            fts.attn_implementation,
            fts.query_prompt,
            fts.document_prompt,
            fts.query_prompt_name,
            fts.document_prompt_name,
            fts.query_encode_task,
            fts.document_encode_task,
            fts.trust_remote_code,
            fts.late_interaction_query_length,
            fts.late_interaction_document_length,
            fts.late_interaction_query_prefix,
            fts.late_interaction_document_prefix,
            fts.late_interaction_query_expansion,
            fts.late_interaction_attend_to_expansion_tokens,
            fts.embedding_variant_name,
            fts.embedding_dim,
            fts.quantization,
            dm.query_mean_chars,
            dm.document_mean_chars
        FROM fact_task_score AS fts
        LEFT JOIN dataset_metadata AS dm
          ON dm.benchmark = fts.benchmark
         AND dm.dataset_id = fts.dataset_id
         AND dm.task_key = fts.task_key
        ORDER BY
            fts.benchmark,
            fts.score_target,
            fts.dataset_id,
            fts.task_name,
            fts.model_name,
            fts.embedding_variant_name IS NOT NULL,
            fts.embedding_variant_name
        """
    )


def _create_viewer_filter_values_table(con: duckdb.DuckDBPyConnection) -> None:
    con.execute(
        """
        CREATE TABLE viewer_filter_values AS
        SELECT *
        FROM (
            SELECT
                'target' AS filter_name,
                score_target AS value,
                CASE score_target
                    WHEN 'all' THEN 'All'
                    WHEN 'reranking' THEN 'Reranking'
                    WHEN 'reranking_without_safeguard' THEN 'Reranking without safeguard'
                    ELSE score_target
                END AS label,
                count(*) AS row_count,
                CASE score_target
                    WHEN 'all' THEN '0:all'
                    WHEN 'reranking' THEN '1:reranking'
                    WHEN 'reranking_without_safeguard' THEN '2:reranking_without_safeguard'
                    ELSE concat('9:', score_target)
                END AS sort_key
            FROM viewer_task_results
            GROUP BY score_target

            UNION ALL

            SELECT
                'benchmark' AS filter_name,
                benchmark AS value,
                benchmark AS label,
                count(*) AS row_count,
                benchmark AS sort_key
            FROM viewer_task_results
            GROUP BY benchmark

            UNION ALL

            SELECT
                'model' AS filter_name,
                model_name AS value,
                model_name AS label,
                count(*) AS row_count,
                model_name AS sort_key
            FROM viewer_task_results
            GROUP BY model_name

            UNION ALL

            SELECT
                'variant' AS filter_name,
                COALESCE(embedding_variant_name, 'base') AS value,
                CASE
                    WHEN embedding_variant_name IS NULL THEN 'Base'
                    ELSE embedding_variant_name
                END AS label,
                count(*) AS row_count,
                CASE
                    WHEN embedding_variant_name IS NULL THEN '0:base'
                    ELSE concat('1:', embedding_variant_name)
                END AS sort_key
            FROM viewer_task_results
            GROUP BY embedding_variant_name
        ) AS filters
        WHERE value IS NOT NULL
        ORDER BY filter_name, sort_key
        """
    )


VIEWER_LEADERBOARD_ROW_COLUMNS = (
    "view_name",
    "score_target",
    "include_quantization_variants",
    "include_truncate_variants",
    "include_rescore_variants",
    "include_other_variants",
    "expected_tasks",
    "borda_rank",
    "mean_rank",
    "model_name",
    "borda_score",
    "mean_score",
    "macro_mean",
    "micro_mean",
    "task_count",
    "active_parameters",
    "total_parameters",
    "max_seq_length",
    "dtype",
    "attn_implementation",
    "prompt_summary",
    "trust_remote_code",
    "embedding_variant_name",
    "embedding_dim",
    "quantization",
    "source_model_name",
    "base_score_delta_percent",
)


VIEWER_LEADERBOARD_LANGUAGE_COLUMNS = (
    "view_name",
    "score_target",
    "include_quantization_variants",
    "include_truncate_variants",
    "include_rescore_variants",
    "include_other_variants",
    "code",
    "label",
    "task_count",
)


def _create_empty_viewer_leaderboard_rows_table(con: duckdb.DuckDBPyConnection) -> None:
    con.execute(
        """
        CREATE TABLE viewer_leaderboard_rows (
            view_name VARCHAR,
            score_target VARCHAR,
            include_quantization_variants BOOLEAN,
            include_truncate_variants BOOLEAN,
            include_rescore_variants BOOLEAN,
            include_other_variants BOOLEAN,
            expected_tasks INTEGER,
            borda_rank DOUBLE,
            mean_rank DOUBLE,
            model_name VARCHAR,
            borda_score DOUBLE,
            mean_score DOUBLE,
            macro_mean DOUBLE,
            micro_mean DOUBLE,
            task_count INTEGER,
            active_parameters BIGINT,
            total_parameters BIGINT,
            max_seq_length INTEGER,
            dtype VARCHAR,
            attn_implementation VARCHAR,
            prompt_summary VARCHAR,
            trust_remote_code BOOLEAN,
            embedding_variant_name VARCHAR,
            embedding_dim INTEGER,
            quantization VARCHAR,
            source_model_name VARCHAR,
            base_score_delta_percent DOUBLE
        )
        """
    )


def _create_empty_viewer_leaderboard_language_options_table(con: duckdb.DuckDBPyConnection) -> None:
    con.execute(
        """
        CREATE TABLE viewer_leaderboard_language_options (
            view_name VARCHAR,
            score_target VARCHAR,
            include_quantization_variants BOOLEAN,
            include_truncate_variants BOOLEAN,
            include_rescore_variants BOOLEAN,
            include_other_variants BOOLEAN,
            code VARCHAR,
            label VARCHAR,
            task_count INTEGER
        )
        """
    )


def build_viewer_leaderboard_mart(
    db_path: Path,
    *,
    viewer_config: ViewerConfig,
    view_names: Sequence[str] | None = None,
) -> None:
    mart_rows, language_rows = _viewer_leaderboard_mart_rows_from_cached_records(
        db_path,
        viewer_config=viewer_config,
        view_names=view_names,
    )
    con = duckdb.connect(str(db_path))
    try:
        con.execute("DROP TABLE IF EXISTS viewer_leaderboard_language_options")
        con.execute("DROP TABLE IF EXISTS viewer_leaderboard_rows")
        _create_empty_viewer_leaderboard_rows_table(con)
        _create_empty_viewer_leaderboard_language_options_table(con)
        _insert_duckdb_rows(con, "viewer_leaderboard_rows", VIEWER_LEADERBOARD_ROW_COLUMNS, mart_rows)
        _insert_duckdb_rows(
            con,
            "viewer_leaderboard_language_options",
            VIEWER_LEADERBOARD_LANGUAGE_COLUMNS,
            language_rows,
        )
    finally:
        con.close()


def _viewer_leaderboard_mart_rows_from_service(
    db_path: Path,
    *,
    viewer_config: ViewerConfig,
    view_names: Sequence[str] | None = None,
) -> tuple[list[tuple[Any, ...]], list[tuple[Any, ...]]]:
    display_flag_sets = list(product((False, True), repeat=4))
    service = LeaderboardService(duckdb_path=db_path, config=viewer_config, use_precomputed=False)
    mart_rows: list[tuple[Any, ...]] = []
    language_rows: list[tuple[Any, ...]] = []
    for view_name in view_names or viewer_config.view_names:
        for score_target in ("all", "reranking"):
            for quantization, truncate, rescore, other in display_flag_sets:
                result = service.get_leaderboard(
                    view_name,
                    score_target=score_target,
                    include_quantization_variants=quantization,
                    include_truncate_variants=truncate,
                    include_rescore_variants=rescore,
                    include_other_variants=other,
                )
                language_rows.extend(
                    (
                        view_name,
                        score_target,
                        quantization,
                        truncate,
                        rescore,
                        other,
                        option.code,
                        option.label,
                        option.task_count,
                    )
                    for option in result.available_languages
                )
                mart_rows.extend(
                    (
                        view_name,
                        score_target,
                        quantization,
                        truncate,
                        rescore,
                        other,
                        result.expected_tasks,
                        row.borda_rank,
                        row.mean_rank,
                        row.model_name,
                        row.borda_score,
                        row.mean_score,
                        row.macro_mean,
                        row.micro_mean,
                        row.task_count,
                        row.active_parameters,
                        row.total_parameters,
                        row.max_seq_length,
                        row.dtype,
                        row.attn_implementation,
                        row.prompt_summary,
                        row.trust_remote_code,
                        row.embedding_variant_name,
                        row.embedding_dim,
                        row.quantization,
                        row.source_model_name,
                        row.base_score_delta_percent,
                    )
                    for row in result.rows
                )
    return mart_rows, language_rows


def _viewer_leaderboard_mart_rows_from_cached_records(
    db_path: Path,
    *,
    viewer_config: ViewerConfig,
    view_names: Sequence[str] | None = None,
) -> tuple[list[tuple[Any, ...]], list[tuple[Any, ...]]]:
    display_flag_sets = list(product((False, True), repeat=4))
    service = LeaderboardService(duckdb_path=db_path, config=viewer_config, use_precomputed=False)
    mart_rows: list[tuple[Any, ...]] = []
    language_rows: list[tuple[Any, ...]] = []
    all_variant_flags = VariantDisplayFlags(quantization=True, truncate=True, rescore=True, other=True)
    for view_name in view_names or viewer_config.view_names:
        benchmarks = viewer_config.benchmarks_for_view(view_name)
        overall = viewer_config.overall_for_view(view_name)
        is_overall = overall is not None
        selected_score_group = (
            None
            if is_overall
            else _select_score_group(_score_groups_for_view(viewer_config, view_name), None)
        )
        language_filter_mode = _language_filter_mode_for_view(viewer_config, view_name)
        language_page_languages = _language_page_languages_for_view(viewer_config, view_name)
        for score_target in ("all", "reranking"):
            records = service.task_results_repository.fetch_task_result_rows(
                benchmarks=benchmarks,
                score_target=score_target,
                score_metric="ndcg@10",
                include_embedding_variants=True,
                variant_display_flags=all_variant_flags,
            )
            bm25_task_scores = []
            if score_target == "reranking":
                bm25_records = service.task_results_repository.fetch_task_result_rows(
                    benchmarks=benchmarks,
                    score_target="all",
                    score_metric="ndcg@10",
                    include_embedding_variants=False,
                    variant_display_flags=VariantDisplayFlags(),
                )
                bm25_task_scores = _task_scores_from_records(
                    bm25_records,
                    include_any_variants=False,
                    variant_flags=VariantDisplayFlags(),
                )
            for quantization, truncate, rescore, other in display_flag_sets:
                variant_flags = VariantDisplayFlags(
                    quantization=quantization,
                    truncate=truncate,
                    rescore=rescore,
                    other=other,
                )
                include_any_variants = variant_flags.any_enabled
                rows = _task_scores_from_records(
                    records,
                    include_any_variants=include_any_variants,
                    variant_flags=variant_flags,
                )
                if score_target == "all":
                    rows = _exclude_reranker_task_scores(rows)
                elif score_target == "reranking":
                    rows = _append_missing_bm25_task_scores(rows, bm25_task_scores)
                rows = _exclude_configured_tasks(rows, viewer_config)
                available_languages = _language_options(
                    rows,
                    mode=language_filter_mode,
                    allowed_languages=language_page_languages,
                )
                metric_score_group = None
                if overall is not None:
                    rows = _aggregate_overall_scores(rows, overall)
                    metric_score_group = _overall_metric_score_group(overall)
                elif selected_score_group is not None:
                    rows = _aggregate_benchmark_score_group_scores(rows, selected_score_group)
                    metric_score_group = selected_score_group
                leaderboard_rows = compute_leaderboard_rows(
                    rows,
                    is_overall=is_overall,
                    score_group=metric_score_group,
                    metric_columns=[],
                )
                sorted_rows = sort_rows(leaderboard_rows, sort="borda_rank", direction="asc")
                expected_tasks = len({row.task_key for row in rows})
                language_rows.extend(
                    (
                        view_name,
                        score_target,
                        quantization,
                        truncate,
                        rescore,
                        other,
                        option.code,
                        option.label,
                        option.task_count,
                    )
                    for option in available_languages
                )
                mart_rows.extend(
                    (
                        view_name,
                        score_target,
                        quantization,
                        truncate,
                        rescore,
                        other,
                        expected_tasks,
                        row.borda_rank,
                        row.mean_rank,
                        row.model_name,
                        row.borda_score,
                        row.mean_score,
                        row.macro_mean,
                        row.micro_mean,
                        row.task_count,
                        row.active_parameters,
                        row.total_parameters,
                        row.max_seq_length,
                        row.dtype,
                        row.attn_implementation,
                        row.prompt_summary,
                        row.trust_remote_code,
                        row.embedding_variant_name,
                        row.embedding_dim,
                        row.quantization,
                        row.source_model_name,
                        row.base_score_delta_percent,
                    )
                    for row in sorted_rows
                )
    return mart_rows, language_rows


def export_duckdb_tables_to_parquet(db_path: Path, output_dir: Path) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)
    con = duckdb.connect(str(db_path), read_only=True)
    try:
        for table in WAREHOUSE_TABLES:
            output_path = output_dir / f"{table}.parquet"
            if output_path.exists():
                output_path.unlink()
            con.execute(f"COPY (SELECT * FROM {table}) TO ? (FORMAT PARQUET)", [str(output_path)])
    finally:
        con.close()


def write_html(
    html_output: Path,
    *,
    duckdb_path: Path,
    rows: list[TaskResult],
    runs: list[dict[str, Any]],
    standings: dict[str, list[dict[str, Any]]],
    target_benchmarks: Sequence[str] | None = None,
) -> None:
    html_output.parent.mkdir(parents=True, exist_ok=True)
    generated_at = datetime.now(timezone.utc).isoformat()
    target_benchmarks = target_benchmarks or TARGET_BENCHMARKS
    data = {
        "generatedAt": generated_at,
        "duckdbPath": str(duckdb_path),
        "views": standings,
        "summary": {
            "taskResults": len(rows),
            "runs": len(runs),
            "completeModels": len(standings.get("Overall", [])),
            "benchmarks": [
                {"name": name, "tasks": len({row.task_key for row in rows if row.benchmark == name})}
                for name in target_benchmarks
            ],
            "skipped": [],
        },
    }
    data_json = json.dumps(data, ensure_ascii=False)
    html_output.write_text(render_html(data_json=data_json), encoding="utf-8")


def render_html(*, data_json: str) -> str:
    return f"""<!doctype html>
<html lang="ja">
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <title>HAKARI-Bench Borda Report</title>
  <script src="https://cdn.jsdelivr.net/npm/@tailwindcss/browser@4"></script>
  <link rel="icon" href="/favicon.svg" type="image/svg+xml" />
</head>
<body class="bg-stone-50 text-stone-900 dark:bg-stone-950 dark:text-stone-100">
  <main class="mx-auto max-w-[1600px] px-5 py-8">
    <header class="mb-7 border-b border-stone-200 pb-5 dark:border-stone-800">
      <p class="text-sm font-medium text-sky-700 dark:text-sky-300">HAKARI-Bench report</p>
      <h1 class="mt-2 text-2xl font-semibold tracking-normal text-stone-950 dark:text-stone-50">Nano benchmark sortable Borda score matrix</h1>
      <p class="mt-3 max-w-5xl text-sm leading-6 text-stone-700 dark:text-stone-300">Completed benchmark results are loaded into DuckDB and summarized by Overall and each Nano benchmark group. Tables are sorted by Borda Score by default. Click any column heading to sort.</p>
    </header>

    <section class="mb-5 grid gap-3 sm:grid-cols-2 lg:grid-cols-4">
      <div class="border border-stone-200 bg-white p-4 dark:border-stone-800 dark:bg-stone-900">
        <div class="text-xs uppercase tracking-wide text-stone-500 dark:text-stone-400">Complete models</div>
        <div id="complete-models" class="mt-1 text-2xl font-semibold tabular-nums"></div>
      </div>
      <div class="border border-stone-200 bg-white p-4 dark:border-stone-800 dark:bg-stone-900">
        <div class="text-xs uppercase tracking-wide text-stone-500 dark:text-stone-400">Task results</div>
        <div id="task-results" class="mt-1 text-2xl font-semibold tabular-nums"></div>
      </div>
      <div class="border border-stone-200 bg-white p-4 dark:border-stone-800 dark:bg-stone-900">
        <div class="text-xs uppercase tracking-wide text-stone-500 dark:text-stone-400">DuckDB</div>
        <div id="duckdb-path" class="mt-1 text-sm font-medium tabular-nums"></div>
      </div>
      <div class="border border-stone-200 bg-white p-4 dark:border-stone-800 dark:bg-stone-900">
        <div class="text-xs uppercase tracking-wide text-stone-500 dark:text-stone-400">Generated UTC</div>
        <div id="generated-at" class="mt-1 text-sm font-medium tabular-nums"></div>
      </div>
    </section>

    <section class="mb-5">
      <div id="benchmark-chips" class="flex flex-wrap gap-2"></div>
    </section>

    <section class="mb-5">
      <div id="view-buttons" class="flex flex-wrap gap-2"></div>
    </section>

    <section class="mb-8">
      <div class="mb-3 flex flex-wrap items-end justify-between gap-3">
        <div>
          <h2 id="view-title" class="text-lg font-semibold text-stone-950 dark:text-stone-50"></h2>
          <p id="view-summary" class="mt-1 text-sm text-stone-600 dark:text-stone-400"></p>
        </div>
      </div>
      <div class="overflow-x-auto border border-stone-200 bg-white dark:border-stone-800 dark:bg-stone-950">
        <table id="ranked-table" class="min-w-full border-collapse">
          <thead id="table-head"></thead>
          <tbody id="table-body"></tbody>
        </table>
      </div>
    </section>

    <section class="border border-stone-200 bg-white p-4 text-sm leading-6 text-stone-700 dark:border-stone-800 dark:bg-stone-900 dark:text-stone-300">
      <h2 class="mb-2 text-base font-semibold text-stone-950 dark:text-stone-50">Definitions</h2>
      <p>Mean nDCG@10 is the average task score multiplied by 100. Borda Score is computed per task from score rank: <span class="font-mono text-stone-900 dark:text-stone-100">100 * (N - rank) / (N - 1)</span>, then averaged within the selected view. Only models with all tasks in the selected view are included in the ranking.</p>
      <div id="skipped" class="mt-3"></div>
    </section>
  </main>
  <script>
    const REPORT_DATA = {data_json};
    const columns = [
      {{ key: 'borda_rank', label: 'Borda Rank', type: 'number', direction: 'asc' }},
      {{ key: 'score_rank', label: 'Score Rank', type: 'number', direction: 'asc' }},
      {{ key: 'model', label: 'Model', type: 'text', direction: 'asc' }},
      {{ key: 'borda_score', label: 'Borda Score', type: 'number', direction: 'desc' }},
      {{ key: 'mean_score', label: 'Mean nDCG@10', type: 'number', direction: 'desc' }},
      {{ key: 'task_count', label: 'Tasks', type: 'number', direction: 'desc' }},
      {{ key: 'active_parameters', label: 'Active Params', type: 'number', direction: 'asc' }},
      {{ key: 'total_parameters', label: 'Total Params', type: 'number', direction: 'asc' }},
      {{ key: 'max_seq_length', label: 'Max Len', type: 'number', direction: 'desc' }},
      {{ key: 'attn_implementation', label: 'Attn', type: 'text', direction: 'asc' }},
      {{ key: 'torch_version', label: 'Torch', type: 'text', direction: 'asc' }},
      {{ key: 'transformers_version', label: 'Transformers', type: 'text', direction: 'asc' }}
    ];
    let currentView = 'Overall';
    let sortState = {{ key: 'borda_score', direction: 'desc' }};

    function fmtNumber(value, digits = 2) {{
      if (value === null || value === undefined || Number.isNaN(Number(value))) return '';
      return Number(value).toFixed(digits);
    }}

    function fmtRank(value) {{
      if (value === null || value === undefined) return '';
      return Number.isInteger(Number(value)) ? String(Number(value)) : Number(value).toFixed(1);
    }}

    function fmtParams(value) {{
      if (!value) return '';
      const n = Number(value);
      if (n >= 1_000_000_000) return (n / 1_000_000_000).toFixed(2) + 'B';
      if (n >= 1_000_000) return (n / 1_000_000).toFixed(1) + 'M';
      return n.toLocaleString();
    }}

    function cellValue(row, key) {{
      const value = row[key];
      if (value === null || value === undefined) return '';
      return value;
    }}

    function compareRows(a, b, column) {{
      const av = cellValue(a, column.key);
      const bv = cellValue(b, column.key);
      const aMissing = av === '';
      const bMissing = bv === '';
      if (aMissing && bMissing) return 0;
      if (aMissing) return 1;
      if (bMissing) return -1;
      let result;
      if (column.type === 'number') result = Number(av) - Number(bv);
      else result = String(av).toLocaleLowerCase().localeCompare(String(bv).toLocaleLowerCase(), 'ja');
      return sortState.direction === 'asc' ? result : -result;
    }}

    function renderSummary() {{
      document.getElementById('complete-models').textContent = REPORT_DATA.summary.completeModels;
      document.getElementById('task-results').textContent = REPORT_DATA.summary.taskResults.toLocaleString();
      document.getElementById('duckdb-path').textContent = REPORT_DATA.duckdbPath;
      document.getElementById('generated-at').textContent = REPORT_DATA.generatedAt;
      const chips = document.getElementById('benchmark-chips');
      chips.innerHTML = '';
      REPORT_DATA.summary.benchmarks.forEach((item) => {{
        const chip = document.createElement('span');
        chip.className = 'inline-flex items-center gap-1 border border-stone-300 bg-white px-2 py-1 text-xs text-stone-700 dark:border-stone-700 dark:bg-stone-900 dark:text-stone-300';
        chip.innerHTML = `<span>${{escapeHtml(item.name)}}</span><span class="font-mono text-stone-500 dark:text-stone-400">${{item.tasks}}</span>`;
        chips.appendChild(chip);
      }});
      const skipped = document.getElementById('skipped');
      skipped.innerHTML = REPORT_DATA.summary.skipped.length
        ? '<h3 class="mb-1 font-semibold text-stone-950 dark:text-stone-50">Skipped FA2 models</h3>' +
          REPORT_DATA.summary.skipped.map((item) => `<p><span class="font-medium">${{escapeHtml(item.model)}}</span>: ${{escapeHtml(item.reason)}}</p>`).join('')
        : '';
    }}

    function renderButtons() {{
      const container = document.getElementById('view-buttons');
      container.innerHTML = '';
      Object.keys(REPORT_DATA.views).forEach((view) => {{
        const button = document.createElement('button');
        button.type = 'button';
        button.className = view === currentView
          ? 'border border-sky-700 bg-sky-100 px-3 py-1.5 text-sm font-medium text-sky-900 dark:border-sky-300 dark:bg-sky-950 dark:text-sky-100'
          : 'border border-stone-300 bg-white px-3 py-1.5 text-sm text-stone-700 hover:border-sky-500 hover:text-sky-700 dark:border-stone-700 dark:bg-stone-900 dark:text-stone-300 dark:hover:border-sky-400 dark:hover:text-sky-300';
        button.textContent = view;
        button.addEventListener('click', () => {{
          currentView = view;
          sortState = {{ key: 'borda_score', direction: 'desc' }};
          render();
        }});
        container.appendChild(button);
      }});
    }}

    function renderTable() {{
      const head = document.getElementById('table-head');
      const body = document.getElementById('table-body');
      head.innerHTML = '';
      body.innerHTML = '';
      const tr = document.createElement('tr');
      columns.forEach((column) => {{
        const th = document.createElement('th');
        th.scope = 'col';
        const align = column.type === 'number' ? 'text-right' : 'text-left';
        th.className = `sticky top-0 z-10 bg-stone-100 px-3 py-2 text-xs font-semibold uppercase tracking-wide text-stone-600 dark:bg-stone-900 dark:text-stone-300 ${{align}}`;
        const button = document.createElement('button');
        button.type = 'button';
        button.className = `inline-flex w-full items-center gap-1 hover:text-sky-700 dark:hover:text-sky-300 ${{column.type === 'number' ? 'justify-end' : 'justify-start'}}`;
        button.textContent = column.label;
        const indicator = document.createElement('span');
        indicator.className = 'text-stone-400';
        indicator.textContent = sortState.key === column.key ? (sortState.direction === 'asc' ? '▲' : '▼') : '';
        button.appendChild(indicator);
        button.addEventListener('click', () => {{
          if (sortState.key === column.key) {{
            sortState.direction = sortState.direction === 'asc' ? 'desc' : 'asc';
          }} else {{
            sortState = {{ key: column.key, direction: column.direction }};
          }}
          renderTable();
        }});
        th.appendChild(button);
        tr.appendChild(th);
      }});
      head.appendChild(tr);

      const sortColumn = columns.find((column) => column.key === sortState.key) || columns[3];
      const rows = [...REPORT_DATA.views[currentView]].sort((a, b) => compareRows(a, b, sortColumn));
      rows.forEach((row) => {{
        const tr = document.createElement('tr');
        tr.className = 'border-b border-stone-200 odd:bg-white even:bg-stone-50 dark:border-stone-800 dark:odd:bg-stone-950 dark:even:bg-stone-900';
        columns.forEach((column) => {{
          const td = document.createElement('td');
          const align = column.type === 'number' ? 'text-right tabular-nums' : 'text-left';
          td.className = `whitespace-nowrap px-3 py-2 text-sm text-stone-700 dark:text-stone-300 ${{align}}`;
          if (column.key === 'model') td.className += ' font-medium text-stone-900 dark:text-stone-100';
          const value = row[column.key];
          if (column.key.endsWith('_rank')) td.textContent = fmtRank(value);
          else if (column.key === 'borda_score' || column.key === 'mean_score') td.textContent = fmtNumber(value);
          else if (column.key === 'active_parameters' || column.key === 'total_parameters') td.textContent = fmtParams(value);
          else if (column.type === 'number') td.textContent = value ?? '';
          else td.textContent = value ?? '';
          tr.appendChild(td);
        }});
        body.appendChild(tr);
      }});
    }}

    function render() {{
      renderButtons();
      const rows = REPORT_DATA.views[currentView];
      document.getElementById('view-title').textContent = currentView + ' ranked models';
      document.getElementById('view-summary').textContent = `${{rows.length}} complete models, default sorted by Borda Score`;
      renderTable();
    }}

    function escapeHtml(value) {{
      return String(value).replace(/[&<>"']/g, (char) => ({{'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}}[char]));
    }}

    renderSummary();
    render();
  </script>
</body>
</html>
"""


def mean(values: Any) -> float:
    vals = list(values)
    return sum(vals) / len(vals) if vals else 0.0


def _late_interaction_metadata(model: dict[str, Any], evaluation: dict[str, Any]) -> dict[str, Any]:
    model_section = model.get("late_interaction")
    evaluation_section = evaluation.get("late_interaction")
    merged: dict[str, Any] = {}
    if isinstance(model_section, dict):
        merged.update(model_section)
    if isinstance(evaluation_section, dict):
        # Per-run evaluation options describe the actual run and should override
        # model defaults when both are present.
        merged.update({key: value for key, value in evaluation_section.items() if value is not None})
    return merged


def _int_or_none(value: Any) -> int | None:
    if not isinstance(value, int | float):
        return None
    if isinstance(value, float) and not math.isfinite(value):
        return None
    return int(value)


def _float_or_none(value: Any) -> float | None:
    return float(value) if isinstance(value, int | float) else None


def _bool_or_none(value: Any) -> bool | None:
    return value if isinstance(value, bool) else None


def _str_or_none(value: Any) -> str | None:
    return str(value) if value is not None else None


def _dataset_revision_value(value: Any, *, key: str) -> str | None:
    if isinstance(value, dict):
        item = value.get(key)
        return str(item) if item is not None else None
    if key == "resolved" and value is not None:
        return str(value)
    return None


def _model_revision_value(value: Any, *, key: str) -> str | None:
    if not isinstance(value, dict):
        return None
    item = value.get(key)
    return str(item) if item is not None else None


if __name__ == "__main__":
    main()
