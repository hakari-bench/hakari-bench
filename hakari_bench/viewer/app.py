from __future__ import annotations

import csv
from functools import lru_cache
import hashlib
from html import escape
from io import StringIO
import math
import os
from pathlib import Path
from typing import TypedDict, cast
from urllib.parse import urlencode

from pydantic import BaseModel, ConfigDict

from hakari_bench.viewer.analytics import ViewerAnalyticsRepository, ViewerSummary
from hakari_bench.viewer.config import ViewerConfig, load_viewer_config
from hakari_bench.viewer.docs import BenchmarkDoc, BenchmarkDocs, render_docs_index_page, render_markdown_page
from hakari_bench.viewer.filters import (
    FILTER_NONE_VALUE,
    FilterContext,
    row_filter_context,
    visible_row_count,
)
from hakari_bench.viewer.leaderboard import (
    LanguageOption,
    LeaderboardResult,
    LeaderboardRow,
    LeaderboardService,
    ScoreTarget,
    SortDirection,
)
from hakari_bench.viewer.model_display import model_cell_views, render_model_detail_modal, render_model_name_cell
from hakari_bench.viewer.model_types import model_type_filter_key
from hakari_bench.viewer.observability import timed_operation
from hakari_bench.viewer.state import (
    FilterState,
    QueryState,
    active_filter_hidden_fields,
    filter_state_from_query,
    normalize_query_state,
    optional_query_string,
    query_string,
    state_payload,
    task_length_bounds,
)
from hakari_bench.viewer.store import LocalDuckDbStore
from hakari_bench.viewer.variant_display import (
    variant_display_flags_from_query,
)

ASSETS_DIR = Path(__file__).with_name("assets")
DEFAULT_FRAME_ANCESTORS = "https://huggingface.co https://*.huggingface.co"
SECURITY_HEADERS = {
    "X-Content-Type-Options": "nosniff",
    "Referrer-Policy": "strict-origin-when-cross-origin",
    "Permissions-Policy": "camera=(), microphone=(), geolocation=(), payment=(), usb=()",
}
Z_SCORE_BUCKET_CLASSES = (
    "task-z-neutral",
    "task-z-pos-025",
    "task-z-pos-050",
    "task-z-pos-075",
    "task-z-pos-100",
    "task-z-pos-125",
    "task-z-pos-150",
    "task-z-pos-175",
    "task-z-pos-200",
    "task-z-neg-025",
    "task-z-neg-050",
    "task-z-neg-075",
    "task-z-neg-100",
    "task-z-neg-125",
    "task-z-neg-150",
    "task-z-neg-175",
    "task-z-neg-200",
)

_ICON_PATHS = {
    "activity": '<path d="M22 12h-4l-3 9L9 3l-3 9H2"/>',
    "arrow-down-up": (
        '<path d="m3 16 4 4 4-4"/>'
        '<path d="M7 20V4"/>'
        '<path d="m21 8-4-4-4 4"/>'
        '<path d="M17 4v16"/>'
    ),
    "bar-chart-3": (
        '<path d="M3 3v18h18"/>'
        '<path d="M18 17V9"/>'
        '<path d="M13 17V5"/>'
        '<path d="M8 17v-3"/>'
    ),
    "binary": '<path d="M6 20h4"/><path d="M14 10h4"/><path d="M6 14h2v6"/><path d="M14 4h2v6"/>',
    "braces": '<path d="M8 3H7a2 2 0 0 0-2 2v4a2 2 0 0 1-2 2 2 2 0 0 1 2 2v4a2 2 0 0 0 2 2h1"/><path d="M16 21h1a2 2 0 0 0 2-2v-4a2 2 0 0 1 2-2 2 2 0 0 1-2-2V7a2 2 0 0 0-2-2h-1"/>',
    "circle-help": (
        '<circle cx="12" cy="12" r="10"/>'
        '<path d="M9.09 9a3 3 0 0 1 5.83 1c0 2-3 3-3 3"/>'
        '<path d="M12 17h.01"/>'
    ),
    "cpu": '<rect width="16" height="16" x="4" y="4" rx="2"/><path d="M9 9h6v6H9z"/><path d="M9 1v3"/><path d="M15 1v3"/><path d="M9 20v3"/><path d="M15 20v3"/><path d="M20 9h3"/><path d="M20 14h3"/><path d="M1 9h3"/><path d="M1 14h3"/>',
    "database": '<ellipse cx="12" cy="5" rx="9" ry="3"/><path d="M3 5v14c0 1.7 4 3 9 3s9-1.3 9-3V5"/><path d="M3 12c0 1.7 4 3 9 3s9-1.3 9-3"/>',
    "eye": '<path d="M2.06 12.35a1 1 0 0 1 0-.7C3.42 7.7 7.16 5 12 5s8.58 2.7 9.94 6.65a1 1 0 0 1 0 .7C20.58 16.3 16.84 19 12 19s-8.58-2.7-9.94-6.65"/><circle cx="12" cy="12" r="3"/>',
    "file-spreadsheet": (
        '<path d="M15 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V7Z"/>'
        '<path d="M14 2v4a2 2 0 0 0 2 2h4"/>'
        '<path d="M8 13h2"/>'
        '<path d="M14 13h2"/>'
        '<path d="M8 17h2"/>'
        '<path d="M14 17h2"/>'
    ),
    "filter": '<polygon points="22 3 2 3 10 12.46 10 19 14 21 14 12.46 22 3"/>',
    "git-branch": '<line x1="6" x2="6" y1="3" y2="15"/><circle cx="18" cy="6" r="3"/><circle cx="6" cy="18" r="3"/><path d="M18 9a9 9 0 0 1-9 9"/>',
    "git-compare-arrows": '<circle cx="5" cy="6" r="3"/><circle cx="19" cy="18" r="3"/><path d="M12 6h3a4 4 0 0 1 4 4v5"/><path d="m15 9-3-3 3-3"/><path d="M12 18H9a4 4 0 0 1-4-4V9"/><path d="m9 15 3 3-3 3"/>',
    "languages": '<path d="m5 8 6 6"/><path d="m4 14 6-6 2-3"/><path d="M2 5h12"/><path d="M7 2h1"/><path d="m22 22-5-10-5 10"/><path d="M14 18h6"/>',
    "layers": '<path d="m12.83 2.18 8.5 4.73a1 1 0 0 1 0 1.75l-8.5 4.73a1.7 1.7 0 0 1-1.66 0l-8.5-4.73a1 1 0 0 1 0-1.75l8.5-4.73a1.7 1.7 0 0 1 1.66 0Z"/><path d="m22 12.5-9.17 5.1a1.7 1.7 0 0 1-1.66 0L2 12.5"/><path d="m22 17.5-9.17 5.1a1.7 1.7 0 0 1-1.66 0L2 17.5"/>',
    "ruler": '<path d="M21.3 15.3a2.4 2.4 0 0 1 0 3.4l-2.6 2.6a2.4 2.4 0 0 1-3.4 0L2.7 8.7a2.4 2.4 0 0 1 0-3.4l2.6-2.6a2.4 2.4 0 0 1 3.4 0Z"/><path d="m14.5 12.5 2-2"/><path d="m11.5 9.5 2-2"/><path d="m8.5 6.5 2-2"/><path d="m17.5 15.5 2-2"/>',
    "table-properties": '<path d="M15 3v18"/><rect width="18" height="18" x="3" y="3" rx="2"/><path d="M21 9H3"/><path d="M21 15H3"/>',
}


class _TaskLengthFilterKwargs(TypedDict):
    rank_filtered: bool
    query_len_min: str
    query_len_max: str
    doc_len_min: str
    doc_len_max: str


class ViewerAppConfig(BaseModel):
    model_config = ConfigDict(frozen=True)

    duckdb_path: Path
    config_dir: Path = Path("config/viewer")


