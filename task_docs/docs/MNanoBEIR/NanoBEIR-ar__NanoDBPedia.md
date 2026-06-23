# MNanoBEIR / NanoBEIR-ar / NanoDBPedia

## Overview

NanoBEIR-ar / NanoDBPedia is the Arabic NanoBEIR version of DBpedia-Entity, an
entity-search benchmark over DBpedia descriptions. The original task is
described in [DBpedia-Entity V2: A Test Collection for Entity
Search](https://doi.org/10.1145/3077136.3080751), which combines entity search,
linked-data search, list-style queries, and question-to-entity retrieval. This
Nano task contains 50 short Arabic queries, 6,045 Arabic translated entity
descriptions, and 1,158 positive qrels. It is highly multi-positive: many
queries ask for a class of entities rather than a single page. The task tests
whether retrieval models can preserve entity names and attributes while also
finding all entities that satisfy a short list-style or natural-language query.

## Details

### What the Original Data Measures

DBpedia-Entity evaluates retrieval over entity descriptions rather than
ordinary web pages or answer passages. The target is a DBpedia entity that
directly satisfies the query. Queries may name a specific entity, describe an
entity by attributes, ask for a list of entities of a certain type, or express a
short natural-language question. Relevance is entity-level: a document can
mention the query terms but still be wrong if it is not one of the desired
entities.

The Arabic NanoBEIR task keeps that objective in translated form. It is useful
for testing multilingual entity retrieval because the query can be very short,
the entity description can include names, locations, dates, occupations, and
types, and many positives can be valid for a single query.

### Observed Data Profile

The metadata records 50 queries, 6,045 documents, and 1,158 positive qrels.
Queries have 23.16 positives on average, a median of 18, and a maximum of 81.
There are 48 multi-positive queries, or 96.0% of the set. Query text is compact,
averaging 31.20 characters, while documents average 315.46 characters. Examples
include location queries, short descriptions of works, architectural topics,
former Yugoslav republics, films shot in Venice, musical authors, Formula 1
drivers, and direct questions about presidents.

This is broad entity retrieval rather than one-answer search. A top-100 list
can be useful even when it does not include every positive entity. Models need
to handle both exact entity names and list semantics: "films filmed in Venice"
or "Formula 1 drivers who won Monaco" require filtering entity pages by type
and attribute, not just matching one phrase.

### BM25 Evaluation Profile

The BM25 candidate subset reaches nDCG@10 = 0.5272, hit@10 = 0.9400, and
Recall@100 = 0.6295. BM25 is strong because many entity queries contain visible
names, places, work titles, occupations, and class terms that appear in the
DBpedia-style summaries. With short queries and concise entity descriptions,
exact overlap often places at least one relevant entity in the top 10.

BM25's weakness is breadth and disambiguation. List-style queries can have many
valid entities, and sparse matching may retrieve pages that mention the right
words without satisfying the full entity constraint. It can also over-rank an
entity with a matching location or title fragment while missing the type,
period, or relation that makes the entity relevant.

### Dense Evaluation Profile

The dense candidate subset from `harrier_oss_v1_270m` reaches nDCG@10 =
0.5204, hit@10 = 0.8800, and Recall@100 = 0.6727. Dense retrieval is slightly
behind BM25 on nDCG@10 and hit@10, but ahead on Recall@100. This means exact
surface forms are very effective for placing an initial positive near the top,
while embedding similarity helps discover additional relevant entities by
semantic type and attribute.

Dense retrieval is useful when a query describes a class or relation rather
than naming the entity directly. Its risk is under-anchoring: it may retrieve
entities of a similar type but miss the exact location, year, occupation,
nationality, or relation required by the query. For this task, dense retrieval
should be evaluated as a broad entity discovery signal, not just a final sorter.

### Reranking Hybrid Evaluation Profile

The `reranking_hybrid` candidate subset reaches nDCG@10 = 0.5277, hit@10 =
0.9400, and Recall@100 = 0.6805. It is the best candidate view overall:
top-rank quality matches or slightly exceeds BM25, while top-100 coverage
exceeds both BM25 and dense. This is the expected pattern for entity search:
lexical retrieval preserves exact names and titles, while dense retrieval adds
semantically related entities that satisfy list-style needs.

For reranker experiments, hybrid is the most useful pool because it contains
both name-overlap candidates and type/attribute-neighbor candidates. The
reranker can then learn to decide whether an entity actually satisfies the full
query constraint.

### Metric Interpretation for Model Researchers

This task is highly multi-positive, so Recall@100 is especially important.
BM25's high hit@10 shows that lexical entity anchors often find at least one
correct entity. Dense's higher Recall@100 shows that semantic similarity
contributes additional relevant entities. Hybrid leading on both nDCG@10 and
Recall@100 means neither lexical nor dense retrieval alone is sufficient for
the full entity set.

For first-stage retrieval, a good model should preserve exact entity strings
while expanding to related entities that share the requested type or attribute.
For reranking, the challenge is not only choosing one page but ordering many
valid entities above near misses.

### Query and Relevance Type Tendencies

Queries are short Arabic entity search requests. Some are direct entity names,
some are attribute descriptions, and many are list queries. Relevant documents
are DBpedia-style summaries of people, places, works, events, organizations,
offices, schools, films, and other entities. A positive document must satisfy
the entity need, not merely mention the query terms.

Lexical-heavy cases include exact names and titles. Semantic-heavy cases
include category or attribute requests where many entities are valid. Hybrid
retrieval is strongest when the query contains both a lexical anchor and a
semantic constraint, such as a place plus a work type or a profession plus an
achievement.

### Representative Failure Modes

BM25 can retrieve entities that share a name fragment, place name, or category
word but do not satisfy the full query. Dense retrieval can retrieve the right
kind of entity while missing a distinguishing attribute such as location, date,
nationality, or relation. Multi-positive list queries also create partial
coverage failures: the model may find a few obvious entities but miss less
lexically similar positives.

Good hard negatives are same-type entities that fail one query constraint,
entities with matching names but different identities, and pages that mention a
place or work without being an answer entity.

### Arabic-Specific Notes

Arabic entity retrieval must handle translated names, transliteration
variation, definite articles, attached particles, and entity descriptions that
mix names, places, dates, and foreign proper nouns. Sparse retrieval benefits
from tokenization that preserves entity names and titles. Dense retrieval helps
when the entity is described by type or attribute rather than named directly,
but it must not collapse distinct named entities. Strong systems should combine
name-sensitive matching with entity-type reasoning.

### Training and Leakage Notes

Training should exclude DBpedia-Entity, BEIR, or NanoBEIR records likely to
overlap with these evaluation queries or entity pages. Useful non-overlapping
data includes DBpedia-style query-to-entity pairs, Arabic entity linking,
multilingual knowledge-base search logs, and list-style entity retrieval
supervision. Training should preserve the entity-retrieval objective rather
than turning every query into a generic QA task.

### Model Improvement Hints

The main improvement target is multi-positive entity coverage with accurate
constraint matching. First-stage retrievers should keep exact entity names and
titles while expanding to entities that satisfy the query's type and attribute
constraints. Rerankers should learn from hard negatives that share one
constraint but fail another.

### Training Data That May Help

Useful training data includes non-overlapping DBpedia-Entity records, Arabic
entity linking datasets, multilingual entity search logs, list-style
query-to-entity supervision, and synthetic entity queries with multiple valid
answers.

### Synthetic Data Guidance

Generate Arabic DBpedia-style entity summaries with names, entity types,
locations, dates, occupations, works, and attributes. Then generate short
entity search queries, list queries, and natural-language questions answerable
by one or more entities. Positives should be entity pages satisfying the query;
hard negatives should share surface terms or entity types while failing the
full constraint.

## Example Data

| Query | Positive document |
| --- | --- |
| موقع فيتزجيرالد أوتو مول في تشامبرسبيرج، بنسلفانيا [50 chars] | فيتزجيرالد للسيارات هي شركة تجارية لبيع السيارات مملوكة من قبل عائلة وتديرها العائلة، تأسست في عام 1966، حيث افتتحت أول موقع لها في بيتسدا، ماريلاند. اعتبارًا من عام 2014، احتلت فيتزجيرالد للسيارات ال... [200 / 429 chars] |
| مجموعة قصص قصيرة صدرت في عام 1994 لأليس مونرو متاحة [51 chars] | أليس آن مونرو (مواليد 10 يوليو 1931) هي كاتبة كندية. عمل مونرو وصف بأنه قد أحدث ثورة في بناء القصص القصيرة، خاصة في قدرته على الانتقال بين الزمن الأمامي والخلفي. قصصها تُصف بأنها "تضمّن أكثر من إعلان،... [200 / 351 chars] |
| العمارة الغالو-رومانية في باريس [31 chars] | الفن في باريس هو مقال عن ثقافة الفن والتاريخ في باريس، عاصمة فرنسا. منذ قرون طويلة، جذبت باريس الفنانين من جميع أنحاء العالم، ليأتوا إلى المدينة لتعلمهم واستلهموا من مواردها الفنية ومتاحفها. وبالتالي،... [200 / 230 chars] |
| الجمهوريات السابقة ليوغوسلافيا [30 chars] | الدستور اليوغوسلافي لعام 1974 كان الرابع والأخير لدستور جمهورية يوغوسلافيا الاشتراكية الفيدرالية. دخل حيز التنفيذ في 21 فبراير. مع 406 مادة أصلية، كان الدستور لعام 1974 من أطول الدستورات في العالم. أض... [200 / 330 chars] |
| الأفلام التي تم تصويرها في فينيسيا [34 chars] | فيلم "رومانسية صغيرة" هو فيلم كوميدي رومانسي أمريكي تم إنتاجه عام 1979، وهو من إخراج جورج روي هيل وبطولة لورنس أوليفييه، ثيلونيوس برنارد، وديان لين في أول ظهور لها على الشاشة. كتب السيناريو ألان بيرنز... [200 / 305 chars] |

### Public Sources

- [DBpedia-Entity V2: A Test Collection for Entity Search](https://doi.org/10.1145/3077136.3080751), 2017.
- [BEIR: A Heterogeneous Benchmark for Zero-shot Evaluation of Information Retrieval Models](https://arxiv.org/abs/2104.08663), 2021.
- [MMTEB: Massive Multilingual Text Embedding Benchmark](https://arxiv.org/abs/2502.13595), 2025.
- [Zeta Alpha NanoBEIR collection](https://huggingface.co/collections/zeta-alpha-ai/nanobeir).

### Hugging Face Links

- Nano dataset: [hakari-bench/NanoBEIR-ar](https://huggingface.co/datasets/hakari-bench/NanoBEIR-ar)
- Source collection: [Zeta Alpha NanoBEIR collection](https://huggingface.co/collections/zeta-alpha-ai/nanobeir)

### Source Reference Table

| Title | Year | Type | URL |
| --- | ---: | --- | --- |
| DBpedia-Entity V2: A Test Collection for Entity Search | 2017 | task paper | [https://doi.org/10.1145/3077136.3080751](https://doi.org/10.1145/3077136.3080751) |
| BEIR: A Heterogeneous Benchmark for Zero-shot Evaluation of Information Retrieval Models | 2021 | benchmark paper | [https://arxiv.org/abs/2104.08663](https://arxiv.org/abs/2104.08663) |
| MMTEB: Massive Multilingual Text Embedding Benchmark | 2025 | benchmark paper | [https://arxiv.org/abs/2502.13595](https://arxiv.org/abs/2502.13595) |
| NanoBEIR: Smaller BEIR dataset subsets | 2024 | dataset collection | [https://huggingface.co/collections/zeta-alpha-ai/nanobeir](https://huggingface.co/collections/zeta-alpha-ai/nanobeir) |
