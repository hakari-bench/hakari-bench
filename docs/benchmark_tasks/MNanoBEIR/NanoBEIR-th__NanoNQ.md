# MNanoBEIR / NanoBEIR-th / NanoNQ

## Overview

Natural Questions is open-domain QA retrieval. `NanoBEIR-th__NanoNQ` uses Thai
translated search questions to retrieve answer passages.

## Details

### What the Original Data Measures

[Natural Questions](https://aclanthology.org/Q19-1026/) uses real search
questions with Wikipedia evidence. BEIR evaluates retrieval, and MMTEB adds
multilingual context.

### Observed Data Profile

The task has 50 queries, 5,035 documents, and 57 qrels. Most queries have one
positive. Queries average 40.82 characters, and documents average 473.63
characters.

### BM25 Difficulty

BM25 reaches nDCG@10 = 0.3191 and hit@10 = 0.5600. Median first-positive rank is
8.0, so answer semantics matter.

### Training Data That May Help

Use Thai open-domain QA, Wikipedia passage retrieval, and multilingual
query-passage pairs, excluding Natural Questions, BEIR, and NanoBEIR overlaps.

### Synthetic Data Guidance

Generate Thai natural questions from encyclopedia passages, with entity-sharing
hard negatives that do not answer the question.

## Example Data

| Query | Positive document |
| --- | --- |
| ปีนี้รอบสุดท้ายจะจัดที่ไหน (26 chars) | การแข่งขันบาสเกตบอลชาย NCAA Division I ปี 2018 เป็นการแข่งขันแบบน็อกเอาต์ 68 ทีมเพื่อกำหนดแชมป์ระดับชาติของสมาคมกรีฑาวิทยาลัยแห่งชาติ (NCAA) Division I สำหรับฤดูกาล 2017–18 รุ่นที่ 80 ของการแข่งขันเริ่มขึ้นเมื่อวันที่ 13 มีนา ... [truncated 225 chars](323 chars) |
| หนัง Nightmare Before Christmas เป็นภาพยนตร์ของดิสนีย์ตั้งแต่แรกหรือไม่ (71 chars) | นิทานก่อนวันคริสต์มาสเริ่มต้นจากบทกวีที่เขียนโดยทีม เบอร์ตันในปี 1982 ขณะที่เขาทำงานเป็นนักสร้างอนิเมชั่นที่วอลท์ ดิสนีย์ ฟีเจอร์ แอนิเมชั่น ด้วยความสำเร็จของวินเซนต์ในปีเดียวกัน สตูดิโอวอลท์ ดิสนีย์เริ่มพิจารณาพัฒนานิทานก่อน ... [truncated 225 chars](557 chars) |
| ทำไมเทวดาแห่งเหนือถึงอยู่ที่นั่น (32 chars) | ตามที่กอร์มลีย์กล่าว ความสำคัญของเทวดามีสามประการ: ประการแรก เพื่อบ่งชี้ว่าภายใต้สถานที่ก่อสร้างนั้น คนงานเหมืองถ่านหินทำงานมาเป็นเวลาสองศตวรรษ; ประการที่สอง เพื่อเข้าใจการเปลี่ยนผ่านจากยุคอุตสาหกรรมสู่ยุคข้อมูล และประการที่ส ... [truncated 225 chars](307 chars) |
| ที่ไหนที่การประนีประนอม 3/5 ถูกกล่าวถึงในรัฐธรรมนูญ (51 chars) | การประนีประนอมสามในห้าพบได้ในมาตรา 1, หมวด 2, ข้อ 3 ของรัฐธรรมนูญสหรัฐอเมริกา ซึ่งระบุว่า: (90 chars) |
| ใครร้องเพลง somebody's watching me ร่วมกับไมเคิล แจ็คสัน (56 chars) | "Somebody's Watching Me" เป็นเพลงของนักร้องชาวอเมริกัน Rockwell จากอัลบั้มสตูดิโอเดบิวต์ของเขา Somebody's Watching Me (1984) ซึ่งถูกปล่อยออกมาเป็นซิงเกิลเดบิวต์ของ Rockwell และซิงเกิลหลักจากอัลบั้มเมื่อวันที่ 14 มกราคม 1984 โ ... [truncated 225 chars](350 chars) |

## Dataset Information

| Field | Value |
| --- | --- |
| Nano set | MNanoBEIR |
| Backing dataset | NanoBEIR-th |
| Task / split | NanoNQ |
| Hugging Face dataset | [hakari-bench/NanoBEIR-th](https://huggingface.co/datasets/hakari-bench/NanoBEIR-th) |
| Language | th |
| Category | natural_language |
| Queries | 50 |
| Documents | 5,035 |
| Positive qrels | 57 |
| Positives per query avg | 1.14 |
| Positives per query min / median / max | 1 / 1.0 / 2 |
| Multi-positive queries | 7 (14.00%) |
| BM25 nDCG@10 | 0.3191 |
| BM25 hit@10 | 0.5600 |
| Query length avg chars | 40.82 |
| Document length avg chars | 473.63 |

### Public Sources

- [Natural Questions](https://aclanthology.org/Q19-1026/), [BEIR](https://arxiv.org/abs/2104.08663), [MMTEB](https://arxiv.org/abs/2502.13595), and [NanoBEIR](https://huggingface.co/collections/zeta-alpha-ai/nanobeir).

### Hugging Face Links

- Nano dataset: [hakari-bench/NanoBEIR-th](https://huggingface.co/datasets/hakari-bench/NanoBEIR-th)
- Source collection: [Zeta Alpha NanoBEIR collection](https://huggingface.co/collections/zeta-alpha-ai/nanobeir)

### Source Reference Table

| Title | Year | Type | URL |
| --- | ---: | --- | --- |
| Natural Questions: a Benchmark for Question Answering Research | 2019 | task paper | https://aclanthology.org/Q19-1026/ |
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
  task_name: NanoNQ
  split_name: NanoNQ
  language: th
  category: natural_language
  document_path: docs/benchmark_tasks/MNanoBEIR/NanoBEIR-th__NanoNQ.md
  source_research: {primary_source_type: task_paper, paper_pdf_or_html_checked: true, no_paper_note: null}
  counts: {queries: 50, documents: 5035, positive_qrels: 57}
  positives_per_query: {average: 1.14, min: 1, median: 1.0, max: 2, multi_positive_queries: 7, multi_positive_query_percent: 14.0}
  text_stats_chars: {query_mean: 40.82, document_mean: 473.625422}
  bm25: {ndcg_at_10: 0.3191231222, hit_at_10: 0.56, source: dataset_bm25_column}
```
