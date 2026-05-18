from __future__ import annotations

from hakari_bench.viewer.config import BenchmarkConfig, OverallConfig, ViewerConfig
from hakari_bench.viewer.leaderboard import LeaderboardResult
from hakari_bench.viewer.state import (
    FilterState,
    filter_state_from_query,
    normalize_query_state,
    query_string,
    state_payload,
)


def test_normalize_query_state_rejects_invalid_view_sort_and_direction() -> None:
    query = normalize_query_state(
        viewer_config=_viewer_config(),
        view="Missing",
        sort="not_a_column",
        direction="sideways",
        group="task",
        variants=False,
        quantization=False,
        truncate=False,
        rescore=False,
        other_variant=False,
        filters=False,
        dim_filter=None,
        quant_filter=None,
        dtype_filter=None,
        attn_filter=None,
        prompt_filter=None,
        model_filter="",
    )

    assert query == {"view": "Overall", "sort": "borda_rank", "direction": "asc", "group": "task"}


def test_normalize_query_state_keeps_explicit_display_flags_separate_from_filters() -> None:
    query = normalize_query_state(
        viewer_config=_viewer_config(),
        view="BenchA",
        sort="metric:task1",
        direction="desc",
        group=None,
        variants=False,
        quantization=True,
        truncate=False,
        rescore=False,
        other_variant=False,
        filters=True,
        dim_filter=["384", ""],
        quant_filter=["int8"],
        dtype_filter=["bf16"],
        attn_filter=[],
        prompt_filter=None,
        model_filter="  jina  ",
        task_scores=True,
        task_filter="  arguana  fever  ",
    )

    assert query == {
        "view": "BenchA",
        "sort": "metric:task1",
        "direction": "desc",
        "task_scores": "1",
        "quantization": "1",
        "filters": "1",
        "dim_filter": ["384"],
        "quant_filter": ["int8"],
        "dtype_filter": ["bf16"],
        "attn_filter": [],
        "prompt_filter": [],
        "model_filter": "jina",
        "task_filter": "arguana  fever",
    }


def test_legacy_variants_query_enables_all_variant_flags() -> None:
    query = normalize_query_state(
        viewer_config=_viewer_config(),
        view="BenchA",
        sort="borda_rank",
        direction="asc",
        group=None,
        variants=True,
        quantization=False,
        truncate=False,
        rescore=False,
        other_variant=False,
        filters=False,
        dim_filter=None,
        quant_filter=None,
        dtype_filter=None,
        attn_filter=None,
        prompt_filter=None,
        model_filter="",
    )

    assert query["quantization"] == "1"
    assert query["truncate"] == "1"
    assert query["rescore"] == "1"
    assert query["other_variant"] == "1"


def test_task_filter_enables_task_score_columns() -> None:
    query = normalize_query_state(
        viewer_config=_viewer_config(),
        view="BenchA",
        sort="borda_rank",
        direction="asc",
        group=None,
        variants=False,
        quantization=False,
        truncate=False,
        rescore=False,
        other_variant=False,
        filters=False,
        dim_filter=None,
        quant_filter=None,
        dtype_filter=None,
        attn_filter=None,
        prompt_filter=None,
        model_filter="",
        task_filter="fever",
    )

    assert query["task_scores"] == "1"
    assert query["task_filter"] == "fever"


def test_task_z_scores_do_not_force_task_score_columns() -> None:
    query = normalize_query_state(
        viewer_config=_viewer_config(),
        view="BenchA",
        sort="borda_rank",
        direction="asc",
        group=None,
        variants=False,
        quantization=False,
        truncate=False,
        rescore=False,
        other_variant=False,
        filters=False,
        dim_filter=None,
        quant_filter=None,
        dtype_filter=None,
        attn_filter=None,
        prompt_filter=None,
        model_filter="",
        task_z_scores=True,
    )

    assert "task_scores" not in query
    assert query["task_z_scores"] == "1"


def test_task_length_filters_are_normalized_into_filter_state() -> None:
    query = normalize_query_state(
        viewer_config=_viewer_config(),
        view="BenchA",
        sort="borda_rank",
        direction="asc",
        group=None,
        variants=False,
        quantization=False,
        truncate=False,
        rescore=False,
        other_variant=False,
        filters=False,
        dim_filter=None,
        quant_filter=None,
        dtype_filter=None,
        attn_filter=None,
        prompt_filter=None,
        model_filter="",
        query_len_min="-1",
        query_len_max=" 1000 ",
        doc_len_min="bad",
        doc_len_max="2000.5",
    )

    assert query["filters"] == "1"
    assert query["query_len_max"] == "1000"
    assert query["doc_len_max"] == "2000.5"
    assert "query_len_min" not in query
    assert "doc_len_min" not in query
    assert filter_state_from_query(query) == FilterState(
        filters_active=True,
        query_len_max="1000",
        doc_len_max="2000.5",
    )


def test_filter_state_from_query_accepts_scalar_or_list_query_values() -> None:
    state = filter_state_from_query(
        {
            "filters": "1",
            "model_filter": "bekko",
            "task_filter": "arguana",
            "dim_filter": "768",
            "quant_filter": ["int8", "binary"],
            "dtype_filter": [],
        }
    )

    assert state == FilterState(
        model_filter="bekko",
        task_filter="arguana",
        filters_active=True,
        dim_filters=("768",),
        quant_filters=("int8", "binary"),
    )


def test_state_payload_round_trips_display_and_filter_state() -> None:
    result = LeaderboardResult(
        view_name="BenchA",
        view_label="Bench A",
        is_overall=False,
        rows=[],
        expected_tasks=1,
        available_views=["Overall", "BenchA"],
        available_view_labels={"Overall": "Overall", "BenchA": "Bench A"},
        include_quantization_variants=True,
        show_task_z_scores=True,
        include_rescore_variants=True,
        score_groups=[],
        metric_columns=[],
    )

    query = state_payload(
        result=result,
        sort="mean_score",
        direction="desc",
        filter_state=FilterState(
            model_filter="jina",
            task_filter="fever",
            filters_active=True,
            dim_filters=("768",),
            quant_filters=("binary",),
        ),
    )

    assert query == {
        "view": "BenchA",
        "sort": "mean_score",
        "direction": "desc",
        "quantization": "1",
        "rescore": "1",
        "task_z_scores": "1",
        "model_filter": "jina",
        "task_filter": "fever",
        "filters": "1",
        "dim_filter": ["768"],
        "quant_filter": ["binary"],
        "dtype_filter": [],
        "attn_filter": [],
        "prompt_filter": [],
    }
    assert query_string(query["dim_filter"]) == "768"


def _viewer_config() -> ViewerConfig:
    return ViewerConfig(
        benchmarks=[BenchmarkConfig(name="BenchA")],
        overalls=[OverallConfig(name="Overall", label="Overall", benchmarks=["BenchA"])],
    )
