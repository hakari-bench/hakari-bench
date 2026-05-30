# NanoChemTEB / NanoChemNQ

## Overview

NanoChemNQ is the chemistry-filtered Natural Questions retrieval task from NanoChemTEB. Queries are English search-style questions, and relevant documents are Wikipedia passages about chemistry, biochemistry, materials, or chemical-adjacent science. The task measures whether a retriever can find the paragraph that contains the requested fact, not merely a topically related article.

## Details

### What the Original Data Measures

ChemTEB defines ChemNQRetrieval as a chemistry-related subset of Natural Questions. Natural Questions uses real search queries and Wikipedia answer passages, which explains the short, lowercase, search-like wording of many queries.

The task focuses on paragraph-level evidence selection. A query may ask about an enzyme suffix, ATP breakdown, proton pumping, periodic-table block names, iron absorption, hops, or crystal lattices. The correct passage must contain the specific answer relation.

### Observed Data Profile

The task contains 27 queries, 10,000 documents, and 35 relevance judgments. It has 1.30 positives per query on average, with a minimum of 1, a median of 1.0, a maximum of 3, and 7 multi-positive queries, or 25.93% of the set.

Queries average 54.00 characters, and documents average 481.24 characters. The split is small, so metrics are sensitive to individual queries. Documents are Wikipedia paragraphs with surrounding explanation rather than isolated answer strings.

### BM25 Evaluation Profile

BM25 reaches nDCG@10 of 0.4446, hit@10 of 0.6667, and recall@100 of 0.8857 using the top-500 BM25 candidate subset. Sparse retrieval works when the query contains a distinctive phrase such as reciprocal lattice, enzyme suffix, ATP, or electron transport chain.

The limitation is relation specificity. BM25 may retrieve a paragraph from the right article but the wrong section, or a passage with the same biochemical term but not the requested product, location, or naming explanation.

### Dense Evaluation Profile

The dense harrier-oss-270m run reaches nDCG@10 of 0.6184, hit@10 of 0.8519, and recall@100 of 0.9714. Dense retrieval is the strongest profile across the reported metrics. It improves top-10 ranking and nearly saturates recall@100.

This suggests that embedding similarity helps map search-like questions to the paragraph that answers the relation, especially when exact lexical overlap points to several nearby paragraphs.

### Reranking Hybrid Evaluation Profile

The reranking_hybrid candidate set reaches nDCG@10 of 0.5526, hit@10 of 0.7778, and recall@100 of 0.9714. It uses a top-100 candidate range with an optional rank-101 safeguard; this task has 1 safeguard row, candidate counts from 100 to 101, and a mean of 100.04 candidates.

Hybrid retrieval ties dense for recall@100 but trails dense for top-10 ordering. Sparse signals help coverage, while dense retrieval better orders the answer-bearing paragraphs.

### Metric Interpretation for Model Researchers

This is a dense-favorable chemistry-filtered QA retrieval task. BM25 is useful because scientific terms are distinctive, but dense retrieval is better at relation-level paragraph selection. Reranking_hybrid is valuable for candidate coverage but not the best observed first-page ranker.

Researchers should focus on paragraph specificity. Article-level topicality is not enough; the passage must contain the exact requested fact or relation.

### Query and Relevance Type Tendencies

Queries ask about reciprocal lattices, enzyme naming, ATP hydrolysis products, proton pumping in electron transport, hop growing regions, iron absorption, periodic-table block names, and related scientific facts. Positive documents are Wikipedia paragraphs containing the answer.

The relevance relation is answer-bearing evidence. Same-topic paragraphs are hard negatives when they omit the requested answer.

### Representative Failure Modes

Likely failures include retrieving the right article but wrong paragraph, over-ranking a passage with stronger term overlap but no answer, and confusing related biochemical or materials-science concepts.

BM25 is vulnerable to article-level lexical overlap. Dense retrieval can still over-match related scientific context. Hybrid retrieval improves coverage but needs reranking for exact evidence selection.

### Training Data That May Help

Useful training data includes non-overlapping Natural Questions long-answer retrieval pairs, chemistry-filtered Wikipedia QA retrieval, biomedical and chemical fact retrieval, and same-article hard negatives.

Synthetic data should generate short search-like questions from non-evaluation chemistry and biochemistry Wikipedia-style passages. Hard negatives should be topically close but answer-different.

### Model Improvement Notes

Strong systems should learn relation-specific evidence selection. Dense retrieval is the best observed profile, but same-article hard negatives and answer-span-aware reranking are likely important for further gains.

Because the Nano split is small, this task should be interpreted as a focused diagnostic rather than a broad estimate of chemistry QA performance.

## Example Data

### Public Sources

The task is based on ChemTEB's chemistry-filtered Natural Questions retrieval setting.

### Source Reference Table

| Item | Reference |
| --- | --- |
| ChemTEB paper | [ChemTEB](https://arxiv.org/abs/2412.00532) |
| Natural Questions paper | [Natural Questions](https://aclanthology.org/Q19-1026/) |
| Source dataset | [BASF-AI/ChemNQRetrieval](https://huggingface.co/datasets/BASF-AI/ChemNQRetrieval) |
| NanoChemTEB dataset | [hakari-bench/NanoChemTEB](https://huggingface.co/datasets/hakari-bench/NanoChemTEB) |

Representative query and positive source snippets:

| Query | Positive document snippet |
| --- | --- |
| the reciprocal lattice of an fcc crystal is | A reciprocal lattice passage states that the reciprocal of FCC is BCC. |
| suffix applied to the end of the name of enzymes | A biochemistry passage explains that the suffix "-ase" is used for enzyme names. |
| what is the breakdown product formed when one phosphate group is removed from atp | An ATP hydrolysis passage describes release of energy and products from ATP. |
| where does the electron transport chain pump protons | An electron transport chain passage describes proton movement during energy extraction. |
| where do they grow hops in the us | A hops passage discusses production in moist temperate climates and leading growing regions. |
