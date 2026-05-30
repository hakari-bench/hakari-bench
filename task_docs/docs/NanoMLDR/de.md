# NanoMLDR / de

## Overview

`NanoMLDR / de` is the German split of NanoMLDR, a multilingual long-document
retrieval benchmark derived from MLDR. German questions retrieve long German
documents, including clean encyclopedia articles and noisy web-style documents,
where the answer-bearing passage may be buried inside a much larger page. The
Nano split has 117 queries, 5,046 documents, and 117 positive qrel rows, with
exactly one positive document per query. Current diagnostics show BM25 as the
strongest top-rank profile, `reranking_hybrid` as the strongest recall profile,
and dense retrieval as substantially weaker on long German documents.

## Details

### What the Original Data Measures

MLDR was introduced with the M3-Embedding work as a multilingual long-document
retrieval benchmark. The dataset card describes a process in which long
documents are sampled, a paragraph is selected, and a specific question is
generated from that paragraph. The full document containing that paragraph is
the retrieval target.

For German, the source data includes Wikipedia and mC4-style web content. This
means the benchmark is not only clean encyclopedia retrieval. Some positives are
long noisy web pages, product pages, forum-like pages, or pages with navigation
and boilerplate. The task measures whether a retriever can identify the full
document that contains a local answer passage.

### Observed Data Profile

The Nano split contains 117 queries, 5,046 documents, and 117 positive qrel
rows. Every query has exactly one positive document. Queries average 81.46
characters, while documents average 12,343.20 characters. The document length
and source mixture dominate the retrieval behavior.

Observed questions ask about events in Lower Saxony, store design protection,
cleaning cloth properties, game previews, artificial intelligence effects, and
other paragraph-level facts embedded in long German pages. Positive documents
may contain substantial irrelevant surrounding text, advertisements, search
result lists, comments, or page scaffolding.

### BM25 Evaluation Profile

The dataset-provided BM25 candidate subset contains 500 candidates per query and
achieves nDCG@10 = 0.7138, hit@10 = 0.7863, and recall@100 = 0.9145. BM25 is
the strongest observed top-rank profile. Long German documents provide many
surface cues, including exact product names, event terms, legal phrases, game
titles, organizations, and web-page-specific wording.

BM25 benefits from the generated-question construction. When a question is
grounded in one paragraph, words from that paragraph often also appear in the
full page. Exact lexical overlap can therefore locate the positive document
even if the page is noisy or extremely long.

### Dense Evaluation Profile

The dense `harrier_oss_v1_270m` candidate subset contains 500 candidates per
query and achieves nDCG@10 = 0.4208, hit@10 = 0.5214, and recall@100 = 0.7521.
Dense retrieval is much weaker than BM25. A single dense representation has to
compress long German documents that may mix answer text, navigation, comments,
product listings, and unrelated boilerplate.

This makes the positive document hard to represent. The generated question may
match a small paragraph, but dense similarity can be dominated by the overall
page theme or noise. Dense retrieval can therefore find semantically related
pages while missing the exact long document containing the answer.

### Reranking Hybrid Evaluation Profile

The `reranking_hybrid` candidate subset contains mostly 100 candidates per
query, with eight queries using a rank-101 safeguard row. It achieves nDCG@10 =
0.5773, hit@10 = 0.6752, and recall@100 = 0.9316. Hybrid retrieval improves
coverage over BM25 and dense retrieval, but it does not match BM25's top-rank
nDCG@10 or hit@10.

This profile shows that hybrid search is most valuable as a candidate source.
BM25 supplies the strongest ranking signal for exact German long-document
matching, while dense retrieval adds some semantically related candidates that
increase recall. Downstream reranking must be careful not to discard the
lexical signal.

### Metric Interpretation for Model Researchers

This task is single-positive: each query has exactly one relevant long
document. Hit@10 measures whether the positive document appears near the top.
nDCG@10 is sensitive to the rank of that single document, and recall@100
measures whether it remains available for reranking.

The German MLDR pattern is a long-document retrieval warning. BM25 is strong
because exact terms survive in long documents, while dense retrieval struggles
when one vector must summarize noisy pages. Strong systems should consider
chunked indexing, paragraph-level retrieval, late interaction, and hybrid
reranking rather than relying on full-document dense embeddings alone.

### Query and Relevance Type Tendencies

Queries are paragraph-grounded German questions about events, legal rulings,
product attributes, game previews, social effects, technical details, and other
facts found inside long pages. The wording can be specific and natural, but the
positive document may be much broader or noisier than the answer paragraph.

Relevant documents are long German documents with article text, web boilerplate,
forum content, comments, product listings, or navigation. The task rewards exact
phrase preservation, robustness to noisy pages, and the ability to connect a
small answer passage to its containing document.

### Representative Failure Modes

Dense retrieval can miss positives when the answer paragraph is a small part of
a long page. Product pages, forum pages, and web pages with search-result or
navigation text can produce diluted embeddings. BM25 can fail when many pages
share the same product name, event phrase, or legal vocabulary, or when the
question paraphrases the paragraph rather than repeating its terms.

Hybrid retrieval can recover more positives but still rank a semantically broad
or lexically noisy page above the exact positive. Rerankers should inspect
paragraph-level evidence rather than scoring only the full page as one text.

### Training Data That May Help

Useful training data includes German long-document QA retrieval pairs, German
Wikipedia retrieval data, German mC4-style web retrieval data, and noisy
web-page hard negatives. Training should include long documents where the
answer is localized to one paragraph, plus negatives that share product,
historical, legal, or technical vocabulary.

Synthetic data can help when it includes both clean German encyclopedia articles
and noisy German web pages. Questions should target paragraph-level facts, while
positives remain the full containing document. Hard negatives should share topic
words or page genre without containing the answer passage.

### Model Improvement Notes

Dense retrievers should move beyond single-vector full-document encoding for
German MLDR. Chunked retrieval, paragraph-aware aggregation, late interaction,
or multi-vector document representations are likely better suited to the task.
Sparse systems should preserve exact names and phrases while reducing noise from
boilerplate and navigation.

For hybrid systems, `NanoMLDR / de` suggests using BM25 as a strong base
candidate generator and treating dense retrieval as a recall supplement.
Rerankers should validate against BM25, because the sparse baseline is the best
top-rank profile in the current diagnostics.

## Example Data

Representative queries ask which event takes place on Sunday in Lower Saxony,
why German store design is considered protectable, what properties a Mikronell
cleaning cloth has, what made an author want to try a game, or what effects
artificial intelligence may have on society. Positive documents are long German
pages containing the answer-bearing paragraph among substantial surrounding
content.

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
| A German question about an event in Lower Saxony. | A long page containing event or sports-club schedule information. |
| A question about why store design can be protected. | A legal or news-style page about Apple store design protection. |
| A question about properties of a cleaning cloth. | A product or search-results page containing the product description. |
| A question about why an author wanted to try a game. | A long game-preview page with the relevant paragraph. |
| A question about possible effects of artificial intelligence. | A long forum or web page containing the paragraph-grounded answer. |
