# NanoMuPLeR / lv

## Overview

`NanoMuPLeR / lv` is the Latvian split of MuPLeR-retrieval, a multilingual legal retrieval task built from European Union legal passages. Queries are synthetic Latvian legal questions, and documents are Latvian DGT-Acquis passages. Each query has exactly one relevant passage, so the benchmark tests whether a model can place the correct legal or administrative passage at the top of a dense field of similar EU material. The split is especially useful because BM25 is very strong, dense retrieval is weaker, and the hybrid candidate set recovers perfect top-100 coverage.

## Details

### What the Original Data Measures

MuPLeR-retrieval evaluates legal passage retrieval across parallel European-language corpora. The source dataset card describes 10,000 DGT-Acquis passages and 200 synthetic parallel queries per language. DGT-Acquis is part of the European Union's multilingual legal corpus resources and is associated with documented EU parallel corpora.

For Latvian, the retrieval problem is same-language and single-positive. The model must find the passage that states the requested legal clause, funding instruction, committee finding, policy instrument, or regulatory definition.

### Observed Data Profile

The Nano split contains 200 queries, 10,000 documents, and 200 positive qrel rows. Each query has one positive. Queries average 140.47 characters, while documents average 608.95 characters.

The examples cover social clauses in Union policy, dissemination of digital competence projects, OLAF de minimis investigations, excise duties on tobacco products, and telecommunications dominance criteria. The passages are formal EU legal and advisory texts with many institutional and numeric anchors.

### BM25 Evaluation Profile

The BM25 candidate subset uses top-500 candidates and reaches nDCG@10 of 0.8376, hit@10 of 0.8900, and recall@100 of 0.9700. This is a very strong sparse profile. Latvian queries and passages share enough distinctive legal vocabulary, named institutions, percentages, and policy phrases for term-frequency matching to be highly effective.

BM25 is stronger than the dense profile across nDCG@10, hit@10, and recall@100. For this split, exact wording and legal anchors are not incidental features; they are central signals for retrieval.

### Dense Evaluation Profile

The dense candidate subset from `harrier_oss_v1_270m` uses top-500 candidates and reaches nDCG@10 of 0.7910, hit@10 of 0.8750, and recall@100 of 0.9550. Dense retrieval remains useful but is weaker than BM25. It can recognize paraphrased legal questions, but it appears more vulnerable to ranking legally adjacent passages above the exact answer.

This profile highlights a multilingual dense-retrieval challenge. Semantic similarity must preserve fine-grained distinctions between EU bodies, policy instruments, legal thresholds, and procedural claims in Latvian.

### Reranking Hybrid Evaluation Profile

The `reranking_hybrid` subset uses top-100 candidates with no safeguard rows. It reaches nDCG@10 of 0.8672, hit@10 of 0.9450, and recall@100 of 1.0000. The hybrid candidate pool is the strongest setting and gives complete positive coverage within the top 100.

The result shows why hybrid search matters even when BM25 is the better standalone ranker. Sparse retrieval supplies exact legal matching, while dense retrieval adds complementary semantic coverage. Together they create a better reranking pool than either list alone.

### Metric Interpretation for Model Researchers

With one positive per query, nDCG@10 rewards ranking the answer passage very early, hit@10 measures whether it appears in the first ten results, and recall@100 measures whether a reranker can access it. For Latvian MuPLeR, BM25 is the stronger standalone baseline, but hybrid retrieval is the target candidate-generation profile.

Researchers should use this split to test whether dense or reranking models can retain the lexical exactness of legal retrieval while improving over sparse matching on paraphrased questions.

### Query and Relevance Type Tendencies

Queries are formal Latvian legal questions. They often ask for a clause, committee, instrument, dissemination plan, tax-policy justification, or regulatory criterion. Relevant documents are EU legal, advisory, and administrative passages with compact translated phrasing.

The relevance relation is strict. A passage about the same EU program, committee, or market can still be wrong if it does not answer the exact fact requested in the query.

### Representative Failure Modes

Typical failures include overmatching shared institutional names, retrieving a related policy paragraph without the requested criterion, confusing committee findings, and selecting passages that mention the same market but not the same regulatory basis. Dense systems can conflate related provisions; sparse systems can miss paraphrase or broader legal framing.

### Training Data That May Help

Useful training data includes non-overlapping Latvian EUR-Lex and DGT-Acquis retrieval pairs, Latvian legal QA, multilingual EU legal bitext, and hard negatives from the same directive, committee domain, or market sector. Evaluation query-passage pairs should be excluded.

### Model Improvement Notes

Models should handle Latvian legal morphology, exact institutional names, numeric conditions, and semantic paraphrase together. Hard negatives should be drawn from adjacent EU legal passages that share vocabulary but differ in the requested clause or actor. The perfect hybrid recall@100 makes this split a strong reranking benchmark.

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
| Which Union clause requires consideration of employment, social protection, exclusion, education, and health requirements? | A passage explaining the social clause that applies when the Union defines and implements policies and activities. |
| How should proposals plan sustainable dissemination of existing digital competence projects, including intermediaries and narrative and numeric indicators? | A passage instructing proposals to focus on effective and sustainable dissemination and use of project results. |
| Which committee concluded that allocating resources to minor internal investigations was inefficient and called for selection criteria in the procedure manual? | A passage about the Supervisory Committee reviewing OLAF de minimis policy and cases with limited financial impact. |
| Which EU advisory committee supports Commission efforts to include health and social impacts in tobacco excise taxation? | A passage explaining the modern public-health and social-policy role of excise duties on tobacco. |
| Which regulatory framework allowed authorities to find dominance around a 25% market share given customer access and financial strength? | A passage about the 1998 telecommunications regulatory framework and ex ante market definitions. |
