from __future__ import annotations

import shutil
from dataclasses import dataclass
from pathlib import Path


DEFAULT_DUCKDB_NAME = "nano_ir_bench.duckdb"


@dataclass(frozen=True)
class DuckDbLocation:
    local_path: Path
    source_path: Path | None = None


class LocalDuckDbStore:
    """Keeps a local DuckDB copy current before each page render."""

    def __init__(self, location: DuckDbLocation) -> None:
        self.location = location

    @property
    def path(self) -> Path:
        return self.location.local_path

    def ensure_current(self) -> bool:
        source = self.location.source_path
        destination = self.location.local_path
        if source is None or not source.exists():
            return False
        if destination.exists() and destination.stat().st_mtime >= source.stat().st_mtime:
            return False
        destination.parent.mkdir(parents=True, exist_ok=True)
        temp_path = destination.with_suffix(destination.suffix + ".tmp")
        shutil.copy2(source, temp_path)
        temp_path.replace(destination)
        return True


def resolve_duckdb_location(
    *,
    data_dir: Path,
    duckdb_path: Path | None,
    source_output_dir: Path | None,
    source_duckdb_path: Path | None,
) -> DuckDbLocation:
    local_path = duckdb_path or data_dir / DEFAULT_DUCKDB_NAME
    source_path = source_duckdb_path or _source_from_output_dir(source_output_dir) or _discover_source_duckdb()
    if source_path is not None and source_path.resolve() == local_path.resolve():
        source_path = None
    return DuckDbLocation(local_path=local_path, source_path=source_path)


def _source_from_output_dir(source_output_dir: Path | None) -> Path | None:
    if source_output_dir is None:
        return None
    candidate = source_output_dir / "results" / DEFAULT_DUCKDB_NAME
    return candidate if candidate.exists() else None


def _discover_source_duckdb() -> Path | None:
    candidates = [
        Path("../nano_ir_bench/output/results") / DEFAULT_DUCKDB_NAME,
        Path("../nano-ir-bench/output/results") / DEFAULT_DUCKDB_NAME,
        Path("../../nano-ir-bench/output/results") / DEFAULT_DUCKDB_NAME,
        Path("output/results") / DEFAULT_DUCKDB_NAME,
    ]
    for candidate in candidates:
        if candidate.exists():
            return candidate
    return None
