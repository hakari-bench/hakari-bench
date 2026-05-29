# NanoMuPLeR / es

## Overview

`NanoMuPLeR / es` is the Spanish split of MuPLeR-retrieval. It evaluates
Spanish legal query-to-passage retrieval over EU legislative text derived from
DGT-Acquis. Queries are synthetic legal questions and documents are Spanish
parallel passages; the relevant item is the single passage that grounds the
question.

## Details

### What the Original Data Measures

The [MuPLeR-retrieval dataset card](https://huggingface.co/datasets/mteb/MuPLeR-retrieval)
describes a 14-language legal retrieval benchmark built from human-translated
DGT-Acquis passages and synthetic parallel queries. [An overview of the European Union's highly multilingual parallel corpora](https://link.springer.com/article/10.1007/s10579-014-9277-0)
is the cited source reference for the EU parallel-corpus family.

### Observed Data Profile

The Spanish split has 200 queries, 10,000 documents, and 200 single-positive
qrels. Queries average 134.67 characters and documents average 734.58
characters. The sampled questions are formal EU-law information needs involving
tax rates, compensation parameters, procurement separation, nuclear policy
priorities, and pre-accession production clauses.

### BM25 Difficulty

BM25 reaches nDCG@10 = 0.7792 and hit@10 = 0.8600, ranking 140 positives first
and 172 in the top 10. Legal terminology, dates, and numeric rates create strong
lexical anchors, but exact retrieval still requires matching the full legal
condition rather than isolated keywords.

### Training Data That May Help

Useful data includes non-overlapping Spanish EUR-Lex/DGT-Acquis retrieval pairs,
Spanish legal QA, multilingual legal bitext, and hard negatives from related EU
provisions. Exclude MuPLeR evaluation queries and exact positives from training.

### Synthetic Data Guidance

Generate Spanish questions from EU legal passages while preserving legal roles,
percentages, dates, and article-like conditions. Hard negatives should share the
topic or institution but answer a different legal issue.

## Example Data

| Query | Positive document |
| --- | --- |
| ¿Por qué la autoridad estadística propone instrumento jurídico para consolidar datos de salud poblacional y seguridad laboral y apoyar metodologías? (148 chars) | Ésta es la razón por la que la Comisión (Eurostat) considera que es hora de establecer una base sólida mediante un acto jurídico fundamental sobre estadísticas de salud pública y salud y seguridad en el trabajo. Los ámbitos r ... [truncated 225 chars](722 chars) |
| Cómo quiso el ejecutivo supranacional que corrieran las ayudas: dos años y hasta tres más al convertir el contrato? (115 chars) | Dado que el régimen de ayudas (identificado con el no NN 91/A/95) adoptado por la Región de Sicilia mediante el artículo 10 de la Ley regional no 27, de 15 de mayo de 1991, preveía un mecanismo de aportaciones para un número ... [truncated 225 chars](650 chars) |
| Cómo relaciona la prevención la explotación insostenible y las intervenciones humanas intencionadas con catástrofes naturales anómalas y de gran magnitud? (154 chars) | La prevención es un principio fundamental para la protección y conservación del medio ambiente así como los daños que pudieran causarse a la población civil, y su finalidad es una utilización sostenible de los recursos natura ... [truncated 225 chars](708 chars) |
| ¿Qué impuesto sobre las importaciones intracomunitarias seguían aplicando siete Estados miembros: dos ≤0,5%, uno 0,6%, cuatro al 1%? (132 chars) | La mayoría de los 25 Estados miembros aceptó la orientación del Consejo de 1985 y ha suprimido totalmente el impuesto. En la actualidad, sólo siete Estados miembros continúan aplicándolo: Polonia y Portugal con un tipo imposi ... [truncated 225 chars](687 chars) |
| Qué órgano asesor cuestionó la guía para operadores de pools irregulares y propuso ampliar normas de consorcios solo para contenedores? (135 chars) | Dado que las secciones que tratan sobre el transporte de tramp y los pools de transporte de tramp son menos detalladas por las razones supuestas anteriormente, el CESE se pregunta si serán suficientes para proporcionar a los ... [truncated 225 chars](783 chars) |

## Dataset Information

| Field | Value |
| --- | --- |
| Nano set | NanoMuPLeR |
| Backing dataset | NanoMuPLeR |
| Task / split | es |
| Hugging Face dataset | [hakari-bench/NanoMuPLeR](https://huggingface.co/datasets/hakari-bench/NanoMuPLeR) |
| Source dataset | [mteb/MuPLeR-retrieval](https://huggingface.co/datasets/mteb/MuPLeR-retrieval) |
| Language | es |
| Category | natural_language |
| Queries | 200 |
| Documents | 10,000 |
| Positive qrels | 200 |
| BM25 nDCG@10 | 0.8302 |
| BM25 hit@10 | 0.9050 |
| BM25 Recall@100 | 0.9700 |
| BM25 candidate subset | top-500 (`bm25`) |
| Dense nDCG@10 | 0.8803 |
| Dense hit@10 | 0.9550 |
| Dense Recall@100 | 0.9850 |
| Dense candidate subset | top-500 (`harrier_oss_v1_270m`) |
| Reranking hybrid nDCG@10 | 0.8862 |
| Reranking hybrid hit@10 | 0.9500 |
| Reranking hybrid Recall@100 | 1.0000 |
| Reranking hybrid candidate subset | top-100 plus optional rank-101 safeguard (`reranking_hybrid`) |
| Reranking hybrid candidates / query | 100 |
| Reranking hybrid safeguard rows | 0 |
| Query length avg chars | 134.67 |
| Document length avg chars | 734.58 |

### Public Sources

- [mteb/MuPLeR-retrieval](https://huggingface.co/datasets/mteb/MuPLeR-retrieval), source dataset card.
- [An overview of the European Union's highly multilingual parallel corpora](https://link.springer.com/article/10.1007/s10579-014-9277-0), DGT-Acquis source reference paper.
- [DGT-Acquis](https://joint-research-centre.ec.europa.eu/language-technology-resources/dgt-acquis_en), European Commission source-corpus page.

### Hugging Face Links

- Nano dataset: [hakari-bench/NanoMuPLeR](https://huggingface.co/datasets/hakari-bench/NanoMuPLeR)
- Source task dataset: [mteb/MuPLeR-retrieval](https://huggingface.co/datasets/mteb/MuPLeR-retrieval)

### Source Reference Table

| Title | Year | Type | URL |
| --- | ---: | --- | --- |
| MuPLeR: Multilingual Parallel Legal Retrieval |  | dataset card | https://huggingface.co/datasets/mteb/MuPLeR-retrieval |
| An overview of the European Union's highly multilingual parallel corpora | 2014 | source paper | https://link.springer.com/article/10.1007/s10579-014-9277-0 |
| DGT-Acquis |  | source corpus | https://joint-research-centre.ec.europa.eu/language-technology-resources/dgt-acquis_en |

## Machine-Readable Metadata

<!-- benchmark-task-metadata:v1 -->

```yaml
benchmark_task_metadata:
  schema_version: 1
  document_status: first_pass
  nano_set: NanoMuPLeR
  backing_dataset: NanoMuPLeR
  dataset_id: hakari-bench/NanoMuPLeR
  task_name: es
  split_name: es
  language: es
  category: natural_language
  document_path: docs/benchmark_tasks/NanoMuPLeR/es.md
  source_research:
    primary_source_type: dataset_card
    paper_pdf_or_html_checked: true
    no_paper_note: no standalone MuPLeR technical paper was confirmed
  counts:
    queries: 200
    documents: 10000
    positive_qrels: 200
  positives_per_query:
    average: 1.0
    min: 1
    median: 1.0
    max: 1
    multi_positive_queries: 0
    multi_positive_query_percent: 0.0
  text_stats_chars:
    query_mean: 134.67
    document_mean: 734.58
  bm25:
    ndcg_at_10: 0.8301758887480121
    hit_at_10: 0.905
    source: dataset_candidate_subset
  example_count: 5
  candidate_subsets:
    bm25:
      config: bm25
      label: BM25
      source: dataset_candidate_subset
      top_k: 500
      ndcg_at_10: 0.8301758887
      hit_at_10: 0.905
      recall_at_100: 0.97
      candidate_count_min: 500
      candidate_count_max: 500
      candidate_count_mean: 500.0
      query_count: 200
      query_coverage: 1.0
      relevant_coverage_at_100: 0.97
    dense:
      config: harrier_oss_v1_270m
      label: Dense
      source: dataset_candidate_subset
      top_k: 500
      ndcg_at_10: 0.8803409381
      hit_at_10: 0.955
      recall_at_100: 0.985
      candidate_count_min: 500
      candidate_count_max: 500
      candidate_count_mean: 500.0
      query_count: 200
      query_coverage: 1.0
      relevant_coverage_at_100: 0.985
    reranking_hybrid:
      config: reranking_hybrid
      label: Reranking hybrid
      source: dataset_candidate_subset
      top_k: 100
      ndcg_at_10: 0.8862173253
      hit_at_10: 0.95
      recall_at_100: 1.0
      candidate_count_min: 100
      candidate_count_max: 100
      candidate_count_mean: 100.0
      query_count: 200
      query_coverage: 1.0
      relevant_coverage_at_100: 1.0
      safeguard_positive_rows: 0
      rows_with_101_candidates: 0
```
