# MNanoBEIR / NanoBEIR-ko / NanoArguAna

## Overview

ArguAna is an argument-counterargument retrieval benchmark. `NanoBEIR-ko__NanoArguAna`
uses Korean translated argumentative passages as queries and retrieves Korean
translated counterarguments or closely paired arguments.

## Details

### What the Original Data Measures

[ArguAna](https://aclanthology.org/P18-1023/) was introduced for argument
retrieval and matching in debate-style text. BEIR includes ArguAna as an
argument retrieval task, and MMTEB provides the multilingual benchmark context.

### Observed Data Profile

The sampled task has 50 queries, 3,635 documents, and 50 positive qrels. Every
query has exactly one positive. Queries are long translated argumentative
passages averaging 619.40 characters, while documents average 519.64
characters.

### BM25 Difficulty

BM25 reaches nDCG@10 = 0.3666 and hit@10 = 0.6600. Long text gives BM25 many
lexical anchors, but matching the correct counterargument requires stance and
argument-structure understanding.

### Training Data That May Help

Useful data includes non-overlapping argument retrieval, debate counterargument
pairs, stance-aware retrieval, and Korean or multilingual argument mining data.
Training should exclude ArguAna, BEIR, NanoBEIR, and translated argument
records likely to overlap.

### Synthetic Data Guidance

Generate Korean claims and counterarguments from non-evaluation debate text.
Hard negatives should address the same topic while taking a different stance or
responding to a different premise.

## Example Data

| Query | Positive document |
| --- | --- |
| 대중은 개혁에 무관심하다. 현재의 경제 상황에서 상원 개혁이 최우선 과제가 되어야 하는지조차 논쟁의 여지가 있으며, 게다가 연립 정부가 그러한 조치를 시작하고 관철시킬 수 있을지조차 미지수이다. 상원 개혁을 시도하려는 노력은 수차례에 걸쳐 지연되어 왔으며, 이는 하원이 변화에 대해 보류하고 있는 태도를 보여준다.[1] 최근 대체 투표제 찬반 국민투표의 결과에서 드러났듯이, 이러한 분위기는 영국 대중의 ... [truncated 225 chars](473 chars) | AV 캠페인을 상원 개혁과 비교할 수는 없으며, 정치적 선전으로 인해 정보를 제대로 얻지 못하는 대중을 무관심과 혼동해서는 안 된다. 유권자들은 종종 자신들이 아무것도 바꿀 수 없고 자신의 투표가 의미가 없다고 느끼기 때문에 무관심을 표현한다. 국민이 직접 선출한 인물들이 나라를 운영하도록 보장하는 개혁은 이러한 감정을 해소하는 데 도움이 될 것이다. (197 chars) |
| 히드로 공항의 확장은 경제에 매우 중요하다. 히드로 공항을 확장하면 기존 일자리를 유지할 뿐 아니라 새로운 일자리도 창출할 수 있다. 현재 히드로 공항은 약 25만 개의 일자리를 뒷받침하고 있다.[1] 여기에 더해 수십만 명이 런던의 관광 산업에 의존하고 있는데, 이 산업은 히드로와 같은 우수한 교통망에 크게 의존하고 있다. 다른 유럽 공항들에 비해 경쟁력을 잃는 것은 단지 새로운 일자리 창출의 기회 ... [truncated 225 chars](725 chars) | 비즈니스 커뮤니티는 제3 활주로 건설에 대한 지지를 놓고 결코 단일한 입장이 아니다. 여론 조사에 따르면 실제로 영향력 있는 다수의 기업들이 확장을 지지하지 않는 것으로 나타났다. 저스틴 킹 J 세인스버리 최고경영자와 BskyB의 제임스 머독이 서명한 서한은 이에 대한 우려를 표명했다.[1] 따라서 비즈니스 커뮤니티를 확장 촉구의 단일한 목소리로 간주하는 것은 오해이다. 히스로 공항의 새로운 활주로 ... [truncated 225 chars](699 chars) |
| 사람들에게 너무 많은 선택권이 주어지는데, 이는 오히려 그들을 덜 행복하게 만든다. 광고는 사람들의 주의를 끌기 위한 끝없는 선택의 필요성 속에서 많은 이들이 압도당하게 만드는데, 이를 '선택의 폭정' 또는 '선택 과부하'라고 한다. 최근의 연구에 따르면, 사람들은 30년 전보다 더 나은 삶을 살고 있으며 돈을 쓸 수 있는 선택지도 훨씬 많음에도 불구하고 평균적으로 더 불행해졌다는 것이다1. 광고의 ... [truncated 225 chars](518 chars) | 사람들이 불행한 이유는 선택지가 너무 많아 스트레스를 받기 때문이 아니라, 모든 것을 가질 수 없기 때문이다. 실제로 광고는 사람들이 가진 돈을 자신에게 가장 적합한 제품에 쓸 수 있도록 보장하는 중요한 역할을 한다. 광고가 허용되지 않는다면, 사람들은 선택의 기회가 주어졌을 때 분명히 다른 제품을 선택할 텐데도 불구하고, 처음 접한 제품에 돈을 낭비하게 될 것이다. 50개의 독립적인 연구를 포함한 ... [truncated 225 chars](523 chars) |
| 사이버 공격은 종종 실제 국가와 무관한 비국가 행위자들, 예를 들어 사이버테러리스트나 해커 활동가(사회 운동을 위해 해킹을 하는 자)에 의해 수행된다. 예를 들어, 2007년 에스토니아를 대상으로 발생한 대규모 사이버 공격은 당시 두 국가 간의 긴장 관계로 인해 러시아의 소행으로 지목되었다[17]. 그러나 에스토니아에 대한 공격은 전 세계 각지에서 발생했으며, 러시아에서 발생한 것으로 보이는 공격조차 ... [truncated 225 chars](513 chars) | 비국가 행위자의 공격의 경우, 국제법 분야의 많은 전문가들은 다른 국가가 자국 영토 내에서 발생하는 공격에 대해 '효과적인 조치를 취할 의사가 없거나 능력이 없는' 상황이라면, 해당 국가가 여전히 자위권을 행사해 응징할 수 있다는 데 동의한다[19]. 이는 전통적 전쟁에 적용되며, 사이버전에도 동일하게 적용될 수 있다. 만약 어떤 국가가 사이버 보안을 확보하거나 사이버 공격자를 처벌하기 위해 아무 조 ... [truncated 225 chars](294 chars) |
| 종교는 믿음의 확실성을 장려하기 때문에, 신의 계시라는 이름 아래 증오를 정당화하고 폭력적 행동 및 차별적 관행을 조장하기가 용이하다. 표현의 자유는 그 발언이 해를 끼칠 가능성이 있을 때에는 둘째로 밀려나야 한다. "우리 편에 신이 계시다"는 구호는 역사적으로 학살과 잔혹 행위를 정당화하는 데 사용되어 왔으며, 여전히 사용되고 있다. 살인을 실제로 저지르는 이들이 대개 성직자나 설교자가 아닐지라도, ... [truncated 225 chars](790 chars) | 다른 사람의 말에 의해 폭력 행위를 강제당하는 사람은 없다. 그것은 그들 자신의 선택이다. 마찬가지로, 동성애 혐오적 시각을 가질 수 있는 많은 사람들이 실제로는 폭력 행위에 대해 경악할 것이다. 타인의 행동에 대해 내가 책임을 지지 않는 것은 개인에 대한 존중의 원칙에서 근본적인 것이다. 내가 돈이 없는 친구에게 농담 반담으로 은행을 털라고 제안하는 것과, 원고가 주장하는 선동 사이에는 명확한 경계 ... [truncated 225 chars](303 chars) |

## Dataset Information

| Field | Value |
| --- | --- |
| Nano set | MNanoBEIR |
| Backing dataset | NanoBEIR-ko |
| Task / split | NanoArguAna |
| Hugging Face dataset | [hakari-bench/NanoBEIR-ko](https://huggingface.co/datasets/hakari-bench/NanoBEIR-ko) |
| Language | ko |
| Category | natural_language |
| Queries | 50 |
| Documents | 3,635 |
| Positive qrels | 50 |
| BM25 nDCG@10 | 0.3666 |
| BM25 hit@10 | 0.6600 |
| Query length avg chars | 619.40 |
| Document length avg chars | 519.64 |

### Public Sources

- [Argument Mining for Understanding Peer Reviews](https://aclanthology.org/P18-1023/).
- [BEIR: A Heterogeneous Benchmark for Zero-shot Evaluation of Information Retrieval Models](https://arxiv.org/abs/2104.08663).
- [MMTEB: Massive Multilingual Text Embedding Benchmark](https://arxiv.org/abs/2502.13595).
- [Zeta Alpha NanoBEIR collection](https://huggingface.co/collections/zeta-alpha-ai/nanobeir).

### Hugging Face Links

- Nano dataset: [hakari-bench/NanoBEIR-ko](https://huggingface.co/datasets/hakari-bench/NanoBEIR-ko)
- Source collection: [Zeta Alpha NanoBEIR collection](https://huggingface.co/collections/zeta-alpha-ai/nanobeir)

### Source Reference Table

| Title | Year | Type | URL |
| --- | ---: | --- | --- |
| Argument Mining for Understanding Peer Reviews | 2018 | task paper | https://aclanthology.org/P18-1023/ |
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
  task_name: NanoArguAna
  split_name: NanoArguAna
  language: ko
  category: natural_language
  document_path: docs/benchmark_tasks/MNanoBEIR/NanoBEIR-ko__NanoArguAna.md
  source_research:
    primary_source_type: task_paper
    paper_pdf_or_html_checked: true
    no_paper_note: null
  counts:
    queries: 50
    documents: 3635
    positive_qrels: 50
  positives_per_query:
    average: 1.0
    min: 1
    median: 1.0
    max: 1
    multi_positive_queries: 0
    multi_positive_query_percent: 0.0
  text_stats_chars:
    query_mean: 619.4
    document_mean: 519.636314
  bm25:
    ndcg_at_10: 0.366582187
    hit_at_10: 0.66
    source: dataset_bm25_column
```
