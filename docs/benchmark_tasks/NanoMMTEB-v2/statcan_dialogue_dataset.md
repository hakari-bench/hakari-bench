# NanoMMTEB-v2 / statcan_dialogue_dataset

## Overview

`statcan_dialogue_dataset` is an English/French conversational table-retrieval
task. Queries are partial live-chat conversations with Statistics Canada users,
and documents are metadata-rich StatCan table descriptions. The retriever must
find the table that would satisfy the user's information need.

## Details

### What the Original Data Measures

[A Dataset for Retrieving Data Tables through Conversations with Genuine Intents](https://arxiv.org/abs/2304.01412)
reports 19,379 conversation turns between Statistics Canada agents and users
looking for published data tables. The paper frames retrieval as finding the
right table from an ongoing conversation and highlights temporal splits,
English/French data, and table metadata as retrieval targets.

### Observed Data Profile

The split has 200 queries, 10,000 documents, and 313 positive qrels. Queries
average 794.77 characters and often serialize multiple user/operator turns.
Documents average 7,237.69 characters, but some table descriptions are far
longer because they include dimensions, subjects, survey fields, and large
metadata payloads. Positives average 1.56 per query.

### BM25 Difficulty

Using the dataset-provided BM25 candidate column, BM25 reaches nDCG@10 = 0.0111
and hit@10 = 0.0300. This is extremely difficult for lexical ranking because
users ask conversationally, mix English/French, and refer to table needs rather
than repeating official table titles or metadata terms.

### Training Data That May Help

Useful data includes conversational search, table retrieval, government
statistics search logs, bilingual English/French support conversations, and
metadata-to-query pairs. Training should avoid overlapping StatCan conversations
and target table IDs from the evaluation split.

### Synthetic Data Guidance

Generate partial support conversations where users ask for official statistics
by geography, date range, sector, and measure. Pair them with realistic table
metadata containing title, dimensions, survey, frequency, and subject. Hard
negatives should be tables from the same domain but wrong geography, period, or
measure.

## Example Data

| Query | Positive document |
| --- | --- |
| [{'content': 'Bonjour,', 'role': 'user'}, {'content': "J'aimerais connaître le moyen de trouver le PIB nominal par habitant d'une province, son PIB réel, son taux de croissance économique ainsi que son taux d'inflation. Je ne ... [truncated 225 chars](523 chars) | Titre: Produit intérieur brut (PIB) aux prix de base, par industries, provinces et territoires Période: 1997-01-01 to 2020-01-01 Dimensions: Géographie, Valeur, Système de classification des industries de l'Amérique du Nord ( ... [truncated 225 chars](26426 chars) |
| [{'content': "Hi, I'm having trouble finding data (custom table) that has race/ethnicity by province and sex", 'role': 'user'}, {'content': 'using 2016 census data', 'role': 'user'}, {'content': 'Hello, my name is Jeremie. I ... [truncated 225 chars](1238 chars) | Title: Persons with and without disabilities aged 15 years and over, by age group and sex, Canada, provinces and territories Date range: 2017-01-01 to 2017-01-01 Dimensions: Geography, Age group, Sex, Disability, Estimates Su ... [truncated 225 chars](1709 chars) |
| [{'content': 'hello', 'role': 'user'}, {'content': 'how many shops specialized in sports are there in canada ?', 'role': 'user'}, {'content': 'Hello, my name is Jimmy N., how may I help you?', 'role': 'operator'}] (213 chars) | Title: Canadian Business Counts, with employees, June 2019 Date range: 2019-01-01 to 2019-01-01 Dimensions: Geography, Employment size, North American Industry Classification System (NAICS) Subject: Business performance and o ... [truncated 225 chars](87780 chars) |
| [{'content': 'Bonjour,', 'role': 'user'}, {'content': "J'aimerais connaître le taux d'inflation au 31 décembre 2019?", 'role': 'user'}, {'content': "Pour le mois de décembre 2019 ou pour l'année 2019?", 'role': 'operator'}, { ... [truncated 225 chars](861 chars) | Titre: Indice des prix à la consommation, moyenne annuelle, non désaisonnalisé Période: 1914-01-01 to 2020-01-01 Dimensions: Géographie, Produits et groupes de produits Sujet: Prix et indices des prix Enquête: Indice des prix ... [truncated 225 chars](22778 chars) |
| [{'content': "Hi, I was wondering if you have any health data on the Tk'emlups Te Secwepemc band?", 'role': 'user'}, {'content': "Hello, my name is Olivier C. Please wait while i'm searching for this information.", 'role': 'o ... [truncated 225 chars](564 chars) | Title: Health indicator profile, by Aboriginal identity and sex, age-standardized rate, four year estimates Date range: 2007-01-01 to 2011-01-01 Dimensions: Geography, Sex, Aboriginal identity, Indicators, Characteristics Sub ... [truncated 225 chars](4353 chars) |

## Dataset Information

| Field | Value |
| --- | --- |
| Nano set | NanoMMTEB-v2 |
| Backing dataset | NanoMMTEB-v2 |
| Task / split | statcan_dialogue_dataset |
| Hugging Face dataset | [hakari-bench/NanoMMTEB-v2](https://huggingface.co/datasets/hakari-bench/NanoMMTEB-v2) |
| Source dataset | [mteb/StatcanDialogueDatasetRetrieval](https://huggingface.co/datasets/mteb/StatcanDialogueDatasetRetrieval) |
| Language | multilingual |
| Category | natural_language |
| Queries | 200 |
| Documents | 10000 |
| Positive qrels | 313 |
| Avg positives / query | 1.56 |
| Positives per query (min / median / max) | 1 / 1.0 / 9 |
| Queries with multiple positives | 56 (28.00%) |
| BM25 nDCG@10 | 0.0112 |
| BM25 hit@10 | 0.0300 |
| BM25 Recall@100 | 0.1406 |
| BM25 candidate subset | top-500 (`bm25`) |
| Dense nDCG@10 | 0.2731 |
| Dense hit@10 | 0.4550 |
| Dense Recall@100 | 0.7220 |
| Dense candidate subset | top-500 (`harrier_oss_v1_270m`) |
| Reranking hybrid nDCG@10 | 0.1564 |
| Reranking hybrid hit@10 | 0.3400 |
| Reranking hybrid Recall@100 | 0.6581 |
| Reranking hybrid candidate subset | top-100 plus optional rank-101 safeguard (`reranking_hybrid`) |
| Reranking hybrid candidates / query | 100-101 |
| Reranking hybrid safeguard rows | 47 |
| Query length avg chars | 794.77 |
| Document length avg chars | 7237.69 |

### Public Sources

- [A Dataset for Retrieving Data Tables through Conversations with Genuine Intents](https://arxiv.org/abs/2304.01412).
- [StatCan Dialogue Dataset project page](https://mcgill-nlp.github.io/statcan-dialogue-dataset/).
- [mteb/StatcanDialogueDatasetRetrieval](https://huggingface.co/datasets/mteb/StatcanDialogueDatasetRetrieval).

### Hugging Face Links

- Nano dataset: [hakari-bench/NanoMMTEB-v2](https://huggingface.co/datasets/hakari-bench/NanoMMTEB-v2)
- Source dataset: [mteb/StatcanDialogueDatasetRetrieval](https://huggingface.co/datasets/mteb/StatcanDialogueDatasetRetrieval)

### Source Reference Table

| Title | Year | Type | URL |
| --- | ---: | --- | --- |
| A Dataset for Retrieving Data Tables through Conversations with Genuine Intents | 2023 | task paper | https://arxiv.org/abs/2304.01412 |
| StatCan Dialogue Dataset project page | 2023 | project page | https://mcgill-nlp.github.io/statcan-dialogue-dataset/ |
| mteb/StatcanDialogueDatasetRetrieval | 2024 | dataset card | https://huggingface.co/datasets/mteb/StatcanDialogueDatasetRetrieval |

## Machine-Readable Metadata

<!-- benchmark-task-metadata:v1 -->

```yaml
benchmark_task_metadata:
  schema_version: 1
  document_status: first_pass
  nano_set: NanoMMTEB-v2
  backing_dataset: NanoMMTEB-v2
  dataset_id: hakari-bench/NanoMMTEB-v2
  task_name: statcan_dialogue_dataset
  split_name: statcan_dialogue_dataset
  language: multilingual
  category: natural_language
  document_path: docs/benchmark_tasks/NanoMMTEB-v2/statcan_dialogue_dataset.md
  source_research:
    primary_source_type: task_paper
    paper_pdf_or_html_checked: true
    no_paper_note: null
  counts:
    queries: 200
    documents: 10000
    positive_qrels: 313
  positives_per_query:
    average: 1.565
    min: 1
    median: 1.0
    max: 9
    multi_positive_queries: 56
    multi_positive_query_percent: 28.0
  text_stats_chars:
    query_mean: 794.77
    document_mean: 7237.6861
  bm25:
    ndcg_at_10: 0.011182567329507074
    hit_at_10: 0.03
    source: dataset_candidate_subset
  learning:
    original_train_split: available
    evaluation_split_origin: dev
    train_eval_overlap_audit: not_audited
    leakage_note: do not train on this Nano split's conversations, table IDs, qrels,
      or target metadata records
    useful_training_data:
    - conversational search data
    - table retrieval pairs
    - government statistics search logs
    - bilingual English/French support conversations
    synthetic_data:
      document_generation: table metadata with title, dimensions, survey, frequency,
        subject, date range, and geography
      question_generation: partial support conversations asking for official statistics
      answerability: positive table should satisfy the user's measure, geography,
        sector, and time requirement
    multi_positive_training: multi_positive_objective
  links:
    nano_dataset: https://huggingface.co/datasets/hakari-bench/NanoMMTEB-v2
    source_urls:
    - label: StatCan Dialogue Dataset arXiv
      url: https://arxiv.org/abs/2304.01412
    - label: StatCan Dialogue Dataset project
      url: https://mcgill-nlp.github.io/statcan-dialogue-dataset/
    - label: mteb/StatcanDialogueDatasetRetrieval
      url: https://huggingface.co/datasets/mteb/StatcanDialogueDatasetRetrieval
    source_notes: []
  references:
  - title: A Dataset for Retrieving Data Tables through Conversations with Genuine
      Intents
    url: https://arxiv.org/abs/2304.01412
    year: 2023
    is_paper: true
    source_confidence: definitive_paper_link
  candidate_subsets:
    bm25:
      config: bm25
      label: BM25
      source: dataset_candidate_subset
      top_k: 500
      ndcg_at_10: 0.0111825673
      hit_at_10: 0.03
      recall_at_100: 0.1405750799
      candidate_count_min: 500
      candidate_count_max: 500
      candidate_count_mean: 500.0
      query_count: 200
      query_coverage: 1.0
      relevant_coverage_at_100: 0.1405750799
    dense:
      config: harrier_oss_v1_270m
      label: Dense
      source: dataset_candidate_subset
      top_k: 500
      ndcg_at_10: 0.2730851332
      hit_at_10: 0.455
      recall_at_100: 0.7220447284
      candidate_count_min: 500
      candidate_count_max: 500
      candidate_count_mean: 500.0
      query_count: 200
      query_coverage: 1.0
      relevant_coverage_at_100: 0.7220447284
    reranking_hybrid:
      config: reranking_hybrid
      label: Reranking hybrid
      source: dataset_candidate_subset
      top_k: 100
      ndcg_at_10: 0.1564489282
      hit_at_10: 0.34
      recall_at_100: 0.6581469649
      candidate_count_min: 100
      candidate_count_max: 101
      candidate_count_mean: 100.235
      query_count: 200
      query_coverage: 1.0
      relevant_coverage_at_100: 0.6581469649
      safeguard_positive_rows: 47
      rows_with_101_candidates: 47
```