def create_app(*, store: LocalDuckDbStore, config_dir: Path = Path("config/viewer"), docs_dir: Path = Path("docs/benchmark_tasks")):
    from fastapi import FastAPI, Query
    from fastapi.middleware.gzip import GZipMiddleware
    from fastapi.responses import FileResponse, HTMLResponse, Response
    from fastapi.staticfiles import StaticFiles

    viewer_config = load_viewer_config(config_dir)
    benchmark_docs = BenchmarkDocs(docs_dir)
    app = FastAPI(title="HAKARI-bench leaderboard")
    app.add_middleware(GZipMiddleware, minimum_size=1024)
    app.mount("/assets", StaticFiles(directory=ASSETS_DIR), name="assets")

    @app.middleware("http")
    async def security_headers(request, call_next):  # type: ignore[no-untyped-def]
        response = await call_next(request)
        for header, value in SECURITY_HEADERS.items():
            response.headers.setdefault(header, value)
        response.headers.setdefault("Content-Security-Policy", _content_security_policy())
        return response

    @app.get("/favicon.png")
    def favicon() -> FileResponse:
        return FileResponse(ASSETS_DIR / "favicon.png", media_type="image/png")

    @app.get("/favicon.ico")
    def favicon_ico() -> FileResponse:
        return FileResponse(ASSETS_DIR / "favicon.png", media_type="image/png")

    @app.get("/docs/benchmark-tasks", response_class=HTMLResponse)
    def benchmark_docs_index() -> HTMLResponse:
        return HTMLResponse(render_docs_index_page(docs=benchmark_docs.group_docs(), css_version=_asset_version("app.css")))

    @app.get("/docs/benchmark-tasks/{benchmark}", response_class=HTMLResponse)
    def benchmark_doc(benchmark: str) -> HTMLResponse:
        from fastapi import HTTPException

        doc = benchmark_docs.route_doc(benchmark=benchmark)
        if doc is None:
            raise HTTPException(status_code=404, detail="Benchmark documentation not found.")
        return HTMLResponse(render_markdown_page(doc=doc, css_version=_asset_version("app.css")))

    @app.get("/docs/benchmark-tasks/{benchmark}/{task}", response_class=HTMLResponse)
    def benchmark_task_doc(benchmark: str, task: str) -> HTMLResponse:
        from fastapi import HTTPException

        doc = benchmark_docs.route_doc(benchmark=benchmark, task=task)
        if doc is None:
            raise HTTPException(status_code=404, detail="Benchmark task documentation not found.")
        return HTMLResponse(render_markdown_page(doc=doc, css_version=_asset_version("app.css")))

    @app.get("/", response_class=HTMLResponse)
    def index(
        view: str = Query(default=viewer_config.overall.name),
        sort: str = Query(default="borda_rank"),
        direction: str = Query(default="asc", pattern="^(asc|desc)$"),
        target: str = Query(default="all", pattern="^(all|reranking)$"),
        metric: str = Query(default="ndcg@10"),
        group: str | None = Query(default=None),
        variants: bool = Query(default=False),
        quantization: bool = Query(default=False),
        truncate: bool = Query(default=False),
        rescore: bool = Query(default=False),
        other_variant: bool = Query(default=False),
        task_scores: bool = Query(default=False),
        task_z_scores: bool = Query(default=False),
        task_ranks: bool = Query(default=False),
        filters: bool = Query(default=False),
        dim_filter: list[str] | None = Query(default=None),
        quant_filter: list[str] | None = Query(default=None),
        model_type_filter: list[str] | None = Query(default=None),
        dtype_filter: list[str] | None = Query(default=None),
        attn_filter: list[str] | None = Query(default=None),
        prompt_filter: list[str] | None = Query(default=None),
        lang_filter: list[str] | None = Query(default=None),
        model_filter: str = Query(default=""),
        task_filter: str = Query(default=""),
        rank_filtered: bool = Query(default=False),
        query_len_min: str = Query(default=""),
        query_len_max: str = Query(default=""),
        doc_len_min: str = Query(default=""),
        doc_len_max: str = Query(default=""),
    ) -> str:
        with timed_operation("viewer.http.request", route="index") as request_timing:
            store.ensure_current()
            initial_query = normalize_query_state(
                viewer_config=viewer_config,
                view=view,
                sort=sort,
                direction=direction,
                target=target,
                metric=metric,
                group=group,
                variants=variants,
                quantization=quantization,
                truncate=truncate,
                rescore=rescore,
                other_variant=other_variant,
                task_scores=task_scores,
                task_z_scores=task_z_scores,
                task_ranks=task_ranks,
                filters=filters,
                dim_filter=dim_filter,
                quant_filter=quant_filter,
                model_type_filter=model_type_filter,
                dtype_filter=dtype_filter,
                attn_filter=attn_filter,
                prompt_filter=prompt_filter,
                lang_filter=lang_filter,
                model_filter=model_filter,
                task_filter=task_filter,
                rank_filtered=rank_filtered,
                query_len_min=query_len_min,
                query_len_max=query_len_max,
                doc_len_min=doc_len_min,
                doc_len_max=doc_len_max,
            )
            if not task_z_scores:
                initial_query["task_z_scores"] = "0"
            summary = ViewerAnalyticsRepository(store.path).fetch_summary()
            with timed_operation("viewer.render", operation="render_page"):
                content = render_page(
                    viewer_config=viewer_config,
                    duckdb_path=store.path,
                    summary=summary,
                    initial_query=initial_query,
                    benchmark_docs=benchmark_docs,
                )
            request_timing["view"] = initial_query["view"]
            return content

    def build_leaderboard_result(state_query: QueryState) -> tuple[LeaderboardResult, str, str, FilterState]:
        view = query_string(state_query["view"])
        sort = query_string(state_query["sort"])
        direction = query_string(state_query["direction"])
        target = query_string(state_query.get("target", "all"))
        score_metric = query_string(state_query.get("metric", "ndcg@10"))
        group = optional_query_string(state_query.get("group"))
        display_flags = variant_display_flags_from_query(state_query)
        filter_state = filter_state_from_query(state_query)
        length_bounds = task_length_bounds(filter_state)
        service = LeaderboardService(duckdb_path=store.path, config=viewer_config)
        result = service.get_leaderboard(
            view,
            sort=sort,
            direction=cast(SortDirection, direction),
            score_target=cast(ScoreTarget, target),
            score_metric=score_metric,
            score_group_name=group,
            include_quantization_variants=display_flags.quantization,
            include_truncate_variants=display_flags.truncate,
            include_rescore_variants=display_flags.rescore,
            include_other_variants=display_flags.other,
            language_filters=filter_state.language_filters,
            show_task_scores=state_query.get("task_scores") == "1",
            show_task_z_scores=state_query.get("task_z_scores") == "1",
            show_task_ranks=state_query.get("task_ranks") == "1",
            rank_filtered=filter_state.rank_filtered,
            model_filter=filter_state.model_filter,
            task_filter=filter_state.task_filter,
            dim_filters=filter_state.dim_filters if filter_state.filters_active else (),
            quant_filters=filter_state.quant_filters if filter_state.filters_active else (),
            model_type_filters=filter_state.model_type_filters if filter_state.filters_active else (),
            dtype_filters=filter_state.dtype_filters if filter_state.filters_active else (),
            attn_filters=filter_state.attn_filters if filter_state.filters_active else (),
            prompt_filters=filter_state.prompt_filters if filter_state.filters_active else (),
            query_min_chars=length_bounds["query_min_chars"],
            query_max_chars=length_bounds["query_max_chars"],
            document_min_chars=length_bounds["document_min_chars"],
            document_max_chars=length_bounds["document_max_chars"],
        )
        return result, sort, direction, filter_state

    @app.get("/leaderboard", response_class=HTMLResponse)
    def leaderboard(
        view: str = Query(default=viewer_config.overall.name),
        sort: str = Query(default="borda_rank"),
        direction: str = Query(default="asc", pattern="^(asc|desc)$"),
        target: str = Query(default="all", pattern="^(all|reranking)$"),
        metric: str = Query(default="ndcg@10"),
        group: str | None = Query(default=None),
        variants: bool = Query(default=False),
        quantization: bool = Query(default=False),
        truncate: bool = Query(default=False),
        rescore: bool = Query(default=False),
        other_variant: bool = Query(default=False),
        task_scores: bool = Query(default=False),
        task_z_scores: bool = Query(default=False),
        task_ranks: bool = Query(default=False),
        filters: bool = Query(default=False),
        dim_filter: list[str] | None = Query(default=None),
        quant_filter: list[str] | None = Query(default=None),
        model_type_filter: list[str] | None = Query(default=None),
        dtype_filter: list[str] | None = Query(default=None),
        attn_filter: list[str] | None = Query(default=None),
        prompt_filter: list[str] | None = Query(default=None),
        lang_filter: list[str] | None = Query(default=None),
        model_filter: str = Query(default=""),
        task_filter: str = Query(default=""),
        rank_filtered: bool = Query(default=False),
        query_len_min: str = Query(default=""),
        query_len_max: str = Query(default=""),
        doc_len_min: str = Query(default=""),
        doc_len_max: str = Query(default=""),
    ) -> HTMLResponse:
        with timed_operation("viewer.http.request", route="leaderboard") as request_timing:
            store.ensure_current()
            state_query = normalize_query_state(
                viewer_config=viewer_config,
                view=view,
                sort=sort,
                direction=direction,
                target=target,
                metric=metric,
                group=group,
                variants=variants,
                quantization=quantization,
                truncate=truncate,
                rescore=rescore,
                other_variant=other_variant,
                task_scores=task_scores,
                task_z_scores=task_z_scores,
                task_ranks=task_ranks,
                filters=filters,
                dim_filter=dim_filter,
                quant_filter=quant_filter,
                model_type_filter=model_type_filter,
                dtype_filter=dtype_filter,
                attn_filter=attn_filter,
                prompt_filter=prompt_filter,
                lang_filter=lang_filter,
                model_filter=model_filter,
                task_filter=task_filter,
                rank_filtered=rank_filtered,
                query_len_min=query_len_min,
                query_len_max=query_len_max,
                doc_len_min=doc_len_min,
                doc_len_max=doc_len_max,
            )
            result, sort, direction, filter_state = build_leaderboard_result(state_query)
            with timed_operation("viewer.render", operation="render_leaderboard", view=view) as render_timing:
                content = render_leaderboard(result=result, sort=sort, direction=direction, filter_state=filter_state, benchmark_docs=benchmark_docs)
                render_timing["leaderboard_row_count"] = len(result.rows)
            request_timing["view"] = result.view_name
            request_timing["leaderboard_row_count"] = len(result.rows)
            return HTMLResponse(content=content, headers={"HX-Push-Url": f"/?{urlencode(state_query, doseq=True)}"})

    @app.get("/leaderboard.csv")
    def leaderboard_csv(
        view: str = Query(default=viewer_config.overall.name),
        sort: str = Query(default="borda_rank"),
        direction: str = Query(default="asc", pattern="^(asc|desc)$"),
        target: str = Query(default="all", pattern="^(all|reranking)$"),
        metric: str = Query(default="ndcg@10"),
        group: str | None = Query(default=None),
        variants: bool = Query(default=False),
        quantization: bool = Query(default=False),
        truncate: bool = Query(default=False),
        rescore: bool = Query(default=False),
        other_variant: bool = Query(default=False),
        task_scores: bool = Query(default=False),
        task_z_scores: bool = Query(default=False),
        task_ranks: bool = Query(default=False),
        filters: bool = Query(default=False),
        dim_filter: list[str] | None = Query(default=None),
        quant_filter: list[str] | None = Query(default=None),
        model_type_filter: list[str] | None = Query(default=None),
        dtype_filter: list[str] | None = Query(default=None),
        attn_filter: list[str] | None = Query(default=None),
        prompt_filter: list[str] | None = Query(default=None),
        lang_filter: list[str] | None = Query(default=None),
        model_filter: str = Query(default=""),
        task_filter: str = Query(default=""),
        rank_filtered: bool = Query(default=False),
        query_len_min: str = Query(default=""),
        query_len_max: str = Query(default=""),
        doc_len_min: str = Query(default=""),
        doc_len_max: str = Query(default=""),
    ) -> Response:
        with timed_operation("viewer.http.request", route="leaderboard_csv") as request_timing:
            store.ensure_current()
            state_query = normalize_query_state(
                viewer_config=viewer_config,
                view=view,
                sort=sort,
                direction=direction,
                target=target,
                metric=metric,
                group=group,
                variants=variants,
                quantization=quantization,
                truncate=truncate,
                rescore=rescore,
                other_variant=other_variant,
                task_scores=task_scores,
                task_z_scores=task_z_scores,
                task_ranks=task_ranks,
                filters=filters,
                dim_filter=dim_filter,
                quant_filter=quant_filter,
                model_type_filter=model_type_filter,
                dtype_filter=dtype_filter,
                attn_filter=attn_filter,
                prompt_filter=prompt_filter,
                lang_filter=lang_filter,
                model_filter=model_filter,
                task_filter=task_filter,
                rank_filtered=rank_filtered,
                query_len_min=query_len_min,
                query_len_max=query_len_max,
                doc_len_min=doc_len_min,
                doc_len_max=doc_len_max,
            )
            result, sort, direction, filter_state = build_leaderboard_result(state_query)
            with timed_operation("viewer.render", operation="render_leaderboard_csv", view=result.view_name) as render_timing:
                content = render_leaderboard_csv(result=result, filter_state=filter_state)
                render_timing["leaderboard_row_count"] = len(result.rows)
            request_timing["view"] = result.view_name
            filename = _csv_filename(view=result.view_name, target=result.score_target)
            return Response(
                content=content,
                media_type="text/csv; charset=utf-8",
                headers={"Content-Disposition": f'attachment; filename="{filename}"'},
            )

    @app.get("/analysis", response_class=HTMLResponse)
    def analysis(
        panel: str = Query(default="variants", pattern="^(variants|reranking|datasets)$"),
        view: str = Query(default=viewer_config.overall.name),
        include_rescore: bool = Query(default=False),
        include_truncate: bool = Query(default=False),
    ) -> HTMLResponse:
        with timed_operation("viewer.http.request", route="analysis", panel=panel) as request_timing:
            store.ensure_current()
            if view not in viewer_config.view_names:
                view = viewer_config.overall.name
            benchmarks = viewer_config.benchmarks_for_view(view)
            repository = ViewerAnalyticsRepository(store.path)
            if panel == "reranking":
                rows = repository.fetch_rerank_diagnostics(benchmarks=benchmarks)
                with timed_operation("viewer.render", operation="render_reranking_panel", view=view) as render_timing:
                    content = render_reranking_panel(
                        view_label=viewer_config.label_for_view(view),
                        rows=rows,
                    )
                    render_timing["row_count"] = len(rows)
            elif panel == "datasets":
                rows = repository.fetch_dataset_diagnostics(benchmarks=benchmarks)
                with timed_operation("viewer.render", operation="render_dataset_diagnostics_panel", view=view) as render_timing:
                    content = render_dataset_diagnostics_panel(
                        view_label=viewer_config.label_for_view(view),
                        rows=rows,
                    )
                    render_timing["row_count"] = len(rows)
            else:
                rows = repository.fetch_variant_analysis(
                    benchmarks=benchmarks,
                    include_rescore=include_rescore,
                    include_truncate=include_truncate,
                )
                with timed_operation("viewer.render", operation="render_variant_panel", view=view) as render_timing:
                    content = render_variant_panel(
                        view_name=view,
                        view_label=viewer_config.label_for_view(view),
                        rows=rows,
                        include_rescore=include_rescore,
                        include_truncate=include_truncate,
                    )
                    render_timing["row_count"] = len(rows)
            request_timing["view"] = view
            return HTMLResponse(content=content)

    return app


def _content_security_policy() -> str:
    frame_ancestors = _frame_ancestors()
    return "; ".join(
        [
            "default-src 'self'",
            "script-src 'self'",
            "style-src 'self'",
            "img-src 'self' data:",
            "connect-src 'self'",
            "base-uri 'none'",
            f"frame-ancestors {frame_ancestors}",
        ]
    )


def _frame_ancestors() -> str:
    value = os.environ.get("HAKARI_BENCH_VIEWER_FRAME_ANCESTORS", DEFAULT_FRAME_ANCESTORS)
    tokens = value.split()
    if any("\r" in token or "\n" in token for token in tokens):
        return DEFAULT_FRAME_ANCESTORS
    return " ".join(tokens) or DEFAULT_FRAME_ANCESTORS


def render_page(
    *,
    viewer_config: ViewerConfig,
    duckdb_path: Path,
    summary: ViewerSummary | None = None,
    initial_query: QueryState | None = None,
    benchmark_docs: BenchmarkDocs | None = None,
) -> str:
    query = urlencode(initial_query or {"view": viewer_config.overall.name, "sort": "borda_rank", "direction": "asc"}, doseq=True)
    css_url = _asset_url("app.css")
    favicon_url = _asset_url("favicon.png")
    htmx_url = _asset_url("htmx.min.js")
    viewer_js_url = _asset_url("viewer.js")
    return f"""<!doctype html>
<html lang="ja">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>HAKARI-bench leaderboard</title>
  <link rel="canonical" href="/">
  <link rel="stylesheet" href="{css_url}">
  <link rel="icon" type="image/png" href="{favicon_url}">
  <meta name="htmx-config" content='{{"allowEval":false,"allowScriptTags":false,"includeIndicatorStyles":false}}'>
  <script src="{htmx_url}"></script>
  <script src="{viewer_js_url}" defer></script>
</head>
<body class="bg-zinc-50 text-zinc-950">
  <main class="mx-auto max-w-[1600px] px-4 py-6 sm:px-6">
    <header class="mb-5 border-b border-zinc-200 pb-4">
      <h1 class="flex items-center gap-2 text-2xl font-semibold">
        <img src="{favicon_url}" alt="" aria-hidden="true" class="h-8 w-8 shrink-0">
        <span>HAKARI-bench leaderboard</span>
      </h1>
      <p class="mt-2 border border-amber-200 bg-amber-50 px-3 py-2 text-sm font-medium text-amber-800">🚧 WIP: This leaderboard is currently under active implementation, so specifications and data may change significantly.</p>
      <p class="mt-2 max-w-4xl text-sm text-zinc-600">Compare multilingual retrieval models, inspect compression variants, and audit reranking and Nano subset diagnostics from the DuckDB result warehouse.</p>
    </header>
    {render_summary_cards(summary or ViewerSummary())}
    <section
      id="leaderboard-panel"
      hx-get="{_leaderboard_url(query)}"
      hx-trigger="load"
      {_leaderboard_request_hx_attrs()}
    >
      <div class="border border-zinc-200 bg-white px-4 py-3 text-sm text-zinc-600">Loading leaderboard...</div>
    </section>
    {render_leaderboard_loading_toast()}
    {render_global_tooltip()}
  </main>
</body>
</html>"""


