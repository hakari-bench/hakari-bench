# NanoMTEB-v2 / hotpot_qa

## Overview

`hotpot_qa` is a multi-hop question-to-Wikipedia retrieval task derived from
HotpotQA. Queries are natural-language questions, and positives are supporting
Wikipedia passages needed to answer them.

## Details

### What the Original Data Measures

[HotpotQA](https://arxiv.org/abs/1809.09600) was introduced for explainable
multi-hop question answering over Wikipedia, with supporting facts annotated for
questions that require combining evidence. The MTEB retrieval version evaluates
retrieval of those supporting passages, using hard negatives in the source
dataset. MTEB reports retrieval tasks with corpus, queries, qrels, and nDCG@10.

### Observed Data Profile

The split has 200 queries, 10,000 documents, and 400 positive qrels. Every query
has exactly two positives, matching the multi-hop character of HotpotQA. Queries
average 95.83 characters, while documents average 421.20 characters and are
short Wikipedia-style passages.

### BM25 Difficulty

Using the dataset-provided BM25 candidate column, BM25 reaches nDCG@10 =
0.8891 and hit@10 = 1.0000. It ranks 190 queries with a positive first, and the
median best positive rank is 1. The Nano sample is very friendly to lexical
retrieval because questions usually name one or both bridge entities.

### Training Data That May Help

Useful data includes HotpotQA supporting-fact pairs, multi-hop Wikipedia QA,
entity-linking retrieval data, and hard negatives with the same named entities
but missing one hop.

### Synthetic Data Guidance

Generate two-hop questions that require retrieving two supporting passages.
Keep bridge entities explicit, and create hard negatives that mention one entity
but not the relation needed for the final answer.

## Example Data

| Query | Positive document |
| --- | --- |
| The Soul of Buddha is a 1918 American silent romance film shot in a borough that is the western terminus of what? (114 chars) | The Soul of Buddha The Soul of Buddha is a 1918 American silent romance film directed by J. Gordon Edwards and starring Theda Bara, who also wrote the film's story. The film was produced by Fox Film Corporation and shot at th ... [truncated 225 chars](263 chars) |
| The lamp used in many lighthouses is similiar to this type of lamp patented in 1780 by Aimé Argand? (99 chars) | Lewis lamp The Lewis lamp is a type of light fixture used in lighthouses. It was invented by Winslow Lewis who patented the design in 1810. The primary marketing point of the Lewis lamp was that it used less than half the oil ... [truncated 225 chars](708 chars) |
| What is the shared country of ancestry between Art Laboe and Scout Tufankjian? (78 chars) | Art Laboe Art Laboe (born Arthur Egnoian on August 7, 1925) is an Armenian American disc jockey, songwriter, record producer, and radio station owner, generally credited with coining the term "Oldies But Goodies". (214 chars) |
| Sebastian Gutierrez is known for writing the screenplay for the 2003 film directed by whom? (91 chars) | Sebastian Gutierrez Sebastian Gutierrez (born September 10, 1974) is a Venezuelan film director, screenwriter and film producer. known for writing the screenplays to the films "Gothika", "Snakes on a Plane", "The Eye" and "Th ... [truncated 225 chars](354 chars) |
| When did the character on Grey's Anatomy, played by the same actor who portrayed Rev James Lawson in "Lee Daniel's The Butler", debut? (134 chars) | Jesse Williams (actor) Jesse Wesley Williams (born August 5, 1981) is an American actor, model, and activist, best known for his role as Dr. Jackson Avery on the ABC Television series "Grey's Anatomy". He also appeared in the ... [truncated 225 chars](526 chars) |

## Dataset Information

| Field | Value |
| --- | --- |
| Nano set | NanoMTEB-v2 |
| Backing dataset | NanoMTEB-v2 |
| Task / split | hotpot_qa |
| Source task | HotpotQAHardNegatives |
| Hugging Face dataset | [hakari-bench/NanoMTEB-v2](https://huggingface.co/datasets/hakari-bench/NanoMTEB-v2) |
| Source dataset | [mteb/HotpotQA_test_top_250_only_w_correct-v2](https://huggingface.co/datasets/mteb/HotpotQA_test_top_250_only_w_correct-v2) |
| Language | en |
| Category | natural_language |
| Queries | 200 |
| Documents | 10000 |
| Positive qrels | 400 |
| Positives per query | avg 2.00, min 2, median 2, max 2 |
| Multi-positive queries | 200 (100.00%) |
| BM25 nDCG@10 | 0.8891 |
| BM25 hit@10 | 1.0000 |
| Query length avg chars | 95.83 |
| Document length avg chars | 421.20 |

### Public Sources

- [HotpotQA: A Dataset for Diverse, Explainable Multi-hop Question Answering](https://arxiv.org/abs/1809.09600).
- [MTEB: Massive Text Embedding Benchmark](https://arxiv.org/abs/2210.07316).
- [mteb/HotpotQA_test_top_250_only_w_correct-v2](https://huggingface.co/datasets/mteb/HotpotQA_test_top_250_only_w_correct-v2).

### Hugging Face Links

- Nano dataset: [hakari-bench/NanoMTEB-v2](https://huggingface.co/datasets/hakari-bench/NanoMTEB-v2)
- Source dataset: [mteb/HotpotQA_test_top_250_only_w_correct-v2](https://huggingface.co/datasets/mteb/HotpotQA_test_top_250_only_w_correct-v2)

### Source Reference Table

| Title | Year | Type | URL |
| --- | ---: | --- | --- |
| HotpotQA: A Dataset for Diverse, Explainable Multi-hop Question Answering | 2018 | source task paper | https://arxiv.org/abs/1809.09600 |
| MTEB: Massive Text Embedding Benchmark | 2023 | benchmark paper | https://arxiv.org/abs/2210.07316 |
| mteb/HotpotQA_test_top_250_only_w_correct-v2 | 2024 | dataset card | https://huggingface.co/datasets/mteb/HotpotQA_test_top_250_only_w_correct-v2 |

## Machine-Readable Metadata

<!-- benchmark-task-metadata:v1 -->

```yaml
benchmark_task_metadata:
  schema_version: 1
  document_status: first_pass
  nano_set: NanoMTEB-v2
  backing_dataset: NanoMTEB-v2
  dataset_id: hakari-bench/NanoMTEB-v2
  task_name: hotpot_qa
  split_name: hotpot_qa
  source_task: HotpotQAHardNegatives
  source_dataset_id: mteb/HotpotQA_test_top_250_only_w_correct-v2
  language: en
  category: natural_language
  document_path: docs/benchmark_tasks/NanoMTEB-v2/hotpot_qa.md
  source_research:
    primary_source_type: task_paper_and_benchmark_paper
    paper_pdf_or_html_checked: true
    no_paper_note: null
  counts:
    queries: 200
    documents: 10000
    positive_qrels: 400
  positives_per_query:
    average: 2.0
    min: 2
    median: 2.0
    max: 2
    multi_positive_queries: 200
    multi_positive_query_percent: 100.0
  text_stats_chars:
    query_mean: 95.83
    document_mean: 421.1971
  bm25:
    ndcg_at_10: 0.889065539981155
    hit_at_10: 1.0
    source: dataset_bm25_column
  learning:
    original_train_split: available
    evaluation_split_origin: MTEB HotpotQA hard-negative test split
    train_eval_overlap_audit: not_audited
    leakage_note: exclude NanoMTEB-v2 hotpot_qa questions and supporting passages
    useful_training_data:
      - HotpotQA supporting-fact retrieval pairs
      - multi-hop Wikipedia QA data
      - entity bridge hard negatives
    synthetic_data:
      document_generation: short Wikipedia passages about linked entities
      question_generation: two-hop natural-language questions
      answerability: positives should include the supporting passages needed for the answer
    multi_positive_training: required
  links:
    nano_dataset: https://huggingface.co/datasets/hakari-bench/NanoMTEB-v2
    source_urls:
      - label: HotpotQA arXiv
        url: https://arxiv.org/abs/1809.09600
      - label: MTEB arXiv
        url: https://arxiv.org/abs/2210.07316
      - label: mteb/HotpotQA_test_top_250_only_w_correct-v2
        url: https://huggingface.co/datasets/mteb/HotpotQA_test_top_250_only_w_correct-v2
    source_notes: []
  references:
    - title: "HotpotQA: A Dataset for Diverse, Explainable Multi-hop Question Answering"
      url: https://arxiv.org/abs/1809.09600
      year: 2018
      is_paper: true
      source_confidence: definitive_paper_link
    - title: "MTEB: Massive Text Embedding Benchmark"
      url: https://arxiv.org/abs/2210.07316
      year: 2023
      is_paper: true
      source_confidence: definitive_paper_link
```
