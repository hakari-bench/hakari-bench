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
| 뱅가드가 제시하는 수익률은 어떤 유형인가요? | 벤처가드 페이지에서 S&P 데이터를 찾기 쉬워서 이 방법이 가장 쉬워 보였다. MoneyChimp 데이터는 산술 평균이 아닌 CAGR을 제공한다는 것을 확인시켜 준다. |
| 프리랜서의 세금 문제 | 미국에서 소득이 있는 경우, 조세조약에서 달리 규정하지 않는 한 해당 소득에 대해 미국 소득세를 납부해야 합니다. |
| 거래량에 대해 이야기할 때 높음과 낮음은 무엇을 기준으로 하나요? | 일일 거래량은 보통 해당 주식의 과거 50일 동안의 평균 일일 거래량과 비교한다. |
| 신용카드 포인트를 사용하여 공제 가능한 사업 비용 납부하기 | 일반적으로 개인용 신용카드의 캐시백은 과세 대상이 아니지만, 사업용으로 사용하는 경우는 과세 대상이 될 수 있다. |
| 계약자로서 세금은 어떻게 신고해야 하나요? | 세금 신고를 위해서는 근로자로서 신고해야 할 뿐 아니라, 사업자로서도 신고해야 합니다. |

### Public Sources

- [FiQA 2018](https://doi.org/10.1145/3184558.3192301).
- [BEIR: A Heterogeneous Benchmark for Zero-shot Evaluation of Information Retrieval Models](https://arxiv.org/abs/2104.08663).
- [MMTEB: Massive Multilingual Text Embedding Benchmark](https://arxiv.org/abs/2502.13595).
- [Zeta Alpha NanoBEIR collection](https://huggingface.co/collections/zeta-alpha-ai/nanobeir).
- [hakari-bench/NanoBEIR-ko](https://huggingface.co/datasets/hakari-bench/NanoBEIR-ko).

### Source Reference Table

| Title | Year | Type | URL |
| --- | ---: | --- | --- |
| FiQA 2018 | 2018 | task paper | https://doi.org/10.1145/3184558.3192301 |
| BEIR: A Heterogeneous Benchmark for Zero-shot Evaluation of Information Retrieval Models | 2021 | benchmark paper | https://arxiv.org/abs/2104.08663 |
| MMTEB: Massive Multilingual Text Embedding Benchmark | 2025 | benchmark paper | https://arxiv.org/abs/2502.13595 |
| NanoBEIR: Smaller BEIR dataset subsets | 2024 | dataset collection | https://huggingface.co/collections/zeta-alpha-ai/nanobeir |
