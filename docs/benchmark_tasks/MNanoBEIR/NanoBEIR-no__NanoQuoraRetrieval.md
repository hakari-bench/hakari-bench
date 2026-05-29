# MNanoBEIR / NanoBEIR-no / NanoQuoraRetrieval

## Overview

Quora retrieval is a duplicate-question retrieval task.
`NanoBEIR-no__NanoQuoraRetrieval` uses Norwegian translated questions to
retrieve Norwegian translated semantically equivalent questions.

## Details

### What the Original Data Measures

The Quora Question Pairs dataset is a duplicate-question benchmark, and
[BEIR](https://arxiv.org/abs/2104.08663) adapts it as duplicate-question
retrieval. [MMTEB](https://arxiv.org/abs/2502.13595) provides the multilingual
context for this Norwegian split.

### Observed Data Profile

The sampled task has 50 queries, 5,046 documents, and 70 positive qrels. Most
queries have one positive, but 10 queries have multiple positives. Queries and
documents are both short questions, averaging 50.62 and 57.87 characters.

### BM25 Difficulty

BM25 reaches nDCG@10 = 0.6342 and hit@10 = 0.7800. Lexical overlap is often
strong, but robust models should match paraphrases and near-duplicate intent.

### Training Data That May Help

Useful data includes non-overlapping duplicate-question pairs, paraphrase
retrieval, Norwegian question matching, and multilingual semantic similarity
data. Training should exclude Quora Question Pairs, BEIR, NanoBEIR, and
overlapping translations.

### Synthetic Data Guidance

Generate Norwegian paraphrase pairs from non-evaluation questions. Hard
negatives should share topic words but ask for different information.

## Example Data

| Query | Positive document |
| --- | --- |
| Er det greit å le av egne vitser? (33 chars) | Er det rart å le av mine egne vitser? (37 chars) |
| Hva er den mest geniale løgn du noen gang har fortalt? (54 chars) | Hva er den mest gjennomtenkte løgnen du noen gang har fortalt? (62 chars) |
| Hvorfor fremmer Quora ofte svar i min feed som kritiserer Donald Trump? (71 chars) | Hvorfor virker det som om Quora bare har subjektive og partiske svar på spørsmål om Donald Trump? (97 chars) |
| Hvordan kan jeg bli sterkere fysisk? (36 chars) | Hvordan blir jeg fysisk sterk? (30 chars) |
| Hvordan fungerer en kvantum-satellitt? (38 chars) | Hvordan fungerer en Quantum-satellitt, og hva er noen av dens hovedbruk? (72 chars) |

## Dataset Information

| Field | Value |
| --- | --- |
| Nano set | MNanoBEIR |
| Backing dataset | NanoBEIR-no |
| Task / split | NanoQuoraRetrieval |
| Hugging Face dataset | [hakari-bench/NanoBEIR-no](https://huggingface.co/datasets/hakari-bench/NanoBEIR-no) |
| Language | no |
| Category | natural_language |
| Queries | 50 |
| Documents | 5,046 |
| Positive qrels | 70 |
| Avg positives / query | 1.40 |
| Positives per query (min / median / max) | 1 / 1.00 / 6 |
| Queries with multiple positives | 10 (20.0%) |
| BM25 nDCG@10 | 0.6347 |
| BM25 hit@10 | 0.7800 |
| BM25 Recall@100 | 0.8857 |
| BM25 candidate subset | top-500 (`bm25`) |
| Dense nDCG@10 | 0.7829 |
| Dense hit@10 | 0.8800 |
| Dense Recall@100 | 0.9714 |
| Dense candidate subset | top-500 (`harrier_oss_v1_270m`) |
| Reranking hybrid nDCG@10 | 0.6988 |
| Reranking hybrid hit@10 | 0.8200 |
| Reranking hybrid Recall@100 | 1.0000 |
| Reranking hybrid candidate subset | top-100 plus optional rank-101 safeguard (`reranking_hybrid`) |
| Reranking hybrid candidates / query | 100 |
| Reranking hybrid safeguard rows | 0 |
| Query length avg chars | 50.62 |
| Document length avg chars | 57.87 |

### Public Sources

- [Quora Question Pairs](https://kaggle.com/competitions/quora-question-pairs).
- [BEIR: A Heterogeneous Benchmark for Zero-shot Evaluation of Information Retrieval Models](https://arxiv.org/abs/2104.08663).
- [MMTEB: Massive Multilingual Text Embedding Benchmark](https://arxiv.org/abs/2502.13595).
- [Zeta Alpha NanoBEIR collection](https://huggingface.co/collections/zeta-alpha-ai/nanobeir).

### Hugging Face Links

- Nano dataset: [hakari-bench/NanoBEIR-no](https://huggingface.co/datasets/hakari-bench/NanoBEIR-no)
- Source collection: [Zeta Alpha NanoBEIR collection](https://huggingface.co/collections/zeta-alpha-ai/nanobeir)

### Source Reference Table

| Title | Year | Type | URL |
| --- | ---: | --- | --- |
| Quora Question Pairs | 2017 | dataset page | https://kaggle.com/competitions/quora-question-pairs |
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
  backing_dataset: NanoBEIR-no
  dataset_id: hakari-bench/NanoBEIR-no
  task_name: NanoQuoraRetrieval
  split_name: NanoQuoraRetrieval
  language: 'no'
  category: natural_language
  document_path: docs/benchmark_tasks/MNanoBEIR/NanoBEIR-no__NanoQuoraRetrieval.md
  source_research:
    primary_source_type: benchmark_paper
    paper_pdf_or_html_checked: true
    no_paper_note: no standalone task paper was confirmed for the BEIR retrieval adaptation
  counts:
    queries: 50
    documents: 5046
    positive_qrels: 70
  positives_per_query:
    average: 1.4
    min: 1
    median: 1.0
    max: 6
    multi_positive_queries: 10
    multi_positive_query_percent: 20.0
  text_stats_chars:
    query_mean: 50.62
    document_mean: 57.871581
  bm25:
    ndcg_at_10: 0.6346849892075749
    hit_at_10: 0.78
    source: dataset_candidate_subset
  candidate_subsets:
    bm25:
      config: bm25
      label: BM25
      source: dataset_candidate_subset
      top_k: 500
      ndcg_at_10: 0.6346849892
      hit_at_10: 0.78
      recall_at_100: 0.8857142857
      candidate_count_min: 500
      candidate_count_max: 500
      candidate_count_mean: 500.0
      query_count: 50
      query_coverage: 1.0
      relevant_coverage_at_100: 0.8857142857
    dense:
      config: harrier_oss_v1_270m
      label: Dense
      source: dataset_candidate_subset
      top_k: 500
      ndcg_at_10: 0.7829249606
      hit_at_10: 0.88
      recall_at_100: 0.9714285714
      candidate_count_min: 500
      candidate_count_max: 500
      candidate_count_mean: 500.0
      query_count: 50
      query_coverage: 1.0
      relevant_coverage_at_100: 0.9714285714
    reranking_hybrid:
      config: reranking_hybrid
      label: Reranking hybrid
      source: dataset_candidate_subset
      top_k: 100
      ndcg_at_10: 0.6988210523
      hit_at_10: 0.82
      recall_at_100: 1.0
      candidate_count_min: 100
      candidate_count_max: 100
      candidate_count_mean: 100.0
      query_count: 50
      query_coverage: 1.0
      relevant_coverage_at_100: 1.0
      safeguard_positive_rows: 0
      rows_with_101_candidates: 0
```
