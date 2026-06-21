from __future__ import annotations

import argparse
import os
import sys
from collections.abc import Sequence
from pathlib import Path

from huggingface_hub import HfApi

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from hakari_bench.viewer.store import DEFAULT_REMOTE_LATEST_DUCKDB_PATH, REMOTE_LATEST_DUCKDB_PATH_ENV
from scripts.generate_results_pr_template import generate_pr_template


def build_arg_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description=(
            "Generate a HAKARI-Bench results PR body and optionally update an "
            "existing Hugging Face Dataset PR comment."
        ),
    )
    parser.add_argument(
        "result_dir",
        type=Path,
        help="Model result directory containing .json/.json.gz/.json.xz result files.",
    )
    parser.add_argument(
        "--repo-path",
        help="Final path in hakari-bench/results, e.g. hakari-results/org__model.",
    )
    parser.add_argument(
        "--config-dir",
        type=Path,
        default=Path("config/viewer"),
        help="Viewer config directory used for Overall grouping.",
    )
    parser.add_argument(
        "--comparison-duckdb-path",
        type=Path,
        help=(
            "DuckDB path used to add the Nano-set comparison table. Defaults to "
            f"${REMOTE_LATEST_DUCKDB_PATH_ENV} or {DEFAULT_REMOTE_LATEST_DUCKDB_PATH} when that file exists."
        ),
    )
    parser.add_argument(
        "--comparison-model",
        action="append",
        dest="comparison_models",
        help=(
            "Model id to include in the DuckDB comparison table. Can be repeated. "
            "Defaults are defined by generate_results_pr_template.py."
        ),
    )
    parser.add_argument(
        "-o",
        "--output",
        type=Path,
        help="Write the generated body to this path.",
    )
    parser.add_argument(
        "--discussion-num",
        type=int,
        help="Existing Hugging Face Dataset PR discussion number to update.",
    )
    parser.add_argument(
        "--repo-id",
        default="hakari-bench/results",
        help="Hugging Face repository id for --discussion-num.",
    )
    parser.add_argument(
        "--repo-type",
        default="dataset",
        help="Hugging Face repository type for --discussion-num.",
    )
    parser.add_argument(
        "--comment-id",
        help="Specific discussion comment id to edit. Defaults to the first comment event.",
    )
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    args = build_arg_parser().parse_args(argv)
    body = generate_pr_template(
        result_dir=args.result_dir,
        config_dir=args.config_dir,
        repo_path=args.repo_path,
        comparison_duckdb_path=args.comparison_duckdb_path or _default_comparison_duckdb_path(),
        comparison_models=args.comparison_models,
    )
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(body, encoding="utf-8")
    if args.discussion_num is not None:
        _update_discussion_comment(
            body,
            repo_id=args.repo_id,
            repo_type=args.repo_type,
            discussion_num=args.discussion_num,
            comment_id=args.comment_id,
        )
    if not args.output and args.discussion_num is None:
        print(body)
    return 0


def _update_discussion_comment(
    body: str,
    *,
    repo_id: str,
    repo_type: str,
    discussion_num: int,
    comment_id: str | None,
) -> None:
    api = HfApi()
    if comment_id is None:
        discussion = api.get_discussion_details(
            repo_id=repo_id,
            repo_type=repo_type,
            discussion_num=discussion_num,
        )
        comment_id = _first_comment_id(discussion.events)
    api.edit_discussion_comment(
        repo_id=repo_id,
        repo_type=repo_type,
        discussion_num=discussion_num,
        comment_id=comment_id,
        new_content=body,
    )


def _first_comment_id(events: Sequence[object]) -> str:
    for event in events:
        if getattr(event, "type", None) == "comment":
            return str(getattr(event, "id"))
    raise ValueError("No editable discussion comment was found.")


def _default_comparison_duckdb_path() -> Path | None:
    env_value = os.getenv(REMOTE_LATEST_DUCKDB_PATH_ENV)
    if env_value:
        return Path(env_value).expanduser()
    return DEFAULT_REMOTE_LATEST_DUCKDB_PATH if DEFAULT_REMOTE_LATEST_DUCKDB_PATH.exists() else None


if __name__ == "__main__":
    raise SystemExit(main())
