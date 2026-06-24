# NanoLongEmbed / NanoNeedle

## Overview

`NanoLongEmbed / NanoNeedle` is LongEmbed's synthetic needle-in-a-haystack
retrieval task. Queries are natural factual questions, and documents are long
base texts into which short answer-bearing facts have been inserted. The model
must retrieve the document containing the inserted fact, not merely the document
whose surrounding essay has a related topic. The Nano split has 98 queries, 800
documents, and one positive document per query. Documents average 35,246.12
characters. Current diagnostics show BM25 as the strongest top-10 ranker,
`reranking_hybrid` as the best recall@100 profile, and dense retrieval as
weaker but still useful for preserving some semantic fact-question matches.

## Details

### What the Original Data Measures

LongEmbed describes Needle-in-a-haystack Retrieval as a synthetic long-context
retrieval task. Unlike passkey-style retrieval, the query is a natural factual
question and the target information is an inserted fact sentence inside a much
longer document. The task is designed to test whether embedding models can
retain localized evidence after long-context encoding and pooling.

There is no separate standalone task paper confirmed for `NanoNeedle`; the
source benchmark is LongEmbed and its public dataset card. The task should be
read as a controlled diagnostic for long-document evidence retention rather
than as a naturally occurring web or QA corpus.

### Observed Data Profile

The Nano split contains 98 queries, 800 documents, and 98 positive qrel rows.
Every query has one positive, with no multi-positive queries. Queries average
58.99 characters. Documents average 35,246.12 characters.

Observed positives are built around a Paul Graham essay-style base document
with inserted facts about formulas, paintings, novels, geography, history, and
scientific facts. The relevant evidence is usually one sentence, while the
surrounding document is long and often topically unrelated to the question.

### BM25 Evaluation Profile

The dataset-provided BM25 candidate subset contains 500 candidates per query
and achieves nDCG@10 = 0.7207, hit@10 = 0.9592, and recall@100 = 0.9694. BM25
is the strongest observed top-10 profile. The inserted facts often contain
distinctive lexical terms from the query, such as a formula, title, name, or
place, making sparse matching highly effective.

The lower nDCG relative to hit@10 is informative. BM25 usually gets the
positive document into the first ten results, but not always at rank 1. Reused
base text, similar inserted fact styles, and common factual wording can make
precise ordering harder than simple detection.

### Dense Evaluation Profile

The dense `harrier_oss_v1_270m` candidate subset contains 500 candidates per
query and achieves nDCG@10 = 0.6099, hit@10 = 0.7857, and recall@100 = 0.9592.
Dense retrieval is meaningfully weaker than BM25 in early ranking, although its
recall@100 remains high. This reflects a long-context embedding challenge:
the inserted fact is a tiny span inside a long document, and a single vector can
lose that evidence during pooling.

Dense retrieval helps when the question paraphrases the inserted fact or when
semantic matching matters more than exact word overlap. But for this synthetic
task, preserving the literal inserted sentence is often more important than
representing the base essay's global meaning.

### Reranking Hybrid Evaluation Profile

The `reranking_hybrid` candidate subset contains 100 or 101 candidates per
query, with 1 safeguard positive row and a mean of 100.010204 candidates. It
achieves nDCG@10 = 0.6823, hit@10 = 0.8878, and recall@100 = 0.9898. Hybrid
retrieval improves over dense retrieval and gives the best top-100 positive
coverage, but it does not surpass BM25's top-10 ranking.

The hybrid profile shows complementarity. BM25 captures exact inserted terms,
while dense retrieval can contribute paraphrastic or semantic matches. For a
reranker, the hybrid pool is useful because it keeps almost every positive
available, but final ranking still needs strong evidence localization.

### Metric Interpretation for Model Researchers

This is a single-positive retrieval task. Hit@10 measures whether the document
with the inserted fact appears in the first ten results, nDCG@10 rewards ranking
it near the top, and recall@100 measures whether candidate generation keeps it
available for reranking.

The key diagnostic is not broad topical retrieval. `NanoNeedle` asks whether a
model can preserve a small fact inside a long document. The observed metrics
show that lexical matching is still very strong, dense retrieval loses some
localized evidence, and hybrid retrieval provides the best candidate coverage.

### Query and Relevance Type Tendencies

Queries are natural factual questions about formulas, authors, publication
dates, locations, definitions, creators, and comparisons. Relevant documents
are long base texts with the answer sentence inserted at some position. The
surrounding text can be unrelated to the question.

The task rewards models that retain local evidence regardless of document
position. It also tests robustness against base-document repetition and
distractor facts.

### Representative Failure Modes

BM25 can fail when several documents share similar inserted terms or when the
answer wording is too common. Dense retrieval can fail when the inserted fact is
washed out by the much longer base document. Hybrid retrieval can recover more
positives but still rank a document with related factual language above the
true positive.

Position sensitivity is another likely failure mode. If an encoder or pooling
strategy underweights text far from the beginning, facts inserted at later
depths may be missed.

### Training Data That May Help

