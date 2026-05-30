# MNanoBEIR / NanoBEIR-de / NanoFiQA2018

## Overview

NanoBEIR-de / NanoFiQA2018 is the German NanoBEIR version of FiQA-2018, a
financial opinion mining and question answering benchmark introduced for the
WWW 2018 Open Challenge. Each query is a German translated personal-finance
question, and the retrieval target is a German translated answer passage that
addresses the user's financial decision or explanation need. The Nano task
contains 50 queries, 4,598 documents, and 123 positive qrels. More than half of
the queries have multiple positives. This is a difficult sparse-retrieval task:
BM25 is weak, dense retrieval is the strongest top-rank signal, and
`reranking_hybrid` gives the best top-100 coverage.

## Details

### What the Original Data Measures

FiQA-2018 includes a financial opinion QA task built from community finance
questions and answers. The retrieval target is not an encyclopedia definition.
It is an answer-like passage that resolves a practical financial question,
often with caveats, examples, account types, tax rules, jurisdictions, or
numeric assumptions.

The German NanoBEIR version keeps this retrieval shape in translated form. The
model must connect a user question to an answer passage, even when the answer
uses different wording and explains the financial reasoning rather than
repeating the query.

### Observed Data Profile

The metadata records 50 queries, 4,598 documents, and 123 positive qrels.
Queries average 2.46 positives; 28 queries are multi-positive, and one has 15
positives. Query text averages 74.62 characters, while documents average
1,052.17 characters. Examples include Vanguard returns, freelancing tax,
trading volume, business credit-card points, contractor tax filing, government
debt, investing through another person, calendar spreads, investor losses, and
401(k)-style employer matches.

The task is practical financial QA. Relevant answers may depend on details
that are not visible in the query terms alone: account type, jurisdiction,
taxability, margin rules, employer contribution, or whether the passage gives
actionable advice.

### BM25 Evaluation Profile

The BM25 candidate subset reaches nDCG@10 = 0.1864, hit@10 = 0.4400, and
Recall@100 = 0.5203. BM25 is the weakest candidate view. It can find passages
when query and answer share product names, account labels, tax terms, or
finance vocabulary, but many answer passages explain the decision in different
words.

BM25 often retrieves generic finance text that shares words like tax, debt,
investment, volume, or credit card without answering the user's specific
question. This task exposes the limits of term-frequency matching for
advice-like financial retrieval.

### Dense Evaluation Profile

The dense candidate subset from `harrier_oss_v1_270m` reaches nDCG@10 =
0.3977, hit@10 = 0.6600, and Recall@100 = 0.7073. Dense retrieval is the best
top-rank signal by a wide margin. This indicates that embedding similarity
helps connect German personal-finance questions to answer passages that resolve
the same decision or explanation need.

Dense retrieval's risk is financial-neighbor drift. It may retrieve an answer
about the same product or broad finance topic while missing the specific
condition, jurisdiction, or account mechanics. Still, it is much more useful
than sparse overlap for this task.

### Reranking Hybrid Evaluation Profile

The `reranking_hybrid` candidate subset reaches nDCG@10 = 0.2704, hit@10 =
0.5000, and Recall@100 = 0.7317. Hybrid is weaker than dense at the top but
has the best Recall@100. The metadata records 4 rows with the optional rank-101
safeguard, showing that some positives needed boundary preservation.

For reranker experiments, hybrid is the safest candidate source because it
keeps lexical product/account anchors while adding dense semantic matches. A
reranker can then decide which answer actually resolves the financial question.

### Metric Interpretation for Model Researchers

NanoFiQA2018-de shows a strong dense advantage. BM25 is poor for top-10
ranking, dense retrieval is the best final first-stage order, and hybrid is the
best candidate pool for reranking. Because the task is multi-positive, Recall@100
matters: a model should recover several useful answers, not only one.

Researchers should inspect whether failures are caused by broad finance-topic
matching, jurisdiction mismatch, product confusion, or missing the decision
framing of the question.

### Query and Relevance Type Tendencies

Queries are German personal-finance questions. They ask about taxes, freelance
income, investments, brokerage mechanics, trading volume, debt, credit cards,
retirement accounts, and employer matches. Relevant documents are longer
community-style answers with assumptions and caveats.

Lexical-heavy cases include named products or exact account terms. Dense-heavy
cases include decision questions where the answer explains reasoning in
different vocabulary. Hybrid retrieval helps when exact product terms and
semantic advice matching are both needed.

### Representative Failure Modes

BM25 can retrieve passages that mention a finance term but do not answer the
specific user question. Dense retrieval can retrieve a plausible answer about
the same product while missing a crucial condition such as tax status,
jurisdiction, business use, or account type. Multi-positive failures occur when
one answer is found but alternative valid answers are missed.

Good hard negatives are same-product answers with different assumptions,
same-topic answers for another jurisdiction, and generic definitions that do
not resolve the decision.

### German-Specific Notes

