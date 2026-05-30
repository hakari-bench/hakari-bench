# MNanoBEIR / NanoBEIR-fr / NanoNQ

## Overview

This task is the French NanoBEIR version of Natural Questions, an open-domain question answering benchmark built from real Google search questions and Wikipedia answer evidence. The original Natural Questions dataset pairs natural user questions with Wikipedia pages and annotated long or short answers. In this NanoBEIR slice, French translated questions must retrieve French translated Wikipedia passages that contain the answer from 5,035 candidate documents. The task contains 50 queries and 57 positive relevance judgments. Most queries have one positive, while seven have two. It is a compact diagnostic for evidence retrieval from naturally phrased questions, where the model must retrieve the answer-bearing passage rather than only a page that shares a named entity.

## Details

### What the Original Data Measures

Natural Questions measures open-domain QA over Wikipedia using real search-style questions. In retrieval form, the goal is to rank the passage containing the answer high enough for a reader or answer extraction model. The questions often ask who, where, why, how many, or whether something is true. Evidence may appear in a contextual paragraph that does not repeat the question wording.

### Observed Data Profile

The French Nano task has 50 queries, 5,035 documents, and 57 positives. Positives per query average 1.14, with seven multi-positive queries. Query length averages about 59 characters, while documents average about 589 characters. Example questions ask where the Final Four takes place, whether The Nightmare Before Christmas was originally a Disney film, why the Angel of the North is located where it is, where the Three-Fifths Compromise appears in the Constitution, and who sings with Michael Jackson on "Somebody's Watching Me".

### BM25 Evaluation Profile

BM25 reaches nDCG@10 of 0.446, Hit@10 of 0.700, and Recall@100 of 0.895. Sparse retrieval is useful for distinctive titles, names, and named entities. However, many natural questions require retrieving the passage that contains the answer relation, not simply the page with the most overlapping entity. BM25 can find candidates but often ranks a less answer-bearing page above the positive.

### Dense Evaluation Profile

The dense harrier-oss-270m baseline is strongest, with nDCG@10 of 0.597, Hit@10 of 0.760, and Recall@100 of 0.965. This shows that semantic question-to-answer matching is central for the French NQ slice. Dense retrieval can connect a natural question to an explanatory passage even when the passage is not written in question form. It improves both top-10 quality and candidate coverage over BM25.

### Reranking Hybrid Evaluation Profile

The reranking_hybrid profile reaches nDCG@10 of 0.556, Hit@10 of 0.760, and Recall@100 of 0.947, with two safeguard rows at 101 candidates. It matches dense Hit@10 but trails dense on nDCG@10 and recall. This suggests that hybrid search is strong, but dense ranking alone is better calibrated for answer-bearing passage placement in this sample. BM25 still contributes entity anchors, but it can also introduce lexical distractors.

### Metric Interpretation for Model Researchers

Because most queries have one positive, Hit@10 and Recall@100 are meaningful evidence discovery measures. nDCG@10 captures whether the answer passage appears high enough for direct retrieval use. The dense advantage indicates that answerability and relation matching are more important than exact term frequency for this task. Hybrid retrieval remains useful when a reranker will refine the candidate pool.

### Query and Relevance Type Tendencies

Queries are French natural-language questions about events, works, public art, constitutional clauses, songs, and people. Relevant documents are Wikipedia-style passages containing the answer. Hard negatives often mention the same entity or topic but do not answer the requested relation. The task rewards relation-aware answer matching and entity precision.

### Representative Failure Modes

BM25 can retrieve a page that shares a title or entity but lacks the answer. Dense retrieval can retrieve a semantically related passage that answers a nearby question. Hybrid retrieval can increase candidate variety but still rank lexical distractors above the evidence. Failure analysis should check whether the passage directly answers the question.

### Training and Leakage Considerations

Training should exclude Natural Questions, BEIR, NanoBEIR, and translated Wikipedia QA records likely to overlap with these examples. Useful non-overlapping data includes open-domain QA evidence retrieval pairs, French or multilingual Wikipedia QA datasets, and question-to-passage supervision with real user questions. Synthetic data should generate natural French questions from answer-bearing non-evaluation Wikipedia passages.

### Model Improvement Signals

Strong models should improve answer relation matching without losing exact entity recall. Useful signals include same-entity hard negatives, paraphrased question forms, title and alias normalization, and answer-bearing passages with surrounding context. Hybrid systems should combine BM25's name recall with dense semantic ranking.

## Example Data

| Query | Positive Document |
|---|---|
| Où se déroule le Final Four cette année ? | Le tournoi de basket-ball universitaire de la Division I de la NCAA 2018 était un tournoi à élimination directe... |
| Le film "L'Étrange Noël de Monsieur Jack" était-il à l'origine un film de Disney ? | L'idée de L'Étrange Noël de Monsieur Jack est née d'un poème écrit par Tim Burton en 1982... |
| Pourquoi l'Ange du Nord se trouve-t-il à cet endroit ? | Selon Gormley, la signification de cet ange est triple : d'abord, pour indiquer que sous le site de sa construction... |
| Où le compromis des trois cinquièmes était-il initialement mentionné dans la Constitution ? | Le Compromis des trois cinquièmes se trouve à l'Article 1, Section 2, Clause 3 de la Constitution des États-Unis... |
| Qui chante "Someone's Watching Me" en duo avec Michael Jackson ? | "Somebody's Watching Me" est une chanson du chanteur américain Rockwell issue de son premier album studio... |

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
