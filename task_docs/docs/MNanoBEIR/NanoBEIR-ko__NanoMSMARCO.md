# MNanoBEIR / NanoBEIR-ko / NanoMSMARCO

## Overview

`NanoBEIR-ko__NanoMSMARCO` is the Korean NanoBEIR version of MS MARCO passage
retrieval. The task uses Korean translated web-search questions as queries and
asks a retriever to rank Korean translated passages that directly answer them.
The Nano split contains 50 queries, 5,043 documents, and 50 positive qrels,
with exactly one positive passage per query. It is a short-query, single-answer
retrieval task. The observed profile shows that lexical matching is not enough:
dense retrieval improves coverage, and the hybrid candidate order gives the
best nDCG@10 while matching dense Recall@100.

## Details

### What the Original Data Measures

[MS MARCO](https://arxiv.org/abs/1611.09268) introduced large-scale real user
queries paired with answer-bearing passages. BEIR evaluates the passage
retrieval version, where the model must rank the passage that answers a
web-style query. In this Korean NanoBEIR version, translated questions and
translated passages preserve the same retrieval behavior. The task measures
whether a model can map concise search intent to a short answer passage.

### Observed Data Profile

The task has 50 queries and 5,043 documents. It contains 50 positive qrels, so
every query has exactly one positive. Queries average only 19.12 characters,
while documents average 169.25 characters. The examples include a definition of
rumination syndrome, a song performer, a television role, desert locations, and
the meaning of "copper" for police officers. These are compact web questions
where the relevant passage must answer the query, not merely discuss the same
term.

### BM25 Evaluation Profile

The BM25 top-500 subset reaches nDCG@10 = 0.3320, hit@10 = 0.5400, and
Recall@100 = 0.8800. BM25 finds many positives somewhere in the top 100, but
its early ranking is weak. Short Korean questions provide few lexical anchors,
and answer passages often use explanatory wording. Entity names and quoted
titles help, but definition and meaning questions often require semantic answer
matching beyond exact token overlap.

### Dense Evaluation Profile

The dense `harrier-oss-270m` top-500 subset reaches nDCG@10 = 0.4164, hit@10 =
0.6200, and Recall@100 = 0.9600. Dense retrieval improves over BM25 on every
reported metric. This indicates that embedding similarity is better suited to
matching concise Korean web queries with answer-bearing passages, especially
when the answer is paraphrased or explanatory rather than a direct word match.

### Reranking Hybrid Evaluation Profile

The `reranking_hybrid` subset uses 100 to 101 candidates per query and reaches
nDCG@10 = 0.4371, hit@10 = 0.6000, and Recall@100 = 0.9600. Two queries use the
rank-101 safeguard. Hybrid retrieval has the best nDCG@10 and ties dense
retrieval on Recall@100, while dense has a slightly higher hit@10. This means
the hybrid order is better at graded top-10 ranking, but dense retrieval is
slightly more reliable for placing at least one positive in the top 10.

### Metric Interpretation for Model Researchers

This task highlights answer-semantic matching. BM25 provides useful candidate
recall but weak top-10 precision. Dense retrieval substantially improves both
ranking and coverage. `reranking_hybrid` gives the best nDCG@10, suggesting
that lexical anchors can still help when combined with dense signals. A model
that improves this task should demonstrate better answer-bearing passage
selection, not just broader topical similarity.

### Query and Relevance Type Tendencies

Queries are short web questions asking what, who, or where. Relevant passages
are compact answer snippets. Many distractors can share the same entity or term
without answering the question. This makes hard negatives straightforward:
they should share visible query words but fail to provide the requested
definition, identity, or location.

### Representative Failure Modes

BM25 can rank passages that repeat a term but do not answer the query. Dense
retrieval can retrieve semantically related snippets that are plausible but
non-answering. Hybrid retrieval can improve nDCG but still mix lexical
distractors into the top ranks. Because each query has one positive, small rank
shifts have a large effect on nDCG@10.

### Training Data That May Help

Useful training data includes non-overlapping web QA retrieval, Korean search
query logs, multilingual passage retrieval, and answer-bearing passage pairs.
Hard negatives should match surface terms without answering the query. Training
should exclude MS MARCO, BEIR, NanoBEIR, and overlapping translated passages
from this benchmark.

### Model Improvement Notes

Strong systems should represent short Korean queries as answer intents and
separate answer-bearing passages from topic-only snippets. Hybrid candidate
generation is useful, but reranking should prioritize direct answer support and
avoid promoting passages that merely contain the same named entity.

## Example Data

| Query | Positive document |
| --- | --- |
| 회상 증후군이란 무엇인가 | 회상 증후군은 메리시즘이라고도 하며, 음식물의 역류를 유발하는 특정되지 않은 유형의 섭식장애이다. |
| 'Here I Go Again'을 부른 사람은 누구인가요? | "Here I Go Again"은 영국의 록 밴드 화이트스네이크의 노래이다. |
| 캠런 보이스는 《리브 앤 매디》에서 루크 콘웨이 역을 맡았다. | 'Liv & Maddie'의 에피소드 미리보기에서 캐머런 보이스가 다른 디즈니 쇼로 건너와 매디를 만나는 장면이 나온다. |
| 지구의 대부분의 큰 사막은 어디에 위치하는가 | 지구의 나머지 사막들은 극지방 외부에 위치해 있다. 가장 큰 것은 북아프리카의 사하라 사막이다. |
| 경찰관에게 '코퍼(copper)'라는 말의 의미 | 'copper'는 경찰관을 뜻하며, 원어 의미는 '체포하는 자'로 설명된다. |

### Public Sources

- [MS MARCO: A Human Generated Machine Reading Comprehension Dataset](https://arxiv.org/abs/1611.09268).
- [BEIR: A Heterogeneous Benchmark for Zero-shot Evaluation of Information Retrieval Models](https://arxiv.org/abs/2104.08663).
- [MMTEB: Massive Multilingual Text Embedding Benchmark](https://arxiv.org/abs/2502.13595).
- [Zeta Alpha NanoBEIR collection](https://huggingface.co/collections/zeta-alpha-ai/nanobeir).
- [hakari-bench/NanoBEIR-ko](https://huggingface.co/datasets/hakari-bench/NanoBEIR-ko).

### Source Reference Table

| Title | Year | Type | URL |
| --- | ---: | --- | --- |
| MS MARCO: A Human Generated Machine Reading Comprehension Dataset | 2016 | task paper | https://arxiv.org/abs/1611.09268 |
| BEIR: A Heterogeneous Benchmark for Zero-shot Evaluation of Information Retrieval Models | 2021 | benchmark paper | https://arxiv.org/abs/2104.08663 |
| MMTEB: Massive Multilingual Text Embedding Benchmark | 2025 | benchmark paper | https://arxiv.org/abs/2502.13595 |
| NanoBEIR: Smaller BEIR dataset subsets | 2024 | dataset collection | https://huggingface.co/collections/zeta-alpha-ai/nanobeir |
