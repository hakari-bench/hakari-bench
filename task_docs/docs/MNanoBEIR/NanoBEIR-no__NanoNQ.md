# MNanoBEIR / NanoBEIR-no / NanoNQ

## Overview

NanoBEIR-no NanoNQ is a Norwegian open-domain question answering retrieval task
derived from Natural Questions. Queries are translated information-seeking
questions, and documents are translated Wikipedia passages that contain answer
evidence. The task represents a common search and QA retrieval problem: a short
question must be matched to the passage that contains the answer, often through
entities, dates, titles, or explanatory context. It is useful for evaluating
whether multilingual retrieval models can connect concise Norwegian questions
to answer-bearing passages when the wording of the question and evidence is not
identical.

## Details

### What the Original Data Measures

Natural Questions was built from real Google search questions paired with
Wikipedia annotations. In retrieval benchmarks such as BEIR, NQ evaluates the
evidence retrieval step before answer extraction. The MNanoBEIR Norwegian
version keeps this open-domain QA structure while using a compact translated
subset. It measures whether a retriever can identify the passage that contains
the answer to a question, not merely a passage that mentions the same entity or
topic.

### Observed Data Profile

This Nano subset contains 50 queries, 5,035 documents, and 57 positive qrels.
Most queries have one positive, while 7 queries have multiple positives. The
average positives per query is 1.14, with a minimum of 1, median of 1.00, and
maximum of 2. Queries average 48.04 characters, and documents average 521.96
characters. This makes the task a short-query evidence retrieval benchmark:
the model has limited query text, but the relevant passage must contain enough
context to answer the question.

### BM25 Evaluation Profile

BM25 uses the `bm25` top-500 candidate subset. It reaches nDCG@10 0.3011,
hit@10 0.4800, and recall@100 0.7018. Lexical matching recovers many positives
within a broad candidate pool, especially when questions contain distinctive
names, titles, or phrases. The weaker top-10 results show that exact word
overlap is often insufficient for answer retrieval. Many passages may mention
the same entity or topic without answering the question, and translated
questions can phrase the information need differently from the evidence
passage. BM25 is therefore useful as a lexical candidate generator but not as a
complete ranking solution.

### Dense Evaluation Profile

Dense retrieval uses the `harrier_oss_v1_270m` top-500 candidate subset. It
scores nDCG@10 0.5490, hit@10 0.7600, and recall@100 0.9474, substantially
outperforming BM25. This profile shows that embedding similarity is strongly
suited to Norwegian NQ-style retrieval. Dense retrieval can connect question
intent to evidence passages through semantic relation, paraphrase, and answer
context rather than exact term repetition. The high recall@100 also means dense
candidates give a downstream reranker access to almost all positives in this
Nano subset. The remaining errors likely involve answer ambiguity, entity
confusion, or passages that are semantically close but do not contain the
requested answer.

### Reranking Hybrid Evaluation Profile

The reranking hybrid subset uses `reranking_hybrid` with top-100 candidates and
an optional rank-101 safeguard. Candidate counts range from 100 to 101, with a
mean of 100.04 and 2 safeguard rows. It reaches nDCG@10 0.3641, hit@10 0.5800,
and recall@100 0.9474. The hybrid profile matches dense recall@100 but trails
dense in early ranking. This indicates that combining BM25 and dense evidence
is effective for candidate coverage, but the hybrid candidate order is less
answer-aware than the dense order. For reranking experiments, this is a useful
pool: it preserves broad coverage while forcing the reranker to distinguish
true answer evidence from lexical and semantic distractors.

### Metric Interpretation for Model Researchers

Because most queries have a single positive, hit@10 is a direct measure of
whether the answer evidence reaches the first page. Recall@100 shows whether a
reranker can access the positive at all, and nDCG@10 rewards placing it near
the top. The dense profile is clearly strongest for early ranking and coverage,
while the hybrid profile shows that mixed lexical-semantic retrieval can match
dense coverage without matching its top-rank quality. For model researchers,
this task is a useful probe of short-question answer semantics, especially the
ability to rank answer-bearing passages above merely topical Wikipedia text.

### Query and Relevance Type Tendencies

Queries are natural questions about events, media, legal references, people,
places, and definitions. Relevant documents are Wikipedia passages containing
the answer or a direct explanation. Examples include questions about where an
event is held, whether a film originated at Disney, why a landmark stands in a
location, where a constitutional compromise appears, and who sang on a song.
These needs favor models that represent interrogative intent, entity
disambiguation, and answer-bearing context.

