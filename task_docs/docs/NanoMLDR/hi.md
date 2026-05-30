# NanoMLDR / hi

## Overview

`NanoMLDR / hi` is the Hindi split of NanoMLDR, a multilingual long-document
retrieval benchmark derived from MLDR. Hindi paragraph-grounded questions
retrieve full Hindi articles, where the answer-bearing passage may be buried
inside a long document. The Nano split has 159 queries, 2,858 documents, and
159 positive qrel rows, with exactly one positive document per query. Current
diagnostics show both BM25 and dense retrieval as weak and nearly tied, while
`reranking_hybrid` is the strongest profile across nDCG@10, hit@10, and
recall@100.

## Details

### What the Original Data Measures

MLDR was introduced with the M3-Embedding work as a multilingual long-document
retrieval benchmark. The dataset card describes sampling long documents,
selecting a paragraph, and generating a specific question from that paragraph.
The full document containing the answer-bearing paragraph is the retrieval
target.

For Hindi, this means the task measures long-document retrieval rather than
short-passage search. A model must connect a Devanagari question to a full
Hindi article whose relevant answer evidence may occupy only a small section.

### Observed Data Profile

The Nano split contains 159 queries, 2,858 documents, and 159 positive qrel
rows. Every query has exactly one positive document. Queries average 79.18
characters, while documents average 11,900.81 characters.

Observed examples include questions about railway-station districts,
constitutional schedules, Hindi font support on mobile devices, kidney tissue,
post-1947 cultural pilgrimage development, banking, biographies, universities,
anatomy, and public figures. The positive documents are long Hindi articles
that contain the answer-bearing paragraph among broad background material.

### BM25 Evaluation Profile

The dataset-provided BM25 candidate subset contains 500 candidates per query and
achieves nDCG@10 = 0.3184, hit@10 = 0.4277, and recall@100 = 0.6604. BM25 is
weak on this split. It can retrieve positives when exact Hindi names,
institutions, legal terms, or technical phrases match, but many questions use
general wording or refer to a paragraph that is not strongly represented by the
article title.

Long Hindi documents also contain many competing terms. Exact lexical overlap
can point to related articles rather than the full article containing the
answer paragraph, especially for constitutional, geographic, medical, or
cultural topics.

### Dense Evaluation Profile

The dense `harrier_oss_v1_270m` candidate subset contains 500 candidates per
query and achieves nDCG@10 = 0.3192, hit@10 = 0.4151, and recall@100 = 0.6604.
Dense retrieval is nearly tied with BM25 by nDCG@10 and recall@100, but slightly
lower by hit@10. This indicates that a single dense representation is also not
enough for Hindi long-document matching here.

The main issue is granularity. A full article embedding must summarize a long
document, while the question may target one paragraph about a schedule, device
support, anatomy detail, or historical development. The relevant local evidence
can be diluted by the rest of the article.

### Reranking Hybrid Evaluation Profile

The `reranking_hybrid` candidate subset contains mostly 100 candidates per
query, with 35 queries using a rank-101 safeguard row. It achieves nDCG@10 =
0.3883, hit@10 = 0.5220, and recall@100 = 0.7799. Hybrid retrieval is the best
observed profile, although absolute scores remain modest.

This split shows that Hindi MLDR benefits from combining lexical and semantic
signals, but also that both signals are individually weak. BM25 contributes
exact Devanagari anchors, while dense retrieval contributes broad semantic
matching. The hybrid candidate set retains more positives for reranking than
either method alone.

### Metric Interpretation for Model Researchers

This task is single-positive: each query has exactly one relevant long
document. Hit@10 measures whether that document appears near the top. nDCG@10
is sensitive to the rank of the single positive, and recall@100 measures whether
it remains available for reranking.

The Hindi MLDR profile is difficult for both sparse and dense retrieval. Unlike
Spanish or French MLDR, lexical overlap does not dominate; unlike many short
passage tasks, dense retrieval does not solve the problem either. Researchers
should consider chunk-level indexing, late interaction, and paragraph-aware
document aggregation.

### Query and Relevance Type Tendencies

Queries are Hindi paragraph-grounded questions about locations, constitutional
rules, mobile-device language support, anatomy, culture, biographies,
institutions, and article-specific factual details. Some contain strong entity
names, while others ask with broad descriptive wording.

Relevant documents are long Hindi articles with title context and answer-bearing
paragraphs. The task rewards Devanagari handling, exact entity matching,
paragraph-to-document linking, and robust retrieval when the title is broader
than the question.

### Representative Failure Modes

BM25 can retrieve related Hindi articles with shared legal, geographic,
technical, or cultural terms while missing the positive document. Dense
retrieval can select a broad semantically related article whose overall topic is
close but whose text lacks the answer paragraph. Both methods struggle when the
question refers to a small local detail inside a long article.

Hybrid retrieval improves recall but still leaves many positives outside the top
ranks. A reranker should inspect chunks or paragraphs and not rely only on a
single full-document score.

### Training Data That May Help

Useful training data includes Hindi long-document QA retrieval pairs, Hindi
Wikipedia article retrieval, multilingual MLDR training data outside this Nano
split, and entity-sharing Hindi hard negatives. Training should include long
Hindi documents where relevance is determined by one paragraph.

Synthetic data can help when it samples a paragraph from a long Hindi
encyclopedic article, generates a grounded Hindi question, and uses the full
article as the positive document. Hard negatives should share entities,
professions, institutions, legal terms, or places without containing the answer
paragraph.

### Model Improvement Notes

Dense retrievers should move beyond single-vector full-document encoding for
Hindi MLDR. Sparse systems need better Hindi tokenization, normalization, and
weighting for Devanagari terms, but lexical matching alone is insufficient.
Hybrid and reranking systems should use paragraph-aware evidence signals.

For hybrid systems, `NanoMLDR / hi` is a case where combining BM25 and dense
retrieval helps, but the next improvement requires better long-document
representation rather than simple score fusion.

## Example Data

Representative queries ask which district Medta Road railway station is in,
what salary and allowances apply to legislative council officers, whether Hindi
fonts are available on a phone, what kidney tissues need to remain alive, or
whether cultural pilgrimage development changed after 1947. Positive documents
are long Hindi articles containing the relevant answer paragraph.

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
| A Hindi question asking which district a railway station is in. | A long article about Nagaur or a related location. |
| A constitutional question about salary and allowances. | A long article about the Seventh Schedule or constitutional provisions. |
| A question about Hindi font availability on phones. | A long article about Hindi support on mobile devices. |
| A question asking for more information about kidney tissue. | A long article about the kidney. |
| A question about cultural pilgrimage development after 1947. | A long article about Mathura or cultural pilgrimage context. |
