from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from hakari_bench.bm25 import (
    BM25Config,
    bm25_config_payload,
    rank_bm25_candidates,
    rankings_to_candidate_rows,
    resolve_bm25_config_for_queries,
)
from hakari_bench.metrics import compute_ir_metrics
from hakari_bench.nano_dataset_builder import (
    force_qrels_positives_into_rankings,
    normalize_corpus_rows,
    normalize_qrels_rows,
    normalize_query_rows,
)
from hakari_bench.scoring import candidate_coverage_for_qrels


@dataclass(frozen=True)
class RebuiltBm25Split:
    candidate_rows: list[dict[str, Any]]
    qrels_rows: list[dict[str, str]] | None
    metadata: dict[str, Any]


def rebuild_bm25_candidate_rows(
    *,
    corpus_rows: list[dict[str, Any]],
    query_rows: list[dict[str, Any]],
    qrels_rows: list[dict[str, Any]],
    split_name: str,
    bm25_config: BM25Config,
    task_metadata: dict[str, Any] | None = None,
    cap_qrels_to_top_k: bool = False,
    require_full_coverage: bool = True,
) -> RebuiltBm25Split:
    corpus = normalize_corpus_rows(corpus_rows)
    queries = normalize_query_rows(query_rows)
    positive_qrels, non_positive_qrels = normalize_qrels_rows(qrels_rows)
    query_map = {row["_id"]: row["text"] for row in queries}
    corpus_map = {row["_id"]: row["text"] for row in corpus}
    resolved_bm25_config = resolve_bm25_config_for_queries(bm25_config, query_map, metadata=task_metadata)
    qrels_selection: dict[str, int | str] | None = None
    if cap_qrels_to_top_k:
        positive_qrels, qrels_selection = _cap_qrels_per_query(
            positive_qrels,
            limit=resolved_bm25_config.top_k,
        )
    qrels_map = _qrels_mapping(positive_qrels)

    over_cap = _qrels_over_candidate_cap(qrels_map, top_k=resolved_bm25_config.top_k)
    if over_cap:
        examples = ", ".join(f"{query_id}={count}" for query_id, count in over_cap[:5])
        raise ValueError(
            f"{split_name} has qrels-positive counts above BM25 top_k={resolved_bm25_config.top_k}: {examples}. "
            "Relevant coverage cannot be 100% unless qrels are capped or top_k is increased."
        )

    raw_rankings = rank_bm25_candidates(corpus=corpus_map, queries=query_map, config=resolved_bm25_config)
    rankings, forcing_metadata = force_qrels_positives_into_rankings(
        rankings=raw_rankings,
        qrels=qrels_map,
        top_k=resolved_bm25_config.top_k,
    )
    coverage = candidate_coverage_for_qrels(
        qrels=qrels_map,
        candidates=rankings,
        top_k=resolved_bm25_config.top_k,
    )
    if require_full_coverage and (
        coverage.get("query_coverage") != 1.0 or coverage.get("relevant_coverage") != 1.0
    ):
        raise RuntimeError(
            f"{split_name} BM25 coverage is not complete after positive forcing: "
            f"query_coverage={coverage.get('query_coverage')}, "
            f"relevant_coverage={coverage.get('relevant_coverage')}."
        )

    metrics = compute_ir_metrics(
        rankings=rankings,
        qrels=qrels_map,
        evaluator_name=split_name,
        score_name="bm25_bm25s_okapi",
    )
    ndcg_key = f"{split_name}_bm25_bm25s_okapi_ndcg@10"
    metadata: dict[str, Any] = {
        "split_name": split_name,
        "queries": len(queries),
        "corpus": len(corpus),
        "qrels": len(positive_qrels),
        "source_non_positive_qrels": len(non_positive_qrels),
        "bm25": {
            "config": bm25_config_payload(resolved_bm25_config),
            "ndcg_at_10": float(metrics.get(ndcg_key, 0.0)),
            "candidate_coverage": coverage,
            "rebuild_policy": (
                "BM25 candidates were recomputed locally and qrels-positive documents missing "
                "from the raw top-k were forced into the final candidate list."
            ),
            **forcing_metadata,
        },
    }
    if qrels_selection is not None:
        metadata["qrels_selection"] = qrels_selection
    return RebuiltBm25Split(
        candidate_rows=rankings_to_candidate_rows(rankings),
        qrels_rows=positive_qrels if cap_qrels_to_top_k else None,
        metadata=metadata,
    )


def _qrels_mapping(qrels: list[dict[str, str]]) -> dict[str, set[str]]:
    output: dict[str, set[str]] = {}
    for row in qrels:
        output.setdefault(row["query-id"], set()).add(row["corpus-id"])
    return output


def _qrels_over_candidate_cap(qrels: dict[str, set[str]], *, top_k: int) -> list[tuple[str, int]]:
    return sorted(
        ((query_id, len(corpus_ids)) for query_id, corpus_ids in qrels.items() if len(corpus_ids) > top_k),
        key=lambda item: (-item[1], item[0]),
    )


def _cap_qrels_per_query(
    qrels: list[dict[str, str]],
    *,
    limit: int,
) -> tuple[list[dict[str, str]], dict[str, int | str]]:
    counts: dict[str, int] = {}
    capped: list[dict[str, str]] = []
    removed = 0
    for row in qrels:
        query_id = row["query-id"]
        count = counts.get(query_id, 0)
        if count >= limit:
            removed += 1
            continue
        counts[query_id] = count + 1
        capped.append(row)
    return capped, {
        "qrels_per_query_cap": limit,
        "removed_qrels_over_cap": removed,
        "qrels_cap_policy": "positive qrels are capped per query to the BM25 candidate top_k",
    }
