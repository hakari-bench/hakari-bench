# NanoIndicQA / ml

## Overview

`NanoIndicQA / ml` is the Malayalam split of IndicQA retrieval. The queries are Malayalam reading-comprehension questions, and the documents are Malayalam context paragraphs.

This task evaluates Malayalam paragraph retrieval for QA. It has relatively long queries and very long context paragraphs, so a retriever must match the question to the specific supporting passage rather than rely only on short answer terms.

## Details

### What the Original Data Measures

IndicQA is part of IndicXTREME, introduced in "Towards Leaving No Indic Language Behind". It is a manually curated cloze-style reading-comprehension benchmark across Indic languages.

The MTEB retrieval version asks models to retrieve the context paragraph that supports each question. In this Malayalam split, the task tests paragraph-level evidence retrieval over a small corpus.

### Observed Data Profile

This Nano split contains 200 queries, 247 documents, and 200 positive qrels. Each query has exactly one positive. Queries average 81.55 characters, the longest query average among the observed NanoIndicQA splits here, and documents average 2,522.64 characters.

Observed examples ask about a Mughal ruler after the East India Company revolt, the year India received independence after years of struggle, R. K. Narayan's first work, a large gate built by Alauddin Khalji, and the year a Nike Apache satellite was launched. Documents are long Malayalam historical, biographical, scientific, and cultural paragraphs.

### BM25 Evaluation Profile

BM25 reaches nDCG@10 of 0.6528, hit@10 of 0.7950, and recall@100 of 0.9400. The candidate pool contains the full 247-document corpus. BM25 is strong when the question includes names, dates, or distinctive concepts that also appear in the paragraph.

However, long paragraphs and long questions can dilute lexical scoring. BM25 may select a passage with overlapping historical or biographical terms while missing the exact evidence context.

### Dense Evaluation Profile

The dense harrier-oss-270m profile reaches nDCG@10 of 0.8214, hit@10 of 0.9550, and recall@100 of 0.9900. Dense retrieval is the strongest direct profile.

The high dense score suggests strong semantic matching between Malayalam questions and contexts. Dense retrieval is particularly helpful when the question paraphrases the paragraph or when the paragraph contains a broad narrative with the answer embedded inside it.

### Reranking Hybrid Evaluation Profile

The reranking_hybrid candidate subset reaches nDCG@10 of 0.7807, hit@10 of 0.9150, and recall@100 of 0.9900. It uses 100 candidates per query, with two rank-101 safeguard positives.

Hybrid retrieval matches dense retrieval on recall@100 but trails dense on top-10 ranking. It remains a good reranking pool, while dense retrieval is the best direct ranker for this split.

### Metric Interpretation for Model Researchers

`NanoIndicQA / ml` is a high-performing Malayalam context retrieval task. BM25 is already strong, but dense retrieval provides a large top-10 improvement. The split is useful for checking whether models support Malayalam semantic QA retrieval rather than only lexical matching.

Since each query has one positive, nDCG@10 and hit@10 directly measure whether the correct context is ranked early. Recall@100 is near ceiling for dense and hybrid candidate pools.

### Query and Relevance Type Tendencies

Queries are Malayalam factual or cloze-style questions, often about historical events, rulers, literature, architecture, science, and biography. Documents are long context paragraphs from encyclopedic or educational sources.

The relevance relation is evidence support: a positive paragraph contains the fact needed to answer the question.

### Representative Failure Modes

BM25 may retrieve paragraphs with the same person, empire, or institution but not the exact answer. Dense retrieval may confuse related historical passages when several contexts describe the same period or ruler. Hybrid retrieval improves candidate coverage but still requires evidence-sensitive reranking.

Long paragraphs also make answer-localization difficult after retrieval; a top result may need downstream reading comprehension.

### Training Data That May Help

Useful training data includes Malayalam QA, Malayalam Wikipedia passage retrieval, Indic multilingual context retrieval, and long-paragraph positives with same-topic hard negatives.

Training should exclude this split's questions and positive context paragraphs.

### Model Improvement Notes

Improving this task requires Malayalam semantic representation and long-context evidence matching. Models should preserve names, dates, titles, and historical relations while handling question paraphrases.

For reranking, the model should verify answer evidence inside the paragraph, not only match the general topic.

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
| A Malayalam question asking which Mughal ruler left the country after the East India Company revolt was suppressed. | A paragraph about British control of Delhi, Mughal rulers, and the aftermath of rebellion. |
| A question asking when India gained independence after years of struggle. | A paragraph about the 1857 revolt and later anti-colonial resistance. |
| A question asking R. K. Narayan's first work. | A long biographical paragraph about R. K. Narayan, his family, education, and writing. |
| A question asking which large gate Alauddin Khalji built. | A paragraph about Qutb Minar, Delhi Sultanate construction, and related architecture. |
| A question asking the year the Nike Apache satellite was launched. | A paragraph about A. P. J. Abdul Kalam, defense work, and early Indian space activity. |
