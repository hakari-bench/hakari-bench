# MNanoBEIR / NanoBEIR-de / NanoTouche2020

## Overview

Touché 2020 is an argument retrieval benchmark for controversial questions.
`NanoBEIR-de__NanoTouche2020` is the German MNanoBEIR version: German
translated controversial questions must retrieve German translated argumentative
documents that address the topic. The task tests topical relevance, argument
quality signals, and broad pro/con coverage.

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
Benchmark](https://arxiv.org/abs/2502.13595) provides the multilingual
benchmark context for this German Nano split.

### Observed Data Profile

The sampled German Nano task has 49 queries, 5,745 documents, and 932 positive
qrel rows. Every query is multi-positive, averaging 19.02 positives with a range
from 6 to 32. The average query length is 51.00 characters, and the average
document length is 2,456.64 characters.

The inspected queries ask controversial questions about concealed weapons,
direct-to-consumer prescription drug advertising, the penny, abortion, and
corporal punishment in schools. Positive documents are long debate-style
arguments, often with multiple paragraphs and explicit persuasive framing.

### BM25 Difficulty

Using the dataset-provided BM25 candidate column, BM25 reaches nDCG@10 =
0.4727 and hit@10 = 1.0000. BM25 ranks a positive first for 26 of 49 queries,
and every query has at least one positive in the top 10.

The high hit@10 reflects many positives per query and strong topic terms, but
ranking remains nontrivial. A good retriever should not merely find any page
mentioning abortion, prescription drugs, or the penny; it should prioritize
documents that contain substantive arguments addressing the controversial
question.

### Training Data That May Help

Useful training data includes non-overlapping Touché argument retrieval data,
debate portal argument collections, pro/con retrieval pairs, argument quality
ranking data, and German or multilingual controversial-topic retrieval
supervision.

Training should exclude Touché 2020, BEIR, NanoBEIR, or translated argument
documents likely to overlap with these evaluation topics or documents.

### Synthetic Data Guidance

For document-to-query generation, start from non-evaluation debate documents and
generate concise German controversial questions. The generated question should
match the central issue rather than a minor example in the document.

For joint generation, create multiple pro and con arguments per topic so that
multi-positive training rewards broad coverage of relevant arguments and does
not collapse the task into single-answer retrieval.

## Example Data

| Query | Positive document |
| --- | --- |
| Ist Hausaufgaben sinnvoll? (26 chars) | Zunächst gibt es drei Argumente dafür, warum Hausaufgaben hervorragend sind und in modernen Schulen fortbestehen sollten. 1. Hausaufgaben unterstützen Lernende, die durch Handeln lernen. Es ist allgemein anerkannt, dass es dr ... [truncated 225 chars](4185 chars) |
| Sollten verschreibungspflichtige Medikamente direkt an Verbraucher beworben werden dürfen? (90 chars) | Viele Werbeanzeigen enthalten nicht genügend Informationen darüber, wie gut Medikamente wirken. Zum Beispiel wird Lunesta durch einen Schmetterling beworben, der durch ein Schlafzimmerfenster fliegt, über einer friedlich schl ... [truncated 225 chars](2016 chars) |
| Welche Impfungen sind für Kinder notwendig? (43 chars) | Es handelt sich noch nicht um einen vollständigen Fall... Nur einige wenige Punkte, die ich zusammengestellt habe... Regierungen sollten kein Recht haben, in die gesundheitlichen Entscheidungen einzugreifen, die Eltern für ih ... [truncated 225 chars](4993 chars) |
| Sollte Abtreibung legal sein? (29 chars) | Abtreibungen sollten legal sein, da die Persönlichkeit erst beginnt, wenn ein Fötus lebensfähig ist oder nach der Geburt. Laut dem Obersten Gerichtshof der USA erhält eine Person ihr Alter, wenn sie aus dem Mutterleib kommt u ... [truncated 225 chars](318 chars) |
| Verbessern standardisierte Tests die Qualität der Bildung? (58 chars) | Die SAT, ACT und andere standardisierte Tests bieten mehr Einblicke in die Vorbereitung eines Schülers auf das Studium an Elite-Universitäten als der Notendurchschnitt in der High School. Daher sollten sie eine größere Rolle ... [truncated 225 chars](4955 chars) |

## Dataset Information

| Field | Value |
| --- | --- |
| Nano set | MNanoBEIR |
| Backing dataset | NanoBEIR-de |
| Task / split | NanoTouche2020 |
| Hugging Face dataset | [hakari-bench/NanoBEIR-de](https://huggingface.co/datasets/hakari-bench/NanoBEIR-de) |
| Language | de |
| Category | natural_language |
| Queries | 49 |
| Documents | 5,745 |
| Positive qrels | 932 |
| Avg positives / query | 19.02 |
| Positives per query (min / median / max) | 6 / 19.00 / 32 |
| Queries with multiple positives | 49 (100.0%) |
| BM25 nDCG@10 | 0.4824 |
| BM25 hit@10 | 1.0000 |
| BM25 Recall@100 | 0.7135 |
| BM25 candidate subset | top-500 (`bm25`) |
| Dense nDCG@10 | 0.4155 |
| Dense hit@10 | 0.9184 |
| Dense Recall@100 | 0.7629 |
| Dense candidate subset | top-500 (`harrier_oss_v1_270m`) |
| Reranking hybrid nDCG@10 | 0.5012 |
| Reranking hybrid hit@10 | 1.0000 |
| Reranking hybrid Recall@100 | 0.7843 |
| Reranking hybrid candidate subset | top-100 plus optional rank-101 safeguard (`reranking_hybrid`) |
| Reranking hybrid candidates / query | 100 |
| Reranking hybrid safeguard rows | 0 |
| Query length avg chars | 51.00 |
| Document length avg chars | 2,456.64 |

### Public Sources

- [Overview of Touché 2020: Argument Retrieval](https://doi.org/10.1007/978-3-030-58219-7_26); 2020; Martin Potthast, Lukas Gienapp, Henning Wachsmuth, Matthias Hagen, Maik Fröbe, Alexander Bondarenko, Yamen Ajjour, Benno Stein; DOI: `10.1007/978-3-030-58219-7_26`.
- [Touche20-Argument-Retrieval-for-Controversial-Questions](https://doi.org/10.5281/zenodo.6862281); 2022; Martin Potthast, Lukas Gienapp, Henning Wachsmuth, Matthias Hagen, Maik Fröbe, Alexander Bondarenko, Yamen Ajjour, Benno Stein; DOI: `10.5281/zenodo.6862281`.
- [BEIR: A Heterogeneous Benchmark for Zero-shot Evaluation of Information Retrieval Models](https://arxiv.org/abs/2104.08663); 2021; Nandan Thakur, Nils Reimers, Andreas Rueckle, Abhishek Srivastava, Iryna Gurevych; DOI: `10.48550/arXiv.2104.08663`.
- [MMTEB: Massive Multilingual Text Embedding Benchmark](https://arxiv.org/abs/2502.13595); 2025; Kenneth Enevoldsen, Isaac Chung, Imene Kerboua, Marton Kardos, Ashwin Mathur, and others; DOI: `10.48550/arXiv.2502.13595`.
- [Zeta Alpha NanoBEIR collection](https://huggingface.co/collections/zeta-alpha-ai/nanobeir).

### Hugging Face Links

- Nano dataset: [hakari-bench/NanoBEIR-de](https://huggingface.co/datasets/hakari-bench/NanoBEIR-de)
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
  backing_dataset: NanoBEIR-de
  dataset_id: hakari-bench/NanoBEIR-de
  task_name: NanoTouche2020
  split_name: NanoTouche2020
  language: de
  category: natural_language
  document_path: docs/benchmark_tasks/MNanoBEIR/NanoBEIR-de__NanoTouche2020.md
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
    query_mean: 51.0
    document_mean: 2456.639687
  bm25:
    ndcg_at_10: 0.48236956272891435
    hit_at_10: 1.0
    source: dataset_candidate_subset
  learning:
    original_train_split: available
    evaluation_split_origin: MNanoBEIR German NanoBEIR task split from hakari-bench/NanoBEIR-de
    train_eval_overlap_audit: not_audited
    leakage_note: prefer excluding Touché 2020, BEIR, or NanoBEIR records likely to
      overlap with these evaluation topics or argument documents
    useful_training_data:
    - non-overlapping Touché argument retrieval data
    - debate portal argument collections
    - pro and con controversial-topic retrieval pairs
    - German or multilingual argument quality ranking data
    synthetic_data:
      document_generation: German debate-style arguments for controversial social
        and policy questions
      question_generation: concise German controversial questions matching the central
        issue of the argument
      answerability: positives should contain substantive arguments addressing the
        question, not only mention the topic
    multi_positive_training: required
  links:
    nano_dataset: https://huggingface.co/datasets/hakari-bench/NanoBEIR-de
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
    - German task is a multilingual NanoBEIR adaptation of the original English BEIR
      task
  references:
  - title: 'Overview of Touché 2020: Argument Retrieval'
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
  - title: 'BEIR: A Heterogeneous Benchmark for Zero-shot Evaluation of Information
      Retrieval Models'
    url: https://arxiv.org/abs/2104.08663
    year: 2021
    doi: 10.48550/arXiv.2104.08663
    is_paper: true
    source_confidence: benchmark_context_paper
  - title: 'MMTEB: Massive Multilingual Text Embedding Benchmark'
    url: https://arxiv.org/abs/2502.13595
    year: 2025
    doi: 10.48550/arXiv.2502.13595
    is_paper: true
    source_confidence: benchmark_context_paper
  - title: 'NanoBEIR: Smaller BEIR dataset subsets'
    url: https://huggingface.co/collections/zeta-alpha-ai/nanobeir
    year: 2024
    doi: null
    is_paper: false
    source_confidence: dataset_collection
  candidate_subsets:
    bm25:
      config: bm25
      label: BM25
      source: dataset_candidate_subset
      top_k: 500
      ndcg_at_10: 0.4823695627
      hit_at_10: 1.0
      recall_at_100: 0.7135193133
      candidate_count_min: 500
      candidate_count_max: 500
      candidate_count_mean: 500.0
      query_count: 49
      query_coverage: 1.0
      relevant_coverage_at_100: 0.7135193133
    dense:
      config: harrier_oss_v1_270m
      label: Dense
      source: dataset_candidate_subset
      top_k: 500
      ndcg_at_10: 0.4155083887
      hit_at_10: 0.9183673469
      recall_at_100: 0.7628755365
      candidate_count_min: 500
      candidate_count_max: 500
      candidate_count_mean: 500.0
      query_count: 49
      query_coverage: 1.0
      relevant_coverage_at_100: 0.7628755365
    reranking_hybrid:
      config: reranking_hybrid
      label: Reranking hybrid
      source: dataset_candidate_subset
      top_k: 100
      ndcg_at_10: 0.5012127127
      hit_at_10: 1.0
      recall_at_100: 0.7843347639
      candidate_count_min: 100
      candidate_count_max: 100
      candidate_count_mean: 100.0
      query_count: 49
      query_coverage: 1.0
      relevant_coverage_at_100: 0.7843347639
      safeguard_positive_rows: 0
      rows_with_101_candidates: 0
```
