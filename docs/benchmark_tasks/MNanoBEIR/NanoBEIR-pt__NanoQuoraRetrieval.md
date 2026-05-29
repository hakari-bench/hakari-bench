# MNanoBEIR / NanoBEIR-pt / NanoQuoraRetrieval

## Overview

QuoraRetrieval is a duplicate-question retrieval task. `NanoBEIR-pt__NanoQuoraRetrieval`
uses Portuguese translated questions to retrieve Portuguese translated duplicate
or near-duplicate questions.

## Details

### What the Original Data Measures

The source is the [Quora Question Pairs](https://kaggle.com/competitions/quora-question-pairs)
duplicate-question dataset. BEIR adapts it as a retrieval task in which a query
question should retrieve semantically equivalent questions, and MMTEB provides
the multilingual context.

### Observed Data Profile

The sampled task has 50 queries, 5,046 documents, and 70 positive qrels. Most
queries have one positive, though 10 queries have multiple duplicates. Queries
average 54.20 characters, and documents are very short at 62.53 characters on
average.

### BM25 Difficulty

BM25 reaches nDCG@10 = 0.7227 and hit@10 = 0.9000. The median first-positive
rank is 1.0, reflecting strong lexical overlap between many duplicate questions,
but paraphrases still require semantic matching.

### Training Data That May Help

Useful data includes non-overlapping duplicate-question retrieval, Portuguese
paraphrase data, and multilingual semantic question matching. Exclude Quora
Question Pairs, BEIR, NanoBEIR, and translated duplicate records from this split.

### Synthetic Data Guidance

Generate Portuguese paraphrase clusters for the same intent. Include hard
negatives that share entities or wording but ask a different question.

## Example Data

| Query | Positive document |
| --- | --- |
| É normal rir das próprias piadas? (33 chars) | É estranho rir das minhas próprias piadas? (42 chars) |
| Qual é a maior mentira que você já contou? (42 chars) | Qual é a maior mentira que você já contou? (42 chars) |
| Por que o Quora frequentemente sugere respostas no meu feed que criticam Donald Trump? (86 chars) | Por que o Quora parece ter apenas respostas tendenciosas e subjetivas sobre perguntas relacionadas a Donald Trump? (114 chars) |
| Como posso ficar mais forte fisicamente? (40 chars) | Como posso ficar mais forte fisicamente? (40 chars) |
| Como funciona um satélite quântico? (35 chars) | Como funciona um satélite quântico e quais seriam suas principais aplicações? (77 chars) |

## Dataset Information

| Field | Value |
| --- | --- |
| Nano set | MNanoBEIR |
| Backing dataset | NanoBEIR-pt |
| Task / split | NanoQuoraRetrieval |
| Hugging Face dataset | [hakari-bench/NanoBEIR-pt](https://huggingface.co/datasets/hakari-bench/NanoBEIR-pt) |
| Language | pt |
| Category | natural_language |
| Queries | 50 |
| Documents | 5,046 |
| Positive qrels | 70 |
| Positives per query avg | 1.40 |
| Positives per query min / median / max | 1 / 1.0 / 6 |
| Multi-positive queries | 10 (20.00%) |
| BM25 nDCG@10 | 0.7247 |
| BM25 hit@10 | 0.9000 |
| BM25 Recall@100 | 0.9571 |
| BM25 candidate subset | top-500 (`bm25`) |
| Dense nDCG@10 | 0.8172 |
| Dense hit@10 | 0.9000 |
| Dense Recall@100 | 0.9286 |
| Dense candidate subset | top-500 (`harrier_oss_v1_270m`) |
| Reranking hybrid nDCG@10 | 0.7634 |
| Reranking hybrid hit@10 | 0.8800 |
| Reranking hybrid Recall@100 | 0.9857 |
| Reranking hybrid candidate subset | top-100 plus optional rank-101 safeguard (`reranking_hybrid`) |
| Reranking hybrid candidates / query | 100-101 |
| Reranking hybrid safeguard rows | 1 |
| Query length avg chars | 54.20 |
| Document length avg chars | 62.53 |

### Public Sources

- [Quora Question Pairs](https://kaggle.com/competitions/quora-question-pairs).
- [BEIR: A Heterogeneous Benchmark for Zero-shot Evaluation of Information Retrieval Models](https://arxiv.org/abs/2104.08663).
- [MMTEB: Massive Multilingual Text Embedding Benchmark](https://arxiv.org/abs/2502.13595).
- [Zeta Alpha NanoBEIR collection](https://huggingface.co/collections/zeta-alpha-ai/nanobeir).

### Hugging Face Links

- Nano dataset: [hakari-bench/NanoBEIR-pt](https://huggingface.co/datasets/hakari-bench/NanoBEIR-pt)
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
  backing_dataset: NanoBEIR-pt
  dataset_id: hakari-bench/NanoBEIR-pt
  task_name: NanoQuoraRetrieval
  split_name: NanoQuoraRetrieval
  language: pt
  category: natural_language
  document_path: docs/benchmark_tasks/MNanoBEIR/NanoBEIR-pt__NanoQuoraRetrieval.md
  source_research:
    primary_source_type: benchmark_or_dataset_source
    paper_pdf_or_html_checked: true
    no_paper_note: No standalone task paper was confirmed; the dataset competition
      and BEIR benchmark paper are the public sources used here.
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
    query_mean: 54.2
    document_mean: 62.533492
  bm25:
    ndcg_at_10: 0.7247257156448448
    hit_at_10: 0.9
    source: dataset_candidate_subset
  candidate_subsets:
    bm25:
      config: bm25
      label: BM25
      source: dataset_candidate_subset
      top_k: 500
      ndcg_at_10: 0.7247257156
      hit_at_10: 0.9
      recall_at_100: 0.9571428571
      candidate_count_min: 500
      candidate_count_max: 500
      candidate_count_mean: 500.0
      query_count: 50
      query_coverage: 1.0
      relevant_coverage_at_100: 0.9571428571
    dense:
      config: harrier_oss_v1_270m
      label: Dense
      source: dataset_candidate_subset
      top_k: 500
      ndcg_at_10: 0.8172471215
      hit_at_10: 0.9
      recall_at_100: 0.9285714286
      candidate_count_min: 500
      candidate_count_max: 500
      candidate_count_mean: 500.0
      query_count: 50
      query_coverage: 1.0
      relevant_coverage_at_100: 0.9285714286
    reranking_hybrid:
      config: reranking_hybrid
      label: Reranking hybrid
      source: dataset_candidate_subset
      top_k: 100
      ndcg_at_10: 0.7634191233
      hit_at_10: 0.88
      recall_at_100: 0.9857142857
      candidate_count_min: 100
      candidate_count_max: 101
      candidate_count_mean: 100.02
      query_count: 50
      query_coverage: 1.0
      relevant_coverage_at_100: 0.9857142857
      safeguard_positive_rows: 1
      rows_with_101_candidates: 1
```
