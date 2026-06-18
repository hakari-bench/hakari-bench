from __future__ import annotations

import argparse
import csv
import importlib
import json
from dataclasses import dataclass
from datetime import UTC, datetime
from pathlib import Path
from statistics import mean, median
from typing import Any

from hakari_bench.datasets import DatasetRegistry, EvalTask, parse_csv_values, resolve_eval_tasks


OPENAI_EMBEDDING_MODELS = ("text-embedding-3-small", "text-embedding-3-large")
OPENAI_EMBEDDING_PRICES_USD_PER_1M_TOKENS = {
    "text-embedding-3-small": 0.02,
    "text-embedding-3-large": 0.13,
}
OPENAI_EMBEDDING_MAX_INPUT_TOKENS = 8100
OPENAI_EMBEDDING_DOC_URL = "https://developers.openai.com/api/docs/guides/embeddings#embedding-models"
TOKEN_COUNT_COLUMN = "_hakari_openai_embedding_token_count"
TEXT_COLUMN = "text"

_PROCESS_ENCODINGS: dict[str, Any] = {}


@dataclass(frozen=True)
class TokenStats:
    count: int
    total_tokens: int
    min_tokens: int
    max_tokens: int
    mean_tokens: float
    median_tokens: float
    over_max_input_count: int


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Estimate OpenAI embedding v3 token counts and API costs for Nano-set datasets."
    )
    parser.add_argument("--config-root", type=Path, default=Path("config"))
    parser.add_argument("--dataset", action="append", default=[], help="Dataset name/id. Repeat or comma-separate.")
    parser.add_argument("--collection", action="append", default=[], help="Collection name. Repeat or comma-separate.")
    parser.add_argument("--split", action="append", default=[], help="Optional split/task. Repeat or comma-separate.")
    parser.add_argument("--dataset-revision", default=None)
    parser.add_argument("--evaluation-scope", choices=("standard", "all"), default="standard")
    parser.add_argument("--num-proc", type=int, default=4)
    parser.add_argument("--batch-size", type=int, default=1000)
    parser.add_argument("--output-dir", type=Path, default=Path("output/openai_embedding_costs"))
    parser.add_argument("--price-small", type=float, default=OPENAI_EMBEDDING_PRICES_USD_PER_1M_TOKENS["text-embedding-3-small"])
    parser.add_argument("--price-large", type=float, default=OPENAI_EMBEDDING_PRICES_USD_PER_1M_TOKENS["text-embedding-3-large"])
    parser.add_argument(
        "--no-load-from-cache-file",
        action="store_true",
        help="Force datasets.map() to recompute token counts instead of using the Hugging Face cache.",
    )
    args = parser.parse_args()

    prices = {
        "text-embedding-3-small": args.price_small,
        "text-embedding-3-large": args.price_large,
    }
    registry = DatasetRegistry.load_from_root(args.config_root)
    datasets = parse_csv_values(args.dataset)
    collections = parse_csv_values(args.collection)
    if not datasets and not collections:
        datasets = registry.dataset_names()

    tasks = resolve_eval_tasks(
        registry=registry,
        dataset_values=datasets,
        collection_values=collections,
        split_values=parse_csv_values(args.split),
        evaluation_scope=args.evaluation_scope,
    )
    rows = estimate_task_costs(
        tasks,
        dataset_revision=args.dataset_revision,
        num_proc=args.num_proc,
        batch_size=args.batch_size,
        load_from_cache_file=not args.no_load_from_cache_file,
        prices_usd_per_1m=prices,
    )
    dataset_rows = aggregate_dataset_rows(rows, prices_usd_per_1m=prices)
    payload = build_payload(
        task_rows=rows,
        dataset_rows=dataset_rows,
        prices_usd_per_1m=prices,
        dataset_revision=args.dataset_revision,
        evaluation_scope=args.evaluation_scope,
    )

    args.output_dir.mkdir(parents=True, exist_ok=True)
    prefix = f"openai_embedding_nanoset_costs_{datetime.now(UTC).strftime('%Y%m%d_%H%M%S')}"
    json_path = args.output_dir / f"{prefix}.json"
    task_csv_path = args.output_dir / f"{prefix}_tasks.csv"
    dataset_csv_path = args.output_dir / f"{prefix}_datasets.csv"
    json_path.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    write_csv(task_csv_path, rows)
    write_csv(dataset_csv_path, dataset_rows)

    total = payload["totals"]
    print(f"wrote JSON: {json_path}")
    print(f"wrote task CSV: {task_csv_path}")
    print(f"wrote dataset CSV: {dataset_csv_path}")
    print(
        "total tokens={total_tokens:,} small=${small:.4f} large=${large:.4f}".format(
            total_tokens=total["total_tokens"],
            small=total["text-embedding-3-small_cost_usd"],
            large=total["text-embedding-3-large_cost_usd"],
        )
    )
    print("top Nano-sets by text-embedding-3-large cost:")
    for row in sorted(dataset_rows, key=lambda item: item["text-embedding-3-large_cost_usd"], reverse=True)[:10]:
        print(
            "  {dataset_name}: {total_tokens:,} tokens, small=${small:.4f}, large=${large:.4f}".format(
                dataset_name=row["dataset_name"],
                total_tokens=row["total_tokens"],
                small=row["text-embedding-3-small_cost_usd"],
                large=row["text-embedding-3-large_cost_usd"],
            )
        )


