# NanoR2MED

## Overview

NanoR2MED is the Nano task group for R2MED, a reasoning-driven medical
retrieval benchmark. It contains eight English retrieval tasks spanning
biomedical StackExchange-style reference search, diagnostic and examination
evidence retrieval, treatment evidence retrieval, and clinical case retrieval.
The group is deliberately difficult because many queries require an implicit
medical, scientific, or clinical inference before the relevant passage can be
identified.

The group contains 876 queries, 80,000 task-local documents, and 2,678 positive
qrel rows. Every task uses a 10,000-document candidate pool, but query count and
positive density vary. NanoR2MED should be treated as a research evaluation
resource, not as a clinical decision system.

## What This Group Measures

R2MED focuses on reasoning-driven medical retrieval: relevance is not simply
semantic similarity between a query and a document. A retriever may need to
infer a biological concept, diagnosis, examination, treatment decision, or
same-diagnosis case group before it can find the supporting evidence. The Nano
group preserves this structure across eight compact splits.

The Q&A reference tasks retrieve answer-supporting references for
bioinformatics, biology, and medical-sciences questions. The diagnostic and
examination tasks retrieve evidence for clinical vignettes. The treatment task
retrieves PubMed Central passages that support management reasoning. The
clinical case tasks retrieve similar cases where relevance is mediated by
diagnosis or clinical similarity rather than surface symptom overlap alone.

## Task Families

- **Biomedical Q&A reference retrieval:** `NanoR2MEDBioinformatics`,
  `NanoR2MEDBiology`, and `NanoR2MEDMedicalSciences` retrieve supporting
  references for biomedical community questions.
- **Diagnostic and examination evidence retrieval:** `NanoR2MEDMedQADiag` and
  `NanoR2MEDMedXpertQAExam` retrieve medical evidence for exam-style vignettes.
- **Treatment evidence retrieval:** `NanoR2MEDPMCTreatment` retrieves PMC
  passages for treatment or management reasoning.
- **Clinical case retrieval:** `NanoR2MEDPMCClinical` and
  `NanoR2MEDIIYiClinical` retrieve clinically similar cases.

## Dataset Shape

All tasks are English and each uses 10,000 candidate documents. The group is
multi-positive, with an average of 3.06 positives per query. `NanoR2MEDMedQADiag`
has the highest average positive density at 4.42 positives per query, while the
clinical and treatment splits generally have two to four positives per query.

Query length varies heavily. Some Q&A tasks are long but still question-like,
while `NanoR2MEDIIYiClinical` and `NanoR2MEDPMCTreatment` use long structured
case summaries. Documents range from biomedical reference passages to long
clinical records. This makes the group sensitive to both medical entity
understanding and long-context representation.

## Retrieval Behavior

### BM25 Profile

BM25 is not the best profile for any task in the current Nano data. It is
strongest on `NanoR2MEDPMCClinical`, where case reports often repeat distinctive
anatomy, disease, imaging, and symptom terms. It is weakest on exam and
diagnostic evidence retrieval, especially `NanoR2MEDMedXpertQAExam`, where
surface overlap does not reveal the examination or diagnostic bridge.

The group-level BM25 nDCG@10 is 0.2110. This low value is expected for a
reasoning-driven medical benchmark. Sparse retrieval can find medically related
documents, but it often misses the latent concept: a diagnosis hidden in a
vignette, a treatment implication, or the practical resource needed for a
bioinformatics problem.

### Dense Profile

Dense retrieval with `harrier-oss-270m` is the strongest query-weighted profile
at 0.2980 nDCG@10. It is best for six tasks: Bioinformatics, Biology, MedXpertQA
Exam, Medical Sciences, PMC Treatment, and the broad Q&A-style biomedical
reference tasks. Dense retrieval helps bridge paraphrase and implicit
answerability, especially when query wording differs from the evidence passage.

Absolute scores remain modest. Even dense retrieval struggles with diagnostic
and examination tasks because the model must infer an intermediate medical
concept before retrieving evidence. NanoR2MED is therefore a hard benchmark even
for embedding-based retrieval.

### Reranking Hybrid Profile

The reranking hybrid profile is best for `NanoR2MEDIIYiClinical`,
`NanoR2MEDMedQADiag`, and `NanoR2MEDPMCClinical`, and it has the strongest
group-level hit@10 and recall@100. This suggests that hybrid candidate
generation helps when exact clinical terms and semantic case similarity are both
useful, especially in case retrieval and diagnosis-oriented tasks.

