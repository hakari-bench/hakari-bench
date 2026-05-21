from __future__ import annotations

from collections.abc import Iterator
from contextlib import contextmanager
import socket
import threading
import time
from pathlib import Path
from typing import Any

import duckdb
import pytest
import uvicorn

from hakari_bench.viewer.app import create_app
from hakari_bench.viewer.data import CURRENT_DUCKDB_SCHEMA_VERSION
from hakari_bench.viewer.store import DuckDbLocation, LocalDuckDbStore


@pytest.mark.browser
def test_viewer_browser_smoke_covers_static_javascript(tmp_path: Path) -> None:
    playwright_sync = pytest.importorskip("playwright.sync_api")

    db_path = tmp_path / "results.duckdb"
    _write_browser_task_results(db_path)
    config_dir = tmp_path / "config"
    config_dir.mkdir()
    (config_dir / "benchmarks.yaml").write_text("benchmarks:\n  - name: BenchA\n  - name: NanoRTEB\n", encoding="utf-8")
    (config_dir / "overall.yaml").write_text("name: Overall\nlabel: Overall\nbenchmarks:\n  - BenchA\n", encoding="utf-8")
    docs_dir = tmp_path / "docs" / "benchmark_tasks"
    bench_docs_dir = docs_dir / "BenchA"
    bench_docs_dir.mkdir(parents=True)
    (bench_docs_dir / "index.md").write_text("# BenchA\n\n## Overview\n\nBenchA overview for browser tests.\n", encoding="utf-8")
    (bench_docs_dir / "a1.md").write_text("# BenchA / a1\n\n## Overview\n\nTask a1 overview for browser tests.\n", encoding="utf-8")
    app = create_app(store=LocalDuckDbStore(DuckDbLocation(local_path=db_path)), config_dir=config_dir, docs_dir=docs_dir)

    with _serve_app(app) as base_url:
        with playwright_sync.sync_playwright() as playwright:
            browser = _launch_chromium_or_skip(playwright, playwright_sync.Error)
            try:
                page = browser.new_page(viewport={"width": 1280, "height": 800})
                page.goto(f"{base_url}/#view=Overall&quantization=1&truncate=1&task_z_scores=1", wait_until="domcontentloaded")
                page.wait_for_selector("#leaderboard-panel table", timeout=15_000)

                assert page.evaluate("() => Boolean(window.__hakariApplyHashQueryState && window.__hakariBindModelDetails)")
                assert page.locator("main script:not([src])").count() == 0
                page.get_by_text("256d <- 384").wait_for(timeout=15_000)
                compact_table_state = page.locator("tbody tr:not([hidden]) td").first.evaluate(
                    """(el) => ({
                        paddingTop: parseFloat(getComputedStyle(el).paddingTop),
                        paddingBottom: parseFloat(getComputedStyle(el).paddingBottom),
                    })"""
                )
                assert compact_table_state["paddingTop"] <= 4
                assert compact_table_state["paddingBottom"] <= 4
                task_std_style = page.locator(".task-z-score").first.evaluate(
                    """(el) => ({
                        borderRadius: getComputedStyle(el).borderRadius,
                        borderStyle: getComputedStyle(el).borderStyle,
                        borderWidth: parseFloat(getComputedStyle(el).borderWidth),
                        boxSizing: getComputedStyle(el).boxSizing,
                        borderColor: getComputedStyle(el).borderColor,
                        deltaFontSize: parseFloat(getComputedStyle(el.querySelector(".task-z-score-delta")).fontSize),
                        deltaFontWeight: getComputedStyle(el.querySelector(".task-z-score-delta")).fontWeight,
                        paddingLeft: parseFloat(getComputedStyle(el).paddingLeft),
                        paddingRight: parseFloat(getComputedStyle(el).paddingRight),
                        paddingTop: parseFloat(getComputedStyle(el).paddingTop),
                        valueFontSize: parseFloat(getComputedStyle(el.querySelector(".task-z-score-value")).fontSize),
                        valueFontWeight: getComputedStyle(el.querySelector(".task-z-score-value")).fontWeight,
                        width: parseFloat(getComputedStyle(el).width),
                    })"""
                )
                assert task_std_style["borderRadius"] == "0px"
                assert task_std_style["borderStyle"] == "solid"
                assert task_std_style["borderWidth"] == pytest.approx(1.0, abs=0.1)
                assert task_std_style["borderColor"] == "rgba(29, 27, 24, 0.14)"
                assert task_std_style["boxSizing"] == "border-box"
                assert task_std_style["valueFontSize"] == pytest.approx(13.0, abs=0.1)
                assert task_std_style["deltaFontSize"] == pytest.approx(9.0, abs=0.1)
                assert task_std_style["valueFontWeight"] == "400"
                assert task_std_style["deltaFontWeight"] == "400"
                assert task_std_style["paddingLeft"] > 0
                assert task_std_style["paddingRight"] > 0
                assert task_std_style["paddingTop"] > 0
                assert task_std_style["width"] == pytest.approx(60.0, abs=0.1)

                long_model_row = page.locator("tbody tr", has_text="ft-mmB-L4-bs8192-v1-20260301-QAT-unir-v9").first
                long_model_row.wait_for(timeout=15_000)
                long_model_layout = long_model_row.evaluate(
                    """(row) => {
                        const cells = row.querySelectorAll("td");
                        const modelCell = cells[0].getBoundingClientRect();
                        const modelButton = cells[0].querySelector(".model-detail-trigger").getBoundingClientRect();
                        const bordaRankCell = cells[1].getBoundingClientRect();
                        const meanRankCell = cells[2].getBoundingClientRect();
                        const bordaScoreCell = cells[3].getBoundingClientRect();
                        const modelButtonStyle = getComputedStyle(cells[0].querySelector(".model-detail-trigger"));
                        return {
                            modelCellLeft: modelCell.left,
                            modelCellRight: modelCell.right,
                            modelButtonRight: modelButton.right,
                            bordaRankLeft: bordaRankCell.left,
                            meanRankLeft: meanRankCell.left,
                            bordaScoreLeft: bordaScoreCell.left,
                            modelCellContentFlexWrap: getComputedStyle(cells[0].firstElementChild).flexWrap,
                            modelButtonFontSize: parseFloat(modelButtonStyle.fontSize),
                            modelButtonLineHeight: parseFloat(modelButtonStyle.lineHeight),
                            modelButtonOverflowWrap: modelButtonStyle.overflowWrap,
                            modelButtonWhiteSpace: modelButtonStyle.whiteSpace,
                            modelButtonTextOverflow: modelButtonStyle.textOverflow,
                        };
                    }"""
                )
                assert 0 <= long_model_layout["modelCellLeft"] <= 32
                assert long_model_layout["modelCellRight"] <= long_model_layout["bordaRankLeft"] + 0.5
                assert long_model_layout["bordaRankLeft"] < long_model_layout["meanRankLeft"] < long_model_layout["bordaScoreLeft"]
                assert long_model_layout["modelButtonRight"] <= long_model_layout["bordaRankLeft"] + 0.5
                assert long_model_layout["modelCellContentFlexWrap"] == "wrap"
                assert long_model_layout["modelButtonFontSize"] == pytest.approx(13.0, abs=0.1)
                assert long_model_layout["modelButtonLineHeight"] == pytest.approx(16.25, abs=0.25)
                assert long_model_layout["modelButtonOverflowWrap"] == "anywhere"
                assert long_model_layout["modelButtonWhiteSpace"] == "normal"
                assert long_model_layout["modelButtonTextOverflow"] == "clip"

                tooltip_trigger = page.locator("[data-tooltip]").first
                tooltip_trigger.hover()
                page.locator("#hakari-global-tooltip:not([hidden])").wait_for(timeout=3_000)
                tooltip_state = page.locator("#hakari-global-tooltip").evaluate(
                    """(el) => ({
                        hidden: el.hidden,
                        text: el.textContent,
                        zIndex: getComputedStyle(el).zIndex,
                    })"""
                )
                assert tooltip_state["hidden"] is False
                assert tooltip_state["text"]
                assert tooltip_state["zIndex"] == "1000"
                assert tooltip_trigger.evaluate("(el) => getComputedStyle(el).cursor") == "pointer"
                help_tooltip_style = page.locator(".tooltip-trigger", has_text="?").first.evaluate(
                    """(el) => ({
                        borderRadius: getComputedStyle(el).borderRadius,
                        height: parseFloat(getComputedStyle(el).height),
                        width: parseFloat(getComputedStyle(el).width),
                    })"""
                )
                assert help_tooltip_style["borderRadius"] == "9999px"
                assert help_tooltip_style["height"] == pytest.approx(14.0, abs=0.1)
                assert help_tooltip_style["width"] == pytest.approx(14.0, abs=0.1)
                page.locator("#hakari-global-tooltip").evaluate("(el) => { el.hidden = true; delete el.dataset.visible; }")

                rank_filtered_checkbox = page.locator("#filter-controls input[name='rank_filtered']")
                rank_filtered_tooltip = page.locator("#filter-controls [data-tooltip]").first
                assert rank_filtered_checkbox.is_checked() is False
                rank_filtered_tooltip.click()
                page.locator("#hakari-global-tooltip:not([hidden])").wait_for(timeout=1_000)
                assert rank_filtered_checkbox.is_checked() is False

                doc_trigger = page.locator(".doc-summary-trigger").first
                doc_trigger_style = doc_trigger.evaluate(
                    """(el) => ({
                        borderRadius: getComputedStyle(el).borderRadius,
                        height: parseFloat(getComputedStyle(el).height),
                        width: parseFloat(getComputedStyle(el).width),
                    })"""
                )
                assert doc_trigger_style["borderRadius"] == "9999px"
                assert doc_trigger_style["height"] == pytest.approx(14.0, abs=0.1)
                assert doc_trigger_style["width"] == pytest.approx(14.0, abs=0.1)
                doc_trigger.click()
                page.locator("#doc-summary-modal[open]").wait_for(timeout=5_000)
                assert page.locator("#doc-summary-title").inner_text() == "BenchA"
                assert "BenchA overview" in page.locator("#doc-summary-description").inner_text()
                assert page.locator("#doc-summary-link").get_attribute("target") == "_blank"
                assert page.locator("#doc-summary-link").inner_text() == "Read the BenchA overview"
                page.locator("#doc-summary-modal").evaluate("(modal) => modal.close()")

                page.locator(".model-detail-trigger").first.click()
                page.locator("#model-detail-modal[open]").wait_for(timeout=5_000)
                assert page.locator("#model-detail-title").inner_text() == "model/a"

                page.locator("#model-detail-modal").evaluate("(modal) => modal.close()")
                page.get_by_role("button", name="AR 1").click()
                page.locator("#leaderboard-loading-toast.htmx-request").wait_for(state="detached", timeout=15_000)
                ar_button = page.get_by_role("button", name="AR 1")
                assert "border-cyan-700" in (ar_button.get_attribute("class") or "")

                page.get_by_role("button", name="NanoRTEB").click()
                page.locator("#leaderboard-loading-toast.htmx-request").wait_for(state="detached", timeout=15_000)
                nano_rteb_button = page.get_by_role("button", name="NanoRTEB")
                assert page.locator("h2.text-lg").first.inner_text() == "NanoRTEB"
                nano_rteb_label = nano_rteb_button.locator("xpath=ancestor::*[@data-doc-label-group='benchmark']").first
                active_classes = nano_rteb_label.get_attribute("class") if nano_rteb_label.count() else nano_rteb_button.get_attribute("class")
                assert "border-cyan-700" in (active_classes or "")
            finally:
                browser.close()


