# NanoRARb / NanoWinoGrande

## Overview

`NanoWinoGrande` is an English commonsense referent-resolution retrieval task from NanoRARb. The query is a Winograd-style sentence with an underspecified blank, and the relevant document is the correct referent string. Each query has one positive answer among 5,095 short candidate documents. The task rewards both lexical access to candidate referents and commonsense disambiguation. `reranking_hybrid` is the strongest observed profile, BM25 is also strong, and dense retrieval is slightly weaker, showing that surface mention overlap remains highly useful for this split.

## Details

### What the Original Data Measures

RAR-b includes WinoGrande as a reasoning-as-retrieval task. The original WinoGrande benchmark is an adversarially filtered Winograd Schema Challenge variant that tests whether systems can resolve a pronoun or blank to the correct entity using commonsense reasoning.

In this retrieval version, the model receives the sentence with a blank and must retrieve the correct referent from a large answer pool. The document is not evidence; it is the candidate referent itself.

### Observed Data Profile

The Nano split contains 200 queries, 5,095 documents, and 200 positive qrel rows. Every query has exactly one positive. Queries average 111.98 characters, while candidate documents average 7.68 characters.

Examples include choosing whether a blank refers to an ear or a piercing, whether a brownie or apple has fewer calories, which person has an analytical mind, whether a bakery or bank has limited supply, and which person argued for getting a pool.

### BM25 Evaluation Profile

The BM25 candidate subset uses top-500 candidates and reaches nDCG@10 of 0.5067, hit@10 of 0.8850, and recall@100 of 1.0000. BM25 performs well because the correct referent is often a word already present in the sentence.

The remaining difficulty is ranking. Many queries contain two plausible referents with similar lexical status, so term matching can put both candidates near the top without deciding which one the blank actually denotes.

### Dense Evaluation Profile

The dense candidate subset from `harrier_oss_v1_270m` uses top-500 candidates and reaches nDCG@10 of 0.4946, hit@10 of 0.7750, and recall@100 of 0.9800. Dense retrieval is competitive but weaker than BM25 on hit@10 and coverage.

This suggests that embedding similarity captures broad sentence-referent compatibility but can underweight exact mention identity. A short answer such as a name or noun may be semantically plausible even when it is the wrong referent.

### Reranking Hybrid Evaluation Profile

The `reranking_hybrid` subset uses top-100 candidates and does not need the rank-101 safeguard. It reaches nDCG@10 of 0.6020, hit@10 of 0.9100, and recall@100 of 1.0000. Hybrid retrieval is the strongest profile for this task.

The result matches the task structure. Sparse retrieval anchors candidate mentions from the sentence, while dense retrieval contributes commonsense compatibility. Combining both signals gives a better candidate order than either method alone.

### Metric Interpretation for Model Researchers

With one positive per query, nDCG@10 measures how early the correct referent appears, hit@10 measures whether it is available in the first ten candidates, and recall@100 measures whether a reranker can access it.

For `NanoWinoGrande`, recall@100 is already saturated for BM25 and hybrid retrieval, so model improvements should focus on top-rank ordering. A strong reranker should compare the two plausible referents in the sentence rather than only score answer strings independently.

### Query and Relevance Type Tendencies

Queries are short cloze-style sentences with an underscore marking the missing referent. Relevant documents are very short names or common nouns. Candidate answers often include words that appear in the query.

Relevance is referent correctness. A candidate may be explicitly mentioned in the sentence and still be wrong if commonsense constraints point to the other mention.

### Representative Failure Modes

Common failures include choosing the wrong mentioned entity, overranking a noun because it appears near the blank, missing causal or comparative cues, and treating both alternatives as equally plausible. BM25 can find mentioned candidates but not resolve the schema; dense retrieval can blur short candidate identities.

### Training Data That May Help

Useful training data includes Winograd-style pronoun resolution, coreference QA, cloze referent retrieval, sentence-level commonsense reasoning, and hard negatives using the competing referent from the same sentence. Evaluation sentences, answer strings, and qrels should be excluded.

### Model Improvement Notes

Models should learn to jointly encode the blank sentence and candidate referent. Hard negatives should be the alternative referent from the same sentence or a semantically similar name or noun. Hybrid retrieval is particularly appropriate because the task needs both exact mention recovery and commonsense selection.

## Example Data

| Query | Positive document |
| --- | --- |
| Sentence: Mary wanted to get another piercing in her ear, but the _ was much too tiny.. [87 chars] | ear [3 chars] |
| Sentence: She counted her calories for her diet and found she needed more so she ate a brownie instead of an apple since the _ has fewer.. [138 chars] | apple [5 chars] |
| Sentence: The game of chess was easy to play for Angela but not Rebecca because _ had a analytical mind.. [105 chars] | Angela [6 chars] |

### Source Reference Table

| Title | Year | Type | URL |
| --- | ---: | --- | --- |
| RAR-b: Reasoning as Retrieval Benchmark | 2024 | arXiv paper | [https://arxiv.org/abs/2404.06347](https://arxiv.org/abs/2404.06347) |
| WinoGrande: An Adversarial Winograd Schema Challenge at Scale | 2019 | arXiv paper | [https://arxiv.org/abs/1907.10641](https://arxiv.org/abs/1907.10641) |

### Representative Snippets

| Query | Relevant document excerpt |
| --- | --- |
| Mary wanted another piercing in her ear, but the _ was much too tiny. | ear |
| She needed more calories, so she ate a brownie instead of an apple since the _ has fewer. | apple |
| The game of chess was easy for Angela but not Rebecca because _ had an analytical mind. | Angela |
| Joe went to the bakery before the bank because the _ had a limited supply of what he wanted. | bakery |
| William liked to be outside more than Kyle, so _ argued for getting a pool. | William |
