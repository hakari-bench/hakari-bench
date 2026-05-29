# NanoDAPFAM / NanoDAPFAMAllTitlAbsToTitlAbs

## Overview

`NanoDAPFAMAllTitlAbsToTitlAbs` is a compact patent-family retrieval task where
both query and target use title plus abstract text. It uses DAPFAM's ALL
citation relevance condition, mixing same-IPC3 and cross-IPC3 positives.

## Details

### What the Original Data Measures

[DAPFAM: A Domain-Aware Family-level Dataset to benchmark cross domain patent retrieval](https://arxiv.org/abs/2506.22141)
evaluates patent retrieval at family level with citation-based relevance and
explicit in-domain/out-domain partitioning by IPC3 overlap. This split is the
short-text representation of the ALL condition: source and target families are
both represented by title and abstract only.

### Observed Data Profile

The Nano split has 200 queries, 10,000 candidate documents, and 3,982 positive
qrels. Every query is multi-positive, averaging 19.91 positives. Query text
averages 776.02 characters and document text averages 777.97 characters.

Observed records read like patent abstracts rather than natural-language search
queries. They contain problem-solution phrasing, apparatus descriptions, and
technical component names.

### BM25 Difficulty

Using the dataset-provided BM25 candidate column and the best-ranked positive
per query, BM25 reaches nDCG@10 = 0.6619 and hit@10 = 0.8500. BM25 ranks 97
positives first and places a positive in the top 100 for all 200 queries.

This is one of the easier DAPFAM ALL variants for lexical matching. Titles and
abstracts are concise enough to reduce full-text noise while preserving strong
technical keywords.

### Training Data That May Help

Useful data includes patent title-abstract citation pairs, prior-art search
pairs, and family-level patent semantic similarity outside the evaluation
families. Training should avoid using DAPFAM Nano qrels or family IDs from this
split.

### Synthetic Data Guidance

Generate title-abstract patent summaries across many technical areas. Pair
summaries through citation-like dependency, shared technical problem, or
improvement-over-prior-art relations, and include hard negatives with overlapping
keywords but different inventions.

## Example Data

| Query | Positive document |
| --- | --- |
| snow removal equipment with automatic walking function the invention relates to snow removal equipment with an automatic walking function. the snow removal equipment comprises a walking module, a working module and a control ... [truncated 225 chars](988 chars) | multifunctional device for clearing snow an apparatus and method for clearing an accumulation of matter from a surface that includes a blade configured to collect matter upon movement of the apparatus and means to shift the c ... [truncated 225 chars](643 chars) |
| modular intelligent transportation system a modular intelligent transportation system, comprising an environmentally protected enclosure, a system communications bus, a processor module, communicating with said bus, having a ... [truncated 225 chars](708 chars) | impact media sharing an example operation includes one or more of associating a transport with an impact in proximity to one or more other transports, transmitting, by a device in proximity to the impact, media related to the ... [truncated 225 chars](462 chars) |
| synthetic hollow microspheres this invention relates to a method of forming a synthetic hollow microsphere comprising the steps of preparing an agglomerate precursor, said agglomerate precursor including a primary component a ... [truncated 225 chars](602 chars) | process for preparing metal-coated hollow microspheres a process for preparing a metal-coated hollow microsphere comprising the combination of steps of: (a) vigorously admixing a major quantity of hollow cenospheres/microsphe ... [truncated 225 chars](821 chars) |
| low weight carpet and carpet tile and methods of manufacture low weight and non-square carpet tile suitable for use in mass transit vehicles, particularly passenger aircraft. the carpet tile preferably weighs less than about ... [truncated 225 chars](565 chars) | anti-static mats and carpets a novel carpet material or mat which is characterized by an extraordinary ability to quickly and comfortably discharge any build-up of a static electricity charge on a person who has built up such ... [truncated 225 chars](510 chars) |
| steering system with lane keeping integration a system for steering a vehicle including: an actuator disposed in a vehicle to apply torque to a steerable wheel; a driver input device receptive to driver commands for directing ... [truncated 225 chars](934 chars) | steer torque manager for an advanced driver assistance system of a road vehicle a steer torque manager for an advanced driver assistance system of a road vehicle and a method therefor. a driver-in-the-loop functionality deter ... [truncated 225 chars](985 chars) |

## Dataset Information

| Field | Value |
| --- | --- |
| Nano set | NanoDAPFAM |
| Backing dataset | NanoDAPFAM |
| Task / split | NanoDAPFAMAllTitlAbsToTitlAbs |
| Hugging Face dataset | [hakari-bench/NanoDAPFAM](https://huggingface.co/datasets/hakari-bench/NanoDAPFAM) |
| Language | en |
| Category | natural_language |
| Queries | 200 |
| Documents | 10000 |
| Positive qrels | 3982 |
| Positives per query | avg 19.91, min 9, median 20.0, max 20 |
| BM25 nDCG@10 | 0.3281 |
| BM25 hit@10 | 0.8750 |
| BM25 Recall@100 | 0.3908 |
| BM25 candidate subset | top-500 (`bm25`) |
| Dense nDCG@10 | 0.3786 |
| Dense hit@10 | 0.8950 |
| Dense Recall@100 | 0.5068 |
| Dense candidate subset | top-500 (`harrier_oss_v1_270m`) |
| Reranking hybrid nDCG@10 | 0.3790 |
| Reranking hybrid hit@10 | 0.8800 |
| Reranking hybrid Recall@100 | 0.5020 |
| Reranking hybrid candidate subset | top-100 plus optional rank-101 safeguard (`reranking_hybrid`) |
| Reranking hybrid candidates / query | 100-101 |
| Reranking hybrid safeguard rows | 8 |
| Query length avg chars | 776.02 |
| Document length avg chars | 777.97 |

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
  task_name: NanoDAPFAMAllTitlAbsToTitlAbs
  split_name: NanoDAPFAMAllTitlAbsToTitlAbs
  language: en
  category: natural_language
  document_path: docs/benchmark_tasks/NanoDAPFAM/NanoDAPFAMAllTitlAbsToTitlAbs.md
  source_research:
    primary_source_type: benchmark_paper
    paper_pdf_or_html_checked: true
  counts:
    queries: 200
    documents: 10000
    positive_qrels: 3982
  positives_per_query:
    average: 19.91
    min: 9
    median: 20.0
    max: 20
    multi_positive_queries: 200
  text_stats_chars:
    query_mean: 776.02
    document_mean: 777.9716
  bm25:
    ndcg_at_10: 0.32809521313876094
    hit_at_10: 0.875
    source: dataset_candidate_subset
  learning:
    original_train_split: not_confirmed
    evaluation_split_origin: DAPFAM ALL title-abstract to title-abstract patent-family
      retrieval
    train_eval_overlap_audit: not_audited
    leakage_note: exclude NanoDAPFAM evaluation families and citation labels
    useful_training_data:
    - patent title-abstract citation retrieval
    - prior-art title-abstract search pairs
    - family-level patent similarity data
    synthetic_data:
      document_generation: compact patent title and abstract records across technical
        fields
      question_generation: patent title and abstract summaries used as queries
      answerability: positives should be cited or technically related patent families
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
      ndcg_at_10: 0.3280952131
      hit_at_10: 0.875
      recall_at_100: 0.3907584129
      candidate_count_min: 500
      candidate_count_max: 500
      candidate_count_mean: 500.0
      query_count: 200
      query_coverage: 1.0
      relevant_coverage_at_100: 0.3907584129
    dense:
      config: harrier_oss_v1_270m
      label: Dense
      source: dataset_candidate_subset
      top_k: 500
      ndcg_at_10: 0.3785515544
      hit_at_10: 0.895
      recall_at_100: 0.5067805123
      candidate_count_min: 500
      candidate_count_max: 500
      candidate_count_mean: 500.0
      query_count: 200
      query_coverage: 1.0
      relevant_coverage_at_100: 0.5067805123
    reranking_hybrid:
      config: reranking_hybrid
      label: Reranking hybrid
      source: dataset_candidate_subset
      top_k: 100
      ndcg_at_10: 0.3789928192
      hit_at_10: 0.88
      recall_at_100: 0.5020090407
      candidate_count_min: 100
      candidate_count_max: 101
      candidate_count_mean: 100.04
      query_count: 200
      query_coverage: 1.0
      relevant_coverage_at_100: 0.5020090407
      safeguard_positive_rows: 8
      rows_with_101_candidates: 8
```
