# NanoMuPLeR / pt

## Overview

`NanoMuPLeR / pt` is the Portuguese split of MuPLeR-retrieval, a multilingual legal retrieval benchmark based on European Union legal passages. Queries are synthetic Portuguese legal questions, and documents are Portuguese DGT-Acquis passages. Each query has exactly one relevant passage, so the task measures whether a retriever can identify the precise legal condition, actor, threshold, model, or administrative rule that answers the question. The split is useful because dense retrieval is stronger than BM25, while hybrid retrieval improves still further by combining semantic and lexical evidence.

## Details

### What the Original Data Measures

MuPLeR-retrieval measures multilingual legal passage retrieval over DGT-Acquis-derived European Union text. The source dataset card describes 10,000 passages and 200 synthetic parallel queries for each language. DGT-Acquis is part of the EU's multilingual legal corpus resources and is documented in work on highly multilingual parallel corpora.

For Portuguese, retrieval is same-language and single-positive. A model must rank the passage that grounds a legal question above other EU passages that may share the same institution, policy area, product, or legal vocabulary.

### Observed Data Profile

The Nano split contains 200 queries, 10,000 documents, and 200 positive qrel rows. Each query has one positive. Queries average 135.46 characters, while documents average 702.90 characters.

Examples include regional state aid proportionality, small and medium enterprise wording in accession documents, criticism of the 1983 Baxter model for interchange fees, cosmetic revisions in marketing-authorization files, and retroactive state compensation without objective prior criteria. The split mixes competition law, state aid, market authorization, and administrative interpretation.

### BM25 Evaluation Profile

The BM25 candidate subset uses top-500 candidates and reaches nDCG@10 of 0.8222, hit@10 of 0.8950, and recall@100 of 0.9750. BM25 is strong because many Portuguese questions retain legal terms, percentages, dates, institutional names, and specialized phrases from the positive passage.

However, BM25 is not the strongest standalone profile. The questions often compress or paraphrase long legal reasoning, so exact term overlap can retrieve a nearby provision without placing the answer passage first.

### Dense Evaluation Profile

The dense candidate subset from `harrier_oss_v1_270m` uses top-500 candidates and reaches nDCG@10 of 0.8552, hit@10 of 0.9300, and recall@100 of 0.9750. Dense retrieval improves top-rank quality and hit@10 while matching BM25's recall@100. This indicates that Portuguese MuPLeR has many cases where embedding similarity captures the legal relation better than term frequency alone.

Dense retrieval is especially helpful for argumentative and explanatory passages, such as state-aid proportionality or competition-policy models, where the query asks for a legal rationale rather than a surface phrase.

### Reranking Hybrid Evaluation Profile

The `reranking_hybrid` subset uses top-100 candidates, with two rows receiving the optional rank-101 safeguard. It reaches nDCG@10 of 0.8895, hit@10 of 0.9650, and recall@100 of 0.9900. This is the strongest profile for the split.

The hybrid result shows that dense retrieval supplies strong semantic ranking while BM25 still contributes exact legal anchors and complementary coverage. A reranker should benefit from the combined pool, especially for questions involving both precise numbers and paraphrased legal consequences.

### Metric Interpretation for Model Researchers

With one positive per query, nDCG@10 reflects how early the correct passage appears, hit@10 measures whether it is in the first ten results, and recall@100 measures candidate availability for reranking. For Portuguese MuPLeR, dense retrieval is the stronger standalone ranker, and hybrid retrieval is the best candidate-generation setting.

This makes the split a useful test for models that claim to improve semantic legal retrieval without losing exact-match behavior on EU terminology, dates, and institutional references.

### Query and Relevance Type Tendencies

Queries are formal Portuguese legal questions about aid proportionality, accession wording, economic models, authorization-file revisions, and Treaty rules on state aid. Relevant passages are formal EU legal or administrative texts that often explain a rule through long clauses.

The relevance relation is exact. A passage may share the same legal domain or vocabulary and still be wrong if it does not answer the requested condition or rationale.

### Representative Failure Modes

Failures include retrieving a related aid provision without the proportionality rule, matching the same economic topic but the wrong model assumption, confusing authorization-file procedures, or selecting a state-aid passage that lacks the requested objective-criteria condition. Sparse systems miss paraphrase; dense systems can overgeneralize among nearby legal topics.

### Training Data That May Help

Useful training data includes non-overlapping Portuguese EUR-Lex and DGT-Acquis retrieval pairs, Portuguese legal QA, multilingual legal bitext, and hard negatives from adjacent EU acts or opinions. Evaluation queries and exact positive passages should be excluded.

### Model Improvement Notes

Portuguese legal retrieval models should preserve exact legal names, percentages, dates, and institutions while learning semantic alignment for legal rationale and procedural paraphrase. Hard negatives should share the same policy area and many surface terms but fail the requested legal condition. Hybrid candidate generation is the strongest setup for downstream reranking.

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
| Why must scarce public aid be proportional, targeted to disadvantaged regions, and justified despite greater distortion of competition? | A passage explaining that regional aid is effective only when used sparingly, proportionally, and concentrated on the most disadvantaged EU regions. |
| What intention is signaled by comments extending a concession to firms with intra-Community turnover below a six-digit euro amount? | A passage noting that Commission references to small and medium enterprises may indicate a clear intention beyond wording in accession protocols. |
| Which 1983 analytical model is criticized for assuming uniform benefits to merchants, buyers, and non-reactive sellers in payments? | A passage explaining limitations of William Baxter's model underlying MasterCard interchange fees. |
| When may cosmetic revisions to an approval file be included in an amendment to that part rather than submitted separately? | A passage defining changes to a marketing authorization dossier and when modifications may be included together. |
| When does retroactive payment for member-state losses without prior objective and transparent criteria constitute prohibited state aid? | A passage stating that compensation parameters must be established objectively and transparently in advance to avoid an economic advantage. |
