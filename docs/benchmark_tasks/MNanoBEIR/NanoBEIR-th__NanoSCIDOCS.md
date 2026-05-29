# MNanoBEIR / NanoBEIR-th / NanoSCIDOCS

## Overview

SCIDOCS is scientific-document retrieval. `NanoBEIR-th__NanoSCIDOCS` uses Thai
translated paper-title style queries to retrieve scientific abstracts.

## Details

### What the Original Data Measures

[SPECTER](https://arxiv.org/abs/2004.07180) evaluates scientific document
representations over SCIDOCS. BEIR includes it as scientific retrieval, and
MMTEB provides multilingual context.

### Observed Data Profile

The task has 50 queries, 2,210 documents, and 244 qrels. Every query is
multi-positive, usually with 3 to 5 positives. Queries average 69.08 characters,
and documents average 820.44 characters.

### BM25 Difficulty

BM25 reaches nDCG@10 = 0.2641 and hit@10 = 0.7600. Median first-positive rank is
3.0, so semantic paper-topic matching matters.

### Training Data That May Help

Use non-overlapping scientific retrieval, citation ranking, Thai abstracts, and
multilingual academic search data. Exclude SCIDOCS, SPECTER evaluation records,
BEIR, and NanoBEIR.

### Synthetic Data Guidance

Generate Thai paper-title queries from abstracts, with hard negatives from the
same field but different contribution.

## Example Data

| Query | Positive document |
| --- | --- |
| ตัวแปลงแรงดันสูงหลายระดับ DC-DC ใหม่ (36 chars) | บทคัดย่อ: ตัวแปลงแรงดันไฟฟ้าหลายระดับกำลังกลายเป็นตัวเลือกใหม่สำหรับการแปลงพลังงานในแอปพลิเคชันที่มีพลังงานสูง ตัวแปลงแรงดันไฟฟ้าหลายระดับมักจะสังเคราะห์คลื่นแรงดันไฟฟ้าขั้นบันไดจากแรงดันไฟฟ้าของตัวเก็บประจุ DC หลายระดับ หนึ่ ... [truncated 225 chars](799 chars) |
| การเรียนรู้ฟิลด์สุ่มมาร์คอฟเกาส์เซียนที่เบาบางอย่างรวดเร็วโดยอิงจากการแยกแฟกเตอร์โชเลสกี้ (89 chars) | Please provide the text you would like to have translated into Thai. (68 chars) |
| การใช้เครือข่ายประสาทเทียมแบบพับซ้อนในการรู้จำภาพขนาดใหญ่ (57 chars) | ในงานนี้เราศึกษาผลกระทบของความลึกของเครือข่ายคอนโวลูชันต่อความแม่นยำในบริบทการรู้จำภาพขนาดใหญ่ ผลงานหลักของเราคือการประเมินเครือข่ายที่มีความลึกเพิ่มขึ้นอย่างละเอียด ซึ่งแสดงให้เห็นว่าการปรับปรุงที่สำคัญจากการกำหนดค่าที่มีอยู ... [truncated 225 chars](747 chars) |
| เสาอากาศวงแหวนแบนราบแบบกว้างที่มีการหมุนเวียนแบบวงกลมสำหรับระบบ RFID (68 chars) | ในเอกสารนี้เสนอเทคนิคการให้อาหารแบบแถบที่มีการเลี้ยวไปข้างหน้า (HMS) เพื่อให้ได้การจับคู่ความต้านทานที่ดีและรูปแบบการแผ่รังสีแบบกว้างขวางที่สมมาตรสำหรับเสาอากาศพatch ที่มีการขับเคลื่อนเดียวแบบวงกว้างที่มีการหมุนเป็นวงกลม ซึ่ง ... [truncated 225 chars](1112 chars) |
| การออกแบบแอปพลิเคชันเสมือนจริงเพื่อการศึกษาเกี่ยวกับกายวิภาคของหัวใจมนุษย์ (74 chars) | ในเอกสารนี้ เราได้นำเสนอการออกแบบและพัฒนาอุปกรณ์รวมใหม่สำหรับการวัดอัตราการเต้นของหัวใจโดยใช้ปลายนิ้วเพื่อปรับปรุงการประมาณอัตราการเต้นของหัวใจ เนื่องจากโรคที่เกี่ยวข้องกับหัวใจมีแนวโน้มเพิ่มขึ้นทุกวัน ความต้องการอุปกรณ์วัดอั ... [truncated 225 chars](1051 chars) |

## Dataset Information

| Field | Value |
| --- | --- |
| Nano set | MNanoBEIR |
| Backing dataset | NanoBEIR-th |
| Task / split | NanoSCIDOCS |
| Hugging Face dataset | [hakari-bench/NanoBEIR-th](https://huggingface.co/datasets/hakari-bench/NanoBEIR-th) |
| Language | th |
| Category | natural_language |
| Queries | 50 |
| Documents | 2,210 |
| Positive qrels | 244 |
| Positives per query avg | 4.88 |
| Positives per query min / median / max | 3 / 5.0 / 5 |
| Multi-positive queries | 50 (100.00%) |
| BM25 nDCG@10 | 0.2641 |
| BM25 hit@10 | 0.7600 |
| BM25 Recall@100 | 0.5615 |
| BM25 candidate subset | top-500 (`bm25`) |
| Dense nDCG@10 | 0.2915 |
| Dense hit@10 | 0.7600 |
| Dense Recall@100 | 0.6025 |
| Dense candidate subset | top-500 (`harrier_oss_v1_270m`) |
| Reranking hybrid nDCG@10 | 0.3165 |
| Reranking hybrid hit@10 | 0.7600 |
| Reranking hybrid Recall@100 | 0.6270 |
| Reranking hybrid candidate subset | top-100 plus optional rank-101 safeguard (`reranking_hybrid`) |
| Reranking hybrid candidates / query | 100-101 |
| Reranking hybrid safeguard rows | 2 |
| Query length avg chars | 69.08 |
| Document length avg chars | 820.44 |

### Public Sources

- [SPECTER](https://arxiv.org/abs/2004.07180), [BEIR](https://arxiv.org/abs/2104.08663), [MMTEB](https://arxiv.org/abs/2502.13595), and [NanoBEIR](https://huggingface.co/collections/zeta-alpha-ai/nanobeir).

### Hugging Face Links

- Nano dataset: [hakari-bench/NanoBEIR-th](https://huggingface.co/datasets/hakari-bench/NanoBEIR-th)
- Source collection: [Zeta Alpha NanoBEIR collection](https://huggingface.co/collections/zeta-alpha-ai/nanobeir)

### Source Reference Table

| Title | Year | Type | URL |
| --- | ---: | --- | --- |
| SPECTER: Document-level Representation Learning using Citation-informed Transformers | 2020 | task paper | https://arxiv.org/abs/2004.07180 |
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
  task_name: NanoSCIDOCS
  split_name: NanoSCIDOCS
  language: th
  category: natural_language
  document_path: docs/benchmark_tasks/MNanoBEIR/NanoBEIR-th__NanoSCIDOCS.md
  source_research:
    primary_source_type: task_paper
    paper_pdf_or_html_checked: true
    no_paper_note: null
  counts:
    queries: 50
    documents: 2210
    positive_qrels: 244
  positives_per_query:
    average: 4.88
    min: 3
    median: 5.0
    max: 5
    multi_positive_queries: 50
    multi_positive_query_percent: 100.0
  text_stats_chars:
    query_mean: 69.08
    document_mean: 820.435747
  bm25:
    ndcg_at_10: 0.26410424102080043
    hit_at_10: 0.76
    source: dataset_candidate_subset
  candidate_subsets:
    bm25:
      config: bm25
      label: BM25
      source: dataset_candidate_subset
      top_k: 500
      ndcg_at_10: 0.264104241
      hit_at_10: 0.76
      recall_at_100: 0.5614754098
      candidate_count_min: 500
      candidate_count_max: 500
      candidate_count_mean: 500.0
      query_count: 50
      query_coverage: 1.0
      relevant_coverage_at_100: 0.5614754098
    dense:
      config: harrier_oss_v1_270m
      label: Dense
      source: dataset_candidate_subset
      top_k: 500
      ndcg_at_10: 0.2914653283
      hit_at_10: 0.76
      recall_at_100: 0.6024590164
      candidate_count_min: 500
      candidate_count_max: 500
      candidate_count_mean: 500.0
      query_count: 50
      query_coverage: 1.0
      relevant_coverage_at_100: 0.6024590164
    reranking_hybrid:
      config: reranking_hybrid
      label: Reranking hybrid
      source: dataset_candidate_subset
      top_k: 100
      ndcg_at_10: 0.3164706262
      hit_at_10: 0.76
      recall_at_100: 0.6270491803
      candidate_count_min: 100
      candidate_count_max: 101
      candidate_count_mean: 100.04
      query_count: 50
      query_coverage: 1.0
      relevant_coverage_at_100: 0.6270491803
      safeguard_positive_rows: 2
      rows_with_101_candidates: 2
```
