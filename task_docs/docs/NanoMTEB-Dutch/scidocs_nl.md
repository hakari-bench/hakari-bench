# NanoMTEB-Dutch / scidocs_nl

## Overview

`scidocs_nl` is the Dutch SCIDOCS retrieval task from BEIR-NL. Queries are
Dutch-translated scientific-paper titles, and documents are translated paper
titles and abstracts. The Nano split contains 200 queries, 10,000 documents,
and 986 positive qrel rows. Every query has multiple positives: the average is
4.93 positives per query, the median is five, and all 200 queries are
multi-positive.

This is one of the hardest Dutch retrieval tasks in the current batch. The
relevance relation is scientific relatedness, citation, co-citation, or paper
recommendation, not answer containment. BM25 is weak because related papers may
share a method, background problem, or citation context without sharing title
terms. Dense retrieval with `harrier_oss_v1_270m` is strongest across nDCG@10,
hit@10, and recall@100 among the individual final orders, while
`reranking_hybrid` improves over BM25 but does not beat dense. The task strongly
rewards scientific semantic representations.

## Details

### What the Original Data Measures

[SPECTER: Document-level Representation Learning using Citation-informed Transformers](https://arxiv.org/abs/2004.07180)
introduced SciDocs as a benchmark for scientific document representation,
including citation prediction, co-citation, recommendation, and classification.
In BEIR-style retrieval, the query is a paper title, and relevant documents are
scientifically related papers.

MTEB-NL describes SCIDOCS-NL as a machine-translated Dutch adaptation from
BEIR-NL. The task asks a model to retrieve documents that are cited by, should
be cited by, or are otherwise related to a query paper. This is closer to paper
recommendation than ordinary fact retrieval.

### Observed Data Profile

Queries average 77.73 characters and are scientific titles. Documents average
1,331.57 characters and are abstract-like scientific records. Each query has
between three and five positives, so the benchmark expects several related
papers to appear near the top.

Representative topics include log mining for system management, search-result
visualization, distributed caching protocols, architectural experience from a
neurophysiological perspective, and robot control with gravity compensation.
The related documents can be conceptually or citation-related rather than
lexically similar to the title.

### BM25 Evaluation Profile

BM25 reaches nDCG@10 = 0.1335, hit@10 = 0.4250, and recall@100 = 0.2698 over
top-500 candidate lists. This low score is expected for citation-style
scientific retrieval. A paper can cite or recommend another paper because it
uses a related method, dataset, theoretical framing, or application area, even
if the title words differ substantially.

BM25 succeeds mainly when query and positive share distinctive technical terms.
It fails when the relation is methodological or bibliographic rather than
lexical. The all-multi-positive setup also makes it harder: finding one
overlapping abstract is not enough when several related papers should be
ranked.

### Dense Evaluation Profile

Dense retrieval with `harrier_oss_v1_270m` reaches nDCG@10 = 0.2264, hit@10 =
0.6400, and recall@100 = 0.4564. Dense retrieval is clearly stronger than BM25
because it can connect papers by topic, method, and contribution beyond exact
title overlap. It is the best candidate profile for top-ranked results in this
task.

The absolute score remains low, which shows how difficult scientific
recommendation is. A model must recognize relatedness among abstracts from the
same research area while distinguishing different methods and contributions.
Generic semantic similarity may still retrieve same-field papers that are not
among the judged positives.

### Reranking Hybrid Evaluation Profile

The `reranking_hybrid` candidate column reaches nDCG@10 = 0.1835, hit@10 =
0.5700, and recall@100 = 0.4280, with 100 to 101 candidates per query and 26
rank-101 safeguard rows. It improves over BM25 but trails dense retrieval.
This indicates that sparse lexical evidence adds some useful candidates but
also brings many title-term distractors that do not match the citation-style
relatedness relation.

For reranking, the hybrid pool is useful but not ideal as a final order. A
reranker must learn that shared title terms are weaker evidence than method,
problem, and citation-context similarity.

### Metric Interpretation for Model Researchers

Every query is multi-positive, so nDCG@10 and recall@100 should be read as
related-paper set retrieval metrics. Hit@10 is less informative by itself
because returning one related paper does not mean the system has captured the
recommended set. Multi-positive or listwise training is strongly aligned with
the benchmark.

The main lesson is that dense retrieval is essential here. BM25 is not a strong
proxy for scientific relatedness, and hybrid search only helps if a reranker
can suppress lexical but non-related scientific papers.

### Query and Relevance Type Tendencies

Queries are title-like scientific strings. Documents are paper records with
titles and abstracts. Relevance indicates scientific relatedness: cited papers,
co-cited papers, recommended papers, or papers that belong to the same research
neighborhood.

The model must infer relatedness from method, task, dataset, field, and
contribution. Exact word overlap is helpful but often insufficient.

### Representative Failure Modes

BM25 fails when related papers have different titles or use different
terminology for the same research area. Dense retrieval can fail by retrieving
broadly same-field papers that are not citation-related. Hybrid retrieval can
over-rank abstracts with shared title words but weak bibliographic relation.

Hard negatives should come from the same discipline or research problem but
use a different method or contribution.

### Training Data That May Help

Useful training data includes non-overlapping citation graph pairs, scientific
paper recommendation datasets, title-to-cited-paper and title-to-abstract
retrieval pairs, and multilingual scientific retrieval data with overlap
removed. Training should exclude SCIDOCS-NL evaluation titles, qrels, and
positive scientific documents used in this Nano split.

Synthetic data can create clusters of scientific titles and abstracts around a
shared method, dataset, or research problem. Each query title should have
several related-paper positives plus same-field hard negatives.

### Model Improvement Notes

Improving this task requires scientific document representations trained on
citation and recommendation signals. Dense encoders should model document-level
relatedness rather than only local sentence semantics. Rerankers should compare
methods, research problems, datasets, and contributions across title and
abstract text.

This task is a strong diagnostic for whether a model can support scientific
literature discovery in Dutch-translated settings.

## Example Data

### Public Sources

- [SPECTER: Document-level Representation Learning using Citation-informed Transformers](https://arxiv.org/abs/2004.07180), 2020.
- [BEIR: A Heterogeneous Benchmark for Zero-shot Evaluation of Information Retrieval Models](https://arxiv.org/abs/2104.08663), 2021.
- [MTEB-NL and E5-NL: Embedding Benchmark and Models for Dutch](https://arxiv.org/abs/2509.12340), 2025.
- [clips/beir-nl-scidocs](https://huggingface.co/datasets/clips/beir-nl-scidocs), source dataset card.

### Source Reference Table

| Title | Year | Type | URL |
| --- | ---: | --- | --- |
| SPECTER: Document-level Representation Learning using Citation-informed Transformers | 2020 | arXiv paper | https://arxiv.org/abs/2004.07180 |
| BEIR: A Heterogeneous Benchmark for Zero-shot Evaluation of Information Retrieval Models | 2021 | arXiv paper | https://arxiv.org/abs/2104.08663 |
| MTEB-NL and E5-NL: Embedding Benchmark and Models for Dutch | 2025 | arXiv paper | https://arxiv.org/abs/2509.12340 |
| clips/beir-nl-scidocs |  | dataset card | https://huggingface.co/datasets/clips/beir-nl-scidocs |

### Representative Snippets

| Query | Positive passage |
| --- | --- |
| Een geintegreerd raamwerk voor het delven van logbestanden voor systeembeheer. | A related scientific document discusses machine learning for automated text categorization and classification. |
| Onderwerp-Relevantiekaart: visualisatie voor verbetering van het begrip van zoekresultaten | A related document discusses exploratory search on touchscreen devices and result-list understanding. |
| Algoritmische brokjes in contentlevering | A related document discusses consistent hashing and distributed caching protocols for reducing web hotspots. |
| De enactieve benadering van architectonische ervaring | A related document discusses affective outcomes of virtual-reality exposure therapy for anxiety and phobias. |
| PD-regeling met online zwaartekrachtcompensatie voor robots met elastische gewrichten | A related document discusses Cartesian impedance control for robots with flexible joints. |
