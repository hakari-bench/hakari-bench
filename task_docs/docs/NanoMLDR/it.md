# NanoMLDR / it

## Overview

`NanoMLDR / it` is the Italian split of NanoMLDR, a multilingual long-document
retrieval benchmark derived from MLDR. Italian paragraph-grounded questions
retrieve full Italian articles, where the answer-bearing paragraph may be only
one part of a long document. The Nano split has 158 queries, 3,116 documents,
and 158 positive qrel rows, with exactly one positive document per query.
Current diagnostics show BM25 as the strongest top-rank profile,
`reranking_hybrid` as matching BM25 on recall@100, and dense retrieval as useful
but weaker for full-document ranking.

## Details

### What the Original Data Measures

MLDR was introduced with the M3-Embedding work as a multilingual long-document
retrieval benchmark. The dataset card describes sampling long documents,
selecting a paragraph, and generating a specific question from that paragraph.
The retrieval target is the full article containing the answer-bearing
paragraph.

For Italian, this creates a long-document retrieval task rather than short
passage search. A retriever must identify a full Italian article from a question
that often refers to a local detail inside a much larger article.

### Observed Data Profile

The Nano split contains 158 queries, 3,116 documents, and 158 positive qrel
rows. Every query has exactly one positive document. Queries average 98.16
characters, while documents average 14,374.38 characters.

Observed examples include questions about Georgian grammar, behavior of a new
duke, Luxembourg tourism, CAD customization, Monferrato wines, cities,
musicians, film awards, football teams, and macroeconomic history. The positive
documents are long Italian articles containing the paragraph that generated the
question.

### BM25 Evaluation Profile

The dataset-provided BM25 candidate subset contains 500 candidates per query and
achieves nDCG@10 = 0.8884, hit@10 = 0.9367, and recall@100 = 0.9873. BM25 is the
strongest observed top-rank profile. Italian generated questions often retain
distinctive names, places, technical terms, historical roles, or regional
vocabulary from the answer paragraph.

This makes lexical retrieval highly effective. Even though documents are long,
rare article-specific terms can point directly to the correct full document.

### Dense Evaluation Profile

The dense `harrier_oss_v1_270m` candidate subset contains 500 candidates per
query and achieves nDCG@10 = 0.6832, hit@10 = 0.7722, and recall@100 = 0.8797.
Dense retrieval captures broad semantic similarity but is clearly weaker than
BM25. A single full-document representation can dilute the local paragraph
evidence needed to distinguish the exact article.

This is especially relevant for biographies, regional articles, technical
topics, and cultural works where many long Italian documents share the same
general theme but only one contains the requested paragraph.

### Reranking Hybrid Evaluation Profile

The `reranking_hybrid` candidate subset contains mostly 100 candidates per
query, with two queries using a rank-101 safeguard row. It achieves nDCG@10 =
0.7807, hit@10 = 0.8671, and recall@100 = 0.9873. Hybrid retrieval matches BM25
on recall@100 but remains below BM25 by nDCG@10 and hit@10.

This profile suggests that dense candidates help maintain coverage but do not
improve top-rank quality over lexical retrieval. Hybrid search is useful for
reranking pipelines, but BM25 remains the strongest base ranking signal here.

### Metric Interpretation for Model Researchers

This task is single-positive: each query has exactly one relevant long
document. Hit@10 measures whether that document appears near the top. nDCG@10
is sensitive to the rank of the positive, and recall@100 measures whether it
remains available for reranking.

The Italian MLDR profile rewards paragraph-derived lexical anchors. Dense
retrieval should be evaluated against a strong BM25 baseline, and any hybrid
reranker should preserve the sparse signal rather than overriding it with broad
semantic similarity.

### Query and Relevance Type Tendencies

Queries are Italian paragraph-grounded questions about grammar, historical
figures, tourism, technical systems, regional products, sports, music, cinema,
and economic history. They often mention multiple named entities or a specific
attribute from the source paragraph.

Relevant documents are long Italian articles with title context and answer-
bearing paragraphs. The task rewards exact entity and phrase matching, robust
long-document indexing, and paragraph-level evidence recognition.

### Representative Failure Modes

Dense retrieval can retrieve a thematically related article but miss the
paragraph-containing document. Long articles about regions, films, sports,
historical figures, or technical systems can be semantically close even when
only one contains the answer. BM25 can fail when several articles share the
same rare entity or when the question paraphrases the paragraph heavily.

Hybrid retrieval can preserve the positive in the candidate pool but rank a
related article above it. Rerankers should inspect document chunks or paragraphs
instead of scoring only full-article summaries.

### Training Data That May Help

Useful training data includes Italian long-document QA retrieval pairs, Italian
Wikipedia article retrieval, multilingual MLDR training data outside this Nano
split, and same-topic Italian article hard negatives. Training should include
cases where the positive full article is determined by a local paragraph.

Synthetic data can help when it samples paragraphs from long Italian
encyclopedic articles, generates grounded Italian questions, and uses the full
article as the positive. Negatives should be adjacent Italian articles that
share named entities, places, events, or technical terms but lack the answer
paragraph.

### Model Improvement Notes

Dense retrievers should use chunked indexing, late interaction, paragraph-aware
pooling, or multi-vector document representations to avoid losing local answer
evidence. Sparse systems should preserve exact Italian lexical anchors while
handling paraphrase and inflection. Rerankers should be validated against BM25
because the sparse ranking is very strong.

For hybrid systems, `NanoMLDR / it` supports BM25-first candidate generation
with dense retrieval as a recall supplement. The current hybrid profile matches
BM25 recall but does not surpass BM25 top-rank quality.

