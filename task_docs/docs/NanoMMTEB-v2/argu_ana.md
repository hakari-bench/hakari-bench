# NanoMMTEB-v2 / argu_ana

## Overview

`NanoMMTEB-v2 / argu_ana` is the ArguAna counterargument retrieval task. Each
query is a long debate argument, and the relevant document is the paired
counterargument. The Nano split has 199 queries, 8,626 documents, and 199
positive qrel rows, with exactly one positive document per query. Current
diagnostics show dense retrieval as the strongest top-rank profile,
`reranking_hybrid` as the strongest recall@100 profile, and BM25 as useful but
weaker because same-topic supporting arguments are strong lexical distractors.

## Details

### What the Original Data Measures

ArguAna was introduced for retrieval of the best counterargument without prior
topic knowledge. The task asks a system to take one argument and retrieve a
paired argument that responds against it. MTEB includes ArguAna in its English
retrieval suite, using ranking metrics such as nDCG@10.

The important distinction is that relevance is not simple topical similarity.
The positive must address the same debate issue and aspect while taking an
opposing stance. A same-topic argument that supports the query can be a hard
negative.

### Observed Data Profile

The split contains 199 queries, 8,626 documents, and 199 positive qrel rows.
Every query has exactly one positive document. Queries average 1,199.80
characters, while documents average 1,029.60 characters.

The text consists of long debate prose with topic labels, claims, warrants,
examples, and citations. Examples involve abortion policy, technological
development, vegetarianism and food safety, baseball collisions, community
radio, climate change, animal ethics, sports policy, media, and good
government.

### BM25 Evaluation Profile

The dataset-provided BM25 candidate subset contains 500 candidates per query and
achieves nDCG@10 = 0.3464, hit@10 = 0.7387, and recall@100 = 0.9548. BM25 can
find the debate topic because the query and counterargument often share issue
terms, policy names, and domain vocabulary.

Its weakness is stance and argumentative relation. Lexical overlap can retrieve
same-topic arguments that agree with the query or discuss a different aspect.
Term frequency is therefore useful for candidate generation but insufficient
for identifying the best counterargument.

### Dense Evaluation Profile

The dense `harrier_oss_v1_270m` candidate subset contains 500 candidates per
query and achieves nDCG@10 = 0.3998, hit@10 = 0.8141, and recall@100 = 0.9497.
Dense retrieval is the strongest observed top-rank profile.

This suggests that embedding similarity helps capture argument-level
relationships beyond exact word overlap. A dense model can connect related
claims, consequences, examples, and policy frames even when the counterargument
uses different wording. However, the single-positive setup still punishes
models that retrieve a plausible same-topic response that is not the annotated
pair.

### Reranking Hybrid Evaluation Profile

The `reranking_hybrid` candidate subset contains mostly 100 candidates per
query, with two queries using a rank-101 safeguard row. It achieves nDCG@10 =
0.3716, hit@10 = 0.7638, and recall@100 = 0.9899. Hybrid retrieval has the best
recall@100 but is below dense retrieval for top-rank quality.

This profile indicates that combining lexical and dense evidence is valuable
for keeping the positive in the candidate pool. The ranking itself still needs
argument-relation modeling: a reranker must distinguish counterarguments from
supporting or merely adjacent debate texts.

### Metric Interpretation for Model Researchers

This task is single-positive: each query has one annotated paired
counterargument. Hit@10 measures whether that paired document appears near the
top. nDCG@10 is sensitive to its exact rank, and recall@100 measures whether it
is available to a downstream reranker.

Because many documents can be topically plausible, false positives may look
reasonable to a generic semantic retriever. The key metric signal is whether
the model retrieves the specific opposing response, not merely an argument on
the same topic.

### Query and Relevance Type Tendencies

Queries are long English arguments with explicit claims, supporting reasons,
examples, and policy framing. They may include stance markers, topic labels,
and citations. Relevant documents are long counterarguments that share the same
issue while challenging a premise, consequence, analogy, factual assumption, or
policy recommendation.

The task rewards aspect-level matching and stance awareness. It penalizes
models that collapse all debate texts about the same topic into a single
semantic neighborhood.

### Representative Failure Modes

BM25 can retrieve a same-topic same-stance argument because it shares vocabulary
with the query. Dense retrieval can retrieve a semantically related but
non-countering document, especially when several arguments discuss the same
policy frame. Hybrid retrieval can increase candidate coverage while preserving
these same-topic distractors.

Rerankers can fail when they do not model opposition explicitly. A useful
reranker should identify what claim is being answered and whether the candidate
attacks, qualifies, or supports that claim.

### Training Data That May Help

Useful training data includes argument-counterargument pairs outside the
evaluation split, stance-labeled debate data, argument mining datasets, and
same-topic same-stance hard negatives. Training on duplicate or paraphrase
retrieval alone is not enough because the positive often disagrees with the
query.

Synthetic data can generate long argument and counterargument pairs where the
positive challenges a premise, consequence, analogy, or policy framing.
Negatives should include same-topic supporting arguments so the model learns
opposition and aspect matching. Evaluation arguments and paired positives from
this Nano split should be excluded from training.

### Model Improvement Notes

Dense retrievers should encode stance and argumentative role, not only topic.
Sparse systems can help preserve issue vocabulary but need reranking to avoid
same-stance distractors. Cross-encoders or instruction-tuned rerankers should
compare the query argument and candidate response at the claim and warrant
level.

For hybrid systems, `NanoMMTEB-v2 / argu_ana` is a good candidate-generation
test: `reranking_hybrid` gives the best recall@100, while dense retrieval gives
the best nDCG@10. The next improvement is a reranker that converts hybrid
coverage into correct counterargument ordering.

## Example Data

Representative queries argue about partial-birth abortion strategy, whether
technology can solve climate change, vegetarianism and food poisoning, whether
baseball should allow home-plate collisions, and the value of community radio.
Positive documents respond with counterarguments on the same issue.

### Public Sources

- [Retrieval of the Best Counterargument without Prior Topic Knowledge](https://aclanthology.org/P18-1023/),
  2018.
- [MTEB: Massive Text Embedding Benchmark](https://arxiv.org/abs/2210.07316),
  2023.
- [mteb/arguana](https://huggingface.co/datasets/mteb/arguana).
- [hakari-bench/NanoMMTEB-v2](https://huggingface.co/datasets/hakari-bench/NanoMMTEB-v2),
  Nano benchmark dataset.

### Source Reference Table

| Title | Year | Type | URL |
| --- | ---: | --- | --- |
| Retrieval of the Best Counterargument without Prior Topic Knowledge | 2018 | task paper | https://aclanthology.org/P18-1023/ |
| MTEB: Massive Text Embedding Benchmark | 2023 | benchmark paper | https://arxiv.org/abs/2210.07316 |
| mteb/arguana | 2024 | dataset card | https://huggingface.co/datasets/mteb/arguana |

### Representative Snippets

| Query pattern | Positive document pattern |
| --- | --- |
| An argument that partial-birth abortion bans are part of a broader anti-abortion strategy. | A counterargument separating partial-birth abortion from abortion policy in general. |
| An argument that new technology can address climate problems. | A counterargument about unequal access and climate impacts. |
| An argument that vegetarianism reduces food-poisoning risk. | A counterargument emphasizing general food safety and hygiene. |
| An argument that collisions are traditional in baseball. | A counterargument that collisions are less central than assumed. |
| An argument that community radio empowers ordinary people. | A counterargument warning that community radio can also be misused. |
