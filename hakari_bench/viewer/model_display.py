from __future__ import annotations

from collections import defaultdict
from html import escape
import json
import re
from typing import Any

from pydantic import BaseModel, ConfigDict, Field

from hakari_bench.viewer.leaderboard import LeaderboardRow
from hakari_bench.viewer.model_types import normalized_model_type


_OPENAI_EMBEDDING_MODELS = {
    "openai/text-embedding-3-small": {
        "url": "https://developers.openai.com/api/docs/models/text-embedding-3-small",
        "max_seq_length": 8192,
    },
    "openai/text-embedding-3-large": {
        "url": "https://developers.openai.com/api/docs/models/text-embedding-3-large",
        "max_seq_length": 8192,
    },
}


class ModelCellView(BaseModel):
    model_config = ConfigDict(frozen=True)

    display_name: str
    full_model_name: str
    ranking_model_name: str
    model_type_label: str
    model_type_badge_label: str | None = None
    dimension_label: str | None = None
    dimension_tooltip: str | None = None
    original_embedding_dim: int | None = None
    truncated_embedding_dim: int | None = None
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
            model_type_label=model_type_view["label"] or "",
            model_type_badge_label=model_type_view["badge_label"],
            dimension_label=_dimension_label(row, model_type_key=model_type_view["key"]),
            dimension_tooltip=None,
            original_embedding_dim=_original_dim_for_view(row=row, original_dim=original_dim),
            truncated_embedding_dim=truncate_dim,
            variant_label=_variant_label(row, original_dim=original_dim, model_type_key=model_type_view["key"]),
            variant_tooltip=_variant_tooltip(row, original_dim=original_dim, model_type_key=model_type_view["key"]),
            metadata=_model_metadata(
                row=row,
                full_model_name=full_model_name,
                original_embedding_dim=_original_dim_for_view(row=row, original_dim=original_dim),
                truncated_embedding_dim=truncate_dim,
            ),
        )
        for row in rows
        for full_model_name in [base_names[row.model_name]]
        for original_dim in [original_dims.get(_source_key(row=row, full_model_name=full_model_name))]
        for truncate_dim in [_truncate_dim(row)]
        for model_type_view in [_model_type_view(row=row, full_model_name=full_model_name)]
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


def _original_dim_for_view(*, row: LeaderboardRow, original_dim: int | None) -> int | None:
    if _truncate_dim(row) is not None:
        return original_dim
    return original_dim or row.embedding_dim


def _source_key(*, row: LeaderboardRow, full_model_name: str) -> str:
    return row.source_model_name or full_model_name


def _dimension_label(row: LeaderboardRow, *, model_type_key: str | None) -> str | None:
    if model_type_key in {"sparse", "bm25"} or row.embedding_dim is None or _truncate_dim(row) is not None:
        return None
    return f"{row.embedding_dim}d"


def _variant_label(row: LeaderboardRow, *, original_dim: int | None, model_type_key: str | None) -> str | None:
    variant_name = row.embedding_variant_name
    if variant_name is None or variant_name == "base":
        return None
    truncate_dim = _truncate_dim(row)
    if truncate_dim is not None:
        return f"{truncate_dim}d <- {original_dim}" if original_dim is not None else f"{truncate_dim}d"
    if model_type_key == "sparse":
        sparse_label = _sparse_active_dims_label(variant_name)
        if sparse_label is not None:
            return sparse_label
    if row.quantization is not None and variant_name.casefold() == row.quantization.casefold():
        return None
    return variant_name


def _variant_tooltip(row: LeaderboardRow, *, original_dim: int | None, model_type_key: str | None) -> str | None:
    variant_name = row.embedding_variant_name or ""
    if model_type_key == "sparse":
        sparse_tooltip = _sparse_active_dims_tooltip(variant_name)
        if sparse_tooltip is not None:
            return sparse_tooltip
    truncate_dim = _truncate_dim(row)
    if truncate_dim is None:
        return None
    if original_dim is None:
        return f"This result was evaluated after truncating embeddings to {truncate_dim} dimensions."
    return (
        f"Original embedding dimension is {original_dim}. "
        f"This result was evaluated after truncating embeddings to {truncate_dim} dimensions."
    )


def _sparse_active_dims_label(variant_name: str) -> str | None:
    query_dim, document_dim = _sparse_active_dims(variant_name)
    labels = []
    if query_dim is not None:
        labels.append(f"q{query_dim}d")
    if document_dim is not None:
        labels.append(f"d{document_dim}d")
    return " ".join(labels) if labels else None


