# NanoFaMTEB-v2 / web_faq_fas

## Overview

`web_faq_fas` is a Persian WebFAQ retrieval task. Queries are FAQ-style questions,
and positive documents are answer passages from FAQ pages.

## Details

### What the Original Data Measures

[FaMTEB](https://arxiv.org/abs/2502.11571) includes web and RAG-style retrieval
datasets for Persian embedding evaluation. The source metadata describes
`mteb/WebFAQRetrieval` as broad-coverage natural question-answer pairs gathered
from FAQ pages in many languages. [MTEB](https://arxiv.org/abs/2210.07316)
provides the common evaluation framework.

### Observed Data Profile

The Nano split has 200 queries, 10,000 documents, and 200 positive qrels. Queries
average 48.01 characters and documents average 209.60 characters. Every query
has one positive.

Observed examples ask about games, security labels, and practical definitions.
Documents are direct FAQ answers.

### BM25 Difficulty

Using the dataset-provided BM25 candidate column, BM25 reaches nDCG@10 = 0.8680
and hit@10 = 0.9350. It ranks 160 positives first.

FAQ question-answer pairs often share key terms, so lexical retrieval is strong.

### Training Data That May Help

Helpful data includes Persian FAQ retrieval, web question-answer pairs, and
customer-support knowledge-base retrieval. Exclude evaluation rows.

### Synthetic Data Guidance

Generate Persian FAQ questions and answer snippets. Include hard negatives from
the same product, topic, or definition family.

## Example Data

| Query | Positive document |
| --- | --- |
| آیا عمل لیپوماتیک با درد و خونریزی همراه است؟ (45 chars) | در عمل لیپوماتیک سوراخ های کوچکی ایجاد می‌شود. سپس لوله مخصوصی به زیر پوست برده می‌شود تا چربی‌ها را بیرون بکشد. این برش‌ها، به طول ۲ تا ۵ میلی‌متر خواهند بود و درد و خونریزی بسیار کمی در پی دارند و خطر عفونت را بسیار کاهش می ... [truncated 225 chars](231 chars) |
| نوزاد تا چه فاصله ای را می بیند؟ (32 chars) | بدیهی است نوزادی که تازه به دنیا آمده شما را با حس بینایی تشخیص نمی‌دهد، زیرا این اولین نگاه او به چهره شما است. نوزادان تازه متولد شده فقط می‌توانند تا فاصله حدود ۳۰ سانتی‌متری را ببینند. این بهترین فاصله‌ بین چشمان او و صور ... [truncated 225 chars](267 chars) |
| آیا همه افراد جامعه با استعداد هستند؟ (37 chars) | پاسخ به این سوال که آیا همه افراد جامعه با استعداد هستند کاملا مثبت بوده و با کشف موضوعات مورد علاقه افراد خواهید دید که چه پیشرفت هایی را در زمینه های مختلف کسب خواهند کرد. هر کدام از ما انسان ها در درون خود استعدادهایی را د ... [truncated 225 chars](507 chars) |
| مرکز خدمات حیوانات آزمایشگاهی جهت خونگیری را معرفی کنید (55 chars) | شما میتوانید انجام امور خدمات مرتبط با آزمایشگاه حیوانات آزمایشگاهی را به شرکت بافت و ژن پاسارگاد (هیستوژن ) برون سپاری کنید (124 chars) |
| آیا تنظیمات استارتاپ ویندوز هشت و ده متفاوت است؟ (48 chars) | تنظیمات Advanced Startup Options ویندوز هشت و ویندوز ده تقریبا مشابه است و تفاوت زیادی با همدیگر ندارند ، مگر برخی امکانات ریکاوری کل ویندوز و بحث Reset و Refresh کردن که شاید کمی متفاوت عمل کنند اما در کل یکسان هستند (217 chars) |

## Dataset Information

| Field | Value |
| --- | --- |
| Nano set | NanoFaMTEB-v2 |
| Backing dataset | NanoFaMTEB-v2 |
| Task / split | web_faq_fas |
| Hugging Face dataset | [hakari-bench/NanoFaMTEB-v2](https://huggingface.co/datasets/hakari-bench/NanoFaMTEB-v2) |
| Language | fa |
| Category | natural_language |
| Queries | 200 |
| Documents | 10000 |
| Positive qrels | 200 |
| BM25 nDCG@10 | 0.8680 |
| BM25 hit@10 | 0.9350 |
| Query length avg chars | 48.01 |
| Document length avg chars | 209.60 |

### Public Sources

- [FaMTEB: Massive Text Embedding Benchmark in Persian Language](https://arxiv.org/abs/2502.11571).
- [MTEB: Massive Text Embedding Benchmark](https://arxiv.org/abs/2210.07316).
- [mteb/WebFAQRetrieval dataset card](https://huggingface.co/datasets/mteb/WebFAQRetrieval).
- [PaDaS Lab Hugging Face organization](https://huggingface.co/PaDaS-Lab).

### Hugging Face Links

- Nano dataset: [hakari-bench/NanoFaMTEB-v2](https://huggingface.co/datasets/hakari-bench/NanoFaMTEB-v2)
- Source dataset: [mteb/WebFAQRetrieval](https://huggingface.co/datasets/mteb/WebFAQRetrieval)

### Source Reference Table

| Title | Year | Type | URL |
| --- | ---: | --- | --- |
| FaMTEB: Massive Text Embedding Benchmark in Persian Language | 2025 | arXiv paper | https://arxiv.org/abs/2502.11571 |
| MTEB: Massive Text Embedding Benchmark | 2023 | arXiv paper | https://arxiv.org/abs/2210.07316 |
| mteb/WebFAQRetrieval | 2024 | dataset card | https://huggingface.co/datasets/mteb/WebFAQRetrieval |

## Machine-Readable Metadata

<!-- benchmark-task-metadata:v1 -->

```yaml
benchmark_task_metadata:
  schema_version: 1
  document_status: first_pass
  nano_set: NanoFaMTEB-v2
  backing_dataset: NanoFaMTEB-v2
  dataset_id: hakari-bench/NanoFaMTEB-v2
  task_name: web_faq_fas
  split_name: web_faq_fas
  language: fa
  category: natural_language
  document_path: docs/benchmark_tasks/NanoFaMTEB-v2/web_faq_fas.md
  source_research:
    primary_source_type: benchmark_paper
    paper_pdf_or_html_checked: true
  counts:
    queries: 200
    documents: 10000
    positive_qrels: 200
  positives_per_query:
    average: 1.0
    min: 1
    median: 1.0
    max: 1
    multi_positive_queries: 0
  text_stats_chars:
    query_mean: 48.005
    document_mean: 209.6025
  bm25:
    ndcg_at_10: 0.868
    hit_at_10: 0.935
    source: dataset_bm25_column
  links:
    nano_dataset: https://huggingface.co/datasets/hakari-bench/NanoFaMTEB-v2
    source_urls:
      - label: FaMTEB arXiv
        url: https://arxiv.org/abs/2502.11571
      - label: mteb/WebFAQRetrieval
        url: https://huggingface.co/datasets/mteb/WebFAQRetrieval
  references:
    - title: "FaMTEB: Massive Text Embedding Benchmark in Persian Language"
      url: https://arxiv.org/abs/2502.11571
      year: 2025
      is_paper: true
```
