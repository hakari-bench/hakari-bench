# NanoMMTEB-v2 / hagrid

## Overview

`NanoMMTEB-v2 / hagrid` is an English information-seeking retrieval task from
HAGRID. Queries are short fact-seeking questions, and documents are concise
answer passages with citation-style markers. The Nano split has 200 queries,
493 documents, and 200 positive qrel rows, with exactly one positive document
per query. Current diagnostics show all retrieval profiles as very strong, with
BM25 best on nDCG@10 and hit@10, `reranking_hybrid` best on recall@100, and
dense retrieval close behind. The task is mostly about exact attributable
evidence selection among compact factual snippets.

## Details

### What the Original Data Measures

HAGRID is a human-LLM collaborative dataset for generative information seeking
with attribution. It builds on information-seeking questions and relevant
passages, then adds generated answers and human judgments of informativeness
and attribution. In this retrieval version, systems retrieve passages that can
support a cited answer.

The task measures whether a retriever can find direct factual evidence for a
question. The positive passage should explicitly support the answer, not merely
mention the same entity.

### Observed Data Profile

The Nano split contains 200 queries, 493 documents, and 200 positive qrel rows.
Every query has exactly one positive document. Queries average 38.36
characters, while documents average 229.57 characters.

Queries are short English fact questions. Documents are compact answer snippets,
often with citation markers such as bracketed source numbers. Examples ask
about the Australian Football League, Nausicaa of the Valley of the Wind, Abi
Branning, Loretta Lynn, and the Cincinnati Bengals.

### BM25 Evaluation Profile

The dataset-provided BM25 candidate subset contains all 493 documents per query
and achieves nDCG@10 = 0.9814, hit@10 = 0.9950, and recall@100 = 0.9950. BM25
is the strongest top-rank profile.

This reflects the factual QA nature of the task. Queries and positive passages
often share core entity names and answer attributes. Exact lexical matching is
therefore highly effective, and the remaining challenge is distinguishing
near-duplicate snippets about the same entity or adjacent fact.

### Dense Evaluation Profile

The dense `harrier_oss_v1_270m` candidate subset contains all 493 documents per
query and achieves nDCG@10 = 0.9570, hit@10 = 0.9650, and recall@100 = 0.9800.
Dense retrieval is also very strong, but slightly below BM25.

Dense similarity helps match question intent and paraphrased evidence, but it
can blur closely related facts. For example, passages about the same person,
team, film, or television character may be semantically close while only one
contains the requested answer.

### Reranking Hybrid Evaluation Profile

The `reranking_hybrid` candidate subset contains 100 candidates per query and
achieves nDCG@10 = 0.9639, hit@10 = 0.9800, and recall@100 = 1.0000. Hybrid
retrieval has perfect recall@100 and sits between BM25 and dense retrieval for
top-rank quality.

The profile suggests that hybrid retrieval is an excellent candidate generator:
it keeps every positive available for reranking. However, BM25 alone remains
the best observed final ranker because exact entity and attribute overlap is so
strong.

### Metric Interpretation for Model Researchers

This task is single-positive: each question has one annotated supporting
passage. Hit@10 measures whether that passage appears near the top. nDCG@10 is
sensitive to its exact rank, and recall@100 measures whether it remains
available to a reranker.

Because the corpus is small and the passages are short, high scores should be
expected from competent lexical and dense retrievers. The most useful signal is
whether a model can avoid confusing same-entity passages that answer different
attributes.

### Query and Relevance Type Tendencies

Queries are short English questions about entities, dates, counts, places,
adaptations, status, or biographical facts. Relevant documents are concise
answer passages that explicitly state the requested fact and often include
citation-like markers.

The task rewards entity recognition, attribute matching, and exact answer
support. It does not require long-context retrieval, but it does require
distinguishing the cited supporting snippet from nearby factual snippets.

### Representative Failure Modes

BM25 can fail when several snippets repeat the same entity name but answer
different questions. Dense retrieval can fail by selecting a semantically
related snippet about the same entity without the requested attribute. Hybrid
retrieval can preserve the correct passage in the candidate pool while ranking a
nearby same-entity answer above it.

