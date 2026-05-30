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
| A compact source summary in one domain. | A claim-rich target family from another domain with citation relevance. |
| A short apparatus abstract. | A cross-domain target with detailed apparatus claims. |
| A short process abstract. | A claim-rich target describing related process steps in another class. |
| A material or device summary. | A cross-domain target with related material or device claims. |
| A control-system summary. | A target claim set from another field with analogous control behavior. |
