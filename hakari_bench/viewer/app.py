from __future__ import annotations

import csv
from datetime import datetime, timezone
from functools import lru_cache
import hashlib
from html import escape
from io import StringIO
import math
import os
from pathlib import Path
import re
from typing import Iterable, TypedDict, cast
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
from hakari_bench.viewer.model_display import (
    ModelCellView,
    model_cell_views,
    render_model_detail_modal,
    render_model_name_cell,
)
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
    variant_category,
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
    "arrow-down-narrow-wide": (
        '<path d="m3 16 4 4 4-4"/>'
        '<path d="M7 20V4"/>'
        '<path d="M11 4h4"/>'
        '<path d="M11 8h7"/>'
        '<path d="M11 12h10"/>'
    ),
    "arrow-down-wide-narrow": (
        '<path d="m3 16 4 4 4-4"/>'
        '<path d="M7 20V4"/>'
        '<path d="M11 4h10"/>'
        '<path d="M11 8h7"/>'
        '<path d="M11 12h4"/>'
    ),
    "bar-chart-3": (
        '<path d="M3 3v18h18"/>'
        '<path d="M18 17V9"/>'
        '<path d="M13 17V5"/>'
        '<path d="M8 17v-3"/>'
    ),
    "binary": '<path d="M6 20h4"/><path d="M14 10h4"/><path d="M6 14h2v6"/><path d="M14 4h2v6"/>',
    "book-open": (
        '<path d="M12 7v14"/>'
        '<path d="M3 18a1 1 0 0 1-1-1V4a1 1 0 0 1 1-1h5a4 4 0 0 1 4 4 4 4 0 0 1 4-4h5a1 1 0 0 1 1 1v13a1 1 0 0 1-1 1h-6a3 3 0 0 0-3 3 3 3 0 0 0-3-3z"/>'
    ),
    "braces": '<path d="M8 3H7a2 2 0 0 0-2 2v4a2 2 0 0 1-2 2 2 2 0 0 1 2 2v4a2 2 0 0 0 2 2h1"/><path d="M16 21h1a2 2 0 0 0 2-2v-4a2 2 0 0 1 2-2 2 2 0 0 1-2-2V7a2 2 0 0 0-2-2h-1"/>',
    "calendar-days": '<path d="M8 2v4"/><path d="M16 2v4"/><rect width="18" height="18" x="3" y="4" rx="2"/><path d="M3 10h18"/><path d="M8 14h.01"/><path d="M12 14h.01"/><path d="M16 14h.01"/><path d="M8 18h.01"/><path d="M12 18h.01"/><path d="M16 18h.01"/>',
    "chevron-right": '<path d="m9 18 6-6-6-6"/>',
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
    "info-simple": '<path d="M12 17v-6"/><path d="M12 7h.01"/>',
    "languages": '<path d="m5 8 6 6"/><path d="m4 14 6-6 2-3"/><path d="M2 5h12"/><path d="M7 2h1"/><path d="m22 22-5-10-5 10"/><path d="M14 18h6"/>',
    "layers": '<path d="m12.83 2.18 8.5 4.73a1 1 0 0 1 0 1.75l-8.5 4.73a1.7 1.7 0 0 1-1.66 0l-8.5-4.73a1 1 0 0 1 0-1.75l8.5-4.73a1.7 1.7 0 0 1 1.66 0Z"/><path d="m22 12.5-9.17 5.1a1.7 1.7 0 0 1-1.66 0L2 12.5"/><path d="m22 17.5-9.17 5.1a1.7 1.7 0 0 1-1.66 0L2 17.5"/>',
    "list-filter": '<path d="M3 6h18"/><path d="M7 12h10"/><path d="M10 18h4"/>',
    "list-ordered": '<path d="M11 5h10"/><path d="M11 12h10"/><path d="M11 19h10"/><path d="M4 4h1v5"/><path d="M4 9h2"/><path d="M6.5 20H3.4c0-1 2.6-1.925 2.6-3.5a1.5 1.5 0 0 0-2.6-1.02"/>',
    "message-square-text": '<path d="M22 17a2 2 0 0 1-2 2H6.828a2 2 0 0 0-1.414.586l-2.202 2.202A.71.71 0 0 1 2 21.286V5a2 2 0 0 1 2-2h16a2 2 0 0 1 2 2z"/><path d="M7 11h10"/><path d="M7 15h6"/><path d="M7 7h8"/>',
    "moon": '<path d="M12 3a6 6 0 0 0 9 9 9 9 0 1 1-9-9Z"/>',
    "ruler": '<path d="M21.3 15.3a2.4 2.4 0 0 1 0 3.4l-2.6 2.6a2.4 2.4 0 0 1-3.4 0L2.7 8.7a2.4 2.4 0 0 1 0-3.4l2.6-2.6a2.4 2.4 0 0 1 3.4 0Z"/><path d="m14.5 12.5 2-2"/><path d="m11.5 9.5 2-2"/><path d="m8.5 6.5 2-2"/><path d="m17.5 15.5 2-2"/>',
    "scan-eye": '<path d="M3 7V5a2 2 0 0 1 2-2h2"/><path d="M17 3h2a2 2 0 0 1 2 2v2"/><path d="M21 17v2a2 2 0 0 1-2 2h-2"/><path d="M7 21H5a2 2 0 0 1-2-2v-2"/><circle cx="12" cy="12" r="1"/><path d="M18.944 12.33a1 1 0 0 0 0-.66 7.5 7.5 0 0 0-13.888 0 1 1 0 0 0 0 .66 7.5 7.5 0 0 0 13.888 0"/>',
    "search": '<path d="m21 21-4.34-4.34"/><circle cx="11" cy="11" r="8"/>',
    "shapes": '<path d="M8.3 10a.7.7 0 0 1-.626-1.079L11.4 3a.7.7 0 0 1 1.198-.043L16.3 8.9a.7.7 0 0 1-.572 1.1Z"/><rect x="3" y="14" width="7" height="7" rx="1"/><circle cx="17.5" cy="17.5" r="3.5"/>',
    "sun": '<circle cx="12" cy="12" r="4"/><path d="M12 2v2"/><path d="M12 20v2"/><path d="m4.93 4.93 1.41 1.41"/><path d="m17.66 17.66 1.41 1.41"/><path d="M2 12h2"/><path d="M20 12h2"/><path d="m6.34 17.66-1.41 1.41"/><path d="m19.07 4.93-1.41 1.41"/>',
    "table-properties": '<path d="M15 3v18"/><rect width="18" height="18" x="3" y="3" rx="2"/><path d="M21 9H3"/><path d="M21 15H3"/>',
    "type": '<path d="M12 4v16"/><path d="M4 7V5a1 1 0 0 1 1-1h14a1 1 0 0 1 1 1v2"/><path d="M9 20h6"/>',
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


