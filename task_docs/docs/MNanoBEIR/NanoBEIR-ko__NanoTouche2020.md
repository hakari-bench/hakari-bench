# MNanoBEIR / NanoBEIR-ko / NanoTouche2020

## Overview

`NanoBEIR-ko__NanoTouche2020` is the Korean NanoBEIR version of the Touché 2020
argument retrieval benchmark for controversial questions. The task uses Korean
translated debate questions as queries and asks a retriever to rank Korean
translated argument documents that address each issue. The Nano split contains
49 queries, 5,745 documents, and 932 positive qrels. Every query is
multi-positive, with 19.02 positives per query on average. The task is
therefore a broad argument retrieval benchmark: finding at least one relevant
argument is often easy, while ranking substantive and diverse arguments remains
the main challenge.

## Details

### What the Original Data Measures

[Touché 2020](https://doi.org/10.1007/978-3-030-58219-7_26) evaluated argument
retrieval for controversial questions. Relevance depends on both topic match
and argumentative content: a useful result should give reasons, evidence, or a
position that addresses the issue. BEIR includes Touché 2020 as an argument
retrieval task. In this Korean NanoBEIR version, short translated controversial
questions are matched against long translated debate-style arguments.

### Observed Data Profile

The task has 49 queries and 5,745 documents. It contains 932 positive qrels,
with positives per query ranging from 6 to 32 and a median of 19.00. Every
query has multiple positives. Queries average 21.73 characters, while documents
are long, averaging 1,032.84 characters. The examples ask about homework,
direct-to-consumer prescription drug advertising, mandatory vaccines, abortion,
and standardized testing. Many relevant arguments exist for each topic, so
coverage and ranking quality both matter.

### BM25 Evaluation Profile

The BM25 top-500 subset reaches nDCG@10 = 0.5033, hit@10 = 0.9796, and
Recall@100 = 0.7371. BM25 is strong because controversial questions and debate
documents share visible topic terms. With many positives per query, lexical
retrieval almost always finds at least one relevant argument in the top 10.
BM25 is also slightly best on nDCG@10, suggesting that topic-word anchoring
orders many early arguments effectively.

### Dense Evaluation Profile

The dense `harrier-oss-270m` top-500 subset reaches nDCG@10 = 0.4564, hit@10 =
0.8776, and Recall@100 = 0.7189. Dense retrieval is weaker than BM25 here.
Broad semantic similarity can retrieve documents about the same controversy,
but argument relevance requires more than topical relatedness. A document must
address the question with substantive argumentative content, and dense
similarity alone can over-rank general opinion passages.

### Reranking Hybrid Evaluation Profile

The `reranking_hybrid` subset uses 100 candidates per query and reaches
nDCG@10 = 0.5013, hit@10 = 0.9796, and Recall@100 = 0.7618, with no rank-101
safeguard rows. Hybrid retrieval ties BM25 on hit@10 and provides the best
Recall@100, while BM25 remains very slightly higher on nDCG@10. This makes
hybrid retrieval the better candidate source for coverage, with BM25-like
early precision.

### Metric Interpretation for Model Researchers

This task is a BM25-and-hybrid strength case. Lexical topic matching is hard to
beat for early ranking because the queries are short and the positive pool is
large. Dense retrieval underperforms when it treats general topical similarity
as argument relevance. Hybrid retrieval improves coverage while retaining
BM25-like hit behavior. Researchers should inspect whether systems rank
substantive arguments, not merely documents that mention the topic.

### Query and Relevance Type Tendencies

Queries are short controversial questions. Positive documents are long debate
arguments containing claims, examples, evidence, and rhetorical framing. A
relevant document may argue for or against the issue, so stance is not the only
criterion. The model must match the issue and recognize argument content.

### Representative Failure Modes

BM25 can over-rank long documents that repeat the topic but contain weak or
off-target argumentation. Dense retrieval can retrieve broad opinion text that
does not directly address the question. Hybrid retrieval improves coverage but
can still mix strong arguments with topical distractors. Long documents also
create partial-match errors when only a small part of a document touches the
query topic.

### Training Data That May Help

Useful training data includes non-overlapping Touché argument retrieval, debate
portal argument collections, pro/con retrieval pairs, and Korean or
multilingual argument quality data. Hard negatives should share the same
controversial topic but lack a direct argument for the query. Training should
exclude Touché 2020, BEIR, NanoBEIR, and overlapping translated argument
documents from this benchmark.

### Model Improvement Notes

Strong systems should combine topic matching with argument-quality and
specificity signals. Candidate generation should retrieve many relevant pro and
con arguments, while reranking should favor documents that directly answer the
question with explicit reasons. Because every query has many positives,
coverage diversity is important.

## Example Data

| Query | Positive document |
| --- | --- |
| 숙제는 유익한가요? [10 chars] | 첫째, 숙제가 훌륭하며 현대 학교에서 계속되어야 할 세 가지 이유가 있다. 1. 숙제는 실천을 통해 배우는 학습자에게 도움이 된다. 일반적으로 세 가지 유형의 학습자가 있다. 듣고 배우는 사람, 보고 배우는 사람, 그리고 실천을 통해 배우는 사람이 그것이다. 많은 사람들이 특정 과목을 듣거나 보는 것으로 학습에 만족하지만, 일부는 실제로 해보아야 이해할 수 있다. 따라서 숙제는 후자 그룹에게 유익하다. 왜냐하면 그들은 행동을 통해 지식을 습득하기 때문이다. 2. 숙제는 학습 내용을 강화한다. 많은 사람들이 숙제 없이 지내는 것을 기뻐할지 모르지만, 숙제가 사라진다면 교육의 질은 분명히 저하될 것이다. 숙제가 배정된 독서, 기말 과제 등 어떤 형태이든 간에, 모두 학생들의 머릿속에 수업 내용을 다시 각인시키기 위해 고안된 것이다. 결국 숙제를 하는 학생들이 하지 않는 학생들보다 학업적으로 더 성공적이다. 이는 자명한 진리라고 생각하지만, 이를 반박하라는 것은 Pro에게 맡기겠다. 3. 숙제는 실제 생활의 요구를 반영한다. 고등학교 졸업 후 졸업생들이 갈 수 있는 길은 주로 두 가지다. 대학 진학 또는 직장 생활이다. 이 두 길 모두에서 과제가 배정되며, 교수나 상사들은 과제가 제때 완수되기를 기대한다. 숙제를 마감 기한 내에 해본 경험이 있는 졸업생들은 이러한 요구에 익숙하므로 성공할 가능성이 더 높다. 그러나 숙제가 사라진다면 학생들은 장기 과제, 마감 기한 등에 익숙하지 않게 될 것이다. 요컨대, 숙제는 졸업생들이 실제 생활의 요구에 대비하도록 돕는다. 이제 나는 Pro의 주장들을 반박하겠다. 1. "숙제를 확인하는 데 수업 시간이 소중하게 낭비된다." 아니, 이는 완전히 잘못된 주장이다. 교사들은 일반적으로 수업 시간에 숙제를 채점하지 않는다. 왜냐하면 수업 시간은 가르치는 시간이지 평가하는 시간이 아니기 때문이다. 교사들은 보통 자신의 사무실이나 집에서 채점을 하며, 이에 대한 보수를 받는다. 숙제 채점이 수업 시간에 영향을 미치는 경우는 거의, 아니 전... [1,000 / 1,872 chars] |
| 처방약을 소비자에게 직접 광고하는 것이 타당한가? [27 chars] | 많은 광고들은 약물의 효과에 대한 충분한 정보를 제공하지 않는다. 예를 들어, 루네스타(Lunesta)는 평화롭게 잠자는 사람 위로 침실 창문을 통해 날아드는 나방의 이미지로 광고된다. 실제로 루네스타는 6개월 치료 후 환자들이 15분 더 빨리 잠들게 하고, 밤에 평균 37분 더 잠을 자게 한다. 대부분의 광고는 감정적 호소에 기반하지만, 질환의 원인, 위험 요인, 중요한 생활 습관 변화에 대한 정보는 거의 포함하지 않는다. 38개의 제약 광고를 조사한 연구에서 연구자들은 82%가 사실에 근거한 주장을 했고, 86%가 제품 사용에 대한 합리적 근거를 제시했음을 발견했다. 그러나 질환의 원인, 위험 요인, 유병률을 설명한 광고는 고작 26%에 불과했다.[1] 따라서 환자들에게 균형 잡힌 정보를 제공하지 않아, 알약 하나를 복용하는 것이 문제의 마법 같은 해결책이 아님을 인식시키지 못하게 된다. 실제로 미국과 뉴질랜드에서 실시된 한 연구에 따르면, 조사된 진료 방문 중 12%에서 환자들이 처방을 요청했으며, 이 중 42%는 소비자 대상 광고된 제품이었다. 또한 환자들은 4개 이상의 의약품 이름을 기억하지 못했다.[2] 이는 환자들의 결정이 더 잘 informed된 상태에서 이루어지는 것이 아니라, 주로 광고된 약물에 대한 압박에 기반하고 있음을 보여준다. [1] 처방약 수요 창출: 텔레비전을 통한 소비자 직접 광고의 내용 분석. Ann Fam Med. 2007년 1월; 5(1): 6–13. http://www.ncbi.nlm.nih.gov/pmc/articles/PMC1783924/ [2] 민츠 B. 및 공동 연구자들, 소비자 직접 제약 광고와 환자 요청이 처방 결정에 미치는 영향: 두 지역 횡단적 설문조사, BMJ 2002, http://www.bmj.com/content/324/7332/278.full.pdf, 2011년 08월 01일 접근 [936 chars] |
| 아이들에게 어떤 백신이라도 의무화되어야 할까요? [26 chars] | 아직 완전한 주장은 아니다. 단지 내가 정리한 몇 가지 사항들이다. 정부는 부모가 자녀의 건강 문제에 대해 내리는 결정에 개입할 권리를 가져서는 안 된다. 미시간 대학교의 2010년 조사에 따르면, 자녀에게 의무화된 학교 입학 백신 접종을 거부할 권리가 있어야 한다고 생각하는 부모는 31%에 달한다. 많은 부모들이 백신 접종에 반대하는 종교적 신념을 가지고 있다. 이러한 부모들에게 백신 접종을 강요하는 것은 시민이 종교를 자유롭게 행사할 권리를 보장하는 헌법 제1조를 위반하는 것이다. 질병으로 인한 사망 위험이 낮은 경우가 많기 때문에 백신은 종종 불필요하다. 19세기 초에 면역화가 보급되기 이전에, 디프테리아, 홍역, 빨간열과 같은 소아 질환으로 인한 사망률은 이미 급격히 감소했다. 이러한 사망률 감소는 개인 위생의 개선, 정수 처리, 효과적인 하수 처리, 그리고 더 나은 식품 위생과 영양 상태 때문인 것으로 알려져 있다. 백신은 자연 법칙과 인간을 위한 하나님의 계획에 간섭한다. 질병은 자연스러운 현상이며, 인간은 그 진행 과정에 간섭해서는 안 된다. 일반적인 소아 백신은 드물지만 심각한 반응을 유발할 수 있는데, 아나필락시스 쇼크, 마비, 갑작스러운 사망 등이 있다. 이러한 위험은 대부분 예방하려는 질병들이 반드시 생명을 위협하는 것은 아니라는 점을 고려할 때 감수할 만한 가치가 없다. 백신은 관절염, 다발성 경화증, 루푸스, 길랭-바레 증후군(GBS) 및 기타 장애와 같은 자가면역 질환을 유발할 수 있다. 백신은 뇌염(encephalopathy)을 유발할 수 있으며, 이는 사망이나 영구적인 뇌 손상, 자폐증, 주의력결핍과잉행동장애(ADHD), 기타 발달 문제로 이어질 수 있다. 또한, 대부분의 1999년 이전 백신에 포함되어 있던 백신 첨가제인 티메로살(thimerosal)은 자폐증 발생과 관련이 있으며, 현재도 일부 수막염, 파상풍, 독감 백신(예: H1N1 백신)에 여전히 포함되어 있다. 백신은 외부 단백질 분자(백신 내 활성 성분)로 림프계를 막고... [1,000 / 2,132 chars] |

### Public Sources

- [Overview of Touché 2020: Argument Retrieval](https://doi.org/10.1007/978-3-030-58219-7_26).
- [Touche20-Argument-Retrieval-for-Controversial-Questions](https://doi.org/10.5281/zenodo.6862281).
- [BEIR: A Heterogeneous Benchmark for Zero-shot Evaluation of Information Retrieval Models](https://arxiv.org/abs/2104.08663).
- [MMTEB: Massive Multilingual Text Embedding Benchmark](https://arxiv.org/abs/2502.13595).
- [Zeta Alpha NanoBEIR collection](https://huggingface.co/collections/zeta-alpha-ai/nanobeir).
- [hakari-bench/NanoBEIR-ko](https://huggingface.co/datasets/hakari-bench/NanoBEIR-ko).

### Source Reference Table

| Title | Year | Type | URL |
| --- | ---: | --- | --- |
| Overview of Touché 2020: Argument Retrieval | 2020 | benchmark paper | [https://doi.org/10.1007/978-3-030-58219-7_26](https://doi.org/10.1007/978-3-030-58219-7_26) |
| Touche20-Argument-Retrieval-for-Controversial-Questions | 2022 | dataset page | [https://doi.org/10.5281/zenodo.6862281](https://doi.org/10.5281/zenodo.6862281) |
| BEIR: A Heterogeneous Benchmark for Zero-shot Evaluation of Information Retrieval Models | 2021 | benchmark paper | [https://arxiv.org/abs/2104.08663](https://arxiv.org/abs/2104.08663) |
| MMTEB: Massive Multilingual Text Embedding Benchmark | 2025 | benchmark paper | [https://arxiv.org/abs/2502.13595](https://arxiv.org/abs/2502.13595) |
| NanoBEIR: Smaller BEIR dataset subsets | 2024 | dataset collection | [https://huggingface.co/collections/zeta-alpha-ai/nanobeir](https://huggingface.co/collections/zeta-alpha-ai/nanobeir) |
