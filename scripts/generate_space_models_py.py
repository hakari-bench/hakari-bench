from __future__ import annotations

import argparse
from pathlib import Path
from typing import Iterable


DEFAULT_DUCKDB_PATH = Path.home() / ".cache" / "hakari-bench" / "duckdb" / "remote_latest_hakari_bench.duckdb"
DEFAULT_OUTPUT_PATH = Path("models.py")


def build_arg_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description=(
            "Generate a Hugging Face Space models.py file from the leaderboard DuckDB. "
            "The generated file is not imported by the Space app; Hugging Face statically scans it "
            "to link the Space from the listed model repositories."
        )
    )
    parser.add_argument(
        "--duckdb-path",
        type=Path,
        default=DEFAULT_DUCKDB_PATH,
        help=f"Leaderboard DuckDB path. Default: {DEFAULT_DUCKDB_PATH}",
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=DEFAULT_OUTPUT_PATH,
        help=f"Output models.py path. Default: {DEFAULT_OUTPUT_PATH}",
    )
    parser.add_argument(
        "--no-verify-hub",
        action="store_true",
        help="Do not check that extracted model ids resolve as Hugging Face model repositories.",
    )
    return parser


def extract_hf_model_names(duckdb_path: Path) -> list[str]:
    import duckdb

    if not duckdb_path.exists():
        raise FileNotFoundError(duckdb_path)
    con = duckdb.connect(str(duckdb_path), read_only=True)
    try:
        rows = con.execute(
            """
            select distinct model_name
            from dim_model
            where model_type <> 'bm25'
              and model_name like '%/%'
            order by lower(model_name)
            """
        ).fetchall()
    finally:
        con.close()
    return [model_name for (model_name,) in rows if is_plain_hf_model_id(model_name)]


def is_plain_hf_model_id(model_name: str) -> bool:
    if model_name.count("/") != 1:
        return False
    if any(char.isspace() for char in model_name):
        return False
    if any(char in model_name for char in "()[]{}"):
        return False
    namespace, repo = model_name.split("/", 1)
    return bool(namespace and repo)


def filter_existing_hf_models(model_names: Iterable[str]) -> list[str]:
    from huggingface_hub import HfApi
    from huggingface_hub.utils import HfHubHTTPError, RepositoryNotFoundError

    api = HfApi()
    existing: list[str] = []
    for model_name in model_names:
        try:
            api.model_info(model_name)
        except (RepositoryNotFoundError, HfHubHTTPError):
            continue
        existing.append(model_name)
    return existing


def render_models_py(model_names: Iterable[str]) -> str:
    lines = [
        '"""Auto-generated list of HAKARI-Bench leaderboard Hugging Face models.',
        "",
        "This file is not imported by the Space app. It is kept in the Space repo so",
        "Hugging Face can statically link the Space from the listed model repositories.",
        '"""',
        "",
        "MODEL_NAMES = [",
    ]
    lines.extend(f'    "{model_name}",' for model_name in model_names)
    lines.extend(["]", ""])
    return "\n".join(lines)


def write_models_py(*, duckdb_path: Path, output_path: Path, verify_hub: bool = True) -> list[str]:
    model_names = extract_hf_model_names(duckdb_path)
    if verify_hub:
        model_names = filter_existing_hf_models(model_names)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(render_models_py(model_names), encoding="utf-8")
    return model_names


def main() -> None:
    args = build_arg_parser().parse_args()
    model_names = write_models_py(
        duckdb_path=args.duckdb_path,
        output_path=args.output,
        verify_hub=not args.no_verify_hub,
    )
    print(f"Wrote {len(model_names)} model ids to {args.output}")


if __name__ == "__main__":
    main()
