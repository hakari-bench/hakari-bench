# NanoMuPLeR / sk

## Overview

`NanoMuPLeR / sk` is the Slovak split of MuPLeR-retrieval, a multilingual legal retrieval benchmark built from European Union legal passages. Queries are synthetic Slovak legal questions, and documents are Slovak DGT-Acquis passages. Each query has exactly one relevant passage. Compared with several other MuPLeR language splits, BM25 is weaker here, dense retrieval provides a clear improvement, and the hybrid pool is strongest. This makes the split useful for studying how Slovak morphology, translation variation, and paraphrased legal questions affect sparse and dense retrieval.

## Details

### What the Original Data Measures

MuPLeR-retrieval evaluates same-language legal passage retrieval across 14 European languages. The source dataset card describes DGT-Acquis-derived passages paired with synthetic parallel legal queries. DGT-Acquis is a European Union multilingual legal corpus and is documented in work on EU parallel corpora.

For Slovak, the retrieval system must identify the one passage that answers a legal or administrative question, even when many candidate passages discuss similar EU policies, institutions, or procedural rules.

### Observed Data Profile

The Nano split contains 200 queries, 10,000 documents, and 200 positive qrel rows. Each query has one positive. Queries average 136.25 characters, while documents average 628.24 characters.

Examples cover a three-level prevention framework for mental health, EU-backed responses to managerial misconduct, EFTA Surveillance Authority discussion of unsettled case law, a Commission movement-management application for NCTS, and voluntary corporate social responsibility commitments through European works councils.

### BM25 Evaluation Profile

The BM25 candidate subset uses top-500 candidates and reaches nDCG@10 of 0.7041, hit@10 of 0.7850, and recall@100 of 0.8950. BM25 is useful because legal passages still contain distinctive institutional names, treaty concepts, and procedural vocabulary, but it is much less dominant than in Dutch, Latvian, or Polish.

This weaker sparse profile suggests that Slovak query wording and passage wording often diverge enough to reduce exact-match effectiveness. Morphology, translated phrasing, and paraphrased question construction can separate the query terms from the terms used in the relevant passage.

### Dense Evaluation Profile

The dense candidate subset from `harrier_oss_v1_270m` uses top-500 candidates and reaches nDCG@10 of 0.7714, hit@10 of 0.8600, and recall@100 of 0.9450. Dense retrieval improves over BM25 on all reported metrics. Embedding similarity appears to capture legal paraphrase and conceptual overlap that sparse matching misses.

Dense retrieval is therefore the stronger standalone first-stage method for this split. It is especially useful for long questions that describe a policy relation, institutional role, or procedural purpose rather than quoting the passage directly.

### Reranking Hybrid Evaluation Profile

The `reranking_hybrid` subset uses top-100 candidates, with four rows receiving the optional rank-101 safeguard. It reaches nDCG@10 of 0.7872, hit@10 of 0.8800, and recall@100 of 0.9800. Hybrid retrieval is the strongest profile, improving candidate coverage and early ranking over dense retrieval.

The improvement shows that BM25 still adds complementary exact anchors even when it is weaker overall. The best reranking pool combines dense semantic coverage with sparse legal names, acronyms, and institutional terms.

### Metric Interpretation for Model Researchers

Because each query has one positive, nDCG@10 and hit@10 measure how reliably the correct passage is placed near the top. Recall@100 indicates whether a reranker can access the positive. For Slovak MuPLeR, BM25 is a relatively weak baseline, dense retrieval is the stronger standalone method, and hybrid retrieval is the best candidate-generation target.

This split is particularly useful for testing multilingual dense models and hybrid retrieval methods in a language where surface matching alone is not enough.

### Query and Relevance Type Tendencies

Queries are formal Slovak legal questions about health policy, committees, case law, customs movement systems, and corporate responsibility. Relevant passages are translated EU legal or advisory texts with long, formal clauses.

The relevance relation is strict. A candidate must answer the exact institutional, procedural, or policy relation in the question, not merely share the same EU topic.

### Representative Failure Modes

Failures include retrieving a health-policy passage without the requested prevention framework, confusing committees or supervisory bodies, matching a customs-system paragraph that lacks the requested movement-management role, and ranking broad corporate-responsibility discussion above the specific works-council commitment. Sparse systems miss paraphrase; dense systems may over-rank adjacent legal concepts.

### Training Data That May Help

Useful training data includes non-overlapping Slovak EUR-Lex and DGT-Acquis retrieval pairs, Slovak legal QA, multilingual legal bitext, and hard negatives from related EU acts and advisory opinions. Evaluation queries and exact positives should be excluded.

### Model Improvement Notes

Models should improve Slovak legal semantic matching while retaining exact sensitivity to institutional names, acronyms, dates, and treaty references. Hard negatives should be selected from the same EU legal domain but differ in the requested actor, legal basis, or procedural condition. Hybrid reranking is the most informative evaluation setup for this split.

## Example Data

### Public Sources

- [mteb/MuPLeR-retrieval](https://huggingface.co/datasets/mteb/MuPLeR-retrieval), source dataset card.
- [An overview of the European Union's highly multilingual parallel corpora](https://link.springer.com/article/10.1007/s10579-014-9277-0), DGT-Acquis source reference.
- [DGT-Acquis](https://joint-research-centre.ec.europa.eu/language-technology-resources/dgt-acquis_en), European Commission source-corpus page.

### Source Reference Table

| Title | Year | Type | URL |
| --- | ---: | --- | --- |
| MuPLeR: Multilingual Parallel Legal Retrieval |  | dataset card | https://huggingface.co/datasets/mteb/MuPLeR-retrieval |
| An overview of the European Union's highly multilingual parallel corpora | 2014 | source paper | https://link.springer.com/article/10.1007/s10579-014-9277-0 |
| DGT-Acquis |  | source corpus | https://joint-research-centre.ec.europa.eu/language-technology-resources/dgt-acquis_en |

### Representative Snippets

| Query | Relevant document excerpt |
| --- | --- |
| Which three-level intervention scheme is proposed together with mental-health promotion, healthy lifestyles, and supportive environments? | A passage emphasizing primary, secondary, and tertiary prevention and initiatives for mental-health promotion. |
| Which committee called for EU-backed measures to remedy management skill and ethics failures after loss of employee and consumer trust? | A passage about a crisis of confidence after misconduct by managers and management structures in the European Community. |
| Which authority explains policy on unresolved case law without prejudging interpretation by regional and Community courts? | A passage outlining the state of EFTA and European Community Court case law and the EFTA Surveillance Authority's policy. |
| Which supervisory body supplied a standalone movement-management solution and later inspected goods movement between regimes in 2006? | A passage describing the Commission-created MCC application as a standalone system for NCTS-related transit management. |
| How do European works councils embed corporate social responsibility commitments through voluntary negotiation, including subcontractor workers and suppliers? | A passage about negotiated CSR commitments in transnational companies with European works councils. |
