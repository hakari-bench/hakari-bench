from __future__ import annotations

import argparse
import statistics
from collections.abc import Iterable, Mapping, Sequence
from dataclasses import dataclass
from functools import lru_cache
from pathlib import Path
from typing import Any

from hakari_bench.task_docs import (
    CandidateSubsetsMetadata,
    CountMetadata,
    PositivesPerQueryMetadata,
    TaskMetadataDocument,
    TextStatsCharsMetadata,
    collect_task_doc_paths,
    load_task_metadata_document,
    task_metadata_json_path,
)
from update_benchmark_task_candidate_metadata import (
    RERANKING_HYBRID_CONFIG,
    load_candidate_metrics,
    qrels_by_query,
)


@dataclass(frozen=True)
class NanoTaskStatistics:
    counts: CountMetadata
    positives_per_query: PositivesPerQueryMetadata
    text_stats_chars: TextStatsCharsMetadata


def main(argv: Sequence[str] | None = None) -> int:
    args = parse_args(argv)
    paths = collect_task_doc_paths(args.paths, docs_root=args.docs_root)
    changed: list[Path] = []
    metrics_cache: dict[tuple[str, str], dict[str, Any]] = {}

    for doc_path in paths:
        document = load_task_metadata_document(
            doc_path,
            docs_root=args.docs_root,
            metadata_root=args.metadata_root,
        )
        metadata = document.task_metadata
        cache_key = (metadata.dataset_id, metadata.split_name)
        if cache_key not in metrics_cache:
            if not args.quiet:
                print(f"load {metadata.dataset_id} {metadata.split_name}", flush=True)
            metrics_cache[cache_key] = {
                "stats": load_nano_task_statistics(
                    dataset_id=metadata.dataset_id,
                    split_name=metadata.split_name,
                ),
                "metrics": load_candidate_metrics(
                    dataset_id=metadata.dataset_id,
                    split_name=metadata.split_name,
                    reranking_hybrid_config=args.reranking_hybrid_config,
                ),
            }

        stats: NanoTaskStatistics = metrics_cache[cache_key]["stats"]
        metrics = metrics_cache[cache_key]["metrics"]
        updated_metadata = metadata.model_copy(
            update={
                "counts": stats.counts,
                "positives_per_query": stats.positives_per_query,
                "text_stats_chars": stats.text_stats_chars,
                "bm25": metadata.bm25.model_copy(
                    update={
                        "ndcg_at_10": metrics["bm25"].ndcg_at_10,
                        "hit_at_10": metrics["bm25"].hit_at_10,
                        "source": "dataset_candidate_subset",
                    },
                    deep=True,
                ),
                "candidate_subsets": CandidateSubsetsMetadata.model_validate(
                    {name: value.as_yaml() for name, value in metrics.items()}
                ),
            },
            deep=True,
        )
        updated_document = TaskMetadataDocument(task_metadata=updated_metadata)
        output_path = task_metadata_json_path(
            doc_path,
            docs_root=args.docs_root,
            metadata_root=args.metadata_root,
        )
        payload = updated_document.model_dump_json(indent=2, exclude_none=True) + "\n"
        if output_path.exists() and output_path.read_text(encoding="utf-8") == payload:
            continue
        changed.append(output_path)
        if not args.dry_run:
            output_path.parent.mkdir(parents=True, exist_ok=True)
            output_path.write_text(payload, encoding="utf-8")

    for path in changed:
        print(path)
    print(f"changed={len(changed)}")
    return 0


def parse_args(argv: Sequence[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Build external task metadata JSON from Nano dataset tables."
    )
    parser.add_argument("paths", nargs="*", type=Path, help="Optional Markdown task docs or directories.")
    parser.add_argument("--docs-root", type=Path, default=Path("docs/benchmark_tasks"))
    parser.add_argument("--metadata-root", type=Path, default=Path("task_docs/metadata"))
    parser.add_argument("--reranking-hybrid-config", default=RERANKING_HYBRID_CONFIG)
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--quiet", action="store_true")
    return parser.parse_args(argv)


def load_nano_task_statistics(*, dataset_id: str, split_name: str) -> NanoTaskStatistics:
    queries = list(load_dataset_split(dataset_id, "queries", split_name))
    corpus = list(load_dataset_split(dataset_id, "corpus", split_name))
    qrels = qrels_by_query(load_dataset_split(dataset_id, "qrels", split_name))
    positives = [len(qrels[query_id]) for query_id in sorted(qrels)]
    if not positives:
        raise ValueError(f"{dataset_id}/{split_name} has no positive qrels")
    multi_positive = sum(1 for count in positives if count > 1)
    return NanoTaskStatistics(
        counts=CountMetadata(
            queries=len(queries),
            documents=len(corpus),
            positive_qrels=sum(positives),
        ),
        positives_per_query=PositivesPerQueryMetadata(
            average=round(sum(positives) / len(positives), 6),
            min=min(positives),
            median=round(float(statistics.median(positives)), 6),
            max=max(positives),
            multi_positive_queries=multi_positive,
            multi_positive_query_percent=round(100.0 * multi_positive / len(positives), 6),
        ),
        text_stats_chars=TextStatsCharsMetadata(
            query_mean=round(mean_text_chars(queries), 6),
            document_mean=round(mean_text_chars(corpus), 6),
        ),
    )


@lru_cache(maxsize=None)
def load_dataset_config(dataset_id: str, config_name: str) -> Any:
    from datasets import disable_progress_bar, load_dataset

    disable_progress_bar()
    return load_dataset(dataset_id, config_name)


def load_dataset_split(dataset_id: str, config_name: str, split_name: str) -> Any:
    dataset = load_dataset_config(dataset_id, config_name)
    try:
        return dataset[split_name]
    except KeyError as exc:
        available = ", ".join(str(split) for split in getattr(dataset, "keys", lambda: [])())
        raise KeyError(f"{dataset_id}/{config_name} does not contain split {split_name!r}; available: {available}") from exc


def mean_text_chars(rows: Iterable[Mapping[str, Any]]) -> float:
    lengths = [len(row_text(row).strip()) for row in rows]
    return sum(lengths) / len(lengths) if lengths else 0.0


def row_text(row: Mapping[str, Any]) -> str:
    return as_text(
        first_present(
            row,
            (
                "text",
                "query",
                "question",
                "contents",
                "content",
                "document",
                "passage",
                "answer",
            ),
        )
    )


def as_text(value: Any) -> str:
    if value is None:
        return ""
    if isinstance(value, str):
        return value
    return str(value)


def first_present(row: Mapping[str, Any], keys: Sequence[str]) -> Any:
    for key in keys:
        if key in row and row[key] is not None:
            return row[key]
    raise KeyError(f"none of the expected keys are present: {', '.join(keys)}")


if __name__ == "__main__":
    raise SystemExit(main())
