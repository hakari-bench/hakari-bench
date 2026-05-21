# MNanoBEIR / NanoBEIR-sr / NanoDBPedia

## Overview

DBPedia Entity is an entity-oriented retrieval benchmark. `NanoBEIR-sr__NanoDBPedia`
uses Serbian translated entity needs to retrieve Serbian translated DBpedia-style
entity descriptions.

## Details

### What the Original Data Measures

[DBpedia-Entity](https://doi.org/10.1145/3077136.3080751) evaluates ranking
entities for information needs over DBpedia. BEIR includes it as a heterogeneous
entity retrieval task, and MMTEB supplies the multilingual framing for this
Serbian translation.

### Observed Data Profile

The sampled task has 50 queries, 6,045 documents, and 1,158 positive qrels.
Almost every query is multi-positive, with an average of 23.16 positives and a
maximum of 81. Queries average 41.18 characters and documents average 338.86
characters.

### BM25 Difficulty

BM25 reaches nDCG@10 = 0.4341 and hit@10 = 0.8800. The median first-positive
rank is 1.0, indicating strong entity-name cues, but the large positive sets
make ordering quality important.

### Training Data That May Help

Useful supervision includes entity search, Serbian Wikipedia or DBpedia
retrieval, alias matching, and multilingual entity description ranking. Exclude
DBPedia Entity, BEIR, NanoBEIR, and any translated duplicate evaluation records.

### Synthetic Data Guidance

Generate Serbian entity needs that mix short keyword phrases with question
forms. Positive documents should be concise entity descriptions; hard negatives
should share entity types, places, occupations, or names.

## Example Data

| Query | Positive document |
| --- | --- |
| Fitzgerald auto salon Chambersburg Pennsylvania (47 chars) | Fitzgerald Auto Malls je porodična auto-kompanija koja je osnovana 1966. godine, a prva lokacija otvorena je u Bethesdi, Maryland. Od 2014. godine, Fitzgerald Auto Malls se nalazio na 59. mestu liste "Top 125 prodajnih grupa" ... [truncated 225 chars](410 chars) |
| Zbirka kratkih priča iz 1994. godine "Alice Munro je Otvorena" (62 chars) | Aliсe En Manro (/ˈælɨs ˌæn mʌnˈroʊ/, devojački Lejdlo /ˈleɪdlɔː/; rođena 10. jula 1931) je kanadska spisateljica. Manrin rad je opisan kao revolucionaran u arhitekturi kratkih priča, posebno u svojoj sklonosti da se kreće nap ... [truncated 225 chars](494 chars) |
| galsko-rimska arhitektura u Parizu (34 chars) | Umetnost u Parizu je članak o umetničkoj kulturi i istoriji u Parizu, glavnom gradu Francuske. Vekovima je Pariz privlačio umetnike iz celog sveta, koji su dolazili u grad kako bi se obrazovali i tražili inspiraciju iz njegov ... [truncated 225 chars](323 chars) |
| Republike bivše Jugoslavije (27 chars) | Ustav Jugoslavije iz 1974. bio je četvrti i poslednji ustav Socijalističke Federativne Republike Jugoslavije. Stupio je na snagu 21. februara. Sa 406 originalnih članova, ustav iz 1974. bio je jedan od najdužih ustava na svet ... [truncated 225 chars](409 chars) |
| filmovi snimljeni u Veneciji (28 chars) | "Mala Romansa" je američki romantični komad iz 1979. godine, snimljen u tehnikoloru i panavizionu, u režiji Džordža Roj Hila. U filmu glume Lorens Olivije, Telonijus Bernard i Dajen Lejn u njenom filmskom debiju. Scenaristi s ... [truncated 225 chars](365 chars) |

## Dataset Information

| Field | Value |
| --- | --- |
| Nano set | MNanoBEIR |
| Backing dataset | NanoBEIR-sr |
| Task / split | NanoDBPedia |
| Hugging Face dataset | [hakari-bench/NanoBEIR-sr](https://huggingface.co/datasets/hakari-bench/NanoBEIR-sr) |
| Language | sr |
| Category | natural_language |
| Queries | 50 |
| Documents | 6,045 |
| Positive qrels | 1,158 |
| Positives per query avg | 23.16 |
| Positives per query min / median / max | 1 / 18.0 / 81 |
| Multi-positive queries | 48 (96.00%) |
| BM25 nDCG@10 | 0.4341 |
| BM25 hit@10 | 0.8800 |
| Query length avg chars | 41.18 |
| Document length avg chars | 338.86 |

### Public Sources

- [DBpedia Entity Retrieval](https://doi.org/10.1145/3077136.3080751).
- [BEIR: A Heterogeneous Benchmark for Zero-shot Evaluation of Information Retrieval Models](https://arxiv.org/abs/2104.08663).
- [MMTEB: Massive Multilingual Text Embedding Benchmark](https://arxiv.org/abs/2502.13595).
- [Zeta Alpha NanoBEIR collection](https://huggingface.co/collections/zeta-alpha-ai/nanobeir).

### Hugging Face Links

- Nano dataset: [hakari-bench/NanoBEIR-sr](https://huggingface.co/datasets/hakari-bench/NanoBEIR-sr)
- Source collection: [Zeta Alpha NanoBEIR collection](https://huggingface.co/collections/zeta-alpha-ai/nanobeir)

### Source Reference Table

| Title | Year | Type | URL |
| --- | ---: | --- | --- |
| DBpedia Entity Retrieval | 2017 | task paper | https://doi.org/10.1145/3077136.3080751 |
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
  backing_dataset: NanoBEIR-sr
  dataset_id: hakari-bench/NanoBEIR-sr
  task_name: NanoDBPedia
  split_name: NanoDBPedia
  language: sr
  category: natural_language
  document_path: docs/benchmark_tasks/MNanoBEIR/NanoBEIR-sr__NanoDBPedia.md
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
    query_mean: 41.18
    document_mean: 338.858561
  bm25:
    ndcg_at_10: 0.4341490171
    hit_at_10: 0.88
    source: dataset_bm25_column
```
