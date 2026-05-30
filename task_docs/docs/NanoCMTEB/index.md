# NanoCMTEB

## Overview

NanoCMTEB is a compact Chinese retrieval group based on C-MTEB retrieval tasks.
It covers medical consultation retrieval, COVID policy and news retrieval,
general Chinese web passage retrieval, e-commerce product retrieval, translated
MS MARCO-style passage ranking, T2Ranking, and entertainment-video retrieval.
Most queries are short Chinese search intents, while documents range from
product or video titles to long web and policy passages.

The group is useful because it tests Chinese retrieval across several practical
domains rather than one homogeneous web-search setting. Short queries, mixed
scripts, product codes, translated MS MARCO artifacts, medical wording, and
multi-positive relevance sets all appear. BM25 measures the strength of Chinese
term and phrase overlap, dense retrieval tests intent matching across terse
queries and domain language, and `reranking_hybrid` shows where sparse and dense
signals recover complementary candidates.

## What This Group Measures

NanoCMTEB follows the C-MTEB view of Chinese embedding evaluation as a
multi-domain benchmark. Its retrieval tasks draw from Chinese web search,
translated MS MARCO, Multi-CPR-style domain retrieval, T2Ranking, and
CMedQA-style medical consultation retrieval.

The shared measurement target is Chinese first-stage retrieval under varied
query and document formats. A relevant document may be a doctor-style answer, a
government COVID passage, a product title, a video title, a translated web
answer passage, or a noisy search result. The group therefore rewards models
that handle short Chinese intent, mixed scripts, domain terms, and multiple
acceptable positives.

## Task Families

- **Medical retrieval:** `cmedqa` and `medical` connect patient or consumer
  health questions to medical-domain answers.
- **COVID and policy retrieval:** `covid` retrieves pandemic-related news,
  notices, and policy passages.
- **Chinese web retrieval:** `du`, `mmarco`, and `t2` cover DuReader-style,
  translated MS MARCO-style, and T2Ranking-style passage ranking.
- **E-commerce retrieval:** `ecom` matches short shopping queries to compact
  product-title-like documents.
- **Video retrieval:** `video` matches short entertainment-video queries to
  title or metadata-like records.

## Dataset Shape

NanoCMTEB contains 8 task pages, 1,600 queries, 80,000 split-local documents,
and 3,208 positive qrel rows. Each task has 200 queries and 10,000 documents.
The group averages about two positives per query, but `du` and `t2` have much
larger relevant sets than e-commerce, medical, and video title retrieval.

Queries are generally very short. `ecom`, `video`, `du`, `mmarco`, and `t2`
average around 7 to 11 characters, while `cmedqa` is longer because patient
questions carry more context. Documents vary sharply: product and video records
are short titles, medical answers are short passages, and T2 or COVID documents
can be much longer and noisier.

## Retrieval Behavior

### BM25 Profile

BM25 is strong on tasks where Chinese keywords, named entities, policy terms, or
search phrases appear directly in the relevant document. `covid`, `du`, `t2`,
`mmarco`, and `video` all show substantial sparse signal in the current
metadata. These tasks often preserve exact query terms, even when the document
is noisy or long.

BM25 is weaker on `cmedqa` and `medical`, where patient wording and doctor or
medical-answer wording can differ. It can also over-rank product or video items
that share brand, series, performer, or category words but do not match the
actual intent.

### Dense Profile

Dense retrieval is the best nDCG@10 profile for most NanoCMTEB tasks. It helps
bridge terse Chinese queries to answer passages and can connect lay health
language to more clinical wording. It is especially strong for `du`, `ecom`,
`medical`, `mmarco`, `t2`, and `video`.

The dense profile should still be read with exact-token caution. Product codes,
movie names, person names, policy names, and transliterated or mixed-script
tokens can be decisive. Dense improvements are most meaningful when they do not
lose these anchors.

### Reranking Hybrid Profile

