# MNanoBEIR / NanoBEIR-vi / NanoTouche2020

## Overview

Touché 2020 is argument retrieval for controversial questions.
`NanoBEIR-vi__NanoTouche2020` uses Vietnamese translated debate questions to
retrieve argument passages.

## Details

### What the Original Data Measures

[Touché 2020](https://doi.org/10.1007/978-3-030-58219-7_26) evaluates argument
retrieval for controversial information needs. BEIR and MMTEB frame this as
multilingual argument retrieval.

### Observed Data Profile

The task has 49 queries, 5,745 documents, and 932 qrels. Every query is
multi-positive, averaging 19.02 positives. Queries average 52.86 characters, and
documents average 1,712.75 characters.

### BM25 Difficulty

BM25 reaches nDCG@10 = 0.5444 and hit@10 = 0.9796. Median first-positive rank is
1.0, so finding one argument is easy for BM25, but ordering many positives is
the central challenge.

### Training Data That May Help

Use Vietnamese debate retrieval, argument passages, stance-aware ranking, and
controversial-question retrieval. Exclude Touché, BEIR, NanoBEIR, and translated
evaluation arguments.

### Synthetic Data Guidance

Generate Vietnamese controversial questions with multiple pro and con arguments.
Hard negatives should discuss the same topic but not answer the specific aspect.

## Example Data

| Query | Positive document |
| --- | --- |
| Bài tập về nhà có lợi không? (28 chars) | Đầu tiên, có ba lý do tại sao bài tập về nhà là tuyệt vời và nên tiếp tục trong các trường học hiện đại. 1. Bài tập về nhà hỗ trợ những người học thực hành. Người ta thường chấp nhận rằng có ba loại người học: những người học ... [truncated 225 chars](3948 chars) |
| Có nên quảng cáo thuốc theo toa trực tiếp đến người tiêu dùng không? (68 chars) | Nhiều quảng cáo không cung cấp đủ thông tin về hiệu quả của thuốc. Ví dụ, Lunesta được quảng cáo bằng hình ảnh một con bướm bay qua cửa sổ phòng ngủ, trên một người đang ngủ say. Thực tế, Lunesta giúp bệnh nhân ngủ nhanh hơn ... [truncated 225 chars](1324 chars) |
| Có cần yêu cầu tiêm vắc xin nào cho trẻ em không? (49 chars) | Chưa phải là một trường hợp đầy đủ... Chỉ là một số điểm nhỏ mà tôi đã tổng hợp... Chính phủ không nên có quyền can thiệp vào các quyết định về sức khỏe mà cha mẹ đưa ra cho con cái của họ. 31% cha mẹ tin rằng họ nên có quyền ... [truncated 225 chars](3913 chars) |
| Phá thai có nên hợp pháp không? (31 chars) | Nạo phá thai nên hợp pháp vì nhân cách bắt đầu khi thai nhi trở nên khả thi hoặc sau khi sinh, chứ không phải tại thời điểm thụ thai. Theo Tòa án Tối cao Hoa Kỳ, một người được tính tuổi khi họ ra khỏi bụng mẹ và hít thở oxy, ... [truncated 225 chars](284 chars) |
| Các bài kiểm tra chuẩn hóa có cải thiện giáo dục không? (55 chars) | Đã giải quyết: SAT, ACT và các bài kiểm tra tiêu chuẩn khác cung cấp nhiều thông tin hơn về sự chuẩn bị của học sinh trung học cho giáo dục tại các trường cao đẳng và đại học elite hơn là GPA trung học, và do đó nên đóng vai ... [truncated 225 chars](4046 chars) |

## Dataset Information

| Field | Value |
| --- | --- |
| Nano set | MNanoBEIR |
| Backing dataset | NanoBEIR-vi |
| Task / split | NanoTouche2020 |
| Hugging Face dataset | [hakari-bench/NanoBEIR-vi](https://huggingface.co/datasets/hakari-bench/NanoBEIR-vi) |
| Language | vi |
| Category | natural_language |
| Queries | 49 |
| Documents | 5,745 |
| Positive qrels | 932 |
| Positives per query avg | 19.02 |
| Positives per query min / median / max | 6 / 19.0 / 32 |
| Multi-positive queries | 49 (100.00%) |
| BM25 nDCG@10 | 0.5444 |
| BM25 hit@10 | 0.9796 |
| Query length avg chars | 52.86 |
| Document length avg chars | 1,712.75 |

### Public Sources

- [Touché 2020](https://doi.org/10.1007/978-3-030-58219-7_26), [BEIR](https://arxiv.org/abs/2104.08663), [MMTEB](https://arxiv.org/abs/2502.13595), and [NanoBEIR](https://huggingface.co/collections/zeta-alpha-ai/nanobeir).

### Hugging Face Links

- Nano dataset: [hakari-bench/NanoBEIR-vi](https://huggingface.co/datasets/hakari-bench/NanoBEIR-vi)
- Source collection: [Zeta Alpha NanoBEIR collection](https://huggingface.co/collections/zeta-alpha-ai/nanobeir)

### Source Reference Table

| Title | Year | Type | URL |
| --- | ---: | --- | --- |
| Overview of Touché 2020: Argument Retrieval | 2020 | task paper | https://doi.org/10.1007/978-3-030-58219-7_26 |
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
  task_name: NanoTouche2020
  split_name: NanoTouche2020
  language: vi
  category: natural_language
  document_path: docs/benchmark_tasks/MNanoBEIR/NanoBEIR-vi__NanoTouche2020.md
  source_research: {primary_source_type: task_paper, paper_pdf_or_html_checked: true, no_paper_note: null}
  counts: {queries: 49, documents: 5745, positive_qrels: 932}
  positives_per_query: {average: 19.020408, min: 6, median: 19.0, max: 32, multi_positive_queries: 49, multi_positive_query_percent: 100.0}
  text_stats_chars: {query_mean: 52.857143, document_mean: 1712.74691}
  bm25: {ndcg_at_10: 0.5444027232, hit_at_10: 0.9795918367, source: dataset_bm25_column}
```
