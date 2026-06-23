# NanoMMTEB-v2 / spart_qa

## Overview

`NanoMMTEB-v2 / spart_qa` is an English spatial-reasoning retrieval task from
SpartQA. Queries describe blocks, objects, colors, sizes, and spatial
relations, while documents are short candidate answer phrases. The Nano split
has 200 queries, 1,592 documents, and 384 positive qrel rows. Many queries have
multiple valid answers, averaging 1.92 positives per query. Current diagnostics
show `reranking_hybrid` as the strongest profile, dense retrieval as better
than BM25 at the top ranks, and BM25 as limited because the correct answer
depends on composing spatial constraints rather than matching object words.

## Details

### What the Original Data Measures

SpartQA is a textual question-answering benchmark for spatial reasoning. It
uses natural-language scene descriptions and asks questions that require
tracking spatial relations across objects, blocks, and reference frames. The
MTEB retrieval framing turns correct answer phrases into retrievable candidate
documents.

The task measures whether retrieval models can connect a dense scene
description to the answer phrase satisfying all spatial constraints. It is
closer to reasoning-over-text than ordinary topical retrieval.

### Observed Data Profile

The Nano split contains 200 queries, 1,592 documents, and 384 positive qrel
rows. The average positives per query is 1.92, with a minimum of 1, median of
1, and maximum of 3. Forty-six percent of queries have multiple positives.
Queries average 654.85 characters, while candidate answer documents average
49.80 characters.

Queries are long scene descriptions followed by a spatial question. Candidate
answers are short phrases such as "both of them", "none of them", or a
description of an object satisfying the relation.

### BM25 Evaluation Profile

The dataset-provided BM25 candidate subset contains 500 candidates per query and
achieves nDCG@10 = 0.1848, hit@10 = 0.3800, and recall@100 = 0.5260. BM25 is
the weakest top-rank profile.

Lexical overlap helps when candidate answers repeat color, size, shape, or
object terms from the query. However, many wrong candidates share almost the
same vocabulary. The correct answer depends on spatial composition: left of,
above, touching, contained in, edge relation, or block relation.

### Dense Evaluation Profile

The dense `harrier_oss_v1_270m` candidate subset contains 500 candidates per
query and achieves nDCG@10 = 0.2591, hit@10 = 0.4900, and recall@100 = 0.4870.
Dense retrieval improves top-rank quality over BM25, suggesting that embedding
similarity captures some relation between scene description and answer phrase.

Dense retrieval still struggles because the answer is often a short phrase with
little semantic content by itself. A phrase like "both of them" or "none of
them" cannot be ranked correctly without resolving the full scene.

### Reranking Hybrid Evaluation Profile

The `reranking_hybrid` candidate subset contains mostly 100 candidates per
query, with 37 queries using a rank-101 safeguard row. It achieves nDCG@10 =
0.3382, hit@10 = 0.5700, and recall@100 = 0.5469. Hybrid retrieval is the best
observed profile across nDCG@10, hit@10, and recall@100.

This is a case where combining lexical object evidence with dense scene-answer
similarity helps. The hybrid pool retains more positives and ranks them better
than either BM25 or dense alone, although absolute scores remain modest because
spatial reasoning is the central difficulty.

### Metric Interpretation for Model Researchers

This is a multi-positive task for nearly half the queries. nDCG@10 rewards
ranking all valid answer phrases high, while hit@10 only checks whether at
least one positive appears near the top. Recall@100 measures whether valid
answers remain available for reranking.

Because candidate answers are short, retrieval metrics reflect both semantic
matching and reasoning limitations. High performance likely requires a model or
reranker that can parse the scene and compose relations, not only embed the
query and answer phrase.

### Query and Relevance Type Tendencies

Queries describe block worlds with colors, shapes, sizes, containment, relative
positions, and edge contacts. Relevant documents are short answer candidates
that satisfy all spatial constraints. Some questions allow multiple valid
answers.

