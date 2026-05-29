# NanoMTEB-Spanish / spanish_passage_s2_s

## Overview

`spanish_passage_s2_s` is the passage/sentence-level version of the Spanish
Passage Retrieval health dataset. Queries are Spanish consumer-health
questions, and documents are short relevant passages extracted from Spanish
health web pages. The retriever must rank concise answer-bearing passages.

## Details

### What the Original Data Measures

The [Spanish Passage Retrieval dataset page](https://mklab.iti.gr/results/spanish-passage-retrieval-dataset/)
describes Spanish health information needs about baby care, vaccination, and
low back pain, with 167 natural language questions and manual passage-level
relevance assessments. The page distinguishes document-level relevance from
passage-level relevance with start and end character offsets.

The S2S variant uses the short relevant passages as the corpus. This makes the
retrieval unit closer to a direct answer paragraph or sentence than a full web
document.

### Observed Data Profile

The Nano split has 167 queries, 250 short passages, and 1,228 positive qrels.
Queries average 67.56 characters and passages average 442.43 characters. Like
S2P, almost every query is multi-positive: 165 queries have more than one
positive passage.

Sampled positives discuss workplace changes for lumbago, causes of back
injury, breastfeeding frequency, pediatric checkups, and newborn weight.

### BM25 Difficulty

Using the dataset-provided BM25 candidate column, BM25 reaches nDCG@10 =
0.4893 and hit@10 = 0.8922. The hit rate matches S2P, but the smaller corpus
and shorter answer passages change the ranking problem: exact medical terms
help, while paraphrases such as `darle el pecho` versus `amamantar` still
matter.

### Training Data That May Help

Useful data includes non-overlapping Spanish medical FAQ passages,
question-answer sentence retrieval, and multi-positive consumer-health
retrieval examples. Avoid training on the PRES evaluation questions, qrels, or
passage text used in Nano.

### Synthetic Data Guidance

Generate Spanish health questions and several answer passages per question.
Passages should be concise, medically grounded, and written for lay readers.
Include paraphrases and near-duplicate questions so models learn to retrieve
all valid passages rather than one exact lexical match.

## Example Data

| Query | Positive document |
| --- | --- |
| ¿Cuáles son los beneficios de la leche materna? (47 chars) | En la misma se reconoce que la lactancia materna es el mejor modo de proporcionar al recién nacido los nutrientes que necesita durante los primeros meses de vida. (162 chars) |
| ¿Cuándo debo introducir alimentos complementarios aparte de la lactancia materna? (81 chars) | Durante los primeros 6 meses de vida el bebé solamente necesita tomar leche materna. Es recomendable utilizar la edad corregida para comenzar a introducir el resto de alimentos, individualizando según las necesidades. No es c ... [truncated 225 chars](314 chars) |
| ¿Tendría que darle el pecho a mi bebé siempre que me lo pida? (61 chars) | Durante el primer mes de vida, su recién nacido debería alimentarse entre ocho y 12 veces al día. (97 chars) |
| ¿Cuáles son las vacunas por las que no tengo que pagar? (55 chars) | Vacunas sistemáticas financiadas, las que todos los niños en España reciben de forma universal, que incluye las vacunas oficiales ofertadas gratuitamente por cada una de las CC. AA. Se incluyen las siguientes: hepatitis B, di ... [truncated 225 chars](539 chars) |
| Me gustaría saber más sobre la vacunación para la prevención de enfermedades infecciosas (88 chars) | Actualmente, los niños en los Estados Unidos reciben vacunas rutinariamente que los protegen de más de una docena de enfermedades como sarampión, polio, tétanos, difteria y tos ferina. (184 chars) |

## Dataset Information

| Field | Value |
| --- | --- |
| Nano set | NanoMTEB-Spanish |
| Backing dataset | NanoMTEB-Spanish |
| Task / split | spanish_passage_s2_s |
| Hugging Face dataset | [hakari-bench/NanoMTEB-Spanish](https://huggingface.co/datasets/hakari-bench/NanoMTEB-Spanish) |
| Language | es |
| Category | natural_language |
| Queries | 167 |
| Documents | 250 |
| Positive qrels | 1228 |
| Avg positives / query | 7.35 |
| Positives per query (min / median / max) | 1 / 6 / 20 |
| Queries with multiple positives | 165 (98.80%) |
| BM25 nDCG@10 | 0.5458 |
| BM25 hit@10 | 0.9401 |
| BM25 Recall@100 | 0.9438 |
| BM25 candidate subset | top-500 (`bm25`) |
| Dense nDCG@10 | 0.6398 |
| Dense hit@10 | 0.9701 |
| Dense Recall@100 | 0.9902 |
| Dense candidate subset | top-500 (`harrier_oss_v1_270m`) |
| Reranking hybrid nDCG@10 | 0.6333 |
| Reranking hybrid hit@10 | 0.9701 |
| Reranking hybrid Recall@100 | 0.9919 |
| Reranking hybrid candidate subset | top-100 plus optional rank-101 safeguard (`reranking_hybrid`) |
| Reranking hybrid candidates / query | 100 |
| Reranking hybrid safeguard rows | 0 |
| Query length avg chars | 67.56 |
| Document length avg chars | 442.43 |

### Public Sources

- [Spanish Passage Retrieval dataset page](https://mklab.iti.gr/results/spanish-passage-retrieval-dataset/).
- [jinaai/spanish_passage_retrieval dataset card](https://huggingface.co/datasets/jinaai/spanish_passage_retrieval).
- `A Test Collection for Passage Retrieval Evaluation of Spanish Health-Related Resources`; ECIR 2019; DOI: `10.1007/978-3-030-15719-7_19`.

### Hugging Face Links

- Nano dataset: [hakari-bench/NanoMTEB-Spanish](https://huggingface.co/datasets/hakari-bench/NanoMTEB-Spanish)
- Source dataset: [mteb/SpanishPassageRetrievalS2S](https://huggingface.co/datasets/mteb/SpanishPassageRetrievalS2S)

### Source Reference Table

| Title | Year | Type | URL |
| --- | ---: | --- | --- |
| A Test Collection for Passage Retrieval Evaluation of Spanish Health-Related Resources | 2019 | paper | https://doi.org/10.1007/978-3-030-15719-7_19 |
| Spanish Passage Retrieval dataset (PRES) | 2019 | project page | https://mklab.iti.gr/results/spanish-passage-retrieval-dataset/ |
| jinaai/spanish_passage_retrieval | 2025 | dataset card | https://huggingface.co/datasets/jinaai/spanish_passage_retrieval |

## Machine-Readable Metadata

<!-- benchmark-task-metadata:v1 -->

```yaml
benchmark_task_metadata:
  schema_version: 1
  document_status: first_pass
  nano_set: NanoMTEB-Spanish
  backing_dataset: NanoMTEB-Spanish
  dataset_id: hakari-bench/NanoMTEB-Spanish
  task_name: spanish_passage_s2_s
  split_name: spanish_passage_s2_s
  language: es
  category: natural_language
  document_path: docs/benchmark_tasks/NanoMTEB-Spanish/spanish_passage_s2_s.md
  source_research:
    primary_source_type: project_page
    paper_pdf_or_html_checked: false
    no_paper_note: ECIR 2019 paper metadata was confirmed, but only the public project
      page and dataset cards were inspected for construction details
  counts:
    queries: 167
    documents: 250
    positive_qrels: 1228
  positives_per_query:
    average: 7.3532934131736525
    min: 1
    median: 6
    max: 20
    multi_positive_queries: 165
    multi_positive_query_percent: 98.80239520958084
  text_stats_chars:
    query_mean: 67.55688622754491
    document_mean: 442.432
  bm25:
    ndcg_at_10: 0.5458057826871833
    hit_at_10: 0.9401197604790419
    source: dataset_candidate_subset
  learning:
    original_train_split: not_found
    evaluation_split_origin: test
    train_eval_overlap_audit: not_audited
    leakage_note: exclude PRES evaluation questions, qrels, and Spanish health passages
      likely to overlap with Nano
    useful_training_data:
    - Spanish medical FAQ passage retrieval pairs
    - consumer-health question-answer sentence pairs
    - multi-positive Spanish health retrieval examples
    - paraphrase-rich baby care, vaccination, and low back pain data
    synthetic_data:
      document_generation: concise Spanish health answer passages for lay readers
      question_generation: Spanish consumer-health questions with paraphrases and
        topic variants
      answerability: each positive passage should explicitly answer the information
        need
    multi_positive_training: multi_positive_objective
  links:
    nano_dataset: https://huggingface.co/datasets/hakari-bench/NanoMTEB-Spanish
    source_urls:
    - label: Spanish Passage Retrieval dataset page
      url: https://mklab.iti.gr/results/spanish-passage-retrieval-dataset/
    - label: jinaai/spanish_passage_retrieval
      url: https://huggingface.co/datasets/jinaai/spanish_passage_retrieval
    - label: mteb/SpanishPassageRetrievalS2S
      url: https://huggingface.co/datasets/mteb/SpanishPassageRetrievalS2S
    source_notes: []
  references:
  - title: A Test Collection for Passage Retrieval Evaluation of Spanish Health-Related
      Resources
    url: https://doi.org/10.1007/978-3-030-15719-7_19
    year: 2019
    doi: 10.1007/978-3-030-15719-7_19
    is_paper: true
    source_confidence: definitive_paper_link
  candidate_subsets:
    bm25:
      config: bm25
      label: BM25
      source: dataset_candidate_subset
      top_k: 500
      ndcg_at_10: 0.5458057827
      hit_at_10: 0.9401197605
      recall_at_100: 0.9438110749
      candidate_count_min: 250
      candidate_count_max: 250
      candidate_count_mean: 250.0
      query_count: 167
      query_coverage: 1.0
      relevant_coverage_at_100: 0.9438110749
    dense:
      config: harrier_oss_v1_270m
      label: Dense
      source: dataset_candidate_subset
      top_k: 500
      ndcg_at_10: 0.6397708028
      hit_at_10: 0.9700598802
      recall_at_100: 0.990228013
      candidate_count_min: 250
      candidate_count_max: 250
      candidate_count_mean: 250.0
      query_count: 167
      query_coverage: 1.0
      relevant_coverage_at_100: 0.990228013
    reranking_hybrid:
      config: reranking_hybrid
      label: Reranking hybrid
      source: dataset_candidate_subset
      top_k: 100
      ndcg_at_10: 0.6332506097
      hit_at_10: 0.9700598802
      recall_at_100: 0.9918566775
      candidate_count_min: 100
      candidate_count_max: 100
      candidate_count_mean: 100.0
      query_count: 167
      query_coverage: 1.0
      relevant_coverage_at_100: 0.9918566775
      safeguard_positive_rows: 0
      rows_with_101_candidates: 0
```
