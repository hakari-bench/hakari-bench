# NanoRTEB / NanoAILAStatutes

## Overview

`NanoAILAStatutes` is an English legal statute retrieval task from NanoRTEB. The query is a long Indian legal situation, and the relevant documents are statutory provisions that apply to the scenario. Every query has multiple positives, so the task measures whether a retriever can recover a set of applicable legal provisions rather than a single answer. Dense retrieval has the best nDCG@10 and hit@10, `reranking_hybrid` is close, and all three candidate profiles reach full recall@100 because the document pool contains only 82 statutes.

## Details

### What the Original Data Measures

The FIRE 2019 AILA track includes a statute retrieval subtask alongside precedent retrieval. Given a legal situation, systems must retrieve statutory provisions useful for analyzing or answering the scenario.

RTEB includes AILA statutes as a realistic English legal retrieval task. The Nano split keeps the long-query-to-statute framing: queries are fact patterns from legal situations, while candidate documents are statute titles and provision text.

### Observed Data Profile

The Nano split contains 50 queries, 82 documents, and 217 positive qrel rows. Queries average 3,038.42 characters, while statute documents average 1,972.63 characters. Every query has multiple positives, averaging 4.34 positives per query, with a minimum of 2, a median of 4.5, and a maximum of 5.

Example queries concern criminal appeals, dowry death, sanction for criminal proceedings, conspiracy, and registration of partnership asset distribution. Positive documents include statutory provisions such as attempt to murder, dowry death, criminal conspiracy, and compulsory registration.

### BM25 Evaluation Profile

The BM25 candidate subset uses the full 82-document pool and reaches nDCG@10 of 0.2070, hit@10 of 0.6600, and recall@100 of 1.0000. BM25 benefits when the legal situation mentions offence names, statute-like terminology, or procedural terms that also appear in the provision text.

The main limitation is abstraction. A long fact pattern may imply a statutory provision without repeating its title or core phrasing. BM25 can also overrank provisions that share generic criminal-law vocabulary but do not control the situation.

### Dense Evaluation Profile

The dense candidate subset from `harrier_oss_v1_270m` uses the full 82-document pool and reaches nDCG@10 of 0.2711, hit@10 of 0.7600, and recall@100 of 1.0000. Dense retrieval is the strongest profile for early ranking.

This indicates that embedding similarity is helpful for mapping facts to abstract legal provisions. The model can connect a scenario to statute meaning even when exact title words are sparse. The remaining nDCG gap shows that ordering several applicable statutes is still difficult.

### Reranking Hybrid Evaluation Profile

The `reranking_hybrid` subset covers the same 82-document pool, does not need the rank-101 safeguard, and reaches nDCG@10 of 0.2564, hit@10 of 0.7400, and recall@100 of 1.0000. Hybrid retrieval is close to dense retrieval but slightly weaker on top-rank quality.

Because recall@100 is saturated for all methods, the useful comparison is early ordering. Dense semantic matching appears to rank applicable provisions slightly better, while the hybrid profile remains valuable when rare statutory terms are important.

### Metric Interpretation for Model Researchers

All queries have multiple positives, so nDCG@10 is the most informative top-rank metric. Hit@10 only asks whether at least one applicable statute appears in the first ten, and recall@100 is less discriminative here because the entire candidate pool fits inside 100 ranks.

For this split, improvements should focus on ranking the right set of provisions early. A model that retrieves one obvious statute but misses related sections may still be weak for legal assistance.

### Query and Relevance Type Tendencies

Queries are long legal scenarios. Relevant documents are statute titles and provision descriptions, usually much shorter and more abstract than the query. Several provisions can jointly apply to one scenario.

Relevance is legal applicability. The statute does not need to reuse the query wording, but it must govern the legal issue raised by the facts.

### Representative Failure Modes

Common failures include retrieving provisions with similar offence vocabulary but different legal elements, missing procedural statutes implied by the facts, overranking broad criminal provisions, and returning only one applicable section when multiple sections are needed. BM25 is sensitive to title overlap; dense retrieval may blur related statutory concepts.

### Training Data That May Help

Useful training data includes statute retrieval, legal issue classification, fact-pattern-to-provision pairs, statutory interpretation examples, and multi-label legal applicability datasets. Evaluation legal situations, statute texts, and qrels should be excluded.

### Model Improvement Notes

Models should learn to map facts to legal elements and to rank groups of applicable provisions. Hard negatives should come from related statutes that share offence names, procedural terms, or legal domains but do not apply. Dense retrieval is the strongest first-stage profile, while hybrid retrieval remains useful for rare legal terminology.

## Example Data

### Public Sources

- [Overview of the FIRE 2019 AILA Track: Artificial Intelligence for Legal Assistance](https://ceur-ws.org/Vol-2517/T1-1.pdf), task paper.
- [AILA 2019 Precedent & Statute Retrieval Task](https://doi.org/10.5281/zenodo.4063986), dataset record.
- [Introducing RTEB: A New Standard for Retrieval Evaluation](https://huggingface.co/blog/rteb), benchmark article.

### Source Reference Table

| Title | Year | Type | URL |
| --- | ---: | --- | --- |
| Overview of the FIRE 2019 AILA Track: Artificial Intelligence for Legal Assistance | 2019 | task paper | https://ceur-ws.org/Vol-2517/T1-1.pdf |
| AILA 2019 Precedent & Statute Retrieval Task | 2020 | dataset record | https://doi.org/10.5281/zenodo.4063986 |
| Introducing RTEB: A New Standard for Retrieval Evaluation | 2025 | benchmark article | https://huggingface.co/blog/rteb |

### Representative Snippets

| Query | Relevant document excerpt |
| --- | --- |
| A criminal appeal challenges conviction and life imprisonment after facts involving serious bodily harm. | Title: Attempt to murder. |
| An appeal concerns conviction connected to the death of a woman within a marriage context. | Title: Dowry death. |
| A proceeding raises whether sanction is required before initiating criminal proceedings. | Title: Certain laws not to be affected by this Act. |
| A complaint involves alleged agreement among parties to commit an offence. | Title: Punishment of criminal conspiracy. |
| A civil dispute asks whether documents distributing partnership assets require registration. | Title: Documents of which registration is compulsory. |
