# NanoMTEB-Polish / cqadupstack_gis

## Overview

`cqadupstack_gis` is the Polish NanoMTEB version of the GIS subset from CQADupStack, a duplicate-question retrieval benchmark built from Stack Exchange community QA data. The task asks a model to retrieve geospatial questions that are duplicates of a short Polish query. The subject matter is specialized: ArcGIS, QGIS, ArcPy, raster processing, DEMs, shapefiles, coordinate systems, styling, model-builder workflows, and spatial data conversion. Relevance is not ordinary topical similarity; a relevant document should ask the same geospatial problem, even if the software version, layer name, or data-processing description differs.

The Nano split contains 200 queries, 10,000 documents, and 313 positive relevance judgments. Queries average about 61 characters, while documents average about 966 characters, making this a short-query to long-document retrieval task. Only 45 queries have multiple positives, and the median number of positives is 1, so many information needs are narrow. At the same time, the maximum of 22 positives shows that some GIS problems form broader duplicate clusters.

## Details

### What the Original Data Measures

CQADupStack evaluates duplicate-question retrieval in community question answering forums. In the GIS subset, the relevant relation is defined by duplicate or equivalent geospatial questions. A post about converting a CSV to a shapefile is relevant to another post asking the same conversion problem, not to every post mentioning CSV or shapefiles. Likewise, a query about DEM slope calculation should retrieve documents about the same raster-processing issue, not merely any DEM-related thread.

This task is valuable for retrieval-model research because GIS questions combine domain terminology with procedural intent. A successful model must recognize tool names and data formats, but it must also understand the operation being requested: projection, conversion, clipping, attribute transfer, raster replacement, map-layout scaling, or Python automation inside ArcMap.

### Observed Data Profile

The documents are relatively long for a CQADupStack split. Candidate posts often include background context, partial code, software versions, error symptoms, or attempted workflows. This increases the chance that irrelevant documents share many terms with the query. A document can mention QGIS, shapefiles, WGS84, or ArcPy and still ask a different question.

The Polish translation introduces morphological variation while preserving many English technical tokens and software names. Terms such as DEM, ArcPy, SRTM, WGS84, CSV, WKT, and QGIS remain strong anchors, but Polish verbs and noun phrases describe the actual operation. The task therefore mixes exact technical matching with semantic recognition of geospatial workflows.

### BM25 Evaluation Profile

BM25 reaches nDCG@10 of 0.2423, hit@10 of 0.3800, and recall@100 of 0.5048. Its recall is not poor because GIS queries often contain distinctive technical tokens. Exact overlap on software names, file formats, coordinate systems, and spatial data terms can bring many relevant documents into the candidate set.

The weakness appears in top-rank ordering. BM25 can overvalue documents that share GIS vocabulary but do not ask the same operation. For example, a shapefile query may concern conversion, styling, attribute transfer, geometry creation, or projection repair. Word frequency alone does not reliably distinguish these intents. This explains why BM25 can preserve some positives at top 100 while still producing modest nDCG@10.

### Dense Evaluation Profile

The dense `harrier-oss-270m` run improves to nDCG@10 of 0.2861, hit@10 of 0.4500, and recall@100 of 0.5527. Dense retrieval appears better at connecting descriptions of the same GIS workflow when the wording differs. It can match a query about calculating slope from SRTM DEM data to documents that discuss coordinate systems, raster units, and slope computation without requiring exact phrasing.

The improvement is meaningful but not decisive. GIS terminology is precise, and dense similarity can still confuse related operations within the same software environment. A model may retrieve a semantically adjacent QGIS or ArcGIS thread that is not a duplicate. The dense profile therefore suggests that semantic modeling helps, but domain-specific operation matching remains difficult.

### Reranking Hybrid Evaluation Profile

`reranking_hybrid` is strongest on this task, with nDCG@10 of 0.3143, hit@10 of 0.4800, and recall@100 of 0.6198. Candidate lists contain 100 to 101 documents, and 56 rows use the relevance safeguard. This result indicates that lexical and dense candidates are complementary: BM25 contributes exact technical anchors, while dense retrieval contributes semantically related workflow descriptions.

For reranking research, this is the most informative profile. The hybrid candidate set better represents what a production first-stage system would want: enough exact matches to preserve software-specific terms, plus enough semantic matches to recover paraphrased duplicate questions. The top-10 hybrid gain suggests that the fusion is not only improving recall; it is also placing more true duplicates near the top.

### Metric Interpretation for Model Researchers

This task is hybrid-favorable. BM25 alone has useful recall but weak top-10 quality. Dense retrieval improves both ranking and recall, but `reranking_hybrid` is best across the reported metrics. A model that performs well here likely handles both domain-specific lexical evidence and procedural semantic similarity.

The gap between recall@100 and nDCG@10 is also important. A first-stage retriever can find relevant GIS documents somewhere in the top 100, yet still fail to rank them above same-topic negatives. Researchers should treat this subset as a strong test for rerankers, especially rerankers that must distinguish "same software and data format" from "same geospatial problem."

### Query and Relevance Type Tendencies

Representative queries ask how to change a map's aspect ratio without changing scale, calculate slope from global DEM data, copy queried shapefile attributes into a new shapefile, convert CSV or WKT data into shapefiles, or run Python scripts inside and outside ArcMap. These are operational questions. Their relevant documents often contain longer descriptions of the same procedure, including software constraints and examples.

