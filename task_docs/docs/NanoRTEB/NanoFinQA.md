# NanoRTEB / NanoFinQA

## Overview

`NanoFinQA` is an English financial evidence retrieval task from NanoRTEB. The query is a short financial question, and the relevant document is the report excerpt or table context needed for numerical reasoning. Each query has one positive document among 380 candidates. This split is unusual because BM25 is the strongest or nearly strongest profile: finance questions often contain exact metric names, years, and company-specific terms. `reranking_hybrid` closely follows BM25, while dense retrieval is weaker on top-rank quality.

## Details

### What the Original Data Measures

FinQA was introduced as a dataset for numerical reasoning over financial data. The original benchmark uses expert-authored questions over company reports, evidence, and executable reasoning programs.

RTEB uses the evidence retrieval component. A system must retrieve the financial table or report passage that supports the question before any numerical reasoning can happen.

### Observed Data Profile

The Nano split contains 200 queries, 380 documents, and 200 positive qrel rows. Every query has exactly one positive. Queries average 101.45 characters, while documents average 3,918.54 characters.

Example questions ask about differences between high and low sales prices, total impairment costs across years, current recourse debt as a percentage of total recourse debt, average operating profit over several years, and future estimated cash payments due in a specific year.

### BM25 Evaluation Profile

The BM25 candidate subset uses the full 380-document pool and reaches nDCG@10 of 0.7330, hit@10 of 0.9250, and recall@100 of 1.0000. BM25 is very strong for this task.

The strength comes from query terms such as financial metrics, years, company names, debt categories, and accounting phrases. These tokens often appear directly in the relevant report excerpt or table. The remaining challenge is choosing the right section when many filings share similar finance vocabulary.

### Dense Evaluation Profile

The dense candidate subset from `harrier_oss_v1_270m` uses the full 380-document pool and reaches nDCG@10 of 0.6051, hit@10 of 0.7600, and recall@100 of 0.9700. Dense retrieval is substantially weaker than BM25 on early rank quality.

This suggests that exact lexical anchoring is more useful than broad semantic similarity for this split. Dense embeddings may connect related financial concepts, but they can underweight precise years, line-item names, and table labels.

### Reranking Hybrid Evaluation Profile

The `reranking_hybrid` subset uses top-100 candidates and does not need the rank-101 safeguard. It reaches nDCG@10 of 0.7309, hit@10 of 0.8900, and recall@100 of 1.0000. Hybrid retrieval nearly matches BM25 on nDCG@10 and has saturated recall@100.

The hybrid result shows that sparse lexical matching remains the dominant signal, while dense retrieval can add some robustness. For reranking, both BM25 and hybrid pools provide full recall at rank 100.

### Metric Interpretation for Model Researchers

With one positive per query, nDCG@10 measures how early the supporting report excerpt appears, hit@10 measures whether it appears in the first ten candidates, and recall@100 measures reranker availability.

For `NanoFinQA`, recall@100 is saturated for BM25 and hybrid retrieval, so improvements should focus on ranking the correct evidence first. Preserving exact numeric and temporal terms is critical.

### Query and Relevance Type Tendencies

Queries are short finance questions that often name a metric, period, company, or calculation target. Relevant documents are long excerpts from financial reports, frequently containing tables or dense numeric context.

Relevance is evidence sufficiency for the calculation. A passage about the same company or year is wrong if it does not contain the numbers needed for the question.

### Representative Failure Modes

Common failures include retrieving a same-company section with the wrong metric, confusing adjacent years, overranking passages with common accounting terms, and missing table rows that contain the decisive number. BM25 can still be misled by repeated finance vocabulary; dense retrieval can blur precise line items.

### Training Data That May Help

Useful training data includes financial report evidence retrieval, SEC filing search, table question answering with supporting evidence, and hard negatives sharing company, year, or metric names. Evaluation questions, report excerpts, and qrels should be excluded.

### Model Improvement Notes

Models should retain exact numbers, dates, company names, and financial line-item labels in their representations. Hard negatives should use the same company and period but different accounting fields. Sparse and hybrid retrieval are strong foundations for this split because exact terminology matters.

## Example Data

