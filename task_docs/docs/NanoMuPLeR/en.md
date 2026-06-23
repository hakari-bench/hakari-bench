# NanoMuPLeR / en

## Overview

`NanoMuPLeR / en` is the English split of MuPLeR-retrieval, a multilingual legal retrieval task built from European Union legal passages. Queries are synthetic English legal questions, and documents are English DGT-Acquis passages. Each query has one positive passage that grounds the legal condition, institution, date, threshold, or procedural rule named in the question. The split is useful as an English baseline for the parallel MuPLeR family: compared with other languages, it shows how well sparse, dense, and hybrid retrieval behave when the legal corpus and query language are both English but the questions remain synthetic and legally specific.

## Details

### What the Original Data Measures

MuPLeR-retrieval measures multilingual parallel legal retrieval. The source dataset card describes 10,000 DGT-Acquis passages and 200 synthetic parallel queries for each language. DGT-Acquis is part of the European Union's multilingual parallel legal resources.

In this English split, retrieval is same-language and single-positive. The system must find the passage that answers a synthetic legal question.

### Observed Data Profile

The Nano split contains 200 queries, 10,000 documents, and 200 positive qrel rows. Each query has exactly one positive. Queries average 134.87 characters, while documents average 650.58 characters.

The examples ask about movement-management systems, EU-backed responses to management misconduct, sustainable tourism rationale, import thresholds, and STABEX account controls. Documents are formal EU legal or administrative passages.

### BM25 Evaluation Profile

The BM25 candidate subset uses top-500 candidates and reaches nDCG@10 of 0.6453, hit@10 of 0.7350, and recall@100 of 0.9000. BM25 is useful because queries often preserve exact institutional terms, numbers, and legal vocabulary from the positive passage.

However, the English questions are not simple title lookups. They can paraphrase the legal condition or ask for an inferred actor, rationale, or procedure. BM25 therefore misses cases where legal meaning is expressed differently despite shared topic terms.

### Dense Evaluation Profile

The dense candidate subset from `harrier_oss_v1_270m` uses top-500 candidates and reaches nDCG@10 of 0.8477, hit@10 of 0.9600, and recall@100 of 0.9750. Dense retrieval is much stronger than BM25 across all metrics. This suggests that English legal semantic matching is especially effective for the synthetic query style.

Dense retrieval better handles paraphrased legal conditions, institutional actions, and long-form procedural wording. It is the strongest standalone first-stage method for this split.

### Reranking Hybrid Evaluation Profile

The `reranking_hybrid` subset uses top-100 candidates with no safeguard positives. It reaches nDCG@10 of 0.7986, hit@10 of 0.8900, and recall@100 of 1.0000. The hybrid pool has perfect recall@100 but lower top-rank quality than dense retrieval.

This separates candidate coverage from ranking quality. Hybrid retrieval is ideal for reranking coverage, while dense retrieval is better as a first-stage ranked list.

### Metric Interpretation for Model Researchers

Because each query has one positive, nDCG@10 and hit@10 directly reflect ranking the exact passage early. Recall@100 indicates whether a reranker can see the positive. Dense retrieval is the top-rank baseline to beat, but hybrid retrieval is the coverage baseline.

The contrast between dense and BM25 in English is useful when comparing against other MuPLeR language splits, where morphology and translation may alter the sparse-dense balance.

### Query and Relevance Type Tendencies

Queries are formal English legal questions. Relevant documents are EU legal passages with administrative, budgetary, trade, social-policy, or procedural content.

The relevance relation is exact grounding of a legal condition. A passage from the same legal area is not sufficient if it does not answer the requested actor, condition, or threshold.

### Representative Failure Modes

Common failures include retrieving a related EU provision with the wrong institution, matching numeric thresholds without the right category, and confusing similar administrative procedures. Sparse systems struggle with paraphrase; dense systems may overgeneralize among legally adjacent provisions.

### Training Data That May Help

