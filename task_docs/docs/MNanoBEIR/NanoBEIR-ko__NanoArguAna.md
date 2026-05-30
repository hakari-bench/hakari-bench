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
| 대중은 개혁에 무관심하다. 현재의 경제 상황에서 상원 개혁이 최우선 과제가 되어야 하는지조차 논쟁의 여지가 있으며... | AV 캠페인을 상원 개혁과 비교할 수는 없으며, 정치적 선전으로 인해 정보를 제대로 얻지 못하는 대중을 무관심과 혼동해서는 안 된다. |
| 히드로 공항의 확장은 경제에 매우 중요하다. 히드로 공항을 확장하면 기존 일자리를 유지할 뿐 아니라 새로운 일자리도 창출할 수 있다... | 비즈니스 커뮤니티는 제3 활주로 건설에 대한 지지를 놓고 결코 단일한 입장이 아니다. |
| 사람들에게 너무 많은 선택권이 주어지는데, 이는 오히려 그들을 덜 행복하게 만든다. 광고는 사람들의 주의를 끌기 위한 끝없는 선택의 필요성 속에서 많은 이들이 압도당하게 만든다... | 사람들이 불행한 이유는 선택지가 너무 많아 스트레스를 받기 때문이 아니라, 모든 것을 가질 수 없기 때문이다. |
| 사이버 공격은 종종 실제 국가와 무관한 비국가 행위자들에 의해 수행된다. | 비국가 행위자의 공격의 경우, 다른 국가가 자국 영토 내에서 발생하는 공격에 대해 효과적인 조치를 취할 의사가 없거나 능력이 없는 상황이라면 자위권을 행사할 수 있다는 견해가 있다. |
| 종교는 믿음의 확실성을 장려하기 때문에, 신의 계시라는 이름 아래 증오를 정당화하고 폭력적 행동 및 차별적 관행을 조장하기가 용이하다. | 다른 사람의 말에 의해 폭력 행위를 강제당하는 사람은 없다. 그것은 그들 자신의 선택이다. |

### Public Sources

- [Argument Mining for Understanding Peer Reviews](https://aclanthology.org/P18-1023/).
- [BEIR: A Heterogeneous Benchmark for Zero-shot Evaluation of Information Retrieval Models](https://arxiv.org/abs/2104.08663).
- [MMTEB: Massive Multilingual Text Embedding Benchmark](https://arxiv.org/abs/2502.13595).
- [Zeta Alpha NanoBEIR collection](https://huggingface.co/collections/zeta-alpha-ai/nanobeir).
- [hakari-bench/NanoBEIR-ko](https://huggingface.co/datasets/hakari-bench/NanoBEIR-ko).

### Source Reference Table

| Title | Year | Type | URL |
| --- | ---: | --- | --- |
| Argument Mining for Understanding Peer Reviews | 2018 | task paper | https://aclanthology.org/P18-1023/ |
| BEIR: A Heterogeneous Benchmark for Zero-shot Evaluation of Information Retrieval Models | 2021 | benchmark paper | https://arxiv.org/abs/2104.08663 |
| MMTEB: Massive Multilingual Text Embedding Benchmark | 2025 | benchmark paper | https://arxiv.org/abs/2502.13595 |
| NanoBEIR: Smaller BEIR dataset subsets | 2024 | dataset collection | https://huggingface.co/collections/zeta-alpha-ai/nanobeir |
