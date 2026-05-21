# NanoMTEB-Polish / cqadupstack_gis

## Overview

CQADupStack frames this task family as duplicate-question retrieval in community
QA, and the Polish GIS split localizes that objective to geospatial software
questions. A short translated GIS title must retrieve a duplicate or equivalent
Stack Exchange post from longer Polish candidate threads. The observed data is
centered on ArcGIS, ArcPy, rasters, DEMs, shapefiles, styling, and
model-builder workflows, so the task requires matching the same geospatial
problem across tool names, data formats, and processing terminology.

## Details

### What the Original Data Measures

[CQADupStack: A Benchmark Data Set for Community Question-Answering Research](https://ir.webis.de/anthology/2015.adcs_conference-2015.3/)
defines the source family as community QA duplicate retrieval. The [MTEB paper](https://arxiv.org/abs/2210.07316)
places CQADupStack among retrieval benchmarks, but the exact Polish GIS split is
specified by the MTEB/CLARIN Polish dataset cards rather than a standalone paper.

### Observed Data Profile

The split contains 200 queries, 10,000 documents, and 313 positive qrels.
Queries average 60.61 characters and documents are relatively long, averaging
965.97 characters. Observed questions mention ArcMap model batches, DEM area
calculation, ArcObjects, shapefile styling, and partial raster replacement. Only
45 queries have multiple positives, so many information needs are narrow.

### BM25 Difficulty

BM25 reaches nDCG@10 = 0.2423 and hit@10 = 0.3800, with 36 positives at rank 1
and 76 in the top 10. This is a hard lexical task: specialized terms such as
DEM, ArcPy, or raster help, but duplicates often use different software
operations or symptoms for the same geospatial workflow.

### Training Data That May Help

Useful data includes GIS Stack Exchange duplicates, Polish GIS help content,
ArcGIS/QGIS documentation questions, and hard negatives with shared product
names but different spatial operations. Avoid training on the upstream test
queries, duplicate qrels, or positive posts.

### Synthetic Data Guidance

Generate Polish GIS troubleshooting posts and duplicate questions grounded in
specific geospatial operations: projection, raster algebra, DEM sampling,
shapefile attributes, and model-builder execution. Synthetic pairs should
preserve the exact operation and failure mode while changing software version,
layer names, and wording.

## Example Data

| Query | Positive document |
| --- | --- |
| Jak zmienić proporcje mapy bez zmiany skali? (44 chars) | Jak zmienić rozmiar elementu mapy w edytorze wydruku QGIS bez zmiany skali? Czy można zablokować skalę w kompozytorze wydruku QGIS 2.0.1? Za każdym razem, gdy zmieniam rozmiar mapy, skala jest dostosowywana. To sprawia, że ​​ ... [truncated 225 chars](286 chars) |
| Jak używać SRTM Global DEM do obliczania nachylenia? (52 chars) | jaki jest odpowiedni układ współrzędnych rzutowanych do WGS84? > **Możliwe duplikowanie:** > Obliczanie globalnego DEM na nachylenie Chcę obliczyć nachylenie z mojego globalnego DEM? DEM ma odwzorowanie WGS84 (stopnie). Aby p ... [truncated 225 chars](520 chars) |
| Skopiuj odpytywane atrybuty pliku kształtu do nowego pliku kształtu (67 chars) | Tworzenie rekordów w wyjściowym pliku kształtu za pomocą Pythona Mam listę (wyjście z poprzedniej pętli) zawierającą atrybuty z wejściowego pliku kształtu. To, z czym utknąłem, to wprowadzanie tych atrybutów do nowego pliku k ... [truncated 225 chars](1933 chars) |
| Konwertowanie pliku CSV do pliku kształtu (41 chars) | Jak mogę przekonwertować plik csv danych WKT na plik kształtu za pomocą programu ogr2ogr? To pytanie dotyczy plików Shape na tekst. Mam plik csv, z jedną kolumną, gdzie wszystkie wiersze odpowiadają WKT POLYGON(): WKT POLYGON ... [truncated 225 chars](579 chars) |
| Skrypty Pythona, które działają w ArcMap, a te, które działają na zewnątrz? (75 chars) | "EOFError: EOF podczas czytania linii" Używanie raw_input() w ArcMaps Python Console Piszę skrypt Pythona, aby zautomatyzować przetwarzanie niektórych danych ArcMaps. Dostaję się zawieszony na raw_input(). Aby uzyskać dane we ... [truncated 225 chars](739 chars) |

## Dataset Information

| Field | Value |
| --- | --- |
| Nano set | NanoMTEB-Polish |
| Backing dataset | NanoMTEB-Polish |
| Task / split | cqadupstack_gis |
| Hugging Face dataset | [hakari-bench/NanoMTEB-Polish](https://huggingface.co/datasets/hakari-bench/NanoMTEB-Polish) |
| Source dataset | [mteb/CQADupstack-Gis-PL](https://huggingface.co/datasets/mteb/CQADupstack-Gis-PL) |
| Language | pl |
| Category | natural_language |
| Queries | 200 |
| Documents | 10,000 |
| Positive qrels | 313 |
| Avg positives / query | 1.565 |
| Positives per query (min / median / max) | 1 / 1.0 / 22 |
| Queries with multiple positives | 45 (22.5%) |
| BM25 nDCG@10 | 0.2423 |
| BM25 hit@10 | 0.3800 |
| Query length avg chars | 60.61 |
| Document length avg chars | 965.97 |

### Public Sources

- [CQADupStack: A Benchmark Data Set for Community Question-Answering Research](https://ir.webis.de/anthology/2015.adcs_conference-2015.3/), original benchmark paper record.
- [MTEB: Massive Text Embedding Benchmark](https://arxiv.org/abs/2210.07316), benchmark paper covering CQADupStack retrieval tasks.
- [CLARIN-KNEXT cqadupstack-gis-pl](https://huggingface.co/datasets/clarin-knext/cqadupstack-gis-pl), Polish source dataset card.

### Hugging Face Links

- Nano dataset: [hakari-bench/NanoMTEB-Polish](https://huggingface.co/datasets/hakari-bench/NanoMTEB-Polish)
- Source task dataset: [mteb/CQADupstack-Gis-PL](https://huggingface.co/datasets/mteb/CQADupstack-Gis-PL)

### Source Reference Table

| Title | Year | Type | URL |
| --- | ---: | --- | --- |
| CQADupStack: A Benchmark Data Set for Community Question-Answering Research | 2015 | task paper | https://ir.webis.de/anthology/2015.adcs_conference-2015.3/ |
| MTEB: Massive Text Embedding Benchmark | 2022 | benchmark paper | https://arxiv.org/abs/2210.07316 |
| CLARIN-KNEXT cqadupstack-gis-pl |  | dataset card | https://huggingface.co/datasets/clarin-knext/cqadupstack-gis-pl |

## Machine-Readable Metadata

<!-- benchmark-task-metadata:v1 -->

```yaml
benchmark_task_metadata:
  schema_version: 1
  document_status: first_pass
  nano_set: NanoMTEB-Polish
  backing_dataset: NanoMTEB-Polish
  dataset_id: hakari-bench/NanoMTEB-Polish
  task_name: cqadupstack_gis
  split_name: cqadupstack_gis
  language: pl
  category: natural_language
  document_path: docs/benchmark_tasks/NanoMTEB-Polish/cqadupstack_gis.md
  source_research:
    primary_source_type: dataset_card
    paper_pdf_or_html_checked: true
    no_paper_note: no standalone paper for this Polish translated split was confirmed
  counts:
    queries: 200
    documents: 10000
    positive_qrels: 313
  positives_per_query:
    average: 1.565
    min: 1
    median: 1.0
    max: 22
    multi_positive_queries: 45
    multi_positive_query_percent: 22.5
  text_stats_chars:
    query_mean: 60.61
    document_mean: 965.9695
  bm25:
    ndcg_at_10: 0.2423
    hit_at_10: 0.38
    source: dataset_bm25_column
  example_count: 5
```
