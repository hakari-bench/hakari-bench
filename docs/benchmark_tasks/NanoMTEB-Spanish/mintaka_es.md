# NanoMTEB-Spanish / mintaka_es

## Overview

`mintaka_es` is the Spanish Mintaka retrieval split in `NanoMTEB-Spanish`.
Queries are Spanish complex QA questions, and documents are very short answer
strings or entity names. The retriever must map a Spanish question to the
correct answer entity, often across question types such as superlative,
comparison, and multi-hop.

## Details

### What the Original Data Measures

[Mintaka: A Complex, Natural, and Multilingual Dataset for End-to-End Question Answering](https://arxiv.org/abs/2210.01613)
introduces 20,000 English question-answer pairs annotated with Wikidata
entities and professionally translated into eight languages, including Spanish,
for 180,000 samples. The paper emphasizes complex naturally elicited questions,
including count, comparison, superlative, intersection, and multi-hop types.

The MTEB retrieval packaging converts Mintaka QA into answer retrieval: the
question is the query and the answer text is the relevant document. This means
the task is closer to entity-answer selection than passage retrieval.

### Observed Data Profile

The Nano split has 200 Spanish queries, 1,693 candidate answer documents, and
200 positive qrels. Every query has one positive. Queries average 66.93
characters, while documents average only 14.29 characters. Sampled positives
include `Marlee Matlin`, `50 Cent`, `Pirates of the Caribbean: Dead Man's
Chest`, `Lo que el viento se llevó`, and `Sting`.

Because documents are answer strings, many positives contain no Spanish
context. A model must connect the Spanish question to a multilingual entity or
title, not rely on long-document evidence.

### BM25 Difficulty

Using the dataset-provided BM25 candidate column, BM25 reaches nDCG@10 =
0.2467 and hit@10 = 0.3050. Only 36 positives are ranked first, and the median
best rank is 100. The sampled questions show why: many correct documents are
short names that share few tokens with the question.

### Training Data That May Help

Useful training data includes non-overlapping Mintaka train examples, Spanish
entity-linking QA pairs, Wikidata question-to-entity supervision, and
multilingual paraphrases of complex questions. Training should exclude Mintaka
test examples, Nano queries, qrels, and positive answer strings likely to
overlap with this evaluation.

### Synthetic Data Guidance

Generate Spanish complex questions over Wikidata-like entities, with answer
documents as short canonical names. Include superlatives, comparisons,
intersection conditions, counts, and multi-hop relations. Do not use Nano
evaluation questions or answer strings as seeds.

## Example Data

| Query | Positive document |
| --- | --- |
| En orden cronológico, ¿cuál es la segunda película de Crepúsculo? (65 chars) | The Twilight Saga: New Moon (27 chars) |
| ¿Qué película de Harry Potter es dirigida por Alfonso Cuarón? (61 chars) | Harry Potter y el prisionero de Azkaban (39 chars) |
| ¿Quién es más joven, Drew Barrymore o Reese Whiterspoon? (56 chars) | Reese Witherspoon (17 chars) |
| ¿Qué película de dibujos animados se estrenó en 2007 y fue dirigida por Tim Hill? (81 chars) | Alvin and the Chipmunks (23 chars) |
| En orden cronológico, ¿cuál es la tercera película de Crepúsculo? (65 chars) | The Twilight Saga: Eclipse (26 chars) |

## Dataset Information

| Field | Value |
| --- | --- |
| Nano set | NanoMTEB-Spanish |
| Backing dataset | NanoMTEB-Spanish |
| Task / split | mintaka_es |
| Hugging Face dataset | [hakari-bench/NanoMTEB-Spanish](https://huggingface.co/datasets/hakari-bench/NanoMTEB-Spanish) |
| Language | es, en |
| Category | natural_language |
| Queries | 200 |
| Documents | 1693 |
| Positive qrels | 200 |
| BM25 nDCG@10 | 0.2502 |
| BM25 hit@10 | 0.3150 |
| BM25 Recall@100 | 0.3500 |
| BM25 candidate subset | top-500 (`bm25`) |
| Dense nDCG@10 | 0.3614 |
| Dense hit@10 | 0.5100 |
| Dense Recall@100 | 0.7500 |
| Dense candidate subset | top-500 (`harrier_oss_v1_270m`) |
| Reranking hybrid nDCG@10 | 0.2721 |
| Reranking hybrid hit@10 | 0.3300 |
| Reranking hybrid Recall@100 | 0.6200 |
| Reranking hybrid candidate subset | top-100 plus optional rank-101 safeguard (`reranking_hybrid`) |
| Reranking hybrid candidates / query | 100-101 |
| Reranking hybrid safeguard rows | 76 |
| Query length avg chars | 66.93 |
| Document length avg chars | 14.29 |

### Public Sources

- [Mintaka: A Complex, Natural, and Multilingual Dataset for End-to-End Question Answering](https://arxiv.org/abs/2210.01613); 2022; Priyanka Sen, Alham Fikri Aji, Amir Saffari.
- [mteb/MintakaRetrieval dataset card](https://huggingface.co/datasets/mteb/MintakaRetrieval).
- [MTEB: Massive Text Embedding Benchmark](https://arxiv.org/abs/2210.07316); 2023; Niklas Muennighoff et al.

### Hugging Face Links

- Nano dataset: [hakari-bench/NanoMTEB-Spanish](https://huggingface.co/datasets/hakari-bench/NanoMTEB-Spanish)
- Source dataset: [mteb/MintakaRetrieval](https://huggingface.co/datasets/mteb/MintakaRetrieval)

### Source Reference Table

| Title | Year | Type | URL |
| --- | ---: | --- | --- |
| Mintaka: A Complex, Natural, and Multilingual Dataset for End-to-End Question Answering | 2022 | arXiv paper | https://arxiv.org/abs/2210.01613 |
| MTEB: Massive Text Embedding Benchmark | 2023 | arXiv paper | https://arxiv.org/abs/2210.07316 |
| mteb/MintakaRetrieval | 2025 | dataset card | https://huggingface.co/datasets/mteb/MintakaRetrieval |

## Machine-Readable Metadata

<!-- benchmark-task-metadata:v1 -->

```yaml
benchmark_task_metadata:
  schema_version: 1
  document_status: first_pass
  nano_set: NanoMTEB-Spanish
  backing_dataset: NanoMTEB-Spanish
  dataset_id: hakari-bench/NanoMTEB-Spanish
  task_name: mintaka_es
  split_name: mintaka_es
  language: multilingual
  category: natural_language
  document_path: docs/benchmark_tasks/NanoMTEB-Spanish/mintaka_es.md
  source_research:
    primary_source_type: task_paper
    paper_pdf_or_html_checked: true
    no_paper_note: null
  counts:
    queries: 200
    documents: 1693
    positive_qrels: 200
  positives_per_query:
    average: 1.0
    min: 1
    median: 1.0
    max: 1
    multi_positive_queries: 0
    multi_positive_query_percent: 0.0
  text_stats_chars:
    query_mean: 66.925
    document_mean: 14.291789722386296
  bm25:
    ndcg_at_10: 0.25018493566322303
    hit_at_10: 0.315
    source: dataset_candidate_subset
  learning:
    original_train_split: available
    evaluation_split_origin: test
    train_eval_overlap_audit: not_audited
    leakage_note: exclude Mintaka test examples, Nano queries, qrels, and answer strings
      likely to overlap with this evaluation
    useful_training_data:
    - non-overlapping Mintaka train examples
    - Spanish Wikidata entity-linking QA pairs
    - multilingual complex question paraphrases
    - hard negatives with related entity names
    synthetic_data:
      document_generation: short canonical entity or answer strings from Wikidata-like
        domains
      question_generation: Spanish complex QA questions with superlative, comparison,
        count, intersection, and multi-hop forms
      answerability: each answer string should be the canonical entity or value implied
        by the question
    multi_positive_training: single_positive_question_document_focus
  links:
    nano_dataset: https://huggingface.co/datasets/hakari-bench/NanoMTEB-Spanish
    source_urls:
    - label: Mintaka arXiv
      url: https://arxiv.org/abs/2210.01613
    - label: mteb/MintakaRetrieval
      url: https://huggingface.co/datasets/mteb/MintakaRetrieval
    - label: MTEB arXiv
      url: https://arxiv.org/abs/2210.07316
    source_notes: []
  references:
  - title: 'Mintaka: A Complex, Natural, and Multilingual Dataset for End-to-End Question
      Answering'
    url: https://arxiv.org/abs/2210.01613
    year: 2022
    doi: 10.48550/arXiv.2210.01613
    is_paper: true
    source_confidence: definitive_paper_link
  candidate_subsets:
    bm25:
      config: bm25
      label: BM25
      source: dataset_candidate_subset
      top_k: 500
      ndcg_at_10: 0.2501849357
      hit_at_10: 0.315
      recall_at_100: 0.35
      candidate_count_min: 500
      candidate_count_max: 500
      candidate_count_mean: 500.0
      query_count: 200
      query_coverage: 1.0
      relevant_coverage_at_100: 0.35
    dense:
      config: harrier_oss_v1_270m
      label: Dense
      source: dataset_candidate_subset
      top_k: 500
      ndcg_at_10: 0.361428097
      hit_at_10: 0.51
      recall_at_100: 0.75
      candidate_count_min: 500
      candidate_count_max: 500
      candidate_count_mean: 500.0
      query_count: 200
      query_coverage: 1.0
      relevant_coverage_at_100: 0.75
    reranking_hybrid:
      config: reranking_hybrid
      label: Reranking hybrid
      source: dataset_candidate_subset
      top_k: 100
      ndcg_at_10: 0.2721193099
      hit_at_10: 0.33
      recall_at_100: 0.62
      candidate_count_min: 100
      candidate_count_max: 101
      candidate_count_mean: 100.38
      query_count: 200
      query_coverage: 1.0
      relevant_coverage_at_100: 0.62
      safeguard_positive_rows: 76
      rows_with_101_candidates: 76
```
