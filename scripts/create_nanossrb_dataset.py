from __future__ import annotations

import argparse
from collections import defaultdict
from dataclasses import replace
import heapq
import json
import math
from pathlib import Path
import sys
from typing import Any, Iterable, cast

from huggingface_hub import HfApi, hf_hub_download

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from hakari_bench.bm25 import BM25Config  # noqa: E402
from hakari_bench.nano_dataset_builder import build_nano_dataset_from_rows  # noqa: E402
from hakari_bench.nanossrb import (  # noqa: E402
    SSRBQuery,
    OverflowPolicy,
    apply_positive_limit,
    condition_stratified_sample,
    parse_source_condition,
    stable_key,
)


SOURCE_DATASET_ID = "vec-ai/struct-ir"
DOMAIN_SPLITS = {
    "Academic": "Academic",
    "Finance_and_Economics": "FinanceAndEconomics",
    "human_resources": "HumanResources",
    "llm_agent_and_tool": "LLMAgentAndTool",
    "product_search": "ProductSearch",
    "resume_search": "ResumeSearch",
}
VARIANTS = {
    "strict-max5": {"dataset_name": "NanoSSRB", "max_positives": 5, "overflow_policy": "drop-query"},
    "cap-max5": {"dataset_name": "NanoSSRB-Cap5", "max_positives": 5, "overflow_policy": "cap-and-exclude"},
    "strict-max3": {"dataset_name": "NanoSSRB-Max3", "max_positives": 3, "overflow_policy": "drop-query"},
}


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Create six-domain NanoSSRB datasets from vec-ai/struct-ir.")
    parser.add_argument("--variant", choices=[*VARIANTS, "all"], default="strict-max5")
    parser.add_argument(
        "--domain",
        action="append",
        choices=sorted(DOMAIN_SPLITS.values()),
        help="Generate only the named output task; repeat for multiple tasks.",
    )
    parser.add_argument("--output-root", type=Path, default=Path("output/nanossrb"))
    parser.add_argument("--dataset-config-dir", type=Path, default=None)
    parser.add_argument("--query-limit", type=int, default=200)
    parser.add_argument("--doc-limit", type=int, default=10_000)
    parser.add_argument("--min-per-schema", type=int, default=2)
    parser.add_argument("--bm25-top-k", type=int, default=500)
    parser.add_argument("--seed", type=int, default=17)
    parser.add_argument("--revision", default="main")
    parser.add_argument(
        "--source-dir",
        type=Path,
        default=None,
        help="Optional local mirror with the same Domain/schema.*.jsonl layout.",
    )
    parser.add_argument("--overwrite", action="store_true")
    return parser.parse_args(argv)


def _source_files(*, source_dir: Path | None, revision: str) -> list[str]:
    if source_dir is not None:
        return sorted(str(path.relative_to(source_dir)) for path in source_dir.glob("*/*.corpus.jsonl"))
    return sorted(
        path
        for path in HfApi().list_repo_files(SOURCE_DATASET_ID, repo_type="dataset", revision=revision)
        if path.endswith(".corpus.jsonl")
    )


def _local_path(relative_path: str, *, source_dir: Path | None, revision: str) -> Path:
    if source_dir is not None:
        path = source_dir / relative_path
        if not path.exists():
            raise FileNotFoundError(path)
        return path
    return Path(
        hf_hub_download(
            SOURCE_DATASET_ID,
            relative_path,
            repo_type="dataset",
            revision=revision,
        )
    )


def _read_jsonl(path: Path) -> list[dict[str, Any]]:
    with path.open(encoding="utf-8") as handle:
        return [json.loads(line) for line in handle if line.strip()]


def _schema_name(corpus_path: str) -> str:
    return Path(corpus_path).name.removesuffix(".corpus.jsonl")


def _related_path(corpus_path: str, kind: str) -> str:
    return corpus_path.replace(".corpus.jsonl", f".{kind}.test.jsonl")