def estimate_task_costs(
    tasks: list[EvalTask],
    *,
    dataset_revision: str | None,
    num_proc: int,
    batch_size: int,
    load_from_cache_file: bool,
    prices_usd_per_1m: dict[str, float],
) -> list[dict[str, Any]]:
    from datasets import load_dataset

    rows: list[dict[str, Any]] = []
    encoding_name = _encoding_for_model("text-embedding-3-small").name
    for index, task in enumerate(tasks, start=1):
        print(f"[{index}/{len(tasks)}] loading {task.dataset_name}/{task.task_name}", flush=True)
        queries = load_dataset(
            task.dataset_id,
            task.dataset.queries_config,
            split=task.split_name,
            revision=dataset_revision,
        )
        corpus = load_dataset(
            task.dataset_id,
            task.dataset.corpus_config,
            split=task.split_name,
            revision=dataset_revision,
        )
        query_stats = count_text_tokens(
            queries,
            encoding_name=encoding_name,
            num_proc=num_proc,
            batch_size=batch_size,
            load_from_cache_file=load_from_cache_file,
            desc=f"tokenizing queries {task.dataset_name}/{task.task_name}",
        )
        document_stats = count_text_tokens(
            corpus,
            encoding_name=encoding_name,
            num_proc=num_proc,
            batch_size=batch_size,
            load_from_cache_file=load_from_cache_file,
            desc=f"tokenizing corpus {task.dataset_name}/{task.task_name}",
        )
        total_tokens = query_stats.total_tokens + document_stats.total_tokens
        row: dict[str, Any] = {
            "dataset_name": task.dataset_name,
            "dataset_id": task.dataset_id,
            "split_name": task.split_name,
            "task_name": task.task_name,
            "query_count": query_stats.count,
            "query_tokens": query_stats.total_tokens,
            "query_min_tokens": query_stats.min_tokens,
            "query_max_tokens": query_stats.max_tokens,
            "query_mean_tokens": query_stats.mean_tokens,
            "query_median_tokens": query_stats.median_tokens,
            "query_over_max_input_count": query_stats.over_max_input_count,
            "document_count": document_stats.count,
            "document_tokens": document_stats.total_tokens,
            "document_min_tokens": document_stats.min_tokens,
            "document_max_tokens": document_stats.max_tokens,
            "document_mean_tokens": document_stats.mean_tokens,
            "document_median_tokens": document_stats.median_tokens,
            "document_over_max_input_count": document_stats.over_max_input_count,
            "total_tokens": total_tokens,
        }
        row.update(cost_columns(total_tokens, prices_usd_per_1m=prices_usd_per_1m))
        rows.append(row)
    return rows


def count_text_tokens(
    dataset: Any,
    *,
    encoding_name: str,
    num_proc: int,
    batch_size: int,
    load_from_cache_file: bool,
    desc: str,
) -> TokenStats:
    tokenized = dataset.map(
        _token_count_batch,
        batched=True,
        batch_size=batch_size,
        num_proc=max(1, num_proc),
        fn_kwargs={"encoding_name": encoding_name, "text_column": TEXT_COLUMN},
        load_from_cache_file=load_from_cache_file,
        desc=desc,
    )
    return token_stats_from_counts([int(value) for value in tokenized[TOKEN_COUNT_COLUMN]])


def token_stats_from_counts(counts: list[int]) -> TokenStats:
    if not counts:
        return TokenStats(
            count=0,
            total_tokens=0,
            min_tokens=0,
            max_tokens=0,
            mean_tokens=0.0,
            median_tokens=0.0,
            over_max_input_count=0,
        )
    return TokenStats(
        count=len(counts),
        total_tokens=sum(counts),
        min_tokens=min(counts),
        max_tokens=max(counts),
        mean_tokens=float(mean(counts)),
        median_tokens=float(median(counts)),
        over_max_input_count=sum(1 for count in counts if count > OPENAI_EMBEDDING_MAX_INPUT_TOKENS),
    )


