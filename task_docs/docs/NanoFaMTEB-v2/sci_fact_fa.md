# NanoFaMTEB-v2 / sci_fact_fa

## Overview

`sci_fact_fa` is a Persian scientific claim-evidence retrieval task in NanoFaMTEB-v2. The query is a scientific claim, and the documents are Persian scientific abstracts or paper snippets that may provide evidence for the claim.

This task tests technical evidence retrieval rather than general factual search. Exact biomedical and scientific terms are important, but a model must also connect a claim to abstracts that support, refute, or otherwise provide evidence for the same scientific relationship.

## Details

### What the Original Data Measures

FaMTEB includes translated BEIR-style retrieval tasks, including scientific evidence retrieval. `sci_fact_fa` uses `MCINext/scifact-fa-v2`, a Persian SciFact variant evaluated through the MTEB retrieval framework.

SciFact-style retrieval measures whether systems can find scientific abstracts relevant to a claim. In retrieval form, the model does not need to decide the stance label in the task document itself, but it must retrieve the abstract that contains the evidence needed for verification.

### Observed Data Profile

This Nano split contains 200 queries, 5,183 documents, and 225 positive qrels. Queries have 1.12 positives on average, with a minimum of 1, a median of 1.0, and a maximum of 5. There are 15 multi-positive queries, or 7.5% of the split. Queries average 84.49 characters, and documents average 1,361.31 characters.

Observed examples include biomedical claims about DNA polymerase deficiency and ionizing radiation sensitivity, CRP and coronary artery bypass surgery mortality, p150 and EB1 interaction, noncoding RNA ribosome occupancy, and febrile seizures. Documents are longer scientific abstracts translated or rendered in Persian.

### BM25 Evaluation Profile

BM25 reaches nDCG@10 of 0.6294, hit@10 of 0.7900, and recall@100 of 0.9022 with a top-500 candidate pool. This is the strongest direct ranking profile among the three first-stage views.

The task gives BM25 strong anchors: biomedical abbreviations, protein names, genes, procedures, and technical phrases often recur in both claims and abstracts. Exact term matching is therefore highly informative. However, BM25 can still struggle when evidence uses a different construction from the claim or when several abstracts share the same technical vocabulary.

### Dense Evaluation Profile

The dense harrier-oss-270m profile reaches nDCG@10 of 0.5610, hit@10 of 0.7000, and recall@100 of 0.8578. Dense retrieval is weaker than BM25 on this task.

This suggests that general-purpose embedding similarity may not preserve enough fine-grained biomedical terminology and negation-sensitive claim structure. Scientific evidence retrieval often depends on exact entities, abbreviations, and measured relationships. Dense retrieval can find broad topical similarity, but that is not always enough to identify the evidence abstract.

### Reranking Hybrid Evaluation Profile

The reranking_hybrid candidate subset reaches nDCG@10 of 0.6100, hit@10 of 0.7400, and recall@100 of 0.9333. It uses 100 candidates per query, with 15 rank-101 safeguard positives.

Hybrid retrieval gives the best recall@100 but does not exceed BM25 on nDCG@10 or hit@10. This makes it useful as a reranking pool: it broadens candidate coverage while retaining much of BM25's terminology-driven strength. The 15 safeguard rows show that a nontrivial number of positives needed the optional positive inclusion mechanism.

### Metric Interpretation for Model Researchers

`sci_fact_fa` is a case where BM25 is stronger than dense retrieval. That is important for researchers because the task rewards precise technical term matching and claim-specific evidence, not only semantic relatedness.

nDCG@10 measures whether the evidence abstract is ranked high enough for a verifier or reader to use. Recall@100 matters for reranking pipelines, especially because the hybrid pool has the highest candidate coverage. Since most queries have only one positive, missing that abstract is costly.

### Query and Relevance Type Tendencies

Queries are declarative Persian scientific claims, often with biomedical abbreviations, molecular entities, diseases, procedures, or experimental findings. Documents are longer abstracts with technical background, methods, and conclusions.

The relevance relation is evidence-based. A relevant abstract is not merely about the same protein or disease; it must contain evidence connected to the claim.

### Representative Failure Modes

BM25 may retrieve abstracts that share a gene, protein, disease, or procedure but discuss a different relationship. Dense retrieval may retrieve topically similar biomedical abstracts that miss the exact claim, numeric result, or negation. Hybrid retrieval improves coverage but still needs a reranker that understands scientific evidence alignment.

Negation and directionality are particularly risky. Claims about whether a factor predicts mortality, increases a threshold, or does not produce a functional peptide require more than topic matching.

### Training Data That May Help

Useful training data includes Persian scientific claim verification, translated SciFact examples, biomedical abstract retrieval, evidence sentence retrieval, and hard negatives that share technical terms but support a different claim or stance.

Training should exclude NanoFaMTEB-v2 evaluation claims and abstracts from this split.

### Model Improvement Notes

Improving this task likely requires better biomedical term handling and claim-evidence alignment. Models should preserve abbreviations, gene and protein symbols, procedure names, negation, and causal or predictive relations.

For reranking, exact evidence sufficiency is more important than topical similarity. A reranker should identify whether the abstract can actually verify the claim.

## Example Data

### Public Sources

This task is documented through the FaMTEB paper and the `MCINext/scifact-fa-v2` dataset card. MTEB provides the broader retrieval evaluation framework.

### Source Reference Table

| Source | Role |
| --- | --- |
| [FaMTEB: Massive Text Embedding Benchmark in Persian Language](https://arxiv.org/abs/2502.11571) | Persian embedding benchmark paper. |
| [MTEB: Massive Text Embedding Benchmark](https://arxiv.org/abs/2210.07316) | General embedding benchmark framework. |
| [MCINext/scifact-fa-v2](https://huggingface.co/datasets/MCINext/scifact-fa-v2) | Public source dataset card. |
| [hakari-bench/NanoFaMTEB-v2](https://huggingface.co/datasets/hakari-bench/NanoFaMTEB-v2) | Nano benchmark dataset containing this split. |

### Representative Snippets

| Query Pattern | Positive Document Pattern |
| --- | --- |
| A Persian claim about DNA polymerase I deficiency increasing sensitivity to ionizing radiation. | A scientific abstract about DNA polymerase functions and immune recombination mechanisms. |
| A claim that CRP cannot predict mortality after coronary artery bypass surgery. | An abstract about prognostic biomarkers and decision models for coronary surgery patients. |
| A claim about the importance of arginine 90 in p150 for EB1 interaction. | An abstract describing structural activation of microtubule assembly by EB1 and p150Glued. |
| A claim that ribosome occupancy by noncoding RNAs does not produce functional peptides. | An abstract using ribosome profiling to argue that large noncoding RNAs do not encode proteins. |
| A claim that febrile seizures increase the threshold for epilepsy onset. | An abstract about long-lasting changes in neuronal excitability after febrile seizures. |
