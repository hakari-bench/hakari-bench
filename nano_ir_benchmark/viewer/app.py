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
    ) -> str:
        store.ensure_current()
        initial_query = _state_query(
            viewer_config=viewer_config,
            view=view,
            sort=sort,
            direction=direction,
            group=group,
        )
        return render_page(viewer_config=viewer_config, duckdb_path=store.path, initial_query=initial_query)

    @app.get("/leaderboard", response_class=HTMLResponse)
    def leaderboard(
        view: str = Query(default=viewer_config.overall.name),
        sort: str = Query(default="borda_rank"),
        direction: str = Query(default="asc", pattern="^(asc|desc)$"),
        group: str | None = Query(default=None),
    ) -> str:
        store.ensure_current()
        state_query = _state_query(
            viewer_config=viewer_config,
            view=view,
            sort=sort,
            direction=direction,
            group=group,
        )
        view = state_query["view"]
        sort = state_query["sort"]
        direction = state_query["direction"]
        group = state_query.get("group")
        service = LeaderboardService(duckdb_path=store.path, config=viewer_config)
        result = service.get_leaderboard(
            view,
            sort=sort,
            direction=cast(SortDirection, direction),
            score_group_name=group,
        )
        return render_leaderboard(result=result, sort=sort, direction=direction)

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


def render_leaderboard(*, result: LeaderboardResult, sort: str, direction: str) -> str:
    return f"""
<div>
  {render_tabs(result=result, sort=sort, direction=direction)}
  {render_score_groups(result=result, sort=sort, direction=direction)}
  <div class="mb-3 flex flex-wrap items-end justify-between gap-3">
    <div>
      <h2 class="text-lg font-semibold">{escape(result.view_label)}</h2>
      <p class="mt-1 text-sm text-zinc-600">{len(result.rows)} complete models / {result.expected_tasks} tasks</p>
    </div>
  </div>
  <div class="overflow-x-auto border border-zinc-200 bg-white">
    <table class="min-w-full border-collapse text-sm">
      {render_table_head(result=result, sort=sort, direction=direction)}
      {render_table_body(result=result)}
    </table>
  </div>
</div>
"""


def render_tabs(*, result: LeaderboardResult, sort: str, direction: str) -> str:
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
        query_payload = {"view": view_name, "sort": tab_sort, "direction": tab_direction}
        query = urlencode(query_payload)
        buttons.append(
            f"""<button type="button" class="border px-3 py-1.5 text-sm {classes}"
                  hx-get="{_leaderboard_url(query)}" hx-push-url="{_page_url(query_payload)}"
                  hx-target="#leaderboard-panel" hx-swap="innerHTML">
                  {escape(view_label)}
                </button>"""
        )
    return f"""<nav class="mb-4 flex flex-wrap gap-2" aria-label="Benchmark views">{''.join(buttons)}</nav>"""


def render_score_groups(*, result: LeaderboardResult, sort: str, direction: str) -> str:
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
        query = urlencode(
            {"view": result.view_name, "sort": "borda_rank", "direction": "asc", "group": score_group.name}
        )
        page_url = _page_url(
            {"view": result.view_name, "sort": "borda_rank", "direction": "asc", "group": score_group.name}
        )
        buttons.append(
            f"""<button type="button" class="border px-3 py-1.5 text-sm {classes}"
                  hx-get="{_leaderboard_url(query)}" hx-push-url="{page_url}"
                  hx-target="#leaderboard-panel" hx-swap="innerHTML">
                  {escape(score_group.label)}
                </button>"""
        )
    return f"""<nav class="mb-4 flex flex-wrap gap-2" aria-label="Score groups">{''.join(buttons)}</nav>"""


def render_table_head(*, result: LeaderboardResult, sort: str, direction: str) -> str:
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
        ]
    )
    heads = []
    for key, label, default_direction, align, is_metric in columns:
        next_direction = _next_direction(key=key, sort=sort, direction=direction, default_direction=default_direction)
        indicator = " ▲" if sort == key and direction == "asc" else " ▼" if sort == key else ""
        query_payload = {"view": result.view_name, "sort": key, "direction": next_direction}
        if result.selected_score_group is not None:
            query_payload["group"] = result.selected_score_group.name
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


def render_table_body(*, result: LeaderboardResult) -> str:
    if not result.rows:
        return """<tbody><tr><td class="px-3 py-5 text-center text-zinc-500" colspan="10">No complete results found.</td></tr></tbody>"""
    body_rows = []
    for row in result.rows:
        mean_cells = (
            f"""<td class="px-3 py-2 text-right tabular-nums">{_fmt_score(row.macro_mean)}</td>
                <td class="px-3 py-2 text-right tabular-nums">{_fmt_score(row.micro_mean)}</td>"""
            if result.is_overall
            else f"""<td class="px-3 py-2 text-right tabular-nums">{_fmt_score(row.mean_score)}</td>"""
        )
        body_rows.append(
            f"""<tr class="border-t border-zinc-200 odd:bg-white even:bg-zinc-50">
              <td class="px-3 py-2 text-right tabular-nums">{_fmt_rank(row.borda_rank)}</td>
              <td class="px-3 py-2 text-right tabular-nums">{_fmt_rank(row.mean_rank)}</td>
              <td class="whitespace-nowrap px-3 py-2 font-medium">{escape(row.model_name)}</td>
              <td class="px-3 py-2 text-right tabular-nums">{_fmt_score(row.borda_score)}</td>
              {mean_cells}
              {_render_metric_cells(result=result, row=row)}
              <td class="px-3 py-2 text-right tabular-nums">{row.task_count}</td>
              <td class="px-3 py-2 text-right tabular-nums">{_fmt_params(row.active_parameters)}</td>
              <td class="px-3 py-2 text-right tabular-nums">{_fmt_params(row.total_parameters)}</td>
              <td class="px-3 py-2 text-right tabular-nums">{_fmt_max_len(row.max_seq_length)}</td>
            </tr>"""
        )
    return f"<tbody>{''.join(body_rows)}</tbody>"


def _render_metric_cells(*, result: LeaderboardResult, row: LeaderboardRow) -> str:
    values = row.metric_values
    return "".join(
        f"""<td class="w-[4.75rem] min-w-[4.75rem] max-w-[4.75rem] px-1.5 py-2 text-right tabular-nums">{_fmt_score(values.get(column))}</td>"""
        for column in result.metric_columns
    )


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


def _metric_column_label(column: str) -> str:
    return column.removeprefix("Nano")


def _state_query(
    *,
    viewer_config: ViewerConfig,
    view: str,
    sort: str,
    direction: str,
    group: str | None,
) -> dict[str, str]:
    if view not in viewer_config.view_names:
        view = viewer_config.overall.name
    if sort not in SORT_COLUMNS and not sort.startswith("metric:"):
        sort = "borda_rank"
    if direction not in {"asc", "desc"}:
        direction = "asc"

    query = {"view": view, "sort": sort, "direction": direction}
    if group:
        query["group"] = group
    return query


def _page_url(query: dict[str, str]) -> str:
    return escape(f"/?{urlencode(query)}", quote=True)


def _leaderboard_url(query: str) -> str:
    return escape(f"/leaderboard?{query}", quote=True)