| Query | Positive document |
| --- | --- |
| what was the difference in the companies high compared to its low sales price for the second quarter of 2001? [109 chars] | part ii item 5 2014market for registrant 2019s common equity and related stockholder matters ( a ) market information . the common stock of the company is currently traded on the new york stock exchange ( nyse ) under the symbol 2018 2018aes 2019 2019 . the following tables set forth the high and low sale prices for the common stock as reported by the nyse for the periods indicated . price range of common stock .[['2001 first quarter', 'high $ 60.15', 'low $ 41.30', '2000 first quarter', 'high $ 44.72', 'low $ 34.25'], ['second quarter', '52.25', '39.95', 'second quarter', '49.63', '35.56'], ['third quarter', '44.50', '12.00', 'third quarter', '70.25', '45.13'], ['fourth quarter', '17.80', '11.60', 'fourth quarter', '72.81', '45.00']]( b ) holders . as of march 2 , 2002 , there were 9967 record holders of the company 2019s common stock , par value $ 0.01 per share . ( c ) dividends . under the terms of the company 2019s corporate revolving loan and letters of credit facility of $ 850 m... [1,000 / 2,073 chars] |
| what was the total impairment costs recorded from 2003 to 2005 in millions [74 chars] | notes to consolidated financial statements for the years ended february 3 , 2006 , january 28 , 2005 , and january 30 , 2004 , gross realized gains and losses on the sales of available-for-sale securities were not mate- rial . the cost of securities sold is based upon the specific identification method . merchandise inventories inventories are stated at the lower of cost or market with cost determined using the retail last-in , first-out ( 201clifo 201d ) method . the excess of current cost over lifo cost was approximately $ 5.8 million at february 3 , 2006 and $ 6.3 million at january 28 , 2005 . current cost is deter- mined using the retail first-in , first-out method . lifo reserves decreased $ 0.5 million and $ 0.2 million in 2005 and 2004 , respectively , and increased $ 0.7 million in 2003 . costs directly associated with warehousing and distribu- tion are capitalized into inventory . in 2005 , the company expanded the number of inven- tory departments it utilizes for its gross p... [1,000 / 4,728 chars] |
| what percent of total recourse debt is current? [47 chars] | the aes corporation notes to consolidated financial statements 2014 ( continued ) december 31 , 2010 , 2009 , and 2008 recourse debt as of december 31 , 2010 is scheduled to reach maturity as set forth in the table below : december 31 , annual maturities ( in millions ) .[['december 31,', 'annual maturities ( in millions )'], ['2011', '$ 463'], ['2012', '2014'], ['2013', '2014'], ['2014', '497'], ['2015', '500'], ['thereafter', '3152'], ['total recourse debt', '$ 4612']]recourse debt transactions during 2010 , the company redeemed $ 690 million aggregate principal of its 8.75% ( 8.75 % ) second priority senior secured notes due 2013 ( 201cthe 2013 notes 201d ) . the 2013 notes were redeemed at a redemption price equal to 101.458% ( 101.458 % ) of the principal amount redeemed . the company recognized a pre-tax loss on the redemption of the 2013 notes of $ 15 million for the year ended december 31 , 2010 , which is included in 201cother expense 201d in the accompanying consolidated stat... [1,000 / 3,155 chars] |

### Source Reference Table

| Title | Year | Type | URL |
| --- | ---: | --- | --- |
| FinQA: A Dataset of Numerical Reasoning over Financial Data | 2021 | task paper | [https://aclanthology.org/2021.emnlp-main.300/](https://aclanthology.org/2021.emnlp-main.300/) |
| ibm/finqa |  | dataset card | [https://huggingface.co/datasets/ibm/finqa](https://huggingface.co/datasets/ibm/finqa) |
| Introducing RTEB: A New Standard for Retrieval Evaluation | 2025 | benchmark article | [https://huggingface.co/blog/rteb](https://huggingface.co/blog/rteb) |

### Representative Snippets

| Query | Relevant document excerpt |
| --- | --- |
| What was the difference between the company's high and low sales price for the second quarter of 2001? | A market-information excerpt listing common stock trading prices. |
| What was the total impairment cost recorded from 2003 to 2005? | A financial statement note discussing impairment and securities. |
| What percent of total recourse debt is current? | A debt maturity table from consolidated financial statements. |
| What was average operating profit for MFC between 2014 and 2016? | A report excerpt with operating profit figures across years. |
| In 2017, what share of future estimated cash payments under obligations was due in 2018? | A contractual obligations passage with future payment amounts. |