def load_domain_queries(
    corpus_paths: list[str],
    *,
    source_dir: Path | None,
    revision: str,
) -> tuple[list[SSRBQuery], dict[str, set[str]]]:
    queries: list[SSRBQuery] = []
    all_positive_ids_by_schema: dict[str, set[str]] = {}
    for corpus_path in corpus_paths:
        domain = corpus_path.split("/", maxsplit=1)[0]
        schema = _schema_name(corpus_path)
        query_rows = _read_jsonl(_local_path(_related_path(corpus_path, "queries"), source_dir=source_dir, revision=revision))
        qrel_rows = _read_jsonl(_local_path(_related_path(corpus_path, "qrels"), source_dir=source_dir, revision=revision))
        positives_by_query: dict[str, list[str]] = defaultdict(list)
        all_positive_ids: set[str] = set()
        for row in qrel_rows:
            if float(row.get("label", 1)) <= 0:
                continue
            query_id = str(row["query_id"])
            corpus_id = str(row["corpus_id"])
            positives_by_query[query_id].append(corpus_id)
            all_positive_ids.add(corpus_id)
        all_positive_ids_by_schema[schema] = all_positive_ids
        for row in query_rows:
            query_id = str(row["_id"])
            positive_ids = tuple(dict.fromkeys(positives_by_query.get(query_id, [])))
            if not positive_ids:
                continue
            exact_conditions, semantic_conditions = parse_source_condition(row.get("cond"))
            queries.append(
                SSRBQuery(
                    query_id=query_id,
                    text=str(row["text"]).strip(),
                    domain=domain,
                    schema=schema,
                    positive_doc_ids=positive_ids,
                    time_type=int(row.get("time_type") or 0),
                    exact_conditions=exact_conditions,
                    semantic_conditions=semantic_conditions,
                    source_condition=str(row["cond"]) if row.get("cond") is not None else None,
                )
            )
    return queries, all_positive_ids_by_schema


def select_variant_queries(
    source_queries: list[SSRBQuery],
    *,
    variant: str,
    query_limit: int,
    min_per_schema: int,
    seed: int,
) -> tuple[list[SSRBQuery], set[str]]:
    settings = VARIANTS[variant]
    max_positives = int(settings["max_positives"])
    overflow_policy = cast(OverflowPolicy, settings["overflow_policy"])
    eligible, _ = apply_positive_limit(
        source_queries,
        max_positives=max_positives,
        overflow_policy=overflow_policy,
        seed=seed,
    )
    pool_limit = query_limit
    if overflow_policy == "cap-and-exclude":
        pool_limit = min(len(eligible), max(query_limit * 2, query_limit + 25))
    selected_pool = condition_stratified_sample(
        eligible,
        query_limit=pool_limit,
        min_per_schema=min_per_schema,
        seed=seed,
    )
    source_by_id = {query.query_id: query for query in source_queries}
    capped_pool, pool_excluded_doc_ids = apply_positive_limit(
        [source_by_id[query.query_id] for query in selected_pool],
        max_positives=max_positives,
        overflow_policy=overflow_policy,
        seed=seed,
    )
    if pool_excluded_doc_ids:
        capped_pool = [
            query
            for query in (
                replace(
                    query,
                    positive_doc_ids=tuple(
                        doc_id for doc_id in query.positive_doc_ids if doc_id not in pool_excluded_doc_ids
                    ),
                )
                for query in capped_pool
            )
            if query.positive_doc_ids
        ]
    selected = condition_stratified_sample(
        capped_pool,
        query_limit=query_limit,
        min_per_schema=min_per_schema,
        seed=seed,
    )
    selected, excluded_doc_ids = apply_positive_limit(
        [source_by_id[query.query_id] for query in selected],
        max_positives=max_positives,
        overflow_policy=overflow_policy,
        seed=seed,
    )
    if overflow_policy == "drop-query" and variant == "strict-max5" and len(selected) < query_limit:
        needed = query_limit - len(selected)
        selected_ids = {query.query_id for query in selected}
        spillover = [
            query
            for query in source_queries
            if query.query_id not in selected_ids and len(query.positive_doc_ids) == max_positives + 1
        ]
        selected.extend(
            condition_stratified_sample(
                spillover,
                query_limit=needed,
                min_per_schema=0,
                seed=seed + 1,
            )
        )
    if excluded_doc_ids:
        selected = [
            replace(
                query,
                positive_doc_ids=tuple(
                    doc_id for doc_id in query.positive_doc_ids if doc_id not in excluded_doc_ids
                ),
            )
            for query in selected
        ]
        selected = [query for query in selected if query.positive_doc_ids]
    return selected, excluded_doc_ids


