# MNanoBEIR / NanoBEIR-ko / NanoQuoraRetrieval

## Overview

`NanoBEIR-ko__NanoQuoraRetrieval` is the Korean NanoBEIR version of Quora
duplicate-question retrieval. The task uses Korean translated questions as
queries and asks a retriever to find Korean translated questions that express
the same or nearly the same intent. The Nano split contains 50 queries, 5,046
documents, and 70 positive qrels. Most queries have one positive, while 10
queries have multiple positives and the maximum is 6. Because both queries and
documents are short questions, the benchmark focuses on paraphrase retrieval,
duplicate intent matching, and separating true equivalence from topical
similarity.

## Details

### What the Original Data Measures

The Quora Question Pairs dataset was released as a duplicate-question
benchmark, and BEIR adapts it as a retrieval task. Given one question, the
system must rank candidate questions so that duplicates or semantic equivalents
appear near the top. In this Korean NanoBEIR version, translated questions
preserve that sentence-level retrieval setting. Relevance can come from nearly
identical wording, a concise rephrasing, or a different expression of the same
information need.

### Observed Data Profile

The task has 50 queries and 5,046 candidate questions. It contains 70 positive
qrels, with 1.40 positives per query on average. The positives-per-query
distribution is 1 minimum, 1.00 median, and 6 maximum, with 20.0%
multi-positive queries. Queries average 28.70 characters, while documents
average 32.81 characters. With such short text, each token matters, and broad
topic similarity can easily be confused with duplicate intent.

### BM25 Evaluation Profile

The BM25 top-500 subset reaches nDCG@10 = 0.7062, hit@10 = 0.8800, and
Recall@100 = 0.9714. BM25 is strong because duplicate questions often reuse key
topic words or phrases. Exact overlap is especially useful for short questions,
where shared nouns can dominate the text. However, BM25 is well below dense
retrieval on nDCG@10, showing that lexical matching alone is not enough to rank
paraphrases and equivalent questions in the best order.

### Dense Evaluation Profile

The dense `harrier-oss-270m` top-500 subset reaches nDCG@10 = 0.8133, hit@10 =
0.9000, and Recall@100 = 0.9714. Dense retrieval is the strongest top-rank
profile. It matches BM25 on top-100 coverage while improving both nDCG@10 and
hit@10. This is the expected behavior for duplicate-question retrieval:
sentence embeddings are well suited to recognizing equivalent intent even when
wording changes.

### Reranking Hybrid Evaluation Profile

The `reranking_hybrid` subset uses 100 candidates per query and reaches
nDCG@10 = 0.7632, hit@10 = 0.9000, and Recall@100 = 1.0000, with no rank-101
safeguard rows. Hybrid retrieval has perfect top-100 coverage and ties dense
retrieval on hit@10, but dense remains stronger on nDCG@10. This makes hybrid
retrieval an excellent candidate pool for reranking, while dense retrieval is
the better first-stage order for the highest ranks.

### Metric Interpretation for Model Researchers

This task separates semantic ranking from exhaustive duplicate coverage. BM25
is strong because lexical overlap is common, dense retrieval gives the best
top-10 ordering, and hybrid retrieval guarantees all positives in the top 100.
Researchers should examine whether gains come from paraphrase understanding,
exact duplicate handling, or avoiding topic-only false positives. A strong
system should preserve hybrid-level coverage while approaching dense-level
nDCG.

### Query and Relevance Type Tendencies

The examples include questions about laughing at one's own jokes, clever lies,
Quora's recommendations about Donald Trump, physical strength, and quantum
satellites. Some positives are nearly identical, while others add or remove
detail without changing the intent. Related-but-different questions are hard
negatives because they may share most topic words but ask for different
information.

### Representative Failure Modes

BM25 can over-rank questions that share terms but differ in intent. Dense
retrieval can overmerge related questions if their topical semantics are close.
Hybrid retrieval can recover all positives while still placing lexical
distractors too high. Multiple-positive queries reveal whether a model finds
only the literal duplicate or also retrieves less direct paraphrases.

### Training Data That May Help

Useful training data includes non-overlapping duplicate-question pairs,
paraphrase retrieval, Korean question matching, and multilingual semantic
similarity data. Hard negatives should share topic words but ask for different
information. Training should exclude Quora Question Pairs, BEIR, NanoBEIR, and
overlapping translated question pairs from this benchmark.

### Model Improvement Notes

Strong systems should represent question intent while preserving fine lexical
distinctions. Hybrid retrieval is valuable for coverage, but final ranking
should be driven by semantic equivalence rather than broad topical similarity.
Hard negative training with short, lexically similar non-duplicates is
especially important.

## Example Data

| Query | Positive document |
| --- | --- |
| 자신의 농담에 웃는 것이 괜찮을까? [19 chars] | 자기 자신이 한 농담에 웃는 건 이상한가요? [24 chars] |
| 당신이 지어낸 최고의 거짓말은 무엇입니까? [23 chars] | 당신이 지금까지 지은 가장 잘 꾸며낸 거짓말은 무엇입니까? [32 chars] |
| 왜 Quora는 자주 내 피드에 도널드 트럼프를貶하는 답변들을 추천할까요? [41 chars] | 왜 도널드 트럼프에 관한 질문에는 주관적이고 편향된 답변만 있는 것처럼 보이나요? [45 chars] |
| 어떻게 하면 신체적으로 강해질 수 있을까요? [24 chars] | 어떻게 하면 신체적으로 강해질 수 있을까요? [24 chars] |
| 양자 위성은 어떻게 작동할 것인가? [19 chars] | 양자 위성은 어떻게 작동하며, 주요 용도는 무엇인가요? [30 chars] |

### Public Sources

- [Quora Question Pairs](https://kaggle.com/competitions/quora-question-pairs).
- [BEIR: A Heterogeneous Benchmark for Zero-shot Evaluation of Information Retrieval Models](https://arxiv.org/abs/2104.08663).
- [MMTEB: Massive Multilingual Text Embedding Benchmark](https://arxiv.org/abs/2502.13595).
- [Zeta Alpha NanoBEIR collection](https://huggingface.co/collections/zeta-alpha-ai/nanobeir).
- [hakari-bench/NanoBEIR-ko](https://huggingface.co/datasets/hakari-bench/NanoBEIR-ko).

### Source Reference Table

| Title | Year | Type | URL |
| --- | ---: | --- | --- |
| Quora Question Pairs | 2017 | dataset page | [https://kaggle.com/competitions/quora-question-pairs](https://kaggle.com/competitions/quora-question-pairs) |
| BEIR: A Heterogeneous Benchmark for Zero-shot Evaluation of Information Retrieval Models | 2021 | benchmark paper | [https://arxiv.org/abs/2104.08663](https://arxiv.org/abs/2104.08663) |
| MMTEB: Massive Multilingual Text Embedding Benchmark | 2025 | benchmark paper | [https://arxiv.org/abs/2502.13595](https://arxiv.org/abs/2502.13595) |
| NanoBEIR: Smaller BEIR dataset subsets | 2024 | dataset collection | [https://huggingface.co/collections/zeta-alpha-ai/nanobeir](https://huggingface.co/collections/zeta-alpha-ai/nanobeir) |
