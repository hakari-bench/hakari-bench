# NanoIFIR / NanoIFIRFiQA

## Overview

`NanoIFIRFiQA` is an English personal-finance instruction-following retrieval task in NanoIFIR. The queries are financial questions, and the documents are answer posts or advice passages that may help with the user's decision.

This task evaluates financial advice retrieval rather than fact lookup. Relevant documents often contain practical caveats, decision factors, and user-specific considerations, so the model must match the financial intent behind the question rather than only repeat product or tax terms.

## Details

### What the Original Data Measures

IFIR uses FiQA for the finance domain and simulates users seeking guidance for informed financial decisions. The IFIR formulation adds instruction complexity, including a basic request for financial suggestions, extra personal information such as age or financial status, and specific financial goals.

FiQA was introduced as a financial opinion mining and question answering benchmark. Its QA task asks systems to rank relevant financial posts for natural-language financial questions. In NanoIFIR, this becomes a compact retrieval task for instruction-sensitive financial advice.

### Observed Data Profile

This Nano split contains 200 queries, 10,000 documents, and 1,010 positive qrels. Every query is multi-positive. Queries have 5.05 positives on average, with a minimum of 3, a median of 4.0, and a maximum of 23. Queries average 65.79 characters, and documents average 791.89 characters.

Observed questions cover dividend versus growth stocks, purchases that increase cash flow, fixed annuities, side-business structure for taxes, bank transaction access, credit cards, loans, gifts, debt, budgeting, and investment choices. Documents are informal but domain-specific financial advice posts.

### BM25 Evaluation Profile

BM25 reaches nDCG@10 of 0.3422, hit@10 of 0.7650, and recall@100 of 0.5802 with a top-500 candidate pool. Lexical matching helps when a question and answer share terms such as dividend, annuity, LLC, tax, loan, or credit card.

BM25 is limited when the answer is relevant through financial reasoning rather than exact wording. Advice posts may discuss risk, goals, liquidity, cash flow, or opportunity cost without repeating the user's phrasing. BM25 can also over-rank same-product posts that answer a different decision problem.

### Dense Evaluation Profile

The dense harrier-oss-270m profile reaches nDCG@10 of 0.5328, hit@10 of 0.8750, and recall@100 of 0.7614. Dense retrieval is clearly strongest across the main metrics.

This pattern fits personal-finance QA. Embedding similarity can connect a short question to advice that uses different vocabulary but addresses the same decision. Dense retrieval also helps identify answers with practical caveats, tradeoffs, or goal-specific reasoning.

### Reranking Hybrid Evaluation Profile

The reranking_hybrid candidate subset reaches nDCG@10 of 0.4678, hit@10 of 0.8750, and recall@100 of 0.7455. It uses 100 candidates per query, with three rank-101 safeguard positives.

Hybrid retrieval is strong but below dense retrieval on nDCG@10 and recall@100. It matches dense hit@10, suggesting that exact finance terminology still helps ensure at least one relevant answer appears near the top. For reranking, hybrid is useful, but dense retrieval is the stronger first-stage signal.

### Metric Interpretation for Model Researchers

`NanoIFIRFiQA` is a dense-favored financial advice retrieval task. The gap between dense and BM25 shows that semantic decision matching is more important than keyword overlap alone.

Because every query has multiple positives, recall@100 matters. A good model should retrieve several useful answers, not only one. nDCG@10 reflects whether the most useful financial advice appears early enough for a user or downstream assistant.

### Query and Relevance Type Tendencies

Queries are short English financial questions. Some ask about products, while others ask about planning, taxes, cash flow, business structure, debt, or investment strategy. Documents are longer answer posts with examples, qualifications, and practical reasoning.

The relevance relation is advice usefulness. A positive document should address the user's financial decision, even if it does not provide a single definitive answer.

### Representative Failure Modes

BM25 may retrieve posts with the same product name but the wrong financial goal. Dense retrieval may retrieve generally related advice that misses a constraint such as age, tax status, risk tolerance, or business structure. Hybrid retrieval can still rank broad topical matches above answers that directly address the decision.

Another common failure is ignoring caveats. Finance advice often depends on personal circumstances, so a topically similar answer may be inappropriate for the user's specific question.

### Training Data That May Help

Useful training data includes non-overlapping FiQA question-document pairs, personal finance forum QA, financial advice retrieval pairs, and same-topic hard negatives about the same product, tax topic, or investment choice.

Training should preserve multiple relevant answers per query and exclude `NanoIFIRFiQA` queries, qrels, and positive financial answer posts.

### Model Improvement Notes

Improving this task requires modeling decision intent, constraints, and advice quality. Models should represent financial goals, risk, time horizon, tax considerations, debt context, and product characteristics.

For reranking, the most valuable behavior is distinguishing advice that answers the user's decision from advice that merely discusses the same financial instrument.

## Example Data

### Public Sources

This task is documented through the IFIR paper and the FiQA financial opinion mining and question answering paper. The Nano split is published in `hakari-bench/NanoIFIR`.

### Source Reference Table

| Source | Role |
| --- | --- |
| [IFIR: A Comprehensive Benchmark for Evaluating Instruction-Following in Expert-Domain Information Retrieval](https://arxiv.org/abs/2503.04644) | Expert-domain instruction-following IR benchmark paper. |
| [WWW'18 Open Challenge: Financial Opinion Mining and Question Answering](https://doi.org/10.1145/3184558.3192301) | Original FiQA financial QA task paper. |
| [hakari-bench/NanoIFIR](https://huggingface.co/datasets/hakari-bench/NanoIFIR) | Nano benchmark dataset containing this split. |

### Representative Snippets

| Query Pattern | Positive Document Pattern |
| --- | --- |
| A question comparing dividend and growth stocks for young investors. | An advice post explaining total return, dividend yield, capital growth, and investment tradeoffs. |
| A question asking what purchases other than real estate can increase cash flow. | An answer discussing increasing income, decreasing expenses, and monthly cash-flow mechanics. |
| A question asking what fixed annuities contain. | A post explaining annuities as contracts and discussing issuer obligations. |
| A question about full-time work plus a side business and the best tax structure. | An answer recommending or discussing an LLC, pass-through income, deductions, and liability protection. |
| A question asking why banks do not expose all transaction activity. | A post explaining legacy banking systems, technology constraints, and institutional history. |
