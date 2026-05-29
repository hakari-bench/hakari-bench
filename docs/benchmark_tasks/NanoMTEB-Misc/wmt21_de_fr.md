# NanoMTEB-Misc / wmt21_de_fr

## Overview

`NanoMTEB-Misc / wmt21_de_fr` is the WMT21 German-French direction of CLSD.
French news sentences retrieve German translation counterparts.

## Details

### What the Original Data Measures

[Cross-Lingual Semantic Discrimination for Building Better Multilingual
Embeddings](https://arxiv.org/abs/2502.08638) introduces CLSD to evaluate
cross-lingual semantic equivalence under difficult distractors. The WMT21
German-French variants use sentence-level parallel news data and require a
retriever to identify the true translation in another language.

The [clsd_wmt19_21 dataset card](https://huggingface.co/datasets/Andrianos/clsd_wmt19_21)
is the public dataset record used by MTEB. In this split, queries are French
and documents are German.

### Observed Data Profile

The split has 200 queries, 4,465 documents, and 200 positive qrel rows. Every
query has one positive. Queries average 170.06 characters and documents average
177.26 characters. Samples are Reuters-style financial and political news
sentences.

### BM25 Difficulty

Using the dataset-provided BM25 candidate column, BM25 reaches nDCG@10 =
0.2167 and hit@10 = 0.3500. It ranks 22 positives at rank 1 and 70 in the top
10.

BM25 has little cross-lingual signal except numbers, names, and shared
international terms. The task is therefore a direct probe of German-French
embedding alignment at the sentence level.

### Training Data That May Help

German-French parallel news data, sentence-transformer contrastive training,
translation-pair mining, and hard negatives with same entities and altered
facts are useful. Domain-matched WMT-style news sentences are especially
relevant.

### Synthetic Data Guidance

Build synthetic examples from non-evaluation French-German sentence pairs and
create distractors that preserve market numbers, names, or organizations while
changing the meaning. Include paraphrases and literal translations, and avoid
labeling same-topic but non-equivalent sentences as positives.

## Example Data

| Query | Positive document |
| --- | --- |
| Le même jour, le bureau du premier ministre a fait savoir que Justin Trudeau témoignerait lui aussi devant cette commission, comme l'exige l'opposition, à une date restant à déterminer. (185 chars) | Am selben Tag kündigte das Büro des Premierministers an, dass Justin Trudeau, wie von der Opposition gefordert, zu einem noch zu bestimmenden Termin ebenfalls vor diesem Ausschuss aussagen wird. (194 chars) |
| Le président Sebastian Piñera a promulgué le 24 juillet une réforme historique qui permet aux Chiliens le retrait anticipé de 10% de leurs fonds de retraite privés pour faire face à la crise économique entraînée par la pandém ... [truncated 225 chars](240 chars) | Präsident Sebastian Piñera verkündete am 24. Juli eine historische Reform, die es den Chilenen erlaubt, 10 % ihrer privaten Rentenfonds vorzeitig zu entnehmen, um die durch die Covid-19-Pandemie verursachte Wirtschaftskrise z ... [truncated 225 chars](238 chars) |
| Des ajustements mineurs qui doivent libérer plus de capital pour les investisseurs et donc permettre aux "entreprises d'obtenir plus facilement les financements dont elles ont besoin et d'investir dans notre économie", assure ... [truncated 225 chars](292 chars) | Geringfügige Anpassungen sollen mehr Kapital für Investoren freisetzen und es so „den Unternehmen leichter machen, die benötigte Finanzierung zu erhalten und in unsere Wirtschaft zu investieren“, versichert der Vizepräsident ... [truncated 225 chars](272 chars) |
| Les géants Apple, Alphabet Inc et Amazon.com doivent publier leurs résultats le 30 juillet, le jour où le département du Commerce doit annoncer sa première estimation du PIB du deuxième trimestre, attendu en chute de 35% par ... [truncated 225 chars](239 chars) | Die Giganten Apple, Alphabet Inc und Amazon.com werden ihre Ergebnisse am 30. Juli vorlegen, dem gleichen Tag, an dem das Handelsministerium seine erste Schätzung für das BIP aus dem zweiten Quartal bekanntgeben wird, das nac ... [truncated 225 chars](270 chars) |
| Justin Trudeau avait admis avoir commis une erreur en ne se retirant pas des discussions lors des négociations entre son gouvernement et UNIS. (142 chars) | Justin Trudeau hatte zugegeben, dass er einen Fehler gemacht hat, als er sich während der Verhandlungen zwischen seiner Regierung und UNIS nicht von den Gesprächen fernhielt. (174 chars) |

## Dataset Information

| Field | Value |
| --- | --- |
| Nano set | NanoMTEB-Misc |
| Backing dataset | NanoMTEB-Misc |
| Task / split | wmt21_de_fr |
| Hugging Face dataset | [hakari-bench/NanoMTEB-Misc](https://huggingface.co/datasets/hakari-bench/NanoMTEB-Misc) |
| Source dataset | [Andrianos/clsd_wmt19_21](https://huggingface.co/datasets/Andrianos/clsd_wmt19_21) |
| Language | multilingual |
| Category | natural_language |
| Queries | 200 |
| Documents | 4,465 |
| Positive qrels | 200 |
| BM25 nDCG@10 | 0.3127 |
| BM25 hit@10 | 0.4400 |
| BM25 Recall@100 | 0.6950 |
| BM25 candidate subset | top-500 (`bm25`) |
| Dense nDCG@10 | 0.9249 |
| Dense hit@10 | 0.9700 |
| Dense Recall@100 | 0.9700 |
| Dense candidate subset | top-500 (`harrier_oss_v1_270m`) |
| Reranking hybrid nDCG@10 | 0.5988 |
| Reranking hybrid hit@10 | 0.7300 |
| Reranking hybrid Recall@100 | 0.9950 |
| Reranking hybrid candidate subset | top-100 plus optional rank-101 safeguard (`reranking_hybrid`) |
| Reranking hybrid candidates / query | 100-101 |
| Reranking hybrid safeguard rows | 1 |
| Query length avg chars | 170.06 |
| Document length avg chars | 177.26 |

### Public Sources

- [Cross-Lingual Semantic Discrimination for Building Better Multilingual Embeddings](https://arxiv.org/abs/2502.08638), CLSD task paper.
- [Andrianos/clsd_wmt19_21](https://huggingface.co/datasets/Andrianos/clsd_wmt19_21), dataset card.
- [MTEB retrieval task listing](https://embeddings-benchmark.github.io/mteb/overview/available_tasks/retrieval/), task metadata.

### Hugging Face Links

- Nano dataset: [hakari-bench/NanoMTEB-Misc](https://huggingface.co/datasets/hakari-bench/NanoMTEB-Misc)
- Source task dataset: [Andrianos/clsd_wmt19_21](https://huggingface.co/datasets/Andrianos/clsd_wmt19_21)

### Source Reference Table

| Title | Year | Type | URL |
| --- | ---: | --- | --- |
| Cross-Lingual Semantic Discrimination for Building Better Multilingual Embeddings | 2025 | task paper | https://arxiv.org/abs/2502.08638 |
| Andrianos/clsd_wmt19_21 |  | dataset card | https://huggingface.co/datasets/Andrianos/clsd_wmt19_21 |
| MTEB retrieval task listing |  | benchmark metadata | https://embeddings-benchmark.github.io/mteb/overview/available_tasks/retrieval/ |

## Machine-Readable Metadata

<!-- benchmark-task-metadata:v1 -->

```yaml
benchmark_task_metadata:
  schema_version: 1
  document_status: first_pass
  nano_set: NanoMTEB-Misc
  backing_dataset: NanoMTEB-Misc
  dataset_id: hakari-bench/NanoMTEB-Misc
  task_name: wmt21_de_fr
  split_name: wmt21_de_fr
  language: multilingual
  category: natural_language
  document_path: docs/benchmark_tasks/NanoMTEB-Misc/wmt21_de_fr.md
  source_research:
    primary_source_type: task_paper
    paper_pdf_or_html_checked: true
    no_paper_note: null
  counts:
    queries: 200
    documents: 4465
    positive_qrels: 200
  positives_per_query:
    average: 1.0
    min: 1
    median: 1.0
    max: 1
    multi_positive_queries: 0
    multi_positive_query_percent: 0.0
  text_stats_chars:
    query_mean: 170.06
    document_mean: 177.26
  bm25:
    ndcg_at_10: 0.3127449028059549
    hit_at_10: 0.44
    source: dataset_candidate_subset
  example_count: 5
  candidate_subsets:
    bm25:
      config: bm25
      label: BM25
      source: dataset_candidate_subset
      top_k: 500
      ndcg_at_10: 0.3127449028
      hit_at_10: 0.44
      recall_at_100: 0.695
      candidate_count_min: 500
      candidate_count_max: 500
      candidate_count_mean: 500.0
      query_count: 200
      query_coverage: 1.0
      relevant_coverage_at_100: 0.695
    dense:
      config: harrier_oss_v1_270m
      label: Dense
      source: dataset_candidate_subset
      top_k: 500
      ndcg_at_10: 0.9248789621
      hit_at_10: 0.97
      recall_at_100: 0.97
      candidate_count_min: 500
      candidate_count_max: 500
      candidate_count_mean: 500.0
      query_count: 200
      query_coverage: 1.0
      relevant_coverage_at_100: 0.97
    reranking_hybrid:
      config: reranking_hybrid
      label: Reranking hybrid
      source: dataset_candidate_subset
      top_k: 100
      ndcg_at_10: 0.5987722389
      hit_at_10: 0.73
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
