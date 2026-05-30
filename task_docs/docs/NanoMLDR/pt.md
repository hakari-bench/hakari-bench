# NanoMLDR / pt

## Overview

`NanoMLDR / pt` is the Portuguese split of NanoMLDR, a multilingual
long-document retrieval benchmark derived from MLDR. Portuguese
paragraph-grounded questions retrieve full Portuguese articles, where the
answer-bearing paragraph may be only a small part of a long document. The Nano
split has 141 queries, 3,028 documents, and 141 positive qrel rows, with
exactly one positive document per query. Current diagnostics show an extremely
strong BM25 profile, dense retrieval as also strong but clearly lower, and
`reranking_hybrid` as recovering full recall while still trailing BM25 at the
top ranks.

## Details

### What the Original Data Measures

MLDR was introduced with the M3-Embedding work as a multilingual long-document
retrieval benchmark. The dataset card describes sampling long documents,
selecting a paragraph, and generating a specific question from that paragraph.
The retrieval target is the full article containing the answer-bearing
paragraph.

For Portuguese, this evaluates whether a model can retrieve a full long article
from a detailed Portuguese question. The positive document may include many
sections beyond the paragraph that produced the question, so the task combines
document-scale retrieval with paragraph-level evidence matching.

### Observed Data Profile

The Nano split contains 141 queries, 3,028 documents, and 141 positive qrel
rows. Every query has exactly one positive document. Queries average 110.99
characters, while documents average 14,744.68 characters.

Observed examples include questions about kinematics formulas, fugue in
classical music, cathode-ray-tube luminosity adjustment, a Brazilian municipal
road, Sega Saturn availability in Brazil, municipalities, amphibians, U.S. state
economics, Windows Vista, and John Adams. The positive documents are long
Portuguese articles containing the paragraph that generated each question.

### BM25 Evaluation Profile

The dataset-provided BM25 candidate subset contains 500 candidates per query and
achieves nDCG@10 = 0.9503, hit@10 = 0.9858, and recall@100 = 1.0000. BM25 is
the strongest observed profile. The generated questions frequently preserve
distinctive Portuguese terms, named entities, formulas, product names, places,
or technical vocabulary from the answer paragraph.

This split is therefore highly favorable to lexical retrieval. Even though the
documents are long, the query often contains enough rare surface evidence to
identify the correct article. For top-rank evaluation, any dense or hybrid
system must be compared against a very strong BM25 baseline.

### Dense Evaluation Profile

The dense `harrier_oss_v1_270m` candidate subset contains 500 candidates per
query and achieves nDCG@10 = 0.7667, hit@10 = 0.8298, and recall@100 = 0.9362.
Dense retrieval is useful and much stronger here than in some other MLDR
languages, but it remains clearly behind BM25.

The main difficulty is exact article selection. A dense model can understand
that a question concerns music theory, physics instrumentation, a city,
economics, or video-game history, but multiple long Portuguese articles can
share that broad meaning. The correct document is often determined by a local
paragraph-specific term.

### Reranking Hybrid Evaluation Profile

The `reranking_hybrid` candidate subset contains 100 candidates per query and
does not require rank-101 safeguard rows. It achieves nDCG@10 = 0.8565, hit@10
= 0.9362, and recall@100 = 1.0000. Hybrid retrieval matches BM25 on
recall@100, showing that it retains every positive in the top-100 pool, but it
does not match BM25's top-rank ordering.

This profile is useful for reranking experiments because the candidate pool has
complete positive coverage. The remaining problem is ranking: a reranker must
use the local paragraph evidence and exact Portuguese lexical anchors to move
the positive above semantically close alternatives.

### Metric Interpretation for Model Researchers

This task is single-positive: each query has exactly one relevant long
document. Hit@10 measures whether that document appears near the top. nDCG@10
is sensitive to its exact rank, and recall@100 measures whether the positive is
available for a downstream reranker.

The Portuguese split is a strong lexical-anchor benchmark. BM25 is near ceiling
for recall@100 and very high for nDCG@10, so improvements should be judged by
whether a model can preserve exact-match strength while adding semantic
robustness. Dense-only retrieval is not enough to characterize the task.

