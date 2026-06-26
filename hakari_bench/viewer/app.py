from __future__ import annotations

from collections.abc import AsyncIterator, Mapping
from contextlib import asynccontextmanager
import csv
from datetime import datetime, timezone
from functools import lru_cache
import hashlib
from html import escape
from io import StringIO
import json
import math
import os
from pathlib import Path
import re
from typing import Iterable, Sequence, TypedDict, cast
from urllib.parse import quote, urlencode

import duckdb
from pydantic import BaseModel, ConfigDict

from hakari_bench.viewer.config import (
    CLEAR_SCOPE_NAME,
    CUSTOM_SCOPE_NAME,
    ScoreAggregation,
    ViewerConfig,
    benchmark_name_from_selection_key,
    benchmark_selection_key,
    load_viewer_config,
    split_benchmark_selection_key,
)
from hakari_bench.viewer.docs import BenchmarkDoc, BenchmarkDocs, DocsPageChrome, render_docs_index_page, render_markdown_page
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
from hakari_bench.viewer.model_types import is_bm25_model, model_type_filter_key
from hakari_bench.viewer.observability import timed_operation
from hakari_bench.viewer.state import (
    FilterState,
    PLOT_AXIS_FIELDS,
    PLOT_ENCODING_FIELDS,
    PLOT_NONE_FIELD,
    PLOT_SCORE_FIELDS,
    QueryState,
    active_filter_hidden_fields,
    filter_state_from_query,
    normalize_query_state,
    optional_query_string,
    parameter_bounds,
    query_values,
    query_string,
    state_payload,
    task_length_bounds,
)
from hakari_bench.viewer.store import DuckDbSyncStatus, LocalDuckDbStore
from hakari_bench.viewer.summary import ViewerSummary
from hakari_bench.viewer.sql import table_columns, table_exists
from hakari_bench.viewer.variant_display import (
    is_sparse_dims_variant_name,
    variant_category,
    variant_display_flags_from_query,
)

ASSETS_DIR = Path(__file__).with_name("assets")
DEFAULT_FRAME_ANCESTORS = "https://huggingface.co https://*.huggingface.co"
_FRAME_ANCESTOR_TOKEN = re.compile(
    r"^(?:'self'|'none'|\*|(?:https?://)?(?:\*\.)?[A-Za-z0-9.-]+(?::\d+)?)$"
)
SECURITY_HEADERS = {
    "X-Content-Type-Options": "nosniff",
    "Referrer-Policy": "strict-origin-when-cross-origin",
    "Permissions-Policy": "camera=(), microphone=(), geolocation=(), payment=(), usb=()",
}
FOOTER_QUERY_TABLES = {"meta_database"}
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
    "chart-scatter": '<path d="M3 3v18h18"/><circle cx="7.5" cy="7.5" r="1"/><circle cx="18.5" cy="5.5" r="1"/><circle cx="11.5" cy="13.5" r="1"/><circle cx="17.5" cy="17.5" r="1"/>',
    "chevron-right": '<path d="m9 18 6-6-6-6"/>',
    "circle-help": (
        '<circle cx="12" cy="12" r="10"/>'
        '<path d="M9.09 9a3 3 0 0 1 5.83 1c0 2-3 3-3 3"/>'
        '<path d="M12 17h.01"/>'
    ),
    "cpu": '<rect width="16" height="16" x="4" y="4" rx="2"/><path d="M9 9h6v6H9z"/><path d="M9 1v3"/><path d="M15 1v3"/><path d="M9 20v3"/><path d="M15 20v3"/><path d="M20 9h3"/><path d="M20 14h3"/><path d="M1 9h3"/><path d="M1 14h3"/>',
    "database": '<ellipse cx="12" cy="5" rx="9" ry="3"/><path d="M3 5v14c0 1.7 4 3 9 3s9-1.3 9-3V5"/><path d="M3 12c0 1.7 4 3 9 3s9-1.3 9-3"/>',
    "eraser": '<path d="m7 21-4.3-4.3c-1-1-1-2.5 0-3.4l9.6-9.6c1-1 2.5-1 3.4 0l5.6 5.6c1 1 1 2.5 0 3.4L13 21"/><path d="M22 21H7"/><path d="m5 11 9 9"/>',
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
    "github": (
        '<path d="M15 22v-4a4.8 4.8 0 0 0-1-3.5c3 0 6-2 6-5.5a5.4 5.4 0 0 0-1-3.5c.28-1.15.28-2.35 0-3.5 0 0-1 0-3 1.5a13.38 13.38 0 0 0-8 0C6 2 5 2 5 2c-.3 1.15-.3 2.35 0 3.5A5.4 5.4 0 0 0 4 9c0 3.5 3 5.5 6 5.5-.39.49-.68 1.05-.85 1.65-.17.6-.22 1.23-.15 1.85v4"/>'
        '<path d="M9 18c-4.51 2-5-2-7-2"/>'
    ),
    "hakari-bench": (
        '<circle cx="12" cy="5" r="2"/>'
        '<path d="M12 7v11"/>'
        '<path d="M7 21h10"/>'
        '<path d="M9 18h6"/>'
        '<path d="M5 10c2.7 0 5-1.1 7-3 2 1.9 4.3 3 7 3"/>'
        '<path d="m5 10-2 6h4Z"/>'
        '<path d="m19 10-2 6h4Z"/>'
        '<path d="M3 16c.5 2 3.5 2 4 0"/>'
        '<path d="M17 16c.5 2 3.5 2 4 0"/>'
    ),
    "info-simple": '<path d="M12 17v-6"/><path d="M12 7h.01"/>',
    "languages": '<path d="m5 8 6 6"/><path d="m4 14 6-6 2-3"/><path d="M2 5h12"/><path d="M7 2h1"/><path d="m22 22-5-10-5 10"/><path d="M14 18h6"/>',
    "layers": '<path d="m12.83 2.18 8.5 4.73a1 1 0 0 1 0 1.75l-8.5 4.73a1.7 1.7 0 0 1-1.66 0l-8.5-4.73a1 1 0 0 1 0-1.75l8.5-4.73a1.7 1.7 0 0 1 1.66 0Z"/><path d="m22 12.5-9.17 5.1a1.7 1.7 0 0 1-1.66 0L2 12.5"/><path d="m22 17.5-9.17 5.1a1.7 1.7 0 0 1-1.66 0L2 17.5"/>',
    "sigma": '<path d="M18 7V4H6l6 8-6 8h12v-3"/>',
    "list-filter": '<path d="M3 6h18"/><path d="M7 12h10"/><path d="M10 18h4"/>',
    "list-ordered": '<path d="M11 5h10"/><path d="M11 12h10"/><path d="M11 19h10"/><path d="M4 4h1v5"/><path d="M4 9h2"/><path d="M6.5 20H3.4c0-1 2.6-1.925 2.6-3.5a1.5 1.5 0 0 0-2.6-1.02"/>',
    "message-square-text": '<path d="M22 17a2 2 0 0 1-2 2H6.828a2 2 0 0 0-1.414.586l-2.202 2.202A.71.71 0 0 1 2 21.286V5a2 2 0 0 1 2-2h16a2 2 0 0 1 2 2z"/><path d="M7 11h10"/><path d="M7 15h6"/><path d="M7 7h8"/>',
    "moon": '<path d="M12 3a6 6 0 0 0 9 9 9 9 0 1 1-9-9Z"/>',
    "ruler": '<path d="M21.3 15.3a2.4 2.4 0 0 1 0 3.4l-2.6 2.6a2.4 2.4 0 0 1-3.4 0L2.7 8.7a2.4 2.4 0 0 1 0-3.4l2.6-2.6a2.4 2.4 0 0 1 3.4 0Z"/><path d="m14.5 12.5 2-2"/><path d="m11.5 9.5 2-2"/><path d="m8.5 6.5 2-2"/><path d="m17.5 15.5 2-2"/>',
    "rotate-ccw": '<path d="M3 12a9 9 0 1 0 9-9 9.75 9.75 0 0 0-6.74 2.74L3 8"/><path d="M3 3v5h5"/>',
    "scan-eye": '<path d="M3 7V5a2 2 0 0 1 2-2h2"/><path d="M17 3h2a2 2 0 0 1 2 2v2"/><path d="M21 17v2a2 2 0 0 1-2 2h-2"/><path d="M7 21H5a2 2 0 0 1-2-2v-2"/><circle cx="12" cy="12" r="1"/><path d="M18.944 12.33a1 1 0 0 0 0-.66 7.5 7.5 0 0 0-13.888 0 1 1 0 0 0 0 .66 7.5 7.5 0 0 0 13.888 0"/>',
    "shield-check": '<path d="M20 13c0 5-3.5 7.5-7.66 8.95a1 1 0 0 1-.67-.01C7.5 20.5 4 18 4 13V6a1 1 0 0 1 1-1c2 0 4.5-1.2 6.24-2.72a1.17 1.17 0 0 1 1.52 0C14.5 3.8 17 5 19 5a1 1 0 0 1 1 1z"/><path d="m9 12 2 2 4-4"/>',
    "search": '<path d="m21 21-4.34-4.34"/><circle cx="11" cy="11" r="8"/>',
    "shapes": '<path d="M8.3 10a.7.7 0 0 1-.626-1.079L11.4 3a.7.7 0 0 1 1.198-.043L16.3 8.9a.7.7 0 0 1-.572 1.1Z"/><rect x="3" y="14" width="7" height="7" rx="1"/><circle cx="17.5" cy="17.5" r="3.5"/>',
    "sun": '<circle cx="12" cy="12" r="4"/><path d="M12 2v2"/><path d="M12 20v2"/><path d="m4.93 4.93 1.41 1.41"/><path d="m17.66 17.66 1.41 1.41"/><path d="M2 12h2"/><path d="M20 12h2"/><path d="m6.34 17.66-1.41 1.41"/><path d="m19.07 4.93-1.41 1.41"/>',
    "table-properties": '<path d="M15 3v18"/><rect width="18" height="18" x="3" y="3" rx="2"/><path d="M21 9H3"/><path d="M21 15H3"/>',
    "type": '<path d="M12 4v16"/><path d="M4 7V5a1 1 0 0 1 1-1h14a1 1 0 0 1 1 1v2"/><path d="M9 20h6"/>',
}


