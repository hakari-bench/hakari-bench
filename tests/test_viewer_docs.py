from __future__ import annotations

from pathlib import Path
import re

from fastapi.testclient import TestClient

from hakari_bench.viewer.app import create_app
from hakari_bench.viewer.docs import BenchmarkDocs, render_markdown_to_html
from hakari_bench.viewer.store import DuckDbLocation, LocalDuckDbStore

from tests.test_viewer import _write_task_results


def test_benchmark_docs_resolves_group_and_task_overviews(tmp_path: Path) -> None:
    docs_dir = tmp_path / "docs" / "benchmark_tasks"
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


def test_benchmark_docs_lists_group_docs_with_descriptions(tmp_path: Path) -> None:
    docs_dir = tmp_path / "docs" / "benchmark_tasks"
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
    docs_dir = tmp_path / "docs" / "benchmark_tasks"
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
    docs_dir = tmp_path / "docs" / "benchmark_tasks"
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
        "# Title\n\n## Overview\n\nA [safe link](https://example.com) and <script>x</script>.\n\n- one\n- two\n"
    )

    assert "<h1>Title</h1>" in html
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
    docs_dir = Path("docs/benchmark_tasks")
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


def test_docs_endpoint_renders_markdown_page_and_rejects_missing_docs(tmp_path: Path) -> None:
    db_path = tmp_path / "results.duckdb"
    _write_task_results(db_path, [("model/a", "NanoMIRACL", "bench/a", "NanoMIRACL", "ja", "ja", "NanoMIRACL::ja", 0.90, 10, 12, 8192)])
    config_dir = tmp_path / "config"
    config_dir.mkdir()
    (config_dir / "benchmarks.yaml").write_text("benchmarks:\n  - name: NanoMIRACL\n", encoding="utf-8")
    (config_dir / "overall.yaml").write_text("name: Overall\nlabel: Overall\nbenchmarks:\n  - NanoMIRACL\n", encoding="utf-8")
    docs_dir = tmp_path / "docs" / "benchmark_tasks"
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
    docs_dir = tmp_path / "docs" / "benchmark_tasks"
    group_dir = docs_dir / "NanoMIRACL"
    group_dir.mkdir(parents=True)
    (group_dir / "index.md").write_text("# NanoMIRACL\n\n## Overview\n\nMIRACL overview.\n", encoding="utf-8")
    app = create_app(store=LocalDuckDbStore(DuckDbLocation(local_path=db_path)), config_dir=config_dir, docs_dir=docs_dir)

    response = TestClient(app).get("/docs/benchmark-tasks")

    assert response.status_code == 200
    assert "Benchmark documentation" in response.text
    assert 'class="font-semibold text-cyan-700 underline underline-offset-2" href="/docs/benchmark-tasks/NanoMIRACL"' in response.text
    assert "MIRACL overview." in response.text


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
    docs_dir = tmp_path / "docs" / "benchmark_tasks"
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
    assert '<a class="underline underline-offset-2" href="/docs/benchmark-tasks">Benchmark documentation</a>' in group_response.text
    assert '<span aria-current="page">NanoCodeRAG</span>' in group_response.text
    assert task_response.status_code == 200
    assert '<a class="underline underline-offset-2" href="/docs/benchmark-tasks">Benchmark documentation</a>' in task_response.text
    assert '<a class="underline underline-offset-2" href="/docs/benchmark-tasks/NanoCodeRAG">NanoCodeRAG</a>' in task_response.text
    assert '<span aria-current="page">NanoCodeRAGOnlineTutorials</span>' in task_response.text


def test_docs_endpoint_renders_group_task_summary_links(tmp_path: Path) -> None:
    db_path = tmp_path / "results.duckdb"
    _write_task_results(db_path, [("model/a", "NanoCoIR", "bench/a", "NanoCoIR", "NanoApps", "NanoApps", "NanoApps", 0.90, 10, 12, 8192)])
    config_dir = tmp_path / "config"
    config_dir.mkdir()
    (config_dir / "benchmarks.yaml").write_text("benchmarks:\n  - name: NanoCoIR\n", encoding="utf-8")
    (config_dir / "overall.yaml").write_text("name: Overall\nlabel: Overall\nbenchmarks:\n  - NanoCoIR\n", encoding="utf-8")
    docs_dir = tmp_path / "docs" / "benchmark_tasks"
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
    docs_dir = tmp_path / "docs" / "benchmark_tasks"
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
    docs_dir = tmp_path / "docs" / "benchmark_tasks"
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
