# NanoFaMTEB-v2 / treccovid_fa

## Overview

`treccovid_fa` is a Persian biomedical retrieval task based on TREC-COVID. The
query is a COVID-19 information need, and positive documents are biomedical
abstracts or article passages.

## Details

### What the Original Data Measures

[FaMTEB](https://arxiv.org/abs/2502.11571) includes translated BEIR-style
retrieval datasets as Persian evaluation resources. This split uses
`MCINext/trec-covid-fa-v2`, a Persian TREC-COVID retrieval variant, under the
MTEB retrieval framework from [MTEB](https://arxiv.org/abs/2210.07316).

### Observed Data Profile

The Nano split has 50 queries, 10,000 documents, and 4,623 positive qrels. It
is highly multi-positive, averaging 92.46 positives per query. Queries average
64.58 characters, while documents average 1,210.70 characters.

Observed queries ask about SARS-CoV-2 protein interactions and public COVID-19
datasets. Documents are Persian biomedical abstracts.

### BM25 Difficulty

Using the dataset-provided BM25 candidate column and best-ranked positive, BM25
reaches nDCG@10 = 0.9490 and hit@10 = 0.9800. It ranks 46 positives first.

The many-positive qrels and distinctive biomedical terminology make BM25 a very
strong baseline in this Nano split.

### Training Data That May Help

Helpful data includes Persian biomedical retrieval, TREC-COVID translations,
scientific abstract search, and COVID-19 literature QA. Exclude this split's
topics, qrels, and positive abstracts.

### Synthetic Data Guidance

Generate Persian biomedical information needs and abstract passages. Include
multiple relevant positives and hard negatives sharing COVID-19 terminology but
not the requested relation.

## Example Data

| Query | Positive document |
| --- | --- |
| چه شواهدی مبنی بر استفاده از دگزامتازون به عنوان درمان کووید-۱۹ وجود دارد؟ (74 chars) | بررسی نظام‌مند و آماری کارآزمایی‌های درمانی بیماری کووید-۱۹ این مرور سیستماتیک و متاآنالیز، داده‌های فعلی مربوط به کارآزمایی‌های بالینی کنترل‌شده انسانی برای درمان کووید-۱۹ را جمع‌آوری می‌کند. یک جستجوی الکترونیکی در منابع عل ... [truncated 225 chars](1536 chars) |
| ویروس کرونا چه مدت روی سطوح پایدار می‌ماند؟ (43 chars) | راهنمای کووید-۱۹: یک همه‌گیری جهانی ناشی از ویروس کرونای جدید SARS-CoV-2 ظهور سویه SARS-CoV-2 از کروناویروس انسانی، جهان را به میانه یک همه‌گیری جدید انداخته است. این ویروس در بدن انسان باعث بیماری کووید-۱۹ می‌شود، بیماری که ... [truncated 225 chars](975 chars) |
| آیا فاصله‌گذاری اجتماعی در کند کردن شیوع کووید-۱۹ تأثیر داشته است؟ (66 chars) | افزایش تشخیص همراه با فاصله‌گذاری اجتماعی و برنامه‌ریزی ظرفیت بهداشتی، بار موارد و مرگ‌ومیر ناشی از کووید-۱۹ را کاهش می‌دهد: یک مطالعه اثبات مفهوم با استفاده از مدل شبیه‌سازی محاسباتی تصادفی. هدف: در غیاب واکسن، همه‌گیری بیما ... [truncated 225 chars](1491 chars) |
| آیا آزمایش‌های سرولوژیکی برای تشخیص آنتی‌بادی‌های ویروس کرونا وجود دارد؟ (72 chars) | سرودیagnostics برای سندرم حاد تنفسی مرتبط با کرونا ویروس ۲: یک مرور روایی آزمایش‌های سرولوژیک دقیق برای تشخیص آنتی‌بادی‌های میزبان علیه ویروس کرونا مرتبط با سندرم تنفسی حاد شدید-۲ (SARS-CoV-2) برای پاسخ بهداشت عمومی به پاندمی ... [truncated 225 chars](1297 chars) |
| کدام نشانگرهای زیستی سیر بالینی شدید عفونت کووید-۱۹ را پیش‌بینی می‌کنند؟ (72 chars) | ویژگی‌های بالینی و عوامل پیش‌بینی‌کننده در بیماران مبتلا به پنومونی شدید ناشی از SARS-CoV-2: یک مطالعه کوهورت چندمرکزی گذشته‌نگر اهداف: این مطالعه با هدف بررسی ویژگی‌های بالینی بیماران مبتلا به پنومونی شدید ناشی از SARS-CoV-2 ... [truncated 225 chars](1387 chars) |

## Dataset Information

| Field | Value |
| --- | --- |
| Nano set | NanoFaMTEB-v2 |
| Backing dataset | NanoFaMTEB-v2 |
| Task / split | treccovid_fa |
| Hugging Face dataset | [hakari-bench/NanoFaMTEB-v2](https://huggingface.co/datasets/hakari-bench/NanoFaMTEB-v2) |
| Language | fa |
| Category | natural_language |
| Queries | 50 |
| Documents | 10000 |
| Positive qrels | 4623 |
| Positives per query | avg 92.46, min 14, median 100.0, max 100 |
| BM25 nDCG@10 | 0.9490 |
| BM25 hit@10 | 0.9800 |
| Query length avg chars | 64.58 |
| Document length avg chars | 1210.70 |

### Public Sources

- [FaMTEB: Massive Text Embedding Benchmark in Persian Language](https://arxiv.org/abs/2502.11571).
- [MTEB: Massive Text Embedding Benchmark](https://arxiv.org/abs/2210.07316).
- [MCINext/trec-covid-fa-v2 dataset card](https://huggingface.co/datasets/MCINext/trec-covid-fa-v2).

### Hugging Face Links

- Nano dataset: [hakari-bench/NanoFaMTEB-v2](https://huggingface.co/datasets/hakari-bench/NanoFaMTEB-v2)
- Source dataset: [MCINext/trec-covid-fa-v2](https://huggingface.co/datasets/MCINext/trec-covid-fa-v2)

### Source Reference Table

| Title | Year | Type | URL |
| --- | ---: | --- | --- |
| FaMTEB: Massive Text Embedding Benchmark in Persian Language | 2025 | arXiv paper | https://arxiv.org/abs/2502.11571 |
| MTEB: Massive Text Embedding Benchmark | 2023 | arXiv paper | https://arxiv.org/abs/2210.07316 |
| MCINext/trec-covid-fa-v2 | 2025 | dataset card | https://huggingface.co/datasets/MCINext/trec-covid-fa-v2 |

## Machine-Readable Metadata

<!-- benchmark-task-metadata:v1 -->

```yaml
benchmark_task_metadata:
  schema_version: 1
  document_status: first_pass
  nano_set: NanoFaMTEB-v2
  backing_dataset: NanoFaMTEB-v2
  dataset_id: hakari-bench/NanoFaMTEB-v2
  task_name: treccovid_fa
  split_name: treccovid_fa
  language: fa
  category: natural_language
  document_path: docs/benchmark_tasks/NanoFaMTEB-v2/treccovid_fa.md
  source_research:
    primary_source_type: benchmark_paper
    paper_pdf_or_html_checked: true
  counts:
    queries: 50
    documents: 10000
    positive_qrels: 4623
  positives_per_query:
    average: 92.46
    min: 14
    median: 100.0
    max: 100
    multi_positive_queries: 50
  text_stats_chars:
    query_mean: 64.58
    document_mean: 1210.7024
  bm25:
    ndcg_at_10: 0.949
    hit_at_10: 0.98
    source: dataset_bm25_column
  links:
    nano_dataset: https://huggingface.co/datasets/hakari-bench/NanoFaMTEB-v2
    source_urls:
      - label: FaMTEB arXiv
        url: https://arxiv.org/abs/2502.11571
      - label: MCINext/trec-covid-fa-v2
        url: https://huggingface.co/datasets/MCINext/trec-covid-fa-v2
  references:
    - title: "FaMTEB: Massive Text Embedding Benchmark in Persian Language"
      url: https://arxiv.org/abs/2502.11571
      year: 2025
      is_paper: true
```
