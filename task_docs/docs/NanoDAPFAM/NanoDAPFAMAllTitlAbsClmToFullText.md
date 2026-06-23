# NanoDAPFAM / NanoDAPFAMAllTitlAbsClmToFullText

## Overview

NanoDAPFAMAllTitlAbsClmToFullText is an English patent-family retrieval task. The query is the title, abstract, and claims of a source patent family, and the target document is the full-text representation of another patent family. Relevance comes from DAPFAM family-level citation links under the ALL condition, meaning both same-domain and cross-domain relations are included.

This task is useful for evaluating long-form prior-art retrieval. Queries are already claim-rich and technical, while targets are extremely long full patent texts. A model must identify cited or technically related families among documents with repeated legal phrasing, dense terminology, and many partially overlapping invention descriptions.

## Details

### What the Original Data Measures

DAPFAM is a domain-aware family-level patent retrieval benchmark. It aggregates patent publications into families, extracts fields such as title, abstract, claims, descriptions, IPC codes, and citations, and uses citation links as relevance judgments. The benchmark distinguishes IN-domain and OUT-domain relations by whether query and target families share IPC3 technical classes.

This split uses the ALL condition, so the relevance set includes both IN and OUT domain relations. It tests whether a title-abstract-claims source representation can retrieve full-text target patent families connected by citation-style technical relevance.

### Observed Data Profile

This Nano split contains 200 queries, 10,000 documents, and 3,989 positive qrels. Every query has multiple positives, with an average of 19.95 positives per query, a minimum of 9, a median of 20.0, and a maximum of 20. Queries average 8,339.47 characters, while full-text documents average 71,050.59 characters.

Observed examples include snow removal equipment, modular intelligent transportation systems, synthetic hollow microspheres, lightweight carpet tiles, and steering systems with lane-keeping integration. The text is patent-like, with titles, abstracts, claim lists, descriptions, and broad legal phrasing.

### BM25 Evaluation Profile

BM25 reaches nDCG@10 of 0.3365, hit@10 of 0.8150, and recall@100 of 0.4605 with a top-500 candidate pool. Lexical retrieval benefits from the long query and target texts: technical nouns, apparatus components, materials, process terms, and claim phrases provide many matching opportunities.

However, the task is difficult for BM25 because full patent texts are huge and repetitive. Many candidates contain similar legal formulae and broad technical vocabulary. Term frequency can identify related technology areas, but it may struggle to rank the most citation-relevant families among many documents with overlapping claim language.

### Dense Evaluation Profile

The dense harrier-oss-270m profile is strongest by nDCG@10, reaching 0.4352, with hit@10 of 0.8950 and recall@100 of 0.5793. Dense retrieval improves over BM25 by capturing semantic relatedness beyond exact wording, which matters when patents describe similar technical functions with different terminology.

Dense retrieval is still far from complete. Full-text patent documents are long, multi-topic, and noisy for fixed-size representations. The model needs to preserve the core invention concept while ignoring boilerplate, background sections, and incidental claim variants. Its advantage indicates useful semantic abstraction, but recall remains limited because each query has many positives.

### Reranking Hybrid Evaluation Profile

The reranking_hybrid candidate subset reaches nDCG@10 of 0.4215, hit@10 of 0.8950, and recall@100 of 0.5831. It uses top-100 candidates with optional rank-101 safeguards; six rows contain 101 candidates and six safeguard-positive rows are recorded. Hybrid retrieval has the best recall@100, while dense retrieval has slightly better nDCG@10.

This pattern shows that lexical and dense signals are complementary. BM25 contributes exact component and claim terminology, while dense retrieval contributes broader technical similarity. The hybrid pool is useful for downstream reranking because it recovers slightly more positives by rank 100, but dense scoring gives the strongest top-rank ordering in this split.

### Metric Interpretation for Model Researchers

This is a dense-favored but hybrid-useful long patent retrieval task. The main challenge is not finding one obvious answer; every query has around 20 positives. Metrics should be interpreted as multi-positive prior-art retrieval, where recall@100 measures how much of the citation family set is recovered.

The low recall values compared with hit@10 show that models often find at least one positive but miss many other relevant families. Improvements should target broader family coverage as well as top-rank precision.

### Query and Relevance Type Tendencies

Queries are long patent source records containing title, abstract, and claims. Documents are full-text patent-family records, including much more background and description text than the query. Relevance is citation-style family relatedness.

