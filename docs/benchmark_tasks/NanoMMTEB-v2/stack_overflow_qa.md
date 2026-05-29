# NanoMMTEB-v2 / stack_overflow_qa

## Overview

`stack_overflow_qa` is an English developer-question retrieval task. Queries are
Stack Overflow questions that may include error messages or code snippets, and
documents are answer posts. The retriever must find the answer that resolves the
developer's issue.

## Details

### What the Original Data Measures

[CoIR: A Comprehensive Benchmark for Code Information Retrieval Models](https://arxiv.org/abs/2407.02883)
describes StackOverflow QA as a single-turn code question-answer retrieval task
derived by pairing Stack Overflow questions with high-voted answers. The task is
important because code information retrieval often mixes natural language,
identifiers, API names, snippets, and troubleshooting context.

### Observed Data Profile

The split has 200 queries, 10,000 documents, and 200 positive qrels. Each query
has one positive. Queries average 1,361.80 characters and can be long posts with
code, stack traces, and attempts. Documents average 1,218.06 characters and may
contain prose, API references, and code snippets.

### BM25 Difficulty

Using the dataset-provided BM25 candidate column, BM25 reaches nDCG@10 = 0.7482
and hit@10 = 0.8300. Exact API names, error strings, and framework terms make
lexical retrieval strong, but semantic troubleshooting is still needed when the
answer explains a cause rather than repeating the full question.

### Training Data That May Help

Useful data includes Stack Overflow question-answer pairs, documentation
retrieval, API examples, issue-to-fix pairs, and code-search tasks. Training
should exclude the evaluation questions and answer posts, especially exact
duplicates from public Stack Overflow dumps.

### Synthetic Data Guidance

Generate realistic developer questions with language, library, version, error,
and minimal code context. Answers should include concrete fixes or explanations.
Hard negatives should mention the same API or error family but solve a different
failure mode.

## Example Data

| Query | Positive document |
| --- | --- |
| How to block mouse click events from another form I have a winforms single form application that uses a "Thickbox" I've created whenever the loads a new view into the application form. The "Thickbox" shows another form in fro ... [truncated 225 chars](1644 chars) | I'm glad to announce that the problem is finally solved. After spending a few days attempting to recreate this bug in a new application, re-constructing the main form in the application, comment out parts of the code in the m ... [truncated 225 chars](916 chars) |
| Passing a parameter to a $resource? I have a controller that that looks like this: (function() { angular .module("main") .controller("HomeCtrl", ["branchResource", "adalAuthenticationService", HomeCtrl]); function HomeCtrl(br ... [truncated 225 chars](1406 chars) | Create the $resource object with: function branchResource($resource){ ̶r̶e̶t̶u̶r̶n̶ ̶$̶r̶e̶s̶o̶u̶r̶c̶e̶(̶"̶/̶a̶p̶i̶/̶u̶s̶e̶r̶/̶G̶e̶t̶A̶l̶l̶U̶s̶e̶r̶B̶r̶a̶n̶c̶h̶e̶s̶?̶f̶e̶d̶e̶r̶a̶t̶e̶d̶U̶s̶e̶r̶N̶a̶m̶e̶=̶:̶u̶s̶e̶r̶"̶)̶ ̶ return ... [truncated 225 chars](991 chars) |
| Chrome doesn’t show un-minified code in spite of source map present I’m using Grunt and UglifyJS to generate source maps for my AngularJS app. It produces a file customDomain.js and customDomain.js.map. JS file Last line of c ... [truncated 225 chars](910 chars) | "sources":["customDomain.js"] should be relative to the customDomain.map.js file. Make sure they are in the same directory on your server if this is the case for you. "file":"customDomain.js" should be changed to the name of ... [truncated 225 chars](641 chars) |
| Get looked up array count for a document i have 2 collections : words and phrases Each word document has an array of phrases id's. And each phrase can be active or inactive. For example : words : {"word" => "hello", phrases = ... [truncated 225 chars](2051 chars) | db.words.aggregate([ { "$unwind" : "$phrases"}, { "$lookup": { "from": "phrases", "localField": "phrases", "foreignField": "id", "as": "phrases_data" } }, { "$match" : { "phrases_data.active" : 1} }, { "$group" : { "_id" : "$ ... [truncated 225 chars](683 chars) |
| Inno Setup Remove version number from "Setup has detected that ... is currently running" I've added the line AppMutex={#MyAppName} to my InnoSetup script, and #MyAppName does NOT include the version number. However, when my S ... [truncated 225 chars](694 chars) | You are wrong. The message is: SetupAppRunningError=Setup has detected that %1 is currently running.%n%nPlease close all instances of it now, then click OK to continue, or Cancel to exit. Where the %1 is replaced by value of ... [truncated 225 chars](858 chars) |

## Dataset Information

| Field | Value |
| --- | --- |
| Nano set | NanoMMTEB-v2 |
| Backing dataset | NanoMMTEB-v2 |
| Task / split | stack_overflow_qa |
| Hugging Face dataset | [hakari-bench/NanoMMTEB-v2](https://huggingface.co/datasets/hakari-bench/NanoMMTEB-v2) |
| Source dataset | [mteb/StackOverflowQA](https://huggingface.co/datasets/mteb/StackOverflowQA) |
| Language | en |
| Category | natural_language |
| Queries | 200 |
| Documents | 10000 |
| Positive qrels | 200 |
| BM25 nDCG@10 | 0.7970 |
| BM25 hit@10 | 0.8700 |
| BM25 Recall@100 | 0.9250 |
| BM25 candidate subset | top-500 (`bm25`) |
| Dense nDCG@10 | 0.8886 |
| Dense hit@10 | 0.9350 |
| Dense Recall@100 | 0.9450 |
| Dense candidate subset | top-500 (`harrier_oss_v1_270m`) |
| Reranking hybrid nDCG@10 | 0.8457 |
| Reranking hybrid hit@10 | 0.8900 |
| Reranking hybrid Recall@100 | 0.9900 |
| Reranking hybrid candidate subset | top-100 plus optional rank-101 safeguard (`reranking_hybrid`) |
| Reranking hybrid candidates / query | 100-101 |
| Reranking hybrid safeguard rows | 2 |
| Query length avg chars | 1361.80 |
| Document length avg chars | 1218.06 |

### Public Sources

- [CoIR: A Comprehensive Benchmark for Code Information Retrieval Models](https://arxiv.org/abs/2407.02883).
- [mteb/StackOverflowQA](https://huggingface.co/datasets/mteb/StackOverflowQA).

### Hugging Face Links

- Nano dataset: [hakari-bench/NanoMMTEB-v2](https://huggingface.co/datasets/hakari-bench/NanoMMTEB-v2)
- Source dataset: [mteb/StackOverflowQA](https://huggingface.co/datasets/mteb/StackOverflowQA)

### Source Reference Table

| Title | Year | Type | URL |
| --- | ---: | --- | --- |
| CoIR: A Comprehensive Benchmark for Code Information Retrieval Models | 2025 | benchmark paper | https://arxiv.org/abs/2407.02883 |
| mteb/StackOverflowQA | 2024 | dataset card | https://huggingface.co/datasets/mteb/StackOverflowQA |

## Machine-Readable Metadata

<!-- benchmark-task-metadata:v1 -->

```yaml
benchmark_task_metadata:
  schema_version: 1
  document_status: first_pass
  nano_set: NanoMMTEB-v2
  backing_dataset: NanoMMTEB-v2
  dataset_id: hakari-bench/NanoMMTEB-v2
  task_name: stack_overflow_qa
  split_name: stack_overflow_qa
  language: en
  category: natural_language
  document_path: docs/benchmark_tasks/NanoMMTEB-v2/stack_overflow_qa.md
  source_research:
    primary_source_type: benchmark_paper
    paper_pdf_or_html_checked: true
    no_paper_note: No standalone StackOverflowQA retrieval paper was confirmed; CoIR
      benchmark paper and dataset card were checked.
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
    query_mean: 1361.805
    document_mean: 1218.0589
  bm25:
    ndcg_at_10: 0.7969967730952047
    hit_at_10: 0.87
    source: dataset_candidate_subset
  learning:
    original_train_split: available
    evaluation_split_origin: test
    train_eval_overlap_audit: not_audited
    leakage_note: do not train on this Nano split's Stack Overflow questions, qrels,
      or answer posts
    useful_training_data:
    - Stack Overflow question-answer pairs
    - documentation retrieval pairs
    - API example retrieval
    - issue-to-fix and error-message retrieval data
    synthetic_data:
      document_generation: developer answers with fixes, explanations, code snippets,
        and version constraints
      question_generation: realistic developer questions with errors, APIs, snippets,
        and attempted solutions
      answerability: positive answer should resolve the stated developer problem
    multi_positive_training: single_positive_question_document_focus
  links:
    nano_dataset: https://huggingface.co/datasets/hakari-bench/NanoMMTEB-v2
    source_urls:
    - label: CoIR arXiv
      url: https://arxiv.org/abs/2407.02883
    - label: mteb/StackOverflowQA
      url: https://huggingface.co/datasets/mteb/StackOverflowQA
    source_notes: []
  references:
  - title: 'CoIR: A Comprehensive Benchmark for Code Information Retrieval Models'
    url: https://arxiv.org/abs/2407.02883
    year: 2025
    is_paper: true
    source_confidence: definitive_paper_link
  candidate_subsets:
    bm25:
      config: bm25
      label: BM25
      source: dataset_candidate_subset
      top_k: 500
      ndcg_at_10: 0.7969967731
      hit_at_10: 0.87
      recall_at_100: 0.925
      candidate_count_min: 500
      candidate_count_max: 500
      candidate_count_mean: 500.0
      query_count: 200
      query_coverage: 1.0
      relevant_coverage_at_100: 0.925
    dense:
      config: harrier_oss_v1_270m
      label: Dense
      source: dataset_candidate_subset
      top_k: 500
      ndcg_at_10: 0.8885799533
      hit_at_10: 0.935
      recall_at_100: 0.945
      candidate_count_min: 500
      candidate_count_max: 500
      candidate_count_mean: 500.0
      query_count: 200
      query_coverage: 1.0
      relevant_coverage_at_100: 0.945
    reranking_hybrid:
      config: reranking_hybrid
      label: Reranking hybrid
      source: dataset_candidate_subset
      top_k: 100
      ndcg_at_10: 0.8457480743
      hit_at_10: 0.89
      recall_at_100: 0.99
      candidate_count_min: 100
      candidate_count_max: 101
      candidate_count_mean: 100.01
      query_count: 200
      query_coverage: 1.0
      relevant_coverage_at_100: 0.99
      safeguard_positive_rows: 2
      rows_with_101_candidates: 2
```
