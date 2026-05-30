# MNanoBEIR / NanoBEIR-sr / NanoDBPedia

## Overview

NanoBEIR-sr NanoDBPedia is a Serbian entity retrieval task derived from
DBpedia-Entity. Queries are short translated entity needs, and documents are
translated DBpedia-style entity descriptions. The task is useful for studying
how retrieval models handle many-positive entity search: a query may point to
many valid entities, and a strong model should retrieve a diverse relevant set
rather than only one obvious exact-name match. It also tests whether Serbian
entity search benefits more from lexical name overlap, dense semantic category
matching, or a hybrid candidate pool.

## Details

### What the Original Data Measures

DBpedia-Entity evaluates ranking entities for information needs over DBpedia.
In BEIR, it is used as an entity retrieval task with heterogeneous query
styles, from exact names to short category-like descriptions. The MNanoBEIR
Serbian version preserves that retrieval objective after translation. It
measures whether models can connect Serbian entity needs to concise entity
descriptions using names, aliases, entity types, places, occupations, and
descriptive attributes.

### Observed Data Profile

This Nano subset contains 50 queries, 6,045 documents, and 1,158 positive
qrels. It is strongly multi-positive: the average is 23.16 positives per query,
with a minimum of 1, median of 18.00, and maximum of 81. There are 48
multi-positive queries, covering 96.0% of the task. Queries are short at 41.18
characters on average, while documents average 338.86 characters. This creates
a broad entity search setting where recall and ranking diversity matter more
than finding a single match.

### BM25 Evaluation Profile

BM25 uses the `bm25` top-500 candidate subset. It reaches nDCG@10 0.4704,
hit@10 0.9000, and recall@100 0.5458. The high hit@10 shows that lexical
entity cues are strong: names, locations, and category terms often survive
translation and appear directly in relevant descriptions. The lower recall
shows that exact overlap does not cover the full positive set. BM25 can
over-rank descriptions that share a name or term while missing entities that
satisfy the query through type, location, or descriptive similarity.

### Dense Evaluation Profile

Dense retrieval uses the `harrier_oss_v1_270m` top-500 candidate subset. It
scores nDCG@10 0.5693, hit@10 0.9400, and recall@100 0.7150, clearly
outperforming BM25. Dense retrieval is stronger because many entity needs are
category or attribute based rather than exact-name lookups. It can connect
queries about former republics, films shot in a place, architecture, or
collections to relevant entity descriptions even when wording differs. The
remaining difficulty is constraint satisfaction: semantically close entities
may fail a specific place, type, or time condition.

### Reranking Hybrid Evaluation Profile

The reranking hybrid subset uses `reranking_hybrid` with exactly 100 candidates
per query and no safeguard rows. It reaches nDCG@10 0.5567, hit@10 0.9600, and
recall@100 0.6883. The hybrid pool has the best hit@10, while dense retrieval
has stronger nDCG@10 and recall@100. This means combining lexical and dense
signals helps ensure at least one relevant entity appears early, but dense
ordering is slightly better for ranking many relevant entities and covering the
positive set. A reranker can use the hybrid pool to balance exact entity
anchors with semantic category matching.

### Metric Interpretation for Model Researchers

Because most queries have many positives, hit@10 should be interpreted as a
minimal first-page success measure, not full retrieval quality. Recall@100
shows how much of the relevant entity set is available, and nDCG@10 reflects
whether useful entities are ranked early. The dense profile is strongest for
coverage and early ranking, while reranking hybrid slightly improves first-page
presence. This task helps separate exact entity-name retrieval from semantic
entity-set retrieval.

### Query and Relevance Type Tendencies

Queries include exact or near-exact entity references, short category phrases,
and location-constrained needs. Relevant documents are compact entity
descriptions with names, types, dates, locations, and identifying facts.
Examples include an auto dealership, Alice Munro, Gallo-Roman architecture in
Paris, former Yugoslav republics, and films shot in Venice. The task favors
models that preserve entity identity while also matching categories and
attributes.

### Representative Failure Modes

BM25 may retrieve entities with overlapping names or rare terms but the wrong
type or relation. Dense models may retrieve semantically related entities that
violate a constraint such as place, category, or period. Hybrid retrieval can
raise first-page success but still needs constraint-aware reranking. Serbian
translation can also vary proper-name transliteration and category wording,
which affects both lexical and dense matching.

### Training Data That May Help

Helpful training data includes non-overlapping entity search, Serbian
Wikipedia or DBpedia retrieval, alias matching, multilingual entity linking,
and short-query to entity-description ranking. Hard negatives should share
entity types, places, occupations, or names while violating one query
constraint. Training should exclude DBpedia-Entity, BEIR, NanoBEIR, and any
translated duplicate evaluation records.

### Model Improvement Notes

NanoDBPedia-sr is a compact benchmark for entity-oriented retrieval. Dense
retrieval is the strongest single profile, while reranking hybrid gives the
highest hit@10. Improvements should focus on Serbian entity names and aliases,
type and attribute constraints, and reranking that diversifies many-positive
entity results. A practical entity search system would combine hybrid recall
with a constraint-aware reranker.

## Example Data

| Query | Positive document |
| --- | --- |
| Fitzgerald auto salon Chambersburg Pennsylvania | Fitzgerald Auto Malls je porodična auto-kompanija koja je osnovana 1966. godine, a prva lokacija otvorena je u Bethesdi... |
| Zbirka kratkih priča iz 1994. godine "Alice Munro je Otvorena" | Aliсe En Manro je kanadska spisateljica. Manrin rad je opisan kao revolucionaran u arhitekturi kratkih priča... |
| galsko-rimska arhitektura u Parizu | Umetnost u Parizu je članak o umetničkoj kulturi i istoriji u Parizu, glavnom gradu Francuske... |
| Republike bivše Jugoslavije | Ustav Jugoslavije iz 1974. bio je četvrti i poslednji ustav Socijalističke Federativne Republike Jugoslavije... |
| filmovi snimljeni u Veneciji | "Mala Romansa" je američki romantični komad iz 1979. godine, snimljen u tehnikoloru i panavizionu... |

### Public Sources

- [DBpedia Entity Retrieval](https://doi.org/10.1145/3077136.3080751).
- [BEIR: A Heterogeneous Benchmark for Zero-shot Evaluation of Information Retrieval Models](https://arxiv.org/abs/2104.08663).
- [MMTEB: Massive Multilingual Text Embedding Benchmark](https://arxiv.org/abs/2502.13595).
- [Zeta Alpha NanoBEIR collection](https://huggingface.co/collections/zeta-alpha-ai/nanobeir).
- [NanoBEIR-sr dataset](https://huggingface.co/datasets/hakari-bench/NanoBEIR-sr).

### Source Reference Table

| Title | Year | Type | URL |
| --- | ---: | --- | --- |
| DBpedia Entity Retrieval | 2017 | task paper | https://doi.org/10.1145/3077136.3080751 |
| BEIR: A Heterogeneous Benchmark for Zero-shot Evaluation of Information Retrieval Models | 2021 | benchmark paper | https://arxiv.org/abs/2104.08663 |
| MMTEB: Massive Multilingual Text Embedding Benchmark | 2025 | benchmark paper | https://arxiv.org/abs/2502.13595 |
| NanoBEIR: Smaller BEIR dataset subsets | 2024 | dataset collection | https://huggingface.co/collections/zeta-alpha-ai/nanobeir |
