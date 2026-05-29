# MNanoBEIR / NanoBEIR-th / NanoSciFact

## Overview

SciFact is scientific claim evidence retrieval. `NanoBEIR-th__NanoSciFact` uses
Thai translated scientific claims to retrieve abstract evidence.

## Details

### What the Original Data Measures

[SciFact](https://arxiv.org/abs/2004.14974) evaluates scientific claim
verification using abstracts. BEIR uses the retrieval portion, and MMTEB gives
multilingual context.

### Observed Data Profile

The task has 50 queries, 2,919 documents, and 56 qrels. Most queries have one
positive. Queries average 92.74 characters, and documents average 1,328.85
characters.

### BM25 Difficulty

BM25 reaches nDCG@10 = 0.6334 and hit@10 = 0.7800. Median first-positive rank is
2.0, so scientific terms help but evidence discrimination remains important.

### Training Data That May Help

Use Thai scientific claim verification, biomedical abstract retrieval, and
multilingual evidence retrieval. Exclude SciFact, BEIR, NanoBEIR, and translated
evaluation examples.

### Synthetic Data Guidance

Generate Thai scientific claims from abstracts, with hard negatives sharing
entities or methods but not supporting the claim.

## Example Data

| Query | Positive document |
| --- | --- |
| การควบคุมฟังก์ชันของเมมเบรนราฟต์ของ Ly49Q ในการเคลื่อนที่ของนิวโทรฟิลไปยังจุดอักเสบ (83 chars) | นิวโทรฟิลจะเกิดการพอระเบียบและเคลื่อนที่ในทิศทางอย่างรวดเร็วเพื่อแทรกซึมเข้าสู่จุดติดเชื้อและการอักเสบ ที่นี่เราจะแสดงให้เห็นว่า ตัวรับ MHC I ที่มีฤทธิ์ยับยั้ง Ly49Q มีความสำคัญต่อการพอระเบียบอย่างรวดเร็วและการแทรกซึมของนิวโท ... [truncated 225 chars](942 chars) |
| การบำบัดด้วยยาต้านไวรัสและผลกระทบต่อการลดอัตราการติดเชื้อวัณโรคในกลุ่ม CD4 ที่หลากหลาย (86 chars) | พื้นหลัง การติดเชื้อไวรัสภูมิคุ้มกันบกพร่องของมนุษย์ (HIV) เป็นปัจจัยเสี่ยงที่สำคัญที่สุดในการพัฒนาวัณโรคและได้กระตุ้นให้เกิดการกลับมาของโรคนี้ โดยเฉพาะในแอฟริกาตอนใต้ของซาฮารา ในปี 2010 มีการประมาณว่ามีผู้ป่วยวัณโรคใหม่ประมา ... [truncated 225 chars](1895 chars) |
| การเพิ่มการแสดงออกอย่างรวดเร็วและการแสดงออกพื้นฐานที่สูงขึ้นของยีนที่กระตุ้นโดยอินเตอร์เฟอรอนลดการอยู่รอดของเซลล์ประสาทเกรนูลที่ติดเชื้อไวรัสเวสต์ไนล์หรือไม่? (158 chars) | แม้ว่าความไวของเซลล์ประสาทในสมองต่อการติดเชื้อจุลินทรีย์จะเป็นปัจจัยหลักที่กำหนดผลลัพธ์ทางคลินิก แต่ข้อมูลเกี่ยวกับปัจจัยโมเลกุลที่ควบคุมความเปราะบางนี้ยังมีน้อย ที่นี่เราจะแสดงให้เห็นว่าเซลล์ประสาทสองประเภทจากภูมิภาคสมองที่แ ... [truncated 225 chars](1021 chars) |
| การตรวจคัดกรองมะเร็งปากมดลูกขั้นต้นด้วยการตรวจหา HPV มีความไวเชิงยาวที่สูงกว่าซิโทโลยีแบบดั้งเดิมในการตรวจหานีโอพลาสเซียในปากมดลูกเกรด 2 หรือไม่? (145 chars) | ภูมิหลัง การคัดกรองมะเร็งปากมดลูกโดยอิงจากการตรวจหาเชื้อไวรัส HPV (human papillomavirus) จะเพิ่มความไวในการตรวจจับเนื้องอกในปากมดลูกระดับสูง (เกรด 2 หรือ 3) แต่ไม่ทราบว่าการเพิ่มขึ้นนี้เป็นการวินิจฉัยเกินจริงหรือเป็นการป้องกั ... [truncated 225 chars](1904 chars) |
| การบล็อกการมีปฏิสัมพันธ์ระหว่าง TDP-43 กับโปรตีนที่เกี่ยวข้องกับระบบหายใจซับซ้อน I ND3 และ ND6 ส่งผลให้เกิดการสูญเสียเซลล์ประสาทที่เกิดจาก TDP-43 เพิ่มขึ้น (155 chars) | การกลายพันธุ์ทางพันธุกรรมในโปรตีนที่จับกับดีเอ็นเอ TAR (TARDBP หรือที่รู้จักในชื่อ TDP-43) ทำให้เกิดโรคกล้ามเนื้ออ่อนแรงข้างเดียว (ALS) และการเพิ่มขึ้นของการมีอยู่ของ TDP-43 (ที่เข้ารหัสโดย TARDBP) ในไซโตพลาสซึมเป็นลักษณะทางพ ... [truncated 225 chars](1252 chars) |

## Dataset Information

| Field | Value |
| --- | --- |
| Nano set | MNanoBEIR |
| Backing dataset | NanoBEIR-th |
| Task / split | NanoSciFact |
| Hugging Face dataset | [hakari-bench/NanoBEIR-th](https://huggingface.co/datasets/hakari-bench/NanoBEIR-th) |
| Language | th |
| Category | natural_language |
| Queries | 50 |
| Documents | 2,919 |
| Positive qrels | 56 |
| Positives per query avg | 1.12 |
| Positives per query min / median / max | 1 / 1.0 / 4 |
| Multi-positive queries | 4 (8.00%) |
| BM25 nDCG@10 | 0.6334 |
| BM25 hit@10 | 0.7800 |
| BM25 Recall@100 | 0.8571 |
| BM25 candidate subset | top-500 (`bm25`) |
| Dense nDCG@10 | 0.5713 |
| Dense hit@10 | 0.7200 |
| Dense Recall@100 | 0.8571 |
| Dense candidate subset | top-500 (`harrier_oss_v1_270m`) |
| Reranking hybrid nDCG@10 | 0.6206 |
| Reranking hybrid hit@10 | 0.7400 |
| Reranking hybrid Recall@100 | 0.9286 |
| Reranking hybrid candidate subset | top-100 plus optional rank-101 safeguard (`reranking_hybrid`) |
| Reranking hybrid candidates / query | 100-101 |
| Reranking hybrid safeguard rows | 4 |
| Query length avg chars | 92.74 |
| Document length avg chars | 1,328.85 |

### Public Sources

- [SciFact](https://arxiv.org/abs/2004.14974), [BEIR](https://arxiv.org/abs/2104.08663), [MMTEB](https://arxiv.org/abs/2502.13595), and [NanoBEIR](https://huggingface.co/collections/zeta-alpha-ai/nanobeir).

### Hugging Face Links

- Nano dataset: [hakari-bench/NanoBEIR-th](https://huggingface.co/datasets/hakari-bench/NanoBEIR-th)
- Source collection: [Zeta Alpha NanoBEIR collection](https://huggingface.co/collections/zeta-alpha-ai/nanobeir)

### Source Reference Table

| Title | Year | Type | URL |
| --- | ---: | --- | --- |
| SciFact: Fact or Fiction: Verifying Scientific Claims | 2020 | task paper | https://arxiv.org/abs/2004.14974 |
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
  task_name: NanoSciFact
  split_name: NanoSciFact
  language: th
  category: natural_language
  document_path: docs/benchmark_tasks/MNanoBEIR/NanoBEIR-th__NanoSciFact.md
  source_research:
    primary_source_type: task_paper
    paper_pdf_or_html_checked: true
    no_paper_note: null
  counts:
    queries: 50
    documents: 2919
    positive_qrels: 56
  positives_per_query:
    average: 1.12
    min: 1
    median: 1.0
    max: 4
    multi_positive_queries: 4
    multi_positive_query_percent: 8.0
  text_stats_chars:
    query_mean: 92.74
    document_mean: 1328.849606
  bm25:
    ndcg_at_10: 0.6334076985810911
    hit_at_10: 0.78
    source: dataset_candidate_subset
  candidate_subsets:
    bm25:
      config: bm25
      label: BM25
      source: dataset_candidate_subset
      top_k: 500
      ndcg_at_10: 0.6334076986
      hit_at_10: 0.78
      recall_at_100: 0.8571428571
      candidate_count_min: 500
      candidate_count_max: 500
      candidate_count_mean: 500.0
      query_count: 50
      query_coverage: 1.0
      relevant_coverage_at_100: 0.8571428571
    dense:
      config: harrier_oss_v1_270m
      label: Dense
      source: dataset_candidate_subset
      top_k: 500
      ndcg_at_10: 0.5712719406
      hit_at_10: 0.72
      recall_at_100: 0.8571428571
      candidate_count_min: 500
      candidate_count_max: 500
      candidate_count_mean: 500.0
      query_count: 50
      query_coverage: 1.0
      relevant_coverage_at_100: 0.8571428571
    reranking_hybrid:
      config: reranking_hybrid
      label: Reranking hybrid
      source: dataset_candidate_subset
      top_k: 100
      ndcg_at_10: 0.6205755909
      hit_at_10: 0.74
      recall_at_100: 0.9285714286
      candidate_count_min: 100
      candidate_count_max: 101
      candidate_count_mean: 100.08
      query_count: 50
      query_coverage: 1.0
      relevant_coverage_at_100: 0.9285714286
      safeguard_positive_rows: 4
      rows_with_101_candidates: 4
```
