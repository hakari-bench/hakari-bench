# MNanoBEIR / NanoBEIR-pt / NanoMSMARCO

## Overview

NanoBEIR-pt NanoMSMARCO is a Portuguese web passage retrieval task derived
from MS MARCO. Queries are short translated web-search questions, and
documents are translated answer-bearing passages. The task represents a
practical open-domain search setting: the relevant passage should answer the
question, not merely mention the same topic. It is useful for evaluating
whether multilingual retrieval models can handle concise Portuguese questions,
paraphrased answer text, and the distinction between topical similarity and
answer utility.

## Details

### What the Original Data Measures

MS MARCO introduced large-scale real user queries paired with answer-bearing
passages. In BEIR, the passage retrieval version tests whether systems can
rank a passage that directly answers a short information need. The MNanoBEIR
Portuguese version keeps this question-to-passage structure after translation.
It measures answer-aware retrieval over compact web passages, where the query
is often only a few words long and the relevant passage must provide the
missing definition, person, place, or explanation.

### Observed Data Profile

This Nano subset contains 50 queries, 5,043 documents, and 50 positive qrels.
Every query has exactly one positive, so the ranking target is narrow. Queries
average 40.22 characters, while documents average 344.65 characters. The
single-positive setup makes top-rank placement important: a system can either
surface the answer passage early or miss the user's need entirely. The examples
cover definitions, songs, television roles, geography, and word meanings.

### BM25 Evaluation Profile

BM25 uses the `bm25` top-500 candidate subset. It reaches nDCG@10 0.3494,
hit@10 0.5200, and recall@100 0.7600. Lexical matching is useful when the
question contains a rare phrase, title, or named entity that appears in the
answer passage. However, the modest hit@10 shows that many Portuguese web
questions require answer-aware semantic matching. BM25 can retrieve passages
that share the same entity or term while failing to answer the exact question,
and translation can reduce direct word overlap between query and passage.

### Dense Evaluation Profile

Dense retrieval uses the `harrier_oss_v1_270m` top-500 candidate subset. It
scores nDCG@10 0.5121, hit@10 0.7000, and recall@100 0.9600, clearly
outperforming BM25. This profile matches the task design: embedding similarity
is better at connecting a short question to a passage that explains or answers
it, even when exact wording differs. Dense retrieval is especially helpful for
definition and "who" questions, where the answer passage may contain context
around the requested fact rather than a direct restatement of the question.
The remaining errors likely involve answer ambiguity and same-topic passages
that are semantically close but not answer-bearing.

### Reranking Hybrid Evaluation Profile

The reranking hybrid subset uses `reranking_hybrid` with top-100 candidates and
an optional rank-101 safeguard. Candidate counts range from 100 to 101, with a
mean of 100.02 and 1 safeguard row. It reaches nDCG@10 0.4873, hit@10 0.6800,
and recall@100 0.9800. The hybrid profile has the best recall@100, while dense
retrieval has slightly better early ranking. This indicates that combining
lexical and dense candidates is valuable for coverage: the positive passage is
almost always available to a reranker. The final ordering, however, still
needs answer-specific scoring to surpass dense retrieval in nDCG@10.

### Metric Interpretation for Model Researchers

Because each query has one positive, hit@10 is a direct first-page success
measure and recall@100 shows whether a reranker can access the answer passage.
nDCG@10 rewards placing that passage near the top. The observed pattern is a
clean short-query retrieval result: BM25 provides partial lexical coverage,
dense retrieval is the best single top-rank signal, and reranking hybrid gives
the broadest candidate coverage. Researchers should use this task to evaluate
answer-aware semantic retrieval rather than generic topic matching.

### Query and Relevance Type Tendencies

Queries are concise Portuguese web questions, including definitions, song and
media lookups, actor roles, geography, and meanings of words. Relevant
documents are short answer passages that contain the requested fact or
explanation. A document about the same entity is not sufficient unless it
answers the actual question. The task favors models that can represent
interrogative intent, entity context, and answer-bearing text.

### Representative Failure Modes

BM25 may over-rank exact-term passages that mention the query topic but do not
answer it. Dense models may retrieve semantically related passages that explain
a nearby concept or entity but miss the requested attribute. Hybrid retrieval
can recover the positive reliably but still include both lexical and semantic
distractors. Translation may also create unnatural phrasing or mismatch between
the Portuguese question and passage.

### Training Data That May Help

Helpful training data includes non-overlapping web QA retrieval, Portuguese
search query logs, multilingual passage retrieval, answer selection, and
short-query to answer-passage pairs. Hard negatives should share the main term
or entity while failing to answer the question. Training should exclude MS
MARCO, BEIR, NanoBEIR, and overlapping translations.

### Model Improvement Notes

NanoMSMARCO-pt is a useful benchmark for open-domain answer passage retrieval.
Dense retrieval is strongest for top ranking, while reranking hybrid provides
slightly better candidate coverage. Improvements should focus on answer
containment, short-query understanding, and reranking passages by whether they
resolve the question. A practical system would use hybrid generation for high
recall and an answer-aware reranker for final ordering.

## Example Data

| Query | Positive document |
| --- | --- |
| O que é a síndrome da ruminação? | Síndrome de Ruminação, também conhecida como mericismo, é um tipo de transtorno alimentar que causa a regurgitação de alimentos... |
| Quem cantou "Aqui vou eu de novo"? | "Here I Go Again" é uma música da banda britânica de rock Whitesnake... |
| Quem Cameron Boyce interpreta em Liv e Maddie? | Em uma prévia exclusiva do episódio de "Liv & Maddie", vemos o astro de "Jessie", Cameron Boyce... |
| Onde a maioria dos grandes desertos da Terra ocorre? | Os outros desertos da Terra estão fora das regiões polares. O maior é o Deserto do Saara... |
| Qual é o significado de "tira" para um policial? | De acordo com os achados atuais, parece que "copper" precede "cop", usado como verbo ou substantivo para policial... |

### Public Sources

- [MS MARCO: A Human Generated MAchine Reading COmprehension Dataset](https://arxiv.org/abs/1611.09268).
- [BEIR: A Heterogeneous Benchmark for Zero-shot Evaluation of Information Retrieval Models](https://arxiv.org/abs/2104.08663).
- [MMTEB: Massive Multilingual Text Embedding Benchmark](https://arxiv.org/abs/2502.13595).
- [Zeta Alpha NanoBEIR collection](https://huggingface.co/collections/zeta-alpha-ai/nanobeir).
- [NanoBEIR-pt dataset](https://huggingface.co/datasets/hakari-bench/NanoBEIR-pt).

### Source Reference Table

| Title | Year | Type | URL |
| --- | ---: | --- | --- |
| MS MARCO: A Human Generated MAchine Reading COmprehension Dataset | 2016 | task paper | https://arxiv.org/abs/1611.09268 |
| BEIR: A Heterogeneous Benchmark for Zero-shot Evaluation of Information Retrieval Models | 2021 | benchmark paper | https://arxiv.org/abs/2104.08663 |
| MMTEB: Massive Multilingual Text Embedding Benchmark | 2025 | benchmark paper | https://arxiv.org/abs/2502.13595 |
| NanoBEIR: Smaller BEIR dataset subsets | 2024 | dataset collection | https://huggingface.co/collections/zeta-alpha-ai/nanobeir |