Hybrid is below dense on the group-level nDCG@10, but its recall@100 is higher.
For R2MED-style retrieval, that distinction matters: hybrid search may be a good
first-stage retriever for medically plausible candidates, while dense or
specialized reranking may still be needed for final top-10 ordering.

## Task Summary

| Task | Family | Language | Queries | Docs | Positives | Positives/query | BM25 nDCG@10 | Dense nDCG@10 | Reranking hybrid nDCG@10 | Best profile |
| --- | --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | --- |
| [NanoR2MEDBioinformatics](NanoR2MEDBioinformatics.md) | Biomedical reference retrieval | `en` | 77 | 10,000 | 226 | 2.94 | 0.2189 | 0.3425 | 0.2623 | Dense |
| [NanoR2MEDBiology](NanoR2MEDBiology.md) | Biomedical reference retrieval | `en` | 103 | 10,000 | 374 | 3.63 | 0.3455 | 0.4953 | 0.4722 | Dense |
| [NanoR2MEDIIYiClinical](NanoR2MEDIIYiClinical.md) | Clinical case retrieval | `en` | 129 | 10,000 | 457 | 3.54 | 0.1482 | 0.1870 | 0.1975 | Reranking hybrid |
| [NanoR2MEDMedQADiag](NanoR2MEDMedQADiag.md) | Diagnostic evidence retrieval | `en` | 118 | 10,000 | 522 | 4.42 | 0.0700 | 0.1254 | 0.1406 | Reranking hybrid |
| [NanoR2MEDMedXpertQAExam](NanoR2MEDMedXpertQAExam.md) | Examination evidence retrieval | `en` | 97 | 10,000 | 292 | 3.01 | 0.0277 | 0.1599 | 0.0979 | Dense |
| [NanoR2MEDMedicalSciences](NanoR2MEDMedicalSciences.md) | Biomedical reference retrieval | `en` | 88 | 10,000 | 244 | 2.77 | 0.2140 | 0.3567 | 0.3320 | Dense |
| [NanoR2MEDPMCClinical](NanoR2MEDPMCClinical.md) | Clinical case retrieval | `en` | 114 | 10,000 | 248 | 2.18 | 0.3933 | 0.3584 | 0.4477 | Reranking hybrid |
| [NanoR2MEDPMCTreatment](NanoR2MEDPMCTreatment.md) | Treatment evidence retrieval | `en` | 150 | 10,000 | 315 | 2.10 | 0.2580 | 0.3801 | 0.3555 | Dense |

## Interpretation Notes for Model Researchers

NanoR2MED is a hard reasoning benchmark. Low BM25 scores do not merely indicate
poor tokenization; they show that relevance often depends on diagnosis,
treatment, case similarity, or biomedical concept inference. Dense retrieval is
the strongest single profile, but hybrid retrieval improves candidate coverage
and leads several clinical case or diagnostic tasks.

Researchers should inspect task families separately. A model that improves
Bioinformatics or Biology may be learning biomedical reference retrieval, while
improvement on MedQA diagnosis or PMC Clinical may indicate better clinical
reasoning or case similarity. The aggregate score alone hides these differences.

## Training and Leakage Notes

Useful training data includes biomedical Q&A reference pairs, tool-documentation
retrieval, medical exam vignettes with evidence passages, diagnosis-labeled case
matching, PubMed Central treatment evidence, PICO-style intervention retrieval,
and hard negatives that share symptoms or disease terms but support a different
clinical conclusion.

Leakage control should exclude NanoR2MED evaluation queries, qrels, positive
documents, same-source near duplicates, public benchmark examples, and clinical
case records with overlapping diagnoses and text. Synthetic data should preserve
the reasoning bridge rather than producing generic symptom-passage similarity.

## Public Sources

- [R2MED: A Benchmark for Reasoning-Driven Medical Retrieval](https://arxiv.org/abs/2505.14558), 2025.
- [R2MED project page](https://r2med.github.io/).
- [R2MED GitHub repository](https://github.com/R2MED/R2MED).
- [R2MED source datasets](https://huggingface.co/R2MED).

### Source Reference Table

| Source | Year | Type | URL |
| --- | ---: | --- | --- |
| R2MED: A Benchmark for Reasoning-Driven Medical Retrieval | 2025 | benchmark paper | https://arxiv.org/abs/2505.14558 |
| R2MED project page | 2025 | project page | https://r2med.github.io/ |
| R2MED GitHub repository | 2025 | source repository | https://github.com/R2MED/R2MED |
| R2MED source datasets | 2025 | dataset collection | https://huggingface.co/R2MED |
