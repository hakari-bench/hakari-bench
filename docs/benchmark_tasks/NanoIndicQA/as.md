# NanoIndicQA / as

## Overview

`NanoIndicQA / as` is the Assamese split of IndicQA retrieval. Assamese
cloze-style reading-comprehension questions retrieve the Assamese context
paragraph that supports the answer.

## Details

### What the Original Data Measures

[Towards Leaving No Indic Language Behind](https://arxiv.org/abs/2212.05409)
introduces IndicXTREME, a human-supervised benchmark for Indic languages, and
includes IndicQA as a manually curated cloze-style reading-comprehension task.
The MTEB retrieval version repurposes the QA task by using the question as the
query and the relevant context paragraph as the document.

This split measures Assamese context retrieval, not answer-string retrieval. A
model must find the paragraph that contains enough evidence for the question.

### Observed Data Profile

The Nano split has 200 queries, 250 documents, and 200 positive qrel rows. Every
query has one positive context. Queries average 55.30 characters and documents
average 1,401.28 characters. The samples show several questions pointing to the
same paragraph, so the task behaves like small-corpus passage selection.

### BM25 Difficulty

Using the dataset-provided BM25 candidate column, BM25 reaches nDCG@10 = 0.6111
and hit@10 = 0.7500. It ranks 96 positives at rank 1 and 150 in the top 10. All
positives appear within the top 100.

BM25 works when the question repeats distinctive Assamese terms from the context.
It fails when a short question uses broad wording or when many paragraphs share
cultural, historical, or named-entity vocabulary.

### Training Data That May Help

Useful training data includes non-overlapping Assamese QA context retrieval,
IndicQA-style cloze pairs, Assamese Wikipedia passage retrieval, and hard
negatives from paragraphs about related Indian cultural or historical topics.

### Synthetic Data Guidance

Generate Assamese questions from non-evaluation context paragraphs and keep the
full paragraph as the positive document. Include multiple questions per paragraph
and hard negatives with overlapping named entities. Avoid generating only short
answer labels; the task retrieves context.

## Example Data

| Query | Positive document |
| --- | --- |
| কেতিয়া কেইবাটাও হাতী আৰু দুটা গঁড় মানাহ ৰাষ্ট্ৰীয় উদ্যানলৈ প্ৰেৰণ কৰা হৈছিল? (78 chars) | [উদ্ধৃতিৰ প্ৰয়োজন] ১৯৬৮ চনত চৰকাৰে প্ৰণয়ন কৰে 'অসম ৰাষ্ট্ৰীয় উদ্যান আইন, ১৯৬৮ চন' (The Assam National Park Act of 1968) আৰু এই আইনৰ জৰিয়তে কাজিৰঙাক ৰাষ্ট্ৰীয় উদ্যানৰ ময্যদা দিয়া হয়। [উদ্ধৃতিৰ প্ৰয়োজন] ১৯৭৪ চনৰ ১১ ফেব্ ... [truncated 225 chars](1207 chars) |
| উগ্ৰস সৌতীয়ে কিমানটা শ্লোক আবৃত্তি কৰিছিল? (43 chars) | আগতেই কৈ অহা হৈছে যে পৰম্পৰাগতভাৱে ব্যাসক মহাভাৰতৰ লেখক বুলি কোৱা হয়। মহাভাৰতৰ প্ৰথম অনুচ্ছেদৰ মতে ব্যাসে গণেশক তেওঁৰ শ্ৰুতলিপি অনুসৰি শ্লোকসমূহ লিখিবলৈ অনুৰোধ কৰে। তেতিয়া গণেশে চৰ্ত্ত দিয়ে যে ব্যাসে আবৃত্তিৰ মাজত অকণো ৰ’ব ... [truncated 225 chars](2113 chars) |
| জাপি কিহেৰে নিৰ্মাণ কৰা হয়? (27 chars) | অসমীয়া সমাজ জীৱনত বিভিন্ন বিশ্বাস, অনুভৱ আৰু আদৰ বা সন্মানৰ ক্ষেত্ৰত তামোল-পান, গামোছা আৰু শৰাইৰ বিশেষ ভূমিকা আছে। যিকোনো সামাজিক কামত তামোল-পাণ ব্যৱহাৰ কৰা হয়। কাৰোবাৰ ঘৰলৈ অহা অতিথিক আন নহ'লেও তামোল-পাণ খাবলৈ দিয়া হয়। স ... [truncated 225 chars](938 chars) |
| মন খেমাৰে কি কি ভাষা কৈছিল? (27 chars) | অতি কমেও কেইবা শতিকাৰ পৰা এই দ্বীপ মালাত মানুহে বসবাস কৰি আহিছে। পুৰাতত্ববিদ সকলৰ মতে প্ৰায় ২,২০০ বছৰ মানৰ পৰা ইয়াত মানুহ থকাৰ প্ৰমাণ আছে, আনহাতেদি জিনীয় আৰু সাংস্কৃতিক অধ্যয়ণৰ পৰা দেখা গৈছে খিলঞ্জীয়া আন্দামানী সকল পৃথিৱ ... [truncated 225 chars](1224 chars) |
| আৰৱ সাগৰৰ সৰ্বাধিক প্ৰস্থ কিমান? (32 chars) | আৰৱ সাগৰৰ আয়তন ৩৮,৬২,০০০ বৰ্গ কিলোমিটাৰ। ইয়াৰ সৰ্বোচ্চ প্ৰস্থ প্ৰায় ২,৪০০ কিলোমিটাৰ আৰু ইয়াৰ সৰ্বনিম্ন গভীৰতা ৪,৬০০ মিটাৰ। সিন্ধু নদ আৰৱ সাগৰলৈ প্ৰবাহিত সৰ্ববৃহৎ নদী। আৰৱ সাগৰৰ দুটা গুৰুত্বপূৰ্ণ শাখা আছে। প্ৰথমটো হ’ল এডেন ... [truncated 225 chars](1063 chars) |

## Dataset Information

| Field | Value |
| --- | --- |
| Nano set | NanoIndicQA |
| Backing dataset | NanoIndicQA |
| Task / split | as |
| Hugging Face dataset | [hakari-bench/NanoIndicQA](https://huggingface.co/datasets/hakari-bench/NanoIndicQA) |
| Language | as |
| Category | natural_language |
| Queries | 200 |
| Documents | 250 |
| Positive qrels | 200 |
| BM25 nDCG@10 | 0.6111 |
| BM25 hit@10 | 0.7500 |
| Query length avg chars | 55.30 |
| Document length avg chars | 1,401.28 |

### Public Sources

- [Towards Leaving No Indic Language Behind: Building Monolingual Corpora, Benchmark and Models for Indic Languages](https://arxiv.org/abs/2212.05409), ACL 2023.
- [mteb/IndicQARetrieval](https://huggingface.co/datasets/mteb/IndicQARetrieval), MTEB dataset card.
- [ai4bharat/IndicQA](https://huggingface.co/datasets/ai4bharat/IndicQA), upstream dataset card.

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
  task_name: as
  split_name: as
  language: as
  category: natural_language
  document_path: docs/benchmark_tasks/NanoIndicQA/as.md
  source_research:
    primary_source_type: task_paper
    paper_pdf_or_html_checked: true
    no_paper_note: null
  counts:
    queries: 200
    documents: 250
    positive_qrels: 200
  positives_per_query:
    average: 1.0
    min: 1
    median: 1.0
    max: 1
    multi_positive_queries: 0
    multi_positive_query_percent: 0.0
  text_stats_chars:
    query_mean: 55.3
    document_mean: 1401.28
  bm25:
    ndcg_at_10: 0.6110883622
    hit_at_10: 0.75
    source: dataset_bm25_column
  example_count: 5
```
