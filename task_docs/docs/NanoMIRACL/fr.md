# NanoMIRACL / fr

## Overview

`NanoMIRACL / fr` is the French split of the MIRACL-style multilingual
monolingual retrieval benchmark. French queries retrieve French Wikipedia
passages, not translated evidence. The Nano split has 200 queries, 10,000
documents, and 417 positive qrel rows. The task is notable because BM25 keeps
high candidate coverage but ranks direct evidence relatively poorly, while dense
retrieval substantially improves top-rank quality. Current diagnostics show
dense retrieval as the strongest nDCG@10 profile and `reranking_hybrid` as the
strongest hit and recall profile.

## Details

### What the Original Data Measures

MIRACL was introduced as a multilingual ad hoc retrieval benchmark over
Wikipedia passages. Its design is monolingual: French queries retrieve French
passages from French Wikipedia. The benchmark emphasizes natural-language
questions, passage-level evidence, and human relevance judgments.

French is one of the MIRACL languages created beyond the earlier Mr. TyDi/TyDi
QA sources. It should therefore be read as a MIRACL-created French Wikipedia
retrieval task, not as translated English retrieval. The relevant item is the
French passage that supports the question, rather than a direct answer string or
an article-level label.

### Observed Data Profile

The Nano split contains 200 queries, 10,000 documents, and 417 positive qrel
rows. Positives per query average 2.09, with a minimum of 1, a median of 2, and
a maximum of 7. There are 123 multi-positive queries, representing 61.5 percent
of the split. Queries average 43.26 characters, while documents average 385.31
characters.

The examples are ordinary French questions using forms such as `Qui`, `Quel`,
`Quelle`, `Quels`, `Quelles`, `Quand`, `Où`, `Comment`, `Combien`, `Pourquoi`,
and `Qu’est-ce`. Topics include people, places, science, music, politics,
history, mathematics, demographics, food, religion, electricity generation,
biomedical data, geography, and definitions.

### BM25 Evaluation Profile

The dataset-provided BM25 candidate subset contains 500 candidates per query and
achieves nDCG@10 = 0.4658, hit@10 = 0.9000, and recall@100 = 0.9832. BM25 is
good at keeping French positives somewhere in the candidate pool. Exact
entities, place names, topical nouns, and technical terms often surface the
right neighborhood.

The weak point is ranking. BM25 frequently retrieves plausible French passages
that share topic words or morphology but do not express the requested relation.
This makes the split difficult for sparse retrieval even though recall@100 is
high. The model must go beyond matching `fleuve`, `chimie`, `café`, or
`morphologie` and identify the passage that directly answers the question.

### Dense Evaluation Profile

The dense `harrier_oss_v1_270m` candidate subset contains 500 candidates per
query and achieves nDCG@10 = 0.6828, hit@10 = 0.9200, and recall@100 = 0.9113.
Dense retrieval is the strongest observed profile by nDCG@10. It improves
top-rank quality by matching question intent and passage evidence more directly
than surface overlap alone.

The tradeoff is lower recall@100 than BM25 and hybrid retrieval. Dense retrieval
is better at selecting strong top evidence, but it leaves more judged positives
outside the top-100 candidate set. For French, this makes dense retrieval a
strong ranker but not the most complete candidate generator.

### Reranking Hybrid Evaluation Profile

The `reranking_hybrid` candidate subset contains exactly 100 candidates per
query, with no safeguard rows. It achieves nDCG@10 = 0.5896, hit@10 = 0.9250,
and recall@100 = 0.9976. Hybrid retrieval is below dense retrieval by nDCG@10,
but it has the best hit@10 and the strongest top-100 positive coverage.

This profile is useful for reranking pipelines. BM25 contributes exact French
surface forms and names, while dense retrieval contributes semantic relation
matching. The combined candidate set almost fully preserves judged positives,
but a downstream reranker is still needed to reach dense-level or better
top-rank ordering.

### Metric Interpretation for Model Researchers

This task is multi-positive for 61.5 percent of queries. Hit@10 measures whether
at least one relevant passage appears near the top. nDCG@10 rewards ranking
relevant passages high, and recall@100 measures how much of the judged positive
set survives for reranking.

The French split clearly separates ranking quality from candidate coverage.
Dense retrieval is best for top-rank ordering, BM25 keeps many positives but
ranks them less well, and `reranking_hybrid` gives the strongest recall. A good
French retrieval system should combine dense semantic ranking with lexical
coverage and then rerank for evidence specificity.

### Query and Relevance Type Tendencies

