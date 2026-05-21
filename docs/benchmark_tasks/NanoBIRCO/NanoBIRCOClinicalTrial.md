# NanoBIRCO / NanoBIRCOClinicalTrial

## Overview

In BIRCO's Clinical-Trial task, the retrieval objective is eligibility matching:
a patient case report must retrieve clinical trial descriptions that fit the
patient's condition, history, tests, medications, and treatment context. This
Nano split is strongly multi-positive, with many eligible trials per patient
case. The task therefore rewards medical constraint matching across diagnosis,
age, pregnancy or treatment status, and trial criteria rather than generic
semantic similarity between a case vignette and oncology or psychiatry text.

## Details

### What the Original Data Measures

[BIRCO: A Benchmark of Information Retrieval Tasks with Complex
Objectives](https://arxiv.org/abs/2402.14151) describes BIRCO as a benchmark for
retrieval tasks where documents must satisfy complex objectives, not just share
surface meaning with the query. The paper states that the Clinical-Trial task
uses paragraph-length patient case reports as queries and clinical trial
descriptions as passages, with the objective of matching eligible patients to
suitable trials for recruitment.

The BIRCO paper reports that Clinical-Trial uses a 3-level relevance scale in
the source benchmark and has many relevant documents per query. It also notes
that Clinical-Trial contains hard negatives: non-relevant clinical trials that
match the patient's disease but fail other eligibility or objective constraints.
This makes the task different from ordinary biomedical keyword retrieval. The
retriever must compare a whole patient profile with the study purpose,
condition, intervention, and trial population.

BIRCO was also designed with LLM evaluation constraints in mind. The paper
describes decontamination filtering, including prompting GPT-4 to generate
plausible clinical trials from patient reports and removing contaminated
queries. For Clinical-Trial, the authors report that 7% of queries were removed
during filtering. Candidate pools were built from the original clinical-trial
candidate pools, while the BIRCO task objective prompt emphasizes patient
recruitment and trial eligibility.

### Observed Data Profile

The sampled Nano task has 50 queries, 3,375 documents, and 1,042 positive qrel
rows. Unlike most other NanoBIRCO tasks, this split is multi-positive: the
average query has 20.84 positive trials, the median has 15, and the maximum has
68. Queries average 496.98 characters and are concise patient vignettes with
age, sex, symptoms, medical history, tests, medications, and acute presentation.

Documents average 1,174.34 characters and are clinical trial descriptions. The
observed positives cover bipolar disorder and mania treatment, peptic ulcer
bleeding, stage IIIB/IV non-small cell lung cancer, diabetic skin ulcers,
COPD exacerbations, familial adenomatous polyposis, diabetes and calcaneal
spur risk, heart failure breathing techniques, pulmonary infections, pulmonary
embolism-like presentations, and femoral catheterization complications.

The task is not answer extraction from a single trial. Many positive trials may
be acceptable for a patient, and the candidate pool contains trials with partial
overlap in disease, symptom, procedure, or demographic group. Strong retrieval
requires matching both medical condition and suitability constraints.

### BM25 Difficulty

Using the dataset-provided BM25 candidate column, BM25 reaches nDCG@10 = 0.1194
and hit@10 = 0.6200 when relevance is treated as membership in the Nano qrels.
BM25 retrieves at least one positive trial in the top 10 for 31 of 50 queries,
but only 57 of 1,042 positive qrel rows appear in the top 10. This is a hard
setting for lexical retrieval because many trials use related but not identical
clinical terminology, and many near matches share the main disease while failing
other constraints.

The inspected failures show the problem clearly. For a patient with familial
adenomatous polyposis and rectosigmoid polyps, BM25 ranks general colonoscopy
and adenoma-detection trials above a black-raspberry FAP rectal-polyp trial. For
a diabetic patient with a painful oozing leg lesion, unrelated dermatology and
vascular trials rank above some relevant diabetes or wound-related trials. For a
heart-failure presentation with orthopnea, crackles, edema, and jugular venous
distension, BM25 retrieves breath, fever, or dyspnea trials before a trial about
slow breathing in heart failure.

Because this task has many positives per query, hit@10 alone is weak evidence:
a system may find one loosely suitable trial while missing many other relevant
trials. nDCG@10 is more useful for measuring whether the top results are densely
populated with relevant trials.

### Training Data That May Help

Useful training data should include non-overlapping patient-to-trial matching
pairs with eligibility labels. ClinicalTrials.gov descriptions paired with
synthetic or real patient vignettes can help, but training data should avoid
overlap with BIRCO's filtered evaluation queries and candidate pools. Strong
auxiliary data includes trial eligibility matching, clinical trial search logs,
biomedical passage retrieval with patient criteria, and hard negatives that
match the diagnosis but fail age, comorbidity, intervention, stage, or acuity.

Training should preserve multi-positive supervision. The model should not learn
to find a single canonical trial; it should rank many eligible or relevant trials
above disease-adjacent but unsuitable studies.

### Synthetic Data Guidance

For document-to-question generation, start from non-evaluation clinical trial
descriptions and generate patient vignettes that satisfy the trial's condition
and eligibility context. Include age, sex, diagnosis, stage, medications,
procedures, symptoms, and exclusions where relevant.

For joint document-and-question generation, create realistic trial summaries and
patient case reports with multiple facets. Do not seed generation with Nano
evaluation queries or positive passages. Useful hard negatives should share the
main disease but differ in severity, intervention, age group, comorbidity,
biomarker, or treatment phase.

## Example Data

| Query | Positive document |
| --- | --- |
| A 31 yo male with no significant past medical history presents with productive cough and chest pain. He reports developing cold symptoms one week ago that were improving until two days ago, when he developed a new fever, chil ... [truncated 225 chars](585 chars) | The objective of this study is to demonstrate the safety and efficacy of IC14 in the treatment of hospitalized patients with community-acquired pneumonia and sepsis. (165 chars) |
| A 48-year-old white male with history of common variable immunodeficiency (CVID) with acute abdominal pain, fever, dehydration, HR of 132 bpm, BP 80/40. The physical examination is remarkable for tenderness and positive Murph ... [truncated 225 chars](452 chars) | This study will try to identify mutations in the genes responsible for primary immunodeficiency disorders (inherited diseases of the immune system) and evaluate the course of these diseases in patients over time to learn more ... [truncated 225 chars](1420 chars) |
| A physician is called to see a 67-year-old woman who underwent cardiac catheterization via the right femoral artery earlier in the morning. She is now complaining of a cool right foot. Upon examination she has a pulsatile mas ... [truncated 225 chars](368 chars) | The purpose of this study is to assess the safety and feasibility of the 7F Ensure Medical Vascular Closure Devices to facilitate hemostasis in patients undergoing diagnostic or interventional coronary procedures using a stan ... [truncated 225 chars](1831 chars) |
| A 20 yo female college student with no significant past medical history presents with a chief complaint of fatigue. She reports increased sleep and appetite over the past few months as well as difficulty concentrating on her ... [truncated 225 chars](481 chars) | The current large randomized placebo-controlled trial is testing the ability of acupuncture to treat major depression. The study is unique in that treatment effects will be from the perspective of both Western psychiatry and ... [truncated 225 chars](1787 chars) |
| A 51-year-old woman is seen in clinic for advice on osteoporosis. She has a past medical history of significant hypertension and diet-controlled diabetes mellitus. She currently smokes 1 pack of cigarettes per day. She was do ... [truncated 225 chars](412 chars) | This study will assess whether treatment with black cohosh is effective in reducing the frequency and intensity of menopausal hot flashes. In addition, this study will determine whether or not black cohosh reduces the frequen ... [truncated 225 chars](1549 chars) |

## Dataset Information

| Field | Value |
| --- | --- |
| Nano set | NanoBIRCO |
| Backing dataset | NanoBIRCO |
| Task / split | NanoBIRCOClinicalTrial |
| Hugging Face dataset | [hakari-bench/NanoBIRCO](https://huggingface.co/datasets/hakari-bench/NanoBIRCO) |
| Language | en |
| Category | natural_language |
| Queries | 50 |
| Documents | 3,375 |
| Positive qrels | 1,042 |
| Positives per query | avg 20.84; min 1; median 15; max 68 |
| Multi-positive queries | 49 / 50 (98.00%) |
| BM25 nDCG@10 | 0.1194 |
| BM25 hit@10 | 0.6200 |
| Query length avg chars | 496.98 |
| Document length avg chars | 1174.34 |

### Public Sources

- [BIRCO: A Benchmark of Information Retrieval Tasks with Complex Objectives](https://arxiv.org/abs/2402.14151); 2024; Xiaoyue Wang, Jianyou Wang, Weili Cao, Kaicheng Wang, Ramamohan Paturi, Leon Bergen; DOI: `10.48550/arXiv.2402.14151`.
- [BIRCO GitHub repository](https://github.com/BIRCO-benchmark/BIRCO).

### Hugging Face Links

- Nano dataset: [hakari-bench/NanoBIRCO](https://huggingface.co/datasets/hakari-bench/NanoBIRCO)

### Source Reference Table

| Title | Year | Type | URL |
| --- | ---: | --- | --- |
| BIRCO: A Benchmark of Information Retrieval Tasks with Complex Objectives | 2024 | paper | https://arxiv.org/abs/2402.14151 |
| BIRCO GitHub repository |  | project repository | https://github.com/BIRCO-benchmark/BIRCO |

## Machine-Readable Metadata

<!-- benchmark-task-metadata:v1 -->

```yaml
benchmark_task_metadata:
  schema_version: 1
  document_status: first_pass
  nano_set: NanoBIRCO
  backing_dataset: NanoBIRCO
  dataset_id: hakari-bench/NanoBIRCO
  task_name: NanoBIRCOClinicalTrial
  split_name: NanoBIRCOClinicalTrial
  language: en
  category: natural_language
  document_path: docs/benchmark_tasks/NanoBIRCO/NanoBIRCOClinicalTrial.md
  source_research:
    primary_source_type: task_paper
    paper_pdf_or_html_checked: true
    no_paper_note: null
  counts:
    queries: 50
    documents: 3375
    positive_qrels: 1042
  positives_per_query:
    average: 20.84
    min: 1
    median: 15.0
    max: 68
    multi_positive_queries: 49
    multi_positive_query_percent: 98.0
  text_stats_chars:
    query_mean: 496.98
    document_mean: 1174.340148
  bm25:
    ndcg_at_10: 0.1193681048
    hit_at_10: 0.62
    source: dataset_bm25_column
  learning:
    original_train_split: available
    evaluation_split_origin: test
    train_eval_overlap_audit: not_audited
    leakage_note: prefer excluding BIRCO Clinical-Trial evaluation queries, candidate pools, and positive clinical trial descriptions from training data
    useful_training_data:
      - non-overlapping patient-to-clinical-trial matching pairs
      - clinical trial eligibility matching datasets
      - biomedical passage retrieval with patient criteria
      - diagnosis-matched hard negatives that fail other eligibility constraints
    synthetic_data:
      document_generation: clinical trial summaries with condition, intervention, inclusion context, exclusion context, and trial population
      question_generation: patient case reports with age, sex, diagnosis, symptoms, medications, comorbidities, tests, and procedures
      answerability: multiple trial passages may be relevant; positives should satisfy the patient condition and eligibility context
    multi_positive_training: preserve_multi_positive_trial_matching
  links:
    nano_dataset: https://huggingface.co/datasets/hakari-bench/NanoBIRCO
    source_urls:
      - label: BIRCO GitHub repository
        url: https://github.com/BIRCO-benchmark/BIRCO
    source_notes: []
  references:
    - title: 'BIRCO: A Benchmark of Information Retrieval Tasks with Complex Objectives'
      url: https://arxiv.org/abs/2402.14151
      year: 2024
      doi: 10.48550/arXiv.2402.14151
      is_paper: true
      source_confidence: definitive_paper_link
    - title: BIRCO GitHub repository
      url: https://github.com/BIRCO-benchmark/BIRCO
      year: null
      doi: null
      is_paper: false
      source_confidence: official_project_repository
```
