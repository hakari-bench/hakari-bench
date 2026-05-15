from __future__ import annotations

from collections import defaultdict
from html import escape
import json
import re
from typing import Any

from pydantic import BaseModel, ConfigDict, Field

from hakari_bench.viewer.leaderboard import LeaderboardRow


class ModelCellView(BaseModel):
    model_config = ConfigDict(frozen=True)

    display_name: str
    full_model_name: str
    ranking_model_name: str
    dimension_label: str | None = None
    dimension_tooltip: str | None = None
    variant_label: str | None = None
    variant_tooltip: str | None = None
    metadata: dict[str, Any] = Field(default_factory=dict)


def model_cell_views(rows: list[LeaderboardRow]) -> dict[str, ModelCellView]:
    base_names = {row.model_name: _base_model_name(row) for row in rows}
    original_dims = _original_embedding_dims(rows=rows, base_names=base_names)
    full_names_by_short_name: dict[str, set[str]] = defaultdict(set)
    for full_model_name in base_names.values():
        full_names_by_short_name[_short_model_name(full_model_name)].add(full_model_name)

    return {
        row.model_name: ModelCellView(
            display_name=_display_name(
                full_model_name=full_model_name,
                full_names_by_short_name=full_names_by_short_name,
            ),
            full_model_name=full_model_name,
            ranking_model_name=row.model_name,
            dimension_label=_dimension_label(row),
            dimension_tooltip=None,
            variant_label=_variant_label(row, original_dim=original_dims.get(_source_key(row=row, full_model_name=full_model_name))),
            variant_tooltip=_variant_tooltip(row, original_dim=original_dims.get(_source_key(row=row, full_model_name=full_model_name))),
            metadata=_model_metadata(row=row, full_model_name=full_model_name),
        )
        for row in rows
        for full_model_name in [base_names[row.model_name]]
    }


def _display_name(
    *,
    full_model_name: str,
    full_names_by_short_name: dict[str, set[str]],
) -> str:
    short_name = _short_model_name(full_model_name)
    return full_model_name if len(full_names_by_short_name[short_name]) > 1 else short_name


def _short_model_name(model_name: str) -> str:
    owner, separator, name = model_name.partition("/")
    return name if separator and owner and name else model_name


def _base_model_name(row: LeaderboardRow) -> str:
    model_name = row.model_name
    for details in _model_name_suffix_detail_candidates(row):
        suffix = f" ({', '.join(details)})"
        if model_name.endswith(suffix):
            return model_name[: -len(suffix)]
    return model_name


def _model_name_suffix_detail_candidates(row: LeaderboardRow) -> list[list[str]]:
    details = []
    if row.embedding_dim is not None:
        details.append(f"{row.embedding_dim} dims")
    if row.quantization:
        details.append(row.quantization)
    with_variant = [*details, row.embedding_variant_name] if row.embedding_variant_name else []
    candidates = [candidate for candidate in (with_variant, details) if candidate]
    if row.embedding_dim is not None:
        candidates.append([f"{row.embedding_dim} dims"])
    return candidates


def _original_embedding_dims(*, rows: list[LeaderboardRow], base_names: dict[str, str]) -> dict[str, int]:
    original_dims: dict[str, int] = {}
    for row in rows:
        if row.embedding_dim is None or (row.embedding_variant_name is not None and row.embedding_variant_name != "base"):
            continue
        full_model_name = base_names[row.model_name]
        original_dims[_source_key(row=row, full_model_name=full_model_name)] = row.embedding_dim
    return original_dims


def _source_key(*, row: LeaderboardRow, full_model_name: str) -> str:
    return row.source_model_name or full_model_name


def _dimension_label(row: LeaderboardRow) -> str | None:
    if row.embedding_dim is None or _truncate_dim(row) is not None:
        return None
    return f"{row.embedding_dim}d"


