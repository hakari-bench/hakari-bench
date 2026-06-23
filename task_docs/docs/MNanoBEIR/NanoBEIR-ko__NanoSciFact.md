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
| Ly49Q는 막 래프트 기능을 조절함으로써 호중구 이동을 염증 부위로 조직하는 것을 조절한다. [52 chars] | 호중구는 감염 및 염증 부위로 신속하게 침윤하기 위해 빠르게 극성화되고 방향성 있는 운동을 한다. 본 연구에서 우리는 억제성 MHC I 수용체인 Ly49Q가 호중구의 신속한 극성화와 조직 침윤에 핵심적인 역할을 한다는 것을 보였다. 정상 상태에서 Ly49Q는 Src 및 PI3 키나제를 억제함으로써 초점 복합체 형성을 방지하여 호중구의 부착을 억제하였다. 그... [200 / 493 chars] |
| 항레트로바이러스 요법은 다양한 CD4 계층에서 결핵 발생률을 감소시킨다. [40 chars] | 배경 인간면역결핍바이러스(HIV) 감염은 결핵 발생의 가장 강력한 위험요인이며, 특히 사하라 이남 아프리카 지역에서 결핵의 재확산을 촉진시켰다. 2010년 전 세계적으로 HIV에 감염된 약 3,400만 명 중 결핵 신규 발생 건수는 약 110만 건으로 추정되었다. 항레트로바이러스 요법은 HIV 관련 결핵 예방에 상당한 가능성을 지닌다. 본 연구는 성인 HI... [200 / 1,116 chars] |
| 인터페론 유도 유전자의 급속한 상향 조절과 더 높은 기초 발현은 서부 나이로바 바이러스에 감염된 소뇌 과립세포 뉴런의 생존을 감소시킨다. [76 chars] | 뇌의 뉴런이 미생물 감염에 취약한 정도는 임상적 결과를 결정하는 주요 요인이지만, 이러한 취약성을 조절하는 분자적 요인들에 대해서는 거의 알려져 있지 않다. 본 연구에서 우리는 서로 다른 뇌 영역에 위치한 두 가지 유형의 뉴런이 여러 양성 가닥 RNA 바이러스의 복제에 대해 상이한 허용성을 나타냄을 보였다. 소뇌의 과립세포 뉴런과 대뇌피질의 피질 뉴런은 독... [200 / 556 chars] |
| HPV 검출을 이용한 1차 자궁경부암 스크리닝은 자궁경부상피내신생물 2도를 발견하기 위해 기존의 세포진 검사보다 장기적 감도가 더 높다. [76 chars] | 배경 자궁경부암 검진에서 인간유두종바이러스(HPV) 검사를 실시하면 고등급(등급 2 또는 3) 자궁경부상피내신생물의 검출 감도가 증가하지만, 이러한 이점이 과진단을 의미하는지 아니면 향후 고등급 자궁경부상피내신생물이나 자궁경부암에 대한 예방 효과를 나타내는지는 알려져 있지 않다. 방법 스웨덴의 인구 기반 검진 프로그램에서 32세에서 38세 사이의 여성 12... [200 / 1,043 chars] |
| TDP-43와 호흡 복합체 I 단백질 ND3 및 ND6 간의 상호작용을 차단하면 TDP-43 유도 신경세포 손실이 증가한다. [69 chars] | TAR DNA 결합 단백질 43(TARDBP, TDP-43로도 알려짐)의 유전적 돌연변이는 근위축성 측삭 경화증(ALS)을 유발하며, 다양한 신경퇴행성 질환에서 퇴행하는 뉴런의 주요 조직병리학적 특징으로 TDP-43(TARDBP 유전자에 의해 암호화됨)의 세포질 내 축적이 나타난다. 그러나 TDP-43가 ALS 병리생리에 기여하는 분자 기전은 여전히 명확하... [200 / 667 chars] |

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
| Fact or Fiction: Verifying Scientific Claims | 2020 | task paper | [https://arxiv.org/abs/2004.14974](https://arxiv.org/abs/2004.14974) |
| SciFact repository |  | project page | [https://github.com/allenai/scifact](https://github.com/allenai/scifact) |
| BEIR: A Heterogeneous Benchmark for Zero-shot Evaluation of Information Retrieval Models | 2021 | benchmark paper | [https://arxiv.org/abs/2104.08663](https://arxiv.org/abs/2104.08663) |
| MMTEB: Massive Multilingual Text Embedding Benchmark | 2025 | benchmark paper | [https://arxiv.org/abs/2502.13595](https://arxiv.org/abs/2502.13595) |
| NanoBEIR: Smaller BEIR dataset subsets | 2024 | dataset collection | [https://huggingface.co/collections/zeta-alpha-ai/nanobeir](https://huggingface.co/collections/zeta-alpha-ai/nanobeir) |
