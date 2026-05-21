# MNanoBEIR / NanoBEIR-sv / NanoDBPedia

## Overview

DBPedia Entity is an entity-oriented retrieval benchmark. `NanoBEIR-sv__NanoDBPedia`
uses Swedish translated entity needs to retrieve Swedish translated
DBpedia-style entity descriptions.

## Details

### What the Original Data Measures

[DBpedia-Entity](https://doi.org/10.1145/3077136.3080751) evaluates ranking
entities for information needs over DBpedia. BEIR includes it as entity
retrieval, and MMTEB supplies the multilingual context.

### Observed Data Profile

The sampled task has 50 queries, 6,045 documents, and 1,158 positive qrels.
Almost every query is multi-positive, averaging 23.16 positives and reaching 81.
Queries average 35.66 characters; documents average 327.04 characters.

### BM25 Difficulty

BM25 reaches nDCG@10 = 0.4339 and hit@10 = 0.9200. The median first-positive
rank is 2.0, showing that entity names are strong lexical anchors, while
complete ranking still needs alias and type awareness.

### Training Data That May Help

Useful supervision includes Swedish entity search, Wikipedia or DBpedia
retrieval, alias matching, and multilingual entity ranking. Exclude DBPedia
Entity, BEIR, NanoBEIR, and translated evaluation records.

### Synthetic Data Guidance

Generate Swedish entity needs with keyword and question forms. Hard negatives
should share entity type, occupation, place, or name fragments.

## Example Data

| Query | Positive document |
| --- | --- |
| Fitzgerald bilmuseet Chambersburg, PA (37 chars) | Fitzgerald Auto Malls är en familjeägd och driven bilhandelskedja som grundades 1966, med sin första plats öppnad i Bethesda, Maryland. År 2014 rankades Fitzgerald Auto Malls som nummer 59 på listan över de "Topp 125 Bilhande ... [truncated 225 chars](404 chars) |
| Samling av noveller från 1994 av Alice Munro är tillgänglig (59 chars) | Alice Ann Munro (/ˈælɨs ˌæn mʌnˈroʊ/, född Laidlaw /ˈleɪdlɔː/; född 10 juli 1931) är en kanadensisk författare. Munros verk har beskrivits som att ha förändrat novellens struktur, särskilt i dess tendens att röra sig framåt o ... [truncated 225 chars](470 chars) |
| Galloromansk arkitektur i Paris (31 chars) | Konst i Paris är en artikel om konstkultur och historia i Paris, Frankrikes huvudstad. Under århundraden har Paris lockat konstnärer från hela världen, som kommit till staden för att utbilda sig och finna inspiration från des ... [truncated 225 chars](331 chars) |
| De tidigare jugoslaviska republikerna (37 chars) | 1974 års jugoslaviska konstitution var den fjärde och sista konstitutionen för den socialistiska federala republiken Jugoslavien. Den trädde i kraft den 21 februari. Med sina 406 ursprungliga artiklar var den 1974 års konstit ... [truncated 225 chars](455 chars) |
| Filmer inspelade i Venedig (26 chars) | A Little Romance är en amerikansk romantisk komedifilm från 1979 i Technicolor och Panavision, regisserad av George Roy Hill och med Laurence Olivier, Thelonious Bernard och Diane Lane i hennes filmdebut. Manus skrevs av Alla ... [truncated 225 chars](370 chars) |

## Dataset Information

| Field | Value |
| --- | --- |
| Nano set | MNanoBEIR |
| Backing dataset | NanoBEIR-sv |
| Task / split | NanoDBPedia |
| Hugging Face dataset | [hakari-bench/NanoBEIR-sv](https://huggingface.co/datasets/hakari-bench/NanoBEIR-sv) |
| Language | sv |
| Category | natural_language |
| Queries | 50 |
| Documents | 6,045 |
| Positive qrels | 1,158 |
| Positives per query avg | 23.16 |
| Positives per query min / median / max | 1 / 18.0 / 81 |
| Multi-positive queries | 48 (96.00%) |
| BM25 nDCG@10 | 0.4339 |
| BM25 hit@10 | 0.9200 |
| Query length avg chars | 35.66 |
| Document length avg chars | 327.04 |

### Public Sources

- [DBpedia Entity Retrieval](https://doi.org/10.1145/3077136.3080751), [BEIR](https://arxiv.org/abs/2104.08663), [MMTEB](https://arxiv.org/abs/2502.13595), and [NanoBEIR](https://huggingface.co/collections/zeta-alpha-ai/nanobeir).

### Hugging Face Links

- Nano dataset: [hakari-bench/NanoBEIR-sv](https://huggingface.co/datasets/hakari-bench/NanoBEIR-sv)
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
  backing_dataset: NanoBEIR-sv
  dataset_id: hakari-bench/NanoBEIR-sv
  task_name: NanoDBPedia
  split_name: NanoDBPedia
  language: sv
  category: natural_language
  document_path: docs/benchmark_tasks/MNanoBEIR/NanoBEIR-sv__NanoDBPedia.md
  source_research: {primary_source_type: task_paper, paper_pdf_or_html_checked: true, no_paper_note: null}
  counts: {queries: 50, documents: 6045, positive_qrels: 1158}
  positives_per_query: {average: 23.16, min: 1, median: 18.0, max: 81, multi_positive_queries: 48, multi_positive_query_percent: 96.0}
  text_stats_chars: {query_mean: 35.66, document_mean: 327.037883}
  bm25: {ndcg_at_10: 0.4339285948, hit_at_10: 0.92, source: dataset_bm25_column}
```
