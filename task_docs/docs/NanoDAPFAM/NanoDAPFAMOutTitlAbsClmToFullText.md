# NanoDAPFAM / NanoDAPFAMOutTitlAbsClmToFullText

## Overview

NanoDAPFAMOutTitlAbsClmToFullText is an English patent-family retrieval task. The query contains a source patent family's title, abstract, and claims, while the target document contains a candidate family's full text. Relevance is restricted to the DAPFAM OUT-domain condition, so positives are citation-related families that do not share IPC3 domain with the query family.

This is a difficult cross-domain prior-art retrieval task. The source query is long and claim-rich, but the relevant target may describe an analogous mechanism or technical dependency in a different patent class. The model must go beyond shared terminology and identify cross-domain patent relationships.

## Details

### What the Original Data Measures

DAPFAM is a family-level patent retrieval benchmark using citation links as qrels and IPC3 overlap to define domain relations. OUT-domain positives are citation-related families without shared IPC3 classes. This split uses title, abstract, and claims as the source representation and full patent text as the target representation.

The task measures cross-domain patent retrieval from detailed source claims to very long target documents. It is closer to technology-transfer or analogy retrieval than ordinary same-class prior-art search.

### Observed Data Profile

This Nano split contains 200 queries, 10,000 documents, and 1,259 positive qrels. There are 159 multi-positive queries. Positives per query average 6.30, with a minimum of 1, median of 4.0, and maximum of 20. Queries average 9,315.66 characters, and full-text target documents average 71,902.31 characters.

Compared with IN and ALL splits, the positive set is smaller and more cross-domain. The target full texts are extremely long, so relevant evidence may be buried in broad descriptions or claims from a different technical class.

### BM25 Evaluation Profile

BM25 is weak on this OUT split. It reaches nDCG@10 of 0.0461, hit@10 of 0.1750, and recall@100 of 0.1851 with a top-500 candidate pool. The low scores show that exact term overlap is a poor proxy for cross-domain citation relevance.

This is expected: OUT-domain positives often use different terminology from the source claims. BM25 may retrieve patents with shared words but not the cross-domain relationship, while true positives may describe similar functions using domain-specific vocabulary from another field.

### Dense Evaluation Profile

The dense harrier-oss-270m profile is strongest by top-rank metrics, with nDCG@10 of 0.1010, hit@10 of 0.3400, and recall@100 of 0.2701. Dense retrieval improves substantially over BM25, indicating that semantic similarity is essential for OUT-domain retrieval.

The absolute scores remain low. Cross-domain patent citation is hard because relevant links can be abstract, functional, or analogical rather than lexically obvious. Long full-text targets also dilute the relevant signal.

### Reranking Hybrid Evaluation Profile

The reranking_hybrid candidate subset reaches nDCG@10 of 0.0869, hit@10 of 0.2950, and recall@100 of 0.2716. It uses top-100 candidates with optional rank-101 safeguards; 65 rows contain 101 candidates and 65 safeguard-positive rows are recorded. Hybrid retrieval has slightly higher recall@100 than dense, but dense has better nDCG@10 and hit@10.

This means BM25 adds some candidates but also introduces noisy lexical distractors. Dense retrieval is the clearer top-rank signal, while hybrid can be useful for candidate coverage.

### Metric Interpretation for Model Researchers

This is one of the hardest NanoDAPFAM variants. The task is not about same-domain vocabulary; it is about identifying cross-domain patent relationships from claim-rich input. Low hit@10 and recall@100 should be expected relative to IN splits.

Researchers should treat recall@100 as a key diagnostic. Dense and hybrid recover only about a quarter of positives by rank 100, so there is substantial room for better cross-domain retrieval.

### Query and Relevance Type Tendencies

Queries include title, abstract, and claims. Documents are full patent texts. Positives are OUT-domain citation-related families, so they do not share IPC3 class with the query.

The relevant relationship may involve a shared mechanism, material behavior, control principle, manufacturing process, or problem-solution analogy across fields.

### Representative Failure Modes

BM25 retrieves documents that share claim words but remain in the wrong relation. Dense retrieval may find broad functional similarity without citation relevance. Hybrid retrieval can recover additional positives but is vulnerable to lexical noise from long full-text targets.

### Training Data That May Help

Useful training data includes cross-domain patent citation retrieval, prior-art search across different IPC classes, and technology analogy retrieval over patents. Training should exclude NanoDAPFAM evaluation families, positives, qrels, and family duplicates.

Synthetic data should pair source title-abstract-claims records with full-text patent records in different technical classes that share related mechanisms or technical effects.

