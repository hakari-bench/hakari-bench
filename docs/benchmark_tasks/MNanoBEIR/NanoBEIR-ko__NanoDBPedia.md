# MNanoBEIR / NanoBEIR-ko / NanoDBPedia

## Overview

DBpedia-Entity is an entity retrieval benchmark. `NanoBEIR-ko__NanoDBPedia`
uses Korean translated entity-style queries to retrieve Korean translated
DBpedia entity descriptions.

## Details

### What the Original Data Measures

[DBpedia-Entity V2](https://doi.org/10.1145/3077136.3080751) evaluates entity
search over DBpedia. [BEIR](https://arxiv.org/abs/2104.08663) includes it as an
entity retrieval task, and [MMTEB](https://arxiv.org/abs/2502.13595) provides
the multilingual benchmark context for this Korean split.

### Observed Data Profile

The sampled Korean Nano task has 50 queries, 6,045 documents, and 1,158
positive qrel rows. It is strongly multi-positive, averaging 23.16 positives per
query. Queries are short entity needs averaging 16.80 characters, while
documents are compact entity descriptions averaging 187.59 characters.

### BM25 Difficulty

Using the dataset-provided BM25 candidate column, BM25 reaches nDCG@10 =
0.5322 and hit@10 = 0.9400. Entity name overlap makes many records easy, but
category-style queries still need ranking among many plausible entities.

### Training Data That May Help

Useful training data includes non-overlapping entity search, Wikipedia/DBpedia
entity linking, multilingual entity retrieval, and short-query passage
retrieval data. Training should exclude DBpedia-Entity, BEIR, NanoBEIR, and
translated entity records likely to overlap.

### Synthetic Data Guidance

Generate Korean entity needs from non-evaluation entity descriptions. Include
both exact-name and category-style queries, with hard negatives from related
entities.

## Example Data

| Query | Positive document |
| --- | --- |
| 피츠제럴드 오토 몰 체임버스버그 펜실베이니아 (24 chars) | 피츠제럴드 오토몰은 1966년 메릴랜드주 베데스다에 첫 번째 지점을 오픈하며 설립된 가족 소유 및 운영 자동차 딜러십이다. 2014년 기준, 피츠제럴드 오토몰은 《오토모티브 뉴스》가 매년 발표하는 미국 '상위 125대 딜러십 그룹'에서 59위를 차지했다. 피츠제럴드 딜러 지점들은 2013년 워즈오토 이디일러 100에 8위, 25위, 30위, 43위, 98위로 다섯 차례 이름을 올렸다. (216 chars) |
| 1994년 단편 소설집 앨리스 먼로는 열려 있다 (26 chars) | 앨리스 앤 먼로(/ˈælɨs ˌæn mʌnˈroʊ/, 본명 레이드로 /ˈleɪdlɔː/; 1931년 7월 10일 출생)는 캐나다의 작가이다. 먼로의 작품은 시간의 전후를 오가며 단편소설의 구조를 혁신시켰다고 평가받는다. 그녀의 작품은 "드러내기보다 숨기며, 과시하기보다 더 많이 드러낸다"고 표현되기도 한다. 먼로의 소설은 대개 그녀의 고향인 온타리오주 남서부 휴런 카운티를 배경으로 한다. 그녀의 이야 ... [truncated 225 chars](251 chars) |
| 파리의 갈로-로마 건축 (12 chars) | 파리의 예술은 프랑스의 수도인 파리의 예술 문화와 역사에 관한 글이다. 수세기 동안 파리는 전 세계의 예술가들을 끌어들여, 이들이 도시에 도착해 예술 교육을 받고 예술 자원 및 갤러리에서 영감을 얻고자 했다. 그 결과, 파리는 '예술의 도시'라는 명성을 얻게 되었다. (149 chars) |
| 구 유고슬라비아의 공화국들 (14 chars) | 1974년 유고슬라비아 헌법은 사회주의 연방 공화국 유고슬라비아의 네 번째이자 마지막 헌법이다. 이 헌법은 2월 21일 발효되었다. 원문 406개 조항으로 구성된 1974년 헌법은 세계에서 가장 긴 헌법 중 하나였다. 이 헌법은 자치 관리 체제를 국가의 간섭으로부터 보호하고 공화국과 자치주들이 모든 선거 및 정책 논의 장에서 더 넓은 대표성을 갖도록 하기 위한 상세한 조문을 추가했다. (216 chars) |
| 베니스에서 촬영된 영화들 (13 chars) | 《작은 로맨스》는 조지 로이 힐이 감독을 맡고 로렌스 올리비에, 셀로니어스 버나드, 그리고 영화 데뷔를 한 다이안 레인이 출연한 1979년 미국 테크니컬러 및 파나비전 로맨틱 코미디 영화이다. 각본은 조지 로이 힐과 앨런 번스가 패트릭 코뱅의 소설 『E=mc² Mon Amour』를 바탕으로 집필하였으며, 원곡 음악은 조르주 들뤼가 작곡하였다. (192 chars) |

## Dataset Information

| Field | Value |
| --- | --- |
| Nano set | MNanoBEIR |
| Backing dataset | NanoBEIR-ko |
| Task / split | NanoDBPedia |
| Hugging Face dataset | [hakari-bench/NanoBEIR-ko](https://huggingface.co/datasets/hakari-bench/NanoBEIR-ko) |
| Language | ko |
| Category | natural_language |
| Queries | 50 |
| Documents | 6,045 |
| Positive qrels | 1,158 |
| Avg positives / query | 23.16 |
| Positives per query (min / median / max) | 1 / 18.00 / 81 |
| Queries with multiple positives | 48 (96.0%) |
| BM25 nDCG@10 | 0.5322 |
| BM25 hit@10 | 0.9400 |
| BM25 Recall@100 | 0.6520 |
| BM25 candidate subset | top-500 (`bm25`) |
| Dense nDCG@10 | 0.5928 |
| Dense hit@10 | 0.9600 |
| Dense Recall@100 | 0.6813 |
| Dense candidate subset | top-500 (`harrier_oss_v1_270m`) |
| Reranking hybrid nDCG@10 | 0.5787 |
| Reranking hybrid hit@10 | 0.9600 |
| Reranking hybrid Recall@100 | 0.6839 |
| Reranking hybrid candidate subset | top-100 plus optional rank-101 safeguard (`reranking_hybrid`) |
| Reranking hybrid candidates / query | 100 |
| Reranking hybrid safeguard rows | 0 |
| Query length avg chars | 16.80 |
| Document length avg chars | 187.59 |

### Public Sources

- [DBpedia-Entity V2](https://doi.org/10.1145/3077136.3080751).
- [BEIR: A Heterogeneous Benchmark for Zero-shot Evaluation of Information Retrieval Models](https://arxiv.org/abs/2104.08663).
- [MMTEB: Massive Multilingual Text Embedding Benchmark](https://arxiv.org/abs/2502.13595).
- [Zeta Alpha NanoBEIR collection](https://huggingface.co/collections/zeta-alpha-ai/nanobeir).

### Hugging Face Links

- Nano dataset: [hakari-bench/NanoBEIR-ko](https://huggingface.co/datasets/hakari-bench/NanoBEIR-ko)
- Source collection: [Zeta Alpha NanoBEIR collection](https://huggingface.co/collections/zeta-alpha-ai/nanobeir)

### Source Reference Table

| Title | Year | Type | URL |
| --- | ---: | --- | --- |
| DBpedia-Entity V2 | 2017 | task paper | https://doi.org/10.1145/3077136.3080751 |
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
  task_name: NanoDBPedia
  split_name: NanoDBPedia
  language: ko
  category: natural_language
  document_path: docs/benchmark_tasks/MNanoBEIR/NanoBEIR-ko__NanoDBPedia.md
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
    query_mean: 16.8
    document_mean: 187.589909
  bm25:
    ndcg_at_10: 0.5321686593585967
    hit_at_10: 0.94
    source: dataset_candidate_subset
  candidate_subsets:
    bm25:
      config: bm25
      label: BM25
      source: dataset_candidate_subset
      top_k: 500
      ndcg_at_10: 0.5321686594
      hit_at_10: 0.94
      recall_at_100: 0.6519861831
      candidate_count_min: 500
      candidate_count_max: 500
      candidate_count_mean: 500.0
      query_count: 50
      query_coverage: 1.0
      relevant_coverage_at_100: 0.6519861831
    dense:
      config: harrier_oss_v1_270m
      label: Dense
      source: dataset_candidate_subset
      top_k: 500
      ndcg_at_10: 0.5928200695
      hit_at_10: 0.96
      recall_at_100: 0.6813471503
      candidate_count_min: 500
      candidate_count_max: 500
      candidate_count_mean: 500.0
      query_count: 50
      query_coverage: 1.0
      relevant_coverage_at_100: 0.6813471503
    reranking_hybrid:
      config: reranking_hybrid
      label: Reranking hybrid
      source: dataset_candidate_subset
      top_k: 100
      ndcg_at_10: 0.5787206228
      hit_at_10: 0.96
      recall_at_100: 0.6839378238
      candidate_count_min: 100
      candidate_count_max: 100
      candidate_count_mean: 100.0
      query_count: 50
      query_coverage: 1.0
      relevant_coverage_at_100: 0.6839378238
      safeguard_positive_rows: 0
      rows_with_101_candidates: 0
```
