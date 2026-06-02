# Leaderboard Metric Policy

This document defines the default HAKARI-Bench leaderboard metric set and the
reasoning behind it.

HAKARI-Bench evaluates compact information retrieval tasks across languages,
domains, model families, and embedding variants. The viewer has to support two
common reading modes:

- Human-facing search quality: the first few results should be correct and
  well ordered.
- AI-facing retrieval quality: the top candidate set should preserve enough
  relevant evidence for a downstream reranker, LLM, RAG pipeline, or agent.

Because those modes answer different questions, no single metric is sufficient.
`nDCG@10` remains the primary ranking metric, but the default visible set also
includes top-100 coverage metrics for AI-facing retrieval analysis.

## Default visible metrics

The viewer exposes the following metrics, in this order:

| Metric | Purpose |
| --- | --- |
| `nDCG@10` | Primary top-10 ranking quality. This is the default leaderboard metric. |
| `nDCG@100` | Top-100 ranking quality. Useful when downstream systems can inspect a wider candidate set but still benefit from better ordering. |
| `Recall@10` | Relevant-document coverage inside the first 10 results. This complements `nDCG@10` for multi-positive tasks. |
| `Recall@100` | AI/RAG candidate retention. This shows whether relevant evidence survives into the top-100 pool. |
| `Acc@1` | Whether the first result contains at least one relevant document. Useful for direct answer and reranking checks. |
| `Acc@10` | Whether the top 10 contains any relevant document. Easy to interpret for single-positive and sparse-qrels tasks. |
| `Acc@100` | Whether the top 100 contains any relevant document. Useful as a broad candidate-recall sanity check. |
| `MRR@10` | Rank of the first relevant document within the top 10. This distinguishes rank 1 from rank 2-10 when `Acc@10` is already 1.0. |
| `MAP@100` | Multi-positive ranking quality through the top 100. This rewards retrieving many relevant documents early. |

## Why keep MRR@10

`MRR@10` focuses on the first relevant result. `Acc@10` only says whether a
relevant item appears anywhere in the first 10 results, so a hit at rank 1 and a
hit at rank 10 both receive the same score. `MRR@10` separates those cases:

- hit at rank 1: `1.0`
- hit at rank 2: `0.5`
- hit at rank 5: `0.2`
- hit at rank 10: `0.1`

This is useful for single-answer retrieval, question answering, and reranking
diagnostics where the first usable result matters.

## Why keep MAP@100

`MAP@100` measures how early multiple relevant documents appear in the top 100.
`Recall@100` measures whether relevant documents remain in the candidate pool,
but it does not distinguish relevant documents at ranks 2, 5, and 9 from the
same documents at ranks 80, 90, and 99. `MAP@100` adds that ordering signal.

This matters for AI-facing retrieval because downstream systems often have
token budgets, chunk budgets, latency limits, or reranking budgets. Even when a
system can retrieve 100 candidates, earlier relevant evidence is easier to use.

`MAP@100` should be read as a secondary metric when qrels are sparse. It is most
informative for tasks with multiple known relevant documents per query.

## Why Precision@10 is not a default viewer metric

`Precision@10` is intentionally not part of the default visible metric set.
Many Nano tasks have only one or a few judged positives per query. In those
tasks, `Precision@10` has a low ceiling even for good systems and can make
single-positive tasks look structurally worse than multi-positive tasks.

For HAKARI-Bench leaderboard comparison, `nDCG@10`, `Recall@10`, `Acc@10`,
`MRR@10`, and `MAP@100` provide more useful views of top-10 and top-100 quality.
`Precision@10` can still be computed externally from the stored top-ranking
artifacts if a task-specific analysis needs it.

## Storage and recomputation

Task result JSON files keep the compact default metrics and embed
`artifacts.top_rankings` with top-100 rankings and qrels. The DuckDB build uses
those artifacts to recompute the default visible metric set without rerunning
model inference. This keeps result JSON compact while allowing the viewer to
compare top-10 quality, top-100 candidate retention, and reranking behavior
from the same canonical ranking artifacts.
