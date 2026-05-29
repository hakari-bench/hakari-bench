# MNanoBEIR / NanoBEIR-sv / NanoFEVER

## Overview

FEVER is a Wikipedia evidence retrieval task for factual claims.
`NanoBEIR-sv__NanoFEVER` uses Swedish translated claims and evidence passages.

## Details

### What the Original Data Measures

[FEVER](https://arxiv.org/abs/1803.05355) was built for fact extraction and
verification over Wikipedia. BEIR evaluates the retrieval step, and MMTEB gives
the multilingual context for this Swedish split.

### Observed Data Profile

The task has 50 queries, 4,996 documents, and 57 positive qrels. Most queries
have one positive; 6 queries have multiple positives. Queries average 44.64
characters, and documents average 1,166.66 characters.

### BM25 Difficulty

BM25 reaches nDCG@10 = 0.7512 and hit@10 = 0.9200, with median first-positive
rank 1.0. Named entities and claim wording give BM25 strong anchors.

### Training Data That May Help

Non-overlapping Swedish claim-evidence retrieval, Wikipedia evidence mining, and
multilingual fact-checking may help. Exclude FEVER, BEIR, NanoBEIR, and direct
translations of evaluation records.

### Synthetic Data Guidance

Generate Swedish factual claims from encyclopedia passages, with related-entity
hard negatives that do not provide the needed evidence.

## Example Data

| Query | Positive document |
| --- | --- |
| Keith Godchaux kände till Grateful Dead (39 chars) | The Grateful Dead var ett amerikanskt rockband som bildades 1965 i Palo Alto, Kalifornien. Bandet, som bestod av fem till sju medlemmar, är känt för sin unika och eklektiska stil, som blandade element från rock, psychedelia, ... [truncated 225 chars](2895 chars) |
| Taarak Mehta Ka Ooltah Chashmah är en sitcom. (45 chars) | Taarak Mehta Ka Ooltah Chashmah (Engelska: Taarak Mehtas olika perspektiv) är Indiens längsta löpande sitcom, producerad av Neela Tele Films Private Limited. Serien sändes för första gången den 28 juli 2008. Den sänds från må ... [truncated 225 chars](583 chars) |
| Hemliga och tekniskt avancerade flygplan tillverkades i Burbank, Kalifornien. (77 chars) | Burbank är en stad i Los Angeles County i södra Kalifornien, USA, cirka 19 kilometer nordväst om centrala Los Angeles. Vid folkräkningen 2010 hade staden 103 340 invånare. Staden marknadsförs som "Världens Mediehuvudstad" och ... [truncated 225 chars](1280 chars) |
| Nero är en människa (19 chars) | Den julisk-claudiska dynastin syftar på de första fem romerska kejsarna – Augustus, Tiberius, Caligula, Claudius och Nero – eller familjen de tillhörde. De styrde Romarriket från dess bildande under Augustus i slutet av 1:a å ... [truncated 225 chars](2022 chars) |
| Scream 2 är enbart en tysk film. (32 chars) | Scream 2 är en amerikansk slasherfilm från 1997, regisserad av Wes Craven och skriven av Kevin Williamson. Filmen har David Arquette, Neve Campbell, Courteney Cox, Sarah Michelle Gellar, Jamie Kennedy, Laurie Metcalf, Jerry O ... [truncated 225 chars](2456 chars) |

## Dataset Information

| Field | Value |
| --- | --- |
| Nano set | MNanoBEIR |
| Backing dataset | NanoBEIR-sv |
| Task / split | NanoFEVER |
| Hugging Face dataset | [hakari-bench/NanoBEIR-sv](https://huggingface.co/datasets/hakari-bench/NanoBEIR-sv) |
| Language | sv |
| Category | natural_language |
| Queries | 50 |
| Documents | 4,996 |
| Positive qrels | 57 |
| Positives per query avg | 1.14 |
| Positives per query min / median / max | 1 / 1.0 / 3 |
| Multi-positive queries | 6 (12.00%) |
| BM25 nDCG@10 | 0.7512 |
| BM25 hit@10 | 0.9200 |
| BM25 Recall@100 | 0.9649 |
| BM25 candidate subset | top-500 (`bm25`) |
| Dense nDCG@10 | 0.8570 |
| Dense hit@10 | 0.9400 |
| Dense Recall@100 | 0.9298 |
| Dense candidate subset | top-500 (`harrier_oss_v1_270m`) |
| Reranking hybrid nDCG@10 | 0.8153 |
| Reranking hybrid hit@10 | 0.9800 |
| Reranking hybrid Recall@100 | 1.0000 |
| Reranking hybrid candidate subset | top-100 plus optional rank-101 safeguard (`reranking_hybrid`) |
| Reranking hybrid candidates / query | 100 |
| Reranking hybrid safeguard rows | 0 |
| Query length avg chars | 44.64 |
| Document length avg chars | 1,166.66 |

### Public Sources

- [FEVER](https://arxiv.org/abs/1803.05355), [BEIR](https://arxiv.org/abs/2104.08663), [MMTEB](https://arxiv.org/abs/2502.13595), and [NanoBEIR](https://huggingface.co/collections/zeta-alpha-ai/nanobeir).

### Hugging Face Links

- Nano dataset: [hakari-bench/NanoBEIR-sv](https://huggingface.co/datasets/hakari-bench/NanoBEIR-sv)
- Source collection: [Zeta Alpha NanoBEIR collection](https://huggingface.co/collections/zeta-alpha-ai/nanobeir)

### Source Reference Table

| Title | Year | Type | URL |
| --- | ---: | --- | --- |
| FEVER: a Large-scale Dataset for Fact Extraction and VERification | 2018 | task paper | https://arxiv.org/abs/1803.05355 |
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
  task_name: NanoFEVER
  split_name: NanoFEVER
  language: sv
  category: natural_language
  document_path: docs/benchmark_tasks/MNanoBEIR/NanoBEIR-sv__NanoFEVER.md
  source_research:
    primary_source_type: task_paper
    paper_pdf_or_html_checked: true
    no_paper_note: null
  counts:
    queries: 50
    documents: 4996
    positive_qrels: 57
  positives_per_query:
    average: 1.14
    min: 1
    median: 1.0
    max: 3
    multi_positive_queries: 6
    multi_positive_query_percent: 12.0
  text_stats_chars:
    query_mean: 44.64
    document_mean: 1166.655124
  bm25:
    ndcg_at_10: 0.7512063741232996
    hit_at_10: 0.92
    source: dataset_candidate_subset
  candidate_subsets:
    bm25:
      config: bm25
      label: BM25
      source: dataset_candidate_subset
      top_k: 500
      ndcg_at_10: 0.7512063741
      hit_at_10: 0.92
      recall_at_100: 0.9649122807
      candidate_count_min: 500
      candidate_count_max: 500
      candidate_count_mean: 500.0
      query_count: 50
      query_coverage: 1.0
      relevant_coverage_at_100: 0.9649122807
    dense:
      config: harrier_oss_v1_270m
      label: Dense
      source: dataset_candidate_subset
      top_k: 500
      ndcg_at_10: 0.856987869
      hit_at_10: 0.94
      recall_at_100: 0.9298245614
      candidate_count_min: 500
      candidate_count_max: 500
      candidate_count_mean: 500.0
      query_count: 50
      query_coverage: 1.0
      relevant_coverage_at_100: 0.9298245614
    reranking_hybrid:
      config: reranking_hybrid
      label: Reranking hybrid
      source: dataset_candidate_subset
      top_k: 100
      ndcg_at_10: 0.8152859558
      hit_at_10: 0.98
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
