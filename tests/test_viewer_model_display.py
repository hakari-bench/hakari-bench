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
    assert ">768 dims</span>" in html
    assert ">binary</span>" in html
    assert ">binary_rescore</span>" in html


def test_render_model_detail_modal_supports_backdrop_close_and_focus_restore() -> None:
    html = render_model_detail_modal()

    assert 'id="model-detail-modal"' in html
    assert "event.target === modal" in html
    assert "modal.close()" in html
    assert "window.__hakariRestoreModelFilterFocus" in html
    assert '["HF trust", "trust_remote_code"]' in html
    assert '["Base delta", "base_score_delta_percent"]' in html
