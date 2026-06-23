# MNanoBEIR / NanoBEIR-ko / NanoFiQA2018

## Overview

`NanoBEIR-ko__NanoFiQA2018` is the Korean NanoBEIR version of FiQA 2018, a
financial question-answer retrieval benchmark. The task uses Korean translated
personal-finance questions as queries and asks a retriever to rank Korean
translated answer passages. The Nano split contains 50 queries, 4,598
documents, and 123 positive qrels. More than half of the queries have multiple
positives, with 2.46 positives per query on average. The benchmark tests
whether retrieval models can match practical finance questions to answer
passages involving tax, investing, trading, credit card rewards, contracting,
and jurisdiction-specific advice.

## Details

### What the Original Data Measures

[FiQA 2018](https://doi.org/10.1145/3184558.3192301) was created around
financial opinion and question answering data. BEIR uses its retrieval version
as a finance-domain benchmark. In this Korean NanoBEIR version, translated
questions are matched against translated forum-style answers. The task measures
domain-specific answer retrieval: relevant passages must address the same
financial situation, not merely mention the same product, tax term, or market
concept.

### Observed Data Profile

The task has 50 queries and 4,598 documents. It contains 123 positive qrels,
with positives per query ranging from 1 to 15 and a median of 2.00. Queries
average 29.58 characters, while documents average 490.34 characters. The
examples include Vanguard return calculations, freelance tax implications,
stock volume, credit card points used for deductible business expenses, and tax
filing as a contractor. Queries are short and practical, while documents are
longer answers with caveats and assumptions.

### BM25 Evaluation Profile

The BM25 top-500 subset reaches nDCG@10 = 0.3415, hit@10 = 0.6000, and
Recall@100 = 0.5610. BM25 uses repeated financial terms effectively when the
query and answer share explicit words such as tax, volume, credit card, or
contractor. However, the low Recall@100 compared with dense and hybrid
retrieval shows that exact term matching misses many valid answers. Financial
advice is often expressed through explanatory reasoning, jurisdictional
context, or examples rather than the query's exact wording.

### Dense Evaluation Profile

The dense `harrier-oss-270m` top-500 subset reaches nDCG@10 = 0.3713, hit@10 =
0.6800, and Recall@100 = 0.7154. Dense retrieval improves over BM25 on all
reported metrics, indicating that embedding similarity is useful for matching a
short finance question to an answer's semantic content. It captures situational
similarity better than surface terms alone, especially when the answer explains
the same rule or decision with different vocabulary.

### Reranking Hybrid Evaluation Profile

The `reranking_hybrid` subset uses 100 to 101 candidates per query and reaches
nDCG@10 = 0.4291, hit@10 = 0.7000, and Recall@100 = 0.7236. Seven queries use
the rank-101 safeguard. Hybrid retrieval is the strongest profile across the
main metrics. It combines lexical financial anchors with dense semantic
matching, which is especially useful when a relevant answer shares both domain
terms and practical reasoning with the query.

### Metric Interpretation for Model Researchers

This task shows a clean BM25-to-dense-to-hybrid progression. BM25 captures
obvious term overlap but has weak coverage. Dense retrieval improves both
ranking and recall by modeling answer semantics. `reranking_hybrid` provides
the best top-10 quality and top-100 coverage, indicating that practical finance
retrieval benefits from both exact terminology and semantic advice matching.
Researchers should inspect whether gains come from financial-domain vocabulary,
jurisdictional context, or distinguishing answer-bearing passages from broad
finance discussion.

### Query and Relevance Type Tendencies

Queries are concise personal-finance questions. Relevant documents are
forum-style answers that often include assumptions, tax caveats, business versus
personal distinctions, or references to specific instruments. A document can
share visible finance words with the query and still be irrelevant if it
answers a different decision or legal context.

### Representative Failure Modes

BM25 can over-rank passages with matching terms that answer another financial
scenario. Dense retrieval can retrieve broadly related advice that lacks the
specific rule or assumption needed by the query. Hybrid retrieval improves
overall behavior but can still over-rank documents from the same broad finance
topic when jurisdiction, account type, or business status differs. Multi-
positive queries also test whether a system retrieves several valid answer
styles rather than one obvious response.

### Training Data That May Help

Useful training data includes non-overlapping financial QA, Korean finance
forum retrieval, tax and investing question-answer pairs, and multilingual
finance retrieval data. Hard negatives should share financial terms but answer
a different decision, jurisdiction, or business context. Training should
exclude FiQA, BEIR, NanoBEIR, and translated answer passages likely to overlap
with this benchmark.

### Model Improvement Notes

Strong systems should preserve financial terminology while modeling the user's
actual situation. Hybrid candidate generation is a natural fit, and reranking
should emphasize answer-bearing specificity, jurisdictional fit, and the
financial decision being asked about rather than broad topic similarity.

## Example Data

| Query | Positive document |
| --- | --- |
| 뱅가드가 제시하는 수익률은 어떤 유형인가요? [24 chars] | 벤처가드 페이지에서 - S&P 데이터를 찾기 쉬워서 이 방법이 가장 쉬워 보였다. 나는 MoneyChimp를 사용해서 데이터를 얻었으며, 이는 벤처가드 페이지가 산술 평균이 아닌 CAGR(복리 성장률)을 제공하고 있다는 것을 확인시켜 준다. 참고로, 벤처가드는 "미국 주식 시장 수익률의 경우 1926년부터 1957년 3월 3일까지 Standard & Poor's 90 지수를 사용한다"고 명시하고 있지만, MoneyChimp는 노벨상 수상자인 로버트 실러(Robert Shiller)의 웹사이트에서 제공하는 데이터를 사용한다. [295 chars] |
| 프리랜서의 세금 문제 [11 chars] | 미국에서 소득이 있는 경우, 귀하의 국가와 체결된 조세조약에서 달리 규정하지 않는 한, 해당 소득에 대해 미국 소득세를 납부해야 합니다. [76 chars] |
| 거래량에 대해 이야기할 때 높음과 낮음은 무엇을 기준으로 하나요? [36 chars] | 일일 거래량은 보통 해당 주식의 과거 50일 동안의 평균 일일 거래량과 비교한다. 높은 거래량은 일반적으로 해당 주식의 최근 50일 평균 일일 거래량의 2배 이상을 의미하지만, 일부 트레이더들은 특정 패턴이나 사건의 확인을 위해 기준을 평균 일일 거래량의 3배 또는 4배로 설정하기도 한다. 거래량은 다른 주식의 거래량과 비교하기보다는 해당 주식 자체의 평균 일일 거래량(ADV)과 비교하는 것이 일반적인데, 이는 서로 다른 기업들은 유통 주식 수, 유동성 수준, 변동성 수준이 모두 다르기 때문에 서로 다른 주식의 거래량을 비교하는 것은 사과와 오렌지를 비교하는 것과 같기 때문이다. 이러한 요소들은 모두 일일 거래량에 영향을 미칠 수 있다. [360 chars] |

### Public Sources

- [FiQA 2018](https://doi.org/10.1145/3184558.3192301).
- [BEIR: A Heterogeneous Benchmark for Zero-shot Evaluation of Information Retrieval Models](https://arxiv.org/abs/2104.08663).
- [MMTEB: Massive Multilingual Text Embedding Benchmark](https://arxiv.org/abs/2502.13595).
- [Zeta Alpha NanoBEIR collection](https://huggingface.co/collections/zeta-alpha-ai/nanobeir).
- [hakari-bench/NanoBEIR-ko](https://huggingface.co/datasets/hakari-bench/NanoBEIR-ko).

### Source Reference Table

| Title | Year | Type | URL |
| --- | ---: | --- | --- |
| FiQA 2018 | 2018 | task paper | [https://doi.org/10.1145/3184558.3192301](https://doi.org/10.1145/3184558.3192301) |
| BEIR: A Heterogeneous Benchmark for Zero-shot Evaluation of Information Retrieval Models | 2021 | benchmark paper | [https://arxiv.org/abs/2104.08663](https://arxiv.org/abs/2104.08663) |
| MMTEB: Massive Multilingual Text Embedding Benchmark | 2025 | benchmark paper | [https://arxiv.org/abs/2502.13595](https://arxiv.org/abs/2502.13595) |
| NanoBEIR: Smaller BEIR dataset subsets | 2024 | dataset collection | [https://huggingface.co/collections/zeta-alpha-ai/nanobeir](https://huggingface.co/collections/zeta-alpha-ai/nanobeir) |
