# NanoMLDR / th

## Overview

`NanoMLDR / th` is the Thai split of NanoMLDR, a multilingual long-document
retrieval benchmark derived from MLDR. Unlike many MLDR language splits, the
Thai data is described as mC4-style web data rather than clean
Wikipedia-sourced articles. The Nano split has 151 queries, 3,199 documents,
and 151 positive qrel rows, with exactly one positive document per query.
Current diagnostics show `reranking_hybrid` as the strongest recall@100
profile, BM25 as the strongest nDCG@10 profile, and dense retrieval as weaker
than both in this noisy Thai web setting.

## Details

### What the Original Data Measures

MLDR was introduced with the M3-Embedding work as a multilingual long-document
retrieval benchmark. The dataset card describes sampling long documents,
selecting a paragraph, and generating a specific question from that paragraph.
For Thai, the source is mC4-style web text, which makes the task different from
the cleaner encyclopedia-like splits.

The retrieval target is a full Thai web document that contains the
answer-bearing paragraph. Models must handle noisy pages, boilerplate,
advertising-like text, mixed scripts, and pages whose topical signal is less
controlled than Wikipedia articles.

### Observed Data Profile

The Nano split contains 151 queries, 3,199 documents, and 151 positive qrel
rows. Every query has exactly one positive document. Queries average 85.25
characters, while documents average 4,994.82 characters.

Observed examples include questions about online slot games, social ideals
around fathers and labor, corporate governance, hotels near Balaclava, Bitcoin
Core folders, casino pages, lodging pages, shopping promotions, fiction pages,
and other Thai web text with boilerplate and mixed-language fragments.

### BM25 Evaluation Profile

The dataset-provided BM25 candidate subset contains 500 candidates per query and
achieves nDCG@10 = 0.3873, hit@10 = 0.4636, and recall@100 = 0.7152. BM25 has
the best nDCG@10 among the three provided profiles, but the absolute score is
low compared with most encyclopedia-based MLDR splits.

This indicates that Thai lexical matching is helpful but fragile. Query terms
may appear in noisy boilerplate, repeated templates, product text, or mixed
script fragments. Thai word segmentation and web-page noise also make exact
term-frequency evidence less reliable than in cleaner article collections.

### Dense Evaluation Profile

The dense `harrier_oss_v1_270m` candidate subset contains 500 candidates per
query and achieves nDCG@10 = 0.2671, hit@10 = 0.3642, and recall@100 = 0.6954.
Dense retrieval is weaker than BM25 at the top ranks and slightly lower in
recall@100.

The profile suggests that embedding similarity is also challenged by the Thai
web source. Pages may combine unrelated boilerplate, promotions, navigation,
and copied fragments. A dense document representation can match broad topical
or commercial context while missing the specific paragraph that generated the
question.

### Reranking Hybrid Evaluation Profile

The `reranking_hybrid` candidate subset contains mostly 100 candidates per
query, with 35 queries using a rank-101 safeguard row. It achieves nDCG@10 =
0.3469, hit@10 = 0.4437, and recall@100 = 0.7682. Hybrid retrieval has the best
recall@100 and nearly reaches BM25 hit@10, but it remains below BM25 on
nDCG@10.

This is a different pattern from splits where BM25 dominates every metric. The
hybrid pool finds additional positives that BM25 misses, which is valuable for
reranking. The tradeoff is rank order: noisy dense or lexical neighbors can
push the single positive lower than BM25 would.

### Metric Interpretation for Model Researchers

This task is single-positive: each query has exactly one relevant long
document. Hit@10 measures whether that document appears near the top. nDCG@10
is sensitive to the positive document's exact rank, and recall@100 measures
whether it remains available for reranking.

The Thai split should be treated as a noisy-web long-document retrieval task,
not only as a Thai-language encyclopedia benchmark. It tests robustness to
boilerplate, mixed scripts, repeated templates, and weakly controlled document
topics. Recall and top-rank precision can move in different directions.

### Query and Relevance Type Tendencies

Queries are Thai paragraph-grounded questions about entertainment, commercial
web pages, lodging, corporate governance, technology, social commentary, and
other web topics. They can contain long question wording, fragments of page
language, or terms shared by many templated pages.

Relevant documents are full Thai web documents containing the answer paragraph.
They may include unrelated navigation, advertisements, product lists, dates,
and copied text. Good retrieval needs both Thai text handling and web-noise
filtering.

### Representative Failure Modes

BM25 can match boilerplate or repeated keywords instead of the paragraph that
answers the query. Dense retrieval can retrieve a page with similar commercial
or topical context but not the specific answer-bearing content. Both methods
can be confused by mixed scripts, duplicated page templates, and pages with
thin original text.

Hybrid retrieval improves coverage but can rank noisy near-duplicates or
template-sharing negatives above the positive. Rerankers should identify the
actual answer paragraph and discount repeated page furniture.

### Training Data That May Help

Useful training data includes Thai noisy-web long-document QA retrieval pairs,
Thai mC4 retrieval data, multilingual MLDR training data outside this Nano
split, and Thai web hard negatives that share boilerplate, product terms,
casino language, travel templates, or entertainment names.

Synthetic data should include noisy Thai web documents, not only clean
encyclopedic articles. Questions should be generated from a specific paragraph,
while hard negatives should share web templates or keywords without answering
the question.

### Model Improvement Notes

Dense retrievers should consider chunked indexing, paragraph-aware pooling, and
noise-aware document representations. Sparse systems need robust Thai
segmentation and should reduce the influence of repeated boilerplate. Rerankers
should be trained to locate answer-bearing spans inside noisy pages.

For hybrid systems, `NanoMLDR / th` is especially useful because
`reranking_hybrid` improves recall@100 over both BM25 and dense retrieval while
not winning nDCG@10. It is a candidate-generation benchmark where better
reranking could convert extra coverage into top-rank gains.

## Example Data

Representative queries ask why online slot games are popular, why an idealized
hard-working father is treated as socialization, what should be considered when
re-electing directors, what amenities make hotels near Balaclava attractive,
and how to address deletion of Bitcoin Core block-folder data. Positive
documents are noisy Thai web documents containing the relevant paragraph.

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
| A Thai question about why online slot games are popular. | A noisy Thai web page with gaming and casino-related text. |
| A question about social ideals and hard-working fathers. | A Thai web article discussing Korean entertainment and society. |
| A question about board re-election and corporate oversight. | A Thai corporate-governance web page. |
| A question about hotel amenities near Balaclava. | A Thai travel or lodging web page. |
| A question about deleting Bitcoin Core block-folder data. | A noisy Thai technology or cryptocurrency page. |