### Query and Relevance Type Tendencies

Queries are Portuguese paragraph-grounded questions about science, music,
municipal geography, technology, games, history, public administration, and
biography. They tend to include multi-word entities, domain-specific nouns, or
technical expressions from the source paragraph.

Relevant documents are long Portuguese articles. The answer-bearing paragraph
may be surrounded by broad background information, lists, historical sections,
or technical exposition. Good systems need both document-level coverage and
paragraph-level discrimination.

### Representative Failure Modes

Dense retrieval can return a long article in the right topic area but not the
one containing the answer paragraph. This can happen for music forms, physics
topics, municipalities, operating systems, game consoles, or historical figures
where several articles share similar semantics.

BM25 failures are rarer but can occur when related documents share the same
rare names, formulas, dates, or product terms. Hybrid retrieval can keep all
positives in the candidate pool but rank a related article above the correct
one, making span-aware reranking important.

### Training Data That May Help

Useful training data includes Portuguese long-document QA retrieval pairs,
Portuguese Wikipedia article retrieval, multilingual MLDR training data outside
this Nano split, and Portuguese hard negatives from related articles with
overlapping names, dates, formulas, institutions, or product vocabulary.

Synthetic data can help when it samples paragraphs from long Portuguese
encyclopedic articles, generates grounded Portuguese questions, and uses the
full article as the positive. Negatives should be long Portuguese articles in
the same topic area but without the answer-bearing paragraph.

### Model Improvement Notes

Dense retrievers should use chunked indexing, late interaction, paragraph-aware
pooling, or multi-vector representations to avoid losing local evidence in a
single full-document vector. Sparse systems should preserve Portuguese lexical
anchors, named entities, formulas, and inflected terms. Rerankers should be
trained against hard negatives that look lexically and semantically close.

For hybrid systems, `NanoMLDR / pt` is a high-recall reranking test. The current
`reranking_hybrid` candidate pool contains all positives in the top 100, so the
main opportunity is better top-rank ordering rather than broader retrieval
coverage.

## Example Data

Representative queries ask about formulas for solving a kinematic equation,
when Haydn, Mozart, and Beethoven used fugue, what is needed to adjust
brightness in a cathode-ray tube, how PR-16 connects Curiuva to other cities,
and how counterfeit games affected the Sega Saturn's popularity in Brazil.
Positive documents are Portuguese long articles containing the relevant
paragraph.

### Public Sources

- [M3-Embedding: Multi-Linguality, Multi-Functionality, Multi-Granularity Text Embeddings Through Self-Knowledge Distillation](https://arxiv.org/abs/2402.03216),
  2024.
- [M3-Embedding ACL Anthology version](https://aclanthology.org/2024.findings-acl.137/),
  2024.
- [Shitao/MLDR dataset card](https://huggingface.co/datasets/Shitao/MLDR).
- [hakari-bench/NanoMLDR](https://huggingface.co/datasets/hakari-bench/NanoMLDR),
  Nano benchmark dataset.

### Source Reference Table

| Title | Year | Type | URL |
| --- | ---: | --- | --- |
| M3-Embedding: Multi-Linguality, Multi-Functionality, Multi-Granularity Text Embeddings Through Self-Knowledge Distillation | 2024 | benchmark paper | https://arxiv.org/abs/2402.03216 |
| M3-Embedding ACL Anthology version | 2024 | paper | https://aclanthology.org/2024.findings-acl.137/ |
| MLDR: Multilingual Long-Document Retrieval dataset | 2024 | dataset card | https://huggingface.co/datasets/Shitao/MLDR |

### Representative Snippets

| Query pattern | Positive document pattern |
| --- | --- |
| A Portuguese question about formulas for a kinematic equation. | A long article about kinematics. |
| A question about use of fugue by classical composers. | A long article about fugue in music. |
| A question about brightness adjustment in a CRT instrument. | A long article about oscilloscopes. |
| A question about the importance of PR-16 for a municipality. | A long article about Curiuva. |
| A question about counterfeit games and console popularity in Brazil. | A long article about the Sega Saturn. |
