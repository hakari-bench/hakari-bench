# NanoRARb / NanoHellaSwag

## Overview

`NanoHellaSwag` is an English commonsense continuation retrieval task from NanoRARb. It recasts HellaSwag as retrieval: the query is an unfinished grounded activity or video-caption context, and the relevant document is the plausible continuation. Each query has one positive continuation among 10,000 short candidate endings. The task requires event coherence and commonsense plausibility rather than fact lookup. BM25 and dense retrieval are both weak, and `reranking_hybrid` is the strongest observed profile, suggesting that both lexical continuity and semantic event matching are useful.

## Details

### What the Original Data Measures

RAR-b includes HellaSwag as a commonsense reasoning task converted into full answer retrieval. The original HellaSwag benchmark asks whether a system can choose the plausible ending for a grounded situation after adversarial filtering creates fluent but wrong distractors.

In this retrieval version, the system must find the correct ending from a large answer pool. The document is not evidence; it is the continuation itself.

### Observed Data Profile

The Nano split contains 200 queries, 10,000 documents, and 200 positive qrel rows. Each query has exactly one positive. Queries average 114.68 characters, and candidate endings average 62.15 characters.

Examples include ice fishing, mopping a floor, weightlifting, crushing a small stone, and flying a kite. Candidate continuations are short action descriptions and often share objects or verbs with the query.

### BM25 Evaluation Profile

The BM25 candidate subset uses top-500 candidates and reaches nDCG@10 of 0.1393, hit@10 of 0.2300, and recall@100 of 0.5250. BM25 is limited because the correct continuation may not repeat enough distinctive query words. Many incorrect endings can mention the same objects or activities but violate temporal or physical plausibility.

Sparse retrieval is useful when the continuation repeats an object or action from the context, but HellaSwag is designed around plausible-looking distractors, so term overlap is only a weak signal.

### Dense Evaluation Profile

The dense candidate subset from `harrier_oss_v1_270m` uses top-500 candidates and reaches nDCG@10 of 0.1253, hit@10 of 0.2500, and recall@100 of 0.5250. Dense retrieval slightly improves hit@10 but has lower nDCG@10 than BM25 and equal recall@100.

This indicates that semantic similarity can identify plausible continuations, but it may not order the exact gold ending above other coherent-looking events. Dense embeddings can overvalue general scene compatibility without capturing the specific next action.

### Reranking Hybrid Evaluation Profile

The `reranking_hybrid` subset uses top-100 candidates, with 81 rows receiving the optional rank-101 safeguard. It reaches nDCG@10 of 0.1551, hit@10 of 0.2900, and recall@100 of 0.5950. Hybrid retrieval is the strongest profile for this split.

The result suggests that event-continuation retrieval benefits from combining sparse overlap with dense plausibility. BM25 helps preserve local objects and actions, while dense retrieval brings broader event semantics. The hybrid pool is the best candidate source for reranking.

### Metric Interpretation for Model Researchers

With one positive per query, nDCG@10 measures how early the correct continuation is ranked, hit@10 measures whether it appears in the first ten candidates, and recall@100 measures whether a reranker can access it.

For HellaSwag, absolute retrieval scores are low. A strong model must reason about temporal order, physical plausibility, and activity continuity among short candidate endings.

### Query and Relevance Type Tendencies

Queries are unfinished descriptions of everyday activities or video-like scenes. Relevant documents are plausible next events. Candidate endings are fluent and may share the same objects, people, or actions.

Relevance is continuation correctness. A candidate can be semantically related and still wrong if it does not continue the scene naturally.

### Representative Failure Modes

Common failures include selecting an ending with matching objects but impossible timing, ranking a generic action above the specific next step, confusing repeated activity with conclusion, and missing physical consequences such as a kite falling when wind lessens. Sparse retrieval overweights object overlap; dense retrieval can over-rank broadly plausible scenes.

### Training Data That May Help

Useful training data includes story and activity continuation, grounded commonsense QA, HellaSwag-style adversarial endings, and hard negatives that share objects or actions but break physical or temporal plausibility. Evaluation examples and answer pool entries should be excluded.

### Model Improvement Notes

Models should learn event sequence compatibility over short text. Hard negatives should be fluent and lexically similar while violating the next-event relation. Hybrid retrieval is useful because both object continuity and semantic plausibility matter.

## Example Data

| Query | Positive document |
| --- | --- |
| A man dressed in yellow and black winter clothes ice fishes on a a frozen lake. The man [87 chars] | is reeling in a fish for a long time. [37 chars] |
| A group of people are in a house. A man is mopping the floor with a mop. Another boy [84 chars] | attempts to walk through where he is mopping. [45 chars] |
| A man is in the gym in tight he bends over picks up a weight over his head and drops it back down. He walks back and loosens up before walking back up and doing it again adding more weight. He [192 chars] | does this multiple times adding more and more weight to the rack. [65 chars] |

### Source Reference Table

| Title | Year | Type | URL |
| --- | ---: | --- | --- |
| RAR-b: Reasoning as Retrieval Benchmark | 2024 | arXiv paper | [https://arxiv.org/abs/2404.06347](https://arxiv.org/abs/2404.06347) |
| HellaSwag: Can a Machine Really Finish Your Sentence? | 2019 | arXiv paper | [https://arxiv.org/abs/1905.07830](https://arxiv.org/abs/1905.07830) |

### Representative Snippets

| Query | Relevant document excerpt |
| --- | --- |
| A man in yellow and black winter clothes ice fishes on a frozen lake. | He is reeling in a fish for a long time. |
| A man is mopping the floor in a house while another boy is nearby. | The boy attempts to walk through where he is mopping. |
| A man repeatedly bends, lifts a weight overhead, drops it, and adds more weight. | He does this multiple times, adding more and more weight to the rack. |
| A person takes a small stone from a flowing river and crushes it on another stone. | They grind it hard to make the pieces smaller. |
| A person hangs onto the handles of a kite flying overhead. | The kite falls as the wind lessens. |