def create_app(
    *,
    store: LocalDuckDbStore,
    config_dir: Path = Path("config/viewer"),
    docs_dir: Path = Path("task_docs/docs"),
    docs_metadata_dir: Path | None = None,
):
    from fastapi import FastAPI, Query
    from fastapi.middleware.gzip import GZipMiddleware
    from fastapi.responses import FileResponse, HTMLResponse, RedirectResponse, Response
    from fastapi.staticfiles import StaticFiles

    viewer_config = load_viewer_config(config_dir)
    resolved_docs_metadata_dir = docs_metadata_dir
    if resolved_docs_metadata_dir is None and docs_dir == Path("task_docs/docs"):
        resolved_docs_metadata_dir = Path("task_docs/metadata")
    benchmark_docs = BenchmarkDocs(docs_dir, metadata_dir=resolved_docs_metadata_dir)
    app = FastAPI(title="HAKARI-Bench leaderboard", docs_url=None, redoc_url=None)
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

    @app.get("/docs")
    @app.get("/docs/")
    def docs_index_redirect() -> RedirectResponse:
        return RedirectResponse(url="/docs/benchmark-tasks")

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
        target: str = Query(default="all", pattern="^(all|reranking|reranking_without_safeguard)$"),
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
                    database_label=_database_footer_label(store),
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
        target: str = Query(default="all", pattern="^(all|reranking|reranking_without_safeguard)$"),
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
        target: str = Query(default="all", pattern="^(all|reranking|reranking_without_safeguard)$"),
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
    database_label: str = "",
) -> str:
    query = urlencode(initial_query or {"view": viewer_config.overall.name, "sort": "borda_rank", "direction": "asc"}, doseq=True)
    css_url = _asset_url("app.css")
    favicon_url = _asset_url("favicon.png")
    htmx_url = _asset_url("htmx.min.js")
    viewer_js_url = _asset_url("viewer.js")
    latest_update = _latest_update_label(summary.latest_finished_at_utc if summary else None)
    footer = _render_page_footer(latest_update=latest_update, database_label=database_label)
    header_actions = _render_header_actions()
    return f"""<!doctype html>
<html lang="ja">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>HAKARI-Bench leaderboard</title>
  <link rel="canonical" href="/">
  <link rel="stylesheet" href="{css_url}">
  <link rel="icon" type="image/png" href="{favicon_url}">
  <meta name="htmx-config" content='{{"allowEval":false,"allowScriptTags":false,"includeIndicatorStyles":false}}'>
  <script src="{htmx_url}"></script>
  <script src="{viewer_js_url}" defer></script>
</head>
<body class="bg-zinc-50 text-zinc-950">
  <main class="mx-auto max-w-[1600px] px-4 py-6 sm:px-6">
    <header class="mb-4">
      <div class="flex items-start justify-between gap-3">
        <h1 class="flex min-w-0 items-center gap-2 text-2xl font-semibold">
          <img src="{favicon_url}" alt="" aria-hidden="true" class="h-8 w-8 shrink-0">
          <span>HAKARI-Bench leaderboard</span>
        </h1>
        {header_actions}
      </div>
      <p class="mt-2 border border-amber-200 bg-amber-50 px-3 py-2 text-sm font-medium text-amber-800">🚧 WIP: This leaderboard is currently under active implementation, so specifications and data may change significantly.</p>
      <p class="mt-2 max-w-4xl text-sm text-zinc-600">HAKARI-Bench is a lightweight multilingual information retrieval benchmark for comparing model performance and efficiency trade-offs across retrieval methods, compression variants, and reranking settings.</p>
    </header>
    <section
      id="leaderboard-panel"
      hx-get="{_leaderboard_url(query)}"
      hx-trigger="load"
      {_leaderboard_request_hx_attrs()}
    >
      <div class="leaderboard-initial-loading border border-zinc-200 bg-white text-sm font-medium text-zinc-700" role="status" aria-live="polite" aria-atomic="true">
        <span class="loading-spinner" aria-hidden="true"></span>
        <span>Loading leaderboard...</span>
      </div>
    </section>
    {render_leaderboard_loading_toast()}
    {render_global_tooltip()}
  </main>
  {footer}
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
      <span class="loading-spinner" aria-hidden="true"></span>
      <span>Loading leaderboard...</span>
    </div>
    """


def render_global_tooltip() -> str:
    return """
    <div id="hakari-global-tooltip" class="global-tooltip fixed border border-zinc-300 bg-white px-2 py-1 text-xs font-medium text-zinc-800 shadow-sm"
         role="tooltip" hidden></div>
    """


def _render_theme_toggle() -> str:
    return f"""<button id="hakari-theme-toggle" type="button" class="theme-toggle grid h-8 w-8 shrink-0 place-items-center border"
          aria-label="Toggle color theme" aria-pressed="false" title="Toggle color theme">
          <span class="theme-toggle-icon-light">{_icon_svg("moon", class_name="hakari-icon")}</span>
          <span class="theme-toggle-icon-dark">{_icon_svg("sun", class_name="hakari-icon")}</span>
        </button>"""


def _render_docs_link() -> str:
    return f"""<a id="hakari-docs-link" href="/docs/" class="theme-toggle grid h-8 w-8 shrink-0 place-items-center border"
          aria-label="Open documentation" title="Open documentation">
          {_icon_svg("book-open", class_name="hakari-icon")}
        </a>"""


def _render_header_actions() -> str:
    return f"""<div class="flex shrink-0 items-center gap-2">
          {_render_docs_link()}
          {_render_theme_toggle()}
        </div>"""


def _render_page_footer(*, latest_update: str, database_label: str) -> str:
    meta_items = []
    if latest_update:
        meta_items.append(
            f"""<span class="inline-flex items-center gap-1 whitespace-nowrap font-mono text-[11px] text-zinc-500">{_icon_svg("calendar-days", class_name="hakari-icon h-3.5 w-3.5 shrink-0")}<span>{escape(latest_update)}</span></span>"""
        )
    if database_label:
        meta_items.append(
            f"""<span class="min-w-0 text-left font-mono text-[11px] text-zinc-500 [overflow-wrap:anywhere] sm:text-right">{escape(database_label)}</span>"""
        )
    meta = "\n        ".join(meta_items)
    if meta:
        meta = f"""
      <div class="flex min-w-0 flex-col gap-1 sm:items-end">
        {meta}
      </div>"""
    return f"""<footer class="mx-auto max-w-[1600px] border-t border-zinc-200 px-4 py-2 text-[11px] text-zinc-500 sm:px-6">
    <div class="flex min-w-0 justify-end">
      {meta}
    </div>
  </footer>"""


def _database_footer_label(store: LocalDuckDbStore) -> str:
    if store.location.hf_source is not None:
        return f"database: remote / {_sha1_prefix(store.path)}"
    return f"database: local / {store.path}"


