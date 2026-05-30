# NanoIndicQA / or

## Overview

`NanoIndicQA / or` is the Odia split of IndicQA retrieval. The queries are Odia reading-comprehension questions, and the documents are Odia context paragraphs from a compact corpus.

This task evaluates Odia paragraph retrieval for QA. The model must retrieve the context paragraph that supports the answer, often among passages that share people, films, history, temples, or political terminology.

## Details

### What the Original Data Measures

IndicQA is a cloze-style reading-comprehension benchmark within IndicXTREME, introduced in "Towards Leaving No Indic Language Behind". The retrieval version measures question-to-context matching by treating the source paragraph as the relevant document.

In the Odia split, the benchmark tests retrieval over Odia contexts with cultural, biographical, historical, and encyclopedic content.

### Observed Data Profile

This Nano split contains 200 queries, 252 documents, and 201 positive qrels. Queries have 1.005 positives on average, with a minimum of 1, a median of 1.0, and a maximum of 2. Only one query is multi-positive. Queries average 57.16 characters, and documents average 801.92 characters.

Observed examples ask about Amitabh Bachchan's father, the release year of a film, the height of an Indonesian Shiva temple, who directed a film, and who wanted Amitabh Bachchan to act. Documents are Odia paragraphs about biography, cinema, temples, history, and culture.

### BM25 Evaluation Profile

BM25 reaches nDCG@10 of 0.6041, hit@10 of 0.7250, and recall@100 of 0.9154. The candidate pool contains the full 252-document corpus. BM25 is useful when the query repeats distinctive names, film titles, or cultural terms from the paragraph.

It struggles when multiple passages share the same person, film, or historical topic. Lexical overlap can identify the broad subject but miss the exact evidence paragraph.

### Dense Evaluation Profile

The dense harrier-oss-270m profile reaches nDCG@10 of 0.7605, hit@10 of 0.8800, and recall@100 of 0.9652. Dense retrieval is the strongest direct profile.

This indicates that semantic question-context matching is important for Odia. Dense retrieval can rank the correct context higher when the query and evidence sentence do not share exact wording.

### Reranking Hybrid Evaluation Profile

The reranking_hybrid candidate subset reaches nDCG@10 of 0.7033, hit@10 of 0.8150, and recall@100 of 0.9751. It uses 100 candidates per query, with four rank-101 safeguard positives.

Hybrid retrieval has the best recall@100 but lower top-10 quality than dense retrieval. It is therefore a useful reranking pool, while dense retrieval is the strongest direct ranker.

### Metric Interpretation for Model Researchers

`NanoIndicQA / or` is a dense-favored Odia context retrieval task. BM25 provides a meaningful lexical baseline, but dense retrieval gives a large top-10 improvement.

Since almost every query has one positive, hit@10 and nDCG@10 directly measure whether the correct evidence paragraph appears early. Recall@100 helps assess candidate coverage for downstream reranking.

### Query and Relevance Type Tendencies

Queries are Odia factual or cloze-style questions. Documents are paragraph-length contexts about biography, cinema, historical movements, temples, geography, and public figures.

The relevance relation is evidence support: the positive paragraph contains the information needed to answer the query.

### Representative Failure Modes

BM25 may retrieve a paragraph about the same actor, film, or temple but not the requested fact. Dense retrieval may confuse semantically related biographical or film contexts. Hybrid retrieval reduces candidate misses but still needs evidence-level reranking.

When several questions point to related people or films, broad topical matching is not sufficient.

### Training Data That May Help

Useful training data includes Odia QA retrieval, Odia Wikipedia passages, multilingual IndicQA-style data, and hard negatives with related organizations, people, movements, films, or historical topics.

Training should exclude this split's questions and positive context paragraphs.

### Model Improvement Notes

Improving this task requires Odia language coverage and paragraph-level evidence selection. Models should preserve person names, titles, dates, numbers, and relation cues while handling question paraphrases.

For reranking, the model should determine whether the paragraph contains the exact answer evidence rather than just the same named entity.

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
| An Odia question asking what Amitabh Bachchan's father was. | A biographical paragraph about Amitabh Bachchan's birth, family, and background. |
| A question asking when a named film was released. | A cinema paragraph about Mahesh Babu, films, directors, and release context. |
| A question asking the height of the tallest Shiva temple in Indonesia. | A paragraph about Indonesian Hindu and Buddhist temples and their structure. |
| A question asking who directed a film. | A paragraph about a film and its director, cast, and production context. |
| A question asking who wanted Amitabh Bachchan to act. | A paragraph about Amitabh Bachchan's family, education, and early career context. |
