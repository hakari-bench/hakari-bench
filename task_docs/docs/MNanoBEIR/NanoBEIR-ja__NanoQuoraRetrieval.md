# MNanoBEIR / NanoBEIR-ja / NanoQuoraRetrieval

## Overview

`NanoBEIR-ja__NanoQuoraRetrieval` is the Japanese NanoBEIR version of Quora
duplicate-question retrieval. The task uses Japanese translated questions as
queries and asks a retriever to find Japanese translated questions with the
same or nearly the same intent. The Nano split contains 50 queries, 5,046
documents, and 70 positive qrels. Most queries have one positive, but 10
queries have multiple positives and the maximum is 6. Because both sides are
short questions, the task is a focused benchmark for paraphrase retrieval,
duplicate intent matching, and distinguishing semantic equivalence from topical
similarity.

## Details

### What the Original Data Measures

The Quora Question Pairs dataset was released as a duplicate-question
benchmark, and BEIR adapts it as a retrieval task: given one question, rank a
pool of candidate questions so duplicates or semantic equivalents appear near
the top. The Japanese NanoBEIR version keeps the same duplicate-question
retrieval setting after translation. A relevant document may be nearly
identical to the query, a more concise reformulation, or a question that asks
the same thing with different wording.

### Observed Data Profile

The task has 50 queries and 5,046 candidate questions. It contains 70 positive
qrels, with 1.40 positives per query on average. The positives-per-query
distribution is 1 minimum, 1.00 median, and 6 maximum, with 20.0%
multi-positive queries. Queries and documents are very short: query length is
about 27 characters and document length is about 32 characters. With so little
context, small wording differences matter. A model must decide whether two
questions are interchangeable, not simply whether they share a topic.

### BM25 Evaluation Profile

The BM25 top-500 subset reaches nDCG@10 = 0.7391, hit@10 = 0.9000, and
Recall@100 = 0.9714. BM25 is very strong because duplicate questions often
reuse key words or phrases. Exact overlap is especially helpful for short
Japanese questions where shared nouns, names, or technical terms dominate the
text. However, BM25 is slightly weaker than dense retrieval on nDCG@10, showing
that word overlap alone is not always enough to rank paraphrases in the best
order.

### Dense Evaluation Profile

The dense `harrier-oss-270m` top-500 subset reaches nDCG@10 = 0.7722, hit@10 =
0.8800, and Recall@100 = 0.9286. Dense retrieval has the best top-10 ranking
quality, even though its hit@10 and Recall@100 are below BM25. This pattern
means embedding similarity is effective at ranking semantically equivalent
questions near the top when it finds them, but lexical retrieval catches more
positives broadly. Dense retrieval is strongest for paraphrases whose intent is
preserved despite wording changes.

### Reranking Hybrid Evaluation Profile

The `reranking_hybrid` subset uses 100 candidates per query and reaches
nDCG@10 = 0.7417, hit@10 = 0.8600, and Recall@100 = 1.0000, with no rank-101
safeguard rows. Hybrid retrieval has perfect top-100 coverage, which makes it a
strong candidate source for downstream reranking. Its top-10 quality is close
to BM25 but below dense retrieval. This suggests that combining lexical and
dense results retrieves every judged duplicate, but the fused order still needs
a semantic reranker to prioritize true duplicate intent.

### Metric Interpretation for Model Researchers

This task separates three retrieval strengths. BM25 provides broad coverage for
near-duplicate wording, dense retrieval gives the best top-rank semantic
ordering, and hybrid retrieval gives complete top-100 coverage. For model
development, the key question is whether the system can avoid confusing topic
overlap with duplicate intent. A better model should improve dense-like nDCG
while retaining hybrid-level candidate coverage.

### Query and Relevance Type Tendencies

The examples include self-deprecating jokes, clever lies, Quora political
recommendations, physical strength, and quantum satellites. Some positives are
nearly literal duplicates, while others add or remove detail but keep the same
information need. This makes the task sensitive to both semantic compression
and over-broad matching: a related question is not necessarily a duplicate.

### Representative Failure Modes

BM25 can over-rank questions that share visible words but ask something
different. Dense retrieval can overmerge semantically related questions when a
topic dominates the representation. Hybrid retrieval can include all positives
but still rank lexical distractors above paraphrases. Multiple-positive queries
also reveal whether a model retrieves only the most literal duplicate or covers
less obvious paraphrases.

### Training Data That May Help

Useful training data includes non-overlapping duplicate-question pairs,
paraphrase retrieval, Japanese question matching, and multilingual semantic
similarity data. Hard negatives should share topic words but ask for different
information. Training should exclude Quora Question Pairs, BEIR, NanoBEIR, and
overlapping translated question pairs from this benchmark.

### Model Improvement Notes

Strong systems should represent question intent at sentence level while keeping
enough lexical detail to avoid false duplicates. Hard negatives are essential:
they should be short, topically similar, and not interchangeable with the query.
Hybrid retrieval is valuable for candidate generation, but final ranking should
be driven by duplicate-intent semantics.

## Example Data

| Query | Positive document |
| --- | --- |
| 自分のジョークを笑っても大丈夫ですか？ [19 chars] | 自分のジョークで笑うのは変ですか？ [17 chars] |
| 今までで最高の嘘は何ですか？ [14 chars] | 今までで最も巧妙に練り上げた嘘は何ですか？ [21 chars] |
| なぜQuoraは頻繁に私のフィードにドナルド・トランプを貶めるような回答をおすすめするのですか？ [48 chars] | なぜクオラではドナルド・トランプに関する質問に対して、主観的で偏った回答しか見受けられるのでしょうか？ [51 chars] |

### Public Sources

- [Quora Question Pairs](https://kaggle.com/competitions/quora-question-pairs).
- [BEIR: A Heterogeneous Benchmark for Zero-shot Evaluation of Information Retrieval Models](https://arxiv.org/abs/2104.08663).
- [MMTEB: Massive Multilingual Text Embedding Benchmark](https://arxiv.org/abs/2502.13595).
- [Zeta Alpha NanoBEIR collection](https://huggingface.co/collections/zeta-alpha-ai/nanobeir).
- [hakari-bench/NanoBEIR-ja](https://huggingface.co/datasets/hakari-bench/NanoBEIR-ja).

### Source Reference Table

| Title | Year | Type | URL |
| --- | ---: | --- | --- |
| Quora Question Pairs | 2017 | dataset page | [https://kaggle.com/competitions/quora-question-pairs](https://kaggle.com/competitions/quora-question-pairs) |
| BEIR: A Heterogeneous Benchmark for Zero-shot Evaluation of Information Retrieval Models | 2021 | benchmark paper | [https://arxiv.org/abs/2104.08663](https://arxiv.org/abs/2104.08663) |
| MMTEB: Massive Multilingual Text Embedding Benchmark | 2025 | benchmark paper | [https://arxiv.org/abs/2502.13595](https://arxiv.org/abs/2502.13595) |
| NanoBEIR: Smaller BEIR dataset subsets | 2024 | dataset collection | [https://huggingface.co/collections/zeta-alpha-ai/nanobeir](https://huggingface.co/collections/zeta-alpha-ai/nanobeir) |
