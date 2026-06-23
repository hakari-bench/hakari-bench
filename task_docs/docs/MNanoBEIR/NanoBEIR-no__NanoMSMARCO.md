# MNanoBEIR / NanoBEIR-no / NanoMSMARCO

## Overview

NanoBEIR-no NanoMSMARCO is a Norwegian web passage retrieval task derived from
MS MARCO. Queries are short translated web-search questions, and documents are
translated answer-bearing passages. The task reflects a familiar search
setting: a user asks a concise natural-language question and expects a passage
that directly answers it. It is useful for evaluating whether multilingual
retrieval models can connect brief Norwegian questions to relevant explanatory
passages when exact word overlap is limited by translation, paraphrase, and
answer phrasing.

## Details

### What the Original Data Measures

MS MARCO introduced a large-scale dataset of real user queries paired with
answer passages. In BEIR, the passage retrieval version evaluates whether
systems can retrieve answer-bearing text for open-domain search questions. The
MNanoBEIR Norwegian version keeps that question-to-passage setup while using a
compact translated subset. It measures short-query retrieval over mixed web
content, where the positive passage should answer the question rather than only
share the same broad topic.

### Observed Data Profile

This Nano subset contains 50 queries, 5,043 documents, and 50 positive qrels.
Every query has exactly one positive document, so the ranking target is narrow.
Queries are short web questions averaging 34.98 characters, while documents are
compact answer passages averaging 331.30 characters. This structure makes early
ranking especially important: a retrieval system must infer the answer intent
from a small amount of query text and place the single relevant passage high
enough for a user or downstream reader to consume.

### BM25 Evaluation Profile

BM25 uses the `bm25` top-500 candidate subset. It reaches nDCG@10 0.3249,
hit@10 0.4800, and recall@100 0.7400. The recall score shows that lexical
matching often finds the positive passage somewhere in the broad candidate
pool, but the top-10 ranking is much weaker. This is expected for web QA:
questions and answers may use different wording, and many passages can repeat
the same entity or term without answering the query. BM25 is strongest when the
query contains a rare name, phrase, or definition target that appears directly
in the passage. It struggles when the answer is expressed descriptively or
requires recognizing that a passage answers an implicit question.

### Dense Evaluation Profile

Dense retrieval uses the `harrier_oss_v1_270m` top-500 candidate subset. It
scores nDCG@10 0.4174, hit@10 0.6000, and recall@100 0.8600, outperforming BM25
on all reported metrics. The dense profile indicates that embedding similarity
is better suited to the short-question, answer-passage format. It can connect
"what is" or "who sang" style questions to passages that explain the entity,
song, place, or definition even when exact terms differ. The remaining errors
likely come from answer ambiguity, translated phrasing, and passages that are
topically close but not answer-bearing. Dense retrieval is the strongest single
candidate profile for this Norwegian subset.

### Reranking Hybrid Evaluation Profile

The reranking hybrid subset uses `reranking_hybrid` with top-100 candidates and
an optional rank-101 safeguard. Candidate counts range from 100 to 101, with a
mean of 100.14 and 7 safeguard rows. It reaches nDCG@10 0.3728, hit@10 0.5600,
and recall@100 0.8600. The hybrid profile matches dense recall@100 and improves
substantially over BM25, but dense remains better in top-10 ranking. This means
the hybrid pool is useful for candidate generation because it preserves both
lexical and semantic options, while the initial hybrid ordering does not fully
capture answer quality. A reranker trained for question-answer relevance should
be able to exploit this pool effectively.

### Metric Interpretation for Model Researchers

Because each query has one positive, hit@10 is a direct first-page success
measure and recall@100 tells whether the positive is available to a reranker.
nDCG@10 reflects how close to the top the answer passage appears. The gap
between BM25 and dense shows that lexical term frequency is not enough for
Norwegian translated web QA. The match between dense and hybrid recall@100
suggests that hybrid search can preserve the same candidate coverage, but
dense ordering is more reliable for ranking the answer early. Researchers
should use this task to test answer-aware short-query retrieval rather than
only topical matching.

### Query and Relevance Type Tendencies

Queries are concise web questions such as definitions, people or song lookups,
television or media facts, geography, and word meanings. Relevant documents are
short passages that directly answer the question or provide enough context for
the answer. The key relevance signal is answer utility: a passage about the
same named entity is not enough unless it contains the requested fact. This
favors models that represent interrogative intent and answer-bearing content,
not just entity co-occurrence.

### Representative Failure Modes

