# NanoMuPLeR / sv

## Overview

`NanoMuPLeR / sv` is the Swedish split of MuPLeR-retrieval, a multilingual legal retrieval benchmark built from European Union legal passages. Queries are synthetic Swedish legal questions, and documents are Swedish DGT-Acquis passages. Each query has one relevant passage. The split is notable because BM25 and dense retrieval are both very strong and nearly tied, while the hybrid pool delivers the best overall ranking and candidate coverage. It is a useful benchmark for testing whether models can preserve exact Swedish legal anchors while also matching paraphrased legal questions.

## Details

### What the Original Data Measures

MuPLeR-retrieval evaluates multilingual parallel legal retrieval with DGT-Acquis passages and synthetic queries. The source dataset card describes 10,000 passages and 200 queries per language. DGT-Acquis is a European Union multilingual legal corpus documented as part of the EU's parallel-corpus resources.

In this Swedish split, retrieval is same-language and single-positive. The model must find the passage that grounds the requested committee finding, sales calculation, authorization procedure, procurement rule, or advisory position.

### Observed Data Profile

The Nano split contains 200 queries, 10,000 documents, and 200 positive qrel rows. Every query has exactly one positive. Queries average 143.74 characters, while documents average 656.78 characters.

Examples include OLAF de minimis investigations, average affected sales for MEGAL-transported energy, minor changes to marketing authorizations, separation of selection and award criteria in procurement, and a Commission service decision to revive an SME observatory. These cases combine exact institutional terms with legal reasoning and procedural distinctions.

### BM25 Evaluation Profile

The BM25 candidate subset uses top-500 candidates and reaches nDCG@10 of 0.8563, hit@10 of 0.9300, and recall@100 of 0.9600. BM25 is highly competitive because Swedish legal queries and passages share distinctive committee names, dates, procedural labels, market terms, and legal vocabulary.

This strong sparse profile means exact term occurrence is a central signal. A model that improves on BM25 must retain sensitivity to legal phrases and named entities rather than relying only on broad semantic similarity.

### Dense Evaluation Profile

The dense candidate subset from `harrier_oss_v1_270m` uses top-500 candidates and reaches nDCG@10 of 0.8576, hit@10 of 0.9400, and recall@100 of 0.9600. Dense retrieval is essentially tied with BM25 on nDCG@10 and recall@100 and slightly better on hit@10. This indicates that Swedish MuPLeR supports both exact lexical retrieval and semantic paraphrase matching.

Dense retrieval is useful for questions that express a procedural or legal rationale rather than directly repeating the passage wording. It must still distinguish closely related EU passages that share policy vocabulary.

### Reranking Hybrid Evaluation Profile

The `reranking_hybrid` subset uses top-100 candidates, with one row receiving the optional rank-101 safeguard. It reaches nDCG@10 of 0.8946, hit@10 of 0.9450, and recall@100 of 0.9950. Hybrid retrieval is the strongest profile.

The result shows that BM25 and dense retrieval make complementary errors despite similar aggregate scores. Combining them improves candidate coverage and ranking quality, making hybrid search a strong reranking setup for Swedish legal retrieval.

### Metric Interpretation for Model Researchers

Because each query has one positive, nDCG@10 rewards ranking the answer passage very early, hit@10 measures whether it appears in the first ten results, and recall@100 measures whether a reranker can see it. For Swedish MuPLeR, BM25 and dense are both strong first-stage baselines, while hybrid retrieval is the best candidate pool.

Researchers should interpret this split as a high-baseline task. Improvements require both exact handling of Swedish legal terms and robust semantic alignment for procedural paraphrase.

### Query and Relevance Type Tendencies

Queries are formal Swedish questions about committees, energy-market sales, authorization holders, procurement criteria, and SME policy. Relevant documents are translated EU legal and administrative passages with dense institutional language.

Relevance is narrow. A passage from the same legal topic is not sufficient unless it states the exact committee judgment, calculation rationale, procedural action, or advisory position requested.

### Representative Failure Modes

Failures include confusing OLAF oversight findings with other budget-control material, matching MEGAL energy passages without the requested sales-calculation rationale, selecting authorization-change passages with the wrong procedural role, and blurring procurement selection criteria with award criteria. Dense systems can overgeneralize; sparse systems can miss paraphrased legal intent.

### Training Data That May Help

Useful training data includes non-overlapping Swedish EUR-Lex and DGT-Acquis retrieval pairs, Swedish legal QA, multilingual legal bitext, and hard negatives from nearby EU legal provisions or advisory opinions. Evaluation queries and exact positive passages should be excluded.

### Model Improvement Notes

Models should preserve exact Swedish legal names, committee labels, dates, and market terms while learning semantic paraphrase of legal procedures and policy findings. Hard negatives should share the legal field but differ in the requested actor, calculation, condition, or procedural outcome. Hybrid reranking is the strongest evaluation setting for this split.

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
| Which committee judged resources for small internal investigations inefficient and called for selection criteria in the operational-procedure manual? | A passage about the committee's review of OLAF de minimis cases and the resource use for investigations under EUR 50,000. |
| Why did the decision use average affected sales for France instead of the last full year for MEGAL-transported energy? | A passage defining affected gas sales transported through the MEGAL pipeline and explaining the calculation basis. |
| Who informs the authorization holder which minor notification changes were approved or refused so refused changes cease immediately? | A passage stating that the reference member state informs the marketing authorization holder about accepted or rejected minor type IA changes. |
| Why must a supplier's total capacity be assessed only at selection and not reassessed when judging tender quality? | A passage distinguishing selection criteria from award criteria in procurement case law. |
| Which EU advisory assembly welcomed a Commission service decision to revive the observatory for categories of small and medium-sized enterprises? | A passage about the need to know and communicate conditions for different categories of SMEs and base Community policy on clear facts. |
