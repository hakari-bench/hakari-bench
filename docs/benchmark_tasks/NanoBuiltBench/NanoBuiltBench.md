# NanoBuiltBench / NanoBuiltBench

## Overview

`NanoBuiltBench` is an English built-asset information retrieval task. Queries
are compact IFC-derived descriptions of building, infrastructure, equipment, or
facility-management entities. Documents are Uniclass product descriptions. The
task measures whether a retriever can align terminology across built-environment
classification systems, such as mapping an IFC entity definition to the relevant
Uniclass product class descriptions.

## Details

### What the Original Data Measures

[Benchmarking pre-trained text embedding models in aligning built asset information](https://arxiv.org/abs/2411.12056)
introduces BuiltBench as a benchmark for evaluating whether text embedding
models can map built asset information to established classification systems and
taxonomies. The later [Scientific Reports version](https://www.nature.com/articles/s41598-025-09052-5)
states that alignment means associating textual descriptions of built asset
entities with corresponding concepts or classes in a target classification
system.

The paper builds its product corpora from two authoritative sources:
Industry Foundation Classes (IFC) 4.3.2.0 and the Uniclass Pr product table. It
extracts names, descriptions, and hierarchy labels, normalizes IFC camel-case
entity names, appends parent type information for ambiguous enumerations, and
uses GPT-4 Turbo to paraphrase synthesized Uniclass descriptions. The authors
report manual review by two domain experts and only 16 adjustments among 4,234
Uniclass paraphrases.

For retrieval, the paper frames the task as finding product textual descriptions
for a query. It uses the Uniclass corpus as the searchable document collection
and IFC product titles or descriptions as queries. Ground truth relevance comes
from NBS-published cross-classification mappings between Uniclass records and
equivalent IFC entities.

### Observed Data Profile

The Nano split has 200 queries, 2,761 documents, and 1,480 positive qrel rows.
Queries average 102.12 characters and are usually short technical definitions,
such as `Water boiler.` or a definition of a molding, bollard, or cooling coil.
Documents average 341.69 characters and are normalized Uniclass descriptions
that include the product name, category, parent group, and a short functional
description.

The task is strongly multi-positive: each query has 7.40 positives on average,
with a median of 3 and a maximum of 93. Broad IFC classes can map to many
Uniclass products, while narrower query definitions may have only one positive.
The result is a fine-grained terminology alignment task rather than open-domain
question answering.

### BM25 Difficulty

Using the dataset-provided BM25 candidate column, BM25 reaches nDCG@10 = 0.3890
and hit@10 = 0.5850. It ranks 71 positives first and finds a positive inside
the top 10 for 117 of 200 queries. Lexical matching is useful because many
queries and documents share built-asset terms such as `cooling coil`, `boiler`,
or `moulding`.

The difficult cases show the limits of surface matching. BM25 can confuse radio
tuners with electronic sounders, ballast track beds with stone capping units,
underground access ducts with drainage pipes, and photocopiers with vending
machine locks. These errors are plausible lexical neighbors but wrong
cross-classification alignments, so strong models need hierarchy-aware and
domain-specific semantic matching.

### Training Data That May Help

Useful training data includes non-evaluation IFC-to-Uniclass mappings,
buildingSMART Data Dictionary definitions, Uniclass product descriptions, BIM
object catalogs, construction specification classification data, and hard
negatives from neighboring product categories. Because the task is
multi-positive, training should preserve multiple relevant products per IFC
query.

Training should not use the NanoBuiltBench evaluation queries, qrels, or
positive Uniclass descriptions. If using the public BuiltBench or MTEB release
for training, remove overlapping IFC and Uniclass IDs before evaluating on this
Nano split.

### Synthetic Data Guidance

For document-to-question generation, start from non-evaluation Uniclass,
buildingSMART, BIM, or product-catalog descriptions and generate concise
IFC-like definitions that preserve function, system, and hierarchy terms. The
query should be answerable by mapping to the document's product class, not by
copying the title.

For joint generation, create product-class descriptions and matching short
entity definitions across different classification vocabularies. Include hard
negatives with the same material, service system, or facility-management domain
but a different class. Do not seed generation with Nano evaluation queries or
positive documents.

## Example Data

| Query | Positive document |
| --- | --- |
| a short, thick post on the deck of a ship or a quay side, to which ship's rope may be secured. not to be confused with traffic bollards. (136 chars) | Capstan Capstan: This product is associated with equipment used for mooring, docking, and flotation, categorized under 'equipment' in the broader context of signage, sanitary fittings, and furnishings and equipment (ff&e) pro ... [truncated 225 chars](315 chars) |
| The covering is used to represent a molding being a strip of material to cover the transition of surfaces (often between wall cladding and ceiling). (148 chars) | Fibrous plaster mouldings Fibrous plaster mouldings are trim products used for interior wall and ceiling detailing, categorized under coverings and finishes. These mouldings add both functional and aesthetic value to room int ... [truncated 225 chars](232 chars) |
| Cooling coil using a refrigerant to cool the air stream directly. (65 chars) | Refrigerant cooling coils Refrigerant cooling coils are components associated with heating and cooling coils, classified under air and fume source products, which are part of the larger group of services and process source pr ... [truncated 225 chars](314 chars) |
| Water boiler. (13 chars) | Biomass boilers Biomass boilers are a type of boiler system classified under heating and cooling source products, which are part of the larger group of services and process source products. These boilers utilize organic mater ... [truncated 225 chars](255 chars) |
| An electrical appliance that has the primary function of storing food at low temperature but above the freezing point of water. (127 chars) | Drink chillers Drink chillers are a type of equipment categorized under commercial display and service catering products, which are part of the broader classification of signage, sanitary fittings, and furnishings and equipme ... [truncated 225 chars](320 chars) |

## Dataset Information

| Field | Value |
| --- | --- |
| Nano set | NanoBuiltBench |
| Backing dataset | NanoBuiltBench |
| Task / split | NanoBuiltBench |
| Hugging Face dataset | [hakari-bench/NanoBuiltBench](https://huggingface.co/datasets/hakari-bench/NanoBuiltBench) |
| Language | en |
| Category | natural_language |
| Queries | 200 |
| Documents | 2,761 |
| Positive qrels | 1,480 |
| Avg positives / query | 7.40 |
| Positives per query (min / median / max) | 1 / 3 / 93 |
| Queries with multiple positives | 133 (66.50%) |
| BM25 nDCG@10 | 0.5235 |
| BM25 hit@10 | 0.7400 |
| BM25 Recall@100 | 0.6642 |
| BM25 candidate subset | top-500 (`bm25`) |
| Dense nDCG@10 | 0.6209 |
| Dense hit@10 | 0.8400 |
| Dense Recall@100 | 0.7649 |
| Dense candidate subset | top-500 (`harrier_oss_v1_270m`) |
| Reranking hybrid nDCG@10 | 0.5751 |
| Reranking hybrid hit@10 | 0.8000 |
| Reranking hybrid Recall@100 | 0.7642 |
| Reranking hybrid candidate subset | top-100 plus optional rank-101 safeguard (`reranking_hybrid`) |
| Reranking hybrid candidates / query | 100-101 |
| Reranking hybrid safeguard rows | 9 |
| Query length avg chars | 102.12 |
| Document length avg chars | 341.69 |

### Public Sources

- [Benchmarking pre-trained text embedding models in aligning built asset information](https://arxiv.org/abs/2411.12056); 2024; Mehrzad Shahinmoghadam and Ali Motamedi; DOI: `10.48550/arXiv.2411.12056`.
- [Scientific Reports version](https://www.nature.com/articles/s41598-025-09052-5); 2025; DOI: `10.1038/s41598-025-09052-5`.
- [BuiltBench paper GitHub repository](https://github.com/mehrzadshm/built-bench-paper).
- [MTEB BuiltBenchRetrieval dataset card](https://huggingface.co/datasets/mteb/BuiltBenchRetrieval).

### Hugging Face Links

- Nano dataset: [hakari-bench/NanoBuiltBench](https://huggingface.co/datasets/hakari-bench/NanoBuiltBench)
- Source dataset: [mteb/BuiltBenchRetrieval](https://huggingface.co/datasets/mteb/BuiltBenchRetrieval)

### Source Reference Table

| Title | Year | Type | URL |
| --- | ---: | --- | --- |
| Benchmarking pre-trained text embedding models in aligning built asset information | 2024 | arXiv paper | https://arxiv.org/abs/2411.12056 |
| Benchmarking pre-trained text embedding models in aligning built asset information | 2025 | journal article | https://www.nature.com/articles/s41598-025-09052-5 |
| BuiltBench paper GitHub repository | 2025 | source repository | https://github.com/mehrzadshm/built-bench-paper |
| MTEB BuiltBenchRetrieval | 2025 | dataset card | https://huggingface.co/datasets/mteb/BuiltBenchRetrieval |

## Machine-Readable Metadata

<!-- benchmark-task-metadata:v1 -->

```yaml
benchmark_task_metadata:
  schema_version: 1
  document_status: first_pass
  nano_set: NanoBuiltBench
  backing_dataset: NanoBuiltBench
  dataset_id: hakari-bench/NanoBuiltBench
  task_name: NanoBuiltBench
  split_name: NanoBuiltBench
  language: en
  category: natural_language
  document_path: docs/benchmark_tasks/NanoBuiltBench/NanoBuiltBench.md
  source_research:
    primary_source_type: task_paper
    paper_pdf_or_html_checked: true
    paper_url: https://arxiv.org/abs/2411.12056
    additional_source_urls:
    - https://www.nature.com/articles/s41598-025-09052-5
    - https://github.com/mehrzadshm/built-bench-paper
    - https://huggingface.co/datasets/mteb/BuiltBenchRetrieval
  counts:
    queries: 200
    documents: 2761
    positive_qrels: 1480
  positives_per_query:
    average: 7.4
    min: 1
    median: 3.0
    max: 93
    multi_positive_queries: 133
    multi_positive_query_percent: 66.5
  text_stats_chars:
    query_mean: 102.125
    document_mean: 341.685983
  bm25:
    ndcg_at_10: 0.5234802923989015
    hit_at_10: 0.74
    source: dataset_candidate_subset
  learning:
    original_train_split: not_found
    evaluation_split_origin: BuiltBench retrieval release sampled into NanoBuiltBench
    train_eval_overlap_audit: not_audited
    leakage_note: exclude NanoBuiltBench evaluation IFC queries, qrels, and positive
      Uniclass descriptions
    useful_training_data:
    - non-overlapping IFC to Uniclass mappings
    - buildingSMART Data Dictionary definitions
    - Uniclass product descriptions and BIM object catalogs
    - construction specification classification pairs with hard negatives
    synthetic_data:
      document_generation: non-evaluation built asset product-class descriptions with
        hierarchy and function details
      question_generation: concise IFC-like entity definitions grounded in those descriptions
      hard_negatives: same material, service system, or product family but different
        class
      answerability: mappings should be justified by product function and classification
        hierarchy
    multi_positive_training: multi_positive_objective
  links:
    nano_dataset: https://huggingface.co/datasets/hakari-bench/NanoBuiltBench
    source_urls:
    - label: BuiltBench arXiv
      url: https://arxiv.org/abs/2411.12056
    - label: Scientific Reports article
      url: https://www.nature.com/articles/s41598-025-09052-5
    - label: BuiltBench GitHub
      url: https://github.com/mehrzadshm/built-bench-paper
    - label: MTEB BuiltBenchRetrieval
      url: https://huggingface.co/datasets/mteb/BuiltBenchRetrieval
    source_notes: []
  references:
  - title: Benchmarking pre-trained text embedding models in aligning built asset
      information
    url: https://arxiv.org/abs/2411.12056
    year: 2024
    doi: 10.48550/arXiv.2411.12056
    is_paper: true
    source_confidence: definitive_paper_link
  - title: Benchmarking pre-trained text embedding models in aligning built asset
      information
    url: https://www.nature.com/articles/s41598-025-09052-5
    year: 2025
    doi: 10.1038/s41598-025-09052-5
    is_paper: true
    source_confidence: definitive_paper_link
  candidate_subsets:
    bm25:
      config: bm25
      label: BM25
      source: dataset_candidate_subset
      top_k: 500
      ndcg_at_10: 0.5234802924
      hit_at_10: 0.74
      recall_at_100: 0.6641891892
      candidate_count_min: 500
      candidate_count_max: 500
      candidate_count_mean: 500.0
      query_count: 200
      query_coverage: 1.0
      relevant_coverage_at_100: 0.6641891892
    dense:
      config: harrier_oss_v1_270m
      label: Dense
      source: dataset_candidate_subset
      top_k: 500
      ndcg_at_10: 0.620879236
      hit_at_10: 0.84
      recall_at_100: 0.7648648649
      candidate_count_min: 500
      candidate_count_max: 500
      candidate_count_mean: 500.0
      query_count: 200
      query_coverage: 1.0
      relevant_coverage_at_100: 0.7648648649
    reranking_hybrid:
      config: reranking_hybrid
      label: Reranking hybrid
      source: dataset_candidate_subset
      top_k: 100
      ndcg_at_10: 0.5751054175
      hit_at_10: 0.8
      recall_at_100: 0.7641891892
      candidate_count_min: 100
      candidate_count_max: 101
      candidate_count_mean: 100.045
      query_count: 200
      query_coverage: 1.0
      relevant_coverage_at_100: 0.7641891892
      safeguard_positive_rows: 9
      rows_with_101_candidates: 9
```