def _variant_label(row: LeaderboardRow, *, original_dim: int | None) -> str | None:
    variant_name = row.embedding_variant_name
    if variant_name is None or variant_name == "base":
        return None
    truncate_dim = _truncate_dim(row)
    if truncate_dim is not None:
        return f"{truncate_dim}d <- {original_dim}" if original_dim is not None else f"{truncate_dim}d"
    if row.quantization is not None and variant_name.casefold() == row.quantization.casefold():
        return None
    return variant_name


def _variant_tooltip(row: LeaderboardRow, *, original_dim: int | None) -> str | None:
    truncate_dim = _truncate_dim(row)
    if truncate_dim is None:
        return None
    if original_dim is None:
        return f"This result was evaluated after truncating embeddings to {truncate_dim} dimensions."
    return (
        f"Original embedding dimension is {original_dim}. "
        f"This result was evaluated after truncating embeddings to {truncate_dim} dimensions."
    )


def _truncate_dim(row: LeaderboardRow) -> int | None:
    variant_name = row.embedding_variant_name or ""
    match = re.search(r"(?:^|_)truncate_dim_(\d+)(?:_|$)", variant_name)
    if match is not None:
        return int(match.group(1))
    return None


def _model_metadata(*, row: LeaderboardRow, full_model_name: str) -> dict[str, Any]:
    return {
        "model_name": full_model_name,
        "ranking_model_name": row.model_name,
        "embedding_variant_name": row.embedding_variant_name,
        "embedding_dim": row.embedding_dim,
        "quantization": row.quantization,
        "base_score_delta_percent": row.base_score_delta_percent,
        "active_parameters": row.active_parameters,
        "total_parameters": row.total_parameters,
        "max_seq_length": row.max_seq_length,
        "dtype": row.dtype,
        "attention": row.attn_implementation,
        "prompt": row.prompt_summary,
        "trust_remote_code": row.trust_remote_code,
    }


def render_model_name_cell(row: LeaderboardRow, model_view: ModelCellView) -> str:
    metadata_json = json.dumps(model_view.metadata, ensure_ascii=False, separators=(",", ":"))
    badges = []
    if model_view.dimension_label is not None:
        badges.append(
            _render_badge(
                label=model_view.dimension_label,
                classes="border-cyan-200 bg-cyan-50 text-cyan-800",
                tooltip=model_view.dimension_tooltip,
            )
        )
    if row.quantization:
        badges.append(
            _render_badge(
                label=row.quantization,
                classes="border-amber-200 bg-amber-50 text-amber-800",
            )
        )
    if model_view.variant_label:
        badges.append(
            _render_badge(
                label=model_view.variant_label,
                classes="border-violet-200 bg-violet-50 text-violet-800",
                tooltip=model_view.variant_tooltip,
            )
        )
    badge_html = f"""<span class="ml-2 inline-flex flex-wrap gap-1 align-middle">{''.join(badges)}</span>""" if badges else ""
    return f"""<td class="sticky left-32 z-10 whitespace-nowrap bg-inherit px-3 py-2 font-medium">
      <button type="button" class="model-detail-trigger text-left font-medium text-cyan-800 underline-offset-2 hover:underline"
              data-model-metadata="{escape(metadata_json)}">{escape(model_view.display_name)}</button>{badge_html}
    </td>"""


def _render_badge(*, label: str, classes: str, tooltip: str | None = None) -> str:
    escaped_tooltip = escape(tooltip, quote=True) if tooltip else ""
    tooltip_attrs = f' tabindex="0" data-tooltip="{escaped_tooltip}" aria-label="{escaped_tooltip}"' if tooltip else ""
    tooltip_class = "tooltip-trigger tooltip-delay " if tooltip else ""
    return (
        f"""<span class="{tooltip_class}inline-flex items-center border px-1.5 py-0.5 text-xs font-medium {classes}"{tooltip_attrs}>"""
        f"{escape(label)}</span>"
    )


