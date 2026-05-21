# NanoMTEB-v2 / cqadupstack_unix

## Overview

CQADupStack's Unix slice evaluates duplicate-question retrieval for Unix and
Linux administration, shell use, and command-line workflows. This NanoMTEB-v2
task uses terse Unix StackExchange titles as queries and longer posts as
candidate duplicate documents. The observed corpus contains command snippets,
error messages, shell examples, paths, duplicate markers, and configuration
details, so relevance is the same operational problem, not merely the same
command name or subsystem.

## Details

### What the Original Data Measures

[CQADupStack](https://eltimster.github.io/www/pubs/adcs2015.pdf) is a
StackExchange duplicate-question benchmark for community question-answering
research. The Unix subset tests whether a retrieval model can connect terse
technical questions to previously asked duplicate questions. [MTEB](https://arxiv.org/abs/2210.07316)
includes CQADupStack subsets as retrieval tasks evaluated with nDCG@10.

### Observed Data Profile

The split has 200 queries, 10,000 documents, and 486 positive qrels. Queries
average 49.21 characters, while documents average 969.12 characters and often
include command snippets, error messages, shell examples, and StackExchange
duplicate markers. Positives average 2.43 per query, but the median is 1 and
one query has 22 positives.

### BM25 Difficulty

Using the dataset-provided BM25 candidate column, BM25 reaches nDCG@10 =
0.3666 and hit@10 = 0.5350. It ranks 65 queries with a positive first, while
the median best positive rank is 8. Lexical matching helps when commands,
paths, or tool names repeat, but duplicate questions often use different
phrasing around the same Unix operation.

### Training Data That May Help

Useful data includes StackExchange duplicate-question pairs, Unix and shell
support forums, command-error paraphrase pairs, and hard negatives from the
same tool or command family.

### Synthetic Data Guidance

Generate short command-line problem titles and longer duplicate questions that
use different filenames, flags, or failure descriptions. Hard negatives should
share tools such as `sed`, `sudo`, `df`, or `screen` while asking about a
different operation.

## Example Data

| Query | Positive document |
| --- | --- |
| copy sas file from prior version directory to new version directory (67 chars) | How to copy datasets from prior version directory to latest version directory I've go a number of directories named like: /data/db/OX/8_10 /data/db/OX/9_1 /data/db/OX/9_2 And need to copy some files (all the `pt.*` files) fro ... [truncated 225 chars](718 chars) |
| Linux Mint Booting Installed Partition (38 chars) | How can I fix/install/reinstall grub? So I started out with a 250GB HDD, the stock drive from an EeePC 1015pem that I am trying to turn into a MintBook. The drive is physically operable, but all data has been nuked, including ... [truncated 225 chars](914 chars) |
| Yanked USB Key During Move (26 chars) | Recovering accidentally deleted files I accidentally deleted a file from my laptop. I'm using Fedora. Is it possible to recover the file? (138 chars) |
| How proc gets updated about the devices (39 chars) | How frequently is the proc file system updated on Linux? How frequently is the `proc` file system updated on Linux? Is it 20 milliseconds (time quantum)? (154 chars) |
| bashrc in custom folder (23 chars) | Change the location of .bashrc Is it possible to change the location of `.bashrc` from `/home/orhanc/.bashrc` to some other directory? (135 chars) |

## Dataset Information

| Field | Value |
| --- | --- |
| Nano set | NanoMTEB-v2 |
| Backing dataset | NanoMTEB-v2 |
| Task / split | cqadupstack_unix |
| Source task | CQADupstackUnixRetrieval |
| Hugging Face dataset | [hakari-bench/NanoMTEB-v2](https://huggingface.co/datasets/hakari-bench/NanoMTEB-v2) |
| Source dataset | [mteb/cqadupstack-unix](https://huggingface.co/datasets/mteb/cqadupstack-unix) |
| Language | en |
| Category | natural_language |
| Queries | 200 |
| Documents | 10000 |
| Positive qrels | 486 |
| Positives per query | avg 2.43, min 1, median 1, max 22 |
| Multi-positive queries | 84 (42.00%) |
| BM25 nDCG@10 | 0.3666 |
| BM25 hit@10 | 0.5350 |
| Query length avg chars | 49.21 |
| Document length avg chars | 969.12 |

### Public Sources

- [CQADupStack](https://eltimster.github.io/www/pubs/adcs2015.pdf).
- [MTEB: Massive Text Embedding Benchmark](https://arxiv.org/abs/2210.07316).
- [mteb/cqadupstack-unix](https://huggingface.co/datasets/mteb/cqadupstack-unix).

### Hugging Face Links

- Nano dataset: [hakari-bench/NanoMTEB-v2](https://huggingface.co/datasets/hakari-bench/NanoMTEB-v2)
- Source dataset: [mteb/cqadupstack-unix](https://huggingface.co/datasets/mteb/cqadupstack-unix)

### Source Reference Table

| Title | Year | Type | URL |
| --- | ---: | --- | --- |
| CQADupStack: A Benchmark Data Set for Community Question-Answering Research | 2015 | source task paper | https://eltimster.github.io/www/pubs/adcs2015.pdf |
| MTEB: Massive Text Embedding Benchmark | 2023 | benchmark paper | https://arxiv.org/abs/2210.07316 |
| mteb/cqadupstack-unix | 2024 | dataset card | https://huggingface.co/datasets/mteb/cqadupstack-unix |

## Machine-Readable Metadata

<!-- benchmark-task-metadata:v1 -->

```yaml
benchmark_task_metadata:
  schema_version: 1
  document_status: first_pass
  nano_set: NanoMTEB-v2
  backing_dataset: NanoMTEB-v2
  dataset_id: hakari-bench/NanoMTEB-v2
  task_name: cqadupstack_unix
  split_name: cqadupstack_unix
  source_task: CQADupstackUnixRetrieval
  source_dataset_id: mteb/cqadupstack-unix
  language: en
  category: natural_language
  document_path: docs/benchmark_tasks/NanoMTEB-v2/cqadupstack_unix.md
  source_research:
    primary_source_type: task_paper_and_benchmark_paper
    paper_pdf_or_html_checked: true
    no_paper_note: null
  counts:
    queries: 200
    documents: 10000
    positive_qrels: 486
  positives_per_query:
    average: 2.43
    min: 1
    median: 1.0
    max: 22
    multi_positive_queries: 84
    multi_positive_query_percent: 42.0
  text_stats_chars:
    query_mean: 49.205
    document_mean: 969.1243
  bm25:
    ndcg_at_10: 0.36656783742488813
    hit_at_10: 0.535
    source: dataset_bm25_column
  learning:
    original_train_split: available
    evaluation_split_origin: MTEB CQADupStack Unix test split
    train_eval_overlap_audit: not_audited
    leakage_note: exclude NanoMTEB-v2 cqadupstack_unix duplicate-question pairs
    useful_training_data:
      - StackExchange duplicate-question pairs
      - Unix and shell support questions
      - same-command hard negatives
    synthetic_data:
      document_generation: long Unix StackExchange questions with commands and errors
      question_generation: short duplicate-style Unix problem titles
      answerability: positive should be a duplicate or near-duplicate technical question
    multi_positive_training: recommended
  links:
    nano_dataset: https://huggingface.co/datasets/hakari-bench/NanoMTEB-v2
    source_urls:
      - label: CQADupStack paper
        url: https://eltimster.github.io/www/pubs/adcs2015.pdf
      - label: MTEB arXiv
        url: https://arxiv.org/abs/2210.07316
      - label: mteb/cqadupstack-unix
        url: https://huggingface.co/datasets/mteb/cqadupstack-unix
    source_notes: []
  references:
    - title: "CQADupStack: A Benchmark Data Set for Community Question-Answering Research"
      url: https://eltimster.github.io/www/pubs/adcs2015.pdf
      year: 2015
      is_paper: true
      source_confidence: definitive_paper_link
    - title: "MTEB: Massive Text Embedding Benchmark"
      url: https://arxiv.org/abs/2210.07316
      year: 2023
      is_paper: true
      source_confidence: definitive_paper_link
```
