# NanoIndicQA / mr

## Overview

`NanoIndicQA / mr` is the Marathi split of IndicQA retrieval. The queries are Marathi reading-comprehension questions, and the documents are Marathi paragraphs that support the answer.

This task evaluates Marathi context retrieval in a compact QA-derived corpus. The model must retrieve the full evidence paragraph for a question, often where multiple questions share related historical, scientific, or biographical passages.

## Details

### What the Original Data Measures

IndicQA is a manually curated cloze-style reading-comprehension component of IndicXTREME, introduced in "Towards Leaving No Indic Language Behind". The retrieval adaptation uses each question as a query and the source context as the relevant document.

In the Marathi split, the task measures whether retrieval models can connect Marathi factual questions to their supporting Marathi paragraphs.

### Observed Data Profile

This Nano split contains 200 queries, 250 documents, and 200 positive qrels. Each query has exactly one positive. Queries average 59.85 characters, and documents average 1,711.74 characters.

Observed examples ask about when Amartya Sen moved to West Bengal with his family, excavated stone-age tools, Ashoka's historical legacy, the last Hindu emperor to rule Delhi, and a statement about no society having the right to enslave another. Documents are long Marathi historical, biographical, political, and scientific paragraphs.

### BM25 Evaluation Profile

BM25 reaches nDCG@10 of 0.4612, hit@10 of 0.5950, and recall@100 of 0.8400. The candidate pool contains the full 250-document corpus. BM25 is useful when named entities, dates, or distinctive terms are repeated.

The relatively low hit rate indicates that lexical overlap is not enough. Marathi questions may use different wording from the evidence sentence, and long paragraphs about related historical topics can share many terms.

### Dense Evaluation Profile

The dense harrier-oss-270m profile reaches nDCG@10 of 0.6720, hit@10 of 0.8150, and recall@100 of 0.9700. Dense retrieval is the strongest direct profile.

This shows that semantic matching is important for Marathi IndicQA. Dense retrieval can connect a factual question to its context even when the exact terms are not repeated prominently.

### Reranking Hybrid Evaluation Profile

The reranking_hybrid candidate subset reaches nDCG@10 of 0.5916, hit@10 of 0.7600, and recall@100 of 0.9650. It uses 100 candidates per query, with seven rank-101 safeguard positives.

Hybrid retrieval has strong candidate coverage but lower top-10 ranking than dense retrieval. It is useful for reranking, while dense retrieval is the better first-stage ranker in this split.

### Metric Interpretation for Model Researchers

`NanoIndicQA / mr` is a dense-favored Marathi paragraph retrieval task. The difference between BM25 and dense retrieval is large enough to expose weak Marathi semantic representations.

Because each query has one positive, hit@10 and nDCG@10 are the key ranking metrics. Recall@100 is useful for measuring whether a candidate pool gives a reranker a chance to recover the correct paragraph.

### Query and Relevance Type Tendencies

Queries are Marathi factual or cloze-style questions. Documents are long context paragraphs about history, biography, politics, science, and society.

The relevance relation is evidence support: the positive paragraph contains the information needed to answer the question.

### Representative Failure Modes

BM25 may retrieve paragraphs with the same person, dynasty, or topic but not the requested fact. Dense retrieval may confuse semantically close history or biography paragraphs. Hybrid retrieval improves coverage but still requires precise evidence ranking.

When multiple questions target related contexts, paragraph-level topic matching can be insufficient for exact retrieval.

### Training Data That May Help

Useful training data includes Marathi QA context retrieval, Marathi Wikipedia retrieval, multilingual IndicQA training, and hard negatives from the same science, history, biography, or political domains.

Training should exclude this split's questions and positive context paragraphs.

### Model Improvement Notes

Improving this task requires Marathi semantic coverage and evidence-sensitive paragraph ranking. Models should preserve names, dates, titles, and factual relations while handling question-context paraphrase.

For reranking, the model should determine whether the paragraph contains the requested answer evidence, not only whether it covers the same broad topic.

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
| A Marathi question asking in which year Amartya Sen moved to West Bengal with his family. | A biographical paragraph about Amartya Sen's birth, family, and early life. |
| A question asking when stone-age tools for dating were excavated in the state. | A historical paragraph about ancient settlement, Vanga, Magadha, and regional history. |
| A question asking who gave one of the most important historical legacies in Indian history. | A paragraph about Ashoka's inscriptions and their importance for history. |
| A question asking who became the last Hindu emperor to rule Delhi. | A paragraph about Akbar, Sher Shah Suri's lineage, and Delhi politics. |
| A question asking who said that no society has the right to enslave another by pressure. | A paragraph about the Simon Commission, constitutional rights, and oppressed communities. |
