# NanoVNMTEB / cqadupstack_android_vn

## Overview

`cqadupstack_android_vn` is a Vietnamese duplicate-question retrieval task from NanoVNMTEB. The query is a short translated Android support question title, and the relevant documents are translated archived Android StackExchange questions marked as duplicates. Many queries have multiple positives, including one very large duplicate cluster. Dense retrieval has the strongest top-rank profile, while `reranking_hybrid` has the best recall@100. BM25 is useful for Android terms but weaker because duplicate questions often phrase the same device or workflow problem differently.

## Details

### What the Original Data Measures

CQADupStack was built for community question-answering duplicate retrieval. The task reflects a realistic setting: given a new question, retrieve earlier archived questions that ask the same thing.

VN-MTEB translates this Android split into Vietnamese. The task keeps the technical duplicate-detection structure while adding translation artifacts and Vietnamese phrasing around Android terminology.

### Observed Data Profile

The Nano split contains 200 queries, 10,000 documents, and 811 positive qrel rows. Queries average 55.64 characters, while documents average 604.76 characters. Positives per query average 4.06, with a minimum of 1, a median of 1, and a maximum of 100. There are 95 multi-positive queries, 47.5% of the split.

Example queries ask about Markdown notes synchronized with Dropbox, SMS database storage paths, streaming video from PC to Android, deleting preinstalled apps on HTC Desire, and a Galaxy S3 sound triggered by placing a card on the back.

### BM25 Evaluation Profile

The BM25 candidate subset uses top-500 candidates and reaches nDCG@10 of 0.3774, hit@10 of 0.6100, and recall@100 of 0.4747. BM25 benefits from technical terms such as adb, APK, ROM, SD card, Google Play, model names, and app names.

The limitation is duplicate paraphrase. Two duplicate questions can use different symptoms, device names, or workflow descriptions, while non-duplicates can share many Android keywords.

### Dense Evaluation Profile

The dense candidate subset from `harrier_oss_v1_270m` uses top-500 candidates and reaches nDCG@10 of 0.4991, hit@10 of 0.7550, and recall@100 of 0.5845. Dense retrieval is the strongest early-ranking profile.

This indicates that embedding similarity handles translated troubleshooting paraphrases better than term frequency. It can connect equivalent Android problems even when the exact title words differ.

### Reranking Hybrid Evaluation Profile

The `reranking_hybrid` subset uses top-100 candidates, with 14 rows receiving the optional rank-101 safeguard. It reaches nDCG@10 of 0.4629, hit@10 of 0.7050, and recall@100 of 0.5980. Hybrid retrieval has the best recall@100 but lower early ranking than dense retrieval.

The pattern is useful for reranking. Sparse matching widens the pool around device and app terms, while dense retrieval better orders the actual duplicate questions.

### Metric Interpretation for Model Researchers

Because many queries have multiple positives, nDCG@10 measures whether duplicate cluster members are ranked early, hit@10 measures whether at least one duplicate is found, and recall@100 measures cluster coverage for reranking.

For `cqadupstack_android_vn`, hit@10 alone can hide weak duplicate-cluster coverage, especially when a query has many positives.

### Query and Relevance Type Tendencies

Queries are short Vietnamese Android question titles. Relevant documents are longer translated community questions, often with title, body, duplicate markers, and technical details.

Relevance is duplicate-question equivalence. A thread with the same device or app is wrong if it asks a different operation or failure mode.

### Representative Failure Modes

Common failures include overmatching phone models, retrieving same-app but different-operation questions, missing paraphrased troubleshooting symptoms, and confusing duplicate clusters with broad topic clusters. BM25 overweights technical tokens; dense retrieval can blur similar Android workflows.

### Training Data That May Help

Useful training data includes non-overlapping Android duplicate-question pairs, Vietnamese mobile troubleshooting QA, translated CQADupStack training splits with overlap removed, and hard negatives sharing device, app, or feature terms. Evaluation questions, documents, qrels, and duplicate clusters should be excluded.

### Model Improvement Notes

Models should represent troubleshooting intent, device context, Android component, and operation type. Hard negatives should share exact model or feature names but ask different questions. Dense retrieval is the best direct ranker, while hybrid retrieval is useful for higher-recall reranking.

## Example Data

### Public Sources

- [CQADupStack: A Benchmark Data Set for Community Question-Answering Research](https://doi.org/10.1145/2838931.2838934), task paper.
- [VN-MTEB: Vietnamese Massive Text Embedding Benchmark](https://aclanthology.org/2026.findings-eacl.86/), VN-MTEB paper.
- [BEIR: A Heterogeneous Benchmark for Zero-shot Evaluation of Information Retrieval Models](https://arxiv.org/abs/2104.08663), benchmark paper.
- [GreenNode/cqadupstack-android-vn](https://huggingface.co/datasets/GreenNode/cqadupstack-android-vn), source dataset card.

### Source Reference Table

| Title | Year | Type | URL |
| --- | ---: | --- | --- |
| CQADupStack: A Benchmark Data Set for Community Question-Answering Research | 2015 | ACM paper | https://doi.org/10.1145/2838931.2838934 |
| VN-MTEB: Vietnamese Massive Text Embedding Benchmark | 2026 | ACL paper | https://aclanthology.org/2026.findings-eacl.86/ |
| BEIR: A Heterogeneous Benchmark for Zero-shot Evaluation of Information Retrieval Models | 2021 | arXiv paper | https://arxiv.org/abs/2104.08663 |
| GreenNode/cqadupstack-android-vn |  | dataset card | https://huggingface.co/datasets/GreenNode/cqadupstack-android-vn |

### Representative Snippets

| Query | Relevant document excerpt |
| --- | --- |
| Ghi chú Markdown với Dropbox đồng bộ | Thread about syncing markup notes through Dropbox on Android. |
| Tin nhắn SMS được lưu trữ ở đâu trên hệ thống file? | Thread asking for the Android SMS database path. |
| Dòng video từ PC đến Android? | Thread about streaming owned videos from a PC to Android. |
| Làm thế nào để xóa các ứng dụng được cài sẵn trên HTC Desire? | Thread about removing manufacturer-locked preinstalled apps. |
| Tại sao thiết bị S3 của tôi phát ra âm thanh khi đặt thẻ từ trên mặt sau? | Thread about a Galaxy S3 sound when the phone is placed down. |
