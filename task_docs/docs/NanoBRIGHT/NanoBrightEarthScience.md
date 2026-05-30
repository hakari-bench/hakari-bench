# NanoBRIGHT / NanoBrightEarthScience

## Overview

NanoBrightEarthScience is the compact NanoBRIGHT slice for Earth Science StackExchange retrieval. Queries are technical Earth science questions, and relevant documents are web passages, reports, tutorials, or reference snippets cited by answers or validated as supporting sources. The retrieval goal is to find evidence that helps answer geological, climate, meteorological, planetary, or environmental questions. This makes the task useful for evaluating reasoning-intensive science retrieval and source-backed technical QA.

## Details

### What the Original Data Measures

BRIGHT's StackExchange tasks define relevance through cited web documents that support the reasoning needed to answer a question. In Earth Science, the useful passage may explain a physical process, data source, geologic method, atmospheric mechanism, or environmental measurement rather than directly containing a short answer string.

The task therefore requires more than surface overlap. Queries often include context, assumptions, or practical constraints. Relevant passages can come from encyclopedic sources, technical documentation, scientific reports, or explanatory pages that provide a concept needed for the answer.

### Observed Data Profile

The task contains 116 queries, 10,000 documents, and 579 relevance judgments. It is strongly multi-positive, with an average of 4.99 positives per query. The minimum is 1, the median is 4.0, the maximum is 22, and 96 queries are multi-positive, or 82.76% of the set.

Queries average 476.71 characters, while documents average 716.25 characters. Queries are usually long enough to include a scenario, prior understanding, or data-access need. Documents are passage chunks that may cite scientific concepts, datasets, web documentation, or explanatory background.

### BM25 Evaluation Profile

BM25 reaches nDCG@10 of 0.4611, hit@10 of 0.7672, and recall@100 of 0.6839 using the top-500 BM25 candidate subset. Lexical matching is fairly strong because many questions contain distinctive terms such as ERA5, limestone, ozone, Mars soil, continental drift, or specific meteorological concepts.

The limitation is that useful evidence may use broader scientific terminology than the question. BM25 can retrieve passages sharing topic words while missing the passage that supports the specific physical explanation, data source, or measurement interpretation. It is a solid candidate generator but not the best profile.

### Dense Evaluation Profile

The dense harrier-oss-270m run reaches nDCG@10 of 0.5406, hit@10 of 0.8448, and recall@100 of 0.7288. Dense retrieval improves all reported metrics over BM25. This shows that embedding similarity helps connect contextual Earth science questions to explanatory passages that may not repeat the same exact wording.

Dense retrieval is particularly useful when the question asks about a mechanism, process, or data concept rather than a named object. It can match the intent of a question about continental drift monitoring, ozone chemistry, plant oxygen production, or Martian soil composition to broader supporting evidence.

### Reranking Hybrid Evaluation Profile

The reranking_hybrid candidate set reaches nDCG@10 of 0.5518, hit@10 of 0.9052, and recall@100 of 0.7979. It uses a top-100 candidate range with an optional rank-101 safeguard; this slice has 2 safeguard rows, candidate counts from 100 to 101, and a mean of 100.02 candidates. It is the strongest profile across the reported metrics.

This suggests that Earth Science retrieval benefits from combining exact terminology with semantic explanation matching. BM25 captures named datasets, substances, and scientific terms, while dense retrieval captures the broader process or evidence relation. The hybrid pool is the best observed starting point for downstream reranking or answer generation.

### Metric Interpretation for Model Researchers

Because most queries have several positives, hit@10 only indicates whether at least one supporting source is visible. nDCG@10 measures whether the first page contains useful evidence, and recall@100 measures whether a downstream answerer or reranker can access enough supporting passages.

The comparison shows that BM25 is already meaningful due to distinctive terminology, dense retrieval improves semantic support matching, and reranking_hybrid gives the best combined ranking and coverage. This task is useful for evaluating scientific source retrieval under realistic question context.

### Query and Relevance Type Tendencies

Queries ask about how continental drift was monitored, forecasting statistics for weather phenomena, oxygen production by plants, Martian soil simulants, and ozone layer thickness. Positive documents include passages about geodetic monitoring, optical phenomena, algae or photosynthesis, Mars soil composition, and ozone-oxygen chemistry.

The task rewards matching the specific scientific intent. A passage can be on the same broad topic, such as weather or Mars, yet fail to provide the evidence needed for the question. Data-access and physical-process questions are especially sensitive to this distinction.

### Representative Failure Modes

Likely failures include retrieving same-topic passages that do not answer the mechanism, missing documentation because the query uses lay phrasing, over-ranking pages with named terms but wrong scope, and under-covering multiple cited sources. BM25 may be too literal, while dense retrieval may retrieve plausible but insufficient background.

### Training Data That May Help

Useful training data includes Earth Science StackExchange posts with cited sources, geology and climate QA with references, scientific data product documentation retrieval, environmental science textbook passages, and hard negatives from the same topic that fail the specific explanation.

### Model Improvement Notes

A model targeting this task should combine scientific terminology precision with process-level semantic matching. Sparse systems need robust handling of datasets, units, and named phenomena. Dense systems should train on source-backed scientific QA. Hybrid systems are especially promising because the observed profile is best across nDCG@10, hit@10, and recall@100.

## Example Data

### Public Sources

The original task is based on BRIGHT's reasoning-intensive retrieval benchmark, with NanoBRIGHT providing the compact dataset packaging.

### Source Reference Table

| Item | Reference |
| --- | --- |
| Original benchmark paper | [BRIGHT](https://arxiv.org/abs/2407.12883) |
| Project page | [BRIGHT project page](https://brightbenchmark.github.io/) |
| Source dataset | [xlangai/BRIGHT](https://huggingface.co/datasets/xlangai/BRIGHT) |
| NanoBRIGHT dataset | [hakari-bench/NanoBRIGHT](https://huggingface.co/datasets/hakari-bench/NanoBRIGHT) |

Representative query and positive source snippets:

| Query | Positive document snippet |
| --- | --- |
| How is or was continental drift monitored before satellite technology? | A reference page provides background on geodetic or tectonic measurement context. |
| Is there a source with integrated statistics on forecasting a meteorological occurrence? | A passage explains how light reflects inside raindrops at particular angles. |
| Which plant is most efficient in making oxygen for its weight? | A park page discusses algae and other less visible plants. |
| How can a student grow plants in simulated Martian soil? | A passage lists elemental composition of Mars soil, including SiO2, Fe2O3, Al2O3, MgO, and CaO. |
| How should ozone layer thickness be understood in Dobson units? | A passage explains the ozone-oxygen cycle and regeneration of ozone in the stratosphere. |