def _sparse_active_dims_tooltip(variant_name: str) -> str | None:
    query_dim, document_dim = _sparse_active_dims(variant_name)
    if query_dim is None and document_dim is None:
        return None
    details = ["Sparse active dimension cap."]
    if query_dim is not None:
        details.append(f"Query max active dims: {query_dim}.")
    if document_dim is not None:
        details.append(f"Document max active dims: {document_dim}.")
    details.append(f"Full variant: {variant_name}")
    return " ".join(details)


def _sparse_active_dims(variant_name: str) -> tuple[int | None, int | None]:
    query_match = re.search(r"(?:^|_)sparse_query_(?:max_active_dims|max_dims)_(\d+)(?:_|$)", variant_name)
    document_match = re.search(
        r"(?:^|_)sparse_(?:document|docs)_(?:max_active_dims|max_dims)_(\d+)(?:_|$)",
        variant_name,
    )
    return (
        int(query_match.group(1)) if query_match is not None else None,
        int(document_match.group(1)) if document_match is not None else None,
    )


def _truncate_dim(row: LeaderboardRow) -> int | None:
    variant_name = row.embedding_variant_name or ""
    match = re.search(r"(?:^|_)truncate_dim_(\d+)(?:_|$)", variant_name)
    if match is not None:
        return int(match.group(1))
    return None


def _model_type_view(*, row: LeaderboardRow, full_model_name: str) -> dict[str, str | None]:
    model_type = _normalized_model_type(row=row, full_model_name=full_model_name)
    labels = {
        "dense": "Dense",
        "reranker": "Cross-encoder reranker",
        "sparse": "Sparse",
        "late-interaction": "Late interaction",
        "bm25": "BM25",
    }
    badge_labels = {
        "reranker": "reranker",
        "sparse": "sparse",
        "late-interaction": "late interaction",
    }
    return {
        "key": model_type,
        "label": labels.get(model_type, model_type),
        "badge_label": badge_labels.get(model_type),
    }


def _normalized_model_type(*, row: LeaderboardRow, full_model_name: str) -> str:
    return normalized_model_type(model_name=full_model_name, model_type=getattr(row, "model_type", None))


def _model_metadata(
    *,
    row: LeaderboardRow,
    full_model_name: str,
    original_embedding_dim: int | None,
    truncated_embedding_dim: int | None,
) -> dict[str, Any]:
    model_type_view = _model_type_view(row=row, full_model_name=full_model_name)
    openai_metadata = _OPENAI_EMBEDDING_MODELS.get(full_model_name)
    return {
        "model_name": full_model_name,
        "model_url": _model_url(full_model_name),
        "model_type": model_type_view["label"],
        "model_type_key": model_type_view["key"],
        "ranking_model_name": row.model_name,
        "source_model_name": row.source_model_name,
        "embedding_variant_name": row.embedding_variant_name,
        "embedding_dim": row.embedding_dim,
        "original_embedding_dim": original_embedding_dim,
        "truncated_embedding_dim": truncated_embedding_dim,
        "truncate_dims": list(row.truncate_dims),
        "quantization": row.quantization,
        "base_score_delta_percent": row.base_score_delta_percent,
        "active_parameters": None if openai_metadata is not None else row.active_parameters,
        "total_parameters": None if openai_metadata is not None else row.total_parameters,
        "max_seq_length": openai_metadata["max_seq_length"] if openai_metadata is not None else row.max_seq_length,
        "dtype": row.dtype,
        "attention": row.attn_implementation,
        "prompt": row.prompt_summary,
        "query_prompt": row.query_prompt,
        "document_prompt": row.document_prompt,
        "query_prompt_name": row.query_prompt_name,
        "document_prompt_name": row.document_prompt_name,
        "trust_remote_code": row.trust_remote_code,
        "late_interaction_query_length": row.late_interaction_query_length,
        "late_interaction_document_length": row.late_interaction_document_length,
        "late_interaction_query_prefix": row.late_interaction_query_prefix,
        "late_interaction_document_prefix": row.late_interaction_document_prefix,
        "late_interaction_query_expansion": row.late_interaction_query_expansion,
        "late_interaction_attend_to_expansion_tokens": row.late_interaction_attend_to_expansion_tokens,
        "language_support_category": row.language_support_category,
        "language_support_languages": list(row.language_support_languages),
        "language_support_label": _language_support_label(row),
        "links": row.links or None,
        "license": row.license or None,
    }


