from __future__ import annotations

from pathlib import Path
import re

from fastapi.testclient import TestClient

from hakari_bench.viewer.app import create_app
from hakari_bench.viewer.docs import BenchmarkDocs, render_markdown_to_html
from hakari_bench.viewer.store import DuckDbLocation, LocalDuckDbStore

from tests.test_viewer import _write_task_results


def test_benchmark_docs_resolves_group_and_task_overviews(tmp_path: Path) -> None:
    docs_dir = tmp_path / "task_docs" / "docs"
    group_dir = docs_dir / "NanoMIRACL"
    group_dir.mkdir(parents=True)
    (group_dir / "index.md").write_text(
        "# NanoMIRACL\n\n## Overview\n\nGroup overview text.\n\n## Details\n\nDetails text.\n",
        encoding="utf-8",
    )
    (group_dir / "ja.md").write_text(
        "# NanoMIRACL / ja\n\n## Overview\n\nJapanese task overview.\n\n## Details\n\nMore detail.\n",
        encoding="utf-8",
    )

    docs = BenchmarkDocs(docs_dir)

    group_doc = docs.group_doc("NanoMIRACL")
    task_doc = docs.task_doc(view_name="NanoMIRACL", metric_column="ja")

    assert group_doc is not None
    assert group_doc.title == "NanoMIRACL"
    assert group_doc.description == "Group overview text."
    assert group_doc.url == "/docs/benchmark-tasks/NanoMIRACL"
    assert task_doc is not None
    assert task_doc.title == "NanoMIRACL / ja"
    assert task_doc.description == "Japanese task overview."
    assert task_doc.url == "/docs/benchmark-tasks/NanoMIRACL/ja"


