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
| bicycle handlebar grip a bicycle handlebar grip contains a plastic inner shell having a tubular shape and an outer surface; a fiber layer having an inner surface and an outer surface and includes a plurality of fibers interweaving with each other and a plurality of weaving gaps located between the fibers; a plastic layer enclosed around the outer surface of the fiber layer and combined with the fiber layer integrally and including a holding portion coated on the outer surface of the fiber layer,... [500 / 2,588 chars] | durable flexible membrane and method of making same a flexible membrane having a valuable combination of desirable properties is composed of a generally heavy, dense supporting and reinforcing reticulated base fabric constituted of thick, generally loose bundles of multiple continuous filaments arranged in a mechanically interengated reticular array having an overall weight within the range of about 3-12 oz/yd.sup.2 the continuous filaments being of a synthetic polymer having good dimensional stability and high resistance to heat and light; and a solidified base coating composition completely impregnating the interstices of the base fabric and as forming a continuous coating along the opposite sides thereof, the composition having as essential ingredients a pvc resin and a plasticizer therefor in the amount of 35-75% of the resin of a trimellitate ester which exhibits high resistance to separation from the resin and imparts to the coating high flexibility at temperatures at least as lo... [1,000 / 7,657 chars] |
| method for improving belt press dewatering a method for increasing the removal of a higher fraction of liquid from the press cake in any belt press is described. specifically, the invention incorporates a series of rollers that create multiple pinch points to compress the solid fraction while removing liquid. after each pinch point, the solid material is allowed to separate from the belt, fall by gravity, and repack so that more liquid can be released at each successive pinch point than is possi... [500 / 4,605 chars] | artificial human anti-factor b antibody problem to be solved: to provide novel engineered forms of a monoclonal antibody and antigen-binding fragments thereof that bind complement protein factor b and selectively inhibit the alternative complement pathway.solution: artificial human anti-factor b antibodies or antigen-binding fragments thereof are derived from murine monoclonal antibody 1379 "mab1379", which selectively binds factor b in the third short consensus repeat ("scr") domain and prevents formation of the c3bbb complex. 1. a humaneered anti-factor b antibody or antigen-binding fragment thereof that selectively binds to factor b within the third short consensus repeat (“scr”) domain and prevents formation of the c3bbb complex, wherein the antibody comprises a v κ -region polypeptide comprising the amino acid sequence of seq id no: 16 and a v h -region polypeptide comprising the amino acid sequence of seq id no: 35. 2. the humaneered anti-factor b antibody or antigen-binding frag... [1,000 / 1,425 chars] |
| stitch distribution control system for tufting machines a stitch distribution control system for a tufting machine for controlling placement of yarns being fed to the needles of the tufting machine by yarn feed mechanisms to form a desired pattern. a backing material is fed through the tufting machine at an increased stitch rate as the needles are shifted according to calculated pattern steps. a series of loopers or hooks engage and pick loops of yarns from the needles. the yarn feed mechanisms... [500 / 5,968 chars] | method and apparatus for measuring direction or position of weft yarn of fabric the measurement of the pick or stitches course position in continuously moved fabrics involves examining at least one gap-shaped segment in a top illumination or transillumination. the width of the segment is small and its legnth long in comparison to the thickness of the picks. the brightness value inside the segment is divided into two stages or areas (light, dark). those sections within the segment, in which the value is continuously associated with one stage, are determined. the number or total length of the sections of s stage is determined or, alternatively the speed at which the sections of a stage move in the segment is determined and the drafting angle of the pick is deduced from this value. 1. a process for measuring the draft angle .alpha. of a weft thread in a travelling textile sheet which comprises: (a) intercepting light transmitted or reflected from a long narrow field of the travelling text... [1,000 / 5,290 chars] |

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
