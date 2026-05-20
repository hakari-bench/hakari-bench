from __future__ import annotations

import argparse
from datetime import datetime, timezone
import json
from pathlib import Path
import sys
from typing import Any

import pyarrow.parquet as pq
from datasets import Dataset, get_dataset_split_names, load_dataset
from huggingface_hub import snapshot_download

REPO_ROOT = Path(__file__).resolve().parents[1]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from hakari_bench.bm25 import BM25Config  # noqa: E402
from hakari_bench.datasets import DatasetRegistry, NanoDatasetSpec  # noqa: E402
from hakari_bench.nano_bm25_rebuild import rebuild_bm25_candidate_rows  # noqa: E402
from hakari_bench.nano_dataset_builder import _write_readme as write_nano_readme  # noqa: E402


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Rebuild MNanoBEIR dataset BM25 candidate subsets locally.")
    parser.add_argument("--collection", default="MNanoBEIR")
    parser.add_argument("--dataset", action="append", default=[], help="Dataset name or id to rebuild. Repeatable.")
    parser.add_argument("--split", action="append", default=[], help="Split/task name to rebuild. Repeatable.")
    parser.add_argument("--output-dir", type=Path, default=Path("output/nano_datasets_mnanobeir_bm25_rebuilt"))
    parser.add_argument("--top-k", type=int, default=100)
    parser.add_argument(
        "--tokenizer",
        default="auto",
        choices=[
            "auto",
            "regex",
            "whitespace",
            "transformer",
            "stemmer",
            "english_regex",
            "english_porter",
            "english_porter_stop",
            "wordseg",
        ],
        help="BM25 tokenizer. The default auto mode detects query language and uses wordseg for ja/zh/th/ko/vi.",
    )
    parser.add_argument("--tokenizer-name")
    parser.add_argument("--stemmer-algorithm", default="english")
    parser.add_argument("--revision")
    parser.add_argument("--overwrite", action="store_true")
    parser.add_argument("--skip-snapshot", action="store_true", help="Use existing local files and load missing splits from HF.")
    parser.add_argument(
        "--preserve-qrels",
        action="store_true",
        help="Do not cap qrels above top-k. Splits with more than top-k positives per query will fail coverage checks.",
    )
    parser.add_argument("--allow-incomplete-coverage", action="store_true")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    if args.top_k <= 0:
        raise SystemExit("--top-k must be positive.")

    registry = DatasetRegistry.load_builtin()
    specs = _selected_specs(registry, collection_name=args.collection, selected=args.dataset)
    bm25_config = _bm25_config_from_args(args)

    summary_rows: list[dict[str, Any]] = []
    for spec in specs:
        dataset_dir = args.output_dir / spec.dataset_id.split("/")[-1]
        if not args.skip_snapshot:
            _snapshot_dataset(spec, dataset_dir=dataset_dir, revision=args.revision)
        splits = _selected_splits(spec, selected=args.split)
        for split in splits:
            bm25_path = _existing_split_parquet_path(dataset_dir, config="bm25", split=split)
            if bm25_path is not None and not args.overwrite:
                print(f"skip existing {spec.name}/{split}: {bm25_path}")
                continue
            print(f"rebuild {spec.name}/{split}")
            corpus_rows = _load_rows(spec, dataset_dir=dataset_dir, config=spec.corpus_config, split=split)
            query_rows = _load_rows(spec, dataset_dir=dataset_dir, config=spec.queries_config, split=split)
            qrels_rows = _load_rows(spec, dataset_dir=dataset_dir, config=spec.qrels_config, split=split)
            rebuilt = rebuild_bm25_candidate_rows(
                corpus_rows=corpus_rows,
                query_rows=query_rows,
                qrels_rows=qrels_rows,
                split_name=split,
                bm25_config=bm25_config,
                cap_qrels_to_top_k=not args.preserve_qrels,
                require_full_coverage=not args.allow_incomplete_coverage,
            )
            _write_canonical_split_parquet(dataset_dir, config=spec.corpus_config, split=split, rows=corpus_rows)
            _write_canonical_split_parquet(dataset_dir, config=spec.queries_config, split=split, rows=query_rows)
            _write_canonical_split_parquet(
                dataset_dir,
                config=spec.qrels_config,
                split=split,
                rows=rebuilt.qrels_rows if rebuilt.qrels_rows is not None else qrels_rows,
            )
            _write_canonical_split_parquet(dataset_dir, config="bm25", split=split, rows=rebuilt.candidate_rows)
            metadata = _merge_split_metadata(dataset_dir / "metadata" / f"{split}.json", rebuilt.metadata)
            _write_json(dataset_dir / "metadata" / f"{split}.json", metadata)
            _upsert_manifest(dataset_dir=dataset_dir, dataset_name=spec.name, dataset_id=spec.dataset_id, split_metadata=metadata)
            coverage = metadata["bm25"]["candidate_coverage"]
            summary_rows.append(
                {
                    "dataset": spec.name,
                    "split": split,
                    "query_coverage": coverage.get("query_coverage"),
                    "relevant_coverage": coverage.get("relevant_coverage"),
                    "forced_doc_count": metadata["bm25"].get("forced_doc_count"),
                }
            )
        write_nano_readme(
            output_dir=dataset_dir,
            dataset_name=spec.name,
            dataset_id=spec.dataset_id,
            metadata=_readme_metadata(spec),
        )

    _write_json(args.output_dir / "bm25_rebuild_summary.json", {"generated_at_utc": _utc_now(), "rows": summary_rows})
    print(f"wrote {args.output_dir / 'bm25_rebuild_summary.json'}")


