# NanoMIRACL / id

## Overview

`NanoMIRACL / id` is the Indonesian split of the MIRACL-style multilingual
monolingual retrieval benchmark. Indonesian queries retrieve Indonesian
Wikipedia passages, not translated evidence. The Nano split has 200 queries,
10,000 documents, and 654 positive qrel rows. It is heavily multi-positive and
uses short Indonesian fact questions with forms such as `Apa`, `Apakah`,
`Kapan`, `Berapa`, `Berapakah`, `Siapa`, `Siapakah`, `Dimana`, and
`Dimanakah`. Current diagnostics show `reranking_hybrid` as the strongest
profile across nDCG@10, hit@10, and recall@100, with BM25 and dense retrieval
both useful but incomplete on their own.

## Details

### What the Original Data Measures

MIRACL was introduced as a multilingual ad hoc retrieval benchmark over
Wikipedia passages. Its design is monolingual: Indonesian queries retrieve
Indonesian passages from Indonesian Wikipedia. The benchmark emphasizes
native-language questions, passage-level evidence, and human relevance
judgments.

Indonesian is one of the MIRACL languages connected to the TyDi/Mr. TyDi
lineage. The MIRACL framing provides passage-level retrieval judgments over a
segmented Wikipedia corpus. For this split, the relevant item is an Indonesian
passage that supports the question, not a translated English passage or direct
answer string.

### Observed Data Profile

The Nano split contains 200 queries, 10,000 documents, and 654 positive qrel
rows. Positives per query average 3.27, with a minimum of 1, a median of 3, and
a maximum of 10. There are 140 multi-positive queries, representing 70.0 percent
of the split. Queries average 38.29 characters, while documents average 416.45
characters.

The examples are short Indonesian questions with visible case variation, such
as `Apa`, lowercase `apakah`, `kapankah`, and `dimanakah`. Topics include
history, religion, science, film, politics, geography, biology, definitions,
national anthems, capitals, populations, wars, salts, cells, caste, regions,
and public figures.

### BM25 Evaluation Profile

The dataset-provided BM25 candidate subset contains 500 candidates per query and
achieves nDCG@10 = 0.6773, hit@10 = 0.9500, and recall@100 = 0.9786. BM25 is
strong because Indonesian questions often contain distinctive entity names,
country names, titles, technical terms, or capital-city clues. Exact matching is
especially useful for named places, people, wars, and religious terms.

The sparse profile still has ranking limitations. BM25 can retrieve a related
capital, national anthem, region, or entity page before the passage that
directly answers the question. It can also be confused when a query and a label
are near an ambiguous topic, such as Quran surah numbering or neighboring
geographic regions.

### Dense Evaluation Profile

The dense `harrier_oss_v1_270m` candidate subset contains 500 candidates per
query and achieves nDCG@10 = 0.7076, hit@10 = 0.9400, and recall@100 = 0.9526.
Dense retrieval improves nDCG@10 over BM25 by ranking semantically relevant
Indonesian passages higher, especially for definition, first-work, capital,
population, and yes/no questions.

The dense profile is slightly weaker than BM25 by hit@10 and recall@100. This
means semantic matching improves top-rank ordering but loses some lexical
coverage. Indonesian therefore benefits from retaining exact entity and title
signals alongside dense similarity.

### Reranking Hybrid Evaluation Profile

The `reranking_hybrid` candidate subset contains exactly 100 candidates per
query, with no safeguard rows. It achieves nDCG@10 = 0.7171, hit@10 = 0.9650,
and recall@100 = 0.9985. Hybrid retrieval is the strongest observed profile on
all three metrics.

This split is a clear case where hybrid search is more than a coverage fallback.
BM25 contributes exact Indonesian surface forms and entity names, while dense
retrieval contributes semantic relation matching. The combined candidate set
both ranks better than either individual profile and preserves nearly all judged
positives for reranking.

### Metric Interpretation for Model Researchers

This task is multi-positive for 70.0 percent of queries. Hit@10 measures whether
at least one relevant passage appears near the top. nDCG@10 rewards ranking
relevant passages high, and recall@100 measures how much of the judged positive
set remains available for reranking.

The Indonesian pattern is comparatively hybrid-friendly. BM25 has strong
coverage, dense retrieval improves semantic ordering, and `reranking_hybrid`
combines both into the best top-rank and recall profile. Researchers should
treat this split as evidence that lexical and dense signals are complementary
for Indonesian Wikipedia retrieval.

### Query and Relevance Type Tendencies

Queries are short Indonesian information needs about capitals, dates, counts,
definitions, religious facts, scientific terms, people, regions, media, and
historical events. Many questions are simple on the surface, but relevance
depends on finding the passage with the exact requested fact.

Relevant documents are Indonesian Wikipedia passages with title context and
answer-bearing prose. The task rewards entity matching, relation understanding,
case-robust question handling, and disambiguation among related countries,
regions, songs, religious texts, or scientific concepts.

### Representative Failure Modes

BM25 can retrieve a page about another capital city before the Tallinn passage
for a question about Estonia's capital. A question about Canada's national
anthem can retrieve other national-anthem pages before the Canadian evidence.
Geographic questions about Riau or Bohemia can pull in related administrative or
capital-city pages. Quran-related queries may expose ambiguity between a direct
surah title and a passage that mentions a range of verses.

Dense retrieval can miss exact named-entity positives when semantic similarity
points to a related but non-answering passage. Hybrid retrieval reduces both
failure modes, but reranking is still useful when many positives and near-
positives are present.

### Training Data That May Help

Useful training data includes non-overlapping MIRACL Indonesian training data,
Indonesian Wikipedia question-to-passage retrieval pairs, Indonesian
entity-attribute QA evidence retrieval pairs, and hard negatives from related
Indonesian Wikipedia pages. Training should include capital-city, national
anthem, region, religion, science, population, and first-work questions.

Synthetic data can help when it creates Indonesian Wikipedia-style passages with
titles, aliases, locations, dates, populations, religious terms, scientific
terms, and factual evidence. Generated questions should use varied `Apa`,
`Apakah`, `Kapan`, `Berapa`, `Berapakah`, `Siapa`, `Siapakah`, `Dimana`, and
`Dimanakah` forms with realistic case variation. Comparable evaluation should
exclude upstream development/test data or other MIRACL-derived examples likely
to overlap with this Nano split.

### Model Improvement Notes

Dense retrievers should retain semantic ranking gains while recovering BM25's
named-entity coverage. Sparse systems should improve ranking among related
entity pages and reduce over-reliance on shared question terms. Rerankers should
combine exact Indonesian entity evidence with relation-level answer matching.

For hybrid systems, `NanoMIRACL / id` is a strong positive example:
`reranking_hybrid` improves nDCG@10, hit@10, and recall@100 at the same time.
The main next step is to rerank the high-coverage candidate set for direct
evidence specificity.

## Example Data

Representative queries ask how many characters can fit in an Indonesian SMS
context, where the printing press was first created, what Acta Sanctorum is,
what audio frequency means, or where James Hepburn died. Positive documents are
Indonesian Wikipedia passages containing the relevant numeric, historical,
definition, technical, or biographical evidence.

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
| An Indonesian question asking about character count in messaging. | A passage about short message service and character limits. |
| A question asking where the printing press was first created. | A passage with historical context about printed texts or scripture transmission. |
| A question asking what Acta Sanctorum is. | A passage defining the publication and its volumes. |
| A question asking what audio frequency means. | A passage explaining low-frequency signals or modulation context. |
| A question asking where a person died. | A biographical passage containing the death place and date. |
