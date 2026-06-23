# MNanoBEIR / NanoBEIR-it / NanoFiQA2018

## Overview

This task is the Italian NanoBEIR version of FiQA 2018, a financial question-answer retrieval benchmark. The original FiQA data was created for financial opinion mining and question answering, and BEIR uses its retrieval form as a finance-domain QA task. In this NanoBEIR slice, Italian translated personal-finance questions must retrieve Italian translated answer passages from 4,598 candidate documents. The task contains 50 queries and 123 positive relevance judgments, with an average of 2.46 positives per query. It is a compact benchmark for finance-domain retrieval, where models must match practical tax, investing, debt, pricing, and account questions to explanatory answers that may use different wording and include scenario-specific caveats.

## Details

### What the Original Data Measures

FiQA measures retrieval of useful finance answers for user questions. Many queries describe practical decisions or definitions rather than simple facts. Relevant answers may explain assumptions, jurisdictional details, account mechanics, tax treatment, investment returns, or debt tradeoffs. The task therefore rewards scenario matching and financial semantics, not just keyword overlap.

### Observed Data Profile

The Italian Nano task has 50 queries, 4,598 documents, and 123 positives. Positives per query average 2.46, and 28 queries have multiple positives. Queries average about 75 characters, while documents average about 1,005 characters. Example queries ask about Vanguard returns, tax implications of self-employment, high or low stock volume, using credit-card points for deductible business expenses, and filing taxes as a self-employed worker.

### BM25 Evaluation Profile

BM25 is weak, with nDCG@10 of 0.263, Hit@10 of 0.480, and Recall@100 of 0.577. Lexical overlap alone often fails because financial answers may address the same decision using different terminology. BM25 can retrieve passages that share a product or tax term but miss the user's scenario. The median rank pattern in the existing data shows that positives are frequently outside the first page.

### Dense Evaluation Profile

The dense harrier-oss-270m baseline is clearly stronger, with nDCG@10 of 0.344, Hit@10 of 0.640, and Recall@100 of 0.740. Dense retrieval better captures finance-domain scenario similarity and answer intent. It can connect questions about taxes, investing, expenses, or account rules to explanatory passages that do not repeat the query exactly. This makes dense retrieval the best top-ranking profile for this Italian FiQA slice.

### Reranking Hybrid Evaluation Profile

The reranking_hybrid profile reaches nDCG@10 of 0.340, Hit@10 of 0.620, and Recall@100 of 0.756, with five safeguard rows at 101 candidates. It gives the best Recall@100 but slightly trails dense retrieval on nDCG@10 and Hit@10. This suggests that hybrid search is useful for candidate generation, while dense retrieval is better calibrated for ranking the first page. BM25 contributes exact financial terms, but dense similarity drives most of the quality.

### Metric Interpretation for Model Researchers

Because many queries have multiple positives, Hit@10 indicates whether at least one useful answer was found, not whether the model covered all relevant advice. nDCG@10 measures whether high-quality answers appear early. Recall@100 matters for reranking pipelines and for multi-answer finance questions where different answers may cover different assumptions. The dense and hybrid profiles show a tradeoff between top-rank quality and coverage.

### Query and Relevance Type Tendencies

Queries are Italian personal-finance questions involving taxes, investing, volume, credit cards, business deductions, and self-employment. Relevant documents are long forum-style answers. Hard negatives may share financial terms but answer a different jurisdiction, account type, risk horizon, or practical decision. The task is sensitive to domain semantics and scenario constraints.

### Representative Failure Modes

BM25 can retrieve text with matching financial terms but the wrong decision context. Dense retrieval can retrieve plausible financial advice that misses a key assumption. Hybrid retrieval improves recall but can still rank broad advice above a precise answer. Failure analysis should check whether the passage directly answers the user's financial scenario.

### Training and Leakage Considerations

Training should exclude FiQA, BEIR, NanoBEIR, and translated answer passages that may overlap. Useful non-overlapping data includes financial QA, Italian finance forum retrieval, tax and investing question-answer pairs, and multilingual finance retrieval data. Multi-positive training is useful because many finance questions have several relevant answers.

### Model Improvement Signals

Strong models should improve scenario-level financial matching and preserve exact product terminology. Useful signals include same-product hard negatives, jurisdiction-sensitive tax examples, investment and debt tradeoff pairs, and long answers with explicit assumptions. Hybrid systems should use sparse matching for financial terms and dense retrieval for answer intent.

## Example Data

| Query | Positive document |
| --- | --- |
| Quali tipi di rendimenti sta indicando Vanguard? [48 chars] | Dalla pagina di Vanguard - Questo sembrava il più semplice da trovare, poiché i dati S&P sono facilmente reperibili. Utilizzo MoneyChimp per verificare - che conferma che la pagina di Vanguard offre i... [200 / 463 chars] |
| Quali sono le implicazioni fiscali del lavoro autonomo? [55 chars] | Se hai reddito negli Stati Uniti, dovrai pagare le tasse sul reddito negli Stati Uniti, a meno che non ci sia un accordo tra il tuo paese e gli Stati Uniti che stabilisce diversamente. [184 chars] |
| Cosa si intende per volume alto o basso? [40 chars] | Il volume giornaliero viene solitamente confrontato con il volume medio giornaliero degli ultimi 50 giorni per un'azione. Un volume elevato è generalmente considerato pari a 2 o più volte il volume me... [200 / 757 chars] |
| Utilizzare i punti accumulati con la carta di credito per pagare le spese aziendali detraibili [94 chars] | Per semplicità, iniziamo considerando solo il cashback. In generale, il cashback dalle carte di credito per uso personale non è tassabile, mentre per uso aziendale lo è (più o meno, spiegherò dopo). L... [200 / 3,942 chars] |
| Come dovrei fare la dichiarazione dei redditi come lavoratore autonomo? [71 chars] | Per scopi fiscali, dovrai dichiarare sia come dipendente (moduli T4 e ritenute fiscali automatiche) sia come imprenditore. Mi sono trovato nella stessa situazione l'anno scorso. "Dipendente e lavorato... [200 / 808 chars] |

## Public Sources

- [FiQA paper](https://doi.org/10.1145/3184558.3192301)
- [BEIR benchmark](https://github.com/beir-cellar/beir)
- [MMTEB benchmark](https://arxiv.org/abs/2502.13595)
- [NanoBEIR dataset](https://huggingface.co/collections/zeta-alpha-ai/nanobeir)

## Source Reference Table

| Label | URL |
|---|---|
| FiQA paper (https://doi.org/10.1145/3184558.3192301) |
| BEIR benchmark (https://github.com/beir-cellar/beir) |
| MMTEB benchmark (https://arxiv.org/abs/2502.13595) |
| NanoBEIR dataset (https://huggingface.co/collections/zeta-alpha-ai/nanobeir) |
