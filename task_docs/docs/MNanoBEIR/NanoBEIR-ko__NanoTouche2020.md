# MNanoBEIR / NanoBEIR-ko / NanoTouche2020

## Overview

`NanoBEIR-ko__NanoTouche2020` is the Korean NanoBEIR version of the Touché 2020
argument retrieval benchmark for controversial questions. The task uses Korean
translated debate questions as queries and asks a retriever to rank Korean
translated argument documents that address each issue. The Nano split contains
49 queries, 5,745 documents, and 932 positive qrels. Every query is
multi-positive, with 19.02 positives per query on average. The task is
therefore a broad argument retrieval benchmark: finding at least one relevant
argument is often easy, while ranking substantive and diverse arguments remains
the main challenge.

## Details

### What the Original Data Measures

[Touché 2020](https://doi.org/10.1007/978-3-030-58219-7_26) evaluated argument
retrieval for controversial questions. Relevance depends on both topic match
and argumentative content: a useful result should give reasons, evidence, or a
position that addresses the issue. BEIR includes Touché 2020 as an argument
retrieval task. In this Korean NanoBEIR version, short translated controversial
questions are matched against long translated debate-style arguments.

### Observed Data Profile

The task has 49 queries and 5,745 documents. It contains 932 positive qrels,
with positives per query ranging from 6 to 32 and a median of 19.00. Every
query has multiple positives. Queries average 21.73 characters, while documents
are long, averaging 1,032.84 characters. The examples ask about homework,
direct-to-consumer prescription drug advertising, mandatory vaccines, abortion,
and standardized testing. Many relevant arguments exist for each topic, so
coverage and ranking quality both matter.

### BM25 Evaluation Profile

The BM25 top-500 subset reaches nDCG@10 = 0.5033, hit@10 = 0.9796, and
Recall@100 = 0.7371. BM25 is strong because controversial questions and debate
documents share visible topic terms. With many positives per query, lexical
retrieval almost always finds at least one relevant argument in the top 10.
BM25 is also slightly best on nDCG@10, suggesting that topic-word anchoring
orders many early arguments effectively.

### Dense Evaluation Profile

The dense `harrier-oss-270m` top-500 subset reaches nDCG@10 = 0.4564, hit@10 =
0.8776, and Recall@100 = 0.7189. Dense retrieval is weaker than BM25 here.
Broad semantic similarity can retrieve documents about the same controversy,
but argument relevance requires more than topical relatedness. A document must
address the question with substantive argumentative content, and dense
similarity alone can over-rank general opinion passages.

### Reranking Hybrid Evaluation Profile

The `reranking_hybrid` subset uses 100 candidates per query and reaches
nDCG@10 = 0.5013, hit@10 = 0.9796, and Recall@100 = 0.7618, with no rank-101
safeguard rows. Hybrid retrieval ties BM25 on hit@10 and provides the best
Recall@100, while BM25 remains very slightly higher on nDCG@10. This makes
hybrid retrieval the better candidate source for coverage, with BM25-like
early precision.

### Metric Interpretation for Model Researchers

This task is a BM25-and-hybrid strength case. Lexical topic matching is hard to
beat for early ranking because the queries are short and the positive pool is
large. Dense retrieval underperforms when it treats general topical similarity
as argument relevance. Hybrid retrieval improves coverage while retaining
BM25-like hit behavior. Researchers should inspect whether systems rank
substantive arguments, not merely documents that mention the topic.

### Query and Relevance Type Tendencies

Queries are short controversial questions. Positive documents are long debate
arguments containing claims, examples, evidence, and rhetorical framing. A
relevant document may argue for or against the issue, so stance is not the only
criterion. The model must match the issue and recognize argument content.

### Representative Failure Modes

BM25 can over-rank long documents that repeat the topic but contain weak or
off-target argumentation. Dense retrieval can retrieve broad opinion text that
does not directly address the question. Hybrid retrieval improves coverage but
can still mix strong arguments with topical distractors. Long documents also
create partial-match errors when only a small part of a document touches the
query topic.

### Training Data That May Help

Useful training data includes non-overlapping Touché argument retrieval, debate
portal argument collections, pro/con retrieval pairs, and Korean or
multilingual argument quality data. Hard negatives should share the same
controversial topic but lack a direct argument for the query. Training should
exclude Touché 2020, BEIR, NanoBEIR, and overlapping translated argument
documents from this benchmark.

### Model Improvement Notes

Strong systems should combine topic matching with argument-quality and
specificity signals. Candidate generation should retrieve many relevant pro and
con arguments, while reranking should favor documents that directly answer the
question with explicit reasons. Because every query has many positives,
coverage diversity is important.

## Example Data

| Query | Positive document |
| --- | --- |
| 숙제는 유익한가요? | 숙제가 현대 학교에서 계속되어야 한다는 세 가지 이유가 있으며, 실천을 통해 배우는 학습자에게 도움이 된다는 주장이 제시된다. |
| 처방약을 소비자에게 직접 광고하는 것이 타당한가? | 많은 광고들은 약물의 효과에 대한 충분한 정보를 제공하지 않으며, 감정적 호소에 기반한다는 주장이 제시된다. |
| 아이들에게 어떤 백신이라도 의무화되어야 할까요? | 정부는 부모가 자녀의 건강 문제에 대해 내리는 결정에 개입할 권리를 가져서는 안 된다는 주장이 제시된다. |
| 낙태는 합법이어야 하나요? | 낙태는 태아가 생존 가능해지거나 출생한 후에 인간으로서의 인격이 시작되므로 합법화되어야 한다는 주장이 제시된다. |
| 표준화된 시험이 교육을 향상시키는가? | SAT, ACT 및 기타 표준화된 시험이 대학 교육 준비 상태에 대해 더 많은 통찰을 제공한다는 주장이 제시된다. |

### Public Sources

- [Overview of Touché 2020: Argument Retrieval](https://doi.org/10.1007/978-3-030-58219-7_26).
- [Touche20-Argument-Retrieval-for-Controversial-Questions](https://doi.org/10.5281/zenodo.6862281).
- [BEIR: A Heterogeneous Benchmark for Zero-shot Evaluation of Information Retrieval Models](https://arxiv.org/abs/2104.08663).
- [MMTEB: Massive Multilingual Text Embedding Benchmark](https://arxiv.org/abs/2502.13595).
- [Zeta Alpha NanoBEIR collection](https://huggingface.co/collections/zeta-alpha-ai/nanobeir).
- [hakari-bench/NanoBEIR-ko](https://huggingface.co/datasets/hakari-bench/NanoBEIR-ko).

### Source Reference Table

| Title | Year | Type | URL |
| --- | ---: | --- | --- |
| Overview of Touché 2020: Argument Retrieval | 2020 | benchmark paper | https://doi.org/10.1007/978-3-030-58219-7_26 |
| Touche20-Argument-Retrieval-for-Controversial-Questions | 2022 | dataset page | https://doi.org/10.5281/zenodo.6862281 |
| BEIR: A Heterogeneous Benchmark for Zero-shot Evaluation of Information Retrieval Models | 2021 | benchmark paper | https://arxiv.org/abs/2104.08663 |
| MMTEB: Massive Multilingual Text Embedding Benchmark | 2025 | benchmark paper | https://arxiv.org/abs/2502.13595 |
| NanoBEIR: Smaller BEIR dataset subsets | 2024 | dataset collection | https://huggingface.co/collections/zeta-alpha-ai/nanobeir |
