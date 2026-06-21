from __future__ import annotations

from pathlib import Path
from types import SimpleNamespace

import pytest

from scripts.upload_leaderboard_duckdb import (
    DEFAULT_DUCKDB_PATH_IN_REPO,
    DuckDbSizeIncreaseError,
    assert_size_within_limit,
    remote_duckdb_file,
    upload_leaderboard_duckdb,
)


class FakeHfApi:
    def __init__(self, *, remote_size: int | None) -> None:
        self.remote_size = remote_size
        self.create_repo_calls: list[dict[str, object]] = []
        self.upload_file_calls: list[dict[str, object]] = []

    def create_repo(self, **kwargs: object) -> None:
        self.create_repo_calls.append(kwargs)

    def repo_info(self, repo_id: str, *, repo_type: str, files_metadata: bool) -> SimpleNamespace:
        assert repo_id == "hakari-bench/leaderboard_database"
        assert repo_type == "dataset"
        assert files_metadata is True
        siblings = []
        if self.remote_size is not None:
            siblings.append(SimpleNamespace(rfilename=DEFAULT_DUCKDB_PATH_IN_REPO, size=self.remote_size, lfs=None))
        return SimpleNamespace(siblings=siblings)

    def upload_file(self, **kwargs: object) -> str:
        self.upload_file_calls.append(kwargs)
        return "https://huggingface.co/datasets/hakari-bench/leaderboard_database/commit/example"


def test_assert_size_within_limit_allows_less_than_twenty_percent_growth() -> None:
    assert_size_within_limit(
        local_size=119,
        remote_size=100,
        max_size_increase_ratio=0.20,
        path_in_repo=DEFAULT_DUCKDB_PATH_IN_REPO,
    )


def test_assert_size_within_limit_rejects_twenty_percent_growth() -> None:
    with pytest.raises(DuckDbSizeIncreaseError, match="Refusing to upload"):
        assert_size_within_limit(
            local_size=120,
            remote_size=100,
            max_size_increase_ratio=0.20,
            path_in_repo=DEFAULT_DUCKDB_PATH_IN_REPO,
        )


def test_remote_duckdb_file_reads_lfs_size_when_direct_size_is_missing() -> None:
    api = SimpleNamespace(
        repo_info=lambda repo_id, *, repo_type, files_metadata: SimpleNamespace(
            siblings=[
                SimpleNamespace(
                    rfilename=DEFAULT_DUCKDB_PATH_IN_REPO,
                    size=None,
                    lfs=SimpleNamespace(size=123),
                )
            ]
        )
    )

    remote_file = remote_duckdb_file(
        api=api,
        repo_id="hakari-bench/leaderboard_database",
        repo_type="dataset",
        path_in_repo=DEFAULT_DUCKDB_PATH_IN_REPO,
    )

    assert remote_file is not None
    assert remote_file.size == 123


def test_upload_leaderboard_duckdb_stops_before_upload_when_growth_is_too_large(tmp_path: Path) -> None:
    duckdb_path = tmp_path / "hakari_bench.duckdb"
    duckdb_path.write_bytes(b"0" * 120)
    api = FakeHfApi(remote_size=100)

    with pytest.raises(DuckDbSizeIncreaseError):
        upload_leaderboard_duckdb(api=api, duckdb_path=duckdb_path)

    assert api.create_repo_calls
    assert api.upload_file_calls == []


def test_upload_leaderboard_duckdb_uploads_when_growth_is_within_limit(tmp_path: Path) -> None:
    duckdb_path = tmp_path / "hakari_bench.duckdb"
    duckdb_path.write_bytes(b"0" * 119)
    api = FakeHfApi(remote_size=100)

    info = upload_leaderboard_duckdb(api=api, duckdb_path=duckdb_path)

    assert info.endswith("/commit/example")
    assert api.upload_file_calls == [
        {
            "repo_id": "hakari-bench/leaderboard_database",
            "repo_type": "dataset",
            "path_or_fileobj": str(duckdb_path),
            "path_in_repo": DEFAULT_DUCKDB_PATH_IN_REPO,
            "commit_message": "Update leaderboard DuckDB",
        }
    ]


def test_upload_leaderboard_duckdb_can_override_large_growth(tmp_path: Path) -> None:
    duckdb_path = tmp_path / "hakari_bench.duckdb"
    duckdb_path.write_bytes(b"0" * 121)
    api = FakeHfApi(remote_size=100)

    upload_leaderboard_duckdb(api=api, duckdb_path=duckdb_path, allow_large_size_increase=True)

    assert len(api.upload_file_calls) == 1
