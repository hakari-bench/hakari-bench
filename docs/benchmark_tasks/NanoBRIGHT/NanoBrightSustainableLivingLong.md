# NanoBRIGHT / NanoBrightSustainableLivingLong

## Overview

`NanoBrightSustainableLivingLong` is the long-document version of the
Sustainable Living StackExchange BRIGHT task. Queries are sustainability
questions, and relevant documents are full cited source pages or reports.

## Details

### What the Original Data Measures

[BRIGHT](https://arxiv.org/abs/2407.12883) describes its long-context
StackExchange variants as retrieval from complete web pages with significantly
more tokens and fewer documents. In this task, the model must retrieve full
environmental reports, encyclopedia pages, or product-program documents that
contain evidence for practical sustainability decisions.

### Observed Data Profile

The split has 108 queries, 551 documents, and 129 positive qrels. Queries
average 682.84 characters. Documents average 38,204.30 characters and include
ENERGY STAR program material, product pages, Wikipedia-style pages, and long
environmental reference pages. Positives average 1.19 per query; 15 queries
have multiple positives.

### BM25 Difficulty

Using the dataset-provided BM25 candidate column, BM25 reaches nDCG@10 =
0.3038 and hit@10 = 0.4815. It ranks 22 queries with a positive first, and the
median best positive rank is 15. Long documents often contain broad
sustainability vocabulary, navigation text, and multiple topics, so exact term
overlap is not enough to identify whether a page supports the decision.

### Training Data That May Help

Useful data includes long environmental report retrieval, document-level
sustainability QA, cited-source retrieval from environmental forums, and
passage-to-full-page supervision. Avoid using the evaluation posts and cited
pages from this Nano split.

### Synthetic Data Guidance

Generate long environmental pages with sections about products, materials,
energy programs, lifecycle impacts, and caveats. Questions should ask practical
comparisons or decision criteria. Hard negatives should cover the same product
or impact category but not answer the specific question.

## Example Data

| Query | Positive document |
| --- | --- |
| More uses for bacon grease We (my family) consume good amounts of bacon which produce a lot of bacon grease. I don't like wasting anything that I could reuse or repurpose, including this. I use this byproduct in many differen ... [truncated 225 chars](604 chars) | [ ![Mother Earth News](https://ogden_images.s3.amazonaws.com/www.motherearthnews.com/images/2022/03/04200002/men_logo.svg) ](https://www.motherearthnews.com) * [ Organic Gardening ](https://www.motherearthnews.com/organic-gar ... [truncated 225 chars](35063 chars) |
| Determining carbon reduction vs cost of various home upgrades I've done some amount of upgrades to my house to reduce my overall carbon emissions, and reading online there are all kinds of suggestions for doing even more: Rep ... [truncated 225 chars](2158 chars) | Skip to main content [ ![National Renewable Energy Laboratory](/assets/images/nrel-logo-web.svg) ](/) Toggle Search Search NREL.gov Search [ Buildings ](/buildings/) Menu * Research * [ Research __ ](/buildings/research.html) ... [truncated 225 chars](17158 chars) |
| Forcing water circulation in solar hot water installation I'm planning an installation for heating water using solar "exchanger" panels (solar used to heat water directly, not through electricity). I don't want to bind the re ... [truncated 225 chars](1071 chars) | Skip to content [ ](https://www.firespeaking.com/wp- login.php?redirect_to=https%3A%2F%2Fwww.firespeaking.com%2Fmasonry- heaters%2Fheat-water%2Fdetails-of-plumbing) Username or Email Address Password Remember Me [ Lost your p ... [truncated 225 chars](19918 chars) |
| How to recognize products with neonicotinoid pesticides in them? Recently, the EU has temporarily banned neonicotinoid pesticides because there are strong indications that these pesticides are responsible for the decline in b ... [truncated 225 chars](561 chars) | Jump to content Main menu Main menu move to sidebar hide Navigation * [ Main page ](/wiki/Main_Page "Visit the main page \[z\]") * [ Contents ](/wiki/Wikipedia:Contents "Guides to browsing Wikipedia") * [ Current events ](/wi ... [truncated 225 chars](132239 chars) |
| Why don't mineral water cans carry a deposit label? I've been putting in the recycling bin all our "sparkling water," "mineral water," and unflavored Canada Dry cans. But then I wondered if I could return them to the grocery ... [truncated 225 chars](443 chars) | Skip to main content Your browser does not support iFrames [ Department of Environmental Conservation ](/) * Things To Do ## Things To Do There are many ways to experience New York’s great outdoors. Maybe you’ll get hooked on ... [truncated 225 chars](27037 chars) |

## Dataset Information

| Field | Value |
| --- | --- |
| Nano set | NanoBRIGHT |
| Backing dataset | NanoBRIGHT |
| Task / split | NanoBrightSustainableLivingLong |
| Source task | Sustainable Living StackExchange long-document |
| Hugging Face dataset | [hakari-bench/NanoBRIGHT](https://huggingface.co/datasets/hakari-bench/NanoBRIGHT) |
| Source dataset | [xlangai/BRIGHT](https://huggingface.co/datasets/xlangai/BRIGHT) |
| Language | en |
| Category | natural_language |
| Queries | 108 |
| Documents | 551 |
| Positive qrels | 129 |
| Positives per query | avg 1.19, min 1, median 1, max 5 |
| Multi-positive queries | 15 (13.89%) |
| BM25 nDCG@10 | 0.3277 |
| BM25 hit@10 | 0.5000 |
| BM25 Recall@100 | 0.8992 |
| BM25 candidate subset | top-500 (`bm25`) |
| Dense nDCG@10 | 0.5501 |
| Dense hit@10 | 0.7870 |
| Dense Recall@100 | 0.9690 |
| Dense candidate subset | top-500 (`harrier_oss_v1_270m`) |
| Reranking hybrid nDCG@10 | 0.4436 |
| Reranking hybrid hit@10 | 0.6852 |
| Reranking hybrid Recall@100 | 0.9845 |
| Reranking hybrid candidate subset | top-100 plus optional rank-101 safeguard (`reranking_hybrid`) |
| Reranking hybrid candidates / query | 100-101 |
| Reranking hybrid safeguard rows | 2 |
| Query length avg chars | 682.84 |
| Document length avg chars | 38204.30 |

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
  task_name: NanoBrightSustainableLivingLong
  split_name: NanoBrightSustainableLivingLong
  source_task: Sustainable Living StackExchange long-document
  source_dataset_id: xlangai/BRIGHT
  language: en
  category: natural_language
  document_path: docs/benchmark_tasks/NanoBRIGHT/NanoBrightSustainableLivingLong.md
  source_research:
    primary_source_type: benchmark_paper
    paper_pdf_or_html_checked: true
    no_paper_note: null
  counts:
    queries: 108
    documents: 551
    positive_qrels: 129
  positives_per_query:
    average: 1.1944444444444444
    min: 1
    median: 1.0
    max: 5
    multi_positive_queries: 15
    multi_positive_query_percent: 13.88888888888889
  text_stats_chars:
    query_mean: 682.8425925925926
    document_mean: 38204.29945553539
  bm25:
    ndcg_at_10: 0.32772659949565813
    hit_at_10: 0.5
    source: dataset_candidate_subset
  learning:
    original_train_split: unknown
    evaluation_split_origin: BRIGHT Sustainable Living long-document evaluation split
    train_eval_overlap_audit: not_audited
    leakage_note: exclude NanoBRIGHT SustainableLivingLong queries and full cited
      source pages
    useful_training_data:
    - long environmental report retrieval
    - document-level sustainability QA
    - cited-source retrieval from environmental forums
    synthetic_data:
      document_generation: long environmental pages about products, materials, energy,
        and lifecycle impacts
      question_generation: sustainability questions asking practical comparisons or
        decision criteria
      answerability: positive full document should contain evidence for the specific
        environmental decision
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
      ndcg_at_10: 0.3277265995
      hit_at_10: 0.5
      recall_at_100: 0.8992248062
      candidate_count_min: 500
      candidate_count_max: 500
      candidate_count_mean: 500.0
      query_count: 108
      query_coverage: 1.0
      relevant_coverage_at_100: 0.8992248062
    dense:
      config: harrier_oss_v1_270m
      label: Dense
      source: dataset_candidate_subset
      top_k: 500
      ndcg_at_10: 0.5500845834
      hit_at_10: 0.787037037
      recall_at_100: 0.9689922481
      candidate_count_min: 500
      candidate_count_max: 500
      candidate_count_mean: 500.0
      query_count: 108
      query_coverage: 1.0
      relevant_coverage_at_100: 0.9689922481
    reranking_hybrid:
      config: reranking_hybrid
      label: Reranking hybrid
      source: dataset_candidate_subset
      top_k: 100
      ndcg_at_10: 0.4435759713
      hit_at_10: 0.6851851852
      recall_at_100: 0.984496124
      candidate_count_min: 100
      candidate_count_max: 101
      candidate_count_mean: 100.018519
      query_count: 108
      query_coverage: 1.0
      relevant_coverage_at_100: 0.984496124
      safeguard_positive_rows: 2
      rows_with_101_candidates: 2
```
