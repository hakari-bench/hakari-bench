# NanoMIRACL / ar

## Overview

`NanoMIRACL / ar` is the Arabic split of the MIRACL-style multilingual
monolingual retrieval benchmark. Arabic queries retrieve Arabic Wikipedia
passages, not translated evidence. The Nano split has 200 queries, 10,000
documents, and 386 positive qrel rows. More than half of the queries have
multiple positives, so the task measures retrieval of an answer-bearing passage
set rather than a single canonical passage. Current diagnostics show dense
retrieval as the strongest nDCG@10 profile, `reranking_hybrid` as the strongest
hit@10 and recall@100 profile, and BM25 as a strong but lower Arabic lexical
baseline.

## Details

### What the Original Data Measures

MIRACL was introduced as a multilingual ad hoc retrieval benchmark across many
languages. Its design is monolingual: Arabic queries retrieve Arabic passages
from Arabic Wikipedia. The benchmark emphasizes native-language queries,
Wikipedia passage evidence, and manual relevance judgments.

For Arabic, this means the model must handle short native Arabic information
needs, Arabic morphology, script normalization, named entities, and
encyclopedic passage structure. The retrieval unit is a passage rather than a
whole article, so the model must select the passage that contains the relevant
definition, date, location, count, entity fact, or answer evidence.

### Observed Data Profile

The Nano split contains 200 queries, 10,000 documents, and 386 positive qrel
rows. Positives per query average 1.93, with a minimum of 1, a median of 2, and
a maximum of 8. There are 109 multi-positive queries, representing 54.5 percent
of the split. Queries average 30.14 characters, while documents average 392.29
characters.

The examples are compact Arabic fact questions, often beginning with forms such
as `ما`, `من`, `متى`, `أين`, `كم`, or `هل`. Topics include publishing in
Lebanon, Marie Curie, the Kuwaiti National Assembly, the Habsburg dynasty,
Amazon cloud computing, geography, public figures, sports, companies, history,
religion, and medicine.

### BM25 Evaluation Profile

The dataset-provided BM25 candidate subset contains 500 candidates per query and
achieves nDCG@10 = 0.6352, hit@10 = 0.9200, and recall@100 = 0.9741. BM25 is
strong because many Arabic questions contain distinctive entity names, titles,
locations, dates, or topical nouns that also appear in relevant Wikipedia
passages.

The sparse profile is limited by Arabic surface variation and passage
disambiguation. Question forms such as attached `ماهي` versus separated `ما هي`,
hamza variants, spelling variation, and ambiguous named entities can affect
matching. BM25 also has difficulty when several passages mention the same
entity family but only some contain the answer relation.

### Dense Evaluation Profile

The dense `harrier_oss_v1_270m` candidate subset contains 500 candidates per
query and achieves nDCG@10 = 0.8223, hit@10 = 0.9500, and recall@100 = 0.9741.
Dense retrieval is the strongest observed profile by nDCG@10. It appears to
rank relevant Arabic passages higher than BM25 by using semantic question-
passage matching beyond exact surface overlap.

This is an important Arabic MIRACL pattern. The queries are short, and relevant
passages may express the requested fact with different morphology or wording.
Dense retrieval helps connect the intent of a question to evidence passages
even when exact token overlap is imperfect. Its recall@100 matches BM25 here,
so the main gain is top-rank ordering.

### Reranking Hybrid Evaluation Profile

The `reranking_hybrid` candidate subset contains exactly 100 candidates per
query, with no safeguard rows. It achieves nDCG@10 = 0.7514, hit@10 = 0.9650,
and recall@100 = 0.9974. Hybrid retrieval is not the best nDCG@10 profile, but
it has the best hit@10 and top-100 positive coverage.

This means hybrid search is especially useful for candidate generation. BM25
contributes exact Arabic names and rare terms, while dense retrieval contributes
semantic evidence matching. The combined profile keeps nearly all positives
available for reranking and finds at least one relevant passage for more
queries, but dense retrieval alone ranks the top results better by nDCG@10.

### Metric Interpretation for Model Researchers

This task is multi-positive for more than half of the queries. Hit@10 measures
whether at least one relevant passage appears near the top. nDCG@10 rewards
ranking relevant passages high, and recall@100 measures how much of the judged
positive set remains available for reranking.

The metric pattern is therefore nuanced: dense is best for top-rank quality,
hybrid is best for coverage, and BM25 is a strong lexical baseline. Arabic
retrieval models should be judged on both their ability to rank the best
evidence passages and their ability to preserve the broader positive set.

### Query and Relevance Type Tendencies

Queries are short Arabic fact questions asking about definitions, people,
dates, locations, counts, organizations, and yes/no properties. Relevant
documents are Arabic Wikipedia passages with article-title context and
answer-bearing prose.

The task rewards Arabic normalization, entity recognition, morphology-aware
matching, and semantic evidence retrieval. It also tests whether a system can
distinguish the right passage among several passages about related entities or
topics.

### Representative Failure Modes

BM25 can fail when Arabic spelling variants, hamza forms, attached question
words, or ambiguous entity names lead to wrong lexical matches. Dense retrieval
can fail by ranking a semantically related passage that lacks the exact answer
fact. Hybrid retrieval can include most positives but still require reranking
to choose the best evidence passage.

Other common risks include retrieving a broad article passage instead of the
specific answer passage, or confusing related locations, dynasties, events, or
institutions.

### Training Data That May Help

Useful training data includes non-overlapping MIRACL Arabic training data,
Arabic Wikipedia question-to-passage retrieval pairs, Arabic entity-centric QA
evidence retrieval, and hard negatives from related Arabic Wikipedia pages.
Training should include short native Arabic questions with varied question
forms and normalization variants.

Comparable evaluation should avoid upstream development or test data, or other
MIRACL-derived data likely to overlap with the NanoMIRACL evaluation questions
and passages.

### Model Improvement Notes

Dense retrievers should improve Arabic evidence ranking while preserving exact
entity and date signals. Sparse systems benefit from Arabic normalization,
tokenization, and handling of attached forms. Rerankers should combine exact
entity cues with semantic answer relation matching, especially for multi-
positive queries where several passages can be relevant.

For hybrid systems, `NanoMIRACL / ar` supports using hybrid retrieval as a
high-coverage candidate stage followed by a dense or cross-encoder reranker for
top-rank ordering.

## Example Data

Representative queries ask about the first publishing house in Lebanon, Marie
Curie's early research, the number of Kuwaiti National Assembly members, the
founder of the Habsburg dynasty, and when Amazon began offering cloud-computing
services. Positive documents are Arabic Wikipedia passages containing the
corresponding facts.

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
| An Arabic question asking about the first publishing house in Lebanon. | An Arabic Wikipedia passage about Lebanon and publishing houses. |
| A question asking about Marie Curie's early research. | A passage about Marie Curie and her scientific work. |
| A question asking how many members the Kuwaiti National Assembly has. | A passage about Kuwaiti politics and assembly membership. |
| A question asking who founded the Habsburg empire or dynasty. | A passage about the Habsburgs and their historical development. |
| A question asking when Amazon began providing cloud-computing service. | A passage about cloud computing and Amazon's role. |
