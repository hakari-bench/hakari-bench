# NanoR2MED / NanoR2MEDPMCClinical

## Overview

`NanoR2MEDPMCClinical` is an English clinical case retrieval task from R2MED. Queries are concise patient case descriptions, and documents are longer PubMed Central case presentations. Relevance is based on similar cases, usually tied by diagnosis or clinically meaningful case similarity. Unlike several other NanoR2MED tasks, BM25 is stronger than dense retrieval here, likely because case reports repeat distinctive anatomy, disease, imaging, and symptom terms. The `reranking_hybrid` pool is strongest overall, combining lexical case-report anchors with semantic similarity.

## Details

### What the Original Data Measures

R2MED defines clinical case retrieval as retrieving cases with the same diagnosis or clinically useful similarity. The benchmark paper describes collecting patient records from PMC-Patients and IIYi sources, extracting clinical presentations, and using confirmed diagnosis as the reasoning bridge between query and relevant cases.

For PMC-Clinical, the source data comes from PubMed Central case reports. R2MED identifies multi-case articles, uses one case as a query source, and treats related cases as positives after filtering and review. The task is intended for research evaluation, not clinical decision-making.

### Observed Data Profile

The Nano split contains 114 queries, 10,000 documents, and 248 positive qrel rows. Queries average 827.68 characters, and documents average 2,103.50 characters. Documents are substantially longer than queries because they are case presentations.

Each query has 2.18 positives on average, with a median of 2 and a maximum of 4. Multi-positive queries account for 83 of 114 queries, or 72.81%. Examples include mandibular osteolytic lesions, melanoma-associated intracranial events, retroperitoneal tumors, skull-base inflammatory disease, and splenic masses.

### BM25 Evaluation Profile

The BM25 candidate subset uses top-500 candidates and reaches nDCG@10 of 0.3933, hit@10 of 0.7105, and recall@100 of 0.8185. BM25 is a strong baseline for this split and outperforms dense retrieval on all reported metrics.

This reflects the nature of PMC case reports. Diagnoses, anatomy, imaging terms, pathology descriptors, and rare disease names often appear explicitly in both query and relevant cases. Exact term frequency is therefore highly informative.

### Dense Evaluation Profile

The dense candidate subset from `harrier_oss_v1_270m` uses top-500 candidates and reaches nDCG@10 of 0.3584, hit@10 of 0.6316, and recall@100 of 0.7540. Dense retrieval is useful but weaker than BM25. It can capture case similarity across paraphrase, but it may overgeneralize among cases that share clinical context without sharing the correct diagnosis.

This split is a reminder that dense models do not automatically dominate in biomedical retrieval. When rare clinical entities and anatomy terms are repeated, lexical matching can be the more reliable first-stage signal.

### Reranking Hybrid Evaluation Profile

The `reranking_hybrid` subset uses top-100 candidates, with six rows receiving the optional rank-101 safeguard. It reaches nDCG@10 of 0.4477, hit@10 of 0.7807, and recall@100 of 0.8589. This is the strongest profile for the split.

Hybrid retrieval benefits from both sides: BM25 supplies exact disease and anatomy anchors, while dense retrieval adds cases that are clinically related despite phrasing differences. The combined pool is therefore the best target for reranking.

### Metric Interpretation for Model Researchers

This is a multi-positive similar-case task. nDCG@10 rewards ranking multiple related cases early, hit@10 measures whether at least one related case is retrieved in the first ten results, and recall@100 measures candidate coverage for reranking.

For PMC-Clinical, BM25 is the stronger standalone baseline, dense retrieval is the semantic comparison point, and hybrid retrieval is the best overall candidate-generation profile. A successful model should preserve rare clinical terms while improving diagnosis-level case matching.

### Query and Relevance Type Tendencies

Queries are case summaries with age, symptoms, imaging, pathology, clinical course, or diagnostic findings. Relevant documents are longer PMC case presentations. Positives may share diagnosis or clinically meaningful similarity without matching every demographic or symptom detail.

Relevance is case-similarity oriented. A passage can share a symptom or anatomical region and still be wrong if it reflects a different diagnosis.

### Representative Failure Modes

Failures include retrieving a case from the same anatomical region but wrong diagnosis, overmatching broad neurocognitive or dental symptoms, ranking general case-report passages above rare-disease matches, and missing cases where the relevant diagnosis is stated with different terminology. Dense retrieval may cluster by broad specialty; BM25 may overvalue repeated anatomy terms.

### Training Data That May Help

Useful training data includes non-overlapping clinical case similarity pairs, PMC-Patients retrieval, diagnosis-labeled case matching, clinical entity linking from case descriptions, and hard negatives sharing symptoms but not diagnoses. Evaluation cases, qrels, positive case passages, and same-article duplicates should be excluded.

### Model Improvement Notes

Models should jointly handle rare disease terms, anatomy, imaging, pathology, and diagnosis-level similarity. Multi-positive objectives are appropriate because many queries have more than one related case. Hard negatives should share symptoms or anatomy while differing in diagnosis.

## Example Data

