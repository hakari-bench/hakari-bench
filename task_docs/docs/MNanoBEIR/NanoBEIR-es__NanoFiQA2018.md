# MNanoBEIR / NanoBEIR-es / NanoFiQA2018

## Overview

This task is the Spanish NanoBEIR version of FiQA 2018, a financial question answering retrieval benchmark. The original FiQA shared task focused on financial opinion mining and question answering, and BEIR uses it as a domain-specific retrieval task where finance questions must retrieve relevant answer passages. In this NanoBEIR slice, Spanish translated finance questions are matched against 4,598 Spanish translated answer documents. The task contains 50 queries and 123 positive relevance judgments, with an average of 2.46 positives per query. It is a compact test of consumer finance retrieval, where models must understand practical scenarios involving debt, investing, taxes, retirement accounts, credit cards, and financial risk rather than simply matching product names.

## Details

### What the Original Data Measures

FiQA measures retrieval for finance-related questions and answers. Many questions describe practical personal-finance situations, often with assumptions, legal or tax conditions, and tradeoffs. Relevant answers may include caveats, conditional advice, and domain-specific terminology. The retrieval problem is therefore different from open-domain Wikipedia QA: the model must match a financial scenario to advice that addresses the same decision or constraint.

### Observed Data Profile

The Spanish Nano task has 50 queries, 4,598 documents, and 123 positives. Positives per query average 2.46, with 28 queries having multiple positives and a maximum of 15. Queries average about 70 characters, while documents average about 994 characters. The examples include Vanguard returns, freelance tax implications, high or low trading volume, redeeming credit card points for deductible business expenses, and self-employment tax filing. Documents are explanatory finance answers, often with practical caveats.

### BM25 Evaluation Profile

BM25 reaches nDCG@10 of 0.321, Hit@10 of 0.580, and Recall@100 of 0.667. This is a moderate sparse profile. BM25 can find answers when questions share terms such as credit card, taxes, 401(k), volume, or Vanguard. It struggles when the answer uses different financial vocabulary, explains a conditional scenario, or discusses the underlying concept rather than repeating the question wording. Query terms alone often do not capture the user's financial intent.

### Dense Evaluation Profile

The dense harrier-oss-270m baseline improves all metrics, with nDCG@10 of 0.382, Hit@10 of 0.640, and Recall@100 of 0.740. This indicates that embedding similarity is useful for matching financial situations to explanatory answers. Dense retrieval can connect questions about debt tradeoffs, investment delegation, taxes, or account rules to passages that use different wording but address the same scenario. The remaining gap shows that general dense models still need stronger finance-domain reasoning and scenario matching.

### Reranking Hybrid Evaluation Profile

The reranking_hybrid profile is strongest, with nDCG@10 of 0.417, Hit@10 of 0.700, and Recall@100 of 0.780, with four safeguard rows at 101 candidates. This is a clear case where hybrid search outperforms either signal alone. BM25 contributes exact financial terms and product names, while dense retrieval contributes scenario-level similarity. The combined result improves both candidate coverage and top-10 ranking, which is important for practical finance QA retrieval.

### Metric Interpretation for Model Researchers

Because many queries have more than one relevant answer, Hit@10 should be treated as a first-evidence measure, not a full task score. nDCG@10 captures whether good answers appear early, while Recall@100 measures whether a reranker or reader has enough relevant answers to work with. The steady improvement from BM25 to dense to hybrid suggests that both lexical finance terminology and semantic scenario matching are important.

### Query and Relevance Type Tendencies

Queries are user-style financial questions. They may be short, but they often imply a scenario involving taxes, investment products, debt priority, legal responsibility, or account mechanics. Relevant documents are answer passages that address the scenario directly. Hard negatives can share financial keywords while giving advice for a different jurisdiction, account type, time horizon, or risk assumption.

### Representative Failure Modes

BM25 can retrieve passages with the same product or tax keyword but the wrong scenario. Dense retrieval can retrieve financially related advice that sounds plausible but does not answer the specific constraint. Hybrid retrieval improves both but can still over-rank broad advice over a narrower correct answer. Failure analysis should check whether the retrieved passage would actually help the user make the decision described by the query.

### Training and Leakage Considerations

Training should exclude FiQA, BEIR, NanoBEIR, and translated finance forum records likely to overlap with these questions or answers. Useful non-overlapping data includes financial QA pairs, consumer finance forum retrieval data, investment and debt advice pairs, and Spanish or multilingual finance-domain supervision. Multi-positive training is useful because several answers can be valid for one question.

### Model Improvement Signals

Strong models should learn finance-domain terminology and scenario-level reasoning. Useful training signals include hard negatives with the same financial product but a different issue, jurisdiction-sensitive tax examples, debt and investment tradeoff pairs, and long answer passages with explicit assumptions. Hybrid retrieval is well suited because it preserves exact product names while using dense similarity for advice intent.

## Example Data

| Query | Positive Document |
|---|---|
| ¿Qué tipo de rentabilidad está ofreciendo Vanguard? | De la página de Vanguard: pareció la opción más sencilla, ya que los datos de S&P son fáciles de encontrar... |
| Implicaciones fiscales del trabajo freelance | Si tienes ingresos en EE.UU., deberás pagar impuestos sobre la renta en EE.UU. a menos que exista un tratado... |
| ¿Qué se entiende por volumen alto o bajo? | El volumen diario generalmente se compara con el volumen promedio diario de los últimos 50 días para una acción... |
| Canjear puntos de tarjeta de crédito para cubrir gastos empresariales deducibles | Para simplificar, empecemos considerando solo el reembolso en efectivo. En general, el reembolso en efectivo de las tarjetas de crédito... |
| ¿Cómo debo declarar mis impuestos como autónomo? | Para efectos fiscales, deberás presentar tus impuestos como empleado y también como emprendedor... |

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
