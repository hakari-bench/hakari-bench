# MNanoBEIR / NanoBEIR-es / NanoSciFact

## Overview

SciFact is a scientific claim verification dataset. `NanoBEIR-es__NanoSciFact`
is the Spanish MNanoBEIR version: Spanish translated scientific claims must
retrieve Spanish translated abstracts that support or refute the claim. The task
tests evidence retrieval in research literature with domain-specific scientific
terminology.

## Details

### What the Original Data Measures

[Fact or Fiction: Verifying Scientific Claims](https://arxiv.org/abs/2004.14974)
introduces SciFact as a dataset of expert-written scientific claims paired with
evidence-containing abstracts annotated with support or refute labels and
rationales. The paper derives claims from citation sentences, making the claims
natural assertions about scientific findings rather than generic factoid
questions.

[BEIR: A Heterogeneous Benchmark for Zero-shot Evaluation of Information
Retrieval Models](https://arxiv.org/abs/2104.08663) includes SciFact as a
fact-checking retrieval task. [MMTEB: Massive Multilingual Text Embedding
Benchmark](https://arxiv.org/abs/2502.13595) provides the multilingual context
for this Spanish Nano split.

### Observed Data Profile

The sampled Spanish Nano task has 50 queries, 2,919 documents, and 56 positive
qrel rows. Most queries have one positive abstract, while 4 queries have
multiple positives. The average query length is 113.56 characters, and the
average document length is 1,644.20 characters.

The inspected claims involve breast cancer risk, brown adipose tissue, T-cell
receptor diversity, disease models, and G-quadruplex biology. Positive
documents are Spanish translated scientific abstracts with study context,
methods, and findings.

### BM25 Difficulty

Using the dataset-provided BM25 candidate column, BM25 reaches nDCG@10 =
0.6605 and hit@10 = 0.7800. BM25 ranks a positive first for 30 queries, and
the median first-positive rank is 1.

Lexical matching is often strong because scientific claims repeat technical
terms from the abstracts. Harder cases require recognizing evidence despite
abbreviations, different phrasing, or experimental context. Retrieval should be
interpreted separately from the later support/refute decision.

### Training Data That May Help

Useful training data includes non-overlapping SciFact-style claim-evidence
pairs, scientific fact verification data, biomedical abstract retrieval pairs,
CORD-19 style claim retrieval, and Spanish or multilingual scientific NLI or
evidence selection data.

Training should exclude SciFact, BEIR, NanoBEIR, or translated abstracts and
claims likely to overlap with these evaluation records.

### Synthetic Data Guidance

For document-to-query generation, start from non-evaluation scientific abstracts
and generate Spanish claims that are supported or refuted by the abstract.
Claims should be atomic and verifiable.

For joint generation, create abstracts with clear findings plus related hard
negative abstracts mentioning the same disease, gene, or intervention but not
providing the needed evidence.

## Example Data

| Query | Positive document |
| --- | --- |
| Ly49Q dirige la migración de los neutrófilos hacia áreas inflamadas regulando las funciones de las balsas lipídicas. (116 chars) | Los neutrófilos rápidamente sufren polarización y movimiento direccional para infiltrarse en los sitios de infección e inflamación. Aquí mostramos que un receptor inhibidor de MHC I, Ly49Q, fue crucial para la rápida polariza ... [truncated 225 chars](1125 chars) |
| La terapia antirretroviral reduce las tasas de tuberculosis en diferentes niveles de CD4. (89 chars) | ANTECEDENTES La infección por el virus de la inmunodeficiencia humana (VIH) es el factor de riesgo más fuerte para desarrollar tuberculosis y ha impulsado su resurgimiento, especialmente en el África subsahariana. En 2010, se ... [truncated 225 chars](2420 chars) |
| Aumento rápido y mayor expresión basal de genes inducidos por interferón reducen la supervivencia de neuronas de células granulares infectadas por el virus del Nilo Occidental. (176 chars) | Aunque la susceptibilidad de las neuronas del cerebro a la infección microbiana es un determinante mayor del resultado clínico, se sabe poco sobre los factores moleculares que gobiernan esta vulnerabilidad. Aquí mostramos que ... [truncated 225 chars](1284 chars) |
| El cribado primario de cáncer cervical con detección de VPH tiene mayor sensibilidad longitudinal que la citología convencional para detectar neoplasia intraepitelial cervical grado 2. (184 chars) | ANTECEDENTES La detección de cáncer cervical basada en la prueba del virus del papiloma humano (VPH) aumenta la sensibilidad para detectar neoplasia intraepitelial cervical de alto grado (grado 2 o 3), pero no se sabe si este ... [truncated 225 chars](2540 chars) |
| Bloquear la interacción entre TDP-43 y las proteínas del complejo respiratorio I ND3 y ND6 resulta en un aumento de la pérdida neuronal inducida por TDP-43. (156 chars) | Las mutaciones genéticas en la proteína TAR DNA-binding protein 43 (TARDBP, también conocida como TDP-43) causan esclerosis lateral amiotrófica (ELA), y un aumento en la presencia de TDP-43 (codificada por TARDBP) en el citop ... [truncated 225 chars](1483 chars) |

## Dataset Information

| Field | Value |
| --- | --- |
| Nano set | MNanoBEIR |
| Backing dataset | NanoBEIR-es |
| Task / split | NanoSciFact |
| Hugging Face dataset | [hakari-bench/NanoBEIR-es](https://huggingface.co/datasets/hakari-bench/NanoBEIR-es) |
| Language | es |
| Category | natural_language |
| Queries | 50 |
| Documents | 2,919 |
| Positive qrels | 56 |
| Avg positives / query | 1.12 |
| Positives per query (min / median / max) | 1 / 1.00 / 4 |
| Queries with multiple positives | 4 (8.0%) |
| BM25 nDCG@10 | 0.7176 |
| BM25 hit@10 | 0.8600 |
| BM25 Recall@100 | 0.9286 |
| BM25 candidate subset | top-500 (`bm25`) |
| Dense nDCG@10 | 0.6480 |
| Dense hit@10 | 0.7600 |
| Dense Recall@100 | 0.8929 |
| Dense candidate subset | top-500 (`harrier_oss_v1_270m`) |
| Reranking hybrid nDCG@10 | 0.7280 |
| Reranking hybrid hit@10 | 0.8600 |
| Reranking hybrid Recall@100 | 0.9286 |
| Reranking hybrid candidate subset | top-100 plus optional rank-101 safeguard (`reranking_hybrid`) |
| Reranking hybrid candidates / query | 100-101 |
| Reranking hybrid safeguard rows | 4 |
| Query length avg chars | 113.56 |
| Document length avg chars | 1,644.20 |

### Public Sources

- [Fact or Fiction: Verifying Scientific Claims](https://arxiv.org/abs/2004.14974); 2020; David Wadden, Shanchuan Lin, Kyle Lo, Lucy Lu Wang, Madeleine van Zuylen, Arman Cohan, Hannaneh Hajishirzi; DOI: `10.18653/v1/2020.emnlp-main.609`.
- [SciFact repository](https://github.com/allenai/scifact).
- [BEIR: A Heterogeneous Benchmark for Zero-shot Evaluation of Information Retrieval Models](https://arxiv.org/abs/2104.08663); 2021; Nandan Thakur, Nils Reimers, Andreas Rueckle, Abhishek Srivastava, Iryna Gurevych; DOI: `10.48550/arXiv.2104.08663`.
- [MMTEB: Massive Multilingual Text Embedding Benchmark](https://arxiv.org/abs/2502.13595); 2025; Kenneth Enevoldsen, Isaac Chung, Imene Kerboua, Marton Kardos, Ashwin Mathur, and others; DOI: `10.48550/arXiv.2502.13595`.
- [Zeta Alpha NanoBEIR collection](https://huggingface.co/collections/zeta-alpha-ai/nanobeir).

### Hugging Face Links

- Nano dataset: [hakari-bench/NanoBEIR-es](https://huggingface.co/datasets/hakari-bench/NanoBEIR-es)
- Source collection: [Zeta Alpha NanoBEIR collection](https://huggingface.co/collections/zeta-alpha-ai/nanobeir)

### Source Reference Table

| Title | Year | Type | URL |
| --- | ---: | --- | --- |
| Fact or Fiction: Verifying Scientific Claims | 2020 | task paper | https://arxiv.org/abs/2004.14974 |
| SciFact repository |  | project page | https://github.com/allenai/scifact |
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
  task_name: NanoSciFact
  split_name: NanoSciFact
  language: es
  category: natural_language
  document_path: docs/benchmark_tasks/MNanoBEIR/NanoBEIR-es__NanoSciFact.md
  source_research:
    primary_source_type: task_paper
    paper_pdf_or_html_checked: true
    no_paper_note: null
  counts:
    queries: 50
    documents: 2919
    positive_qrels: 56
  positives_per_query:
    average: 1.12
    min: 1
    median: 1.0
    max: 4
    multi_positive_queries: 4
    multi_positive_query_percent: 8.0
  text_stats_chars:
    query_mean: 113.56
    document_mean: 1644.202809
  bm25:
    ndcg_at_10: 0.7175670537043329
    hit_at_10: 0.86
    source: dataset_candidate_subset
  learning:
    original_train_split: available
    evaluation_split_origin: MNanoBEIR Spanish NanoBEIR task split from hakari-bench/NanoBEIR-es
    train_eval_overlap_audit: not_audited
    leakage_note: prefer excluding SciFact, BEIR, or NanoBEIR records likely to overlap
      with these evaluation claims or abstracts
    useful_training_data:
    - non-overlapping SciFact-style claim-evidence pairs
    - scientific fact verification data
    - biomedical abstract retrieval pairs
    - Spanish or multilingual scientific NLI and evidence selection data
    synthetic_data:
      document_generation: Spanish scientific abstracts with explicit findings outside
        the evaluation set
      question_generation: atomic Spanish scientific claims supported or refuted by
        the abstract
      answerability: positives should provide evidence for or against the claim, not
        only share scientific terminology
    multi_positive_training: useful_but_not_central
  links:
    nano_dataset: https://huggingface.co/datasets/hakari-bench/NanoBEIR-es
    source_urls:
    - label: SciFact paper
      url: https://arxiv.org/abs/2004.14974
    - label: SciFact repository
      url: https://github.com/allenai/scifact
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
  - title: 'Fact or Fiction: Verifying Scientific Claims'
    url: https://arxiv.org/abs/2004.14974
    year: 2020
    doi: 10.18653/v1/2020.emnlp-main.609
    is_paper: true
    source_confidence: definitive_paper_link
  - title: SciFact repository
    url: https://github.com/allenai/scifact
    year: null
    doi: null
    is_paper: false
    source_confidence: definitive_project_page
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
      ndcg_at_10: 0.7175670537
      hit_at_10: 0.86
      recall_at_100: 0.9285714286
      candidate_count_min: 500
      candidate_count_max: 500
      candidate_count_mean: 500.0
      query_count: 50
      query_coverage: 1.0
      relevant_coverage_at_100: 0.9285714286
    dense:
      config: harrier_oss_v1_270m
      label: Dense
      source: dataset_candidate_subset
      top_k: 500
      ndcg_at_10: 0.647993755
      hit_at_10: 0.76
      recall_at_100: 0.8928571429
      candidate_count_min: 500
      candidate_count_max: 500
      candidate_count_mean: 500.0
      query_count: 50
      query_coverage: 1.0
      relevant_coverage_at_100: 0.8928571429
    reranking_hybrid:
      config: reranking_hybrid
      label: Reranking hybrid
      source: dataset_candidate_subset
      top_k: 100
      ndcg_at_10: 0.7279811245
      hit_at_10: 0.86
      recall_at_100: 0.9285714286
      candidate_count_min: 100
      candidate_count_max: 101
      candidate_count_mean: 100.08
      query_count: 50
      query_coverage: 1.0
      relevant_coverage_at_100: 0.9285714286
      safeguard_positive_rows: 4
      rows_with_101_candidates: 4
```
