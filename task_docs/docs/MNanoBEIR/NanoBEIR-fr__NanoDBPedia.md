# MNanoBEIR / NanoBEIR-fr / NanoDBPedia

## Overview

This task is the French NanoBEIR version of DBpedia-Entity, an entity search benchmark built from DBpedia entity pages and heterogeneous entity-oriented queries. The original DBpedia-Entity collection evaluates whether retrieval systems can find entity pages matching names, categories, aliases, or property constraints. In this NanoBEIR slice, French translated entity queries must retrieve French translated DBpedia-style entity descriptions from 6,045 candidate documents. The task contains 50 queries and 1,158 positive relevance judgments, with an average of 23.16 positives per query. It is a many-positive entity retrieval task that tests exact entity matching, category search, attribute disambiguation, and retrieval of broad sets of relevant entities.

## Details

### What the Original Data Measures

DBpedia-Entity measures entity search rather than answer passage retrieval. A query may name a specific entity, describe a class of entities, or include a property such as location, creator, publication date, role, or filming place. Relevant documents are entity descriptions that satisfy the information need. Because many queries have many positives, the model should retrieve a useful set of entities, not just one obvious match.

### Observed Data Profile

The French Nano task has 50 queries, 6,045 documents, and 1,158 positives. Positives per query average 23.16, with a median of 18 and a maximum of 81. Forty-eight queries are multi-positive. Queries average about 41 characters, and documents average about 374 characters. Example queries include a Fitzgerald car dealership in Chambersburg, an Alice Munro short-story collection, Gallo-Roman architecture in Paris, former Yugoslav republics, and films shot in Venice.

### BM25 Evaluation Profile

BM25 is strong, with nDCG@10 of 0.583, Hit@10 of 0.940, and Recall@100 of 0.684. This reflects the entity-oriented structure of the task: names, locations, categories, and property words often appear directly in the relevant descriptions. Sparse matching is especially effective for rare entity names and short category phrases. Its main limitation is distinguishing among many same-type entities when a query is broad or attribute-based.

### Dense Evaluation Profile

The dense harrier-oss-270m baseline reaches nDCG@10 of 0.558, Hit@10 of 0.860, and Recall@100 of 0.687. Dense retrieval slightly improves recall over BM25 but is weaker at top ranking. This suggests that embeddings help recover semantically related entity descriptions, while exact names and category labels remain critical for early precision. Dense retrieval can also blur distinctions among same-type entities when the query requires a specific attribute.

### Reranking Hybrid Evaluation Profile

The reranking_hybrid profile reaches nDCG@10 of 0.571, Hit@10 of 0.960, and Recall@100 of 0.719. It gives the best Hit@10 and Recall@100, while BM25 gives the best nDCG@10. This makes hybrid search useful for broad candidate coverage in many-positive entity retrieval. BM25 anchors exact names and categories, while dense retrieval adds semantically matching entity pages that may not repeat the query wording exactly.

### Metric Interpretation for Model Researchers

Hit@10 is high for all methods, so it should be treated as a basic coverage signal. nDCG@10 measures whether the best relevant entities appear early. Recall@100 is important because most queries have many positives and a good system should retrieve a broad entity set. The hybrid profile's higher recall suggests it is preferable as a candidate generator, while BM25's nDCG advantage shows the continued value of exact entity matching.

### Query and Relevance Type Tendencies

Queries are short French entity information needs. Relevant documents are compact DBpedia-style summaries. Some queries target a single named entity, while others request a class of entities with constraints. Hard negatives often share entity type or topic but fail a required property such as location, creator, publication history, or relation to a work.

### Representative Failure Modes

BM25 can over-rank entity pages that repeat a class term but miss the required attribute. Dense retrieval can retrieve semantically similar entities that are not in the intended set. Hybrid retrieval improves coverage but can still rank generic same-type entities above more precise matches. Failure analysis should identify which entity constraint was ignored.

### Training and Leakage Considerations

Training should exclude DBpedia-Entity, BEIR, NanoBEIR, and translated DBpedia records likely to overlap with these queries or pages. Useful non-overlapping data includes entity search datasets, knowledge-base description retrieval pairs, French or multilingual entity linking data, and hard negatives from same-type entities. Multi-positive training is recommended because most queries have many valid entities.

### Model Improvement Signals

Strong models should combine alias normalization, exact name matching, and attribute-aware ranking. Useful training signals include same-type hard negatives, property-based entity queries, multilingual entity descriptions, and class-level retrieval pairs. Hybrid systems should preserve sparse entity anchors while using dense retrieval for semantic category and property matching.

## Example Data

| Query | Positive document |
| --- | --- |
| concession automobile fitzgerald à chambersburg, pa [51 chars] | Fitzgerald Auto Malls est un concessionnaire automobile familial fondé en 1966, avec son premier emplacement ouvert à Bethesda, Maryland. En 2014, Fitzgerald Auto Malls était classé 59e sur la liste des "Top 125 Dealership Groups" aux États-Unis, publiée annuellement par Automotive News. Les emplacements des concessionnaires Fitzgerald figurent cinq fois dans le classement WardsAuto e-Dealer 100 de 2013, aux 8e, 25e, 30e, 43e et 98e places. [444 chars] |
| Le recueil de nouvelles de 1994 d'Alice Munro est disponible [60 chars] | Alice Ann Munro (/ˈælɨs ˌæn mʌnˈroʊ/, née Laidlaw /ˈleɪdlɔː/; née le 10 juillet 1931) est une auteure canadienne. L'œuvre de Munro a été décrite comme ayant révolutionné la structure des nouvelles, notamment par sa tendance à aller de l'avant et en arrière dans le temps. Ses récits ont été qualifiés de "suggérant plus qu'annonçant, révélant plus qu'exhibant." Les fictions de Munro se déroulent le plus souvent dans son comté natal de Huron, dans le sud-ouest de l'Ontario. Ses histoires explorent les complexités humaines dans un style d'écriture simple et direct. [567 chars] |
| Architecture gallo-romaine à Paris [34 chars] | L'art à Paris parle de la culture et de l'histoire de l'art à Paris, la capitale de la France. Depuis des siècles, Paris a attiré des artistes du monde entier, venant s'y former et y puiser l'inspiration dans ses ressources artistiques et ses galeries. En conséquence, Paris a acquis la réputation de la 'Ville de l'Art'. [321 chars] |

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
