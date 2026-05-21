# NanoCodeRAG / NanoCodeRAGOnlineTutorials

## Overview

CodeRAG-Bench includes online tutorials as a retrieval source for
code-generation support, collecting pages from sites such as GeeksforGeeks,
W3Schools, Tutorialspoint, and Towards Data Science through ClueWeb22. In this
Nano split, short tutorial or programming-problem titles must retrieve long
articles containing prose, steps, code snippets, examples, dates, and
explanations. The retrieval problem is to connect a developer's
title-like need to the tutorial page that explains the relevant API, language
feature, algorithm, or task.

## Details

### What the Original Data Measures

[CodeRAG-Bench: Can Retrieval Augment Code Generation?](https://arxiv.org/abs/2406.14497)
collects online tutorials as one of five retrieval sources for code RAG. The
paper says these tutorials come from sites including GeeksforGeeks, W3Schools,
Tutorialspoint, and Towards Data Science, using raw HTML pages from ClueWeb22.
Each page contains code snippets and textual explanations, spanning basic
programming techniques through advanced library usage.

The paper's open retrieval analysis finds that tutorials can help some code
generation settings, especially when the tutorial is about the same programming
problem or gives detailed textual explanations. This Nano split isolates the
tutorial retrieval source itself: the correct document is the tutorial article
matching the query title or problem statement.

### Observed Data Profile

The Nano split has 200 queries, 9,997 documents, and 200 positive qrel rows.
Every query has one positive. Queries average 51.91 characters and are usually
page-title style strings such as Android screen control, Linux secure deletion,
C++ access modifiers, Python subscript printing, or GeeksforGeeks practice
problem names. Documents average 5,722.55 characters, with many long tutorial
pages that include dates, examples, code blocks, and step-by-step instructions.

The sampled documents are mostly article-like, not compact API references. They
often contain boilerplate, multiple examples, and broad explanatory context. This
means the retriever must use title and task intent while tolerating long
documents that contain many unrelated tokens.

### BM25 Difficulty

Using the dataset-provided BM25 candidate column, BM25 reaches nDCG@10 = 0.7472
and hit@10 = 0.8400. It ranks 132 positives first and finds 168 positives in the
top 10. Lexical matching is strong because titles and tutorials often share exact
phrases, framework names, and language names.

The failures show where exact matching is brittle. A query like
`java.time.LocalDate.atTime() Method Example` can be outranked by unrelated web
content, and `Map in C++ Standard Template Library (STL)` retrieves a nearby map
operator page before the overview tutorial. Short or generic titles such as
`Tryit Editor v3.7` are especially ambiguous.

### Training Data That May Help

Useful training data includes non-overlapping programming tutorial title-to-page
pairs, developer search logs, Stack Overflow question-to-tutorial citations,
documentation search data, and code-example retrieval where prose and snippets
jointly explain the solution. Training should exclude the NanoCodeRAG tutorial
evaluation queries, qrels, and positive tutorial pages.

Training should preserve long-document behavior. Models need to match the
article's central task, not just an incidental code token that appears in a long
page.

### Synthetic Data Guidance

For document-to-question generation, use non-evaluation tutorial pages and
generate title-like queries, "how to" questions, and practice-problem prompts
that the tutorial answers. Preserve language names, framework names, function
names, expected inputs, and output behavior.

For joint generation, create realistic tutorial pages with steps, examples, and
code snippets, then generate concise page-title queries for them. Hard negatives
should be tutorials from the same language or topic that solve a different task.
Do not use Nano evaluation queries or positive tutorial pages as seeds.

## Example Data

| Query | Positive document |
| --- | --- |
| How to turn Android device screen on and off programmatically? (62 chars) | This example demonstrate about How to turn Android device screen on and off programmatically. Step 1 − Create a new project in Android Studio, go to File ⇒ New Project and fill all required details to create a new project. St ... [truncated 225 chars](6654 chars) |
| Tools to Securely Delete Files from Linux - GeeksforGeeks (57 chars) | 16 Feb, 2021 Every time you delete a file from your Linux system using the shift + delete or rm command, it doesn’t actually permanently and securely delete the file from the hard disk. When you delete a file with the rm comm ... [truncated 225 chars](3940 chars) |
| Difference between Private and Protected in C++ with Example - GeeksforGeeks (76 chars) | 03 Jan, 2022 Protected Protected access modifier is similar to that of private access modifiers, the difference is that the class member declared as Protected are inaccessible outside the class but they can be accessed by any ... [truncated 225 chars](2559 chars) |
| How to print Superscript and Subscript in Python? - GeeksforGeeks (65 chars) | 24 Jan, 2021 Whenever we are working with formulas there may be a need of writing the given formula in a given format which may require subscripts or superscripts. There are several methods available to print subscripts and s ... [truncated 225 chars](2336 chars) |
| Maximum Difference \| Practice \| GeeksforGeeks (45 chars) | Given array A[] of integers, the task is to complete the function findMaxDiff which finds the maximum absolute difference between nearest left and right smaller element of every element in array.If the element is the leftmost ... [truncated 225 chars](12706 chars) |

## Dataset Information

| Field | Value |
| --- | --- |
| Nano set | NanoCodeRAG |
| Backing dataset | NanoCodeRAG |
| Task / split | NanoCodeRAGOnlineTutorials |
| Hugging Face dataset | [hakari-bench/NanoCodeRAG](https://huggingface.co/datasets/hakari-bench/NanoCodeRAG) |
| Language | en |
| Category | code |
| Queries | 200 |
| Documents | 9,997 |
| Positive qrels | 200 |
| BM25 nDCG@10 | 0.7472 |
| BM25 hit@10 | 0.8400 |
| Query length avg chars | 51.91 |
| Document length avg chars | 5,722.55 |

### Public Sources

- [CodeRAG-Bench: Can Retrieval Augment Code Generation?](https://arxiv.org/abs/2406.14497); 2025; Zora Zhiruo Wang, Akari Asai, Xinyan Velocity Yu, Frank F. Xu, Yiqing Xie, Graham Neubig, and Daniel Fried; DOI: `10.18653/v1/2025.findings-naacl.176`.
- [CodeRAG-Bench project page](https://code-rag-bench.github.io/).
- [CodeRAG-Bench GitHub repository](https://github.com/code-rag-bench/code-rag-bench).
- [code-rag-bench/online-tutorials dataset card](https://huggingface.co/datasets/code-rag-bench/online-tutorials).

### Hugging Face Links

- Nano dataset: [hakari-bench/NanoCodeRAG](https://huggingface.co/datasets/hakari-bench/NanoCodeRAG)
- Source dataset: [code-rag-bench/online-tutorials](https://huggingface.co/datasets/code-rag-bench/online-tutorials)

### Source Reference Table

| Title | Year | Type | URL |
| --- | ---: | --- | --- |
| CodeRAG-Bench: Can Retrieval Augment Code Generation? | 2025 | arXiv paper | https://arxiv.org/abs/2406.14497 |
| CodeRAG-Bench project page | 2025 | project page | https://code-rag-bench.github.io/ |
| code-rag-bench/online-tutorials | 2024 | dataset card | https://huggingface.co/datasets/code-rag-bench/online-tutorials |

## Machine-Readable Metadata

<!-- benchmark-task-metadata:v1 -->

```yaml
benchmark_task_metadata:
  schema_version: 1
  document_status: first_pass
  nano_set: NanoCodeRAG
  backing_dataset: NanoCodeRAG
  dataset_id: hakari-bench/NanoCodeRAG
  task_name: NanoCodeRAGOnlineTutorials
  split_name: NanoCodeRAGOnlineTutorials
  language: en
  category: code
  document_path: docs/benchmark_tasks/NanoCodeRAG/NanoCodeRAGOnlineTutorials.md
  source_research:
    primary_source_type: benchmark_paper
    paper_pdf_or_html_checked: true
    paper_url: https://arxiv.org/abs/2406.14497
    additional_source_urls:
      - https://aclanthology.org/2025.findings-naacl.176/
      - https://code-rag-bench.github.io/
      - https://github.com/code-rag-bench/code-rag-bench
      - https://huggingface.co/datasets/code-rag-bench/online-tutorials
  counts:
    queries: 200
    documents: 9997
    positive_qrels: 200
  positives_per_query:
    average: 1.0
    min: 1
    median: 1.0
    max: 1
    multi_positive_queries: 0
    multi_positive_query_percent: 0.0
  text_stats_chars:
    query_mean: 51.905
    document_mean: 5722.545864
  bm25:
    ndcg_at_10: 0.7471740687
    hit_at_10: 0.84
    source: dataset_bm25_column
  learning:
    original_train_split: unknown
    evaluation_split_origin: CodeRAG-Bench online tutorials retrieval source sampled into NanoCodeRAG
    train_eval_overlap_audit: not_audited
    leakage_note: exclude NanoCodeRAG tutorial queries, qrels, and positive tutorial pages
    useful_training_data:
      - non-overlapping programming tutorial title-to-page pairs
      - developer search logs over tutorials and documentation
      - Stack Overflow question-to-tutorial citation pairs
      - code example retrieval with long tutorial hard negatives
    synthetic_data:
      document_generation: realistic programming tutorials with prose, steps, code snippets, inputs, outputs, and language-specific details
      question_generation: title-like and how-to programming queries grounded in the tutorial's main task
      answerability: the selected tutorial should explain the requested API, algorithm, or programming procedure
    multi_positive_training: single_positive_question_document_focus
  links:
    nano_dataset: https://huggingface.co/datasets/hakari-bench/NanoCodeRAG
    source_urls:
      - label: CodeRAG-Bench arXiv
        url: https://arxiv.org/abs/2406.14497
      - label: CodeRAG-Bench project page
        url: https://code-rag-bench.github.io/
      - label: CodeRAG-Bench GitHub
        url: https://github.com/code-rag-bench/code-rag-bench
      - label: code-rag-bench/online-tutorials
        url: https://huggingface.co/datasets/code-rag-bench/online-tutorials
    source_notes: []
  references:
    - title: "CodeRAG-Bench: Can Retrieval Augment Code Generation?"
      url: https://arxiv.org/abs/2406.14497
      year: 2025
      doi: 10.18653/v1/2025.findings-naacl.176
      is_paper: true
      source_confidence: definitive_paper_link
```