def test_benchmark_docs_renders_task_metadata_from_task_docs_json(tmp_path: Path) -> None:
    docs_dir = tmp_path / "task_docs" / "docs"
    metadata_dir = tmp_path / "task_docs" / "metadata"
    group_dir = docs_dir / "NanoMIRACL"
    metadata_group_dir = metadata_dir / "NanoMIRACL"
    group_dir.mkdir(parents=True)
    metadata_group_dir.mkdir(parents=True)
    (group_dir / "ja.md").write_text(
        "# NanoMIRACL / ja\n\n## Overview\n\nJapanese task overview.\n",
        encoding="utf-8",
    )
    (metadata_group_dir / "ja.json").write_text(
        """
{
  "task_metadata": {
    "schema_version": 1,
    "document_status": "first_pass",
    "nano_set": "NanoMIRACL",
    "backing_dataset": "NanoMIRACL",
    "dataset_id": "hakari-bench/NanoMIRACL",
    "task_name": "ja",
    "split_name": "ja",
    "language": "ja",
    "category": "natural_language",
    "document_path": "task_docs/docs/NanoMIRACL/ja.md",
    "source_research": {"primary_source_type": "task_paper", "paper_pdf_or_html_checked": true},
    "counts": {"queries": 200, "documents": 10000, "positive_qrels": 373},
    "positives_per_query": {
      "average": 1.865,
      "min": 1,
      "median": 1.0,
      "max": 8,
      "multi_positive_queries": 78,
      "multi_positive_query_percent": 39.0
    },
    "text_stats_chars": {"query_mean": 17.5, "document_mean": 173.3871},
    "bm25": {"ndcg_at_10": 0.6600634301, "hit_at_10": 0.935, "source": "dataset_candidate_subset"},
    "candidate_subsets": {
      "bm25": {
        "config": "bm25",
        "label": "BM25",
        "source": "dataset_candidate_subset",
        "top_k": 500,
        "ndcg_at_10": 0.6600634301,
        "hit_at_10": 0.935,
        "recall_at_100": 0.9705093834,
        "candidate_count_min": 500,
        "candidate_count_max": 500,
        "candidate_count_mean": 500.0,
        "query_count": 200,
        "query_coverage": 1.0,
        "relevant_coverage_at_100": 0.9705093834
      },
      "dense": {
        "config": "harrier_oss_v1_270m",
        "label": "Dense",
        "source": "dataset_candidate_subset",
        "top_k": 500,
        "ndcg_at_10": 0.7744598647,
        "hit_at_10": 0.915,
        "recall_at_100": 0.9302949062,
        "candidate_count_min": 500,
        "candidate_count_max": 500,
        "candidate_count_mean": 500.0,
        "query_count": 200,
        "query_coverage": 1.0,
        "relevant_coverage_at_100": 0.9302949062
      },
      "reranking_hybrid": {
        "config": "reranking_hybrid",
        "label": "Reranking hybrid",
        "source": "dataset_candidate_subset",
        "top_k": 100,
        "ndcg_at_10": 0.7223080894,
        "hit_at_10": 0.97,
        "recall_at_100": 1.0,
        "candidate_count_min": 100,
        "candidate_count_max": 100,
        "candidate_count_mean": 100.0,
        "query_count": 200,
        "query_coverage": 1.0,
        "relevant_coverage_at_100": 1.0
      }
    },
    "links": {
      "nano_dataset": "https://huggingface.co/datasets/hakari-bench/NanoMIRACL",
      "source_urls": [{"label": "MIRACL repository", "url": "https://github.com/project-miracl/miracl"}]
    },
    "references": [
      {
        "title": "Making a MIRACL: Multilingual Information Retrieval Across a Continuum of Languages",
        "url": "https://arxiv.org/abs/2210.09984",
        "year": 2022,
        "is_paper": true,
        "doi": "10.48550/arXiv.2210.09984"
      }
    ]
  }
}
""".strip(),
        encoding="utf-8",
    )

    docs = BenchmarkDocs(docs_dir, metadata_dir=metadata_dir)

    doc = docs.task_doc(view_name="NanoMIRACL", metric_column="ja")

    assert doc is not None
    assert "## Dataset Information" in doc.markdown
    assert "| Queries | 200 |" in doc.markdown
    assert "| Positive qrels | 373 |" in doc.markdown
    assert "| BM25 | `bm25` | 0.6601 | 0.9350 | 0.9705 | top-500 |" in doc.markdown
    assert "| Dense | `harrier_oss_v1_270m` | 0.7745 | 0.9150 | 0.9303 | top-500 |" in doc.markdown
    assert "- Nano dataset: [hakari-bench/NanoMIRACL](https://huggingface.co/datasets/hakari-bench/NanoMIRACL)" in doc.markdown
    assert "| Making a MIRACL: Multilingual Information Retrieval Across a Continuum of Languages | 2022 | paper | https://arxiv.org/abs/2210.09984 |" in doc.markdown


