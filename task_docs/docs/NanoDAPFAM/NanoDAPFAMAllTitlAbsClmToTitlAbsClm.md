# NanoDAPFAM / NanoDAPFAMAllTitlAbsClmToTitlAbsClm

## Overview

NanoDAPFAMAllTitlAbsClmToTitlAbsClm is an English patent-family retrieval task. Both query and target documents include title, abstract, and claims. Relevance comes from DAPFAM citation links under the ALL condition, so positives include both same-domain and cross-domain family relations.

This split is a claim-rich patent retrieval setting. Compared with title-abstract targets, candidate documents expose more technical and legal detail. Compared with full-text targets, they are much shorter and less noisy. The model must use claim language to identify related patent families without being misled by generic claim phrasing.

## Details

### What the Original Data Measures

DAPFAM benchmarks family-level patent retrieval using citation links and domain-aware IPC3 relations. It aggregates patents into families and represents them with fields such as titles, abstracts, claims, descriptions, and citations. The ALL condition keeps all citation positives, regardless of whether source and target share an IPC3 class.

This split evaluates title-abstract-claims to title-abstract-claims retrieval. It is a balanced field setting: both sides contain summaries and claims, so both lexical claim overlap and semantic invention similarity can contribute.

### Observed Data Profile

This Nano split contains 200 queries, 10,000 documents, and 3,989 positive qrels. Every query has multiple positives, with an average of 19.95 positives per query, a minimum of 9, a median of 20.0, and a maximum of 20. Queries average 8,339.47 characters, and target documents average 7,229.06 characters.

The observed examples include patents about snow removal, transportation systems, hollow microspheres, carpets, and vehicle steering. Both query and target sides include claim-style enumerations and technical component descriptions.

### BM25 Evaluation Profile

BM25 reaches nDCG@10 of 0.3360, hit@10 of 0.8550, and recall@100 of 0.4415 with a top-500 candidate pool. The score is higher than the title-abstract target variant because target claims provide additional lexical anchors. Shared components, materials, functional terms, and claim phrases can all help lexical retrieval.

BM25 still misses many positives because patent claims are repetitive and formal. Similar legal phrasing can appear across unrelated families, while citation-relevant families may describe related concepts using different claim structures.

### Dense Evaluation Profile

The dense harrier-oss-270m profile is strongest, with nDCG@10 of 0.4156, hit@10 of 0.8950, and recall@100 of 0.5530. Dense retrieval improves over BM25 by capturing technical relatedness across paraphrased claim language.

Dense retrieval benefits from having claims on both sides: the target contains enough technical detail to support semantic matching without the extreme length of full text. Still, multi-positive recall remains challenging because each source patent can cite many related families across different technical aspects.

### Reranking Hybrid Evaluation Profile

The reranking_hybrid candidate subset reaches nDCG@10 of 0.3989, hit@10 of 0.8900, and recall@100 of 0.5463. It uses top-100 candidates with optional rank-101 safeguards; seven rows contain 101 candidates and seven safeguard-positive rows are recorded. Dense retrieval is slightly stronger at the top and in recall, while hybrid is close.

The close dense-hybrid relationship indicates that exact claim terms and semantic similarity both matter. Hybrid retrieval helps recover candidates that one signal alone might miss, but dense retrieval remains the cleanest top-rank signal for this ALL split.

### Metric Interpretation for Model Researchers

This is a balanced claim-rich patent retrieval task. It is less sparse than title-abstract targets and less noisy than full-text targets. The metric pattern shows that dense retrieval is strongest, but BM25 is meaningful because both sides contain claims.

Because every query has around 20 positives, researchers should inspect both nDCG@10 and recall@100. A model may find one relevant family while missing many other cited families.

### Query and Relevance Type Tendencies

Queries and documents include title, abstract, and claims. The ALL condition includes both IN-domain and OUT-domain relations. Positives are citation-style related patent families, not necessarily duplicates or same-class patents.

Claim text tends to contain detailed components, steps, materials, and functional relationships. These features are useful but can also be repetitive across similar patent classes.

### Representative Failure Modes

BM25 may over-rank candidates with shared claim boilerplate. Dense retrieval may over-rank broad technical similarity without the citation-style dependency required by qrels. Hybrid retrieval can still struggle when lexical and semantic signals point to different aspects of a multi-positive query.

Another failure mode is domain mixing. In ALL retrieval, cross-domain positives may use different terminology, while same-domain negatives may look lexically closer.

### Training Data That May Help

Useful training data includes patent claim retrieval, family-level citation prediction, and prior-art search pairs with claim text. Training should exclude NanoDAPFAM evaluation query and target families and citation labels.

Synthetic data should generate patent titles, abstracts, and claims with related cited family records. Positives should be cited or technically dependent patent families, and hard negatives should share claim terminology without the same inventive relation.

### Model Improvement Notes

Improving this task requires claim-aware semantic retrieval. Models should preserve components, process steps, materials, and technical effects while reducing the influence of generic legal phrasing.

For reranking, useful signals include claim-element correspondence, problem-solution alignment, citation-likelihood, and domain-aware interpretation of IPC overlap.

## Example Data

| Query | Positive document |
| --- | --- |
| snow removal equipment with automatic walking function the invention relates to snow removal equipme... [100 / 6,075 chars] | multifunctional device for clearing snow an apparatus and method for clearing an accumulation of matter from a surface that includes a blade configured to collect matter upon movement of the apparatus... [200 / 12,229 chars] |
| modular intelligent transportation system a modular intelligent transportation system, comprising an... [100 / 7,061 chars] | impact media sharing an example operation includes one or more of associating a transport with an impact in proximity to one or more other transports, transmitting, by a device in proximity to the imp... [200 / 4,416 chars] |
| synthetic hollow microspheres this invention relates to a method of forming a synthetic hollow micro... [100 / 8,392 chars] | process for preparing metal-coated hollow microspheres a process for preparing a metal-coated hollow microsphere comprising the combination of steps of: (a) vigorously admixing a major quantity of hol... [200 / 4,174 chars] |
| low weight carpet and carpet tile and methods of manufacture low weight and non-square carpet tile s... [100 / 3,799 chars] | anti-static mats and carpets a novel carpet material or mat which is characterized by an extraordinary ability to quickly and comfortably discharge any build-up of a static electricity charge on a per... [200 / 3,680 chars] |
| steering system with lane keeping integration a system for steering a vehicle including: an actuator... [100 / 5,360 chars] | steer torque manager for an advanced driver assistance system of a road vehicle a steer torque manager for an advanced driver assistance system of a road vehicle and a method therefor. a driver-in-the... [200 / 9,884 chars] |

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
| A claim-rich snow-removal equipment source family. | A title-abstract-claims target family for snow-clearing apparatus technology. |
| A modular intelligent transportation source family. | A target family describing transportation impact media sharing. |
| A synthetic hollow microsphere source family. | A target family with claims for preparing metal-coated hollow microspheres. |
| A lightweight carpet tile source family. | A target family about anti-static mat or carpet materials. |
| A lane-keeping steering system source family. | A target family about steer torque management for driver assistance. |
