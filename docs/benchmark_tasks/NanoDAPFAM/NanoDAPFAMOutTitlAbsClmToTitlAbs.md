# NanoDAPFAM / NanoDAPFAMOutTitlAbsClmToTitlAbs

## Overview

`NanoDAPFAMOutTitlAbsClmToTitlAbs` retrieves short title-abstract patent-family
records from long title-abstract-claims queries. It is an OUT-domain DAPFAM
split, so positives do not share IPC3 classes with the source family.

## Details

### What the Original Data Measures

[DAPFAM: A Domain-Aware Family-level Dataset to benchmark cross domain patent retrieval](https://arxiv.org/abs/2506.22141)
uses OUT-domain citation pairs to evaluate cross-domain prior-art retrieval. In
this variant, the source side is detailed but the target side is compact, making
cross-domain evidence especially sparse.

### Observed Data Profile

The Nano split has 200 queries, 10,000 documents, and 1,257 positive qrels.
Queries average 9,315.69 characters, documents average 777.87 characters, and
positives per query average 6.29.

Observed pairs often have weak surface overlap: the source may describe one
product or apparatus category, while the cited target describes a transferable
material, process, or component from another technical area.

### BM25 Difficulty

Using the dataset-provided BM25 candidate column and best-ranked positive per
query, BM25 reaches nDCG@10 = 0.0719 and hit@10 = 0.1150. Only 6 positives are
ranked first, though every query has a positive in the top 100.

This is one of the hardest NanoDAPFAM lexical baselines because target abstracts
are short and cross-domain positives often lack exact query terms.

### Training Data That May Help

Useful training data includes cross-IPC patent citation pairs where targets are
represented by title and abstract, analogy-style patent retrieval, and
technology-transfer prior-art search.

### Synthetic Data Guidance

Generate long source patent claims and short target summaries from different
technical classes. Positives should preserve a transferable mechanism; hard
negatives should match surface words inside the source domain.

## Example Data

| Query | Positive document |
| --- | --- |
| bicycle handlebar grip a bicycle handlebar grip contains a plastic inner shell having a tubular shape and an outer surface; a fiber layer having an inner surface and an outer surface and includes a plurality of fibers interwe ... [truncated 225 chars](2588 chars) | durable flexible membrane and method of making same a flexible membrane having a valuable combination of desirable properties is composed of a generally heavy, dense supporting and reinforcing reticulated base fabric constitu ... [truncated 225 chars](1921 chars) |
| method for improving belt press dewatering a method for increasing the removal of a higher fraction of liquid from the press cake in any belt press is described. specifically, the invention incorporates a series of rollers th ... [truncated 225 chars](4605 chars) | artificial human anti-factor b antibody problem to be solved: to provide novel engineered forms of a monoclonal antibody and antigen-binding fragments thereof that bind complement protein factor b and selectively inhibit the ... [truncated 225 chars](533 chars) |
| stitch distribution control system for tufting machines a stitch distribution control system for a tufting machine for controlling placement of yarns being fed to the needles of the tufting machine by yarn feed mechanisms to ... [truncated 225 chars](5968 chars) | method and apparatus for measuring direction or position of weft yarn of fabric the measurement of the pick or stitches course position in continuously moved fabrics involves examining at least one gap-shaped segment in a top ... [truncated 225 chars](789 chars) |
| low weight carpet and carpet tile and methods of manufacture low weight and non-square carpet tile suitable for use in mass transit vehicles, particularly passenger aircraft. the carpet tile preferably weighs less than about ... [truncated 225 chars](3799 chars) | modular floor covering units with built-in lighting an apparatus for guiding the occupants of a structure along a path of travel within the structure is provided. the apparatus is comprised of modular floor covering units whi ... [truncated 225 chars](785 chars) |
| method and apparatus for the zonal transmission of data using building lighting fixtures this invention relates to the zonal transmission of data by the modulation of the light output of arc lamps (150) or discharge lamps; li ... [truncated 225 chars](7344 chars) | shelf tag with ambient light detector the present invention relates to an electronic shelf display device which includes an optical device and an ambient light detector circuitry. the electronic shelf display device includes ... [truncated 225 chars](1213 chars) |

## Dataset Information

| Field | Value |
| --- | --- |
| Nano set | NanoDAPFAM |
| Backing dataset | NanoDAPFAM |
| Task / split | NanoDAPFAMOutTitlAbsClmToTitlAbs |
| Hugging Face dataset | [hakari-bench/NanoDAPFAM](https://huggingface.co/datasets/hakari-bench/NanoDAPFAM) |
| Language | en |
| Category | natural_language |
| Queries | 200 |
| Documents | 10000 |
| Positive qrels | 1257 |
| Positives per query | avg 6.29, min 1, median 4.0, max 20 |
| BM25 nDCG@10 | 0.0439 |
| BM25 hit@10 | 0.1600 |
| BM25 Recall@100 | 0.1225 |
| BM25 candidate subset | top-500 (`bm25`) |
| Dense nDCG@10 | 0.0872 |
| Dense hit@10 | 0.2900 |
| Dense Recall@100 | 0.2235 |
| Dense candidate subset | top-500 (`harrier_oss_v1_270m`) |
| Reranking hybrid nDCG@10 | 0.0714 |
| Reranking hybrid hit@10 | 0.2500 |
| Reranking hybrid Recall@100 | 0.2220 |
| Reranking hybrid candidate subset | top-100 plus optional rank-101 safeguard (`reranking_hybrid`) |
| Reranking hybrid candidates / query | 100-101 |
| Reranking hybrid safeguard rows | 77 |
| Query length avg chars | 9315.69 |
| Document length avg chars | 777.87 |

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
  task_name: NanoDAPFAMOutTitlAbsClmToTitlAbs
  split_name: NanoDAPFAMOutTitlAbsClmToTitlAbs
  language: en
  category: natural_language
  document_path: docs/benchmark_tasks/NanoDAPFAM/NanoDAPFAMOutTitlAbsClmToTitlAbs.md
  source_research:
    primary_source_type: benchmark_paper
    paper_pdf_or_html_checked: true
  counts:
    queries: 200
    documents: 10000
    positive_qrels: 1257
  positives_per_query:
    average: 6.285
    min: 1
    median: 4.0
    max: 20
    multi_positive_queries: 139
  text_stats_chars:
    query_mean: 9315.675
    document_mean: 777.8655
  bm25:
    ndcg_at_10: 0.04385346684717721
    hit_at_10: 0.16
    source: dataset_candidate_subset
  learning:
    original_train_split: not_confirmed
    evaluation_split_origin: DAPFAM OUT-domain title-abstract-claims to title-abstract
      patent-family retrieval
    train_eval_overlap_audit: not_audited
    leakage_note: exclude NanoDAPFAM evaluation families and qrels
    useful_training_data:
    - cross-IPC patent citation retrieval
    - cross-domain prior-art search with short targets
    - patent analogy retrieval
    synthetic_data:
      document_generation: short target title and abstract records from different
        technical classes
      question_generation: long source title abstract and claims records
      answerability: positives should be cited cross-domain summaries
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
      ndcg_at_10: 0.0438534668
      hit_at_10: 0.16
      recall_at_100: 0.122513922
      candidate_count_min: 500
      candidate_count_max: 500
      candidate_count_mean: 500.0
      query_count: 200
      query_coverage: 1.0
      relevant_coverage_at_100: 0.122513922
    dense:
      config: harrier_oss_v1_270m
      label: Dense
      source: dataset_candidate_subset
      top_k: 500
      ndcg_at_10: 0.0871614447
      hit_at_10: 0.29
      recall_at_100: 0.2235481305
      candidate_count_min: 500
      candidate_count_max: 500
      candidate_count_mean: 500.0
      query_count: 200
      query_coverage: 1.0
      relevant_coverage_at_100: 0.2235481305
    reranking_hybrid:
      config: reranking_hybrid
      label: Reranking hybrid
      source: dataset_candidate_subset
      top_k: 100
      ndcg_at_10: 0.0714373801
      hit_at_10: 0.25
      recall_at_100: 0.2219570406
      candidate_count_min: 100
      candidate_count_max: 101
      candidate_count_mean: 100.385
      query_count: 200
      query_coverage: 1.0
      relevant_coverage_at_100: 0.2219570406
      safeguard_positive_rows: 77
      rows_with_101_candidates: 77
```
