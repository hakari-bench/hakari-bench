# NanoBRIGHT / NanoBrightEconomics

## Overview

`NanoBrightEconomics` is the Economics StackExchange slice of BRIGHT. Queries
are user posts about economics, finance, markets, policy, and theory; relevant
documents are passages from web pages or papers cited by answers and validated
as useful evidence.

## Details

### What the Original Data Measures

[BRIGHT: A Realistic and Challenging Benchmark for Reasoning-Intensive Retrieval](https://arxiv.org/abs/2407.12883)
defines the StackExchange tasks by combining a post title and body into a query,
then collecting cited web pages from accepted or high-vote answers. The paper
emphasizes that positives are supporting documents, not necessarily direct
answer snippets, and that annotators add topically similar hard negatives so
retrievers cannot rely only on keyword overlap.

### Observed Data Profile

The split has 103 queries, 10,000 documents, and 800 positive qrels. Queries
average 739.57 characters and often include quoted claims, economic examples,
and requests for papers or explanations. Documents average 532.57 characters
and are passage chunks from articles, papers, reports, or reference pages.
Positives average 7.77 per query, but the distribution is uneven: the median is
3 and one query has 85 positives.

### BM25 Difficulty

Using the dataset-provided BM25 candidate column, BM25 reaches nDCG@10 =
0.2160 and hit@10 = 0.4466. It ranks 24 queries with a positive first, while
the median best positive rank is 23. The task is difficult because economic
questions often ask for conceptual support, models, or empirical evidence, and
the cited passage may use different vocabulary from the question.

### Training Data That May Help

Useful data includes non-overlapping Economics StackExchange posts with cited
sources, economics paper recommendation pairs, policy-report retrieval, and
finance or macroeconomics QA with explicit references. Avoid using the same
BRIGHT evaluation posts, cited documents, or qrels as training targets.

### Synthetic Data Guidance

Generate realistic economics questions with quoted claims, theoretical puzzles,
or policy scenarios, then pair them with source-style passages from papers,
reports, or textbooks. Hard negatives should be topically close but fail to
support the exact mechanism, model, or empirical claim requested by the query.

## Example Data

| Query | Positive document |
| --- | --- |
| Would a GDP measure be improved by excluding foreign interest paid? The income method of calculating GDP is as follows: GDP = wages + profits + rents + interest + depreciation + taxes + NFFI. If an economy has high external d ... [truncated 225 chars](684 chars) | So why in these two sets of countries do economic performance and well-being not go strictly hand in hand? One explanation is that the countries that do better in terms of well-being have made the choice of working less to ac ... [truncated 225 chars](1068 chars) |
| Derivative to ln(K(t)) in the RBC model In the calculation of the equation of motion for capital in the RBC model, I came across this equation: d ln K_(t+1) / d ln K_t = (d K_(t+1) / d K_t) * (K_t / K_(t+1)) Can someone expla ... [truncated 225 chars](406 chars) | Example [ [ edit ](/w/index.php?title=Elasticity_of_substitution&action=edit&section=3 "Edit section: Example") ] Consider [ Cobb–Douglas production function ](/wiki/Cobb%E2%80%93Douglas_production_function "Cobb–Douglas prod ... [truncated 225 chars](2640 chars) |
| What is the purpose of taxes if central banks can fund deficit spending? Somewhat straight forward. If the federal reserve can print money to buy treasuries to fund deficit spending, what is the purpose of taxes? Sure, taxes ... [truncated 225 chars](524 chars) | financial market innovations and shocks, may provide evidence of long-run inconsistencies between policies and targets and give rise to a reassessment of policy. IV CONCLUSIONS This paper has re-examined the correlations betw ... [truncated 225 chars](3286 chars) |
| Is it always a trade off between efficiency and equity? Is there any situations where we can achieve both equity and efficiency? I'm thinking of Covid 19 vaccine program which is run by Goverment. Although the cost for the pr ... [truncated 225 chars](467 chars) | What is the greatest single class of distortions in the global economy? One contender for this title is the tightly binding constraints on emigration from poor countries. Vast numbers of people in low-income countries want to ... [truncated 225 chars](821 chars) |
| How are stock prices determined in the following cases? I looked at this question already. I know there is an order book with bid and ask and that the price is updated when a match occurs. But I have two questions: What happe ... [truncated 225 chars](689 chars) | KEY TAKEAWAYS Matching orders is the process of identifying and effecting a trade between equal and opposite requests for a security (i.e., a buy and a sale at the same price). Order matching is how many exchanges pair buyers ... [truncated 225 chars](366 chars) |

## Dataset Information

| Field | Value |
| --- | --- |
| Nano set | NanoBRIGHT |
| Backing dataset | NanoBRIGHT |
| Task / split | NanoBrightEconomics |
| Source task | Economics StackExchange |
| Hugging Face dataset | [hakari-bench/NanoBRIGHT](https://huggingface.co/datasets/hakari-bench/NanoBRIGHT) |
| Source dataset | [xlangai/BRIGHT](https://huggingface.co/datasets/xlangai/BRIGHT) |
| Language | en |
| Category | natural_language |
| Queries | 103 |
| Documents | 10000 |
| Positive qrels | 800 |
| Positives per query | avg 7.77, min 1, median 3, max 85 |
| Multi-positive queries | 68 (66.02%) |
| BM25 nDCG@10 | 0.3029 |
| BM25 hit@10 | 0.5340 |
| BM25 Recall@100 | 0.4888 |
| BM25 candidate subset | top-500 (`bm25`) |
| Dense nDCG@10 | 0.4095 |
| Dense hit@10 | 0.6311 |
| Dense Recall@100 | 0.5950 |
| Dense candidate subset | top-500 (`harrier_oss_v1_270m`) |
| Reranking hybrid nDCG@10 | 0.3875 |
| Reranking hybrid hit@10 | 0.6408 |
| Reranking hybrid Recall@100 | 0.6262 |
| Reranking hybrid candidate subset | top-100 plus optional rank-101 safeguard (`reranking_hybrid`) |
| Reranking hybrid candidates / query | 100-101 |
| Reranking hybrid safeguard rows | 19 |
| Query length avg chars | 739.57 |
| Document length avg chars | 532.57 |

### Public Sources

- [BRIGHT: A Realistic and Challenging Benchmark for Reasoning-Intensive Retrieval](https://arxiv.org/abs/2407.12883).
- [BRIGHT project page](https://brightbenchmark.github.io/).
- [xlangai/BRIGHT](https://huggingface.co/datasets/xlangai/BRIGHT).

### Hugging Face Links

- Nano dataset: [hakari-bench/NanoBRIGHT](https://huggingface.co/datasets/hakari-bench/NanoBRIGHT)
- Source dataset: [xlangai/BRIGHT](https://huggingface.co/datasets/xlangai/BRIGHT)
- MTEB dataset record: [mteb/BRIGHT](https://huggingface.co/datasets/mteb/BRIGHT)

### Source Reference Table

| Title | Year | Type | URL |
| --- | ---: | --- | --- |
| BRIGHT: A Realistic and Challenging Benchmark for Reasoning-Intensive Retrieval | 2024 | benchmark paper | https://arxiv.org/abs/2407.12883 |
| BRIGHT project page | 2024 | project page | https://brightbenchmark.github.io/ |
| xlangai/BRIGHT | 2024 | dataset card | https://huggingface.co/datasets/xlangai/BRIGHT |

## Machine-Readable Metadata

<!-- benchmark-task-metadata:v1 -->

```yaml
benchmark_task_metadata:
  schema_version: 1
  document_status: first_pass
  nano_set: NanoBRIGHT
  backing_dataset: NanoBRIGHT
  dataset_id: hakari-bench/NanoBRIGHT
  task_name: NanoBrightEconomics
  split_name: NanoBrightEconomics
  source_task: Economics StackExchange
  source_dataset_id: xlangai/BRIGHT
  language: en
  category: natural_language
  document_path: docs/benchmark_tasks/NanoBRIGHT/NanoBrightEconomics.md
  source_research:
    primary_source_type: benchmark_paper
    paper_pdf_or_html_checked: true
    no_paper_note: null
  counts:
    queries: 103
    documents: 10000
    positive_qrels: 800
  positives_per_query:
    average: 7.766990291262136
    min: 1
    median: 3
    max: 85
    multi_positive_queries: 68
    multi_positive_query_percent: 66.01941747572816
  text_stats_chars:
    query_mean: 739.5728155339806
    document_mean: 532.5738
  bm25:
    ndcg_at_10: 0.3028895430244026
    hit_at_10: 0.5339805825242718
    source: dataset_candidate_subset
  learning:
    original_train_split: unknown
    evaluation_split_origin: BRIGHT Economics StackExchange evaluation split
    train_eval_overlap_audit: not_audited
    leakage_note: exclude NanoBRIGHT Economics queries, cited positives, and linked
      answer pages
    useful_training_data:
    - non-overlapping Economics StackExchange posts with cited sources
    - economics paper recommendation pairs
    - policy-report and finance QA retrieval data
    synthetic_data:
      document_generation: economics papers, reports, reference passages, or textbook
        explanations
      question_generation: economics questions with quoted claims, models, or policy
        scenarios
      answerability: positives should support the exact economic mechanism or empirical
        claim
    multi_positive_training: multi_positive_objective
  links:
    nano_dataset: https://huggingface.co/datasets/hakari-bench/NanoBRIGHT
    source_urls:
    - label: BRIGHT arXiv
      url: https://arxiv.org/abs/2407.12883
    - label: BRIGHT project
      url: https://brightbenchmark.github.io/
    - label: xlangai/BRIGHT
      url: https://huggingface.co/datasets/xlangai/BRIGHT
    source_notes: []
  references:
  - title: 'BRIGHT: A Realistic and Challenging Benchmark for Reasoning-Intensive
      Retrieval'
    url: https://arxiv.org/abs/2407.12883
    year: 2024
    doi: 10.48550/arXiv.2407.12883
    is_paper: true
    source_confidence: definitive_paper_link
  candidate_subsets:
    bm25:
      config: bm25
      label: BM25
      source: dataset_candidate_subset
      top_k: 500
      ndcg_at_10: 0.302889543
      hit_at_10: 0.5339805825
      recall_at_100: 0.48875
      candidate_count_min: 500
      candidate_count_max: 500
      candidate_count_mean: 500.0
      query_count: 103
      query_coverage: 1.0
      relevant_coverage_at_100: 0.48875
    dense:
      config: harrier_oss_v1_270m
      label: Dense
      source: dataset_candidate_subset
      top_k: 500
      ndcg_at_10: 0.4095366877
      hit_at_10: 0.6310679612
      recall_at_100: 0.595
      candidate_count_min: 500
      candidate_count_max: 500
      candidate_count_mean: 500.0
      query_count: 103
      query_coverage: 1.0
      relevant_coverage_at_100: 0.595
    reranking_hybrid:
      config: reranking_hybrid
      label: Reranking hybrid
      source: dataset_candidate_subset
      top_k: 100
      ndcg_at_10: 0.3875496618
      hit_at_10: 0.640776699
      recall_at_100: 0.62625
      candidate_count_min: 100
      candidate_count_max: 101
      candidate_count_mean: 100.184466
      query_count: 103
      query_coverage: 1.0
      relevant_coverage_at_100: 0.62625
      safeguard_positive_rows: 19
      rows_with_101_candidates: 19
```