@lru_cache(maxsize=None)
def _asset_url(filename: str) -> str:
    return f"/assets/{filename}?v={_asset_version(filename)}"


@lru_cache(maxsize=None)
def _asset_version(filename: str) -> str:
    return hashlib.sha256((ASSETS_DIR / filename).read_bytes()).hexdigest()[:12]


def _leaderboard_request_hx_attrs() -> str:
    return 'hx-target="#leaderboard-panel" hx-swap="innerHTML" hx-indicator="#leaderboard-loading-toast" hx-sync="#leaderboard-panel:replace"'


def _leaderboard_control_hx_attrs() -> str:
    return f'{_leaderboard_request_hx_attrs()} data-leaderboard-control="true"'


def render_leaderboard_loading_toast() -> str:
    return """
    <div id="leaderboard-loading-toast"
         class="leaderboard-loading-toast fixed bottom-4 right-4 z-50 border border-zinc-300 bg-white px-3 py-2 text-sm font-medium text-zinc-800 shadow-sm"
         role="status" aria-live="polite" aria-atomic="true">
      Loading leaderboard...
    </div>
    """


def render_global_tooltip() -> str:
    return """
    <div id="hakari-global-tooltip" class="global-tooltip fixed border border-zinc-300 bg-white px-2 py-1 text-xs font-medium text-zinc-800 shadow-sm"
         role="tooltip" hidden></div>
    """


def _icon_svg(name: str, *, class_name: str = "hakari-icon") -> str:
    path = _ICON_PATHS[name]
    return (
        f"""<svg class="{class_name}" data-icon="{escape(name, quote=True)}" aria-hidden="true" """
        """viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" """
        f"""stroke-linecap="round" stroke-linejoin="round">{path}</svg>"""
    )


def _section_title(*, icon: str, text: str, class_name: str = "text-base font-semibold") -> str:
    return (
        f"""<h2 class="inline-flex items-center gap-1.5 {class_name}">"""
        f"""{_icon_svg(icon, class_name="hakari-icon section-heading-icon shrink-0")}"""
        f"""<span>{escape(text)}</span></h2>"""
    )


def _control_label(*, icon: str, text: str, extra_class: str = "") -> str:
    spacing = f" {extra_class}" if extra_class else ""
    return (
        f"""<span class="inline-flex items-center gap-1 font-medium text-zinc-800{spacing}">"""
        f"""{_icon_svg(icon, class_name="hakari-icon control-heading-icon shrink-0")}"""
        f"""<span>{escape(text)}</span></span>"""
    )


def render_doc_summary_modal() -> str:
    return """
<dialog id="doc-summary-modal" class="w-[min(92vw,42rem)] border border-zinc-300 bg-white p-0 text-zinc-950 backdrop:bg-zinc-950/35">
  <form method="dialog">
    <div class="flex items-center justify-between border-b border-zinc-200 px-4 py-3">
      <h3 class="text-base font-semibold">Benchmark Documentation</h3>
      <button type="submit" class="border border-zinc-300 px-2 py-1 text-sm text-zinc-700 hover:border-cyan-600 hover:text-cyan-700">Close</button>
    </div>
  </form>
  <div class="px-4 py-3">
    <p id="doc-summary-title" class="break-all font-mono text-sm font-semibold text-zinc-900"></p>
    <p id="doc-summary-description" class="mt-3 whitespace-pre-wrap text-sm leading-tight text-zinc-700"></p>
    <p class="mt-3 text-sm">
      <a id="doc-summary-link" class="text-cyan-700 underline-offset-2 hover:underline" href="#" target="_blank" rel="noopener noreferrer">Read the benchmark overview</a>
    </p>
  </div>
</dialog>
"""


def _render_doc_summary_trigger(*, doc: BenchmarkDoc, label: str) -> str:
    return f"""<button type="button"
                  class="doc-summary-trigger inline-flex h-3.5 w-3.5 shrink-0 cursor-pointer items-center justify-center rounded-full border border-zinc-300 text-[9px] leading-none text-zinc-600 hover:border-cyan-600 hover:text-cyan-700"
                  data-doc-title="{escape(doc.title, quote=True)}"
                  data-doc-description="{escape(doc.description, quote=True)}"
                  data-doc-url="{escape(doc.url, quote=True)}"
                  aria-label="{escape(label, quote=True)}">{_icon_svg("circle-help")}</button>"""


def _render_help_tooltip(tooltip: str) -> str:
    return f"""<span tabindex="0"
                    class="tooltip-trigger inline-flex h-3.5 w-3.5 shrink-0 cursor-pointer items-center justify-center rounded-full border border-zinc-300 text-[9px] leading-none text-zinc-600 hover:border-cyan-600 hover:text-cyan-700"
                    data-tooltip="{escape(tooltip, quote=True)}"
                    data-tooltip-placement="left"
                    aria-label="{escape(tooltip, quote=True)}">{_icon_svg("circle-help")}</span>"""


def render_summary_cards(summary: ViewerSummary) -> str:
    cards = [
        ("Models", f"{summary.model_count:,}", "summary-card-models"),
        ("Benchmarks", f"{summary.benchmark_count:,}", "summary-card-benchmarks"),
        ("Tasks", f"{summary.task_count:,}", "summary-card-tasks"),
        ("Languages", f"{summary.language_count:,}", "summary-card-languages"),
        ("Base rows", f"{summary.base_result_count:,}", "summary-card-base"),
        ("Variant rows", f"{summary.variant_result_count:,}", "summary-card-variants"),
    ]
    card_html = "".join(
        f"""
        <div data-testid="{escape(testid)}" class="border border-zinc-200 bg-white px-3 py-2">
          <p class="text-xs font-medium uppercase text-zinc-500">{escape(label)}</p>
          <p class="mt-1 text-xl font-semibold tabular-nums text-zinc-950">{escape(value)}</p>
        </div>
        """
        for label, value, testid in cards
    )
    timestamp = (
        f"""<p class="mt-2 text-xs text-zinc-500">Latest result: <span class="font-mono">{escape(summary.latest_finished_at_utc)}</span></p>"""
        if summary.latest_finished_at_utc
        else ""
    )
    return f"""
    <section class="mb-5" aria-label="Benchmark coverage">
      <div class="mb-2 flex flex-wrap items-end justify-between gap-2">
        <div>
          {_section_title(icon="bar-chart-3", text="Benchmark coverage")}
          <p class="text-sm text-zinc-600">Result warehouse size and coverage visible in this viewer.</p>
        </div>
        {timestamp}
      </div>
      <div class="grid gap-2 sm:grid-cols-3 lg:grid-cols-6">{card_html}</div>
    </section>
    """


def render_analysis_shell(*, view: str) -> str:
    variant_query = urlencode({"panel": "variants", "view": view})
    rerank_query = urlencode({"panel": "reranking", "view": view})
    dataset_query = urlencode({"panel": "datasets", "view": view})
    return f"""
    <section class="mb-5 border border-zinc-200 bg-white" aria-label="Analysis views">
      <div class="flex flex-wrap items-center justify-between gap-2 border-b border-zinc-200 px-3 py-2">
        <div>
          {_section_title(icon="activity", text="Analysis views")}
          <p class="text-sm text-zinc-600">Use these panels for paper-facing variant, reranking, and Nano subset audits.</p>
        </div>
        <div class="flex flex-wrap gap-2">
          <button type="button" class="inline-flex items-center gap-1.5 border border-zinc-300 px-2 py-1 text-[0.8125rem] text-zinc-800 hover:border-cyan-600 hover:text-cyan-700"
                  hx-get="/analysis?{escape(variant_query, quote=True)}" hx-target="#analysis-panel" hx-swap="innerHTML">{_icon_svg("git-compare-arrows", class_name="hakari-icon action-icon shrink-0")}<span>Variant impact</span></button>
          <button type="button" class="inline-flex items-center gap-1.5 border border-zinc-300 px-2 py-1 text-[0.8125rem] text-zinc-800 hover:border-cyan-600 hover:text-cyan-700"
                  hx-get="/analysis?{escape(rerank_query, quote=True)}" hx-target="#analysis-panel" hx-swap="innerHTML">{_icon_svg("arrow-down-up", class_name="hakari-icon action-icon shrink-0")}<span>Reranking diagnostics</span></button>
          <button type="button" class="inline-flex items-center gap-1.5 border border-zinc-300 px-2 py-1 text-[0.8125rem] text-zinc-800 hover:border-cyan-600 hover:text-cyan-700"
                  hx-get="/analysis?{escape(dataset_query, quote=True)}" hx-target="#analysis-panel" hx-swap="innerHTML">{_icon_svg("database", class_name="hakari-icon action-icon shrink-0")}<span>Dataset diagnostics</span></button>
        </div>
      </div>
      <div id="analysis-panel">
        <div class="border-t border-zinc-200 px-3 py-3 text-sm text-zinc-600">Select an analysis view to load paper-facing diagnostics for the current benchmark view.</div>
      </div>
    </section>
    """


def render_leaderboard(
    *,
    result: LeaderboardResult,
    sort: str,
    direction: str,
    filter_state: FilterState | None = None,
    benchmark_docs: BenchmarkDocs | None = None,
) -> str:
    filter_state = filter_state or FilterState()
    filter_context = row_filter_context(result.rows, filter_state)
    shown_count = visible_row_count(result.rows, filter_context)
    csv_query = urlencode(state_payload(result=result, sort=sort, direction=direction, filter_state=filter_state), doseq=True)
    return f"""
<div>
  {render_analysis_shell(view=result.view_name)}
  {render_tabs(result=result, sort=sort, direction=direction, filter_state=filter_state, benchmark_docs=benchmark_docs)}
  {render_language_pages(result=result, sort=sort, direction=direction, filter_state=filter_state)}
  {render_controls(result=result, sort=sort, direction=direction, filter_state=filter_state, filter_context=filter_context)}
  {render_score_groups(result=result, sort=sort, direction=direction, filter_state=filter_state)}
  <div class="mb-3 flex flex-wrap items-end justify-between gap-3">
    <div>
      <h2 class="text-lg font-semibold">{escape(result.view_label)}</h2>
      <p class="mt-1 text-sm text-zinc-600" data-shown-count="{shown_count}">
        {shown_count} shown / {len(result.rows)} complete models / {result.expected_tasks} tasks
        <a class="ml-2 inline-flex items-center gap-1 border border-zinc-300 bg-zinc-50 px-2 py-0.5 text-xs font-medium text-zinc-800 underline-offset-2 hover:border-cyan-600 hover:text-cyan-700"
           href="{_csv_url(csv_query)}" aria-label="Download visible leaderboard as CSV">
          {_icon_svg("file-spreadsheet", class_name="hakari-icon h-3.5 w-3.5")}
          <span>Download CSV</span>
        </a>
      </p>
    </div>
  </div>
  <div class="leaderboard-table-scroll overflow-x-auto border border-zinc-200 bg-white">
    <table class="leaderboard-table min-w-full border-collapse text-[0.8125rem]">
      {render_table_head(result=result, sort=sort, direction=direction, filter_state=filter_state, benchmark_docs=benchmark_docs)}
      {render_table_body(result=result, filter_context=filter_context)}
    </table>
  </div>
  {render_model_detail_modal()}
  {render_doc_summary_modal()}
</div>
"""


