# NanoMuPLeR / es

## Overview

`NanoMuPLeR / es` is the Spanish split of MuPLeR-retrieval. It evaluates Spanish legal query-to-passage retrieval over European Union legal text derived from DGT-Acquis. Queries are synthetic Spanish legal questions, and documents are Spanish parallel legal passages. Each query has exactly one positive passage. The task is useful for evaluating same-language Spanish legal retrieval where formal legal terms, institutions, rates, dates, and procedural conditions must be matched precisely. It also supports comparison across the parallel MuPLeR languages because the same legal source material is represented in multiple languages.

## Details

### What the Original Data Measures

MuPLeR-retrieval measures multilingual parallel legal retrieval over EU legal passages. The dataset card describes 10,000 human-translated DGT-Acquis passages and 200 synthetic parallel queries per language. The DGT-Acquis source belongs to the European Union's multilingual legal corpus resources.

For this Spanish split, the system must retrieve the passage that grounds the condition or legal detail in the Spanish query.

### Observed Data Profile

The Nano split contains 200 queries, 10,000 documents, and 200 positive qrel rows. Each query has exactly one positive. Queries average 134.67 characters, while documents average 734.58 characters.

Examples ask about public-health statistics, regional aid, environmental prevention, intra-Community import tax, and advisory-committee comments on transport pools. Documents are formal Spanish EU-law passages.

### BM25 Evaluation Profile

The BM25 candidate subset uses top-500 candidates and reaches nDCG@10 of 0.8302, hit@10 of 0.9050, and recall@100 of 0.9700. BM25 is very strong because Spanish legal questions often reuse distinctive legal terms, institution names, percentages, dates, and topic labels from the relevant passage.

BM25's remaining weakness is exact condition matching. A passage may share an institution or legal area but answer a different legal issue.

### Dense Evaluation Profile

The dense candidate subset from `harrier_oss_v1_270m` uses top-500 candidates and reaches nDCG@10 of 0.8803, hit@10 of 0.9550, and recall@100 of 0.9850. Dense retrieval is stronger than BM25 across all reported metrics.

This suggests that semantic matching helps with synthetic Spanish legal questions, especially where the query paraphrases the passage rather than copying its wording.

### Reranking Hybrid Evaluation Profile

The `reranking_hybrid` subset uses top-100 candidates with no safeguard positives. It reaches nDCG@10 of 0.8862, hit@10 of 0.9500, and recall@100 of 1.0000. Hybrid retrieval has the strongest nDCG@10 and complete recall@100.

The result shows that exact legal anchors and dense semantic matching are complementary. The hybrid pool is the strongest candidate source for reranking.

### Metric Interpretation for Model Researchers

This is a single-positive retrieval task. nDCG@10 and hit@10 measure whether the exact grounding passage is ranked early, while recall@100 measures candidate availability for reranking.

The high scores mean the task is not primarily a low-recall benchmark; its value is in measuring precise legal grounding and cross-language consistency within MuPLeR.

### Query and Relevance Type Tendencies

Queries are formal Spanish legal questions. Relevant documents are Spanish EU legal passages about policy, taxation, state aid, transport, public health, or administrative procedure.

The relevance relation is exact legal grounding. Same-topic legal material is not enough unless it answers the specific query.

### Representative Failure Modes

Common failures include retrieving a related EU provision, matching a numeric rate without the right condition, confusing advisory bodies, and over-ranking passages with similar legal boilerplate. Sparse systems can miss paraphrases; dense systems can overgeneralize among adjacent provisions.

### Training Data That May Help

Useful training data includes non-overlapping Spanish EUR-Lex or DGT-Acquis retrieval pairs, Spanish legal QA, multilingual legal bitext, and hard negatives from related EU provisions. MuPLeR evaluation queries and exact positive passages should be excluded.

### Model Improvement Notes

Models should preserve Spanish legal terminology, article-style conditions, dates, percentages, and institutional names. Hard negatives should share topic and vocabulary but fail to answer the exact legal condition. Hybrid retrieval is the strongest starting point for reranking.