German financial retrieval includes compound terms, translated community style,
English product names, tax vocabulary, account labels, and numeric examples.
Sparse retrieval needs to preserve product names and financial expressions.
Dense retrieval needs German finance-domain coverage and should not smooth away
account-specific details.

### Training and Leakage Notes

Training should exclude FiQA, BEIR, or NanoBEIR records likely to overlap with
these evaluation questions or answer passages. Useful non-overlapping data
includes FiQA-style QA, German or multilingual financial community QA,
personal-finance forum retrieval, and brokerage, tax, debt, banking, or
retirement-account FAQ retrieval pairs.

### Model Improvement Hints

The main improvement target is financial answerability matching. First-stage
retrievers should use dense semantics for decision/explanation matching while
preserving account and product terms. Rerankers should be trained on
same-topic answers with different assumptions so they learn whether a candidate
actually resolves the query.

### Training Data That May Help

Useful training data includes non-overlapping financial QA, German personal
finance forums, multilingual finance QA, tax and brokerage FAQ retrieval, debt
and retirement-account examples, and hard negatives from the same product
family.

### Synthetic Data Guidance

Generate German community-style financial answers with caveats, examples,
account types, jurisdictions, and numeric assumptions. Then generate
personal-finance questions asking for decisions or explanations that the answer
resolves. Positives should answer the financial need, not merely mention the
same product.

## Example Data

| Query | Positive document |
| --- | --- |
| Welche Art von Renditen bietet Vanguard an? (43 chars) | Von der Vanguard-Seite - Dies erschien als das einfachste, da die S&P-Daten leicht zu finden sind. Ich nutze MoneyChimp, um zu bestätigen, dass die Vanguard-Seite den CAGR und nicht den arithmetischen Durchschnitt anbietet. H ... [truncated 225 chars](449 chars) |
| Steuerliche Auswirkungen des Freelancings (41 chars) | Wenn Sie in den USA Einkommen erzielen, müssen Sie darauf US-Einkommensteuer zahlen, es sei denn, es gibt ein Abkommen mit Ihrem Land, das etwas anderes regelt. (160 chars) |
| Was bedeutet "hoch" oder "niedrig" im Zusammenhang mit Lautstärke? (66 chars) | Das tägliche Handelsvolumen wird in der Regel mit dem durchschnittlichen Tageshandelsvolumen der letzten 50 Tage für eine Aktie verglichen. Ein hohes Handelsvolumen wird in der Regel als 2-mal oder mehr des durchschnittlichen ... [truncated 225 chars](890 chars) |
| Kann ich Kreditkartenpunkte für steuerlich absetzbare Geschäftsausgaben verwenden? (82 chars) | Um es einfach zu halten, beginnen wir mit der Rückerstattung von Bargeld. Im Allgemeinen ist die Rückerstattung von Bargeld durch Kreditkarten für den privaten Gebrauch nicht steuerpflichtig, für den Geschäftsgebrauch jedoch ... [truncated 225 chars](4138 chars) |
| Wie mache ich meine Steuererklärung als Freiberufler? (53 chars) | Für steuerliche Zwecke müssen Sie Ihre Steuern sowohl als Arbeitnehmer (T4-Belege und automatisch einbehaltene Steuern) als auch als Selbstständiger einreichen. Ich hatte letztes Jahr die gleiche Situation. "Arbeitnehmer und ... [truncated 225 chars](893 chars) |

### Public Sources

- [WWW'18 Open Challenge: Financial Opinion Mining and Question Answering](https://doi.org/10.1145/3184558.3192301), 2018.
- [BEIR: A Heterogeneous Benchmark for Zero-shot Evaluation of Information Retrieval Models](https://arxiv.org/abs/2104.08663), 2021.
- [MMTEB: Massive Multilingual Text Embedding Benchmark](https://arxiv.org/abs/2502.13595), 2025.
- [Zeta Alpha NanoBEIR collection](https://huggingface.co/collections/zeta-alpha-ai/nanobeir).

### Hugging Face Links

- Nano dataset: [hakari-bench/NanoBEIR-de](https://huggingface.co/datasets/hakari-bench/NanoBEIR-de)
- Source collection: [Zeta Alpha NanoBEIR collection](https://huggingface.co/collections/zeta-alpha-ai/nanobeir)

### Source Reference Table

| Title | Year | Type | URL |
| --- | ---: | --- | --- |
| WWW'18 Open Challenge: Financial Opinion Mining and Question Answering | 2018 | task paper | https://doi.org/10.1145/3184558.3192301 |
| BEIR: A Heterogeneous Benchmark for Zero-shot Evaluation of Information Retrieval Models | 2021 | benchmark paper | https://arxiv.org/abs/2104.08663 |
| MMTEB: Massive Multilingual Text Embedding Benchmark | 2025 | benchmark paper | https://arxiv.org/abs/2502.13595 |
| NanoBEIR: Smaller BEIR dataset subsets | 2024 | dataset collection | https://huggingface.co/collections/zeta-alpha-ai/nanobeir |
