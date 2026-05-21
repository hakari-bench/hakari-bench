# MNanoBEIR / NanoBEIR-es / NanoTouche2020

## Overview

Touché 2020 is an argument retrieval benchmark for controversial questions.
`NanoBEIR-es__NanoTouche2020` is the Spanish MNanoBEIR version: Spanish
translated controversial questions must retrieve Spanish translated
argumentative documents that address the topic. The task tests topical
relevance, argument quality, and broad pro/con coverage.

## Details

### What the Original Data Measures

[Overview of Touché 2020: Argument Retrieval](https://doi.org/10.1007/978-3-030-58219-7_26)
describes the CLEF 2020 Touché lab as a shared task on retrieving arguments for
socially important topics and everyday decision questions. The paper emphasizes
that argument retrieval differs from ordinary ad hoc search because relevance
depends not only on topic match but also on argumentative content and quality.

[BEIR: A Heterogeneous Benchmark for Zero-shot Evaluation of Information
Retrieval Models](https://arxiv.org/abs/2104.08663) includes Touché 2020 as an
argument retrieval task. [MMTEB: Massive Multilingual Text Embedding
Benchmark](https://arxiv.org/abs/2502.13595) provides the multilingual context
for this Spanish Nano split.

### Observed Data Profile

The sampled Spanish Nano task has 49 queries, 5,745 documents, and 932 positive
qrel rows. Every query is multi-positive, averaging 19.02 positives with a range
from 6 to 32. The average query length is 53.94 characters, and the average
document length is 2,360.76 characters.

The inspected queries ask about concealed weapons, direct-to-consumer
prescription drug advertising, the penny, abortion, and corporal punishment in
schools. Positive documents are long debate-style arguments in Spanish
translation.

### BM25 Difficulty

Using the dataset-provided BM25 candidate column, BM25 reaches nDCG@10 =
0.5130 and hit@10 = 0.9796. BM25 ranks a positive first for 29 queries, and
almost every query has a positive in the top 10.

The high hit rate reflects strong topic terms and many positives per query, but
ranking remains meaningful. A good retriever should prioritize substantive
arguments that address the question, not just any document mentioning abortion,
weapons, drug advertising, or school punishment.

### Training Data That May Help

Useful training data includes non-overlapping Touché argument retrieval data,
debate portal argument collections, pro/con retrieval pairs, argument quality
ranking data, and Spanish or multilingual controversial-topic retrieval
supervision.

Training should exclude Touché 2020, BEIR, NanoBEIR, or translated argument
documents likely to overlap with these evaluation topics or documents.

### Synthetic Data Guidance

For document-to-query generation, start from non-evaluation debate documents
and generate concise Spanish controversial questions. The generated question
should match the central issue rather than a minor example in the document.

For joint generation, create multiple pro and con arguments per topic so that
multi-positive training rewards broad coverage of relevant arguments.

## Example Data

| Query | Positive document |
| --- | --- |
| ¿Son útiles las tareas? (23 chars) | Primero, hay tres argumentos sobre por qué los deberes son excelentes y deberían continuar en las escuelas modernas. 1. Los deberes ayudan a los aprendices prácticos. Generalmente se acepta que hay tres tipos de aprendices: l ... [truncated 225 chars](4011 chars) |
| ¿Deberían anunciarse los medicamentos con receta directamente a los consumidores? (81 chars) | Muchos anuncios no incluyen suficiente información sobre la eficacia de los medicamentos. Por ejemplo, Lunesta se promociona con una polilla que entra volando por una ventana de un dormitorio, sobre una persona que duerme plá ... [truncated 225 chars](2009 chars) |
| ¿Es necesario vacunar a los niños? (34 chars) | Aún no es un caso completo... Solo algunos puntos que he reunido... Los gobiernos no deberían tener el derecho de intervenir en las decisiones de salud que los padres toman para sus hijos. Según una encuesta de 2010 realizada ... [truncated 225 chars](5062 chars) |
| ¿Debería ser legal el aborto? (29 chars) | Los abortos deberían ser legales, ya que la personalidad jurídica comienza cuando el feto es viable o después del nacimiento, no en el momento de la concepción. Según la Corte Suprema de Estados Unidos, una persona comienza a ... [truncated 225 chars](347 chars) |
| ¿Mejoran las pruebas estandarizadas la educación? (49 chars) | Resuelto: El SAT, el ACT y otras pruebas estandarizadas proporcionan más información sobre la preparación de un estudiante de secundaria para la educación en universidades y colegios de élite que el promedio de calificaciones ... [truncated 225 chars](4878 chars) |

## Dataset Information

| Field | Value |
| --- | --- |
| Nano set | MNanoBEIR |
| Backing dataset | NanoBEIR-es |
| Task / split | NanoTouche2020 |
| Hugging Face dataset | [hakari-bench/NanoBEIR-es](https://huggingface.co/datasets/hakari-bench/NanoBEIR-es) |
| Language | es |
| Category | natural_language |
| Queries | 49 |
| Documents | 5,745 |
| Positive qrels | 932 |
| Avg positives / query | 19.02 |
| Positives per query (min / median / max) | 6 / 19.00 / 32 |
| Queries with multiple positives | 49 (100.0%) |
| BM25 nDCG@10 | 0.5130 |
| BM25 hit@10 | 0.9796 |
| Query length avg chars | 53.94 |
| Document length avg chars | 2,360.76 |

### Public Sources

- [Overview of Touché 2020: Argument Retrieval](https://doi.org/10.1007/978-3-030-58219-7_26); 2020; Martin Potthast, Lukas Gienapp, Henning Wachsmuth, Matthias Hagen, Maik Fröbe, Alexander Bondarenko, Yamen Ajjour, Benno Stein; DOI: `10.1007/978-3-030-58219-7_26`.
- [Touche20-Argument-Retrieval-for-Controversial-Questions](https://doi.org/10.5281/zenodo.6862281); 2022; Martin Potthast, Lukas Gienapp, Henning Wachsmuth, Matthias Hagen, Maik Fröbe, Alexander Bondarenko, Yamen Ajjour, Benno Stein; DOI: `10.5281/zenodo.6862281`.
- [BEIR: A Heterogeneous Benchmark for Zero-shot Evaluation of Information Retrieval Models](https://arxiv.org/abs/2104.08663); 2021; Nandan Thakur, Nils Reimers, Andreas Rueckle, Abhishek Srivastava, Iryna Gurevych; DOI: `10.48550/arXiv.2104.08663`.
- [MMTEB: Massive Multilingual Text Embedding Benchmark](https://arxiv.org/abs/2502.13595); 2025; Kenneth Enevoldsen, Isaac Chung, Imene Kerboua, Marton Kardos, Ashwin Mathur, and others; DOI: `10.48550/arXiv.2502.13595`.
- [Zeta Alpha NanoBEIR collection](https://huggingface.co/collections/zeta-alpha-ai/nanobeir).

### Hugging Face Links

- Nano dataset: [hakari-bench/NanoBEIR-es](https://huggingface.co/datasets/hakari-bench/NanoBEIR-es)
- Source collection: [Zeta Alpha NanoBEIR collection](https://huggingface.co/collections/zeta-alpha-ai/nanobeir)

### Source Reference Table

| Title | Year | Type | URL |
| --- | ---: | --- | --- |
| Overview of Touché 2020: Argument Retrieval | 2020 | benchmark paper | https://doi.org/10.1007/978-3-030-58219-7_26 |
| Touche20-Argument-Retrieval-for-Controversial-Questions | 2022 | dataset page | https://doi.org/10.5281/zenodo.6862281 |
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
  task_name: NanoTouche2020
  split_name: NanoTouche2020
  language: es
  category: natural_language
  document_path: docs/benchmark_tasks/MNanoBEIR/NanoBEIR-es__NanoTouche2020.md
  source_research:
    primary_source_type: benchmark_paper
    paper_pdf_or_html_checked: true
    no_paper_note: null
  counts:
    queries: 49
    documents: 5745
    positive_qrels: 932
  positives_per_query:
    average: 19.020408
    min: 6
    median: 19.0
    max: 32
    multi_positive_queries: 49
    multi_positive_query_percent: 100.0
  text_stats_chars:
    query_mean: 53.938776
    document_mean: 2360.756136
  bm25:
    ndcg_at_10: 0.5130237931
    hit_at_10: 0.9795918367
    source: dataset_bm25_column
  learning:
    original_train_split: available
    evaluation_split_origin: MNanoBEIR Spanish NanoBEIR task split from hakari-bench/NanoBEIR-es
    train_eval_overlap_audit: not_audited
    leakage_note: prefer excluding Touché 2020, BEIR, or NanoBEIR records likely to overlap with these evaluation topics or argument documents
    useful_training_data:
      - non-overlapping Touché argument retrieval data
      - debate portal argument collections
      - pro and con controversial-topic retrieval pairs
      - Spanish or multilingual argument quality ranking data
    synthetic_data:
      document_generation: Spanish debate-style arguments for controversial social and policy questions
      question_generation: concise Spanish controversial questions matching the central issue of the argument
      answerability: positives should contain substantive arguments addressing the question, not only mention the topic
    multi_positive_training: required
  links:
    nano_dataset: https://huggingface.co/datasets/hakari-bench/NanoBEIR-es
    source_urls:
      - label: Touché 2020 overview
        url: https://doi.org/10.1007/978-3-030-58219-7_26
      - label: Touché 2020 dataset
        url: https://doi.org/10.5281/zenodo.6862281
      - label: BEIR paper
        url: https://arxiv.org/abs/2104.08663
      - label: MMTEB paper
        url: https://arxiv.org/abs/2502.13595
      - label: Zeta Alpha NanoBEIR collection
        url: https://huggingface.co/collections/zeta-alpha-ai/nanobeir
    source_notes:
      - Spanish task is a multilingual NanoBEIR adaptation of the original English BEIR task
  references:
    - title: "Overview of Touché 2020: Argument Retrieval"
      url: https://doi.org/10.1007/978-3-030-58219-7_26
      year: 2020
      doi: 10.1007/978-3-030-58219-7_26
      is_paper: true
      source_confidence: benchmark_context_paper
    - title: Touche20-Argument-Retrieval-for-Controversial-Questions
      url: https://doi.org/10.5281/zenodo.6862281
      year: 2022
      doi: 10.5281/zenodo.6862281
      is_paper: false
      source_confidence: dataset_page
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
