# NanoMMTEB-v2 / lembpasskey

## Overview

`lembpasskey` is a long-context passkey retrieval task from LongEmbed. Queries
ask for the passkey associated with a named person, and each document is a long
repeated filler passage containing the target passkey statement. The task tests
whether an embedding model can preserve a small fact inside a long document.

## Details

### What the Original Data Measures

[LongEmbed: Extending Embedding Models for Long Context Retrieval](https://arxiv.org/abs/2404.12096)
introduces passkey and needle retrieval tasks with documents of controlled
lengths and target information inserted at varying positions. The paper uses
these tasks to test whether retrieval embeddings can process long inputs rather
than only short passages.

### Observed Data Profile

The split has 100 queries, 100 documents, and 100 positive qrels. Each query has
one positive. Queries are short English prompts averaging 37.80 characters.
Documents average 28,060.87 characters and range from short to very long
haystacks, with repeated filler text surrounding a passkey sentence.

### BM25 Difficulty

Using the dataset-provided BM25 candidate column, BM25 reaches nDCG@10 = 0.9963
and hit@10 = 1.0000. The lexical cue is usually explicit: the person's name and
the word `passkey` appear in the target document. The benchmark is therefore
less about lexical ambiguity and more about whether embedding systems retain the
needle when the document is long.

### Training Data That May Help

Useful training data includes long-context retrieval, needle-in-haystack
retrieval, synthetic passkey retrieval, and QA pairs where the answer-bearing
fact appears at varied positions in long documents. Training should avoid the
same generated names, passkeys, and evaluation documents.

### Synthetic Data Guidance

Generate long documents with neutral filler plus one or more explicit facts at
controlled positions. Questions should request a fact tied to a named entity.
Include hard negatives with nearby names or different passkeys so the model must
bind the requested entity to the correct fact, not just find generic filler.

## Example Data

| Query | Positive document |
| --- | --- |
| what is the passkey for Douglas Alfaro? (39 chars) | The grass is green. Douglas Alfaro's pass key is 6699. Remember it. 6699 is the pass key for Douglas Alfaro. The sky is blue. The sun is yellow. Here we go. There and back again. The grass is green. The sky is blue. The sun i ... [truncated 225 chars](1786 chars) |
| what is the passkey for Declan Horton? (38 chars) | The grass is green. The sky is blue. The sun is yellow. Here we go. There and back again. The grass is green. The sky is blue. The sun is yellow. Here we go. There and back again. The grass is green. The sky is blue. The sun ... [truncated 225 chars](58175 chars) |
| what is the passkey for Denisse Wilcox? (39 chars) | The grass is green. The sky is blue. The sun is yellow. Here we go. There and back again. The grass is green. The sky is blue. The sun is yellow. Here we go. There and back again. The grass is green. The sky is blue. The sun ... [truncated 225 chars](3610 chars) |
| what is the passkey for Cheyenne Jarvis? (40 chars) | The grass is green. The sky is blue. The sun is yellow. Here we go. There and back again. The grass is green. The sky is blue. The sun is yellow. Here we go. There and back again. The grass is green. The sky is blue. The sun ... [truncated 225 chars](29076 chars) |
| what is the passkey for Zyaire Sweeney? (39 chars) | The grass is green. The sky is blue. The sun is yellow. Here we go. There and back again. The grass is green. The sky is blue. The sun is yellow. Here we go. There and back again. The grass is green. The sky is blue. The sun ... [truncated 225 chars](7243 chars) |

## Dataset Information

| Field | Value |
| --- | --- |
| Nano set | NanoMMTEB-v2 |
| Backing dataset | NanoMMTEB-v2 |
| Task / split | lembpasskey |
| Hugging Face dataset | [hakari-bench/NanoMMTEB-v2](https://huggingface.co/datasets/hakari-bench/NanoMMTEB-v2) |
| Source dataset | [mteb/LEMBPasskeyRetrieval](https://huggingface.co/datasets/mteb/LEMBPasskeyRetrieval) |
| Language | en |
| Category | natural_language |
| Queries | 100 |
| Documents | 100 |
| Positive qrels | 100 |
| BM25 nDCG@10 | 0.9963 |
| BM25 hit@10 | 1.0000 |
| BM25 Recall@100 | 1.0000 |
| BM25 candidate subset | top-500 (`bm25`) |
| Dense nDCG@10 | 0.8463 |
| Dense hit@10 | 0.8500 |
| Dense Recall@100 | 1.0000 |
| Dense candidate subset | top-500 (`harrier_oss_v1_270m`) |
| Reranking hybrid nDCG@10 | 0.8525 |
| Reranking hybrid hit@10 | 0.8700 |
| Reranking hybrid Recall@100 | 1.0000 |
| Reranking hybrid candidate subset | top-100 plus optional rank-101 safeguard (`reranking_hybrid`) |
| Reranking hybrid candidates / query | 100 |
| Reranking hybrid safeguard rows | 0 |
| Query length avg chars | 37.80 |
| Document length avg chars | 28060.87 |

### Public Sources

- [LongEmbed: Extending Embedding Models for Long Context Retrieval](https://arxiv.org/abs/2404.12096).
- [dwzhu/LongEmbed](https://huggingface.co/datasets/dwzhu/LongEmbed).
- [mteb/LEMBPasskeyRetrieval](https://huggingface.co/datasets/mteb/LEMBPasskeyRetrieval).

### Hugging Face Links

- Nano dataset: [hakari-bench/NanoMMTEB-v2](https://huggingface.co/datasets/hakari-bench/NanoMMTEB-v2)
- Source dataset: [mteb/LEMBPasskeyRetrieval](https://huggingface.co/datasets/mteb/LEMBPasskeyRetrieval)
- Source collection: [dwzhu/LongEmbed](https://huggingface.co/datasets/dwzhu/LongEmbed)

### Source Reference Table

| Title | Year | Type | URL |
| --- | ---: | --- | --- |
| LongEmbed: Extending Embedding Models for Long Context Retrieval | 2024 | task paper | https://arxiv.org/abs/2404.12096 |
| dwzhu/LongEmbed | 2024 | dataset card | https://huggingface.co/datasets/dwzhu/LongEmbed |
| mteb/LEMBPasskeyRetrieval | 2024 | dataset card | https://huggingface.co/datasets/mteb/LEMBPasskeyRetrieval |

## Machine-Readable Metadata

<!-- benchmark-task-metadata:v1 -->

```yaml
benchmark_task_metadata:
  schema_version: 1
  document_status: first_pass
  nano_set: NanoMMTEB-v2
  backing_dataset: NanoMMTEB-v2
  dataset_id: hakari-bench/NanoMMTEB-v2
  task_name: lembpasskey
  split_name: lembpasskey
  language: en
  category: natural_language
  document_path: docs/benchmark_tasks/NanoMMTEB-v2/lembpasskey.md
  source_research:
    primary_source_type: task_paper
    paper_pdf_or_html_checked: true
    no_paper_note: null
  counts:
    queries: 100
    documents: 100
    positive_qrels: 100
  positives_per_query:
    average: 1.0
    min: 1
    median: 1.0
    max: 1
    multi_positive_queries: 0
    multi_positive_query_percent: 0.0
  text_stats_chars:
    query_mean: 37.8
    document_mean: 28060.87
  bm25:
    ndcg_at_10: 0.9963092975357145
    hit_at_10: 1.0
    source: dataset_candidate_subset
  learning:
    original_train_split: available
    evaluation_split_origin: test_256+test_512+test_1024+test_2048+test_4096+test_8192+test_16384+test_32768
    train_eval_overlap_audit: not_audited
    leakage_note: do not train on this Nano split's generated names, passkeys, qrels,
      or positive documents
    useful_training_data:
    - long-context retrieval examples
    - needle-in-haystack retrieval
    - synthetic passkey retrieval with non-overlapping names
    - QA over long documents with varied answer positions
    synthetic_data:
      document_generation: long filler documents with entity-bound passkey facts at
        controlled positions
      question_generation: short questions asking for a named entity's passkey
      answerability: positive document must contain the requested entity-passkey association
    multi_positive_training: single_positive_question_document_focus
  links:
    nano_dataset: https://huggingface.co/datasets/hakari-bench/NanoMMTEB-v2
    source_urls:
    - label: LongEmbed arXiv
      url: https://arxiv.org/abs/2404.12096
    - label: dwzhu/LongEmbed
      url: https://huggingface.co/datasets/dwzhu/LongEmbed
    - label: mteb/LEMBPasskeyRetrieval
      url: https://huggingface.co/datasets/mteb/LEMBPasskeyRetrieval
    source_notes: []
  references:
  - title: 'LongEmbed: Extending Embedding Models for Long Context Retrieval'
    url: https://arxiv.org/abs/2404.12096
    year: 2024
    is_paper: true
    source_confidence: definitive_paper_link
  candidate_subsets:
    bm25:
      config: bm25
      label: BM25
      source: dataset_candidate_subset
      top_k: 500
      ndcg_at_10: 0.9963092975
      hit_at_10: 1.0
      recall_at_100: 1.0
      candidate_count_min: 100
      candidate_count_max: 100
      candidate_count_mean: 100.0
      query_count: 100
      query_coverage: 1.0
      relevant_coverage_at_100: 1.0
    dense:
      config: harrier_oss_v1_270m
      label: Dense
      source: dataset_candidate_subset
      top_k: 500
      ndcg_at_10: 0.8463092975
      hit_at_10: 0.85
      recall_at_100: 1.0
      candidate_count_min: 100
      candidate_count_max: 100
      candidate_count_mean: 100.0
      query_count: 100
      query_coverage: 1.0
      relevant_coverage_at_100: 1.0
    reranking_hybrid:
      config: reranking_hybrid
      label: Reranking hybrid
      source: dataset_candidate_subset
      top_k: 100
      ndcg_at_10: 0.8524742463
      hit_at_10: 0.87
      recall_at_100: 1.0
      candidate_count_min: 100
      candidate_count_max: 100
      candidate_count_mean: 100.0
      query_count: 100
      query_coverage: 1.0
      relevant_coverage_at_100: 1.0
      safeguard_positive_rows: 0
      rows_with_101_candidates: 0
```
