# NanoDAPFAM / NanoDAPFAMInTitlAbsClmToTitlAbs

## Overview

NanoDAPFAMInTitlAbsClmToTitlAbs is an English patent-family retrieval task. The query contains title, abstract, and claims from a source patent family, while target documents contain only title and abstract. Relevance is restricted to DAPFAM IN-domain positives: cited or related families that share IPC3 domain with the query family.

This split tests whether long claim-rich queries can retrieve concise same-domain patent summaries. The target representation is short, so many claim-level details are absent. The model must identify the central invention and match it to a compact summary inside the same technical field.

## Details

### What the Original Data Measures

DAPFAM uses patent-family citations as relevance judgments and distinguishes in-domain relations by IPC3 overlap. This split uses the IN condition, so positives are same-domain citation-related families. The source field includes claims, while the target field is limited to title and abstract.

The task measures claim-to-summary retrieval under same-domain constraints. It is a fine-grained prior-art search problem where positives and negatives may come from similar technical areas.

### Observed Data Profile

This Nano split contains 200 queries, 10,000 documents, and 3,062 positive qrels. The average positives per query is 15.31, with a minimum of 1, median of 18.0, and maximum of 20. There are 194 multi-positive queries. Queries average 8,405.46 characters, while target documents average 777.86 characters.

The large query-target length mismatch is central. Queries include detailed claim language, but targets expose only summary-level title and abstract content.

### BM25 Evaluation Profile

BM25 reaches nDCG@10 of 0.2970, hit@10 of 0.8200, and recall@100 of 0.4347 with a top-500 candidate pool. Exact terms from the source title and abstract help, and some claim terms survive into target abstracts. However, much of the query's detailed claim vocabulary cannot match short target records.

Same-domain negatives make lexical ranking harder. Many title-abstract candidates in the same IPC3 area share broad technical words, so BM25 may rank topic-near summaries above citation positives.

### Dense Evaluation Profile

The dense harrier-oss-270m profile is strongest, with nDCG@10 of 0.4135, hit@10 of 0.9050, and recall@100 of 0.6381. Dense retrieval substantially improves over BM25 by matching claim-level invention meaning to shorter summaries.

This split is a good example of dense semantic compression. The model must reduce long claims to the underlying technical contribution and compare that contribution with compact abstracts.

### Reranking Hybrid Evaluation Profile

The reranking_hybrid candidate subset reaches nDCG@10 of 0.3805, hit@10 of 0.8750, and recall@100 of 0.6084. It uses top-100 candidates with optional rank-101 safeguards; 10 rows contain 101 candidates and 10 safeguard-positive rows are recorded. Dense retrieval is stronger for both top ranking and recall.

Hybrid retrieval improves over BM25 but does not beat dense retrieval. The target title-abstract field provides limited lexical evidence, so adding BM25 candidates introduces same-domain term-overlap distractors.

### Metric Interpretation for Model Researchers

This is a dense-favored in-domain claim-to-summary retrieval task. BM25 can often find at least one positive, but its recall is much lower than dense retrieval. The task stresses semantic matching under short target representations and many same-domain distractors.

Because qrels are multi-positive, recall@100 is important. A model that only finds one close same-domain family may still miss many citation positives.

### Query and Relevance Type Tendencies

Queries contain title, abstract, and claims. Documents contain title and abstract only. Positives are same-domain cited families. The target abstract may summarize the same technical area without exposing every claim element.

### Representative Failure Modes

BM25 misses positives whose abstracts paraphrase the source claims. Dense retrieval may over-rank broad same-domain summaries that are semantically similar but not cited. Hybrid retrieval may be pulled toward candidates with shared technical terminology but insufficient citation relevance.

### Training Data That May Help

Useful training data includes same-domain patent citation retrieval, claim-rich query to patent abstract retrieval, and prior-art search pairs within shared IPC areas. Training should exclude NanoDAPFAM evaluation families and qrels.

Synthetic data should pair long source title-abstract-claims records with short target title-abstract records from same-domain cited families.

### Model Improvement Notes

Improving this task requires claim abstraction and summary matching. Models should learn to identify the core invention from claims and match it to concise summaries without depending on exact claim phrasing.

For reranking, signals such as citation likelihood, shared technical effect, and problem-solution similarity should be stronger than raw term overlap.

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
| A same-domain source family with title, abstract, and detailed claims. | A concise title-abstract target for a cited same-domain family. |
| A claim-rich apparatus source patent. | A short target summary describing a related apparatus in the same IPC3 class. |
| A source patent with detailed process steps. | A target abstract summarizing a cited process or method. |
| A source material patent with detailed compositions. | A same-domain title-abstract target about related material technology. |
| A source vehicle or control-system patent. | A same-domain title-abstract target about a cited control or steering family. |
