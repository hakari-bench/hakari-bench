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

| Query | Positive document |
| --- | --- |
| Appellant calls in question legality of the judgment rendered by High Court confirming his conviction for offence and sentence of imprisonment for life as awarded by the learned Sessions Judge. Background facts as unfolded during trial by the prosecution are essentially as follows. One P1 (hereinafter referred to as the 'deceased') was having industry and he employed a number of girls. The accused used to make fun of the girls/workers outside the factory and this was objected to by the deceased... [500 / 3,569 chars] | Title: Attempt to murder Desc: Whoever does any act with such intention or knowledge, and under such circumstances that, if he by that act caused death, he would be guilty or murder, shall be punished with imprisonment of either description for a term which may extend to ten years, and shall also be liable to fine; and if hurt is caused to any person by such act, the offender shall be liable either to 1 [imprisonment for life], or to such punishment as is hereinbefore mentioned. Attempts by life convicts2 [When any person offending under this section is under sentence of 3 [imprisonment for life], he may, if hurt is caused, be punished with death.] Illustrations (a) A shoots at Z with intention to kill him, under such circumstances that, if death ensued. A would be guilty of murder. A is liable to punishment under this section. (b) A, with the intention of causing the death of a child of tender years, exposes it in a desert place. A has committed the offence defined by this section, th... [1,000 / 1,973 chars] |
| This appeal, by special leave, has been preferred against the judgment and order dated 23 February 2005 of the High Court (Aurangabad Bench), by which the appeal preferred by the appellants was dismissed and their conviction and sentence of 7 years RI imposed thereunder was affirmed. The deceased P1 was daughter of PW1. P2 resident of village Sanjkheda and she was married to appellant no. 1 P3 son of P4 about two and half years prior to the date of incident which took place on 15 September 1991.... [500 / 3,266 chars] | Title: Dowry death Desc: (1) Where the death of a woman is caused by any burns or bodily injury or occurs otherwise than under normal circumstances within seven years of her marriage and it is shown that soon before her death she was subjected to cruelty or harassment by her husband or any relative of her husband for, or in connection with, any demand for dowry, such death shall be called "dowry death", and such husband or relative shall be deemed to have caused her death. Explanation.-For the purpose of this sub-section, "dowry" shall have the same meaning as in section 2 of the Dowry Prohibition Act, 1961 (28 of 1961). (2) Whoever commits dowry death shall be punished with imprisonment for a term which shall not be less than seven years but which may extend to imprisonment for life.] Inserted by Act 43 of 1986, section 10 (w.e.f. 19-11-1986). [856 chars] |
| The appellant before us was examined as prime witness in the trial of T.R. on the file of the Special Judge against the first respondent. The trial ended in conviction against the first respondent and when the appeal filed by him came to be heard by the High Court the appellant had become a Cabinet Minister. On account of the disparaging remarks made by the Appellate Judge the appellant tendered his resignation and demitted office for maintaining democratic traditions. It is in that backgroud th... [500 / 2,857 chars] | Title: Certain laws not to be affected by this Act Desc: Nothing in this Act shall affect the provisions of any Act for punishing mutiny and desertion of officers, soldiers, sailors or airmen in the service of the Government of India or the provisions of any special or local law.] Substituted by the A.O. 1950, for the original section. [337 chars] |

### Source Reference Table

| Title | Year | Type | URL |
| --- | ---: | --- | --- |
| Overview of the FIRE 2019 AILA Track: Artificial Intelligence for Legal Assistance | 2019 | task paper | [https://ceur-ws.org/Vol-2517/T1-1.pdf](https://ceur-ws.org/Vol-2517/T1-1.pdf) |
| AILA 2019 Precedent & Statute Retrieval Task | 2020 | dataset record | [https://doi.org/10.5281/zenodo.4063986](https://doi.org/10.5281/zenodo.4063986) |
| Introducing RTEB: A New Standard for Retrieval Evaluation | 2025 | benchmark article | [https://huggingface.co/blog/rteb](https://huggingface.co/blog/rteb) |

### Representative Snippets

| Query | Relevant document excerpt |
| --- | --- |
| A criminal appeal challenges conviction and life imprisonment after facts involving serious bodily harm. | Title: Attempt to murder. |
| An appeal concerns conviction connected to the death of a woman within a marriage context. | Title: Dowry death. |
| A proceeding raises whether sanction is required before initiating criminal proceedings. | Title: Certain laws not to be affected by this Act. |
| A complaint involves alleged agreement among parties to commit an offence. | Title: Punishment of criminal conspiracy. |
| A civil dispute asks whether documents distributing partnership assets require registration. | Title: Documents of which registration is compulsory. |
