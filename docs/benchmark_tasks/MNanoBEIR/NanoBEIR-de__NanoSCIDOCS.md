# MNanoBEIR / NanoBEIR-de / NanoSCIDOCS

## Overview

SCIDOCS is a scientific document retrieval benchmark derived from scholarly
relatedness signals. `NanoBEIR-de__NanoSCIDOCS` is the German MNanoBEIR version:
German translated scientific paper titles or abstracts are used as queries, and
the system must retrieve German translated related scientific documents. The
task tests document-level scholarly relatedness rather than question answering.

## Details

### What the Original Data Measures

[SPECTER: Document-level Representation Learning using Citation-informed
Transformers](https://arxiv.org/abs/2004.07180) introduces SCIDOCS as an
evaluation benchmark for scientific document embeddings. The paper uses
citations and related scholarly signals to measure whether representations
capture document-level relatedness across tasks such as citation prediction and
recommendation.

[BEIR: A Heterogeneous Benchmark for Zero-shot Evaluation of Information
Retrieval Models](https://arxiv.org/abs/2104.08663) includes SCIDOCS as a
citation-prediction style retrieval task. [MMTEB: Massive Multilingual Text
Embedding Benchmark](https://arxiv.org/abs/2502.13595) provides the multilingual
benchmark context for this German Nano split.

### Observed Data Profile

The sampled German Nano task has 50 queries, 2,210 documents, and 244 positive
qrel rows. Every query is multi-positive, with 3 to 5 positives and an average
of 4.88 positives per query. The average query length is 82.38 characters, and
the average document length is 1,071.09 characters.

The inspected queries are scientific titles about neural machine translation,
automotive information security, Bitcoin transaction privacy, IoT security, and
motion capture for gait analysis. Documents are translated scientific abstracts
or paper descriptions. Some positives are conceptually or citation-related
rather than lexically obvious.

### BM25 Difficulty

Using the dataset-provided BM25 candidate column, BM25 reaches nDCG@10 =
0.1650 and hit@10 = 0.5800. BM25 ranks a positive first for only 8 queries, and
the median first-positive rank is 7.5.

This is hard for lexical retrieval because related scientific papers may use
different terminology, methods, or application framing. The fifth inspected
example pairs a gait-analysis query with a sequence-indexing document, showing
that citation-informed relatedness can be less direct than ordinary topical
matching. Dense models need robust scientific-document representations, not just
title keyword overlap.

### Training Data That May Help

Useful training data includes non-overlapping citation prediction pairs,
scientific paper recommendation data, co-citation or co-viewed paper pairs,
S2ORC-style scientific abstracts, and German or multilingual scholarly retrieval
supervision.

Training should exclude SCIDOCS, SPECTER evaluation data, BEIR, NanoBEIR, or
translated scientific records likely to overlap with these evaluation documents.

### Synthetic Data Guidance

For document-to-query generation, start from non-evaluation scientific abstracts
and generate German paper-title-like queries or short abstract summaries. Include
method names, datasets, tasks, and application domains.

For joint generation, create clusters of related scientific abstracts connected
by shared methods, citations, application settings, or problem formulations so
that multi-positive ranking reflects scholarly relatedness.

## Example Data

| Query | Positive document |
| --- | --- |
| Neuartiger Gleichstrom-Gleichstrom-Mehrstufen-Aufwärtswandler (61 chars) | Mehrstufige Spannungsquellenwandler (Multilevel Voltage Source Converters) etablieren sich als neue Optionen für leistungsstarke Anwendungen. Diese Wandler erzeugen in der Regel eine treppenförmige Spannungswelle aus mehreren ... [truncated 225 chars](1027 chars) |
| Schnelles Lernen von sparsen Gaußschen Markov-Feldern basierend auf Cholesky-Zerlegung (86 chars) | Sure, please provide the English document text that you need translated into German. (84 chars) |
| Textursynthese mit Convolutional Neural Networks (48 chars) | In dieser Arbeit untersuchen wir den Einfluss der Tiefe von Faltungsnetzwerken auf deren Genauigkeit in der groß angelegten Bilderkennung. Unser Hauptbeitrag ist eine gründliche Bewertung von Netzwerken zunehmender Tiefe, die ... [truncated 225 chars](910 chars) |
| Planare Breitband-Ringantenne mit zirkularer Polarisation für ein RFID-System (77 chars) | In dieser Arbeit wird eine Technik mit einem horizontal mäanderförmig verlaufenden Streifen (HMS) vorgeschlagen, um eine gute Impedanzanpassung und symmetrische Strahlungsdiagramme in Breitseite für eine einseitig gespeiste B ... [truncated 225 chars](1467 chars) |
| Entwurf eines fortschrittlichen digitalen Herzfrequenzmonitors mit einfachen elektronischen Bauteilen (101 chars) | In dieser Arbeit stellen wir das Design und die Entwicklung eines neuen integrierten Geräts zur Messung der Herzfrequenz mittels Fingerspitze vor, um die Schätzung der Herzfrequenz zu verbessern. Da herzbedingte Erkrankungen ... [truncated 225 chars](1254 chars) |

## Dataset Information

| Field | Value |
| --- | --- |
| Nano set | MNanoBEIR |
| Backing dataset | NanoBEIR-de |
| Task / split | NanoSCIDOCS |
| Hugging Face dataset | [hakari-bench/NanoBEIR-de](https://huggingface.co/datasets/hakari-bench/NanoBEIR-de) |
| Language | de |
| Category | natural_language |
| Queries | 50 |
| Documents | 2,210 |
| Positive qrels | 244 |
| Avg positives / query | 4.88 |
| Positives per query (min / median / max) | 3 / 5.00 / 5 |
| Queries with multiple positives | 50 (100.0%) |
| BM25 nDCG@10 | 0.1650 |
| BM25 hit@10 | 0.5800 |
| Query length avg chars | 82.38 |
| Document length avg chars | 1,071.09 |

### Public Sources

- [SPECTER: Document-level Representation Learning using Citation-informed Transformers](https://arxiv.org/abs/2004.07180); 2020; Arman Cohan, Sergey Feldman, Iz Beltagy, Doug Downey, Daniel S. Weld; DOI: `10.18653/v1/2020.acl-main.207`.
- [SCIDOCS repository](https://github.com/allenai/scidocs).
- [BEIR: A Heterogeneous Benchmark for Zero-shot Evaluation of Information Retrieval Models](https://arxiv.org/abs/2104.08663); 2021; Nandan Thakur, Nils Reimers, Andreas Rueckle, Abhishek Srivastava, Iryna Gurevych; DOI: `10.48550/arXiv.2104.08663`.
- [MMTEB: Massive Multilingual Text Embedding Benchmark](https://arxiv.org/abs/2502.13595); 2025; Kenneth Enevoldsen, Isaac Chung, Imene Kerboua, Marton Kardos, Ashwin Mathur, and others; DOI: `10.48550/arXiv.2502.13595`.
- [Zeta Alpha NanoBEIR collection](https://huggingface.co/collections/zeta-alpha-ai/nanobeir).

### Hugging Face Links

- Nano dataset: [hakari-bench/NanoBEIR-de](https://huggingface.co/datasets/hakari-bench/NanoBEIR-de)
- Source collection: [Zeta Alpha NanoBEIR collection](https://huggingface.co/collections/zeta-alpha-ai/nanobeir)

### Source Reference Table

| Title | Year | Type | URL |
| --- | ---: | --- | --- |
| SPECTER: Document-level Representation Learning using Citation-informed Transformers | 2020 | task paper | https://arxiv.org/abs/2004.07180 |
| SCIDOCS repository |  | project page | https://github.com/allenai/scidocs |
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
  task_name: NanoSCIDOCS
  split_name: NanoSCIDOCS
  language: de
  category: natural_language
  document_path: docs/benchmark_tasks/MNanoBEIR/NanoBEIR-de__NanoSCIDOCS.md
  source_research:
    primary_source_type: task_paper
    paper_pdf_or_html_checked: true
    no_paper_note: null
  counts:
    queries: 50
    documents: 2210
    positive_qrels: 244
  positives_per_query:
    average: 4.88
    min: 3
    median: 5.0
    max: 5
    multi_positive_queries: 50
    multi_positive_query_percent: 100.0
  text_stats_chars:
    query_mean: 82.38
    document_mean: 1071.089593
  bm25:
    ndcg_at_10: 0.1650032568
    hit_at_10: 0.58
    source: dataset_bm25_column
  learning:
    original_train_split: available
    evaluation_split_origin: MNanoBEIR German NanoBEIR task split from hakari-bench/NanoBEIR-de
    train_eval_overlap_audit: not_audited
    leakage_note: prefer excluding SCIDOCS, SPECTER evaluation data, BEIR, or NanoBEIR records likely to overlap with these scientific documents
    useful_training_data:
      - non-overlapping citation prediction pairs
      - scientific paper recommendation data
      - co-citation or co-viewed paper pairs
      - German or multilingual scholarly retrieval supervision
    synthetic_data:
      document_generation: German scientific abstracts and paper summaries outside the evaluation set
      question_generation: German paper-title-like queries and short abstract summaries
      answerability: positives should be scholarly related documents, not only documents with title keyword overlap
    multi_positive_training: required
  links:
    nano_dataset: https://huggingface.co/datasets/hakari-bench/NanoBEIR-de
    source_urls:
      - label: SPECTER paper
        url: https://arxiv.org/abs/2004.07180
      - label: SCIDOCS repository
        url: https://github.com/allenai/scidocs
      - label: BEIR paper
        url: https://arxiv.org/abs/2104.08663
      - label: MMTEB paper
        url: https://arxiv.org/abs/2502.13595
      - label: Zeta Alpha NanoBEIR collection
        url: https://huggingface.co/collections/zeta-alpha-ai/nanobeir
    source_notes:
      - German task is a multilingual NanoBEIR adaptation of the original English BEIR task
  references:
    - title: "SPECTER: Document-level Representation Learning using Citation-informed Transformers"
      url: https://arxiv.org/abs/2004.07180
      year: 2020
      doi: 10.18653/v1/2020.acl-main.207
      is_paper: true
      source_confidence: definitive_paper_link
    - title: SCIDOCS repository
      url: https://github.com/allenai/scidocs
      year: null
      doi: null
      is_paper: false
      source_confidence: definitive_project_page
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
