# NanoIFIR / NanoIFIRFiQA

## Overview

`NanoIFIRFiQA` is an instruction-following personal-finance retrieval task.
Queries are English financial questions, and documents are answer posts or
advice passages. The retriever must find financial suggestions that match the
user's question and, in IFIR, the user-specific instruction context.

## Details

### What the Original Data Measures

[IFIR](https://arxiv.org/abs/2503.04644) uses FiQA for the finance domain,
simulating users seeking guidance for informed financial decisions. The paper
adds three instruction-complexity levels: a basic request for a financial
suggestion, extra personal information such as age or financial status, and
specific financial goals.

[WWW'18 Open Challenge: Financial Opinion Mining and Question Answering](https://doi.org/10.1145/3184558.3192301)
introduced FiQA tasks for financial sentiment and opinion-based QA. The QA task
asks systems to answer natural-language financial questions by ranking relevant
financial posts; the paper reports a knowledge base of 57,640 answer posts.

### Observed Data Profile

The Nano split has 200 queries, 10,000 documents, and 1,010 positive qrels.
Every query has multiple positives, with a median of 4 and maximum of 23.
Queries average 65.79 characters, and documents average 788.42 characters.
Observed questions cover credit cards, business structure, taxes, loans,
budgeting, gifts, debt, and investment choices.

Documents are informal but domain-specific advice posts. They often contain
qualifiers and practical caveats rather than a single canonical answer.

### BM25 Difficulty

Using the dataset-provided BM25 candidate column, BM25 reaches nDCG@10 =
0.2252 and hit@10 = 0.6100. BM25 ranks a positive first for 50 queries. Lexical
matching helps when the question and advice share finance terms, but many
answers are semantically relevant without repeating the exact wording.

### Training Data That May Help

Useful training data includes non-overlapping FiQA question-document pairs,
personal finance forum QA, financial advice retrieval, and hard negatives about
the same product or tax topic. Training should preserve multiple relevant
answers per query.

### Synthetic Data Guidance

Generate personal-finance questions with user context, goals, and constraints.
Positive documents should offer practical advice with caveats. Hard negatives
should use the same financial product or tax term but answer a different
decision problem.

## Example Data

| Query | Positive document |
| --- | --- |
| Dividend vs Growth Stocks for young investors (45 chars) | "The key is to look at total return, that is dividend yields plus capital growth. Some stocks have yields of 5%-7%, and no growth. In that case, you get the dividends, and not a whole lot more. These are called dividend stock ... [truncated 225 chars](589 chars) |
| What purchases, not counting real estate, will help me increase my cash flow? (77 chars) | You can increase your monthly cash flow in two ways: It's really that simple. I'd even argue that to a certain extent, decreasing expenses can be more cash-positive than increasing income by the same amount if you're spending ... [truncated 225 chars](883 chars) |
| What are the contents of fixed annuities? (41 chars) | "An annuity is a contract. Its contents are ""a contractual obligation from the issuing company"". If you want to evaluate how your annuity is likely to fare, you're essentially asking whether or not its issuer will honor its ... [truncated 225 chars](2509 chars) |
| Full-time work + running small side business: Best business structure for taxes? (80 chars) | You should look into an LLC. Its a fairly simple process, and the income simply flows through to your individual return. It will allow you to deduct supplies and other expenses from that income. It should also protect you if ... [truncated 225 chars](603 chars) |
| Why don't banks give access to all your transaction activity? (61 chars) | "Things are the way they are because they got that way. - Gerald Weinberg Banks have been in business for a very long time. Yet, much of what we take for granted in terms of technology (capabilities, capacity, and cost) are r ... [truncated 225 chars](1103 chars) |

## Dataset Information

| Field | Value |
| --- | --- |
| Nano set | NanoIFIR |
| Backing dataset | NanoIFIR |
| Task / split | NanoIFIRFiQA |
| Hugging Face dataset | [hakari-bench/NanoIFIR](https://huggingface.co/datasets/hakari-bench/NanoIFIR) |
| Language | en |
| Category | natural_language |
| Queries | 200 |
| Documents | 10,000 |
| Positive qrels | 1,010 |
| Positives per query | avg 5.05 / min 3 / median 4.0 / max 23 |
| Multi-positive queries | 200 (100.00%) |
| BM25 nDCG@10 | 0.3422 |
| BM25 hit@10 | 0.7650 |
| BM25 Recall@100 | 0.5802 |
| BM25 candidate subset | top-500 (`bm25`) |
| Dense nDCG@10 | 0.5328 |
| Dense hit@10 | 0.8750 |
| Dense Recall@100 | 0.7614 |
| Dense candidate subset | top-500 (`harrier_oss_v1_270m`) |
| Reranking hybrid nDCG@10 | 0.4678 |
| Reranking hybrid hit@10 | 0.8750 |
| Reranking hybrid Recall@100 | 0.7455 |
| Reranking hybrid candidate subset | top-100 plus optional rank-101 safeguard (`reranking_hybrid`) |
| Reranking hybrid candidates / query | 100-101 |
| Reranking hybrid safeguard rows | 3 |
| Query length avg chars | 65.79 |
| Document length avg chars | 788.42 |

### Public Sources

- [IFIR: A Comprehensive Benchmark for Evaluating Instruction-Following in Expert-Domain Information Retrieval](https://arxiv.org/abs/2503.04644); 2025; Tingyu Song et al.
- [WWW'18 Open Challenge: Financial Opinion Mining and Question Answering](https://doi.org/10.1145/3184558.3192301); 2018; Macedo Maia et al.

### Hugging Face Links

- Nano dataset: [hakari-bench/NanoIFIR](https://huggingface.co/datasets/hakari-bench/NanoIFIR)

### Source Reference Table

| Title | Year | Type | URL |
| --- | ---: | --- | --- |
| IFIR: A Comprehensive Benchmark for Evaluating Instruction-Following in Expert-Domain Information Retrieval | 2025 | arXiv paper | https://arxiv.org/abs/2503.04644 |
| WWW'18 Open Challenge: Financial Opinion Mining and Question Answering | 2018 | ACM paper | https://doi.org/10.1145/3184558.3192301 |

## Machine-Readable Metadata

<!-- benchmark-task-metadata:v1 -->

```yaml
benchmark_task_metadata:
  schema_version: 1
  document_status: first_pass
  nano_set: NanoIFIR
  backing_dataset: NanoIFIR
  dataset_id: hakari-bench/NanoIFIR
  task_name: NanoIFIRFiQA
  split_name: NanoIFIRFiQA
  language: en
  category: natural_language
  document_path: docs/benchmark_tasks/NanoIFIR/NanoIFIRFiQA.md
  source_research:
    primary_source_type: benchmark_paper_and_task_paper
    paper_pdf_or_html_checked: true
    no_paper_note: null
  counts:
    queries: 200
    documents: 10000
    positive_qrels: 1010
  positives_per_query:
    average: 5.05
    min: 3
    median: 4.0
    max: 23
    multi_positive_queries: 200
    multi_positive_query_percent: 100.0
  text_stats_chars:
    query_mean: 65.79
    document_mean: 788.4161
  bm25:
    ndcg_at_10: 0.34221328710644366
    hit_at_10: 0.765
    source: dataset_candidate_subset
  learning:
    original_train_split: available
    evaluation_split_origin: ifir_adapted
    train_eval_overlap_audit: not_audited
    leakage_note: exclude NanoIFIRFiQA queries, qrels, and positive financial answer
      posts
    useful_training_data:
    - non-overlapping FiQA question-document pairs
    - personal finance forum QA
    - financial advice retrieval pairs
    - same-topic financial hard negatives
    synthetic_data:
      document_generation: practical personal-finance advice posts with caveats and
        decision factors
      question_generation: user-specific financial questions with goals, constraints,
        and product context
      answerability: positives should address the financial decision or advice need
        in the query
    multi_positive_training: preserve_multiple_useful_financial_answers
  links:
    nano_dataset: https://huggingface.co/datasets/hakari-bench/NanoIFIR
    source_urls:
    - label: IFIR arXiv
      url: https://arxiv.org/abs/2503.04644
    - label: FiQA DOI
      url: https://doi.org/10.1145/3184558.3192301
    source_notes: []
  references:
  - title: 'WWW''18 Open Challenge: Financial Opinion Mining and Question Answering'
    url: https://doi.org/10.1145/3184558.3192301
    year: 2018
    doi: 10.1145/3184558.3192301
    is_paper: true
    source_confidence: definitive_paper_link
  candidate_subsets:
    bm25:
      config: bm25
      label: BM25
      source: dataset_candidate_subset
      top_k: 500
      ndcg_at_10: 0.3422132871
      hit_at_10: 0.765
      recall_at_100: 0.5801980198
      candidate_count_min: 500
      candidate_count_max: 500
      candidate_count_mean: 500.0
      query_count: 200
      query_coverage: 1.0
      relevant_coverage_at_100: 0.5801980198
    dense:
      config: harrier_oss_v1_270m
      label: Dense
      source: dataset_candidate_subset
      top_k: 500
      ndcg_at_10: 0.5328158992
      hit_at_10: 0.875
      recall_at_100: 0.7613861386
      candidate_count_min: 500
      candidate_count_max: 500
      candidate_count_mean: 500.0
      query_count: 200
      query_coverage: 1.0
      relevant_coverage_at_100: 0.7613861386
    reranking_hybrid:
      config: reranking_hybrid
      label: Reranking hybrid
      source: dataset_candidate_subset
      top_k: 100
      ndcg_at_10: 0.4677708963
      hit_at_10: 0.875
      recall_at_100: 0.7455445545
      candidate_count_min: 100
      candidate_count_max: 101
      candidate_count_mean: 100.015
      query_count: 200
      query_coverage: 1.0
      relevant_coverage_at_100: 0.7455445545
      safeguard_positive_rows: 3
      rows_with_101_candidates: 3
```
