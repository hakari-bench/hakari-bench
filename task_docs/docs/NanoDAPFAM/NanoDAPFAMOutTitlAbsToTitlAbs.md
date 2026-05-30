# NanoDAPFAM / NanoDAPFAMOutTitlAbsToTitlAbs

## Overview

NanoDAPFAMOutTitlAbsToTitlAbs is an English patent-family retrieval task where both source queries and target documents contain only title and abstract. Positives are DAPFAM OUT-domain citation relations, so target families are technically related but do not share IPC3 domain with the query family.

This is the most compact cross-domain DAPFAM split. It asks whether short patent summaries can retrieve other short summaries from different technical fields. The task is hard because both detailed claims and full descriptions are absent.

## Details

### What the Original Data Measures

DAPFAM uses family-level citation links as qrels and IPC3 overlap to define domain relations. OUT-domain positives are cited families outside the query's IPC3 domain. This split uses title and abstract fields for both source and target families.

The task measures cross-domain patent-summary retrieval, where the relevant relationship must be inferred from concise descriptions.

### Observed Data Profile

This Nano split contains 200 queries, 10,000 documents, and 1,257 positive qrels. There are 159 multi-positive queries. Positives per query average 6.29, with a minimum of 1, median of 4.0, and maximum of 20. Queries average 786.61 characters, and documents average 777.94 characters.

The field symmetry removes long-document noise but also removes much of the evidence that could explain cross-domain relevance.

### BM25 Evaluation Profile

BM25 reaches nDCG@10 of 0.0583, hit@10 of 0.1750, and recall@100 of 0.1527 with a top-500 candidate pool. The low score shows that exact title and abstract overlap is a weak signal for cross-domain citation retrieval.

BM25 may find candidates with similar words, but OUT-domain positives often use different domain vocabularies for related mechanisms or effects.

### Dense Evaluation Profile

The dense harrier-oss-270m profile is strongest by top-rank metrics, with nDCG@10 of 0.0872, hit@10 of 0.3150, and recall@100 of 0.2045. Dense retrieval improves over BM25 by matching abstract technical meaning across domains.

The score remains modest because title-abstract text alone may not expose enough detail to identify cross-domain citation relevance.

### Reranking Hybrid Evaluation Profile

The reranking_hybrid candidate subset reaches nDCG@10 of 0.0762, hit@10 of 0.2650, and recall@100 of 0.2188. It uses top-100 candidates with optional rank-101 safeguards; 76 rows contain 101 candidates and 76 safeguard-positive rows are recorded. Hybrid improves recall over dense but ranks positives lower at the top.

This indicates that lexical evidence occasionally adds missing positives, but dense retrieval is more reliable for top-10 ordering.

### Metric Interpretation for Model Researchers

This is a compact cross-domain summary retrieval stress test. Low BM25 and dense scores show that patent title-abstract fields are often insufficient for easy OUT-domain discovery. Models need cross-domain semantic abstraction rather than keyword search.

The many safeguard rows show that candidate generation itself is difficult. A reranker cannot solve the task unless positives first enter the candidate pool.

### Query and Relevance Type Tendencies

Queries and documents are title-abstract summaries. Positives are cross-domain cited families. Relevance may be based on analogy, shared technical effect, transferred mechanism, or problem-solution correspondence.

### Representative Failure Modes

BM25 fails when domain vocabulary changes. Dense retrieval may find broad analogy but not the cited family. Hybrid retrieval can improve recall while still over-ranking candidates with superficial overlap.

### Training Data That May Help

Useful training data includes cross-domain patent abstract citation retrieval, technology analogy search, and cross-IPC prior-art retrieval. Training should exclude NanoDAPFAM evaluation family IDs, positives, qrels, and duplicates.

Synthetic data should use compact title and abstract records from different domains, with positives that are cross-domain cited patent summaries.

### Model Improvement Notes

Improving this task requires strong patent-summary embeddings that can represent function and effect independently of IPC vocabulary. Hard negatives should include same-word but non-cited summaries and different-word but functionally related positives.

Citation-graph-aware contrastive training may be particularly useful.

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
| A source title-abstract summary from one field. | A target title-abstract summary from another field with citation relevance. |
| A compact apparatus summary. | A cross-domain summary describing an analogous apparatus or mechanism. |
| A process or method summary. | A target abstract in another class with related process behavior. |
| A material or device summary. | A cross-domain target summary with related technical effect. |
| A control-system summary. | A target abstract from another field with analogous control logic. |
