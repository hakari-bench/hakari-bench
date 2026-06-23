# NanoR2MED / NanoR2MEDIIYiClinical

## Overview

`NanoR2MEDIIYiClinical` is an English clinical case retrieval task from R2MED. The source records come from de-identified IIYi online consultation cases translated into English. Queries and documents are long structured patient records with chief complaint, present illness, history, examination, auxiliary findings, and treatment details. Relevance is driven by shared diagnosis or clinically useful case similarity, not by textbook passage matching. The split is difficult for both BM25 and dense retrieval, but dense and hybrid retrieval substantially improve over sparse matching.

## Details

### What the Original Data Measures

R2MED describes IIYi-Clinical as part of its clinical case retrieval setting. The benchmark paper reports using anonymized consultation records from multiple departments, applying de-identification and privacy-preserving processing, translating records into English, and grouping cases by diagnostic label.

In this task, one case becomes a query and other cases in the same diagnostic group form the relevant set. The retrieval problem is therefore case-to-case similarity under a latent diagnosis. A system must compare full clinical presentations rather than retrieve a textbook explanation.

### Observed Data Profile

The Nano split contains 129 queries, 10,000 documents, and 457 positive qrel rows. Queries average 2,584.10 characters, and documents average 5,042.31 characters. These are among the longest task texts in NanoR2MED.

Each query has 3.54 positives on average, with a median of 3 and a maximum of 6. Most queries are multi-positive: 114 of 129 queries, or 88.37%. Example cases include pregnancy complications with hypertension, cerebrovascular presentations with dizziness or limb weakness, gynecologic infection, post-abortion abdominal pain, and digestive or neurologic disease.

### BM25 Evaluation Profile

The BM25 candidate subset uses top-500 candidates and reaches nDCG@10 of 0.1482, hit@10 of 0.4109, and recall@100 of 0.4617. BM25 benefits from repeated section headings, symptoms, demographics, and measurements, but those signals are often distractors.

The core sparse-retrieval failure is that similar complaints do not necessarily mean the same diagnosis. A case can share abdominal pain, dizziness, pregnancy, discharge, or limb weakness while belonging to a different diagnostic group. BM25 sees surface overlap but has limited ability to infer the latent clinical condition.

### Dense Evaluation Profile

The dense candidate subset from `harrier_oss_v1_270m` uses top-500 candidates and reaches nDCG@10 of 0.1870, hit@10 of 0.4961, and recall@100 of 0.6674. Dense retrieval improves over BM25 on all reported metrics, especially recall@100. Embedding similarity better captures combinations of symptoms, history, and clinical context that point toward a diagnosis.

Even so, the absolute scores remain low. Long translated records contain many irrelevant details, and clinically similar cases may differ in wording, demographics, or treatment narrative. Dense models must learn diagnosis-level similarity rather than general patient-record similarity.

### Reranking Hybrid Evaluation Profile

The `reranking_hybrid` subset uses top-100 candidates, with 14 rows receiving the optional rank-101 safeguard. It reaches nDCG@10 of 0.1975, hit@10 of 0.5426, and recall@100 of 0.6674. Hybrid retrieval is the strongest top-rank profile and matches dense recall@100.

The improvement over dense nDCG and hit@10 suggests that sparse features still help once dense retrieval supplies broader clinical coverage. Hybrid retrieval can combine exact symptoms, measurements, and diagnostic vocabulary with semantic case similarity.

### Metric Interpretation for Model Researchers

This is a multi-positive clinical case task. nDCG@10 rewards ranking several diagnostically related cases early, hit@10 measures whether at least one related case appears in the first ten results, and recall@100 measures how much of the relevant case cluster is exposed to reranking.

For this split, BM25 is weak, dense retrieval is the stronger coverage baseline, and hybrid retrieval is the best early-ranking profile. Researchers should interpret success as diagnosis-aware case matching, not simple symptom matching.

### Query and Relevance Type Tendencies

Queries are long structured patient records. They include demographics, vital signs, symptom timelines, prior history, physical findings, imaging or lab tests, and treatment context. Relevant documents are other de-identified clinical cases that share the diagnosis or provide clinically similar support.

Relevance is latent. The positive case may not repeat all symptoms, and a near negative may share many symptoms while reflecting a different disease.

### Representative Failure Modes

