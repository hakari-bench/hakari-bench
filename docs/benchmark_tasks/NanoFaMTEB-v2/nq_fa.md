# NanoFaMTEB-v2 / nq_fa

## Overview

`nq_fa` is a Persian Natural Questions-style retrieval split. Short factual
queries retrieve Persian encyclopedia passages.

## Details

### What the Original Data Measures

[FaMTEB](https://arxiv.org/abs/2502.11571) includes translated and Persian
retrieval datasets to evaluate text embeddings beyond English. This split uses
`MCINext/NQ_FA_test_top_250_only_w_correct-v2`, a Persian NQ hard-negative
dataset under the MTEB retrieval setup described by [MTEB](https://arxiv.org/abs/2210.07316).

### Observed Data Profile

The split has 200 queries, 10,000 documents, and 251 positive qrels. Queries
average 46.72 characters and documents average 556.82 characters. Positives per
query average 1.25.

Observed examples ask factual questions about cheese differences and film
locations. Positive documents are concise encyclopedia passages.

### BM25 Difficulty

Using the dataset-provided BM25 candidate column and the best-ranked positive,
BM25 reaches nDCG@10 = 0.4683 and hit@10 = 0.7000. It ranks 55 positives first.

Named entities help lexical retrieval, but answer-bearing passages may phrase
the answer differently from the question.

### Training Data That May Help

Helpful data includes Persian open-domain QA retrieval, translated NQ examples,
and Wikipedia passage retrieval. Avoid source test rows included in this Nano
split.

### Synthetic Data Guidance

Generate Persian factual questions over encyclopedia passages. Hard negatives
should share named entities but omit the requested answer.

## Example Data

| Query | Positive document |
| --- | --- |
| داوران برنامه رقص روی یخ در سال ۲۰۱۴ چه کسانی بودند؟ (52 chars) | رقص روی یخ فیلیپ Schofield و Christine Bleakley برای اجرای مشترک برنامه بازگشتند. Dean، Torvill و Karen Barber برای مربیگری افراد مشهور به برنامه برگشتند. Robin Cousins، Jason Gardiner، Barber و Ashley Roberts برای نهمین، هشت ... [truncated 225 chars](469 chars) |
| فصل پنجم روبی کی منتشر می‌شود؟ (30 chars) | فهرست قسمت‌های RWBY RWBY یک مجموعهٔ وب انیمه‌ای آمریکایی در حال تولید است که توسط شرکت Rooster Teeth Productions ساخته شده است. این مجموعه ابتدا در ۱۸ ژوئیهٔ ۲۰۱۳ در وب‌سایت Rooster Teeth منتشر شد و بعداً قسمت‌های آن در یوتیو ... [truncated 225 chars](457 chars) |
| چه زمانی ترن هوایی آب‌نما در آلن تاورز بسته شد؟ (47 chars) | فلوم (التون تاورز) فلوم یک ترن هوایی آبی (Log Flume) در پارک التون تاورز در استافوردشایر بود. این ترن هوایی در سال ۱۹۸۱ افتتاح شد و در سال ۲۰۰۴ همزمان با اسپانسرینگ آن توسط شرکت ایمپریال لدر، دوباره طراحی شد. این ترن هوایی با ... [truncated 225 chars](425 chars) |
| چه کسی نقش پروفسور پروتون در سریال تئوری بیگ بنگ را بازی می‌کرد؟ (64 chars) | باب نیوهارت نیوارت بعدها به بازیگری روی آورد و در دهه 1970 در نقش دکتر رابرت هارتلی، روانشناس شیکاگویی، در سریال «نمایش باب نیوارت» و سپس در دهه 1980 در نقش دیک لادون، صاحب مسافرخانه در ورمونت، در سریال «نیوارت» بازی کرد. او ... [truncated 225 chars](835 chars) |
| تعداد پارک‌های ملی در هند چند تاست؟ (35 chars) | فهرست پارک‌های ملی هند در دهه 1980، قوانین فدرال بیشتری برای تقویت حمایت از حیات وحش به تصویب رسید. تا ژوئیه 2017، 103 پارک ملی به مساحت 40,500 کیلومتر مربع (15,600 مایل مربع) وجود داشت که 1.23 درصد از کل مساحت سطح هند را تشک ... [truncated 225 chars](239 chars) |

## Dataset Information

| Field | Value |
| --- | --- |
| Nano set | NanoFaMTEB-v2 |
| Backing dataset | NanoFaMTEB-v2 |
| Task / split | nq_fa |
| Hugging Face dataset | [hakari-bench/NanoFaMTEB-v2](https://huggingface.co/datasets/hakari-bench/NanoFaMTEB-v2) |
| Language | fa |
| Category | natural_language |
| Queries | 200 |
| Documents | 10000 |
| Positive qrels | 251 |
| Positives per query | avg 1.25, min 1, median 1.0, max 3 |
| BM25 nDCG@10 | 0.4683 |
| BM25 hit@10 | 0.7000 |
| Query length avg chars | 46.72 |
| Document length avg chars | 556.82 |

### Public Sources

- [FaMTEB: Massive Text Embedding Benchmark in Persian Language](https://arxiv.org/abs/2502.11571).
- [MTEB: Massive Text Embedding Benchmark](https://arxiv.org/abs/2210.07316).
- [MCINext/NQ_FA_test_top_250_only_w_correct-v2 dataset card](https://huggingface.co/datasets/MCINext/NQ_FA_test_top_250_only_w_correct-v2).

### Hugging Face Links

- Nano dataset: [hakari-bench/NanoFaMTEB-v2](https://huggingface.co/datasets/hakari-bench/NanoFaMTEB-v2)
- Source dataset: [MCINext/NQ_FA_test_top_250_only_w_correct-v2](https://huggingface.co/datasets/MCINext/NQ_FA_test_top_250_only_w_correct-v2)

### Source Reference Table

| Title | Year | Type | URL |
| --- | ---: | --- | --- |
| FaMTEB: Massive Text Embedding Benchmark in Persian Language | 2025 | arXiv paper | https://arxiv.org/abs/2502.11571 |
| MTEB: Massive Text Embedding Benchmark | 2023 | arXiv paper | https://arxiv.org/abs/2210.07316 |
| MCINext/NQ_FA_test_top_250_only_w_correct-v2 | 2025 | dataset card | https://huggingface.co/datasets/MCINext/NQ_FA_test_top_250_only_w_correct-v2 |

## Machine-Readable Metadata

<!-- benchmark-task-metadata:v1 -->

```yaml
benchmark_task_metadata:
  schema_version: 1
  document_status: first_pass
  nano_set: NanoFaMTEB-v2
  backing_dataset: NanoFaMTEB-v2
  dataset_id: hakari-bench/NanoFaMTEB-v2
  task_name: nq_fa
  split_name: nq_fa
  language: fa
  category: natural_language
  document_path: docs/benchmark_tasks/NanoFaMTEB-v2/nq_fa.md
  source_research:
    primary_source_type: benchmark_paper
    paper_pdf_or_html_checked: true
  counts:
    queries: 200
    documents: 10000
    positive_qrels: 251
  positives_per_query:
    average: 1.255
    min: 1
    median: 1.0
    max: 3
    multi_positive_queries: 49
  text_stats_chars:
    query_mean: 46.72
    document_mean: 556.8156
  bm25:
    ndcg_at_10: 0.4683
    hit_at_10: 0.7
    source: dataset_bm25_column
  links:
    nano_dataset: https://huggingface.co/datasets/hakari-bench/NanoFaMTEB-v2
    source_urls:
      - label: FaMTEB arXiv
        url: https://arxiv.org/abs/2502.11571
      - label: MCINext/NQ_FA_test_top_250_only_w_correct-v2
        url: https://huggingface.co/datasets/MCINext/NQ_FA_test_top_250_only_w_correct-v2
  references:
    - title: "FaMTEB: Massive Text Embedding Benchmark in Persian Language"
      url: https://arxiv.org/abs/2502.11571
      year: 2025
      is_paper: true
```