def test_benchmark_docs_renders_group_metadata_summary_from_task_docs_json(tmp_path: Path) -> None:
    docs_dir = tmp_path / "task_docs" / "docs"
    metadata_dir = tmp_path / "task_docs" / "metadata"
    group_dir = docs_dir / "NanoTiny"
    metadata_group_dir = metadata_dir / "NanoTiny"
    group_dir.mkdir(parents=True)
    metadata_group_dir.mkdir(parents=True)
    (group_dir / "index.md").write_text("# NanoTiny\n\n## Overview\n\nTiny overview.\n", encoding="utf-8")
    for name, language, queries, docs_count, positives, ndcg in [
        ("alpha", "en", 10, 100, 12, 0.25),
        ("beta", "ja", 20, 200, 40, 0.75),
    ]:
        (group_dir / f"{name}.md").write_text(f"# NanoTiny / {name}\n\n## Overview\n\n{name} overview.\n", encoding="utf-8")
        (metadata_group_dir / f"{name}.json").write_text(
            f"""
{{
  "task_metadata": {{
    "schema_version": 1,
    "document_status": "first_pass",
    "nano_set": "NanoTiny",
    "backing_dataset": "NanoTiny",
    "dataset_id": "hakari-bench/NanoTiny",
    "task_name": "{name}",
    "split_name": "{name}",
    "language": "{language}",
    "category": "natural_language",
    "document_path": "task_docs/docs/NanoTiny/{name}.md",
    "source_research": {{"primary_source_type": "dataset_card", "paper_pdf_or_html_checked": false}},
    "counts": {{"queries": {queries}, "documents": {docs_count}, "positive_qrels": {positives}}},
    "positives_per_query": {{"average": 1.0, "min": 1, "median": 1.0, "max": 1, "multi_positive_queries": 0}},
    "text_stats_chars": {{"query_mean": 12.5, "document_mean": 234.5}},
    "bm25": {{"ndcg_at_10": {ndcg}, "hit_at_10": 0.5, "source": "dataset_candidate_subset"}},
    "candidate_subsets": {{
      "bm25": {{
        "config": "bm25",
        "label": "BM25",
        "source": "dataset_candidate_subset",
        "top_k": 500,
        "ndcg_at_10": {ndcg},
        "hit_at_10": 0.5,
        "recall_at_100": 0.6,
        "candidate_count_min": 500,
        "candidate_count_max": 500,
        "candidate_count_mean": 500.0,
        "query_count": {queries},
        "query_coverage": 1.0,
        "relevant_coverage_at_100": 0.6
      }}
    }}
  }}
}}
""".strip(),
            encoding="utf-8",
        )

    docs = BenchmarkDocs(docs_dir, metadata_dir=metadata_dir)

    doc = docs.group_doc("NanoTiny")

    assert doc is not None
    assert "## Metadata Summary" in doc.markdown
    assert "| Task pages | 2 |" in doc.markdown
    assert "| Queries | 30 |" in doc.markdown
    assert "| Languages | en, ja |" in doc.markdown
    assert "| [alpha](alpha.md) | NanoTiny | en | natural_language | 10 | 100 | 12 | 0.2500 |  |  | BM25 |" in doc.markdown
    assert "| [beta](beta.md) | NanoTiny | ja | natural_language | 20 | 200 | 40 | 0.7500 |  |  | BM25 |" in doc.markdown


def test_benchmark_docs_lists_group_docs_with_descriptions(tmp_path: Path) -> None:
    docs_dir = tmp_path / "task_docs" / "docs"
    miracl_dir = docs_dir / "NanoMIRACL"
    coir_dir = docs_dir / "NanoCoIR"
    empty_dir = docs_dir / "NoIndex"
    miracl_dir.mkdir(parents=True)
    coir_dir.mkdir()
    empty_dir.mkdir()
    (miracl_dir / "index.md").write_text("# NanoMIRACL\n\n## Overview\n\nMIRACL overview.\n", encoding="utf-8")
    (coir_dir / "index.md").write_text("# NanoCoIR\n\n## Overview\n\nCoIR overview.\n", encoding="utf-8")

    docs = BenchmarkDocs(docs_dir)

    group_docs = docs.group_docs()

    assert [doc.title for doc in group_docs] == ["NanoCoIR", "NanoMIRACL"]
    assert [doc.url for doc in group_docs] == ["/docs/benchmark-tasks/NanoCoIR", "/docs/benchmark-tasks/NanoMIRACL"]
    assert [doc.description for doc in group_docs] == ["CoIR overview.", "MIRACL overview."]


def test_benchmark_docs_resolves_mnanobeir_task_key_documents(tmp_path: Path) -> None:
    docs_dir = tmp_path / "task_docs" / "docs"
    group_dir = docs_dir / "MNanoBEIR"
    group_dir.mkdir(parents=True)
    (group_dir / "NanoBEIR-ja__NanoMSMARCO.md").write_text(
        "# MNanoBEIR / NanoBEIR-ja / NanoMSMARCO\n\n## Overview\n\nMS MARCO overview.\n",
        encoding="utf-8",
    )
    docs = BenchmarkDocs(docs_dir)

    doc = docs.task_doc(
        view_name="MNanoBEIR",
        metric_column="MNanoBEIR::hakari-bench/NanoBEIR-ja::NanoMSMARCO",
    )

    assert doc is not None
    assert doc.url == "/docs/benchmark-tasks/MNanoBEIR/NanoBEIR-ja__NanoMSMARCO"
    assert doc.description == "MS MARCO overview."


