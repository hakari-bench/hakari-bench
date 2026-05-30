# NanoBIRCO / NanoBIRCOClinicalTrial

## Overview

NanoBIRCOClinicalTrial is a compact Nano task derived from BIRCO's clinical trial matching setting. Each query is a patient case report, and the corpus contains clinical trial descriptions. The retrieval goal is to find trials that fit the patient's condition, presentation, treatment context, and eligibility constraints. This makes the task useful for evaluating complex biomedical retrieval, patient-to-trial matching, eligibility reasoning, and multi-positive ranking.

## Details

### What the Original Data Measures

BIRCO was designed for retrieval tasks where relevance depends on complex objectives rather than simple semantic similarity. In the Clinical-Trial task, paragraph-length patient reports are matched to trial descriptions. A relevant trial should suit the patient's condition and recruitment context, not merely mention the same disease.

This task therefore requires constraint matching. The retriever must compare diagnosis, symptoms, age, sex, acuity, medications, procedures, comorbidities, and treatment phase with a trial's target population, intervention, inclusion setting, and exclusions. Disease-matched but unsuitable trials are natural hard negatives.

### Observed Data Profile

The task contains 50 queries, 3,375 documents, and 1,042 relevance judgments. It is strongly multi-positive, with an average of 20.84 positives per query. The minimum is 1, the median is 15.0, the maximum is 68, and 49 queries are multi-positive, or 98.0% of the set.

Queries average 496.98 characters, while documents average 1,174.34 characters. Queries are concise clinical vignettes with patient history and presentation. Documents are clinical trial summaries, usually describing study objective, disease area, intervention, and population. The task rewards ranking many suitable trials, not finding one canonical answer.

### BM25 Evaluation Profile

BM25 reaches nDCG@10 of 0.1322, hit@10 of 0.5800, and recall@100 of 0.2735 using the top-500 BM25 candidate subset. This is a difficult sparse baseline. Exact words can identify obvious disease areas, but eligibility often depends on related medical terminology or constraints that are not repeated verbatim.

The low recall@100 is important because almost every query has many positives. BM25 may retrieve one diagnosis-adjacent trial but miss many eligible alternatives. It can also rank trials that share symptoms or diseases while failing stage, intervention, age, acuity, or comorbidity constraints.

### Dense Evaluation Profile

The dense harrier-oss-270m run reaches nDCG@10 of 0.2152, hit@10 of 0.7400, and recall@100 of 0.4309. Dense retrieval is the strongest profile by nDCG@10 and recall@100. It improves substantially over BM25, showing that embedding similarity helps match patient descriptions to trial objectives beyond exact term overlap.

Even so, the absolute scores remain low. Patient-to-trial matching is a hard structured retrieval problem: suitable trials may share only some terms with the vignette, while many near misses are medically similar. Dense retrieval helps but does not fully model eligibility.

### Reranking Hybrid Evaluation Profile

The reranking_hybrid candidate set reaches nDCG@10 of 0.1959, hit@10 of 0.7600, and recall@100 of 0.3954. It uses a top-100 candidate range with an optional rank-101 safeguard; this slice has 1 safeguard row, candidate counts from 100 to 101, and a mean of 100.02 candidates. Hybrid has the best hit@10 but trails dense retrieval in nDCG@10 and recall@100.

This suggests that lexical anchors can help surface at least one suitable trial, while dense retrieval better covers the broader positive set. For downstream reranking, reranking_hybrid is useful but should be paired with eligibility-aware scoring to avoid disease-only matches.

### Metric Interpretation for Model Researchers

Because almost all queries have many positives, hit@10 is not enough. A system can find one loosely appropriate trial while missing most eligible trials. nDCG@10 measures whether the first page is densely populated with suitable studies, and recall@100 measures whether downstream ranking has enough trial candidates.

The comparison shows that BM25 is weak for this complex medical objective, dense retrieval is the best general first-stage profile, and hybrid retrieval improves first-hit visibility. This task is useful for testing whether retrievers can model clinical constraints rather than biomedical topicality alone.

### Query and Relevance Type Tendencies

Queries describe cases such as community-acquired pneumonia with sepsis, common variable immunodeficiency with abdominal symptoms, femoral artery catheterization complications, depression-like fatigue in a college student, and osteoporosis counseling with smoking and menopause context. Positive documents are clinical trials that match the condition or intervention setting.

The task rewards matching patient state to trial eligibility. Relevant trials may not repeat every symptom, but they should fit the core condition and recruitment context. Diagnosis-only matches are often insufficient.

### Representative Failure Modes

Likely failures include retrieving trials for the same disease but wrong stage, missing trials because the case uses a symptom description rather than a formal diagnosis, over-ranking general observational studies, and failing age, sex, treatment-status, or comorbidity constraints. BM25 may be too literal, while dense retrieval may be too broad without structured eligibility training.

### Training Data That May Help

Useful training data includes non-overlapping patient-to-clinical-trial matching pairs, clinical trial eligibility datasets, ClinicalTrials.gov summaries paired with patient vignettes, biomedical retrieval with patient criteria, and hard negatives that match diagnosis but fail other constraints. Multi-positive training should be preserved.

### Model Improvement Notes

A model targeting this task should encode clinical constraints explicitly. Sparse systems need medical synonym expansion and field-aware trial indexing. Dense systems need patient-trial contrastive training with diagnosis-matched hard negatives. Hybrid systems can help first-hit coverage but need downstream eligibility-aware reranking for strong top-10 quality.

## Example Data

### Public Sources

The original task is based on BIRCO's complex-objective retrieval benchmark, with NanoBIRCO providing the compact dataset packaging.

### Source Reference Table

| Item | Reference |
| --- | --- |
| Original benchmark paper | [BIRCO](https://arxiv.org/abs/2402.14151) |
| Project repository | [BIRCO GitHub repository](https://github.com/BIRCO-benchmark/BIRCO) |
| NanoBIRCO dataset | [hakari-bench/NanoBIRCO](https://huggingface.co/datasets/hakari-bench/NanoBIRCO) |

Representative query and positive trial snippets:

| Query | Positive document snippet |
| --- | --- |
| A 31-year-old male presents with productive cough, chest pain, fever, chills, and sepsis-like signs. | A study tests the safety and efficacy of IC14 in hospitalized patients with community-acquired pneumonia and sepsis. |
| A 48-year-old male with common variable immunodeficiency presents with abdominal pain, fever, and dehydration. | A study identifies mutations responsible for primary immunodeficiency disorders and follows patients over time. |
| A 67-year-old woman has a cool right foot after right femoral artery catheterization. | A study assesses vascular closure devices for hemostasis after coronary procedures using femoral access. |
| A 20-year-old college student has fatigue, increased sleep and appetite, and difficulty concentrating. | A randomized trial tests acupuncture for treatment of major depression. |
| A 51-year-old woman asks for osteoporosis advice with hypertension, diabetes, smoking, and menopause history. | A study assesses whether black cohosh reduces menopausal hot flashes and related symptoms. |