def _reservoir_rows(
    corpus_path: Path,
    *,
    wanted_ids: set[str],
    excluded_ids: set[str],
    known_positive_ids: set[str],
    candidate_limit: int,
    seed: int,
) -> tuple[dict[str, dict[str, str]], list[dict[str, str]]]:
    wanted: dict[str, dict[str, str]] = {}
    heap: list[tuple[int, str]] = []
    candidate_rows: dict[str, dict[str, str]] = {}
    with corpus_path.open(encoding="utf-8") as handle:
        for line in handle:
            if not line.strip():
                continue
            raw = json.loads(line)
            doc_id = str(raw["_id"])
            if doc_id in excluded_ids:
                continue
            row = {"_id": doc_id, "text": str(raw["text"]).strip()}
            if not row["text"]:
                continue
            if doc_id in wanted_ids:
                wanted[doc_id] = row
                continue
            if doc_id in known_positive_ids or "--n--" not in doc_id:
                continue
            score = int(stable_key(doc_id, seed=seed), 16)
            item = (-score, doc_id)
            candidate_rows[doc_id] = row
            if len(heap) < candidate_limit:
                heapq.heappush(heap, item)
            elif item > heap[0]:
                removed = heapq.heapreplace(heap, item)
                candidate_rows.pop(removed[1], None)
            else:
                candidate_rows.pop(doc_id, None)
    candidates = [candidate_rows[item[1]] for item in sorted(heap, reverse=True)]
    return wanted, candidates


def sample_domain_corpus(
    corpus_paths: list[str],
    *,
    selected_queries: list[SSRBQuery],
    excluded_doc_ids: set[str],
    all_positive_ids_by_schema: dict[str, set[str]],
    source_dir: Path | None,
    revision: str,
    doc_limit: int,
    seed: int,
) -> list[dict[str, str]]:
    positives_by_schema: dict[str, set[str]] = defaultdict(set)
    for query in selected_queries:
        positives_by_schema[query.schema].update(query.positive_doc_ids)
    candidate_limit = max(100, math.ceil(doc_limit / len(corpus_paths)) * 2)
    positives: dict[str, dict[str, str]] = {}
    candidates_by_schema: dict[str, list[dict[str, str]]] = {}
    for index, corpus_path in enumerate(corpus_paths, start=1):
        schema = _schema_name(corpus_path)
        print(f"  scanning corpus {index}/{len(corpus_paths)}: {corpus_path}", flush=True)
        wanted, candidates = _reservoir_rows(
            _local_path(corpus_path, source_dir=source_dir, revision=revision),
            wanted_ids=positives_by_schema[schema],
            excluded_ids=excluded_doc_ids,
            known_positive_ids=all_positive_ids_by_schema[schema],
            candidate_limit=candidate_limit,
            seed=seed,
        )
        missing = positives_by_schema[schema] - set(wanted)
        if missing:
            raise RuntimeError(f"missing {len(missing)} selected positives in {corpus_path}: {sorted(missing)[:3]}")
        positives.update(wanted)
        candidates_by_schema[schema] = candidates
    if len(positives) > doc_limit:
        raise RuntimeError(f"selected positives ({len(positives)}) exceed doc limit ({doc_limit})")

    output = list(positives.values())
    selected_ids = set(positives)
    schemas = sorted(candidates_by_schema)
    offset = 0
    while len(output) < doc_limit:
        added = False
        for schema in schemas:
            candidates = candidates_by_schema[schema]
            if offset >= len(candidates):
                continue
            row = candidates[offset]
            if row["_id"] not in selected_ids:
                output.append(row)
                selected_ids.add(row["_id"])
                added = True
                if len(output) >= doc_limit:
                    break
        if not added:
            break
        offset += 1
    if len(output) < doc_limit:
        raise RuntimeError(f"only sampled {len(output)} documents for requested limit {doc_limit}")
    return output


def _query_rows(queries: Iterable[SSRBQuery]) -> list[dict[str, str]]:
    return [{"_id": query.query_id, "text": query.text} for query in queries]


def _qrel_rows(queries: Iterable[SSRBQuery]) -> list[dict[str, object]]:
    return [
        {"query-id": query.query_id, "corpus-id": doc_id, "score": 1}
        for query in queries
        for doc_id in query.positive_doc_ids
    ]


