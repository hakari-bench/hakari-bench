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
| È utile fare i compiti a casa? [30 chars] | Prima di tutto, ci sono tre argomenti a favore del perché i compiti a casa sono eccellenti e dovrebbero continuare nelle scuole moderne. 1. I compiti aiutano gli studenti che imparano facendo. È generalmente accettato che ci siano tre tipi di studenti: quelli che imparano ascoltando, quelli che imparano vedendo e quelli che imparano facendo. Mentre molti sono soddisfatti di ascoltare o vedere le istruzioni su un dato argomento, alcuni devono effettivamente farlo. Pertanto, i compiti sono benefici per questo ultimo gruppo perché l'istruzione viene appresa attraverso l'azione. 2. I compiti rafforzano l'insegnamento. Anche se molti probabilmente sarebbero felici di non avere compiti, la qualità dell'istruzione ricevuta ne risentirebbe sicuramente se venissero eliminati. Che si tratti di letture assegnate, tesine, ecc., tutto è progettato per rafforzare l'insegnamento nella mente degli studenti. Dopo tutto, coloro che fanno i compiti sono più accademicamente di successo rispetto a chi non... [1,000 / 4,034 chars] |
| È giusto che i farmaci da prescrizione siano pubblicizzati direttamente ai consumatori? [87 chars] | Molti annunci pubblicitari non includono informazioni sufficienti su quanto bene funzionano i farmaci. Ad esempio, Lunesta viene pubblicizzato da una falena che vola attraverso una finestra della camera da letto, sopra una persona che dorme tranquillamente. In realtà, Lunesta aiuta i pazienti ad addormentarsi 15 minuti più velocemente dopo sei mesi di trattamento e fornisce 37 minuti in più di sonno per notte. La maggior parte degli annunci si basa su appelli emotivi, ma pochi includono le cause della condizione, i fattori di rischio o i cambiamenti nello stile di vita importanti. In uno studio di 38 pubblicità farmaceutiche, i ricercatori hanno riscontrato che l'82% faceva affermazioni di fatto e l'86% presentava argomentazioni razionali per l'uso del prodotto. Solo il 26% descriveva le cause della condizione, i fattori di rischio o la prevalenza. Questo non fornisce ai pazienti informazioni bilanciate che li renderebbero consapevoli che assumere una di queste pillole non è una soluzi... [1,000 / 1,972 chars] |
| Quali vaccini sono necessari per i bambini? [43 chars] | Non è ancora un caso completo... Solo alcuni punti che ho messo insieme... I governi non dovrebbero avere il diritto di intervenire nelle decisioni sanitarie che i genitori prendono per i loro figli. Secondo un sondaggio del 2010 dell'Università del Michigan, il 31% dei genitori ritiene di avere il diritto di rifiutare le vaccinazioni obbligatorie per l'ingresso a scuola per i propri figli. Molti genitori hanno convinzioni religiose contro la vaccinazione. Costringere tali genitori a vaccinare i loro figli violerebbe il 1° Emendamento, che garantisce ai cittadini il diritto di esercitare liberamente la propria religione. I vaccini sono spesso inutili in molti casi in cui la minaccia di morte per malattia è piccola. All'inizio del XIX secolo, la mortalità per malattie infantili come la pertosse, il morbillo e la scarlattina è diminuita drasticamente prima che le immunizzazioni diventassero disponibili. Questa riduzione della mortalità è stata attribuita a una migliore igiene personale,... [1,000 / 5,135 chars] |

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
