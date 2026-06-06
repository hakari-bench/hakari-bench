from __future__ import annotations

import math
from collections.abc import Iterable
from collections.abc import Sequence

DEFAULT_ACC_K = [100]
DEFAULT_PRECISION_RECALL_K: list[int] = []
DEFAULT_MRR_K: list[int] = []
DEFAULT_NDCG_K = [10]
DEFAULT_MAP_K: list[int] = []
SUPPORTED_IR_METRIC_FAMILIES = ("acc", "accuracy", "hit", "precision", "recall", "mrr", "ndcg", "map")


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
    requested_cutoffs = sorted({cutoff for cutoffs in requested_metrics.values() for cutoff in cutoffs})
    if not requested_cutoffs:
        return {}
    max_cutoff = requested_cutoffs[-1]
    metric_sums = {
        f"{family}@{cutoff}": 0.0
        for family, cutoffs in requested_metrics.items()
        if family not in {"accuracy", "hit"}
        for cutoff in cutoffs
    }
    ideal_dcg_cache: dict[tuple[int, int], float] = {}
    empty_relevant: set[str] = set()

    for query_id in query_ids:
        ranking = rankings[query_id]
        relevant_docs = qrels.get(query_id, empty_relevant)
        relevant_count = len(relevant_docs)
        cutoff_values = _ranking_cutoff_values(
            ranking=ranking,
            relevant_docs=relevant_docs,
            relevant_count=relevant_count,
            max_cutoff=max_cutoff,
            requested_cutoffs=requested_cutoffs,
            ideal_dcg_cache=ideal_dcg_cache,
        )
        for metric_name in metric_sums:
            family, cutoff_text = metric_name.split("@", 1)
            metric_sums[metric_name] += cutoff_values[family][int(cutoff_text)]

    query_count = float(len(query_ids))
    metrics = {metric_name: metric_sum / query_count for metric_name, metric_sum in metric_sums.items()}

    return {f"{evaluator_name}_{score_name}_{key}": value for key, value in metrics.items()}


def _ranking_cutoff_values(
    *,
    ranking: list[str],
    relevant_docs: set[str],
    relevant_count: int,
    max_cutoff: int,
    requested_cutoffs: Sequence[int],
    ideal_dcg_cache: dict[tuple[int, int], float],
) -> dict[str, dict[int, float]]:
    seen_relevant: set[str] = set()
    unique_hits = 0
    hit_count = 0
    dcg = 0.0
    average_precision_sum = 0.0
    first_hit_rank: int | None = None
    values = {family: {} for family in ("acc", "precision", "recall", "mrr", "ndcg", "map")}
    cutoff_index = 0

    def record(cutoff: int) -> None:
        values["acc"][cutoff] = 1.0 if unique_hits else 0.0
        values["precision"][cutoff] = unique_hits / float(cutoff)
        values["recall"][cutoff] = unique_hits / float(relevant_count) if relevant_count else 0.0
        values["mrr"][cutoff] = 1.0 / float(first_hit_rank) if first_hit_rank is not None and first_hit_rank <= cutoff else 0.0
        ideal = _ideal_dcg(relevant_count, cutoff, ideal_dcg_cache)
        values["ndcg"][cutoff] = dcg / ideal if ideal else 0.0
        denominator = min(relevant_count, cutoff)
        values["map"][cutoff] = average_precision_sum / float(denominator) if denominator and hit_count else 0.0

    for index, doc_id in enumerate(ranking[:max_cutoff], start=1):
        if doc_id in relevant_docs:
            hit_count += 1
            if first_hit_rank is None:
                first_hit_rank = index
            if doc_id not in seen_relevant:
                seen_relevant.add(doc_id)
                unique_hits += 1
            dcg += 1.0 / math.log2(index + 1)
            average_precision_sum += hit_count / float(index)
        while cutoff_index < len(requested_cutoffs) and requested_cutoffs[cutoff_index] == index:
            record(requested_cutoffs[cutoff_index])
            cutoff_index += 1
    while cutoff_index < len(requested_cutoffs):
        record(requested_cutoffs[cutoff_index])
        cutoff_index += 1
    return values


def _ideal_dcg(relevant_count: int, cutoff: int, cache: dict[tuple[int, int], float]) -> float:
    key = (relevant_count, cutoff)
    if key not in cache:
        cache[key] = _dcg([1] * min(relevant_count, cutoff)) if relevant_count else 0.0
    return cache[key]


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
        canonical_family = "acc" if family in {"accuracy", "hit"} else family
        canonical = f"{canonical_family}@{cutoff}"
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
            "acc": tuple(DEFAULT_ACC_K),
            "accuracy": (),
            "hit": (),
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
