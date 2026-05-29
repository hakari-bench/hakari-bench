# MNanoBEIR / NanoBEIR-sv / NanoNFCorpus

## Overview

NFCorpus is biomedical and nutrition retrieval. `NanoBEIR-sv__NanoNFCorpus`
uses Swedish translated health queries to retrieve Swedish translated scientific
or medical passages.

## Details

### What the Original Data Measures

[NFCorpus](https://www.cl.uni-heidelberg.de/~riezler/publications/papers/ECIR2016.pdf)
uses health and nutrition information needs with relevance judgments. BEIR
includes it as domain-specific retrieval, and MMTEB provides multilingual
context.

### Observed Data Profile

The task has 50 queries, 2,953 documents, and 1,651 positive qrels. It is highly
multi-positive: average 33.02 positives, maximum 100. Queries average 23.16
characters, and documents average 1,493.97 characters.

### BM25 Difficulty

BM25 reaches nDCG@10 = 0.3058 and hit@10 = 0.6400. Biomedical terminology helps,
but broad positive sets and long abstracts still make ranking difficult.

### Training Data That May Help

Non-overlapping biomedical retrieval, Swedish medical QA, scientific abstract
retrieval, and multi-positive ranking can help. Exclude NFCorpus, BEIR, and
NanoBEIR overlaps.

### Synthetic Data Guidance

Generate Swedish biomedical keyword queries from scientific passages, preserving
multiple positives for shared condition, treatment, or outcome.

## Example Data

| Query | Positive document |
| --- | --- |
| Hälsosamma chokladmjölkshakes (29 chars) | Syfte: Att undersöka sambandet mellan intag av körsbär och risken för återkommande giktattacker hos individer med gikt. Metoder: Vi genomförde en fall-korsstudie för att undersöka sambandet mellan en uppsättning misstänkta ri ... [truncated 225 chars](1591 chars) |
| medicinsk etik (14 chars) | Bakgrund: En av de stora utmaningarna med att kontrollera serumkolesterol genom dietintervention verkar vara behovet av att förbättra patientens följsamhet. Syfte: Att utforska de många frågorna kring hinder och motiv för att ... [truncated 225 chars](1812 chars) |
| favabönor (9 chars) | De senaste 20 åren har intresset för L-arginins biokemi, näring och farmakologi ökat, vilket har lett till omfattande studier för att utforska dess näringsmässiga och terapeutiska roller i behandling och förebyggande av mänsk ... [truncated 225 chars](1220 chars) |
| Vad finns egentligen i kycklingbitar? (37 chars) | SYFTE: Att bestämma innehållet i kycklingbitar från 2 nationella matkedjor. BAKGRUND: Kycklingbitar har blivit en viktig del av den amerikanska kosten. Vi sökte att fastställa den nuvarande sammansättningen av denna högproces ... [truncated 225 chars](720 chars) |
| mättat fett (11 chars) | Intresset har ökat för möjligheten att moderns kostintag under graviditeten kan påverka utvecklingen av allergiska sjukdomar hos barn. Denna prospektiva studie undersökte sambandet mellan moderns intag av utvalda livsmedel me ... [truncated 225 chars](1954 chars) |

## Dataset Information

| Field | Value |
| --- | --- |
| Nano set | MNanoBEIR |
| Backing dataset | NanoBEIR-sv |
| Task / split | NanoNFCorpus |
| Hugging Face dataset | [hakari-bench/NanoBEIR-sv](https://huggingface.co/datasets/hakari-bench/NanoBEIR-sv) |
| Language | sv |
| Category | natural_language |
| Queries | 50 |
| Documents | 2,953 |
| Positive qrels | 1,651 |
| Positives per query avg | 33.02 |
| Positives per query min / median / max | 1 / 23.5 / 100 |
| Multi-positive queries | 47 (94.00%) |
| BM25 nDCG@10 | 0.2383 |
| BM25 hit@10 | 0.6000 |
| BM25 Recall@100 | 0.1224 |
| BM25 candidate subset | top-500 (`bm25`) |
| Dense nDCG@10 | 0.2315 |
| Dense hit@10 | 0.5600 |
| Dense Recall@100 | 0.1757 |
| Dense candidate subset | top-500 (`harrier_oss_v1_270m`) |
| Reranking hybrid nDCG@10 | 0.2519 |
| Reranking hybrid hit@10 | 0.5600 |
| Reranking hybrid Recall@100 | 0.1799 |
| Reranking hybrid candidate subset | top-100 plus optional rank-101 safeguard (`reranking_hybrid`) |
| Reranking hybrid candidates / query | 100-101 |
| Reranking hybrid safeguard rows | 9 |
| Query length avg chars | 23.16 |
| Document length avg chars | 1,493.97 |

### Public Sources

- [NFCorpus](https://www.cl.uni-heidelberg.de/~riezler/publications/papers/ECIR2016.pdf), [BEIR](https://arxiv.org/abs/2104.08663), [MMTEB](https://arxiv.org/abs/2502.13595), and [NanoBEIR](https://huggingface.co/collections/zeta-alpha-ai/nanobeir).

### Hugging Face Links

- Nano dataset: [hakari-bench/NanoBEIR-sv](https://huggingface.co/datasets/hakari-bench/NanoBEIR-sv)
- Source collection: [Zeta Alpha NanoBEIR collection](https://huggingface.co/collections/zeta-alpha-ai/nanobeir)

### Source Reference Table

| Title | Year | Type | URL |
| --- | ---: | --- | --- |
| NFCorpus: A Full-Text Learning to Rank Dataset for Medical Information Retrieval | 2016 | task paper | https://www.cl.uni-heidelberg.de/~riezler/publications/papers/ECIR2016.pdf |
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
  task_name: NanoNFCorpus
  split_name: NanoNFCorpus
  language: sv
  category: natural_language
  document_path: docs/benchmark_tasks/MNanoBEIR/NanoBEIR-sv__NanoNFCorpus.md
  source_research:
    primary_source_type: task_paper
    paper_pdf_or_html_checked: true
    no_paper_note: null
  counts:
    queries: 50
    documents: 2953
    positive_qrels: 1651
  positives_per_query:
    average: 33.02
    min: 1
    median: 23.5
    max: 100
    multi_positive_queries: 47
    multi_positive_query_percent: 94.0
  text_stats_chars:
    query_mean: 23.16
    document_mean: 1493.97257
  bm25:
    ndcg_at_10: 0.23833044376642504
    hit_at_10: 0.6
    source: dataset_candidate_subset
  candidate_subsets:
    bm25:
      config: bm25
      label: BM25
      source: dataset_candidate_subset
      top_k: 500
      ndcg_at_10: 0.2383304438
      hit_at_10: 0.6
      recall_at_100: 0.1223500909
      candidate_count_min: 500
      candidate_count_max: 500
      candidate_count_mean: 500.0
      query_count: 50
      query_coverage: 1.0
      relevant_coverage_at_100: 0.1223500909
    dense:
      config: harrier_oss_v1_270m
      label: Dense
      source: dataset_candidate_subset
      top_k: 500
      ndcg_at_10: 0.2315401822
      hit_at_10: 0.56
      recall_at_100: 0.1756511205
      candidate_count_min: 500
      candidate_count_max: 500
      candidate_count_mean: 500.0
      query_count: 50
      query_coverage: 1.0
      relevant_coverage_at_100: 0.1756511205
    reranking_hybrid:
      config: reranking_hybrid
      label: Reranking hybrid
      source: dataset_candidate_subset
      top_k: 100
      ndcg_at_10: 0.2518720494
      hit_at_10: 0.56
      recall_at_100: 0.1798909752
      candidate_count_min: 100
      candidate_count_max: 101
      candidate_count_mean: 100.18
      query_count: 50
      query_coverage: 1.0
      relevant_coverage_at_100: 0.1798909752
      safeguard_positive_rows: 9
      rows_with_101_candidates: 9
```
