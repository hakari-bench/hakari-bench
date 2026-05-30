# MNanoBEIR / NanoBEIR-pt / NanoSCIDOCS

## Overview

NanoBEIR-pt NanoSCIDOCS is a Portuguese scientific-document retrieval task
derived from SCIDOCS. Queries are translated scientific titles or short paper
descriptions, and documents are translated scientific abstracts. The task
measures related-paper retrieval rather than answer extraction: a relevant
document may share a method, research problem, citation-like relation, or
scientific contribution with the query. It is useful for evaluating whether
multilingual retrieval models can represent scholarly relatedness across
technical text, where exact title terms are helpful but do not fully define
relevance.

## Details

### What the Original Data Measures

SCIDOCS was introduced with SPECTER as an evaluation suite for scientific
document representations informed by citation links. In BEIR, it is used as a
scientific retrieval task. The MNanoBEIR Portuguese version keeps the
scientific-document retrieval objective after translation. It measures whether
models can connect a query paper or title-like description to abstracts that
are scientifically related by topic, method, or contribution.

### Observed Data Profile

This Nano subset contains 50 queries, 2,210 documents, and 244 positive qrels.
Every query is multi-positive, usually with 3 to 5 positives. The average is
4.88 positives per query, with a minimum of 3, median of 5.00, and maximum of
5. Queries average 83.02 characters, while documents average 1,028.76
characters. This creates a multi-positive scholarly retrieval problem where a
system should recover several related scientific documents, not only the
single abstract with the closest title wording.

### BM25 Evaluation Profile

BM25 uses the `bm25` top-500 candidate subset. It reaches nDCG@10 0.2911,
hit@10 0.8000, and recall@100 0.5656. Scientific terminology gives BM25 useful
anchors: method names, field terms, acronyms, and technical phrases often
repeat across related papers. The limitation is that relatedness can be
semantic or citation-like rather than lexical. Papers may use different words
for similar methods, tasks, or contributions, and BM25 can over-rank documents
that share title terms but are not the best related work.

### Dense Evaluation Profile

Dense retrieval uses the `harrier_oss_v1_270m` top-500 candidate subset. It
scores nDCG@10 0.3163, hit@10 0.8200, and recall@100 0.6393, improving over
BM25 across all reported metrics. This suggests that embedding similarity is
better at capturing scientific relatedness beyond exact term overlap. Dense
retrieval helps when a query title and an abstract share a method or problem
setting but use different wording. The remaining errors likely involve
fine-grained distinctions between same-field papers, translation artifacts in
technical terminology, and abstracts that are broadly related but not among
the judged positives.

### Reranking Hybrid Evaluation Profile

The reranking hybrid subset uses `reranking_hybrid` with top-100 candidates and
an optional rank-101 safeguard. Candidate counts range from 100 to 101, with a
mean of 100.02 and 1 safeguard row. It reaches nDCG@10 0.3201, hit@10 0.8200,
and recall@100 0.6311. Hybrid retrieval gives the best nDCG@10 and matches
dense hit@10, while dense has slightly higher recall@100. This is a balanced
profile: lexical signals preserve exact technical anchors, while dense signals
add semantic scientific relatedness. A reranker can use this mixed pool to
judge method, contribution, and domain similarity more precisely.

### Metric Interpretation for Model Researchers

Because every query has multiple positives, hit@10 only says that at least one
related document was found. Recall@100 measures whether the retrieval stage
covers the related-document set, and nDCG@10 measures whether strong positives
appear early. The observed results show that BM25 is a useful baseline but
dense and hybrid retrieval are stronger for scientific relatedness. The small
gap between dense and hybrid also makes this a useful task for studying whether
rerankers can improve candidate order without losing semantic coverage.

### Query and Relevance Type Tendencies

