# MNanoBEIR / NanoBEIR-th / NanoDBPedia

## Overview

DBPedia Entity is entity retrieval. `NanoBEIR-th__NanoDBPedia` uses Thai
translated entity needs to retrieve Thai translated DBpedia-style descriptions.

## Details

### What the Original Data Measures

[DBpedia-Entity](https://doi.org/10.1145/3077136.3080751) evaluates ranking
entities for DBpedia information needs. BEIR and MMTEB frame it as multilingual
entity retrieval.

### Observed Data Profile

The task has 50 queries, 6,045 documents, and 1,158 qrels. It is strongly
multi-positive, averaging 23.16 positives and reaching 81. Queries average 30.92
characters, and documents average 316.44 characters.

### BM25 Difficulty

BM25 reaches nDCG@10 = 0.5043 and hit@10 = 0.9200. Entity names make lexical
matching strong, but ranking many acceptable entities remains important.

### Training Data That May Help

Useful data includes Thai entity search, Wikipedia/DBpedia retrieval, alias
matching, and multilingual entity ranking. Exclude DBPedia Entity, BEIR, and
NanoBEIR overlaps.

### Synthetic Data Guidance

Generate Thai entity queries and concise descriptions. Hard negatives should
share entity type, location, or name fragments.

## Example Data

| Query | Positive document |
| --- | --- |
| ฟิตซ์เจอรัลด์ออโต้มอลล์แชมเบอร์สเบิร์กเพนซิลเวเนีย (50 chars) | ฟิตซ์เจอรัลด์ ออโต้ มอลล์ เป็นตัวแทนจำหน่ายรถยนต์ที่เป็นของครอบครัวและดำเนินการโดยครอบครัว ซึ่งก่อตั้งขึ้นในปี 1966 โดยมีสถานที่ตั้งแรกเปิดในเบธesda รัฐแมรี่แลนด์ จนถึงปี 2014 ฟิตซ์เจอรัลด์ ออโต้ มอลล์ ได้รับอันดับที่ 59 ในรา ... [truncated 225 chars](431 chars) |
| การรวบรวมเรื่องสั้นปี 1994 ของอลิส มุนโร เปิดอยู่ (49 chars) | อลิซ แอน มันโร (/ˈælɨs ˌæn mʌnˈroʊ/, ชื่อเดิม เลดลอว์ /ˈleɪdlɔː/; เกิด 10 กรกฎาคม 1931) เป็นนักเขียนชาวแคนาดา ผลงานของมันโรถูกอธิบายว่าปฏิวัติสถาปัตยกรรมของเรื่องสั้น โดยเฉพาะในแนวโน้มที่จะเคลื่อนที่ไปข้างหน้าและถอยหลังในเวลา ... [truncated 225 chars](440 chars) |
| สถาปัตยกรรมโรมันในปารีส (23 chars) | ศิลปะในปารีสเป็นบทความเกี่ยวกับวัฒนธรรมและประวัติศาสตร์ศิลปะในปารีส เมืองหลวงของฝรั่งเศส เป็นเวลาหลายศตวรรษที่ปารีสดึงดูดศิลปินจากทั่วโลกให้เดินทางมาที่เมืองนี้เพื่อศึกษาและค้นหาแรงบันดาลใจจากทรัพยากรศิลปะและแกลเลอรีต่างๆ ดัง ... [truncated 225 chars](271 chars) |
| สาธารณรัฐของยูโกสลาเวียเดิม (27 chars) | รัฐธรรมนูญยูโกสลาเวียปี 1974 เป็นรัฐธรรมนูญฉบับที่สี่และฉบับสุดท้ายของสาธารณรัฐสังคมนิยมยูโกสลาเวีย มีผลบังคับใช้ตั้งแต่วันที่ 21 กุมภาพันธ์ โดยมีบทความต้นฉบับ 406 บท ทำให้รัฐธรรมนูญปี 1974 เป็นหนึ่งในรัฐธรรมนูญที่ยาวที่สุดใน ... [truncated 225 chars](375 chars) |
| ภาพยนตร์ที่ถ่ายทำในเวนิส (24 chars) | A Little Romance เป็นภาพยนตร์ตลกโรแมนติก Technicolor และ Panavision ของอเมริกาที่ออกฉายในปี 1979 กำกับโดย George Roy Hill และนำแสดงโดย Laurence Olivier, Thelonious Bernard, และ Diane Lane ในการเปิดตัวภาพยนตร์ของเธอ บทภาพยนตร์ ... [truncated 225 chars](360 chars) |

## Dataset Information

| Field | Value |
| --- | --- |
| Nano set | MNanoBEIR |
| Backing dataset | NanoBEIR-th |
| Task / split | NanoDBPedia |
| Hugging Face dataset | [hakari-bench/NanoBEIR-th](https://huggingface.co/datasets/hakari-bench/NanoBEIR-th) |
| Language | th |
| Category | natural_language |
| Queries | 50 |
| Documents | 6,045 |
| Positive qrels | 1,158 |
| Positives per query avg | 23.16 |
| Positives per query min / median / max | 1 / 18.0 / 81 |
| Multi-positive queries | 48 (96.00%) |
| BM25 nDCG@10 | 0.5043 |
| BM25 hit@10 | 0.9200 |
| BM25 Recall@100 | 0.6520 |
| BM25 candidate subset | top-500 (`bm25`) |
| Dense nDCG@10 | 0.5468 |
| Dense hit@10 | 0.9400 |
| Dense Recall@100 | 0.6675 |
| Dense candidate subset | top-500 (`harrier_oss_v1_270m`) |
| Reranking hybrid nDCG@10 | 0.5482 |
| Reranking hybrid hit@10 | 0.9000 |
| Reranking hybrid Recall@100 | 0.6986 |
| Reranking hybrid candidate subset | top-100 plus optional rank-101 safeguard (`reranking_hybrid`) |
| Reranking hybrid candidates / query | 100 |
| Reranking hybrid safeguard rows | 0 |
| Query length avg chars | 30.92 |
| Document length avg chars | 316.44 |

### Public Sources

- [DBpedia Entity Retrieval](https://doi.org/10.1145/3077136.3080751), [BEIR](https://arxiv.org/abs/2104.08663), [MMTEB](https://arxiv.org/abs/2502.13595), and [NanoBEIR](https://huggingface.co/collections/zeta-alpha-ai/nanobeir).

### Hugging Face Links

- Nano dataset: [hakari-bench/NanoBEIR-th](https://huggingface.co/datasets/hakari-bench/NanoBEIR-th)
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
  backing_dataset: NanoBEIR-th
  dataset_id: hakari-bench/NanoBEIR-th
  task_name: NanoDBPedia
  split_name: NanoDBPedia
  language: th
  category: natural_language
  document_path: docs/benchmark_tasks/MNanoBEIR/NanoBEIR-th__NanoDBPedia.md
  source_research:
    primary_source_type: task_paper
    paper_pdf_or_html_checked: true
    no_paper_note: null
  counts:
    queries: 50
    documents: 6045
    positive_qrels: 1158
  positives_per_query:
    average: 23.16
    min: 1
    median: 18.0
    max: 81
    multi_positive_queries: 48
    multi_positive_query_percent: 96.0
  text_stats_chars:
    query_mean: 30.92
    document_mean: 316.439702
  bm25:
    ndcg_at_10: 0.5043314872250944
    hit_at_10: 0.92
    source: dataset_candidate_subset
  candidate_subsets:
    bm25:
      config: bm25
      label: BM25
      source: dataset_candidate_subset
      top_k: 500
      ndcg_at_10: 0.5043314872
      hit_at_10: 0.92
      recall_at_100: 0.6519861831
      candidate_count_min: 500
      candidate_count_max: 500
      candidate_count_mean: 500.0
      query_count: 50
      query_coverage: 1.0
      relevant_coverage_at_100: 0.6519861831
    dense:
      config: harrier_oss_v1_270m
      label: Dense
      source: dataset_candidate_subset
      top_k: 500
      ndcg_at_10: 0.5468184394
      hit_at_10: 0.94
      recall_at_100: 0.6675302245
      candidate_count_min: 500
      candidate_count_max: 500
      candidate_count_mean: 500.0
      query_count: 50
      query_coverage: 1.0
      relevant_coverage_at_100: 0.6675302245
    reranking_hybrid:
      config: reranking_hybrid
      label: Reranking hybrid
      source: dataset_candidate_subset
      top_k: 100
      ndcg_at_10: 0.5482440542
      hit_at_10: 0.9
      recall_at_100: 0.6986183074
      candidate_count_min: 100
      candidate_count_max: 100
      candidate_count_mean: 100.0
      query_count: 50
      query_coverage: 1.0
      relevant_coverage_at_100: 0.6986183074
      safeguard_positive_rows: 0
      rows_with_101_candidates: 0
```
