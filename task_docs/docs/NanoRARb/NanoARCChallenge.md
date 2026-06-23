# NanoRARb / NanoARCChallenge

## Overview

`NanoARCChallenge` is an English reasoning-as-retrieval task from NanoRARb. It recasts AI2 ARC-Challenge science questions as retrieval: the query is a grade-school science question, and the document pool consists of short candidate answers. Each query has one correct answer document. The task is difficult because the answer is often a concise phrase that must be inferred from scientific reasoning rather than matched lexically. Dense retrieval improves over BM25, but absolute scores remain low, showing that answer retrieval from short candidates is not solved by semantic similarity alone.

## Details

### What the Original Data Measures

RAR-b, the Reasoning as Retrieval Benchmark, converts reasoning tasks into retrieval problems by pooling possible answers and asking a retriever to find the gold answer. The original ARC-Challenge benchmark was designed to test grade-school science question answering, especially questions that are difficult for simple retrieval and word co-occurrence methods.

In this Nano task, the retrieval target is not a supporting passage. It is the correct short answer option. A model must connect the question to the answer through scientific knowledge, causal reasoning, physical reasoning, or basic biology and earth-science concepts.

### Observed Data Profile

The Nano split contains 200 queries, 9,350 documents, and 200 positive qrel rows. Each query has exactly one positive. Queries average 126.66 characters, while documents average only 30.94 characters.

Examples include hardness ordering, hurricanes forming near the equator, the troposphere, the atomic unit of copper, and decay of discarded objects. Candidate documents are usually very short phrases or one-sentence answers, so the corpus provides little contextual text to help retrieval.

### BM25 Evaluation Profile

The BM25 candidate subset uses top-500 candidates and reaches nDCG@10 of 0.0386, hit@10 of 0.0850, and recall@100 of 0.2250. BM25 is very weak because many correct answers do not repeat the important query words. The answer may be `greatest density`, `the atom`, or `solar heating is greatest near the equator`, while the query frames the concept indirectly.

Sparse retrieval can work when the correct answer shares unusual terms with the question, but ARC-Challenge was explicitly built to avoid trivial lexical matching. This makes BM25 a low baseline rather than a strong retrieval method.

### Dense Evaluation Profile

The dense candidate subset from `harrier_oss_v1_270m` uses top-500 candidates and reaches nDCG@10 of 0.1113, hit@10 of 0.1900, and recall@100 of 0.3600. Dense retrieval improves over BM25 across all reported metrics, suggesting that embeddings capture some science-question semantics and answer plausibility.

The scores remain low because the candidate documents are extremely short and the query often requires multi-step reasoning. Dense similarity can identify related concepts but may still rank plausible distractor answers above the exact gold answer.

### Reranking Hybrid Evaluation Profile

The `reranking_hybrid` subset uses top-100 candidates, with 129 rows receiving the optional rank-101 safeguard. It reaches nDCG@10 of 0.0642, hit@10 of 0.1350, and recall@100 of 0.3550. Hybrid retrieval improves over BM25 but does not match dense retrieval on top-rank metrics.

The high number of safeguard rows shows that many positives are difficult to keep inside a compact top-100 answer pool. Hybrid retrieval is close to dense recall@100, but dense retrieval is the better standalone ranker for this split.

### Metric Interpretation for Model Researchers

Because there is exactly one positive answer per query, nDCG@10 mostly reflects how early the correct answer appears, hit@10 measures first-page answer retrieval, and recall@100 indicates whether a later reranker can see the gold answer.

For ARC-Challenge, dense retrieval is the stronger first-stage baseline, but the task remains hard. A high-performing model needs reasoning-aware answer selection, not just passage retrieval.

### Query and Relevance Type Tendencies

Queries are short science questions. They may ask about cause and effect, ordering, atmosphere layers, material properties, units of matter, or biological decay. Relevant documents are concise answer options, often too short to contain explanatory context.

Relevance is answer correctness. A semantically related answer is wrong if it does not satisfy the specific scientific question.

### Representative Failure Modes

Common failures include ranking a topical answer that shares science vocabulary but gives the wrong relationship, missing answers that are short generic phrases, confusing cause with effect, and failing to compute an ordering or comparison implied by the question. BM25 misses non-overlapping answers; dense retrieval can prefer plausible but incorrect distractors.

### Training Data That May Help

Useful training data includes science QA answer selection, explanation-backed multiple-choice QA, retrieval-formatted ARC-style pairs, and hard negatives from incorrect answer choices. Evaluation queries, candidate answers, and qrels should be excluded.

### Model Improvement Notes

Models should learn to map questions to concise answer phrases through science reasoning. Hard negatives should be topically close and fluent but scientifically wrong. Because candidate documents are short, training should emphasize query-answer reasoning rather than passage matching.

## Example Data

| Query | Positive document |
| --- | --- |
| Some students are performing hardness tests on several substances. X scratches Y. Y scratches Z. Z s... [100 / 176 chars] | W is the softest of the four substances tested. [47 chars] |
| Hurricanes form over equatorial areas. This is because [54 chars] | solar heating is greatest near the equator. [43 chars] |
| The best description of the troposphere is the layer of the atmosphere with the [79 chars] | greatest density. [17 chars] |
| Copper is an element that is used in electrical wires. What is the smallest unit of copper that stil... [100 / 142 chars] | the atom [8 chars] |
| If you throw each one of these things away, which will decay fastest? [69 chars] | An apple core [13 chars] |

### Source Reference Table

| Title | Year | Type | URL |
| --- | ---: | --- | --- |
| RAR-b: Reasoning as Retrieval Benchmark | 2024 | arXiv paper | [https://arxiv.org/abs/2404.06347](https://arxiv.org/abs/2404.06347) |
| Think you have solved question answering? Try ARC, the AI2 Reasoning Challenge | 2018 | arXiv paper | [https://arxiv.org/abs/1803.05457](https://arxiv.org/abs/1803.05457) |

### Representative Snippets

| Query | Relevant document excerpt |
| --- | --- |
| Students compare hardness: X scratches Y, Y scratches Z, and Z scratches W. What follows about W? | W is the softest of the four substances tested. |
| Why do hurricanes form over equatorial areas? | Solar heating is greatest near the equator. |
| What best describes the troposphere? | The layer with the greatest density. |
| What is the smallest unit of copper that still has copper's characteristics? | The atom. |
| Which discarded item will decay fastest? | An apple core. |
