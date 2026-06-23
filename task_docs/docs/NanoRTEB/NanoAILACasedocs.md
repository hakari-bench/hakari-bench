# NanoRTEB / NanoAILACasedocs

## Overview

`NanoAILACasedocs` is an English legal precedent retrieval task from NanoRTEB. The query is a long Indian legal situation, and the relevant documents are Supreme Court of India case documents that serve as precedents for the facts and legal issues. The task has multiple positives for most queries and very long documents, so it tests issue-level legal retrieval rather than short keyword matching. Dense retrieval has the best nDCG@10, `reranking_hybrid` has the best hit@10 and recall@100, and BM25 remains competitive because legal situations and precedents often share distinctive statutory and procedural language.

## Details

### What the Original Data Measures

The AILA track at FIRE 2019 studied artificial intelligence for legal assistance. Its case-law retrieval subtask asks systems to retrieve prior cases relevant to a legal situation, supporting workflows such as precedent search and legal research.

RTEB includes AILA case documents as an English retrieval benchmark with realistic long-form legal text. In the Nano version, queries are full legal fact patterns and candidate documents are complete case documents, not short abstracts.

### Observed Data Profile

The Nano split contains 50 queries, 186 documents, and 195 positive qrel rows. Queries average 3,038.42 characters, while documents average 26,947.34 characters. Positives per query average 3.90, with a minimum of 1, a median of 3, and a maximum of 22. Forty of 50 queries have more than one positive document.

Example queries concern appeals against criminal convictions, questions about sanction before initiating criminal proceedings, and civil issues such as whether distribution of partnership assets on dissolution requires registration. Positive documents are full Supreme Court of India judgments.

### BM25 Evaluation Profile

The BM25 candidate subset uses the full 186-document pool and reaches nDCG@10 of 0.2805, hit@10 of 0.6200, and recall@100 of 0.9128. BM25 benefits from shared names, statutes, procedural phrases, offences, and legal terminology.

Its limitation is that a precedent can be relevant because of legal issue similarity even when the surface wording differs. Long documents also contain many generic legal phrases, so term frequency can overvalue cases that share broad vocabulary but not the controlling issue.

### Dense Evaluation Profile

The dense candidate subset from `harrier_oss_v1_270m` uses the full 186-document pool and reaches nDCG@10 of 0.4003, hit@10 of 0.6800, and recall@100 of 0.9026. Dense retrieval has the strongest top-rank quality for this split.

This suggests that embedding similarity is useful for matching legal situations to cases with similar factual and doctrinal structure. The slightly lower recall@100 compared with BM25 and hybrid retrieval shows that dense matching can miss some relevant precedents when the case relation depends on rare terms or citations.

### Reranking Hybrid Evaluation Profile

The `reranking_hybrid` subset uses top-100 candidates, with 2 rows receiving the optional rank-101 safeguard. It reaches nDCG@10 of 0.3667, hit@10 of 0.7000, and recall@100 of 0.9436. Hybrid retrieval has the best top-ten hit rate and best broad coverage.

The pattern is useful for reranking experiments. Dense retrieval orders the highest-ranked precedents better, while hybrid retrieval exposes more relevant documents to a second-stage model by combining issue-level similarity with legal term overlap.

### Metric Interpretation for Model Researchers

Because queries have multiple positives, nDCG@10 rewards ranking several relevant precedents early, hit@10 only measures whether at least one relevant case appears in the first ten, and recall@100 measures how much of the relevant set is available for reranking.

For `NanoAILACasedocs`, a high hit@10 alone is not enough. Practical legal retrieval should retrieve a set of precedents covering the main issue and related authorities, so nDCG@10 and recall@100 are both important.

### Query and Relevance Type Tendencies

Queries are long legal fact patterns. Relevant documents are long case-law documents, often with procedural history, facts, issues, reasoning, citations, and holdings. Relevance is based on legal analogy and precedent utility.

The task differs from ordinary semantic search because a relevant document can be long and only partially aligned with the query. Legal issue, statutory context, and procedural posture often matter more than document-wide topical similarity.

### Representative Failure Modes

Common failures include retrieving cases with matching crime names but different legal questions, overranking documents that share procedural phrases, missing precedents with different vocabulary, and ranking only one relevant case when several are needed. BM25 overweights legal boilerplate; dense retrieval may blur fine-grained doctrinal distinctions.

### Training Data That May Help

Useful training data includes legal precedent retrieval, Indian case-law citation graphs, legal issue classification, legal entailment, and hard negatives from cases with similar facts but different holdings. Evaluation queries, judgments, and qrels should be excluded.

### Model Improvement Notes

Models should represent legal issues, statutes, facts, procedural posture, and holdings separately enough to support precedent matching. Hard negatives should share parties, statutes, offences, or procedural language while differing in the controlling issue. Hybrid candidate pools are strong for this task because both rare legal terms and issue-level similarity matter.

## Example Data

