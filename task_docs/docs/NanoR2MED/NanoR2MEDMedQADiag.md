# NanoR2MED / NanoR2MEDMedQADiag

## Overview

`NanoR2MEDMedQADiag` is an English clinical evidence retrieval task from R2MED. Queries are MedQA-style patient vignettes converted into open-ended diagnostic retrieval problems, and documents are medical textbook passages. Relevant passages support the diagnosis, mechanism, anatomy, or diagnostic reasoning needed for the vignette. The split is very difficult for lexical retrieval because the query often describes symptoms while the positive passage states the disease or mechanism. Dense retrieval improves substantially, and hybrid retrieval gives the best early-ranking profile despite slightly lower recall@100 than dense.

## Details

### What the Original Data Measures

R2MED defines clinical evidence retrieval as retrieving authoritative medical evidence that supports diagnostic or treatment decisions. For MedQA-Diag, the source questions come from MedQA-style clinical vignettes, and the document pool comes from medical textbook materials associated with the original MedQA benchmark.

The R2MED construction converts multiple-choice diagnosis questions into open-ended retrieval queries. Relevance is assessed using the query, answer, and reasoning path, so a positive passage may support the inferred diagnosis even if it does not share the same surface symptoms.

### Observed Data Profile

The Nano split contains 118 queries, 10,000 documents, and 522 positive qrel rows. Queries average 706.74 characters and usually include age, symptoms, history, physical findings, laboratory values, imaging, or exam clues. Documents average 791.42 characters and are textbook chunks from sources such as Harrison, Gray's Anatomy, First Aid, Lippincott, Katzung, and Schwartz.

Each query has 4.42 positives on average, with a median of 4 and a maximum of 8. Multi-positive queries are common: 103 of 118 queries, or 87.29%. Examples include diabetic pregnancy malformations, cranial-nerve anatomy, lymphogranuloma venereum, neonatal unconjugated hyperbilirubinemia, and cystic fibrosis.

### BM25 Evaluation Profile

The BM25 candidate subset uses top-500 candidates and reaches nDCG@10 of 0.0700, hit@10 of 0.2458, and recall@100 of 0.2318. This is a very weak sparse profile. BM25 can match symptoms, ages, labs, and body-system terms, but those surface terms often occur in many unrelated textbook passages.

The central difficulty is diagnostic inference. A vignette may describe a disease without naming it, while the positive passage uses the disease name or mechanism. BM25 tends to retrieve passages with overlapping symptoms rather than the passage that supports the latent diagnosis.

### Dense Evaluation Profile

The dense candidate subset from `harrier_oss_v1_270m` uses top-500 candidates and reaches nDCG@10 of 0.1254, hit@10 of 0.3559, and recall@100 of 0.4272. Dense retrieval improves over BM25 across all metrics, especially recall@100, because embeddings can connect a vignette to a diagnosis or mechanism even when terminology differs.

The scores remain low because the task requires medical reasoning. A model must infer the likely disease entity from the clinical presentation and then retrieve evidence about that entity.

### Reranking Hybrid Evaluation Profile

The `reranking_hybrid` subset uses top-100 candidates, with 34 rows receiving the optional rank-101 safeguard. It reaches nDCG@10 of 0.1406, hit@10 of 0.3983, and recall@100 of 0.3985. Hybrid retrieval gives the best nDCG@10 and hit@10, but its recall@100 is lower than dense retrieval because the candidate list is smaller.

This suggests that sparse exact terms help promote some correct evidence passages once dense retrieval has captured the diagnostic neighborhood. For reranking, the tradeoff is between dense top-500 coverage and hybrid top-100 precision.

### Metric Interpretation for Model Researchers

This is a multi-positive evidence retrieval task. nDCG@10 rewards ranking several relevant textbook passages early. Hit@10 measures whether at least one diagnostic support passage appears in the first ten results. Recall@100 measures how much evidence is exposed to reranking.

For MedQA-Diag, BM25 is a low baseline, dense retrieval is the stronger coverage profile, and hybrid retrieval is the best early-ranking profile. Model improvements should show diagnosis-aware retrieval rather than symptom-word matching.

### Query and Relevance Type Tendencies

Queries are clinical vignettes with exam-style diagnostic clues. Relevant documents are textbook passages about diseases, mechanisms, anatomy, complications, or management principles. The positive passage may name the diagnosis directly or explain the pathophysiology needed to infer it.

Relevance is reasoning-based. A passage is useful if it supports the diagnosis or diagnostic step, even if it does not repeat the vignette's exact wording.

### Representative Failure Modes

Failures include matching the same symptom cluster with the wrong disease, retrieving pharmacology or anatomy passages that share terms but not the diagnostic answer, missing disease-name passages when the query never names the disease, and confusing similar pediatric, obstetric, infectious, or neurologic presentations. BM25 is especially vulnerable to surface symptom overlap; dense retrieval may retrieve the right body system but the wrong diagnosis.

### Training Data That May Help

Useful training data includes non-overlapping MedQA diagnostic cases with evidence passages, clinical vignette-to-diagnosis retrieval, medical textbook section retrieval, and hard negatives from similar symptoms but different diagnoses. Evaluation queries, qrels, and positive textbook passages should be excluded.

### Model Improvement Notes

Models should learn to infer diagnoses from vignettes and retrieve evidence about the inferred entity or mechanism. Multi-positive training is appropriate because several textbook passages may support one case. Hard negatives should share age, symptoms, body system, or labs while implying a different diagnosis.

## Example Data

### Public Sources

- [R2MED: A Benchmark for Reasoning-Driven Medical Retrieval](https://arxiv.org/abs/2505.14558), benchmark paper.
- [R2MED project page](https://r2med.github.io/).
- [R2MED GitHub repository](https://github.com/R2MED/R2MED).
- [R2MED/MedQA-Diag dataset card](https://huggingface.co/datasets/R2MED/MedQA-Diag).

### Source Reference Table

| Title | Year | Type | URL |
| --- | ---: | --- | --- |
| R2MED: A Benchmark for Reasoning-Driven Medical Retrieval | 2025 | arXiv paper | https://arxiv.org/abs/2505.14558 |
| R2MED project page | 2025 | project page | https://r2med.github.io/ |
| R2MED GitHub repository | 2025 | source repository | https://github.com/R2MED/R2MED |
| R2MED/MedQA-Diag | 2025 | dataset card | https://huggingface.co/datasets/R2MED/MedQA-Diag |

### Representative Snippets

| Query | Relevant document excerpt |
| --- | --- |
| A pregnant patient with poor type 1 diabetes control asks about fetal risk. | A textbook passage explains that major malformations in type 1 diabetic pregnancies are at least doubled and account for many perinatal deaths. |
| A patient presentation requires recognizing a cranial nerve or visual pathway issue. | A textbook passage explains the optic nerve as an extension of the brain carrying afferent retinal fibers. |
| A young woman has a painful groin mass that ulcerated after sexual exposure. | A passage describes lymphogranuloma venereum caused by invasive `C. trachomatis` serovars L1, L2, and L3. |
| A neonate has severe unconjugated hyperbilirubinemia with lethargy and worsening symptoms. | A passage describes Crigler-Najjar syndrome type I and its striking neonatal unconjugated hyperbilirubinemia. |
| A child has recurrent pneumonia, persistent cough, fever, vomiting, and concerning chronic features. | A passage describes cystic fibrosis as a single-gene disorder with viscid secretions blocking airways and pancreatic ducts. |