Useful training data includes synthetic needle-in-context retrieval, long
document QA with inserted facts, evidence localization over essays or articles,
and position-robust factual retrieval examples. Training should vary base
document, insertion depth, answer type, and distractor facts.

Comparable evaluation should exclude Nano evaluation questions, inserted facts,
qrels, and positive documents.

### Model Improvement Notes

Dense retrievers can improve through chunk-aware or multi-vector
representations, position-robust pooling, and training objectives that require
retaining tiny evidence spans. Sparse systems already perform well because
inserted facts carry explicit words, but must handle repeated base text and
similar factual templates. Rerankers should inspect whether the candidate
contains the exact inserted answer sentence.

For hybrid systems, this task supports using BM25 as a strong evidence detector
and dense retrieval as a recall supplement.

## Example Data

| Query | Positive document |
| --- | --- |
| Who developed the laws of motion and when? [42 chars] | Aaron Swartz created a scraped feed of the essays page. November 2021(This essay is derived from a talk at the Cambridge Union. )When I was a kid, I'd have said there wasn't. My father told me so. Some people like some things, and other people like other things, and who's to say who's right?It seemed so obvious that there was no such thing as good taste that it was only through indirect evidence that I realized my father was wrong. And that's what I'm going to give you here: a proof by reductio ad absurdum. If we start from the premise that there's no such thing as good taste, we end up with conclusions that are obviously false, and therefore the premise must be wrong. We'd better start by saying what good taste is. There's a narrow sense in which it refers to aesthetic judgements and a broader one in which it refers to preferences of any kind. The strongest proof would be to show that taste exists in the narrowest sense, so I'm going to talk about taste in art. You have better taste t... [1,000 / 1,990 chars] |
| Who wrote the novel "The Grapes of Wrath" and when was it published? [68 chars] | Aaron Swartz created a scraped feed of the essays page. November 2021(This essay is derived from a talk at the Cambridge Union. )When I was a kid, I'd have said there wasn't. My father told me so. Some people like some things, and other people like other things, and who's to say who's right?It seemed so obvious that there was no such thing as good taste that it was only through indirect evidence that I realized my father was wrong. And that's what I'm going to give you here: a proof by reductio ad absurdum. If we start from the premise that there's no such thing as good taste, we end up with conclusions that are obviously false, and therefore the premise must be wrong. We'd better start by saying what good taste is. There's a narrow sense in which it refers to aesthetic judgements and a broader one in which it refers to preferences of any kind. The strongest proof would be to show that taste exists in the narrowest sense, so I'm going to talk about taste in art. You have better taste t... [1,000 / 72,045 chars] |
| What is the Panama Canal and what does it connect? [50 chars] | Aaron Swartz created a scraped feed of the essays page. November 2021(This essay is derived from a talk at the Cambridge Union. )When I was a kid, I'd have said there wasn't. My father told me so. Some people like some things, and other people like other things, and who's to say who's right?It seemed so obvious that there was no such thing as good taste that it was only through indirect evidence that I realized my father was wrong. The Panama Canal is a man-made waterway that connects the Atlantic and Pacific Oceans. And that's what I'm going to give you here: a proof by reductio ad absurdum. If we start from the premise that there's no such thing as good taste, we end up with conclusions that are obviously false, and therefore the premise must be wrong. We'd better start by saying what good taste is. There's a narrow sense in which it refers to aesthetic judgements and a broader one in which it refers to preferences of any kind. The strongest proof would be to show that taste exists i... [1,000 / 4,062 chars] |

### Public Sources

- [LongEmbed: Extending Embedding Models for Long Context Retrieval](https://arxiv.org/abs/2404.12096),
  2024.
- [dwzhu/LongEmbed](https://huggingface.co/datasets/dwzhu/LongEmbed), source
  dataset card.
- [hakari-bench/NanoLongEmbed](https://huggingface.co/datasets/hakari-bench/NanoLongEmbed),
  Nano benchmark dataset.

### Source Reference Table

| Title | Year | Type | URL |
| --- | ---: | --- | --- |
| LongEmbed: Extending Embedding Models for Long Context Retrieval | 2024 | arXiv paper | [https://arxiv.org/abs/2404.12096](https://arxiv.org/abs/2404.12096) |
| dwzhu/LongEmbed | 2024 | dataset card | [https://huggingface.co/datasets/dwzhu/LongEmbed](https://huggingface.co/datasets/dwzhu/LongEmbed) |

### Representative Snippets

| Query pattern | Positive document pattern |
| --- | --- |
| A question asking who developed the laws of motion and when. | A long essay-like base document with one inserted factual sentence about the laws of motion. |
| A question asking who wrote *The Grapes of Wrath* and when it was published. | A long base text containing an inserted sentence with the author and publication year. |
| A question asking what the Panama Canal is and what it connects. | A long document with an inserted sentence defining the canal and its connection. |
| A question asking for the area formula of a kite. | A long text containing the formula as a local inserted fact. |
| A question asking who wrote *One Hundred Years of Solitude* and when it was published. | A long document with an inserted sentence naming Gabriel Garcia Marquez and the publication date. |