def render_tabs(
    *,
    result: LeaderboardResult,
    sort: str,
    direction: str,
    filter_state: FilterState | None = None,
    benchmark_docs: BenchmarkDocs | None = None,
) -> str:
    filter_state = filter_state or FilterState()
    grouped_buttons: dict[str, list[str]] = {
        "Overall": [],
        "Core benchmarks": [],
        "Language-specific": [],
        "Domain-specific": [],
    }
    for view_name in result.available_views:
        active = view_name == result.view_name
        view_label = result.available_view_labels.get(view_name, view_name)
        classes = (
            "border-cyan-700 bg-cyan-50 text-cyan-900"
            if active
            else "border-zinc-300 bg-white text-zinc-700 hover:border-cyan-500 hover:text-cyan-700"
        )
        tab_sort = "borda_rank" if sort.startswith("metric:") else sort
        tab_direction = "asc" if sort.startswith("metric:") else direction
        query_payload = state_payload(result=result, sort=tab_sort, direction=tab_direction, filter_state=filter_state)
        query_payload["view"] = view_name
        query = urlencode(query_payload, doseq=True)
        doc = benchmark_docs.group_doc(view_name) if benchmark_docs is not None else None
        if doc is None:
            grouped_buttons[_view_group(view_name)].append(
                f"""<button type="button" class="border px-2 py-1 text-[0.8125rem] {classes}"
                      hx-get="{_leaderboard_url(query)}" hx-push-url="{_page_url(query_payload)}"
                      {_leaderboard_control_hx_attrs()}>
                      {escape(view_label)}
                    </button>"""
            )
            continue
        doc_trigger = _render_doc_summary_trigger(doc=doc, label=f"{view_label} overview")
        grouped_buttons[_view_group(view_name)].append(
            f"""<span class="doc-label-group inline-flex items-center border text-[0.8125rem] {classes}" data-doc-label-group="benchmark">
                  <button type="button" class="py-1 pl-2 pr-0 text-left"
                    hx-get="{_leaderboard_url(query)}" hx-push-url="{_page_url(query_payload)}"
                    {_leaderboard_control_hx_attrs()}>
                    {escape(view_label)}
                  </button>
                  <span class="inline-flex items-center pl-0.5 pr-2">{doc_trigger}</span>
                </span>"""
        )
    primary_sections = [
        _render_target_group(result=result, sort=sort, direction=direction, filter_state=filter_state),
        _render_metric_group(result=result, sort=sort, direction=direction, filter_state=filter_state),
        _render_benchmark_group(label="Overall", buttons=grouped_buttons.pop("Overall")),
        _render_benchmark_group(label="Core benchmarks", buttons=grouped_buttons.pop("Core benchmarks")),
    ]
    groups = [
        f"""
            <div class="min-w-0 space-y-3" data-testid="primary-benchmark-column">
              {''.join(section for section in primary_sections if section)}
            </div>
            """
    ]
    for label, buttons in grouped_buttons.items():
        if not buttons:
            continue
        groups.append(
            f"""
            <div class="min-w-0" data-testid="secondary-benchmark-column">
              {_render_benchmark_group(label=label, buttons=buttons)}
            </div>
            """
        )
    return f"""
    <nav class="mb-4 border border-zinc-200 bg-white p-3" aria-label="Benchmark views">
      <div class="mb-2 flex items-center justify-between gap-2">
        {_section_title(icon="layers", text="Benchmark groups", class_name="text-sm font-semibold")}
        <p class="text-xs text-zinc-500">Views are grouped to keep multilingual and domain-specific suites scannable.</p>
      </div>
      <div class="grid gap-3">{''.join(groups)}</div>
    </nav>
    """


def _render_benchmark_group(*, label: str, buttons: list[str]) -> str:
    if not buttons:
        return ""
    return f"""
              <div>
                <p class="mb-1 text-xs font-semibold uppercase text-zinc-500">{escape(label)}</p>
                <div class="flex flex-wrap gap-2">{''.join(buttons)}</div>
              </div>
            """


def _render_target_group(*, result: LeaderboardResult, sort: str, direction: str, filter_state: FilterState) -> str:
    target_options = [
        ("all", "All"),
        ("reranking", "Reranking"),
    ]
    tooltip = (
        "All shows full-corpus retrieval scores and excludes cross-encoder reranker runs. "
        "Reranking shows BM25 top-100 reranking scores when available. BM25 is omitted only for @100 metrics because the candidate subset can contain relevant documents at the tail."
    )
    buttons = []
    for target, label in target_options:
        active = result.score_target == target
        classes = (
            "border-cyan-700 bg-cyan-50 text-cyan-900"
            if active
            else "border-zinc-300 bg-white text-zinc-700 hover:border-cyan-500 hover:text-cyan-700"
        )
        tab_sort = "borda_rank" if sort.startswith("metric:") else sort
        tab_direction = "asc" if sort.startswith("metric:") else direction
        query_payload = state_payload(result=result, sort=tab_sort, direction=tab_direction, filter_state=filter_state)
        if target == "all":
            query_payload.pop("target", None)
        else:
            query_payload["target"] = target
        query = urlencode(query_payload, doseq=True)
        buttons.append(
            f"""<button type="button" class="border px-2 py-1 text-[0.8125rem] {classes}"
                  hx-get="{_leaderboard_url(query)}" hx-push-url="{_page_url(query_payload)}"
                  {_leaderboard_control_hx_attrs()}>
                  {escape(label)}
                </button>"""
        )
    return f"""
            <div>
              <p class="mb-1 inline-flex items-center gap-1 text-xs font-semibold uppercase text-zinc-500">
                <span>Target</span>
                {_render_help_tooltip(tooltip)}
              </p>
              <div class="flex flex-wrap gap-2">{''.join(buttons)}</div>
            </div>
            """


def _render_metric_group(*, result: LeaderboardResult, sort: str, direction: str, filter_state: FilterState) -> str:
    if len(result.available_score_metrics) <= 1:
        return ""
    buttons = []
    for metric in result.available_score_metrics:
        active = metric == result.selected_score_metric
        classes = (
            "border-cyan-700 bg-cyan-50 text-cyan-900"
            if active
            else "border-zinc-300 bg-white text-zinc-700 hover:border-cyan-500 hover:text-cyan-700"
        )
        tab_sort = "borda_rank" if sort.startswith("metric:") else sort
        tab_direction = "asc" if sort.startswith("metric:") else direction
        query_payload = state_payload(result=result, sort=tab_sort, direction=tab_direction, filter_state=filter_state)
        if metric == "ndcg@10":
            query_payload.pop("metric", None)
        else:
            query_payload["metric"] = metric
        query = urlencode(query_payload, doseq=True)
        buttons.append(
            f"""<button type="button" class="border px-2 py-1 text-[0.8125rem] {classes}"
                  hx-get="{_leaderboard_url(query)}" hx-push-url="{_page_url(query_payload)}"
                  {_leaderboard_control_hx_attrs()}>
                  {escape(_score_metric_label(metric))}
                </button>"""
        )
    return f"""
            <div>
              <p class="mb-1 text-xs font-semibold uppercase text-zinc-500">Metric</p>
              <div class="flex flex-wrap gap-2">{''.join(buttons)}</div>
            </div>
            """


def _score_metric_label(metric: str) -> str:
    family, separator, cutoff = metric.partition("@")
    labels = {
        "ndcg": "nDCG",
        "map": "MAP",
        "mrr": "MRR",
        "accuracy": "Acc",
        "precision": "Precision",
        "recall": "Recall",
    }
    return f"{labels.get(family, family.upper())}@{cutoff}" if separator else metric


def _view_group(view_name: str) -> str:
    overall_views = {"All", "Core", "Group"}
    language_specific_views = {
        "NanoCMTEB",
        "NanoFaMTEB-v2",
        "NanoJMTEB-v2",
        "NanoRuMTEB",
        "NanoVNMTEB",
    }
    if view_name in overall_views or view_name.startswith("Overall"):
        return "Overall"
    if view_name.startswith("NanoMTEB-") or view_name in language_specific_views:
        return "Language-specific"
    if view_name in {
        "MNanoBEIR",
        "NanoMMTEB-v2",
        "NanoRTEB",
        "NanoMLDR",
        "NanoBRIGHT",
        "NanoLaw",
        "NanoCoIR",
    }:
        return "Core benchmarks"
    return "Domain-specific"


def render_language_pages(
    *,
    result: LeaderboardResult,
    sort: str,
    direction: str,
    filter_state: FilterState | None = None,
) -> str:
    filter_state = filter_state or FilterState()
    if not result.available_languages:
        return ""

    buttons = [
        _language_page_button(
            option=None,
            result=result,
            sort=sort,
            direction=direction,
            filter_state=filter_state,
        )
    ]
    visible_options = result.available_languages[:12]
    more_options = result.available_languages[12:]
    buttons.extend(
        _language_page_button(
            option=option,
            result=result,
            sort=sort,
            direction=direction,
            filter_state=filter_state,
        )
        for option in visible_options
    )
    more = ""
    if more_options:
        more_buttons = "".join(
            _language_page_button(
                option=option,
                result=result,
                sort=sort,
                direction=direction,
                filter_state=filter_state,
            )
            for option in more_options
        )
        more = f"""
          <details class="relative">
            <summary class="cursor-pointer border border-zinc-300 bg-white px-2 py-1 text-[0.8125rem] text-zinc-700 hover:border-cyan-500 hover:text-cyan-700">More</summary>
            <div class="absolute z-10 mt-1 grid max-h-72 min-w-[28rem] grid-cols-3 gap-1 overflow-auto border border-zinc-300 bg-white p-2 shadow-sm sm:grid-cols-5">
              {more_buttons}
            </div>
          </details>
        """
    return f"""
      <nav class="mb-4 flex flex-wrap items-start gap-2" aria-label="Language pages">
        {_control_label(icon="languages", text="Language pages", extra_class="pt-1 text-[0.8125rem]")}
        {''.join(buttons)}
        {more}
      </nav>
    """


def _language_page_button(
    *,
    option: LanguageOption | None,
    result: LeaderboardResult,
    sort: str,
    direction: str,
    filter_state: FilterState,
) -> str:
    language_filters = () if option is None else (option.code,)
    active = result.selected_languages == language_filters
    label = "All" if option is None else f"{option.label} {option.task_count}"
    classes = (
        "border-cyan-700 bg-cyan-50 text-cyan-900"
        if active
        else "border-zinc-300 bg-white text-zinc-700 hover:border-cyan-500 hover:text-cyan-700"
    )
    query_payload = state_payload(
        result=result,
        sort=sort,
        direction=direction,
        filter_state=_filter_state_with_languages(filter_state, language_filters),
    )
    query = urlencode(query_payload, doseq=True)
    data_attr = "" if option is None else f' data-language-page="{escape(option.code)}"'
    return f"""<button type="button"{data_attr} class="border px-2 py-1 text-[0.8125rem] {classes}"
              hx-get="{_leaderboard_url(query)}" hx-push-url="{_page_url(query_payload)}"
              {_leaderboard_control_hx_attrs()}>{escape(label)}</button>"""


def _filter_state_with_languages(filter_state: FilterState, language_filters: tuple[str, ...]) -> FilterState:
    return FilterState(
        model_filter=filter_state.model_filter,
        task_filter=filter_state.task_filter,
        language_filters=language_filters,
        filters_active=filter_state.filters_active,
        dim_filters=filter_state.dim_filters,
        quant_filters=filter_state.quant_filters,
        model_type_filters=filter_state.model_type_filters,
        dtype_filters=filter_state.dtype_filters,
        attn_filters=filter_state.attn_filters,
        prompt_filters=filter_state.prompt_filters,
        **_task_length_filter_kwargs(filter_state),
    )


def _task_length_filter_kwargs(filter_state: FilterState) -> _TaskLengthFilterKwargs:
    return {
        "rank_filtered": filter_state.rank_filtered,
        "query_len_min": filter_state.query_len_min,
        "query_len_max": filter_state.query_len_max,
        "doc_len_min": filter_state.doc_len_min,
        "doc_len_max": filter_state.doc_len_max,
    }


