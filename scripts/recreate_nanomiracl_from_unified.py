from __future__ import annotations

import argparse
import json
import random
from collections import defaultdict
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from datasets import Dataset, load_dataset
from huggingface_hub import HfApi

from hakari_bench.bm25 import BM25Config
from hakari_bench.nano_dataset_builder import (
    DEFAULT_BM25_TOP_K,
    build_nano_dataset_from_rows,
)


LANGUAGES = (
    "ar",
    "bn",
    "de",
    "en",
    "es",
    "fa",
    "fi",
    "fr",
    "hi",
    "id",
    "ja",
    "ko",
    "ru",
    "sw",
    "te",
    "th",
    "yo",
    "zh",
)
DEFAULT_SOURCE_DATASET_ID = "hotchpotch/miracl-hf-unified"
DEFAULT_OUTPUT_DIR = Path(
    "output/nano_datasets_miracl_unified_multipos_hardneg/NanoMIRACL"
)
WORDSEG_LANGUAGES = {"ja", "ko", "th", "zh"}
WHITESPACE_LANGUAGES = {"bn", "te"}
STEMMER_ALGORITHMS_BY_LANGUAGE = {
    "ar": "arabic",
    "de": "german",
    "es": "spanish",
    "fi": "finnish",
    "fr": "french",
    "hi": "hindi",
    "id": "indonesian",
    "ru": "russian",
}


@dataclass(frozen=True)
class SplitInput:
    queries: list[dict[str, Any]]
    corpus: list[dict[str, Any]]
    qrels: list[dict[str, Any]]
    selected_positive_indices: int
    selected_hard_negative_indices: int
    random_fill_indices: int
    source_query_count: int


def main() -> None:
    args = _parse_args()
    source_info = HfApi().dataset_info(args.source_dataset_id)
    source_revision = source_info.sha or ""
    args.output_dir.mkdir(parents=True, exist_ok=True)

    summary_rows: list[dict[str, Any]] = []
    for language in args.languages:
        print(
            f"building {language} from {args.source_dataset_id} {language}_queries/{args.eval_split}"
        )
        split_input = _load_split_input(
            source_dataset_id=args.source_dataset_id,
            language=language,
            eval_split=args.eval_split,
            query_limit=args.query_limit,
            doc_limit=args.doc_limit,
            seed=args.seed,
            random_fill_oversample=args.random_fill_oversample,
        )
        bm25_config = _bm25_config_for_language(
            language,
            tokenizer_policy=args.bm25_tokenizer,
            top_k=args.bm25_top_k,
        )
        result = build_nano_dataset_from_rows(
            output_dir=args.output_dir,
            dataset_name="NanoMIRACL",
            dataset_id="hakari-bench/NanoMIRACL",
            split_name=language,
            corpus_rows=split_input.corpus,
            query_rows=split_input.queries,
            qrels_rows=split_input.qrels,
            query_limit=args.query_limit,
            doc_limit=args.doc_limit,
            bm25_config=bm25_config,
            metadata={
                "language": "multilingual",
                "languages": list(args.languages),
                "description": (
                    "NanoMIRACL rebuilt from hotchpotch/miracl-hf-unified dev queries, preserving all "
                    "source positive passages for each sampled query and using source negatives as hard "
                    "negative corpus candidates before random corpus fill."
                ),
                "source_benchmark_name": "MIRACL",
                "source_dataset_id": args.source_dataset_id,
                "source_dataset_revision": source_revision,
                "source_dataset_subset": f"{language}_queries",
                "source_eval_split": args.eval_split,
                "source_split_policy": f"Use `{args.eval_split}` from `{language}_queries` for each language.",
                "source_query_selection_policy": (
                    f"Take the first {args.query_limit} queries with at least one source positive; fewer if "
                    "the source split has fewer eligible queries."
                ),
                "corpus_fill_policy": (
                    "Include all selected positive documents, then source negatives balanced by query with "
                    "round-robin selection, then fill remaining corpus slots with deterministic random corpus "
                    "samples excluding already selected source row indices."
                ),
                "source_hard_negative_note": (
                    "The source `negatives` arrays are used as hard-negative corpus candidates. If positives "
                    "plus negatives exceed the document cap, negatives are selected round-robin across queries "
                    "to avoid one query dominating the corpus."
                ),
                "qrels_score_policy_note": (
                    "Every source `positives` entry for a selected query is written as a positive qrel; source "
                    "`negatives` are used only for corpus construction and are not written as positive qrels."
                ),
                "bm25_score_notes": (
                    "BM25 is computed over the rebuilt 10k-document split-local corpus with all positive qrels "
                    "per query. The published `bm25` config stores top-100 candidates."
                ),
                "source_dataset_location": args.source_dataset_id,
                "source_links": [
                    f"https://huggingface.co/datasets/{args.source_dataset_id}",
                    "https://huggingface.co/datasets/miracl/miracl",
                    "https://huggingface.co/datasets/miracl/miracl-corpus",
                ],
            },
        )
        row = {
            "split_name": language,
            "queries": result.queries,
            "corpus": result.corpus,
            "qrels": result.qrels,
            "bm25_tokenizer": bm25_config.tokenizer,
            "bm25_tokenizer_name": bm25_config.tokenizer_name,
            "bm25_stemmer_algorithm": bm25_config.stemmer_algorithm,
            "source_query_count": split_input.source_query_count,
            "selected_positive_source_indices": split_input.selected_positive_indices,
            "selected_hard_negative_source_indices": split_input.selected_hard_negative_indices,
            "random_fill_source_indices": split_input.random_fill_indices,
            "forced_doc_count": result.forced_doc_count,
            "missing_positive_doc_count_after_forcing": result.missing_positive_doc_count_after_forcing,
            "bm25_ndcg_at_10": result.bm25_ndcg_at_10,
        }
        summary_rows.append(row)
        print(json.dumps(row, ensure_ascii=False, sort_keys=True))

    _write_summary(
        args.output_dir, args.source_dataset_id, source_revision, summary_rows
    )


