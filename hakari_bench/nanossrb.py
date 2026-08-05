from __future__ import annotations

from collections import Counter, defaultdict
from dataclasses import dataclass, replace
import hashlib
import json
import random
from typing import Literal


OverflowPolicy = Literal["drop-query", "cap-and-exclude"]


@dataclass(frozen=True)
class SSRBQuery:
    query_id: str
    text: str
    domain: str
    schema: str
    positive_doc_ids: tuple[str, ...]
    time_type: int
    exact_conditions: int
    semantic_conditions: int
    source_condition: str | None

    @property
    def strata(self) -> tuple[str, ...]:
        positive_count = len(self.positive_doc_ids)
        tags = [f"positive-count:{positive_count}"]
        tags.append("time:yes" if self.time_type else "time:no")
        tags.append(f"exact:{min(self.exact_conditions, 2)}")
        tags.append(f"semantic:{min(self.semantic_conditions, 2)}")
        return tuple(tags)


def stable_key(value: str, *, seed: int) -> str:
    return hashlib.sha256(f"{seed}:{value}".encode()).hexdigest()


def parse_source_condition(raw: object) -> tuple[int, int]:
    if raw is None:
        return 0, 0
    try:
        parsed = json.loads(str(raw))
    except (json.JSONDecodeError, TypeError, ValueError):
        return 0, 0
    if not isinstance(parsed, list):
        return 0, 0
    integers = [value for value in parsed if isinstance(value, int) and not isinstance(value, bool)]
    if len(integers) < 2:
        return 0, 0
    return max(0, integers[-2]), max(0, integers[-1])


def apply_positive_limit(
    queries: list[SSRBQuery],
    *,
    max_positives: int,
    overflow_policy: OverflowPolicy,
    seed: int = 17,
) -> tuple[list[SSRBQuery], set[str]]:
    if max_positives <= 0:
        raise ValueError("max_positives must be positive")
    if overflow_policy not in ("drop-query", "cap-and-exclude"):
        raise ValueError(f"unsupported overflow policy: {overflow_policy}")

    kept: list[SSRBQuery] = []
    excluded_doc_ids: set[str] = set()
    for query in queries:
        positives = tuple(dict.fromkeys(query.positive_doc_ids))
        if not positives:
            continue
        if len(positives) <= max_positives:
            kept.append(replace(query, positive_doc_ids=positives))
            continue
        if overflow_policy == "drop-query":
            continue
        ordered = sorted(positives, key=lambda doc_id: stable_key(f"{query.query_id}:{doc_id}", seed=seed))
        retained = tuple(ordered[:max_positives])
        excluded_doc_ids.update(ordered[max_positives:])
        kept.append(replace(query, positive_doc_ids=retained))
    return kept, excluded_doc_ids


def _rarity_score(query: SSRBQuery, counts: Counter[str]) -> float:
    return sum(1.0 / counts[tag] for tag in query.strata if counts[tag])


def condition_stratified_sample(
    queries: list[SSRBQuery],
    *,
    query_limit: int,
    min_per_schema: int = 2,
    seed: int = 17,
) -> list[SSRBQuery]:
    if query_limit <= 0:
        raise ValueError("query_limit must be positive")
    if min_per_schema < 0:
        raise ValueError("min_per_schema must not be negative")

    unique = {query.query_id: query for query in queries}
    candidates = list(unique.values())
    if len(candidates) <= query_limit:
        return sorted(candidates, key=lambda query: (query.schema, stable_key(query.query_id, seed=seed)))

    strata_counts = Counter(tag for query in candidates for tag in query.strata)
    by_schema: dict[str, list[SSRBQuery]] = defaultdict(list)
    for query in candidates:
        by_schema[query.schema].append(query)

    selected: list[SSRBQuery] = []
    selected_ids: set[str] = set()
    selected_strata: Counter[str] = Counter()

    def score(query: SSRBQuery) -> tuple[float, str]:
        uncovered = sum(1 for tag in query.strata if selected_strata[tag] == 0)
        balance = sum(1.0 / (selected_strata[tag] + 1) for tag in query.strata)
        return uncovered * 1000 + balance * 10 + _rarity_score(query, strata_counts), stable_key(
            query.query_id, seed=seed
        )

    for schema in sorted(by_schema):
        schema_candidates = by_schema[schema]
        for _ in range(min(min_per_schema, len(schema_candidates))):
            remaining = [query for query in schema_candidates if query.query_id not in selected_ids]
            if not remaining or len(selected) >= query_limit:
                break
            chosen = max(remaining, key=score)
            selected.append(chosen)
            selected_ids.add(chosen.query_id)
            selected_strata.update(chosen.strata)

    while len(selected) < query_limit:
        remaining = [query for query in candidates if query.query_id not in selected_ids]
        if not remaining:
            break
        chosen = max(remaining, key=score)
        selected.append(chosen)
        selected_ids.add(chosen.query_id)
        selected_strata.update(chosen.strata)

    rng = random.Random(seed)
    rng.shuffle(selected)
    return selected
