# MNanoBEIR / NanoBEIR-sv / NanoSCIDOCS

## Overview

SCIDOCS is scientific-document retrieval. `NanoBEIR-sv__NanoSCIDOCS` uses
Swedish translated paper titles or descriptions to retrieve Swedish translated
scientific abstracts.

## Details

### What the Original Data Measures

[SPECTER](https://arxiv.org/abs/2004.07180) evaluates scientific document
representations over SCIDOCS. BEIR includes it as scientific retrieval, and
MMTEB provides multilingual context.

### Observed Data Profile

The task has 50 queries, 2,210 documents, and 244 positive qrels. Every query
has multiple positives, usually 3 to 5. Queries average 74.74 characters, and
documents average 941.30 characters.

### BM25 Difficulty

BM25 reaches nDCG@10 = 0.1892 and hit@10 = 0.6800. The median first-positive
rank is 5.0, so Swedish scientific title retrieval needs semantic paper-topic
matching.

### Training Data That May Help

Non-overlapping scientific retrieval, citation ranking, Swedish abstracts, and
multilingual academic search data may help. Exclude SCIDOCS, SPECTER
evaluation data, BEIR, and NanoBEIR.

### Synthetic Data Guidance

Generate Swedish paper-title queries from scientific abstracts; hard negatives
should come from the same field but different contribution.

## Example Data

| Query | Positive document |
| --- | --- |
| Ny DC-DC flernivåspänningshöjande omvandlare (44 chars) | Multinivåspänningsomvandlare är på väg att bli en ny typ av kraftomvandlare för högspänningsapplikationer. Multinivåspänningsomvandlare syntetiserar vanligtvis en trappformad spänningsvåg från flera nivåer av likspänningskond ... [truncated 225 chars](923 chars) |
| Snabb inlärning av glesa gaussiska Markovfält baserat på Cholesky-faktorisering (79 chars) | Sure, please provide the English document text that you need translated into Swedish. (85 chars) |
| Textursyntes med konvolutiva neurala nätverk (44 chars) | I detta arbete undersöker vi effekten av djupet i ett konvolutivt nätverk på dess noggrannhet i en stor skala bildigenkänningsinställning. Vår huvudsakliga bidrag är en grundlig utvärdering av nätverk med ökande djup, vilket ... [truncated 225 chars](830 chars) |
| Planär bredbandsringantenn med cirkulär polarisering för RFID-system (68 chars) | I denna artikel föreslås en teknik med horisontellt meanderande strimma (HMS) för att uppnå god impedansanpassning och symmetriska bredsidorstrålningsmönster för en enkelmatad bredbandscirkulärt polariserad staplad patchanten ... [truncated 225 chars](1261 chars) |
| Design av en avancerad digital hjärtmonitor med grundläggande elektroniska komponenter (86 chars) | I denna artikel presenterar vi designen och utvecklingen av en ny integrerad enhet för att mäta hjärtfrekvens med hjälp av fingertoppen för att förbättra uppskattningen av hjärtfrekvensen. Eftersom hjärtrelaterade sjukdomar ö ... [truncated 225 chars](1099 chars) |

## Dataset Information

| Field | Value |
| --- | --- |
| Nano set | MNanoBEIR |
| Backing dataset | NanoBEIR-sv |
| Task / split | NanoSCIDOCS |
| Hugging Face dataset | [hakari-bench/NanoBEIR-sv](https://huggingface.co/datasets/hakari-bench/NanoBEIR-sv) |
| Language | sv |
| Category | natural_language |
| Queries | 50 |
| Documents | 2,210 |
| Positive qrels | 244 |
| Positives per query avg | 4.88 |
| Positives per query min / median / max | 3 / 5.0 / 5 |
| Multi-positive queries | 50 (100.00%) |
| BM25 nDCG@10 | 0.1892 |
| BM25 hit@10 | 0.6800 |
| BM25 Recall@100 | 0.4221 |
| BM25 candidate subset | top-500 (`bm25`) |
| Dense nDCG@10 | 0.3472 |
| Dense hit@10 | 0.8200 |
| Dense Recall@100 | 0.6557 |
| Dense candidate subset | top-500 (`harrier_oss_v1_270m`) |
| Reranking hybrid nDCG@10 | 0.2844 |
| Reranking hybrid hit@10 | 0.8000 |
| Reranking hybrid Recall@100 | 0.6393 |
| Reranking hybrid candidate subset | top-100 plus optional rank-101 safeguard (`reranking_hybrid`) |
| Reranking hybrid candidates / query | 100-101 |
| Reranking hybrid safeguard rows | 1 |
| Query length avg chars | 74.74 |
| Document length avg chars | 941.30 |

### Public Sources

- [SPECTER](https://arxiv.org/abs/2004.07180), [BEIR](https://arxiv.org/abs/2104.08663), [MMTEB](https://arxiv.org/abs/2502.13595), and [NanoBEIR](https://huggingface.co/collections/zeta-alpha-ai/nanobeir).

### Hugging Face Links

- Nano dataset: [hakari-bench/NanoBEIR-sv](https://huggingface.co/datasets/hakari-bench/NanoBEIR-sv)
- Source collection: [Zeta Alpha NanoBEIR collection](https://huggingface.co/collections/zeta-alpha-ai/nanobeir)

### Source Reference Table

| Title | Year | Type | URL |
| --- | ---: | --- | --- |
| SPECTER: Document-level Representation Learning using Citation-informed Transformers | 2020 | task paper | https://arxiv.org/abs/2004.07180 |
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
  task_name: NanoSCIDOCS
  split_name: NanoSCIDOCS
  language: sv
  category: natural_language
  document_path: docs/benchmark_tasks/MNanoBEIR/NanoBEIR-sv__NanoSCIDOCS.md
  source_research:
    primary_source_type: task_paper
    paper_pdf_or_html_checked: true
    no_paper_note: null
  counts:
    queries: 50
    documents: 2210
    positive_qrels: 244
  positives_per_query:
    average: 4.88
    min: 3
    median: 5.0
    max: 5
    multi_positive_queries: 50
    multi_positive_query_percent: 100.0
  text_stats_chars:
    query_mean: 74.74
    document_mean: 941.304525
  bm25:
    ndcg_at_10: 0.18924048759322207
    hit_at_10: 0.68
    source: dataset_candidate_subset
  candidate_subsets:
    bm25:
      config: bm25
      label: BM25
      source: dataset_candidate_subset
      top_k: 500
      ndcg_at_10: 0.1892404876
      hit_at_10: 0.68
      recall_at_100: 0.4221311475
      candidate_count_min: 500
      candidate_count_max: 500
      candidate_count_mean: 500.0
      query_count: 50
      query_coverage: 1.0
      relevant_coverage_at_100: 0.4221311475
    dense:
      config: harrier_oss_v1_270m
      label: Dense
      source: dataset_candidate_subset
      top_k: 500
      ndcg_at_10: 0.347195206
      hit_at_10: 0.82
      recall_at_100: 0.6557377049
      candidate_count_min: 500
      candidate_count_max: 500
      candidate_count_mean: 500.0
      query_count: 50
      query_coverage: 1.0
      relevant_coverage_at_100: 0.6557377049
    reranking_hybrid:
      config: reranking_hybrid
      label: Reranking hybrid
      source: dataset_candidate_subset
      top_k: 100
      ndcg_at_10: 0.284426928
      hit_at_10: 0.8
      recall_at_100: 0.6393442623
      candidate_count_min: 100
      candidate_count_max: 101
      candidate_count_mean: 100.02
      query_count: 50
      query_coverage: 1.0
      relevant_coverage_at_100: 0.6393442623
      safeguard_positive_rows: 1
      rows_with_101_candidates: 1
```
