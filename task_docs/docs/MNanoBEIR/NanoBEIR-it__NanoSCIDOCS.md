# MNanoBEIR / NanoBEIR-it / NanoSCIDOCS

## Overview

`NanoBEIR-it__NanoSCIDOCS` is the Italian NanoBEIR version of SCIDOCS, a
scientific-document retrieval benchmark associated with the SPECTER scientific
document representation work. The task uses Italian translated paper titles or
scientific query texts to retrieve Italian translated abstracts or document
descriptions that are related in a scholarly sense. The Nano split contains 50
queries, 2,210 documents, and 244 positive qrels. Every query has multiple
positives, usually five. This makes the task a compact benchmark for related
paper retrieval, where exact scientific terminology helps but disciplinary
context, method similarity, and citation-like relatedness are often needed to
rank the best documents.

## Details

### What the Original Data Measures

[SPECTER](https://arxiv.org/abs/2004.07180) introduced document-level
representations for scientific papers using citation-informed supervision, and
SCIDOCS provides evaluation tasks for scholarly document relatedness. BEIR uses
SCIDOCS as a scientific retrieval benchmark. In this Italian NanoBEIR version,
the retrieval problem is translated into Italian while retaining the original
scientific-document structure. Queries are often paper titles or compact
technical descriptions, and relevant documents are abstracts or descriptions of
papers that are related by method, topic, dataset, application, or research
area.

### Observed Data Profile

The task contains 50 queries and 2,210 documents. There are 244 positive qrels,
with 4.88 positives per query on average. The minimum number of positives per
query is 3, the median is 5.00, and the maximum is 5, so every query is
multi-positive. Queries average 89.52 characters, and documents average
1,062.02 characters. The documents are substantially longer than duplicate
questions or web snippets, and the queries often contain technical terms. This
creates a retrieval setting where vocabulary overlap and semantic relatedness
both matter, but relevance is rarely as simple as finding an answer sentence.

### BM25 Evaluation Profile

The BM25 top-500 subset reaches nDCG@10 = 0.2867, hit@10 = 0.7200, and
Recall@100 = 0.5410. BM25 benefits from technical terms that appear in both a
paper title and related abstracts, such as method names, device types, model
families, or application areas. However, its ranking quality is limited because
scientific relatedness often crosses vocabulary boundaries. Papers can be
relevant because they use a similar method, solve a related problem, or belong
to the same citation neighborhood without sharing many exact Italian tokens.

### Dense Evaluation Profile

The dense `harrier-oss-270m` top-500 subset reaches nDCG@10 = 0.3378, hit@10 =
0.8400, and Recall@100 = 0.6516. Dense retrieval is clearly stronger than BM25
for this task, especially in hit@10 and Recall@100. The result suggests that
embedding similarity captures scientific topic and method relatedness better
than term frequency alone. This is the expected behavior for SCIDOCS-like
retrieval: relevant papers can use different surface forms while still sharing
an underlying research contribution, experiment type, or scholarly context.

### Reranking Hybrid Evaluation Profile

The `reranking_hybrid` subset uses 100 to 101 candidates per query and reaches
nDCG@10 = 0.3499, hit@10 = 0.7800, and Recall@100 = 0.6475. One query uses the
rank-101 safeguard. Hybrid retrieval has the best nDCG@10, slightly above dense
retrieval, while dense remains stronger on hit@10 and marginally stronger on
Recall@100. This pattern indicates that lexical anchors still help order the
highest ranks when combined with dense similarity, but pure dense retrieval is
slightly better at ensuring at least one positive appears in the top 10.

### Metric Interpretation for Model Researchers

This task is best read as a related-document retrieval benchmark rather than
fact lookup. BM25 is a useful baseline for technical vocabulary overlap, but
dense retrieval provides a substantial gain in semantic coverage. The hybrid
profile shows that fusing lexical and dense signals can improve top-rank graded
quality, even when it does not dominate every metric. A strong model should be
able to rank multiple related scientific papers, not just one obvious abstract
that repeats the query title. Researchers should examine whether improvements
come from domain terminology, abstract-level semantic matching, or better
separation of same-field but unrelated papers.

### Query and Relevance Type Tendencies

The examples include power converters, sparse Gaussian Markov fields,
convolutional texture synthesis, RFID antenna design, and digital heart-rate
monitoring. Positive documents may describe methods, applications, or related
experiments rather than the exact query item. Some examples also reveal
translation noise in the document text, which can stress retrieval models that
depend too heavily on fluent phrasing. Effective retrieval needs to represent
technical concepts robustly across translated scientific prose.

### Representative Failure Modes

BM25 can miss related work when the query title and abstract use different
terminology for the same method or application. Dense retrieval can over-rank
papers from the same broad discipline that are not closely related to the query.
Hybrid retrieval can improve top-rank ordering but still inherit distractors
from both sides: exact vocabulary matches that are not relevant, and semantic
neighbors that are too broad. Multi-positive queries also expose coverage
failures when a model retrieves only one narrow cluster of related papers.

### Training Data That May Help

Useful training data includes non-overlapping citation recommendation,
related-paper retrieval, scientific abstract retrieval, and multilingual
scholarly text pairs. Hard negatives should come from the same field or use
overlapping technical vocabulary while differing in method, dataset, or claim.
Training should exclude SCIDOCS, SPECTER evaluation data, BEIR, NanoBEIR, and
overlapping translated abstracts from this benchmark.

### Model Improvement Notes

Strong systems for this task should combine domain-term precision with
document-level semantic representations. Citation-informed or related-work
training can help because relevance is closer to scholarly relatedness than to
question answering. For reranking, features that compare method, task,
application, and experimental context are likely more useful than features that
only count shared technical terms.

## Example Data

| Query | Positive document |
| --- | --- |
| Convertitore Elevatore CC-CC a Più Livelli Innovativo [53 chars] | I convertitori di tensione a sorgente multlivello stanno emergendo come una nuova categoria di opzioni di convertitori di potenza per applicazioni ad alta potenza. I convertitori di tensione a sorgente multlivello solitamente sintetizzano l'onda di tensione a gradini da diversi livelli di tensione dei condensatori in corrente continua. Una delle principali limitazioni dei convertitori multlivello è lo squilibrio di tensione tra i diversi livelli. Le tecniche per bilanciare la tensione tra i diversi livelli coinvolgono solitamente il clampaggio della tensione o il controllo della carica dei condensatori. Ci sono diversi modi per implementare il bilanciamento della tensione nei convertitori multlivello. Escludendo i convertitori tradizionali accoppiati magneticamente, questo articolo presenta tre convertitori di tensione a sorgente multlivello recentemente sviluppati: 1) a clamp diodi, 2) a condensatori volanti, e 3) inverter a cascata con sorgenti di corrente continua separate. Il princ... [1,000 / 1,122 chars] |
| Apprendimento di Campi Markoviani Gaussiani Sparsi Veloci Basato sulla Fattorizzazione di Cholesky [98 chars] | Sure, please provide the English document text that you need translated into Italian. [85 chars] |
| Sintesi delle Texture Utilizzando Reti Neurali Convoluzionali [61 chars] | In questo lavoro indaghiamo l'effetto della profondità della rete convoluzionale sulla sua accuratezza nel contesto del riconoscimento delle immagini su larga scala. Il nostro principale contributo è una valutazione approfondita di reti di profondità crescente, che dimostra che un miglioramento significativo rispetto alle configurazioni dello stato dell'arte può essere ottenuto aumentando la profondità a 16–19 strati di peso. Questi risultati sono stati la base della nostra partecipazione all'ImageNet Challenge 2014, dove il nostro team ha conquistato il primo e il secondo posto nelle categorie di localizzazione e classificazione rispettivamente. Abbiamo anche dimostrato che le nostre rappresentazioni si generalizzano bene ad altri dataset, dove ottengono risultati all'avanguardia. Importante, abbiamo reso disponibili al pubblico i nostri due modelli ConvNet migliori per facilitare ulteriori ricerche sull'uso delle rappresentazioni visive profonde nella visione artificiale. [988 chars] |

### Public Sources

- [SPECTER: Document-level Representation Learning using Citation-informed Transformers](https://arxiv.org/abs/2004.07180).
- [BEIR: A Heterogeneous Benchmark for Zero-shot Evaluation of Information Retrieval Models](https://arxiv.org/abs/2104.08663).
- [MMTEB: Massive Multilingual Text Embedding Benchmark](https://arxiv.org/abs/2502.13595).
- [Zeta Alpha NanoBEIR collection](https://huggingface.co/collections/zeta-alpha-ai/nanobeir).
- [hakari-bench/NanoBEIR-it](https://huggingface.co/datasets/hakari-bench/NanoBEIR-it).

### Source Reference Table

| Title | Year | Type | URL |
| --- | ---: | --- | --- |
| SPECTER: Document-level Representation Learning using Citation-informed Transformers | 2020 | task paper | [https://arxiv.org/abs/2004.07180](https://arxiv.org/abs/2004.07180) |
| BEIR: A Heterogeneous Benchmark for Zero-shot Evaluation of Information Retrieval Models | 2021 | benchmark paper | [https://arxiv.org/abs/2104.08663](https://arxiv.org/abs/2104.08663) |
| MMTEB: Massive Multilingual Text Embedding Benchmark | 2025 | benchmark paper | [https://arxiv.org/abs/2502.13595](https://arxiv.org/abs/2502.13595) |
| NanoBEIR: Smaller BEIR dataset subsets | 2024 | dataset collection | [https://huggingface.co/collections/zeta-alpha-ai/nanobeir](https://huggingface.co/collections/zeta-alpha-ai/nanobeir) |