def _parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Rebuild local NanoMIRACL from hotchpotch/miracl-hf-unified."
    )
    parser.add_argument("--source-dataset-id", default=DEFAULT_SOURCE_DATASET_ID)
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_OUTPUT_DIR)
    parser.add_argument("--languages", nargs="+", default=list(LANGUAGES))
    parser.add_argument("--eval-split", default="dev")
    parser.add_argument("--query-limit", type=int, default=200)
    parser.add_argument("--doc-limit", type=int, default=10_000)
    parser.add_argument("--seed", type=int, default=13)
    parser.add_argument("--random-fill-oversample", type=int, default=2_000)
    parser.add_argument(
        "--bm25-tokenizer",
        default="language",
        help=(
            "`language` selects wordseg/stemmer/english_porter_stop/regex by NanoMIRACL language. "
            "Any other value is passed through as an explicit BM25 tokenizer."
        ),
    )
    parser.add_argument("--bm25-top-k", type=int, default=DEFAULT_BM25_TOP_K)
    args = parser.parse_args()
    unknown = sorted(set(args.languages) - set(LANGUAGES))
    if unknown:
        raise SystemExit(f"Unknown NanoMIRACL languages: {', '.join(unknown)}")
    if args.query_limit <= 0:
        raise SystemExit("--query-limit must be positive")
    if args.doc_limit <= 0:
        raise SystemExit("--doc-limit must be positive")
    if args.random_fill_oversample < 0:
        raise SystemExit("--random-fill-oversample must be non-negative")
    return args


def _bm25_config_for_language(
    language: str, *, tokenizer_policy: str, top_k: int
) -> BM25Config:
    if tokenizer_policy != "language":
        return BM25Config(tokenizer=tokenizer_policy, top_k=top_k)
    if language in WORDSEG_LANGUAGES:
        return BM25Config(tokenizer="wordseg", tokenizer_name=language, top_k=top_k)
    if language == "en":
        return BM25Config(tokenizer="english_porter_stop", top_k=top_k)
    if language in WHITESPACE_LANGUAGES:
        return BM25Config(tokenizer="whitespace", top_k=top_k)
    stemmer_algorithm = STEMMER_ALGORITHMS_BY_LANGUAGE.get(language)
    if stemmer_algorithm is not None:
        return BM25Config(
            tokenizer="stemmer",
            stemmer_algorithm=stemmer_algorithm,
            top_k=top_k,
        )
    return BM25Config(tokenizer="regex", top_k=top_k)


