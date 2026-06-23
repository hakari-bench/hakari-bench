# NanoRARb / NanoSpartQA

## Overview

`NanoSpartQA` is an English spatial reasoning retrieval task from NanoRARb. It recasts SpartQA as answer retrieval: the query describes blocks, objects, colors, sizes, and spatial relations, and the relevant documents are short answer phrases that satisfy the question. Unlike most NanoRARb tasks, some queries have multiple positives. The task tests whether retrievers can compose spatial relations rather than only match object names. `reranking_hybrid` is the strongest profile, dense retrieval has better top-rank quality than BM25 but lower recall@100, and BM25 provides useful lexical anchors.

## Details

### What the Original Data Measures

RAR-b uses SpartQA as a spatial reasoning task converted into retrieval. The original SpartQA benchmark focuses on textual question answering where a model must track spatial relations among entities described in language.

In this Nano task, the answer pool contains short phrases such as object descriptions, `both of them`, or `none of them`. A retriever must encode the described scene and select the answer consistent with the spatial constraints.

### Observed Data Profile

The Nano split contains 200 queries, 1,592 documents, and 384 positive qrel rows. Queries average 654.85 characters, while answer documents average 49.80 characters.

Each query has 1.92 positives on average, with a median of 1 and a maximum of 3. Ninety-two of 200 queries, or 46.0%, have multiple positives. Examples describe three blocks containing colored shapes and ask which object satisfies a relation, whether both objects satisfy it, or whether no object does.

### BM25 Evaluation Profile

The BM25 candidate subset uses top-500 candidates and reaches nDCG@10 of 0.1888, hit@10 of 0.3750, and recall@100 of 0.5260. BM25 benefits from repeated color, size, shape, and block labels. Object names in the answer can overlap directly with the query.

The limitation is spatial composition. A phrase such as `medium blue square` is not enough; the answer must also satisfy above, below, left, right, touching, or containment relations across the scene. BM25 can retrieve the right object words while missing the relational constraint.

### Dense Evaluation Profile

The dense candidate subset from `harrier_oss_v1_270m` uses top-500 candidates and reaches nDCG@10 of 0.2634, hit@10 of 0.4950, and recall@100 of 0.4870. Dense retrieval improves top-rank quality and hit@10 over BM25 but has lower recall@100.

This suggests that embeddings capture some spatial-scene semantics and answer plausibility but may miss part of the positive set when several answer phrases are valid. Dense retrieval is better at ranking an answer early when it finds it, while BM25 has broader lexical coverage.

### Reranking Hybrid Evaluation Profile

The `reranking_hybrid` subset uses top-100 candidates, with 37 rows receiving the optional rank-101 safeguard. It reaches nDCG@10 of 0.3419, hit@10 of 0.5600, and recall@100 of 0.5443. Hybrid retrieval is strongest across the reported metrics.

The improvement reflects complementary signals. Sparse matching preserves exact object descriptors, while dense retrieval contributes relational and semantic compatibility. The combined pool is the best setting for downstream reranking.

### Metric Interpretation for Model Researchers

Because some queries have multiple positives, nDCG@10 rewards ranking one or more valid answer phrases early. Hit@10 measures whether at least one positive answer appears in the first ten results, and recall@100 measures coverage of the positive answer set.

For SpartQA, hybrid retrieval is the main candidate-generation baseline. A strong model should improve spatial relation composition, not just object-name matching.

### Query and Relevance Type Tendencies

Queries are long textual scene descriptions with blocks, shapes, colors, sizes, and relative positions. Relevant documents are short answer phrases referring to selected objects or aggregate answers such as `both of them`.

Relevance depends on satisfying the spatial question. A candidate can mention the right object type but be wrong if the object is in the wrong block or relation.

### Representative Failure Modes

Common failures include matching color and shape but ignoring position, confusing block-level relations with object-level relations, selecting one object when multiple are valid, and misranking generic answers such as `both of them` or `none of them`. BM25 overweights object descriptors; dense retrieval can blur exact relation chains.

### Training Data That May Help

Useful training data includes textual spatial QA, scene-graph QA, relation-composition tasks, and retrieval pairs where answers refer to objects selected by spatial constraints. Evaluation queries, answers, and qrels should be excluded.

### Model Improvement Notes

Models should learn structured spatial representations from text. Hard negatives should share colors, shapes, sizes, and block labels but violate one relation. Multi-positive handling is important because some questions allow several correct answer phrases.

## Example Data

| Query | Positive document |
| --- | --- |
| There are three blocks. Lets call them A, B and C. Block A is below B and block B is below C. Block... [100 / 797 chars] | both of them [12 chars] |
| We have three blocks, A, B and C. Blocks B and C are above A. Block A contains one medium black squa... [100 / 484 chars] | both of them [12 chars] |
| We have three blocks, A, B and C. Block B is below block C and it is to the left of block A. Block A... [100 / 669 chars] | both of them [12 chars] |
| We have three blocks. We call them A, B and C. Block B is below and C is above A. Block A contains o... [100 / 761 chars] | the yellow thing that is touching the right edge of a block [59 chars] |
| There are three blocks, A, B and C. Block A is below C. Block C is to the right of B. Block A has a... [100 / 565 chars] | none of them [12 chars] |

### Source Reference Table

| Title | Year | Type | URL |
| --- | ---: | --- | --- |
| RAR-b: Reasoning as Retrieval Benchmark | 2024 | arXiv paper | [https://arxiv.org/abs/2404.06347](https://arxiv.org/abs/2404.06347) |
| SpartQA: A Textual Question Answering Benchmark for Spatial Reasoning | 2021 | arXiv paper | [https://arxiv.org/abs/2104.05832](https://arxiv.org/abs/2104.05832) |

### Representative Snippets

| Query | Relevant document excerpt |
| --- | --- |
| A scene describes three blocks and colored shapes, then asks whether described objects satisfy a relation. | Both of them. |
| A scene describes blocks above and below each other and objects inside block A and B. | Both of them. |
| A scene describes a blue circle and triangle in block B with relations to other shapes. | Both of them. |
| A scene asks for the object touching the right edge of a block. | The yellow thing that is touching the right edge of a block. |
| A scene describes medium blue and yellow squares across blocks. | None of them. |
