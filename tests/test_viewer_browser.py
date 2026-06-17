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
    docs_dir = tmp_path / "task_docs" / "docs"
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
                section_icon_state = page.locator("h1 svg.section-heading-icon[data-icon='hakari-bench']").first.evaluate(
                    """(el) => ({
                        width: parseFloat(getComputedStyle(el).width),
                        height: parseFloat(getComputedStyle(el).height),
                        color: getComputedStyle(el).color,
                    })"""
                )
                assert section_icon_state["width"] == pytest.approx(14.0, abs=0.1)
                assert section_icon_state["height"] == pytest.approx(14.0, abs=0.1)
                assert section_icon_state["color"] != "rgb(0, 0, 0)"
                assert page.locator("button", has_text="Variant impact").count() == 0
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
                        backgroundColor: getComputedStyle(el).backgroundColor,
                        borderRadius: getComputedStyle(el).borderRadius,
                        borderStyle: getComputedStyle(el).borderStyle,
                        borderWidth: parseFloat(getComputedStyle(el).borderWidth),
                        boxSizing: getComputedStyle(el).boxSizing,
                        deltaFontSize: parseFloat(getComputedStyle(el.querySelector(".task-z-score-delta")).fontSize),
                        deltaFontWeight: getComputedStyle(el.querySelector(".task-z-score-delta")).fontWeight,
                        deltaColor: getComputedStyle(el.querySelector(".task-z-score-delta")).color,
                        paddingLeft: parseFloat(getComputedStyle(el).paddingLeft),
                        paddingRight: parseFloat(getComputedStyle(el).paddingRight),
                        paddingTop: parseFloat(getComputedStyle(el).paddingTop),
                        valueFontSize: parseFloat(getComputedStyle(el.querySelector(".task-z-score-value")).fontSize),
                        valueFontWeight: getComputedStyle(el.querySelector(".task-z-score-value")).fontWeight,
                        valueColor: getComputedStyle(el.querySelector(".task-z-score-value")).color,
                        width: parseFloat(getComputedStyle(el).width),
                    })"""
                )
                assert task_std_style["backgroundColor"] == "rgba(0, 0, 0, 0)"
                assert task_std_style["borderRadius"] == "0px"
                assert task_std_style["borderStyle"] == "none"
                assert task_std_style["borderWidth"] == pytest.approx(0.0, abs=0.1)
                assert task_std_style["boxSizing"] == "border-box"
                assert task_std_style["valueFontSize"] == pytest.approx(13.0, abs=0.1)
                assert task_std_style["deltaFontSize"] == pytest.approx(9.0, abs=0.1)
                assert task_std_style["valueFontWeight"] == "400"
                assert task_std_style["deltaFontWeight"] == "400"
                assert task_std_style["valueColor"] == task_std_style["deltaColor"]
                assert task_std_style["valueColor"] != "rgb(36, 48, 54)"
                assert task_std_style["paddingLeft"] > 0
                assert task_std_style["paddingRight"] > 0
                assert task_std_style["paddingTop"] > 0
                assert task_std_style["width"] == pytest.approx(60.0, abs=0.1)

                long_model_row = page.locator("tbody tr", has_text="ft-mmB-L4-bs8192-v1-20260301-QAT-unir-v9").first
                long_model_row.wait_for(timeout=15_000)
                long_model_layout = long_model_row.evaluate(
                    """(row) => {
                        const cells = row.querySelectorAll("td");
                        const headers = row.closest("table").querySelectorAll("thead th");
                        const rankCell = cells[0].getBoundingClientRect();
                        const modelCell = cells[1].getBoundingClientRect();
                        const modelButton = cells[1].querySelector(".model-detail-trigger").getBoundingClientRect();
                        const badgeRow = cells[1].querySelector(".model-variant-badges").getBoundingClientRect();
                        const bordaScoreCell = cells[2].getBoundingClientRect();
                        const macroMeanCell = cells[3].getBoundingClientRect();
                        const microMeanCell = cells[4].getBoundingClientRect();
                        const modelButtonStyle = getComputedStyle(cells[1].querySelector(".model-detail-trigger"));
                        const badgeStyle = getComputedStyle(cells[1].querySelector(".model-variant-badges span"));
                        const rankStyle = getComputedStyle(cells[0]);
                        const bordaScoreStyle = getComputedStyle(cells[2]);
                        const rankHeaderStyle = getComputedStyle(headers[0]);
                        const modelHeaderStyle = getComputedStyle(headers[1]);
                        const bordaScoreHeaderStyle = getComputedStyle(headers[2]);
                        const headerLabelLeft = (index) => headers[index].querySelector("button span:first-child").getBoundingClientRect().left;
                        const bodyContentLeft = (index) => {
                            const cellStyle = getComputedStyle(cells[index]);
                            return cells[index].getBoundingClientRect().left + parseFloat(cellStyle.paddingLeft);
                        };
                        return {
                            rankCellLeft: rankCell.left,
                            rankCellRight: rankCell.right,
                            modelCellLeft: modelCell.left,
                            modelCellRight: modelCell.right,
                            modelButtonRight: modelButton.right,
                            badgeRowTop: badgeRow.top,
                            badgeRowLeft: badgeRow.left,
                            modelButtonBottom: modelButton.bottom,
                            modelButtonTop: modelButton.top,
                            bordaScoreLeft: bordaScoreCell.left,
                            macroMeanLeft: macroMeanCell.left,
                            microMeanLeft: microMeanCell.left,
                            rankHeaderText: headers[0].innerText,
                            modelHeaderText: headers[1].innerText,
                            bordaScoreHeaderText: headers[2].innerText,
                            macroMeanHeaderText: headers[3].innerText,
                            microMeanHeaderText: headers[4].innerText,
                            bordaScoreHeaderLabelLeft: headerLabelLeft(2),
                            bordaScoreBodyContentLeft: bodyContentLeft(2),
                            macroMeanHeaderLabelLeft: headerLabelLeft(3),
                            macroMeanBodyContentLeft: bodyContentLeft(3),
                            microMeanHeaderLabelLeft: headerLabelLeft(4),
                            microMeanBodyContentLeft: bodyContentLeft(4),
                            bordaScoreHeaderButtonTextAlign: getComputedStyle(headers[2].querySelector("button")).textAlign,
                            macroMeanHeaderButtonTextAlign: getComputedStyle(headers[3].querySelector("button")).textAlign,
                            microMeanHeaderButtonTextAlign: getComputedStyle(headers[4].querySelector("button")).textAlign,
                            rankHeaderPosition: rankHeaderStyle.position,
                            modelHeaderPosition: modelHeaderStyle.position,
                            bordaScoreHeaderPosition: bordaScoreHeaderStyle.position,
                            rankCellPosition: rankStyle.position,
                            modelCellContentFlexWrap: getComputedStyle(cells[1].firstElementChild).flexWrap,
                            modelCellContentFlexDirection: getComputedStyle(cells[1].firstElementChild).flexDirection,
                            modelButtonFontSize: parseFloat(modelButtonStyle.fontSize),
                            badgeFontSize: parseFloat(badgeStyle.fontSize),
                            badgePaddingLeft: parseFloat(badgeStyle.paddingLeft),
                            badgePaddingTop: parseFloat(badgeStyle.paddingTop),
                            rankTextAlign: rankStyle.textAlign,
                            bordaScoreFontSize: parseFloat(bordaScoreStyle.fontSize),
                            bordaScoreTextAlign: bordaScoreStyle.textAlign,
                            modelButtonLineHeight: parseFloat(modelButtonStyle.lineHeight),
                            modelButtonOverflowWrap: modelButtonStyle.overflowWrap,
                            modelButtonWhiteSpace: modelButtonStyle.whiteSpace,
                            modelButtonTextOverflow: modelButtonStyle.textOverflow,
                        };
                    }"""
                )
                assert 0 <= long_model_layout["rankCellLeft"] <= 32
                assert long_model_layout["rankCellRight"] <= long_model_layout["modelCellLeft"] + 0.5
                assert long_model_layout["modelCellRight"] <= long_model_layout["bordaScoreLeft"] + 0.5
                assert long_model_layout["bordaScoreLeft"] < long_model_layout["macroMeanLeft"] < long_model_layout["microMeanLeft"]
                assert long_model_layout["modelButtonRight"] <= long_model_layout["bordaScoreLeft"] + 0.5
                assert long_model_layout["badgeRowTop"] >= long_model_layout["modelButtonTop"] - 0.5
                assert long_model_layout["rankHeaderText"] == ""
                assert "Model" in long_model_layout["modelHeaderText"]
                assert "Borda" in long_model_layout["bordaScoreHeaderText"]
                assert "Mean" in long_model_layout["macroMeanHeaderText"]
                assert "Mean" in long_model_layout["microMeanHeaderText"]
                assert long_model_layout["modelCellContentFlexWrap"] == "wrap"
                assert long_model_layout["modelCellContentFlexDirection"] == "row"
                assert long_model_layout["modelButtonFontSize"] == pytest.approx(13.0, abs=0.1)
                assert long_model_layout["badgeFontSize"] < long_model_layout["modelButtonFontSize"]
                assert long_model_layout["badgePaddingLeft"] <= 4.0
                assert long_model_layout["badgePaddingTop"] == pytest.approx(0.0, abs=0.1)
                assert long_model_layout["rankTextAlign"] == "right"
                assert long_model_layout["bordaScoreHeaderButtonTextAlign"] == "left"
                assert long_model_layout["macroMeanHeaderButtonTextAlign"] == "left"
                assert long_model_layout["microMeanHeaderButtonTextAlign"] == "left"
                assert long_model_layout["bordaScoreHeaderLabelLeft"] == pytest.approx(
                    long_model_layout["bordaScoreBodyContentLeft"], abs=0.5
                )
                assert long_model_layout["macroMeanHeaderLabelLeft"] == pytest.approx(
                    long_model_layout["macroMeanBodyContentLeft"], abs=0.5
                )
                assert long_model_layout["microMeanHeaderLabelLeft"] == pytest.approx(
                    long_model_layout["microMeanBodyContentLeft"], abs=0.5
                )
                assert long_model_layout["rankHeaderPosition"] == "sticky"
                assert long_model_layout["modelHeaderPosition"] == "sticky"
                assert long_model_layout["bordaScoreHeaderPosition"] == "static"
                assert long_model_layout["rankCellPosition"] == "sticky"
                assert long_model_layout["bordaScoreFontSize"] == pytest.approx(long_model_layout["modelButtonFontSize"], abs=0.1)
                assert long_model_layout["bordaScoreTextAlign"] == "left"
                assert long_model_layout["modelButtonLineHeight"] == pytest.approx(16.25, abs=0.25)
                assert long_model_layout["modelButtonOverflowWrap"] == "anywhere"
                assert long_model_layout["modelButtonWhiteSpace"] == "normal"
                assert long_model_layout["modelButtonTextOverflow"] == "clip"
                page.set_viewport_size({"width": 1024, "height": 800})
                page.locator("#leaderboard-panel table").first.wait_for(timeout=5_000)
                compact_layout = long_model_row.evaluate(
                    """(row) => {
                        const cells = row.querySelectorAll("td");
                        const headers = row.closest("table").querySelectorAll("thead th");
                        const scroller = row.closest(".leaderboard-table-scroll");
                        const rankCell = cells[0].getBoundingClientRect();
                        const modelCell = cells[1].getBoundingClientRect();
                        const bordaScoreCell = cells[2].getBoundingClientRect();
                        const rankHeader = headers[0].getBoundingClientRect();
                        const modelHeader = headers[1].getBoundingClientRect();
                        const bordaScoreHeader = headers[2].getBoundingClientRect();
                        scroller.scrollLeft = 240;
                        const rankAfterScroll = cells[0].getBoundingClientRect();
                        const modelAfterScroll = cells[1].getBoundingClientRect();
                        const bordaScoreAfterScroll = cells[2].getBoundingClientRect();
                        const rankHeaderAfterScroll = headers[0].getBoundingClientRect();
                        const modelHeaderAfterScroll = headers[1].getBoundingClientRect();
                        const bordaScoreHeaderAfterScroll = headers[2].getBoundingClientRect();
                        return {
                            rankCellLeft: rankCell.left,
                            rankCellRight: rankCell.right,
                            modelCellLeft: modelCell.left,
                            modelCellRight: modelCell.right,
                            bordaScoreLeft: bordaScoreCell.left,
                            rankHeaderLeft: rankHeader.left,
                            rankHeaderRight: rankHeader.right,
                            modelHeaderLeft: modelHeader.left,
                            modelHeaderRight: modelHeader.right,
                            bordaScoreHeaderLeft: bordaScoreHeader.left,
                            rankAfterScrollLeft: rankAfterScroll.left,
                            modelAfterScrollLeft: modelAfterScroll.left,
                            bordaScoreAfterScrollLeft: bordaScoreAfterScroll.left,
                            rankHeaderAfterScrollLeft: rankHeaderAfterScroll.left,
                            modelHeaderAfterScrollLeft: modelHeaderAfterScroll.left,
                            bordaScoreHeaderAfterScrollLeft: bordaScoreHeaderAfterScroll.left,
                        };
                    }"""
                )
                assert compact_layout["rankCellRight"] == pytest.approx(compact_layout["modelCellLeft"], abs=0.5)
                assert compact_layout["modelCellRight"] == pytest.approx(compact_layout["bordaScoreLeft"], abs=0.5)
                assert compact_layout["rankHeaderRight"] == pytest.approx(compact_layout["modelHeaderLeft"], abs=0.5)
                assert compact_layout["modelHeaderRight"] == pytest.approx(compact_layout["bordaScoreHeaderLeft"], abs=0.5)
                assert compact_layout["rankAfterScrollLeft"] == pytest.approx(compact_layout["rankCellLeft"], abs=0.5)
                assert compact_layout["modelAfterScrollLeft"] == pytest.approx(compact_layout["modelCellLeft"], abs=0.5)
                assert compact_layout["rankHeaderAfterScrollLeft"] == pytest.approx(compact_layout["rankHeaderLeft"], abs=0.5)
                assert compact_layout["modelHeaderAfterScrollLeft"] == pytest.approx(compact_layout["modelHeaderLeft"], abs=0.5)
                assert compact_layout["bordaScoreAfterScrollLeft"] <= compact_layout["bordaScoreLeft"]
                assert compact_layout["bordaScoreHeaderAfterScrollLeft"] <= compact_layout["bordaScoreHeaderLeft"]

                hover_before = long_model_row.locator("td").first.evaluate("(el) => getComputedStyle(el).backgroundColor")
                long_model_row.hover()
                hover_after = long_model_row.locator("td").first.evaluate("(el) => getComputedStyle(el).backgroundColor")
                hover_state = {"before": hover_before, "after": hover_after}
                assert hover_state["after"] != hover_state["before"]

                page.locator("#filter-controls-panel").evaluate("(el) => { el.open = true; }")
                rank_filtered_checkbox = page.locator("#filter-controls input[type='checkbox'][name='rank_filtered']")
                help_trigger = page.locator("#filter-controls .refine-results-actions .help-summary-trigger").first
                assert rank_filtered_checkbox.is_checked() is False
                help_trigger.click()
                page.locator("#help-summary-modal[open]").wait_for(timeout=3_000)
                help_modal_state = page.locator("#help-summary-modal").evaluate(
                    """(el) => ({
                        open: el.open,
                        heading: el.querySelector("#help-summary-heading").textContent,
                        summary: el.querySelector("#help-summary-short").textContent,
                        details: el.querySelector("#help-summary-details").textContent,
                        zIndex: getComputedStyle(el).zIndex,
                    })"""
                )
                assert help_modal_state["open"] is True
                assert help_modal_state["heading"] == "Recalculate ranks from filters"
                assert help_modal_state["summary"]
                assert help_modal_state["details"]
                assert help_trigger.evaluate("(el) => getComputedStyle(el).cursor") == "pointer"
                assert rank_filtered_checkbox.is_checked() is False
                help_tooltip_style = page.locator(".help-summary-trigger svg[data-icon='circle-help']").first.evaluate(
                    """(el) => ({
                        parentBorderRadius: getComputedStyle(el.parentElement).borderRadius,
                        height: parseFloat(getComputedStyle(el).height),
                        width: parseFloat(getComputedStyle(el).width),
                        stroke: getComputedStyle(el).stroke,
                    })"""
                )
                assert help_tooltip_style["parentBorderRadius"] == "9999px"
                assert help_tooltip_style["height"] == pytest.approx(14.0, abs=0.1)
                assert help_tooltip_style["width"] >= 12.0
                assert help_tooltip_style["stroke"] != "none"
                page.locator("#help-summary-modal").evaluate("(modal) => modal.close()")

                doc_trigger = page.locator(".doc-summary-trigger").first
                doc_trigger_style = doc_trigger.evaluate(
                    """(el) => ({
                        borderRadius: getComputedStyle(el).borderRadius,
                        height: parseFloat(getComputedStyle(el).height),
                        width: parseFloat(getComputedStyle(el).width),
                        iconCount: el.querySelectorAll("svg[data-icon='book-open']").length,
                    })"""
                )
                assert doc_trigger_style["borderRadius"] == "9999px"
                assert doc_trigger_style["height"] == pytest.approx(14.0, abs=0.1)
                assert doc_trigger_style["width"] == pytest.approx(14.0, abs=0.1)
                assert doc_trigger_style["iconCount"] == 1
                doc_trigger.click()
                page.locator("#doc-summary-modal[open]").wait_for(timeout=5_000)
                assert page.locator("#doc-summary-heading").inner_text() == "BenchA"
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

                page.get_by_role("button", name="RTEB").click()
                page.locator("#leaderboard-loading-toast.htmx-request").wait_for(state="detached", timeout=15_000)
                nano_rteb_button = page.get_by_role("button", name="RTEB")
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