def _load_split_input(
    *,
    source_dataset_id: str,
    language: str,
    eval_split: str,
    query_limit: int,
    doc_limit: int,
    seed: int,
    random_fill_oversample: int,
) -> SplitInput:
    query_dataset = load_dataset(
        source_dataset_id, f"{language}_queries", split=eval_split
    )
    corpus_dataset = load_dataset(
        source_dataset_id, f"{language}_corpus", split="train"
    )
    source_queries = _select_source_queries(query_dataset, query_limit=query_limit)
    positive_indices, negative_indices = _select_relevant_source_indices(
        source_queries, doc_limit=doc_limit
    )
    random_fill_indices = _sample_random_fill_indices(
        corpus_size=len(corpus_dataset),
        excluded_indices=set(positive_indices) | set(negative_indices),
        target_count=max(
            doc_limit - len(set(positive_indices) | set(negative_indices)), 0
        ),
        oversample=random_fill_oversample,
        seed=_language_seed(seed, language),
    )

    ordered_indices = _unique_preserving_order(
        [*positive_indices, *negative_indices, *random_fill_indices]
    )
    corpus_by_index = _load_corpus_rows_by_index(corpus_dataset, ordered_indices)
    qrels_rows = _qrels_rows(
        source_queries, corpus_by_index, selected_negative_indices=set(negative_indices)
    )

    return SplitInput(
        queries=[
            {"_id": str(row["query_id"]), "text": str(row["query"])}
            for row in source_queries
        ],
        corpus=[
            corpus_by_index[index]
            for index in ordered_indices
            if index in corpus_by_index
        ],
        qrels=qrels_rows,
        selected_positive_indices=len(set(positive_indices)),
        selected_hard_negative_indices=len(set(negative_indices)),
        random_fill_indices=len(random_fill_indices),
        source_query_count=len(query_dataset),
    )


def _select_source_queries(
    query_dataset: Dataset, *, query_limit: int
) -> list[dict[str, Any]]:
    selected: list[dict[str, Any]] = []
    seen_ids: set[str] = set()
    seen_texts: set[str] = set()
    for row in query_dataset:
        query_id = str(row["query_id"])
        query_text = str(row["query"])
        positives = [int(value) for value in row.get("positives", [])]
        if not positives or query_id in seen_ids or query_text in seen_texts:
            continue
        selected.append(
            {
                "query_id": query_id,
                "query": query_text,
                "positives": positives,
                "negatives": [int(value) for value in row.get("negatives", [])],
            }
        )
        seen_ids.add(query_id)
        seen_texts.add(query_text)
        if len(selected) >= query_limit:
            break
    return selected


def _select_relevant_source_indices(
    source_queries: list[dict[str, Any]], *, doc_limit: int
) -> tuple[list[int], list[int]]:
    positive_indices = _unique_preserving_order(
        index for row in source_queries for index in row["positives"]
    )
    selected_positive_set = set(positive_indices)
    remaining_slots = max(doc_limit - len(selected_positive_set), 0)
    if remaining_slots <= 0:
        return positive_indices[:doc_limit], []

    negatives_by_query: dict[str, list[int]] = defaultdict(list)
    for row in source_queries:
        query_id = str(row["query_id"])
        for index in row["negatives"]:
            if index in selected_positive_set or index in negatives_by_query[query_id]:
                continue
            negatives_by_query[query_id].append(index)

    negative_indices: list[int] = []
    selected_negative_set: set[int] = set()
    round_index = 0
    query_ids = sorted(negatives_by_query)
    while len(selected_negative_set) < remaining_slots:
        added = False
        for query_id in query_ids:
            values = negatives_by_query[query_id]
            if round_index >= len(values):
                continue
            candidate = values[round_index]
            if candidate not in selected_negative_set:
                selected_negative_set.add(candidate)
                negative_indices.append(candidate)
                added = True
                if len(selected_negative_set) >= remaining_slots:
                    break
        if not added:
            break
        round_index += 1
    return positive_indices, negative_indices