def test_benchmark_docs_resolves_nanobeir_short_task_aliases(tmp_path: Path) -> None:
    docs_dir = tmp_path / "task_docs" / "docs"
    group_dir = docs_dir / "MNanoBEIR"
    group_dir.mkdir(parents=True)
    (group_dir / "NanoBEIR-ja__NanoArguAna.md").write_text(
        "# MNanoBEIR / NanoBEIR-ja / NanoArguAna\n\n## Overview\n\nArguAna overview.\n",
        encoding="utf-8",
    )
    docs = BenchmarkDocs(docs_dir)

    doc = docs.task_doc(
        view_name="MNanoBEIR",
        metric_column="MNanoBEIR::hakari-bench/NanoBEIR-ja::arguana",
    )

    assert doc is not None
    assert doc.title == "MNanoBEIR / NanoBEIR-ja / NanoArguAna"
    assert doc.url == "/docs/benchmark-tasks/MNanoBEIR/NanoBEIR-ja__NanoArguAna"
    assert doc.description == "ArguAna overview."


def test_markdown_renderer_escapes_html_and_renders_basic_markdown() -> None:
    html = render_markdown_to_html(
        "# Title\n\n## Overview\n\nA **bold phrase**, [safe link](https://example.com), and <script>x</script>.\n\n- one\n- two\n"
    )

    assert "<h1>Title</h1>" in html
    assert "<strong>bold phrase</strong>" in html
    assert "**bold phrase**" not in html
    assert '<a href="https://example.com" target="_blank" rel="noopener noreferrer">safe link</a>' in html
    assert "&lt;script&gt;x&lt;/script&gt;" in html
    assert "<ul>" in html
    assert "<li>one</li>" in html


def test_markdown_renderer_links_relative_task_docs_from_group_page() -> None:
    html = render_markdown_to_html(
        "| Task | Retrieval shape |\n"
        "| --- | --- |\n"
        "| [NanoApps](NanoApps.md) | problem statement to Python solution |\n"
        "| [unsafe](../outside.md) | must not escape the benchmark docs route |\n",
        base_url="/docs/benchmark-tasks/NanoCoIR",
    )

    assert '<a href="/docs/benchmark-tasks/NanoCoIR/NanoApps">NanoApps</a>' in html
    assert "../outside.md" not in html
    assert "<a href" in html
    assert ">unsafe</a>" not in html


def test_markdown_renderer_collapses_machine_readable_metadata_by_default() -> None:
    html = render_markdown_to_html(
        "# NanoCoIR\n\n"
        "## Overview\n\n"
        "Visible overview.\n\n"
        "## Machine-Readable Metadata\n\n"
        "```yaml\n"
        "nano_set: NanoCoIR\n"
        "```\n\n"
        "## References\n\n"
        "Visible references.\n",
        base_url="/docs/benchmark-tasks/NanoCoIR",
    )

    assert '<details class="machine-readable-metadata' in html
    assert "<summary" in html
    assert "Machine-Readable Metadata" in html
    assert "nano_set: NanoCoIR" in html
    assert "<details open" not in html
    assert html.index("</details>") < html.index("<h2>References</h2>")
    assert "<p>Visible references.</p>" in html


