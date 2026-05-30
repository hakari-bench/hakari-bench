# NanoMuPLeR / lt

## Overview

`NanoMuPLeR / lt` is the Lithuanian split of MuPLeR-retrieval, a multilingual legal retrieval benchmark based on European Union legal passages. Queries are synthetic Lithuanian legal questions, and documents are Lithuanian DGT-Acquis passages. Each query has one relevant passage, so the task evaluates exact grounding rather than broad topical retrieval. The split is valuable for model researchers because sparse matching remains highly competitive, dense retrieval has weaker candidate coverage, and the hybrid pool gives the best top-rank profile.

## Details

### What the Original Data Measures

MuPLeR-retrieval measures same-language legal passage retrieval across multiple European languages. The source dataset card describes 10,000 DGT-Acquis passages and 200 synthetic parallel queries per language. DGT-Acquis is a European Union multilingual legal corpus and is documented as part of the EU's highly multilingual parallel resources.

In this Lithuanian split, the model must connect a legal question to the single passage that states the relevant tax rule, procedural deadline, governance structure, institutional action, or legal obligation.

### Observed Data Profile

The Nano split contains 200 queries, 10,000 documents, and 200 positive qrel rows. Each query has exactly one positive. Queries average 143.04 characters, while documents average 621.81 characters.

The examples include harmonized minimum excise duty for gas oil and petrol, remaining capital duty on intra-EU imports, governance of a metrology research pilot, a deadline for interested parties to preserve procedural rights, and procedural-rights protection in criminal proceedings. This makes the split a mix of numeric, procedural, institutional, and policy-grounding retrieval.

### BM25 Evaluation Profile

The BM25 candidate subset uses top-500 candidates and reaches nDCG@10 of 0.8115, hit@10 of 0.8750, and recall@100 of 0.9650. BM25 is the stronger standalone ranking profile than dense retrieval by nDCG@10 and recall@100. Lithuanian legal passages contain many exact anchors: dates, percentages, EU institutions, regulation names, deadlines, and formal legal nouns.

This suggests that term occurrence remains highly informative for this split. A sparse system can often locate the right provision when the query preserves enough distinctive legal vocabulary, even if the document is long and formal.

### Dense Evaluation Profile

The dense candidate subset from `harrier_oss_v1_270m` uses top-500 candidates and reaches nDCG@10 of 0.7495, hit@10 of 0.8800, and recall@100 of 0.9300. Dense retrieval slightly improves hit@10 over BM25 but has lower nDCG@10 and lower recall@100. This means it often finds the positive somewhere in the top ten but is less reliable at placing it very early and less complete as a candidate source.

The profile indicates that semantic similarity alone can blur neighboring EU legal passages in Lithuanian. Dense models need better handling of legal morphology, named provisions, and exact numeric or procedural constraints.

### Reranking Hybrid Evaluation Profile

The `reranking_hybrid` subset uses top-100 candidates, with three rows receiving the optional rank-101 safeguard. It reaches nDCG@10 of 0.8442, hit@10 of 0.9350, and recall@100 of 0.9850. This is the strongest setting for this split.

Hybrid retrieval works because BM25 supplies exact legal anchors while dense retrieval adds paraphrase coverage for questions whose wording differs from the passage. The result is not merely an average of two systems: it gives a reranker access to positives that either standalone method may rank too low.

### Metric Interpretation for Model Researchers

Because there is one positive per query, nDCG@10 and hit@10 measure the early placement of a single answer passage. Recall@100 indicates whether a reranker can see that passage at all. For Lithuanian MuPLeR, BM25 is a strong first-stage baseline, dense retrieval is weaker by nDCG and recall, and hybrid retrieval is the best candidate profile.

Researchers should treat this split as a test of exact legal anchoring under Lithuanian morphology and formal EU translation style. Improvements should not sacrifice sparse-style precision on dates, percentages, and institutional names.

### Query and Relevance Type Tendencies

Queries are formal Lithuanian questions that often ask for a date, rate, institution, deadline, governance arrangement, or procedural endorsement. Relevant passages are EU legal or administrative texts with compact translated phrasing and many named legal concepts.

The relevance relation is narrow. Related provisions in the same legal instrument can be hard negatives if they do not answer the exact condition or entity requested.

### Representative Failure Modes

Common failures include matching the right regulation but the wrong threshold, selecting a passage about a similar procedure with a different deadline, confusing EU bodies with overlapping roles, and ranking general policy language above a passage that states the requested fact. Dense retrieval can overgeneralize; sparse retrieval can miss paraphrased legal intent.

### Training Data That May Help

Useful training data includes non-overlapping Lithuanian EUR-Lex and DGT-Acquis retrieval pairs, Lithuanian legal QA, multilingual legal bitext, and hard negatives from adjacent EU provisions. Evaluation queries and exact positive passages should be excluded.

### Model Improvement Notes

Models should combine robust Lithuanian lexical matching with semantic alignment for legal paraphrase. Hard negatives should share the legal field and much of the vocabulary while differing in the requested condition, deadline, institution, or amount. This split favors hybrid candidate generation for downstream reranking.

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
| When was a harmonized minimum excise duty of EUR 380 per cubic meter for gas oil and petrol supposed to enter into force? | A passage about amending Directive 2003/96/EC and gradually increasing the minimum excise level for gas oil used as motor fuel. |
| Which intra-EU import tax was still applied by seven member states, with rates around 0.5%, 0.6%, and 1%? | A passage explaining that most member states had abolished the tax while seven still applied it at specified rates. |
| What governance structure was proposed for a short-term metrology research pilot limited to 2013? | A passage about implementing a pilot European metrology research project based on iMERA Plus and preparatory work. |
| How long do interested parties have to make themselves known after publication in order to preserve procedural rights? | A passage stating that interested parties generally have 40 days after publication in the Official Journal to contact the Commission. |
| Which EU body endorsed the Council-approved roadmap for strengthening procedural rights and included it in the Stockholm Programme? | A passage about the protection of suspects' and accused persons' rights as a core Union value and part of the roadmap. |
