# MNanoBEIR / NanoBEIR-pt / NanoFEVER

## Overview

NanoBEIR-pt NanoFEVER is a Portuguese factual-claim evidence retrieval task
derived from FEVER. Queries are short translated claims, and documents are
translated Wikipedia-style evidence passages. The retrieval objective is to
find the passage that can verify the claim before any support or refute label
is assigned. This task is useful for evaluating whether multilingual retrieval
systems can combine exact named-entity matching with semantic evidence
matching over long encyclopedic passages.

## Details

### What the Original Data Measures

FEVER was built for fact extraction and verification over Wikipedia. In BEIR,
the retrieval stage is evaluated separately: systems must retrieve evidence
for factual claims. The MNanoBEIR Portuguese version keeps that evidence
retrieval structure in a compact translated setting. It measures whether a
retriever can connect a short Portuguese claim to the Wikipedia passage that
contains the fact needed for verification, including cases involving entities,
titles, locations, genres, or historical relations.

### Observed Data Profile

This Nano subset contains 50 queries, 4,996 documents, and 57 positive qrels.
Most queries have one positive, with a small multi-positive tail. The average
is 1.14 positives per query, with a minimum of 1, median of 1.00, and maximum
of 3. Six queries are multi-positive, representing 12.0% of the task. Queries
average 49.04 characters, while documents average 1,245.71 characters. This
creates a short-claim to long-evidence retrieval setting where precise early
ranking matters.

### BM25 Evaluation Profile

BM25 uses the `bm25` top-500 candidate subset. It reaches nDCG@10 0.8043,
hit@10 0.9400, and recall@100 1.0000. This is an extremely strong lexical
baseline. Portuguese translated FEVER claims often preserve named entities,
titles, and distinctive factual phrases that appear in the evidence passage.
BM25 therefore recovers every positive within the top 100 candidates and
usually ranks a positive in the top 10. The remaining challenge is fine
ordering: term overlap can still retrieve nearby entity pages or related
passages that do not verify the exact claim.

### Dense Evaluation Profile

Dense retrieval uses the `harrier_oss_v1_270m` top-500 candidate subset. It
scores nDCG@10 0.8461, hit@10 0.9600, and recall@100 0.9649. Dense retrieval
has better top-10 ranking than BM25 but slightly lower recall@100. This pattern
shows the tradeoff between semantic ordering and exact lexical coverage.
Embedding similarity is very effective at placing the best evidence high when
the claim and passage are semantically aligned, but it may miss a few
positives that are easier to recover through exact entity or title matching.

### Reranking Hybrid Evaluation Profile

The reranking hybrid subset uses `reranking_hybrid` with exactly 100 candidates
per query and no safeguard rows. It reaches nDCG@10 0.8511, hit@10 0.9800, and
recall@100 1.0000, making it the strongest profile overall. The hybrid result
combines BM25's complete coverage with dense retrieval's stronger semantic
ranking. This is an ideal case for hybrid retrieval: lexical matching captures
names and titles, while dense similarity improves claim-evidence ordering.
For reranking experiments, this candidate pool gives full access to positives
and already strong first-page quality.

### Metric Interpretation for Model Researchers

Because most queries have a single positive, hit@10 is close to a query-level
success measure, and recall@100 shows whether the evidence is available to a
reranker. nDCG@10 is the most sensitive top-rank signal. The observed pattern
is clear: BM25 provides complete coverage, dense retrieval improves ranking,
and reranking hybrid combines both advantages. For model research, this task
is a strong example of why FEVER-style evidence retrieval benefits from
lexical entity preservation and semantic claim matching together.

### Query and Relevance Type Tendencies

Queries are short factual claims about people, television series, cities,
historical figures, and films. Relevant documents are Wikipedia passages that
contain the verification evidence. Examples include claims about Keith
Godchaux and the Grateful Dead, an Indian sitcom, advanced aircraft in
Burbank, Nero, and the film Scream 2. The task favors models that understand
entity identity, aliases, title matching, and factual relations.

### Representative Failure Modes

BM25 may retrieve a passage with the right entity but the wrong fact. Dense
models may retrieve semantically related evidence about a nearby entity or
work, especially when the claim is short and ambiguous. Hybrid retrieval
reduces both errors but can still require reranking to check whether the
passage actually verifies the claim. Translation can create small mismatches
in titles, names, or relation wording, which makes preserving both lexical and
semantic signals important.

### Training Data That May Help

Helpful training data includes non-overlapping claim-evidence retrieval,
Wikipedia evidence mining, multilingual fact-checking, entity-centric QA, and
Portuguese factual claim pairs. Hard negatives should come from related
entities, same-title passages, or neighboring events that share terms but fail
to verify the claim. Training should exclude FEVER, BEIR, NanoBEIR, and direct
translations of evaluation claims or evidence pages.

### Model Improvement Notes

NanoFEVER-pt is a high-scoring but still informative evidence retrieval task.
The hybrid profile is strongest because it keeps complete lexical coverage and
adds semantic ordering. Improvements should focus on claim-specific reranking,
entity disambiguation, alias handling, and relation matching. In practical
systems, this task supports a hybrid-first architecture followed by a reranker
that verifies whether a passage contains the exact evidence requested by the
claim.

## Example Data

| Query | Positive document |
| --- | --- |
| Keith Godchaux conhecia o Grateful Dead. | A Grateful Dead foi uma banda de rock americana formada em 1965 em Palo Alto, Califórnia... |
| Taarak Mehta Ka Ooltah Chashmah é uma sitcom. | Taarak Mehta Ka Ooltah Chashmah é a sitcom mais longa da Índia, produzida pela Neela Tele Films Private Limited... |
| Aviões secretos e avançados foram fabricados em Burbank, Califórnia. | Burbank é uma cidade no Condado de Los Angeles, no sul da Califórnia, Estados Unidos... |
| Nero é uma pessoa. | A dinastia Júlio-Cláudia refere-se aos primeiros cinco imperadores romanos, incluindo Augusto, Tibério, Calígula, Cláudio e Nero... |
| Scream 2 é um filme exclusivamente alemão. | Scream 2 é um filme de terror americano de 1997 dirigido por Wes Craven e escrito por Kevin Williamson... |

### Public Sources

- [FEVER: a Large-scale Dataset for Fact Extraction and VERification](https://arxiv.org/abs/1803.05355).
- [BEIR: A Heterogeneous Benchmark for Zero-shot Evaluation of Information Retrieval Models](https://arxiv.org/abs/2104.08663).
- [MMTEB: Massive Multilingual Text Embedding Benchmark](https://arxiv.org/abs/2502.13595).
- [Zeta Alpha NanoBEIR collection](https://huggingface.co/collections/zeta-alpha-ai/nanobeir).
- [NanoBEIR-pt dataset](https://huggingface.co/datasets/hakari-bench/NanoBEIR-pt).

### Source Reference Table

| Title | Year | Type | URL |
| --- | ---: | --- | --- |
| FEVER: a Large-scale Dataset for Fact Extraction and VERification | 2018 | task paper | https://arxiv.org/abs/1803.05355 |
| BEIR: A Heterogeneous Benchmark for Zero-shot Evaluation of Information Retrieval Models | 2021 | benchmark paper | https://arxiv.org/abs/2104.08663 |
| MMTEB: Massive Multilingual Text Embedding Benchmark | 2025 | benchmark paper | https://arxiv.org/abs/2502.13595 |
| NanoBEIR: Smaller BEIR dataset subsets | 2024 | dataset collection | https://huggingface.co/collections/zeta-alpha-ai/nanobeir |
