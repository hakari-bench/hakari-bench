# NanoDAPFAM / NanoDAPFAMAllTitlAbsToTitlAbs

## Overview

NanoDAPFAMAllTitlAbsToTitlAbs is an English patent-family retrieval task where both queries and target documents contain only patent titles and abstracts. Relevance comes from DAPFAM family-level citation links under the ALL condition, so positive families may be same-domain or cross-domain by IPC3.

This is the most compact ALL-field variant in NanoDAPFAM. It resembles summary-level patent search: the model must match concise invention descriptions, without relying on claims or full descriptions. The task is less noisy than full-text retrieval, but it also exposes much less evidence.

## Details

### What the Original Data Measures

DAPFAM measures family-level patent retrieval using citation links and domain-aware IPC3 relations. This split keeps all positives, regardless of domain overlap, and represents both source and target families with title plus abstract only.

The task measures whether short patent summaries are enough to recover citation-related families. It is a useful baseline for title-abstract retrieval before adding claims or full text.

### Observed Data Profile

This Nano split contains 200 queries, 10,000 documents, and 3,982 positive qrels. Every query is multi-positive, with an average of 19.91 positives per query, a minimum of 9, a median of 20.0, and a maximum of 20. Queries average 775.99 characters, and target documents average 777.99 characters.

Because query and document lengths are similar, this split has the cleanest field symmetry among the ALL variants. Both sides usually contain problem statements, invention summaries, and key technical terms.

### BM25 Evaluation Profile

BM25 reaches nDCG@10 of 0.3281, hit@10 of 0.8750, and recall@100 of 0.3908 with a top-500 candidate pool. Exact title and abstract terms are useful, and BM25 often finds at least one positive near the top.

The low recall@100 relative to hit@10 shows that title-abstract overlap cannot cover the full multi-positive citation set. Many relevant families do not repeat the same short summary vocabulary, especially across domains.

### Dense Evaluation Profile

The dense harrier-oss-270m profile reaches nDCG@10 of 0.3786, hit@10 of 0.8950, and recall@100 of 0.5068. Dense retrieval is stronger than BM25 because it can match related invention summaries even when terminology differs.

The improvement is meaningful but not complete. Abstracts are concise and may omit the detailed component relationships that explain citation relevance. Dense models must infer relatedness from high-level technical descriptions.

### Reranking Hybrid Evaluation Profile

The reranking_hybrid candidate subset reaches nDCG@10 of 0.3790, hit@10 of 0.8800, and recall@100 of 0.5020. It uses top-100 candidates with optional rank-101 safeguards; eight rows contain 101 candidates and eight safeguard-positive rows are recorded.

Dense and hybrid are nearly tied by nDCG, with dense slightly higher in hit@10 and recall. This suggests that lexical title-abstract overlap and semantic similarity provide overlapping rather than strongly complementary evidence in this compact split.

### Metric Interpretation for Model Researchers

This is a compact summary-to-summary patent retrieval task. BM25 is strong enough to find at least one related family, but dense retrieval and hybrid improve the ability to cover more of the citation set. The key challenge is multi-positive recall from short descriptions.

Researchers should use this split to test semantic patent-summary matching without the confounding effect of very long documents. It is a useful comparison point for the claim and full-text target variants.

### Query and Relevance Type Tendencies

Queries and documents are title-abstract records. Positives are cited or technically related patent families under the ALL condition. Same-domain positives may share terminology, while cross-domain positives may require more abstract problem-solution matching.

The short field format favors models that represent the main invention concept, not every claim detail.

### Representative Failure Modes

BM25 may miss positives that paraphrase the invention or use broader terminology. Dense retrieval may rank summaries from the same broad technology area above the cited family. Hybrid retrieval may not add much when lexical and semantic signals retrieve similar candidates.

### Training Data That May Help

Useful training data includes patent title-abstract citation retrieval, prior-art title-abstract search pairs, and family-level patent similarity data. Training should exclude NanoDAPFAM evaluation families and citation labels.

Synthetic data should create compact patent title and abstract records across technical fields, with positives that preserve citation-style technical relevance and hard negatives that are same-topic but non-cited.

### Model Improvement Notes

Improving this task requires high-quality patent summary representations. Models should capture the invention's technical problem, solution, field, and effect from a short abstract.

For reranking, citation-style relationship modeling and domain-aware comparison may help distinguish true positives from same-topic summaries.

## Example Data

| Query | Positive document |
| --- | --- |
| snow removal equipment with automatic walking function the invention relates to snow removal equipment with an automatic walking function. the snow removal equipment comprises a walking module, a working module and a control module, wherein the walking module drives a snow removal machine to move; the working module comprises a working motor and a snow throwing mechanism driven by the working motor, and the snow throwing mechanism collects and throws out snows and occluded foreign substances on... [500 / 988 chars] | multifunctional device for clearing snow an apparatus and method for clearing an accumulation of matter from a surface that includes a blade configured to collect matter upon movement of the apparatus and means to shift the collected matter and distribute it laterally from the apparatus. the apparatus may include a plurality of helically arranged ribbons adjacent the blade formed such that the radial distance from a central axis decreases away from a center portion of the blade. a sealed rotor chamber may also include a rotor with blades that are adjustable in a radial direction or flared in both first and second rotational directions. [643 chars] |
| modular intelligent transportation system a modular intelligent transportation system, comprising an environmentally protected enclosure, a system communications bus, a processor module, communicating with said bus, having a image data input and an audio input, the processor module analyzing the image data and/or audio input for data patterns represented therein, having at least one available option slot, a power supply, and a communication link for external communications, in which at least one... [500 / 708 chars] | impact media sharing an example operation includes one or more of associating a transport with an impact in proximity to one or more other transports, transmitting, by a device in proximity to the impact, media related to the impact, receiving, by a server, the media, determining, by the server, one or more sounds based on the media, and associating, by the server, the one or more sounds with one or more of the transport and the one or more other transports. [462 chars] |
| synthetic hollow microspheres this invention relates to a method of forming a synthetic hollow microsphere comprising the steps of preparing an agglomerate precursor, said agglomerate precursor including a primary component and a blowing agent; and firing the precursor at a predetermined temperature profile sufficient to seal the surface of the precursor and activate the blowing agent thereby forming a synthetic hollow microsphere, wherein the primary component comprises at lea st one aluminosil... [500 / 602 chars] | process for preparing metal-coated hollow microspheres a process for preparing a metal-coated hollow microsphere comprising the combination of steps of: (a) vigorously admixing a major quantity of hollow cenospheres/microspheres with a thermo-setting binder adhesive until the cenospheres are wet-out; (b) slowly adding metal flakes to the thus wet-out cenospheres of step (a) until the wet-out cenospheres are fully coated with the metal flakes; (c) binding the metal flakes to the said wet-out cenospheres by slowly increasing the temperature of the metal coated wet-out cenospheres from step (b), the temperature being raised up to about 350.degree. f.; and (d) the metal-coated cenospheres of step (c) are intermittently admixed in the absence of any further heating until dry. the dry product is ready for packaging. [821 chars] |

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
| A title-abstract record for automatic walking snow-removal equipment. | A title-abstract record for a related snow-clearing apparatus. |
| A title-abstract record for modular intelligent transportation. | A title-abstract record for impact media sharing in transportation. |
| A title-abstract record for synthetic hollow microspheres. | A title-abstract record for metal-coated hollow microspheres. |
| A title-abstract record for lightweight carpet tile. | A title-abstract record for anti-static carpet or mat technology. |
| A title-abstract record for lane-keeping steering. | A title-abstract record for steering torque management. |
