from __future__ import annotations

import math
from collections.abc import Iterable
from collections.abc import Sequence

DEFAULT_ACCURACY_K = [1, 3, 5, 10]
DEFAULT_PRECISION_RECALL_K = [1, 3, 5, 10]
DEFAULT_MRR_K = [10]
DEFAULT_NDCG_K = [10]
DEFAULT_MAP_K = [100]
SUPPORTED_IR_METRIC_FAMILIES = ("accuracy", "precision", "recall", "mrr", "ndcg", "map")


def compute_ir_metrics(
    *,
    rankings: dict[str, list[str]],
    qrels: dict[str, set[str]],
    evaluator_name: str,
    score_name: str,
    metric_names: Sequence[str] | None = None,
) -> dict[str, float]:
    query_ids = list(rankings)
    if not query_ids:
        return {}

    requested_metrics = _requested_metric_groups(metric_names)
    metrics: dict[str, float] = {}
    for k_value in requested_metrics["accuracy"]:
        metrics[f"accuracy@{k_value}"] = _mean(
            1.0 if _hits_at_k(rankings[query_id], qrels.get(query_id, set()), k_value) else 0.0
            for query_id in query_ids
        )

    for k_value in requested_metrics["precision"]:
        metrics[f"precision@{k_value}"] = _mean(
            _precision_at_k(rankings[query_id], qrels.get(query_id, set()), k_value) for query_id in query_ids
        )
    for k_value in requested_metrics["recall"]:
        metrics[f"recall@{k_value}"] = _mean(
            _recall_at_k(rankings[query_id], qrels.get(query_id, set()), k_value) for query_id in query_ids
        )

    for k_value in requested_metrics["mrr"]:
        metrics[f"mrr@{k_value}"] = _mean(
            _reciprocal_rank_at_k(rankings[query_id], qrels.get(query_id, set()), k_value) for query_id in query_ids
        )

    for k_value in requested_metrics["ndcg"]:
        metrics[f"ndcg@{k_value}"] = _mean(
            _ndcg_at_k(rankings[query_id], qrels.get(query_id, set()), k_value) for query_id in query_ids
        )

    for k_value in requested_metrics["map"]:
        metrics[f"map@{k_value}"] = _mean(
            _average_precision_at_k(rankings[query_id], qrels.get(query_id, set()), k_value) for query_id in query_ids
        )

    return {f"{evaluator_name}_{score_name}_{key}": value for key, value in metrics.items()}


def normalize_ir_metric_names(metric_names: Sequence[str]) -> tuple[str, ...]:
    """Return canonical lower-case IR metric names such as ``("ndcg@10",)``."""

    normalized: list[str] = []
    seen: set[str] = set()
    for metric_name in metric_names:
        metric = metric_name.strip().lower()
        if "@" not in metric:
            raise ValueError(f"IR metric must include a cutoff, for example 'nDCG@10': {metric_name!r}.")
        family, cutoff_text = metric.split("@", 1)
        if family not in SUPPORTED_IR_METRIC_FAMILIES:
            supported = ", ".join(SUPPORTED_IR_METRIC_FAMILIES)
            raise ValueError(f"Unsupported IR metric family {family!r}. Supported families are: {supported}.")
        try:
            cutoff = int(cutoff_text)
        except ValueError as exc:
            raise ValueError(f"IR metric cutoff must be an integer: {metric_name!r}.") from exc
        if cutoff <= 0:
            raise ValueError(f"IR metric cutoff must be positive: {metric_name!r}.")
        canonical = f"{family}@{cutoff}"
        if canonical in seen:
            continue
        seen.add(canonical)
        normalized.append(canonical)
    if not normalized:
        raise ValueError("At least one IR metric must be requested.")
    return tuple(normalized)


def _requested_metric_groups(metric_names: Sequence[str] | None) -> dict[str, tuple[int, ...]]:
    if metric_names is None:
        return {
            "accuracy": tuple(DEFAULT_ACCURACY_K),
            "precision": tuple(DEFAULT_PRECISION_RECALL_K),
            "recall": tuple(DEFAULT_PRECISION_RECALL_K),
            "mrr": tuple(DEFAULT_MRR_K),
            "ndcg": tuple(DEFAULT_NDCG_K),
            "map": tuple(DEFAULT_MAP_K),
        }

    grouped: dict[str, list[int]] = {family: [] for family in SUPPORTED_IR_METRIC_FAMILIES}
    for metric in normalize_ir_metric_names(metric_names):
        family, cutoff_text = metric.split("@", 1)
        grouped[family].append(int(cutoff_text))
    return {family: tuple(cutoffs) for family, cutoffs in grouped.items()}


def _mean(values: Iterable[float]) -> float:
    materialized = list(values)
    return float(sum(materialized) / len(materialized)) if materialized else 0.0


def _hits_at_k(ranking: list[str], relevant_docs: set[str], k_value: int) -> bool:
    return bool(set(ranking[:k_value]) & relevant_docs)


def _precision_at_k(ranking: list[str], relevant_docs: set[str], k_value: int) -> float:
    if k_value <= 0:
        return 0.0
    return len(set(ranking[:k_value]) & relevant_docs) / float(k_value)


def _recall_at_k(ranking: list[str], relevant_docs: set[str], k_value: int) -> float:
    if not relevant_docs:
        return 0.0
    return len(set(ranking[:k_value]) & relevant_docs) / float(len(relevant_docs))


def _reciprocal_rank_at_k(ranking: list[str], relevant_docs: set[str], k_value: int) -> float:
    for index, doc_id in enumerate(ranking[:k_value], start=1):
        if doc_id in relevant_docs:
            return 1.0 / float(index)
    return 0.0


def _dcg(relevances: list[int]) -> float:
    return sum(rel / math.log2(index + 2) for index, rel in enumerate(relevances))


def _ndcg_at_k(ranking: list[str], relevant_docs: set[str], k_value: int) -> float:
    if not relevant_docs:
        return 0.0
    relevances = [1 if doc_id in relevant_docs else 0 for doc_id in ranking[:k_value]]
    ideal_relevances = [1] * min(len(relevant_docs), k_value)
    ideal = _dcg(ideal_relevances)
    if ideal == 0.0:
        return 0.0
    return _dcg(relevances) / ideal


def _average_precision_at_k(ranking: list[str], relevant_docs: set[str], k_value: int) -> float:
    if not relevant_docs:
        return 0.0
    hit_count = 0
    precision_sum = 0.0
    for index, doc_id in enumerate(ranking[:k_value], start=1):
        if doc_id not in relevant_docs:
            continue
        hit_count += 1
        precision_sum += hit_count / float(index)
    return precision_sum / float(min(len(relevant_docs), k_value))
