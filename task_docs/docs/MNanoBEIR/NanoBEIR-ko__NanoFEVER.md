# MNanoBEIR / NanoBEIR-ko / NanoFEVER

## Overview

`NanoBEIR-ko__NanoFEVER` is the Korean NanoBEIR version of FEVER, a fact
verification evidence retrieval benchmark. The task uses Korean translated
claims as queries and asks a retriever to rank Korean translated Wikipedia
passages that contain evidence for verification. The Nano split contains 50
queries, 4,996 documents, and 57 positive qrels. Most claims have one positive
evidence passage, while 6 queries have multiple positives. The task is a
compact test of claim-to-Wikipedia retrieval, where dense retrieval is the
strongest top-rank profile and hybrid retrieval gives the best top-100
coverage.

## Details

### What the Original Data Measures

[FEVER](https://arxiv.org/abs/1803.05355) introduced a large-scale fact
extraction and verification dataset built from claims and Wikipedia evidence.
BEIR evaluates the retrieval step: the system must find evidence passages before
a verifier can classify a claim as supported, refuted, or not enough
information. This Korean NanoBEIR version preserves that setting with
translated claims and translated Wikipedia passages. The task measures entity
matching, predicate matching, and evidence selection under Korean translation.

### Observed Data Profile

The task has 50 queries and 4,996 documents. It contains 57 positive qrels,
with 1.14 positives per query on average. The positives-per-query distribution
is 1 minimum, 1.00 median, and 3 maximum, and 12.0% of queries are
multi-positive. Queries are short claims averaging 26.38 characters, while
documents average 648.15 characters. The examples include claims about a rock
band, a sitcom, aircraft production in Burbank, Nero, and the film "Scream 2".

### BM25 Evaluation Profile

The BM25 top-500 subset reaches nDCG@10 = 0.5723, hit@10 = 0.7400, and
Recall@100 = 0.9123. BM25 benefits from entity names, titles, and distinctive
phrases in FEVER claims. It still trails the other profiles because the evidence
passage may express the claim through surrounding context, translated title
variation, or a predicate that does not repeat the query exactly. Lexical
matching provides a useful baseline but is not sufficient for best top-rank
evidence retrieval.

### Dense Evaluation Profile

The dense `harrier-oss-270m` top-500 subset reaches nDCG@10 = 0.7335, hit@10 =
0.9400, and Recall@100 = 0.9649. Dense retrieval is the strongest top-10
profile for this task. The result indicates that embedding similarity is highly
effective for mapping short Korean claims to evidence-bearing Wikipedia
passages, especially when the passage contains the answer context rather than
the exact claim wording. Dense retrieval also improves candidate coverage over
BM25.

### Reranking Hybrid Evaluation Profile

The `reranking_hybrid` subset uses 100 candidates per query and reaches
nDCG@10 = 0.7001, hit@10 = 0.9000, and Recall@100 = 0.9825, with no rank-101
safeguard rows. Hybrid retrieval has the best top-100 coverage, while dense
retrieval remains better on nDCG@10 and hit@10. This means that combining
lexical and dense candidates is valuable for downstream reranking, but the
fused order is not as strong as dense-only ranking near the top.

### Metric Interpretation for Model Researchers

This task separates semantic evidence ranking from candidate coverage. BM25 is
strong for exact entity recall, dense retrieval is best at placing evidence high
in the ranking, and hybrid retrieval is best at keeping positives in the top
100. A model improvement should be described in terms of whether it improves
claim semantics, entity recall, or reranker-ready candidate coverage. Since
most queries have one positive, early rank errors strongly affect nDCG@10.

### Query and Relevance Type Tendencies

Queries are short factual claims that usually contain an entity plus a
predicate. Relevant passages are Wikipedia summaries that provide the context
needed to verify the claim. A page about the same entity is not always enough;
the evidence must address the specific assertion, such as whether a program is
a sitcom or whether a film's country claim is true.

### Representative Failure Modes

BM25 can retrieve pages with the right entity but not the evidence-bearing
predicate. Dense retrieval can retrieve semantically related pages that do not
verify the claim. Hybrid retrieval can recover more positives in the candidate
set while still ranking topical distractors above evidence passages. Translation
variation in names and titles can affect all retrieval families.

### Training Data That May Help

Useful training data includes non-overlapping FEVER-style claim-evidence pairs,
Wikipedia evidence retrieval, Korean fact-checking data, and multilingual claim
verification. Hard negatives should come from the same entity page, nearby
entities, or title-sharing pages that do not verify the predicate. Training
should exclude FEVER, BEIR, NanoBEIR, and overlapping translated Wikipedia
evidence from this benchmark.

### Model Improvement Notes

Strong systems should preserve exact entity recall while learning to rank
predicate-relevant evidence. Dense retrieval already performs well at top-10
ranking, so a practical pipeline should use hybrid retrieval for coverage and a
reranker to recover dense-like evidence ordering.

## Example Data

| Query | Positive document |
| --- | --- |
| 키스 고쇼는 그레이트풀 데드를 잘 알고 있었다. | 그레이트풀 데드는 1965년 캘리포니아주 팔로 알토에서 결성된 미국의 록 밴드이다. |
| '타라크 메타 카 울타 카슈마'는 시트콤이다. | '타라크 메타의 올타흐 차슈마'는 인도에서 가장 오래 방영된 시트콤 드라마이다. |
| 캘리포니아 버뱅크에서는 비밀스럽고 기술적으로 진보된 비행기들이 생산되었다. | 버번크는 미국 캘리포니아주 남부 로스앤젤레스 카운티에 위치한 도시로, 여러 미디어 기업이 있는 곳이다. |
| 네로는 사람이다. | 율리오-클라우디우스 왕조라는 용어는 로마 최초의 다섯 황제인 아우구스투스, 티베리우스, 칼리굴라, 클라우디우스, 네로를 가리킨다. |
| Scream 2는 독일 영화로만 제작되었다. | 《스크림 2》는 웨스 크레이븐이 감독하고 케빈 윌리엄슨이 각본을 쓴 1997년 미국의 슬래셔 영화이다. |

### Public Sources

- [FEVER: a Large-scale Dataset for Fact Extraction and VERification](https://arxiv.org/abs/1803.05355).
- [BEIR: A Heterogeneous Benchmark for Zero-shot Evaluation of Information Retrieval Models](https://arxiv.org/abs/2104.08663).
- [MMTEB: Massive Multilingual Text Embedding Benchmark](https://arxiv.org/abs/2502.13595).
- [Zeta Alpha NanoBEIR collection](https://huggingface.co/collections/zeta-alpha-ai/nanobeir).
- [hakari-bench/NanoBEIR-ko](https://huggingface.co/datasets/hakari-bench/NanoBEIR-ko).

### Source Reference Table

| Title | Year | Type | URL |
| --- | ---: | --- | --- |
| FEVER: a Large-scale Dataset for Fact Extraction and VERification | 2018 | task paper | https://arxiv.org/abs/1803.05355 |
| BEIR: A Heterogeneous Benchmark for Zero-shot Evaluation of Information Retrieval Models | 2021 | benchmark paper | https://arxiv.org/abs/2104.08663 |
| MMTEB: Massive Multilingual Text Embedding Benchmark | 2025 | benchmark paper | https://arxiv.org/abs/2502.13595 |
| NanoBEIR: Smaller BEIR dataset subsets | 2024 | dataset collection | https://huggingface.co/collections/zeta-alpha-ai/nanobeir |