## Example Data

| Query | Positive document |
| --- | --- |
| Qual è la struttura delle frasi in georgiano riguardo l'uso dei numerali e degli aggettivi qualificativi? [105 chars] | La lingua georgiana (nome nativo ქართული ენა, kartuli ena) è la lingua più parlata della famiglia caucasica meridionale, di cui rappresenta la lingua franca, nonché l'unica lingua con una propria tradizione letteraria. È la lingua ufficiale della Georgia, dove conta all'incirca 3,9 milioni di parlanti nativi (l'83% della popolazione). Altre 3,5 milioni di persone la parlano all'estero (soprattutto in Turchia, Russia e Stati Uniti con piccole comunità in Iran ed Azerbaigian). Si tratta di una lingua agglutinante (nella quale cioè gli elementi si combinano a formare le parole in sequenza lineare), come risulta evidente soprattutto nei verbi. Possiede una flessione nominale articolata in sette casi. Il sistema fonetico presenta suoni particolari, detti glottalizzati. Le parole georgiane possono avere serie consecutive molto lunghe di consonanti: fino a otto (ad esempio in gvprtskvni "ci sbucci"). Per la scrittura sono stati utilizzati nel tempo tre diversi alfabeti. L'attuale alfabeto geo... [1,000 / 27,139 chars] |
| Quali caratteristiche negative emerse nel comportamento del nuovo Duca dopo aver preso il controllo del ducato? [111 chars] | Biografia L'unica erede del ducato Bianca Maria nacque nel castello di Settimo Pavese il 31 marzo del 1425, dalla nobildonna Agnese del Maino, forse dama di compagnia della sventurata Beatrice di Tenda, e dal duca Filippo Maria Visconti. Alla piccola venne dato il nome di Bianca, mutuato dalla nonna paterna di Filippo Maria, seguito dal nome Maria che era imposto per voto a tutti i discendenti di Gian Galeazzo Visconti. Le venne assegnata come balia Caterina Meravigli, (il cognome talvolta si trova nella forma Mirabiglia), appartenente a una famiglia di fidati cortigiani. Nonostante il padre desiderasse un figlio maschio, la nascita di una figlia non fu una completa delusione. Non avendo avuto figli dal primo matrimonio con Beatrice di Tenda, Filippo Maria aveva infatti presentato all'imperatore Sigismondo di Lussemburgo, di cui era vassallo, la richiesta di poter nominare suo successore un figlio naturale. Questa richiesta, inizialmente, fu rifiutata dalla corte imperiale ma, dopo con... [1,000 / 26,308 chars] |
| Quali sono alcuni dei luoghi turistici più importanti del Granducato che hanno ispirato Victor Hugo? [100 chars] | Il Lussemburgo (), ufficialmente Granducato di Lussemburgo (; ; ), è uno Stato dell'Unione europea senza affaccio sul mare, confinante con Germania, Francia e Belgio. Membro fondatore dell'Unione europea, della NATO, del Benelux e delle Nazioni Unite, la sua capitale, l'omonima città di Lussemburgo, è sede di numerose istituzioni e agenzie europee oltre a essere uno snodo finanziario di primaria importanza. Storia L'anno 963 segna l'inizio della storia del Lussemburgo con uno scambio tra il conte Sigfrido di Lussemburgo e l'Abbazia di San Massimino a Treviri. Sui resti di un castellum romano sul Bock chiamato Lucilinburhuc (che significa "piccolo castello"), Sigfrido fa costruire un castello attorno al quale, nel corso dei secoli, si sviluppa una città-fortezza. Nel 1354 la contea del Lussemburgo viene elevata al rango di un ducato del Sacro Romano Impero. Con l'estinzione della dinastia dei Conti di Lussemburgo (1443) viene prima integrato nello Stato borgognone di Filippo il Buono e... [1,000 / 25,354 chars] |

### Public Sources

- [M3-Embedding: Multi-Linguality, Multi-Functionality, Multi-Granularity Text Embeddings Through Self-Knowledge Distillation](https://arxiv.org/abs/2402.03216),
  2024.
- [M3-Embedding ACL Anthology version](https://aclanthology.org/2024.findings-acl.137/),
  2024.
- [Shitao/MLDR dataset card](https://huggingface.co/datasets/Shitao/MLDR).
- [hakari-bench/NanoMLDR](https://huggingface.co/datasets/hakari-bench/NanoMLDR),
  Nano benchmark dataset.

### Source Reference Table

| Title | Year | Type | URL |
| --- | ---: | --- | --- |
| M3-Embedding: Multi-Linguality, Multi-Functionality, Multi-Granularity Text Embeddings Through Self-Knowledge Distillation | 2024 | benchmark paper | [https://arxiv.org/abs/2402.03216](https://arxiv.org/abs/2402.03216) |
| M3-Embedding ACL Anthology version | 2024 | paper | [https://aclanthology.org/2024.findings-acl.137/](https://aclanthology.org/2024.findings-acl.137/) |
| MLDR: Multilingual Long-Document Retrieval dataset | 2024 | dataset card | [https://huggingface.co/datasets/Shitao/MLDR](https://huggingface.co/datasets/Shitao/MLDR) |

### Representative Snippets

| Query pattern | Positive document pattern |
| --- | --- |
| An Italian question about Georgian grammar and numerals. | A long article about the Georgian language. |
| A question about behavior after taking control of a duchy. | A long biographical or historical article. |
| A question about tourist places that inspired Victor Hugo. | A long article about Luxembourg. |
| A question about CAD customization options. | A long article about CAD systems. |
| A question about famous wines of Monferrato. | A long article about the Monferrato region. |
