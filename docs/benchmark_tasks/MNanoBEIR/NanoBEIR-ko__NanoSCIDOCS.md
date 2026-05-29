# MNanoBEIR / NanoBEIR-ko / NanoSCIDOCS

## Overview

SCIDOCS is a scientific-document retrieval benchmark. `NanoBEIR-ko__NanoSCIDOCS`
uses Korean translated paper titles or scientific queries to retrieve Korean
translated paper abstracts or document descriptions.

## Details

### What the Original Data Measures

[SPECTER](https://arxiv.org/abs/2004.07180) introduced scientific document
representations and the SCIDOCS evaluation suite. BEIR includes SCIDOCS as a
scientific retrieval task, and MMTEB provides multilingual context.

### Observed Data Profile

The sampled task has 50 queries, 2,210 documents, and 244 positive qrels. Every
query has multiple positives, usually five. Queries average 32.10 characters,
and documents average 452.83 characters.

### BM25 Difficulty

BM25 reaches nDCG@10 = 0.2688 and hit@10 = 0.7400. Scientific vocabulary helps
lexical matching, but cross-paper relatedness often requires semantic and
disciplinary context.

### Training Data That May Help

Useful data includes non-overlapping citation recommendation, related-paper
retrieval, scientific abstract retrieval, and Korean or multilingual scholarly
text pairs. Training should exclude SCIDOCS, SPECTER evaluation data, BEIR, and
NanoBEIR.

### Synthetic Data Guidance

Generate Korean paper-title or abstract queries from non-evaluation scholarly
abstracts. Hard negatives should be in the same research area but not the same
method, dataset, or claim.

## Example Data

| Query | Positive document |
| --- | --- |
| 신형 DC-DC 다단계 부스트 컨버터 (20 chars) | 초록다단계 전압원 변환기는 고출력 응용 분야를 위한 새로운 유형의 전력 변환기 옵션으로 등장하고 있다. 다단계 전압원 변환기는 일반적으로 여러 단계의 직류 콘덴서 전압을 이용하여 계단형 전압 파형을 생성한다. 다단계 변환기의 주요 제한 사항 중 하나는 서로 다른 단계들 사이의 전압 불균형이다. 서로 다른 단계들 사이의 전압을 균형 잡기 위한 기술은 일반적으로 전압 클램핑 또는 콘덴서 충전 제어를 포함 ... [truncated 225 chars](443 chars) |
| 촐레스키 분해를 기반으로 한 빠른 희소 가우시안 마르코프 임의장 학습 (38 chars) |  (0 chars) |
| 합성곱 신경망을 이용한 텍스처 생성 (19 chars) | 본 연구에서는 대규모 이미지 인식 환경에서 합성곱 네트워크의 깊이가 정확도에 미치는 영향을 조사한다. 우리의 주요 기여는 깊이를 점차 증가시킨 네트워크에 대한 철저한 평가로, 기존 최고 수준의 구성 대비 16~19개의 가중치 층까지 깊이를 확장함으로써 상당한 성능 향상을 달성할 수 있음을 보여준다. 이러한 발견은 우리 팀이 ImageNet Challenge 2014에 참가한 기반이 되었으며, 이 대회 ... [truncated 225 chars](418 chars) |
| RFID 시스템을 위한 원형 편파를 가진 평면 광대역 고리형 링 안테나 (39 chars) | 본 논문에서는 범용 초고주파(UHF) 무선 주파수 인식(RFID) 응용에 적합한 단일 공급 대역폭 넓은 원형 편파 적층 패치 안테나에서 임피던스 정합을 개선하고 대칭적인 정방향 복사 패턴을 얻기 위해 수평으로 미로형(Mezzane) 스트립(HMS) 공급 기법을 제안한다. 안테나는 두 개의 모서리 절단된 패치와 HMS로 구성되며, 모두 FR4 기판의 상부면에 인쇄된다. HMS의 한쪽 끝은 프로브를 통해 ... [truncated 225 chars](633 chars) |
| 기본 전자 부품을 사용한 고급 디지털 심박수 모니터 설계 (31 chars) | 본 논문에서는 심박수 추정의 정확도를 향상시키기 위해 손가락 끝을 이용한 심박수 측정을 위한 새로운 통합 장치의 설계 및 개발을 제시하였다. 심장 관련 질병이 날로 증가함에 따라 건강 관리의 질을 보장하기 위해 정확하고 저렴한 심박수 측정 장치 또는 심장 모니터의 필요성이 절실하다. 그러나 대부분의 심박수 측정 도구와 환경은 비용이 비싸고 인간공학적 설계를 따르지 않는다. 제안된 심박수 측정(HRM) ... [truncated 225 chars](508 chars) |

## Dataset Information

| Field | Value |
| --- | --- |
| Nano set | MNanoBEIR |
| Backing dataset | NanoBEIR-ko |
| Task / split | NanoSCIDOCS |
| Hugging Face dataset | [hakari-bench/NanoBEIR-ko](https://huggingface.co/datasets/hakari-bench/NanoBEIR-ko) |
| Language | ko |
| Category | natural_language |
| Queries | 50 |
| Documents | 2,210 |
| Positive qrels | 244 |
| Avg positives / query | 4.88 |
| Positives per query (min / median / max) | 3 / 5.00 / 5 |
| Queries with multiple positives | 50 (100.0%) |
| BM25 nDCG@10 | 0.2673 |
| BM25 hit@10 | 0.7400 |
| BM25 Recall@100 | 0.6066 |
| BM25 candidate subset | top-500 (`bm25`) |
| Dense nDCG@10 | 0.3310 |
| Dense hit@10 | 0.8600 |
| Dense Recall@100 | 0.6434 |
| Dense candidate subset | top-500 (`harrier_oss_v1_270m`) |
| Reranking hybrid nDCG@10 | 0.3380 |
| Reranking hybrid hit@10 | 0.8800 |
| Reranking hybrid Recall@100 | 0.6434 |
| Reranking hybrid candidate subset | top-100 plus optional rank-101 safeguard (`reranking_hybrid`) |
| Reranking hybrid candidates / query | 100-101 |
| Reranking hybrid safeguard rows | 1 |
| Query length avg chars | 32.10 |
| Document length avg chars | 452.83 |

### Public Sources

- [SPECTER: Document-level Representation Learning using Citation-informed Transformers](https://arxiv.org/abs/2004.07180).
- [BEIR: A Heterogeneous Benchmark for Zero-shot Evaluation of Information Retrieval Models](https://arxiv.org/abs/2104.08663).
- [MMTEB: Massive Multilingual Text Embedding Benchmark](https://arxiv.org/abs/2502.13595).
- [Zeta Alpha NanoBEIR collection](https://huggingface.co/collections/zeta-alpha-ai/nanobeir).

### Hugging Face Links

- Nano dataset: [hakari-bench/NanoBEIR-ko](https://huggingface.co/datasets/hakari-bench/NanoBEIR-ko)
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
  backing_dataset: NanoBEIR-ko
  dataset_id: hakari-bench/NanoBEIR-ko
  task_name: NanoSCIDOCS
  split_name: NanoSCIDOCS
  language: ko
  category: natural_language
  document_path: docs/benchmark_tasks/MNanoBEIR/NanoBEIR-ko__NanoSCIDOCS.md
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
    query_mean: 32.1
    document_mean: 452.833937
  bm25:
    ndcg_at_10: 0.2672595100113479
    hit_at_10: 0.74
    source: dataset_candidate_subset
  candidate_subsets:
    bm25:
      config: bm25
      label: BM25
      source: dataset_candidate_subset
      top_k: 500
      ndcg_at_10: 0.26725951
      hit_at_10: 0.74
      recall_at_100: 0.606557377
      candidate_count_min: 500
      candidate_count_max: 500
      candidate_count_mean: 500.0
      query_count: 50
      query_coverage: 1.0
      relevant_coverage_at_100: 0.606557377
    dense:
      config: harrier_oss_v1_270m
      label: Dense
      source: dataset_candidate_subset
      top_k: 500
      ndcg_at_10: 0.330995521
      hit_at_10: 0.86
      recall_at_100: 0.643442623
      candidate_count_min: 500
      candidate_count_max: 500
      candidate_count_mean: 500.0
      query_count: 50
      query_coverage: 1.0
      relevant_coverage_at_100: 0.643442623
    reranking_hybrid:
      config: reranking_hybrid
      label: Reranking hybrid
      source: dataset_candidate_subset
      top_k: 100
      ndcg_at_10: 0.338003064
      hit_at_10: 0.88
      recall_at_100: 0.643442623
      candidate_count_min: 100
      candidate_count_max: 101
      candidate_count_mean: 100.02
      query_count: 50
      query_coverage: 1.0
      relevant_coverage_at_100: 0.643442623
      safeguard_positive_rows: 1
      rows_with_101_candidates: 1
```