def build_variant(args: argparse.Namespace, *, variant: str, corpus_files: list[str]) -> None:
    settings = VARIANTS[variant]
    dataset_name = str(settings["dataset_name"])
    output_dir = args.output_root / dataset_name
    if output_dir.exists() and not args.overwrite:
        raise FileExistsError(f"{output_dir} already exists; pass --overwrite to replace split files")
    for source_domain, split_name in DOMAIN_SPLITS.items():
        if args.domain and split_name not in args.domain:
            continue
        print(f"[{variant}] preparing {split_name}", flush=True)
        domain_corpora = [path for path in corpus_files if path.startswith(f"{source_domain}/")]
        source_queries, all_positive_ids_by_schema = load_domain_queries(
            domain_corpora,
            source_dir=args.source_dir,
            revision=args.revision,
        )
        selected_queries, excluded_doc_ids = select_variant_queries(
            source_queries,
            variant=variant,
            query_limit=args.query_limit,
            min_per_schema=args.min_per_schema,
            seed=args.seed,
        )
        spillover_query_count = sum(
            len(query.positive_doc_ids) == int(settings["max_positives"]) + 1 for query in selected_queries
        )
        if len(selected_queries) != args.query_limit:
            raise RuntimeError(
                f"{split_name} selected {len(selected_queries)} queries, expected {args.query_limit}; "
                "adjust the positive threshold or selection policy"
            )
        corpus_rows = sample_domain_corpus(
            domain_corpora,
            selected_queries=selected_queries,
            excluded_doc_ids=excluded_doc_ids,
            all_positive_ids_by_schema=all_positive_ids_by_schema,
            source_dir=args.source_dir,
            revision=args.revision,
            doc_limit=args.doc_limit,
            seed=args.seed,
        )
        metadata = {
            "description": (
                f"{dataset_name} merges SSRB schemas into six domain retrieval tasks using condition-stratified "
                f"query sampling and the {variant} positive-label policy."
            ),
            "source_benchmark_name": "SSRB (Struct-IR)",
            "source_dataset_id": SOURCE_DATASET_ID,
            "source_dataset_revision": args.revision,
            "source_eval_split": "test",
            "source_subset_count": len(domain_corpora),
            "source_selected_query_count": len(selected_queries),
            "source_query_selection_policy": "condition-stratified with per-schema minimum coverage",
            "strict_shortfall_spillover": {
                "positive_count": int(settings["max_positives"]) + 1,
                "query_count": spillover_query_count,
                "qrels_policy": "all upstream positives are retained without capping",
            },
            "source_corpus_order_policy": "all selected positives, then schema-round-robin deterministic n-provenance negatives",
            "source_positive_like_exclusion_policy": (
                "all source-qrels positives are excluded from negative sampling; positives omitted by the cap policy "
                "are excluded from the Nano corpus"
            ),
            "source_links": [
                "https://github.com/vec-ai/struct-ir",
                "https://huggingface.co/datasets/vec-ai/struct-ir",
            ],
            "source_dataset_location": "vec-ai/struct-ir on Hugging Face",
            "source_split_policy": "Six domain tasks formed by merging the 99 upstream schema subsets.",
            "corpus_fill_policy": "selected positives followed by deterministic schema-balanced n-provenance documents",
            "qrels_capping_note": (
                f"Positive policy {variant}; queries normally have at most {settings['max_positives']} qrels. "
                "If the strict pool cannot reach the requested query count, the shortfall is filled only with "
                f"queries having {int(settings['max_positives']) + 1} positives, retaining every qrel."
            ),
            "language": "en",
            "category": "structured_data",
        }
        build_nano_dataset_from_rows(
            output_dir=output_dir,
            dataset_name=dataset_name,
            dataset_id=f"hakari-bench/{dataset_name}",
            split_name=split_name,
            corpus_rows=corpus_rows,
            query_rows=_query_rows(selected_queries),
            qrels_rows=_qrel_rows(selected_queries),
            dataset_config_dir=args.dataset_config_dir,
            query_limit=args.query_limit,
            doc_limit=args.doc_limit,
            bm25_config=BM25Config(tokenizer="regex", top_k=args.bm25_top_k, show_progress=True),
            metadata=metadata,
            dedupe_query_texts=False,
            dedupe_doc_texts=False,
        )


def main(argv: list[str] | None = None) -> None:
    args = parse_args(argv)
    corpus_files = _source_files(source_dir=args.source_dir, revision=args.revision)
    expected = sum(1 for path in corpus_files if path.split("/", maxsplit=1)[0] in DOMAIN_SPLITS)
    if expected != 99:
        raise RuntimeError(f"expected 99 SSRB corpus files, found {expected}")
    variants = list(VARIANTS) if args.variant == "all" else [args.variant]
    for variant in variants:
        build_variant(args, variant=variant, corpus_files=corpus_files)


if __name__ == "__main__":
    main()
