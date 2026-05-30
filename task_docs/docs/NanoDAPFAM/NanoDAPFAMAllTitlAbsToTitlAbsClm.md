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

### Public Sources

NanoDAPFAM is documented through the DAPFAM paper and the public DAPFAM patent dataset card.

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
