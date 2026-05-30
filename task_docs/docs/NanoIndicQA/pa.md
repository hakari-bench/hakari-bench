# NanoIndicQA / pa

## Overview

`NanoIndicQA / pa` is the Punjabi split of IndicQA retrieval. The queries are Punjabi reading-comprehension questions, and the documents are Punjabi evidence paragraphs.

This task evaluates Punjabi paragraph retrieval for QA. The model must identify the context paragraph that supports the answer, often when several passages share names, actors, films, historical events, or political terms.

## Details

### What the Original Data Measures

IndicQA is part of IndicXTREME from "Towards Leaving No Indic Language Behind". It is a cloze-style reading-comprehension task that MTEB repurposes as question-to-context retrieval.

In the Punjabi split, each query is a Punjabi question and the positive document is the source paragraph containing the answer evidence.

### Observed Data Profile

This Nano split contains 200 queries, 241 documents, and 200 positive qrels. Each query has exactly one positive. Queries average 63.51 characters, and documents average 1,423.51 characters.

Observed examples ask about Kashmiri Pandits leaving the valley, participation in a named world program tour, Bhagat Singh and a bomb inspired by Auguste Vaillant, Priyanka Chopra's 2006 Farhan Akhtar action thriller, and Shah Rukh Khan's collaboration in a musical romance. Documents are Punjabi paragraphs about politics, cinema, biography, and history.

### BM25 Evaluation Profile

BM25 reaches nDCG@10 of 0.5983, hit@10 of 0.7600, and recall@100 of 0.9250. The candidate pool contains the full 241-document corpus. BM25 is strong when questions repeat distinctive names, film titles, places, or historical terms.

BM25 can still fail when several passages share the same celebrity, event, or political topic. It may retrieve the right broad subject without selecting the exact paragraph that contains the answer.

### Dense Evaluation Profile

The dense harrier-oss-270m profile reaches nDCG@10 of 0.6445, hit@10 of 0.8550, and recall@100 of 0.9800. Dense retrieval improves top-10 hit and recall over BM25.

This suggests that semantic matching helps connect Punjabi questions to supporting contexts beyond repeated words. Dense retrieval is useful when the answer relation is expressed indirectly in the paragraph.

### Reranking Hybrid Evaluation Profile

The reranking_hybrid candidate subset reaches nDCG@10 of 0.6885, hit@10 of 0.8750, and recall@100 of 0.9800. It uses 100 candidates per query, with four rank-101 safeguard positives.

Hybrid retrieval is the strongest profile in this split. It combines lexical anchors from names and titles with semantic question-context matching, improving top-10 ranking while preserving dense-level recall.

### Metric Interpretation for Model Researchers

`NanoIndicQA / pa` is a Punjabi context retrieval task where hybrid search is best. BM25 is a strong baseline, dense retrieval improves semantic matching, and reranking_hybrid gives the best top-10 ordering.

Since each query has one positive, nDCG@10 and hit@10 directly measure correct-context placement. Recall@100 is high for dense and hybrid, so reranking can focus on choosing the exact evidence paragraph.

### Query and Relevance Type Tendencies

Queries are Punjabi factual or cloze-style questions. Documents are paragraph-length contexts about politics, film, biography, history, and social events.

The relevance relation is evidence support: the positive paragraph contains the information needed to answer the query.

### Representative Failure Modes

BM25 may retrieve a paragraph with the same actor, film, or historical figure but not the requested fact. Dense retrieval may confuse related celebrity or history contexts. Hybrid retrieval reduces these failures but still needs answer-evidence discrimination.

Questions tied to film and actor biographies can be especially difficult because many paragraphs share names, years, and titles.

### Training Data That May Help

Useful training data includes Punjabi QA context retrieval, Punjabi Wikipedia passage retrieval, cross-lingual Indic QA training, and hard negatives from similar entertainment, history, and biography contexts.

Training should exclude this split's questions and positive context paragraphs.

### Model Improvement Notes

Improving this task requires Punjabi language coverage, entity-sensitive matching, and paragraph-level evidence ranking. Models should preserve names, film titles, years, and relation cues while handling question paraphrases.

For reranking, the model should check whether the paragraph contains the answer evidence rather than merely matching the named entity.

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
| A Punjabi question asking how many Kashmiri Pandits left the valley in a decade. | A paragraph about Kashmir valley population, religious composition, and political context. |
| A question asking whether a person participated in a World Program Tour. | A paragraph about Priyanka Chopra, Miss India, and career events. |
| A question asking where a French anarchist inspired Bhagat Singh to throw a bomb. | A paragraph about HSRA, Auguste Vaillant, and the Central Legislative Assembly bombing. |
| A question asking the name of Priyanka Chopra's last 2006 Farhan Akhtar action thriller. | A paragraph about Priyanka Chopra's film roles and releases. |
| A question asking with whom Khan's second collaboration in a musical romance was. | A paragraph about the 1997 film Dil To Pagal Hai, Yash Chopra, and the role of Rahul. |