def render_controls(
    *,
    result: LeaderboardResult,
    sort: str,
    direction: str,
    filter_state: FilterState | None = None,
    filter_context: FilterContext | None = None,
) -> str:
    filter_state = filter_state or FilterState()
    filter_context = filter_context or row_filter_context(result.rows, filter_state)
    quantization_checked = " checked" if result.include_quantization_variants else ""
    truncate_checked = " checked" if result.include_truncate_variants else ""
    rescore_checked = " checked" if result.include_rescore_variants else ""
    other_variant_checked = " checked" if result.include_other_variants else ""
    task_scores_checked = " checked" if result.show_task_scores else ""
    task_z_scores_checked = " checked" if result.show_task_z_scores else ""
    task_ranks_checked = " checked" if result.show_task_ranks else ""
    rank_filtered_checked = " checked" if filter_state.rank_filtered else ""
    state_fields = [
        ("view", result.view_name),
        ("sort", sort),
        ("direction", direction),
    ]
    if result.score_target != "all":
        state_fields.append(("target", result.score_target))
    if result.selected_score_metric != "ndcg@10":
        state_fields.append(("metric", result.selected_score_metric))
    if result.selected_score_group is not None:
        state_fields.append(("group", result.selected_score_group.name))
    sticky_filter_fields = active_filter_hidden_fields(filter_state) + _text_filter_hidden_fields(filter_state)
    variant_hidden_fields = _active_variant_hidden_fields(result)
    task_score_hidden_fields = []
    if result.show_task_scores:
        task_score_hidden_fields.append(("task_scores", "1"))
    if result.show_task_z_scores:
        task_score_hidden_fields.append(("task_z_scores", "1"))
    else:
        task_score_hidden_fields.append(("task_z_scores", "0"))
    if result.show_task_ranks:
        task_score_hidden_fields.append(("task_ranks", "1"))
    column_hidden_html = _hidden_inputs(state_fields + sticky_filter_fields + variant_hidden_fields)
    variant_hidden_html = _hidden_inputs(state_fields + sticky_filter_fields + task_score_hidden_fields)
    filter_hidden_fields = [
        *state_fields,
        ("filters", "1"),
        *variant_hidden_fields,
        *task_score_hidden_fields,
    ]
    filter_hidden_html = _hidden_inputs(filter_hidden_fields)
    dim_options = filter_context.dim_options
    quant_options = filter_context.quant_options
    dtype_options = filter_context.dtype_options
    attn_options = filter_context.attn_options
    prompt_options = filter_context.prompt_options
    model_type_options = filter_context.model_type_options
    language_options = [(option.code, f"{option.label} ({option.task_count})") for option in result.available_languages]
    selected_dims = filter_context.selected_dims
    selected_quants = filter_context.selected_quants
    selected_dtypes = filter_context.selected_dtypes
    selected_attn = filter_context.selected_attn
    selected_prompts = filter_context.selected_prompts
    selected_model_types = filter_context.selected_model_types
    dim_all_query = state_payload(
        result=result,
        sort=sort,
        direction=direction,
        filter_state=FilterState(
            model_filter=filter_state.model_filter,
            task_filter=filter_state.task_filter,
            language_filters=filter_state.language_filters,
            filters_active=True,
            dim_filters=tuple(value for value, _ in dim_options),
            quant_filters=tuple(filter_context.ordered_selected_quants()),
            model_type_filters=tuple(filter_context.ordered_selected_model_types()),
            dtype_filters=tuple(filter_context.ordered_selected_dtypes()),
            attn_filters=tuple(filter_context.ordered_selected_attn()),
            prompt_filters=tuple(filter_context.ordered_selected_prompts()),
            **_task_length_filter_kwargs(filter_state),
        ),
    )
    dim_none_query = state_payload(
        result=result,
        sort=sort,
        direction=direction,
        filter_state=FilterState(
            model_filter=filter_state.model_filter,
            task_filter=filter_state.task_filter,
            language_filters=filter_state.language_filters,
            filters_active=True,
            dim_filters=(FILTER_NONE_VALUE,),
            quant_filters=tuple(filter_context.ordered_selected_quants()),
            model_type_filters=tuple(filter_context.ordered_selected_model_types()),
            dtype_filters=tuple(filter_context.ordered_selected_dtypes()),
            attn_filters=tuple(filter_context.ordered_selected_attn()),
            prompt_filters=tuple(filter_context.ordered_selected_prompts()),
            **_task_length_filter_kwargs(filter_state),
        ),
    )
    quant_all_query = state_payload(
        result=result,
        sort=sort,
        direction=direction,
        filter_state=FilterState(
            model_filter=filter_state.model_filter,
            task_filter=filter_state.task_filter,
            language_filters=filter_state.language_filters,
            filters_active=True,
            dim_filters=tuple(filter_context.ordered_selected_dims()),
            quant_filters=tuple(value for value, _ in quant_options),
            model_type_filters=tuple(filter_context.ordered_selected_model_types()),
            dtype_filters=tuple(filter_context.ordered_selected_dtypes()),
            attn_filters=tuple(filter_context.ordered_selected_attn()),
            prompt_filters=tuple(filter_context.ordered_selected_prompts()),
            **_task_length_filter_kwargs(filter_state),
        ),
    )
    quant_none_query = state_payload(
        result=result,
        sort=sort,
        direction=direction,
        filter_state=FilterState(
            model_filter=filter_state.model_filter,
            task_filter=filter_state.task_filter,
            language_filters=filter_state.language_filters,
            filters_active=True,
            dim_filters=tuple(filter_context.ordered_selected_dims()),
            quant_filters=(FILTER_NONE_VALUE,),
            model_type_filters=tuple(filter_context.ordered_selected_model_types()),
            dtype_filters=tuple(filter_context.ordered_selected_dtypes()),
            attn_filters=tuple(filter_context.ordered_selected_attn()),
            prompt_filters=tuple(filter_context.ordered_selected_prompts()),
            **_task_length_filter_kwargs(filter_state),
        ),
    )
    dtype_all_query = state_payload(
        result=result,
        sort=sort,
        direction=direction,
        filter_state=FilterState(
            model_filter=filter_state.model_filter,
            task_filter=filter_state.task_filter,
            language_filters=filter_state.language_filters,
            filters_active=True,
            dim_filters=tuple(filter_context.ordered_selected_dims()),
            quant_filters=tuple(filter_context.ordered_selected_quants()),
            model_type_filters=tuple(filter_context.ordered_selected_model_types()),
            dtype_filters=tuple(value for value, _ in dtype_options),
            attn_filters=tuple(filter_context.ordered_selected_attn()),
            prompt_filters=tuple(filter_context.ordered_selected_prompts()),
            **_task_length_filter_kwargs(filter_state),
        ),
    )
    dtype_none_query = state_payload(
        result=result,
        sort=sort,
        direction=direction,
        filter_state=FilterState(
            model_filter=filter_state.model_filter,
            task_filter=filter_state.task_filter,
            language_filters=filter_state.language_filters,
            filters_active=True,
            dim_filters=tuple(filter_context.ordered_selected_dims()),
            quant_filters=tuple(filter_context.ordered_selected_quants()),
            model_type_filters=tuple(filter_context.ordered_selected_model_types()),
            dtype_filters=(FILTER_NONE_VALUE,),
            attn_filters=tuple(filter_context.ordered_selected_attn()),
            prompt_filters=tuple(filter_context.ordered_selected_prompts()),
            **_task_length_filter_kwargs(filter_state),
        ),
    )
    attn_all_query = state_payload(
        result=result,
        sort=sort,
        direction=direction,
        filter_state=FilterState(
            model_filter=filter_state.model_filter,
            task_filter=filter_state.task_filter,
            language_filters=filter_state.language_filters,
            filters_active=True,
            dim_filters=tuple(filter_context.ordered_selected_dims()),
            quant_filters=tuple(filter_context.ordered_selected_quants()),
            model_type_filters=tuple(filter_context.ordered_selected_model_types()),
            dtype_filters=tuple(filter_context.ordered_selected_dtypes()),
            attn_filters=tuple(value for value, _ in attn_options),
            prompt_filters=tuple(filter_context.ordered_selected_prompts()),
            **_task_length_filter_kwargs(filter_state),
        ),
    )
    attn_none_query = state_payload(
        result=result,
        sort=sort,
        direction=direction,
        filter_state=FilterState(
            model_filter=filter_state.model_filter,
            task_filter=filter_state.task_filter,
            language_filters=filter_state.language_filters,
            filters_active=True,
            dim_filters=tuple(filter_context.ordered_selected_dims()),
            quant_filters=tuple(filter_context.ordered_selected_quants()),
            model_type_filters=tuple(filter_context.ordered_selected_model_types()),
            dtype_filters=tuple(filter_context.ordered_selected_dtypes()),
            attn_filters=(FILTER_NONE_VALUE,),
            prompt_filters=tuple(filter_context.ordered_selected_prompts()),
            **_task_length_filter_kwargs(filter_state),
        ),
    )
    prompt_all_query = state_payload(
        result=result,
        sort=sort,
        direction=direction,
        filter_state=FilterState(
            model_filter=filter_state.model_filter,
            task_filter=filter_state.task_filter,
            language_filters=filter_state.language_filters,
            filters_active=True,
            dim_filters=tuple(filter_context.ordered_selected_dims()),
            quant_filters=tuple(filter_context.ordered_selected_quants()),
            model_type_filters=tuple(filter_context.ordered_selected_model_types()),
            dtype_filters=tuple(filter_context.ordered_selected_dtypes()),
            attn_filters=tuple(filter_context.ordered_selected_attn()),
            prompt_filters=tuple(value for value, _ in prompt_options),
            **_task_length_filter_kwargs(filter_state),
        ),
    )
    prompt_none_query = state_payload(
        result=result,
        sort=sort,
        direction=direction,
        filter_state=FilterState(
            model_filter=filter_state.model_filter,
            task_filter=filter_state.task_filter,
            language_filters=filter_state.language_filters,
            filters_active=True,
            dim_filters=tuple(filter_context.ordered_selected_dims()),
            quant_filters=tuple(filter_context.ordered_selected_quants()),
            model_type_filters=tuple(filter_context.ordered_selected_model_types()),
            dtype_filters=tuple(filter_context.ordered_selected_dtypes()),
            attn_filters=tuple(filter_context.ordered_selected_attn()),
            prompt_filters=(FILTER_NONE_VALUE,),
            **_task_length_filter_kwargs(filter_state),
        ),
    )
    language_all_query = state_payload(
        result=result,
        sort=sort,
        direction=direction,
        filter_state=FilterState(
            model_filter=filter_state.model_filter,
            task_filter=filter_state.task_filter,
            filters_active=filter_state.filters_active,
            dim_filters=filter_state.dim_filters,
            quant_filters=filter_state.quant_filters,
            model_type_filters=filter_state.model_type_filters,
            dtype_filters=filter_state.dtype_filters,
            attn_filters=filter_state.attn_filters,
            prompt_filters=filter_state.prompt_filters,
            **_task_length_filter_kwargs(filter_state),
        ),
    )
    language_none_query = state_payload(
        result=result,
        sort=sort,
        direction=direction,
        filter_state=FilterState(
            model_filter=filter_state.model_filter,
            task_filter=filter_state.task_filter,
            filters_active=filter_state.filters_active,
            dim_filters=filter_state.dim_filters,
            quant_filters=filter_state.quant_filters,
            model_type_filters=filter_state.model_type_filters,
            dtype_filters=filter_state.dtype_filters,
            attn_filters=filter_state.attn_filters,
            prompt_filters=filter_state.prompt_filters,
            **_task_length_filter_kwargs(filter_state),
        ),
    )
    language_filter_html = (
        _render_filter_details(
            name="lang_filter",
            summary=f"Languages ({len(result.available_languages)})",
            icon="languages",
            options=language_options,
            selected_values=set(result.selected_languages),
            all_query=language_all_query,
            none_query=language_none_query,
            grid_class="grid max-h-72 min-w-[28rem] grid-cols-3 gap-x-2 gap-y-1 overflow-auto sm:grid-cols-5",
        )
        if language_options
        else ""
    )
    return f"""
    <div class="mb-4 text-[0.8125rem] text-zinc-700">
      <form id="column-controls" class="flex flex-wrap items-center gap-x-5 gap-y-2"
            hx-get="/leaderboard" hx-push-url="true"
            {_leaderboard_control_hx_attrs()}
            hx-trigger="change, submit">
        {column_hidden_html}
        {_control_label(icon="table-properties", text="Columns:")}
        <label class="inline-flex items-center gap-2">
          <input type="checkbox" name="task_scores" value="1" class="h-4 w-4 accent-cyan-700"{task_scores_checked}>
          <span>Tasks</span>
        </label>
        {_control_label(icon="eye", text="Display:")}
        <label class="inline-flex items-center gap-2">
          <input type="hidden" name="task_z_scores" value="0">
          <input type="checkbox" name="task_z_scores" value="1" class="h-4 w-4 accent-cyan-700"{task_z_scores_checked}>
          <span>STD</span>
        </label>
        <label class="inline-flex items-center gap-2">
          <input type="hidden" name="task_ranks" value="0">
          <input type="checkbox" name="task_ranks" value="1" class="h-4 w-4 accent-cyan-700"{task_ranks_checked}>
          <span>Task Rank</span>
        </label>
      </form>
      <form id="variant-controls" class="mt-2 flex flex-wrap items-center gap-x-5 gap-y-2"
            hx-get="/leaderboard" hx-push-url="true"
            {_leaderboard_control_hx_attrs()}
            hx-trigger="change, submit">
        {variant_hidden_html}
        {_control_label(icon="git-branch", text="Include variants:")}
        <label class="inline-flex items-center gap-2">
          <input type="checkbox" name="quantization" value="1" class="h-4 w-4 accent-cyan-700"{quantization_checked}>
          <span>Quantization</span>
        </label>
        <label class="inline-flex items-center gap-2">
          <input type="checkbox" name="truncate" value="1" class="h-4 w-4 accent-cyan-700"{truncate_checked}>
          <span>Truncate dims</span>
        </label>
        <label class="inline-flex items-center gap-2">
          <input type="checkbox" name="rescore" value="1" class="h-4 w-4 accent-cyan-700"{rescore_checked}>
          <span>Rescore</span>
        </label>
        <label class="inline-flex items-center gap-2">
          <input type="checkbox" name="other_variant" value="1" class="h-4 w-4 accent-cyan-700"{other_variant_checked}>
          <span>Other variants</span>
        </label>
      </form>
      <div class="mt-3 flex flex-wrap items-start gap-3">
        <p class="pt-1">{_control_label(icon="filter", text="Filters:")}</p>
        <form id="filter-controls" class="flex flex-wrap items-start gap-3"
              hx-get="/leaderboard" hx-push-url="true"
              {_leaderboard_control_hx_attrs()}
              hx-trigger="change, submit">
          {filter_hidden_html}
        {_render_model_type_controls(
            options=model_type_options,
            selected_values=selected_model_types,
        )}
        <label class="flex min-w-64 items-center gap-2">
          <span class="shrink-0 whitespace-nowrap font-medium text-zinc-800">Model</span>
          {_render_help_tooltip("Filter by model name. Separate multiple names with spaces. Partial matches are supported.")}
          <input id="model-filter-input" type="search" name="model_filter" value="{escape(filter_state.model_filter)}"
                 class="w-72 max-w-full border border-zinc-300 bg-white px-2 py-1 text-[0.8125rem] text-zinc-900 outline-none focus:border-cyan-700"
                 autocomplete="off">
        </label>
        <label class="flex min-w-64 items-center gap-2">
          <span class="shrink-0 whitespace-nowrap font-medium text-zinc-800">Task</span>
          {_render_help_tooltip("Filter by task name. Separate multiple names with spaces. Partial matches are supported.")}
          <input id="task-filter-input" type="search" name="task_filter" value="{escape(filter_state.task_filter)}"
                 class="w-72 max-w-full border border-zinc-300 bg-white px-2 py-1 text-[0.8125rem] text-zinc-900 outline-none focus:border-cyan-700"
                 autocomplete="off">
        </label>
        <label class="inline-flex items-center gap-2 pt-1">
          <input type="checkbox" name="rank_filtered" value="1" class="h-4 w-4 accent-cyan-700"{rank_filtered_checked}>
          <span class="whitespace-nowrap font-medium text-zinc-800">Recalculate Borda, Mean</span>
          {_render_help_tooltip("When enabled, Model, Task, and active facet filters narrow the ranking population before Borda and Mean are recomputed. With a Task filter, Borda is computed from per-task ranks over the filtered tasks.")}
        </label>
        <button type="submit" class="border border-zinc-300 bg-zinc-50 px-2 py-0.5 text-[0.8125rem] font-medium text-zinc-800 hover:border-cyan-600 hover:text-cyan-700">
          Apply
        </button>
          <div id="facet-filters" class="flex flex-wrap items-start gap-3">
            {_render_task_length_filter_inputs(filter_state)}
            {language_filter_html}
            {_render_filter_details(name="dim_filter", summary="Dims", icon="ruler", options=dim_options, selected_values=selected_dims, all_query=dim_all_query, none_query=dim_none_query)}
            {_render_filter_details(name="quant_filter", summary="Quantization", icon="binary", options=quant_options, selected_values=selected_quants, all_query=quant_all_query, none_query=quant_none_query)}
            <div class="flex flex-wrap items-start gap-3 border-l border-zinc-200 pl-3">
              <p class="pt-1">{_control_label(icon="cpu", text="Runtime")}</p>
              {_render_filter_details(name="dtype_filter", summary="Dtype", icon="braces", options=dtype_options, selected_values=selected_dtypes, all_query=dtype_all_query, none_query=dtype_none_query)}
              {_render_filter_details(name="attn_filter", summary="Attention", icon="activity", options=attn_options, selected_values=selected_attn, all_query=attn_all_query, none_query=attn_none_query)}
              {_render_filter_details(name="prompt_filter", summary="Prompt", icon="table-properties", options=prompt_options, selected_values=selected_prompts, all_query=prompt_all_query, none_query=prompt_none_query)}
            </div>
          </div>
        </form>
      </div>
    </div>
    """


