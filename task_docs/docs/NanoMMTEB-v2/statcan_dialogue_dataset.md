# NanoMMTEB-v2 / statcan_dialogue_dataset

## Overview

`NanoMMTEB-v2 / statcan_dialogue_dataset` is a multilingual conversational
table-retrieval task from the Statistics Canada Dialogue Dataset. Queries are
partial live-chat conversations in English and French, and documents are
metadata-rich StatCan table descriptions. The Nano split has 200 queries,
10,000 documents, and 313 positive qrel rows. Many queries have multiple
relevant tables, averaging 1.565 positives per query. Current diagnostics show
dense retrieval as the strongest profile, `reranking_hybrid` as second, and
BM25 as extremely weak because users ask conversationally rather than repeating
official table metadata.

## Details

### What the Original Data Measures

The StatCan Dialogue Dataset was created for retrieving data tables through
conversations with genuine intents. It contains support conversations between
Statistics Canada agents and users looking for official published data. The
retrieval problem is to identify the table that satisfies the user's need from
an ongoing conversation.

The task measures conversational search over structured statistical metadata.
The model must infer measure, geography, sector, time period, population, and
table type from multiple dialogue turns.

### Observed Data Profile

The Nano split contains 200 queries, 10,000 documents, and 313 positive qrel
rows. The average positives per query is 1.565, with a minimum of 1, median of
1, and maximum of 9. The metadata records 32.0% of queries as multi-positive.
Queries average 794.77 characters, while documents average 7,237.69 characters.

Queries serialize live-chat turns between users and operators. Documents are
long table metadata records including title, dimensions, survey, frequency,
subject, geography, and date range.

### BM25 Evaluation Profile

The dataset-provided BM25 candidate subset contains 500 candidates per query and
achieves nDCG@10 = 0.0112, hit@10 = 0.0300, and recall@100 = 0.1406. BM25 is
extremely weak for this task.

The lexical mismatch is severe. Users describe needs conversationally, may ask
in French or English, and often do not know the official table title or metadata
terms. Long metadata records also contain many repeated statistical fields that
dilute sparse ranking.

### Dense Evaluation Profile

The dense `harrier_oss_v1_270m` candidate subset contains 500 candidates per
query and achieves nDCG@10 = 0.2731, hit@10 = 0.4550, and recall@100 = 0.7220.
Dense retrieval is the strongest observed profile.

This shows that semantic matching is essential. A dense model can connect a
conversation about inflation, GDP, business counts, race and sex tables, or
health data to a table whose official metadata uses different wording. The
absolute scores remain modest because tables with similar subjects often differ
only by geography, date range, frequency, or dimension.

### Reranking Hybrid Evaluation Profile

The `reranking_hybrid` candidate subset contains mostly 100 candidates per
query, with 47 queries using a rank-101 safeguard row. It achieves nDCG@10 =
0.1564, hit@10 = 0.3400, and recall@100 = 0.6581. Hybrid retrieval is much
better than BM25 but below dense retrieval.

This is a dense-first conversational retrieval task. Sparse evidence contributes
some table terminology, but BM25's weak signal can dilute dense ranking. The
hybrid pool is useful for reranking, yet dense retrieval currently provides the
best first-stage order.

### Metric Interpretation for Model Researchers

This is a multi-positive task for a substantial minority of queries. nDCG@10
rewards ranking all relevant tables early, while hit@10 only checks whether at
least one relevant table appears near the top. Recall@100 measures whether
candidate generation retains possible target tables for reranking.

The gap between dense and BM25 is itself important: it shows that official table
retrieval from conversations requires semantic and bilingual intent modeling,
not just title or keyword matching.

### Query and Relevance Type Tendencies

Queries are partial support conversations about official statistics. They may
ask for GDP, inflation, race or ethnicity by province and sex, business counts,
education, health indicators, sectors, geography, or date ranges. The dialogue
may include clarifying questions from an operator.

Relevant documents are table metadata records. The correct table must satisfy
the user's measure, geography, population, sector, time requirement, and
sometimes language preference.

### Representative Failure Modes

BM25 can miss the target because the user uses everyday wording while the table
uses official metadata terminology. Dense retrieval can retrieve the right
subject but wrong geography, period, population, or dimension. Hybrid retrieval
can improve coverage but still under-rank the exact table when long metadata
contains many overlapping fields.

Rerankers should compare the conversation to table dimensions and filter by
measure, geography, date range, subject, frequency, and survey.

### Training Data That May Help

Useful training data includes conversational search data, table retrieval pairs,
government statistics search logs, bilingual English/French support
conversations, and metadata-to-query pairs. The Nano split's conversations,
table IDs, qrels, and target metadata records should be excluded from training.

Synthetic data can generate partial support conversations where users ask for
official statistics by geography, date range, sector, and measure. Positive
tables should contain matching title, dimensions, survey, frequency, subject,
date range, and geography. Hard negatives should come from the same domain but
use the wrong geography, period, or measure.

### Model Improvement Notes

Dense retrievers should improve bilingual conversational intent matching and
structured table-metadata understanding. Sparse systems need query expansion,
translation, and metadata-field weighting to be useful. Rerankers should
explicitly compare requested table constraints against metadata fields.

For hybrid systems, `NanoMMTEB-v2 / statcan_dialogue_dataset` is a warning case:
adding sparse evidence does not surpass dense retrieval. The best gains are
likely from dense retrieval plus a table-aware reranker.

## Example Data

Representative conversations ask for provincial GDP, real GDP, growth and
inflation; race or ethnicity by province and sex; counts of sports-specialized
shops in Canada; annual inflation for 2019; and health data for a specific
Indigenous community. Positive documents are StatCan table metadata records
that satisfy the statistical need.

### Public Sources

- [A Dataset for Retrieving Data Tables through Conversations with Genuine Intents](https://arxiv.org/abs/2304.01412),
  2023.
- [StatCan Dialogue Dataset project page](https://mcgill-nlp.github.io/statcan-dialogue-dataset/).
- [mteb/StatcanDialogueDatasetRetrieval](https://huggingface.co/datasets/mteb/StatcanDialogueDatasetRetrieval).
- [hakari-bench/NanoMMTEB-v2](https://huggingface.co/datasets/hakari-bench/NanoMMTEB-v2),
  Nano benchmark dataset.

### Source Reference Table

| Title | Year | Type | URL |
| --- | ---: | --- | --- |
| A Dataset for Retrieving Data Tables through Conversations with Genuine Intents | 2023 | task paper | https://arxiv.org/abs/2304.01412 |
| StatCan Dialogue Dataset project page | 2023 | project page | https://mcgill-nlp.github.io/statcan-dialogue-dataset/ |
| mteb/StatcanDialogueDatasetRetrieval | 2024 | dataset card | https://huggingface.co/datasets/mteb/StatcanDialogueDatasetRetrieval |

### Representative Snippets

| Query pattern | Positive document pattern |
| --- | --- |
| A French conversation asking for provincial nominal GDP, real GDP, growth, and inflation. | A French table metadata record for GDP by industry, province, and territory. |
| An English conversation asking for race or ethnicity by province and sex. | A table metadata record about demographic characteristics by geography and sex. |
| A conversation asking how many sports-specialized shops exist in Canada. | A Canadian Business Counts table with NAICS and geography dimensions. |
| A French conversation asking for inflation at the end of 2019. | A consumer price index table with annual averages and product groups. |
| A conversation asking for health data on an Indigenous community. | A health indicator table by Aboriginal identity, sex, and geography. |
