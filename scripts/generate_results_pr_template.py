from __future__ import annotations

import argparse
import gzip
import json
import lzma
import math
from collections import defaultdict
from collections.abc import Iterable, Sequence
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from hakari_bench.viewer.config import BenchmarkConfig, OverallBenchmarkConfig, load_viewer_config
from hakari_bench.viewer.task_names import canonical_task_key, canonical_task_name


RESULT_JSON_SUFFIXES = (".json", ".json.gz", ".json.xz")
SUMMARY_VIEW_NAME = "Overall"
PRIMARY_METRIC = "ndcg@10"
DEFAULT_COMPARISON_MODELS = (
    "Qwen/Qwen3-Embedding-0.6B",
    "jinaai/jina-embeddings-v5-text-small",
    "BAAI/bge-m3",
    "intfloat/e5-small-v2",
    "bm25",
)


@dataclass(frozen=True)
class CoreTaskScore:
    benchmark: str
    dataset_id: str
    dataset_name: str
    task_name: str
    task_key: str
    score: float


@dataclass(frozen=True)
class CoreBenchmarkSummary:
    benchmark: str
    score: float
    score_unit_count: int
    raw_task_count: int


@dataclass(frozen=True)
class CoreSummary:
    score: float | None
    score_unit_count: int
    raw_task_count: int
    benchmarks: list[CoreBenchmarkSummary]


@dataclass(frozen=True)
class ComparisonRow:
    model_name: str
    score: float
    variant_label: str
    score_unit_count: int
    raw_task_count: int
    component_scores: dict[str, float]


def build_arg_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Generate a Hugging Face dataset PR description from HAKARI result JSON files.",
    )
    parser.add_argument(
        "result_dir",
        type=Path,
        help="Model result directory, e.g. PROJECT_ROOT/hakari-results/org__model or output/results/.../org__model.",
    )
    parser.add_argument(
        "-o",
        "--output",
        type=Path,
        help="Write the generated Markdown to this path. Defaults to stdout.",
    )
    parser.add_argument(
        "--repo-path",
        help="Path where the result directory will live inside hakari-bench/results.",
    )
    parser.add_argument(
        "--config-dir",
        type=Path,
        default=Path("config/viewer"),
        help="Viewer config directory used to resolve Overall benchmark grouping.",
    )
    parser.add_argument(
        "--comparison-duckdb-path",
        type=Path,
        help=(
            "Optional result DuckDB used to add an Overall comparison table. "
            "The table is recomputed from task_results with the same grouping as this PR body."
        ),
    )
    parser.add_argument(
        "--comparison-model",
        action="append",
        dest="comparison_models",
        help=(
            "Model id to include in the DuckDB comparison table. Can be repeated. "
            "Defaults to Qwen3-Embedding-4B, jina v5 small, bge-m3, e5-small-v2, and bm25."
        ),
    )
    return parser


def result_json_paths(path: Path) -> list[Path]:
    if path.is_file():
        return [path] if is_result_json_path(path) else []
    return sorted(file for file in path.rglob("*") if file.is_file() and is_result_json_path(file))


def is_result_json_path(path: Path) -> bool:
    value = path.as_posix()
    return any(value.endswith(suffix) for suffix in RESULT_JSON_SUFFIXES)


def load_result_payload(path: Path) -> dict[str, Any]:
    if path.as_posix().endswith(".json.xz"):
        with lzma.open(path, "rt", encoding="utf-8") as file:
            return json.load(file)
    if path.as_posix().endswith(".json.gz"):
        with gzip.open(path, "rt", encoding="utf-8") as file:
            return json.load(file)
    return json.loads(path.read_text(encoding="utf-8"))


def benchmark_name(
    dataset_id: Any,
    dataset_name: Any,
    *,
    benchmark_configs: Sequence[BenchmarkConfig],
) -> str:
    value = f"{dataset_id or ''}/{dataset_name or ''}"
    best_name: str | None = None
    best_match_length = -1
    for benchmark in benchmark_configs:
        for pattern in benchmark.match_patterns:
            if pattern in value and len(pattern) > best_match_length:
                best_name = benchmark.name
                best_match_length = len(pattern)
    return best_name or "Other"


