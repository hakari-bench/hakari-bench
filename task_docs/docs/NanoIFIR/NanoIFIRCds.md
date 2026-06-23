# NanoIFIR / NanoIFIRCds

## Overview

`NanoIFIRCds` is an English clinical decision support retrieval task in NanoIFIR. The queries describe patient cases and ask for diagnosis, treatment, or test information, while the documents are biomedical article abstracts or article-like records.

This task evaluates patient-vignette biomedical retrieval. A useful retriever must connect symptoms, demographics, test results, and the clinical question type to articles that can help a clinician answer the case-specific information need.

## Details

### What the Original Data Measures

IFIR uses TREC Clinical Decision Support as a healthcare subset, treating the clinical case summary and detailed description as the retrieval instruction. IFIR frames this setting as simulating a doctor retrieving healthcare-relevant passages for patient cases.

The TREC 2015 Clinical Decision Support track evaluates biomedical literature retrieval for generic clinical questions about diagnosis, testing, and treatment. It uses case narratives as idealized medical records and asks systems to retrieve biomedical articles that a physician might find useful.

### Observed Data Profile

This Nano split contains 42 queries, 10,000 documents, and 466 positive qrels. Queries have 11.10 positives on average, with a minimum of 1, a median of 9.0, and a maximum of 37. There are 38 multi-positive queries, or 90.48% of the split. Queries average 225.21 characters, and documents average 1,630.22 characters.

Observed queries describe cases such as a woman with sweaty hands, exophthalmia, and weight loss; an infant with postoperative decreased urine output and edema; a woman with arm pain and hypotension; a child with Kawasaki-like signs; and a woman with amenorrhea and elevated prolactin. Documents are biomedical titles and abstracts.

### BM25 Evaluation Profile

BM25 reaches nDCG@10 of 0.2258, hit@10 of 0.6905, and recall@100 of 0.3927 with a top-500 candidate pool. Lexical matching is helpful when symptoms, diseases, tests, or treatments appear directly in article abstracts.

The limitation is clinical reasoning. Relevant articles may discuss the diagnosis or treatment without repeating the full patient description. BM25 may also retrieve articles that share a symptom or disease term but answer the wrong clinical question type.

### Dense Evaluation Profile

The dense harrier-oss-270m profile reaches nDCG@10 of 0.4073, hit@10 of 0.8095, and recall@100 of 0.7124. Dense retrieval is clearly strongest across the main metrics.

This pattern indicates that embedding similarity helps map case descriptions to clinically useful literature. Dense retrieval can connect a vignette to disease, diagnostic, or treatment concepts even when the abstract does not share all symptoms exactly. It is especially valuable for multi-positive biomedical evidence retrieval.

### Reranking Hybrid Evaluation Profile

The reranking_hybrid candidate subset reaches nDCG@10 of 0.3376, hit@10 of 0.7619, and recall@100 of 0.6652. It uses 100 candidates per query, with three rank-101 safeguard positives.

Hybrid retrieval is strong but below dense retrieval on this task. This suggests that the dense model is better at capturing clinical semantic similarity than the lexical-heavy hybrid pool. The hybrid pool remains useful for reranking because it provides broad coverage and preserves biomedical term matches.

### Metric Interpretation for Model Researchers

`NanoIFIRCds` is a dense-favored clinical retrieval task. BM25 has reasonable hit rate, but dense retrieval substantially improves ranking and candidate coverage. This is a sign that clinical semantic matching matters more than exact term overlap.

Because most queries have many positives, recall@100 is important. nDCG@10 measures whether a model surfaces clinically useful evidence early enough for decision support. A strong reranker should improve the dense or hybrid candidate pool by distinguishing diagnosis, test, and treatment relevance.

### Query and Relevance Type Tendencies

Queries are short patient vignettes with age, sex, symptoms, tests, findings, and an explicit clinical question. Documents are biomedical abstracts or article records.

The relevance relation is clinical usefulness. A positive article may help diagnose the condition, choose a test, or guide treatment for the patient scenario.

### Representative Failure Modes

