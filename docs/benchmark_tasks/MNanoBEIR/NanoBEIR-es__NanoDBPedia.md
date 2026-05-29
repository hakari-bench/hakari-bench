# MNanoBEIR / NanoBEIR-es / NanoDBPedia

## Overview

DBpedia-Entity is an entity search benchmark. `NanoBEIR-es__NanoDBPedia` is the
Spanish MNanoBEIR version: Spanish translated entity-oriented queries must
retrieve Spanish translated DBpedia entity descriptions. The task tests entity
disambiguation, short query matching, and many-positive retrieval.

## Details

### What the Original Data Measures

[DBpedia-Entity V2: A Test Collection for Entity Search](https://doi.org/10.1145/3077136.3080751)
introduces a DBpedia-based entity search collection built from heterogeneous
query sources and relevance judgments. The task is not ordinary passage
answering: relevant documents are entity pages whose descriptions match the
entity information need.

[BEIR: A Heterogeneous Benchmark for Zero-shot Evaluation of Information
Retrieval Models](https://arxiv.org/abs/2104.08663) includes DBpedia-Entity as
an entity retrieval task. [MMTEB: Massive Multilingual Text Embedding
Benchmark](https://arxiv.org/abs/2502.13595) provides the multilingual context
for this Spanish Nano split.

### Observed Data Profile

The sampled Spanish Nano task has 50 queries, 6,045 documents, and 1,158
positive qrel rows. Queries average 23.16 positives, and 48 of 50 queries have
multiple positives. The average query length is 37.98 characters, and the
average document length is 367.78 characters.

The inspected queries include Formula 1 races in Europe, Thomas Jefferson,
best guitarist, Jack Kerouac books published by Viking Press, and films shot in
Venice. Documents are compact DBpedia-style entity descriptions.

### BM25 Difficulty

Using the dataset-provided BM25 candidate column, BM25 reaches nDCG@10 =
0.5215 and hit@10 = 0.9200. BM25 ranks a positive first for 33 queries, and the
median first-positive rank is 1.

BM25 is strong because entity names and category words often overlap directly.
The remaining difficulty is ranking the right entity among many plausible
entities, especially when a short Spanish query names a broad class or ambiguous
person.

### Training Data That May Help

Useful training data includes non-overlapping entity search datasets,
knowledge-base page retrieval pairs, Spanish or multilingual entity linking and
description retrieval data, and hard negatives from same-type entities.

Training should exclude DBpedia-Entity, BEIR, NanoBEIR, or translated DBpedia
records likely to overlap with these evaluation queries or entity pages.

### Synthetic Data Guidance

For document-to-query generation, start from Spanish entity descriptions and
generate short entity-search queries, categories, aliases, or property-based
questions. Include ambiguous names and list-style category needs.

For joint generation, create clusters of same-type entities so that hard
negatives require disambiguating attributes such as creator, location, role, or
publication history.

## Example Data

| Query | Positive document |
| --- | --- |
| Concesionario Fitzgerald en Chambersburg, PA (44 chars) | Fitzgerald Auto Malls es una concesionaria de automóviles propiedad y operada por una familia, fundada en 1966. Su primera ubicación se abrió en Bethesda, Maryland. A partir de 2014, Fitzgerald Auto Malls ocupó el puesto núme ... [truncated 225 chars](509 chars) |
| Colección de cuentos de 1994 de Alice Munro está disponible (59 chars) | Alice Ann Munro (/ˈælɨs ˌæn mʌnˈroʊ/, de soltera Laidlaw /ˈleɪdlɔː/; nacida el 10 de julio de 1931) es una autora canadiense. La obra de Munro ha sido descrita como haber revolucionado la estructura de los cuentos, especialme ... [truncated 225 chars](537 chars) |
| Arquitectura romana gala en París (33 chars) | El arte en París es un artículo sobre la cultura y la historia del arte en París, la capital de Francia. Desde hace siglos, París ha atraído a artistas de todo el mundo, quienes llegan a la ciudad en busca de formación y de i ... [truncated 225 chars](343 chars) |
| Repúblicas de la antigua Yugoslavia (35 chars) | La Constitución de 1974 de Yugoslavia fue la cuarta y última constitución de la República Federal Socialista de Yugoslavia. Entró en vigor el 21 de febrero. Con 406 artículos originales, la constitución de 1974 fue una de las ... [truncated 225 chars](450 chars) |
| Películas filmadas en Venecia (29 chars) | A Little Romance es una comedia romántica estadounidense de 1979 en Technicolor y Panavision, dirigida por George Roy Hill y protagonizada por Laurence Olivier, Thelonious Bernard y Diane Lane en su debut cinematográfico. El ... [truncated 225 chars](408 chars) |

## Dataset Information

| Field | Value |
| --- | --- |
| Nano set | MNanoBEIR |
| Backing dataset | NanoBEIR-es |
| Task / split | NanoDBPedia |
| Hugging Face dataset | [hakari-bench/NanoBEIR-es](https://huggingface.co/datasets/hakari-bench/NanoBEIR-es) |
| Language | es |
| Category | natural_language |
| Queries | 50 |
| Documents | 6,045 |
| Positive qrels | 1,158 |
| Avg positives / query | 23.16 |
| Positives per query (min / median / max) | 1 / 18.00 / 81 |
| Queries with multiple positives | 48 (96.0%) |
| BM25 nDCG@10 | 0.6140 |
| BM25 hit@10 | 0.9600 |
| BM25 Recall@100 | 0.6770 |
| BM25 candidate subset | top-500 (`bm25`) |
| Dense nDCG@10 | 0.6099 |
| Dense hit@10 | 0.9400 |
| Dense Recall@100 | 0.7055 |
| Dense candidate subset | top-500 (`harrier_oss_v1_270m`) |
| Reranking hybrid nDCG@10 | 0.6210 |
| Reranking hybrid hit@10 | 0.9400 |
| Reranking hybrid Recall@100 | 0.7263 |
| Reranking hybrid candidate subset | top-100 plus optional rank-101 safeguard (`reranking_hybrid`) |
| Reranking hybrid candidates / query | 100 |
| Reranking hybrid safeguard rows | 0 |
| Query length avg chars | 37.98 |
| Document length avg chars | 367.78 |

### Public Sources

- [DBpedia-Entity V2: A Test Collection for Entity Search](https://doi.org/10.1145/3077136.3080751); 2017; Faegheh Hasibi, Fedor Nikolaev, Chenyan Xiong, Krisztian Balog, Svein Erik Bratsberg, Alexander Kotov, Jamie Callan; DOI: `10.1145/3077136.3080751`.
- [BEIR: A Heterogeneous Benchmark for Zero-shot Evaluation of Information Retrieval Models](https://arxiv.org/abs/2104.08663); 2021; Nandan Thakur, Nils Reimers, Andreas Rueckle, Abhishek Srivastava, Iryna Gurevych; DOI: `10.48550/arXiv.2104.08663`.
- [MMTEB: Massive Multilingual Text Embedding Benchmark](https://arxiv.org/abs/2502.13595); 2025; Kenneth Enevoldsen, Isaac Chung, Imene Kerboua, Marton Kardos, Ashwin Mathur, and others; DOI: `10.48550/arXiv.2502.13595`.
- [Zeta Alpha NanoBEIR collection](https://huggingface.co/collections/zeta-alpha-ai/nanobeir).

### Hugging Face Links

- Nano dataset: [hakari-bench/NanoBEIR-es](https://huggingface.co/datasets/hakari-bench/NanoBEIR-es)
- Source collection: [Zeta Alpha NanoBEIR collection](https://huggingface.co/collections/zeta-alpha-ai/nanobeir)

### Source Reference Table

| Title | Year | Type | URL |
| --- | ---: | --- | --- |
| DBpedia-Entity V2: A Test Collection for Entity Search | 2017 | task paper | https://doi.org/10.1145/3077136.3080751 |
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
  task_name: NanoDBPedia
  split_name: NanoDBPedia
  language: es
  category: natural_language
  document_path: docs/benchmark_tasks/MNanoBEIR/NanoBEIR-es__NanoDBPedia.md
  source_research:
    primary_source_type: task_paper
    paper_pdf_or_html_checked: true
    no_paper_note: null
  counts:
    queries: 50
    documents: 6045
    positive_qrels: 1158
  positives_per_query:
    average: 23.16
    min: 1
    median: 18.0
    max: 81
    multi_positive_queries: 48
    multi_positive_query_percent: 96.0
  text_stats_chars:
    query_mean: 37.98
    document_mean: 367.776344
  bm25:
    ndcg_at_10: 0.6139768715463029
    hit_at_10: 0.96
    source: dataset_candidate_subset
  learning:
    original_train_split: available
    evaluation_split_origin: MNanoBEIR Spanish NanoBEIR task split from hakari-bench/NanoBEIR-es
    train_eval_overlap_audit: not_audited
    leakage_note: prefer excluding DBpedia-Entity, BEIR, or NanoBEIR records likely
      to overlap with these evaluation queries or entity pages
    useful_training_data:
    - non-overlapping entity search datasets
    - knowledge-base page retrieval pairs
    - Spanish or multilingual entity linking and description retrieval data
    - hard negatives from same-type entities
    synthetic_data:
      document_generation: Spanish DBpedia-style entity descriptions
      question_generation: short entity-search queries, aliases, categories, and property
        questions
      answerability: positives should be the intended entity pages, not merely same-type
        entities
    multi_positive_training: recommended
  links:
    nano_dataset: https://huggingface.co/datasets/hakari-bench/NanoBEIR-es
    source_urls:
    - label: DBpedia-Entity V2 paper
      url: https://doi.org/10.1145/3077136.3080751
    - label: BEIR paper
      url: https://arxiv.org/abs/2104.08663
    - label: MMTEB paper
      url: https://arxiv.org/abs/2502.13595
    - label: Zeta Alpha NanoBEIR collection
      url: https://huggingface.co/collections/zeta-alpha-ai/nanobeir
    source_notes:
    - Spanish task is a multilingual NanoBEIR adaptation of the original English BEIR
      task
  references:
  - title: 'DBpedia-Entity V2: A Test Collection for Entity Search'
    url: https://doi.org/10.1145/3077136.3080751
    year: 2017
    doi: 10.1145/3077136.3080751
    is_paper: true
    source_confidence: definitive_paper_link
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
      ndcg_at_10: 0.6139768715
      hit_at_10: 0.96
      recall_at_100: 0.677029361
      candidate_count_min: 500
      candidate_count_max: 500
      candidate_count_mean: 500.0
      query_count: 50
      query_coverage: 1.0
      relevant_coverage_at_100: 0.677029361
    dense:
      config: harrier_oss_v1_270m
      label: Dense
      source: dataset_candidate_subset
      top_k: 500
      ndcg_at_10: 0.6098501445
      hit_at_10: 0.94
      recall_at_100: 0.7055267703
      candidate_count_min: 500
      candidate_count_max: 500
      candidate_count_mean: 500.0
      query_count: 50
      query_coverage: 1.0
      relevant_coverage_at_100: 0.7055267703
    reranking_hybrid:
      config: reranking_hybrid
      label: Reranking hybrid
      source: dataset_candidate_subset
      top_k: 100
      ndcg_at_10: 0.6210069573
      hit_at_10: 0.94
      recall_at_100: 0.7262521589
      candidate_count_min: 100
      candidate_count_max: 100
      candidate_count_mean: 100.0
      query_count: 50
      query_coverage: 1.0
      relevant_coverage_at_100: 0.7262521589
      safeguard_positive_rows: 0
      rows_with_101_candidates: 0
```
