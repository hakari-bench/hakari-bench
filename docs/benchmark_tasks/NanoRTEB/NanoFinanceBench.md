# NanoRTEB / NanoFinanceBench

## Overview

`NanoRTEB / NanoFinanceBench` retrieves financial filing evidence needed to
answer expert-written FinanceBench questions.

## Details

### What the Original Data Measures

[FinanceBench: A New Benchmark for Financial Question Answering](https://arxiv.org/abs/2311.11944)
introduces expert-written finance questions grounded in public company filings.
The benchmark emphasizes realistic analyst-style questions and evidence from
financial statements, footnotes, and management discussion.

RTEB repurposes the evidence-finding part of FinanceBench as retrieval. The
query is an analyst question, and the positive document is the excerpt needed
to answer it.

### Observed Data Profile

The split has 150 queries, 145 documents, and 150 positive qrel rows. Every
query has one positive. Queries average 161.09 characters and documents average
1,676.96 characters. The examples include cash-flow statements, balance sheets,
segment tables, and explanatory filing excerpts.

### BM25 Difficulty

Using the dataset-provided BM25 candidate column, BM25 reaches nDCG@10 =
0.3165 and hit@10 = 0.5067. It ranks 25 positives at rank 1 and 76 in the top
10.

BM25 can match company names, fiscal years, and table labels, but many
questions require finding the right financial table among similar filing
sections. Numeric reasoning and table context matter even before answer
generation.

### Training Data That May Help

Useful data includes financial QA evidence retrieval, annual-report table
retrieval, SEC filing search, and hard negatives from the same company and year
but different statement sections.

### Synthetic Data Guidance

Generate analyst questions from real non-evaluation filings and attach the
exact table or excerpt that supports the computation. Include distractors from
the same filing with overlapping years and metrics. Avoid answer-only examples
that omit the evidence span.

## Example Data

| Query | Positive document |
| --- | --- |
| What Was AMCOR's Adjusted Non GAAP EBITDA for FY 2023 (53 chars) | Twelve Months Ended June 30, 2022 Twelve Months Ended June 30, 2023 ($ million) EBITDA EBIT Net Income EPS (Diluted US cents)(1) EBITDA EBIT Net Income EPS (Diluted US cents)(1) Net income attributable to Amcor 805 805 805 52 ... [truncated 225 chars](1049 chars) |
| Which debt securities are registered to trade on a national securities exchange under 3M's name as of Q2 of 2023? (113 chars) | Title of each class Trading Symbol(s) Name of each exchange on which registered Common Stock, Par Value $.01 Per Share MMM New York Stock Exchange MMM Chicago Stock Exchange, Inc. 1.500% Notes due 2026 MMM26 New York Stock Ex ... [truncated 225 chars](335 chars) |
| Based on the information provided primarily in the balance sheet and the statement of income, what is FY2020 days payable outstanding (DPO) for Corning? DPO is defined as: 365 * (average accounts payable between FY2019 and FY ... [truncated 225 chars](336 chars) | Index Consolidated Statements of Income Corning Incorporated and Subsidiary Companies Year ended December 31, (In millions, except per share amounts) 2020 2019 2018 Net sales $ 11,303 $ 11,503 $ 11,290 Cost of sales 7,772 7,4 ... [truncated 225 chars](4015 chars) |
| Does Boeing have an improving gross margin profile as of FY2022? If gross margin is not a useful metric for a company like this, then state that and explain why. (161 chars) | The Boeing Company and Subsidiaries Consolidated Statements of Operations (Dollars in millions, except per share data) Years ended December 31, 2022 2021 2020 Sales of products $55,893 $51,386 $47,142 Sales of services 10,715 ... [truncated 225 chars](479 chars) |
| What is the FY2019 - FY2020 total revenue growth rate for Block (formerly known as Square)? Answer in units of percents and round to one decimal place. Approach the question asked by assuming the standpoint of an investment b ... [truncated 225 chars](287 chars) | SQUARE, INC. CONSOLIDATED STATEMENTS OF OPERATIONS (In thousands, except per share data) Year Ended December 31, 2020 2019 2018 Revenue: Transaction-based revenue $ 3,294,978 $ 3,081,074 $ 2,471,451 Subscription and services- ... [truncated 225 chars](1779 chars) |

## Dataset Information

| Field | Value |
| --- | --- |
| Nano set | NanoRTEB |
| Backing dataset | NanoRTEB |
| Task / split | NanoFinanceBench |
| Hugging Face dataset | [hakari-bench/NanoRTEB](https://huggingface.co/datasets/hakari-bench/NanoRTEB) |
| Source dataset | [virattt/financebench](https://huggingface.co/datasets/virattt/financebench) |
| Language | en |
| Category | natural_language |
| Queries | 150 |
| Documents | 145 |
| Positive qrels | 150 |
| BM25 nDCG@10 | 0.4267 |
| BM25 hit@10 | 0.6533 |
| BM25 Recall@100 | 0.9467 |
| BM25 candidate subset | top-500 (`bm25`) |
| Dense nDCG@10 | 0.7694 |
| Dense hit@10 | 0.9533 |
| Dense Recall@100 | 0.9933 |
| Dense candidate subset | top-500 (`harrier_oss_v1_270m`) |
| Reranking hybrid nDCG@10 | 0.6613 |
| Reranking hybrid hit@10 | 0.9133 |
| Reranking hybrid Recall@100 | 1.0000 |
| Reranking hybrid candidate subset | top-100 plus optional rank-101 safeguard (`reranking_hybrid`) |
| Reranking hybrid candidates / query | 100 |
| Reranking hybrid safeguard rows | 0 |
| Query length avg chars | 161.09 |
| Document length avg chars | 1,676.96 |

### Public Sources

- [FinanceBench: A New Benchmark for Financial Question Answering](https://arxiv.org/abs/2311.11944), task paper.
- [virattt/financebench](https://huggingface.co/datasets/virattt/financebench), source dataset card.
- [Introducing RTEB: A New Standard for Retrieval Evaluation](https://huggingface.co/blog/rteb), RTEB benchmark announcement.

### Hugging Face Links

- Nano dataset: [hakari-bench/NanoRTEB](https://huggingface.co/datasets/hakari-bench/NanoRTEB)
- Source task dataset: [virattt/financebench](https://huggingface.co/datasets/virattt/financebench)

### Source Reference Table

| Title | Year | Type | URL |
| --- | ---: | --- | --- |
| FinanceBench: A New Benchmark for Financial Question Answering | 2023 | task paper | https://arxiv.org/abs/2311.11944 |
| virattt/financebench |  | dataset card | https://huggingface.co/datasets/virattt/financebench |
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
  task_name: NanoFinanceBench
  split_name: NanoFinanceBench
  language: en
  category: natural_language
  document_path: docs/benchmark_tasks/NanoRTEB/NanoFinanceBench.md
  source_research:
    primary_source_type: task_paper
    paper_pdf_or_html_checked: true
    no_paper_note: null
  counts:
    queries: 150
    documents: 145
    positive_qrels: 150
  positives_per_query:
    average: 1.0
    min: 1
    median: 1.0
    max: 1
    multi_positive_queries: 0
    multi_positive_query_percent: 0.0
  text_stats_chars:
    query_mean: 161.09
    document_mean: 1676.96
  bm25:
    ndcg_at_10: 0.42671358545916066
    hit_at_10: 0.6533333333333333
    source: dataset_candidate_subset
  example_count: 5
  candidate_subsets:
    bm25:
      config: bm25
      label: BM25
      source: dataset_candidate_subset
      top_k: 500
      ndcg_at_10: 0.4267135855
      hit_at_10: 0.6533333333
      recall_at_100: 0.9466666667
      candidate_count_min: 145
      candidate_count_max: 145
      candidate_count_mean: 145.0
      query_count: 150
      query_coverage: 1.0
      relevant_coverage_at_100: 0.9466666667
    dense:
      config: harrier_oss_v1_270m
      label: Dense
      source: dataset_candidate_subset
      top_k: 500
      ndcg_at_10: 0.7693544637
      hit_at_10: 0.9533333333
      recall_at_100: 0.9933333333
      candidate_count_min: 145
      candidate_count_max: 145
      candidate_count_mean: 145.0
      query_count: 150
      query_coverage: 1.0
      relevant_coverage_at_100: 0.9933333333
    reranking_hybrid:
      config: reranking_hybrid
      label: Reranking hybrid
      source: dataset_candidate_subset
      top_k: 100
      ndcg_at_10: 0.6613433505
      hit_at_10: 0.9133333333
      recall_at_100: 1.0
      candidate_count_min: 100
      candidate_count_max: 100
      candidate_count_mean: 100.0
      query_count: 150
      query_coverage: 1.0
      relevant_coverage_at_100: 1.0
      safeguard_positive_rows: 0
      rows_with_101_candidates: 0
```
