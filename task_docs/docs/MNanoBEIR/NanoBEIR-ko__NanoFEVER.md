# MNanoBEIR / NanoBEIR-ko / NanoFEVER

## Overview

`NanoBEIR-ko__NanoFEVER` is the Korean NanoBEIR version of FEVER, a fact
verification evidence retrieval benchmark. The task uses Korean translated
claims as queries and asks a retriever to rank Korean translated Wikipedia
passages that contain evidence for verification. The Nano split contains 50
queries, 4,996 documents, and 57 positive qrels. Most claims have one positive
evidence passage, while 6 queries have multiple positives. The task is a
compact test of claim-to-Wikipedia retrieval, where dense retrieval is the
strongest top-rank profile and hybrid retrieval gives the best top-100
coverage.

## Details

### What the Original Data Measures

[FEVER](https://arxiv.org/abs/1803.05355) introduced a large-scale fact
extraction and verification dataset built from claims and Wikipedia evidence.
BEIR evaluates the retrieval step: the system must find evidence passages before
a verifier can classify a claim as supported, refuted, or not enough
information. This Korean NanoBEIR version preserves that setting with
translated claims and translated Wikipedia passages. The task measures entity
matching, predicate matching, and evidence selection under Korean translation.

### Observed Data Profile

The task has 50 queries and 4,996 documents. It contains 57 positive qrels,
with 1.14 positives per query on average. The positives-per-query distribution
is 1 minimum, 1.00 median, and 3 maximum, and 12.0% of queries are
multi-positive. Queries are short claims averaging 26.38 characters, while
documents average 648.15 characters. The examples include claims about a rock
band, a sitcom, aircraft production in Burbank, Nero, and the film "Scream 2".

### BM25 Evaluation Profile

The BM25 top-500 subset reaches nDCG@10 = 0.5723, hit@10 = 0.7400, and
Recall@100 = 0.9123. BM25 benefits from entity names, titles, and distinctive
phrases in FEVER claims. It still trails the other profiles because the evidence
passage may express the claim through surrounding context, translated title
variation, or a predicate that does not repeat the query exactly. Lexical
matching provides a useful baseline but is not sufficient for best top-rank
evidence retrieval.

### Dense Evaluation Profile

The dense `harrier-oss-270m` top-500 subset reaches nDCG@10 = 0.7335, hit@10 =
0.9400, and Recall@100 = 0.9649. Dense retrieval is the strongest top-10
profile for this task. The result indicates that embedding similarity is highly
effective for mapping short Korean claims to evidence-bearing Wikipedia
passages, especially when the passage contains the answer context rather than
the exact claim wording. Dense retrieval also improves candidate coverage over
BM25.

### Reranking Hybrid Evaluation Profile

The `reranking_hybrid` subset uses 100 candidates per query and reaches
nDCG@10 = 0.7001, hit@10 = 0.9000, and Recall@100 = 0.9825, with no rank-101
safeguard rows. Hybrid retrieval has the best top-100 coverage, while dense
retrieval remains better on nDCG@10 and hit@10. This means that combining
lexical and dense candidates is valuable for downstream reranking, but the
fused order is not as strong as dense-only ranking near the top.

### Metric Interpretation for Model Researchers

This task separates semantic evidence ranking from candidate coverage. BM25 is
strong for exact entity recall, dense retrieval is best at placing evidence high
in the ranking, and hybrid retrieval is best at keeping positives in the top
100. A model improvement should be described in terms of whether it improves
claim semantics, entity recall, or reranker-ready candidate coverage. Since
most queries have one positive, early rank errors strongly affect nDCG@10.

### Query and Relevance Type Tendencies

Queries are short factual claims that usually contain an entity plus a
predicate. Relevant passages are Wikipedia summaries that provide the context
needed to verify the claim. A page about the same entity is not always enough;
the evidence must address the specific assertion, such as whether a program is
a sitcom or whether a film's country claim is true.

### Representative Failure Modes

BM25 can retrieve pages with the right entity but not the evidence-bearing
predicate. Dense retrieval can retrieve semantically related pages that do not
verify the claim. Hybrid retrieval can recover more positives in the candidate
set while still ranking topical distractors above evidence passages. Translation
variation in names and titles can affect all retrieval families.

### Training Data That May Help

Useful training data includes non-overlapping FEVER-style claim-evidence pairs,
Wikipedia evidence retrieval, Korean fact-checking data, and multilingual claim
verification. Hard negatives should come from the same entity page, nearby
entities, or title-sharing pages that do not verify the predicate. Training
should exclude FEVER, BEIR, NanoBEIR, and overlapping translated Wikipedia
evidence from this benchmark.

### Model Improvement Notes

Strong systems should preserve exact entity recall while learning to rank
predicate-relevant evidence. Dense retrieval already performs well at top-10
ranking, so a practical pipeline should use hybrid retrieval for coverage and a
reranker to recover dense-like evidence ordering.

## Example Data

| Query | Positive document |
| --- | --- |
| 키스 고쇼는 그레이트풀 데드를 잘 알고 있었다. [26 chars] | 그레이트풀 데드는 1965년 캘리포니아주 팔로 알토에서 결성된 미국의 록 밴드이다. 5인조에서 7인조까지 구성이 변했으며, 이 밴드는 록, 사이키델리아, 실험 음악, 모달 재즈, 컨트리, 포크, 블루그래스, 블루스, 레게, 스페이스 록 등 다양한 요소를 융합한 독특하고 독창적인 스타일로 알려져 있으며, 긴 즉흥 연주를 특징으로 하는 라이브 공연과 '데드헤즈(Deadheads)'라 불리는 열성적인 팬층으로도 유명하다. 레니 케이(Lenny Kaye)는 "그들의 음악은 다른 대부분의 밴드가 존재조차 모르는 영역을 다룬다"고 평했다. 이러한 다양한 영향들은 하나의 다양하고 사이키델릭한 음악 세계로 응축되어, 그레이트풀 데드를 "재즈 밴드 문화의 개척자이자 대부들"로 만들었다. 롤링 스톤지는 이 밴드를 '역사상 가장 위대한 아티스트 100'에서 57위로 선정했다. 그레이트풀 데드는 1994년 록 앤드 롤 명예의 전당에 헌액되었으며, 1977년 5월 8일 코넬 대학교 바튼 홀에서의 공연 녹음본은 2012년 미국 의회 도서관의 내셔널 레코딩 레지스트리에 등재되었다. 그레이트풀 데드는 전 세계적으로 3,500만 장 이상의 음반을 판매했다. 그레이트풀 데드는 1960년대 카운터컬처가 부상하던 시기에 샌프란시스코 베이 에어리어에서 결성되었다. 창단 멤버는 제리 가르시아(리드 기타, 보컬), 밥 와이어(리듬 기타, 보컬), 론 '피그펜' 맥커넌(키보드, 하모니카, 보컬), 필 레시(베이스, 보컬), 빌 크로이츠만(드럼)이다. 그레이트풀 데드의 멤버들은 이전에 모더 맥크리의 업타운 저그 챔피언스(Mother McCree's Uptown Jug Champions)와 워록스(The Warlocks) 등 샌프란시스코 지역의 여러 밴드에서 함께 연주한 적이 있다. 필 레시는 워록스가 그레이트풀 데드로 바뀌기 직전 마지막으로 합류한 멤버로, 단 몇 차례의 공연에서 베이스를 연주했던 다나 모건 주니어(Dana Morgan Jr.)를 대신하게 되었다. 드러머 마이키 하트와 무대에 서지 않는... [1,000 / 1,780 chars] |
| '타라크 메타 카 울타 카슈마'는 시트콤이다. [25 chars] | '타라크 메타의 올타흐 차슈마'(영어: Taarak Mehta's Different Perspective)는 넬라 텔레 필름 프라이빗 리미티드가 제작한 인도에서 가장 오래 방영된 시트콤 드라마이다. 이 프로그램은 2008년 7월 28일에 첫 방송을 시작했으며, 매주 월요일부터 금요일까지 오후 8시 30분에 방영되며, SAB TV에서 오후 11시와 다음날 오후 3시에 재방송된다. 이 프로그램은 2015년 11월 2일부터 소니 팔(Sony Pal)에서 매일 오후 4시 30분과 오후 8시에 재방송을 시작했다. 이 쇼는 타라크 메타가 구자라트어 주간지 치트랄레카(Chitralekha)를 위해 집필한 칼럼 '두니야 네 온다 차슈마(Duniya Ne Oondha Chashma)'를 바탕으로 제작되었다. [391 chars] |
| 캘리포니아 버뱅크에서는 비밀스럽고 기술적으로 진보된 비행기들이 생산되었다. [41 chars] | 버번크는 미국 캘리포니아주 남부 로스앤젤레스 카운티에 위치한 도시로, 로스앤젤레스 다운타운에서 북서쪽으로 약 12마일 떨어져 있다. 2010년 인구 조사 기준 인구는 103,340명이다. 할리우드에서 북동쪽으로 몇 마일 떨어진 곳에 위치한 버번크는 "세계의 미디어 수도"로 불리며, 월트 디즈니 컴퍼니, 워너브라더스 엔터테인먼트, 니켈로디언 애니메이션 스튜디오, NBC, 카툰 네트워크 스튜디오(카툰 네트워크의 서부 지사 포함), 인소미악 게임스 등 수많은 미디어 및 엔터테인먼트 회사의 본사 또는 주요 제작 시설이 자리잡고 있다. 이 도시는 밥 호프 공항의 소재지이기도 하다. 또한 록히드의 스컹크웍스가 위치했던 곳으로, 1962년 10월 쿠바에 배치된 소련 미사일 부품을 발견한 U-2 정찰기 등 가장 기밀을 유지하며 기술적으로 최첨단인 항공기를 개발한 곳이다. 버번크는 베르두고 산맥의 언덕 지대에 위치한 다운타운/언덕 지역과 평지 지역의 두 가지 뚜렷한 지역으로 구성되어 있다. 버번크는 샌퍼낸도 밸리에서 가장 동쪽에 위치한 도시이며, 인근의 글렌데일은 샌가브리엘 밸리에서 가장 서쪽에 위치한 도시이다. 이 도시는 《래프-인》과 《조니 캐슨의 투나잇 쇼》에서 "아름다운 다운타운 버번크"로 언급된 바 있다. 버번크라는 이름은 1867년 이곳에 양치기 목장을 세운 뉴햄프셔 출신의 치과의사이자 기업가인 데이비드 버번크의 이름을 따 지어졌다. [697 chars] |

### Public Sources

- [FEVER: a Large-scale Dataset for Fact Extraction and VERification](https://arxiv.org/abs/1803.05355).
- [BEIR: A Heterogeneous Benchmark for Zero-shot Evaluation of Information Retrieval Models](https://arxiv.org/abs/2104.08663).
- [MMTEB: Massive Multilingual Text Embedding Benchmark](https://arxiv.org/abs/2502.13595).
- [Zeta Alpha NanoBEIR collection](https://huggingface.co/collections/zeta-alpha-ai/nanobeir).
- [hakari-bench/NanoBEIR-ko](https://huggingface.co/datasets/hakari-bench/NanoBEIR-ko).

### Source Reference Table

| Title | Year | Type | URL |
| --- | ---: | --- | --- |
| FEVER: a Large-scale Dataset for Fact Extraction and VERification | 2018 | task paper | [https://arxiv.org/abs/1803.05355](https://arxiv.org/abs/1803.05355) |
| BEIR: A Heterogeneous Benchmark for Zero-shot Evaluation of Information Retrieval Models | 2021 | benchmark paper | [https://arxiv.org/abs/2104.08663](https://arxiv.org/abs/2104.08663) |
| MMTEB: Massive Multilingual Text Embedding Benchmark | 2025 | benchmark paper | [https://arxiv.org/abs/2502.13595](https://arxiv.org/abs/2502.13595) |
| NanoBEIR: Smaller BEIR dataset subsets | 2024 | dataset collection | [https://huggingface.co/collections/zeta-alpha-ai/nanobeir](https://huggingface.co/collections/zeta-alpha-ai/nanobeir) |
