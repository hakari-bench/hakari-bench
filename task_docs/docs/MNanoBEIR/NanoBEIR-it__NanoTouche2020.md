# MNanoBEIR / NanoBEIR-it / NanoTouche2020

## Overview

`NanoBEIR-it__NanoTouche2020` is the Italian NanoBEIR version of the Touché
2020 argument retrieval task for controversial questions. The task uses Italian
translated debate-style questions as queries and asks a retriever to rank
Italian translated arguments that address the topic. The Nano split contains 49
queries, 5,745 documents, and 932 positive qrels. Every query is multi-positive,
with 19.02 positives per query on average. This makes it a broad argument
retrieval benchmark: finding one topical argument is often easy, but ranking
substantive, relevant pro and con arguments above long topical distractors is
the harder part.

## Details

### What the Original Data Measures

[Touché 2020](https://doi.org/10.1007/978-3-030-58219-7_26) evaluated argument
retrieval for controversial questions. Relevance depends on more than topic
match: a useful document should contain argumentative content that can support,
oppose, or otherwise address the issue raised by the query. BEIR includes
Touché 2020 as an argument retrieval benchmark, and this Italian NanoBEIR task
keeps the same structure after translation. Queries are short controversial
questions, while documents are longer debate-style passages.

### Observed Data Profile

The task has 49 queries rather than 50, 5,745 documents, and 932 positive qrels.
Every query has multiple positives. The positives-per-query distribution ranges
from 6 to 32, with a median of 19.00. Queries average 56.29 characters, while
documents are long, averaging 2,352.77 characters. This combination creates an
evaluation where hit@10 can be very high because many relevant arguments exist,
but nDCG@10 still tests whether the most useful arguments are ranked early.
Long documents also introduce many opportunities for partial topical overlap.

### BM25 Evaluation Profile

The BM25 top-500 subset reaches nDCG@10 = 0.5714, hit@10 = 1.0000, and
Recall@100 = 0.7554. BM25 is very strong at finding at least one relevant
argument because controversial questions repeat topical words that also appear
in debate documents. Its perfect hit@10 should not be overinterpreted: with many
positives per query, at least one relevant document is usually easy to retrieve.
The more important signal is nDCG@10, where BM25 provides strong early ranking
but still has room to improve argument quality and coverage.

### Dense Evaluation Profile

The dense `harrier-oss-270m` top-500 subset reaches nDCG@10 = 0.4599, hit@10 =
0.9796, and Recall@100 = 0.7725. Dense retrieval has slightly better top-100
coverage than BM25, but it is much weaker on nDCG@10. This indicates that
embedding similarity can broaden the candidate set to include additional
arguments, but it may also rank general semantic or topical matches above
stronger argumentative passages. For this task, the distinction between
"discusses the issue" and "is a relevant argument for the issue" matters.

### Reranking Hybrid Evaluation Profile

The `reranking_hybrid` subset uses 100 candidates per query and reaches
nDCG@10 = 0.5717, hit@10 = 0.9796, and Recall@100 = 0.7994, with no rank-101
safeguard rows. Hybrid retrieval is marginally the strongest on nDCG@10 and
clearly the strongest on Recall@100. It keeps BM25-like early ranking quality
while adding dense-retrieval coverage. The hit@10 value is slightly below BM25,
but in a many-positive argument task, the hybrid gain in coverage and nDCG is
more informative than a single missed top-10 hit.

### Metric Interpretation for Model Researchers

Touché 2020 is a useful example where BM25 looks very strong because topical
terms and many positives make first-hit retrieval easy. Dense retrieval helps
coverage but can weaken early ranking if it treats broad semantic relatedness as
argument relevance. The hybrid profile is the most balanced: it preserves
lexical topic anchoring and adds additional relevant arguments within the top
100. Researchers should evaluate not only whether a system finds any relevant
argument, but also whether it ranks diverse, substantive arguments above long
documents that merely mention the topic.

### Query and Relevance Type Tendencies

The examples ask whether homework is useful, whether prescription drugs should
be advertised directly to consumers, which vaccines children need, whether
abortion should be legal, and whether standardized tests improve education.
Positive documents are long debate passages, often with explicit claims,
evidence, and rhetorical structure. Relevance can include either side of a
controversy, so the retriever must match the issue and recognize argumentative
content rather than only a stance.

### Representative Failure Modes

BM25 can over-rank documents that repeat the topic words but contain weak or
off-target argumentation. Dense retrieval can retrieve broadly related opinion
or policy text that does not answer the specific controversial question. Hybrid
retrieval can improve coverage but still mix strong arguments with topical
distractors. Long documents also make partial-match errors common: one paragraph
may mention the issue while the overall document addresses a different debate.

### Training Data That May Help

Useful training data includes non-overlapping argument retrieval data, debate
portal argument collections, pro/con retrieval pairs, and multilingual argument
quality or stance datasets. Hard negatives should share the controversial topic
but lack a direct argument for the query. Training should exclude Touché 2020,
BEIR, NanoBEIR, and overlapping translated argument documents from this
benchmark.

### Model Improvement Notes

Strong systems should combine topic matching, stance-agnostic argument
recognition, and ranking signals for argument specificity. A candidate generator
should retrieve both pro and con documents, while a reranker should favor
passages that directly address the question with explicit reasons or evidence.
Because the task has many positives, diversity across relevant arguments is also
important for robust top-100 coverage.

## Example Data

| Query | Positive document |
| --- | --- |
| È utile fare i compiti a casa? [30 chars] | Prima di tutto, ci sono tre argomenti a favore del perché i compiti a casa sono eccellenti e dovrebbero continuare nelle scuole moderne. 1. I compiti aiutano gli studenti che imparano facendo. È gener... [200 / 4,034 chars] |
| È giusto che i farmaci da prescrizione siano pubblicizzati direttamente ai consumatori? [87 chars] | Molti annunci pubblicitari non includono informazioni sufficienti su quanto bene funzionano i farmaci. Ad esempio, Lunesta viene pubblicizzato da una falena che vola attraverso una finestra della came... [200 / 1,972 chars] |
| Quali vaccini sono necessari per i bambini? [43 chars] | Non è ancora un caso completo... Solo alcuni punti che ho messo insieme... I governi non dovrebbero avere il diritto di intervenire nelle decisioni sanitarie che i genitori prendono per i loro figli.... [200 / 5,135 chars] |
| L'aborto dovrebbe essere legale? [32 chars] | L'aborto dovrebbe essere legale poiché la personalità giuridica inizia dopo che il feto diventa vitale o dopo la nascita, non al momento del concepimento. Secondo la Corte Suprema degli Stati Uniti, u... [200 / 353 chars] |
| I test standardizzati migliorano l'istruzione? [46 chars] | Risolto: Il SAT, l'ACT e altri test standardizzati forniscono maggiori informazioni sulla preparazione di uno studente delle superiori per l'istruzione in college e università di élite rispetto al vot... [200 / 4,640 chars] |

### Public Sources

- [Overview of Touché 2020: Argument Retrieval](https://doi.org/10.1007/978-3-030-58219-7_26).
- [Touche20-Argument-Retrieval-for-Controversial-Questions](https://doi.org/10.5281/zenodo.6862281).
- [BEIR: A Heterogeneous Benchmark for Zero-shot Evaluation of Information Retrieval Models](https://arxiv.org/abs/2104.08663).
- [MMTEB: Massive Multilingual Text Embedding Benchmark](https://arxiv.org/abs/2502.13595).
- [Zeta Alpha NanoBEIR collection](https://huggingface.co/collections/zeta-alpha-ai/nanobeir).
- [hakari-bench/NanoBEIR-it](https://huggingface.co/datasets/hakari-bench/NanoBEIR-it).

### Source Reference Table

| Title | Year | Type | URL |
| --- | ---: | --- | --- |
| Overview of Touché 2020: Argument Retrieval | 2020 | benchmark paper | [https://doi.org/10.1007/978-3-030-58219-7_26](https://doi.org/10.1007/978-3-030-58219-7_26) |
| Touche20-Argument-Retrieval-for-Controversial-Questions | 2022 | dataset page | [https://doi.org/10.5281/zenodo.6862281](https://doi.org/10.5281/zenodo.6862281) |
| BEIR: A Heterogeneous Benchmark for Zero-shot Evaluation of Information Retrieval Models | 2021 | benchmark paper | [https://arxiv.org/abs/2104.08663](https://arxiv.org/abs/2104.08663) |
| MMTEB: Massive Multilingual Text Embedding Benchmark | 2025 | benchmark paper | [https://arxiv.org/abs/2502.13595](https://arxiv.org/abs/2502.13595) |
| NanoBEIR: Smaller BEIR dataset subsets | 2024 | dataset collection | [https://huggingface.co/collections/zeta-alpha-ai/nanobeir](https://huggingface.co/collections/zeta-alpha-ai/nanobeir) |