def _sample_random_fill_indices(
    *,
    corpus_size: int,
    excluded_indices: set[int],
    target_count: int,
    oversample: int,
    seed: int,
) -> list[int]:
    if target_count <= 0:
        return []
    rng = random.Random(seed)
    selected: list[int] = []
    selected_set: set[int] = set()
    desired = min(
        target_count + oversample, max(corpus_size - len(excluded_indices), 0)
    )
    while len(selected) < desired:
        candidate = rng.randrange(corpus_size)
        if candidate in excluded_indices or candidate in selected_set:
            continue
        selected_set.add(candidate)
        selected.append(candidate)
    return selected


def _load_corpus_rows_by_index(
    corpus_dataset: Dataset, indices: list[int]
) -> dict[int, dict[str, str]]:
    if not indices:
        return {}
    sorted_indices = sorted(set(indices))
    rows = corpus_dataset.select(sorted_indices)
    output: dict[int, dict[str, str]] = {}
    for source_index, row in zip(sorted_indices, rows, strict=True):
        output[source_index] = {
            "_id": str(row["docid"]),
            "title": str(row.get("title") or ""),
            "text": str(row.get("text") or ""),
        }
    return output


def _qrels_rows(
    source_queries: list[dict[str, Any]],
    corpus_by_index: dict[int, dict[str, str]],
    *,
    selected_negative_indices: set[int],
) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    seen: set[tuple[str, str, int]] = set()
    for query in source_queries:
        query_id = str(query["query_id"])
        for index in query["positives"]:
            corpus = corpus_by_index.get(index)
            if corpus is None:
                continue
            key = (query_id, corpus["_id"], 1)
            if key not in seen:
                seen.add(key)
                rows.append(
                    {"query-id": query_id, "corpus-id": corpus["_id"], "score": 1}
                )
        for index in query["negatives"]:
            if index not in selected_negative_indices:
                continue
            corpus = corpus_by_index.get(index)
            if corpus is None:
                continue
            key = (query_id, corpus["_id"], 0)
            if key not in seen:
                seen.add(key)
                rows.append(
                    {"query-id": query_id, "corpus-id": corpus["_id"], "score": 0}
                )
    return rows


def _unique_preserving_order(values: Any) -> list[Any]:
    seen: set[Any] = set()
    output: list[Any] = []
    for value in values:
        if value in seen:
            continue
        seen.add(value)
        output.append(value)
    return output


def _language_seed(seed: int, language: str) -> int:
    return seed * 10_000 + sum(
        (index + 1) * ord(char) for index, char in enumerate(language)
    )


def _write_summary(
    output_dir: Path,
    source_dataset_id: str,
    source_revision: str,
    rows: list[dict[str, Any]],
) -> None:
    payload = {
        "source_dataset_id": source_dataset_id,
        "source_dataset_revision": source_revision,
        "rows": rows,
        "query_weighted_bm25_ndcg_at_10": _weighted_mean(
            rows, "bm25_ndcg_at_10", "queries"
        ),
        "unweighted_bm25_ndcg_at_10": sum(float(row["bm25_ndcg_at_10"]) for row in rows)
        / len(rows)
        if rows
        else 0.0,
    }
    (output_dir / "nanomiracl_unified_rebuild_summary.json").write_text(
        json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )


def _weighted_mean(
    rows: list[dict[str, Any]], value_key: str, weight_key: str
) -> float:
    total_weight = sum(int(row[weight_key]) for row in rows)
    if total_weight <= 0:
        return 0.0
    return (
        sum(float(row[value_key]) * int(row[weight_key]) for row in rows) / total_weight
    )


if __name__ == "__main__":
    main()
