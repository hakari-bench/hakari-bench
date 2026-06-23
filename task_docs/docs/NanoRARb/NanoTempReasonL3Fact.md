# NanoRARb / NanoTempReasonL3Fact

## Overview

`NanoTempReasonL3Fact` is an English temporal reasoning retrieval task from NanoRARb. The query contains a harder before/after temporal question plus a compact set of supporting dated facts, and the relevant document is the correct short answer string. Each query has one positive. Dense retrieval is the strongest top-rank profile, while `reranking_hybrid` gives the highest recall@100. This makes the task a useful probe for whether a reranker can exploit a broad hybrid candidate pool and then perform exact temporal ordering.

## Details

### What the Original Data Measures

RAR-b converts TempReason reasoning tasks into answer retrieval tasks. TempReason evaluates temporal reasoning over dated facts, including interval validity and relative ordering.

The L3 fact variant supplies supporting temporal facts in the query, but the question usually asks for a predecessor, successor, or other relative state. The retriever must identify the relevant timeline and select the answer whose temporal position satisfies the question.

### Observed Data Profile

The Nano split contains 200 queries, 10,000 documents, and 200 positive qrel rows. Every query has exactly one positive. Queries average 1,981.07 characters, while answer documents average 19.88 characters.

Examples ask who chaired Technical University of Munich before Wolfgang A. Herrmann, who led Romania before Alexandru G. Golescu, which parliamentary position Lord Douglas Gordon-Hallyburton held before a later Parliament, which employer Eduard Winkelmann joined after the Imperial University of Dorpat, and who led Romania after Adrian Nastase.

### BM25 Evaluation Profile

The BM25 candidate subset uses top-500 candidates and reaches nDCG@10 of 0.0547, hit@10 of 0.1150, and recall@100 of 0.6600. BM25 can recover many answers into the broader candidate set because the compact fact list contains entity and role strings.

Top-rank quality remains weak because the most lexically similar fact is not necessarily the temporally correct one. The task often requires ordering facts before or after an anchor state, which term frequency does not model.

### Dense Evaluation Profile

The dense candidate subset from `harrier_oss_v1_270m` uses top-500 candidates and reaches nDCG@10 of 0.2549, hit@10 of 0.4700, and recall@100 of 0.8700. Dense retrieval is much stronger than BM25 for early ranking.

The compact fact setting lets semantic similarity focus on the relevant timeline more effectively than in long-context variants. Still, the model must distinguish adjacent timeline entries that are semantically similar but temporally different.

### Reranking Hybrid Evaluation Profile

The `reranking_hybrid` subset uses top-100 candidates, with 15 rows receiving the optional rank-101 safeguard. It reaches nDCG@10 of 0.1981, hit@10 of 0.4450, and recall@100 of 0.9250. Hybrid retrieval has the best recall@100 but lower nDCG@10 than dense retrieval.

This is a classic candidate-pool tradeoff. Sparse matching helps expose correct answer strings from the provided facts, while dense retrieval orders likely answers better. A capable temporal reranker should benefit from the hybrid pool because it contains more positives at rank 100.

### Metric Interpretation for Model Researchers

With one positive per query, nDCG@10 measures early placement of the exact answer string, hit@10 measures top-ten availability, and recall@100 measures whether a second-stage reranker can access the correct answer.

For this split, dense retrieval is the better first-stage ranker, but hybrid retrieval is the better source of reranking candidates. Improvements should be judged by both early rank quality and whether recall@100 increases without adding too many temporally adjacent distractors.

### Query and Relevance Type Tendencies

Queries contain a temporal question and a compact set of dated facts. Relevant documents are short answer strings, often names, offices, institutions, or roles. The answer is usually determined by before/after ordering inside a timeline.

Relevance is exact temporal order. An answer from the same timeline is wrong if it is not the specified predecessor, successor, or otherwise ordered target.

### Representative Failure Modes

Common failures include retrieving the anchor entity, selecting a non-adjacent timeline entry, ranking an answer with stronger lexical overlap above the ordered answer, and confusing related offices or employers. BM25 sees the strings but not the order; dense retrieval can still compress adjacent states into similar representations.

### Training Data That May Help

Useful training data includes timeline QA, before/after retrieval pairs, temporal ordering examples, entity succession tasks, and hard negatives from adjacent entries in the same timeline. Evaluation facts, queries, answers, and qrels should be excluded.

### Model Improvement Notes

Models should learn to represent temporal direction and position, not only entity similarity. Hard negatives should include the anchor entity and nearby timeline entries. This split is especially useful for testing rerankers because the hybrid pool provides strong recall while still requiring temporal reasoning for final ordering.

## Example Data

| Query | Positive document |
| --- | --- |
| Question: Who was the chair of Technical University of Munich before Wolfgang A. Herrmann? Facts: Ot... [100 / 473 chars] | Otto Meitinger [14 chars] |
| Question: Who was the head of Romania before Alexandru G. Golescu? Facts: Gheorghe Tătărescu is the... [100 / 4,784 chars] | Dimitrie Ghica [14 chars] |
| Question: Which position did Lord Douglas Gordon-Hallyburton hold before Member of the 13th Parliame... [100 / 675 chars] | Member of the 12th Parliament of the United Kingdom [51 chars] |
| Question: Which employer did Eduard Winkelmann work for after Imperial University of Dorpat? Facts:... [100 / 514 chars] | University of Bern [18 chars] |
| Question: Who was the head of Romania after Adrian Năstase? Facts: Petre Roman is the head of the go... [100 / 4,777 chars] | Călin Popescu-Tăriceanu [23 chars] |

### Source Reference Table

| Title | Year | Type | URL |
| --- | ---: | --- | --- |
| RAR-b: Reasoning as Retrieval Benchmark | 2024 | arXiv paper | [https://arxiv.org/abs/2404.06347](https://arxiv.org/abs/2404.06347) |
| Towards Benchmarking and Improving the Temporal Reasoning Capability of Large Language Models | 2023 | arXiv paper | [https://arxiv.org/abs/2306.08952](https://arxiv.org/abs/2306.08952) |

### Representative Snippets

| Query | Relevant document excerpt |
| --- | --- |
| Who was the chair of Technical University of Munich before Wolfgang A. Herrmann, given a compact timeline of chair facts? | Otto Meitinger. |
| Who was the head of Romania before Alexandru G. Golescu? | Dimitrie Ghica. |
| Which position did Lord Douglas Gordon-Hallyburton hold before Member of the 13th Parliament of the United Kingdom? | Member of the 12th Parliament of the United Kingdom. |
| Which employer did Eduard Winkelmann work for after Imperial University of Dorpat? | University of Bern. |
| Who was the head of Romania after Adrian Nastase? | Calin Popescu-Tariceanu. |
