# MNanoBEIR / NanoBEIR-sr / NanoNQ

## Overview

Natural Questions is an answer-oriented Wikipedia retrieval benchmark.
`NanoBEIR-sr__NanoNQ` uses Serbian translated search questions to retrieve
Serbian translated answer passages.

## Details

### What the Original Data Measures

[Natural Questions](https://aclanthology.org/Q19-1026/) introduced naturally
occurring search questions paired with Wikipedia evidence. BEIR evaluates the
retrieval step, and MMTEB supplies the multilingual framing.

### Observed Data Profile

The sampled task has 50 queries, 5,035 documents, and 57 positive qrels. Most
queries have one positive, with 7 multi-positive queries. Queries average 45.60
characters, and documents average 514.47 characters.

### BM25 Difficulty

BM25 reaches nDCG@10 = 0.2624 and hit@10 = 0.4800. The median first-positive
rank is 12.5, so many questions require semantic answer matching rather than
only lexical overlap.

### Training Data That May Help

Helpful data includes non-overlapping open-domain QA retrieval, Serbian
Wikipedia passage search, and multilingual query-passage pairs. Exclude Natural
Questions, BEIR, NanoBEIR, and translated evaluation examples.

### Synthetic Data Guidance

Generate Serbian natural questions from encyclopedia passages. Positive
documents should contain answer-bearing context; hard negatives should share
entities without answering the question.

## Example Data

| Query | Positive document |
| --- | --- |
| Gde se održava Final Four ove godine? (37 chars) | NCAA Divizija I muški košarkaški turnir 2018. bio je turnir sa 68 timova po sistemu direktnog ispadanja, održan kako bi se odredio nacionalni šampion u muškoj koledž košarci NCAA Divizije I za sezonu 2017–18. Osamdeseto izdan ... [truncated 225 chars](353 chars) |
| Da li je "Noćna mora pre Božića" originalno bio Diznijev film? (62 chars) | "Pakao pre Božića" nastao je iz pesme koju je Tim Burton napisao 1982. godine, dok je radio kao animator u studiju Walt Disney Feature Animation. Uz uspeh filma "Vinsent" iste godine, studijo Walt Disney počeo je da razmatra ... [truncated 225 chars](616 chars) |
| Zašto je anđeo severa tu? (25 chars) | Prema Gormliju, značaj anđela je bio trostruk: prvo, da označi da su ispod mesta njegove izgradnje rudari uglja radili dva veka; drugo, da obuhvati prelazak iz industrijskog u informaciono doba, i treće, da posluži kao fokus ... [truncated 225 chars](264 chars) |
| Gde je kompromis 3/5 prvobitno naveden u ustavu? (48 chars) | Kompromis o tri petine nalazi se u Članu 1, Odeljku 2, Stav 3 Ustava Sjedinjenih Država, koji glasi: (100 chars) |
| Ko peva pesmu "Somebody's Watching Me" sa Majklom Džeksonom? (60 chars) | "Somebody's Watching Me" je pesma američkog pevača Rokvela sa njegovog debitantskog studijskog albuma Somebody's Watching Me (1984). Objavljena je kao Rokvelov debitanski singl i vodeći singl sa albuma 14. januara 1984. godin ... [truncated 225 chars](358 chars) |

## Dataset Information

| Field | Value |
| --- | --- |
| Nano set | MNanoBEIR |
| Backing dataset | NanoBEIR-sr |
| Task / split | NanoNQ |
| Hugging Face dataset | [hakari-bench/NanoBEIR-sr](https://huggingface.co/datasets/hakari-bench/NanoBEIR-sr) |
| Language | sr |
| Category | natural_language |
| Queries | 50 |
| Documents | 5,035 |
| Positive qrels | 57 |
| Positives per query avg | 1.14 |
| Positives per query min / median / max | 1 / 1.0 / 2 |
| Multi-positive queries | 7 (14.00%) |
| BM25 nDCG@10 | 0.2624 |
| BM25 hit@10 | 0.4800 |
| BM25 Recall@100 | 0.7368 |
| BM25 candidate subset | top-500 (`bm25`) |
| Dense nDCG@10 | 0.5343 |
| Dense hit@10 | 0.7200 |
| Dense Recall@100 | 0.8772 |
| Dense candidate subset | top-500 (`harrier_oss_v1_270m`) |
| Reranking hybrid nDCG@10 | 0.4228 |
| Reranking hybrid hit@10 | 0.6800 |
| Reranking hybrid Recall@100 | 0.9123 |
| Reranking hybrid candidate subset | top-100 plus optional rank-101 safeguard (`reranking_hybrid`) |
| Reranking hybrid candidates / query | 100-101 |
| Reranking hybrid safeguard rows | 3 |
| Query length avg chars | 45.60 |
| Document length avg chars | 514.47 |

### Public Sources

- [Natural Questions](https://aclanthology.org/Q19-1026/), [BEIR](https://arxiv.org/abs/2104.08663), [MMTEB](https://arxiv.org/abs/2502.13595), and [NanoBEIR](https://huggingface.co/collections/zeta-alpha-ai/nanobeir).

### Hugging Face Links

- Nano dataset: [hakari-bench/NanoBEIR-sr](https://huggingface.co/datasets/hakari-bench/NanoBEIR-sr)
- Source collection: [Zeta Alpha NanoBEIR collection](https://huggingface.co/collections/zeta-alpha-ai/nanobeir)

### Source Reference Table

| Title | Year | Type | URL |
| --- | ---: | --- | --- |
| Natural Questions: a Benchmark for Question Answering Research | 2019 | task paper | https://aclanthology.org/Q19-1026/ |
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
  backing_dataset: NanoBEIR-sr
  dataset_id: hakari-bench/NanoBEIR-sr
  task_name: NanoNQ
  split_name: NanoNQ
  language: sr
  category: natural_language
  document_path: docs/benchmark_tasks/MNanoBEIR/NanoBEIR-sr__NanoNQ.md
  source_research:
    primary_source_type: task_paper
    paper_pdf_or_html_checked: true
    no_paper_note: null
  counts:
    queries: 50
    documents: 5035
    positive_qrels: 57
  positives_per_query:
    average: 1.14
    min: 1
    median: 1.0
    max: 2
    multi_positive_queries: 7
    multi_positive_query_percent: 14.0
  text_stats_chars:
    query_mean: 45.6
    document_mean: 514.465541
  bm25:
    ndcg_at_10: 0.26236862756949814
    hit_at_10: 0.48
    source: dataset_candidate_subset
  candidate_subsets:
    bm25:
      config: bm25
      label: BM25
      source: dataset_candidate_subset
      top_k: 500
      ndcg_at_10: 0.2623686276
      hit_at_10: 0.48
      recall_at_100: 0.7368421053
      candidate_count_min: 500
      candidate_count_max: 500
      candidate_count_mean: 500.0
      query_count: 50
      query_coverage: 1.0
      relevant_coverage_at_100: 0.7368421053
    dense:
      config: harrier_oss_v1_270m
      label: Dense
      source: dataset_candidate_subset
      top_k: 500
      ndcg_at_10: 0.5342635576
      hit_at_10: 0.72
      recall_at_100: 0.8771929825
      candidate_count_min: 500
      candidate_count_max: 500
      candidate_count_mean: 500.0
      query_count: 50
      query_coverage: 1.0
      relevant_coverage_at_100: 0.8771929825
    reranking_hybrid:
      config: reranking_hybrid
      label: Reranking hybrid
      source: dataset_candidate_subset
      top_k: 100
      ndcg_at_10: 0.4227698386
      hit_at_10: 0.68
      recall_at_100: 0.9122807018
      candidate_count_min: 100
      candidate_count_max: 101
      candidate_count_mean: 100.06
      query_count: 50
      query_coverage: 1.0
      relevant_coverage_at_100: 0.9122807018
      safeguard_positive_rows: 3
      rows_with_101_candidates: 3
```
