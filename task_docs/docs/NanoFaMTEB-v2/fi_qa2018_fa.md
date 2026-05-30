# NanoFaMTEB-v2 / fi_qa2018_fa

## Overview

`fi_qa2018_fa` is a Persian financial question-answer retrieval task in NanoFaMTEB-v2. Queries are short finance questions, and positive documents are Persian answer passages or forum-style explanations. The task is adapted from FiQA-style retrieval through FaMTEB.

This task evaluates whether a retriever can connect concise financial questions to explanatory answers. Lexical financial terms help, but the answer may explain a concept, tax rule, market mechanism, or personal-finance issue using wording that differs from the query.

## Details

### What the Original Data Measures

FaMTEB includes Persian retrieval datasets derived from BEIR-style tasks and Persian data sources. `fi_qa2018_fa` uses `MCINext/fiqa-fa-v2`, a Persian FiQA retrieval variant evaluated under an MTEB-style retrieval protocol.

The original FiQA task measures financial question-answer retrieval. Relevant documents are answers or passages that address the information need in the query, often with explanatory rather than extractive wording.

### Observed Data Profile

This Nano split contains 200 queries, 10,000 documents, and 534 positive qrels. Many queries have multiple positives: 128 queries are multi-positive. Positives per query average 2.67, with a minimum of 1, median of 2.0, and maximum of 12. Queries average 65.78 characters, while documents average 763.49 characters.

Observed queries ask about taxes on stocks or ETFs, exchange-rate conversion, broker fees, state income tax for work abroad, and inflation rates. Documents are explanatory Persian passages, sometimes containing URLs, finance terminology, and regulatory context.

### BM25 Evaluation Profile

BM25 reaches nDCG@10 of 0.2923, hit@10 of 0.5300, and recall@100 of 0.6180 with a top-500 candidate pool. Financial terms such as tax, exchange rate, brokerage, income, and inflation provide useful lexical anchors.

BM25 is limited because financial answers often explain a concept rather than repeat the query wording. A short question can be answered by a passage using broader market or tax terminology, and many distractors share the same finance vocabulary.

### Dense Evaluation Profile

The dense harrier-oss-270m profile reaches nDCG@10 of 0.3525, hit@10 of 0.6150, and recall@100 of 0.6948. Dense retrieval improves over BM25 by matching question intent to explanatory answers.

Dense similarity helps connect concepts such as ETF taxation, exchange-rate categories, or consumer price index definitions to answer passages that use different wording. It still struggles with fine-grained finance distinctions, especially when many passages mention similar instruments or tax contexts.

### Reranking Hybrid Evaluation Profile

The reranking_hybrid candidate subset is strongest, with nDCG@10 of 0.3722, hit@10 of 0.6500, and recall@100 of 0.7247. It uses top-100 candidates with optional rank-101 safeguards; 25 rows contain 101 candidates and 25 safeguard-positive rows are recorded.

This is a hybrid-friendly task. BM25 contributes exact financial terms, while dense retrieval captures explanatory semantics. Combining them gives better top ranking and broader positive coverage.

### Metric Interpretation for Model Researchers

`fi_qa2018_fa` is a Persian finance QA retrieval task where both terminology and semantic explanation matter. BM25 is useful but not sufficient. Dense retrieval improves meaning matching, and hybrid retrieval provides the best overall candidate and ranking profile.

Because many queries have multiple positives, recall@100 indicates whether the retriever covers several acceptable answers, not just one.

### Query and Relevance Type Tendencies

Queries are short Persian financial questions. Documents are longer answer passages with explanations, examples, or regulatory details. Relevance depends on answering the financial question, not merely mentioning the same instrument.

### Representative Failure Modes

BM25 may retrieve passages that share finance terms but answer a different question. Dense retrieval may retrieve a conceptually related passage with the wrong jurisdiction, instrument, or tax condition. Hybrid retrieval reduces these failures but still needs fine-grained reranking.

### Training Data That May Help

Useful training data includes Persian finance QA, translated FiQA pairs, investment FAQ retrieval, and financial forum answer selection. Hard negatives should share financial terms but answer a different question.

Training should exclude evaluation queries and answer passages from this split.

### Model Improvement Notes

Improving this task requires Persian financial vocabulary and explanatory QA matching. Models should preserve terms for securities, tax, inflation, exchange rates, and fees while matching the user's actual information need.

For reranking, jurisdiction, instrument type, and question intent are important disambiguation signals.

## Example Data

### Public Sources

This task is documented through the FaMTEB paper and the `MCINext/fiqa-fa-v2` dataset card. MTEB provides the broader retrieval evaluation framework.

### Source Reference Table

| Source | Role |
| --- | --- |
| [FaMTEB: Massive Text Embedding Benchmark in Persian Language](https://arxiv.org/abs/2502.11571) | Persian embedding benchmark paper. |
| [MTEB: Massive Text Embedding Benchmark](https://arxiv.org/abs/2210.07316) | General benchmark framework. |
| [MCINext/fiqa-fa-v2](https://huggingface.co/datasets/MCINext/fiqa-fa-v2) | Public source dataset card. |
| [hakari-bench/NanoFaMTEB-v2](https://huggingface.co/datasets/hakari-bench/NanoFaMTEB-v2) | Nano benchmark dataset containing this split. |

### Representative Snippets

| Query Pattern | Positive Document Pattern |
| --- | --- |
| A Persian question about taxes on stocks or ETFs. | An answer explaining taxable realized gains and distributions. |
| A question about which exchange rate is used for a final payment. | A passage explaining bank exchange-rate categories and representative rates. |
| A question about broker fees paid to exchanges. | An explanatory answer about passive and active transaction fees. |
| A question about state income tax for self-employment while abroad. | A passage discussing state tax absence and federal or treaty context. |
| A question asking what the inflation rate is. | An answer explaining CPI and the consumer basket used to measure inflation. |
