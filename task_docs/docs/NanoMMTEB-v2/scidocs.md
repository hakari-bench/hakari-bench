# NanoMMTEB-v2 / scidocs

## Overview

`NanoMMTEB-v2 / scidocs` is an English scientific-document retrieval task from
SCIDOCS. Queries are paper titles, and documents are scientific title/abstract
records. The Nano split has 200 queries, 10,000 documents, and 986 positive
qrel rows. Every query has multiple positives, averaging 4.93 related papers.
Current diagnostics show dense retrieval as the strongest profile,
`reranking_hybrid` close behind, and BM25 as weaker because scientific
relatedness often depends on citation, method, task, or application similarity
rather than exact keyword overlap.

## Details

### What the Original Data Measures

SPECTER introduced document-level representation learning for scientific papers
using citation-informed transformers, and SCIDOCS provides scientific
document-level evaluation tasks. In retrieval form, a query paper should return
scientifically related papers from a held-out corpus.

The task measures related-paper retrieval. A relevant document may be related by
citation context, shared method, common task, follow-up application, or
scientific background, not only by identical title words.

### Observed Data Profile

The Nano split contains 200 queries, 10,000 documents, and 986 positive qrel
rows. Every query has multiple positives: the average is 4.93 positives per
query, with a minimum of 3, median of 5, and maximum of 5. Queries average
69.79 characters, while documents average 1,202.68 characters.

Observed examples include papers about log mining, search-result visualization,
content delivery algorithms, architectural experience, and control of robots
with elastic joints. Documents are title plus abstract records across computer
science and related technical areas.

### BM25 Evaluation Profile

The dataset-provided BM25 candidate subset contains 500 candidates per query and
achieves nDCG@10 = 0.2067, hit@10 = 0.6100, and recall@100 = 0.4209. BM25 is
useful but clearly weaker than dense retrieval.

Exact scientific terms help when a query title and related abstract share a
method name, technical phrase, or application. However, true relevance can be
based on citation-informed relatedness, broader method families, or application
links that do not repeat the same title vocabulary.

### Dense Evaluation Profile

The dense `harrier_oss_v1_270m` candidate subset contains 500 candidates per
query and achieves nDCG@10 = 0.2773, hit@10 = 0.7050, and recall@100 = 0.5740.
Dense retrieval is the strongest observed profile.

This fits the SCIDOCS task design. Embedding similarity can capture research
topic, method, and application relationships beyond exact keywords. The modest
absolute scores also show that scientific relatedness is difficult: many papers
share terminology while belonging to different research lines.

### Reranking Hybrid Evaluation Profile

The `reranking_hybrid` candidate subset contains mostly 100 candidates per
query, with 11 queries using a rank-101 safeguard row. It achieves nDCG@10 =
0.2590, hit@10 = 0.6750, and recall@100 = 0.5335. Hybrid retrieval improves
over BM25 but remains below dense retrieval.

The hybrid profile suggests that sparse evidence helps retain keyword-related
papers, but the dense signal better ranks scientifically related documents.
Downstream rerankers should use the hybrid pool carefully and avoid overvaluing
surface overlap.

### Metric Interpretation for Model Researchers

This is a multi-positive task. nDCG@10 rewards ranking several related papers
early, while hit@10 only checks whether at least one positive appears near the
top. Recall@100 measures how many positives remain available to reranking.

Because each query has three to five positives, systems should be evaluated by
their ability to recover a set of related papers, not just a single obvious
match. Low recall@100 indicates that candidate generation itself is still a
major bottleneck.

### Query and Relevance Type Tendencies

Queries are paper titles. Relevant documents are title/abstract records related
by citation, topic, method, application, or scientific neighborhood. The
language is technical and often contains domain-specific terms.

The task rewards scientific-document representations that capture research
intent and related-work structure. It penalizes models that only match rare
keywords without understanding whether the papers address related problems.

### Representative Failure Modes

BM25 can retrieve papers that share technical vocabulary but are not related by
method, task, or citation context. Dense retrieval can retrieve broadly similar
research but miss a specific citation-style positive. Hybrid retrieval can
carry both exact-keyword false positives and broad-topic dense false positives.

Rerankers should compare method, task, dataset, application, and claimed
contribution across title and abstract, not just title overlap.

### Training Data That May Help

Useful training data includes citation-linked paper pairs, title and abstract
similarity data, co-citation and bibliography graph pairs, and SPECTER-style
scientific paper triplets. The Nano split's SCIDOCS query papers, qrels, and
positive records should be excluded from training.

Synthetic data can generate scientific title and abstract records with methods,
tasks, and claims. Queries can be paper titles or related-work search needs.
Positive documents should be scientifically related by citation, method, task,
or application. Negatives should share keywords while belonging to a different
research line.

### Model Improvement Notes

Dense retrievers should encode citation-informed relatedness, method
similarity, and task/application links. Sparse systems should preserve technical
terms but need reranking to handle shared vocabulary. Rerankers should reason
over title and abstract together and support multi-positive ranking.

For hybrid systems, `NanoMMTEB-v2 / scidocs` is a scientific relatedness test
where dense retrieval currently leads. Hybrid search can help with candidate
diversity, but top-rank improvements likely require scientific-document
reranking.

## Example Data

Representative queries include paper titles about mining log files, improving
search result comprehension, content delivery algorithms, architectural
experience, and gravity compensation for robots with elastic joints. Positive
documents are related scientific title/abstract records.

### Public Sources

- [SPECTER: Document-level Representation Learning using Citation-informed Transformers](https://arxiv.org/abs/2004.07180),
  2020.
- [SCIDOCS project page](https://allenai.org/data/scidocs).
- [mteb/scidocs](https://huggingface.co/datasets/mteb/scidocs).
- [hakari-bench/NanoMMTEB-v2](https://huggingface.co/datasets/hakari-bench/NanoMMTEB-v2),
  Nano benchmark dataset.

### Source Reference Table

| Title | Year | Type | URL |
| --- | ---: | --- | --- |
| SPECTER: Document-level Representation Learning using Citation-informed Transformers | 2020 | task paper | https://arxiv.org/abs/2004.07180 |
| SCIDOCS project page | 2020 | project page | https://allenai.org/data/scidocs |
| mteb/scidocs | 2024 | dataset card | https://huggingface.co/datasets/mteb/scidocs |

### Representative Snippets

| Query pattern | Positive document pattern |
| --- | --- |
| A paper title about mining log files for computing system management. | A related title/abstract record about automated text categorization. |
| A title about visualizing topic relevance in search results. | A related paper about exploratory search interfaces. |
| A title about content delivery algorithms. | A related paper about distributed caching and hot spots. |
| A title about architectural experience and embodiment. | A related paper about virtual reality exposure therapy outcomes. |
| A title about robot control with gravity compensation. | A related paper about impedance control for flexible-joint robots. |
