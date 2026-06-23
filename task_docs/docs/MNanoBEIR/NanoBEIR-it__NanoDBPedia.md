# MNanoBEIR / NanoBEIR-it / NanoDBPedia

## Overview

This task is the Italian NanoBEIR version of DBpedia-Entity, an entity retrieval benchmark built from DBpedia entity pages and heterogeneous entity-oriented queries. The original DBpedia-Entity collection evaluates whether systems can retrieve entity descriptions for names, aliases, categories, and property-based information needs. In this NanoBEIR slice, Italian translated entity-style queries must retrieve Italian translated DBpedia passages or entity descriptions from 6,045 candidate documents. The task contains 50 queries and 1,158 positive relevance judgments, with an average of 23.16 positives per query. It is a many-positive entity retrieval benchmark that tests exact name matching, category search, attribute disambiguation, and broad entity-set recall.

## Details

### What the Original Data Measures

DBpedia-Entity measures entity search rather than answer passage retrieval. A query may name an entity, describe a class of entities, or ask for entities with a property such as location, creator, publication history, or filming place. Relevant documents are entity descriptions that satisfy the information need. Because most queries have many positives, the benchmark evaluates both first-page quality and coverage of the relevant entity set.

### Observed Data Profile

The Italian Nano task has 50 queries, 6,045 documents, and 1,158 positives. Positives per query average 23.16, with a median of 18 and a maximum of 81. Forty-eight queries are multi-positive. Queries are short, averaging about 38 characters, and documents are compact, averaging about 362 characters. Examples include Fitzgerald Auto Mall in Chambersburg, Alice Munro's 1994 story collection, Gallo-Roman architecture in Paris, former Yugoslav republics, and films shot in Venice.

### BM25 Evaluation Profile

BM25 is strong but not dominant, with nDCG@10 of 0.534, Hit@10 of 0.940, and Recall@100 of 0.602. Sparse retrieval works well when entity names, locations, or category terms repeat directly. It struggles more with broader category or property queries where relevant entities may not share the exact wording. Because the task is highly multi-positive, retrieving one entity is not enough.

### Dense Evaluation Profile

The dense harrier-oss-270m baseline is strongest, with nDCG@10 of 0.643, Hit@10 of 1.000, and Recall@100 of 0.732. Dense retrieval improves both ranking and recall, showing that semantic entity-description matching is valuable in this Italian slice. It can recover entities that satisfy a category or property need even when the surface wording differs. Exact names still help, but dense similarity provides the best direct retrieval profile here.

### Reranking Hybrid Evaluation Profile

The reranking_hybrid profile reaches nDCG@10 of 0.607, Hit@10 of 0.960, and Recall@100 of 0.704. It improves substantially over BM25 but does not beat dense retrieval. This suggests that the dense candidate signal is already highly effective for Italian DBpedia entity retrieval, while hybrid search remains useful as a balanced candidate pool that preserves exact entity anchors.

### Metric Interpretation for Model Researchers

Hit@10 is high, especially for dense retrieval, so nDCG@10 and Recall@100 are more informative. nDCG@10 measures whether the most useful relevant entities appear early. Recall@100 matters because most queries have many valid entities. A strong model should retrieve a broad set of relevant descriptions, not just the first obvious entity page.

### Query and Relevance Type Tendencies

Queries are short Italian entity needs. Some are exact-name lookups, while others are category or property constraints. Relevant documents are DBpedia-style entity descriptions. Hard negatives often share entity type or topic but miss a required attribute, such as location, author, publication date, or relation to a film or place.

### Representative Failure Modes

BM25 can over-rank descriptions that repeat a category term but fail a specific constraint. Dense retrieval can retrieve semantically similar same-type entities that are not in the intended set. Hybrid retrieval improves robustness but may still rank generic entities above precise matches. Failure analysis should identify which entity attribute or class constraint was missed.

### Training and Leakage Considerations

Training should exclude DBpedia-Entity, BEIR, NanoBEIR, and translated entity records likely to overlap. Useful non-overlapping supervision includes entity search data, Wikipedia or DBpedia entity linking, multilingual entity retrieval, and short-query passage retrieval data. Multi-positive training is recommended because most queries have many relevant entity descriptions.

### Model Improvement Signals

Strong models should improve alias handling, attribute-aware ranking, and category-level recall. Useful signals include same-type hard negatives, property-based entity queries, multilingual entity descriptions, and entity linking supervision. Hybrid systems should preserve exact names through sparse search while dense retrieval expands toward semantically matching descriptions.

## Example Data

| Query | Positive document |
| --- | --- |
| Fitzgerald Auto Mall a Chambersburg, Pennsylvania [49 chars] | Fitzgerald Auto Malls è un'azienda a conduzione familiare che opera nel settore dell'auto e che è stata fondata nel 1966, con la sua prima sede aperta a Bethesda, nel Maryland. Nel 2014, Fitzgerald Auto Malls si è classificata al 59° posto nella lista delle "Top 125 Dealership Groups" negli Stati Uniti, pubblicata annualmente da Automotive News. Le sedi di Fitzgerald Auto Malls sono presenti cinque volte nella classifica WardsAuto e-Dealer 100 del 2013, rispettivamente al 8°, 25°, 30°, 43° e 98° posto. [507 chars] |
| La raccolta di racconti del 1994 di Alice Munro è disponibile [61 chars] | Alice Ann Munro (nata Laidlaw; 10 luglio 1931) è una scrittrice canadese. Il lavoro di Munro è stato descritto come avere rivoluzionato la struttura del racconto breve, soprattutto per la sua tendenza a muoversi avanti e indietro nel tempo. Le sue storie sono state definite come "suggerire più che esporre, rivelare più che ostentare." La narrativa di Munro è ambientata più spesso nella sua natia contea di Huron, nel sud-ovest dell'Ontario. Le sue storie esplorano le complessità umane con uno stile di scrittura semplice e diretto. [535 chars] |
| Architettura gallo-romana a Parigi [34 chars] | L'arte a Parigi è un articolo sulla cultura e la storia dell'arte nella capitale francese. Da secoli, Parigi attira artisti da tutto il mondo, che giungono in città per formarsi e trovare ispirazione nelle sue risorse artistiche e gallerie. Così, Parigi è diventata famosa come la "Città dell'Arte". [299 chars] |

## Public Sources

- [DBpedia-Entity V2 paper](https://doi.org/10.1145/3077136.3080751)
- [BEIR benchmark](https://github.com/beir-cellar/beir)
- [MMTEB benchmark](https://arxiv.org/abs/2502.13595)
- [NanoBEIR dataset](https://huggingface.co/collections/zeta-alpha-ai/nanobeir)

## Source Reference Table

| Label | URL |
|---|---|
| DBpedia-Entity V2 paper (https://doi.org/10.1145/3077136.3080751) |
| BEIR benchmark (https://github.com/beir-cellar/beir) |
| MMTEB benchmark (https://arxiv.org/abs/2502.13595) |
| NanoBEIR dataset (https://huggingface.co/collections/zeta-alpha-ai/nanobeir) |
