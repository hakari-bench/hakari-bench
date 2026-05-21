# NanoLaw / NanoLegalBenchConsumerContractsQA

## Overview

`NanoLegalBenchConsumerContractsQA` is an English legal retrieval task derived
from LegalBench consumer-contract QA. Queries are yes/no questions about online
terms of service, and documents are contract clauses or sections that answer
the question.

## Details

### What the Original Data Measures

[LegalBench: A Collaboratively Built Benchmark for Measuring Legal Reasoning in Large Language Models](https://arxiv.org/abs/2308.11462)
places `consumer_contracts_qa` in its interpretation tasks. The paper says the
task was first introduced by Noam Kolt and asks whether a model can understand
consumer contracts, especially terms of service. It describes 200 yes/no legal
questions plus alternatively worded versions, covering issues such as
eligibility, payments, liability limits, intellectual property, and dispute
resolution.

The [LegalBench task page](https://hazyresearch.stanford.edu/legalbench/tasks/consumer_contracts_qa.html)
lists 400 samples, the legal reasoning type as interpretation, and the task type
as yes/no question-answering. The page points to the Berkeley Technology Law
Journal article [Predicting Consumer Contracts](https://papers.ssrn.com/sol3/papers.cfm?abstract_id=3844988)
for the original dataset construction.

### Observed Data Profile

The Nano split has 200 queries, 153 documents, and 200 positive qrels. Each
query has exactly one positive document. Queries average 97.22 characters and
are direct legal questions such as whether a service may charge fees, translate
listings, require information, or help with copyright infringement. Documents
average 2,743.33 characters and are terms-of-service sections from services
such as Google, Verizon, Disney, eBay, and Reddit.

### BM25 Difficulty

Using the dataset-provided BM25 candidate column, BM25 reaches nDCG@10 =
0.6453 and hit@10 = 0.8400. It ranks a positive first for 93 queries. Lexical
signals are often strong because questions reuse product names and legal
concepts from the clauses, but some examples require interpreting permissions,
exceptions, or obligations rather than matching a single phrase.

### Training Data That May Help

Useful training data includes non-overlapping consumer-contract QA, contract
clause retrieval, terms-of-service entailment, and hard negatives from the same
service but different rights or obligations.

### Synthetic Data Guidance

Generate yes/no questions over realistic terms-of-service clauses. Positives
should contain the exact clause needed to answer the question; hard negatives
should come from the same provider or topic while answering a different legal
issue.

## Example Data

| Query | Positive document |
| --- | --- |
| Does data sharing (including sharing of user data) take place between and among Instagram and Facebook? (103 chars) | Welcome to Instagram! These Terms of Use (or Terms) govern your use of Instagram, except where we expressly state that separate terms (and not these) apply, and provide information about the Instagram Service (the Service), o ... [truncated 225 chars](4112 chars) |
| Is it possible that Ill have to pay money for the services? (59 chars) | Using the Services Authority. You agree that you are permitted to use the Services under applicable law. If you are using the Services on behalf of a company, business or other entity, you represent that you have the legal au ... [truncated 225 chars](7928 chars) |
| Do minors require parental permission in order to access Youtubes services? (75 chars) | Introduction Thank you for using the YouTube platform and the products, services and features we make available to you as part of the platform (collectively, the Service). Our Service The Service allows you to discover, watch ... [truncated 225 chars](2811 chars) |
| Can I use a program to automatically scrape video data from Youtube? (68 chars) | Content on the Service The content on the Service includes videos, audio (for example music and other sounds), graphics, photos, text (such as comments and scripts), branding (including trade names, trademarks, service marks, ... [truncated 225 chars](6181 chars) |
| By default, does eBay prohibit transfers of eBay accounts? (58 chars) | In connection with using or accessing our Services you will not: post, list or upload content or items in inappropriate categories or areas on our sites; breach or circumvent any laws, regulations, third-party rights or our s ... [truncated 225 chars](4566 chars) |

## Dataset Information

| Field | Value |
| --- | --- |
| Nano set | NanoLaw |
| Backing dataset | NanoLaw |
| Task / split | NanoLegalBenchConsumerContractsQA |
| Hugging Face dataset | [hakari-bench/NanoLaw](https://huggingface.co/datasets/hakari-bench/NanoLaw) |
| Language | en |
| Category | natural_language |
| Queries | 200 |
| Documents | 153 |
| Positive qrels | 200 |
| BM25 nDCG@10 | 0.6453 |
| BM25 hit@10 | 0.8400 |
| Query length avg chars | 97.22 |
| Document length avg chars | 2743.33 |

### Public Sources

- [LegalBench: A Collaboratively Built Benchmark for Measuring Legal Reasoning in Large Language Models](https://arxiv.org/abs/2308.11462); 2023; Neel Guha et al.
- [consumer_contracts_qa LegalBench task page](https://hazyresearch.stanford.edu/legalbench/tasks/consumer_contracts_qa.html).
- [Predicting Consumer Contracts](https://papers.ssrn.com/sol3/papers.cfm?abstract_id=3844988); 2022; Noam Kolt.

### Hugging Face Links

- Nano dataset: [hakari-bench/NanoLaw](https://huggingface.co/datasets/hakari-bench/NanoLaw)
- Source dataset: [mteb/legalbench_consumer_contracts_qa](https://huggingface.co/datasets/mteb/legalbench_consumer_contracts_qa)

### Source Reference Table

| Title | Year | Type | URL |
| --- | ---: | --- | --- |
| LegalBench: A Collaboratively Built Benchmark for Measuring Legal Reasoning in Large Language Models | 2023 | arXiv paper | https://arxiv.org/abs/2308.11462 |
| consumer_contracts_qa | 2023 | LegalBench task page | https://hazyresearch.stanford.edu/legalbench/tasks/consumer_contracts_qa.html |
| Predicting Consumer Contracts | 2022 | law review article | https://papers.ssrn.com/sol3/papers.cfm?abstract_id=3844988 |

## Machine-Readable Metadata

<!-- benchmark-task-metadata:v1 -->

```yaml
benchmark_task_metadata:
  schema_version: 1
  document_status: first_pass
  nano_set: NanoLaw
  backing_dataset: NanoLaw
  dataset_id: hakari-bench/NanoLaw
  task_name: NanoLegalBenchConsumerContractsQA
  split_name: NanoLegalBenchConsumerContractsQA
  language: en
  category: natural_language
  document_path: docs/benchmark_tasks/NanoLaw/NanoLegalBenchConsumerContractsQA.md
  source_research:
    primary_source_type: benchmark_paper_and_task_page
    paper_pdf_or_html_checked: true
    no_paper_note: null
  counts:
    queries: 200
    documents: 153
    positive_qrels: 200
  positives_per_query:
    average: 1.0
    min: 1
    median: 1.0
    max: 1
    multi_positive_queries: 0
    multi_positive_query_percent: 0.0
  text_stats_chars:
    query_mean: 97.225
    document_mean: 2743.326797385621
  bm25:
    ndcg_at_10: 0.6453269540326203
    hit_at_10: 0.84
    source: dataset_bm25_column
  learning:
    original_train_split: available
    evaluation_split_origin: legalbench_consumer_contracts_qa
    train_eval_overlap_audit: not_audited
    leakage_note: exclude NanoLegalBenchConsumerContractsQA questions, qrels, and positive contract clauses
    useful_training_data:
      - consumer-contract QA
      - terms-of-service clause retrieval
      - contract entailment over rights and obligations
      - same-provider hard negatives
    synthetic_data:
      document_generation: terms-of-service clauses with permissions, duties, exceptions, and remedies
      question_generation: yes/no consumer questions about contractual rights or obligations
      answerability: positives should contain the clause needed to answer the question
    multi_positive_training: single_positive
  links:
    nano_dataset: https://huggingface.co/datasets/hakari-bench/NanoLaw
    source_urls:
      - label: LegalBench arXiv
        url: https://arxiv.org/abs/2308.11462
      - label: LegalBench task page
        url: https://hazyresearch.stanford.edu/legalbench/tasks/consumer_contracts_qa.html
      - label: MTEB legalbench_consumer_contracts_qa
        url: https://huggingface.co/datasets/mteb/legalbench_consumer_contracts_qa
    source_notes: []
  references:
    - title: "LegalBench: A Collaboratively Built Benchmark for Measuring Legal Reasoning in Large Language Models"
      url: https://arxiv.org/abs/2308.11462
      year: 2023
      doi: 10.48550/arXiv.2308.11462
      is_paper: true
      source_confidence: definitive_paper_link
```
