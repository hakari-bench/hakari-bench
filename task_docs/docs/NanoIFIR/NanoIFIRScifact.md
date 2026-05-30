# NanoIFIR / NanoIFIRScifact

## Overview

`NanoIFIRScifact` is an English scientific literature retrieval task in NanoIFIR. The queries are scientific claims, and the documents are scientific article titles and abstracts.

This task evaluates evidence retrieval for scientific claim verification. The retriever must find abstracts that support, refute, or otherwise provide evidence for the claim under the instruction-following setting. It is lexically favorable compared with many other IFIR tasks because claims often include distinctive scientific terms that appear in relevant abstracts.

## Details

### What the Original Data Measures

IFIR uses SciFact-open for the scientific literature domain. It turns claim-evidence retrieval into instruction-following retrieval by adding requirements such as finding supporting evidence, refuting evidence, or research-objective-specific passages.

SciFact is a scientific claim verification benchmark. It asks systems to select abstracts from the research literature that support or refute a scientific claim and to identify rationales. In NanoIFIR, this becomes a retrieval-focused task over scientific abstracts.

### Observed Data Profile

This Nano split contains 43 queries, 10,000 documents, and 255 positive qrels. Every query is multi-positive. Queries have 5.93 positives on average, with a minimum of 3, a median of 5.0, and a maximum of 24. Queries average 73.63 characters, and documents average 1,452.61 characters.

Observed claims cover obesity genetics, teaching versus non-teaching hospital outcomes, risedronate fracture reduction, bariatric surgery and diabetes, BRCA mutation location and cancer risk, biomedical mechanisms, receptors, stem cells, and gene expression. Documents are article titles and abstracts.

### BM25 Evaluation Profile

BM25 reaches nDCG@10 of 0.8682, hit@10 of 1.0000, and recall@100 of 0.9765 with a top-500 candidate pool. This is an extremely strong lexical profile.

Scientific claims often reuse technical terms, disease names, drug names, gene names, or intervention phrases found in evidence abstracts. BM25 can therefore retrieve relevant evidence reliably. Remaining ranking errors are likely cases where several abstracts share the same entities but differ in evidence relation or polarity.

### Dense Evaluation Profile

The dense harrier-oss-270m profile reaches nDCG@10 of 0.8516, hit@10 of 0.9767, and recall@100 of 0.9686. Dense retrieval is also very strong, but slightly below BM25.

This suggests that exact scientific terminology is particularly valuable in this split. Dense retrieval captures semantic relatedness, but may blur fine distinctions between evidence-bearing abstracts and related scientific background.

### Reranking Hybrid Evaluation Profile

The reranking_hybrid candidate subset reaches nDCG@10 of 0.9055, hit@10 of 1.0000, and recall@100 of 0.9922. It uses exactly 100 candidates per query and has no safeguard-positive rows.

Hybrid retrieval is the strongest profile. It preserves BM25's terminology precision while adding semantic evidence coverage, producing the best nDCG@10 and recall@100. This is a high-quality reranking pool with little candidate-miss pressure.

### Metric Interpretation for Model Researchers

`NanoIFIRScifact` is a high-scoring scientific evidence retrieval task. BM25 is already near ceiling for hit and recall, so improvements should be judged mainly through nDCG@10 and evidence-ordering quality.

Because every query has multiple positives, recall@100 remains meaningful. The hybrid profile shows that combining lexical and dense signals can improve the ordering of evidence abstracts even when lexical retrieval is already strong.

### Query and Relevance Type Tendencies

Queries are concise scientific claims. Documents are scientific abstracts with titles, background, methods, and findings. The topics are heavily biomedical but include general scientific and healthcare outcome claims.

The relevance relation is evidence-bearing relevance. A positive abstract should contain information useful for supporting, refuting, or evaluating the claim, not merely mention the same entity.

### Representative Failure Modes

BM25 may retrieve abstracts with the same technical terms but a different finding or evidence polarity. Dense retrieval may retrieve related literature that lacks the specific outcome or claim relation. Hybrid retrieval reduces both failure modes but still needs reranking to handle support versus refute distinctions.

Negation and comparative claims are especially sensitive. A passage can share all major entities while contradicting the claim or addressing a different endpoint.

### Training Data That May Help

Useful training data includes non-overlapping SciFact claim-evidence pairs, scientific abstract retrieval pairs, citation intent and evidence retrieval data, and same-entity scientific hard negatives.

Training should distinguish evidence retrieval from truth classification, preserve multiple evidence abstracts, and exclude `NanoIFIRScifact` claims, qrels, and positive evidence abstracts.

### Model Improvement Notes

Improving this task requires evidence-level scientific matching. Models should preserve named entities and interventions while representing finding direction, comparison, causality, and evidence polarity.

For reranking, the core question is whether the abstract provides usable evidence for the claim. A strong reranker should not treat topical similarity as sufficient when the claim relation differs.

## Example Data

### Public Sources

This task is documented through the IFIR paper and the SciFact scientific claim verification paper. The Nano split is published in `hakari-bench/NanoIFIR`.

### Source Reference Table

| Source | Role |
| --- | --- |
| [IFIR: A Comprehensive Benchmark for Evaluating Instruction-Following in Expert-Domain Information Retrieval](https://arxiv.org/abs/2503.04644) | Expert-domain instruction-following IR benchmark paper. |
| [SciFact: A Dataset and Benchmark for Scientific Claim Verification](https://aclanthology.org/2020.emnlp-main.609/) | Original scientific claim verification paper. |
| [hakari-bench/NanoIFIR](https://huggingface.co/datasets/hakari-bench/NanoIFIR) | Nano benchmark dataset containing this split. |

### Representative Snippets

| Query Pattern | Positive Document Pattern |
| --- | --- |
| A claim that obesity is partly determined by genetic factors. | An abstract about genetics of obesity in adoptees and biological siblings. |
| A claim that teaching hospitals provide better care than non-teaching hospitals. | A systematic review comparing patient outcomes in teaching and non-teaching healthcare. |
| A claim that risedronate reduces vertebral and non-vertebral fracture risk. | A randomized controlled trial abstract about risedronate treatment in postmenopausal osteoporosis. |
| A claim about bariatric surgery and diabetes resolution. | A cohort-study abstract about bariatric surgery outcomes and weight-loss effects. |
| A claim about BRCA mutation location and breast or ovarian cancer risk. | An abstract analyzing the association between BRCA1/BRCA2 mutation type or location and cancer risk. |
