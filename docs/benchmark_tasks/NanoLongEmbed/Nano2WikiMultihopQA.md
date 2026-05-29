# NanoLongEmbed / Nano2WikiMultihopQA

## Overview

`Nano2WikiMultihopQA` is the 2WikiMultiHopQA retrieval task in LongEmbed.
Queries are English multi-hop questions, and documents are long concatenations
of Wikipedia-derived passages. The retriever must find the document containing
the evidence chain needed to answer the question.

## Details

### What the Original Data Measures

[Constructing A Multi-hop QA Dataset for Comprehensive Evaluation of Reasoning Steps](https://arxiv.org/abs/2011.01060)
introduces 2WikiMultiHopQA, a dataset built from Wikipedia and Wikidata with
evidence triples that describe the reasoning path. The paper defines comparison,
inference, compositional, and bridge-comparison questions and uses templates
and logical rules to ensure multi-hop reasoning is needed.

[LongEmbed: Extending Embedding Models for Long Context Retrieval](https://arxiv.org/abs/2404.12096)
uses 2WikiMultiHopQA as a long-document retrieval task by making the question
the query and the Wikipedia-derived document the positive. The observed
documents contain many `Passage N:` sections, so the evidence can be embedded
among distractor entity summaries.

### Observed Data Profile

The Nano split has 200 English queries, 300 candidate documents, and 200
positive qrels. Every query has one positive. Queries average 67.52 characters,
while documents average 37,445.60 characters. Sampled questions ask about
family relations, places of death, song composers, film countries, and
nationalities.

The documents are much more structured than NarrativeQA or QMSum: each positive
is a bundle of short encyclopedia passages. This makes entity matching strong,
but the retriever still needs to rank the bundle that contains the bridge
entities and final answer evidence.

### BM25 Difficulty

Using the dataset-provided BM25 candidate column, BM25 reaches nDCG@10 =
0.9515 and hit@10 = 0.9800. BM25 ranks 184 positives first and 196 in the top
10. The strong lexical baseline reflects the entity-heavy question style and
the repeated entity names inside candidate passage bundles.

Remaining errors are likely cases where multiple documents share the same
entities, relation words, or film and person names. Dense models still need to
preserve multi-hop relation intent rather than only retrieve by surface entity
overlap.

### Training Data That May Help

Useful training data includes the non-overlapping 2WikiMultiHopQA train split,
HotpotQA-style multi-hop retrieval pairs, Wikipedia entity-linking retrieval
pairs, and hard negatives that share one bridge entity but not the full
reasoning chain. Training should exclude 2WikiMultiHopQA test examples, Nano
queries, qrels, and positive documents likely to overlap with this evaluation.

### Synthetic Data Guidance

For document-to-question generation, use non-evaluation Wikipedia passage
bundles and generate questions requiring a bridge relation, comparison, or
inference step. For joint generation, create bundled encyclopedia passages with
explicit entities and relations, then ask for the final property reachable only
through the chain. Do not use Nano evaluation questions or positives as seeds.

## Example Data

| Query | Positive document |
| --- | --- |
| Which film has the director who is older than the other, Women'S Weapons or She Wants Me? (89 chars) | Passage 1: Scotty Fox Scott Fox is a pornographic film director who is a member of the AVN Hall of Fame. Awards 1992 AVN Award – Best Director, Video (The Cockateer) 1995 AVN Hall of Fame inductee Passage 2: Elliot Silverstei ... [truncated 225 chars](16726 chars) |
| Where did the director of film Crd (Film) study? (48 chars) | Passage 1: Peter Levin Peter Levin is an American director of film, television and theatre. Career Since 1967, Levin has amassed a large number of credits directing episodic television and television films. Some of his televi ... [truncated 225 chars](27463 chars) |
| Who is the mother-in-law of Queen Insun? (40 chars) | Passage 1: Maria Thins Maria Thins (c. 1593 – 27 December 1680) was the mother-in-law of Johannes Vermeer and a member of the Gouda Thins family. She was raised in a devout Dutch Catholic family with two sisters and a brother ... [truncated 225 chars](43300 chars) |
| What is the place of birth of Frankie Bridge's husband? (55 chars) | Passage 1: Wayne Bridge Wayne Michael Bridge (born 5 August 1980) is an English former professional footballer who played as a left back. A graduate of the Southampton academy, he made his debut in 1998 and would go on to mak ... [truncated 225 chars](55577 chars) |
| Where did Elisabeth Zu Fürstenberg's husband die? (49 chars) | Passage 1: Virginia von Fürstenberg Princess Virginia Maria Clara von und zu Fürstenberg (Virginia Maria Clara Prinzessin von und zu Fürstenberg; 5 October 1974 – 10 May 2023) was an Italian artist, poet, filmmaker, and fashi ... [truncated 225 chars](39248 chars) |

## Dataset Information

| Field | Value |
| --- | --- |
| Nano set | NanoLongEmbed |
| Backing dataset | NanoLongEmbed |
| Task / split | Nano2WikiMultihopQA |
| Hugging Face dataset | [hakari-bench/NanoLongEmbed](https://huggingface.co/datasets/hakari-bench/NanoLongEmbed) |
| Language | en |
| Category | natural_language |
| Queries | 200 |
| Documents | 300 |
| Positive qrels | 200 |
| BM25 nDCG@10 | 0.9503 |
| BM25 hit@10 | 0.9800 |
| BM25 Recall@100 | 0.9900 |
| BM25 candidate subset | top-500 (`bm25`) |
| Dense nDCG@10 | 0.8400 |
| Dense hit@10 | 0.9050 |
| Dense Recall@100 | 0.9650 |
| Dense candidate subset | top-500 (`harrier_oss_v1_270m`) |
| Reranking hybrid nDCG@10 | 0.9111 |
| Reranking hybrid hit@10 | 0.9550 |
| Reranking hybrid Recall@100 | 1.0000 |
| Reranking hybrid candidate subset | top-100 plus optional rank-101 safeguard (`reranking_hybrid`) |
| Reranking hybrid candidates / query | 100 |
| Reranking hybrid safeguard rows | 0 |
| Query length avg chars | 67.52 |
| Document length avg chars | 37445.60 |

### Public Sources

- [Constructing A Multi-hop QA Dataset for Comprehensive Evaluation of Reasoning Steps](https://arxiv.org/abs/2011.01060); 2020; Xanh Ho et al.; DOI: `10.18653/v1/2020.coling-main.580`.
- [LongEmbed: Extending Embedding Models for Long Context Retrieval](https://arxiv.org/abs/2404.12096); 2024; Dawei Zhu et al.; DOI: `10.18653/v1/2024.emnlp-main.47`.
- [dwzhu/LongEmbed dataset card](https://huggingface.co/datasets/dwzhu/LongEmbed).

### Hugging Face Links

- Nano dataset: [hakari-bench/NanoLongEmbed](https://huggingface.co/datasets/hakari-bench/NanoLongEmbed)
- Source dataset: [dwzhu/LongEmbed](https://huggingface.co/datasets/dwzhu/LongEmbed)

### Source Reference Table

| Title | Year | Type | URL |
| --- | ---: | --- | --- |
| Constructing A Multi-hop QA Dataset for Comprehensive Evaluation of Reasoning Steps | 2020 | arXiv paper | https://arxiv.org/abs/2011.01060 |
| LongEmbed: Extending Embedding Models for Long Context Retrieval | 2024 | arXiv paper | https://arxiv.org/abs/2404.12096 |
| dwzhu/LongEmbed | 2024 | dataset card | https://huggingface.co/datasets/dwzhu/LongEmbed |

## Machine-Readable Metadata

<!-- benchmark-task-metadata:v1 -->

```yaml
benchmark_task_metadata:
  schema_version: 1
  document_status: first_pass
  nano_set: NanoLongEmbed
  backing_dataset: NanoLongEmbed
  dataset_id: hakari-bench/NanoLongEmbed
  task_name: Nano2WikiMultihopQA
  split_name: Nano2WikiMultihopQA
  language: en
  category: natural_language
  document_path: docs/benchmark_tasks/NanoLongEmbed/Nano2WikiMultihopQA.md
  source_research:
    primary_source_type: task_paper
    paper_pdf_or_html_checked: true
    no_paper_note: null
  counts:
    queries: 200
    documents: 300
    positive_qrels: 200
  positives_per_query:
    average: 1.0
    min: 1
    median: 1.0
    max: 1
    multi_positive_queries: 0
    multi_positive_query_percent: 0.0
  text_stats_chars:
    query_mean: 67.515
    document_mean: 37445.60333333333
  bm25:
    ndcg_at_10: 0.9502725395716047
    hit_at_10: 0.98
    source: dataset_candidate_subset
  learning:
    original_train_split: available
    evaluation_split_origin: test
    train_eval_overlap_audit: not_audited
    leakage_note: exclude 2WikiMultiHopQA test data, Nano queries, qrels, and positive
      passage bundles likely to overlap with this evaluation
    useful_training_data:
    - non-overlapping 2WikiMultiHopQA train examples
    - HotpotQA-style multi-hop retrieval pairs
    - Wikipedia entity-linking retrieval pairs
    - hard negatives sharing one bridge entity but not the full reasoning chain
    synthetic_data:
      document_generation: bundled Wikipedia-style passages with explicit entities,
        relations, bridge entities, and distractor passages
      question_generation: multi-hop questions requiring comparison, inference, compositional,
        or bridge-comparison reasoning
      answerability: the answer should require evidence from the linked passage bundle
        rather than one isolated entity mention
    multi_positive_training: single_positive_question_document_focus
  links:
    nano_dataset: https://huggingface.co/datasets/hakari-bench/NanoLongEmbed
    source_urls:
    - label: 2WikiMultiHopQA arXiv
      url: https://arxiv.org/abs/2011.01060
    - label: LongEmbed arXiv
      url: https://arxiv.org/abs/2404.12096
    - label: dwzhu/LongEmbed
      url: https://huggingface.co/datasets/dwzhu/LongEmbed
    source_notes: []
  references:
  - title: Constructing A Multi-hop QA Dataset for Comprehensive Evaluation of Reasoning
      Steps
    url: https://arxiv.org/abs/2011.01060
    year: 2020
    doi: 10.18653/v1/2020.coling-main.580
    is_paper: true
    source_confidence: definitive_paper_link
  - title: 'LongEmbed: Extending Embedding Models for Long Context Retrieval'
    url: https://arxiv.org/abs/2404.12096
    year: 2024
    doi: 10.18653/v1/2024.emnlp-main.47
    is_paper: true
    source_confidence: definitive_paper_link
  candidate_subsets:
    bm25:
      config: bm25
      label: BM25
      source: dataset_candidate_subset
      top_k: 500
      ndcg_at_10: 0.9502725396
      hit_at_10: 0.98
      recall_at_100: 0.99
      candidate_count_min: 300
      candidate_count_max: 300
      candidate_count_mean: 300.0
      query_count: 200
      query_coverage: 1.0
      relevant_coverage_at_100: 0.99
    dense:
      config: harrier_oss_v1_270m
      label: Dense
      source: dataset_candidate_subset
      top_k: 500
      ndcg_at_10: 0.8400424577
      hit_at_10: 0.905
      recall_at_100: 0.965
      candidate_count_min: 300
      candidate_count_max: 300
      candidate_count_mean: 300.0
      query_count: 200
      query_coverage: 1.0
      relevant_coverage_at_100: 0.965
    reranking_hybrid:
      config: reranking_hybrid
      label: Reranking hybrid
      source: dataset_candidate_subset
      top_k: 100
      ndcg_at_10: 0.9110949311
      hit_at_10: 0.955
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
