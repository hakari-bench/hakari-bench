"""JSON API for the React leaderboard frontend.

The legacy htmx routes render HTML server-side. These endpoints expose the same
underlying data (``LeaderboardResult`` and viewer configuration) as JSON so the
React frontend can own presentation. State handling mirrors the htmx routes:
the same query parameters drive both surfaces via
:func:`hakari_bench.viewer.state.normalize_query_state`.
"""

from __future__ import annotations

from typing import Any

from fastapi import APIRouter, Request
from fastapi.responses import JSONResponse, PlainTextResponse

from hakari_bench.viewer.config import CLEAR_SCOPE_NAME, ViewerConfig
from hakari_bench.viewer.filters import (
    FilterOption,
    attn_filter_options,
    commercial_filter_options,
    dim_filter_options,
    dtype_filter_options,
    model_type_filter_options,
    prompt_filter_options,
    quant_filter_options,
    row_filter_context,
)
from hakari_bench.viewer.results_builder import build_leaderboard_result
from hakari_bench.viewer.state import QueryState, normalize_query_state
from hakari_bench.viewer.store import LocalDuckDbStore


_BOOL_TRUE = {"1", "true", "on", "yes"}

_LIST_PARAMS = (
    "dim_filter",
    "quant_filter",
    "commercial_filter",
    "model_type_filter",
    "dtype_filter",
    "attn_filter",
    "prompt_filter",
    "lang_filter",
    "bench",
)

_BOOL_PARAMS = (
    "variants",
    "quantization",
    "truncate",
    "rescore",
    "other_variant",
    "task_scores",
    "task_z_scores",
    "task_ranks",
    "other_columns",
    "filters",
    "rank_filtered",
)

_STR_PARAMS = (
    "sort",
    "direction",
    "target",
    "score",
    "metric",
    "group",
    "model_filter",
    "task_filter",
    "active_params_min",
    "active_params_max",
    "total_params_min",
    "total_params_max",
    "query_len_min",
    "query_len_max",
    "doc_len_min",
    "doc_len_max",
    "result_view",
    "chart_y",
    "chart_x",
    "chart_color",
)


def _as_bool(value: str | None) -> bool:
    return value is not None and value.strip().casefold() in _BOOL_TRUE


def _facet_options(options: list[FilterOption]) -> list[dict[str, str]]:
    return [{"value": value, "label": label} for value, label in options]


def _metric_columns_meta(result, benchmark_docs) -> dict[str, Any]:
    """Per task-column metadata: two-line label, hover tooltip, and doc link."""

    from hakari_bench.viewer.app import (
        _metric_column_header_parts,
        _metric_column_labels,
        _metric_column_tooltip,
    )

    labels = _metric_column_labels(
        result.metric_columns,
        overrides=result.metric_column_labels,
        parent_label=result.view_name,
    )
    meta: dict[str, Any] = {}
    for column in result.metric_columns:
        label = labels[column]
        top, bottom = _metric_column_header_parts(label)
        doc = (
            benchmark_docs.task_doc(view_name=result.view_name, metric_column=column)
            if benchmark_docs is not None
            else None
        )
        meta[column] = {
            "label": label,
            "lines": [part for part in (top, bottom) if part],
            "tooltip": _metric_column_tooltip(label=label, full_metric_name=column, result=result),
            "doc": _doc_dict(doc),
        }
    return meta


def _task_breakdown_docs(result, benchmark_docs) -> dict[str, Any]:
    if benchmark_docs is None:
        return {}
    docs: dict[str, Any] = {}
    for breakdown in result.task_breakdowns:
        doc = benchmark_docs.task_doc(view_name=result.view_name, metric_column=breakdown.doc_key)
        if doc is not None:
            docs[breakdown.key] = {"title": doc.title, "url": doc.url}
    return docs


def _docs_document_response(benchmark_docs, *, benchmark: str, task: str | None = None) -> JSONResponse:
    from fastapi import HTTPException

    from hakari_bench.viewer.docs import render_markdown_to_html

    doc = benchmark_docs.route_doc(benchmark=benchmark, task=task) if benchmark_docs is not None else None
    if doc is None:
        raise HTTPException(status_code=404, detail="Benchmark documentation not found.")
    return JSONResponse(
        {
            "title": doc.title,
            "description": doc.description,
            "url": doc.url,
            "html": render_markdown_to_html(doc.markdown, base_url=doc.url),
        }
    )