def _active_variant_hidden_fields(result: LeaderboardResult) -> list[tuple[str, str]]:
    fields = []
    if result.include_quantization_variants:
        fields.append(("quantization", "1"))
    if result.include_truncate_variants:
        fields.append(("truncate", "1"))
    if result.include_rescore_variants:
        fields.append(("rescore", "1"))
    if result.include_other_variants:
        fields.append(("other_variant", "1"))
    return fields


def _text_filter_hidden_fields(filter_state: FilterState) -> list[tuple[str, str]]:
    fields = []
    if filter_state.model_filter:
        fields.append(("model_filter", filter_state.model_filter))
    if filter_state.task_filter:
        fields.append(("task_filter", filter_state.task_filter))
    if filter_state.rank_filtered:
        fields.append(("rank_filtered", "1"))
    return fields


def _render_model_type_controls(
    *,
    options: list[tuple[str, str]],
    selected_values: set[str],
) -> str:
    if not options:
        return ""
    checkboxes = []
    for value, label in options:
        checked = " checked" if value in selected_values else ""
        checkboxes.append(
            f"""<label class="inline-flex items-center gap-1.5">
              <input type="checkbox" name="model_type_filter" value="{escape(value)}" class="h-4 w-4 accent-cyan-700"{checked}>
              <span>{escape(label)}</span>
            </label>"""
        )
    return f"""
      <fieldset id="model-type-controls" class="flex flex-wrap items-center gap-x-4 gap-y-2">
        <input type="hidden" name="model_type_filter" value="{FILTER_NONE_VALUE}">
        {_control_label(icon="cpu", text="Model type:")}
        {''.join(checkboxes)}
      </fieldset>
    """


def _render_task_length_filter_inputs(filter_state: FilterState) -> str:
    input_class = (
        "w-24 border border-zinc-300 bg-white px-2 py-1 text-[0.8125rem] text-zinc-900 outline-none "
        "focus:border-cyan-700"
    )
    active_classes = "border-cyan-700 bg-cyan-50" if filter_state.has_task_length_filters else "border-zinc-200 bg-zinc-50"
    tooltip = (
        "Filters tasks by average query and document string length in characters. "
        "Tasks missing length metadata are excluded when a bound is set."
    )
    return f"""
    <fieldset class="flex flex-wrap items-center gap-2 border {active_classes} px-1.5 py-1">
      <legend class="inline-flex items-center gap-1 px-1 text-xs font-semibold uppercase text-zinc-500">
        <span>Task string length</span>
        {_render_help_tooltip(tooltip)}
      </legend>
      <label class="inline-flex items-center gap-1">
        <span class="text-xs font-medium text-zinc-700">Query string >=</span>
        <input type="number" min="0" step="any" name="query_len_min" value="{escape(filter_state.query_len_min)}"
               class="{input_class}">
      </label>
      <label class="inline-flex items-center gap-1">
        <span class="text-xs font-medium text-zinc-700">Query string <=</span>
        <input type="number" min="0" step="any" name="query_len_max" value="{escape(filter_state.query_len_max)}"
               class="{input_class}">
      </label>
      <label class="inline-flex items-center gap-1">
        <span class="text-xs font-medium text-zinc-700">Doc string >=</span>
        <input type="number" min="0" step="any" name="doc_len_min" value="{escape(filter_state.doc_len_min)}"
               class="{input_class}">
      </label>
      <label class="inline-flex items-center gap-1">
        <span class="text-xs font-medium text-zinc-700">Doc string <=</span>
        <input type="number" min="0" step="any" name="doc_len_max" value="{escape(filter_state.doc_len_max)}"
               class="{input_class}">
      </label>
    </fieldset>
    """


def render_score_groups(*, result: LeaderboardResult, sort: str, direction: str, filter_state: FilterState | None = None) -> str:
    filter_state = filter_state or FilterState()
    if len(result.score_groups) <= 1 or result.selected_score_group is None:
        return ""
    buttons: list[str] = []
    for score_group in result.score_groups:
        active = score_group.name == result.selected_score_group.name
        classes = (
            "border-zinc-900 bg-zinc-900 text-white"
            if active
            else "border-zinc-300 bg-white text-zinc-700 hover:border-cyan-500 hover:text-cyan-700"
        )
        query_payload = state_payload(result=result, sort="borda_rank", direction="asc", filter_state=filter_state)
        query_payload["group"] = score_group.name
        query = urlencode(query_payload, doseq=True)
        page_url = _page_url(query_payload)
        buttons.append(
            f"""<button type="button" class="border px-2 py-1 text-[0.8125rem] {classes}"
                  hx-get="{_leaderboard_url(query)}" hx-push-url="{page_url}"
                  {_leaderboard_control_hx_attrs()}>
                  {escape(score_group.label)}
                </button>"""
        )
    return f"""<nav class="mb-4 flex flex-wrap gap-2" aria-label="Score groups">{''.join(buttons)}</nav>"""


def render_table_head(
    *,
    result: LeaderboardResult,
    sort: str,
    direction: str,
    filter_state: FilterState | None = None,
    benchmark_docs: BenchmarkDocs | None = None,
) -> str:
    filter_state = filter_state or FilterState()
    metric_labels = _metric_column_labels(result.metric_columns, overrides=result.metric_column_labels)
    columns = [
        ("model_name", "Model Name", "asc", "left", False, ""),
        ("borda_rank", "Borda", "asc", "right", False, ""),
        ("mean_rank", "Mean", "asc", "right", False, ""),
        ("borda_score", "Borda Score", "desc", "right", False, ""),
    ]
    if result.is_overall and not (result.rank_filtered and result.task_filter):
        columns.extend(
            [
                ("macro_mean", "Macro Mean", "desc", "right", False, ""),
                ("micro_mean", "Micro Mean", "desc", "right", False, ""),
            ]
        )
    else:
        columns.append(("mean_score", "Mean Score", "desc", "right", False, ""))
    columns.extend(
        (f"metric:{column}", metric_labels[column], "asc" if result.show_task_ranks else "desc", "right", True, column)
        for column in result.metric_columns
    )
    columns.extend(
        [
            ("task_count", "Tasks", "desc", "right", False, ""),
            ("active_parameters", "Active Params", "asc", "right", False, ""),
            ("total_parameters", "Total Params", "asc", "right", False, ""),
            ("max_seq_length", "Max Len", "desc", "right", False, ""),
            ("embedding_dim", "Dims", "desc", "right", False, ""),
        ]
    )
    if result.include_quantization_variants:
        columns.append(("quantization", "Quantization", "asc", "left", False, ""))
    if _show_base_delta_column(result):
        columns.append(("base_score_delta_percent", "Δ vs Base", "desc", "right", False, ""))
    heads = []
    for key, label, default_direction, align, is_metric, full_metric_name in columns:
        align = "left"
        next_direction = _next_direction(key=key, sort=sort, direction=direction, default_direction=default_direction)
        indicator = " ▲" if sort == key and direction == "asc" else " ▼" if sort == key else ""
        query_payload = state_payload(result=result, sort=key, direction=next_direction, filter_state=filter_state)
        query = urlencode(query_payload, doseq=True)
        justify = "justify-end" if align == "right" else "justify-start"
        text_align = "text-right" if align == "right" else "text-left"
        th_spacing = "w-[4.75rem] min-w-[4.75rem] max-w-[4.75rem] px-1 normal-case" if is_metric else "px-2 uppercase"
        sticky = _sticky_head_class(key)
        label_class = "min-w-0 text-left leading-tight [overflow-wrap:anywhere]" if is_metric else "text-left"
        label_attrs = (
            f' data-metric-column-full-name="{escape(full_metric_name, quote=True)}"' if is_metric else ""
        )
        doc = (
            benchmark_docs.task_doc(view_name=result.view_name, metric_column=full_metric_name)
            if benchmark_docs is not None and is_metric
            else None
        )
        doc_trigger = _render_doc_summary_trigger(doc=doc, label=f"{label} overview") if doc is not None else ""
        header_content = f"""
                 <span class="doc-label-group inline-flex w-full items-center gap-0.5" data-doc-label-group="metric">
                   <button type="button" class="inline-flex w-full min-w-0 flex-1 {justify} text-left hover:text-cyan-700"
                           hx-get="{_leaderboard_url(query)}" hx-push-url="{_page_url(query_payload)}"
                           {_leaderboard_control_hx_attrs()}>
                     <span class="{label_class}"{label_attrs}>{escape(label)}</span><span class="shrink-0 text-zinc-400">{indicator}</span>
                   </button>{doc_trigger}
                 </span>"""
        heads.append(
            f"""<th scope="col" data-column-key="{escape(key, quote=True)}" class="bg-zinc-100 py-1 text-xs font-semibold text-zinc-600 {text_align} {th_spacing} {sticky}">
                 {header_content}
               </th>"""
        )
    return f"<thead><tr>{''.join(heads)}</tr></thead>"


def _sticky_head_class(key: str) -> str:
    if key == "model_name":
        return "leaderboard-col-model sticky z-20"
    if key == "borda_rank":
        return "leaderboard-col-rank"
    if key == "mean_rank":
        return "leaderboard-col-rank"
    return ""


def render_table_body(*, result: LeaderboardResult, filter_context: FilterContext | None = None) -> str:
    if not result.rows:
        return """<tbody><tr><td class="px-3 py-5 text-center text-zinc-500" colspan="12">No complete results found.</td></tr></tbody>"""
    filter_context = filter_context or row_filter_context(result.rows, FilterState())
    body_rows = []
    model_views = model_cell_views(result.rows)
    for row in result.rows:
        hidden = not filter_context.is_visible(row)
        row_class = "leaderboard-row border-t border-zinc-200 odd:bg-white even:bg-zinc-50"
        hidden_attrs = ' hidden data-filter-hidden="true"' if hidden else ""
        mean_cells = _render_mean_cells(result=result, row=row)
        body_rows.append(
            f"""<tr class="{row_class}"{hidden_attrs}>
              {render_model_name_cell(row, model_views[row.model_name])}
              <td class="leaderboard-col-rank px-2 py-1 text-left tabular-nums">{_fmt_rank(row.borda_rank)}</td>
              <td class="leaderboard-col-rank px-2 py-1 text-left tabular-nums">{_fmt_rank(row.mean_rank)}</td>
              <td class="px-2 py-1 text-left tabular-nums">{_fmt_score(row.borda_score)}</td>
              {mean_cells}
              {_render_metric_cells(result=result, row=row)}
              <td class="px-2 py-1 text-left tabular-nums">{row.task_count}</td>
              <td class="px-2 py-1 text-left tabular-nums">{_fmt_params(row.active_parameters)}</td>
              <td class="px-2 py-1 text-left tabular-nums">{_fmt_params(row.total_parameters)}</td>
              <td class="px-2 py-1 text-left tabular-nums">{_fmt_max_len(row.max_seq_length)}</td>
              <td class="px-2 py-1 text-left tabular-nums">{_fmt_row_embedding_dim(row)}</td>
              {_render_quantization_cell(result=result, row=row)}
              {_render_base_delta_cell(result=result, row=row)}
            </tr>"""
        )
    return f"<tbody>{''.join(body_rows)}</tbody>"


