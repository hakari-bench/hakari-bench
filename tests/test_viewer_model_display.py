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
    assert 'sticky left-0 z-10 w-[36rem] min-w-72 max-w-[36rem]' in html
    assert 'class="flex min-w-0 flex-wrap items-center gap-1"' in html
    assert "model-detail-trigger min-w-0 [overflow-wrap:anywhere] text-left text-[0.8125rem] leading-tight font-medium underline-offset-2" in html
    assert " min-w-0 truncate " not in html
    assert "whitespace-nowrap" not in html
    assert "&quot;trust_remote_code&quot;:true" in html
    assert ">768d</span>" in html
    assert ">binary</span>" in html
    assert ">binary_rescore</span>" in html


def test_render_model_name_cell_allows_long_visible_model_name_to_wrap() -> None:
    long_name = "Model NAME " + ("A" * 45)
    row = LeaderboardRow(
        borda_rank=1,
        mean_rank=1,
        model_name=long_name,
        borda_score=100,
        mean_score=90,
        task_count=1,
    )
    model_view = model_cell_views([row])[row.model_name]

    html = render_model_name_cell(row, model_view)

    assert f">{long_name}</button>" in html
    assert f'title="{long_name}"' in html
    assert "aria-label=" not in html
    assert " min-w-0 truncate " not in html
    assert "[overflow-wrap:anywhere]" in html
    assert model_view.display_name == long_name
    assert model_view.metadata["model_name"] == long_name


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

    assert "dimension-badge truncate-dim-badge border-cyan-200 bg-cyan-50 text-cyan-800" in html
    assert ">768d &lt;- 1024</span>" in html
    assert ">768d</span>" not in html
    assert ">truncate_dim_768</span>" not in html
    assert 'class="tooltip-trigger tooltip-delay cursor-pointer inline-flex' in html
    assert (
        'data-tooltip="Original embedding dimension is 1024. '
        'This result was evaluated after truncating embeddings to 768 dimensions."'
    ) in html


def test_render_model_name_cell_shows_non_dense_model_type_before_dimensions() -> None:
    row = LeaderboardRow(
        borda_rank=1,
        mean_rank=1,
        model_name="opensearch-project/opensearch-neural-sparse-encoding-v2-distill (1024 dims)",
        borda_score=100,
        mean_score=90,
        task_count=1,
        model_type="sparse",
        embedding_dim=1024,
    )
    model_view = model_cell_views([row])[row.model_name]

    html = render_model_name_cell(row, model_view)

    assert model_view.metadata["model_type"] == "Sparse"
    assert ">sparse</span>" in html
    assert html.index(">sparse</span>") < html.index(">1024d</span>")


def test_render_model_name_cell_orders_dimension_badges_before_quantization() -> None:
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
    truncated_quantized = LeaderboardRow(
        borda_rank=2,
        mean_rank=2,
        model_name="model/a (768 dims, int8, truncate_dim_768)",
        borda_score=90,
        mean_score=80,
        task_count=1,
        embedding_variant_name="truncate_dim_768",
        embedding_dim=768,
        quantization="int8",
        source_model_name="model/a",
    )
    model_view = model_cell_views([base, truncated_quantized])[truncated_quantized.model_name]

    html = render_model_name_cell(truncated_quantized, model_view)

    assert html.index(">768d &lt;- 1024</span>") < html.index(">int8</span>")


def test_render_model_name_cell_infers_reranker_type_without_dimension_badge() -> None:
    row = LeaderboardRow(
        borda_rank=1,
        mean_rank=1,
        model_name="cross-encoder/mmarco-mMiniLMv2-L12-H384-v1",
        borda_score=100,
        mean_score=90,
        task_count=1,
    )
    model_view = model_cell_views([row])[row.model_name]

    html = render_model_name_cell(row, model_view)

    assert model_view.metadata["model_type"] == "Cross-encoder reranker"
    assert ">reranker</span>" in html


def test_render_model_name_cell_hides_table_type_badge_for_dense_and_bm25() -> None:
    dense = LeaderboardRow(
        borda_rank=1,
        mean_rank=1,
        model_name="BAAI/bge-m3 (1024 dims)",
        borda_score=100,
        mean_score=90,
        task_count=1,
        model_type="dense",
        embedding_dim=1024,
    )
    bm25 = LeaderboardRow(
        borda_rank=2,
        mean_rank=2,
        model_name="bm25",
        borda_score=90,
        mean_score=80,
        task_count=1,
    )
    model_views = model_cell_views([dense, bm25])

    dense_html = render_model_name_cell(dense, model_views[dense.model_name])
    bm25_html = render_model_name_cell(bm25, model_views[bm25.model_name])

    assert model_views[dense.model_name].metadata["model_type"] == "Dense"
    assert model_views[bm25.model_name].metadata["model_type"] == "BM25"
    assert ">dense</span>" not in dense_html
    assert ">bm25</span>" not in bm25_html


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
    assert 'id="model-detail-title"' in html
    assert 'id="model-detail-fields"' in html
    assert "<script>" not in html
