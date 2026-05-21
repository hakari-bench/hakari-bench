# NanoMTEB-Dutch / cqadupstack_physics

## Overview

`cqadupstack_physics` is the Dutch-translated Physics subforum split of
CQADupStack. Queries are physics questions and positive documents are earlier
duplicate questions from the same Stack Exchange domain. The task covers
mechanics, acoustics, thermodynamics, quantum mechanics, constants, and related
scientific notation.

## Details

### What the Original Data Measures

[CQADupStack](https://doi.org/10.1145/2838931.2838934) evaluates duplicate
question retrieval in community QA archives using manually flagged duplicate
links from StackExchange. The paper reports that exact-topic subforums such as
physics and statistics tend to have more focused questions, but retrieval still
requires more than surface overlap because duplicates can be phrased in different
ways.

This Dutch version comes through [BEIR-NL](https://aclanthology.org/2025.bucc-1.5/),
which automatically translates BEIR datasets to Dutch. Mathematical notation and
symbols often remain unchanged while explanatory prose becomes Dutch.

### Observed Data Profile

The Nano split has 200 queries, 10,000 documents, and 200 positive qrel rows.
Each query has one positive. Queries average 62.09 characters and documents
average 870.44 characters. Examples include angular momentum, active noise
cancellation, thermodynamic state functions, the Schrodinger equation, and
whether physical constants are constant.

The observed documents often include formulas, variables, images, and careful
setup. Duplicate matching requires recognizing that two differently worded
physics questions ask about the same concept or derivation.

### BM25 Difficulty

Using the dataset-provided BM25 candidate column, BM25 reaches nDCG@10 = 0.3269
and hit@10 = 0.4250. Symbols and specialized terms give BM25 useful anchors,
but paraphrased concepts such as angular momentum versus moment of inertia can
still be missed.

### Training Data That May Help

Useful training data includes non-overlapping Physics Stack Exchange duplicate
pairs, Dutch-translated scientific QA, formula-aware retrieval examples, and
multilingual STEM duplicate-question data. Exclude the translated test queries
and positives in this Nano split.

### Synthetic Data Guidance

Generate Dutch physics questions from non-evaluation explanatory posts. Preserve
math notation, but vary the natural-language framing. Use hard negatives that
share variables or equations but ask about a different physical concept.

## Example Data

| Query | Positive document |
| --- | --- |
| Hoe is de Schrödingervergelijking een golffvergelijking? (56 chars) | Relatie tussen de Schrödingervergelijking en de golfvergelijking Ik ben altijd in de war geweest over de relatie tussen de Schrödingervergelijking en de golfvergelijking. $$ i\hbar \frac{\partial \psi}{\partial t} = - \frac{\ ... [truncated 225 chars](1081 chars) |
| Metingen van actieve ruisonderdrukkingstechnologie (50 chars) | Maximale vertraging voor effectieve actieve ruisonderdrukking? Actieve ruisonderdrukking vermindert ongewenste geluiden door de omgekeerde fase van de originele fase te verzenden: ![Actieve ruisonderdrukking](http://i.stack.i ... [truncated 225 chars](985 chars) |
| Zijn continue wiskundige modellen van discrete fysische verschijnselen rommelig vanwege een discrepantie tussen "continu" en "discontinu"? (138 chars) | Wat is het "discrete" analogon van de "continuüm" mechanica? Als ik een discrete wiskundige benadering van de continuümmechanica wil verkennen, welke leerboeken moet ik dan raadplegen? Een kant-en-klaar antwoord op de vraag z ... [truncated 225 chars](549 chars) |
| Gravitatie van energie (22 chars) | Kan een zwart gat ontstaan door Lorentz-contractie? **Mogelijke dubbel:</** > Als een massa van 1 kg bijna met de lichtsnelheid wordt versneld, zou deze dan veranderen > in een zwart gat? Stel je voor, een staaf met lengte ** ... [truncated 225 chars](1111 chars) |
| Waarom neemt de (relativistische) massa van een object toe naarmate zijn snelheid de lichtsnelheid benadert? (108 chars) | Verwarring over de (relativistische) massa van objecten Volgens Einsteins theorie hangt de (relativistische) massa van objecten af van de snelheid. Dan zullen in een inertiaal referentiesysteem 2 waarnemers die met 2 verschil ... [truncated 225 chars](371 chars) |

## Dataset Information

| Field | Value |
| --- | --- |
| Nano set | NanoMTEB-Dutch |
| Backing dataset | NanoMTEB-Dutch |
| Task / split | cqadupstack_physics |
| Hugging Face dataset | [hakari-bench/NanoMTEB-Dutch](https://huggingface.co/datasets/hakari-bench/NanoMTEB-Dutch) |
| Source dataset | [clips/beir-nl-cqadupstack](https://huggingface.co/datasets/clips/beir-nl-cqadupstack) |
| Language | nl |
| Category | natural_language |
| Queries | 200 |
| Documents | 10,000 |
| Positive qrels | 200 |
| BM25 nDCG@10 | 0.3269 |
| BM25 hit@10 | 0.4250 |
| Query length avg chars | 62.09 |
| Document length avg chars | 870.44 |

### Public Sources

- [CQADupStack: A Benchmark Data Set for Community Question-Answering Research](https://doi.org/10.1145/2838931.2838934), 2015.
- [Author-hosted CQADupStack PDF](https://eltimster.github.io/www/pubs/adcs2015.pdf), 2015.
- [BEIR-NL: Zero-shot Information Retrieval Benchmark for the Dutch Language](https://aclanthology.org/2025.bucc-1.5/), 2025.
- [BEIR: A Heterogeneous Benchmark for Zero-shot Evaluation of Information Retrieval Models](https://arxiv.org/abs/2104.08663), 2021.
- [clips/beir-nl-cqadupstack](https://huggingface.co/datasets/clips/beir-nl-cqadupstack), source dataset card.

### Hugging Face Links

- Nano dataset: [hakari-bench/NanoMTEB-Dutch](https://huggingface.co/datasets/hakari-bench/NanoMTEB-Dutch)
- Source dataset: [clips/beir-nl-cqadupstack](https://huggingface.co/datasets/clips/beir-nl-cqadupstack)

### Source Reference Table

| Title | Year | Type | URL |
| --- | ---: | --- | --- |
| CQADupStack: A Benchmark Data Set for Community Question-Answering Research | 2015 | proceedings paper | https://doi.org/10.1145/2838931.2838934 |
| BEIR-NL: Zero-shot Information Retrieval Benchmark for the Dutch Language | 2025 | proceedings paper | https://aclanthology.org/2025.bucc-1.5/ |
| BEIR: A Heterogeneous Benchmark for Zero-shot Evaluation of Information Retrieval Models | 2021 | arXiv paper | https://arxiv.org/abs/2104.08663 |
| clips/beir-nl-cqadupstack |  | dataset card | https://huggingface.co/datasets/clips/beir-nl-cqadupstack |

## Machine-Readable Metadata

<!-- benchmark-task-metadata:v1 -->

```yaml
benchmark_task_metadata:
  schema_version: 1
  document_status: first_pass
  nano_set: NanoMTEB-Dutch
  backing_dataset: NanoMTEB-Dutch
  dataset_id: hakari-bench/NanoMTEB-Dutch
  task_name: cqadupstack_physics
  split_name: cqadupstack_physics
  language: nl
  category: natural_language
  document_path: docs/benchmark_tasks/NanoMTEB-Dutch/cqadupstack_physics.md
  source_research:
    primary_source_type: task_paper
    paper_pdf_or_html_checked: true
    paper_url: https://doi.org/10.1145/2838931.2838934
    additional_source_urls:
      - https://eltimster.github.io/www/pubs/adcs2015.pdf
      - https://aclanthology.org/2025.bucc-1.5/
      - https://arxiv.org/abs/2104.08663
      - https://huggingface.co/datasets/clips/beir-nl-cqadupstack
  counts:
    queries: 200
    documents: 10000
    positive_qrels: 200
  positives_per_query:
    average: 1.0
    min: 1
    median: 1.0
    max: 1
    multi_positive_queries: 0
    multi_positive_query_percent: 0.0
  text_stats_chars:
    query_mean: 62.095
    document_mean: 870.4386
  bm25:
    ndcg_at_10: 0.32693259
    hit_at_10: 0.425
    source: dataset_bm25_column
  learning:
    original_train_split: available
    evaluation_split_origin: "CQADupstackPhysics-NL test split from clips/beir-nl-cqadupstack"
    train_eval_overlap_audit: not_audited
    leakage_note: "Exclude translated CQADupStack Physics test queries and duplicate positives used by this Nano split."
    useful_training_data:
      - non-overlapping CQADupStack Physics duplicate-question pairs
      - Dutch-translated scientific QA pairs
      - formula-aware STEM duplicate retrieval data
    synthetic_data:
      document_generation: "Dutch physics forum questions with equations and variables preserved."
      question_generation: "Paraphrased duplicate physics questions targeting the same concept."
      answerability: "Each query should duplicate one prior physics question, with equation-near hard negatives."
    multi_positive_training: single_positive
  example_count: 5
```