def render_leaderboard_csv(*, result: LeaderboardResult, filter_state: FilterState | None = None) -> str:
    filter_context = row_filter_context(result.rows, filter_state or FilterState())
    visible_rows = [row for row in result.rows if filter_context.is_visible(row)]
    model_views = model_cell_views(result.rows)
    metric_labels = _metric_column_labels(result.metric_columns, overrides=result.metric_column_labels)
    metric_headers = _csv_metric_headers(result=result, metric_labels=metric_labels)
    output = StringIO()
    writer = csv.writer(output, lineterminator="\n")
    headers = _csv_headers(result=result, metric_headers=metric_headers)
    writer.writerow(headers)
    for row in visible_rows:
        model_view = model_views[row.model_name]
        record = _csv_record_for_row(result=result, row=row, model_view=model_view, metric_headers=metric_headers)
        writer.writerow([_csv_cell(record.get(header)) for header in headers])
    return output.getvalue()


def _csv_headers(*, result: LeaderboardResult, metric_headers: dict[str, str]) -> list[str]:
    headers = [
        "Borda Rank",
        "Mean Rank",
        "Model Name",
        "Borda Score",
    ]
    if result.is_overall and not (result.rank_filtered and result.task_filter):
        headers.extend(["Macro Mean", "Micro Mean"])
    else:
        headers.append("Mean Score")
    headers.extend(metric_headers[column] for column in result.metric_columns)
    headers.extend(
        [
            "Task Count",
            "Full Model Name",
            "Ranking Model Name",
            "Source Model Name",
            "Model Type",
            "Model Type Key",
            "Active Params",
            "Total Params",
            "Max Sequence Length",
            "Embedding Dims",
            "Original Embedding Dims",
            "Truncated Embedding Dims",
            "Quantization",
            "Embedding Variant",
            "Base Score Delta Percent",
            "DType",
            "Attention Implementation",
            "Prompt",
            "Trust Remote Code",
        ]
    )
    return headers


def _csv_metric_headers(*, result: LeaderboardResult, metric_labels: dict[str, str]) -> dict[str, str]:
    existing = {
        "Borda Rank",
        "Mean Rank",
        "Model Name",
        "Borda Score",
        "Macro Mean",
        "Micro Mean",
        "Mean Score",
        "Task Count",
        "Full Model Name",
        "Ranking Model Name",
        "Source Model Name",
        "Model Type",
        "Model Type Key",
        "Active Params",
        "Total Params",
        "Max Sequence Length",
        "Embedding Dims",
        "Original Embedding Dims",
        "Truncated Embedding Dims",
        "Quantization",
        "Embedding Variant",
        "Base Score Delta Percent",
        "DType",
        "Attention Implementation",
        "Prompt",
        "Trust Remote Code",
    }
    headers: dict[str, str] = {}
    for column in result.metric_columns:
        header = metric_labels[column]
        if header not in existing:
            headers[column] = header
            existing.add(header)
            continue
        index = 2
        while f"{header} ({index})" in existing:
            index += 1
        headers[column] = f"{header} ({index})"
        existing.add(headers[column])
    return headers


def _csv_filename(*, view: str, target: str) -> str:
    slug = "".join(char if char.isalnum() or char in {"-", "_"} else "_" for char in view).strip("_") or "leaderboard"
    target_slug = "".join(char if char.isalnum() or char in {"-", "_"} else "_" for char in target).strip("_") or "all"
    return f"hakari_bench_{slug}_{target_slug}.csv"


def _csv_record_for_row(
    *,
    result: LeaderboardResult,
    row: LeaderboardRow,
    model_view: object,
    metric_headers: dict[str, str],
) -> dict[str, object | None]:
    metadata = getattr(model_view, "metadata")
    record: dict[str, object | None] = {
        "Borda Rank": row.borda_rank,
        "Mean Rank": row.mean_rank,
        "Model Name": getattr(model_view, "display_name"),
        "Borda Score": row.borda_score,
        "Task Count": row.task_count,
        "Full Model Name": metadata.get("model_name"),
        "Ranking Model Name": metadata.get("ranking_model_name"),
        "Source Model Name": metadata.get("source_model_name"),
        "Model Type": metadata.get("model_type"),
        "Model Type Key": metadata.get("model_type_key"),
        "Active Params": metadata.get("active_parameters"),
        "Total Params": metadata.get("total_parameters"),
        "Max Sequence Length": metadata.get("max_seq_length"),
        "Embedding Dims": metadata.get("embedding_dim"),
        "Original Embedding Dims": metadata.get("original_embedding_dim"),
        "Truncated Embedding Dims": metadata.get("truncated_embedding_dim"),
        "Quantization": metadata.get("quantization"),
        "Embedding Variant": metadata.get("embedding_variant_name"),
        "Base Score Delta Percent": metadata.get("base_score_delta_percent"),
        "DType": metadata.get("dtype"),
        "Attention Implementation": metadata.get("attention"),
        "Prompt": metadata.get("prompt"),
        "Trust Remote Code": metadata.get("trust_remote_code"),
    }
    if result.is_overall and not (result.rank_filtered and result.task_filter):
        record["Macro Mean"] = row.macro_mean
        record["Micro Mean"] = row.micro_mean
    else:
        record["Mean Score"] = row.mean_score
    for column in result.metric_columns:
        record[metric_headers[column]] = row.metric_values.get(column)
    return record


def _csv_cell(value: object | None) -> str:
    if value is None:
        return ""
    if isinstance(value, bool):
        return "true" if value else "false"
    if isinstance(value, float):
        if not math.isfinite(value):
            return ""
        return f"{value:.6f}".rstrip("0").rstrip(".")
    text = str(value)
    if text.startswith(("=", "+", "-", "@")):
        return "'" + text
    return text


def render_variant_panel(
    *,
    view_label: str,
    rows,
    include_rescore: bool = False,
    include_truncate: bool = False,
    view_name: str | None = None,
) -> str:
    rescore_toggle = _variant_analysis_toggle(
        view_name=view_name,
        label_enabled="Hide rescore",
        label_disabled="Include rescore",
        flag_name="include_rescore",
        flag_value=include_rescore,
        other_flags={"include_truncate": include_truncate},
    )
    truncate_toggle = _variant_analysis_toggle(
        view_name=view_name,
        label_enabled="Hide truncate_dim",
        label_disabled="Include truncate_dim",
        flag_name="include_truncate",
        flag_value=include_truncate,
        other_flags={"include_rescore": include_rescore},
    )
    if not rows:
        body = """<tr><td class="px-3 py-5 text-center text-zinc-500" colspan="7">No embedding variant rows are available for this view.</td></tr>"""
    else:
        body = "".join(
            f"""
            <tr class="border-t border-zinc-200 odd:bg-white even:bg-zinc-50">
              <td class="px-3 py-2 font-medium">{escape(row.model_name)}</td>
              <td class="px-3 py-2">{escape(row.variant_name)}</td>
              <td class="px-3 py-2 text-right tabular-nums">{_fmt_embedding_dim(row.embedding_dim)}</td>
              <td class="px-3 py-2">{escape(row.quantization or "original")}</td>
              <td class="px-3 py-2 text-right tabular-nums">{row.task_count:,}</td>
              <td class="px-3 py-2 text-right tabular-nums">{_fmt_score(row.mean_score_100)}</td>
              <td class="px-3 py-2 text-right tabular-nums">{_fmt_percent_delta(row.base_delta_percent)}</td>
            </tr>
            """
            for row in rows
        )
    return f"""
    <div class="px-3 py-3">
      <div class="mb-3 flex flex-wrap items-end justify-between gap-2">
        <div>
          <h3 class="text-base font-semibold">Variant impact</h3>
          <p class="text-sm text-zinc-600">{escape(view_label)}: base-relative score changes for embedding variants. Rescore and truncate_dim variants are hidden by default.</p>
        </div>
        <div class="flex flex-wrap items-center gap-2">
          {rescore_toggle}
          {truncate_toggle}
          <p class="text-xs text-zinc-500">{len(rows):,} variant groups</p>
        </div>
      </div>
      <div class="max-h-80 overflow-auto border border-zinc-200">
        <table class="min-w-full text-sm">
          <thead>
            <tr class="bg-zinc-100 text-xs font-semibold uppercase text-zinc-600">
              <th class="px-3 py-2 text-left">Model</th>
              <th class="px-3 py-2 text-left">Variant</th>
              <th class="px-3 py-2 text-right">Dims</th>
              <th class="px-3 py-2 text-left">Quantization</th>
              <th class="px-3 py-2 text-right">Tasks</th>
              <th class="px-3 py-2 text-right">Mean score</th>
              <th class="px-3 py-2 text-right">Delta vs base</th>
            </tr>
          </thead>
          <tbody>{body}</tbody>
        </table>
      </div>
    </div>
    """


def _variant_analysis_toggle(
    *,
    view_name: str | None,
    label_enabled: str,
    label_disabled: str,
    flag_name: str,
    flag_value: bool,
    other_flags: dict[str, bool],
) -> str:
    if view_name is None:
        return ""
    query_payload = {
        "panel": "variants",
        "view": view_name,
        flag_name: "0" if flag_value else "1",
    }
    query_payload.update({name: "1" for name, value in other_flags.items() if value})
    toggle_query = urlencode(query_payload)
    toggle_label = label_enabled if flag_value else label_disabled
    toggle_classes = (
        "border-cyan-700 bg-cyan-50 text-cyan-900"
        if flag_value
        else "border-zinc-300 bg-white text-zinc-700 hover:border-cyan-600 hover:text-cyan-700"
    )
    return f"""
    <button type="button" class="border px-2 py-1 text-[0.8125rem] {toggle_classes}"
            hx-get="/analysis?{escape(toggle_query, quote=True)}"
            hx-target="#analysis-panel" hx-swap="innerHTML">{escape(toggle_label)}</button>
    """


def render_reranking_panel(*, view_label: str, rows) -> str:
    if not rows:
        return _empty_analysis_panel(
            title="Reranking diagnostics",
            body="No reranking diagnostic rows are available for this view.",
        )
    body = "".join(
        f"""
        <tr class="border-t border-zinc-200 odd:bg-white even:bg-zinc-50">
          <td class="px-3 py-2 font-medium">{escape(row.benchmark)}</td>
          <td class="px-3 py-2 text-right tabular-nums">{row.task_count:,}</td>
          <td class="px-3 py-2 text-right tabular-nums">{_fmt_percent(row.query_coverage_percent)}</td>
          <td class="px-3 py-2 text-right tabular-nums">{_fmt_percent(row.relevant_coverage_percent)}</td>
          <td class="px-3 py-2 text-right tabular-nums">{_fmt_signed_points(row.mean_lift_points)}</td>
          <td class="px-3 py-2 text-right tabular-nums">{_fmt_max_len(row.rerank_top_k)}</td>
          <td class="px-3 py-2">{escape(row.candidate_source or "")}</td>
          <td class="px-3 py-2">{escape(row.candidate_ranking or "")}</td>
          <td class="px-3 py-2">{escape(row.bm25_source or "")}</td>
        </tr>
        """
        for row in rows
    )
    return f"""
    <div class="px-3 py-3">
      <div class="mb-3 flex flex-wrap items-end justify-between gap-2">
        <div>
          <h3 class="text-base font-semibold">Reranking diagnostics</h3>
          <p class="text-sm text-zinc-600">{escape(view_label)}: candidate coverage and second-stage rerank lift.</p>
        </div>
        <p class="text-xs text-zinc-500">{len(rows):,} benchmark rows</p>
      </div>
      <div class="max-h-80 overflow-auto border border-zinc-200">
        <table class="min-w-full text-sm">
          <thead>
            <tr class="bg-zinc-100 text-xs font-semibold uppercase text-zinc-600">
              <th class="px-3 py-2 text-left">Benchmark</th>
              <th class="px-3 py-2 text-right">Tasks</th>
              <th class="px-3 py-2 text-right">Query coverage</th>
              <th class="px-3 py-2 text-right">Relevant coverage</th>
              <th class="px-3 py-2 text-right">Lift</th>
              <th class="px-3 py-2 text-right">Top K</th>
              <th class="px-3 py-2 text-left">Candidate source</th>
              <th class="px-3 py-2 text-left">Ranking</th>
              <th class="px-3 py-2 text-left">BM25 source</th>
            </tr>
          </thead>
          <tbody>{body}</tbody>
        </table>
      </div>
    </div>
    """


