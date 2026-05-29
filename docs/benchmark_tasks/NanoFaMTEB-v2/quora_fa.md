# NanoFaMTEB-v2 / quora_fa

## Overview

`quora_fa` is a Persian duplicate-question retrieval task. The query is a
question, and the positive document is a semantically equivalent or closely
matching question.

## Details

### What the Original Data Measures

[FaMTEB](https://arxiv.org/abs/2502.11571) includes Persian retrieval datasets
created through translations and Persian data curation. This split uses
`MCINext/quora-fa-v2`, a Persian Quora-style retrieval dataset, evaluated in the
MTEB framework described by [MTEB](https://arxiv.org/abs/2210.07316).

### Observed Data Profile

The Nano split has 200 queries, 10,000 candidate questions, and 570 positive
qrels. Queries average 48.67 characters and candidate documents average 60.81
characters. Positives per query average 2.85, with a maximum of 47.

Observed examples are everyday or factual questions, and positives are paraphrased
questions rather than answer passages.

### BM25 Difficulty

Using the dataset-provided BM25 candidate column and the best-ranked positive,
BM25 reaches nDCG@10 = 0.8832 and hit@10 = 0.9550. It ranks 159 positives first.

BM25 is strong because duplicate questions often share rare topic words, but
semantic paraphrases still produce non-top-1 cases.

### Training Data That May Help

Helpful data includes Persian question paraphrase pairs, duplicate-question
retrieval, and multilingual Quora translations. Exclude evaluation question IDs
and positives.

### Synthetic Data Guidance

Generate Persian question paraphrases with different wording, word order, and
specificity. Hard negatives should share the main topic but ask a different
intent.

## Example Data

| Query | Positive document |
| --- | --- |
| بهترین سریال‌های درام کدام‌اند؟ (31 chars) | بهترین سریال‌های درام کدام‌ها هستند؟ (36 chars) |
| آیا ریاضیات را به عنوان هنر می‌بینید یا علم؟ (44 chars) | آیا ریاضی هنر است یا علم؟ (25 chars) |
| به نظر شما بهترین آهنگ کلاسیک تمام دوران کدام است؟ (50 chars) | بهترین قطعه موسیقی کلاسیک تمام دوران کدام است؟ (46 chars) |
| بهترین موسسات آموزش آزمون جی‌مات در دهلی/NCR کدام‌ها هستند؟ (59 chars) | بهترین موسسه آموزش آزمون جی‌مات در منطقه دهلی ان‌سی‌آر کدام است؟ (64 chars) |
| بهترین نقاط قوت ارتش هند کدامند؟ (32 chars) | بزرگترین نقاط قوت ارتش هند کدامند؟ (34 chars) |

## Dataset Information

| Field | Value |
| --- | --- |
| Nano set | NanoFaMTEB-v2 |
| Backing dataset | NanoFaMTEB-v2 |
| Task / split | quora_fa |
| Hugging Face dataset | [hakari-bench/NanoFaMTEB-v2](https://huggingface.co/datasets/hakari-bench/NanoFaMTEB-v2) |
| Language | fa |
| Category | natural_language |
| Queries | 200 |
| Documents | 10000 |
| Positive qrels | 570 |
| Positives per query | avg 2.85, min 1, median 1.0, max 47 |
| BM25 nDCG@10 | 0.8393 |
| BM25 hit@10 | 0.9550 |
| BM25 Recall@100 | 0.8895 |
| BM25 candidate subset | top-500 (`bm25`) |
| Dense nDCG@10 | 0.9122 |
| Dense hit@10 | 0.9500 |
| Dense Recall@100 | 0.9298 |
| Dense candidate subset | top-500 (`harrier_oss_v1_270m`) |
| Reranking hybrid nDCG@10 | 0.8861 |
| Reranking hybrid hit@10 | 0.9850 |
| Reranking hybrid Recall@100 | 0.9439 |
| Reranking hybrid candidate subset | top-100 plus optional rank-101 safeguard (`reranking_hybrid`) |
| Reranking hybrid candidates / query | 100-101 |
| Reranking hybrid safeguard rows | 1 |
| Query length avg chars | 48.67 |
| Document length avg chars | 60.81 |

### Public Sources

- [FaMTEB: Massive Text Embedding Benchmark in Persian Language](https://arxiv.org/abs/2502.11571).
- [MTEB: Massive Text Embedding Benchmark](https://arxiv.org/abs/2210.07316).
- [MCINext/quora-fa-v2 dataset card](https://huggingface.co/datasets/MCINext/quora-fa-v2).

### Hugging Face Links

- Nano dataset: [hakari-bench/NanoFaMTEB-v2](https://huggingface.co/datasets/hakari-bench/NanoFaMTEB-v2)
- Source dataset: [MCINext/quora-fa-v2](https://huggingface.co/datasets/MCINext/quora-fa-v2)

### Source Reference Table

| Title | Year | Type | URL |
| --- | ---: | --- | --- |
| FaMTEB: Massive Text Embedding Benchmark in Persian Language | 2025 | arXiv paper | https://arxiv.org/abs/2502.11571 |
| MTEB: Massive Text Embedding Benchmark | 2023 | arXiv paper | https://arxiv.org/abs/2210.07316 |
| MCINext/quora-fa-v2 | 2025 | dataset card | https://huggingface.co/datasets/MCINext/quora-fa-v2 |

## Machine-Readable Metadata

<!-- benchmark-task-metadata:v1 -->

```yaml
benchmark_task_metadata:
  schema_version: 1
  document_status: first_pass
  nano_set: NanoFaMTEB-v2
  backing_dataset: NanoFaMTEB-v2
  dataset_id: hakari-bench/NanoFaMTEB-v2
  task_name: quora_fa
  split_name: quora_fa
  language: fa
  category: natural_language
  document_path: docs/benchmark_tasks/NanoFaMTEB-v2/quora_fa.md
  source_research:
    primary_source_type: benchmark_paper
    paper_pdf_or_html_checked: true
  counts:
    queries: 200
    documents: 10000
    positive_qrels: 570
  positives_per_query:
    average: 2.85
    min: 1
    median: 1.0
    max: 47
    multi_positive_queries: 78
  text_stats_chars:
    query_mean: 48.67
    document_mean: 60.814
  bm25:
    ndcg_at_10: 0.8392840284548829
    hit_at_10: 0.955
    source: dataset_candidate_subset
  links:
    nano_dataset: https://huggingface.co/datasets/hakari-bench/NanoFaMTEB-v2
    source_urls:
    - label: FaMTEB arXiv
      url: https://arxiv.org/abs/2502.11571
    - label: MCINext/quora-fa-v2
      url: https://huggingface.co/datasets/MCINext/quora-fa-v2
  references:
  - title: 'FaMTEB: Massive Text Embedding Benchmark in Persian Language'
    url: https://arxiv.org/abs/2502.11571
    year: 2025
    is_paper: true
  candidate_subsets:
    bm25:
      config: bm25
      label: BM25
      source: dataset_candidate_subset
      top_k: 500
      ndcg_at_10: 0.8392840285
      hit_at_10: 0.955
      recall_at_100: 0.8894736842
      candidate_count_min: 500
      candidate_count_max: 500
      candidate_count_mean: 500.0
      query_count: 200
      query_coverage: 1.0
      relevant_coverage_at_100: 0.8894736842
    dense:
      config: harrier_oss_v1_270m
      label: Dense
      source: dataset_candidate_subset
      top_k: 500
      ndcg_at_10: 0.912197763
      hit_at_10: 0.95
      recall_at_100: 0.9298245614
      candidate_count_min: 500
      candidate_count_max: 500
      candidate_count_mean: 500.0
      query_count: 200
      query_coverage: 1.0
      relevant_coverage_at_100: 0.9298245614
    reranking_hybrid:
      config: reranking_hybrid
      label: Reranking hybrid
      source: dataset_candidate_subset
      top_k: 100
      ndcg_at_10: 0.8860743454
      hit_at_10: 0.985
      recall_at_100: 0.9438596491
      candidate_count_min: 100
      candidate_count_max: 101
      candidate_count_mean: 100.005
      query_count: 200
      query_coverage: 1.0
      relevant_coverage_at_100: 0.9438596491
      safeguard_positive_rows: 1
      rows_with_101_candidates: 1
```
