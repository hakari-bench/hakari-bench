# NanoMTEB-v2 / argu_ana

## Overview

`NanoMTEB-v2 / argu_ana` is the ArguAna counterargument retrieval task. Each query is a long debate argument, and the relevant document is the paired counterargument. The original ArguAna paper frames this as retrieval of the best opposing argument without prior topic knowledge: the model must find text that addresses the same issue but takes the opposite argumentative stance. This makes the task different from ordinary semantic similarity. A passage that agrees with the query, paraphrases it, or discusses the same topic may be a hard negative rather than a positive. The Nano split keeps 199 single-positive queries over 8,626 candidate arguments.

## Details

### What the Original Data Measures

ArguAna measures counterargument retrieval. The relevant document should oppose the query's claim or reasoning while engaging with similar aspects of the debate. It is not enough to retrieve a topically similar argument. The target document should be useful as a response in an argumentative setting.

MTEB includes ArguAna as an English retrieval task and evaluates it primarily with nDCG@10. In this Nano version, the query and document texts remain long-form English debate prose, often with topic labels, claims, supporting examples, and policy or ethical framing.

### Observed Data Profile

The Nano split contains 199 queries, 8,626 documents, and 199 positive qrel rows. Each query has exactly one positive. Queries average 1,199.80 characters, and documents average 1,029.60 characters. The long query and document lengths make this a meaning-heavy task rather than a short keyword lookup.

The examples cover abortion policy, climate technology, vegetarianism, baseball collisions, and community radio. Positive documents are not duplicates of the query. They often share topic vocabulary but reverse the stance, attack a premise, or challenge the claimed consequence.

### BM25 Evaluation Profile

The BM25 candidate subset uses top-500 candidates and reaches nDCG@10 of 0.3464, hit@10 of 0.7387, and recall@100 of 0.9548. BM25 is useful because debate pairs often share topic words, named concepts, and policy terms. However, lexical overlap does not indicate whether the document is a counterargument.

This task exposes a key sparse-retrieval limitation: same-topic same-stance arguments can look excellent lexically while being the wrong kind of match. BM25 can find the topic neighborhood, but it has weak access to argumentative polarity and response quality.

### Dense Evaluation Profile

The dense candidate subset from `harrier_oss_v1_270m` uses top-500 candidates and reaches nDCG@10 of 0.4092, hit@10 of 0.8342, and recall@100 of 0.9598. Dense retrieval is the strongest standalone candidate source. Its advantage suggests that embedding similarity captures more than word overlap: it can better connect two long arguments that discuss the same issue with a contrasting stance.

The task is still challenging for dense retrieval because semantic closeness and stance opposition are in tension. A model trained only to place semantically similar texts together may over-rank supporting arguments. The best dense models need representations that preserve topic, aspect, and stance relation rather than collapsing all same-topic texts together.

### Reranking Hybrid Evaluation Profile

The `reranking_hybrid` subset uses top-100 candidates, with two queries carrying a rank-101 safeguard positive. It reaches nDCG@10 of 0.3775, hit@10 of 0.7739, and recall@100 of 0.9899. The hybrid pool provides the best recall@100, but its top-rank quality is below dense retrieval.

This pattern is useful for reranking experiments. Sparse and dense retrieval together expose almost all positives to the reranker, while the top of the hybrid list still contains many plausible same-topic negatives. A reranker can add value if it learns that the positive must counter the query rather than support it.

### Metric Interpretation for Model Researchers

nDCG@10 should be read as counterargument ranking quality, not general topical retrieval quality. A high hit@10 score means the system often finds the paired counterargument somewhere near the top, but the single-positive setup makes exact top-rank placement difficult.

Recall@100 is high for all candidate sources, especially hybrid, so candidate generation is not the only bottleneck. The main challenge is rank ordering among same-topic arguments with different stance relations.

### Query and Relevance Type Tendencies

Queries are long, self-contained arguments. Relevant documents are long counterarguments from the same or related debate topic. Many texts contain explicit claims, warrants, examples, policy consequences, and ethical positions.

The relevance relation is stance-sensitive. A relevant document should be an opposing response, not merely an adjacent argument on the same subject.

### Representative Failure Modes

Common failures include retrieving supporting arguments, retrieving a same-topic document that addresses a different aspect, ranking a generic debate introduction above the paired counterargument, and mistaking shared topic vocabulary for relevance. Dense systems may also over-rank semantically close paraphrases that do not oppose the query.

### Training Data That May Help

Useful training data includes non-overlapping argument-counterargument pairs, pro/con debate corpora, stance-labeled argument pairs, and hard negatives from same-topic same-stance arguments. Evaluation queries, qrels, and positive documents from this split should be excluded from training.

### Model Improvement Notes

Models should represent argumentative role as well as topic. Contrastive training should include same-topic supporting arguments as hard negatives and counterarguments that attack different aspects as graded or difficult cases. Rerankers may benefit from explicit signals for claim, premise, stance, and rebuttal relation.

## Example Data

### Public Sources

- [Retrieval of the Best Counterargument without Prior Topic Knowledge](https://aclanthology.org/P18-1023/), 2018.
- [MTEB: Massive Text Embedding Benchmark](https://arxiv.org/abs/2210.07316), 2023.
- [mteb/arguana](https://huggingface.co/datasets/mteb/arguana), source dataset card.

### Source Reference Table

| Title | Year | Type | URL |
| --- | ---: | --- | --- |
| Retrieval of the Best Counterargument without Prior Topic Knowledge | 2018 | source task paper | https://aclanthology.org/P18-1023/ |
| MTEB: Massive Text Embedding Benchmark | 2023 | benchmark paper | https://arxiv.org/abs/2210.07316 |
| mteb/arguana |  | dataset card | https://huggingface.co/datasets/mteb/arguana |

### Representative Snippets

| Query | Relevant document excerpt |
| --- | --- |
| An argument claiming opposition to partial-birth abortion is part of a broader strategy to ban abortion in general. | A counterargument stating that opposition to partial-birth abortion does not necessarily imply opposition to all abortion. |
| An argument that new technology has repeatedly transformed human life and may address major future problems. | A counterargument about climate change, unequal access to technology, and harms to people least able to afford solutions. |
| An argument that vegetarianism reduces food-poisoning risks because dangerous food poisoning often comes from meat or eggs. | A counterargument emphasizing food safety and hygiene standards rather than treating vegetarianism as the only solution. |
| An argument that collisions are part of baseball tradition and expected by fans and players. | A counterargument claiming collisions are less central to baseball than commonly believed and should not be preserved simply as tradition. |
| An argument that community radio gives ordinary people a voice against powerful institutions. | A counterargument warning that community radio can also be misused or fail to produce the claimed democratic benefits. |