def _query_state_from_request(request: Request, *, viewer_config: ViewerConfig) -> QueryState:
    """Map raw request query params onto :func:`normalize_query_state` kwargs."""

    params = request.query_params
    kwargs: dict[str, Any] = {
        "viewer_config": viewer_config,
        "view": params.get("view", viewer_config.overall.name),
        "sort": params.get("sort", "borda_score"),
        "direction": params.get("direction", "desc"),
    }
    for key in _STR_PARAMS:
        if key in ("sort", "direction"):
            continue
        if key in params:
            kwargs[key] = params[key]
    kwargs["group"] = params.get("group")
    for key in _BOOL_PARAMS:
        kwargs[key] = _as_bool(params.get(key))
    for key in _LIST_PARAMS:
        values = params.getlist(key)
        kwargs[key] = values if values else None
    return normalize_query_state(**kwargs)


def _doc_dict(doc) -> dict[str, str] | None:
    if doc is None:
        return None
    return {"title": doc.title, "description": doc.description, "url": doc.url}


def _scope_payload(viewer_config: ViewerConfig, benchmark_docs) -> dict[str, Any]:
    """Benchmark scope buttons: presets plus ordered Nano suite toggles.

    Mirrors the htmx render_tabs grouping/labels so the React controls match the
    legacy viewer (e.g. NanoMMTEB-v2 -> "MMTEB-v2", MNanoBEIR -> two buttons).
    """

    from hakari_bench.viewer.app import _view_group_sort_key

    def suite_doc(name: str) -> dict[str, str] | None:
        return _doc_dict(benchmark_docs.group_doc(name)) if benchmark_docs is not None else None

    presets = [
        {"name": "Overall", "label": "Overall", "kind": "overall", "help": "scope_overall"},
        {"name": "Overall (EN)", "label": "Overall (EN)", "kind": "overall", "help": "scope_overall_en"},
        {"name": CLEAR_SCOPE_NAME, "label": CLEAR_SCOPE_NAME, "kind": "clear", "help": "scope_clear"},
    ]
    suites: list[dict[str, Any]] = []
    for index, benchmark in enumerate(viewer_config.benchmarks):
        base_sort = _view_group_sort_key(view_name=benchmark.name, fallback=index)
        if benchmark.name == "MNanoBEIR":
            doc = suite_doc("MNanoBEIR")
            suites.append({"label": "M-BEIR(task)", "selection_key": "MNanoBEIR:task_mean", "benchmark": "MNanoBEIR", "sort_key": base_sort * 10, "doc": doc, "help": "mnanobeir_task"})
            suites.append({"label": "M-BEIR(lang)", "selection_key": "MNanoBEIR:lang_mean", "benchmark": "MNanoBEIR", "sort_key": base_sort * 10 + 1, "doc": doc, "help": "mnanobeir_lang"})
            continue
        label = benchmark.display_label
        if label.startswith("Nano"):
            label = label.removeprefix("Nano")
        suites.append({"label": label, "selection_key": benchmark.name, "benchmark": benchmark.name, "sort_key": base_sort * 10, "doc": suite_doc(benchmark.name)})
    suites.sort(key=lambda item: item["sort_key"])
    return {"presets": presets, "suites": suites}


def _config_payload(*, store: LocalDuckDbStore, viewer_config: ViewerConfig, benchmark_docs=None) -> dict[str, Any]:
    from hakari_bench.viewer.app import _database_footer_label, _fetch_database_latest_update_label

    return {
        "overalls": [{"name": overall.name, "label": overall.label} for overall in viewer_config.overalls],
        "benchmarks": [
            {"name": benchmark.name, "label": benchmark.display_label}
            for benchmark in viewer_config.benchmarks
        ],
        "scope": _scope_payload(viewer_config, benchmark_docs),
        "clear_scope": CLEAR_SCOPE_NAME,
        "defaults": {
            "view": viewer_config.overall.name,
            "sort": "borda_score",
            "direction": "desc",
            "target": "all",
            "score": "micro",
            "metric": "ndcg@10",
            "result_view": "table",
        },
        "footer": {
            "latest_update": _fetch_database_latest_update_label(store.path),
            "database_label": _database_footer_label(store),
        },
        "links": {
            "github": "https://github.com/hakari-bench/hakari-bench",
            "docs": "/docs/",
        },
    }


