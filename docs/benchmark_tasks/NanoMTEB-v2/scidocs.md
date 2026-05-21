# NanoMTEB-v2 / scidocs

## Overview

`scidocs` is a scientific-document retrieval task. Queries are paper titles,
and relevant documents are scientific papers that are related by citation or
recommendation-style relevance.

## Details

### What the Original Data Measures

[SCIDOCS](https://arxiv.org/abs/2004.07180) was introduced with SPECTER as a
benchmark for document-level scientific paper representations across citation,
classification, and recommendation tasks. The MTEB retrieval variant tests
whether a model can retrieve relevant paper abstracts from a scientific corpus.

### Observed Data Profile

The split has 200 queries, 10,000 documents, and 986 positive qrels. Queries
average 69.79 characters and look like paper titles. Documents average
1202.68 characters and usually include a title plus abstract. Every query is
multi-positive, with a median of 5 positives per query.

### BM25 Difficulty

Using the dataset-provided BM25 candidate column, BM25 reaches nDCG@10 =
0.1933 and hit@10 = 0.6050. It ranks 44 queries with a positive first, and the
median best positive rank is 5. The low nDCG indicates that lexical overlap
between related scientific papers is unreliable, especially when relevance is
based on citation context or research affinity rather than exact title terms.

### Training Data That May Help

Useful data includes citation-linked paper pairs, paper recommendation datasets,
title-to-abstract retrieval pairs, and hard negatives from the same venue,
topic, or method family.

### Synthetic Data Guidance

Generate paper titles and abstracts with realistic technical vocabulary. Build
positives around shared research problems or citation-worthy methods, and use
hard negatives from the same area that differ in task, dataset, or technique.

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
| Nano set | NanoMTEB-v2 |
| Backing dataset | NanoMTEB-v2 |
| Task / split | scidocs |
| Source task | SCIDOCS |
| Hugging Face dataset | [hakari-bench/NanoMTEB-v2](https://huggingface.co/datasets/hakari-bench/NanoMTEB-v2) |
| Source dataset | [mteb/scidocs](https://huggingface.co/datasets/mteb/scidocs) |
| Language | en |
| Category | natural_language |
| Queries | 200 |
| Documents | 10000 |
| Positive qrels | 986 |
| Positives per query | avg 4.93, min 3, median 5, max 5 |
| Multi-positive queries | 200 (100.00%) |
| BM25 nDCG@10 | 0.1933 |
| BM25 hit@10 | 0.6050 |
| Query length avg chars | 69.79 |
| Document length avg chars | 1202.68 |

### Public Sources

- [SPECTER: Document-level Representation Learning using Citation-informed Transformers](https://arxiv.org/abs/2004.07180).
- [MTEB: Massive Text Embedding Benchmark](https://arxiv.org/abs/2210.07316).
- [mteb/scidocs](https://huggingface.co/datasets/mteb/scidocs).

### Hugging Face Links

- Nano dataset: [hakari-bench/NanoMTEB-v2](https://huggingface.co/datasets/hakari-bench/NanoMTEB-v2)
- Source dataset: [mteb/scidocs](https://huggingface.co/datasets/mteb/scidocs)

### Source Reference Table

| Title | Year | Type | URL |
| --- | ---: | --- | --- |
| SPECTER: Document-level Representation Learning using Citation-informed Transformers | 2020 | source task paper | https://arxiv.org/abs/2004.07180 |
| MTEB: Massive Text Embedding Benchmark | 2023 | benchmark paper | https://arxiv.org/abs/2210.07316 |
| mteb/scidocs | 2024 | dataset card | https://huggingface.co/datasets/mteb/scidocs |

## Machine-Readable Metadata

<!-- benchmark-task-metadata:v1 -->

```yaml
benchmark_task_metadata:
  schema_version: 1
  document_status: first_pass
  nano_set: NanoMTEB-v2
  backing_dataset: NanoMTEB-v2
  dataset_id: hakari-bench/NanoMTEB-v2
  task_name: scidocs
  split_name: scidocs
  source_task: SCIDOCS
  source_dataset_id: mteb/scidocs
  language: en
  category: natural_language
  document_path: docs/benchmark_tasks/NanoMTEB-v2/scidocs.md
  source_research:
    primary_source_type: task_paper_and_benchmark_paper
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
    ndcg_at_10: 0.19329407857667313
    hit_at_10: 0.605
    source: dataset_bm25_column
  learning:
    original_train_split: available
    evaluation_split_origin: MTEB SCIDOCS test split
    train_eval_overlap_audit: not_audited
    leakage_note: exclude NanoMTEB-v2 scidocs paper pairs
    useful_training_data:
      - citation-linked paper pairs
      - scientific paper recommendation data
      - title-to-abstract retrieval pairs
    synthetic_data:
      document_generation: paper titles plus scientific abstracts
      question_generation: scientific paper titles used as retrieval queries
      answerability: positive should be a scientifically related paper
    multi_positive_training: recommended
  links:
    nano_dataset: https://huggingface.co/datasets/hakari-bench/NanoMTEB-v2
    source_urls:
      - label: SPECTER and SCIDOCS arXiv
        url: https://arxiv.org/abs/2004.07180
      - label: MTEB arXiv
        url: https://arxiv.org/abs/2210.07316
      - label: mteb/scidocs
        url: https://huggingface.co/datasets/mteb/scidocs
    source_notes: []
  references:
    - title: "SPECTER: Document-level Representation Learning using Citation-informed Transformers"
      url: https://arxiv.org/abs/2004.07180
      year: 2020
      is_paper: true
      source_confidence: definitive_paper_link
    - title: "MTEB: Massive Text Embedding Benchmark"
      url: https://arxiv.org/abs/2210.07316
      year: 2023
      is_paper: true
      source_confidence: definitive_paper_link
```