class _TaskLengthFilterKwargs(TypedDict):
    rank_filtered: bool
    active_params_min: str
    active_params_max: str
    total_params_min: str
    total_params_max: str
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
    benchmark_docs = BenchmarkDocs(
        docs_dir,
        metadata_dir=resolved_docs_metadata_dir,
        group_names=viewer_config.benchmark_names,
    )

    @asynccontextmanager
    async def lifespan(_app: object) -> AsyncIterator[None]:
        store.start_background_sync()
        yield

    app = FastAPI(title="HAKARI-Bench leaderboard", docs_url=None, redoc_url=None, lifespan=lifespan)
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

    @app.get("/favicon.svg")
    def favicon_svg() -> FileResponse:
        return FileResponse(ASSETS_DIR / "favicon-white.svg", media_type="image/svg+xml")

    @app.get("/favicon.ico")
    def favicon_ico() -> FileResponse:
        return FileResponse(ASSETS_DIR / "favicon.png", media_type="image/png")

    @app.get("/hello")
    def hello() -> Response:
        return Response("hello\n", media_type="text/plain; charset=utf-8")

    @app.get("/docs")
    @app.get("/docs/")
    def docs_index_redirect() -> RedirectResponse:
        return RedirectResponse(url="/docs/benchmark-tasks")

    @app.get("/docs/benchmark-tasks", response_class=HTMLResponse)
    def benchmark_docs_index() -> HTMLResponse:
        return HTMLResponse(render_docs_index_page(docs=benchmark_docs.group_docs(), chrome=_docs_page_chrome()))

    @app.get("/docs/benchmark-tasks/{benchmark}", response_class=HTMLResponse)
    def benchmark_doc(benchmark: str) -> HTMLResponse:
        from fastapi import HTTPException

        doc = benchmark_docs.route_doc(benchmark=benchmark)
        if doc is None:
            raise HTTPException(status_code=404, detail="Benchmark documentation not found.")
        return HTMLResponse(render_markdown_page(doc=doc, chrome=_docs_page_chrome()))

    @app.get("/docs/benchmark-tasks/{benchmark}/{task}", response_class=HTMLResponse)
    def benchmark_task_doc(benchmark: str, task: str) -> HTMLResponse:
        from fastapi import HTTPException

        doc = benchmark_docs.route_doc(benchmark=benchmark, task=task)
        if doc is None:
            raise HTTPException(status_code=404, detail="Benchmark task documentation not found.")
        return HTMLResponse(render_markdown_page(doc=doc, chrome=_docs_page_chrome()))

    @app.get("/duckdb-sync-status", response_class=HTMLResponse)
    def duckdb_sync_status(next: str = Query(default="/leaderboard")) -> HTMLResponse:  # noqa: A002
        status = store.sync_status()
        if status.state == "idle":
            status = store.start_background_sync()
        next_url = _safe_duckdb_sync_next_url(next)
        if status.state == "ready" and store.path.exists():
            return HTMLResponse(render_duckdb_sync_complete(next_url=next_url))
        return HTMLResponse(render_duckdb_sync_progress(status, next_url=next_url))

    @app.get("/", response_class=HTMLResponse)
    def index(
        view: str = Query(default=viewer_config.overall.name),
        sort: str = Query(default="borda_score"),
        direction: str = Query(default="desc", pattern="^(asc|desc)$"),
        target: str = Query(default="all", pattern="^(all|reranking|reranking_without_safeguard)$"),
        score: str = Query(default="micro", pattern="^(macro|micro)$"),
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
        other_columns: bool = Query(default=False),
        filters: bool = Query(default=False),
        dim_filter: list[str] | None = Query(default=None),
        quant_filter: list[str] | None = Query(default=None),
        commercial_filter: list[str] | None = Query(default=None),
        model_type_filter: list[str] | None = Query(default=None),
        dtype_filter: list[str] | None = Query(default=None),
        attn_filter: list[str] | None = Query(default=None),
        prompt_filter: list[str] | None = Query(default=None),
        lang_filter: list[str] | None = Query(default=None),
        bench: list[str] | None = Query(default=None),
        model_filter: str = Query(default=""),
        task_filter: str = Query(default=""),
        rank_filtered: bool = Query(default=False),
        active_params_min: str = Query(default=""),
        active_params_max: str = Query(default=""),
        total_params_min: str = Query(default=""),
        total_params_max: str = Query(default=""),
        query_len_min: str = Query(default=""),
        query_len_max: str = Query(default=""),
        doc_len_min: str = Query(default=""),
        doc_len_max: str = Query(default=""),
        result_view: str = Query(default="table", pattern="^(table|chart)$"),
        chart_y: str = Query(default="borda_score"),
        chart_x: str = Query(default="active_parameters"),
        chart_color: str = Query(default="embedding_dim"),
    ) -> str:
        with timed_operation("viewer.http.request", route="index") as request_timing:
            store.start_background_sync()
            initial_query = normalize_query_state(
                viewer_config=viewer_config,
                view=view,
                sort=sort,
                direction=direction,
                target=target,
                score=score,
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
                other_columns=other_columns,
                filters=filters,
                dim_filter=dim_filter,
                quant_filter=quant_filter,
                commercial_filter=commercial_filter,
                model_type_filter=model_type_filter,
                dtype_filter=dtype_filter,
                attn_filter=attn_filter,
                prompt_filter=prompt_filter,
                lang_filter=lang_filter,
                bench=bench,
                model_filter=model_filter,
                task_filter=task_filter,
                rank_filtered=rank_filtered,
                active_params_min=active_params_min,
                active_params_max=active_params_max,
                total_params_min=total_params_min,
                total_params_max=total_params_max,
                query_len_min=query_len_min,
                query_len_max=query_len_max,
                doc_len_min=doc_len_min,
                doc_len_max=doc_len_max,
                result_view=result_view,
                chart_y=chart_y,
                chart_x=chart_x,
                chart_color=chart_color,
            )
            if not task_z_scores:
                initial_query["task_z_scores"] = "0"
            with timed_operation("viewer.render", operation="render_page"):
                content = render_page(
                    viewer_config=viewer_config,
                    duckdb_path=store.path,
                    summary=None,
                    initial_query=initial_query,
                    benchmark_docs=benchmark_docs,
                    database_label="",
                )
            request_timing["view"] = initial_query["view"]
            return content

    def build_leaderboard_result(state_query: QueryState) -> tuple[LeaderboardResult, str, str, FilterState]:
        view = query_string(state_query["view"])
        sort = query_string(state_query["sort"])
        direction = query_string(state_query["direction"])
        target = query_string(state_query.get("target", "all"))
        score = query_string(state_query.get("score", "micro"))
        score_metric = query_string(state_query.get("metric", "ndcg@10"))
        group = optional_query_string(state_query.get("group"))
        selected_benchmarks = tuple(query_values(state_query.get("bench")))
        display_flags = variant_display_flags_from_query(state_query)
        filter_state = filter_state_from_query(state_query)
        params_bounds = parameter_bounds(filter_state)
        length_bounds = task_length_bounds(filter_state)
        service = LeaderboardService(duckdb_path=store.path, config=viewer_config)
        result = service.get_leaderboard(
            view,
            sort=sort,
            direction=cast(SortDirection, direction),
            score_target=cast(ScoreTarget, target),
            score_aggregation=cast(ScoreAggregation, score),
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
            show_other_columns=state_query.get("other_columns") == "1",
            rank_filtered=filter_state.rank_filtered,
            model_filter=filter_state.model_filter,
            task_filter=filter_state.task_filter,
            dim_filters=filter_state.dim_filters if filter_state.filters_active else (),
            quant_filters=filter_state.quant_filters if filter_state.filters_active else (),
            commercial_filters=filter_state.commercial_filters if filter_state.filters_active else (),
            model_type_filters=filter_state.model_type_filters if filter_state.filters_active else (),
            dtype_filters=filter_state.dtype_filters if filter_state.filters_active else (),
            attn_filters=filter_state.attn_filters if filter_state.filters_active else (),
            prompt_filters=filter_state.prompt_filters if filter_state.filters_active else (),
            active_params_min_millions=params_bounds["active_min_millions"],
            active_params_max_millions=params_bounds["active_max_millions"],
            total_params_min_millions=params_bounds["total_min_millions"],
            total_params_max_millions=params_bounds["total_max_millions"],
            query_min_chars=length_bounds["query_min_chars"],
            query_max_chars=length_bounds["query_max_chars"],
            document_min_chars=length_bounds["document_min_chars"],
            document_max_chars=length_bounds["document_max_chars"],
            selected_benchmarks=selected_benchmarks,
        )
        return result, sort, direction, filter_state

    @app.get("/leaderboard", response_class=HTMLResponse)
    def leaderboard(
        view: str = Query(default=viewer_config.overall.name),
        sort: str = Query(default="borda_score"),
        direction: str = Query(default="desc", pattern="^(asc|desc)$"),
        target: str = Query(default="all", pattern="^(all|reranking|reranking_without_safeguard)$"),
        score: str = Query(default="micro", pattern="^(macro|micro)$"),
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
        other_columns: bool = Query(default=False),
        filters: bool = Query(default=False),
        dim_filter: list[str] | None = Query(default=None),
        quant_filter: list[str] | None = Query(default=None),
        commercial_filter: list[str] | None = Query(default=None),
        model_type_filter: list[str] | None = Query(default=None),
        dtype_filter: list[str] | None = Query(default=None),
        attn_filter: list[str] | None = Query(default=None),
        prompt_filter: list[str] | None = Query(default=None),
        lang_filter: list[str] | None = Query(default=None),
        bench: list[str] | None = Query(default=None),
        model_filter: str = Query(default=""),
        task_filter: str = Query(default=""),
        rank_filtered: bool = Query(default=False),
        active_params_min: str = Query(default=""),
        active_params_max: str = Query(default=""),
        total_params_min: str = Query(default=""),
        total_params_max: str = Query(default=""),
        query_len_min: str = Query(default=""),
        query_len_max: str = Query(default=""),
        doc_len_min: str = Query(default=""),
        doc_len_max: str = Query(default=""),
        result_view: str = Query(default="table", pattern="^(table|chart)$"),
        chart_y: str = Query(default="borda_score"),
        chart_x: str = Query(default="active_parameters"),
        chart_color: str = Query(default="embedding_dim"),
    ) -> HTMLResponse:
        with timed_operation("viewer.http.request", route="leaderboard") as request_timing:
            state_query = normalize_query_state(
                viewer_config=viewer_config,
                view=view,
                sort=sort,
                direction=direction,
                target=target,
                score=score,
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
                other_columns=other_columns,
                filters=filters,
                dim_filter=dim_filter,
                quant_filter=quant_filter,
                commercial_filter=commercial_filter,
                model_type_filter=model_type_filter,
                dtype_filter=dtype_filter,
                attn_filter=attn_filter,
                prompt_filter=prompt_filter,
                lang_filter=lang_filter,
                bench=bench,
                model_filter=model_filter,
                task_filter=task_filter,
                rank_filtered=rank_filtered,
                active_params_min=active_params_min,
                active_params_max=active_params_max,
                total_params_min=total_params_min,
                total_params_max=total_params_max,
                query_len_min=query_len_min,
                query_len_max=query_len_max,
                doc_len_min=doc_len_min,
                doc_len_max=doc_len_max,
                result_view=result_view,
                chart_y=chart_y,
                chart_x=chart_x,
                chart_color=chart_color,
            )
            sync_status = store.start_background_sync()
            if _duckdb_sync_blocks_leaderboard(store, sync_status):
                return HTMLResponse(
                    render_duckdb_sync_progress(
                        sync_status,
                        next_url=_leaderboard_url(urlencode(state_query, doseq=True)),
                    )
                )
            result, sort, direction, filter_state = build_leaderboard_result(state_query)
            with timed_operation("viewer.render", operation="render_leaderboard", view=view) as render_timing:
                content = render_leaderboard(
                    result=result,
                    sort=sort,
                    direction=direction,
                    filter_state=filter_state,
                    benchmark_docs=benchmark_docs,
                    result_view=query_string(state_query.get("result_view", "table")),
                    plot_y=query_string(state_query.get("chart_y", "borda_score")),
                    plot_x=query_string(state_query.get("chart_x", "active_parameters")),
                    plot_color=query_string(state_query.get("chart_color", "embedding_dim")),
                )
                content = f"{content}\n{_render_footer_update(store=store)}"
                render_timing["leaderboard_row_count"] = len(result.rows)
            request_timing["view"] = result.view_name
            request_timing["leaderboard_row_count"] = len(result.rows)
            return HTMLResponse(content=content, headers={"HX-Push-Url": f"/?{urlencode(state_query, doseq=True)}"})

    @app.get("/leaderboard.csv")
    def leaderboard_csv(
        view: str = Query(default=viewer_config.overall.name),
        sort: str = Query(default="borda_score"),
        direction: str = Query(default="desc", pattern="^(asc|desc)$"),
        target: str = Query(default="all", pattern="^(all|reranking|reranking_without_safeguard)$"),
        score: str = Query(default="micro", pattern="^(macro|micro)$"),
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
        other_columns: bool = Query(default=False),
        filters: bool = Query(default=False),
        dim_filter: list[str] | None = Query(default=None),
        quant_filter: list[str] | None = Query(default=None),
        commercial_filter: list[str] | None = Query(default=None),
        model_type_filter: list[str] | None = Query(default=None),
        dtype_filter: list[str] | None = Query(default=None),
        attn_filter: list[str] | None = Query(default=None),
        prompt_filter: list[str] | None = Query(default=None),
        lang_filter: list[str] | None = Query(default=None),
        bench: list[str] | None = Query(default=None),
        model_filter: str = Query(default=""),
        task_filter: str = Query(default=""),
        rank_filtered: bool = Query(default=False),
        active_params_min: str = Query(default=""),
        active_params_max: str = Query(default=""),
        total_params_min: str = Query(default=""),
        total_params_max: str = Query(default=""),
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
                score=score,
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
                other_columns=other_columns,
                filters=filters,
                dim_filter=dim_filter,
                quant_filter=quant_filter,
                commercial_filter=commercial_filter,
                model_type_filter=model_type_filter,
                dtype_filter=dtype_filter,
                attn_filter=attn_filter,
                prompt_filter=prompt_filter,
                lang_filter=lang_filter,
                bench=bench,
                model_filter=model_filter,
                task_filter=task_filter,
                rank_filtered=rank_filtered,
                active_params_min=active_params_min,
                active_params_max=active_params_max,
                total_params_min=total_params_min,
                total_params_max=total_params_max,
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


def _duckdb_sync_blocks_leaderboard(store: LocalDuckDbStore, status: DuckDbSyncStatus) -> bool:
    if store.location.hf_source is None and store.location.source_path is None:
        return False
    if store.path.exists():
        return False
    if status.state == "error":
        return True
    return status.active


def _safe_duckdb_sync_next_url(next_url: str) -> str:
    if next_url == "/leaderboard" or next_url.startswith("/leaderboard?"):
        return next_url
    return "/leaderboard"


def _content_security_policy() -> str:
    frame_ancestors = _frame_ancestors()
    return "; ".join(
        [
            "default-src 'self'",
            "script-src 'self'",
            "style-src 'self'",
            "img-src 'self' data:",
            "connect-src 'self'",
            "object-src 'none'",
            "frame-src 'none'",
            "form-action 'self'",
            "base-uri 'none'",
            f"frame-ancestors {frame_ancestors}",
        ]
    )


def _frame_ancestors() -> str:
    value = os.environ.get("HAKARI_BENCH_VIEWER_FRAME_ANCESTORS", DEFAULT_FRAME_ANCESTORS)
    tokens = value.split()
    if not tokens or not all(_FRAME_ANCESTOR_TOKEN.match(token) for token in tokens):
        return DEFAULT_FRAME_ANCESTORS
    return " ".join(tokens)


def render_page(
    *,
    viewer_config: ViewerConfig,
    duckdb_path: Path,
    summary: ViewerSummary | None = None,
    initial_query: QueryState | None = None,
    benchmark_docs: BenchmarkDocs | None = None,
    database_label: str = "",
) -> str:
    query = urlencode(initial_query or {"view": viewer_config.overall.name, "sort": "borda_score", "direction": "desc"}, doseq=True)
    css_url = _asset_url("app.css")
    favicon_svg_url = _asset_url("favicon-white.svg")
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
  <link rel="icon" type="image/svg+xml" href="{favicon_svg_url}">
  <link rel="icon" type="image/png" href="{favicon_url}">
  <meta name="htmx-config" content='{{"allowEval":false,"allowScriptTags":false,"includeIndicatorStyles":false}}'>
  <script src="{htmx_url}"></script>
  <script src="{viewer_js_url}" defer></script>
</head>
<body class="bg-zinc-50 text-zinc-950">
  <main class="mx-auto max-w-[1600px] px-4 pt-2 pb-4 sm:px-6">
    <header class="mb-2">
      <div class="flex items-center justify-between gap-3">
        <h1 class="flex min-w-0 items-center gap-1.5 text-sm text-zinc-600">
          <a id="hakari-home-link" href="/" class="inline-flex min-w-0 items-center gap-1.5 hover:text-cyan-700" aria-label="Refresh HAKARI-Bench leaderboard">
            {_icon_svg("hakari-bench", class_name="hakari-icon section-heading-icon shrink-0")}
            <span>HAKARI-Bench leaderboard</span>
          </a>
        </h1>
        {header_actions}
      </div>
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
         class="leaderboard-loading-toast fixed bottom-4 right-4 z-50 border border-zinc-300 bg-white px-4 py-3 text-sm font-medium text-zinc-800 shadow-sm"
         role="status" aria-live="polite" aria-atomic="true">
      <span class="loading-spinner" aria-hidden="true"></span>
      <span>Loading leaderboard...</span>
    </div>
    """


def render_duckdb_sync_progress(status: DuckDbSyncStatus, *, next_url: str) -> str:
    progress_percent = status.progress_percent
    progress_value = "" if progress_percent is None else f' value="{progress_percent:.0f}" max="100"'
    progress_label = _duckdb_sync_progress_label(status)
    error_html = (
        f'<p class="mt-1 text-xs text-amber-800 [overflow-wrap:anywhere]">{escape(status.error)}</p>'
        if status.error
        else ""
    )
    return f"""
    <div id="duckdb-sync-progress"
         class="leaderboard-initial-loading duckdb-sync-loading border border-zinc-200 bg-white text-sm font-medium text-zinc-700"
         role="status" aria-live="polite" aria-atomic="true"
         hx-get="/duckdb-sync-status?next={quote(next_url, safe='')}"
         hx-trigger="every 1s"
         hx-target="#leaderboard-panel"
         hx-swap="innerHTML">
      <div class="duckdb-sync-content">
        <span class="loading-spinner" aria-hidden="true"></span>
        <span>{escape(status.message)}</span>
        <progress class="duckdb-sync-progress" aria-label="DuckDB download progress"{progress_value}></progress>
        <span class="duckdb-sync-progress-label text-xs text-zinc-500">{escape(progress_label)}</span>
        {error_html}
      </div>
    </div>
    """


def render_duckdb_sync_complete(*, next_url: str) -> str:
    return f"""
    <div id="duckdb-sync-complete"
         class="leaderboard-initial-loading border border-zinc-200 bg-white text-sm font-medium text-zinc-700"
         role="status" aria-live="polite" aria-atomic="true"
         hx-get="{escape(next_url, quote=True)}"
         hx-trigger="load"
         hx-target="#leaderboard-panel"
         hx-swap="innerHTML">
      <span class="loading-spinner" aria-hidden="true"></span>
      <span>Loading leaderboard...</span>
    </div>
    """


def _duckdb_sync_progress_label(status: DuckDbSyncStatus) -> str:
    percent = status.progress_percent
    if status.downloaded_bytes is None:
        return "Preparing download..."
    downloaded = _fmt_bytes(status.downloaded_bytes)
    if status.total_bytes is None:
        return f"{downloaded} downloaded"
    label = f"{downloaded} / {_fmt_bytes(status.total_bytes)}"
    if percent is not None:
        label = f"{label} ({percent:.1f}%)"
    return label


def _fmt_bytes(value: int) -> str:
    units = ("B", "KiB", "MiB", "GiB")
    amount = float(value)
    for unit in units:
        if amount < 1024 or unit == units[-1]:
            if unit == "B":
                return f"{int(amount)} {unit}"
            return f"{amount:.1f} {unit}"
        amount /= 1024
    return f"{value} B"


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


def _render_github_link() -> str:
    return f"""<a id="hakari-github-link" href="https://github.com/hakari-bench/hakari-bench" target="_blank" rel="noopener noreferrer" class="theme-toggle grid h-8 w-8 shrink-0 place-items-center border"
          aria-label="Open hakari-bench/hakari-bench on GitHub" title="Open hakari-bench/hakari-bench on GitHub">
          {_icon_svg("github", class_name="hakari-icon")}
        </a>"""


def _render_header_actions() -> str:
    return f"""<div class="flex shrink-0 items-center gap-2">
          {_render_github_link()}
          {_render_docs_link()}
          {_render_theme_toggle()}
        </div>"""


def _render_docs_header() -> str:
    return f"""<header class="mb-5 flex items-center justify-between gap-3">
          <a href="/" class="docs-brand flex min-w-0 items-center gap-1.5 text-sm font-medium text-zinc-600" aria-label="Back to HAKARI-Bench leaderboard">
            {_icon_svg("hakari-bench", class_name="hakari-icon section-heading-icon shrink-0")}
            <span>HAKARI-Bench</span>
          </a>
          <div class="flex shrink-0 items-center gap-2">
            {_render_github_link()}
            {_render_theme_toggle()}
          </div>
        </header>"""


def _docs_page_chrome() -> DocsPageChrome:
    return DocsPageChrome(
        css_url=_asset_url("app.css"),
        viewer_js_url=_asset_url("viewer.js"),
        favicon_svg_url=_asset_url("favicon-white.svg"),
        favicon_png_url=_asset_url("favicon.png"),
        header_html=_render_docs_header(),
    )


def _render_page_footer(*, latest_update: str, database_label: str, swap_oob: bool = False) -> str:
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
    oob_attr = ' hx-swap-oob="outerHTML"' if swap_oob else ""
    return f"""<footer id="hakari-page-footer" class="mx-auto max-w-[1600px] border-t border-zinc-200 px-4 py-2 text-[11px] text-zinc-500 sm:px-6"{oob_attr}>
    <div class="flex min-w-0 justify-end">
      {meta}
    </div>
  </footer>"""


def _render_footer_update(*, store: LocalDuckDbStore) -> str:
    return _render_page_footer(
        latest_update=_fetch_database_latest_update_label(store.path),
        database_label=_database_footer_label(store),
        swap_oob=True,
    )


def _database_footer_label(store: LocalDuckDbStore) -> str:
    if store.location.hf_source is not None:
        return f"database: remote / {_sha1_prefix(store.path)}"
    return f"database: local / {store.path}"


def _fetch_database_latest_update_label(duckdb_path: Path) -> str:
    if not duckdb_path.exists():
        return ""
    try:
        with timed_operation("viewer.duckdb.connection", operation="fetch_footer_latest_update"):
            con = duckdb.connect(str(duckdb_path), read_only=True)
    except (duckdb.Error, OSError):
        return ""
    try:
        if not table_exists(con, "meta_database", allowed_tables=FOOTER_QUERY_TABLES):
            return ""
        columns = table_columns(con, "meta_database", allowed_tables=FOOTER_QUERY_TABLES)
        if "built_at_utc" not in columns:
            return ""
        with timed_operation("viewer.duckdb.query", operation="fetch_footer_latest_update") as timing:
            row = con.execute("SELECT max(built_at_utc) FROM meta_database").fetchone()
            timing["row_count"] = 1 if row is not None else 0
    except duckdb.Error:
        return ""
    finally:
        con.close()
    value = row[0] if row is not None else None
    return _latest_update_label(str(value) if value else None)


def _sha1_prefix(path: Path, *, length: int = 12) -> str:
    if not path.exists():
        return "unavailable"
    digest = hashlib.sha1(usedforsecurity=False)
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
    return f"""
<dialog id="doc-summary-modal" class="hakari-modal">
  <form method="dialog">
    <div class="hakari-modal-header">
      <h3 class="hakari-modal-title">
        {_icon_svg("book-open", class_name="hakari-icon")}
        <span id="doc-summary-heading" class="break-all">Benchmark documentation</span>
      </h3>
      <button type="submit" class="hakari-modal-close">Close</button>
    </div>
  </form>
  <div class="hakari-modal-body">
    <p id="doc-summary-description" class="hakari-modal-text text-sm"></p>
    <p class="mt-3 text-sm">
      <a id="doc-summary-link" class="hakari-modal-link" href="#" target="_blank" rel="noopener noreferrer">Read the benchmark overview</a>
    </p>
  </div>
</dialog>
"""


def render_help_summary_modal() -> str:
    return f"""
<dialog id="help-summary-modal" class="hakari-modal">
  <form method="dialog">
    <div class="hakari-modal-header">
      <h3 class="hakari-modal-title">
        {_icon_svg("circle-help", class_name="hakari-icon")}
        <span id="help-summary-heading" class="break-all">Help</span>
      </h3>
      <button type="submit" class="hakari-modal-close">Close</button>
    </div>
  </form>
  <div class="hakari-modal-body">
    <p id="help-summary-short" class="hakari-modal-lead text-sm"></p>
    <p id="help-summary-details" class="hakari-modal-text text-sm"></p>
    <div id="help-summary-table-container" class="mt-3 overflow-x-auto" hidden></div>
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


def _render_help_tooltip(
    title: str,
    summary: str | None = None,
    details: str | None = None,
    *,
    table_rows: list[dict[str, str]] | None = None,
) -> str:
    summary = summary or _first_sentence(title)
    details = details or title
    table_attr = (
        f' data-help-table="{escape(json.dumps(table_rows, separators=(",", ":")), quote=True)}"'
        if table_rows
        else ""
    )
    return f"""<button type="button"
                    class="help-summary-trigger inline-flex h-3.5 w-3.5 shrink-0 cursor-pointer items-center justify-center rounded-full border border-zinc-300 text-[9px] leading-none text-zinc-600 hover:border-cyan-600 hover:text-cyan-700"
                    data-help-title="{escape(title, quote=True)}"
                    data-help-summary="{escape(summary, quote=True)}"
                    data-help-details="{escape(details, quote=True)}"
                    {table_attr}
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
    result_view: str = "table",
    plot_y: str = "borda_score",
    plot_x: str = "active_parameters",
    plot_size: str = "embedding_dim",
    plot_color: str = "embedding_dim",
) -> str:
    filter_state = filter_state or FilterState()
    filter_context = row_filter_context(result.rows, filter_state)
    shown_count = visible_row_count(result.rows, filter_context)
    csv_query = urlencode(state_payload(result=result, sort=sort, direction=direction, filter_state=filter_state), doseq=True)
    mode_icon, mode_label = _score_target_display(result.score_target)
    result_view = result_view if result_view in {"table", "chart"} else "table"
    plot_state = _plot_state_query(
        result_view=result_view,
        plot_y=plot_y,
        plot_x=plot_x,
        plot_size=plot_size,
        plot_color=plot_color,
    )
    data_surface = (
        render_leaderboard_plot(
            result=result,
            filter_context=filter_context,
            sort=sort,
            direction=direction,
            filter_state=filter_state,
            plot_y=plot_y,
            plot_x=plot_x,
            plot_size=plot_size,
            plot_color=plot_color,
        )
        if result_view == "chart"
        else f"""
  <div class="leaderboard-table-scroll table-shell overflow-x-auto bg-white">
    <table class="leaderboard-table min-w-full border-collapse text-[0.8125rem]">
      {render_table_head(result=result, sort=sort, direction=direction, filter_state=filter_state, benchmark_docs=benchmark_docs)}
      {render_table_body(result=result, filter_context=filter_context)}
    </table>
  </div>"""
    )
    return f"""
<div>
  {render_tabs(result=result, sort=sort, direction=direction, filter_state=filter_state, filter_context=filter_context, benchmark_docs=benchmark_docs, plot_state=plot_state)}
  <div class="mb-2 flex flex-wrap items-center justify-between gap-2 text-sm text-zinc-600" data-shown-count="{shown_count}">
    <div class="inline-flex flex-wrap items-center gap-x-2 gap-y-1">
      {render_result_view_tabs(result=result, sort=sort, direction=direction, filter_state=filter_state, result_view=result_view, plot_y=plot_y, plot_x=plot_x, plot_size=plot_size, plot_color=plot_color)}
      <span class="inline-flex items-center gap-1 font-medium text-zinc-600">
        {_icon_svg("database", class_name="hakari-icon h-3.5 w-3.5 shrink-0")}
        <span>{escape(result.view_label)}</span>
      </span>
      <span class="text-zinc-400">/</span>
      <span class="inline-flex items-center gap-1 text-zinc-600">
        {_icon_svg(mode_icon, class_name="hakari-icon h-3.5 w-3.5 shrink-0")}
        <span>{escape(mode_label)}</span>
      </span>
      <span class="text-zinc-400">/</span>
      {_render_status_count_buttons(result=result, shown_count=shown_count)}
    </div>
    <a class="inline-flex items-center gap-1 border border-zinc-300 bg-zinc-50 px-2 py-0.5 text-xs font-medium text-zinc-800 underline-offset-2 hover:border-cyan-600 hover:text-cyan-700"
       href="{_csv_url(csv_query)}" aria-label="Download visible leaderboard as CSV">
      {_icon_svg("file-spreadsheet", class_name="hakari-icon h-3.5 w-3.5")}
      <span>Download CSV</span>
    </a>
  </div>
  {data_surface}
  {_render_count_breakdown_modal(result=result, filter_context=filter_context, benchmark_docs=benchmark_docs)}
  {render_model_detail_modal()}
  {render_doc_summary_modal()}
  {render_help_summary_modal()}
</div>
"""


def _render_status_count_buttons(*, result: LeaderboardResult, shown_count: int) -> str:
    return f"""
      <span class="inline-flex items-center gap-1">
        <button type="button" class="leaderboard-status-count-trigger underline underline-offset-2 hover:text-cyan-700" data-count-breakdown-trigger="shown">{shown_count} shown</button>
        <span class="text-zinc-400">/</span>
        <button type="button" class="leaderboard-status-count-trigger underline underline-offset-2 hover:text-cyan-700" data-count-breakdown-trigger="complete">{len(result.rows)} complete models</button>
        <span class="text-zinc-400">/</span>
        <button type="button" class="leaderboard-status-count-trigger underline underline-offset-2 hover:text-cyan-700" data-count-breakdown-trigger="tasks">{result.expected_tasks} tasks</button>
      </span>
    """


def _render_count_breakdown_modal(
    *,
    result: LeaderboardResult,
    filter_context: FilterContext,
    benchmark_docs: BenchmarkDocs | None,
) -> str:
    visible_rows = [row for row in result.rows if filter_context.is_visible(row)]
    model_views = model_cell_views(result.rows)
    return f"""
<dialog id="count-breakdown-modal" class="hakari-modal hakari-count-modal">
  <form method="dialog">
    <div class="hakari-modal-header">
      <h3 class="hakari-modal-title">
        {_icon_svg("activity", class_name="hakari-icon")}
        <span id="count-breakdown-title">Result breakdown</span>
      </h3>
      <button type="submit" class="hakari-modal-close">Close</button>
    </div>
  </form>
  <div class="hakari-modal-body">
    <div class="grid gap-3">
      {_render_count_breakdown_section(
          section_id="count-breakdown-shown",
          title="Visible rows",
          count=len(visible_rows),
          description="Rows currently visible after the selected result set and all active text, facet, and range filters.",
          rows=visible_rows,
          model_views=model_views,
      )}
      {_render_count_breakdown_section(
          section_id="count-breakdown-complete",
          title="Complete models",
          count=len(result.rows),
          description="Complete rows for the selected evaluation mode, benchmark scope, task facets, variant display, and pre-ranking range filters before row visibility filters.",
          rows=result.rows,
          model_views=model_views,
      )}
      {_render_task_breakdown_section(result=result, benchmark_docs=benchmark_docs)}
    </div>
  </div>
</dialog>
"""


def _render_count_breakdown_section(
    *,
    section_id: str,
    title: str,
    count: int,
    description: str,
    rows: list[LeaderboardRow],
    model_views: dict[str, ModelCellView],
) -> str:
    section_key = section_id.removeprefix("count-breakdown-")
    return f"""
      <section id="{section_id}" data-count-breakdown-section="{escape(section_key, quote=True)}" data-count-breakdown-title="{escape(title, quote=True)}" hidden class="pt-2">
        <h4 class="font-semibold text-zinc-900">{escape(title)}: {count}</h4>
        <p class="mt-1 text-sm text-zinc-600">{escape(description)}</p>
        {_render_status_model_list(rows=rows, model_views=model_views)}
      </section>
    """


def _render_status_model_list(*, rows: list[LeaderboardRow], model_views: dict[str, ModelCellView]) -> str:
    if not rows:
        return '<p class="mt-2 text-sm text-zinc-500">No models.</p>'
    items = []
    for row in rows:
        model_view = model_views.get(row.model_name)
        metadata = model_view.metadata if model_view is not None else {"model_name": row.model_name}
        metadata_json = escape(json.dumps(metadata, ensure_ascii=False, separators=(",", ":")), quote=True)
        items.append(
            f"""<li class="border-t border-zinc-200 py-1">
              <button type="button" class="model-detail-trigger break-all text-left font-mono text-sm underline underline-offset-2 hover:text-cyan-700"
                      data-model-metadata="{metadata_json}">{escape(row.model_name)}</button>
            </li>"""
        )
    return f"""<ul class="mt-2 max-h-72 overflow-auto">{''.join(items)}</ul>"""


def _render_task_breakdown_section(*, result: LeaderboardResult, benchmark_docs: BenchmarkDocs | None) -> str:
    task_items = []
    for task in result.task_breakdowns:
        doc = (
            benchmark_docs.task_doc(view_name=result.view_name, metric_column=task.doc_key)
            if benchmark_docs is not None
            else None
        )
        label = doc.title if doc is not None else task.label
        if doc is not None:
            task_items.append(
                f"""<li class="border-t border-zinc-200 py-1">
                  <a class="count-breakdown-task-link underline underline-offset-2 hover:text-cyan-700" href="{escape(doc.url, quote=True)}" target="_blank" rel="noopener noreferrer">{escape(label)}</a>
                </li>"""
            )
        else:
            task_items.append(
                f"""<li class="border-t border-zinc-200 py-1 text-zinc-600">{escape(label)}</li>"""
            )
    task_body = (
        f"""<ul class="mt-2 max-h-72 overflow-auto text-sm">{''.join(task_items)}</ul>"""
        if task_items
        else '<p class="mt-2 text-sm text-zinc-500">Task-level breakdown is unavailable for this precomputed summary.</p>'
    )
    return f"""
      <section id="count-breakdown-tasks" data-count-breakdown-section="tasks" data-count-breakdown-title="Tasks" hidden class="pt-2">
        <h4 class="font-semibold text-zinc-900">Tasks: {result.expected_tasks}</h4>
        <p class="mt-1 text-sm text-zinc-600">Tasks in the selected evaluation mode, benchmark scope, task facets, and task-length range filters. Linked tasks have verified local documentation and open in a new tab.</p>
        {task_body}
      </section>
    """


PLOT_SCORE_OPTIONS = {
    "borda_score": ("Borda Score", "Borda score"),
    "macro_mean": ("Task Mean (Macro)", "Task Mean (Macro)"),
    "micro_mean": ("Task Mean (Micro)", "Task Mean (Micro)"),
}
PLOT_AXIS_OPTIONS = {
    "active_parameters": ("Active Params (log scale)", "Active params"),
    "active_parameters_linear": ("Active Params", "Active params"),
    "total_parameters": ("Total Params (log scale)", "Total params"),
    "total_parameters_linear": ("Total Params", "Total params"),
    "max_seq_length": ("Max Tokens", "Max tokens"),
    "embedding_dim": ("Dims", "Embedding dim"),
    "quantization": ("Quantization", "Quantization"),
    "sparse_query_dims": ("Sparse Query Dims", "Sparse query dims"),
    "sparse_document_dims": ("Sparse Doc Dims", "Sparse doc dims"),
}
PLOT_CHANNEL_OPTIONS = {PLOT_NONE_FIELD: ("None", "None"), **PLOT_AXIS_OPTIONS}
PLOT_LOG_FIELDS = {
    "active_parameters",
    "total_parameters",
    "max_seq_length",
    "embedding_dim",
    "sparse_query_dims",
    "sparse_document_dims",
}
PLOT_POINT_RADIUS = 5.5
PLOT_DIMENSION_GRID_STEP = 128.0
PLOT_DIMENSION_COMPRESSED_MAX = 256.0
PLOT_DIMENSION_COMPRESSED_FRACTION = 0.12
PLOT_DIMENSION_DENSE_TICK_MAX = 1024.0
PLOT_DIMENSION_HIGH_TICKS = (2048.0,)
PLOT_LOG_ZERO_BUCKET_FRACTION = 0.07
PLOT_COLOR_STOPS = ((79, 70, 229), (8, 145, 178), (245, 158, 11))


class _PlotPoint(TypedDict):
    row: LeaderboardRow
    x: float | None
    y: float | None
    color: float | None
    active_parameters: float | None
    total_parameters: float | None
    max_seq_length: float | None
    x_label: str
    y_label: str
    color_label: str


def render_result_view_tabs(
    *,
    result: LeaderboardResult,
    sort: str,
    direction: str,
    filter_state: FilterState | None = None,
    result_view: str = "table",
    plot_y: str = "borda_score",
    plot_x: str = "active_parameters",
    plot_size: str = "embedding_dim",
    plot_color: str = "embedding_dim",
) -> str:
    filter_state = filter_state or FilterState()
    result_view = result_view if result_view in {"table", "chart"} else "table"
    buttons = []
    for value, label, icon in [("table", "Table", "table-properties"), ("chart", "Chart", "chart-scatter")]:
        active = result_view == value
        query_payload = _plot_state_payload(
            result=result,
            sort=sort,
            direction=direction,
            filter_state=filter_state,
            result_view=value,
            plot_y=plot_y,
            plot_x=plot_x,
            plot_size=plot_size,
            plot_color=plot_color,
        )
        query = urlencode(query_payload, doseq=True)
        buttons.append(
            f"""<button type="button" role="tab" aria-selected="{str(active).lower()}" class="inline-flex items-center gap-1 border px-2 py-1 text-[0.8125rem] leading-tight {_control_button_classes(active=active)}"
                  hx-get="{_leaderboard_url(query)}" hx-push-url="{_page_url(query_payload)}"
                  {_leaderboard_control_hx_attrs()}>{_icon_svg(icon, class_name="hakari-icon h-3.5 w-3.5 shrink-0")}<span>{escape(label)}</span></button>"""
        )
    return f"""
      <span class="inline-flex items-center gap-1" role="tablist" aria-label="Result view">{''.join(buttons)}</span>
"""


def render_plot_controls(
    *,
    result: LeaderboardResult,
    sort: str,
    direction: str,
    filter_state: FilterState,
    plot_y: str,
    plot_x: str,
    plot_color: str,
) -> str:
    state_fields = _plot_state_fields(
        result=result,
        sort=sort,
        direction=direction,
        filter_state=filter_state,
        result_view="chart",
    )
    return f"""
    <form id="plot-controls" class="plot-controls flex flex-wrap items-center justify-end gap-2 border border-zinc-200 bg-white p-1.5 text-[0.8125rem] text-zinc-700 shadow-sm"
          hx-get="/leaderboard" hx-push-url="true"
          {_leaderboard_control_hx_attrs()}
          hx-trigger="change, submit">
      {_hidden_inputs(state_fields)}
      {_render_plot_select("chart_y", "Y axis", PLOT_SCORE_OPTIONS, _normalized_plot_score_field(plot_y))}
      {_render_plot_select("chart_x", "X axis", PLOT_AXIS_OPTIONS, _normalized_plot_axis_field(plot_x))}
      {_render_plot_select("chart_color", "Color", PLOT_CHANNEL_OPTIONS, _normalized_plot_channel_field(plot_color, default="embedding_dim"))}
    </form>
"""


def _render_plot_select(name: str, label: str, options: dict[str, tuple[str, str]], selected: str) -> str:
    option_html = "".join(
        f'<option value="{escape(value)}"{" selected" if value == selected else ""}>{escape(option_label)}</option>'
        for value, (option_label, _axis_label) in options.items()
    )
    return f"""
      <label class="inline-flex items-center gap-1">
        <span class="text-xs font-medium text-zinc-700">{escape(label)}</span>
        <select name="{escape(name)}" class="viewer-select border border-zinc-300 bg-white px-2 py-1 text-[0.8125rem] text-zinc-900">
          {option_html}
        </select>
      </label>
"""


def _plot_state_payload(
    *,
    result: LeaderboardResult,
    sort: str,
    direction: str,
    filter_state: FilterState,
    result_view: str,
    plot_y: str,
    plot_x: str,
    plot_size: str,
    plot_color: str,
) -> QueryState:
    payload = state_payload(result=result, sort=sort, direction=direction, filter_state=filter_state)
    if result_view != "table":
        payload["result_view"] = result_view
    plot_y = _normalized_plot_score_field(plot_y)
    plot_x = _normalized_plot_axis_field(plot_x)
    plot_color = _normalized_plot_channel_field(plot_color, default="embedding_dim")
    if plot_y != "borda_score":
        payload["chart_y"] = plot_y
    if plot_x != "active_parameters":
        payload["chart_x"] = plot_x
    if plot_color != "embedding_dim":
        payload["chart_color"] = plot_color
    if "quantization" in {plot_x, plot_color}:
        payload["quantization"] = "1"
    return payload


def _plot_state_fields(
    *,
    result: LeaderboardResult,
    sort: str,
    direction: str,
    filter_state: FilterState,
    result_view: str,
) -> list[tuple[str, str]]:
    payload = state_payload(result=result, sort=sort, direction=direction, filter_state=filter_state)
    payload["result_view"] = result_view
    fields: list[tuple[str, str]] = []
    for key, value in payload.items():
        if isinstance(value, list):
            fields.extend((key, item) for item in value)
        else:
            fields.append((key, value))
    return fields


def _plot_state_query(
    *,
    result_view: str,
    plot_y: str,
    plot_x: str,
    plot_size: str,
    plot_color: str,
) -> QueryState:
    result_view = result_view if result_view in {"table", "chart"} else "table"
    if result_view == "table":
        return {}
    plot_y = _normalized_plot_score_field(plot_y)
    plot_x = _normalized_plot_axis_field(plot_x)
    plot_color = _normalized_plot_channel_field(plot_color, default="embedding_dim")
    payload: QueryState = {"result_view": "chart"}
    if plot_y != "borda_score":
        payload["chart_y"] = plot_y
    if plot_x != "active_parameters":
        payload["chart_x"] = plot_x
    if plot_color != "embedding_dim":
        payload["chart_color"] = plot_color
    if "quantization" in {plot_x, plot_color}:
        payload["quantization"] = "1"
    return payload


def _apply_plot_state(payload: QueryState, plot_state: QueryState | None) -> QueryState:
    if not plot_state:
        return payload
    payload.update(plot_state)
    return payload


def _query_state_fields(payload: QueryState | None) -> list[tuple[str, str]]:
    if not payload:
        return []
    fields: list[tuple[str, str]] = []
    for key, value in payload.items():
        if isinstance(value, list):
            fields.extend((key, item) for item in value)
        else:
            fields.append((key, value))
    return fields


def render_leaderboard_plot(
    *,
    result: LeaderboardResult,
    filter_context: FilterContext | None = None,
    sort: str = "borda_score",
    direction: str = "desc",
    filter_state: FilterState | None = None,
    plot_y: str = "borda_score",
    plot_x: str = "active_parameters",
    plot_size: str = "embedding_dim",
    plot_color: str = "embedding_dim",
) -> str:
    filter_state = filter_state or FilterState()
    filter_context = filter_context or row_filter_context(result.rows, filter_state)
    y_field = _normalized_plot_score_field(plot_y)
    x_field = _normalized_plot_axis_field(plot_x)
    color_field = _normalized_plot_channel_field(plot_color, default="embedding_dim")
    visible_rows = [row for row in result.rows if filter_context.is_visible(row)]
    sparse_embedding_dim = _average_dense_embedding_dim(visible_rows) or _average_dense_embedding_dim(result.rows)
    max_active_parameters = _max_plot_active_parameters(visible_rows) or _max_plot_active_parameters(result.rows)
    max_total_parameters = _max_plot_total_parameters(visible_rows) or _max_plot_total_parameters(result.rows)
    max_seq_length = _max_plot_seq_length(visible_rows) or _max_plot_seq_length(result.rows)
    points: list[_PlotPoint] = [
        _plot_point_values(
            row,
            y_field=y_field,
            x_field=x_field,
            color_field=color_field,
            sparse_embedding_dim=sparse_embedding_dim,
            max_active_parameters=max_active_parameters,
            max_total_parameters=max_total_parameters,
            max_seq_length=max_seq_length,
        )
        for row in visible_rows
    ]
    points = [
        point
        for point in points
        if _plot_point_has_required_values(
            point,
            x_field=x_field,
            color_field=color_field,
        )
    ]
    if not points:
        return '<div class="leaderboard-plot-empty border border-zinc-200 bg-white px-3 py-5 text-center text-zinc-500">No plottable rows found.</div>'
    width = 1100
    height = 560
    left = 82
    right = 138
    top = 26
    bottom = 72
    plot_width = width - left - right
    plot_height = height - top - bottom
    x_log = _plot_field_uses_log(x_field)
    color_log = _plot_field_uses_log(color_field)
    x_values = [
        float(point["x"])
        for point in points
        if point["x"] is not None and (not x_log or float(point["x"]) > 0)
    ]
    y_values = [float(point["y"]) for point in points if point["y"] is not None]
    color_values = [
        float(point["color"])
        for point in points
        if point["color"] is not None and (not color_log or float(point["color"]) > 0)
    ]
    x_has_zero = x_log and any(point["x"] == 0 for point in points)
    x_min, x_max = _plot_extent_for_field(x_values, field=x_field, log=x_log)
    y_min, y_max = _plot_score_extent(y_values, y_field=y_field)
    color_min, color_max = _plot_extent_for_field(color_values, field=color_field, log=color_log)
    grid = _render_plot_grid(
        left=left,
        top=top,
        plot_width=plot_width,
        plot_height=plot_height,
        x_min=x_min,
        x_max=x_max,
        y_min=y_min,
        y_max=y_max,
        x_log=x_log,
        x_has_zero=x_has_zero,
        x_label=PLOT_AXIS_OPTIONS[x_field][0],
        y_label=PLOT_SCORE_OPTIONS[y_field][0],
    )
    circles = []
    model_views = model_cell_views([point["row"] for point in points])
    for point in points:
        x_raw = point["x"]
        y_raw = point["y"]
        if x_raw is None or y_raw is None:
            continue
        x_value = float(x_raw)
        if x_log and x_value < 0:
            continue
        y_value = float(y_raw)
        cx = left + _plot_x_scale(
            x_value,
            min_value=x_min,
            max_value=x_max,
            log=x_log,
            label=PLOT_AXIS_OPTIONS[x_field][0],
            has_zero=x_has_zero,
        ) * plot_width
        cy = top + (1.0 - _plot_scale(y_value, min_value=y_min, max_value=y_max, log=False)) * plot_height
        fill = _plot_color(point["color"], min_value=color_min, max_value=color_max, log=color_log)
        tooltip = _plot_tooltip(point)
        metadata = _plot_model_metadata(point["row"], model_views)
        circles.append(
            f"""<circle class="leaderboard-plot-point tooltip-trigger model-detail-trigger" cx="{cx:.2f}" cy="{cy:.2f}" r="{PLOT_POINT_RADIUS:.2f}" fill="{fill}" data-tooltip="{escape(tooltip, quote=True)}" data-tooltip-hover-only="true" data-tooltip-delay="0" data-model-metadata="{metadata}" tabindex="0" aria-label="{escape(tooltip, quote=True)}"></circle>"""
        )
    legend = (
        ""
        if color_field == PLOT_NONE_FIELD
        else _render_plot_legend(
            x=width - right + 42,
            y=top + 16,
            height=plot_height - 32,
            label=PLOT_AXIS_OPTIONS[color_field][0],
            min_value=color_min,
            max_value=color_max,
            field=color_field,
        )
    )
    plot_controls = render_plot_controls(
        result=result,
        sort=sort,
        direction=direction,
        filter_state=filter_state,
        plot_y=y_field,
        plot_x=x_field,
        plot_color=color_field,
    )
    return f"""
  <div class="leaderboard-plot-shell relative border border-zinc-200 bg-white p-2" data-testid="leaderboard-plot">
    <div class="leaderboard-plot-controls-region" style="position:absolute;right:0.75rem;top:0.75rem;z-index:10;">{plot_controls}</div>
    <div class="leaderboard-plot-mobile-message" role="status">Chart view is available only on wider screens.</div>
    <svg class="leaderboard-plot" viewBox="0 0 {width} {height}" role="img" aria-label="{escape(PLOT_SCORE_OPTIONS[y_field][0])} by {escape(PLOT_AXIS_OPTIONS[x_field][0])}">
      {grid}
      <g>{''.join(circles)}</g>
      {legend}
    </svg>
  </div>
"""


def _plot_point_values(
    row: LeaderboardRow,
    *,
    y_field: str,
    x_field: str,
    color_field: str,
    sparse_embedding_dim: float | None,
    max_active_parameters: float | None,
    max_total_parameters: float | None,
    max_seq_length: float | None,
) -> _PlotPoint:
    active_parameters = _plot_active_parameters(row, fallback=max_active_parameters)
    total_parameters = _plot_total_parameters(row, fallback=max_total_parameters)
    plot_max_seq_length = _plot_max_seq_length(row, fallback=max_seq_length)
    return {
        "row": row,
        "x": _plot_axis_value(
            row,
            x_field,
            sparse_embedding_dim=sparse_embedding_dim,
            active_parameters=active_parameters,
            total_parameters=total_parameters,
            max_seq_length=plot_max_seq_length,
        ),
        "y": _plot_score_value(row, y_field),
        "color": _plot_axis_value(
            row,
            color_field,
            sparse_embedding_dim=sparse_embedding_dim,
            active_parameters=active_parameters,
            total_parameters=total_parameters,
            max_seq_length=plot_max_seq_length,
        ),
        "active_parameters": active_parameters,
        "total_parameters": total_parameters,
        "max_seq_length": plot_max_seq_length,
        "x_label": PLOT_AXIS_OPTIONS[x_field][1],
        "y_label": PLOT_SCORE_OPTIONS[y_field][1],
        "color_label": PLOT_CHANNEL_OPTIONS[color_field][1],
    }


def _plot_point_has_required_values(point: _PlotPoint, *, x_field: str, color_field: str) -> bool:
    if point["x"] is None or point["y"] is None:
        return False
    if x_field == "max_seq_length" and point["x"] is None:
        return False
    if color_field == "max_seq_length" and point["color"] is None:
        return False
    return True


def _plot_score_value(row: LeaderboardRow, field: str) -> float | None:
    if field == "macro_mean":
        return row.macro_mean
    if field == "micro_mean":
        return row.micro_mean
    return row.borda_score


def _plot_axis_value(
    row: LeaderboardRow,
    field: str,
    *,
    sparse_embedding_dim: float | None,
    active_parameters: float | None,
    total_parameters: float | None,
    max_seq_length: float | None,
) -> float | None:
    if field in {"active_parameters", "active_parameters_linear"}:
        return active_parameters
    if field in {"total_parameters", "total_parameters_linear"}:
        return total_parameters
    if field == "max_seq_length":
        return max_seq_length
    if field == "embedding_dim":
        if _is_sparse_or_bm25_row(row):
            return sparse_embedding_dim
        return float(row.embedding_dim) if row.embedding_dim is not None else None
    if field == "quantization":
        return float(_quantization_numeric_value(row.quantization))
    if field == "sparse_query_dims":
        return _sparse_dim_from_variant(row.embedding_variant_name, "query")
    if field == "sparse_document_dims":
        return _sparse_dim_from_variant(row.embedding_variant_name, "document")
    if field == PLOT_NONE_FIELD:
        return 1.0
    return None


def _plot_active_parameters(row: LeaderboardRow, *, fallback: float | None) -> float | None:
    if _plot_unknown_params_as_zero(row):
        return 0.0
    if row.active_parameters is not None:
        return float(row.active_parameters)
    return fallback


def _plot_total_parameters(row: LeaderboardRow, *, fallback: float | None) -> float | None:
    if _plot_unknown_params_as_zero(row):
        return 0.0
    if row.total_parameters is not None:
        return float(row.total_parameters)
    return fallback


def _plot_unknown_params_as_zero(row: LeaderboardRow) -> bool:
    return _is_bm25_row(row) or _is_static_embedding_row(row)


def _is_bm25_row(row: LeaderboardRow) -> bool:
    return is_bm25_model(model_name=row.source_model_name or row.model_name, model_type=row.model_type)


def _is_static_embedding_row(row: LeaderboardRow) -> bool:
    model_name = (row.source_model_name or row.model_name).casefold()
    return model_name.startswith("static-") or "/static-" in model_name or model_name.startswith("static/")


def _max_plot_active_parameters(rows: Iterable[LeaderboardRow]) -> float | None:
    values = [
        float(row.active_parameters)
        for row in rows
        if row.active_parameters is not None and not _plot_unknown_params_as_zero(row)
    ]
    if not values:
        return None
    return max(values)


def _max_plot_total_parameters(rows: Iterable[LeaderboardRow]) -> float | None:
    values = [
        float(row.total_parameters)
        for row in rows
        if row.total_parameters is not None and not _plot_unknown_params_as_zero(row)
    ]
    if not values:
        return None
    return max(values)


def _plot_max_seq_length(row: LeaderboardRow, *, fallback: float | None) -> float | None:
    if row.max_seq_length is not None:
        return float(row.max_seq_length)
    return fallback


def _max_plot_seq_length(rows: Iterable[LeaderboardRow]) -> float | None:
    values = [float(row.max_seq_length) for row in rows if row.max_seq_length is not None]
    if not values:
        return None
    return max(values)


def _quantization_numeric_value(quantization: str | None) -> int:
    if not quantization:
        return 16
    normalized = quantization.casefold()
    if "binary" in normalized or normalized in {"bin", "ubinary"}:
        return 1
    if "int8" in normalized or "uint8" in normalized or "8" in normalized:
        return 8
    return 16


def _average_dense_embedding_dim(rows: Iterable[LeaderboardRow]) -> float | None:
    values = [
        float(row.embedding_dim)
        for row in rows
        if row.embedding_dim is not None and _uses_regular_embedding_dim_for_plot(row)
    ]
    if not values:
        return None
    return sum(values) / len(values)


def _max_dense_embedding_dim(rows: Iterable[LeaderboardRow]) -> float | None:
    values = [
        float(row.embedding_dim)
        for row in rows
        if row.embedding_dim is not None and _uses_regular_embedding_dim_for_plot(row)
    ]
    if not values:
        return None
    return max(values)


def _uses_regular_embedding_dim_for_plot(row: LeaderboardRow) -> bool:
    return not _is_sparse_or_bm25_row(row) and not _is_late_interaction_row(row)


def _is_sparse_or_bm25_row(row: LeaderboardRow) -> bool:
    return model_type_filter_key(model_name=row.source_model_name or row.model_name, model_type=row.model_type) in {
        "bm25",
        "sparse",
    }


def _is_late_interaction_row(row: LeaderboardRow) -> bool:
    return (
        model_type_filter_key(model_name=row.source_model_name or row.model_name, model_type=row.model_type)
        == "late-interaction"
    )


def _sparse_dim_from_variant(embedding_variant_name: str | None, side: str) -> float | None:
    if not embedding_variant_name or not is_sparse_dims_variant_name(embedding_variant_name):
        return None
    normalized = embedding_variant_name.lower()
    patterns = (
        (rf"{side}[^0-9]*(\d+)", rf"{side[0]}[^0-9]*(\d+)"),
        (r"query[^0-9]*(\d+)", r"q[^0-9]*(\d+)"),
    ) if side == "query" else (
        (r"document[^0-9]*(\d+)", r"doc[^0-9]*(\d+)", r"d[^0-9]*(\d+)"),
    )
    for group in patterns:
        for pattern in group:
            match = re.search(pattern, normalized)
            if match:
                return float(match.group(1))
    match = re.search(r"(?:max_active_dims|max_dims)[^0-9]*(\d+)", normalized)
    return float(match.group(1)) if match else None


def _plot_field_uses_log(field: str) -> bool:
    return field in PLOT_LOG_FIELDS


def _plot_extent(
    values: list[float],
    *,
    log: bool,
    pad_fraction: float = 0.04,
    nonnegative: bool = False,
) -> tuple[float, float]:
    values = [value for value in values if math.isfinite(value) and (not log or value > 0)]
    if not values:
        return (1.0, 10.0) if log else (0.0, 1.0)
    minimum = min(values)
    maximum = max(values)
    if minimum == maximum:
        if log:
            return minimum / 2.0, maximum * 2.0
        pad = abs(minimum) * 0.1 or 1.0
        lower = minimum - pad
        upper = maximum + pad
    elif log:
        lower = minimum
        upper = maximum
    else:
        span = maximum - minimum
        lower = minimum - span * pad_fraction
        upper = maximum + span * pad_fraction
    if nonnegative and not log:
        lower = max(0.0, lower)
    return lower, upper


def _plot_extent_for_field(values: list[float], *, field: str, log: bool) -> tuple[float, float]:
    if field == "quantization":
        return 1.0, 16.0
    if values:
        return _plot_extent(values, log=log, nonnegative=True)
    return (1.0, 10.0) if log else (0.0, 1.0)


def _plot_score_extent(values: list[float], *, y_field: str) -> tuple[float, float]:
    finite_values = [value for value in values if math.isfinite(value)]
    if y_field == "borda_score":
        return 0.0, 100.0
    if not finite_values:
        return 0.0, 1.0
    minimum = min(finite_values)
    maximum = max(finite_values)
    return minimum, maximum


def _plot_scale(value: float, *, min_value: float, max_value: float, log: bool) -> float:
    if log:
        value = math.log10(max(value, 1e-9))
        min_value = math.log10(max(min_value, 1e-9))
        max_value = math.log10(max(max_value, 1e-9))
    if max_value == min_value:
        return 0.5
    return min(1.0, max(0.0, (value - min_value) / (max_value - min_value)))


def _plot_x_scale(
    value: float,
    *,
    min_value: float,
    max_value: float,
    log: bool,
    label: str,
    has_zero: bool = False,
) -> float:
    if label == "Dims":
        return _plot_dimension_scale(value, max_value=max_value)
    if has_zero and log:
        if value <= 0:
            return 0.0
        scaled = _plot_scale(value, min_value=min_value, max_value=max_value, log=log)
        return PLOT_LOG_ZERO_BUCKET_FRACTION + scaled * (1.0 - PLOT_LOG_ZERO_BUCKET_FRACTION)
    return _plot_scale(value, min_value=min_value, max_value=max_value, log=log)


def _plot_dimension_scale(value: float, *, max_value: float) -> float:
    value = max(0.0, value)
    max_value = max(value, max_value, PLOT_DIMENSION_COMPRESSED_MAX)
    if max_value <= PLOT_DIMENSION_COMPRESSED_MAX:
        return _plot_scale(value, min_value=0.0, max_value=max_value, log=False)
    if value <= PLOT_DIMENSION_COMPRESSED_MAX:
        return (value / PLOT_DIMENSION_COMPRESSED_MAX) * PLOT_DIMENSION_COMPRESSED_FRACTION
    high_min = math.log10(PLOT_DIMENSION_COMPRESSED_MAX)
    high_max = math.log10(max_value)
    if math.isclose(high_min, high_max, rel_tol=1e-9, abs_tol=1e-9):
        return PLOT_DIMENSION_COMPRESSED_FRACTION
    high_scaled = (math.log10(value) - high_min) / (high_max - high_min)
    return min(
        1.0,
        max(
            0.0,
            PLOT_DIMENSION_COMPRESSED_FRACTION + high_scaled * (1.0 - PLOT_DIMENSION_COMPRESSED_FRACTION),
        ),
    )


def _plot_color(value: object, *, min_value: float, max_value: float, log: bool) -> str:
    if not isinstance(value, (int, float)) or not math.isfinite(float(value)):
        return "rgb(115 120 126 / 0.82)"
    scaled = _plot_scale(float(value), min_value=min_value, max_value=max_value, log=log)
    if scaled <= 0.5:
        local = scaled * 2.0
        start, end = PLOT_COLOR_STOPS[0], PLOT_COLOR_STOPS[1]
    else:
        local = (scaled - 0.5) * 2.0
        start, end = PLOT_COLOR_STOPS[1], PLOT_COLOR_STOPS[2]
    red = round(start[0] + (end[0] - start[0]) * local)
    green = round(start[1] + (end[1] - start[1]) * local)
    blue = round(start[2] + (end[2] - start[2]) * local)
    alpha = 0.88 + scaled * 0.02
    return f"rgb({red} {green} {blue} / {alpha:.2f})"


def _render_plot_grid(
    *,
    left: int,
    top: int,
    plot_width: int,
    plot_height: int,
    x_min: float,
    x_max: float,
    y_min: float,
    y_max: float,
    x_log: bool,
    x_has_zero: bool,
    x_label: str,
    y_label: str,
) -> str:
    x_ticks = _plot_x_ticks(x_min, x_max, log=x_log, label=x_label)
    if x_has_zero:
        x_ticks = [0.0, *x_ticks]
    y_ticks = _plot_ticks(y_min, y_max, log=False)
    parts = [f'<rect x="{left}" y="{top}" width="{plot_width}" height="{plot_height}" class="plot-frame"></rect>']
    for tick in x_ticks:
        x = left + _plot_x_scale(
            tick,
            min_value=x_min,
            max_value=x_max,
            log=x_log,
            label=x_label,
            has_zero=x_has_zero,
        ) * plot_width
        parts.append(f'<line x1="{x:.2f}" y1="{top}" x2="{x:.2f}" y2="{top + plot_height}" class="plot-grid-line"></line>')
        tick_label = _fmt_plot_x_tick(tick, x_label, log=x_log)
        parts.append(f'<text x="{x:.2f}" y="{top + plot_height + 24}" class="plot-axis-tick" text-anchor="middle">{escape(tick_label)}</text>')
    for tick in y_ticks:
        y = top + (1.0 - _plot_scale(tick, min_value=y_min, max_value=y_max, log=False)) * plot_height
        parts.append(f'<line x1="{left}" y1="{y:.2f}" x2="{left + plot_width}" y2="{y:.2f}" class="plot-grid-line"></line>')
        parts.append(f'<text x="{left - 12}" y="{y + 4:.2f}" class="plot-axis-tick" text-anchor="end">{escape(_fmt_plot_score_tick(tick))}</text>')
    parts.append(f'<text x="{left + plot_width / 2:.2f}" y="{top + plot_height + 56}" class="plot-axis-label" text-anchor="middle">{escape(x_label)}</text>')
    parts.append(f'<text x="24" y="{top + plot_height / 2:.2f}" class="plot-axis-label" text-anchor="middle" transform="rotate(-90 24 {top + plot_height / 2:.2f})">{escape(y_label)}</text>')
    return "\n".join(parts)


def _plot_ticks(min_value: float, max_value: float, *, log: bool) -> list[float]:
    if log:
        start = math.floor(math.log10(max(min_value, 1e-9)))
        end = math.ceil(math.log10(max(max_value, 1e-9)))
        ticks = []
        for exponent in range(start, end + 1):
            for multiplier in (1, 2, 5):
                value = multiplier * (10 ** exponent)
                if min_value <= value <= max_value:
                    ticks.append(float(value))
        return ticks or [min_value, max_value]
    step_count = 5
    return [min_value + (max_value - min_value) * index / step_count for index in range(step_count + 1)]


def _plot_x_ticks(min_value: float, max_value: float, *, log: bool, label: str) -> list[float]:
    if label == "Dims":
        return _plot_dimension_ticks(min_value, max_value)
    return _plot_ticks(min_value, max_value, log=log)


def _plot_dimension_ticks(min_value: float, max_value: float) -> list[float]:
    start = math.ceil(min_value / PLOT_DIMENSION_GRID_STEP) * PLOT_DIMENSION_GRID_STEP
    dense_end = min(max_value, PLOT_DIMENSION_DENSE_TICK_MAX)
    end = math.floor(dense_end / PLOT_DIMENSION_GRID_STEP) * PLOT_DIMENSION_GRID_STEP
    ticks = []
    value = start
    while value <= end:
        ticks.append(float(value))
        value += PLOT_DIMENSION_GRID_STEP
    for value in (*PLOT_DIMENSION_HIGH_TICKS, max_value):
        if value > PLOT_DIMENSION_DENSE_TICK_MAX and min_value <= value <= max_value:
            if not any(math.isclose(value, tick, rel_tol=1e-9, abs_tol=1e-9) for tick in ticks):
                ticks.append(float(value))
    return ticks or [min_value, max_value]


def _render_plot_legend(*, x: int, y: int, height: int, label: str, min_value: float, max_value: float, field: str) -> str:
    label_x = x + 84
    label_y = y + height / 2
    mid_value = _plot_legend_mid_value(min_value=min_value, max_value=max_value, field=field)
    return f"""
      <defs>
        <linearGradient id="plot-color-gradient" x1="0" x2="0" y1="1" y2="0">
          <stop offset="0%" stop-color="#4f46e5"></stop>
          <stop offset="50%" stop-color="#0891b2"></stop>
          <stop offset="100%" stop-color="#f59e0b"></stop>
        </linearGradient>
      </defs>
      <g class="plot-legend">
        <text x="{label_x}" y="{label_y:.2f}" class="plot-axis-label plot-legend-label" text-anchor="middle" transform="rotate(-90 {label_x} {label_y:.2f})">{escape(label)}</text>
        <rect x="{x}" y="{y}" width="18" height="{height}" fill="url(#plot-color-gradient)"></rect>
        <text x="{x + 28}" y="{y + 5}" class="plot-axis-tick">{escape(_fmt_plot_axis_value(max_value, PLOT_AXIS_OPTIONS[field][0]))}</text>
        <text x="{x + 28}" y="{y + height / 2 + 4:.2f}" class="plot-axis-tick">{escape(_fmt_plot_axis_value(mid_value, PLOT_AXIS_OPTIONS[field][0]))}</text>
        <text x="{x + 28}" y="{y + height}" class="plot-axis-tick">{escape(_fmt_plot_axis_value(min_value, PLOT_AXIS_OPTIONS[field][0]))}</text>
      </g>
"""


def _plot_legend_mid_value(*, min_value: float, max_value: float, field: str) -> float:
    if field == "quantization":
        return 8.0
    if _plot_field_uses_log(field) and min_value > 0 and max_value > 0:
        return math.sqrt(min_value * max_value)
    return min_value + (max_value - min_value) / 2.0


def _plot_tooltip(point: _PlotPoint) -> str:
    row = point["row"]
    lines = [row.model_name, f"Type: {_plot_model_type_label(row)}"]
    if row.embedding_variant_name:
        lines.append(f"Variant: {row.embedding_variant_name}")
    lines.extend(["", f"Borda score: {_fmt_score(row.borda_score)}"])
    if row.micro_mean is not None or row.macro_mean is not None:
        if row.micro_mean is not None:
            lines.append(f"Mean (Micro): {_fmt_score(row.micro_mean)}")
        if row.macro_mean is not None:
            lines.append(f"Mean (Macro): {_fmt_score(row.macro_mean)}")
    else:
        lines.append(f"Mean score: {_fmt_score(row.mean_score)}")
    lines.extend(
        [
            f"Rank: {_fmt_rank(row.borda_rank)}",
            "",
            f"Active params: {_plot_tooltip_active_parameters_label(row)}",
            f"Total params: {_plot_tooltip_total_parameters_label(row)}",
            f"Max tokens: {_fmt_int(row.max_seq_length)}",
            f"{_plot_dimension_tooltip_label(row)}: {_plot_embedding_dim_label(row)}",
            f"Quantization: {_plot_quantization_label(row.quantization)}",
        ]
    )
    return "\n".join(lines)


def _plot_model_metadata(row: LeaderboardRow, model_views: dict[str, ModelCellView]) -> str:
    model_view = model_views.get(row.model_name)
    metadata = model_view.metadata if model_view is not None else {"model_name": row.model_name}
    return escape(json.dumps(metadata, ensure_ascii=False, separators=(",", ":")), quote=True)


def _plot_model_type_label(row: LeaderboardRow) -> str:
    if _is_bm25_row(row):
        return "BM25"
    model_type_key = model_type_filter_key(model_name=row.source_model_name or row.model_name, model_type=row.model_type)
    return {
        "dense": "Dense",
        "sparse": "Sparse",
        "late-interaction": "Late interaction",
        "reranker": "Reranker",
    }.get(model_type_key, "Dense")


def _fmt_plot_axis_value(value: float, label: str) -> str:
    if "Params" in label:
        return _fmt_params(int(value))
    if "Tokens" in label:
        return _fmt_max_len(int(value))
    if "Quantization" in label:
        return f"{value:g}"
    if value >= 1000:
        return f"{int(value):,}"
    return f"{value:.2f}".rstrip("0").rstrip(".")


def _fmt_plot_x_tick(value: float, label: str, *, log: bool) -> str:
    if log and "Params" in label:
        multiplier = _plot_log_tick_multiplier(value)
        if multiplier in {2, 5}:
            return str(multiplier)
    return _fmt_plot_axis_value(value, label)


def _plot_log_tick_multiplier(value: float) -> int | None:
    if value <= 0 or not math.isfinite(value):
        return None
    exponent = math.floor(math.log10(value))
    multiplier = value / (10**exponent)
    for candidate in (1, 2, 5):
        if math.isclose(multiplier, candidate, rel_tol=1e-9, abs_tol=1e-9):
            return candidate
    return None


def _fmt_plot_score_tick(value: float) -> str:
    return f"{value:.0f}" if abs(value) >= 10 else f"{value:.2f}".rstrip("0").rstrip(".")


def _fmt_int(value: int | None) -> str:
    return "Unknown" if value is None else f"{value:,}"


def _plot_tooltip_active_parameters_label(row: LeaderboardRow) -> str:
    if _plot_unknown_params_as_zero(row):
        return "0"
    return _fmt_int(row.active_parameters)


def _plot_tooltip_total_parameters_label(row: LeaderboardRow) -> str:
    if _plot_unknown_params_as_zero(row):
        return "0"
    return _fmt_int(row.total_parameters)


def _plot_embedding_dim_label(row: LeaderboardRow) -> str:
    if _is_sparse_or_bm25_row(row):
        return "sparse"
    return _fmt_int(row.embedding_dim)


def _plot_dimension_tooltip_label(row: LeaderboardRow) -> str:
    return "Token dim" if _is_late_interaction_row(row) else "Embedding dim"


def _plot_quantization_label(quantization: str | None) -> str:
    return quantization or "none"


def _normalized_plot_score_field(value: str) -> str:
    return value if value in PLOT_SCORE_FIELDS else "borda_score"


def _normalized_plot_axis_field(value: str) -> str:
    return value if value in PLOT_AXIS_FIELDS else "active_parameters"


def _normalized_plot_channel_field(value: str, *, default: str) -> str:
    return value if value in PLOT_ENCODING_FIELDS else default


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
    plot_state: QueryState | None = None,
) -> str:
    filter_state = filter_state or FilterState()
    filter_context = filter_context or row_filter_context(result.rows, filter_state)
    grouped_buttons: dict[str, list[tuple[int, str]]] = {
        "Scope presets": [],
        "Nano suites": [],
    }
    available_views = _available_view_names_with_clear(result.available_views)
    for index, view_name in enumerate(available_views):
        active = _scope_or_benchmark_active(result=result, view_name=view_name)
        raw_view_label = result.available_view_labels.get(view_name, view_name)
        view_label = _viewer_scope_label(view_name=view_name, fallback=raw_view_label)
        classes = _control_button_classes(active=active)
        tab_sort = "borda_score" if sort.startswith("metric:") else sort
        tab_direction = "asc" if sort.startswith("metric:") else direction
        query_payload = _apply_plot_state(
            state_payload(result=result, sort=tab_sort, direction=tab_direction, filter_state=filter_state),
            plot_state,
        )
        doc = benchmark_docs.group_doc(view_name) if benchmark_docs is not None else None
        group = _view_group(view_name)
        sort_key = _view_group_sort_key(view_name=view_name, fallback=index)
        if group == "Scope presets":
            query_payload = _scope_preset_query_payload(
                result=result,
                view_name=view_name,
                sort=tab_sort,
                direction=tab_direction,
                filter_state=filter_state,
            )
            query_payload = _apply_plot_state(query_payload, plot_state)
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
        query_payload = _benchmark_toggle_query_payload(
            result=result,
            view_name=view_name,
            sort=tab_sort,
            direction=tab_direction,
            filter_state=filter_state,
            available_views=available_views,
        )
        query_payload = _apply_plot_state(query_payload, plot_state)
        if view_name == "MNanoBEIR":
            if result.view_name != "MNanoBEIR":
                for offset, selection_key, label in [
                    (0, benchmark_selection_key("MNanoBEIR", "task_mean"), "M-BEIR(task)"),
                    (1, benchmark_selection_key("MNanoBEIR", "lang_mean"), "M-BEIR(lang)"),
                ]:
                    _benchmark_name, score_group = split_benchmark_selection_key(selection_key)
                    score_group = score_group or "task_mean"
                    selection_query_payload = _benchmark_toggle_query_payload(
                        result=result,
                        selection_key=selection_key,
                        sort=tab_sort,
                        direction=tab_direction,
                        filter_state=filter_state,
                        available_views=available_views,
                    )
                    selection_query_payload = _apply_plot_state(selection_query_payload, plot_state)
                    selection_query = urlencode(selection_query_payload, doseq=True)
                    selection_active = _benchmark_selection_active(result=result, selection_key=selection_key)
                    grouped_buttons[group].append(
                        (
                            sort_key * 10 + offset,
                            _render_benchmark_view_button(
                                label=label,
                                active=selection_active,
                                query=selection_query,
                                query_payload=selection_query_payload,
                                doc=doc,
                                benchmark_name=selection_key,
                                help_content=_mnanobeir_scope_help(score_group),
                            ),
                        )
                    )
                continue
            for offset, score_group, label in [
                (0, "task_mean", "M-BEIR(task)"),
                (1, "lang_mean", "M-BEIR(lang)"),
            ]:
                group_query_payload = state_payload(
                    result=result,
                    sort=tab_sort,
                    direction=tab_direction,
                    filter_state=filter_state,
                )
                group_query_payload = _apply_plot_state(group_query_payload, plot_state)
                group_query_payload["view"] = view_name
                group_query_payload.pop("bench", None)
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
                            benchmark_name=view_name,
                            help_content=_mnanobeir_scope_help(score_group),
                        ),
                    )
                )
            continue
        query = urlencode(query_payload, doseq=True)
        if doc is None:
            grouped_buttons[group].append(
                (
                    sort_key * 10,
                    f"""<button type="button" class="border px-2 py-1 text-[0.8125rem] leading-tight {classes}"
                      data-benchmark-toggle="{escape(view_name, quote=True)}"
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
                    benchmark_name=view_name,
                ),
            )
        )
    preset_buttons = [button for _, button in sorted(grouped_buttons["Scope presets"])]
    suite_buttons = [button for _, button in sorted(grouped_buttons["Nano suites"])]
    return f"""
    <nav class="mb-3 border border-zinc-200 bg-white p-1.5 text-[0.8125rem] text-zinc-700" aria-label="Leaderboard configuration">
      <div class="grid gap-1.5">
        <div class="border border-zinc-200 bg-white p-1.5">
          <div class="flex flex-wrap items-center gap-x-4 gap-y-1.5">
            {_render_target_group(result=result, sort=sort, direction=direction, filter_state=filter_state, plot_state=plot_state)}
            {_render_score_aggregation_group(result=result, sort=sort, direction=direction, filter_state=filter_state, plot_state=plot_state)}
            {_render_metric_group(result=result, sort=sort, direction=direction, filter_state=filter_state, plot_state=plot_state)}
          </div>
        </div>
        <div class="grid gap-1.5">
          <div class="border border-zinc-200 bg-white p-1.5">
            <div class="mb-1.5 flex flex-wrap items-center gap-2">
              <span class="control-label-group inline-flex items-center gap-1 px-2 py-1 text-[0.8125rem]">
                {_control_label(icon="database", text="Benchmark scope")}
              </span>
              <div class="flex flex-wrap gap-2">{''.join(preset_buttons)}</div>
            </div>
            <div class="benchmark-scope-divider mb-1.5 border-t border-zinc-200" aria-hidden="true"></div>
            <div class="flex min-w-0 flex-wrap gap-2">{''.join(suite_buttons)}</div>
          </div>
          {render_language_pages(result=result, sort=sort, direction=direction, filter_state=filter_state, embedded=True, plot_state=plot_state)}
        </div>
        {render_display_controls(result=result, sort=sort, direction=direction, filter_state=filter_state, plot_state=plot_state)}
        {render_controls(result=result, sort=sort, direction=direction, filter_state=filter_state, filter_context=filter_context, plot_state=plot_state)}
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
    active = view_name == result.view_name and view_name != CLEAR_SCOPE_NAME
    classes = _control_button_classes(active=active)
    title, summary, details = _scope_preset_help(view_name)
    help_icon = _render_button_help_icon(title=title, summary=summary, details=details)
    label_html = (
        f"""{_icon_svg("eraser")}<span>{escape(view_label)}</span>"""
        if view_name == CLEAR_SCOPE_NAME
        else escape(view_label)
    )
    button_classes = (
        "inline-flex items-center gap-1.5 py-1 pl-2 pr-0 text-left"
        if view_name == CLEAR_SCOPE_NAME
        else "py-1 pl-2 pr-0 text-left"
    )
    return f"""<span class="control-button-group inline-flex items-center border text-[0.8125rem] leading-tight {classes}">
                  <button type="button" class="{button_classes}"
                    hx-get="{_leaderboard_url(query)}" hx-push-url="{_page_url(query_payload)}"
                    {_leaderboard_control_hx_attrs()}>{label_html}</button>
                  <span class="inline-flex items-center pl-1 pr-2">{help_icon}</span>
                </span>"""


def _render_benchmark_view_button(
    *,
    label: str,
    active: bool,
    query: str,
    query_payload: QueryState,
    doc: BenchmarkDoc | None,
    benchmark_name: str | None = None,
    help_content: tuple[str, str, str] | None = None,
) -> str:
    classes = _control_button_classes(active=active)
    data_attr = "" if benchmark_name is None else f' data-benchmark-toggle="{escape(benchmark_name, quote=True)}"'
    if doc is None and help_content is None:
        return f"""<button type="button"{data_attr} class="border px-2 py-1 text-[0.8125rem] leading-tight {classes}"
                      hx-get="{_leaderboard_url(query)}" hx-push-url="{_page_url(query_payload)}"
                      {_leaderboard_control_hx_attrs()}>
                      {escape(label)}
                    </button>"""
    if doc is not None and help_content is None:
        doc_trigger = _render_doc_summary_trigger(doc=doc, label=f"{doc.title} overview")
        return f"""<span class="control-button-group doc-label-group inline-flex items-center border text-[0.8125rem] leading-tight {classes}" data-doc-label-group="benchmark">
                  <button type="button" class="py-1 pl-2 pr-0 text-left"
                    {data_attr}
                    hx-get="{_leaderboard_url(query)}" hx-push-url="{_page_url(query_payload)}"
                    {_leaderboard_control_hx_attrs()}>
                    {escape(label)}
                  </button>
                  <span class="inline-flex items-center pl-0.5 pr-2">{doc_trigger}</span>
                </span>"""
    icon_triggers = []
    if doc is not None:
        icon_triggers.append(_render_doc_summary_trigger(doc=doc, label=f"{doc.title} overview"))
    if help_content is not None:
        title, summary, details = help_content
        icon_triggers.append(_render_button_help_icon(title=title, summary=summary, details=details))
    return f"""<span class="control-button-group doc-label-group inline-flex items-center border text-[0.8125rem] leading-tight {classes}" data-doc-label-group="benchmark">
              <button type="button" class="py-1 pl-2 pr-0 text-left"
                {data_attr}
                hx-get="{_leaderboard_url(query)}" hx-push-url="{_page_url(query_payload)}"
                {_leaderboard_control_hx_attrs()}>
                {escape(label)}
              </button>
              <span class="inline-flex items-center gap-0.5 pl-0.5 pr-2">{''.join(icon_triggers)}</span>
            </span>"""


def _mnanobeir_scope_help(score_group: str) -> tuple[str, str, str]:
    matrix_note = (
        "MNanoBEIR is a language x task benchmark matrix: each raw row is one "
        "NanoBEIR language dataset, such as NanoBEIR-ja, crossed with one "
        "BEIR-style task, such as NanoArguAna or NanoSciFact. Showing every "
        "language-task cell as an individual benchmark scope would make the "
        "picker hard to scan, so the viewer exposes two grouped views."
    )
    if score_group == "lang_mean":
        return (
            "Benchmark scope: NanoBEIR(lang)",
            "Averages the multilingual NanoBEIR matrix by language dataset.",
            f"{matrix_note}\n\nNanoBEIR(lang) first groups rows by language dataset, such as NanoBEIR-en, NanoBEIR-ja, or NanoBEIR-de, averaging all tasks within each language before the final score is computed. Use it when you want language coverage and per-language robustness to be the visible unit.\n\nThis differs from NanoBEIR(task), which groups by BEIR source task first and averages languages inside each task.",
        )
    return (
        "Benchmark scope: NanoBEIR(task)",
        "Averages the multilingual NanoBEIR matrix by BEIR source task.",
        f"{matrix_note}\n\nNanoBEIR(task) first groups rows by BEIR-style task, such as ArguAna, FEVER, or SciFact, averaging all available languages within each task before the final score is computed. Use it when you want task behavior to be the visible unit while smoothing over language coverage.\n\nThis differs from NanoBEIR(lang), which groups by language dataset first and averages tasks inside each language.",
    )


def _available_view_names_with_clear(available_views: list[str]) -> list[str]:
    if CLEAR_SCOPE_NAME in available_views:
        return available_views
    views = list(available_views)
    insert_after = "Overall (EN)" if "Overall (EN)" in views else "Overall"
    if insert_after in views:
        views.insert(views.index(insert_after) + 1, CLEAR_SCOPE_NAME)
    else:
        views.insert(0, CLEAR_SCOPE_NAME)
    return views


def _scope_or_benchmark_active(*, result: LeaderboardResult, view_name: str) -> bool:
    if view_name == CLEAR_SCOPE_NAME:
        return False
    if _view_group(view_name) == "Scope presets":
        return view_name == result.view_name
    selected_benchmarks = set(result.selected_benchmarks)
    if selected_benchmarks:
        return view_name in selected_benchmarks
    return view_name == result.view_name


def _benchmark_selection_active(*, result: LeaderboardResult, selection_key: str) -> bool:
    selected_benchmarks = set(result.selected_benchmarks)
    if selected_benchmarks:
        return selection_key in selected_benchmarks
    return benchmark_name_from_selection_key(selection_key) == result.view_name


def _scope_preset_query_payload(
    *,
    result: LeaderboardResult,
    view_name: str,
    sort: str,
    direction: str,
    filter_state: FilterState,
) -> QueryState:
    scope_filter_state = filter_state
    if view_name in {"Overall", CLEAR_SCOPE_NAME}:
        scope_filter_state = _filter_state_with_languages(filter_state, ())
    elif view_name == "Overall (EN)":
        scope_filter_state = _filter_state_with_languages(filter_state, ("en",))
    query_payload = state_payload(
        result=result,
        sort=sort,
        direction=direction,
        filter_state=scope_filter_state,
    )
    query_payload["view"] = CUSTOM_SCOPE_NAME if view_name == CLEAR_SCOPE_NAME else view_name
    query_payload.pop("bench", None)
    if view_name == CLEAR_SCOPE_NAME:
        query_payload.pop("lang_filter", None)
    return query_payload


def _benchmark_toggle_query_payload(
    *,
    result: LeaderboardResult,
    view_name: str | None = None,
    selection_key: str | None = None,
    sort: str,
    direction: str,
    filter_state: FilterState,
    available_views: list[str],
) -> QueryState:
    selection_key = selection_key or view_name
    if selection_key is None:
        raise ValueError("selection_key or view_name is required")
    benchmark_name = benchmark_name_from_selection_key(selection_key)
    selected = list(result.selected_benchmarks)
    if not selected and _view_group(result.view_name) == "Nano suites":
        selected = [result.view_name]
    if selection_key in selected:
        selected = [benchmark for benchmark in selected if benchmark != selection_key]
    else:
        selected = [
            benchmark
            for benchmark in selected
            if benchmark_name_from_selection_key(benchmark) != benchmark_name
        ]
        selected.append(selection_key)
    selected = _ordered_benchmark_selection(selected, available_views)
    query_payload = state_payload(
        result=result,
        sort=sort,
        direction=direction,
        filter_state=filter_state,
    )
    query_payload.pop("group", None)
    query_payload.pop("bench", None)
    if not selected:
        query_payload["view"] = CLEAR_SCOPE_NAME
        query_payload.pop("lang_filter", None)
        return query_payload
    query_payload["view"] = CUSTOM_SCOPE_NAME
    query_payload["bench"] = selected
    return query_payload


def _ordered_benchmark_selection(selected: list[str], available_views: list[str]) -> list[str]:
    selected_by_benchmark = {
        benchmark_name_from_selection_key(selection_key): selection_key
        for selection_key in selected
    }
    ordered = [
        selected_by_benchmark[view_name]
        for view_name in available_views
        if _view_group(view_name) == "Nano suites" and view_name in selected_by_benchmark
    ]
    ordered.extend(
        selection_key
        for selection_key in selected
        if selection_key not in ordered
    )
    return ordered


def _render_button_help_icon(*, title: str, summary: str, details: str) -> str:
    return f"""<button type="button"
                    class="help-summary-trigger inline-flex h-3.5 w-3.5 shrink-0 items-center justify-center rounded-full border border-zinc-300 text-[9px] leading-none text-zinc-600"
                    data-help-title="{escape(title, quote=True)}"
                    data-help-summary="{escape(summary, quote=True)}"
                    data-help-details="{escape(details, quote=True)}"
                    aria-label="{escape(title, quote=True)}">{_icon_svg("circle-help")}</button>"""


def _scope_preset_help(view_name: str) -> tuple[str, str, str]:
    help_text = {
        "Overall": (
            "Benchmark scope: Overall",
            "Shows every benchmark family available in the viewer.",
            "Overall is the default and broadest leaderboard scope. It includes multilingual, language-specific, and domain-specific NanoSets before any task facet, model, task, or variant filters are applied.\n\nUse Overall when you want a comprehensive ranking across the full current HAKARI-Bench database. Pair it with Micro when you want every raw task row to contribute equally, or Macro when you want each NanoSet to contribute equally.",
        ),
        "Overall (EN)": (
            "Benchmark scope: Overall (EN)",
            "Shows the full benchmark scope filtered to English task facets.",
            "Overall (EN) uses the same benchmark families as Overall, then applies the EN task facet. It is the English-focused counterpart to the broad Overall leaderboard, not a smaller curated subset.\n\nUse Overall (EN) when you want English task comparisons while keeping the same Micro and Macro score controls. Selecting it switches Task facets to EN so multilingual suites contribute their English slices.",
        ),
        CLEAR_SCOPE_NAME: (
            "Benchmark scope: Clear",
            "Clears every NanoSet selection.",
            "Clear resets the page to empty Custom selection. No benchmark tasks are selected, Task facets return to All languages/categories, and the leaderboard table shows no rows.\n\nClear is an action, not a selected scope state. After pressing it, the URL remains view=Custom with no bench parameters so the next NanoSet toggle starts from a clean custom set.",
        ),
    }
    return help_text.get(
        view_name,
        (
            f"Benchmark scope: {view_name}",
            f"Shows the {view_name} scope from the viewer configuration.",
            "Benchmark scope chooses the tasks that are eligible for the leaderboard before row filters are applied.\n\nUse this control first when you want to compare models on a specific benchmark family, then refine the result with task facets, model filters, task filters, and variant controls.",
        ),
    )


def _render_score_aggregation_group(
    *,
    result: LeaderboardResult,
    sort: str,
    direction: str,
    filter_state: FilterState,
    plot_state: QueryState | None = None,
) -> str:
    if not result.is_overall:
        return ""
    buttons = []
    for score, label in [("micro", "Micro"), ("macro", "Macro")]:
        active = result.score_aggregation == score
        classes = _control_button_classes(active=active)
        tab_sort = "borda_score" if sort.startswith("metric:") else sort
        tab_direction = "asc" if sort.startswith("metric:") else direction
        query_payload = _apply_plot_state(
            state_payload(result=result, sort=tab_sort, direction=tab_direction, filter_state=filter_state),
            plot_state,
        )
        if score == "micro":
            query_payload.pop("score", None)
        else:
            query_payload["score"] = score
        query = urlencode(query_payload, doseq=True)
        buttons.append(
            f"""<button type="button" class="border px-2 py-1 text-[0.8125rem] leading-tight {classes}"
                  hx-get="{_leaderboard_url(query)}" hx-push-url="{_page_url(query_payload)}"
                  {_leaderboard_control_hx_attrs()}>
                  {escape(label)}
                </button>"""
        )
    return f"""
            <div class="flex min-w-0 flex-wrap items-center gap-2">
              <span class="control-label-group inline-flex items-center gap-1 px-2 py-1 text-[0.8125rem]">
                {_control_label(icon="sigma", text="Score")}
                {_render_help_tooltip(
                  "Score aggregation",
                  "Chooses between raw task weighting and grouped NanoSet weighting.",
                  "Micro is the default score. Think of it as the raw task average: every task row gets one vote. A NanoSet with many tasks or language variants therefore has more influence on the final ranking. This is the closest mode to the older raw-task Overall/All behavior.\n\nMacro is the grouped score. Think of it as the Group-style idea moved into the Score control: tasks are first summarized into one score per NanoSet, then the leaderboard ranks and averages those NanoSet scores. Each NanoSet gets one vote regardless of how many raw tasks it contains, so large suites do not dominate simply because they are larger.\n\nFor grouped collections such as MNanoBEIR, language variants are first averaged by BEIR source task, then MNanoBEIR contributes one NanoSet score to the final Macro ranking. Use Macro when you want a family-balanced view across benchmark groups.",
                )}
              </span>
              {''.join(buttons)}
            </div>
            """


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


def _render_target_group(
    *,
    result: LeaderboardResult,
    sort: str,
    direction: str,
    filter_state: FilterState,
    plot_state: QueryState | None = None,
) -> str:
    target_options = [
        ("all", "Retrieval", "search"),
        ("reranking", "Reranking", "list-ordered"),
    ]
    buttons = []
    for target, label, icon in target_options:
        active = result.score_target == "all" if target == "all" else result.score_target != "all"
        classes = _control_button_classes(active=active)
        tab_sort = "borda_score" if sort.startswith("metric:") else sort
        tab_direction = "asc" if sort.startswith("metric:") else direction
        query_payload = _apply_plot_state(
            state_payload(result=result, sort=tab_sort, direction=tab_direction, filter_state=filter_state),
            plot_state,
        )
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
        query_payload = _apply_plot_state(
            state_payload(result=result, sort=sort, direction=direction, filter_state=filter_state),
            plot_state,
        )
        query_payload["target"] = toggle_target
        query = urlencode(query_payload, doseq=True)
        safeguard_help = _render_help_tooltip(
            "Safeguard positives",
            "Keeps reranking comparable by using the safeguarded hybrid candidate set.",
            "This option applies only in Reranking mode. Reranking rows do not search the full corpus; they score or reorder the fixed reranking_hybrid candidate set.\n\nHybrid means RRF over BM25 and dense candidate rankings: BM25 contributes lexical candidates, the dense retriever contributes semantic candidates, and reciprocal rank fusion combines them into the top-100 hybrid candidates for each query.\n\nWhen Safeguard positives is enabled, a query whose top-100 hybrid candidates contain no qrels-positive document gets an optional rank-101 safeguard positive appended. This keeps reranking scores from being dominated by candidate lists where the model had no relevant document to promote.\n\nTurn it off only when you intentionally want to inspect reranking on the raw hybrid top-100 without the appended safeguard positive.",
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
                  "Evaluation mode chooses which result family is shown before the benchmark scope and filters are applied.\n\nRetrieval shows full-corpus retrieval results. Dense, BM25, sparse, and late-interaction models retrieve directly from the corpus and are compared as retrieval systems.\n\nReranking shows materialized rerank scores on the reranking_hybrid candidate set. The candidate set is built from RRF over BM25 and dense candidate rankings, with an optional safeguard positive. Use Reranking to compare how models reorder that fixed hybrid candidate pool. BM25 appears as a candidate-order baseline, not as a cross-encoder reranker.",
              )}
              {safeguard_toggle}
            </div>
            """


