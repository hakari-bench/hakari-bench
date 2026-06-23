# MNanoBEIR / NanoBEIR-ko / NanoClimateFEVER

## Overview

`NanoBEIR-ko__NanoClimateFEVER` is the Korean NanoBEIR version of
CLIMATE-FEVER, a climate-science fact-checking retrieval benchmark. The task
uses Korean translated climate claims as queries and asks a retriever to rank
Korean translated evidence passages. The Nano split contains 50 queries, 3,408
documents, and 148 positive qrels. Most queries have multiple positives, with
2.96 positives per query on average and 44 of 50 queries having more than one
evidence passage. This is a claim-to-evidence retrieval task where scientific
terminology, paraphrase, and broader climate context all matter.

## Details

### What the Original Data Measures

[CLIMATE-FEVER](https://arxiv.org/abs/2012.00614) extends FEVER-style claim
verification to climate change claims and evidence. BEIR frames it as an
evidence retrieval task: a system must retrieve passages that bear on a climate
claim before any verifier can determine support or refutation. In this Korean
NanoBEIR version, translated claims are matched against translated evidence
documents, testing whether retrieval models can connect short climate claims to
longer explanatory passages.

### Observed Data Profile

The task has 50 queries and 3,408 documents. It contains 148 positive qrels,
with positives per query ranging from 1 to 5 and a median of 3.00. Queries
average 66.02 characters, while documents average 779.69 characters. The
examples include warming periods, statistically insignificant trends, local sea
level variability, Hurricane Harvey, and CERN CLOUD claims about cosmic rays.
The evidence passages often explain mechanisms or scientific context rather
than repeating the claim verbatim.

### BM25 Evaluation Profile

The BM25 top-500 subset reaches nDCG@10 = 0.2457, hit@10 = 0.6000, and
Recall@100 = 0.5946. BM25 benefits when a claim and evidence share climate
terms, named events, or technical phrases. However, this is the weakest profile
overall. Climate evidence can be expressed through broader descriptions,
scientific mechanisms, or translated paraphrases that do not line up cleanly
with query terms. BM25 therefore provides useful anchors but struggles with
evidence-context matching.

### Dense Evaluation Profile

The dense `harrier-oss-270m` top-500 subset reaches nDCG@10 = 0.3003, hit@10 =
0.6200, and Recall@100 = 0.6216. Dense retrieval has the best nDCG@10 and
Recall@100, showing that semantic similarity helps connect climate claims to
evidence passages. It is still only moderately strong, which suggests that
scientific specificity remains difficult: a general climate-change passage can
be semantically related without being valid evidence for the exact claim.

### Reranking Hybrid Evaluation Profile

The `reranking_hybrid` subset uses 100 to 101 candidates per query and reaches
nDCG@10 = 0.2983, hit@10 = 0.7000, and Recall@100 = 0.6081. Three queries use
the rank-101 safeguard. Hybrid retrieval has the best hit@10, while dense is
slightly stronger on nDCG@10 and Recall@100. This means hybrid fusion is useful
for placing at least one relevant evidence passage in the top 10 more often,
but dense retrieval provides marginally better overall ranking and coverage for
the multi-positive evidence set.

### Metric Interpretation for Model Researchers

This task does not show a simple winner across every metric. Dense retrieval is
best for nDCG@10 and Recall@100, hybrid retrieval is best for hit@10, and BM25
is weakest. The pattern suggests that Korean climate evidence retrieval needs
semantic matching beyond term overlap, but exact lexical anchors still help with
top-10 first-hit behavior. Researchers should analyze whether gains come from
finding any evidence for a claim or from covering multiple supporting and
contextual passages.

### Query and Relevance Type Tendencies

Queries are compact climate claims, often phrased as assertions rather than
questions. Relevant documents may describe climate mechanisms, trends,
attribution, sea level, solar cycles, or greenhouse gas effects. The correct
evidence can be broader than the claim text, so relevance depends on whether
the passage bears on the assertion, not merely whether it discusses climate
change generally.

### Representative Failure Modes

BM25 can over-rank passages that repeat a climate term while failing to address
the claim. Dense retrieval can over-rank broad climate summaries that are
semantically related but not evidential. Hybrid retrieval can increase first-hit
success but still miss some relevant passages in the top 100. Multi-positive
queries expose whether a model retrieves only one obvious evidence type or
covers several scientific contexts.

### Training Data That May Help

Useful training data includes non-overlapping climate claim-evidence pairs,
scientific fact-checking retrieval, Korean climate science QA, and multilingual
claim verification data. Hard negatives should share climate terminology but
fail to support or refute the exact claim. Training should exclude
CLIMATE-FEVER, BEIR, NanoBEIR, and overlapping translated evidence from this
benchmark.

### Model Improvement Notes

Strong systems should combine climate terminology with claim decomposition and
evidence-context reasoning. Dense retrieval should be trained against hard
negatives that are topically climate-related but not evidential. Hybrid
candidate generation can help first-hit retrieval, while reranking should focus
on whether the passage actually supports, refutes, or contextualizes the claim.

## Example Data

| Query | Positive document |
| --- | --- |
| 1970년부터 1998년까지 약 0.7°F의 온도 상승을 가져온 온난화 시기가 있었으며, 이는 전지구적 온난화 경고 운동의 출현을 도왔다. [77 chars] | 파레오세(Paleocene, -LSB- 발음: /ˈpæliəˌsiːn/, /ˈpæ-/, /-lioʊ-/ -RSB-) 또는 파라이오세(Palaeocene)는 약 ~ 사이에 지속된 지질 시대의 한 시기로, '오래된 최근'을 의미한다. 이 시기는 현대의 신생대(제3기)에 속하는 파레오제(제3기)의 첫 번째 시대이다. 많은 지질 시대와 마찬가지로 이 시대의 시작과... [200 / 619 chars] |
| 사실, 통계적으로 유의미하지는 않지만 하락하는 추세이다. [31 chars] | 태양 주기 또는 태양 자기 활동 주기는 태양의 활동(태양 복사량과 태양 물질 방출 정도의 변화 포함)과 외형(태양 흑점, 플레어 및 기타 현상의 수와 크기 변화)에서 나타나는 거의 주기적인 11년 주기의 변화를 말한다. 이러한 변화는 수세기 동안 태양의 외형 변화와 오로라와 같은 지구상에서 관측되는 변화를 통해 관찰되어 왔다. 태양의 변화는 우주와 대기,... [200 / 260 chars] |
| 지역 및 지역적인 해수면은 여전히 전형적인 자연 변동성을 나타내고 있으며, 일부 지역에서는 상승하고 다른 지역에서는 하락하고 있다. [73 chars] | 평균 해수면(MSL, Mean Sea Level)은 지구의 해양 표면의 평균 수준으로, 고도(예: 해발 고도)를 측정하는 기준이 된다. MSL은 표준화된 지오데식 기준점인 수직 기준면으로, 예를 들어 지도 제작 및 해양 항해에서 사용되는 도법 기준면(chart datum)이나 항공 분야에서 대기압을 측정하여 고도를 보정하고 항공기 비행 고도층을 결정하는 기... [200 / 514 chars] |
| [기후 과학자들]은 허리케인 하비의 사례에서 나타나는 여러 측면이 지구 온난화가 나쁜 상황을 더욱 악화시키고 있음을 시사한다고 말한다. [75 chars] | 지구 온난화의 영향은 온실가스의 인간 배출로 인해 직접 또는 간접적으로 발생하는 환경적 및 사회적 변화이다. 기후 변화가 실제로 발생하고 있으며, 인간 활동이 주요 원인이라는 데 과학계의 합의가 있다. 빙하의 후퇴, 계절적 사건의 시기 변화(예: 식물의 개화 시기 조기화), 농업 생산성 변화 등 기후 변화의 많은 영향이 이미 관측되고 있다. 기후 변화의 미... [200 / 584 chars] |
| CERN의 CLOUD 실험은 우주선이 지구 온난화의 원인이라고 주장하기 위해 필요한 네 가지 조건 중 네 가지 중 하나의 3분의 1만을 테스트했으며, 나머지 조건 중 두 가지는 이... [100 / 115 chars] | 최근 기후 변화의 원인 규명은 지구상에서 관측되는 최근의 기후 변화, 즉 일반적으로 '지구 온난화'로 알려진 현상의 책임 있는 메커니즘을 과학적으로 밝히는 노력을 의미한다. 이 노력은 기온 기록 장비가 가장 신뢰할 수 있는 시기인 계기 온도 기록 기간 동안 관측된 변화에 초점을 맞추었으며, 특히 인간 활동이 가장 빠르게 증가하고 성층권 관측이 가능해진 최근... [200 / 948 chars] |

### Public Sources

- [CLIMATE-FEVER](https://arxiv.org/abs/2012.00614).
- [BEIR: A Heterogeneous Benchmark for Zero-shot Evaluation of Information Retrieval Models](https://arxiv.org/abs/2104.08663).
- [MMTEB: Massive Multilingual Text Embedding Benchmark](https://arxiv.org/abs/2502.13595).
- [Zeta Alpha NanoBEIR collection](https://huggingface.co/collections/zeta-alpha-ai/nanobeir).
- [hakari-bench/NanoBEIR-ko](https://huggingface.co/datasets/hakari-bench/NanoBEIR-ko).

### Source Reference Table

| Title | Year | Type | URL |
| --- | ---: | --- | --- |
| CLIMATE-FEVER | 2020 | task paper | [https://arxiv.org/abs/2012.00614](https://arxiv.org/abs/2012.00614) |
| BEIR: A Heterogeneous Benchmark for Zero-shot Evaluation of Information Retrieval Models | 2021 | benchmark paper | [https://arxiv.org/abs/2104.08663](https://arxiv.org/abs/2104.08663) |
| MMTEB: Massive Multilingual Text Embedding Benchmark | 2025 | benchmark paper | [https://arxiv.org/abs/2502.13595](https://arxiv.org/abs/2502.13595) |
| NanoBEIR: Smaller BEIR dataset subsets | 2024 | dataset collection | [https://huggingface.co/collections/zeta-alpha-ai/nanobeir](https://huggingface.co/collections/zeta-alpha-ai/nanobeir) |
