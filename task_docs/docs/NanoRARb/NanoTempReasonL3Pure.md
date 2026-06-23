# NanoRARb / NanoTempReasonL3Pure

## Overview

`NanoTempReasonL3Pure` is an English temporal reasoning retrieval task from NanoRARb. The query is a compact before/after temporal question without supporting facts, and the relevant document is the correct short answer string. Each query has one positive. This split combines the sparse evidence problem of pure retrieval with the harder ordering requirement of L3 TempReason. Dense retrieval is the strongest profile, `reranking_hybrid` improves over BM25, and BM25 remains near zero because the answer is usually not lexically present in the query.

## Details

### What the Original Data Measures

RAR-b reformulates TempReason reasoning tasks as retrieval over answer candidates. TempReason evaluates whether systems can reason about dates, intervals, and temporal order.

The L3 pure variant removes the supporting facts and asks a harder relative temporal question. The model must retrieve the correct predecessor, successor, or ordered answer using knowledge encoded in its representation rather than evidence included in the query.

### Observed Data Profile

The Nano split contains 200 queries, 10,000 documents, and 200 positive qrel rows. Every query has exactly one positive. Queries average 65.13 characters, while answer documents average 19.88 characters.

Examples ask who chaired Technical University of Munich before Wolfgang A. Herrmann, who led Romania before Alexandru G. Golescu, which parliamentary position Lord Douglas Gordon-Hallyburton held before a later Parliament, which employer Eduard Winkelmann joined after the Imperial University of Dorpat, and who led Romania after Adrian Nastase.

### BM25 Evaluation Profile

The BM25 candidate subset uses top-500 candidates and reaches nDCG@10 of 0.0074, hit@10 of 0.0150, and recall@100 of 0.0950. This is a very weak lexical baseline.

The query contains an anchor entity and a temporal relation, while the correct answer is a different short string. BM25 cannot infer a missing timeline or identify the neighboring state, so it only succeeds when the answer has accidental overlap with the query.

### Dense Evaluation Profile

The dense candidate subset from `harrier_oss_v1_270m` uses top-500 candidates and reaches nDCG@10 of 0.0707, hit@10 of 0.1550, and recall@100 of 0.5400. Dense retrieval is clearly the strongest method among the three reported profiles.

The score remains modest because the task asks for implicit temporal knowledge. Embedding similarity can connect some anchors and likely answer strings, but it often confuses adjacent timeline entities or more prominent alternatives.

### Reranking Hybrid Evaluation Profile

The `reranking_hybrid` subset uses top-100 candidates, with 117 rows receiving the optional rank-101 safeguard. It reaches nDCG@10 of 0.0238, hit@10 of 0.0600, and recall@100 of 0.4150. Hybrid retrieval improves over BM25 but is weaker than dense retrieval.

This shows that sparse matching contributes little when supporting facts are absent. Hybrid retrieval may still increase candidate diversity, but the main useful signal comes from dense association and temporal knowledge.

### Metric Interpretation for Model Researchers

With one positive per query, nDCG@10 measures early placement of the exact answer, hit@10 measures whether the answer appears in the first ten candidates, and recall@100 measures reranker availability.

For `NanoTempReasonL3Pure`, recall@100 is a proxy for whether a retriever can find plausible timeline answers at all. High-quality ranking also requires distinguishing the correct ordered answer from related but temporally invalid candidates.

### Query and Relevance Type Tendencies

Queries are short before/after questions. Relevant documents are short names, offices, institutions, or role strings. The target answer is usually not named in the query and must be inferred from an external temporal sequence.

Relevance is exact ordered validity. The answer must satisfy the specified before or after relation, not merely belong to the same entity timeline.

### Representative Failure Modes

Common failures include retrieving the anchor entity, choosing a more famous office holder, selecting an adjacent but wrong timeline entry, ignoring the before/after direction, and overranking semantically related answer strings. BM25 mostly lacks usable evidence; dense retrieval can recover candidates but may not encode exact ordering.

### Training Data That May Help

Useful training data includes temporal knowledge-base QA, before/after entity retrieval, succession timelines, date-conditioned contrastive examples, and hard negatives from neighboring timeline entries. Evaluation queries, answers, and qrels should be excluded.

### Model Improvement Notes

Models need stronger temporal knowledge and direction-sensitive retrieval. Hard negatives should share the same anchor timeline but differ in before/after relation or adjacency. This split is useful for measuring whether a retriever can use implicit temporal memory rather than copied context.

## Example Data

| Query | Positive document |
| --- | --- |
| Who was the chair of Technical University of Munich before Wolfgang A. Herrmann? [80 chars] | Otto Meitinger [14 chars] |
| Who was the head of Romania before Alexandru G. Golescu? [56 chars] | Dimitrie Ghica [14 chars] |
| Which position did Lord Douglas Gordon-Hallyburton hold before Member of the 13th Parliament of the... [100 / 115 chars] | Member of the 12th Parliament of the United Kingdom [51 chars] |
| Which employer did Eduard Winkelmann work for after Imperial University of Dorpat? [82 chars] | University of Bern [18 chars] |
| Who was the head of Romania after Adrian Năstase? [49 chars] | Călin Popescu-Tăriceanu [23 chars] |

### Source Reference Table

| Title | Year | Type | URL |
| --- | ---: | --- | --- |
| RAR-b: Reasoning as Retrieval Benchmark | 2024 | arXiv paper | [https://arxiv.org/abs/2404.06347](https://arxiv.org/abs/2404.06347) |
| Towards Benchmarking and Improving the Temporal Reasoning Capability of Large Language Models | 2023 | arXiv paper | [https://arxiv.org/abs/2306.08952](https://arxiv.org/abs/2306.08952) |

### Representative Snippets

| Query | Relevant document excerpt |
| --- | --- |
| Who was the chair of Technical University of Munich before Wolfgang A. Herrmann? | Otto Meitinger. |
| Who was the head of Romania before Alexandru G. Golescu? | Dimitrie Ghica. |
| Which position did Lord Douglas Gordon-Hallyburton hold before Member of the 13th Parliament of the United Kingdom? | Member of the 12th Parliament of the United Kingdom. |
| Which employer did Eduard Winkelmann work for after Imperial University of Dorpat? | University of Bern. |
| Who was the head of Romania after Adrian Nastase? | Calin Popescu-Tariceanu. |
