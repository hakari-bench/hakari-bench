# NanoBRIGHT / NanoBrightSustainableLiving

## Overview

`NanoBrightSustainableLiving` is the Sustainable Living StackExchange slice of
BRIGHT. Queries are user questions about environmental impact, energy, waste,
materials, and everyday sustainability decisions; relevant documents are cited
web passages that support an evidence-based answer.

## Details

### What the Original Data Measures

[BRIGHT](https://arxiv.org/abs/2407.12883) defines its StackExchange tasks
through cited-source retrieval: query posts come from accepted or high-vote
answer threads, and positive documents are web passages judged useful for
addressing the query. The benchmark also includes topically similar negatives,
which matters here because many sustainability questions share vocabulary about
energy, carbon, lifecycle analysis, or recycling.

### Observed Data Profile

The split has 108 queries, 10,000 documents, and 575 positive qrels. Queries
average 682.84 characters and often ask for quantitative or comparative
environmental reasoning. Documents average 733.62 characters and include
reports, article excerpts, encyclopedia passages, and practical guidance.
Positives average 5.32 per query, with a median of 3 and one query having 55
positives.

### BM25 Difficulty

Using the dataset-provided BM25 candidate column, BM25 reaches nDCG@10 =
0.2845 and hit@10 = 0.5185. It ranks 30 queries with a positive first, and the
median best positive rank is 10. Lexical matching is useful when terms such as
"life cycle assessment" or "emission intensity" appear, but many questions ask
for a comparison or judgment that requires the supporting evidence, not only the
topic.

### Training Data That May Help

Useful data includes non-overlapping Sustainable Living StackExchange posts with
cited sources, environmental QA with references, lifecycle-assessment document
retrieval, and hard negatives on the same product or resource but a different
impact pathway.

### Synthetic Data Guidance

Generate sustainability questions that compare materials, energy use, carbon
intensity, waste treatment, or lifecycle impacts. Positives should be source
passages containing the evidence needed for the comparison. Hard negatives
should be plausible environmental pages that do not address the exact decision.

## Example Data

| Query | Positive document |
| --- | --- |
| More uses for bacon grease We (my family) consume good amounts of bacon which produce a lot of bacon grease. I don't like wasting anything that I could reuse or repurpose, including this. I use this byproduct in many differen ... [truncated 225 chars](604 chars) | Tallow, or rendered beef fat, can be used to make soap. It went against my grain to throw out the tallow from a side of beef we bought, so I called our County Agent to see if he had any directions for making soap. To my surpr ... [truncated 225 chars](2693 chars) |
| Determining carbon reduction vs cost of various home upgrades I've done some amount of upgrades to my house to reduce my overall carbon emissions, and reading online there are all kinds of suggestions for doing even more: Rep ... [truncated 225 chars](2158 chars) | BEopt: Building Energy Optimization Tool The BEopt™ (Building Energy Optimization Tool) software provides capabilities to evaluate residential building designs and identify cost-optimal efficiency packages at various levels o ... [truncated 225 chars](1457 chars) |
| Forcing water circulation in solar hot water installation I'm planning an installation for heating water using solar "exchanger" panels (solar used to heat water directly, not through electricity). I don't want to bind the re ... [truncated 225 chars](1071 chars) | Here you can see the array of pipe going between the coil, the tank, and the domestic hot water plumbing. Alan transitioned to a flexible, pre-insulated stainless steel pipe to complete the thermosiphon loop (black-covered pi ... [truncated 225 chars](493 chars) |
| How to recognize products with neonicotinoid pesticides in them? Recently, the EU has temporarily banned neonicotinoid pesticides because there are strong indications that these pesticides are responsible for the decline in b ... [truncated 225 chars](561 chars) | Market [ [ edit ](/w/index.php?title=Neonicotinoid&action=edit&section=2 "Edit section: Market") ] ![](//upload.wikimedia.org/wikipedia/commons/thumb/9/98/Ambox_current_red.svg/42px- Ambox_current_red.svg.png) \| This section ... [truncated 225 chars](1911 chars) |
| Why don't mineral water cans carry a deposit label? I've been putting in the recycling bin all our "sparkling water," "mineral water," and unflavored Canada Dry cans. But then I wondered if I could return them to the grocery ... [truncated 225 chars](443 chars) | What beverages are covered by NY's Bottle Bill? Carbonated Soft Drinks Including Sparkling Water Carbonated Energy Drinks Carbonated Juice (anything less than 100% juice, containing added sugar or water) Carbonated Tea Soda W ... [truncated 225 chars](444 chars) |

## Dataset Information

| Field | Value |
| --- | --- |
| Nano set | NanoBRIGHT |
| Backing dataset | NanoBRIGHT |
| Task / split | NanoBrightSustainableLiving |
| Source task | Sustainable Living StackExchange |
| Hugging Face dataset | [hakari-bench/NanoBRIGHT](https://huggingface.co/datasets/hakari-bench/NanoBRIGHT) |
| Source dataset | [xlangai/BRIGHT](https://huggingface.co/datasets/xlangai/BRIGHT) |
| Language | en |
| Category | natural_language |
| Queries | 108 |
| Documents | 10000 |
| Positive qrels | 575 |
| Positives per query | avg 5.32, min 1, median 3, max 55 |
| Multi-positive queries | 76 (70.37%) |
| BM25 nDCG@10 | 0.4189 |
| BM25 hit@10 | 0.7130 |
| BM25 Recall@100 | 0.5948 |
| BM25 candidate subset | top-500 (`bm25`) |
| Dense nDCG@10 | 0.5338 |
| Dense hit@10 | 0.7963 |
| Dense Recall@100 | 0.7774 |
| Dense candidate subset | top-500 (`harrier_oss_v1_270m`) |
| Reranking hybrid nDCG@10 | 0.5198 |
| Reranking hybrid hit@10 | 0.7963 |
| Reranking hybrid Recall@100 | 0.7617 |
| Reranking hybrid candidate subset | top-100 plus optional rank-101 safeguard (`reranking_hybrid`) |
| Reranking hybrid candidates / query | 100-101 |
| Reranking hybrid safeguard rows | 7 |
| Query length avg chars | 682.84 |
| Document length avg chars | 733.62 |

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
  task_name: NanoBrightSustainableLiving
  split_name: NanoBrightSustainableLiving
  source_task: Sustainable Living StackExchange
  source_dataset_id: xlangai/BRIGHT
  language: en
  category: natural_language
  document_path: docs/benchmark_tasks/NanoBRIGHT/NanoBrightSustainableLiving.md
  source_research:
    primary_source_type: benchmark_paper
    paper_pdf_or_html_checked: true
    no_paper_note: null
  counts:
    queries: 108
    documents: 10000
    positive_qrels: 575
  positives_per_query:
    average: 5.324074074074074
    min: 1
    median: 3.0
    max: 55
    multi_positive_queries: 76
    multi_positive_query_percent: 70.37037037037037
  text_stats_chars:
    query_mean: 682.8425925925926
    document_mean: 733.6211
  bm25:
    ndcg_at_10: 0.41894516371556173
    hit_at_10: 0.7129629629629629
    source: dataset_candidate_subset
  learning:
    original_train_split: unknown
    evaluation_split_origin: BRIGHT Sustainable Living StackExchange evaluation split
    train_eval_overlap_audit: not_audited
    leakage_note: exclude NanoBRIGHT SustainableLiving queries, cited positives, and
      linked answer pages
    useful_training_data:
    - non-overlapping Sustainable Living StackExchange posts with cited sources
    - environmental QA with references
    - lifecycle-assessment document retrieval
    synthetic_data:
      document_generation: sustainability reports, lifecycle passages, and environmental
        guidance
      question_generation: comparative sustainability questions about materials, energy,
        waste, or carbon
      answerability: positives should provide evidence for the specific environmental
        comparison
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
      ndcg_at_10: 0.4189451637
      hit_at_10: 0.712962963
      recall_at_100: 0.5947826087
      candidate_count_min: 500
      candidate_count_max: 500
      candidate_count_mean: 500.0
      query_count: 108
      query_coverage: 1.0
      relevant_coverage_at_100: 0.5947826087
    dense:
      config: harrier_oss_v1_270m
      label: Dense
      source: dataset_candidate_subset
      top_k: 500
      ndcg_at_10: 0.5338133236
      hit_at_10: 0.7962962963
      recall_at_100: 0.7773913043
      candidate_count_min: 500
      candidate_count_max: 500
      candidate_count_mean: 500.0
      query_count: 108
      query_coverage: 1.0
      relevant_coverage_at_100: 0.7773913043
    reranking_hybrid:
      config: reranking_hybrid
      label: Reranking hybrid
      source: dataset_candidate_subset
      top_k: 100
      ndcg_at_10: 0.5197543247
      hit_at_10: 0.7962962963
      recall_at_100: 0.7617391304
      candidate_count_min: 100
      candidate_count_max: 101
      candidate_count_mean: 100.064815
      query_count: 108
      query_coverage: 1.0
      relevant_coverage_at_100: 0.7617391304
      safeguard_positive_rows: 7
      rows_with_101_candidates: 7
```
