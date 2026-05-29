# NanoMTEB-Spanish / miracl_es

## Overview

`miracl_es` is the Spanish MIRACL retrieval split in `NanoMTEB-Spanish`.
Queries are Spanish information needs, and documents are Spanish Wikipedia
passages. The retriever must rank all relevant answer-bearing passages for each
query, not only one passage.

## Details

### What the Original Data Measures

[Making a MIRACL: Multilingual Information Retrieval Across a Continuum of Languages](https://arxiv.org/abs/2210.09984)
introduces a multilingual ad hoc retrieval benchmark covering 18 languages,
including Spanish. The paper describes monolingual retrieval over Wikipedia,
native-speaker query and judgment creation, and train/dev/test splits with
passage-level relevance judgments.

The MTEB hard-negative version pools documents from BM25 and dense retrievers.
In this Nano split, the query and documents are both Spanish, and many queries
have several positive passages.

### Observed Data Profile

The Nano split has 200 Spanish queries, 10,000 documents, and 934 positive
qrels. Queries average 47.65 characters, documents average 555.02 characters,
and 86.0% of queries have multiple positives. Sampled questions cover sports,
Paraguayan music, ancient Greek philosophy, guerrilla agriculture, and
PlayStation.

Documents are Wikipedia-like passages with titles at the beginning. Positive
sets may include several passages from the same article or related articles, so
multi-positive retrieval behavior matters.

### BM25 Difficulty

Using the dataset-provided BM25 candidate column, BM25 reaches nDCG@10 =
0.5246 and hit@10 = 0.9300. BM25 puts 88 queries' best positive at rank 1 and
186 queries' best positive in the top 10.

The high hit@10 but moderate nDCG reflects multi-positive ranking: BM25 often
finds at least one relevant Wikipedia passage, but does not necessarily order
all relevant passages well.

### Training Data That May Help

Useful training data includes the non-overlapping MIRACL Spanish train split,
Spanish Wikipedia question-passage pairs, and multilingual retrieval data with
native Spanish queries. Training should avoid MIRACL dev/test data, Nano
queries, qrels, and positive passages likely to overlap with this evaluation.
Multi-positive losses or listwise distillation are useful here.

### Synthetic Data Guidance

Generate Spanish Wikipedia-style passages and Spanish search questions grounded
in named entities, definitions, dates, events, and comparisons. For
multi-positive training, create several relevant passages per query and hard
negatives from the same topic area. Do not seed generation from Nano evaluation
queries or positives.

## Example Data

| Query | Positive document |
| --- | --- |
| ¿Cómo es la arquitectura del caravasar de Orbelián? (51 chars) | Caravasar de Orbelian El caravasar está construido con bloques de basalto. (75 chars) |
| ¿Cómo llaman los judíos al Pentateuco? (38 chars) | Pentateuco Se corresponde con los que en la tradición hebrea forman la "Torá" —La Ley—, núcleo de la religión judía. Los cinco libros que lo componen son:Está contenido a su vez en el "Tanaj", el cual es considerado sagrado p ... [truncated 225 chars](679 chars) |
| ¿Cuándo recibió Daniel Harold Rolling la inyección letal de su condenación? (75 chars) | Daniel Harold Rolling Rolling fue ejecutado por inyección letal en prisión estatal de Florida el 25 de octubre de 2006, después de que la Corte Suprema de Estados Unidos rechazó una última apelación. Fue declarado fallecido a ... [truncated 225 chars](241 chars) |
| ¿Cómo definir el parlamentarismo? (33 chars) | Parlamentarismo El parlamentarismo, también conocido como sistema parlamentario o «régimen parlamentario» es en política, un sistema de gobierno en el que la elección del gobierno (poder ejecutivo) emana del parlamento (poder ... [truncated 225 chars](500 chars) |
| ¿Cuál era la misión de la Guardia Pretoriana? (45 chars) | Guardia Pretoriana La Guardia Pretoriana era un cuerpo militar que servía de escolta y protección a los emperadores romanos. Antes de los emperadores, esta escolta ya era usada por los líderes militares desde la época de los ... [truncated 225 chars](387 chars) |

## Dataset Information

| Field | Value |
| --- | --- |
| Nano set | NanoMTEB-Spanish |
| Backing dataset | NanoMTEB-Spanish |
| Task / split | miracl_es |
| Hugging Face dataset | [hakari-bench/NanoMTEB-Spanish](https://huggingface.co/datasets/hakari-bench/NanoMTEB-Spanish) |
| Language | es |
| Category | natural_language |
| Queries | 200 |
| Documents | 10000 |
| Positive qrels | 934 |
| Avg positives / query | 4.67 |
| Positives per query (min / median / max) | 1 / 4.0 / 10 |
| Queries with multiple positives | 172 (86.00%) |
| BM25 nDCG@10 | 0.5620 |
| BM25 hit@10 | 0.9400 |
| BM25 Recall@100 | 0.9743 |
| BM25 candidate subset | top-500 (`bm25`) |
| Dense nDCG@10 | 0.7481 |
| Dense hit@10 | 0.9250 |
| Dense Recall@100 | 0.9122 |
| Dense candidate subset | top-500 (`harrier_oss_v1_270m`) |
| Reranking hybrid nDCG@10 | 0.7042 |
| Reranking hybrid hit@10 | 0.9900 |
| Reranking hybrid Recall@100 | 0.9989 |
| Reranking hybrid candidate subset | top-100 plus optional rank-101 safeguard (`reranking_hybrid`) |
| Reranking hybrid candidates / query | 100 |
| Reranking hybrid safeguard rows | 0 |
| Query length avg chars | 47.65 |
| Document length avg chars | 555.02 |

### Public Sources

- [Making a MIRACL: Multilingual Information Retrieval Across a Continuum of Languages](https://arxiv.org/abs/2210.09984); 2023; Xueguang Ma et al.
- [mteb/MIRACLRetrievalHardNegatives dataset card](https://huggingface.co/datasets/mteb/MIRACLRetrievalHardNegatives).
- [MTEB: Massive Text Embedding Benchmark](https://arxiv.org/abs/2210.07316); 2023; Niklas Muennighoff et al.

### Hugging Face Links

- Nano dataset: [hakari-bench/NanoMTEB-Spanish](https://huggingface.co/datasets/hakari-bench/NanoMTEB-Spanish)
- Source dataset: [mteb/MIRACLRetrievalHardNegatives](https://huggingface.co/datasets/mteb/MIRACLRetrievalHardNegatives)

### Source Reference Table

| Title | Year | Type | URL |
| --- | ---: | --- | --- |
| Making a MIRACL: Multilingual Information Retrieval Across a Continuum of Languages | 2023 | arXiv paper | https://arxiv.org/abs/2210.09984 |
| MTEB: Massive Text Embedding Benchmark | 2023 | arXiv paper | https://arxiv.org/abs/2210.07316 |
| mteb/MIRACLRetrievalHardNegatives | 2025 | dataset card | https://huggingface.co/datasets/mteb/MIRACLRetrievalHardNegatives |

## Machine-Readable Metadata

<!-- benchmark-task-metadata:v1 -->

```yaml
benchmark_task_metadata:
  schema_version: 1
  document_status: first_pass
  nano_set: NanoMTEB-Spanish
  backing_dataset: NanoMTEB-Spanish
  dataset_id: hakari-bench/NanoMTEB-Spanish
  task_name: miracl_es
  split_name: miracl_es
  language: es
  category: natural_language
  document_path: docs/benchmark_tasks/NanoMTEB-Spanish/miracl_es.md
  source_research:
    primary_source_type: task_paper
    paper_pdf_or_html_checked: true
    no_paper_note: null
  counts:
    queries: 200
    documents: 10000
    positive_qrels: 934
  positives_per_query:
    average: 4.67
    min: 1
    median: 4.0
    max: 10
    multi_positive_queries: 172
    multi_positive_query_percent: 86.0
  text_stats_chars:
    query_mean: 47.65
    document_mean: 555.024
  bm25:
    ndcg_at_10: 0.5620061185917705
    hit_at_10: 0.94
    source: dataset_candidate_subset
  learning:
    original_train_split: available
    evaluation_split_origin: dev
    train_eval_overlap_audit: not_audited
    leakage_note: exclude MIRACL dev/test data, Nano queries, qrels, and positive
      Spanish Wikipedia passages likely to overlap with this evaluation
    useful_training_data:
    - non-overlapping MIRACL Spanish train data
    - Spanish Wikipedia question-passage retrieval pairs
    - native Spanish multilingual retrieval data
    - hard negatives from related Wikipedia entities
    synthetic_data:
      document_generation: Spanish Wikipedia-style passages with titles, entities,
        dates, definitions, and event descriptions
      question_generation: native Spanish search questions answerable by one or more
        passages
      answerability: each query should have explicit evidence in every positive passage
    multi_positive_training: multi_positive_objective
  links:
    nano_dataset: https://huggingface.co/datasets/hakari-bench/NanoMTEB-Spanish
    source_urls:
    - label: MIRACL arXiv
      url: https://arxiv.org/abs/2210.09984
    - label: mteb/MIRACLRetrievalHardNegatives
      url: https://huggingface.co/datasets/mteb/MIRACLRetrievalHardNegatives
    - label: MTEB arXiv
      url: https://arxiv.org/abs/2210.07316
    source_notes: []
  references:
  - title: 'Making a MIRACL: Multilingual Information Retrieval Across a Continuum
      of Languages'
    url: https://arxiv.org/abs/2210.09984
    year: 2023
    doi: 10.1162/tacl_a_00595
    is_paper: true
    source_confidence: definitive_paper_link
  candidate_subsets:
    bm25:
      config: bm25
      label: BM25
      source: dataset_candidate_subset
      top_k: 500
      ndcg_at_10: 0.5620061186
      hit_at_10: 0.94
      recall_at_100: 0.9743040685
      candidate_count_min: 500
      candidate_count_max: 500
      candidate_count_mean: 500.0
      query_count: 200
      query_coverage: 1.0
      relevant_coverage_at_100: 0.9743040685
    dense:
      config: harrier_oss_v1_270m
      label: Dense
      source: dataset_candidate_subset
      top_k: 500
      ndcg_at_10: 0.74805075
      hit_at_10: 0.925
      recall_at_100: 0.9122055675
      candidate_count_min: 500
      candidate_count_max: 500
      candidate_count_mean: 500.0
      query_count: 200
      query_coverage: 1.0
      relevant_coverage_at_100: 0.9122055675
    reranking_hybrid:
      config: reranking_hybrid
      label: Reranking hybrid
      source: dataset_candidate_subset
      top_k: 100
      ndcg_at_10: 0.7041973434
      hit_at_10: 0.99
      recall_at_100: 0.9989293362
      candidate_count_min: 100
      candidate_count_max: 100
      candidate_count_mean: 100.0
      query_count: 200
      query_coverage: 1.0
      relevant_coverage_at_100: 0.9989293362
      safeguard_positive_rows: 0
      rows_with_101_candidates: 0
```
