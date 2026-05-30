# MNanoBEIR / NanoBEIR-no / NanoDBPedia

## Overview

NanoBEIR-no NanoDBPedia is a Norwegian entity retrieval task derived from
DBpedia-Entity. Queries are short entity needs, including names, descriptions,
categories, and natural-language requests, and the target documents are
translated DBpedia entity descriptions. The task is useful for studying how
retrieval systems behave when the query is compact but the relevant set is
large. It also separates exact entity-name matching from broader entity search:
some queries can be solved with surface overlap, while others require mapping a
category or description to many plausible entities.

## Details

### What the Original Data Measures

DBpedia-Entity evaluates search over structured encyclopedic entities from
DBpedia. In BEIR, it is framed as an entity retrieval benchmark where systems
must retrieve entities relevant to a short user query. The MNanoBEIR Norwegian
version keeps the same retrieval goal while using translated Norwegian query
and document text. This makes it a multilingual test of entity recognition,
entity type matching, and short-query semantic retrieval over compact knowledge
base descriptions.

### Observed Data Profile

This Nano subset contains 50 queries, 6,045 documents, and 1,158 positive qrels.
It is strongly multi-positive: the average is 23.16 positives per query, with a
minimum of 1, median of 18.00, and maximum of 81. There are 48 multi-positive
queries, covering 96.0% of the task. Queries are very short at 36.86 characters
on average, while documents are concise entity descriptions averaging 331.00
characters. This creates a broad-recall retrieval setting: many entities can be
valid for a single query, and ranking should surface several good candidates
early rather than only one exact match.

### BM25 Evaluation Profile

BM25 uses the `bm25` top-500 candidate subset. It reaches nDCG@10 0.4684,
hit@10 0.8400, and recall@100 0.5173. These scores show that lexical matching
is a strong baseline for entity retrieval. Entity names, locations, titles, and
category words often appear directly in both query and document, allowing BM25
to recover many relevant records. The limitation is coverage and ordering
within broad categories. When a query describes "films shot in Venice" or
"former Yugoslav republics," many documents may share only partial lexical
evidence, and BM25 may rank exact word matches above entities that are
semantically valid but phrased differently.

### Dense Evaluation Profile

Dense retrieval uses the `harrier_oss_v1_270m` top-500 candidate subset. It
scores nDCG@10 0.5506, hit@10 0.9000, and recall@100 0.6468, improving over
BM25 on every metric. The gain is expected for short descriptive entity
queries: embedding similarity can connect category wording and entity
descriptions even when the same terms are not repeated. Dense retrieval is also
better suited to many-positive queries because it can cluster entities by type,
place, period, or topic rather than depending only on exact surface forms. The
task still has hard negatives, especially entities from the same class or
knowledge graph neighborhood, so semantic similarity alone does not solve final
ordering.

### Reranking Hybrid Evaluation Profile

The reranking hybrid subset uses `reranking_hybrid` with exactly 100 candidates
per query and no safeguard rows. It reaches nDCG@10 0.5184, hit@10 0.9200, and
recall@100 0.6373. The hybrid profile has the best hit@10, nearly matches dense
recall@100, and sits between BM25 and dense for nDCG@10. This indicates that a
combined lexical-semantic pool is useful for ensuring at least one relevant
entity appears in the first page, while the dense ordering is slightly stronger
for ranking multiple relevant entities near the top. For reranker evaluation,
this candidate set is valuable because it contains both exact-name candidates
and semantically related entities that a final model must distinguish.

### Metric Interpretation for Model Researchers

Because there are many positives per query, hit@10 is a weak success signal by
itself: a model may hit one relevant entity while still missing most of the
valid set. nDCG@10 captures early ranking quality, and recall@100 captures how
well the retrieval stage covers the relevant entity pool. The dense and hybrid
results show that semantic matching improves coverage beyond BM25, but BM25's
relatively high hit@10 confirms that lexical entity evidence remains important.
Strong systems should therefore be judged on whether they retrieve diverse
relevant entities for each query, not just whether they find a single obvious
name match.

### Query and Relevance Type Tendencies

