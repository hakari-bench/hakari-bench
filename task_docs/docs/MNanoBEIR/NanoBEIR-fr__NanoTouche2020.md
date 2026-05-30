# MNanoBEIR / NanoBEIR-fr / NanoTouche2020

## Overview

This task is the French NanoBEIR version of Touché 2020, an argument retrieval benchmark for controversial questions. The original CLEF Touché task focuses on retrieving arguments for socially important topics and everyday decision questions, where relevance depends on both topic match and argumentative content. In this NanoBEIR slice, French translated controversial questions must retrieve French translated debate-style argument documents from 5,745 candidates. The task contains 49 queries and 932 positive relevance judgments. Every query has multiple positives, averaging 19.02 relevant arguments. It is a compact benchmark for pro/con coverage, argument relevance, and ranking long argumentative documents rather than short answer passages.

## Details

### What the Original Data Measures

Touché 2020 measures argument retrieval. A relevant document should address the controversial question with a substantive argument, stance, reason, example, or evidence. Topical mention alone is not enough. For queries about homework, prescription drug advertising, child vaccination, abortion, or standardized testing, a good retriever should surface documents that actually argue the issue.

### Observed Data Profile

The French Nano task has 49 queries, 5,745 documents, and 932 positives. Every query is multi-positive, with 6 to 32 positives and a median of 19. Queries average about 60 characters, while documents are long, averaging about 2,488 characters. Example queries ask whether homework is useful, whether prescription drugs should be advertised directly to consumers, which vaccines children should receive, whether abortion should be legal, and whether standardized tests improve education.

### BM25 Evaluation Profile

BM25 is strong, with nDCG@10 of 0.561, Hit@10 of 1.000, and Recall@100 of 0.791. The perfect Hit@10 reflects strong topic terms and many positives per query. Sparse matching is very effective at finding at least one relevant argument for every topic. However, ranking remains meaningful because argument retrieval should prioritize substantive arguments, not only documents that mention the same controversial issue.

### Dense Evaluation Profile

The dense harrier-oss-270m baseline reaches nDCG@10 of 0.473, Hit@10 of 0.959, and Recall@100 of 0.752. Dense retrieval is weaker than BM25 in this French sample, suggesting that exact topic anchoring is especially important. Embedding similarity can retrieve broad opinion text or adjacent policy discussions that are semantically related but not as directly responsive to the query.

### Reranking Hybrid Evaluation Profile

The reranking_hybrid profile is strongest overall, with nDCG@10 of 0.576, Hit@10 of 1.000, and Recall@100 of 0.827. It preserves BM25's complete first-page coverage while improving both nDCG and recall. This is a clear hybrid-search case: BM25 anchors the central issue, while dense retrieval broadens coverage to arguments that use different wording or stance framing.

### Metric Interpretation for Model Researchers

Hit@10 is saturated for BM25 and hybrid, so nDCG@10 and Recall@100 are more useful. nDCG@10 measures whether strong relevant arguments appear early. Recall@100 measures whether the candidate set covers a broad pro/con space. Because every query has many positives, a system that retrieves only one argument is incomplete even if Hit@10 is high.

### Query and Relevance Type Tendencies

Queries are concise French controversial questions. Relevant documents are long debate arguments, often with claims, reasons, examples, and persuasive framing. Positives can cover different sides of the issue, so retrieval should favor coverage and diversity. Hard negatives may mention the same topic but fail to address the central question argumentatively.

### Representative Failure Modes

BM25 can over-rank long documents that repeat the topic without strong argumentative content. Dense retrieval can retrieve broad opinion pieces that do not answer the specific question. Hybrid retrieval improves coverage but may still underrepresent one side of the debate. Failure analysis should check argument substance and stance coverage, not just topic match.

### Training and Leakage Considerations

Training should exclude Touché 2020, BEIR, NanoBEIR, and translated argument documents likely to overlap with these topics or documents. Useful non-overlapping data includes debate portal argument collections, pro/con retrieval pairs, argument quality ranking data, and French or multilingual controversial-topic retrieval supervision. Multi-positive training is required because every query has many relevant arguments.

### Model Improvement Signals

Strong models should preserve exact issue matching while learning argumentative relevance and stance coverage. Useful signals include same-topic non-argument hard negatives, stance-diverse positives, paired pro/con arguments, and long-document argument ranking. Hybrid systems are well suited because they combine topic anchoring with semantic argument expansion.

## Example Data

| Query | Positive Document |
|---|---|
| Les devoirs sont-ils utiles ? | Premièrement, voici trois arguments en faveur du maintien des devoirs dans les écoles modernes... |
| Les médicaments sur ordonnance doivent-ils être publicisés directement auprès des consommateurs ? | De nombreuses publicités ne fournissent pas suffisamment d'informations sur l'efficacité des médicaments... |
| Quels vaccins les enfants doivent-ils recevoir ? | Ce n'est pas encore un dossier complet... Les gouvernements ne devraient pas avoir le droit d'intervenir... |
| L'avortement devrait-il être légal ? | Les avortements devraient être légaux, car la personnalité juridique commence après que le fœtus devient viable... |
| Les tests standardisés améliorent-ils l'éducation ? | Le SAT, l'ACT et autres tests standardisés fournissent plus d'informations sur la préparation d'un élève... |

## Public Sources

- [Touché 2020 overview](https://doi.org/10.1007/978-3-030-58219-7_26)
- [Touché 2020 dataset](https://doi.org/10.5281/zenodo.6862281)
- [BEIR benchmark](https://github.com/beir-cellar/beir)
- [MMTEB benchmark](https://arxiv.org/abs/2502.13595)
- [NanoBEIR dataset](https://huggingface.co/collections/zeta-alpha-ai/nanobeir)

## Source Reference Table

| Label | URL |
|---|---|
| Touché 2020 overview | https://doi.org/10.1007/978-3-030-58219-7_26 |
| Touché 2020 dataset | https://doi.org/10.5281/zenodo.6862281 |
| BEIR benchmark | https://github.com/beir-cellar/beir |
| MMTEB benchmark | https://arxiv.org/abs/2502.13595 |
| NanoBEIR dataset | https://huggingface.co/collections/zeta-alpha-ai/nanobeir |
