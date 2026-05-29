# NanoRARb / NanoARCChallenge

## Overview

`NanoARCChallenge` recasts AI2 ARC-Challenge science questions as retrieval.
The query is a grade-school science question, and the correct answer option is
hidden in a large answer corpus.

## Details

### What the Original Data Measures

[RAR-b: Reasoning as Retrieval Benchmark](https://arxiv.org/abs/2404.06347)
converts reasoning tasks into full-dataset retrieval by pooling candidate
answers across splits and asking whether the ground-truth answer is retrieved.
For ARC-Challenge, [Think you have solved question answering? Try ARC, the AI2
Reasoning Challenge](https://arxiv.org/abs/1803.05457) describes a science QA
set intentionally focused on questions that are difficult for retrieval and
word-cooccurrence baselines.

This task therefore measures whether a retriever can map a science question to
the correct concise answer, not merely find topical overlap.

### Observed Data Profile

The Nano split has 200 English queries, 9,350 candidate answer documents, and
200 positive qrels. Every query has one positive. Queries average 126.66
characters, while answer documents average 30.94 characters.

Observed examples ask about plankton, experimental review, animal behavior, and
other elementary science concepts. Documents are short answer options, often a
phrase or one sentence.

### BM25 Difficulty

Using the dataset-provided BM25 candidate column, BM25 reaches nDCG@10 = 0.0394
and hit@10 = 0.0800. It ranks only 2 positives first.

The weak lexical baseline fits the ARC-Challenge design: many questions require
scientific reasoning and answer selection rather than direct term matching.

### Training Data That May Help

Helpful data includes science QA answer selection, explanation-backed
multiple-choice QA, and retrieval-formatted ARC-style pairs. Training should
exclude NanoRARb queries, answer documents, and qrels.

### Synthetic Data Guidance

Generate science questions with concise answer options and hard distractors that
share topical terms. Synthetic positives should require causal, physical, or
biological reasoning grounded in the question.

## Example Data

| Query | Positive document |
| --- | --- |
| Some students are performing hardness tests on several substances. X scratches Y. Y scratches Z. Z scratches W. Which of these statements best describes substance W's hardness? (176 chars) | W is the softest of the four substances tested. (47 chars) |
| Hurricanes form over equatorial areas. This is because (54 chars) | solar heating is greatest near the equator. (43 chars) |
| The best description of the troposphere is the layer of the atmosphere with the (79 chars) | greatest density. (17 chars) |
| Copper is an element that is used in electrical wires. What is the smallest unit of copper that still maintains the characteristics of copper? (142 chars) | the atom (8 chars) |
| If you throw each one of these things away, which will decay fastest? (69 chars) | An apple core (13 chars) |

## Dataset Information

| Field | Value |
| --- | --- |
| Nano set | NanoRARb |
| Backing dataset | NanoRARb |
| Task / split | NanoARCChallenge |
| Hugging Face dataset | [hakari-bench/NanoRARb](https://huggingface.co/datasets/hakari-bench/NanoRARb) |
| Language | en |
| Category | natural_language |
| Queries | 200 |
| Documents | 9350 |
| Positive qrels | 200 |
| BM25 nDCG@10 | 0.0386 |
| BM25 hit@10 | 0.0850 |
| BM25 Recall@100 | 0.2250 |
| BM25 candidate subset | top-500 (`bm25`) |
| Dense nDCG@10 | 0.1113 |
| Dense hit@10 | 0.1900 |
| Dense Recall@100 | 0.3600 |
| Dense candidate subset | top-500 (`harrier_oss_v1_270m`) |
| Reranking hybrid nDCG@10 | 0.0642 |
| Reranking hybrid hit@10 | 0.1350 |
| Reranking hybrid Recall@100 | 0.3550 |
| Reranking hybrid candidate subset | top-100 plus optional rank-101 safeguard (`reranking_hybrid`) |
| Reranking hybrid candidates / query | 100-101 |
| Reranking hybrid safeguard rows | 129 |
| Query length avg chars | 126.66 |
| Document length avg chars | 30.94 |

### Public Sources

- [RAR-b: Reasoning as Retrieval Benchmark](https://arxiv.org/abs/2404.06347).
- [Think you have solved question answering? Try ARC, the AI2 Reasoning Challenge](https://arxiv.org/abs/1803.05457).

### Hugging Face Links

- Nano dataset: [hakari-bench/NanoRARb](https://huggingface.co/datasets/hakari-bench/NanoRARb)

### Source Reference Table

| Title | Year | Type | URL |
| --- | ---: | --- | --- |
| RAR-b: Reasoning as Retrieval Benchmark | 2024 | arXiv paper | https://arxiv.org/abs/2404.06347 |
| Think you have solved question answering? Try ARC, the AI2 Reasoning Challenge | 2018 | arXiv paper | https://arxiv.org/abs/1803.05457 |

## Machine-Readable Metadata

<!-- benchmark-task-metadata:v1 -->

```yaml
benchmark_task_metadata:
  schema_version: 1
  document_status: first_pass
  nano_set: NanoRARb
  backing_dataset: NanoRARb
  dataset_id: hakari-bench/NanoRARb
  task_name: NanoARCChallenge
  split_name: NanoARCChallenge
  language: en
  category: natural_language
  document_path: docs/benchmark_tasks/NanoRARb/NanoARCChallenge.md
  source_research:
    primary_source_type: benchmark_paper
    paper_pdf_or_html_checked: true
  counts:
    queries: 200
    documents: 9350
    positive_qrels: 200
  positives_per_query:
    average: 1.0
    min: 1
    median: 1.0
    max: 1
    multi_positive_queries: 0
  text_stats_chars:
    query_mean: 126.66
    document_mean: 30.94235294117647
  bm25:
    ndcg_at_10: 0.03862006820672147
    hit_at_10: 0.085
    source: dataset_candidate_subset
  links:
    nano_dataset: https://huggingface.co/datasets/hakari-bench/NanoRARb
    source_urls:
    - label: RAR-b arXiv
      url: https://arxiv.org/abs/2404.06347
    - label: ARC arXiv
      url: https://arxiv.org/abs/1803.05457
  references:
  - title: 'RAR-b: Reasoning as Retrieval Benchmark'
    url: https://arxiv.org/abs/2404.06347
    year: 2024
    is_paper: true
  - title: Think you have solved question answering? Try ARC, the AI2 Reasoning Challenge
    url: https://arxiv.org/abs/1803.05457
    year: 2018
    is_paper: true
  candidate_subsets:
    bm25:
      config: bm25
      label: BM25
      source: dataset_candidate_subset
      top_k: 500
      ndcg_at_10: 0.0386200682
      hit_at_10: 0.085
      recall_at_100: 0.225
      candidate_count_min: 500
      candidate_count_max: 500
      candidate_count_mean: 500.0
      query_count: 200
      query_coverage: 1.0
      relevant_coverage_at_100: 0.225
    dense:
      config: harrier_oss_v1_270m
      label: Dense
      source: dataset_candidate_subset
      top_k: 500
      ndcg_at_10: 0.1113404108
      hit_at_10: 0.19
      recall_at_100: 0.36
      candidate_count_min: 500
      candidate_count_max: 500
      candidate_count_mean: 500.0
      query_count: 200
      query_coverage: 1.0
      relevant_coverage_at_100: 0.36
    reranking_hybrid:
      config: reranking_hybrid
      label: Reranking hybrid
      source: dataset_candidate_subset
      top_k: 100
      ndcg_at_10: 0.0641517955
      hit_at_10: 0.135
      recall_at_100: 0.355
      candidate_count_min: 100
      candidate_count_max: 101
      candidate_count_mean: 100.645
      query_count: 200
      query_coverage: 1.0
      relevant_coverage_at_100: 0.355
      safeguard_positive_rows: 129
      rows_with_101_candidates: 129
```