def _write_browser_task_results(db_path: Path) -> None:
    con = duckdb.connect(str(db_path))
    try:
        con.execute("CREATE TABLE meta_database (schema_version VARCHAR)")
        con.execute("INSERT INTO meta_database VALUES (?)", [CURRENT_DUCKDB_SCHEMA_VERSION])
        con.execute(
            """
            CREATE TABLE viewer_task_results (
                model_name VARCHAR,
                benchmark VARCHAR,
                dataset_id VARCHAR,
                dataset_name VARCHAR,
                split_name VARCHAR,
                task_name VARCHAR,
                task_key VARCHAR,
                score_target VARCHAR,
                score DOUBLE,
                language VARCHAR,
                languages VARCHAR[],
                active_parameters BIGINT,
                total_parameters BIGINT,
                max_seq_length INTEGER,
                dtype VARCHAR,
                attn_implementation VARCHAR,
                query_prompt VARCHAR,
                document_prompt VARCHAR,
                query_prompt_name VARCHAR,
                document_prompt_name VARCHAR,
                query_encode_task VARCHAR,
                document_encode_task VARCHAR,
                trust_remote_code BOOLEAN,
                embedding_variant_name VARCHAR,
                embedding_dim INTEGER,
                quantization VARCHAR
            )
            """
        )
        con.executemany(
            "INSERT INTO viewer_task_results VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
            [
                _viewer_task_result_row(
                    ("model/a", "BenchA", "bench/a", "BenchA", "en", "a1", "a1", 0.90, 10, 12, 8192, None, 384, None)
                ),
                _viewer_task_result_row(
                    (
                        "model/a",
                        "BenchA",
                        "bench/a",
                        "BenchA",
                        "en",
                        "a1",
                        "a1",
                        0.82,
                        10,
                        12,
                        8192,
                        "truncate_dim_256",
                        256,
                        None,
                    )
                ),
                _viewer_task_result_row(
                    ("model/b", "BenchA", "bench/a", "BenchA", "ar", "a2", "a2", 0.75, 20, 24, 4096, None, 512, None)
                ),
                _viewer_task_result_row(
                    ("model/b", "BenchA", "bench/a", "BenchA", "en", "a1", "a1", 0.73, 20, 24, 4096, None, 512, None)
                ),
                _viewer_task_result_row(
                    (
                        "org/ft-mmB-L4-bs8192-v1-20260301-QAT-unir-v9-extremely-long-model-name",
                        "BenchA",
                        "bench/a",
                        "BenchA",
                        "en",
                        "a1",
                        "a1",
                        0.72,
                        30,
                        36,
                        4096,
                        None,
                        384,
                        None,
                    )
                ),
                _viewer_task_result_row(
                    (
                        "org/ft-mmB-L4-bs8192-v1-20260301-QAT-unir-v9-extremely-long-model-name",
                        "BenchA",
                        "bench/a",
                        "BenchA",
                        "ar",
                        "a2",
                        "a2",
                        0.69,
                        30,
                        36,
                        4096,
                        None,
                        384,
                        None,
                    )
                ),
                _viewer_task_result_row(
                    (
                        "org/ft-mmB-L4-bs8192-v1-20260301-QAT-unir-v9-extremely-long-model-name",
                        "BenchA",
                        "bench/a",
                        "BenchA",
                        "en",
                        "a1",
                        "a1",
                        0.68,
                        30,
                        36,
                        4096,
                        None,
                        384,
                        "int8",
                    )
                ),
                _viewer_task_result_row(
                    (
                        "org/ft-mmB-L4-bs8192-v1-20260301-QAT-unir-v9-extremely-long-model-name",
                        "BenchA",
                        "bench/a",
                        "BenchA",
                        "ar",
                        "a2",
                        "a2",
                        0.66,
                        30,
                        36,
                        4096,
                        None,
                        384,
                        "int8",
                    )
                ),
                _viewer_task_result_row(
                    ("model/a", "BenchA", "bench/a", "BenchA", "ar", "a2", "a2", 0.70, 10, 12, 8192, None, 384, None)
                ),
                _viewer_task_result_row(
                    (
                        "model/a",
                        "BenchA",
                        "bench/a",
                        "BenchA",
                        "ar",
                        "a2",
                        "a2",
                        0.62,
                        10,
                        12,
                        8192,
                        "truncate_dim_256",
                        256,
                        None,
                    )
                ),
                _viewer_task_result_row(
                    ("model/a", "NanoRTEB", "bench/rteb", "NanoRTEB", "en", "r1", "r1", 0.65, 10, 12, 8192, None, 384, None)
                ),
                _viewer_task_result_row(
                    ("model/b", "NanoRTEB", "bench/rteb", "NanoRTEB", "en", "r1", "r1", 0.55, 20, 24, 4096, None, 512, None)
                ),
            ],
        )
    finally:
        con.close()


