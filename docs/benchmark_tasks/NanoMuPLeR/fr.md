# NanoMuPLeR / fr

## Overview

`NanoMuPLeR / fr` is the French split of MuPLeR-retrieval. It pairs synthetic
French legal questions with French EU-law passages derived from DGT-Acquis. The
retrieval problem is to rank the one passage that explicitly grounds the legal
answer ahead of other similar EU legal passages.

## Details

### What the Original Data Measures

The [MuPLeR-retrieval dataset card](https://huggingface.co/datasets/mteb/MuPLeR-retrieval)
describes 10,000 human-translated DGT-Acquis passages and 200 synthetic
parallel queries across 14 languages. [An overview of the European Union's highly multilingual parallel corpora](https://link.springer.com/article/10.1007/s10579-014-9277-0)
is the source reference for the EU parallel corpora behind the task.

### Observed Data Profile

The French split contains 200 queries, 10,000 documents, and 200 positives.
Queries average 141.22 characters and documents average 746.43 characters.
Sampled items ask about capital duty, state-aid compensation, procurement award
criteria, nuclear-policy priorities, and pre-accession production rules.

### BM25 Difficulty

BM25 reaches nDCG@10 = 0.7773 and hit@10 = 0.8850, with 132 positives at rank 1
and 177 in the top 10. French legal phrasing often preserves exact institutional
terms and numeric conditions, so lexical retrieval is strong, but the task still
tests whether the model captures the full legal condition.

### Training Data That May Help

Useful data includes non-overlapping French EU legal search pairs, French
EUR-Lex passages, multilingual legal bitext, and hard negatives from related
regulations or opinions. Evaluation query-passage pairs should be excluded.

### Synthetic Data Guidance

Generate French questions from non-evaluation EU legal passages. Preserve dates,
percentages, legal terms, and named institutions, and pair them with near
negatives from adjacent legal topics that do not answer the same condition.

## Example Data

| Query | Positive document |
| --- | --- |
| Quelles deux constatations de l'enquête réglementaire ont miné l'affirmation des opérateurs selon laquelle ils pouvaient internaliser le rapprochement des transactions ? (169 chars) | Pour les parties notifiantes, il existe une solution sérieuse pour les ORM, celle de l'auto-approvisionnement puisque les ORM possèdent à l'intérieur de leur entreprise les capacités et le savoir-faire nécessaires pour passer ... [truncated 225 chars](726 chars) |
| Quelle chambre régionale est nommée avec les institutions de l'Union pour promouvoir la parité comme norme éthique de gouvernance politique ? (141 chars) | Pour être efficace et significative, la démocratie doit garantir la possibilité de pleine participation des citoyens aux décisions finales contraignantes qui concernent leur vie quotidienne. Tant que le principe d'inégalité e ... [truncated 225 chars](664 chars) |
| Quelles deux clauses la Commission, dans l'évaluation préliminaire, a‑t‑elle jugées potentiellement incompatibles avec les règles de concurrence CE et EEE ? (156 chars) | Il ressort de l'évaluation préliminaire de la Commission que deux des clauses de la convention soulèvent des doutes sérieux quant à leur compatibilité avec l'article 81 du traité CE et l'article 53 de l'accord EEE. La premièr ... [truncated 225 chars](656 chars) |
| Quel pays a omis d'appliquer les règles de reconnaissance de l'UE aux professions sanitaires réglementées et apparentées ? (122 chars) | juger, qu'en n'omettant de prendre les mesures législatives et réglementaires nécessaires, ou de les communiquer à la Commission, la République fédérale d'Allemagne a méconnu ses obligations de transposer de manière complète ... [truncated 225 chars](795 chars) |
| Quelle pièce de charcuterie dont l'étymologie remonte à des termes désignant des chasseurs est une ration portable à longue conservation ? (138 chars) | Le nom kiełbasa myśliwska reflète les caractéristiques spécifiques du produit. Les caractéristiques spécifiques exprimées par ce nom transparaissent dans l’origine étymologique de ce dernier, qui vient de myśliwy (chasseur), ... [truncated 225 chars](730 chars) |

## Dataset Information

| Field | Value |
| --- | --- |
| Nano set | NanoMuPLeR |
| Backing dataset | NanoMuPLeR |
| Task / split | fr |
| Hugging Face dataset | [hakari-bench/NanoMuPLeR](https://huggingface.co/datasets/hakari-bench/NanoMuPLeR) |
| Source dataset | [mteb/MuPLeR-retrieval](https://huggingface.co/datasets/mteb/MuPLeR-retrieval) |
| Language | fr |
| Category | natural_language |
| Queries | 200 |
| Documents | 10,000 |
| Positive qrels | 200 |
| BM25 nDCG@10 | 0.8179 |
| BM25 hit@10 | 0.9150 |
| BM25 Recall@100 | 0.9800 |
| BM25 candidate subset | top-500 (`bm25`) |
| Dense nDCG@10 | 0.8329 |
| Dense hit@10 | 0.9150 |
| Dense Recall@100 | 0.9550 |
| Dense candidate subset | top-500 (`harrier_oss_v1_270m`) |
| Reranking hybrid nDCG@10 | 0.8628 |
| Reranking hybrid hit@10 | 0.9350 |
| Reranking hybrid Recall@100 | 0.9950 |
| Reranking hybrid candidate subset | top-100 plus optional rank-101 safeguard (`reranking_hybrid`) |
| Reranking hybrid candidates / query | 100-101 |
| Reranking hybrid safeguard rows | 1 |
| Query length avg chars | 141.22 |
| Document length avg chars | 746.43 |

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
  task_name: fr
  split_name: fr
  language: fr
  category: natural_language
  document_path: docs/benchmark_tasks/NanoMuPLeR/fr.md
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
    query_mean: 141.22
    document_mean: 746.43
  bm25:
    ndcg_at_10: 0.8179292343262202
    hit_at_10: 0.915
    source: dataset_candidate_subset
  example_count: 5
  candidate_subsets:
    bm25:
      config: bm25
      label: BM25
      source: dataset_candidate_subset
      top_k: 500
      ndcg_at_10: 0.8179292343
      hit_at_10: 0.915
      recall_at_100: 0.98
      candidate_count_min: 500
      candidate_count_max: 500
      candidate_count_mean: 500.0
      query_count: 200
      query_coverage: 1.0
      relevant_coverage_at_100: 0.98
    dense:
      config: harrier_oss_v1_270m
      label: Dense
      source: dataset_candidate_subset
      top_k: 500
      ndcg_at_10: 0.8328664806
      hit_at_10: 0.915
      recall_at_100: 0.955
      candidate_count_min: 500
      candidate_count_max: 500
      candidate_count_mean: 500.0
      query_count: 200
      query_coverage: 1.0
      relevant_coverage_at_100: 0.955
    reranking_hybrid:
      config: reranking_hybrid
      label: Reranking hybrid
      source: dataset_candidate_subset
      top_k: 100
      ndcg_at_10: 0.8628377007
      hit_at_10: 0.935
      recall_at_100: 0.995
      candidate_count_min: 100
      candidate_count_max: 101
      candidate_count_mean: 100.005
      query_count: 200
      query_coverage: 1.0
      relevant_coverage_at_100: 0.995
      safeguard_positive_rows: 1
      rows_with_101_candidates: 1
```
