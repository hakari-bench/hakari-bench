# NanoMLDR / es

## Overview

`NanoMLDR / es` is the Spanish split of NanoMLDR, a multilingual long-document
retrieval benchmark derived from MLDR. Spanish paragraph-grounded questions
retrieve full Spanish documents, including long encyclopedia and web-style
articles. The Nano split has 176 queries, 3,312 documents, and 176 positive
qrel rows, with exactly one positive document per query. Current diagnostics
show BM25 as the strongest profile by nDCG@10 and hit@10, while
`reranking_hybrid` matches BM25 on recall@100 and dense retrieval trails both
lexical and hybrid search.

## Details

### What the Original Data Measures

MLDR was introduced with the M3-Embedding work as a multilingual long-document
retrieval benchmark. The dataset card describes sampling long documents,
selecting a paragraph, and generating a specific question from that paragraph.
The retrieval target is the full article or long document that contains the
answer-bearing paragraph.

For Spanish, source data includes Wikipedia and mC4-style long documents. The
task therefore measures paragraph-to-document retrieval over long Spanish
articles, not short-passage retrieval. A system must identify the full document
from a question whose evidence may be localized to a single paragraph.

### Observed Data Profile

The Nano split contains 176 queries, 3,312 documents, and 176 positive qrel
rows. Every query has exactly one positive document. Queries average 120.26
characters, while documents average 12,539.90 characters. The queries are
longer than in many other NanoMLDR splits and often contain distinctive
article-specific phrasing.

Observed examples include questions about ethanol-based hydrogen production,
Schindler's List, geography in the Gulf of Ancud, renovation of Centro Cultural
Recoleta, and why Square developers chose to create a role-playing game for
Game Boy. The positive documents are long Spanish articles containing the
paragraph used to generate the question.

### BM25 Evaluation Profile

The dataset-provided BM25 candidate subset contains 500 candidates per query and
achieves nDCG@10 = 0.9439, hit@10 = 0.9716, and recall@100 = 0.9886. BM25 is the
strongest observed profile and is extremely effective on this split. The
generated Spanish questions often preserve specific terms, names, dates,
entities, and technical phrases from the target paragraph.

This makes lexical matching a very strong long-document signal. Even when the
positive is a long article, the question often contains enough rare Spanish
surface evidence to identify the correct document.

### Dense Evaluation Profile

The dense `harrier_oss_v1_270m` candidate subset contains 500 candidates per
query and achieves nDCG@10 = 0.7844, hit@10 = 0.8636, and recall@100 = 0.9432.
Dense retrieval is solid but clearly weaker than BM25. It captures broad
semantic similarity, but full-document embeddings can dilute the paragraph-level
evidence needed to distinguish the exact article.

The dense profile is still useful as a semantic signal, especially for
paraphrased questions. However, on this split the long and specific Spanish
queries make lexical matching the more reliable top-rank method.

### Reranking Hybrid Evaluation Profile

The `reranking_hybrid` candidate subset contains mostly 100 candidates per
query, with two queries using a rank-101 safeguard row. It achieves nDCG@10 =
0.8580, hit@10 = 0.9375, and recall@100 = 0.9886. Hybrid retrieval matches BM25
on recall@100 but does not match BM25's top-rank quality.

This profile shows that dense candidates can help preserve coverage while BM25
remains the strongest ranking signal. Hybrid search is a useful candidate stage
for reranking, but a reranker should not assume that dense similarity is more
reliable than exact lexical evidence for Spanish MLDR.

### Metric Interpretation for Model Researchers

This task is single-positive: each query has exactly one relevant long
document. Hit@10 measures whether that document appears near the top. nDCG@10
is sensitive to the rank of the positive, and recall@100 measures whether it
remains available for reranking.

The Spanish MLDR profile is an example where BM25 is not merely a baseline but
the dominant method. The data rewards exact paragraph-derived terms inside long
documents. Dense retrieval should be judged against this strong lexical
reference, and hybrid reranking should preserve BM25's high top-rank precision.

### Query and Relevance Type Tendencies

Queries are long Spanish paragraph-grounded questions about technical processes,
film interpretation, geography, cultural institutions, games, history, and
article-specific facts. Many contain enough context to strongly identify the
source article.

Relevant documents are long Spanish articles or web documents that contain the
answer-bearing paragraph. The task rewards rare-term matching, robust
long-document indexing, and paragraph-level evidence selection inside full
documents.

### Representative Failure Modes

Dense retrieval can return a thematically related article but miss the exact
document containing the paragraph. Full-document embeddings may be dominated by
the main article topic and lose the local answer phrase. BM25 can fail when
several long documents share the same entity, film, place, or technical term, or
when the generated question paraphrases the paragraph strongly.

Hybrid retrieval can include the positive but rank another semantically or
lexically plausible document above it. Reranking should operate over chunks or
paragraphs rather than only full-document text.

