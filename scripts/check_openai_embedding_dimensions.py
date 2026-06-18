from __future__ import annotations

import argparse
import importlib
import json
import math
import os
from pathlib import Path


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Compare OpenAI embeddings API dimensions output with local full-vector truncation."
    )
    parser.add_argument("--model", default="text-embedding-3-small")
    parser.add_argument("--dimensions", type=int, default=256)
    parser.add_argument("--text", default="HAKARI OpenAI embedding dimension check.")
    parser.add_argument("--dotenv-path", default=".env")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()

    load_dotenv(Path(args.dotenv_path))
    try:
        openai_module = importlib.import_module("openai")
    except ModuleNotFoundError as exc:
        raise ModuleNotFoundError(
            "openai is required for this check. Run it with `uv run --group openai ...`."
        ) from exc
    client = openai_module.OpenAI()

    full = client.embeddings.create(model=args.model, input=args.text).data[0].embedding
    reduced = client.embeddings.create(model=args.model, input=args.text, dimensions=args.dimensions).data[0].embedding
    prefix = full[: args.dimensions]
    prefix_norm = math.sqrt(sum(value * value for value in prefix))
    renormalized_prefix = [value / prefix_norm for value in prefix] if prefix_norm > 0 else prefix

    payload = {
        "model": args.model,
        "dimensions": args.dimensions,
        "full_dim": len(full),
        "api_reduced_dim": len(reduced),
        "full_norm": l2_norm(full),
        "api_reduced_norm": l2_norm(reduced),
        "full_prefix_norm": prefix_norm,
        "max_abs_diff_api_vs_full_prefix": max_abs_diff(reduced, prefix),
        "max_abs_diff_api_vs_renormalized_full_prefix": max_abs_diff(reduced, renormalized_prefix),
        "mean_abs_diff_api_vs_renormalized_full_prefix": mean_abs_diff(reduced, renormalized_prefix),
        "api_matches_full_prefix_exactly": reduced == prefix,
        "api_matches_renormalized_full_prefix_1e_6": max_abs_diff(reduced, renormalized_prefix) <= 1e-6,
    }
    if args.json:
        print(json.dumps(payload, indent=2, sort_keys=True))
        return
    for key, value in payload.items():
        print(f"{key}={value}")


def load_dotenv(path: Path) -> None:
    path = path.expanduser()
    if not path.exists():
        return
    for raw_line in path.read_text(encoding="utf-8").splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#"):
            continue
        if line.startswith("export "):
            line = line[len("export ") :].strip()
        key, separator, value = line.partition("=")
        if not separator:
            continue
        key = key.strip()
        if not key or key in os.environ:
            continue
        value = value.strip()
        if len(value) >= 2 and value[0] == value[-1] and value[0] in {"'", '"'}:
            value = value[1:-1]
        os.environ[key] = value


def l2_norm(values: list[float]) -> float:
    return math.sqrt(sum(value * value for value in values))


def max_abs_diff(left: list[float], right: list[float]) -> float:
    return max(abs(left_value - right_value) for left_value, right_value in zip(left, right, strict=True))


def mean_abs_diff(left: list[float], right: list[float]) -> float:
    diffs = [abs(left_value - right_value) for left_value, right_value in zip(left, right, strict=True)]
    return sum(diffs) / len(diffs)


if __name__ == "__main__":
    main()