def generate_pr_template(
    result_dir: Path,
    *,
    config_dir: Path = Path("config/viewer"),
    repo_path: str | None = None,
    comparison_duckdb_path: Path | None = None,
    comparison_models: Sequence[str] | None = None,
) -> str:
    paths = result_json_paths(result_dir)
    if not paths:
        raise ValueError(f"No result JSON files found under {result_dir}")

    viewer_config = load_viewer_config(config_dir)
    summary_scope = viewer_config.overall_for_view(SUMMARY_VIEW_NAME)
    if summary_scope is None:
        raise ValueError(f"{config_dir} does not define an {SUMMARY_VIEW_NAME} overall view")

    payloads = [(path, load_result_payload(path)) for path in paths]
    first_payload = payloads[0][1]
    model_dir = result_dir.name
    repo_path = repo_path or f"PROJECT_ROOT/hakari-results/{model_dir}"
    model_name = _model_name(first_payload, model_dir=model_dir)
    core_rows = _core_task_scores(
        payloads,
        benchmark_configs=viewer_config.benchmarks,
        core_components=summary_scope.benchmark_components,
    )
    core_summary = summarize_core_scores(core_rows, core_components=summary_scope.benchmark_components)
    comparison_rows = _comparison_rows_from_duckdb(
        comparison_duckdb_path,
        model_name=model_name,
        submitted_summary=core_summary,
        comparison_models=comparison_models,
        benchmark_configs=viewer_config.benchmarks,
        core_components=summary_scope.benchmark_components,
    )

    metadata = _metadata_summary(payloads, result_dir=result_dir, repo_path=repo_path, model_dir=model_dir)
    return _render_markdown(
        model_name=model_name,
        model_dir=model_dir,
        repo_path=repo_path,
        metadata=metadata,
        core_summary=core_summary,
        comparison_rows=comparison_rows,
    )


def summarize_core_scores(
    rows: Sequence[CoreTaskScore],
    *,
    core_components: Sequence[OverallBenchmarkConfig],
) -> CoreSummary:
    rows_by_benchmark: dict[str, list[CoreTaskScore]] = defaultdict(list)
    for row in rows:
        rows_by_benchmark[row.benchmark].append(row)

    all_units: list[float] = []
    benchmark_summaries: list[CoreBenchmarkSummary] = []
    for component in core_components:
        benchmark_rows = rows_by_benchmark.get(component.name, [])
        if not benchmark_rows:
            benchmark_summaries.append(
                CoreBenchmarkSummary(
                    benchmark=component.name,
                    score=math.nan,
                    score_unit_count=0,
                    raw_task_count=0,
                )
            )
            continue
        group_by = component.group_by or "task_key"
        grouped: dict[str, list[float]] = defaultdict(list)
        for row in benchmark_rows:
            grouped[_score_group_key(row, group_by)].append(row.score)
        units = [_mean(scores) for scores in grouped.values()]
        all_units.extend(units)
        benchmark_summaries.append(
            CoreBenchmarkSummary(
                benchmark=component.name,
                score=_mean(units),
                score_unit_count=len(units),
                raw_task_count=len(benchmark_rows),
            )
        )

    return CoreSummary(
        score=_mean(all_units) if all_units else None,
        score_unit_count=len(all_units),
        raw_task_count=len(rows),
        benchmarks=benchmark_summaries,
    )


def _core_task_scores(
    payloads: Sequence[tuple[Path, dict[str, Any]]],
    *,
    benchmark_configs: Sequence[BenchmarkConfig],
    core_components: Sequence[OverallBenchmarkConfig],
) -> list[CoreTaskScore]:
    core_benchmarks = {component.name for component in core_components}
    excluded_tasks = {
        benchmark.name: set(benchmark.excluded_tasks)
        for benchmark in benchmark_configs
    }
    rows: list[CoreTaskScore] = []
    for _, payload in payloads:
        target = payload.get("target")
        if not isinstance(target, dict):
            continue
        dataset_id = str(target.get("dataset_id") or "")
        dataset_name = str(target.get("dataset_name") or "")
        benchmark = benchmark_name(dataset_id, dataset_name, benchmark_configs=benchmark_configs)
        if benchmark not in core_benchmarks:
            continue
        raw_task_name = str(target.get("task_name") or target.get("split_name") or "")
        task_name = canonical_task_name(benchmark, raw_task_name)
        if task_name in excluded_tasks.get(benchmark, set()):
            continue
        score = _primary_metric_score(payload)
        if score is None:
            continue
        task_key = canonical_task_key(benchmark=benchmark, dataset_id=dataset_id, task_name=task_name)
        rows.append(
            CoreTaskScore(
                benchmark=benchmark,
                dataset_id=dataset_id,
                dataset_name=dataset_name,
                task_name=task_name,
                task_key=task_key,
                score=score,
            )
        )
    return rows


