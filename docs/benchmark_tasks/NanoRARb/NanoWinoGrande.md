# NanoRARb / NanoWinoGrande

## Overview

`NanoWinoGrande` is a pronoun and masked-referent reasoning retrieval task. The
query is a Winograd-style sentence with an underscore, and the positive document
is the correct referent.

## Details

### What the Original Data Measures

[RAR-b: Reasoning as Retrieval Benchmark](https://arxiv.org/abs/2404.06347)
describes WinoGrande as a level-1.5 task because its blank-filling format is less
like ordinary IR training data and often benefits from task instructions.
[WinoGrande: An Adversarial Winograd Schema Challenge at Scale](https://arxiv.org/abs/1907.10641)
introduces adversarially filtered Winograd-style examples requiring commonsense
referent resolution.

This retrieval split asks whether the correct entity string is closest to the
masked sentence among thousands of candidate answer strings.

### Observed Data Profile

The Nano split has 200 queries, 5,095 candidate documents, and 200 positive
qrels. Queries average 111.98 characters, while answers average 7.68 characters.

Observed positives are usually one-word referents such as names or common nouns.

### BM25 Difficulty

Using the dataset-provided BM25 candidate column, BM25 reaches nDCG@10 = 0.4306
and hit@10 = 0.7950. It ranks 23 positives first.

BM25 hit@10 is high because the correct referent is often present in the query
sentence, but top-1 ranking still requires resolving which mention fills the
blank.

### Training Data That May Help

Helpful data includes Winograd-style pronoun resolution, coreference QA,
sentence cloze answer retrieval, and adversarial commonsense examples. Avoid
using NanoRARb evaluation sentences and answer strings.

### Synthetic Data Guidance

Generate sentences with two plausible referents and a masked position. Hard
negatives should be the competing referent from the same sentence or a semantically
similar name/noun.

## Example Data

| Query | Positive document |
| --- | --- |
| Sentence: Mary wanted to get another piercing in her ear, but the _ was much too tiny.. (87 chars) | ear (3 chars) |
| Sentence: She counted her calories for her diet and found she needed more so she ate a brownie instead of an apple since the _ has fewer.. (138 chars) | apple (5 chars) |
| Sentence: The game of chess was easy to play for Angela but not Rebecca because _ had a analytical mind.. (105 chars) | Angela (6 chars) |
| Sentence: Joe immediately went to bakery before the bank because the _ had a limited supply of what he wanted.. (111 chars) | bakery (6 chars) |
| Sentence: William liked to be outside more than Kyle so _ spent time arguing for getting a pool.. (97 chars) | William (7 chars) |

## Dataset Information

| Field | Value |
| --- | --- |
| Nano set | NanoRARb |
| Backing dataset | NanoRARb |
| Task / split | NanoWinoGrande |
| Hugging Face dataset | [hakari-bench/NanoRARb](https://huggingface.co/datasets/hakari-bench/NanoRARb) |
| Language | en |
| Category | natural_language |
| Queries | 200 |
| Documents | 5095 |
| Positive qrels | 200 |
| BM25 nDCG@10 | 0.5067 |
| BM25 hit@10 | 0.8850 |
| BM25 Recall@100 | 1.0000 |
| BM25 candidate subset | top-500 (`bm25`) |
| Dense nDCG@10 | 0.4946 |
| Dense hit@10 | 0.7750 |
| Dense Recall@100 | 0.9800 |
| Dense candidate subset | top-500 (`harrier_oss_v1_270m`) |
| Reranking hybrid nDCG@10 | 0.6020 |
| Reranking hybrid hit@10 | 0.9100 |
| Reranking hybrid Recall@100 | 1.0000 |
| Reranking hybrid candidate subset | top-100 plus optional rank-101 safeguard (`reranking_hybrid`) |
| Reranking hybrid candidates / query | 100 |
| Reranking hybrid safeguard rows | 0 |
| Query length avg chars | 111.98 |
| Document length avg chars | 7.68 |

### Public Sources

- [RAR-b: Reasoning as Retrieval Benchmark](https://arxiv.org/abs/2404.06347).
- [WinoGrande: An Adversarial Winograd Schema Challenge at Scale](https://arxiv.org/abs/1907.10641).

### Hugging Face Links

- Nano dataset: [hakari-bench/NanoRARb](https://huggingface.co/datasets/hakari-bench/NanoRARb)

### Source Reference Table

| Title | Year | Type | URL |
| --- | ---: | --- | --- |
| RAR-b: Reasoning as Retrieval Benchmark | 2024 | arXiv paper | https://arxiv.org/abs/2404.06347 |
| WinoGrande: An Adversarial Winograd Schema Challenge at Scale | 2019 | arXiv paper | https://arxiv.org/abs/1907.10641 |

## Machine-Readable Metadata

<!-- benchmark-task-metadata:v1 -->

```yaml
benchmark_task_metadata:
  schema_version: 1
  document_status: first_pass
  nano_set: NanoRARb
  backing_dataset: NanoRARb
  dataset_id: hakari-bench/NanoRARb
  task_name: NanoWinoGrande
  split_name: NanoWinoGrande
  language: en
  category: natural_language
  document_path: docs/benchmark_tasks/NanoRARb/NanoWinoGrande.md
  source_research:
    primary_source_type: benchmark_paper
    paper_pdf_or_html_checked: true
  counts:
    queries: 200
    documents: 5095
    positive_qrels: 200
  positives_per_query:
    average: 1.0
    min: 1
    median: 1.0
    max: 1
    multi_positive_queries: 0
  text_stats_chars:
    query_mean: 111.975
    document_mean: 7.68243375858685
  bm25:
    ndcg_at_10: 0.5066991863724619
    hit_at_10: 0.885
    source: dataset_candidate_subset
  links:
    nano_dataset: https://huggingface.co/datasets/hakari-bench/NanoRARb
    source_urls:
    - label: RAR-b arXiv
      url: https://arxiv.org/abs/2404.06347
    - label: WinoGrande arXiv
      url: https://arxiv.org/abs/1907.10641
  references:
  - title: 'RAR-b: Reasoning as Retrieval Benchmark'
    url: https://arxiv.org/abs/2404.06347
    year: 2024
    is_paper: true
  - title: 'WinoGrande: An Adversarial Winograd Schema Challenge at Scale'
    url: https://arxiv.org/abs/1907.10641
    year: 2019
    is_paper: true
  candidate_subsets:
    bm25:
      config: bm25
      label: BM25
      source: dataset_candidate_subset
      top_k: 500
      ndcg_at_10: 0.5066991864
      hit_at_10: 0.885
      recall_at_100: 1.0
      candidate_count_min: 500
      candidate_count_max: 500
      candidate_count_mean: 500.0
      query_count: 200
      query_coverage: 1.0
      relevant_coverage_at_100: 1.0
    dense:
      config: harrier_oss_v1_270m
      label: Dense
      source: dataset_candidate_subset
      top_k: 500
      ndcg_at_10: 0.4946444306
      hit_at_10: 0.775
      recall_at_100: 0.98
      candidate_count_min: 500
      candidate_count_max: 500
      candidate_count_mean: 500.0
      query_count: 200
      query_coverage: 1.0
      relevant_coverage_at_100: 0.98
    reranking_hybrid:
      config: reranking_hybrid
      label: Reranking hybrid
      source: dataset_candidate_subset
      top_k: 100
      ndcg_at_10: 0.602030545
      hit_at_10: 0.91
      recall_at_100: 1.0
      candidate_count_min: 100
      candidate_count_max: 100
      candidate_count_mean: 100.0
      query_count: 200
      query_coverage: 1.0
      relevant_coverage_at_100: 1.0
      safeguard_positive_rows: 0
      rows_with_101_candidates: 0
```