def test_real_benchmark_task_summary_links_resolve_to_existing_docs() -> None:
    docs_dir = Path("task_docs/docs")
    broken_links: list[str] = []
    link_count = 0
    for index_path in sorted(docs_dir.glob("*/index.md")):
        markdown = index_path.read_text(encoding="utf-8")
        for label, href in re.findall(r"\[([^\]]+)\]\(([^)]+\.md)\)", markdown):
            link_count += 1
            target_path = (index_path.parent / href).resolve()
            try:
                target_path.relative_to(index_path.parent.resolve())
            except ValueError:
                broken_links.append(f"{index_path}: {label} -> {href} escapes the benchmark docs directory")
                continue
            if not target_path.is_file():
                broken_links.append(f"{index_path}: {label} -> {href} is missing")

    assert link_count >= 300
    assert broken_links == []


def test_language_specific_group_overviews_start_with_language_axis_context() -> None:
    docs = BenchmarkDocs(Path("task_docs/docs"))

    expected_phrases = {
        "NanoMIRACL": "language specific",
        "NanoIndicQA": "language specific",
        "NanoMuPLeR": "language specific translated/parallel legal retrieval",
    }
    for view_name, phrase in expected_phrases.items():
        doc = docs.group_doc(view_name)
        assert doc is not None
        assert phrase in doc.description.lower()


def test_docs_endpoint_renders_markdown_page_and_rejects_missing_docs(tmp_path: Path) -> None:
    db_path = tmp_path / "results.duckdb"
    _write_task_results(db_path, [("model/a", "NanoMIRACL", "bench/a", "NanoMIRACL", "ja", "ja", "NanoMIRACL::ja", 0.90, 10, 12, 8192)])
    config_dir = tmp_path / "config"
    config_dir.mkdir()
    (config_dir / "benchmarks.yaml").write_text("benchmarks:\n  - name: NanoMIRACL\n", encoding="utf-8")
    (config_dir / "overall.yaml").write_text("name: Overall\nlabel: Overall\nbenchmarks:\n  - NanoMIRACL\n", encoding="utf-8")
    docs_dir = tmp_path / "task_docs" / "docs"
    group_dir = docs_dir / "NanoMIRACL"
    group_dir.mkdir(parents=True)
    (group_dir / "index.md").write_text("# NanoMIRACL\n\n## Overview\n\nGroup overview text.\n", encoding="utf-8")
    (group_dir / "ja.md").write_text("# NanoMIRACL / ja\n\n## Overview\n\nJapanese task overview.\n", encoding="utf-8")
    app = create_app(store=LocalDuckDbStore(DuckDbLocation(local_path=db_path)), config_dir=config_dir, docs_dir=docs_dir)
    client = TestClient(app)

    group_response = client.get("/docs/benchmark-tasks/NanoMIRACL")
    response = client.get("/docs/benchmark-tasks/NanoMIRACL/ja")
    missing_response = client.get("/docs/benchmark-tasks/NanoMIRACL/missing")

    assert group_response.status_code == 200
    assert "Group overview text." in group_response.text
    assert response.status_code == 200
    assert "NanoMIRACL / ja" in response.text
    assert "Japanese task overview." in response.text
    assert '<link rel="stylesheet" href="/assets/app.css' in response.text
    assert missing_response.status_code == 404


def test_docs_index_endpoint_lists_benchmark_docs(tmp_path: Path) -> None:
    db_path = tmp_path / "results.duckdb"
    _write_task_results(db_path, [("model/a", "NanoMIRACL", "bench/a", "NanoMIRACL", "ja", "ja", "NanoMIRACL::ja", 0.90, 10, 12, 8192)])
    config_dir = tmp_path / "config"
    config_dir.mkdir()
    (config_dir / "benchmarks.yaml").write_text("benchmarks:\n  - name: NanoMIRACL\n", encoding="utf-8")
    (config_dir / "overall.yaml").write_text("name: Overall\nlabel: Overall\nbenchmarks:\n  - NanoMIRACL\n", encoding="utf-8")
    docs_dir = tmp_path / "task_docs" / "docs"
    group_dir = docs_dir / "NanoMIRACL"
    group_dir.mkdir(parents=True)
    (group_dir / "index.md").write_text("# NanoMIRACL\n\n## Overview\n\nMIRACL overview.\n", encoding="utf-8")
    app = create_app(store=LocalDuckDbStore(DuckDbLocation(local_path=db_path)), config_dir=config_dir, docs_dir=docs_dir)

    response = TestClient(app).get("/docs/benchmark-tasks")

    assert response.status_code == 200
    assert "Benchmark documentation" in response.text
    assert '<a class="underline underline-offset-2" href="/">Top</a>' in response.text
    assert response.text.index(">Top</a>") < response.text.index(">Benchmark documentation</span>")
    assert 'class="font-semibold text-cyan-700 underline underline-offset-2" href="/docs/benchmark-tasks/NanoMIRACL"' in response.text
    assert "MIRACL overview." in response.text


