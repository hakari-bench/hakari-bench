# NanoIFIR / NanoIFIRCds

## Overview

`NanoIFIRCds` is an instruction-following clinical decision support retrieval
task. Queries describe patient cases and ask for diagnosis, treatment, or test
information. Documents are biomedical article abstracts or article-like records
that may help a clinician answer the case-specific information need.

## Details

### What the Original Data Measures

[IFIR](https://arxiv.org/abs/2503.04644) uses TREC-CDS as a healthcare subset,
directly using the clinical case summary and detailed description as the
instruction. The IFIR paper frames this as simulating a doctor retrieving
healthcare-relevant passages for patient cases.

[Overview of the TREC 2015 Clinical Decision Support Track](https://trec.nist.gov/pubs/trec24/papers/Overview-CL.pdf)
states that CDS evaluates biomedical literature retrieval for generic clinical
questions about patient cases: diagnosis, test, and treatment. It used case
narratives as idealized medical records and asked systems to retrieve full-text
biomedical articles from PubMed Central that a physician might find useful.

### Observed Data Profile

The Nano split has 42 queries, 10,000 documents, and 466 positive qrels. Queries
average 225.21 characters, and documents average 1,627.45 characters. Queries
are short patient vignettes such as "58-year-old woman..." followed by a direct
clinical question. Documents are biomedical titles and abstracts.

The task is highly multi-positive: the median query has 9 positives and the
maximum is 37.

### BM25 Difficulty

Using the dataset-provided BM25 candidate column, BM25 reaches nDCG@10 =
0.1345 and hit@10 = 0.4762. BM25 ranks a positive first for 10 queries. The
task is difficult because relevant articles may discuss diagnostic or treatment
evidence without repeating every symptom or patient detail.

### Training Data That May Help

Useful training data includes non-overlapping TREC-CDS topics, biomedical case
retrieval, PubMed/PMC evidence retrieval, and hard negatives with the same
disease or symptom cluster. Training should preserve the clinical question type
and avoid using Nano qrels or positives.

### Synthetic Data Guidance

Generate patient vignettes with age, sex, symptoms, tests, and a question type.
Positive documents should be abstracts that could help answer diagnosis,
treatment, or testing needs. Hard negatives should be medically topical but
wrong for the question type or patient context.

## Example Data

| Query | Positive document |
| --- | --- |
| Given some infomation about patient.A 46-year-old woman with sweaty hands, exophthalmia, and weight loss despite increased eating.What is the patient's diagnosis? (162 chars) | Recognizing thyrotoxicosis in a patient with bipolar mania: a case report A thyroid stimulating hormone level is commonly measured in patients presenting with symptoms of mania in order to rule out an underlying general medic ... [truncated 225 chars](949 chars) |
| Given some infomation about patient.6-month-old male with decreased urine output and edema several hours after surgery. He is hypertensive and tachycardic, has a high BUN and creatinine, and urine microscopy reveals red blood ... [truncated 225 chars](289 chars) | Serum cystatin C concentration as a marker of acute renal dysfunction in critically ill patients In critically ill patients sudden changes in glomerular filtration rate (GFR) are not instantly followed by parallel changes in ... [truncated 225 chars](1849 chars) |
| Given some infomation about patient.40-year-old woman with severe right arm pain and hypotension. She has no history of trauma and right arm exam reveals no significant findings.What tests should the patient receive? (216 chars) | A simple statistical model for prediction of acute coronary syndrome in chest pain patients in the emergency department Several models for prediction of acute coronary syndrome (ACS) among chest pain patients in the emergency ... [truncated 225 chars](1449 chars) |
| Given some infomation about patient.2-year-old boy with fever and irritability for 5 days. Physical exam findings include conjunctivitis, strawberry tongue, and desquamation of the fingers and toes. Lab results include low al ... [truncated 225 chars](396 chars) | Behaviour sequelae following acute Kawasaki disease Kawasaki disease is a systemic vasculitis and may affect cerebral function acutely. The aim of the present study was to measure a number of behaviour and social parameters w ... [truncated 225 chars](1803 chars) |
| Given some infomation about patient.31-year-old female with amenorrhea, milky nipple discharge, negative urine pregnancy test, and elevated prolactin level.How should the patient be treated? (190 chars) | Prolactinomas, Cushing's disease and acromegaly: debating the role of medical therapy for secretory pituitary adenomas Pituitary adenomas are associated with a variety of clinical manifestations resulting from excessive hormo ... [truncated 225 chars](2805 chars) |

## Dataset Information

| Field | Value |
| --- | --- |
| Nano set | NanoIFIR |
| Backing dataset | NanoIFIR |
| Task / split | NanoIFIRCds |
| Hugging Face dataset | [hakari-bench/NanoIFIR](https://huggingface.co/datasets/hakari-bench/NanoIFIR) |
| Language | en |
| Category | natural_language |
| Queries | 42 |
| Documents | 10,000 |
| Positive qrels | 466 |
| Positives per query | avg 11.10 / min 1 / median 9.0 / max 37 |
| Multi-positive queries | 38 (90.48%) |
| BM25 nDCG@10 | 0.2258 |
| BM25 hit@10 | 0.6905 |
| BM25 Recall@100 | 0.3927 |
| BM25 candidate subset | top-500 (`bm25`) |
| Dense nDCG@10 | 0.4073 |
| Dense hit@10 | 0.8095 |
| Dense Recall@100 | 0.7124 |
| Dense candidate subset | top-500 (`harrier_oss_v1_270m`) |
| Reranking hybrid nDCG@10 | 0.3376 |
| Reranking hybrid hit@10 | 0.7619 |
| Reranking hybrid Recall@100 | 0.6652 |
| Reranking hybrid candidate subset | top-100 plus optional rank-101 safeguard (`reranking_hybrid`) |
| Reranking hybrid candidates / query | 100-101 |
| Reranking hybrid safeguard rows | 3 |
| Query length avg chars | 225.21 |
| Document length avg chars | 1,627.45 |

### Public Sources

- [IFIR: A Comprehensive Benchmark for Evaluating Instruction-Following in Expert-Domain Information Retrieval](https://arxiv.org/abs/2503.04644); 2025; Tingyu Song et al.
- [Overview of the TREC 2015 Clinical Decision Support Track](https://trec.nist.gov/pubs/trec24/papers/Overview-CL.pdf); 2015; Kirk Roberts et al.

### Hugging Face Links

- Nano dataset: [hakari-bench/NanoIFIR](https://huggingface.co/datasets/hakari-bench/NanoIFIR)

### Source Reference Table

| Title | Year | Type | URL |
| --- | ---: | --- | --- |
| IFIR: A Comprehensive Benchmark for Evaluating Instruction-Following in Expert-Domain Information Retrieval | 2025 | arXiv paper | https://arxiv.org/abs/2503.04644 |
| Overview of the TREC 2015 Clinical Decision Support Track | 2015 | TREC overview paper | https://trec.nist.gov/pubs/trec24/papers/Overview-CL.pdf |

## Machine-Readable Metadata

<!-- benchmark-task-metadata:v1 -->

```yaml
benchmark_task_metadata:
  schema_version: 1
  document_status: first_pass
  nano_set: NanoIFIR
  backing_dataset: NanoIFIR
  dataset_id: hakari-bench/NanoIFIR
  task_name: NanoIFIRCds
  split_name: NanoIFIRCds
  language: en
  category: natural_language
  document_path: docs/benchmark_tasks/NanoIFIR/NanoIFIRCds.md
  source_research:
    primary_source_type: benchmark_paper_and_task_paper
    paper_pdf_or_html_checked: true
    no_paper_note: null
  counts:
    queries: 42
    documents: 10000
    positive_qrels: 466
  positives_per_query:
    average: 11.095238095238095
    min: 1
    median: 9.0
    max: 37
    multi_positive_queries: 38
    multi_positive_query_percent: 90.47619047619048
  text_stats_chars:
    query_mean: 225.21428571428572
    document_mean: 1627.4549
  bm25:
    ndcg_at_10: 0.22575663643446836
    hit_at_10: 0.6904761904761905
    source: dataset_candidate_subset
  learning:
    original_train_split: available
    evaluation_split_origin: ifir_adapted
    train_eval_overlap_audit: not_audited
    leakage_note: exclude NanoIFIRCds queries, qrels, and positive biomedical articles
    useful_training_data:
    - non-overlapping TREC-CDS topics
    - PubMed and PMC clinical case retrieval
    - biomedical diagnosis treatment and test retrieval data
    - same-disease hard negatives
    synthetic_data:
      document_generation: biomedical article titles and abstracts about diagnosis,
        testing, and treatment
      question_generation: patient vignettes with explicit diagnosis/test/treatment
        retrieval instructions
      answerability: positives should provide information useful for the patient-specific
        clinical need
    multi_positive_training: preserve_multiple_clinically_relevant_articles
  links:
    nano_dataset: https://huggingface.co/datasets/hakari-bench/NanoIFIR
    source_urls:
    - label: IFIR arXiv
      url: https://arxiv.org/abs/2503.04644
    - label: TREC 2015 CDS overview
      url: https://trec.nist.gov/pubs/trec24/papers/Overview-CL.pdf
    source_notes: []
  references:
  - title: Overview of the TREC 2015 Clinical Decision Support Track
    url: https://trec.nist.gov/pubs/trec24/papers/Overview-CL.pdf
    year: 2015
    doi: null
    is_paper: true
    source_confidence: definitive_paper_link
  candidate_subsets:
    bm25:
      config: bm25
      label: BM25
      source: dataset_candidate_subset
      top_k: 500
      ndcg_at_10: 0.2257566364
      hit_at_10: 0.6904761905
      recall_at_100: 0.3927038627
      candidate_count_min: 500
      candidate_count_max: 500
      candidate_count_mean: 500.0
      query_count: 42
      query_coverage: 1.0
      relevant_coverage_at_100: 0.3927038627
    dense:
      config: harrier_oss_v1_270m
      label: Dense
      source: dataset_candidate_subset
      top_k: 500
      ndcg_at_10: 0.4073249106
      hit_at_10: 0.8095238095
      recall_at_100: 0.7124463519
      candidate_count_min: 500
      candidate_count_max: 500
      candidate_count_mean: 500.0
      query_count: 42
      query_coverage: 1.0
      relevant_coverage_at_100: 0.7124463519
    reranking_hybrid:
      config: reranking_hybrid
      label: Reranking hybrid
      source: dataset_candidate_subset
      top_k: 100
      ndcg_at_10: 0.3376132788
      hit_at_10: 0.7619047619
      recall_at_100: 0.6652360515
      candidate_count_min: 100
      candidate_count_max: 101
      candidate_count_mean: 100.071429
      query_count: 42
      query_coverage: 1.0
      relevant_coverage_at_100: 0.6652360515
      safeguard_positive_rows: 3
      rows_with_101_candidates: 3
```
