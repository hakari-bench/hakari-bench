# MNanoBEIR / NanoBEIR-th / NanoTouche2020

## Overview

Touché 2020 is argument retrieval for controversial questions.
`NanoBEIR-th__NanoTouche2020` uses Thai translated debate questions to retrieve
Thai translated argument passages.

## Details

### What the Original Data Measures

[Touché 2020](https://doi.org/10.1007/978-3-030-58219-7_26) evaluates argument
retrieval for controversial information needs. BEIR and MMTEB frame this as
multilingual argument retrieval.

### Observed Data Profile

The task has 49 queries, 5,745 documents, and 932 qrels. Every query is
multi-positive, averaging 19.02 positives. Queries average 46.29 characters, and
documents average 1,438.05 characters.

### BM25 Difficulty

BM25 reaches nDCG@10 = 0.5108 and hit@10 = 0.9796. Median first-positive rank is
1.0, so BM25 usually finds at least one argument, while ordering many positives
is the harder part.

### Training Data That May Help

Use Thai debate retrieval, argument passages, and stance-aware ranking. Exclude
Touché, BEIR, NanoBEIR, and translated evaluation arguments.

### Synthetic Data Guidance

Generate Thai controversial questions with multiple pro and con arguments.
Negatives should discuss the same topic but not the specific aspect requested.

## Example Data

| Query | Positive document |
| --- | --- |
| การบ้านมีประโยชน์หรือไม่? (25 chars) | ก่อนอื่นมีสามเหตุผลว่าทำไมการบ้านจึงยอดเยี่ยมและควรดำเนินต่อไปในโรงเรียนสมัยใหม่ 1. การบ้านช่วยผู้เรียนที่ลงมือทำ โดยทั่วไปแล้วถือว่ามีผู้เรียนสามประเภท: ผู้ที่เรียนรู้จากการฟัง, ผู้ที่เรียนรู้จากการมองเห็น, และผู้ที่เรียนรู้ ... [truncated 225 chars](3199 chars) |
| ควรโฆษณายาใบสั่งโดยตรงถึงผู้บริโภคหรือไม่? (42 chars) | โฆษณาหลายรายการไม่รวมข้อมูลเพียงพอเกี่ยวกับประสิทธิภาพของยา ตัวอย่างเช่น Lunesta ถูกโฆษณาผ่านผีเสื้อที่ลอยผ่านหน้าต่างห้องนอนเหนือคนที่นอนหลับอย่างสงบ จริงๆ แล้ว Lunesta ช่วยให้ผู้ป่วยนอนหลับเร็วขึ้น 15 นาทีหลังจากการรักษาเป็ ... [truncated 225 chars](1096 chars) |
| ควรมีวัคซีนใด ๆ ที่จำเป็นสำหรับเด็กหรือไม่? (43 chars) | ยังไม่ใช่กรณีที่เต็มรูปแบบ.. แค่จุดเล็กๆ ที่ฉันรวบรวมไว้... รัฐบาลไม่ควรมีสิทธิ์แทรกแซงในเรื่องการตัดสินใจด้านสุขภาพที่พ่อแม่ทำเพื่อบุตรหลานของตน ตามการสำรวจในปี 2010 โดยมหาวิทยาลัยมิชิแกน พบว่า 31% ของพ่อแม่เชื่อว่าพวกเขาควร ... [truncated 225 chars](3513 chars) |
| การทำแท้งควรเป็นเรื่องถูกกฎหมายหรือไม่? (39 chars) | การทำแท้งควรถูกกฎหมายเนื่องจากสถานะบุคคลเริ่มต้นหลังจากที่ทารกในครรภ์มีความสามารถในการมีชีวิตอยู่หรือหลังจากเกิด ไม่ใช่ในขณะที่ตั้งครรภ์ ตามที่ศาลสูงสุดของสหรัฐอเมริกากล่าวว่าบุคคลจะมีอายุเมื่อพวกเขาออกจากครรภ์มารดาและเริ่มหา ... [truncated 225 chars](286 chars) |
| การทดสอบมาตรฐานช่วยพัฒนาการศึกษาไหม? (36 chars) | ข้อสรุป: SAT, ACT และการทดสอบมาตรฐานอื่น ๆ ให้ข้อมูลเชิงลึกเกี่ยวกับความพร้อมของนักเรียนมัธยมปลายสำหรับการศึกษาในวิทยาลัยและมหาวิทยาลัยชั้นนำมากกว่าคะแนน GPA ของโรงเรียนมัธยมปลาย และดังนั้นควรมีบทบาทมากขึ้นในการรับสมัคร เพื่อ ... [truncated 225 chars](3585 chars) |

## Dataset Information

| Field | Value |
| --- | --- |
| Nano set | MNanoBEIR |
| Backing dataset | NanoBEIR-th |
| Task / split | NanoTouche2020 |
| Hugging Face dataset | [hakari-bench/NanoBEIR-th](https://huggingface.co/datasets/hakari-bench/NanoBEIR-th) |
| Language | th |
| Category | natural_language |
| Queries | 49 |
| Documents | 5,745 |
| Positive qrels | 932 |
| Positives per query avg | 19.02 |
| Positives per query min / median / max | 6 / 19.0 / 32 |
| Multi-positive queries | 49 (100.00%) |
| BM25 nDCG@10 | 0.5108 |
| BM25 hit@10 | 0.9796 |
| Query length avg chars | 46.29 |
| Document length avg chars | 1,438.05 |

### Public Sources

- [Touché 2020](https://doi.org/10.1007/978-3-030-58219-7_26), [BEIR](https://arxiv.org/abs/2104.08663), [MMTEB](https://arxiv.org/abs/2502.13595), and [NanoBEIR](https://huggingface.co/collections/zeta-alpha-ai/nanobeir).

### Hugging Face Links

- Nano dataset: [hakari-bench/NanoBEIR-th](https://huggingface.co/datasets/hakari-bench/NanoBEIR-th)
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
  backing_dataset: NanoBEIR-th
  dataset_id: hakari-bench/NanoBEIR-th
  task_name: NanoTouche2020
  split_name: NanoTouche2020
  language: th
  category: natural_language
  document_path: docs/benchmark_tasks/MNanoBEIR/NanoBEIR-th__NanoTouche2020.md
  source_research: {primary_source_type: task_paper, paper_pdf_or_html_checked: true, no_paper_note: null}
  counts: {queries: 49, documents: 5745, positive_qrels: 932}
  positives_per_query: {average: 19.020408, min: 6, median: 19.0, max: 32, multi_positive_queries: 49, multi_positive_query_percent: 100.0}
  text_stats_chars: {query_mean: 46.285714, document_mean: 1438.05483}
  bm25: {ndcg_at_10: 0.5108277498, hit_at_10: 0.9795918367, source: dataset_bm25_column}
```
