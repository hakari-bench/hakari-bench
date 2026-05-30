# MNanoBEIR / NanoBEIR-es / NanoNQ

## Overview

This task is the Spanish NanoBEIR version of Natural Questions, an open-domain question answering benchmark built from real Google search questions and Wikipedia answer evidence. The original Natural Questions dataset pairs natural user questions with Wikipedia pages and annotated answer regions. In this NanoBEIR slice, Spanish translated questions must retrieve Spanish translated Wikipedia passages that contain the answer. The task contains 50 queries, 5,035 documents, and 57 positive relevance judgments. Most queries have one positive, while seven have two. It is a compact diagnostic for answer evidence retrieval from naturally phrased questions, where models must find the passage that answers the question rather than simply matching a named entity from the query.

## Details

### What the Original Data Measures

Natural Questions measures open-domain QA over Wikipedia using real search-style questions. The retrieval framing asks whether a model can rank the answer-bearing passage high enough for a reader or answer extractor to use. Questions often ask who, where, why, how many, or whether something is true, and the answer may appear in a contextual paragraph rather than in wording that mirrors the query.

### Observed Data Profile

The Spanish Nano task has 50 queries, 5,035 documents, and 57 positives. Positives per query average 1.14, with seven multi-positive queries. Query length averages about 53 characters, and documents average about 574 characters. Example questions ask where the Final Four will be held, whether The Nightmare Before Christmas was originally a Disney film, why the Angel of the North is located where it is, where the Three-Fifths Compromise appears in the Constitution, and who sings with Michael Jackson on "Somebody's Watching Me".

### BM25 Evaluation Profile

BM25 reaches nDCG@10 of 0.320, Hit@10 of 0.500, and Recall@100 of 0.825. Sparse retrieval often finds the answer passage somewhere in the top 100 when distinctive names or titles appear in the query, but top-10 ranking is weak. Natural questions often need relation matching: the answer passage may discuss a location, reason, performer, or historical fact without repeating the full question wording. BM25 can also over-rank pages that mention a visible entity but do not answer the question.

### Dense Evaluation Profile

The dense harrier-oss-270m baseline is strongest by top-rank quality, with nDCG@10 of 0.506, Hit@10 of 0.720, and Recall@100 of 0.877. This shows that semantic question-to-answer matching is the central signal for this Spanish NQ slice. Dense retrieval can connect a natural question to a passage containing the answer even when the passage uses explanatory or descriptive prose. It improves both first-page visibility and broad coverage over BM25.

### Reranking Hybrid Evaluation Profile

The reranking_hybrid profile reaches nDCG@10 of 0.413, Hit@10 of 0.660, and Recall@100 of 0.912, with four safeguard rows at 101 candidates. It has the best Recall@100 but trails dense retrieval in top-10 ranking. This indicates that hybrid search is useful as a candidate generator because it recovers more evidence passages, while dense retrieval is better at placing the answer passage early. For downstream reranking, the hybrid pool may be preferable; for direct retrieval, dense is stronger.

### Metric Interpretation for Model Researchers

Because most queries have one positive, Hit@10 and Recall@100 are straightforward evidence-finding measures. nDCG@10 captures early ranking quality and separates dense retrieval from hybrid candidate coverage. The pattern suggests a two-stage interpretation: use hybrid retrieval when recall is the priority, but use dense ranking or a stronger reranker to improve first-page ordering.

### Query and Relevance Type Tendencies

Queries are natural Spanish questions and often contain a named entity plus a requested relation. Relevant documents are Wikipedia-style answer passages. Hard negatives can mention the same entity or title but omit the answer. The task rewards answerability, relation understanding, entity precision, and robustness to translated question phrasing.

### Representative Failure Modes

BM25 can retrieve an entity page that shares terms but lacks the answer. Dense retrieval can retrieve semantically adjacent passages that answer a related question. Hybrid retrieval improves coverage but can still rank lexical distractors above the evidence. Failure analysis should verify whether the passage actually answers the question, not only whether it is about the same entity.

### Training and Leakage Considerations

Training should exclude Natural Questions, BEIR, NanoBEIR, and translated Wikipedia QA records likely to overlap with these questions or passages. Useful non-overlapping data includes open-domain QA evidence retrieval pairs, Spanish or multilingual Wikipedia QA datasets, and real-question-to-passage supervision. Synthetic data should generate natural Spanish questions whose answers are explicitly present in non-evaluation Wikipedia passages.

### Model Improvement Signals

Strong models should improve answer relation matching while keeping entity precision. Useful training signals include hard negatives from the same Wikipedia entity, title and alias normalization, paraphrased question forms, and answer-bearing passages with surrounding context. Hybrid systems should combine BM25's name recall with dense semantic ranking.

## Example Data

| Query | Positive Document |
|---|---|
| ¿Dónde se celebrará el Final Four este año? | El Torneo de Baloncesto Masculino de la División I de la NCAA de 2018 fue un torneo de eliminación directa... |
| ¿Era "Pesadilla antes de Navidad" originalmente una película de Disney? | La Pesadilla Antes de Navidad surgió de un poema escrito por Tim Burton en 1982... |
| ¿Por qué está el Ángel del Norte ahí? | Según Gormley, el significado de un ángel tenía tres aspectos importantes: primero, representar que bajo el lugar de su construcción... |
| ¿Dónde se estableció originalmente el Compromiso de los Tres Quintos en la Constitución? | El Compromiso de los Tres Quintos se encuentra en el Artículo 1, Sección 2, Cláusula 3... |
| ¿Quién canta "Somebody's Watching Me" con Michael Jackson? | "Somebody's Watching Me" es una canción del cantante estadounidense Rockwell de su álbum debut... |

## Public Sources

- [Natural Questions paper](https://aclanthology.org/Q19-1026/)
- [Natural Questions dataset page](https://ai.google.com/research/NaturalQuestions)
- [BEIR benchmark](https://github.com/beir-cellar/beir)
- [MMTEB benchmark](https://arxiv.org/abs/2502.13595)
- [NanoBEIR dataset](https://huggingface.co/collections/zeta-alpha-ai/nanobeir)

## Source Reference Table

| Label | URL |
|---|---|
| Natural Questions paper | https://aclanthology.org/Q19-1026/ |
| Natural Questions dataset page | https://ai.google.com/research/NaturalQuestions |
| BEIR benchmark | https://github.com/beir-cellar/beir |
| MMTEB benchmark | https://arxiv.org/abs/2502.13595 |
| NanoBEIR dataset | https://huggingface.co/collections/zeta-alpha-ai/nanobeir |
