# NanoSSRB / FinanceAndEconomics

## Overview

FinanceAndEconomics evaluates retrieval over JSON records for banking,
transactions, markets, insurance, budgets, risk, personal finance, and economic
indicators. Its 200 English queries search 10,000 documents with 601 positive
qrels. Requests frequently combine currencies, amounts, dates, account or asset
types, geographic conditions, and qualitative risk or purpose descriptions.
The main difficulty is precise conjunction: a transaction can share the right
currency and topic yet fail an amount threshold or beneficiary condition.

## Details

### What the Original Data Measures

The [SSRB paper](https://papers.neurips.cc/paper_files/paper/2025/hash/631bbd89466337712564872840a401be-Abstract-Datasets_and_Benchmarks_Track.html)
tests neural retrieval as a direct interface to semi-structured collections.
This domain emphasizes numerical and logical semantics that keyword search
cannot reliably enforce.

### Observed Data Profile

Queries average 314 characters and documents 556 characters, with about three
positives per query. Examples combine budgets, portfolio composition, crypto
amounts, suspicious-transfer intent, or economic conditions with hard filters.

### BM25 Evaluation Profile

BM25 reaches 0.1532 nDCG@10, 0.3950 hit@10, and 0.5524 Recall@100. Currency,
ticker, account, and transaction vocabulary helps, but token overlap does not
perform numerical comparison or reliably infer financial intent.

### Dense Evaluation Profile

Dense retrieval reaches 0.2795 nDCG@10, 0.6200 hit@10, and 0.6972 Recall@100.
It better captures risk and purpose paraphrases, while exact amounts, bounds,
and currencies remain frequent failure points.

### Reranking Hybrid Evaluation Profile

Hybrid reaches 0.2791 nDCG@10, 0.6350 hit@10, and 0.6889 Recall@100. It slightly
improves hit rate but does not recover every dense candidate, showing that both
candidate coverage and constraint-aware ordering remain open problems.

### Metric Interpretation for Model Researchers

This is the lowest-recall NanoSSRB domain, so Recall@100 is as important as
nDCG@10. A reranker cannot repair a missing qualifying transaction. Dense gains
show value from semantic intent, but high scores require reliable comparison of
numbers, dates, currencies, and nested financial attributes.

### Query and Relevance Type Tendencies

Queries include threshold search, temporal windows, portfolio suitability,
beneficiary or geography filters, and risk interpretation. Relevant records
must satisfy hard financial constraints and the softer requested rationale.

### Representative Failure Modes

Common errors include reversing greater-than and less-than, confusing account
and transaction currencies, ignoring a date window, or matching generic risk
language without the requested asset allocation. Near-identical records with
one wrong numeric field are strong hard negatives.

### Finance-Specific Notes

Amounts, percentages, currency codes, timestamps, and negative conditions must
remain distinct. Models should connect aliases such as ETH/Ethereum while not
conflating units or treating all large-number mentions as equivalent.

### Training and Leakage Notes

Exclude evaluation objects and SSRB test derivatives; disclose SSRB exposure.
Synthetic financial data should not copy real personal identifiers or seed from
the benchmark's positive records.

### Model Improvement Hints

Combine field-aware embeddings with explicit numeric/date features and
constraint-level reranking. Train on counterfactual negatives that change one
amount, currency, period, beneficiary, or risk attribute.

### Training Data That May Help

Non-overlapping transaction search, filing evidence, market-data catalogs, and
financial QA retrieval pairs can teach terminology and constraint grounding.

### Synthetic Data Guidance

Create independent ledger, budget, portfolio, insurance, and indicator schemas;
generate answerable requests and single-constraint near misses without using
evaluation queries or positives.

### Public Sources

- [SSRB: Direct Natural Language Querying to Massive Heterogeneous Semi-Structured Data](https://papers.neurips.cc/paper_files/paper/2025/hash/631bbd89466337712564872840a401be-Abstract-Datasets_and_Benchmarks_Track.html), 2025.
- [vec-ai/struct-ir](https://huggingface.co/datasets/vec-ai/struct-ir).

### Hugging Face Links

- Nano dataset: [hakari-bench/NanoSSRB](https://huggingface.co/datasets/hakari-bench/NanoSSRB)
- Source dataset: [vec-ai/struct-ir](https://huggingface.co/datasets/vec-ai/struct-ir)

### Source Reference Table

| Title | Year | Type | URL |
| --- | ---: | --- | --- |
| SSRB: Direct Natural Language Querying to Massive Heterogeneous Semi-Structured Data | 2025 | benchmark paper | [NeurIPS](https://papers.neurips.cc/paper_files/paper/2025/hash/631bbd89466337712564872840a401be-Abstract-Datasets_and_Benchmarks_Track.html) |
| vec-ai/struct-ir | 2025 | source dataset | [Hugging Face](https://huggingface.co/datasets/vec-ai/struct-ir) |

## Example Data

| Query | Positive document |
| --- | --- |
| I'm looking for a user profile with a monthly budget over $3000 and who is actively saving for a down payment on a house. I'd prefer someone relatively young, say under 40, and who seems to prioritize long-term financial health, meaning they have an investment portfolio, but not one heavily focused on very high-risk investments. Also, I need expense categories that include both essential and discretionary spending. [[The current time is 2024-01-01]] [455 chars] | { "user_profile": { "name": "Alice Johnson", "age": 32, "contact_info": "alice.johnson@email.com" }, "monthly_budget": 3500.0, "expense_categories": [ "rent", "groceries", "utilities", "transportation", "entertainment", "savings" ], "savings_goal": 50000.0, "investment_portfolio": { "stocks": 0.4, "bonds": 0.5, "mutual_funds": 0.1, "crypto": 0.0 }, "financial_advice": "Focus on high-yield savings accounts and low-risk bond investments to preserve capital for your down payment goal." } [629 chars] |
| I'm investigating a potentially large Ethereum transaction to a known wallet address. I need to find all transactions on the Ethereum blockchain with a transaction amount greater than 100 ETH. [192 chars] | { "crypto_symbol": "ETH", "blockchain_network": "Ethereum", "transaction_hash": "0x1b8b4e3e5f7a21b694d8a185d319275360d1476c34b7418b49c51f8e923a519a", "transaction_date": "2023-05-20T08:00:00Z", "wallet_address": "0x00000000219ab540356cbb839cbe05303d7705fa", "transaction_amount": 1000.0, "smart_contract_details": { "contract_name": "Large Exchange Wallet", "contract_address": "0xdef1234567890123456789012345678901234567" }, "miners_fee": 1.2 } [497 chars] |
| Find transactions made in US dollars with a substantial amount, specifically those that seem like they might be related to international transfers or payments – perhaps larger than usual personal expenses. [205 chars] | { "account_number": "9876543210", "transaction_id": "TXN123456789", "transaction_type": "withdrawal", "transaction_date": "2024-01-20T14:30:00Z", "transaction_amount": 650.0, "transaction_currency": "USD", "beneficiary_details": { "name": "Global Payments Inc.", "location": "Cayman Islands", "description": "Overseas transfer - suspicious activity" } } [409 chars] |
