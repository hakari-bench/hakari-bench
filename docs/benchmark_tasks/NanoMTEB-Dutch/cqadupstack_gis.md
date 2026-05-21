# NanoMTEB-Dutch / cqadupstack_gis

## Overview

`cqadupstack_gis` is the Dutch-translated GIS subforum split of CQADupStack.
Queries are geospatial software questions and positive documents are older
Stack Exchange questions marked as duplicates. The task tests duplicate-question
retrieval for GIS workflows, QGIS, PostGIS, projections, raster/vector
operations, and map export issues.

## Details

### What the Original Data Measures

[CQADupStack: A Benchmark Data Set for Community Question-Answering Research](https://doi.org/10.1145/2838931.2838934)
builds a duplicate-question benchmark from twelve StackExchange subforums and
provides chronological retrieval splits in which later questions are matched
against earlier indexed questions. The paper notes that subforums differ
substantially in topic and question length, which matters here because GIS posts
often contain software versions, data formats, and workflow details.

[BEIR-NL](https://aclanthology.org/2025.bucc-1.5/) translates BEIR datasets into
Dutch for zero-shot retrieval evaluation. This split is therefore translated
Dutch GIS text, not native Dutch GIS forum data, while retaining the original
CQADupStack duplicate links.

### Observed Data Profile

The Nano split has 200 queries, 10,000 documents, and 200 positive qrel rows.
Each query has one positive. Queries average 62.70 characters. Documents average
1,036.05 characters, making this one of the longer CQADupStack Dutch subforums.
Examples include PostGIS speed, QGIS coordinate extraction, OpenLayers print
exports, offline plugin installation, and raster values in polygon zones.

The positive documents frequently contain product names, version numbers,
commands, shapefile/raster terminology, and long descriptions of attempted
workflows. A model must retrieve the duplicate troubleshooting intent, not just
the same software name.

### BM25 Difficulty

Using the dataset-provided BM25 candidate column, BM25 reaches nDCG@10 = 0.2790
and hit@10 = 0.3700. Technical tokens such as PostGIS, QGIS, shapefile, and
OpenLayers help BM25, but the long documents dilute signals and many posts use
different descriptions for the same geospatial operation.

### Training Data That May Help

Useful training data includes non-overlapping GIS Stack Exchange duplicate
pairs, Dutch-translated geospatial support QA, and technical duplicate-question
pairs with software/version metadata preserved. Exclude the translated test
queries and positives used by this Nano split.

### Synthetic Data Guidance

Generate Dutch GIS troubleshooting questions from non-evaluation GIS posts.
Synthetic duplicates should vary software names, workflow wording, coordinate
system terms, and file formats while preserving the same underlying problem.
Use same-tool hard negatives that ask about related but different operations.

## Example Data

| Query | Positive document |
| --- | --- |
| Hoe verander ik de beeldverhouding van een kaart zonder dat de schaal verandert? (80 chars) | Hoe de grootte van het kaart item in de QGIS print composer aan te passen zonder de schaal te veranderen? Is het mogelijk om de schaal te vergrendelen in de QGIS 2.0.1 print composer? Elke keer dat ik de kaart verplaats, word ... [truncated 225 chars](321 chars) |
| Hoe gebruik ik SRTM Global DEM voor hellingberekening? (54 chars) | GTOPO30 hellinganalyse in ArcGIS 10.1 Gebruikmakend van de gereedschapskist oppervlakte - hellinganalyse. Alle waarden voor de hellingberekening liggen tussen 80 en 89. Er zijn geen waarden onder de 80. Wat doe ik verkeerd? (224 chars) |
| Attributen van een shapefile kopiëren naar een nieuw shapefile (62 chars) | Records aanmaken in een output shapefile met behulp van Python Ik heb een lijst (output van een eerdere loop) met attributen van een input shapefile. Waar ik vastloop is het invoeren van die attributen in een nieuwe shapefile ... [truncated 225 chars](2511 chars) |
| Het converteren van een CSV naar een shapefile (46 chars) | Hoe kan ik een CSV-bestand met WKT-gegevens converteren naar een shapefile met ogr2ogr? Deze vraag heeft betrekking op Shapefiles naar tekst. Ik heb een CSV-bestand met één kolom, waarin alle rijen overeenkomen met WKT POLYGO ... [truncated 225 chars](653 chars) |
| Python-scripts die binnen ArcMap draaien versus die erbuiten draaien? (69 chars) | "EOFError: EOF when reading a line" Gebruik van raw_input() in de ArcMaps Python Console Ik schrijf een Python-script om sommige ArcMaps-gegevensverwerking te automatiseren. Ik loop vast bij raw_input(). Ik gebruik raw_input ... [truncated 225 chars](729 chars) |

## Dataset Information

| Field | Value |
| --- | --- |
| Nano set | NanoMTEB-Dutch |
| Backing dataset | NanoMTEB-Dutch |
| Task / split | cqadupstack_gis |
| Hugging Face dataset | [hakari-bench/NanoMTEB-Dutch](https://huggingface.co/datasets/hakari-bench/NanoMTEB-Dutch) |
| Source dataset | [clips/beir-nl-cqadupstack](https://huggingface.co/datasets/clips/beir-nl-cqadupstack) |
| Language | nl |
| Category | natural_language |
| Queries | 200 |
| Documents | 10,000 |
| Positive qrels | 200 |
| BM25 nDCG@10 | 0.2790 |
| BM25 hit@10 | 0.3700 |
| Query length avg chars | 62.70 |
| Document length avg chars | 1,036.05 |

### Public Sources

- [CQADupStack: A Benchmark Data Set for Community Question-Answering Research](https://doi.org/10.1145/2838931.2838934), 2015.
- [Author-hosted CQADupStack PDF](https://eltimster.github.io/www/pubs/adcs2015.pdf), 2015.
- [BEIR-NL: Zero-shot Information Retrieval Benchmark for the Dutch Language](https://aclanthology.org/2025.bucc-1.5/), 2025.
- [BEIR: A Heterogeneous Benchmark for Zero-shot Evaluation of Information Retrieval Models](https://arxiv.org/abs/2104.08663), 2021.
- [clips/beir-nl-cqadupstack](https://huggingface.co/datasets/clips/beir-nl-cqadupstack), source dataset card.

### Hugging Face Links

- Nano dataset: [hakari-bench/NanoMTEB-Dutch](https://huggingface.co/datasets/hakari-bench/NanoMTEB-Dutch)
- Source dataset: [clips/beir-nl-cqadupstack](https://huggingface.co/datasets/clips/beir-nl-cqadupstack)

### Source Reference Table

| Title | Year | Type | URL |
| --- | ---: | --- | --- |
| CQADupStack: A Benchmark Data Set for Community Question-Answering Research | 2015 | proceedings paper | https://doi.org/10.1145/2838931.2838934 |
| BEIR-NL: Zero-shot Information Retrieval Benchmark for the Dutch Language | 2025 | proceedings paper | https://aclanthology.org/2025.bucc-1.5/ |
| BEIR: A Heterogeneous Benchmark for Zero-shot Evaluation of Information Retrieval Models | 2021 | arXiv paper | https://arxiv.org/abs/2104.08663 |
| clips/beir-nl-cqadupstack |  | dataset card | https://huggingface.co/datasets/clips/beir-nl-cqadupstack |

## Machine-Readable Metadata

<!-- benchmark-task-metadata:v1 -->

```yaml
benchmark_task_metadata:
  schema_version: 1
  document_status: first_pass
  nano_set: NanoMTEB-Dutch
  backing_dataset: NanoMTEB-Dutch
  dataset_id: hakari-bench/NanoMTEB-Dutch
  task_name: cqadupstack_gis
  split_name: cqadupstack_gis
  language: nl
  category: natural_language
  document_path: docs/benchmark_tasks/NanoMTEB-Dutch/cqadupstack_gis.md
  source_research:
    primary_source_type: task_paper
    paper_pdf_or_html_checked: true
    paper_url: https://doi.org/10.1145/2838931.2838934
    additional_source_urls:
      - https://eltimster.github.io/www/pubs/adcs2015.pdf
      - https://aclanthology.org/2025.bucc-1.5/
      - https://arxiv.org/abs/2104.08663
      - https://huggingface.co/datasets/clips/beir-nl-cqadupstack
  counts:
    queries: 200
    documents: 10000
    positive_qrels: 200
  positives_per_query:
    average: 1.0
    min: 1
    median: 1.0
    max: 1
    multi_positive_queries: 0
    multi_positive_query_percent: 0.0
  text_stats_chars:
    query_mean: 62.705
    document_mean: 1036.0503
  bm25:
    ndcg_at_10: 0.2790339168
    hit_at_10: 0.37
    source: dataset_bm25_column
  learning:
    original_train_split: available
    evaluation_split_origin: "CQADupstackGis-NL test split from clips/beir-nl-cqadupstack"
    train_eval_overlap_audit: not_audited
    leakage_note: "Exclude translated CQADupStack GIS test queries and duplicate positives used by this Nano split."
    useful_training_data:
      - non-overlapping CQADupStack GIS duplicate-question pairs
      - Dutch-translated geospatial support QA
      - technical duplicate-question retrieval data with software metadata
    synthetic_data:
      document_generation: "Dutch GIS troubleshooting posts outside the evaluation set."
      question_generation: "Paraphrased duplicate GIS workflow questions."
      answerability: "Each generated query should duplicate one prior GIS problem, with same-tool hard negatives."
    multi_positive_training: single_positive
  example_count: 5
```
