from __future__ import annotations

import os
import shutil
from dataclasses import dataclass
from pathlib import Path
from time import monotonic


DEFAULT_DUCKDB_NAME = "hakari_bench.duckdb"
DEFAULT_HF_DUCKDB_PATH = "duckdb/hakari_bench.duckdb"
DEFAULT_HF_SOURCE_CHECK_TTL_SECONDS = 600.0


@dataclass(frozen=True)
class HuggingFaceDuckDbSource:
    repo_id: str
    filename: str = DEFAULT_HF_DUCKDB_PATH
    revision: str | None = None


@dataclass(frozen=True)
class DuckDbLocation:
    local_path: Path
    source_path: Path | None = None
    hf_source: HuggingFaceDuckDbSource | None = None


class LocalDuckDbStore:
    """Keeps a local DuckDB copy current before each page render."""

    def __init__(self, location: DuckDbLocation) -> None:
        self.location = location
        self._last_hf_source_check_at: float | None = None

    @property
    def path(self) -> Path:
        return self.location.local_path

    def ensure_current(self) -> bool:
        if self._hf_source_check_is_fresh():
            return False
        source = self._source_path()
        self._mark_hf_source_checked()
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

    def _source_path(self) -> Path | None:
        if self.location.hf_source is not None:
            return _download_hf_duckdb(self.location.hf_source)
        return self.location.source_path

    def _hf_source_check_is_fresh(self) -> bool:
        if self.location.hf_source is None:
            return False
        if not self.location.local_path.exists():
            return False
        if self._last_hf_source_check_at is None:
            return False
        return monotonic() - self._last_hf_source_check_at < DEFAULT_HF_SOURCE_CHECK_TTL_SECONDS

    def _mark_hf_source_checked(self) -> None:
        if self.location.hf_source is not None:
            self._last_hf_source_check_at = monotonic()


def resolve_duckdb_location(
    *,
    data_dir: Path,
    duckdb_path: Path | None,
    source_results_dir: Path | None,
    source_duckdb_path: Path | None,
    hf_dataset_repo_id: str | None = None,
    hf_dataset_path: str | None = None,
    hf_dataset_revision: str | None = None,
) -> DuckDbLocation:
    local_path = duckdb_path or _env_path("HAKARI_BENCH_VIEWER_DUCKDB_PATH") or data_dir / DEFAULT_DUCKDB_NAME
    source_results_dir = source_results_dir or _env_path("HAKARI_BENCH_VIEWER_SOURCE_RESULTS_DIR")
    hf_source = _resolve_hf_source(
        repo_id=hf_dataset_repo_id,
        filename=hf_dataset_path,
        revision=hf_dataset_revision,
    )
    source_path = (
        source_duckdb_path
        or _env_path("HAKARI_BENCH_VIEWER_SOURCE_DUCKDB_PATH")
        or _source_from_results_dir(source_results_dir)
    )
    if source_path is None and hf_source is None:
        source_path = _discover_source_duckdb()
    if source_path is not None and source_path.resolve() == local_path.resolve():
        source_path = None
    if source_path is not None:
        hf_source = None
    return DuckDbLocation(local_path=local_path, source_path=source_path, hf_source=hf_source)


def _env_path(name: str) -> Path | None:
    value = os.getenv(name)
    return Path(value) if value else None


def _resolve_hf_source(
    *,
    repo_id: str | None,
    filename: str | None,
    revision: str | None,
) -> HuggingFaceDuckDbSource | None:
    repo_id = repo_id or os.getenv("HAKARI_BENCH_VIEWER_HF_DATASET_REPO_ID")
    if not repo_id:
        return None
    filename = filename or os.getenv("HAKARI_BENCH_VIEWER_HF_DATASET_PATH") or DEFAULT_HF_DUCKDB_PATH
    revision = revision or os.getenv("HAKARI_BENCH_VIEWER_HF_DATASET_REVISION") or None
    return HuggingFaceDuckDbSource(repo_id=repo_id, filename=filename, revision=revision)


def _download_hf_duckdb(source: HuggingFaceDuckDbSource) -> Path:
    from huggingface_hub import hf_hub_download

    return Path(
        hf_hub_download(
            repo_id=source.repo_id,
            filename=source.filename,
            repo_type="dataset",
            revision=source.revision,
        )
    )


def _source_from_results_dir(source_results_dir: Path | None) -> Path | None:
    if source_results_dir is None:
        return None
    candidate = source_results_dir / DEFAULT_DUCKDB_NAME
    return candidate if candidate.exists() else None


def _discover_source_duckdb() -> Path | None:
    candidates = [
        Path("../hakari-bench/output/results") / DEFAULT_DUCKDB_NAME,
        Path("../../hakari-bench/output/results") / DEFAULT_DUCKDB_NAME,
        Path("output/results") / DEFAULT_DUCKDB_NAME,
    ]
    for candidate in candidates:
        if candidate.exists():
            return candidate
    return None
