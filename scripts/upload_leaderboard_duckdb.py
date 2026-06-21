from __future__ import annotations

import argparse
from dataclasses import dataclass
from pathlib import Path
from typing import Any


DEFAULT_REPO_ID = "hakari-bench/leaderboard_database"
DEFAULT_REPO_TYPE = "dataset"
DEFAULT_DUCKDB_PATH_IN_REPO = "duckdb/hakari_bench.duckdb"
DEFAULT_COMMIT_MESSAGE = "Update leaderboard DuckDB"
DEFAULT_MAX_SIZE_INCREASE_RATIO = 0.20


class DuckDbSizeIncreaseError(RuntimeError):
    pass


@dataclass(frozen=True)
class RemoteDuckDbFile:
    path: str
    size: int


def build_arg_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Upload the leaderboard DuckDB to Hugging Face with a size guard.")
    parser.add_argument("duckdb_path", type=Path, help="Local DuckDB file to upload.")
    parser.add_argument("--repo-id", default=DEFAULT_REPO_ID, help="Hugging Face dataset repo id.")
    parser.add_argument("--repo-type", default=DEFAULT_REPO_TYPE, help="Hugging Face repo type.")
    parser.add_argument("--path-in-repo", default=DEFAULT_DUCKDB_PATH_IN_REPO, help="Remote path for the DuckDB file.")
    parser.add_argument("--commit-message", default=DEFAULT_COMMIT_MESSAGE)
    parser.add_argument(
        "--max-size-increase-ratio",
        type=float,
        default=DEFAULT_MAX_SIZE_INCREASE_RATIO,
        help="Maximum allowed local size increase over the existing remote file. Default: 0.20.",
    )
    parser.add_argument(
        "--allow-large-size-increase",
        action="store_true",
        help="Upload even when the local DuckDB is more than the configured size increase limit.",
    )
    parser.add_argument("--private", action="store_true", help="Create the repo as private when it does not exist.")
    return parser


def upload_leaderboard_duckdb(
    *,
    api: Any,
    duckdb_path: Path,
    repo_id: str = DEFAULT_REPO_ID,
    repo_type: str = DEFAULT_REPO_TYPE,
    path_in_repo: str = DEFAULT_DUCKDB_PATH_IN_REPO,
    commit_message: str = DEFAULT_COMMIT_MESSAGE,
    max_size_increase_ratio: float = DEFAULT_MAX_SIZE_INCREASE_RATIO,
    allow_large_size_increase: bool = False,
    private: bool = False,
) -> str:
    if max_size_increase_ratio < 0:
        raise ValueError("--max-size-increase-ratio must be non-negative")
    if not duckdb_path.exists():
        raise FileNotFoundError(duckdb_path)
    if not duckdb_path.is_file():
        raise ValueError(f"DuckDB path is not a file: {duckdb_path}")

    local_size = duckdb_path.stat().st_size
    api.create_repo(repo_id=repo_id, repo_type=repo_type, exist_ok=True, private=private)
    remote_file = remote_duckdb_file(api=api, repo_id=repo_id, repo_type=repo_type, path_in_repo=path_in_repo)
    if remote_file is not None:
        print(
            "DuckDB size check: "
            f"local={format_bytes(local_size)} remote={format_bytes(remote_file.size)} "
            f"limit=+{max_size_increase_ratio:.0%}"
        )
        if not allow_large_size_increase:
            assert_size_within_limit(
                local_size=local_size,
                remote_size=remote_file.size,
                max_size_increase_ratio=max_size_increase_ratio,
                path_in_repo=path_in_repo,
            )
    else:
        print(f"DuckDB size check: no existing remote file at {path_in_repo}; upload is not size-gated.")

    info = api.upload_file(
        repo_id=repo_id,
        repo_type=repo_type,
        path_or_fileobj=str(duckdb_path),
        path_in_repo=path_in_repo,
        commit_message=commit_message,
    )
    return str(info)


def remote_duckdb_file(*, api: Any, repo_id: str, repo_type: str, path_in_repo: str) -> RemoteDuckDbFile | None:
    info = api.repo_info(repo_id, repo_type=repo_type, files_metadata=True)
    for sibling in getattr(info, "siblings", ()):
        if getattr(sibling, "rfilename", None) != path_in_repo:
            continue
        size = getattr(sibling, "size", None)
        if size is None:
            lfs = getattr(sibling, "lfs", None)
            size = getattr(lfs, "size", None) if lfs is not None else None
        if not isinstance(size, int):
            raise RuntimeError(f"Remote file size is unavailable for {repo_id}/{path_in_repo}")
        return RemoteDuckDbFile(path=path_in_repo, size=size)
    return None


def assert_size_within_limit(
    *,
    local_size: int,
    remote_size: int,
    max_size_increase_ratio: float,
    path_in_repo: str,
) -> None:
    if remote_size < 0 or local_size < 0:
        raise ValueError("file sizes must be non-negative")
    if local_size <= remote_size:
        return
    increase_ratio = (local_size - remote_size) / remote_size if remote_size > 0 else float("inf")
    if increase_ratio < max_size_increase_ratio:
        return
    raise DuckDbSizeIncreaseError(
        f"Refusing to upload {path_in_repo}: local DuckDB is {format_bytes(local_size)}, "
        f"remote DuckDB is {format_bytes(remote_size)}, increase is {increase_ratio:.1%}, "
        f"which is at or above the allowed {max_size_increase_ratio:.0%}. "
        "Rebuild/check the DuckDB or rerun with --allow-large-size-increase if this growth is expected."
    )


def format_bytes(size: int) -> str:
    units = ("B", "KiB", "MiB", "GiB", "TiB")
    value = float(size)
    for unit in units:
        if value < 1024.0 or unit == units[-1]:
            return f"{value:.1f} {unit}" if unit != "B" else f"{size} B"
        value /= 1024.0
    raise AssertionError("unreachable")


def main(argv: list[str] | None = None) -> int:
    args = build_arg_parser().parse_args(argv)
    from huggingface_hub import HfApi

    info = upload_leaderboard_duckdb(
        api=HfApi(),
        duckdb_path=args.duckdb_path,
        repo_id=args.repo_id,
        repo_type=args.repo_type,
        path_in_repo=args.path_in_repo,
        commit_message=args.commit_message,
        max_size_increase_ratio=args.max_size_increase_ratio,
        allow_large_size_increase=args.allow_large_size_increase,
        private=args.private,
    )
    print(info)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
