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
| 건강한 초콜릿 밀크쉐이크 | 목적 통풍 환자에서 체리 섭취와 재발성 통풍 발작 위험 간의 관계를 조사하는 것. |
| 의료 윤리 | 배경: 식이요법을 통한 혈중 콜레스테롤 조절에서 주요 문제 중 하나는 환자의 준수도를 향상시켜야 할 필요성이 있는 것으로 보인다. |
| 파바 콩 | 지난 20년 동안 L-아르기닌의 생화학, 영양학 및 약리학에 대한 관심이 증가했다. |
| 치킨 너겟에는 실제로 무엇이 들어 있을까? | 목적: 두 개의 전국적 패스트푸드 체인에서 제공하는 치킨너겟의 구성 성분을 파악하기 위함이다. |
| 포화 지방 | 임신 중 산모의 식이 섭취가 자녀의 알레르기 질환 발생에 영향을 미칠 수 있다는 가능성에 대한 관심이 증가하고 있다. |

### Public Sources

- [NFCorpus: A Full-Text Learning to Rank Dataset for Medical Information Retrieval](https://www.cl.uni-heidelberg.de/~riezler/publications/papers/ECIR2016.pdf).
- [BEIR: A Heterogeneous Benchmark for Zero-shot Evaluation of Information Retrieval Models](https://arxiv.org/abs/2104.08663).
- [MMTEB: Massive Multilingual Text Embedding Benchmark](https://arxiv.org/abs/2502.13595).
- [Zeta Alpha NanoBEIR collection](https://huggingface.co/collections/zeta-alpha-ai/nanobeir).
- [hakari-bench/NanoBEIR-ko](https://huggingface.co/datasets/hakari-bench/NanoBEIR-ko).

### Source Reference Table

| Title | Year | Type | URL |
| --- | ---: | --- | --- |
| NFCorpus: A Full-Text Learning to Rank Dataset for Medical Information Retrieval | 2016 | task paper | https://www.cl.uni-heidelberg.de/~riezler/publications/papers/ECIR2016.pdf |
| BEIR: A Heterogeneous Benchmark for Zero-shot Evaluation of Information Retrieval Models | 2021 | benchmark paper | https://arxiv.org/abs/2104.08663 |
| MMTEB: Massive Multilingual Text Embedding Benchmark | 2025 | benchmark paper | https://arxiv.org/abs/2502.13595 |
| NanoBEIR: Smaller BEIR dataset subsets | 2024 | dataset collection | https://huggingface.co/collections/zeta-alpha-ai/nanobeir |
