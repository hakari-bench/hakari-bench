# MNanoBEIR / NanoBEIR-ar / NanoFiQA2018

## Overview

NanoBEIR-ar / NanoFiQA2018 is the Arabic NanoBEIR version of FiQA-2018, a
financial opinion mining and question answering benchmark introduced for the
WWW 2018 Open Challenge. Each query is an Arabic translated personal-finance
question, and the retrieval target is an Arabic translated answer passage that
addresses the user's financial decision or explanation need. The Nano task
contains 50 queries, 4,598 answer candidates, and 123 positive qrels. More than
half of the queries have multiple positives, so the task is not simply finding
one exact answer. It tests whether retrieval models can connect short financial
questions to longer community-style answers with caveats, examples, account
types, tax assumptions, debt details, or investment-product reasoning.

## Details

### What the Original Data Measures

FiQA-2018 includes an opinion-based financial question answering task built from
financial community question-answer data. In BEIR-style retrieval, the question
is the query and answer passages are ranked as candidate documents. The task is
not an encyclopedia lookup: answers often contain practical reasoning,
conditional advice, assumptions, warnings, or explanations from a personal
finance context.

The Arabic NanoBEIR version keeps that retrieval shape in translated form. A
retriever must find answer passages that resolve the financial question, not
merely passages that mention the same product or account name. This makes the
task useful for evaluating domain-specific semantic retrieval in finance.

### Observed Data Profile

The metadata records 50 queries, 4,598 documents, and 123 positive qrels. The
average is 2.46 positives per query, the median is 2, and the maximum is 15.
There are 28 multi-positive queries, or 56.0% of the set. Queries average 53.60
characters, while answer documents average 796.36 characters. Example topics
include Vanguard returns, self-employment tax, volume thresholds, business
credit-card points, tax returns for contractors, country debt, calendar
spreads, investor losses, and 401(k) employer matches.

The data shape is practical QA retrieval. Many queries ask for an explanation
or decision rather than a definition. Relevant answers may use different words
from the question and may depend on jurisdiction, account type, investment
instrument, or numeric assumptions. This makes semantic matching more important
than simple term overlap.

### BM25 Evaluation Profile

The BM25 candidate subset reaches nDCG@10 = 0.3196, hit@10 = 0.5400, and
Recall@100 = 0.6016. BM25 can recover answers when the question and passage
share product names, account labels, tax terms, debt terms, or finance
vocabulary such as margin, options, credit cards, retirement accounts, and
brokerage operations.

Its weakness is that financial questions often express an action or decision,
while the answer explains the reasoning indirectly. The same words can appear
in generic definitions, related anecdotes, or answers to a different financial
situation. BM25 therefore works as a domain-term anchor but misses many
relevant answers and is not reliable as a final ranking signal for advice-like
questions.

### Dense Evaluation Profile

The dense candidate subset from `harrier_oss_v1_270m` reaches nDCG@10 =
0.3934, hit@10 = 0.6200, and Recall@100 = 0.7236. Dense retrieval improves over
BM25 on all visible aggregate metrics. This indicates that embedding similarity
is better at matching a short Arabic finance question to an answer passage that
uses different wording but resolves the same decision.

Dense retrieval is especially useful for questions about tradeoffs, account
mechanics, tax treatment, or financial planning choices. Its failure mode is
domain-neighbor drift: a model may retrieve a passage about the same broad
financial product but not the same decision, jurisdiction, constraint, or
numeric assumption. The task therefore rewards semantic matching that remains
grounded in the specific financial context.

### Reranking Hybrid Evaluation Profile

The `reranking_hybrid` candidate subset reaches nDCG@10 = 0.3900, hit@10 =
0.6200, and Recall@100 = 0.7317. Hybrid nearly matches dense at the top of the
ranking and slightly improves Recall@100. The metadata records 6 rows with the
optional rank-101 safeguard, showing that a few positives sit near the
candidate boundary and need preservation.