### Model Improvement Notes

Improving this task requires cross-domain patent semantics. Models should learn functional analogy, technology transfer, and citation-style dependency beyond exact terminology.

For full-text targets, passage-level retrieval and evidence aggregation are likely important because the cross-domain connection may appear in a small part of the document.

## Example Data

| Query | Positive document |
| --- | --- |
| bicycle handlebar grip a bicycle handlebar grip contains a plastic inner shell having a tubular shape and an outer surface; a fiber layer having an inner surface and an outer surface and includes a plurality of fibers interweaving with each other and a plurality of weaving gaps located between the fibers; a plastic layer enclosed around the outer surface of the fiber layer and combined with the fiber layer integrally and including a holding portion coated on the outer surface of the fiber layer,... [500 / 2,588 chars] | durable flexible membrane and method of making same a flexible membrane having a valuable combination of desirable properties is composed of a generally heavy, dense supporting and reinforcing reticulated base fabric constituted of thick, generally loose bundles of multiple continuous filaments arranged in a mechanically interengated reticular array having an overall weight within the range of about 3-12 oz/yd.sup.2 the continuous filaments being of a synthetic polymer having good dimensional stability and high resistance to heat and light; and a solidified base coating composition completely impregnating the interstices of the base fabric and as forming a continuous coating along the opposite sides thereof, the composition having as essential ingredients a pvc resin and a plasticizer therefor in the amount of 35-75% of the resin of a trimellitate ester which exhibits high resistance to separation from the resin and imparts to the coating high flexibility at temperatures at least as lo... [1,000 / 28,042 chars] |
| method for improving belt press dewatering a method for increasing the removal of a higher fraction of liquid from the press cake in any belt press is described. specifically, the invention incorporates a series of rollers that create multiple pinch points to compress the solid fraction while removing liquid. after each pinch point, the solid material is allowed to separate from the belt, fall by gravity, and repack so that more liquid can be released at each successive pinch point than is possi... [500 / 4,605 chars] | artificial human anti-factor b antibody problem to be solved: to provide novel engineered forms of a monoclonal antibody and antigen-binding fragments thereof that bind complement protein factor b and selectively inhibit the alternative complement pathway.solution: artificial human anti-factor b antibodies or antigen-binding fragments thereof are derived from murine monoclonal antibody 1379 "mab1379", which selectively binds factor b in the third short consensus repeat ("scr") domain and prevents formation of the c3bbb complex. 1. a humaneered anti-factor b antibody or antigen-binding fragment thereof that selectively binds to factor b within the third short consensus repeat (“scr”) domain and prevents formation of the c3bbb complex, wherein the antibody comprises a v κ -region polypeptide comprising the amino acid sequence of seq id no: 16 and a v h -region polypeptide comprising the amino acid sequence of seq id no: 35. 2. the humaneered anti-factor b antibody or antigen-binding frag... [1,000 / 108,109 chars] |
| stitch distribution control system for tufting machines a stitch distribution control system for a tufting machine for controlling placement of yarns being fed to the needles of the tufting machine by yarn feed mechanisms to form a desired pattern. a backing material is fed through the tufting machine at an increased stitch rate as the needles are shifted according to calculated pattern steps. a series of loopers or hooks engage and pick loops of yarns from the needles. the yarn feed mechanisms... [500 / 5,968 chars] | method and apparatus for measuring direction or position of weft yarn of fabric the measurement of the pick or stitches course position in continuously moved fabrics involves examining at least one gap-shaped segment in a top illumination or transillumination. the width of the segment is small and its legnth long in comparison to the thickness of the picks. the brightness value inside the segment is divided into two stages or areas (light, dark). those sections within the segment, in which the value is continuously associated with one stage, are determined. the number or total length of the sections of s stage is determined or, alternatively the speed at which the sections of a stage move in the segment is determined and the drafting angle of the pick is deduced from this value. 1. a process for measuring the draft angle .alpha. of a weft thread in a travelling textile sheet which comprises: (a) intercepting light transmitted or reflected from a long narrow field of the travelling text... [1,000 / 24,253 chars] |

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
| A claim-rich source family in one IPC3 domain. | A full-text target family from another domain with a citation-style technical relationship. |
| A detailed apparatus claim set. | A cross-domain full-text family using an analogous mechanism or component relationship. |
| A source process patent with enumerated claim steps. | A full-text target from a different class with related process logic. |
| A material or device source patent. | A cross-domain target whose full text describes a related technical effect. |
| A source control or sensing system. | A full-text target from another field with a related control principle. |
