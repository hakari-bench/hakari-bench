# MNanoBEIR / NanoBEIR-ko / NanoArguAna

## Overview

`NanoBEIR-ko__NanoArguAna` is the Korean NanoBEIR version of ArguAna, an
argument and counterargument retrieval benchmark. The task uses Korean
translated argumentative passages as queries and asks a retriever to find the
paired Korean translated counterargument or closely matched argumentative
response. The Nano split contains 50 queries, 3,635 documents, and 50 positive
qrels, with exactly one positive document per query. Queries and documents are
both long compared with ordinary search tasks, so the benchmark tests whether a
model can match stance, premise, and argumentative relation rather than only
topic words.

## Details

### What the Original Data Measures

[ArguAna](https://aclanthology.org/P18-1023/) was introduced for argument
retrieval and matching in debate-style text. BEIR includes ArguAna as an
argument retrieval task where the relevant document is not a factual answer but
an argumentative counterpart. In this Korean NanoBEIR version, long translated
claims and supporting passages are used as queries, and the positive document
usually responds to the same issue with a counterargument or closely paired
argument. This makes relevance discourse-oriented and stance-aware.

### Observed Data Profile

The task has 50 queries and 3,635 documents. It contains 50 positive qrels, and
every query has exactly one positive. Queries average 619.40 characters, while
documents average 519.64 characters. The examples discuss public indifference
to reform, Heathrow expansion, choice overload, cyber attacks, and religious
speech. These long passages include several claims and supporting details,
which gives lexical retrieval many anchors but also creates many same-topic
distractors.

### BM25 Evaluation Profile

The BM25 top-500 subset reaches nDCG@10 = 0.3661, hit@10 = 0.6600, and
Recall@100 = 0.9000. BM25 is reasonably strong for candidate recall because
long argumentative passages repeat topic terms and policy vocabulary. However,
its top-10 ranking is limited. The correct paired counterargument is often not
the passage with the highest surface overlap; it is the one that responds to
the same premise or challenges the same claim. Topic-level lexical matching
therefore leaves many hard negatives near the top.

### Dense Evaluation Profile

The dense `harrier-oss-270m` top-500 subset reaches nDCG@10 = 0.4082, hit@10 =
0.6800, and Recall@100 = 0.9400. Dense retrieval improves over BM25 on all
reported metrics, which indicates that semantic representations help connect
argumentative passages by meaning and response relation. Dense retrieval is
better at capturing paraphrased premises and stance-level similarity, but it
still does not fully solve the single-positive ranking problem.

### Reranking Hybrid Evaluation Profile

The `reranking_hybrid` subset uses 100 to 101 candidates per query and reaches
nDCG@10 = 0.4217, hit@10 = 0.7800, and Recall@100 = 0.9600. Two queries use the
rank-101 safeguard. Hybrid retrieval is the strongest profile across all three
metrics. This shows that lexical and dense signals are complementary for Korean
ArguAna: BM25 preserves topic and phrase anchors, while dense retrieval adds
semantic and argumentative relatedness. The combined candidate set is both
broader and better ranked than either single retrieval family.

### Metric Interpretation for Model Researchers

This task is a clear hybrid-strength case. BM25 alone has good top-100 recall
but weak early precision, dense retrieval improves semantic ranking, and
`reranking_hybrid` gives the best top-10 and top-100 behavior. Researchers
should interpret improvements as evidence of argument-level matching, not just
long-text similarity. Because every query has one positive, a model must
separate the exact paired response from many same-topic argument passages.

### Query and Relevance Type Tendencies

The examples are long debate passages where the positive document challenges,
qualifies, or reframes the query's claim. The relationship can involve
counterevidence, a distinction between public opinion and misinformation, an
alternative economic analysis, or a legal principle. Relevance depends on
responding to the same argument structure, not merely discussing the same
topic.

### Representative Failure Modes

BM25 can retrieve passages that share issue words but respond to a different
premise. Dense retrieval can retrieve semantically related debate text that is
not the paired counterargument. Hybrid retrieval can still fail when both
signals favor broad same-topic documents. Long Korean translated passages also
increase the chance that one paragraph overlaps strongly while the overall
argument relation is wrong.

### Training Data That May Help

Useful training data includes non-overlapping argument retrieval, debate
counterargument pairs, stance-aware retrieval, Korean argument mining, and
multilingual debate-pair data. Hard negatives should address the same topic
while taking a different stance or responding to a different premise. Training
should exclude ArguAna, BEIR, NanoBEIR, and translated argument records likely
to overlap with this benchmark.

### Model Improvement Notes

Strong systems should encode long argument passages without reducing them to
topic vectors. Useful directions include stance-aware contrastive learning,
premise-response hard negatives, and reranking signals that compare the main
claim, evidence, and counterclaim. Hybrid candidate generation is especially
appropriate because both lexical anchors and semantic argument structure matter.

## Example Data

| Query | Positive document |
| --- | --- |
| 대중은 개혁에 무관심하다. 현재의 경제 상황에서 상원 개혁이 최우선 과제가 되어야 하는지조차 논쟁의 여지가 있으며, 게다가 연립 정부가 그러한 조치를 시작하고 관철시킬 수 있을지조차 미지수이다. 상원 개혁을 시도하려는 노력은 수차례에 걸쳐 지연되어 왔으며, 이는 하원이 변화에 대해 보류하고 있는 태도를 보여준다.[1] 최근 대체 투표제 찬반 국민투표의 결과에서 드러났듯이, 이러한 분위기는 영국 대중의 여론에서도 분명히 공감되고 있다. 즉 대중은 변화에 대해 부정적인 태도를 보이거나 아니면 무관심한 상태이다.[2] [1] Summers, Deborah, 『Labour's attempts to reform the House of Lords』, The Guardian (2009년 1월 27일), 2011년 6월 1일 열람 [2] BBC News, 『Vote 2011: UK rejects alternative vote』, 2011년 5월 7일 [473 chars] | AV 캠페인을 상원 개혁과 비교할 수는 없으며, 정치적 선전으로 인해 정보를 제대로 얻지 못하는 대중을 무관심과 혼동해서는 안 된다. 유권자들은 종종 자신들이 아무것도 바꿀 수 없고 자신의 투표가 의미가 없다고 느끼기 때문에 무관심을 표현한다. 국민이 직접 선출한 인물들이 나라를 운영하도록 보장하는 개혁은 이러한 감정을 해소하는 데 도움이 될 것이다. [197 chars] |
| 히드로 공항의 확장은 경제에 매우 중요하다. 히드로 공항을 확장하면 기존 일자리를 유지할 뿐 아니라 새로운 일자리도 창출할 수 있다. 현재 히드로 공항은 약 25만 개의 일자리를 뒷받침하고 있다.[1] 여기에 더해 수십만 명이 런던의 관광 산업에 의존하고 있는데, 이 산업은 히드로와 같은 우수한 교통망에 크게 의존하고 있다. 다른 유럽 공항들에 비해 경쟁력을 잃는 것은 단지 새로운 일자리 창출의 기회를 놓치는 것을 넘어 기존 일자리마저 잃을 수 있음을 의미한다. 히드로 공항의 확장은 경기 침체로 인해 영국의 인프라 지출이 매우 낮은 시기에 중요한 인프라를 구축함으로써 성장을 촉진하는 데도 기여할 것이다. 우수한 항공 연결망은 새로운 기업 유치와 기존 기업 유지에 필수적이다. 이는 항공 인프라가 새로운 비즈니스 기회를 발굴하는 데 중요하기 때문이다. 영국의 경제적 미래는 유럽과 미국 같은 전통적인 거래 지역뿐 아니라 충칭과 청두 같은 중국과 인도의 성장하는 도시들과의 무역에 달려 있다... [500 / 725 chars] | 비즈니스 커뮤니티는 제3 활주로 건설에 대한 지지를 놓고 결코 단일한 입장이 아니다. 여론 조사에 따르면 실제로 영향력 있는 다수의 기업들이 확장을 지지하지 않는 것으로 나타났다. 저스틴 킹 J 세인스버리 최고경영자와 BskyB의 제임스 머독이 서명한 서한은 이에 대한 우려를 표명했다.[1] 따라서 비즈니스 커뮤니티를 확장 촉구의 단일한 목소리로 간주하는 것은 오해이다. 히스로 공항의 새로운 활주로 외의 대안들, 즉 다른 런던 공항에 새로운 활주로를 건설하거나 완전히 새로운 공항을 만드는 방안을 고려할 때, 이러한 대안들도 히스로 확장과 유사한 경제적 영향을 미칠 가능성이 있음을 기억해야 한다. 비즈니스와 관광객 유치에 중요한 것이 연결성이라면, 그 연결이 런던과 이루어진다면 어느 공항에서 이루어지든 상관없다. 런던에 대한 이익에 초점을 맞춘다면, 공항이 허브 공항일 필요조차 줄어들 수 있는데, 전 브리티시에어웨이스 최고경영자인 밥 에일링은 히스로 공항이 단순한 환승지점이 아니라 런던을 방문하려는 승객에 집중해야 한다고 말하며, 제3 활주로는 "비용이 많이 드는 실수"가 될 수 있다고 지적했다.[2] [1] 오스본, 알리스터, '킹피셔 최고경영자 이안 체셔, 히스로 활주로 성공성에 의문 제기', 더 텔레그래프, 2009년 7월 13일, [2] 스튜어트, 존, '히캔(HACAN)이 제공한 히스로 공항 브리핑: 2012년 6월' [699 chars] |
| 사람들에게 너무 많은 선택권이 주어지는데, 이는 오히려 그들을 덜 행복하게 만든다. 광고는 사람들의 주의를 끌기 위한 끝없는 선택의 필요성 속에서 많은 이들이 압도당하게 만드는데, 이를 '선택의 폭정' 또는 '선택 과부하'라고 한다. 최근의 연구에 따르면, 사람들은 30년 전보다 더 나은 삶을 살고 있으며 돈을 쓸 수 있는 선택지도 훨씬 많음에도 불구하고 평균적으로 더 불행해졌다는 것이다1. 광고의 주장들이 사람들을 압박하며 제품에 대한 기대를 높이다 보니, 제품을 구입한 후에는 필연적으로 실망하게 된다. 최근 영국에서는 한 화장품 광고가 제품의 효과를 실제보다 더 좋게 제시했다는 이유로 금지되었다2. 소비자들은 잘못된 구매를 자신이 더 현명하게 선택하지 못한 탓이라고 느끼며, 다른 것을 선택하지 않은 것을 후회한다. 어떤 사람들은 너무 압도되어 아예 선택조차 하지 못하기도 한다. 1 슈와르츠, 『선택의 폭정』, 2004. 2 키크, 『너무 아름다운가? 영국 국회의원, 화장품 광고에... [500 / 518 chars] | 사람들이 불행한 이유는 선택지가 너무 많아 스트레스를 받기 때문이 아니라, 모든 것을 가질 수 없기 때문이다. 실제로 광고는 사람들이 가진 돈을 자신에게 가장 적합한 제품에 쓸 수 있도록 보장하는 중요한 역할을 한다. 광고가 허용되지 않는다면, 사람들은 선택의 기회가 주어졌을 때 분명히 다른 제품을 선택할 텐데도 불구하고, 처음 접한 제품에 돈을 낭비하게 될 것이다. 50개의 독립적인 연구를 포함한 메타 분석에서는 선택과 불안 사이에 의미 있는 연결 고리는 발견되지 않았지만, 연구들 간의 차이로 인해 선택 과부하가 특정한 매우 제한된 조건과 연결될 가능성은 여전히 열려 있다고 추측했다1. 1 ^ Scheibehenne, Benjamin; Greifeneder, R. & Todd, P. M. (2010). "Can There Ever be Too Many Options? A Meta-Analytic Review of Choice Overload". Journal of Consumer Research 37: 409-425. [523 chars] |

### Public Sources

- [Argument Mining for Understanding Peer Reviews](https://aclanthology.org/P18-1023/).
- [BEIR: A Heterogeneous Benchmark for Zero-shot Evaluation of Information Retrieval Models](https://arxiv.org/abs/2104.08663).
- [MMTEB: Massive Multilingual Text Embedding Benchmark](https://arxiv.org/abs/2502.13595).
- [Zeta Alpha NanoBEIR collection](https://huggingface.co/collections/zeta-alpha-ai/nanobeir).
- [hakari-bench/NanoBEIR-ko](https://huggingface.co/datasets/hakari-bench/NanoBEIR-ko).

### Source Reference Table

| Title | Year | Type | URL |
| --- | ---: | --- | --- |
| Argument Mining for Understanding Peer Reviews | 2018 | task paper | [https://aclanthology.org/P18-1023/](https://aclanthology.org/P18-1023/) |
| BEIR: A Heterogeneous Benchmark for Zero-shot Evaluation of Information Retrieval Models | 2021 | benchmark paper | [https://arxiv.org/abs/2104.08663](https://arxiv.org/abs/2104.08663) |
| MMTEB: Massive Multilingual Text Embedding Benchmark | 2025 | benchmark paper | [https://arxiv.org/abs/2502.13595](https://arxiv.org/abs/2502.13595) |
| NanoBEIR: Smaller BEIR dataset subsets | 2024 | dataset collection | [https://huggingface.co/collections/zeta-alpha-ai/nanobeir](https://huggingface.co/collections/zeta-alpha-ai/nanobeir) |
