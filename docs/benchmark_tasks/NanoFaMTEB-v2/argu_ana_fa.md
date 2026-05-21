# NanoFaMTEB-v2 / argu_ana_fa

## Overview

`argu_ana_fa` is a Persian argument retrieval task. The query is an argument or
claim, and the positive document is a counterargument-style paired text from the
Persian ArguAna variant.

## Details

### What the Original Data Measures

[FaMTEB: Massive Text Embedding Benchmark in Persian Language](https://arxiv.org/abs/2502.11571)
introduces a Persian embedding benchmark built on MTEB, including retrieval
datasets created from existing Persian data, translations of English datasets,
and synthetic Persian data. It lists ArguAna-Fa as a retrieval dataset. [MTEB:
Massive Text Embedding Benchmark](https://arxiv.org/abs/2210.07316) provides the
multi-task evaluation framework that FaMTEB follows.

This split uses `MCINext/arguana-fa-v2`, a Persian ArguAna-style retrieval
dataset. It tests whether a model can retrieve an opposing or paired argument,
which is semantically related but often not a lexical paraphrase.

### Observed Data Profile

The Nano split has 199 queries, 8,669 candidate documents, and 199 positive
qrels. Every query has one positive. Queries average 1,100.98 characters and
documents average 973.15 characters, so both sides are paragraph-length Persian
argument texts.

Observed examples discuss healthcare policy, drug markets, physician ethics, and
other argumentative topics. The retrieval target is often a counter-position
with overlapping domain words but a different stance.

### BM25 Difficulty

Using the dataset-provided BM25 candidate column, BM25 reaches nDCG@10 = 0.2860
and hit@10 = 0.6432. It ranks no positives first, but places a positive in the
top 100 for every query.

The high hit@10 but zero top-1 count suggests lexical overlap narrows the search
space, while stance-sensitive ranking remains difficult.

### Training Data That May Help

Helpful training data includes Persian argument-pair retrieval, translated
ArguAna-style counterargument pairs, debate datasets, and stance-aware semantic
search. Exclude the NanoFaMTEB-v2 evaluation queries, positives, and source
dataset rows used in this split.

### Synthetic Data Guidance

Generate Persian arguments with paired counterarguments across policy, health,
ethics, and social topics. Hard negatives should share the topic vocabulary but
support a different relation or stance than the positive.

## Example Data

| Query | Positive document |
| --- | --- |
| مخالفت با سقط جنین ناقص زایمان بخشی از استراتژی‌ای است که هدف آن ممنوع کردن سقط جنین به طور کلی است. سقط جنین ناقص زایمان درصد بسیار کمی از کل سقط جنین‌ها را تشکیل می‌دهد، اما از نظر پزشکی و روان‌شناختی، باید کمترین بحث‌برانگ ... [truncated 225 chars](668 chars) | فلسفه بارداری، اخلاق، زندگی، خانواده، خانه، ممنوعیت سقط جنین ناقص اگرچه بسیاری از مخالفان سقط جنین نوع خاص، در اصل با سقط جنین مخالف هستند، اما ارتباط ضروری بین این دو وجود ندارد، زیرا سقط جنین نوع خاص، شکلی به‌ویژه وحشتناک ا ... [truncated 225 chars](694 chars) |
| فناوری نوین بشر بارها از طریق اختراعات عظیمی مانند کشاورزی، فولاد، آنتی‌بیوتیک‌ها و ریزتراشه‌ها، جهان را دگرگون کرده است. و همانطور که فناوری پیشرفت کرده، سرعت پیشرفت فناوری نیز افزایش یافته است. پیش‌بینی می‌شود که بین سال‌ها ... [truncated 225 chars](966 chars) | خانه اقلیم معتقد است برای تغییرات اقلیمی جهانی خیلی دیر شده است. پیشرفت‌های تکنولوژیکی تقریباً به‌طور قطع برای کسانی که توانایی پرداخت آن را دارند توسعه خواهند یافت (همانطور که معمولاً در مورد بیشتر فناوری‌ها اتفاق می‌افتد). ... [truncated 225 chars](472 chars) |
| گیاهخواری خطر مسمومیت غذایی را کاهش می‌دهد. تقریباً تمام انواع خطرناک مسمومیت غذایی از طریق گوشت یا تخم‌مرغ منتقل می‌شوند. به عنوان مثال، باکتری کمپیلوباکتر که شایع‌ترین علت مسمومیت غذایی در انگلستان است، معمولاً در گوشت و طی ... [truncated 225 chars](808 chars) | حیوانات، محیط زیست، سلامت عمومی، بهداشت عمومی، وزن، فلسفه، اخلاق. ایمنی و بهداشت مواد غذایی برای همه بسیار مهم است و دولت‌ها باید برای اطمینان از وجود استانداردهای بالا، به ویژه در رستوران‌ها و سایر مکان‌هایی که مردم غذا تهیه ... [truncated 225 chars](1605 chars) |
| برخوردها بخشی از بازی هستند. اولاً، برخوردها بخشی از سنت بیسبال هستند. آنها برای مدت طولانی بخشی از این بازی بوده‌اند. طرفداران، بازیکنان و مربیان همه انتظار دارند که ضربات به صفحه اصلی هر از گاهی رخ دهد. جیسون واریتک، گیرنده ... [truncated 225 chars](2033 chars) | تیم ورزشی هوس معتقد است که لیگ اصلی بیسبال باید به بازیکنان اجازه دهد برخوردها را ادامه دهند. برخوردها بخش به مراتب کمتری از بازی را تشکیل می‌دهند تا آنچه مردم تصور می‌کنند. این تصور که برخوردها از دیرباز در بازی وجود داشته‌ا ... [truncated 225 chars](1475 chars) |
| رادیوهای مردمی به جای تحمیل صدای قدرتمندان، به مردم امکان بیان دیدگاه‌هایشان را می‌دهند. رویدادهای بهار عربی (و رویدادهای پیشین مانند انقلاب‌های ۱۹۸۹) نشان داده‌اند که ابزارهای ارتباطی مؤثر حیاتی هستند. در کشوری که مردم تنها ... [truncated 225 chars](1121 chars) | رسانه‌ها و خانه دولت معتقدند رادیوهای محلی خوب هستند. رادیوهای محلی می‌توانند همان کارهای شگفت‌انگیزی را که به نظر می‌رسد طرفداران آن به آن‌ها امیدوارند، انجام دهند. آن‌ها حتی می‌توانند کارهای دیگری هم انجام دهند. اگر این پیش ... [truncated 225 chars](537 chars) |

## Dataset Information

| Field | Value |
| --- | --- |
| Nano set | NanoFaMTEB-v2 |
| Backing dataset | NanoFaMTEB-v2 |
| Task / split | argu_ana_fa |
| Hugging Face dataset | [hakari-bench/NanoFaMTEB-v2](https://huggingface.co/datasets/hakari-bench/NanoFaMTEB-v2) |
| Language | fa |
| Category | natural_language |
| Queries | 199 |
| Documents | 8669 |
| Positive qrels | 199 |
| BM25 nDCG@10 | 0.2860 |
| BM25 hit@10 | 0.6432 |
| Query length avg chars | 1100.98 |
| Document length avg chars | 973.15 |

### Public Sources

- [FaMTEB: Massive Text Embedding Benchmark in Persian Language](https://arxiv.org/abs/2502.11571).
- [MTEB: Massive Text Embedding Benchmark](https://arxiv.org/abs/2210.07316).
- [MCINext/arguana-fa-v2 dataset card](https://huggingface.co/datasets/MCINext/arguana-fa-v2).

### Hugging Face Links

- Nano dataset: [hakari-bench/NanoFaMTEB-v2](https://huggingface.co/datasets/hakari-bench/NanoFaMTEB-v2)
- Source dataset: [MCINext/arguana-fa-v2](https://huggingface.co/datasets/MCINext/arguana-fa-v2)

### Source Reference Table

| Title | Year | Type | URL |
| --- | ---: | --- | --- |
| FaMTEB: Massive Text Embedding Benchmark in Persian Language | 2025 | arXiv paper | https://arxiv.org/abs/2502.11571 |
| MTEB: Massive Text Embedding Benchmark | 2023 | arXiv paper | https://arxiv.org/abs/2210.07316 |
| MCINext/arguana-fa-v2 | 2025 | dataset card | https://huggingface.co/datasets/MCINext/arguana-fa-v2 |

## Machine-Readable Metadata

<!-- benchmark-task-metadata:v1 -->

```yaml
benchmark_task_metadata:
  schema_version: 1
  document_status: first_pass
  nano_set: NanoFaMTEB-v2
  backing_dataset: NanoFaMTEB-v2
  dataset_id: hakari-bench/NanoFaMTEB-v2
  task_name: argu_ana_fa
  split_name: argu_ana_fa
  language: fa
  category: natural_language
  document_path: docs/benchmark_tasks/NanoFaMTEB-v2/argu_ana_fa.md
  source_research:
    primary_source_type: benchmark_paper
    paper_pdf_or_html_checked: true
  counts:
    queries: 199
    documents: 8669
    positive_qrels: 199
  positives_per_query:
    average: 1.0
    min: 1
    median: 1
    max: 1
    multi_positive_queries: 0
  text_stats_chars:
    query_mean: 1100.9849246231156
    document_mean: 973.1475372015227
  bm25:
    ndcg_at_10: 0.286
    hit_at_10: 0.6432
    source: dataset_bm25_column
  links:
    nano_dataset: https://huggingface.co/datasets/hakari-bench/NanoFaMTEB-v2
    source_urls:
      - label: FaMTEB arXiv
        url: https://arxiv.org/abs/2502.11571
      - label: MCINext/arguana-fa-v2
        url: https://huggingface.co/datasets/MCINext/arguana-fa-v2
  references:
    - title: "FaMTEB: Massive Text Embedding Benchmark in Persian Language"
      url: https://arxiv.org/abs/2502.11571
      year: 2025
      is_paper: true
```