The task is sensitive to data-format and operation words. A model must preserve distinctions between converting, styling, joining, copying, projecting, clipping, and calculating. It must also recognize that a short query can map to a longer post where the actual duplicate intent is embedded in an attempted workflow.

### Representative Failure Modes

Lexical systems may retrieve documents that share terms like shapefile, raster, DEM, or QGIS but solve a different geospatial task. Dense systems may retrieve posts with a similar spatial-analysis theme while missing that the required operation is different. Both failure modes are common when documents are long and contain many domain terms.

Another failure mode is overfitting to software names. ArcGIS, ArcMap, and QGIS are strong cues, but duplicates can sometimes be defined by the data operation rather than the platform. Conversely, two posts can describe similar operations in different tools but still not be duplicates if the software-specific behavior is the focus of the question.

### Training Data That May Help

Useful training data includes GIS Stack Exchange duplicate pairs, Polish GIS documentation questions, translated geospatial troubleshooting posts, and hard negatives that share the same software and file format but ask different operations. Data with short titles matched to longer forum posts would be especially useful.

Hard negatives should include near misses such as multiple shapefile conversion tasks, multiple DEM tasks, or multiple ArcPy automation questions. These examples teach a model to distinguish topical overlap from true duplicate relevance.

### Model Improvement Notes

Dense models can improve by representing procedural intent in technical domains: what operation is being attempted, what input data is involved, and what output or failure state is expected. Sparse systems can improve through better Polish tokenization and handling of GIS abbreviations, but exact matching alone is not enough for strong top-10 ranking.

Hybrid systems are well suited to this task. The observed metrics suggest that a balanced candidate pool followed by a stronger reranker is likely to outperform either lexical or dense retrieval alone. Researchers should track whether improvements come from higher recall@100, better top-10 ordering, or both.

## Example Data

| Query | Positive document |
| --- | --- |
| Jak zmienić proporcje mapy bez zmiany skali? [44 chars] | Jak zmienić rozmiar elementu mapy w edytorze wydruku QGIS bez zmiany skali? Czy można zablokować skalę w kompozytorze wydruku QGIS 2.0.1? Za każdym razem, gdy zmieniam rozmiar mapy, skala jest dostosowywana. To sprawia, że ​​wypróbowywanie różnych układów map jest naprawdę denerwujące. [286 chars] |
| Jak używać SRTM Global DEM do obliczania nachylenia? [52 chars] | jaki jest odpowiedni układ współrzędnych rzutowanych do WGS84? > **Możliwe duplikowanie:** > Obliczanie globalnego DEM na nachylenie Chcę obliczyć nachylenie z mojego globalnego DEM? DEM ma odwzorowanie WGS84 (stopnie). Aby poprawnie obliczyć nachylenie z DEM, musi być rzutowana współrzędna system, a nie układ współrzędnych geograficznych.Naprawdę trudno powiedzieć, który z rzutów na liście: rzutowane układy współrzędnych odpowiada układowi WGS84(world) pod listą układów współrzędnych geograficznych.Jakieś pomysły? [520 chars] |
| Skopiuj odpytywane atrybuty pliku kształtu do nowego pliku kształtu [67 chars] | Tworzenie rekordów w wyjściowym pliku kształtu za pomocą Pythona Mam listę (wyjście z poprzedniej pętli) zawierającą atrybuty z wejściowego pliku kształtu. To, z czym utknąłem, to wprowadzanie tych atrybutów do nowego pliku kształtu. Wykreśliłem dane punktowe za pomocą `w.point(x, y)`, a także stworzyłem odpowiednie pola `w.field()` z pól wejściowych pliku kształtu. Tam, gdzie utknąłem, jest kopia rekordów, która daje mi błąd związany z flagą usunięcia. > AttributeError: obiekt 'tuple' nie ma atrybutu 'startswith' Wklejam fragment kodu z moimi zapytaniami. from datetime import datetime import osgeo.ogr, osgeo.ogr z osgeo import ogr z osgeo import gdal import shapefile import os sf = shapefile.Reader("-- Lokalizacja pliku wejściowego --") # Czytanie pól Shapefile = sf.fields # Odczytywanie pól atrybutów records = sf.records() # Odczytywanie rekordów funkcji shapRecs = sf.shapeRecords() # Odczytuj jednocześnie geometrię i rekordy w = shapefile.Writer(shapefile.POINT) w.autoBalance = 1 wy... [1,000 / 1,933 chars] |

### Source Reference Table

| Source | What it contributes |
| --- | --- |
| CQADupStack paper | Original community QA duplicate-retrieval construction. |
| MTEB paper | Benchmark framing for retrieval evaluation. |
| CLARIN-KNEXT dataset card | Polish translated GIS subset. |
| MTEB task card | Task packaging and dataset interface. |

### Representative Snippets

- A query asks how to change a map's aspect ratio without changing scale; relevant documents discuss locking map scale in QGIS print layout workflows.
- A query asks how to use SRTM Global DEM data to calculate slope; relevant posts discuss coordinate systems and global DEM slope computation.
- A query asks how to copy queried shapefile attributes into a new shapefile; relevant documents describe creating records from selected attributes with Python.
- A query asks how to convert CSV data to a shapefile; relevant posts discuss WKT, CSV columns, and `ogr2ogr` conversion.
- A query asks about Python scripts that behave differently inside and outside ArcMap; relevant posts describe ArcMap console input behavior and automation constraints.
