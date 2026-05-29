# MNanoBEIR / NanoBEIR-ko / NanoClimateFEVER

## Overview

CLIMATE-FEVER is a climate-science fact-checking retrieval task.
`NanoBEIR-ko__NanoClimateFEVER` is the Korean MNanoBEIR version: Korean
translated climate claims must retrieve Korean translated evidence passages.

## Details

### What the Original Data Measures

[CLIMATE-FEVER](https://arxiv.org/abs/2012.00614) extends FEVER-style claim
verification to climate change claims and evidence. [BEIR](https://arxiv.org/abs/2104.08663)
uses it as a fact-checking retrieval task, and [MMTEB](https://arxiv.org/abs/2502.13595)
provides the multilingual embedding benchmark context for this Korean split.

### Observed Data Profile

The sampled Korean Nano task has 50 queries, 3,408 documents, and 148 positive
qrel rows. Most queries have multiple positives: the average is 2.96, with a
range from 1 to 5. The average query length is 66.02 characters, and the
average document length is 779.69 characters.

The inspected examples include claims about brown bears in Alaska, polar ice
melt and methane release, sea-level variability, sea-ice decline, and wind-power
carbon footprints.

### BM25 Difficulty

Using the dataset-provided BM25 candidate column, BM25 reaches nDCG@10 =
0.2457 and hit@10 = 0.6000. BM25 ranks a positive first for 12 queries, and the
median first-positive rank is 5.

Lexical overlap helps when named entities and technical climate terms are
preserved, but the task still requires evidence matching under translation,
paraphrase, and scientific context.

### Training Data That May Help

Useful training data includes non-overlapping climate claim-evidence pairs,
scientific fact-checking retrieval data, and Korean or multilingual climate
science QA. Training should exclude CLIMATE-FEVER, BEIR, NanoBEIR, and
translated evidence likely to overlap with the evaluation records.

### Synthetic Data Guidance

Generate Korean climate claims from non-evaluation evidence passages and pair
them with evidence-bearing documents. Hard negatives should share climate terms
but fail to support or refute the exact claim.

## Example Data

| Query | Positive document |
| --- | --- |
| 1970년부터 1998년까지 약 0.7°F의 온도 상승을 가져온 온난화 시기가 있었으며, 이는 전지구적 온난화 경고 운동의 출현을 도왔다. (77 chars) | 파레오세(Paleocene, -LSB- 발음: /ˈpæliəˌsiːn/, /ˈpæ-/, /-lioʊ-/ -RSB-) 또는 파라이오세(Palaeocene)는 약 ~ 사이에 지속된 지질 시대의 한 시기로, '오래된 최근'을 의미한다. 이 시기는 현대의 신생대(제3기)에 속하는 파레오제(제3기)의 첫 번째 시대이다. 많은 지질 시대와 마찬가지로 이 시대의 시작과 끝을 정의하는 지층은 잘 알려져 있지만, 정 ... [truncated 225 chars](619 chars) |
| 사실, 통계적으로 유의미하지는 않지만 하락하는 추세이다. (31 chars) | 태양 주기 또는 태양 자기 활동 주기는 태양의 활동(태양 복사량과 태양 물질 방출 정도의 변화 포함)과 외형(태양 흑점, 플레어 및 기타 현상의 수와 크기 변화)에서 나타나는 거의 주기적인 11년 주기의 변화를 말한다. 이러한 변화는 수세기 동안 태양의 외형 변화와 오로라와 같은 지구상에서 관측되는 변화를 통해 관찰되어 왔다. 태양의 변화는 우주와 대기, 지구 표면에 영향을 미친다. 태양 활동에서 가 ... [truncated 225 chars](260 chars) |
| 지역 및 지역적인 해수면은 여전히 전형적인 자연 변동성을 나타내고 있으며, 일부 지역에서는 상승하고 다른 지역에서는 하락하고 있다. (73 chars) | 평균 해수면(MSL, Mean Sea Level)은 지구의 해양 표면의 평균 수준으로, 고도(예: 해발 고도)를 측정하는 기준이 된다. MSL은 표준화된 지오데식 기준점인 수직 기준면으로, 예를 들어 지도 제작 및 해양 항해에서 사용되는 도법 기준면(chart datum)이나 항공 분야에서 대기압을 측정하여 고도를 보정하고 항공기 비행 고도층을 결정하는 기준으로 사용된다. 일반적이고 비교적 간단한 평 ... [truncated 225 chars](514 chars) |
| [기후 과학자들]은 허리케인 하비의 사례에서 나타나는 여러 측면이 지구 온난화가 나쁜 상황을 더욱 악화시키고 있음을 시사한다고 말한다. (75 chars) | 지구 온난화의 영향은 온실가스의 인간 배출로 인해 직접 또는 간접적으로 발생하는 환경적 및 사회적 변화이다. 기후 변화가 실제로 발생하고 있으며, 인간 활동이 주요 원인이라는 데 과학계의 합의가 있다. 빙하의 후퇴, 계절적 사건의 시기 변화(예: 식물의 개화 시기 조기화), 농업 생산성 변화 등 기후 변화의 많은 영향이 이미 관측되고 있다. 기후 변화의 미래 영향은 기후 변화 정책과 사회 발전에 따라 ... [truncated 225 chars](584 chars) |
| CERN의 CLOUD 실험은 우주선이 지구 온난화의 원인이라고 주장하기 위해 필요한 네 가지 조건 중 네 가지 중 하나의 3분의 1만을 테스트했으며, 나머지 조건 중 두 가지는 이미 실패한 것으로 나타났다. (115 chars) | 최근 기후 변화의 원인 규명은 지구상에서 관측되는 최근의 기후 변화, 즉 일반적으로 '지구 온난화'로 알려진 현상의 책임 있는 메커니즘을 과학적으로 밝히는 노력을 의미한다. 이 노력은 기온 기록 장비가 가장 신뢰할 수 있는 시기인 계기 온도 기록 기간 동안 관측된 변화에 초점을 맞추었으며, 특히 인간 활동이 가장 빠르게 증가하고 성층권 관측이 가능해진 최근 50년 동안의 변화에 집중되어 왔다. 주된 ... [truncated 225 chars](948 chars) |

## Dataset Information

| Field | Value |
| --- | --- |
| Nano set | MNanoBEIR |
| Backing dataset | NanoBEIR-ko |
| Task / split | NanoClimateFEVER |
| Hugging Face dataset | [hakari-bench/NanoBEIR-ko](https://huggingface.co/datasets/hakari-bench/NanoBEIR-ko) |
| Language | ko |
| Category | natural_language |
| Queries | 50 |
| Documents | 3,408 |
| Positive qrels | 148 |
| Avg positives / query | 2.96 |
| Positives per query (min / median / max) | 1 / 3.00 / 5 |
| Queries with multiple positives | 44 (88.0%) |
| BM25 nDCG@10 | 0.2457 |
| BM25 hit@10 | 0.6000 |
| BM25 Recall@100 | 0.5946 |
| BM25 candidate subset | top-500 (`bm25`) |
| Dense nDCG@10 | 0.3003 |
| Dense hit@10 | 0.6200 |
| Dense Recall@100 | 0.6216 |
| Dense candidate subset | top-500 (`harrier_oss_v1_270m`) |
| Reranking hybrid nDCG@10 | 0.2983 |
| Reranking hybrid hit@10 | 0.7000 |
| Reranking hybrid Recall@100 | 0.6081 |
| Reranking hybrid candidate subset | top-100 plus optional rank-101 safeguard (`reranking_hybrid`) |
| Reranking hybrid candidates / query | 100-101 |
| Reranking hybrid safeguard rows | 3 |
| Query length avg chars | 66.02 |
| Document length avg chars | 779.69 |

### Public Sources

- [CLIMATE-FEVER](https://arxiv.org/abs/2012.00614).
- [BEIR: A Heterogeneous Benchmark for Zero-shot Evaluation of Information Retrieval Models](https://arxiv.org/abs/2104.08663).
- [MMTEB: Massive Multilingual Text Embedding Benchmark](https://arxiv.org/abs/2502.13595).
- [Zeta Alpha NanoBEIR collection](https://huggingface.co/collections/zeta-alpha-ai/nanobeir).

### Hugging Face Links

- Nano dataset: [hakari-bench/NanoBEIR-ko](https://huggingface.co/datasets/hakari-bench/NanoBEIR-ko)
- Source collection: [Zeta Alpha NanoBEIR collection](https://huggingface.co/collections/zeta-alpha-ai/nanobeir)

### Source Reference Table

| Title | Year | Type | URL |
| --- | ---: | --- | --- |
| CLIMATE-FEVER | 2020 | task paper | https://arxiv.org/abs/2012.00614 |
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
  task_name: NanoClimateFEVER
  split_name: NanoClimateFEVER
  language: ko
  category: natural_language
  document_path: docs/benchmark_tasks/MNanoBEIR/NanoBEIR-ko__NanoClimateFEVER.md
  source_research:
    primary_source_type: task_paper
    paper_pdf_or_html_checked: true
    no_paper_note: null
  counts:
    queries: 50
    documents: 3408
    positive_qrels: 148
  positives_per_query:
    average: 2.96
    min: 1
    median: 3.0
    max: 5
    multi_positive_queries: 44
    multi_positive_query_percent: 88.0
  text_stats_chars:
    query_mean: 66.02
    document_mean: 779.685739
  bm25:
    ndcg_at_10: 0.24568861434329187
    hit_at_10: 0.6
    source: dataset_candidate_subset
  candidate_subsets:
    bm25:
      config: bm25
      label: BM25
      source: dataset_candidate_subset
      top_k: 500
      ndcg_at_10: 0.2456886143
      hit_at_10: 0.6
      recall_at_100: 0.5945945946
      candidate_count_min: 500
      candidate_count_max: 500
      candidate_count_mean: 500.0
      query_count: 50
      query_coverage: 1.0
      relevant_coverage_at_100: 0.5945945946
    dense:
      config: harrier_oss_v1_270m
      label: Dense
      source: dataset_candidate_subset
      top_k: 500
      ndcg_at_10: 0.3002690996
      hit_at_10: 0.62
      recall_at_100: 0.6216216216
      candidate_count_min: 500
      candidate_count_max: 500
      candidate_count_mean: 500.0
      query_count: 50
      query_coverage: 1.0
      relevant_coverage_at_100: 0.6216216216
    reranking_hybrid:
      config: reranking_hybrid
      label: Reranking hybrid
      source: dataset_candidate_subset
      top_k: 100
      ndcg_at_10: 0.2983479087
      hit_at_10: 0.7
      recall_at_100: 0.6081081081
      candidate_count_min: 100
      candidate_count_max: 101
      candidate_count_mean: 100.06
      query_count: 50
      query_coverage: 1.0
      relevant_coverage_at_100: 0.6081081081
      safeguard_positive_rows: 3
      rows_with_101_candidates: 3
```