Rerankers should verify answer support directly: the passage should contain the
number, place, date, adaptation source, or yes-no status asked by the query.

### Training Data That May Help

Useful training data includes open-domain QA retrieval pairs, attributable
answer support selection data, quote retrieval, non-overlapping MIRACL or
Wikipedia question-passage pairs, and same-entity factual hard negatives. The
Nano split's questions, qrels, and cited answer passages should be excluded
from training.

Synthetic data can generate short factual questions and concise answer-bearing
passages with citation-like markers. Negatives should mention the same entity
but answer a different attribute, date, location, count, or status. Positives
should explicitly support the answer.

### Model Improvement Notes

Sparse systems should preserve entity and attribute terms. Dense retrievers
should strengthen fine-grained factual discrimination within the same entity
cluster. Rerankers should compare the question's requested slot against the
candidate passage.

For hybrid systems, `NanoMMTEB-v2 / hagrid` is a near-ceiling candidate
generation task. `reranking_hybrid` gives perfect recall@100, so the remaining
work is precise top-rank ordering among compact factual snippets.

## Example Data

| Query | Positive document |
| --- | --- |
| How many clubs are in the Australian Football League? [53 chars] | The Australian Football League consists of 18 clubs [1][2] [58 chars] |
| What was the film Nausicaä of the Valley of the Wind adapted from? [66 chars] | Nausicaä of the Valley of the Wind was adapted from the manga series of the same name written and illustrated by Hayao Miyazaki. [4] [132 chars] |
| Is Abi Branning still a character on EastEnders? [48 chars] | No, Abi Branning is not a regular character on EastEnders as she was killed off in January 2018 after falling from the roof of The Queen Victoria pub [2]. However, she did make a few guest appearances... [200 / 281 chars] |
| Where was Loretta Lynn born? [28 chars] | Loretta Lynn was born in Butcher Hollow, Kentucky. [1][2] [57 chars] |
| How old is the Cincinnati Bengals? [34 chars] | The Cincinnati Bengals are 51 years old overall and have been playing in the National Football League for 49 seasons [1]. [121 chars] |

### Public Sources

- [HAGRID: A Human-LLM Collaborative Dataset for Generative Information-Seeking with Attribution](https://arxiv.org/abs/2307.16883),
  2023.
- [HAGRID GitHub repository](https://github.com/project-miracl/hagrid).
- [mteb/HagridRetrieval](https://huggingface.co/datasets/mteb/HagridRetrieval).
- [hakari-bench/NanoMMTEB-v2](https://huggingface.co/datasets/hakari-bench/NanoMMTEB-v2),
  Nano benchmark dataset.

### Source Reference Table

| Title | Year | Type | URL |
| --- | ---: | --- | --- |
| HAGRID: A Human-LLM Collaborative Dataset for Generative Information-Seeking with Attribution | 2023 | task paper | [https://arxiv.org/abs/2307.16883](https://arxiv.org/abs/2307.16883) |
| HAGRID GitHub repository | 2023 | project page | [https://github.com/project-miracl/hagrid](https://github.com/project-miracl/hagrid) |
| mteb/HagridRetrieval | 2024 | dataset card | [https://huggingface.co/datasets/mteb/HagridRetrieval](https://huggingface.co/datasets/mteb/HagridRetrieval) |

### Representative Snippets

| Query pattern | Positive document pattern |
| --- | --- |
| A question asking how many clubs are in the Australian Football League. | A short passage stating the league has 18 clubs. |
| A question asking what Nausicaa of the Valley of the Wind was adapted from. | A passage stating it was adapted from the manga series. |
| A question asking whether Abi Branning is still a character on EastEnders. | A passage explaining that she was killed off and only later guest-appeared. |
| A question asking where Loretta Lynn was born. | A passage giving Butcher Hollow, Kentucky. |
| A question asking how old the Cincinnati Bengals are. | A passage giving the team's age and NFL seasons. |
