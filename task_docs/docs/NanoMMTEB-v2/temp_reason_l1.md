# NanoMMTEB-v2 / temp_reason_l1

## Overview

`NanoMMTEB-v2 / temp_reason_l1` is a temporal arithmetic retrieval task from
TempReason. Each query asks for the month-year obtained after adding a number
of years and months to a starting month-year, and documents are candidate
month-year answer strings. The Nano split has 200 queries, 10,000 documents,
and 200 positive qrel rows, with exactly one positive document per query.
Current diagnostics show dense retrieval as the strongest profile by recall,
while BM25 and `reranking_hybrid` are very weak at the top ranks. The task is a
computed-answer retrieval problem, not a lexical matching problem.

## Details

### What the Original Data Measures

TempReason was introduced to benchmark temporal reasoning in language models.
The level-1 task uses simple calendar offsets: given a starting month and year,
add a specified number of years and months to compute the target month-year. In
the MTEB retrieval formulation, the question is the query and answer strings
are retrievable documents.

The task measures whether retrieval can behave like temporal arithmetic. The
correct answer often does not appear in the query, so models must represent the
operation and computed result rather than matching terms.

### Observed Data Profile

The Nano split contains 200 queries, 10,000 documents, and 200 positive qrel
rows. Every query has exactly one positive document. Queries average 49.88
characters, while documents average 9.00 characters.

Queries are short English prompts such as asking for the time a number of years
and months after a given month-year. Documents are terse month-year strings such
as "Sep, 1180" or "May, 2008". Many candidate documents are near-answer
distractors differing by one month or one year.

### BM25 Evaluation Profile

The dataset-provided BM25 candidate subset contains 500 candidates per query and
achieves nDCG@10 = 0.0161, hit@10 = 0.0350, and recall@100 = 0.0350. BM25 is
almost unusable for this task.

This is expected because the correct computed month-year usually does not occur
in the query. Lexical matching can only use fragments such as the starting
month, starting year, or the word "month"; those are often misleading for the
answer string.

### Dense Evaluation Profile

The dense `harrier_oss_v1_270m` candidate subset contains 500 candidates per
query and achieves nDCG@10 = 0.0488, hit@10 = 0.1050, and recall@100 = 0.6450.
Dense retrieval is the strongest observed profile by recall@100, but its
top-rank quality remains low.

Dense embeddings appear to capture some structure of date strings and temporal
offset questions, but a standard embedding model is not a reliable calendar
calculator. It can retrieve broad neighborhoods of plausible dates while
failing to rank the exact computed answer first.

### Reranking Hybrid Evaluation Profile

The `reranking_hybrid` candidate subset contains mostly 100 candidates per
query, with 127 queries using a rank-101 safeguard row. It achieves nDCG@10 =
0.0134, hit@10 = 0.0350, and recall@100 = 0.3650. Hybrid retrieval is below
dense retrieval and similar to BM25 at the top ranks.

The large number of safeguard rows shows that the positive often needs explicit
injection into the candidate pool. Sparse evidence does not help much because
the answer is computed, and hybrid fusion can dilute the already fragile dense
signal.

### Metric Interpretation for Model Researchers

This task is single-positive: each query has one exact computed month-year
answer. Hit@10 measures whether that answer appears near the top. nDCG@10 is
sensitive to exact rank, and recall@100 measures whether the correct answer is
available to a reranker.

The task should not be read as ordinary semantic retrieval. It is a diagnostic
for whether retrieval models can support symbolic temporal computation or at
least preserve candidate answers for a calculator-like reranker.

### Query and Relevance Type Tendencies

Queries contain a starting month-year and a temporal offset in years and months.
Relevant documents are exact month-year strings. Candidate documents are short
and often lexically indistinguishable except for the month and year.

The task rewards calendar arithmetic, month-boundary handling, year carry, and
exact answer selection. It penalizes models that treat the query as a bag of
date tokens.

### Representative Failure Modes

BM25 can retrieve the starting month or starting year rather than the computed
answer. Dense retrieval can retrieve nearby years or months because they are
semantically and lexically similar date strings. Hybrid retrieval can under-rank
the correct answer when lexical evidence points to the input date rather than
the output date.

Rerankers should compute the calendar offset explicitly or use structured date
normalization before scoring candidates.

### Training Data That May Help

Useful training data includes temporal arithmetic QA, date normalization
examples, calendar offset reasoning data, and retrieval pairs with computed
date answers. The Nano split's temporal questions, qrels, and answer strings
should be excluded from training.

Synthetic data can generate many month-year offset questions with varied year
ranges, month boundaries, and near-answer distractors. Negatives one month or
one year away from the correct answer are important because they force
calculation rather than string overlap.

### Model Improvement Notes

Dense retrievers should not be expected to solve this task without explicit
temporal reasoning support. Sparse systems are structurally mismatched.
Rerankers or tool-augmented systems should parse the query, compute the target
month-year, and compare candidates exactly.

For hybrid systems, `NanoMMTEB-v2 / temp_reason_l1` is a warning case:
`reranking_hybrid` does not improve top-rank quality over BM25 and is far below
dense recall. The best path is computation-aware reranking rather than better
lexical fusion.

## Example Data

| Query | Positive document |
| --- | --- |
| What is the time 9 year and 10 month after Nov, 1170 [52 chars] | Sep, 1180 [9 chars] |
| What is the time 5 year and 12 month after Jun, 1243 [52 chars] | Jun, 1249 [9 chars] |
| What is the time 6 year and 4 month after Jun, 1905 [51 chars] | Oct, 1911 [9 chars] |

### Public Sources

- [Towards Benchmarking and Improving the Temporal Reasoning Capability of Large Language Models](https://arxiv.org/abs/2306.08952),
  2023.
- [TempReason repository](https://github.com/DAMO-NLP-SG/TempReason).
- [mteb/TempReasonL1](https://huggingface.co/datasets/mteb/TempReasonL1).
- [hakari-bench/NanoMMTEB-v2](https://huggingface.co/datasets/hakari-bench/NanoMMTEB-v2),
  Nano benchmark dataset.

### Source Reference Table

| Title | Year | Type | URL |
| --- | ---: | --- | --- |
| Towards Benchmarking and Improving the Temporal Reasoning Capability of Large Language Models | 2023 | task paper | [https://arxiv.org/abs/2306.08952](https://arxiv.org/abs/2306.08952) |
| TempReason repository | 2023 | repository | [https://github.com/DAMO-NLP-SG/TempReason](https://github.com/DAMO-NLP-SG/TempReason) |
| mteb/TempReasonL1 | 2024 | dataset card | [https://huggingface.co/datasets/mteb/TempReasonL1](https://huggingface.co/datasets/mteb/TempReasonL1) |

### Representative Snippets

| Query pattern | Positive document pattern |
| --- | --- |
| A query asking for 9 years and 10 months after Nov, 1170. | The computed answer string "Sep, 1180." |
| A query asking for 5 years and 12 months after Jun, 1243. | The computed answer string "Jun, 1249." |
| A query asking for 6 years and 4 months after Jun, 1905. | The computed answer string "Oct, 1911." |
| A query asking for 10 years and 1 month after Oct, 1093. | The computed answer string "Nov, 1103." |
| A query asking for 12 months after May, 2007. | The computed answer string "May, 2008." |