def _viewer_task_result_row(row: tuple) -> tuple:
    return (
        *row[:4],
        None,
        row[5],
        row[6],
        "all",
        row[7],
        row[4],
        [row[4]],
        *row[8:11],
        None,
        None,
        None,
        None,
        None,
        None,
        None,
        None,
        None,
        *row[11:],
    )


@contextmanager
def _serve_app(app: Any) -> Iterator[str]:
    port = _free_port()
    config = uvicorn.Config(app, host="127.0.0.1", port=port, log_level="warning")
    server = uvicorn.Server(config)
    thread = threading.Thread(target=server.run, daemon=True)
    thread.start()
    try:
        deadline = time.time() + 10
        while not server.started:
            if not thread.is_alive():
                raise RuntimeError("Uvicorn server stopped before startup completed")
            if time.time() > deadline:
                raise TimeoutError("Timed out waiting for Uvicorn test server")
            time.sleep(0.05)
        yield f"http://127.0.0.1:{port}"
    finally:
        server.should_exit = True
        thread.join(timeout=5)


def _free_port() -> int:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.bind(("127.0.0.1", 0))
        return int(sock.getsockname()[1])


def _launch_chromium_or_skip(playwright: Any, playwright_error: type[Exception]):
    try:
        return playwright.chromium.launch()
    except playwright_error as exc:
        message = str(exc)
        if "Executable doesn't exist" in message or "playwright install" in message:
            pytest.skip("Playwright Chromium is not installed; run `uv run playwright install chromium`.")
        raise
