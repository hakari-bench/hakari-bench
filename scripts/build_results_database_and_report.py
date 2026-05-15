from __future__ import annotations

import argparse
import json
import math
from collections import defaultdict
from collections.abc import Sequence
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import duckdb

from hakari_bench.datasets import DatasetRegistry
from hakari_bench.viewer.config import BenchmarkConfig, load_viewer_config
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


def load_benchmark_configs(config_dir: Path = DEFAULT_VIEWER_CONFIG_DIR) -> list[BenchmarkConfig]:
    return load_viewer_config(config_dir).benchmarks


def target_benchmark_names(benchmark_configs: Sequence[BenchmarkConfig]) -> list[str]:
    return [benchmark.name for benchmark in benchmark_configs]


TARGET_BENCHMARKS: list[str] = target_benchmark_names(load_benchmark_configs())
VIEWS = ["Overall", *TARGET_BENCHMARKS]
WAREHOUSE_TABLES = (
    "runs",
    "task_results",
    "metrics_long",
    "retrieval_rankings",
    "task_diagnostics",
    "dataset_metadata",
    "viewer_task_results",
    "model_scores",
    "borda_task_scores",
)


TaskResult = TaskResultRow


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--results-dir", type=Path, default=Path("output/results"))
    parser.add_argument("--duckdb-path", type=Path, default=Path("output/results/hakari_bench.duckdb"))
    parser.add_argument("--html-output", type=Path, required=True)
    parser.add_argument(
        "--viewer-config-dir",
        type=Path,
        default=DEFAULT_VIEWER_CONFIG_DIR,
        help="Directory containing viewer benchmark and overall YAML configuration.",
    )
    parser.add_argument(
        "--parquet-output-dir",
        type=Path,
        default=None,
        help="Optional directory for Parquet snapshots of the canonical DuckDB tables.",
    )
    args = parser.parse_args()

    benchmark_configs = load_benchmark_configs(args.viewer_config_dir)
    target_benchmarks = target_benchmark_names(benchmark_configs)
    rows, runs, metric_rows, diagnostic_rows, dataset_metadata_rows, ranking_rows = load_results(
        args.results_dir,
        benchmark_configs=benchmark_configs,
    )
    base_rows = [row for row in rows if row.embedding_variant_name is None]
    standings, borda_rows = compute_standings(base_rows, target_benchmarks=target_benchmarks)
    write_duckdb(
        args.duckdb_path,
        runs=runs,
        rows=rows,
        metric_rows=metric_rows,
        diagnostic_rows=diagnostic_rows,
        dataset_metadata_rows=dataset_metadata_rows,
        ranking_rows=ranking_rows,
        standings=standings,
        borda_rows=borda_rows,
    )
    if args.parquet_output_dir is not None:
        export_duckdb_tables_to_parquet(args.duckdb_path, args.parquet_output_dir)
    write_html(
        args.html_output,
        duckdb_path=args.duckdb_path,
        rows=base_rows,
        runs=runs,
        standings=standings,
        target_benchmarks=target_benchmarks,
    )


