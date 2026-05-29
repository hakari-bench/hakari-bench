# NanoRARb / NanoHellaSwag

## Overview

`NanoHellaSwag` is a commonsense continuation retrieval task. The query is an
unfinished activity or video-caption context, and the relevant document is the
plausible continuation.

## Details

### What the Original Data Measures

[RAR-b: Reasoning as Retrieval Benchmark](https://arxiv.org/abs/2404.06347)
includes HellaSwag as a level-1 commonsense task because the query and answer
often resemble span-continuation pairs seen in representation learning. [HellaSwag:
Can a Machine Really Finish Your Sentence?](https://arxiv.org/abs/1905.07830)
introduces adversarially filtered commonsense endings for grounded situations.

This split tests whether a retriever can rank the coherent ending above many
pooled endings.

### Observed Data Profile

The Nano split has 200 queries, 10,000 candidate documents, and 200 positive
qrels. Queries average 114.68 characters, and candidate endings average 62.15
characters.

Observed examples are short activity descriptions about car washing, brushing
teeth, and playing harmonica. Positives are brief continuations.

### BM25 Difficulty

Using the dataset-provided BM25 candidate column, BM25 reaches nDCG@10 = 0.1166
and hit@10 = 0.2000. It ranks 9 positives first.

Lexical matching is limited because many endings are generic and plausibility
depends on event coherence rather than repeated terms.

### Training Data That May Help

Helpful training data includes story and activity continuation, grounded
commonsense QA, and HellaSwag-style adversarial endings. Avoid NanoRARb
evaluation examples and answer pool entries.

### Synthetic Data Guidance

Generate short contexts and plausible endings with adversarial distractors that
share objects or actions but violate temporal or physical plausibility.

## Example Data

| Query | Positive document |
| --- | --- |
| A man dressed in yellow and black winter clothes ice fishes on a a frozen lake. The man (87 chars) | is reeling in a fish for a long time. (37 chars) |
| A group of people are in a house. A man is mopping the floor with a mop. Another boy (84 chars) | attempts to walk through where he is mopping. (45 chars) |
| A man is in the gym in tight he bends over picks up a weight over his head and drops it back down. He walks back and loosens up before walking back up and doing it again adding more weight. He (192 chars) | does this multiple times adding more and more weight to the rack. (65 chars) |
| Then he takes a small stone from the flowing river and smashes it on another stone. He starts to crush the small stone to smaller pieces. He (140 chars) | grind it hard to make the pieces smaller. (41 chars) |
| A person hangs onto the handles of a kite flying overhead. The kite (67 chars) | falls as the wind lessens. (26 chars) |

## Dataset Information

| Field | Value |
| --- | --- |
| Nano set | NanoRARb |
| Backing dataset | NanoRARb |
| Task / split | NanoHellaSwag |
| Hugging Face dataset | [hakari-bench/NanoRARb](https://huggingface.co/datasets/hakari-bench/NanoRARb) |
| Language | en |
| Category | natural_language |
| Queries | 200 |
| Documents | 10000 |
| Positive qrels | 200 |
| BM25 nDCG@10 | 0.1393 |
| BM25 hit@10 | 0.2300 |
| BM25 Recall@100 | 0.5250 |
| BM25 candidate subset | top-500 (`bm25`) |
| Dense nDCG@10 | 0.1253 |
| Dense hit@10 | 0.2500 |
| Dense Recall@100 | 0.5250 |
| Dense candidate subset | top-500 (`harrier_oss_v1_270m`) |
| Reranking hybrid nDCG@10 | 0.1551 |
| Reranking hybrid hit@10 | 0.2900 |
| Reranking hybrid Recall@100 | 0.5950 |
| Reranking hybrid candidate subset | top-100 plus optional rank-101 safeguard (`reranking_hybrid`) |
| Reranking hybrid candidates / query | 100-101 |
| Reranking hybrid safeguard rows | 81 |
| Query length avg chars | 114.68 |
| Document length avg chars | 62.15 |

### Public Sources

- [RAR-b: Reasoning as Retrieval Benchmark](https://arxiv.org/abs/2404.06347).
- [HellaSwag: Can a Machine Really Finish Your Sentence?](https://arxiv.org/abs/1905.07830).

### Hugging Face Links

- Nano dataset: [hakari-bench/NanoRARb](https://huggingface.co/datasets/hakari-bench/NanoRARb)

### Source Reference Table

| Title | Year | Type | URL |
| --- | ---: | --- | --- |
| RAR-b: Reasoning as Retrieval Benchmark | 2024 | arXiv paper | https://arxiv.org/abs/2404.06347 |
| HellaSwag: Can a Machine Really Finish Your Sentence? | 2019 | arXiv paper | https://arxiv.org/abs/1905.07830 |

## Machine-Readable Metadata

<!-- benchmark-task-metadata:v1 -->

```yaml
benchmark_task_metadata:
  schema_version: 1
  document_status: first_pass
  nano_set: NanoRARb
  backing_dataset: NanoRARb
  dataset_id: hakari-bench/NanoRARb
  task_name: NanoHellaSwag
  split_name: NanoHellaSwag
  language: en
  category: natural_language
  document_path: docs/benchmark_tasks/NanoRARb/NanoHellaSwag.md
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
    query_mean: 114.68
    document_mean: 62.1517
  bm25:
    ndcg_at_10: 0.13925998972991618
    hit_at_10: 0.23
    source: dataset_candidate_subset
  links:
    nano_dataset: https://huggingface.co/datasets/hakari-bench/NanoRARb
    source_urls:
    - label: RAR-b arXiv
      url: https://arxiv.org/abs/2404.06347
    - label: HellaSwag arXiv
      url: https://arxiv.org/abs/1905.07830
  references:
  - title: 'RAR-b: Reasoning as Retrieval Benchmark'
    url: https://arxiv.org/abs/2404.06347
    year: 2024
    is_paper: true
  - title: 'HellaSwag: Can a Machine Really Finish Your Sentence?'
    url: https://arxiv.org/abs/1905.07830
    year: 2019
    is_paper: true
  candidate_subsets:
    bm25:
      config: bm25
      label: BM25
      source: dataset_candidate_subset
      top_k: 500
      ndcg_at_10: 0.1392599897
      hit_at_10: 0.23
      recall_at_100: 0.525
      candidate_count_min: 500
      candidate_count_max: 500
      candidate_count_mean: 500.0
      query_count: 200
      query_coverage: 1.0
      relevant_coverage_at_100: 0.525
    dense:
      config: harrier_oss_v1_270m
      label: Dense
      source: dataset_candidate_subset
      top_k: 500
      ndcg_at_10: 0.1253130035
      hit_at_10: 0.25
      recall_at_100: 0.525
      candidate_count_min: 500
      candidate_count_max: 500
      candidate_count_mean: 500.0
      query_count: 200
      query_coverage: 1.0
      relevant_coverage_at_100: 0.525
    reranking_hybrid:
      config: reranking_hybrid
      label: Reranking hybrid
      source: dataset_candidate_subset
      top_k: 100
      ndcg_at_10: 0.1550535462
      hit_at_10: 0.29
      recall_at_100: 0.595
      candidate_count_min: 100
      candidate_count_max: 101
      candidate_count_mean: 100.405
      query_count: 200
      query_coverage: 1.0
      relevant_coverage_at_100: 0.595
      safeguard_positive_rows: 81
      rows_with_101_candidates: 81
```
