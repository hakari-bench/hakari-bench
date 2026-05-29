# NanoFaMTEB-v2 / msmarco_fa

## Overview

`msmarco_fa` is a Persian MS MARCO-style passage retrieval split. Short web
queries retrieve answer passages from a Persian hard-negative corpus.

## Details

### What the Original Data Measures

[FaMTEB](https://arxiv.org/abs/2502.11571) describes using translated BEIR and
mMARCO-style retrieval data for Persian evaluation. This split uses
`MCINext/MSMARCO_FA_test_top_250_only_w_correct-v2`, under the MTEB-style
retrieval evaluation introduced by [MTEB](https://arxiv.org/abs/2210.07316).

### Observed Data Profile

The Nano split has 43 queries, 8,766 documents, and 2,826 positive qrels. This
split is heavily multi-positive: queries average 65.72 positives, with a median
of 75. Queries average 31.49 characters and documents average 326.20
characters.

Observed examples include Persian translations of web search questions about
social groups and sous-vide cooking.

### BM25 Difficulty

Using the dataset-provided BM25 candidate column and the best-ranked positive,
BM25 reaches nDCG@10 = 0.8161 and hit@10 = 0.9535. It ranks 29 positives first.

The many-positive qrels and short keyword-like queries make lexical retrieval
strong, but ranked quality still matters because many passages can be partially
relevant.

### Training Data That May Help

Helpful data includes Persian web search logs, mMARCO translations, query-passage
retrieval, and hard-negative passage ranking. Avoid using the 43 evaluation
queries and their positive passages.

### Synthetic Data Guidance

Generate Persian web-search questions and answer passages. Include many
semantically related positives and hard negatives that share query terms but
answer a different intent.

## Example Data

| Query | Positive document |
| --- | --- |
| علل خودکشی در میان نظامیان (26 chars) | علائم اختلال استرس پس از سانحه می‌توانند خیلی زود پس از تجربه یک رویداد آسیب‌زا ظاهر شوند. مشکلات دیگری نیز معمولاً همراه با اختلال استرس پس از سانحه رخ می‌دهند، از جمله افسردگی، سایر اختلالات اضطرابی و سوء مصرف الکل و مواد م ... [truncated 225 chars](580 chars) |
| توصیف فیزیکی درخت کاج چیست؟ (27 chars) | توضیحات محصول. صنوبر چشم آبی نوزاد، یک گونه مخروطی و پرشاخه از صنوبر کلرادو با رشد یکنواخت و سوزن‌های آبی رنگ فشرده است. به طور متوسط، سالانه حدود 20 سانتی‌متر رشد عمودی دارد، در حالی که برخی از صنوبرهای کلرادو می‌توانند تا 3 ... [truncated 225 chars](371 chars) |
| هزینه کفپوش بتنی داخلی (22 chars) | برخی از عواملی که ممکن است به این هزینه اضافه کنند عبارتند از: آماده‌سازی محل و زیرسازی، دسترسی به محل، کف‌های کوچک زیر ۴۶ متر مربع، و بتن ضخیم‌تر. هزینه کف بتنی رنگی یکپارچه: ۳.۷۵ دلار به ازای هر متر مربع، که شامل بسته پایه ... [truncated 225 chars](260 chars) |
| تعریف حکم اعلامی (16 chars) | در بیشتر ایالت‌های آمریکا و کانادا، شرکت بیمه به طور کلی در این مرحله چهار گزینه اصلی دارد: ۱. دفاع بی‌قید و شرط از بیمه‌شده؛ ۲. دفاع از بیمه‌شده با قید حفظ حقوق؛ ۳. درخواست حکم قضایی مبنی بر عدم تعهد به دفاع از ادعا؛ یا ۴. ا ... [truncated 225 chars](260 chars) |
| هیدروژن در چه دمایی به حالت مایع تبدیل می‌شود؟ (46 chars) | گاز. برای اینکه هیدروژن به مایع تبدیل شود، باید آن را تا 20.28 کلوین، که معادل -252.87 درجه سانتی‌گراد یا -434.45 درجه فارنهایت است، سرد کنید. ۶ نفر این مطلب را مفید دانسته‌اند. (177 chars) |

## Dataset Information

| Field | Value |
| --- | --- |
| Nano set | NanoFaMTEB-v2 |
| Backing dataset | NanoFaMTEB-v2 |
| Task / split | msmarco_fa |
| Hugging Face dataset | [hakari-bench/NanoFaMTEB-v2](https://huggingface.co/datasets/hakari-bench/NanoFaMTEB-v2) |
| Language | fa |
| Category | natural_language |
| Queries | 43 |
| Documents | 8766 |
| Positive qrels | 2826 |
| Positives per query | avg 65.72, min 4, median 75, max 100 |
| BM25 nDCG@10 | 0.4737 |
| BM25 hit@10 | 0.9070 |
| BM25 Recall@100 | 0.4296 |
| BM25 candidate subset | top-500 (`bm25`) |
| Dense nDCG@10 | 0.6139 |
| Dense hit@10 | 0.9302 |
| Dense Recall@100 | 0.4922 |
| Dense candidate subset | top-500 (`harrier_oss_v1_270m`) |
| Reranking hybrid nDCG@10 | 0.6119 |
| Reranking hybrid hit@10 | 0.9767 |
| Reranking hybrid Recall@100 | 0.4812 |
| Reranking hybrid candidate subset | top-100 plus optional rank-101 safeguard (`reranking_hybrid`) |
| Reranking hybrid candidates / query | 100 |
| Reranking hybrid safeguard rows | 0 |
| Query length avg chars | 31.49 |
| Document length avg chars | 326.20 |

### Public Sources

- [FaMTEB: Massive Text Embedding Benchmark in Persian Language](https://arxiv.org/abs/2502.11571).
- [MTEB: Massive Text Embedding Benchmark](https://arxiv.org/abs/2210.07316).
- [MCINext/MSMARCO_FA_test_top_250_only_w_correct-v2 dataset card](https://huggingface.co/datasets/MCINext/MSMARCO_FA_test_top_250_only_w_correct-v2).

### Hugging Face Links

- Nano dataset: [hakari-bench/NanoFaMTEB-v2](https://huggingface.co/datasets/hakari-bench/NanoFaMTEB-v2)
- Source dataset: [MCINext/MSMARCO_FA_test_top_250_only_w_correct-v2](https://huggingface.co/datasets/MCINext/MSMARCO_FA_test_top_250_only_w_correct-v2)

### Source Reference Table

| Title | Year | Type | URL |
| --- | ---: | --- | --- |
| FaMTEB: Massive Text Embedding Benchmark in Persian Language | 2025 | arXiv paper | https://arxiv.org/abs/2502.11571 |
| MTEB: Massive Text Embedding Benchmark | 2023 | arXiv paper | https://arxiv.org/abs/2210.07316 |
| MCINext/MSMARCO_FA_test_top_250_only_w_correct-v2 | 2025 | dataset card | https://huggingface.co/datasets/MCINext/MSMARCO_FA_test_top_250_only_w_correct-v2 |

## Machine-Readable Metadata

<!-- benchmark-task-metadata:v1 -->

```yaml
benchmark_task_metadata:
  schema_version: 1
  document_status: first_pass
  nano_set: NanoFaMTEB-v2
  backing_dataset: NanoFaMTEB-v2
  dataset_id: hakari-bench/NanoFaMTEB-v2
  task_name: msmarco_fa
  split_name: msmarco_fa
  language: fa
  category: natural_language
  document_path: docs/benchmark_tasks/NanoFaMTEB-v2/msmarco_fa.md
  source_research:
    primary_source_type: benchmark_paper
    paper_pdf_or_html_checked: true
  counts:
    queries: 43
    documents: 8766
    positive_qrels: 2826
  positives_per_query:
    average: 65.72093023255815
    min: 4
    median: 75
    max: 100
    multi_positive_queries: 43
  text_stats_chars:
    query_mean: 31.488372093023255
    document_mean: 326.20146018708647
  bm25:
    ndcg_at_10: 0.4737383211242888
    hit_at_10: 0.9069767441860465
    source: dataset_candidate_subset
  links:
    nano_dataset: https://huggingface.co/datasets/hakari-bench/NanoFaMTEB-v2
    source_urls:
    - label: FaMTEB arXiv
      url: https://arxiv.org/abs/2502.11571
    - label: MCINext/MSMARCO_FA_test_top_250_only_w_correct-v2
      url: https://huggingface.co/datasets/MCINext/MSMARCO_FA_test_top_250_only_w_correct-v2
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
      ndcg_at_10: 0.4737383211
      hit_at_10: 0.9069767442
      recall_at_100: 0.4295824487
      candidate_count_min: 500
      candidate_count_max: 500
      candidate_count_mean: 500.0
      query_count: 43
      query_coverage: 1.0
      relevant_coverage_at_100: 0.4295824487
    dense:
      config: harrier_oss_v1_270m
      label: Dense
      source: dataset_candidate_subset
      top_k: 500
      ndcg_at_10: 0.6138555639
      hit_at_10: 0.9302325581
      recall_at_100: 0.4922151451
      candidate_count_min: 500
      candidate_count_max: 500
      candidate_count_mean: 500.0
      query_count: 43
      query_coverage: 1.0
      relevant_coverage_at_100: 0.4922151451
    reranking_hybrid:
      config: reranking_hybrid
      label: Reranking hybrid
      source: dataset_candidate_subset
      top_k: 100
      ndcg_at_10: 0.6118709318
      hit_at_10: 0.976744186
      recall_at_100: 0.4812455768
      candidate_count_min: 100
      candidate_count_max: 100
      candidate_count_mean: 100.0
      query_count: 43
      query_coverage: 1.0
      relevant_coverage_at_100: 0.4812455768
      safeguard_positive_rows: 0
      rows_with_101_candidates: 0
```