### Training Data That May Help

Useful training data includes Spanish long-document QA retrieval pairs, Spanish
Wikipedia article retrieval, Spanish mC4 long-document retrieval, and same-
entity article hard negatives. Training should include examples where the
positive is a full document but the answer is localized in a paragraph.

Synthetic data can help when it samples paragraphs from long Spanish articles,
generates specific Spanish questions, and uses the whole article as the
positive. Negatives should share the main entity, historical period, technical
domain, or cultural work but not contain the answer-bearing paragraph.

### Model Improvement Notes

Dense retrievers should incorporate chunking, late interaction, paragraph-aware
pooling, or multi-vector representations to avoid diluting paragraph evidence.
Sparse systems should preserve exact Spanish article-specific terms while
handling paraphrase and inflection. Rerankers should validate against BM25
because the sparse candidate ranking is very strong.

For hybrid systems, `NanoMLDR / es` supports using BM25 as the primary
candidate generator with dense retrieval as a recall supplement. The current
hybrid profile keeps BM25-level recall but does not surpass BM25 top-rank
quality.

## Example Data

| Query | Positive document |
| --- | --- |
| ¿Cuál es el catalizador utilizado para convertir el monóxido de carbono en un producto menos perjudi... [100 / 169 chars] | Etanol (combustible) El etanol es un compuesto químico obtenido a partir de la fermentación de los azúcares que puede utilizarse como combustible, solo, o bien, mezclado en cantidades variadas con gas... [200 / 31,421 chars] |
| ¿Cómo perpetúa la actividad financiera en el gueto el estereotipo de la vida judía según Sara Horowi... [100 / 103 chars] | La lista de Schindler Argumento En Cracovia, durante la Segunda Guerra Mundial, las tropas alemanas de ocupación han forzado a los judíos polacos a vivir recluidos en un gueto. El empresario Oskar Sch... [200 / 29,815 chars] |
| ¿Cuál es la altura del cerro Calzoncillo en la isla mencionada en el texto? [75 chars] | Golfo de Ancud Geología y orografía Tanto los golfos de Ancud y Corcovado como el seno de Reloncaví, son las cuencas de grandes lagos que, en época remota, formaron parte del valle central que luego s... [200 / 25,915 chars] |
| ¿Cuáles fueron los principales cambios realizados durante la remodelación del Centro Cultural Recole... [100 / 111 chars] | Centro Cultural Recoleta Historia El Centro Cultural Recoleta es conocido históricamente como la sede de lo nuevo. Desde su inauguración como centro cultural en 1980, sus salas se convirtieron en el l... [200 / 26,824 chars] |
| ¿Cuál fue la razón principal por la que los desarrolladores de Square decidieron crear un juego de r... [100 / 151 chars] | Final Fantasy Legend Modo de juego En The Final Fantasy Legend, el jugador recorre el mundo del juego con un equipo de hasta cuatro personajes, explorando áreas e interactuando con otros personajes no... [200 / 26,818 chars] |

### Public Sources

- [M3-Embedding: Multi-Linguality, Multi-Functionality, Multi-Granularity Text Embeddings Through Self-Knowledge Distillation](https://arxiv.org/abs/2402.03216),
  2024.
- [M3-Embedding ACL Anthology version](https://aclanthology.org/2024.findings-acl.137/),
  2024.
- [Shitao/MLDR dataset card](https://huggingface.co/datasets/Shitao/MLDR).
- [hakari-bench/NanoMLDR](https://huggingface.co/datasets/hakari-bench/NanoMLDR),
  Nano benchmark dataset.

### Source Reference Table

| Title | Year | Type | URL |
| --- | ---: | --- | --- |
| M3-Embedding: Multi-Linguality, Multi-Functionality, Multi-Granularity Text Embeddings Through Self-Knowledge Distillation | 2024 | benchmark paper | [https://arxiv.org/abs/2402.03216](https://arxiv.org/abs/2402.03216) |
| M3-Embedding ACL Anthology version | 2024 | paper | [https://aclanthology.org/2024.findings-acl.137/](https://aclanthology.org/2024.findings-acl.137/) |
| MLDR: Multilingual Long-Document Retrieval dataset | 2024 | dataset card | [https://huggingface.co/datasets/Shitao/MLDR](https://huggingface.co/datasets/Shitao/MLDR) |

### Representative Snippets

| Query pattern | Positive document pattern |
| --- | --- |
| A Spanish technical question about ethanol hydrogen production. | A long article about ethanol as fuel. |
| A question about interpretation of Jewish life in a film. | A long article about Schindler's List. |
| A question about the height of a named hill. | A long geography article about the Gulf of Ancud region. |
| A question about remodeling a cultural center. | A long article about Centro Cultural Recoleta. |
| A question about why game developers chose an RPG design. | A long article about Final Fantasy Legend. |
