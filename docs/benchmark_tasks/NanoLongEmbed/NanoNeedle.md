# NanoLongEmbed / NanoNeedle

## Overview

`NanoNeedle` is LongEmbed's synthetic needle-in-a-haystack retrieval task.
Queries ask for a specific fact, and documents are long base texts with a short
answer-bearing needle inserted. The retriever must find the document containing
the relevant inserted fact rather than only matching the broad surrounding
essay.

## Details

### What the Original Data Measures

[LongEmbed: Extending Embedding Models for Long Context Retrieval](https://arxiv.org/abs/2404.12096)
describes Needle-in-a-haystack Retrieval as a synthetic long-context retrieval
task. In contrast to passkey retrieval, the query is a natural factual question
and the target information is inserted into a longer document. LongEmbed uses
this task to test whether embedding models can retain localized evidence inside
long inputs.

There is no separate standalone dataset paper confirmed for this synthetic
task. The interpretation here is based on the LongEmbed paper, the public
LongEmbed dataset card, and observed Nano examples.

### Observed Data Profile

The Nano split has 98 English queries, 800 candidate documents, and 98 positive
qrels. Every query has one positive. Queries average 58.99 characters, and
documents average 35,246.12 characters. Observed positives are built around a
Paul Graham essay-style base document with inserted facts about formulas,
paintings, novels, geography, and history.

The relevant evidence is usually one sentence, while the surrounding document
is long and topically unrelated. This makes the task a direct test of whether a
document embedding preserves a small inserted fact after long-context pooling.

### BM25 Difficulty

Using the dataset-provided BM25 candidate column, BM25 reaches nDCG@10 =
0.6852 and hit@10 = 0.9286. BM25 ranks 43 positives first and 91 in the top 10,
with a median best rank of 2.

The high hit@10 but lower top-1 rate suggests that lexical terms from the
inserted fact often retrieve the right neighborhood, but repeated base text and
similar inserted question styles make precise ranking difficult.

### Training Data That May Help

There is no separate official train split confirmed for this synthetic task.
Useful training data includes synthetic needle-in-context retrieval, long
document QA with inserted facts, and evidence localization examples over essays
or articles. Training should not use Nano evaluation questions, inserted facts,
qrels, or positive documents.

### Synthetic Data Guidance

Generate long non-evaluation base documents and insert one or a few factual
needle sentences at varied depths. Queries should ask directly for the inserted
fact, including formulas, creators, dates, locations, definitions, and
comparisons. Vary base text, position, and distractor facts, and keep the answer
explicitly grounded in the positive document.

## Example Data

| Query | Positive document |
| --- | --- |
| Who developed the laws of motion and when? (42 chars) | Aaron Swartz created a scraped feed of the essays page. November 2021(This essay is derived from a talk at the Cambridge Union. )When I was a kid, I'd have said there wasn't. My father told me so. Some people like some things ... [truncated 225 chars](1990 chars) |
| Who wrote the novel "The Grapes of Wrath" and when was it published? (68 chars) | Aaron Swartz created a scraped feed of the essays page. November 2021(This essay is derived from a talk at the Cambridge Union. )When I was a kid, I'd have said there wasn't. My father told me so. Some people like some things ... [truncated 225 chars](72045 chars) |
| What is the Panama Canal and what does it connect? (50 chars) | Aaron Swartz created a scraped feed of the essays page. November 2021(This essay is derived from a talk at the Cambridge Union. )When I was a kid, I'd have said there wasn't. My father told me so. Some people like some things ... [truncated 225 chars](4062 chars) |
| What is the formula for calculating the area of a kite? (55 chars) | Aaron Swartz created a scraped feed of the essays page. November 2021(This essay is derived from a talk at the Cambridge Union. )When I was a kid, I'd have said there wasn't. My father told me so. Some people like some things ... [truncated 225 chars](2030 chars) |
| Who wrote the novel "One Hundred Years of Solitude" and when was it published? (78 chars) | Aaron Swartz created a scraped feed of the essays page. The novel "One Hundred Years of Solitude" was written by Gabriel Garcia Marquez and published November 2021(This essay is derived from a talk at the Cambridge Union. )Wh ... [truncated 225 chars](1012 chars) |

## Dataset Information

| Field | Value |
| --- | --- |
| Nano set | NanoLongEmbed |
| Backing dataset | NanoLongEmbed |
| Task / split | NanoNeedle |
| Hugging Face dataset | [hakari-bench/NanoLongEmbed](https://huggingface.co/datasets/hakari-bench/NanoLongEmbed) |
| Language | en |
| Category | natural_language |
| Queries | 98 |
| Documents | 800 |
| Positive qrels | 98 |
| BM25 nDCG@10 | 0.6852 |
| BM25 hit@10 | 0.9286 |
| Query length avg chars | 58.99 |
| Document length avg chars | 35246.12 |

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
  task_name: NanoNeedle
  split_name: NanoNeedle
  language: en
  category: natural_language
  document_path: docs/benchmark_tasks/NanoLongEmbed/NanoNeedle.md
  source_research:
    primary_source_type: benchmark_paper
    paper_pdf_or_html_checked: true
    no_paper_note: no standalone task paper was confirmed; LongEmbed is the source paper for this synthetic retrieval task
  counts:
    queries: 98
    documents: 800
    positive_qrels: 98
  positives_per_query:
    average: 1.0
    min: 1
    median: 1.0
    max: 1
    multi_positive_queries: 0
    multi_positive_query_percent: 0.0
  text_stats_chars:
    query_mean: 58.98979591836735
    document_mean: 35246.1175
  bm25:
    ndcg_at_10: 0.6852432935
    hit_at_10: 0.9285714286
    source: dataset_bm25_column
  learning:
    original_train_split: not_found
    evaluation_split_origin: synthetic
    train_eval_overlap_audit: not_audited
    leakage_note: exclude Nano evaluation questions, inserted facts, qrels, and positive documents
    useful_training_data:
      - synthetic needle-in-context retrieval
      - long document QA with inserted facts
      - evidence localization over essays or articles
      - position-robust factual retrieval examples
    synthetic_data:
      document_generation: long non-evaluation base documents with explicit factual needle sentences inserted at varied depths
      question_generation: natural factual questions about formulas, creators, dates, locations, definitions, and comparisons
      answerability: each answer should be explicitly stated in the inserted needle sentence inside the positive document
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
    - title: "LongEmbed: Extending Embedding Models for Long Context Retrieval"
      url: https://arxiv.org/abs/2404.12096
      year: 2024
      doi: 10.18653/v1/2024.emnlp-main.47
      is_paper: true
      source_confidence: definitive_paper_link
```
