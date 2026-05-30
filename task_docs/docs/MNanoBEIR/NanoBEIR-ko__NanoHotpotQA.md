# MNanoBEIR / NanoBEIR-ko / NanoHotpotQA

## Overview

`NanoBEIR-ko__NanoHotpotQA` is the Korean NanoBEIR version of HotpotQA, a
multi-hop question answering benchmark. The task uses Korean translated
questions and asks a retriever to rank Korean translated Wikipedia paragraphs
that contain supporting evidence. The Nano split contains 50 queries, 5,090
documents, and 100 positive qrels. Every query has exactly two positives. This
fixed two-support structure makes the benchmark useful for studying whether a
retriever can recover both evidence passages needed for multi-hop reasoning,
not only the most obvious entity page.

## Details

### What the Original Data Measures

[HotpotQA](https://arxiv.org/abs/1809.09600) was designed for explainable
multi-hop question answering with supporting facts. BEIR converts it into an
evidence retrieval task: the model must rank passages that contain the facts
needed to answer the question. In this Korean NanoBEIR version, translated
questions are matched against translated Wikipedia paragraphs. The task tests
entity anchoring, relation matching, and the ability to retrieve multiple
supporting passages for one question.

### Observed Data Profile

The task has 50 queries and 5,090 documents. It contains 100 positive qrels,
with exactly two positives for every query. Queries average 49.50 characters,
while documents are short Wikipedia-style paragraphs averaging 197.13
characters. The examples include actors and sitcoms, historical figures and
swords, films and composers, football game dates, and music groups. Relevant
evidence is compact, but often split across two related passages.

### BM25 Evaluation Profile

The BM25 top-500 subset reaches nDCG@10 = 0.5966, hit@10 = 0.8800, and
Recall@100 = 0.8700. BM25 is useful because many questions contain named
entities, titles, and distinctive surface forms. However, multi-hop retrieval
requires both supporting passages, and the second support can share fewer exact
terms with the question. BM25 therefore provides strong first-hop anchoring but
does not fully cover the evidence set.

### Dense Evaluation Profile

The dense `harrier-oss-270m` top-500 subset reaches nDCG@10 = 0.6269, hit@10 =
0.8400, and Recall@100 = 0.8400. Dense retrieval slightly improves top-10
ranking quality over BM25, indicating that semantic similarity helps order some
supporting passages that do not share all query terms. At the same time, dense
hit@10 and Recall@100 are lower than BM25, showing that pure semantic retrieval
can lose some entity-specific support passages.

### Reranking Hybrid Evaluation Profile

The `reranking_hybrid` subset uses 100 to 101 candidates per query and reaches
nDCG@10 = 0.6316, hit@10 = 0.9200, and Recall@100 = 0.9300. Two queries use the
rank-101 safeguard. Hybrid retrieval is the strongest profile across all main
metrics. This pattern is well aligned with multi-hop evidence retrieval:
lexical search contributes precise entity matches, while dense retrieval adds
semantic bridge matches. The combination recovers both supports more often than
either single method.

### Metric Interpretation for Model Researchers

This task is a hybrid-strength case. BM25 is strong for entity anchors, dense
retrieval improves semantic ordering, and `reranking_hybrid` gives the best
balance of top-10 quality and top-100 coverage. Researchers should evaluate
whether a system retrieves both positives for each query, because finding only
one support can still produce a high-looking hit metric. Improvements should be
analyzed as first-hop recall, second-hop recall, and final rank ordering.

### Query and Relevance Type Tendencies

The examples ask linked questions: which actor appeared with Penny Rae Bridges,
who gave a Muramasa sword to Kaganoi Shigemochi, which film connects Joby
Harold and Samuel Sim, and when a Clemson-Oklahoma football game occurred. The
retriever must follow the relation implied by the question, not simply retrieve
a page about the first named entity.

### Representative Failure Modes

BM25 can retrieve the most explicit entity page but miss the second support.
Dense retrieval can retrieve semantically related pages that omit one required
fact. Hybrid retrieval reduces both failure modes but can still rank only one
support high enough for practical use. Errors should be inspected by whether
the missing passage is a bridge entity, answer-bearing page, or near-miss topic
match.

### Training Data That May Help

Useful training data includes non-overlapping multi-hop QA retrieval pairs,
Wikipedia evidence selection data, Korean question-to-passage retrieval, and
multilingual multi-hop evidence data. Hard negatives should include one-hop
partial matches that mention one entity but do not complete the evidence chain.
Training should exclude HotpotQA, BEIR, NanoBEIR, and overlapping translated
support paragraphs.

### Model Improvement Notes

Strong systems should combine entity-sensitive candidate generation with
relation-aware semantic ranking. Hybrid retrieval is a good first-stage
candidate source, and reranking should prioritize complete evidence chains
rather than a single high-confidence support passage.

## Example Data

| Query | Positive document |
| --- | --- |
| 페니 레이 브리지스는 어떤 다른 배우와 함께 텔레비전 시트콤에 출연했는가? | 페니 레이 브리지스는 미국의 여배우이다. 그녀는 여러 텔레비전 프로그램에 출연했으며, 『할프 앤드 할프』에서 어린 모나 역할로 알려져 있다. |
| 무라마사 학파를 창립한 인물이 만든 칼을 가가노이 시게모치에게 하사한 사람은 누구인가? | 가가노이 시게모치는 아즈치모모야마 시대의 일본 무사로, 오다 가문을 섬겼다. |
| 음악을 사무엘 심이 작곡하고 조비 할로드가 각본을 쓰고 감독한 영화는 무엇인가요? | 사무엘 심은 영화 및 텔레비전 음악 작곡가이다. |
| 플로리다주 마이애미 가든스의 선 라이프 스타디움에서 열린 이 대학 미식축구 경기의 경기 일자는 무엇인가? | 2015년 클렘슨 타이거스 미식축구 팀은 2015년 NCAA 디비전 I FBS 시즌에서 클렘슨 대학교를 대표했다. |
| Devil's Food은 미국의 록 앤드롤 밴드가 발매한 싱글 컴필레이션이다. | 『Devil's Food』은 미국의 록 앤드 롤 밴드 슈퍼서커스가 2005년 4월 미드파이 레코드를 통해 발매한 음반이다. |

### Public Sources

- [HotpotQA: A Dataset for Diverse, Explainable Multi-hop Question Answering](https://arxiv.org/abs/1809.09600).
- [BEIR: A Heterogeneous Benchmark for Zero-shot Evaluation of Information Retrieval Models](https://arxiv.org/abs/2104.08663).
- [MMTEB: Massive Multilingual Text Embedding Benchmark](https://arxiv.org/abs/2502.13595).
- [Zeta Alpha NanoBEIR collection](https://huggingface.co/collections/zeta-alpha-ai/nanobeir).
- [hakari-bench/NanoBEIR-ko](https://huggingface.co/datasets/hakari-bench/NanoBEIR-ko).

### Source Reference Table

| Title | Year | Type | URL |
| --- | ---: | --- | --- |
| HotpotQA: A Dataset for Diverse, Explainable Multi-hop Question Answering | 2018 | task paper | https://arxiv.org/abs/1809.09600 |
| BEIR: A Heterogeneous Benchmark for Zero-shot Evaluation of Information Retrieval Models | 2021 | benchmark paper | https://arxiv.org/abs/2104.08663 |
| MMTEB: Massive Multilingual Text Embedding Benchmark | 2025 | benchmark paper | https://arxiv.org/abs/2502.13595 |
| NanoBEIR: Smaller BEIR dataset subsets | 2024 | dataset collection | https://huggingface.co/collections/zeta-alpha-ai/nanobeir |
