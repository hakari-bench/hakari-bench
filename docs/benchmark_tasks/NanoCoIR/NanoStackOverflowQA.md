# NanoCoIR / NanoStackOverflowQA

## Overview

CoIR derives this hybrid code retrieval task from StackOverflow question-answer
pairs, using developer questions as queries and high-voted answers as retrieval
targets. The task reflects practical debugging and framework help: queries often
contain error messages, code snippets, and surrounding context, while positives
mix explanation with runnable fragments. A good retriever must identify the
actual developer problem rather than only match language or library names.

## Details

### What the Original Data Measures

[CoIR](https://arxiv.org/abs/2407.02883) describes StackOverflow QA as a hybrid
code retrieval task derived from the Kaggle StackOverflow dump: user questions
are paired with their highest-voted answers. CoIR samples and splits these
question-answer pairs so retrieval models must find the relevant answer among
other developer answers.

### Observed Data Profile

The Nano split has 200 queries, 10,000 documents, and 200 positive qrels. Each
query has one positive. Queries average 1,361.81 characters and often include
error messages, code excerpts, and framework context. Documents average
1,218.06 characters and mix explanation, code, and sometimes multiple answer
fragments.

### BM25 Difficulty

Using the dataset-provided BM25 candidate column, BM25 reaches nDCG@10 =
0.7403 and hit@10 = 0.8150. It ranks 134 positives first and 163 positives in
the top 10. Lexical overlap from stack traces, API names, and framework terms is
strong, but answers can paraphrase diagnosis and fixes.

### Training Data That May Help

StackOverflow question-answer retrieval, code troubleshooting data, error-message
matching, and hard negatives from the same tag or framework are useful.

### Synthetic Data Guidance

Generate realistic developer questions with code snippets, error text, and
environment details. Positives should diagnose or solve the issue, while hard
negatives should share tags but solve a different failure.

### Benchmark Information Leakage

CoIR builds a StackOverflow QA retrieval task with roughly 13k train queries, 3k
dev queries, and 2k test queries over a 20k-document corpus. This Nano split is
derived from the CoIR StackOverflow QA test side. Training on unfiltered
StackOverflow QA test rows, CoIR-Retrieval exports, or raw StackOverflow dumps
without deduplication can leak the benchmark question-answer pairs.

Training should use train-side or non-overlapping StackOverflow-style QA pairs,
then remove any row whose question title, question body, accepted answer, code
snippet, URL/id, or token fingerprint matches NanoStackOverflowQA. A model
trained on leaked StackOverflow answers may report high scores by memorizing
community posts rather than learning troubleshooting retrieval.

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
| Nano set | NanoCoIR |
| Backing dataset | NanoCoIR |
| Task / split | NanoStackOverflowQA |
| Hugging Face dataset | [hakari-bench/NanoCoIR](https://huggingface.co/datasets/hakari-bench/NanoCoIR) |
| Language | en |
| Category | code |
| Queries | 200 |
| Documents | 10000 |
| Positive qrels | 200 |
| BM25 nDCG@10 | 0.7482 |
| BM25 hit@10 | 0.8300 |
| BM25 Recall@100 | 0.9250 |
| BM25 candidate subset | top-500 (`bm25`) |
| Dense nDCG@10 | 0.8836 |
| Dense hit@10 | 0.9300 |
| Dense Recall@100 | 0.9400 |
| Dense candidate subset | top-500 (`harrier_oss_v1_270m`) |
| Reranking hybrid nDCG@10 | 0.8328 |
| Reranking hybrid hit@10 | 0.8850 |
| Reranking hybrid Recall@100 | 0.9900 |
| Reranking hybrid candidate subset | top-100 plus optional rank-101 safeguard (`reranking_hybrid`) |
| Reranking hybrid candidates / query | 100-101 |
| Reranking hybrid safeguard rows | 2 |
| Query length avg chars | 1361.81 |
| Document length avg chars | 1218.06 |

### Public Sources

- [CoIR](https://arxiv.org/abs/2407.02883); 2025; Xiangyang Li et al.
- [Stack Overflow Data on Kaggle](https://www.kaggle.com/datasets/stackoverflow/stacksample/data).

### Hugging Face Links

- Nano dataset: [hakari-bench/NanoCoIR](https://huggingface.co/datasets/hakari-bench/NanoCoIR)
- Source dataset: [CoIR-Retrieval/stackoverflow-qa](https://huggingface.co/datasets/CoIR-Retrieval/stackoverflow-qa)

### Source Reference Table

| Title | Year | Type | URL |
| --- | ---: | --- | --- |
| CoIR: A Comprehensive Benchmark for Code Information Retrieval Models | 2025 | benchmark paper | https://arxiv.org/abs/2407.02883 |
| Stack Overflow Data | 2025 | source data page | https://www.kaggle.com/datasets/stackoverflow/stacksample/data |

## Machine-Readable Metadata

<!-- benchmark-task-metadata:v1 -->

```yaml
benchmark_task_metadata:
  schema_version: 1
  document_status: first_pass
  nano_set: NanoCoIR
  backing_dataset: NanoCoIR
  dataset_id: hakari-bench/NanoCoIR
  task_name: NanoStackOverflowQA
  split_name: NanoStackOverflowQA
  language: en
  category: code
  document_path: docs/benchmark_tasks/NanoCoIR/NanoStackOverflowQA.md
  source_research:
    primary_source_type: benchmark_paper_and_dataset_card
    paper_pdf_or_html_checked: true
    no_paper_note: no standalone task paper confirmed beyond CoIR construction details
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
    ndcg_at_10: 0.7481959299785959
    hit_at_10: 0.83
    source: dataset_candidate_subset
  learning:
    original_train_split: available
    evaluation_split_origin: CoIR StackOverflow QA test-derived retrieval split
    train_eval_overlap_audit: not_audited_split_filtering_required
    leakage_note: exclude NanoStackOverflowQA question-answer pairs; do not train
      on StackOverflow QA test-derived rows
    leakage_risk:
      source_dataset: CoIR StackOverflow QA / Stack Overflow data
      source_train_queries_reported_by_coir: 13000
      source_dev_queries_reported_by_coir: 3000
      source_test_queries_reported_by_coir: 2000
      risk: upstream StackOverflow QA test pairs can overlap with NanoStackOverflowQA
        evaluation rows
      recommended_filter: train-side only plus normalized title, body, answer, code,
        URL/id, and token-fingerprint exclusion
    useful_training_data:
    - StackOverflow question-answer retrieval
    - code troubleshooting pairs
    - framework-tag hard negatives
    synthetic_data:
      document_generation: developer answers with fixes and code snippets
      question_generation: realistic programming questions with errors and context
      answerability: positive answer must solve or explain the user question
    multi_positive_training: single_positive
  links:
    nano_dataset: https://huggingface.co/datasets/hakari-bench/NanoCoIR
    source_urls:
    - label: CoIR arXiv
      url: https://arxiv.org/abs/2407.02883
    - label: CoIR-Retrieval/stackoverflow-qa
      url: https://huggingface.co/datasets/CoIR-Retrieval/stackoverflow-qa
    - label: Stack Overflow Data on Kaggle
      url: https://www.kaggle.com/datasets/stackoverflow/stacksample/data
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
      ndcg_at_10: 0.74819593
      hit_at_10: 0.83
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
      ndcg_at_10: 0.8835799533
      hit_at_10: 0.93
      recall_at_100: 0.94
      candidate_count_min: 500
      candidate_count_max: 500
      candidate_count_mean: 500.0
      query_count: 200
      query_coverage: 1.0
      relevant_coverage_at_100: 0.94
    reranking_hybrid:
      config: reranking_hybrid
      label: Reranking hybrid
      source: dataset_candidate_subset
      top_k: 100
      ndcg_at_10: 0.8328011758
      hit_at_10: 0.885
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
