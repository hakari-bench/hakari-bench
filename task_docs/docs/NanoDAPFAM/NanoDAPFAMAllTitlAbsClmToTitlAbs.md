# NanoDAPFAM / NanoDAPFAMAllTitlAbsClmToTitlAbs

## Overview

NanoDAPFAMAllTitlAbsClmToTitlAbs is an English patent-family retrieval task. The query contains the title, abstract, and claims of a source patent family, while each target document contains only the title and abstract of a candidate family. Relevance is based on DAPFAM citation links under the ALL condition, including both same-domain and cross-domain patent-family relations.

This split tests whether a long, claim-heavy patent record can retrieve short patent summaries. Compared with the full-text target variant, the target documents contain far fewer lexical anchors, so the model must compress the query's claim language into the core technical concept and match it to concise title-abstract descriptions.

## Details

### What the Original Data Measures

DAPFAM is a domain-aware patent retrieval benchmark built at patent-family level. It uses citation links as relevance labels and tracks whether query and target families share IPC3 technical classes. The ALL condition keeps all cited or related families regardless of domain overlap.

This split focuses on long-query to short-document retrieval. The source representation includes claims, but the target representation is limited to title and abstract. It measures whether retrieval models can bridge detailed legal claim language and compact invention summaries.

### Observed Data Profile

This Nano split contains 200 queries, 10,000 documents, and 3,981 positive qrels. Every query has multiple positives, with an average of 19.91 positives per query, a minimum of 9, a median of 20.0, and a maximum of 20. Queries average 8,339.47 characters, while title-abstract documents average 777.90 characters.

The length asymmetry is substantial. Queries may include many numbered claims and component descriptions, while target documents give only a short invention summary. Examples include snow clearing, transportation systems, microspheres, carpet tiles, and steering systems.

### BM25 Evaluation Profile

BM25 reaches nDCG@10 of 0.2864, hit@10 of 0.8250, and recall@100 of 0.3587 with a top-500 candidate pool. The high hit@10 but low recall@100 shows that BM25 can often find at least one related family, but it misses many positives from the multi-positive relevance set.

Lexical matching is constrained by the short target representation. Many claim-level terms in the query do not appear in the title or abstract of the cited family. BM25 performs best when distinctive invention terms survive into the target abstract, and worse when relevance depends on technical dependency or paraphrase.

### Dense Evaluation Profile

The dense harrier-oss-270m profile is strongest, with nDCG@10 of 0.3997, hit@10 of 0.9000, and recall@100 of 0.5278. Dense retrieval improves substantially over BM25, indicating that semantic similarity helps bridge long claim text and short patent summaries.

Dense retrieval can connect a detailed claim set to a concise target abstract even when exact wording differs. It still misses many positives, which is expected because title-abstract targets omit much of the evidence that appears in full-text or claim representations.

### Reranking Hybrid Evaluation Profile

The reranking_hybrid candidate subset reaches nDCG@10 of 0.3767, hit@10 of 0.8850, and recall@100 of 0.5046. It uses top-100 candidates with optional rank-101 safeguards; eight rows contain 101 candidates and eight safeguard-positive rows are recorded. Dense retrieval is best for top ranking and recall, while hybrid is second.

This result suggests that adding BM25 evidence helps with exact terminology but does not fully compensate for short target documents. The most important signal is semantic compression from claims to summary-level patent descriptions.

### Metric Interpretation for Model Researchers

This is a dense-favored long-query to short-target patent retrieval task. Because every query has many positives, recall@100 is particularly important. BM25's low recall indicates that title-abstract targets do not expose enough matching terms for lexical search to cover the citation family set.

Researchers should compare this split with the full-text and title-abstract-claims target variants. The target field choice changes the retrieval problem: shorter targets reduce noise but also remove many useful anchors.

### Query and Relevance Type Tendencies

Queries include title, abstract, and claims. Documents include only title and abstract. Positives may come from any DAPFAM domain relation because this is an ALL split.

Relevant targets are concise summaries of patent families connected by citation-style technical relevance. A target can be relevant even when the abstract uses different terminology from the source claims.

### Representative Failure Modes

BM25 often misses positives whose target abstracts do not repeat claim terms. Dense retrieval may over-rank semantically broad summaries that resemble the query but lack citation-level relevance. Hybrid retrieval can inherit both issues when exact terms and semantic similarity point to different candidates.

Another failure mode is ambiguity in short abstracts. A target title and abstract may not expose enough detail to distinguish several related patent families.

### Training Data That May Help

Useful training data includes patent citation retrieval with claim-rich queries, title-abstract patent search pairs, and prior-art search examples outside NanoDAPFAM families. Training should exclude evaluation families, qrels, positives, and same-family duplicates.

Synthetic data should pair long source patent claims with concise target title-abstract records. Hard negatives should reuse terminology from the query claims but describe different inventions.

### Model Improvement Notes

Improving this task requires claim-to-summary alignment. Models should identify the central inventive concept in long claims and match it to compact target abstracts.

For reranking, useful evidence includes technical function, cited-family relation, component overlap, and whether the short abstract expresses the same problem-solution pattern as the source patent.

## Example Data

| Query | Positive document |
| --- | --- |
| snow removal equipment with automatic walking function the invention relates to snow removal equipme... [100 / 6,075 chars] | multifunctional device for clearing snow an apparatus and method for clearing an accumulation of matter from a surface that includes a blade configured to collect matter upon movement of the apparatus... [200 / 643 chars] |
| modular intelligent transportation system a modular intelligent transportation system, comprising an... [100 / 7,061 chars] | impact media sharing an example operation includes one or more of associating a transport with an impact in proximity to one or more other transports, transmitting, by a device in proximity to the imp... [200 / 462 chars] |
| synthetic hollow microspheres this invention relates to a method of forming a synthetic hollow micro... [100 / 8,392 chars] | process for preparing metal-coated hollow microspheres a process for preparing a metal-coated hollow microsphere comprising the combination of steps of: (a) vigorously admixing a major quantity of hol... [200 / 821 chars] |
| low weight carpet and carpet tile and methods of manufacture low weight and non-square carpet tile s... [100 / 3,799 chars] | anti-static mats and carpets a novel carpet material or mat which is characterized by an extraordinary ability to quickly and comfortably discharge any build-up of a static electricity charge on a per... [200 / 510 chars] |
| steering system with lane keeping integration a system for steering a vehicle including: an actuator... [100 / 5,360 chars] | steer torque manager for an advanced driver assistance system of a road vehicle a steer torque manager for an advanced driver assistance system of a road vehicle and a method therefor. a driver-in-the... [200 / 985 chars] |

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
| A snow-removal equipment family with walking, working, and control modules. | A title-abstract record for a multifunctional snow-clearing apparatus. |
| A modular intelligent transportation system with protected enclosure and bus modules. | A title-abstract record about media sharing around transport impacts. |
| A synthetic hollow microsphere formation method. | A title-abstract record about preparing metal-coated hollow microspheres. |
| A lightweight carpet tile for aircraft or mass-transit use. | A title-abstract record about anti-static mats and carpets. |
| A steering system with lane-keeping integration. | A title-abstract record about steer torque management in driver assistance. |
