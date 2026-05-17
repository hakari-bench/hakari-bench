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
    app = create_app(store=LocalDuckDbStore(DuckDbLocation(local_path=db_path)), config_dir=config_dir)

    with _serve_app(app) as base_url:
        with playwright_sync.sync_playwright() as playwright:
            browser = _launch_chromium_or_skip(playwright, playwright_sync.Error)
            try:
                page = browser.new_page(viewport={"width": 1280, "height": 800})
                page.goto(f"{base_url}/#view=Overall&truncate=1", wait_until="domcontentloaded")
                page.wait_for_selector("#leaderboard-panel table", timeout=15_000)

                assert page.evaluate("Boolean(window.__hakariApplyHashQueryState && window.__hakariBindModelDetails)")
                assert page.locator("main script:not([src])").count() == 0
                page.get_by_text("256d <- 384").wait_for(timeout=15_000)

                tooltip_trigger = page.locator("[data-tooltip]").first
                tooltip_trigger.hover()
                page.wait_for_function("!document.getElementById('hakari-global-tooltip').hidden", timeout=3_000)
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

                page.locator(".model-detail-trigger").first.click()
                page.locator("#model-detail-modal[open]").wait_for(timeout=5_000)
                assert page.locator("#model-detail-title").inner_text() == "model/a"

                page.locator("#model-detail-modal").evaluate("(modal) => modal.close()")
                page.get_by_role("button", name="AR 1").click()
                page.wait_for_function("!document.querySelector('#leaderboard-loading-toast.htmx-request')", timeout=15_000)
                ar_button = page.get_by_role("button", name="AR 1")
                assert "border-cyan-700" in (ar_button.get_attribute("class") or "")

                page.get_by_role("button", name="NanoRTEB").click()
                page.wait_for_function("!document.querySelector('#leaderboard-loading-toast.htmx-request')", timeout=15_000)
                nano_rteb_button = page.get_by_role("button", name="NanoRTEB")
                assert page.locator("h2.text-lg").first.inner_text() == "NanoRTEB"
                assert "border-cyan-700" in (nano_rteb_button.get_attribute("class") or "")
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
