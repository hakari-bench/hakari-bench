# NanoR2MED / NanoR2MEDMedQADiag

## Overview

R2MED defines MedQA-Diagnosis as clinical evidence retrieval for diagnostic
reasoning: a MedQA-style patient vignette is converted into an open-ended
diagnostic question, and relevant documents are medical textbook chunks that
support the diagnosis or reasoning. In this Nano split, long case queries with
age, symptoms, labs, imaging, and exam findings retrieve passages from sources
such as Harrison, Gray's Anatomy, First Aid, Lippincott, Katzung, and Schwartz.
The task therefore tests inference from a case narrative to authoritative
diagnostic evidence.

## Details

### What the Original Data Measures

[R2MED: A Benchmark for Reasoning-Driven Medical Retrieval](https://arxiv.org/abs/2505.14558)
describes the clinical evidence retrieval task as retrieving authoritative
medical evidence that supports diagnostic or treatment decisions. For the
diagnosis dataset, R2MED uses MedQA as the QA source and medical textbook
materials released with the original MedQA benchmark as documents.

The paper explains that clinical evidence datasets are built through task-based
filtering, rule-based filtering, difficulty filtering with several instruction
models, and open-ended reformulation of multiple-choice questions. Relevance is
then assessed with the query, answer, and generated reasoning path; documents
must score highly for both answer relevance and reasoning support.

### Observed Data Profile

The Nano split has 118 queries, 10,000 documents, and 522 positive qrels. Queries
average 706.74 characters and usually present a patient vignette with age,
symptoms, history, labs, imaging, or examination findings. Documents average
791.42 characters and are short textbook chunks from sources such as Harrison,
Gray's Anatomy, First Aid, Lippincott, Katzung, Schwartz, and similar materials.

Each query has 4.42 positives on average, with a median of 4 and a maximum of
8 positives. The positives may state the diagnosis directly, explain a mechanism,
or provide a relevant management or anatomy fact. This makes the split strongly
reasoning-dependent: the model often must infer the disease entity first and
then retrieve supporting textbook evidence.

### BM25 Difficulty

Using the dataset-provided BM25 candidate column, BM25 reaches nDCG@10 = 0.0281
and hit@10 = 0.1356. It ranks only 2 positives first and finds a positive in the
top 10 for 16 of 118 queries. This is one of the hardest NanoR2MED splits for
sparse retrieval.

Observed failures include a pregnancy/diabetes query where the positive
textbook passage concerns diabetic pregnancy counseling but BM25 surfaces an
unrelated pharmacology vignette, a stillbirth-malformation query where surgical
congenital-abnormality material ranks above embryology definitions, and
toxidrome or infection cases where BM25 latches onto matching demographics or
symptoms rather than the latent diagnosis.

### Training Data That May Help

Useful training data includes non-overlapping MedQA training cases paired with
diagnosis-supporting textbook passages, medical exam retrieval, diagnostic
entity linking, clinical vignette-to-concept retrieval, and hard negatives from
similar symptoms but different diagnoses. Training should preserve the
multi-positive structure because many cases have several evidence passages.

For clean evaluation, avoid the R2MED MedQA-Diag benchmark queries, qrels, and
positive textbook chunks. If using MedQA or textbook-derived corpora, audit for
overlap with the R2MED release and Nano positives.

### Synthetic Data Guidance

For document-to-question generation, start from non-evaluation medical textbook
passages and generate patient vignettes whose correct diagnosis or diagnostic
step is explicitly supported by the passage. The generated question should not
just paraphrase the passage; it should require clinical inference from symptoms,
labs, or risk factors.

For joint generation, create textbook-style evidence chunks and realistic exam
vignettes with one or more explicit diagnostic anchors. Hard negatives should
share symptoms, demographics, or body systems but imply a different diagnosis.
Do not seed generation with Nano evaluation queries or positive passages.

## Example Data

| Query | Positive document |
| --- | --- |
| A 33-year-old G2P1 woman presents to the office because of poor diabetic control. She is currently at 18 weeks gestation and admits to having poor control of her type 1 diabetes before becoming pregnant. Her family history is ... [truncated 225 chars](439 chars) | Malformations. he incidence of major malformations in women with type 1 diabetes is at least doubled and approximates 11 percent Qovanovic, 2015). These account for almost half of perinatal deaths in diabetic pregnancies. As ... [truncated 225 chars](628 chars) |
| A 68-year-old man presents with difficulty breathing for the last 3 hours. Upon asking about other symptoms, he mentions that he had a cough for the last 4 months which he attributes to his smoking. He says he had frequent na ... [truncated 225 chars](986 chars) | The optic nerve [II] is not a true cranial nerve, but rather an extension of the brain carrying afferent fibers from the retina of the eyeball to the visual centers of the brain. The optic nerve is surrounded by the cranial m ... [truncated 225 chars](921 chars) |
| A 25-year-old woman presents to her primary care provider for evaluation of a "painful mass in my left groin." She says that her symptoms began 4 days ago as a painful mass that slowly enlarged, ruptured, and ulcerated. Howev ... [truncated 225 chars](796 chars) | lympHogranUloma venereUm C. trachomatis serovars L1, L2, and L3 cause LGV, an invasive systemic STD. The peak inci dence of LGV corresponds with the age of greatest sexual activity: the second and third decades of life. The w ... [truncated 225 chars](995 chars) |
| A one-week-old boy presents with yellow sclerae, severe lethargy, and decreased muscle tone. His mother notes that the symptoms started shortly after birth and have been progressively worsening. The patient is breast fed and ... [truncated 225 chars](637 chars) | Crigler-Najjar Syndrome, Type I CN-I is characterized by striking uncon jugated hyperbilirubinemia of about 340–765 μmol/L (20–45 mg/dL) that appears in the neonatal period and persists for life. Other conventional hepatic bi ... [truncated 225 chars](997 chars) |
| A 4-year-old girl is brought to the emergency department with a persistent cough, fever, and vomiting. The past year the child has been admitted to the hospital 3 times with pneumonia. For the past 1 week, the child has been ... [truncated 225 chars](888 chars) | Mendelian Disorders: Diseases Caused by Single-Gene Defects251 abnormally viscid mucous secretions that block the airways and the pancreatic ducts which in turn are responsible for the two most important clinical manifestatio ... [truncated 225 chars](845 chars) |

