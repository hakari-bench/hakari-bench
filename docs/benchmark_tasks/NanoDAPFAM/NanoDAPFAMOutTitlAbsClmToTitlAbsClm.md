# NanoDAPFAM / NanoDAPFAMOutTitlAbsClmToTitlAbsClm

## Overview

`NanoDAPFAMOutTitlAbsClmToTitlAbsClm` is a cross-domain patent-family retrieval
task where both source and target records include title, abstract, and claims.
Positive targets are citation-linked families without shared IPC3 codes.

## Details

### What the Original Data Measures

[DAPFAM: A Domain-Aware Family-level Dataset to benchmark cross domain patent retrieval](https://arxiv.org/abs/2506.22141)
uses OUT-domain pairs to evaluate whether retrieval systems can find cited
patent families outside the source family's technical class. This split keeps
claims on both sides, preserving detailed legal and technical language.

### Observed Data Profile

The Nano split has 200 queries, 10,000 documents, and 1,259 positive qrels.
Queries average 9,315.69 characters, documents average 7,257.19 characters, and
positives per query average 6.29.

The text contains long claims on both sides, but the cross-domain relation means
the shared signal may be a material, component, or process rather than the
headline invention category.

### BM25 Difficulty

Using the dataset-provided BM25 candidate column and the best-ranked positive
per query, BM25 reaches nDCG@10 = 0.1188 and hit@10 = 0.2200. It ranks 7
positives first and places a positive in the top 100 for all 200 queries.

Claims help BM25 compared with title-abstract targets, but cross-domain
terminology still makes top-10 retrieval difficult.

### Training Data That May Help

Useful training data includes cross-domain citation retrieval with claims,
patent technology-transfer datasets, and hard-negative mining across IPC/CPC
classes.

### Synthetic Data Guidance

Generate claim-rich source and target patent records from different technical
classes. Positives should encode transferable mechanisms; negatives should
share legal claim phrasing or components without the same technical dependency.

## Example Data

| Query | Positive document |
| --- | --- |
| bicycle handlebar grip a bicycle handlebar grip contains a plastic inner shell having a tubular shape and an outer surface; a fiber layer having an inner surface and an outer surface and includes a plurality of fibers interwe ... [truncated 225 chars](2588 chars) | durable flexible membrane and method of making same a flexible membrane having a valuable combination of desirable properties is composed of a generally heavy, dense supporting and reinforcing reticulated base fabric constitu ... [truncated 225 chars](7657 chars) |
| method for improving belt press dewatering a method for increasing the removal of a higher fraction of liquid from the press cake in any belt press is described. specifically, the invention incorporates a series of rollers th ... [truncated 225 chars](4605 chars) | artificial human anti-factor b antibody problem to be solved: to provide novel engineered forms of a monoclonal antibody and antigen-binding fragments thereof that bind complement protein factor b and selectively inhibit the ... [truncated 225 chars](1425 chars) |
| stitch distribution control system for tufting machines a stitch distribution control system for a tufting machine for controlling placement of yarns being fed to the needles of the tufting machine by yarn feed mechanisms to ... [truncated 225 chars](5968 chars) | method and apparatus for measuring direction or position of weft yarn of fabric the measurement of the pick or stitches course position in continuously moved fabrics involves examining at least one gap-shaped segment in a top ... [truncated 225 chars](5290 chars) |
| low weight carpet and carpet tile and methods of manufacture low weight and non-square carpet tile suitable for use in mass transit vehicles, particularly passenger aircraft. the carpet tile preferably weighs less than about ... [truncated 225 chars](3799 chars) | modular floor covering units with built-in lighting an apparatus for guiding the occupants of a structure along a path of travel within the structure is provided. the apparatus is comprised of modular floor covering units whi ... [truncated 225 chars](17660 chars) |
| method and apparatus for the zonal transmission of data using building lighting fixtures this invention relates to the zonal transmission of data by the modulation of the light output of arc lamps (150) or discharge lamps; li ... [truncated 225 chars](7344 chars) | shelf tag with ambient light detector the present invention relates to an electronic shelf display device which includes an optical device and an ambient light detector circuitry. the electronic shelf display device includes ... [truncated 225 chars](7219 chars) |

## Dataset Information

| Field | Value |
| --- | --- |
| Nano set | NanoDAPFAM |
| Backing dataset | NanoDAPFAM |
| Task / split | NanoDAPFAMOutTitlAbsClmToTitlAbsClm |
| Hugging Face dataset | [hakari-bench/NanoDAPFAM](https://huggingface.co/datasets/hakari-bench/NanoDAPFAM) |
| Language | en |
| Category | natural_language |
| Queries | 200 |
| Documents | 10000 |
| Positive qrels | 1259 |
| Positives per query | avg 6.29, min 1, median 4.0, max 20 |
| BM25 nDCG@10 | 0.0640 |
| BM25 hit@10 | 0.2400 |
| BM25 Recall@100 | 0.1684 |
| BM25 candidate subset | top-500 (`bm25`) |
| Dense nDCG@10 | 0.0952 |
| Dense hit@10 | 0.3100 |
| Dense Recall@100 | 0.2462 |
| Dense candidate subset | top-500 (`harrier_oss_v1_270m`) |
| Reranking hybrid nDCG@10 | 0.0811 |
| Reranking hybrid hit@10 | 0.3100 |
| Reranking hybrid Recall@100 | 0.2423 |
| Reranking hybrid candidate subset | top-100 plus optional rank-101 safeguard (`reranking_hybrid`) |
| Reranking hybrid candidates / query | 100-101 |
| Reranking hybrid safeguard rows | 72 |
| Query length avg chars | 9315.69 |
| Document length avg chars | 7257.19 |

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
  task_name: NanoDAPFAMOutTitlAbsClmToTitlAbsClm
  split_name: NanoDAPFAMOutTitlAbsClmToTitlAbsClm
  language: en
  category: natural_language
  document_path: docs/benchmark_tasks/NanoDAPFAM/NanoDAPFAMOutTitlAbsClmToTitlAbsClm.md
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
    query_mean: 9315.675
    document_mean: 7257.1909
  bm25:
    ndcg_at_10: 0.0640324381027413
    hit_at_10: 0.24
    source: dataset_candidate_subset
  learning:
    original_train_split: not_confirmed
    evaluation_split_origin: DAPFAM OUT-domain title-abstract-claims to title-abstract-claims
      patent-family retrieval
    train_eval_overlap_audit: not_audited
    leakage_note: exclude NanoDAPFAM evaluation families and qrels
    useful_training_data:
    - cross-domain patent claim retrieval
    - cross-IPC citation prediction
    - patent technology-transfer retrieval
    synthetic_data:
      document_generation: claim-rich patent records from different technical classes
      question_generation: source patent title abstract and claims records
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
      ndcg_at_10: 0.0640324381
      hit_at_10: 0.24
      recall_at_100: 0.1683876092
      candidate_count_min: 500
      candidate_count_max: 500
      candidate_count_mean: 500.0
      query_count: 200
      query_coverage: 1.0
      relevant_coverage_at_100: 0.1683876092
    dense:
      config: harrier_oss_v1_270m
      label: Dense
      source: dataset_candidate_subset
      top_k: 500
      ndcg_at_10: 0.0952275196
      hit_at_10: 0.31
      recall_at_100: 0.2462271644
      candidate_count_min: 500
      candidate_count_max: 500
      candidate_count_mean: 500.0
      query_count: 200
      query_coverage: 1.0
      relevant_coverage_at_100: 0.2462271644
    reranking_hybrid:
      config: reranking_hybrid
      label: Reranking hybrid
      source: dataset_candidate_subset
      top_k: 100
      ndcg_at_10: 0.0811288804
      hit_at_10: 0.31
      recall_at_100: 0.2422557585
      candidate_count_min: 100
      candidate_count_max: 101
      candidate_count_mean: 100.36
      query_count: 200
      query_coverage: 1.0
      relevant_coverage_at_100: 0.2422557585
      safeguard_positive_rows: 72
      rows_with_101_candidates: 72
```
