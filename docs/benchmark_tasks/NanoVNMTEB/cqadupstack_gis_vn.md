# NanoVNMTEB / cqadupstack_gis_vn

## Overview

CQADupStack evaluates retrieval of manually flagged duplicate community
questions; VN-MTEB brings the GIS subforum into Vietnamese via translation and
quality filtering. A short GIS title must retrieve the translated archived
thread that asks the same geospatial problem. The sampled examples include QGIS
C++ plugin debugging, splitting lines at vertices, JavaScript mapping library
comparisons, ArcGIS field-numbering scripts, and OpenLayers/WFS CORS issues, so
the model must align equivalent GIS workflows across tool names and code terms.

## Details

### What the Original Data Measures

[CQADupStack](https://doi.org/10.1145/2838931.2838934) was built to evaluate
automatic duplicate detection in community QA. It contains twelve StackExchange
subforums with predefined retrieval splits, where the output for a new question
is a ranked list of earlier duplicate questions.

The Vietnamese version comes from [VN-MTEB](https://aclanthology.org/2026.findings-eacl.86/),
which translates source benchmark samples and applies language, semantic
similarity, and LLM-judge filtering. The GIS split keeps the original
geospatial technical domain but presents the text in Vietnamese.

### Observed Data Profile

The Nano split has 200 queries, 10,000 documents, and 299 positive qrel rows.
The average is 1.50 positives per query; 39 queries have multiple positives and
the maximum is 22. Queries average 59.16 characters. Documents average 929.23
characters and often include code/tool names and longer problem descriptions.

Examples include QGIS C++ plugin debugging, splitting lines at vertices,
JavaScript mapping library comparisons, ArcGIS field numbering scripts, and
OpenLayers/WFS CORS or proxy issues. Many documents retain product names and
URLs alongside translated prose.

### BM25 Difficulty

Using the dataset-provided BM25 candidate column, BM25 reaches nDCG@10 = 0.3009
and hit@10 = 0.4300. This is difficult for BM25. Tool names help, but duplicate
questions can use different geospatial vocabulary, and many documents are long
enough to dilute the exact title terms.

Dense models should help when two questions describe the same workflow with
different phrasing, such as CORS and proxy errors or line-splitting operations.

### Training Data That May Help

Useful training data includes non-overlapping GIS duplicate-question pairs,
Vietnamese GIS support data, translated CQADupStack training splits with overlap
removed, and StackExchange-style geospatial QA pairs. Exclude the translated GIS
test questions, qrels, and document texts used by this Nano split.

Hard negatives should share the same tool or API but ask a different operation.

### Synthetic Data Guidance

For document-to-query generation, use non-evaluation GIS support threads and
generate Vietnamese duplicate titles. Preserve technical tokens such as QGIS,
ArcGIS, GeoServer, WFS, OpenLayers, coordinates, layers, and plugins.

For joint generation, create clusters of Vietnamese geospatial troubleshooting
questions with duplicate variants and same-tool non-duplicates. Include code or
configuration snippets when they are central to the retrieval intent.

## Example Data

| Query | Positive document |
| --- | --- |
| Tải nhiều tập tin shapefile vào PostGIS (39 chars) | lô hàng tải shp vào postgis > **Có thể trùng lặp:** > Tải khối nhiều tập tin hình dạng vào PostGIS Liệu có khả năng tải khối tập tin shp vào postgis. Hiện tại tôi đang thử nghiệm với postgis, qgis và geoserver (như một máy ch ... [truncated 225 chars](515 chars) |
| Có công cụ nào có thể lấy lại hệ tọa độ được dùng để tạo ra một shapefile khi file prj bị thiếu không? (102 chars) | Xác định hệ tọa độ của Shapefile khi chưa biết? Tôi có một Shapefile nhưng hệ tọa độ của nó là Unknown, và không có tệp *.prj. Làm thế nào tôi có thể xác định được bây giờ? Có công cụ nào có thể giúp đỡ không? (210 chars) |
| .tif và .tfw sang GeoTIFF (25 chars) | tfw tif to GeoTiff Làm thế nào để kết hợp một tệp .tif với một tệp .tfw để tạo GeoTiff? Có rất nhiều câu trả lời cho tôi sử dụng gdal, nhưng tôi không có ý tưởng. Vì vậy có ai có thể cung cấp một ví dụ từng bước về cách thực ... [truncated 225 chars](246 chars) |
| Chuyển đổi tệp CSV sang shapefile (33 chars) | Làm thế nào để tôi chuyển đổi một tệp csv của dữ liệu WKT sang một tệp hình dạng sử dụng ogr2ogr? Câu hỏi này liên quan đến Shapefiles to Text. Tôi có một tệp csv, với một cột, tất cả các hàng tương ứng với WKT POLYGON(): WKT ... [truncated 225 chars](619 chars) |
| Làm thế nào để tạo các điểm tính năng với tọa độ chính xác? (59 chars) | QGIS thêm điểm sử dụng độ thập phân Khi giấy phép được bán, chúng tôi cần thêm vị trí sử dụng lat/long. Chúng tôi đang làm việc trong ArcView nhưng muốn chuyển sang QGIS- Mọi thứ tôi có thể tìm thấy dường như chỉ liên quan đế ... [truncated 225 chars](539 chars) |

## Dataset Information

| Field | Value |
| --- | --- |
| Nano set | NanoVNMTEB |
| Backing dataset | NanoVNMTEB |
| Task / split | cqadupstack_gis_vn |
| Hugging Face dataset | [hakari-bench/NanoVNMTEB](https://huggingface.co/datasets/hakari-bench/NanoVNMTEB) |
| Source dataset | [GreenNode/cqadupstack-gis-vn](https://huggingface.co/datasets/GreenNode/cqadupstack-gis-vn) |
| Language | vi |
| Category | natural_language |
| Queries | 200 |
| Documents | 10,000 |
| Positive qrels | 299 |
| Avg positives / query | 1.50 |
| Positives per query (min / median / max) | 1 / 1 / 22 |
| Queries with multiple positives | 39 (19.50%) |
| BM25 nDCG@10 | 0.3038 |
| BM25 hit@10 | 0.4400 |
| BM25 Recall@100 | 0.6087 |
| BM25 candidate subset | top-500 (`bm25`) |
| Dense nDCG@10 | 0.3481 |
| Dense hit@10 | 0.5150 |
| Dense Recall@100 | 0.6555 |
| Dense candidate subset | top-500 (`harrier_oss_v1_270m`) |
| Reranking hybrid nDCG@10 | 0.3420 |
| Reranking hybrid hit@10 | 0.5250 |
| Reranking hybrid Recall@100 | 0.7391 |
| Reranking hybrid candidate subset | top-100 plus optional rank-101 safeguard (`reranking_hybrid`) |
| Reranking hybrid candidates / query | 100-101 |
| Reranking hybrid safeguard rows | 40 |
| Query length avg chars | 59.16 |
| Document length avg chars | 929.23 |

### Public Sources

- [CQADupStack: A Benchmark Data Set for Community Question-Answering Research](https://doi.org/10.1145/2838931.2838934), 2015.
- [VN-MTEB: Vietnamese Massive Text Embedding Benchmark](https://aclanthology.org/2026.findings-eacl.86/), 2026.
- [BEIR: A Heterogeneous Benchmark for Zero-shot Evaluation of Information Retrieval Models](https://arxiv.org/abs/2104.08663), 2021.
- [GreenNode/cqadupstack-gis-vn](https://huggingface.co/datasets/GreenNode/cqadupstack-gis-vn), source dataset card.

### Hugging Face Links

- Nano dataset: [hakari-bench/NanoVNMTEB](https://huggingface.co/datasets/hakari-bench/NanoVNMTEB)
- Source dataset: [GreenNode/cqadupstack-gis-vn](https://huggingface.co/datasets/GreenNode/cqadupstack-gis-vn)

### Source Reference Table

| Title | Year | Type | URL |
| --- | ---: | --- | --- |
| CQADupStack: A Benchmark Data Set for Community Question-Answering Research | 2015 | ACM paper | https://doi.org/10.1145/2838931.2838934 |
| VN-MTEB: Vietnamese Massive Text Embedding Benchmark | 2026 | ACL paper | https://aclanthology.org/2026.findings-eacl.86/ |
| BEIR: A Heterogeneous Benchmark for Zero-shot Evaluation of Information Retrieval Models | 2021 | arXiv paper | https://arxiv.org/abs/2104.08663 |
| GreenNode/cqadupstack-gis-vn |  | dataset card | https://huggingface.co/datasets/GreenNode/cqadupstack-gis-vn |

## Machine-Readable Metadata

<!-- benchmark-task-metadata:v1 -->

```yaml
benchmark_task_metadata:
  schema_version: 1
  document_status: first_pass
  nano_set: NanoVNMTEB
  backing_dataset: NanoVNMTEB
  dataset_id: hakari-bench/NanoVNMTEB
  task_name: cqadupstack_gis_vn
  split_name: cqadupstack_gis_vn
  language: vi
  category: natural_language
  document_path: docs/benchmark_tasks/NanoVNMTEB/cqadupstack_gis_vn.md
  source_research:
    primary_source_type: task_paper
    paper_pdf_or_html_checked: true
    paper_url: https://doi.org/10.1145/2838931.2838934
    additional_source_urls:
    - https://aclanthology.org/2026.findings-eacl.86/
    - https://arxiv.org/abs/2104.08663
    - https://huggingface.co/datasets/GreenNode/cqadupstack-gis-vn
    no_paper_note: null
  counts:
    queries: 200
    documents: 10000
    positive_qrels: 299
  positives_per_query:
    average: 1.495
    min: 1
    median: 1.0
    max: 22
    multi_positive_queries: 39
    multi_positive_query_percent: 19.5
  text_stats_chars:
    query_mean: 59.155
    document_mean: 929.2255
  bm25:
    ndcg_at_10: 0.3037590584054381
    hit_at_10: 0.44
    source: dataset_candidate_subset
  learning:
    original_train_split: available
    evaluation_split_origin: translated VN-MTEB CQADupStack GIS test split from GreenNode/cqadupstack-gis-vn
    train_eval_overlap_audit: not_audited
    leakage_note: Exclude translated GIS test questions, documents, qrels, and duplicate
      clusters used by this Nano split.
    useful_training_data:
    - non-overlapping GIS duplicate-question pairs
    - Vietnamese geospatial support QA
    - translated CQADupStack training splits with overlap removed
    - same-tool hard negatives for QGIS, ArcGIS, GeoServer, and OpenLayers
    synthetic_data:
      document_generation: Vietnamese GIS support threads with software names, configuration,
        coordinates, and map layers.
      question_generation: Short Vietnamese geospatial duplicate-question titles.
      answerability: Each query should have duplicate-thread positives and same-tool
        hard negatives.
    multi_positive_training: multi_positive_objective
  links:
    nano_dataset: https://huggingface.co/datasets/hakari-bench/NanoVNMTEB
    source_urls:
    - label: CQADupStack DOI
      url: https://doi.org/10.1145/2838931.2838934
    - label: VN-MTEB ACL Anthology
      url: https://aclanthology.org/2026.findings-eacl.86/
    - label: BEIR arXiv
      url: https://arxiv.org/abs/2104.08663
    - label: GreenNode/cqadupstack-gis-vn
      url: https://huggingface.co/datasets/GreenNode/cqadupstack-gis-vn
    source_notes: []
  references:
  - title: 'CQADupStack: A Benchmark Data Set for Community Question-Answering Research'
    url: https://doi.org/10.1145/2838931.2838934
    year: 2015
    doi: 10.1145/2838931.2838934
    is_paper: true
    source_confidence: definitive_paper_link
  - title: 'VN-MTEB: Vietnamese Massive Text Embedding Benchmark'
    url: https://aclanthology.org/2026.findings-eacl.86/
    year: 2026
    doi: 10.18653/v1/2026.findings-eacl.86
    is_paper: true
    source_confidence: definitive_paper_link
  - title: 'BEIR: A Heterogeneous Benchmark for Zero-shot Evaluation of Information
      Retrieval Models'
    url: https://arxiv.org/abs/2104.08663
    year: 2021
    doi: 10.48550/arXiv.2104.08663
    is_paper: true
    source_confidence: definitive_paper_link
  - title: GreenNode/cqadupstack-gis-vn
    url: https://huggingface.co/datasets/GreenNode/cqadupstack-gis-vn
    year: null
    doi: null
    is_paper: false
    source_confidence: probably_correct
  candidate_subsets:
    bm25:
      config: bm25
      label: BM25
      source: dataset_candidate_subset
      top_k: 500
      ndcg_at_10: 0.3037590584
      hit_at_10: 0.44
      recall_at_100: 0.6086956522
      candidate_count_min: 500
      candidate_count_max: 500
      candidate_count_mean: 500.0
      query_count: 200
      query_coverage: 1.0
      relevant_coverage_at_100: 0.6086956522
    dense:
      config: harrier_oss_v1_270m
      label: Dense
      source: dataset_candidate_subset
      top_k: 500
      ndcg_at_10: 0.34807068
      hit_at_10: 0.515
      recall_at_100: 0.6555183946
      candidate_count_min: 500
      candidate_count_max: 500
      candidate_count_mean: 500.0
      query_count: 200
      query_coverage: 1.0
      relevant_coverage_at_100: 0.6555183946
    reranking_hybrid:
      config: reranking_hybrid
      label: Reranking hybrid
      source: dataset_candidate_subset
      top_k: 100
      ndcg_at_10: 0.3419997502
      hit_at_10: 0.525
      recall_at_100: 0.7391304348
      candidate_count_min: 100
      candidate_count_max: 101
      candidate_count_mean: 100.2
      query_count: 200
      query_coverage: 1.0
      relevant_coverage_at_100: 0.7391304348
      safeguard_positive_rows: 40
      rows_with_101_candidates: 40
```
