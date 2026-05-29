# NanoBRIGHT / NanoBrightEarthScience

## Overview

`NanoBrightEarthScience` is the Earth Science StackExchange slice of BRIGHT.
Queries are technical Earth-science posts, and relevant documents are web
passages cited by answers or otherwise validated as supporting the answer.

## Details

### What the Original Data Measures

[BRIGHT](https://arxiv.org/abs/2407.12883) describes its StackExchange tasks as
retrieval problems where documents provide useful information for deriving an
answer rather than directly containing a short answer string. For Earth Science,
this means queries can involve geology, seasons, climate data, planetary
science, or environmental chemistry, while positives are cited web passages that
support the reasoning needed to answer.

### Observed Data Profile

The split has 116 queries, 10,000 documents, and 579 positive qrels. Queries
average 476.71 characters and often include long context, quoted assumptions, or
tooling details. Documents average 716.25 characters and are passage chunks from
web pages, reports, tutorials, or encyclopedic sources. Positives average 4.99
per query, with a maximum of 22.

### BM25 Difficulty

Using the dataset-provided BM25 candidate column, BM25 reaches nDCG@10 =
0.3163 and hit@10 = 0.6552. It ranks 37 queries with a positive first, and the
median best positive rank is 3.5. BM25 is stronger here than in AoPS because
some queries contain distinctive terms such as ERA5, limestone, or season, but
it still misses cases where the useful evidence uses a broader scientific
concept.

### Training Data That May Help

Useful data includes Earth Science StackExchange posts with cited sources,
geology and climate QA with references, technical documentation retrieval for
data products, and hard negatives from the same geological or climate topic.

### Synthetic Data Guidance

Generate realistic Earth-science questions with assumptions and context, then
pair them with source passages from reports, encyclopedic pages, or data
documentation. Hard negatives should share topic terms but fail to answer the
specific physical, geological, or data-access question.

## Example Data

| Query | Positive document |
| --- | --- |
| How is/was continental drift monitored? I am curious about current technology but I am particularly interested in what techniques were employed prior to the advent of satellite technology. (189 chars) | ReadEditView history General What links hereRelated changesUpload fileSpecial pagesPermanent linkPage informationCite this pageGet shortened URLDownload QR codeWikidata item Print/export Download as PDFPrintable version From ... [truncated 225 chars](6171 chars) |
| I am a lay person in meteorology, maybe this is not the right place for my question, but I would like to ask then. My question is simple: is there a website or institute that has integrated statistics on forecasting the occur ... [truncated 225 chars](284 chars) | 48 degrees (relative to the normal). Therefore, if light strikes the back of a raindrop at an angle greater than 48 degrees, it will be reflected back. If the angle is smaller than 48 degrees, the light will simply pass on th ... [truncated 225 chars](1114 chars) |
| Which plant is the most efficient in making oxygen for it's weight? I want to think it is the greenest plant with more leaves and least trunk in full sun? (154 chars) | more information on current conditions... Dismiss View all alerts Contact Us Algae While some plants decorate the landscape and are very visible at Rocky Mountain National Park, others are seldom seen. Tiny floating plants, c ... [truncated 225 chars](4877 chars) |
| My son wants to replicate some experiments and try to grow plants in Martian soil for his A-level science project. I know NASA have managed to produce soil that mimics Martian soil, however I also know how expensive it is. My ... [truncated 225 chars](408 chars) | NASA graph of elemental composition of Mars soil. The five most abundant ingredients, account for almost 90% of the dirt taken from Mars samples. SiO2 - 49.5% Fe2O3 - 17.9% Al2O3 - 7.2% MgO - 7.7% CaO - 6.7% That seems like a ... [truncated 225 chars](1624 chars) |
| It is said about ozone: a layer in the earth's stratosphere at an altitude of about 10 km (6.2 miles) containing a high concentration of ozone Over the Earth’s surface, the ozone layer’s average thickness is about 300 Dobson ... [truncated 225 chars](350 chars) | part1 ------------------- The ozone–oxygen cycle is the process by which ozone is continually regenerated in Earth's stratosphere, converting ultraviolet radiation (UV) into heat. In 1930 Sydney Chapman resolved the chemistry ... [truncated 225 chars](632 chars) |

## Dataset Information

| Field | Value |
| --- | --- |
| Nano set | NanoBRIGHT |
| Backing dataset | NanoBRIGHT |
| Task / split | NanoBrightEarthScience |
| Source task | Earth Science StackExchange |
| Hugging Face dataset | [hakari-bench/NanoBRIGHT](https://huggingface.co/datasets/hakari-bench/NanoBRIGHT) |
| Source dataset | [xlangai/BRIGHT](https://huggingface.co/datasets/xlangai/BRIGHT) |
| Language | en |
| Category | natural_language |
| Queries | 116 |
| Documents | 10000 |
| Positive qrels | 579 |
| Positives per query | avg 4.99, min 1, median 4, max 22 |
| Multi-positive queries | 96 (82.76%) |
| BM25 nDCG@10 | 0.4611 |
| BM25 hit@10 | 0.7672 |
| BM25 Recall@100 | 0.6839 |
| BM25 candidate subset | top-500 (`bm25`) |
| Dense nDCG@10 | 0.5406 |
| Dense hit@10 | 0.8448 |
| Dense Recall@100 | 0.7288 |
| Dense candidate subset | top-500 (`harrier_oss_v1_270m`) |
| Reranking hybrid nDCG@10 | 0.5518 |
| Reranking hybrid hit@10 | 0.9052 |
| Reranking hybrid Recall@100 | 0.7979 |
| Reranking hybrid candidate subset | top-100 plus optional rank-101 safeguard (`reranking_hybrid`) |
| Reranking hybrid candidates / query | 100-101 |
| Reranking hybrid safeguard rows | 2 |
| Query length avg chars | 476.71 |
| Document length avg chars | 716.25 |

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
  task_name: NanoBrightEarthScience
  split_name: NanoBrightEarthScience
  source_task: Earth Science StackExchange
  source_dataset_id: xlangai/BRIGHT
  language: en
  category: natural_language
  document_path: docs/benchmark_tasks/NanoBRIGHT/NanoBrightEarthScience.md
  source_research:
    primary_source_type: benchmark_paper
    paper_pdf_or_html_checked: true
    no_paper_note: null
  counts:
    queries: 116
    documents: 10000
    positive_qrels: 579
  positives_per_query:
    average: 4.991379310344827
    min: 1
    median: 4.0
    max: 22
    multi_positive_queries: 96
    multi_positive_query_percent: 82.75862068965517
  text_stats_chars:
    query_mean: 476.7068965517241
    document_mean: 716.2489
  bm25:
    ndcg_at_10: 0.46112272549313976
    hit_at_10: 0.7672413793103449
    source: dataset_candidate_subset
  learning:
    original_train_split: unknown
    evaluation_split_origin: BRIGHT Earth Science StackExchange evaluation split
    train_eval_overlap_audit: not_audited
    leakage_note: exclude NanoBRIGHT EarthScience queries, cited positives, and linked
      answer pages
    useful_training_data:
    - Earth Science StackExchange posts with cited sources
    - geology and climate QA with references
    - technical documentation retrieval for scientific data products
    synthetic_data:
      document_generation: reports, encyclopedic passages, or data documentation about
        Earth science
      question_generation: contextual Earth-science questions with physical or data-access
        intent
      answerability: positives should support the specific geological, climate, or
        data explanation
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
      ndcg_at_10: 0.4611227255
      hit_at_10: 0.7672413793
      recall_at_100: 0.6839378238
      candidate_count_min: 500
      candidate_count_max: 500
      candidate_count_mean: 500.0
      query_count: 116
      query_coverage: 1.0
      relevant_coverage_at_100: 0.6839378238
    dense:
      config: harrier_oss_v1_270m
      label: Dense
      source: dataset_candidate_subset
      top_k: 500
      ndcg_at_10: 0.5405929676
      hit_at_10: 0.8448275862
      recall_at_100: 0.7288428325
      candidate_count_min: 500
      candidate_count_max: 500
      candidate_count_mean: 500.0
      query_count: 116
      query_coverage: 1.0
      relevant_coverage_at_100: 0.7288428325
    reranking_hybrid:
      config: reranking_hybrid
      label: Reranking hybrid
      source: dataset_candidate_subset
      top_k: 100
      ndcg_at_10: 0.5518341636
      hit_at_10: 0.9051724138
      recall_at_100: 0.7979274611
      candidate_count_min: 100
      candidate_count_max: 101
      candidate_count_mean: 100.017241
      query_count: 116
      query_coverage: 1.0
      relevant_coverage_at_100: 0.7979274611
      safeguard_positive_rows: 2
      rows_with_101_candidates: 2
```
