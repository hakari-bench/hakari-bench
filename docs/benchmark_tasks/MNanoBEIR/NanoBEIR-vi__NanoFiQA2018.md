# MNanoBEIR / NanoBEIR-vi / NanoFiQA2018

## Overview

FiQA is financial answer retrieval. `NanoBEIR-vi__NanoFiQA2018` uses Vietnamese
translated finance questions and answer passages.

## Details

### What the Original Data Measures

[FiQA](https://doi.org/10.1145/3184558.3192301) introduced financial opinion and
QA data. BEIR evaluates answer-passage retrieval, and MMTEB provides
multilingual context.

### Observed Data Profile

The task has 50 queries, 4,598 documents, and 123 qrels. 28 queries have
multiple positives. Queries average 66.50 characters, and documents average
936.13 characters.

### BM25 Difficulty

BM25 reaches nDCG@10 = 0.3300 and hit@10 = 0.5800. Median first-positive rank is
6.5, so lexical retrieval is useful but incomplete.

### Training Data That May Help

Use Vietnamese financial QA, multilingual finance retrieval, and multi-positive
answer ranking. Exclude FiQA, BEIR, NanoBEIR, and translated evaluation answers.

### Synthetic Data Guidance

Generate Vietnamese finance questions from answer passages. Hard negatives
should use related financial terminology while answering a different issue.

## Example Data

| Query | Positive document |
| --- | --- |
| Loại lợi suất nào mà Vanguard đang báo giá? (43 chars) | "Từ trang Vanguard - Đây có vẻ là cái dễ nhất vì dữ liệu S&P dễ tìm. Tôi sử dụng MoneyChimp để lấy - điều này xác nhận rằng trang của Vanguard đang cung cấp CAGR, không phải Trung bình số học. Lưu ý: Vanguard tuyên bố ""Đối v ... [truncated 225 chars](431 chars) |
| Các tác động thuế của việc làm tự do ở Hoa Kỳ (45 chars) | Nếu bạn có thu nhập ở Mỹ, bạn sẽ phải nộp thuế thu nhập Mỹ trên số thu nhập đó, trừ khi có hiệp định với quốc gia của bạn quy định khác. (136 chars) |
| Cái gì được coi là cao hoặc thấp khi nói về âm lượng? (53 chars) | Khối lượng giao dịch hàng ngày thường được so sánh với khối lượng giao dịch trung bình hàng ngày trong 50 ngày qua của một cổ phiếu. Khối lượng cao thường được coi là gấp 2 lần hoặc hơn khối lượng giao dịch trung bình hàng ng ... [truncated 225 chars](782 chars) |
| Sử dụng điểm thẻ tín dụng để thanh toán cho chi phí kinh doanh có thể khấu trừ thuế (83 chars) | "Để đơn giản, hãy bắt đầu bằng cách chỉ xem xét tiền hoàn lại. Nói chung, tiền hoàn lại từ thẻ tín dụng cho mục đích cá nhân không phải chịu thuế, nhưng cho mục đích kinh doanh thì phải chịu thuế (một phần, tôi sẽ giải thích ... [truncated 225 chars](3814 chars) |
| Tôi nên nộp thuế của mình như thế nào với tư cách là một nhà thầu? (66 chars) | Về mục đích thuế, bạn sẽ cần nộp hồ sơ như một nhân viên (biên lai T4 và thuế bị khấu trừ tự động), nhưng cũng như một doanh nhân. Tôi đã gặp tình huống tương tự năm ngoái. Nhân viên và tự làm chủ là một ấn phẩm từ Cơ quan Do ... [truncated 225 chars](723 chars) |

## Dataset Information

| Field | Value |
| --- | --- |
| Nano set | MNanoBEIR |
| Backing dataset | NanoBEIR-vi |
| Task / split | NanoFiQA2018 |
| Hugging Face dataset | [hakari-bench/NanoBEIR-vi](https://huggingface.co/datasets/hakari-bench/NanoBEIR-vi) |
| Language | vi |
| Category | natural_language |
| Queries | 50 |
| Documents | 4,598 |
| Positive qrels | 123 |
| Positives per query avg | 2.46 |
| Positives per query min / median / max | 1 / 2.0 / 15 |
| Multi-positive queries | 28 (56.00%) |
| BM25 nDCG@10 | 0.3300 |
| BM25 hit@10 | 0.5800 |
| Query length avg chars | 66.50 |
| Document length avg chars | 936.13 |

### Public Sources

- [FiQA](https://doi.org/10.1145/3184558.3192301), [BEIR](https://arxiv.org/abs/2104.08663), [MMTEB](https://arxiv.org/abs/2502.13595), and [NanoBEIR](https://huggingface.co/collections/zeta-alpha-ai/nanobeir).

### Hugging Face Links

- Nano dataset: [hakari-bench/NanoBEIR-vi](https://huggingface.co/datasets/hakari-bench/NanoBEIR-vi)
- Source collection: [Zeta Alpha NanoBEIR collection](https://huggingface.co/collections/zeta-alpha-ai/nanobeir)

### Source Reference Table

| Title | Year | Type | URL |
| --- | ---: | --- | --- |
| FiQA: Financial Opinion Mining and Question Answering | 2018 | task paper | https://doi.org/10.1145/3184558.3192301 |
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
  backing_dataset: NanoBEIR-vi
  dataset_id: hakari-bench/NanoBEIR-vi
  task_name: NanoFiQA2018
  split_name: NanoFiQA2018
  language: vi
  category: natural_language
  document_path: docs/benchmark_tasks/MNanoBEIR/NanoBEIR-vi__NanoFiQA2018.md
  source_research: {primary_source_type: task_paper, paper_pdf_or_html_checked: true, no_paper_note: null}
  counts: {queries: 50, documents: 4598, positive_qrels: 123}
  positives_per_query: {average: 2.46, min: 1, median: 2.0, max: 15, multi_positive_queries: 28, multi_positive_query_percent: 56.0}
  text_stats_chars: {query_mean: 66.5, document_mean: 936.129404}
  bm25: {ndcg_at_10: 0.3300251683, hit_at_10: 0.58, source: dataset_bm25_column}
```
