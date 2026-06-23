# NanoDAPFAM / NanoDAPFAMOutTitlAbsClmToTitlAbsClm

## Overview

NanoDAPFAMOutTitlAbsClmToTitlAbsClm is an English patent-family retrieval task. Both queries and targets contain title, abstract, and claims, while relevance is restricted to DAPFAM OUT-domain citation relations. Positive target families are technically related but do not share IPC3 domain with the source.

This split tests cross-domain claim-to-claim retrieval. Claims provide more technical evidence than abstracts, but the lack of shared IPC3 domain means relevant families may use different terminology. The task is a hard benchmark for patent analogy and technology-transfer retrieval.

## Details

### What the Original Data Measures

DAPFAM evaluates family-level patent retrieval using citation labels and domain relations. OUT-domain relations identify citation-positive families outside the source's IPC3 technical class. This split represents both sides with title, abstract, and claims.

The task measures whether claim-rich semantic matching can recover cross-domain cited families when both source and target provide detailed but domain-specific legal and technical language.

### Observed Data Profile

This Nano split contains 200 queries, 10,000 documents, and 1,259 positive qrels. There are 159 multi-positive queries. Positives per query average 6.30, with a minimum of 1, median of 4.0, and maximum of 20. Queries average 9,315.66 characters, and target documents average 7,257.21 characters.

The field lengths are balanced and claim-rich, but cross-domain vocabulary mismatch remains substantial.

### BM25 Evaluation Profile

BM25 reaches nDCG@10 of 0.0640, hit@10 of 0.2400, and recall@100 of 0.1684 with a top-500 candidate pool. It is stronger here than in the title-abstract target OUT variant because target claims add more lexical anchors.

Even so, BM25 remains weak. Cross-domain positives may share mechanisms or functions without sharing many exact terms. Claim boilerplate also creates false matches among non-relevant targets.

### Dense Evaluation Profile

The dense harrier-oss-270m profile is strongest by nDCG@10 and recall, reaching nDCG@10 of 0.0952, hit@10 of 0.3100, and recall@100 of 0.2462. Dense retrieval captures more cross-domain relevance than BM25 by abstracting over terminology.

The scores remain low because cross-domain patent relevance is subtle. A model must compare technical effects and claim structure across different domains, not just topical similarity.

### Reranking Hybrid Evaluation Profile

The reranking_hybrid candidate subset reaches nDCG@10 of 0.0811, hit@10 of 0.3100, and recall@100 of 0.2423. It uses top-100 candidates with optional rank-101 safeguards; 72 rows contain 101 candidates and 72 safeguard-positive rows are recorded. Dense and hybrid tie on hit@10, but dense is better by nDCG and recall.

The hybrid profile suggests that BM25 adds some useful claim-term candidates but also adds noise. Dense retrieval remains the best first signal for cross-domain claim matching.

### Metric Interpretation for Model Researchers

This is a difficult cross-domain patent retrieval task with claim-rich evidence on both sides. Scores are much lower than IN-domain variants, showing that shared IPC vocabulary is a major advantage in patent retrieval. OUT-domain retrieval requires more abstract technical reasoning.

The target claims improve lexical and dense matching relative to title-abstract targets, but not enough to make the task easy. Candidate recall remains a major bottleneck.

### Query and Relevance Type Tendencies

Queries and documents contain title, abstract, and claims. Positives are citation-related families outside the source IPC3 domain. Relevance may be based on functional equivalence, transferred mechanism, materials behavior, or analogous control/process structure.

### Representative Failure Modes

BM25 retrieves claim-rich targets with shared formal language but no cross-domain relevance. Dense retrieval retrieves broad technical analogies that are not citation positives. Hybrid retrieval can tie hit@10 with dense but rank positives lower due to lexical distractors.

### Training Data That May Help

Useful training data includes cross-domain patent claim retrieval, cross-IPC citation prediction, and patent technology-transfer retrieval. Training should exclude NanoDAPFAM evaluation families and qrels.

Synthetic data should create claim-rich patent records from different technical classes, with positives that are cited cross-domain patent families and hard negatives that share either function or vocabulary without citation relation.

### Model Improvement Notes

Improving this task requires models that compare claim elements across domains. Useful representations should capture function, mechanism, technical effect, and problem-solution structure even when field terminology changes.

For reranking, claim-element alignment and citation-graph-aware training may be more effective than lexical overlap alone.

## Example Data

| Query | Positive document |
| --- | --- |
| bicycle handlebar grip a bicycle handlebar grip contains a plastic inner shell having a tubular shap... [100 / 2,588 chars] | durable flexible membrane and method of making same a flexible membrane having a valuable combination of desirable properties is composed of a generally heavy, dense supporting and reinforcing reticul... [200 / 7,657 chars] |
| method for improving belt press dewatering a method for increasing the removal of a higher fraction... [100 / 4,605 chars] | artificial human anti-factor b antibody problem to be solved: to provide novel engineered forms of a monoclonal antibody and antigen-binding fragments thereof that bind complement protein factor b and... [200 / 1,425 chars] |
| stitch distribution control system for tufting machines a stitch distribution control system for a t... [100 / 5,968 chars] | method and apparatus for measuring direction or position of weft yarn of fabric the measurement of the pick or stitches course position in continuously moved fabrics involves examining at least one ga... [200 / 5,290 chars] |
| low weight carpet and carpet tile and methods of manufacture low weight and non-square carpet tile s... [100 / 3,799 chars] | modular floor covering units with built-in lighting an apparatus for guiding the occupants of a structure along a path of travel within the structure is provided. the apparatus is comprised of modular... [200 / 17,660 chars] |
| method and apparatus for the zonal transmission of data using building lighting fixtures this invent... [100 / 7,344 chars] | shelf tag with ambient light detector the present invention relates to an electronic shelf display device which includes an optical device and an ambient light detector circuitry. the electronic shelf... [200 / 7,219 chars] |

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
| A claim-rich source family in one technical domain. | A claim-rich target family in another domain with citation-style relevance. |
| A detailed apparatus claim set. | A cross-domain target claim set with analogous mechanism. |
| A process or method claim set. | A target from another class with related technical steps. |
| A material or device claim set. | A cross-domain claim set describing related effects or structures. |
| A control-system claim set. | A target claim set from another field with analogous control behavior. |
