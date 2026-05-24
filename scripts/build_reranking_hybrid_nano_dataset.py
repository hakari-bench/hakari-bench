from __future__ import annotations

import argparse
import json
import random
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import torch
import yaml
from datasets import Dataset, get_dataset_split_names, load_dataset
from sentence_transformers import SentenceTransformer

from hakari_bench.bm25 import BM25Config, rank_bm25_candidates, resolve_bm25_config_for_queries

SOURCE_DATASET = "hakari-bench/NanoMMTEB-v2"
HARRIER_MODEL_ID = "microsoft/harrier-oss-v1-270m"
HARRIER_QUERY_PROMPT_NAME = "web_search_query"
HARRIER_CONFIG_NAME = "harrier_oss_v1_270m"
HYBRID_CONFIG_NAME = "reranking_hybrid"


def main() -> None:
    args = parse_args()
    build_dataset(
        source_dataset=args.source_dataset,
        output_dir=Path(args.output_dir),
        splits=args.splits,
        harrier_model=args.harrier_model,
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


def build_dataset(
    *,
    source_dataset: str,
    output_dir: Path,
    splits: list[str] | None,
    harrier_model: str = HARRIER_MODEL_ID,
    model: SentenceTransformer | None = None,
    device: str = "cpu",
    batch_size: int = 64,
    dense_score_batch_size: int = 64,
    bm25_top_k: int = 100,
    dense_top_k: int = 100,
    hybrid_top_k: int = 101,
    rrf_k: int = 60,
    seed: int = 20260524,
    overwrite: bool = False,
    show_progress: bool = False,
) -> dict[str, Any]:
    output_dir = Path(output_dir)
    if output_dir.exists() and not overwrite:
        raise SystemExit(f"Output directory already exists: {output_dir}. Pass --overwrite to replace it.")
    output_dir.mkdir(parents=True, exist_ok=True)

    resolved_splits = splits or get_dataset_split_names(source_dataset, "queries")
    model = model or SentenceTransformer(harrier_model, device=device)
    prompts = getattr(model, "prompts", {}) or {}
    if HARRIER_QUERY_PROMPT_NAME not in prompts:
        raise ValueError(
            f"{harrier_model} does not expose the required {HARRIER_QUERY_PROMPT_NAME!r} prompt. "
            f"Available prompts: {sorted(prompts)}"
        )

    metadata: dict[str, Any] = {
        "generated_at_utc": datetime.now(timezone.utc).isoformat(),
        "source_dataset": source_dataset,
        "configs": {
            "bm25": {"top_k": bm25_top_k, "tokenizer": "auto"},
            HARRIER_CONFIG_NAME: {
                "model": harrier_model,
                "top_k": dense_top_k,
                "query_prompt_name": HARRIER_QUERY_PROMPT_NAME,
                "query_prompt": prompts[HARRIER_QUERY_PROMPT_NAME],
                "document_prompt_name": None,
            },
            HYBRID_CONFIG_NAME: {
                "top_k": hybrid_top_k,
                "method": "reciprocal_rank_fusion",
                "rrf_k": rrf_k,
                "random_seed": seed,
            },
        },
        "splits": {},
    }

    for split in resolved_splits:
        split_metadata = build_split(
            source_dataset=source_dataset,
            split=split,
            output_dir=output_dir,
            model=model,
            bm25_top_k=bm25_top_k,
            dense_top_k=dense_top_k,
            hybrid_top_k=hybrid_top_k,
            rrf_k=rrf_k,
            seed=seed,
            batch_size=batch_size,
            dense_score_batch_size=dense_score_batch_size,
            show_progress=show_progress,
        )
        metadata["splits"][split] = split_metadata
        print(
            f"{split}: corpus={split_metadata['corpus_count']} queries={split_metadata['query_count']} "
            f"hybrid_min={split_metadata['reranking_hybrid']['candidate_count_min']} "
            f"hybrid_max={split_metadata['reranking_hybrid']['candidate_count_max']} "
            f"coverage={split_metadata['reranking_hybrid']['query_coverage']:.4f}"
        )

    write_dataset_readme(output_dir=output_dir, splits=resolved_splits, metadata=metadata)
    metadata_path = output_dir / "reranking_hybrid_metadata.json"
    metadata_path.write_text(json.dumps(metadata, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    audit_dataset(output_dir=output_dir, splits=resolved_splits, metadata=metadata)
    print(f"Wrote {output_dir}")
    return metadata


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Build Nano reranking_hybrid candidate subsets.")
    parser.add_argument("--source-dataset", default=SOURCE_DATASET)
    parser.add_argument("--output-dir", default="output/nano_reranking_hybrid/NanoMMTEB-v2")
    parser.add_argument("--split", dest="splits", action="append", default=None)
    parser.add_argument("--harrier-model", default=HARRIER_MODEL_ID)
    parser.add_argument("--device", default="cuda:0" if torch.cuda.is_available() else "cpu")
    parser.add_argument("--batch-size", type=int, default=64)
    parser.add_argument("--dense-score-batch-size", type=int, default=64)
    parser.add_argument("--bm25-top-k", type=int, default=100)
    parser.add_argument("--dense-top-k", type=int, default=100)
    parser.add_argument("--hybrid-top-k", type=int, default=101)
    parser.add_argument("--rrf-k", type=int, default=60)
    parser.add_argument("--seed", type=int, default=20260524)
    parser.add_argument("--overwrite", action="store_true")
    parser.add_argument("--show-progress", action="store_true")
    return parser.parse_args()


def build_split(
    *,
    source_dataset: str,
    split: str,
    output_dir: Path,
    model: SentenceTransformer,
    bm25_top_k: int,
    dense_top_k: int,
    hybrid_top_k: int,
    rrf_k: int,
    seed: int,
    batch_size: int,
    dense_score_batch_size: int,
    show_progress: bool,
) -> dict[str, Any]:
    corpus_rows = list(load_dataset(source_dataset, "corpus", split=split))
    query_rows = list(load_dataset(source_dataset, "queries", split=split))
    qrel_rows = list(load_dataset(source_dataset, "qrels", split=split))
    corpus = {str(row["_id"]): str(row["text"]) for row in corpus_rows}
    queries = {str(row["_id"]): str(row["text"]) for row in query_rows}
    qrels = qrels_by_query(qrel_rows)

    write_config_split(output_dir, "corpus", split, corpus_rows)
    write_config_split(output_dir, "queries", split, query_rows)
    write_config_split(output_dir, "qrels", split, qrel_rows)

    bm25_config = resolve_bm25_config_for_queries(
        BM25Config(top_k=bm25_top_k, show_progress=show_progress),
        queries,
    )
    bm25_rankings = rank_bm25_candidates(corpus=corpus, queries=queries, config=bm25_config)
    dense_rankings = rank_harrier_candidates(
        model=model,
        corpus=corpus,
        queries=queries,
        top_k=dense_top_k,
        batch_size=batch_size,
        score_batch_size=dense_score_batch_size,
        show_progress=show_progress,
    )
    hybrid_rankings, hybrid_metadata = rrf_hybrid_rankings(
        query_ids=list(queries),
        corpus_ids=list(corpus),
        qrels=qrels,
        bm25_rankings=bm25_rankings,
        dense_rankings=dense_rankings,
        top_k=hybrid_top_k,
        rrf_k=rrf_k,
        seed=seed,
        split=split,
    )

    write_config_split(output_dir, "bm25", split, candidate_rows(bm25_rankings, query_ids=list(queries)))
    write_config_split(output_dir, HARRIER_CONFIG_NAME, split, candidate_rows(dense_rankings, query_ids=list(queries)))
    write_config_split(output_dir, HYBRID_CONFIG_NAME, split, candidate_rows(hybrid_rankings, query_ids=list(queries)))

    return {
        "corpus_count": len(corpus),
        "query_count": len(queries),
        "qrel_count": sum(len(values) for values in qrels.values()),
        "bm25": {
            "candidate_count_min": min_len(bm25_rankings),
            "candidate_count_max": max_len(bm25_rankings),
            "resolved_tokenizer": bm25_config.tokenizer,
            "resolved_tokenizer_name": bm25_config.tokenizer_name,
            "auto_detected_language": bm25_config.auto_detected_language,
            "auto_detection_language_counts": bm25_config.auto_detection_language_counts,
        },
        HARRIER_CONFIG_NAME: {
            "candidate_count_min": min_len(dense_rankings),
            "candidate_count_max": max_len(dense_rankings),
        },
        HYBRID_CONFIG_NAME: hybrid_metadata,
    }


def rank_harrier_candidates(
    *,
    model: SentenceTransformer,
    corpus: dict[str, str],
    queries: dict[str, str],
    top_k: int,
    batch_size: int,
    score_batch_size: int,
    show_progress: bool,
) -> dict[str, list[str]]:
    corpus_ids = list(corpus)
    query_ids = list(queries)
    doc_embeddings = model.encode(
        [corpus[corpus_id] for corpus_id in corpus_ids],
        batch_size=batch_size,
        show_progress_bar=show_progress,
        convert_to_tensor=True,
        normalize_embeddings=True,
    )
    query_embeddings = model.encode(
        [queries[query_id] for query_id in query_ids],
        batch_size=batch_size,
        show_progress_bar=show_progress,
        convert_to_tensor=True,
        normalize_embeddings=True,
        prompt_name=HARRIER_QUERY_PROMPT_NAME,
    )
    doc_embeddings = doc_embeddings.to(model.device)
    query_embeddings = query_embeddings.to(model.device)
    actual_top_k = max(1, min(top_k, len(corpus_ids)))
    rankings: dict[str, list[str]] = {}
    with torch.no_grad():
        for offset in range(0, len(query_ids), score_batch_size):
            query_chunk = query_embeddings[offset : offset + score_batch_size]
            scores = query_chunk @ doc_embeddings.T
            _values, indices = torch.topk(scores, k=actual_top_k, dim=1, largest=True, sorted=True)
            for query_id, row in zip(query_ids[offset : offset + score_batch_size], indices.cpu().tolist(), strict=True):
                rankings[query_id] = [corpus_ids[int(index)] for index in row]
    return rankings


def rrf_hybrid_rankings(
    *,
    query_ids: list[str],
    corpus_ids: list[str],
    qrels: dict[str, set[str]],
    bm25_rankings: dict[str, list[str]],
    dense_rankings: dict[str, list[str]],
    top_k: int,
    rrf_k: int,
    seed: int,
    split: str,
) -> tuple[dict[str, list[str]], dict[str, Any]]:
    corpus_set = set(corpus_ids)
    rankings: dict[str, list[str]] = {}
    forced_positive_count = 0
    random_filler_count = 0
    limited_by_corpus_count = 0
    covered_query_count = 0
    relevant_query_count = 0
    relevant_count = 0
    covered_relevant_count = 0
    additions: list[dict[str, Any]] = []

    for query_id in query_ids:
        scores: dict[str, float] = {}
        best_source_rank: dict[str, int] = {}
        for source_name, source_ranking in (
            ("bm25", bm25_rankings.get(query_id, [])),
            (HARRIER_CONFIG_NAME, dense_rankings.get(query_id, [])),
        ):
            for zero_rank, doc_id in enumerate(source_ranking):
                if doc_id not in corpus_set:
                    continue
                rank = zero_rank + 1
                scores[doc_id] = scores.get(doc_id, 0.0) + 1.0 / (rrf_k + rank)
                best_source_rank[doc_id] = min(best_source_rank.get(doc_id, rank), rank)

        ordered = sorted(scores, key=lambda doc_id: (-scores[doc_id], best_source_rank[doc_id], doc_id))
        ranking = ordered[: min(top_k, len(corpus_ids))]
        positives = [doc_id for doc_id in sorted(qrels.get(query_id, set())) if doc_id in corpus_set]
        if positives:
            relevant_query_count += 1
            relevant_count += len(positives)
        if positives and not set(ranking).intersection(positives):
            selected_positive = stable_random_choice(
                positives,
                seed=seed,
                split=split,
                query_id=query_id,
                reason="positive_safeguard",
            )
            ranking = add_or_replace_tail(ranking, selected_positive, top_k=top_k)
            forced_positive_count += 1
            additions.append(
                {
                    "query_id": query_id,
                    "reason": "positive_safeguard",
                    "corpus_id": selected_positive,
                }
            )
        elif len(ranking) < top_k and len(ranking) < len(corpus_ids):
            remaining = [doc_id for doc_id in corpus_ids if doc_id not in set(ranking)]
            selected_doc = stable_random_choice(
                remaining,
                seed=seed,
                split=split,
                query_id=query_id,
                reason="random_filler",
            )
            ranking.append(selected_doc)
            random_filler_count += 1
            additions.append({"query_id": query_id, "reason": "random_filler", "corpus_id": selected_doc})

        if len(ranking) < top_k and len(ranking) == len(corpus_ids):
            limited_by_corpus_count += 1
        rankings[query_id] = ranking
        covered = set(ranking).intersection(positives)
        if covered:
            covered_query_count += 1
            covered_relevant_count += len(covered)

    counts = [len(rankings[query_id]) for query_id in query_ids]
    return rankings, {
        "candidate_count_min": min(counts) if counts else 0,
        "candidate_count_max": max(counts) if counts else 0,
        "candidate_count_mean": sum(counts) / len(counts) if counts else 0.0,
        "query_with_relevance_count": relevant_query_count,
        "covered_query_count": covered_query_count,
        "query_coverage": covered_query_count / relevant_query_count if relevant_query_count else 0.0,
        "relevant_count": relevant_count,
        "covered_relevant_count": covered_relevant_count,
        "relevant_coverage": covered_relevant_count / relevant_count if relevant_count else 0.0,
        "forced_positive_count": forced_positive_count,
        "random_filler_count": random_filler_count,
        "limited_by_corpus_size_count": limited_by_corpus_count,
        "additions": additions,
    }


def add_or_replace_tail(ranking: list[str], doc_id: str, *, top_k: int) -> list[str]:
    if doc_id in ranking:
        return ranking[:top_k]
    if len(ranking) >= top_k:
        return [*ranking[: top_k - 1], doc_id]
    return [*ranking, doc_id]


def stable_random_choice(values: list[str], *, seed: int, split: str, query_id: str, reason: str) -> str:
    rng = random.Random(f"{seed}\0{split}\0{query_id}\0{reason}")
    return rng.choice(values)


def qrels_by_query(rows: list[dict[str, Any]]) -> dict[str, set[str]]:
    qrels: dict[str, set[str]] = {}
    for row in rows:
        query_id = str(row["query-id"])
        corpus_ids = row.get("corpus-id")
        qrels.setdefault(query_id, set())
        if isinstance(corpus_ids, list):
            qrels[query_id].update(str(corpus_id) for corpus_id in corpus_ids)
        else:
            qrels[query_id].add(str(corpus_ids))
    return qrels


def candidate_rows(rankings: dict[str, list[str]], *, query_ids: list[str]) -> list[dict[str, Any]]:
    return [{"query-id": query_id, "corpus-ids": rankings.get(query_id, [])} for query_id in query_ids]


def write_config_split(output_dir: Path, config_name: str, split: str, rows: list[dict[str, Any]]) -> None:
    path = output_dir / config_name / f"{split}.parquet"
    path.parent.mkdir(parents=True, exist_ok=True)
    Dataset.from_list(rows).to_parquet(str(path))


def write_dataset_readme(*, output_dir: Path, splits: list[str], metadata: dict[str, Any]) -> None:
    configs = []
    for config_name in ("corpus", "queries", "qrels", "bm25", HARRIER_CONFIG_NAME, HYBRID_CONFIG_NAME):
        configs.append(
            {
                "config_name": config_name,
                "data_files": [
                    {"split": split, "path": f"{config_name}/{split}.parquet"}
                    for split in splits
                ],
            }
        )
    frontmatter = yaml.safe_dump({"configs": configs}, sort_keys=False, allow_unicode=True)
    split_summaries = metadata["splits"]
    forced_count = sum(item[HYBRID_CONFIG_NAME]["forced_positive_count"] for item in split_summaries.values())
    filler_count = sum(item[HYBRID_CONFIG_NAME]["random_filler_count"] for item in split_summaries.values())
    limited_count = sum(item[HYBRID_CONFIG_NAME]["limited_by_corpus_size_count"] for item in split_summaries.values())
    readme = f"""---
{frontmatter}---
# NanoMMTEB-v2 reranking_hybrid

This local dataset was generated from `{metadata["source_dataset"]}` and is not uploaded to Hugging Face.

Candidate configs:

- `bm25`: locally recomputed BM25 top-100 with automatic language-aware tokenization. The tokenizer uses `wordseg` for supported detected languages and `regex` otherwise.
- `{HARRIER_CONFIG_NAME}`: dense top-100 from `{HARRIER_MODEL_ID}`. Queries use the SentenceTransformers `{HARRIER_QUERY_PROMPT_NAME}` prompt; documents use no prompt.
- `{HYBRID_CONFIG_NAME}`: top-101 Reciprocal Rank Fusion over `bm25` and `{HARRIER_CONFIG_NAME}`.

Hybrid construction notes:

- If no qrels-positive document appears in the hybrid top-101, position 101 is replaced with one deterministic random qrels-positive document.
- If RRF produces only 100 unique documents and the corpus has additional documents, one deterministic random filler document is appended.
- Some splits have fewer than 101 corpus documents; those candidate lists are limited by corpus size.

Random addition counts:

- Forced positives: {forced_count}
- Random fillers: {filler_count}
- Limited by corpus size: {limited_count}

Detailed per-split metadata is stored in `reranking_hybrid_metadata.json`.
"""
    (output_dir / "README.md").write_text(readme, encoding="utf-8")


def audit_dataset(*, output_dir: Path, splits: list[str], metadata: dict[str, Any]) -> None:
    errors: list[str] = []
    for split in splits:
        corpus_rows = list(load_dataset(str(output_dir), "corpus", split=split))
        query_rows = list(load_dataset(str(output_dir), "queries", split=split))
        qrel_rows = list(load_dataset(str(output_dir), "qrels", split=split))
        hybrid_rows = list(load_dataset(str(output_dir), HYBRID_CONFIG_NAME, split=split))
        corpus_ids = {str(row["_id"]) for row in corpus_rows}
        query_ids = {str(row["_id"]) for row in query_rows}
        qrels = qrels_by_query(qrel_rows)
        if {str(row["query-id"]) for row in hybrid_rows} != query_ids:
            errors.append(f"{split}: hybrid query ids do not match queries.")
        for row in hybrid_rows:
            query_id = str(row["query-id"])
            candidate_ids = [str(doc_id) for doc_id in row["corpus-ids"]]
            if len(candidate_ids) != len(set(candidate_ids)):
                errors.append(f"{split}/{query_id}: duplicate candidate ids.")
            missing = [doc_id for doc_id in candidate_ids if doc_id not in corpus_ids]
            if missing:
                errors.append(f"{split}/{query_id}: candidate ids missing from corpus: {missing[:3]}.")
            expected = min(101, len(corpus_ids))
            if len(candidate_ids) != expected:
                errors.append(f"{split}/{query_id}: expected {expected} candidates, got {len(candidate_ids)}.")
            positives = qrels.get(query_id, set()).intersection(corpus_ids)
            if positives and not positives.intersection(candidate_ids):
                errors.append(f"{split}/{query_id}: no qrels-positive candidate in hybrid list.")
        split_meta = metadata["splits"][split][HYBRID_CONFIG_NAME]
        if split_meta["query_coverage"] != 1.0:
            errors.append(f"{split}: hybrid query coverage is {split_meta['query_coverage']}.")
    if errors:
        raise RuntimeError("Dataset audit failed:\n" + "\n".join(errors[:50]))


def min_len(rankings: dict[str, list[str]]) -> int:
    return min((len(values) for values in rankings.values()), default=0)


def max_len(rankings: dict[str, list[str]]) -> int:
    return max((len(values) for values in rankings.values()), default=0)


if __name__ == "__main__":
    main()
