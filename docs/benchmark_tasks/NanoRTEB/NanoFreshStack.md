# NanoRTEB / NanoFreshStack

## Overview

`NanoRTEB / NanoFreshStack` retrieves technical documentation and code-oriented
documents for recent community programming questions.

## Details

### What the Original Data Measures

[FreshStack: Building Realistic Benchmarks for Evaluating Retrieval on Technical
Documents](https://arxiv.org/abs/2504.13128) introduces a framework for building
realistic IR/RAG benchmarks from niche, recent technical domains. The paper
describes collecting technical document corpora, using community questions and
answers to generate information nuggets, and labeling nugget-level document
support.

[Introducing RTEB: A New Standard for Retrieval Evaluation](https://huggingface.co/blog/rteb)
includes FreshStack as an open English technical retrieval task. This Nano split
therefore measures retrieval for practical developer questions over
documentation, release notes, tests, and code-adjacent text.

### Observed Data Profile

The split has 200 queries, 3,770 documents, and 1,522 positive qrel rows.
Queries average 1,660.21 characters and documents average 4,983.03 characters.
Most queries are multi-positive: 189 queries have more than one positive, with
an average of 7.61 positives per query.

### BM25 Difficulty

Using the dataset-provided BM25 candidate column, BM25 reaches nDCG@10 =
0.2755 and hit@10 = 0.6750. It ranks 70 queries at rank 1 and finds a positive
in the top 10 for 135 queries.

BM25 can match API names, Angular symbols, and exact error terms, but technical
questions are long and often require connecting a problem report to a relevant
documentation section or test file. Multi-positive nugget labels make recall
important.

### Training Data That May Help

Useful data includes technical-doc retrieval, StackOverflow question to
documentation retrieval, issue-to-doc linking, code/documentation contrastive
training, and hard negatives from the same framework version.

### Synthetic Data Guidance

Generate realistic developer questions from non-evaluation documentation,
release notes, and code examples. Pair each question with multiple supporting
documents when appropriate. Hard negatives should use the same API names but
different versions, lifecycle hooks, or framework behavior.

## Example Data

| Query | Positive document |
| --- | --- |
| My buttons are displayed (show method) after a short pause, and if I hover the mouse cursor over the position where the button will be and leave it, the button will not realize that it is hovered. This is fixed when moving th ... [truncated 225 chars](403 chars) | <?xml version="1.0" encoding="UTF-8" ?> <class name="InputEventMouse" inherits="InputEventWithModifiers" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:noNamespaceSchemaLocation="../class.xsd"> <brief_description> ... [truncated 225 chars](1732 chars) |
| Angular is failing to compile because of the following error and I'm really confused as to why. error TS2322: Type 'string' is not assignable to type 'MenuItem'. 4 <menu-item item={{item}}></menu-item> ~~~~ apps/angular-monor ... [truncated 225 chars](1922 chars) | # Binding dynamic text, properties and attributes In Angular, a **binding** creates a dynamic connection between a component's template and its data. This connection ensures that changes to the component's data automatically ... [truncated 225 chars](9518 chars) |
| I am testing angular 16 signals and per my understanding, when I disable zone.js and call signal.update() the view should be updated with new value. It is not. Please help me to understand why. main.ts platformBrowserDynamic( ... [truncated 225 chars](734 chars) | # Resolving zone pollution **Zone.js** is a signaling mechanism that Angular uses to detect when an application state might have changed. It captures asynchronous operations like `setTimeout`, network requests, and event list ... [truncated 225 chars](5856 chars) |
| After exporting my project to Android a directory named .godot/exported appeared in the root of my Godot project. It seems to contain some cache for the resources I have exported. Problem is, autofill gets scenes from it when ... [truncated 225 chars](852 chars) | revent race condition on initial breakpoints from DAP ([GH-84895](https://github.com/godotengine/godot/pull/84895)). - Do not bother with line colors if `line_number_gutter` is not yet calculated ([GH-84907](https://github.co ... [truncated 225 chars](6827 chars) |
| I have an Angular 17 application that uses server-side rendering. The state of the application is managed using ngrx. When I access the page, I can see that the page comes pre-rendered (by viewing the source of the page, for ... [truncated 225 chars](1264 chars) | # Angular SSR Read the dev guide [here](https://angular.dev/guide/ssr). (72 chars) |

## Dataset Information

| Field | Value |
| --- | --- |
| Nano set | NanoRTEB |
| Backing dataset | NanoRTEB |
| Task / split | NanoFreshStack |
| Hugging Face dataset | [hakari-bench/NanoRTEB](https://huggingface.co/datasets/hakari-bench/NanoRTEB) |
| Source dataset | [mteb/FreshStackRetrieval](https://huggingface.co/datasets/mteb/FreshStackRetrieval) |
| Language | en |
| Category | natural_language |
| Queries | 200 |
| Documents | 3,770 |
| Positive qrels | 1,522 |
| Positives per query | avg 7.61 / min 1 / median 7 / max 21 |
| Multi-positive queries | 189 |
| BM25 nDCG@10 | 0.2755 |
| BM25 hit@10 | 0.6750 |
| Query length avg chars | 1,660.21 |
| Document length avg chars | 4,983.03 |

### Public Sources

- [FreshStack: Building Realistic Benchmarks for Evaluating Retrieval on Technical Documents](https://arxiv.org/abs/2504.13128), task paper.
- [FreshStack project site](https://fresh-stack.github.io/), project page.
- [mteb/FreshStackRetrieval](https://huggingface.co/datasets/mteb/FreshStackRetrieval), source retrieval dataset card.
- [Introducing RTEB: A New Standard for Retrieval Evaluation](https://huggingface.co/blog/rteb), RTEB benchmark announcement.

### Hugging Face Links

- Nano dataset: [hakari-bench/NanoRTEB](https://huggingface.co/datasets/hakari-bench/NanoRTEB)
- Source task dataset: [mteb/FreshStackRetrieval](https://huggingface.co/datasets/mteb/FreshStackRetrieval)

### Source Reference Table

| Title | Year | Type | URL |
| --- | ---: | --- | --- |
| FreshStack: Building Realistic Benchmarks for Evaluating Retrieval on Technical Documents | 2025 | task paper | https://arxiv.org/abs/2504.13128 |
| FreshStack project site | 2025 | project page | https://fresh-stack.github.io/ |
| mteb/FreshStackRetrieval |  | dataset card | https://huggingface.co/datasets/mteb/FreshStackRetrieval |
| Introducing RTEB: A New Standard for Retrieval Evaluation | 2025 | benchmark article | https://huggingface.co/blog/rteb |

## Machine-Readable Metadata

<!-- benchmark-task-metadata:v1 -->

```yaml
benchmark_task_metadata:
  schema_version: 1
  document_status: first_pass
  nano_set: NanoRTEB
  backing_dataset: NanoRTEB
  dataset_id: hakari-bench/NanoRTEB
  task_name: NanoFreshStack
  split_name: NanoFreshStack
  language: en
  category: natural_language
  document_path: docs/benchmark_tasks/NanoRTEB/NanoFreshStack.md
  source_research:
    primary_source_type: task_paper
    paper_pdf_or_html_checked: true
    no_paper_note: null
  counts:
    queries: 200
    documents: 3770
    positive_qrels: 1522
  positives_per_query:
    average: 7.61
    min: 1
    median: 7.0
    max: 21
    multi_positive_queries: 189
    multi_positive_query_percent: 94.5
  text_stats_chars:
    query_mean: 1660.21
    document_mean: 4983.03
  bm25:
    ndcg_at_10: 0.2755
    hit_at_10: 0.675
    source: dataset_bm25_column
  example_count: 5
```