BM25 may retrieve passages that contain the same name or term but do not answer
the question. Dense models may retrieve semantically related passages that
explain a nearby concept, media item, or entity while missing the requested
attribute. Hybrid retrieval may include both exact-match distractors and broad
semantic distractors, leaving final answer selection to a reranker. Translation
can reduce literal overlap when the Norwegian question and answer passage use
different expressions for the same web-search intent.

### Training Data That May Help

Helpful training data includes non-overlapping web QA retrieval, multilingual
passage retrieval, answer selection, Norwegian question-answer pairs, and
short-query search logs. Hard negatives should share the main entity or phrase
with the query while failing to answer it. Training should avoid MS MARCO,
BEIR, NanoBEIR, and overlapping translated answer passages.

### Model Improvement Notes

NanoMSMARCO-no is a compact diagnostic for open-domain answer passage
retrieval. Dense retrieval is the strongest single profile, while the
reranking hybrid pool gives the same recall@100 and may be more useful as an
input to a learned reranker. Improvements should focus on recognizing answer
intent, handling concise translated questions, and separating answer-bearing
passages from merely topical passages. A practical system would use hybrid
candidate generation for coverage, then rerank with a model trained on
question-passage answer relevance.

## Example Data

| Query | Positive document |
| --- | --- |
| Hva er ruminasjonssyndrom? [26 chars] | Ruminasjonssyndrom, også kalt merykisme, er en type spiseforstyrrelse som ikke er spesifisert ellers og som fører til oppkast av mat. Selv om det ikke er identifisert som en spesifikk spiseforstyrrels... [200 / 281 chars] |
| Hvem sang "Here I Go Again"? [28 chars] | For andre bruk, se Here I Go Again (forklaring). Here I Go Again er en sang av det britiske rockebandet Whitesnake. Sangen ble opprinnelig utgitt på albumet Saints & Sinners fra 1982, og ble spilt inn... [200 / 306 chars] |
| Hvem spiller Cameron Boyce i TV-serien Liv og Maddie? [53 chars] | Bli klar for mye latter, dere. I en eksklusiv forhåndsvisning av episoden den 19. april av 'Liv & Maddie' kalt 'Prom-A-Rooney.' Selvsagt. I den morsomme klippet ser vi Jessie-stjernen Cameron Boyce ho... [200 / 312 chars] |
| Hvor finner vi flest av jordens store ørkener? [46 chars] | De resterende ørkener på jorden ligger utenfor polområdene. Den største er Saharaørkenen, en subtropisk ørken i Nord-Afrika. [124 chars] |
| Hva betyr "bølle"? [18 chars] | Ut fra nåværende funn ser det ut til at kopper (en politimann, bokstavelig 'en som arresterer') er eldre enn cop (brukt verbalt og betyr å arrestere eller som substantiv for en politimann). Det kan go... [200 / 358 chars] |

### Public Sources

- [MS MARCO: A Human Generated Machine Reading Comprehension Dataset](https://arxiv.org/abs/1611.09268).
- [BEIR: A Heterogeneous Benchmark for Zero-shot Evaluation of Information Retrieval Models](https://arxiv.org/abs/2104.08663).
- [MMTEB: Massive Multilingual Text Embedding Benchmark](https://arxiv.org/abs/2502.13595).
- [Zeta Alpha NanoBEIR collection](https://huggingface.co/collections/zeta-alpha-ai/nanobeir).
- [NanoBEIR-no dataset](https://huggingface.co/datasets/hakari-bench/NanoBEIR-no).

### Source Reference Table

| Title | Year | Type | URL |
| --- | ---: | --- | --- |
| MS MARCO: A Human Generated Machine Reading Comprehension Dataset | 2016 | task paper | [https://arxiv.org/abs/1611.09268](https://arxiv.org/abs/1611.09268) |
| BEIR: A Heterogeneous Benchmark for Zero-shot Evaluation of Information Retrieval Models | 2021 | benchmark paper | [https://arxiv.org/abs/2104.08663](https://arxiv.org/abs/2104.08663) |
| MMTEB: Massive Multilingual Text Embedding Benchmark | 2025 | benchmark paper | [https://arxiv.org/abs/2502.13595](https://arxiv.org/abs/2502.13595) |
| NanoBEIR: Smaller BEIR dataset subsets | 2024 | dataset collection | [https://huggingface.co/collections/zeta-alpha-ai/nanobeir](https://huggingface.co/collections/zeta-alpha-ai/nanobeir) |
