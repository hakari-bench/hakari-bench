# NanoMMTEB-v2 / treccovid

## Overview

`treccovid` is an English biomedical ad-hoc retrieval task from the TREC-COVID
challenge. Queries are COVID-19 information needs, and documents are scientific
article titles and abstracts from pandemic literature. The retriever must find
articles relevant to the biomedical question.

## Details

### What the Original Data Measures

[TREC-COVID: Constructing a Pandemic Information Retrieval Test Collection](https://arxiv.org/abs/2005.04474)
describes a rapidly built IR collection over CORD-19 literature, with evolving
topics, pooled relevance judgments, and clinical or biomedical assessors. The
task captures pandemic search needs where literature and terminology changed
quickly.

### Observed Data Profile

The split has 50 queries, 10,000 documents, and 4,527 positive qrels. Every
query is highly multi-positive, with an average of 90.54 positives and a median
of 100. Queries average 69.24 characters. Documents average 1,321.57 characters
and typically contain titles plus abstracts.

### BM25 Difficulty

Using the dataset-provided BM25 candidate column, BM25 reaches nDCG@10 = 0.8979
and hit@10 = 1.0000. Biomedical terms, disease names, and exact topic wording
make lexical retrieval very strong, but ranking among many relevant scientific
articles still rewards evidence specificity.

### Training Data That May Help

Useful data includes biomedical literature retrieval, CORD-19 or PubMed
title-abstract search, TREC-style judged topics outside the evaluation split,
and hard negatives sharing disease or drug terms but addressing different
clinical questions.

### Synthetic Data Guidance

Generate biomedical titles and abstracts with explicit population,
intervention, outcome, organism, and evidence-type details. Questions should ask
for COVID-19 evidence needs. Hard negatives should share SARS-CoV-2 terminology
but differ in the clinical or mechanistic focus.

## Example Data

| Query | Positive document |
| --- | --- |
| what evidence is there for dexamethasone as a treatment for COVID-19? (69 chars) | Targeting inflammation and cytokine storm in COVID-19 (53 chars) |
| how long does coronavirus remain stable on surfaces? (53 chars) | Body fluids may contribute to human-to-human transmission of severe acute respiratory syndrome coronavirus 2: evidence and practical experience BACKGROUND: In December 2019, an unbelievable outbreak of pneumonia associated wi ... [truncated 225 chars](1172 chars) |
| has social distancing had an impact on slowing the spread of COVID-19? (70 chars) | A first study on the impact of current and future control measures on the spread of COVID-19 in Germany The novel coronavirus (SARS-CoV-2), identified in China at the end of December 2019 and causing the disease COVID-19, has ... [truncated 225 chars](948 chars) |
| are there serological tests that detect antibodies to coronavirus? (66 chars) | Serodiagnostics for Severe Acute Respiratory Syndrome-Related Coronavirus-2: A Narrative Review Accurate serologic tests to detect host antibodies to severe acute respiratory syndrome-related coronavirus-2 (SARS-CoV-2) will b ... [truncated 225 chars](1429 chars) |
| which biomarkers predict the severe clinical course of 2019-nCOV infection? (75 chars) | Clinical Features and Predictors for Patients with Severe SARS-CoV-2 Pneumonia: a retrospective multicenter cohort study Objectives: This study was performed to investigate clinical features of patients with severe SARS-CoV-2 ... [truncated 225 chars](1518 chars) |

## Dataset Information

| Field | Value |
| --- | --- |
| Nano set | NanoMMTEB-v2 |
| Backing dataset | NanoMMTEB-v2 |
| Task / split | treccovid |
| Hugging Face dataset | [hakari-bench/NanoMMTEB-v2](https://huggingface.co/datasets/hakari-bench/NanoMMTEB-v2) |
| Source dataset | [mteb/trec-covid](https://huggingface.co/datasets/mteb/trec-covid) |
| Language | en |
| Category | natural_language |
| Queries | 50 |
| Documents | 10000 |
| Positive qrels | 4527 |
| Avg positives / query | 90.54 |
| Positives per query (min / median / max) | 22 / 100.0 / 100 |
| Queries with multiple positives | 50 (100.00%) |
| BM25 nDCG@10 | 0.3627 |
| BM25 hit@10 | 0.9200 |
| BM25 Recall@100 | 0.2319 |
| BM25 candidate subset | top-500 (`bm25`) |
| Dense nDCG@10 | 0.4266 |
| Dense hit@10 | 0.9400 |
| Dense Recall@100 | 0.2576 |
| Dense candidate subset | top-500 (`harrier_oss_v1_270m`) |
| Reranking hybrid nDCG@10 | 0.4505 |
| Reranking hybrid hit@10 | 0.9800 |
| Reranking hybrid Recall@100 | 0.2761 |
| Reranking hybrid candidate subset | top-100 plus optional rank-101 safeguard (`reranking_hybrid`) |
| Reranking hybrid candidates / query | 100 |
| Reranking hybrid safeguard rows | 0 |
| Query length avg chars | 69.24 |
| Document length avg chars | 1321.57 |

### Public Sources

- [TREC-COVID: Constructing a Pandemic Information Retrieval Test Collection](https://arxiv.org/abs/2005.04474).
- [NIST TREC-COVID challenge page](https://ir.nist.gov/covidSubmit/index.html).
- [mteb/trec-covid](https://huggingface.co/datasets/mteb/trec-covid).

### Hugging Face Links

- Nano dataset: [hakari-bench/NanoMMTEB-v2](https://huggingface.co/datasets/hakari-bench/NanoMMTEB-v2)
- Source dataset: [mteb/trec-covid](https://huggingface.co/datasets/mteb/trec-covid)

### Source Reference Table

| Title | Year | Type | URL |
| --- | ---: | --- | --- |
| TREC-COVID: Constructing a Pandemic Information Retrieval Test Collection | 2020 | task paper | https://arxiv.org/abs/2005.04474 |
| NIST TREC-COVID challenge page | 2020 | challenge page | https://ir.nist.gov/covidSubmit/index.html |
| mteb/trec-covid | 2024 | dataset card | https://huggingface.co/datasets/mteb/trec-covid |

## Machine-Readable Metadata

<!-- benchmark-task-metadata:v1 -->

```yaml
benchmark_task_metadata:
  schema_version: 1
  document_status: first_pass
  nano_set: NanoMMTEB-v2
  backing_dataset: NanoMMTEB-v2
  dataset_id: hakari-bench/NanoMMTEB-v2
  task_name: treccovid
  split_name: treccovid
  language: en
  category: natural_language
  document_path: docs/benchmark_tasks/NanoMMTEB-v2/treccovid.md
  source_research:
    primary_source_type: task_paper
    paper_pdf_or_html_checked: true
    no_paper_note: null
  counts:
    queries: 50
    documents: 10000
    positive_qrels: 4527
  positives_per_query:
    average: 90.54
    min: 22
    median: 100.0
    max: 100
    multi_positive_queries: 50
    multi_positive_query_percent: 100.0
  text_stats_chars:
    query_mean: 69.24
    document_mean: 1321.5673
  bm25:
    ndcg_at_10: 0.36270342680916934
    hit_at_10: 0.92
    source: dataset_candidate_subset
  learning:
    original_train_split: available
    evaluation_split_origin: test
    train_eval_overlap_audit: not_audited
    leakage_note: do not train on this Nano split's TREC-COVID topics, qrels, or judged
      article records
    useful_training_data:
    - biomedical literature retrieval
    - CORD-19 and PubMed title-abstract retrieval
    - TREC-style judged biomedical topics outside this split
    - disease and drug matched hard negatives
    synthetic_data:
      document_generation: biomedical titles and abstracts with clinical and mechanistic
        evidence
      question_generation: COVID-19 information needs about populations, interventions,
        outcomes, and mechanisms
      answerability: positive article should address the biomedical evidence need
    multi_positive_training: multi_positive_objective
  links:
    nano_dataset: https://huggingface.co/datasets/hakari-bench/NanoMMTEB-v2
    source_urls:
    - label: TREC-COVID arXiv
      url: https://arxiv.org/abs/2005.04474
    - label: NIST TREC-COVID
      url: https://ir.nist.gov/covidSubmit/index.html
    - label: mteb/trec-covid
      url: https://huggingface.co/datasets/mteb/trec-covid
    source_notes: []
  references:
  - title: 'TREC-COVID: Constructing a Pandemic Information Retrieval Test Collection'
    url: https://arxiv.org/abs/2005.04474
    year: 2020
    is_paper: true
    source_confidence: definitive_paper_link
  candidate_subsets:
    bm25:
      config: bm25
      label: BM25
      source: dataset_candidate_subset
      top_k: 500
      ndcg_at_10: 0.3627034268
      hit_at_10: 0.92
      recall_at_100: 0.2319416832
      candidate_count_min: 500
      candidate_count_max: 500
      candidate_count_mean: 500.0
      query_count: 50
      query_coverage: 1.0
      relevant_coverage_at_100: 0.2319416832
    dense:
      config: harrier_oss_v1_270m
      label: Dense
      source: dataset_candidate_subset
      top_k: 500
      ndcg_at_10: 0.4266339246
      hit_at_10: 0.94
      recall_at_100: 0.2575657168
      candidate_count_min: 500
      candidate_count_max: 500
      candidate_count_mean: 500.0
      query_count: 50
      query_coverage: 1.0
      relevant_coverage_at_100: 0.2575657168
    reranking_hybrid:
      config: reranking_hybrid
      label: Reranking hybrid
      source: dataset_candidate_subset
      top_k: 100
      ndcg_at_10: 0.4505324745
      hit_at_10: 0.98
      recall_at_100: 0.2761210515
      candidate_count_min: 100
      candidate_count_max: 100
      candidate_count_mean: 100.0
      query_count: 50
      query_coverage: 1.0
      relevant_coverage_at_100: 0.2761210515
      safeguard_positive_rows: 0
      rows_with_101_candidates: 0
```
