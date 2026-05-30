# NanoMLDR / ru

## Overview

`NanoMLDR / ru` is the Russian split of NanoMLDR, a multilingual long-document
retrieval benchmark derived from MLDR. Russian paragraph-grounded questions
retrieve full Russian articles, where the answer-bearing paragraph may be a
small section inside a long document. The Nano split has 160 queries, 3,125
documents, and 160 positive qrel rows, with exactly one positive document per
query. Current diagnostics show BM25 as the strongest top-rank profile,
`reranking_hybrid` as matching BM25 recall@100, and dense retrieval as
substantially weaker for exact full-article selection.

## Details

### What the Original Data Measures

MLDR was introduced with the M3-Embedding work as a multilingual long-document
retrieval benchmark. The dataset card describes sampling long documents,
selecting a paragraph, and generating a specific question from that paragraph.
The retrieval target is the full article containing the answer-bearing
paragraph.

For Russian, this evaluates document-scale retrieval from detailed Russian
questions. A model must find the full article that contains the local evidence,
not just an article in the same broad historical, technical, literary, or
geographic topic area.

### Observed Data Profile

The Nano split contains 160 queries, 3,125 documents, and 160 positive qrel
rows. Every query has exactly one positive document. Queries average 92.89
characters, while documents average 14,163.52 characters.

Observed examples include questions about steam locomotive history, political
satire, time-zone boundaries, building wall types, poetry collections, city
history, geometry, literary motifs, Palestinian politics, and ancient Macedonian
history. The positive documents are long Russian articles containing the
paragraph that generated each question.

### BM25 Evaluation Profile

The dataset-provided BM25 candidate subset contains 500 candidates per query and
achieves nDCG@10 = 0.8664, hit@10 = 0.9125, and recall@100 = 0.9625. BM25 is
the strongest observed top-rank profile. Russian questions often preserve
distinctive names, quoted titles, dates, technical terms, or historically
specific phrases from the answer-bearing paragraph.

This gives lexical retrieval a strong advantage. Even in long documents, rare
surface forms can identify the correct article. Remaining BM25 failures are
likely to involve shared named entities, broad cultural topics, morphological
variation, or multiple Russian articles using similar specialist terminology.

### Dense Evaluation Profile

The dense `harrier_oss_v1_270m` candidate subset contains 500 candidates per
query and achieves nDCG@10 = 0.5992, hit@10 = 0.6750, and recall@100 = 0.8125.
Dense retrieval captures broad semantic similarity but is clearly weaker than
BM25 for this split.

The gap is consistent with long-document retrieval. A dense representation can
find articles about politics, architecture, poetry, transportation, geography,
or history, but it may not preserve the exact paragraph-level clue needed to
select the one positive article from related Russian documents.

### Reranking Hybrid Evaluation Profile

The `reranking_hybrid` candidate subset contains mostly 100 candidates per
query, with six queries using a rank-101 safeguard row. It achieves nDCG@10 =
0.6969, hit@10 = 0.7937, and recall@100 = 0.9625. Hybrid retrieval matches BM25
on recall@100 but does not match BM25 on top-rank ordering.

This makes the hybrid pool useful for reranking while showing that lexical
signals remain the dominant first-stage evidence. The candidate set keeps the
same positive coverage as BM25, but dense candidates and fusion can still place
semantically related negatives above the correct long article.

### Metric Interpretation for Model Researchers

This task is single-positive: each query has exactly one relevant long
document. Hit@10 measures whether that document appears near the top. nDCG@10
is sensitive to the positive document's exact rank, and recall@100 measures
whether it remains available for reranking.

The Russian split rewards exact lexical anchors in a long-document setting.
Dense retrieval should be judged against the strong BM25 baseline, and hybrid
systems should demonstrate that they preserve sparse precision rather than only
adding semantic breadth.

### Query and Relevance Type Tendencies

Queries are Russian paragraph-grounded questions about history, politics,
engineering, architecture, literature, cities, science, and cultural works.
They often contain a quoted title, date range, person name, technical term, or
institutional phrase that narrows the target article.

Relevant documents are full Russian articles. The answer-bearing paragraph may
be buried inside a long document, so successful retrieval requires both
article-level identification and paragraph-level evidence sensitivity.

### Representative Failure Modes

Dense retrieval can return a thematically related Russian article that lacks
the answer paragraph. This is likely for articles about related historical
figures, political concepts, buildings, literary movements, or transport
technology. BM25 can fail when several documents share the same rare term or
when Russian inflection and morphology reduce exact-match alignment.

Hybrid retrieval can preserve the positive in the candidate pool but rank a
nearby semantic neighbor above it. Rerankers should inspect local supporting
passages and not rely only on global document meaning.

### Training Data That May Help

Useful training data includes Russian long-document QA retrieval pairs, Russian
Wikipedia article retrieval, multilingual MLDR training data outside this Nano
split, and same-topic Russian hard negatives. Training should include full
articles as positives when only one paragraph answers the question.

Synthetic data can help when it samples paragraphs from long Russian
encyclopedic articles, generates grounded Russian questions, and uses the full
article as the positive. Negatives should share names, dates, concepts, or
topic labels but omit the relevant answer paragraph.

### Model Improvement Notes

Dense retrievers should use chunked indexing, late interaction, paragraph-aware
pooling, or multi-vector document representations to retain local evidence.
Sparse systems should preserve Russian lexical anchors while handling
morphology, quoted titles, and inflected named entities. Rerankers should be
trained with same-topic Russian hard negatives.

For hybrid systems, `NanoMLDR / ru` is a strong check on whether fusion keeps
BM25's high recall while improving rank order. The current `reranking_hybrid`
profile preserves recall but still leaves a substantial top-rank gap.

## Example Data

Representative queries ask who wrote an early textbook on locomotives, how
Averchenko depicted Trotsky and Lenin, why two-hour time-zone jumps appeared in
northern regions, which walls in a building are load-bearing, and which
editions were included in a poetry collection. Positive documents are Russian
long articles containing the relevant paragraph.

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
| A Russian question about the author of an early locomotive textbook. | A long article about the history of steam locomotives. |
| A question about satirical depictions of Trotsky and Lenin. | A long article about Arkady Averchenko. |
| A question about two-hour time-zone boundary changes. | A long article about time zones. |
| A question about load-bearing and non-load-bearing walls. | A long article about buildings. |
| A question about editions in a selected poetry collection. | A long article about David Samoilov. |
