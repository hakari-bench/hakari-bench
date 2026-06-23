# NanoMuPLeR / fr

## Overview

`NanoMuPLeR / fr` is the French split of MuPLeR-retrieval, a multilingual legal retrieval benchmark built from European Union legal passages. Queries are synthetic French legal questions, and documents are French DGT-Acquis passages. Each query has exactly one relevant passage, so the task measures whether a model can identify the precise legal provision, administrative statement, actor, condition, or product definition that grounds the question. The split is a useful French legal retrieval probe because the corpus contains highly formal translated legal language, while the queries often ask for the answer indirectly through a condition or institutional relationship rather than by repeating a passage title.

## Details

### What the Original Data Measures

MuPLeR-retrieval measures multilingual parallel legal retrieval over DGT-Acquis-derived EU legal text. The source dataset card describes 10,000 human-translated passages and 200 synthetic parallel queries for each language. The DGT-Acquis collection is part of the European Union's multilingual legal resources and is documented in work on highly multilingual EU parallel corpora.

In this French split, retrieval is same-language and single-positive. A model must rank the one French passage that answers the legal question ahead of many passages that may share EU institutions, legal vocabulary, products, directives, or procedural language.

### Observed Data Profile

The Nano split contains 200 queries, 10,000 documents, and 200 positive qrel rows. Every query has exactly one positive passage. Queries average 141.22 characters, while documents average 746.43 characters.

The examples cover transaction internalisation in regulatory investigations, parity as a democratic governance norm, clauses assessed under EC and EEA competition rules, recognition of regulated health professions, and a named cured meat whose name derives from hunting terminology. This produces a mix of legal-procedural, institutional, and definitional retrieval.

### BM25 Evaluation Profile

The BM25 candidate subset uses top-500 candidates and reaches nDCG@10 of 0.8179, hit@10 of 0.9150, and recall@100 of 0.9800. This is a strong sparse baseline. French EU legal text preserves distinctive terminology, article references, institutional names, and specialized product or policy terms, so exact term frequency is often enough to locate the correct passage.

The remaining gap shows that the task is not only a keyword lookup. Some questions paraphrase the relevant legal condition, ask for the implication of an investigation, or mention a concept that is distributed across a longer passage. BM25 can retrieve a near legal neighbor that shares terminology but fails to satisfy the exact requested condition.

### Dense Evaluation Profile

The dense candidate subset from `harrier_oss_v1_270m` uses top-500 candidates and reaches nDCG@10 of 0.8329, hit@10 of 0.9150, and recall@100 of 0.9550. Dense retrieval improves top-rank ordering over BM25, but its recall@100 is lower. This suggests that embedding similarity helps when the question paraphrases a legal relation, while sparse matching still contributes broader candidate coverage for some exact-reference cases.

Dense retrieval is especially relevant for questions whose answer is expressed through legal reasoning or descriptive phrasing rather than repeated surface words. It may, however, over-rank passages from the same legal area when several provisions are semantically close.

### Reranking Hybrid Evaluation Profile

The `reranking_hybrid` subset uses top-100 candidates, with one row receiving the optional rank-101 safeguard. It reaches nDCG@10 of 0.8628, hit@10 of 0.9350, and recall@100 of 0.9950. It is the strongest profile for this split, combining the lexical coverage of BM25 with the semantic matching strength of dense retrieval.

This pattern is important for reranking research. French MuPLeR benefits from hybrid candidate construction because either sparse or dense retrieval alone can miss some positives, while their union gives a reranker a more complete candidate set and better early precision.

### Metric Interpretation for Model Researchers

Because there is one positive per query, hit@10 is an intuitive success rate for placing the answer passage in the first ten results, and nDCG@10 reflects how early that single passage appears. Recall@100 is best interpreted as candidate availability for a later reranker.

For this split, BM25 is already high, dense is slightly better at top rank, and hybrid retrieval is best overall. A model that beats the hybrid profile must handle both exact French legal terminology and semantic paraphrase of legal conditions.

### Query and Relevance Type Tendencies

Queries are formal French questions that usually ask for a specific actor, clause, country, product, or legal conclusion. Relevant passages are translated EU legal or administrative texts, often with long sentences and dense nominal phrases.

The relevance relation is exact grounding. A passage can share the same directive, market, product category, or institutional context and still be wrong if it does not answer the particular condition in the query.

### Representative Failure Modes

