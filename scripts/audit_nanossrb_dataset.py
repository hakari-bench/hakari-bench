from __future__ import annotations

import argparse
from collections import Counter, defaultdict
import json
from pathlib import Path
import sys
from typing import Any

import pyarrow.parquet as pq

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from scripts.create_nanossrb_dataset import (  # noqa: E402
    DOMAIN_SPLITS,
    _local_path,
    _read_jsonl,
    _related_path,
    _source_files,
)


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Audit generated NanoSSRB variants against upstream qrels.")
    parser.add_argument("--output-root", type=Path, default=Path("output/nanossrb"))
    parser.add_argument("--dataset", action="append", dest="datasets")
    parser.add_argument("--source-dir", type=Path, default=None)
    parser.add_argument("--revision", default="main")
    parser.add_argument("--query-limit", type=int, default=200)
    return parser.parse_args(argv)


def _upstream_qrels(
    corpus_paths: list[str], *, source_dir: Path | None, revision: str
) -> dict[str, set[str]]:
    output: dict[str, set[str]] = defaultdict(set)
    for corpus_path in corpus_paths:
        rows = _read_jsonl(
            _local_path(_related_path(corpus_path, "qrels"), source_dir=source_dir, revision=revision)
        )
        for row in rows:
            if float(row.get("label", 1)) > 0:
                output[str(row["query_id"])].add(str(row["corpus_id"]))
    return output


def audit_split(
    *,
    output_dir: Path,
    split_name: str,
    upstream_qrels: dict[str, set[str]],
    expected_max_positives: int,
    expected_query_count: int,
) -> dict[str, Any]:
    queries = pq.read_table(output_dir / "queries" / f"{split_name}.parquet").to_pylist()
    corpus = pq.read_table(output_dir / "corpus" / f"{split_name}.parquet").to_pylist()
    qrels = pq.read_table(output_dir / "qrels" / f"{split_name}.parquet").to_pylist()
    candidates = pq.read_table(output_dir / "bm25" / f"{split_name}.parquet").to_pylist()
    query_ids = {str(row["_id"]) for row in queries}
    corpus_ids = {str(row["_id"]) for row in corpus}
    output_by_query: dict[str, set[str]] = defaultdict(set)
    for row in qrels:
        output_by_query[str(row["query-id"])].add(str(row["corpus-id"]))
    omitted_positive_ids = {
        doc_id
        for query_id in query_ids
        for doc_id in upstream_qrels.get(query_id, set()) - output_by_query.get(query_id, set())
    }
    candidate_by_query = {
        str(row["query-id"]): {str(doc_id) for doc_id in row["corpus-ids"]} for row in candidates
    }
    positive_counts = Counter(len(output_by_query[query_id]) for query_id in query_ids)
    unknown_qrels = [
        (query_id, doc_id)
        for query_id, doc_ids in output_by_query.items()
        for doc_id in doc_ids
        if doc_id not in upstream_qrels.get(query_id, set())
    ]
    missing_candidate_positives = [
        (query_id, doc_id)
        for query_id, doc_ids in output_by_query.items()
        for doc_id in doc_ids
        if doc_id not in candidate_by_query.get(query_id, set())
    ]
    non_positive_fillers = [
        doc_id
        for doc_id in corpus_ids
        if doc_id not in {doc for docs in output_by_query.values() for doc in docs} and "--n--" not in doc_id
    ]
    checks = {
        "query_count_matches_limit": len(query_ids) == expected_query_count,
        "corpus_count_is_10000": len(corpus_ids) == 10_000,
        "all_queries_have_qrels": set(output_by_query) == query_ids,
        "qrels_reference_output_rows": all(
            query_id in query_ids and doc_id in corpus_ids
            for query_id, doc_ids in output_by_query.items()
            for doc_id in doc_ids
        ),
        "qrels_are_upstream_positives": not unknown_qrels,
        "positive_limit_respected": max(positive_counts, default=0) <= expected_max_positives,
        "omitted_positives_absent_from_corpus": not (omitted_positive_ids & corpus_ids),
        "bm25_covers_all_qrels": not missing_candidate_positives,
        "fillers_are_n_provenance": not non_positive_fillers,
    }
    return {
        "split_name": split_name,
        "queries": len(query_ids),
        "corpus": len(corpus_ids),
        "qrels": sum(map(len, output_by_query.values())),
        "positive_count_distribution": {str(key): value for key, value in sorted(positive_counts.items())},
        "query_schema_count": len({query_id.split("--")[1] for query_id in query_ids}),
        "corpus_schema_count": len({doc_id.split("--")[1] for doc_id in corpus_ids}),
        "omitted_upstream_positive_doc_count": len(omitted_positive_ids),
        "omitted_positive_in_corpus_count": len(omitted_positive_ids & corpus_ids),
        "unknown_qrel_count": len(unknown_qrels),
        "missing_bm25_positive_count": len(missing_candidate_positives),
        "non_n_filler_count": len(non_positive_fillers),
        "checks": checks,
        "passed": all(checks.values()),
    }


def main(argv: list[str] | None = None) -> None:
    args = parse_args(argv)
    datasets = args.datasets or ["NanoSSRB", "NanoSSRB-Cap5", "NanoSSRB-Max3"]
    corpus_files = _source_files(source_dir=args.source_dir, revision=args.revision)
    reverse_domains = {split: domain for domain, split in DOMAIN_SPLITS.items()}
    for dataset_name in datasets:
        output_dir = args.output_root / dataset_name
        expected_max = 3 if dataset_name.endswith("Max3") else (6 if dataset_name == "NanoSSRB" else 5)
        results = []
        for split_name in DOMAIN_SPLITS.values():
            domain = reverse_domains[split_name]
            domain_corpora = [path for path in corpus_files if path.startswith(f"{domain}/")]
            results.append(
                audit_split(
                    output_dir=output_dir,
                    split_name=split_name,
                    upstream_qrels=_upstream_qrels(
                        domain_corpora, source_dir=args.source_dir, revision=args.revision
                    ),
                    expected_max_positives=expected_max,
                    expected_query_count=args.query_limit,
                )
            )
        payload = {
            "dataset_name": dataset_name,
            "source_dataset_id": "vec-ai/struct-ir",
            "source_revision": args.revision,
            "passed": all(result["passed"] for result in results),
            "splits": results,
        }
        (output_dir / "sampling_audit.json").write_text(
            json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
        )
        print(f"{dataset_name}: {'PASS' if payload['passed'] else 'FAIL'}")
        for result in results:
            print(
                f"  {result['split_name']}: q={result['queries']} d={result['corpus']} "
                f"r={result['qrels']} omitted={result['omitted_upstream_positive_doc_count']} "
                f"false_negative={result['omitted_positive_in_corpus_count']} "
                f"{'PASS' if result['passed'] else 'FAIL'}"
            )
        if not payload["passed"]:
            raise SystemExit(1)


if __name__ == "__main__":
    main()
