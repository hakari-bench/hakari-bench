# NanoDAPFAM / NanoDAPFAMOutTitlAbsToFullText

## Overview

`NanoDAPFAMOutTitlAbsToFullText` retrieves full-text patent-family records from
title-abstract queries. It is an OUT-domain split: positives are citation-linked
families without shared IPC3 classes.

## Details

### What the Original Data Measures

[DAPFAM: A Domain-Aware Family-level Dataset to benchmark cross domain patent retrieval](https://arxiv.org/abs/2506.22141)
uses OUT-domain partitions to study cross-domain patent retrieval. This split
tests whether a compact source summary can retrieve long patent records from a
different technical class.

### Observed Data Profile

The Nano split has 200 queries, 10,000 documents, and 1,259 positive qrels.
Queries average 786.64 characters, full-text target documents average 71,902.31
characters, and positives per query average 6.29.

The shorter query makes the cross-domain signal sparse. Relevant target records
may contain the answer-like prior-art relation deep inside long descriptions or
claims.

### BM25 Difficulty

Using the dataset-provided BM25 candidate column and best-ranked positive per
query, BM25 reaches nDCG@10 = 0.1102 and hit@10 = 0.2100. It ranks 8 positives
first and finds a positive in the top 100 for every query.

Full text gives BM25 more chances to match terms than title-abstract targets,
but cross-domain terminology keeps top-10 recall low.

### Training Data That May Help

Helpful training data includes cross-domain title-abstract to full-text patent
retrieval, cross-IPC citations, and prior-art search examples that require
technical analogy.

### Synthetic Data Guidance

Generate short source patent summaries and long target records from different
technical areas. Positives should share a mechanism, material, or prior-art
role despite different domain labels.

## Example Data

| Query | Positive document |
| --- | --- |
| bicycle handlebar grip a bicycle handlebar grip contains a plastic inner shell having a tubular shape and an outer surface; a fiber layer having an inner surface and an outer surface and includes a plurality of fibers interwe ... [truncated 225 chars](821 chars) | durable flexible membrane and method of making same a flexible membrane having a valuable combination of desirable properties is composed of a generally heavy, dense supporting and reinforcing reticulated base fabric constitu ... [truncated 225 chars](28042 chars) |
| method for improving belt press dewatering a method for increasing the removal of a higher fraction of liquid from the press cake in any belt press is described. specifically, the invention incorporates a series of rollers th ... [truncated 225 chars](620 chars) | artificial human anti-factor b antibody problem to be solved: to provide novel engineered forms of a monoclonal antibody and antigen-binding fragments thereof that bind complement protein factor b and selectively inhibit the ... [truncated 225 chars](108109 chars) |
| stitch distribution control system for tufting machines a stitch distribution control system for a tufting machine for controlling placement of yarns being fed to the needles of the tufting machine by yarn feed mechanisms to ... [truncated 225 chars](647 chars) | method and apparatus for measuring direction or position of weft yarn of fabric the measurement of the pick or stitches course position in continuously moved fabrics involves examining at least one gap-shaped segment in a top ... [truncated 225 chars](24253 chars) |
| low weight carpet and carpet tile and methods of manufacture low weight and non-square carpet tile suitable for use in mass transit vehicles, particularly passenger aircraft. the carpet tile preferably weighs less than about ... [truncated 225 chars](565 chars) | modular floor covering units with built-in lighting an apparatus for guiding the occupants of a structure along a path of travel within the structure is provided. the apparatus is comprised of modular floor covering units whi ... [truncated 225 chars](35319 chars) |
| method and apparatus for the zonal transmission of data using building lighting fixtures this invention relates to the zonal transmission of data by the modulation of the light output of arc lamps (150) or discharge lamps; li ... [truncated 225 chars](969 chars) | shelf tag with ambient light detector the present invention relates to an electronic shelf display device which includes an optical device and an ambient light detector circuitry. the electronic shelf display device includes ... [truncated 225 chars](54320 chars) |

## Dataset Information

| Field | Value |
| --- | --- |
| Nano set | NanoDAPFAM |
| Backing dataset | NanoDAPFAM |
| Task / split | NanoDAPFAMOutTitlAbsToFullText |
| Hugging Face dataset | [hakari-bench/NanoDAPFAM](https://huggingface.co/datasets/hakari-bench/NanoDAPFAM) |
| Language | en |
| Category | natural_language |
| Queries | 200 |
| Documents | 10000 |
| Positive qrels | 1259 |
| Positives per query | avg 6.29, min 1, median 4.0, max 20 |
| BM25 nDCG@10 | 0.0638 |
| BM25 hit@10 | 0.2100 |
| BM25 Recall@100 | 0.1875 |
| BM25 candidate subset | top-500 (`bm25`) |
| Dense nDCG@10 | 0.0952 |
| Dense hit@10 | 0.3350 |
| Dense Recall@100 | 0.2518 |
| Dense candidate subset | top-500 (`harrier_oss_v1_270m`) |
| Reranking hybrid nDCG@10 | 0.0858 |
| Reranking hybrid hit@10 | 0.3050 |
| Reranking hybrid Recall@100 | 0.2653 |
| Reranking hybrid candidate subset | top-100 plus optional rank-101 safeguard (`reranking_hybrid`) |
| Reranking hybrid candidates / query | 100-101 |
| Reranking hybrid safeguard rows | 74 |
| Query length avg chars | 786.64 |
| Document length avg chars | 71902.31 |

### Public Sources

- [DAPFAM: A Domain-Aware Family-level Dataset to benchmark cross domain patent retrieval](https://arxiv.org/abs/2506.22141); 2026; Iliass Ayaou, Denis Cavallucci, and Hicham Chibane; DOI: `10.1016/j.array.2026.100720`.
- [DAPFAM DOI record](https://doi.org/10.1016/j.array.2026.100720).
- [datalyes/DAPFAM_patent dataset card](https://huggingface.co/datasets/datalyes/DAPFAM_patent).

### Hugging Face Links

- Nano dataset: [hakari-bench/NanoDAPFAM](https://huggingface.co/datasets/hakari-bench/NanoDAPFAM)
- Source dataset: [datalyes/DAPFAM_patent](https://huggingface.co/datasets/datalyes/DAPFAM_patent)

### Source Reference Table

| Title | Year | Type | URL |
| --- | ---: | --- | --- |
| DAPFAM: A Domain-Aware Family-level Dataset to benchmark cross domain patent retrieval | 2026 | arXiv paper | https://arxiv.org/abs/2506.22141 |
| DAPFAM DOI record | 2026 | DOI | https://doi.org/10.1016/j.array.2026.100720 |
| datalyes/DAPFAM_patent | 2025 | dataset card | https://huggingface.co/datasets/datalyes/DAPFAM_patent |

## Machine-Readable Metadata

<!-- benchmark-task-metadata:v1 -->

```yaml
benchmark_task_metadata:
  schema_version: 1
  document_status: first_pass
  nano_set: NanoDAPFAM
  backing_dataset: NanoDAPFAM
  dataset_id: hakari-bench/NanoDAPFAM
  task_name: NanoDAPFAMOutTitlAbsToFullText
  split_name: NanoDAPFAMOutTitlAbsToFullText
  language: en
  category: natural_language
  document_path: docs/benchmark_tasks/NanoDAPFAM/NanoDAPFAMOutTitlAbsToFullText.md
  source_research:
    primary_source_type: benchmark_paper
    paper_pdf_or_html_checked: true
  counts:
    queries: 200
    documents: 10000
    positive_qrels: 1259
  positives_per_query:
    average: 6.295
    min: 1
    median: 4.0
    max: 20
    multi_positive_queries: 139
  text_stats_chars:
    query_mean: 786.64
    document_mean: 71902.3141
  bm25:
    ndcg_at_10: 0.06380115115854927
    hit_at_10: 0.21
    source: dataset_candidate_subset
  learning:
    original_train_split: not_confirmed
    evaluation_split_origin: DAPFAM OUT-domain title-abstract to full-text patent-family
      retrieval
    train_eval_overlap_audit: not_audited
    leakage_note: exclude NanoDAPFAM evaluation family IDs, positives, and qrels
    useful_training_data:
    - cross-domain title-abstract patent retrieval
    - cross-IPC patent citation pairs
    - long-target prior-art search
    synthetic_data:
      document_generation: long full-text patent records from different technical
        classes
      question_generation: compact source patent title and abstract summaries
      answerability: positives should be cited cross-domain patent families
    multi_positive_training: citation_family_multi_positive
  links:
    nano_dataset: https://huggingface.co/datasets/hakari-bench/NanoDAPFAM
    source_urls:
    - label: DAPFAM arXiv
      url: https://arxiv.org/abs/2506.22141
    - label: DAPFAM DOI
      url: https://doi.org/10.1016/j.array.2026.100720
    - label: datalyes/DAPFAM_patent
      url: https://huggingface.co/datasets/datalyes/DAPFAM_patent
  references:
  - title: 'DAPFAM: A Domain-Aware Family-level Dataset to benchmark cross domain
      patent retrieval'
    url: https://arxiv.org/abs/2506.22141
    year: 2026
    doi: 10.1016/j.array.2026.100720
    is_paper: true
    source_confidence: definitive_paper_link
  candidate_subsets:
    bm25:
      config: bm25
      label: BM25
      source: dataset_candidate_subset
      top_k: 500
      ndcg_at_10: 0.0638011512
      hit_at_10: 0.21
      recall_at_100: 0.1874503574
      candidate_count_min: 500
      candidate_count_max: 500
      candidate_count_mean: 500.0
      query_count: 200
      query_coverage: 1.0
      relevant_coverage_at_100: 0.1874503574
    dense:
      config: harrier_oss_v1_270m
      label: Dense
      source: dataset_candidate_subset
      top_k: 500
      ndcg_at_10: 0.0951616834
      hit_at_10: 0.335
      recall_at_100: 0.2517871326
      candidate_count_min: 500
      candidate_count_max: 500
      candidate_count_mean: 500.0
      query_count: 200
      query_coverage: 1.0
      relevant_coverage_at_100: 0.2517871326
    reranking_hybrid:
      config: reranking_hybrid
      label: Reranking hybrid
      source: dataset_candidate_subset
      top_k: 100
      ndcg_at_10: 0.085756564
      hit_at_10: 0.305
      recall_at_100: 0.2652899126
      candidate_count_min: 100
      candidate_count_max: 101
      candidate_count_mean: 100.37
      query_count: 200
      query_coverage: 1.0
      relevant_coverage_at_100: 0.2652899126
      safeguard_positive_rows: 74
      rows_with_101_candidates: 74
```
