from __future__ import annotations

from html import escape
from pathlib import Path
from typing import cast
from urllib.parse import urlencode

from pydantic import BaseModel, ConfigDict

from nano_ir_benchmark.viewer.config import ViewerConfig, load_viewer_config
from nano_ir_benchmark.viewer.leaderboard import (
    LeaderboardResult,
    LeaderboardRow,
    LeaderboardService,
    SORT_COLUMNS,
    SortDirection,
)
from nano_ir_benchmark.viewer.store import LocalDuckDbStore


class ViewerAppConfig(BaseModel):
    model_config = ConfigDict(frozen=True)

    duckdb_path: Path
    config_dir: Path = Path("config/viewer")


def create_app(*, store: LocalDuckDbStore, config_dir: Path = Path("config/viewer")):
    from fastapi import FastAPI, Query
    from fastapi.responses import HTMLResponse

    viewer_config = load_viewer_config(config_dir)
    app = FastAPI(title="Nano IR Benchmark Viewer")

    @app.get("/", response_class=HTMLResponse)
    def index(
        view: str = Query(default=viewer_config.overall.name),
        sort: str = Query(default="borda_rank"),
        direction: str = Query(default="asc", pattern="^(asc|desc)$"),
        group: str | None = Query(default=None),
        variants: bool = Query(default=False),
        quantization: bool = Query(default=False),
        truncate: bool = Query(default=False),
        model_filter: str = Query(default=""),
    ) -> str:
        store.ensure_current()
        initial_query = _state_query(
            viewer_config=viewer_config,
            view=view,
            sort=sort,
            direction=direction,
            group=group,
            variants=variants,
            quantization=quantization,
            truncate=truncate,
            model_filter=model_filter,
        )
        return render_page(viewer_config=viewer_config, duckdb_path=store.path, initial_query=initial_query)

    @app.get("/leaderboard", response_class=HTMLResponse)
    def leaderboard(
        view: str = Query(default=viewer_config.overall.name),
        sort: str = Query(default="borda_rank"),
        direction: str = Query(default="asc", pattern="^(asc|desc)$"),
        group: str | None = Query(default=None),
        variants: bool = Query(default=False),
        quantization: bool = Query(default=False),
        truncate: bool = Query(default=False),
        model_filter: str = Query(default=""),
    ) -> HTMLResponse:
        store.ensure_current()
        state_query = _state_query(
            viewer_config=viewer_config,
            view=view,
            sort=sort,
            direction=direction,
            group=group,
            variants=variants,
            quantization=quantization,
            truncate=truncate,
            model_filter=model_filter,
        )
        view = state_query["view"]
        sort = state_query["sort"]
        direction = state_query["direction"]
        group = state_query.get("group")
        include_quantization_variants = state_query.get("quantization") == "1"
        include_truncate_variants = state_query.get("truncate") == "1"
        model_filter = state_query.get("model_filter", "")
        service = LeaderboardService(duckdb_path=store.path, config=viewer_config)
        result = service.get_leaderboard(
            view,
            sort=sort,
            direction=cast(SortDirection, direction),
            score_group_name=group,
            include_quantization_variants=include_quantization_variants,
            include_truncate_variants=include_truncate_variants,
        )
        content = render_leaderboard(result=result, sort=sort, direction=direction, model_filter=model_filter)
        return HTMLResponse(content=content, headers={"HX-Push-Url": f"/?{urlencode(state_query)}"})

    return app


def render_page(*, viewer_config: ViewerConfig, duckdb_path: Path, initial_query: dict[str, str] | None = None) -> str:
    query = urlencode(initial_query or {"view": viewer_config.overall.name, "sort": "borda_rank", "direction": "asc"})
    return f"""<!doctype html>
<html lang="ja">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Nano IR Benchmark Viewer</title>
  <link rel="canonical" href="/">
  <script src="https://cdn.tailwindcss.com"></script>
  <script src="https://unpkg.com/htmx.org@2.0.8"></script>
</head>
<body class="bg-zinc-50 text-zinc-950">
  <main class="mx-auto max-w-[1500px] px-4 py-6 sm:px-6">
    <header class="mb-5 border-b border-zinc-200 pb-4">
      <p class="text-sm font-medium text-cyan-700">Nano IR benchmark viewer</p>
      <h1 class="mt-1 text-2xl font-semibold">Borda leaderboard</h1>
      <p class="mt-2 text-sm text-zinc-600">DuckDB: <span class="font-mono">{escape(str(duckdb_path))}</span></p>
    </header>
    <section
      id="leaderboard-panel"
      hx-get="{_leaderboard_url(query)}"
      hx-trigger="load"
      hx-swap="innerHTML"
    >
      <div class="border border-zinc-200 bg-white px-4 py-3 text-sm text-zinc-600">Loading leaderboard...</div>
    </section>
  </main>
</body>
</html>"""


