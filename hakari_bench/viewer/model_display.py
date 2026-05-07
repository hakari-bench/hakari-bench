from __future__ import annotations

from collections import defaultdict
from typing import Any

from pydantic import BaseModel, ConfigDict, Field

from hakari_bench.viewer.leaderboard import LeaderboardRow


class ModelCellView(BaseModel):
    model_config = ConfigDict(frozen=True)

    display_name: str
    full_model_name: str
    ranking_model_name: str
    variant_label: str | None = None
    metadata: dict[str, Any] = Field(default_factory=dict)


def model_cell_views(rows: list[LeaderboardRow]) -> dict[str, ModelCellView]:
    base_names = {row.model_name: _base_model_name(row) for row in rows}
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
            variant_label=_variant_label(row),
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


def _variant_label(row: LeaderboardRow) -> str | None:
    variant_name = row.embedding_variant_name
    if variant_name is None or variant_name == "base":
        return None
    if row.quantization is not None and variant_name.casefold() == row.quantization.casefold():
        return None
    return variant_name


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
