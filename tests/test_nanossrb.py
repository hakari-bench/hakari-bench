from __future__ import annotations

import json

from hakari_bench.nanossrb import (
    SSRBQuery,
    apply_positive_limit,
    condition_stratified_sample,
)
from scripts.create_nanossrb_dataset import _reservoir_rows, select_variant_queries


def _query(
    query_id: str,
    *,
    schema: str,
    positives: int,
    time_type: int = 0,
    exact_conditions: int = 1,
    semantic_conditions: int = 0,
) -> SSRBQuery:
    return SSRBQuery(
        query_id=query_id,
        text=f"query {query_id}",
        domain="product_search",
        schema=schema,
        positive_doc_ids=tuple(f"{query_id}-d{index}" for index in range(positives)),
        time_type=time_type,
        exact_conditions=exact_conditions,
        semantic_conditions=semantic_conditions,
        source_condition=None,
    )


def test_apply_positive_limit_strict_drops_queries_over_limit() -> None:
    kept, excluded = apply_positive_limit(
        [_query("q5", schema="a", positives=5), _query("q6", schema="b", positives=6)],
        max_positives=5,
        overflow_policy="drop-query",
    )

    assert [query.query_id for query in kept] == ["q5"]
    assert excluded == set()


def test_apply_positive_limit_cap_excludes_omitted_positive_documents_globally() -> None:
    kept, excluded = apply_positive_limit(
        [_query("q7", schema="a", positives=7)],
        max_positives=5,
        overflow_policy="cap-and-exclude",
    )

    assert len(kept[0].positive_doc_ids) == 5
    assert len(excluded) == 2
    assert set(kept[0].positive_doc_ids) | excluded == {f"q7-d{index}" for index in range(7)}


def test_condition_stratified_sample_is_deterministic_and_covers_schemas_and_conditions() -> None:
    candidates = [
        _query("a-basic", schema="a", positives=1),
        _query("a-time", schema="a", positives=2, time_type=1),
        _query("a-sem", schema="a", positives=3, semantic_conditions=1),
        _query("b-basic", schema="b", positives=4),
        _query("b-time", schema="b", positives=5, time_type=1),
        _query("b-sem", schema="b", positives=1, semantic_conditions=1),
    ]

    first = condition_stratified_sample(candidates, query_limit=4, min_per_schema=1, seed=7)
    second = condition_stratified_sample(candidates, query_limit=4, min_per_schema=1, seed=7)

    assert [query.query_id for query in first] == [query.query_id for query in second]
    assert {query.schema for query in first} == {"a", "b"}
    assert any(query.time_type for query in first)
    assert any(query.semantic_conditions for query in first)
    assert all(1 <= len(query.positive_doc_ids) <= 5 for query in first)


def test_strict_max5_fills_a_shortfall_with_uncapped_six_positive_queries() -> None:
    selected, excluded = select_variant_queries(
        [
            _query("q1", schema="a", positives=1),
            _query("q5", schema="b", positives=5),
            _query("q6", schema="c", positives=6),
            _query("q7", schema="d", positives=7),
        ],
        variant="strict-max5",
        query_limit=3,
        min_per_schema=1,
        seed=17,
    )

    assert {query.query_id for query in selected} == {"q1", "q5", "q6"}
    assert len(next(query for query in selected if query.query_id == "q6").positive_doc_ids) == 6
    assert excluded == set()


def test_reservoir_keeps_wanted_docs_and_uses_only_safe_n_provenance_fillers(tmp_path) -> None:
    corpus_path = tmp_path / "schema.corpus.jsonl"
    rows = [
        {"_id": "domain--schema--p--wanted", "text": "wanted"},
        {"_id": "domain--schema--n--safe-1", "text": "safe one"},
        {"_id": "domain--schema--n--safe-2", "text": "safe two"},
        {"_id": "domain--schema--n--known-positive", "text": "judged elsewhere"},
        {"_id": "domain--schema--n--excluded", "text": "capped positive"},
        {"_id": "domain--schema--p--unjudged", "text": "positive provenance"},
    ]
    corpus_path.write_text("".join(json.dumps(row) + "\n" for row in rows), encoding="utf-8")

    wanted, candidates = _reservoir_rows(
        corpus_path,
        wanted_ids={"domain--schema--p--wanted"},
        excluded_ids={"domain--schema--n--excluded"},
        known_positive_ids={"domain--schema--n--known-positive", "domain--schema--p--wanted"},
        candidate_limit=10,
        seed=17,
    )

    assert set(wanted) == {"domain--schema--p--wanted"}
    assert {row["_id"] for row in candidates} == {
        "domain--schema--n--safe-1",
        "domain--schema--n--safe-2",
    }