For reranker evaluation, hybrid is the safest candidate pool. It keeps BM25's
financial terminology anchors while adding dense candidates that answer the
same question with different wording. The reranker can then focus on whether a
candidate answer actually resolves the user's financial need.

### Metric Interpretation for Model Researchers

NanoFiQA2018-ar shows a semantic-retrieval advantage. Dense retrieval is the
best top-rank signal by nDCG@10 and ties hybrid on hit@10. Hybrid gives the
best Recall@100, which matters because the task is multi-positive and several
answers may be useful for the same question. BM25 is noticeably weaker,
suggesting that exact financial vocabulary is not enough for Arabic translated
community QA.

For first-stage retrievers, the target is to preserve product and account terms
while expanding to answers that explain the same decision. For rerankers, the
target is to distinguish useful advice from passages that merely discuss the
same financial product.

### Query and Relevance Type Tendencies

Queries are short Arabic personal-finance questions. They ask about taxes,
investment returns, employer matches, debt payment, brokerage rules, option
positions, trading volume, account treatment, and business expenses. Relevant
documents are longer answer passages, often with caveats or examples. A
positive answer should address the financial decision or explanation, not just
mention the same terms.

Lexical-heavy cases include named products, account labels, tax forms, or
investment instruments. Dense-heavy cases include "what should I do" questions,
causal explanations, and advice where the answer uses different vocabulary.
Hybrid retrieval is useful when the product name must be preserved but semantic
matching is needed to find the actual answer.

### Representative Failure Modes

BM25 can retrieve generic pages or forum answers that share a term such as tax,
debt, margin, credit card, or retirement account but do not answer the user's
specific question. Dense retrieval can retrieve a plausible finance answer that
matches the broad topic while missing a crucial condition such as jurisdiction,
account type, employer match, business use, or investment product. Multi-positive
queries also create coverage failures when the model finds one answer but misses
other valid perspectives.

Good hard negatives are same-product answers with different assumptions,
same-topic answers for a different jurisdiction, and passages that explain a
financial term without resolving the query.

### Arabic-Specific Notes

Arabic financial retrieval mixes translated community language, technical
finance terms, account names, tax vocabulary, English product names, and
numbers. Sparse retrieval needs tokenization that preserves product labels and
financial expressions. Dense retrieval needs finance-domain coverage so it can
connect user-style questions to answer-style explanations. Strong systems
should preserve exact account and product terms while matching paraphrased
advice.

### Training and Leakage Notes

Training should exclude FiQA, BEIR, or NanoBEIR records likely to overlap with
these evaluation questions or answer passages. Useful non-overlapping data
includes FiQA-style question-answer pairs, Arabic or multilingual financial
community QA, personal-finance forum retrieval, and brokerage, tax, debt,
banking, or retirement-account FAQ retrieval pairs. Reports should disclose any
FiQA or StackExchange-derived financial QA exposure.

### Model Improvement Hints

The main improvement target is domain-aware answer matching. First-stage
retrievers should preserve financial terms while using dense similarity to find
answers that resolve the same decision. Rerankers should compare same-topic
answers with different assumptions and learn whether the candidate actually
addresses the question. Multi-positive training is useful because several
answers may be relevant.

### Training Data That May Help

Useful training data includes non-overlapping financial QA, Arabic personal
finance forums, multilingual finance QA, tax and brokerage FAQs, debt and
retirement-account retrieval data, and synthetic question-answer pairs with
explicit account types and assumptions.

### Synthetic Data Guidance

Generate Arabic personal-finance questions from non-evaluation answer passages.
Include investment products, taxes, debt, banking, brokerage operations,
retirement accounts, employer matches, jurisdictions, numeric assumptions, and
caveats. Positives should answer the decision or explanation need; hard
negatives should mention the same product but fail to resolve the user's
situation.

## Example Data

