# NanoMTEB-Thai / belebele_tha_thai_eng_latn

## Overview

`NanoMTEB-Thai / belebele_tha_thai_eng_latn` is the reverse cross-lingual
Belebele split: English questions retrieve Thai passages. It tests whether a
retriever can bridge English reading-comprehension queries to Thai translated
passages.

## Details

### What the Original Data Measures

[The Belebele Benchmark](https://arxiv.org/abs/2308.16884) is a parallel
reading-comprehension benchmark over 122 language variants. The retrieval
version treats each question as a query and the corresponding passage as the
document. Because Belebele is parallel, MTEB can create same-language and
cross-language retrieval directions from the same underlying passage set.

This split uses English queries and Thai documents, making it a strong test of
English-to-Thai semantic alignment rather than Thai lexical retrieval.

### Observed Data Profile

The Nano split has 200 queries, 488 documents, and 200 positive qrel rows. Each
query has one positive. English queries average 81.31 characters; Thai documents
average 456.17 characters. The sample begins with accordion-playing advice,
overscan in TV images, and American Revolutionary War passages.

### BM25 Difficulty

Using the dataset-provided BM25 candidate column, BM25 reaches nDCG@10 = 0.0395
and hit@10 = 0.0750. It ranks only 3 positives at rank 1 and 15 in the top 10.
All positives still appear within the top 100.

This is the hardest of the three Belebele Thai directions for BM25. The English
query shares almost no tokens with the Thai document, so sparse matching can only
use names, digits, and accidental script overlap.

### Training Data That May Help

English-to-Thai parallel retrieval, translated QA pairs, and multilingual
dual-encoder training are directly useful. Models should learn to represent
English questions and Thai passages in a shared space. Avoid using the same
Belebele evaluation items as training examples.

### Synthetic Data Guidance

Create English questions from Thai passages, or translate Thai
reading-comprehension questions into English while keeping Thai positives.
Include passages where the answer requires local comprehension, and add Thai
hard negatives from nearby topics.

## Example Data

| Query | Positive document |
| --- | --- |
| Which of the changes prompted by The French Revolution had a significant impact on working class citizens? (106 chars) | ผลกระทบทางสังคมและการเมืองมีมากมาย เช่น การใช้ระบบเมตริก การเปลี่ยนจากระบอบสมบูรณาญาสิทธิราชย์ไปสู่ระบอบสาธารณรัฐ ความเป็นชาตินิยม และความเชื่อว่าประเทศเป็นของประชาชน ไม่ใช่ของผู้ปกครองคนเดียว หลังการปฏิวัติ อาชีพต่าง ๆ ยังได ... [truncated 225 chars](553 chars) |
| According to the passage, who may have started an agriculture society? (70 chars) | เมื่อนานมาแล้วในช่วงศตวรรษที่สิบเก้าและยี่สิบ เชื่อกันว่าคนกลุ่มแรกที่อยู่​อาศัยในประเทศ​นิวซีแลนด์คือชนเผ่าเมารีซึ่งเป็นผู้ล่านกยักษ์โมอา จากนั้นทฤษฎีดังกล่าวได้ก่อให้เกิดแนวคิดที่ว่าชาวเมารีอพยพมาจากโพลีนีเซียในลักษณะเป็นกอ ... [truncated 225 chars](682 chars) |
| Which of the following accurately describes the practice of subsistence agriculture? (84 chars) | การเกษตรเพื่อดำรงชีพ คือการเกษตรที่กระทำพื่อผลิตอาหารให้เพียงพอต่อความต้องการของเกษตรกรและครอบครัวของพวกเขา การเกษตรเพื่อดำรงชีพคือระบบเรียบง่ายที่มักเป็นการเกษตรอินทรีย์โดยใช้เมล็ดพันธุ์ที่ขึ้นในเขตภูมิเวศผสานรวมกับการหมุนเว ... [truncated 225 chars](383 chars) |
| According to the passage, which of the following was one of China’s most violent eras? (86 chars) | จีนสมัยโบราณมีวิธีการแสดงช่วงเวลาต่าง ๆ ที่พิเศษไม่เหมือนใคร โดยแบ่งเป็นช่วงระยะของจีน หรือแต่ละตระกูลที่อยู่ในอำนาจเป็นราชวงศ์ที่มีลักษณะพิเศษ ในช่วงเวลาระหว่างแต่ละราชวงศ์เป็นยุคที่จังหวัดต่าง ๆ ซึ่งแยกจากกันไม่มีความมั่นคง ... [truncated 225 chars](565 chars) |
| When did King Tutankhamun gain notoriety? (41 chars) | "ใช่แล้วล่ะ! กษัตริย์ตุตันคามุนซึ่งบางครั้งก็ถูกเรียกว่า ""กษัตริย์ทุต"" หรือ ""กษัตริย์เด็ก"" คือหนึ่งในกษัตริย์อียิปต์โบราณที่เป็นที่รู้จักกันมากที่สุดในยุคปัจจุบัน ที่น่าสนใจคือ ผู้คนไม่คิดว่าเขาเป็นคนสำคัญมากในสมัยโบราณ แ ... [truncated 225 chars](550 chars) |

## Dataset Information

| Field | Value |
| --- | --- |
| Nano set | NanoMTEB-Thai |
| Backing dataset | NanoMTEB-Thai |
| Task / split | belebele_tha_thai_eng_latn |
| Hugging Face dataset | [hakari-bench/NanoMTEB-Thai](https://huggingface.co/datasets/hakari-bench/NanoMTEB-Thai) |
| Language | en, th |
| Category | natural_language |
| Queries | 200 |
| Documents | 488 |
| Positive qrels | 200 |
| BM25 nDCG@10 | 0.0944 |
| BM25 hit@10 | 0.1050 |
| BM25 Recall@100 | 0.2850 |
| BM25 candidate subset | top-500 (`bm25`) |
| Dense nDCG@10 | 0.8046 |
| Dense hit@10 | 0.8650 |
| Dense Recall@100 | 0.9850 |
| Dense candidate subset | top-500 (`harrier_oss_v1_270m`) |
| Reranking hybrid nDCG@10 | 0.2741 |
| Reranking hybrid hit@10 | 0.3150 |
| Reranking hybrid Recall@100 | 0.9850 |
| Reranking hybrid candidate subset | top-100 plus optional rank-101 safeguard (`reranking_hybrid`) |
| Reranking hybrid candidates / query | 100-101 |
| Reranking hybrid safeguard rows | 3 |
| Query length avg chars | 81.31 |
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
  task_name: belebele_tha_thai_eng_latn
  split_name: belebele_tha_thai_eng_latn
  language: multilingual
  category: natural_language
  document_path: docs/benchmark_tasks/NanoMTEB-Thai/belebele_tha_thai_eng_latn.md
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
    query_mean: 81.305
    document_mean: 456.165984
  bm25:
    ndcg_at_10: 0.0943957982414988
    hit_at_10: 0.105
    source: dataset_candidate_subset
  example_count: 5
  candidate_subsets:
    bm25:
      config: bm25
      label: BM25
      source: dataset_candidate_subset
      top_k: 500
      ndcg_at_10: 0.0943957982
      hit_at_10: 0.105
      recall_at_100: 0.285
      candidate_count_min: 488
      candidate_count_max: 488
      candidate_count_mean: 488.0
      query_count: 200
      query_coverage: 1.0
      relevant_coverage_at_100: 0.285
    dense:
      config: harrier_oss_v1_270m
      label: Dense
      source: dataset_candidate_subset
      top_k: 500
      ndcg_at_10: 0.8045538219
      hit_at_10: 0.865
      recall_at_100: 0.985
      candidate_count_min: 488
      candidate_count_max: 488
      candidate_count_mean: 488.0
      query_count: 200
      query_coverage: 1.0
      relevant_coverage_at_100: 0.985
    reranking_hybrid:
      config: reranking_hybrid
      label: Reranking hybrid
      source: dataset_candidate_subset
      top_k: 100
      ndcg_at_10: 0.2741353669
      hit_at_10: 0.315
      recall_at_100: 0.985
      candidate_count_min: 100
      candidate_count_max: 101
      candidate_count_mean: 100.015
      query_count: 200
      query_coverage: 1.0
      relevant_coverage_at_100: 0.985
      safeguard_positive_rows: 3
      rows_with_101_candidates: 3
```
