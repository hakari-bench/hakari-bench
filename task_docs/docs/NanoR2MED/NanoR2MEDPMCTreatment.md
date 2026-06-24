# NanoR2MED / NanoR2MEDPMCTreatment

## Overview

`NanoR2MEDPMCTreatment` is an English clinical evidence retrieval task from R2MED focused on treatment planning. Queries are long structured clinical case summaries, and documents are PubMed Central passages that support treatment or management reasoning. Each query can have multiple positives. The task requires retrieving evidence for a management decision rather than simply matching diagnosis words. Dense retrieval improves strongly over BM25, while `reranking_hybrid` gives the highest hit@10 and recall@100 but slightly lower nDCG@10 than dense retrieval.

## Details

### What the Original Data Measures

R2MED describes PMC-Treatment as a clinical evidence retrieval dataset. The source question set comes from MedRBench_Treat, and R2MED uses associated PubMed Central article content as positive evidence. Additional PMC Open Access case reports are used to form a challenging negative corpus.

The relevance pipeline judges whether documents support both the answer and reasoning path for a treatment decision. As a result, positives may provide background evidence, treatment mechanism, procedure rationale, or management context rather than a direct answer sentence.

### Observed Data Profile

The Nano split contains 150 queries, 10,000 documents, and 315 positive qrel rows. Queries average 1,755.83 characters and include demographics, chief complaint, history, tests, diagnosis, management, and outcome. Documents average 726.63 characters.

Each query has 2.10 positives on average, with a median of 2 and a maximum of 5. Multi-positive queries account for 77 of 150 queries, or 51.33%. Examples include daratumumab for plasma-cell depletion, renal denervation for resistant hypertension, Taussig-Bing anomaly, endovascular aortic repair, and surgical reconstruction for ocular surface burns.

### BM25 Evaluation Profile

The BM25 candidate subset uses top-500 candidates and reaches nDCG@10 of 0.2580, hit@10 of 0.4933, and recall@100 of 0.5048. BM25 is useful when query and evidence share disease names, drug names, procedures, or treatment vocabulary.

The task remains difficult for sparse retrieval because treatment reasoning often depends on why a therapy, procedure, or management path is appropriate. Long case summaries also contain many distractor terms, and surface overlap may retrieve general case-report text rather than the evidence supporting the specific management decision.

### Dense Evaluation Profile

The dense candidate subset from `harrier_oss_v1_270m` uses top-500 candidates and reaches nDCG@10 of 0.3801, hit@10 of 0.6133, and recall@100 of 0.6413. Dense retrieval is substantially stronger than BM25 on all reported metrics. Embedding similarity helps bridge from a structured case summary to evidence about treatment mechanism or procedure rationale.

Dense retrieval is the best nDCG@10 profile, suggesting that it places highly relevant treatment evidence earlier when it finds it.

### Reranking Hybrid Evaluation Profile

The `reranking_hybrid` subset uses top-100 candidates, with 23 rows receiving the optional rank-101 safeguard. It reaches nDCG@10 of 0.3555, hit@10 of 0.6667, and recall@100 of 0.6984. Hybrid retrieval improves hit@10 and recall@100 over dense retrieval but has lower nDCG@10.

This means hybrid search is a stronger coverage pool for reranking, while dense retrieval provides better ordering among the top results. The hybrid pool is valuable when a sparse treatment term or procedure name recovers evidence that dense retrieval ranks lower.

### Metric Interpretation for Model Researchers

This is a multi-positive treatment-evidence task. nDCG@10 rewards early ranking of multiple supporting passages, hit@10 measures whether any treatment-supporting evidence appears in the first ten results, and recall@100 measures how much of the evidence set is available to a reranker.

For PMC-Treatment, dense retrieval is the strongest ranking baseline, while hybrid retrieval is the stronger coverage-oriented candidate pool. Strong models should infer the treatment decision and retrieve evidence for the clinical management rationale.

### Query and Relevance Type Tendencies

Queries are structured treatment-planning cases with diagnosis, tests, management, and outcomes. Relevant documents are PMC passages about therapies, procedures, mechanisms, complications, or treatment context. Positives may support a treatment decision indirectly.

Relevance is management-supporting. A document is useful if it justifies or contextualizes the treatment reasoning, not merely because it mentions the same disease.

### Representative Failure Modes

Common failures include retrieving general treatment commentary instead of evidence for the specific therapy, matching the same disease but a different management implication, selecting case reports with shared drug vocabulary but unrelated reasoning, and missing mechanism passages when the query is long and noisy. BM25 is vulnerable to treatment-word overlap; dense retrieval can still confuse adjacent therapies.

### Training Data That May Help

Useful training data includes non-overlapping treatment-planning medical QA, clinical case-to-evidence retrieval, PubMed Central treatment and case-report retrieval, and hard negatives with the same disease but different treatment decisions. Evaluation queries, qrels, and positive PMC passages should be excluded.

### Model Improvement Notes

Models should learn to identify the management decision latent in a case and retrieve evidence that supports that decision. Multi-positive objectives are useful because several passages may support one treatment plan. Hard negatives should share disease and treatment vocabulary while implying a different procedure, drug, complication, or management path.

## Example Data

