# NanoRTEB / NanoDS1000

## Overview

`NanoRTEB / NanoDS1000` retrieves Python data-science code snippets for
natural-language programming tasks involving libraries such as NumPy, SciPy,
pandas, and matplotlib.

## Details

### What the Original Data Measures

[DS-1000: A Natural and Reliable Benchmark for Data Science Code
Generation](https://arxiv.org/abs/2211.11501) introduces DS-1000 as a
data-science code generation benchmark built from natural user questions and
library-specific tasks. It emphasizes execution-based correctness and common
Python data-science libraries.

RTEB turns this into retrieval: the query is the natural-language problem and
the positive document is a code snippet that solves it. This measures whether a
retriever can connect API intent to executable code.

### Observed Data Profile

The split has 200 queries, 997 documents, and 200 positive qrel rows. Each query
has one positive. Queries average 1,154.15 characters and include code fragments
or StackOverflow-style context. Documents average 687.85 characters and often
load test inputs before applying a concise library operation.

### BM25 Difficulty

Using the dataset-provided BM25 candidate column, BM25 reaches nDCG@10 =
0.4515 and hit@10 = 0.6050. It ranks 59 positives at rank 1 and 121 in the top
10.

BM25 does better than on APPS because user questions often name exact APIs such
as SciPy sparse matrices or lognormal distributions. It still misses cases where
the correct solution depends on semantic API behavior rather than shared tokens.

### Training Data That May Help

Useful data includes data-science StackOverflow question-code pairs, API
documentation retrieval, notebook-to-code retrieval, and hard negatives from
similar APIs in the same library.

### Synthetic Data Guidance

Generate realistic data-science questions from non-evaluation library examples
and pair them with minimal working code. Include hard negatives using nearby
functions, similar array shapes, or the same library but a different operation.

## Example Data

| Query | Positive document |
| --- | --- |
| Problem: I have a list of numpy vectors of the format: [array([[-0.36314615, 0.80562619, -0.82777381, ..., 2.00876354,2.08571887, -1.24526026]]), array([[ 0.9766923 , -0.05725135, -0.38505339, ..., 0.12187988,-0.83129255, 0.3 ... [truncated 225 chars](1055 chars) | import pickle import argparse parser = argparse.ArgumentParser() parser.add_argument("--test_case", type=int, default=1) args = parser.parse_args() import numpy as np import scipy.sparse as sparse vectors, max_vector_size = p ... [truncated 225 chars](520 chars) |
| Problem: I'm trying to reduce noise in a binary python array by removing all completely isolated single cells, i.e. setting "1" value cells to 0 if they are completely surrounded by other "0"s like this: 0 0 0 0 1 0 0 0 0 I h ... [truncated 225 chars](925 chars) | import pickle import argparse parser = argparse.ArgumentParser() parser.add_argument("--test_case", type=int, default=1) args = parser.parse_args() import numpy as np import scipy.ndimage square = pickle.load(open(f"input/inp ... [truncated 225 chars](777 chars) |
| Problem: I am having a problem with minimization procedure. Actually, I could not create a correct objective function for my problem. Problem definition • My function: yn = a_11*x1**2 + a_12*x2**2 + ... + a_m*xn**2,where xn- ... [truncated 225 chars](1716 chars) | import pickle import argparse parser = argparse.ArgumentParser() parser.add_argument("--test_case", type=int, default=1) args = parser.parse_args() import scipy.optimize import numpy as np a, x_true, y, x0, x_lower_bounds = p ... [truncated 225 chars](614 chars) |
| Problem: I am working with a 2D numpy array made of 512x512=262144 values. Such values are of float type and range from 0.0 to 1.0. The array has an X,Y coordinate system which originates in the top left corner: thus, positio ... [truncated 225 chars](1020 chars) | import pickle import argparse parser = argparse.ArgumentParser() parser.add_argument("--test_case", type=int, default=1) args = parser.parse_args() import numpy as np from scipy import ndimage img = pickle.load(open(f"input/i ... [truncated 225 chars](455 chars) |
| Problem: I'm trying to integrate X (X ~ N(u, o2)) to calculate the probability up to position `x`. However I'm running into an error of: Traceback (most recent call last): File "<ipython console>", line 1, in <module> File "s ... [truncated 225 chars](1047 chars) | import pickle import argparse parser = argparse.ArgumentParser() parser.add_argument("--test_case", type=int, default=1) args = parser.parse_args() import scipy.integrate import math import numpy as np x, u, o2 = pickle.load( ... [truncated 225 chars](527 chars) |

## Dataset Information

| Field | Value |
| --- | --- |
| Nano set | NanoRTEB |
| Backing dataset | NanoRTEB |
| Task / split | NanoDS1000 |
| Hugging Face dataset | [hakari-bench/NanoRTEB](https://huggingface.co/datasets/hakari-bench/NanoRTEB) |
| Source dataset | [xlangai/DS-1000](https://huggingface.co/datasets/xlangai/DS-1000) |
| Language | en |
| Category | code |
| Queries | 200 |
| Documents | 997 |
| Positive qrels | 200 |
| BM25 nDCG@10 | 0.4424 |
| BM25 hit@10 | 0.6200 |
| BM25 Recall@100 | 0.8750 |
| BM25 candidate subset | top-500 (`bm25`) |
| Dense nDCG@10 | 0.6835 |
| Dense hit@10 | 0.8700 |
| Dense Recall@100 | 0.9550 |
| Dense candidate subset | top-500 (`harrier_oss_v1_270m`) |
| Reranking hybrid nDCG@10 | 0.6053 |
| Reranking hybrid hit@10 | 0.8450 |
| Reranking hybrid Recall@100 | 0.9700 |
| Reranking hybrid candidate subset | top-100 plus optional rank-101 safeguard (`reranking_hybrid`) |
| Reranking hybrid candidates / query | 100-101 |
| Reranking hybrid safeguard rows | 6 |
| Query length avg chars | 1,154.15 |
| Document length avg chars | 687.85 |

### Public Sources

- [DS-1000: A Natural and Reliable Benchmark for Data Science Code Generation](https://arxiv.org/abs/2211.11501), task paper.
- [xlangai/DS-1000](https://huggingface.co/datasets/xlangai/DS-1000), source dataset card.
- [Introducing RTEB: A New Standard for Retrieval Evaluation](https://huggingface.co/blog/rteb), RTEB benchmark announcement.

### Hugging Face Links

- Nano dataset: [hakari-bench/NanoRTEB](https://huggingface.co/datasets/hakari-bench/NanoRTEB)
- Source task dataset: [xlangai/DS-1000](https://huggingface.co/datasets/xlangai/DS-1000)

### Source Reference Table

| Title | Year | Type | URL |
| --- | ---: | --- | --- |
| DS-1000: A Natural and Reliable Benchmark for Data Science Code Generation | 2022 | task paper | https://arxiv.org/abs/2211.11501 |
| xlangai/DS-1000 |  | dataset card | https://huggingface.co/datasets/xlangai/DS-1000 |
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
  task_name: NanoDS1000
  split_name: NanoDS1000
  language: en
  category: code
  document_path: docs/benchmark_tasks/NanoRTEB/NanoDS1000.md
  source_research:
    primary_source_type: task_paper
    paper_pdf_or_html_checked: true
    no_paper_note: null
  counts:
    queries: 200
    documents: 997
    positive_qrels: 200
  positives_per_query:
    average: 1.0
    min: 1
    median: 1.0
    max: 1
    multi_positive_queries: 0
    multi_positive_query_percent: 0.0
  text_stats_chars:
    query_mean: 1154.15
    document_mean: 687.85
  bm25:
    ndcg_at_10: 0.442387453763988
    hit_at_10: 0.62
    source: dataset_candidate_subset
  example_count: 5
  candidate_subsets:
    bm25:
      config: bm25
      label: BM25
      source: dataset_candidate_subset
      top_k: 500
      ndcg_at_10: 0.4423874538
      hit_at_10: 0.62
      recall_at_100: 0.875
      candidate_count_min: 500
      candidate_count_max: 500
      candidate_count_mean: 500.0
      query_count: 200
      query_coverage: 1.0
      relevant_coverage_at_100: 0.875
    dense:
      config: harrier_oss_v1_270m
      label: Dense
      source: dataset_candidate_subset
      top_k: 500
      ndcg_at_10: 0.6834992845
      hit_at_10: 0.87
      recall_at_100: 0.955
      candidate_count_min: 500
      candidate_count_max: 500
      candidate_count_mean: 500.0
      query_count: 200
      query_coverage: 1.0
      relevant_coverage_at_100: 0.955
    reranking_hybrid:
      config: reranking_hybrid
      label: Reranking hybrid
      source: dataset_candidate_subset
      top_k: 100
      ndcg_at_10: 0.6052723879
      hit_at_10: 0.845
      recall_at_100: 0.97
      candidate_count_min: 100
      candidate_count_max: 101
      candidate_count_mean: 100.03
      query_count: 200
      query_coverage: 1.0
      relevant_coverage_at_100: 0.97
      safeguard_positive_rows: 6
      rows_with_101_candidates: 6
```
