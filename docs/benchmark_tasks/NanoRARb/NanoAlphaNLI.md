# NanoRARb / NanoAlphaNLI

## Overview

`NanoAlphaNLI` turns abductive commonsense reasoning into retrieval. The query
contains the start and end of a short story, and the retriever must find the
most plausible missing explanatory event.

## Details

### What the Original Data Measures

[RAR-b: Reasoning as Retrieval Benchmark](https://arxiv.org/abs/2404.06347)
places AlphaNLI among commonsense reasoning tasks and evaluates whether
retrievers can retrieve ground-truth answers from a full answer corpus. [Abductive
Commonsense Reasoning](https://arxiv.org/abs/1908.05739) introduces the original
task as selecting the most plausible hypothesis connecting two observations.

This split measures narrative plausibility and causal bridging rather than
topical document retrieval.

### Observed Data Profile

The Nano split has 200 queries, 10,000 candidate documents, and 200 positive
qrels. Every query has one positive. Queries average 103.79 characters, and
candidate explanations average 43.84 characters.

Observed queries use `Start:` and `End:` fields. Positives are short story
middle events such as booking a trip, practicing a skill, or testing samples.

### BM25 Difficulty

Using the dataset-provided BM25 candidate column, BM25 reaches nDCG@10 = 0.2936
and hit@10 = 0.4450. It ranks 33 positives first.

Lexical overlap helps when the hypothesis repeats story entities, but many
queries require causal plausibility rather than shared terms.

### Training Data That May Help

Helpful data includes abductive commonsense QA, story cloze, narrative
continuation, and retrieval-formatted hypothesis selection. Exclude NanoRARb
evaluation questions and candidate answers.

### Synthetic Data Guidance

Generate two observations and several plausible or implausible bridging events.
Hard negatives should mention the same characters or objects but fail to explain
the ending.

## Example Data

| Query | Positive document |
| --- | --- |
| Start: Scott has felt increasingly unhappy in his last few Year's in New York. End: Driving out of New York, Scott feels both relieved and nostalgic. (149 chars) | The daily grind, extreme traffic and rude city dwellers left Scott longing for small town living. (97 chars) |
| Start: Joe's mother bugged him constantly to tie his shoelaces. End: As he lay at the bottom of the stairs he wished he'd listened. (131 chars) | Joe tripped down the stairs with his shoes untied. (50 chars) |
| Start: Alex was at target with his mom. End: He begged his mother to buy it until she gave in. (94 chars) | Alex saw a game he really wanted. (33 chars) |
| Start: Ali's mom enrolled her in a karate class. End: Ali was so embarrassed she didn't tell any of her friends. (112 chars) | Ali did not want to take karate. (32 chars) |
| Start: Once there was a girl named Mia who could spell well. End: Mia won the spelling bee and felt more sure of herself afterwards. (132 chars) | She studied hard because she wanted to spell. (45 chars) |

## Dataset Information

| Field | Value |
| --- | --- |
| Nano set | NanoRARb |
| Backing dataset | NanoRARb |
| Task / split | NanoAlphaNLI |
| Hugging Face dataset | [hakari-bench/NanoRARb](https://huggingface.co/datasets/hakari-bench/NanoRARb) |
| Language | en |
| Category | natural_language |
| Queries | 200 |
| Documents | 10000 |
| Positive qrels | 200 |
| BM25 nDCG@10 | 0.3288 |
| BM25 hit@10 | 0.4650 |
| BM25 Recall@100 | 0.6750 |
| BM25 candidate subset | top-500 (`bm25`) |
| Dense nDCG@10 | 0.5898 |
| Dense hit@10 | 0.7900 |
| Dense Recall@100 | 0.9150 |
| Dense candidate subset | top-500 (`harrier_oss_v1_270m`) |
| Reranking hybrid nDCG@10 | 0.4777 |
| Reranking hybrid hit@10 | 0.6500 |
| Reranking hybrid Recall@100 | 0.8950 |
| Reranking hybrid candidate subset | top-100 plus optional rank-101 safeguard (`reranking_hybrid`) |
| Reranking hybrid candidates / query | 100-101 |
| Reranking hybrid safeguard rows | 21 |
| Query length avg chars | 103.79 |
| Document length avg chars | 43.84 |

### Public Sources

- [RAR-b: Reasoning as Retrieval Benchmark](https://arxiv.org/abs/2404.06347).
- [Abductive Commonsense Reasoning](https://arxiv.org/abs/1908.05739).

### Hugging Face Links

- Nano dataset: [hakari-bench/NanoRARb](https://huggingface.co/datasets/hakari-bench/NanoRARb)

### Source Reference Table

| Title | Year | Type | URL |
| --- | ---: | --- | --- |
| RAR-b: Reasoning as Retrieval Benchmark | 2024 | arXiv paper | https://arxiv.org/abs/2404.06347 |
| Abductive Commonsense Reasoning | 2019 | arXiv paper | https://arxiv.org/abs/1908.05739 |

## Machine-Readable Metadata

<!-- benchmark-task-metadata:v1 -->

```yaml
benchmark_task_metadata:
  schema_version: 1
  document_status: first_pass
  nano_set: NanoRARb
  backing_dataset: NanoRARb
  dataset_id: hakari-bench/NanoRARb
  task_name: NanoAlphaNLI
  split_name: NanoAlphaNLI
  language: en
  category: natural_language
  document_path: docs/benchmark_tasks/NanoRARb/NanoAlphaNLI.md
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
    query_mean: 103.79
    document_mean: 43.8436
  bm25:
    ndcg_at_10: 0.32882198321454403
    hit_at_10: 0.465
    source: dataset_candidate_subset
  links:
    nano_dataset: https://huggingface.co/datasets/hakari-bench/NanoRARb
    source_urls:
    - label: RAR-b arXiv
      url: https://arxiv.org/abs/2404.06347
    - label: AlphaNLI arXiv
      url: https://arxiv.org/abs/1908.05739
  references:
  - title: 'RAR-b: Reasoning as Retrieval Benchmark'
    url: https://arxiv.org/abs/2404.06347
    year: 2024
    is_paper: true
  - title: Abductive Commonsense Reasoning
    url: https://arxiv.org/abs/1908.05739
    year: 2019
    is_paper: true
  candidate_subsets:
    bm25:
      config: bm25
      label: BM25
      source: dataset_candidate_subset
      top_k: 500
      ndcg_at_10: 0.3288219832
      hit_at_10: 0.465
      recall_at_100: 0.675
      candidate_count_min: 500
      candidate_count_max: 500
      candidate_count_mean: 500.0
      query_count: 200
      query_coverage: 1.0
      relevant_coverage_at_100: 0.675
    dense:
      config: harrier_oss_v1_270m
      label: Dense
      source: dataset_candidate_subset
      top_k: 500
      ndcg_at_10: 0.5898374791
      hit_at_10: 0.79
      recall_at_100: 0.915
      candidate_count_min: 500
      candidate_count_max: 500
      candidate_count_mean: 500.0
      query_count: 200
      query_coverage: 1.0
      relevant_coverage_at_100: 0.915
    reranking_hybrid:
      config: reranking_hybrid
      label: Reranking hybrid
      source: dataset_candidate_subset
      top_k: 100
      ndcg_at_10: 0.4776837661
      hit_at_10: 0.65
      recall_at_100: 0.895
      candidate_count_min: 100
      candidate_count_max: 101
      candidate_count_mean: 100.105
      query_count: 200
      query_coverage: 1.0
      relevant_coverage_at_100: 0.895
      safeguard_positive_rows: 21
      rows_with_101_candidates: 21
```
