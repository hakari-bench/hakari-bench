from __future__ import annotations

import argparse
import math
import re
from collections.abc import Mapping, Sequence
from dataclasses import dataclass
from functools import lru_cache
from pathlib import Path
from typing import Any

import yaml

from hakari_bench.benchmark_docs import BENCHMARK_TASK_METADATA_RE


TASK_METADATA_RE = BENCHMARK_TASK_METADATA_RE
GROUP_METADATA_RE = re.compile(
    r"<!-- benchmark-task-group-metadata:v1 -->\s*```yaml\n(.*?)\n```",
    re.DOTALL,
)
DATASET_INFORMATION_RE = re.compile(
    r"(## Dataset Information\n\n\| Field \| Value \|\n\| --- \| --- \|\n)(.*?)(?=\n\n### Public Sources)",
    re.DOTALL,
)

BM25_CONFIG = "bm25"
DENSE_CONFIG = "harrier_oss_v1_270m"
RERANKING_HYBRID_CONFIG = "reranking_hybrid"


@dataclass(frozen=True)
class CandidateMetrics:
    config: str
    label: str
    source: str
    top_k: int
    ndcg_at_10: float
    hit_at_10: float
    recall_at_100: float
    candidate_count_min: int
    candidate_count_max: int
    candidate_count_mean: float
    query_count: int
    query_coverage: float
    relevant_coverage_at_100: float
    safeguard_positive_rows: int | None = None
    rows_with_101_candidates: int | None = None

    def as_yaml(self) -> dict[str, Any]:
        payload: dict[str, Any] = {
            "config": self.config,
            "label": self.label,
            "source": self.source,
            "top_k": self.top_k,
            "ndcg_at_10": round(self.ndcg_at_10, 10),
            "hit_at_10": round(self.hit_at_10, 10),
            "recall_at_100": round(self.recall_at_100, 10),
            "candidate_count_min": self.candidate_count_min,
            "candidate_count_max": self.candidate_count_max,
            "candidate_count_mean": round(self.candidate_count_mean, 6),
            "query_count": self.query_count,
            "query_coverage": round(self.query_coverage, 10),
            "relevant_coverage_at_100": round(self.relevant_coverage_at_100, 10),
        }
        if self.safeguard_positive_rows is not None:
            payload["safeguard_positive_rows"] = self.safeguard_positive_rows
        if self.rows_with_101_candidates is not None:
            payload["rows_with_101_candidates"] = self.rows_with_101_candidates
        return payload


def main(argv: Sequence[str] | None = None) -> int:
    args = parse_args(argv)
    task_docs = sorted(path for path in args.docs_root.rglob("*.md") if path.name != "index.md")
    changed: list[Path] = []
    metrics_cache: dict[tuple[str, str], dict[str, CandidateMetrics]] = {}

    for path in task_docs:
        text = path.read_text(encoding="utf-8")
        match = TASK_METADATA_RE.search(text)
        if not match:
            continue
        payload = yaml.safe_load(match.group(1))
        metadata = payload["benchmark_task_metadata"]
        if args.skip_existing and metadata.get("candidate_subsets"):
            continue
        key = (metadata["dataset_id"], metadata["split_name"])
        if key not in metrics_cache:
            if not args.dry_run:
                print(f"load {metadata['dataset_id']} {metadata['split_name']}", flush=True)
            metrics_cache[key] = load_candidate_metrics(
                dataset_id=metadata["dataset_id"],
                split_name=metadata["split_name"],
                reranking_hybrid_config=args.reranking_hybrid_config,
            )
        updated_metadata = dict(metadata)
        metrics = metrics_cache[key]
        updated_metadata["bm25"] = {
            "ndcg_at_10": metrics["bm25"].ndcg_at_10,
            "hit_at_10": metrics["bm25"].hit_at_10,
            "source": "dataset_candidate_subset",
        }
        updated_metadata["candidate_subsets"] = {
            name: value.as_yaml()
            for name, value in metrics.items()
            if value is not None
        }
        updated_text = replace_task_metadata(text, {"benchmark_task_metadata": updated_metadata})
        updated_text = replace_dataset_information(updated_text, metrics)
        if updated_text != text:
            changed.append(path)
            if not args.dry_run:
                path.write_text(updated_text, encoding="utf-8")

    group_changed = update_group_docs(args.docs_root, dry_run=args.dry_run)
    changed.extend(group_changed)

    for path in changed:
        print(path)
    print(f"changed={len(changed)}")
    return 0


