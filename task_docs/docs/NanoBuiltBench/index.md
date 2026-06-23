# NanoBuiltBench

## Overview

NanoBuiltBench is a compact English benchmark for built-asset information
retrieval. It evaluates whether a model can align architecture, engineering,
construction, and operations terminology across entity descriptions and
classification-system descriptions. The retrieval target is not generic web
relevance: the model must connect IFC-style building, infrastructure, product,
equipment, or facility-management entities to relevant Uniclass-style product
or class descriptions.

The group has two tasks: a broader retrieval split and a reranking-oriented
variant. Both are terminology-heavy and multi-positive. A single asset can map
to several acceptable classifications, and a correct match may depend on
function, hierarchy, material, or system context rather than exact wording.
BM25 measures how far controlled-vocabulary overlap goes, dense retrieval tests
semantic alignment across taxonomy language, and `reranking_hybrid` shows
whether exact terms and embedding similarity recover complementary candidates.

## What This Group Measures

[Benchmarking pre-trained text embedding models in aligning built asset information](https://www.nature.com/articles/s41598-025-09052-5)
studies text embedding models for aligning built-asset information across
classification systems. NanoBuiltBench adapts that setting into compact
retrieval tasks where queries are IFC-style names and definitions and documents
are Uniclass-style product or class descriptions.

The shared relevance relation is classification compatibility. A model must
rank descriptions that represent the same or compatible built-asset concept.
This is harder than matching words such as `door`, `duct`, `valve`, or
`sensor`, because nearby classes can share vocabulary while differing in asset
type, use, installation context, or level of generality.

## Task Families

- **Built-asset classification retrieval:** `NanoBuiltBench` retrieves
  Uniclass-style product descriptions for IFC-style asset descriptions.
- **Built-asset reranking:** `NanoBuiltBenchReranking` uses the same domain but
  emphasizes ranking candidate class descriptions for entity definitions.
- **Multi-positive taxonomy alignment:** both tasks contain several positives
  per query, so ranking quality matters beyond first-hit success.

## Dataset Shape

NanoBuiltBench contains 2 task pages, 282 queries, 5,659 split-local documents,
and 2,054 positive qrel rows. The main retrieval task has 200 queries and 1,480
positives; the reranking variant has 82 queries and 574 positives. Both average
about seven positives per query.

The texts are compact but technical. Query averages range from about 102 to 138
characters, while documents average about 309 to 342 characters. This is enough
text to include definition-like cues, but not enough to hide behind long-context
reasoning. The benchmark mainly tests domain vocabulary, taxonomy alignment,
and ranking among close class descriptions.

## Retrieval Behavior

### BM25 Profile

BM25 benefits from exact built-environment terms. Asset names, product labels,
and classification words often overlap between the IFC-style query and
Uniclass-style documents. The broader `NanoBuiltBench` task is stronger under
BM25 than the reranking variant, suggesting that direct vocabulary overlap
helps but does not fully order the relevant class set.

Sparse retrieval is limited when the query and document use different taxonomy
levels or synonyms. A term like `pipe`, `fitting`, `terminal`, or `control`
can appear in many nearby classes, and BM25 may rank related but incompatible
descriptions above the intended classification.

### Dense Profile

Dense retrieval is the strongest profile for both tasks in the current
metadata. It improves over BM25 because it can connect definitions by function
and built-asset semantics, not only by repeated tokens. This is important when
classification descriptions use different wording from IFC entity names.

Dense retrieval still needs domain sensitivity. Overly broad embedding
similarity can group assets by general topic while missing level of detail or
system role. For this group, dense gains are most meaningful when paired with
hard negatives from neighboring classes.

### Reranking Hybrid Profile

`reranking_hybrid` sits between BM25 and dense in the current task scores. That
does not make it unimportant: in taxonomy alignment, exact terms and semantic
definitions often recover different relevant classes. The hybrid profile is
therefore useful as a candidate-pool diagnostic for downstream reranking.

If a reranker is evaluated on this group, it should be checked against both
ranking quality and candidate coverage. The relevant set is multi-positive, so
dropping secondary valid classifications can lower recall even when a first hit
is found.

## Task Summary

| Task | Retrieval focus | Queries | Docs | Positives | BM25 nDCG@10 | Dense nDCG@10 | Reranking hybrid nDCG@10 | Best profile |
| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | --- |
| [NanoBuiltBench](NanoBuiltBench.md) | IFC-style asset to Uniclass description | 200 | 2,761 | 1,480 | 0.5235 | 0.6209 | 0.5751 | Dense |
| [NanoBuiltBenchReranking](NanoBuiltBenchReranking.md) | entity definition to candidate class | 82 | 2,898 | 574 | 0.2681 | 0.3650 | 0.3277 | Dense |

## Interpretation Notes for Model Researchers

NanoBuiltBench is a domain-alignment benchmark. Strong performance indicates
that a retriever understands built-environment terminology and classification
semantics, not simply that it can match English definitions. The multi-positive
structure matters: a query may have several valid class descriptions, and a
model should rank the relevant cluster well.

The group is also useful for testing domain adaptation. If a general embedding
model performs poorly here but well on web QA, the gap likely reflects missing
construction taxonomy knowledge. If BM25 is competitive, exact controlled
vocabulary is still carrying the task; if dense retrieval is much stronger, the
model is learning synonymy and hierarchy across classification systems.

## Training and Leakage Notes

Useful training data includes non-overlapping built-asset entity-to-class pairs,
IFC and Uniclass descriptions, construction taxonomy mappings, product-class
alignment data, and facility-management terminology. Hard negatives should come
from nearby product classes that share words but differ in function, level, or
asset type.

Exclude NanoBuiltBench evaluation queries, positives, qrels, and near-duplicate
classification descriptions. If source taxonomy tables are used for training,
audit exact row overlap before evaluating.

## Public Sources

- [Benchmarking pre-trained text embedding models in aligning built asset information](https://www.nature.com/articles/s41598-025-09052-5), 2025.

### Source Reference Table

| Source | Year | Type | URL |
| --- | ---: | --- | --- |
| Benchmarking pre-trained text embedding models in aligning built asset information | 2025 | paper | [https://www.nature.com/articles/s41598-025-09052-5](https://www.nature.com/articles/s41598-025-09052-5) |
