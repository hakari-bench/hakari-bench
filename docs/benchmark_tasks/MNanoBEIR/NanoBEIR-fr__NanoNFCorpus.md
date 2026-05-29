# MNanoBEIR / NanoBEIR-fr / NanoNFCorpus

## Overview

NFCorpus is a medical information retrieval dataset built around health and
nutrition information needs linked to research articles. `NanoBEIR-fr__NanoNFCorpus`
is the French MNanoBEIR version: short French translated health queries must
retrieve French translated medical or biomedical documents. The task stresses
lay-to-technical matching and many relevant documents per query.

## Details

### What the Original Data Measures

[A Full-Text Learning to Rank Dataset for Medical Information
Retrieval](https://www.cl.uni-heidelberg.de/~riezler/publications/papers/ECIR2016.pdf)
describes NFCorpus as a medical learning-to-rank dataset whose queries come
from NutritionFacts.org health topics and whose relevance links connect those
queries to PubMed and medical articles. The paper highlights the lexical gap
between lay health language and biomedical literature.

[BEIR: A Heterogeneous Benchmark for Zero-shot Evaluation of Information
Retrieval Models](https://arxiv.org/abs/2104.08663) includes NFCorpus as a
bio-medical retrieval task. [MMTEB: Massive Multilingual Text Embedding
Benchmark](https://arxiv.org/abs/2502.13595) provides the multilingual context
for this French split.

### Observed Data Profile

The sampled French Nano task has 50 queries, 2,953 documents, and 1,651
positive qrel rows. Queries average 33.02 positives, with 47 of 50 queries
having multiple positives. The average query length is 29.06 characters, and
the average document length is 1,810.71 characters.

The inspected queries include chicken nuggets, meat cleaning and cola, Atkins
diet, adenovirus 36, and probiotics for common cold prevention. Documents are
long French translated biomedical abstracts or scientific summaries.

### BM25 Difficulty

Using the dataset-provided BM25 candidate column, BM25 reaches nDCG@10 =
0.3489 and hit@10 = 0.6400. BM25 ranks a positive first for 23 queries, and
the median first-positive rank is 2.

BM25 often finds one related document, but ranking remains hard because each
query can have many positives. Strong models should bridge lay French health
phrasing to biomedical mechanisms, interventions, and outcomes.

### Training Data That May Help

Useful training data includes non-overlapping biomedical IR datasets,
consumer-health question to biomedical abstract pairs, PubMed relevance ranking
data, and French or multilingual medical retrieval supervision. Training should
exclude NFCorpus, BEIR, NanoBEIR, or translated NutritionFacts records likely to
overlap with these examples.

### Synthetic Data Guidance

For document-to-query generation, start from non-evaluation biomedical abstracts
and generate short French lay questions or topic labels. Synthetic clusters
should include multiple related evidence documents per health topic so models
learn multi-positive ranking.

## Example Data

| Query | Positive document |
| --- | --- |
| Milkshakes au chocolat santé (28 chars) | Objectif : Étudier la relation entre la consommation de cerises et le risque de crises de goutte récidivantes chez les personnes atteintes de goutte. Méthodes : Nous avons mené une étude cas-témoins appariés pour examiner les ... [truncated 225 chars](2038 chars) |
| éthique médicale (16 chars) | CONTEXTE : L'un des principaux défis dans la gestion du cholestérol sérique par l'intervention diététique semble être l'amélioration de l'adhésion des patients. OBJECTIFS : Explorer les nombreuses questions concernant les obs ... [truncated 225 chars](2144 chars) |
| fèves (5 chars) | Au cours des 20 dernières années, l'intérêt croissant pour la biochimie, la nutrition et la pharmacologie de la L-arginine a conduit à des études approfondies visant à explorer ses rôles nutritionnels et thérapeutiques dans l ... [truncated 225 chars](1531 chars) |
| Qu'est-ce qu'il y a vraiment dans les nuggets de poulet ? (57 chars) | But : Déterminer la composition des nuggets de poulet de deux chaînes de restauration nationales. Contexte : Les nuggets de poulet sont devenus un élément majeur de l'alimentation américaine. Nous avons cherché à déterminer l ... [truncated 225 chars](851 chars) |
| graisses saturées (17 chars) | L'intérêt pour la possibilité que l'alimentation maternelle pendant la grossesse puisse influencer le développement des troubles allergiques chez les enfants a augmenté. La présente étude prospective a examiné l'association e ... [truncated 225 chars](2400 chars) |

## Dataset Information

| Field | Value |
| --- | --- |
| Nano set | MNanoBEIR |
| Backing dataset | NanoBEIR-fr |
| Task / split | NanoNFCorpus |
| Hugging Face dataset | [hakari-bench/NanoBEIR-fr](https://huggingface.co/datasets/hakari-bench/NanoBEIR-fr) |
| Language | fr |
| Category | natural_language |
| Queries | 50 |
| Documents | 2,953 |
| Positive qrels | 1,651 |
| Avg positives / query | 33.02 |
| Positives per query (min / median / max) | 1 / 23.50 / 100 |
| Queries with multiple positives | 47 (94.0%) |
| BM25 nDCG@10 | 0.3026 |
| BM25 hit@10 | 0.6400 |
| BM25 Recall@100 | 0.1666 |
| BM25 candidate subset | top-500 (`bm25`) |
| Dense nDCG@10 | 0.3048 |
| Dense hit@10 | 0.6200 |
| Dense Recall@100 | 0.1962 |
| Dense candidate subset | top-500 (`harrier_oss_v1_270m`) |
| Reranking hybrid nDCG@10 | 0.3099 |
| Reranking hybrid hit@10 | 0.5800 |
| Reranking hybrid Recall@100 | 0.2029 |
| Reranking hybrid candidate subset | top-100 plus optional rank-101 safeguard (`reranking_hybrid`) |
| Reranking hybrid candidates / query | 100-101 |
| Reranking hybrid safeguard rows | 8 |
| Query length avg chars | 29.06 |
| Document length avg chars | 1,810.71 |

### Public Sources

- [A Full-Text Learning to Rank Dataset for Medical Information Retrieval](https://www.cl.uni-heidelberg.de/~riezler/publications/papers/ECIR2016.pdf).
- [NFCorpus project page](https://www.cl.uni-heidelberg.de/statnlpgroup/nfcorpus/).
- [BEIR: A Heterogeneous Benchmark for Zero-shot Evaluation of Information Retrieval Models](https://arxiv.org/abs/2104.08663).
- [MMTEB: Massive Multilingual Text Embedding Benchmark](https://arxiv.org/abs/2502.13595).
- [Zeta Alpha NanoBEIR collection](https://huggingface.co/collections/zeta-alpha-ai/nanobeir).

### Hugging Face Links

- Nano dataset: [hakari-bench/NanoBEIR-fr](https://huggingface.co/datasets/hakari-bench/NanoBEIR-fr)
- Source collection: [Zeta Alpha NanoBEIR collection](https://huggingface.co/collections/zeta-alpha-ai/nanobeir)

### Source Reference Table

| Title | Year | Type | URL |
| --- | ---: | --- | --- |
| A Full-Text Learning to Rank Dataset for Medical Information Retrieval | 2016 | task paper | https://www.cl.uni-heidelberg.de/~riezler/publications/papers/ECIR2016.pdf |
| NFCorpus project page |  | project page | https://www.cl.uni-heidelberg.de/statnlpgroup/nfcorpus/ |
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
  task_name: NanoNFCorpus
  split_name: NanoNFCorpus
  language: fr
  category: natural_language
  document_path: docs/benchmark_tasks/MNanoBEIR/NanoBEIR-fr__NanoNFCorpus.md
  source_research:
    primary_source_type: task_paper
    paper_pdf_or_html_checked: true
    no_paper_note: null
  counts:
    queries: 50
    documents: 2953
    positive_qrels: 1651
  positives_per_query:
    average: 33.02
    min: 1
    median: 23.5
    max: 100
    multi_positive_queries: 47
    multi_positive_query_percent: 94.0
  text_stats_chars:
    query_mean: 29.06
    document_mean: 1810.714866
  bm25:
    ndcg_at_10: 0.30264286131085205
    hit_at_10: 0.64
    source: dataset_candidate_subset
  candidate_subsets:
    bm25:
      config: bm25
      label: BM25
      source: dataset_candidate_subset
      top_k: 500
      ndcg_at_10: 0.3026428613
      hit_at_10: 0.64
      recall_at_100: 0.1665657177
      candidate_count_min: 500
      candidate_count_max: 500
      candidate_count_mean: 500.0
      query_count: 50
      query_coverage: 1.0
      relevant_coverage_at_100: 0.1665657177
    dense:
      config: harrier_oss_v1_270m
      label: Dense
      source: dataset_candidate_subset
      top_k: 500
      ndcg_at_10: 0.3048113218
      hit_at_10: 0.62
      recall_at_100: 0.1962447002
      candidate_count_min: 500
      candidate_count_max: 500
      candidate_count_mean: 500.0
      query_count: 50
      query_coverage: 1.0
      relevant_coverage_at_100: 0.1962447002
    reranking_hybrid:
      config: reranking_hybrid
      label: Reranking hybrid
      source: dataset_candidate_subset
      top_k: 100
      ndcg_at_10: 0.3099159636
      hit_at_10: 0.58
      recall_at_100: 0.2029073289
      candidate_count_min: 100
      candidate_count_max: 101
      candidate_count_mean: 100.16
      query_count: 50
      query_coverage: 1.0
      relevant_coverage_at_100: 0.2029073289
      safeguard_positive_rows: 8
      rows_with_101_candidates: 8
```
