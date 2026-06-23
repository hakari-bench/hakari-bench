# MNanoBEIR / NanoBEIR-sr / NanoMSMARCO

## Overview

NanoBEIR-sr NanoMSMARCO is a Serbian web passage retrieval task derived from
MS MARCO. Queries are short translated web-search questions, and documents are
translated answer-bearing passages. The task represents a practical search
setting where a user asks a concise question and expects a passage that
directly answers it. It is useful for evaluating whether multilingual retrieval
models can connect Serbian question phrasing to answer passages when exact
word overlap is weak or the answer is expressed descriptively.

## Details

### What the Original Data Measures

MS MARCO introduced large-scale real user queries paired with answer-bearing
passages. BEIR includes the passage retrieval version as a benchmark for
ranking passages that answer a query. The MNanoBEIR Serbian version preserves
this question-to-passage structure after translation. It measures whether a
retriever can identify answer-bearing text, not only text that shares the same
entity, phrase, or general topic.

### Observed Data Profile

This Nano subset contains 50 queries, 5,043 documents, and 50 positive qrels.
Every query has exactly one positive document, so the ranking target is narrow.
Queries average 35.64 characters, and documents average 331.07 characters.
This short-query structure makes the task sensitive to early ranking: if the
single answer passage is not near the top, the query is effectively missed for
downstream answer extraction or user-facing search.

### BM25 Evaluation Profile

BM25 uses the `bm25` top-500 candidate subset. It reaches nDCG@10 0.2833,
hit@10 0.4400, and recall@100 0.7600. Lexical matching can find the positive
when the question contains a distinctive term, song title, entity, or phrase
that appears in the passage. However, the top-10 success rate is low. Serbian
translated web questions often require recognizing that a passage answers the
question even when wording differs. BM25 is therefore useful for broad lexical
candidate generation but weak for answer-aware top ranking.

### Dense Evaluation Profile

Dense retrieval uses the `harrier_oss_v1_270m` top-500 candidate subset. It
scores nDCG@10 0.4541, hit@10 0.6600, and recall@100 0.9200, outperforming
BM25 across all reported metrics. This shows that embedding similarity is much
better suited to Serbian MS MARCO-style retrieval. Dense retrieval can connect
definition questions, "who sang" questions, actor-role questions, geography
questions, and word-meaning queries to passages that provide the answer even
when exact phrasing differs. The remaining errors are likely answer ambiguity
or same-topic passages that do not contain the requested fact.

### Reranking Hybrid Evaluation Profile

The reranking hybrid subset uses `reranking_hybrid` with top-100 candidates and
an optional rank-101 safeguard. Candidate counts range from 100 to 101, with a
mean of 100.10 and 5 safeguard rows. It reaches nDCG@10 0.4072, hit@10 0.6400,
and recall@100 0.9000. Hybrid retrieval improves greatly over BM25 and nearly
matches dense recall, but dense remains better for early ordering. The hybrid
pool is still useful for reranking because it combines exact lexical anchors
with semantic answer candidates, giving a downstream model a broad set of
possible answer passages.

### Metric Interpretation for Model Researchers

Because every query has one positive, hit@10 is a direct first-page success
measure, and recall@100 shows whether the positive is available to a reranker.
nDCG@10 captures how highly the answer passage is ranked. The dense profile is
clearly strongest here, indicating that Serbian translated web QA relies
heavily on semantic answer matching. Hybrid retrieval provides a strong
candidate pool but needs answer-aware reranking to surpass dense ordering.

### Query and Relevance Type Tendencies

Queries are short Serbian web questions about definitions, songs, television
roles, geography, and word meanings. Relevant documents are compact passages
that answer the question directly or contain enough context to answer it. A
document that merely mentions the same entity or phrase is not sufficient.
This favors models that preserve interrogative intent and answer-bearing
content.

### Representative Failure Modes

BM25 may retrieve passages with the same entity or term but no answer. Dense
models may retrieve semantically nearby passages that discuss a related topic
or entity while missing the requested attribute. Hybrid retrieval can include
both lexical and semantic distractors. Serbian translation and transliteration
can also reduce direct overlap for names, titles, and borrowed terms.

