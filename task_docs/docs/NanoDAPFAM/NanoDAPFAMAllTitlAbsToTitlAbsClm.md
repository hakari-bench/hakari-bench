# NanoDAPFAM / NanoDAPFAMAllTitlAbsToTitlAbsClm

## Overview

NanoDAPFAMAllTitlAbsToTitlAbsClm is an English patent-family retrieval task. The query contains a source patent family's title and abstract, while the target document contains title, abstract, and claims. Relevance is based on DAPFAM citation links under the ALL condition, including both same-domain and cross-domain patent-family relations.

This split tests summary-to-claim-rich retrieval. The query is concise, but the target exposes more detailed claim language. A model must use the query's summary-level invention description to find target families whose claims reveal related prior art or technical dependency.

## Details

### What the Original Data Measures

DAPFAM is a domain-aware family-level patent retrieval benchmark using citation links as qrels. It records title, abstract, claims, full text, IPC codes, and domain relations. This split keeps all relation types and varies only the source and target text fields.

The source field is title plus abstract, and the target field is title, abstract, and claims. This measures whether compact source summaries can retrieve more detailed claim-enriched target records.

### Observed Data Profile

This Nano split contains 200 queries, 10,000 documents, and 3,989 positive qrels. Every query has multiple positives, with an average of 19.95 positives per query, a minimum of 9, a median of 20.0, and a maximum of 20. Queries average 775.99 characters, and target documents average 7,230.59 characters.

The target claims add many technical details and legal formulations. This can help retrieval when the query's invention terms appear in target claims, but it can also introduce broad claim vocabulary that creates distractors.

### BM25 Evaluation Profile

BM25 reaches nDCG@10 of 0.3510, hit@10 of 0.8750, and recall@100 of 0.4294 with a top-500 candidate pool. It is stronger than the title-abstract target variant by recall, likely because target claims expose more matching technical terms.

BM25 still struggles with multi-positive coverage. A concise query may not contain enough terms to match every relevant target family, and claims often include repeated legal language that can inflate lexical similarity for non-relevant candidates.

### Dense Evaluation Profile

The dense harrier-oss-270m profile reaches nDCG@10 of 0.4056, hit@10 of 0.8850, and recall@100 of 0.5370. Dense retrieval improves over BM25 by matching summary-level intent to claim-level technical meaning.

Dense retrieval benefits from the richer target representation. Claims provide additional semantic evidence that short abstracts may omit. The remaining recall gap reflects the difficulty of representing long claim sets and many positives per query.

### Reranking Hybrid Evaluation Profile

The reranking_hybrid candidate subset is slightly strongest by nDCG@10, reaching 0.4088, with hit@10 of 0.8850 and recall@100 of 0.5367. It uses top-100 candidates with optional rank-101 safeguards; six rows contain 101 candidates and six safeguard-positive rows are recorded.

Dense and hybrid are effectively close. Hybrid adds exact claim-term matches to dense semantic similarity, improving nDCG slightly while matching dense hit@10. Recall is nearly identical.

### Metric Interpretation for Model Researchers

This is a hybrid-leaning summary-to-claims patent retrieval task. Target claims add useful detail, but they also add noise. The best systems must use claims selectively: exact technical elements matter, while boilerplate claim language should be discounted.

Because there are around 20 positives per query, recall@100 remains a central diagnostic. Finding one related family is easier than covering the broader cited family set.

### Query and Relevance Type Tendencies

Queries are title-abstract patent summaries. Documents contain title, abstract, and claims. Positives can be same-domain or cross-domain because this is an ALL split.

The target claims often include components, process steps, material constraints, or apparatus relationships that are not fully expressed in the target abstract alone.

### Representative Failure Modes

BM25 may over-rank targets that share claim terms without citation relevance. Dense retrieval may prefer semantically broad target families while missing specific cited families. Hybrid retrieval can still struggle when exact claim overlap conflicts with summary-level semantic similarity.

### Training Data That May Help

Useful training data includes title-abstract to claim-enriched patent retrieval, family-level citation retrieval, and prior-art search over patent records. Training should exclude NanoDAPFAM evaluation families, positives, qrels, and duplicate family publications.

Synthetic data should pair concise source title-abstract summaries with target patent records containing title, abstract, and numbered claims. Positives should be cited or technically related target families.

### Model Improvement Notes

