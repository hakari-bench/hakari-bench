# MNanoBEIR / NanoBEIR-ko / NanoDBPedia

## Overview

`NanoBEIR-ko__NanoDBPedia` is the Korean NanoBEIR version of DBpedia-Entity, an
entity retrieval benchmark. The task uses Korean translated entity-style
queries and asks a retriever to rank Korean translated DBpedia entity
descriptions. The Nano split contains 50 queries, 6,045 documents, and 1,158
positive qrels. It is strongly multi-positive: the average query has 23.16
positives, and 48 of 50 queries have more than one relevant entity. This makes
the benchmark a short-query entity search task where exact names help, but
category-level and description-level semantic matching are also important.

## Details

### What the Original Data Measures

[DBpedia-Entity V2](https://doi.org/10.1145/3077136.3080751) evaluates entity
search over DBpedia. BEIR includes it as an entity retrieval task, and this
Korean NanoBEIR version evaluates the same setting through translated queries
and translated entity descriptions. Queries can be exact entity references,
partial names, or category-style needs such as films shot in a location or
entities related to a historical region. The retriever must rank compact
descriptions that satisfy the entity need.

### Observed Data Profile

The task has 50 queries and 6,045 documents. It contains 1,158 positive qrels,
with positives per query ranging from 1 to 81 and a median of 18.00. Queries
are very short, averaging 16.80 characters, while documents average 187.59
characters. The examples include a dealership and location, an Alice Munro
short-story collection, Gallo-Roman architecture in Paris, former Yugoslav
republics, and films shot in Venice. Many queries represent sets of valid
entities rather than one exact answer.

### BM25 Evaluation Profile

The BM25 top-500 subset reaches nDCG@10 = 0.5322, hit@10 = 0.9400, and
Recall@100 = 0.6520. BM25 is strong because entity names, locations, dates, and
category words often appear in both query and description. However, BM25 is
below dense and hybrid retrieval across the main ranking and coverage signals.
Very short Korean queries provide few lexical anchors, and many relevant
entities are described through attributes rather than the exact query words.

### Dense Evaluation Profile

The dense `harrier-oss-270m` top-500 subset reaches nDCG@10 = 0.5928, hit@10 =
0.9600, and Recall@100 = 0.6813. Dense retrieval is the strongest profile for
top-10 ranking quality. This suggests that embedding similarity helps connect
short entity needs to descriptions that are semantically compatible but not
lexically identical. It is especially valuable for category-style queries where
the relevant entity belongs to a class or relation implied by the query.

### Reranking Hybrid Evaluation Profile

The `reranking_hybrid` subset uses 100 candidates per query and reaches
nDCG@10 = 0.5787, hit@10 = 0.9600, and Recall@100 = 0.6839, with no rank-101
safeguard rows. Hybrid retrieval ties dense retrieval on hit@10 and is slightly
stronger on Recall@100, while dense remains stronger on nDCG@10. This indicates
that hybrid search provides the broadest candidate coverage, but dense-only
ranking orders the highest positions slightly better for this split.

### Metric Interpretation for Model Researchers

This task separates top-rank semantic ordering from candidate coverage. BM25 is
a strong exact-name baseline, dense retrieval provides the best nDCG@10, and
hybrid retrieval provides the best top-100 coverage. A model that improves this
benchmark should be analyzed for whether it handles exact entity labels,
category relations, or multi-positive coverage. Since many queries have dozens
of positives, top-100 recall and result diversity are important alongside
top-10 ranking.

### Query and Relevance Type Tendencies

The examples mix exact entity lookup with category-style retrieval. Some
queries contain distinctive names, while others describe a class of entities
such as films in a location or republics from a former state. Positive
documents are short DBpedia-style descriptions, so relevance depends on matching
the entity relation, not only the visible terms in the query.

### Representative Failure Modes

BM25 can retrieve descriptions that share names or locations but do not satisfy
the intended entity category. Dense retrieval can retrieve plausible related
entities that are not judged relevant. Hybrid retrieval can improve coverage
while still missing less obvious positives when a query has many valid
entities. Korean translation and transliteration variation can also affect both
lexical and dense matching.

### Training Data That May Help

Useful training data includes non-overlapping entity search, Wikipedia or
DBpedia entity linking, multilingual entity retrieval, and short-query passage
retrieval. Hard negatives should be related entities from the same category,
location, or time period that fail the specific query relation. Training should
exclude DBpedia-Entity, BEIR, NanoBEIR, and translated entity records likely to
overlap with this benchmark.

### Model Improvement Notes

Strong systems should combine exact label recall with semantic description
matching. For category-heavy queries, the model should retrieve a diverse set
of relevant entities rather than only the most lexically similar descriptions.
Hybrid candidate generation is useful for coverage, while reranking should
focus on whether each entity satisfies the query relation.

## Example Data

| Query | Positive document |
| --- | --- |
| 피츠제럴드 오토 몰 체임버스버그 펜실베이니아 [24 chars] | 피츠제럴드 오토몰은 1966년 메릴랜드주 베데스다에 첫 번째 지점을 오픈하며 설립된 가족 소유 및 운영 자동차 딜러십이다. 2014년 기준, 피츠제럴드 오토몰은 《오토모티브 뉴스》가 매년 발표하는 미국 '상위 125대 딜러십 그룹'에서 59위를 차지했다. 피츠제럴드 딜러 지점들은 2013년 워즈오토 이디일러 100에 8위, 25위, 30위, 43위, 98위... [200 / 216 chars] |
| 1994년 단편 소설집 앨리스 먼로는 열려 있다 [26 chars] | 앨리스 앤 먼로(/ˈælɨs ˌæn mʌnˈroʊ/, 본명 레이드로 /ˈleɪdlɔː/; 1931년 7월 10일 출생)는 캐나다의 작가이다. 먼로의 작품은 시간의 전후를 오가며 단편소설의 구조를 혁신시켰다고 평가받는다. 그녀의 작품은 "드러내기보다 숨기며, 과시하기보다 더 많이 드러낸다"고 표현되기도 한다. 먼로의 소설은 대개 그녀의 고향인 온타리오주 남서... [200 / 251 chars] |
| 파리의 갈로-로마 건축 [12 chars] | 파리의 예술은 프랑스의 수도인 파리의 예술 문화와 역사에 관한 글이다. 수세기 동안 파리는 전 세계의 예술가들을 끌어들여, 이들이 도시에 도착해 예술 교육을 받고 예술 자원 및 갤러리에서 영감을 얻고자 했다. 그 결과, 파리는 '예술의 도시'라는 명성을 얻게 되었다. [149 chars] |
| 구 유고슬라비아의 공화국들 [14 chars] | 1974년 유고슬라비아 헌법은 사회주의 연방 공화국 유고슬라비아의 네 번째이자 마지막 헌법이다. 이 헌법은 2월 21일 발효되었다. 원문 406개 조항으로 구성된 1974년 헌법은 세계에서 가장 긴 헌법 중 하나였다. 이 헌법은 자치 관리 체제를 국가의 간섭으로부터 보호하고 공화국과 자치주들이 모든 선거 및 정책 논의 장에서 더 넓은 대표성을 갖도록 하기... [200 / 216 chars] |
| 베니스에서 촬영된 영화들 [13 chars] | 《작은 로맨스》는 조지 로이 힐이 감독을 맡고 로렌스 올리비에, 셀로니어스 버나드, 그리고 영화 데뷔를 한 다이안 레인이 출연한 1979년 미국 테크니컬러 및 파나비전 로맨틱 코미디 영화이다. 각본은 조지 로이 힐과 앨런 번스가 패트릭 코뱅의 소설 『E=mc² Mon Amour』를 바탕으로 집필하였으며, 원곡 음악은 조르주 들뤼가 작곡하였다. [192 chars] |

### Public Sources

- [DBpedia-Entity V2](https://doi.org/10.1145/3077136.3080751).
- [BEIR: A Heterogeneous Benchmark for Zero-shot Evaluation of Information Retrieval Models](https://arxiv.org/abs/2104.08663).
- [MMTEB: Massive Multilingual Text Embedding Benchmark](https://arxiv.org/abs/2502.13595).
- [Zeta Alpha NanoBEIR collection](https://huggingface.co/collections/zeta-alpha-ai/nanobeir).
- [hakari-bench/NanoBEIR-ko](https://huggingface.co/datasets/hakari-bench/NanoBEIR-ko).

### Source Reference Table

| Title | Year | Type | URL |
| --- | ---: | --- | --- |
| DBpedia-Entity V2 | 2017 | task paper | [https://doi.org/10.1145/3077136.3080751](https://doi.org/10.1145/3077136.3080751) |
| BEIR: A Heterogeneous Benchmark for Zero-shot Evaluation of Information Retrieval Models | 2021 | benchmark paper | [https://arxiv.org/abs/2104.08663](https://arxiv.org/abs/2104.08663) |
| MMTEB: Massive Multilingual Text Embedding Benchmark | 2025 | benchmark paper | [https://arxiv.org/abs/2502.13595](https://arxiv.org/abs/2502.13595) |
| NanoBEIR: Smaller BEIR dataset subsets | 2024 | dataset collection | [https://huggingface.co/collections/zeta-alpha-ai/nanobeir](https://huggingface.co/collections/zeta-alpha-ai/nanobeir) |
