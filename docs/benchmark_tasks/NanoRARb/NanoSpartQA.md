# NanoRARb / NanoSpartQA

## Overview

`NanoSpartQA` is a spatial reasoning answer retrieval task. Queries describe
blocks and objects with spatial relations, and the retriever must find the
correct answer phrase.

## Details

### What the Original Data Measures

[RAR-b: Reasoning as Retrieval Benchmark](https://arxiv.org/abs/2404.06347)
uses SpartQA as a level-2 spatial reasoning task. [SpartQA: A Textual Question
Answering Benchmark for Spatial Reasoning](https://arxiv.org/abs/2104.05832)
introduces QA examples that require tracking spatial relations in text.

This split measures whether a retriever can encode a spatial scene and select
the answer, not just match object names.

### Observed Data Profile

The Nano split has 200 queries, 1,592 candidate documents, and 384 positive
qrels. Queries average 654.85 characters, while answers average 49.80
characters. This is the only observed NanoRARb split here with multiple
positives for some queries, averaging 1.92 positives per query.

Observed queries list blocks, colors, sizes, and relative positions. Positives
are short spatial answer phrases such as "the medium blue square that is in
block B."

### BM25 Difficulty

Using the dataset-provided BM25 candidate column and the best-ranked positive
per query, BM25 reaches nDCG@10 = 0.2321 and hit@10 = 0.3350. It ranks 26
positives first.

Lexical overlap with object labels helps, but solving the task requires
composing spatial relations across a dense scene description.

### Training Data That May Help

Helpful data includes textual spatial QA, scene-graph QA, and retrieval pairs
where answers refer to objects selected by spatial constraints. Exclude NanoRARb
queries, answers, and qrels.

### Synthetic Data Guidance

Generate textual scenes with blocks, shapes, colors, and relative positions.
Construct questions whose answers require relation composition, and add
distractors that share object names but violate location constraints.

## Example Data

| Query | Positive document |
| --- | --- |
| There are three blocks. Lets call them A, B and C. Block A is below B and block B is below C. Block A has one small yellow circle. Block B has a big black square and a big blue square. To the left of and above a medium blue c ... [truncated 225 chars](797 chars) | both of them (12 chars) |
| We have three blocks, A, B and C. Blocks B and C are above A. Block A contains one medium black square and a medium blue square. Below the medium blue square there is the medium black square. Block B contains one medium yello ... [truncated 225 chars](484 chars) | both of them (12 chars) |
| We have three blocks, A, B and C. Block B is below block C and it is to the left of block A. Block A has a small black triangle. Block B has a medium black triangle, one big blue circle and one small blue triangle. The big bl ... [truncated 225 chars](669 chars) | both of them (12 chars) |
| We have three blocks. We call them A, B and C. Block B is below and C is above A. Block A contains one big black square. Block B has one small blue square and one big yellow triangle. It also has a medium blue square. This sh ... [truncated 225 chars](761 chars) | the yellow thing that is touching the right edge of a block (59 chars) |
| There are three blocks, A, B and C. Block A is below C. Block C is to the right of B. Block A has a medium blue square. Block B contains a medium black square. Block C contains two medium yellow squares. There is also one med ... [truncated 225 chars](565 chars) | none of them (12 chars) |

## Dataset Information

| Field | Value |
| --- | --- |
| Nano set | NanoRARb |
| Backing dataset | NanoRARb |
| Task / split | NanoSpartQA |
| Hugging Face dataset | [hakari-bench/NanoRARb](https://huggingface.co/datasets/hakari-bench/NanoRARb) |
| Language | en |
| Category | natural_language |
| Queries | 200 |
| Documents | 1592 |
| Positive qrels | 384 |
| Positives per query | avg 1.92, min 1, median 1.0, max 3 |
| BM25 nDCG@10 | 0.1888 |
| BM25 hit@10 | 0.3750 |
| BM25 Recall@100 | 0.5260 |
| BM25 candidate subset | top-500 (`bm25`) |
| Dense nDCG@10 | 0.2634 |
| Dense hit@10 | 0.4950 |
| Dense Recall@100 | 0.4870 |
| Dense candidate subset | top-500 (`harrier_oss_v1_270m`) |
| Reranking hybrid nDCG@10 | 0.3419 |
| Reranking hybrid hit@10 | 0.5600 |
| Reranking hybrid Recall@100 | 0.5443 |
| Reranking hybrid candidate subset | top-100 plus optional rank-101 safeguard (`reranking_hybrid`) |
| Reranking hybrid candidates / query | 100-101 |
| Reranking hybrid safeguard rows | 37 |
| Query length avg chars | 654.85 |
| Document length avg chars | 49.80 |

### Public Sources

- [RAR-b: Reasoning as Retrieval Benchmark](https://arxiv.org/abs/2404.06347).
- [SpartQA: A Textual Question Answering Benchmark for Spatial Reasoning](https://arxiv.org/abs/2104.05832).

### Hugging Face Links

- Nano dataset: [hakari-bench/NanoRARb](https://huggingface.co/datasets/hakari-bench/NanoRARb)

### Source Reference Table

| Title | Year | Type | URL |
| --- | ---: | --- | --- |
| RAR-b: Reasoning as Retrieval Benchmark | 2024 | arXiv paper | https://arxiv.org/abs/2404.06347 |
| SpartQA: A Textual Question Answering Benchmark for Spatial Reasoning | 2021 | arXiv paper | https://arxiv.org/abs/2104.05832 |

## Machine-Readable Metadata

<!-- benchmark-task-metadata:v1 -->

```yaml
benchmark_task_metadata:
  schema_version: 1
  document_status: first_pass
  nano_set: NanoRARb
  backing_dataset: NanoRARb
  dataset_id: hakari-bench/NanoRARb
  task_name: NanoSpartQA
  split_name: NanoSpartQA
  language: en
  category: natural_language
  document_path: docs/benchmark_tasks/NanoRARb/NanoSpartQA.md
  source_research:
    primary_source_type: benchmark_paper
    paper_pdf_or_html_checked: true
  counts:
    queries: 200
    documents: 1592
    positive_qrels: 384
  positives_per_query:
    average: 1.92
    min: 1
    median: 1.0
    max: 3
    multi_positive_queries: 92
  text_stats_chars:
    query_mean: 654.85
    document_mean: 49.79711055276382
  bm25:
    ndcg_at_10: 0.188797063880075
    hit_at_10: 0.375
    source: dataset_candidate_subset
  links:
    nano_dataset: https://huggingface.co/datasets/hakari-bench/NanoRARb
    source_urls:
    - label: RAR-b arXiv
      url: https://arxiv.org/abs/2404.06347
    - label: SpartQA arXiv
      url: https://arxiv.org/abs/2104.05832
  references:
  - title: 'RAR-b: Reasoning as Retrieval Benchmark'
    url: https://arxiv.org/abs/2404.06347
    year: 2024
    is_paper: true
  - title: 'SpartQA: A Textual Question Answering Benchmark for Spatial Reasoning'
    url: https://arxiv.org/abs/2104.05832
    year: 2021
    is_paper: true
  candidate_subsets:
    bm25:
      config: bm25
      label: BM25
      source: dataset_candidate_subset
      top_k: 500
      ndcg_at_10: 0.1887970639
      hit_at_10: 0.375
      recall_at_100: 0.5260416667
      candidate_count_min: 500
      candidate_count_max: 500
      candidate_count_mean: 500.0
      query_count: 200
      query_coverage: 1.0
      relevant_coverage_at_100: 0.5260416667
    dense:
      config: harrier_oss_v1_270m
      label: Dense
      source: dataset_candidate_subset
      top_k: 500
      ndcg_at_10: 0.2633728519
      hit_at_10: 0.495
      recall_at_100: 0.4869791667
      candidate_count_min: 500
      candidate_count_max: 500
      candidate_count_mean: 500.0
      query_count: 200
      query_coverage: 1.0
      relevant_coverage_at_100: 0.4869791667
    reranking_hybrid:
      config: reranking_hybrid
      label: Reranking hybrid
      source: dataset_candidate_subset
      top_k: 100
      ndcg_at_10: 0.3418953726
      hit_at_10: 0.56
      recall_at_100: 0.5442708333
      candidate_count_min: 100
      candidate_count_max: 101
      candidate_count_mean: 100.185
      query_count: 200
      query_coverage: 1.0
      relevant_coverage_at_100: 0.5442708333
      safeguard_positive_rows: 37
      rows_with_101_candidates: 37
```
