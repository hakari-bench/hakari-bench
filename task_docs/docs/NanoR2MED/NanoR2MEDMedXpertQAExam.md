# NanoR2MED / NanoR2MEDMedXpertQAExam

## Overview

`NanoR2MEDMedXpertQAExam` is an English clinical evidence retrieval task from R2MED focused on examination recommendation. Queries are complex MedXpertQA-style patient vignettes, and documents are Wikipedia-style medical passages from MedCorp. Relevant passages justify the diagnostic test, imaging study, screening instrument, or laboratory examination implied by the case. The task is extremely hard for BM25 because the query rarely names the desired test directly. Dense retrieval is the strongest observed profile, while the hybrid pool improves over BM25 but does not match dense top-rank quality.

## Details

### What the Original Data Measures

R2MED defines clinical evidence retrieval as retrieving authoritative medical evidence for examination recommendation, diagnosis, and treatment planning. MedXpertQA-Exam uses expert medical exam questions as the source and reformulates selected multiple-choice items into open-ended retrieval queries.

The construction pipeline classifies question intent, filters shallow or ambiguous items, reformulates them into open-ended questions, mines candidate evidence from query, answer, and reasoning-path views, and assesses relevance to both the answer and the reasoning process.

### Observed Data Profile

The Nano split contains 97 queries, 10,000 documents, and 292 positive qrel rows. Queries average 928.44 characters and often include comorbidities, vital signs, medication history, physical findings, or diagnostic clues. Documents average 723.85 characters.

Each query has 3.01 positives on average, with a median of 3 and a maximum of 8. Multi-positive queries account for 74 of 97 queries, or 76.29%. Representative positives include PHQ-9 depression screening, barium swallow, pre-eclampsia testing, fibroid diagnosis, and copper testing for Wilson disease.

### BM25 Evaluation Profile

The BM25 candidate subset uses top-500 candidates and reaches nDCG@10 of 0.0277, hit@10 of 0.0825, and recall@100 of 0.1678. This is an extremely weak sparse baseline. The vignette may describe symptoms, risk factors, or context while the relevant passage names the examination or diagnostic procedure.

BM25 therefore tends to match incidental disease or symptom words rather than the best test. In this split, exact term frequency is rarely enough unless the query already names the examination.

### Dense Evaluation Profile

The dense candidate subset from `harrier_oss_v1_270m` uses top-500 candidates and reaches nDCG@10 of 0.1599, hit@10 of 0.4021, and recall@100 of 0.4144. Dense retrieval improves sharply over BM25. Embedding similarity can connect a vignette to the clinical concept, disease, or test category that the relevant passage describes.

Dense retrieval is the strongest profile for this task. The absolute scores remain modest because the model must infer the recommended examination before retrieving evidence, and several distractor passages can share the same symptoms or disease vocabulary.

### Reranking Hybrid Evaluation Profile

The `reranking_hybrid` subset uses top-100 candidates, with 33 rows receiving the optional rank-101 safeguard. It reaches nDCG@10 of 0.0979, hit@10 of 0.2577, and recall@100 of 0.3699. Hybrid retrieval is much better than BM25 but worse than dense retrieval on every reported metric.

This indicates that BM25 contributes some exact clinical anchors, but sparse candidates can dilute the semantic signal for an examination-inference task. For reranking, dense top-500 coverage is the stronger starting point, while hybrid candidates may still supply occasional exact-test matches.

### Metric Interpretation for Model Researchers

This is a multi-positive evidence retrieval task. nDCG@10 rewards ranking several relevant test-support passages early, hit@10 measures whether any supporting evidence appears in the first ten results, and recall@100 measures candidate availability for reranking.

For MedXpertQA-Exam, dense retrieval is the clear baseline to beat. Improvements should show that the model can infer a diagnostic test from a patient vignette rather than merely match symptoms or disease names.

### Query and Relevance Type Tendencies

Queries are long exam-style clinical vignettes. They may imply a psychiatric screen, barium swallow, pregnancy-related test, pelvic ultrasound, liver or copper study, imaging modality, or other diagnostic procedure. Relevant documents explain the examination, its application, or the disease context that motivates it.

Relevance is reasoning-based. A passage is useful when it justifies the examination recommendation, even if the query never uses the test name.

### Representative Failure Modes

Failures include retrieving disease pages without the requested diagnostic procedure, matching symptoms with the wrong test, ranking broad medical topics above a specific screening instrument, and missing the latent test when the vignette contains many comorbidities. BM25 is especially weak; dense retrieval may still confuse tests used for adjacent diseases.

### Training Data That May Help

Useful training data includes non-overlapping expert medical exam questions paired with test evidence, clinical examination recommendation retrieval, medical entity linking from vignettes to diagnostic tests, and hard negatives from similar symptoms with different tests. Evaluation queries, qrels, and positive Wikipedia passages should be excluded.

### Model Improvement Notes

Models should learn to infer the test target from clinical clues and retrieve passages about the corresponding examination. Multi-positive objectives are useful because more than one passage can justify the recommendation. Hard negatives should share symptoms, disease vocabulary, or body system but describe a different diagnostic procedure.

## Example Data