Queries are concise French information needs about definitions, people, places,
dates, quantities, causes, roles, classifications, and scientific or geographic
facts. They often include an obvious topic word, but the relevant passage must
state the requested relation.

Relevant documents are French Wikipedia passages with title context and
answer-bearing prose. The task rewards sense disambiguation, entity matching,
question-form understanding, and passage-level relation selection.

### Representative Failure Modes

BM25 can retrieve a passage with the right word sense family but the wrong
answer relation. A question about the Orinoco river can retrieve an unrelated
song or named-entity passage containing `Orénoque`. A question about branches of
chemistry can retrieve language or chemistry-adjacent pages before the passage
that describes the relevant scientific domains. A question about the largest
coffee producer can retrieve coffee-terroir or country-specific pages before a
general coffee passage with the answer. A question about flower morphology can
retrieve linguistic morphology pages instead of botanical evidence.

Dense retrieval can fail by choosing a semantically related passage that lacks
the exact fact. Hybrid retrieval reduces missing positives but still needs a
reranker to prefer the direct evidence passage among many plausible French
candidates.

### Training Data That May Help

Useful training data includes non-overlapping MIRACL French training data,
French Wikipedia question-to-passage retrieval pairs, French open-domain QA
evidence retrieval datasets, and French entity-attribute supervision for places,
dates, counts, professions, definitions, causes, and classifications. Hard
negatives should include homonymous and near-topic French passages.

Synthetic data can help when it creates French Wikipedia-style passages with
titles, aliases, dates, places, demographic facts, definitions, roles, and
factual evidence. Generated questions should use varied `Qui`, `Quel`,
`Quelle`, `Quels`, `Quelles`, `Quand`, `Où`, `Comment`, `Combien`, `Pourquoi`,
and `Qu’est-ce` forms. Comparable evaluation should exclude upstream
development/test data or other MIRACL-derived examples likely to overlap with
this Nano split.

### Model Improvement Notes

Dense retrievers should preserve their French top-rank advantage while
recovering more lexical candidate coverage. Sparse systems should improve sense
disambiguation and relation-aware term weighting rather than relying only on
surface overlap. Rerankers should penalize topic-near but non-answering
passages, especially for ambiguous terms and scientific or geographic questions.

For hybrid systems, `NanoMIRACL / fr` supports a high-coverage candidate stage
followed by strong reranking. The hybrid profile nearly covers all positives,
while the dense profile shows the level of semantic ranking quality needed at
the top of the list.

## Example Data

Representative queries ask what a cardinal does, what Pablo Picasso's wife was
called, what a referendum is, who the last Polish king was, or what branches of
chemistry are. Positive documents are French Wikipedia passages containing the
requested role, relationship, definition, historical fact, or classification.

### Public Sources

- [Making a MIRACL: Multilingual Information Retrieval Across a Continuum of Languages](https://arxiv.org/abs/2210.09984),
  2022.
- [MIRACL: A Multilingual Retrieval Dataset Covering 18 Diverse Languages](https://aclanthology.org/2023.tacl-1.63/),
  2023.
- [MIRACL GitHub repository](https://github.com/project-miracl/miracl).
- [miracl/miracl-corpus](https://huggingface.co/datasets/miracl/miracl-corpus),
  source corpus dataset.
- [hakari-bench/NanoMIRACL](https://huggingface.co/datasets/hakari-bench/NanoMIRACL),
  Nano benchmark dataset.

### Source Reference Table

| Title | Year | Type | URL |
| --- | ---: | --- | --- |
| Making a MIRACL: Multilingual Information Retrieval Across a Continuum of Languages | 2022 | paper | https://arxiv.org/abs/2210.09984 |
| MIRACL: A Multilingual Retrieval Dataset Covering 18 Diverse Languages | 2023 | paper | https://aclanthology.org/2023.tacl-1.63/ |
| MIRACL GitHub repository |  | project repository | https://github.com/project-miracl/miracl |
| miracl/miracl-corpus |  | dataset card | https://huggingface.co/datasets/miracl/miracl-corpus |

### Representative Snippets

| Query pattern | Positive document pattern |
| --- | --- |
| A French question asking what a cardinal does. | A passage about cardinals and their role in the Catholic Church. |
| A question asking for Pablo Picasso's wife. | A biographical passage about Picasso and his family context. |
| A question asking what a referendum is. | A passage defining referendum as a legal or democratic process. |
| A question asking who the last Polish king was. | A passage listing Polish sovereigns and the final king. |
| A question asking for branches of chemistry. | A passage describing chemistry domains or the chemist profession. |
