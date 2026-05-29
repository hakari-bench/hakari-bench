# NanoMLDR / fr

## Overview

`fr` is the French split of NanoMLDR. It evaluates long-document retrieval for
French questions generated from paragraphs in long French articles.

## Details

### What the Original Data Measures

[M3-Embedding](https://arxiv.org/abs/2402.03216) presents MLDR as a
multilingual long-document retrieval benchmark and evaluates it with NDCG@10.
The paper notes that long-document retrieval stresses input granularity and that
BM25 remains a strong baseline in this setting. The [MLDR dataset card](https://huggingface.co/datasets/Shitao/MLDR)
lists French as Wikipedia-sourced and describes the construction as
paragraph-based GPT-3.5 question generation over long articles.

### Observed Data Profile

The Nano split has 152 queries, 3,059 documents, and 152 positive qrels. Each
query has one positive. Queries average 119.92 characters and documents average
11,534.15 characters. The examples are French questions over articles about
charitable orders, comics, theater, Formula 1, and Jewish community history.

### BM25 Difficulty

Using the dataset-provided BM25 candidate column, BM25 reaches nDCG@10 =
0.8774 and hit@10 = 0.9211. It ranks 126 positives first. The generated French
questions often retain distinctive article vocabulary, so lexical retrieval is
strong, though an example at rank 13 shows that unrelated-looking titles can
still hide the relevant paragraph.

### Training Data That May Help

Useful training data includes French Wikipedia question-article pairs,
long-document QA retrieval, multilingual MLDR training data, and hard negatives
from articles with overlapping entities or cultural references.

### Synthetic Data Guidance

Synthetic data should generate French paragraph-grounded questions from full
articles. Negatives should be full articles in the same topical area but missing
the answer paragraph.

## Example Data

| Query | Positive document |
| --- | --- |
| Quels sont les résultats des huitièmes de finale de la Coupe de France et de la Coupe UEFA ? (92 chars) | Cette page concerne l'actualité sportive du mois de . Mardi mars Football : surprises à l'occasion des huitièmes de finale de la Coupe de France. Clermont Foot, modeste seizième en Ligue 2, sort l'Olympique lyonnais, leader d ... [truncated 225 chars](24419 chars) |
| Quel est le lien entre les personnages Xavier et Magnéto et les figures historiques de Martin Luther King et Malcolm X dans le projet proposé par Bryan Singer et Tom DeSanto à la Fox en 1998? (191 chars) | X-Men est un film américain réalisé par Bryan Singer, sorti en 2000. C'est le premier film de la série X-Men mettant en scène les personnages de la série de comics X-Men de Marvel Comics, créés par le scénariste Stan Lee et l ... [truncated 225 chars](22611 chars) |
| Quel est le temps de traversée entre Ouistreham et Portsmouth en utilisant la ligne de ferry de Brittany Ferries ? (114 chars) | Le port de Caen-Ouistreham est un port de commerce, un port passager et un port de plaisance français s'étendant sur le canal de Caen à la mer depuis l'embouchure de l'Orne à Ouistreham jusqu'à la ville de Caen, dans le dépar ... [truncated 225 chars](22300 chars) |
| Quel événement a conduit à la perte de la place de Bernard en équipe de France en été 199x ? (92 chars) | Bernard Lama, né le à Saint-Symphorien (Indre-et-Loire), est un footballeur international français évoluant au poste de gardien de but dans les années 1980-1990. Lama grandit et débute le football en Guyane, où naissent ses p ... [truncated 225 chars](24800 chars) |
| Quelles modifications ont été apportées à la monoplace de Lola pour améliorer ses performances en Formule 1 ? (109 chars) | La Lola T97/30 est une monoplace de Formule 1, conçue par Eric Broadley, fondateur de l'officine de construction de voitures de courses Lola Cars et engagée en championnat du monde de Formule 1 en 1997. Elle est pilotée par l ... [truncated 225 chars](24630 chars) |

## Dataset Information

| Field | Value |
| --- | --- |
| Nano set | NanoMLDR |
| Backing dataset | NanoMLDR |
| Task / split | fr |
| Hugging Face dataset | [hakari-bench/NanoMLDR](https://huggingface.co/datasets/hakari-bench/NanoMLDR) |
| Language | fr |
| Category | natural_language |
| Queries | 152 |
| Documents | 3059 |
| Positive qrels | 152 |
| BM25 nDCG@10 | 0.9125 |
| BM25 hit@10 | 0.9408 |
| BM25 Recall@100 | 0.9868 |
| BM25 candidate subset | top-500 (`bm25`) |
| Dense nDCG@10 | 0.7706 |
| Dense hit@10 | 0.8421 |
| Dense Recall@100 | 0.9211 |
| Dense candidate subset | top-500 (`harrier_oss_v1_270m`) |
| Reranking hybrid nDCG@10 | 0.8421 |
| Reranking hybrid hit@10 | 0.9145 |
| Reranking hybrid Recall@100 | 0.9868 |
| Reranking hybrid candidate subset | top-100 plus optional rank-101 safeguard (`reranking_hybrid`) |
| Reranking hybrid candidates / query | 100-101 |
| Reranking hybrid safeguard rows | 2 |
| Query length avg chars | 119.92 |
| Document length avg chars | 11534.15 |

### Public Sources

- [M3-Embedding](https://arxiv.org/abs/2402.03216); 2024; Jianlv Chen et al.
- [MLDR dataset card](https://huggingface.co/datasets/Shitao/MLDR).

### Hugging Face Links

- Nano dataset: [hakari-bench/NanoMLDR](https://huggingface.co/datasets/hakari-bench/NanoMLDR)
- Source dataset: [Shitao/MLDR](https://huggingface.co/datasets/Shitao/MLDR)

### Source Reference Table

| Title | Year | Type | URL |
| --- | ---: | --- | --- |
| M3-Embedding: Multi-Linguality, Multi-Functionality, Multi-Granularity Text Embeddings Through Self-Knowledge Distillation | 2024 | benchmark paper | https://arxiv.org/abs/2402.03216 |
| MLDR: Multilingual Long-Document Retrieval dataset | 2024 | dataset card | https://huggingface.co/datasets/Shitao/MLDR |

## Machine-Readable Metadata

<!-- benchmark-task-metadata:v1 -->

```yaml
benchmark_task_metadata:
  schema_version: 1
  document_status: first_pass
  nano_set: NanoMLDR
  backing_dataset: NanoMLDR
  dataset_id: hakari-bench/NanoMLDR
  task_name: fr
  split_name: fr
  language: fr
  category: natural_language
  document_path: docs/benchmark_tasks/NanoMLDR/fr.md
  source_research:
    primary_source_type: benchmark_paper_and_dataset_card
    paper_pdf_or_html_checked: true
    no_paper_note: null
  counts:
    queries: 152
    documents: 3059
    positive_qrels: 152
  positives_per_query:
    average: 1.0
    min: 1
    median: 1.0
    max: 1
    multi_positive_queries: 0
    multi_positive_query_percent: 0.0
  text_stats_chars:
    query_mean: 119.92105263157895
    document_mean: 11534.147433801896
  bm25:
    ndcg_at_10: 0.912452039749984
    hit_at_10: 0.9407894736842105
    source: dataset_candidate_subset
  learning:
    original_train_split: available
    evaluation_split_origin: MLDR French split
    train_eval_overlap_audit: not_audited
    leakage_note: exclude NanoMLDR fr queries, qrels, and positive documents
    useful_training_data:
    - French long-document QA retrieval pairs
    - French Wikipedia article retrieval
    - multilingual MLDR training data outside this Nano split
    - same-entity French article hard negatives
    synthetic_data:
      document_generation: long French encyclopedic articles
      question_generation: paragraph-grounded French questions
      answerability: positives should be full articles containing the answer-bearing
        paragraph
    multi_positive_training: single_positive
  links:
    nano_dataset: https://huggingface.co/datasets/hakari-bench/NanoMLDR
    source_urls:
    - label: M3-Embedding arXiv
      url: https://arxiv.org/abs/2402.03216
    - label: Shitao/MLDR
      url: https://huggingface.co/datasets/Shitao/MLDR
    source_notes: []
  references:
  - title: 'M3-Embedding: Multi-Linguality, Multi-Functionality, Multi-Granularity
      Text Embeddings Through Self-Knowledge Distillation'
    url: https://arxiv.org/abs/2402.03216
    year: 2024
    is_paper: true
    source_confidence: definitive_paper_link
  candidate_subsets:
    bm25:
      config: bm25
      label: BM25
      source: dataset_candidate_subset
      top_k: 500
      ndcg_at_10: 0.9124520397
      hit_at_10: 0.9407894737
      recall_at_100: 0.9868421053
      candidate_count_min: 500
      candidate_count_max: 500
      candidate_count_mean: 500.0
      query_count: 152
      query_coverage: 1.0
      relevant_coverage_at_100: 0.9868421053
    dense:
      config: harrier_oss_v1_270m
      label: Dense
      source: dataset_candidate_subset
      top_k: 500
      ndcg_at_10: 0.7706096152
      hit_at_10: 0.8421052632
      recall_at_100: 0.9210526316
      candidate_count_min: 500
      candidate_count_max: 500
      candidate_count_mean: 500.0
      query_count: 152
      query_coverage: 1.0
      relevant_coverage_at_100: 0.9210526316
    reranking_hybrid:
      config: reranking_hybrid
      label: Reranking hybrid
      source: dataset_candidate_subset
      top_k: 100
      ndcg_at_10: 0.8420871873
      hit_at_10: 0.9144736842
      recall_at_100: 0.9868421053
      candidate_count_min: 100
      candidate_count_max: 101
      candidate_count_mean: 100.013158
      query_count: 152
      query_coverage: 1.0
      relevant_coverage_at_100: 0.9868421053
      safeguard_positive_rows: 2
      rows_with_101_candidates: 2
```
