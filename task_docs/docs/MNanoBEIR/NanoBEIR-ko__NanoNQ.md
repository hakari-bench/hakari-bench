# MNanoBEIR / NanoBEIR-ko / NanoNQ

## Overview

`NanoBEIR-ko__NanoNQ` is the Korean NanoBEIR version of Natural Questions, an
open-domain question answering retrieval benchmark based on real Google search
questions and Wikipedia evidence. The task uses Korean translated questions as
queries and asks a retriever to rank Korean translated Wikipedia passages that
contain answer evidence. The Nano split contains 50 queries, 5,035 documents,
and 57 positive qrels. Most queries have one positive passage, while 7 queries
have two. Dense retrieval is strongest for the top ranks, while hybrid
retrieval provides the best candidate coverage.

## Details

### What the Original Data Measures

[Natural Questions](https://aclanthology.org/Q19-1026/) introduced real
information-seeking questions paired with Wikipedia answers and annotations.
BEIR uses NQ as open-domain QA retrieval: the system must retrieve passages
that contain answer evidence before a downstream reader can answer the
question. In this Korean NanoBEIR version, translated questions are matched
against translated Wikipedia passages, testing short question semantics,
entity matching, and answer-context retrieval.

### Observed Data Profile

The task has 50 queries and 5,035 documents. It contains 57 positive qrels,
with 1.14 positives per query on average. The positives-per-query distribution
is 1 minimum, 1.00 median, and 2 maximum, and 14.0% of queries are
multi-positive. Queries average 29.30 characters, while documents average
274.21 characters. The examples ask about a sports event location, a film's
origin, the meaning of a landmark's location, a constitutional clause, and a
song credit.

### BM25 Evaluation Profile

The BM25 top-500 subset reaches nDCG@10 = 0.4301, hit@10 = 0.6200, and
Recall@100 = 0.7895. BM25 can exploit names, titles, and distinctive terms, but
short Korean questions often do not share enough surface wording with the
answer passage. Evidence may be expressed through surrounding encyclopedia
context rather than direct repetition of the query. BM25 is therefore useful as
an entity-aware baseline but limited for answer semantics.

### Dense Evaluation Profile

The dense `harrier-oss-270m` top-500 subset reaches nDCG@10 = 0.5805, hit@10 =
0.8400, and Recall@100 = 0.9298. Dense retrieval is clearly the strongest
top-10 profile. It connects question intent to answer-bearing passages more
effectively than exact term matching, especially when the passage expresses the
answer through explanation, date, relation, or context. Dense retrieval also
substantially improves candidate coverage over BM25.

### Reranking Hybrid Evaluation Profile

The `reranking_hybrid` subset uses 100 candidates per query and reaches
nDCG@10 = 0.5033, hit@10 = 0.7200, and Recall@100 = 0.9825, with no rank-101
safeguard rows. Hybrid retrieval has the best Recall@100, but its top-10
ranking is weaker than dense retrieval. This means the hybrid candidate pool is
excellent for downstream reranking, while dense retrieval is the stronger
first-stage order when only the top ranks are used directly.

### Metric Interpretation for Model Researchers

This task cleanly separates answer-ranking quality from coverage. BM25 is the
weakest because lexical overlap undercaptures question-answer relations. Dense
retrieval is best for nDCG@10 and hit@10. Hybrid retrieval is best for
Recall@100, making it valuable when a reranker follows candidate generation.
Model improvements should be described as semantic answer ranking, candidate
coverage, or both.

### Query and Relevance Type Tendencies

Queries are short open-domain questions. Relevant passages are Wikipedia-style
summaries that contain the answer in context. The retriever must match the
relation expressed by the question, such as where an event took place, why a
landmark is located somewhere, or who participated in a song, not just the
headline entity.

### Representative Failure Modes

BM25 can retrieve the right entity but the wrong answer passage. Dense
retrieval can retrieve semantically related Wikipedia passages that omit the
specific answer. Hybrid retrieval can recover more positives in the candidate
set while still ranking lexical or semantic distractors above the evidence.
For the few two-positive queries, retrieving only one evidence passage remains
a coverage error.

### Training Data That May Help

Useful training data includes non-overlapping open-domain QA retrieval,
Wikipedia question-passage pairs, Korean answer retrieval, and multilingual QA
evidence retrieval. Hard negatives should contain related entities without the
answer. Training should exclude Natural Questions, BEIR, NanoBEIR, and
overlapping translated passages from this benchmark.

### Model Improvement Notes

Strong systems should represent short Korean questions as answer-seeking
intents while preserving entity precision. Dense retrieval is a strong direct
ranker; hybrid candidates are useful for reranking experiments that seek higher
coverage without losing semantic answer ordering.

## Example Data

| Query | Positive document |
| --- | --- |
| 올해 파이널 포는 어디에서 열리나요? | 2018년 NCAA 디비전 I 남자 농구 토너먼트는 텍사스주 샌안토니오의 알라모돔에서 열린 챔피언십 경기를 끝으로 막을 내렸다. |
| 『크리스마스 전날의 악몽』은 원래 디즈니 영화였나요? | 『크리스마스의 악몽』은 1982년 월트 디즈니 피처 애니메이션에서 일하던 팀 버튼이 쓴 시에서 비롯되었다. |
| 왜 북쪽의 천사상이 거기에 있는가 | 고름리에 따르면, 천사의 의미는 광부들의 역사, 산업 시대에서 정보 시대로의 전환, 변화하는 희망과 두려움을 상징하는 것이었다. |
| 3/5 타협안은 헌법의 어디에 처음 명시되어 있는가 | 3분의 5 타협은 미국 헌법 제1조 제2항 제3항에 명시되어 있다. |
| 'Somebody's Watching Me'는 마이클 잭슨이 피처링한 로크웰이 부른 곡입니다. | "Somebody's Watching Me"는 미국 가수 록웰이 발표한 곡이며, 마이클 잭슨이 코러스 보컬로 참여했다. |

### Public Sources

- [Natural Questions: A Benchmark for Question Answering Research](https://aclanthology.org/Q19-1026/).
- [BEIR: A Heterogeneous Benchmark for Zero-shot Evaluation of Information Retrieval Models](https://arxiv.org/abs/2104.08663).
- [MMTEB: Massive Multilingual Text Embedding Benchmark](https://arxiv.org/abs/2502.13595).
- [Zeta Alpha NanoBEIR collection](https://huggingface.co/collections/zeta-alpha-ai/nanobeir).
- [hakari-bench/NanoBEIR-ko](https://huggingface.co/datasets/hakari-bench/NanoBEIR-ko).

### Source Reference Table

| Title | Year | Type | URL |
| --- | ---: | --- | --- |
| Natural Questions: A Benchmark for Question Answering Research | 2019 | task paper | https://aclanthology.org/Q19-1026/ |
| BEIR: A Heterogeneous Benchmark for Zero-shot Evaluation of Information Retrieval Models | 2021 | benchmark paper | https://arxiv.org/abs/2104.08663 |
| MMTEB: Massive Multilingual Text Embedding Benchmark | 2025 | benchmark paper | https://arxiv.org/abs/2502.13595 |
| NanoBEIR: Smaller BEIR dataset subsets | 2024 | dataset collection | https://huggingface.co/collections/zeta-alpha-ai/nanobeir |
