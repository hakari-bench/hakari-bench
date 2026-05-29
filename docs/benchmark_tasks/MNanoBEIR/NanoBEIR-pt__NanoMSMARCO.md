# MNanoBEIR / NanoBEIR-pt / NanoMSMARCO

## Overview

MS MARCO is a web passage retrieval benchmark. `NanoBEIR-pt__NanoMSMARCO` uses
Portuguese translated web-search questions to retrieve Portuguese translated
answer-bearing passages.

## Details

### What the Original Data Measures

[MS MARCO](https://arxiv.org/abs/1611.09268) introduced large-scale real user
queries with answer-bearing passages. BEIR includes it as a passage retrieval
task, and MMTEB gives the multilingual context for the Portuguese translation.

### Observed Data Profile

The sampled task has 50 queries, 5,043 documents, and 50 positive qrels. Every
query has exactly one positive. Queries are short web questions averaging 40.22
characters; documents average 344.65 characters.

### BM25 Difficulty

BM25 reaches nDCG@10 = 0.3494 and hit@10 = 0.5200. The median first-positive
rank is 7.0, so lexical matching sometimes succeeds, but many Portuguese
translated web questions require answer-aware semantic matching.

### Training Data That May Help

Useful data includes non-overlapping web QA retrieval, Portuguese search query
logs, multilingual passage retrieval, and answer-bearing passage pairs. Exclude
MS MARCO, BEIR, NanoBEIR, and overlapping translations.

### Synthetic Data Guidance

Generate concise Portuguese web queries from non-evaluation passages. The
positive passage should directly answer the query, while hard negatives should
match surface terms without answering it.

## Example Data

| Query | Positive document |
| --- | --- |
| O que é a síndrome da ruminação? (32 chars) | Síndrome de Ruminação. A síndrome de ruminação, também conhecida como mericismo, é um tipo de transtorno alimentar não especificado de outra forma que causa a regurgitação de alimentos. Embora não seja identificada como um tr ... [truncated 225 chars](335 chars) |
| Quem cantou "Aqui vou eu de novo"? (34 chars) | Para outros usos, veja Here I Go Again (desambiguação). "Here I Go Again" é uma música da banda britânica de rock Whitesnake. Originalmente lançada no álbum de 1982, Saints & Sinners, a canção foi regravada para o álbum homôn ... [truncated 225 chars](323 chars) |
| Quem Cameron Boyce interpreta em Liv e Maddie? (46 chars) | Prepare-se para muitas risadas, pessoal. Em uma prévia exclusiva do episódio de 19 de abril de "Liv & Maddie" chamado "Prom-A-Rooney." Obviamente. No clipe hilariante, vemos o astro de "Jessie," Cameron Boyce, aparecer em out ... [truncated 225 chars](324 chars) |
| Onde a maioria dos grandes desertos da Terra ocorre? (52 chars) | Os outros desertos da Terra estão fora das regiões polares. O maior é o Deserto do Saara, um deserto subtropical no norte da África. (132 chars) |
| Qual é o significado de "tira" para um policial? (48 chars) | De acordo com os achados atuais, parece que 'copper' (um policial, literalmente 'aquele que prende') precede 'cop' (usado verbalmente para significar prender ou como substantivo para policial). Pode ser que as insignias de co ... [truncated 225 chars](370 chars) |

## Dataset Information

| Field | Value |
| --- | --- |
| Nano set | MNanoBEIR |
| Backing dataset | NanoBEIR-pt |
| Task / split | NanoMSMARCO |
| Hugging Face dataset | [hakari-bench/NanoBEIR-pt](https://huggingface.co/datasets/hakari-bench/NanoBEIR-pt) |
| Language | pt |
| Category | natural_language |
| Queries | 50 |
| Documents | 5,043 |
| Positive qrels | 50 |
| BM25 nDCG@10 | 0.3494 |
| BM25 hit@10 | 0.5200 |
| BM25 Recall@100 | 0.7600 |
| BM25 candidate subset | top-500 (`bm25`) |
| Dense nDCG@10 | 0.5121 |
| Dense hit@10 | 0.7000 |
| Dense Recall@100 | 0.9600 |
| Dense candidate subset | top-500 (`harrier_oss_v1_270m`) |
| Reranking hybrid nDCG@10 | 0.4873 |
| Reranking hybrid hit@10 | 0.6800 |
| Reranking hybrid Recall@100 | 0.9800 |
| Reranking hybrid candidate subset | top-100 plus optional rank-101 safeguard (`reranking_hybrid`) |
| Reranking hybrid candidates / query | 100-101 |
| Reranking hybrid safeguard rows | 1 |
| Query length avg chars | 40.22 |
| Document length avg chars | 344.65 |

### Public Sources

- [MS MARCO: A Human Generated MAchine Reading COmprehension Dataset](https://arxiv.org/abs/1611.09268).
- [BEIR: A Heterogeneous Benchmark for Zero-shot Evaluation of Information Retrieval Models](https://arxiv.org/abs/2104.08663).
- [MMTEB: Massive Multilingual Text Embedding Benchmark](https://arxiv.org/abs/2502.13595).
- [Zeta Alpha NanoBEIR collection](https://huggingface.co/collections/zeta-alpha-ai/nanobeir).

### Hugging Face Links

- Nano dataset: [hakari-bench/NanoBEIR-pt](https://huggingface.co/datasets/hakari-bench/NanoBEIR-pt)
- Source collection: [Zeta Alpha NanoBEIR collection](https://huggingface.co/collections/zeta-alpha-ai/nanobeir)

### Source Reference Table

| Title | Year | Type | URL |
| --- | ---: | --- | --- |
| MS MARCO: A Human Generated MAchine Reading COmprehension Dataset | 2016 | task paper | https://arxiv.org/abs/1611.09268 |
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
  task_name: NanoMSMARCO
  split_name: NanoMSMARCO
  language: pt
  category: natural_language
  document_path: docs/benchmark_tasks/MNanoBEIR/NanoBEIR-pt__NanoMSMARCO.md
  source_research:
    primary_source_type: task_paper
    paper_pdf_or_html_checked: true
    no_paper_note: null
  counts:
    queries: 50
    documents: 5043
    positive_qrels: 50
  positives_per_query:
    average: 1.0
    min: 1
    median: 1.0
    max: 1
    multi_positive_queries: 0
    multi_positive_query_percent: 0.0
  text_stats_chars:
    query_mean: 40.22
    document_mean: 344.650407
  bm25:
    ndcg_at_10: 0.349428899857823
    hit_at_10: 0.52
    source: dataset_candidate_subset
  candidate_subsets:
    bm25:
      config: bm25
      label: BM25
      source: dataset_candidate_subset
      top_k: 500
      ndcg_at_10: 0.3494288999
      hit_at_10: 0.52
      recall_at_100: 0.76
      candidate_count_min: 500
      candidate_count_max: 500
      candidate_count_mean: 500.0
      query_count: 50
      query_coverage: 1.0
      relevant_coverage_at_100: 0.76
    dense:
      config: harrier_oss_v1_270m
      label: Dense
      source: dataset_candidate_subset
      top_k: 500
      ndcg_at_10: 0.5120861036
      hit_at_10: 0.7
      recall_at_100: 0.96
      candidate_count_min: 500
      candidate_count_max: 500
      candidate_count_mean: 500.0
      query_count: 50
      query_coverage: 1.0
      relevant_coverage_at_100: 0.96
    reranking_hybrid:
      config: reranking_hybrid
      label: Reranking hybrid
      source: dataset_candidate_subset
      top_k: 100
      ndcg_at_10: 0.4873292762
      hit_at_10: 0.68
      recall_at_100: 0.98
      candidate_count_min: 100
      candidate_count_max: 101
      candidate_count_mean: 100.02
      query_count: 50
      query_coverage: 1.0
      relevant_coverage_at_100: 0.98
      safeguard_positive_rows: 1
      rows_with_101_candidates: 1
```