def render_model_detail_modal() -> str:
    return """
<dialog id="model-detail-modal" class="w-[min(92vw,42rem)] border border-zinc-300 bg-white p-0 text-zinc-950 backdrop:bg-zinc-950/35">
  <form method="dialog">
    <div class="flex items-center justify-between border-b border-zinc-200 px-4 py-3">
      <h3 class="text-base font-semibold">Model Details</h3>
      <button type="submit" class="border border-zinc-300 px-2 py-1 text-sm text-zinc-700 hover:border-cyan-600 hover:text-cyan-700">Close</button>
    </div>
  </form>
  <div class="px-4 py-3">
    <p id="model-detail-title" class="break-all font-mono text-sm font-semibold text-zinc-900"></p>
    <dl id="model-detail-fields" class="mt-3 grid grid-cols-[10rem_1fr] gap-x-3 gap-y-2 text-sm"></dl>
  </div>
</dialog>
<script>
(() => {
  if (window.__hakariModelDetailsBound) return;
  window.__hakariModelDetailsBound = true;
    const fields = [
    ["Ranking label", "ranking_model_name"],
    ["Variant", "embedding_variant_name"],
    ["Dimensions", "embedding_dim"],
    ["Quantization", "quantization"],
    ["Base delta", "base_score_delta_percent"],
    ["Active params", "active_parameters"],
    ["Total params", "total_parameters"],
    ["Max len", "max_seq_length"],
    ["DType", "dtype"],
    ["Attention", "attention"],
    ["Prompt", "prompt"],
    ["HF trust", "trust_remote_code"],
  ];
  const fmt = (value) => {
    if (value === null || value === undefined || value === "") return "";
    if (typeof value === "boolean") return value ? "true" : "false";
    if (typeof value === "number") return value.toLocaleString();
    return String(value);
  };
  document.addEventListener("click", (event) => {
    const trigger = event.target.closest(".model-detail-trigger");
    if (!trigger) return;
    const modal = document.getElementById("model-detail-modal");
    const title = document.getElementById("model-detail-title");
    const list = document.getElementById("model-detail-fields");
    if (!modal || !title || !list) return;
    const metadata = JSON.parse(trigger.dataset.modelMetadata || "{}");
    title.textContent = metadata.model_name || trigger.textContent || "";
    list.replaceChildren();
    for (const [label, key] of fields) {
      const value = fmt(metadata[key]);
      if (!value) continue;
      const dt = document.createElement("dt");
      dt.className = "font-medium text-zinc-600";
      dt.textContent = label;
      const dd = document.createElement("dd");
      dd.className = "break-all font-mono text-zinc-900";
      dd.textContent = value;
      list.append(dt, dd);
    }
    if (typeof modal.showModal === "function") modal.showModal();
  });
  const modal = document.getElementById("model-detail-modal");
  if (modal) {
    modal.addEventListener("click", (event) => {
      if (event.target === modal) modal.close();
    });
  }
  document.addEventListener("submit", (event) => {
    if (event.target?.id !== "display-controls") return;
    const activeId = document.activeElement?.id;
    window.__hakariRestoreModelFilterFocus = activeId === "model-filter-input";
    window.__hakariRestoreTaskFilterFocus = activeId === "task-filter-input";
  });
  document.addEventListener("htmx:afterSwap", (event) => {
    if (
      event.target?.id !== "leaderboard-panel" ||
      (!window.__hakariRestoreModelFilterFocus && !window.__hakariRestoreTaskFilterFocus)
    ) return;
    const inputId = window.__hakariRestoreTaskFilterFocus ? "task-filter-input" : "model-filter-input";
    window.__hakariRestoreModelFilterFocus = false;
    window.__hakariRestoreTaskFilterFocus = false;
    const input = document.getElementById(inputId);
    if (!input) return;
    input.focus();
    const end = input.value.length;
    if (typeof input.setSelectionRange === "function") input.setSelectionRange(end, end);
  });
})();
</script>
"""
