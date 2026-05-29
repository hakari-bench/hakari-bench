# NanoDAPFAM / NanoDAPFAMInTitlAbsClmToFullText

## Overview

`NanoDAPFAMInTitlAbsClmToFullText` is an in-domain English patent-family
retrieval task. The query contains title, abstract, and claims, while the target
contains full patent-family text. Positives are DAPFAM citation relations where
the query and target share at least one IPC3 technical class.

## Details

### What the Original Data Measures

[DAPFAM: A Domain-Aware Family-level Dataset to benchmark cross domain patent retrieval](https://arxiv.org/abs/2506.22141)
defines IN-domain patent retrieval by IPC3 overlap between cited and citing
families. The paper uses this contrast with OUT-domain retrieval to test whether
models can retrieve prior art inside familiar technical areas and across domain
boundaries. This split is the long-query, full-target version of the IN-domain
condition.

### Observed Data Profile

The Nano split has 200 queries, 10,000 documents, and 3,069 positive qrels.
Queries average 8,405.48 characters and full-text target documents average
68,905.96 characters. Positives per query average 15.35, with a minimum of 1 and
a maximum of 20.

Observed examples include nanoparticle luminescence, soil remediation, and other
same-area patent families. The shared IPC3 condition means lexical and
terminological overlap is expected to be stronger than in the OUT-domain tasks.

### BM25 Difficulty

Using the dataset-provided BM25 candidate column and the best-ranked positive
per query, BM25 reaches nDCG@10 = 0.6537 and hit@10 = 0.8100. It ranks 100
positives first and finds a positive in the top 100 for all queries.

BM25 is strong because IN-domain patent families often share the same technical
terms, and full-text targets contain many opportunities for term overlap.

### Training Data That May Help

Useful training data includes patent-family citation pairs restricted to shared
IPC/CPC classes, same-domain prior-art retrieval, and claim-aware patent search.
Training must exclude NanoDAPFAM evaluation families and positives.

### Synthetic Data Guidance

Generate same-domain patent families with title, abstract, claims, and full
descriptions. Hard negatives should share IPC-style terminology and components
but lack a citation-style prior-art relation.

## Example Data

| Query | Positive document |
| --- | --- |
| snow removal equipment with automatic walking function the invention relates to snow removal equipment with an automatic walking function. the snow removal equipment comprises a walking module, a working module and a control ... [truncated 225 chars](6075 chars) | multifunctional device for clearing snow an apparatus and method for clearing an accumulation of matter from a surface that includes a blade configured to collect matter upon movement of the apparatus and means to shift the c ... [truncated 225 chars](59310 chars) |
| apparatus for indication of at least one subsurface barrier characteristic and methods of use a containment system for use adjacent to a selected region of a subterranean formation and comprising a plurality of laterally inte ... [truncated 225 chars](11428 chars) | method of confirming position of drain material left and apparatus for confirming same in drain engineering method a method and apparatus is provided to embed paper drain material in water-laden soil by means of a mandrel dri ... [truncated 225 chars](23599 chars) |
| an article including identification for use in an electrically heated smoking system. there is provided an electrically heated smoking system (101) for receiving a smoking article (115) or cleaning article (205) configured fo ... [truncated 225 chars](5076 chars) | apparatus for generating aerosol from an aerosolisable medium, an article of aerosolisable medium and a method of determining a parameter of an article to provide an apparatus that heats an aerosolizable medium to volatilize ... [truncated 225 chars](52756 chars) |
| low weight carpet and carpet tile and methods of manufacture low weight and non-square carpet tile suitable for use in mass transit vehicles, particularly passenger aircraft. the carpet tile preferably weighs less than about ... [truncated 225 chars](3799 chars) | anti-static mats and carpets a novel carpet material or mat which is characterized by an extraordinary ability to quickly and comfortably discharge any build-up of a static electricity charge on a person who has built up such ... [truncated 225 chars](17195 chars) |
| organosilicon precursors for interlayer dielectric films with low dielectric constants a method of forming a low dielectric constant interlayer dielectric film on a substrate by reacting, under chemical vapor deposition condi ... [truncated 225 chars](11588 chars) | radiation shield a radiation shield and an assembly and a reactor including the radiation shield are disclosed. the radiation shield can be used to control heat flux from a susceptor heater assembly and thereby enable better ... [truncated 225 chars](48536 chars) |

## Dataset Information

| Field | Value |
| --- | --- |
| Nano set | NanoDAPFAM |
| Backing dataset | NanoDAPFAM |
| Task / split | NanoDAPFAMInTitlAbsClmToFullText |
| Hugging Face dataset | [hakari-bench/NanoDAPFAM](https://huggingface.co/datasets/hakari-bench/NanoDAPFAM) |
| Language | en |
| Category | natural_language |
| Queries | 200 |
| Documents | 10000 |
| Positive qrels | 3069 |
| Positives per query | avg 15.35, min 1, median 18.0, max 20 |
| BM25 nDCG@10 | 0.3505 |
| BM25 hit@10 | 0.8150 |
| BM25 Recall@100 | 0.5673 |
| BM25 candidate subset | top-500 (`bm25`) |
| Dense nDCG@10 | 0.4484 |
| Dense hit@10 | 0.8950 |
| Dense Recall@100 | 0.7025 |
| Dense candidate subset | top-500 (`harrier_oss_v1_270m`) |
| Reranking hybrid nDCG@10 | 0.4375 |
| Reranking hybrid hit@10 | 0.8850 |
| Reranking hybrid Recall@100 | 0.7032 |
| Reranking hybrid candidate subset | top-100 plus optional rank-101 safeguard (`reranking_hybrid`) |
| Reranking hybrid candidates / query | 100-101 |
| Reranking hybrid safeguard rows | 7 |
| Query length avg chars | 8405.48 |
| Document length avg chars | 68905.96 |

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
  task_name: NanoDAPFAMInTitlAbsClmToFullText
  split_name: NanoDAPFAMInTitlAbsClmToFullText
  language: en
  category: natural_language
  document_path: docs/benchmark_tasks/NanoDAPFAM/NanoDAPFAMInTitlAbsClmToFullText.md
  source_research:
    primary_source_type: benchmark_paper
    paper_pdf_or_html_checked: true
  counts:
    queries: 200
    documents: 10000
    positive_qrels: 3069
  positives_per_query:
    average: 15.345
    min: 1
    median: 18.0
    max: 20
    multi_positive_queries: 198
  text_stats_chars:
    query_mean: 8405.475
    document_mean: 68905.9642
  bm25:
    ndcg_at_10: 0.3504705323358214
    hit_at_10: 0.815
    source: dataset_candidate_subset
  learning:
    original_train_split: not_confirmed
    evaluation_split_origin: DAPFAM IN-domain title-abstract-claims to full-text patent-family
      retrieval
    train_eval_overlap_audit: not_audited
    leakage_note: exclude NanoDAPFAM evaluation families, positives, qrels, and same-family
      duplicates
    useful_training_data:
    - same-IPC patent citation retrieval
    - in-domain prior-art search
    - claim-aware patent-family retrieval
    synthetic_data:
      document_generation: same-domain patent full-text records with shared IPC-style
        terminology
      question_generation: title abstract and claims from a source patent family
      answerability: positives should be cited same-domain patent families
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
      ndcg_at_10: 0.3504705323
      hit_at_10: 0.815
      recall_at_100: 0.5672857608
      candidate_count_min: 500
      candidate_count_max: 500
      candidate_count_mean: 500.0
      query_count: 200
      query_coverage: 1.0
      relevant_coverage_at_100: 0.5672857608
    dense:
      config: harrier_oss_v1_270m
      label: Dense
      source: dataset_candidate_subset
      top_k: 500
      ndcg_at_10: 0.4483747423
      hit_at_10: 0.895
      recall_at_100: 0.7025089606
      candidate_count_min: 500
      candidate_count_max: 500
      candidate_count_mean: 500.0
      query_count: 200
      query_coverage: 1.0
      relevant_coverage_at_100: 0.7025089606
    reranking_hybrid:
      config: reranking_hybrid
      label: Reranking hybrid
      source: dataset_candidate_subset
      top_k: 100
      ndcg_at_10: 0.4374716828
      hit_at_10: 0.885
      recall_at_100: 0.7031606386
      candidate_count_min: 100
      candidate_count_max: 101
      candidate_count_mean: 100.035
      query_count: 200
      query_coverage: 1.0
      relevant_coverage_at_100: 0.7031606386
      safeguard_positive_rows: 7
      rows_with_101_candidates: 7
```
