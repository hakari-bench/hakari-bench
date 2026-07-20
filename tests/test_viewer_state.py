from __future__ import annotations

from hakari_bench.viewer.config import BenchmarkConfig, OverallConfig, ScoreGroupConfig, ViewerConfig
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
        commercial_filter=["commercial", "non_commercial", "unknown"],
        model_type_filter=["bm25", "sparse", "reranker"],
        dtype_filter=["bf16"],
        attn_filter=[],
        prompt_filter=None,
        model_filter="  jina  ",
        rank_filtered=True,
        task_scores=True,
        task_filter="  arguana  fever  ",
    )

    assert query == {
        "view": "BenchA",
        "sort": "metric:task1",
        "direction": "desc",
        "columns": "task",
        "quantization": "1",
        "filters": "1",
        "dim_filter": ["384"],
        "quant_filter": ["int8"],
        "commercial_filter": ["commercial", "non_commercial", "unknown"],
        "model_type_filter": ["bm25", "sparse", "reranker"],
        "dtype_filter": ["bf16"],
        "attn_filter": [],
        "prompt_filter": [],
        "model_filter": "jina",
        "task_filter": "arguana  fever",
        "rank_filtered": "1",
    }


def test_normalize_query_state_ignores_none_sentinel_when_facet_values_are_selected() -> None:
    query = normalize_query_state(
        viewer_config=_viewer_config(),
        view="Overall",
        sort="borda_score",
        direction="desc",
        group=None,
        variants=False,
        quantization=True,
        truncate=False,
        rescore=False,
        other_variant=False,
        filters=True,
        dim_filter=["__none_selected__", "384", "768"],
        quant_filter=["__none_selected__", "__none__", "int8", "binary"],
        commercial_filter=["__none_selected__", "commercial"],
        model_type_filter=["__none_selected__", "dense"],
        dtype_filter=["__none_selected__", "bf16"],
        attn_filter=["__none_selected__", "sdpa"],
        prompt_filter=["__none_selected__", "model default"],
        model_filter="bge-m3 jina-embeddings-",
    )

    assert query["dim_filter"] == ["384", "768"]
    assert query["quant_filter"] == ["__none__", "int8", "binary"]
    assert query["commercial_filter"] == ["commercial"]
    assert query["model_type_filter"] == ["dense"]
    assert query["dtype_filter"] == ["bf16"]
    assert query["attn_filter"] == ["sdpa"]
    assert query["prompt_filter"] == ["model default"]


def test_normalize_query_state_keeps_none_sentinel_when_no_facet_value_is_selected() -> None:
    query = normalize_query_state(
        viewer_config=_viewer_config(),
        view="Overall",
        sort="borda_score",
        direction="desc",
        group=None,
        variants=False,
        quantization=True,
        truncate=False,
        rescore=False,
        other_variant=False,
        filters=True,
        dim_filter=["__none_selected__"],
        quant_filter=["__none_selected__"],
        commercial_filter=["__none_selected__"],
        model_type_filter=["__none_selected__"],
        dtype_filter=["__none_selected__"],
        attn_filter=["__none_selected__"],
        prompt_filter=["__none_selected__"],
        model_filter="",
    )

    assert query["dim_filter"] == ["__none_selected__"]
    assert query["quant_filter"] == ["__none_selected__"]
    assert query["commercial_filter"] == []
    assert query["model_type_filter"] == []
    assert query["dtype_filter"] == ["__none_selected__"]
    assert query["attn_filter"] == ["__none_selected__"]
    assert query["prompt_filter"] == ["__none_selected__"]


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


def test_chart_none_encoding_is_allowed_for_color_only() -> None:
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
        result_view="chart",
        chart_x="none",
        chart_color="none",
    )

    assert query["result_view"] == "chart"
    assert "chart_x" not in query
    assert query["chart_color"] == "none"


def test_chart_linear_parameter_axis_is_preserved_in_query_state() -> None:
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
        result_view="chart",
        chart_x="active_parameters_linear",
        chart_color="total_parameters_linear",
    )

    assert query["chart_x"] == "active_parameters_linear"
    assert query["chart_color"] == "total_parameters_linear"


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

    assert query["columns"] == "task"
    assert query["task_filter"] == "fever"


def test_task_column_mode_forces_micro_score() -> None:
    query = normalize_query_state(
        viewer_config=_viewer_config(),
        view="Overall",
        sort="borda_score",
        direction="desc",
        score="macro",
        columns=["task"],
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
    )

    assert query["columns"] == "task"
    assert "score" not in query
    assert "task_scores" not in query


def test_grouped_column_mode_forces_macro_score() -> None:
    query = normalize_query_state(
        viewer_config=_viewer_config(),
        view="Overall",
        sort="borda_score",
        direction="desc",
        score="micro",
        columns=["grouped"],
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
    )

    assert query["columns"] == "grouped"
    assert query["score"] == "macro"
    assert "task_scores" not in query


def test_column_modes_are_normalized_to_one_selection() -> None:
    query = normalize_query_state(
        viewer_config=_viewer_config(),
        view="Overall",
        sort="borda_score",
        direction="desc",
        columns=["task", "grouped"],
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
    )

    assert query["columns"] == "grouped"
    assert query["score"] == "macro"


