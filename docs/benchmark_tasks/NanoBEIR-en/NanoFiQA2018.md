# NanoBEIR-en / NanoFiQA2018

## Overview

FiQA-2018 is a financial opinion mining and question answering benchmark.
`NanoFiQA2018` is the compact English NanoBEIR retrieval task: each query is a
finance-related user question, and the system must retrieve answer posts or
answer-like passages that address it. The task tests retrieval in a specialized
personal-finance domain, where short questions about taxes, retirement accounts,
brokerage mechanics, checks, ETFs, debt, or investing must be matched to
opinionated explanatory answers.

## Details

### What the Original Data Measures

[WWW'18 Open Challenge: Financial Opinion Mining and Question
Answering](https://doi.org/10.1145/3184558.3192301) describes FiQA as a Web
Conference 2018 challenge for NLP over financial data. The paper frames finance
as a domain where interpretation of unstructured and structured sources is
important for fast decision making, and where domain-specific terminology and
concepts require specialized models.

The challenge had two tasks. Task 1 focused on aspect-based financial sentiment
analysis over microblogs and news headlines. Task 2, the source of this
retrieval task, focused on opinion-based question answering over financial data.
For Task 2, systems were given structured and unstructured English financial
text from sources such as microblogs, reports, and news, and were asked to
answer natural-language questions. The paper states that the task can be viewed
from both an information retrieval and a question answering perspective:
systems may rank relevant documents from the reference knowledge base or
generate answers.

The paper reports that the Opinion QA test collection was built by crawling
StackExchange posts under the Investment topic between 2009 and 2017. It
contains a knowledge base of 57,640 answer posts, with 17,110 question-answer
pairs for training and 531 question-answer pairs for testing. Evaluation used
ranking metrics such as nDCG and MRR. This matters for the Nano task because
the corpus documents are not neutral encyclopedic passages; they are community
answers, often written as practical financial advice with qualifications,
examples, and opinionated reasoning.

[BEIR: A Heterogeneous Benchmark for Zero-shot Evaluation of Information
Retrieval Models](https://arxiv.org/abs/2104.08663) includes FiQA as a
domain-specific financial question answering retrieval task. In the NanoBEIR
version, the query remains a financial question, while the relevant documents
are answer posts or answer passages selected by the FiQA/BEIR relevance data.

### Observed Data Profile

The sampled Nano task has 50 queries, 4,598 documents, and 123 positive qrel
rows. It is a multi-positive task: queries have an average of 2.46 positives,
28 of 50 queries have more than one positive, and one query has 15 positives.
The average query length is 58.52 characters, and the average document length is
899.63 characters.

The queries are practical personal-finance questions rather than abstract
finance definitions. The sample includes `Pay off credit card debt or earn
employer 401(k) match?`, `How should I file my taxes as a contractor?`,
`Short selling - lender's motivation`, `Which colors can one use to fill out a
check in the US?`, and `Will an ETF immediately reflect a reconstitution of
underlying index`. Many queries include jurisdictional, product, or account
details that change the answer.

The documents are long community answers. They often contain direct advice,
caveats, numeric assumptions, references to tax rules, broker behavior, or
personal experience. A relevant answer may not repeat the exact query wording:
for a 401(k) match question, the positive passage argues to take the employer
match; for a cheque-number question, the answer explains sequential numbering
and storage limits; for a contractor tax question, the answer distinguishes
employee and self-employed filing obligations.

### BM25 Difficulty

Using the dataset-provided BM25 candidate column, BM25 reaches nDCG@10 = 0.3583
and hit@10 = 0.6400. Only 32 of 50 queries have any positive in the top 10, and
the median first-positive rank is 3.5. Several inspected queries have no
positive until rank 100. This is much harder for BM25 than Quora duplicates or
FEVER-style entity claims.

The failure cases are domain-specific. For `What is the average cost of a
portfolio on a trading site?`, BM25 retrieves generic pages about average
returns and volatility before the relevant broker-cost answer. For `Selling
high, pay capital gains, re-purchase later`, BM25 retrieves broad capital-gains
definitions and generic tax-efficiency answers before the concise answer about
long-term capital gains and the wash-sale rule. For `Which colors can one use
to fill out a check in the US?`, BM25 drifts toward tax forms and background
checks because the words `check`, `fill out`, and `US` are not enough to capture
the banking-document intent.

The task rewards models that understand financial advice semantics, not just
finance vocabulary. Sparse matching often finds documents with the right words
but the wrong decision point: tax filing versus contract payment paperwork,
ETF construction versus index reconstitution timing, or selling shares for cash
versus tax gain harvesting. A stronger retriever should capture the user's
financial action, the instrument or account type, the jurisdictional setting,
and whether the answer is explanatory advice rather than a dictionary
definition.

### Training Data That May Help

Useful non-synthetic training data includes FiQA training question-answer pairs,
financial community QA pairs, personal-finance forum duplicates, financial FAQ
retrieval data, and domain QA data covering taxes, investments, retirement
accounts, banking, insurance, debt, and brokerage operations. Generic QA data is
helpful for question-answer matching, but the domain shift is large because
FiQA answers often include practical advice and opinionated reasoning.

Training should preferably exclude upstream dev/test data, BEIR-derived
evaluation records, and FiQA records likely to overlap with the NanoBEIR
evaluation queries or answers. When using public financial QA data, it is also
important to preserve question-answer direction: the positive is an explanatory
answer post, not a document merely mentioning the same financial product.

### Synthetic Data Guidance

For document-to-question generation, start from non-evaluation financial advice
answers and generate realistic user questions that the answer would satisfy.
Generated questions should mention concrete actions, account types, constraints,
and jurisdictions, such as selling shares, filing contractor taxes, taking an
employer match, filling checks, short selling, ETF rebalancing, or credit-card
debt repayment.

For joint document-and-question generation, create short community-style
financial answers with caveats and then generate questions that ask for the same
decision. The synthetic data should include multiple valid answers for some
questions, because the benchmark contains multi-positive qrels. Avoid generic
finance-definition pairs unless the answer actually resolves a user's practical
decision.

## Example Data

| Query | Positive document |
| --- | --- |
| What type of returns Vanguard is quoting? (41 chars) | "From the Vanguard page - This seemed the easiest one as S&P data is simple to find. I use MoneyChimp to get - which confirms that Vanguard's page is offering CAGR, not arithmetic Average. Note: Vanguard states ""For U.S. sto ... [truncated 225 chars](387 chars) |
| Freelancing Tax implication (27 chars) | If you have income in the US, you will owe US income tax on it, unless there is a treaty with your country that says otherwise. (127 chars) |
| What is considered high or low when talking about volume? (57 chars) | The daily Volume is usually compared to the average daily volume over the past 50 days for a stock. High volume is usually considered to be 2 or more times the average daily volume over the last 50 days for that stock, howeve ... [truncated 225 chars](684 chars) |
| Using credit card points to pay for tax deductible business expenses (68 chars) | "For simplicity, let's start by just considering cash back. In general, cash back from credit cards for personal use is not taxable, but for business use it is taxable (sort of, I'll explain later). The reason is most persona ... [truncated 225 chars](3496 chars) |
| How should I file my taxes as a contractor? (43 chars) | For tax purposes you will need to file as an employee (T4 slips and tax withheld automatically), but also as an entrepreneur. I had the same situation myself last year. Employee and self-employed is a publication from Revenue ... [truncated 225 chars](689 chars) |

## Dataset Information

| Field | Value |
| --- | --- |
| Nano set | NanoBEIR-en |
| Backing dataset | NanoBEIR-en |
| Task / split | NanoFiQA2018 |
| Hugging Face dataset | [hakari-bench/NanoBEIR-en](https://huggingface.co/datasets/hakari-bench/NanoBEIR-en) |
| Language | en |
| Category | natural_language |
| Queries | 50 |
| Documents | 4,598 |
| Positive qrels | 123 |
| Avg positives / query | 2.46 |
| Positives per query (min / median / max) | 1 / 2.00 / 15 |
| Queries with multiple positives | 28 (56.0%) |
| BM25 nDCG@10 | 0.3583 |
| BM25 hit@10 | 0.6400 |
| Query length avg chars | 58.52 |
| Document length avg chars | 899.63 |

### Public Sources

- [WWW'18 Open Challenge: Financial Opinion Mining and Question Answering](https://doi.org/10.1145/3184558.3192301); 2018; Macedo Maia, Siegfried Handschuh, Andre Freitas, Brian Davis, Ross McDermott, Manel Zarrouk, Alexandra Balahur; DOI: `10.1145/3184558.3192301`.
- [FiQA 2018 official challenge site](https://sites.google.com/view/fiqa/home).
- [BEIR: A Heterogeneous Benchmark for Zero-shot Evaluation of Information Retrieval Models](https://arxiv.org/abs/2104.08663); 2021; Nandan Thakur, Nils Reimers, Andreas Rueckle, Abhishek Srivastava, Iryna Gurevych; DOI: `10.48550/arXiv.2104.08663`.

### Hugging Face Links

- Nano dataset: [hakari-bench/NanoBEIR-en](https://huggingface.co/datasets/hakari-bench/NanoBEIR-en)
- Source collection: [Zeta Alpha NanoBEIR collection](https://huggingface.co/collections/zeta-alpha-ai/nanobeir)

### Source Reference Table

| Title | Year | Type | URL |
| --- | ---: | --- | --- |
| WWW'18 Open Challenge: Financial Opinion Mining and Question Answering | 2018 | paper | https://doi.org/10.1145/3184558.3192301 |
| FiQA 2018 official challenge site |  | project page | https://sites.google.com/view/fiqa/home |
| BEIR: A Heterogeneous Benchmark for Zero-shot Evaluation of Information Retrieval Models | 2021 | benchmark paper | https://arxiv.org/abs/2104.08663 |

## Machine-Readable Metadata

<!-- benchmark-task-metadata:v1 -->

```yaml
benchmark_task_metadata:
  schema_version: 1
  document_status: first_pass
  nano_set: NanoBEIR-en
  backing_dataset: NanoBEIR-en
  dataset_id: hakari-bench/NanoBEIR-en
  task_name: NanoFiQA2018
  split_name: NanoFiQA2018
  language: en
  category: natural_language
  document_path: docs/benchmark_tasks/NanoBEIR-en/NanoFiQA2018.md
  source_research:
    primary_source_type: task_paper
    paper_pdf_or_html_checked: true
    no_paper_note: null
  counts:
    queries: 50
    documents: 4598
    positive_qrels: 123
  positives_per_query:
    average: 2.46
    min: 1
    median: 2.0
    max: 15
    multi_positive_queries: 28
    multi_positive_query_percent: 56.0
  text_stats_chars:
    query_mean: 58.52
    document_mean: 899.632666
  bm25:
    ndcg_at_10: 0.358343363
    hit_at_10: 0.64
    source: dataset_bm25_column
  learning:
    original_train_split: available
    evaluation_split_origin: unknown
    train_eval_overlap_audit: not_audited
    leakage_note: prefer excluding upstream dev/test data or other FiQA/BEIR-derived records likely to overlap with the NanoBEIR evaluation questions and answers
    useful_training_data:
      - non-overlapping FiQA training question-answer pairs
      - financial community QA pairs
      - personal-finance forum and FAQ retrieval data
      - domain QA covering taxes, retirement accounts, brokerage, debt, and banking
    synthetic_data:
      document_generation: community-style financial answer posts with practical advice, caveats, account types, jurisdictions, and numeric assumptions
      question_generation: realistic personal-finance questions asking for decisions or explanations that the answer resolves
      answerability: positives should answer the financial decision or explanation need, not merely mention the same product
    multi_positive_training: multi_positive_objective
  links:
    nano_dataset: https://huggingface.co/datasets/hakari-bench/NanoBEIR-en
    source_urls:
      - label: FiQA 2018 official challenge site
        url: https://sites.google.com/view/fiqa/home
      - label: Zeta Alpha NanoBEIR collection
        url: https://huggingface.co/collections/zeta-alpha-ai/nanobeir
    source_notes:
      - no_arxiv_page_confirmed_for_original_task_paper
  references:
    - title: "WWW'18 Open Challenge: Financial Opinion Mining and Question Answering"
      url: https://doi.org/10.1145/3184558.3192301
      year: 2018
      doi: 10.1145/3184558.3192301
      is_paper: true
      source_confidence: definitive_paper_link
    - title: FiQA 2018 official challenge site
      url: https://sites.google.com/view/fiqa/home
      year: null
      doi: null
      is_paper: false
      source_confidence: definitive_project_page
    - title: 'BEIR: A Heterogeneous Benchmark for Zero-shot Evaluation of Information Retrieval Models'
      url: https://arxiv.org/abs/2104.08663
      year: 2021
      doi: 10.48550/arXiv.2104.08663
      is_paper: true
      source_confidence: benchmark_context_paper
```
