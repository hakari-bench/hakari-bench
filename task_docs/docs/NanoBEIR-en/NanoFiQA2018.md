# NanoBEIR-en / NanoFiQA2018

## Overview

NanoFiQA2018 is the compact English NanoBEIR version of FiQA-2018, a financial question answering retrieval task. Each query is a finance-related user question, and the corpus contains answer posts or answer-like passages from a specialized finance domain. The retrieval goal is to find passages that resolve practical questions about taxes, retirement accounts, trading mechanics, debt, checks, ETFs, and investing. This makes the task useful for evaluating domain-specific answer retrieval and financial decision-oriented matching.

## Details

### What the Original Data Measures

FiQA-2018 was introduced as a Web Conference challenge for financial opinion mining and question answering. The QA component focuses on ranking or producing answers for financial questions, using finance-domain text rather than generic encyclopedic passages. Answers are often practical, opinionated, and caveated.

The BEIR version treats FiQA as a retrieval benchmark: the query is a financial question and relevant documents are answer posts or passages. The NanoBEIR version keeps this domain-specific retrieval setting in a compact sample. A model must understand the user's financial action and constraints, not simply match finance keywords.

### Observed Data Profile

The task contains 50 queries, 4,598 documents, and 123 relevance judgments. It is moderately multi-positive, with an average of 2.46 positives per query. The minimum is 1, the median is 2.0, the maximum is 15, and 28 queries are multi-positive, or 56.0% of the set.

Queries average 58.52 characters, while documents average 899.63 characters. The queries are concise practical questions, and the documents are longer community-style answers with examples, assumptions, tax caveats, or broker-specific reasoning. This creates a large gap between query wording and answer expression.

### BM25 Evaluation Profile

BM25 reaches nDCG@10 of 0.4211, hit@10 of 0.7400, and recall@100 of 0.7236 using the top-500 BM25 candidate subset. Lexical matching is useful when queries contain explicit product names, tax terms, account types, or finance actions. It often retrieves documents in the right financial subdomain.

The limitation is answer intent. BM25 can over-rank passages that share terms such as tax, check, ETF, debt, or capital gains while answering a different decision. Finance retrieval often turns on jurisdiction, account type, timing, and practical consequence, which may not be captured by word overlap alone.

### Dense Evaluation Profile

The dense harrier-oss-270m run reaches nDCG@10 of 0.5011, hit@10 of 0.7600, and recall@100 of 0.7317. Dense retrieval improves top-rank quality and coverage over BM25. This shows that embedding similarity helps connect short financial questions to explanatory answer passages that may use different wording.

The gain is meaningful but not complete. A general dense model may still retrieve semantically related financial advice that does not answer the exact question. Domain-specific terms, tax rules, and account mechanics require specialized supervision to rank the right answer over near-topic distractors.

### Reranking Hybrid Evaluation Profile

The reranking_hybrid candidate set reaches nDCG@10 of 0.5150, hit@10 of 0.8000, and recall@100 of 0.8049. It uses a top-100 candidate range with an optional rank-101 safeguard; this slice has 4 safeguard rows, candidate counts from 100 to 101, and a mean of 100.08 candidates. It is the strongest profile across the reported metrics.

The hybrid result shows that finance QA benefits from combining exact financial terminology with semantic answer matching. BM25 contributes product and rule anchors, while dense retrieval contributes paraphrase and decision-intent coverage. For downstream reranking, reranking_hybrid is the best observed candidate pool.

### Metric Interpretation for Model Researchers

Because more than half the queries have multiple positives, nDCG@10 rewards ranking several useful answers, while hit@10 measures whether at least one answer appears. recall@100 is important when a reranker may need to choose among several possible answer posts.

The comparison shows that BM25 alone is not enough, dense retrieval improves answer-intent matching, and reranking_hybrid gives the best overall behavior. This task is useful for evaluating whether a model can retrieve practical financial advice rather than merely finance-themed text.

### Query and Relevance Type Tendencies

