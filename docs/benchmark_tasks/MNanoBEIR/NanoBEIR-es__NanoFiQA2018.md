# MNanoBEIR / NanoBEIR-es / NanoFiQA2018

## Overview

FiQA 2018 is a financial question answering retrieval benchmark.
`NanoBEIR-es__NanoFiQA2018` is the Spanish MNanoBEIR version: Spanish
translated finance questions must retrieve Spanish translated answer passages.
The task tests retrieval for consumer finance and investment questions with
domain-specific reasoning.

## Details

### What the Original Data Measures

[FiQA: A Question Answering Dataset for Financial Opinion
Mining](https://doi.org/10.1145/3184558.3192301) introduced shared tasks around
financial opinion and question answering. In the BEIR retrieval framing, FiQA
is used as a financial question-answering retrieval task where user questions
must retrieve relevant answers from finance discussions.

[BEIR: A Heterogeneous Benchmark for Zero-shot Evaluation of Information
Retrieval Models](https://arxiv.org/abs/2104.08663) includes FiQA as a
question-answering retrieval task outside Wikipedia and general web QA. [MMTEB:
Massive Multilingual Text Embedding Benchmark](https://arxiv.org/abs/2502.13595)
provides the multilingual context for this Spanish Nano split.

### Observed Data Profile

The sampled Spanish Nano task has 50 queries, 4,598 documents, and 123 positive
qrel rows. Queries average 2.46 positives, and 28 queries have multiple
positives. The average query length is 70.34 characters, and the average
document length is 993.55 characters.

The inspected queries ask about buying property in China, a deceased co-signer,
hiring someone to invest and share gains, paying credit card debt versus a
401(k) match, and check number length. Documents are Spanish translated finance
answers with practical caveats and long explanatory reasoning.

### BM25 Difficulty

Using the dataset-provided BM25 candidate column, BM25 reaches nDCG@10 =
0.2720 and hit@10 = 0.4600. BM25 ranks a positive first for 14 queries, and
the median first-positive rank is 20.

This is difficult for lexical retrieval because financial answers often use
different vocabulary from the question and include conditional advice. Strong
models should capture the underlying financial issue, risk horizon, legal role,
or debt tradeoff rather than only matching surface terms.

### Training Data That May Help

Useful training data includes non-overlapping financial QA pairs, consumer
finance forum retrieval data, investment and debt advice question-answer pairs,
and Spanish or multilingual finance-domain retrieval supervision.

Training should exclude FiQA, BEIR, NanoBEIR, or translated finance forum
records likely to overlap with these evaluation questions or answers.

### Synthetic Data Guidance

For document-to-query generation, start from non-evaluation Spanish finance
answers and generate realistic user questions. Include mortgages, debt,
co-signing, investing, retirement accounts, fees, taxes, and personal finance
edge cases.

For joint generation, create answer passages with explicit assumptions and
generate questions that require matching the advice scenario, not just a shared
financial keyword.

## Example Data

| Query | Positive document |
| --- | --- |
| ¿Qué tipo de rentabilidad está ofreciendo Vanguard? (51 chars) | De la página de Vanguard - Pareció la opción más sencilla, ya que los datos de S&P son fáciles de encontrar. Utilizo MoneyChimp para verificar, lo que confirma que la página de Vanguard ofrece la Tasa de Crecimiento Anual Com ... [truncated 225 chars](525 chars) |
| Implicaciones fiscales del trabajo freelance (44 chars) | Si tienes ingresos en EE.UU., deberás pagar impuestos sobre la renta en EE.UU. a menos que exista un tratado con tu país que lo indique. (136 chars) |
| ¿Qué se entiende por volumen alto o bajo? (41 chars) | El volumen diario generalmente se compara con el volumen promedio diario de los últimos 50 días para una acción. Un volumen alto generalmente se considera que es 2 o más veces el volumen promedio diario de los últimos 50 días ... [truncated 225 chars](723 chars) |
| Canjear puntos de tarjeta de crédito para cubrir gastos empresariales deducibles (80 chars) | Para simplificar, empecemos considerando solo el reembolso en efectivo. En general, el reembolso en efectivo de las tarjetas de crédito para uso personal no es gravable, pero para uso empresarial sí lo es (más o menos, lo exp ... [truncated 225 chars](4025 chars) |
| ¿Cómo debo declarar mis impuestos como autónomo? (48 chars) | Para efectos fiscales, deberás presentar tus impuestos como empleado (usando tus talones T4 y con retenciones automáticas) y también como emprendedor. Yo tuve la misma situación el año pasado. "Empleado y trabajador independi ... [truncated 225 chars](780 chars) |

## Dataset Information

| Field | Value |
| --- | --- |
| Nano set | MNanoBEIR |
| Backing dataset | NanoBEIR-es |
| Task / split | NanoFiQA2018 |
| Hugging Face dataset | [hakari-bench/NanoBEIR-es](https://huggingface.co/datasets/hakari-bench/NanoBEIR-es) |
| Language | es |
| Category | natural_language |
| Queries | 50 |
| Documents | 4,598 |
| Positive qrels | 123 |
| Avg positives / query | 2.46 |
| Positives per query (min / median / max) | 1 / 2.00 / 15 |
| Queries with multiple positives | 28 (56.0%) |
| BM25 nDCG@10 | 0.3205 |
| BM25 hit@10 | 0.5800 |
| BM25 Recall@100 | 0.6667 |
| BM25 candidate subset | top-500 (`bm25`) |
| Dense nDCG@10 | 0.3819 |
| Dense hit@10 | 0.6400 |
| Dense Recall@100 | 0.7398 |
| Dense candidate subset | top-500 (`harrier_oss_v1_270m`) |
| Reranking hybrid nDCG@10 | 0.4174 |
| Reranking hybrid hit@10 | 0.7000 |
| Reranking hybrid Recall@100 | 0.7805 |
| Reranking hybrid candidate subset | top-100 plus optional rank-101 safeguard (`reranking_hybrid`) |
| Reranking hybrid candidates / query | 100-101 |
| Reranking hybrid safeguard rows | 4 |
| Query length avg chars | 70.34 |
| Document length avg chars | 993.55 |

### Public Sources

- [FiQA: A Question Answering Dataset for Financial Opinion Mining](https://doi.org/10.1145/3184558.3192301); 2018; Maciej Maia, Siegfried Handschuh, André Freitas, Brian Davis, Ross McDermott, Manel Zarrouk, Alexandra Balahur; DOI: `10.1145/3184558.3192301`.
- [BEIR: A Heterogeneous Benchmark for Zero-shot Evaluation of Information Retrieval Models](https://arxiv.org/abs/2104.08663); 2021; Nandan Thakur, Nils Reimers, Andreas Rueckle, Abhishek Srivastava, Iryna Gurevych; DOI: `10.48550/arXiv.2104.08663`.
- [MMTEB: Massive Multilingual Text Embedding Benchmark](https://arxiv.org/abs/2502.13595); 2025; Kenneth Enevoldsen, Isaac Chung, Imene Kerboua, Marton Kardos, Ashwin Mathur, and others; DOI: `10.48550/arXiv.2502.13595`.
- [Zeta Alpha NanoBEIR collection](https://huggingface.co/collections/zeta-alpha-ai/nanobeir).

### Hugging Face Links

- Nano dataset: [hakari-bench/NanoBEIR-es](https://huggingface.co/datasets/hakari-bench/NanoBEIR-es)
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
  backing_dataset: NanoBEIR-es
  dataset_id: hakari-bench/NanoBEIR-es
  task_name: NanoFiQA2018
  split_name: NanoFiQA2018
  language: es
  category: natural_language
  document_path: docs/benchmark_tasks/MNanoBEIR/NanoBEIR-es__NanoFiQA2018.md
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
    query_mean: 70.34
    document_mean: 993.551109
  bm25:
    ndcg_at_10: 0.3205376270981585
    hit_at_10: 0.58
    source: dataset_candidate_subset
  learning:
    original_train_split: available
    evaluation_split_origin: MNanoBEIR Spanish NanoBEIR task split from hakari-bench/NanoBEIR-es
    train_eval_overlap_audit: not_audited
    leakage_note: prefer excluding FiQA, BEIR, or NanoBEIR records likely to overlap
      with these evaluation questions or answers
    useful_training_data:
    - non-overlapping financial QA pairs
    - consumer finance forum retrieval data
    - investment and debt advice question-answer pairs
    - Spanish or multilingual finance-domain retrieval supervision
    synthetic_data:
      document_generation: Spanish personal finance answer passages with practical
        caveats
      question_generation: realistic finance questions about debt, investing, accounts,
        taxes, and risk
      answerability: positives should address the financial scenario, not merely mention
        the same product
    multi_positive_training: useful
  links:
    nano_dataset: https://huggingface.co/datasets/hakari-bench/NanoBEIR-es
    source_urls:
    - label: FiQA paper
      url: https://doi.org/10.1145/3184558.3192301
    - label: BEIR paper
      url: https://arxiv.org/abs/2104.08663
    - label: MMTEB paper
      url: https://arxiv.org/abs/2502.13595
    - label: Zeta Alpha NanoBEIR collection
      url: https://huggingface.co/collections/zeta-alpha-ai/nanobeir
    source_notes:
    - Spanish task is a multilingual NanoBEIR adaptation of the original English BEIR
      task
  references:
  - title: 'FiQA: A Question Answering Dataset for Financial Opinion Mining'
    url: https://doi.org/10.1145/3184558.3192301
    year: 2018
    doi: 10.1145/3184558.3192301
    is_paper: true
    source_confidence: definitive_paper_link
  - title: 'BEIR: A Heterogeneous Benchmark for Zero-shot Evaluation of Information
      Retrieval Models'
    url: https://arxiv.org/abs/2104.08663
    year: 2021
    doi: 10.48550/arXiv.2104.08663
    is_paper: true
    source_confidence: benchmark_context_paper
  - title: 'MMTEB: Massive Multilingual Text Embedding Benchmark'
    url: https://arxiv.org/abs/2502.13595
    year: 2025
    doi: 10.48550/arXiv.2502.13595
    is_paper: true
    source_confidence: benchmark_context_paper
  - title: 'NanoBEIR: Smaller BEIR dataset subsets'
    url: https://huggingface.co/collections/zeta-alpha-ai/nanobeir
    year: 2024
    doi: null
    is_paper: false
    source_confidence: dataset_collection
  candidate_subsets:
    bm25:
      config: bm25
      label: BM25
      source: dataset_candidate_subset
      top_k: 500
      ndcg_at_10: 0.3205376271
      hit_at_10: 0.58
      recall_at_100: 0.6666666667
      candidate_count_min: 500
      candidate_count_max: 500
      candidate_count_mean: 500.0
      query_count: 50
      query_coverage: 1.0
      relevant_coverage_at_100: 0.6666666667
    dense:
      config: harrier_oss_v1_270m
      label: Dense
      source: dataset_candidate_subset
      top_k: 500
      ndcg_at_10: 0.3819415207
      hit_at_10: 0.64
      recall_at_100: 0.7398373984
      candidate_count_min: 500
      candidate_count_max: 500
      candidate_count_mean: 500.0
      query_count: 50
      query_coverage: 1.0
      relevant_coverage_at_100: 0.7398373984
    reranking_hybrid:
      config: reranking_hybrid
      label: Reranking hybrid
      source: dataset_candidate_subset
      top_k: 100
      ndcg_at_10: 0.4173531376
      hit_at_10: 0.7
      recall_at_100: 0.7804878049
      candidate_count_min: 100
      candidate_count_max: 101
      candidate_count_mean: 100.08
      query_count: 50
      query_coverage: 1.0
      relevant_coverage_at_100: 0.7804878049
      safeguard_positive_rows: 4
      rows_with_101_candidates: 4
```