def _metadata_summary(
    payloads: Sequence[tuple[Path, dict[str, Any]]],
    *,
    result_dir: Path,
    repo_path: str,
    model_dir: str,
) -> dict[str, Any]:
    first_payload = payloads[0][1]
    model_payload = _dict_or_empty(first_payload.get("model"))
    environment = _dict_or_empty(first_payload.get("environment"))
    package_versions = _dict_or_empty(environment.get("package_versions"))
    cuda = _dict_or_empty(environment.get("cuda"))

    generated_at = _sorted_strings(payload.get("generated_at_utc") for _, payload in payloads)
    evaluated_at = _sorted_strings(
        _dict_get(payload.get("evaluation"), "evaluated_at_utc")
        or _dict_get(payload.get("evaluation"), "finished_at_utc")
        for _, payload in payloads
    )
    dataset_revisions = sorted(
        {
            str(revision)
            for _, payload in payloads
            if (revision := _dataset_revision(payload))
        }
    )
    configs = [payload.get("config") for _, payload in payloads if isinstance(payload.get("config"), dict)]
    models = [payload.get("model") for _, payload in payloads if isinstance(payload.get("model"), dict)]

    return {
        "result_dir": result_dir.as_posix(),
        "repo_path": repo_path,
        "model_dir": model_dir,
        "result_files": len(payloads),
        "json_xz_files": sum(1 for path, _ in payloads if path.as_posix().endswith(".json.xz")),
        "model_method": _set_summary(_dict_get(model, "method") for model in models),
        "model_source": _dict_get(model_payload, "id") or _dict_get(_dict_get(model_payload, "source"), "name") or model_dir,
        "model_revision": _dict_get(_dict_get(model_payload, "source"), "revision"),
        "dtype": _set_summary(_dict_get(model, "dtype") for model in models),
        "device": _set_summary(_dict_get(model, "device") for model in models),
        "attn_implementation": _set_summary(_dict_get(model, "attn_implementation") for model in models),
        "trust_remote_code": _set_summary(_dict_get(model, "trust_remote_code") for model in models),
        "max_seq_length": _set_summary(_dict_get(model, "max_seq_length") for model in models),
        "batch_size": _set_summary(_dict_get(config, "batch_size") for config in configs),
        "candidate_ranking": _set_summary(_dict_get(config, "candidate_ranking") for config in configs),
        "rerank_top_k": _set_summary(_dict_get(config, "rerank_top_k") for config in configs),
        "query_prompt_name": _set_summary(_dict_get(config, "query_prompt_name") for config in configs),
        "document_prompt_name": _set_summary(_dict_get(config, "document_prompt_name") for config in configs),
        "python": environment.get("python"),
        "platform": environment.get("platform"),
        "torch": package_versions.get("torch"),
        "transformers": package_versions.get("transformers"),
        "sentence_transformers": package_versions.get("sentence-transformers"),
        "datasets": package_versions.get("datasets"),
        "cuda_available": cuda.get("is_available"),
        "cuda_version": cuda.get("cuda_version"),
        "cuda_devices": _cuda_devices(cuda),
        "generated_at_first": generated_at[0] if generated_at else None,
        "generated_at_last": generated_at[-1] if generated_at else None,
        "evaluated_at_first": evaluated_at[0] if evaluated_at else None,
        "evaluated_at_last": evaluated_at[-1] if evaluated_at else None,
        "dataset_revisions": dataset_revisions,
    }


