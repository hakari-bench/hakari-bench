# MNanoBEIR / NanoBEIR-fr / NanoFiQA2018

## Overview

This task is the French NanoBEIR version of FiQA 2018, a financial question answering retrieval benchmark. The original FiQA shared task focused on financial opinion mining and question answering, and BEIR uses it as a finance-domain passage retrieval task. In this NanoBEIR slice, French translated finance questions must retrieve French translated answer passages from 4,598 candidate documents. The task contains 50 queries and 123 positive relevance judgments, with an average of 2.46 positives per query. It is a compact benchmark for consumer finance retrieval, where models must match practical financial scenarios involving taxes, debt, investing, retirement accounts, fees, and risk rather than simply matching product names.

## Details

### What the Original Data Measures

FiQA measures retrieval for finance questions and answers. Many questions describe practical situations with assumptions, jurisdictional details, account types, tradeoffs, or caveats. Relevant answers may use different wording from the question while addressing the same financial decision. The task therefore rewards scenario understanding, financial terminology, and the ability to distinguish useful advice from merely related finance content.

### Observed Data Profile

The French Nano task has 50 queries, 4,598 documents, and 123 positives. Positives per query average 2.46, and 28 queries have multiple positives. Queries average about 82 characters, while documents average about 1,072 characters. The examples include Vanguard returns, tax implications of freelance work, high or low trading volume, credit-card reward points for deductible business expenses, and tax filing as a self-employed worker. Documents are explanatory finance answers with practical caveats.

### BM25 Evaluation Profile

BM25 reaches nDCG@10 of 0.340, Hit@10 of 0.560, and Recall@100 of 0.642. Sparse retrieval can match exact finance terms such as tax, Vanguard, volume, credit card, or self-employed status. It struggles when the relevant answer explains the underlying scenario with different vocabulary or when the query requires interpreting a financial tradeoff. BM25's moderate recall indicates that lexical terms help candidate discovery but are not enough for strong top ranking.

### Dense Evaluation Profile

The dense harrier-oss-270m baseline improves all metrics, reaching nDCG@10 of 0.388, Hit@10 of 0.680, and Recall@100 of 0.691. Dense retrieval better captures scenario-level similarity between a user question and a finance answer. It can connect questions about taxes, investment returns, or business expenses to passages that use explanatory language rather than matching the question phrase exactly. The remaining gap suggests that finance-domain reasoning and jurisdiction-sensitive caveats remain difficult.

### Reranking Hybrid Evaluation Profile

The reranking_hybrid profile is strongest, with nDCG@10 of 0.434, Hit@10 of 0.700, and Recall@100 of 0.740, with eight safeguard rows at 101 candidates. This is a clear hybrid-search pattern: BM25 preserves product names and financial terms, while dense retrieval captures advice intent and scenario similarity. The hybrid candidate set improves both top-10 ranking and recall, making it the best first-stage profile for this French FiQA slice.

### Metric Interpretation for Model Researchers

Because many queries have several positive answers, Hit@10 should be read as a first-useful-answer measure rather than full coverage. nDCG@10 reflects whether the best relevant advice appears early. Recall@100 matters for reranking pipelines because multiple answers may address different assumptions or caveats. The steady improvement from BM25 to dense to hybrid shows that both exact terminology and semantic scenario matching are needed.

### Query and Relevance Type Tendencies

Queries are French personal-finance questions. Relevant documents are long answer passages that may include assumptions, tax rules, account mechanics, and advice. Hard negatives can share a financial product or topic but differ in jurisdiction, account type, time horizon, or decision context. The task is sensitive to practical scenario matching rather than only topical similarity.

### Representative Failure Modes

BM25 can retrieve passages with the same product or tax keyword but the wrong scenario. Dense retrieval can retrieve plausible finance advice that misses a key constraint. Hybrid retrieval improves coverage but can still over-rank broad explanatory passages over a precise answer. Failure analysis should check whether the passage directly addresses the user's financial decision.

### Training and Leakage Considerations

Training should exclude FiQA, BEIR, NanoBEIR, and translated finance forum records likely to overlap with these examples. Useful non-overlapping data includes financial QA pairs, consumer finance forum retrieval data, investment and debt advice pairs, and French or multilingual finance-domain supervision. Multi-positive training is useful because several answers can be relevant to one financial question.

### Model Improvement Signals

Strong models should learn finance terminology and scenario reasoning. Useful signals include same-product hard negatives, jurisdiction-aware tax examples, debt and investment tradeoff pairs, and long answers with explicit assumptions. Hybrid systems should preserve exact finance terms while using dense similarity to recover answer passages written in different explanatory language.

## Example Data

| Query | Positive Document |
|---|---|
| Quel type de rendements Vanguard indique-t-il ? | À partir de la page de Vanguard - Cela semblait être le plus simple, car les données S&P sont faciles à trouver... |
| Quelles sont les implications fiscales du travail indépendant ? | Si vous avez un revenu aux États-Unis, vous devrez payer l'impôt sur le revenu américain... |
| Qu'est-ce qui est considéré comme élevé ou bas en matière de volume ? | Le volume quotidien est généralement comparé au volume quotidien moyen des 50 derniers jours pour une action... |
| Utiliser les points de fidélité de votre carte de crédit pour régler des dépenses professionnelles déductibles fiscalement | Pour simplifier, commençons par considérer uniquement le remboursement en espèces... |
| Comment dois-je déclarer mes impôts en tant que travailleur indépendant ? | Pour des raisons fiscales, vous devrez déclarer vos revenus en tant qu'employé et aussi en tant qu'entrepreneur... |

## Public Sources

- [FiQA paper](https://doi.org/10.1145/3184558.3192301)
- [BEIR benchmark](https://github.com/beir-cellar/beir)
- [MMTEB benchmark](https://arxiv.org/abs/2502.13595)
- [NanoBEIR dataset](https://huggingface.co/collections/zeta-alpha-ai/nanobeir)

## Source Reference Table

| Label | URL |
|---|---|
| FiQA paper | https://doi.org/10.1145/3184558.3192301 |
| BEIR benchmark | https://github.com/beir-cellar/beir |
| MMTEB benchmark | https://arxiv.org/abs/2502.13595 |
| NanoBEIR dataset | https://huggingface.co/collections/zeta-alpha-ai/nanobeir |
