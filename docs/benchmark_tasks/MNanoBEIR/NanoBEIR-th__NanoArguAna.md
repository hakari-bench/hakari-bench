# MNanoBEIR / NanoBEIR-th / NanoArguAna

## Overview

ArguAna is argument-counterargument retrieval. `NanoBEIR-th__NanoArguAna` uses
Thai translated argumentative passages as queries and retrieves paired
arguments.

## Details

### What the Original Data Measures

[ArguAna](https://aclanthology.org/P18-1023/) is used in BEIR for argument
retrieval, where relevance depends on stance and response relation. MMTEB
provides the multilingual context.

### Observed Data Profile

The task has 50 queries, 3,635 documents, and 50 qrels. Every query has one
positive. Queries average 820.62 characters, and documents average 860.05
characters.

### BM25 Difficulty

BM25 reaches nDCG@10 = 0.4051 and hit@10 = 0.7200. Median first-positive rank is
4.5; lexical overlap helps, but stance matching is still needed.

### Training Data That May Help

Use Thai debate retrieval, argument mining, counterargument pairs, and
stance-aware ranking. Exclude ArguAna, BEIR, NanoBEIR, and translated overlaps.

### Synthetic Data Guidance

Generate Thai claims and counterarguments. Hard negatives should discuss the
same topic but respond to a different stance or premise.

## Example Data

| Query | Positive document |
| --- | --- |
| สาธารณชนไม่สนใจการปฏิรูป ไม่ว่าจะเป็นการปฏิรูปสภาขุนนางควรเป็นลำดับความสำคัญสูงสุดในสภาพเศรษฐกิจปัจจุบันหรือไม่เป็นเรื่องที่ถกเถียงกันได้ ยิ่งไปกว่านั้นรัฐบาลผสมจะสามารถเริ่มต้นและผลักดันมาตรการดังกล่าวได้หรือไม่ ความพยายามใน ... [truncated 225 chars](528 chars) | แคมเปญ AV ไม่สามารถเปรียบเทียบกับการปฏิรูปสภาขุนนางได้ นอกจากนี้ ไม่ควรเข้าใจผิดว่าประชาชนที่มีข้อมูลผิดพลาดจากการเมืองเป็นความเฉยเมย บ่อยครั้งที่ผู้มีสิทธิเลือกตั้งแสดงออกว่าพวกเขาเฉยเมยเพราะรู้สึกว่าพวกเขาไม่สามารถเปลี่ยนแป ... [truncated 225 chars](370 chars) |
| การขยายสนามบินฮีทโธรว์มีความสำคัญต่อเศรษฐกิจ การขยายสนามบินฮีทโธรว์จะทำให้มั่นใจได้ว่ามีงานปัจจุบันจำนวนมากและสร้างงานใหม่ด้วย ขณะนี้สนามบินฮีทโธรว์สนับสนุนงานประมาณ 250,000 ตำแหน่ง [1] นอกจากนี้ยังมีคนอีกหลายแสนคนที่พึ่งพากา ... [truncated 225 chars](911 chars) | ชุมชนธุรกิจยังห่างไกลจากการเป็นเอกภาพในความสนับสนุนที่กล่าวอ้างต่อการสร้างรันเวย์ที่สาม การสำรวจแสดงให้เห็นว่าหลายธุรกิจที่มีอิทธิพลจริง ๆ แล้วไม่สนับสนุนการขยายตัว จดหมายที่แสดงความกังวลได้รับการลงนามโดยจัสติน คิง ประธานเจ้า ... [truncated 225 chars](1032 chars) |
| ผู้คนได้รับทางเลือกมากเกินไป ซึ่งทำให้พวกเขาน้อยใจมากขึ้น การโฆษณานำไปสู่หลายคนที่รู้สึกท่วมท้นจากความต้องการที่ไม่มีที่สิ้นสุดในการตัดสินใจระหว่างความต้องการที่แข่งขันกันสำหรับความสนใจของพวกเขา – สิ่งนี้เรียกว่าการปกครองของท ... [truncated 225 chars](797 chars) | ผู้คนไม่พอใจเพราะพวกเขาไม่สามารถมีทุกอย่างได้ ไม่ใช่เพราะพวกเขาได้รับทางเลือกมากเกินไปและรู้สึกเครียด ในความเป็นจริง โฆษณามีบทบาทสำคัญในการทำให้แน่ใจว่าผู้คนใช้เงินที่มีอยู่ไปกับผลิตภัณฑ์ที่เหมาะสมที่สุดสำหรับตัวเอง หากไม่มีก ... [truncated 225 chars](788 chars) |
| การโจมตีทางไซเบอร์มักเกิดขึ้นโดยผู้ที่ไม่ใช่รัฐ การโจมตีทางไซเบอร์มักเกิดขึ้นโดยผู้ที่ไม่ใช่รัฐ เช่น ผู้ก่อการร้ายทางไซเบอร์หรือแฮกติวิสต์ (นักเคลื่อนไหวทางสังคมที่แฮ็ก) โดยไม่มีการมีส่วนร่วมของรัฐที่แท้จริง ตัวอย่างเช่น ในปี ... [truncated 225 chars](903 chars) | ในกรณีที่มีการโจมตีจากผู้ไม่ใช่รัฐ ผู้เชี่ยวชาญหลายคนในกฎหมายระหว่างประเทศเห็นพ้องกันว่ารัฐยังสามารถตอบโต้ในลักษณะการป้องกันตนเองได้หากรัฐอื่น 'ไม่เต็มใจหรือไม่สามารถดำเนินการที่มีประสิทธิภาพ' เพื่อตอบสนองต่อการโจมตีที่เกิดจา ... [truncated 225 chars](533 chars) |
| เนื่องจากศาสนาส่งเสริมความแน่นอนของความเชื่อ ความเกลียดชังที่ได้รับแรงบันดาลใจจากพระเจ้าเป็นเรื่องง่ายที่จะใช้เพื่อให้เหตุผลและส่งเสริมการกระทำที่รุนแรงและการปฏิบัติที่เลือกปฏิบัติ เสรีภาพในการพูดต้องมาเป็นอันดับสองเมื่อมีควา ... [truncated 225 chars](953 chars) | ไม่มีใครถูกบังคับให้กระทำการใช้ความรุนแรงโดยคำพูดของผู้อื่น; นี่เป็นทางเลือกของพวกเขาเอง เช่นเดียวกัน มีคนจำนวนมากที่มีความคิดเห็นที่อาจถือว่าเป็นการเหยียดเชื้อชาติ แต่กลับรู้สึกตกใจต่อการกระทำความรุนแรง มันเป็นหลักการพื้นฐาน ... [truncated 225 chars](541 chars) |

## Dataset Information

| Field | Value |
| --- | --- |
| Nano set | MNanoBEIR |
| Backing dataset | NanoBEIR-th |
| Task / split | NanoArguAna |
| Hugging Face dataset | [hakari-bench/NanoBEIR-th](https://huggingface.co/datasets/hakari-bench/NanoBEIR-th) |
| Language | th |
| Category | natural_language |
| Queries | 50 |
| Documents | 3,635 |
| Positive qrels | 50 |
| BM25 nDCG@10 | 0.4051 |
| BM25 hit@10 | 0.7200 |
| BM25 Recall@100 | 0.9400 |
| BM25 candidate subset | top-500 (`bm25`) |
| Dense nDCG@10 | 0.3721 |
| Dense hit@10 | 0.7000 |
| Dense Recall@100 | 0.9000 |
| Dense candidate subset | top-500 (`harrier_oss_v1_270m`) |
| Reranking hybrid nDCG@10 | 0.4349 |
| Reranking hybrid hit@10 | 0.7200 |
| Reranking hybrid Recall@100 | 0.9200 |
| Reranking hybrid candidate subset | top-100 plus optional rank-101 safeguard (`reranking_hybrid`) |
| Reranking hybrid candidates / query | 100-101 |
| Reranking hybrid safeguard rows | 4 |
| Query length avg chars | 820.62 |
| Document length avg chars | 860.05 |

### Public Sources

- [ArguAna](https://aclanthology.org/P18-1023/), [BEIR](https://arxiv.org/abs/2104.08663), [MMTEB](https://arxiv.org/abs/2502.13595), and [NanoBEIR](https://huggingface.co/collections/zeta-alpha-ai/nanobeir).

### Hugging Face Links

- Nano dataset: [hakari-bench/NanoBEIR-th](https://huggingface.co/datasets/hakari-bench/NanoBEIR-th)
- Source collection: [Zeta Alpha NanoBEIR collection](https://huggingface.co/collections/zeta-alpha-ai/nanobeir)

### Source Reference Table

| Title | Year | Type | URL |
| --- | ---: | --- | --- |
| Argument Mining for Understanding Peer Reviews | 2018 | task paper | https://aclanthology.org/P18-1023/ |
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
  task_name: NanoArguAna
  split_name: NanoArguAna
  language: th
  category: natural_language
  document_path: docs/benchmark_tasks/MNanoBEIR/NanoBEIR-th__NanoArguAna.md
  source_research:
    primary_source_type: task_paper
    paper_pdf_or_html_checked: true
    no_paper_note: null
  counts:
    queries: 50
    documents: 3635
    positive_qrels: 50
  positives_per_query:
    average: 1.0
    min: 1
    median: 1.0
    max: 1
    multi_positive_queries: 0
    multi_positive_query_percent: 0.0
  text_stats_chars:
    query_mean: 820.62
    document_mean: 860.05282
  bm25:
    ndcg_at_10: 0.40511531684461494
    hit_at_10: 0.72
    source: dataset_candidate_subset
  candidate_subsets:
    bm25:
      config: bm25
      label: BM25
      source: dataset_candidate_subset
      top_k: 500
      ndcg_at_10: 0.4051153168
      hit_at_10: 0.72
      recall_at_100: 0.94
      candidate_count_min: 500
      candidate_count_max: 500
      candidate_count_mean: 500.0
      query_count: 50
      query_coverage: 1.0
      relevant_coverage_at_100: 0.94
    dense:
      config: harrier_oss_v1_270m
      label: Dense
      source: dataset_candidate_subset
      top_k: 500
      ndcg_at_10: 0.3720891677
      hit_at_10: 0.7
      recall_at_100: 0.9
      candidate_count_min: 500
      candidate_count_max: 500
      candidate_count_mean: 500.0
      query_count: 50
      query_coverage: 1.0
      relevant_coverage_at_100: 0.9
    reranking_hybrid:
      config: reranking_hybrid
      label: Reranking hybrid
      source: dataset_candidate_subset
      top_k: 100
      ndcg_at_10: 0.4348827613
      hit_at_10: 0.72
      recall_at_100: 0.92
      candidate_count_min: 100
      candidate_count_max: 101
      candidate_count_mean: 100.08
      query_count: 50
      query_coverage: 1.0
      relevant_coverage_at_100: 0.92
      safeguard_positive_rows: 4
      rows_with_101_candidates: 4
```
