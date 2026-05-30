# NanoMLDR / ko

## Overview

`NanoMLDR / ko` is the Korean split of NanoMLDR, a multilingual long-document
retrieval benchmark derived from MLDR. Korean paragraph-grounded questions
retrieve full Korean articles, so the model must connect a local answer-bearing
paragraph to its complete document. The Nano split has 177 queries, 3,087
documents, and 177 positive qrel rows, with exactly one positive document per
query. Current diagnostics show BM25 as the strongest top-rank profile, dense
retrieval as much weaker, and `reranking_hybrid` as improving coverage beyond
BM25 while still below BM25 on nDCG@10.

## Details

### What the Original Data Measures

MLDR was introduced with the M3-Embedding work as a multilingual long-document
retrieval benchmark. The dataset card describes sampling long documents,
selecting a paragraph, and generating a specific question from that paragraph.
The retrieval target is the full article containing the answer-bearing
paragraph.

For Korean, this creates a document-scale retrieval task rather than a short
passage task. The question may focus on a narrow statement, character, event,
place, medical concept, or historical detail, while the indexed candidate is a
long Korean article.

### Observed Data Profile

The Nano split contains 177 queries, 3,087 documents, and 177 positive qrel
rows. Every query has exactly one positive document. Queries average 55.27
characters, while documents average 5,915.24 characters.

Observed examples include questions about fictional characters, Korean family
lineages, clinical trials, Novosibirsk daylight, voice actor roles,
superconductivity, fantasy novels, Netherlands history, and apartment history.
The positive documents are long Korean articles containing the paragraph that
generated the question.

### BM25 Evaluation Profile

The dataset-provided BM25 candidate subset contains 500 candidates per query and
achieves nDCG@10 = 0.6868, hit@10 = 0.7740, and recall@100 = 0.8870. BM25 is
the strongest observed top-rank profile. Korean questions often retain
distinctive names, transliterated terms, article titles, technical vocabulary,
or proper nouns from the source paragraph.

This lexical signal is valuable for long-document retrieval because a rare
entity or phrase can point to the correct full article. BM25 can still struggle
when Korean morphology, spacing, or shared names create competing matches, but
it remains the best observed ranker at the top of the list.

### Dense Evaluation Profile

The dense `harrier_oss_v1_270m` candidate subset contains 500 candidates per
query and achieves nDCG@10 = 0.4120, hit@10 = 0.5311, and recall@100 = 0.7797.
Dense retrieval captures broad embedding similarity but loses a large amount of
top-rank precision relative to BM25.

This is consistent with the long-document setting. A single dense vector for a
long Korean article can blur the local paragraph evidence. Articles about
related games, historical regions, scientific concepts, public figures, or
medical topics can be semantically close even when only one contains the exact
answer-bearing paragraph.

### Reranking Hybrid Evaluation Profile

The `reranking_hybrid` candidate subset contains mostly 100 candidates per
query, with 17 queries using a rank-101 safeguard row. It achieves nDCG@10 =
0.5925, hit@10 = 0.7345, and recall@100 = 0.9040. Hybrid retrieval improves
clearly over dense retrieval and slightly exceeds BM25 on recall@100, but BM25
still has stronger top-rank quality.

This profile suggests that hybrid search is useful as a candidate generator for
reranking: it recovers positives that BM25 misses while preserving many lexical
hits. The remaining gap in nDCG@10 means the reranker must learn when to trust
Korean lexical anchors over broad semantic similarity.

### Metric Interpretation for Model Researchers

This task is single-positive: each query has exactly one relevant long
document. Hit@10 measures whether that document appears near the top. nDCG@10
is sensitive to the exact rank of the positive, and recall@100 measures whether
the positive remains available to a downstream reranker.

The Korean profile is a strong test of lexical-entity preservation in a
long-document setting. Dense models should not be evaluated only by semantic
coverage; they must also separate the exact article from related Korean
documents that share entities, genres, or topical vocabulary.

### Query and Relevance Type Tendencies

Queries are Korean paragraph-grounded questions about fiction, genealogy,
medicine, geography, biography, science, history, entertainment, and social
topics. They often mention a specific named entity, role, event, method, place,
or object from the source paragraph.

Relevant documents are long Korean articles. The answer-bearing information may
be local, while the rest of the document introduces many unrelated lexical and
semantic signals. This makes paragraph-aware evidence especially important.

### Representative Failure Modes

Dense retrieval can return a thematically similar Korean article but miss the
one containing the generated-question paragraph. BM25 can fail when several
articles share a name, title, or technical term, or when Korean spacing and
morphology reduce exact-match reliability.

Hybrid retrieval can increase recall but still place a semantically related
negative above the positive. Rerankers should compare local evidence spans and
not rely only on article titles or global document embeddings.

### Training Data That May Help

Useful training data includes Korean long-document QA retrieval pairs, Korean
Wikipedia article retrieval, multilingual MLDR training data outside this Nano
split, and Korean hard negatives that share entities, genres, or technical
terminology. Training should include full-article positives selected from a
single answer-bearing paragraph.

Synthetic data can help when it samples paragraphs from long Korean
encyclopedic articles, generates grounded Korean questions, and uses the full
article as the positive. Negatives should be related Korean articles that share
names, categories, or topical labels but do not answer the question.

### Model Improvement Notes

Dense retrievers should consider chunked indexing, late interaction,
paragraph-aware pooling, or multi-vector document representations. Sparse
systems should preserve Korean lexical anchors while handling morphology and
spacing variation. Rerankers should be trained with same-entity and same-topic
long-document hard negatives.

For hybrid systems, `NanoMLDR / ko` is a useful reminder that better
recall@100 does not automatically mean better nDCG@10. The current
`reranking_hybrid` profile gives a strong reranking candidate pool, but top-rank
ordering still needs improvement.

## Example Data

Representative queries ask why a character does not recognize magical ability,
what role historical lineage members played, whether clinical-trial stages can
be optimized, how daylight changes in Novosibirsk, and what roles characters
play in a voice actor's works. Positive documents are Korean long articles
containing the relevant paragraph.

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
| A Korean question about a character's unrecognized magical ability. | A long article about a Korean-served online role-playing game or related fiction. |
| A question about historical lineage members and their contributions. | A long article about a Korean family lineage. |
| A question about optimizing or replacing clinical-trial stages. | A long article about clinical trials. |
| A question about seasonal daylight in Novosibirsk. | A long article about the Russian city. |
| A question about roles played by main characters in a work. | A long article about a Korean voice actor and credited roles. |
