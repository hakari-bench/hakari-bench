from __future__ import annotations

from scripts.estimate_openai_embedding_nanoset_costs import (
    OPENAI_EMBEDDING_MAX_INPUT_TOKENS,
    aggregate_dataset_rows,
    embedding_cost_usd,
    token_stats_from_counts,
)


def test_embedding_cost_usd_uses_price_per_million_tokens() -> None:
    assert embedding_cost_usd(2_500_000, price_usd_per_1m_tokens=0.02) == 0.05
    assert embedding_cost_usd(2_500_000, price_usd_per_1m_tokens=0.13) == 0.325


def test_token_stats_from_counts_includes_over_limit_count() -> None:
    stats = token_stats_from_counts([3, 7, OPENAI_EMBEDDING_MAX_INPUT_TOKENS + 1])
    expected_total = OPENAI_EMBEDDING_MAX_INPUT_TOKENS + 11

    assert stats.count == 3
    assert stats.total_tokens == expected_total
    assert stats.min_tokens == 3
    assert stats.max_tokens == OPENAI_EMBEDDING_MAX_INPUT_TOKENS + 1
    assert stats.mean_tokens == expected_total / 3
    assert stats.median_tokens == 7
    assert stats.over_max_input_count == 1


def test_aggregate_dataset_rows_sums_task_cost_inputs() -> None:
    rows = aggregate_dataset_rows(
        [
            {
                "dataset_name": "NanoToy",
                "dataset_id": "hakari-bench/NanoToy",
                "query_count": 2,
                "query_tokens": 10,
                "query_over_max_input_count": 0,
                "document_count": 3,
                "document_tokens": 90,
                "document_over_max_input_count": 1,
                "total_tokens": 100,
            },
            {
                "dataset_name": "NanoToy",
                "dataset_id": "hakari-bench/NanoToy",
                "query_count": 1,
                "query_tokens": 20,
                "query_over_max_input_count": 1,
                "document_count": 2,
                "document_tokens": 80,
                "document_over_max_input_count": 0,
                "total_tokens": 100,
            },
        ],
        prices_usd_per_1m={"text-embedding-3-small": 0.02, "text-embedding-3-large": 0.13},
    )

    assert rows == [
        {
            "dataset_name": "NanoToy",
            "dataset_id": "hakari-bench/NanoToy",
            "task_count": 2,
            "query_count": 3,
            "query_tokens": 30,
            "query_over_max_input_count": 1,
            "document_count": 5,
            "document_tokens": 170,
            "document_over_max_input_count": 1,
            "total_tokens": 200,
            "text-embedding-3-small_cost_usd": 0.000004,
            "text-embedding-3-large_cost_usd": 0.000026,
        }
    ]
