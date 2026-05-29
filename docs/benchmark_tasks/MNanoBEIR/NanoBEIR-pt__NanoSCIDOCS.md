# MNanoBEIR / NanoBEIR-pt / NanoSCIDOCS

## Overview

SCIDOCS is a scientific-document retrieval benchmark. `NanoBEIR-pt__NanoSCIDOCS`
uses Portuguese translated paper titles or descriptions to retrieve Portuguese
translated scientific abstracts.

## Details

### What the Original Data Measures

[SPECTER](https://arxiv.org/abs/2004.07180) introduced document embeddings
trained from scientific citation links and evaluated on SCIDOCS tasks. BEIR
includes SCIDOCS as scientific retrieval, and MMTEB provides the multilingual
benchmark context.

### Observed Data Profile

The sampled task has 50 queries, 2,210 documents, and 244 positive qrels. Every
query is multi-positive, usually with 3 to 5 positives. Queries average 83.02
characters, and documents average 1,028.76 characters.

### BM25 Difficulty

BM25 reaches nDCG@10 = 0.2911 and hit@10 = 0.8000. The median first-positive
rank is 2.0, so BM25 can often find a related paper, but ranking all relevant
scientific documents needs more than title-term overlap.

### Training Data That May Help

Helpful data includes non-overlapping scientific-paper retrieval, citation and
co-citation ranking, Portuguese scientific abstracts, and multilingual academic
search data. Exclude SCIDOCS, SPECTER evaluation records, BEIR, and NanoBEIR
overlaps.

### Synthetic Data Guidance

Generate Portuguese paper-title queries from scientific abstracts. Use positives
that share methods, problem statements, or citation context, and hard negatives
from the same field but different contribution.

## Example Data

| Query | Positive document |
| --- | --- |
| Conversor Elevador Multinível DC-DC Novo (40 chars) | Os conversores de fonte de tensão multinível estão surgindo como uma nova geração de opções de conversores de energia para aplicações de alta potência. Os conversores de fonte de tensão multinível geralmente sintetizam a onda ... [truncated 225 chars](1078 chars) |
| Aprendizado Rápido de Campos Aleatórios de Markov Esparsos Baseado em Fatorização de Cholesky (93 chars) | Sure, please provide the English document text that you need translated into Portuguese. (88 chars) |
| Síntese de Texturas Usando Redes Neurais Convolucionais (55 chars) | Neste trabalho, investigamos o efeito da profundidade de redes convolucionais na sua precisão em ambientes de reconhecimento de imagens em grande escala. Nossa principal contribuição é uma avaliação detalhada de redes de prof ... [truncated 225 chars](917 chars) |
| Antena anelar plana de banda larga com polarização circular para sistema RFID (77 chars) | Neste artigo, é proposta uma técnica de alimentação com faixa meandrante horizontal (HMS) para alcançar uma boa adaptação de impedância e padrões de radiação simétricos em banda larga para uma antena de patch empilhada circul ... [truncated 225 chars](1434 chars) |
| Projeto de monitor cardíaco digital avançado utilizando componentes eletrônicos básicos (87 chars) | Neste artigo, apresentamos o design e o desenvolvimento de um novo dispositivo integrado para medir a frequência cardíaca utilizando a ponta do dedo, visando melhorar a estimativa da frequência cardíaca. Com o aumento diário ... [truncated 225 chars](1291 chars) |

## Dataset Information

| Field | Value |
| --- | --- |
| Nano set | MNanoBEIR |
| Backing dataset | NanoBEIR-pt |
| Task / split | NanoSCIDOCS |
| Hugging Face dataset | [hakari-bench/NanoBEIR-pt](https://huggingface.co/datasets/hakari-bench/NanoBEIR-pt) |
| Language | pt |
| Category | natural_language |
| Queries | 50 |
| Documents | 2,210 |
| Positive qrels | 244 |
| Positives per query avg | 4.88 |
| Positives per query min / median / max | 3 / 5.0 / 5 |
| Multi-positive queries | 50 (100.00%) |
| BM25 nDCG@10 | 0.2911 |
| BM25 hit@10 | 0.8000 |
| BM25 Recall@100 | 0.5656 |
| BM25 candidate subset | top-500 (`bm25`) |
| Dense nDCG@10 | 0.3163 |
| Dense hit@10 | 0.8200 |
| Dense Recall@100 | 0.6393 |
| Dense candidate subset | top-500 (`harrier_oss_v1_270m`) |
| Reranking hybrid nDCG@10 | 0.3201 |
| Reranking hybrid hit@10 | 0.8200 |
| Reranking hybrid Recall@100 | 0.6311 |
| Reranking hybrid candidate subset | top-100 plus optional rank-101 safeguard (`reranking_hybrid`) |
| Reranking hybrid candidates / query | 100-101 |
| Reranking hybrid safeguard rows | 1 |
| Query length avg chars | 83.02 |
| Document length avg chars | 1,028.76 |

### Public Sources

- [SPECTER: Document-level Representation Learning using Citation-informed Transformers](https://arxiv.org/abs/2004.07180).
- [BEIR: A Heterogeneous Benchmark for Zero-shot Evaluation of Information Retrieval Models](https://arxiv.org/abs/2104.08663).
- [MMTEB: Massive Multilingual Text Embedding Benchmark](https://arxiv.org/abs/2502.13595).
- [Zeta Alpha NanoBEIR collection](https://huggingface.co/collections/zeta-alpha-ai/nanobeir).

### Hugging Face Links

- Nano dataset: [hakari-bench/NanoBEIR-pt](https://huggingface.co/datasets/hakari-bench/NanoBEIR-pt)
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
  backing_dataset: NanoBEIR-pt
  dataset_id: hakari-bench/NanoBEIR-pt
  task_name: NanoSCIDOCS
  split_name: NanoSCIDOCS
  language: pt
  category: natural_language
  document_path: docs/benchmark_tasks/MNanoBEIR/NanoBEIR-pt__NanoSCIDOCS.md
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
    query_mean: 83.02
    document_mean: 1028.756109
  bm25:
    ndcg_at_10: 0.29114339160160524
    hit_at_10: 0.8
    source: dataset_candidate_subset
  candidate_subsets:
    bm25:
      config: bm25
      label: BM25
      source: dataset_candidate_subset
      top_k: 500
      ndcg_at_10: 0.2911433916
      hit_at_10: 0.8
      recall_at_100: 0.5655737705
      candidate_count_min: 500
      candidate_count_max: 500
      candidate_count_mean: 500.0
      query_count: 50
      query_coverage: 1.0
      relevant_coverage_at_100: 0.5655737705
    dense:
      config: harrier_oss_v1_270m
      label: Dense
      source: dataset_candidate_subset
      top_k: 500
      ndcg_at_10: 0.3163181689
      hit_at_10: 0.82
      recall_at_100: 0.6393442623
      candidate_count_min: 500
      candidate_count_max: 500
      candidate_count_mean: 500.0
      query_count: 50
      query_coverage: 1.0
      relevant_coverage_at_100: 0.6393442623
    reranking_hybrid:
      config: reranking_hybrid
      label: Reranking hybrid
      source: dataset_candidate_subset
      top_k: 100
      ndcg_at_10: 0.3200807646
      hit_at_10: 0.82
      recall_at_100: 0.631147541
      candidate_count_min: 100
      candidate_count_max: 101
      candidate_count_mean: 100.02
      query_count: 50
      query_coverage: 1.0
      relevant_coverage_at_100: 0.631147541
      safeguard_positive_rows: 1
      rows_with_101_candidates: 1
```
