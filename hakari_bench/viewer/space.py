from __future__ import annotations

import os
from pathlib import Path

from hakari_bench.viewer.app import create_app
from hakari_bench.viewer.store import LocalDuckDbStore, resolve_duckdb_location


def create_space_app():
    data_dir = Path(os.getenv("HAKARI_BENCH_VIEWER_DATA_DIR", "output/viewer"))
    config_dir = Path(os.getenv("HAKARI_BENCH_VIEWER_CONFIG_DIR", "config/viewer"))
    location = resolve_duckdb_location(
        data_dir=data_dir,
        duckdb_path=None,
        source_results_dir=None,
        source_duckdb_path=None,
    )
    store = LocalDuckDbStore(location)
    store.ensure_current()
    return create_app(store=store, config_dir=config_dir)
