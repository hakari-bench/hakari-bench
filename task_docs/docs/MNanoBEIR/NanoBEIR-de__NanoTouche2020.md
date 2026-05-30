# MNanoBEIR / NanoBEIR-de / NanoTouche2020

## Overview

This task is the German NanoBEIR version of Touché 2020, an argument retrieval benchmark for controversial and socially important questions. The original CLEF Touché task focuses on retrieving argumentative documents, where relevance depends not only on topic match but also on whether the document contains substantive arguments addressing the question. In this NanoBEIR slice, German translated controversial questions must retrieve German translated debate-style argument documents. The task contains 49 queries, 5,745 documents, and 932 positive relevance judgments. Every query has multiple positives, averaging about 19 relevant documents. This makes the benchmark useful for diagnosing broad pro/con coverage, argument relevance, and the difference between merely mentioning a topic and actually arguing about it.

## Details

### What the Original Data Measures

Touché 2020 measures argument retrieval rather than ordinary ad hoc search. A relevant document should address the controversial question with an argument, stance, reason, or evidence. The benchmark therefore requires topical matching, but topical matching alone is not enough. For questions about abortion, homework, standardized testing, prescription drug advertising, or school discipline, a system should prioritize documents that make a substantive argumentative contribution rather than documents that only contain the same keywords.

### Observed Data Profile

The German Nano task has 49 queries, 5,745 documents, and 932 positives. Every query is multi-positive, with 6 to 32 positives and a median of 19. Query length averages 51 characters, while documents are long, averaging about 2,457 characters. The examples include controversial questions about homework, direct-to-consumer drug advertising, vaccines for children, abortion legality, and standardized testing. Positive documents are often multi-paragraph debate texts with explicit persuasive framing.

### BM25 Evaluation Profile

BM25 is strong by first-page coverage, with nDCG@10 of 0.482, Hit@10 of 1.000, and Recall@100 of 0.714. The perfect Hit@10 reflects the large number of positives per query and the presence of strong topic terms. BM25 can quickly find at least one argumentative document for each topic when terms such as abortion, homework, vaccines, or standardized tests are repeated. However, nDCG and recall show that ranking many relevant arguments remains difficult. Sparse matching can retrieve topic mentions without understanding argumentative substance or stance diversity.

### Dense Evaluation Profile

The dense harrier-oss-270m baseline reaches nDCG@10 of 0.416, Hit@10 of 0.918, and Recall@100 of 0.763. Dense retrieval has better Recall@100 than BM25 but weaker top-10 ranking. This suggests that embeddings help broaden candidate coverage across paraphrased argument wording and related stances, but may not always place the most directly relevant arguments at the top. Dense models can recognize semantic relation to a controversial issue, yet may over-rank broad opinion pieces or thematically adjacent documents that do not directly address the query.

### Reranking Hybrid Evaluation Profile

The reranking_hybrid profile performs best overall, with nDCG@10 of 0.501, Hit@10 of 1.000, and Recall@100 of 0.784. It combines BM25's strong topic-term anchoring with dense retrieval's broader semantic coverage. This is a clear hybrid-search case: sparse signals ensure that direct topic matches remain prominent, while dense signals recover arguments that use different wording or stance framing. The result improves both top-10 ranking over BM25 and recall over dense alone.

### Metric Interpretation for Model Researchers

Hit@10 is saturated for BM25 and hybrid and should not be used alone. nDCG@10 is the better top-rank signal because every query has many relevant arguments and ranking quality matters. Recall@100 is also important because an argument retrieval system should expose diverse pro and con material, not just one relevant document. A model that retrieves a single argument for every topic but misses most relevant stances is not sufficient for this task.

### Query and Relevance Type Tendencies

Queries are concise controversial questions. Relevant documents are long argument passages, often presenting reasons, examples, evidence, or policy claims. Positives can include different stances on the same issue, so retrieval should cover a set of arguments rather than converge on one viewpoint. The task rewards models that recognize central issue framing, pro/con language, and argumentative content.

### Representative Failure Modes

BM25 can retrieve documents that repeat the topic but lack a substantive argument. Dense retrieval can retrieve broadly related opinion text that does not answer the exact controversial question. Hybrid retrieval reduces these risks but may still underrepresent one side of a debate or over-rank long documents with many topical terms. Failure analysis should consider stance coverage and argument quality, not just topical relevance.

### Training and Leakage Considerations

Training should exclude Touché 2020, BEIR, NanoBEIR, and translated argument documents likely to overlap with the evaluation topics or documents. Useful non-overlapping data includes debate portal argument collections, pro/con retrieval pairs, argument quality ranking data, and German or multilingual controversial-topic retrieval supervision. Multi-positive training is required because each query should retrieve a broad set of relevant arguments.

### Model Improvement Signals

Strong models should combine exact issue matching with argument-awareness. Useful training signals include hard negatives that discuss the same topic without arguing the central question, paired pro/con documents, and stance-diverse positives. Hybrid systems are especially appropriate because they can preserve query topic terms while using dense similarity to recover paraphrased or differently framed arguments.

## Example Data

| Query | Positive Document |
|---|---|
| Ist Hausaufgaben sinnvoll? | Zunächst gibt es drei Argumente dafür, warum Hausaufgaben hervorragend sind und in modernen Schulen fortbestehen sollten... |
| Sollten verschreibungspflichtige Medikamente direkt an Verbraucher beworben werden dürfen? | Viele Werbeanzeigen enthalten nicht genügend Informationen darüber, wie gut Medikamente wirken... |
| Welche Impfungen sind für Kinder notwendig? | Es handelt sich noch nicht um einen vollständigen Fall... Nur einige wenige Punkte, die ich zusammengestellt habe... |
| Sollte Abtreibung legal sein? | Abtreibungen sollten legal sein, da die Persönlichkeit erst beginnt, wenn ein Fötus lebensfähig ist oder nach der Geburt... |
| Verbessern standardisierte Tests die Qualität der Bildung? | Die SAT, ACT und andere standardisierte Tests bieten mehr Einblicke in die Vorbereitung eines Schülers auf das Studium... |

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
