# MNanoBEIR / NanoBEIR-th / NanoFiQA2018

## Overview

FiQA is financial answer retrieval. `NanoBEIR-th__NanoFiQA2018` uses Thai
translated finance questions and answer passages.

## Details

### What the Original Data Measures

[FiQA](https://doi.org/10.1145/3184558.3192301) introduced financial opinion and
QA data. BEIR evaluates answer-passage retrieval, and MMTEB provides
multilingual context.

### Observed Data Profile

The task has 50 queries, 4,598 documents, and 123 positive qrels. 28 queries
have multiple positives. Queries average 55.18 characters, and documents average
779.20 characters.

### BM25 Difficulty

BM25 reaches nDCG@10 = 0.2726 and hit@10 = 0.5200. Median first-positive rank is
9.5, so lexical matching is moderately difficult.

### Training Data That May Help

Use Thai financial QA, multilingual finance retrieval, and multi-positive answer
ranking while excluding FiQA, BEIR, NanoBEIR, and translated evaluation answers.

### Synthetic Data Guidance

Generate Thai finance questions from answer passages. Hard negatives should
reuse finance terms but answer a different decision problem.

## Example Data

| Query | Positive document |
| --- | --- |
| Vanguard กำลังอ้างถึงผลตอบแทนประเภทใด? (38 chars) | จากหน้า Vanguard - นี่ดูเหมือนจะเป็นเรื่องที่ง่ายที่สุดเพราะข้อมูล S&P หาง่าย ฉันใช้ MoneyChimp เพื่อยืนยัน - ซึ่งยืนยันว่าหน้า Vanguard เสนอ CAGR ไม่ใช่ค่าเฉลี่ยเลขคณิต หมายเหตุ: Vanguard ระบุว่า "สำหรับผลตอบแทนของตลาดหุ้นสห ... [truncated 225 chars](373 chars) |
| ผลกระทบด้านภาษีของการทำงานฟรีแลนซ์ในสหรัฐอเมริกา (48 chars) | หากคุณมีรายได้ในสหรัฐอเมริกา คุณจะต้องเสียภาษีรายได้สหรัฐจากรายได้ดังกล่าว ยกเว้นว่าจะมีสนธิสัญญากับประเทศของคุณที่ระบุเป็นอย่างอื่น (132 chars) |
| ปริมาณอะไรถือว่าสูงหรือต่ำเมื่อพูดถึงปริมาณ? (44 chars) | ปริมาณการซื้อขายรายวันมักจะถูกเปรียบเทียบกับปริมาณการซื้อขายเฉลี่ยรายวันในช่วง 50 วันที่ผ่านมา สำหรับหุ้นหนึ่งๆ ปริมาณที่สูงมักจะถือว่ามีค่า 2 เท่าหรือมากกว่าปริมาณการซื้อขายเฉลี่ยรายวันในช่วง 50 วันที่ผ่านมา สำหรับหุ้นนั้น อ ... [truncated 225 chars](646 chars) |
| การใช้คะแนนบัตรเครดิตเพื่อชำระค่าใช้จ่ายทางธุรกิจที่หักลดหย่อนภาษีได้ (69 chars) | เพื่อความเรียบง่าย มาลองพิจารณาแค่เงินคืนกันก่อน โดยทั่วไปแล้ว เงินคืนจากบัตรเครดิตสำหรับการใช้งานส่วนตัวจะไม่ต้องเสียภาษี แต่สำหรับการใช้งานธุรกิจจะต้องเสียภาษี (ประมาณนั้น ฉันจะอธิบายเพิ่มเติมในภายหลัง) สาเหตุคือการซื้อส่วน ... [truncated 225 chars](3140 chars) |
| ฉันควรยื่นภาษีอย่างไรในฐานะผู้รับเหมา? (38 chars) | เพื่อวัตถุประสงค์ด้านภาษี คุณจะต้องยื่นแบบฟอร์มในฐานะพนักงาน (T4 slips และภาษีที่หักโดยอัตโนมัติ) แต่ก็ต้องยื่นในฐานะผู้ประกอบการด้วย ปีที่แล้วฉันก็มีสถานการณ์เดียวกันนี้ หนังสือพิมพ์ "พนักงานและผู้ประกอบการอิสระ" จาก Revenue ... [truncated 225 chars](639 chars) |

## Dataset Information

| Field | Value |
| --- | --- |
| Nano set | MNanoBEIR |
| Backing dataset | NanoBEIR-th |
| Task / split | NanoFiQA2018 |
| Hugging Face dataset | [hakari-bench/NanoBEIR-th](https://huggingface.co/datasets/hakari-bench/NanoBEIR-th) |
| Language | th |
| Category | natural_language |
| Queries | 50 |
| Documents | 4,598 |
| Positive qrels | 123 |
| Positives per query avg | 2.46 |
| Positives per query min / median / max | 1 / 2.0 / 15 |
| Multi-positive queries | 28 (56.00%) |
| BM25 nDCG@10 | 0.2726 |
| BM25 hit@10 | 0.5200 |
| Query length avg chars | 55.18 |
| Document length avg chars | 779.20 |

### Public Sources

- [FiQA](https://doi.org/10.1145/3184558.3192301), [BEIR](https://arxiv.org/abs/2104.08663), [MMTEB](https://arxiv.org/abs/2502.13595), and [NanoBEIR](https://huggingface.co/collections/zeta-alpha-ai/nanobeir).

### Hugging Face Links

- Nano dataset: [hakari-bench/NanoBEIR-th](https://huggingface.co/datasets/hakari-bench/NanoBEIR-th)
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
  backing_dataset: NanoBEIR-th
  dataset_id: hakari-bench/NanoBEIR-th
  task_name: NanoFiQA2018
  split_name: NanoFiQA2018
  language: th
  category: natural_language
  document_path: docs/benchmark_tasks/MNanoBEIR/NanoBEIR-th__NanoFiQA2018.md
  source_research: {primary_source_type: task_paper, paper_pdf_or_html_checked: true, no_paper_note: null}
  counts: {queries: 50, documents: 4598, positive_qrels: 123}
  positives_per_query: {average: 2.46, min: 1, median: 2.0, max: 15, multi_positive_queries: 28, multi_positive_query_percent: 56.0}
  text_stats_chars: {query_mean: 55.18, document_mean: 779.201174}
  bm25: {ndcg_at_10: 0.2725832779, hit_at_10: 0.52, source: dataset_bm25_column}
```
