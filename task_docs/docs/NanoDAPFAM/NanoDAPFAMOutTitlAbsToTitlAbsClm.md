# NanoDAPFAM / NanoDAPFAMOutTitlAbsToTitlAbsClm

## Overview

NanoDAPFAMOutTitlAbsToTitlAbsClm is an English patent-family retrieval task. The query contains a source patent family's title and abstract, while target documents contain title, abstract, and claims. Positives are DAPFAM OUT-domain citation relations, so relevant target families do not share IPC3 domain with the source.

This split tests compact-query to claim-rich cross-domain retrieval. Target claims provide more technical evidence than abstracts, but they also use terminology from a different technical field. A strong model must identify cross-domain relevance from short source summaries and detailed target claims.

## Details

### What the Original Data Measures

DAPFAM benchmarks patent-family retrieval with citation qrels and domain-aware IPC3 labels. OUT-domain positives are cited families outside the source's IPC3 domain. This split uses title-abstract source queries and title-abstract-claims target documents.

The task measures whether claim-rich target representations help recover cross-domain cited families from compact source summaries.

### Observed Data Profile

This Nano split contains 200 queries, 10,000 documents, and 1,259 positive qrels. There are 159 multi-positive queries. Positives per query average 6.30, with a minimum of 1, median of 4.0, and maximum of 20. Queries average 786.61 characters, and target documents average 7,257.21 characters.

The target claims add technical detail but also legal boilerplate and domain-specific vocabulary.

### BM25 Evaluation Profile

BM25 reaches nDCG@10 of 0.0699, hit@10 of 0.2450, and recall@100 of 0.1708 with a top-500 candidate pool. This is better than the title-abstract target variant, because target claims provide more terms that may overlap with the source summary.

Still, BM25 remains weak. Cross-domain relevance often depends on function or mechanism rather than exact vocabulary, and claim text can introduce many misleading matches.

### Dense Evaluation Profile

The dense harrier-oss-270m profile reaches nDCG@10 of 0.0909, hit@10 of 0.3150, and recall@100 of 0.2311. Dense retrieval is stronger than BM25 by matching semantic relationships across domains.

The task remains hard because the short query may not contain enough information to identify which target claim set is citation-relevant.

### Reranking Hybrid Evaluation Profile

The reranking_hybrid candidate subset reaches nDCG@10 of 0.0901, hit@10 of 0.3100, and recall@100 of 0.2335. It uses top-100 candidates with optional rank-101 safeguards; 76 rows contain 101 candidates and 76 safeguard-positive rows are recorded. Dense and hybrid are nearly tied, with hybrid slightly higher in recall and dense slightly higher in nDCG and hit.

This shows that exact target claim terms add some coverage, but dense semantic matching remains the primary signal.

### Metric Interpretation for Model Researchers

This is a difficult cross-domain patent retrieval task where target claims help but do not solve the problem. Compared with title-abstract targets, claims expose more evidence. Compared with IN-domain variants, vocabulary shift keeps all scores low.

Researchers should focus on candidate recall and top-rank precision together. Many positives are absent from natural top-100 pools without safeguards.

### Query and Relevance Type Tendencies

Queries are title-abstract summaries. Documents contain title, abstract, and claims. Positives are citation-related families outside the source IPC3 domain.

The relevant relationship may be an analogy between mechanisms, a transferred process, a related material effect, or a functional dependency across technical fields.

### Representative Failure Modes

BM25 retrieves claim-rich targets with superficial overlap. Dense retrieval retrieves broad cross-domain similarity but not necessarily citation positives. Hybrid retrieval is close to dense but may rank lexical distractors highly.

### Training Data That May Help

Useful training data includes cross-domain summary-to-claims patent retrieval, cross-IPC citation prediction, and patent analogy retrieval with hard negatives. Training should exclude NanoDAPFAM evaluation family IDs, positives, qrels, and duplicate family publications.

Synthetic data should use compact source patent summaries and claim-rich target records from different technical classes, with positives based on cross-domain citations.

### Model Improvement Notes

Improving this task requires summary-to-claim alignment across domains. Models should compare technical effects and functional roles rather than only surface claim terms.

For reranking, claim-element abstraction and cross-domain hard-negative training are likely important.