## Example Data

| Query | Positive document |
| --- | --- |
| ¿Por qué la autoridad estadística propone instrumento jurídico para consolidar datos de salud poblac... [100 / 148 chars] | Ésta es la razón por la que la Comisión (Eurostat) considera que es hora de establecer una base sólida mediante un acto jurídico fundamental sobre estadísticas de salud pública y salud y seguridad en... [200 / 722 chars] |
| Cómo quiso el ejecutivo supranacional que corrieran las ayudas: dos años y hasta tres más al convert... [100 / 115 chars] | Dado que el régimen de ayudas (identificado con el no NN 91/A/95) adoptado por la Región de Sicilia mediante el artículo 10 de la Ley regional no 27, de 15 de mayo de 1991, preveía un mecanismo de apo... [200 / 650 chars] |
| Cómo relaciona la prevención la explotación insostenible y las intervenciones humanas intencionadas... [100 / 154 chars] | La prevención es un principio fundamental para la protección y conservación del medio ambiente así como los daños que pudieran causarse a la población civil, y su finalidad es una utilización sostenib... [200 / 708 chars] |
| ¿Qué impuesto sobre las importaciones intracomunitarias seguían aplicando siete Estados miembros: do... [100 / 132 chars] | La mayoría de los 25 Estados miembros aceptó la orientación del Consejo de 1985 y ha suprimido totalmente el impuesto. En la actualidad, sólo siete Estados miembros continúan aplicándolo: Polonia y Po... [200 / 687 chars] |
| Qué órgano asesor cuestionó la guía para operadores de pools irregulares y propuso ampliar normas de... [100 / 135 chars] | Dado que las secciones que tratan sobre el transporte de tramp y los pools de transporte de tramp son menos detalladas por las razones supuestas anteriormente, el CESE se pregunta si serán suficientes... [200 / 783 chars] |

### Source Reference Table

| Title | Year | Type | URL |
| --- | ---: | --- | --- |
| MuPLeR: Multilingual Parallel Legal Retrieval |  | dataset card | [https://huggingface.co/datasets/mteb/MuPLeR-retrieval](https://huggingface.co/datasets/mteb/MuPLeR-retrieval) |
| An overview of the European Union's highly multilingual parallel corpora | 2014 | source paper | [https://link.springer.com/article/10.1007/s10579-014-9277-0](https://link.springer.com/article/10.1007/s10579-014-9277-0) |
| DGT-Acquis |  | source corpus | [https://joint-research-centre.ec.europa.eu/language-technology-resources/dgt-acquis_en](https://joint-research-centre.ec.europa.eu/language-technology-resources/dgt-acquis_en) |

### Representative Snippets

| Query | Relevant document excerpt |
| --- | --- |
| ¿Por qué la autoridad estadística propone instrumento jurídico para consolidar datos de salud poblacional y seguridad laboral y apoyar metodologías? | A Spanish passage explaining why Eurostat considered a legal basis necessary for public health and work-safety statistics. |
| Cómo quiso el ejecutivo supranacional que corrieran las ayudas: dos años y hasta tres más al convertir el contrato? | A Spanish passage about a Sicilian regional aid mechanism and contribution periods. |
| Cómo relaciona la prevención la explotación insostenible y las intervenciones humanas intencionadas con catástrofes naturales anómalas y de gran magnitud? | A passage describing prevention as a principle for environmental protection and sustainable use of natural resources. |
| ¿Qué impuesto sobre las importaciones intracomunitarias seguían aplicando siete Estados miembros: dos ≤0,5%, uno 0,6%, cuatro al 1%? | A passage explaining that seven Member States continued applying the tax at specified rates. |
| Qué órgano asesor cuestionó la guía para operadores de pools irregulares y propuso ampliar normas de consorcios solo para contenedores? | A passage about the EESC questioning whether guidance on tramp pools is sufficient. |
