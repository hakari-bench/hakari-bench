# NanoRTEB / NanoHumanEval

## Overview

`NanoRTEB / NanoHumanEval` retrieves Python implementations for HumanEval
programming task descriptions.

## Details

### What the Original Data Measures

[Evaluating Large Language Models Trained on Code](https://arxiv.org/abs/2107.03374)
introduces HumanEval as a hand-written set of Python programming problems used
to evaluate functional correctness from docstrings and tests. RTEB converts the
generation task into retrieval by treating the problem description as the query
and the implementation body as the positive document.

This task measures semantic code retrieval for compact Python functions. It is
closer to docstring-to-code search than to long competitive-programming
retrieval.

### Observed Data Profile

The split has 158 queries, 158 documents, and 158 positive qrel rows. Every
query has one positive. Queries average 291.16 characters and documents average
176.99 characters. Many examples are short algorithmic functions with direct
natural-language descriptions.

### BM25 Difficulty

Using the dataset-provided BM25 candidate column, BM25 reaches nDCG@10 =
0.3990 and hit@10 = 0.6266. It ranks 31 positives at rank 1 and 99 in the top
10.

BM25 works when descriptions mention variable names or operations visible in the
implementation. It struggles when the code is short and semantically obvious
but lexically sparse, such as returning a tuple of sum and product.

### Training Data That May Help

Useful data includes docstring-to-code retrieval, Python unit-test-linked
functions, HumanEval-style programming problems, and hard negatives from
functions with similar control flow but different semantics.

### Synthetic Data Guidance

Generate concise function specifications paired with executable Python
implementations and tests. Include negative functions that share keywords,
argument names, or loops but implement a different requirement. Preserve small
functions; overlong generated code would not match this benchmark well.

## Example Data

| Query | Positive document |
| --- | --- |
| Filter an input list of strings only for ones that start with a given prefix. (77 chars) | return [x for x in strings if x.startswith(prefix)] (51 chars) |
| Input to this function is a string represented multiple groups for nested parentheses separated by spaces. For each of the group, output the deepest level of nesting of parentheses. E.g. (()()) has maximum two levels of nesti ... [truncated 225 chars](251 chars) | def parse_paren_group(s): depth = 0 max_depth = 0 for c in s: if c == '(': depth += 1 max_depth = max(depth, max_depth) else: depth -= 1 return max_depth return [parse_paren_group(x) for x in paren_string.split(' ') if x] (331 chars) |
| Write a function that returns true if the given number is the multiplication of 3 prime numbers and false otherwise. Knowing that (a) is less then 100. Example: is_multiply_prime(30) == True (191 chars) | def is_prime(n): for j in range(2,n): if n%j == 0: return False return True for i in range(2,101): if not is_prime(i): continue for j in range(2,101): if not is_prime(j): continue for k in range(2,101): if not is_prime(k): co ... [truncated 225 chars](396 chars) |
| In this task, you will be given a string that represents a number of apples and oranges that are distributed in a basket of fruit this basket contains apples, oranges, and mango fruits. Given the string that represents the to ... [truncated 225 chars](606 chars) | lis = list() for i in s.split(' '): if i.isdigit(): lis.append(int(i)) return n - sum(lis) (118 chars) |
| brackets is a string of "(" and ")". return True if every opening bracket has a corresponding closing bracket. (110 chars) | depth = 0 for b in brackets: if b == "(": depth += 1 else: depth -= 1 if depth < 0: return False return depth == 0 (182 chars) |

## Dataset Information

| Field | Value |
| --- | --- |
| Nano set | NanoRTEB |
| Backing dataset | NanoRTEB |
| Task / split | NanoHumanEval |
| Hugging Face dataset | [hakari-bench/NanoRTEB](https://huggingface.co/datasets/hakari-bench/NanoRTEB) |
| Source dataset | [openai/openai_humaneval](https://huggingface.co/datasets/openai/openai_humaneval) |
| Language | en |
| Category | code |
| Queries | 158 |
| Documents | 158 |
| Positive qrels | 158 |
| BM25 nDCG@10 | 0.3405 |
| BM25 hit@10 | 0.5443 |
| BM25 Recall@100 | 0.9051 |
| BM25 candidate subset | top-500 (`bm25`) |
| Dense nDCG@10 | 0.5666 |
| Dense hit@10 | 0.7975 |
| Dense Recall@100 | 0.9937 |
| Dense candidate subset | top-500 (`harrier_oss_v1_270m`) |
| Reranking hybrid nDCG@10 | 0.5770 |
| Reranking hybrid hit@10 | 0.7405 |
| Reranking hybrid Recall@100 | 0.9937 |
| Reranking hybrid candidate subset | top-100 plus optional rank-101 safeguard (`reranking_hybrid`) |
| Reranking hybrid candidates / query | 100-101 |
| Reranking hybrid safeguard rows | 1 |
| Query length avg chars | 291.16 |
| Document length avg chars | 176.99 |

### Public Sources

- [Evaluating Large Language Models Trained on Code](https://arxiv.org/abs/2107.03374), task paper.
- [openai/openai_humaneval](https://huggingface.co/datasets/openai/openai_humaneval), source dataset card.
- [Introducing RTEB: A New Standard for Retrieval Evaluation](https://huggingface.co/blog/rteb), RTEB benchmark announcement.

### Hugging Face Links

- Nano dataset: [hakari-bench/NanoRTEB](https://huggingface.co/datasets/hakari-bench/NanoRTEB)
- Source task dataset: [openai/openai_humaneval](https://huggingface.co/datasets/openai/openai_humaneval)

### Source Reference Table

| Title | Year | Type | URL |
| --- | ---: | --- | --- |
| Evaluating Large Language Models Trained on Code | 2021 | task paper | https://arxiv.org/abs/2107.03374 |
| openai/openai_humaneval |  | dataset card | https://huggingface.co/datasets/openai/openai_humaneval |
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
  task_name: NanoHumanEval
  split_name: NanoHumanEval
  language: en
  category: code
  document_path: docs/benchmark_tasks/NanoRTEB/NanoHumanEval.md
  source_research:
    primary_source_type: task_paper
    paper_pdf_or_html_checked: true
    no_paper_note: null
  counts:
    queries: 158
    documents: 158
    positive_qrels: 158
  positives_per_query:
    average: 1.0
    min: 1
    median: 1.0
    max: 1
    multi_positive_queries: 0
    multi_positive_query_percent: 0.0
  text_stats_chars:
    query_mean: 291.16
    document_mean: 176.99
  bm25:
    ndcg_at_10: 0.340549984590461
    hit_at_10: 0.5443037974683544
    source: dataset_candidate_subset
  example_count: 5
  candidate_subsets:
    bm25:
      config: bm25
      label: BM25
      source: dataset_candidate_subset
      top_k: 500
      ndcg_at_10: 0.3405499846
      hit_at_10: 0.5443037975
      recall_at_100: 0.9050632911
      candidate_count_min: 158
      candidate_count_max: 158
      candidate_count_mean: 158.0
      query_count: 158
      query_coverage: 1.0
      relevant_coverage_at_100: 0.9050632911
    dense:
      config: harrier_oss_v1_270m
      label: Dense
      source: dataset_candidate_subset
      top_k: 500
      ndcg_at_10: 0.5666155469
      hit_at_10: 0.7974683544
      recall_at_100: 0.9936708861
      candidate_count_min: 158
      candidate_count_max: 158
      candidate_count_mean: 158.0
      query_count: 158
      query_coverage: 1.0
      relevant_coverage_at_100: 0.9936708861
    reranking_hybrid:
      config: reranking_hybrid
      label: Reranking hybrid
      source: dataset_candidate_subset
      top_k: 100
      ndcg_at_10: 0.57703577
      hit_at_10: 0.7405063291
      recall_at_100: 0.9936708861
      candidate_count_min: 100
      candidate_count_max: 101
      candidate_count_mean: 100.006329
      query_count: 158
      query_coverage: 1.0
      relevant_coverage_at_100: 0.9936708861
      safeguard_positive_rows: 1
      rows_with_101_candidates: 1
```
