# NanoJMTEB-v2 / mr_tidy_japanese

## Overview

`NanoJMTEB-v2 / mr_tidy_japanese` is the Japanese Nano split of Mr. TyDi, a
multilingual benchmark line for monolingual dense retrieval. The task uses
short Japanese factual questions as queries and Japanese passages or entity
summaries as retrieval documents. It is useful for evaluating whether a model
can retrieve answer-bearing passages from concise information needs rather than
from long, keyword-rich queries. The Nano split has 200 queries, 10,000
documents, and 259 positive qrel rows. Unlike many Nano tasks, it includes
multi-positive queries: 56 queries have more than one positive. Current
diagnostics show dense retrieval as the strongest top-10 ranker, BM25 as a
strong high-recall sparse candidate generator, and `reranking_hybrid` as the
best top-100 coverage profile.

## Details

### What the Original Data Measures

Mr. TyDi was introduced as a multilingual benchmark for dense retrieval across
typologically diverse languages. Its Japanese split evaluates monolingual
retrieval: a Japanese query should retrieve relevant Japanese documents. The
benchmark was designed to test learned retrieval representations beyond
English and to expose how dense and sparse retrieval behave across different
languages.

The JMTEB version keeps this Japanese retrieval setting in an embedding
benchmark format. In this Nano split, the queries are short factual questions
and the relevant documents are short answer-bearing passages or entity
descriptions. The task therefore measures factual passage retrieval, entity and
relation matching, and robustness to concise Japanese question wording.

### Observed Data Profile

The Nano split contains 200 queries, 10,000 documents, and 259 positive qrel
rows. Positives per query average 1.295, with a minimum of 1, a median of 1, and
a maximum of 3. There are 56 multi-positive queries, representing 28.0 percent
of the query set. Queries average 18.44 characters, while documents average
233.46 characters.

Representative queries ask whether youth hostels have age limits, when Annie
Besant was born, what the indigenous religion of the Sami is, what citizen
ombudsmen monitor, and when Martin Luther King Jr. died. The positives are
Japanese passages that often contain the answer directly, but some require
matching an entity role or supporting context rather than simply finding a
word-for-word restatement.

### BM25 Evaluation Profile

The dataset-provided BM25 candidate subset contains 500 candidates per query and
achieves nDCG@10 = 0.5518, hit@10 = 0.7550, and recall@100 = 0.9614. This is a
useful but imperfect sparse profile. BM25 keeps most positives within the first
100 candidates, which makes it a good candidate generator, but its top-10
ranking is well below dense retrieval.

The pattern reflects the task's short factual queries. BM25 benefits when a
query contains a distinctive name, date expression, institution, or technical
term that appears in the passage. It struggles when the query asks for a role,
property, or relation and the top overlapping document is a related page rather
than an answer-bearing passage. For example, sparse matching can prioritize an
entity page that shares words with the question while missing the passage that
contains the exact answer relationship.

### Dense Evaluation Profile

The dense `harrier_oss_v1_270m` candidate subset contains 500 candidates per
query and achieves nDCG@10 = 0.7399, hit@10 = 0.8700, and recall@100 = 0.9228.
Dense retrieval is the strongest observed profile for top-10 ranking. This
fits the benchmark: the model must connect short natural questions to passages
that express the answer relation, sometimes without heavy lexical overlap.

The dense profile's recall@100 is lower than BM25's, which is also informative.
Embedding similarity improves ordering among many factual questions, but sparse
matching still catches some positives through names and exact terms that dense
retrieval misses. For researchers, this means the task rewards semantic
question-passage matching while still retaining important lexical anchors.

### Reranking Hybrid Evaluation Profile

The `reranking_hybrid` candidate subset contains 100 or 101 candidates per
query, with 3 safeguard positive rows and a mean of 100.015 candidates. It
achieves nDCG@10 = 0.6633, hit@10 = 0.8350, and recall@100 = 0.9846. The hybrid
profile has the best candidate coverage and is stronger than BM25 at top-10
ranking, but it does not match dense retrieval's nDCG@10 or hit@10.

This pattern shows complementary behavior. BM25 contributes exact-name and
exact-term coverage, while dense retrieval contributes semantic ranking quality.
The hybrid candidate set is especially attractive for reranking because it
keeps nearly all positives available in the first 100 candidates. A strong
reranker should be able to use this broader candidate pool to recover the dense
top-rank advantage while preserving BM25's coverage.

### Metric Interpretation for Model Researchers

This task has multiple positives for a substantial minority of queries, so
metrics should be read differently from single-positive entity-label tasks.
Hit@10 asks whether at least one relevant passage is retrieved near the top.
nDCG@10 rewards ranking relevant passages highly and can reflect gains from
ordering several positives. Recall@100 measures how many judged positives remain
available for reranking.

