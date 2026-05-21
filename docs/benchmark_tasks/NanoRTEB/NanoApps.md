# NanoRTEB / NanoApps

## Overview

`NanoRTEB / NanoApps` retrieves Python solution code for long natural-language
programming challenge statements from APPS.

## Details

### What the Original Data Measures

[Measuring Coding Challenge Competence With APPS](https://arxiv.org/abs/2105.09938)
introduces APPS as a benchmark of 10,000 coding problems collected from
competitive-programming and interview-style sources. The original benchmark
evaluates whether a model can synthesize correct programs from problem
statements and hidden tests.

RTEB repurposes APPS as retrieval: the query is the full problem statement and
the positive document is a Python solution. This makes the task a problem-to-code
matching benchmark rather than code generation.

### Observed Data Profile

The split has 200 queries, 8,754 documents, and 200 positive qrel rows. Each
query has one positive. Queries are long programming statements averaging
1,675.41 characters, while documents average 573.12 characters. Some solution
documents are very long because they include full submissions or helper code.

### BM25 Difficulty

Using the dataset-provided BM25 candidate column, BM25 reaches nDCG@10 =
0.0097 and hit@10 = 0.0150. It ranks only one positive at rank 1 and three in
the top 10.

This is extremely hard for lexical retrieval because problem statements and
solutions share few surface terms. A model must map constraints and examples to
algorithmic structure and code behavior.

### Training Data That May Help

Useful training data includes problem-statement-to-solution retrieval,
competitive-programming code search, code contest submissions with statement
metadata, and hard negatives from problems requiring similar data structures but
different algorithms.

### Synthetic Data Guidance

Generate or mine programming statements paired with accepted solutions. Include
hard negatives from same-topic problems, such as two-pointer, dynamic
programming, or greedy tasks with similar wording. Avoid training only on
function-name/docstring pairs; APPS queries are long contest statements.

## Example Data

| Query | Positive document |
| --- | --- |
| On the way to Rio de Janeiro Ostap kills time playing with a grasshopper he took with him in a special box. Ostap builds a line of length n such that some cells of this line are empty and some contain obstacles. Then, he plac ... [truncated 225 chars](2427 chars) | from math import * from sys import * from queue import * from decimal import * n,k=(int(z) for z in input().split()) s=input() i=0 while i<len(s) and s[i] not in ["G","T"]: i+=1 i+=k while i<len(s) and s[i] not in ["G","T","# ... [truncated 225 chars](300 chars) |
| The All-Berland National Olympiad in Informatics has just ended! Now Vladimir wants to upload the contest from the Olympiad as a gym to a popular Codehorses website. Unfortunately, the archive with Olympiad's data is a mess. ... [truncated 225 chars](2762 chars) | n = int(input()) t = [1] + [0] * n b, a = d = [], [] h, s = [], [] for i in range(n): f, k = input().split() d[int(k)].append(f) m = len(a) for i in a: if i.isdigit() and i[0] != '0': j = int(i) if 0 < j <= m: t[j] = 1 elif m ... [truncated 225 chars](1311 chars) |
| You are fighting with Zmei Gorynich — a ferocious monster from Slavic myths, a huge dragon-like reptile with multiple heads! $m$ Initially Zmei Gorynich has $x$ heads. You can deal $n$ types of blows. If you deal a blow of th ... [truncated 225 chars](2047 chars) | for _ in range(int(input())): n, x = list(map(int, input().split())) A = [] for _1 in range(n): d, h = list(map(int, input().split())) A.append([d, h]) A.sort(reverse=True) if A[0][0] >= x: print(1) else: x -= A[0][0] mz = 0 ... [truncated 225 chars](434 chars) |
| Salem gave you $n$ sticks with integer positive lengths $a_1, a_2, \ldots, a_n$. For every stick, you can change its length to any other positive integer length (that is, either shrink or stretch it). The cost of changing the ... [truncated 225 chars](1556 chars) | n = int(input()) a = list(map(int,input().split())) t = 0 mn = 1000000000 for i in range(1,100): cur = 0 for j in range(n): cur += max(0,abs(i-a[j])-1) if cur < mn: mn = cur t = i print(t,mn) (227 chars) |
| Polycarp is crazy about round numbers. He especially likes the numbers divisible by 10^{k}. In the given number of n Polycarp wants to remove the least number of digits to get a number that is divisible by 10^{k}. For example ... [truncated 225 chars](1533 chars) | s = input().split() k = int(s[1]) s = s[0] if s.count('0') < k: if s.count('0') > 0: print(len(s) - 1) else: print(len(s)) return have = 0 its = 0 for i in range(len(s) - 1, -1, -1): its += 1 if s[i] == '0': have += 1 if have ... [truncated 225 chars](320 chars) |

## Dataset Information

| Field | Value |
| --- | --- |
| Nano set | NanoRTEB |
| Backing dataset | NanoRTEB |
| Task / split | NanoApps |
| Hugging Face dataset | [hakari-bench/NanoRTEB](https://huggingface.co/datasets/hakari-bench/NanoRTEB) |
| Source dataset | [codeparrot/apps](https://huggingface.co/datasets/codeparrot/apps) |
| Language | en |
| Category | code |
| Queries | 200 |
| Documents | 8,754 |
| Positive qrels | 200 |
| BM25 nDCG@10 | 0.0097 |
| BM25 hit@10 | 0.0150 |
| Query length avg chars | 1,675.41 |
| Document length avg chars | 573.12 |

### Public Sources

- [Measuring Coding Challenge Competence With APPS](https://arxiv.org/abs/2105.09938), task paper.
- [codeparrot/apps](https://huggingface.co/datasets/codeparrot/apps), source dataset card.
- [Introducing RTEB: A New Standard for Retrieval Evaluation](https://huggingface.co/blog/rteb), RTEB benchmark announcement.

### Hugging Face Links

- Nano dataset: [hakari-bench/NanoRTEB](https://huggingface.co/datasets/hakari-bench/NanoRTEB)
- Source task dataset: [codeparrot/apps](https://huggingface.co/datasets/codeparrot/apps)

### Source Reference Table

| Title | Year | Type | URL |
| --- | ---: | --- | --- |
| Measuring Coding Challenge Competence With APPS | 2021 | task paper | https://arxiv.org/abs/2105.09938 |
| codeparrot/apps |  | dataset card | https://huggingface.co/datasets/codeparrot/apps |
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
  task_name: NanoApps
  split_name: NanoApps
  language: en
  category: code
  document_path: docs/benchmark_tasks/NanoRTEB/NanoApps.md
  source_research:
    primary_source_type: task_paper
    paper_pdf_or_html_checked: true
    no_paper_note: null
  counts:
    queries: 200
    documents: 8754
    positive_qrels: 200
  positives_per_query:
    average: 1.0
    min: 1
    median: 1.0
    max: 1
    multi_positive_queries: 0
    multi_positive_query_percent: 0.0
  text_stats_chars:
    query_mean: 1675.41
    document_mean: 573.12
  bm25:
    ndcg_at_10: 0.0097
    hit_at_10: 0.015
    source: dataset_bm25_column
  example_count: 5
```