| Query | Positive document |
| --- | --- |
| Appellant calls in question legality of the judgment rendered by High Court confirming his conviction for offence and sentence of imprisonment for life as awarded by the learned Sessions Judge. Background facts as unfolded during trial by the prosecution are essentially as follows. One P1 (hereinafter referred to as the 'deceased') was having industry and he employed a number of girls. The accused used to make fun of the girls/workers outside the factory and this was objected to by the deceased... [500 / 3,569 chars] | Kalarimadathil Unni v State of Kerala Supreme Court of India 22 April 1966 Criminal Appeals Nos. 102 & 103 of 1965 The Judgment was delivered by : M. Hidayatullah, J. 1. This judgment will also govern the disposal of Criminal Appeal No. 102 of 1965 (Rajwant Singh v. The State of Kerala). The appellants in these two appeals have been convicted under ss. 302/34, 364, 392, 394 and 447 of the Indian Penal Code. Unni (appellant in this appeal) has been sentenced to death and Rajwant Singh (appellant in the other appeal) has been sentenced to imprisonment for life. No separate sentences under the other sections have been imposed on Unni but Rajwant Singh has been sentenced to four years' rigorous imprisonment under ss. 392 and 394, Indian Penal Code, with a direction that the sentences shall run concurrently with the sentence of imprisonment for life. The High Court of Kerala has dismissed their appeals and confirmed the sentence of death on Unni. They now appeal by special leave of this Cou... [1,000 / 18,777 chars] |
| This appeal, by special leave, has been preferred against the judgment and order dated 23 February 2005 of the High Court (Aurangabad Bench), by which the appeal preferred by the appellants was dismissed and their conviction and sentence of 7 years RI imposed thereunder was affirmed. The deceased P1 was daughter of PW1. P2 resident of village Sanjkheda and she was married to appellant no. 1 P3 son of P4 about two and half years prior to the date of incident which took place on 15 September 1991.... [500 / 3,266 chars] | State of Andhra Pradesh v Thadi Narayana Supreme Court of India 24 July 1961 Criminal Appeal No. 222 of 1959. Appeal by special leave from the judgment and order dated February 24, 1959, of the Andhra Pradesh High Court, Hyderabad, in Criminal Revision Case No. 636 of 1958. AND Criminal Appeal No. 112 of 1961. Appeal by special leave from the Judgment and order dated July 15, 1958, of the Andhra Pradesh High Court in Criminal Appeal No. 237 of 1957. The Judgment was delivered by : P. B. Gajendragadkar, J. 1. The short and interesting question which arises for our decision in the present appeal is in respect of the powers of the High Court in disposing of appeals under s. 423(1) (b) of the Code of Criminal Procedure. In dealing with an appeal preferred by a convicted person against the order of conviction and sentence imposed on him by the trial court can the High Court in exercise of its appellate powers under s. 423(1)(b) reverse the finding of acquittal recorded by the trial court in... [1,000 / 30,909 chars] |
| The appellant before us was examined as prime witness in the trial of T.R. on the file of the Special Judge against the first respondent. The trial ended in conviction against the first respondent and when the appeal filed by him came to be heard by the High Court the appellant had become a Cabinet Minister. On account of the disparaging remarks made by the Appellate Judge the appellant tendered his resignation and demitted office for maintaining democratic traditions. It is in that backgroud th... [500 / 2,857 chars] | R. K. Lakshmanan v A. K. Srinivasan and Another Supreme Court of India 1 August 1975 CRIMINAL APPELLATE JURISDICTION : Criminal Appeal No. 1 30 of 1975. Appeal by Special Leave from the Judgment and Order dated the 13th March, 1974 of the Kerala High Court in Criminal Misc. Petition No. 7 of 1974 with Crl. M.P. No. 967/73. The Judgment was delivered by: R. S. Sarkaria, J. 1. This appeal by special leave is directed against a judgment of the Kerala High Court rejecting the appellant's application under s. 561-A. Criminal Procedure Code for expunction of certain remarks made against him in the High Court's order, dated 20-11-1973, in Criminal Misc. Petition No. 967 of 1973. 2. The appellant is a member of the Kerala Judicial Service, while the respondent herein is an Advocate practising at Ernakulam. On 14-8-1973, the appellant was working as District Magistrate Ernakulam. One Kamaleswaran, who was an accused in C.C. Nos. 216 and 217 of 1973 pending before him, was ordered to be released... [1,000 / 15,791 chars] |

### Source Reference Table

| Title | Year | Type | URL |
| --- | ---: | --- | --- |
| Overview of the FIRE 2019 AILA Track: Artificial Intelligence for Legal Assistance | 2019 | task paper | [https://ceur-ws.org/Vol-2517/T1-1.pdf](https://ceur-ws.org/Vol-2517/T1-1.pdf) |
| AILA 2019 Precedent & Statute Retrieval Task | 2020 | dataset record | [https://doi.org/10.5281/zenodo.4063986](https://doi.org/10.5281/zenodo.4063986) |
| Introducing RTEB: A New Standard for Retrieval Evaluation | 2025 | benchmark article | [https://huggingface.co/blog/rteb](https://huggingface.co/blog/rteb) |

### Representative Snippets

| Query | Relevant document excerpt |
| --- | --- |
| A criminal appeal challenges conviction and life imprisonment confirmed by the High Court. | Kalarimadathil Unni v State of Kerala, Supreme Court of India. |
| An appeal challenges dismissal by the High Court and conviction under criminal charges. | State of Andhra Pradesh v Thadi Narayana, Supreme Court of India. |
| A prime witness in a special judge trial faces proceedings after appeal from conviction. | R. K. Lakshmanan v A. K. Srinivasan and Another, Supreme Court of India. |
| A legal question asks whether sanction is required before criminal proceedings are initiated. | Shambhoo Nath Misra v State of U. P., Supreme Court of India. |
| A civil appeal asks whether distribution of partnership assets on dissolution requires registration. | S. V. Chandra Pandian and Others v S. V. Sivalinga Nadar and Others, Supreme Court of India. |