def _render_markdown(
    *,
    model_name: str,
    model_dir: str,
    repo_path: str,
    metadata: dict[str, Any],
    core_summary: CoreSummary,
    comparison_rows: Sequence[ComparisonRow] = (),
) -> str:
    core_score = _format_score(core_summary.score)
    dataset_revisions = metadata["dataset_revisions"]
    dataset_revision_value = _format_list(dataset_revisions, max_items=5)
    benchmark_rows = "\n".join(
        f"| {summary.benchmark} | {_format_score(summary.score)} | {summary.score_unit_count} | {summary.raw_task_count} |"
        for summary in core_summary.benchmarks
    )
    comparison_section = _render_comparison_section(comparison_rows, core_summary.benchmarks)

    return f"""# Add HAKARI-Bench results for `{model_name}`

## Summary

| Field | Value |
| --- | --- |
| Model | `{model_name}` |
| Result directory | `{model_dir}` |
| Target path | `{repo_path}` |
| Result files | {metadata["result_files"]} total, {metadata["json_xz_files"]} `.json.xz` |
| Evaluation method | {metadata["model_method"]} |
| Overall nDCG@10 | {core_score} |
| Overall score units | {core_summary.score_unit_count} grouped units from {core_summary.raw_task_count} raw task results |

{comparison_section}
## Overall nDCG@10

| Overall component | nDCG@10 | Score units | Raw task results |
| --- | ---: | ---: | ---: |
{benchmark_rows}

## Reproducibility

| Field | Value |
| --- | --- |
| Model source | `{metadata["model_source"]}` |
| Model revision | `{_format_optional(metadata["model_revision"])}` |
| Dataset revision(s) | {dataset_revision_value} |
| Evaluated at UTC | {_format_range(metadata["evaluated_at_first"], metadata["evaluated_at_last"])} |
| Generated at UTC | {_format_range(metadata["generated_at_first"], metadata["generated_at_last"])} |
| dtype | {metadata["dtype"]} |
| device | {metadata["device"]} |
| batch size | {metadata["batch_size"]} |
| attention implementation | {metadata["attn_implementation"]} |
| trust remote code | {metadata["trust_remote_code"]} |
| max sequence length | {metadata["max_seq_length"]} |
| candidate ranking | {metadata["candidate_ranking"]} |
| rerank top-k | {metadata["rerank_top_k"]} |
| query prompt name | {metadata["query_prompt_name"]} |
| document prompt name | {metadata["document_prompt_name"]} |
| Python | `{_format_optional(metadata["python"])}` |
| Platform | `{_format_optional(metadata["platform"])}` |
| torch | `{_format_optional(metadata["torch"])}` |
| transformers | `{_format_optional(metadata["transformers"])}` |
| sentence-transformers | `{_format_optional(metadata["sentence_transformers"])}` |
| datasets | `{_format_optional(metadata["datasets"])}` |
| CUDA | available={_format_optional(metadata["cuda_available"])}, version=`{_format_optional(metadata["cuda_version"])}` |
| CUDA devices | {_format_optional(metadata["cuda_devices"])} |

## Command

```bash
# TODO: paste the exact evaluation command or job manifest used to produce these files.
```

## Submitter Notes

- TODO: Describe any model-specific prompt, dtype, attention, trust-remote-code, or batching choices.
- TODO: Describe any retry, resumed run, failed task, memory adjustment, or other caveat.
- TODO: Confirm whether these are standard `--all` results or a narrower benchmark subset.

## Checklist

- [ ] Result files are committed under `{repo_path}/`.
- [ ] Result files are compressed `.json.xz`; no caches, DuckDB files, HTML reports, or local scratch artifacts are included.
- [ ] The result JSON records model revision, dataset revision, runtime configuration, and package versions.
- [ ] Overall nDCG@10 above was generated from the submitted result files.
- [ ] Any non-default prompt, sequence length, attention implementation, candidate ranking, or reranker setting is documented above.
"""


def _render_comparison_section(
    rows: Sequence[ComparisonRow],
    benchmark_summaries: Sequence[CoreBenchmarkSummary],
) -> str:
    if not rows:
        return ""
    headers = " | ".join(_comparison_column_label(row) for row in rows)
    alignments = " | ".join("---:" for _ in rows)
    body = "\n".join(
        _comparison_table_row(label, scores)
        for label, scores in [
            ("Overall", [row.score for row in rows]),
            *[
                (
                    summary.benchmark,
                    [row.component_scores.get(summary.benchmark) for row in rows],
                )
                for summary in benchmark_summaries
                if summary.raw_task_count > 0
            ],
        ]
    )
    return f"""## DuckDB Nano-set Comparison

Computed from DuckDB `task_results` with the same Overall grouping as this PR body. Quantized and rescore variants are excluded; truncate variants are considered, and each model column uses that model's best Overall variant.

| Overall component | {headers} |
| --- | {alignments} |
{body}

"""


def _comparison_table_row(label: str, scores: Sequence[float | None]) -> str:
    available = [score for score in scores if score is not None and not math.isnan(score)]
    best_score = max(available) if available else math.nan
    rendered_scores = [
        _format_best_score(score, best_score) if score is not None else "not available"
        for score in scores
    ]
    return f"| {label} | {' | '.join(rendered_scores)} |"


def _comparison_column_label(row: ComparisonRow) -> str:
    if row.variant_label in {"base", "submitted"}:
        return row.model_name
    return f"{row.model_name} ({row.variant_label})"


