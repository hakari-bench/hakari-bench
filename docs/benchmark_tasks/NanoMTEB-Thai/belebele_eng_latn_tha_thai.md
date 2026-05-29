# NanoMTEB-Thai / belebele_eng_latn_tha_thai

## Overview

`NanoMTEB-Thai / belebele_eng_latn_tha_thai` is a cross-lingual Belebele
retrieval split. Thai questions retrieve English passages. It tests whether a
retriever can map Thai reading-comprehension questions to the corresponding
English source passage.

## Details

### What the Original Data Measures

[The Belebele Benchmark](https://arxiv.org/abs/2308.16884) introduces a fully
parallel multiple-choice reading-comprehension dataset in 122 language variants.
Each question is based on a short FLORES-200 passage and has four answer
options. The MTEB retrieval conversion uses the question as the query and the
passage as the document.

This split is cross-lingual: queries are Thai and documents are English. It is
therefore not only a reading-comprehension retrieval task, but also a
translation-alignment task over parallel passages.

### Observed Data Profile

The Nano split has 200 queries, 488 documents, and 200 positive qrel rows. Each
query has one positive passage. Queries average 57.67 characters and documents
average 475.51 characters. The sampled Thai queries ask which statement follows
from a passage or where/why something happened; positives are English
paragraphs.

### BM25 Difficulty

Using the dataset-provided BM25 candidate column, BM25 reaches nDCG@10 = 0.0809
and hit@10 = 0.0950. It ranks 15 positives at rank 1 and 19 in the top 10. All
positives are present within the top 100.

The low score is expected because the query and document languages differ. BM25
can only exploit shared named entities, numbers, and punctuation. It fails on
ordinary Thai-to-English semantic matches such as questions about TV overscan or
historical passages.

### Training Data That May Help

Useful training includes Thai-English parallel retrieval pairs,
question-to-passage translation pairs, and multilingual reading-comprehension
retrieval data. Belebele train/evaluation overlap should be avoided; other
parallel corpora can be used to teach Thai queries to retrieve English passages.

### Synthetic Data Guidance

Generate Thai questions from English passages and keep the positives in English.
Include questions that require sentence-level passage comprehension, not only
entity lookup. Hard negatives should be English passages from the same broad
topic but answering a different Thai question.

## Example Data

| Query | Positive document |
| --- | --- |
| การเปลี่ยนแปลงใดที่เกิดจากการปฏิวัติฝรั่งเศสมีผลกระทบอย่างมากต่อพลเมืองชนชั้นแรงงาน (83 chars) | There are a lot of social and political effects such as the use of metric system, a shift from absolutism to republicanism, nationalism and the belief the country belongs to the people not to one sole ruler. Also after the Re ... [truncated 225 chars](576 chars) |
| จากบทความ ใครน่าจะเป็นผู้สร้างสังคมเกษตรกรรมขึ้น (48 chars) | For a long time during the nineteenth and twentieth centuries, it was believed the first inhabitants of New Zealand were the Maori people, who hunted giant birds called moas. The theory then established the idea that the Maor ... [truncated 225 chars](747 chars) |
| ข้อใดต่อไปนี้กล่าวถึงเกษตรกรรมเพื่อยังชีพได้ถูกต้อง (51 chars) | Subsistence agriculture is agriculture carried out for the production of enough food to meet just the needs of the agriculturalist and his/her family. Subsistence agriculture is a simple, often organic, system using saved see ... [truncated 225 chars](456 chars) |
| จากบทความ ข้อใดเป็นยุคที่มีการนองเลือดที่สุดยุคหนึ่งของจีน (58 chars) | Ancient China had a unique way of showing different time periods; each stage of China or each family that was in power was a distinctive dynasty. Also between each dynasty was an unstable age of divided provinces. The best-kn ... [truncated 225 chars](596 chars) |
| กษัตริย์ตุตันคามุนมีชื่อเสียงในแง่ลบตอนไหน (42 chars) | "Yes! King Tutankhamun, sometimes referred to as ""King Tut"" or ""The Boy King"", is one of the most well known ancient Egyptian kings in modern times. Interestingly, he was not considered to be very important in ancient tim ... [truncated 225 chars](570 chars) |

## Dataset Information

| Field | Value |
| --- | --- |
| Nano set | NanoMTEB-Thai |
| Backing dataset | NanoMTEB-Thai |
| Task / split | belebele_eng_latn_tha_thai |
| Hugging Face dataset | [hakari-bench/NanoMTEB-Thai](https://huggingface.co/datasets/hakari-bench/NanoMTEB-Thai) |
| Language | th, en |
| Category | natural_language |
| Queries | 200 |
| Documents | 488 |
| Positive qrels | 200 |
| BM25 nDCG@10 | 0.0891 |
| BM25 hit@10 | 0.1050 |
| BM25 Recall@100 | 0.3550 |
| BM25 candidate subset | top-500 (`bm25`) |
| Dense nDCG@10 | 0.8483 |
| Dense hit@10 | 0.9150 |
| Dense Recall@100 | 0.9800 |
| Dense candidate subset | top-500 (`harrier_oss_v1_270m`) |
| Reranking hybrid nDCG@10 | 0.2919 |
| Reranking hybrid hit@10 | 0.3500 |
| Reranking hybrid Recall@100 | 0.9750 |
| Reranking hybrid candidate subset | top-100 plus optional rank-101 safeguard (`reranking_hybrid`) |
| Reranking hybrid candidates / query | 100-101 |
| Reranking hybrid safeguard rows | 5 |
| Query length avg chars | 57.67 |
| Document length avg chars | 475.51 |

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
  task_name: belebele_eng_latn_tha_thai
  split_name: belebele_eng_latn_tha_thai
  language: multilingual
  category: natural_language
  document_path: docs/benchmark_tasks/NanoMTEB-Thai/belebele_eng_latn_tha_thai.md
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
    document_mean: 475.510246
  bm25:
    ndcg_at_10: 0.08905559698767598
    hit_at_10: 0.105
    source: dataset_candidate_subset
  example_count: 5
  candidate_subsets:
    bm25:
      config: bm25
      label: BM25
      source: dataset_candidate_subset
      top_k: 500
      ndcg_at_10: 0.089055597
      hit_at_10: 0.105
      recall_at_100: 0.355
      candidate_count_min: 488
      candidate_count_max: 488
      candidate_count_mean: 488.0
      query_count: 200
      query_coverage: 1.0
      relevant_coverage_at_100: 0.355
    dense:
      config: harrier_oss_v1_270m
      label: Dense
      source: dataset_candidate_subset
      top_k: 500
      ndcg_at_10: 0.848315108
      hit_at_10: 0.915
      recall_at_100: 0.98
      candidate_count_min: 488
      candidate_count_max: 488
      candidate_count_mean: 488.0
      query_count: 200
      query_coverage: 1.0
      relevant_coverage_at_100: 0.98
    reranking_hybrid:
      config: reranking_hybrid
      label: Reranking hybrid
      source: dataset_candidate_subset
      top_k: 100
      ndcg_at_10: 0.2919345287
      hit_at_10: 0.35
      recall_at_100: 0.975
      candidate_count_min: 100
      candidate_count_max: 101
      candidate_count_mean: 100.025
      query_count: 200
      query_coverage: 1.0
      relevant_coverage_at_100: 0.975
      safeguard_positive_rows: 5
      rows_with_101_candidates: 5
```
