# NanoDAPFAM / NanoDAPFAMOutTitlAbsClmToFullText

## Overview

`NanoDAPFAMOutTitlAbsClmToFullText` is an OUT-domain patent-family retrieval
task. Queries contain title, abstract, and claims, targets contain full patent
text, and positives are citation relations where query and target families do
not share an IPC3 technical class.

## Details

### What the Original Data Measures

[DAPFAM: A Domain-Aware Family-level Dataset to benchmark cross domain patent retrieval](https://arxiv.org/abs/2506.22141)
states that OUT-domain patent retrieval is substantially harder than IN-domain
retrieval because cited prior art may come from a different technical area. This
split tests that condition with the richest query and target representations.

### Observed Data Profile

The Nano split has 200 queries, 10,000 documents, and 1,259 positive qrels.
Queries average 9,315.69 characters because they include claims, and full-text
targets average 71,902.31 characters. Positives per query average 6.29, with a
median of 4.0.

Observed examples include an extreme ultraviolet light source retrieving lithium
sputtering prior art, and vehicle lighting retrieving antireflective glass
coating. These pairs show the cross-domain nature of the task.

### BM25 Difficulty

Using the dataset-provided BM25 candidate column and the best-ranked positive
per query, BM25 reaches nDCG@10 = 0.0980 and hit@10 = 0.1850. It ranks only 7
positives first, though a positive is still present in the top 100 for every
query.

This is much harder than the ALL and IN variants because surface terminology is
less reliable across IPC3 boundaries. A good model needs cross-domain technical
analogy, not just exact patent vocabulary.

### Training Data That May Help

Helpful training data includes cross-domain patent citation retrieval, prior-art
search where source and target IPC/CPC classes differ, and technology-transfer
or analogy retrieval data. Exclude NanoDAPFAM evaluation families and qrels.

### Synthetic Data Guidance

Generate cross-domain patent pairs where the source and target solve related
technical problems with different vocabulary. Hard negatives should be lexical
matches within the source domain, while positives should require recognizing a
shared mechanism or material across domains.

## Example Data

| Query | Positive document |
| --- | --- |
| bicycle handlebar grip a bicycle handlebar grip contains a plastic inner shell having a tubular shape and an outer surface; a fiber layer having an inner surface and an outer surface and includes a plurality of fibers interwe ... [truncated 225 chars](2588 chars) | durable flexible membrane and method of making same a flexible membrane having a valuable combination of desirable properties is composed of a generally heavy, dense supporting and reinforcing reticulated base fabric constitu ... [truncated 225 chars](28042 chars) |
| method for improving belt press dewatering a method for increasing the removal of a higher fraction of liquid from the press cake in any belt press is described. specifically, the invention incorporates a series of rollers th ... [truncated 225 chars](4605 chars) | artificial human anti-factor b antibody problem to be solved: to provide novel engineered forms of a monoclonal antibody and antigen-binding fragments thereof that bind complement protein factor b and selectively inhibit the ... [truncated 225 chars](108109 chars) |
| stitch distribution control system for tufting machines a stitch distribution control system for a tufting machine for controlling placement of yarns being fed to the needles of the tufting machine by yarn feed mechanisms to ... [truncated 225 chars](5968 chars) | method and apparatus for measuring direction or position of weft yarn of fabric the measurement of the pick or stitches course position in continuously moved fabrics involves examining at least one gap-shaped segment in a top ... [truncated 225 chars](24253 chars) |
| low weight carpet and carpet tile and methods of manufacture low weight and non-square carpet tile suitable for use in mass transit vehicles, particularly passenger aircraft. the carpet tile preferably weighs less than about ... [truncated 225 chars](3799 chars) | modular floor covering units with built-in lighting an apparatus for guiding the occupants of a structure along a path of travel within the structure is provided. the apparatus is comprised of modular floor covering units whi ... [truncated 225 chars](35319 chars) |
| method and apparatus for the zonal transmission of data using building lighting fixtures this invention relates to the zonal transmission of data by the modulation of the light output of arc lamps (150) or discharge lamps; li ... [truncated 225 chars](7344 chars) | shelf tag with ambient light detector the present invention relates to an electronic shelf display device which includes an optical device and an ambient light detector circuitry. the electronic shelf display device includes ... [truncated 225 chars](54320 chars) |

## Dataset Information

| Field | Value |
| --- | --- |
| Nano set | NanoDAPFAM |
| Backing dataset | NanoDAPFAM |
| Task / split | NanoDAPFAMOutTitlAbsClmToFullText |
| Hugging Face dataset | [hakari-bench/NanoDAPFAM](https://huggingface.co/datasets/hakari-bench/NanoDAPFAM) |
| Language | en |
| Category | natural_language |
| Queries | 200 |
| Documents | 10000 |
| Positive qrels | 1259 |
| Positives per query | avg 6.29, min 1, median 4.0, max 20 |
| BM25 nDCG@10 | 0.0980 |
| BM25 hit@10 | 0.1850 |
| Query length avg chars | 9315.69 |
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
  task_name: NanoDAPFAMOutTitlAbsClmToFullText
  split_name: NanoDAPFAMOutTitlAbsClmToFullText
  language: en
  category: natural_language
  document_path: docs/benchmark_tasks/NanoDAPFAM/NanoDAPFAMOutTitlAbsClmToFullText.md
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
    document_mean: 71902.3141
  bm25:
    ndcg_at_10: 0.0980166244
    hit_at_10: 0.185
    source: dataset_bm25_column
  learning:
    original_train_split: not_confirmed
    evaluation_split_origin: DAPFAM OUT-domain title-abstract-claims to full-text patent-family retrieval
    train_eval_overlap_audit: not_audited
    leakage_note: exclude NanoDAPFAM evaluation families, positives, qrels, and family duplicates
    useful_training_data:
      - cross-domain patent citation retrieval
      - prior-art search across different IPC classes
      - technology analogy retrieval over patents
    synthetic_data:
      document_generation: full-text patent records in different technical classes with related mechanisms
      question_generation: title abstract and claims from source patent families
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
    - title: "DAPFAM: A Domain-Aware Family-level Dataset to benchmark cross domain patent retrieval"
      url: https://arxiv.org/abs/2506.22141
      year: 2026
      doi: 10.1016/j.array.2026.100720
      is_paper: true
      source_confidence: definitive_paper_link
```