The task rewards relation composition, object binding, and spatial constraint
checking. It penalizes systems that only match color or shape words.

### Representative Failure Modes

BM25 can retrieve a candidate with the right object vocabulary but the wrong
relation. Dense retrieval can prefer semantically generic answer phrases that
fit many questions. Hybrid retrieval can still rank a near-miss object above a
valid one when both share the same colors and shapes.

Rerankers should build or approximate a scene graph from the query and evaluate
candidate answers against the graph.

### Training Data That May Help

Useful training data includes textual spatial QA, scene-graph question
answering, synthetic block-world relation questions, and relation-composition
hard negatives. Training should preserve multiple positives where several
answer phrases are valid. The Nano split's scene queries, qrels, and answer
candidates should be excluded from training.

Synthetic data can generate text scenes with blocks, objects, colors, sizes,
and relative positions. Questions should require relation composition rather
than matching a single object mention. Negatives should reuse the same object
vocabulary while violating the queried spatial relation.

### Model Improvement Notes

Dense retrievers should encode object binding and relation composition, not
only scene topic. Sparse systems can preserve object labels but need reasoning
rerankers. Cross-encoders or structured rerankers should parse the query into a
scene graph and test candidate answers against all constraints.

For hybrid systems, `NanoMMTEB-v2 / spart_qa` is a positive hybrid case:
`reranking_hybrid` wins all three provided metrics. The remaining opportunity is
not broader retrieval alone but spatially faithful reranking.

## Example Data

| Query | Positive document |
| --- | --- |
| There are three blocks. Lets call them A, B and C. Block A is below B and block B is below C. Block... [100 / 797 chars] | both of them [12 chars] |
| We have three blocks, A, B and C. Blocks B and C are above A. Block A contains one medium black squa... [100 / 484 chars] | both of them [12 chars] |
| We have three blocks, A, B and C. Block B is below block C and it is to the left of block A. Block A... [100 / 669 chars] | both of them [12 chars] |
| We have three blocks. We call them A, B and C. Block B is below and C is above A. Block A contains o... [100 / 761 chars] | the yellow thing that is touching the right edge of a block [59 chars] |
| There are three blocks, A, B and C. Block A is below C. Block C is to the right of B. Block A has a... [100 / 565 chars] | none of them [12 chars] |

### Public Sources

- [SpartQA: A Textual Question Answering Benchmark for Spatial Reasoning](https://arxiv.org/abs/2104.05832),
  2021.
- [SpartQA generation repository](https://github.com/HLR/SpartQA_generation).
- [mteb/SpartQA](https://huggingface.co/datasets/mteb/SpartQA).
- [hakari-bench/NanoMMTEB-v2](https://huggingface.co/datasets/hakari-bench/NanoMMTEB-v2),
  Nano benchmark dataset.

### Source Reference Table

| Title | Year | Type | URL |
| --- | ---: | --- | --- |
| SpartQA: A Textual Question Answering Benchmark for Spatial Reasoning | 2021 | task paper | [https://arxiv.org/abs/2104.05832](https://arxiv.org/abs/2104.05832) |
| SpartQA generation repository | 2021 | repository | [https://github.com/HLR/SpartQA_generation](https://github.com/HLR/SpartQA_generation) |
| mteb/SpartQA | 2024 | dataset card | [https://huggingface.co/datasets/mteb/SpartQA](https://huggingface.co/datasets/mteb/SpartQA) |

### Representative Snippets

| Query pattern | Positive document pattern |
| --- | --- |
| A three-block scene asking which objects satisfy a relation. | The answer phrase "both of them." |
| A scene with medium black and blue squares in a block. | A short candidate answer naming all valid objects. |
| A scene with blue circles and triangles across blocks. | The answer phrase "both of them." |
| A scene asking for an object touching a block edge. | A phrase naming the yellow object touching the edge. |
| A scene where no candidate satisfies the relation. | The answer phrase "none of them." |
