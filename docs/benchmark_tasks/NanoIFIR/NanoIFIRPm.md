# NanoIFIR / NanoIFIRPm

## Overview

`NanoIFIRPm` is an instruction-following precision-medicine retrieval task.
Queries describe cancer patients, diagnoses, and genetic variants, and documents
are clinical trial descriptions. The retriever must find trials suitable for the
patient profile.

## Details

### What the Original Data Measures

[IFIR](https://arxiv.org/abs/2503.04644) uses TREC-PM for healthcare
instruction-following retrieval. It expands patient information into different
instruction complexity levels, starting with disease and gene variation and
adding demographics, treatment history, or family history.

[Overview of the TREC 2017 Precision Medicine Track](https://trec.nist.gov/pubs/trec26/papers/Overview-PM.pdf)
states that the track focuses on precision oncology. Topics include cancer type,
genetic variants, demographics, and other factors, and systems retrieve
scientific articles or clinical trials relevant to individualized treatment
decisions. The 2017 track included a ClinicalTrials.gov corpus of 241,006 trial
descriptions.

### Observed Data Profile

The Nano split has 59 queries, 10,000 documents, and 1,217 positive qrels.
Queries average 145.75 characters, and documents average 2,233.58 characters.
Most queries ask for clinical trials for a patient with a cancer diagnosis and a
mutation such as ROS1, BRAF V600E, NRAS Q61R, PTEN, or CDK4 amplification.

This is strongly multi-positive: the median query has 22 positives, and the
maximum is 47.

### BM25 Difficulty

Using the dataset-provided BM25 candidate column, BM25 reaches nDCG@10 =
0.3522 and hit@10 = 0.8136. BM25 ranks a positive first for 30 queries. Gene
and cancer-type strings help lexical retrieval, but trial eligibility can depend
on variants, demographics, tumor type, and treatment details.

### Training Data That May Help

Useful training data includes non-overlapping TREC Precision Medicine topics,
ClinicalTrials.gov trial retrieval, biomedical entity linking, oncology trial
eligibility matching, and hard negatives with the same cancer type but different
mutation or inclusion criteria.

### Synthetic Data Guidance

Generate oncology patient profiles with cancer type, gene variants, age/sex, and
treatment history. Positive documents should be clinical trial descriptions with
matching inclusion criteria. Hard negatives should match one key entity but fail
another, such as cancer type, variant, stage, or prior therapy.

## Example Data

| Query | Positive document |
| --- | --- |
| A patient diagnosed with head and neck squamous cell carcinoma with a mutation in the CDKN2A gene. I am looking for possible clinical trials suitable for this patient. (167 chars) | De-intensification of Radiation and Chemotherapy for Low-Risk Human Papillomavirus-related Oropharyngeal Squamous Cell Carcinoma Carcinoma, Squamous Cell The purpose of this research study is to learn about the effectiveness ... [truncated 225 chars](3238 chars) |
| Patient diagnosed with prostate cancer with PTEN inactivating gene mutation. I am looking for possible clinical trials suitable for this patient. (145 chars) | Phase II Study of RAD001 in a Neoadjuvant Setting in Men With Intermediate or High Risk Prostate Cancer Prostate Cancer The mechanisms responsible for the development of hormonal refractory prostate cancer (HRPC)have been elu ... [truncated 225 chars](3481 chars) |
| A patient diagnosed with gastric cancer with the PIK3CA (E545K) gene mutation. I am looking for possible clinical trials suitable for this patient. (147 chars) | BKM120 in Cancers With PIK3CA Activating Mutations Lung Cancer In people whos cancers have a PIK3CA mutation, this trial will be evaluating the drug BKM120as a possible treatment. BKM120 works by blocking the phosphatidylinos ... [truncated 225 chars](2539 chars) |
| A patient diagnosed with papillary thyroid carcinoma and carrying the NTRK1 gene mutation. I am looking for possible clinical trials suitable for this patient. (159 chars) | Study of Oral RXDX-101 in Adult Patients With Locally Advanced or Metastatic Cancer Targeting NTRK1, NTRK2, NTRK3, ROS1, or ALK Molecular Alterations. Locally Advanced Solid Tumors Entrectinib (RXDX-101) is an orally availabl ... [truncated 225 chars](2588 chars) |
| Patient diagnosed with Ampullary carcinoma with KRAS gene mutation. Seeking possible clinical trials suitable for this patient. (127 chars) | Combined Biological Treatment and Chemotherapy for Patients With Inoperable Cholangiocarcinoma Cholangiocarcinoma The purpose of this study is partly to continue the good experience the investigators havewith chemotherapy and ... [truncated 225 chars](2078 chars) |

## Dataset Information

| Field | Value |
| --- | --- |
| Nano set | NanoIFIR |
| Backing dataset | NanoIFIR |
| Task / split | NanoIFIRPm |
| Hugging Face dataset | [hakari-bench/NanoIFIR](https://huggingface.co/datasets/hakari-bench/NanoIFIR) |
| Language | en |
| Category | natural_language |
| Queries | 59 |
| Documents | 10,000 |
| Positive qrels | 1,217 |
| Positives per query | avg 20.63 / min 1 / median 22 / max 47 |
| Multi-positive queries | 57 (96.61%) |
| BM25 nDCG@10 | 0.4232 |
| BM25 hit@10 | 0.8644 |
| BM25 Recall@100 | 0.5768 |
| BM25 candidate subset | top-500 (`bm25`) |
| Dense nDCG@10 | 0.5448 |
| Dense hit@10 | 0.9153 |
| Dense Recall@100 | 0.6812 |
| Dense candidate subset | top-500 (`harrier_oss_v1_270m`) |
| Reranking hybrid nDCG@10 | 0.5468 |
| Reranking hybrid hit@10 | 0.8983 |
| Reranking hybrid Recall@100 | 0.7305 |
| Reranking hybrid candidate subset | top-100 plus optional rank-101 safeguard (`reranking_hybrid`) |
| Reranking hybrid candidates / query | 100-101 |
| Reranking hybrid safeguard rows | 1 |
| Query length avg chars | 145.75 |
| Document length avg chars | 2,233.58 |

### Public Sources

- [IFIR: A Comprehensive Benchmark for Evaluating Instruction-Following in Expert-Domain Information Retrieval](https://arxiv.org/abs/2503.04644); 2025; Tingyu Song et al.
- [Overview of the TREC 2017 Precision Medicine Track](https://trec.nist.gov/pubs/trec26/papers/Overview-PM.pdf); 2017; Kirk Roberts et al.

### Hugging Face Links

- Nano dataset: [hakari-bench/NanoIFIR](https://huggingface.co/datasets/hakari-bench/NanoIFIR)

### Source Reference Table

| Title | Year | Type | URL |
| --- | ---: | --- | --- |
| IFIR: A Comprehensive Benchmark for Evaluating Instruction-Following in Expert-Domain Information Retrieval | 2025 | arXiv paper | https://arxiv.org/abs/2503.04644 |
| Overview of the TREC 2017 Precision Medicine Track | 2017 | TREC overview paper | https://trec.nist.gov/pubs/trec26/papers/Overview-PM.pdf |

## Machine-Readable Metadata

<!-- benchmark-task-metadata:v1 -->

```yaml
benchmark_task_metadata:
  schema_version: 1
  document_status: first_pass
  nano_set: NanoIFIR
  backing_dataset: NanoIFIR
  dataset_id: hakari-bench/NanoIFIR
  task_name: NanoIFIRPm
  split_name: NanoIFIRPm
  language: en
  category: natural_language
  document_path: docs/benchmark_tasks/NanoIFIR/NanoIFIRPm.md
  source_research:
    primary_source_type: benchmark_paper_and_task_paper
    paper_pdf_or_html_checked: true
    no_paper_note: null
  counts:
    queries: 59
    documents: 10000
    positive_qrels: 1217
  positives_per_query:
    average: 20.627118644067796
    min: 1
    median: 22
    max: 47
    multi_positive_queries: 57
    multi_positive_query_percent: 96.61016949152543
  text_stats_chars:
    query_mean: 145.74576271186442
    document_mean: 2233.5822
  bm25:
    ndcg_at_10: 0.42322297218973576
    hit_at_10: 0.864406779661017
    source: dataset_candidate_subset
  learning:
    original_train_split: available
    evaluation_split_origin: ifir_adapted
    train_eval_overlap_audit: not_audited
    leakage_note: exclude NanoIFIRPm patient queries, qrels, and positive clinical
      trial documents
    useful_training_data:
    - non-overlapping TREC Precision Medicine topics
    - ClinicalTrials.gov oncology trial retrieval pairs
    - biomedical entity linking and gene-variant normalization
    - same-cancer different-mutation hard negatives
    synthetic_data:
      document_generation: clinical trial descriptions with cancer type, gene variants,
        inclusion criteria, and interventions
      question_generation: patient-specific oncology trial search instructions
      answerability: positives should satisfy the patient disease and mutation profile
    multi_positive_training: preserve_multiple_suitable_trials
  links:
    nano_dataset: https://huggingface.co/datasets/hakari-bench/NanoIFIR
    source_urls:
    - label: IFIR arXiv
      url: https://arxiv.org/abs/2503.04644
    - label: TREC 2017 Precision Medicine overview
      url: https://trec.nist.gov/pubs/trec26/papers/Overview-PM.pdf
    source_notes: []
  references:
  - title: Overview of the TREC 2017 Precision Medicine Track
    url: https://trec.nist.gov/pubs/trec26/papers/Overview-PM.pdf
    year: 2017
    doi: null
    is_paper: true
    source_confidence: definitive_paper_link
  candidate_subsets:
    bm25:
      config: bm25
      label: BM25
      source: dataset_candidate_subset
      top_k: 500
      ndcg_at_10: 0.4232229722
      hit_at_10: 0.8644067797
      recall_at_100: 0.5768282662
      candidate_count_min: 500
      candidate_count_max: 500
      candidate_count_mean: 500.0
      query_count: 59
      query_coverage: 1.0
      relevant_coverage_at_100: 0.5768282662
    dense:
      config: harrier_oss_v1_270m
      label: Dense
      source: dataset_candidate_subset
      top_k: 500
      ndcg_at_10: 0.5447890924
      hit_at_10: 0.9152542373
      recall_at_100: 0.6811832375
      candidate_count_min: 500
      candidate_count_max: 500
      candidate_count_mean: 500.0
      query_count: 59
      query_coverage: 1.0
      relevant_coverage_at_100: 0.6811832375
    reranking_hybrid:
      config: reranking_hybrid
      label: Reranking hybrid
      source: dataset_candidate_subset
      top_k: 100
      ndcg_at_10: 0.5468354766
      hit_at_10: 0.8983050847
      recall_at_100: 0.7304847987
      candidate_count_min: 100
      candidate_count_max: 101
      candidate_count_mean: 100.016949
      query_count: 59
      query_coverage: 1.0
      relevant_coverage_at_100: 0.7304847987
      safeguard_positive_rows: 1
      rows_with_101_candidates: 1
```
