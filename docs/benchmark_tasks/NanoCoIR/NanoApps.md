# NanoCoIR / NanoApps

## Overview

CoIR adapts APPS from a coding-challenge generation benchmark into a
text-to-code retrieval task: the full problem statement, including constraints
and examples, must retrieve a Python solution program. The task is therefore
about recognizing algorithmic intent from competitive-programming prose rather
than matching API names, and the long APPS prompts make distractors with similar
input/output formats especially plausible.

## Details

### What the Original Data Measures

[CoIR](https://arxiv.org/abs/2407.02883) adapts APPS as a text-to-code
retrieval task: the original problem description is used as the query, and
solution code is the retrieval target. The [APPS paper](https://arxiv.org/abs/2105.09938)
describes APPS as 10,000 programming problems collected from open-access coding
challenge sites such as Codewars, AtCoder, Kattis, and Codeforces, with
solutions checked by test cases. In NanoCoIR, the task measures whether a
retriever can map a full algorithmic specification to a semantically correct
Python implementation.

### Observed Data Profile

The Nano split has 200 queries, 8,754 documents, and 200 positive qrels. Each
query has one positive. Queries are long problem statements with input/output
sections and examples, averaging 1,675.41 characters. Documents are mostly short
Python solutions, averaging 573.12 characters, although the candidate pool
contains some very large programs.

### BM25 Difficulty

Using the dataset-provided BM25 candidate column, BM25 reaches nDCG@10 =
0.0097 and hit@10 = 0.0150. Only 3 of 200 positives appear in the top 10, and
the median best positive rank is 100. This is the hardest observed NanoCoIR
split for BM25 because problem statements describe constraints and behavior,
while compact solutions often share few literal terms with the statement.

### Training Data That May Help

Useful training data includes problem-statement-to-solution pairs from APPS-like
coding challenges, hard negatives from other solutions with similar algorithmic
patterns, and code retrieval training that preserves long natural-language
specifications instead of reducing them to short intents.

### Synthetic Data Guidance

Synthetic data should pair full contest-style problem statements with working
solutions and include distractors that solve related but different algorithms.
Generated statements should include constraints and examples so models learn to
use specification details, not just topic words.

### Benchmark Information Leakage

CoIR adapts APPS into a retrieval benchmark with roughly 5k train queries and
3.8k test queries over a 9k-document corpus, and this Nano split is derived from
the CoIR APPS test side. Training on APPS test examples, or on any public APPS
copy that has not been filtered by split and by Nano query/positive hashes, can
leak the benchmark problem statements and solution documents.

The safer use of APPS-like data is to restrict training to upstream train-side
problem-solution pairs and then remove any row whose problem statement, solution,
or normalized token fingerprint matches NanoApps queries, qrels, or positive
documents. Models trained on unfiltered APPS test-derived data may score well on
NanoApps by memorizing contest solutions rather than learning general
problem-to-code retrieval.

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
| Nano set | NanoCoIR |
| Backing dataset | NanoCoIR |
| Task / split | NanoApps |
| Hugging Face dataset | [hakari-bench/NanoCoIR](https://huggingface.co/datasets/hakari-bench/NanoCoIR) |
| Language | en |
| Category | code |
| Queries | 200 |
| Documents | 8754 |
| Positive qrels | 200 |
| BM25 nDCG@10 | 0.0084 |
| BM25 hit@10 | 0.0150 |
| BM25 Recall@100 | 0.0750 |
| BM25 candidate subset | top-500 (`bm25`) |
| Dense nDCG@10 | 0.2528 |
| Dense hit@10 | 0.3500 |
| Dense Recall@100 | 0.6700 |
| Dense candidate subset | top-500 (`harrier_oss_v1_270m`) |
| Reranking hybrid nDCG@10 | 0.1655 |
| Reranking hybrid hit@10 | 0.2750 |
| Reranking hybrid Recall@100 | 0.5400 |
| Reranking hybrid candidate subset | top-100 plus optional rank-101 safeguard (`reranking_hybrid`) |
| Reranking hybrid candidates / query | 100-101 |
| Reranking hybrid safeguard rows | 92 |
| Query length avg chars | 1675.41 |
| Document length avg chars | 573.12 |

### Public Sources

- [CoIR](https://arxiv.org/abs/2407.02883); 2025; Xiangyang Li et al.
- [Measuring Coding Challenge Competence With APPS](https://arxiv.org/abs/2105.09938); 2021; Dan Hendrycks et al.

### Hugging Face Links

- Nano dataset: [hakari-bench/NanoCoIR](https://huggingface.co/datasets/hakari-bench/NanoCoIR)
- Source dataset: [codeparrot/apps](https://huggingface.co/datasets/codeparrot/apps)

### Source Reference Table

| Title | Year | Type | URL |
| --- | ---: | --- | --- |
| CoIR: A Comprehensive Benchmark for Code Information Retrieval Models | 2025 | benchmark paper | https://arxiv.org/abs/2407.02883 |
| Measuring Coding Challenge Competence With APPS | 2021 | source task paper | https://arxiv.org/abs/2105.09938 |

## Machine-Readable Metadata

<!-- benchmark-task-metadata:v1 -->

```yaml
benchmark_task_metadata:
  schema_version: 1
  document_status: first_pass
  nano_set: NanoCoIR
  backing_dataset: NanoCoIR
  dataset_id: hakari-bench/NanoCoIR
  task_name: NanoApps
  split_name: NanoApps
  language: en
  category: code
  document_path: docs/benchmark_tasks/NanoCoIR/NanoApps.md
  source_research:
    primary_source_type: benchmark_paper_and_task_paper
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
    query_mean: 1675.415
    document_mean: 573.1170893305917
  bm25:
    ndcg_at_10: 0.008379588167762148
    hit_at_10: 0.015
    source: dataset_candidate_subset
  learning:
    original_train_split: available
    evaluation_split_origin: CoIR APPS test-derived retrieval split
    train_eval_overlap_audit: not_audited_split_filtering_required
    leakage_note: exclude NanoApps queries, qrels, and positive solution documents;
      do not train on APPS test-derived rows
    leakage_risk:
      source_dataset: APPS / codeparrot/apps
      source_train_queries_reported_by_coir: 5000
      source_test_queries_reported_by_coir: 3800
      risk: upstream APPS test examples can overlap with NanoApps evaluation rows
      recommended_filter: train-side only plus normalized query, solution, and token-fingerprint
        exclusion
    useful_training_data:
    - APPS-style problem-to-solution retrieval pairs
    - competitive-programming solutions with hard negatives
    - long specification to code retrieval data
    synthetic_data:
      document_generation: working Python solutions for contest-style problems
      question_generation: full algorithmic problem statements with constraints
      answerability: positive solution must solve the stated problem
    multi_positive_training: single_positive
  links:
    nano_dataset: https://huggingface.co/datasets/hakari-bench/NanoCoIR
    source_urls:
    - label: CoIR arXiv
      url: https://arxiv.org/abs/2407.02883
    - label: APPS arXiv
      url: https://arxiv.org/abs/2105.09938
    - label: codeparrot/apps
      url: https://huggingface.co/datasets/codeparrot/apps
    source_notes: []
  references:
  - title: 'CoIR: A Comprehensive Benchmark for Code Information Retrieval Models'
    url: https://arxiv.org/abs/2407.02883
    year: 2025
    is_paper: true
    source_confidence: definitive_paper_link
  - title: Measuring Coding Challenge Competence With APPS
    url: https://arxiv.org/abs/2105.09938
    year: 2021
    is_paper: true
    source_confidence: definitive_paper_link
  candidate_subsets:
    bm25:
      config: bm25
      label: BM25
      source: dataset_candidate_subset
      top_k: 500
      ndcg_at_10: 0.0083795882
      hit_at_10: 0.015
      recall_at_100: 0.075
      candidate_count_min: 500
      candidate_count_max: 500
      candidate_count_mean: 500.0
      query_count: 200
      query_coverage: 1.0
      relevant_coverage_at_100: 0.075
    dense:
      config: harrier_oss_v1_270m
      label: Dense
      source: dataset_candidate_subset
      top_k: 500
      ndcg_at_10: 0.2527864024
      hit_at_10: 0.35
      recall_at_100: 0.67
      candidate_count_min: 500
      candidate_count_max: 500
      candidate_count_mean: 500.0
      query_count: 200
      query_coverage: 1.0
      relevant_coverage_at_100: 0.67
    reranking_hybrid:
      config: reranking_hybrid
      label: Reranking hybrid
      source: dataset_candidate_subset
      top_k: 100
      ndcg_at_10: 0.1654971989
      hit_at_10: 0.275
      recall_at_100: 0.54
      candidate_count_min: 100
      candidate_count_max: 101
      candidate_count_mean: 100.46
      query_count: 200
      query_coverage: 1.0
      relevant_coverage_at_100: 0.54
      safeguard_positive_rows: 92
      rows_with_101_candidates: 92
```