def _render_metric_group(
    *,
    result: LeaderboardResult,
    sort: str,
    direction: str,
    filter_state: FilterState,
    plot_state: QueryState | None = None,
) -> str:
    if len(result.available_score_metrics) <= 1:
        return ""
    buttons = []
    for metric in result.available_score_metrics:
        active = metric == result.selected_score_metric
        classes = _control_button_classes(active=active)
        tab_sort = "borda_score" if sort.startswith("metric:") else sort
        tab_direction = "asc" if sort.startswith("metric:") else direction
        query_payload = _apply_plot_state(
            state_payload(result=result, sort=tab_sort, direction=tab_direction, filter_state=filter_state),
            plot_state,
        )
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
    overall_views = {"All", "Group", "Overall", "Overall (EN)", CUSTOM_SCOPE_NAME, CLEAR_SCOPE_NAME}
    if view_name in overall_views or view_name.startswith("Overall"):
        return "Scope presets"
    return "Nano suites"


def _view_group_sort_key(*, view_name: str, fallback: int) -> int:
    priority = {
        "Overall": 0,
        "Overall (EN)": 1,
        CLEAR_SCOPE_NAME: 2,
        CUSTOM_SCOPE_NAME: 3,
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


_LANGUAGE_FULL_NAMES = {
    "ar": "Arabic",
    "bn": "Bengali",
    "da": "Danish",
    "de": "German",
    "en": "English",
    "es": "Spanish",
    "fa": "Persian",
    "fi": "Finnish",
    "fr": "French",
    "hi": "Hindi",
    "id": "Indonesian",
    "it": "Italian",
    "ja": "Japanese",
    "ko": "Korean",
    "nl": "Dutch",
    "no": "Norwegian",
    "pl": "Polish",
    "pt": "Portuguese",
    "ru": "Russian",
    "sv": "Swedish",
    "sw": "Swahili",
    "te": "Telugu",
    "th": "Thai",
    "vi": "Vietnamese",
    "yo": "Yoruba",
    "zh": "Chinese",
}


def _task_facet_help_table_rows(options: Sequence[LanguageOption]) -> list[dict[str, str]]:
    rows = []
    for option in options:
        if option.code.startswith("category:"):
            rows.append(
                {
                    "code": option.code,
                    "name": _task_category_facet_full_name(option.code),
                    "tasks": f"{option.task_count:,}",
                }
            )
            continue
        rows.append(
            {
                "code": option.code.upper(),
                "name": _language_full_name(option.code),
                "tasks": f"{option.task_count:,}",
            }
        )
    return rows


def _language_full_name(code: str) -> str:
    normalized = code.casefold()
    return _LANGUAGE_FULL_NAMES.get(normalized, code.upper() if 2 <= len(code) <= 3 else code)


def _task_category_facet_full_name(code: str) -> str:
    category = code.removeprefix("category:")
    labels = {"code": "Code tasks"}
    return labels.get(category, category.replace("_", " ").title())


def render_language_pages(
    *,
    result: LeaderboardResult,
    sort: str,
    direction: str,
    filter_state: FilterState | None = None,
    embedded: bool = False,
    plot_state: QueryState | None = None,
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
            plot_state=plot_state,
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
            plot_state=plot_state,
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
                plot_state=plot_state,
            )
            for option in more_options
        )
        more = f"""
          <details class="relative">
            <summary class="language-more-summary flex cursor-pointer list-none items-center gap-1.5 border border-zinc-300 bg-white px-2 py-1 text-[0.8125rem] text-zinc-700 hover:border-cyan-500 hover:text-cyan-700">
              <span class="details-chevron inline-flex h-3.5 w-3.5 shrink-0 items-center justify-center text-zinc-500">{_icon_svg("chevron-right")}</span>
              <span>More languages</span>
            </summary>
            <div class="absolute z-10 mt-1 grid max-h-72 min-w-[28rem] grid-cols-3 gap-1 overflow-auto border border-zinc-300 bg-white p-2 shadow-sm sm:grid-cols-5">
              {more_buttons}
            </div>
          </details>
        """
    wrapper_tag = "div" if embedded else "nav"
    wrapper_class = (
        "flex flex-wrap items-start gap-2 border border-zinc-200 bg-white p-1.5"
        if embedded
        else "mb-4 flex flex-wrap items-start gap-2 border border-zinc-200 bg-white p-2"
    )
    return f"""
      <{wrapper_tag} class="{wrapper_class}" aria-label="Task facets">
        <span class="control-label-group inline-flex items-center gap-1 px-2 py-1 text-[0.8125rem]">
          {_control_label(icon="languages", text="Task facets")}
          {_render_help_tooltip(
              "Task facets",
              "Filters tasks inside the selected benchmark scope by language or category.",
              "Task facets narrows the tasks that are included after you choose a benchmark scope.\n\nFor multilingual suites such as MNanoBEIR, each language page filters the task set to one language-specific slice, such as Japanese or German. Code filters to tasks whose metadata category is code. The All languages button removes that task facet filter.\n\nThis is different from Benchmark scope: scope chooses the benchmark family, while Task facets filters the tasks inside that family.",
              table_rows=_task_facet_help_table_rows(result.available_languages),
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
    plot_state: QueryState | None = None,
) -> str:
    language_filters = () if option is None else (option.code,)
    active = result.selected_languages == language_filters
    label = "All languages" if option is None else f"{option.label} {option.task_count}"
    classes = _control_button_classes(active=active)
    query_payload = _apply_plot_state(
        state_payload(
            result=result,
            sort=sort,
            direction=direction,
            filter_state=_filter_state_with_languages(filter_state, language_filters),
        ),
        plot_state,
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
        commercial_filters=filter_state.commercial_filters,
        model_type_filters=filter_state.model_type_filters,
        dtype_filters=filter_state.dtype_filters,
        attn_filters=filter_state.attn_filters,
        prompt_filters=filter_state.prompt_filters,
        **_task_length_filter_kwargs(filter_state),
    )


def _task_length_filter_kwargs(filter_state: FilterState) -> _TaskLengthFilterKwargs:
    return {
        "rank_filtered": filter_state.rank_filtered,
        "active_params_min": filter_state.active_params_min,
        "active_params_max": filter_state.active_params_max,
        "total_params_min": filter_state.total_params_min,
        "total_params_max": filter_state.total_params_max,
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
    plot_state: QueryState | None = None,
) -> str:
    filter_state = filter_state or FilterState()
    quantization_checked = " checked" if result.include_quantization_variants else ""
    truncate_checked = " checked" if result.include_truncate_variants else ""
    rescore_checked = " checked" if result.include_rescore_variants else ""
    other_variant_checked = " checked" if result.include_other_variants else ""
    task_scores_checked = " checked" if result.show_task_scores else ""
    task_z_scores_checked = " checked" if result.show_task_z_scores else ""
    task_ranks_checked = " checked" if result.show_task_ranks else ""
    other_columns_checked = " checked" if result.show_other_columns else ""
    state_fields = [
        ("view", result.view_name),
        ("sort", sort),
        ("direction", direction),
    ]
    state_fields.extend(_selected_benchmark_hidden_fields(result))
    if result.score_target != "all":
        state_fields.append(("target", result.score_target))
    if result.selected_score_metric != "ndcg@10":
        state_fields.append(("metric", result.selected_score_metric))
    if result.selected_score_group is not None:
        state_fields.append(("group", result.selected_score_group.name))
    state_fields.extend(_query_state_fields(plot_state))
    sticky_filter_fields = active_filter_hidden_fields(filter_state) + _text_filter_hidden_fields(filter_state)
    variant_filter_fields = _variant_filter_hidden_fields(filter_state)
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
    if result.show_other_columns:
        task_score_hidden_fields.append(("other_columns", "1"))
    column_hidden_html = _hidden_inputs(state_fields + sticky_filter_fields + variant_hidden_fields)
    variant_hidden_html = _hidden_inputs(state_fields + variant_filter_fields + task_score_hidden_fields)
    return f"""
    <div class="grid gap-1.5 text-[0.8125rem] text-zinc-700 lg:grid-cols-2">
      <form id="column-controls" class="border border-zinc-200 bg-white p-1.5"
            hx-get="/leaderboard" hx-push-url="true"
            {_leaderboard_control_hx_attrs()}
            hx-trigger="change, submit">
        {column_hidden_html}
        <div class="mb-1.5 flex flex-wrap items-center gap-2">
          {_control_label(icon="table-properties", text="Table display")}
          {_render_help_tooltip(
              "Table display",
              "Changes which columns and per-task annotations are visible.",
              "Table display controls how much detail appears in the result table without changing which models or tasks are included.\n\nTask columns adds one score column per task or grouped task. STD adds standard-deviation deltas so you can see unusually strong or weak task performance. Task ranks shows the per-task rank instead of the raw score; when STD and Task ranks are both enabled, each task cell shows the rank, score, and standard-deviation delta together.\n\nUse this panel when the ranking is already scoped correctly and you want to inspect the table at a different level of detail.",
          )}
        </div>
        <div class="flex flex-wrap items-center gap-2">
          <label class="toggle-chip">
            <input type="checkbox" name="task_scores" value="1"{task_scores_checked}>
            <span>Task columns</span>
          </label>
          <label class="toggle-chip">
            <input type="hidden" name="task_z_scores" value="0">
            <input type="checkbox" name="task_z_scores" value="1"{task_z_scores_checked}>
            <span>STD</span>
          </label>
          <label class="toggle-chip">
            <input type="hidden" name="task_ranks" value="0">
            <input type="checkbox" name="task_ranks" value="1"{task_ranks_checked}>
            <span>Task ranks</span>
          </label>
          <label class="toggle-chip">
            <input type="checkbox" name="other_columns" value="1"{other_columns_checked}>
            <span>Others</span>
          </label>
        </div>
      </form>
      <form id="variant-controls" class="border border-zinc-200 bg-white p-1.5"
            hx-get="/leaderboard" hx-push-url="true"
            {_leaderboard_control_hx_attrs()}
            hx-trigger="change, submit">
        {variant_hidden_html}
        <div class="mb-1.5 flex flex-wrap items-center gap-2">
          {_control_label(icon="git-compare-arrows", text="Efficiency variants")}
          {_render_help_tooltip(
              "Efficiency variants",
              "Adds non-base rows that compare quality against storage, dimension, and reranking trade-offs.",
              "Efficiency variants are additional result rows for the same source model. They are hidden by default so the base leaderboard stays compact.\n\nDims includes truncated dense embedding rows and uses short labels such as 512d or 512d <- 1024. Quantization includes compressed numeric formats such as int8 and binary. Rescore includes variants that run a compressed first pass and then rescore or rerank. Sparse pruning includes sparse encoder pruning variants that cap active query or document dimensions, with compact labels such as q32d and d256d when available. It only includes variants whose names match sparse max-active-dims or max-dims settings.\n\nUse this panel when you want to compare a model's base score with smaller, faster, or compressed alternatives.",
          )}
        </div>
        <div class="flex flex-wrap items-center gap-2">
          <label class="toggle-chip">
            <input type="checkbox" name="truncate" value="1"{truncate_checked}>
            <span>Dims</span>
          </label>
          <label class="toggle-chip">
            <input type="checkbox" name="quantization" value="1"{quantization_checked}>
            <span>Quantization</span>
          </label>
          <label class="toggle-chip">
            <input type="checkbox" name="rescore" value="1"{rescore_checked}>
            <span>Rescore</span>
          </label>
          <label class="toggle-chip">
            <input type="checkbox" name="other_variant" value="1"{other_variant_checked}>
            <span>Sparse pruning</span>
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
    plot_state: QueryState | None = None,
) -> str:
    filter_state = filter_state or FilterState()
    filter_context = filter_context or row_filter_context(result.rows, filter_state)
    rank_filtered_checked = " checked" if filter_state.rank_filtered else ""
    state_fields = [
        ("view", result.view_name),
        ("sort", sort),
        ("direction", direction),
    ]
    state_fields.extend(_selected_benchmark_hidden_fields(result))
    if result.score_target != "all":
        state_fields.append(("target", result.score_target))
    if result.selected_score_metric != "ndcg@10":
        state_fields.append(("metric", result.selected_score_metric))
    if result.selected_score_group is not None:
        state_fields.append(("group", result.selected_score_group.name))
    state_fields.extend(_query_state_fields(plot_state))
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
    commercial_options = filter_context.commercial_options
    dtype_options = filter_context.dtype_options
    attn_options = filter_context.attn_options
    prompt_options = filter_context.prompt_options
    model_type_options = filter_context.model_type_options
    selected_dims = filter_context.selected_dims
    selected_quants = filter_context.selected_quants
    selected_commercial = filter_context.selected_commercial
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
            commercial_filters=tuple(filter_context.ordered_selected_commercial()),
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
            commercial_filters=tuple(filter_context.ordered_selected_commercial()),
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
            commercial_filters=tuple(filter_context.ordered_selected_commercial()),
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
            commercial_filters=tuple(filter_context.ordered_selected_commercial()),
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
            commercial_filters=tuple(filter_context.ordered_selected_commercial()),
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
            commercial_filters=tuple(filter_context.ordered_selected_commercial()),
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
            commercial_filters=tuple(filter_context.ordered_selected_commercial()),
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
            commercial_filters=tuple(filter_context.ordered_selected_commercial()),
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
            commercial_filters=tuple(filter_context.ordered_selected_commercial()),
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
            commercial_filters=tuple(filter_context.ordered_selected_commercial()),
            model_type_filters=tuple(filter_context.ordered_selected_model_types()),
            dtype_filters=tuple(filter_context.ordered_selected_dtypes()),
            attn_filters=tuple(filter_context.ordered_selected_attn()),
            prompt_filters=(FILTER_NONE_VALUE,),
            **_task_length_filter_kwargs(filter_state),
        ),
    )
    for query_payload in (
        dim_all_query,
        dim_none_query,
        quant_all_query,
        quant_none_query,
        dtype_all_query,
        dtype_none_query,
        attn_all_query,
        attn_none_query,
        prompt_all_query,
        prompt_none_query,
    ):
        _apply_plot_state(query_payload, plot_state)
    refine_results_open = (
        bool(filter_state.model_filter.strip())
        or bool(filter_state.task_filter.strip())
        or filter_state.rank_filtered
        or bool(filter_state.model_type_filters)
        or filter_state.filters_active
        or filter_state.has_parameter_filters
        or filter_state.has_task_length_filters
    )
    refine_results_open_attr = " open" if refine_results_open else ""
    return f"""
    <div class="grid gap-2 text-[0.8125rem] text-zinc-700">
      <details id="filter-controls-panel" class="border border-zinc-200 bg-white"{refine_results_open_attr}>
        <summary class="refine-results-summary flex cursor-pointer list-none items-center justify-between gap-2 p-2 text-[0.8125rem] font-medium text-zinc-800">
          <span class="inline-flex items-center gap-1.5">
            <span class="details-chevron inline-flex h-4 w-4 shrink-0 items-center justify-center text-zinc-500">{_icon_svg("chevron-right")}</span>
            <span class="inline-flex items-center gap-1">
              {_control_label(icon="filter", text="Filter results")}
              {_render_help_tooltip(
                  "Filter results",
                  "Narrows the models, tasks, and variant rows shown in the current leaderboard.",
                  "Filter results applies filters after Evaluation mode, Benchmark scope, Task facets, and Efficiency variants have selected the candidate result set.\n\nModel and Task text filters are applied when you press Enter. Checkbox and facet filters update automatically. These controls can hide rows and task columns from the table, and they also affect CSV download.\n\nBy default, text and facet filters keep rank context within the current evaluation mode, benchmark scope, task facets, and variant selection. Enable Recalculate ranks from filters when you want those filters to recompute ranks and means. Params and Length range filters always narrow the ranked model or task population when set.",
              )}
            </span>
          </span>
        </summary>
        <form id="filter-controls" class="border-t border-zinc-200 p-2"
              hx-get="/leaderboard" hx-push-url="true"
              {_leaderboard_control_hx_attrs()}
              hx-trigger="change, submit">
          {filter_hidden_html}
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
                    "Model filter searches the displayed model names and hides rows that do not match.\n\nYou can search for multiple model-name keywords by separating them with spaces. The terms are matched as OR conditions with partial, case-insensitive matching. For example, jina bge keeps rows whose model name contains jina or bge.\n\nModel keywords under 3 characters are ignored to avoid accidental broad matches. By default this filter changes which model rows are visible. When Recalculate ranks from filters is enabled, it also changes the ranked model population. It does not change the selected benchmark scope or which task columns are available.",
                )}
                <input id="model-filter-input" type="search" name="model_filter" value="{escape(filter_state.model_filter)}"
                       class="viewer-text-input w-72 max-w-full border border-zinc-300 bg-white px-2 py-1 text-[0.8125rem] text-zinc-900 outline-none focus:border-cyan-700"
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
                       class="viewer-text-input w-72 max-w-full border border-zinc-300 bg-white px-2 py-1 text-[0.8125rem] text-zinc-900 outline-none focus:border-cyan-700"
                       autocomplete="off">
              </label>
            </div>
          </div>
          <div class="filter-panel min-w-0 bg-zinc-50 p-2">
            <div class="filter-panel-body space-y-2">
              <div class="flex flex-wrap items-center gap-2">
                {_control_label(icon="git-branch", text="Efficiency filters")}
                {_render_help_tooltip(
                    "Efficiency filters",
                    "Filters already-included variant rows by dimensions or quantization type.",
                    "Efficiency filters only operate on rows that are already present in the table.\n\nFirst use Efficiency variants to include Dims, Quantization, Rescore, or Sparse pruning variant rows. Then use Dims to keep specific embedding sizes, or Quantization to keep formats such as int8 or binary.\n\nThis is useful when a variant category is too broad and you want to compare a smaller set of compression settings.",
                )}
                {_render_filter_details(name="dim_filter", summary="Dims", icon="ruler", options=dim_options, selected_values=selected_dims, all_query=dim_all_query, none_query=dim_none_query)}
                {_render_filter_details(name="quant_filter", summary="Quantization", icon="binary", options=quant_options, selected_values=selected_quants, all_query=quant_all_query, none_query=quant_none_query)}
              </div>
              {_render_parameter_filter_inputs(filter_state)}
              {_render_task_length_filter_inputs(filter_state)}
              <div class="flex flex-wrap items-center gap-2">
                {_control_label(icon="shield-check", text="License filters")}
                {_render_help_tooltip(
                    "License filters",
                    "Filters rows by whether model-card license metadata permits commercial use.",
                    "Commercial use groups license metadata from model cards. Commercial includes permissive licenses and proprietary terms that permit commercial use with conditions, including the MIT-licensed BM25 baseline. Non-commercial includes licenses such as CC BY-NC. N/A is for rows where commercial-use classification does not apply. Unknown keeps rows without reviewed commercial-use metadata.",
                )}
                {_render_commercial_filter_controls(options=commercial_options, selected_values=selected_commercial)}
              </div>
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
              <div class="refine-results-actions flex flex-wrap items-center gap-2">
                <label class="inline-flex items-center gap-2">
                  <input type="hidden" name="rank_filtered" value="0">
                  <input type="checkbox" name="rank_filtered" value="1" class="h-4 w-4 accent-cyan-700"{rank_filtered_checked}>
                  {_control_label(icon="sigma", text="Recalculate ranks from filters")}
                  {_render_help_tooltip(
                      "Recalculate ranks from filters",
                      "Recomputes ranking numbers using only the currently filtered result set.",
                      "When this is enabled, Borda ranks, mean ranks, task counts, and visible means are recalculated after the active text, model-family, license, runtime, efficiency, and task filters are applied.\n\nParams and Length range filters already narrow the ranked model or task population whenever they are set.\n\nUse it when you want to answer a local question, such as which model is best among dense models only, or which model wins on a specific task family. Leave it off when you want text and facet filters to keep their rank context from the current evaluation mode, benchmark scope, task facets, and variant selection.",
                  )}
                </label>
              </div>
            </div>
          </div>
        </div>
      </form>
      </details>
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


def _variant_filter_hidden_fields(filter_state: FilterState) -> list[tuple[str, str]]:
    reset_facet_state = FilterState(
        model_filter=filter_state.model_filter,
        task_filter=filter_state.task_filter,
        language_filters=filter_state.language_filters,
        filters_active=False,
        **_task_length_filter_kwargs(filter_state),
    )
    return active_filter_hidden_fields(reset_facet_state) + _text_filter_hidden_fields(reset_facet_state)


def _selected_benchmark_hidden_fields(result: LeaderboardResult) -> list[tuple[str, str]]:
    if result.view_name != CUSTOM_SCOPE_NAME:
        return []
    return [("bench", benchmark) for benchmark in result.selected_benchmarks]


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
              "Model family separates model rows by how the result was produced.\n\nDense models use dense embeddings. BM25 rows use lexical BM25 baselines. Sparse rows use learned sparse retrieval. Late interaction rows use token-level interaction methods such as ColBERT-style scoring. Reranker rows are shown only in Reranking mode.\n\nReranking mode can also include dense or late-interaction candidate-rerank rows and the BM25 candidate-order baseline, so use this filter when you want to compare one family or hide families that are not relevant to the current analysis.",
          )}
        </span>
        {''.join(checkboxes)}
      </fieldset>
    """