def create_api_router(
    *,
    store: LocalDuckDbStore,
    viewer_config: ViewerConfig,
    benchmark_docs=None,
) -> APIRouter:
    router = APIRouter(prefix="/api")

    @router.get("/docs")
    def docs_index() -> JSONResponse:
        groups = benchmark_docs.group_docs() if benchmark_docs is not None else []
        return JSONResponse(
            {
                "groups": [
                    {"title": doc.title, "description": doc.description, "url": doc.url}
                    for doc in groups
                ]
            }
        )

    @router.get("/docs/benchmark-tasks/{benchmark}")
    def docs_group(benchmark: str) -> JSONResponse:
        return _docs_document_response(benchmark_docs, benchmark=benchmark)

    @router.get("/docs/benchmark-tasks/{benchmark}/{task}")
    def docs_task(benchmark: str, task: str) -> JSONResponse:
        return _docs_document_response(benchmark_docs, benchmark=benchmark, task=task)

    @router.get("/config")
    def config() -> JSONResponse:
        return JSONResponse(
            _config_payload(store=store, viewer_config=viewer_config, benchmark_docs=benchmark_docs)
        )

    @router.get("/leaderboard")
    def leaderboard(request: Request) -> JSONResponse:
        store.start_background_sync()
        state_query = _query_state_from_request(request, viewer_config=viewer_config)
        result, sort, direction, filter_state = build_leaderboard_result(
            duckdb_path=store.path,
            viewer_config=viewer_config,
            state_query=state_query,
        )
        # Facet options come from the full scope rows so toggling never hides a
        # bucket. Row visibility reuses the htmx render-time FilterContext so the
        # dim/quant/license/model-type/dtype/attn/prompt/model-text filters match
        # the legacy viewer exactly (these are applied at display time, not SQL).
        all_rows = result.rows
        context = row_filter_context(all_rows, filter_state)
        visible_rows = [row for row in all_rows if context.is_visible(row)]

        payload = result.model_dump()
        payload["rows"] = [row.model_dump() for row in visible_rows]
        payload["all_rows"] = [row.model_dump() for row in all_rows]
        payload["total_row_count"] = len(all_rows)
        payload["effective_sort"] = sort
        payload["effective_direction"] = direction
        payload["query_state"] = state_query
        payload["metric_columns_meta"] = _metric_columns_meta(result, benchmark_docs)
        payload["task_breakdown_docs"] = _task_breakdown_docs(result, benchmark_docs)
        payload["filter_facets"] = {
            "dim": _facet_options(dim_filter_options(all_rows)),
            "quant": _facet_options(quant_filter_options(all_rows)),
            "commercial": _facet_options(commercial_filter_options(all_rows)),
            "model_type": _facet_options(model_type_filter_options(all_rows)),
            "dtype": _facet_options(dtype_filter_options(all_rows)),
            "attn": _facet_options(attn_filter_options(all_rows)),
            "prompt": _facet_options(prompt_filter_options(all_rows)),
        }
        payload["filter_selected"] = {
            "dim": list(context.selected_dims),
            "quant": context.ordered_selected_quants(),
            "commercial": context.ordered_selected_commercial(),
            "model_type": context.ordered_selected_model_types(),
            "dtype": context.ordered_selected_dtypes(),
            "attn": context.ordered_selected_attn(),
            "prompt": context.ordered_selected_prompts(),
        }
        return JSONResponse(payload)

    @router.get("/leaderboard.csv")
    def leaderboard_csv(request: Request) -> PlainTextResponse:
        from hakari_bench.viewer.app import render_leaderboard_csv

        state_query = _query_state_from_request(request, viewer_config=viewer_config)
        result, _sort, _direction, filter_state = build_leaderboard_result(
            duckdb_path=store.path,
            viewer_config=viewer_config,
            state_query=state_query,
        )
        csv_text = render_leaderboard_csv(result=result, filter_state=filter_state)
        return PlainTextResponse(
            csv_text,
            media_type="text/csv",
            headers={"Content-Disposition": "attachment; filename=hakari-bench-leaderboard.csv"},
        )

    @router.get("/sync-status")
    def sync_status() -> JSONResponse:
        status = store.start_background_sync()
        return JSONResponse(
            {
                "state": status.state,
                "message": status.message,
                "active": status.active,
                "progress_percent": status.progress_percent,
                "error": status.error,
            }
        )

    return router