def aggregate_dataset_rows(
    task_rows: list[dict[str, Any]],
    *,
    prices_usd_per_1m: dict[str, float],
) -> list[dict[str, Any]]:
    grouped: dict[tuple[str, str], dict[str, Any]] = {}
    for row in task_rows:
        key = (str(row["dataset_name"]), str(row["dataset_id"]))
        target = grouped.setdefault(
            key,
            {
                "dataset_name": row["dataset_name"],
                "dataset_id": row["dataset_id"],
                "task_count": 0,
                "query_count": 0,
                "query_tokens": 0,
                "query_over_max_input_count": 0,
                "document_count": 0,
                "document_tokens": 0,
                "document_over_max_input_count": 0,
                "total_tokens": 0,
            },
        )
        for column in (
            "task_count",
            "query_count",
            "query_tokens",
            "query_over_max_input_count",
            "document_count",
            "document_tokens",
            "document_over_max_input_count",
            "total_tokens",
        ):
            target[column] += 1 if column == "task_count" else int(row[column])
    rows = list(grouped.values())
    for row in rows:
        row.update(cost_columns(int(row["total_tokens"]), prices_usd_per_1m=prices_usd_per_1m))
    return sorted(rows, key=lambda item: str(item["dataset_name"]).lower())


def build_payload(
    *,
    task_rows: list[dict[str, Any]],
    dataset_rows: list[dict[str, Any]],
    prices_usd_per_1m: dict[str, float],
    dataset_revision: str | None,
    evaluation_scope: str,
) -> dict[str, Any]:
    total_tokens = sum(int(row["total_tokens"]) for row in task_rows)
    totals: dict[str, Any] = {"total_tokens": total_tokens}
    totals.update(cost_columns(total_tokens, prices_usd_per_1m=prices_usd_per_1m))
    return {
        "created_at": datetime.now(UTC).isoformat(),
        "assumptions": {
            "models": list(OPENAI_EMBEDDING_MODELS),
            "tokenizer_model": "text-embedding-3-small",
            "tokenizer_encoding": _encoding_for_model("text-embedding-3-small").name,
            "max_input_tokens": OPENAI_EMBEDDING_MAX_INPUT_TOKENS,
            "prices_usd_per_1m_tokens": dict(prices_usd_per_1m),
            "pricing_source": OPENAI_EMBEDDING_DOC_URL,
            "cost_scope": "one embedding pass over every selected Nano-set query and corpus document",
            "dataset_revision": dataset_revision,
            "evaluation_scope": evaluation_scope,
        },
        "totals": totals,
        "datasets": dataset_rows,
        "tasks": task_rows,
    }


def cost_columns(total_tokens: int, *, prices_usd_per_1m: dict[str, float]) -> dict[str, float]:
    return {
        f"{model}_cost_usd": embedding_cost_usd(total_tokens, price_usd_per_1m_tokens=price)
        for model, price in prices_usd_per_1m.items()
    }


def embedding_cost_usd(total_tokens: int, *, price_usd_per_1m_tokens: float) -> float:
    return round((total_tokens / 1_000_000) * price_usd_per_1m_tokens, 12)


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    if not rows:
        path.write_text("", encoding="utf-8")
        return
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)


def _token_count_batch(batch: dict[str, list[Any]], *, encoding_name: str, text_column: str) -> dict[str, list[int]]:
    encoding = _get_process_encoding(encoding_name)
    values = batch[text_column]
    return {TOKEN_COUNT_COLUMN: [len(encoding.encode(str(value or ""), disallowed_special=())) for value in values]}


def _get_process_encoding(encoding_name: str) -> Any:
    encoding = _PROCESS_ENCODINGS.get(encoding_name)
    if encoding is None:
        encoding = _tiktoken().get_encoding(encoding_name)
        _PROCESS_ENCODINGS[encoding_name] = encoding
    return encoding


def _encoding_for_model(model_name: str) -> Any:
    return _tiktoken().encoding_for_model(model_name)


def _tiktoken() -> Any:
    try:
        return importlib.import_module("tiktoken")
    except ModuleNotFoundError as exc:
        raise ModuleNotFoundError(
            "tiktoken is required for OpenAI embedding token counting. "
            "Run this script with `uv run --group openai ...`."
        ) from exc


if __name__ == "__main__":
    main()
