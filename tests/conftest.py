from __future__ import annotations

from pathlib import Path

import pytest


@pytest.fixture(autouse=True)
def _isolated_result_extract_cache(monkeypatch: pytest.MonkeyPatch, tmp_path: Path) -> None:
    # CLI builds enable the result extract cache by default; keep tests from
    # writing into the user's home cache directory.
    monkeypatch.setenv("HAKARI_BENCH_RESULT_CACHE_DIR", str(tmp_path / "result-extract-cache"))
