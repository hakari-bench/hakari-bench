# NanoMedical / NanoSciFact

## Overview

`NanoMedical / NanoSciFact` is an English scientific claim-evidence retrieval task derived from SciFact. Queries are atomic biomedical or scientific claims, and documents are research abstracts that contain evidence supporting or refuting those claims. The original SciFact benchmark was introduced for scientific claim verification, including abstract retrieval, support/refute classification, and rationale selection. This Nano split focuses on the retrieval component: given a claim, retrieve the abstract that contains the evidence. It is useful for evaluating whether retrieval models can connect compact scientific claims to evidence-bearing abstracts while preserving directionality, mechanism, population, and outcome details.

## Details

### What the Original Data Measures

SciFact measures scientific claim verification. Claims are written from scientific citation contexts, and abstracts are labeled according to whether they support, refute, or provide no information for the claim. The full task includes rationale identification, but this Nano task isolates the evidence-retrieval step.

The retrieval target is not a general paper about the same topic. A relevant abstract must contain evidence for or against the specific claim.

### Observed Data Profile

The Nano split contains 200 queries, 5,183 documents, and 226 positive qrel rows. Queries have 1.13 positives on average, with a median of 1 and a maximum of 5. There are 16 multi-positive queries, or 8.0% of the set. Queries average 90.07 characters, while documents average 1,499.41 characters.

The examples include claims about metastatic colorectal cancer treatment, CRP and CABG mortality, p150 and EB1 interaction, obesity genetics, and febrile seizures. Documents are long article-title plus abstract passages containing methods, results, and conclusions.

### BM25 Evaluation Profile

The BM25 candidate subset uses top-500 candidates and reaches nDCG@10 of 0.7017, hit@10 of 0.8650, and recall@100 of 0.9425. BM25 is strong because claims often include distinctive gene names, clinical terms, interventions, or outcomes that also appear in the evidence abstract.

The main difficulty is not finding the topic but matching the exact evidence relation. Same-topic abstracts may differ in direction, population, mechanism, or outcome. Sparse retrieval can over-rank an abstract that shares terminology but does not support or refute the claim.

### Dense Evaluation Profile

The dense candidate subset from `harrier_oss_v1_270m` uses top-500 candidates and reaches nDCG@10 of 0.7334, hit@10 of 0.8800, and recall@100 of 0.9336. Dense retrieval improves top-rank quality and hit rate over BM25, though BM25 has slightly higher recall@100.

This suggests that semantic matching helps rank evidence-bearing abstracts above same-topic negatives. Dense models still need to preserve fine-grained scientific directionality and not collapse all related abstracts together.

### Reranking Hybrid Evaluation Profile

The `reranking_hybrid` subset uses top-100 candidates, with 5 queries carrying a rank-101 safeguard positive. It reaches nDCG@10 of 0.7506, hit@10 of 0.8850, and recall@100 of 0.9779. This is the strongest overall profile, combining BM25's exact terminology coverage with dense retrieval's semantic ranking.

The hybrid result is well suited for downstream reranking and verification. It exposes nearly all positives while placing evidence abstracts early enough for a reranker to inspect.

### Metric Interpretation for Model Researchers

Most queries have one positive abstract, so nDCG@10 largely reflects whether the correct evidence abstract is ranked early. Recall@100 matters for evidence verification pipelines because the verifier cannot classify a claim if the evidence abstract is absent.

The strong hybrid profile shows that exact scientific terms and semantic relation matching are both valuable.

### Query and Relevance Type Tendencies

Queries are compact scientific claims with biomedical entities, mechanisms, interventions, associations, or clinical outcomes. Relevant documents are abstracts containing evidence for or against the claim.

The relevance relation is evidence sufficiency. A related paper is not enough unless it contains evidence bearing on the claim.

### Representative Failure Modes

Common failures include retrieving same-topic abstracts with the wrong outcome, missing negation or directionality, confusing related genes or pathways, and ignoring population or experimental condition differences. Sparse systems over-match terminology; dense systems may over-match broad semantic similarity.

### Training Data That May Help

Useful training data includes non-overlapping scientific claim-evidence pairs, biomedical citation-to-abstract retrieval data, SciFact-style rationale and verification data outside the evaluation split, and same-topic biomedical hard negatives. Training should exclude SciFact evaluation claims, positive abstracts, and near-duplicate claims derived from the same citances.

### Model Improvement Notes

Models should learn evidence relation, not just topic. Hard negatives should share disease, gene, intervention, or method terms while changing direction, condition, population, or outcome. Rerankers should be trained with support/refute-aware examples even if the retrieval metric itself is label-agnostic.

## Example Data

### Public Sources

- [Fact or Fiction: Verifying Scientific Claims](https://arxiv.org/abs/2004.14974), 2020.
- [SciFact ACL Anthology record](https://aclanthology.org/2020.emnlp-main.609/).

### Source Reference Table

| Title | Year | Type | URL |
| --- | ---: | --- | --- |
| Fact or Fiction: Verifying Scientific Claims | 2020 | arXiv paper | https://arxiv.org/abs/2004.14974 |
| Fact or Fiction: Verifying Scientific Claims | 2020 | ACL Anthology paper | https://aclanthology.org/2020.emnlp-main.609/ |

### Representative Snippets

| Query | Relevant document excerpt |
| --- | --- |
| Metastatic colorectal cancer treated with a single agent fluoropyrimidines resulted in reduced efficacy and lower quality of life when compared with oxaliplatin-based chemotherapy in elderly patients. | An abstract about chemotherapy options in elderly and frail patients with metastatic colorectal cancer. |
| CRP is not predictive of postoperative mortality following Coronary Artery Bypass Graft (CABG) surgery. | An abstract about prognostic biomarkers and prioritizing patients waiting for coronary artery surgery. |
| Arginine 90 in p150n is important for interaction with EB1. | An abstract about the EB1 and p150Glued complex and microtubule assembly. |
| Obesity is determined solely by environmental factors. | An abstract about an adoption study examining genetic effects on adult obesity. |
| Febrile seizures increase the threshold for development of epilepsy. | An abstract about febrile seizures and persistent modification of neuronal excitability. |
