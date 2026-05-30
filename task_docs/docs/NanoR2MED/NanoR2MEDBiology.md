# NanoR2MED / NanoR2MEDBiology

## Overview

`NanoR2MEDBiology` is an English reasoning-driven biology retrieval task from R2MED. Queries are Biology StackExchange questions, and documents are explanatory biology passages drawn from web or Wikipedia-derived sources. Each query can have multiple relevant passages, so the task measures retrieval of answer-supporting evidence rather than one exact passage. Dense retrieval is much stronger than BM25, while the hybrid pool improves hit@10 and recall@100 but trails dense retrieval on nDCG@10. The split is useful for evaluating concept selection in biology questions with everyday phrasing.

## Details

### What the Original Data Measures

R2MED frames retrieval as finding documents that support a latent reasoning answer. The benchmark paper includes Q&A reference retrieval, clinical evidence retrieval, and clinical case retrieval. Biology is part of the Q&A reference retrieval group and is adopted from BRIGHT-style reasoning-intensive retrieval data.

In this task, StackExchange questions serve as queries and external answer-supporting pages serve as positives. Relevance often depends on identifying the biological mechanism, molecule, organism, or evolutionary concept behind the question rather than matching a short keyword string.

### Observed Data Profile

The Nano split contains 103 queries, 10,000 documents, and 374 positive qrel rows. Queries average 523.03 characters, and documents average 474.07 characters.

The task is strongly multi-positive: each query has 3.63 positives on average, with a median of 3 and a maximum of 19. Ninety-three of 103 queries, or 90.29%, have multiple positives. Examples ask about long-lived proteins in the human body, whether kissing is natural human behavior, which monitor light plants can use for photosynthesis, immune recognition of tumor mutations, and bacteriophage therapy.

### BM25 Evaluation Profile

The BM25 candidate subset uses top-500 candidates and reaches nDCG@10 of 0.3455, hit@10 of 0.5922, and recall@100 of 0.6818. BM25 benefits from clear entity or concept words such as chlorophyll, phage, tumor, protein, and photosynthesis.

The remaining difficulty is conceptual. Many questions are phrased as everyday puzzles or broad biological curiosity, while the relevant documents use scientific terminology. BM25 can retrieve the same broad biological topic but miss the mechanism that actually supports the answer.

### Dense Evaluation Profile

The dense candidate subset from `harrier_oss_v1_270m` uses top-500 candidates and reaches nDCG@10 of 0.4953, hit@10 of 0.7573, and recall@100 of 0.8369. Dense retrieval clearly outperforms BM25 across all reported metrics. This shows that embedding similarity is better at mapping informal biology questions to explanatory scientific passages.

Dense retrieval is especially useful when the query describes a phenomenon in plain language and the document names the underlying mechanism. It is the strongest standalone ranking profile for this split.

### Reranking Hybrid Evaluation Profile

The `reranking_hybrid` subset uses top-100 candidates, with three rows receiving the optional rank-101 safeguard. It reaches nDCG@10 of 0.4722, hit@10 of 0.7864, and recall@100 of 0.8503. Hybrid retrieval improves hit@10 and recall@100 over dense retrieval but has lower nDCG@10.

This means hybrid candidate construction is valuable for coverage, but dense retrieval still orders the most relevant evidence more effectively at the very top. A reranker should use the hybrid pool to recover additional positives while restoring dense-like top-rank precision.

### Metric Interpretation for Model Researchers

Because most queries have multiple positives, nDCG@10 captures graded quality of the ranked evidence set, not just whether one document is found. Hit@10 measures whether the system finds any supporting evidence early. Recall@100 measures how much of the available positive set is exposed to a reranker.

For Biology, dense retrieval is the top-rank baseline, while hybrid retrieval is the stronger coverage-oriented pool. A model improvement should be judged by whether it retrieves the right mechanism, not merely the same broad biological topic.

### Query and Relevance Type Tendencies

Queries are natural-language biology questions, often with a misconception, analogy, or explanatory goal. Relevant passages are encyclopedia-like or educational descriptions of proteins, behavior, plant pigments, antigen presentation, phage therapy, and related mechanisms.

The relevance relation is answer support. A passage may be relevant if it explains the mechanism needed to answer the question, even if it does not repeat the user's exact phrasing.

### Representative Failure Modes

Common failures include retrieving a page about the same organism or broad topic but the wrong mechanism, matching everyday words such as light or smell without the needed biological concept, and ranking disease or immune-system passages that do not support the requested causal explanation. BM25 misses latent concepts; dense retrieval can overgeneralize among related mechanisms.

### Training Data That May Help

Useful training data includes non-overlapping Biology StackExchange answer-link retrieval, BRIGHT reasoning-intensive biology retrieval without overlap, biological concept QA, Wikipedia section retrieval, and hard negatives from adjacent mechanisms or taxa. Evaluation queries, qrels, and positive passages should be excluded, and overlap with BRIGHT should be audited before training.

### Model Improvement Notes

Models should learn to map informal biology questions to scientific mechanisms and evidence passages. Multi-positive objectives are appropriate because most queries have several supporting documents. Hard negatives should share the same broad biology field while changing the mechanism, molecule, organism, or evolutionary explanation.

## Example Data

### Public Sources

- [R2MED: A Benchmark for Reasoning-Driven Medical Retrieval](https://arxiv.org/abs/2505.14558), benchmark paper.
- [R2MED project page](https://r2med.github.io/).
- [R2MED GitHub repository](https://github.com/R2MED/R2MED).
- [R2MED/Biology dataset card](https://huggingface.co/datasets/R2MED/Biology).

### Source Reference Table

| Title | Year | Type | URL |
| --- | ---: | --- | --- |
| R2MED: A Benchmark for Reasoning-Driven Medical Retrieval | 2025 | arXiv paper | https://arxiv.org/abs/2505.14558 |
| R2MED project page | 2025 | project page | https://r2med.github.io/ |
| R2MED GitHub repository | 2025 | source repository | https://github.com/R2MED/R2MED |
| R2MED/Biology | 2025 | dataset card | https://huggingface.co/datasets/R2MED/Biology |

### Representative Snippets

| Query | Relevant document excerpt |
| --- | --- |
| What is the longest-lasting protein in the human body? | A passage identifying elastin as a very long-lived protein with a human half-life of more than 78 years. |
| Is kissing a natural human activity rather than only a sociological construct? | A passage discussing animal analogies to kissing and biological or evolutionary interpretations of the behavior. |
| What kinds of light can or cannot support plant photosynthesis from a monitor? | A passage explaining chlorophyll pigments in cyanobacteria, algae, and plants. |
| If tumors contain many mutations, why can the immune system fail to detect them? | A passage about antigen processing and presentation through the MHC class I pathway. |
| Could viruses that affect bacteria be used as antibiotics? | A passage about therapeutic applications of bacteriophages and collection of phages from bacteria-rich environments. |
