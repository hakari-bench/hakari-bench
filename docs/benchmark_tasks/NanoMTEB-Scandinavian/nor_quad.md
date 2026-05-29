# NanoMTEB-Scandinavian / nor_quad

## Overview

NorQuAD was introduced as Norwegian extractive reading comprehension over
Bokmål Wikipedia and news passages. The Scandinavian retrieval adaptation turns
those QA pairs into question-to-answer retrieval: a Norwegian question must
retrieve the correct short answer string or answer-bearing snippet. In this
Nano split, many positives are names, places, dates, or numbers and nearly half
the queries have two positives, so the task is sharply different from passage
retrieval: the model must map a full question to a concise answer that may
share very little lexical context.

## Details

### What the Original Data Measures

[NorQuAD: Norwegian Question Answering Dataset](https://aclanthology.org/2023.nodalida-1.17/)
introduces the first Norwegian machine reading comprehension dataset. The paper
reports 4,752 manually created question-answer pairs from Norwegian Bokmål
Wikipedia and news passages, following an extractive QA methodology rather than
open-domain information seeking.

SEB formalizes QA datasets for retrieval by using questions as queries and
answers as corpus documents. This makes `nor_quad` closer to answer selection
than passage retrieval.

### Observed Data Profile

The Nano split has 196 Norwegian queries, 1,048 documents, and 291 positive
qrels. Queries average 48.61 characters, and documents average 214.39
characters. About 48.47% of queries have two positives. Observed positives can
be extremely short, such as names, places, dates, and numeric quantities.

The short answer format sharply changes the task from the original
reading-comprehension framing: a system must map a full question to a concise
answer string that may share little vocabulary with the question.

### BM25 Difficulty

Using the dataset-provided BM25 candidate column, BM25 reaches nDCG@10 =
0.1118 and hit@10 = 0.2143. BM25 ranks only 22 queries' positives first. Many
sampled positives appear at rank 100 because the answer text does not repeat
query words. This is one of the harder lexical retrieval tasks in this set.

### Training Data That May Help

Useful training data includes non-overlapping NorQuAD train questions, Norwegian
Wikipedia/news extractive QA pairs, and answer-selection data with short
answers. Hard negatives should include same-question-type answers, nearby dates,
and named entities from the same source domain.

### Synthetic Data Guidance

Generate Norwegian passages, write extractive questions, then use concise answer
strings as positives. Include short answers that require semantic type matching:
person, city, number, date, reason, and location. Synthetic negatives should be
plausible answers of the same type.

## Example Data

| Query | Positive document |
| --- | --- |
| Når ble euroen innført? (23 chars) | I 1999 (6 chars) |
| Hvilken bok lyver flest briter om at de har lest? (49 chars) | «Bibelen» (9 chars) |
| Hvilket land i Øst-Europa var det første til å få en ikke-kommunistisk statsminister? (85 chars) | 30 år uten Berlinmur Berlinmuren falt ikke, den ble revet av mennesker som ikke lenger ville leve bak stengsler. FOTO: GERARD MALLE/NTB SCANPIX Det heter at muren falt. Som om den tumlet over ende av utmattelse i kamp mot tid ... [truncated 225 chars](1948 chars) |
| Hva kalte romerne provinsen de lagde ut av dagens England og Wales? (67 chars) | Romersk Britannia (17 chars) |
| Hvordan var tonen til Botnan etter løpet? (41 chars) | litt mer spøkefull (18 chars) |

## Dataset Information

| Field | Value |
| --- | --- |
| Nano set | NanoMTEB-Scandinavian |
| Backing dataset | NanoMTEB-Scandinavian |
| Task / split | nor_quad |
| Hugging Face dataset | [hakari-bench/NanoMTEB-Scandinavian](https://huggingface.co/datasets/hakari-bench/NanoMTEB-Scandinavian) |
| Language | no |
| Category | natural_language |
| Queries | 196 |
| Documents | 1,048 |
| Positive qrels | 291 |
| BM25 nDCG@10 | 0.1118 |
| BM25 hit@10 | 0.2143 |
| BM25 Recall@100 | 0.2131 |
| BM25 candidate subset | top-500 (`bm25`) |
| Dense nDCG@10 | 0.2378 |
| Dense hit@10 | 0.3724 |
| Dense Recall@100 | 0.4536 |
| Dense candidate subset | top-500 (`harrier_oss_v1_270m`) |
| Reranking hybrid nDCG@10 | 0.1301 |
| Reranking hybrid hit@10 | 0.2296 |
| Reranking hybrid Recall@100 | 0.4261 |
| Reranking hybrid candidate subset | top-100 plus optional rank-101 safeguard (`reranking_hybrid`) |
| Reranking hybrid candidates / query | 100-101 |
| Reranking hybrid safeguard rows | 89 |
| Query length avg chars | 48.61 |
| Document length avg chars | 214.39 |

### Public Sources

- [The Scandinavian Embedding Benchmarks](https://arxiv.org/abs/2406.02396); 2024; Kenneth Enevoldsen et al.
- [NorQuAD: Norwegian Question Answering Dataset](https://aclanthology.org/2023.nodalida-1.17/); 2023; Sardana Ivanova et al.
- [mteb/norquad_retrieval dataset card](https://huggingface.co/datasets/mteb/norquad_retrieval).

### Hugging Face Links

- Nano dataset: [hakari-bench/NanoMTEB-Scandinavian](https://huggingface.co/datasets/hakari-bench/NanoMTEB-Scandinavian)
- Source dataset: [mteb/norquad_retrieval](https://huggingface.co/datasets/mteb/norquad_retrieval)

### Source Reference Table

| Title | Year | Type | URL |
| --- | ---: | --- | --- |
| The Scandinavian Embedding Benchmarks | 2024 | arXiv paper | https://arxiv.org/abs/2406.02396 |
| NorQuAD: Norwegian Question Answering Dataset | 2023 | ACL Anthology paper | https://aclanthology.org/2023.nodalida-1.17/ |
| mteb/norquad_retrieval | 2024 | dataset card | https://huggingface.co/datasets/mteb/norquad_retrieval |

## Machine-Readable Metadata

<!-- benchmark-task-metadata:v1 -->

```yaml
benchmark_task_metadata:
  schema_version: 1
  document_status: first_pass
  nano_set: NanoMTEB-Scandinavian
  backing_dataset: NanoMTEB-Scandinavian
  dataset_id: hakari-bench/NanoMTEB-Scandinavian
  task_name: nor_quad
  split_name: nor_quad
  language: false
  category: natural_language
  document_path: docs/benchmark_tasks/NanoMTEB-Scandinavian/nor_quad.md
  source_research:
    primary_source_type: task_paper
    paper_pdf_or_html_checked: true
    no_paper_note: null
  counts:
    queries: 196
    documents: 1048
    positive_qrels: 291
  positives_per_query:
    average: 1.4846938775510203
    min: 1
    median: 1.0
    max: 2
    multi_positive_queries: 95
    multi_positive_query_percent: 48.46938775510204
  text_stats_chars:
    query_mean: 48.607142857142854
    document_mean: 214.39312977099237
  bm25:
    ndcg_at_10: 0.11183189367748354
    hit_at_10: 0.21428571428571427
    source: dataset_candidate_subset
  learning:
    original_train_split: available
    evaluation_split_origin: test
    train_eval_overlap_audit: not_audited
    leakage_note: exclude NorQuAD test questions, Nano qrels, and answer strings in
      this split
    useful_training_data:
    - non-overlapping NorQuAD train question-answer pairs
    - Norwegian Wikipedia extractive QA pairs
    - Norwegian news QA pairs
    - short-answer answer-selection negatives
    synthetic_data:
      document_generation: concise Norwegian answer strings plus optional short evidence
        snippets
      question_generation: Norwegian wh-questions targeting person, place, date, quantity,
        and reason answers
      answerability: positive answer text should answer the question directly, even
        when lexical overlap is low
    multi_positive_training: support_multiple_valid_answers_per_question
  links:
    nano_dataset: https://huggingface.co/datasets/hakari-bench/NanoMTEB-Scandinavian
    source_urls:
    - label: Scandinavian Embedding Benchmarks
      url: https://arxiv.org/abs/2406.02396
    - label: NorQuAD paper
      url: https://aclanthology.org/2023.nodalida-1.17/
    - label: mteb/norquad_retrieval
      url: https://huggingface.co/datasets/mteb/norquad_retrieval
    source_notes: []
  references:
  - title: 'NorQuAD: Norwegian Question Answering Dataset'
    url: https://aclanthology.org/2023.nodalida-1.17/
    year: 2023
    doi: null
    is_paper: true
    source_confidence: definitive_paper_link
  candidate_subsets:
    bm25:
      config: bm25
      label: BM25
      source: dataset_candidate_subset
      top_k: 500
      ndcg_at_10: 0.1118318937
      hit_at_10: 0.2142857143
      recall_at_100: 0.2130584192
      candidate_count_min: 500
      candidate_count_max: 500
      candidate_count_mean: 500.0
      query_count: 196
      query_coverage: 1.0
      relevant_coverage_at_100: 0.2130584192
    dense:
      config: harrier_oss_v1_270m
      label: Dense
      source: dataset_candidate_subset
      top_k: 500
      ndcg_at_10: 0.2378449014
      hit_at_10: 0.3724489796
      recall_at_100: 0.4536082474
      candidate_count_min: 500
      candidate_count_max: 500
      candidate_count_mean: 500.0
      query_count: 196
      query_coverage: 1.0
      relevant_coverage_at_100: 0.4536082474
    reranking_hybrid:
      config: reranking_hybrid
      label: Reranking hybrid
      source: dataset_candidate_subset
      top_k: 100
      ndcg_at_10: 0.1300945227
      hit_at_10: 0.2295918367
      recall_at_100: 0.4261168385
      candidate_count_min: 100
      candidate_count_max: 101
      candidate_count_mean: 100.454082
      query_count: 196
      query_coverage: 1.0
      relevant_coverage_at_100: 0.4261168385
      safeguard_positive_rows: 89
      rows_with_101_candidates: 89
```