def render_leaderboard(*, result: LeaderboardResult, sort: str, direction: str, model_filter: str = "") -> str:
    return f"""
<div>
  {render_tabs(result=result, sort=sort, direction=direction, model_filter=model_filter)}
  {render_controls(result=result, sort=sort, direction=direction, model_filter=model_filter)}
  {render_score_groups(result=result, sort=sort, direction=direction, model_filter=model_filter)}
  <div class="mb-3 flex flex-wrap items-end justify-between gap-3">
    <div>
      <h2 class="text-lg font-semibold">{escape(result.view_label)}</h2>
      <p class="mt-1 text-sm text-zinc-600">{len(result.rows)} complete models / {result.expected_tasks} tasks</p>
    </div>
  </div>
  <div class="overflow-x-auto border border-zinc-200 bg-white">
    <table class="min-w-full border-collapse text-sm">
      {render_table_head(result=result, sort=sort, direction=direction, model_filter=model_filter)}
      {render_table_body(result=result, model_filter=model_filter)}
    </table>
  </div>
</div>
"""


def render_tabs(*, result: LeaderboardResult, sort: str, direction: str, model_filter: str = "") -> str:
    buttons: list[str] = []
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
        query_payload = _state_payload(result=result, sort=tab_sort, direction=tab_direction, model_filter=model_filter)
        query_payload["view"] = view_name
        query = urlencode(query_payload)
        buttons.append(
            f"""<button type="button" class="border px-3 py-1.5 text-sm {classes}"
                  hx-get="{_leaderboard_url(query)}" hx-push-url="{_page_url(query_payload)}"
                  hx-target="#leaderboard-panel" hx-swap="innerHTML">
                  {escape(view_label)}
                </button>"""
        )
    return f"""<nav class="mb-4 flex flex-wrap gap-2" aria-label="Benchmark views">{''.join(buttons)}</nav>"""


def render_controls(*, result: LeaderboardResult, sort: str, direction: str, model_filter: str = "") -> str:
    quantization_checked = " checked" if result.include_quantization_variants else ""
    truncate_checked = " checked" if result.include_truncate_variants else ""
    hidden_fields = [
        ("view", result.view_name),
        ("sort", sort),
        ("direction", direction),
    ]
    if result.selected_score_group is not None:
        hidden_fields.append(("group", result.selected_score_group.name))
    hidden_html = "".join(
        f"""<input type="hidden" name="{escape(name)}" value="{escape(value)}">""" for name, value in hidden_fields
    )
    return f"""
    <form class="mb-4 flex flex-wrap items-center gap-x-5 gap-y-2 text-sm text-zinc-700"
          hx-get="/leaderboard" hx-push-url="true"
          hx-target="#leaderboard-panel" hx-swap="innerHTML"
          hx-trigger="change from:input[type='checkbox'], input changed delay:700ms from:input[name='model_filter']">
      {hidden_html}
      <div class="flex flex-wrap items-center gap-3">
        <span class="font-medium text-zinc-800">Variants:</span>
        <label class="inline-flex items-center gap-2">
          <input type="checkbox" name="quantization" value="1" class="h-4 w-4 accent-cyan-700"{quantization_checked}>
          <span>Quantization</span>
        </label>
        <label class="inline-flex items-center gap-2">
          <input type="checkbox" name="truncate" value="1" class="h-4 w-4 accent-cyan-700"{truncate_checked}>
          <span>Truncate dims</span>
        </label>
      </div>
      <label class="flex min-w-64 items-center gap-2">
        <span class="font-medium text-zinc-800">Model name</span>
        <input type="search" name="model_filter" value="{escape(model_filter)}"
               class="w-72 max-w-full border border-zinc-300 bg-white px-2 py-1 text-sm text-zinc-900 outline-none focus:border-cyan-700"
               autocomplete="off">
      </label>
    </form>
    """


def render_score_groups(*, result: LeaderboardResult, sort: str, direction: str, model_filter: str = "") -> str:
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
        query_payload = _state_payload(result=result, sort="borda_rank", direction="asc", model_filter=model_filter)
        query_payload["group"] = score_group.name
        query = urlencode(query_payload)
        page_url = _page_url(query_payload)
        buttons.append(
            f"""<button type="button" class="border px-3 py-1.5 text-sm {classes}"
                  hx-get="{_leaderboard_url(query)}" hx-push-url="{page_url}"
                  hx-target="#leaderboard-panel" hx-swap="innerHTML">
                  {escape(score_group.label)}
                </button>"""
        )
    return f"""<nav class="mb-4 flex flex-wrap gap-2" aria-label="Score groups">{''.join(buttons)}</nav>"""


