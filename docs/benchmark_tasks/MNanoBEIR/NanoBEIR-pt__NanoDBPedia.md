# MNanoBEIR / NanoBEIR-pt / NanoDBPedia

## Overview

DBPedia Entity is an entity-oriented retrieval benchmark. `NanoBEIR-pt__NanoDBPedia`
uses Portuguese translated keyword and natural-language entity needs to retrieve
Portuguese translated DBpedia-style entity descriptions.

## Details

### What the Original Data Measures

[DBpedia-Entity](https://doi.org/10.1145/3077136.3080751) evaluates ranking
entities for information needs over DBpedia. BEIR includes it as a heterogeneous
entity retrieval task, and MMTEB supplies the multilingual framing for this
Portuguese translation.

### Observed Data Profile

The sampled task has 50 queries, 6,045 documents, and 1,158 positive qrels.
Almost every query is multi-positive, with an average of 23.16 positives and a
maximum of 81. Queries average 36.62 characters and documents average 354.37
characters.

### BM25 Difficulty

BM25 reaches nDCG@10 = 0.5094 and hit@10 = 0.9200. The median first-positive
rank is 1.0, showing that lexical entity cues are strong, but the many positives
make high-quality ordering more demanding than simple hit detection.

### Training Data That May Help

Useful supervision includes entity search, Portuguese Wikipedia or DBpedia
retrieval, alias matching, and multilingual entity description ranking. Exclude
DBPedia Entity, BEIR, NanoBEIR, and any translated duplicate evaluation records.

### Synthetic Data Guidance

Generate Portuguese entity needs that mix short keyword phrases with question
forms. Positive documents should be concise entity descriptions; hard negatives
should share entity types, places, occupations, or names.

## Example Data

| Query | Positive document |
| --- | --- |
| Fitzgerald Auto Mall em Chambersburg, PA (40 chars) | Fitzgerald Auto Malls é uma concessionária de automóveis de propriedade e operação familiar fundada em 1966, com sua primeira localização abrindo em Bethesda, Maryland. Em 2014, a Fitzgerald Auto Malls ficou em 59º lugar na l ... [truncated 225 chars](436 chars) |
| Coleção de contos de 1994 de Alice Munro está disponível (56 chars) | Alice Ann Munro (nascida Laidlaw; 10 de julho de 1931) é uma autora canadense. O trabalho de Munro é frequentemente descrito como tendo revolucionado a arquitetura dos contos, especialmente por sua tendência de avançar e retr ... [truncated 225 chars](528 chars) |
| Arquitetura galo-romana em Paris (32 chars) | A Arte em Paris é um artigo sobre a cultura e a história da arte em Paris, a capital da França. Há séculos, Paris atrai artistas de todo o mundo, que chegam à cidade para se educarem e buscar inspiração em seus recursos artís ... [truncated 225 chars](306 chars) |
| Repúblicas da antiga Iugoslávia (31 chars) | A Constituição de 1974 da Iugoslávia foi a quarta e última constituição da República Federal Socialista da Iugoslávia. Ela entrou em vigor em 21 de fevereiro. Com 406 artigos originais, a constituição de 1974 foi uma das mais ... [truncated 225 chars](440 chars) |
| Filmes filmados em Veneza (25 chars) | A Pequena Romântica é um filme de comédia romântica americano de 1979, em Technicolor e Panavision, dirigido por George Roy Hill e estrelado por Laurence Olivier, Thelonious Bernard e Diane Lane, em sua estreia no cinema. O r ... [truncated 225 chars](391 chars) |

## Dataset Information

| Field | Value |
| --- | --- |
| Nano set | MNanoBEIR |
| Backing dataset | NanoBEIR-pt |
| Task / split | NanoDBPedia |
| Hugging Face dataset | [hakari-bench/NanoBEIR-pt](https://huggingface.co/datasets/hakari-bench/NanoBEIR-pt) |
| Language | pt |
| Category | natural_language |
| Queries | 50 |
| Documents | 6,045 |
| Positive qrels | 1,158 |
| Positives per query avg | 23.16 |
| Positives per query min / median / max | 1 / 18.0 / 81 |
| Multi-positive queries | 48 (96.00%) |
| BM25 nDCG@10 | 0.5094 |
| BM25 hit@10 | 0.9200 |
| Query length avg chars | 36.62 |
| Document length avg chars | 354.37 |

### Public Sources

- [DBpedia Entity Retrieval](https://doi.org/10.1145/3077136.3080751).
- [BEIR: A Heterogeneous Benchmark for Zero-shot Evaluation of Information Retrieval Models](https://arxiv.org/abs/2104.08663).
- [MMTEB: Massive Multilingual Text Embedding Benchmark](https://arxiv.org/abs/2502.13595).
- [Zeta Alpha NanoBEIR collection](https://huggingface.co/collections/zeta-alpha-ai/nanobeir).

### Hugging Face Links

- Nano dataset: [hakari-bench/NanoBEIR-pt](https://huggingface.co/datasets/hakari-bench/NanoBEIR-pt)
- Source collection: [Zeta Alpha NanoBEIR collection](https://huggingface.co/collections/zeta-alpha-ai/nanobeir)

### Source Reference Table

| Title | Year | Type | URL |
| --- | ---: | --- | --- |
| DBpedia Entity Retrieval | 2017 | task paper | https://doi.org/10.1145/3077136.3080751 |
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
  task_name: NanoDBPedia
  split_name: NanoDBPedia
  language: pt
  category: natural_language
  document_path: docs/benchmark_tasks/MNanoBEIR/NanoBEIR-pt__NanoDBPedia.md
  source_research:
    primary_source_type: task_paper
    paper_pdf_or_html_checked: true
    no_paper_note: null
  counts:
    queries: 50
    documents: 6045
    positive_qrels: 1158
  positives_per_query:
    average: 23.16
    min: 1
    median: 18.0
    max: 81
    multi_positive_queries: 48
    multi_positive_query_percent: 96.0
  text_stats_chars:
    query_mean: 36.62
    document_mean: 354.3689
  bm25:
    ndcg_at_10: 0.5093920127
    hit_at_10: 0.92
    source: dataset_bm25_column
```
