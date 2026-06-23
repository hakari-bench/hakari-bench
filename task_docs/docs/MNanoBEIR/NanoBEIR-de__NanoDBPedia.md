# MNanoBEIR / NanoBEIR-de / NanoDBPedia

## Overview

NanoBEIR-de / NanoDBPedia is the German NanoBEIR version of DBpedia-Entity, an
entity-search benchmark introduced in
[DBpedia-Entity V2: A Test Collection for Entity
Search](https://doi.org/10.1145/3077136.3080751). Each query is a short German
translated entity-oriented request, and the retrieval target is a German
translated DBpedia-style entity description. The Nano task contains 50 queries,
6,045 entity documents, and 1,158 positive qrels. It is highly multi-positive:
queries average 23.16 positives, and many are list-style entity needs rather
than single-entity lookups. The task tests entity-name preservation,
disambiguation, and retrieval of all entities satisfying a type or attribute
constraint. Dense retrieval and `reranking_hybrid` slightly outperform BM25,
showing that semantic entity matching adds value beyond exact name overlap.

## Details

### What the Original Data Measures

DBpedia-Entity evaluates entity search over DBpedia descriptions. Queries come
from multiple sources, including entity search, linked-data search, list
search, and question answering. Relevance is entity-level: a document is
positive when the entity itself satisfies the query, not merely because the text
mentions the same words.

The German NanoBEIR version keeps this entity-search objective in translated
form. The retriever must rank entity descriptions for direct names, natural
questions, and list-style requests. This makes the task different from passage
QA: the desired result is the entity page.

### Observed Data Profile

The metadata records 50 queries, 6,045 documents, and 1,158 positive qrels.
Queries have 23.16 positives on average, with a median of 18 and a maximum of
81. There are 48 multi-positive queries, or 96.0% of the set. Query text
averages 38.00 characters, and documents average 369.48 characters. Examples
include Fitzgerald Auto Mall in Chambersburg, Alice Munro's 1994 short-story
collection, Gallo-Roman architecture in Paris, former Yugoslav republics, and
films shot in Venice.

This is broad entity retrieval. Some queries have a single obvious entity, but
many request a class of entities. A good model should retrieve many correct
entities, not only the most lexically obvious one.

### BM25 Evaluation Profile

The BM25 candidate subset reaches nDCG@10 = 0.5747, hit@10 = 0.9600, and
Recall@100 = 0.6468. BM25 is strong because short entity queries often contain
names, places, work titles, occupations, or category words that appear in the
entity description. For German translated entity text, exact names and titles
remain powerful anchors.

BM25's weakness is complete entity-set coverage and constraint satisfaction. A
document can share a place name or type word while failing the full query. In
list-style cases, sparse matching may find obvious entities but miss less
lexically similar positives that still satisfy the request.

### Dense Evaluation Profile

The dense candidate subset from `harrier_oss_v1_270m` reaches nDCG@10 =
0.6152, hit@10 = 0.9600, and Recall@100 = 0.7021. Dense retrieval improves
top-rank ordering and coverage over BM25 while preserving the same high hit@10.
This suggests that embedding similarity helps identify entity types and
attributes beyond exact surface overlap.

Dense retrieval is especially useful for list queries and natural-language
entity questions. Its risk is type-neighbor drift: it can retrieve similar
entities that match the general category but fail a required location, date,
work, office, or relation.

### Reranking Hybrid Evaluation Profile

The `reranking_hybrid` candidate subset reaches nDCG@10 = 0.6157, hit@10 =
0.9600, and Recall@100 = 0.7133. It is the strongest candidate view overall,
though only slightly ahead of dense at the top. The hybrid pool has exactly 100
candidates per query and no rank-101 safeguard rows.

For reranker experiments, hybrid is the safest pool because it combines exact
entity/name matches with semantically related entity candidates. A reranker can
then decide whether each entity satisfies the full query constraint.

### Metric Interpretation for Model Researchers

NanoDBPedia-de is highly multi-positive, so Recall@100 matters as much as
top-10 ranking. BM25 already finds a positive for almost every query, but dense
and hybrid recover more of the relevant entity set. This means the task is not
only "find one matching entity"; it is "rank many valid entities above near
misses."

A strong model should preserve exact names while also reasoning over entity
type, attribute, location, and relation. Hybrid retrieval is the best practical
candidate-generation view for reranking.

### Query and Relevance Type Tendencies

Queries are short German entity search requests. They include direct entity
names, list queries, place/work constraints, and natural-language entity
questions. Relevant documents are entity summaries for people, places, works,
events, offices, organizations, and other DBpedia entities.

Lexical-heavy cases involve exact names and titles. Dense-heavy cases involve
type or attribute matching, especially when many entities are valid. Hybrid is
strongest when a query combines a visible name or place with a broader semantic
constraint.

### Representative Failure Modes

BM25 can retrieve entities that share a name fragment, place, or type word but
do not satisfy the full request. Dense retrieval can retrieve the right kind of
entity while missing a distinguishing attribute. Multi-positive failures occur
when the model finds a few obvious entities but misses the broader set.

Good hard negatives are same-type entities with a wrong location or relation,
entities with similar names, and pages that mention the query words without
being answer entities.

### German-Specific Notes

German entity retrieval must handle compound terms, translated names, foreign
proper nouns, titles, and place names. Sparse retrieval benefits from
tokenization that preserves names and compounds. Dense retrieval helps with
entity-type matching but must not collapse distinct entities. Mixed-language
names and untranslated titles can be important anchors.

### Training and Leakage Notes

Training should exclude DBpedia-Entity, BEIR, or NanoBEIR records likely to
overlap with these evaluation queries or entity pages. Useful non-overlapping
data includes DBpedia-Entity query-to-entity records, German or multilingual
entity linking data, knowledge-base entity retrieval pairs, and list-style
query-to-entity supervision.

### Model Improvement Hints

The main improvement target is multi-positive entity coverage with accurate
constraints. First-stage retrievers should keep exact entity strings while
expanding to entities that match type and attributes. Rerankers should learn
from hard negatives that satisfy one part of the query but fail another.

### Training Data That May Help

Useful training data includes non-overlapping entity search logs,
query-to-entity pairs, German entity linking, multilingual knowledge-base
retrieval, list-search supervision, and synthetic entity clusters with multiple
valid positives.

### Synthetic Data Guidance

Generate German DBpedia-style entity summaries with names, types, dates,
locations, occupations, works, and attributes. Then generate entity search
queries, list queries, and natural-language questions. Positives should be
entity pages satisfying the query; hard negatives should share terms or entity
types while failing the full constraint.

## Example Data

| Query | Positive document |
| --- | --- |
| Fitzgerald Autohaus in Chambersburg, PA [39 chars] | Fitzgerald Auto Malls ist ein familiengeführtes und -betriebenes Autohaus, das 1966 gegründet wurde und seine erste Filiale in Bethesda, Maryland, eröffnete. Stand 2014 belegte Fitzgerald Auto Malls P... [200 / 445 chars] |
| Ist die Kurzgeschichtensammlung von Alice Munro aus dem Jahr 1994 verfügbar? [76 chars] | Alice Ann Munro (/ˈælɨs ˌæn mʌnˈroʊ/, geb. Laidlaw /ˈleɪdlɔː/; geboren 10. Juli 1931) ist eine kanadische Autorin. Munros Werk wird beschrieben, die Struktur von Kurzgeschichten neu definiert zu haben... [200 / 575 chars] |
| Gallorömische Architektur in Paris [34 chars] | Kunst in Paris ist ein Artikel über die Kunstkultur und -geschichte in Paris, der Hauptstadt Frankreichs. Seit Jahrhunderten hat Paris Künstler aus aller Welt angezogen, die in die Stadt kommen, um si... [200 / 354 chars] |
| Republiken des ehemaligen Jugoslawiens [38 chars] | Die Verfassung von 1974 Jugoslawiens war die vierte und letzte Verfassung der Sozialistischen Föderativen Republik Jugoslawien. Sie trat am 21. Februar in Kraft. Mit 406 ursprünglichen Artikeln war di... [200 / 454 chars] |
| Filme, die in Venedig gedreht wurden [36 chars] | A Little Romance ist ein 1979er amerikanischer Technicolor- und Panavision-Romantikkomödie unter der Regie von George Roy Hill mit Laurence Olivier, Thelonious Bernard und Diane Lane in ihrer ersten F... [200 / 366 chars] |

### Public Sources

- [DBpedia-Entity V2: A Test Collection for Entity Search](https://doi.org/10.1145/3077136.3080751), 2017.
- [BEIR: A Heterogeneous Benchmark for Zero-shot Evaluation of Information Retrieval Models](https://arxiv.org/abs/2104.08663), 2021.
- [MMTEB: Massive Multilingual Text Embedding Benchmark](https://arxiv.org/abs/2502.13595), 2025.
- [Zeta Alpha NanoBEIR collection](https://huggingface.co/collections/zeta-alpha-ai/nanobeir).

### Hugging Face Links

- Nano dataset: [hakari-bench/NanoBEIR-de](https://huggingface.co/datasets/hakari-bench/NanoBEIR-de)
- Source collection: [Zeta Alpha NanoBEIR collection](https://huggingface.co/collections/zeta-alpha-ai/nanobeir)

### Source Reference Table

| Title | Year | Type | URL |
| --- | ---: | --- | --- |
| DBpedia-Entity V2: A Test Collection for Entity Search | 2017 | task paper | [https://doi.org/10.1145/3077136.3080751](https://doi.org/10.1145/3077136.3080751) |
| BEIR: A Heterogeneous Benchmark for Zero-shot Evaluation of Information Retrieval Models | 2021 | benchmark paper | [https://arxiv.org/abs/2104.08663](https://arxiv.org/abs/2104.08663) |
| MMTEB: Massive Multilingual Text Embedding Benchmark | 2025 | benchmark paper | [https://arxiv.org/abs/2502.13595](https://arxiv.org/abs/2502.13595) |
| NanoBEIR: Smaller BEIR dataset subsets | 2024 | dataset collection | [https://huggingface.co/collections/zeta-alpha-ai/nanobeir](https://huggingface.co/collections/zeta-alpha-ai/nanobeir) |
