# NanoCoIR / NanoCosQA

## Overview

CoIR incorporates CoSQA as a web-query-to-code retrieval task. The original
CoSQA paper pairs Bing-style natural-language search queries with Python
functions from CodeSearchNet, annotated for whether the code satisfies the
search intent. In this split, very short and sometimes ungrammatical user search
phrases must retrieve the relevant function, so the task stresses intent
recovery from sparse wording rather than long-form problem understanding.

## Details

### What the Original Data Measures

[CoIR](https://arxiv.org/abs/2407.02883) uses CoSQA for web query code
retrieval: natural-language web queries retrieve Python code snippets from a
candidate code corpus. [CoSQA](https://arxiv.org/abs/2105.13239) introduces
20,604 labels for web-query and Python-function pairs, with each pair annotated
by at least three human annotators. The CoSQA paper states that the queries come
from Microsoft Bing search logs and that the code comes from complete Python
functions with documentation from CodeSearchNet.

### Observed Data Profile

The Nano split has 200 queries, 6,267 documents, and 200 positive qrels. Each
query has one positive. Queries are very short, averaging 36.10 characters, and
look like real search phrases with typos or incomplete grammar. Documents
average 307.61 characters and are compact Python functions with docstrings.

### BM25 Difficulty

Using the dataset-provided BM25 candidate column, BM25 reaches nDCG@10 =
0.3574 and hit@10 = 0.5200. It ranks 44 positives first, and the median best
positive rank is 10. Short queries make lexical evidence sparse, and many
positives require mapping colloquial web wording to function intent.

### Training Data That May Help

Useful data includes CoSQA-style query-code pairs, CodeSearchNet Python
functions with docstrings, search-log style paraphrases, and hard negatives with
nearby Python utility names.

### Synthetic Data Guidance

Synthetic queries should be short, messy, and search-like rather than polished
requirements. Positives should be executable or plausible Python utility
functions, with negatives that share common words such as `date`, `list`, or
`numpy` but implement a different operation.

## Example Data

| Query | Positive document |
| --- | --- |
| token to id python (18 chars) | def strids2ids(tokens: Iterable[str]) -> List[int]: """ Returns sequence of integer ids given a sequence of string ids. :param tokens: List of integer tokens. :return: List of word ids. """ return list(map(int, tokens)) (244 chars) |
| python 3 tkinter open file dialog (33 chars) | def askopenfilename(**kwargs): """Return file name(s) from Tkinter's file open dialog.""" try: from Tkinter import Tk import tkFileDialog as filedialog except ImportError: from tkinter import Tk, filedialog root = Tk() root.w ... [truncated 225 chars](389 chars) |
| python calc page align (22 chars) | def page_align_content_length(length): # type: (int) -> int """Compute page boundary alignment :param int length: content length :rtype: int :return: aligned byte boundary """ mod = length % _PAGEBLOB_BOUNDARY if mod != 0: re ... [truncated 225 chars](323 chars) |
| how to separate list elements by white space python (51 chars) | def split_strings_in_list_retain_spaces(orig_list): """ Function to split every line in a list, and retain spaces for a rejoin :param orig_list: Original list :return: A List with split lines """ temp_list = list() for line i ... [truncated 225 chars](381 chars) |
| python how to change file extension (35 chars) | def lower_ext(abspath): """Convert file extension to lowercase. """ fname, ext = os.path.splitext(abspath) return fname + ext.lower() (149 chars) |

## Dataset Information

| Field | Value |
| --- | --- |
| Nano set | NanoCoIR |
| Backing dataset | NanoCoIR |
| Task / split | NanoCosQA |
| Hugging Face dataset | [hakari-bench/NanoCoIR](https://huggingface.co/datasets/hakari-bench/NanoCoIR) |
| Language | en |
| Category | code |
| Queries | 200 |
| Documents | 6267 |
| Positive qrels | 200 |
| BM25 nDCG@10 | 0.3574 |
| BM25 hit@10 | 0.5200 |
| Query length avg chars | 36.10 |
| Document length avg chars | 307.61 |

### Public Sources

- [CoIR](https://arxiv.org/abs/2407.02883); 2025; Xiangyang Li et al.
- [CoSQA](https://arxiv.org/abs/2105.13239); 2021; Junjie Huang et al.

### Hugging Face Links

- Nano dataset: [hakari-bench/NanoCoIR](https://huggingface.co/datasets/hakari-bench/NanoCoIR)
- Source dataset: [CoIR-Retrieval/cosqa](https://huggingface.co/datasets/CoIR-Retrieval/cosqa)

### Source Reference Table

| Title | Year | Type | URL |
| --- | ---: | --- | --- |
| CoIR: A Comprehensive Benchmark for Code Information Retrieval Models | 2025 | benchmark paper | https://arxiv.org/abs/2407.02883 |
| CoSQA: 20,000+ Web Queries for Code Search and Question Answering | 2021 | source task paper | https://arxiv.org/abs/2105.13239 |

## Machine-Readable Metadata

<!-- benchmark-task-metadata:v1 -->

```yaml
benchmark_task_metadata:
  schema_version: 1
  document_status: first_pass
  nano_set: NanoCoIR
  backing_dataset: NanoCoIR
  dataset_id: hakari-bench/NanoCoIR
  task_name: NanoCosQA
  split_name: NanoCosQA
  language: en
  category: code
  document_path: docs/benchmark_tasks/NanoCoIR/NanoCosQA.md
  source_research:
    primary_source_type: benchmark_paper_and_task_paper
    paper_pdf_or_html_checked: true
    no_paper_note: null
  counts:
    queries: 200
    documents: 6267
    positive_qrels: 200
  positives_per_query:
    average: 1.0
    min: 1
    median: 1.0
    max: 1
    multi_positive_queries: 0
    multi_positive_query_percent: 0.0
  text_stats_chars:
    query_mean: 36.1
    document_mean: 307.6144885910324
  bm25:
    ndcg_at_10: 0.3573610255127629
    hit_at_10: 0.52
    source: dataset_bm25_column
  learning:
    original_train_split: available
    evaluation_split_origin: CoIR CoSQA test-derived retrieval split
    train_eval_overlap_audit: not_audited
    leakage_note: exclude NanoCosQA queries and positive Python functions
    useful_training_data:
      - CoSQA query-code pairs
      - CodeSearchNet Python functions and docstrings
      - search-log style code queries
    synthetic_data:
      document_generation: compact Python utility functions with docstrings
      question_generation: short web-search-style code queries
      answerability: positive function must satisfy the query intent
    multi_positive_training: single_positive
  links:
    nano_dataset: https://huggingface.co/datasets/hakari-bench/NanoCoIR
    source_urls:
      - label: CoIR arXiv
        url: https://arxiv.org/abs/2407.02883
      - label: CoSQA arXiv
        url: https://arxiv.org/abs/2105.13239
      - label: CoIR-Retrieval/cosqa
        url: https://huggingface.co/datasets/CoIR-Retrieval/cosqa
    source_notes: []
  references:
    - title: "CoIR: A Comprehensive Benchmark for Code Information Retrieval Models"
      url: https://arxiv.org/abs/2407.02883
      year: 2025
      is_paper: true
      source_confidence: definitive_paper_link
    - title: "CoSQA: 20,000+ Web Queries for Code Search and Question Answering"
      url: https://arxiv.org/abs/2105.13239
      year: 2021
      is_paper: true
      source_confidence: definitive_paper_link
```
