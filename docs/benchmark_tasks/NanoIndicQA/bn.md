# NanoIndicQA / bn

## Overview

`NanoIndicQA / bn` is the Bengali split of IndicQA retrieval. Bengali
reading-comprehension questions retrieve the Bengali context paragraph that
supports the answer.

## Details

### What the Original Data Measures

[Towards Leaving No Indic Language Behind](https://arxiv.org/abs/2212.05409)
describes IndicXTREME and its IndicQA component as a manually curated
cloze-style reading-comprehension benchmark for Indic languages. The retrieval
formulation uses questions as queries and context paragraphs as documents.

### Observed Data Profile

The Nano split has 200 queries, 250 documents, and 201 positive qrel rows. One
query has two positives; the rest have one. Queries average 52.08 characters and
documents average 2,196.01 characters. Many questions in the sample are tied to
the same longer historical paragraph.

### BM25 Difficulty

Using the dataset-provided BM25 candidate column, BM25 reaches nDCG@10 = 0.5077
and hit@10 = 0.6750. It ranks 71 positives at rank 1 and 135 in the top 10. All
positives are within the top 100.

Sparse retrieval handles repeated Bengali names well, but it struggles with
questions that rely on context rather than direct term repetition.

### Training Data That May Help

Bengali QA context retrieval, Bengali Wikipedia passage retrieval, and
IndicQA-style multilingual training will help. Same-topic paragraphs should be
used as hard negatives.

### Synthetic Data Guidance

Generate Bengali cloze-style or factual questions from context paragraphs and
pair them with the full paragraph. Include multiple questions per paragraph,
dates, people, actions, and event descriptions.

## Example Data

| Query | Positive document |
| --- | --- |
| কার দ্বারা পাঞ্জাবের জালিয়ানওয়ালাবাগে বেসামরিক লোকদের গণহত্যা জনরোষ সৃষ্টি করে এবং সহিংসতা বৃদ্ধি করে ? (105 chars) | অন্যায়ের বিরুদ্ধে গান্ধীর অস্ত্র ছিল অসহযোগ এবং শান্তিপূর্ণ প্রতিরোধ। পাঞ্জাবের জালিয়ানওয়ালাবাগে সাধারণ মানুষের উপরে ব্রিটিশ সরকার কর্তৃক সংগঠিত হত্যাকাণ্ডের ফলে জনসাধারণ ক্ষুব্ধ হয়ে যায় এবং সহিংসতার মাত্রা বৃদ্ধি পায়। ... [truncated 225 chars](1277 chars) |
| ঘুরি রাজবংশের অন্যতম শাসক কে ছিলেন ? (36 chars) | আফগানিস্থানে সম্প্রতি মেন্‌রোজ প্রদেশের ‘শাহ্ পোশ্’-এ খননকালে একটি মিনারের ধ্বংসাবশেষ আবিষ্কৃত হয়েছে। একটি মস্‌জিদের অনতিদূরে সেই মিনারটি নির্মিত হয়েছিল নবম অথবা দশম-শতাব্দীর প্রথম পাদে। সামানিদ্-ইটের তৈরি এই মিনারের শুধু প ... [truncated 225 chars](961 chars) |
| বাংলাদেশের জাতীয় খেলার নাম কি ? (31 chars) | ঈদুল ফিতরের আগের দিনটি বাংলাদেশে ‘চাঁদ রাত’ নামে পরিচিত। ছোট ছোট বাচ্চারা এ দিনটি অনেক সময়ই আতশবাজির মাধ্যমে পটকা ফাটিয়ে উদ্‌যাপন করে। ঈদুল আজহার সময় শহরাঞ্চলে প্রচুর কোরবানির পশুর আগমন হয় এবং এটি নিয়ে শিশুদের মাঝে একটি ... [truncated 225 chars](2396 chars) |
| এই তাজমহলের বড় গম্বুজের চূড়ায় স্বর্ণের কাজ কে করেছিলেন ? (59 chars) | আরও তামার পাইপ দিয়ে উত্তর-দক্ষিণ দিকে নালার ঝরনাগুলোতে পানি সরবরাহ করা হতো। সহায়ক আরও নালা খনন করা হয়েছিল পুরো বাগানে সেচ দেয়ার জন্য। ঝরনার পাইপগুলো সরাসরি সরবরাহ পাইপের সাথে যুক্ত ছিল না। এর বদলে, প্রতিটি ঝরনার নিচে একটি ... [truncated 225 chars](2169 chars) |
| সম্রাট অশোককে চণ্ড অশোক বলার কারণ কি? (37 chars) | অশোকের ক্রূর স্বভাবের জন্য তাকে চণ্ড অশোক নামে অভিহিত করা হত। অধ্যাপক চার্লস ড্রেকেমেয়ার অবশ্য বৌদ্ধ প্রবাদগুলিকে অতিশয়োক্তি হিসেবে বিবেচনা করেছেন। তার মতে, কোপণ স্বভাবের অশোক যে বৌদ্ধ ধর্মে প্রভাবিত হয়ে একজন ধার্মিক ব্যক্ ... [truncated 225 chars](1193 chars) |

## Dataset Information

| Field | Value |
| --- | --- |
| Nano set | NanoIndicQA |
| Backing dataset | NanoIndicQA |
| Task / split | bn |
| Hugging Face dataset | [hakari-bench/NanoIndicQA](https://huggingface.co/datasets/hakari-bench/NanoIndicQA) |
| Language | bn |
| Category | natural_language |
| Queries | 200 |
| Documents | 250 |
| Positive qrels | 201 |
| BM25 nDCG@10 | 0.6971 |
| BM25 hit@10 | 0.8150 |
| BM25 Recall@100 | 0.8955 |
| BM25 candidate subset | top-500 (`bm25`) |
| Dense nDCG@10 | 0.7773 |
| Dense hit@10 | 0.8700 |
| Dense Recall@100 | 0.9900 |
| Dense candidate subset | top-500 (`harrier_oss_v1_270m`) |
| Reranking hybrid nDCG@10 | 0.7460 |
| Reranking hybrid hit@10 | 0.8350 |
| Reranking hybrid Recall@100 | 0.9701 |
| Reranking hybrid candidate subset | top-100 plus optional rank-101 safeguard (`reranking_hybrid`) |
| Reranking hybrid candidates / query | 100-101 |
| Reranking hybrid safeguard rows | 6 |
| Query length avg chars | 52.08 |
| Document length avg chars | 2,196.01 |

### Public Sources

- [Towards Leaving No Indic Language Behind](https://arxiv.org/abs/2212.05409), ACL 2023.
- [mteb/IndicQARetrieval](https://huggingface.co/datasets/mteb/IndicQARetrieval).
- [ai4bharat/IndicQA](https://huggingface.co/datasets/ai4bharat/IndicQA).

### Hugging Face Links

- Nano dataset: [hakari-bench/NanoIndicQA](https://huggingface.co/datasets/hakari-bench/NanoIndicQA)
- Source task dataset: [mteb/IndicQARetrieval](https://huggingface.co/datasets/mteb/IndicQARetrieval)

### Source Reference Table

| Title | Year | Type | URL |
| --- | ---: | --- | --- |
| Towards Leaving No Indic Language Behind | 2023 | paper | https://arxiv.org/abs/2212.05409 |
| mteb/IndicQARetrieval |  | dataset card | https://huggingface.co/datasets/mteb/IndicQARetrieval |
| ai4bharat/IndicQA |  | dataset card | https://huggingface.co/datasets/ai4bharat/IndicQA |

## Machine-Readable Metadata

<!-- benchmark-task-metadata:v1 -->

```yaml
benchmark_task_metadata:
  schema_version: 1
  document_status: first_pass
  nano_set: NanoIndicQA
  backing_dataset: NanoIndicQA
  dataset_id: hakari-bench/NanoIndicQA
  task_name: bn
  split_name: bn
  language: bn
  category: natural_language
  document_path: docs/benchmark_tasks/NanoIndicQA/bn.md
  source_research:
    primary_source_type: task_paper
    paper_pdf_or_html_checked: true
    no_paper_note: null
  counts:
    queries: 200
    documents: 250
    positive_qrels: 201
  positives_per_query:
    average: 1.005
    min: 1
    median: 1.0
    max: 2
    multi_positive_queries: 1
    multi_positive_query_percent: 0.5
  text_stats_chars:
    query_mean: 52.08
    document_mean: 2196.012
  bm25:
    ndcg_at_10: 0.6970903549209829
    hit_at_10: 0.815
    source: dataset_candidate_subset
  example_count: 5
  candidate_subsets:
    bm25:
      config: bm25
      label: BM25
      source: dataset_candidate_subset
      top_k: 500
      ndcg_at_10: 0.6970903549
      hit_at_10: 0.815
      recall_at_100: 0.8955223881
      candidate_count_min: 250
      candidate_count_max: 250
      candidate_count_mean: 250.0
      query_count: 200
      query_coverage: 1.0
      relevant_coverage_at_100: 0.8955223881
    dense:
      config: harrier_oss_v1_270m
      label: Dense
      source: dataset_candidate_subset
      top_k: 500
      ndcg_at_10: 0.7772637972
      hit_at_10: 0.87
      recall_at_100: 0.9900497512
      candidate_count_min: 250
      candidate_count_max: 250
      candidate_count_mean: 250.0
      query_count: 200
      query_coverage: 1.0
      relevant_coverage_at_100: 0.9900497512
    reranking_hybrid:
      config: reranking_hybrid
      label: Reranking hybrid
      source: dataset_candidate_subset
      top_k: 100
      ndcg_at_10: 0.7460182224
      hit_at_10: 0.835
      recall_at_100: 0.9701492537
      candidate_count_min: 100
      candidate_count_max: 101
      candidate_count_mean: 100.03
      query_count: 200
      query_coverage: 1.0
      relevant_coverage_at_100: 0.9701492537
      safeguard_positive_rows: 6
      rows_with_101_candidates: 6
```
