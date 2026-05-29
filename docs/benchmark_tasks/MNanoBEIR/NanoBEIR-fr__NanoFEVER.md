# MNanoBEIR / NanoBEIR-fr / NanoFEVER

## Overview

FEVER is a Wikipedia fact verification benchmark. `NanoBEIR-fr__NanoFEVER` is
the French MNanoBEIR version: French translated claims must retrieve French
translated Wikipedia evidence pages. The task tests fact-checking evidence
retrieval for short claims across broad encyclopedic topics.

## Details

### What the Original Data Measures

[FEVER: a Large-scale Dataset for Fact Extraction and
VERification](https://arxiv.org/abs/1803.05355) introduces claims generated from
Wikipedia and annotated with evidence supporting or refuting each claim. In the
BEIR retrieval framing, the task is to find the evidence documents that make
verification possible.

[BEIR: A Heterogeneous Benchmark for Zero-shot Evaluation of Information
Retrieval Models](https://arxiv.org/abs/2104.08663) includes FEVER as a
fact-checking retrieval task. [MMTEB: Massive Multilingual Text Embedding
Benchmark](https://arxiv.org/abs/2502.13595) supplies the multilingual context
for this French split.

### Observed Data Profile

The sampled French Nano task has 50 queries, 4,996 documents, and 57 positive
qrel rows. Most queries have one positive document, while 6 queries have
multiple positives. The average query length is 51.22 characters, and the
average document length is 1,325.25 characters.

The inspected claims concern Vic Mensa, the Tenth Doctor, Menace II Society,
Alex Jones, and The Man in the Iron Mask. Positive documents are French
translated Wikipedia-style pages containing the facts needed for verification.

### BM25 Difficulty

Using the dataset-provided BM25 candidate column, BM25 reaches nDCG@10 =
0.7567 and hit@10 = 0.9000. BM25 ranks a positive first for 30 queries, and
the median first-positive rank is 1.

BM25 is strong because many claims contain explicit entity names. The remaining
difficulty is finding the page that verifies a relation such as date, role,
setting, or director, especially when the claim is false and shares wording with
a plausible but incorrect entity page.

### Training Data That May Help

Useful training data includes non-overlapping FEVER evidence retrieval pairs,
French or multilingual Wikipedia claim verification data, entity-centric QA
evidence pairs, and hard negatives from similar entity pages. Training should
exclude FEVER, BEIR, NanoBEIR, or translated records likely to overlap with
these evaluation claims or pages.

### Synthetic Data Guidance

For document-to-query generation, start from non-evaluation French
Wikipedia-style passages and generate supported and contradicted factual claims.
For joint generation, create related entity pages and claims that require
selecting the evidence page with the right relation, not simply the most
overlapping title.

## Example Data

| Query | Positive document |
| --- | --- |
| Keith Godchaux connaissait les Grateful Dead. (45 chars) | Les Grateful Dead étaient un groupe de rock américain formé en 1965 à Palo Alto, en Californie. Composé de cinq à sept membres, le groupe est connu pour son style unique et éclectique, qui fusionnait des éléments de rock, de ... [truncated 225 chars](3140 chars) |
| Taarak Mehta Ka Ooltah Chashmah est une sitcom. (47 chars) | Taarak Mehta Ka Ooltah Chashmah (en anglais : La Perspective Différente de Taarak Mehta) est la sitcom la plus longue en cours de diffusion en Inde, produite par Neela Tele Films Private Limited. La série a été diffusée pour ... [truncated 225 chars](643 chars) |
| Des avions de pointe et secrets ont été fabriqués à Burbank, en Californie. (75 chars) | Burbank est une ville située dans le comté de Los Angeles, en Californie du Sud, aux États-Unis, à environ 19 km au nord-ouest du centre-ville de Los Angeles. Lors du recensement de 2010, la population était de 103 340 habita ... [truncated 225 chars](1525 chars) |
| Nero est une personne. (22 chars) | La dynastie julio-claudienne désigne les cinq premiers empereurs romains -- Auguste, Tibère, Caligula, Claude et Néron -- ou la famille à laquelle ils appartenaient. Ils ont gouverné l'Empire romain depuis sa formation sous A ... [truncated 225 chars](2138 chars) |
| Scream 2 est un film exclusivement allemand. (44 chars) | Scream 2 est un film d'horreur américain de 1997 réalisé par Wes Craven et écrit par Kevin Williamson. Il met en vedette David Arquette, Neve Campbell, Courteney Cox, Sarah Michelle Gellar, Jamie Kennedy, Laurie Metcalf, Jerr ... [truncated 225 chars](2643 chars) |

## Dataset Information

| Field | Value |
| --- | --- |
| Nano set | MNanoBEIR |
| Backing dataset | NanoBEIR-fr |
| Task / split | NanoFEVER |
| Hugging Face dataset | [hakari-bench/NanoBEIR-fr](https://huggingface.co/datasets/hakari-bench/NanoBEIR-fr) |
| Language | fr |
| Category | natural_language |
| Queries | 50 |
| Documents | 4,996 |
| Positive qrels | 57 |
| Avg positives / query | 1.14 |
| Positives per query (min / median / max) | 1 / 1.00 / 3 |
| Queries with multiple positives | 6 (12.0%) |
| BM25 nDCG@10 | 0.7469 |
| BM25 hit@10 | 0.9200 |
| BM25 Recall@100 | 0.9649 |
| BM25 candidate subset | top-500 (`bm25`) |
| Dense nDCG@10 | 0.8194 |
| Dense hit@10 | 0.9400 |
| Dense Recall@100 | 0.9298 |
| Dense candidate subset | top-500 (`harrier_oss_v1_270m`) |
| Reranking hybrid nDCG@10 | 0.7803 |
| Reranking hybrid hit@10 | 0.9200 |
| Reranking hybrid Recall@100 | 1.0000 |
| Reranking hybrid candidate subset | top-100 plus optional rank-101 safeguard (`reranking_hybrid`) |
| Reranking hybrid candidates / query | 100 |
| Reranking hybrid safeguard rows | 0 |
| Query length avg chars | 51.22 |
| Document length avg chars | 1,325.25 |

### Public Sources

- [FEVER: a Large-scale Dataset for Fact Extraction and VERification](https://arxiv.org/abs/1803.05355).
- [FEVER shared task site](https://fever.ai/).
- [BEIR: A Heterogeneous Benchmark for Zero-shot Evaluation of Information Retrieval Models](https://arxiv.org/abs/2104.08663).
- [MMTEB: Massive Multilingual Text Embedding Benchmark](https://arxiv.org/abs/2502.13595).
- [Zeta Alpha NanoBEIR collection](https://huggingface.co/collections/zeta-alpha-ai/nanobeir).

### Hugging Face Links

- Nano dataset: [hakari-bench/NanoBEIR-fr](https://huggingface.co/datasets/hakari-bench/NanoBEIR-fr)
- Source collection: [Zeta Alpha NanoBEIR collection](https://huggingface.co/collections/zeta-alpha-ai/nanobeir)

### Source Reference Table

| Title | Year | Type | URL |
| --- | ---: | --- | --- |
| FEVER: a Large-scale Dataset for Fact Extraction and VERification | 2018 | task paper | https://arxiv.org/abs/1803.05355 |
| FEVER shared task site |  | project page | https://fever.ai/ |
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
  task_name: NanoFEVER
  split_name: NanoFEVER
  language: fr
  category: natural_language
  document_path: docs/benchmark_tasks/MNanoBEIR/NanoBEIR-fr__NanoFEVER.md
  source_research:
    primary_source_type: task_paper
    paper_pdf_or_html_checked: true
    no_paper_note: null
  counts:
    queries: 50
    documents: 4996
    positive_qrels: 57
  positives_per_query:
    average: 1.14
    min: 1
    median: 1.0
    max: 3
    multi_positive_queries: 6
    multi_positive_query_percent: 12.0
  text_stats_chars:
    query_mean: 51.22
    document_mean: 1325.248799
  bm25:
    ndcg_at_10: 0.7469205665919203
    hit_at_10: 0.92
    source: dataset_candidate_subset
  candidate_subsets:
    bm25:
      config: bm25
      label: BM25
      source: dataset_candidate_subset
      top_k: 500
      ndcg_at_10: 0.7469205666
      hit_at_10: 0.92
      recall_at_100: 0.9649122807
      candidate_count_min: 500
      candidate_count_max: 500
      candidate_count_mean: 500.0
      query_count: 50
      query_coverage: 1.0
      relevant_coverage_at_100: 0.9649122807
    dense:
      config: harrier_oss_v1_270m
      label: Dense
      source: dataset_candidate_subset
      top_k: 500
      ndcg_at_10: 0.8193982747
      hit_at_10: 0.94
      recall_at_100: 0.9298245614
      candidate_count_min: 500
      candidate_count_max: 500
      candidate_count_mean: 500.0
      query_count: 50
      query_coverage: 1.0
      relevant_coverage_at_100: 0.9298245614
    reranking_hybrid:
      config: reranking_hybrid
      label: Reranking hybrid
      source: dataset_candidate_subset
      top_k: 100
      ndcg_at_10: 0.7802744291
      hit_at_10: 0.92
      recall_at_100: 1.0
      candidate_count_min: 100
      candidate_count_max: 100
      candidate_count_mean: 100.0
      query_count: 50
      query_coverage: 1.0
      relevant_coverage_at_100: 1.0
      safeguard_positive_rows: 0
      rows_with_101_candidates: 0
```