def _format_best_score(score: float, best_score: float) -> str:
    formatted = _format_score(score)
    if math.isclose(score, best_score, rel_tol=1e-12, abs_tol=1e-12):
        return f"**{formatted}**"
    return formatted


def _comparison_rows_from_duckdb(
    duckdb_path: Path | None,
    *,
    model_name: str,
    submitted_summary: CoreSummary,
    comparison_models: Sequence[str] | None,
    benchmark_configs: Sequence[BenchmarkConfig],
    core_components: Sequence[OverallBenchmarkConfig],
) -> list[ComparisonRow]:
    if duckdb_path is None:
        return []
    import duckdb

    model_ids = _comparison_model_ids(model_name, comparison_models)
    con = duckdb.connect(str(duckdb_path), read_only=True)
    try:
        rows: list[ComparisonRow] = []
        for model_id in model_ids:
            row = _best_comparison_row_for_model(
                    con,
                    model_id=model_id,
                    benchmark_configs=benchmark_configs,
                    core_components=core_components,
                )
            if row is None and model_id == model_name:
                row = _comparison_row_from_summary(model_name, submitted_summary)
            if row is not None:
                rows.append(row)
        return rows
    finally:
        con.close()


def _comparison_model_ids(model_name: str, comparison_models: Sequence[str] | None) -> list[str]:
    model_ids = [model_name]
    model_ids.extend(comparison_models if comparison_models is not None else DEFAULT_COMPARISON_MODELS)
    deduped: list[str] = []
    for model_id in model_ids:
        if model_id not in deduped:
            deduped.append(model_id)
    return deduped


def _best_comparison_row_for_model(
    con: Any,
    *,
    model_id: str,
    benchmark_configs: Sequence[BenchmarkConfig],
    core_components: Sequence[OverallBenchmarkConfig],
) -> ComparisonRow | None:
    excluded_tasks = {benchmark.name: set(benchmark.excluded_tasks) for benchmark in benchmark_configs}
    core_benchmarks = {component.name for component in core_components}
    rows_by_variant: dict[tuple[str | None, int | None], list[CoreTaskScore]] = defaultdict(list)
    for (
        benchmark,
        dataset_id,
        dataset_name,
        task_name,
        score,
        embedding_variant_name,
        embedding_dim,
    ) in con.execute(
        """
        SELECT
            benchmark,
            dataset_id,
            dataset_name,
            task_name,
            score,
            embedding_variant_name,
            embedding_dim
        FROM task_results
        WHERE model_name = ?
          AND lower(aggregate_metric) = ?
          AND score IS NOT NULL
          AND (quantization IS NULL OR quantization = '')
          AND (embedding_variant_name IS NULL OR embedding_variant_name LIKE 'truncate_dim_%')
        """,
        [model_id, PRIMARY_METRIC],
    ).fetchall():
        benchmark = str(benchmark or "")
        if benchmark not in core_benchmarks:
            continue
        task_name = canonical_task_name(benchmark, str(task_name or ""))
        if task_name in excluded_tasks.get(benchmark, set()):
            continue
        dataset_id = str(dataset_id or "")
        dataset_name = str(dataset_name or "")
        task_key = canonical_task_key(benchmark=benchmark, dataset_id=dataset_id, task_name=task_name)
        variant_key = (
            str(embedding_variant_name) if embedding_variant_name else None,
            int(embedding_dim) if embedding_dim is not None else None,
        )
        rows_by_variant[variant_key].append(
            CoreTaskScore(
                benchmark=benchmark,
                dataset_id=dataset_id,
                dataset_name=dataset_name,
                task_name=task_name,
                task_key=task_key,
                score=float(score),
            )
        )
    if not rows_by_variant:
        return None

    best: ComparisonRow | None = None
    for (variant_name, embedding_dim), task_rows in rows_by_variant.items():
        summary = summarize_core_scores(task_rows, core_components=core_components)
        if summary.score is None:
            continue
        row = ComparisonRow(
            model_name=model_id,
            score=summary.score,
            variant_label=_comparison_variant_label(variant_name, embedding_dim),
            score_unit_count=summary.score_unit_count,
            raw_task_count=summary.raw_task_count,
            component_scores={
                benchmark_summary.benchmark: benchmark_summary.score
                for benchmark_summary in summary.benchmarks
                if benchmark_summary.raw_task_count > 0
            },
        )
        if best is None or row.score > best.score:
            best = row
    return best


