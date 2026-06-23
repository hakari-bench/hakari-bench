# MNanoBEIR / NanoBEIR-sv / NanoDBPedia

## Overview

NanoDBPedia in the Swedish NanoBEIR slice is an entity-oriented retrieval task derived from DBpedia Entity Retrieval. The queries are Swedish translated entity information needs, and the corpus contains Swedish translated DBpedia-style entity descriptions. The retrieval goal is to rank entities that satisfy short keyword-like needs, such as people, places, works, organizations, or entity categories. This makes the task a compact diagnostic for entity search, alias handling, and type-aware retrieval in a multilingual setting.

## Details

### What the Original Data Measures

DBpedia Entity Retrieval evaluates ranking entities for information needs over a structured encyclopedic collection. In BEIR-style form, the task becomes text retrieval over entity descriptions. Relevance can depend on names, aliases, categories, occupations, locations, relationships, and entity type. The right answer is often not just a document about the same words, but an entity that satisfies the requested description.

The Swedish translated version tests whether a model can connect short Swedish needs to translated entity descriptions. Many queries are brief noun phrases rather than full questions, and many relevant documents are compact encyclopedic summaries. This favors systems that preserve entity names and type constraints while still recognizing paraphrase and alias variation.

### Observed Data Profile

The task contains 50 queries, 6,045 documents, and 1,158 relevance judgments. Almost every query is multi-positive, with an average of 23.16 positives per query. The minimum is 1, the median is 18.0, the maximum is 81, and 48 queries are multi-positive, or 96.0% of the query set. This is a broad relevant-set entity ranking task.

Queries average only 35.66 characters, while documents average 327.04 characters. The queries are short and often underspecified, while the documents are concise entity summaries. This means that relevance depends heavily on entity type and category matching. A model must retrieve many acceptable entities for broad needs such as films, former republics, architecture, or available works.

### BM25 Evaluation Profile

BM25 reaches nDCG@10 of 0.4342, hit@10 of 0.9200, and recall@100 of 0.5009 using the top-500 BM25 candidate subset. This is a strong lexical profile for finding at least one relevant entity. Short entity queries often contain names, places, or category words that appear directly in entity descriptions.

The recall@100 value shows the limitation of lexical matching on broad multi-positive needs. BM25 can retrieve obvious name or keyword matches, but it may miss relevant entities that use aliases, category descriptions, or related terminology. For entity search, exact overlap is an important anchor but does not cover the full relevant set.

### Dense Evaluation Profile

The dense harrier-oss-270m run reaches nDCG@10 of 0.5906, hit@10 of 0.9200, and recall@100 of 0.6744. Dense retrieval substantially improves nDCG@10 and recall@100 over BM25 while keeping the same hit@10. This indicates that embedding similarity is better at ranking multiple relevant entities and recognizing type-level or semantic matches beyond exact words.

The dense strength is especially important for short queries. When the query is only a phrase, dense embeddings can use broader semantic associations between the need and entity descriptions. Remaining errors likely involve ambiguous entity types, names that require precise lexical matching, or queries where many relevant entities are only weakly distinguished by their summaries.

### Reranking Hybrid Evaluation Profile

The reranking_hybrid candidate set reaches nDCG@10 of 0.5073, hit@10 of 0.9600, and recall@100 of 0.6468. It uses exactly 100 candidates per query, with no rank-101 safeguard rows. The hybrid profile improves hit@10 over both BM25 and dense retrieval, but dense retrieval remains stronger on nDCG@10 and recall@100.

This pattern suggests that hybrid search improves the chance of at least one relevant entity appearing very early, because lexical and dense signals cover different entity matches. However, the dense ordering is better at ranking the broader relevant set. For downstream reranking, the hybrid pool is useful, but a dense first-stage ranking may be more informative when the goal is to present many good entities in the top 10.

### Metric Interpretation for Model Researchers

Because most queries have many positives, nDCG@10 and recall@100 are more informative than hit@10 alone. A model can achieve high hit@10 by finding one obvious entity while still failing to retrieve many other relevant entities. recall@100 measures relevant-set coverage, while nDCG@10 measures how densely the first page is populated with correct entities.

The method comparison shows that BM25 is strong for lexical entity anchors, dense retrieval is best for broad entity ranking, and reranking_hybrid is best at guaranteeing at least one early positive. This makes NanoDBPedia-sv useful for separating exact-name matching, semantic type matching, and multi-positive ranking quality.

### Query and Relevance Type Tendencies

Queries include entity needs such as a Fitzgerald car museum in Chambersburg, a 1994 short-story collection by Alice Munro, Gallo-Roman architecture in Paris, former Yugoslav republics, and films shot in Venice. Relevant documents are DBpedia-style descriptions of entities that satisfy those needs.