def test_custom_benchmark_selection_is_normalized() -> None:
    query = normalize_query_state(
        viewer_config=_viewer_config(),
        view="Custom",
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
        bench=["BenchB", "Missing", "BenchA", "BenchA"],
    )

    assert query == {
        "view": "Custom",
        "sort": "borda_rank",
        "direction": "asc",
        "bench": ["BenchB", "BenchA"],
    }


def test_mnanobeir_task_and_lang_selection_are_exclusive() -> None:
    query = normalize_query_state(
        viewer_config=_viewer_config(),
        view="Custom",
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
        bench=["MNanoBEIR:task_mean", "BenchA", "MNanoBEIR:lang_mean"],
    )

    assert query["bench"] == ["BenchA", "MNanoBEIR:lang_mean"]


def test_bare_mnanobeir_selection_defaults_to_task_mean() -> None:
    query = normalize_query_state(
        viewer_config=_viewer_config(),
        view="Custom",
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
        bench=["MNanoBEIR"],
    )

    assert query["bench"] == ["MNanoBEIR:task_mean"]


def test_empty_custom_benchmark_selection_stays_custom_and_resets_language() -> None:
    query = normalize_query_state(
        viewer_config=_viewer_config(),
        view="Custom",
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
        bench=[],
        lang_filter=["ja"],
    )

    assert query == {"view": "Custom", "sort": "borda_rank", "direction": "asc"}


def test_overall_en_view_normalizes_to_en_language_filter() -> None:
    query = normalize_query_state(
        viewer_config=_viewer_config(),
        view="Overall (EN)",
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
        lang_filter=["ja"],
    )

    assert query == {
        "view": "Overall (EN)",
        "sort": "borda_rank",
        "direction": "asc",
        "lang_filter": ["en"],
    }


def test_legacy_clear_view_normalizes_to_empty_custom() -> None:
    query = normalize_query_state(
        viewer_config=_viewer_config(),
        view="Clear",
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
        task_scores=True,
        lang_filter=["ja"],
    )

    assert query == {"view": "Custom", "sort": "borda_rank", "direction": "asc", "columns": "task"}


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


def test_task_ranks_force_task_score_columns() -> None:
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
        task_ranks=True,
        other_columns=True,
    )

    assert query["columns"] == "task"
    assert query["task_ranks"] == "1"
    assert query["other_columns"] == "1"


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


def test_parameter_filters_are_normalized_into_filter_state() -> None:
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
        active_params_min="-1",
        active_params_max=" 100 ",
        total_params_min="bad",
        total_params_max="250.5",
    )

    assert query["filters"] == "1"
    assert query["active_params_max"] == "100"
    assert query["total_params_max"] == "250.5"
    assert "active_params_min" not in query
    assert "total_params_min" not in query
    assert filter_state_from_query(query) == FilterState(
        filters_active=True,
        active_params_max="100",
        total_params_max="250.5",
    )


def test_filter_state_from_query_accepts_scalar_or_list_query_values() -> None:
    state = filter_state_from_query(
        {
            "filters": "1",
            "model_filter": "bekko",
            "task_filter": "arguana",
            "dim_filter": "768",
            "quant_filter": ["int8", "binary"],
            "model_type_filter": "sparse",
            "dtype_filter": [],
        }
    )

    assert state == FilterState(
        model_filter="bekko",
        task_filter="arguana",
        filters_active=True,
        dim_filters=("768",),
        quant_filters=("int8", "binary"),
        model_type_filters=("sparse",),
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
        show_task_ranks=True,
        show_other_columns=True,
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
            rank_filtered=True,
            filters_active=True,
            dim_filters=("768",),
            quant_filters=("binary",),
            commercial_filters=("commercial",),
            model_type_filters=("sparse",),
        ),
    )

    assert query == {
        "view": "BenchA",
        "sort": "mean_score",
        "direction": "desc",
        "quantization": "1",
        "rescore": "1",
        "task_z_scores": "1",
        "task_ranks": "1",
        "other_columns": "1",
        "model_filter": "jina",
        "task_filter": "fever",
        "rank_filtered": "1",
        "filters": "1",
        "dim_filter": ["768"],
        "quant_filter": ["binary"],
        "commercial_filter": ["commercial"],
        "model_type_filter": ["sparse"],
        "dtype_filter": [],
        "attn_filter": [],
        "prompt_filter": [],
    }
    assert query_string(query["dim_filter"]) == "768"


def _viewer_config() -> ViewerConfig:
    return ViewerConfig(
        benchmarks=[
            BenchmarkConfig(name="BenchA"),
            BenchmarkConfig(name="BenchB"),
            BenchmarkConfig(
                name="MNanoBEIR",
                score_groups=[
                    ScoreGroupConfig(name="task_mean", group_by="task_name"),
                    ScoreGroupConfig(name="lang_mean", group_by="dataset_name"),
                ],
            ),
        ],
        overalls=[
            OverallConfig(name="Overall", label="Overall", benchmarks=["BenchA"]),
            OverallConfig(name="Overall (EN)", label="Overall (EN)", benchmarks=["BenchA"]),
        ],
    )
