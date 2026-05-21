# NanoCoIR / NanoCodeFeedbackMT

## Overview

CoIR turns OpenCodeInterpreter-style feedback conversations into a multi-turn
retrieval problem: the query is a long programming dialogue with instructions,
code, feedback, and intermediate assistant turns, and the target is the final
assistant response. The task tests whether a retriever can preserve dialogue
state and repair intent across several turns, not merely match a standalone
programming question to an answer.

## Details

### What the Original Data Measures

[CoIR](https://arxiv.org/abs/2407.02883) defines CodeFeedback-MT as a hybrid
code retrieval task where a model must use multi-turn dialogue context to
retrieve the final assistant reply. The [OpenCodeInterpreter paper](https://arxiv.org/abs/2402.14658)
describes Code-Feedback as a 68K multi-turn interaction dataset with execution
feedback and human-style feedback for iterative code refinement. CoIR adapts
that data by taking the initial dialogue history as the query and the final
assistant response as the corpus item.

### Observed Data Profile

The Nano split has 200 queries, 10,000 documents, and 200 positive qrels. Each
query has one positive. Queries are very long, averaging 4,468.62 characters,
because they contain dialogue history, instructions, code, and intermediate
assistant responses. Documents average 1,468.16 characters and often contain
explanatory prose plus code.

### BM25 Difficulty

Using the dataset-provided BM25 candidate column, BM25 reaches nDCG@10 =
0.7311 and hit@10 = 0.8050. It ranks 132 positives first and 161 positives in
the top 10. Exact overlap is strong for many examples because the target reply
shares terms with the dialogue context, but long histories can also pull BM25
toward irrelevant programming concepts.

### Training Data That May Help

Useful training data includes multi-turn coding conversations, execution-error
repair traces, assistant-response retrieval data, and hard negatives from
nearby turns in the same conversation family.

### Synthetic Data Guidance

Synthetic data should preserve long dialogue histories and retrieve the next
assistant response, not just a standalone answer. Include hard negatives that
answer earlier turns or similar tasks so the model must track dialogue state.

## Example Data

| Query | Positive document |
| --- | --- |
| 'user': Write a SQL query to list customers who have placed orders for more than $100 in the past month and have made at least 3 orders. Additionally, the query should exclude customers who have placed orders for less than $5 ... [truncated 225 chars](3249 chars) | To adhere to standard SQL formatting, keywords are written in uppercase, while database, table, and column names in lowercase. Indentation is used to show the structure of SQL statements clearly, and each sub-clause should be ... [truncated 225 chars](2115 chars) |
| 'user': Design a programming function that integrates underscores in place of spaces that separate words ending with punctuation symbols in a provided text string. This function should be proficient at handling multiple punct ... [truncated 225 chars](2357 chars) | The function `underscore_punctuation` has been successfully defined without any syntactical errors. Now we can use this function to replace spaces with underscores in string words, ending with punctuation, while preserving sp ... [truncated 225 chars](557 chars) |
| 'user': A divisor $d$ of a number $n$ is deemed unitary if it possesses the characteristic $\gcd(d, n/d) = 1$. For instance, the unitary divisors of $4! = 24$ are $1, 3, 8$ and $24$, and the summation of their squares is $1^2 ... [truncated 225 chars](7649 chars) | I apologize for any confusion caused earlier. Calculating $S(100,000,000!)$ directly is not feasible due to the size of the numbers involved. In mathematics, problems like this often require a deep understanding of number the ... [truncated 225 chars](777 chars) |
| 'user': Write a detailed explanation of the Model-View-Controller (MVC) architecture pattern and its implementation in Django, including how it handles form validation and database transactions. In addition, discuss the conce ... [truncated 225 chars](11785 chars) | Apologies for the confusion, but as an AI, I can't execute Django code. However, I can indeed enhance the middleware code with comments and improved formatting for better readability: For the threading example: ```python impo ... [truncated 225 chars](2136 chars) |
| 'user': Write a Python code that takes a Unix timestamp as input, converts it to date and time, and retrieves specific elements from the converted date. Then, evaluate if the year derived from this timestamp is a leap year or ... [truncated 225 chars](3514 chars) | The provided Unix timestamp, 1594102055, has been successfully converted into a date and time. The year extracted from this conversion was 2020, and based on that, the program has returned the message that 2020 is indeed a le ... [truncated 225 chars](429 chars) |

## Dataset Information

| Field | Value |
| --- | --- |
| Nano set | NanoCoIR |
| Backing dataset | NanoCoIR |
| Task / split | NanoCodeFeedbackMT |
| Hugging Face dataset | [hakari-bench/NanoCoIR](https://huggingface.co/datasets/hakari-bench/NanoCoIR) |
| Language | en |
| Category | code |
| Queries | 200 |
| Documents | 10000 |
| Positive qrels | 200 |
| BM25 nDCG@10 | 0.7311 |
| BM25 hit@10 | 0.8050 |
| Query length avg chars | 4468.62 |
| Document length avg chars | 1468.16 |

### Public Sources

- [CoIR](https://arxiv.org/abs/2407.02883); 2025; Xiangyang Li et al.
- [OpenCodeInterpreter](https://arxiv.org/abs/2402.14658); 2024; Tianyu Zheng et al.

### Hugging Face Links

- Nano dataset: [hakari-bench/NanoCoIR](https://huggingface.co/datasets/hakari-bench/NanoCoIR)
- Source dataset: [m-a-p/Code-Feedback](https://huggingface.co/datasets/m-a-p/Code-Feedback)

### Source Reference Table

| Title | Year | Type | URL |
| --- | ---: | --- | --- |
| CoIR: A Comprehensive Benchmark for Code Information Retrieval Models | 2025 | benchmark paper | https://arxiv.org/abs/2407.02883 |
| OpenCodeInterpreter: Integrating Code Generation with Execution and Refinement | 2024 | source task paper | https://arxiv.org/abs/2402.14658 |

## Machine-Readable Metadata

<!-- benchmark-task-metadata:v1 -->

```yaml
benchmark_task_metadata:
  schema_version: 1
  document_status: first_pass
  nano_set: NanoCoIR
  backing_dataset: NanoCoIR
  dataset_id: hakari-bench/NanoCoIR
  task_name: NanoCodeFeedbackMT
  split_name: NanoCodeFeedbackMT
  language: en
  category: code
  document_path: docs/benchmark_tasks/NanoCoIR/NanoCodeFeedbackMT.md
  source_research:
    primary_source_type: benchmark_paper_and_task_paper
    paper_pdf_or_html_checked: true
    no_paper_note: null
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
    query_mean: 4468.625
    document_mean: 1468.1565
  bm25:
    ndcg_at_10: 0.7311458867470343
    hit_at_10: 0.805
    source: dataset_bm25_column
  learning:
    original_train_split: available
    evaluation_split_origin: CoIR CodeFeedback-MT test-derived retrieval split
    train_eval_overlap_audit: not_audited
    leakage_note: exclude NanoCodeFeedbackMT dialogue histories and final responses
    useful_training_data:
      - multi-turn code assistant conversations
      - execution-feedback repair traces
      - hard negatives from adjacent code-feedback turns
    synthetic_data:
      document_generation: final assistant responses with prose and code
      question_generation: multi-turn coding dialogue histories
      answerability: positive response must be the next relevant assistant turn
    multi_positive_training: single_positive
  links:
    nano_dataset: https://huggingface.co/datasets/hakari-bench/NanoCoIR
    source_urls:
      - label: CoIR arXiv
        url: https://arxiv.org/abs/2407.02883
      - label: OpenCodeInterpreter arXiv
        url: https://arxiv.org/abs/2402.14658
      - label: m-a-p/Code-Feedback
        url: https://huggingface.co/datasets/m-a-p/Code-Feedback
    source_notes: []
  references:
    - title: "CoIR: A Comprehensive Benchmark for Code Information Retrieval Models"
      url: https://arxiv.org/abs/2407.02883
      year: 2025
      is_paper: true
      source_confidence: definitive_paper_link
    - title: "OpenCodeInterpreter: Integrating Code Generation with Execution and Refinement"
      url: https://arxiv.org/abs/2402.14658
      year: 2024
      is_paper: true
      source_confidence: definitive_paper_link
```