| Query | Positive document |
| --- | --- |
| Case Summary: - **Patient Demographics:** 43-year-old male - **Chief Complaint:** Unexplained edema of the eyelids and lower limbs - **History of Present Illness:** Progressive edema without hematuria. Proteinuria measured at 4446.7 mg/g by urine protein-creatinine ratio. Serum creatinine was elevated at 126 μmol/L. Elevated serum free kappa and lambda light chains with a normal ratio. Diagnosed with nephrotic syndrome after clinical evaluation. - **Past Medical History:** No detailed past medic... [500 / 2,067 chars] | Daratumumab is an antibody against CD38 used for plasma cell depletion in relapsed or refractory multiple myeloma (MM). It mediates depletion of plasma cells, which overexpress CD38, through a wide range of mechanisms including complement- and antibody-mediated cytotoxicity, Fcy receptor-dependent apoptosis, and modulating immune cell composition [11]. Zand et al. conducted the first clinical trial to explore daratumumab as a treatment in PGNMID, including in treatment-naive disease. Of the 10 PGNMID patients who received daratumumab, 4 entered complete remission (urine protein creatinine ratio < 500 mg/day and eGFR decline < 15%), and 6 had partial remission (at least 50% reduction in baseline proteinuria and eGFR decline < 30%) by 12 months after treatment. Three patients relapsed with partial response after re-initiation of daratumumab. Most patients had obvious reduction in proteinuria by one month after their inaugural infusion [12]. [952 chars] |
| Case Summary: - Patient Demographics: 43-year-old male - Chief Complaint: Long-standing therapy-resistant hypertension refractory to maximal medical therapy with symptoms including agitation, headaches, chest pain, sweating, and epistaxis, mandated frequent hospitalizations for intravenous therapy due to hypertensive crises. - History of Present Illness: Hypertension since age 18 progressively worsened over the years despite increasing pharmacological interventions. Currently on a 9-component ma... [500 / 1,404 chars] | While the observed 24 hours systolic ambulatory BD reduction at 6-months follow-up in contemporary trials such as SPYRAL ON MED is generally considered to be modest (−1.9 mmHg),6 it seems that the observed treatment effect in our patient was much more pronounced. Previous studies showed that the density of orthosympathetic nerves increases progressively with increasing distance from the ostium. Additionally, in a percutaneous approach the nerves that are located at the outer border of the vessel may be incompletely targeted. Therefore, it seems plausible that a surgical approach would result in more profound and more complete orthosympathetic denervation.5 [664 chars] |
| Case Summary: - **Patient Demographics:** 2-day-old male neonate - **Chief Complaint:** Central cyanosis and poor breastfeeding following birth - **History of Present Illness:** - Neonate presented with central cyanosis and poor feeding shortly after birth. - Diagnosed with Taussig Bing anomaly (TBA) combined with pulmonary artery and pulmonary valve stenosis through investigations including electrocardiogram, chest X-rays, and echocardiography by 3 months of age. - Temporary palliative Blalock-... [500 / 2,145 chars] | Helen B. Taussig and Richard J. Bing were the first to describe a rare cyanotic congenital heart defect known as the Taussig-Bing anomaly (TBA) in 1949, that includes a non-restrictive subpulmonary ventricular septal defect (VSD) and a double outlet right ventricle (DORV) [8]. TBA is the third most prevalent type of DORV [8]. TBA is characterized by a bilateral conus and the absence of pulmonary-mitral fibrous continuity, distinguishing it from a transposition of the great arteries (TGA) with VSD [8]. TBA is a complex cardiac anomaly; in addition to its primary features, it may be associated with malformations involving the aortic arch, coronary arteries, right ventricle, and subaortic area [2]. A clinical symptom of TBA is cyanosis caused by hypoxia due to a small volume of blood flowing from the left ventricle through the aorta [1]. Increasing pulmonary blood flow, early onset of pulmonary vascular disease, pulmonary hypertension, and heart failure are complications of left-to-right... [1,000 / 2,503 chars] |

### Source Reference Table

| Title | Year | Type | URL |
| --- | ---: | --- | --- |
| R2MED: A Benchmark for Reasoning-Driven Medical Retrieval | 2025 | arXiv paper | [https://arxiv.org/abs/2505.14558](https://arxiv.org/abs/2505.14558) |
| R2MED project page | 2025 | project page | [https://r2med.github.io/](https://r2med.github.io/) |
| R2MED GitHub repository | 2025 | source repository | [https://github.com/R2MED/R2MED](https://github.com/R2MED/R2MED) |
| R2MED/PMC-Treatment | 2025 | dataset card | [https://huggingface.co/datasets/R2MED/PMC-Treatment](https://huggingface.co/datasets/R2MED/PMC-Treatment) |

### Representative Snippets

| Query | Relevant document excerpt |
| --- | --- |
| A patient with unexplained edema, proteinuria, and renal disease needs treatment reasoning involving plasma-cell depletion. | A passage describes daratumumab as an anti-CD38 antibody used for plasma cell depletion in relapsed or refractory multiple myeloma. |
| A patient has long-standing treatment-resistant hypertension despite maximal medical therapy. | A passage discusses ambulatory blood-pressure reduction after renal denervation trials such as SPYRAL ON MED. |
| A neonate has central cyanosis and poor feeding after birth, suggesting congenital heart disease. | A passage describes Taussig-Bing anomaly as a rare cyanotic congenital heart defect. |
| Older patients have persistent chest and back pain after treatment for a penetrating aortic ulcer. | A passage explains the importance of adequate proximal seal zones for durable endovascular aortic repair. |
| A patient has ocular surface burn after lime exposure with pain, redness, and decreased vision. | A passage explains surgical reconstruction goals for severe ocular surface burns. |