def render_model_name_cell(row: LeaderboardRow, model_view: ModelCellView, *, borda_score_bar_width: float | None = None) -> str:
    metadata_json = json.dumps(model_view.metadata, ensure_ascii=False, separators=(",", ":"))
    display_name = model_view.display_name
    name_attrs = f' aria-label="{escape(model_view.display_name, quote=True)}"'
    borda_bar_html = ""
    if borda_score_bar_width is not None:
        clamped_width = min(100.0, max(0.0, borda_score_bar_width))
        borda_bar_html = (
            f'<progress class="borda-score-bar" value="{clamped_width:.2f}" max="100"'
            ' aria-hidden="true"></progress>'
        )
    badges = []
    if model_view.model_type_badge_label is not None:
        badges.append(
            _render_badge(
                label=model_view.model_type_badge_label,
                classes="model-type-badge bg-zinc-100 text-zinc-700",
            )
        )
    if model_view.dimension_label is not None:
        badges.append(
            _render_badge(
                label=model_view.dimension_label,
                classes="dimension-badge bg-zinc-100 text-cyan-800",
                tooltip=model_view.dimension_tooltip,
            )
        )
    if model_view.variant_label and model_view.truncated_embedding_dim is not None:
        badges.append(
            _render_badge(
                label=model_view.variant_label,
                classes="dimension-badge truncate-dim-badge bg-zinc-100 text-cyan-800",
                tooltip=model_view.variant_tooltip,
            )
        )
    if row.quantization:
        badges.append(
            _render_badge(
                label=row.quantization,
                classes="quantization-badge bg-zinc-100 text-amber-800",
            )
        )
    if model_view.variant_label and model_view.truncated_embedding_dim is None:
        badges.append(
            _render_badge(
                label=model_view.variant_label,
                classes="variant-badge bg-zinc-100 text-cyan-800",
                tooltip=model_view.variant_tooltip,
            )
        )
    badge_html = (
        f"""<span class="model-variant-badges inline-flex min-w-0 flex-wrap gap-1 align-middle">{''.join(badges)}</span>"""
        if badges
        else ""
    )
    return f"""<td class="leaderboard-col-model sticky z-10 bg-inherit px-2 py-1">
      <div class="relative z-10 flex min-w-0 flex-wrap items-center gap-1">
        <button type="button" class="model-detail-trigger min-w-0 [overflow-wrap:anywhere] text-left text-[0.8125rem] leading-tight font-medium underline-offset-2 hover:underline"
                data-model-metadata="{escape(metadata_json)}"{name_attrs}>{escape(display_name)}</button>{badge_html}
      </div>{borda_bar_html}
    </td>"""


def _language_support_label(row: LeaderboardRow) -> str | None:
    category = row.language_support_category
    if category == "multilingual":
        return "Multilingual"
    if category == "english_only":
        return "English only"
    if category == "english_plus":
        return ", ".join(row.language_support_languages) if row.language_support_languages else "Multiple"
    return None


def _model_url(model_name: str) -> str | None:
    if model_name in _OPENAI_EMBEDDING_MODELS:
        return str(_OPENAI_EMBEDDING_MODELS[model_name]["url"])
    owner, separator, name = model_name.partition("/")
    if not owner or not separator or not name:
        return None
    return f"https://huggingface.co/{model_name}"


def _render_badge(*, label: str, classes: str, tooltip: str | None = None) -> str:
    escaped_tooltip = escape(tooltip, quote=True) if tooltip else ""
    tooltip_attrs = f' tabindex="0" data-tooltip="{escaped_tooltip}" aria-label="{escaped_tooltip}"' if tooltip else ""
    tooltip_class = "tooltip-trigger tooltip-delay cursor-pointer " if tooltip else ""
    return (
        f"""<span class="{tooltip_class}inline-flex items-center border px-1 py-0 text-[0.6875rem] leading-tight font-medium {classes}"{tooltip_attrs}>"""
        f"{escape(label)}</span>"
    )


def render_model_detail_modal() -> str:
    return """
<dialog id="model-detail-modal" class="hakari-modal">
  <form method="dialog">
    <div class="hakari-modal-header">
      <h3 class="hakari-modal-title"><span>Model Details</span></h3>
      <button type="submit" class="hakari-modal-close">Close</button>
    </div>
  </form>
  <div class="hakari-modal-body">
    <a id="model-detail-title" class="hakari-modal-link break-all font-mono text-sm font-semibold" target="_blank" rel="noopener noreferrer"></a>
    <dl id="model-detail-fields" class="mt-3 grid grid-cols-[10rem_1fr] gap-x-3 gap-y-2 text-sm"></dl>
  </div>
</dialog>
"""