def render_dataset_diagnostics_panel(*, view_label: str, rows) -> str:
    if not rows:
        return _empty_analysis_panel(
            title="Dataset diagnostics",
            body="No dataset metadata rows are available for this view.",
        )
    body = "".join(
        f"""
        <tr class="border-t border-zinc-200 odd:bg-white even:bg-zinc-50">
          <td class="px-3 py-2 font-medium">{escape(row.benchmark)}</td>
          <td class="px-3 py-2 text-right tabular-nums">{row.task_count:,}</td>
          <td class="px-3 py-2 text-right tabular-nums">{row.language_count:,}</td>
          <td class="px-3 py-2 text-right tabular-nums">{row.category_count:,}</td>
          <td class="px-3 py-2 text-right tabular-nums">{row.base_rows:,}</td>
          <td class="px-3 py-2 text-right tabular-nums">{_fmt_percent(row.saturation_percent)}</td>
          <td class="px-3 py-2 text-right tabular-nums">{_fmt_number(row.mean_query_count)}</td>
          <td class="px-3 py-2 text-right tabular-nums">{_fmt_number(row.mean_document_count)}</td>
          <td class="px-3 py-2 text-right tabular-nums">{_fmt_number(row.mean_query_chars)}</td>
          <td class="px-3 py-2 text-right tabular-nums">{_fmt_number(row.mean_document_chars)}</td>
        </tr>
        """
        for row in rows
    )
    return f"""
    <div class="px-3 py-3">
      <div class="mb-3 flex flex-wrap items-end justify-between gap-2">
        <div>
          <h3 class="text-base font-semibold">Dataset diagnostics</h3>
          <p class="text-sm text-zinc-600">{escape(view_label)}: metadata coverage, sample sizes, text lengths, and score saturation.</p>
        </div>
        <p class="text-xs text-zinc-500">{len(rows):,} benchmark rows</p>
      </div>
      <div class="max-h-80 overflow-auto border border-zinc-200">
        <table class="min-w-full text-sm">
          <thead>
            <tr class="bg-zinc-100 text-xs font-semibold uppercase text-zinc-600">
              <th class="px-3 py-2 text-left">Benchmark</th>
              <th class="px-3 py-2 text-right">Tasks</th>
              <th class="px-3 py-2 text-right">Languages</th>
              <th class="px-3 py-2 text-right">Categories</th>
              <th class="px-3 py-2 text-right">Base rows</th>
              <th class="px-3 py-2 text-right">Saturation</th>
              <th class="px-3 py-2 text-right">Queries</th>
              <th class="px-3 py-2 text-right">Docs</th>
              <th class="px-3 py-2 text-right">Query chars</th>
              <th class="px-3 py-2 text-right">Doc chars</th>
            </tr>
          </thead>
          <tbody>{body}</tbody>
        </table>
      </div>
    </div>
    """


def _empty_analysis_panel(*, title: str, body: str) -> str:
    return f"""
    <div class="px-3 py-4">
      <h3 class="text-base font-semibold">{escape(title)}</h3>
      <p class="mt-1 text-sm text-zinc-600">{escape(body)}</p>
    </div>
    """


def _render_metric_cells(*, result: LeaderboardResult, row: LeaderboardRow) -> str:
    if result.show_task_ranks:
        values = row.metric_rank_values
        return "".join(
            f"""<td class="w-[4.75rem] min-w-[4.75rem] max-w-[4.75rem] px-1 py-1 text-left tabular-nums">{_fmt_optional_rank(values.get(column))}</td>"""
            for column in result.metric_columns
        )
    if result.show_task_z_scores:
        return "".join(
            _render_metric_z_cell(score=row.metric_values.get(column), z_score=row.metric_z_values.get(column))
            for column in result.metric_columns
        )
    values = row.metric_values
    return "".join(
        f"""<td class="w-[4.75rem] min-w-[4.75rem] max-w-[4.75rem] px-1 py-1 text-left tabular-nums">{_fmt_score(values.get(column))}</td>"""
        for column in result.metric_columns
    )


def _render_mean_cells(*, result: LeaderboardResult, row: LeaderboardRow) -> str:
    if result.is_overall and not (result.rank_filtered and result.task_filter):
        if result.show_task_z_scores:
            return (
                _render_score_z_cell(score=row.macro_mean, z_score=row.macro_mean_z, cell_class="px-2 py-1 text-left tabular-nums")
                + _render_score_z_cell(score=row.micro_mean, z_score=row.micro_mean_z, cell_class="px-2 py-1 text-left tabular-nums")
            )
        return f"""<td class="px-2 py-1 text-left tabular-nums">{_fmt_score(row.macro_mean)}</td>
                <td class="px-2 py-1 text-left tabular-nums">{_fmt_score(row.micro_mean)}</td>"""
    if result.show_task_z_scores:
        return _render_score_z_cell(score=row.mean_score, z_score=row.mean_score_z, cell_class="px-2 py-1 text-left tabular-nums")
    return f"""<td class="px-2 py-1 text-left tabular-nums">{_fmt_score(row.mean_score)}</td>"""


def _render_metric_z_cell(*, score: float | None, z_score: float | None) -> str:
    return _render_score_z_cell(
        score=score,
        z_score=z_score,
        cell_class="w-[4.75rem] min-w-[4.75rem] max-w-[4.75rem] px-1 py-1 text-left tabular-nums",
    )


def _render_score_z_cell(*, score: float | None, z_score: float | None, cell_class: str) -> str:
    rounded = _rounded_z_score(z_score)
    if rounded is None:
        z_label = ""
        bucket_class = "task-z-neutral"
    else:
        assert z_score is not None
        z_label = f"{_fmt_z_score(z_score)}σ"
        bucket_class = _z_score_bucket_class(rounded)
    return (
        f'<td class="{cell_class}">'
        f'<span class="task-z-score {bucket_class}">'
        f'<span class="task-z-score-value">{escape(_fmt_score(score))}</span>'
        f'<span class="task-z-score-delta">{escape(z_label)}</span>'
        "</span>"
        "</td>"
    )


def _render_base_delta_cell(*, result: LeaderboardResult, row: LeaderboardRow) -> str:
    if not _show_base_delta_column(result):
        return ""
    return f"""<td class="px-2 py-1 text-left tabular-nums">{_fmt_percent_delta(row.base_score_delta_percent)}</td>"""


def _render_quantization_cell(*, result: LeaderboardResult, row: LeaderboardRow) -> str:
    if not result.include_quantization_variants:
        return ""
    return f"""<td class="px-2 py-1 text-left">{escape(row.quantization or "")}</td>"""


def _show_base_delta_column(result: LeaderboardResult) -> bool:
    return result.include_quantization_variants or result.include_truncate_variants


def _render_filter_details(
    *,
    name: str,
    summary: str,
    icon: str,
    options: list[tuple[str, str]],
    selected_values: set[str],
    all_query: QueryState,
    none_query: QueryState,
    grid_class: str = "grid max-h-60 min-w-64 grid-cols-2 gap-x-2 gap-y-1 overflow-auto sm:grid-cols-3",
) -> str:
    checkboxes = []
    for value, label in options:
        checked = " checked" if value in selected_values else ""
        checkboxes.append(
            f"""<label class="flex min-w-0 items-center gap-2 whitespace-nowrap px-1.5 py-0.5">
              <input type="checkbox" name="{escape(name)}" value="{escape(value)}" class="h-4 w-4 accent-cyan-700"{checked}>
              <span>{escape(label)}</span>
            </label>"""
        )
    all_url = _leaderboard_url(urlencode(all_query, doseq=True))
    none_url = _leaderboard_url(urlencode(none_query, doseq=True))
    all_page_url = _page_url(all_query)
    none_page_url = _page_url(none_query)
    return f"""
      <details class="filter-detail border border-zinc-300 bg-white" data-filter-detail="{escape(name, quote=True)}" data-filter-icon="{escape(icon, quote=True)}">
        <summary class="cursor-pointer px-1.5 py-0.5 text-[0.8125rem] font-medium text-zinc-800">
          <span class="inline-flex items-center gap-1.5">
            {_icon_svg(icon, class_name="hakari-icon filter-detail-icon shrink-0")}
            <span>{escape(summary)}</span>
          </span>
        </summary>
        <div class="border-t border-zinc-200 p-2">
          <div class="mb-2 flex gap-1">
            <button type="button" class="border border-zinc-300 bg-zinc-50 px-2 py-0.5 text-xs font-medium text-zinc-700 hover:border-cyan-500 hover:text-cyan-700"
                    hx-get="{all_url}" hx-push-url="{all_page_url}"
                    {_leaderboard_control_hx_attrs()}>All</button>
            <button type="button" class="border border-zinc-300 bg-zinc-50 px-2 py-0.5 text-xs font-medium text-zinc-700 hover:border-cyan-500 hover:text-cyan-700"
                    hx-get="{none_url}" hx-push-url="{none_page_url}"
                    {_leaderboard_control_hx_attrs()}>None</button>
          </div>
          <div class="{escape(grid_class)}">
            {''.join(checkboxes)}
          </div>
        </div>
      </details>
    """


def _hidden_inputs(fields: list[tuple[str, str]]) -> str:
    return "".join(f"""<input type="hidden" name="{escape(name)}" value="{escape(value)}">""" for name, value in fields)


def _next_direction(*, key: str, sort: str, direction: str, default_direction: str) -> str:
    if key != sort:
        return default_direction
    return "desc" if direction == "asc" else "asc"


def _fmt_rank(value: float) -> str:
    return str(int(value)) if float(value).is_integer() else f"{value:.1f}"


def _fmt_optional_rank(value: float | None) -> str:
    return "" if value is None else _fmt_rank(value)


def _fmt_score(value: float | None) -> str:
    return "" if value is None else f"{value:.2f}"


def _rounded_z_score(value: float | None) -> float | None:
    if value is None:
        return None
    sign = -1.0 if value < 0 else 1.0
    rounded = sign * (int(abs(value) * 4.0 + 0.5) / 4.0)
    return max(-2.0, min(2.0, rounded))


def _fmt_z_score(value: float) -> str:
    if abs(value) < 0.005:
        return "0.00"
    return f"{value:+.2f}"


def _z_score_bucket_class(value: float) -> str:
    if value == 0.0:
        return "task-z-neutral"
    prefix = "pos" if value > 0.0 else "neg"
    bucket = int(abs(value) * 100)
    bucket_class = f"task-z-{prefix}-{bucket:03d}"
    return bucket_class if bucket_class in Z_SCORE_BUCKET_CLASSES else "task-z-neutral"


def _fmt_params(value: int | None) -> str:
    if value is None:
        return ""
    if value >= 1_000_000_000:
        return f"{value / 1_000_000_000:.2f}B"
    if value >= 1_000_000:
        return f"{value / 1_000_000:.1f}M"
    return f"{value:,}"


def _fmt_max_len(value: int | None) -> str:
    return "" if value is None else f"{value:,}"


def _fmt_embedding_dim(value: int | None) -> str:
    return "" if value is None else f"{value:,}"


def _fmt_row_embedding_dim(row: LeaderboardRow) -> str:
    if model_type_filter_key(model_name=row.source_model_name or row.model_name, model_type=row.model_type) == "sparse":
        return ""
    return _fmt_embedding_dim(row.embedding_dim)


def _fmt_percent_delta(value: float | None) -> str:
    return "" if value is None else f"{value:+.1f}%"


def _fmt_percent(value: float | None) -> str:
    return "" if value is None else f"{value:.1f}%"


def _fmt_signed_points(value: float | None) -> str:
    return "" if value is None else f"{value:+.2f}"


def _fmt_number(value: float | None) -> str:
    return "" if value is None else f"{value:,.1f}"


def _metric_column_label(column: str) -> str:
    parts = column.split("::")
    if len(parts) >= 3:
        dataset = parts[-2].rsplit("/", 1)[-1]
        task = parts[-1]
        return f"{dataset}::{task}"
    if len(parts) == 2:
        return column
    return column.removeprefix("Nano")


def _metric_column_labels(columns: list[str], *, overrides: dict[str, str] | None = None) -> dict[str, str]:
    overrides = overrides or {}
    labels_by_column = {column: overrides.get(column) or _metric_column_label(column) for column in columns}
    counts: dict[str, int] = {}
    for label in labels_by_column.values():
        counts[label] = counts.get(label, 0) + 1
    return {
        column: column if counts[label] > 1 else label
        for column, label in labels_by_column.items()
    }


def _page_url(query: QueryState) -> str:
    return escape(f"/?{urlencode(query, doseq=True)}", quote=True)


def _leaderboard_url(query: str) -> str:
    return escape(f"/leaderboard?{query}", quote=True)


def _csv_url(query: str) -> str:
    return escape(f"/leaderboard.csv?{query}", quote=True)
