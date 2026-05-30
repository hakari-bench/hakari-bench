# MNanoBEIR / NanoBEIR-es / NanoTouche2020

## Overview

This task is the Spanish NanoBEIR version of Touché 2020, an argument retrieval benchmark for controversial questions. The original CLEF Touché 2020 task focuses on retrieving arguments for socially important or everyday decision questions, where relevance depends on both topic match and argumentative content. In this NanoBEIR slice, Spanish translated controversial questions must retrieve Spanish translated debate-style argument documents from 5,745 candidates. The task contains 49 queries and 932 positive relevance judgments. Every query has multiple positives, averaging 19.02 relevant arguments. It is a compact benchmark for broad pro/con retrieval, argument relevance, and ranking long argumentative documents rather than short answer passages.

## Details

### What the Original Data Measures

Touché 2020 measures argument retrieval. A relevant document should contain a substantive argument addressing the central issue in the query. For controversial questions about homework, prescription drug advertising, child vaccination, abortion, or standardized testing, a topical mention is not enough: the retrieved document should present reasons, evidence, stance, or persuasive framing that engages with the question.

### Observed Data Profile

The Spanish Nano task has 49 queries, 5,745 documents, and 932 positives. Every query is multi-positive, with 6 to 32 positives and a median of 19. Query length averages about 54 characters, while documents are long, averaging about 2,361 characters. The examples include questions about homework, prescription drug advertising to consumers, child vaccination, abortion legality, and standardized tests. Positive documents are long Spanish translated debate arguments.

### BM25 Evaluation Profile

BM25 is strongest by nDCG@10, with 0.573, Hit@10 of 1.000, and Recall@100 of 0.786. This reflects the large number of positives and the strong topic terms in controversial questions. Sparse matching can reliably find at least one relevant argument for every query and ranks many arguments well when documents repeat the central issue. The risk is that BM25 may favor long topical documents that mention the issue frequently even if their argumentative fit is weaker.

### Dense Evaluation Profile

The dense harrier-oss-270m baseline reaches nDCG@10 of 0.414, Hit@10 of 0.878, and Recall@100 of 0.740. Dense retrieval is weaker here than BM25, suggesting that exact topic anchoring is very important for this Spanish argument slice. Embedding similarity can capture broad stance or issue proximity, but it may also retrieve generally related opinion text that does not directly address the controversial question. Dense retrieval alone underperforms for both top ranking and coverage.

### Reranking Hybrid Evaluation Profile

The reranking_hybrid profile reaches nDCG@10 of 0.531, Hit@10 of 0.980, and Recall@100 of 0.818. It has the best recall and is close to BM25 on first-page coverage, but BM25 still has the best nDCG@10. This indicates that hybrid search broadens candidate coverage by adding semantically related arguments, while sparse topic matching remains the strongest top-rank signal. For downstream reranking, the hybrid candidate pool is useful because it captures the largest share of relevant arguments.

### Metric Interpretation for Model Researchers

Hit@10 is nearly saturated and should not be treated as sufficient. Because every query has many positives, nDCG@10 and Recall@100 are more useful. nDCG@10 measures whether the top of the ranking contains high-quality relevant arguments, while Recall@100 measures whether the candidate set covers the broader pro/con space. Argument retrieval systems should be evaluated for coverage and diversity, not only whether they find one relevant document.

### Query and Relevance Type Tendencies

Queries are concise Spanish controversial questions. Relevant documents are long argument passages with claims, reasons, examples, and sometimes explicit stance language. Positives can include multiple sides of the debate, so the task rewards coverage of the issue rather than a single answer. Hard negatives may discuss the same topic but not argue the central question.

### Representative Failure Modes

BM25 can over-rank documents that repeat the topic without strong argumentative content. Dense retrieval can retrieve broad opinion pieces or adjacent policy discussions that do not answer the exact question. Hybrid retrieval improves coverage but may still under-rank arguments with less lexical overlap. Failure analysis should consider whether a retrieved document makes a substantive argument and whether the result set covers multiple relevant perspectives.

### Training and Leakage Considerations

Training should exclude Touché 2020, BEIR, NanoBEIR, and translated argument documents likely to overlap with these topics or documents. Useful non-overlapping data includes debate portal arguments, pro/con retrieval pairs, argument quality ranking data, and Spanish or multilingual controversial-topic retrieval supervision. Multi-positive training is required because each query has many relevant arguments.

### Model Improvement Signals

Strong models should preserve exact topic matching while learning argument quality and stance coverage. Useful training signals include same-topic non-argument hard negatives, paired pro/con arguments, stance-diverse positives, and long-document argument ranking. Hybrid systems should use BM25 for central issue anchoring and dense retrieval for paraphrased or differently framed arguments.

## Example Data

| Query | Positive Document |
|---|---|
| ¿Son útiles las tareas? | Primero, hay tres argumentos sobre por qué los deberes son excelentes y deberían continuar en las escuelas modernas... |
| ¿Deberían anunciarse los medicamentos con receta directamente a los consumidores? | Muchos anuncios no incluyen suficiente información sobre la eficacia de los medicamentos. Por ejemplo, Lunesta se promociona con una polilla... |
| ¿Es necesario vacunar a los niños? | Aún no es un caso completo... Solo algunos puntos que he reunido... Los gobiernos no deberían tener el derecho de intervenir... |
| ¿Debería ser legal el aborto? | Los abortos deberían ser legales, ya que la personalidad jurídica comienza cuando el feto es viable o después del nacimiento... |
| ¿Mejoran las pruebas estandarizadas la educación? | El SAT, el ACT y otras pruebas estandarizadas proporcionan más información sobre la preparación de un estudiante... |

## Public Sources

- [Touché 2020 overview](https://doi.org/10.1007/978-3-030-58219-7_26)
- [Touché 2020 dataset](https://doi.org/10.5281/zenodo.6862281)
- [BEIR benchmark](https://github.com/beir-cellar/beir)
- [MMTEB benchmark](https://arxiv.org/abs/2502.13595)
- [NanoBEIR dataset](https://huggingface.co/collections/zeta-alpha-ai/nanobeir)

## Source Reference Table

| Label | URL |
|---|---|
| Touché 2020 overview | https://doi.org/10.1007/978-3-030-58219-7_26 |
| Touché 2020 dataset | https://doi.org/10.5281/zenodo.6862281 |
| BEIR benchmark | https://github.com/beir-cellar/beir |
| MMTEB benchmark | https://arxiv.org/abs/2502.13595 |
| NanoBEIR dataset | https://huggingface.co/collections/zeta-alpha-ai/nanobeir |
