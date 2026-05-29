# NanoMMTEB-v2 / wino_grande

## Overview

`wino_grande` is an English commonsense-reasoning retrieval task. Queries are
Winograd-style sentences with a blank, and documents are short candidate
referents. The retriever must select the entity or noun that correctly fills the
blank.

## Details

### What the Original Data Measures

[WinoGrande: An Adversarial Winograd Schema Challenge at Scale](https://arxiv.org/abs/1907.10641)
introduces a large adversarially filtered Winograd-style benchmark for
commonsense pronoun and referent resolution. The retrieval version treats the
masked sentence as a query and the correct referent string as the positive
document.

### Observed Data Profile

The split has 200 queries, 5,095 documents, and 200 positive qrels. Each query
has one positive. Queries average 111.98 characters. Documents average 7.68
characters and are usually names or short common nouns, such as `water`, `apple`,
or `Carrie`.

### BM25 Difficulty

Using the dataset-provided BM25 candidate column, BM25 reaches nDCG@10 = 0.4611
and hit@10 = 0.9000. BM25 often finds the correct answer because the referent
appears verbatim in the sentence, but top ranking still requires resolving which
candidate fits the commonsense relation.

### Training Data That May Help

Useful data includes Winograd-style pronoun resolution, coreference QA,
commonsense cloze tasks, and retrieval pairs with candidate referents. Training
should avoid evaluation sentences and answer strings.

### Synthetic Data Guidance

Generate sentences with two plausible referents and one blank. The positive
should require a commonsense relation such as cause, possession, physical
property, intention, or social role. Hard negatives should include the competing
referent from the same sentence.

## Example Data

| Query | Positive document |
| --- | --- |
| Sentence: Mary wanted to get another piercing in her ear, but the _ was much too tiny.. (87 chars) | ear (3 chars) |
| Sentence: She counted her calories for her diet and found she needed more so she ate a brownie instead of an apple since the _ has fewer.. (138 chars) | apple (5 chars) |
| Sentence: The game of chess was easy to play for Angela but not Rebecca because _ had a analytical mind.. (105 chars) | Angela (6 chars) |
| Sentence: Joe immediately went to bakery before the bank because the _ had a limited supply of what he wanted.. (111 chars) | bakery (6 chars) |
| Sentence: William liked to be outside more than Kyle so _ spent time arguing for getting a pool.. (97 chars) | William (7 chars) |

## Dataset Information

| Field | Value |
| --- | --- |
| Nano set | NanoMMTEB-v2 |
| Backing dataset | NanoMMTEB-v2 |
| Task / split | wino_grande |
| Hugging Face dataset | [hakari-bench/NanoMMTEB-v2](https://huggingface.co/datasets/hakari-bench/NanoMMTEB-v2) |
| Source dataset | [mteb/WinoGrande](https://huggingface.co/datasets/mteb/WinoGrande) |
| Language | en |
| Category | natural_language |
| Queries | 200 |
| Documents | 5095 |
| Positive qrels | 200 |
| BM25 nDCG@10 | 0.5084 |
| BM25 hit@10 | 0.8750 |
| BM25 Recall@100 | 1.0000 |
| BM25 candidate subset | top-500 (`bm25`) |
| Dense nDCG@10 | 0.4940 |
| Dense hit@10 | 0.7750 |
| Dense Recall@100 | 0.9800 |
| Dense candidate subset | top-500 (`harrier_oss_v1_270m`) |
| Reranking hybrid nDCG@10 | 0.6139 |
| Reranking hybrid hit@10 | 0.9050 |
| Reranking hybrid Recall@100 | 1.0000 |
| Reranking hybrid candidate subset | top-100 plus optional rank-101 safeguard (`reranking_hybrid`) |
| Reranking hybrid candidates / query | 100 |
| Reranking hybrid safeguard rows | 0 |
| Query length avg chars | 111.98 |
| Document length avg chars | 7.68 |

### Public Sources

- [WinoGrande: An Adversarial Winograd Schema Challenge at Scale](https://arxiv.org/abs/1907.10641).
- [WinoGrande project page](https://winogrande.allenai.org/).
- [mteb/WinoGrande](https://huggingface.co/datasets/mteb/WinoGrande).

### Hugging Face Links

- Nano dataset: [hakari-bench/NanoMMTEB-v2](https://huggingface.co/datasets/hakari-bench/NanoMMTEB-v2)
- Source dataset: [mteb/WinoGrande](https://huggingface.co/datasets/mteb/WinoGrande)

### Source Reference Table

| Title | Year | Type | URL |
| --- | ---: | --- | --- |
| WinoGrande: An Adversarial Winograd Schema Challenge at Scale | 2019 | task paper | https://arxiv.org/abs/1907.10641 |
| WinoGrande project page | 2019 | project page | https://winogrande.allenai.org/ |
| mteb/WinoGrande | 2024 | dataset card | https://huggingface.co/datasets/mteb/WinoGrande |

## Machine-Readable Metadata

<!-- benchmark-task-metadata:v1 -->

```yaml
benchmark_task_metadata:
  schema_version: 1
  document_status: first_pass
  nano_set: NanoMMTEB-v2
  backing_dataset: NanoMMTEB-v2
  dataset_id: hakari-bench/NanoMMTEB-v2
  task_name: wino_grande
  split_name: wino_grande
  language: en
  category: natural_language
  document_path: docs/benchmark_tasks/NanoMMTEB-v2/wino_grande.md
  source_research:
    primary_source_type: task_paper
    paper_pdf_or_html_checked: true
    no_paper_note: null
  counts:
    queries: 200
    documents: 5095
    positive_qrels: 200
  positives_per_query:
    average: 1.0
    min: 1
    median: 1.0
    max: 1
    multi_positive_queries: 0
    multi_positive_query_percent: 0.0
  text_stats_chars:
    query_mean: 111.975
    document_mean: 7.68243375858685
  bm25:
    ndcg_at_10: 0.5084184388392939
    hit_at_10: 0.875
    source: dataset_candidate_subset
  learning:
    original_train_split: available
    evaluation_split_origin: test
    train_eval_overlap_audit: not_audited
    leakage_note: do not train on this Nano split's Winogrande sentences, qrels, or
      answer candidates
    useful_training_data:
    - Winograd-style pronoun resolution
    - coreference question answering
    - commonsense cloze tasks
    - candidate-referent retrieval pairs
    synthetic_data:
      document_generation: short candidate referent strings from sentence entities
      question_generation: masked commonsense sentences with two plausible referents
      answerability: positive referent should be selected by commonsense constraints
        in the sentence
    multi_positive_training: single_positive_question_document_focus
  links:
    nano_dataset: https://huggingface.co/datasets/hakari-bench/NanoMMTEB-v2
    source_urls:
    - label: WinoGrande arXiv
      url: https://arxiv.org/abs/1907.10641
    - label: WinoGrande project page
      url: https://winogrande.allenai.org/
    - label: mteb/WinoGrande
      url: https://huggingface.co/datasets/mteb/WinoGrande
    source_notes: []
  references:
  - title: 'WinoGrande: An Adversarial Winograd Schema Challenge at Scale'
    url: https://arxiv.org/abs/1907.10641
    year: 2019
    is_paper: true
    source_confidence: definitive_paper_link
  candidate_subsets:
    bm25:
      config: bm25
      label: BM25
      source: dataset_candidate_subset
      top_k: 500
      ndcg_at_10: 0.5084184388
      hit_at_10: 0.875
      recall_at_100: 1.0
      candidate_count_min: 500
      candidate_count_max: 500
      candidate_count_mean: 500.0
      query_count: 200
      query_coverage: 1.0
      relevant_coverage_at_100: 1.0
    dense:
      config: harrier_oss_v1_270m
      label: Dense
      source: dataset_candidate_subset
      top_k: 500
      ndcg_at_10: 0.4939897818
      hit_at_10: 0.775
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
      ndcg_at_10: 0.6139469035
      hit_at_10: 0.905
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
