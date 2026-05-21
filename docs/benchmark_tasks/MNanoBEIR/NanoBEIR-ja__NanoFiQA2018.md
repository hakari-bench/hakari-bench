# MNanoBEIR / NanoBEIR-ja / NanoFiQA2018

## Overview

FiQA is a financial question-answer retrieval dataset. `NanoBEIR-ja__NanoFiQA2018`
uses Japanese translated personal-finance questions to retrieve Japanese
translated answer passages.

## Details

### What the Original Data Measures

[FiQA 2018](https://doi.org/10.1145/3184558.3192301) was created for financial
opinion and question answering data. BEIR uses its retrieval version as a
finance-domain retrieval task, and MMTEB provides the multilingual benchmark
context for the Japanese adaptation.

### Observed Data Profile

The sampled Japanese task has 50 queries, 4,598 documents, and 123 positive
qrels. Queries average 28.48 characters and ask practical tax, investing, loan,
pricing, and contracting questions. Documents average 427.96 characters and are
forum-style financial answers.

### BM25 Difficulty

BM25 reaches nDCG@10 = 0.3288 and hit@10 = 0.6200. The median first-positive
rank is 7, so lexical matching helps but does not solve the task. Strong models
need financial-domain semantics and answer matching.

### Training Data That May Help

Useful data includes non-overlapping financial QA, Japanese finance forum
retrieval, tax and investing question-answer pairs, and multilingual finance
retrieval data. Training should exclude FiQA, BEIR, NanoBEIR, and translated
answer passages likely to overlap.

### Synthetic Data Guidance

Generate Japanese finance questions from non-evaluation answer passages,
keeping the question realistic and specific. Hard negatives should share
financial terms but answer a different decision or jurisdictional issue.

## Example Data

| Query | Positive document |
| --- | --- |
| ヴァンガードが提示しているリターンの種類は何ですか？ (26 chars) | ヴァンガードのページから - S&Pのデータが見つけやすいため、これが最も簡単な方法に思えた。私はMoneyChimpを使用して確認したが、そこではヴァンガードのページが算術平均ではなくCAGR（複利成長率）を提示していることを裏付けている。注：ヴァンガードは「米国株式市場のリターンについては、1926年から1957年3月3日まではS&P 90を使用している」と述べているが、Chimpはノーベル賞受賞者であるロバート・シラーのサイトのデータを使用 ... [truncated 225 chars](230 chars) |
| フリーランスの税務上の影響 (13 chars) | 米国で所得がある場合、あなたの国と米国との間に別段の規定を定める条約がない限り、米国所得税が課税されます。 (53 chars) |
| 「ボリューム」について話す際に、高いまたは低いとは何を指すのでしょうか？ (36 chars) | 1日の出来高は、通常、その銘柄の過去50日間の平均1日出来高と比較されます。高い出来高とは、その銘柄の過去50日間の平均1日出来高の2倍以上を指すことが一般的ですが、あるトレーダーは特定のパターンや出来事の確認のために、3倍または4倍の平均1日出来高を基準とすることもあります。出来高はその銘柄自身の平均1日出来高（ADV）と比較されるため、他の銘柄の出来高と比較することはしません。これは、異なる企業では発行済み株式数や流動性、変動性のレベルが異な ... [truncated 225 chars](294 chars) |
| クレジットカードのポイントを、税務上の経費として計上可能なビジネス支出の支払いに使用する (44 chars) | 単純化するために、まずキャッシュバックについてのみ考えましょう。一般的に、個人利用のクレジットカードからのキャッシュバックは課税対象ではありませんが、事業利用の場合は課税対象になります（ただし、後で説明しますが、完全にそうというわけではありません）。その理由は、個人での購入のほとんどが税後所得で行われるためです。通常、個人的な購入品の費用を個人の所得から控除することはないため、100ドルの商品を購入してクレジットカード会社から2ドルのキャッシュバ ... [truncated 225 chars](1624 chars) |
| 請負業として税金を申告するにはどうすればよいですか？ (26 chars) | 税務上の目的で、従業員として（T4スリップで自動的に税金が控除される）申告するだけでなく、起業家としても申告する必要があります。昨年、私も同じ状況でした。「Employee and self-employed」はカナダ税務局（Revenue Canada）が発行している資料で、参考になります。事業活動明細書のフォームを記入し、控除可能なすべての経費について詳細な記録を残す必要があります。コピーを取って7年間保管してください。確定申告の際は会計士に ... [truncated 225 chars](317 chars) |

## Dataset Information

| Field | Value |
| --- | --- |
| Nano set | MNanoBEIR |
| Backing dataset | NanoBEIR-ja |
| Task / split | NanoFiQA2018 |
| Hugging Face dataset | [hakari-bench/NanoBEIR-ja](https://huggingface.co/datasets/hakari-bench/NanoBEIR-ja) |
| Language | ja |
| Category | natural_language |
| Queries | 50 |
| Documents | 4,598 |
| Positive qrels | 123 |
| Avg positives / query | 2.46 |
| Positives per query (min / median / max) | 1 / 2.00 / 15 |
| Queries with multiple positives | 28 (56.0%) |
| BM25 nDCG@10 | 0.3288 |
| BM25 hit@10 | 0.6200 |
| Query length avg chars | 28.48 |
| Document length avg chars | 427.96 |

### Public Sources

- [FiQA 2018](https://doi.org/10.1145/3184558.3192301).
- [BEIR: A Heterogeneous Benchmark for Zero-shot Evaluation of Information Retrieval Models](https://arxiv.org/abs/2104.08663).
- [MMTEB: Massive Multilingual Text Embedding Benchmark](https://arxiv.org/abs/2502.13595).
- [Zeta Alpha NanoBEIR collection](https://huggingface.co/collections/zeta-alpha-ai/nanobeir).

### Hugging Face Links

- Nano dataset: [hakari-bench/NanoBEIR-ja](https://huggingface.co/datasets/hakari-bench/NanoBEIR-ja)
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
  backing_dataset: NanoBEIR-ja
  dataset_id: hakari-bench/NanoBEIR-ja
  task_name: NanoFiQA2018
  split_name: NanoFiQA2018
  language: ja
  category: natural_language
  document_path: docs/benchmark_tasks/MNanoBEIR/NanoBEIR-ja__NanoFiQA2018.md
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
    query_mean: 28.48
    document_mean: 427.9602
  bm25:
    ndcg_at_10: 0.3288331534
    hit_at_10: 0.62
    source: dataset_bm25_column
```
