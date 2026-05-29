# NanoFaMTEB-v2 / scidocs_fa

## Overview

`scidocs_fa` is a Persian scientific document retrieval task. Queries are paper
titles or scientific text snippets, and positives are related scientific
documents.

## Details

### What the Original Data Measures

[FaMTEB](https://arxiv.org/abs/2502.11571) includes translated scientific
retrieval datasets as part of the Persian MTEB suite. This split uses
`MCINext/scidocs-fa-v2`, a Persian SCIDOCS variant, within the common retrieval
framework from [MTEB](https://arxiv.org/abs/2210.07316).

### Observed Data Profile

The split has 200 queries, 10,000 documents, and 986 positive qrels. Queries
average 61.56 characters and documents average 1,092.04 characters. Each query
has 3 to 5 positives, averaging 4.93.

Observed examples are scientific paper titles in Persian, with related abstracts
or paper summaries as positives.

### BM25 Difficulty

Using the dataset-provided BM25 candidate column and best-ranked positive, BM25
reaches nDCG@10 = 0.3664 and hit@10 = 0.5650. It ranks 36 positives first.

Lexical matching is weaker than in entity-centric QA because related papers may
share concepts without repeating exact title terms.

### Training Data That May Help

Helpful data includes citation recommendation, scientific title-to-abstract
retrieval, Persian academic search, and translated SCIDOCS pairs. Exclude
evaluation paper IDs and qrels.

### Synthetic Data Guidance

Generate Persian scientific titles and abstracts across fields. Positives should
be conceptually related papers; hard negatives should use similar terminology
from a different method or application.

## Example Data

| Query | Positive document |
| --- | --- |
| چارچوبی یکپارچه برای استخراج داده از فایل‌های گزارش سیستم‌های محاسباتی جهت مدیریت سیستم (87 chars) | یادگیری ماشین در دسته‌بندی خودکار متن دسته‌بندی خودکار (یا طبقه‌بندی) متون به دسته‌های از پیش تعریف‌شده، در ۱۰ سال گذشته با افزایش علاقه مواجه شده است، به دلیل افزایش در دسترس بودن اسناد به صورت دیجیتال و نیاز ناشی از آن برای ... [truncated 225 chars](925 chars) |
| نقشهٔ ارتباط موضوعی: تجسم برای بهبود درک نتایج جستجو (52 chars) | طراحی برای جستجوی اکتشافی بر روی دستگاه‌های لمسی جستجوی اکتشافی کاربران را با چالش‌هایی در بیان مقاصد جستجو مواجه می‌کند، زیرا رابط‌های جستجوی فعلی نیازمند بررسی فهرست نتایج برای شناسایی مسیرهای جستجو، تایپ تکراری و بازنویسی ... [truncated 225 chars](1191 chars) |
| ریزه‌کاری‌های الگوریتمی در تحویل محتوا (38 chars) | هشینگ سازگار و درخت‌های تصادفی: پروتکل‌های ذخیره‌سازی توزیع‌شده برای کاهش نقاط داغ در وب جهان‌گستر ما مجموعه‌ای از پروتکل‌های حافظه پنهان برای شبکه‌های توزیع‌شده را توصیف می‌کنیم که می‌توانند برای کاهش یا حذف نقاط داغ در شبکه ... [truncated 225 chars](1200 chars) |
| رویکرد فعال‌گرایانه به تجربه معماری: یک دیدگاه نورفیزیولوژیکی در مورد تجسم، انگیزش و امکانات رفتاری (99 chars) | نتایج عاطفی درمان مواجهه با واقعیت مجازی برای اضطراب و فوبیاهای خاص: یک متاآنالیز. درمان مواجهه با واقعیت مجازی (VRET) به طور فزاینده‌ای به عنوان یک روش درمانی رایج برای اضطراب و فوبیاهای خاص مورد استفاده قرار می‌گیرد. با این ... [truncated 225 chars](816 chars) |
| کنترل PD با جبران‌سازی گرانش آنلاین برای ربات‌هایی با مفاصل ارتجاعی: تئوری و آزمایش‌ها (86 chars) | یک کنترل‌گر امپدانس کارتزینی مبتنی بر پسیویتی برای ربات‌های مفصلی انعطاف‌پذیر - قسمت اول: بازخورد گشتاور و جبران گرانش در این مقاله، یک رویکرد نوین به مسئله کنترل امپدانس کارتزین برای ربات‌هایی با مفاصل انعطاف‌پذیر ارائه می‌ش ... [truncated 225 chars](700 chars) |

## Dataset Information

| Field | Value |
| --- | --- |
| Nano set | NanoFaMTEB-v2 |
| Backing dataset | NanoFaMTEB-v2 |
| Task / split | scidocs_fa |
| Hugging Face dataset | [hakari-bench/NanoFaMTEB-v2](https://huggingface.co/datasets/hakari-bench/NanoFaMTEB-v2) |
| Language | fa |
| Category | natural_language |
| Queries | 200 |
| Documents | 10000 |
| Positive qrels | 986 |
| Positives per query | avg 4.93, min 3, median 5.0, max 5 |
| BM25 nDCG@10 | 0.1745 |
| BM25 hit@10 | 0.5650 |
| BM25 Recall@100 | 0.3925 |
| BM25 candidate subset | top-500 (`bm25`) |
| Dense nDCG@10 | 0.1937 |
| Dense hit@10 | 0.5800 |
| Dense Recall@100 | 0.4209 |
| Dense candidate subset | top-500 (`harrier_oss_v1_270m`) |
| Reranking hybrid nDCG@10 | 0.2143 |
| Reranking hybrid hit@10 | 0.6400 |
| Reranking hybrid Recall@100 | 0.4371 |
| Reranking hybrid candidate subset | top-100 plus optional rank-101 safeguard (`reranking_hybrid`) |
| Reranking hybrid candidates / query | 100-101 |
| Reranking hybrid safeguard rows | 25 |
| Query length avg chars | 61.56 |
| Document length avg chars | 1092.04 |

### Public Sources

- [FaMTEB: Massive Text Embedding Benchmark in Persian Language](https://arxiv.org/abs/2502.11571).
- [MTEB: Massive Text Embedding Benchmark](https://arxiv.org/abs/2210.07316).
- [MCINext/scidocs-fa-v2 dataset card](https://huggingface.co/datasets/MCINext/scidocs-fa-v2).

### Hugging Face Links

- Nano dataset: [hakari-bench/NanoFaMTEB-v2](https://huggingface.co/datasets/hakari-bench/NanoFaMTEB-v2)
- Source dataset: [MCINext/scidocs-fa-v2](https://huggingface.co/datasets/MCINext/scidocs-fa-v2)

### Source Reference Table

| Title | Year | Type | URL |
| --- | ---: | --- | --- |
| FaMTEB: Massive Text Embedding Benchmark in Persian Language | 2025 | arXiv paper | https://arxiv.org/abs/2502.11571 |
| MTEB: Massive Text Embedding Benchmark | 2023 | arXiv paper | https://arxiv.org/abs/2210.07316 |
| MCINext/scidocs-fa-v2 | 2025 | dataset card | https://huggingface.co/datasets/MCINext/scidocs-fa-v2 |

## Machine-Readable Metadata

<!-- benchmark-task-metadata:v1 -->

```yaml
benchmark_task_metadata:
  schema_version: 1
  document_status: first_pass
  nano_set: NanoFaMTEB-v2
  backing_dataset: NanoFaMTEB-v2
  dataset_id: hakari-bench/NanoFaMTEB-v2
  task_name: scidocs_fa
  split_name: scidocs_fa
  language: fa
  category: natural_language
  document_path: docs/benchmark_tasks/NanoFaMTEB-v2/scidocs_fa.md
  source_research:
    primary_source_type: benchmark_paper
    paper_pdf_or_html_checked: true
  counts:
    queries: 200
    documents: 10000
    positive_qrels: 986
  positives_per_query:
    average: 4.93
    min: 3
    median: 5.0
    max: 5
    multi_positive_queries: 200
  text_stats_chars:
    query_mean: 61.565
    document_mean: 1092.0389
  bm25:
    ndcg_at_10: 0.1745265642994616
    hit_at_10: 0.565
    source: dataset_candidate_subset
  links:
    nano_dataset: https://huggingface.co/datasets/hakari-bench/NanoFaMTEB-v2
    source_urls:
    - label: FaMTEB arXiv
      url: https://arxiv.org/abs/2502.11571
    - label: MCINext/scidocs-fa-v2
      url: https://huggingface.co/datasets/MCINext/scidocs-fa-v2
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
      ndcg_at_10: 0.1745265643
      hit_at_10: 0.565
      recall_at_100: 0.392494929
      candidate_count_min: 500
      candidate_count_max: 500
      candidate_count_mean: 500.0
      query_count: 200
      query_coverage: 1.0
      relevant_coverage_at_100: 0.392494929
    dense:
      config: harrier_oss_v1_270m
      label: Dense
      source: dataset_candidate_subset
      top_k: 500
      ndcg_at_10: 0.1937141038
      hit_at_10: 0.58
      recall_at_100: 0.4208924949
      candidate_count_min: 500
      candidate_count_max: 500
      candidate_count_mean: 500.0
      query_count: 200
      query_coverage: 1.0
      relevant_coverage_at_100: 0.4208924949
    reranking_hybrid:
      config: reranking_hybrid
      label: Reranking hybrid
      source: dataset_candidate_subset
      top_k: 100
      ndcg_at_10: 0.214305666
      hit_at_10: 0.64
      recall_at_100: 0.4371196755
      candidate_count_min: 100
      candidate_count_max: 101
      candidate_count_mean: 100.125
      query_count: 200
      query_coverage: 1.0
      relevant_coverage_at_100: 0.4371196755
      safeguard_positive_rows: 25
      rows_with_101_candidates: 25
```