def test_docs_root_redirects_to_benchmark_docs_until_docs_home_exists(tmp_path: Path) -> None:
    db_path = tmp_path / "results.duckdb"
    _write_task_results(db_path, [("model/a", "NanoMIRACL", "bench/a", "NanoMIRACL", "ja", "ja", "NanoMIRACL::ja", 0.90, 10, 12, 8192)])
    config_dir = tmp_path / "config"
    config_dir.mkdir()
    (config_dir / "benchmarks.yaml").write_text("benchmarks:\n  - name: NanoMIRACL\n", encoding="utf-8")
    (config_dir / "overall.yaml").write_text("name: Overall\nlabel: Overall\nbenchmarks:\n  - NanoMIRACL\n", encoding="utf-8")
    app = create_app(store=LocalDuckDbStore(DuckDbLocation(local_path=db_path)), config_dir=config_dir)

    response = TestClient(app).get("/docs/", follow_redirects=False)
    slashless_response = TestClient(app).get("/docs", follow_redirects=False)

    assert response.status_code == 307
    assert response.headers["location"] == "/docs/benchmark-tasks"
    assert slashless_response.status_code == 307
    assert slashless_response.headers["location"] == "/docs/benchmark-tasks"


def test_docs_pages_render_breadcrumb_navigation(tmp_path: Path) -> None:
    db_path = tmp_path / "results.duckdb"
    _write_task_results(
        db_path,
        [
            (
                "model/a",
                "NanoCodeRAG",
                "bench/a",
                "NanoCodeRAG",
                "NanoCodeRAGOnlineTutorials",
                "NanoCodeRAGOnlineTutorials",
                "NanoCodeRAGOnlineTutorials",
                0.90,
                10,
                12,
                8192,
            )
        ],
    )
    config_dir = tmp_path / "config"
    config_dir.mkdir()
    (config_dir / "benchmarks.yaml").write_text("benchmarks:\n  - name: NanoCodeRAG\n", encoding="utf-8")
    (config_dir / "overall.yaml").write_text("name: Overall\nlabel: Overall\nbenchmarks:\n  - NanoCodeRAG\n", encoding="utf-8")
    docs_dir = tmp_path / "task_docs" / "docs"
    group_dir = docs_dir / "NanoCodeRAG"
    group_dir.mkdir(parents=True)
    (group_dir / "index.md").write_text("# NanoCodeRAG\n\n## Overview\n\nGroup overview.\n", encoding="utf-8")
    (group_dir / "NanoCodeRAGOnlineTutorials.md").write_text(
        "# NanoCodeRAG / NanoCodeRAGOnlineTutorials\n\n## Overview\n\nTask overview.\n",
        encoding="utf-8",
    )
    app = create_app(store=LocalDuckDbStore(DuckDbLocation(local_path=db_path)), config_dir=config_dir, docs_dir=docs_dir)
    client = TestClient(app)

    group_response = client.get("/docs/benchmark-tasks/NanoCodeRAG")
    task_response = client.get("/docs/benchmark-tasks/NanoCodeRAG/NanoCodeRAGOnlineTutorials")

    assert group_response.status_code == 200
    assert 'class="doc-breadcrumb' in group_response.text
    assert '<a class="underline underline-offset-2" href="/">Top</a>' in group_response.text
    assert '<a class="underline underline-offset-2" href="/docs/benchmark-tasks">Benchmark documentation</a>' in group_response.text
    assert '<span aria-current="page">NanoCodeRAG</span>' in group_response.text
    assert group_response.text.index(">Top</a>") < group_response.text.index(">Benchmark documentation</a>")
    assert group_response.text.index(">Benchmark documentation</a>") < group_response.text.index(">NanoCodeRAG</span>")
    assert task_response.status_code == 200
    assert '<a class="underline underline-offset-2" href="/">Top</a>' in task_response.text
    assert '<a class="underline underline-offset-2" href="/docs/benchmark-tasks">Benchmark documentation</a>' in task_response.text
    assert '<a class="underline underline-offset-2" href="/docs/benchmark-tasks/NanoCodeRAG">NanoCodeRAG</a>' in task_response.text
    assert '<span aria-current="page">NanoCodeRAGOnlineTutorials</span>' in task_response.text
    assert task_response.text.index(">Top</a>") < task_response.text.index(">Benchmark documentation</a>")
    assert task_response.text.index(">Benchmark documentation</a>") < task_response.text.index(">NanoCodeRAG</a>")
    assert task_response.text.index(">NanoCodeRAG</a>") < task_response.text.index(">NanoCodeRAGOnlineTutorials</span>")