Queries range from exact or near-exact entity names to short category
descriptions and natural-language entity requests. Relevant documents are short
DBpedia-style summaries with names, types, dates, locations, and identifying
attributes. Some queries point to a single entity, while many identify a class
of entities. This favors models that can combine entity linking behavior with
category retrieval. It also rewards multilingual robustness, since translated
entity descriptions may preserve names but vary in how categories and
attributes are phrased.

### Representative Failure Modes

BM25 may over-rank documents that repeat rare query terms but are not valid
entities for the requested category. Dense models may retrieve entities that
are semantically close but fail a specific constraint such as place, year,
author, or type. Hybrid retrieval may broaden the pool but still require a
reranker to enforce all constraints in the query. Multi-positive evaluation
also exposes diversity failures: a model can fill the top ranks with closely
related entities while missing other valid subtypes or examples.

### Training Data That May Help

Helpful training data includes entity search, entity linking, Wikipedia and
DBpedia retrieval, multilingual knowledge base search, and short-query to
description matching. Hard negatives should be entities from the same class,
location, or surface-name neighborhood that violate one query constraint.
Training should avoid overlap with DBpedia-Entity, BEIR, NanoBEIR, and
translated DBpedia records that may appear in this benchmark.

### Model Improvement Notes

This task is a compact diagnostic for entity-oriented retrieval. Dense
retrieval is the strongest single profile for early ranking and coverage, while
reranking hybrid has the highest hit@10 and provides a good candidate pool for
downstream rerankers. Improvements should focus on constraint satisfaction,
entity type representation, multilingual entity descriptions, and diversified
ranking for many-positive queries. For production-style entity search, a
hybrid first stage followed by a reranker that checks type, attribute, and
category constraints would be the most natural architecture.

## Example Data

| Query | Positive document |
| --- | --- |
| Fitzgerald bilutstillingssenter i Chambersburg, PA | Fitzgerald Auto Malls er en familieeid og drevet bilforhandler som ble grunnlagt i 1966, med sin første lokalisering åpnet i Bethesda, Maryland... |
| Hvor kan jeg finne samlingen av kortfortellinger fra 1994 av Alice Munro? | Alice Ann Munro er en kanadisk forfatter. Munros arbeid er blitt beskrevet som å ha revolusjonert kortprosasjangeren... |
| Galloromersk arkitektur i Paris | Kunst i Paris er en artikkel om kunstkulturen og historien i Paris, Frankrikes hovedstad... |
| De tidligere jugoslaviske republikkene | Den jugoslaviske grunnloven av 1974 var den fjerde og siste grunnloven for Den sosialistiske føderale republikken Jugoslavia... |
| Filmer innspilt i Venezia | En liten romanse er en amerikansk romantisk komedie fra 1979, innspilt i Technicolor og Panavision... |

### Public Sources

- [DBpedia-Entity V2](https://doi.org/10.1145/3077136.3080751).
- [BEIR: A Heterogeneous Benchmark for Zero-shot Evaluation of Information Retrieval Models](https://arxiv.org/abs/2104.08663).
- [MMTEB: Massive Multilingual Text Embedding Benchmark](https://arxiv.org/abs/2502.13595).
- [Zeta Alpha NanoBEIR collection](https://huggingface.co/collections/zeta-alpha-ai/nanobeir).
- [NanoBEIR-no dataset](https://huggingface.co/datasets/hakari-bench/NanoBEIR-no).

### Source Reference Table

| Title | Year | Type | URL |
| --- | ---: | --- | --- |
| DBpedia-Entity V2 | 2017 | task paper | https://doi.org/10.1145/3077136.3080751 |
| BEIR: A Heterogeneous Benchmark for Zero-shot Evaluation of Information Retrieval Models | 2021 | benchmark paper | https://arxiv.org/abs/2104.08663 |
| MMTEB: Massive Multilingual Text Embedding Benchmark | 2025 | benchmark paper | https://arxiv.org/abs/2502.13595 |
| NanoBEIR: Smaller BEIR dataset subsets | 2024 | dataset collection | https://huggingface.co/collections/zeta-alpha-ai/nanobeir |