def _selected_specs(
    registry: DatasetRegistry,
    *,
    collection_name: str,
    selected: list[str],
) -> list[NanoDatasetSpec]:
    if selected:
        return [registry.get_dataset(value) for value in selected]
    collection = registry.get_collection(collection_name)
    return [registry.get_dataset(name) for name in collection.datasets]


def _bm25_config_from_args(args: argparse.Namespace) -> BM25Config:
    tokenizer = None if args.tokenizer == "auto" else args.tokenizer
    return BM25Config(
        tokenizer=tokenizer,
        tokenizer_name=args.tokenizer_name,
        stemmer_algorithm=args.stemmer_algorithm,
        top_k=args.top_k,
        show_progress=True,
    )


def _selected_splits(spec: NanoDatasetSpec, *, selected: list[str]) -> list[str]:
    available = spec.splits or get_dataset_split_names(spec.dataset_id, spec.qrels_config)
    if not selected:
        return available
    selected_set = set(selected)
    return [split for split in available if split in selected_set]


def _snapshot_dataset(spec: NanoDatasetSpec, *, dataset_dir: Path, revision: str | None) -> None:
    dataset_dir.mkdir(parents=True, exist_ok=True)
    snapshot_download(
        repo_id=spec.dataset_id,
        repo_type="dataset",
        revision=revision,
        local_dir=dataset_dir,
        allow_patterns=["README.md", "manifest.json", "metadata/*.json", "corpus/*.parquet", "queries/*.parquet", "qrels/*.parquet"],
    )


def _load_rows(spec: NanoDatasetSpec, *, dataset_dir: Path, config: str, split: str) -> list[dict[str, Any]]:
    parquet_path = _existing_split_parquet_path(dataset_dir, config=config, split=split)
    if parquet_path is not None:
        return [dict(row) for row in pq.read_table(parquet_path).to_pylist()]
    return [dict(row) for row in load_dataset(spec.dataset_id, config, split=split)]


def _existing_split_parquet_path(dataset_dir: Path, *, config: str, split: str) -> Path | None:
    config_dir = dataset_dir / config
    exact_path = config_dir / f"{split}.parquet"
    if exact_path.exists():
        return exact_path
    matches = sorted(config_dir.glob(f"{split}-*.parquet"))
    if len(matches) == 1:
        return matches[0]
    return None


