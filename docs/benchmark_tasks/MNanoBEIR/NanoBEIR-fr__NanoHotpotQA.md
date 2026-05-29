# MNanoBEIR / NanoBEIR-fr / NanoHotpotQA

## Overview

HotpotQA is a multi-hop question answering benchmark built from Wikipedia.
`NanoBEIR-fr__NanoHotpotQA` is the French MNanoBEIR version: French translated
multi-hop questions must retrieve French translated supporting Wikipedia
passages. The task tests whether a retriever can surface the evidence pages
needed for bridge or comparison reasoning.

## Details

### What the Original Data Measures

[HotpotQA: A Dataset for Diverse, Explainable Multi-hop Question
Answering](https://arxiv.org/abs/1809.09600) introduces a Wikipedia QA dataset
designed to require reasoning over multiple supporting documents. The paper
builds bridge questions from the Wikipedia hyperlink graph and comparison
questions over similar entities.

[BEIR: A Heterogeneous Benchmark for Zero-shot Evaluation of Information
Retrieval Models](https://arxiv.org/abs/2104.08663) includes HotpotQA as a QA
retrieval task where supporting evidence must be retrieved. [MMTEB: Massive
Multilingual Text Embedding Benchmark](https://arxiv.org/abs/2502.13595)
provides the multilingual context for this French split.

### Observed Data Profile

The sampled French Nano task has 50 queries, 5,090 documents, and 100 positive
qrel rows. Every query has exactly two positive passages. The average query
length is 98.60 characters, and the average document length is 389.24
characters.

The inspected questions compare tennis players, ask about Ian Hunter and Rob
Thomas, compare Czesław Miłosz and Nathalie Sarraute, identify a Joby Harold
film, and ask about Arthur Noss. Positive documents are short French translated
Wikipedia-style entity descriptions.

### BM25 Difficulty

Using the dataset-provided BM25 candidate column, BM25 reaches nDCG@10 =
0.7143 and hit@10 = 0.9200. BM25 ranks a positive first for 35 queries, and
the median first-positive rank is 1.

The main difficulty is retrieving both supporting documents. A retriever that
finds only the most obvious entity page can still fail the multi-hop evidence
need. Strong models should preserve bridge relations, comparisons, aliases, and
the second supporting entity.

### Training Data That May Help

Useful training data includes non-overlapping HotpotQA examples with supporting
facts, multi-hop QA retrieval datasets, Wikipedia hyperlink graph retrieval
pairs, and French or multilingual question-to-multiple-document supervision.
Training should exclude HotpotQA, BEIR, NanoBEIR, or translated records likely
to overlap with these evaluation questions or pages.

### Synthetic Data Guidance

For document-to-query generation, start from connected pairs of French
Wikipedia-style passages and generate bridge or comparison questions. For joint
generation, create paired entity passages linked by occupation, nationality,
creator, dates, or events and require both passages as positives.

## Example Data

| Query | Positive document |
| --- | --- |
| Avec quel autre acteur Penny Rae Bridges a-t-elle joué dans une sitcom ? (72 chars) | Penny Rae Bridges (née le 29 juillet 1990) est une actrice américaine. Elle a joué dans les séries "For Your Love", "Family Law", "Boy Meets World" et "The Parent 'Hood". Elle est surtout connue pour son rôle dans "Half & Hal ... [truncated 225 chars](252 chars) |
| Qui a donné à Kaganoi Shigemochi une lame forgée par Masamune, le fondateur de l'école Muramasa ? (97 chars) | Kaganoi Shigemochi (加賀井 重望, 1561 – 27 août 1600) était un samouraï japonais de la période Azuchi-Momoyama, au service du clan Oda. Il gouvernait le château de Kaganoi. Lors de la bataille de Komaki et Nagakute, Shigemochi com ... [truncated 225 chars](606 chars) |
| Quel film a été écrit et réalisé par Joby Harold avec la musique de Samuel Sim ? (80 chars) | Samuel Sim est un compositeur de films et de séries télévisées. Il a acquis une notoriété avec sa bande originale récompensée pour la série dramatique de la BBC "Dunkirk". Depuis, il a composé la musique pour une grande varié ... [truncated 225 chars](600 chars) |
| Quand a eu lieu ce match de football universitaire au Sun Life Stadium à Miami Gardens, en Floride, où Clemson a battu les Sooners de l'Oklahoma, classés 4e, sur le score de 37-17 ? (181 chars) | L'équipe de football des Tigers de Clemson de 2015 a représenté l'Université de Clemson lors de la saison 2015 de la NCAA Division I FBS. Les Tigers étaient dirigés par l'entraîneur-chef Dabo Swinney, en sa septième année com ... [truncated 225 chars](1181 chars) |
| Plat du Diable est un album de titres d'un groupe de rock and roll américain qui a également été connu pour jouer des concerts country sous quel nom ? (150 chars) | Diabolique est une compilation de singles du groupe américain de rock 'n' roll Supersuckers, sortie en avril 2005 chez Mid-Fi Records. (134 chars) |

## Dataset Information

| Field | Value |
| --- | --- |
| Nano set | MNanoBEIR |
| Backing dataset | NanoBEIR-fr |
| Task / split | NanoHotpotQA |
| Hugging Face dataset | [hakari-bench/NanoBEIR-fr](https://huggingface.co/datasets/hakari-bench/NanoBEIR-fr) |
| Language | fr |
| Category | natural_language |
| Queries | 50 |
| Documents | 5,090 |
| Positive qrels | 100 |
| Avg positives / query | 2.00 |
| Positives per query (min / median / max) | 2 / 2.00 / 2 |
| Queries with multiple positives | 50 (100.0%) |
| BM25 nDCG@10 | 0.7258 |
| BM25 hit@10 | 0.9400 |
| BM25 Recall@100 | 0.9200 |
| BM25 candidate subset | top-500 (`bm25`) |
| Dense nDCG@10 | 0.7564 |
| Dense hit@10 | 0.9600 |
| Dense Recall@100 | 0.9300 |
| Dense candidate subset | top-500 (`harrier_oss_v1_270m`) |
| Reranking hybrid nDCG@10 | 0.7834 |
| Reranking hybrid hit@10 | 1.0000 |
| Reranking hybrid Recall@100 | 0.9500 |
| Reranking hybrid candidate subset | top-100 plus optional rank-101 safeguard (`reranking_hybrid`) |
| Reranking hybrid candidates / query | 100 |
| Reranking hybrid safeguard rows | 0 |
| Query length avg chars | 98.60 |
| Document length avg chars | 389.24 |

### Public Sources

- [HotpotQA: A Dataset for Diverse, Explainable Multi-hop Question Answering](https://arxiv.org/abs/1809.09600).
- [HotpotQA official site](https://hotpotqa.github.io/).
- [BEIR: A Heterogeneous Benchmark for Zero-shot Evaluation of Information Retrieval Models](https://arxiv.org/abs/2104.08663).
- [MMTEB: Massive Multilingual Text Embedding Benchmark](https://arxiv.org/abs/2502.13595).
- [Zeta Alpha NanoBEIR collection](https://huggingface.co/collections/zeta-alpha-ai/nanobeir).

### Hugging Face Links

- Nano dataset: [hakari-bench/NanoBEIR-fr](https://huggingface.co/datasets/hakari-bench/NanoBEIR-fr)
- Source collection: [Zeta Alpha NanoBEIR collection](https://huggingface.co/collections/zeta-alpha-ai/nanobeir)

### Source Reference Table

| Title | Year | Type | URL |
| --- | ---: | --- | --- |
| HotpotQA: A Dataset for Diverse, Explainable Multi-hop Question Answering | 2018 | task paper | https://arxiv.org/abs/1809.09600 |
| HotpotQA official site |  | project page | https://hotpotqa.github.io/ |
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
  task_name: NanoHotpotQA
  split_name: NanoHotpotQA
  language: fr
  category: natural_language
  document_path: docs/benchmark_tasks/MNanoBEIR/NanoBEIR-fr__NanoHotpotQA.md
  source_research:
    primary_source_type: task_paper
    paper_pdf_or_html_checked: true
    no_paper_note: null
  counts:
    queries: 50
    documents: 5090
    positive_qrels: 100
  positives_per_query:
    average: 2.0
    min: 2
    median: 2.0
    max: 2
    multi_positive_queries: 50
    multi_positive_query_percent: 100.0
  text_stats_chars:
    query_mean: 98.6
    document_mean: 389.244204
  bm25:
    ndcg_at_10: 0.7257862371086377
    hit_at_10: 0.94
    source: dataset_candidate_subset
  candidate_subsets:
    bm25:
      config: bm25
      label: BM25
      source: dataset_candidate_subset
      top_k: 500
      ndcg_at_10: 0.7257862371
      hit_at_10: 0.94
      recall_at_100: 0.92
      candidate_count_min: 500
      candidate_count_max: 500
      candidate_count_mean: 500.0
      query_count: 50
      query_coverage: 1.0
      relevant_coverage_at_100: 0.92
    dense:
      config: harrier_oss_v1_270m
      label: Dense
      source: dataset_candidate_subset
      top_k: 500
      ndcg_at_10: 0.7563951793
      hit_at_10: 0.96
      recall_at_100: 0.93
      candidate_count_min: 500
      candidate_count_max: 500
      candidate_count_mean: 500.0
      query_count: 50
      query_coverage: 1.0
      relevant_coverage_at_100: 0.93
    reranking_hybrid:
      config: reranking_hybrid
      label: Reranking hybrid
      source: dataset_candidate_subset
      top_k: 100
      ndcg_at_10: 0.7833808877
      hit_at_10: 1.0
      recall_at_100: 0.95
      candidate_count_min: 100
      candidate_count_max: 100
      candidate_count_mean: 100.0
      query_count: 50
      query_coverage: 1.0
      relevant_coverage_at_100: 0.95
      safeguard_positive_rows: 0
      rows_with_101_candidates: 0
```