def test_docs_endpoint_renders_group_task_summary_links(tmp_path: Path) -> None:
    db_path = tmp_path / "results.duckdb"
    _write_task_results(db_path, [("model/a", "NanoCoIR", "bench/a", "NanoCoIR", "NanoApps", "NanoApps", "NanoApps", 0.90, 10, 12, 8192)])
    config_dir = tmp_path / "config"
    config_dir.mkdir()
    (config_dir / "benchmarks.yaml").write_text("benchmarks:\n  - name: NanoCoIR\n", encoding="utf-8")
    (config_dir / "overall.yaml").write_text("name: Overall\nlabel: Overall\nbenchmarks:\n  - NanoCoIR\n", encoding="utf-8")
    docs_dir = tmp_path / "task_docs" / "docs"
    group_dir = docs_dir / "NanoCoIR"
    group_dir.mkdir(parents=True)
    (group_dir / "index.md").write_text(
        "# NanoCoIR\n\n## Overview\n\nGroup overview.\n\n## Task Summary\n\n"
        "| Task | Retrieval shape |\n"
        "| --- | --- |\n"
        "| [NanoApps](NanoApps.md) | problem statement to Python solution |\n",
        encoding="utf-8",
    )
    (group_dir / "NanoApps.md").write_text("# NanoCoIR / NanoApps\n\n## Overview\n\nTask overview.\n", encoding="utf-8")
    app = create_app(store=LocalDuckDbStore(DuckDbLocation(local_path=db_path)), config_dir=config_dir, docs_dir=docs_dir)

    response = TestClient(app).get("/docs/benchmark-tasks/NanoCoIR")

    assert response.status_code == 200
    assert '<a href="/docs/benchmark-tasks/NanoCoIR/NanoApps">NanoApps</a>' in response.text