Likely failures include matching the right legal field but the wrong clause, selecting a nearby procedural statement instead of the requested finding, confusing similar product definitions, and overvaluing shared institutional names. Dense models may blur adjacent legal provisions; sparse models may miss paraphrased descriptions of the same legal action.

### Training Data That May Help

Useful training data includes non-overlapping French EUR-Lex or DGT-Acquis retrieval pairs, French legal QA, multilingual legal bitext, and hard negatives from the same EU legal topic. Training should exclude the evaluation queries and exact positive passages.

### Model Improvement Notes

French legal retrieval models should retain sensitivity to exact legal tokens, dates, names, and product terms while learning to align paraphrased legal questions with long formal passages. Hard negatives should share many words with the positive passage but differ in the requested actor, obligation, clause, or condition. Hybrid retrieval is a strong candidate-generation setting for this split.

## Example Data

| Query | Positive document |
| --- | --- |
| Quelles deux constatations de l'enquête réglementaire ont miné l'affirmation des opérateurs selon la... [100 / 169 chars] | Pour les parties notifiantes, il existe une solution sérieuse pour les ORM, celle de l'auto-approvisionnement puisque les ORM possèdent à l'intérieur de leur entreprise les capacités et le savoir-fair... [200 / 726 chars] |
| Quelle chambre régionale est nommée avec les institutions de l'Union pour promouvoir la parité comme... [100 / 141 chars] | Pour être efficace et significative, la démocratie doit garantir la possibilité de pleine participation des citoyens aux décisions finales contraignantes qui concernent leur vie quotidienne. Tant que... [200 / 664 chars] |
| Quelles deux clauses la Commission, dans l'évaluation préliminaire, a‑t‑elle jugées potentiellement... [100 / 156 chars] | Il ressort de l'évaluation préliminaire de la Commission que deux des clauses de la convention soulèvent des doutes sérieux quant à leur compatibilité avec l'article 81 du traité CE et l'article 53 de... [200 / 656 chars] |
| Quel pays a omis d'appliquer les règles de reconnaissance de l'UE aux professions sanitaires régleme... [100 / 122 chars] | juger, qu'en n'omettant de prendre les mesures législatives et réglementaires nécessaires, ou de les communiquer à la Commission, la République fédérale d'Allemagne a méconnu ses obligations de transp... [200 / 795 chars] |
| Quelle pièce de charcuterie dont l'étymologie remonte à des termes désignant des chasseurs est une r... [100 / 138 chars] | Le nom kiełbasa myśliwska reflète les caractéristiques spécifiques du produit. Les caractéristiques spécifiques exprimées par ce nom transparaissent dans l’origine étymologique de ce dernier, qui vien... [200 / 730 chars] |

### Source Reference Table

| Title | Year | Type | URL |
| --- | ---: | --- | --- |
| MuPLeR: Multilingual Parallel Legal Retrieval |  | dataset card | [https://huggingface.co/datasets/mteb/MuPLeR-retrieval](https://huggingface.co/datasets/mteb/MuPLeR-retrieval) |
| An overview of the European Union's highly multilingual parallel corpora | 2014 | source paper | [https://link.springer.com/article/10.1007/s10579-014-9277-0](https://link.springer.com/article/10.1007/s10579-014-9277-0) |
| DGT-Acquis |  | source corpus | [https://joint-research-centre.ec.europa.eu/language-technology-resources/dgt-acquis_en](https://joint-research-centre.ec.europa.eu/language-technology-resources/dgt-acquis_en) |

### Representative Snippets

| Query | Relevant document excerpt |
| --- | --- |
| Which two findings in a regulatory investigation undermined operators' claim that they could internalize transaction settlement? | A passage explaining why notifying parties viewed self-supply as an option for ORM operators, while the Commission's investigation found limits to that claim. |
| Which regional chamber is named with EU institutions in presenting parity as an ethical norm for political governance? | A passage arguing that meaningful democracy requires full citizen participation and equal access to binding decisions. |
| Which two clauses did the Commission preliminarily consider potentially incompatible with EC and EEA competition rules? | A passage describing the Commission's preliminary assessment of two contractual clauses under Article 81 EC and Article 53 EEA. |
| Which country failed to apply EU recognition rules to regulated health and related professions? | A passage concerning Germany's obligations to transpose rules for regulated health professions and communicate measures to the Commission. |
| Which cured meat has an etymology linked to hunters and is described as a portable long-keeping ration? | A passage explaining the origin and product characteristics of `kielbasa mysliwska` as a hunter-associated sausage. |
