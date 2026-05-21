# NanoMMTEB-v2 / scidocs

## Overview

`scidocs` is an English scientific-document retrieval task. Queries are paper
titles, and documents are paper title/abstract records. The retriever must find
scientifically related papers, often via citation-like topical relatedness rather
than direct keyword match.

## Details

### What the Original Data Measures

[SPECTER: Document-level Representation Learning using Citation-informed Transformers](https://arxiv.org/abs/2004.07180)
introduces SCIDOCS as a suite of scientific document-level evaluation tasks. The
BEIR paper treats SCIDOCS as a citation-prediction retrieval task, where a query
paper should retrieve related scientific papers from a held-out corpus.

### Observed Data Profile

The split has 200 queries, 10,000 documents, and 986 positive qrels. Queries
average 69.79 characters and documents average 1,202.68 characters. Each query
has three to five positive papers, with an average of 4.93 positives. Observed
documents are title plus abstract text across computer science and related
technical areas.

### BM25 Difficulty

Using the dataset-provided BM25 candidate column, BM25 reaches nDCG@10 = 0.1933
and hit@10 = 0.6050. Exact scientific terms help, but true relatedness can be
based on citation, method, or application similarity, so lexical overlap alone
often misses relevant papers.

### Training Data That May Help

Useful training data includes citation-linked paper pairs, title/abstract
similarity data, co-citation pairs, SPECTER-style triplets, and hard negatives
from the same venue or topic. Exclude SCIDOCS evaluation query papers and
positive documents when training.

### Synthetic Data Guidance

Generate title/abstract records and queries that describe related work,
follow-up methods, or shared applications. Synthetic positives should be related
by method, cited background, or task; negatives should share keywords while
belonging to a different research line.

## Example Data

| Query | Positive document |
| --- | --- |
| An integrated framework on mining logs files for computing system management (76 chars) | Machine learning in automated text categorization The automated categorization (or classification) of texts into predefined categories has witnessed a booming interest in the last 10 years, due to the increased availability o ... [truncated 225 chars](1103 chars) |
| Topic-Relevance Map: Visualization for Improving Search Result Comprehension (76 chars) | Designing for Exploratory Search on Touch Devices Exploratory search confront users with challenges in expressing search intents as the current search interfaces require investigating result listings to identify search direct ... [truncated 225 chars](1194 chars) |
| Algorithmic Nuggets in Content Delivery (39 chars) | Consistent Hashing and Random Trees: Distributed Caching Protocols for Relieving Hot Spots on the World Wide Web We describe a family of caching protocols for distrib-uted networks that can be used to decrease or eliminate th ... [truncated 225 chars](1323 chars) |
| The Enactive Approach to Architectural Experience: A Neurophysiological Perspective on Embodiment, Motivation, and Affordances (126 chars) | Affective outcomes of virtual reality exposure therapy for anxiety and specific phobias: a meta-analysis. Virtual reality exposure therapy (VRET) is an increasingly common treatment for anxiety and specific phobias. Lacking i ... [truncated 225 chars](836 chars) |
| PD control with on-line gravity compensation for robots with elastic joints: Theory and experiments (99 chars) | A passivity based Cartesian impedance controller for flexible joint robots - part I: torque feedback and gravity compensation In this paper a novel approach to the Cartesian impedance control problem for robots with flexible ... [truncated 225 chars](780 chars) |

## Dataset Information

| Field | Value |
| --- | --- |
| Nano set | NanoMMTEB-v2 |
| Backing dataset | NanoMMTEB-v2 |
| Task / split | scidocs |
| Hugging Face dataset | [hakari-bench/NanoMMTEB-v2](https://huggingface.co/datasets/hakari-bench/NanoMMTEB-v2) |
| Source dataset | [mteb/scidocs](https://huggingface.co/datasets/mteb/scidocs) |
| Language | en |
| Category | natural_language |
| Queries | 200 |
| Documents | 10000 |
| Positive qrels | 986 |
| Avg positives / query | 4.93 |
| Positives per query (min / median / max) | 3 / 5.0 / 5 |
| Queries with multiple positives | 200 (100.00%) |
| BM25 nDCG@10 | 0.1933 |
| BM25 hit@10 | 0.6050 |
| Query length avg chars | 69.79 |
| Document length avg chars | 1202.68 |

### Public Sources

- [SPECTER: Document-level Representation Learning using Citation-informed Transformers](https://arxiv.org/abs/2004.07180).
- [SCIDOCS project page](https://allenai.org/data/scidocs).
- [mteb/scidocs](https://huggingface.co/datasets/mteb/scidocs).

### Hugging Face Links

- Nano dataset: [hakari-bench/NanoMMTEB-v2](https://huggingface.co/datasets/hakari-bench/NanoMMTEB-v2)
- Source dataset: [mteb/scidocs](https://huggingface.co/datasets/mteb/scidocs)

### Source Reference Table

| Title | Year | Type | URL |
| --- | ---: | --- | --- |
| SPECTER: Document-level Representation Learning using Citation-informed Transformers | 2020 | task paper | https://arxiv.org/abs/2004.07180 |
| SCIDOCS project page | 2020 | project page | https://allenai.org/data/scidocs |
| mteb/scidocs | 2024 | dataset card | https://huggingface.co/datasets/mteb/scidocs |

## Machine-Readable Metadata

<!-- benchmark-task-metadata:v1 -->

```yaml
benchmark_task_metadata:
  schema_version: 1
  document_status: first_pass
  nano_set: NanoMMTEB-v2
  backing_dataset: NanoMMTEB-v2
  dataset_id: hakari-bench/NanoMMTEB-v2
  task_name: scidocs
  split_name: scidocs
  language: en
  category: natural_language
  document_path: docs/benchmark_tasks/NanoMMTEB-v2/scidocs.md
  source_research:
    primary_source_type: task_paper
    paper_pdf_or_html_checked: true
    no_paper_note: null
  counts:
    queries: 200
    documents: 10000
    positive_qrels: 986
  positives_per_query:
    average: 4.93
    min: 3
    median: 5.0
    max: 5
    multi_positive_queries: 200
    multi_positive_query_percent: 100.0
  text_stats_chars:
    query_mean: 69.79
    document_mean: 1202.6798
  bm25:
    ndcg_at_10: 0.19326143403163346
    hit_at_10: 0.605
    source: dataset_bm25_column
  learning:
    original_train_split: available
    evaluation_split_origin: test
    train_eval_overlap_audit: not_audited
    leakage_note: do not train on this Nano split's SCIDOCS query papers, qrels, or positive records
    useful_training_data:
      - citation-linked paper pairs
      - title and abstract similarity data
      - co-citation and bibliography graph pairs
      - SPECTER-style scientific paper triplets
    synthetic_data:
      document_generation: scientific title and abstract records with methods, tasks, and claims
      question_generation: paper titles or short related-work search needs
      answerability: positives should be scientifically related by citation, method, task, or application
    multi_positive_training: multi_positive_objective
  links:
    nano_dataset: https://huggingface.co/datasets/hakari-bench/NanoMMTEB-v2
    source_urls:
      - label: SPECTER arXiv
        url: https://arxiv.org/abs/2004.07180
      - label: SCIDOCS project page
        url: https://allenai.org/data/scidocs
      - label: mteb/scidocs
        url: https://huggingface.co/datasets/mteb/scidocs
    source_notes: []
  references:
    - title: "SPECTER: Document-level Representation Learning using Citation-informed Transformers"
      url: https://arxiv.org/abs/2004.07180
      year: 2020
      is_paper: true
      source_confidence: definitive_paper_link
```
