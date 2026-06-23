# NanoRARb / NanoTempReasonL2Context

## Overview

`NanoTempReasonL2Context` is an English temporal reasoning retrieval task from NanoRARb. The query contains a temporal question plus a very long context of dated facts, and the relevant document is the correct entity or answer string. Each query has one positive answer. The task is difficult because the retriever must locate the relevant fact inside a long list, reason over date intervals, and return a short answer. Dense retrieval is much stronger than BM25, while `reranking_hybrid` is close but slightly weaker on top-rank quality and coverage.

## Details

### What the Original Data Measures

RAR-b converts TempReason tasks into retrieval settings. The underlying TempReason benchmark is designed to test temporal reasoning, including reasoning over dates, durations, and interval relations. RAR-b separates temporal tasks into pure, fact, and context variants to test how much supporting information is exposed in the query.

The context variant is the long-query setting. It includes many dated facts, often far more than the needed evidence. The retriever must identify which fact interval contains the queried date and retrieve the corresponding answer string.

### Observed Data Profile

The Nano split contains 200 queries, 10,000 documents, and 200 positive qrel rows. Each query has exactly one positive. Queries average 28,755.18 characters, while answer documents average only 19.91 characters.

Examples ask which office Patricia de Lille held in September 2015, which Parliament Lord Douglas Gordon-Hallyburton belonged to in October 1833, who led Russia in July 1999, which team Glynn Snodin played for in January 1992, and who led Romania in May 1935.

### BM25 Evaluation Profile

The BM25 candidate subset uses top-500 candidates and reaches nDCG@10 of 0.1114, hit@10 of 0.1850, and recall@100 of 0.4600. BM25 can benefit when the answer string appears verbatim in the long context or when an entity name overlaps strongly with the question.

The limitation is severe long-context dilution. Most query words are distractor facts, and the correct answer is a short string chosen by interval containment. Term frequency does not know which dated fact is active at the target month and year.

### Dense Evaluation Profile

The dense candidate subset from `harrier_oss_v1_270m` uses top-500 candidates and reaches nDCG@10 of 0.2171, hit@10 of 0.3750, and recall@100 of 0.7950. Dense retrieval substantially improves over BM25. It is better at mapping the question and relevant factual context to the correct entity or role.

The gap between recall@100 and hit@10 shows that dense retrieval often finds the answer somewhere in the candidate set but still struggles to rank the exact temporal answer very early. This is expected because the task requires interval reasoning rather than pure semantic similarity.

### Reranking Hybrid Evaluation Profile

The `reranking_hybrid` subset uses top-100 candidates, with 46 rows receiving the optional rank-101 safeguard. It reaches nDCG@10 of 0.2049, hit@10 of 0.3650, and recall@100 of 0.7700. Hybrid retrieval is close to dense retrieval but slightly weaker on every reported metric.

This suggests that sparse overlap adds some entity-name anchoring but also introduces long-context distractors. Dense retrieval is the stronger standalone first-stage profile, while hybrid remains a useful reranking comparison.

### Metric Interpretation for Model Researchers

With one positive per query, nDCG@10 measures how early the exact answer string appears, hit@10 measures whether it appears in the first ten candidates, and recall@100 measures whether a reranker can access it.

For this split, recall@100 is especially important because long-context retrieval may expose the correct answer without ranking it first. Strong systems should combine retrieval with temporal interval reasoning.

### Query and Relevance Type Tendencies

Queries contain a question followed by a long set of dated facts. Relevant documents are short answer strings such as an office, team, leader name, or role. The answer is determined by whether a fact's interval contains the queried date.

Relevance is exact temporal validity. An answer associated with the same entity is wrong if its interval does not cover the target date.

### Representative Failure Modes

Common failures include retrieving a role from the wrong time interval, selecting an entity from a nearby fact, overmatching repeated country or person names, and losing the relevant fact among thousands of context tokens. BM25 is vulnerable to term frequency in distractor facts; dense retrieval can cluster related entities without exact interval selection.

### Training Data That May Help

Useful training data includes temporal interval QA, long-context temporal retrieval, entity-time reasoning pairs, and date containment tasks. Evaluation facts, questions, answers, and qrels should be excluded.

### Model Improvement Notes

Models should learn to identify the relevant interval before ranking short answer strings. Hard negatives should use the same entity or relation but with nearby dates outside the valid interval. Long-context handling and temporal computation are both central to this split.

## Example Data

| Query | Positive document |
| --- | --- |
| Question: Which position did Patricia de Lille hold in Sep, 2015? Facts: Patricia de Lille holds the... [100 / 11,244 chars] | mayor of Cape Town [18 chars] |
| Question: Which position did Lord Douglas Gordon-Hallyburton hold in Oct, 1833? Facts: Lord Douglas... [100 / 2,981 chars] | Member of the 11th Parliament of the United Kingdom [51 chars] |
| Question: Who was the head of Russia in Jul, 1999? Facts: Mikhail Kasyanov is the head of the govern... [100 / 71,906 chars] | Sergei Stepashin [16 chars] |
| Question: Which team did Glynn Snodin play for in Jan, 1992? Facts: Glynn Snodin plays for Heart of... [100 / 5,484 chars] | Leeds United F.C. [17 chars] |
| Question: Who was the head of Romania in May, 1935? Facts: Take Ionescu is the head of the governmen... [100 / 75,421 chars] | Gheorghe Tătărescu [18 chars] |

### Source Reference Table

| Title | Year | Type | URL |
| --- | ---: | --- | --- |
| RAR-b: Reasoning as Retrieval Benchmark | 2024 | arXiv paper | [https://arxiv.org/abs/2404.06347](https://arxiv.org/abs/2404.06347) |
| Towards Benchmarking and Improving the Temporal Reasoning Capability of Large Language Models | 2023 | arXiv paper | [https://arxiv.org/abs/2306.08952](https://arxiv.org/abs/2306.08952) |

### Representative Snippets

| Query | Relevant document excerpt |
| --- | --- |
| Which position did Patricia de Lille hold in Sep, 2015, given many dated office facts? | Mayor of Cape Town. |
| Which position did Lord Douglas Gordon-Hallyburton hold in Oct, 1833? | Member of the 11th Parliament of the United Kingdom. |
| Who was the head of Russia in Jul, 1999? | Sergei Stepashin. |
| Which team did Glynn Snodin play for in Jan, 1992? | Leeds United F.C. |
| Who was the head of Romania in May, 1935? | Gheorghe Tatarescu. |
