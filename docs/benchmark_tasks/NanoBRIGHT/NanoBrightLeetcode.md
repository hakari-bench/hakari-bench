# NanoBRIGHT / NanoBrightLeetcode

## Overview

`NanoBrightLeetcode` is the LeetCode-style coding slice of BRIGHT. Queries are
algorithmic programming problems, and relevant documents are solved problems
that share the same algorithmic design or data-structure technique.

## Details

### What the Original Data Measures

[BRIGHT](https://arxiv.org/abs/2407.12883) describes LeetCode as a coding
retrieval task where problem descriptions are queries and positive documents are
similar solved problems annotated by LeetCode. Each document contains a problem
statement and a Python solution. The paper keeps real-world scenario problems
where identifying the underlying algorithm or data structure requires reasoning,
then combines LeetCode problems and CodeSearchNet Python code into the corpus.

### Observed Data Profile

The split has 142 queries, 10,000 documents, and 262 positive qrels. Queries
average 1459.30 characters and are full programming problem statements with
examples and constraints. Documents average 1079.62 characters and often include
Python code plus a problem description. Positives average 1.85 per query, with
about half of queries having multiple positives.

### BM25 Difficulty

Using the dataset-provided BM25 candidate column, BM25 reaches nDCG@10 =
0.2705 and hit@10 = 0.5915. It ranks 16 queries with a positive first, and the
median best positive rank is 7.5. Lexical overlap helps when two problems share
graph, array, or dynamic-programming vocabulary, but the intended relevance is
the algorithmic pattern, not the story text.

### Training Data That May Help

Useful data includes non-overlapping coding-problem similarity pairs, solved
algorithm problems with tags, code-search pairs, and hard negatives that share
input types but require a different algorithm. Do not train on the exact
LeetCode pairs used by this Nano split.

### Synthetic Data Guidance

Generate full programming problems with examples, constraints, and reference
solutions. Positives should be different problems that use the same algorithmic
idea, such as BFS, interval DP, bitmask DP, union-find, or greedy scheduling.
Hard negatives should share entities or data structures but require a different
solution pattern.

## Example Data

| Query | Positive document |
| --- | --- |
| You are given a **0-indexed** 2D integer array `grid` of size `m x n`. Each cell has one of two values: * `0` represents an **empty** cell, * `1` represents an **obstacle** that may be removed. You can move up, down, left, or ... [truncated 225 chars](1162 chars) | from collections import deque """You are given an `m x n` integer matrix `grid` where each cell is either `0` (empty) or `1` (obstacle). You can move up, down, left, or right from and to an empty cell in **one step**. Return ... [truncated 225 chars](2061 chars) |
| Alice and Bob want to water `n` plants in their garden. The plants are arranged in a row and are labeled from `0` to `n - 1` from left to right where the `ith` plant is located at `x = i`. Each plant needs a specific amount o ... [truncated 225 chars](2955 chars) | from collections import defaultdict """You want to water `n` plants in your garden with a watering can. The plants are arranged in a row and are labeled from `0` to `n - 1` from left to right where the `ith` plant is located ... [truncated 225 chars](3089 chars) |
| You are given an `m x n` binary matrix `grid`. An island is a group of `1`'s (representing land) connected **4-directionally** (horizontal or vertical.) You may assume all four edges of the grid are surrounded by water. The * ... [truncated 225 chars](979 chars) | def islandPerimeter(grid): """You are given `row x col` `grid` representing a map where `grid[i][j] = 1` represents land and `grid[i][j] = 0` represents water. Grid cells are connected **horizontally/vertically** (not diagona ... [truncated 225 chars](1442 chars) |
| You are given an array of `n` pairs `pairs` where `pairs[i] = [lefti, righti]` and `lefti < righti`. A pair `p2 = [c, d]` **follows** a pair `p1 = [a, b]` if `b < c`. A **chain** of pairs can be formed in this fashion. Return ... [truncated 225 chars](747 chars) | def lengthOfLIS(nums): """Given an integer array `nums`, return _the length of the longest **strictly increasing**_ _**subsequence**_. **Example 1:** **Input:** nums = \[10,9,2,5,3,7,101,18\] **Output:** 4 **Explanation:** Th ... [truncated 225 chars](868 chars) |
| In the "100 game " two players take turns adding, to a running total, any integer from `1` to `10`. The player who first causes the running total to **reach or exceed** 100 wins. What if we change the game so that players **c ... [truncated 225 chars](1356 chars) | def getMoneyAmount(n: int) -> int: """We are playing the Guessing Game. The game will work as follows: 1. I pick a number between `1` and `n`. 2. You guess a number. 3. If you guess the right number, **you win the game**. 4. ... [truncated 225 chars](2787 chars) |

## Dataset Information

| Field | Value |
| --- | --- |
| Nano set | NanoBRIGHT |
| Backing dataset | NanoBRIGHT |
| Task / split | NanoBrightLeetcode |
| Source task | LeetCode |
| Hugging Face dataset | [hakari-bench/NanoBRIGHT](https://huggingface.co/datasets/hakari-bench/NanoBRIGHT) |
| Source dataset | [xlangai/BRIGHT](https://huggingface.co/datasets/xlangai/BRIGHT) |
| Language | en |
| Category | natural_language |
| Queries | 142 |
| Documents | 10000 |
| Positive qrels | 262 |
| Positives per query | avg 1.85, min 1, median 1, max 5 |
| Multi-positive queries | 70 (49.30%) |
| BM25 nDCG@10 | 0.2705 |
| BM25 hit@10 | 0.5915 |
| Query length avg chars | 1459.30 |
| Document length avg chars | 1079.62 |

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
  task_name: NanoBrightLeetcode
  split_name: NanoBrightLeetcode
  source_task: LeetCode
  source_dataset_id: xlangai/BRIGHT
  language: en
  category: natural_language
  document_path: docs/benchmark_tasks/NanoBRIGHT/NanoBrightLeetcode.md
  source_research:
    primary_source_type: benchmark_paper
    paper_pdf_or_html_checked: true
    no_paper_note: null
  counts:
    queries: 142
    documents: 10000
    positive_qrels: 262
  positives_per_query:
    average: 1.8450704225352113
    min: 1
    median: 1.0
    max: 5
    multi_positive_queries: 70
    multi_positive_query_percent: 49.29577464788732
  text_stats_chars:
    query_mean: 1459.3028169014085
    document_mean: 1079.6235
  bm25:
    ndcg_at_10: 0.270523544902632
    hit_at_10: 0.5915492957746479
    source: dataset_bm25_column
  learning:
    original_train_split: unknown
    evaluation_split_origin: BRIGHT LeetCode evaluation split
    train_eval_overlap_audit: not_audited
    leakage_note: exclude NanoBRIGHT LeetCode queries and similar-problem positives
    useful_training_data:
      - non-overlapping coding-problem similarity pairs
      - solved algorithm problems with tags
      - code-search and algorithm explanation pairs
    synthetic_data:
      document_generation: solved programming problems with Python solutions and constraints
      question_generation: full algorithmic problem statements with examples
      answerability: positives should use the same algorithmic design despite different story wording
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
    - title: "BRIGHT: A Realistic and Challenging Benchmark for Reasoning-Intensive Retrieval"
      url: https://arxiv.org/abs/2407.12883
      year: 2024
      doi: 10.48550/arXiv.2407.12883
      is_paper: true
      source_confidence: definitive_paper_link
```
