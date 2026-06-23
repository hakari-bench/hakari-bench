# MNanoBEIR / NanoBEIR-pt / NanoDBPedia

## Overview

NanoBEIR-pt NanoDBPedia is a Portuguese entity retrieval task derived from
DBpedia-Entity. Queries are short keyword or natural-language entity needs, and
documents are translated DBpedia-style entity descriptions. The task is useful
for evaluating entity search under many-positive relevance: a query may have
many valid entities, and a good system should retrieve a diverse set of
matching descriptions rather than only the most obvious name match. It also
tests how well multilingual retrieval models combine exact entity cues with
broader semantic category matching.

## Details

### What the Original Data Measures

DBpedia-Entity evaluates ranking entities for information needs over DBpedia.
In BEIR, the dataset is used as an entity retrieval task with heterogeneous
queries ranging from exact names to category-like descriptions. The MNanoBEIR
Portuguese version preserves this objective after translation. It measures
whether a retriever can match Portuguese entity needs to concise entity
descriptions by using names, aliases, locations, occupations, types, and
descriptive attributes.

### Observed Data Profile

This Nano subset contains 50 queries, 6,045 documents, and 1,158 positive
qrels. It is strongly multi-positive: the average is 23.16 positives per query,
with a minimum of 1, median of 18.00, and maximum of 81. There are 48
multi-positive queries, covering 96.0% of the task. Queries are short at 36.62
characters on average, while documents average 354.37 characters. This makes
the task a high-coverage entity search benchmark rather than a single-answer
retrieval problem.

### BM25 Evaluation Profile

BM25 uses the `bm25` top-500 candidate subset. It reaches nDCG@10 0.5110,
hit@10 0.9200, and recall@100 0.6114. Entity search is favorable to lexical
retrieval because names, places, and category terms often appear directly in
both query and document. The high hit@10 confirms that BM25 is very effective
at finding at least one relevant entity. The harder part is ranking many valid
entities and covering the broader positive set. BM25 can overvalue exact term
overlap and miss descriptions that satisfy the query through type or attribute
matching rather than direct wording.

### Dense Evaluation Profile

Dense retrieval uses the `harrier_oss_v1_270m` top-500 candidate subset. It
scores nDCG@10 0.5816, hit@10 0.9200, and recall@100 0.6865. Dense retrieval
improves ranking and coverage over BM25 while matching its first-page hit
rate. This suggests that embedding similarity is better at capturing entity
type, category, and attribute relationships that are not expressed with the
same surface words. Dense retrieval is particularly helpful for category-style
queries such as films, republics, architecture, or collections, where the
relevant entities may share meaning more than exact vocabulary.

### Reranking Hybrid Evaluation Profile

The reranking hybrid subset uses `reranking_hybrid` with exactly 100 candidates
per query and no safeguard rows. It reaches nDCG@10 0.5620, hit@10 0.9600, and
recall@100 0.7098. The hybrid profile has the best hit@10 and recall@100,
while dense retrieval has the best nDCG@10. This shows that lexical and dense
signals are complementary for Portuguese entity search: hybrid retrieval brings
more positives into the candidate pool, but dense ordering is slightly cleaner
near the top. A reranker can use the hybrid pool to improve both coverage and
early ordering.

### Metric Interpretation for Model Researchers

Because each query often has many positives, hit@10 is not enough to evaluate
success. Recall@100 shows how much of the relevant entity set is available,
and nDCG@10 shows whether useful entities appear early. The observed scores
show that BM25 is strong for exact entity cues, dense retrieval improves
semantic category matching, and reranking hybrid gives the broadest top-100
coverage. This task is therefore useful for separating exact-name retrieval
from true entity set retrieval.

### Query and Relevance Type Tendencies

Queries include exact or near-exact entity references, short category
descriptions, and natural-language requests. Relevant documents are compact
entity descriptions containing names, types, locations, dates, or identifying
facts. Examples include an auto mall, Alice Munro, Gallo-Roman architecture in
Paris, former Yugoslav republics, and films shot in Venice. The task favors
models that preserve both surface entity clues and semantic constraints.

### Representative Failure Modes

