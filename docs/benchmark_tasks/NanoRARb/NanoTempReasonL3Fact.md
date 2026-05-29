# NanoRARb / NanoTempReasonL3Fact

## Overview

`NanoTempReasonL3Fact` retrieves answers for harder TempReason level-3 questions
where the query includes supporting temporal facts. The positive document is a
short entity or answer.

## Details

### What the Original Data Measures

[RAR-b: Reasoning as Retrieval Benchmark](https://arxiv.org/abs/2404.06347)
uses level-3 TempReason to probe harder before/after temporal ordering. The
underlying benchmark is [Towards Benchmarking and Improving the Temporal
Reasoning Capability of Large Language Models](https://arxiv.org/abs/2306.08952).
This fact variant supplies relevant dated facts without the full context length.

### Observed Data Profile

The Nano split has 200 queries, 10,000 candidate answers, and 200 positive
qrels. Queries average 1,981.07 characters, and answers average 19.88
characters.

Observed questions ask for a head of government or employer before another
named person or organization.

### BM25 Difficulty

Using the dataset-provided BM25 candidate column, BM25 reaches nDCG@10 = 0.0679
and hit@10 = 0.1400. It ranks 1 positive first.

The supporting facts raise BM25 above the pure version, but ranking still
depends on temporal ordering rather than surface matching.

### Training Data That May Help

Helpful data includes timeline QA, before/after reasoning, and retrieval tasks
where answer candidates are entities selected from dated fact sets.

### Synthetic Data Guidance

Generate compact timeline facts and before/after questions. Include distractors
from adjacent intervals and entities with similar names or roles.

## Example Data

| Query | Positive document |
| --- | --- |
| Question: Who was the chair of Technical University of Munich before Wolfgang A. Herrmann? Facts: Otto Meitinger is the chair of Technical University of Munich from Jan, 1987 to Jan, 1995. Herbert Kupfer is the chair of Techn ... [truncated 225 chars](473 chars) | Otto Meitinger (14 chars) |
| Question: Who was the head of Romania before Alexandru G. Golescu? Facts: Gheorghe Tătărescu is the head of the government of Romania from Jan, 1934 to Dec, 1937. Adrian Năstase is the head of the government of Romania from D ... [truncated 225 chars](4784 chars) | Dimitrie Ghica (14 chars) |
| Question: Which position did Lord Douglas Gordon-Hallyburton hold before Member of the 13th Parliament of the United Kingdom? Facts: Lord Douglas Gordon-Hallyburton holds the position of Member of the 11th Parliament of the U ... [truncated 225 chars](675 chars) | Member of the 12th Parliament of the United Kingdom (51 chars) |
| Question: Which employer did Eduard Winkelmann work for after Imperial University of Dorpat? Facts: Eduard Winkelmann works for Tallinn Cathedral School from Jan, 1860 to Jan, 1865. Eduard Winkelmann works for Heidelberg Univ ... [truncated 225 chars](514 chars) | University of Bern (18 chars) |
| Question: Who was the head of Romania after Adrian Năstase? Facts: Petre Roman is the head of the government of Romania from Dec, 1989 to Oct, 1991. Ludovic Orban is the head of the government of Romania from Nov, 2019 to Dec ... [truncated 225 chars](4777 chars) | Călin Popescu-Tăriceanu (23 chars) |

## Dataset Information

| Field | Value |
| --- | --- |
| Nano set | NanoRARb |
| Backing dataset | NanoRARb |
| Task / split | NanoTempReasonL3Fact |
| Hugging Face dataset | [hakari-bench/NanoRARb](https://huggingface.co/datasets/hakari-bench/NanoRARb) |
| Language | en |
| Category | natural_language |
| Queries | 200 |
| Documents | 10000 |
| Positive qrels | 200 |
| BM25 nDCG@10 | 0.0547 |
| BM25 hit@10 | 0.1150 |
| BM25 Recall@100 | 0.6600 |
| BM25 candidate subset | top-500 (`bm25`) |
| Dense nDCG@10 | 0.2549 |
| Dense hit@10 | 0.4700 |
| Dense Recall@100 | 0.8700 |
| Dense candidate subset | top-500 (`harrier_oss_v1_270m`) |
| Reranking hybrid nDCG@10 | 0.1981 |
| Reranking hybrid hit@10 | 0.4450 |
| Reranking hybrid Recall@100 | 0.9250 |
| Reranking hybrid candidate subset | top-100 plus optional rank-101 safeguard (`reranking_hybrid`) |
| Reranking hybrid candidates / query | 100-101 |
| Reranking hybrid safeguard rows | 15 |
| Query length avg chars | 1981.07 |
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
  task_name: NanoTempReasonL3Fact
  split_name: NanoTempReasonL3Fact
  language: en
  category: natural_language
  document_path: docs/benchmark_tasks/NanoRARb/NanoTempReasonL3Fact.md
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
    query_mean: 1981.07
    document_mean: 19.8842
  bm25:
    ndcg_at_10: 0.05465347978521584
    hit_at_10: 0.115
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
      ndcg_at_10: 0.0546534798
      hit_at_10: 0.115
      recall_at_100: 0.66
      candidate_count_min: 500
      candidate_count_max: 500
      candidate_count_mean: 500.0
      query_count: 200
      query_coverage: 1.0
      relevant_coverage_at_100: 0.66
    dense:
      config: harrier_oss_v1_270m
      label: Dense
      source: dataset_candidate_subset
      top_k: 500
      ndcg_at_10: 0.2548855558
      hit_at_10: 0.47
      recall_at_100: 0.87
      candidate_count_min: 500
      candidate_count_max: 500
      candidate_count_mean: 500.0
      query_count: 200
      query_coverage: 1.0
      relevant_coverage_at_100: 0.87
    reranking_hybrid:
      config: reranking_hybrid
      label: Reranking hybrid
      source: dataset_candidate_subset
      top_k: 100
      ndcg_at_10: 0.1981044614
      hit_at_10: 0.445
      recall_at_100: 0.925
      candidate_count_min: 100
      candidate_count_max: 101
      candidate_count_mean: 100.075
      query_count: 200
      query_coverage: 1.0
      relevant_coverage_at_100: 0.925
      safeguard_positive_rows: 15
      rows_with_101_candidates: 15
```
