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
| Ly49Q는 막 래프트 기능을 조절함으로써 호중구 이동을 염증 부위로 조직하는 것을 조절한다. [52 chars] | 호중구는 감염 및 염증 부위로 신속하게 침윤하기 위해 빠르게 극성화되고 방향성 있는 운동을 한다. 본 연구에서 우리는 억제성 MHC I 수용체인 Ly49Q가 호중구의 신속한 극성화와 조직 침윤에 핵심적인 역할을 한다는 것을 보였다. 정상 상태에서 Ly49Q는 Src 및 PI3 키나제를 억제함으로써 초점 복합체 형성을 방지하여 호중구의 부착을 억제하였다. 그러나 염증 자극이 존재할 경우, Ly49Q는 ITIM 도메인 의존적인 방식으로 호중구의 신속한 극성화와 조직 침윤을 매개하였다. 이러한 상반된 기능은 효과기 인산가수분해효소인 SHP-1과 SHP-2의 서로 다른 사용에 의해 매개되는 것으로 보인다. Ly49Q 의존적인 극성화와 이동은 Ly49Q가 막 뗏목 기능을 조절함으로써 영향을 받았다. 우리는 Ly49Q가 막 뗏목과 뗏목 관련 신호 분자의 공간-시간적 조절을 통해 염증 발생 시 호중구를 극성화된 형태와 신속한 이동 상태로 전환하는 데 핵심적인 역할을 한다고 제안한다. [493 chars] |
| 항레트로바이러스 요법은 다양한 CD4 계층에서 결핵 발생률을 감소시킨다. [40 chars] | 배경 인간면역결핍바이러스(HIV) 감염은 결핵 발생의 가장 강력한 위험요인이며, 특히 사하라 이남 아프리카 지역에서 결핵의 재확산을 촉진시켰다. 2010년 전 세계적으로 HIV에 감염된 약 3,400만 명 중 결핵 신규 발생 건수는 약 110만 건으로 추정되었다. 항레트로바이러스 요법은 HIV 관련 결핵 예방에 상당한 가능성을 지닌다. 본 연구는 성인 HIV 감염자에서 항레트로바이러스 요법이 결핵 발생률에 미치는 영향을 분석한 연구들을 체계적으로 검토하였다. 방법 및 결과 PubMed, Embase, African Index Medicus, LILACS 및 임상시험 등록기관을 체계적으로 검색하였다. 무작위 대조시험, 전향적 코호트 연구, 후향적 코호트 연구 중 개발도상국에서 HIV 감염 성인을 대상으로 항레트로바이러스 요법의 유무에 따라 결핵 발생률을 비교하고 중앙값이 6개월을 초과하는 연구를 포함시켰다. 메타분석을 위해 항레트로바이러스 요법 시작 시의 CD4 수치에 따라 네 가지 범주를 설정하였다: (1) 200세포/µl 미만, (2) 200~350세포/µl, (3) 350세포/µl 초과, (4) 모든 CD4 수치. 11건의 연구가 포함 기준을 충족하였다. 항레트로바이러스 요법은 기저 CD4 수치 범주에 관계없이 결핵 발생률 감소와 강하게 연관되어 있었다: (1) 200세포/µl 미만(HR 0.16, 95% 신뢰구간[CI] 0.07~0.36), (2) 200~350세포/µl(HR 0.34, 95% CI 0.19~0.60), (3) 350세포/µl 초과(HR 0.43, 95% CI 0.30~0.63), (4) 모든 CD4 수치(HR 0.35, 95% CI 0.28~0.44). 기저 CD4 수치 범주에 따른 위험도 비율(HR)의 차이를 보여주는 증거는 없었다(p = 0.20). 결론 항레트로바이러스 요법은 모든 CD4 수치 범주에서 결핵 발생률 감소와 강하게 연관되어 있다. 항레트로바이러스 요법의 조기 시작은 전 세계 및 국가 차원에서 HIV 관련 결핵의 공중보... [1,000 / 1,116 chars] |
| 인터페론 유도 유전자의 급속한 상향 조절과 더 높은 기초 발현은 서부 나이로바 바이러스에 감염된 소뇌 과립세포 뉴런의 생존을 감소시킨다. [76 chars] | 뇌의 뉴런이 미생물 감염에 취약한 정도는 임상적 결과를 결정하는 주요 요인이지만, 이러한 취약성을 조절하는 분자적 요인들에 대해서는 거의 알려져 있지 않다. 본 연구에서 우리는 서로 다른 뇌 영역에 위치한 두 가지 유형의 뉴런이 여러 양성 가닥 RNA 바이러스의 복제에 대해 상이한 허용성을 나타냄을 보였다. 소뇌의 과립세포 뉴런과 대뇌피질의 피질 뉴런은 독특한 선천 면역 프로그램을 가지며, 이는 생체 외 및 생체 내에서 바이러스 감염에 대한 상이한 감수성을 부여한다. 과립세포 뉴런에서 더 높게 발현되는 유전자들을 피질 뉴런에 도입함으로써, 다양한 신경성 바이러스에 대한 항바이러스 효과를 매개하는 세 가지 인터페론 자극 유전자(ISG; Ifi27, Irg1 및 Rsad2(또는 Viperin))를 확인하였다. 또한, ISG의 에피제네틱 상태와 마이크로RNA(miRNA) 매개 조절이 과립세포 뉴런에서 강화된 항바이러스 반응과 관련되어 있음을 발견하였다. 따라서 진화적으로 상이한 뇌 영역의 뉴런들은 고유한 선천 면역 서명을 가지며, 이는 감염에 대한 상대적 허용성에 기여할 가능성이 있다. [556 chars] |

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
