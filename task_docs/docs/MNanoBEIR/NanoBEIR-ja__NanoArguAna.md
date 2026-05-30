# MNanoBEIR / NanoBEIR-ja / NanoArguAna

## Overview

`NanoBEIR-ja__NanoArguAna` is the Japanese NanoBEIR version of ArguAna, an
argument and counterargument retrieval benchmark. The task uses Japanese
translated argumentative passages as queries and asks the retriever to find the
paired Japanese translated counterargument or closely matched argumentative
response. The Nano split contains 50 queries, 3,635 documents, and 50 positive
qrels, with exactly one positive document per query. Queries are long
argumentative passages rather than short keywords, so the task tests whether a
model can identify stance, premise, and argumentative relation across long
translated text.

## Details

### What the Original Data Measures

[ArguAna](https://aclanthology.org/P18-1023/) was introduced for argument
retrieval and argument matching in debate-style text. BEIR includes ArguAna as
an argument retrieval task in which the system must retrieve a corresponding
argumentative text rather than a factual answer passage. In this Japanese
NanoBEIR version, long translated claims and supporting paragraphs are used as
queries, and the relevant document is usually the counterargument or paired
argument that responds to the same issue. The benchmark therefore measures
argument-level semantic matching, not just topic retrieval.

### Observed Data Profile

The task has 50 queries and 3,635 documents. It contains 50 positive qrels, and
every query has exactly one positive. Query length is unusually high, averaging
553.90 characters, while documents average 458.77 characters. The examples are
full debate passages about public indifference to reform, airport expansion,
advertising and happiness, cyber attacks, and religious speech. Long inputs
provide many lexical anchors, but they also contain multiple premises and
supporting details that can distract a retriever from the actual argumentative
relation.

### BM25 Evaluation Profile

The BM25 top-500 subset reaches nDCG@10 = 0.3620, hit@10 = 0.6600, and
Recall@100 = 0.8800. Long queries give BM25 many repeated terms and topical
anchors, so lexical retrieval can often find a relevant candidate within the
top 100. The top-10 score is much weaker, however, because the correct paired
argument is not always the document with the greatest word overlap. Documents
from the same debate topic may share terms while responding to a different
premise or taking a different stance.

### Dense Evaluation Profile

The dense `harrier-oss-270m` top-500 subset reaches nDCG@10 = 0.4239, hit@10 =
0.7800, and Recall@100 = 0.9400. Dense retrieval is the strongest profile for
top-10 ranking on this task. The result indicates that embedding similarity is
better able to connect long argumentative passages by meaning, stance, and
response structure than BM25 alone. This is especially important in translated
Japanese text, where the counterargument may not reuse the same surface forms
as the query but still addresses the same proposition.

### Reranking Hybrid Evaluation Profile

The `reranking_hybrid` subset uses 100 to 101 candidates per query and reaches
nDCG@10 = 0.4022, hit@10 = 0.7600, and Recall@100 = 0.9600. Two queries use the
rank-101 safeguard. Hybrid retrieval has the best top-100 coverage, while dense
retrieval remains better on nDCG@10 and hit@10. This means that combining
lexical and dense search is useful for keeping the single positive in the
candidate set, but the fused order can still rank topical lexical matches above
the best semantic counterargument.

### Metric Interpretation for Model Researchers

This task separates candidate coverage from argumentative ranking. BM25 is not
enough for early precision, even with long text, because word overlap often
tracks topic more than argumentative relation. Dense retrieval is the best
single profile for ranking the positive near the top, suggesting that semantic
representations are essential for counterargument matching. Hybrid retrieval is
best for Recall@100 and is therefore attractive for reranking pipelines. A
strong model should improve dense-like top-rank behavior while preserving the
hybrid candidate coverage.

### Query and Relevance Type Tendencies

The examples involve long policy or social debate passages. The positive
document often challenges a premise, presents a counterexample, or reframes the
claim. Relevance depends on whether the document responds to the same argument,
not simply whether it discusses the same topic. This makes stance, premise
tracking, and discourse relation important features for model analysis.

### Representative Failure Modes

BM25 can retrieve documents that share issue words such as reform, airport
expansion, advertising, cyber attacks, or religion but do not answer the query's
specific claim. Dense retrieval can retrieve semantically related debate text
that is on-topic but not the paired counterargument. Hybrid retrieval can
increase coverage while still placing broad topic matches above the exact
argument pair. Single-positive evaluation makes these rank-order errors costly.

### Training Data That May Help

Useful training data includes non-overlapping argument retrieval,
counterargument pairs, stance-aware retrieval, Japanese debate text, and
multilingual argument mining data. Hard negatives should address the same topic
while responding to a different premise or stance. Training should exclude
ArguAna, BEIR, NanoBEIR, and translated argument records likely to overlap with
this benchmark.

### Model Improvement Notes

Strong systems should encode long argumentative passages without collapsing them
into coarse topic vectors. Useful improvements include stance-aware contrastive
training, hard negatives from the same debate topic, and reranking features that
compare the claim, premise, and response relation. Candidate generation should
retain lexical coverage, but final ranking needs argument-structure awareness.

## Example Data

| Query | Positive document |
| --- | --- |
| 一般大衆は改革に対して無関心である。現在の経済情勢において上院の改革が最優先事項であるべきかどうかは議論の余地がある... | AVキャンペーンを貴族院の改革と比較することはできない。さらに、政治的プロパガンダによって誤解している有権者を、無関心と混同してはならない... |
| ヒースロー空港の拡張は経済にとって極めて重要である。ヒースローの拡張により、現在の多くの雇用が守られる... | ビジネス界は、第3滑走路建設への支持に関して決して一致しているわけではない。調査によれば、多くの有力企業が実際には拡張に賛成していない... |
| 人々にはあまりにも多くの選択肢が与えられており、それによって幸福度が低下している。広告は人々の注意を引きつけようとする... | 人々が不満を感じているのは、すべてを持てないからであって、選択肢が多すぎてストレスを感じるからではない... |
| サイバー攻撃は、国家に属さない行為者、例えばサイバーテロリストやハクティビストによって、国家の関与なしに行われることが多い... | 非国家主体による攻撃の場合、国際法の多くの専門家は、他国が自国内から発生する攻撃に対処するために「効果的な措置を講じる意思がない、または能力がない」... |
| 宗教は信念の確実性を促進するため、神の啓示による憎悪を暴力行為や差別的慣行を正当化し推進するため... | 誰も他人の言葉によって暴力行為を強制されているわけではない。それはあくまで本人の選択である。同様に、同性愛に対して否定的な見解を持っているが... |

### Public Sources

- [Argument Mining for Understanding Peer Reviews](https://aclanthology.org/P18-1023/).
- [BEIR: A Heterogeneous Benchmark for Zero-shot Evaluation of Information Retrieval Models](https://arxiv.org/abs/2104.08663).
- [MMTEB: Massive Multilingual Text Embedding Benchmark](https://arxiv.org/abs/2502.13595).
- [Zeta Alpha NanoBEIR collection](https://huggingface.co/collections/zeta-alpha-ai/nanobeir).
- [hakari-bench/NanoBEIR-ja](https://huggingface.co/datasets/hakari-bench/NanoBEIR-ja).

### Source Reference Table

| Title | Year | Type | URL |
| --- | ---: | --- | --- |
| Argument Mining for Understanding Peer Reviews | 2018 | task paper | https://aclanthology.org/P18-1023/ |
| BEIR: A Heterogeneous Benchmark for Zero-shot Evaluation of Information Retrieval Models | 2021 | benchmark paper | https://arxiv.org/abs/2104.08663 |
| MMTEB: Massive Multilingual Text Embedding Benchmark | 2025 | benchmark paper | https://arxiv.org/abs/2502.13595 |
| NanoBEIR: Smaller BEIR dataset subsets | 2024 | dataset collection | https://huggingface.co/collections/zeta-alpha-ai/nanobeir |