## Dataset Information

| Field | Value |
| --- | --- |
| Nano set | NanoR2MED |
| Backing dataset | NanoR2MED |
| Task / split | NanoR2MEDMedQADiag |
| Hugging Face dataset | [hakari-bench/NanoR2MED](https://huggingface.co/datasets/hakari-bench/NanoR2MED) |
| Language | en |
| Category | natural_language |
| Queries | 118 |
| Documents | 10,000 |
| Positive qrels | 522 |
| Avg positives / query | 4.42 |
| Positives per query (min / median / max) | 1 / 4 / 8 |
| Queries with multiple positives | 103 (87.29%) |
| BM25 nDCG@10 | 0.0700 |
| BM25 hit@10 | 0.2458 |
| BM25 Recall@100 | 0.2318 |
| BM25 candidate subset | top-500 (`bm25`) |
| Dense nDCG@10 | 0.1254 |
| Dense hit@10 | 0.3559 |
| Dense Recall@100 | 0.4272 |
| Dense candidate subset | top-500 (`harrier_oss_v1_270m`) |
| Reranking hybrid nDCG@10 | 0.1406 |
| Reranking hybrid hit@10 | 0.3983 |
| Reranking hybrid Recall@100 | 0.3985 |
| Reranking hybrid candidate subset | top-100 plus optional rank-101 safeguard (`reranking_hybrid`) |
| Reranking hybrid candidates / query | 100-101 |
| Reranking hybrid safeguard rows | 34 |
| Query length avg chars | 706.74 |
| Document length avg chars | 791.42 |

### Public Sources

- [R2MED: A Benchmark for Reasoning-Driven Medical Retrieval](https://arxiv.org/abs/2505.14558); 2025; Xiangxu Zhang, Lei Li, Xiao Zhou, and Zheng Liu; DOI: `10.48550/arXiv.2505.14558`.
- [R2MED project page](https://r2med.github.io/).
- [R2MED GitHub repository](https://github.com/R2MED/R2MED).
- [R2MED/MedQA-Diag dataset card](https://huggingface.co/datasets/R2MED/MedQA-Diag).

### Hugging Face Links

- Nano dataset: [hakari-bench/NanoR2MED](https://huggingface.co/datasets/hakari-bench/NanoR2MED)
- Source dataset: [R2MED/MedQA-Diag](https://huggingface.co/datasets/R2MED/MedQA-Diag)

### Source Reference Table

| Title | Year | Type | URL |
| --- | ---: | --- | --- |
| R2MED: A Benchmark for Reasoning-Driven Medical Retrieval | 2025 | arXiv paper | https://arxiv.org/abs/2505.14558 |
| R2MED project page | 2025 | project page | https://r2med.github.io/ |
| R2MED GitHub repository | 2025 | source repository | https://github.com/R2MED/R2MED |
| R2MED/MedQA-Diag | 2025 | dataset card | https://huggingface.co/datasets/R2MED/MedQA-Diag |

## Machine-Readable Metadata

<!-- benchmark-task-metadata:v1 -->

```yaml
benchmark_task_metadata:
  schema_version: 1
  document_status: first_pass
  nano_set: NanoR2MED
  backing_dataset: NanoR2MED
  dataset_id: hakari-bench/NanoR2MED
  task_name: NanoR2MEDMedQADiag
  split_name: NanoR2MEDMedQADiag
  language: en
  category: natural_language
  document_path: docs/benchmark_tasks/NanoR2MED/NanoR2MEDMedQADiag.md
  source_research:
    primary_source_type: benchmark_paper
    paper_pdf_or_html_checked: true
    paper_url: https://arxiv.org/abs/2505.14558
    additional_source_urls:
    - https://r2med.github.io/
    - https://github.com/R2MED/R2MED
    - https://huggingface.co/datasets/R2MED/MedQA-Diag
  counts:
    queries: 118
    documents: 10000
    positive_qrels: 522
  positives_per_query:
    average: 4.4237288136
    min: 1
    median: 4.0
    max: 8
    multi_positive_queries: 103
    multi_positive_query_percent: 87.29
  text_stats_chars:
    query_mean: 706.737288
    document_mean: 791.422
  bm25:
    ndcg_at_10: 0.07001734152215396
    hit_at_10: 0.2457627118644068
    source: dataset_candidate_subset
  learning:
    original_train_split: not_found
    evaluation_split_origin: R2MED benchmark release sampled into NanoR2MED
    train_eval_overlap_audit: not_audited
    leakage_note: exclude R2MED MedQA-Diag evaluation queries, qrels, and positive
      textbook passages
    useful_training_data:
    - non-overlapping MedQA diagnostic cases with evidence passages
    - clinical vignette to diagnosis retrieval
    - medical textbook section retrieval
    - hard negatives from similar symptoms but different diagnoses
    synthetic_data:
      document_generation: non-evaluation textbook passages about diagnoses, mechanisms,
        anatomy, or management
      question_generation: open-ended clinical vignettes requiring diagnostic inference
        grounded in the passage
      hard_negatives: same symptoms or body system but different diagnosis
      answerability: the passage should support the inferred diagnosis or diagnostic
        step
    multi_positive_training: multi_positive_objective
  links:
    nano_dataset: https://huggingface.co/datasets/hakari-bench/NanoR2MED
    source_urls:
    - label: R2MED arXiv
      url: https://arxiv.org/abs/2505.14558
    - label: R2MED project page
      url: https://r2med.github.io/
    - label: R2MED GitHub
      url: https://github.com/R2MED/R2MED
    - label: R2MED/MedQA-Diag
      url: https://huggingface.co/datasets/R2MED/MedQA-Diag
    source_notes: []
  references:
  - title: 'R2MED: A Benchmark for Reasoning-Driven Medical Retrieval'
    url: https://arxiv.org/abs/2505.14558
    year: 2025
    doi: 10.48550/arXiv.2505.14558
    is_paper: true
    source_confidence: definitive_paper_link
  candidate_subsets:
    bm25:
      config: bm25
      label: BM25
      source: dataset_candidate_subset
      top_k: 500
      ndcg_at_10: 0.0700173415
      hit_at_10: 0.2457627119
      recall_at_100: 0.2318007663
      candidate_count_min: 500
      candidate_count_max: 500
      candidate_count_mean: 500.0
      query_count: 118
      query_coverage: 1.0
      relevant_coverage_at_100: 0.2318007663
    dense:
      config: harrier_oss_v1_270m
      label: Dense
      source: dataset_candidate_subset
      top_k: 500
      ndcg_at_10: 0.1254054773
      hit_at_10: 0.3559322034
      recall_at_100: 0.4272030651
      candidate_count_min: 500
      candidate_count_max: 500
      candidate_count_mean: 500.0
      query_count: 118
      query_coverage: 1.0
      relevant_coverage_at_100: 0.4272030651
    reranking_hybrid:
      config: reranking_hybrid
      label: Reranking hybrid
      source: dataset_candidate_subset
      top_k: 100
      ndcg_at_10: 0.1405588095
      hit_at_10: 0.3983050847
      recall_at_100: 0.398467433
      candidate_count_min: 100
      candidate_count_max: 101
      candidate_count_mean: 100.288136
      query_count: 118
      query_coverage: 1.0
      relevant_coverage_at_100: 0.398467433
      safeguard_positive_rows: 34
      rows_with_101_candidates: 34
```