BM25 may focus on isolated symptoms and retrieve articles unrelated to the actual diagnosis or question type. Dense retrieval may retrieve clinically related disease literature but miss whether the query asks for diagnosis, treatment, or testing. Hybrid retrieval can still include articles that are medically topical but not patient-specific.

Multi-positive relevance also creates coverage risk: one retrieved article may be useful, but the full evidence set may include many diagnostic and therapeutic perspectives.

### Training Data That May Help

Useful training data includes non-overlapping TREC-CDS topics, PubMed and PMC clinical case retrieval, biomedical diagnosis/treatment/test retrieval data, and same-disease hard negatives with the wrong patient context or question type.

Training should exclude `NanoIFIRCds` queries, qrels, and positive biomedical articles.

### Model Improvement Notes

Improving this task requires biomedical semantic retrieval and clinical question-type awareness. Models should represent symptoms, demographics, lab findings, possible diagnoses, tests, and treatment intent.

For reranking, the model should assess whether an article is useful for the specific patient scenario, not just whether it mentions the same disease or symptom cluster.

## Example Data

| Query | Positive document |
| --- | --- |
| Given some infomation about patient.A 46-year-old woman with sweaty hands, exophthalmia, and weight... [100 / 162 chars] | Recognizing thyrotoxicosis in a patient with bipolar mania: a case report A thyroid stimulating hormone level is commonly measured in patients presenting with symptoms of mania in order to rule out an... [200 / 949 chars] |
| Given some infomation about patient.6-month-old male with decreased urine output and edema several h... [100 / 289 chars] | Serum cystatin C concentration as a marker of acute renal dysfunction in critically ill patients In critically ill patients sudden changes in glomerular filtration rate (GFR) are not instantly followe... [200 / 1,849 chars] |
| Given some infomation about patient.40-year-old woman with severe right arm pain and hypotension. Sh... [100 / 216 chars] | A simple statistical model for prediction of acute coronary syndrome in chest pain patients in the emergency department Several models for prediction of acute coronary syndrome (ACS) among chest pain... [200 / 1,449 chars] |
| Given some infomation about patient.2-year-old boy with fever and irritability for 5 days. Physical... [100 / 396 chars] | Behaviour sequelae following acute Kawasaki disease Kawasaki disease is a systemic vasculitis and may affect cerebral function acutely. The aim of the present study was to measure a number of behaviou... [200 / 1,803 chars] |
| Given some infomation about patient.31-year-old female with amenorrhea, milky nipple discharge, nega... [100 / 190 chars] | Prolactinomas, Cushing's disease and acromegaly: debating the role of medical therapy for secretory pituitary adenomas Pituitary adenomas are associated with a variety of clinical manifestations resul... [200 / 2,805 chars] |

### Source Reference Table

| Source | Role |
| --- | --- |
| [IFIR: A Comprehensive Benchmark for Evaluating Instruction-Following in Expert-Domain Information Retrieval](https://arxiv.org/abs/2503.04644) | Expert-domain instruction-following IR benchmark paper. |
| [Overview of the TREC 2015 Clinical Decision Support Track](https://trec.nist.gov/pubs/trec24/papers/Overview-CL.pdf) | Original clinical decision support retrieval overview. |
| [hakari-bench/NanoIFIR](https://huggingface.co/datasets/hakari-bench/NanoIFIR) | Nano benchmark dataset containing this split. |

### Representative Snippets

| Query Pattern | Positive Document Pattern |
| --- | --- |
| A patient vignette with sweaty hands, exophthalmia, and weight loss asking for diagnosis. | A biomedical case report or review involving thyrotoxicosis or thyroid-related presentation. |
| An infant with decreased urine output, edema, hypertension, high BUN and creatinine asking about renal dysfunction. | An abstract about acute renal dysfunction markers such as serum cystatin C. |
| A woman with severe arm pain and hypotension asking what tests should be received. | An article about predicting acute coronary syndrome or emergency diagnostic evaluation. |
| A child with fever, conjunctivitis, strawberry tongue, desquamation, and lab abnormalities. | An article about Kawasaki disease and clinical or behavioral sequelae. |
| A woman with amenorrhea, milky nipple discharge, negative pregnancy test, and high prolactin asking about treatment. | A review about prolactinomas or secretory pituitary adenoma medical therapy. |
