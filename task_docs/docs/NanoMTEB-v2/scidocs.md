# NanoMTEB-v2 / scidocs

## Overview

`NanoMTEB-v2 / scidocs` is a scientific-document retrieval task. Queries are paper titles, and relevant documents are scientifically related papers, usually represented by title and abstract text. SCIDOCS was introduced with SPECTER as a benchmark for document-level scientific paper representations across citation, classification, and recommendation-style tasks. This Nano split contains 200 title queries over 10,000 scientific documents, with every query having multiple positives. It is useful for evaluating whether retrieval models capture research affinity beyond exact keyword overlap, including citation-like relatedness, shared methods, and related problem settings.

## Details

### What the Original Data Measures

SCIDOCS measures scientific paper representation quality. In retrieval form, a model must retrieve papers that are related to the query paper. The relevance relation is closer to citation or recommendation relevance than simple answer matching.

This makes the task hard for generic retrieval systems. A related paper may use different terminology, study a neighboring problem, or share a method without repeating many title words.

### Observed Data Profile

The Nano split contains 200 queries, 10,000 documents, and 986 positive qrel rows. Queries have 4.93 positives on average, with a median of 5 and a maximum of 5. Every query is multi-positive. Queries average 69.79 characters, while documents average 1,202.68 characters.

Queries look like scientific paper titles. Documents usually include paper titles and abstracts, often with dense technical vocabulary. The examples cover system log mining, search-result visualization, content delivery, architectural experience, and robot control.

### BM25 Evaluation Profile

The BM25 candidate subset uses top-500 candidates and reaches nDCG@10 of 0.2067, hit@10 of 0.6100, and recall@100 of 0.4209. BM25 is limited because scientific relatedness often does not depend on exact title overlap. Two related papers can use different keywords for the same research problem, and citation relevance may connect method, application, or background rather than repeated terms.

BM25 still helps when titles and abstracts share distinctive technical phrases, datasets, algorithms, or application names. Its low nDCG shows that exact vocabulary is not enough to rank citation-like related papers well.

### Dense Evaluation Profile

The dense candidate subset from `harrier_oss_v1_270m` uses top-500 candidates and reaches nDCG@10 of 0.2757, hit@10 of 0.7050, and recall@100 of 0.5730. Dense retrieval is stronger than BM25 across all reported metrics, which is expected for scientific recommendation-style retrieval.

The dense advantage suggests that embeddings capture broader research similarity, including shared tasks or methods that may not use identical wording. However, absolute scores remain modest, indicating that scientific paper retrieval requires specialized training beyond general semantic similarity.

### Reranking Hybrid Evaluation Profile

The `reranking_hybrid` subset uses top-100 candidates, with 12 queries carrying a rank-101 safeguard positive. It reaches nDCG@10 of 0.2565, hit@10 of 0.6750, and recall@100 of 0.5325. Hybrid retrieval improves over BM25 but does not beat dense retrieval, either in top-rank quality or recall.

This pattern indicates that the dense model is the stronger source of scientific relatedness for this split, while BM25 contributes some exact-terminology candidates. A reranker may still prefer the hybrid pool if it can use exact scientific terms without being dominated by them.

### Metric Interpretation for Model Researchers

Every query is multi-positive, so recall@100 is a central metric. A useful scientific retrieval system should expose several related papers, not only one. nDCG@10 measures whether related papers are ranked high enough for recommendation or literature-review use.

The gap between dense and BM25 shows that this task is more semantic than lexical. The moderate absolute scores also suggest that domain-specific scientific representation learning remains important.

### Query and Relevance Type Tendencies

Queries are paper titles. Relevant documents are scientific papers with titles and abstracts. Relevance may reflect citation, topical affinity, shared method, shared problem, or recommendation-style relatedness.

The relevance relation is research relatedness. It is not exact-answer retrieval and not duplicate detection.

### Representative Failure Modes

Common failures include retrieving papers with shared keywords but different research goals, missing related work that uses different terminology, over-ranking broad survey-like papers, and confusing method similarity with task similarity. Dense models may retrieve generally similar scientific areas while missing the specific citation-worthy relation.

### Training Data That May Help

Useful training data includes citation-linked paper pairs, scientific paper recommendation data, title-to-abstract retrieval pairs, and hard negatives from the same venue, topic, or method family. Multi-positive training is recommended because each query has several related papers.

### Model Improvement Notes

Models should be trained on scientific relatedness, not only text similarity. Citation-informed contrastive learning, field-aware hard negatives, and title-plus-abstract encoders are likely helpful. Rerankers should compare research contribution, task, method, and dataset rather than relying only on shared terminology.

## Example Data

### Public Sources

- [SPECTER: Document-level Representation Learning using Citation-informed Transformers](https://arxiv.org/abs/2004.07180), 2020.
- [MTEB: Massive Text Embedding Benchmark](https://arxiv.org/abs/2210.07316), 2023.
- [mteb/scidocs](https://huggingface.co/datasets/mteb/scidocs), source dataset card.

### Source Reference Table

| Title | Year | Type | URL |
| --- | ---: | --- | --- |
| SPECTER: Document-level Representation Learning using Citation-informed Transformers | 2020 | source task paper | https://arxiv.org/abs/2004.07180 |
| MTEB: Massive Text Embedding Benchmark | 2023 | benchmark paper | https://arxiv.org/abs/2210.07316 |
| mteb/scidocs |  | dataset card | https://huggingface.co/datasets/mteb/scidocs |

### Representative Snippets

| Query | Relevant document excerpt |
| --- | --- |
| An integrated framework on mining logs files for computing system management | A paper abstract about automated text categorization and classification of text into predefined categories. |
| Topic-Relevance Map: Visualization for Improving Search Result Comprehension | A paper about designing exploratory search on touch devices and improving search interaction. |
| Algorithmic Nuggets in Content Delivery | A paper about consistent hashing, random trees, and distributed caching protocols for web hot spots. |
| The Enactive Approach to Architectural Experience: A Neurophysiological Perspective on Embodiment, Motivation, and Affordances | A paper abstract about virtual reality exposure therapy for anxiety and specific phobias. |
| PD control with on-line gravity compensation for robots with elastic joints: Theory and experiments | A paper about Cartesian impedance control for flexible-joint robots using torque feedback and gravity compensation. |
