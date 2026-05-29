# NanoFaMTEB-v2 / syn_per_chatbot_ragfaq

## Overview

`syn_per_chatbot_ragfaq` is a synthetic Persian chatbot RAG FAQ retrieval task.
Queries are multi-turn chatbot conversations, and the positive document is the
FAQ-style question-answer item that should be retrieved.

## Details

### What the Original Data Measures

[FaMTEB](https://arxiv.org/abs/2502.11571) explicitly introduces chatbot and RAG
datasets into the Persian MTEB benchmark, describing synthetic Persian chatbot
and chatbot-RAG data generation. This split uses
`MCINext/synthetic-persian-chatbot-rag-faq-retrieval`, evaluated with the MTEB
retrieval setup from [MTEB](https://arxiv.org/abs/2210.07316).

### Observed Data Profile

The Nano split has 200 queries, 8,696 documents, and 200 positive qrels. Queries
average 597.44 characters and are dialogue transcripts. Documents average
145.69 characters and are compact FAQ entries.

Observed queries include user/chatbot turns about books, computers, and other
support-like topics.

### BM25 Difficulty

Using the dataset-provided BM25 candidate column, BM25 reaches nDCG@10 = 0.2882
and hit@10 = 0.4150. It ranks 38 positives first.

Lexical retrieval is limited because the query contains long conversational
history, while the target is a concise FAQ formulation.

### Training Data That May Help

Helpful data includes Persian RAG FAQ retrieval, conversation-to-knowledge-base
matching, synthetic chatbot logs, and dialogue query rewriting. Exclude the
evaluation conversations and FAQ entries.

### Synthetic Data Guidance

Generate Persian multi-turn conversations with a clear information need and a
matching FAQ item. Hard negatives should share the topic but answer a different
support question.

## Example Data

| Query | Positive document |
| --- | --- |
| کاربر : با سلام، می‌خواستم اطلاعات بیشتری در مورد نحوه پرداخت قبوض برق دریافت کنم. چت بات : سلام! برای پرداخت قبوض برق، می‌تونی از چندین روش استفاده کنی. مثل پرداخت آنلاین، از طریق تلفن، یا مراجعه به دفاتر پرداخت. کاربر : آیا ... [truncated 225 chars](889 chars) | سوال : چگونه می‌توانم صورتحساب خود را از طریق ایمیل دریافت کنم؟ پاسخ : برای دریافت صورتحساب از طریق ایمیل، کافیست اطلاعات خود را به خدمات مشتریان بدهید. (152 chars) |
| کاربر : چرا هنوز سفارش من ارسال نشده؟ چت بات : ما هیچ تأخیری نداریم! سفارش شما همین حالا در حال پردازش است. کاربر : به من گفتید که سه روزه می‌رسد، حالا یک هفته گذشته! چت بات : این مسئله به شرایط حمل و نقل بستگی دارد! ما در ای ... [truncated 225 chars](632 chars) | سوال : چگونه می‌توانم وضعیت سفارش خود را بررسی کنم؟ پاسخ : شما می‌توانید با وارد کردن شماره سفارش در بخش پیگیری سفارش، وضعیت آن را بررسی کنید. (142 chars) |
| کاربر : با سلام، می‌خواستم در مورد نظریه‌های کلان اجتماعی توضیح دهید. چت بات : سلام! حتماً، نظریه‌های کلان اجتماعی به بررسی ساختارهای بزرگ اجتماعی مثل جامعه، فرهنگ و تاریخ می‌پردازند. کاربر : آیا می‌توانید به صورت مختصر به بر ... [truncated 225 chars](824 chars) | سوال : نقش نظریه‌های اجتماعی در سیاست چیست؟ پاسخ : نظریه‌های اجتماعی به ما کمک می‌کنند تا درک بهتری از رفتارهای سیاسی و فرایندهای اجتماعی داشته باشیم. (150 chars) |
| کاربر : سلام! می‌تونی به من بگی چه چیزی برای خریدن خوبه؟ چت بات : سلام! البته. چه نوع کالایی مد نظرتان است؟ مثلاً لباس، اسباب‌ بازی، یا وسایل الکترونیکی؟ کاربر : می‌خوام یه اسباب بازی خوشگل بخرم! چت بات : بسیار خوب. چه سن و چ ... [truncated 225 chars](857 chars) | سوال : چطور می‌توانم اسباب بازی‌های مناسب برای سن خودم را پیدا کنم؟ پاسخ : شما می‌توانید با توجه به سن و سلیقه‌ی خود، از نظرات و پیشنهادات فروشندگان یا منابع آنلاین برای خرید اسباب بازی استفاده کنید. (199 chars) |
| پیام جدید کاربر : آیا می‌توانید توصیه‌های بهداشتی خاصی برای افراد در گروه سنی جوانان ارائه دهید؟ (96 chars) | سوال : توصیه‌های بهداشتی برای نوجوانان چیست؟ پاسخ : نوجوانان باید به تغذیه متوازن، فعالیت بدنی منظم و خواب کافی توجه کنند. همچنین، کاهش مصرف قند و نمک و دوری از سیگار و مشروبات الکلی بسیار اهمیت دارد. (200 chars) |

## Dataset Information

| Field | Value |
| --- | --- |
| Nano set | NanoFaMTEB-v2 |
| Backing dataset | NanoFaMTEB-v2 |
| Task / split | syn_per_chatbot_ragfaq |
| Hugging Face dataset | [hakari-bench/NanoFaMTEB-v2](https://huggingface.co/datasets/hakari-bench/NanoFaMTEB-v2) |
| Language | fa |
| Category | natural_language |
| Queries | 200 |
| Documents | 8696 |
| Positive qrels | 200 |
| BM25 nDCG@10 | 0.2882 |
| BM25 hit@10 | 0.4150 |
| BM25 Recall@100 | 0.7250 |
| BM25 candidate subset | top-500 (`bm25`) |
| Dense nDCG@10 | 0.4304 |
| Dense hit@10 | 0.6200 |
| Dense Recall@100 | 0.8900 |
| Dense candidate subset | top-500 (`harrier_oss_v1_270m`) |
| Reranking hybrid nDCG@10 | 0.3826 |
| Reranking hybrid hit@10 | 0.5600 |
| Reranking hybrid Recall@100 | 0.8900 |
| Reranking hybrid candidate subset | top-100 plus optional rank-101 safeguard (`reranking_hybrid`) |
| Reranking hybrid candidates / query | 100-101 |
| Reranking hybrid safeguard rows | 22 |
| Query length avg chars | 597.44 |
| Document length avg chars | 145.69 |

### Public Sources

- [FaMTEB: Massive Text Embedding Benchmark in Persian Language](https://arxiv.org/abs/2502.11571).
- [MTEB: Massive Text Embedding Benchmark](https://arxiv.org/abs/2210.07316).
- [MCINext/synthetic-persian-chatbot-rag-faq-retrieval dataset card](https://huggingface.co/datasets/MCINext/synthetic-persian-chatbot-rag-faq-retrieval).

### Hugging Face Links

- Nano dataset: [hakari-bench/NanoFaMTEB-v2](https://huggingface.co/datasets/hakari-bench/NanoFaMTEB-v2)
- Source dataset: [MCINext/synthetic-persian-chatbot-rag-faq-retrieval](https://huggingface.co/datasets/MCINext/synthetic-persian-chatbot-rag-faq-retrieval)

### Source Reference Table

| Title | Year | Type | URL |
| --- | ---: | --- | --- |
| FaMTEB: Massive Text Embedding Benchmark in Persian Language | 2025 | arXiv paper | https://arxiv.org/abs/2502.11571 |
| MTEB: Massive Text Embedding Benchmark | 2023 | arXiv paper | https://arxiv.org/abs/2210.07316 |
| MCINext/synthetic-persian-chatbot-rag-faq-retrieval | 2025 | dataset card | https://huggingface.co/datasets/MCINext/synthetic-persian-chatbot-rag-faq-retrieval |

## Machine-Readable Metadata

<!-- benchmark-task-metadata:v1 -->

```yaml
benchmark_task_metadata:
  schema_version: 1
  document_status: first_pass
  nano_set: NanoFaMTEB-v2
  backing_dataset: NanoFaMTEB-v2
  dataset_id: hakari-bench/NanoFaMTEB-v2
  task_name: syn_per_chatbot_ragfaq
  split_name: syn_per_chatbot_ragfaq
  language: fa
  category: natural_language
  document_path: docs/benchmark_tasks/NanoFaMTEB-v2/syn_per_chatbot_ragfaq.md
  source_research:
    primary_source_type: benchmark_paper
    paper_pdf_or_html_checked: true
  counts:
    queries: 200
    documents: 8696
    positive_qrels: 200
  positives_per_query:
    average: 1.0
    min: 1
    median: 1.0
    max: 1
    multi_positive_queries: 0
  text_stats_chars:
    query_mean: 597.44
    document_mean: 145.69319227230912
  bm25:
    ndcg_at_10: 0.2881862395640961
    hit_at_10: 0.415
    source: dataset_candidate_subset
  links:
    nano_dataset: https://huggingface.co/datasets/hakari-bench/NanoFaMTEB-v2
    source_urls:
    - label: FaMTEB arXiv
      url: https://arxiv.org/abs/2502.11571
    - label: MCINext/synthetic-persian-chatbot-rag-faq-retrieval
      url: https://huggingface.co/datasets/MCINext/synthetic-persian-chatbot-rag-faq-retrieval
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
      ndcg_at_10: 0.2881862396
      hit_at_10: 0.415
      recall_at_100: 0.725
      candidate_count_min: 500
      candidate_count_max: 500
      candidate_count_mean: 500.0
      query_count: 200
      query_coverage: 1.0
      relevant_coverage_at_100: 0.725
    dense:
      config: harrier_oss_v1_270m
      label: Dense
      source: dataset_candidate_subset
      top_k: 500
      ndcg_at_10: 0.4303510233
      hit_at_10: 0.62
      recall_at_100: 0.89
      candidate_count_min: 500
      candidate_count_max: 500
      candidate_count_mean: 500.0
      query_count: 200
      query_coverage: 1.0
      relevant_coverage_at_100: 0.89
    reranking_hybrid:
      config: reranking_hybrid
      label: Reranking hybrid
      source: dataset_candidate_subset
      top_k: 100
      ndcg_at_10: 0.3825960292
      hit_at_10: 0.56
      recall_at_100: 0.89
      candidate_count_min: 100
      candidate_count_max: 101
      candidate_count_mean: 100.11
      query_count: 200
      query_coverage: 1.0
      relevant_coverage_at_100: 0.89
      safeguard_positive_rows: 22
      rows_with_101_candidates: 22
```
