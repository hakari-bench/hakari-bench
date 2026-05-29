# NanoDAPFAM / NanoDAPFAMInTitlAbsToFullText

## Overview

`NanoDAPFAMInTitlAbsToFullText` retrieves full-text patent-family records from
title-abstract queries. Positives are IN-domain DAPFAM citation links where the
query and target share an IPC3 class.

## Details

### What the Original Data Measures

[DAPFAM: A Domain-Aware Family-level Dataset to benchmark cross domain patent retrieval](https://arxiv.org/abs/2506.22141)
reports that domain partitions are central to understanding patent retrieval
difficulty. This split represents the same-domain setting with compact queries
and full target documents.

### Observed Data Profile

The Nano split has 200 queries, 10,000 documents, and 3,072 positive qrels.
Queries average 771.33 characters, and full-text targets average 68,924.34
characters. Positives per query average 15.36.

The query title and abstract usually identify the technical problem and proposed
solution, while full target records contain detailed descriptions and claims
from same-domain patent families.

### BM25 Difficulty

Using the dataset-provided BM25 candidate column and best-ranked positive per
query, BM25 reaches nDCG@10 = 0.6643 and hit@10 = 0.8500. It ranks 95 positives
first and finds a positive in the top 100 for every query.

The same-domain restriction and long targets make lexical matching effective,
though the task still requires choosing among many related patents.

### Training Data That May Help

Useful data includes same-domain title-abstract prior-art search against full
patent records, family-level citation retrieval, and patent semantic search
outside NanoDAPFAM evaluation families.

### Synthetic Data Guidance

Generate compact source summaries and long same-domain target records. Positives
should share a cited technical mechanism, while hard negatives should have
similar IPC terms but no direct prior-art relation.

## Example Data

| Query | Positive document |
| --- | --- |
| snow removal equipment with automatic walking function the invention relates to snow removal equipment with an automatic walking function. the snow removal equipment comprises a walking module, a working module and a control ... [truncated 225 chars](988 chars) | multifunctional device for clearing snow an apparatus and method for clearing an accumulation of matter from a surface that includes a blade configured to collect matter upon movement of the apparatus and means to shift the c ... [truncated 225 chars](59310 chars) |
| waste disposal devices waste disposal device including a housing defining a waste compartment for receiving enclosed waste and arranged to removably receive a cartridge containing a length of flexible tubing which operatively ... [truncated 225 chars](891 chars) | cassette for dispensing pleated tubing a cassette for use in dispensing a pleated tubing. the cassette includes an annular body having a generally u shaped housing with an open central cylindrical core. the annular body inclu ... [truncated 225 chars](36269 chars) |
| an article including identification for use in an electrically heated smoking system. there is provided an electrically heated smoking system (101) for receiving a smoking article (115) or cleaning article (205) configured fo ... [truncated 225 chars](1164 chars) | apparatus for generating aerosol from an aerosolisable medium, an article of aerosolisable medium and a method of determining a parameter of an article to provide an apparatus that heats an aerosolizable medium to volatilize ... [truncated 225 chars](52756 chars) |
| low weight carpet and carpet tile and methods of manufacture low weight and non-square carpet tile suitable for use in mass transit vehicles, particularly passenger aircraft. the carpet tile preferably weighs less than about ... [truncated 225 chars](565 chars) | anti-static mats and carpets a novel carpet material or mat which is characterized by an extraordinary ability to quickly and comfortably discharge any build-up of a static electricity charge on a person who has built up such ... [truncated 225 chars](17195 chars) |
| organosilicon precursors for interlayer dielectric films with low dielectric constants a method of forming a low dielectric constant interlayer dielectric film on a substrate by reacting, under chemical vapor deposition condi ... [truncated 225 chars](546 chars) | radiation shield a radiation shield and an assembly and a reactor including the radiation shield are disclosed. the radiation shield can be used to control heat flux from a susceptor heater assembly and thereby enable better ... [truncated 225 chars](48536 chars) |

## Dataset Information

| Field | Value |
| --- | --- |
| Nano set | NanoDAPFAM |
| Backing dataset | NanoDAPFAM |
| Task / split | NanoDAPFAMInTitlAbsToFullText |
| Hugging Face dataset | [hakari-bench/NanoDAPFAM](https://huggingface.co/datasets/hakari-bench/NanoDAPFAM) |
| Language | en |
| Category | natural_language |
| Queries | 200 |
| Documents | 10000 |
| Positive qrels | 3072 |
| Positives per query | avg 15.36, min 1, median 18.0, max 20 |
| BM25 nDCG@10 | 0.3490 |
| BM25 hit@10 | 0.8200 |
| BM25 Recall@100 | 0.5677 |
| BM25 candidate subset | top-500 (`bm25`) |
| Dense nDCG@10 | 0.4255 |
| Dense hit@10 | 0.8750 |
| Dense Recall@100 | 0.6729 |
| Dense candidate subset | top-500 (`harrier_oss_v1_270m`) |
| Reranking hybrid nDCG@10 | 0.4228 |
| Reranking hybrid hit@10 | 0.8900 |
| Reranking hybrid Recall@100 | 0.6803 |
| Reranking hybrid candidate subset | top-100 plus optional rank-101 safeguard (`reranking_hybrid`) |
| Reranking hybrid candidates / query | 100-101 |
| Reranking hybrid safeguard rows | 5 |
| Query length avg chars | 771.33 |
| Document length avg chars | 68924.34 |

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
  task_name: NanoDAPFAMInTitlAbsToFullText
  split_name: NanoDAPFAMInTitlAbsToFullText
  language: en
  category: natural_language
  document_path: docs/benchmark_tasks/NanoDAPFAM/NanoDAPFAMInTitlAbsToFullText.md
  source_research:
    primary_source_type: benchmark_paper
    paper_pdf_or_html_checked: true
  counts:
    queries: 200
    documents: 10000
    positive_qrels: 3072
  positives_per_query:
    average: 15.36
    min: 1
    median: 18.0
    max: 20
    multi_positive_queries: 198
  text_stats_chars:
    query_mean: 771.33
    document_mean: 68924.3436
  bm25:
    ndcg_at_10: 0.34904709347662766
    hit_at_10: 0.82
    source: dataset_candidate_subset
  learning:
    original_train_split: not_confirmed
    evaluation_split_origin: DAPFAM IN-domain title-abstract to full-text patent-family
      retrieval
    train_eval_overlap_audit: not_audited
    leakage_note: exclude NanoDAPFAM evaluation family IDs and citation labels
    useful_training_data:
    - same-domain title-abstract patent retrieval
    - full-text patent prior-art search
    - family-level citation retrieval
    synthetic_data:
      document_generation: full-text same-domain patent family records
      question_generation: title and abstract source patent summaries
      answerability: positives should be cited same-domain families
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
      ndcg_at_10: 0.3490470935
      hit_at_10: 0.82
      recall_at_100: 0.5677083333
      candidate_count_min: 500
      candidate_count_max: 500
      candidate_count_mean: 500.0
      query_count: 200
      query_coverage: 1.0
      relevant_coverage_at_100: 0.5677083333
    dense:
      config: harrier_oss_v1_270m
      label: Dense
      source: dataset_candidate_subset
      top_k: 500
      ndcg_at_10: 0.4254613529
      hit_at_10: 0.875
      recall_at_100: 0.6728515625
      candidate_count_min: 500
      candidate_count_max: 500
      candidate_count_mean: 500.0
      query_count: 200
      query_coverage: 1.0
      relevant_coverage_at_100: 0.6728515625
    reranking_hybrid:
      config: reranking_hybrid
      label: Reranking hybrid
      source: dataset_candidate_subset
      top_k: 100
      ndcg_at_10: 0.4228331588
      hit_at_10: 0.89
      recall_at_100: 0.6803385417
      candidate_count_min: 100
      candidate_count_max: 101
      candidate_count_mean: 100.025
      query_count: 200
      query_coverage: 1.0
      relevant_coverage_at_100: 0.6803385417
      safeguard_positive_rows: 5
      rows_with_101_candidates: 5
```
