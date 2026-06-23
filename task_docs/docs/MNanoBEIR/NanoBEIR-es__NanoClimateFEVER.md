# MNanoBEIR / NanoBEIR-es / NanoClimateFEVER

## Overview

This task is the Spanish NanoBEIR version of Climate-FEVER, a climate claim verification retrieval benchmark. The original Climate-FEVER dataset uses real-world climate claims and Wikipedia evidence to test whether systems can retrieve and verify evidence for scientifically and politically sensitive claims. In this NanoBEIR slice, each query is a Spanish translated climate claim and the system must retrieve Spanish translated Wikipedia-style evidence documents. The task contains 50 queries, 3,408 documents, and 148 positive relevance judgments. Most queries have multiple positives, with an average of 2.96 relevant documents per claim. The benchmark is useful for evaluating claim-evidence retrieval under climate-science terminology, temporal framing, and broad evidence pages that may not repeat the claim wording directly.

## Details

### What the Original Data Measures

Climate-FEVER measures evidence retrieval for climate claims. A claim may discuss sea-level change, CO2 emissions, historical temperature periods, climate models, extreme weather, or scientific attribution. The retrieval task is to find documents that provide evidence relevant to the claim before any final verification label is applied. A good retriever must connect Spanish claim text to evidence pages that contain the needed scientific or historical context, not merely pages that mention a climate keyword.

### Observed Data Profile

The Spanish Nano task has 50 queries, 3,408 documents, and 148 positives. Positives per query average 2.96, with 44 of 50 queries having multiple positives. Queries average about 155 characters, while documents are long, averaging about 1,772 characters. The examples include claims about warming from 1970 to 1998, downward trends, local and regional sea-level variability, Hurricane Harvey and global warming, and the CERN CLOUD experiment. Positive documents are translated Wikipedia-style pages about climate systems, geologic periods, sea level, solar cycles, and climate attribution.

### BM25 Evaluation Profile

BM25 reaches nDCG@10 of 0.285, Hit@10 of 0.640, and Recall@100 of 0.601. Sparse retrieval is useful when claims contain distinctive terms such as sea level, CO2, Holocene, solar cycle, or named experiments. However, climate evidence often appears in broad background pages or uses different wording from the claim. BM25 can retrieve documents that share climate vocabulary while missing the specific evidential relation needed for verification.

### Dense Evaluation Profile

The dense harrier-oss-270m baseline reaches nDCG@10 of 0.310, Hit@10 of 0.640, and Recall@100 of 0.581. Dense retrieval slightly improves top-10 ranking but has lower Recall@100 than BM25. This suggests that semantic similarity helps place some evidence pages higher, but exact climate terminology still matters for candidate coverage. Dense models may also retrieve generally climate-related pages that are semantically close but not one of the annotated evidence documents.

### Reranking Hybrid Evaluation Profile

The reranking_hybrid profile is strongest overall, with nDCG@10 of 0.309, Hit@10 of 0.700, and Recall@100 of 0.669, with three safeguard rows at 101 candidates. It combines the broad lexical coverage of BM25 with dense semantic matching and gives the best first-page hit rate and recall. The nDCG is nearly tied with dense retrieval, while recall is clearly higher. For this task, hybrid search is the most useful candidate strategy because climate claims require both exact scientific terms and broader evidence-page matching.

### Metric Interpretation for Model Researchers

Because most queries have multiple positives, Hit@10 only indicates whether at least one evidence page was retrieved. Recall@100 is important for verification pipelines because a claim may require several evidence documents or because different annotated positives may capture different aspects of the claim. nDCG@10 measures whether relevant evidence is visible early. The hybrid profile's higher recall suggests it is better suited as a first-stage retriever, while dense and hybrid top-rank behavior should be inspected by claim type.

### Query and Relevance Type Tendencies

Queries are declarative climate claims, often with temporal, causal, or attribution language. Relevant documents are encyclopedic evidence pages rather than short answer passages. Some positives may be broad pages that provide background context, while others target a specific mechanism or record. The task is sensitive to scientific terminology, Spanish translation choices, numeric or temporal references, and the ability to distinguish evidence from topical mention.

### Representative Failure Modes

BM25 can retrieve climate pages that repeat a term but do not address the claim. Dense retrieval can retrieve generally related climate science pages while missing the specific evidence page. Hybrid retrieval improves coverage but may still rank broad climate pages above narrower evidence. Failure analysis should ask whether the retrieved document would help verify the claim, not only whether it is about climate.

### Training and Leakage Considerations