def parse_args(argv: Sequence[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Update benchmark task docs with Nano candidate subset metadata.")
    parser.add_argument("--docs-root", type=Path, default=Path("docs/benchmark_tasks"))
    parser.add_argument("--reranking-hybrid-config", default=RERANKING_HYBRID_CONFIG)
    parser.add_argument("--skip-existing", action="store_true", help="Skip task docs that already have candidate_subsets.")
    parser.add_argument("--dry-run", action="store_true")
    return parser.parse_args(argv)


def load_candidate_metrics(
    *, dataset_id: str, split_name: str, reranking_hybrid_config: str
) -> dict[str, CandidateMetrics]:
    configs = set(get_config_names(dataset_id))
    required = [BM25_CONFIG, DENSE_CONFIG, reranking_hybrid_config]
    missing = [config for config in required if config not in configs]
    if missing:
        raise ValueError(f"{dataset_id} is missing required configs: {', '.join(missing)}")

    qrels = qrels_by_query(load_dataset_split(dataset_id, "qrels", split_name))
    bm25 = rankings_by_query(load_dataset_split(dataset_id, BM25_CONFIG, split_name))
    dense = rankings_by_query(load_dataset_split(dataset_id, DENSE_CONFIG, split_name))
    reranking_hybrid = rankings_by_query(load_dataset_split(dataset_id, reranking_hybrid_config, split_name))

    return {
        "bm25": compute_candidate_metrics(
            rankings=bm25,
            qrels=qrels,
            config=BM25_CONFIG,
            label="BM25",
            source="dataset_candidate_subset",
            top_k=500,
        ),
        "dense": compute_candidate_metrics(
            rankings=dense,
            qrels=qrels,
            config=DENSE_CONFIG,
            label="Dense",
            source="dataset_candidate_subset",
            top_k=500,
        ),
        "reranking_hybrid": compute_candidate_metrics(
            rankings=reranking_hybrid,
            qrels=qrels,
            config=reranking_hybrid_config,
            label="Reranking hybrid",
            source="dataset_candidate_subset",
            top_k=100,
            include_safeguard=True,
        ),
    }


@lru_cache(maxsize=None)
def get_config_names(dataset_id: str) -> tuple[str, ...]:
    from datasets import get_dataset_config_names

    return tuple(get_dataset_config_names(dataset_id))


@lru_cache(maxsize=None)
def load_dataset_config(dataset_id: str, config_name: str) -> Any:
    from datasets import disable_progress_bar, load_dataset

    disable_progress_bar()
    return load_dataset(dataset_id, config_name)


def load_dataset_split(dataset_id: str, config_name: str, split_name: str) -> Any:
    return load_dataset_config(dataset_id, config_name)[split_name]


def qrels_by_query(rows: Any) -> dict[str, set[str]]:
    qrels: dict[str, set[str]] = {}
    for row in rows:
        query_id = str(first_present(row, ("query-id", "query_id", "qid", "query", "_id")))
        corpus_id = str(first_present(row, ("corpus-id", "corpus_id", "docid", "document_id", "doc_id")))
        if "score" in row and row["score"] is not None:
            try:
                if float(row["score"]) <= 0:
                    continue
            except (TypeError, ValueError):
                pass
        qrels.setdefault(query_id, set()).add(corpus_id)
    return qrels


def rankings_by_query(rows: Any) -> dict[str, list[str]]:
    rankings: dict[str, list[str]] = {}
    for row in rows:
        query_id = str(first_present(row, ("query-id", "query_id", "qid", "_id")))
        corpus_ids = row.get("corpus-ids") or row.get("corpus_ids") or row.get("doc_ids") or []
        rankings[query_id] = [str(corpus_id) for corpus_id in corpus_ids]
    return rankings


def first_present(row: Mapping[str, Any], keys: Sequence[str]) -> Any:
    for key in keys:
        if key in row and row[key] is not None:
            return row[key]
    raise KeyError(f"none of the expected keys are present: {', '.join(keys)}")


def compute_candidate_metrics(
    *,
    rankings: Mapping[str, list[str]],
    qrels: Mapping[str, set[str]],
    config: str,
    label: str,
    source: str,
    top_k: int,
    include_safeguard: bool = False,
) -> CandidateMetrics:
    query_ids = sorted(qrels)
    if not query_ids:
        raise ValueError("cannot compute candidate metrics without qrels")
    ndcg_values: list[float] = []
    hit_values: list[float] = []
    covered_relevant = 0
    relevant_count = 0
    query_with_candidates = 0
    candidate_counts: list[int] = []
    rows_with_101 = 0
    safeguard_rows = 0

    for query_id in query_ids:
        positives = qrels[query_id]
        candidates = rankings.get(query_id, [])
        if candidates:
            query_with_candidates += 1
        candidate_counts.append(len(candidates))
        cutoff_10 = candidates[:10]
        cutoff_100 = candidates[:100]
        ndcg_values.append(ndcg_at_k(cutoff_10, positives, k=10))
        hit_values.append(1.0 if any(candidate in positives for candidate in cutoff_10) else 0.0)
        covered_relevant += len(set(cutoff_100) & positives)
        relevant_count += len(positives)
        if include_safeguard and len(candidates) == 101:
            rows_with_101 += 1
            if candidates[100] in positives and not any(candidate in positives for candidate in cutoff_100):
                safeguard_rows += 1

    return CandidateMetrics(
        config=config,
        label=label,
        source=source,
        top_k=top_k,
        ndcg_at_10=sum(ndcg_values) / len(ndcg_values),
        hit_at_10=sum(hit_values) / len(hit_values),
        recall_at_100=covered_relevant / relevant_count if relevant_count else 0.0,
        candidate_count_min=min(candidate_counts) if candidate_counts else 0,
        candidate_count_max=max(candidate_counts) if candidate_counts else 0,
        candidate_count_mean=sum(candidate_counts) / len(candidate_counts) if candidate_counts else 0.0,
        query_count=len(query_ids),
        query_coverage=query_with_candidates / len(query_ids),
        relevant_coverage_at_100=covered_relevant / relevant_count if relevant_count else 0.0,
        safeguard_positive_rows=safeguard_rows if include_safeguard else None,
        rows_with_101_candidates=rows_with_101 if include_safeguard else None,
    )


def ndcg_at_k(candidates: Sequence[str], positives: set[str], *, k: int) -> float:
    if not positives:
        return 0.0
    dcg = 0.0
    for index, candidate in enumerate(candidates[:k], start=1):
        if candidate in positives:
            dcg += 1.0 / math.log2(index + 1)
    ideal_relevant = min(len(positives), k)
    idcg = sum(1.0 / math.log2(index + 1) for index in range(1, ideal_relevant + 1))
    return dcg / idcg if idcg else 0.0


def replace_task_metadata(text: str, payload: Mapping[str, Any]) -> str:
    yaml_text = yaml.safe_dump(payload, sort_keys=False, allow_unicode=True).rstrip()
    return TASK_METADATA_RE.sub(f"<!-- benchmark-task-metadata:v1 -->\n\n```yaml\n{yaml_text}\n```", text, count=1)


def replace_dataset_information(text: str, metrics: Mapping[str, CandidateMetrics]) -> str:
    match = DATASET_INFORMATION_RE.search(text)
    if not match:
        return text
    rows = parse_markdown_rows(match.group(2))
    for key in (
        "BM25 Recall@100",
        "BM25 candidate subset",
        "Dense candidate subset",
        "Dense nDCG@10",
        "Dense hit@10",
        "Dense Recall@100",
        "RRF reranking candidate subset",
        "RRF reranking nDCG@10",
        "RRF reranking hit@10",
        "RRF reranking Recall@100",
        "RRF reranking candidates / query",
        "RRF safeguard rows",
        "Reranking hybrid candidate subset",
        "Reranking hybrid nDCG@10",
        "Reranking hybrid hit@10",
        "Reranking hybrid Recall@100",
        "Reranking hybrid candidates / query",
        "Reranking hybrid safeguard rows",
    ):
        rows.pop(key, None)

    rows["BM25 nDCG@10"] = score(metrics["bm25"].ndcg_at_10)
    rows["BM25 hit@10"] = score(metrics["bm25"].hit_at_10)
    insert_after(
        rows,
        "BM25 hit@10",
        [
            ("BM25 Recall@100", score(metrics["bm25"].recall_at_100)),
            ("BM25 candidate subset", "top-500 (`bm25`)"),
            ("Dense nDCG@10", score(metrics["dense"].ndcg_at_10)),
            ("Dense hit@10", score(metrics["dense"].hit_at_10)),
            ("Dense Recall@100", score(metrics["dense"].recall_at_100)),
            ("Dense candidate subset", "top-500 (`harrier_oss_v1_270m`)"),
            ("Reranking hybrid nDCG@10", score(metrics["reranking_hybrid"].ndcg_at_10)),
            ("Reranking hybrid hit@10", score(metrics["reranking_hybrid"].hit_at_10)),
            ("Reranking hybrid Recall@100", score(metrics["reranking_hybrid"].recall_at_100)),
            (
                "Reranking hybrid candidate subset",
                f"top-100 plus optional rank-101 safeguard (`{metrics['reranking_hybrid'].config}`)",
            ),
            (
                "Reranking hybrid candidates / query",
                candidate_count_range(metrics["reranking_hybrid"]),
            ),
            ("Reranking hybrid safeguard rows", str(metrics["reranking_hybrid"].safeguard_positive_rows or 0)),
        ],
    )
    replacement = match.group(1) + render_markdown_rows(rows)
    return text[: match.start()] + replacement + text[match.end() :]


def parse_markdown_rows(table_body: str) -> dict[str, str]:
    rows: dict[str, str] = {}
    for line in table_body.strip().splitlines():
        if not line.startswith("|"):
            continue
        cells = [cell.strip() for cell in line.strip().strip("|").split("|")]
        if len(cells) >= 2:
            rows[cells[0]] = cells[1]
    return rows


def insert_after(rows: dict[str, str], anchor: str, new_rows: Sequence[tuple[str, str]]) -> None:
    if not new_rows:
        return
    items = list(rows.items())
    rows.clear()
    inserted = False
    for key, value in items:
        rows[key] = value
        if key == anchor:
            for new_key, new_value in new_rows:
                rows[new_key] = new_value
            inserted = True
    if not inserted:
        for new_key, new_value in new_rows:
            rows[new_key] = new_value


def render_markdown_rows(rows: Mapping[str, str]) -> str:
    return "\n".join(f"| {key} | {value} |" for key, value in rows.items())


def score(value: float) -> str:
    return f"{value:.4f}"


def candidate_count_range(metrics: CandidateMetrics) -> str:
    if metrics.candidate_count_min == metrics.candidate_count_max:
        return str(metrics.candidate_count_min)
    return f"{metrics.candidate_count_min}-{metrics.candidate_count_max}"


def update_group_docs(docs_root: Path, *, dry_run: bool) -> list[Path]:
    changed: list[Path] = []
    for path in sorted(docs_root.rglob("index.md")):
        text = path.read_text(encoding="utf-8")
        match = GROUP_METADATA_RE.search(text)
        if not match:
            continue
        task_metrics = load_group_task_metrics(path.parent)
        if not task_metrics:
            continue
        payload = yaml.safe_load(match.group(1))
        group_metadata = dict(payload["benchmark_task_group_metadata"])
        group_metadata["candidate_subsets"] = aggregate_group_metrics(task_metrics)
        if "bm25" in group_metadata and "bm25" in group_metadata["candidate_subsets"]:
            group_metadata["bm25"]["ndcg_at_10_query_weighted"] = group_metadata["candidate_subsets"]["bm25"][
                "query_weighted_ndcg_at_10"
            ]
            group_metadata["bm25"]["hit_at_10_query_weighted"] = group_metadata["candidate_subsets"]["bm25"][
                "query_weighted_hit_at_10"
            ]
            group_metadata["bm25"]["source"] = "dataset_candidate_subset"
        updated_text = replace_group_metadata(text, {"benchmark_task_group_metadata": group_metadata})
        updated_text = replace_group_dataset_information(updated_text, group_metadata["candidate_subsets"])
        if updated_text != text:
            changed.append(path)
            if not dry_run:
                path.write_text(updated_text, encoding="utf-8")
    return changed


def load_group_task_metrics(group_dir: Path) -> list[tuple[int, Mapping[str, Any]]]:
    items: list[tuple[int, Mapping[str, Any]]] = []
    for path in sorted(group_dir.glob("*.md")):
        if path.name == "index.md":
            continue
        text = path.read_text(encoding="utf-8")
        match = TASK_METADATA_RE.search(text)
        if not match:
            continue
        metadata = yaml.safe_load(match.group(1))["benchmark_task_metadata"]
        candidate_subsets = metadata.get("candidate_subsets")
        if candidate_subsets:
            items.append((int(metadata["counts"]["queries"]), candidate_subsets))
    return items


def aggregate_group_metrics(task_metrics: Sequence[tuple[int, Mapping[str, Any]]]) -> dict[str, Any]:
    total_queries = sum(weight for weight, _ in task_metrics)
    aggregates: dict[str, Any] = {}
    for name in ("bm25", "dense", "reranking_hybrid"):
        weighted = [((weight, metrics[name])) for weight, metrics in task_metrics if name in metrics]
        if not weighted:
            continue
        aggregates[name] = {
            "query_weighted_ndcg_at_10": round(
                sum(weight * float(metrics["ndcg_at_10"]) for weight, metrics in weighted) / total_queries,
                10,
            ),
            "query_weighted_hit_at_10": round(
                sum(weight * float(metrics["hit_at_10"]) for weight, metrics in weighted) / total_queries,
                10,
            ),
            "query_weighted_recall_at_100": round(
                sum(weight * float(metrics["recall_at_100"]) for weight, metrics in weighted) / total_queries,
                10,
            ),
            "source": "dataset_candidate_subset",
        }
    return aggregates


def replace_group_metadata(text: str, payload: Mapping[str, Any]) -> str:
    yaml_text = yaml.safe_dump(payload, sort_keys=False, allow_unicode=True).rstrip()
    return GROUP_METADATA_RE.sub(
        f"<!-- benchmark-task-group-metadata:v1 -->\n\n```yaml\n{yaml_text}\n```",
        text,
        count=1,
    )


def replace_group_dataset_information(text: str, candidate_subsets: Mapping[str, Any]) -> str:
    match = DATASET_INFORMATION_RE.search(text)
    if not match:
        return text
    rows = parse_markdown_rows(match.group(2))
    for key in (
        "Query-weighted BM25 Recall@100",
        "Query-weighted Dense nDCG@10",
        "Query-weighted Dense hit@10",
        "Query-weighted Dense Recall@100",
        "Query-weighted RRF reranking nDCG@10",
        "Query-weighted RRF reranking hit@10",
        "Query-weighted RRF reranking Recall@100",
        "Query-weighted Reranking hybrid nDCG@10",
        "Query-weighted Reranking hybrid hit@10",
        "Query-weighted Reranking hybrid Recall@100",
    ):
        rows.pop(key, None)
    rows["Query-weighted BM25 nDCG@10"] = score(candidate_subsets["bm25"]["query_weighted_ndcg_at_10"])
    rows["Query-weighted BM25 hit@10"] = score(candidate_subsets["bm25"]["query_weighted_hit_at_10"])
    insert_after(
        rows,
        "Query-weighted BM25 hit@10",
        [
            (
                "Query-weighted BM25 Recall@100",
                score(candidate_subsets["bm25"]["query_weighted_recall_at_100"]),
            ),
            ("Query-weighted Dense nDCG@10", score(candidate_subsets["dense"]["query_weighted_ndcg_at_10"])),
            ("Query-weighted Dense hit@10", score(candidate_subsets["dense"]["query_weighted_hit_at_10"])),
            (
                "Query-weighted Dense Recall@100",
                score(candidate_subsets["dense"]["query_weighted_recall_at_100"]),
            ),
            (
                "Query-weighted Reranking hybrid nDCG@10",
                score(candidate_subsets["reranking_hybrid"]["query_weighted_ndcg_at_10"]),
            ),
            (
                "Query-weighted Reranking hybrid hit@10",
                score(candidate_subsets["reranking_hybrid"]["query_weighted_hit_at_10"]),
            ),
            (
                "Query-weighted Reranking hybrid Recall@100",
                score(candidate_subsets["reranking_hybrid"]["query_weighted_recall_at_100"]),
            ),
        ],
    )
    replacement = match.group(1) + render_markdown_rows(rows)
    return text[: match.start()] + replacement + text[match.end() :]


if __name__ == "__main__":
    raise SystemExit(main())
