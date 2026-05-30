# NanoDAPFAM / NanoDAPFAMInTitlAbsToTitlAbsClm

## Overview

NanoDAPFAMInTitlAbsToTitlAbsClm is an English patent-family retrieval task. The query contains a source patent family's title and abstract, and the target document contains title, abstract, and claims. Relevance is restricted to DAPFAM IN-domain citation relations, meaning positives share IPC3 technical class with the query family.

This split tests compact-query to claim-rich target retrieval inside the same technical domain. The target claims expose more detail than a short abstract, but they also introduce formal claim language and many same-domain distractors.

## Details

### What the Original Data Measures

DAPFAM uses patent-family citations as qrels and labels domain relations by IPC3 overlap. This split uses IN-domain positives and compares a title-abstract source representation against target records enriched with claims.

The task measures whether a short patent summary can retrieve same-domain cited families when candidate documents include detailed claim language.

### Observed Data Profile

This Nano split contains 200 queries, 10,000 documents, and 3,072 positive qrels. There are 194 multi-positive queries. Positives per query average 15.36, with a minimum of 1, median of 18.0, and maximum of 20. Queries average 771.27 characters, and target documents average 7,226.36 characters.

The target claims provide more evidence than title-abstract records, but also more repeated legal vocabulary and term overlap among same-domain candidates.

### BM25 Evaluation Profile

BM25 reaches nDCG@10 of 0.3593, hit@10 of 0.8500, and recall@100 of 0.5160 with a top-500 candidate pool. Claims on the target side improve lexical coverage because query terms may appear in target claim elements.

BM25 still trails dense and hybrid methods. Same-domain claims often share broad terminology, so lexical overlap alone is not enough to identify citation-related families.

### Dense Evaluation Profile

The dense harrier-oss-270m profile reaches nDCG@10 of 0.4125, hit@10 of 0.8700, and recall@100 of 0.6452. Dense retrieval improves positive coverage by matching summary-level invention meaning to detailed target claims.

Dense retrieval is useful when the target claim structure expresses the same technical contribution with different wording from the source abstract.

### Reranking Hybrid Evaluation Profile

The reranking_hybrid candidate subset is strongest by nDCG@10 and hit@10, reaching 0.4220 and 0.8850 respectively, with recall@100 of 0.6413. It uses top-100 candidates with optional rank-101 safeguards; five rows contain 101 candidates and five safeguard-positive rows are recorded. Dense retrieval has slightly higher recall@100, while hybrid has better top-10 ordering.

This suggests that exact target claim terms and dense semantic matching are both valuable. Hybrid ranking helps place relevant same-domain families higher when the target claims contain useful lexical anchors.

### Metric Interpretation for Model Researchers

This is a hybrid-friendly in-domain patent retrieval task. Target claims add useful lexical and semantic detail, so combining BM25 and dense candidates can improve top ranking. Dense retrieval remains slightly better for broad positive coverage.

As with other DAPFAM splits, multi-positive recall matters. A strong system should recover many same-domain cited families, not just the easiest one.

### Query and Relevance Type Tendencies

Queries are title-abstract summaries. Documents contain title, abstract, and claims. Positives are cited families in the same IPC3 domain. Target claims often contain the detailed component or process evidence missing from the short query.

### Representative Failure Modes

BM25 may over-rank target claims that repeat query terms but describe a different invention. Dense retrieval may retrieve semantically close same-domain patents without citation relation. Hybrid retrieval can improve top ranking but still confuse claim-rich distractors.

### Training Data That May Help

Useful training data includes same-domain title-abstract to patent-claims retrieval, IPC-restricted citation prediction, and prior-art search with claim-rich targets. Training should exclude NanoDAPFAM evaluation families, positives, qrels, and same-family duplicates.

Synthetic data should pair compact source title-abstract summaries with same-domain target records containing title, abstract, and claims.

### Model Improvement Notes

Improving this task requires summary-to-claim alignment. Models should connect abstract-level invention descriptions to specific claim elements and should down-weight generic claim boilerplate.

For reranking, claim-element matching and citation-style dependency features are likely useful.

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
| A title-abstract source summary. | A same-domain cited target with title, abstract, and claims. |
| A compact apparatus abstract. | A target claim set for a related same-domain apparatus. |
| A compact process abstract. | A same-domain cited target with detailed method claims. |
| A material or composition abstract. | A claim-rich target about related material technology. |
| A vehicle or control-system abstract. | A same-domain target with related control-system claims. |
