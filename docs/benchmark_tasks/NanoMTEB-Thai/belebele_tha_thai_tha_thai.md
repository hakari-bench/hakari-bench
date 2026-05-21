# NanoMTEB-Thai / belebele_tha_thai_tha_thai

## Overview

`NanoMTEB-Thai / belebele_tha_thai_tha_thai` is the same-language Thai Belebele
retrieval split. Thai reading-comprehension questions retrieve Thai passages.
It isolates Thai passage matching from the cross-lingual alignment difficulty in
the other Belebele Thai splits.

## Details

### What the Original Data Measures

[The Belebele Benchmark](https://arxiv.org/abs/2308.16884) provides parallel
multiple-choice reading-comprehension data across 122 language variants, based
on short FLORES-200 passages. The MTEB retrieval formulation maps questions to
their source passages.

In this split, both queries and documents are Thai. The task measures Thai
reading-comprehension retrieval over short translated passages.

### Observed Data Profile

The Nano split has 200 queries, 488 documents, and 200 positive qrel rows. Each
query has one positive passage. Queries average 57.67 characters and Thai
documents average 456.17 characters. The first examples cover accordion-playing
advice, DVD overscan, and historical passages.

### BM25 Difficulty

Using the dataset-provided BM25 candidate column, BM25 reaches nDCG@10 = 0.7271
and hit@10 = 0.8150. It ranks 130 positives at rank 1 and 163 in the top 10. All
positives are in the top 100.

This is much easier for BM25 than the cross-lingual Belebele directions because
query and passage share Thai words. Remaining failures involve questions whose
key phrase is paraphrased or where many passages share generic terms.

### Training Data That May Help

Thai question-to-passage retrieval, Thai reading-comprehension data converted to
retrieval, and same-language Belebele-style pairs should help. Hard negatives
from other short Thai passages are useful because the corpus is small and
passages are topically diverse.

### Synthetic Data Guidance

Generate Thai questions from Thai short passages. Keep the passage-level
reading-comprehension style, including "according to the passage" questions,
where/why questions, and factual questions. Include paraphrases so the model
does not rely only on copied spans.

## Example Data

| Query | Positive document |
| --- | --- |
| การเปลี่ยนแปลงใดที่เกิดจากการปฏิวัติฝรั่งเศสมีผลกระทบอย่างมากต่อพลเมืองชนชั้นแรงงาน (83 chars) | ผลกระทบทางสังคมและการเมืองมีมากมาย เช่น การใช้ระบบเมตริก การเปลี่ยนจากระบอบสมบูรณาญาสิทธิราชย์ไปสู่ระบอบสาธารณรัฐ ความเป็นชาตินิยม และความเชื่อว่าประเทศเป็นของประชาชน ไม่ใช่ของผู้ปกครองคนเดียว หลังการปฏิวัติ อาชีพต่าง ๆ ยังได ... [truncated 225 chars](553 chars) |
| จากบทความ ใครน่าจะเป็นผู้สร้างสังคมเกษตรกรรมขึ้น (48 chars) | เมื่อนานมาแล้วในช่วงศตวรรษที่สิบเก้าและยี่สิบ เชื่อกันว่าคนกลุ่มแรกที่อยู่​อาศัยในประเทศ​นิวซีแลนด์คือชนเผ่าเมารีซึ่งเป็นผู้ล่านกยักษ์โมอา จากนั้นทฤษฎีดังกล่าวได้ก่อให้เกิดแนวคิดที่ว่าชาวเมารีอพยพมาจากโพลีนีเซียในลักษณะเป็นกอ ... [truncated 225 chars](682 chars) |
| ข้อใดต่อไปนี้กล่าวถึงเกษตรกรรมเพื่อยังชีพได้ถูกต้อง (51 chars) | การเกษตรเพื่อดำรงชีพ คือการเกษตรที่กระทำพื่อผลิตอาหารให้เพียงพอต่อความต้องการของเกษตรกรและครอบครัวของพวกเขา การเกษตรเพื่อดำรงชีพคือระบบเรียบง่ายที่มักเป็นการเกษตรอินทรีย์โดยใช้เมล็ดพันธุ์ที่ขึ้นในเขตภูมิเวศผสานรวมกับการหมุนเว ... [truncated 225 chars](383 chars) |
| จากบทความ ข้อใดเป็นยุคที่มีการนองเลือดที่สุดยุคหนึ่งของจีน (58 chars) | จีนสมัยโบราณมีวิธีการแสดงช่วงเวลาต่าง ๆ ที่พิเศษไม่เหมือนใคร โดยแบ่งเป็นช่วงระยะของจีน หรือแต่ละตระกูลที่อยู่ในอำนาจเป็นราชวงศ์ที่มีลักษณะพิเศษ ในช่วงเวลาระหว่างแต่ละราชวงศ์เป็นยุคที่จังหวัดต่าง ๆ ซึ่งแยกจากกันไม่มีความมั่นคง ... [truncated 225 chars](565 chars) |
| กษัตริย์ตุตันคามุนมีชื่อเสียงในแง่ลบตอนไหน (42 chars) | "ใช่แล้วล่ะ! กษัตริย์ตุตันคามุนซึ่งบางครั้งก็ถูกเรียกว่า ""กษัตริย์ทุต"" หรือ ""กษัตริย์เด็ก"" คือหนึ่งในกษัตริย์อียิปต์โบราณที่เป็นที่รู้จักกันมากที่สุดในยุคปัจจุบัน ที่น่าสนใจคือ ผู้คนไม่คิดว่าเขาเป็นคนสำคัญมากในสมัยโบราณ แ ... [truncated 225 chars](550 chars) |

## Dataset Information

| Field | Value |
| --- | --- |
| Nano set | NanoMTEB-Thai |
| Backing dataset | NanoMTEB-Thai |
| Task / split | belebele_tha_thai_tha_thai |
| Hugging Face dataset | [hakari-bench/NanoMTEB-Thai](https://huggingface.co/datasets/hakari-bench/NanoMTEB-Thai) |
| Language | th |
| Category | natural_language |
| Queries | 200 |
| Documents | 488 |
| Positive qrels | 200 |
| BM25 nDCG@10 | 0.7271 |
| BM25 hit@10 | 0.8150 |
| Query length avg chars | 57.67 |
| Document length avg chars | 456.17 |

### Public Sources

- [The Belebele Benchmark: a Parallel Reading Comprehension Dataset in 122 Language Variants](https://arxiv.org/abs/2308.16884), 2023.
- [facebookresearch/belebele](https://github.com/facebookresearch/belebele), source repository.
- [mteb/belebele](https://huggingface.co/datasets/mteb/belebele), MTEB dataset card.

### Hugging Face Links

- Nano dataset: [hakari-bench/NanoMTEB-Thai](https://huggingface.co/datasets/hakari-bench/NanoMTEB-Thai)
- Source task dataset: [mteb/belebele](https://huggingface.co/datasets/mteb/belebele)

### Source Reference Table

| Title | Year | Type | URL |
| --- | ---: | --- | --- |
| The Belebele Benchmark: a Parallel Reading Comprehension Dataset in 122 Language Variants | 2023 | paper | https://arxiv.org/abs/2308.16884 |
| facebookresearch/belebele | 2023 | repository | https://github.com/facebookresearch/belebele |
| mteb/belebele |  | dataset card | https://huggingface.co/datasets/mteb/belebele |

## Machine-Readable Metadata

<!-- benchmark-task-metadata:v1 -->

```yaml
benchmark_task_metadata:
  schema_version: 1
  document_status: first_pass
  nano_set: NanoMTEB-Thai
  backing_dataset: NanoMTEB-Thai
  dataset_id: hakari-bench/NanoMTEB-Thai
  task_name: belebele_tha_thai_tha_thai
  split_name: belebele_tha_thai_tha_thai
  language: th
  category: natural_language
  document_path: docs/benchmark_tasks/NanoMTEB-Thai/belebele_tha_thai_tha_thai.md
  source_research:
    primary_source_type: task_paper
    paper_pdf_or_html_checked: true
    no_paper_note: null
  counts:
    queries: 200
    documents: 488
    positive_qrels: 200
  positives_per_query:
    average: 1.0
    min: 1
    median: 1.0
    max: 1
    multi_positive_queries: 0
    multi_positive_query_percent: 0.0
  text_stats_chars:
    query_mean: 57.67
    document_mean: 456.165984
  bm25:
    ndcg_at_10: 0.7271309311
    hit_at_10: 0.815
    source: dataset_bm25_column
  example_count: 5
```
