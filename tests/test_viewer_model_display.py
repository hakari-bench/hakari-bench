from __future__ import annotations

from pathlib import Path

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
    assert 'leaderboard-col-model sticky z-10' in html
    assert 'class="relative z-10 flex min-w-0 flex-wrap items-center gap-1"' in html
    assert "model-detail-trigger min-w-0 [overflow-wrap:anywhere] text-left text-[0.8125rem] leading-tight font-medium underline-offset-2" in html
    assert 'class="model-variant-badges inline-flex min-w-0 flex-wrap gap-1 align-middle"' in html
    assert html.index("jina-embeddings-v5-text-nano</button>") < html.index(">768d</span>")
    assert "border px-1 py-0 text-[0.6875rem] leading-tight" in html
    assert " min-w-0 truncate " not in html
    assert "whitespace-nowrap" not in html
    assert "&quot;trust_remote_code&quot;:true" in html
    assert ">768d</span>" in html
    assert ">binary</span>" in html
    assert ">binary_rescore</span>" in html
    assert "quantization-badge bg-zinc-100 text-amber-800" in html
    assert "variant-badge bg-zinc-100 text-cyan-800" in html
    assert "variant-badge bg-zinc-100 text-amber-800" not in html


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
    assert f'aria-label="{long_name}"' in html
    assert "title=" not in html
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

    assert "dimension-badge truncate-dim-badge bg-zinc-100 text-cyan-800" in html
    assert "dimension-badge truncate-dim-badge bg-zinc-100 text-amber-800" not in html
    assert ">768d &lt;- 1024</span>" in html
    assert ">768d</span>" not in html
    assert ">truncate_dim_768</span>" not in html
    assert 'class="tooltip-trigger tooltip-delay cursor-pointer inline-flex' in html
    assert (
        'data-tooltip="Original embedding dimension is 1024. '
        'This result was evaluated after truncating embeddings to 768 dimensions."'
    ) in html


def test_render_model_name_cell_shows_sparse_type_without_dimension_badge() -> None:
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
    assert "model-type-badge bg-zinc-100 text-zinc-700" in html
    assert ">sparse</span>" in html
    assert ">1024d</span>" not in html


def test_render_model_name_cell_shortens_sparse_active_dim_variant_with_tooltip() -> None:
    row = LeaderboardRow(
        borda_rank=1,
        mean_rank=1,
        model_name=(
            "opensearch-project/opensearch-neural-sparse-encoding-multilingual-v1 "
            "(sparse_query_max_active_dims_32_sparse_document_max_active_dims_256)"
        ),
        borda_score=100,
        mean_score=90,
        task_count=1,
        model_type="sparse",
        embedding_variant_name="sparse_query_max_active_dims_32_sparse_document_max_active_dims_256",
    )
    model_view = model_cell_views([row])[row.model_name]

    html = render_model_name_cell(row, model_view)

    assert model_view.variant_label == "q32d d256d"
    assert "variant-badge bg-zinc-100 text-cyan-800" in html
    assert "variant-badge bg-zinc-100 text-amber-800" not in html
    assert ">q32d d256d</span>" in html
    assert "Sparse active dimension cap." in html
    assert "Query max active dims: 32." in html
    assert "Document max active dims: 256." in html
    assert "Full variant: sparse_query_max_active_dims_32_sparse_document_max_active_dims_256" in html


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


def test_render_model_name_cell_places_variant_badges_inline_after_model_name() -> None:
    row = LeaderboardRow(
        borda_rank=1,
        mean_rank=1,
        model_name="org/model-a (768 dims, int8, truncate_dim_768)",
        borda_score=100,
        mean_score=90,
        task_count=1,
        model_type="reranker",
        embedding_variant_name="truncate_dim_768",
        embedding_dim=768,
        quantization="int8",
    )
    model_view = model_cell_views([row])[row.model_name]

    html = render_model_name_cell(row, model_view)

    assert "<button" in html
    assert 'class="model-variant-badges inline-flex min-w-0 flex-wrap gap-1 align-middle"' in html
    assert 'class="relative z-10 flex min-w-0 flex-wrap items-center gap-1"' in html
    assert html.index("</button>") < html.index('<span class="model-variant-badges inline-flex min-w-0 flex-wrap gap-1 align-middle">')
    assert html.index(">reranker</span>") > html.index("</button>")
    assert html.index(">768d</span>") > html.index("</button>")
    assert html.index(">int8</span>") > html.index("</button>")


def test_render_model_name_cell_uses_explicit_reranker_type_without_dimension_badge() -> None:
    row = LeaderboardRow(
        borda_rank=1,
        mean_rank=1,
        model_name="cross-encoder/mmarco-mMiniLMv2-L12-H384-v1",
        borda_score=100,
        mean_score=90,
        task_count=1,
        model_type="reranker",
    )
    model_view = model_cell_views([row])[row.model_name]

    html = render_model_name_cell(row, model_view)

    assert model_view.metadata["model_type"] == "Cross-encoder reranker"
    assert ">reranker</span>" in html