| Query | Positive document |
| --- | --- |
| A 5-year-old female patient presents with swelling and pain in the right mandibular region. Initial antibiotic treatment provided temporary relief, but her symptoms recurred. Computed tomography (CT) shows an osteolytic, well-defined, buccolingual, expansile lesion in the mandible, coupled with a profuse periosteal reaction. Laboratory tests, including a complete blood count and other parameters, showed no notable systemic symptoms. An incisional biopsy was performed. What is the likely diagnosi... [500 / 532 chars] | A 33-year-old male attended the medical consultation complaining of a painful perianal lesion over the last 18 months. Previous therapeutic attempts, including different antibiotics orally or topically administered, and topical steroids failed to result in a cure. The patient had a history of central diabetes insipidus 4 years ago, the etiology of which has remained unknown. The diagnosis of diabetes insipidus was based on clinical grounds as imaging studies were not available. The symptoms presented as thirst, polyuria (diluted urine), antidiuretic hormone defect, and a favorable response to desmopressin. On examination, the surgeon reported a perianal ulcerative plaque with necrotic floor and raised edges that was oozing pus. A biopsy was taken. The ulcer was single and measured 2.0 × 2.0 cm with irregular outlines. A histopathological examination of the lesion showed a partially ulcerated epidermal covering, and the underlying dermis was infiltrated by sheets of dyscohesive round ce... [1,000 / 1,579 chars] |
| A 46-year-old man with a history of radical extirpated melanoma presents with spontaneous acute severe headache, followed by progressive confusion and mild left-sided hemiparesis. MRI of the brain shows ischemic lesions in the bilateral occipital and right parietal regions. Initial MR angiography showed no abnormality, but the examination was without gadolinium and considered poor quality. The patient smokes 20 cigarettes and uses cannabis 3–4 times a day. On admission, his blood pressure was 18... [500 / 988 chars] | A 29-year-old female patient with a 6-day history of laparoscopic uterine myomectomy visited a local hospital complaining of worsening headache and mild left hand weakness since surgery. Brain computed tomography (CT) showed acute ICH in the right basal ganglia and no enhancing lesion within the hemorrhage was observed on CT angiography (CTA). However, mild multifocal stenoses were detected on the bilateral distal middle cerebral arteries (MCA), which had gone undetected at that time (). She had developed severe anemia (5.3 g/dL) attributable to menorrhagia and required a red blood cell transfusion before and after myomectomy. In addition, because of uncontrolled vaginal bleeding after myomectomy, uterine constrictors (oxytocin and methylergometrine) were administered 2 days after myomectomy. Right basal ganglia ICH was managed conservatively, but she developed right side weakness three days after ICH diagnosis. Diffusion weighted magnetic resonance imaging (DWI) performed at that time... [1,000 / 1,977 chars] |
| An 82-year-old man presented with a chief complaint of an abdominal mass and associated abdominal discomfort, which he first noticed 4 years prior. A CT scan revealed a lipomatous retroperitoneal tumor that had been growing. Physical examination showed a large palpable abdominal mass, but no other specific abnormalities. An abdominal CT scan confirmed a huge abdominal mass lesion composed mainly of lipomatous tissues. All laboratory data were normal. What is the most likely diagnosis for this pa... [500 / 518 chars] | A 71-year-old woman presented with complaint of progressive abdominal distension. The ultrasonography revealed a huge retroperitoneal or mesenchymal mass occupying the entire abdomen. The patient had not experienced any symptoms, such as abdominal pain, nausea, vomiting, constipation, dyspepsia, or dyspnea. She had a history of hypertension only.\nThe patient was admitted to the hospital and underwent contrast-enhanced computed tomography (CT) of the abdomen. The scan revealed a huge fatty mass originating from the retroperitoneum probably indicative of retroperitoneal liposarcoma. The CT scan also showed tumor encasement of the entire left kidney. Septations and solid portions were observed within the mass. The spleen was pushed anteriorly and the small bowel was deviated to the right side of the intra-abdominal space by the mass (fig. ).\nBecause the patient was old, we decided to attempt organ-preserving surgery for the removal of the tumor to minimize the morbidity. The mass was ap... [1,000 / 2,908 chars] |

### Source Reference Table

| Title | Year | Type | URL |
| --- | ---: | --- | --- |
| R2MED: A Benchmark for Reasoning-Driven Medical Retrieval | 2025 | arXiv paper | [https://arxiv.org/abs/2505.14558](https://arxiv.org/abs/2505.14558) |
| R2MED project page | 2025 | project page | [https://r2med.github.io/](https://r2med.github.io/) |
| R2MED GitHub repository | 2025 | source repository | [https://github.com/R2MED/R2MED](https://github.com/R2MED/R2MED) |
| R2MED/PMC-Clinical | 2025 | dataset card | [https://huggingface.co/datasets/R2MED/PMC-Clinical](https://huggingface.co/datasets/R2MED/PMC-Clinical) |

### Representative Snippets

| Query | Relevant document excerpt |
| --- | --- |
| A child has recurrent swelling and pain in the right mandibular region with an osteolytic lesion on CT. | A related case describes a chronic painful lesion with repeated treatments and clinically relevant lesion history. |
| A man with prior melanoma develops acute severe headache, confusion, and hemiparesis with ischemic brain lesions. | A related case describes postoperative headache and hand weakness with brain CT findings. |
| An older man has an abdominal mass and a growing lipomatous retroperitoneal tumor. | A related case describes progressive abdominal distension and a huge retroperitoneal or mesenchymal mass. |
| A man has progressive paroxysmal headache, vomiting, diplopia, and visual disturbance without fever. | A related case describes paroxysmal headache with visual disturbance over months. |
| A child has an incidental splenic mass detected on abdominal ultrasonography. | A related case describes abdominal pain and mass-like distention involving the left abdomen. |
