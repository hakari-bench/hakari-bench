# NanoCoIR / NanoSyntheticText2SQL

## Overview

CoIR adapts Gretel's Synthetic Text-to-SQL data from generation into retrieval:
a natural-language analytics or database-management request must retrieve the
corresponding SQL statement. Because the source data includes schema-oriented
business prompts, SQL complexity labels, and varied operations, this split tests
whether retrievers can align intent with joins, aggregations, window functions,
and data modification statements rather than only matching table words.

## Details

### What the Original Data Measures

[CoIR](https://arxiv.org/abs/2407.02883) adapts Gretel's Synthetic Text-to-SQL
dataset as a text-to-code retrieval task: the natural-language SQL prompt is the
query and the SQL query is the document to retrieve. The [Gretel dataset card](https://huggingface.co/datasets/gretelai/synthetic_text_to_sql)
describes a large Apache-2.0 synthetic Text-to-SQL dataset with domains,
schema context, SQL complexity labels, prompts, SQL, and explanations.

### Observed Data Profile

The Nano split has 200 queries, 10,000 documents, and 200 positive qrels. Each
query has one positive. Queries average 102.94 characters and are business or
analytics requests. SQL documents average 130.60 characters and include
aggregation, joins, window functions, inserts, deletes, and updates.

### BM25 Difficulty

Using the dataset-provided BM25 candidate column, BM25 reaches nDCG@10 =
0.5918 and hit@10 = 0.6950. It ranks 100 positives first and 139 in the top 10.
Lexical matching helps with table and domain words, but schema-free prompts can
be broad while SQL documents contain compact identifiers and operations.

### Training Data That May Help

Text-to-SQL prompt/query pairs, SQL schema linking data, synthetic SQL
generation corpora, and hard negatives sharing domains or table names should
help.

### Synthetic Data Guidance

Synthetic data should include varied domains, SQL task types, and complexity
levels. Pair each natural-language prompt with executable SQL, and create hard
negatives that use the same tables but answer a different analytical question.

### Benchmark Information Leakage

CoIR adapts Gretel's Synthetic Text-to-SQL data with roughly 100k train queries
and 6k test queries over a 106k-document corpus. This Nano split is derived from
the CoIR Synthetic Text-to-SQL test side. Training on the public Gretel test
split, or on an unfiltered export that mixes train and test rows, can leak the
evaluation natural-language prompts and SQL documents.

The safer training source is the Gretel train split only, followed by normalized
prompt, SQL, schema-context, and token-fingerprint exclusion against
NanoSyntheticText2SQL. Models trained on unfiltered test-derived prompt-SQL
pairs may report high scores by memorizing exact SQL statements rather than
learning schema-aware retrieval.

## Example Data

| Query | Positive document |
| --- | --- |
| What is the difference in average permit cost between high-rise and low-rise buildings in British Columbia in 2021? (115 chars) | SELECT AVG(permit_cost) - LAG(AVG(permit_cost)) OVER (PARTITION BY province ORDER BY EXTRACT(YEAR FROM issue_date)) FROM permit_cost_comparison WHERE province = 'British Columbia' AND building_type IN ('High-rise', 'Low-rise' ... [truncated 225 chars](280 chars) |
| What is the total amount of aid provided by each government, for community development projects in Southeast Asia, in the last 10 years, and the average duration of the projects? (178 chars) | SELECT government.name as government, SUM(aid) as total_aid, AVG(DATEDIFF(end_date, start_date) / 365) as avg_project_duration FROM community_development_projects JOIN government ON community_development_projects.government_i ... [truncated 225 chars](412 chars) |
| Find the difference in the number of trees between the tree species with the highest and lowest carbon sequestration rates in the private_lands schema. (151 chars) | SELECT species_high.species AS high_species, species_low.species AS low_species, species_high.sequestration_rate - species_low.sequestration_rate AS difference FROM (SELECT species, MAX(sequestration_rate) AS sequestration_ra ... [truncated 225 chars](522 chars) |
| Which cities have had a female mayor for the longest continuous period? (71 chars) | SELECT c.name, MAX(m.end_year - m.start_year) as max_tenure FROM city c JOIN mayor m ON c.id = m.city_id WHERE m.gender = 'Female' GROUP BY c.name HAVING MAX(m.end_year - m.start_year) >= ALL (SELECT MAX(m2.end_year - m2.star ... [truncated 225 chars](274 chars) |
| Which ingredients are used in products that have received a safety violation in the past year and are not cruelty-free certified? (129 chars) | SELECT ingredient_sources.ingredient_id FROM ingredient_sources INNER JOIN products ON ingredient_sources.product_id = products.product_id INNER JOIN safety_records ON products.product_id = safety_records.product_id WHERE saf ... [truncated 225 chars](318 chars) |

## Dataset Information

| Field | Value |
| --- | --- |
| Nano set | NanoCoIR |
| Backing dataset | NanoCoIR |
| Task / split | NanoSyntheticText2SQL |
| Hugging Face dataset | [hakari-bench/NanoCoIR](https://huggingface.co/datasets/hakari-bench/NanoCoIR) |
| Language | en |
| Category | code |
| Queries | 200 |
| Documents | 10000 |
| Positive qrels | 200 |
| BM25 nDCG@10 | 0.2240 |
| BM25 hit@10 | 0.3100 |
| BM25 Recall@100 | 0.6900 |
| BM25 candidate subset | top-500 (`bm25`) |
| Dense nDCG@10 | 0.9567 |
| Dense hit@10 | 0.9800 |
| Dense Recall@100 | 0.9800 |
| Dense candidate subset | top-500 (`harrier_oss_v1_270m`) |
| Reranking hybrid nDCG@10 | 0.5577 |
| Reranking hybrid hit@10 | 0.7350 |
| Reranking hybrid Recall@100 | 0.9850 |
| Reranking hybrid candidate subset | top-100 plus optional rank-101 safeguard (`reranking_hybrid`) |
| Reranking hybrid candidates / query | 100-101 |
| Reranking hybrid safeguard rows | 3 |
| Query length avg chars | 102.94 |
| Document length avg chars | 130.60 |

### Public Sources

- [CoIR](https://arxiv.org/abs/2407.02883); 2025; Xiangyang Li et al.
- [gretelai/synthetic_text_to_sql](https://huggingface.co/datasets/gretelai/synthetic_text_to_sql).

### Hugging Face Links

- Nano dataset: [hakari-bench/NanoCoIR](https://huggingface.co/datasets/hakari-bench/NanoCoIR)
- Source dataset: [gretelai/synthetic_text_to_sql](https://huggingface.co/datasets/gretelai/synthetic_text_to_sql)

### Source Reference Table

| Title | Year | Type | URL |
| --- | ---: | --- | --- |
| CoIR: A Comprehensive Benchmark for Code Information Retrieval Models | 2025 | benchmark paper | https://arxiv.org/abs/2407.02883 |
| Synthetic-Text-To-SQL | 2024 | dataset card | https://huggingface.co/datasets/gretelai/synthetic_text_to_sql |

## Machine-Readable Metadata

<!-- benchmark-task-metadata:v1 -->

```yaml
benchmark_task_metadata:
  schema_version: 1
  document_status: first_pass
  nano_set: NanoCoIR
  backing_dataset: NanoCoIR
  dataset_id: hakari-bench/NanoCoIR
  task_name: NanoSyntheticText2SQL
  split_name: NanoSyntheticText2SQL
  language: en
  category: code
  document_path: docs/benchmark_tasks/NanoCoIR/NanoSyntheticText2SQL.md
  source_research:
    primary_source_type: benchmark_paper_and_dataset_card
    paper_pdf_or_html_checked: true
    no_paper_note: no standalone task paper confirmed beyond the dataset card and
      CoIR construction notes
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
    query_mean: 102.935
    document_mean: 130.6048
  bm25:
    ndcg_at_10: 0.22401324602456768
    hit_at_10: 0.31
    source: dataset_candidate_subset
  learning:
    original_train_split: available
    evaluation_split_origin: CoIR Synthetic Text-to-SQL test-derived retrieval split
    train_eval_overlap_audit: not_audited_split_filtering_required
    leakage_note: exclude NanoSyntheticText2SQL prompt-SQL pairs; do not train on
      Gretel or CoIR Text-to-SQL test-derived rows
    leakage_risk:
      source_dataset: gretelai/synthetic_text_to_sql
      source_train_queries_reported_by_coir: 100000
      source_test_queries_reported_by_coir: 6000
      risk: upstream Text-to-SQL test examples can overlap with NanoSyntheticText2SQL
        evaluation rows
      recommended_filter: train split only plus normalized prompt, SQL, schema-context,
        and token-fingerprint exclusion
    useful_training_data:
    - text-to-SQL prompt and query pairs
    - schema-linking retrieval data
    - domain-sharing SQL hard negatives
    synthetic_data:
      document_generation: SQL queries across varied task types
      question_generation: natural-language analytics and database prompts
      answerability: positive SQL must answer the prompt
    multi_positive_training: single_positive
  links:
    nano_dataset: https://huggingface.co/datasets/hakari-bench/NanoCoIR
    source_urls:
    - label: CoIR arXiv
      url: https://arxiv.org/abs/2407.02883
    - label: gretelai/synthetic_text_to_sql
      url: https://huggingface.co/datasets/gretelai/synthetic_text_to_sql
    source_notes: []
  references:
  - title: 'CoIR: A Comprehensive Benchmark for Code Information Retrieval Models'
    url: https://arxiv.org/abs/2407.02883
    year: 2025
    is_paper: true
    source_confidence: definitive_paper_link
  candidate_subsets:
    bm25:
      config: bm25
      label: BM25
      source: dataset_candidate_subset
      top_k: 500
      ndcg_at_10: 0.224013246
      hit_at_10: 0.31
      recall_at_100: 0.69
      candidate_count_min: 500
      candidate_count_max: 500
      candidate_count_mean: 500.0
      query_count: 200
      query_coverage: 1.0
      relevant_coverage_at_100: 0.69
    dense:
      config: harrier_oss_v1_270m
      label: Dense
      source: dataset_candidate_subset
      top_k: 500
      ndcg_at_10: 0.9567126579
      hit_at_10: 0.98
      recall_at_100: 0.98
      candidate_count_min: 500
      candidate_count_max: 500
      candidate_count_mean: 500.0
      query_count: 200
      query_coverage: 1.0
      relevant_coverage_at_100: 0.98
    reranking_hybrid:
      config: reranking_hybrid
      label: Reranking hybrid
      source: dataset_candidate_subset
      top_k: 100
      ndcg_at_10: 0.5577138637
      hit_at_10: 0.735
      recall_at_100: 0.985
      candidate_count_min: 100
      candidate_count_max: 101
      candidate_count_mean: 100.015
      query_count: 200
      query_coverage: 1.0
      relevant_coverage_at_100: 0.985
      safeguard_positive_rows: 3
      rows_with_101_candidates: 3
```