Training should exclude Climate-FEVER, BEIR, NanoBEIR, and translated records likely to overlap with these evaluation claims or evidence pages. Useful non-overlapping data includes climate fact-checking data, scientific claim-evidence retrieval pairs, Spanish or multilingual Wikipedia verification data, and hard negatives from related climate pages. Multi-positive training is recommended because most claims have several relevant evidence documents.

### Model Improvement Signals

Strong models should improve evidence recall while maintaining claim-specific ranking. Useful training signals include climate-domain entity and term normalization, temporal reasoning examples, evidence-page hard negatives, and multilingual claim verification pairs. Hybrid systems should preserve exact scientific terms while using dense similarity to recover evidence pages written in broader explanatory language.

## Example Data

| Query | Positive document |
| --- | --- |
| Desde 1970 hasta 1998 hubo un período de calentamiento que elevó las temperaturas aproximadamente 0.4 grados Celsius, lo que dio origen al movimiento alarmista sobre el calentamiento global. [190 chars] | El Paleoceno (pronunciado /ˈpæliəˌsiːn/ o /ˈpæ - , - lioʊ - /) o Paleoceno, el "reciente antiguo", es una época geológica que duró aproximadamente desde hace 66 a 56 millones de años. Es la primera época del Período Paleógeno en la Era Cenozoica moderna. Al igual que muchos períodos geológicos, las capas que definen el inicio y el fin de la época están bien identificadas, pero las edades exactas siguen siendo inciertas. La Época del Paleoceno abarca dos eventos importantes en la historia de la Tierra. Comenzó con el evento de extinción masiva al final del Cretácico, conocido como la frontera Cretácico-Paleógeno (K-Pg). Este fue un tiempo marcado por la desaparición de los dinosaurios no aviares, los grandes reptiles marinos y gran parte de la fauna y flora. La extinción de los dinosaurios dejó nichos ecológicos vacíos en todo el mundo. El Paleoceno terminó con el Máximo Térmico del Paleoceno-Eoceno, un intervalo geológicamente breve (aproximadamente 0.2 millones de años) caracterizado... [1,000 / 1,219 chars] |
| De hecho, la tendencia, aunque no es estadísticamente significativa, está a la baja. [84 chars] | El ciclo solar, o ciclo de actividad magnética solar, es el cambio casi periódico de 11 años en la actividad del Sol (incluyendo variaciones en los niveles de radiación solar y la expulsión de material solar) y en su apariencia (cambios en el número y tamaño de las manchas solares, las llamaradas y otras manifestaciones). Estos cambios han sido observados (por variaciones en la apariencia del Sol y por fenómenos observados en la Tierra, como las auroras boreales) durante siglos. Los cambios en el Sol provocan efectos en el espacio, en la atmósfera y en la superficie terrestre. Aunque es la variable dominante en la actividad solar, también ocurren fluctuaciones no periódicas. [683 chars] |
| Los niveles del mar locales y regionales siguen mostrando su variabilidad natural, subiendo en algunas áreas y bajando en otras. [128 chars] | El nivel medio del mar (NMM) (abreviado simplemente como nivel del mar) es el nivel promedio de la superficie de uno o más de los océanos de la Tierra, a partir del cual se pueden medir alturas como las elevaciones. El NMM es un tipo de dato vertical estándar geodésico que se utiliza, por ejemplo, como dato de referencia en cartografía y navegación marítima, o, en aviación, como el nivel del mar estándar en el que se mide la presión atmosférica para calibrar la altitud y, en consecuencia, los niveles de vuelo de las aeronaves. Un estándar común y relativamente sencillo del nivel medio del mar es el punto medio entre la marea baja media y la marea alta media en una ubicación particular. Los niveles del mar pueden verse afectados por muchos factores y se sabe que han variado considerablemente a lo largo de escalas de tiempo geológicas. La medición cuidadosa de las variaciones en el NMM puede ofrecer información sobre el cambio climático en curso, y el aumento del nivel del mar ha sido am... [1,000 / 1,181 chars] |

## Public Sources

- [Climate-FEVER paper](https://arxiv.org/abs/2012.00614)
- [BEIR benchmark](https://github.com/beir-cellar/beir)
- [MMTEB benchmark](https://arxiv.org/abs/2502.13595)
- [NanoBEIR dataset](https://huggingface.co/collections/zeta-alpha-ai/nanobeir)

## Source Reference Table

| Label | URL |
|---|---|
| Climate-FEVER paper (https://arxiv.org/abs/2012.00614) |
| BEIR benchmark (https://github.com/beir-cellar/beir) |
| MMTEB benchmark (https://arxiv.org/abs/2502.13595) |
| NanoBEIR dataset (https://huggingface.co/collections/zeta-alpha-ai/nanobeir) |
