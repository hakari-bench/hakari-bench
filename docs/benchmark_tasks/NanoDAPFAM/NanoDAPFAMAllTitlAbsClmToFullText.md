# NanoDAPFAM / NanoDAPFAMAllTitlAbsClmToFullText

## Overview

`NanoDAPFAMAllTitlAbsClmToFullText` is an English patent-family retrieval task.
The query is a patent-family title, abstract, and claims text, and the target is
the full text representation of another patent family. Relevance comes from
DAPFAM citation links across all domain relations, without filtering to only
shared or non-shared IPC3 technical classes.

## Details

### What the Original Data Measures

[DAPFAM: A Domain-Aware Family-level Dataset to benchmark cross domain patent retrieval](https://arxiv.org/abs/2506.22141)
introduces a family-level prior-art retrieval benchmark built from Lens.org
patent families. The paper aggregates patents at family level, extracts title,
abstract, claims, descriptions, dates, IPC codes, and citations, and uses
citation links as relevance judgments. It also defines IN-domain and OUT-domain
relations by whether query and target families share at least one IPC code at
the first-three-character level.

This split uses the DAPFAM "ALL" condition: relevant targets may be in the same
IPC3 area or outside it. Because both the query and target include claims or
full text, the task stresses long patent language, repeated legal phrasing, and
technical paraphrases rather than short keyword search alone.

### Observed Data Profile

The Nano split has 200 queries, 10,000 candidate documents, and 3,989 positive
qrels. Every query is multi-positive, with an average of 19.95 positives per
query. Queries average 8,339.47 characters because they include claims; target
documents average 71,050.59 characters because they include full patent text.

Observed examples include machinery-condition monitoring, soil remediation,
food-processing sterilization, and other technical families. The text is
lowercase, patent-like, and often contains long enumerated claim lists.

### BM25 Difficulty

Using the dataset-provided BM25 candidate column and the best-ranked positive
for each query, BM25 reaches nDCG@10 = 0.6536 and hit@10 = 0.8100. It ranks 101
positives first and places at least one positive in the top 100 for every query.

Lexical retrieval is strong in this ALL split because titles, abstracts, claims,
and full descriptions provide many overlapping technical terms. The remaining
difficulty is ranking the most relevant family among many long documents with
similar claim vocabulary.

### Training Data That May Help

Helpful non-evaluation training data would include patent-family citation
retrieval, prior-art search pairs, and patent semantic search data with title,
abstract, claim, and description fields. Training should exclude NanoDAPFAM
evaluation query families, positive target families, qrels, and near-duplicate
family members.

### Synthetic Data Guidance

Synthetic data should generate patent-family records with titles, abstracts,
claims, and descriptions, then create citation-style query-positive pairs.
Useful negatives include same-IPC3 families with overlapping terminology and
different-IPC3 families that share surface terms but solve different technical
problems.

## Example Data

| Query | Positive document |
| --- | --- |
| snow removal equipment with automatic walking function the invention relates to snow removal equipment with an automatic walking function. the snow removal equipment comprises a walking module, a working module and a control ... [truncated 225 chars](6075 chars) | multifunctional device for clearing snow an apparatus and method for clearing an accumulation of matter from a surface that includes a blade configured to collect matter upon movement of the apparatus and means to shift the c ... [truncated 225 chars](59310 chars) |
| modular intelligent transportation system a modular intelligent transportation system, comprising an environmentally protected enclosure, a system communications bus, a processor module, communicating with said bus, having a ... [truncated 225 chars](7061 chars) | impact media sharing an example operation includes one or more of associating a transport with an impact in proximity to one or more other transports, transmitting, by a device in proximity to the impact, media related to the ... [truncated 225 chars](110067 chars) |
| synthetic hollow microspheres this invention relates to a method of forming a synthetic hollow microsphere comprising the steps of preparing an agglomerate precursor, said agglomerate precursor including a primary component a ... [truncated 225 chars](8392 chars) | process for preparing metal-coated hollow microspheres a process for preparing a metal-coated hollow microsphere comprising the combination of steps of: (a) vigorously admixing a major quantity of hollow cenospheres/microsphe ... [truncated 225 chars](19034 chars) |
| low weight carpet and carpet tile and methods of manufacture low weight and non-square carpet tile suitable for use in mass transit vehicles, particularly passenger aircraft. the carpet tile preferably weighs less than about ... [truncated 225 chars](3799 chars) | anti-static mats and carpets a novel carpet material or mat which is characterized by an extraordinary ability to quickly and comfortably discharge any build-up of a static electricity charge on a person who has built up such ... [truncated 225 chars](17195 chars) |
| steering system with lane keeping integration a system for steering a vehicle including: an actuator disposed in a vehicle to apply torque to a steerable wheel; a driver input device receptive to driver commands for directing ... [truncated 225 chars](5360 chars) | steer torque manager for an advanced driver assistance system of a road vehicle a steer torque manager for an advanced driver assistance system of a road vehicle and a method therefor. a driver-in-the-loop functionality deter ... [truncated 225 chars](44337 chars) |

## Dataset Information

| Field | Value |
| --- | --- |
| Nano set | NanoDAPFAM |
| Backing dataset | NanoDAPFAM |
| Task / split | NanoDAPFAMAllTitlAbsClmToFullText |
| Hugging Face dataset | [hakari-bench/NanoDAPFAM](https://huggingface.co/datasets/hakari-bench/NanoDAPFAM) |
| Language | en |
| Category | natural_language |
| Queries | 200 |
| Documents | 10000 |
| Positive qrels | 3989 |
| Positives per query | avg 19.95, min 9, median 20.0, max 20 |
| BM25 nDCG@10 | 0.6536 |
| BM25 hit@10 | 0.8100 |
| Query length avg chars | 8339.47 |
| Document length avg chars | 71050.59 |

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
  task_name: NanoDAPFAMAllTitlAbsClmToFullText
  split_name: NanoDAPFAMAllTitlAbsClmToFullText
  language: en
  category: natural_language
  document_path: docs/benchmark_tasks/NanoDAPFAM/NanoDAPFAMAllTitlAbsClmToFullText.md
  source_research:
    primary_source_type: benchmark_paper
    paper_pdf_or_html_checked: true
    no_paper_note: DAPFAM is the source paper for this patent-family retrieval benchmark
  counts:
    queries: 200
    documents: 10000
    positive_qrels: 3989
  positives_per_query:
    average: 19.945
    min: 9
    median: 20.0
    max: 20
    multi_positive_queries: 200
  text_stats_chars:
    query_mean: 8339.47
    document_mean: 71050.5946
  bm25:
    ndcg_at_10: 0.6536271218
    hit_at_10: 0.81
    source: dataset_bm25_column
  learning:
    original_train_split: not_confirmed
    evaluation_split_origin: DAPFAM ALL title-abstract-claims to full-text patent-family retrieval
    train_eval_overlap_audit: not_audited
    leakage_note: exclude NanoDAPFAM evaluation query families, positive target families, qrels, and near-duplicate patent family members
    useful_training_data:
      - patent-family citation retrieval
      - prior-art search pairs with title abstract claims and descriptions
      - patent semantic search data outside the Nano evaluation families
    synthetic_data:
      document_generation: patent-family titles abstracts claims and descriptions with citation-style related families
      question_generation: use source patent title abstract and claims as the retrieval query
      answerability: positive documents should be cited or technically related patent families
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
    source_notes: []
  references:
    - title: "DAPFAM: A Domain-Aware Family-level Dataset to benchmark cross domain patent retrieval"
      url: https://arxiv.org/abs/2506.22141
      year: 2026
      doi: 10.1016/j.array.2026.100720
      is_paper: true
      source_confidence: definitive_paper_link
```
