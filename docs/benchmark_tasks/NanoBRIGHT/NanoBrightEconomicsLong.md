# NanoBRIGHT / NanoBrightEconomicsLong

## Overview

`NanoBrightEconomicsLong` is the long-document version of the Economics
StackExchange BRIGHT task. Queries are long economics or finance posts, and the
retrieval pool contains full cited source pages rather than passage chunks.

## Details

### What the Original Data Measures

[BRIGHT](https://arxiv.org/abs/2407.12883) converts StackExchange tasks to
long-context retrieval by using complete web pages with far fewer documents.
The paper notes that these long-document variants are intended to stress
retrieval over lengthy sources where evidence can be buried among navigation,
citations, tables, and unrelated sections.

### Observed Data Profile

The split has 103 queries, 515 documents, and 109 positive qrels. Queries
average 739.57 characters, matching the short Economics split. Documents average
38,615.97 characters and include full papers, reference pages, PMC articles,
Wikipedia pages, and long technical pages. Most queries have one positive in
this long-document version; only 5 queries have multiple positives.

### BM25 Difficulty

Using the dataset-provided BM25 candidate column, BM25 reaches nDCG@10 =
0.2510 and hit@10 = 0.3592. It ranks 18 queries with a positive first, and the
median best positive rank is 19. The full pages contain much more noise than
the passage version, so keyword overlap with a cited paper title or economics
term does not reliably place the right document in the top ranks.

### Training Data That May Help

Useful data includes long economics reports aligned to questions, document-level
paper recommendation data, cited-source retrieval from economics forums, and
passage-to-full-document distillation. Do not train on the same evaluation posts
or cited source pages.

### Synthetic Data Guidance

Generate long economics documents with abstracts, tables, policy context, and
reference-like sections, then write detailed questions that require one portion
of the document. Hard negatives should be long documents from the same
economics topic but with the wrong model, region, or empirical claim.

## Example Data

| Query | Positive document |
| --- | --- |
| Would a GDP measure be improved by excluding foreign interest paid? The income method of calculating GDP is as follows: GDP = wages + profits + rents + interest + depreciation + taxes + NFFI. If an economy has high external d ... [truncated 225 chars](684 chars) | [ OECD Better Life Index ](/) ![](/media/bli/theme/img/logo-bli@2x.png) * [ Index ](/) * [ Responses ](/responses/) * Countries __ * [ Australia ](/countries/australia/) * [ Austria ](/countries/austria/) * [ Belgium ](/count ... [truncated 225 chars](13187 chars) |
| Derivative to ln(K(t)) in the RBC model In the calculation of the equation of motion for capital in the RBC model, I came across this equation: d ln K_(t+1) / d ln K_t = (d K_(t+1) / d K_t) * (K_t / K_(t+1)) Can someone expla ... [truncated 225 chars](406 chars) | Jump to content Main menu Main menu move to sidebar hide Navigation * [ Main page ](/wiki/Main_Page "Visit the main page \[z\]") * [ Contents ](/wiki/Wikipedia:Contents "Guides to browsing Wikipedia") * [ Current events ](/wi ... [truncated 225 chars](34111 chars) |
| What is the purpose of taxes if central banks can fund deficit spending? Somewhat straight forward. If the federal reserve can print money to buy treasuries to fund deficit spending, what is the purpose of taxes? Sure, taxes ... [truncated 225 chars](524 chars) | The Economic and Social Review, Vol. 35, No. 3, Winter, 2004, pp. 251-266 Inflation and Money Growth: Evidence from a Multi-Country Data-Set JOHN C. FRAIN* Central Bank and Financial Services Regulatory Authority of Ireland a ... [truncated 225 chars](29854 chars) |
| Is it always a trade off between efficiency and equity? Is there any situations where we can achieve both equity and efficiency? I'm thinking of Covid 19 vaccine program which is run by Goverment. Although the cost for the pr ... [truncated 225 chars](467 chars) | ##### This website uses cookies. By clicking the "Accept" button or continuing to browse our site, you agree to first-party and session-only cookies being stored on your device to enhance site navigation and analyze site perf ... [truncated 225 chars](5408 chars) |
| How are stock prices determined in the following cases? I looked at this question already. I know there is an order book with bid and ask and that the price is updated when a match occurs. But I have two questions: What happe ... [truncated 225 chars](689 chars) | INVESTING SIMULATOR BANKING PERSONAL FINANCE NEWS REVIEWS ACADEMY TRADE TRADING SKILLS TRADING BASIC EDUCATION Matching Orders: What They Are, How They Work, and Examples By GORDON SCOTT Updated April 27, 2022 Reviewed by CHA ... [truncated 225 chars](6039 chars) |

## Dataset Information

| Field | Value |
| --- | --- |
| Nano set | NanoBRIGHT |
| Backing dataset | NanoBRIGHT |
| Task / split | NanoBrightEconomicsLong |
| Source task | Economics StackExchange long-document |
| Hugging Face dataset | [hakari-bench/NanoBRIGHT](https://huggingface.co/datasets/hakari-bench/NanoBRIGHT) |
| Source dataset | [xlangai/BRIGHT](https://huggingface.co/datasets/xlangai/BRIGHT) |
| Language | en |
| Category | natural_language |
| Queries | 103 |
| Documents | 515 |
| Positive qrels | 109 |
| Positives per query | avg 1.06, min 1, median 1, max 3 |
| Multi-positive queries | 5 (4.85%) |
| BM25 nDCG@10 | 0.2658 |
| BM25 hit@10 | 0.4369 |
| BM25 Recall@100 | 0.7248 |
| BM25 candidate subset | top-500 (`bm25`) |
| Dense nDCG@10 | 0.4266 |
| Dense hit@10 | 0.6602 |
| Dense Recall@100 | 0.9083 |
| Dense candidate subset | top-500 (`harrier_oss_v1_270m`) |
| Reranking hybrid nDCG@10 | 0.3764 |
| Reranking hybrid hit@10 | 0.5728 |
| Reranking hybrid Recall@100 | 0.8991 |
| Reranking hybrid candidate subset | top-100 plus optional rank-101 safeguard (`reranking_hybrid`) |
| Reranking hybrid candidates / query | 100-101 |
| Reranking hybrid safeguard rows | 10 |
| Query length avg chars | 739.57 |
| Document length avg chars | 38615.97 |

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
  task_name: NanoBrightEconomicsLong
  split_name: NanoBrightEconomicsLong
  source_task: Economics StackExchange long-document
  source_dataset_id: xlangai/BRIGHT
  language: en
  category: natural_language
  document_path: docs/benchmark_tasks/NanoBRIGHT/NanoBrightEconomicsLong.md
  source_research:
    primary_source_type: benchmark_paper
    paper_pdf_or_html_checked: true
    no_paper_note: null
  counts:
    queries: 103
    documents: 515
    positive_qrels: 109
  positives_per_query:
    average: 1.058252427184466
    min: 1
    median: 1
    max: 3
    multi_positive_queries: 5
    multi_positive_query_percent: 4.854368932038835
  text_stats_chars:
    query_mean: 739.5728155339806
    document_mean: 38615.970873786406
  bm25:
    ndcg_at_10: 0.26583981555927855
    hit_at_10: 0.4368932038834951
    source: dataset_candidate_subset
  learning:
    original_train_split: unknown
    evaluation_split_origin: BRIGHT Economics long-document evaluation split
    train_eval_overlap_audit: not_audited
    leakage_note: exclude NanoBRIGHT EconomicsLong queries and full cited source pages
    useful_training_data:
    - long economics reports aligned to questions
    - document-level paper recommendation data
    - cited-source retrieval from economics forums
    synthetic_data:
      document_generation: long economics documents with abstracts, tables, and policy
        context
      question_generation: detailed economics questions requiring one section of the
        source
      answerability: positive full document should contain the relevant model, evidence,
        or explanation
    multi_positive_training: single_positive_question_document_focus
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
      ndcg_at_10: 0.2658398156
      hit_at_10: 0.4368932039
      recall_at_100: 0.7247706422
      candidate_count_min: 500
      candidate_count_max: 500
      candidate_count_mean: 500.0
      query_count: 103
      query_coverage: 1.0
      relevant_coverage_at_100: 0.7247706422
    dense:
      config: harrier_oss_v1_270m
      label: Dense
      source: dataset_candidate_subset
      top_k: 500
      ndcg_at_10: 0.426587992
      hit_at_10: 0.6601941748
      recall_at_100: 0.9082568807
      candidate_count_min: 500
      candidate_count_max: 500
      candidate_count_mean: 500.0
      query_count: 103
      query_coverage: 1.0
      relevant_coverage_at_100: 0.9082568807
    reranking_hybrid:
      config: reranking_hybrid
      label: Reranking hybrid
      source: dataset_candidate_subset
      top_k: 100
      ndcg_at_10: 0.3764442369
      hit_at_10: 0.572815534
      recall_at_100: 0.8990825688
      candidate_count_min: 100
      candidate_count_max: 101
      candidate_count_mean: 100.097087
      query_count: 103
      query_coverage: 1.0
      relevant_coverage_at_100: 0.8990825688
      safeguard_positive_rows: 10
      rows_with_101_candidates: 10
```
