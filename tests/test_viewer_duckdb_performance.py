from __future__ import annotations

import os
from pathlib import Path
import time

import pytest

from hakari_bench.viewer.data import TaskResultFacetFilters
from hakari_bench.viewer.leaderboard import (
    TaskScore,
    _filter_rows_by_facets,
    _load_task_scores_uncached,
)
from hakari_bench.viewer.variant_display import VariantDisplayFlags


def test_latest_duckdb_rank_facet_pushdown_matches_python_filter_and_is_not_slower() -> None:
    if os.getenv("HAKARI_BENCH_RUN_DUCKDB_PERF_TESTS") != "1":
        pytest.skip("Set HAKARI_BENCH_RUN_DUCKDB_PERF_TESTS=1 to run latest DuckDB performance checks.")
    duckdb_path = _latest_duckdb_path()
    if duckdb_path is None:
        pytest.skip("No latest leaderboard DuckDB found. Set HAKARI_BENCH_VIEWER_PERF_DUCKDB_PATH.")

    variant_flags = VariantDisplayFlags(quantization=True, truncate=True)
    facet_filters = TaskResultFacetFilters(
        dim_filters=("384",),
        quant_filters=("int8",),
        dtype_filters=("bf16",),
        attn_filters=("sdpa",),
        prompt_filters=("model_default",),
    )

    baseline_start = time.perf_counter()
    baseline_scores = list(
        _load_task_scores_uncached(
            duckdb_path=duckdb_path,
            benchmarks=("MNanoBEIR",),
            score_target="all",
            score_metric="ndcg@10",
            include_any_variants=True,
            variant_flags=variant_flags,
            facet_filters=None,
        )
    )
    baseline_filtered = _filter_rows_by_facets(
        baseline_scores,
        dim_filters=facet_filters.dim_filters,
        quant_filters=facet_filters.quant_filters,
        model_type_filters=facet_filters.model_type_filters,
        dtype_filters=facet_filters.dtype_filters,
        attn_filters=facet_filters.attn_filters,
        prompt_filters=facet_filters.prompt_filters,
    )
    baseline_seconds = time.perf_counter() - baseline_start

    pushdown_start = time.perf_counter()
    pushdown_scores = list(
        _load_task_scores_uncached(
            duckdb_path=duckdb_path,
            benchmarks=("MNanoBEIR",),
            score_target="all",
            score_metric="ndcg@10",
            include_any_variants=True,
            variant_flags=variant_flags,
            facet_filters=facet_filters,
        )
    )
    pushdown_filtered = _filter_rows_by_facets(
        pushdown_scores,
        dim_filters=facet_filters.dim_filters,
        quant_filters=facet_filters.quant_filters,
        model_type_filters=facet_filters.model_type_filters,
        dtype_filters=facet_filters.dtype_filters,
        attn_filters=facet_filters.attn_filters,
        prompt_filters=facet_filters.prompt_filters,
    )
    pushdown_seconds = time.perf_counter() - pushdown_start

    assert _task_score_signature(pushdown_filtered) == _task_score_signature(baseline_filtered)
    assert len(pushdown_scores) == len(pushdown_filtered)
    assert len(pushdown_scores) < len(baseline_scores)
    assert pushdown_seconds <= baseline_seconds * 1.25
    print(
        "latest DuckDB facet pushdown: "
        f"baseline={baseline_seconds:.3f}s/{len(baseline_scores)} rows, "
        f"pushdown={pushdown_seconds:.3f}s/{len(pushdown_scores)} rows"
    )


def _latest_duckdb_path() -> Path | None:
    configured = os.getenv("HAKARI_BENCH_VIEWER_PERF_DUCKDB_PATH")
    candidates = [
        Path(configured).expanduser() if configured else None,
        Path("output/clean-hf-results-duckdb/hakari-bench__results__xet/hakari_bench.duckdb"),
        Path("~/.cache/hakari-bench/duckdb/remote_latest_hakari_bench.duckdb").expanduser(),
    ]
    for candidate in candidates:
        if candidate is not None and candidate.is_file():
            return candidate
    return None


def _task_score_signature(rows: list[TaskScore]) -> list[tuple[object, ...]]:
    return sorted(
        (
            row.source_model_name,
            row.model_name,
            row.benchmark,
            row.dataset_id,
            row.task_key,
            row.embedding_variant_name,
            row.embedding_dim,
            row.quantization,
            row.score,
        )
        for row in rows
    )
