# NanoMLDR / zh

## Overview

`NanoMLDR / zh` is the Chinese split of NanoMLDR, a multilingual long-document
retrieval benchmark derived from MLDR. Chinese paragraph-grounded questions
retrieve full Chinese articles from Wikipedia and Wudao-style sources. The Nano
split has 200 queries, 7,877 documents, and 200 positive qrel rows, with
exactly one positive document per query. Current diagnostics show BM25 as much
stronger than dense retrieval, while `reranking_hybrid` recovers nearly the same
recall@100 as BM25 but remains well below BM25 for top-rank quality.

## Details

### What the Original Data Measures

MLDR was introduced with the M3-Embedding work as a multilingual long-document
retrieval benchmark. The dataset card describes sampling long documents,
selecting a paragraph, and generating a specific question from that paragraph.
The Chinese split is described as sourced from Wikipedia and Wudao-style
articles.

The retrieval target is the full Chinese article containing the answer-bearing
paragraph. The query is short relative to the document, so the model must use a
small amount of paragraph-derived evidence to identify a long article.

### Observed Data Profile

The Nano split contains 200 queries, 7,877 documents, and 200 positive qrel
rows. Every query has exactly one positive document. Queries average 20.68
characters, while documents average 12,307.31 characters.

Observed examples include questions about water-resource regulations, central
theory concepts, health exercises, zodiac compatibility, the Gongsun family,
web fiction, campus romance, historical geography, cooking recipes, and
pre-modern biography. The positive documents are long Chinese articles
containing the paragraph that generated the query.

### BM25 Evaluation Profile

The dataset-provided BM25 candidate subset contains 500 candidates per query and
achieves nDCG@10 = 0.7030, hit@10 = 0.7950, and recall@100 = 0.9000. BM25 is
the strongest observed top-rank profile. Short Chinese questions often retain
distinctive names, titles, topic phrases, or domain terms that can anchor the
correct article.

This is a strong lexical signal, especially when the query includes a rare
entity or exact phrase. The difficulty is that Chinese questions are short and
documents are long, so many articles can share overlapping titles, genre terms,
or broad topic vocabulary.

### Dense Evaluation Profile

The dense `harrier_oss_v1_270m` candidate subset contains 500 candidates per
query and achieves nDCG@10 = 0.3392, hit@10 = 0.4450, and recall@100 = 0.6300.
Dense retrieval is much weaker than BM25 on this split.

This gap suggests that broad embedding similarity is not enough for short-query
Chinese long-document retrieval. A dense model may retrieve articles about the
same genre, historical period, regulation, health topic, or cultural concept
while missing the exact paragraph-containing document.

### Reranking Hybrid Evaluation Profile

The `reranking_hybrid` candidate subset contains mostly 100 candidates per
query, with 21 queries using a rank-101 safeguard row. It achieves nDCG@10 =
0.4933, hit@10 = 0.6250, and recall@100 = 0.8950. Hybrid retrieval improves
substantially over dense retrieval and nearly matches BM25 recall@100, but it
still trails BM25 by a large margin at the top ranks.

This makes `reranking_hybrid` useful as a candidate pool for reranking, not as
a final ranking replacement for BM25. It keeps most positives available, but
the rank order still needs strong lexical and paragraph-aware evidence.

### Metric Interpretation for Model Researchers

This task is single-positive: each query has exactly one relevant long
document. Hit@10 measures whether that document appears near the top. nDCG@10
is sensitive to the exact rank of the positive, and recall@100 measures whether
the positive remains available to a downstream reranker.

The Chinese split is a short-query, long-document task with strong lexical
anchors. Dense retrieval should be interpreted against BM25, because BM25
captures exact names and phrases that appear to be central to the task. Hybrid
systems should focus on converting BM25-like coverage into better top-rank
ordering.

### Query and Relevance Type Tendencies

Queries are short Chinese paragraph-grounded questions about regulation,
finance-like theory, health, astrology, biography, fiction, geography, recipes,
history, and cultural topics. They often contain a compact title, person name,
concept, or phrase that identifies the source paragraph.

Relevant documents are long Chinese articles from Wikipedia or Wudao-style
sources. The answer-bearing paragraph may be surrounded by unrelated sections,
lists, or copied web-style context. Good retrieval needs exact phrase matching
and enough semantic robustness to handle short paraphrases.

### Representative Failure Modes

Dense retrieval can return a topically close Chinese article that lacks the
answer paragraph. This is likely when many documents share genre labels,
historical names, health terminology, or regulatory vocabulary. BM25 can fail
when short queries contain common terms or when several long articles share the
same title-like phrase.

Hybrid retrieval can preserve the positive in the candidate pool while ranking
a lexically or semantically adjacent article above it. Rerankers should inspect
the answer-bearing paragraph rather than relying only on the article title or a
global document vector.

### Training Data That May Help

Useful training data includes Chinese long-document QA retrieval pairs, Chinese
Wikipedia and Wudao article retrieval, multilingual MLDR training data outside
this Nano split, and title-sharing Chinese hard negatives. Training should
include short questions whose full-article positive is determined by one local
paragraph.

Synthetic data can help when it samples paragraphs from long Chinese
Wikipedia-like or Wudao-style articles, generates short grounded Chinese
questions, and uses the full article as the positive. Negatives should share
named entities, titles, genre terms, or topic labels while omitting the answer
paragraph.

### Model Improvement Notes

Dense retrievers should consider chunked indexing, late interaction,
paragraph-aware pooling, or multi-vector document representations. Sparse
systems should preserve Chinese lexical anchors and robust segmentation for
short questions. Rerankers should be trained on title-sharing and same-topic
Chinese hard negatives.

For hybrid systems, `NanoMLDR / zh` is a test of whether dense candidates can
supplement BM25 without degrading lexical precision. The current
`reranking_hybrid` profile nearly matches BM25 recall but needs better
top-rank ordering.

## Example Data

Representative queries ask about water-resource management measures in a
regulation, the core concept of a central theory, how a health exercise uses
acupoints and meridians, how Gemini and Pisces personalities affect a
relationship, and when the Gongsun clan first appeared. Positive documents are
Chinese long articles containing the relevant paragraph.

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
| A Chinese question about measures in a water-resource regulation. | A long article about a provincial drought-resistance regulation. |
| A question about the core concept of a central theory. | A long Chinese article about central expansion concepts. |
| A question about health exercises, acupoints, and meridians. | A long Chinese article about health preservation. |
| A question about Gemini and Pisces relationship traits. | A long article about water-sign astrology. |
| A question about the first appearance of the Gongsun clan. | A long article about a late Han figure. |