| Query | Positive document |
| --- | --- |
| ما نوع العوائد التي تقدمها فيجارد؟ [34 chars] | من صفحة فاندغارد - بدا هذا هو الأسهل لأن بيانات S&P سهلة العثور عليها. أستخدم MoneyChimp للحصول على البيانات، والتي تؤكد أن صفحة فاندغارد تقدم معدل نمو مركب سنوي، وليس متوسط حسابي. ملاحظة: تعلن فاندغا... [200 / 370 chars] |
| التزامات الضريبية للعمل الحر [28 chars] | إذا كان لديك دخل في الولايات المتحدة، فأنت ملزم بدفع ضريبة الدخل الأمريكية عليه، إلا إذا كان هناك اتفاقية بين بلدك والولايات المتحدة تنص على خلاف ذلك. [150 chars] |
| ما هو المعيار للتمييز بين الحجم العالي والنخفض؟ [47 chars] | الحجم اليومي عادةً ما يقارن بالمتوسط اليومي للحجم على مدى الـ 50 يومًا الماضية لأسهم معينة. يُعتبر الحجم العالي عادةً أنه ضعف أو أكثر من المتوسط اليومي للحجم على مدى الـ 50 يومًا الماضية لأسهم معينة،... [200 / 596 chars] |
| استخدام نقاط بطاقة الائتمان في دفع نفقات العمل المستحقة للخصم الضريبي [69 chars] | لتبسيط الأمر، لنبدأ بتفكيرنا في استرداد النقد فقط. عمومًا، لا يتم فرض ضرائب على استرداد النقد من بطاقات الائتمان للاستخدام الشخصي، ولكن للاستخدام التجاري، يتم فرض ضرائب عليه (بشكل ما، سأشرح ذلك لاحقًا... [200 / 3,125 chars] |
| كيف يمكنني إعداد إقرار ضريبي كعامل مستقل؟ [41 chars] | لأغراض الضرائب، يجب عليك تقديم الإقرار كعامل (إيصالات T4 والضرائب المحجوزة تلقائيًا)، ولكن أيضًا كمتعهد. كنت في نفس الوضع نفسي العام الماضي. موضوع "عامل ومتعهد" هو نشر من قبل دائرة الإيرادات الكندية س... [200 / 558 chars] |

### Public Sources

- [WWW'18 Open Challenge: Financial Opinion Mining and Question Answering](https://doi.org/10.1145/3184558.3192301), 2018.
- [BEIR: A Heterogeneous Benchmark for Zero-shot Evaluation of Information Retrieval Models](https://arxiv.org/abs/2104.08663), 2021.
- [MMTEB: Massive Multilingual Text Embedding Benchmark](https://arxiv.org/abs/2502.13595), 2025.
- [Zeta Alpha NanoBEIR collection](https://huggingface.co/collections/zeta-alpha-ai/nanobeir).

### Hugging Face Links

- Nano dataset: [hakari-bench/NanoBEIR-ar](https://huggingface.co/datasets/hakari-bench/NanoBEIR-ar)
- Source collection: [Zeta Alpha NanoBEIR collection](https://huggingface.co/collections/zeta-alpha-ai/nanobeir)

### Source Reference Table

| Title | Year | Type | URL |
| --- | ---: | --- | --- |
| WWW'18 Open Challenge: Financial Opinion Mining and Question Answering | 2018 | task paper | [https://doi.org/10.1145/3184558.3192301](https://doi.org/10.1145/3184558.3192301) |
| BEIR: A Heterogeneous Benchmark for Zero-shot Evaluation of Information Retrieval Models | 2021 | benchmark paper | [https://arxiv.org/abs/2104.08663](https://arxiv.org/abs/2104.08663) |
| MMTEB: Massive Multilingual Text Embedding Benchmark | 2025 | benchmark paper | [https://arxiv.org/abs/2502.13595](https://arxiv.org/abs/2502.13595) |
| NanoBEIR: Smaller BEIR dataset subsets | 2024 | dataset collection | [https://huggingface.co/collections/zeta-alpha-ai/nanobeir](https://huggingface.co/collections/zeta-alpha-ai/nanobeir) |
