# NanoRTEB / NanoMBPP

## Overview

`NanoRTEB / NanoMBPP` retrieves Python implementations for Mostly Basic Python
Programming task descriptions.

## Details

### What the Original Data Measures

[Program Synthesis with Large Language Models](https://arxiv.org/abs/2108.07732)
introduces MBPP as a set of 974 entry-level Python programming tasks with
natural-language descriptions and tests. The original task evaluates program
synthesis; the RTEB version evaluates retrieval of the correct implementation
from a code corpus.

The task is short-description-to-code retrieval. It measures whether a model can
map simple functional requirements to small Python programs.

### Observed Data Profile

The split has 200 queries, 972 documents, and 200 positive qrel rows. Every
query has one positive. Queries are short, averaging 78.40 characters, and
documents average 180.80 characters. Examples include basic algorithms,
set operations, heap operations, primality checks, and dynamic programming.

### BM25 Difficulty

Using the dataset-provided BM25 candidate column, BM25 reaches nDCG@10 =
0.3029 and hit@10 = 0.4700. It ranks 32 positives at rank 1 and 94 in the top
10.

BM25 benefits from exact terms such as "heap queue" or "tuple lists", but short
queries and short code snippets often have little overlap. Semantic intent and
API knowledge are important.

### Training Data That May Help

Useful data includes MBPP-style problem-code pairs, docstring-to-function
retrieval, introductory Python exercises, and hard negatives from functions with
the same keywords but different outputs.

### Synthetic Data Guidance

Generate small Python tasks with reference implementations and tests. Include
nearby negatives such as two list-processing functions or two matrix dynamic
programming functions. Keep task descriptions short and direct.

## Example Data

| Query | Positive document |
| --- | --- |
| Write a python function to check whether the sum of divisors are same or not. (77 chars) | import math def divSum(n): sum = 1; i = 2; while(i * i <= n): if (n % i == 0): sum = (sum + i +math.floor(n / i)); i += 1; return sum; def areEquivalent(num1,num2): return divSum(num1) == divSum(num2); (269 chars) |
| Write a python function to find the element occurring odd number of times. (74 chars) | def get_Odd_Occurrence(arr,arr_size): for i in range(0,arr_size): count = 0 for j in range(0,arr_size): if arr[i] == arr[j]: count+=1 if (count % 2 != 0): return arr[i] return -1 (275 chars) |
| Write a function to find all words which are at least 4 characters long in a string by using regex. (99 chars) | import re def find_char_long(text): return (re.findall(r"\b\w{4,}\b", text)) (80 chars) |
| Write a python function to count the number of integral co-ordinates that lie inside a square. (94 chars) | def count_Intgral_Points(x1,y1,x2,y2): return ((y2 - y1 - 1) * (x2 - x1 - 1)) (83 chars) |
| Write a function to sort a list of elements using comb sort. (60 chars) | def comb_sort(nums): shrink_fact = 1.3 gaps = len(nums) swapped = True i = 0 while gaps > 1 or swapped: gaps = int(float(gaps) / shrink_fact) swapped = False i = 0 while gaps + i < len(nums): if nums[i] > nums[i+gaps]: nums[i ... [truncated 225 chars](424 chars) |

## Dataset Information

| Field | Value |
| --- | --- |
| Nano set | NanoRTEB |
| Backing dataset | NanoRTEB |
| Task / split | NanoMBPP |
| Hugging Face dataset | [hakari-bench/NanoRTEB](https://huggingface.co/datasets/hakari-bench/NanoRTEB) |
| Source dataset | [google-research-datasets/mbpp](https://huggingface.co/datasets/google-research-datasets/mbpp) |
| Language | en |
| Category | code |
| Queries | 200 |
| Documents | 972 |
| Positive qrels | 200 |
| BM25 nDCG@10 | 0.3029 |
| BM25 hit@10 | 0.4700 |
| Query length avg chars | 78.40 |
| Document length avg chars | 180.80 |

### Public Sources

- [Program Synthesis with Large Language Models](https://arxiv.org/abs/2108.07732), task paper.
- [google-research-datasets/mbpp](https://huggingface.co/datasets/google-research-datasets/mbpp), source dataset card.
- [Introducing RTEB: A New Standard for Retrieval Evaluation](https://huggingface.co/blog/rteb), RTEB benchmark announcement.

### Hugging Face Links

- Nano dataset: [hakari-bench/NanoRTEB](https://huggingface.co/datasets/hakari-bench/NanoRTEB)
- Source task dataset: [google-research-datasets/mbpp](https://huggingface.co/datasets/google-research-datasets/mbpp)

### Source Reference Table

| Title | Year | Type | URL |
| --- | ---: | --- | --- |
| Program Synthesis with Large Language Models | 2021 | task paper | https://arxiv.org/abs/2108.07732 |
| google-research-datasets/mbpp |  | dataset card | https://huggingface.co/datasets/google-research-datasets/mbpp |
| Introducing RTEB: A New Standard for Retrieval Evaluation | 2025 | benchmark article | https://huggingface.co/blog/rteb |

## Machine-Readable Metadata

<!-- benchmark-task-metadata:v1 -->

```yaml
benchmark_task_metadata:
  schema_version: 1
  document_status: first_pass
  nano_set: NanoRTEB
  backing_dataset: NanoRTEB
  dataset_id: hakari-bench/NanoRTEB
  task_name: NanoMBPP
  split_name: NanoMBPP
  language: en
  category: code
  document_path: docs/benchmark_tasks/NanoRTEB/NanoMBPP.md
  source_research:
    primary_source_type: task_paper
    paper_pdf_or_html_checked: true
    no_paper_note: null
  counts:
    queries: 200
    documents: 972
    positive_qrels: 200
  positives_per_query:
    average: 1.0
    min: 1
    median: 1.0
    max: 1
    multi_positive_queries: 0
    multi_positive_query_percent: 0.0
  text_stats_chars:
    query_mean: 78.4
    document_mean: 180.8
  bm25:
    ndcg_at_10: 0.3029
    hit_at_10: 0.47
    source: dataset_bm25_column
  example_count: 5
```
