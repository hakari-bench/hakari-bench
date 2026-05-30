# NanoIndicQA / kn

## Overview

`NanoIndicQA / kn` is the Kannada split of IndicQA retrieval. The queries are Kannada reading-comprehension questions, and the documents are Kannada evidence paragraphs.

This task evaluates Kannada context retrieval in a small paragraph corpus. The target is the full supporting paragraph, so models must rank the passage that contains the answer evidence rather than generate or match only the answer string.

## Details

### What the Original Data Measures

IndicQA is a manually curated cloze-style reading-comprehension task introduced with IndicXTREME in "Towards Leaving No Indic Language Behind". The retrieval conversion asks models to retrieve the source context paragraph for each question.

In the Kannada split, the benchmark measures whether a retriever can map Kannada questions to Kannada paragraphs covering history, geography, cities, culture, and public institutions.

### Observed Data Profile

This Nano split contains 200 queries, 257 documents, and 200 positive qrels. Each query has exactly one positive. Queries average 53.27 characters, and documents average 882.74 characters.

Observed examples ask about Muslim-majority regions, the meaning of "Chennai", vintage cars in Jaipur, the river region where the British East India Company was established, and the best time to visit Aligarh. Several questions may target related geography or history contexts.

### BM25 Evaluation Profile

BM25 reaches nDCG@10 of 0.4730, hit@10 of 0.6000, and recall@100 of 0.8250. The candidate pool contains the full 257-document corpus. BM25 is useful when the Kannada question repeats a distinctive place name, institution, or entity from the context.

The lower hit rate shows that lexical overlap alone is fragile. Short questions may not repeat enough of the context, and multiple history or geography paragraphs can share names and topic words.

### Dense Evaluation Profile

The dense harrier-oss-270m profile reaches nDCG@10 of 0.7037, hit@10 of 0.8500, and recall@100 of 0.9800. Dense retrieval is clearly strongest across the main metrics.

This indicates that semantic question-context matching is important for Kannada IndicQA. Dense retrieval can connect a question to the paragraph even when the exact evidence sentence is phrased differently.

### Reranking Hybrid Evaluation Profile

The reranking_hybrid candidate subset reaches nDCG@10 of 0.6111, hit@10 of 0.7450, and recall@100 of 0.9700. It uses 100 candidates per query, with six rank-101 safeguard positives.

Hybrid retrieval has high recall but does not match dense retrieval's top-10 ranking. It is a useful candidate pool for reranking, while dense retrieval is the best direct first-stage ranker for this split.

### Metric Interpretation for Model Researchers

`NanoIndicQA / kn` is a dense-favored Kannada context retrieval task. The gap between BM25 and dense retrieval is large, so this split is useful for detecting whether a model has robust Kannada semantic representations.

Since each query has one positive, nDCG@10 and hit@10 directly measure correct-context ranking. Recall@100 is useful for diagnosing candidate generation, especially for reranking pipelines.

### Query and Relevance Type Tendencies

Queries are Kannada factual or cloze-style questions. Documents are paragraph-length contexts from encyclopedic or educational sources.

The relevance relation is evidence support: the positive paragraph must contain the information needed to answer the question.

### Representative Failure Modes

BM25 may retrieve a paragraph that repeats a place or institution name but lacks the requested detail. Dense retrieval may still confuse semantically similar city, history, or geography paragraphs. Hybrid retrieval reduces candidate misses but requires reranking for exact evidence selection.

Because the corpus is small, recall can be high while top-10 ordering remains difficult.

### Training Data That May Help

Useful training data includes Kannada QA, Kannada Wikipedia passage retrieval, Indic multilingual retrieval training, and topic-neighbor negatives from related history, geography, city, or cultural paragraphs.

Training should exclude this split's questions and positive context paragraphs.

### Model Improvement Notes

Improving this task requires Kannada semantic coverage and paragraph-level evidence ranking. Models should preserve names, dates, locations, and factual relations while handling question paraphrases.

For reranking, the model should determine whether the paragraph actually contains the answer evidence, not only whether it shares topical vocabulary.

## Example Data

### Public Sources

This task is documented through the IndicXTREME paper, the `mteb/IndicQARetrieval` dataset card, and the upstream `ai4bharat/IndicQA` dataset card. The Nano split is published in `hakari-bench/NanoIndicQA`.

### Source Reference Table

| Source | Role |
| --- | --- |
| [Towards Leaving No Indic Language Behind](https://arxiv.org/abs/2212.05409) | IndicXTREME and IndicQA benchmark paper. |
| [mteb/IndicQARetrieval](https://huggingface.co/datasets/mteb/IndicQARetrieval) | MTEB retrieval task dataset card. |
| [ai4bharat/IndicQA](https://huggingface.co/datasets/ai4bharat/IndicQA) | Upstream IndicQA dataset card. |
| [hakari-bench/NanoIndicQA](https://huggingface.co/datasets/hakari-bench/NanoIndicQA) | Nano benchmark dataset containing this split. |

### Representative Snippets

| Query Pattern | Positive Document Pattern |
| --- | --- |
| A Kannada question asking which region was Muslim-majority. | A paragraph about Kashmir's population, borders, and accession context around 1947. |
| A question asking the meaning or origin of the word Chennai. | A paragraph about Madras, Madraspatnam, and the British East India Company settlement. |
| A question asking what types of vintage cars enthusiasts can see. | A paragraph about Jaipur festivals, fairs, and the vintage car rally. |
| A question asking in which river region the British East India Company was established. | A paragraph about the Ganga plain and British East India Company influence. |
| A question asking the best time to visit Aligarh. | A climate paragraph about monsoon-influenced weather, summer, and temperature ranges. |