Improving this task requires matching short invention summaries to detailed claim structures. Models should learn which claim elements express the same technical contribution and which are generic legal scaffolding.

For reranking, claim-element alignment, problem-solution matching, and domain-aware citation prediction are likely more useful than raw term overlap.

## Example Data

| Query | Positive document |
| --- | --- |
| snow removal equipment with automatic walking function the invention relates to snow removal equipment with an automatic walking function. the snow removal equipment comprises a walking module, a working module and a control module, wherein the walking module drives a snow removal machine to move; the working module comprises a working motor and a snow throwing mechanism driven by the working motor, and the snow throwing mechanism collects and throws out snows and occluded foreign substances on... [500 / 988 chars] | multifunctional device for clearing snow an apparatus and method for clearing an accumulation of matter from a surface that includes a blade configured to collect matter upon movement of the apparatus and means to shift the collected matter and distribute it laterally from the apparatus. the apparatus may include a plurality of helically arranged ribbons adjacent the blade formed such that the radial distance from a central axis decreases away from a center portion of the blade. a sealed rotor chamber may also include a rotor with blades that are adjustable in a radial direction or flared in both first and second rotational directions. claims what is claimed is: 1. an apparatus for clearing an accumulation of matter from a surface, including: a blade configured to collect matter upon movement of the apparatus, the blade including a central portion and lateral portions; a first ribbon and a second ribbon located adjacent the blade, the first ribbon and the second ribbon arranged helical... [1,000 / 12,229 chars] |
| modular intelligent transportation system a modular intelligent transportation system, comprising an environmentally protected enclosure, a system communications bus, a processor module, communicating with said bus, having a image data input and an audio input, the processor module analyzing the image data and/or audio input for data patterns represented therein, having at least one available option slot, a power supply, and a communication link for external communications, in which at least one... [500 / 708 chars] | impact media sharing an example operation includes one or more of associating a transport with an impact in proximity to one or more other transports, transmitting, by a device in proximity to the impact, media related to the impact, receiving, by a server, the media, determining, by the server, one or more sounds based on the media, and associating, by the server, the one or more sounds with one or more of the transport and the one or more other transports. 1. a method, comprising: determining, by a server, sounds based on media related to an impact of a transport by identifying a source and a direction of each of the one or more sounds; and associating, by the server, the sounds with other transports proximate the transport. 2. the method of claim 1 , comprising transmitting, by a device proximate the impact, the media, wherein the device is associated with one or more of the transport, the other transports, an occupant of the transport, and an occupant of the other transports. 3. th... [1,000 / 4,416 chars] |
| synthetic hollow microspheres this invention relates to a method of forming a synthetic hollow microsphere comprising the steps of preparing an agglomerate precursor, said agglomerate precursor including a primary component and a blowing agent; and firing the precursor at a predetermined temperature profile sufficient to seal the surface of the precursor and activate the blowing agent thereby forming a synthetic hollow microsphere, wherein the primary component comprises at lea st one aluminosil... [500 / 602 chars] | process for preparing metal-coated hollow microspheres a process for preparing a metal-coated hollow microsphere comprising the combination of steps of: (a) vigorously admixing a major quantity of hollow cenospheres/microspheres with a thermo-setting binder adhesive until the cenospheres are wet-out; (b) slowly adding metal flakes to the thus wet-out cenospheres of step (a) until the wet-out cenospheres are fully coated with the metal flakes; (c) binding the metal flakes to the said wet-out cenospheres by slowly increasing the temperature of the metal coated wet-out cenospheres from step (b), the temperature being raised up to about 350.degree. f.; and (d) the metal-coated cenospheres of step (c) are intermittently admixed in the absence of any further heating until dry. the dry product is ready for packaging. 1. a process for preparing metal-coated hollow microspheres comprising the combination of steps of: a) vigorously admixing a major quantity of hollow microspheres with a thermose... [1,000 / 4,174 chars] |

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
| A summary of automatic walking snow-removal equipment. | A title-abstract-claims target for related snow-clearing technology. |
| A summary of modular intelligent transportation infrastructure. | A claim-enriched target about impact media sharing for transports. |
| A summary of synthetic hollow microsphere formation. | A target with claims for preparing metal-coated hollow microspheres. |
| A summary of lightweight carpet tile. | A claim-enriched target for anti-static carpet materials. |
| A summary of lane-keeping steering integration. | A target with claims about steer torque management. |
