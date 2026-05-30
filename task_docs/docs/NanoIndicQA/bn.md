# NanoIndicQA / bn

## Overview

`NanoIndicQA / bn` is the Bengali split of IndicQA retrieval. The queries are Bengali reading-comprehension questions, and the documents are Bengali context paragraphs that support the answer.

This task evaluates Bengali context retrieval in a small-corpus setting. The model must retrieve the paragraph that contains the evidence for the question, not merely return a short answer string.

## Details

### What the Original Data Measures

IndicQA is part of IndicXTREME, introduced in "Towards Leaving No Indic Language Behind". It is a manually curated cloze-style reading-comprehension benchmark for Indic languages.

The retrieval formulation uses questions as queries and context paragraphs as documents. In the Bengali split, the task measures whether a retriever can identify the Bengali paragraph that contains the necessary evidence.

### Observed Data Profile

This Nano split contains 200 queries, 250 documents, and 201 positive qrels. Queries have 1.005 positives on average, with a minimum of 1, a median of 1.0, and a maximum of 2. Only one query is multi-positive. Queries average 52.08 characters, and documents average 2,196.01 characters.

Observed examples ask about Jallianwala Bagh and public anger, the Ghurid dynasty, the national sport of Bangladesh, construction details of the Taj Mahal, and why Ashoka was called Chanda Ashoka. Documents are long Bengali paragraphs about history, culture, geography, politics, and religion.

### BM25 Evaluation Profile

BM25 reaches nDCG@10 of 0.6971, hit@10 of 0.8150, and recall@100 of 0.8955. The candidate pool contains the full 250-document corpus. BM25 is strong when Bengali names, events, dates, or historical terms repeat between the question and context.

Its main weakness is contextual matching. A question may rely on information in a long paragraph where the evidence is expressed indirectly, or several paragraphs may share the same names and cultural vocabulary.

### Dense Evaluation Profile

The dense harrier-oss-270m profile reaches nDCG@10 of 0.7773, hit@10 of 0.8700, and recall@100 of 0.9900. Dense retrieval is the strongest direct profile.

This suggests that embedding similarity helps with Bengali paragraph selection, especially when the question and paragraph do not share all surface words. Dense retrieval also improves recall substantially, making it a better candidate generator than BM25.

### Reranking Hybrid Evaluation Profile

The reranking_hybrid candidate subset reaches nDCG@10 of 0.7460, hit@10 of 0.8350, and recall@100 of 0.9701. It uses 100 candidates per query, with six rank-101 safeguard positives.

Hybrid retrieval is strong but below dense retrieval across the main metrics. It still provides a useful reranking pool by combining exact Bengali term overlap with semantic context matching.

### Metric Interpretation for Model Researchers

`NanoIndicQA / bn` is a Bengali single-context retrieval task with mostly one positive per query. nDCG@10 and hit@10 are the main indicators of whether the correct paragraph is surfaced early.

The profile is dense-favored. BM25 works well for repeated names and explicit terms, but dense retrieval is better for ranking and coverage. Hybrid retrieval is useful, but not the top direct ranker for this split.

### Query and Relevance Type Tendencies

Queries are Bengali factual or cloze-style questions. Documents are long context paragraphs, often from encyclopedic or educational material.

The relevance relation is paragraph-level evidence support. The positive paragraph should contain the information needed to answer the question.

### Representative Failure Modes

BM25 may retrieve a paragraph sharing a historical figure, place, or event but missing the requested fact. Dense retrieval may confuse related history or culture paragraphs when several cover similar topics. Hybrid retrieval can still rank a topically related paragraph above the exact evidence context.

Long context paragraphs can also contain many unrelated terms, making both lexical and dense matching noisy.

### Training Data That May Help

Useful training data includes Bengali QA context retrieval, Bengali Wikipedia passage retrieval, IndicQA-style multilingual training, and hard negatives from same-topic Bengali paragraphs.

Training should exclude this split's questions and positive context paragraphs.

### Model Improvement Notes

Improving this task requires Bengali language coverage and evidence-sensitive paragraph ranking. Models should preserve named entities, dates, and factual relations while handling paraphrased question wording.

For reranking, the key check is whether the paragraph actually contains the answer evidence, not only whether it discusses the same broad topic.

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
| A Bengali question asking who caused the Jallianwala Bagh massacre that created public anger. | A paragraph about Gandhi's non-cooperation, peaceful resistance, and public reaction to the massacre. |
| A question asking who was one of the rulers of the Ghurid dynasty. | A historical paragraph about Afghanistan, minaret remains, and medieval dynastic context. |
| A question asking the name of Bangladesh's national sport. | A cultural paragraph about Bangladeshi festivals and children's activities. |
| A question asking who made gold work on the Taj Mahal's large dome finial. | A paragraph describing Taj Mahal water systems, garden infrastructure, and architectural details. |
| A question asking why Emperor Ashoka was called Chanda Ashoka. | A paragraph discussing Ashoka's cruel nature and later Buddhist transformation. |