The task rewards models that understand entity categories and constraints. A query may specify a work type, location, time, author, or class of entities. A relevant result must satisfy those constraints, not merely mention one query word. The short-query format makes missing or misinterpreting a single term costly.

### Representative Failure Modes

Likely failures include retrieving entities that share a name fragment but have the wrong type, missing aliases or translated category labels, over-ranking famous entities that are only loosely related, and failing to cover all members of a broad entity class. BM25 may overvalue exact words in descriptions, while dense models may blur neighboring entity categories when descriptions are short.

### Training Data That May Help

Useful training data includes entity retrieval, Wikipedia and DBpedia search, alias matching, multilingual entity linking, type-aware ranking, and hard negatives that share names, locations, occupations, or categories. Swedish encyclopedic data can help with translated entity descriptions and category wording. For rerankers, negatives should be entities that look plausible but violate a key type or constraint.

### Model Improvement Notes

A model targeting this task should combine exact entity-name precision with semantic type awareness. Sparse systems need good handling of aliases, morphology, and named entities. Dense systems need stronger constraint tracking for short queries. Hybrid systems can improve early positive discovery, but ranking the full relevant set likely requires explicit entity-type and relation sensitivity.

## Example Data

| Query | Positive document |
| --- | --- |
| Fitzgerald bilmuseet Chambersburg, PA [37 chars] | Fitzgerald Auto Malls är en familjeägd och driven bilhandelskedja som grundades 1966, med sin första plats öppnad i Bethesda, Maryland. År 2014 rankades Fitzgerald Auto Malls som nummer 59 på listan ö... [200 / 404 chars] |
| Samling av noveller från 1994 av Alice Munro är tillgänglig [59 chars] | Alice Ann Munro (/ˈælɨs ˌæn mʌnˈroʊ/, född Laidlaw /ˈleɪdlɔː/; född 10 juli 1931) är en kanadensisk författare. Munros verk har beskrivits som att ha förändrat novellens struktur, särskilt i dess tend... [200 / 470 chars] |
| Galloromansk arkitektur i Paris [31 chars] | Konst i Paris är en artikel om konstkultur och historia i Paris, Frankrikes huvudstad. Under århundraden har Paris lockat konstnärer från hela världen, som kommit till staden för att utbilda sig och f... [200 / 331 chars] |
| De tidigare jugoslaviska republikerna [37 chars] | 1974 års jugoslaviska konstitution var den fjärde och sista konstitutionen för den socialistiska federala republiken Jugoslavien. Den trädde i kraft den 21 februari. Med sina 406 ursprungliga artiklar... [200 / 455 chars] |
| Filmer inspelade i Venedig [26 chars] | A Little Romance är en amerikansk romantisk komedifilm från 1979 i Technicolor och Panavision, regisserad av George Roy Hill och med Laurence Olivier, Thelonious Bernard och Diane Lane i hennes filmde... [200 / 370 chars] |

### Source Reference Table

| Item | Reference |
| --- | --- |
| Original dataset | [DBpedia Entity Retrieval](https://doi.org/10.1145/3077136.3080751) |
| Retrieval benchmark framing | [BEIR](https://arxiv.org/abs/2104.08663) |
| Multilingual benchmark context | [MMTEB](https://arxiv.org/abs/2502.13595) |
| NanoBEIR collection | [NanoBEIR on Hugging Face](https://huggingface.co/collections/zeta-alpha-ai/nanobeir) |
| NanoBEIR-sv dataset | [hakari-bench/NanoBEIR-sv](https://huggingface.co/datasets/hakari-bench/NanoBEIR-sv) |

Representative query and positive entity snippets:

| Query | Positive document snippet |
| --- | --- |
| Fitzgerald bilmuseet Chambersburg, PA | Fitzgerald Auto Malls är en familjeägd och driven bilhandelskedja som grundades 1966... |
| Samling av noveller från 1994 av Alice Munro är tillgänglig | Alice Ann Munro är en kanadensisk författare. Munros verk har beskrivits som att ha förändrat novellens struktur... |
| Galloromansk arkitektur i Paris | Konst i Paris är en artikel om konstkultur och historia i Paris, Frankrikes huvudstad... |
| De tidigare jugoslaviska republikerna | 1974 års jugoslaviska konstitution var den fjärde och sista konstitutionen för den socialistiska federala republiken Jugoslavien... |
| Filmer inspelade i Venedig | A Little Romance är en amerikansk romantisk komedifilm från 1979 i Technicolor och Panavision... |
