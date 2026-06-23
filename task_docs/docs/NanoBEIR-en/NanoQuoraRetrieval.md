# NanoBEIR-en / NanoQuoraRetrieval

## Overview

NanoQuoraRetrieval is the compact English NanoBEIR version of Quora duplicate-question retrieval. Each query is a user-written question, and the corpus contains candidate questions. The retrieval goal is to find questions that ask the same underlying information need, even when wording, grammar, or specificity differs. This makes the task useful for evaluating paraphrase retrieval, duplicate intent detection, FAQ routing, and short-text semantic matching.

## Details

### What the Original Data Measures

Quora duplicate-question retrieval is based on the Quora Question Pairs setting and is framed in BEIR as duplicate-question retrieval. A relevant document is another question, not an answer passage. The benchmark therefore measures whether a model can identify answer-equivalent questions.

No standalone task paper is used as the primary source here; the Quora Question Pairs dataset record and BEIR benchmark context explain the task framing. The important point for retrieval is that a same-topic question is not necessarily positive. The candidate must preserve the same user intent closely enough to be treated as a duplicate.

### Observed Data Profile

The task contains 50 queries, 5,046 documents, and 70 relevance judgments. The average number of positives is 1.40 per query, with a minimum of 1, a median of 1.0, and a maximum of 6. There are 10 multi-positive queries, or 20.0% of the set.

Queries average 47.96 characters, and documents average 54.81 characters. This is a short-text retrieval task. Since both sides are questions, relevance depends on comparing intent rather than finding an answer in a longer passage.

### BM25 Evaluation Profile

BM25 reaches nDCG@10 of 0.8745, hit@10 of 0.9800, and recall@100 of 1.0000 using the top-500 BM25 candidate subset. This is an extremely strong lexical baseline. Many duplicate questions retain rare content words, names, or phrases, and the short documents make exact overlap very informative.

The remaining errors are still meaningful. BM25 can struggle when duplicates use different wording, morphology, abbreviations, or spelling variants, and it can over-rank questions that share a template but ask for a different thing. It is excellent for candidate generation but can still be improved at cluster-level ordering.

### Dense Evaluation Profile

The dense harrier-oss-270m run reaches nDCG@10 of 0.8888, hit@10 of 0.9600, and recall@100 of 0.9714. Dense retrieval improves nDCG@10 over BM25 but loses a little hit@10 and recall@100. This indicates that embedding similarity helps rank paraphrastic duplicates, but sparse exact matching still recovers some positives that dense misses.

The dense gain in nDCG@10 reflects the core semantic nature of the task. Duplicate questions may ask the same intent with different surface phrasing, and embeddings can connect those variants better than term frequency alone. However, exact phrases remain important in short questions.

### Reranking Hybrid Evaluation Profile

The reranking_hybrid candidate set reaches nDCG@10 of 0.9105, hit@10 of 0.9800, and recall@100 of 1.0000. It uses exactly 100 candidates per query, with no safeguard rows. This is the strongest profile overall, combining BM25's complete recall and high hit rate with dense-style paraphrase ordering.

The hybrid result is a clean example of the value of combining sparse and dense retrieval. BM25 captures exact duplicate wording, while dense retrieval captures intent-preserving paraphrases. The combined pool gives the best top-rank quality without sacrificing candidate coverage.

### Metric Interpretation for Model Researchers

Because many queries have one positive but some have duplicate clusters, nDCG@10 is more informative than hit@10 alone. A model should rank all acceptable duplicate questions high, not only find one. recall@100 measures whether a reranker has access to the whole duplicate set.

The comparison shows that BM25 is already very strong, dense retrieval improves semantic ordering, and reranking_hybrid is best overall. This task is useful for testing short-text intent equivalence under high lexical overlap.

### Query and Relevance Type Tendencies

Queries include questions such as whether it is okay to laugh at your own jokes, the best lie someone has told, why Quora suggests anti-Donald Trump answers, how to become physically strong, and how a quantum satellite works. Positives are alternate questions with the same practical intent.

The task rewards answer-equivalence rather than broad topic similarity. A question can mention the same entity or phrase and still be negative if it asks for a different answer. Conversely, a positive can use different wording if the expected answer is the same.

### Representative Failure Modes

Likely failures include ranking related but non-duplicate questions, missing paraphrases with different wording, over-valuing generic question templates, and mishandling spelling or morphology differences. BM25 may miss semantic paraphrases, while dense retrieval may over-generalize topic similarity.

### Training Data That May Help

Useful training data includes non-overlapping Quora duplicate-question pairs, FAQ duplicate pairs, StackExchange duplicate links, community-question paraphrase data, and supervised intent-equivalence datasets. Multi-positive training is useful for duplicate clusters with several acceptable formulations.

### Model Improvement Notes

A model targeting this task should optimize for answer-equivalent question matching. Sparse systems need phrase and spelling robustness. Dense systems need hard negatives that share topics but are not duplicates. Hybrid systems are especially strong here because exact overlap and semantic paraphrase both matter.

## Example Data

| Query | Positive document |
| --- | --- |
| Is it okay to laugh at your own jokes? [38 chars] | Is it weird to laugh at my own jokes? [37 chars] |
| What is the best lie you ever spun? [35 chars] | What's the best-crafted lie you've ever told? [45 chars] |
| Why does Quora frequently suggest answers to my feed that put down Donald Trump? [80 chars] | Why does Quora only seem to have subjective, biased answers to questions about Donald Trump? [92 chars] |
| How can I make my self physically strong? [41 chars] | How do I make myself physically strong? [39 chars] |
| How will a quantum satellite work? [34 chars] | How does a Quantum satellite work and what would be some of its primary uses? [77 chars] |

### Source Reference Table

| Item | Reference |
| --- | --- |
| Source dataset | [Quora Question Pairs](https://kaggle.com/competitions/quora-question-pairs) |
| Retrieval benchmark framing | [BEIR](https://arxiv.org/abs/2104.08663) |
| Dataset documentation | [ir_datasets BEIR documentation](https://ir-datasets.com/beir) |
| NanoBEIR collection | [NanoBEIR on Hugging Face](https://huggingface.co/collections/zeta-alpha-ai/nanobeir) |
| NanoBEIR-en dataset | [hakari-bench/NanoBEIR-en](https://huggingface.co/datasets/hakari-bench/NanoBEIR-en) |

Representative query and duplicate-question snippets:

| Query | Positive question snippet |
| --- | --- |
| Is it okay to laugh at your own jokes? | Is it weird to laugh at my own jokes? |
| What is the best lie you ever spun? | What's the best-crafted lie you've ever told? |
| Why does Quora frequently suggest answers to my feed that put down Donald Trump? | Why does Quora only seem to have subjective, biased answers about Donald Trump? |
| How can I make my self physically strong? | How do I make myself physically strong? |
| How will a quantum satellite work? | How does a quantum satellite work and what would be some of its primary uses? |