| Query | Positive document |
| --- | --- |
| A 27-year-old male presents with anxiety and ongoing moodiness, citing stress at home and work. His medical history includes chronic gastritis previously treated for *Helicobacter pylori*, chronic pyelonephritis with kidney stones, and stage 1 chronic kidney disease. He also has an 8-year smoking history and has unsuccessfully attempted to quit using nicotine patches, experiencing recurrent anxiety during those attempts. His grandfather, a heavy smoker, recently passed away from metastatic lung... [500 / 703 chars] | Applications The National Institute for Health and Clinical Excellence endorsed the PHQ-9 for measuring depression severity and responsiveness to treatment in adults in a primary care setting. The Behavioral Risk Factor Surveillance Survey (BRFSS), the National Health and Nutrition Examination Survey, the Medical Expenditure Panel Survey, the National Epidemiologic Survey on Alcohol and Related Conditions, the Medicare Health Support program, and the Millennium Cohort Study use the full PHQ-9 or a shortened form of it. The Veterans Administration, Department of Defense, and Kaiser Permanente adopted the PHQ-9 as a standard measure for depression screening. The PHQ-9 is also the most commonly used depression measure in the United Kingdom's National Health Service, which requires providers to use a depression screening instrument when treating depression. [865 chars] |
| A 65-year-old woman presents with an 8-month history of progressive difficulty swallowing food and retrosternal chest discomfort. She describes a sensation of “food getting stuck” in her throat and occasionally hears a “gurgling sound” while eating. She has also experienced episodes of coughing up undigested food, along with a bad taste in her mouth and bad breath. She denies fever or weight loss. Her medical history includes Raynaud disease treated with nifedipine, and she has traveled to Mexic... [500 / 954 chars] | Procedure Clinical status and relevant medical history are reviewed prior to the studies. Patient consent is required. Barium swallow A barium swallow study is also known as a barium esophagram and needs little if any preparations for the study of the larynx, pharynx, and esophagus when studied alone. A thick barium mixture is swallowed in supine position and fluoroscopic images of the swallowing process are made. Then several swallows of a thin barium mixture are taken and the passage is recorded by fluoroscopy and standard radiographs. The procedure is repeated several times with the examination table tilted at various angles. A total of 350-450 mL of barium is swallowed during the process. Normally, 90% of ingested fluid should have passed into the stomach after 15 seconds. [787 chars] |
| A 27-year-old primigravida at 33 weeks gestation visits her primary care physician with concerns about generalized swelling in her ankles and legs. Her medical history is significant for diabetes and obesity. Her vital signs show: temperature 98.5°F (36.9°C), blood pressure 147/92 mmHg, heart rate 80/min, respiratory rate 15/min, and oxygen saturation 97% on room air. Physical examination reveals bilateral lower extremity edema. What is the most appropriate initial step in management? [489 chars] | Immune factors may also play a role. Diagnosis Testing for pre-eclampsia is recommended throughout pregnancy via measuring a woman's blood pressure. Diagnostic criteria Pre-eclampsia is diagnosed when a pregnant woman develops: Blood pressure ≥140 mmHg systolic or ≥90 mmHg diastolic on two separate readings taken at least four to six hours apart after 20 weeks' gestation in an individual with previously normal blood pressure. In a woman with essential hypertension beginning before 20 weeks' gestational age, the diagnostic criteria are an increase in systolic blood pressure (SBP) of ≥30 mmHg or an increase in diastolic blood pressure (DBP) of ≥15 mmHg. Proteinuria ≥ or more of protein in a 24-hour urine sample or a SPOT urinary protein to creatinine ratio ≥0.3 or a urine dipstick reading of 1+ or greater (dipstick reading should only be used if other quantitative methods are not available). [902 chars] |

### Source Reference Table

| Title | Year | Type | URL |
| --- | ---: | --- | --- |
| R2MED: A Benchmark for Reasoning-Driven Medical Retrieval | 2025 | arXiv paper | [https://arxiv.org/abs/2505.14558](https://arxiv.org/abs/2505.14558) |
| R2MED project page | 2025 | project page | [https://r2med.github.io/](https://r2med.github.io/) |
| R2MED GitHub repository | 2025 | source repository | [https://github.com/R2MED/R2MED](https://github.com/R2MED/R2MED) |
| R2MED/MedXpertQA-Exam | 2025 | dataset card | [https://huggingface.co/datasets/R2MED/MedXpertQA-Exam](https://huggingface.co/datasets/R2MED/MedXpertQA-Exam) |

### Representative Snippets

| Query | Relevant document excerpt |
| --- | --- |
| A young male with anxiety, mood symptoms, stress, and a complex medical history needs the appropriate assessment. | A passage describes PHQ-9 applications for measuring depression severity and responsiveness to treatment. |
| An older woman has progressive dysphagia, chest discomfort, and food-sticking sensation. | A passage describes barium swallow or barium esophagram procedure and preparation. |
| A pregnant patient has edema, diabetes, obesity, and abnormal findings concerning for hypertensive disease. | A passage describes testing and diagnostic criteria for pre-eclampsia during pregnancy. |
| A woman with fatigue, lightheadedness, diabetes, and heavy menstrual periods requires evaluation of a pelvic cause. | A passage discusses diagnosis of uterine fibroid versus adnexal tumor and related imaging context. |
| A teenage girl has upper-right abdominal pain and features suggesting a metabolic liver disorder. | A passage discusses hereditary hemochromatosis and Wilson disease, including clinical presentation and testing context. |