def test_render_model_name_cell_does_not_infer_reranker_type_from_model_name() -> None:
    row = LeaderboardRow(
        borda_rank=1,
        mean_rank=1,
        model_name="mixedbread-ai/mxbai-rerank-base-v2",
        borda_score=100,
        mean_score=90,
        task_count=1,
        max_seq_length=32768,
    )
    model_view = model_cell_views([row])[row.model_name]

    html = render_model_name_cell(row, model_view)

    assert model_view.metadata["model_type"] == "Dense"
    assert model_view.metadata["model_type_key"] == "dense"
    assert ">reranker</span>" not in html


def test_model_cell_views_use_openai_metadata_for_openai_embedding_models() -> None:
    row = LeaderboardRow(
        borda_rank=1,
        mean_rank=1,
        model_name="openai/text-embedding-3-small",
        model_type="dense",
        borda_score=100,
        mean_score=90,
        task_count=1,
        active_parameters=123,
        total_parameters=456,
        max_seq_length=8100,
    )

    model_view = model_cell_views([row])[row.model_name]

    assert model_view.metadata["model_url"] == "https://developers.openai.com/api/docs/models/text-embedding-3-small"
    assert model_view.metadata["model_type"] == "Dense"
    assert model_view.metadata["active_parameters"] is None
    assert model_view.metadata["total_parameters"] is None
    assert model_view.metadata["max_seq_length"] == 8192


def test_model_cell_views_include_late_interaction_metadata_for_details_modal() -> None:
    row = LeaderboardRow(
        borda_rank=1,
        mean_rank=1,
        model_name="mixedbread-ai/mxbai-edge-colbert-v0-17m",
        model_type="late-interaction",
        borda_score=100,
        mean_score=90,
        task_count=1,
        late_interaction_query_length=48,
        late_interaction_document_length=512,
        late_interaction_query_expansion=False,
    )

    model_view = model_cell_views([row])[row.model_name]
    html = render_model_name_cell(row, model_view)

    assert model_view.metadata["late_interaction_query_length"] == 48
    assert model_view.metadata["late_interaction_document_length"] == 512
    assert model_view.metadata["late_interaction_query_expansion"] is False
    assert "&quot;late_interaction_query_length&quot;:48" in html
    assert "&quot;late_interaction_document_length&quot;:512" in html
    assert "&quot;late_interaction_query_expansion&quot;:false" in html


def test_model_cell_views_include_model_card_detail_metadata() -> None:
    row = LeaderboardRow(
        borda_rank=1,
        mean_rank=1,
        model_name="jinaai/jina-embeddings-v3",
        model_type="dense",
        borda_score=100,
        mean_score=90,
        task_count=1,
        license={"id": "cc-by-nc-4.0", "label": "CC BY-NC 4.0"},
        links={"github": "https://github.com/jina-ai/embeddings", "huggingface": "https://huggingface.co/jinaai/jina-embeddings-v3"},
        truncate_dims=(32, 64, 128),
        query_prompt_name="retrieval.query",
        document_prompt_name="retrieval.passage",
    )

    model_view = model_cell_views([row])[row.model_name]
    html = render_model_name_cell(row, model_view)

    assert model_view.metadata["license"] == {"id": "cc-by-nc-4.0", "label": "CC BY-NC 4.0"}
    assert model_view.metadata["links"] == {
        "github": "https://github.com/jina-ai/embeddings",
        "huggingface": "https://huggingface.co/jinaai/jina-embeddings-v3",
    }
    assert model_view.metadata["truncate_dims"] == [32, 64, 128]
    assert model_view.metadata["query_prompt_name"] == "retrieval.query"
    assert model_view.metadata["document_prompt_name"] == "retrieval.passage"
    assert "&quot;truncate_dims&quot;:[32,64,128]" in html
    assert "&quot;query_prompt_name&quot;:&quot;retrieval.query&quot;" in html


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


def test_model_cell_views_hide_sparse_dimension_badges() -> None:
    row = LeaderboardRow(
        borda_rank=1,
        mean_rank=1,
        model_name="org/sparse-encoder",
        model_type="sparse",
        borda_score=100,
        mean_score=90,
        task_count=1,
        embedding_dim=30000,
    )

    model_view = model_cell_views([row])[row.model_name]
    html = render_model_name_cell(row, model_view)

    assert model_view.model_type_badge_label == "sparse"
    assert model_view.dimension_label is None
    assert ">30000d</span>" not in html


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


def test_model_detail_script_orders_fields_and_labels_github_repo() -> None:
    script = Path("hakari_bench/viewer/assets/viewer.js").read_text(encoding="utf-8")

    assert script.index('["Language", "language_support_label"]') < script.index('["Active params", "active_parameters"]')
    assert script.index('["Max len", "max_seq_length"]') < script.index("appendModelDetailLicense")
    click_handler = script.split("list.replaceChildren();", 1)[1]
    assert click_handler.index("appendModelDetailLicense") < click_handler.index("appendModelDetailLinks")
    assert click_handler.index("appendModelDetailLinks") < click_handler.index("modelDetailFieldsAfterLinks")
    assert '["Query Prompt", "query_prompt"]' in script
    assert '["Doc Prompt", "document_prompt"]' in script
    assert 'replace(/^https?:\\/\\/github\\.com\\//, "")' in script
    assert '"Repository"' not in script
