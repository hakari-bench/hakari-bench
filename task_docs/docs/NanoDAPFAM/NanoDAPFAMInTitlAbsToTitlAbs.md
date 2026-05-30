# NanoDAPFAM / NanoDAPFAMInTitlAbsToTitlAbs

## Overview

NanoDAPFAMInTitlAbsToTitlAbs is an English patent-family retrieval task where both source queries and target documents contain only title and abstract. Positives are restricted to DAPFAM IN-domain citation relations, so target families share IPC3 technical class with the query family.

This is a compact same-domain patent-summary retrieval task. It resembles title-abstract prior-art search in a known technical class. Since both sides are short summaries, the task is less noisy than full-text retrieval but provides fewer details for distinguishing cited families.

## Details

### What the Original Data Measures

DAPFAM measures patent-family retrieval with citation qrels and domain labels. The IN condition keeps citation-related families that share IPC3 domain with the source. This split uses title and abstract fields on both sides, making it a summary-to-summary version of in-domain patent retrieval.

### Observed Data Profile

This Nano split contains 200 queries, 10,000 documents, and 3,066 positive qrels. There are 194 multi-positive queries. Positives per query average 15.33, with a minimum of 1, median of 18.0, and maximum of 20. Queries average 771.27 characters, and documents average 777.74 characters.

The field symmetry makes this split useful for isolating semantic summary matching without long-document artifacts.

### BM25 Evaluation Profile

BM25 reaches nDCG@10 of 0.3386, hit@10 of 0.8650, and recall@100 of 0.4677 with a top-500 candidate pool. Exact technical terms in titles and abstracts are useful, especially because positives share the same domain.

BM25 still has limited recall. Same-domain abstracts may share terms even when not citation-related, and cited families may use different terminology for the same technical contribution.

### Dense Evaluation Profile

The dense harrier-oss-270m profile reaches nDCG@10 of 0.3923, hit@10 of 0.8750, and recall@100 of 0.6093. Dense retrieval improves recall substantially over BM25 by matching semantic relatedness between compact invention summaries.

Dense retrieval is helpful for paraphrased same-domain relevance, but it must still distinguish citation positives from other abstracts in the same field.

### Reranking Hybrid Evaluation Profile

The reranking_hybrid candidate subset reaches nDCG@10 of 0.3942, hit@10 of 0.8700, and recall@100 of 0.5985. It uses top-100 candidates with optional rank-101 safeguards; nine rows contain 101 candidates and nine safeguard-positive rows are recorded. Hybrid slightly leads nDCG, while dense leads hit@10 and recall@100.

The close scores show that lexical and dense signals overlap substantially in this compact representation. Hybrid can improve top ordering for some queries, but dense retrieval provides slightly broader positive coverage.

### Metric Interpretation for Model Researchers

This is a compact in-domain patent retrieval task with multi-positive qrels. It is a good setting for evaluating patent-summary embeddings without the confound of very long targets or claim-heavy text.

The key metric distinction is that BM25 has a high hit@10 but much lower recall@100 than dense. It often finds one related family but misses much of the citation set.

### Query and Relevance Type Tendencies

Queries and documents are title-abstract summaries. Positives are same-domain citation-related families. The short records emphasize invention summaries, problem statements, and technical effects.

### Representative Failure Modes

BM25 may rank abstracts with shared terminology but no citation link. Dense retrieval may over-rank broadly similar summaries in the same IPC3 area. Hybrid retrieval may not add much when both signals retrieve similar same-domain candidates.

### Training Data That May Help

Useful training data includes same-domain title-abstract patent citation retrieval, IPC-restricted patent semantic search, and prior-art retrieval over compact patent summaries. Training should exclude NanoDAPFAM evaluation families, positives, and qrels.

Synthetic data should generate short title and abstract patent records in shared technical classes, with positives drawn from cited same-domain families.

### Model Improvement Notes

Improving this task requires fine-grained summary embeddings for patents. Models should capture technical problem, solution, effect, and domain without relying only on shared class vocabulary.

For reranking, citation-style relation modeling may help separate true positives from same-topic summaries.

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
| A title-abstract source summary in a shared IPC3 domain. | A cited same-domain target represented by title and abstract. |
| A concise device or apparatus abstract. | A same-domain target summary for related prior art. |
| A concise process or method abstract. | A target abstract about a cited same-domain method. |
| A material or composition summary. | A same-domain target summary about related material technology. |
| A vehicle or control-system summary. | A same-domain target abstract about related control technology. |