def _comparison_row_from_summary(model_name: str, summary: CoreSummary) -> ComparisonRow | None:
    if summary.score is None:
        return None
    return ComparisonRow(
        model_name=model_name,
        score=summary.score,
        variant_label="submitted",
        score_unit_count=summary.score_unit_count,
        raw_task_count=summary.raw_task_count,
        component_scores={
            benchmark_summary.benchmark: benchmark_summary.score
            for benchmark_summary in summary.benchmarks
            if benchmark_summary.raw_task_count > 0
        },
    )


def _comparison_variant_label(variant_name: str | None, embedding_dim: int | None) -> str:
    if variant_name and variant_name.startswith("truncate_dim_"):
        return f"{variant_name.removeprefix('truncate_dim_')} dims"
    if embedding_dim is not None:
        return f"{embedding_dim} dims"
    return "base"


def _model_name(payload: dict[str, Any], *, model_dir: str) -> str:
    model = payload.get("model")
    if not isinstance(model, dict):
        return model_dir
    return str(model.get("id") or _dict_get(model.get("source"), "name") or model_dir)


def _primary_metric_score(payload: dict[str, Any]) -> float | None:
    evaluation = payload.get("evaluation")
    if isinstance(evaluation, dict):
        metric = str(evaluation.get("aggregate_metric") or "").lower()
        value = evaluation.get("aggregate_metric_value")
        if metric == PRIMARY_METRIC and isinstance(value, int | float):
            return float(value)

    metrics = payload.get("metrics")
    if isinstance(metrics, dict):
        for key in sorted(metrics):
            value = metrics[key]
            if key.lower().endswith(PRIMARY_METRIC) and isinstance(value, int | float):
                return float(value)
    return None


def _dataset_revision(payload: dict[str, Any]) -> str | None:
    config_revision = _dict_get(payload.get("config"), "dataset_revision")
    if isinstance(config_revision, str) and config_revision:
        return config_revision
    target_revision = _dict_get(_dict_get(payload.get("target"), "dataset_revision"), "resolved")
    if isinstance(target_revision, str) and target_revision:
        return target_revision
    return None


def _score_group_key(row: CoreTaskScore, group_by: str) -> str:
    if group_by == "task_key":
        return row.task_key
    if group_by == "dataset_name":
        return row.dataset_name
    if group_by == "dataset_id":
        return row.dataset_id
    if group_by == "benchmark":
        return row.benchmark
    return row.task_name


def _mean(values: Iterable[float]) -> float:
    vals = list(values)
    return sum(vals) / len(vals)


def _dict_get(value: Any, key: str) -> Any:
    if isinstance(value, dict):
        return value.get(key)
    return None


def _dict_or_empty(value: Any) -> dict[str, Any]:
    if isinstance(value, dict):
        return value
    return {}


def _sorted_strings(values: Iterable[Any]) -> list[str]:
    return sorted(str(value) for value in values if isinstance(value, str) and value)


def _set_summary(values: Iterable[Any]) -> str:
    formatted = sorted({_format_optional(value) for value in values})
    if not formatted:
        return "not recorded"
    return ", ".join(formatted)


def _cuda_devices(cuda: dict[str, Any]) -> str | None:
    devices = cuda.get("devices")
    if not isinstance(devices, list):
        return None
    names = []
    for device in devices:
        if isinstance(device, dict):
            index = device.get("index")
            name = device.get("name")
            names.append(f"{index}: {name}" if index is not None else str(name))
    return ", ".join(names) if names else None


def _format_score(value: float | None) -> str:
    if value is None or math.isnan(value):
        return "not available"
    return f"{value:.4f}"


def _format_optional(value: Any) -> str:
    if value is None or value == "":
        return "not recorded"
    return str(value)


def _format_range(start: Any, end: Any) -> str:
    if not start and not end:
        return "not recorded"
    if start == end or not end:
        return f"`{start}`"
    return f"`{start}` to `{end}`"


def _format_list(values: Sequence[str], *, max_items: int) -> str:
    if not values:
        return "not recorded"
    rendered = ", ".join(f"`{value}`" for value in values[:max_items])
    if len(values) > max_items:
        rendered += f", ... ({len(values)} total)"
    return rendered


def main(argv: Sequence[str] | None = None) -> int:
    args = build_arg_parser().parse_args(argv)
    text = generate_pr_template(
        args.result_dir,
        config_dir=args.config_dir,
        repo_path=args.repo_path,
        comparison_duckdb_path=args.comparison_duckdb_path,
        comparison_models=args.comparison_models,
    )
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(text, encoding="utf-8")
    else:
        print(text)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
