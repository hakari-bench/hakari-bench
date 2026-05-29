# NanoMMTEB-v2 / temp_reason_l1

## Overview

`temp_reason_l1` is a temporal arithmetic retrieval task. Each query asks for
the date after adding a number of years and months to a given month-year, and
the retriever must select the correct month-year answer from many candidate
date strings.

## Details

### What the Original Data Measures

[Towards Benchmarking and Improving the Temporal Reasoning Capability of Large Language Models](https://arxiv.org/abs/2306.08952)
introduces TempReason to test temporal calculation and reasoning. The MTEB
retrieval version uses the level-1 offset questions as queries and the resulting
dates as documents.

### Observed Data Profile

The split has 200 queries, 10,000 documents, and 200 positive qrels. Each query
has one positive. Queries average 49.88 characters; answer documents average
9.00 characters and are nearly all short month-year strings such as `May, 1732`.

### BM25 Difficulty

Using the dataset-provided BM25 candidate column, BM25 reaches nDCG@10 = 0.0161
and hit@10 = 0.0350. Lexical matching is almost irrelevant because the answer is
computed; the correct month and year often do not appear in the query.

### Training Data That May Help

Useful training data includes temporal arithmetic, date normalization,
calendar-offset QA, and retrieval formulations where the answer is a computed
date. Training should avoid evaluation question-answer pairs and exact answer
candidate labels.

### Synthetic Data Guidance

Generate many month-year offset questions with varied year ranges, month
boundaries, and near-answer distractors. Include negatives one month or one year
away from the correct answer to force computation rather than string overlap.

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
| Nano set | NanoMMTEB-v2 |
| Backing dataset | NanoMMTEB-v2 |
| Task / split | temp_reason_l1 |
| Hugging Face dataset | [hakari-bench/NanoMMTEB-v2](https://huggingface.co/datasets/hakari-bench/NanoMMTEB-v2) |
| Source dataset | [mteb/TempReasonL1](https://huggingface.co/datasets/mteb/TempReasonL1) |
| Language | multilingual |
| Category | natural_language |
| Queries | 200 |
| Documents | 10000 |
| Positive qrels | 200 |
| BM25 nDCG@10 | 0.0161 |
| BM25 hit@10 | 0.0350 |
| BM25 Recall@100 | 0.0350 |
| BM25 candidate subset | top-500 (`bm25`) |
| Dense nDCG@10 | 0.0488 |
| Dense hit@10 | 0.1050 |
| Dense Recall@100 | 0.6450 |
| Dense candidate subset | top-500 (`harrier_oss_v1_270m`) |
| Reranking hybrid nDCG@10 | 0.0134 |
| Reranking hybrid hit@10 | 0.0350 |
| Reranking hybrid Recall@100 | 0.3650 |
| Reranking hybrid candidate subset | top-100 plus optional rank-101 safeguard (`reranking_hybrid`) |
| Reranking hybrid candidates / query | 100-101 |
| Reranking hybrid safeguard rows | 127 |
| Query length avg chars | 49.88 |
| Document length avg chars | 9.00 |

### Public Sources

- [Towards Benchmarking and Improving the Temporal Reasoning Capability of Large Language Models](https://arxiv.org/abs/2306.08952).
- [TempReason repository](https://github.com/DAMO-NLP-SG/TempReason).
- [mteb/TempReasonL1](https://huggingface.co/datasets/mteb/TempReasonL1).

### Hugging Face Links

- Nano dataset: [hakari-bench/NanoMMTEB-v2](https://huggingface.co/datasets/hakari-bench/NanoMMTEB-v2)
- Source dataset: [mteb/TempReasonL1](https://huggingface.co/datasets/mteb/TempReasonL1)

### Source Reference Table

| Title | Year | Type | URL |
| --- | ---: | --- | --- |
| Towards Benchmarking and Improving the Temporal Reasoning Capability of Large Language Models | 2023 | task paper | https://arxiv.org/abs/2306.08952 |
| TempReason repository | 2023 | repository | https://github.com/DAMO-NLP-SG/TempReason |
| mteb/TempReasonL1 | 2024 | dataset card | https://huggingface.co/datasets/mteb/TempReasonL1 |

## Machine-Readable Metadata

<!-- benchmark-task-metadata:v1 -->

```yaml
benchmark_task_metadata:
  schema_version: 1
  document_status: first_pass
  nano_set: NanoMMTEB-v2
  backing_dataset: NanoMMTEB-v2
  dataset_id: hakari-bench/NanoMMTEB-v2
  task_name: temp_reason_l1
  split_name: temp_reason_l1
  language: multilingual
  category: natural_language
  document_path: docs/benchmark_tasks/NanoMMTEB-v2/temp_reason_l1.md
  source_research:
    primary_source_type: task_paper
    paper_pdf_or_html_checked: true
    no_paper_note: null
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
    multi_positive_query_percent: 0.0
  text_stats_chars:
    query_mean: 49.875
    document_mean: 8.9975
  bm25:
    ndcg_at_10: 0.016083465550765213
    hit_at_10: 0.035
    source: dataset_candidate_subset
  learning:
    original_train_split: available
    evaluation_split_origin: test
    train_eval_overlap_audit: not_audited
    leakage_note: do not train on this Nano split's temporal questions, qrels, or
      answer strings
    useful_training_data:
    - temporal arithmetic QA
    - date normalization examples
    - calendar offset reasoning data
    - retrieval pairs with computed date answers
    synthetic_data:
      document_generation: candidate month-year answer strings and near-answer distractors
      question_generation: month-year offset questions with varied month and year
        boundaries
      answerability: positive answer should be the exact computed month-year
    multi_positive_training: single_positive_question_document_focus
  links:
    nano_dataset: https://huggingface.co/datasets/hakari-bench/NanoMMTEB-v2
    source_urls:
    - label: TempReason arXiv
      url: https://arxiv.org/abs/2306.08952
    - label: TempReason repository
      url: https://github.com/DAMO-NLP-SG/TempReason
    - label: mteb/TempReasonL1
      url: https://huggingface.co/datasets/mteb/TempReasonL1
    source_notes: []
  references:
  - title: Towards Benchmarking and Improving the Temporal Reasoning Capability of
      Large Language Models
    url: https://arxiv.org/abs/2306.08952
    year: 2023
    is_paper: true
    source_confidence: definitive_paper_link
  candidate_subsets:
    bm25:
      config: bm25
      label: BM25
      source: dataset_candidate_subset
      top_k: 500
      ndcg_at_10: 0.0160834656
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
      ndcg_at_10: 0.0133905059
      hit_at_10: 0.035
      recall_at_100: 0.365
      candidate_count_min: 100
      candidate_count_max: 101
      candidate_count_mean: 100.635
      query_count: 200
      query_coverage: 1.0
      relevant_coverage_at_100: 0.365
      safeguard_positive_rows: 127
      rows_with_101_candidates: 127
```
