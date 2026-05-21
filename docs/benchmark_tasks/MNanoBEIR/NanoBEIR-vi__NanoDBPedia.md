# MNanoBEIR / NanoBEIR-vi / NanoDBPedia

## Overview

DBPedia Entity is entity retrieval. `NanoBEIR-vi__NanoDBPedia` uses Vietnamese
translated entity needs to retrieve Vietnamese translated entity descriptions.

## Details

### What the Original Data Measures

[DBpedia-Entity](https://doi.org/10.1145/3077136.3080751) evaluates entity
ranking for DBpedia information needs. BEIR and MMTEB frame it as multilingual
entity retrieval.

### Observed Data Profile

The task has 50 queries, 6,045 documents, and 1,158 qrels. It averages 23.16
positives per query and reaches 81. Queries average 35.04 characters, and
documents average 358.04 characters.

### BM25 Difficulty

BM25 reaches nDCG@10 = 0.4949 and hit@10 = 0.9000. Entity names provide strong
lexical anchors, but multi-positive ordering still matters.

### Training Data That May Help

Use Vietnamese entity search, Wikipedia/DBpedia ranking, alias matching, and
multilingual entity retrieval. Exclude DBPedia Entity, BEIR, and NanoBEIR
overlaps.

### Synthetic Data Guidance

Generate Vietnamese entity queries and descriptions with hard negatives sharing
entity type, place, or name fragments.

## Example Data

| Query | Positive document |
| --- | --- |
| fitzgerald auto mall chambersburg pa (36 chars) | Fitzgerald Auto Malls là một đại lý ô tô thuộc sở hữu và điều hành bởi gia đình, được thành lập vào năm 1966, với địa điểm đầu tiên mở cửa tại Bethesda, Maryland. Tính đến năm 2014, Fitzgerald Auto Malls đứng thứ 59 trong dan ... [truncated 225 chars](457 chars) |
| Tập truyện ngắn năm 1994 của Alice Munro là Mở (46 chars) | Alice Ann Munro (/ˈælɨs ˌæn mʌnˈroʊ/, tên thật là Laidlaw /ˈleɪdlɔː/; sinh ngày 10 tháng 7 năm 1931) là một tác giả người Canada. Tác phẩm của Munro được mô tả là đã cách mạng hóa cấu trúc của truyện ngắn, đặc biệt là trong x ... [truncated 225 chars](553 chars) |
| kiến trúc Gallo-Roman ở Paris (29 chars) | Nghệ thuật ở Paris là một bài viết về văn hóa và lịch sử nghệ thuật ở Paris, thủ đô của Pháp. Trong nhiều thế kỷ, Paris đã thu hút các nghệ sĩ từ khắp nơi trên thế giới, đến thành phố để học hỏi và tìm kiếm cảm hứng từ các ng ... [truncated 225 chars](344 chars) |
| các nước cộng hòa của Nam Tư cũ (31 chars) | Hiến pháp Nam Tư năm 1974 là hiến pháp thứ tư và cuối cùng của Cộng hòa Liên bang Xã hội chủ nghĩa Nam Tư. Nó có hiệu lực vào ngày 21 tháng 2. Với 406 điều khoản gốc, hiến pháp năm 1974 là một trong những hiến pháp dài nhất t ... [truncated 225 chars](420 chars) |
| phim quay ở Venice (18 chars) | A Little Romance là một bộ phim hài lãng mạn Technicolor và Panavision của Mỹ ra mắt năm 1979, được đạo diễn bởi George Roy Hill và có sự tham gia của Laurence Olivier, Thelonious Bernard, và Diane Lane trong vai diễn điện ản ... [truncated 225 chars](403 chars) |

## Dataset Information

| Field | Value |
| --- | --- |
| Nano set | MNanoBEIR |
| Backing dataset | NanoBEIR-vi |
| Task / split | NanoDBPedia |
| Hugging Face dataset | [hakari-bench/NanoBEIR-vi](https://huggingface.co/datasets/hakari-bench/NanoBEIR-vi) |
| Language | vi |
| Category | natural_language |
| Queries | 50 |
| Documents | 6,045 |
| Positive qrels | 1,158 |
| Positives per query avg | 23.16 |
| Positives per query min / median / max | 1 / 18.0 / 81 |
| Multi-positive queries | 48 (96.00%) |
| BM25 nDCG@10 | 0.4949 |
| BM25 hit@10 | 0.9000 |
| Query length avg chars | 35.04 |
| Document length avg chars | 358.04 |

### Public Sources

- [DBpedia Entity Retrieval](https://doi.org/10.1145/3077136.3080751), [BEIR](https://arxiv.org/abs/2104.08663), [MMTEB](https://arxiv.org/abs/2502.13595), and [NanoBEIR](https://huggingface.co/collections/zeta-alpha-ai/nanobeir).

### Hugging Face Links

- Nano dataset: [hakari-bench/NanoBEIR-vi](https://huggingface.co/datasets/hakari-bench/NanoBEIR-vi)
- Source collection: [Zeta Alpha NanoBEIR collection](https://huggingface.co/collections/zeta-alpha-ai/nanobeir)

### Source Reference Table

| Title | Year | Type | URL |
| --- | ---: | --- | --- |
| DBpedia Entity Retrieval | 2017 | task paper | https://doi.org/10.1145/3077136.3080751 |
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
  task_name: NanoDBPedia
  split_name: NanoDBPedia
  language: vi
  category: natural_language
  document_path: docs/benchmark_tasks/MNanoBEIR/NanoBEIR-vi__NanoDBPedia.md
  source_research: {primary_source_type: task_paper, paper_pdf_or_html_checked: true, no_paper_note: null}
  counts: {queries: 50, documents: 6045, positive_qrels: 1158}
  positives_per_query: {average: 23.16, min: 1, median: 18.0, max: 81, multi_positive_queries: 48, multi_positive_query_percent: 96.0}
  text_stats_chars: {query_mean: 35.04, document_mean: 358.0445}
  bm25: {ndcg_at_10: 0.4948833642, hit_at_10: 0.9, source: dataset_bm25_column}
```
