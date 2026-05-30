# MNanoBEIR / NanoBEIR-ja / NanoSCIDOCS

## Overview

`NanoBEIR-ja__NanoSCIDOCS` is the Japanese NanoBEIR version of SCIDOCS, a
scientific-document retrieval benchmark associated with the SPECTER scientific
document representation work. The task uses Japanese translated paper titles or
scientific query texts and asks a retriever to rank Japanese translated paper
abstracts or document descriptions. The Nano split contains 50 queries, 2,210
documents, and 244 positive qrels. Every query has multiple positives, usually
five. The task is a compact test of related-paper retrieval, where scientific
vocabulary helps but method, topic, and disciplinary relatedness matter more
than exact word overlap alone.

## Details

### What the Original Data Measures

[SPECTER](https://arxiv.org/abs/2004.07180) introduced document-level
representations for scientific papers using citation-informed supervision, and
SCIDOCS provides evaluation tasks for scientific document relatedness. BEIR
includes SCIDOCS as a scientific retrieval benchmark. In this Japanese NanoBEIR
version, translated title-like queries are matched against translated abstracts
or descriptions. Relevance often reflects related work, shared methods, shared
applications, or citation-like neighborhood rather than direct answer evidence.

### Observed Data Profile

The task has 50 queries and 2,210 documents. It contains 244 positive qrels,
with 4.88 positives per query on average. The positives-per-query distribution
is 3 minimum, 5.00 median, and 5 maximum, so every query is multi-positive.
Queries average 30.52 characters, while documents average 399.63 characters.
The examples cover power converters, sparse Gaussian Markov fields, texture
synthesis, RFID antennas, and heart-rate monitoring. Some translated records
also include noisy text, which makes robust document-level matching important.

### BM25 Evaluation Profile

The BM25 top-500 subset reaches nDCG@10 = 0.3116, hit@10 = 0.8200, and
Recall@100 = 0.6148. BM25 benefits from exact scientific terms, model names,
device names, and technical phrases that appear in both a query title and
related abstracts. However, scientific relatedness often crosses vocabulary
boundaries. A relevant document may share a method family or research area
without repeating the title wording, so lexical ranking is useful but limited.

### Dense Evaluation Profile

The dense `harrier-oss-270m` top-500 subset reaches nDCG@10 = 0.3498, hit@10 =
0.8400, and Recall@100 = 0.6434. Dense retrieval improves over BM25 on all
reported metrics. This indicates that embedding similarity captures
topic-level and method-level relationships that exact term matching misses.
For SCIDOCS, that behavior is central: the task is closer to related-paper
retrieval than fact lookup, so semantic representations of abstracts and titles
are important.

### Reranking Hybrid Evaluation Profile

The `reranking_hybrid` subset uses 100 to 101 candidates per query and reaches
nDCG@10 = 0.3710, hit@10 = 0.8400, and Recall@100 = 0.6516. One query uses the
rank-101 safeguard. Hybrid retrieval is the strongest profile overall, tying
dense retrieval on hit@10 and improving nDCG@10 and Recall@100. This suggests
that exact technical anchors and dense scientific relatedness are complementary
for Japanese SCIDOCS. The hybrid profile is the best approximation of a
practical related-paper candidate set.

### Metric Interpretation for Model Researchers

This task shows a clear move from lexical matching toward semantic and hybrid
retrieval. BM25 is useful for technical vocabulary but lower than dense and
hybrid retrieval. Dense retrieval captures relatedness better, while
`reranking_hybrid` gives the best balance of top-rank quality and coverage.
Researchers should inspect whether improvements come from better Japanese
scientific terminology, better abstract-level semantic representations, or more
diverse coverage across the multiple relevant papers for each query.

### Query and Relevance Type Tendencies

Queries are compact scientific titles or title-like phrases. Relevant documents
are longer abstract-style descriptions and may be related by method, domain,
or application. For example, a query about a converter, antenna, or neural
network method can have positives that discuss related designs or experiments.
The task rewards models that can represent scientific concepts beyond literal
surface overlap.

### Representative Failure Modes

BM25 can miss related work that uses different terminology for the same method.
Dense retrieval can over-rank papers from the same broad discipline that are
not close enough to be relevant. Hybrid retrieval can still mix exact term
distractors with semantic near-misses. Because every query has multiple
positives, another common failure is low diversity: retrieving one narrow
cluster of papers while missing other relevant related work.

### Training Data That May Help

Useful training data includes non-overlapping citation recommendation,
related-paper retrieval, scientific abstract retrieval, and Japanese or
multilingual scholarly text pairs. Hard negatives should come from the same
research area but differ in method, dataset, or claim. Training should exclude
SCIDOCS, SPECTER evaluation data, BEIR, NanoBEIR, and overlapping translated
abstracts from this benchmark.

### Model Improvement Notes

Strong systems should combine technical term precision with document-level
semantic relatedness. Citation-informed or related-work supervision can help
because relevance is closer to scholarly neighborhood than answer matching.
Hybrid candidate generation is effective here, but reranking should focus on
method, task, and application alignment rather than simple topic overlap.

## Example Data

| Query | Positive document |
| --- | --- |
| 新規DC-DC多レベルブーストコンバータ | マルチレベル電圧源コンバータは、大電力用途向けの新しいタイプの電力変換装置として登場している。 |
| Cholesky分解に基づく高速スパースガウスマルコフ確率場の学習 | （空の入力のため、翻訳なし） |
| 畳み込みニューラルネットワークを用いたテクスチャ合成 | 本研究では、大規模画像認識の設定において、畳み込みネットワークの深さがその精度に与える影響を調査する。 |
| RFIDシステム用の円偏波を備えた平面広帯域環状リングアンテナ | 本論文では、単一給電の広帯域円偏波スタックパッチアンテナに対して、水平メアンダストリップ給電方式を提案する。 |
| 基本的な電子部品を使用した高度なデジタル心拍モニターの設計 | 本論文では、心拍数の推定精度を向上させるために指先を使用した新しい統合型心拍数測定装置の設計と開発について報告する。 |

### Public Sources

- [SPECTER: Document-level Representation Learning using Citation-informed Transformers](https://arxiv.org/abs/2004.07180).
- [BEIR: A Heterogeneous Benchmark for Zero-shot Evaluation of Information Retrieval Models](https://arxiv.org/abs/2104.08663).
- [MMTEB: Massive Multilingual Text Embedding Benchmark](https://arxiv.org/abs/2502.13595).
- [Zeta Alpha NanoBEIR collection](https://huggingface.co/collections/zeta-alpha-ai/nanobeir).
- [hakari-bench/NanoBEIR-ja](https://huggingface.co/datasets/hakari-bench/NanoBEIR-ja).

### Source Reference Table

| Title | Year | Type | URL |
| --- | ---: | --- | --- |
| SPECTER: Document-level Representation Learning using Citation-informed Transformers | 2020 | task paper | https://arxiv.org/abs/2004.07180 |
| BEIR: A Heterogeneous Benchmark for Zero-shot Evaluation of Information Retrieval Models | 2021 | benchmark paper | https://arxiv.org/abs/2104.08663 |
| MMTEB: Massive Multilingual Text Embedding Benchmark | 2025 | benchmark paper | https://arxiv.org/abs/2502.13595 |
| NanoBEIR: Smaller BEIR dataset subsets | 2024 | dataset collection | https://huggingface.co/collections/zeta-alpha-ai/nanobeir |
