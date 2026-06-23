# NanoRTEB / NanoHC3Finance

## Overview

`NanoHC3Finance` is an English finance-domain answer retrieval task from NanoRTEB. The query is a short personal-finance or investing prompt, and the relevant document is the paired explanatory answer from the HC3 finance subset. Each query has one positive answer among 415 documents. Dense retrieval has the strongest top-rank profile, `reranking_hybrid` has the best recall@100, and BM25 is weaker because many prompts are terse and do not provide enough lexical signal to identify the paired response.

## Details

### What the Original Data Measures

HC3 compares human expert and ChatGPT answers across several domains, including finance. The original corpus was designed for studying answer style and detection, not as a classic retrieval benchmark.

RTEB uses the finance portion as retrieval. A system receives a user finance question and must retrieve the answer or explanation paired with it. The task is therefore answer retrieval over practical finance advice, not financial statement evidence retrieval.

### Observed Data Profile

The Nano split contains 200 queries, 415 documents, and 200 positive qrel rows. Every query has exactly one positive. Queries average 61.41 characters, while answer documents average 991.30 characters.

Example prompts ask whether a web scheme is legitimate, how to interpret Google Finance dividend data, how to track credit card transactions for fraud prevention, whether stock options encourage long-term investment, and whether a lender cares what borrowed money is used for.

### BM25 Evaluation Profile

The BM25 candidate subset uses the full 415-document pool and reaches nDCG@10 of 0.3079, hit@10 of 0.4750, and recall@100 of 0.7800. BM25 can match distinctive finance terms such as dividends, credit cards, stock options, or loans.

The limitation is that many queries are short and broad. A prompt such as a beginner investing question can match many plausible answers, and the paired response may use different vocabulary from the user question.

### Dense Evaluation Profile

The dense candidate subset from `harrier_oss_v1_270m` uses the full 415-document pool and reaches nDCG@10 of 0.4654, hit@10 of 0.6650, and recall@100 of 0.9150. Dense retrieval is the strongest top-rank profile.

This indicates that embedding similarity captures finance-topic intent and advice type better than term frequency. It is especially useful when the response explains a concept or risk without repeating the exact wording of the prompt.

### Reranking Hybrid Evaluation Profile

The `reranking_hybrid` subset uses top-100 candidates, with 13 rows receiving the optional rank-101 safeguard. It reaches nDCG@10 of 0.4177, hit@10 of 0.5950, and recall@100 of 0.9350. Hybrid retrieval has the best broad coverage but weaker early ranking than dense retrieval.

This makes hybrid useful as a reranking pool. Sparse terms recover exact finance topics, while dense retrieval ranks paired responses more effectively. A downstream reranker can benefit from the extra coverage.

### Metric Interpretation for Model Researchers

With one positive per query, nDCG@10 measures how early the paired answer appears, hit@10 measures whether it appears in the first ten candidates, and recall@100 measures whether a reranker can access it.

For `NanoHC3Finance`, dense nDCG@10 is the main first-stage signal. Recall@100 matters because many answers are topically plausible and a reranker may need to compare advice specificity.

### Query and Relevance Type Tendencies

Queries are short personal-finance prompts. Relevant documents are long explanatory answers about investing, loans, fraud, dividends, taxes, or credit. The answer often expands the topic far beyond the wording of the query.

Relevance is the original question-answer pairing. A finance answer can be topically reasonable and still be non-relevant if it is not the paired response.

### Representative Failure Modes

Common failures include retrieving a generic finance explanation, confusing nearby topics such as investing and retirement accounts, overmatching exact terms while missing advice intent, and ranking broad answers above the paired answer. BM25 is limited by short queries; dense retrieval can still blur similar finance-advice categories.

### Training Data That May Help

Useful training data includes personal-finance QA retrieval, finance forum question-answer pairs, answer ranking, and hard negatives from nearby topics such as budgeting, investing, taxes, loans, and credit. Evaluation questions, answers, and qrels should be excluded.

### Model Improvement Notes

Models should represent user intent, topic, risk framing, and answer specificity. Hard negatives should share the same finance keyword but give advice for a different context. Dense retrieval is the best first-stage ranker, while hybrid retrieval is useful for higher-recall candidate generation.

## Example Data

| Query | Positive document |
| --- | --- |
| Is socialtrend.com or/and feelthetrend.com legitimate? [54 chars] | It's called a "Pyramid scheme". Its illegal in almost every country of the Western world. You're not going to earn lifetime income, of course, and these things collapse pretty quickly. Most of the "co... [200 / 989 chars] |
| How to read Google Finance data on dividends [44 chars] | However, you have to remember that not all dividends are paid quarterly. For example one stock I recently purchased has a price of $8.03 and the Div/yield = 0.08/11.9 . $.08 * 4 = $0.32 which is only... [200 / 392 chars] |
| What is a good way to keep track of your credit card transactions, to reduce likelihood of fraud? [97 chars] | Read your bill, question things that don't look familiar. People who steal credit card numbers don't bother to conceal themselves well. So if you live in Florida, and all of the sudden charges appear... [200 / 725 chars] |
| When Employees are “Granted” Stock Options, is the Company encouraging Long-Term investments from th... [100 / 103 chars] | There are two things to consider: taxes - beneficial treatment for long-term holding, and for ESPP's you can get lower taxes on higher earnings. Also, depending on local laws, some share schemes allow... [200 / 931 chars] |
| Does lender care what I use the money for? [42 chars] | When you borrow from a bank, there are secured loans, as with a mortgage, or unsecured lines of credit, usually a more reasonable amount of money, but also based on income. You just asked about a priv... [200 / 429 chars] |

### Source Reference Table

| Title | Year | Type | URL |
| --- | ---: | --- | --- |
| How Close is ChatGPT to Human Experts? Comparison Corpus, Evaluation, and Detection | 2023 | task paper | [https://arxiv.org/abs/2301.07597](https://arxiv.org/abs/2301.07597) |
| Hello-SimpleAI/HC3 |  | dataset card | [https://huggingface.co/datasets/Hello-SimpleAI/HC3](https://huggingface.co/datasets/Hello-SimpleAI/HC3) |
| Introducing RTEB: A New Standard for Retrieval Evaluation | 2025 | benchmark article | [https://huggingface.co/blog/rteb](https://huggingface.co/blog/rteb) |

### Representative Snippets

| Query | Relevant document excerpt |
| --- | --- |
| Is a trend-income website legitimate? | The answer identifies the pattern as a pyramid scheme and warns about collapse risk. |
| How should Google Finance dividend data be read? | The answer explains dividend frequency and annualized yield interpretation. |
| How can someone track credit card transactions to reduce fraud risk? | The answer advises reading bills and investigating unfamiliar charges. |
| Do granted stock options encourage employees to invest long term? | The answer discusses tax treatment and share-scheme incentives. |
| Does a lender care what borrowed money is used for? | The answer contrasts secured loans, credit lines, and private loans. |
