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
| 대중은 개혁에 무관심하다. 현재의 경제 상황에서 상원 개혁이 최우선 과제가 되어야 하는지조차 논쟁의 여지가 있으며, 게다가 연립 정부가 그러한 조치를 시작하고 관철시킬 수 있을지조... [100 / 473 chars] | AV 캠페인을 상원 개혁과 비교할 수는 없으며, 정치적 선전으로 인해 정보를 제대로 얻지 못하는 대중을 무관심과 혼동해서는 안 된다. 유권자들은 종종 자신들이 아무것도 바꿀 수 없고 자신의 투표가 의미가 없다고 느끼기 때문에 무관심을 표현한다. 국민이 직접 선출한 인물들이 나라를 운영하도록 보장하는 개혁은 이러한 감정을 해소하는 데 도움이 될 것이다. [197 chars] |
| 히드로 공항의 확장은 경제에 매우 중요하다. 히드로 공항을 확장하면 기존 일자리를 유지할 뿐 아니라 새로운 일자리도 창출할 수 있다. 현재 히드로 공항은 약 25만 개의 일자리를... [100 / 725 chars] | 비즈니스 커뮤니티는 제3 활주로 건설에 대한 지지를 놓고 결코 단일한 입장이 아니다. 여론 조사에 따르면 실제로 영향력 있는 다수의 기업들이 확장을 지지하지 않는 것으로 나타났다. 저스틴 킹 J 세인스버리 최고경영자와 BskyB의 제임스 머독이 서명한 서한은 이에 대한 우려를 표명했다.[1] 따라서 비즈니스 커뮤니티를 확장 촉구의 단일한 목소리로 간주하는... [200 / 699 chars] |
| 사람들에게 너무 많은 선택권이 주어지는데, 이는 오히려 그들을 덜 행복하게 만든다. 광고는 사람들의 주의를 끌기 위한 끝없는 선택의 필요성 속에서 많은 이들이 압도당하게 만드는데,... [100 / 518 chars] | 사람들이 불행한 이유는 선택지가 너무 많아 스트레스를 받기 때문이 아니라, 모든 것을 가질 수 없기 때문이다. 실제로 광고는 사람들이 가진 돈을 자신에게 가장 적합한 제품에 쓸 수 있도록 보장하는 중요한 역할을 한다. 광고가 허용되지 않는다면, 사람들은 선택의 기회가 주어졌을 때 분명히 다른 제품을 선택할 텐데도 불구하고, 처음 접한 제품에 돈을 낭비하게... [200 / 523 chars] |
| 사이버 공격은 종종 실제 국가와 무관한 비국가 행위자들, 예를 들어 사이버테러리스트나 해커 활동가(사회 운동을 위해 해킹을 하는 자)에 의해 수행된다. 예를 들어, 2007년 에스... [100 / 513 chars] | 비국가 행위자의 공격의 경우, 국제법 분야의 많은 전문가들은 다른 국가가 자국 영토 내에서 발생하는 공격에 대해 '효과적인 조치를 취할 의사가 없거나 능력이 없는' 상황이라면, 해당 국가가 여전히 자위권을 행사해 응징할 수 있다는 데 동의한다[19]. 이는 전통적 전쟁에 적용되며, 사이버전에도 동일하게 적용될 수 있다. 만약 어떤 국가가 사이버 보안을 확보... [200 / 294 chars] |
| 종교는 믿음의 확실성을 장려하기 때문에, 신의 계시라는 이름 아래 증오를 정당화하고 폭력적 행동 및 차별적 관행을 조장하기가 용이하다. 표현의 자유는 그 발언이 해를 끼칠 가능성이... [100 / 790 chars] | 다른 사람의 말에 의해 폭력 행위를 강제당하는 사람은 없다. 그것은 그들 자신의 선택이다. 마찬가지로, 동성애 혐오적 시각을 가질 수 있는 많은 사람들이 실제로는 폭력 행위에 대해 경악할 것이다. 타인의 행동에 대해 내가 책임을 지지 않는 것은 개인에 대한 존중의 원칙에서 근본적인 것이다. 내가 돈이 없는 친구에게 농담 반담으로 은행을 털라고 제안하는 것과... [200 / 303 chars] |

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
