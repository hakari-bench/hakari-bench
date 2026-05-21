# MNanoBEIR / NanoBEIR-fr / NanoFiQA2018

## Overview

FiQA 2018 is a financial question answering retrieval benchmark.
`NanoBEIR-fr__NanoFiQA2018` is the French MNanoBEIR version: French translated
finance questions must retrieve French translated answer passages. The task
tests retrieval for consumer finance, investing, debt, and practical financial
reasoning.

## Details

### What the Original Data Measures

[FiQA: A Question Answering Dataset for Financial Opinion
Mining](https://doi.org/10.1145/3184558.3192301) introduced shared tasks around
financial opinion and question answering. BEIR uses FiQA as a financial
question-answering retrieval task, where the retriever must surface useful
answers from finance discussions.

[BEIR: A Heterogeneous Benchmark for Zero-shot Evaluation of Information
Retrieval Models](https://arxiv.org/abs/2104.08663) is important context
because FiQA adds a finance domain outside Wikipedia and general web QA.
[MMTEB: Massive Multilingual Text Embedding Benchmark](https://arxiv.org/abs/2502.13595)
provides the multilingual setting for this French split.

### Observed Data Profile

The sampled French Nano task has 50 queries, 4,598 documents, and 123 positive
qrel rows. Queries average 2.46 positives, and 28 of 50 queries have multiple
positives. The average query length is 82.20 characters, and the average
document length is 1,072.01 characters.

The inspected queries ask about buying an apartment in China, a deceased
co-signer, paying someone to invest, credit-card debt versus retirement matching,
and check number length. Documents are long explanatory finance answers with
assumptions and caveats.

### BM25 Difficulty

Using the dataset-provided BM25 candidate column, BM25 reaches nDCG@10 =
0.2754 and hit@10 = 0.4800. BM25 ranks a positive first for 11 queries, and
the median first-positive rank is 15.

This is difficult because financial questions often need scenario matching
rather than direct word overlap. Strong models should capture risk horizon,
legal role, debt tradeoff, account type, and practical advice.

### Training Data That May Help

Useful training data includes non-overlapping financial QA pairs, consumer
finance forum retrieval data, investment and debt advice pairs, and French or
multilingual finance-domain retrieval supervision. Training should exclude
FiQA, BEIR, NanoBEIR, or translated finance forum records likely to overlap
with these examples.

### Synthetic Data Guidance

For document-to-query generation, start from non-evaluation French finance
answers and generate realistic questions about mortgages, debt, investing,
retirement accounts, fees, taxes, and edge cases. Synthetic positives should
address the scenario, not merely share a product keyword.

## Example Data

| Query | Positive document |
| --- | --- |
| Quel type de rendements Vanguard indique-t-il ? (47 chars) | À partir de la page de Vanguard - Cela semblait être le plus simple, car les données S&P sont faciles à trouver. J'utilise MoneyChimp pour obtenir des informations - ce qui confirme que la page de Vanguard propose le taux de ... [truncated 225 chars](543 chars) |
| Quelles sont les implications fiscales du travail indépendant ? (63 chars) | Si vous avez un revenu aux États-Unis, vous devrez payer l'impôt sur le revenu américain. Sauf si un traité entre votre pays et les États-Unis en dispose autrement. (164 chars) |
| Qu'est-ce qui est considéré comme élevé ou bas en matière de volume ? (69 chars) | Le volume quotidien est généralement comparé au volume quotidien moyen des 50 derniers jours pour une action. Un volume élevé est généralement considéré comme étant 2 fois ou plus le volume quotidien moyen des 50 derniers jou ... [truncated 225 chars](765 chars) |
| Utiliser les points de fidélité de votre carte de crédit pour régler des dépenses professionnelles déductibles fiscalement (122 chars) | Pour simplifier, commençons par considérer uniquement le remboursement en espèces. En général, le remboursement en espèces des cartes de crédit pour un usage personnel n'est pas imposable, mais pour un usage professionnel, il ... [truncated 225 chars](4415 chars) |
| Comment dois-je déclarer mes impôts en tant que travailleur indépendant ? (73 chars) | Pour des raisons fiscales, vous devrez déclarer vos revenus en tant qu'employé (feuilles T4 et impôts retenus automatiquement), mais aussi en tant qu'entrepreneur. J'ai eu la même situation l'année dernière. "Employé et trava ... [truncated 225 chars](853 chars) |

## Dataset Information

| Field | Value |
| --- | --- |
| Nano set | MNanoBEIR |
| Backing dataset | NanoBEIR-fr |
| Task / split | NanoFiQA2018 |
| Hugging Face dataset | [hakari-bench/NanoBEIR-fr](https://huggingface.co/datasets/hakari-bench/NanoBEIR-fr) |
| Language | fr |
| Category | natural_language |
| Queries | 50 |
| Documents | 4,598 |
| Positive qrels | 123 |
| Avg positives / query | 2.46 |
| Positives per query (min / median / max) | 1 / 2.00 / 15 |
| Queries with multiple positives | 28 (56.0%) |
| BM25 nDCG@10 | 0.2754 |
| BM25 hit@10 | 0.4800 |
| Query length avg chars | 82.20 |
| Document length avg chars | 1,072.01 |

### Public Sources

- [FiQA: A Question Answering Dataset for Financial Opinion Mining](https://doi.org/10.1145/3184558.3192301).
- [BEIR: A Heterogeneous Benchmark for Zero-shot Evaluation of Information Retrieval Models](https://arxiv.org/abs/2104.08663).
- [MMTEB: Massive Multilingual Text Embedding Benchmark](https://arxiv.org/abs/2502.13595).
- [Zeta Alpha NanoBEIR collection](https://huggingface.co/collections/zeta-alpha-ai/nanobeir).

### Hugging Face Links

- Nano dataset: [hakari-bench/NanoBEIR-fr](https://huggingface.co/datasets/hakari-bench/NanoBEIR-fr)
- Source collection: [Zeta Alpha NanoBEIR collection](https://huggingface.co/collections/zeta-alpha-ai/nanobeir)

### Source Reference Table

| Title | Year | Type | URL |
| --- | ---: | --- | --- |
| FiQA: A Question Answering Dataset for Financial Opinion Mining | 2018 | task paper | https://doi.org/10.1145/3184558.3192301 |
| BEIR: A Heterogeneous Benchmark for Zero-shot Evaluation of Information Retrieval Models | 2021 | benchmark paper | https://arxiv.org/abs/2104.08663 |
| MMTEB: Massive Multilingual Text Embedding Benchmark | 2025 | benchmark paper | https://arxiv.org/abs/2502.13595 |
| NanoBEIR: Smaller BEIR dataset subsets | 2024 | dataset collection | https://huggingface.co/collections/zeta-alpha-ai/nanobeir |

## Machine-Readable Metadata

<!-- benchmark-task-metadata:v1 -->

```yaml
benchmark_task_metadata:
  schema_version: 1
  document_status: first_pass
  nano_set: MNanoBEIR
  backing_dataset: NanoBEIR-fr
  dataset_id: hakari-bench/NanoBEIR-fr
  task_name: NanoFiQA2018
  split_name: NanoFiQA2018
  language: fr
  category: natural_language
  document_path: docs/benchmark_tasks/MNanoBEIR/NanoBEIR-fr__NanoFiQA2018.md
  source_research:
    primary_source_type: task_paper
    paper_pdf_or_html_checked: true
    no_paper_note: null
  counts:
    queries: 50
    documents: 4598
    positive_qrels: 123
  positives_per_query:
    average: 2.46
    min: 1
    median: 2.0
    max: 15
    multi_positive_queries: 28
    multi_positive_query_percent: 56.0
  text_stats_chars:
    query_mean: 82.2
    document_mean: 1072.012179
  bm25:
    ndcg_at_10: 0.2753626647
    hit_at_10: 0.48
    source: dataset_bm25_column
```