def _render_commercial_filter_controls(
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
              <input type="checkbox" name="commercial_filter" value="{escape(value)}" class="h-4 w-4 accent-cyan-700"{checked}>
              <span>{escape(label)}</span>
            </label>"""
        )
    return f"""
      <fieldset id="commercial-use-controls" class="flex flex-wrap items-center gap-x-4 gap-y-2">
        <input type="hidden" name="commercial_filter" value="{FILTER_NONE_VALUE}">
        <span class="inline-flex items-center gap-1 font-medium text-zinc-800">Commercial use</span>
        {''.join(checkboxes)}
      </fieldset>
    """


def _render_parameter_filter_inputs(filter_state: FilterState) -> str:
    input_class = (
        "viewer-text-input w-20 border border-zinc-300 bg-white px-2 py-1 text-[0.8125rem] text-zinc-900 outline-none "
        "focus:border-cyan-700"
    )
    active_class = "text-cyan-700" if filter_state.has_parameter_filters else ""
    return f"""
    <div class="flex flex-wrap items-center gap-2">
      <span class="inline-flex items-center gap-1">
        {_control_label(icon="cpu", text="Params", extra_class=active_class)}
        {_render_help_tooltip(
            "Parameter filters",
            "Filters model rows by active or total parameter count.",
            "Parameter filters operate at the model row level using parameter metadata measured in millions of parameters.\n\nActive Params bounds use active parameter counts. Total Params bounds use total parameter counts. For example, setting Active Params <= 100 keeps rows with at most 100M active parameters.\n\nRows without the selected parameter metadata are excluded when any bound for that parameter type is set. These range filters narrow the ranked model population immediately, even when Recalculate ranks from filters is off.",
        )}
      </span>
      <label class="inline-flex items-center gap-1">
        <span class="text-xs font-medium text-zinc-700">Active Params ≥</span>
        <input type="number" min="0" step="any" name="active_params_min" value="{escape(filter_state.active_params_min)}"
               aria-label="Active Params minimum in millions"
               class="{input_class}">
        <span class="text-xs text-zinc-500">M</span>
      </label>
      <label class="inline-flex items-center gap-1">
        <span class="text-xs font-medium text-zinc-700">Active Params ≤</span>
        <input type="number" min="0" step="any" name="active_params_max" value="{escape(filter_state.active_params_max)}"
               aria-label="Active Params maximum in millions"
               class="{input_class}">
        <span class="text-xs text-zinc-500">M</span>
      </label>
      <label class="inline-flex items-center gap-1">
        <span class="text-xs font-medium text-zinc-700">Total Params ≥</span>
        <input type="number" min="0" step="any" name="total_params_min" value="{escape(filter_state.total_params_min)}"
               aria-label="Total Params minimum in millions"
               class="{input_class}">
        <span class="text-xs text-zinc-500">M</span>
      </label>
      <label class="inline-flex items-center gap-1">
        <span class="text-xs font-medium text-zinc-700">Total Params ≤</span>
        <input type="number" min="0" step="any" name="total_params_max" value="{escape(filter_state.total_params_max)}"
               aria-label="Total Params maximum in millions"
               class="{input_class}">
        <span class="text-xs text-zinc-500">M</span>
      </label>
    </div>
    """


def _render_task_length_filter_inputs(filter_state: FilterState) -> str:
    input_class = (
        "viewer-text-input w-24 border border-zinc-300 bg-white px-2 py-1 text-[0.8125rem] text-zinc-900 outline-none "
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
            "Length filters operate at the task level using average text length metadata measured in characters.\n\nQuery length bounds filter by the average query string length for a task. Document length bounds filter by the average document string length. For example, setting Document length <= 2000 keeps tasks whose documents are relatively short on average.\n\nTasks without length metadata are excluded when any bound is set. These range filters narrow the ranked task population immediately, even when Recalculate ranks from filters is off.",
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
        query_payload = state_payload(result=result, sort="borda_score", direction="desc", filter_state=filter_state)
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
    metric_labels = _metric_column_labels(
        result.metric_columns,
        overrides=result.metric_column_labels,
        parent_label=result.view_name,
    )
    columns = [
        ("model_name", "Model Name", "asc", "left", False, ""),
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
            ("active_parameters", "Active Params", "asc", "right", False, ""),
            ("total_parameters", "Total Params", "asc", "right", False, ""),
            ("max_seq_length", "Max Tokens", "desc", "right", False, ""),
            ("embedding_dim", "Dims", "desc", "right", False, ""),
        ]
    )
    if result.include_quantization_variants:
        columns.append(("quantization", "Quant", "asc", "left", False, ""))
    if _show_base_delta_column(result):
        columns.append(("base_score_delta_percent", "Δ vs Base", "desc", "right", False, ""))
    if result.show_other_columns:
        columns.extend(
            [
                ("license", "License", "", "left", False, ""),
                ("model_type", "Model Type", "", "left", False, ""),
            ]
        )
    heads = []
    for key, label, default_direction, align, is_metric, full_metric_name in columns:
        align = "left"
        sortable = bool(default_direction)
        next_direction = (
            _next_direction(key=key, sort=sort, direction=direction, default_direction=default_direction)
            if sortable
            else ""
        )
        indicator = _render_sort_indicator(active=sort == key, direction=direction) if sortable else ""
        query_payload = (
            state_payload(result=result, sort=key, direction=next_direction, filter_state=filter_state)
            if sortable
            else {}
        )
        query = urlencode(query_payload, doseq=True) if sortable else ""
        justify = "justify-end" if align == "right" else "justify-start"
        text_align = "text-right" if align == "right" else "text-left"
        th_spacing = f"{_metric_column_width_class(result)} px-1 normal-case" if is_metric else "px-2 uppercase"
        sticky = _sticky_head_class(key)
        label_class = "min-w-0 text-left leading-tight font-normal" if is_metric else "text-left"
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
                     <span class="block w-full truncate font-normal">{escape(group_label)}</span>
                     <span class="inline-flex max-w-full items-center gap-1">
                       <button type="button" class="inline-flex min-w-0 items-center gap-0.5 text-left hover:text-cyan-700"
                               hx-get="{_leaderboard_url(query)}" hx-push-url="{_page_url(query_payload)}"
                               {_leaderboard_control_hx_attrs()}>
                         <span class="block max-w-full truncate font-normal">{escape(task_label)}</span>{indicator}
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
            if sortable:
                header_content = f"""
                 <button type="button" class="inline-flex w-full min-w-0 flex-1 items-center gap-0.5 {justify} text-left hover:text-cyan-700"
                         hx-get="{_leaderboard_url(query)}" hx-push-url="{_page_url(query_payload)}"
                         {_leaderboard_control_hx_attrs()}>
                   <span class="{label_class}"{label_attrs}>{label_markup}</span>{indicator}
                 </button>"""
            else:
                header_content = f"""
                 <span class="inline-flex w-full min-w-0 flex-1 items-center gap-0.5 {justify} text-left">
                   <span class="{label_class}"{label_attrs}>{label_markup}</span>
                 </span>"""
        heads.append(
            f"""<th scope="col" data-column-key="{escape(key, quote=True)}" class="bg-zinc-100 py-1 text-[0.6875rem] font-normal text-zinc-600 {text_align} {th_spacing} {sticky}">
                 {header_content}
               </th>"""
        )
    index_head = (
        '<th scope="col" aria-label="Rank" data-column-key="index" '
        'class="leaderboard-col-index sticky z-30 bg-zinc-100 px-1.5 py-1 text-right text-[0.6875rem] font-normal text-zinc-600"></th>'
    )
    return f"<thead><tr>{index_head}{''.join(heads)}</tr></thead>"


def _sticky_head_class(key: str) -> str:
    if key == "model_name":
        return "leaderboard-col-model sticky z-20"
    return ""


def render_table_body(*, result: LeaderboardResult, filter_context: FilterContext | None = None) -> str:
    if not result.rows:
        colspan = _leaderboard_table_colspan(result)
        return f"""<tbody><tr><td class="px-3 py-5 text-center text-zinc-500" colspan="{colspan}">No complete results found.</td></tr></tbody>"""
    filter_context = filter_context or row_filter_context(result.rows, FilterState())
    body_rows = []
    model_views = model_cell_views(result.rows)
    borda_score_bar_widths = _borda_score_bar_widths(rows=result.rows, filter_context=filter_context)
    metric_rank_labels = _metric_rank_display_labels(result)
    visible_index = 0
    for row in result.rows:
        hidden = not filter_context.is_visible(row)
        row_class = "leaderboard-row odd:bg-white even:bg-zinc-50"
        hidden_attrs = ' hidden data-filter-hidden="true"' if hidden else ""
        if hidden:
            index_label = ""
        else:
            visible_index += 1
            index_label = str(visible_index)
        borda_score_cell = _render_borda_score_cell(result=result, row=row)
        mean_cells = _render_mean_cells(result=result, row=row)
        body_rows.append(
            f"""<tr class="{row_class}"{hidden_attrs}>
              <td class="leaderboard-col-index sticky z-10 bg-inherit px-1.5 py-1 text-right tabular-nums text-zinc-500">{index_label}</td>
              {render_model_name_cell(row, model_views[row.model_name], borda_score_bar_width=borda_score_bar_widths.get(row.model_name))}
              {borda_score_cell}
              {mean_cells}
              {_render_metric_cells(result=result, row=row, metric_rank_labels=metric_rank_labels)}
              <td class="px-2 py-1 text-left tabular-nums">{_fmt_params(row.active_parameters)}</td>
              <td class="px-2 py-1 text-left tabular-nums">{_fmt_params(row.total_parameters)}</td>
              <td class="px-2 py-1 text-left tabular-nums">{_fmt_max_len(row.max_seq_length)}</td>
              <td class="px-2 py-1 text-left tabular-nums">{_fmt_row_embedding_dim(row)}</td>
              {_render_quantization_cell(result=result, row=row)}
              {_render_base_delta_cell(result=result, row=row)}
              {_render_other_columns(result=result, model_view=model_views[row.model_name])}
            </tr>"""
        )
    return f"<tbody>{''.join(body_rows)}</tbody>"


def _leaderboard_table_colspan(result: LeaderboardResult) -> int:
    column_count = 3  # leading rank index + model + borda score
    column_count += 2 if result.is_overall and not (result.rank_filtered and result.task_filter) else 1
    column_count += len(result.metric_columns)
    column_count += 4
    if result.include_quantization_variants:
        column_count += 1
    if _show_base_delta_column(result):
        column_count += 1
    if result.show_other_columns:
        column_count += 2
    return column_count


def _render_borda_score_cell(*, result: LeaderboardResult, row: LeaderboardRow) -> str:
    if result.show_task_z_scores:
        return _render_score_z_cell(
            score=row.borda_score,
            z_score=row.borda_score_z,
            cell_class="px-2 py-1 text-left tabular-nums",
        )
    return f"""<td class="px-2 py-1 text-left tabular-nums">{_fmt_score(row.borda_score)}</td>"""


def _borda_score_bar_widths(*, rows: Sequence[LeaderboardRow], filter_context: FilterContext) -> dict[str, float]:
    visible_rows = [row for row in rows if filter_context.is_visible(row)]
    if not visible_rows:
        return {}
    max_score = max(row.borda_score for row in visible_rows)
    if max_score <= 0:
        return {row.model_name: 0.0 for row in visible_rows}
    return {row.model_name: (row.borda_score / max_score) * 100.0 for row in visible_rows}


def render_leaderboard_csv(*, result: LeaderboardResult, filter_state: FilterState | None = None) -> str:
    filter_context = row_filter_context(result.rows, filter_state or FilterState())
    visible_rows = [row for row in result.rows if filter_context.is_visible(row)]
    model_views = model_cell_views(result.rows)
    metric_labels = _metric_column_labels(
        result.metric_columns,
        overrides=result.metric_column_labels,
        parent_label=result.view_name,
    )
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
            "Max Tokens",
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
        "Max Tokens",
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
        "Max Tokens": metadata.get("max_seq_length"),
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
    return (
        model_type_filter_key(model_name=row.source_model_name or row.model_name, model_type=row.model_type) == "sparse"
        and is_sparse_dims_variant_name(row.embedding_variant_name)
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
    score_html = _render_score_z_badge(
        score=row.metric_values.get(column),
        z_score=row.metric_z_values.get(column),
        rank_label=rank_label,
    )
    return (
        f'<td class="{metric_width_class} px-1 py-1 text-left tabular-nums">'
        f"{score_html}"
        "</td>"
    )


def _metric_column_width_class(result: LeaderboardResult) -> str:
    if result.show_task_ranks and result.show_task_z_scores:
        return "w-[5.5rem] min-w-[5.5rem] max-w-[5.5rem]"
    if result.show_task_ranks:
        return "w-[5.5rem] min-w-[5.5rem] max-w-[5.5rem]"
    return "w-[5.5rem] min-w-[5.5rem] max-w-[5.5rem]"


def _render_score_z_cell(*, score: float | None, z_score: float | None, cell_class: str) -> str:
    return f'<td class="{cell_class}">{_render_score_z_badge(score=score, z_score=z_score)}</td>'


def _render_score_z_badge(*, score: float | None, z_score: float | None, rank_label: str | None = None) -> str:
    rounded = _rounded_z_score(z_score)
    if rounded is None:
        z_label = ""
        bucket_class = "task-z-neutral"
    else:
        assert z_score is not None
        z_label = f"{_fmt_z_score(z_score)}σ"
        bucket_class = _z_score_bucket_class(rounded)
    rank_html = (
        f'<span class="task-rank-label">{escape(f"[{rank_label}]")}</span>'
        if rank_label
        else ""
    )
    value_html = f'<span class="task-z-score-value">{escape(_fmt_score(score))}</span>'
    score_main_html = (
        f'<span class="task-z-score-main">{rank_html}{value_html}</span>'
        if rank_label
        else value_html
    )
    badge_modifier = " task-z-score-with-rank" if rank_label else ""
    return (
        f'<span class="task-z-score {bucket_class}{badge_modifier}">'
        f"{score_main_html}"
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


def _render_other_columns(*, result: LeaderboardResult, model_view: ModelCellView) -> str:
    if not result.show_other_columns:
        return ""
    metadata = model_view.metadata
    license_label, license_tooltip = _license_table_labels(metadata.get("license"))
    model_type_label, model_type_tooltip = _model_type_table_labels(metadata)
    return _render_short_metadata_cell(license_label, license_tooltip) + _render_short_metadata_cell(
        model_type_label,
        model_type_tooltip,
    )


def _render_short_metadata_cell(label: str, tooltip: str) -> str:
    tooltip_class = " tooltip-trigger tooltip-delay cursor-pointer" if tooltip and tooltip != label else ""
    tooltip_attrs = (
        f' data-tooltip="{escape(tooltip, quote=True)}" aria-label="{escape(tooltip, quote=True)}"'
        if tooltip
        else ""
    )
    return (
        f'<td class="max-w-[7rem] truncate whitespace-nowrap px-2 py-1 text-left{tooltip_class}"{tooltip_attrs}>'
        f"{escape(label)}</td>"
    )


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
        <summary class="filter-detail-summary flex cursor-pointer list-none items-center px-2 py-1 text-[0.8125rem] font-medium text-zinc-800">
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
        return "Unknown"
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
    if value is None:
        return "None"
    if value >= 1_024:
        thousands = math.floor(value / 1_024 + 0.5)
        return f"{thousands}K"
    return f"{value:,}"


def _fmt_embedding_dim(value: int | None) -> str:
    return "Unknown" if value is None else f"{value:,}"


def _fmt_row_embedding_dim(row: LeaderboardRow) -> str:
    if _is_sparse_or_bm25_row(row):
        return "sparse"
    return _fmt_embedding_dim(row.embedding_dim)


def _fmt_license(value: object) -> str:
    return _license_table_labels(value)[1]


def _license_table_labels(value: object) -> tuple[str, str]:
    if not isinstance(value, Mapping):
        return "", ""
    license_metadata = cast(Mapping[str, object], value)
    label = license_metadata.get("label") or license_metadata.get("id")
    full_label = str(label) if label else ""
    license_id = str(license_metadata.get("id") or "").strip().casefold()
    normalized_label = full_label.strip().casefold()
    short_labels = {
        "apache-2.0": "Apache",
        "mit": "MIT",
        "cc-by-nc-4.0": "CC BY-NC",
        "cc-by-nc-sa-4.0": "CC BY-NC",
        "openai-service-terms": "OpenAI",
        "gemma": "Gemma",
        "lfm1.0": "LFM",
    }
    label_prefixes = {
        "apache 2.0": "Apache",
        "cc by-nc 4.0": "CC BY-NC",
        "cc by-nc-sa 4.0": "CC BY-NC",
        "openai service terms": "OpenAI",
        "gemma terms": "Gemma",
        "lfm open license": "LFM",
    }
    short_label = short_labels.get(license_id)
    if short_label is None:
        short_label = next(
            (short for prefix, short in label_prefixes.items() if normalized_label.startswith(prefix)),
            full_label,
        )
    return short_label, full_label


def _model_type_table_labels(metadata: Mapping[str, object]) -> tuple[str, str]:
    full_label = str(metadata.get("model_type") or "")
    key = str(metadata.get("model_type_key") or "").casefold()
    short_labels = {
        "dense": "Dense",
        "sparse": "Sparse",
        "bm25": "BM25",
        "reranker": "Reranker",
        "late-interaction": "Late int.",
    }
    return short_labels.get(key, full_label), full_label


def _fmt_percent_delta(value: float | None) -> str:
    return "" if value is None else f"{value:+.1f}%"


def _metric_column_label(column: str, *, parent_label: str | None = None) -> str:
    parts = column.split("::")
    if len(parts) >= 3:
        dataset = parts[-2].rsplit("/", 1)[-1]
        task = parts[-1]
        if dataset == task:
            return dataset
        task = _strip_repeated_task_prefix(group_label=dataset, task_label=task)
        return f"{dataset}::{task}"
    if len(parts) == 2:
        if parts[0] == parts[1]:
            return parts[0]
        task = _strip_repeated_task_prefix(group_label=parts[0], task_label=parts[1])
        return f"{parts[0]}::{task}"
    if parent_label is not None:
        parent = parent_label.rsplit("/", 1)[-1]
        if _starts_with_ignore_case(column, parent):
            stripped = column[len(parent) :]
            if stripped:
                return stripped
            return column
    return column.removeprefix("Nano")


def _strip_repeated_task_prefix(*, group_label: str, task_label: str) -> str:
    if not _starts_with_ignore_case(task_label, group_label):
        return task_label
    stripped = task_label[len(group_label) :]
    return stripped or task_label


def _starts_with_ignore_case(value: str, prefix: str) -> bool:
    return value.casefold().startswith(prefix.casefold())


def _metric_column_label_markup(label: str) -> str:
    parts = [part for part in label.split("::") if part]
    if len(parts) <= 1:
        return f'<span class="block w-full truncate">{escape(label)}</span>'
    escaped_parts = [escape(part) for part in parts]
    first, rest = escaped_parts[0], escaped_parts[1:]
    return (
        f'<span class="block w-full truncate font-normal">{first}</span>'
        + "".join(f'<span class="block w-full truncate font-normal">{part}</span>' for part in rest)
    )


def _metric_column_header_parts(label: str) -> tuple[str, str]:
    parts = [part for part in label.split("::") if part]
    if len(parts) >= 3:
        group_label = parts[-2].rsplit("/", 1)[-1]
        return group_label, _strip_repeated_task_prefix(group_label=group_label, task_label=parts[-1])
    if len(parts) == 2:
        return parts[0], "" if parts[0] == parts[1] else _strip_repeated_task_prefix(
            group_label=parts[0], task_label=parts[1]
        )
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


def _metric_column_labels(
    columns: list[str],
    *,
    overrides: dict[str, str] | None = None,
    parent_label: str | None = None,
) -> dict[str, str]:
    overrides = overrides or {}
    labels_by_column = {
        column: overrides.get(column) or _metric_column_label(column, parent_label=parent_label)
        for column in columns
    }
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
