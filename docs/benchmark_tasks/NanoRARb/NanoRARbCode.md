# NanoRARb / NanoRARbCode

## Overview

`NanoRARbCode` is a code reasoning retrieval task. Queries are programming
prompts or partially specified functions, and the positive document is the code
answer or implementation.

## Details

### What the Original Data Measures

[RAR-b: Reasoning as Retrieval Benchmark](https://arxiv.org/abs/2404.06347)
builds a pooled code task from HumanEvalPack and MBPP evaluation queries, with
CodeSearchNet and TinyCode-style examples used to enlarge the answer corpus. It
uses code retrieval as a symbolic reasoning probe because the retriever must
match specifications to implementations.

The source references include [CodeSearchNet Challenge](https://arxiv.org/abs/1909.09436)
and [OctoPack](https://arxiv.org/abs/2308.07124), reflecting the code-search and
instruction-tuned code-data background used around the corpus.

### Observed Data Profile

The Nano split has 200 queries, 10,000 candidate documents, and 200 positive
qrels. Queries average 470.08 characters, and code documents average 256.00
characters.

Observed queries include function signatures and docstrings. Positives are code
snippets, often only the missing function body.

### BM25 Difficulty

Using the dataset-provided BM25 candidate column, BM25 reaches nDCG@10 = 0.0263
and hit@10 = 0.0350. It ranks 3 positives first.

Lexical search is weak because the query describes behavior while the positive
is executable code. Good retrieval needs program semantics, not only identifier
matching.

### Training Data That May Help

Helpful data includes code search, docstring-to-code retrieval, unit-test-backed
program synthesis pairs, and HumanEval/MBPP-style tasks outside the evaluation
queries. Avoid NanoRARb code prompts and solutions.

### Synthetic Data Guidance

Generate function docstrings, signatures, examples, and matching solutions in
multiple languages. Hard negatives should share identifiers or APIs but fail the
specified behavior.

## Example Data

| Query | Positive document |
| --- | --- |
| Finish the following code based on the docstring: def digitSum(s): """Task Write a function that takes a string as input and returns the sum of the upper characters only' ASCII codes. Examples: digitSum("") => 0 digitSum("abA ... [truncated 225 chars](412 chars) | if s == "": return 0 return sum(ord(char) if char.isupper() else 0 for char in s) (85 chars) |
| Finish the following code based on the docstring: def get_odd_collatz(n): """ Given a positive integer n, return a sorted list that has the odd numbers in collatz sequence. The Collatz conjecture is a conjecture in mathematic ... [truncated 225 chars](892 chars) | if n%2==0: odd_collatz = [] else: odd_collatz = [n] while n > 1: if n % 2 == 0: n = n/2 else: n = n*3 + 1 if n%2 == 1: odd_collatz.append(int(n)) return sorted(odd_collatz) (275 chars) |
| Finish the following code based on the docstring: def rounded_avg(n, m): """You are given two positive integers n and m, and your task is to compute the average of the integers from n through m (including n and m). Round the ... [truncated 225 chars](489 chars) | if m < n: return -1 summation = 0 for i in range(n, m+1): summation += i return bin(round(summation/(m - n + 1))) (141 chars) |
| Finish the following code based on the docstring: from typing import List, Tuple def rolling_max(numbers: List[int]) -> List[int]: """ From a given list of integers, generate a list of rolling maximum element found until give ... [truncated 225 chars](337 chars) | running_max = None result = [] for n in numbers: if running_max is None: running_max = n else: running_max = max(running_max, n) result.append(running_max) return result (232 chars) |
| Finish the following code based on the docstring: def solve(s): """You are given a string s. if s[i] is a letter, reverse its case from lower to upper or vise versa, otherwise keep it as it is. If the string contains no lette ... [truncated 225 chars](416 chars) | flg = 0 idx = 0 new_str = list(s) for i in s: if i.isalpha(): new_str[idx] = i.swapcase() flg = 1 idx += 1 s = "" for i in new_str: s += i if flg == 0: return s[len(s)::-1] return s (265 chars) |

## Dataset Information

| Field | Value |
| --- | --- |
| Nano set | NanoRARb |
| Backing dataset | NanoRARb |
| Task / split | NanoRARbCode |
| Hugging Face dataset | [hakari-bench/NanoRARb](https://huggingface.co/datasets/hakari-bench/NanoRARb) |
| Language | en |
| Category | natural_language |
| Queries | 200 |
| Documents | 10000 |
| Positive qrels | 200 |
| BM25 nDCG@10 | 0.1318 |
| BM25 hit@10 | 0.2150 |
| BM25 Recall@100 | 0.4450 |
| BM25 candidate subset | top-500 (`bm25`) |
| Dense nDCG@10 | 0.1173 |
| Dense hit@10 | 0.2000 |
| Dense Recall@100 | 0.4350 |
| Dense candidate subset | top-500 (`harrier_oss_v1_270m`) |
| Reranking hybrid nDCG@10 | 0.1773 |
| Reranking hybrid hit@10 | 0.3000 |
| Reranking hybrid Recall@100 | 0.5750 |
| Reranking hybrid candidate subset | top-100 plus optional rank-101 safeguard (`reranking_hybrid`) |
| Reranking hybrid candidates / query | 100-101 |
| Reranking hybrid safeguard rows | 85 |
| Query length avg chars | 470.08 |
| Document length avg chars | 256.00 |

### Public Sources

- [RAR-b: Reasoning as Retrieval Benchmark](https://arxiv.org/abs/2404.06347).
- [CodeSearchNet Challenge: Evaluating the State of Semantic Code Search](https://arxiv.org/abs/1909.09436).
- [OctoPack: Instruction Tuning Code Large Language Models](https://arxiv.org/abs/2308.07124).

### Hugging Face Links

- Nano dataset: [hakari-bench/NanoRARb](https://huggingface.co/datasets/hakari-bench/NanoRARb)

### Source Reference Table

| Title | Year | Type | URL |
| --- | ---: | --- | --- |
| RAR-b: Reasoning as Retrieval Benchmark | 2024 | arXiv paper | https://arxiv.org/abs/2404.06347 |
| CodeSearchNet Challenge: Evaluating the State of Semantic Code Search | 2019 | arXiv paper | https://arxiv.org/abs/1909.09436 |
| OctoPack: Instruction Tuning Code Large Language Models | 2023 | arXiv paper | https://arxiv.org/abs/2308.07124 |

## Machine-Readable Metadata

<!-- benchmark-task-metadata:v1 -->

```yaml
benchmark_task_metadata:
  schema_version: 1
  document_status: first_pass
  nano_set: NanoRARb
  backing_dataset: NanoRARb
  dataset_id: hakari-bench/NanoRARb
  task_name: NanoRARbCode
  split_name: NanoRARbCode
  language: en
  category: natural_language
  document_path: docs/benchmark_tasks/NanoRARb/NanoRARbCode.md
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
    query_mean: 470.08
    document_mean: 255.998
  bm25:
    ndcg_at_10: 0.1318144120626158
    hit_at_10: 0.215
    source: dataset_candidate_subset
  links:
    nano_dataset: https://huggingface.co/datasets/hakari-bench/NanoRARb
    source_urls:
    - label: RAR-b arXiv
      url: https://arxiv.org/abs/2404.06347
    - label: CodeSearchNet arXiv
      url: https://arxiv.org/abs/1909.09436
    - label: OctoPack arXiv
      url: https://arxiv.org/abs/2308.07124
  references:
  - title: 'RAR-b: Reasoning as Retrieval Benchmark'
    url: https://arxiv.org/abs/2404.06347
    year: 2024
    is_paper: true
  - title: 'CodeSearchNet Challenge: Evaluating the State of Semantic Code Search'
    url: https://arxiv.org/abs/1909.09436
    year: 2019
    is_paper: true
  - title: 'OctoPack: Instruction Tuning Code Large Language Models'
    url: https://arxiv.org/abs/2308.07124
    year: 2023
    is_paper: true
  candidate_subsets:
    bm25:
      config: bm25
      label: BM25
      source: dataset_candidate_subset
      top_k: 500
      ndcg_at_10: 0.1318144121
      hit_at_10: 0.215
      recall_at_100: 0.445
      candidate_count_min: 500
      candidate_count_max: 500
      candidate_count_mean: 500.0
      query_count: 200
      query_coverage: 1.0
      relevant_coverage_at_100: 0.445
    dense:
      config: harrier_oss_v1_270m
      label: Dense
      source: dataset_candidate_subset
      top_k: 500
      ndcg_at_10: 0.1172756841
      hit_at_10: 0.2
      recall_at_100: 0.435
      candidate_count_min: 500
      candidate_count_max: 500
      candidate_count_mean: 500.0
      query_count: 200
      query_coverage: 1.0
      relevant_coverage_at_100: 0.435
    reranking_hybrid:
      config: reranking_hybrid
      label: Reranking hybrid
      source: dataset_candidate_subset
      top_k: 100
      ndcg_at_10: 0.1773298312
      hit_at_10: 0.3
      recall_at_100: 0.575
      candidate_count_min: 100
      candidate_count_max: 101
      candidate_count_mean: 100.425
      query_count: 200
      query_coverage: 1.0
      relevant_coverage_at_100: 0.575
      safeguard_positive_rows: 85
      rows_with_101_candidates: 85
```
