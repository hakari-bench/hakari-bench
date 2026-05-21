# NanoMTEB-v2 / treccovid

## Overview

`treccovid` is a biomedical ad-hoc retrieval task from the TREC-COVID
challenge. Queries are COVID-19 information needs, and relevant documents are
scientific article records from the pandemic literature.

## Details

### What the Original Data Measures

[TREC-COVID](https://arxiv.org/abs/2005.04474) was created as an information
retrieval test collection over COVID-19 literature, coordinated by NIST with
rounds of topics and relevance judgments. The task evaluates retrieval of
scientific articles for biomedical questions about SARS-CoV-2, treatments,
risk factors, and clinical evidence. [MTEB](https://arxiv.org/abs/2210.07316)
includes TREC-COVID as an English retrieval task.

### Observed Data Profile

The split has 50 queries, 10,000 documents, and 4,584 positive qrels. Queries
average 69.24 characters and are direct biomedical information needs. Documents
average 1326.60 characters and typically contain titles plus abstracts. Every
query is highly multi-positive, with a median of 100 positives.

### BM25 Difficulty

Using the dataset-provided BM25 candidate column, BM25 reaches nDCG@10 =
0.9039 and hit@10 = 1.0000. It ranks 46 queries with a positive first, and the
median best positive rank is 1. Strong biomedical term overlap makes BM25 very
competitive in this Nano sample, though many relevant documents mean fine-grained
ranking still matters.

### Training Data That May Help

Useful data includes biomedical literature retrieval pairs, CORD-19 or
PubMed-style title-abstract search logs, TREC-COVID training topics, and hard
negatives that share disease or drug terms but address a different clinical
question.

### Synthetic Data Guidance

Generate biomedical information needs and title-abstract records with explicit
clinical concepts. Hard negatives should share COVID-19 terminology while
differing in population, intervention, outcome, or evidence type.

## Example Data

| Query | Positive document |
| --- | --- |
| what evidence is there for dexamethasone as a treatment for COVID-19? (69 chars) | The Combination of Tocilizumab and Methylprednisolone Along With Initial Lung Recruitment Strategy in Coronavirus Disease 2019 Patients Requiring Mechanical Ventilation: A Series of 21 Consecutive Cases OBJECTIVE: To describe ... [truncated 225 chars](1757 chars) |
| how long does coronavirus remain stable on surfaces? (53 chars) | Body fluids may contribute to human-to-human transmission of severe acute respiratory syndrome coronavirus 2: evidence and practical experience BACKGROUND: In December 2019, an unbelievable outbreak of pneumonia associated wi ... [truncated 225 chars](1172 chars) |
| has social distancing had an impact on slowing the spread of COVID-19? (70 chars) | Increased Detection coupled with Social Distancing and Health Capacity Planning Reduce the Burden of COVID-19 Cases and Fatalities: A Proof of Concept Study using a Stochastic Computational Simulation Model Objective: In abse ... [truncated 225 chars](1576 chars) |
| are there serological tests that detect antibodies to coronavirus? (66 chars) | A Guide to COVID‐19: a global pandemic caused by the novel coronavirus SARS‐CoV‐2 The emergence of the SARS‐CoV‐2 strain of the human coronavirus has thrown the world into the midst of a new pandemic. In the human body, the v ... [truncated 225 chars](1084 chars) |
| which biomarkers predict the severe clinical course of 2019-nCOV infection? (75 chars) | Clinical course and outcome of 107 patients infected with the novel coronavirus, SARS-CoV-2, discharged from two hospitals in Wuhan, China BACKGROUND: In December 2019, coronavirus disease 2019 (COVID-19) outbreak was reporte ... [truncated 225 chars](1932 chars) |

## Dataset Information

| Field | Value |
| --- | --- |
| Nano set | NanoMTEB-v2 |
| Backing dataset | NanoMTEB-v2 |
| Task / split | treccovid |
| Source task | TRECCOVID |
| Hugging Face dataset | [hakari-bench/NanoMTEB-v2](https://huggingface.co/datasets/hakari-bench/NanoMTEB-v2) |
| Source dataset | [mteb/trec-covid](https://huggingface.co/datasets/mteb/trec-covid) |
| Language | en |
| Category | natural_language |
| Queries | 50 |
| Documents | 10000 |
| Positive qrels | 4584 |
| Positives per query | avg 91.68, min 19, median 100, max 100 |
| Multi-positive queries | 50 (100.00%) |
| BM25 nDCG@10 | 0.9039 |
| BM25 hit@10 | 1.0000 |
| Query length avg chars | 69.24 |
| Document length avg chars | 1326.60 |

### Public Sources

- [TREC-COVID: Constructing a Pandemic Information Retrieval Test Collection](https://arxiv.org/abs/2005.04474).
- [NIST TREC-COVID challenge page](https://ir.nist.gov/covidSubmit/index.html).
- [MTEB: Massive Text Embedding Benchmark](https://arxiv.org/abs/2210.07316).
- [mteb/trec-covid](https://huggingface.co/datasets/mteb/trec-covid).

### Hugging Face Links

- Nano dataset: [hakari-bench/NanoMTEB-v2](https://huggingface.co/datasets/hakari-bench/NanoMTEB-v2)
- Source dataset: [mteb/trec-covid](https://huggingface.co/datasets/mteb/trec-covid)

### Source Reference Table

| Title | Year | Type | URL |
| --- | ---: | --- | --- |
| TREC-COVID: Constructing a Pandemic Information Retrieval Test Collection | 2020 | source task paper | https://arxiv.org/abs/2005.04474 |
| NIST TREC-COVID | 2020 | challenge page | https://ir.nist.gov/covidSubmit/index.html |
| MTEB: Massive Text Embedding Benchmark | 2023 | benchmark paper | https://arxiv.org/abs/2210.07316 |
| mteb/trec-covid | 2024 | dataset card | https://huggingface.co/datasets/mteb/trec-covid |

## Machine-Readable Metadata

<!-- benchmark-task-metadata:v1 -->

```yaml
benchmark_task_metadata:
  schema_version: 1
  document_status: first_pass
  nano_set: NanoMTEB-v2
  backing_dataset: NanoMTEB-v2
  dataset_id: hakari-bench/NanoMTEB-v2
  task_name: treccovid
  split_name: treccovid
  source_task: TRECCOVID
  source_dataset_id: mteb/trec-covid
  language: en
  category: natural_language
  document_path: docs/benchmark_tasks/NanoMTEB-v2/treccovid.md
  source_research:
    primary_source_type: task_paper_and_benchmark_paper
    paper_pdf_or_html_checked: true
    no_paper_note: null
  counts:
    queries: 50
    documents: 10000
    positive_qrels: 4584
  positives_per_query:
    average: 91.68
    min: 19
    median: 100.0
    max: 100
    multi_positive_queries: 50
    multi_positive_query_percent: 100.0
  text_stats_chars:
    query_mean: 69.24
    document_mean: 1326.6045
  bm25:
    ndcg_at_10: 0.9038626806840664
    hit_at_10: 1.0
    source: dataset_bm25_column
  learning:
    original_train_split: available
    evaluation_split_origin: MTEB TREC-COVID test split
    train_eval_overlap_audit: not_audited
    leakage_note: exclude NanoMTEB-v2 treccovid topics and judged articles
    useful_training_data:
      - biomedical literature retrieval data
      - CORD-19 and PubMed title-abstract retrieval pairs
      - TREC-COVID topics and qrels outside this Nano split
    synthetic_data:
      document_generation: biomedical article titles and abstracts
      question_generation: COVID-19 clinical or scientific information needs
      answerability: positive article should address the biomedical information need
    multi_positive_training: required
  links:
    nano_dataset: https://huggingface.co/datasets/hakari-bench/NanoMTEB-v2
    source_urls:
      - label: TREC-COVID paper
        url: https://arxiv.org/abs/2005.04474
      - label: NIST TREC-COVID
        url: https://ir.nist.gov/covidSubmit/index.html
      - label: MTEB arXiv
        url: https://arxiv.org/abs/2210.07316
      - label: mteb/trec-covid
        url: https://huggingface.co/datasets/mteb/trec-covid
    source_notes: []
  references:
    - title: "TREC-COVID: Constructing a Pandemic Information Retrieval Test Collection"
      url: https://arxiv.org/abs/2005.04474
      year: 2020
      is_paper: true
      source_confidence: definitive_paper_link
    - title: "MTEB: Massive Text Embedding Benchmark"
      url: https://arxiv.org/abs/2210.07316
      year: 2023
      is_paper: true
      source_confidence: definitive_paper_link
```
