# MNanoBEIR / NanoBEIR-ko / NanoNFCorpus

## Overview

`NanoBEIR-ko__NanoNFCorpus` is the Korean NanoBEIR version of NFCorpus, a
biomedical and nutrition information retrieval benchmark. The task uses Korean
translated health queries and asks a retriever to rank Korean translated
biomedical documents. The Nano split contains 50 queries, 2,953 documents, and
1,651 positive qrels. It is highly multi-positive: the average query has 33.02
positives, and 47 of 50 queries have more than one relevant document. The task
therefore tests broad biomedical coverage for very short health phrases as much
as top-rank precision.

## Details

### What the Original Data Measures

[NFCorpus](https://www.cl.uni-heidelberg.de/~riezler/publications/papers/ECIR2016.pdf)
was built for medical information retrieval over nutrition and health claims.
BEIR includes it as a biomedical retrieval benchmark, and this Korean NanoBEIR
version evaluates the same setting through translated queries and biomedical
abstracts. The task connects short health information needs to scientific
documents, so it stresses domain vocabulary, layperson-to-technical mapping,
and high-recall retrieval over many relevant abstracts.

### Observed Data Profile

The task has 50 queries and 2,953 documents. It contains 1,651 positive qrels,
with positives per query ranging from 1 to 100 and a median of 23.50. Queries
are extremely short, averaging 10.82 characters, while documents are much longer
biomedical abstracts averaging 752.67 characters. Examples include healthy
chocolate milkshakes, medical ethics, fava beans, chicken nuggets, and saturated
fat. This profile makes the benchmark difficult: one or two visible health
terms must retrieve a broad set of relevant scientific documents.

### BM25 Evaluation Profile

The BM25 top-500 subset reaches nDCG@10 = 0.2466, hit@10 = 0.6200, and
Recall@100 = 0.1399. BM25 has the best nDCG@10, which means exact biomedical or
nutrition terms are still valuable for the very top ranks. However, its
Recall@100 is low because many relevant documents use different terminology or
belong to related biomedical subtopics. For broad multi-positive queries, exact
term matching can find a good early document while missing much of the relevant
set.

### Dense Evaluation Profile

The dense `harrier-oss-270m` top-500 subset reaches nDCG@10 = 0.2332, hit@10 =
0.6600, and Recall@100 = 0.1617. Dense retrieval has the best hit@10 and better
coverage than BM25, but its top-ranked order is weaker by nDCG@10. This
suggests that embedding similarity can find semantically related biomedical
documents for short Korean queries, but it may rank broad topical abstracts
above the most directly relevant ones. Dense retrieval helps exploration more
than early precision on this split.

### Reranking Hybrid Evaluation Profile

The `reranking_hybrid` subset uses 100 to 101 candidates per query and reaches
nDCG@10 = 0.2440, hit@10 = 0.5800, and Recall@100 = 0.1732. Nine queries use
the rank-101 safeguard. Hybrid retrieval has the best Recall@100 and nearly
matches BM25 on nDCG@10, but it has the lowest hit@10. This indicates that the
hybrid candidate pool broadens relevant coverage, while the fused top ranks may
still need reranking to reliably place at least one positive in the first 10.

### Metric Interpretation for Model Researchers

This task is a precision-coverage tradeoff. BM25 is best for early graded
ranking, dense retrieval is best for first-hit behavior, and hybrid retrieval
is best for top-100 relevant coverage. Because most queries have many
positives, a low Recall@100 is expected, but relative differences are still
informative. Researchers should evaluate whether improvements come from exact
medical term handling, semantic expansion over related biomedical concepts, or
better coverage diversity.

### Query and Relevance Type Tendencies

Queries are short lay or technical health phrases. Relevant documents are
scientific abstracts with objectives, methods, and conclusions. A query such as
a food name, nutrient, or health phrase can have many relevant abstracts across
different biomedical mechanisms. This makes both synonym handling and
subtopic-diverse retrieval important.

### Representative Failure Modes

BM25 can miss abstracts that use technical synonyms or related biomedical terms
instead of the query phrase. Dense retrieval can overgeneralize to broad health
documents that are not judged relevant. Hybrid retrieval can improve coverage
but still rank noisy topical matches high. Since many positives exist per
query, low diversity is also a common failure: a model may retrieve many
similar abstracts while missing other relevant subtopics.

### Training Data That May Help

Useful training data includes non-overlapping biomedical IR, nutrition QA,
clinical abstract retrieval, and Korean or multilingual health retrieval.
Hard negatives should share symptoms, foods, organisms, or interventions but
address a different finding. Training should exclude NFCorpus, BEIR, NanoBEIR,
and overlapping translated medical abstracts from this benchmark.

### Model Improvement Notes

Strong systems should combine exact biomedical terminology with semantic
expansion over related concepts. Candidate generation should preserve precise
term matches, while reranking should learn which abstracts directly address the
health information need. Coverage diversity is important because each query can
have dozens of positives.

## Example Data

| Query | Positive document |
| --- | --- |
| 건강한 초콜릿 밀크쉐이크 [13 chars] | 목적 통풍 환자에서 체리 섭취와 재발성 통풍 발작 위험 간의 관계를 조사하는 것. 방법 우리는 일련의 가설적 위험 요인이 재발성 통풍 발작에 미치는 영향을 조사하기 위해 사례-교차 연구를 수행하였다. 통풍 환자들을 전향적으로 모집하여 1년간 온라인으로 추적 관찰하였다. 참가자들은 통풍 발작 발생 시 다음 정보를 보고하도록 하였다: 통풍 발작의 발병 일자, 증상 및 징후, 약물 복용 내역(통풍 치료 약물 포함), 그리고 통풍 발작 2일 전 기간 동안의 잠재적 위험 요인(체리 및 체리 추출물의 일일 섭취 포함). 동일한 노출 정보를 통제 기간(2일) 동안에 대해서도 평가하였다. 조건부 로지스틱 회귀분석을 사용하여 체리 섭취와 재발성 통풍 발작 위험 간의 관계를 추정하였다. 결과 본 연구에는 633명의 통풍 환자가 포함되었다. 2일간의 기간 동안 체리를 섭취하지 않은 경우와 비교할 때, 체리 섭취는 통풍 발작 위험이 35% 낮아지는 것과 연관되었다(다변량 오즈비[OR] = 0.65, 95% 신뢰구간[CI]: 0.50-0.85). 체리 추출물 섭취 역시 유사한 역상관 관계를 보였다(다변량 OR=0.55, 95% CI: 0.30-0.98). 체리 섭취의 효과는 성별, 비만 상태, 퓨린 섭취량, 알코올 사용, 이뇨제 사용, 통풍 치료 약물 사용 여부 등 다양한 하위 그룹에서 일관되게 나타났다. 체리 섭취와 알로푸리놀 복용을 함께 할 경우, 두 요인 모두 노출되지 않은 기간에 비해 통풍 발작 위험이 75% 감소하였다(OR=0.25, 95% CI: 0.15-0.42). 결론 이 연구 결과는 체리 섭취가 통풍 발작 위험 감소와 관련이 있음을 시사한다. [824 chars] |
| 의료 윤리 [5 chars] | 배경: 식이요법을 통한 혈중 콜레스테롤 조절에서 주요 문제 중 하나는 환자의 준수도를 향상시켜야 할 필요성이 있는 것으로 보인다. 목적: 콜레스테롤 저하 식이요법 준수에 대한 장벽과 동기를 둘러싼 여러 질문을 탐색하는 것. 방법: 고콜레스테롤혈증 환자를 대상으로 한 프랑스 일반의사들의 식이요법 관행을 조사하고, 환자들의 이러한 접근법에 대한 태도를 살펴보았다. 결과: 의사 234명의 개인 설문지와 환자 356명의 자가 보고 설문지를 분석하였다. 환자들이 처방된 식이요법을 따르지 않는 이유로는 '이미 만족스러운 식습관을 가지고 있기 때문'(34.7%), '영양 섭취 제한을 견디고 싶지 않기 때문'(33.3%), '가정생활과 식이요법을 조화시키기 어려움'(27.8%), '콜레스테롤 저하 약물을 복용 중이기 때문'(22.2%) 등이 있었다. 환자들은 의사의 권고를 전반적으로 잘 이해하고 있었음에도 불구하고, 양측의 진술 사이에 일부 차이가 있었다. 의사들은 환자들이 식이요법이 콜레스테롤을 낮추고 약물 복용을 피하는 데 어떻게 도움이 되는지에 대한 설명이 더 필요하다고 널리 생각했지만, 환자 중 이와 같은 정보를 필요하다고 답한 비율은 39.4%에 불과했다. 또한 환자 준수에 대한 장벽과 동기와 관련해서도 다른 차이점들이 관찰되었다. 게다가 일부 식이요법 지침은 다른 것보다 준수하기 더 어려운 것으로 나타났다. 예를 들어, '생선을 더 많이 먹어야 한다'는 것을 기억하는 환자는 82.6%였지만 실제로 그렇게 실천하는 환자는 51.3%에 그쳤다. 마지막으로, 의사와 환자 모두 콜레스테롤 저하 식이요법의 효과에 대해 낮은 신뢰를 보였다. 결론: 환자 교육을 개선하고, 특히 환자의 위험 인식을 높이며, 영양사의 개입을 강화하는 것은 준수도 향상을 위해 탐색해볼 만한 동기 요인들이다. Copyright © 2012 Elsevier Masson SAS. All rights reserved. [959 chars] |
| 파바 콩 [4 chars] | 지난 20년 동안 L-아르기닌의 생화학, 영양학 및 약리학에 대한 관심이 증가함에 따라, 인간의 대사질환 예방 및 치료에서의 영양적·치료적 역할을 탐구하기 위한 광범위한 연구가 진행되어 왔다. 최근의 증거들은 식이성 L-아르기닌 보충이 유전적으로 비만한 쥐, 식이로 유도된 비만 쥐, 육성 돼지 및 제2형 당뇨병을 가진 비만 인간에게서 지방 축적을 감소시킨다는 것을 보여준다. L-아르기닌의 유익한 효과를 담당하는 기전은 복잡할 가능성이 높지만, 결국 에너지 섭취와 소비의 균형을 지방 감소 또는 백색 지방조직의 성장 억제 방향으로 변화시키는 데 관련되어 있다. 최근 연구들은 L-아르기닌 보충이 세포신호전달 물질(예: 일산화질소, 일산화탄소, 폴리아민, cGMP, cAMP)의 합성을 증가시키고, 전신적인 에너지 기질(예: 포도당 및 지방산)의 산화를 촉진하는 유전자들의 발현을 증가시킴으로써 미토콘드리아 생합성과 갈색 지방조직 발달을 자극할 수 있음을 시사한다. 따라서 L-아르기닌은 동물과 인간에서 지방 축적을 줄이고 근육량을 증가시키며 대사 프로파일을 개선할 수 있는 안전하고 비용 효율적인 영양소로서 큰 가능성을 지니고 있다. [579 chars] |

### Public Sources

- [NFCorpus: A Full-Text Learning to Rank Dataset for Medical Information Retrieval](https://www.cl.uni-heidelberg.de/~riezler/publications/papers/ECIR2016.pdf).
- [BEIR: A Heterogeneous Benchmark for Zero-shot Evaluation of Information Retrieval Models](https://arxiv.org/abs/2104.08663).
- [MMTEB: Massive Multilingual Text Embedding Benchmark](https://arxiv.org/abs/2502.13595).
- [Zeta Alpha NanoBEIR collection](https://huggingface.co/collections/zeta-alpha-ai/nanobeir).
- [hakari-bench/NanoBEIR-ko](https://huggingface.co/datasets/hakari-bench/NanoBEIR-ko).

### Source Reference Table

| Title | Year | Type | URL |
| --- | ---: | --- | --- |
| NFCorpus: A Full-Text Learning to Rank Dataset for Medical Information Retrieval | 2016 | task paper | [https://www.cl.uni-heidelberg.de/~riezler/publications/papers/ECIR2016.pdf](https://www.cl.uni-heidelberg.de/~riezler/publications/papers/ECIR2016.pdf) |
| BEIR: A Heterogeneous Benchmark for Zero-shot Evaluation of Information Retrieval Models | 2021 | benchmark paper | [https://arxiv.org/abs/2104.08663](https://arxiv.org/abs/2104.08663) |
| MMTEB: Massive Multilingual Text Embedding Benchmark | 2025 | benchmark paper | [https://arxiv.org/abs/2502.13595](https://arxiv.org/abs/2502.13595) |
| NanoBEIR: Smaller BEIR dataset subsets | 2024 | dataset collection | [https://huggingface.co/collections/zeta-alpha-ai/nanobeir](https://huggingface.co/collections/zeta-alpha-ai/nanobeir) |
