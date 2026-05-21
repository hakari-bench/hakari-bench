# MNanoBEIR / NanoBEIR-vi / NanoArguAna

## Overview

ArguAna is argument-counterargument retrieval. `NanoBEIR-vi__NanoArguAna` uses
Vietnamese translated argumentative passages as queries and retrieves paired
arguments.

## Details

### What the Original Data Measures

[ArguAna](https://aclanthology.org/P18-1023/) is used in BEIR as argument
retrieval, where relevance depends on stance and response relation. MMTEB
provides multilingual context.

### Observed Data Profile

The task has 50 queries, 3,635 documents, and 50 qrels. Every query has one
positive. Queries average 979.28 characters, and documents average 998.38
characters.

### BM25 Difficulty

BM25 reaches nDCG@10 = 0.4275 and hit@10 = 0.7400. Median first-positive rank is
4.0, so lexical overlap helps but stance and counterargument fit matter.

### Training Data That May Help

Use Vietnamese debate retrieval, argument mining, counterargument pairs, and
stance-aware ranking. Exclude ArguAna, BEIR, NanoBEIR, and translated overlaps.

### Synthetic Data Guidance

Generate Vietnamese claims and counterarguments. Hard negatives should discuss
the same topic but answer a different premise or stance.

## Example Data

| Query | Positive document |
| --- | --- |
| Công chúng thờ ơ với cải cách. Liệu cải cách của Thượng viện có nên là ưu tiên hàng đầu trong bối cảnh kinh tế hiện tại hay không là một vấn đề gây tranh cãi, chưa kể đến việc liệu một chính phủ liên minh có thể khởi xướng và ... [truncated 225 chars](824 chars) | Chiến dịch AV không thể so sánh với cải cách Thượng viện, hơn nữa không nên nhầm lẫn một công chúng thiếu thông tin do sự xoay chuyển chính trị với sự thờ ơ. Thường thì cử tri bày tỏ rằng họ thờ ơ vì họ cảm thấy rằng họ không ... [truncated 225 chars](412 chars) |
| Sự mở rộng của Heathrow là rất quan trọng cho nền kinh tế Mở rộng Heathrow sẽ đảm bảo nhiều việc làm hiện tại cũng như tạo ra những việc làm mới. Hiện tại, Heathrow hỗ trợ khoảng 250.000 việc làm. [1] Thêm vào đó, hàng trăm n ... [truncated 225 chars](1000 chars) | Cộng đồng doanh nghiệp còn xa mới thống nhất trong sự ủng hộ được cho là dành cho một đường băng thứ ba. Các cuộc khảo sát cho thấy nhiều doanh nghiệp có ảnh hưởng thực sự không ủng hộ việc mở rộng. Một bức thư bày tỏ lo ngại ... [truncated 225 chars](1180 chars) |
| Con người được đưa ra quá nhiều sự lựa chọn, điều này khiến họ kém hạnh phúc hơn. Quảng cáo dẫn đến việc nhiều người bị choáng ngợp bởi nhu cầu vô tận phải quyết định giữa các yêu cầu cạnh tranh về sự chú ý của họ - điều này ... [truncated 225 chars](952 chars) | Con người không hạnh phúc vì họ không thể có mọi thứ, chứ không phải vì họ được đưa ra quá nhiều sự lựa chọn và cảm thấy căng thẳng. Thực tế, quảng cáo đóng một vai trò quan trọng trong việc đảm bảo rằng số tiền mà mọi người ... [truncated 225 chars](734 chars) |
| Các cuộc tấn công mạng thường được thực hiện bởi các tác nhân phi nhà nước Các cuộc tấn công mạng thường được thực hiện bởi các tác nhân phi nhà nước, chẳng hạn như khủng bố mạng hoặc hacktivists (các nhà hoạt động xã hội thự ... [truncated 225 chars](1143 chars) | Trong trường hợp các tác nhân phi nhà nước tấn công, nhiều chuyên gia trong lĩnh vực luật quốc tế đồng ý rằng nhà nước vẫn có thể trả đũa để tự vệ nếu một nhà nước khác "không sẵn sàng hoặc không có khả năng thực hiện hành độ ... [truncated 225 chars](592 chars) |
| Bởi vì tôn giáo thúc đẩy sự chắc chắn trong niềm tin, sự thù hận được thần thánh hóa dễ dàng được sử dụng để biện minh và thúc đẩy các hành động bạo lực và thực hành phân biệt. Tự do ngôn luận phải đứng thứ hai khi có khả năn ... [truncated 225 chars](1172 chars) | Không ai bị buộc phải thực hiện các hành vi bạo lực bởi lời nói của người khác; đó là sự lựa chọn của họ. Tương tự, có rất nhiều người có quan điểm có thể được coi là kỳ thị đồng tính nhưng lại cảm thấy kinh hoàng trước các h ... [truncated 225 chars](657 chars) |

## Dataset Information

| Field | Value |
| --- | --- |
| Nano set | MNanoBEIR |
| Backing dataset | NanoBEIR-vi |
| Task / split | NanoArguAna |
| Hugging Face dataset | [hakari-bench/NanoBEIR-vi](https://huggingface.co/datasets/hakari-bench/NanoBEIR-vi) |
| Language | vi |
| Category | natural_language |
| Queries | 50 |
| Documents | 3,635 |
| Positive qrels | 50 |
| BM25 nDCG@10 | 0.4275 |
| BM25 hit@10 | 0.7400 |
| Query length avg chars | 979.28 |
| Document length avg chars | 998.38 |

### Public Sources

- [ArguAna](https://aclanthology.org/P18-1023/), [BEIR](https://arxiv.org/abs/2104.08663), [MMTEB](https://arxiv.org/abs/2502.13595), and [NanoBEIR](https://huggingface.co/collections/zeta-alpha-ai/nanobeir).

### Hugging Face Links

- Nano dataset: [hakari-bench/NanoBEIR-vi](https://huggingface.co/datasets/hakari-bench/NanoBEIR-vi)
- Source collection: [Zeta Alpha NanoBEIR collection](https://huggingface.co/collections/zeta-alpha-ai/nanobeir)

### Source Reference Table

| Title | Year | Type | URL |
| --- | ---: | --- | --- |
| Argument Mining for Understanding Peer Reviews | 2018 | task paper | https://aclanthology.org/P18-1023/ |
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
  task_name: NanoArguAna
  split_name: NanoArguAna
  language: vi
  category: natural_language
  document_path: docs/benchmark_tasks/MNanoBEIR/NanoBEIR-vi__NanoArguAna.md
  source_research: {primary_source_type: task_paper, paper_pdf_or_html_checked: true, no_paper_note: null}
  counts: {queries: 50, documents: 3635, positive_qrels: 50}
  positives_per_query: {average: 1.0, min: 1, median: 1.0, max: 1, multi_positive_queries: 0, multi_positive_query_percent: 0.0}
  text_stats_chars: {query_mean: 979.28, document_mean: 998.382669}
  bm25: {ndcg_at_10: 0.4275398701, hit_at_10: 0.74, source: dataset_bm25_column}
```
