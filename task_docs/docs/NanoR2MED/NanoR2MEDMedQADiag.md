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

| Query | Positive document |
| --- | --- |
| A 33-year-old G2P1 woman presents to the office because of poor diabetic control. She is currently at 18 weeks gestation and admits to having poor control of her type 1 diabetes before becoming pregnant. Her family history is non-contributory. The physical examination shows a pregnant woman with a fundal height of 20 cm (7.9 in). An abdominal ultrasound is ordered. What is the most likely congenital abnormality shown on the ultrasound? [439 chars] | Malformations. he incidence of major malformations in women with type 1 diabetes is at least doubled and approximates 11 percent Qovanovic, 2015). These account for almost half of perinatal deaths in diabetic pregnancies. As shown in Table 57-6, cardiovascular malformations accounted for more than half of the anomalies. In a cohort study of more than 2 million births in Canada, the risk of an isolated cardiac defect was ivefold higher in women with type 1 diabetes (Uu, 2013). he caudal regression sequence, described in Chapter 10 (p. 196), is a rare malformation frequently associated with maternal diabetes (Garne, 2012). [628 chars] |
| A 68-year-old man presents with difficulty breathing for the last 3 hours. Upon asking about other symptoms, he mentions that he had a cough for the last 4 months which he attributes to his smoking. He says he had frequent nasal stuffiness and headaches over the last 3 months, for which he takes over-the-counter cold medications and analgesics. Over the last 2 months, he often felt that his face was mildly swollen, especially in the morning hours, but he did not consider it to be anything seriou... [500 / 986 chars] | The optic nerve [II] is not a true cranial nerve, but rather an extension of the brain carrying afferent fibers from the retina of the eyeball to the visual centers of the brain. The optic nerve is surrounded by the cranial meninges, including the subarachnoid space, which extends as far forward as the eyeball. Any increase in intracranial pressure therefore results in increased pressure in the subarachnoid space surrounding the optic nerve. This may impede venous return along the retinal veins, causing edema of the optic disc (papilledema), which can be seen when the retina is examined using an ophthalmoscope. The optic nerve leaves the orbit through the optic canal (Fig. 8.101). It is accompanied in the optic canal by the ophthalmic artery. The oculomotor nerve [III] leaves the anterior surface of the brainstem between the midbrain and the pons. It passes forward in the lateral wall of the cavernous sinus. [921 chars] |
| A 25-year-old woman presents to her primary care provider for evaluation of a "painful mass in my left groin." She says that her symptoms began 4 days ago as a painful mass that slowly enlarged, ruptured, and ulcerated. However, she denies fever, chills, dysuria, or hematuria. Three weeks prior to her current symptoms she noted a small, painless ulcer on her labium majorum that resolved after a few days. She admits to having unprotected sex with a male partner a month ago while she was traveling... [500 / 796 chars] | lympHogranUloma venereUm C. trachomatis serovars L1, L2, and L3 cause LGV, an invasive systemic STD. The peak inci dence of LGV corresponds with the age of greatest sexual activity: the second and third decades of life. The worldwide incidence of LGV is falling, but the disease is still endemic and a major cause of morbidity in parts of Asia, Africa, South America, and the Caribbean. LGV is rare in industrialized countries; for more than a decade, the reported incidence in the United States has been only 0.1 case per 100,000 population. In the Bahamas, an apparent outbreak of LGV was described in association with a concurrent increase in heterosexual infection with HIV. Reports of outbreaks with the newly identified variant L2b in Europe, Australia, and the United States indicate that LGV is becoming more prevalent among MSM. These cases have usually presented as hemorrhagic proctocolitis in HIV-positive men. More widespread use of NAATs for identification of rectal infections may [995 chars] |

### Source Reference Table

| Title | Year | Type | URL |
| --- | ---: | --- | --- |
| R2MED: A Benchmark for Reasoning-Driven Medical Retrieval | 2025 | arXiv paper | [https://arxiv.org/abs/2505.14558](https://arxiv.org/abs/2505.14558) |
| R2MED project page | 2025 | project page | [https://r2med.github.io/](https://r2med.github.io/) |
| R2MED GitHub repository | 2025 | source repository | [https://github.com/R2MED/R2MED](https://github.com/R2MED/R2MED) |
| R2MED/MedQA-Diag | 2025 | dataset card | [https://huggingface.co/datasets/R2MED/MedQA-Diag](https://huggingface.co/datasets/R2MED/MedQA-Diag) |

### Representative Snippets

| Query | Relevant document excerpt |
| --- | --- |
| A pregnant patient with poor type 1 diabetes control asks about fetal risk. | A textbook passage explains that major malformations in type 1 diabetic pregnancies are at least doubled and account for many perinatal deaths. |
| A patient presentation requires recognizing a cranial nerve or visual pathway issue. | A textbook passage explains the optic nerve as an extension of the brain carrying afferent retinal fibers. |
| A young woman has a painful groin mass that ulcerated after sexual exposure. | A passage describes lymphogranuloma venereum caused by invasive `C. trachomatis` serovars L1, L2, and L3. |
| A neonate has severe unconjugated hyperbilirubinemia with lethargy and worsening symptoms. | A passage describes Crigler-Najjar syndrome type I and its striking neonatal unconjugated hyperbilirubinemia. |
| A child has recurrent pneumonia, persistent cough, fever, vomiting, and concerning chronic features. | A passage describes cystic fibrosis as a single-gene disorder with viscid secretions blocking airways and pancreatic ducts. |
