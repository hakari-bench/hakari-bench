# NanoMLDR

## Overview

NanoMLDR is the compact Nano set for MLDR, a multilingual long-document
retrieval benchmark. It covers 13 monolingual retrieval splits: Arabic, German,
English, Spanish, French, Hindi, Italian, Japanese, Korean, Portuguese,
Russian, Thai, and Chinese. Each query is a question generated from a paragraph
inside a long article, while the positive document is the full article rather
than the short answer-bearing paragraph.

The group is useful because it isolates a difficult document-level retrieval
problem. The query may point to one small region of a very long same-language
document. A successful retriever must preserve language coverage, exact entity
and phrase anchors, and enough long-document representation to select the
whole source article. BM25 is the dominant profile for most languages in the
current metadata, dense retrieval is weaker on long-document compression, and
`reranking_hybrid` is useful where sparse and dense candidates recover
different long documents.

## What This Group Measures

[M3-Embedding: Multi-Linguality, Multi-Functionality, Multi-Granularity Text Embeddings Through Self-Knowledge Distillation](https://arxiv.org/abs/2402.03216)
describes the MLDR long-document setting. The MLDR dataset construction samples
long documents from multilingual sources, selects a paragraph, and generates a
question from that paragraph. The retrieval target remains the full document.

NanoMLDR therefore measures monolingual long-document retrieval, not short
passage retrieval and not cross-lingual transfer. The answer-bearing evidence
may be a small part of the document, and the document itself may be a clean
Wikipedia article, a noisy mC4 page, or a Wudao-style Chinese text.

## Task Families

- **Wikipedia-like long-document retrieval:** many language splits retrieve
  long encyclopedia-style articles from generated questions.
- **Noisy web long-document retrieval:** German, Spanish, Thai, and Chinese can
  include noisier web or mixed-source documents.
- **Script-diverse monolingual retrieval:** Arabic, Hindi, Japanese, Korean,
  Thai, and Chinese test long-document retrieval under different segmentation
  and script conditions.
- **Single-positive article selection:** every split is single-positive, so the
  key question is whether the full source document is ranked near the top.

## Dataset Shape

NanoMLDR contains 13 task pages, 2,089 queries, 55,585 split-local documents,
and 2,089 positive qrel rows. Query counts vary by language, from 117 German
queries to 200 English and Chinese queries. Every observed query has one
positive full document.

Documents are long. English averages nearly 28,000 characters per document,
while many European and Indic-language splits average around 12,000 to 15,000
characters. Japanese, Korean, and Thai have shorter character counts but are
still long-document retrieval tasks. The group should be interpreted as
document-level retrieval under multilingual source and noise variation.

## Retrieval Behavior

### BM25 Profile

BM25 is the best profile for nearly every NanoMLDR language in the current
metadata. Portuguese, Spanish, French, Italian, and Russian are especially
strong, suggesting that generated questions often preserve rare entities,
phrases, dates, or topical terms from the source article. BM25 is also strong
for Arabic, German, English, Japanese, Korean, and Chinese relative to dense
retrieval.

Thai and Hindi are harder. Thai includes noisier web documents and weaker
lexical anchoring. Hindi is the main split where hybrid beats BM25, suggesting
that sparse and dense retrieval recover complementary signals.

### Dense Profile

Dense retrieval is generally weaker than BM25 on NanoMLDR. The likely issue is
long-document compression: a single embedding must represent an entire article
while the query is grounded in one paragraph. Important rare terms can be
diluted by the rest of the document.

Dense scores are still diagnostic. A model that improves dense retrieval here
without losing BM25-like exact anchors is likely improving long-document
representation rather than only short-passage semantics.

### Reranking Hybrid Profile

`reranking_hybrid` usually sits between BM25 and dense. It helps when BM25
captures exact terms and dense retrieval captures broader semantic relation.
Hindi is the clearest hybrid-led language in the current metadata; several
other languages have hybrid scores that are meaningfully above dense but below
BM25.

For reranker experiments, hybrid can be a safer candidate pool than dense alone
because it preserves sparse long-document anchors. This matters when the full
document is long and only a small region answers the question.

## Language Summary

| Language | Task | Queries | Docs | BM25 nDCG@10 | Dense nDCG@10 | Reranking hybrid nDCG@10 | Best profile |
| --- | --- | ---: | ---: | ---: | ---: | ---: | --- |
| Arabic | [ar](ar.md) | 150 | 4,766 | 0.7604 | 0.4443 | 0.6181 | BM25 |
| German | [de](de.md) | 117 | 5,046 | 0.7138 | 0.4208 | 0.5773 | BM25 |
| English | [en](en.md) | 200 | 10,000 | 0.7254 | 0.4611 | 0.5916 | BM25 |
| Spanish | [es](es.md) | 176 | 3,312 | 0.9439 | 0.7844 | 0.8580 | BM25 |
| French | [fr](fr.md) | 152 | 3,059 | 0.9125 | 0.7706 | 0.8421 | BM25 |
| Hindi | [hi](hi.md) | 159 | 2,858 | 0.3184 | 0.3192 | 0.3883 | Reranking hybrid |
| Italian | [it](it.md) | 158 | 3,116 | 0.8884 | 0.6832 | 0.7807 | BM25 |
| Japanese | [ja](ja.md) | 148 | 3,112 | 0.7589 | 0.5014 | 0.6452 | BM25 |
| Korean | [ko](ko.md) | 177 | 3,087 | 0.6868 | 0.4120 | 0.5925 | BM25 |
| Portuguese | [pt](pt.md) | 141 | 3,028 | 0.9503 | 0.7667 | 0.8565 | BM25 |
| Russian | [ru](ru.md) | 160 | 3,125 | 0.8664 | 0.5992 | 0.6969 | BM25 |
| Thai | [th](th.md) | 151 | 3,199 | 0.3873 | 0.2671 | 0.3469 | BM25 |
| Chinese | [zh](zh.md) | 200 | 7,877 | 0.7030 | 0.3392 | 0.4933 | BM25 |

## Interpretation Notes for Model Researchers

NanoMLDR is a long-document retrieval benchmark first and a multilingual
benchmark second. Strong results mean the model can identify a full document
from a short question grounded in one paragraph. Dense models should not be
judged only by passage-retrieval performance; this group tests whether their
representations survive long-document aggregation.

The BM25 dominance is meaningful. It shows that exact rare terms and entities
remain powerful when questions are generated from source paragraphs. Dense or
hybrid improvements are most interesting in languages where BM25 is weak, such
as Hindi and Thai, or where noisy web documents make exact matching less stable.

## Training and Leakage Notes

Useful training data includes MLDR-style paragraph-grounded question/full
article pairs, multilingual long-document QA, Wikipedia article retrieval,
mC4/Wudao web-document retrieval, and hard negatives with overlapping entities,
dates, locations, or template language. Training should preserve full-document
targets rather than converting all examples to short passage retrieval.

Exclude NanoMLDR evaluation queries, positives, qrels, and source documents. If
using public MLDR data, audit train/dev/test boundaries and article overlap
before mixing examples into training.

## Public Sources

- [M3-Embedding: Multi-Linguality, Multi-Functionality, Multi-Granularity Text Embeddings Through Self-Knowledge Distillation](https://arxiv.org/abs/2402.03216), 2024.
- [MLDR dataset](https://huggingface.co/datasets/Shitao/MLDR).

### Source Reference Table

| Source | Year | Type | URL |
| --- | ---: | --- | --- |
| M3-Embedding: Multi-Linguality, Multi-Functionality, Multi-Granularity Text Embeddings Through Self-Knowledge Distillation | 2024 | paper | https://arxiv.org/abs/2402.03216 |
| MLDR dataset |  | dataset | https://huggingface.co/datasets/Shitao/MLDR |
