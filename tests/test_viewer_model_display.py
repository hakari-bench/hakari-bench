from __future__ import annotations

from hakari_bench.viewer.leaderboard import LeaderboardRow
from hakari_bench.viewer.model_display import (
    model_cell_views,
    render_model_detail_modal,
    render_model_name_cell,
)


def test_render_model_name_cell_uses_metadata_json_and_compact_badges() -> None:
    row = LeaderboardRow(
        borda_rank=1,
        mean_rank=1,
        model_name="jinaai/jina-embeddings-v5-text-nano (768 dims, binary)",
        borda_score=100,
        mean_score=90,
        task_count=1,
        embedding_variant_name="binary_rescore",
        embedding_dim=768,
        quantization="binary",
        trust_remote_code=True,
    )
    model_view = model_cell_views([row])[row.model_name]

    html = render_model_name_cell(row, model_view)

    assert "jina-embeddings-v5-text-nano" in html
    assert "remote code" not in html
    assert "data-model-metadata=" in html
    assert "&quot;trust_remote_code&quot;:true" in html
    assert ">768d</span>" in html
    assert ">binary</span>" in html
    assert ">binary_rescore</span>" in html


def test_render_model_name_cell_uses_compact_truncate_dimension_badge_with_tooltip() -> None:
    base = LeaderboardRow(
        borda_rank=1,
        mean_rank=1,
        model_name="model/a (1024 dims)",
        borda_score=100,
        mean_score=90,
        task_count=1,
        embedding_dim=1024,
        source_model_name="model/a",
    )
    truncated = LeaderboardRow(
        borda_rank=2,
        mean_rank=2,
        model_name="model/a (768 dims)",
        borda_score=90,
        mean_score=80,
        task_count=1,
        embedding_variant_name="truncate_dim_768",
        embedding_dim=768,
        source_model_name="model/a",
    )
    model_view = model_cell_views([base, truncated])[truncated.model_name]

    html = render_model_name_cell(truncated, model_view)

    assert "border-violet-200 bg-violet-50" in html
    assert ">768d &lt;- 1024</span>" in html
    assert ">768d</span>" not in html
    assert ">truncate_dim_768</span>" not in html
    assert 'class="tooltip-trigger tooltip-delay inline-flex' in html
    assert (
        'data-tooltip="Original embedding dimension is 1024. '
        'This result was evaluated after truncating embeddings to 768 dimensions."'
    ) in html


def test_render_model_name_cell_falls_back_for_truncate_badge_without_original_dimension() -> None:
    row = LeaderboardRow(
        borda_rank=1,
        mean_rank=1,
        model_name="model/a (256 dims)",
        borda_score=100,
        mean_score=90,
        task_count=1,
        embedding_variant_name="truncate_dim_256",
        embedding_dim=256,
    )
    model_view = model_cell_views([row])[row.model_name]

    html = render_model_name_cell(row, model_view)

    assert ">256d</span>" in html
    assert ">truncate_dim_256</span>" not in html
    assert 'data-tooltip="This result was evaluated after truncating embeddings to 256 dimensions."' in html


def test_render_model_detail_modal_supports_backdrop_close_and_focus_restore() -> None:
    html = render_model_detail_modal()

    assert 'id="model-detail-modal"' in html
    assert "event.target === modal" in html
    assert "modal.close()" in html
    assert "window.__hakariRestoreModelFilterFocus" in html
    assert '["HF trust", "trust_remote_code"]' in html
    assert '["Base delta", "base_score_delta_percent"]' in html
