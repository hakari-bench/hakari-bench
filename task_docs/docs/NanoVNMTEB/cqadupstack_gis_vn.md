# NanoVNMTEB / cqadupstack_gis_vn

## Overview

`cqadupstack_gis_vn` is a Vietnamese duplicate-question retrieval task from NanoVNMTEB. The query is a short translated GIS question title, and the relevant documents are archived GIS StackExchange questions marked as duplicates. The task requires matching equivalent geospatial workflows across tools such as QGIS, ArcGIS, GeoServer, OpenLayers, WFS, shapefiles, and coordinate systems. Dense retrieval slightly improves nDCG@10 over BM25, while `reranking_hybrid` has the best hit@10 and recall@100.

## Details

### What the Original Data Measures

CQADupStack evaluates duplicate retrieval in community question answering. The GIS split focuses on geospatial technical questions, where duplicates may describe the same operation using different software, terminology, or configuration details.

VN-MTEB translates the task into Vietnamese while preserving technical terms and product names. The resulting benchmark tests translated geospatial duplicate retrieval.

### Observed Data Profile

The Nano split contains 200 queries, 10,000 documents, and 299 positive qrel rows. Queries average 59.16 characters, while documents average 929.23 characters. Positives per query average 1.50, with a minimum of 1, a median of 1, and a maximum of 22. There are 39 multi-positive queries, 19.5% of the split.

Example queries ask about bulk loading shapefiles into PostGIS, recovering a coordinate system when a `.prj` file is missing, converting `.tif` and `.tfw` to GeoTIFF, converting CSV WKT data to shapefile, and creating feature points with exact coordinates.

### BM25 Evaluation Profile

The BM25 candidate subset uses top-500 candidates and reaches nDCG@10 of 0.3038, hit@10 of 0.4400, and recall@100 of 0.6087. BM25 benefits from geospatial tool names, file extensions, coordinate terms, and API names.

The limitation is that duplicate GIS questions can use different workflows or software terms to describe the same underlying task. Long documents can also dilute the short title terms.

### Dense Evaluation Profile

The dense candidate subset from `harrier_oss_v1_270m` uses top-500 candidates and reaches nDCG@10 of 0.3481, hit@10 of 0.5150, and recall@100 of 0.6555. Dense retrieval has the best nDCG@10.

This shows that semantic matching helps align duplicate geospatial tasks even when they use different wording, such as coordinate-system identification, file conversion, or layer loading.

### Reranking Hybrid Evaluation Profile

The `reranking_hybrid` subset uses top-100 candidates, with 40 rows receiving the optional rank-101 safeguard. It reaches nDCG@10 of 0.3420, hit@10 of 0.5250, and recall@100 of 0.7391. Hybrid retrieval has the best hit@10 and recall@100.

Sparse terms recover tool-specific candidates, while dense retrieval helps with workflow paraphrases. The hybrid pool is therefore the best source when a reranker can evaluate actual duplicate equivalence.

### Metric Interpretation for Model Researchers

Because some queries have multiple positives, nDCG@10 measures early duplicate ranking, hit@10 measures whether at least one duplicate is found, and recall@100 measures how much of the duplicate cluster is available.

For `cqadupstack_gis_vn`, recall@100 is important because geospatial tasks often have several archived variants with different titles and tool-specific wording.

### Query and Relevance Type Tendencies

Queries are short Vietnamese GIS question titles. Relevant documents are longer translated community questions with software names, configuration, coordinates, map layers, file formats, and sometimes code snippets.

Relevance is duplicate-question equivalence, not broad GIS topicality. A document about the same tool is wrong if it solves a different operation.

### Representative Failure Modes

Common failures include matching the same GIS software but wrong task, confusing file conversion with coordinate-system repair, overmatching extensions such as `.tif` or shapefile, and missing paraphrased workflow descriptions. BM25 overweights exact tools; dense retrieval can confuse related geospatial operations.

### Training Data That May Help