Queries ask about quoted Vanguard returns, freelancing tax implications, what counts as high or low trading volume, using credit-card points for deductible business expenses, and filing taxes as a contractor. Relevant documents are explanatory answers that may include calculations, legal assumptions, or personal finance guidance.

The task rewards domain-specific interpretation. A relevant answer should resolve the user's financial decision or explanation need. Documents that mention the same account, tax form, or financial product but answer another issue are hard negatives.

### Representative Failure Modes

Likely failures include retrieving generic finance definitions, confusing related tax or account scenarios, missing answers expressed with financial jargon or examples, and over-ranking passages that share product names but not the decision point. BM25 may be too literal, while dense retrieval may be too broad without finance-domain training.

### Training Data That May Help

Useful training data includes non-overlapping FiQA question-answer pairs, financial community QA, personal-finance forum retrieval, finance FAQ ranking, and domain QA covering taxes, retirement accounts, brokerage, debt, banking, and insurance. Multi-positive objectives are useful because many questions have several acceptable answers.

### Model Improvement Notes

A model targeting this task should improve domain-specific answer matching while preserving exact financial terminology. Sparse systems need normalization and expansion for finance terms. Dense systems need financial QA contrastive training with near-topic hard negatives. Hybrid systems are promising because the observed profile is best when lexical and semantic signals are combined.

## Example Data

| Query | Positive document |
| --- | --- |
| What type of returns Vanguard is quoting? [41 chars] | "From the Vanguard page - This seemed the easiest one as S&P data is simple to find. I use MoneyChimp to get - which confirms that Vanguard's page is offering CAGR, not arithmetic Average. Note: Vanguard states ""For U.S. stock market returns, we use the Standard & Poor's 90 from 1926 through March 3, 1957,"" while the Chimp uses data from Nobel Prize winner, Robert Shiller's site." [387 chars] |
| Freelancing Tax implication [27 chars] | If you have income in the US, you will owe US income tax on it, unless there is a treaty with your country that says otherwise. [127 chars] |
| What is considered high or low when talking about volume? [57 chars] | The daily Volume is usually compared to the average daily volume over the past 50 days for a stock. High volume is usually considered to be 2 or more times the average daily volume over the last 50 days for that stock, however some traders might set the crireia to be 3x or 4x the ADV for confirmation of a particular pattern or event. The volume is compared to the ADV of the stock itself, as comparing it to the volume of other stocks would be like comparing apples with oranges, as difference companies would have different number of total stocks available, different levels of liquidity and different levels of volatility, which can all contribute to the volumes traded each day. [684 chars] |

### Source Reference Table

| Item | Reference |
| --- | --- |
| Original challenge paper | [WWW'18 Open Challenge: Financial Opinion Mining and Question Answering](https://doi.org/10.1145/3184558.3192301) |
| Challenge site | [FiQA 2018 official challenge site](https://sites.google.com/view/fiqa/home) |
| Retrieval benchmark framing | [BEIR](https://arxiv.org/abs/2104.08663) |
| NanoBEIR collection | [NanoBEIR on Hugging Face](https://huggingface.co/collections/zeta-alpha-ai/nanobeir) |
| NanoBEIR-en dataset | [hakari-bench/NanoBEIR-en](https://huggingface.co/datasets/hakari-bench/NanoBEIR-en) |

Representative query and positive answer snippets:

| Query | Positive document snippet |
| --- | --- |
| What type of returns Vanguard is quoting? | The Vanguard page appears to be offering CAGR, not arithmetic average. |
| Freelancing Tax implication | If you have income in the US, you will owe US income tax on it unless a treaty says otherwise. |
| What is considered high or low when talking about volume? | Daily volume is usually compared to average daily volume over the past 50 days. |
| Using credit card points to pay for tax deductible business expenses | Cash back from credit cards for personal use is generally not taxable, but business use is different. |
| How should I file my taxes as a contractor? | You may need to file as an employee and also as an entrepreneur, depending on the arrangement. |
