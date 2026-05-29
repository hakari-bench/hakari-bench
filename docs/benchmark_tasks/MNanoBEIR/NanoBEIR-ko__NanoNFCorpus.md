# MNanoBEIR / NanoBEIR-ko / NanoNFCorpus

## Overview

NFCorpus is a biomedical and nutrition-focused retrieval benchmark.
`NanoBEIR-ko__NanoNFCorpus` uses Korean translated health queries to retrieve
Korean translated biomedical documents.

## Details

### What the Original Data Measures

[NFCorpus](https://www.cl.uni-heidelberg.de/~riezler/publications/papers/ECIR2016.pdf)
was built for medical information retrieval over nutrition and health claims.
[BEIR](https://arxiv.org/abs/2104.08663) includes it as a biomedical retrieval
task, and [MMTEB](https://arxiv.org/abs/2502.13595) provides the multilingual
benchmark context.

### Observed Data Profile

The sampled Korean Nano task has 50 queries, 2,953 documents, and 1,651
positive qrels. It is highly multi-positive, averaging 33.02 positives per
query. Queries are often very short health phrases, averaging 10.82 characters;
documents are biomedical abstracts averaging 752.67 characters.

### BM25 Difficulty

BM25 reaches nDCG@10 = 0.3112 and hit@10 = 0.6200. Very short Korean queries
make lexical matching brittle, although exact biomedical terms can still help.
Good retrieval needs domain terminology and lay-health paraphrase handling.

### Training Data That May Help

Useful training data includes non-overlapping biomedical IR, nutrition QA,
clinical abstract retrieval, and Korean or multilingual health retrieval.
Training should exclude NFCorpus, BEIR, NanoBEIR, and overlapping medical
abstracts.

### Synthetic Data Guidance

Generate Korean health search phrases from non-evaluation biomedical abstracts.
Include short layperson queries and technical queries, with hard negatives that
share symptoms, foods, or organisms but address a different finding.

## Example Data

| Query | Positive document |
| --- | --- |
| 건강한 초콜릿 밀크쉐이크 (13 chars) | 목적 통풍 환자에서 체리 섭취와 재발성 통풍 발작 위험 간의 관계를 조사하는 것. 방법 우리는 일련의 가설적 위험 요인이 재발성 통풍 발작에 미치는 영향을 조사하기 위해 사례-교차 연구를 수행하였다. 통풍 환자들을 전향적으로 모집하여 1년간 온라인으로 추적 관찰하였다. 참가자들은 통풍 발작 발생 시 다음 정보를 보고하도록 하였다: 통풍 발작의 발병 일자, 증상 및 징후, 약물 복용 내역(통풍 치료 약 ... [truncated 225 chars](824 chars) |
| 의료 윤리 (5 chars) | 배경: 식이요법을 통한 혈중 콜레스테롤 조절에서 주요 문제 중 하나는 환자의 준수도를 향상시켜야 할 필요성이 있는 것으로 보인다. 목적: 콜레스테롤 저하 식이요법 준수에 대한 장벽과 동기를 둘러싼 여러 질문을 탐색하는 것. 방법: 고콜레스테롤혈증 환자를 대상으로 한 프랑스 일반의사들의 식이요법 관행을 조사하고, 환자들의 이러한 접근법에 대한 태도를 살펴보았다. 결과: 의사 234명의 개인 설문지와 환 ... [truncated 225 chars](959 chars) |
| 파바 콩 (4 chars) | 지난 20년 동안 L-아르기닌의 생화학, 영양학 및 약리학에 대한 관심이 증가함에 따라, 인간의 대사질환 예방 및 치료에서의 영양적·치료적 역할을 탐구하기 위한 광범위한 연구가 진행되어 왔다. 최근의 증거들은 식이성 L-아르기닌 보충이 유전적으로 비만한 쥐, 식이로 유도된 비만 쥐, 육성 돼지 및 제2형 당뇨병을 가진 비만 인간에게서 지방 축적을 감소시킨다는 것을 보여준다. L-아르기닌의 유익한 효과 ... [truncated 225 chars](579 chars) |
| 치킨 너겟에는 실제로 무엇이 들어 있을까? (23 chars) | 목적: 두 개의 전국적 패스트푸드 체인에서 제공하는 치킨너겟의 구성 성분을 파악하기 위함이다. 배경: 치킨너겟은 미국인의 식생활에서 주요한 부분을 차지하게 되었다. 우리는 이 고도로 가공된 식품의 현재 구성 성분을 조사하고자 하였다. 방법: 두 개의 서로 다른 전국적 패스트푸드 체인에서 무작위로 선택한 치킨너겟을 포르말린에 고정한 후 절편을 만들어 현미경 분석을 위한 염색을 실시하였다. 결과: 두 종 ... [truncated 225 chars](421 chars) |
| 포화 지방 (5 chars) | 임신 중 산모의 식이 섭취가 자녀의 알레르기 질환 발생에 영향을 미칠 수 있다는 가능성에 대한 관심이 증가하고 있다. 본 전향적 연구는 임신 기간 동안 지방산이 풍부한 특정 식품 및 특정 지방산의 섭취가 일본에서 3~4개월 된 영아의 의심되는 아토피 피부염 위험과 어떤 관련이 있는지를 조사하였다. 연구 대상은 771쌍의 산모와 자녀였다. 임신 중 산모의 식이 섭취 정보는 타당성이 입증된 자가 보고식 ... [truncated 225 chars](948 chars) |

## Dataset Information

| Field | Value |
| --- | --- |
| Nano set | MNanoBEIR |
| Backing dataset | NanoBEIR-ko |
| Task / split | NanoNFCorpus |
| Hugging Face dataset | [hakari-bench/NanoBEIR-ko](https://huggingface.co/datasets/hakari-bench/NanoBEIR-ko) |
| Language | ko |
| Category | natural_language |
| Queries | 50 |
| Documents | 2,953 |
| Positive qrels | 1,651 |
| Avg positives / query | 33.02 |
| Positives per query (min / median / max) | 1 / 23.50 / 100 |
| Queries with multiple positives | 47 (94.0%) |
| BM25 nDCG@10 | 0.2466 |
| BM25 hit@10 | 0.6200 |
| BM25 Recall@100 | 0.1399 |
| BM25 candidate subset | top-500 (`bm25`) |
| Dense nDCG@10 | 0.2332 |
| Dense hit@10 | 0.6600 |
| Dense Recall@100 | 0.1617 |
| Dense candidate subset | top-500 (`harrier_oss_v1_270m`) |
| Reranking hybrid nDCG@10 | 0.2440 |
| Reranking hybrid hit@10 | 0.5800 |
| Reranking hybrid Recall@100 | 0.1732 |
| Reranking hybrid candidate subset | top-100 plus optional rank-101 safeguard (`reranking_hybrid`) |
| Reranking hybrid candidates / query | 100-101 |
| Reranking hybrid safeguard rows | 9 |
| Query length avg chars | 10.82 |
| Document length avg chars | 752.67 |

### Public Sources

- [NFCorpus: A Full-Text Learning to Rank Dataset for Medical Information Retrieval](https://www.cl.uni-heidelberg.de/~riezler/publications/papers/ECIR2016.pdf).
- [BEIR: A Heterogeneous Benchmark for Zero-shot Evaluation of Information Retrieval Models](https://arxiv.org/abs/2104.08663).
- [MMTEB: Massive Multilingual Text Embedding Benchmark](https://arxiv.org/abs/2502.13595).
- [Zeta Alpha NanoBEIR collection](https://huggingface.co/collections/zeta-alpha-ai/nanobeir).

### Hugging Face Links

- Nano dataset: [hakari-bench/NanoBEIR-ko](https://huggingface.co/datasets/hakari-bench/NanoBEIR-ko)
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
  backing_dataset: NanoBEIR-ko
  dataset_id: hakari-bench/NanoBEIR-ko
  task_name: NanoNFCorpus
  split_name: NanoNFCorpus
  language: ko
  category: natural_language
  document_path: docs/benchmark_tasks/MNanoBEIR/NanoBEIR-ko__NanoNFCorpus.md
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
    query_mean: 10.82
    document_mean: 752.670166
  bm25:
    ndcg_at_10: 0.24660563066685093
    hit_at_10: 0.62
    source: dataset_candidate_subset
  candidate_subsets:
    bm25:
      config: bm25
      label: BM25
      source: dataset_candidate_subset
      top_k: 500
      ndcg_at_10: 0.2466056307
      hit_at_10: 0.62
      recall_at_100: 0.1399152029
      candidate_count_min: 500
      candidate_count_max: 500
      candidate_count_mean: 500.0
      query_count: 50
      query_coverage: 1.0
      relevant_coverage_at_100: 0.1399152029
    dense:
      config: harrier_oss_v1_270m
      label: Dense
      source: dataset_candidate_subset
      top_k: 500
      ndcg_at_10: 0.233185135
      hit_at_10: 0.66
      recall_at_100: 0.1617201696
      candidate_count_min: 500
      candidate_count_max: 500
      candidate_count_mean: 500.0
      query_count: 50
      query_coverage: 1.0
      relevant_coverage_at_100: 0.1617201696
    reranking_hybrid:
      config: reranking_hybrid
      label: Reranking hybrid
      source: dataset_candidate_subset
      top_k: 100
      ndcg_at_10: 0.2440001674
      hit_at_10: 0.58
      recall_at_100: 0.1732283465
      candidate_count_min: 100
      candidate_count_max: 101
      candidate_count_mean: 100.18
      query_count: 50
      query_coverage: 1.0
      relevant_coverage_at_100: 0.1732283465
      safeguard_positive_rows: 9
      rows_with_101_candidates: 9
```