def render_table_head(*, result: LeaderboardResult, sort: str, direction: str, model_filter: str = "") -> str:
    columns = [
        ("borda_rank", "Borda", "asc", "right", False),
        ("mean_rank", "Mean", "asc", "right", False),
        ("model_name", "Model Name", "asc", "left", False),
        ("borda_score", "Borda Score", "desc", "right", False),
    ]
    if result.is_overall:
        columns.extend(
            [
                ("macro_mean", "Macro Mean", "desc", "right", False),
                ("micro_mean", "Micro Mean", "desc", "right", False),
            ]
        )
    else:
        columns.append(("mean_score", "Mean Score", "desc", "right", False))
        columns.extend(
            (f"metric:{column}", _metric_column_label(column), "desc", "right", True)
            for column in result.metric_columns
        )
    columns.extend(
        [
            ("task_count", "Tasks", "desc", "right", False),
            ("active_parameters", "Active Params", "asc", "right", False),
            ("total_parameters", "Total Params", "asc", "right", False),
            ("max_seq_length", "Max Len", "desc", "right", False),
            ("embedding_dim", "Dims", "desc", "right", False),
            ("quantization", "Quantization", "asc", "left", False),
        ]
    )
    heads = []
    for key, label, default_direction, align, is_metric in columns:
        next_direction = _next_direction(key=key, sort=sort, direction=direction, default_direction=default_direction)
        indicator = " ▲" if sort == key and direction == "asc" else " ▼" if sort == key else ""
        query_payload = _state_payload(result=result, sort=key, direction=next_direction, model_filter=model_filter)
        query = urlencode(query_payload)
        justify = "justify-end" if align == "right" else "justify-start"
        text_align = "text-right" if align == "right" else "text-left"
        th_spacing = "w-[4.75rem] min-w-[4.75rem] max-w-[4.75rem] px-1.5 normal-case" if is_metric else "px-3 uppercase"
        label_class = "min-w-0 leading-tight [overflow-wrap:anywhere]" if is_metric else ""
        heads.append(
            f"""<th scope="col" class="bg-zinc-100 py-2 text-xs font-semibold text-zinc-600 {text_align} {th_spacing}">
                 <button type="button" class="inline-flex w-full {justify} hover:text-cyan-700"
                         hx-get="{_leaderboard_url(query)}" hx-push-url="{_page_url(query_payload)}"
                         hx-target="#leaderboard-panel" hx-swap="innerHTML">
                   <span class="{label_class}">{escape(label)}</span><span class="shrink-0 text-zinc-400">{indicator}</span>
                 </button>
               </th>"""
        )
    return f"<thead><tr>{''.join(heads)}</tr></thead>"


def render_table_body(*, result: LeaderboardResult, model_filter: str = "") -> str:
    if not result.rows:
        return """<tbody><tr><td class="px-3 py-5 text-center text-zinc-500" colspan="12">No complete results found.</td></tr></tbody>"""
    body_rows = []
    normalized_filter = _active_model_filter(model_filter)
    for row in result.rows:
        hidden = bool(normalized_filter and normalized_filter not in row.model_name.lower())
        row_class = "border-t border-zinc-200 odd:bg-white even:bg-zinc-50"
        hidden_attrs = ' hidden data-filter-hidden="true"' if hidden else ""
        mean_cells = (
            f"""<td class="px-3 py-2 text-right tabular-nums">{_fmt_score(row.macro_mean)}</td>
                <td class="px-3 py-2 text-right tabular-nums">{_fmt_score(row.micro_mean)}</td>"""
            if result.is_overall
            else f"""<td class="px-3 py-2 text-right tabular-nums">{_fmt_score(row.mean_score)}</td>"""
        )
        body_rows.append(
            f"""<tr class="{row_class}"{hidden_attrs}>
              <td class="px-3 py-2 text-right tabular-nums">{_fmt_rank(row.borda_rank)}</td>
              <td class="px-3 py-2 text-right tabular-nums">{_fmt_rank(row.mean_rank)}</td>
              {_render_model_name_cell(row)}
              <td class="px-3 py-2 text-right tabular-nums">{_fmt_score(row.borda_score)}</td>
              {mean_cells}
              {_render_metric_cells(result=result, row=row)}
              <td class="px-3 py-2 text-right tabular-nums">{row.task_count}</td>
              <td class="px-3 py-2 text-right tabular-nums">{_fmt_params(row.active_parameters)}</td>
              <td class="px-3 py-2 text-right tabular-nums">{_fmt_params(row.total_parameters)}</td>
              <td class="px-3 py-2 text-right tabular-nums">{_fmt_max_len(row.max_seq_length)}</td>
              <td class="px-3 py-2 text-right tabular-nums">{_fmt_embedding_dim(row.embedding_dim)}</td>
              <td class="px-3 py-2 text-left">{escape(row.quantization or "")}</td>
            </tr>"""
        )
    return f"<tbody>{''.join(body_rows)}</tbody>"