### Training Data That May Help

Helpful training data includes non-overlapping web QA retrieval, Serbian
search query logs, multilingual passage retrieval, answer-bearing passage
pairs, and hard-negative answer selection. Hard negatives should match surface
terms without answering the question. Training should exclude MS MARCO, BEIR,
NanoBEIR, and overlapping translations.

### Model Improvement Notes

NanoMSMARCO-sr is a compact benchmark for answer-aware passage retrieval.
Dense retrieval is the strongest single profile, while reranking hybrid offers
a useful mixed candidate pool. Improvements should focus on short-query
understanding, answer containment, Serbian entity and title handling, and
rerankers that distinguish answer passages from topical passages.

## Example Data

| Query | Positive document |
| --- | --- |
| Šta je sindrom ruminacije? [26 chars] | Ruminacioni sindrom. Ruminacioni sindrom, takođe poznat kao Mericizam, je vrsta poremećaja ishrane koji nije drugačije određen, a uzrokuje regurgitaciju hrane. Iako nije prepoznat kao specifični poremećaj ishrane u DSM-IV, određeni parametri su definisani za dijagnozu ovog poremećaja. [285 chars] |
| Ko je pevao pesmu "Here I Go Again"? [36 chars] | Za druge upotrebe, pogledajte Here I Go Again (razvrstavanje). "Here I Go Again" je pesma britanskog rok benda Whitesnake. Prvobitno objavljena na njihovom albumu iz 1982. godine Saints & Sinners, pesma je ponovo snimljena za njihov istoimeni album iz 1987. godine Whitesnake. Iste godine pesma je ponovo snimljena u novoj radio-miks verziji. [342 chars] |
| Koga Kameron Bojs glumi u seriji "Liv i Madi"? [46 chars] | Spremite se na prave hah-ahe, ljudi. U EKSKLUZIVNOM prethodnom prikazu epizode "Liv i Madi" od 19. aprila pod nazivom "Maturska večer-A-Runi". Naravno. U urnebesnom isečku vidimo Džesijevu zvezdu Kamerona Bojsa kako prelazi u drugi Diznijev šou kako bi upoznao Madi (Šelbi Vulfert). Njegov lik je, hm, ekscentričan! [315 chars] |

### Public Sources

- [MS MARCO: A Human Generated MAchine Reading COmprehension Dataset](https://arxiv.org/abs/1611.09268).
- [BEIR: A Heterogeneous Benchmark for Zero-shot Evaluation of Information Retrieval Models](https://arxiv.org/abs/2104.08663).
- [MMTEB: Massive Multilingual Text Embedding Benchmark](https://arxiv.org/abs/2502.13595).
- [Zeta Alpha NanoBEIR collection](https://huggingface.co/collections/zeta-alpha-ai/nanobeir).
- [NanoBEIR-sr dataset](https://huggingface.co/datasets/hakari-bench/NanoBEIR-sr).

### Source Reference Table

| Title | Year | Type | URL |
| --- | ---: | --- | --- |
| MS MARCO: A Human Generated MAchine Reading COmprehension Dataset | 2016 | task paper | [https://arxiv.org/abs/1611.09268](https://arxiv.org/abs/1611.09268) |
| BEIR: A Heterogeneous Benchmark for Zero-shot Evaluation of Information Retrieval Models | 2021 | benchmark paper | [https://arxiv.org/abs/2104.08663](https://arxiv.org/abs/2104.08663) |
| MMTEB: Massive Multilingual Text Embedding Benchmark | 2025 | benchmark paper | [https://arxiv.org/abs/2502.13595](https://arxiv.org/abs/2502.13595) |
| NanoBEIR: Smaller BEIR dataset subsets | 2024 | dataset collection | [https://huggingface.co/collections/zeta-alpha-ai/nanobeir](https://huggingface.co/collections/zeta-alpha-ai/nanobeir) |