def load_results(
    results_dir: Path,
    *,
    benchmark_configs: Sequence[BenchmarkConfig] | None = None,
) -> tuple[
    list[TaskResult],
    list[dict[str, Any]],
    list[MetricLongRow],
    list[TaskDiagnosticRow],
    list[DatasetMetadataRow],
    list[RetrievalRankingRow],
]:
    rows: list[TaskResult] = []
    run_accumulators: dict[str, dict[str, Any]] = {}
    metric_rows: list[MetricLongRow] = []
    diagnostic_rows: list[TaskDiagnosticRow] = []
    dataset_metadata_rows: list[DatasetMetadataRow] = []
    ranking_rows: list[RetrievalRankingRow] = []
    registry = DatasetRegistry.load_builtin()
    benchmark_configs = list(benchmark_configs or load_benchmark_configs())
    target_benchmarks = set(target_benchmark_names(benchmark_configs))

    for result_path in sorted(results_dir.glob("*/*/*.json")):
        task_payload = json.loads(result_path.read_text(encoding="utf-8"))
        target = task_payload.get("target", {})
        if not isinstance(target, dict):
            continue
        benchmark = benchmark_name(
            target.get("dataset_id"),
            target.get("dataset_name"),
            benchmark_configs=benchmark_configs,
        )
        if benchmark not in target_benchmarks:
            continue
        evaluation = task_payload.get("evaluation", {})
        if not isinstance(evaluation, dict):
            continue
        config = task_payload.get("config", {})
        if not isinstance(config, dict):
            config = {}
        score = evaluation.get("aggregate_metric_value")
        if not isinstance(score, int | float):
            continue
        model = task_payload.get("model", {})
        environment = task_payload.get("environment", {})
        package_versions = environment.get("package_versions", {}) if isinstance(environment, dict) else {}
        experiment_manifest = task_payload.get("experiment_manifest", {})
        experiment_manifest = experiment_manifest if isinstance(experiment_manifest, dict) else {}
        model_dir = result_path.relative_to(results_dir).parts[0]
        model_name = _model_name_from_payload(model, model_dir=model_dir)
        model_source = model.get("source", {}) if isinstance(model, dict) else {}
        model_revision = _model_revision_value(model_source, key="revision")
        model_revision_requested = _model_revision_value(model_source, key="revision_requested")
        dataset_id = str(target.get("dataset_id") or "")
        dataset_revision = _dataset_revision_value(target.get("dataset_revision"), key="resolved")
        dataset_revision_requested = _dataset_revision_value(target.get("dataset_revision"), key="requested")
        raw_task_name = str(target.get("task_name") or target.get("split_name") or "")
        task_name = canonical_task_name(benchmark, raw_task_name)
        split_name = canonical_split_name(
            benchmark,
            str(target["split_name"]) if target.get("split_name") is not None else None,
        )
        task_key = canonical_task_key(benchmark=benchmark, dataset_id=dataset_id, task_name=task_name)
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
                    )
                )
        ranking_rows.extend(_retrieval_ranking_rows(common=common, task_payload=task_payload, result_path=result_path))

    return (
        _dedupe_task_results(rows),
        _runs_from_task_results(run_accumulators),
        _dedupe_metric_rows(metric_rows),
        _dedupe_task_diagnostic_rows(diagnostic_rows),
        _dedupe_dataset_metadata_rows(dataset_metadata_rows),
        _dedupe_retrieval_ranking_rows(ranking_rows),
    )


def _model_name_from_payload(model: Any, *, model_dir: str) -> str:
    if not isinstance(model, dict):
        return model_dir
    return str(model.get("id") or model_dir)


