# NanoDAPFAM / NanoDAPFAMInTitlAbsClmToTitlAbsClm

## Overview

NanoDAPFAMInTitlAbsClmToTitlAbsClm is an English patent-family retrieval task where both query and target records contain title, abstract, and claims. Relevance is restricted to DAPFAM IN-domain positives, so positive target families are citation-related and share IPC3 technical class with the source family.

This is a same-domain, claim-rich patent retrieval task. Both sides expose detailed claim language, making lexical overlap useful, but same-domain distractors can be very similar. The model must distinguish cited families from merely related patents in the same technical area.

## Details

### What the Original Data Measures

DAPFAM benchmarks patent retrieval at family level using citation links. It marks IN-domain relations when query and target families share IPC3 domain. This split uses title, abstract, and claims on both sides, so it emphasizes claim-aware in-domain prior-art retrieval.

The task measures whether models can retrieve citation-related families when both relevant and non-relevant candidates may share technical field and claim vocabulary.

### Observed Data Profile

This Nano split contains 200 queries, 10,000 documents, and 3,069 positive qrels. There are 194 multi-positive queries, with an average of 15.35 positives per query, a minimum of 1, median of 18.0, and maximum of 20. Queries average 8,405.46 characters, and target documents average 7,225.19 characters.

Both sides are claim-rich but not full-text length. This gives retrieval models substantial technical evidence while avoiding the extreme noise of full descriptions.

### BM25 Evaluation Profile

BM25 reaches nDCG@10 of 0.3473, hit@10 of 0.8450, and recall@100 of 0.5357 with a top-500 candidate pool. Because both query and target include claims, exact component names, process steps, and functional terms can match directly.

BM25 still trails dense retrieval because shared claim vocabulary is common among same-domain families. Lexical overlap can indicate technical class but not necessarily citation relevance.

### Dense Evaluation Profile

The dense harrier-oss-270m profile is strongest, with nDCG@10 of 0.4325, hit@10 of 0.8950, and recall@100 of 0.6716. Dense retrieval improves over BM25 by recognizing technical dependency and paraphrased claim relationships inside the same domain.

The result suggests that semantic similarity remains important even when exact claim terms are available on both sides. Dense retrieval better covers the multi-positive relevance set.

### Reranking Hybrid Evaluation Profile

The reranking_hybrid candidate subset reaches nDCG@10 of 0.4157, hit@10 of 0.8900, and recall@100 of 0.6579. It uses top-100 candidates with optional rank-101 safeguards; seven rows contain 101 candidates and seven safeguard-positive rows are recorded. Hybrid retrieval is close to dense but slightly lower.

The hybrid profile shows that BM25 terms are useful but can also introduce same-domain distractors. Dense retrieval remains the strongest top-rank and recall signal in this split.

### Metric Interpretation for Model Researchers

This is a dense-favored but lexically meaningful same-domain patent task. BM25 has stronger recall here than in short target variants because claims appear on both sides. Dense retrieval still improves top ranking and positive coverage.

The task is useful for testing whether models can rank inside dense technical neighborhoods. The challenge is not broad domain identification; it is citation-level distinction among patents in the same IPC3 area.

### Query and Relevance Type Tendencies

Queries and documents contain title, abstract, and claims. Positives are same-domain cited families. Claim text contains component lists, process steps, materials, apparatus limitations, and functional effects.

### Representative Failure Modes

BM25 may retrieve patents with matching claim vocabulary but different inventive contribution. Dense retrieval may rank technically similar but non-cited families above positives. Hybrid retrieval can inherit both errors when exact claim overlap and broad semantic similarity reinforce a distractor.

### Training Data That May Help

Useful training data includes same-domain patent claim retrieval, IPC-restricted citation prediction, and prior-art search with claims. Training should exclude NanoDAPFAM evaluation families, positives, and qrels.

Synthetic data should generate same-domain patent title-abstract-claims records, with positives that are cited same-domain families and hard negatives that share claim vocabulary without citation relation.

### Model Improvement Notes

Improving this task requires claim-aware in-domain reranking. Models should compare claim elements, technical effects, and problem-solution relationships, not just IPC class or shared terminology.

Late-interaction and claim-element alignment approaches may be useful because relevant evidence often appears in specific claim clauses.

## Example Data

| Query | Positive document |
| --- | --- |
| snow removal equipment with automatic walking function the invention relates to snow removal equipme... [100 / 6,075 chars] | multifunctional device for clearing snow an apparatus and method for clearing an accumulation of matter from a surface that includes a blade configured to collect matter upon movement of the apparatus... [200 / 12,229 chars] |
| apparatus for indication of at least one subsurface barrier characteristic and methods of use a cont... [100 / 11,428 chars] | method of confirming position of drain material left and apparatus for confirming same in drain engineering method a method and apparatus is provided to embed paper drain material in water-laden soil... [200 / 6,762 chars] |
| an article including identification for use in an electrically heated smoking system. there is provi... [100 / 5,076 chars] | apparatus for generating aerosol from an aerosolisable medium, an article of aerosolisable medium and a method of determining a parameter of an article to provide an apparatus that heats an aerosoliza... [200 / 5,466 chars] |
| low weight carpet and carpet tile and methods of manufacture low weight and non-square carpet tile s... [100 / 3,799 chars] | anti-static mats and carpets a novel carpet material or mat which is characterized by an extraordinary ability to quickly and comfortably discharge any build-up of a static electricity charge on a per... [200 / 3,680 chars] |
| organosilicon precursors for interlayer dielectric films with low dielectric constants a method of f... [100 / 11,588 chars] | radiation shield a radiation shield and an assembly and a reactor including the radiation shield are disclosed. the radiation shield can be used to control heat flux from a susceptor heater assembly a... [200 / 4,267 chars] |

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
| A title-abstract-claims source family in a specific IPC3 area. | A cited same-domain target family represented with title, abstract, and claims. |
| A claim-rich apparatus patent. | A target claim set for a related same-domain apparatus. |
| A claim-rich process or method patent. | A cited target family with corresponding process claims. |
| A source material or composition patent. | A same-domain target with related composition claims. |
| A source control-system patent. | A cited target family with related control or actuation claims. |
