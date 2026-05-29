# NanoBRIGHT / NanoBrightPony

## Overview

`NanoBrightPony` is the Pony programming-language documentation retrieval slice
of BRIGHT. Queries are coding tasks to be solved in Pony, and relevant documents
are manual passages about the syntax or language feature needed to implement the
solution.

## Details

### What the Original Data Measures

[BRIGHT](https://arxiv.org/abs/2407.12883) describes Pony as a rare-language
coding retrieval task. The paper uses coding-problem instructions as queries,
annotated documentation about required syntax as positives, and the complete
Pony language manual as the retrieval pool. It is designed to be hard because a
problem statement may have little lexical overlap with the relevant syntax
documentation.

### Observed Data Profile

The split has 112 queries, 6,183 documents, and 2,219 positive qrels. Queries
average 388.97 characters and include a natural-language problem plus a Pony
function template. Documents average 306.50 characters and are short manual
passages about control structures, errors, operators, primitives, and library
features. Positives are highly multi-positive, averaging 19.81 per query.

### BM25 Difficulty

Using the dataset-provided BM25 candidate column, BM25 reaches nDCG@10 =
0.0362 and hit@10 = 0.2946. It ranks only 2 queries with a positive first, and
the median best positive rank is 21.5. This is one of the hardest observed
NanoBRIGHT splits for BM25 because matching a programming task to needed Pony
syntax requires reasoning about implementation steps.

### Training Data That May Help

Useful data includes non-overlapping Pony documentation retrieval pairs,
rare-language code tasks with documentation references, API-doc search data,
and program-synthesis examples labeled with required language constructs.

### Synthetic Data Guidance

Generate Pony coding tasks with templates and identify the exact syntax or
manual section needed to solve them. Positives should be documentation passages,
not solution code. Hard negatives should discuss nearby language constructs,
such as other loops or error-handling forms, that would not solve the task.

## Example Data

| Query | Positive document |
| --- | --- |
| I will use the programming language pony. Problem: You are given an array of integers stones where stones[i] is the weight of the ith stone. We are playing a game with the stones. On each turn, we choose the heaviest two ston ... [truncated 225 chars](730 chars) | So first we ask if there are any more names to get. If there are then we get a name and see if it's "Jack" or "Jill". If it is we're done and we break out of the loop, handing back the name we've found. If not we try again. T ... [truncated 225 chars](676 chars) |
| I will use the programming language pony. Problem: You are given an integer array nums. The unique elements of an array are the elements that appear exactly once in the array. Write a function that returns the sum of all the ... [truncated 225 chars](323 chars) | We can see that it makes more sense for the unary operator to be applied before either infix as it only acts on a single number in the expression so it is never ambiguous. Unary operators can also be applied to parentheses an ... [truncated 225 chars](380 chars) |
| I will use the programming language pony. Problem: Given an array of integers nums, write a function that returns the number of good pairs. A pair (i, j) is called good if nums[i] == nums[j] and i < j. Here is the code templa ... [truncated 225 chars](281 chars) | # Local variables Local variables in Pony work very much as they do in other languages, allowing you to store temporary values while you perform calculations. Local variables live within a chunk of code (they are _local_ to t ... [truncated 225 chars](1245 chars) |
| I will use the programming language pony. Problem: Given an integer number n, write a function that returns the difference between the product of its digits and the sum of its digits. For example, if n = 234, product of digit ... [truncated 225 chars](370 chars) | # Infix Operators Infix operators take two operands and are written between those operands. Arithmetic and comparison operators are the most common: ```pony 1 + 2 a < b ``` Pony has pretty much the same set of infix operators ... [truncated 225 chars](248 chars) |
| I will use the programming language pony. Problem: A string s is nice if, for every letter of the alphabet that s contains, it appears both in uppercase and lowercase. For example, "abABB" is nice because 'A' and 'a' appear, ... [truncated 225 chars](592 chars) | So first we ask if there are any more names to get. If there are then we get a name and see if it's "Jack" or "Jill". If it is we're done and we break out of the loop, handing back the name we've found. If not we try again. T ... [truncated 225 chars](676 chars) |

## Dataset Information

| Field | Value |
| --- | --- |
| Nano set | NanoBRIGHT |
| Backing dataset | NanoBRIGHT |
| Task / split | NanoBrightPony |
| Source task | Pony |
| Hugging Face dataset | [hakari-bench/NanoBRIGHT](https://huggingface.co/datasets/hakari-bench/NanoBRIGHT) |
| Source dataset | [xlangai/BRIGHT](https://huggingface.co/datasets/xlangai/BRIGHT) |
| Language | en |
| Category | natural_language |
| Queries | 112 |
| Documents | 6183 |
| Positive qrels | 2219 |
| Positives per query | avg 19.81, min 1, median 21, max 28 |
| Multi-positive queries | 111 (99.11%) |
| BM25 nDCG@10 | 0.0496 |
| BM25 hit@10 | 0.3304 |
| BM25 Recall@100 | 0.2438 |
| BM25 candidate subset | top-500 (`bm25`) |
| Dense nDCG@10 | 0.0219 |
| Dense hit@10 | 0.1429 |
| Dense Recall@100 | 0.0518 |
| Dense candidate subset | top-500 (`harrier_oss_v1_270m`) |
| Reranking hybrid nDCG@10 | 0.0780 |
| Reranking hybrid hit@10 | 0.4375 |
| Reranking hybrid Recall@100 | 0.1717 |
| Reranking hybrid candidate subset | top-100 plus optional rank-101 safeguard (`reranking_hybrid`) |
| Reranking hybrid candidates / query | 100-101 |
| Reranking hybrid safeguard rows | 8 |
| Query length avg chars | 388.97 |
| Document length avg chars | 306.50 |

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
  task_name: NanoBrightPony
  split_name: NanoBrightPony
  source_task: Pony
  source_dataset_id: xlangai/BRIGHT
  language: en
  category: natural_language
  document_path: docs/benchmark_tasks/NanoBRIGHT/NanoBrightPony.md
  source_research:
    primary_source_type: benchmark_paper
    paper_pdf_or_html_checked: true
    no_paper_note: null
  counts:
    queries: 112
    documents: 6183
    positive_qrels: 2219
  positives_per_query:
    average: 19.8125
    min: 1
    median: 21.0
    max: 28
    multi_positive_queries: 111
    multi_positive_query_percent: 99.10714285714286
  text_stats_chars:
    query_mean: 388.9732142857143
    document_mean: 306.50072780203783
  bm25:
    ndcg_at_10: 0.04963607682149031
    hit_at_10: 0.33035714285714285
    source: dataset_candidate_subset
  learning:
    original_train_split: unknown
    evaluation_split_origin: BRIGHT Pony evaluation split
    train_eval_overlap_audit: not_audited
    leakage_note: exclude NanoBRIGHT Pony task templates and annotated manual positives
    useful_training_data:
    - non-overlapping Pony documentation retrieval pairs
    - rare-language code tasks with documentation references
    - API documentation search and program-synthesis supervision
    synthetic_data:
      document_generation: Pony manual passages about syntax, control flow, errors,
        and libraries
      question_generation: Pony coding tasks with function templates
      answerability: positives should be documentation needed to implement the task
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
      ndcg_at_10: 0.0496360768
      hit_at_10: 0.3303571429
      recall_at_100: 0.2438035151
      candidate_count_min: 500
      candidate_count_max: 500
      candidate_count_mean: 500.0
      query_count: 112
      query_coverage: 1.0
      relevant_coverage_at_100: 0.2438035151
    dense:
      config: harrier_oss_v1_270m
      label: Dense
      source: dataset_candidate_subset
      top_k: 500
      ndcg_at_10: 0.0219208838
      hit_at_10: 0.1428571429
      recall_at_100: 0.0518251465
      candidate_count_min: 500
      candidate_count_max: 500
      candidate_count_mean: 500.0
      query_count: 112
      query_coverage: 1.0
      relevant_coverage_at_100: 0.0518251465
    reranking_hybrid:
      config: reranking_hybrid
      label: Reranking hybrid
      source: dataset_candidate_subset
      top_k: 100
      ndcg_at_10: 0.0779735468
      hit_at_10: 0.4375
      recall_at_100: 0.1716989635
      candidate_count_min: 100
      candidate_count_max: 101
      candidate_count_mean: 100.071429
      query_count: 112
      query_coverage: 1.0
      relevant_coverage_at_100: 0.1716989635
      safeguard_positive_rows: 8
      rows_with_101_candidates: 8
```