Useful training data includes non-overlapping English EUR-Lex and DGT-Acquis retrieval pairs, legal QA data, multilingual legal alignment data, and hard negatives from similar EU provisions. MuPLeR evaluation queries and exact positive passages should be excluded.

### Model Improvement Notes

Models should preserve exact legal references while learning semantic paraphrase of legal actions and conditions. Hard negatives should come from the same legal domain and share terminology, but fail to satisfy the query's exact condition. Hybrid pools are valuable for reranking even when dense retrieval is the stronger first-stage ranker.

## Example Data

| Query | Positive document |
| --- | --- |
| Which oversight body supplied a standalone movement-management solution while later inspecting count... [100 / 142 chars] | In the beginning of the NCTS project several Member States not wishing to develop a national transit application requested the Commission to produce a standard one. MCC as supplied by the Commission i... [200 / 799 chars] |
| Which committee urged EU-backed measures to remedy leadership skill and ethics failings after miscon... [100 / 150 chars] | The crisis of confidence among employees and consumers is made worse in many countries of the European Union by revelations about mistakes and impropriety on the part of managers and entire management... [200 / 695 chars] |
| Which rationale links consensus on sector growth caps to both environmental resilience and long-term... [100 / 147 chars] | The arguments presented in the communication in support of the Agenda seem appropriate, in that they assess both the economic impact of tourism and its ability to create jobs for young people and also... [200 / 707 chars] |
| What does the EU executive do when pro-rated, category-specific inflows exceed set thresholds over a... [100 / 128 chars] | On the basis of the monitoring of imports that it is carrying out in accordance with the provisions of Council Regulation (EEC) No 3030/93, the Commission will be examining regularly whether some indi... [200 / 754 chars] |
| Who retains co-signing authority on the dual-signatory interest-bearing account to ensure proper dis... [100 / 110 chars] | In addition to these funds, there are other STABEX funds held by beneficiary ACP States. Once the Commission and the beneficiary (ACP) State have reached agreement on how the STABEX funds are to be ut... [200 / 745 chars] |

### Source Reference Table

| Title | Year | Type | URL |
| --- | ---: | --- | --- |
| MuPLeR: Multilingual Parallel Legal Retrieval |  | dataset card | [https://huggingface.co/datasets/mteb/MuPLeR-retrieval](https://huggingface.co/datasets/mteb/MuPLeR-retrieval) |
| An overview of the European Union's highly multilingual parallel corpora | 2014 | source paper | [https://link.springer.com/article/10.1007/s10579-014-9277-0](https://link.springer.com/article/10.1007/s10579-014-9277-0) |
| DGT-Acquis |  | source corpus | [https://joint-research-centre.ec.europa.eu/language-technology-resources/dgt-acquis_en](https://joint-research-centre.ec.europa.eu/language-technology-resources/dgt-acquis_en) |

### Representative Snippets

| Query | Relevant document excerpt |
| --- | --- |
| Which oversight body supplied a standalone movement-management solution while later inspecting countries' cross-regime goods controls in 2006? | A passage explaining that the Commission supplied a standalone MCC application during the NCTS project. |
| Which committee urged EU-backed measures to remedy leadership skill and ethics failings after misconduct undermined workforce and customer confidence? | A passage about the Committee's concern over employee and consumer confidence after management impropriety. |
| Which rationale links consensus on sector growth caps to both environmental resilience and long-term market competitiveness and youth job creation? | A passage about tourism policy balancing economic impact, job creation for young people, and environmental sustainability. |
| What does the EU executive do when pro-rated, category-specific inflows exceed set thresholds over a minimum three-month period? | A passage about the Commission monitoring imports and examining threshold exceedance under Council Regulation rules. |
| Who retains co-signing authority on the dual-signatory interest-bearing account to ensure proper disbursement? | A passage about STABEX funds, transfer conventions, and Commission co-signing authority for fund use. |
