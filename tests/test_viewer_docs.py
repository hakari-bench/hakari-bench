from __future__ import annotations

from pathlib import Path

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
