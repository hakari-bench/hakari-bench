# NanoRARb / NanoSIQA

## Overview

`NanoSIQA` is a social commonsense retrieval task. The query gives a social
situation and asks about a likely intention, motivation, or next event; the
positive document is the correct short answer.

## Details

### What the Original Data Measures

[RAR-b: Reasoning as Retrieval Benchmark](https://arxiv.org/abs/2404.06347)
includes SocialIQA as a commonsense reasoning task converted to full-dataset
retrieval. [SocialIQA: Commonsense Reasoning about Social Interactions](https://arxiv.org/abs/1904.09728)
defines questions about people's intents, reactions, and social consequences.

This retrieval split tests whether short answer embeddings capture social
plausibility, not just entity or word overlap with the situation.

### Observed Data Profile

The Nano split has 200 queries, 10,000 candidate documents, and 200 positive
qrels. Every query has one positive. Queries average 126.94 characters, and
answer documents average 21.51 characters.

Observed answers are very short phrases such as "make an educated choice" or
"watch television", which makes exact lexical retrieval brittle.

### BM25 Difficulty

Using the dataset-provided BM25 candidate column, BM25 reaches nDCG@10 = 0.0278
and hit@10 = 0.0450. It ranks 3 positives first.

The low BM25 score reflects the gap between a social situation and the implied
answer phrase.

### Training Data That May Help

Helpful data includes social commonsense QA, intent/effect prediction, dialogue
commonsense, and retrieval-formatted answer selection. Exclude NanoRARb
evaluation examples and answer documents.

### Synthetic Data Guidance

Generate short social contexts and questions about intent, reaction, or likely
next action. Hard negatives should mention the same people or setting but imply
the wrong social relation.

## Example Data

| Query | Positive document |
| --- | --- |
| Context: Cameron's parents told them to do well at school or they would be grounded. Cameron took their words seriously. Question: What will happen to Cameron? (160 chars) | study very hard (15 chars) |
| Context: Riley had a lot of friends. Question: What will happen to Riley? (73 chars) | they will play with Riley (25 chars) |
| Context: Sydney is a fan of Hillary Clinton. One day she found a biography of Hillary Clinton. Sydney wanted to read it. Question: Why did Sydney do this? (154 chars) | know more about Hillary Clinton (31 chars) |
| Context: Austin knew Quinn intimately and they slept together many times. Question: Why did Austin do this? (107 chars) | found QUinn attractive (22 chars) |
| Context: Quinn knew Ash well enough that they broken into and stole a jacket from Ash's locker. Question: How would Quinn feel afterwards? (138 chars) | ashamed (7 chars) |

## Dataset Information

| Field | Value |
| --- | --- |
| Nano set | NanoRARb |
| Backing dataset | NanoRARb |
| Task / split | NanoSIQA |
| Hugging Face dataset | [hakari-bench/NanoRARb](https://huggingface.co/datasets/hakari-bench/NanoRARb) |
| Language | en |
| Category | natural_language |
| Queries | 200 |
| Documents | 10000 |
| Positive qrels | 200 |
| BM25 nDCG@10 | 0.0239 |
| BM25 hit@10 | 0.0400 |
| BM25 Recall@100 | 0.1850 |
| BM25 candidate subset | top-500 (`bm25`) |
| Dense nDCG@10 | 0.0618 |
| Dense hit@10 | 0.1250 |
| Dense Recall@100 | 0.3850 |
| Dense candidate subset | top-500 (`harrier_oss_v1_270m`) |
| Reranking hybrid nDCG@10 | 0.0405 |
| Reranking hybrid hit@10 | 0.0700 |
| Reranking hybrid Recall@100 | 0.3350 |
| Reranking hybrid candidate subset | top-100 plus optional rank-101 safeguard (`reranking_hybrid`) |
| Reranking hybrid candidates / query | 100-101 |
| Reranking hybrid safeguard rows | 133 |
| Query length avg chars | 126.94 |
| Document length avg chars | 21.51 |

### Public Sources

- [RAR-b: Reasoning as Retrieval Benchmark](https://arxiv.org/abs/2404.06347).
- [SocialIQA: Commonsense Reasoning about Social Interactions](https://arxiv.org/abs/1904.09728).

### Hugging Face Links

- Nano dataset: [hakari-bench/NanoRARb](https://huggingface.co/datasets/hakari-bench/NanoRARb)

### Source Reference Table

| Title | Year | Type | URL |
| --- | ---: | --- | --- |
| RAR-b: Reasoning as Retrieval Benchmark | 2024 | arXiv paper | https://arxiv.org/abs/2404.06347 |
| SocialIQA: Commonsense Reasoning about Social Interactions | 2019 | arXiv paper | https://arxiv.org/abs/1904.09728 |

## Machine-Readable Metadata

<!-- benchmark-task-metadata:v1 -->

```yaml
benchmark_task_metadata:
  schema_version: 1
  document_status: first_pass
  nano_set: NanoRARb
  backing_dataset: NanoRARb
  dataset_id: hakari-bench/NanoRARb
  task_name: NanoSIQA
  split_name: NanoSIQA
  language: en
  category: natural_language
  document_path: docs/benchmark_tasks/NanoRARb/NanoSIQA.md
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
    query_mean: 126.94
    document_mean: 21.509
  bm25:
    ndcg_at_10: 0.023938644528462786
    hit_at_10: 0.04
    source: dataset_candidate_subset
  links:
    nano_dataset: https://huggingface.co/datasets/hakari-bench/NanoRARb
    source_urls:
    - label: RAR-b arXiv
      url: https://arxiv.org/abs/2404.06347
    - label: SocialIQA arXiv
      url: https://arxiv.org/abs/1904.09728
  references:
  - title: 'RAR-b: Reasoning as Retrieval Benchmark'
    url: https://arxiv.org/abs/2404.06347
    year: 2024
    is_paper: true
  - title: 'SocialIQA: Commonsense Reasoning about Social Interactions'
    url: https://arxiv.org/abs/1904.09728
    year: 2019
    is_paper: true
  candidate_subsets:
    bm25:
      config: bm25
      label: BM25
      source: dataset_candidate_subset
      top_k: 500
      ndcg_at_10: 0.0239386445
      hit_at_10: 0.04
      recall_at_100: 0.185
      candidate_count_min: 500
      candidate_count_max: 500
      candidate_count_mean: 500.0
      query_count: 200
      query_coverage: 1.0
      relevant_coverage_at_100: 0.185
    dense:
      config: harrier_oss_v1_270m
      label: Dense
      source: dataset_candidate_subset
      top_k: 500
      ndcg_at_10: 0.0617802067
      hit_at_10: 0.125
      recall_at_100: 0.385
      candidate_count_min: 500
      candidate_count_max: 500
      candidate_count_mean: 500.0
      query_count: 200
      query_coverage: 1.0
      relevant_coverage_at_100: 0.385
    reranking_hybrid:
      config: reranking_hybrid
      label: Reranking hybrid
      source: dataset_candidate_subset
      top_k: 100
      ndcg_at_10: 0.0405086604
      hit_at_10: 0.07
      recall_at_100: 0.335
      candidate_count_min: 100
      candidate_count_max: 101
      candidate_count_mean: 100.665
      query_count: 200
      query_coverage: 1.0
      relevant_coverage_at_100: 0.335
      safeguard_positive_rows: 133
      rows_with_101_candidates: 133
```
