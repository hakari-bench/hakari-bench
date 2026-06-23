# NanoRARb / NanoPIQA

## Overview

`NanoPIQA` is an English physical commonsense retrieval task from NanoRARb. It recasts PIQA as retrieval: the query is a short practical goal or problem, and the relevant document is the correct solution or physical procedure. Each query has one positive answer. The task tests whether retrievers understand object affordances and everyday physical constraints. Dense retrieval is the strongest observed profile, while the hybrid pool is close and BM25 is weaker but still useful when object names overlap.

## Details

### What the Original Data Measures

RAR-b uses PIQA as a physical commonsense reasoning task converted into answer retrieval. The original PIQA benchmark asks systems to choose between plausible and implausible solutions for everyday physical goals. It focuses on affordances, procedures, and physical interactions.

In this Nano split, the answer pool contains many short procedures. The retriever must map a short goal to the procedure that would actually work.

### Observed Data Profile

The Nano split contains 200 queries, 10,000 documents, and 200 positive qrel rows. Each query has exactly one positive. Queries average 37.89 characters, and candidate answer documents average 98.01 characters.

Examples include lighting a deep wick, growing a plant, getting gym membership reimbursement, wrapping an extension cord, and using a napkin or similar object affordance. The queries are much shorter than the answer candidates.

### BM25 Evaluation Profile

The BM25 candidate subset uses top-500 candidates and reaches nDCG@10 of 0.2443, hit@10 of 0.3650, and recall@100 of 0.5950. BM25 helps when the solution repeats the goal's object names, such as candle, plant, gym, or extension cord.

The limitation is that physical commonsense often requires knowing what action is appropriate even when the answer uses different wording. A wrong candidate can mention the same object but describe an unsafe, irrelevant, or ineffective action.

### Dense Evaluation Profile

The dense candidate subset from `harrier_oss_v1_270m` uses top-500 candidates and reaches nDCG@10 of 0.4017, hit@10 of 0.5500, and recall@100 of 0.6800. Dense retrieval clearly outperforms BM25. Embedding similarity helps connect short practical goals to longer procedural answers.

Dense retrieval is the strongest standalone profile for this split. It captures some affordance and goal-solution relationships that are not visible through exact term overlap alone.

### Reranking Hybrid Evaluation Profile

The `reranking_hybrid` subset uses top-100 candidates, with 65 rows receiving the optional rank-101 safeguard. It reaches nDCG@10 of 0.3741, hit@10 of 0.5300, and recall@100 of 0.6750. Hybrid retrieval is close to dense retrieval but slightly weaker on all metrics.

This suggests that BM25 adds useful object anchors but also introduces distractors with shared nouns and wrong procedures. Dense retrieval remains the better first-stage ranker, while hybrid can still be useful for reranking coverage.

### Metric Interpretation for Model Researchers

With one positive per query, nDCG@10 reflects the rank of the correct procedure, hit@10 measures whether the right solution appears in the first ten candidates, and recall@100 measures whether a reranker can see it.

For PIQA, dense retrieval is the baseline to beat. Improvements should show better physical-action understanding, not just stronger matching of object names.

### Query and Relevance Type Tendencies

Queries are short goals, often just a phrase or simple question. Relevant documents are procedural solutions involving object use, motion, household actions, or practical constraints. Candidate answers may be longer and contain more detail than the query.

Relevance is physical feasibility. A candidate must solve the goal in the real world, not merely mention the same objects.

### Representative Failure Modes

Common failures include selecting an answer that shares an object but uses it incorrectly, ranking vague advice above a concrete procedure, failing to infer an affordance, and confusing a related household action with the actual goal. BM25 overweights repeated nouns; dense retrieval can over-rank semantically related but impractical actions.

### Training Data That May Help

Useful training data includes physical commonsense QA, how-to retrieval, goal-to-procedure pairs, household task instructions, and hard negatives that mention the same objects but use unsafe or impossible actions. Evaluation queries and answer documents should be excluded.

### Model Improvement Notes

Models should learn goal-to-action compatibility and object affordances. Hard negatives should be lexically similar but physically wrong. Because the query is very short, training should emphasize practical reasoning over passage-level semantic similarity.

## Example Data

| Query | Positive document |
| --- | --- |
| How to light a candle with a deep seated wick? [46 chars] | invert the candle upside down and use the lighter to reach into the wick to light it [84 chars] |
| How to grow a plant. [20 chars] | Bury seed in soil and add 1 cup of water daily. [47 chars] |
| How can I get free gym memberships? [35 chars] | Check with your health insurance co., many times they'll reimburse your gym costs. [82 chars] |

### Source Reference Table

| Title | Year | Type | URL |
| --- | ---: | --- | --- |
| RAR-b: Reasoning as Retrieval Benchmark | 2024 | arXiv paper | [https://arxiv.org/abs/2404.06347](https://arxiv.org/abs/2404.06347) |
| PIQA: Reasoning about Physical Commonsense in Natural Language | 2020 | arXiv paper | [https://arxiv.org/abs/1911.11641](https://arxiv.org/abs/1911.11641) |

### Representative Snippets

| Query | Relevant document excerpt |
| --- | --- |
| How do you light a candle with a deep-seated wick? | Invert the candle and use the lighter to reach into the wick. |
| How do you grow a plant? | Bury a seed in soil and add water daily. |
| How can someone get free gym memberships? | Check whether health insurance reimburses gym costs. |
| How do you neatly wrap an extension cord? | Wrap the cord around your hand and elbow. |
| What can a napkin be used for in a practical object-use setting? | Hold an ice cream scoop to keep hands warm. |
