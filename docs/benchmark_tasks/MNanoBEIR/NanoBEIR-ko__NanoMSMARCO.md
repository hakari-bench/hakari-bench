# MNanoBEIR / NanoBEIR-ko / NanoMSMARCO

## Overview

MS MARCO is a web passage retrieval benchmark. `NanoBEIR-ko__NanoMSMARCO` uses
Korean translated web-search questions to retrieve Korean translated
answer-bearing passages.

## Details

### What the Original Data Measures

[MS MARCO](https://arxiv.org/abs/1611.09268) introduced large-scale real user
queries with answer-bearing passages. BEIR includes it as a passage retrieval
task, and MMTEB provides the multilingual evaluation context for the Korean
translation.

### Observed Data Profile

The sampled task has 50 queries, 5,043 documents, and 50 positive qrels. Every
query has exactly one positive. Queries are short web questions averaging 19.12
characters; documents average 169.25 characters.

### BM25 Difficulty

BM25 reaches nDCG@10 = 0.3320 and hit@10 = 0.5400. The median first-positive
rank is 7, so lexical matching is often insufficient for Korean translated web
QA.

### Training Data That May Help

Useful data includes non-overlapping web QA retrieval, Korean search query logs,
multilingual passage retrieval, and answer-bearing passage pairs. Exclude MS
MARCO, BEIR, NanoBEIR, and overlapping translations.

### Synthetic Data Guidance

Generate concise Korean web queries from non-evaluation passages. The positive
passage should directly answer the query, while hard negatives should match
surface terms without answering it.

## Example Data

| Query | Positive document |
| --- | --- |
| 회상 증후군이란 무엇인가 (13 chars) | 회상 증후군. 회상 증후군은 메리시즘(Merycism)이라고도 하며, 음식물의 역류를 유발하는 특정되지 않은 유형의 섭식장애이다. 비록 DSM-IV에서 특정한 섭식장애로 명시되지는 않았지만, 이 장애를 진단하기 위한 특정 기준들이 제시되어 있다. (137 chars) |
| 'Here I Go Again'을 부른 사람은 누구인가요? (32 chars) | 다른 뜻에 대해서는 'Here I Go Again' (동음이의어)를 참조하십시오. "Here I Go Again"은 영국의 록 밴드 화이트스네이크(Whitesnake)의 노래이다. 이 곡은 원래 1982년 앨범 『Saints & Sinners』에 수록되었으며, 이후 1987년 발매된 동명의 앨범 『Whitesnake』를 위해 다시 녹음되었다. 같은 해에 이 곡은 새로운 라디오 믹스 버전으로 다시 한번 ... [truncated 225 chars](235 chars) |
| 캠런 보이스는 《리브 앤 매디》에서 루크 콘웨이 역을 맡았다. (34 chars) | 여러분, 진지한 웃음 준비하세요. 4월 19일 방영 예정인 'Liv & Maddie'의 에피소드 "Prom-A-Rooney"에 대한 독점 미리보기입니다. 당연히 그렇죠. 이 웃긴 클립에서 우리는 '제시'의 캐머런 보이스가 다른 디즈니 쇼로 건너와 매디(셸비 울퍼트)를 만나는 장면을 볼 수 있습니다. 그의 캐릭터는 다소 기묘하답니다! (186 chars) |
| 지구의 대부분의 큰 사막은 어디에 위치하는가 (24 chars) | 지구의 나머지 사막들은 극지방 외부에 위치해 있다. 그 중 가장 큰 것은 북아프리카에 있는 아열대 사막인 사하라 사막이다. (68 chars) |
| 경찰관에게 '코퍼(copper)'라는 말의 의미 (26 chars) | 현재의 연구 결과에 따르면, 'cop'보다 'copper'(경찰관, 원어 의미는 '체포하는 자')가 더 오래된 것으로 보인다. 'cop'는 말로 사용되어 체포를 의미하거나 명사로 경찰관을 의미할 수 있다. 뉴욕시 최초의 경감들이 착용한 구리 제질의 배지—런던의 '밥비(bobbies)'가 착용한 단추와는 달리—가 여기에 영향을 미쳤을 가능성이 있다. (195 chars) |

## Dataset Information

| Field | Value |
| --- | --- |
| Nano set | MNanoBEIR |
| Backing dataset | NanoBEIR-ko |
| Task / split | NanoMSMARCO |
| Hugging Face dataset | [hakari-bench/NanoBEIR-ko](https://huggingface.co/datasets/hakari-bench/NanoBEIR-ko) |
| Language | ko |
| Category | natural_language |
| Queries | 50 |
| Documents | 5,043 |
| Positive qrels | 50 |
| BM25 nDCG@10 | 0.3320 |
| BM25 hit@10 | 0.5400 |
| Query length avg chars | 19.12 |
| Document length avg chars | 169.25 |

### Public Sources

- [MS MARCO: A Human Generated Machine Reading Comprehension Dataset](https://arxiv.org/abs/1611.09268).
- [BEIR: A Heterogeneous Benchmark for Zero-shot Evaluation of Information Retrieval Models](https://arxiv.org/abs/2104.08663).
- [MMTEB: Massive Multilingual Text Embedding Benchmark](https://arxiv.org/abs/2502.13595).
- [Zeta Alpha NanoBEIR collection](https://huggingface.co/collections/zeta-alpha-ai/nanobeir).

### Hugging Face Links

- Nano dataset: [hakari-bench/NanoBEIR-ko](https://huggingface.co/datasets/hakari-bench/NanoBEIR-ko)
- Source collection: [Zeta Alpha NanoBEIR collection](https://huggingface.co/collections/zeta-alpha-ai/nanobeir)

### Source Reference Table

| Title | Year | Type | URL |
| --- | ---: | --- | --- |
| MS MARCO: A Human Generated Machine Reading Comprehension Dataset | 2016 | task paper | https://arxiv.org/abs/1611.09268 |
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
  backing_dataset: NanoBEIR-ko
  dataset_id: hakari-bench/NanoBEIR-ko
  task_name: NanoMSMARCO
  split_name: NanoMSMARCO
  language: ko
  category: natural_language
  document_path: docs/benchmark_tasks/MNanoBEIR/NanoBEIR-ko__NanoMSMARCO.md
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
    query_mean: 19.12
    document_mean: 169.245885
  bm25:
    ndcg_at_10: 0.3319666333
    hit_at_10: 0.54
    source: dataset_bm25_column
```
