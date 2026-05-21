# MNanoBEIR / NanoBEIR-es / NanoClimateFEVER

## Overview

Climate-FEVER is a climate claim verification benchmark. `NanoBEIR-es__NanoClimateFEVER`
is the Spanish MNanoBEIR version: each query is a Spanish translated climate
claim, and the system must retrieve Spanish translated Wikipedia evidence
documents. The task tests claim-evidence retrieval in a climate-science setting.

## Details

### What the Original Data Measures

[CLIMATE-FEVER: A Dataset for Verification of Real-World Climate
Claims](https://arxiv.org/abs/2012.00614) introduces climate claim verification
using real-world climate claims and evidence from Wikipedia. The paper frames
the task as evidence retrieval and verification for claims that can require
scientific context, temporal framing, and careful interpretation.

[BEIR: A Heterogeneous Benchmark for Zero-shot Evaluation of Information
Retrieval Models](https://arxiv.org/abs/2104.08663) includes Climate-FEVER as a
fact-checking retrieval task. [MMTEB: Massive Multilingual Text Embedding
Benchmark](https://arxiv.org/abs/2502.13595) provides the multilingual
benchmark context for this Spanish Nano split.

### Observed Data Profile

The sampled Spanish Nano task has 50 queries, 3,408 documents, and 148 positive
qrel rows. Queries average 2.96 positives, with 44 of 50 queries having multiple
positives. The average query length is 154.62 characters, and the average
document length is 1,772.08 characters.

The inspected claims discuss existential risk, sea-level variability, human CO2
emissions, Holocene warmth, and historical warming/cooling cycles. Positive
documents are Spanish translated Wikipedia-style pages about climate,
geography, people, and climate history.

### BM25 Difficulty

Using the dataset-provided BM25 candidate column, BM25 reaches nDCG@10 =
0.2635 and hit@10 = 0.6600. BM25 ranks a positive first for 14 queries, and
the median first-positive rank is 4.5.

Lexical matching helps when claims repeat distinctive climate terms, but many
claims require broader evidence pages rather than passages that repeat the exact
wording. A strong retriever should connect Spanish claim language to evidence
about climate mechanisms, records, and historical periods.

### Training Data That May Help

Useful training data includes non-overlapping climate fact-checking data,
scientific claim-evidence retrieval pairs, Spanish or multilingual Wikipedia
claim verification data, and hard negatives from related climate pages.

Training should exclude Climate-FEVER, BEIR, NanoBEIR, or translated records
likely to overlap with these evaluation claims or evidence pages.

### Synthetic Data Guidance

For document-to-query generation, start from non-evaluation Spanish climate or
environmental encyclopedia passages and generate claims that need evidence.
Include sea level, CO2, historical temperature, weather variability, and named
scientists or institutions.

For joint generation, create related evidence pages and claims that require
selecting the right page among topically similar climate documents.

## Example Data

| Query | Positive document |
| --- | --- |
| Desde 1970 hasta 1998 hubo un período de calentamiento que elevó las temperaturas aproximadamente 0.4 grados Celsius, lo que dio origen al movimiento alarmista sobre el calentamiento global. (190 chars) | El Paleoceno (pronunciado /ˈpæliəˌsiːn/ o /ˈpæ - , - lioʊ - /) o Paleoceno, el "reciente antiguo", es una época geológica que duró aproximadamente desde hace 66 a 56 millones de años. Es la primera época del Período Paleógeno ... [truncated 225 chars](1219 chars) |
| De hecho, la tendencia, aunque no es estadísticamente significativa, está a la baja. (84 chars) | El ciclo solar, o ciclo de actividad magnética solar, es el cambio casi periódico de 11 años en la actividad del Sol (incluyendo variaciones en los niveles de radiación solar y la expulsión de material solar) y en su aparienc ... [truncated 225 chars](683 chars) |
| Los niveles del mar locales y regionales siguen mostrando su variabilidad natural, subiendo en algunas áreas y bajando en otras. (128 chars) | El nivel medio del mar (NMM) (abreviado simplemente como nivel del mar) es el nivel promedio de la superficie de uno o más de los océanos de la Tierra, a partir del cual se pueden medir alturas como las elevaciones. El NMM es ... [truncated 225 chars](1181 chars) |
| Los expertos en clima afirman que ciertos elementos del caso del huracán Harvey sugieren que el calentamiento global está agravando una situación ya complicada. (160 chars) | Los efectos del calentamiento global son los cambios ambientales y sociales causados (directa o indirectamente) por las emisiones humanas de gases de efecto invernadero. Existe un consenso científico de que el cambio climátic ... [truncated 225 chars](1501 chars) |
| El experimento CLOUD del CERN solo probó una tercera parte de uno de los cuatro requisitos necesarios para culpar al calentamiento global a los rayos cósmicos, y dos de los otros requisitos ya han fallado. (205 chars) | La atribución del cambio climático reciente se refiere al esfuerzo por determinar científicamente los mecanismos responsables de los cambios climáticos recientes en la Tierra, comúnmente conocidos como `calentamiento global`. ... [truncated 225 chars](2352 chars) |

## Dataset Information

| Field | Value |
| --- | --- |
| Nano set | MNanoBEIR |
| Backing dataset | NanoBEIR-es |
| Task / split | NanoClimateFEVER |
| Hugging Face dataset | [hakari-bench/NanoBEIR-es](https://huggingface.co/datasets/hakari-bench/NanoBEIR-es) |
| Language | es |
| Category | natural_language |
| Queries | 50 |
| Documents | 3,408 |
| Positive qrels | 148 |
| Avg positives / query | 2.96 |
| Positives per query (min / median / max) | 1 / 3.00 / 5 |
| Queries with multiple positives | 44 (88.0%) |
| BM25 nDCG@10 | 0.2635 |
| BM25 hit@10 | 0.6600 |
| Query length avg chars | 154.62 |
| Document length avg chars | 1,772.08 |

### Public Sources

- [CLIMATE-FEVER: A Dataset for Verification of Real-World Climate Claims](https://arxiv.org/abs/2012.00614); 2021; Thomas Diggelmann, Jordan Boyd-Graber, Jannis Bulian, Massimiliano Ciaramita, Markus Leippold; DOI: `10.48550/arXiv.2012.00614`.
- [BEIR: A Heterogeneous Benchmark for Zero-shot Evaluation of Information Retrieval Models](https://arxiv.org/abs/2104.08663); 2021; Nandan Thakur, Nils Reimers, Andreas Rueckle, Abhishek Srivastava, Iryna Gurevych; DOI: `10.48550/arXiv.2104.08663`.
- [MMTEB: Massive Multilingual Text Embedding Benchmark](https://arxiv.org/abs/2502.13595); 2025; Kenneth Enevoldsen, Isaac Chung, Imene Kerboua, Marton Kardos, Ashwin Mathur, and others; DOI: `10.48550/arXiv.2502.13595`.
- [Zeta Alpha NanoBEIR collection](https://huggingface.co/collections/zeta-alpha-ai/nanobeir).

### Hugging Face Links

- Nano dataset: [hakari-bench/NanoBEIR-es](https://huggingface.co/datasets/hakari-bench/NanoBEIR-es)
- Source collection: [Zeta Alpha NanoBEIR collection](https://huggingface.co/collections/zeta-alpha-ai/nanobeir)

### Source Reference Table

| Title | Year | Type | URL |
| --- | ---: | --- | --- |
| CLIMATE-FEVER: A Dataset for Verification of Real-World Climate Claims | 2021 | task paper | https://arxiv.org/abs/2012.00614 |
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
  backing_dataset: NanoBEIR-es
  dataset_id: hakari-bench/NanoBEIR-es
  task_name: NanoClimateFEVER
  split_name: NanoClimateFEVER
  language: es
  category: natural_language
  document_path: docs/benchmark_tasks/MNanoBEIR/NanoBEIR-es__NanoClimateFEVER.md
  source_research:
    primary_source_type: task_paper
    paper_pdf_or_html_checked: true
    no_paper_note: null
  counts:
    queries: 50
    documents: 3408
    positive_qrels: 148
  positives_per_query:
    average: 2.96
    min: 1
    median: 3.0
    max: 5
    multi_positive_queries: 44
    multi_positive_query_percent: 88.0
  text_stats_chars:
    query_mean: 154.62
    document_mean: 1772.075411
  bm25:
    ndcg_at_10: 0.2634976639
    hit_at_10: 0.66
    source: dataset_bm25_column
  learning:
    original_train_split: available
    evaluation_split_origin: MNanoBEIR Spanish NanoBEIR task split from hakari-bench/NanoBEIR-es
    train_eval_overlap_audit: not_audited
    leakage_note: prefer excluding Climate-FEVER, BEIR, or NanoBEIR records likely to overlap with these evaluation claims or evidence pages
    useful_training_data:
      - non-overlapping climate fact-checking data
      - scientific claim-evidence retrieval pairs
      - Spanish or multilingual Wikipedia claim verification data
      - hard negatives from related climate pages
    synthetic_data:
      document_generation: Spanish climate and environmental encyclopedia passages outside the evaluation set
      question_generation: Spanish climate claims requiring evidence retrieval
      answerability: positives should provide evidence for the claim, not merely mention a climate topic
    multi_positive_training: recommended
  links:
    nano_dataset: https://huggingface.co/datasets/hakari-bench/NanoBEIR-es
    source_urls:
      - label: CLIMATE-FEVER paper
        url: https://arxiv.org/abs/2012.00614
      - label: BEIR paper
        url: https://arxiv.org/abs/2104.08663
      - label: MMTEB paper
        url: https://arxiv.org/abs/2502.13595
      - label: Zeta Alpha NanoBEIR collection
        url: https://huggingface.co/collections/zeta-alpha-ai/nanobeir
    source_notes:
      - Spanish task is a multilingual NanoBEIR adaptation of the original English BEIR task
  references:
    - title: "CLIMATE-FEVER: A Dataset for Verification of Real-World Climate Claims"
      url: https://arxiv.org/abs/2012.00614
      year: 2021
      doi: 10.48550/arXiv.2012.00614
      is_paper: true
      source_confidence: definitive_paper_link
    - title: "BEIR: A Heterogeneous Benchmark for Zero-shot Evaluation of Information Retrieval Models"
      url: https://arxiv.org/abs/2104.08663
      year: 2021
      doi: 10.48550/arXiv.2104.08663
      is_paper: true
      source_confidence: benchmark_context_paper
    - title: "MMTEB: Massive Multilingual Text Embedding Benchmark"
      url: https://arxiv.org/abs/2502.13595
      year: 2025
      doi: 10.48550/arXiv.2502.13595
      is_paper: true
      source_confidence: benchmark_context_paper
    - title: "NanoBEIR: Smaller BEIR dataset subsets"
      url: https://huggingface.co/collections/zeta-alpha-ai/nanobeir
      year: 2024
      doi: null
      is_paper: false
      source_confidence: dataset_collection
```
