# NanoDAPFAM / NanoDAPFAMInTitlAbsToTitlAbsClm

## Overview

`NanoDAPFAMInTitlAbsToTitlAbsClm` retrieves title-abstract-claims patent-family
records from title-abstract queries. It is an IN-domain DAPFAM split where
positive citation targets share at least one IPC3 class with the query family.

## Details

### What the Original Data Measures

[DAPFAM: A Domain-Aware Family-level Dataset to benchmark cross domain patent retrieval](https://arxiv.org/abs/2506.22141)
compares patent retrieval representations and domain partitions. This split
tests whether a compact same-domain patent summary can retrieve a target family
represented by title, abstract, and claims.

### Observed Data Profile

The Nano split has 200 queries, 10,000 documents, and 3,072 positive qrels.
Queries average 771.33 characters, target documents average 7,226.37
characters, and positives per query average 15.36.

The target claims add technical detail and exact component language beyond the
abstract. Because positives are same-domain, many relevant records share
vocabulary but differ in claim scope.

### BM25 Difficulty

Using the dataset-provided BM25 candidate column and best-ranked positive per
query, BM25 reaches nDCG@10 = 0.6549 and hit@10 = 0.8300. It ranks 97 positives
first and finds a positive in the top 100 for every query.

BM25 benefits from same-domain terms and target-side claims, but some positives
still rank below the top 10 because short queries can under-specify detailed
claim relationships.

### Training Data That May Help

Useful training data includes same-domain patent summary-to-claim retrieval,
citation prediction between patent families, and IPC-restricted prior-art search
pairs outside the evaluation set.

### Synthetic Data Guidance

Generate short source summaries and claim-rich same-domain targets. Include
hard negatives with matching IPC-style terminology and overlapping components
but no cited relation.

## Example Data

| Query | Positive document |
| --- | --- |
| snow removal equipment with automatic walking function the invention relates to snow removal equipment with an automatic walking function. the snow removal equipment comprises a walking module, a working module and a control ... [truncated 225 chars](988 chars) | multifunctional device for clearing snow an apparatus and method for clearing an accumulation of matter from a surface that includes a blade configured to collect matter upon movement of the apparatus and means to shift the c ... [truncated 225 chars](12229 chars) |
| waste disposal devices waste disposal device including a housing defining a waste compartment for receiving enclosed waste and arranged to removably receive a cartridge containing a length of flexible tubing which operatively ... [truncated 225 chars](891 chars) | cassette for dispensing pleated tubing a cassette for use in dispensing a pleated tubing. the cassette includes an annular body having a generally u shaped housing with an open central cylindrical core. the annular body inclu ... [truncated 225 chars](3454 chars) |
| an article including identification for use in an electrically heated smoking system. there is provided an electrically heated smoking system (101) for receiving a smoking article (115) or cleaning article (205) configured fo ... [truncated 225 chars](1164 chars) | apparatus for generating aerosol from an aerosolisable medium, an article of aerosolisable medium and a method of determining a parameter of an article to provide an apparatus that heats an aerosolizable medium to volatilize ... [truncated 225 chars](5466 chars) |
| low weight carpet and carpet tile and methods of manufacture low weight and non-square carpet tile suitable for use in mass transit vehicles, particularly passenger aircraft. the carpet tile preferably weighs less than about ... [truncated 225 chars](565 chars) | anti-static mats and carpets a novel carpet material or mat which is characterized by an extraordinary ability to quickly and comfortably discharge any build-up of a static electricity charge on a person who has built up such ... [truncated 225 chars](3680 chars) |
| organosilicon precursors for interlayer dielectric films with low dielectric constants a method of forming a low dielectric constant interlayer dielectric film on a substrate by reacting, under chemical vapor deposition condi ... [truncated 225 chars](546 chars) | radiation shield a radiation shield and an assembly and a reactor including the radiation shield are disclosed. the radiation shield can be used to control heat flux from a susceptor heater assembly and thereby enable better ... [truncated 225 chars](4267 chars) |

## Dataset Information

| Field | Value |
| --- | --- |
| Nano set | NanoDAPFAM |
| Backing dataset | NanoDAPFAM |
| Task / split | NanoDAPFAMInTitlAbsToTitlAbsClm |
| Hugging Face dataset | [hakari-bench/NanoDAPFAM](https://huggingface.co/datasets/hakari-bench/NanoDAPFAM) |
| Language | en |
| Category | natural_language |
| Queries | 200 |
| Documents | 10000 |
| Positive qrels | 3072 |
| Positives per query | avg 15.36, min 1, median 18.0, max 20 |
| BM25 nDCG@10 | 0.6549 |
| BM25 hit@10 | 0.8300 |
| Query length avg chars | 771.33 |
| Document length avg chars | 7226.37 |

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
  task_name: NanoDAPFAMInTitlAbsToTitlAbsClm
  split_name: NanoDAPFAMInTitlAbsToTitlAbsClm
  language: en
  category: natural_language
  document_path: docs/benchmark_tasks/NanoDAPFAM/NanoDAPFAMInTitlAbsToTitlAbsClm.md
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
    document_mean: 7226.3717
  bm25:
    ndcg_at_10: 0.6549425465
    hit_at_10: 0.83
    source: dataset_bm25_column
  learning:
    original_train_split: not_confirmed
    evaluation_split_origin: DAPFAM IN-domain title-abstract to title-abstract-claims patent-family retrieval
    train_eval_overlap_audit: not_audited
    leakage_note: exclude NanoDAPFAM evaluation families, positives, qrels, and same-family duplicates
    useful_training_data:
      - same-domain title-abstract to patent-claims retrieval
      - IPC-restricted citation prediction
      - prior-art search with claim-rich targets
    synthetic_data:
      document_generation: same-domain target patent records with title abstract and claims
      question_generation: compact source title and abstract summaries
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
    - title: "DAPFAM: A Domain-Aware Family-level Dataset to benchmark cross domain patent retrieval"
      url: https://arxiv.org/abs/2506.22141
      year: 2026
      doi: 10.1016/j.array.2026.100720
      is_paper: true
      source_confidence: definitive_paper_link
```