### Representative Failure Modes

BM25 may retrieve a passage that repeats a named entity but lacks the answer.
Dense models may retrieve semantically related passages that discuss the same
event, film, or song but answer a different question. Hybrid retrieval can
include both exact-match and semantic distractors, leaving the ordering problem
to a downstream reranker. Translation can also introduce mismatch when the
Norwegian query expresses the question naturally but the evidence passage uses
a different translated phrase.

### Training Data That May Help

Helpful training data includes non-overlapping open-domain QA retrieval,
Wikipedia question-passage pairs, multilingual QA evidence selection,
Norwegian information-seeking questions, and hard-negative passage retrieval.
Hard negatives should contain related entities or topics without the requested
answer. Training should exclude Natural Questions, BEIR, NanoBEIR, and
overlapping translated Wikipedia passages.

### Model Improvement Notes

NanoNQ-no is a compact benchmark for answer-aware open-domain retrieval. Dense
retrieval is the strongest single candidate profile, while reranking hybrid
offers the same recall@100 and a broader mixed candidate set. Improvements
should focus on short-query understanding, answer containment, entity
disambiguation, and rerankers that verify whether a passage actually answers
the question. For practical QA systems, the main objective is to preserve dense
coverage while improving the ordering of answer-bearing passages inside hybrid
candidate pools.

## Example Data

| Query | Positive document |
| --- | --- |
| Hvor blir Final Four avholdt i år? [34 chars] | Turneringen om NCAA Division I menns college-basketball i 2018 var en 68-lags utslagningsturnering som skulle kåre nasjonal mester i college-basketball for sesongen 2017–18. Den 80. utgaven av turneringen startet 13. mars 2018 og avsluttet med finalen 2. april på Alamodome i San Antonio, Texas. [295 chars] |
| Var Nattens Hær opprinnelig en Disney-film? [43 chars] | The Nightmare Before Christmas hadde sin opprinnelse i et dikt skrevet av Tim Burton i 1982, mens han jobbet som animator ved Walt Disney Feature Animation. Med suksessen til Vincent samme år begynte Walt Disney Studios å vurdere å utvikle The Nightmare Before Christmas som enten en kortfilm eller en 30-minutters TV-spesial. Gjennom årene vendte Burtons tanker stadig tilbake til prosjektet, og i 1990 inngikk han en utviklingsavtale med Disney. Produksjonen startet i juli 1991 i San Francisco; Disney ga ut filmen under sitt Touchstone Pictures-banner fordi studioet mente filmen ville være 'for mørk og skremmende for barn'. [629 chars] |
| Hvorfor står Engelen i Nord-England der? [40 chars] | Ifølge Gormley hadde en engel en trefoldig betydning: først for å indikere at kullgruvearbeidere hadde jobbet i to århundrer under stedet der den ble bygget, andre for å fange overgangen fra en industriell til en informasjonsalder, og tredje for å fungere som et fokus for våre utviklende håp og frykt. [302 chars] |

### Public Sources

- [Natural Questions: A Benchmark for Question Answering Research](https://aclanthology.org/Q19-1026/).
- [BEIR: A Heterogeneous Benchmark for Zero-shot Evaluation of Information Retrieval Models](https://arxiv.org/abs/2104.08663).
- [MMTEB: Massive Multilingual Text Embedding Benchmark](https://arxiv.org/abs/2502.13595).
- [Zeta Alpha NanoBEIR collection](https://huggingface.co/collections/zeta-alpha-ai/nanobeir).
- [NanoBEIR-no dataset](https://huggingface.co/datasets/hakari-bench/NanoBEIR-no).

### Source Reference Table

| Title | Year | Type | URL |
| --- | ---: | --- | --- |
| Natural Questions: A Benchmark for Question Answering Research | 2019 | task paper | [https://aclanthology.org/Q19-1026/](https://aclanthology.org/Q19-1026/) |
| BEIR: A Heterogeneous Benchmark for Zero-shot Evaluation of Information Retrieval Models | 2021 | benchmark paper | [https://arxiv.org/abs/2104.08663](https://arxiv.org/abs/2104.08663) |
| MMTEB: Massive Multilingual Text Embedding Benchmark | 2025 | benchmark paper | [https://arxiv.org/abs/2502.13595](https://arxiv.org/abs/2502.13595) |
| NanoBEIR: Smaller BEIR dataset subsets | 2024 | dataset collection | [https://huggingface.co/collections/zeta-alpha-ai/nanobeir](https://huggingface.co/collections/zeta-alpha-ai/nanobeir) |