def test_leaderboard_renders_doc_summary_triggers_for_group_and_task_columns(tmp_path: Path) -> None:
    db_path = tmp_path / "results.duckdb"
    _write_task_results(
        db_path,
        [
            ("model/a", "NanoMIRACL", "bench/a", "NanoMIRACL", "ja", "ja", "ja", 0.90, 10, 12, 8192),
            ("model/b", "NanoMIRACL", "bench/a", "NanoMIRACL", "ja", "ja", "ja", 0.80, 20, 24, 4096),
        ],
    )
    config_dir = tmp_path / "config"
    config_dir.mkdir()
    (config_dir / "benchmarks.yaml").write_text(
        """
benchmarks:
  - name: NanoMIRACL
    score_groups:
      - name: task
        label: Task
        group_by: task_name
""".strip(),
        encoding="utf-8",
    )
    (config_dir / "overall.yaml").write_text("name: Overall\nlabel: Overall\nbenchmarks:\n  - NanoMIRACL\n", encoding="utf-8")
    docs_dir = tmp_path / "task_docs" / "docs"
    group_dir = docs_dir / "NanoMIRACL"
    group_dir.mkdir(parents=True)
    (group_dir / "index.md").write_text("# NanoMIRACL\n\n## Overview\n\nGroup overview text.\n", encoding="utf-8")
    (group_dir / "ja.md").write_text("# NanoMIRACL / ja\n\n## Overview\n\nJapanese task overview.\n", encoding="utf-8")
    app = create_app(store=LocalDuckDbStore(DuckDbLocation(local_path=db_path)), config_dir=config_dir, docs_dir=docs_dir)

    response = TestClient(app).get("/leaderboard?view=NanoMIRACL&task_scores=1")

    assert response.status_code == 200
    assert 'class="doc-summary-trigger' in response.text
    assert 'data-doc-title="NanoMIRACL"' in response.text
    assert 'data-doc-description="Group overview text."' in response.text
    assert 'data-doc-url="/docs/benchmark-tasks/NanoMIRACL"' in response.text
    assert 'data-doc-label-group="benchmark"' in response.text
    assert 'data-doc-title="NanoMIRACL / ja"' in response.text
    assert 'data-doc-description="Japanese task overview."' in response.text
    assert 'data-doc-url="/docs/benchmark-tasks/NanoMIRACL/ja"' in response.text
    assert 'data-doc-label-group="metric"' in response.text
    assert 'id="doc-summary-modal"' in response.text
    assert "Read the benchmark overview" in response.text


def test_leaderboard_renders_nanobeir_task_doc_triggers_for_short_task_keys(tmp_path: Path) -> None:
    db_path = tmp_path / "results.duckdb"
    _write_task_results(
        db_path,
        [
            (
                "model/a",
                "MNanoBEIR",
                "hakari-bench/NanoBEIR-ja",
                "NanoBEIR-ja",
                "NanoArguAna",
                "arguana",
                "MNanoBEIR::hakari-bench/NanoBEIR-ja::arguana",
                0.90,
                10,
                12,
                8192,
            ),
            (
                "model/b",
                "MNanoBEIR",
                "hakari-bench/NanoBEIR-ja",
                "NanoBEIR-ja",
                "NanoArguAna",
                "arguana",
                "MNanoBEIR::hakari-bench/NanoBEIR-ja::arguana",
                0.80,
                20,
                24,
                4096,
            ),
        ],
    )
    config_dir = tmp_path / "config"
    config_dir.mkdir()
    (config_dir / "benchmarks.yaml").write_text("benchmarks:\n  - name: MNanoBEIR\n", encoding="utf-8")
    (config_dir / "overall.yaml").write_text("name: Overall\nlabel: Overall\nbenchmarks:\n  - MNanoBEIR\n", encoding="utf-8")
    docs_dir = tmp_path / "task_docs" / "docs"
    group_dir = docs_dir / "MNanoBEIR"
    group_dir.mkdir(parents=True)
    (group_dir / "NanoBEIR-ja__NanoArguAna.md").write_text(
        "# MNanoBEIR / NanoBEIR-ja / NanoArguAna\n\n## Overview\n\nArguAna overview.\n",
        encoding="utf-8",
    )
    app = create_app(store=LocalDuckDbStore(DuckDbLocation(local_path=db_path)), config_dir=config_dir, docs_dir=docs_dir)

    response = TestClient(app).get("/leaderboard?view=MNanoBEIR&task_scores=1")

    assert response.status_code == 200
    assert 'data-doc-title="MNanoBEIR / NanoBEIR-ja / NanoArguAna"' in response.text
    assert 'data-doc-url="/docs/benchmark-tasks/MNanoBEIR/NanoBEIR-ja__NanoArguAna"' in response.text
