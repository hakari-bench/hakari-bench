# NanoRTEB / NanoFinanceBench

## Overview

`NanoFinanceBench` is an English financial filing evidence retrieval task from NanoRTEB. The query is an analyst-style finance question, and the relevant document is the filing excerpt, table, or statement section needed to answer it. Each query has one positive document among 145 candidates. Dense retrieval is clearly the strongest top-rank profile, `reranking_hybrid` reaches full recall@100, and BM25 is weaker because exact lexical overlap is not enough to identify the right filing evidence.

## Details

### What the Original Data Measures

FinanceBench was introduced as a benchmark for financial question answering grounded in public company filings. It emphasizes realistic analyst questions that require evidence from financial statements, footnotes, and management discussion.

RTEB repurposes the evidence-finding portion as retrieval. The system receives a finance question and must retrieve the exact filing excerpt needed before answer generation or numerical calculation.

### Observed Data Profile

The Nano split contains 150 queries, 145 documents, and 150 positive qrel rows. Every query has exactly one positive. Queries average 161.09 characters, while documents average 1,676.96 characters.

Example questions ask for adjusted non-GAAP EBITDA, registered debt securities, days payable outstanding, gross margin profile, and total revenue growth rate. Positive documents include cash-flow statements, balance sheets, segment tables, security listings, and explanatory filing excerpts.

### BM25 Evaluation Profile

The BM25 candidate subset uses the full 145-document pool and reaches nDCG@10 of 0.4267, hit@10 of 0.6533, and recall@100 of 0.9467. BM25 can match company names, years, table labels, and financial terms.

Its weakness is that many filing sections share similar vocabulary. A question may require a particular statement line, footnote, or table relation, and term overlap alone can retrieve the wrong section from the same company or period.

### Dense Evaluation Profile

The dense candidate subset from `harrier_oss_v1_270m` uses the full 145-document pool and reaches nDCG@10 of 0.7694, hit@10 of 0.9533, and recall@100 of 0.9933. Dense retrieval is the best top-rank profile by a large margin.

This indicates that semantic matching is highly useful for analyst-style questions. Dense retrieval can map concepts such as margin profile, debt securities, and payable outstanding to the filing excerpt that supports the calculation or assessment.

### Reranking Hybrid Evaluation Profile

The `reranking_hybrid` subset uses top-100 candidates and does not need the rank-101 safeguard. It reaches nDCG@10 of 0.6613, hit@10 of 0.9133, and recall@100 of 1.0000. Hybrid retrieval has the best recall@100 but lower nDCG@10 than dense retrieval.

The pattern suggests that sparse matching helps complete the candidate pool, while dense retrieval orders the correct filing evidence better. For reranking, hybrid is attractive because it exposes all positives by rank 100.

### Metric Interpretation for Model Researchers

With one positive per query, nDCG@10 measures early placement of the exact evidence excerpt, hit@10 measures whether it appears in the first ten candidates, and recall@100 measures reranker availability.

For `NanoFinanceBench`, dense nDCG@10 is the key first-stage signal. Recall@100 is also useful because finance rerankers may need to inspect tables and numeric context to select the final evidence.

### Query and Relevance Type Tendencies

Queries are analyst-style financial questions, often asking for a metric, comparison, rate, or interpretation from a company filing. Relevant documents are excerpts from annual or quarterly reports, often containing tables and numeric statements.

Relevance is evidence sufficiency. A document from the same company can be wrong if it does not contain the table or section needed for the requested calculation.

### Representative Failure Modes

Common failures include retrieving the right company but wrong statement section, confusing fiscal years, matching metric names without the needed calculation inputs, and overranking broad management discussion when a table is required. BM25 is vulnerable to repeated finance terminology; dense retrieval can still miss exact numeric rows.

### Training Data That May Help

Useful training data includes financial QA evidence retrieval, SEC filing search, annual-report table retrieval, analyst-question datasets, and hard negatives from the same company and year but different statement sections. Evaluation questions, filing excerpts, and qrels should be excluded.

### Model Improvement Notes

Models should represent company, period, metric, table role, and calculation intent. Hard negatives should use nearby filing sections with overlapping vocabulary. Dense retrieval is the strongest first-stage profile, while hybrid retrieval is best when maximizing reranking coverage.

## Example Data

### Public Sources

- [FinanceBench: A New Benchmark for Financial Question Answering](https://arxiv.org/abs/2311.11944), task paper.
- [virattt/financebench](https://huggingface.co/datasets/virattt/financebench), source dataset card.
- [Introducing RTEB: A New Standard for Retrieval Evaluation](https://huggingface.co/blog/rteb), benchmark article.

### Source Reference Table

| Title | Year | Type | URL |
| --- | ---: | --- | --- |
| FinanceBench: A New Benchmark for Financial Question Answering | 2023 | task paper | https://arxiv.org/abs/2311.11944 |
| virattt/financebench |  | dataset card | https://huggingface.co/datasets/virattt/financebench |
| Introducing RTEB: A New Standard for Retrieval Evaluation | 2025 | benchmark article | https://huggingface.co/blog/rteb |

### Representative Snippets

| Query | Relevant document excerpt |
| --- | --- |
| What was AMCOR's adjusted non-GAAP EBITDA for FY 2023? | A reconciliation table listing EBITDA, EBIT, net income, and EPS. |
| Which debt securities are registered to trade on a national securities exchange under 3M's name? | A securities listing table with trading symbols and exchanges. |
| What is Corning's FY2020 days payable outstanding using balance sheet and income statement information? | Consolidated statements of income and related financial data. |
| Does Boeing have an improving gross margin profile as of FY2022? | A consolidated statement of operations with sales and cost figures. |
| What is Block's FY2019 to FY2020 total revenue growth rate? | A consolidated statement of operations listing revenue by year. |
