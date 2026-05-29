# NanoFaMTEB-v2 / sci_fact_fa

## Overview

`sci_fact_fa` is a Persian scientific claim-evidence retrieval task. The query
is a scientific claim, and positive documents are scientific abstracts or paper
snippets that provide evidence.

## Details

### What the Original Data Measures

[FaMTEB](https://arxiv.org/abs/2502.11571) includes translated BEIR-style
retrieval tasks, including scientific evidence retrieval. This split uses
`MCINext/scifact-fa-v2`, a Persian SciFact variant, within the MTEB retrieval
setup from [MTEB](https://arxiv.org/abs/2210.07316).

### Observed Data Profile

The split has 200 queries, 5,183 documents, and 225 positive qrels. Queries
average 84.49 characters and documents average 1,361.31 characters. Most
queries have one positive, but some have up to 5.

Observed examples include biomedical claims about NOX2, peroxynitrite, and
Helicobacter pylori. Documents are longer scientific abstracts in Persian.

### BM25 Difficulty

Using the dataset-provided BM25 candidate column and best-ranked positive, BM25
reaches nDCG@10 = 0.6374 and hit@10 = 0.7900. It ranks 99 positives first.

Scientific terminology gives BM25 strong anchors, but some evidence requires
matching claim semantics rather than exact words.

### Training Data That May Help

Helpful data includes Persian scientific claim verification, translated SciFact,
biomedical abstract retrieval, and evidence sentence retrieval. Exclude
NanoFaMTEB-v2 evaluation claims and abstracts.

### Synthetic Data Guidance

Generate Persian scientific claims from abstracts and pair them with evidence
documents. Hard negatives should share biomedical terms but support a different
claim or contradict the query.

## Example Data

| Query | Positive document |
| --- | --- |
| موش‌هایی که نقص در پلی‌مراز I دی‌ان‌ای (polI) دارند، حساسیت بیشتری به اشعه‌ی یونیزان (IR) نشان می‌دهند. (103 chars) | عملکردهای غیرهمپوشانِ پلیمرازهای DNA مو، لامبدا و ترمینال دئوکسی‌نوکلئوتیدیل‌ترانسفراز در بازترکیب V(D)J ایمونوگلوبولین در شرایط زنده. پلی‌مرازهای DNA مو (pol mu)، لامبدا (pol lambda) و ترمینال دئوکسی‌نوکلئوتیدیل‌ترانسفراز (T ... [truncated 225 chars](1153 chars) |
| پروتئین واکنشی سی (CRP) نمی‌تواند مرگ و میر پس از عمل جراحی بای‌پس عروق کرونر (CABG) را پیش‌بینی کند. (101 chars) | ارزیابی مقرون‌به‌صرفه بودن استفاده از نشانگرهای پیش‌آگاهی در مدل‌های تصمیم‌گیری: مطالعه موردی در اولویت‌بندی بیماران در انتظار جراحی عروق کرونر هدف: تعیین اثربخشی و مقرون به صرفه بودن استفاده از اطلاعات بیومارکرهای در گردش بر ... [truncated 225 chars](2564 chars) |
| آرژینین ۹۰ در p150n برای برهم‌کنش با EB1 مهم است. (49 chars) | مبنای ساختاری فعال‌سازی مونتاژ میکروتوبول توسط کمپلکس EB1 و p150Glued. پروتئین‌های ردیاب انتهای مثبت، مانند EB1 و کمپلکس داینین/دایناکتین، پویایی میکروتوبول‌ها را تنظیم می‌کنند. تصور می‌شود این پروتئین‌ها با تشکیل یک کمپلکس ا ... [truncated 225 chars](1181 chars) |
| اشغال ریبوزوم‌ها توسط RNAهای غیرکدکننده منجر به تولید پپتیدهای عملکردی نمی‌شود. (79 chars) | پروفایل‌بندی ریبوزوم شواهدی ارائه می‌دهد مبنی بر اینکه آر‌ان‌ای‌های غیرکدشونده بزرگ، پروتئین کد نمی‌کنند. RNAهای غیرکدکننده بزرگ به عنوان یک جزء مهم در تنظیم سلولی در حال ظهور هستند. شواهد قابل توجهی نشان می‌دهد که این رونوشت ... [truncated 225 chars](1163 chars) |
| تشنج‌های تب‌دار آستانه بروز صرع را افزایش می‌دهند. (50 chars) | تشنج‌های تب‌دار در مغز در حال رشد، منجر به تغییرات پایدار در تحریک‌پذیری نورونی در مدارهای لیمبیک می‌شوند. تشنج‌های تب‌دار ۳ تا ۵ درصد از نوزادان و کودکان خردسال را تحت تأثیر قرار می‌دهند. با وجود شیوع بالای تشنج‌های تب‌دار، ... [truncated 225 chars](685 chars) |

## Dataset Information

| Field | Value |
| --- | --- |
| Nano set | NanoFaMTEB-v2 |
| Backing dataset | NanoFaMTEB-v2 |
| Task / split | sci_fact_fa |
| Hugging Face dataset | [hakari-bench/NanoFaMTEB-v2](https://huggingface.co/datasets/hakari-bench/NanoFaMTEB-v2) |
| Language | fa |
| Category | natural_language |
| Queries | 200 |
| Documents | 5183 |
| Positive qrels | 225 |
| Positives per query | avg 1.12, min 1, median 1.0, max 5 |
| BM25 nDCG@10 | 0.6294 |
| BM25 hit@10 | 0.7900 |
| BM25 Recall@100 | 0.9022 |
| BM25 candidate subset | top-500 (`bm25`) |
| Dense nDCG@10 | 0.5610 |
| Dense hit@10 | 0.7000 |
| Dense Recall@100 | 0.8578 |
| Dense candidate subset | top-500 (`harrier_oss_v1_270m`) |
| Reranking hybrid nDCG@10 | 0.6100 |
| Reranking hybrid hit@10 | 0.7400 |
| Reranking hybrid Recall@100 | 0.9333 |
| Reranking hybrid candidate subset | top-100 plus optional rank-101 safeguard (`reranking_hybrid`) |
| Reranking hybrid candidates / query | 100-101 |
| Reranking hybrid safeguard rows | 15 |
| Query length avg chars | 84.49 |
| Document length avg chars | 1361.31 |

### Public Sources

- [FaMTEB: Massive Text Embedding Benchmark in Persian Language](https://arxiv.org/abs/2502.11571).
- [MTEB: Massive Text Embedding Benchmark](https://arxiv.org/abs/2210.07316).
- [MCINext/scifact-fa-v2 dataset card](https://huggingface.co/datasets/MCINext/scifact-fa-v2).

### Hugging Face Links

- Nano dataset: [hakari-bench/NanoFaMTEB-v2](https://huggingface.co/datasets/hakari-bench/NanoFaMTEB-v2)
- Source dataset: [MCINext/scifact-fa-v2](https://huggingface.co/datasets/MCINext/scifact-fa-v2)

### Source Reference Table

| Title | Year | Type | URL |
| --- | ---: | --- | --- |
| FaMTEB: Massive Text Embedding Benchmark in Persian Language | 2025 | arXiv paper | https://arxiv.org/abs/2502.11571 |
| MTEB: Massive Text Embedding Benchmark | 2023 | arXiv paper | https://arxiv.org/abs/2210.07316 |
| MCINext/scifact-fa-v2 | 2025 | dataset card | https://huggingface.co/datasets/MCINext/scifact-fa-v2 |

## Machine-Readable Metadata

<!-- benchmark-task-metadata:v1 -->

```yaml
benchmark_task_metadata:
  schema_version: 1
  document_status: first_pass
  nano_set: NanoFaMTEB-v2
  backing_dataset: NanoFaMTEB-v2
  dataset_id: hakari-bench/NanoFaMTEB-v2
  task_name: sci_fact_fa
  split_name: sci_fact_fa
  language: fa
  category: natural_language
  document_path: docs/benchmark_tasks/NanoFaMTEB-v2/sci_fact_fa.md
  source_research:
    primary_source_type: benchmark_paper
    paper_pdf_or_html_checked: true
  counts:
    queries: 200
    documents: 5183
    positive_qrels: 225
  positives_per_query:
    average: 1.125
    min: 1
    median: 1.0
    max: 5
    multi_positive_queries: 19
  text_stats_chars:
    query_mean: 84.485
    document_mean: 1361.3071580165927
  bm25:
    ndcg_at_10: 0.6294447844094562
    hit_at_10: 0.79
    source: dataset_candidate_subset
  links:
    nano_dataset: https://huggingface.co/datasets/hakari-bench/NanoFaMTEB-v2
    source_urls:
    - label: FaMTEB arXiv
      url: https://arxiv.org/abs/2502.11571
    - label: MCINext/scifact-fa-v2
      url: https://huggingface.co/datasets/MCINext/scifact-fa-v2
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
      ndcg_at_10: 0.6294447844
      hit_at_10: 0.79
      recall_at_100: 0.9022222222
      candidate_count_min: 500
      candidate_count_max: 500
      candidate_count_mean: 500.0
      query_count: 200
      query_coverage: 1.0
      relevant_coverage_at_100: 0.9022222222
    dense:
      config: harrier_oss_v1_270m
      label: Dense
      source: dataset_candidate_subset
      top_k: 500
      ndcg_at_10: 0.5610046151
      hit_at_10: 0.7
      recall_at_100: 0.8577777778
      candidate_count_min: 500
      candidate_count_max: 500
      candidate_count_mean: 500.0
      query_count: 200
      query_coverage: 1.0
      relevant_coverage_at_100: 0.8577777778
    reranking_hybrid:
      config: reranking_hybrid
      label: Reranking hybrid
      source: dataset_candidate_subset
      top_k: 100
      ndcg_at_10: 0.6100056603
      hit_at_10: 0.74
      recall_at_100: 0.9333333333
      candidate_count_min: 100
      candidate_count_max: 101
      candidate_count_mean: 100.075
      query_count: 200
      query_coverage: 1.0
      relevant_coverage_at_100: 0.9333333333
      safeguard_positive_rows: 15
      rows_with_101_candidates: 15
```
