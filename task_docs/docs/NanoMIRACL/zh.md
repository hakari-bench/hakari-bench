# NanoMIRACL / zh

## Overview

`NanoMIRACL / zh` is the Chinese split of the MIRACL-style multilingual
monolingual retrieval benchmark. Chinese queries retrieve Chinese Wikipedia
passages, not translated evidence. The Nano split has 200 queries, 10,000
documents, and 471 positive qrel rows. Queries are very short compared with
most other MIRACL splits, often asking one compact entity-attribute question.
Current diagnostics show dense retrieval as the strongest top-rank profile,
`reranking_hybrid` as the strongest recall profile, and BM25 as a weak lexical
baseline for this short-query setting.

## Details

### What the Original Data Measures

MIRACL was introduced as a multilingual ad hoc retrieval benchmark over
Wikipedia passages. Its design is monolingual: Chinese queries retrieve Chinese
passages from Chinese Wikipedia. The benchmark emphasizes native-language
questions, passage-level evidence, and human relevance judgments.

Chinese is one of the MIRACL languages created beyond the earlier Mr. TyDi/TyDi
QA sources. The task should therefore be read as MIRACL-style Chinese Wikipedia
retrieval, not as a translated English benchmark. The relevant item is a
Chinese passage that contains evidence for the question, not a direct answer
string.

### Observed Data Profile

The Nano split contains 200 queries, 10,000 documents, and 471 positive qrel
rows. Positives per query average 2.36, with a minimum of 1, a median of 2, and
a maximum of 7. There are 122 multi-positive queries, representing 61.0 percent
of the split. Queries average only 10.86 characters, while documents average
133.35 characters.

The examples are compact complete Chinese questions such as year, location,
area, list, membership, person, symbolic meaning, and quantity questions.
Topics include countries, institutions, history, religion, transportation,
people, geography, companies, entertainment, biographies, canals, railways, UN
membership, Christian symbols, and country area.

### BM25 Evaluation Profile

The dataset-provided BM25 candidate subset contains 500 candidates per query and
achieves nDCG@10 = 0.4022, hit@10 = 0.7300, and recall@100 = 0.8514. BM25 is
limited because Chinese queries are extremely short. A few characters can
represent both the main entity and the requested relation, so surface overlap
alone can retrieve many plausible but non-answering passages.

BM25 works when the query contains a distinctive title or entity, but it is
vulnerable to short-query ambiguity. Country area questions can retrieve general
geography pages, organization-membership questions can retrieve broad
organization pages, and person-date questions can retrieve related event pages
instead of the passage with the requested fact.

### Dense Evaluation Profile

The dense `harrier_oss_v1_270m` candidate subset contains 500 candidates per
query and achieves nDCG@10 = 0.7191, hit@10 = 0.9850, and recall@100 = 0.9873.
Dense retrieval is the strongest observed profile by nDCG@10 and hit@10, and it
also has very high recall. It substantially improves over BM25 by binding the
short Chinese question to the intended relation.

This split is therefore a strong dense-retrieval case. The model must infer
that a query asks for which year, where, how large, which items, who, what a
symbol represents, when something happened, or how many items exist. Dense
retrieval handles this relation-level intent much better than exact term
matching alone.

### Reranking Hybrid Evaluation Profile

The `reranking_hybrid` candidate subset contains exactly 100 candidates per
query, with no safeguard rows. It achieves nDCG@10 = 0.5619, hit@10 = 0.8800,
and recall@100 = 1.0000. Hybrid retrieval is below dense retrieval at top ranks,
but it preserves every judged positive within the observed top-100 candidate
set.

This profile is useful for candidate generation. BM25 contributes exact Chinese
entity strings, titles, and list terms, while dense retrieval contributes
semantic relation matching. The hybrid candidate set maximizes coverage, but it
needs a reranker to recover dense-level top-rank ordering.

### Metric Interpretation for Model Researchers

This task is multi-positive for 61.0 percent of queries. Hit@10 measures whether
at least one relevant passage appears near the top. nDCG@10 rewards ranking
relevant passages high, and recall@100 measures how much of the judged positive
set remains available for reranking.

The Chinese metric pattern is clear. Dense retrieval is the best top-rank and
single-source candidate model, while `reranking_hybrid` is best for complete
positive coverage. BM25 alone is much weaker because very short Chinese queries
leave little room for robust lexical discrimination.

### Query and Relevance Type Tendencies

Queries are concise Chinese information needs about years, locations, country
areas, lists, memberships, people, symbolic meanings, historical events,
institutions, and quantities. Many contain only the entity plus the requested
attribute phrase.

Relevant documents are Chinese Wikipedia passages with title context and short
answer-bearing prose. The task rewards short-query relation binding, entity
recognition, list and membership reasoning, and disambiguation among passages
that share the same entity or attribute word.

### Representative Failure Modes

BM25 can retrieve general UN pages before a passage that explicitly lists the
Security Council permanent members for `联合国五常国家有哪些?`. A Sui dynasty canal
question can retrieve Grand Canal or canal pages before a passage listing the
segments built under Sui rule. A question about when Cameron took office can
retrieve government-formation or Brexit pages before the David Cameron
biography passage. An Australia area question can retrieve environmental or
federal-state pages before the country passage with the area statement.

Dense retrieval can still fail when a semantically close Chinese passage lacks
the exact relation or list. Hybrid retrieval reduces missing positives but
requires reranking to place the direct evidence passage first.

### Training Data That May Help

Useful training data includes non-overlapping MIRACL Chinese training data,
Chinese Wikipedia question-to-passage retrieval pairs, Chinese open-domain QA
evidence retrieval datasets, and related Chinese Wikipedia hard negatives with
similar entity or attribute words. Training should focus on short-query
relation binding and hard negatives that reuse the same entity.

Synthetic data can help when it creates Chinese Wikipedia-style passages with
titles, aliases, dates, lists, areas, memberships, historical events,
institutions, geography, and biographies. Generated questions should be concise
and use which-year, where, how-large, which-items, who, what-represents, when,
and how-many forms. Comparable evaluation should exclude upstream
development/test data or other MIRACL-derived examples likely to overlap with
this Nano split.

### Model Improvement Notes

Dense retrievers should preserve their strong Chinese short-query behavior
while approaching hybrid recall. Sparse systems need better Chinese
segmentation, phrase handling, and relation-aware weighting for extremely short
queries. Rerankers should distinguish direct evidence from pages that merely
share the same entity, country, organization, or list vocabulary.

For hybrid systems, `NanoMIRACL / zh` supports `reranking_hybrid` as a complete
coverage candidate stage, followed by dense or cross-encoder reranking. Dense
retrieval sets the top-rank quality target; hybrid retrieval supplies the full
positive pool.

## Example Data

Representative queries ask how large Xinjiang is, who belongs to the British
royal family, which genres are part of American popular music, which continent
Venezuela is in, or what the Yellow Emperor's wife was called. Positive
documents are Chinese Wikipedia passages containing the requested area,
membership, list, geographic, or biographical evidence.

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
| A Chinese question asking how large Xinjiang is. | A passage about Xinjiang and its area. |
| A question asking which members belong to the British royal family. | A passage about the British royal family and succession context. |
| A question asking which genres belong to American popular music. | A passage listing styles and genres in American popular music. |
| A question asking which continent Venezuela is in. | A passage about Venezuela and its South American location. |
| A question asking the name of the Yellow Emperor's wife. | A passage about the Yellow Emperor and his consorts. |