Useful training data includes non-overlapping GIS duplicate-question pairs, Vietnamese geospatial support QA, translated CQADupStack training splits with overlap removed, and hard negatives from the same tools such as QGIS, ArcGIS, GeoServer, and OpenLayers. Evaluation queries, documents, qrels, and duplicate clusters should be excluded.

### Model Improvement Notes

Models should encode geospatial operation type, software context, file format, coordinate system, and error condition. Hard negatives should share the same tool or file format but ask a different operation. Hybrid retrieval is the best high-recall candidate source.

## Example Data

| Query | Positive document |
| --- | --- |
| Tải nhiều tập tin shapefile vào PostGIS [39 chars] | lô hàng tải shp vào postgis > **Có thể trùng lặp:** > Tải khối nhiều tập tin hình dạng vào PostGIS Liệu có khả năng tải khối tập tin shp vào postgis. Hiện tại tôi đang thử nghiệm với postgis, qgis và geoserver (như một máy chủ arcgis tiềm năng, thay thế arcmap và arcsde) và muốn tôi có thể chạy một tập tin lô (tôi đoán) sẽ tải lên một số tập tin shp (xuất khẩu từ arcsde) ghi đè các tập tin shapfile / bảng hiện có trong postgis. Về hiệu ứng postgis sẽ là một cơ sở dữ liệu nô lệ (cho thời gian hiện tại). Med [515 chars] |
| Có công cụ nào có thể lấy lại hệ tọa độ được dùng để tạo ra một shapefile khi file prj bị thiếu không? [102 chars] | Xác định hệ tọa độ của Shapefile khi chưa biết? Tôi có một Shapefile nhưng hệ tọa độ của nó là Unknown, và không có tệp *.prj. Làm thế nào tôi có thể xác định được bây giờ? Có công cụ nào có thể giúp đỡ không? [210 chars] |
| .tif và .tfw sang GeoTIFF [25 chars] | tfw tif to GeoTiff Làm thế nào để kết hợp một tệp .tif với một tệp .tfw để tạo GeoTiff? Có rất nhiều câu trả lời cho tôi sử dụng gdal, nhưng tôi không có ý tưởng. Vì vậy có ai có thể cung cấp một ví dụ từng bước về cách thực hiện điều này không? [246 chars] |

### Source Reference Table

| Title | Year | Type | URL |
| --- | ---: | --- | --- |
| CQADupStack: A Benchmark Data Set for Community Question-Answering Research | 2015 | ACM paper | [https://doi.org/10.1145/2838931.2838934](https://doi.org/10.1145/2838931.2838934) |
| VN-MTEB: Vietnamese Massive Text Embedding Benchmark | 2026 | ACL paper | [https://aclanthology.org/2026.findings-eacl.86/](https://aclanthology.org/2026.findings-eacl.86/) |
| BEIR: A Heterogeneous Benchmark for Zero-shot Evaluation of Information Retrieval Models | 2021 | arXiv paper | [https://arxiv.org/abs/2104.08663](https://arxiv.org/abs/2104.08663) |
| GreenNode/cqadupstack-gis-vn |  | dataset card | [https://huggingface.co/datasets/GreenNode/cqadupstack-gis-vn](https://huggingface.co/datasets/GreenNode/cqadupstack-gis-vn) |

### Representative Snippets

| Query | Relevant document excerpt |
| --- | --- |
| Tải nhiều tập tin shapefile vào PostGIS | Thread about bulk loading shapefiles into PostGIS. |
| Có công cụ nào có thể lấy lại hệ tọa độ khi file prj bị thiếu không? | Thread about identifying an unknown shapefile coordinate system. |
| .tif và .tfw sang GeoTIFF | Thread about combining `.tif` and `.tfw` files into GeoTIFF. |
| Chuyển đổi tệp CSV sang shapefile | Thread about using `ogr2ogr` to convert WKT CSV data to shapefile. |
| Làm thế nào để tạo các điểm tính năng với tọa độ chính xác? | Thread about adding points with exact latitude and longitude coordinates. |
