# MNanoBEIR / NanoBEIR-ko / NanoSciFact

## Overview

`NanoBEIR-ko__NanoSciFact` is the Korean NanoBEIR version of SciFact, a
scientific claim verification retrieval benchmark. The task uses Korean
translated scientific claims as queries and asks a retriever to rank Korean
translated abstracts that provide evidence for support or refutation. The Nano
split contains 50 queries, 2,919 documents, and 56 positive qrels. Most queries
have one positive, while 4 queries have multiple positives. This is a
claim-to-evidence task where exact biomedical terminology is highly predictive,
but semantic context still matters for ranking the strongest evidence.

## Details

### What the Original Data Measures

[Fact or Fiction: Verifying Scientific Claims](https://arxiv.org/abs/2004.14974)
introduced SciFact as expert-written scientific claims paired with evidence
abstracts, support/refute labels, and rationales. BEIR evaluates the retrieval
step: a verifier cannot decide a claim unless the evidence abstract is first
retrieved. In this Korean NanoBEIR version, translated biomedical claims are
matched against translated abstracts, testing whether a model can preserve
scientific entity specificity while matching the claim's finding.

### Observed Data Profile

The task has 50 queries and 2,919 documents. It contains 56 positive qrels,
with 1.12 positives per query on average. The positives-per-query distribution
is 1 minimum, 1.00 median, and 4 maximum, and only 8.0% of queries are
multi-positive. Queries average 46.28 characters, while documents average
723.55 characters. The examples cover neutrophil migration, antiretroviral
therapy and tuberculosis, interferon-induced genes, cervical cancer screening,
and TDP-43 interactions.

### BM25 Evaluation Profile

The BM25 top-500 subset reaches nDCG@10 = 0.6835, hit@10 = 0.8600, and
Recall@100 = 0.9286. BM25 is very strong because claims and abstracts often
share distinctive genes, proteins, diseases, interventions, and outcome terms.
Exact term matching gives a reliable candidate pool and the best coverage. Its
remaining limitation is rank ordering: a term-overlapping abstract can discuss
the same entity without bearing on the exact claim.

### Dense Evaluation Profile

The dense `harrier-oss-270m` top-500 subset reaches nDCG@10 = 0.6207, hit@10 =
0.7800, and Recall@100 = 0.8571. Dense retrieval is weaker than BM25 on this
split. The result suggests that general semantic similarity can blur fine
biomedical distinctions. A passage about the same molecule, disease, or therapy
may be semantically close but not evidence for the exact claim. Dense retrieval
therefore needs domain-specific hard-negative training to compete here.

### Reranking Hybrid Evaluation Profile

The `reranking_hybrid` subset uses 100 to 101 candidates per query and reaches
nDCG@10 = 0.6838, hit@10 = 0.8400, and Recall@100 = 0.9107. Five queries use
the rank-101 safeguard. Hybrid retrieval is very slightly strongest on
nDCG@10, while BM25 remains stronger on hit@10 and Recall@100. This means that
combining lexical and dense signals can improve top-rank ordering, but lexical
candidate coverage remains essential for Korean SciFact.

### Metric Interpretation for Model Researchers

This task is not dense-dominant. BM25 is a hard baseline because biomedical
claim retrieval depends on exact terminology and relation specificity.
`reranking_hybrid` improves nDCG@10 only marginally, suggesting that dense
signals help order evidence when they reinforce lexical matches. Researchers
should preserve entity, intervention, and outcome precision rather than relying
on broad semantic similarity.

### Query and Relevance Type Tendencies

Queries are concise scientific claims. Relevant documents are abstracts that
describe experiments, observations, or clinical findings related to those
claims. Relevance depends on the exact scientific relation. A paper that shares
TDP-43, HPV, CD4, or interferon terminology can still be a distractor if it
does not support or refute the claim.

### Representative Failure Modes

BM25 can over-rank abstracts that share the right terms but describe a
different finding. Dense retrieval can over-rank same-domain abstracts that are
too broad or scientifically adjacent. Hybrid retrieval can improve top-rank
ordering but still lose some BM25 coverage. Retrieval errors are especially
harmful because downstream verification cannot recover if the evidence abstract
is absent.

### Training Data That May Help

Useful training data includes non-overlapping scientific fact verification,
claim-evidence retrieval, biomedical abstract retrieval, and Korean or
multilingual scientific NLI. Hard negatives should share terminology with the
claim but differ in the finding, intervention, or outcome. Training should
exclude SciFact, BEIR, NanoBEIR, and overlapping translated abstracts from this
benchmark.

### Model Improvement Notes

Strong systems should combine exact biomedical lexical recall with claim-level
semantic matching. Rerankers should attend to relation direction,
experimental context, and whether the abstract actually bears on the claim.
For this task, preserving BM25-like candidate coverage is a practical
requirement.

## Example Data

| Query | Positive document |
| --- | --- |
| Ly49Q는 막 래프트 기능을 조절함으로써 호중구 이동을 염증 부위로 조직하는 것을 조절한다. | 호중구는 감염 및 염증 부위로 신속하게 침윤하기 위해 빠르게 극성화되고 방향성 있는 운동을 한다. |
| 항레트로바이러스 요법은 다양한 CD4 계층에서 결핵 발생률을 감소시킨다. | HIV 감염은 결핵 발생의 가장 강력한 위험요인이며, 항레트로바이러스 요법은 HIV 관련 결핵 예방에 가능성을 지닌다. |
| 인터페론 유도 유전자의 급속한 상향 조절과 더 높은 기초 발현은 서부 나일 바이러스에 감염된 소뇌 과립세포 뉴런의 생존을 감소시킨다. | 뇌의 뉴런이 미생물 감염에 취약한 정도는 임상적 결과를 결정하는 주요 요인이다. |
| HPV 검출을 이용한 1차 자궁경부암 스크리닝은 기존의 세포진 검사보다 장기적 감도가 더 높다. | HPV 검사를 실시하면 고등급 자궁경부상피내신생물의 검출 감도가 증가한다. |
| TDP-43와 호흡 복합체 I 단백질 ND3 및 ND6 간의 상호작용을 차단하면 신경세포 손실이 증가한다. | TAR DNA 결합 단백질 43의 돌연변이는 근위축성 측삭 경화증을 유발하며, 신경퇴행성 질환에서 중요한 특징으로 나타난다. |

### Public Sources

- [Fact or Fiction: Verifying Scientific Claims](https://arxiv.org/abs/2004.14974).
- [SciFact repository](https://github.com/allenai/scifact).
- [BEIR: A Heterogeneous Benchmark for Zero-shot Evaluation of Information Retrieval Models](https://arxiv.org/abs/2104.08663).
- [MMTEB: Massive Multilingual Text Embedding Benchmark](https://arxiv.org/abs/2502.13595).
- [Zeta Alpha NanoBEIR collection](https://huggingface.co/collections/zeta-alpha-ai/nanobeir).
- [hakari-bench/NanoBEIR-ko](https://huggingface.co/datasets/hakari-bench/NanoBEIR-ko).

### Source Reference Table

| Title | Year | Type | URL |
| --- | ---: | --- | --- |
| Fact or Fiction: Verifying Scientific Claims | 2020 | task paper | https://arxiv.org/abs/2004.14974 |
| SciFact repository |  | project page | https://github.com/allenai/scifact |
| BEIR: A Heterogeneous Benchmark for Zero-shot Evaluation of Information Retrieval Models | 2021 | benchmark paper | https://arxiv.org/abs/2104.08663 |
| MMTEB: Massive Multilingual Text Embedding Benchmark | 2025 | benchmark paper | https://arxiv.org/abs/2502.13595 |
| NanoBEIR: Smaller BEIR dataset subsets | 2024 | dataset collection | https://huggingface.co/collections/zeta-alpha-ai/nanobeir |