def _retrieval_ranking_rows(
    *,
    common: dict[str, Any],
    task_payload: dict[str, Any],
    result_path: Path,
) -> list[RetrievalRankingRow]:
    artifact = _top_rankings_artifact(task_payload)
    if artifact is None:
        return []
    ranking_path = result_path.parent / artifact["path"]
    if not ranking_path.exists():
        return []
    ranking_payload = json.loads(ranking_path.read_text(encoding="utf-8"))
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
                    ranking_path=str(ranking_path),
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
    if not isinstance(path, str) or not path:
        return None
    return artifact


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
        model_dir,
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
    for model_dir in sorted(accumulators):
        item = accumulators[model_dir]
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
    deduped: dict[tuple[str, str, str, str, str, str | None, int | None, str | None], TaskResult] = {}
    for row in rows:
        key = (
            row.model_dir,
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
    return Path(row.result_path).stem == row.task_name


def _dedupe_metric_rows(rows: list[MetricLongRow]) -> list[MetricLongRow]:
    deduped: dict[tuple[Any, ...], MetricLongRow] = {}
    for row in rows:
        key = (
            row.model_dir,
            row.model_name,
            row.benchmark,
            row.dataset_id,
            row.task_name,
            row.metric_name,
        )
        current = deduped.get(key)
        if current is None or _prefer_metric_row(row, current):
            deduped[key] = row
    return list(deduped.values())


def _prefer_metric_row(candidate: MetricLongRow, current: MetricLongRow) -> bool:
    return _metric_result_path_stem_matches_task(candidate) and not _metric_result_path_stem_matches_task(current)


def _metric_result_path_stem_matches_task(row: MetricLongRow) -> bool:
    return Path(row.result_path).stem == row.task_name


def _dedupe_task_diagnostic_rows(rows: list[TaskDiagnosticRow]) -> list[TaskDiagnosticRow]:
    deduped: dict[tuple[str, str, str, str, str, str], TaskDiagnosticRow] = {}
    for row in rows:
        key = (row.model_dir, row.model_name, row.benchmark, row.dataset_id, row.task_key, row.result_path)
        current = deduped.get(key)
        if current is None or _diagnostic_result_path_stem_matches_task(row):
            deduped[key] = row
    return list(deduped.values())


def _diagnostic_result_path_stem_matches_task(row: TaskDiagnosticRow) -> bool:
    return Path(row.result_path).stem == row.task_name


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
    con = duckdb.connect(str(db_path))
    try:
        for table in WAREHOUSE_TABLES:
            con.execute(f"DROP TABLE IF EXISTS {table}")
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
        con.executemany(
            "INSERT INTO runs VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
            [
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
            ],
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
                torch_version VARCHAR, transformers_version VARCHAR,
                sentence_transformers_version VARCHAR, started_at_utc VARCHAR, finished_at_utc VARCHAR,
                evaluated_at_utc VARCHAR, duration_seconds_including_dataset_load DOUBLE, wall_seconds DOUBLE
            )
            """
        )
        con.executemany(
            "INSERT INTO task_results VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
            [row.duckdb_values() for row in rows],
        )
        con.execute(
            """
            CREATE TABLE metrics_long (
                model_dir VARCHAR, model_name VARCHAR, benchmark VARCHAR,
                dataset_id VARCHAR, task_name VARCHAR, metric_name VARCHAR, metric_value DOUBLE, result_path VARCHAR
            )
            """
        )
        con.executemany(
            "INSERT INTO metrics_long VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
            [row.duckdb_values() for row in normalized_metric_rows],
        )
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
            con.executemany(
                "INSERT INTO retrieval_rankings VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
                [row.duckdb_values() for row in normalized_ranking_rows],
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
            con.executemany(
                "INSERT INTO task_diagnostics VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
                [row.duckdb_values() for row in normalized_diagnostic_rows],
            )
        con.execute(
            """
            CREATE TABLE dataset_metadata (
                benchmark VARCHAR, dataset_id VARCHAR, dataset_name VARCHAR, split_name VARCHAR,
                task_name VARCHAR, task_key VARCHAR, language VARCHAR, languages VARCHAR[], category VARCHAR,
                short_description VARCHAR, citation_count INTEGER, reference_count INTEGER,
                has_bibtex BOOLEAN, query_count INTEGER, document_count INTEGER,
                query_mean_chars DOUBLE, document_mean_chars DOUBLE
            )
            """
        )
        if normalized_dataset_metadata_rows:
            con.executemany(
                "INSERT INTO dataset_metadata VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
                [row.duckdb_values() for row in normalized_dataset_metadata_rows],
            )
        _create_viewer_task_results_table(con)
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
        con.executemany(
            "INSERT INTO model_scores VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
            [
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
            ],
        )
        con.execute(
            """
            CREATE TABLE borda_task_scores (
                view_name VARCHAR, model_name VARCHAR, benchmark VARCHAR, task_key VARCHAR,
                rank DOUBLE, model_count INTEGER, borda_score DOUBLE, score DOUBLE
            )
            """
        )
        con.executemany(
            "INSERT INTO borda_task_scores VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
            [
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
            ],
        )
    finally:
        con.close()


def _create_viewer_task_results_table(con: duckdb.DuckDBPyConnection) -> None:
    con.execute(
        """
        CREATE TABLE viewer_task_results AS
        SELECT
            tr.model_name,
            tr.benchmark,
            tr.dataset_id,
            tr.dataset_name,
            COALESCE(tr.split_name, '') AS split_name,
            tr.task_name,
            tr.task_key,
            tr.score,
            dm.language,
            dm.languages,
            tr.active_parameters,
            tr.total_parameters,
            tr.max_seq_length,
            tr.dtype,
            tr.attn_implementation,
            tr.query_prompt,
            tr.document_prompt,
            tr.query_prompt_name,
            tr.document_prompt_name,
            tr.query_encode_task,
            tr.document_encode_task,
            tr.trust_remote_code,
            tr.embedding_variant_name,
            tr.embedding_dim,
            tr.quantization
        FROM task_results AS tr
        LEFT JOIN dataset_metadata AS dm
          ON dm.benchmark = tr.benchmark
         AND dm.dataset_id = tr.dataset_id
         AND dm.task_key = tr.task_key
        ORDER BY
            tr.benchmark,
            tr.dataset_id,
            tr.task_name,
            tr.model_name,
            tr.embedding_variant_name IS NOT NULL,
            tr.embedding_variant_name
        """
    )


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