## Example Data

| Query | Positive document |
| --- | --- |
| bicycle handlebar grip a bicycle handlebar grip contains a plastic inner shell having a tubular shape and an outer surface; a fiber layer having an inner surface and an outer surface and includes a plurality of fibers interweaving with each other and a plurality of weaving gaps located between the fibers; a plastic layer enclosed around the outer surface of the fiber layer and combined with the fiber layer integrally and including a holding portion coated on the outer surface of the fiber layer,... [500 / 821 chars] | durable flexible membrane and method of making same a flexible membrane having a valuable combination of desirable properties is composed of a generally heavy, dense supporting and reinforcing reticulated base fabric constituted of thick, generally loose bundles of multiple continuous filaments arranged in a mechanically interengated reticular array having an overall weight within the range of about 3-12 oz/yd.sup.2 the continuous filaments being of a synthetic polymer having good dimensional stability and high resistance to heat and light; and a solidified base coating composition completely impregnating the interstices of the base fabric and as forming a continuous coating along the opposite sides thereof, the composition having as essential ingredients a pvc resin and a plasticizer therefor in the amount of 35-75% of the resin of a trimellitate ester which exhibits high resistance to separation from the resin and imparts to the coating high flexibility at temperatures at least as lo... [1,000 / 7,657 chars] |
| method for improving belt press dewatering a method for increasing the removal of a higher fraction of liquid from the press cake in any belt press is described. specifically, the invention incorporates a series of rollers that create multiple pinch points to compress the solid fraction while removing liquid. after each pinch point, the solid material is allowed to separate from the belt, fall by gravity, and repack so that more liquid can be released at each successive pinch point than is possi... [500 / 620 chars] | artificial human anti-factor b antibody problem to be solved: to provide novel engineered forms of a monoclonal antibody and antigen-binding fragments thereof that bind complement protein factor b and selectively inhibit the alternative complement pathway.solution: artificial human anti-factor b antibodies or antigen-binding fragments thereof are derived from murine monoclonal antibody 1379 "mab1379", which selectively binds factor b in the third short consensus repeat ("scr") domain and prevents formation of the c3bbb complex. 1. a humaneered anti-factor b antibody or antigen-binding fragment thereof that selectively binds to factor b within the third short consensus repeat (“scr”) domain and prevents formation of the c3bbb complex, wherein the antibody comprises a v κ -region polypeptide comprising the amino acid sequence of seq id no: 16 and a v h -region polypeptide comprising the amino acid sequence of seq id no: 35. 2. the humaneered anti-factor b antibody or antigen-binding frag... [1,000 / 1,425 chars] |
| stitch distribution control system for tufting machines a stitch distribution control system for a tufting machine for controlling placement of yarns being fed to the needles of the tufting machine by yarn feed mechanisms to form a desired pattern. a backing material is fed through the tufting machine at an increased stitch rate as the needles are shifted according to calculated pattern steps. a series of loopers or hooks engage and pick loops of yarns from the needles. the yarn feed mechanisms... [500 / 647 chars] | method and apparatus for measuring direction or position of weft yarn of fabric the measurement of the pick or stitches course position in continuously moved fabrics involves examining at least one gap-shaped segment in a top illumination or transillumination. the width of the segment is small and its legnth long in comparison to the thickness of the picks. the brightness value inside the segment is divided into two stages or areas (light, dark). those sections within the segment, in which the value is continuously associated with one stage, are determined. the number or total length of the sections of s stage is determined or, alternatively the speed at which the sections of a stage move in the segment is determined and the drafting angle of the pick is deduced from this value. 1. a process for measuring the draft angle .alpha. of a weft thread in a travelling textile sheet which comprises: (a) intercepting light transmitted or reflected from a long narrow field of the travelling text... [1,000 / 5,290 chars] |

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
| A compact source summary in one domain. | A claim-rich target family from another domain with citation relevance. |
| A short apparatus abstract. | A cross-domain target with detailed apparatus claims. |
| A short process abstract. | A claim-rich target describing related process steps in another class. |
| A material or device summary. | A cross-domain target with related material or device claims. |
| A control-system summary. | A target claim set from another field with analogous control behavior. |
