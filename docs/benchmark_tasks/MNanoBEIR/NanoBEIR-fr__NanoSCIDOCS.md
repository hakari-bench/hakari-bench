# MNanoBEIR / NanoBEIR-fr / NanoSCIDOCS

## Overview

SCIDOCS is a scientific document retrieval benchmark derived from scholarly
relatedness signals. `NanoBEIR-fr__NanoSCIDOCS` is the French MNanoBEIR version:
French translated scientific paper titles or abstracts are used as queries, and
the system must retrieve French translated related scientific documents. The
task tests document-level scholarly relatedness.

## Details

### What the Original Data Measures

[SPECTER: Document-level Representation Learning using Citation-informed
Transformers](https://arxiv.org/abs/2004.07180) introduces SCIDOCS as an
evaluation benchmark for scientific document embeddings. The paper uses
citations and related scholarly signals to test whether representations capture
document-level relatedness.

[BEIR: A Heterogeneous Benchmark for Zero-shot Evaluation of Information
Retrieval Models](https://arxiv.org/abs/2104.08663) includes SCIDOCS as a
citation-prediction style retrieval task. [MMTEB: Massive Multilingual Text
Embedding Benchmark](https://arxiv.org/abs/2502.13595) provides the
multilingual context for this French split.

### Observed Data Profile

The sampled French Nano task has 50 queries, 2,210 documents, and 244 positive
qrel rows. Every query is multi-positive, with 3 to 5 positives and an average
of 4.88 positives. The average query length is 93.28 characters, and the
average document length is 1,115.29 characters.

The inspected queries cover neural machine translation, automotive information
security, Bitcoin transaction privacy, IoT security, and gait-analysis motion
capture. Documents are French translated scientific abstracts or paper
descriptions.

### BM25 Difficulty

Using the dataset-provided BM25 candidate column, BM25 reaches nDCG@10 =
0.3219 and hit@10 = 0.7800. BM25 ranks a positive first for 23 queries, and
the median first-positive rank is 2.

BM25 benefits from technical vocabulary overlap, but related scientific papers
may share methods, citations, or application areas without using the same title
terms. Strong models should represent scholarly relatedness, not just title
keyword overlap.

### Training Data That May Help

Useful training data includes non-overlapping citation prediction pairs,
scientific paper recommendation data, co-citation or co-viewed paper pairs, and
French or multilingual scholarly retrieval supervision. Training should exclude
SCIDOCS, SPECTER evaluation data, BEIR, NanoBEIR, or translated scientific
records likely to overlap with these documents.

### Synthetic Data Guidance

For document-to-query generation, start from non-evaluation scientific
abstracts and generate French paper-title-like queries or short summaries. For
joint generation, create clusters of related abstracts linked by methods,
citations, or problem formulations.

## Example Data

| Query | Positive document |
| --- | --- |
| Nouveau convertisseur élévateur multiniveau CC-CC (49 chars) | Les convertisseurs de tension à sources multiples sont en train d'émerger comme une nouvelle génération d'options de convertisseurs de puissance pour les applications à haute puissance. Les convertisseurs de tension à sources ... [truncated 225 chars](1262 chars) |
| Apprentissage accéléré des champs aléatoires de Markov gaussiens creux basé sur la décomposition de Cholesky (108 chars) | Sure, please provide the English document text that you need translated into French. (84 chars) |
| Synthèse de textures par réseaux de neurones convolutifs (56 chars) | Dans ce travail, nous examinons l'impact de la profondeur des réseaux convolutifs sur leur précision dans le contexte de la reconnaissance d'images à grande échelle. Notre principale contribution est une évaluation approfondi ... [truncated 225 chars](1020 chars) |
| Antenne annulaire plane à large bande avec polarisation circulaire pour un système RFID (87 chars) | Dans cet article, une technique d'alimentation à bande horizontale sinueuse (HMS) est proposée pour obtenir une bonne adaptation d'impédance et des diagrammes de rayonnement symétriques en champ lointain pour une antenne à pa ... [truncated 225 chars](1507 chars) |
| Conception d'un moniteur cardiaque numérique avancé en utilisant des composants électroniques de base (101 chars) | Dans cet article, nous présentons la conception et le développement d'un nouveau dispositif intégré pour mesurer la fréquence cardiaque à l'aide du bout des doigts, afin d'améliorer l'estimation de la fréquence cardiaque. Alo ... [truncated 225 chars](1375 chars) |

## Dataset Information

| Field | Value |
| --- | --- |
| Nano set | MNanoBEIR |
| Backing dataset | NanoBEIR-fr |
| Task / split | NanoSCIDOCS |
| Hugging Face dataset | [hakari-bench/NanoBEIR-fr](https://huggingface.co/datasets/hakari-bench/NanoBEIR-fr) |
| Language | fr |
| Category | natural_language |
| Queries | 50 |
| Documents | 2,210 |
| Positive qrels | 244 |
| Avg positives / query | 4.88 |
| Positives per query (min / median / max) | 3 / 5.00 / 5 |
| Queries with multiple positives | 50 (100.0%) |
| BM25 nDCG@10 | 0.3129 |
| BM25 hit@10 | 0.7600 |
| BM25 Recall@100 | 0.6066 |
| BM25 candidate subset | top-500 (`bm25`) |
| Dense nDCG@10 | 0.3734 |
| Dense hit@10 | 0.8200 |
| Dense Recall@100 | 0.6148 |
| Dense candidate subset | top-500 (`harrier_oss_v1_270m`) |
| Reranking hybrid nDCG@10 | 0.3787 |
| Reranking hybrid hit@10 | 0.8400 |
| Reranking hybrid Recall@100 | 0.6639 |
| Reranking hybrid candidate subset | top-100 plus optional rank-101 safeguard (`reranking_hybrid`) |
| Reranking hybrid candidates / query | 100-101 |
| Reranking hybrid safeguard rows | 1 |
| Query length avg chars | 93.28 |
| Document length avg chars | 1,115.29 |

### Public Sources

- [SPECTER: Document-level Representation Learning using Citation-informed Transformers](https://arxiv.org/abs/2004.07180).
- [SCIDOCS repository](https://github.com/allenai/scidocs).
- [BEIR: A Heterogeneous Benchmark for Zero-shot Evaluation of Information Retrieval Models](https://arxiv.org/abs/2104.08663).
- [MMTEB: Massive Multilingual Text Embedding Benchmark](https://arxiv.org/abs/2502.13595).
- [Zeta Alpha NanoBEIR collection](https://huggingface.co/collections/zeta-alpha-ai/nanobeir).

### Hugging Face Links

- Nano dataset: [hakari-bench/NanoBEIR-fr](https://huggingface.co/datasets/hakari-bench/NanoBEIR-fr)
- Source collection: [Zeta Alpha NanoBEIR collection](https://huggingface.co/collections/zeta-alpha-ai/nanobeir)

### Source Reference Table

| Title | Year | Type | URL |
| --- | ---: | --- | --- |
| SPECTER: Document-level Representation Learning using Citation-informed Transformers | 2020 | task paper | https://arxiv.org/abs/2004.07180 |
| SCIDOCS repository |  | project page | https://github.com/allenai/scidocs |
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
  task_name: NanoSCIDOCS
  split_name: NanoSCIDOCS
  language: fr
  category: natural_language
  document_path: docs/benchmark_tasks/MNanoBEIR/NanoBEIR-fr__NanoSCIDOCS.md
  source_research:
    primary_source_type: task_paper
    paper_pdf_or_html_checked: true
    no_paper_note: null
  counts:
    queries: 50
    documents: 2210
    positive_qrels: 244
  positives_per_query:
    average: 4.88
    min: 3
    median: 5.0
    max: 5
    multi_positive_queries: 50
    multi_positive_query_percent: 100.0
  text_stats_chars:
    query_mean: 93.28
    document_mean: 1115.291403
  bm25:
    ndcg_at_10: 0.3129003181506328
    hit_at_10: 0.76
    source: dataset_candidate_subset
  candidate_subsets:
    bm25:
      config: bm25
      label: BM25
      source: dataset_candidate_subset
      top_k: 500
      ndcg_at_10: 0.3129003182
      hit_at_10: 0.76
      recall_at_100: 0.606557377
      candidate_count_min: 500
      candidate_count_max: 500
      candidate_count_mean: 500.0
      query_count: 50
      query_coverage: 1.0
      relevant_coverage_at_100: 0.606557377
    dense:
      config: harrier_oss_v1_270m
      label: Dense
      source: dataset_candidate_subset
      top_k: 500
      ndcg_at_10: 0.3734492517
      hit_at_10: 0.82
      recall_at_100: 0.6147540984
      candidate_count_min: 500
      candidate_count_max: 500
      candidate_count_mean: 500.0
      query_count: 50
      query_coverage: 1.0
      relevant_coverage_at_100: 0.6147540984
    reranking_hybrid:
      config: reranking_hybrid
      label: Reranking hybrid
      source: dataset_candidate_subset
      top_k: 100
      ndcg_at_10: 0.3786741338
      hit_at_10: 0.84
      recall_at_100: 0.6639344262
      candidate_count_min: 100
      candidate_count_max: 101
      candidate_count_mean: 100.02
      query_count: 50
      query_coverage: 1.0
      relevant_coverage_at_100: 0.6639344262
      safeguard_positive_rows: 1
      rows_with_101_candidates: 1
```
