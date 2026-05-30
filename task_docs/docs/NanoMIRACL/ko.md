# NanoMIRACL / ko

## Overview

`NanoMIRACL / ko` is the Korean split of the MIRACL-style multilingual
monolingual retrieval benchmark. Korean queries retrieve Korean Wikipedia
passages, not translated evidence. The Nano split has 200 queries, 10,000
documents, and 508 positive qrel rows. Queries are short, often entity-first,
and frequently express intent through Korean endings rather than an initial
question word. Current diagnostics show `reranking_hybrid` as the strongest
profile across nDCG@10, hit@10, and recall@100, with dense retrieval improving
top-rank quality over BM25 and BM25 preserving useful lexical coverage.

## Details

### What the Original Data Measures

MIRACL was introduced as a multilingual ad hoc retrieval benchmark over
Wikipedia passages. Its design is monolingual: Korean queries retrieve Korean
passages from Korean Wikipedia. The benchmark emphasizes native-language
questions, passage-level evidence, and human relevance judgments.

Korean is one of the MIRACL languages connected to the TyDi/Mr. TyDi lineage.
The MIRACL framing adds passage-level relevance judgments over a segmented
Wikipedia corpus. For this split, the relevant item is a Korean passage that
supports the question, not a translated English passage or a short answer.

### Observed Data Profile

The Nano split contains 200 queries, 10,000 documents, and 508 positive qrel
rows. Positives per query average 2.54, with a minimum of 1, a median of 2, and
a maximum of 12. There are 103 multi-positive queries, representing 51.5 percent
of the split. Queries average 21.71 characters, while documents average 205.28
characters.

The examples include short Korean questions and yes/no checks. Many begin with
the entity or topic, such as `세상에서`, `일본의`, `임진왜란이`, `중국의`,
`태양은`, `대한민국의`, or `히틀러가`, while intent appears through forms such
as `무엇인가`, `언제`, `어디`, `누구`, `몇`, `인가요`, and `있나요`. Topics
include science, history, geography, politics, entertainment, religion,
technology, definitions, universities, and public figures.

### BM25 Evaluation Profile

The dataset-provided BM25 candidate subset contains 500 candidates per query and
achieves nDCG@10 = 0.4994, hit@10 = 0.8000, and recall@100 = 0.9606. BM25 is
useful when there is near-verbatim overlap or a distinctive Korean title,
entity, date, or technical term. It also preserves many positives somewhere in
the top-100 pool.

The weak point is top-rank ordering. Short Korean questions can share generic
endings and forms such as `어디인가요`, `무엇인가`, and `몇 년도` with unrelated
passages. BM25 can also retrieve a passage about the right entity family while
missing the passage that states the requested capital, date, definition, or
yes/no fact.

### Dense Evaluation Profile

The dense `harrier_oss_v1_270m` candidate subset contains 500 candidates per
query and achieves nDCG@10 = 0.6910, hit@10 = 0.9100, and recall@100 = 0.9213.
Dense retrieval substantially improves top-rank quality over BM25 by matching
the semantic relation expressed in the Korean question.

The tradeoff is coverage. Dense retrieval has better nDCG@10 and hit@10 than
BM25, but lower recall@100. It is stronger at placing direct evidence near the
top, while lexical retrieval still helps preserve additional judged positives
for reranking.

### Reranking Hybrid Evaluation Profile

The `reranking_hybrid` candidate subset contains mostly 100 candidates per
query, with three queries using a rank-101 safeguard row. It achieves nDCG@10 =
0.7026, hit@10 = 0.9400, and recall@100 = 0.9882. Hybrid retrieval is the best
observed profile on all three metrics.

This makes Korean a strong hybrid-search case. BM25 contributes exact Korean
surface forms, names, and title matches, while dense retrieval contributes
relation-sensitive evidence matching. The combined candidate set ranks better
than dense alone and preserves more positives than either single-source profile.

### Metric Interpretation for Model Researchers

This task is multi-positive for 51.5 percent of queries. Hit@10 measures whether
at least one relevant passage appears near the top. nDCG@10 rewards ranking
relevant passages high, and recall@100 measures how much of the judged positive
set remains available for reranking.

The Korean pattern is complementary: BM25 supplies lexical recall, dense
retrieval supplies semantic ordering, and `reranking_hybrid` combines both into
the best observed candidate ranking. Researchers should evaluate whether models
handle Korean endings and entity-first phrasing without losing exact title and
name signals.

### Query and Relevance Type Tendencies

Queries are short Korean information needs about capitals, dates, historical
events, scientific definitions, yes/no claims, countries, organizations,
entertainment, and technology. Many are topic-led rather than wh-word-led, so a
model must infer the requested relation from the whole sentence.

Relevant documents are Korean Wikipedia passages with title context and
answer-bearing prose. The task rewards entity recognition, morphology-aware
matching, question-ending interpretation, and disambiguation among related
title pages or topic-near passages.

### Representative Failure Modes

BM25 can over-rank passages that share generic question endings. A question
about Iceland's capital can retrieve unrelated pages containing `어딘가` before
the Reykjavík passage. Similar issues occur for first-university and Tang
dynasty location questions where `어디`-like overlap is strong. Snow, Hitler,
or historical-date questions can retrieve plausible but non-labeled passages
around the same event or entity.

Dense retrieval can fail by selecting a semantically related Korean passage
that lacks the exact requested evidence. Hybrid retrieval reduces both missing
positive and top-rank failures, but reranking remains useful when the candidate
set contains several near-answer passages.

### Training Data That May Help

Useful training data includes non-overlapping MIRACL Korean training data,
Korean Wikipedia question-to-passage retrieval pairs, Korean open-domain QA
evidence retrieval datasets, and entity-attribute supervision for dates,
locations, historical roles, definitions, and yes/no factual checks. Hard
negatives should include near-title passages and generic-question distractors.

Synthetic data can help when it creates Korean Wikipedia-style passages with
titles, aliases, dates, places, organizations, definitions, and factual
evidence. Generated questions should include entity-first wording and forms such
as `무엇인가`, `언제`, `어디`, `누구`, `몇`, `인가요`, and `있나요`. Comparable
evaluation should exclude upstream development/test data or other MIRACL-derived
examples likely to overlap with this Nano split.

### Model Improvement Notes

Dense retrievers should improve Korean semantic relation matching while
preserving exact names, titles, and dates. Sparse systems benefit from Korean
morphological handling and better weighting of generic question endings.
Rerankers should choose the passage that directly states the fact, not merely a
passage with the right entity or a matching ending.

For hybrid systems, `NanoMIRACL / ko` is a positive hybrid benchmark:
`reranking_hybrid` improves nDCG@10, hit@10, and recall@100 over both individual
profiles. The main improvement target is robust reranking among multiple short
Korean evidence passages.

## Example Data

Representative queries ask whether Heracles is one of the Greek gods, which
number king Sukjong was in Joseon, whether Catholic canon law governs church
organization and believers, whether RNA is based on ribose chains, or where
Buddhism began. Positive documents are Korean Wikipedia passages containing the
requested yes/no, ordinal, definition, biochemical, or historical evidence.

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
| A Korean yes/no question asking whether Heracles is one of the Greek gods. | A passage about Greek mythology and Heracles. |
| A question asking which number king Sukjong was. | A passage about Joseon Sukjong and his reign. |
| A long yes/no question about Catholic canon law. | A passage about the Roman Catholic Church and canon law. |
| A question asking whether RNA is based on ribose chains. | A passage about RNA structure and ribose. |
| A question asking where Buddhism began. | A passage about Buddhist history and early spread from India. |