The current values indicate that dense retrieval is best when the evaluation
focuses on the first ten ranks, while hybrid retrieval is best when candidate
coverage matters. BM25 is not obsolete; it remains valuable as a high-recall
component, but it is less effective as a final ranker.

### Query and Relevance Type Tendencies

Queries are short Japanese factual questions. They often ask about dates,
definitions, legal or institutional categories, people, scientific facts, films,
or public qualifications. Relevant documents are short passages or summaries
that either state the answer directly or contain enough context to justify it.

Because queries are concise, a model must infer the answer type and relation
from few characters. The task rewards Japanese entity recognition, relation
matching, and the ability to distinguish an answer-bearing passage from a merely
topically related passage.

### Representative Failure Modes

BM25 can fail by ranking a page that shares the main entity name but does not
answer the question's relation. Dense retrieval can fail by retrieving a
semantically related passage with the wrong answer type, such as a related
person, institution, film, or event. Hybrid retrieval can keep both the right
and wrong candidates, leaving the final decision to a reranker.

Multi-positive queries add another source of complexity. A system can retrieve
one relevant passage but miss another, affecting recall-oriented metrics. Models
that compress all relevance into one canonical answer may underperform when
several passages are judged relevant.

### Training Data That May Help

Helpful training data includes Japanese Mr. TyDi examples, MIRACL-style
Japanese passage retrieval, Japanese factual QA retrieval, and Wikipedia-based
question-to-evidence pairs. Hard negatives should include pages that mention
the same entity but express the wrong relation or answer type. Multi-positive
training examples are also useful because this task includes multiple relevant
documents for some queries.

Benchmark-comparable training should avoid overlap with the Mr. TyDi Japanese
evaluation examples and the Nano split's qrels. Synthetic data can help when it
generates short Japanese factual questions from non-evaluation passages and
adds hard negatives from nearby entities.

### Model Improvement Notes

Dense retrievers should focus on relation-aware passage matching: not just
whether a passage is about the query's entity, but whether it answers the
question being asked. Sparse systems benefit from Japanese tokenization that
preserves names, dates, and technical terms. Rerankers should compare the
question's answer type against the passage content and handle multiple relevant
passages where available.

For hybrid systems, `mr_tidy_japanese` supports a two-stage design: use sparse
signals to maintain coverage, use dense signals for semantic ranking, and train
the reranker to resolve entity-role distinctions among topically similar
passages.

## Example Data

Representative questions ask about age limits for youth hostels, Annie
Besant's birth date, the indigenous religious role of the Sami, what groups
citizen ombudsmen monitor, and the death date of Martin Luther King Jr. The
positive passages are Japanese summaries that contain direct answers or
supporting context for those facts.

### Public Sources

- [Mr. TyDi: A Multi-lingual Benchmark for Dense Retrieval](https://arxiv.org/abs/2108.08787),
  2021.
- [castorini/mr-tydi](https://huggingface.co/datasets/castorini/mr-tydi),
  source dataset card.
- [sbintuitions/JMTEB](https://huggingface.co/datasets/sbintuitions/JMTEB),
  Japanese embedding benchmark card.
- [hakari-bench/NanoJMTEB-v2](https://huggingface.co/datasets/hakari-bench/NanoJMTEB-v2),
  Nano benchmark dataset.
- [mteb/mrtidy](https://huggingface.co/datasets/mteb/mrtidy), source task
  dataset.

### Source Reference Table

| Title | Year | Type | URL |
| --- | ---: | --- | --- |
| Mr. TyDi: A Multi-lingual Benchmark for Dense Retrieval | 2021 | paper | https://arxiv.org/abs/2108.08787 |
| castorini/mr-tydi |  | dataset card | https://huggingface.co/datasets/castorini/mr-tydi |
| sbintuitions/JMTEB | 2024 | dataset card | https://huggingface.co/datasets/sbintuitions/JMTEB |

### Representative Snippets

| Query pattern | Positive document pattern |
| --- | --- |
| A short question asking whether youth hostels have age limits. | A passage explaining historical age limits and later removal of upper age restrictions. |
| A question asking when Annie Wood Besant was born. | A biographical passage that includes Annie Besant's birth date and life dates. |
| A question asking what the indigenous religion of the Sami is. | A passage about the noaidi role in Sami indigenous religion. |
| A question asking what citizen ombudsmen are monitored as. | A passage about groups subject to information gathering or monitoring by a public-security institution. |
| A question asking when Martin Luther King Jr. died. | A short biographical passage containing his life dates. |