def _render_metric_cells(*, result: LeaderboardResult, row: LeaderboardRow) -> str:
    values = row.metric_values
    return "".join(
        f"""<td class="w-[4.75rem] min-w-[4.75rem] max-w-[4.75rem] px-1.5 py-2 text-right tabular-nums">{_fmt_score(values.get(column))}</td>"""
        for column in result.metric_columns
    )


def _render_model_name_cell(row: LeaderboardRow) -> str:
    details = _model_variant_details(row)
    model_name = row.model_name
    if details:
        suffix = f" ({', '.join(details)})"
        if model_name.endswith(suffix):
            model_name = model_name[: -len(suffix)]
    badges = []
    if row.embedding_dim is not None:
        badges.append(
            f"""<span class="inline-flex items-center border border-cyan-200 bg-cyan-50 px-1.5 py-0.5 text-xs font-medium text-cyan-800">{escape(f"{row.embedding_dim:,} dims")}</span>"""
        )
    if row.quantization:
        badges.append(
            f"""<span class="inline-flex items-center border border-amber-200 bg-amber-50 px-1.5 py-0.5 text-xs font-medium text-amber-800">{escape(row.quantization)}</span>"""
        )
    badge_html = f"""<span class="ml-2 inline-flex flex-wrap gap-1 align-middle">{''.join(badges)}</span>""" if badges else ""
    return f"""<td class="whitespace-nowrap px-3 py-2 font-medium">{escape(model_name)}{badge_html}</td>"""


def _model_variant_details(row: LeaderboardRow) -> list[str]:
    details = []
    if row.embedding_dim is not None:
        details.append(f"{row.embedding_dim} dims")
    if row.quantization:
        details.append(row.quantization)
    return details


def _active_model_filter(model_filter: str) -> str:
    normalized = model_filter.strip().lower()
    return normalized if len(normalized) >= 3 else ""


def _next_direction(*, key: str, sort: str, direction: str, default_direction: str) -> str:
    if key != sort:
        return default_direction
    return "desc" if direction == "asc" else "asc"


def _fmt_rank(value: float) -> str:
    return str(int(value)) if float(value).is_integer() else f"{value:.1f}"


def _fmt_score(value: float | None) -> str:
    return "" if value is None else f"{value:.2f}"


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


def _metric_column_label(column: str) -> str:
    return column.removeprefix("Nano")


def _state_payload(
    *,
    result: LeaderboardResult,
    sort: str,
    direction: str,
    model_filter: str = "",
) -> dict[str, str]:
    query_payload = {"view": result.view_name, "sort": sort, "direction": direction}
    if result.selected_score_group is not None:
        query_payload["group"] = result.selected_score_group.name
    if result.include_quantization_variants:
        query_payload["quantization"] = "1"
    if result.include_truncate_variants:
        query_payload["truncate"] = "1"
    if model_filter:
        query_payload["model_filter"] = model_filter
    return query_payload


def _state_query(
    *,
    viewer_config: ViewerConfig,
    view: str,
    sort: str,
    direction: str,
    group: str | None,
    variants: bool,
    quantization: bool,
    truncate: bool,
    model_filter: str,
) -> dict[str, str]:
    if view not in viewer_config.view_names:
        view = viewer_config.overall.name
    if sort not in SORT_COLUMNS and not sort.startswith("metric:"):
        sort = "borda_rank"
    if direction not in {"asc", "desc"}:
        direction = "asc"
    if variants:
        quantization = True
        truncate = True

    query = {"view": view, "sort": sort, "direction": direction}
    if group:
        query["group"] = group
    if quantization:
        query["quantization"] = "1"
    if truncate:
        query["truncate"] = "1"
    model_filter = model_filter.strip()
    if model_filter:
        query["model_filter"] = model_filter
    return query


def _page_url(query: dict[str, str]) -> str:
    return escape(f"/?{urlencode(query)}", quote=True)


def _leaderboard_url(query: str) -> str:
    return escape(f"/leaderboard?{query}", quote=True)
