# MNanoBEIR / NanoBEIR-es / NanoDBPedia

## Overview

This task is the Spanish NanoBEIR version of DBpedia-Entity, an entity search benchmark built from DBpedia pages and heterogeneous entity-oriented queries. The original DBpedia-Entity collection evaluates whether systems can retrieve the intended entity pages for short information needs, category requests, aliases, and property-based descriptions. In this NanoBEIR slice, Spanish translated entity queries must retrieve Spanish translated DBpedia-style entity descriptions from 6,045 documents. The task contains 50 queries and 1,158 positive relevance judgments, with an average of 23.16 positives per query. It is therefore a many-positive entity retrieval task that stresses entity disambiguation, category matching, and ranking among many plausible same-type entities.

## Details

### What the Original Data Measures

DBpedia-Entity measures entity search rather than ordinary passage answer retrieval. A query may name a person, class, location, work, organization, or property constraint, and relevant documents are entity descriptions that satisfy that need. Because many queries are short and many positives can exist, the task evaluates whether a model can retrieve a useful set of entity pages while ranking the most relevant entities early.

### Observed Data Profile

The Spanish Nano task has 50 queries, 6,045 documents, and 1,158 positives. Positives per query average 23.16, with a median of 18 and a maximum of 81. Query length averages about 38 characters, while document descriptions average about 368 characters. The examples include a car dealership in Chambersburg, an Alice Munro short-story collection, Gallo-Roman architecture in Paris, former Yugoslav republics, and films shot in Venice. Documents are compact entity summaries.

### BM25 Evaluation Profile

BM25 is very strong, with nDCG@10 of 0.614, Hit@10 of 0.960, and Recall@100 of 0.677. This reflects the entity-search nature of the task: names, locations, categories, and descriptive properties often overlap directly between query and entity descriptions. Short queries containing rare entity names or category phrases are especially favorable to sparse matching. The remaining challenge is ranking among many same-type entities and handling ambiguous or broad entity needs.

### Dense Evaluation Profile

The dense harrier-oss-270m baseline is nearly tied on top-10 quality, with nDCG@10 of 0.610, Hit@10 of 0.940, and Recall@100 of 0.706. Dense retrieval improves recall, indicating that embeddings help recover entities whose descriptions are semantically related even when exact terms differ. However, dense ranking does not clearly beat BM25 at the top, because entity search strongly rewards exact names and category words. Dense retrieval is most useful for broader category or property queries.

### Reranking Hybrid Evaluation Profile

The reranking_hybrid profile is best overall, with nDCG@10 of 0.621, Hit@10 of 0.940, and Recall@100 of 0.726. It combines BM25's strong exact entity and category matching with dense retrieval's broader semantic coverage. The gains are modest but consistent with an entity task that benefits from both signals. Hybrid search is particularly useful when a query has many positives: it can surface more relevant entity pages while still ranking direct lexical matches highly.

### Metric Interpretation for Model Researchers

Hit@10 is high for all profiles and should be treated as a coarse sanity check. nDCG@10 captures how well the retriever orders relevant entity pages near the top. Recall@100 is important because most queries have many positives, and a strong system should retrieve a broad entity set rather than only one match. The hybrid profile's higher recall suggests better candidate coverage, while the close nDCG scores show that the top of the ranking is already dominated by strong lexical and entity cues.

### Query and Relevance Type Tendencies

Queries are short entity information needs: names, categories, geographic constraints, works by an author, or entities with a property. Relevant documents are DBpedia-style summaries. Many hard negatives are same-type entities that share class terms but miss a required attribute such as location, creator, publication history, or filming place. The task rewards entity normalization and attribute-aware ranking.

### Representative Failure Modes

BM25 can over-rank entities that repeat category terms but do not satisfy the query constraint. Dense retrieval can retrieve semantically similar entity types while missing a named constraint. Hybrid retrieval improves coverage but can still rank generic same-class entities above the intended set. Failure analysis should check which query attribute is being ignored.

### Training and Leakage Considerations

Training should exclude DBpedia-Entity, BEIR, NanoBEIR, and translated DBpedia records likely to overlap with these queries or entity pages. Useful non-overlapping data includes entity search datasets, knowledge-base page retrieval pairs, Spanish or multilingual entity linking data, and hard negatives from same-type entities. Multi-positive training is recommended because most queries have many valid entity pages.

### Model Improvement Signals

Strong models should preserve exact entity names while learning attribute and category matching. Useful training signals include alias handling, entity-description contrastive learning, same-type hard negatives, and multilingual knowledge-base retrieval pairs. Hybrid systems are a good fit because sparse search captures names and dense search recovers semantically matching entity descriptions.

## Example Data

| Query | Positive Document |
|---|---|
| Concesionario Fitzgerald en Chambersburg, PA | Fitzgerald Auto Malls es una concesionaria de automóviles propiedad y operada por una familia, fundada en 1966... |
| Colección de cuentos de 1994 de Alice Munro está disponible | Alice Ann Munro es una autora canadiense. La obra de Munro ha sido descrita como haber revolucionado la estructura de los cuentos... |
| Arquitectura romana gala en París | El arte en París es un artículo sobre la cultura y la historia del arte en París, la capital de Francia... |
| Repúblicas de la antigua Yugoslavia | La Constitución de 1974 de Yugoslavia fue la cuarta y última constitución de la República Federal Socialista de Yugoslavia... |
| Películas filmadas en Venecia | A Little Romance es una comedia romántica estadounidense de 1979 dirigida por George Roy Hill... |

## Public Sources

- [DBpedia-Entity V2 paper](https://doi.org/10.1145/3077136.3080751)
- [BEIR benchmark](https://github.com/beir-cellar/beir)
- [MMTEB benchmark](https://arxiv.org/abs/2502.13595)
- [NanoBEIR dataset](https://huggingface.co/collections/zeta-alpha-ai/nanobeir)

## Source Reference Table

| Label | URL |
|---|---|
| DBpedia-Entity V2 paper | https://doi.org/10.1145/3077136.3080751 |
| BEIR benchmark | https://github.com/beir-cellar/beir |
| MMTEB benchmark | https://arxiv.org/abs/2502.13595 |
| NanoBEIR dataset | https://huggingface.co/collections/zeta-alpha-ai/nanobeir |
