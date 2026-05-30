# NanoMMTEB-v2 / covid

## Overview

`NanoMMTEB-v2 / covid` is a Chinese COVID-19 passage-retrieval task from the
Multi-CPR family. Queries are concise Chinese information needs about pandemic
response, public services, factory reopening, local policies, and government
notices. The Nano split has 200 queries, 10,000 documents, and 204 positive
qrel rows. Most queries have one positive, with two multi-positive queries.
Current diagnostics show BM25 and `reranking_hybrid` as nearly tied on nDCG@10,
`reranking_hybrid` as strongest on hit@10 and recall@100, and dense retrieval
as close but slightly weaker.

## Details

### What the Original Data Measures

Multi-CPR introduced multi-domain Chinese passage retrieval datasets from real
search and human relevance annotation. The COVID retrieval split is a Chinese
news and policy retrieval task: a short user question must retrieve the article
passage that answers it.

The task measures fact-focused Chinese retrieval over pandemic-era public
information. Relevant passages often contain dates, locations, agencies,
measures, hotline numbers, service rules, reopening conditions, or operational
statistics.

### Observed Data Profile

The Nano split contains 200 queries, 10,000 documents, and 204 positive qrel
rows. Most queries have one positive; two queries have multiple positives. The
average positives per query is 1.02, with a maximum of 4. Queries average 25.74
characters, while documents average 409.35 characters.

Observed examples include questions about Beijing measures for small
businesses, Jiangsu medical teams sent to Hubei, online teaching in Wuzhou,
guidance for older adults and chronic-disease patients, and Ministry of
Transport accountability rules.

### BM25 Evaluation Profile

The dataset-provided BM25 candidate subset contains 500 candidates per query and
achieves nDCG@10 = 0.7888, hit@10 = 0.8750, and recall@100 = 0.9608. BM25 is a
very strong profile for this task.

The strength comes from short Chinese queries that often include distinctive
locations, agencies, policy terms, dates, or measured quantities. Term-frequency
matching can directly connect a question to the passage containing the requested
fact. BM25 may still fail when related notices share the same locality or
agency but answer a different operational question.

### Dense Evaluation Profile

The dense `harrier_oss_v1_270m` candidate subset contains 500 candidates per
query and achieves nDCG@10 = 0.7592, hit@10 = 0.8600, and recall@100 = 0.9363.
Dense retrieval is close to BM25 but slightly weaker across the main metrics.

This suggests that embedding similarity captures the public-health and policy
semantics well, but exact factual anchors still matter. A dense model may find
passages about the same city, service category, or pandemic measure while
missing the exact notice that contains the answer.

### Reranking Hybrid Evaluation Profile

The `reranking_hybrid` candidate subset contains mostly 100 candidates per
query, with two queries using a rank-101 safeguard row. It achieves nDCG@10 =
0.7873, hit@10 = 0.8900, and recall@100 = 0.9902. Hybrid retrieval has the best
hit@10 and recall@100 and is nearly tied with BM25 on nDCG@10.

This is a balanced hybrid-search case. Sparse matching contributes strong
factual anchors, while dense retrieval helps recover paraphrased policy or
service expressions. The remaining nDCG difference is small, so rerankers can
focus on distinguishing near-identical notices.

### Metric Interpretation for Model Researchers

This task is almost single-positive, but a small number of queries have
multiple positives. Hit@10 measures whether at least one answer passage appears
near the top. nDCG@10 rewards ranking relevant passages early, and recall@100
measures whether positives remain available for reranking.

Because the documents are short and fact-focused, high lexical scores are
meaningful. A good model should preserve exact Chinese names, dates, agencies,
and quantities while still handling paraphrased public-policy questions.

### Query and Relevance Type Tendencies

Queries are short Chinese questions targeting explicit facts in news or
government notice passages. They often ask how many measures were issued, when
a team departed, how an activity was executed, what a patient should do, or
which class of people is subject to accountability.

Relevant passages are Chinese news or policy snippets with concrete facts.
They may share locality and pandemic vocabulary with many other passages, so
fine-grained factual matching is important.

### Representative Failure Modes

BM25 can over-rank a passage from the right locality or agency that answers a
different question. Dense retrieval can retrieve a semantically related
COVID-era passage but miss the precise date, number, service rule, or targeted
population. Hybrid retrieval can still confuse near-duplicate policy notices.

Rerankers should compare the requested fact type against the passage, including
date, count, agency, service process, and affected group.

### Training Data That May Help

Useful training data includes Chinese passage retrieval data, Chinese news QA
pairs, COVID-era policy and public-service retrieval data, and hard negatives
matched by locality, agency, date, or service domain. The Nano split's queries,
qrels, and positive passages should be excluded from training.

Synthetic data can generate Chinese news and government notices with explicit
dates, agencies, services, rates, and quantities. Questions should target one
explicit fact. Negatives should come from the same public-health scenario while
answering a different operational question.

### Model Improvement Notes

Sparse systems should preserve Chinese lexical anchors and handle short-query
segmentation. Dense retrievers should strengthen fine-grained factual
distinctions within the same policy domain. Rerankers should score answer
support, not only topical match.

For hybrid systems, `NanoMMTEB-v2 / covid` is a strong example of hybrid search
working well: `reranking_hybrid` improves recall@100 and hit@10 while retaining
BM25-level nDCG@10. The main remaining challenge is ordering very similar
public-notice passages.

## Example Data

Representative queries ask how many measures Beijing issued for small and
micro enterprises, when Jiangsu sent its first medical team to Hubei, how Wuzhou
schools carried out online teaching, what older adults or chronic-disease
patients should do when symptoms appear, and which people the transport
authority said should be held accountable. Positive documents are Chinese
passages containing the requested fact.

### Public Sources

- [Multi-CPR: A Multi Domain Chinese Dataset for Passage Retrieval](https://arxiv.org/abs/2203.03367),
  2022.
- [MMTEB: Massive Multilingual Text Embedding Benchmark](https://arxiv.org/abs/2502.13595),
  2025.
- [mteb/CovidRetrieval](https://huggingface.co/datasets/mteb/CovidRetrieval).
- [hakari-bench/NanoMMTEB-v2](https://huggingface.co/datasets/hakari-bench/NanoMMTEB-v2),
  Nano benchmark dataset.

### Source Reference Table

| Title | Year | Type | URL |
| --- | ---: | --- | --- |
| Multi-CPR: A Multi Domain Chinese Dataset for Passage Retrieval | 2022 | task paper | https://arxiv.org/abs/2203.03367 |
| MMTEB: Massive Multilingual Text Embedding Benchmark | 2025 | benchmark paper | https://arxiv.org/abs/2502.13595 |
| mteb/CovidRetrieval | 2024 | dataset card | https://huggingface.co/datasets/mteb/CovidRetrieval |

### Representative Snippets

| Query pattern | Positive document pattern |
| --- | --- |
| A Chinese question asking how many measures Beijing issued for small businesses. | A passage about 16 measures and rent relief for small enterprises. |
| A question asking when the first Jiangsu medical team supported Hubei. | A passage about Jiangsu medical teams departing for Hubei. |
| A question about how Wuzhou online teaching was implemented. | A passage about delayed school opening and online teaching activity. |
| A question about what older adults and chronic-disease patients should do when symptomatic. | A public-health guidance passage for grassroots medical institutions. |
| A question about which people the Ministry of Transport would hold accountable. | A passage about strengthening COVID-19 prevention supervision. |
