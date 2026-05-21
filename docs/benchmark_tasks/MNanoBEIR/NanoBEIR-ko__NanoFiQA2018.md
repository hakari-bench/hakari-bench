# MNanoBEIR / NanoBEIR-ko / NanoFiQA2018

## Overview

FiQA is a financial question-answer retrieval dataset. `NanoBEIR-ko__NanoFiQA2018`
uses Korean translated personal-finance questions to retrieve Korean translated
answer passages.

## Details

### What the Original Data Measures

[FiQA 2018](https://doi.org/10.1145/3184558.3192301) was created for financial
opinion and question answering data. BEIR uses its retrieval version as a
finance-domain retrieval task, and MMTEB provides the multilingual benchmark
context for the Korean adaptation.

### Observed Data Profile

The sampled Korean task has 50 queries, 4,598 documents, and 123 positive
qrels. Queries average 29.58 characters and ask practical tax, investing, loan,
pricing, and contracting questions. Documents average 490.34 characters and are
forum-style financial answers.

### BM25 Difficulty

BM25 reaches nDCG@10 = 0.3433 and hit@10 = 0.6000. The median first-positive
rank is 5, so lexical matching helps but does not solve the task. Strong models
need financial-domain semantics and answer matching.

### Training Data That May Help

Useful data includes non-overlapping financial QA, Korean finance forum
retrieval, tax and investing question-answer pairs, and multilingual finance
retrieval data. Training should exclude FiQA, BEIR, NanoBEIR, and translated
answer passages likely to overlap.

### Synthetic Data Guidance

Generate Korean finance questions from non-evaluation answer passages, keeping
the question realistic and specific. Hard negatives should share financial terms
but answer a different decision or jurisdictional issue.

## Example Data

| Query | Positive document |
| --- | --- |
| 뱅가드가 제시하는 수익률은 어떤 유형인가요? (24 chars) | 벤처가드 페이지에서 - S&P 데이터를 찾기 쉬워서 이 방법이 가장 쉬워 보였다. 나는 MoneyChimp를 사용해서 데이터를 얻었으며, 이는 벤처가드 페이지가 산술 평균이 아닌 CAGR(복리 성장률)을 제공하고 있다는 것을 확인시켜 준다. 참고로, 벤처가드는 "미국 주식 시장 수익률의 경우 1926년부터 1957년 3월 3일까지 Standard & Poor's 90 지수를 사용한다"고 명시하고 있지 ... [truncated 225 chars](295 chars) |
| 프리랜서의 세금 문제 (11 chars) | 미국에서 소득이 있는 경우, 귀하의 국가와 체결된 조세조약에서 달리 규정하지 않는 한, 해당 소득에 대해 미국 소득세를 납부해야 합니다. (76 chars) |
| 거래량에 대해 이야기할 때 높음과 낮음은 무엇을 기준으로 하나요? (36 chars) | 일일 거래량은 보통 해당 주식의 과거 50일 동안의 평균 일일 거래량과 비교한다. 높은 거래량은 일반적으로 해당 주식의 최근 50일 평균 일일 거래량의 2배 이상을 의미하지만, 일부 트레이더들은 특정 패턴이나 사건의 확인을 위해 기준을 평균 일일 거래량의 3배 또는 4배로 설정하기도 한다. 거래량은 다른 주식의 거래량과 비교하기보다는 해당 주식 자체의 평균 일일 거래량(ADV)과 비교하는 것이 일반적 ... [truncated 225 chars](360 chars) |
| 신용카드 포인트를 사용하여 공제 가능한 사업 비용 납부하기 (32 chars) | 간단히 하기 위해 캐시백만을 먼저 고려해 보겠습니다. 일반적으로 개인용 신용카드의 캐시백은 과세 대상이 아니지만, 사업용으로 사용하는 경우는 과세 대상이 됩니다(정확히는 아닙니다. 나중에 설명하겠습니다). 그 이유는 대부분의 개인 구매가 세후 소득으로 이루어지기 때문입니다. 보통 개인 소득에서 구매한 물품 비용을 공제하지 않기 때문에, 예를 들어 100달러짜리 물건을 구입하고 신용카드 회사로부터 2달 ... [truncated 225 chars](1845 chars) |
| 계약자로서 세금은 어떻게 신고해야 하나요? (23 chars) | 세금 신고를 위해서는 근로자로서(자동으로 원천징수된 T4 소득공제 영수증 포함) 신고해야 할 뿐 아니라, 사업자로서도 신고해야 합니다. 저는 작년에 동일한 상황이었는데요, 캐나다국세청(Revenue Canada)에서 발행한 '근로자 및 자영업자(Employee and self-employed)'라는 안내서가 도움이 될 것입니다. 사업 활동 내역서(form)를 작성하고 공제 가능한 모든 지출 내역을 상 ... [truncated 225 chars](395 chars) |

## Dataset Information

| Field | Value |
| --- | --- |
| Nano set | MNanoBEIR |
| Backing dataset | NanoBEIR-ko |
| Task / split | NanoFiQA2018 |
| Hugging Face dataset | [hakari-bench/NanoBEIR-ko](https://huggingface.co/datasets/hakari-bench/NanoBEIR-ko) |
| Language | ko |
| Category | natural_language |
| Queries | 50 |
| Documents | 4,598 |
| Positive qrels | 123 |
| Avg positives / query | 2.46 |
| Positives per query (min / median / max) | 1 / 2.00 / 15 |
| Queries with multiple positives | 28 (56.0%) |
| BM25 nDCG@10 | 0.3433 |
| BM25 hit@10 | 0.6000 |
| Query length avg chars | 29.58 |
| Document length avg chars | 490.34 |

### Public Sources

- [FiQA 2018](https://doi.org/10.1145/3184558.3192301).
- [BEIR: A Heterogeneous Benchmark for Zero-shot Evaluation of Information Retrieval Models](https://arxiv.org/abs/2104.08663).
- [MMTEB: Massive Multilingual Text Embedding Benchmark](https://arxiv.org/abs/2502.13595).
- [Zeta Alpha NanoBEIR collection](https://huggingface.co/collections/zeta-alpha-ai/nanobeir).

### Hugging Face Links

- Nano dataset: [hakari-bench/NanoBEIR-ko](https://huggingface.co/datasets/hakari-bench/NanoBEIR-ko)
- Source collection: [Zeta Alpha NanoBEIR collection](https://huggingface.co/collections/zeta-alpha-ai/nanobeir)

### Source Reference Table

| Title | Year | Type | URL |
| --- | ---: | --- | --- |
| FiQA 2018 | 2018 | task paper | https://doi.org/10.1145/3184558.3192301 |
| BEIR: A Heterogeneous Benchmark for Zero-shot Evaluation of Information Retrieval Models | 2021 | benchmark paper | https://arxiv.org/abs/2104.08663 |
| MMTEB: Massive Multilingual Text Embedding Benchmark | 2025 | benchmark paper | https://arxiv.org/abs/2502.13595 |
| NanoBEIR: Smaller BEIR dataset subsets | 2024 | dataset collection | https://huggingface.co/collections/zeta-alpha-ai/nanobeir |

## Machine-Readable Metadata

<!-- benchmark-task-metadata:v1 -->

```yaml
benchmark_task_metadata:
  schema_version: 1
  document_status: first_pass
  nano_set: MNanoBEIR
  backing_dataset: NanoBEIR-ko
  dataset_id: hakari-bench/NanoBEIR-ko
  task_name: NanoFiQA2018
  split_name: NanoFiQA2018
  language: ko
  category: natural_language
  document_path: docs/benchmark_tasks/MNanoBEIR/NanoBEIR-ko__NanoFiQA2018.md
  source_research:
    primary_source_type: task_paper
    paper_pdf_or_html_checked: true
    no_paper_note: null
  counts:
    queries: 50
    documents: 4598
    positive_qrels: 123
  positives_per_query:
    average: 2.46
    min: 1
    median: 2.0
    max: 15
    multi_positive_queries: 28
    multi_positive_query_percent: 56.0
  text_stats_chars:
    query_mean: 29.58
    document_mean: 490.337538
  bm25:
    ndcg_at_10: 0.3433232515
    hit_at_10: 0.6
    source: dataset_bm25_column
```