BM25 may retrieve descriptions that repeat a rare name or category word but do
not satisfy the full entity need. Dense systems may retrieve semantically
related entities that fail a specific location, type, or time constraint.
Hybrid systems improve coverage but may still require reranking to diversify
and enforce constraints. Translation can also alter category wording while
preserving names, making exact lexical matching uneven across query types.

### Training Data That May Help

Helpful training data includes non-overlapping entity search, Wikipedia and
DBpedia retrieval, alias matching, multilingual entity linking, and
short-query to entity-description ranking. Hard negatives should share entity
types, places, occupations, or names while violating one query constraint.
Training should exclude DBpedia-Entity, BEIR, NanoBEIR, and translated
duplicate evaluation records.

### Model Improvement Notes

NanoDBPedia-pt is a strong benchmark for entity-oriented retrieval. Dense
retrieval is the best early ranker, while reranking hybrid gives the best
coverage and first-page success. Improvements should focus on entity type
representation, alias and attribute handling, and reranking that checks
constraints rather than only broad semantic similarity. A production entity
search system would likely use hybrid candidates followed by a constraint-aware
reranker.

## Example Data

| Query | Positive document |
| --- | --- |
| Fitzgerald Auto Mall em Chambersburg, PA [40 chars] | Fitzgerald Auto Malls é uma concessionária de automóveis de propriedade e operação familiar fundada em 1966, com sua primeira localização abrindo em Bethesda, Maryland. Em 2014, a Fitzgerald Auto Mall... [200 / 436 chars] |
| Coleção de contos de 1994 de Alice Munro está disponível [56 chars] | Alice Ann Munro (nascida Laidlaw; 10 de julho de 1931) é uma autora canadense. O trabalho de Munro é frequentemente descrito como tendo revolucionado a arquitetura dos contos, especialmente por sua te... [200 / 528 chars] |
| Arquitetura galo-romana em Paris [32 chars] | A Arte em Paris é um artigo sobre a cultura e a história da arte em Paris, a capital da França. Há séculos, Paris atrai artistas de todo o mundo, que chegam à cidade para se educarem e buscar inspiraç... [200 / 306 chars] |
| Repúblicas da antiga Iugoslávia [31 chars] | A Constituição de 1974 da Iugoslávia foi a quarta e última constituição da República Federal Socialista da Iugoslávia. Ela entrou em vigor em 21 de fevereiro. Com 406 artigos originais, a constituição... [200 / 440 chars] |
| Filmes filmados em Veneza [25 chars] | A Pequena Romântica é um filme de comédia romântica americano de 1979, em Technicolor e Panavision, dirigido por George Roy Hill e estrelado por Laurence Olivier, Thelonious Bernard e Diane Lane, em s... [200 / 391 chars] |

### Public Sources

- [DBpedia Entity Retrieval](https://doi.org/10.1145/3077136.3080751).
- [BEIR: A Heterogeneous Benchmark for Zero-shot Evaluation of Information Retrieval Models](https://arxiv.org/abs/2104.08663).
- [MMTEB: Massive Multilingual Text Embedding Benchmark](https://arxiv.org/abs/2502.13595).
- [Zeta Alpha NanoBEIR collection](https://huggingface.co/collections/zeta-alpha-ai/nanobeir).
- [NanoBEIR-pt dataset](https://huggingface.co/datasets/hakari-bench/NanoBEIR-pt).

### Source Reference Table

| Title | Year | Type | URL |
| --- | ---: | --- | --- |
| DBpedia Entity Retrieval | 2017 | task paper | [https://doi.org/10.1145/3077136.3080751](https://doi.org/10.1145/3077136.3080751) |
| BEIR: A Heterogeneous Benchmark for Zero-shot Evaluation of Information Retrieval Models | 2021 | benchmark paper | [https://arxiv.org/abs/2104.08663](https://arxiv.org/abs/2104.08663) |
| MMTEB: Massive Multilingual Text Embedding Benchmark | 2025 | benchmark paper | [https://arxiv.org/abs/2502.13595](https://arxiv.org/abs/2502.13595) |
| NanoBEIR: Smaller BEIR dataset subsets | 2024 | dataset collection | [https://huggingface.co/collections/zeta-alpha-ai/nanobeir](https://huggingface.co/collections/zeta-alpha-ai/nanobeir) |
