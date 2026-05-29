# NanoMMTEB-v2 / legal_bench_corporate_lobbying

## Overview

`legal_bench_corporate_lobbying` is an English legal-policy retrieval task from
LegalBench. Queries are bill titles or short bill descriptions, and documents
are bill records. The task tests whether a retriever can connect policy intent
to the matching legislative summary.

## Details

### What the Original Data Measures

[LEGALBENCH: A Collaboratively Built Benchmark](https://proceedings.neurips.cc/paper_files/paper/2023/file/89e44582fd28ddfea1ea4dcb0ebbf4b0-Paper-Datasets_and_Benchmarks.pdf)
describes `corporate_lobbying` as an issue-spotting style task in which a model
must determine whether a proposed Congressional bill may implicate company or
issue interests. The MTEB retrieval version turns this into matching bill titles
and summaries to the corresponding bill text.

### Observed Data Profile

The Nano split has 200 queries, 319 documents, and 200 positive qrels. Each
query has one positive. Queries average 179.67 characters and usually describe a
bill objective. Documents average 1,157.21 characters and contain bill names
plus structured legislative summaries.

### BM25 Difficulty

Using the dataset-provided BM25 candidate column, BM25 reaches nDCG@10 = 0.8993
and hit@10 = 0.9800. Lexical matching is strong because titles and summaries
often reuse bill-specific terms, but the task still includes broader policy
paraphrases such as health-care stabilization, firearms regulation, or internet
openness.

### Training Data That May Help

Useful training data includes legislative title-to-summary retrieval, bill
classification, legal issue spotting, policy-domain search logs, and hard
negatives from bills in the same policy area. Avoid evaluation bill summaries
and qrels when building supervised training data.

### Synthetic Data Guidance

Generate bill titles, short objectives, and legislative summaries with realistic
policy scope, agencies, affected actors, and exceptions. Pair each query with the
matching bill record and include same-domain bills that differ in remedy, agency,
or regulated activity as negatives.

## Example Data

| Query | Positive document |
| --- | --- |
| To require the President to develop a strategy to ensure the security of next generation mobile telecommunications systems and infrastructure in the United States and to assist allies and strategic partners in maximizing the ... [truncated 225 chars](341 chars) | Secure 5G and Beyond Act of 2020 This bill requires the President, in consultation with relevant federal agencies, to develop (1) a strategy to secure and protect U.S. fifth and future generations (5G) systems and infrastruct ... [truncated 225 chars](685 chars) |
| To establish a business incubators program within the Department of the Interior to promote economic development in Indian reservation communities. (147 chars) | Native American Business Incubators Program Act This bill requires the Department of the Interior to establish a grant program in the Office of Indian Energy and Economic Development for establishing and operating business in ... [truncated 225 chars](826 chars) |
| To amend the Internal Revenue Code of 1986 to provide a safe harbor for determinations of worker classification, to require increased reporting, and for other purposes. (168 chars) | New Economy Works to Guarantee Independence and Growth Act of 2019 or the NEW GIG Act of 2019 This bill establishes a test for determining if a service provider should be classified as an independent contractor rather than as ... [truncated 225 chars](1572 chars) |
| To make improvements to certain defense and security assistance provisions and to authorize theappropriation of funds to Israel, to reauthorize the United States-Jordan Defense Cooperation Act of 2015, and to halt the wholesa ... [truncated 225 chars](283 chars) | Strengthening America's Security in the Middle East Act of 2019 This bill authorizes assistance and weapons transfers to Israel, and extends defense cooperation with Jordan. It establishes additional sanctions related to the ... [truncated 225 chars](1724 chars) |
| To support carbon dioxide utilization and direct air capture research, to facilitate the permitting and development of carbon capture, utilization, and sequestration projects and carbon dioxide pipelines, and for other purpos ... [truncated 225 chars](228 chars) | Utilizing Significant Emissions with Innovative Technologies Act or the USE IT Act This bill addresses the capture, utilization, and sequestration of carbon dioxide. The Environmental Protection Agency must (1) establish a co ... [truncated 225 chars](1562 chars) |

## Dataset Information

| Field | Value |
| --- | --- |
| Nano set | NanoMMTEB-v2 |
| Backing dataset | NanoMMTEB-v2 |
| Task / split | legal_bench_corporate_lobbying |
| Hugging Face dataset | [hakari-bench/NanoMMTEB-v2](https://huggingface.co/datasets/hakari-bench/NanoMMTEB-v2) |
| Source dataset | [mteb/legalbench_corporate_lobbying](https://huggingface.co/datasets/mteb/legalbench_corporate_lobbying) |
| Language | en |
| Category | natural_language |
| Queries | 200 |
| Documents | 319 |
| Positive qrels | 200 |
| BM25 nDCG@10 | 0.8955 |
| BM25 hit@10 | 0.9800 |
| BM25 Recall@100 | 1.0000 |
| BM25 candidate subset | top-500 (`bm25`) |
| Dense nDCG@10 | 0.9110 |
| Dense hit@10 | 0.9700 |
| Dense Recall@100 | 0.9800 |
| Dense candidate subset | top-500 (`harrier_oss_v1_270m`) |
| Reranking hybrid nDCG@10 | 0.9080 |
| Reranking hybrid hit@10 | 0.9700 |
| Reranking hybrid Recall@100 | 1.0000 |
| Reranking hybrid candidate subset | top-100 plus optional rank-101 safeguard (`reranking_hybrid`) |
| Reranking hybrid candidates / query | 100 |
| Reranking hybrid safeguard rows | 0 |
| Query length avg chars | 179.67 |
| Document length avg chars | 1157.21 |

### Public Sources

- [LEGALBENCH: A Collaboratively Built Benchmark](https://proceedings.neurips.cc/paper_files/paper/2023/file/89e44582fd28ddfea1ea4dcb0ebbf4b0-Paper-Datasets_and_Benchmarks.pdf).
- [LegalBench corporate_lobbying task page](https://hazyresearch.stanford.edu/legalbench/tasks/corporate_lobbying.html).
- [mteb/legalbench_corporate_lobbying](https://huggingface.co/datasets/mteb/legalbench_corporate_lobbying).

### Hugging Face Links

- Nano dataset: [hakari-bench/NanoMMTEB-v2](https://huggingface.co/datasets/hakari-bench/NanoMMTEB-v2)
- Source dataset: [mteb/legalbench_corporate_lobbying](https://huggingface.co/datasets/mteb/legalbench_corporate_lobbying)

### Source Reference Table

| Title | Year | Type | URL |
| --- | ---: | --- | --- |
| LEGALBENCH: A Collaboratively Built Benchmark | 2023 | benchmark paper | https://proceedings.neurips.cc/paper_files/paper/2023/file/89e44582fd28ddfea1ea4dcb0ebbf4b0-Paper-Datasets_and_Benchmarks.pdf |
| LegalBench corporate_lobbying task page | 2023 | task page | https://hazyresearch.stanford.edu/legalbench/tasks/corporate_lobbying.html |
| mteb/legalbench_corporate_lobbying | 2024 | dataset card | https://huggingface.co/datasets/mteb/legalbench_corporate_lobbying |

## Machine-Readable Metadata

<!-- benchmark-task-metadata:v1 -->

```yaml
benchmark_task_metadata:
  schema_version: 1
  document_status: first_pass
  nano_set: NanoMMTEB-v2
  backing_dataset: NanoMMTEB-v2
  dataset_id: hakari-bench/NanoMMTEB-v2
  task_name: legal_bench_corporate_lobbying
  split_name: legal_bench_corporate_lobbying
  language: en
  category: natural_language
  document_path: docs/benchmark_tasks/NanoMMTEB-v2/legal_bench_corporate_lobbying.md
  source_research:
    primary_source_type: benchmark_paper
    paper_pdf_or_html_checked: true
    no_paper_note: No standalone retrieval paper was confirmed; LegalBench benchmark
      paper and task page were checked.
  counts:
    queries: 200
    documents: 319
    positive_qrels: 200
  positives_per_query:
    average: 1.0
    min: 1
    median: 1.0
    max: 1
    multi_positive_queries: 0
    multi_positive_query_percent: 0.0
  text_stats_chars:
    query_mean: 179.67
    document_mean: 1157.2131661442006
  bm25:
    ndcg_at_10: 0.8955364489395502
    hit_at_10: 0.98
    source: dataset_candidate_subset
  learning:
    original_train_split: available
    evaluation_split_origin: test
    train_eval_overlap_audit: not_audited
    leakage_note: do not train on this Nano split's bill queries, qrels, or positive
      bill summaries
    useful_training_data:
    - legislative title-to-summary retrieval
    - bill classification and policy issue spotting data
    - same-policy-area bill hard negatives
    - legal and regulatory document search data
    synthetic_data:
      document_generation: realistic congressional bill titles and structured summaries
      question_generation: bill objectives or short policy descriptions
      answerability: positive bill record should implement the described policy objective
    multi_positive_training: single_positive_question_document_focus
  links:
    nano_dataset: https://huggingface.co/datasets/hakari-bench/NanoMMTEB-v2
    source_urls:
    - label: LegalBench paper
      url: https://proceedings.neurips.cc/paper_files/paper/2023/file/89e44582fd28ddfea1ea4dcb0ebbf4b0-Paper-Datasets_and_Benchmarks.pdf
    - label: LegalBench corporate_lobbying
      url: https://hazyresearch.stanford.edu/legalbench/tasks/corporate_lobbying.html
    - label: mteb/legalbench_corporate_lobbying
      url: https://huggingface.co/datasets/mteb/legalbench_corporate_lobbying
    source_notes: []
  references:
  - title: 'LEGALBENCH: A Collaboratively Built Benchmark'
    url: https://proceedings.neurips.cc/paper_files/paper/2023/file/89e44582fd28ddfea1ea4dcb0ebbf4b0-Paper-Datasets_and_Benchmarks.pdf
    year: 2023
    is_paper: true
    source_confidence: definitive_paper_link
  candidate_subsets:
    bm25:
      config: bm25
      label: BM25
      source: dataset_candidate_subset
      top_k: 500
      ndcg_at_10: 0.8955364489
      hit_at_10: 0.98
      recall_at_100: 1.0
      candidate_count_min: 319
      candidate_count_max: 319
      candidate_count_mean: 319.0
      query_count: 200
      query_coverage: 1.0
      relevant_coverage_at_100: 1.0
    dense:
      config: harrier_oss_v1_270m
      label: Dense
      source: dataset_candidate_subset
      top_k: 500
      ndcg_at_10: 0.9110210433
      hit_at_10: 0.97
      recall_at_100: 0.98
      candidate_count_min: 319
      candidate_count_max: 319
      candidate_count_mean: 319.0
      query_count: 200
      query_coverage: 1.0
      relevant_coverage_at_100: 0.98
    reranking_hybrid:
      config: reranking_hybrid
      label: Reranking hybrid
      source: dataset_candidate_subset
      top_k: 100
      ndcg_at_10: 0.9080311234
      hit_at_10: 0.97
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
