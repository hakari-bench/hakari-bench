# NanoLongEmbed / NanoPasskey

## Overview

`NanoPasskey` is LongEmbed's synthetic personalized passkey retrieval task.
Queries ask for the passkey associated with a named person, and documents are
long filler contexts containing exactly the requested passkey statement. The
retriever must find the document that contains the right name-key association.

## Details

### What the Original Data Measures

[LongEmbed: Extending Embedding Models for Long Context Retrieval](https://arxiv.org/abs/2404.12096)
describes Personalized Passkey Retrieval as a synthetic task for testing
whether long-context embedding models retain a small piece of target
information inside a long document. The query names the person, while the
positive document embeds the matching passkey among repetitive filler.

There is no separate standalone dataset paper confirmed for this synthetic
task. The interpretation here is based on the LongEmbed paper, the public
LongEmbed dataset card, and observed Nano examples.

### Observed Data Profile

The Nano split has 100 English queries, 800 candidate documents, and 100
positive qrels. Every query has one positive. Queries average 37.80 characters,
and documents average 28,956.68 characters. The observed examples use repeated
sentences such as "The grass is green" and "The sky is blue" around a sentence
like "Cooper McCann's pass key is 6718."

The query is short and formulaic, but the relevant sentence can occur at
different positions and context lengths. Because many documents share the same
filler text, the person name and passkey sentence carry almost all relevance.

### BM25 Difficulty

Using the dataset-provided BM25 candidate column, BM25 reaches nDCG@10 =
0.7506 and hit@10 = 0.9900. BM25 finds almost every positive somewhere in the
top 10, but it ranks only 47 positives first and has a median best rank of 2.

This is a useful diagnostic: lexical matching sees the rare person name, but
the repetitive documents make top-1 ordering fragile. A strong model should
retain the exact name-key association after pooling a long context.

### Training Data That May Help

There is no separate official train split confirmed for this synthetic task.
Useful training data can include synthetic key-value retrieval tasks, named
entity attribute lookup, and long-context QA over inserted facts. Training
should not use Nano evaluation names, passkeys, qrels, or positive documents.

### Synthetic Data Guidance

Generate long filler documents with one explicit key-value fact linking a
person or entity to an identifier. Vary context length, fact position, filler
templates, names, and identifier format. Queries should ask for the associated
identifier, and each positive should contain exactly the requested association.

## Example Data

| Query | Positive document |
| --- | --- |
| what is the passkey for Ronan Day? (34 chars) | The grass is green. The sky is blue. The sun is yellow. Here we go. There and back again. The grass is green. The sky is blue. The sun is yellow. Here we go. There and back again. The grass is green. The sky is blue. Ronan Da ... [truncated 225 chars](1778 chars) |
| what is the passkey for Flora Wu? (33 chars) | The grass is green. The sky is blue. The sun is yellow. Here we go. There and back again. The grass is green. The sky is blue. The sun is yellow. Here we go. There and back again. The grass is green. The sky is blue. The sun ... [truncated 225 chars](3598 chars) |
| what is the passkey for Summer Walton? (38 chars) | The grass is green. The sky is blue. The sun is yellow. Here we go. There and back again. The grass is green. The sky is blue. The sun is yellow. Here we go. There and back again. The grass is green. The sky is blue. The sun ... [truncated 225 chars](3608 chars) |
| what is the passkey for Cassidy Wolf? (37 chars) | The grass is green. The sky is blue. The sun is yellow. Here we go. There and back again. The grass is green. The sky is blue. The sun is yellow. Here we go. There and back again. The grass is green. The sky is blue. The sun ... [truncated 225 chars](1784 chars) |
| what is the passkey for Archer Peralta? (39 chars) | The grass is green. The sky is blue. The sun is yellow. Here we go. There and back again. The grass is green. The sky is blue. The sun is yellow. Here we go. There and back again. The grass is green. The sky is blue. The sun ... [truncated 225 chars](878 chars) |

## Dataset Information

| Field | Value |
| --- | --- |
| Nano set | NanoLongEmbed |
| Backing dataset | NanoLongEmbed |
| Task / split | NanoPasskey |
| Hugging Face dataset | [hakari-bench/NanoLongEmbed](https://huggingface.co/datasets/hakari-bench/NanoLongEmbed) |
| Language | en |
| Category | natural_language |
| Queries | 100 |
| Documents | 800 |
| Positive qrels | 100 |
| BM25 nDCG@10 | 0.7717 |
| BM25 hit@10 | 1.0000 |
| BM25 Recall@100 | 1.0000 |
| BM25 candidate subset | top-500 (`bm25`) |
| Dense nDCG@10 | 0.6473 |
| Dense hit@10 | 1.0000 |
| Dense Recall@100 | 1.0000 |
| Dense candidate subset | top-500 (`harrier_oss_v1_270m`) |
| Reranking hybrid nDCG@10 | 0.7294 |
| Reranking hybrid hit@10 | 1.0000 |
| Reranking hybrid Recall@100 | 1.0000 |
| Reranking hybrid candidate subset | top-100 plus optional rank-101 safeguard (`reranking_hybrid`) |
| Reranking hybrid candidates / query | 100 |
| Reranking hybrid safeguard rows | 0 |
| Query length avg chars | 37.80 |
| Document length avg chars | 28956.68 |

### Public Sources

- [LongEmbed: Extending Embedding Models for Long Context Retrieval](https://arxiv.org/abs/2404.12096); 2024; Dawei Zhu et al.; DOI: `10.18653/v1/2024.emnlp-main.47`.
- [dwzhu/LongEmbed dataset card](https://huggingface.co/datasets/dwzhu/LongEmbed).

### Hugging Face Links

- Nano dataset: [hakari-bench/NanoLongEmbed](https://huggingface.co/datasets/hakari-bench/NanoLongEmbed)
- Source dataset: [dwzhu/LongEmbed](https://huggingface.co/datasets/dwzhu/LongEmbed)

### Source Reference Table

| Title | Year | Type | URL |
| --- | ---: | --- | --- |
| LongEmbed: Extending Embedding Models for Long Context Retrieval | 2024 | arXiv paper | https://arxiv.org/abs/2404.12096 |
| dwzhu/LongEmbed | 2024 | dataset card | https://huggingface.co/datasets/dwzhu/LongEmbed |

## Machine-Readable Metadata

<!-- benchmark-task-metadata:v1 -->

```yaml
benchmark_task_metadata:
  schema_version: 1
  document_status: first_pass
  nano_set: NanoLongEmbed
  backing_dataset: NanoLongEmbed
  dataset_id: hakari-bench/NanoLongEmbed
  task_name: NanoPasskey
  split_name: NanoPasskey
  language: en
  category: natural_language
  document_path: docs/benchmark_tasks/NanoLongEmbed/NanoPasskey.md
  source_research:
    primary_source_type: benchmark_paper
    paper_pdf_or_html_checked: true
    no_paper_note: no standalone task paper was confirmed; LongEmbed is the source
      paper for this synthetic retrieval task
  counts:
    queries: 100
    documents: 800
    positive_qrels: 100
  positives_per_query:
    average: 1.0
    min: 1
    median: 1.0
    max: 1
    multi_positive_queries: 0
    multi_positive_query_percent: 0.0
  text_stats_chars:
    query_mean: 37.8
    document_mean: 28956.68
  bm25:
    ndcg_at_10: 0.7717469202122306
    hit_at_10: 1.0
    source: dataset_candidate_subset
  learning:
    original_train_split: not_found
    evaluation_split_origin: synthetic
    train_eval_overlap_audit: not_audited
    leakage_note: exclude Nano evaluation names, passkeys, qrels, and positive documents
    useful_training_data:
    - synthetic key-value retrieval over long contexts
    - named entity attribute lookup pairs
    - long-context QA over inserted facts
    - position-robust retrieval examples
    synthetic_data:
      document_generation: long filler documents with one explicit entity-to-identifier
        passkey fact at varied positions
      question_generation: short questions asking for the identifier associated with
        a named person or entity
      answerability: each positive should contain exactly the requested association
        and enough distractor filler to test long-context retention
    multi_positive_training: single_positive_question_document_focus
  links:
    nano_dataset: https://huggingface.co/datasets/hakari-bench/NanoLongEmbed
    source_urls:
    - label: LongEmbed arXiv
      url: https://arxiv.org/abs/2404.12096
    - label: dwzhu/LongEmbed
      url: https://huggingface.co/datasets/dwzhu/LongEmbed
    source_notes: []
  references:
  - title: 'LongEmbed: Extending Embedding Models for Long Context Retrieval'
    url: https://arxiv.org/abs/2404.12096
    year: 2024
    doi: 10.18653/v1/2024.emnlp-main.47
    is_paper: true
    source_confidence: definitive_paper_link
  candidate_subsets:
    bm25:
      config: bm25
      label: BM25
      source: dataset_candidate_subset
      top_k: 500
      ndcg_at_10: 0.7717469202
      hit_at_10: 1.0
      recall_at_100: 1.0
      candidate_count_min: 500
      candidate_count_max: 500
      candidate_count_mean: 500.0
      query_count: 100
      query_coverage: 1.0
      relevant_coverage_at_100: 1.0
    dense:
      config: harrier_oss_v1_270m
      label: Dense
      source: dataset_candidate_subset
      top_k: 500
      ndcg_at_10: 0.6473220347
      hit_at_10: 1.0
      recall_at_100: 1.0
      candidate_count_min: 500
      candidate_count_max: 500
      candidate_count_mean: 500.0
      query_count: 100
      query_coverage: 1.0
      relevant_coverage_at_100: 1.0
    reranking_hybrid:
      config: reranking_hybrid
      label: Reranking hybrid
      source: dataset_candidate_subset
      top_k: 100
      ndcg_at_10: 0.7294399112
      hit_at_10: 1.0
      recall_at_100: 1.0
      candidate_count_min: 100
      candidate_count_max: 100
      candidate_count_mean: 100.0
      query_count: 100
      query_coverage: 1.0
      relevant_coverage_at_100: 1.0
      safeguard_positive_rows: 0
      rows_with_101_candidates: 0
```
