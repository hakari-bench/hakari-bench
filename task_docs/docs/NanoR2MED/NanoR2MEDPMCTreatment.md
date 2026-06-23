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
| Case Summary: - **Patient Demographics:** 43-year-old male - **Chief Complaint:** Unexplained edema... [100 / 2,067 chars] | Daratumumab is an antibody against CD38 used for plasma cell depletion in relapsed or refractory multiple myeloma (MM). It mediates depletion of plasma cells, which overexpress CD38, through a wide ra... [200 / 952 chars] |
| Case Summary: - Patient Demographics: 43-year-old male - Chief Complaint: Long-standing therapy-resi... [100 / 1,404 chars] | While the observed 24 hours systolic ambulatory BD reduction at 6-months follow-up in contemporary trials such as SPYRAL ON MED is generally considered to be modest (−1.9 mmHg),6 it seems that the obs... [200 / 664 chars] |
| Case Summary: - **Patient Demographics:** 2-day-old male neonate - **Chief Complaint:** Central cyan... [100 / 2,145 chars] | Helen B. Taussig and Richard J. Bing were the first to describe a rare cyanotic congenital heart defect known as the Taussig-Bing anomaly (TBA) in 1949, that includes a non-restrictive subpulmonary ve... [200 / 2,503 chars] |
| Case Summary: - Patient Demographics: - Case 1: 87-year-old woman - Case 2: 84-year-old man - Chief... [100 / 1,709 chars] | Adequate proximal seal zones are essential for durable endovascular aortic repair. Although the definition of an adequate proximal seal zone can vary depending on the underlying aortic pathology, comp... [200 / 660 chars] |
| Case Summary: - Patient Demographics: 43-year-old male - Chief Complaint: Redness, pain, and decreas... [100 / 1,950 chars] | The surgical approach for severe ocular surface burns aims to reconstruct ocular surface function, address eyelid deformities, correct limbal stem cell deficiency, and alleviate conjunctival sac const... [200 / 634 chars] |

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