Common failures include matching the same chief complaint but a different diagnosis, overvaluing shared age or pregnancy status, ranking records with similar abdominal or neurologic symptoms above same-diagnosis cases, and treating translated section boilerplate as meaningful evidence. Dense retrieval may cluster cases by broad specialty; BM25 may cluster by repeated symptoms.

### Training Data That May Help

Useful training data includes non-overlapping diagnosis-labeled clinical case retrieval, de-identified consultation case similarity pairs, translated or native-English clinical case retrieval, and hard negatives with similar chief complaints but different diagnoses. Evaluation queries, qrels, and positive translated case records should be excluded.

### Model Improvement Notes

Models should learn diagnosis-level similarity from full patient presentations. Multi-positive objectives are appropriate because most queries have several related cases. Hard negatives should share chief complaint, demographics, or department while differing in the final diagnosis or clinically decisive findings.

## Example Data

| Query | Positive document |
| --- | --- |
| [Chief Complaint]: A 28-year-old pregnant woman presents for evaluation. [Current Medical History]:... [100 / 2,601 chars] | [Case Presentation] Chief Complaint Female, 29 years old, office worker 36+1 weeks amenorrhea, headache with lower abdominal pain for 1 day Present Illness Pregnant woman, G1P0. The patient has a hist... [200 / 4,341 chars] |
| [Chief Complaint]: A 70-year-old male patient. Chief Reason: Intermittent dizziness and left upper l... [100 / 1,471 chars] | [Case Presentation] Chief Complaint Male, 69 years old, farmer Chief complaint: Dizziness, numbness and weakness in the right limb for 10 hours, admitted to the hospital. Current Medical History The p... [200 / 3,582 chars] |
| [Chief Complaint]: Male, 63 years old, farmer Admitted due to speech impairment and right-sided limb... [100 / 2,595 chars] | [Case Presentation] Chief Complaint Male, 75 years old, farmer Right limb movement restriction for 1 hour Present History The patient reports that 1 hour before admission, he suddenly developed sympto... [200 / 4,142 chars] |
| [Chief Complaint]: Increased vaginal discharge for 5 days, external genital itching for 1 day [Prese... [100 / 997 chars] | [Case Presentation] Chief Complaint Increased vaginal discharge with external genital pruritus for 3 days Present History The patient is usually in good health, with normal secretions. Three days ago,... [200 / 1,166 chars] |
| [Chief Complaint]: Abdominal pain for 3 days after abortion 7 days ago [Present Illness]: The patien... [100 / 1,069 chars] | [Case Presentation] Chief Complaint Female, 33, unemployed Lower abdominal pain for half a month Present History The patient is a married middle-aged female, G1P0, with a history of one induced aborti... [200 / 3,552 chars] |

### Source Reference Table

| Title | Year | Type | URL |
| --- | ---: | --- | --- |
| R2MED: A Benchmark for Reasoning-Driven Medical Retrieval | 2025 | arXiv paper | [https://arxiv.org/abs/2505.14558](https://arxiv.org/abs/2505.14558) |
| R2MED project page | 2025 | project page | [https://r2med.github.io/](https://r2med.github.io/) |
| R2MED GitHub repository | 2025 | source repository | [https://github.com/R2MED/R2MED](https://github.com/R2MED/R2MED) |
| R2MED/IIYi-Clinical | 2025 | dataset card | [https://huggingface.co/datasets/R2MED/IIYi-Clinical](https://huggingface.co/datasets/R2MED/IIYi-Clinical) |

### Representative Snippets

| Query | Relevant document excerpt |
| --- | --- |
| A pregnant patient presents with confusion, tachypnea, hypertension, and abnormal vital signs during late pregnancy. | A related case describes a pregnant patient at 36+1 weeks with headache, lower abdominal pain, and pregnancy history. |
| An older male patient has intermittent dizziness and limb numbness or weakness over several days. | A related case describes dizziness, numbness, and weakness in a limb with acute hospital admission. |
| A male patient presents with speech impairment and right-sided limb weakness for several hours. | A related case describes an older male patient with sudden right-limb movement restriction. |
| A patient reports increased vaginal discharge and external genital itching. | A related case describes increased vaginal discharge with external genital pruritus over several days. |
| A patient reports abdominal pain after a recent abortion. | A related case describes a female patient with lower abdominal pain and a history of induced abortion. |
