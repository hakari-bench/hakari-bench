# NanoBRIGHT / NanoBrightPonyLong

## Overview

`NanoBrightPonyLong` is the long-document Pony programming-language retrieval
task from BRIGHT. Queries are Pony coding tasks, and relevant documents are
longer manual pages or documentation sections that contain the needed syntax or
language feature.

## Details

### What the Original Data Measures

[BRIGHT](https://arxiv.org/abs/2407.12883) includes Pony because rare-language
programming often requires consulting syntax documentation whose wording does
not resemble the user task. The long-document setting uses larger documentation
units, so the retriever must identify the right page even when the answer is
only one section among many.

### Observed Data Profile

The split has 112 queries, 577 documents, and 769 positive qrels. Queries
average 388.97 characters and contain a task plus a Pony function template.
Documents average 3553.13 characters, much longer than the passage-level Pony
split but still shorter than the long StackExchange pages. Positives average
6.87 per query, and almost every query has multiple positives.

### BM25 Difficulty

Using the dataset-provided BM25 candidate column, BM25 reaches nDCG@10 =
0.2674 and hit@10 = 0.9464. It ranks 21 queries with a positive first, and the
median best positive rank is 3. The long Pony task is much easier for BM25 than
the short-passage Pony task because page-level documentation aggregates many
related syntax terms, but ranking the best section still requires understanding
the implementation need.

### Training Data That May Help

Useful data includes document-level programming manual retrieval, rare-language
coding tasks aligned to manual pages, and synthetic tasks labeled with required
constructs. Exclude the exact Pony templates and documentation positives from
this evaluation split.

### Synthetic Data Guidance

Generate Pony tasks that require language constructs such as loops,
conditionals, primitives, iterators, errors, or numeric operators, then pair
them with complete manual pages. Hard negatives should be pages about adjacent
constructs that look plausible but do not contain the needed feature.

## Example Data

| Query | Positive document |
| --- | --- |
| I will use the programming language pony. Problem: You are given an array of integers stones where stones[i] is the weight of the ith stone. We are playing a game with the stones. On each turn, we choose the heaviest two ston ... [truncated 225 chars](730 chars) | # Control Structures To do real work in a program you have to be able to make decisions, iterate through collections of items and perform actions repeatedly. For this, you need control structures. Pony has control structures ... [truncated 225 chars](12050 chars) |
| I will use the programming language pony. Problem: You are given an integer array nums. The unique elements of an array are the elements that appear exactly once in the array. Write a function that returns the sum of all the ... [truncated 225 chars](323 chars) | # Control Structures To do real work in a program you have to be able to make decisions, iterate through collections of items and perform actions repeatedly. For this, you need control structures. Pony has control structures ... [truncated 225 chars](12050 chars) |
| I will use the programming language pony. Problem: Given an array of integers nums, write a function that returns the number of good pairs. A pair (i, j) is called good if nums[i] == nums[j] and i < j. Here is the code templa ... [truncated 225 chars](281 chars) | # Control Structures To do real work in a program you have to be able to make decisions, iterate through collections of items and perform actions repeatedly. For this, you need control structures. Pony has control structures ... [truncated 225 chars](12050 chars) |
| I will use the programming language pony. Problem: Given an integer number n, write a function that returns the difference between the product of its digits and the sum of its digits. For example, if n = 234, product of digit ... [truncated 225 chars](370 chars) | # Control Structures To do real work in a program you have to be able to make decisions, iterate through collections of items and perform actions repeatedly. For this, you need control structures. Pony has control structures ... [truncated 225 chars](12050 chars) |
| I will use the programming language pony. Problem: A string s is nice if, for every letter of the alphabet that s contains, it appears both in uppercase and lowercase. For example, "abABB" is nice because 'A' and 'a' appear, ... [truncated 225 chars](592 chars) | # Control Structures To do real work in a program you have to be able to make decisions, iterate through collections of items and perform actions repeatedly. For this, you need control structures. Pony has control structures ... [truncated 225 chars](12050 chars) |

## Dataset Information

| Field | Value |
| --- | --- |
| Nano set | NanoBRIGHT |
| Backing dataset | NanoBRIGHT |
| Task / split | NanoBrightPonyLong |
| Source task | Pony long-document |
| Hugging Face dataset | [hakari-bench/NanoBRIGHT](https://huggingface.co/datasets/hakari-bench/NanoBRIGHT) |
| Source dataset | [xlangai/BRIGHT](https://huggingface.co/datasets/xlangai/BRIGHT) |
| Language | en |
| Category | natural_language |
| Queries | 112 |
| Documents | 577 |
| Positive qrels | 769 |
| Positives per query | avg 6.87, min 1, median 7, max 12 |
| Multi-positive queries | 111 (99.11%) |
| BM25 nDCG@10 | 0.2244 |
| BM25 hit@10 | 0.8304 |
| BM25 Recall@100 | 0.8765 |
| BM25 candidate subset | top-500 (`bm25`) |
| Dense nDCG@10 | 0.0767 |
| Dense hit@10 | 0.4554 |
| Dense Recall@100 | 0.4174 |
| Dense candidate subset | top-500 (`harrier_oss_v1_270m`) |
| Reranking hybrid nDCG@10 | 0.2871 |
| Reranking hybrid hit@10 | 0.8661 |
| Reranking hybrid Recall@100 | 0.7750 |
| Reranking hybrid candidate subset | top-100 plus optional rank-101 safeguard (`reranking_hybrid`) |
| Reranking hybrid candidates / query | 100 |
| Reranking hybrid safeguard rows | 0 |
| Query length avg chars | 388.97 |
| Document length avg chars | 3553.13 |

### Public Sources

- [BRIGHT: A Realistic and Challenging Benchmark for Reasoning-Intensive Retrieval](https://arxiv.org/abs/2407.12883).
- [BRIGHT project page](https://brightbenchmark.github.io/).
- [xlangai/BRIGHT](https://huggingface.co/datasets/xlangai/BRIGHT).

### Hugging Face Links

- Nano dataset: [hakari-bench/NanoBRIGHT](https://huggingface.co/datasets/hakari-bench/NanoBRIGHT)
- Source dataset: [xlangai/BRIGHT](https://huggingface.co/datasets/xlangai/BRIGHT)
- MTEB dataset record: [mteb/BRIGHT](https://huggingface.co/datasets/mteb/BRIGHT)

### Source Reference Table

| Title | Year | Type | URL |
| --- | ---: | --- | --- |
| BRIGHT: A Realistic and Challenging Benchmark for Reasoning-Intensive Retrieval | 2024 | benchmark paper | https://arxiv.org/abs/2407.12883 |
| BRIGHT project page | 2024 | project page | https://brightbenchmark.github.io/ |
| xlangai/BRIGHT | 2024 | dataset card | https://huggingface.co/datasets/xlangai/BRIGHT |

## Machine-Readable Metadata

<!-- benchmark-task-metadata:v1 -->

```yaml
benchmark_task_metadata:
  schema_version: 1
  document_status: first_pass
  nano_set: NanoBRIGHT
  backing_dataset: NanoBRIGHT
  dataset_id: hakari-bench/NanoBRIGHT
  task_name: NanoBrightPonyLong
  split_name: NanoBrightPonyLong
  source_task: Pony long-document
  source_dataset_id: xlangai/BRIGHT
  language: en
  category: natural_language
  document_path: docs/benchmark_tasks/NanoBRIGHT/NanoBrightPonyLong.md
  source_research:
    primary_source_type: benchmark_paper
    paper_pdf_or_html_checked: true
    no_paper_note: null
  counts:
    queries: 112
    documents: 577
    positive_qrels: 769
  positives_per_query:
    average: 6.866071428571429
    min: 1
    median: 7.0
    max: 12
    multi_positive_queries: 111
    multi_positive_query_percent: 99.10714285714286
  text_stats_chars:
    query_mean: 388.9732142857143
    document_mean: 3553.1282495667247
  bm25:
    ndcg_at_10: 0.2244474654295809
    hit_at_10: 0.8303571428571429
    source: dataset_candidate_subset
  learning:
    original_train_split: unknown
    evaluation_split_origin: BRIGHT Pony long-document evaluation split
    train_eval_overlap_audit: not_audited
    leakage_note: exclude NanoBRIGHT PonyLong task templates and manual-page positives
    useful_training_data:
    - document-level programming manual retrieval
    - rare-language coding tasks aligned to manual pages
    - synthetic tasks labeled with required language constructs
    synthetic_data:
      document_generation: complete Pony manual pages about syntax, control flow,
        errors, and libraries
      question_generation: Pony coding tasks requiring a specific language construct
      answerability: positive page should contain the manual section needed to implement
        the task
    multi_positive_training: multi_positive_objective
  links:
    nano_dataset: https://huggingface.co/datasets/hakari-bench/NanoBRIGHT
    source_urls:
    - label: BRIGHT arXiv
      url: https://arxiv.org/abs/2407.12883
    - label: BRIGHT project
      url: https://brightbenchmark.github.io/
    - label: xlangai/BRIGHT
      url: https://huggingface.co/datasets/xlangai/BRIGHT
    source_notes: []
  references:
  - title: 'BRIGHT: A Realistic and Challenging Benchmark for Reasoning-Intensive
      Retrieval'
    url: https://arxiv.org/abs/2407.12883
    year: 2024
    doi: 10.48550/arXiv.2407.12883
    is_paper: true
    source_confidence: definitive_paper_link
  candidate_subsets:
    bm25:
      config: bm25
      label: BM25
      source: dataset_candidate_subset
      top_k: 500
      ndcg_at_10: 0.2244474654
      hit_at_10: 0.8303571429
      recall_at_100: 0.8764629389
      candidate_count_min: 500
      candidate_count_max: 500
      candidate_count_mean: 500.0
      query_count: 112
      query_coverage: 1.0
      relevant_coverage_at_100: 0.8764629389
    dense:
      config: harrier_oss_v1_270m
      label: Dense
      source: dataset_candidate_subset
      top_k: 500
      ndcg_at_10: 0.076675447
      hit_at_10: 0.4553571429
      recall_at_100: 0.4174252276
      candidate_count_min: 500
      candidate_count_max: 500
      candidate_count_mean: 500.0
      query_count: 112
      query_coverage: 1.0
      relevant_coverage_at_100: 0.4174252276
    reranking_hybrid:
      config: reranking_hybrid
      label: Reranking hybrid
      source: dataset_candidate_subset
      top_k: 100
      ndcg_at_10: 0.2870728499
      hit_at_10: 0.8660714286
      recall_at_100: 0.7750325098
      candidate_count_min: 100
      candidate_count_max: 100
      candidate_count_mean: 100.0
      query_count: 112
      query_coverage: 1.0
      relevant_coverage_at_100: 0.7750325098
      safeguard_positive_rows: 0
      rows_with_101_candidates: 0
```
