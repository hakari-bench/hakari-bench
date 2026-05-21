# NanoR2MED / NanoR2MEDMedXpertQAExam

## Overview

R2MED's MedXpertQA-Exam task covers examination recommendation: complex
MedXpertQA patient vignettes are reformulated as open-ended questions, and the
corpus comes from Wikipedia-style medical passages sampled from MedCorp. In the
Nano split, queries include comorbidities, vital signs, medication history, and
exam findings, while relevant passages describe diagnostic tests, clinical
instruments, imaging, laboratory findings, or disease entities. Retrieval
therefore requires inferring the appropriate examination from the vignette
before matching evidence text.

## Details

### What the Original Data Measures

[R2MED: A Benchmark for Reasoning-Driven Medical Retrieval](https://arxiv.org/abs/2505.14558)
states that the clinical evidence retrieval task covers examination
recommendation, diagnosis, and treatment planning. For MedXpertQA-Exam, R2MED
uses MedXpertQA questions as the query source and samples documents from the
Wikipedia subset of MedCorp.

The paper describes a multi-stage construction pipeline: GPT-4o classifies the
question intent, rule-based filtering removes shallow or ambiguous examples,
small instruction models filter out questions that are too easy, and GPT-4o
reformulates selected multiple-choice items into open-ended questions. Candidate
documents are then mined from query, answer, and reasoning-path views and
reviewed for relevance and clinical support.

### Observed Data Profile

The Nano split has 97 queries, 10,000 documents, and 292 positive qrels. Queries
average 928.44 characters and are long patient vignettes with comorbidities,
vital signs, medication history, or examination findings. Documents average
723.85 characters and are Wikipedia-style passages about diagnostic tests,
clinical instruments, imaging, laboratory findings, or disease entities.

Each query has 3.01 positives on average, with a median of 3 and a maximum of
8 positives. Sampled positives include PHQ-9 depression screening, barium
swallow, serum albumin testing, pelvic ultrasound, and serum/urine copper
testing. Many queries require inferring the test target before retrieving the
document, so direct symptom overlap is often weak.

### BM25 Difficulty

Using the dataset-provided BM25 candidate column, BM25 reaches nDCG@10 = 0.0245
and hit@10 = 0.0722. It ranks only 2 positives first and finds a positive inside
the top 10 for 7 of 97 queries. This is an extremely difficult sparse baseline.

Observed failures include renal-colic cases where BM25 retrieves reflux pages
before renal ultrasonography, hypoglycemia presentations where irrelevant
biographical text ranks first, and carotid/vision-loss or osteoporosis screening
cases where surface vocabulary does not identify the desired examination. Strong
retrieval likely needs diagnosis or examination inference before matching.

### Training Data That May Help

Useful training data includes non-overlapping MedXpertQA or similar expert exam
questions paired with diagnostic-test evidence, clinical examination
recommendation datasets, medical entity linking from vignettes to tests, and
Wikipedia medical section retrieval with hard negatives from similar symptoms.
Training should preserve multiple positives when available.

Do not train on the R2MED MedXpertQA-Exam evaluation queries, qrels, or positive
Wikipedia passages. If using MedXpertQA directly, check that the same questions
or reformulations are not reused in the evaluation split.

### Synthetic Data Guidance

For document-to-question generation, use non-evaluation Wikipedia or medical
reference sections about diagnostic tests, laboratory studies, imaging, or
screening instruments. Generate patient vignettes where the best next test is
grounded in the document.

For joint generation, create a medical examination passage and a realistic
exam-style vignette with symptoms, history, and confounders. Hard negatives
should share disease or symptom vocabulary but describe a different test. Do not
seed generation with Nano evaluation queries or positives.

## Example Data

| Query | Positive document |
| --- | --- |
| A 27-year-old male presents with anxiety and ongoing moodiness, citing stress at home and work. His medical history includes chronic gastritis previously treated for *Helicobacter pylori*, chronic pyelonephritis with kidney s ... [truncated 225 chars](703 chars) | Applications The National Institute for Health and Clinical Excellence endorsed the PHQ-9 for measuring depression severity and responsiveness to treatment in adults in a primary care setting. The Behavioral Risk Factor Surve ... [truncated 225 chars](865 chars) |
| A 65-year-old woman presents with an 8-month history of progressive difficulty swallowing food and retrosternal chest discomfort. She describes a sensation of “food getting stuck” in her throat and occasionally hears a “gurgl ... [truncated 225 chars](954 chars) | Procedure Clinical status and relevant medical history are reviewed prior to the studies. Patient consent is required. Barium swallow A barium swallow study is also known as a barium esophagram and needs little if any prepara ... [truncated 225 chars](787 chars) |
| A 27-year-old primigravida at 33 weeks gestation visits her primary care physician with concerns about generalized swelling in her ankles and legs. Her medical history is significant for diabetes and obesity. Her vital signs ... [truncated 225 chars](489 chars) | Immune factors may also play a role. Diagnosis Testing for pre-eclampsia is recommended throughout pregnancy via measuring a woman's blood pressure. Diagnostic criteria Pre-eclampsia is diagnosed when a pregnant woman develop ... [truncated 225 chars](902 chars) |
| A 43-year-old female daycare teacher seeks medical attention for one month of fatigue and lightheadedness. She has diabetes managed with metformin and reports increasingly heavy menstrual periods over the past year. She also ... [truncated 225 chars](675 chars) | Diagnosis The presence of a uterine fibroid versus an adnexal tumor is made. Fibroids can be mistaken for ovarian neoplasms. An uncommon tumor which may be mistaken for a fibroid is Sarcoma botryoides. It is more common in ch ... [truncated 225 chars](890 chars) |
| A 14-year-old girl with no notable medical history reports having intermittent mild pain in her upper right abdomen for the past 2 months. Her father notes that her appetite has been diminished but that her abdominal discomfo ... [truncated 225 chars](2334 chars) | Hereditary hemochromatosis usually presents with a family history of cirrhosis, skin hyperpigmentation, diabetes mellitus, pseudogout, or cardiomyopathy, all due to signs of iron overload. Wilson's disease is an autosomal rec ... [truncated 225 chars](929 chars) |

## Dataset Information

| Field | Value |
| --- | --- |
| Nano set | NanoR2MED |
| Backing dataset | NanoR2MED |
| Task / split | NanoR2MEDMedXpertQAExam |
| Hugging Face dataset | [hakari-bench/NanoR2MED](https://huggingface.co/datasets/hakari-bench/NanoR2MED) |
| Language | en |
| Category | natural_language |
| Queries | 97 |
| Documents | 10,000 |
| Positive qrels | 292 |
| Avg positives / query | 3.01 |
| Positives per query (min / median / max) | 1 / 3 / 8 |
| Queries with multiple positives | 74 (76.29%) |
| BM25 nDCG@10 | 0.0245 |
| BM25 hit@10 | 0.0722 |
| Query length avg chars | 928.44 |
| Document length avg chars | 723.85 |

### Public Sources

- [R2MED: A Benchmark for Reasoning-Driven Medical Retrieval](https://arxiv.org/abs/2505.14558); 2025; Xiangxu Zhang, Lei Li, Xiao Zhou, and Zheng Liu; DOI: `10.48550/arXiv.2505.14558`.
- [R2MED project page](https://r2med.github.io/).
- [R2MED GitHub repository](https://github.com/R2MED/R2MED).
- [R2MED/MedXpertQA-Exam dataset card](https://huggingface.co/datasets/R2MED/MedXpertQA-Exam).

### Hugging Face Links

- Nano dataset: [hakari-bench/NanoR2MED](https://huggingface.co/datasets/hakari-bench/NanoR2MED)
- Source dataset: [R2MED/MedXpertQA-Exam](https://huggingface.co/datasets/R2MED/MedXpertQA-Exam)

### Source Reference Table

| Title | Year | Type | URL |
| --- | ---: | --- | --- |
| R2MED: A Benchmark for Reasoning-Driven Medical Retrieval | 2025 | arXiv paper | https://arxiv.org/abs/2505.14558 |
| R2MED project page | 2025 | project page | https://r2med.github.io/ |
| R2MED GitHub repository | 2025 | source repository | https://github.com/R2MED/R2MED |
| R2MED/MedXpertQA-Exam | 2025 | dataset card | https://huggingface.co/datasets/R2MED/MedXpertQA-Exam |

## Machine-Readable Metadata

<!-- benchmark-task-metadata:v1 -->

```yaml
benchmark_task_metadata:
  schema_version: 1
  document_status: first_pass
  nano_set: NanoR2MED
  backing_dataset: NanoR2MED
  dataset_id: hakari-bench/NanoR2MED
  task_name: NanoR2MEDMedXpertQAExam
  split_name: NanoR2MEDMedXpertQAExam
  language: en
  category: natural_language
  document_path: docs/benchmark_tasks/NanoR2MED/NanoR2MEDMedXpertQAExam.md
  source_research:
    primary_source_type: benchmark_paper
    paper_pdf_or_html_checked: true
    paper_url: https://arxiv.org/abs/2505.14558
    additional_source_urls:
      - https://r2med.github.io/
      - https://github.com/R2MED/R2MED
      - https://huggingface.co/datasets/R2MED/MedXpertQA-Exam
  counts:
    queries: 97
    documents: 10000
    positive_qrels: 292
  positives_per_query:
    average: 3.0103092784
    min: 1
    median: 3.0
    max: 8
    multi_positive_queries: 74
    multi_positive_query_percent: 76.29
  text_stats_chars:
    query_mean: 928.443299
    document_mean: 723.8511
  bm25:
    ndcg_at_10: 0.0244625982
    hit_at_10: 0.0721649485
    source: dataset_bm25_column
  learning:
    original_train_split: not_found
    evaluation_split_origin: R2MED benchmark release sampled into NanoR2MED
    train_eval_overlap_audit: not_audited
    leakage_note: exclude R2MED MedXpertQA-Exam evaluation queries, qrels, and positive Wikipedia passages
    useful_training_data:
      - non-overlapping expert medical exam questions paired with test evidence
      - clinical examination recommendation retrieval
      - medical entity linking from vignettes to diagnostic tests
      - hard negatives from similar symptoms with different tests
    synthetic_data:
      document_generation: non-evaluation medical reference sections about diagnostic tests, imaging, labs, or screening instruments
      question_generation: patient vignettes asking for the best examination or test
      hard_negatives: same disease or symptom vocabulary but different diagnostic procedure
      answerability: the passage should justify the inferred examination recommendation
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
      - label: R2MED/MedXpertQA-Exam
        url: https://huggingface.co/datasets/R2MED/MedXpertQA-Exam
    source_notes: []
  references:
    - title: "R2MED: A Benchmark for Reasoning-Driven Medical Retrieval"
      url: https://arxiv.org/abs/2505.14558
      year: 2025
      doi: 10.48550/arXiv.2505.14558
      is_paper: true
      source_confidence: definitive_paper_link
```
