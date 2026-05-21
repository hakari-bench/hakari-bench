# NanoRTEB / NanoHC3Finance

## Overview

`NanoRTEB / NanoHC3Finance` retrieves finance-domain answer passages for short
personal-finance or investing prompts adapted from HC3.

## Details

### What the Original Data Measures

[How Close is ChatGPT to Human Experts? Comparison Corpus, Evaluation, and
Detection](https://arxiv.org/abs/2301.07597) introduces HC3, a corpus comparing
human expert and ChatGPT answers across open-domain, financial, medical, legal,
and psychological questions. RTEB uses the finance portion as a retrieval task:
the user question is the query and the relevant answer/explanation is the
document.

[Introducing RTEB: A New Standard for Retrieval Evaluation](https://huggingface.co/blog/rteb)
describes HC3Finance as an open finance dataset sourced from HC3 and included
to cover practical domain retrieval.

### Observed Data Profile

The split has 200 queries, 415 documents, and 200 positive qrel rows. Each query
has one positive. Queries are short, averaging 61.41 characters, while answer
documents average 991.30 characters. The examples look like personal-finance
forum questions and explanatory answers.

### BM25 Difficulty

Using the dataset-provided BM25 candidate column, BM25 reaches nDCG@10 =
0.2708 and hit@10 = 0.4100. It ranks 32 positives at rank 1 and 82 in the top
10.

Short queries such as "Starting off as an investor" contain little lexical
signal, so BM25 often retrieves a plausible finance answer before the specific
paired response. Semantic matching of intent and advice type matters.

### Training Data That May Help

Useful data includes personal-finance QA, StackExchange-style finance retrieval,
financial advice answer ranking, and hard negatives from answers about nearby
topics such as budgeting, investing, taxes, and credit.

### Synthetic Data Guidance

Generate short finance prompts and pair them with full explanatory answers.
Include ambiguous prompts and same-topic hard negatives. Avoid making all
queries keyword-rich; the benchmark includes terse user questions.

## Example Data

| Query | Positive document |
| --- | --- |
| Is socialtrend.com or/and feelthetrend.com legitimate? (54 chars) | It's called a "Pyramid scheme". Its illegal in almost every country of the Western world. You're not going to earn lifetime income, of course, and these things collapse pretty quickly. Most of the "common folks" don't return ... [truncated 225 chars](989 chars) |
| How to read Google Finance data on dividends (44 chars) | However, you have to remember that not all dividends are paid quarterly. For example one stock I recently purchased has a price of $8.03 and the Div/yield = 0.08/11.9 . $.08 * 4 = $0.32 which is only 3.9% (But this stock pays ... [truncated 225 chars](392 chars) |
| What is a good way to keep track of your credit card transactions, to reduce likelihood of fraud? (97 chars) | Read your bill, question things that don't look familiar. People who steal credit card numbers don't bother to conceal themselves well. So if you live in Florida, and all of the sudden charges appear in Idaho, you should inve ... [truncated 225 chars](725 chars) |
| When Employees are “Granted” Stock Options, is the Company encouraging Long-Term investments from them? (103 chars) | There are two things to consider: taxes - beneficial treatment for long-term holding, and for ESPP's you can get lower taxes on higher earnings. Also, depending on local laws, some share schemes allow one to avoid some or all ... [truncated 225 chars](931 chars) |
| Does lender care what I use the money for? (42 chars) | When you borrow from a bank, there are secured loans, as with a mortgage, or unsecured lines of credit, usually a more reasonable amount of money, but also based on income. You just asked about a private loan. It depends on t ... [truncated 225 chars](429 chars) |

## Dataset Information

| Field | Value |
| --- | --- |
| Nano set | NanoRTEB |
| Backing dataset | NanoRTEB |
| Task / split | NanoHC3Finance |
| Hugging Face dataset | [hakari-bench/NanoRTEB](https://huggingface.co/datasets/hakari-bench/NanoRTEB) |
| Source dataset | [Hello-SimpleAI/HC3](https://huggingface.co/datasets/Hello-SimpleAI/HC3) |
| Language | en |
| Category | natural_language |
| Queries | 200 |
| Documents | 415 |
| Positive qrels | 200 |
| BM25 nDCG@10 | 0.2708 |
| BM25 hit@10 | 0.4100 |
| Query length avg chars | 61.41 |
| Document length avg chars | 991.30 |

### Public Sources

- [How Close is ChatGPT to Human Experts? Comparison Corpus, Evaluation, and Detection](https://arxiv.org/abs/2301.07597), HC3 paper.
- [Hello-SimpleAI/HC3](https://huggingface.co/datasets/Hello-SimpleAI/HC3), source dataset card.
- [Introducing RTEB: A New Standard for Retrieval Evaluation](https://huggingface.co/blog/rteb), RTEB benchmark announcement.

### Hugging Face Links

- Nano dataset: [hakari-bench/NanoRTEB](https://huggingface.co/datasets/hakari-bench/NanoRTEB)
- Source task dataset: [Hello-SimpleAI/HC3](https://huggingface.co/datasets/Hello-SimpleAI/HC3)

### Source Reference Table

| Title | Year | Type | URL |
| --- | ---: | --- | --- |
| How Close is ChatGPT to Human Experts? Comparison Corpus, Evaluation, and Detection | 2023 | task paper | https://arxiv.org/abs/2301.07597 |
| Hello-SimpleAI/HC3 |  | dataset card | https://huggingface.co/datasets/Hello-SimpleAI/HC3 |
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
  task_name: NanoHC3Finance
  split_name: NanoHC3Finance
  language: en
  category: natural_language
  document_path: docs/benchmark_tasks/NanoRTEB/NanoHC3Finance.md
  source_research:
    primary_source_type: task_paper
    paper_pdf_or_html_checked: true
    no_paper_note: null
  counts:
    queries: 200
    documents: 415
    positive_qrels: 200
  positives_per_query:
    average: 1.0
    min: 1
    median: 1.0
    max: 1
    multi_positive_queries: 0
    multi_positive_query_percent: 0.0
  text_stats_chars:
    query_mean: 61.41
    document_mean: 991.3
  bm25:
    ndcg_at_10: 0.2708
    hit_at_10: 0.41
    source: dataset_bm25_column
  example_count: 5
```
