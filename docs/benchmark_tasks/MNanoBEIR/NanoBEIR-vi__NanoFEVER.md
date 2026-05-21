# MNanoBEIR / NanoBEIR-vi / NanoFEVER

## Overview

FEVER is factual claim evidence retrieval. `NanoBEIR-vi__NanoFEVER` uses
Vietnamese translated claims and Wikipedia-style evidence passages.

## Details

### What the Original Data Measures

[FEVER](https://arxiv.org/abs/1803.05355) evaluates fact verification with
retrieved Wikipedia evidence. BEIR uses the retrieval component, and MMTEB
provides multilingual context.

### Observed Data Profile

The task has 50 queries, 4,996 documents, and 57 qrels. Most queries have one
positive. Queries average 53.12 characters, and documents average 1,248.48
characters.

### BM25 Difficulty

BM25 reaches nDCG@10 = 0.6109 and hit@10 = 0.7200. Median first-positive rank is
2.0, so entity cues help but many claims still need semantic evidence matching.

### Training Data That May Help

Use Vietnamese claim-evidence retrieval, Wikipedia evidence mining, and
multilingual fact-checking. Exclude FEVER, BEIR, NanoBEIR, and translated
evaluation examples.

### Synthetic Data Guidance

Generate Vietnamese factual claims from encyclopedia passages with related
entity hard negatives.

## Example Data

| Query | Positive document |
| --- | --- |
| Keith Godchaux biết đến Grateful Dead. (38 chars) | Grateful Dead là một ban nhạc rock của Mỹ được thành lập vào năm 1965 tại Palo Alto, California. Với đội hình từ quintet đến septet, ban nhạc nổi tiếng với phong cách độc đáo và đa dạng, kết hợp các yếu tố của rock, psychedel ... [truncated 225 chars](3093 chars) |
| Taarak Mehta Ka Ooltah Chashmah phim hài? (41 chars) | Taarak Mehta Ka Ooltah Chashmah (tiếng Anh: Góc Nhìn Khác Của Taarak Mehta) là bộ phim hài dài nhất Ấn Độ do Neela Tele Films Private Limited sản xuất. Chương trình bắt đầu phát sóng vào ngày 28 tháng 7 năm 2008. Nó được phát ... [truncated 225 chars](608 chars) |
| Có phải những chiếc máy bay bí mật và công nghệ tiên tiến đã được sản xuất ở Burbank, California không? (103 chars) | Burbank là một thành phố thuộc quận Los Angeles ở miền Nam California, Hoa Kỳ, cách trung tâm Los Angeles 12 dặm về phía tây bắc. Dân số theo điều tra năm 2010 là 103,340. Được mệnh danh là "Thủ đô truyền thông của thế giới" ... [truncated 225 chars](1401 chars) |
| Nero có phải là một người không? (32 chars) | Thuật ngữ triều đại Julio-Claudian đề cập đến năm hoàng đế La Mã đầu tiên - Augustus, Tiberius, Caligula, Claudius và Nero - hoặc gia đình mà họ thuộc về. Họ cai trị Đế chế La Mã từ khi hình thành dưới thời Augustus vào nửa s ... [truncated 225 chars](2091 chars) |
| Scream 2 là một bộ phim độc quyền của Đức. (42 chars) | Scream 2 là một bộ phim kinh dị slasher của Mỹ ra mắt năm 1997 do Wes Craven đạo diễn và Kevin Williamson viết kịch bản. Phim có sự tham gia của David Arquette, Neve Campbell, Courteney Cox, Sarah Michelle Gellar, Jamie Kenne ... [truncated 225 chars](2664 chars) |

## Dataset Information

| Field | Value |
| --- | --- |
| Nano set | MNanoBEIR |
| Backing dataset | NanoBEIR-vi |
| Task / split | NanoFEVER |
| Hugging Face dataset | [hakari-bench/NanoBEIR-vi](https://huggingface.co/datasets/hakari-bench/NanoBEIR-vi) |
| Language | vi |
| Category | natural_language |
| Queries | 50 |
| Documents | 4,996 |
| Positive qrels | 57 |
| Positives per query avg | 1.14 |
| Positives per query min / median / max | 1 / 1.0 / 3 |
| Multi-positive queries | 6 (12.00%) |
| BM25 nDCG@10 | 0.6109 |
| BM25 hit@10 | 0.7200 |
| Query length avg chars | 53.12 |
| Document length avg chars | 1,248.48 |

### Public Sources

- [FEVER](https://arxiv.org/abs/1803.05355), [BEIR](https://arxiv.org/abs/2104.08663), [MMTEB](https://arxiv.org/abs/2502.13595), and [NanoBEIR](https://huggingface.co/collections/zeta-alpha-ai/nanobeir).

### Hugging Face Links

- Nano dataset: [hakari-bench/NanoBEIR-vi](https://huggingface.co/datasets/hakari-bench/NanoBEIR-vi)
- Source collection: [Zeta Alpha NanoBEIR collection](https://huggingface.co/collections/zeta-alpha-ai/nanobeir)

### Source Reference Table

| Title | Year | Type | URL |
| --- | ---: | --- | --- |
| FEVER: a Large-scale Dataset for Fact Extraction and VERification | 2018 | task paper | https://arxiv.org/abs/1803.05355 |
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
  task_name: NanoFEVER
  split_name: NanoFEVER
  language: vi
  category: natural_language
  document_path: docs/benchmark_tasks/MNanoBEIR/NanoBEIR-vi__NanoFEVER.md
  source_research: {primary_source_type: task_paper, paper_pdf_or_html_checked: true, no_paper_note: null}
  counts: {queries: 50, documents: 4996, positive_qrels: 57}
  positives_per_query: {average: 1.14, min: 1, median: 1.0, max: 3, multi_positive_queries: 6, multi_positive_query_percent: 12.0}
  text_stats_chars: {query_mean: 53.12, document_mean: 1248.484588}
  bm25: {ndcg_at_10: 0.6108763054, hit_at_10: 0.72, source: dataset_bm25_column}
```
