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
| A criminal appeal challenges conviction and life imprisonment confirmed by the High Court. | Kalarimadathil Unni v State of Kerala, Supreme Court of India. |
| An appeal challenges dismissal by the High Court and conviction under criminal charges. | State of Andhra Pradesh v Thadi Narayana, Supreme Court of India. |
| A prime witness in a special judge trial faces proceedings after appeal from conviction. | R. K. Lakshmanan v A. K. Srinivasan and Another, Supreme Court of India. |
| A legal question asks whether sanction is required before criminal proceedings are initiated. | Shambhoo Nath Misra v State of U. P., Supreme Court of India. |
| A civil appeal asks whether distribution of partnership assets on dissolution requires registration. | S. V. Chandra Pandian and Others v S. V. Sivalinga Nadar and Others, Supreme Court of India. |
