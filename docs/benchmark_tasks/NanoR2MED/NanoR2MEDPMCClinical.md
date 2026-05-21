# NanoR2MED / NanoR2MEDPMCClinical

## Overview

R2MED defines PMC-Clinical as similar-case retrieval from PubMed Central case
reports: the confirmed diagnosis acts as the bridge between a query case and
relevant case documents. This Nano split uses concise patient case descriptions
as queries and longer PMC case presentations as documents. The sampled cases
include mandibular lesions, melanoma complications, retroperitoneal disease,
and other rare or complex presentations, so the retriever must match inferred
diagnosis and clinically meaningful similarity rather than only overlapping
symptom words.

## Details

### What the Original Data Measures

[R2MED: A Benchmark for Reasoning-Driven Medical Retrieval](https://arxiv.org/abs/2505.14558)
defines clinical case retrieval as retrieving similar cases with the same
diagnosis to assist analysis of a patient scenario. The paper states that
R2MED collects full patient records from PMC-Patients and IIYi-bingli, extracts
structured clinical presentations, and uses the confirmed diagnosis as the
reasoning bridge between query and relevant cases.

For PMC-Clinical, R2MED identifies multi-case PMC-Patients articles, extracts
the first described case as the query source, and keeps a limited number of
additional cases from the same report as positives. Candidate cases undergo
quality filtering, question formulation, relevance assessment, and expert
review. The paper notes that PMC-Patients is a curated PubMed Central case
collection and that R2MED is intended only for research evaluation.

### Observed Data Profile

The Nano split has 114 queries, 10,000 documents, and 248 positive qrels.
Queries average 827.68 characters and are concise case summaries with age,
symptoms, imaging, pathology, examination findings, or clinical course.
Documents average 2,103.50 characters and are longer case presentations.

Each query has 2.18 positives on average, with a median of 2 and a maximum of
4 positives. Sampled cases include mandibular osteolytic lesions, melanoma with
intracranial events, retroperitoneal tumors, skull-base inflammatory disease,
and splenic masses. The positives can be clinically similar without sharing the
same age, sex, or exact symptom wording, so diagnosis-level reasoning matters.

### BM25 Difficulty

Using the dataset-provided BM25 candidate column, BM25 reaches nDCG@10 = 0.3277
and hit@10 = 0.6140. It ranks 36 positives first and finds a positive inside
the top 10 for 70 of 114 queries. Among NanoR2MED tasks, this is relatively
strong for BM25 because case reports often repeat distinctive anatomy, disease,
imaging, or symptom terms.

Hard cases remain. BM25 can retrieve a topically similar case with the wrong
diagnosis, such as neurocognitive or dental presentations that share symptoms
but not the diagnostic entity. In other failures, the top BM25 document matches
anatomical region or complaint while the positive is a diagnostically related
case with different surface wording.

### Training Data That May Help

Useful training data includes non-overlapping case-report similarity pairs,
PMC-Patients retrieval, diagnosis-labeled case matching, clinical entity linking,
and hard negatives from cases sharing symptoms but different diagnoses.
Multi-positive training is appropriate because most queries have more than one
positive case.

Training should exclude the R2MED PMC-Clinical evaluation cases, qrels, and
positive case passages. If using PMC-Patients, audit for article-level overlap
because multiple cases from the same article can appear as positives.

### Synthetic Data Guidance

For document-to-question generation, use non-evaluation case reports and produce
query cases with diagnosis names removed while preserving symptoms, imaging,
labs, and course. The generated positive should be another case whose diagnosis
and clinical reasoning support the query.

For joint generation, create clusters of related cases sharing a diagnosis but
varying demographics and presentation. Hard negatives should share anatomy or
symptoms but have a different diagnosis. Do not seed generation with Nano
evaluation cases or positives.

## Example Data

| Query | Positive document |
| --- | --- |
| A 5-year-old female patient presents with swelling and pain in the right mandibular region. Initial antibiotic treatment provided temporary relief, but her symptoms recurred. Computed tomography (CT) shows an osteolytic, well ... [truncated 225 chars](532 chars) | A 33-year-old male attended the medical consultation complaining of a painful perianal lesion over the last 18 months. Previous therapeutic attempts, including different antibiotics orally or topically administered, and topic ... [truncated 225 chars](1579 chars) |
| A 46-year-old man with a history of radical extirpated melanoma presents with spontaneous acute severe headache, followed by progressive confusion and mild left-sided hemiparesis. MRI of the brain shows ischemic lesions in th ... [truncated 225 chars](988 chars) | A 29-year-old female patient with a 6-day history of laparoscopic uterine myomectomy visited a local hospital complaining of worsening headache and mild left hand weakness since surgery. Brain computed tomography (CT) showed ... [truncated 225 chars](1977 chars) |
| An 82-year-old man presented with a chief complaint of an abdominal mass and associated abdominal discomfort, which he first noticed 4 years prior. A CT scan revealed a lipomatous retroperitoneal tumor that had been growing. ... [truncated 225 chars](518 chars) | A 71-year-old woman presented with complaint of progressive abdominal distension. The ultrasonography revealed a huge retroperitoneal or mesenchymal mass occupying the entire abdomen. The patient had not experienced any sympt ... [truncated 225 chars](2908 chars) |
| A 69-year-old male presents with a progressive frontal paroxysmal headache, mild vomiting, diplopia, and visual disturbance for 1 month. He denies having fever. His visual acuity is 0.6 in the left eye and 0.9 in the right ey ... [truncated 225 chars](749 chars) | A 52-year-old male was admitted with a paroxysmal headache in the right parietal region accompanied by visual disturbance in the right eye for over 2 months. Both symptoms mostly occurred in the morning and could be partially ... [truncated 225 chars](1291 chars) |
| An 8-year-old boy was incidentally found to have a splenic mass on abdominal ultrasonography during a routine check and was admitted for further investigation. He has no significant medical history, and physical examination a ... [truncated 225 chars](966 chars) | A 39-year-old Greek woman, with no remarkable medical history, presented to the emergency room of our hospital with diffuse abdominal pain and a mass-like distention of the left side of her abdomen. No weight loss was reporte ... [truncated 225 chars](1977 chars) |

## Dataset Information

| Field | Value |
| --- | --- |
| Nano set | NanoR2MED |
| Backing dataset | NanoR2MED |
| Task / split | NanoR2MEDPMCClinical |
| Hugging Face dataset | [hakari-bench/NanoR2MED](https://huggingface.co/datasets/hakari-bench/NanoR2MED) |
| Language | en |
| Category | natural_language |
| Queries | 114 |
| Documents | 10,000 |
| Positive qrels | 248 |
| Avg positives / query | 2.18 |
| Positives per query (min / median / max) | 1 / 2 / 4 |
| Queries with multiple positives | 83 (72.81%) |
| BM25 nDCG@10 | 0.3277 |
| BM25 hit@10 | 0.6140 |
| Query length avg chars | 827.68 |
| Document length avg chars | 2,103.50 |

### Public Sources

- [R2MED: A Benchmark for Reasoning-Driven Medical Retrieval](https://arxiv.org/abs/2505.14558); 2025; Xiangxu Zhang, Lei Li, Xiao Zhou, and Zheng Liu; DOI: `10.48550/arXiv.2505.14558`.
- [R2MED project page](https://r2med.github.io/).
- [R2MED GitHub repository](https://github.com/R2MED/R2MED).
- [R2MED/PMC-Clinical dataset card](https://huggingface.co/datasets/R2MED/PMC-Clinical).

### Hugging Face Links

- Nano dataset: [hakari-bench/NanoR2MED](https://huggingface.co/datasets/hakari-bench/NanoR2MED)
- Source dataset: [R2MED/PMC-Clinical](https://huggingface.co/datasets/R2MED/PMC-Clinical)

### Source Reference Table

| Title | Year | Type | URL |
| --- | ---: | --- | --- |
| R2MED: A Benchmark for Reasoning-Driven Medical Retrieval | 2025 | arXiv paper | https://arxiv.org/abs/2505.14558 |
| R2MED project page | 2025 | project page | https://r2med.github.io/ |
| R2MED GitHub repository | 2025 | source repository | https://github.com/R2MED/R2MED |
| R2MED/PMC-Clinical | 2025 | dataset card | https://huggingface.co/datasets/R2MED/PMC-Clinical |

## Machine-Readable Metadata

<!-- benchmark-task-metadata:v1 -->

```yaml
benchmark_task_metadata:
  schema_version: 1
  document_status: first_pass
  nano_set: NanoR2MED
  backing_dataset: NanoR2MED
  dataset_id: hakari-bench/NanoR2MED
  task_name: NanoR2MEDPMCClinical
  split_name: NanoR2MEDPMCClinical
  language: en
  category: natural_language
  document_path: docs/benchmark_tasks/NanoR2MED/NanoR2MEDPMCClinical.md
  source_research:
    primary_source_type: benchmark_paper
    paper_pdf_or_html_checked: true
    paper_url: https://arxiv.org/abs/2505.14558
    additional_source_urls:
      - https://r2med.github.io/
      - https://github.com/R2MED/R2MED
      - https://huggingface.co/datasets/R2MED/PMC-Clinical
  counts:
    queries: 114
    documents: 10000
    positive_qrels: 248
  positives_per_query:
    average: 2.1754385965
    min: 1
    median: 2.0
    max: 4
    multi_positive_queries: 83
    multi_positive_query_percent: 72.81
  text_stats_chars:
    query_mean: 827.675439
    document_mean: 2103.4971
  bm25:
    ndcg_at_10: 0.3277008275
    hit_at_10: 0.6140350877
    source: dataset_bm25_column
  learning:
    original_train_split: not_found
    evaluation_split_origin: R2MED benchmark release sampled into NanoR2MED
    train_eval_overlap_audit: not_audited
    leakage_note: exclude R2MED PMC-Clinical evaluation cases, qrels, positive case passages, and same-article duplicates
    useful_training_data:
      - non-overlapping clinical case similarity pairs
      - PMC-Patients retrieval and diagnosis-labeled case matching
      - clinical entity linking from case descriptions
      - hard negatives sharing symptoms but not diagnoses
    synthetic_data:
      document_generation: non-evaluation case reports with diagnosis-bearing clinical presentations
      question_generation: diagnosis-removed case queries seeking similar supporting cases
      hard_negatives: same anatomy or symptoms with different diagnoses
      answerability: positive cases should share the diagnosis or provide diagnostic support for the query case
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
      - label: R2MED/PMC-Clinical
        url: https://huggingface.co/datasets/R2MED/PMC-Clinical
    source_notes: []
  references:
    - title: "R2MED: A Benchmark for Reasoning-Driven Medical Retrieval"
      url: https://arxiv.org/abs/2505.14558
      year: 2025
      doi: 10.48550/arXiv.2505.14558
      is_paper: true
      source_confidence: definitive_paper_link
```
