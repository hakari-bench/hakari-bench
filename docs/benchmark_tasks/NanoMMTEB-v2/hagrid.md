# NanoMMTEB-v2 / hagrid

## Overview

`hagrid` is an English information-seeking retrieval task from HAGRID. Queries
are short fact-seeking questions, and documents are concise answer passages with
citation markers. The task tests whether retrievers can identify directly
attributable evidence for generative question answering.

## Details

### What the Original Data Measures

[HAGRID: A Human-LLM Collaborative Dataset for Generative Information-Seeking with Attribution](https://arxiv.org/abs/2307.16883)
builds on MIRACL-style information-seeking questions and relevant passages, then
adds generated answers and human judgments of informativeness and
attributability. The retrieval split focuses on returning candidate quotes or
passages that support an answer.

### Observed Data Profile

The Nano split has 200 queries, 493 documents, and 200 positive qrels. Each
query has one positive. Queries are short English questions averaging 38.36
characters, and documents average 229.57 characters. Most documents are compact
answer snippets with explicit citation markers such as `[1]`.

### BM25 Difficulty

Using the dataset-provided BM25 candidate column, BM25 reaches nDCG@10 = 0.9657
and hit@10 = 0.9900. Lexical matching is very strong because questions and
answer passages often share named entities and core terms; the remaining
difficulty is mostly distinguishing near-duplicate factual snippets.

### Training Data That May Help

Useful training data includes open-domain QA retrieval, attributable answer
support selection, quote retrieval, and non-overlapping MIRACL or Wikipedia
question-passage pairs. Training should avoid memorizing HAGRID evaluation
questions or snippets.

### Synthetic Data Guidance

Generate short factual questions and concise answer-bearing passages with
source-like citation markers. Add negatives that mention the same entity but
answer a different attribute, date, or location. Synthetic positives should
support the answer explicitly and be suitable as cited evidence.

## Example Data

| Query | Positive document |
| --- | --- |
| How many clubs are in the Australian Football League? (53 chars) | The Australian Football League consists of 18 clubs [1][2] (58 chars) |
| What was the film Nausicaä of the Valley of the Wind adapted from? (66 chars) | Nausicaä of the Valley of the Wind was adapted from the manga series of the same name written and illustrated by Hayao Miyazaki. [4] (132 chars) |
| Is Abi Branning still a character on EastEnders? (48 chars) | No, Abi Branning is not a regular character on EastEnders as she was killed off in January 2018 after falling from the roof of The Queen Victoria pub [2]. However, she did make a few guest appearances in 2018, with one being ... [truncated 225 chars](281 chars) |
| Where was Loretta Lynn born? (28 chars) | Loretta Lynn was born in Butcher Hollow, Kentucky. [1][2] (57 chars) |
| How old is the Cincinnati Bengals? (34 chars) | The Cincinnati Bengals are 51 years old overall and have been playing in the National Football League for 49 seasons [1]. (121 chars) |

## Dataset Information

| Field | Value |
| --- | --- |
| Nano set | NanoMMTEB-v2 |
| Backing dataset | NanoMMTEB-v2 |
| Task / split | hagrid |
| Hugging Face dataset | [hakari-bench/NanoMMTEB-v2](https://huggingface.co/datasets/hakari-bench/NanoMMTEB-v2) |
| Source dataset | [mteb/HagridRetrieval](https://huggingface.co/datasets/mteb/HagridRetrieval) |
| Language | en |
| Category | natural_language |
| Queries | 200 |
| Documents | 493 |
| Positive qrels | 200 |
| BM25 nDCG@10 | 0.9814 |
| BM25 hit@10 | 0.9950 |
| BM25 Recall@100 | 0.9950 |
| BM25 candidate subset | top-500 (`bm25`) |
| Dense nDCG@10 | 0.9570 |
| Dense hit@10 | 0.9650 |
| Dense Recall@100 | 0.9800 |
| Dense candidate subset | top-500 (`harrier_oss_v1_270m`) |
| Reranking hybrid nDCG@10 | 0.9639 |
| Reranking hybrid hit@10 | 0.9800 |
| Reranking hybrid Recall@100 | 1.0000 |
| Reranking hybrid candidate subset | top-100 plus optional rank-101 safeguard (`reranking_hybrid`) |
| Reranking hybrid candidates / query | 100 |
| Reranking hybrid safeguard rows | 0 |
| Query length avg chars | 38.36 |
| Document length avg chars | 229.57 |

### Public Sources

- [HAGRID: A Human-LLM Collaborative Dataset for Generative Information-Seeking with Attribution](https://arxiv.org/abs/2307.16883).
- [HAGRID GitHub repository](https://github.com/project-miracl/hagrid).
- [mteb/HagridRetrieval](https://huggingface.co/datasets/mteb/HagridRetrieval).

### Hugging Face Links

- Nano dataset: [hakari-bench/NanoMMTEB-v2](https://huggingface.co/datasets/hakari-bench/NanoMMTEB-v2)
- Source dataset: [mteb/HagridRetrieval](https://huggingface.co/datasets/mteb/HagridRetrieval)

### Source Reference Table

| Title | Year | Type | URL |
| --- | ---: | --- | --- |
| HAGRID: A Human-LLM Collaborative Dataset for Generative Information-Seeking with Attribution | 2023 | task paper | https://arxiv.org/abs/2307.16883 |
| HAGRID GitHub repository | 2023 | project page | https://github.com/project-miracl/hagrid |
| mteb/HagridRetrieval | 2024 | dataset card | https://huggingface.co/datasets/mteb/HagridRetrieval |

## Machine-Readable Metadata

<!-- benchmark-task-metadata:v1 -->

```yaml
benchmark_task_metadata:
  schema_version: 1
  document_status: first_pass
  nano_set: NanoMMTEB-v2
  backing_dataset: NanoMMTEB-v2
  dataset_id: hakari-bench/NanoMMTEB-v2
  task_name: hagrid
  split_name: hagrid
  language: en
  category: natural_language
  document_path: docs/benchmark_tasks/NanoMMTEB-v2/hagrid.md
  source_research:
    primary_source_type: task_paper
    paper_pdf_or_html_checked: true
    no_paper_note: null
  counts:
    queries: 200
    documents: 493
    positive_qrels: 200
  positives_per_query:
    average: 1.0
    min: 1
    median: 1.0
    max: 1
    multi_positive_queries: 0
    multi_positive_query_percent: 0.0
  text_stats_chars:
    query_mean: 38.36
    document_mean: 229.56795131845843
  bm25:
    ndcg_at_10: 0.9814278926071437
    hit_at_10: 0.995
    source: dataset_candidate_subset
  learning:
    original_train_split: available
    evaluation_split_origin: dev
    train_eval_overlap_audit: not_audited
    leakage_note: do not train on this Nano split's questions, qrels, or cited answer
      passages
    useful_training_data:
    - open-domain QA retrieval pairs
    - attributable answer support selection data
    - non-overlapping MIRACL or Wikipedia question-passage pairs
    - same-entity factual hard negatives
    synthetic_data:
      document_generation: concise answer snippets with citation-like source markers
      question_generation: short fact-seeking questions about entities, dates, and
        places
      answerability: positive passage should explicitly support a cited answer
    multi_positive_training: single_positive_question_document_focus
  links:
    nano_dataset: https://huggingface.co/datasets/hakari-bench/NanoMMTEB-v2
    source_urls:
    - label: HAGRID arXiv
      url: https://arxiv.org/abs/2307.16883
    - label: HAGRID GitHub
      url: https://github.com/project-miracl/hagrid
    - label: mteb/HagridRetrieval
      url: https://huggingface.co/datasets/mteb/HagridRetrieval
    source_notes: []
  references:
  - title: 'HAGRID: A Human-LLM Collaborative Dataset for Generative Information-Seeking
      with Attribution'
    url: https://arxiv.org/abs/2307.16883
    year: 2023
    is_paper: true
    source_confidence: definitive_paper_link
  candidate_subsets:
    bm25:
      config: bm25
      label: BM25
      source: dataset_candidate_subset
      top_k: 500
      ndcg_at_10: 0.9814278926
      hit_at_10: 0.995
      recall_at_100: 0.995
      candidate_count_min: 493
      candidate_count_max: 493
      candidate_count_mean: 493.0
      query_count: 200
      query_coverage: 1.0
      relevant_coverage_at_100: 0.995
    dense:
      config: harrier_oss_v1_270m
      label: Dense
      source: dataset_candidate_subset
      top_k: 500
      ndcg_at_10: 0.9569639463
      hit_at_10: 0.965
      recall_at_100: 0.98
      candidate_count_min: 493
      candidate_count_max: 493
      candidate_count_mean: 493.0
      query_count: 200
      query_coverage: 1.0
      relevant_coverage_at_100: 0.98
    reranking_hybrid:
      config: reranking_hybrid
      label: Reranking hybrid
      source: dataset_candidate_subset
      top_k: 100
      ndcg_at_10: 0.9639131544
      hit_at_10: 0.98
      recall_at_100: 1.0
      candidate_count_min: 100
      candidate_count_max: 100
      candidate_count_mean: 100.0
      query_count: 200
      query_coverage: 1.0
      relevant_coverage_at_100: 1.0
      safeguard_positive_rows: 0
      rows_with_101_candidates: 0
```