`reranking_hybrid` is strongest when exact Chinese terms and dense intent
matching recover different positives. It is the best profile for `covid`, where
policy and news wording benefits from both term anchors and semantic context.
For other tasks it often sits between BM25 and dense, making it useful as a
candidate-pool view for reranking even when dense has the best top-rank score.

Because `du` and `t2` have many positives per query, hybrid candidate coverage
should be interpreted together with nDCG@10. Finding one positive is not enough;
the model must rank several relevant passages well.

## Task Summary

| Task | Retrieval shape | Language | Queries | Docs | Positives | BM25 nDCG@10 | Dense nDCG@10 | Reranking hybrid nDCG@10 | Best profile |
| --- | --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | --- |
| [cmedqa](cmedqa.md) | patient question to doctor answer | `zh` | 200 | 10,000 | 324 | 0.1667 | 0.3322 | 0.2595 | Dense |
| [covid](covid.md) | COVID query to policy or news passage | `zh` | 200 | 10,000 | 204 | 0.7888 | 0.7518 | 0.7834 | BM25 |
| [du](du.md) | Chinese web query to passage | `zh` | 200 | 10,000 | 889 | 0.7337 | 0.9286 | 0.8224 | Dense |
| [ecom](ecom.md) | shopping query to product title | `multilingual` | 200 | 10,000 | 200 | 0.5913 | 0.8052 | 0.7025 | Dense |
| [medical](medical.md) | health query to medical answer | `zh` | 200 | 10,000 | 200 | 0.3582 | 0.5691 | 0.4699 | Dense |
| [mmarco](mmarco.md) | translated MS MARCO query to passage | `zh` | 200 | 10,000 | 212 | 0.6795 | 0.8859 | 0.7984 | Dense |
| [t2](t2.md) | Chinese search query to noisy web passage | `zh` | 200 | 10,000 | 979 | 0.7944 | 0.9245 | 0.8604 | Dense |
| [video](video.md) | video search query to title or metadata | `zh` | 200 | 10,000 | 200 | 0.6897 | 0.8629 | 0.8103 | Dense |

## Interpretation Notes for Model Researchers

NanoCMTEB is useful for separating Chinese token and phrase matching from
semantic intent matching. BM25-heavy tasks show that exact Chinese terms and
named entities remain powerful. Dense-heavy tasks show where an embedding model
captures user intent, paraphrase, or domain wording beyond exact overlap.

The group should also be read by document format. Product and video retrieval
are title-heavy; medical and CMedQA are answer-heavy; T2 and COVID include
longer passages; `du` and `mmarco` are closer to web QA retrieval. A model that
does well on one format may not transfer to another.

## Training and Leakage Notes

Useful training data includes Chinese web-search relevance judgments,
multi-positive passage ranking, CMedQA-style consultation pairs, Chinese
medical QA, COVID and policy retrieval data, product-search logs, video-search
title matching, and translated MS MARCO pairs with overlap removed. For `du` and
`t2`, training should preserve multi-positive labels.

Exclude NanoCMTEB evaluation queries, qrels, positives, product titles, video
titles, consultation threads, and translated MS MARCO evaluation rows. Synthetic
data should keep short Chinese query style and include hard negatives that share
keywords but fail the true intent.

## Public Sources

- [C-Pack: Packaged Resources To Advance General Chinese Embedding](https://arxiv.org/abs/2309.07597), 2023.
- [C-MTEB benchmark](https://github.com/FlagOpen/FlagEmbedding/tree/master/C_MTEB).
- [MTEB benchmark](https://github.com/embeddings-benchmark/mteb).

### Source Reference Table

| Source | Year | Type | URL |
| --- | ---: | --- | --- |
| C-Pack: Packaged Resources To Advance General Chinese Embedding | 2023 | paper | https://arxiv.org/abs/2309.07597 |
| C-MTEB benchmark |  | project | https://github.com/FlagOpen/FlagEmbedding/tree/master/C_MTEB |
| MTEB benchmark |  | project | https://github.com/embeddings-benchmark/mteb |
