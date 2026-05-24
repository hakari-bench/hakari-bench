from __future__ import annotations

import argparse
import json
import sys
import time
from pathlib import Path
from typing import Any

from datasets import get_dataset_split_names
from sentence_transformers import SentenceTransformer

from hakari_bench.datasets import DatasetRegistry

sys.path.append(str(Path(__file__).resolve().parent))
from build_reranking_hybrid_nano_dataset import HARRIER_MODEL_ID, build_dataset  # noqa: E402


def main() -> None:
    args = parse_args()
    assignments = assigned_datasets(args)
    args.output_root.mkdir(parents=True, exist_ok=True)
    log_path = args.output_root / f"worker_{args.worker_index}_status.jsonl"

    model = SentenceTransformer(args.harrier_model, device=args.device)
    print(
        f"worker {args.worker_index}/{args.worker_count}: {len(assignments)} datasets, "
        f"{sum(item['split_count'] for item in assignments)} splits",
        flush=True,
    )

    for item in assignments:
        output_dir = args.output_root / item["name"]
        metadata_path = output_dir / "reranking_hybrid_metadata.json"
        if metadata_path.exists() and not args.overwrite:
            print(f"skip existing {item['name']}", flush=True)
            write_status(log_path, item, status="skipped_existing")
            continue
        started = time.perf_counter()
        print(f"start {item['name']} splits={item['split_count']} dataset={item['dataset_id']}", flush=True)
        try:
            metadata = build_dataset(
                source_dataset=item["dataset_id"],
                output_dir=output_dir,
                splits=None,
                harrier_model=args.harrier_model,
                model=model,
                device=args.device,
                batch_size=args.batch_size,
                dense_score_batch_size=args.dense_score_batch_size,
                bm25_top_k=args.bm25_top_k,
                dense_top_k=args.dense_top_k,
                hybrid_top_k=args.hybrid_top_k,
                rrf_k=args.rrf_k,
                seed=args.seed,
                overwrite=args.overwrite,
                show_progress=args.show_progress,
            )
            write_status(
                log_path,
                item,
                status="completed",
                seconds=time.perf_counter() - started,
                forced_positive_count=sum(
                    split[args.hybrid_config_name]["forced_positive_count"]
                    for split in metadata["splits"].values()
                ),
                random_filler_count=sum(
                    split[args.hybrid_config_name]["random_filler_count"]
                    for split in metadata["splits"].values()
                ),
            )
            print(f"done {item['name']} seconds={time.perf_counter() - started:.1f}", flush=True)
        except Exception as exc:
            write_status(
                log_path,
                item,
                status="failed",
                seconds=time.perf_counter() - started,
                error=f"{type(exc).__name__}: {exc}",
            )
            print(f"failed {item['name']}: {type(exc).__name__}: {exc}", flush=True)
            if not args.keep_going:
                raise


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Build all local Nano reranking_hybrid datasets.")
    parser.add_argument("--output-root", type=Path, default=Path("output/nano_reranking_hybrid"))
    parser.add_argument("--harrier-model", default=HARRIER_MODEL_ID)
    parser.add_argument("--device", default="cuda:0")
    parser.add_argument("--batch-size", type=int, default=4)
    parser.add_argument("--dense-score-batch-size", type=int, default=64)
    parser.add_argument("--bm25-top-k", type=int, default=100)
    parser.add_argument("--dense-top-k", type=int, default=100)
    parser.add_argument("--hybrid-top-k", type=int, default=101)
    parser.add_argument("--rrf-k", type=int, default=60)
    parser.add_argument("--seed", type=int, default=20260524)
    parser.add_argument("--worker-index", type=int, default=0)
    parser.add_argument("--worker-count", type=int, default=1)
    parser.add_argument("--include-existing", action="store_true")
    parser.add_argument("--overwrite", action="store_true")
    parser.add_argument("--keep-going", action="store_true")
    parser.add_argument("--show-progress", action="store_true")
    parser.add_argument("--hybrid-config-name", default="reranking_hybrid")
    return parser.parse_args()


def assigned_datasets(args: argparse.Namespace) -> list[dict[str, Any]]:
    if args.worker_index < 0 or args.worker_index >= args.worker_count:
        raise ValueError("--worker-index must be in [0, --worker-count).")
    registry = DatasetRegistry.load_builtin()
    items: list[dict[str, Any]] = []
    for name in registry.dataset_names():
        spec = registry.get_dataset(name)
        if not spec.name.startswith("Nano"):
            continue
        output_dir = args.output_root / spec.name
        if not args.include_existing and (output_dir / "reranking_hybrid_metadata.json").exists():
            continue
        split_count = len(get_dataset_split_names(spec.dataset_id, "queries"))
        items.append({"name": spec.name, "dataset_id": spec.dataset_id, "split_count": split_count})

    buckets: list[list[dict[str, Any]]] = [[] for _ in range(args.worker_count)]
    bucket_splits = [0 for _ in range(args.worker_count)]
    for item in sorted(items, key=lambda value: (-int(value["split_count"]), str(value["name"]))):
        bucket_index = min(range(args.worker_count), key=lambda index: bucket_splits[index])
        buckets[bucket_index].append(item)
        bucket_splits[bucket_index] += int(item["split_count"])
    return sorted(buckets[args.worker_index], key=lambda value: str(value["name"]))


def write_status(path: Path, item: dict[str, Any], *, status: str, **extra: Any) -> None:
    row = {"dataset": item["name"], "dataset_id": item["dataset_id"], "split_count": item["split_count"], "status": status}
    row.update(extra)
    with path.open("a", encoding="utf-8") as file:
        file.write(json.dumps(row, ensure_ascii=False, sort_keys=True) + "\n")


if __name__ == "__main__":
    main()

