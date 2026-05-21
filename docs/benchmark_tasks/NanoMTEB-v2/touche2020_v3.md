# NanoMTEB-v2 / touche2020_v3

## Overview

`touche2020_v3` is an argument retrieval task from Touché 2020. Queries are
controversial questions, and relevant documents are argumentative passages or
debate-style texts.

## Details

### What the Original Data Measures

[Touché 2020 Task 1](https://downloads.webis.de/touche/publications/papers/bondarenko_2020d.pdf)
focused on argument retrieval for controversial questions. Systems retrieve
documents that contain relevant arguments, often from web or debate material.
[MTEB](https://arxiv.org/abs/2210.07316) includes the Webis Touché retrieval
dataset as an English retrieval task.

### Observed Data Profile

The split has 49 queries, 10,000 documents, and 1,704 positive qrels. Queries
average 43.43 characters and are short controversial questions. Documents are
long, averaging 2386.21 characters, with some very long debate-style passages.
Every query is highly multi-positive, with a median of 33 positives.

### BM25 Difficulty

Using the dataset-provided BM25 candidate column, BM25 reaches nDCG@10 =
0.8083 and hit@10 = 0.9796. It ranks 39 queries with a positive first, and the
median best positive rank is 1. Lexical cues from the controversy topic help
BM25, but ranking the best arguments among many relevant passages remains a
separate relevance-quality problem.

### Training Data That May Help

Useful data includes argument retrieval collections, debate passages aligned to
controversial questions, stance and claim-evidence corpora, and hard negatives
from the same topic with weak or off-target argumentation.

### Synthetic Data Guidance

Generate controversial questions and multiple pro/con argumentative passages.
Hard negatives should discuss the same issue but answer a different aspect or
provide unsupported commentary rather than a usable argument.

## Example Data

| Query | Positive document |
| --- | --- |
| Is homework beneficial? (23 chars) | First, there are three arguments for why homework is excellent and ought to continue in modern schools. 1. Homework aids doer-learners. It is generally accepted that there are three types of learners: those who learn by heari ... [truncated 225 chars](3553 chars) |
| Should prescription drugs be advertised directly to consumers? (62 chars) | Many ads don't include enough information on how well drugs work. For example, Lunesta is advertised by a moth floating through a bedroom window, above a peacefully sleeping person. Actually, Lunesta helps patients sleep 15 m ... [truncated 225 chars](1682 chars) |
| Should any vaccines be required for children? (45 chars) | Not a full case yet.. Just some little points I put together... Governments should not have the right to intervene in the health decisions parents make for their children. 31% of parents believe they should have the right to ... [truncated 225 chars](4497 chars) |
| Should abortion be legal? (25 chars) | Abortions should be legal as Personhood begins after a fetus becomes viable or after birth, not at conception. According to the U.S. Supreme Court a person is to get their age when they are out of the mother's womb and breath ... [truncated 225 chars](309 chars) |
| Do standardized tests improve education? (40 chars) | Resolved: The SAT, ACT, and other standardized tests provided more insight into a high school student's preparedness for education at elite colleges and universities than high school GPA and therefore should play a greater ro ... [truncated 225 chars](4159 chars) |

## Dataset Information

| Field | Value |
| --- | --- |
| Nano set | NanoMTEB-v2 |
| Backing dataset | NanoMTEB-v2 |
| Task / split | touche2020_v3 |
| Source task | Touche2020Retrieval.v3 |
| Hugging Face dataset | [hakari-bench/NanoMTEB-v2](https://huggingface.co/datasets/hakari-bench/NanoMTEB-v2) |
| Source dataset | [mteb/webis-touche2020-v3](https://huggingface.co/datasets/mteb/webis-touche2020-v3) |
| Language | en |
| Category | natural_language |
| Queries | 49 |
| Documents | 10000 |
| Positive qrels | 1704 |
| Positives per query | avg 34.78, min 6, median 33, max 65 |
| Multi-positive queries | 49 (100.00%) |
| BM25 nDCG@10 | 0.8083 |
| BM25 hit@10 | 0.9796 |
| Query length avg chars | 43.43 |
| Document length avg chars | 2386.21 |

### Public Sources

- [Overview of Touché 2020: Argument Retrieval](https://downloads.webis.de/touche/publications/papers/bondarenko_2020d.pdf).
- [MTEB: Massive Text Embedding Benchmark](https://arxiv.org/abs/2210.07316).
- [mteb/webis-touche2020-v3](https://huggingface.co/datasets/mteb/webis-touche2020-v3).

### Hugging Face Links

- Nano dataset: [hakari-bench/NanoMTEB-v2](https://huggingface.co/datasets/hakari-bench/NanoMTEB-v2)
- Source dataset: [mteb/webis-touche2020-v3](https://huggingface.co/datasets/mteb/webis-touche2020-v3)

### Source Reference Table

| Title | Year | Type | URL |
| --- | ---: | --- | --- |
| Overview of Touché 2020: Argument Retrieval | 2020 | source task paper | https://downloads.webis.de/touche/publications/papers/bondarenko_2020d.pdf |
| MTEB: Massive Text Embedding Benchmark | 2023 | benchmark paper | https://arxiv.org/abs/2210.07316 |
| mteb/webis-touche2020-v3 | 2024 | dataset card | https://huggingface.co/datasets/mteb/webis-touche2020-v3 |

## Machine-Readable Metadata

<!-- benchmark-task-metadata:v1 -->

```yaml
benchmark_task_metadata:
  schema_version: 1
  document_status: first_pass
  nano_set: NanoMTEB-v2
  backing_dataset: NanoMTEB-v2
  dataset_id: hakari-bench/NanoMTEB-v2
  task_name: touche2020_v3
  split_name: touche2020_v3
  source_task: Touche2020Retrieval.v3
  source_dataset_id: mteb/webis-touche2020-v3
  language: en
  category: natural_language
  document_path: docs/benchmark_tasks/NanoMTEB-v2/touche2020_v3.md
  source_research:
    primary_source_type: task_paper_and_benchmark_paper
    paper_pdf_or_html_checked: true
    no_paper_note: null
  counts:
    queries: 49
    documents: 10000
    positive_qrels: 1704
  positives_per_query:
    average: 34.775510204081634
    min: 6
    median: 33
    max: 65
    multi_positive_queries: 49
    multi_positive_query_percent: 100.0
  text_stats_chars:
    query_mean: 43.42857142857143
    document_mean: 2386.2117
  bm25:
    ndcg_at_10: 0.8082621810352335
    hit_at_10: 0.9795918367346939
    source: dataset_bm25_column
  learning:
    original_train_split: available
    evaluation_split_origin: MTEB Webis Touché 2020 v3 test split
    train_eval_overlap_audit: not_audited
    leakage_note: exclude NanoMTEB-v2 touche2020_v3 controversial questions and passages
    useful_training_data:
      - argument retrieval data
      - debate passage collections
      - stance and claim-evidence corpora
    synthetic_data:
      document_generation: pro and con argumentative passages for controversial topics
      question_generation: short controversial questions
      answerability: positive should contain a relevant argument for the question
    multi_positive_training: required
  links:
    nano_dataset: https://huggingface.co/datasets/hakari-bench/NanoMTEB-v2
    source_urls:
      - label: Touché 2020 overview
        url: https://downloads.webis.de/touche/publications/papers/bondarenko_2020d.pdf
      - label: MTEB arXiv
        url: https://arxiv.org/abs/2210.07316
      - label: mteb/webis-touche2020-v3
        url: https://huggingface.co/datasets/mteb/webis-touche2020-v3
    source_notes: []
  references:
    - title: "Overview of Touché 2020: Argument Retrieval"
      url: https://downloads.webis.de/touche/publications/papers/bondarenko_2020d.pdf
      year: 2020
      is_paper: true
      source_confidence: definitive_paper_link
    - title: "MTEB: Massive Text Embedding Benchmark"
      url: https://arxiv.org/abs/2210.07316
      year: 2023
      is_paper: true
      source_confidence: definitive_paper_link
```