Queries are Portuguese translations of paper titles or compact scientific
descriptions, including power converters, sparse Gaussian Markov fields,
texture synthesis, RFID antennas, and heart-monitor design. Relevant documents
are abstracts from the same or closely related research areas. The relevance
relation is not duplicate text; it is related work. Models must connect
problem, method, and contribution even when exact terminology differs.

### Representative Failure Modes

BM25 may retrieve papers that repeat technical terms but address a different
contribution. Dense models may retrieve abstracts from the same broad field
while missing the exact method or task relationship. Hybrid retrieval may
include both useful signals but still require a domain-aware reranker. Some
examples also show translation noise in scientific text, which can make both
lexical and semantic matching less stable.

### Training Data That May Help

Helpful training data includes non-overlapping scientific-paper retrieval,
citation and co-citation ranking, related-work recommendation, title-to-
abstract retrieval, Portuguese scientific abstracts, and multilingual academic
search data. Hard negatives should come from the same field but differ in
method, dataset, or contribution. Training should exclude SCIDOCS, SPECTER
evaluation records, BEIR, NanoBEIR, and overlapping translated abstracts.

### Model Improvement Notes

NanoSCIDOCS-pt is a compact benchmark for scholarly semantic retrieval. Dense
and hybrid profiles both improve over BM25, with hybrid slightly stronger in
nDCG@10 and dense slightly stronger in recall@100. Improvements should focus on
scientific-domain representation, technical term normalization, citation-style
contrastive learning, and reranking that compares research contribution rather
than only topic similarity.

## Example Data

| Query | Positive document |
| --- | --- |
| Conversor Elevador Multinível DC-DC Novo | Os conversores de fonte de tensão multinível estão surgindo como uma nova geração de opções de conversores de energia para aplicações de alta potência... |
| Aprendizado Rápido de Campos Aleatórios de Markov Esparsos Baseado em Fatorização de Cholesky | Sure, please provide the English document text that you need translated into Portuguese. |
| Síntese de Texturas Usando Redes Neurais Convolucionais | Neste trabalho, investigamos o efeito da profundidade de redes convolucionais na sua precisão em reconhecimento de imagens em grande escala... |
| Antena anelar plana de banda larga com polarização circular para sistema RFID | Neste artigo, é proposta uma técnica de alimentação com faixa meandrante horizontal para alcançar boa adaptação de impedância... |
| Projeto de monitor cardíaco digital avançado utilizando componentes eletrônicos básicos | Neste artigo, apresentamos o design e o desenvolvimento de um novo dispositivo integrado para medir a frequência cardíaca... |

### Public Sources

- [SPECTER: Document-level Representation Learning using Citation-informed Transformers](https://arxiv.org/abs/2004.07180).
- [BEIR: A Heterogeneous Benchmark for Zero-shot Evaluation of Information Retrieval Models](https://arxiv.org/abs/2104.08663).
- [MMTEB: Massive Multilingual Text Embedding Benchmark](https://arxiv.org/abs/2502.13595).
- [Zeta Alpha NanoBEIR collection](https://huggingface.co/collections/zeta-alpha-ai/nanobeir).
- [NanoBEIR-pt dataset](https://huggingface.co/datasets/hakari-bench/NanoBEIR-pt).

### Source Reference Table

| Title | Year | Type | URL |
| --- | ---: | --- | --- |
| SPECTER: Document-level Representation Learning using Citation-informed Transformers | 2020 | task paper | https://arxiv.org/abs/2004.07180 |
| BEIR: A Heterogeneous Benchmark for Zero-shot Evaluation of Information Retrieval Models | 2021 | benchmark paper | https://arxiv.org/abs/2104.08663 |
| MMTEB: Massive Multilingual Text Embedding Benchmark | 2025 | benchmark paper | https://arxiv.org/abs/2502.13595 |
| NanoBEIR: Smaller BEIR dataset subsets | 2024 | dataset collection | https://huggingface.co/collections/zeta-alpha-ai/nanobeir |
