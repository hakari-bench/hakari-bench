# MNanoBEIR / NanoBEIR-it / NanoMSMARCO

## Overview

`NanoBEIR-it__NanoMSMARCO` is the Italian NanoBEIR version of MS MARCO passage
retrieval, a benchmark built from real web-search questions and answer-bearing
passages. The task asks a retrieval model to rank Italian translated passages
for short Italian translated user queries. Unlike multi-positive evidence tasks,
this Nano split has 50 queries, 5,043 documents, and 50 positive qrels, with
exactly one positive passage per query. It is therefore a focused test of
whether the retriever can identify the single passage that directly answers a
compact question. The observed results show a clear dense-retrieval advantage:
semantic matching substantially improves both top-10 quality and top-100
coverage over lexical matching alone.

## Details

### What the Original Data Measures

[MS MARCO](https://arxiv.org/abs/1611.09268) was introduced as a large-scale
machine reading comprehension and web passage retrieval dataset built from
human-generated search queries. In BEIR, the passage retrieval version is used
as a zero-shot retrieval benchmark: the model receives a natural web query and
must rank passages that contain an answer. The Italian NanoBEIR task preserves
that intent through translated queries and translated answer passages. It is
less about retrieving all evidence for a complex topic and more about matching a
short information need to a concise answer-bearing paragraph.

### Observed Data Profile

The task contains 50 queries and 5,043 documents. The qrels contain one positive
for each query: the average, minimum, median, and maximum positives per query
are all 1, and there are no multi-positive queries. Queries are short, averaging
42.04 characters, while documents average 356.59 characters. The examples cover
definition questions, entity questions, entertainment questions, geography, and
word-meaning queries. This profile resembles ordinary web search more than
scientific or argumentative retrieval: a user asks a compact question, and the
best passage often answers with wording that may not repeat the query exactly.

### BM25 Evaluation Profile

The BM25 top-500 subset reaches nDCG@10 = 0.3957, hit@10 = 0.6000, and
Recall@100 = 0.8800. BM25 retrieves many positives somewhere in the first 100
candidates, but its top-10 ranking quality is modest. This is expected for web
questions where the answer passage may use paraphrase, explanatory wording, or a
different grammatical form than the query. Exact term overlap is still useful
for entities, titles, and rare words, but it is not enough to consistently push
the answer-bearing passage into the first few ranks.

### Dense Evaluation Profile

The dense `harrier-oss-270m` top-500 subset reaches nDCG@10 = 0.5087, hit@10 =
0.7000, and Recall@100 = 0.9800. This is the strongest single profile for the
task, with a large improvement over BM25 on both ranking quality and support
coverage. The result indicates that embedding similarity is well matched to
Italian MS MARCO-style queries: definitions, paraphrased answers, and implicit
question-answer relationships benefit from semantic retrieval. For model
researchers, this task is a useful diagnostic for whether a multilingual
embedding model can map a short web query and an answer paragraph into a shared
semantic space without relying only on repeated words.

### Reranking Hybrid Evaluation Profile

The `reranking_hybrid` subset uses 100 to 101 candidates per query and reaches
nDCG@10 = 0.4781, hit@10 = 0.6800, and Recall@100 = 0.9800. One query uses the
rank-101 safeguard. The hybrid subset matches dense retrieval on top-100
coverage, but its nDCG@10 is lower than dense alone. This means that combining
lexical and dense candidates successfully keeps the relevant passage available
for reranking, while the fused ranking is not always as clean as the dense
ordering in the first 10 positions. In this task, hybrid search is best viewed
as a high-coverage candidate pool rather than the strongest first-stage ranker.

### Metric Interpretation for Model Researchers

The main pattern is dense dominance. BM25 has acceptable Recall@100, so lexical
signals are not irrelevant, but the low nDCG@10 shows that exact matching often
places answer passages below distractors. Dense retrieval improves both top-10
hit rate and rank ordering, which is the most important behavior for single
positive web passage retrieval. The hybrid profile is still valuable because it
preserves dense-level Recall@100 while adding lexical coverage, but it does not
beat dense ranking at nDCG@10 on this split. A strong reranker trained for this
task should therefore focus on using the hybrid pool to recover coverage and
then re-establish the semantic answer match near the top.

### Query and Relevance Type Tendencies

The sample questions are concise and answer seeking: "what is" questions,
"who sang" questions, actor-role questions, location questions, and lexical
meaning questions. The positive documents usually contain direct explanations,
short encyclopedia-like statements, or snippets from web-style answer pages.
Relevance is often determined by whether the passage answers the exact
information need, not merely whether it discusses the same entity. This makes
near-topic distractors a serious source of error.

### Representative Failure Modes

BM25 can miss the best passage when the query asks a short question and the
answer is phrased as an explanatory sentence rather than a term repetition.
Dense retrieval can retrieve semantically close but non-answering passages,
especially for broad entities or common concepts. Hybrid search can include the
right passage but still rank a lexical distractor above it if the distractor
shares more surface terms with the query. Because each query has only one
positive, a single rank swap has a large effect on nDCG@10.

### Training Data That May Help

Useful training data includes non-overlapping web QA retrieval pairs, Italian
search-query logs, multilingual passage retrieval data, and answer-bearing
question-passage pairs. Hard negatives should include passages that share the
entity or topic but do not answer the question. Training and tuning should avoid
overlap with MS MARCO, BEIR, NanoBEIR, and translated passages from this
benchmark.

### Model Improvement Notes

This task rewards semantic answer matching more than broad topical similarity.
Improvements should prioritize concise query understanding, paraphrase handling,
and hard-negative separation between answer-bearing and merely related
passages. A practical system can use hybrid candidate generation for coverage,
but the final ranking model needs a strong answer selection signal to beat the
dense baseline at the top of the list.

## Example Data

| Query | Positive document |
| --- | --- |
| Cos'è la sindrome da ruminazione? [33 chars] | Sindrome da Ruminazione. La sindrome da ruminazione, nota anche come mericismo, è un tipo di disturbo alimentare non altrimenti specificato che provoca la rigurgitazione del cibo. Sebbene non sia iden... [200 / 326 chars] |
| Chi ha cantato "Ecco che vado di nuovo"? [40 chars] | Per altri significati, vedi Here I Go Again (disambiguazione). Here I Go Again è una canzone del gruppo rock britannico Whitesnake. Pubblicata originariamente nell'album del 1982 Saints & Sinners, la... [200 / 346 chars] |
| Chi interpreta Cameron Boyce in "Liv e Maddie"? [47 chars] | Preparatevi a sbellicarvi dalle risate, ragazzi. In un'anteprima esclusiva dell'episodio del 19 aprile di 'Liv & Maddie' intitolato 'Prom-A-Rooney.' Ovviamente. Nel divertentissimo clip, vediamo Camer... [200 / 355 chars] |
| Dove si trovano la maggior parte dei grandi deserti della Terra? [64 chars] | Gli altri deserti della Terra si trovano al di fuori delle aree polari. Il più grande è il deserto del Sahara, un deserto subtropicale nell'Africa settentrionale. [162 chars] |
| Che significa "copper" per un poliziotto? [41 chars] | Secondo le attuali scoperte, sembra che "copper" (un poliziotto, letteralmente 'colui che arresta') preceda "cop" (usato sia come verbo per arrestare, sia come sostantivo per indicare un poliziotto).... [200 / 371 chars] |

### Public Sources

- [MS MARCO: A Human Generated Machine Reading Comprehension Dataset](https://arxiv.org/abs/1611.09268).
- [BEIR: A Heterogeneous Benchmark for Zero-shot Evaluation of Information Retrieval Models](https://arxiv.org/abs/2104.08663).
- [MMTEB: Massive Multilingual Text Embedding Benchmark](https://arxiv.org/abs/2502.13595).
- [Zeta Alpha NanoBEIR collection](https://huggingface.co/collections/zeta-alpha-ai/nanobeir).
- [hakari-bench/NanoBEIR-it](https://huggingface.co/datasets/hakari-bench/NanoBEIR-it).

### Source Reference Table

| Title | Year | Type | URL |
| --- | ---: | --- | --- |
| MS MARCO: A Human Generated Machine Reading Comprehension Dataset | 2016 | task paper | [https://arxiv.org/abs/1611.09268](https://arxiv.org/abs/1611.09268) |
| BEIR: A Heterogeneous Benchmark for Zero-shot Evaluation of Information Retrieval Models | 2021 | benchmark paper | [https://arxiv.org/abs/2104.08663](https://arxiv.org/abs/2104.08663) |
| MMTEB: Massive Multilingual Text Embedding Benchmark | 2025 | benchmark paper | [https://arxiv.org/abs/2502.13595](https://arxiv.org/abs/2502.13595) |
| NanoBEIR: Smaller BEIR dataset subsets | 2024 | dataset collection | [https://huggingface.co/collections/zeta-alpha-ai/nanobeir](https://huggingface.co/collections/zeta-alpha-ai/nanobeir) |
