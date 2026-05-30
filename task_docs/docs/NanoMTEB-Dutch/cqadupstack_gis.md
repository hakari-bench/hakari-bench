# NanoMTEB-Dutch / cqadupstack_gis

## Overview

`cqadupstack_gis` is the Dutch-translated GIS subforum split of CQADupStack.
Queries are geospatial software support questions, and positive documents are
older Stack Exchange questions marked as duplicates. The Nano split contains
200 queries, 10,000 documents, and 200 positive qrel rows, with one positive
duplicate for every query. It evaluates duplicate-question retrieval for GIS
workflows involving QGIS, PostGIS, ArcGIS, OpenLayers, coordinate systems,
shapefiles, rasters, map export, and spatial data processing.

The task is technical, long-document, and duplicate-intent oriented. BM25 can
use software names and file-format terms, but many documents are long and
contain workflow details that dilute exact-match signals. Dense retrieval with
`harrier_oss_v1_270m` improves both top-10 and top-100 performance, while
`reranking_hybrid` is strongest overall, combining technical lexical anchors
with semantic workflow matching. This makes the split a practical test of
hybrid retrieval for translated geospatial support data.

## Details

### What the Original Data Measures

[CQADupStack: A Benchmark Data Set for Community Question-Answering Research](https://doi.org/10.1145/2838931.2838934)
builds retrieval and classification tasks from Stack Exchange duplicate links.
In the retrieval formulation, a later question is used as the query and the
system must retrieve an older question marked as its duplicate. The GIS
subforum is especially workflow-heavy: posts often include software versions,
commands, data formats, projections, and descriptions of attempted procedures.

BEIR standardized CQADupStack as part of a heterogeneous retrieval benchmark,
and BEIR-NL translated the public BEIR datasets into Dutch. This Nano task
therefore preserves the original duplicate labels while presenting translated
Dutch GIS questions and documents. Code-like tokens, software names, and file
extensions often remain recognizable, but the surrounding explanatory text is
Dutch.

### Observed Data Profile

The split contains 200 queries and 10,000 documents. Queries average 62.70
characters, while documents average 1,036.05 characters, making this one of the
longer Dutch CQADupStack splits. Positive documents can contain multi-step
problem descriptions, attempted commands, data examples, and contextual
software details.

Representative questions ask how to change a map aspect ratio without changing
scale, how to use SRTM Global DEM for slope calculation, how to copy shapefile
attributes into a new shapefile, how to convert CSV data to a shapefile, and
how Python scripts differ inside and outside ArcMap. These examples show that
the retrieval target is usually a duplicate workflow, not just a shared product
name.

### BM25 Evaluation Profile

BM25 reaches nDCG@10 = 0.2790, hit@10 = 0.3700, and recall@100 = 0.6000 over
top-500 candidate lists. Sparse retrieval has meaningful signals in this task:
terms such as QGIS, PostGIS, ArcGIS, OpenLayers, shapefile, raster, CSV, WKT,
and DEM can strongly narrow the search space. When the duplicate uses the same
tool and data-format vocabulary, BM25 can find it.

The weaknesses come from long translated documents and varied workflow
phrasing. Many GIS questions mention the same tool but ask about different
operations. Other duplicates describe the same operation with different
software steps, coordinate terminology, or data formats. BM25 therefore tends
to retrieve same-tool or same-format neighbors, but it does not consistently
identify the exact duplicate intent.

### Dense Evaluation Profile

Dense retrieval with `harrier_oss_v1_270m` reaches nDCG@10 = 0.3202, hit@10 =
0.4500, and recall@100 = 0.6850. Dense retrieval improves over BM25, suggesting
that embedding similarity captures workflow equivalence better than exact term
frequency alone. It can connect questions about map scaling, projection,
conversion, or scripting even when the query and positive document use
different wording.

The moderate score also shows that dense retrieval is not enough by itself.
GIS support posts contain many same-domain hard negatives: two questions can
mention QGIS print composer, shapefiles, rasters, or ArcMap Python while asking
for different operations. Dense models that overemphasize broad geospatial
topic similarity may rank plausible but non-duplicate workflow questions above
the true positive.

### Reranking Hybrid Evaluation Profile

The `reranking_hybrid` candidate column reaches nDCG@10 = 0.3272, hit@10 =
0.4550, and recall@100 = 0.7200, with 100 to 101 candidates per query and 56
rank-101 safeguard rows. It is the strongest profile among the three candidate
sources, with the best top-10 ranking and the best top-100 coverage. The result
suggests that sparse and dense signals are complementary for GIS duplicate
retrieval.

Hybrid search is useful here because exact software and file-format names
matter, but they are not sufficient. Dense retrieval supplies workflow-level
similarity, while BM25 keeps rare technical identifiers in the candidate pool.
The hybrid column should be read as a high-recall reranking pool whose top
order is already slightly better than either individual signal, but still far
from solved.

### Metric Interpretation for Model Researchers

Since each query has one positive duplicate, nDCG@10 measures how high the true
duplicate is ranked. Hit@10 approximates whether a user sees the duplicate in a
short result list, and recall@100 measures whether a reranker has the positive
available. The ranking pattern is clear: BM25 is useful, dense is better, and
hybrid gives the broadest and best initial candidate set.

This split is a good benchmark for technical hybrid search. A system that
ignores lexical evidence may miss rare GIS identifiers, while a system that
relies only on lexical evidence may confuse same-tool questions. The best
models should combine both while learning duplicate intent.

### Query and Relevance Type Tendencies

Queries are short Dutch-translated GIS support questions. They often mention a
specific tool, data type, operation, or environment, such as QGIS print
composer, SRTM DEM, ArcMap, shapefiles, CSV, or Python. Relevant documents are
prior questions marked as duplicates, usually containing longer workflow
descriptions and sometimes attempted code or commands.

The relevance relation is not simply "same GIS topic." It is "same problem or
workflow question." Two questions about shapefile conversion may not be
duplicates if one asks about attributes and another asks about coordinate
encoding.

### Representative Failure Modes

BM25 can fail when the same workflow is described with different terminology,
or when long documents include many irrelevant tool names. It can also over-
rank documents that share a software name but ask a different workflow
question. Dense retrieval can fail when semantically similar GIS tasks are not
duplicates, such as two QGIS print-layout questions with different constraints.

Hybrid failures are likely to involve same-tool hard negatives. The positive
may be present in the candidate set, but a candidate with stronger exact
software overlap can outrank it. Rerankers need to compare the requested
operation, input data, and desired output, not only the tool name.

### Training Data That May Help

Useful training data includes non-overlapping CQADupStack GIS duplicate pairs,
Dutch-translated geospatial support QA, and technical duplicate-question data
with software and version metadata preserved. Training should exclude the
translated GIS test queries and duplicate positives used by this Nano split.

Synthetic data can be generated from GIS troubleshooting posts outside the
evaluation set. Good synthetic duplicates should vary the wording of the same
workflow while preserving the operation. Hard negatives should use the same
tool or file format but ask about a different task, such as export versus
projection or attribute copying versus geometry conversion.

### Model Improvement Notes

Improving this task requires treating software identifiers as important but not
decisive. Dense models should learn workflow-level equivalence from technical
support pairs, while rerankers should inspect whether query and candidate share
the same operation and failure condition. Long-document handling matters
because the positive signal can be buried inside a translated body.

Hybrid and reranking systems are especially promising here. BM25 protects rare
technical strings, dense retrieval handles paraphrased workflows, and the
reranker can make the final duplicate judgment.

## Example Data

### Public Sources

- [CQADupStack: A Benchmark Data Set for Community Question-Answering Research](https://doi.org/10.1145/2838931.2838934), 2015.
- [Author-hosted CQADupStack PDF](https://eltimster.github.io/www/pubs/adcs2015.pdf), 2015.
- [BEIR-NL: Zero-shot Information Retrieval Benchmark for the Dutch Language](https://aclanthology.org/2025.bucc-1.5/), 2025.
- [BEIR: A Heterogeneous Benchmark for Zero-shot Evaluation of Information Retrieval Models](https://arxiv.org/abs/2104.08663), 2021.
- [clips/beir-nl-cqadupstack](https://huggingface.co/datasets/clips/beir-nl-cqadupstack), source dataset card.

### Source Reference Table

| Title | Year | Type | URL |
| --- | ---: | --- | --- |
| CQADupStack: A Benchmark Data Set for Community Question-Answering Research | 2015 | proceedings paper | https://doi.org/10.1145/2838931.2838934 |
| BEIR-NL: Zero-shot Information Retrieval Benchmark for the Dutch Language | 2025 | proceedings paper | https://aclanthology.org/2025.bucc-1.5/ |
| BEIR: A Heterogeneous Benchmark for Zero-shot Evaluation of Information Retrieval Models | 2021 | arXiv paper | https://arxiv.org/abs/2104.08663 |
| clips/beir-nl-cqadupstack |  | dataset card | https://huggingface.co/datasets/clips/beir-nl-cqadupstack |

### Representative Snippets

| Query | Positive passage |
| --- | --- |
| Hoe verander ik de beeldverhouding van een kaart zonder dat de schaal verandert? | A translated QGIS print-composer question asks how to resize a map item while keeping the map scale locked. |
| Hoe gebruik ik SRTM Global DEM voor hellingberekening? | A translated ArcGIS question describes slope analysis over elevation data where all resulting slope values look wrong. |
| Attributen van een shapefile kopieren naar een nieuw shapefile | A translated Python/GIS question asks how to create records in an output shapefile using attributes from an input shapefile. |
| Het converteren van een CSV naar een shapefile | A translated question asks how to convert CSV rows containing WKT geometry into a shapefile with `ogr2ogr`. |
| Python-scripts die binnen ArcMap draaien versus die erbuiten draaien? | A translated ArcMap Python question discusses `raw_input()` and different behavior inside the ArcMap Python console. |
