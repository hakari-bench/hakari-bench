# MNanoBEIR / NanoBEIR-sv / NanoQuoraRetrieval

## Overview

QuoraRetrieval is duplicate-question retrieval. `NanoBEIR-sv__NanoQuoraRetrieval`
uses Swedish translated questions to retrieve Swedish translated duplicate or
near-duplicate questions.

## Details

### What the Original Data Measures

The source is [Quora Question Pairs](https://kaggle.com/competitions/quora-question-pairs).
BEIR adapts it as retrieval, and MMTEB provides multilingual context.

### Observed Data Profile

The task has 50 queries, 5,046 documents, and 70 positive qrels. Ten queries
have multiple positives. Queries average 48.54 characters, and documents average
57.16 characters.

### BM25 Difficulty

BM25 reaches nDCG@10 = 0.6435 and hit@10 = 0.8000. The median first-positive
rank is 1.5, so lexical similarity is strong but paraphrase handling still
matters.

### Training Data That May Help

Use non-overlapping Swedish paraphrase retrieval and multilingual duplicate
question data. Exclude Quora, BEIR, NanoBEIR, and translated evaluation pairs.

### Synthetic Data Guidance

Generate Swedish paraphrase clusters with hard negatives that share entities or
wording but ask a different question.

## Example Data

| Query | Positive document |
| --- | --- |
| Är det okej att skratta åt sina egna skämt? (43 chars) | Är det konstigt att skratta åt sina egna skämt? (47 chars) |
| Vad är den bästa lögn du någonsin har berättat? (47 chars) | Vilken är den mest genomtänkta lögn du någonsin har berättat? (61 chars) |
| Varför föreslår Quora ofta svar i min flödesmatning som kritiserar Donald Trump? (80 chars) | Varför verkar Quora bara ha partiska och subjektiva svar på frågor om Donald Trump? (83 chars) |
| Hur kan jag bli starkare? (25 chars) | Hur blir jag starkare fysiskt? (30 chars) |
| Hur fungerar en kvantsatellit? (30 chars) | Hur fungerar en kvantumsatellit och vad skulle några av dess huvudanvändningar vara? (84 chars) |

## Dataset Information

| Field | Value |
| --- | --- |
| Nano set | MNanoBEIR |
| Backing dataset | NanoBEIR-sv |
| Task / split | NanoQuoraRetrieval |
| Hugging Face dataset | [hakari-bench/NanoBEIR-sv](https://huggingface.co/datasets/hakari-bench/NanoBEIR-sv) |
| Language | sv |
| Category | natural_language |
| Queries | 50 |
| Documents | 5,046 |
| Positive qrels | 70 |
| Positives per query avg | 1.40 |
| Positives per query min / median / max | 1 / 1.0 / 6 |
| Multi-positive queries | 10 (20.00%) |
| BM25 nDCG@10 | 0.6435 |
| BM25 hit@10 | 0.8000 |
| Query length avg chars | 48.54 |
| Document length avg chars | 57.16 |

### Public Sources

- [Quora Question Pairs](https://kaggle.com/competitions/quora-question-pairs), [BEIR](https://arxiv.org/abs/2104.08663), [MMTEB](https://arxiv.org/abs/2502.13595), and [NanoBEIR](https://huggingface.co/collections/zeta-alpha-ai/nanobeir).

### Hugging Face Links

- Nano dataset: [hakari-bench/NanoBEIR-sv](https://huggingface.co/datasets/hakari-bench/NanoBEIR-sv)
- Source collection: [Zeta Alpha NanoBEIR collection](https://huggingface.co/collections/zeta-alpha-ai/nanobeir)

### Source Reference Table

| Title | Year | Type | URL |
| --- | ---: | --- | --- |
| Quora Question Pairs | 2017 | dataset competition | https://kaggle.com/competitions/quora-question-pairs |
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
  backing_dataset: NanoBEIR-sv
  dataset_id: hakari-bench/NanoBEIR-sv
  task_name: NanoQuoraRetrieval
  split_name: NanoQuoraRetrieval
  language: sv
  category: natural_language
  document_path: docs/benchmark_tasks/MNanoBEIR/NanoBEIR-sv__NanoQuoraRetrieval.md
  source_research: {primary_source_type: benchmark_or_dataset_source, paper_pdf_or_html_checked: true, no_paper_note: No standalone task paper was confirmed; the dataset competition and BEIR benchmark paper are the public sources used here.}
  counts: {queries: 50, documents: 5046, positive_qrels: 70}
  positives_per_query: {average: 1.4, min: 1, median: 1.0, max: 6, multi_positive_queries: 10, multi_positive_query_percent: 20.0}
  text_stats_chars: {query_mean: 48.54, document_mean: 57.161118}
  bm25: {ndcg_at_10: 0.643504055, hit_at_10: 0.8, source: dataset_bm25_column}
```