The ALL condition means positives can be same-domain or cross-domain by IPC3. This creates both lexical matches within similar technical classes and harder semantic matches across different domains.

### Representative Failure Modes

BM25 may retrieve documents with many shared claim words but weak citation relevance. Dense retrieval may retrieve semantically related families while missing exact component constraints. Hybrid retrieval can improve coverage but still rank broad same-domain documents above the most relevant cited families.

Full-text targets also create length-related failures. A relevant signal may be buried in a long document, while an irrelevant document may contain many matching terms spread across background sections.

### Training Data That May Help

Useful training data includes patent-family citation retrieval, prior-art search pairs with title, abstract, claims, and descriptions, and patent semantic search data outside the Nano evaluation families. Training should exclude NanoDAPFAM evaluation query families, positive target families, qrels, and near-duplicate patent family members.

Synthetic data should generate patent-family titles, abstracts, claims, and descriptions with citation-style related families. Positives should be cited or technically related families, while hard negatives should reuse terminology without sharing the same inventive contribution.

### Model Improvement Notes

Improving this task requires long-document patent representations that emphasize invention substance over boilerplate. Models should preserve claim elements, materials, apparatus components, process steps, and functional relationships.

For reranking, useful signals include citation-style dependency, shared technical effects, component-function alignment, and domain-aware treatment of IPC overlap. Chunking or late-interaction approaches may help full-text targets more than single-vector averaging.

## Example Data

| Query | Positive document |
| --- | --- |
| snow removal equipment with automatic walking function the invention relates to snow removal equipme... [100 / 6,075 chars] | multifunctional device for clearing snow an apparatus and method for clearing an accumulation of matter from a surface that includes a blade configured to collect matter upon movement of the apparatus... [200 / 59,310 chars] |
| modular intelligent transportation system a modular intelligent transportation system, comprising an... [100 / 7,061 chars] | impact media sharing an example operation includes one or more of associating a transport with an impact in proximity to one or more other transports, transmitting, by a device in proximity to the imp... [200 / 110,067 chars] |
| synthetic hollow microspheres this invention relates to a method of forming a synthetic hollow micro... [100 / 8,392 chars] | process for preparing metal-coated hollow microspheres a process for preparing a metal-coated hollow microsphere comprising the combination of steps of: (a) vigorously admixing a major quantity of hol... [200 / 19,034 chars] |
| low weight carpet and carpet tile and methods of manufacture low weight and non-square carpet tile s... [100 / 3,799 chars] | anti-static mats and carpets a novel carpet material or mat which is characterized by an extraordinary ability to quickly and comfortably discharge any build-up of a static electricity charge on a per... [200 / 17,195 chars] |
| steering system with lane keeping integration a system for steering a vehicle including: an actuator... [100 / 5,360 chars] | steer torque manager for an advanced driver assistance system of a road vehicle a steer torque manager for an advanced driver assistance system of a road vehicle and a method therefor. a driver-in-the... [200 / 44,337 chars] |

### Source Reference Table

| Source | Role |
| --- | --- |
| [DAPFAM: A Domain-Aware Family-level Dataset to benchmark cross domain patent retrieval](https://arxiv.org/abs/2506.22141) | Source benchmark paper for family-level patent retrieval. |
| [DAPFAM DOI record](https://doi.org/10.1016/j.array.2026.100720) | DOI record for the DAPFAM paper. |
| [datalyes/DAPFAM_patent](https://huggingface.co/datasets/datalyes/DAPFAM_patent) | Public source dataset card. |
| [hakari-bench/NanoDAPFAM](https://huggingface.co/datasets/hakari-bench/NanoDAPFAM) | Nano benchmark dataset containing this split. |

### Representative Snippets

| Query Pattern | Positive Document Pattern |
| --- | --- |
| A claim-rich snow-removal equipment family with automatic walking and control modules. | A full-text patent family about a multifunctional snow-clearing apparatus. |
| A modular intelligent transportation system with processor and communication modules. | A full-text family about impact media sharing and transportation-related sensing. |
| A method for forming synthetic hollow microspheres. | A full-text family about preparing metal-coated hollow microspheres. |
| A lightweight carpet or carpet tile for mass-transit vehicles. | A full-text family about anti-static mats and carpet materials. |
| A vehicle steering system integrating lane-keeping support. | A full-text family about steer torque management for advanced driver assistance. |
