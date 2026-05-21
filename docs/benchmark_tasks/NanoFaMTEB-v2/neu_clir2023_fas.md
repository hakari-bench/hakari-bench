# NanoFaMTEB-v2 / neu_clir2023_fas

## Overview

`neu_clir2023_fas` is a Persian NeuCLIR retrieval task. Queries are information
needs, and documents are longer Persian news or web documents from a hard-negative
pool.

## Details

### What the Original Data Measures

[FaMTEB](https://arxiv.org/abs/2502.11571) includes NeuCLIR retrieval among its
Persian retrieval resources. The source metadata describes
`mteb/NeuCLIR2023RetrievalHardNegatives` as a hard-negative version built from
BM25 and multilingual dense retriever pools. [MTEB](https://arxiv.org/abs/2210.07316)
defines the retrieval task interface used by FaMTEB.

### Observed Data Profile

The split has 74 queries, 10,000 documents, and 3,669 positive qrels. It is
strongly multi-positive, averaging 49.58 positives per query. Queries average
65.82 characters and documents average 3,121.94 characters.

Observed examples ask for information about sanctioned Chinese companies and
the Evergreen ship incident in the Suez Canal. Documents are long news-style
Persian passages.

### BM25 Difficulty

Using the dataset-provided BM25 candidate column and the best-ranked positive,
BM25 reaches nDCG@10 = 0.7761 and hit@10 = 0.9324. It ranks 46 positives first.

BM25 is strong because many queries contain specific names, but the long document
set and many relevant judgments still make ranking nontrivial.

### Training Data That May Help

Helpful training data includes Persian news retrieval, CLIR-style information
needs, hard-negative document ranking, and long-document retrieval. Exclude this
test split's topics, documents, and relevance labels.

### Synthetic Data Guidance

Generate Persian news search topics with multiple relevant articles. Hard
negatives should mention the same event or organization without satisfying the
information need.

## Example Data

| Query | Positive document |
| --- | --- |
| اطلاعاتی درباره شرکت های چینی تحریم شده توسط ایالات متحده، به استثنای هواوی، پیدا کنید. (87 chars) | گنجانده شدن چند شرکت چینی در لیست سیاه پنتاگون+ جزئیات به گزارش اسپوتنیک، شرکت China Construction Technology Co. Ltd. (CCTC) ، China International Engineering Consulting Corp. (CIECC) ، شرکت China National Offshore Oil Corp. ... [truncated 225 chars](1417 chars) |
| اطلاعاتی در مورد کشتی "اورگرین" که در کانال سوئز گیر کرده است را پیدا کنید (74 chars) | تلاش تازه برای شناور کردن کشتی گرفتار در کانال سوئز تلاش تازه برای شناور کردن کشتی گرفتار در کانال سوئز ۳۳ دقیقه پیش منبع تصویر، EPA تلاشی تازه برای به شناور کردن یک کشتی عظیم باربری که کانال سوئز در مصر را سد کرده است در جری ... [truncated 225 chars](2891 chars) |
| پتانسیل گردشگری بين ازبکستان و ایران چقدر است؟ (46 chars) | جاده ابریشم پل ارتباطی گردشگری ایران و ازبکستان غلامحسین ابراهیمی با سابقه فعالیت در بخش های اقتصادی و گردشگری در کشورهای تونس، اردن، لهستان، لیتوانی ، ازبکستان و مالزی به خبرنگار مهر گفت: ازبکستان مانند ایران به دلیل قرار گر ... [truncated 225 chars](4940 chars) |
| تاثیرات اکولوژیکی و زیست محیطی برخورد نفتکش سانچی در 6 ژانویه 2018 چه بود؟ (74 chars) | افزایش مساحت لکه نفتی در سواحل چین به گزارش اسپوتنیک، نفتکش سانچی که حامل 136 هزار تن کندنسانت گاز بود و به شرکت ایرانی تعلق داشت و تحت پرچم پاناما شناوری می کرد با کشتی باری هنگ کنگی در سواحل چین تصادم کرد. این حادثه 6 ژانوی ... [truncated 225 chars](1072 chars) |
| اینترنت 5G چه پتانسیل ها و چالش هایی را برای افراد و شرکت ها به ارمغان می آورد؟ (79 chars) | توسعه 5G بدون آزادسازی باند ۷۰۰ مگاهرتزی مشکل است معاون فنی و توسعه شبکه همراه اول با اشاره به طیف‌های فرکانسی موردنیاز برای توسعه شبکه 5G گفت: باند ۷۰۰-۸۰۰ مگاهرتز در اکثر کشورهای دنیا برای 5G آزاد شده، اما این اتفاق در ایرا ... [truncated 225 chars](4473 chars) |

## Dataset Information

| Field | Value |
| --- | --- |
| Nano set | NanoFaMTEB-v2 |
| Backing dataset | NanoFaMTEB-v2 |
| Task / split | neu_clir2023_fas |
| Hugging Face dataset | [hakari-bench/NanoFaMTEB-v2](https://huggingface.co/datasets/hakari-bench/NanoFaMTEB-v2) |
| Language | fa |
| Category | natural_language |
| Queries | 74 |
| Documents | 10000 |
| Positive qrels | 3669 |
| Positives per query | avg 49.58, min 1, median 38.0, max 100 |
| BM25 nDCG@10 | 0.7761 |
| BM25 hit@10 | 0.9324 |
| Query length avg chars | 65.82 |
| Document length avg chars | 3121.94 |

### Public Sources

- [FaMTEB: Massive Text Embedding Benchmark in Persian Language](https://arxiv.org/abs/2502.11571).
- [MTEB: Massive Text Embedding Benchmark](https://arxiv.org/abs/2210.07316).
- [NeuCLIR project](https://neuclir.github.io/).
- [mteb/NeuCLIR2023RetrievalHardNegatives dataset card](https://huggingface.co/datasets/mteb/NeuCLIR2023RetrievalHardNegatives).

### Hugging Face Links

- Nano dataset: [hakari-bench/NanoFaMTEB-v2](https://huggingface.co/datasets/hakari-bench/NanoFaMTEB-v2)
- Source dataset: [mteb/NeuCLIR2023RetrievalHardNegatives](https://huggingface.co/datasets/mteb/NeuCLIR2023RetrievalHardNegatives)

### Source Reference Table

| Title | Year | Type | URL |
| --- | ---: | --- | --- |
| FaMTEB: Massive Text Embedding Benchmark in Persian Language | 2025 | arXiv paper | https://arxiv.org/abs/2502.11571 |
| MTEB: Massive Text Embedding Benchmark | 2023 | arXiv paper | https://arxiv.org/abs/2210.07316 |
| NeuCLIR | 2023 | project page | https://neuclir.github.io/ |
| mteb/NeuCLIR2023RetrievalHardNegatives | 2024 | dataset card | https://huggingface.co/datasets/mteb/NeuCLIR2023RetrievalHardNegatives |

## Machine-Readable Metadata

<!-- benchmark-task-metadata:v1 -->

```yaml
benchmark_task_metadata:
  schema_version: 1
  document_status: first_pass
  nano_set: NanoFaMTEB-v2
  backing_dataset: NanoFaMTEB-v2
  dataset_id: hakari-bench/NanoFaMTEB-v2
  task_name: neu_clir2023_fas
  split_name: neu_clir2023_fas
  language: fa
  category: natural_language
  document_path: docs/benchmark_tasks/NanoFaMTEB-v2/neu_clir2023_fas.md
  source_research:
    primary_source_type: benchmark_paper
    paper_pdf_or_html_checked: true
  counts:
    queries: 74
    documents: 10000
    positive_qrels: 3669
  positives_per_query:
    average: 49.58108108108108
    min: 1
    median: 38.0
    max: 100
    multi_positive_queries: 73
  text_stats_chars:
    query_mean: 65.82432432432432
    document_mean: 3121.942
  bm25:
    ndcg_at_10: 0.7761
    hit_at_10: 0.9324
    source: dataset_bm25_column
  links:
    nano_dataset: https://huggingface.co/datasets/hakari-bench/NanoFaMTEB-v2
    source_urls:
      - label: FaMTEB arXiv
        url: https://arxiv.org/abs/2502.11571
      - label: mteb/NeuCLIR2023RetrievalHardNegatives
        url: https://huggingface.co/datasets/mteb/NeuCLIR2023RetrievalHardNegatives
  references:
    - title: "FaMTEB: Massive Text Embedding Benchmark in Persian Language"
      url: https://arxiv.org/abs/2502.11571
      year: 2025
      is_paper: true
```
