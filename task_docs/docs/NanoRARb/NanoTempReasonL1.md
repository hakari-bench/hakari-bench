# NanoRARb / NanoTempReasonL1

## Overview

`NanoTempReasonL1` is an English temporal arithmetic retrieval task from NanoRARb. The query asks for the month-year obtained after adding a number of years and months to a starting month-year, and the relevant document is the resulting date string. Each query has one positive answer. This is a deliberately difficult retrieval formulation because the answer is computed, not retrieved by meaning. BM25 is almost useless, dense retrieval gives much better candidate coverage, and hybrid retrieval improves over BM25 but remains weaker than dense retrieval.

## Details

### What the Original Data Measures

RAR-b uses TempReason as a temporal reasoning probe converted into retrieval. The underlying TempReason work benchmarks temporal reasoning capability, including date arithmetic and reasoning over time relations.

This level-1 split is the most direct form: add an offset of years and months to a given date. The target document is a short date string such as `Sep, 1180`.

### Observed Data Profile

The Nano split contains 200 queries, 10,000 documents, and 200 positive qrel rows. Each query has exactly one positive. Queries average 49.88 characters, and answer documents average only 9.00 characters.

Examples ask for the time several years and months after a starting date. Positive documents are terse month-year strings, typically with no explanatory context.

### BM25 Evaluation Profile

The BM25 candidate subset uses top-500 candidates and reaches nDCG@10 of 0.0125, hit@10 of 0.0350, and recall@100 of 0.0350. BM25 is essentially not solving the task. The correct date may share no useful terms with the query except possibly a month or nearby year.

This shows the limitation of lexical retrieval for computed answers. Term frequency cannot add months, handle year rollover, or normalize a date offset.

### Dense Evaluation Profile

The dense candidate subset from `harrier_oss_v1_270m` uses top-500 candidates and reaches nDCG@10 of 0.0488, hit@10 of 0.1050, and recall@100 of 0.6450. Dense retrieval is still weak at top rank, but its recall@100 is far better than BM25.

The high gap between hit@10 and recall@100 suggests that dense retrieval can often place the answer somewhere in the candidate set but cannot reliably rank the exact date string at the top. Date arithmetic remains a reasoning problem, not a semantic similarity problem.

### Reranking Hybrid Evaluation Profile

The `reranking_hybrid` subset uses top-100 candidates, with 126 rows receiving the optional rank-101 safeguard. It reaches nDCG@10 of 0.0129, hit@10 of 0.0350, and recall@100 of 0.3700. Hybrid retrieval improves coverage over BM25 but is much worse than dense retrieval for recall@100 and does not improve top-ten ranking.

This pattern indicates that sparse signals contribute little to direct date arithmetic. Dense retrieval is the better candidate source, but a true solution requires computation-aware reranking or answer generation.

### Metric Interpretation for Model Researchers

With one positive per query, nDCG@10 measures the rank of the exact date string, hit@10 measures whether the computed date appears in the first ten results, and recall@100 measures candidate availability for reranking.

For TempReasonL1, retrieval metrics are a proxy for whether a model can represent a computed answer. A high-performing system likely needs explicit temporal arithmetic or a reranker that can compute the offset.

### Query and Relevance Type Tendencies

Queries are short date-offset questions. Relevant documents are short date strings with month and year. The corpus contains many nearby distractor dates, making accidental lexical overlap unhelpful.

Relevance is exact computation. A date that is one month or one year off is wrong, even if it looks similar.

### Representative Failure Modes

Common failures include retrieving the starting month, a nearby year, an answer with the right month but wrong year, or a date with the right year but wrong month. BM25 fails because the answer is not stated in the query; dense retrieval can cluster plausible-looking dates without doing arithmetic.

### Training Data That May Help

Useful training data includes temporal arithmetic, date normalization, offset calculation, calendar QA, and retrieval pairs where answers are computed from dates. Evaluation temporal examples and answer strings should be excluded.

### Model Improvement Notes

Models should learn or invoke exact date arithmetic. Hard negatives should include dates near the correct answer, dates with the correct month but wrong year, and dates with correct year but wrong month. This split is a good diagnostic for whether retrieval can handle computed answers at all.

## Example Data

| Query | Positive document |
| --- | --- |
| What is the time 9 year and 10 month after Nov, 1170 [52 chars] | Sep, 1180 [9 chars] |
| What is the time 5 year and 12 month after Jun, 1243 [52 chars] | Jun, 1249 [9 chars] |
| What is the time 6 year and 4 month after Jun, 1905 [51 chars] | Oct, 1911 [9 chars] |

### Source Reference Table

| Title | Year | Type | URL |
| --- | ---: | --- | --- |
| RAR-b: Reasoning as Retrieval Benchmark | 2024 | arXiv paper | [https://arxiv.org/abs/2404.06347](https://arxiv.org/abs/2404.06347) |
| Towards Benchmarking and Improving the Temporal Reasoning Capability of Large Language Models | 2023 | arXiv paper | [https://arxiv.org/abs/2306.08952](https://arxiv.org/abs/2306.08952) |

### Representative Snippets

| Query | Relevant document excerpt |
| --- | --- |
| What is the time 9 years and 10 months after Nov, 1170? | Sep, 1180. |
| What is the time 5 years and 12 months after Jun, 1243? | Jun, 1249. |
| What is the time 6 years and 4 months after Jun, 1905? | Oct, 1911. |
| What is the time 10 years and 1 month after Oct, 1093? | Nov, 1103. |
| What is the time 12 months after May, 2007? | May, 2008. |
