# MNanoBEIR / NanoBEIR-th / NanoMSMARCO

## Overview

MS MARCO is web passage retrieval. `NanoBEIR-th__NanoMSMARCO` uses Thai
translated search questions to retrieve Thai translated answer passages.

## Details

### What the Original Data Measures

[MS MARCO](https://arxiv.org/abs/1611.09268) uses real web-search questions and
answer passages. BEIR includes it as passage retrieval, and MMTEB gives
multilingual context.

### Observed Data Profile

The task has 50 queries, 5,043 documents, and 50 qrels. Every query has one
positive. Queries average 32.14 characters, and documents average 293.94
characters.

### BM25 Difficulty

BM25 reaches nDCG@10 = 0.2907 and hit@10 = 0.4600. Median first-positive rank is
17.0, so answer-aware semantic matching is important.

### Training Data That May Help

Use Thai web QA, search-query logs, and multilingual passage retrieval, excluding
MS MARCO, BEIR, NanoBEIR, and translated overlaps.

### Synthetic Data Guidance

Generate concise Thai web questions from non-evaluation passages; hard negatives
should share terms but not answer the question.

## Example Data

| Query | Positive document |
| --- | --- |
| โรคการคิดซ้ำคืออะไร (19 chars) | โรคการย้อนกลับอาหาร โรคการย้อนกลับอาหาร ซึ่งเรียกว่า Merycism เป็นประเภทของความผิดปกติในการกินที่ไม่ได้ระบุไว้ในประเภทอื่น ซึ่งทำให้เกิดการย้อนกลับของอาหาร แม้ว่าจะไม่ได้ถูกระบุว่าเป็นความผิดปกติในการกินเฉพาะใน DSM-IV แต่มีพา ... [truncated 225 chars](283 chars) |
| ใครร้องเพลง Here I Go Again (27 chars) | สำหรับการใช้งานอื่น ๆ ดูที่ Here I Go Again (การชี้แจงความหมาย) Here I Go Again เป็นเพลงของวงร็อคอังกฤษ Whitesnake เปิดตัวครั้งแรกในอัลบั้ม Saints & Sinners ปี 1982 เพลงนี้ถูกบันทึกเสียงใหม่สำหรับอัลบั้ม Whitesnake ปี 1987 ขอ ... [truncated 225 chars](298 chars) |
| คาเมรอน บอยซ์ แสดงเป็นใครในลิฟและแมดดี้ (39 chars) | เตรียมตัวให้พร้อมสำหรับเสียงหัวเราะที่จริงจังนะทุกคน ในการชมพิเศษก่อนออกอากาศตอนวันที่ 19 เม.ย. ของ Liv & Maddie ที่ชื่อว่า “Prom-A-Rooney” แน่นอน ในคลิปที่ตลกขบขันนี้ เราเห็นเจสซี่ที่แสดงโดยแคเมอรอน บอยซ์ กระโดดไปยังรายการดิ ... [truncated 225 chars](306 chars) |
| ทะเลทรายขนาดใหญ่ส่วนใหญ่ของโลกเกิดขึ้นที่ไหน (44 chars) | ทะเลทรายที่เหลือของโลกอยู่ภายนอกพื้นที่ขั้วโลก ทะเลทรายที่ใหญ่ที่สุดคือทะเลทรายซาฮารา ซึ่งเป็นทะเลทรายเขตร้อนชื้นในแอฟริกาเหนือ (127 chars) |
| ความหมายของทองแดงสำหรับตำรวจ (28 chars) | จากการค้นพบในปัจจุบัน ดูเหมือนว่า "copper" (ตำรวจ, แปลตรงตัวว่า 'ผู้ที่จับกุม') จะมีมาก่อน "cop" (ไม่ว่าจะใช้ในรูปแบบคำกริยาหมายถึงการจับกุม หรือในรูปแบบคำนามหมายถึงตำรวจ) อาจเป็นไปได้ว่าเหรียญตรา "copper" ที่ตำรวจสารวัตรคนแร ... [truncated 225 chars](322 chars) |

## Dataset Information

| Field | Value |
| --- | --- |
| Nano set | MNanoBEIR |
| Backing dataset | NanoBEIR-th |
| Task / split | NanoMSMARCO |
| Hugging Face dataset | [hakari-bench/NanoBEIR-th](https://huggingface.co/datasets/hakari-bench/NanoBEIR-th) |
| Language | th |
| Category | natural_language |
| Queries | 50 |
| Documents | 5,043 |
| Positive qrels | 50 |
| BM25 nDCG@10 | 0.2907 |
| BM25 hit@10 | 0.4600 |
| BM25 Recall@100 | 0.8000 |
| BM25 candidate subset | top-500 (`bm25`) |
| Dense nDCG@10 | 0.4265 |
| Dense hit@10 | 0.6200 |
| Dense Recall@100 | 0.9200 |
| Dense candidate subset | top-500 (`harrier_oss_v1_270m`) |
| Reranking hybrid nDCG@10 | 0.3653 |
| Reranking hybrid hit@10 | 0.5400 |
| Reranking hybrid Recall@100 | 0.9400 |
| Reranking hybrid candidate subset | top-100 plus optional rank-101 safeguard (`reranking_hybrid`) |
| Reranking hybrid candidates / query | 100-101 |
| Reranking hybrid safeguard rows | 3 |
| Query length avg chars | 32.14 |
| Document length avg chars | 293.94 |

### Public Sources

- [MS MARCO](https://arxiv.org/abs/1611.09268), [BEIR](https://arxiv.org/abs/2104.08663), [MMTEB](https://arxiv.org/abs/2502.13595), and [NanoBEIR](https://huggingface.co/collections/zeta-alpha-ai/nanobeir).

### Hugging Face Links

- Nano dataset: [hakari-bench/NanoBEIR-th](https://huggingface.co/datasets/hakari-bench/NanoBEIR-th)
- Source collection: [Zeta Alpha NanoBEIR collection](https://huggingface.co/collections/zeta-alpha-ai/nanobeir)

### Source Reference Table

| Title | Year | Type | URL |
| --- | ---: | --- | --- |
| MS MARCO: A Human Generated MAchine Reading COmprehension Dataset | 2016 | task paper | https://arxiv.org/abs/1611.09268 |
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
  backing_dataset: NanoBEIR-th
  dataset_id: hakari-bench/NanoBEIR-th
  task_name: NanoMSMARCO
  split_name: NanoMSMARCO
  language: th
  category: natural_language
  document_path: docs/benchmark_tasks/MNanoBEIR/NanoBEIR-th__NanoMSMARCO.md
  source_research:
    primary_source_type: task_paper
    paper_pdf_or_html_checked: true
    no_paper_note: null
  counts:
    queries: 50
    documents: 5043
    positive_qrels: 50
  positives_per_query:
    average: 1.0
    min: 1
    median: 1.0
    max: 1
    multi_positive_queries: 0
    multi_positive_query_percent: 0.0
  text_stats_chars:
    query_mean: 32.14
    document_mean: 293.935951
  bm25:
    ndcg_at_10: 0.29072217611710294
    hit_at_10: 0.46
    source: dataset_candidate_subset
  candidate_subsets:
    bm25:
      config: bm25
      label: BM25
      source: dataset_candidate_subset
      top_k: 500
      ndcg_at_10: 0.2907221761
      hit_at_10: 0.46
      recall_at_100: 0.8
      candidate_count_min: 500
      candidate_count_max: 500
      candidate_count_mean: 500.0
      query_count: 50
      query_coverage: 1.0
      relevant_coverage_at_100: 0.8
    dense:
      config: harrier_oss_v1_270m
      label: Dense
      source: dataset_candidate_subset
      top_k: 500
      ndcg_at_10: 0.4264964722
      hit_at_10: 0.62
      recall_at_100: 0.92
      candidate_count_min: 500
      candidate_count_max: 500
      candidate_count_mean: 500.0
      query_count: 50
      query_coverage: 1.0
      relevant_coverage_at_100: 0.92
    reranking_hybrid:
      config: reranking_hybrid
      label: Reranking hybrid
      source: dataset_candidate_subset
      top_k: 100
      ndcg_at_10: 0.3652801564
      hit_at_10: 0.54
      recall_at_100: 0.94
      candidate_count_min: 100
      candidate_count_max: 101
      candidate_count_mean: 100.06
      query_count: 50
      query_coverage: 1.0
      relevant_coverage_at_100: 0.94
      safeguard_positive_rows: 3
      rows_with_101_candidates: 3
```