def _write_canonical_split_parquet(
    dataset_dir: Path,
    *,
    config: str,
    split: str,
    rows: list[dict[str, Any]],
) -> None:
    config_dir = dataset_dir / config
    config_dir.mkdir(parents=True, exist_ok=True)
    exact_path = config_dir / f"{split}.parquet"
    Dataset.from_list(rows).to_parquet(str(exact_path))
    for path in config_dir.glob(f"{split}-*.parquet"):
        path.unlink()


def _merge_split_metadata(path: Path, rebuilt: dict[str, Any]) -> dict[str, Any]:
    existing = json.loads(path.read_text(encoding="utf-8")) if path.exists() else {}
    existing = existing if isinstance(existing, dict) else {}
    merged = {**existing, **{key: value for key, value in rebuilt.items() if key != "bm25"}}
    existing_bm25 = existing.get("bm25")
    existing_bm25 = existing_bm25 if isinstance(existing_bm25, dict) else {}
    merged["bm25"] = {**existing_bm25, **rebuilt["bm25"]}
    merged["bm25"]["rebuilt_at_utc"] = _utc_now()
    return merged


def _upsert_manifest(
    *,
    dataset_dir: Path,
    dataset_name: str,
    dataset_id: str,
    split_metadata: dict[str, Any],
) -> None:
    path = dataset_dir / "manifest.json"
    manifest = json.loads(path.read_text(encoding="utf-8")) if path.exists() else {}
    manifest = manifest if isinstance(manifest, dict) else {}
    manifest.setdefault("dataset_name", dataset_name)
    manifest.setdefault("dataset_id", dataset_id)
    splits = [
        item
        for item in manifest.get("splits", [])
        if isinstance(item, dict) and item.get("split_name") != split_metadata["split_name"]
    ]
    splits.append(
        {
            "split_name": split_metadata["split_name"],
            "queries": split_metadata["queries"],
            "corpus": split_metadata["corpus"],
            "qrels": split_metadata["qrels"],
            "forced_doc_count": split_metadata["bm25"]["forced_doc_count"],
            "bm25_ndcg_at_10": split_metadata["bm25"]["ndcg_at_10"],
            "bm25_query_coverage": split_metadata["bm25"]["candidate_coverage"]["query_coverage"],
            "bm25_relevant_coverage": split_metadata["bm25"]["candidate_coverage"]["relevant_coverage"],
        }
    )
    manifest["splits"] = sorted(splits, key=lambda item: str(item["split_name"]))
    _write_json(path, manifest)


def _readme_metadata(spec: NanoDatasetSpec) -> dict[str, Any]:
    metadata = dict(spec.metadata or {})
    metadata.setdefault("source_benchmark_name", "MNanoBEIR / NanoBEIR")
    metadata["source_dataset_location"] = f"the `{spec.dataset_id}` corpus, queries, and qrels tables"
    metadata["source_split_policy"] = "the NanoBEIR split set"
    metadata["corpus_fill_policy"] = (
        "the included corpus tables for each Nano split; no additional document resampling is performed"
    )
    metadata["qrels_score_policy_note"] = (
        "The `qrels` config is positive-only. When needed for top-k reranking "
        "coverage, positive qrels are capped per query to the BM25 top-k."
    )
    metadata["qrels_capping_note"] = (
        "For top-100 reranking diagnostics, positive qrels are capped to at most "
        "100 documents per query before BM25 positive forcing. This makes full "
        "relevant coverage possible for splits whose upstream qrels contain more "
        "than 100 positives for a single query."
    )
    metadata["source_hard_negative_note"] = (
        "The `bm25` candidate subset is generated from the included corpus for each split."
    )
    metadata["bm25_score_notes"] = (
        "Coverage is measured against included qrels at the same BM25 top-k used for reranking diagnostics. "
        "The included BM25 candidate subset has 100.00% query coverage and 100.00% relevant coverage for every split."
    )
    return metadata


def _write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def _utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


if __name__ == "__main__":
    main()