def _sha1_prefix(path: Path, *, length: int = 12) -> str:
    if not path.exists():
        return "unavailable"
    digest = hashlib.sha1()
    with path.open("rb") as file:
        for chunk in iter(lambda: file.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()[:length]


def _latest_update_label(latest_finished_at_utc: str | None) -> str:
    if not latest_finished_at_utc:
        return ""
    value = latest_finished_at_utc.strip()
    if not value:
        return ""
    try:
        parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError:
        timestamp = value.split(".", 1)[0]
        timestamp = timestamp.removesuffix("+00:00").removesuffix("Z")
        return f"Latest update: {timestamp}(UTC)" if timestamp else ""
    if parsed.tzinfo is not None:
        parsed = parsed.astimezone(timezone.utc)
    return f"Latest update: {parsed.strftime('%Y-%m-%dT%H:%M:%S')}(UTC)"


def _icon_svg(name: str, *, class_name: str = "hakari-icon") -> str:
    path = _ICON_PATHS[name]
    return (
        f"""<svg class="{class_name}" data-icon="{escape(name, quote=True)}" aria-hidden="true" """
        """viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" """
        f"""stroke-linecap="round" stroke-linejoin="round">{path}</svg>"""
    )


def _render_sort_indicator(*, active: bool, direction: str) -> str:
    if not active:
        return ""
    icon = "arrow-down-narrow-wide" if direction == "asc" else "arrow-down-wide-narrow"
    sort_direction_attr = escape(direction, quote=True)
    return (
        f"""<span class="inline-flex shrink-0 items-center text-cyan-700" """
        f"""data-sort-active="true" data-sort-direction="{sort_direction_attr}">"""
        f"""{_icon_svg(icon, class_name="hakari-icon h-3.5 w-3.5")}</span>"""
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
      <h3 id="doc-summary-heading" class="break-all text-base font-semibold">Benchmark documentation</h3>
      <button type="submit" class="border border-zinc-300 px-2 py-1 text-sm text-zinc-700 hover:border-cyan-600 hover:text-cyan-700">Close</button>
    </div>
  </form>
  <div class="px-4 py-3">
    <p id="doc-summary-description" class="mt-3 whitespace-pre-wrap text-sm leading-tight text-zinc-700"></p>
    <p class="mt-3 text-sm">
      <a id="doc-summary-link" class="text-cyan-700 underline-offset-2 hover:underline" href="#" target="_blank" rel="noopener noreferrer">Read the benchmark overview</a>
    </p>
  </div>
</dialog>
"""


def render_help_summary_modal() -> str:
    return """
<dialog id="help-summary-modal" class="w-[min(92vw,42rem)] border border-zinc-300 bg-white p-0 text-zinc-950 backdrop:bg-zinc-950/35">
  <form method="dialog">
    <div class="flex items-center justify-between border-b border-zinc-200 px-4 py-3">
      <h3 id="help-summary-heading" class="break-all text-base font-semibold">Help</h3>
      <button type="submit" class="border border-zinc-300 px-2 py-1 text-sm text-zinc-700 hover:border-cyan-600 hover:text-cyan-700">Close</button>
    </div>
  </form>
  <div class="px-4 py-3">
    <p id="help-summary-short" class="mt-3 text-sm font-medium leading-tight text-zinc-800"></p>
    <p id="help-summary-details" class="mt-3 whitespace-pre-wrap text-sm leading-tight text-zinc-700"></p>
  </div>
</dialog>
"""


def _render_doc_summary_trigger(*, doc: BenchmarkDoc, label: str) -> str:
    return f"""<button type="button"
                  class="doc-summary-trigger inline-flex h-3.5 w-3.5 shrink-0 cursor-pointer items-center justify-center rounded-full text-[9px] leading-none"
                  data-doc-title="{escape(doc.title, quote=True)}"
                  data-doc-description="{escape(doc.description, quote=True)}"
                  data-doc-url="{escape(doc.url, quote=True)}"
                  aria-label="{escape(label, quote=True)}">{_icon_svg("book-open")}</button>"""


def _render_help_tooltip(title: str, summary: str | None = None, details: str | None = None) -> str:
    summary = summary or _first_sentence(title)
    details = details or title
    return f"""<button type="button"
                    class="help-summary-trigger inline-flex h-3.5 w-3.5 shrink-0 cursor-pointer items-center justify-center rounded-full border border-zinc-300 text-[9px] leading-none text-zinc-600 hover:border-cyan-600 hover:text-cyan-700"
                    data-help-title="{escape(title, quote=True)}"
                    data-help-summary="{escape(summary, quote=True)}"
                    data-help-details="{escape(details, quote=True)}"
                    aria-label="{escape(title, quote=True)}">{_icon_svg("circle-help")}</button>"""


def _first_sentence(text: str) -> str:
    stripped = text.strip()
    if not stripped:
        return ""
    match = re.search(r"(?<=[.!?])\s+", stripped)
    return stripped[: match.start()].strip() if match else stripped


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
    mode_icon, mode_label = _score_target_display(result.score_target)
    return f"""
<div>
  {render_tabs(result=result, sort=sort, direction=direction, filter_state=filter_state, filter_context=filter_context, benchmark_docs=benchmark_docs)}
  <div class="mb-3 flex flex-wrap items-center justify-between gap-2 text-sm text-zinc-600" data-shown-count="{shown_count}">
    <div class="inline-flex flex-wrap items-center gap-x-2 gap-y-1">
      <span class="inline-flex items-center gap-1 font-medium text-zinc-600">
        {_icon_svg("table-properties", class_name="hakari-icon control-heading-icon shrink-0")}
        <span>{escape(result.view_label)}</span>
      </span>
      <span class="text-zinc-400">/</span>
      <span class="inline-flex items-center gap-1 text-zinc-600">
        {_icon_svg(mode_icon, class_name="hakari-icon h-3.5 w-3.5 shrink-0")}
        <span>{escape(mode_label)}</span>
      </span>
      <span class="text-zinc-400">/</span>
      <span>{shown_count} shown / {len(result.rows)} complete models / {result.expected_tasks} tasks</span>
    </div>
    <a class="inline-flex items-center gap-1 border border-zinc-300 bg-zinc-50 px-2 py-0.5 text-xs font-medium text-zinc-800 underline-offset-2 hover:border-cyan-600 hover:text-cyan-700"
       href="{_csv_url(csv_query)}" aria-label="Download visible leaderboard as CSV">
      {_icon_svg("file-spreadsheet", class_name="hakari-icon h-3.5 w-3.5")}
      <span>Download CSV</span>
    </a>
  </div>
  <div class="leaderboard-table-scroll overflow-x-auto border border-zinc-200 bg-white">
    <table class="leaderboard-table min-w-full border-collapse text-[0.8125rem]">
      {render_table_head(result=result, sort=sort, direction=direction, filter_state=filter_state, benchmark_docs=benchmark_docs)}
      {render_table_body(result=result, filter_context=filter_context)}
    </table>
  </div>
  {render_model_detail_modal()}
  {render_doc_summary_modal()}
  {render_help_summary_modal()}
</div>
"""


def _score_target_display(score_target: str) -> tuple[str, str]:
    if score_target == "all":
        return "search", "Retrieval"
    return "list-ordered", "Reranking"


def render_tabs(
    *,
    result: LeaderboardResult,
    sort: str,
    direction: str,
    filter_state: FilterState | None = None,
    filter_context: FilterContext | None = None,
    benchmark_docs: BenchmarkDocs | None = None,
) -> str:
    filter_state = filter_state or FilterState()
    filter_context = filter_context or row_filter_context(result.rows, filter_state)
    grouped_buttons: dict[str, list[tuple[int, str]]] = {
        "Scope presets": [],
        "Nano suites": [],
    }
    for index, view_name in enumerate(result.available_views):
        active = view_name == result.view_name
        raw_view_label = result.available_view_labels.get(view_name, view_name)
        view_label = _viewer_scope_label(view_name=view_name, fallback=raw_view_label)
        classes = _control_button_classes(active=active)
        tab_sort = "borda_rank" if sort.startswith("metric:") else sort
        tab_direction = "asc" if sort.startswith("metric:") else direction
        query_payload = state_payload(result=result, sort=tab_sort, direction=tab_direction, filter_state=filter_state)
        query_payload["view"] = view_name
        doc = benchmark_docs.group_doc(view_name) if benchmark_docs is not None else None
        group = _view_group(view_name)
        sort_key = _view_group_sort_key(view_name=view_name, fallback=index)
        if group == "Scope presets":
            query_payload.pop("group", None)
            query = urlencode(query_payload, doseq=True)
            grouped_buttons[group].append(
                (
                    sort_key,
                    _render_scope_button(
                        result=result,
                        view_name=view_name,
                        view_label=view_label,
                        query=query,
                        query_payload=query_payload,
                    ),
                )
            )
            continue
        if view_name == "MNanoBEIR":
            for offset, score_group, label in [
                (0, "task_mean", "M-BEIR(task)"),
                (1, "lang_mean", "M-BEIR(lang)"),
            ]:
                group_query_payload = dict(query_payload)
                group_query_payload["group"] = score_group
                group_query = urlencode(group_query_payload, doseq=True)
                active = result.view_name == view_name and (
                    result.selected_score_group is not None and result.selected_score_group.name == score_group
                )
                grouped_buttons[group].append(
                    (
                        sort_key * 10 + offset,
                        _render_benchmark_view_button(
                            label=label,
                            active=active,
                            query=group_query,
                            query_payload=group_query_payload,
                            doc=doc,
                        ),
                    )
                )
            continue
        query_payload.pop("group", None)
        query = urlencode(query_payload, doseq=True)
        if doc is None:
            grouped_buttons[group].append(
                (
                    sort_key * 10,
                    f"""<button type="button" class="border px-2 py-1 text-[0.8125rem] leading-tight {classes}"
                      hx-get="{_leaderboard_url(query)}" hx-push-url="{_page_url(query_payload)}"
                      {_leaderboard_control_hx_attrs()}>
                      {escape(view_label)}
                    </button>""",
                )
            )
            continue
        grouped_buttons[group].append(
            (
                sort_key * 10,
                _render_benchmark_view_button(
                    label=view_label,
                    active=active,
                    query=query,
                    query_payload=query_payload,
                    doc=doc,
                ),
            )
        )
    preset_buttons = [button for _, button in sorted(grouped_buttons["Scope presets"])]
    suite_buttons = [button for _, button in sorted(grouped_buttons["Nano suites"])]
    return f"""
    <nav class="mb-4 border border-zinc-200 bg-white p-2 text-[0.8125rem] text-zinc-700" aria-label="Leaderboard configuration">
      <div class="grid gap-2">
        <div class="border border-zinc-200 bg-white p-2">
          <div class="flex flex-wrap items-center gap-x-5 gap-y-2">
            {_render_target_group(result=result, sort=sort, direction=direction, filter_state=filter_state)}
            {_render_metric_group(result=result, sort=sort, direction=direction, filter_state=filter_state)}
          </div>
        </div>
        <div class="grid gap-2">
          <div class="border border-zinc-200 bg-white p-2">
            <div class="mb-2 flex flex-wrap items-center gap-2">
              <span class="control-label-group inline-flex items-center gap-1 px-2 py-1 text-[0.8125rem]">
                {_control_label(icon="database", text="Benchmark scope")}
              </span>
              <div class="flex flex-wrap gap-2">{''.join(preset_buttons)}</div>
            </div>
            <div class="flex min-w-0 flex-wrap gap-2">{''.join(suite_buttons)}</div>
          </div>
          {render_language_pages(result=result, sort=sort, direction=direction, filter_state=filter_state, embedded=True)}
        </div>
        {render_display_controls(result=result, sort=sort, direction=direction, filter_state=filter_state)}
        {render_controls(result=result, sort=sort, direction=direction, filter_state=filter_state, filter_context=filter_context)}
      </div>
    </nav>
    """


def _render_scope_button(
    *,
    result: LeaderboardResult,
    view_name: str,
    view_label: str,
    query: str,
    query_payload: QueryState,
) -> str:
    active = view_name == result.view_name
    classes = _control_button_classes(active=active)
    title, summary, details = _scope_preset_help(view_name)
    help_icon = _render_button_help_icon(title=title, summary=summary, details=details)
    return f"""<span class="control-button-group inline-flex items-center border text-[0.8125rem] leading-tight {classes}">
                  <button type="button" class="py-1 pl-2 pr-0 text-left"
                    hx-get="{_leaderboard_url(query)}" hx-push-url="{_page_url(query_payload)}"
                    {_leaderboard_control_hx_attrs()}>{escape(view_label)}</button>
                  <span class="inline-flex items-center pl-1 pr-2">{help_icon}</span>
                </span>"""


def _render_benchmark_view_button(
    *,
    label: str,
    active: bool,
    query: str,
    query_payload: QueryState,
    doc: BenchmarkDoc | None,
) -> str:
    classes = _control_button_classes(active=active)
    if doc is None:
        return f"""<button type="button" class="border px-2 py-1 text-[0.8125rem] leading-tight {classes}"
                      hx-get="{_leaderboard_url(query)}" hx-push-url="{_page_url(query_payload)}"
                      {_leaderboard_control_hx_attrs()}>
                      {escape(label)}
                    </button>"""
    doc_trigger = _render_doc_summary_trigger(doc=doc, label=f"{doc.title} overview")
    return f"""<span class="control-button-group doc-label-group inline-flex items-center border text-[0.8125rem] leading-tight {classes}" data-doc-label-group="benchmark">
              <button type="button" class="py-1 pl-2 pr-0 text-left"
                hx-get="{_leaderboard_url(query)}" hx-push-url="{_page_url(query_payload)}"
                {_leaderboard_control_hx_attrs()}>
                {escape(label)}
              </button>
              <span class="inline-flex items-center pl-0.5 pr-2">{doc_trigger}</span>
            </span>"""


def _render_button_help_icon(*, title: str, summary: str, details: str) -> str:
    return f"""<button type="button"
                    class="help-summary-trigger inline-flex h-3.5 w-3.5 shrink-0 items-center justify-center rounded-full border border-zinc-300 text-[9px] leading-none text-zinc-600"
                    data-help-title="{escape(title, quote=True)}"
                    data-help-summary="{escape(summary, quote=True)}"
                    data-help-details="{escape(details, quote=True)}"
                    aria-label="{escape(title, quote=True)}">{_icon_svg("circle-help")}</button>"""


def _scope_preset_help(view_name: str) -> tuple[str, str, str]:
    help_text = {
        "All": (
            "Benchmark scope: All",
            "Shows every benchmark family available in the viewer.",
            "All is the broadest leaderboard scope. It includes multilingual suites, language-specific Nano suites, and domain-specific Nano suites before any language, model, task, or variant filters are applied.\n\nUse All when you want a comprehensive ranking across the full current HAKARI-Bench database. Because large benchmark families contain many tasks, use Group when you want a more balanced family-level overview.",
        ),
        "Core": (
            "Benchmark scope: Core",
            "Shows the compact core benchmark set.",
            "Core is a smaller scope intended for a quick read of general retrieval quality. It includes MNanoBEIR by task plus NanoMMTEB-v2, NanoRTEB, NanoMLDR, NanoBRIGHT, and NanoCoIR.\n\nUse Core when you want a dense but manageable comparison before drilling into a specific Nano suite or language.",
        ),
        "Group": (
            "Benchmark scope: Group",
            "Ranks models after configured benchmark families are averaged into groups.",
            "Group reduces the influence of large suites by first aggregating configured benchmark families, then ranking models on those grouped scores.\n\nUse Group when you want a balanced overview across benchmark families instead of letting suites with many tasks dominate the mean.",
        ),
    }
    return help_text.get(
        view_name,
        (
            f"Benchmark scope: {view_name}",
            f"Shows the {view_name} scope from the viewer configuration.",
            "Benchmark scope chooses the tasks that are eligible for the leaderboard before row filters are applied.\n\nUse this control first when you want to compare models on a specific benchmark family, then refine the result with language, model, task, and variant filters.",
        ),
    )


def _render_benchmark_group(*, label: str, description: str, buttons: list[str], framed: bool = True) -> str:
    if not buttons:
        return ""
    wrapper_class = "min-w-0 border border-zinc-200 bg-zinc-50 p-2" if framed else "min-w-0"
    description_html = f'<p class="mb-2 text-xs leading-tight text-zinc-500">{escape(description)}</p>' if description and not framed else ""
    return f"""
              <div class="{wrapper_class}">
                <p class="mb-1 text-xs font-semibold uppercase text-zinc-500">{escape(label)}</p>
                {description_html}
                <div class="flex flex-wrap gap-2">{''.join(buttons)}</div>
              </div>
            """


def _render_target_group(*, result: LeaderboardResult, sort: str, direction: str, filter_state: FilterState) -> str:
    target_options = [
        ("all", "Retrieval", "search"),
        ("reranking", "Reranking", "list-ordered"),
    ]
    buttons = []
    for target, label, icon in target_options:
        active = result.score_target == "all" if target == "all" else result.score_target != "all"
        classes = _control_button_classes(active=active)
        tab_sort = "borda_rank" if sort.startswith("metric:") else sort
        tab_direction = "asc" if sort.startswith("metric:") else direction
        query_payload = state_payload(result=result, sort=tab_sort, direction=tab_direction, filter_state=filter_state)
        if target == "all":
            query_payload.pop("target", None)
        else:
            query_payload["target"] = target
        query = urlencode(query_payload, doseq=True)
        buttons.append(
            f"""<button type="button" class="inline-flex items-center gap-1.5 border px-2 py-1 text-[0.8125rem] leading-tight {classes}"
                  hx-get="{_leaderboard_url(query)}" hx-push-url="{_page_url(query_payload)}"
                  {_leaderboard_control_hx_attrs()}>
                  {_icon_svg(icon)}
                  <span>{escape(label)}</span>
                </button>"""
        )
    safeguard_toggle = ""
    if result.score_target != "all":
        safeguard_enabled = result.score_target == "reranking"
        toggle_target = "reranking_without_safeguard" if safeguard_enabled else "reranking"
        checked_attr = " checked" if safeguard_enabled else ""
        query_payload = state_payload(result=result, sort=sort, direction=direction, filter_state=filter_state)
        query_payload["target"] = toggle_target
        query = urlencode(query_payload, doseq=True)
        safeguard_help = _render_help_tooltip(
            "Safeguard positives",
            "Keeps reranking tasks comparable by ensuring each candidate list contains at least one relevant positive.",
            "This option applies only in Reranking mode. Rerankers do not search the full corpus; they reorder a fixed candidate list, usually produced by BM25.\n\nWhen Safeguard positives is enabled, the candidate list uses the rank-101 safeguard so every evaluated task includes at least one known positive document. This is the default because it avoids scoring a reranker on tasks where the relevant document never appears in the candidate set.\n\nTurn it off only when you intentionally want to inspect reranking behavior without that safeguard.",
        )
        safeguard_toggle = f"""
                <span class="control-button-group inline-flex items-center border border-zinc-300 bg-white text-[0.8125rem] leading-tight text-zinc-700 hover:border-cyan-500 hover:text-cyan-700">
                  <label class="inline-flex items-center gap-2 py-1 pl-2 pr-0">
                    <input type="checkbox" class="h-4 w-4 accent-cyan-700"{checked_attr}
                      hx-get="{_leaderboard_url(query)}" hx-push-url="{_page_url(query_payload)}"
                      {_leaderboard_control_hx_attrs()}>
                    <span>Safeguard positives</span>
                  </label>
                  <span class="inline-flex items-center pl-1 pr-2">{safeguard_help}</span>
                </span>
        """
    return f"""
            <div class="flex min-w-0 flex-wrap items-center gap-2">
              {''.join(buttons)}
              {_render_help_tooltip(
                  "Evaluation mode",
                  "Switches the leaderboard between retrieval runs and reranking runs.",
                  "Evaluation mode chooses which result family is shown before the benchmark scope and filters are applied.\n\nRetrieval shows full-corpus retrieval results. Dense, sparse/BM25, and late-interaction models retrieve directly from the corpus and are compared as retrieval systems.\n\nReranking shows cross-encoder reranker results on a shared candidate set. Use Reranking when you want to compare how rerankers reorder candidates rather than how retrievers search the full corpus.",
              )}
              {safeguard_toggle}
            </div>
            """


def _render_metric_group(*, result: LeaderboardResult, sort: str, direction: str, filter_state: FilterState) -> str:
    if len(result.available_score_metrics) <= 1:
        return ""
    buttons = []
    for metric in result.available_score_metrics:
        active = metric == result.selected_score_metric
        classes = _control_button_classes(active=active)
        tab_sort = "borda_rank" if sort.startswith("metric:") else sort
        tab_direction = "asc" if sort.startswith("metric:") else direction
        query_payload = state_payload(result=result, sort=tab_sort, direction=tab_direction, filter_state=filter_state)
        if metric == "ndcg@10":
            query_payload.pop("metric", None)
        else:
            query_payload["metric"] = metric
        query = urlencode(query_payload, doseq=True)
        buttons.append(
            f"""<button type="button" class="border px-2 py-1 text-[0.8125rem] leading-tight {classes}"
                  hx-get="{_leaderboard_url(query)}" hx-push-url="{_page_url(query_payload)}"
                  {_leaderboard_control_hx_attrs()}>
                  {escape(_score_metric_label(metric))}
                </button>"""
        )
    return f"""
            <div class="flex min-w-0 flex-wrap items-center gap-2">
              <span class="control-label-group inline-flex items-center gap-1 px-2 py-1 text-[0.8125rem]">
                {_control_label(icon="bar-chart-3", text="Metric")}
                {_render_help_tooltip(
                  "Score metric",
                  "Changes the metric used for model means, Borda ranks, and task columns.",
                  "Score metric selects which evaluation score is used throughout the current leaderboard.\n\nThe selected metric affects model means, Borda rank calculations, sortable task columns, and exported CSV scores. nDCG@10 is the default because it is the primary ranking-quality metric for the benchmark.\n\nRecall metrics are useful when you care about candidate coverage, especially before reranking. Accuracy, MRR, and MAP views are diagnostic alternatives for tasks where those metrics are available.",
                )}
              </span>
              {''.join(buttons)}
            </div>
            """


def _score_metric_label(metric: str) -> str:
    family, separator, cutoff = metric.partition("@")
    labels = {
        "ndcg": "nDCG",
        "acc": "Acc",
        "hit": "Acc",
        "map": "MAP",
        "mrr": "MRR",
        "accuracy": "Acc",
        "precision": "Precision",
        "recall": "Recall",
    }
    return f"{labels.get(family, family.upper())}@{cutoff}" if separator else metric


def _view_group(view_name: str) -> str:
    overall_views = {"All", "Core", "Group"}
    if view_name in overall_views or view_name.startswith("Overall"):
        return "Scope presets"
    return "Nano suites"


def _view_group_sort_key(*, view_name: str, fallback: int) -> int:
    priority = {
        "All": 0,
        "Core": 1,
        "Group": 2,
        "MNanoBEIR": 0,
        "NanoMMTEB-v2": 1,
        "NanoRTEB": 2,
        "NanoMLDR": 3,
        "NanoMIRACL": 4,
        "NanoCoIR": 5,
        "NanoBRIGHT": 6,
        "NanoIndicQA": 7,
        "NanoMuPLeR": 8,
        "NanoCodeRAG": 9,
    }
    return priority.get(view_name, 1000 + fallback)


def _viewer_scope_label(*, view_name: str, fallback: str) -> str:
    if view_name == "MNanoBEIR":
        return "M-BEIR(task)"
    if fallback.startswith("Nano"):
        return fallback.removeprefix("Nano")
    return fallback


def _control_button_classes(*, active: bool) -> str:
    return (
        "border-cyan-700 bg-cyan-50 text-cyan-900"
        if active
        else "border-zinc-300 bg-white text-zinc-700 hover:border-cyan-500 hover:text-cyan-700"
    )


def render_language_pages(
    *,
    result: LeaderboardResult,
    sort: str,
    direction: str,
    filter_state: FilterState | None = None,
    embedded: bool = False,
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
    visible_options = result.available_languages[:8]
    more_options = result.available_languages[8:]
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
            <summary class="cursor-pointer border border-zinc-300 bg-white px-2 py-1 text-[0.8125rem] text-zinc-700 hover:border-cyan-500 hover:text-cyan-700">More languages</summary>
            <div class="absolute z-10 mt-1 grid max-h-72 min-w-[28rem] grid-cols-3 gap-1 overflow-auto border border-zinc-300 bg-white p-2 shadow-sm sm:grid-cols-5">
              {more_buttons}
            </div>
          </details>
        """
    wrapper_tag = "div" if embedded else "nav"
    wrapper_class = (
        "flex flex-wrap items-start gap-2 border border-zinc-200 bg-white p-2"
        if embedded
        else "mb-4 flex flex-wrap items-start gap-2 border border-zinc-200 bg-white p-2"
    )
    return f"""
      <{wrapper_tag} class="{wrapper_class}" aria-label="Task facets">
        <span class="control-label-group inline-flex items-center gap-1 px-2 py-1 text-[0.8125rem]">
          {_control_label(icon="languages", text="Task facets")}
          {_render_help_tooltip(
              "Task facets",
              "Filters tasks inside the selected benchmark scope by language.",
              "Task facets narrows the tasks that are included after you choose a benchmark scope.\n\nFor multilingual suites such as MNanoBEIR, each language page filters the task set to one language-specific slice, such as Japanese or German. The All languages button removes that language filter.\n\nThis is different from Benchmark scope: scope chooses the benchmark family, while Task facets filters the tasks inside that family.",
          )}
        </span>
        {''.join(buttons)}
        {more}
      </{wrapper_tag}>
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
    label = "All languages" if option is None else f"{option.label} {option.task_count}"
    classes = _control_button_classes(active=active)
    query_payload = state_payload(
        result=result,
        sort=sort,
        direction=direction,
        filter_state=_filter_state_with_languages(filter_state, language_filters),
    )
    query = urlencode(query_payload, doseq=True)
    data_attr = "" if option is None else f' data-language-page="{escape(option.code)}"'
    return f"""<button type="button"{data_attr} class="shrink-0 whitespace-nowrap border px-2 py-1 text-[0.8125rem] {classes}"
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


def render_display_controls(
    *,
    result: LeaderboardResult,
    sort: str,
    direction: str,
    filter_state: FilterState | None = None,
) -> str:
    filter_state = filter_state or FilterState()
    quantization_checked = " checked" if result.include_quantization_variants else ""
    truncate_checked = " checked" if result.include_truncate_variants else ""
    rescore_checked = " checked" if result.include_rescore_variants else ""
    other_variant_checked = " checked" if result.include_other_variants else ""
    task_scores_checked = " checked" if result.show_task_scores else ""
    task_z_scores_checked = " checked" if result.show_task_z_scores else ""
    task_ranks_checked = " checked" if result.show_task_ranks else ""
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
    return f"""
    <div class="grid gap-2 text-[0.8125rem] text-zinc-700 lg:grid-cols-2">
      <form id="column-controls" class="border border-zinc-200 bg-white p-2"
            hx-get="/leaderboard" hx-push-url="true"
            {_leaderboard_control_hx_attrs()}
            hx-trigger="change, submit">
        {column_hidden_html}
        <div class="mb-2 flex flex-wrap items-center gap-2">
          {_control_label(icon="table-properties", text="Table display")}
          {_render_help_tooltip(
              "Table display",
              "Changes which columns and per-task annotations are visible.",
              "Table display controls how much detail appears in the result table without changing which models or tasks are included.\n\nTask columns adds one score column per task or grouped task. STD overlays standardized task scores so you can see unusually strong or weak task performance. Task ranks shows the per-task rank instead of the raw score; when STD and Task ranks are both enabled, each task cell shows the rank alongside the standardized score.\n\nUse this panel when the ranking is already scoped correctly and you want to inspect the table at a different level of detail.",
          )}
        </div>
        <div class="flex flex-wrap items-center gap-x-5 gap-y-2">
          <label class="inline-flex items-center gap-2">
            <input type="checkbox" name="task_scores" value="1" class="h-4 w-4 accent-cyan-700"{task_scores_checked}>
            <span>Task columns</span>
          </label>
          <label class="inline-flex items-center gap-2">
            <input type="hidden" name="task_z_scores" value="0">
            <input type="checkbox" name="task_z_scores" value="1" class="h-4 w-4 accent-cyan-700"{task_z_scores_checked}>
            <span>STD</span>
          </label>
          <label class="inline-flex items-center gap-2">
            <input type="hidden" name="task_ranks" value="0">
            <input type="checkbox" name="task_ranks" value="1" class="h-4 w-4 accent-cyan-700"{task_ranks_checked}>
            <span>Task ranks</span>
          </label>
        </div>
      </form>
      <form id="variant-controls" class="border border-zinc-200 bg-white p-2"
            hx-get="/leaderboard" hx-push-url="true"
            {_leaderboard_control_hx_attrs()}
            hx-trigger="change, submit">
        {variant_hidden_html}
        <div class="mb-2 flex flex-wrap items-center gap-2">
          {_control_label(icon="git-compare-arrows", text="Efficiency variants")}
          {_render_help_tooltip(
              "Efficiency variants",
              "Adds non-base rows that compare quality against storage, dimension, and reranking trade-offs.",
              "Efficiency variants are additional result rows for the same source model. They are hidden by default so the base leaderboard stays compact.\n\nDims includes truncated embedding rows and uses short labels such as 512d or 512d <- 1024. Quantization includes compressed numeric formats such as int8 and binary. Rescore includes variants that run a compressed first pass and then rescore or rerank. Other includes model-specific variants, especially sparse active-dimension limits, with compact labels such as q32d and d256d when available.\n\nUse this panel when you want to compare a model's base score with smaller, faster, or compressed alternatives.",
          )}
        </div>
        <div class="flex flex-wrap items-center gap-x-5 gap-y-2">
          <label class="inline-flex items-center gap-2">
            <input type="checkbox" name="truncate" value="1" class="h-4 w-4 accent-cyan-700"{truncate_checked}>
            <span>Dims</span>
          </label>
          <label class="inline-flex items-center gap-2">
            <input type="checkbox" name="quantization" value="1" class="h-4 w-4 accent-cyan-700"{quantization_checked}>
            <span>Quantization</span>
          </label>
          <label class="inline-flex items-center gap-2">
            <input type="checkbox" name="rescore" value="1" class="h-4 w-4 accent-cyan-700"{rescore_checked}>
            <span>Rescore</span>
          </label>
          <label class="inline-flex items-center gap-2">
            <input type="checkbox" name="other_variant" value="1" class="h-4 w-4 accent-cyan-700"{other_variant_checked}>
            <span>Other</span>
          </label>
        </div>
      </form>
    </div>
    """


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
    advanced_filter_open_attr = " open" if filter_state.filters_active or filter_state.has_task_length_filters else ""
    return f"""
    <div class="grid gap-2 text-[0.8125rem] text-zinc-700">
      <form id="filter-controls" class="border border-zinc-200 bg-white p-2"
            hx-get="/leaderboard" hx-push-url="true"
            {_leaderboard_control_hx_attrs()}
            hx-trigger="change, submit">
        {filter_hidden_html}
        <div class="mb-2 flex flex-wrap items-center justify-between gap-2">
          <span class="inline-flex items-center gap-1">
            {_control_label(icon="filter", text="Refine results")}
            {_render_help_tooltip(
                "Refine results",
                "Narrows the models, tasks, and variant rows shown in the current leaderboard.",
                "Refine results applies filters after Evaluation mode, Benchmark scope, Task facets, and Efficiency variants have selected the candidate result set.\n\nModel and Task text filters are applied when you press Enter. Checkbox and facet filters update automatically. These controls can hide rows and task columns from the table, and they also affect CSV download.\n\nBy default, ranks keep their original global context. Enable Recalculate ranks from filters when you want ranks and means to be recomputed from only the filtered results.",
            )}
          </span>
          <label class="inline-flex items-center gap-2">
            <input type="hidden" name="rank_filtered" value="0">
            <input type="checkbox" name="rank_filtered" value="1" class="h-4 w-4 accent-cyan-700"{rank_filtered_checked}>
            <span class="font-medium text-zinc-800">Recalculate ranks from filters</span>
            {_render_help_tooltip(
                "Recalculate ranks from filters",
                "Recomputes ranking numbers using only the currently filtered result set.",
                "When this is enabled, Borda ranks, mean ranks, and visible means are recalculated after model, task, language, variant, and advanced filters are applied.\n\nUse it when you want to answer a local question, such as which model is best among dense models only, or which model wins on a specific task family.\n\nLeave it off when you want filtered rows to keep their original leaderboard rank context.",
            )}
          </label>
        </div>
        <div class="grid gap-2">
          <div class="min-w-0 space-y-2">
            {_render_model_type_controls(
                options=model_type_options,
                selected_values=selected_model_types,
            )}
            <div class="flex flex-wrap items-center gap-3">
              <label class="flex min-w-64 flex-1 items-center gap-2">
                <span class="shrink-0 whitespace-nowrap font-medium text-zinc-800">Model</span>
                {_render_help_tooltip(
                    "Model filter",
                    "Filters leaderboard rows by model name.",
                    "Model filter searches the displayed model names and hides rows that do not match.\n\nYou can search for multiple model-name keywords by separating them with spaces. The terms are matched as OR conditions with partial, case-insensitive matching. For example, jina bge keeps rows whose model name contains jina or bge.\n\nModel keywords under 3 characters are ignored to avoid accidental broad matches. This filter changes which model rows are visible. It does not change the selected benchmark scope or which task columns are available.",
                )}
                <input id="model-filter-input" type="search" name="model_filter" value="{escape(filter_state.model_filter)}"
                       class="w-72 max-w-full border border-zinc-300 bg-white px-2 py-1 text-[0.8125rem] text-zinc-900 outline-none focus:border-cyan-700"
                       autocomplete="off">
              </label>
              <label class="flex min-w-64 flex-1 items-center gap-2">
                <span class="shrink-0 whitespace-nowrap font-medium text-zinc-800">Task</span>
                {_render_help_tooltip(
                    "Task filter",
                    "Filters task columns and task rows by benchmark, dataset, split, or task name.",
                    "Task filter searches task identifiers such as benchmark name, dataset name, split name, task name, and task key.\n\nYou can search for multiple task keywords by separating them with spaces. The terms are matched as OR conditions with partial, case-insensitive matching. For example, arguana fever keeps task columns or task rows whose identifiers contain arguana or fever. Short task names such as nq also work because task keywords are accepted from 2 characters.\n\nWhen task columns are visible, matching task columns remain and non-matching columns are hidden. The underlying model ranking keeps its original context unless Recalculate ranks from filters is enabled. One-character task keywords are ignored.",
                )}
                <input id="task-filter-input" type="search" name="task_filter" value="{escape(filter_state.task_filter)}"
                       class="w-72 max-w-full border border-zinc-300 bg-white px-2 py-1 text-[0.8125rem] text-zinc-900 outline-none focus:border-cyan-700"
                       autocomplete="off">
              </label>
            </div>
          </div>
          <details id="facet-filters" class="filter-panel min-w-0 bg-zinc-50 p-2"{advanced_filter_open_attr}>
            <summary class="advanced-filter-summary flex cursor-pointer list-none items-center justify-between gap-2 text-[0.8125rem] font-medium text-zinc-800">
              <span class="inline-flex items-center gap-1.5">
                <span class="details-chevron inline-flex h-4 w-4 shrink-0 items-center justify-center text-zinc-500">{_icon_svg("chevron-right")}</span>
                <span class="inline-flex items-center gap-1">
                  {_control_label(icon="list-filter", text="Advanced filters")}
                  {_render_help_tooltip(
                      "Advanced filters",
                      "Opens lower-level filters for dimensions, quantization, task length, dtype, attention, and prompts.",
                      "Advanced filters refine the current result set after the main controls have selected the evaluation mode, benchmark scope, language facet, and variant categories.\n\nUse Efficiency filters to narrow variant rows by embedding dimensions or quantization type. Use Length to include only tasks within query/document length bounds. Use Run metadata to inspect how results were produced, such as dtype, attention implementation, or prompt metadata.\n\nThese filters are useful for diagnostics and audits. They can change which rows and task columns are visible, especially when Recalculate ranks from filters is enabled.",
                  )}
                </span>
              </span>
            </summary>
            <div class="filter-panel-body mt-2 space-y-2">
              <div class="flex flex-wrap items-center gap-2">
                {_control_label(icon="git-branch", text="Efficiency filters")}
                {_render_help_tooltip(
                    "Efficiency filters",
                    "Filters already-included variant rows by dimensions or quantization type.",
                    "Efficiency filters only operate on rows that are already present in the table.\n\nFirst use Efficiency variants to include Dims, Quantization, Rescore, or Other variant rows. Then use Dims to keep specific embedding sizes, or Quantization to keep formats such as int8 or binary.\n\nThis is useful when a variant category is too broad and you want to compare a smaller set of compression settings.",
                )}
                {_render_filter_details(name="dim_filter", summary="Dims", icon="ruler", options=dim_options, selected_values=selected_dims, all_query=dim_all_query, none_query=dim_none_query)}
                {_render_filter_details(name="quant_filter", summary="Quantization", icon="binary", options=quant_options, selected_values=selected_quants, all_query=quant_all_query, none_query=quant_none_query)}
              </div>
              {_render_task_length_filter_inputs(filter_state)}
              <div class="flex flex-wrap items-center gap-2">
                {_control_label(icon="cpu", text="Run metadata")}
                {_render_help_tooltip(
                    "Run metadata filters",
                    "Filters rows by recorded evaluation metadata such as dtype, attention, and prompt use.",
                    "Run metadata describes how a result was produced. Dtype indicates numeric precision such as bf16 or fp32. Attention records the attention implementation when available. Prompt records whether query or document prompts were used.\n\nThese filters do not change the benchmark scope or task definition. They help audit comparability between runs and isolate results produced with a specific runtime configuration.",
                )}
                {_render_filter_details(name="dtype_filter", summary="Dtype", icon="type", options=dtype_options, selected_values=selected_dtypes, all_query=dtype_all_query, none_query=dtype_none_query)}
                {_render_filter_details(name="attn_filter", summary="Attention", icon="scan-eye", options=attn_options, selected_values=selected_attn, all_query=attn_all_query, none_query=attn_none_query)}
                {_render_filter_details(name="prompt_filter", summary="Prompt", icon="message-square-text", options=prompt_options, selected_values=selected_prompts, all_query=prompt_all_query, none_query=prompt_none_query)}
              </div>
            </div>
          </details>
        </div>
      </form>
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
        <span class="inline-flex items-center gap-1">
          {_control_label(icon="shapes", text="Model family")}
          {_render_help_tooltip(
              "Model family",
              "Filters rows by the retrieval or reranking family recorded for each model result.",
              "Model family separates model rows by how the result was produced.\n\nDense models use dense embeddings. Sparse / BM25 rows use lexical or sparse retrieval. Late interaction rows use token-level interaction methods such as ColBERT-style scoring. Reranker rows appear when Evaluation mode is set to Reranking.\n\nUse this filter when you want to compare models within one retrieval family or hide families that are not relevant to the current analysis.",
          )}
        </span>
        {''.join(checkboxes)}
      </fieldset>
    """


def _render_task_length_filter_inputs(filter_state: FilterState) -> str:
    input_class = (
        "w-24 border border-zinc-300 bg-white px-2 py-1 text-[0.8125rem] text-zinc-900 outline-none "
        "focus:border-cyan-700"
    )
    active_class = "text-cyan-700" if filter_state.has_task_length_filters else ""
    return f"""
    <div class="flex flex-wrap items-center gap-2">
      <span class="inline-flex items-center gap-1">
        {_control_label(icon="ruler", text="Length", extra_class=active_class)}
        {_render_help_tooltip(
            "Length filters",
            "Filters tasks by average query and document string length.",
            "Length filters operate at the task level using average text length metadata measured in characters.\n\nQuery length bounds filter by the average query string length for a task. Document length bounds filter by the average document string length. For example, setting Document length <= 2000 keeps tasks whose documents are relatively short on average.\n\nTasks without length metadata are excluded when any bound is set. Use this when you want to inspect short-query tasks, long-document tasks, or other length-sensitive behavior.",
        )}
      </span>
      <label class="inline-flex items-center gap-1">
        <span class="text-xs font-medium text-zinc-700">Query length ≥</span>
        <input type="number" min="0" step="any" name="query_len_min" value="{escape(filter_state.query_len_min)}"
               class="{input_class}">
      </label>
      <label class="inline-flex items-center gap-1">
        <span class="text-xs font-medium text-zinc-700">Query length ≤</span>
        <input type="number" min="0" step="any" name="query_len_max" value="{escape(filter_state.query_len_max)}"
               class="{input_class}">
      </label>
      <label class="inline-flex items-center gap-1">
        <span class="text-xs font-medium text-zinc-700">Document length ≥</span>
        <input type="number" min="0" step="any" name="doc_len_min" value="{escape(filter_state.doc_len_min)}"
               class="{input_class}">
      </label>
      <label class="inline-flex items-center gap-1">
        <span class="text-xs font-medium text-zinc-700">Document length ≤</span>
        <input type="number" min="0" step="any" name="doc_len_max" value="{escape(filter_state.doc_len_max)}"
               class="{input_class}">
      </label>
    </div>
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
        indicator = _render_sort_indicator(active=sort == key, direction=direction)
        query_payload = state_payload(result=result, sort=key, direction=next_direction, filter_state=filter_state)
        query = urlencode(query_payload, doseq=True)
        justify = "justify-end" if align == "right" else "justify-start"
        text_align = "text-right" if align == "right" else "text-left"
        th_spacing = f"{_metric_column_width_class(result)} px-1 normal-case" if is_metric else "px-2 uppercase"
        sticky = _sticky_head_class(key)
        label_class = "min-w-0 text-left leading-tight" if is_metric else "text-left"
        label_attrs = (
            f' data-metric-column-full-name="{escape(full_metric_name, quote=True)}"' if is_metric else ""
        )
        if is_metric:
            label_attrs += (
                f' data-tooltip="{escape(_metric_column_tooltip(label=label, full_metric_name=full_metric_name, result=result), quote=True)}"'
                ' data-tooltip-placement="left"'
                f' aria-label="{escape(_metric_column_tooltip(label=label, full_metric_name=full_metric_name, result=result), quote=True)}"'
            )
        doc_metric_name = result.metric_column_doc_keys.get(full_metric_name, full_metric_name)
        doc = (
            benchmark_docs.task_doc(view_name=result.view_name, metric_column=doc_metric_name)
            if benchmark_docs is not None and is_metric
            else None
        )
        doc_trigger = _render_doc_summary_trigger(doc=doc, label=f"{label} overview") if doc is not None else ""
        if is_metric:
            group_label, task_label = _metric_column_header_parts(label)
            if task_label:
                header_content = f"""
                 <span class="doc-label-group block w-full min-w-0" data-doc-label-group="metric">
                   <span class="{label_class} tooltip-trigger cursor-pointer"{label_attrs}>
                     <span class="block w-full truncate">{escape(group_label)}</span>
                     <span class="inline-flex max-w-full items-center gap-1">
                       <button type="button" class="inline-flex min-w-0 items-center gap-0.5 text-left hover:text-cyan-700"
                               hx-get="{_leaderboard_url(query)}" hx-push-url="{_page_url(query_payload)}"
                               {_leaderboard_control_hx_attrs()}>
                         <span class="block max-w-full truncate font-normal text-zinc-500">{escape(task_label)}</span>{indicator}
                       </button>{doc_trigger}
                     </span>
                   </span>
                 </span>"""
            else:
                header_content = f"""
                 <span class="doc-label-group inline-flex w-full min-w-0 items-center gap-1" data-doc-label-group="metric">
                   <button type="button" class="inline-flex min-w-0 items-center gap-0.5 {justify} text-left hover:text-cyan-700"
                           hx-get="{_leaderboard_url(query)}" hx-push-url="{_page_url(query_payload)}"
                           {_leaderboard_control_hx_attrs()}>
                     <span class="{label_class} block max-w-full truncate tooltip-trigger cursor-pointer"{label_attrs}>{escape(group_label)}</span>{indicator}
                   </button>{doc_trigger}
                 </span>"""
        else:
            label_markup = escape(label)
            header_content = f"""
                 <button type="button" class="inline-flex w-full min-w-0 flex-1 items-center gap-0.5 {justify} text-left hover:text-cyan-700"
                         hx-get="{_leaderboard_url(query)}" hx-push-url="{_page_url(query_payload)}"
                         {_leaderboard_control_hx_attrs()}>
                   <span class="{label_class}"{label_attrs}>{label_markup}</span>{indicator}
                 </button>"""
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
    borda_rank_labels = _rank_display_labels((row.model_name, row.borda_rank) for row in result.rows)
    mean_rank_labels = _rank_display_labels((row.model_name, row.mean_rank) for row in result.rows)
    metric_rank_labels = _metric_rank_display_labels(result)
    for row in result.rows:
        hidden = not filter_context.is_visible(row)
        row_class = "leaderboard-row border-t border-zinc-200 odd:bg-white even:bg-zinc-50"
        hidden_attrs = ' hidden data-filter-hidden="true"' if hidden else ""
        mean_cells = _render_mean_cells(result=result, row=row)
        body_rows.append(
            f"""<tr class="{row_class}"{hidden_attrs}>
              {render_model_name_cell(row, model_views[row.model_name])}
              <td class="leaderboard-col-rank px-2 py-1 text-left tabular-nums">{borda_rank_labels[row.model_name]}</td>
              <td class="leaderboard-col-rank px-2 py-1 text-left tabular-nums">{mean_rank_labels[row.model_name]}</td>
              <td class="px-2 py-1 text-left tabular-nums">{_fmt_score(row.borda_score)}</td>
              {mean_cells}
              {_render_metric_cells(result=result, row=row, metric_rank_labels=metric_rank_labels)}
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
            "Variant Label",
            "Variant Category",
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
        "Variant Label",
        "Variant Category",
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
    model_view: ModelCellView,
    metric_headers: dict[str, str],
) -> dict[str, object | None]:
    metadata = model_view.metadata
    record: dict[str, object | None] = {
        "Borda Rank": row.borda_rank,
        "Mean Rank": row.mean_rank,
        "Model Name": model_view.display_name,
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
        "Variant Label": _csv_variant_label(row=row, model_view=model_view),
        "Variant Category": _csv_variant_category(row),
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


def _csv_variant_label(*, row: LeaderboardRow, model_view: ModelCellView) -> str | None:
    if row.embedding_variant_name is None and row.quantization is None:
        return None
    return model_view.variant_label or row.quantization or row.embedding_variant_name


def _csv_variant_category(row: LeaderboardRow) -> str | None:
    if row.embedding_variant_name is None:
        return "quantization" if row.quantization is not None else None
    if _is_sparse_active_dims_variant(row):
        return "sparse active dims"
    category = variant_category(embedding_variant_name=row.embedding_variant_name, quantization=row.quantization)
    labels = []
    if category.truncate:
        labels.append("truncate")
    if category.quantization:
        labels.append("quantization")
    if category.rescore:
        labels.append("rescore")
    return " + ".join(labels) if labels else "other"


def _is_sparse_active_dims_variant(row: LeaderboardRow) -> bool:
    variant_name = row.embedding_variant_name or ""
    return (
        model_type_filter_key(model_name=row.source_model_name or row.model_name, model_type=row.model_type) == "sparse"
        and "sparse_" in variant_name
        and ("max_active_dims" in variant_name or "max_dims" in variant_name)
    )


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


def _render_metric_cells(
    *,
    result: LeaderboardResult,
    row: LeaderboardRow,
    metric_rank_labels: dict[tuple[str, str], str] | None = None,
) -> str:
    if result.show_task_ranks:
        return "".join(
            _render_metric_rank_score_cell(
                result=result,
                row=row,
                column=column,
                metric_rank_labels=metric_rank_labels,
            )
            for column in result.metric_columns
        )
    if result.show_task_z_scores:
        return "".join(
            _render_metric_z_cell(score=row.metric_values.get(column), z_score=row.metric_z_values.get(column))
            for column in result.metric_columns
        )
    values = row.metric_values
    metric_width_class = _metric_column_width_class(result)
    return "".join(
        f"""<td class="{metric_width_class} px-1 py-1 text-left tabular-nums">{_fmt_score(values.get(column))}</td>"""
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
    return (
        '<td class="w-[5.5rem] min-w-[5.5rem] max-w-[5.5rem] px-1 py-1 text-left tabular-nums">'
        f"{_render_score_z_badge(score=score, z_score=z_score)}"
        "</td>"
    )


def _render_metric_rank_score_cell(
    *,
    result: LeaderboardResult,
    row: LeaderboardRow,
    column: str,
    metric_rank_labels: dict[tuple[str, str], str] | None,
) -> str:
    rank_label = _metric_rank_label(row, column, row.metric_rank_values.get(column), metric_rank_labels)
    metric_width_class = _metric_column_width_class(result)
    if not result.show_task_z_scores:
        return f"""<td class="{metric_width_class} px-1 py-1 text-left tabular-nums">{escape(rank_label)}</td>"""
    rank_html = f'<span class="task-rank-label">{escape(f"[{rank_label}]")}</span>' if rank_label else ""
    score_html = _render_score_z_badge(score=row.metric_values.get(column), z_score=row.metric_z_values.get(column))
    return (
        f'<td class="{metric_width_class} px-1 py-1 tabular-nums">'
        '<span class="task-rank-score-cell">'
        f"{rank_html}{score_html}"
        "</span>"
        "</td>"
    )


def _metric_column_width_class(result: LeaderboardResult) -> str:
    if result.show_task_ranks and result.show_task_z_scores:
        return "w-[7rem] min-w-[7rem] max-w-[7rem]"
    if result.show_task_ranks:
        return "w-[5.5rem] min-w-[5.5rem] max-w-[5.5rem]"
    return "w-[5.5rem] min-w-[5.5rem] max-w-[5.5rem]"


def _render_score_z_cell(*, score: float | None, z_score: float | None, cell_class: str) -> str:
    return f'<td class="{cell_class}">{_render_score_z_badge(score=score, z_score=z_score)}</td>'


def _render_score_z_badge(*, score: float | None, z_score: float | None) -> str:
    rounded = _rounded_z_score(z_score)
    if rounded is None:
        z_label = ""
        bucket_class = "task-z-neutral"
    else:
        assert z_score is not None
        z_label = f"{_fmt_z_score(z_score)}σ"
        bucket_class = _z_score_bucket_class(rounded)
    return (
        f'<span class="task-z-score {bucket_class}">'
        f'<span class="task-z-score-value">{escape(_fmt_score(score))}</span>'
        f'<span class="task-z-score-delta">{escape(z_label)}</span>'
        "</span>"
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
    return (
        result.include_quantization_variants
        or result.include_truncate_variants
        or result.include_rescore_variants
        or result.include_other_variants
    )


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
      <details class="filter-detail bg-zinc-50" data-filter-detail="{escape(name, quote=True)}" data-filter-icon="{escape(icon, quote=True)}">
        <summary class="filter-detail-summary flex cursor-pointer list-none items-center px-1.5 py-0.5 text-[0.8125rem] font-medium text-zinc-800">
          <span class="inline-flex items-center gap-1.5">
            <span class="details-chevron inline-flex h-3.5 w-3.5 shrink-0 items-center justify-center text-zinc-500">{_icon_svg("chevron-right")}</span>
            {_icon_svg(icon, class_name="hakari-icon filter-detail-icon shrink-0")}
            <span>{escape(summary)}</span>
          </span>
        </summary>
        <div class="filter-detail-body p-2">
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


def _metric_rank_label(
    row: LeaderboardRow,
    column: str,
    value: float | None,
    metric_rank_labels: dict[tuple[str, str], str] | None,
) -> str:
    if value is None:
        return ""
    if metric_rank_labels is None:
        return _fmt_rank(value)
    return metric_rank_labels.get((row.model_name, column), _fmt_rank(value))


def _metric_rank_display_labels(result: LeaderboardResult) -> dict[tuple[str, str], str]:
    if not result.show_task_ranks:
        return {}
    labels: dict[tuple[str, str], str] = {}
    for column in result.metric_columns:
        column_labels = _rank_display_labels(
            (row.model_name, row.metric_rank_values.get(column))
            for row in result.rows
            if row.metric_rank_values.get(column) is not None
        )
        labels.update({(model_name, column): label for model_name, label in column_labels.items()})
    return labels


def _rank_display_labels(items: Iterable[tuple[str, float | None]]) -> dict[str, str]:
    values_by_key: dict[str, float] = {key: value for key, value in items if value is not None}
    keys_by_value: dict[float, list[str]] = {}
    for key, value in values_by_key.items():
        keys_by_value.setdefault(value, []).append(key)
    labels: dict[str, str] = {}
    for value, keys in keys_by_value.items():
        if len(keys) == 1:
            labels[keys[0]] = _fmt_rank(value)
            continue
        start_rank = int(round(value - ((len(keys) - 1) / 2.0)))
        for key in keys:
            labels[key] = f"T{start_rank}"
    return labels


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
        raw_billions = value / 1_000_000_000
        if raw_billions >= 100:
            billions = math.floor(raw_billions + 0.5)
            return f"{billions}B"
        if raw_billions >= 10:
            billions = math.floor(raw_billions * 10 + 0.5) / 10
            return f"{billions:.1f}B"
        billions = math.floor(raw_billions * 100 + 0.5) / 100
        return f"{billions:.2f}B"
    if value >= 1_000_000:
        millions = math.floor(value / 1_000_000 + 0.5)
        return f"{millions}M"
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


def _metric_column_label(column: str) -> str:
    parts = column.split("::")
    if len(parts) >= 3:
        dataset = parts[-2].rsplit("/", 1)[-1]
        task = parts[-1]
        if dataset == task:
            return dataset
        return f"{dataset}::{task}"
    if len(parts) == 2:
        if parts[0] == parts[1]:
            return parts[0]
        return column
    return column.removeprefix("Nano")


def _metric_column_label_markup(label: str) -> str:
    parts = [part for part in label.split("::") if part]
    if len(parts) <= 1:
        return f'<span class="block w-full truncate">{escape(label)}</span>'
    escaped_parts = [escape(part) for part in parts]
    first, rest = escaped_parts[0], escaped_parts[1:]
    return (
        f'<span class="block w-full truncate">{first}</span>'
        + "".join(f'<span class="block w-full truncate font-normal text-zinc-500">{part}</span>' for part in rest)
    )


def _metric_column_header_parts(label: str) -> tuple[str, str]:
    parts = [part for part in label.split("::") if part]
    if len(parts) >= 3:
        return parts[-2].rsplit("/", 1)[-1], parts[-1]
    if len(parts) == 2:
        return parts[0], "" if parts[0] == parts[1] else parts[1]
    return label, ""


def _metric_column_tooltip(*, label: str, full_metric_name: str, result: LeaderboardResult) -> str:
    if result.selected_score_group is not None:
        group_label = result.selected_score_group.label
        base = (
            f"{group_label} column. Scores are averaged per model over the raw benchmark rows that belong "
            "to this group."
        )
    else:
        base = "Task score column for this benchmark task."
    if full_metric_name == label:
        return f"{base} Full key: {full_metric_name}"
    return f"{base} Display: {label}. Full key: {full_metric_name}"


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
