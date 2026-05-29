# NanoRARb / NanoTempReasonL1

## Overview

`NanoTempReasonL1` is a temporal arithmetic retrieval task. The query asks for a
date after adding a number of years and months, and the positive document is the
resulting date string.

## Details

### What the Original Data Measures

[RAR-b: Reasoning as Retrieval Benchmark](https://arxiv.org/abs/2404.06347)
uses TempReason as a level-2 temporal reasoning probe. [Towards Benchmarking and
Improving the Temporal Reasoning Capability of Large Language Models](https://arxiv.org/abs/2306.08952)
introduces the underlying temporal reasoning tasks. This level-1 split is the
most direct date-offset form.

### Observed Data Profile

The Nano split has 200 queries, 10,000 candidate documents, and 200 positive
qrels. Queries average 49.88 characters, and answer documents average 9.00
characters.

Observed positives are short month-year strings such as `Jul, 1663`.

### BM25 Difficulty

Using the dataset-provided BM25 candidate column, BM25 reaches nDCG@10 = 0.0125
and hit@10 = 0.0350. It ranks no positives first.

Lexical matching is almost unhelpful because the answer requires date
calculation, and the target date may share few or no terms with the query.

### Training Data That May Help

Helpful training data includes temporal arithmetic, date normalization, and
question-answer pairs where the answer is computed from offsets. Exclude
NanoRARb temporal examples and answer strings.

### Synthetic Data Guidance

Generate date-offset questions with varied calendars, month boundaries, and
year changes. Include distractor dates near the correct answer.

## Example Data

| Query | Positive document |
| --- | --- |
| What is the time 9 year and 10 month after Nov, 1170 (52 chars) | Sep, 1180 (9 chars) |
| What is the time 5 year and 12 month after Jun, 1243 (52 chars) | Jun, 1249 (9 chars) |
| What is the time 6 year and 4 month after Jun, 1905 (51 chars) | Oct, 1911 (9 chars) |
| What is the time 10 year and 1 month after Oct, 1093 (52 chars) | Nov, 1103 (9 chars) |
| What is the time 12 month after May, 2007 (41 chars) | May, 2008 (9 chars) |

## Dataset Information

| Field | Value |
| --- | --- |
| Nano set | NanoRARb |
| Backing dataset | NanoRARb |
| Task / split | NanoTempReasonL1 |
| Hugging Face dataset | [hakari-bench/NanoRARb](https://huggingface.co/datasets/hakari-bench/NanoRARb) |
| Language | en |
| Category | natural_language |
| Queries | 200 |
| Documents | 10000 |
| Positive qrels | 200 |
| BM25 nDCG@10 | 0.0125 |
| BM25 hit@10 | 0.0350 |
| BM25 Recall@100 | 0.0350 |
| BM25 candidate subset | top-500 (`bm25`) |
| Dense nDCG@10 | 0.0488 |
| Dense hit@10 | 0.1050 |
| Dense Recall@100 | 0.6450 |
| Dense candidate subset | top-500 (`harrier_oss_v1_270m`) |
| Reranking hybrid nDCG@10 | 0.0129 |
| Reranking hybrid hit@10 | 0.0350 |
| Reranking hybrid Recall@100 | 0.3700 |
| Reranking hybrid candidate subset | top-100 plus optional rank-101 safeguard (`reranking_hybrid`) |
| Reranking hybrid candidates / query | 100-101 |
| Reranking hybrid safeguard rows | 126 |
| Query length avg chars | 49.88 |
| Document length avg chars | 9.00 |

### Public Sources

- [RAR-b: Reasoning as Retrieval Benchmark](https://arxiv.org/abs/2404.06347).
- [Towards Benchmarking and Improving the Temporal Reasoning Capability of Large Language Models](https://arxiv.org/abs/2306.08952).

### Hugging Face Links

- Nano dataset: [hakari-bench/NanoRARb](https://huggingface.co/datasets/hakari-bench/NanoRARb)

### Source Reference Table

| Title | Year | Type | URL |
| --- | ---: | --- | --- |
| RAR-b: Reasoning as Retrieval Benchmark | 2024 | arXiv paper | https://arxiv.org/abs/2404.06347 |
| Towards Benchmarking and Improving the Temporal Reasoning Capability of Large Language Models | 2023 | arXiv paper | https://arxiv.org/abs/2306.08952 |

## Machine-Readable Metadata

<!-- benchmark-task-metadata:v1 -->

```yaml
benchmark_task_metadata:
  schema_version: 1
  document_status: first_pass
  nano_set: NanoRARb
  backing_dataset: NanoRARb
  dataset_id: hakari-bench/NanoRARb
  task_name: NanoTempReasonL1
  split_name: NanoTempReasonL1
  language: en
  category: natural_language
  document_path: docs/benchmark_tasks/NanoRARb/NanoTempReasonL1.md
  source_research:
    primary_source_type: benchmark_paper
    paper_pdf_or_html_checked: true
  counts:
    queries: 200
    documents: 10000
    positive_qrels: 200
  positives_per_query:
    average: 1.0
    min: 1
    median: 1.0
    max: 1
    multi_positive_queries: 0
  text_stats_chars:
    query_mean: 49.875
    document_mean: 8.9975
  bm25:
    ndcg_at_10: 0.01245646179238261
    hit_at_10: 0.035
    source: dataset_candidate_subset
  links:
    nano_dataset: https://huggingface.co/datasets/hakari-bench/NanoRARb
    source_urls:
    - label: RAR-b arXiv
      url: https://arxiv.org/abs/2404.06347
    - label: TempReason arXiv
      url: https://arxiv.org/abs/2306.08952
  references:
  - title: 'RAR-b: Reasoning as Retrieval Benchmark'
    url: https://arxiv.org/abs/2404.06347
    year: 2024
    is_paper: true
  - title: Towards Benchmarking and Improving the Temporal Reasoning Capability of
      Large Language Models
    url: https://arxiv.org/abs/2306.08952
    year: 2023
    is_paper: true
  candidate_subsets:
    bm25:
      config: bm25
      label: BM25
      source: dataset_candidate_subset
      top_k: 500
      ndcg_at_10: 0.0124564618
      hit_at_10: 0.035
      recall_at_100: 0.035
      candidate_count_min: 500
      candidate_count_max: 500
      candidate_count_mean: 500.0
      query_count: 200
      query_coverage: 1.0
      relevant_coverage_at_100: 0.035
    dense:
      config: harrier_oss_v1_270m
      label: Dense
      source: dataset_candidate_subset
      top_k: 500
      ndcg_at_10: 0.0488266823
      hit_at_10: 0.105
      recall_at_100: 0.645
      candidate_count_min: 500
      candidate_count_max: 500
      candidate_count_mean: 500.0
      query_count: 200
      query_coverage: 1.0
      relevant_coverage_at_100: 0.645
    reranking_hybrid:
      config: reranking_hybrid
      label: Reranking hybrid
      source: dataset_candidate_subset
      top_k: 100
      ndcg_at_10: 0.0129111858
      hit_at_10: 0.035
      recall_at_100: 0.37
      candidate_count_min: 100
      candidate_count_max: 101
      candidate_count_mean: 100.63
      query_count: 200
      query_coverage: 1.0
      relevant_coverage_at_100: 0.37
      safeguard_positive_rows: 126
      rows_with_101_candidates: 126
```
