# MNanoBEIR / NanoBEIR-pt / NanoNQ

## Overview

NanoBEIR-pt NanoNQ is a Portuguese open-domain question answering retrieval
task derived from Natural Questions. Queries are translated Google-style
questions, and documents are translated Wikipedia passages that contain answer
evidence. The task is useful for evaluating whether a multilingual retriever
can connect a short, naturally phrased Portuguese question to the passage that
answers it. It tests answer-aware retrieval rather than simple topical search:
the best passage must contain the requested fact or explanation, not merely
mention the same entity.

## Details

### What the Original Data Measures

Natural Questions introduced naturally occurring search questions paired with
Wikipedia answers and annotations. In BEIR, the task is used as evidence
retrieval before answer extraction. The MNanoBEIR Portuguese version preserves
that retrieval structure after translation. It measures whether models can
retrieve answer-bearing passages for real question forms, including questions
about events, media, landmarks, constitutional references, and songs.

### Observed Data Profile

This Nano subset contains 50 queries, 5,035 documents, and 57 positive qrels.
Most queries have one positive, with a small two-positive tail. The average is
1.14 positives per query, with a minimum of 1, median of 1.00, and maximum of
2. Seven queries are multi-positive, covering 14.0% of the task. Queries
average 51.58 characters, while documents average 549.83 characters. This is a
short-query to medium-length evidence retrieval task where the relevant
passage must be ranked early enough for downstream QA.

### BM25 Evaluation Profile

BM25 uses the `bm25` top-500 candidate subset. It reaches nDCG@10 0.3645,
hit@10 0.6000, and recall@100 0.8070. Lexical overlap is useful because many
questions contain names, titles, places, or distinctive phrases that also
appear in the evidence passage. However, the top-10 score shows that term
matching is not enough for many Portuguese natural questions. BM25 can retrieve
passages about the same entity without confirming that the passage contains
the answer, and translated wording can reduce exact overlap between question
and evidence.

### Dense Evaluation Profile

Dense retrieval uses the `harrier_oss_v1_270m` top-500 candidate subset. It
scores nDCG@10 0.5103, hit@10 0.6600, and recall@100 0.8421, outperforming
BM25 in early ranking and coverage. Dense retrieval is better at mapping
question intent to evidence context, especially when the passage answers the
question with a paraphrase or a longer explanation. The remaining errors
likely involve entity ambiguity, answer-bearing passages that are lexically
sparse, or semantically related Wikipedia text that does not contain the exact
answer.

### Reranking Hybrid Evaluation Profile

The reranking hybrid subset uses `reranking_hybrid` with top-100 candidates and
an optional rank-101 safeguard. Candidate counts range from 100 to 101, with a
mean of 100.10 and 5 safeguard rows. It reaches nDCG@10 0.4522, hit@10 0.6600,
and recall@100 0.8772. The hybrid profile has the best recall@100 and matches
dense hit@10, but dense retrieval has stronger nDCG@10. This means hybrid
search is useful for candidate coverage, while the initial hybrid order still
needs a reranker that can identify true answer evidence.

### Metric Interpretation for Model Researchers

Because most queries have one positive, hit@10 is close to a query-level
first-page success signal, and recall@100 shows whether the positive is
available for reranking. nDCG@10 captures whether the answer passage is placed
near the top. The observed pattern separates the roles of retrieval stages:
dense retrieval gives the best early ordering, while reranking hybrid gives
the broadest positive coverage. This task is therefore useful for testing
answer-aware reranking over a high-recall mixed candidate pool.

### Query and Relevance Type Tendencies

Queries are naturally phrased Portuguese questions about events, films,
landmarks, constitutional text, and music. Relevant documents are Wikipedia
passages that provide the requested answer or direct supporting context.
Examples include the Final Four location, whether a film originated at Disney,
the purpose of the Angel of the North, the location of the Three-Fifths
Compromise in the Constitution, and who sang with Michael Jackson. The task
favors models that preserve question intent, entity identity, and answer
containment.

### Representative Failure Modes

BM25 may retrieve a passage that shares a title or entity but does not answer
the question. Dense models may retrieve semantically related passages about
the same topic but miss the requested attribute. Hybrid retrieval can recover
more positives but may mix answer-bearing passages with both lexical and
semantic distractors. Translation can also make titles or relations appear in
slightly different forms across query and passage.

### Training Data That May Help

Helpful training data includes non-overlapping open-domain QA retrieval,
Portuguese Wikipedia passage search, multilingual query-passage pairs, answer
selection, and hard-negative evidence retrieval. Hard negatives should share
entities without answering the question. Training should exclude Natural
Questions, BEIR, NanoBEIR, and translated evaluation examples.

### Model Improvement Notes

NanoNQ-pt is a compact benchmark for answer-bearing passage retrieval. Dense
retrieval is the strongest single ranking profile, while reranking hybrid
offers the best top-100 coverage. Improvements should focus on answer
containment, entity disambiguation, and rerankers that compare the question
with passage-level evidence. A practical QA retrieval system would use hybrid
candidate generation for coverage and dense or cross-encoder scoring for final
answer-aware ordering.

## Example Data

| Query | Positive document |
| --- | --- |
| Onde vai ser realizado o Final Four este ano? | O Torneio de Basquetebol Masculino da Divisão I da NCAA de 2018 foi um torneio de eliminação simples... |
| O "O Estranho Mundo de Jack" é um filme original da Disney? | O Pesadelo Antes do Natal surgiu de um poema escrito por Tim Burton em 1982, enquanto ele trabalhava como animador na Walt Disney... |
| Por que existe o Anjo do Norte? | De acordo com Gormley, o significado de um anjo era tríplice, incluindo a memória dos mineiros de carvão... |
| Onde foi originalmente mencionado o Compromisso dos Três Quintos na Constituição? | O Compromisso dos Três Quintos está no Artigo 1, Seção 2, Cláusula 3 da Constituição dos Estados Unidos... |
| Quem canta "Someone's Watching Me" com Michael Jackson? | "Somebody's Watching Me" é uma música do cantor americano Rockwell de seu álbum de estreia... |

### Public Sources

- [Natural Questions: a Benchmark for Question Answering Research](https://aclanthology.org/Q19-1026/).
- [BEIR: A Heterogeneous Benchmark for Zero-shot Evaluation of Information Retrieval Models](https://arxiv.org/abs/2104.08663).
- [MMTEB: Massive Multilingual Text Embedding Benchmark](https://arxiv.org/abs/2502.13595).
- [Zeta Alpha NanoBEIR collection](https://huggingface.co/collections/zeta-alpha-ai/nanobeir).
- [NanoBEIR-pt dataset](https://huggingface.co/datasets/hakari-bench/NanoBEIR-pt).

### Source Reference Table

| Title | Year | Type | URL |
| --- | ---: | --- | --- |
| Natural Questions: a Benchmark for Question Answering Research | 2019 | task paper | https://aclanthology.org/Q19-1026/ |
| BEIR: A Heterogeneous Benchmark for Zero-shot Evaluation of Information Retrieval Models | 2021 | benchmark paper | https://arxiv.org/abs/2104.08663 |
| MMTEB: Massive Multilingual Text Embedding Benchmark | 2025 | benchmark paper | https://arxiv.org/abs/2502.13595 |
| NanoBEIR: Smaller BEIR dataset subsets | 2024 | dataset collection | https://huggingface.co/collections/zeta-alpha-ai/nanobeir |
