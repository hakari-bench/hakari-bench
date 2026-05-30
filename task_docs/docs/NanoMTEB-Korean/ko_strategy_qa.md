# NanoMTEB-Korean / ko_strategy_qa

## Overview

`ko_strategy_qa` is a Korean StrategyQA-style evidence retrieval task. Queries
are short Korean implicit-reasoning questions, and documents are Korean evidence
passages. The Nano split contains 200 queries, 9,251 documents, and 378
positive qrels. It is multi-positive: each query has 1.89 positives on average,
the median is two, and 61.5% of queries have more than one positive. Queries
average only 22.43 characters, while documents average 321.26 characters. The
task tests whether a retriever can find evidence needed for hidden reasoning
steps, not just match surface wording in the question.

## Details

### What the Original Data Measures

[Did Aristotle Use a Laptop? A Question Answering Benchmark with Implicit Reasoning Strategies](https://arxiv.org/abs/2101.02235)
introduced StrategyQA, a Boolean question-answering benchmark where the
reasoning strategy is implicit in the question. The paper emphasizes that
questions often require decomposition into evidence-seeking steps and that
supporting evidence may have limited lexical overlap with the question.

[taeminlee/Ko-StrategyQA](https://huggingface.co/datasets/taeminlee/Ko-StrategyQA)
adapts this setting into Korean and BEIR/MTEB-style retrieval. The Nano task
evaluates evidence retrieval rather than final yes/no answering: a model must
retrieve the passages that supply the facts needed by the hidden reasoning
chain.

### Observed Data Profile

The split has 200 Korean queries, 9,251 documents, and 378 positive judgments.
Many queries have multiple evidence passages, with a maximum of five positives.
Queries are short and sometimes under-specified because the reasoning step is
implicit. Documents are short evidence passages, often with title prefixes and
entity-centered factual content.

Examples include evidence about Snowdon's annual precipitation, Joan Crawford's
career, Elton John's knighthood, halal dietary restrictions, and the inventor of
the polio vaccine. The relevant passage may not answer the query directly; it
may provide one intermediate fact needed for reasoning.

### BM25 Evaluation Profile

BM25 reaches nDCG@10 of 0.4740, hit@10 of 0.7550, and recall@100 of 0.7804.
This is a solid but limited lexical baseline. It works when the question
contains an entity or term that appears in the evidence passage, but it loses
ground when the implicit reasoning step changes the vocabulary needed for
retrieval.

The result matches the core StrategyQA challenge. A query can require evidence
about a related entity, property, date, or definition that is not directly named
in the question. Lexical frequency alone is therefore incomplete.

### Dense Evaluation Profile

Dense retrieval is strongest for top-10 ranking, with nDCG@10 of 0.7084,
hit@10 of 0.8350, and recall@100 of 0.8413. The dense model better connects
short implicit questions to semantically relevant evidence passages. It can
retrieve evidence even when the query and passage share fewer terms than a
direct QA task would.

Dense retrieval still leaves room for improvement. Multi-hop evidence can
require several distinct passages, and a dense model may retrieve only one
obvious fact while missing another supporting step. Better decomposition-aware
retrieval should improve this split.

### Reranking Hybrid Evaluation Profile

The `reranking_hybrid` profile reaches nDCG@10 of 0.6476, hit@10 of 0.8400,
and recall@100 of 0.8704. It has the best recall@100 and slightly higher
hit@10 than dense retrieval, while dense keeps the best nDCG@10. Candidate
lists contain 100 to 101 rows, with 14 safeguard-positive rows.

This is a useful hybrid pattern: dense retrieval provides strong semantic
ranking, while hybrid search exposes more supporting evidence passages for
reranking. Since many queries have multiple positives, broader candidate
coverage is especially valuable.

### Metric Interpretation for Model Researchers

`ko_strategy_qa` is dense-favorable for early ranking and hybrid-favorable for
evidence coverage. BM25 is useful but cannot fully handle implicit reasoning.
nDCG@10 measures whether useful evidence appears early, hit@10 measures whether
at least one supporting passage is found, and recall@100 measures how much of
the multi-positive evidence set is available to a downstream reasoner.

Because the task has multiple positives for most queries, a model should not be
evaluated as if there is only one correct passage. Retrieving several evidence
pieces can matter for final reasoning even when one positive is already present.

### Query and Relevance Type Tendencies

Queries are short Korean implicit-reasoning questions. Positive documents are
evidence passages about entities, definitions, dates, properties, or facts that
support the hidden decomposition. The evidence may be indirect: the passage can
provide a necessary fact rather than a final answer.

Relevance is reasoning-step evidence. A passage with shared topic words can be
irrelevant if it does not support the needed inference, while a passage with
limited overlap can be positive if it supplies the missing fact.

### Representative Failure Modes

BM25 fails when the evidence vocabulary differs from the question. Dense
retrieval can fail by selecting a semantically related passage that does not
support the specific reasoning step. Hybrid retrieval can improve coverage but
still over-rank obvious entity matches while missing less direct evidence.

Multi-positive queries add another risk: a retriever may find one evidence
passage and miss the rest, limiting a downstream reasoning model.

### Training Data That May Help

Useful training data includes non-overlapping Ko-StrategyQA train evidence
pairs, StrategyQA evidence retrieval and decomposition-step pairs, Korean
multi-hop QA evidence retrieval data, and hard negatives sharing entities but
supporting different reasoning steps. Training should exclude Ko-StrategyQA dev
examples, Nano queries, qrels, and positive evidence passages.

Synthetic data should create short Korean evidence passages about entities,
dates, definitions, and properties, then generate implicit reasoning questions
that require one or more evidence passages. Multi-positive objectives are
appropriate because the benchmark often expects multiple supporting facts.

### Model Improvement Notes

Models should learn decomposition-aware retrieval. Dense encoders need to map a
short question to the evidence implied by its hidden reasoning path. Rerankers
should judge whether a passage supports a reasoning step rather than merely
sharing an entity or topic with the query.

## Example Data

### Public Sources

- [Did Aristotle Use a Laptop? A Question Answering Benchmark with Implicit Reasoning Strategies](https://arxiv.org/abs/2101.02235)
- [taeminlee/Ko-StrategyQA](https://huggingface.co/datasets/taeminlee/Ko-StrategyQA)
- [hakari-bench/NanoMTEB-Korean](https://huggingface.co/datasets/hakari-bench/NanoMTEB-Korean)

### Source Reference Table

| Title | Year | Type | URL |
| --- | ---: | --- | --- |
| Did Aristotle Use a Laptop? A Question Answering Benchmark with Implicit Reasoning Strategies | 2021 | Paper | https://arxiv.org/abs/2101.02235 |
| taeminlee/Ko-StrategyQA | 2025 | Dataset card | https://huggingface.co/datasets/taeminlee/Ko-StrategyQA |

### Representative Snippets

| Query | Positive document excerpt |
| --- | --- |
| 스노우다운의 연간 강수량은 얼마나 되나요? | A Korean Snowdon passage describing very wet slopes and annual precipitation. |
| 조안 크로포드의 텔레비전 배우로서의 경력은 언제 끝났나요? | A Joan Crawford passage about her acting career and later roles. |
| 엘튼 존이 기사 작위를 받았나요? | An Elton John passage listing awards, honors, and recognition. |
| 1은 어떤 식단 제한을 부과합니까? | A Haram passage describing prohibited foods and emergency exceptions. |
| 소아마비 백신은 누가 만들었나요? | A polio vaccine passage naming Jonas Salk and collaborators. |
