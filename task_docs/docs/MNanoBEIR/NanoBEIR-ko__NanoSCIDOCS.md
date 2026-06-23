# MNanoBEIR / NanoBEIR-ko / NanoSCIDOCS

## Overview

`NanoBEIR-ko__NanoSCIDOCS` is the Korean NanoBEIR version of SCIDOCS, a
scientific-document retrieval benchmark associated with SPECTER. The task uses
Korean translated paper titles or scientific query texts and asks a retriever
to rank Korean translated paper abstracts or document descriptions. The Nano
split contains 50 queries, 2,210 documents, and 244 positive qrels. Every query
has multiple positives, usually five. This makes the benchmark a compact
related-paper retrieval task, where exact scientific vocabulary helps but
semantic relatedness across methods, applications, and research areas is
central.

## Details

### What the Original Data Measures

[SPECTER](https://arxiv.org/abs/2004.07180) introduced document-level
representations for scientific papers using citation-informed supervision, and
SCIDOCS provides evaluation tasks for scientific document relatedness. BEIR
includes SCIDOCS as a scientific retrieval task. In this Korean NanoBEIR
version, translated title-like queries are matched against translated abstracts
or descriptions. Relevance usually means related work, shared method,
application similarity, or citation-neighborhood similarity rather than direct
answer evidence.

### Observed Data Profile

The task has 50 queries and 2,210 documents. It contains 244 positive qrels,
with 4.88 positives per query on average. The positives-per-query distribution
is 3 minimum, 5.00 median, and 5 maximum, so every query is multi-positive.
Queries average about 32 characters, while documents average 452.83 characters.
The examples cover power converters, sparse Gaussian Markov fields, texture
synthesis, RFID antennas, and heart-rate monitoring. Some translated examples
include empty or noisy text, which further stresses robust document-level
matching.

### BM25 Evaluation Profile

The BM25 top-500 subset reaches nDCG@10 = 0.2673, hit@10 = 0.7400, and
Recall@100 = 0.6066. BM25 benefits from exact technical terms and method names,
but it is the weakest profile. Scientific relatedness often crosses vocabulary
boundaries: two papers can be relevant because they share a method family,
application, or research context without repeating the same title words. BM25
therefore provides useful anchors but misses many semantically related papers.

### Dense Evaluation Profile

The dense `harrier-oss-270m` top-500 subset reaches nDCG@10 = 0.3310, hit@10 =
0.8600, and Recall@100 = 0.6434. Dense retrieval improves strongly over BM25 on
all reported metrics. This is expected for SCIDOCS-like retrieval, where
embedding similarity can represent related methods and research areas better
than exact word frequency. Dense retrieval is therefore a better baseline for
Korean related-paper search than pure lexical matching.

### Reranking Hybrid Evaluation Profile

The `reranking_hybrid` subset uses 100 to 101 candidates per query and reaches
nDCG@10 = 0.3380, hit@10 = 0.8800, and Recall@100 = 0.6434. One query uses the
rank-101 safeguard. Hybrid retrieval has the best top-10 ranking quality and
hit@10, while tying dense retrieval on Recall@100. This suggests that lexical
technical anchors still help order the top ranks when combined with dense
scientific relatedness, even though dense retrieval supplies most of the
coverage gain.

### Metric Interpretation for Model Researchers

This task shows that scientific document retrieval is not simply keyword
matching. BM25 is useful but lower than dense and hybrid retrieval. Dense
retrieval captures paper relatedness more effectively, while `reranking_hybrid`
adds enough lexical precision to improve top-rank quality. Researchers should
inspect whether improvements come from Korean scientific terminology,
abstract-level semantic representations, or better coverage across several
related papers for each query.

### Query and Relevance Type Tendencies

Queries are compact scientific titles or title-like phrases. Relevant documents
are abstract-style descriptions and may be related by method, domain, dataset,
or application. A query about an antenna, converter, neural network, or medical
device can have positives that do not repeat the query exactly but belong to
the same scholarly neighborhood.

### Representative Failure Modes

BM25 can miss related work that uses different terminology. Dense retrieval can
over-rank broad same-field papers that are not closely related enough. Hybrid
retrieval can still mix exact technical distractors with semantic near-misses.
Because every query has several positives, low result diversity is also a
failure mode: a model may retrieve one narrow cluster and miss other related
papers.

### Training Data That May Help

Useful training data includes non-overlapping citation recommendation,
related-paper retrieval, scientific abstract retrieval, and Korean or
multilingual scholarly text pairs. Hard negatives should come from the same
research area but differ in method, dataset, or claim. Training should exclude
SCIDOCS, SPECTER evaluation data, BEIR, NanoBEIR, and overlapping translated
abstracts from this benchmark.

### Model Improvement Notes

Strong systems should combine technical term precision with document-level
semantic relatedness. Citation-informed supervision and hard negatives from the
same field are likely useful. Hybrid candidate generation is appropriate, but
reranking should compare method, task, and application alignment rather than
only lexical overlap.

## Example Data

| Query | Positive document |
| --- | --- |
| 신형 DC-DC 다단계 부스트 컨버터 [20 chars] | 초록다단계 전압원 변환기는 고출력 응용 분야를 위한 새로운 유형의 전력 변환기 옵션으로 등장하고 있다. 다단계 전압원 변환기는 일반적으로 여러 단계의 직류 콘덴서 전압을 이용하여 계단형 전압 파형을 생성한다. 다단계 변환기의 주요 제한 사항 중 하나는 서로 다른 단계들 사이의 전압 불균형이다. 서로 다른 단계들 사이의 전압을 균형 잡기 위한 기술은 일반적으... [200 / 443 chars] |
| 촐레스키 분해를 기반으로 한 빠른 희소 가우시안 마르코프 임의장 학습 [38 chars] |  [0 chars] |
| 합성곱 신경망을 이용한 텍스처 생성 [19 chars] | 본 연구에서는 대규모 이미지 인식 환경에서 합성곱 네트워크의 깊이가 정확도에 미치는 영향을 조사한다. 우리의 주요 기여는 깊이를 점차 증가시킨 네트워크에 대한 철저한 평가로, 기존 최고 수준의 구성 대비 16~19개의 가중치 층까지 깊이를 확장함으로써 상당한 성능 향상을 달성할 수 있음을 보여준다. 이러한 발견은 우리 팀이 ImageNet Challenge... [200 / 418 chars] |
| RFID 시스템을 위한 원형 편파를 가진 평면 광대역 고리형 링 안테나 [39 chars] | 본 논문에서는 범용 초고주파(UHF) 무선 주파수 인식(RFID) 응용에 적합한 단일 공급 대역폭 넓은 원형 편파 적층 패치 안테나에서 임피던스 정합을 개선하고 대칭적인 정방향 복사 패턴을 얻기 위해 수평으로 미로형(Mezzane) 스트립(HMS) 공급 기법을 제안한다. 안테나는 두 개의 모서리 절단된 패치와 HMS로 구성되며, 모두 FR4 기판의 상부면에... [200 / 633 chars] |
| 기본 전자 부품을 사용한 고급 디지털 심박수 모니터 설계 [31 chars] | 본 논문에서는 심박수 추정의 정확도를 향상시키기 위해 손가락 끝을 이용한 심박수 측정을 위한 새로운 통합 장치의 설계 및 개발을 제시하였다. 심장 관련 질병이 날로 증가함에 따라 건강 관리의 질을 보장하기 위해 정확하고 저렴한 심박수 측정 장치 또는 심장 모니터의 필요성이 절실하다. 그러나 대부분의 심박수 측정 도구와 환경은 비용이 비싸고 인간공학적 설계를... [200 / 508 chars] |

### Public Sources

- [SPECTER: Document-level Representation Learning using Citation-informed Transformers](https://arxiv.org/abs/2004.07180).
- [BEIR: A Heterogeneous Benchmark for Zero-shot Evaluation of Information Retrieval Models](https://arxiv.org/abs/2104.08663).
- [MMTEB: Massive Multilingual Text Embedding Benchmark](https://arxiv.org/abs/2502.13595).
- [Zeta Alpha NanoBEIR collection](https://huggingface.co/collections/zeta-alpha-ai/nanobeir).
- [hakari-bench/NanoBEIR-ko](https://huggingface.co/datasets/hakari-bench/NanoBEIR-ko).

### Source Reference Table

| Title | Year | Type | URL |
| --- | ---: | --- | --- |
| SPECTER: Document-level Representation Learning using Citation-informed Transformers | 2020 | task paper | [https://arxiv.org/abs/2004.07180](https://arxiv.org/abs/2004.07180) |
| BEIR: A Heterogeneous Benchmark for Zero-shot Evaluation of Information Retrieval Models | 2021 | benchmark paper | [https://arxiv.org/abs/2104.08663](https://arxiv.org/abs/2104.08663) |
| MMTEB: Massive Multilingual Text Embedding Benchmark | 2025 | benchmark paper | [https://arxiv.org/abs/2502.13595](https://arxiv.org/abs/2502.13595) |
| NanoBEIR: Smaller BEIR dataset subsets | 2024 | dataset collection | [https://huggingface.co/collections/zeta-alpha-ai/nanobeir](https://huggingface.co/collections/zeta-alpha-ai/nanobeir) |
