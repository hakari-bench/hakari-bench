# MNanoBEIR / NanoBEIR-ar / NanoDBPedia

## Overview

DBpedia-Entity is an entity-search benchmark over DBpedia. `NanoBEIR-ar__NanoDBPedia`
is the Arabic MNanoBEIR version: short Arabic entity-oriented queries must
retrieve relevant translated DBpedia entity descriptions. The task tests entity
disambiguation, list-style entity retrieval, and question-to-entity matching
under compact Arabic queries.

## Details

### What the Original Data Measures

[DBpedia-Entity V2: A Test Collection for Entity
Search](https://doi.org/10.1145/3077136.3080751) introduces an updated entity
search test collection using the English part of the DBpedia 2015-10 dump. The
paper describes DBpedia as a database version of Wikipedia and combines several
query sources, including SemSearch entity search, INEX linked-data search, list
search, and QALD question answering. Relevance judgments are entity-level:
systems should return DBpedia entities that directly answer or help answer the
query.

[BEIR: A Heterogeneous Benchmark for Zero-shot Evaluation of Information
Retrieval Models](https://arxiv.org/abs/2104.08663) includes DBpedia-Entity as
an entity retrieval task and notes that the task involves named entities,
keyword-style information needs, and natural-language queries. [MMTEB: Massive
Multilingual Text Embedding Benchmark](https://arxiv.org/abs/2502.13595)
provides the multilingual evaluation context for MNanoBEIR, including broad
task coverage and retrieval downsampling to reduce evaluation cost. The Arabic
Nano task keeps the entity-search objective but presents queries and entity
texts in Arabic translation.

### Observed Data Profile

The sampled Arabic Nano task has 50 queries, 6,045 documents, and 1,158
positive qrel rows. It is highly multi-positive: queries average 23.16
positives, 48 of 50 queries have more than one positive, and one query has 81
positives. The average query length is only 31.20 characters, and the average
document length is 315.46 characters.

The inspected queries include direct entities (`بوت، مونتانا`, `جون إليوت`),
list-style needs (`مؤلفين موسيقى التانغو`, `سائقو فورمولا 1 الذين فازوا
بجائزة موناكو الكبرى`), and a natural-language question (`من كان الرئيس
الخامس للولايات المتحدة الأمريكية؟`). Positive documents are concise DBpedia
entity descriptions, often people, places, events, offices, schools, films, or
works. For list queries, many entities can be relevant, so ranking breadth is
important.

### BM25 Difficulty

Using the dataset-provided BM25 candidate column, BM25 reaches nDCG@10 =
0.4633 and hit@10 = 0.9400. BM25 ranks a positive first for 25 of 50 queries,
and the median first-positive rank is 2. Every query has a positive within the
top 100.

The task is still not trivial. Short Arabic entity queries leave little context
for disambiguation, transliterated names may vary, and list-style queries can
have many acceptable positives. BM25 can benefit from direct name overlap, but
semantic ranking is needed to put the best entity descriptions above loosely
related entities, especially for broad classes such as tango composers or
Formula 1 drivers connected to a particular Grand Prix.

### Training Data That May Help

Useful training data includes non-overlapping DBpedia-Entity training or
development data, entity search logs, knowledge-base entity retrieval pairs,
Arabic entity linking data, and multilingual query-to-entity datasets. Data
with list-style queries is particularly valuable because many positives may be
valid for the same query.

Training should exclude BEIR, NanoBEIR, or DBpedia-Entity records likely to
overlap with the evaluation queries and entities. For Arabic models,
translation-aligned entity descriptions can help, but training should preserve
the entity-retrieval objective rather than turning the task into generic
question answering.

### Synthetic Data Guidance

For document-to-query generation, start from non-evaluation entity descriptions
and generate Arabic queries that name the entity, describe a type plus
attribute, or ask a short question answerable by the entity. Include ambiguous
names and list-style needs that map to multiple entities.

For joint generation, create Arabic DBpedia-style entity summaries and generate
short entity search queries with realistic transliteration variation. Synthetic
positives should be entity pages that satisfy the query, not passages that only
mention the query terms.

## Example Data

| Query | Positive document |
| --- | --- |
| موقع فيتزجيرالد أوتو مول في تشامبرسبيرج، بنسلفانيا (50 chars) | فيتزجيرالد للسيارات هي شركة تجارية لبيع السيارات مملوكة من قبل عائلة وتديرها العائلة، تأسست في عام 1966، حيث افتتحت أول موقع لها في بيتسدا، ماريلاند. اعتبارًا من عام 2014، احتلت فيتزجيرالد للسيارات المرتبة 59 في قائمة "أفضل 1 ... [truncated 225 chars](429 chars) |
| مجموعة قصص قصيرة صدرت في عام 1994 لأليس مونرو متاحة (51 chars) | أليس آن مونرو (مواليد 10 يوليو 1931) هي كاتبة كندية. عمل مونرو وصف بأنه قد أحدث ثورة في بناء القصص القصيرة، خاصة في قدرته على الانتقال بين الزمن الأمامي والخلفي. قصصها تُصف بأنها "تضمّن أكثر من إعلان، تكشف أكثر من عرض". قصص م ... [truncated 225 chars](351 chars) |
| العمارة الغالو-رومانية في باريس (31 chars) | الفن في باريس هو مقال عن ثقافة الفن والتاريخ في باريس، عاصمة فرنسا. منذ قرون طويلة، جذبت باريس الفنانين من جميع أنحاء العالم، ليأتوا إلى المدينة لتعلمهم واستلهموا من مواردها الفنية ومتاحفها. وبالتالي، اكتسبت باريس سمعة مدينة ... [truncated 225 chars](230 chars) |
| الجمهوريات السابقة ليوغوسلافيا (30 chars) | الدستور اليوغوسلافي لعام 1974 كان الرابع والأخير لدستور جمهورية يوغوسلافيا الاشتراكية الفيدرالية. دخل حيز التنفيذ في 21 فبراير. مع 406 مادة أصلية، كان الدستور لعام 1974 من أطول الدستورات في العالم. أضاف لغة مفصلة لحماية نظام ... [truncated 225 chars](330 chars) |
| الأفلام التي تم تصويرها في فينيسيا (34 chars) | فيلم "رومانسية صغيرة" هو فيلم كوميدي رومانسي أمريكي تم إنتاجه عام 1979، وهو من إخراج جورج روي هيل وبطولة لورنس أوليفييه، ثيلونيوس برنارد، وديان لين في أول ظهور لها على الشاشة. كتب السيناريو ألان بيرنز وجورج روي هيل، بناءً على ... [truncated 225 chars](305 chars) |

## Dataset Information

| Field | Value |
| --- | --- |
| Nano set | MNanoBEIR |
| Backing dataset | NanoBEIR-ar |
| Task / split | NanoDBPedia |
| Hugging Face dataset | [hakari-bench/NanoBEIR-ar](https://huggingface.co/datasets/hakari-bench/NanoBEIR-ar) |
| Language | ar |
| Category | natural_language |
| Queries | 50 |
| Documents | 6,045 |
| Positive qrels | 1,158 |
| Avg positives / query | 23.16 |
| Positives per query (min / median / max) | 1 / 18.00 / 81 |
| Queries with multiple positives | 48 (96.0%) |
| BM25 nDCG@10 | 0.4633 |
| BM25 hit@10 | 0.9400 |
| Query length avg chars | 31.20 |
| Document length avg chars | 315.46 |

### Public Sources

- [DBpedia-Entity V2: A Test Collection for Entity Search](https://doi.org/10.1145/3077136.3080751); 2017; Faegheh Hasibi, Fedor Nikolaev, Chenyan Xiong, Krisztian Balog, Svein Erik Bratsberg, Alexander Kotov, Jamie Callan; DOI: `10.1145/3077136.3080751`.
- [BEIR: A Heterogeneous Benchmark for Zero-shot Evaluation of Information Retrieval Models](https://arxiv.org/abs/2104.08663); 2021; Nandan Thakur, Nils Reimers, Andreas Rueckle, Abhishek Srivastava, Iryna Gurevych; DOI: `10.48550/arXiv.2104.08663`.
- [MMTEB: Massive Multilingual Text Embedding Benchmark](https://arxiv.org/abs/2502.13595); 2025; Kenneth Enevoldsen, Isaac Chung, Imene Kerboua, Marton Kardos, Ashwin Mathur, and others; DOI: `10.48550/arXiv.2502.13595`.
- [Zeta Alpha NanoBEIR collection](https://huggingface.co/collections/zeta-alpha-ai/nanobeir).

### Hugging Face Links

- Nano dataset: [hakari-bench/NanoBEIR-ar](https://huggingface.co/datasets/hakari-bench/NanoBEIR-ar)
- Source collection: [Zeta Alpha NanoBEIR collection](https://huggingface.co/collections/zeta-alpha-ai/nanobeir)

### Source Reference Table

| Title | Year | Type | URL |
| --- | ---: | --- | --- |
| DBpedia-Entity V2: A Test Collection for Entity Search | 2017 | task paper | https://doi.org/10.1145/3077136.3080751 |
| BEIR: A Heterogeneous Benchmark for Zero-shot Evaluation of Information Retrieval Models | 2021 | benchmark paper | https://arxiv.org/abs/2104.08663 |
| MMTEB: Massive Multilingual Text Embedding Benchmark | 2025 | benchmark paper | https://arxiv.org/abs/2502.13595 |
| NanoBEIR: Smaller BEIR dataset subsets | 2024 | dataset collection | https://huggingface.co/collections/zeta-alpha-ai/nanobeir |

## Machine-Readable Metadata

<!-- benchmark-task-metadata:v1 -->

```yaml
benchmark_task_metadata:
  schema_version: 1
  document_status: first_pass
  nano_set: MNanoBEIR
  backing_dataset: NanoBEIR-ar
  dataset_id: hakari-bench/NanoBEIR-ar
  task_name: NanoDBPedia
  split_name: NanoDBPedia
  language: ar
  category: natural_language
  document_path: docs/benchmark_tasks/MNanoBEIR/NanoBEIR-ar__NanoDBPedia.md
  source_research:
    primary_source_type: task_paper
    paper_pdf_or_html_checked: true
    no_paper_note: null
  counts:
    queries: 50
    documents: 6045
    positive_qrels: 1158
  positives_per_query:
    average: 23.16
    min: 1
    median: 18.0
    max: 81
    multi_positive_queries: 48
    multi_positive_query_percent: 96.0
  text_stats_chars:
    query_mean: 31.2
    document_mean: 315.46402
  bm25:
    ndcg_at_10: 0.4633029025
    hit_at_10: 0.94
    source: dataset_bm25_column
  learning:
    original_train_split: available
    evaluation_split_origin: MNanoBEIR Arabic NanoBEIR task split from hakari-bench/NanoBEIR-ar
    train_eval_overlap_audit: not_audited
    leakage_note: prefer excluding DBpedia-Entity, BEIR, or NanoBEIR records likely to overlap with these evaluation queries or entity pages
    useful_training_data:
      - non-overlapping DBpedia-Entity query-to-entity records
      - Arabic entity linking and entity retrieval datasets
      - multilingual knowledge-base search logs
      - list-style query-to-entity supervision
    synthetic_data:
      document_generation: Arabic DBpedia-style entity summaries with names, types, dates, locations, and attributes
      question_generation: short Arabic entity search queries, list queries, and natural-language questions answerable by an entity
      answerability: positives should be entity pages satisfying the query rather than documents that only mention the words
    multi_positive_training: multi_positive_objective
  links:
    nano_dataset: https://huggingface.co/datasets/hakari-bench/NanoBEIR-ar
    source_urls:
      - label: DBpedia-Entity V2 paper
        url: https://doi.org/10.1145/3077136.3080751
      - label: BEIR paper
        url: https://arxiv.org/abs/2104.08663
      - label: MMTEB paper
        url: https://arxiv.org/abs/2502.13595
      - label: Zeta Alpha NanoBEIR collection
        url: https://huggingface.co/collections/zeta-alpha-ai/nanobeir
    source_notes:
      - no_arxiv_page_confirmed_for_original_task_paper
      - Arabic task is a multilingual NanoBEIR adaptation of the original English BEIR task
  references:
    - title: "DBpedia-Entity V2: A Test Collection for Entity Search"
      url: https://doi.org/10.1145/3077136.3080751
      year: 2017
      doi: 10.1145/3077136.3080751
      is_paper: true
      source_confidence: definitive_paper_link
    - title: "BEIR: A Heterogeneous Benchmark for Zero-shot Evaluation of Information Retrieval Models"
      url: https://arxiv.org/abs/2104.08663
      year: 2021
      doi: 10.48550/arXiv.2104.08663
      is_paper: true
      source_confidence: benchmark_context_paper
    - title: "MMTEB: Massive Multilingual Text Embedding Benchmark"
      url: https://arxiv.org/abs/2502.13595
      year: 2025
      doi: 10.48550/arXiv.2502.13595
      is_paper: true
      source_confidence: benchmark_context_paper
    - title: "NanoBEIR: Smaller BEIR dataset subsets"
      url: https://huggingface.co/collections/zeta-alpha-ai/nanobeir
      year: 2024
      doi: null
      is_paper: false
      source_confidence: dataset_collection
```
