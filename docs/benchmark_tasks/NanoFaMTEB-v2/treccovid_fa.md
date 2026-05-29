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
| BM25 nDCG@10 | 0.3519 |
| BM25 hit@10 | 0.8800 |
| BM25 Recall@100 | 0.2029 |
| BM25 candidate subset | top-500 (`bm25`) |
| Dense nDCG@10 | 0.3594 |
| Dense hit@10 | 0.9000 |
| Dense Recall@100 | 0.2379 |
| Dense candidate subset | top-500 (`harrier_oss_v1_270m`) |
| Reranking hybrid nDCG@10 | 0.4161 |
| Reranking hybrid hit@10 | 0.9400 |
| Reranking hybrid Recall@100 | 0.2557 |
| Reranking hybrid candidate subset | top-100 plus optional rank-101 safeguard (`reranking_hybrid`) |
| Reranking hybrid candidates / query | 100 |
| Reranking hybrid safeguard rows | 0 |
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
    ndcg_at_10: 0.3519444257263538
    hit_at_10: 0.88
    source: dataset_candidate_subset
  links:
    nano_dataset: https://huggingface.co/datasets/hakari-bench/NanoFaMTEB-v2
    source_urls:
    - label: FaMTEB arXiv
      url: https://arxiv.org/abs/2502.11571
    - label: MCINext/trec-covid-fa-v2
      url: https://huggingface.co/datasets/MCINext/trec-covid-fa-v2
  references:
  - title: 'FaMTEB: Massive Text Embedding Benchmark in Persian Language'
    url: https://arxiv.org/abs/2502.11571
    year: 2025
    is_paper: true
  candidate_subsets:
    bm25:
      config: bm25
      label: BM25
      source: dataset_candidate_subset
      top_k: 500
      ndcg_at_10: 0.3519444257
      hit_at_10: 0.88
      recall_at_100: 0.2028985507
      candidate_count_min: 500
      candidate_count_max: 500
      candidate_count_mean: 500.0
      query_count: 50
      query_coverage: 1.0
      relevant_coverage_at_100: 0.2028985507
    dense:
      config: harrier_oss_v1_270m
      label: Dense
      source: dataset_candidate_subset
      top_k: 500
      ndcg_at_10: 0.3593859725
      hit_at_10: 0.9
      recall_at_100: 0.2379407311
      candidate_count_min: 500
      candidate_count_max: 500
      candidate_count_mean: 500.0
      query_count: 50
      query_coverage: 1.0
      relevant_coverage_at_100: 0.2379407311
    reranking_hybrid:
      config: reranking_hybrid
      label: Reranking hybrid
      source: dataset_candidate_subset
      top_k: 100
      ndcg_at_10: 0.4161435188
      hit_at_10: 0.94
      recall_at_100: 0.2556781311
      candidate_count_min: 100
      candidate_count_max: 100
      candidate_count_mean: 100.0
      query_count: 50
      query_coverage: 1.0
      relevant_coverage_at_100: 0.2556781311
      safeguard_positive_rows: 0
      rows_with_101_candidates: 0
```
