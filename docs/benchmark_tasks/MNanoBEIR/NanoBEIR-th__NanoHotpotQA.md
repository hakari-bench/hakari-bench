# MNanoBEIR / NanoBEIR-th / NanoHotpotQA

## Overview

HotpotQA is multi-hop Wikipedia QA retrieval. `NanoBEIR-th__NanoHotpotQA` uses
Thai translated questions to retrieve supporting passages.

## Details

### What the Original Data Measures

[HotpotQA](https://arxiv.org/abs/1809.09600) evaluates explainable multi-hop QA.
BEIR uses the supporting-passage retrieval portion, and MMTEB provides
multilingual context.

### Observed Data Profile

The task has 50 queries, 5,090 documents, and 100 qrels. Every query has exactly
two positives. Queries average 79.74 characters, and documents average 330.66
characters.

### BM25 Difficulty

BM25 reaches nDCG@10 = 0.5523 and hit@10 = 0.8800. Median first-positive rank is
1.0, but retrieving both supporting passages remains important.

### Training Data That May Help

Use non-overlapping Thai multi-hop QA, Wikipedia retrieval, and multi-positive
passage ranking. Exclude HotpotQA, BEIR, NanoBEIR, and translated evaluation
questions.

### Synthetic Data Guidance

Generate Thai bridge questions requiring two passages; negatives should mention
one entity but omit the bridge fact.

## Example Data

| Query | Positive document |
| --- | --- |
| เพนนี เรย์ บริดจ์แสดงในซิทคอมโทรทัศน์กับเบน ซาเวจหรือไม่? (57 chars) | เพนนี เรย์ บริดจ์ส (เกิด 29 กรกฎาคม 1990) เป็นนักแสดงชาวอเมริกัน ผลงานทางโทรทัศน์ของเธอรวมถึงบทบาทใน "For Your Love", "Family Law", "Boy Meets World" และ "The Parent 'Hood" เธอเป็นที่รู้จักดีที่สุดจากบทบาทใน "Half & Half" ในฐ ... [truncated 225 chars](240 chars) |
| ใครมอบดาบที่ทำโดยผู้ก่อตั้งโรงเรียนมุรามาสะให้กับคางาโนอิ ชิเกโมจิ? (67 chars) | คางาโนอิ ชิเกโมชิ (加賀井 重望, 1561 – 27 สิงหาคม 1600) เป็นซามูไรชาวญี่ปุ่นในยุคอาซูจิ-โมโมยามะ ผู้รับใช้ตระกูลโอดะ เขาปกครองปราสาทคางาโนอิ ในระหว่างการรบที่โคมากิและนากาคุเตะ ชิเกโมชิได้ต่อสู้ภายใต้การนำของบิดา ชิเกมุเนะ ซึ่งอยู ... [truncated 225 chars](488 chars) |
| ภาพยนตร์เรื่องไหนที่เขียนและกำกับโดยโจบี้ ฮาร์โรลด์ พร้อมดนตรีที่เขียนโดยซามูเอล ซิม? (85 chars) | ซามูเอล ซิม เป็นนักแต่งเพลงสำหรับภาพยนตร์และโทรทัศน์ เขาเริ่มได้รับการยอมรับจากคะแนนเสียงที่ได้รับรางวัลสำหรับซีรีส์ดราม่า "ดันเคิร์ก" ของ BBC ตั้งแต่นั้นมาเขาได้แต่งเพลงสำหรับการผลิตภาพยนตร์และโทรทัศน์ที่หลากหลาย โดยล่าสุดได ... [truncated 225 chars](508 chars) |
| วันที่เล่นของเกมฟุตบอลวิทยาลัยนี้ที่สนามซันไลฟ์ในไมอามี่การ์เดนส์ รัฐฟลอริดา คือเมื่อไหร่ ที่คลีมสันเอาชนะหมายเลข 4 โอคลาโฮมาซูนเนอร์ส 37-17? (141 chars) | ทีมฟุตบอล Clemson Tigers ปี 2015 แทนมหาวิทยาลัย Clemson ในฤดูกาลฟุตบอล NCAA Division I FBS ปี 2015 Tigers นำโดยหัวหน้าโค้ช Dabo Swinney ในปีที่เจ็ดเต็มและปีที่แปดโดยรวมตั้งแต่เข้ามารับตำแหน่งกลางฤดูกาล 2008 พวกเขาเล่นเกมเหย้า ... [truncated 225 chars](949 chars) |
| อาหารของปีศาจเป็นการรวบรวมเพลงเดี่ยวโดยวงดนตรีร็อคแอนด์โรลจากอเมริกาที่รู้จักกันในการแสดงเพลงคันทรีภายใต้ชื่ออะไร? (114 chars) | Devil's Food เป็นการรวมเพลงซิงเกิลของวงร็อกแอนด์โรลอเมริกัน Supersuckers ซึ่งออกจำหน่ายในเดือนเมษายนปี 2005 โดย Mid-Fi records. (127 chars) |

## Dataset Information

| Field | Value |
| --- | --- |
| Nano set | MNanoBEIR |
| Backing dataset | NanoBEIR-th |
| Task / split | NanoHotpotQA |
| Hugging Face dataset | [hakari-bench/NanoBEIR-th](https://huggingface.co/datasets/hakari-bench/NanoBEIR-th) |
| Language | th |
| Category | natural_language |
| Queries | 50 |
| Documents | 5,090 |
| Positive qrels | 100 |
| Positives per query avg | 2.00 |
| Positives per query min / median / max | 2 / 2.0 / 2 |
| Multi-positive queries | 50 (100.00%) |
| BM25 nDCG@10 | 0.5523 |
| BM25 hit@10 | 0.8800 |
| Query length avg chars | 79.74 |
| Document length avg chars | 330.66 |

### Public Sources

- [HotpotQA](https://arxiv.org/abs/1809.09600), [BEIR](https://arxiv.org/abs/2104.08663), [MMTEB](https://arxiv.org/abs/2502.13595), and [NanoBEIR](https://huggingface.co/collections/zeta-alpha-ai/nanobeir).

### Hugging Face Links

- Nano dataset: [hakari-bench/NanoBEIR-th](https://huggingface.co/datasets/hakari-bench/NanoBEIR-th)
- Source collection: [Zeta Alpha NanoBEIR collection](https://huggingface.co/collections/zeta-alpha-ai/nanobeir)

### Source Reference Table

| Title | Year | Type | URL |
| --- | ---: | --- | --- |
| HotpotQA: A Dataset for Diverse, Explainable Multi-hop Question Answering | 2018 | task paper | https://arxiv.org/abs/1809.09600 |
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
  task_name: NanoHotpotQA
  split_name: NanoHotpotQA
  language: th
  category: natural_language
  document_path: docs/benchmark_tasks/MNanoBEIR/NanoBEIR-th__NanoHotpotQA.md
  source_research: {primary_source_type: task_paper, paper_pdf_or_html_checked: true, no_paper_note: null}
  counts: {queries: 50, documents: 5090, positive_qrels: 100}
  positives_per_query: {average: 2.0, min: 2, median: 2.0, max: 2, multi_positive_queries: 50, multi_positive_query_percent: 100.0}
  text_stats_chars: {query_mean: 79.74, document_mean: 330.662475}
  bm25: {ndcg_at_10: 0.5523012117, hit_at_10: 0.88, source: dataset_bm25_column}
```
