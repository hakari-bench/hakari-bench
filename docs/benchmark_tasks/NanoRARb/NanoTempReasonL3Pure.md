# NanoRARb / NanoTempReasonL3Pure

## Overview

`NanoTempReasonL3Pure` retrieves answers for harder before/after temporal
questions without supporting facts. The answer is a short entity string.

## Details

### What the Original Data Measures

[RAR-b: Reasoning as Retrieval Benchmark](https://arxiv.org/abs/2404.06347)
frames TempReason pure settings as retrieval probes where the model must rely on
temporal knowledge and reasoning encoded in the representation. The source
benchmark is [Towards Benchmarking and Improving the Temporal Reasoning
Capability of Large Language Models](https://arxiv.org/abs/2306.08952).

Level 3 asks harder relative temporal questions, such as which employer came
before another employer.

### Observed Data Profile

The Nano split has 200 queries, 10,000 documents, and 200 positive qrels.
Queries average 65.13 characters, and candidate answers average 19.88
characters.

Observed queries are compact before/after questions with no supporting facts.

### BM25 Difficulty

Using the dataset-provided BM25 candidate column, BM25 reaches nDCG@10 = 0.0057
and hit@10 = 0.0100. It ranks no positives first.

The near-zero lexical score shows that pure temporal reasoning is not solved by
matching words in the query to answer strings.

### Training Data That May Help

Helpful data includes temporal knowledge-base QA, timeline ordering examples,
and before/after entity retrieval. Exclude NanoRARb temporal evaluation rows.

### Synthetic Data Guidance

Generate compact before/after questions over timelines, with answer candidates
from adjacent events. Include distractors from the same entity timeline.

## Example Data

| Query | Positive document |
| --- | --- |
| Who was the chair of Technical University of Munich before Wolfgang A. Herrmann? (80 chars) | Otto Meitinger (14 chars) |
| Who was the head of Romania before Alexandru G. Golescu? (56 chars) | Dimitrie Ghica (14 chars) |
| Which position did Lord Douglas Gordon-Hallyburton hold before Member of the 13th Parliament of the United Kingdom? (115 chars) | Member of the 12th Parliament of the United Kingdom (51 chars) |
| Which employer did Eduard Winkelmann work for after Imperial University of Dorpat? (82 chars) | University of Bern (18 chars) |
| Who was the head of Romania after Adrian Năstase? (49 chars) | Călin Popescu-Tăriceanu (23 chars) |

## Dataset Information

| Field | Value |
| --- | --- |
| Nano set | NanoRARb |
| Backing dataset | NanoRARb |
| Task / split | NanoTempReasonL3Pure |
| Hugging Face dataset | [hakari-bench/NanoRARb](https://huggingface.co/datasets/hakari-bench/NanoRARb) |
| Language | en |
| Category | natural_language |
| Queries | 200 |
| Documents | 10000 |
| Positive qrels | 200 |
| BM25 nDCG@10 | 0.0074 |
| BM25 hit@10 | 0.0150 |
| BM25 Recall@100 | 0.0950 |
| BM25 candidate subset | top-500 (`bm25`) |
| Dense nDCG@10 | 0.0707 |
| Dense hit@10 | 0.1550 |
| Dense Recall@100 | 0.5400 |
| Dense candidate subset | top-500 (`harrier_oss_v1_270m`) |
| Reranking hybrid nDCG@10 | 0.0238 |
| Reranking hybrid hit@10 | 0.0600 |
| Reranking hybrid Recall@100 | 0.4150 |
| Reranking hybrid candidate subset | top-100 plus optional rank-101 safeguard (`reranking_hybrid`) |
| Reranking hybrid candidates / query | 100-101 |
| Reranking hybrid safeguard rows | 117 |
| Query length avg chars | 65.13 |
| Document length avg chars | 19.88 |

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
  task_name: NanoTempReasonL3Pure
  split_name: NanoTempReasonL3Pure
  language: en
  category: natural_language
  document_path: docs/benchmark_tasks/NanoRARb/NanoTempReasonL3Pure.md
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
    query_mean: 65.13
    document_mean: 19.8842
  bm25:
    ndcg_at_10: 0.007435684703397398
    hit_at_10: 0.015
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
      ndcg_at_10: 0.0074356847
      hit_at_10: 0.015
      recall_at_100: 0.095
      candidate_count_min: 500
      candidate_count_max: 500
      candidate_count_mean: 500.0
      query_count: 200
      query_coverage: 1.0
      relevant_coverage_at_100: 0.095
    dense:
      config: harrier_oss_v1_270m
      label: Dense
      source: dataset_candidate_subset
      top_k: 500
      ndcg_at_10: 0.0706588195
      hit_at_10: 0.155
      recall_at_100: 0.54
      candidate_count_min: 500
      candidate_count_max: 500
      candidate_count_mean: 500.0
      query_count: 200
      query_coverage: 1.0
      relevant_coverage_at_100: 0.54
    reranking_hybrid:
      config: reranking_hybrid
      label: Reranking hybrid
      source: dataset_candidate_subset
      top_k: 100
      ndcg_at_10: 0.0238066443
      hit_at_10: 0.06
      recall_at_100: 0.415
      candidate_count_min: 100
      candidate_count_max: 101
      candidate_count_mean: 100.585
      query_count: 200
      query_coverage: 1.0
      relevant_coverage_at_100: 0.415
      safeguard_positive_rows: 117
      rows_with_101_candidates: 117
```
