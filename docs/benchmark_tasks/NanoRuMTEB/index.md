# NanoRuMTEB

## Overview

NanoRuMTEB is a compact Russian retrieval group based on ruMTEB retrieval tasks.
It contains three Russian-language subtasks: MIRACL-style Wikipedia passage
retrieval, RIA news headline-to-article retrieval, and RuBQ question-to-Wikipedia
paragraph retrieval. The group is small but covers two important Russian
retrieval modes: short question answering over Wikipedia and headline/article
matching in news.

The group is useful for checking whether a retriever handles Russian morphology,
named entities, inflection, and native-language query phrasing rather than only
English or translated retrieval.

## Details

### What the Original Group Measures

[The Russian-focused embedders' exploration: ruMTEB benchmark and Russian embedding model design](https://aclanthology.org/2025.naacl-long.12/)
introduces ruMTEB as a Russian-focused benchmark for embedding models. NanoRuMTEB
uses compact retrieval splits from that ecosystem. `miracl_ru` and `ru_bq` are
question-to-passage retrieval tasks over Russian Wikipedia-style evidence, while
`ria_news` matches Russian news headlines to article bodies from a news corpus.

These tasks stress native Russian lexical and semantic matching. The retriever
must handle inflected words, entity names, topical paraphrases, and the
difference between a short query or headline and a longer answer-bearing passage
or article.

### Subtask Coverage

- **miracl_ru:** Russian MIRACL hard-negative retrieval with short Russian
  questions and Russian Wikipedia passages.
- **ria_news:** RIA headline strings retrieving corresponding news articles from
  the Rossiya Segodnya-style news corpus.
- **ru_bq:** RuBQRetrieval question answering, where Russian questions retrieve
  Wikipedia paragraphs that support the answer.

All three tasks are Russian natural-language retrieval tasks. `miracl_ru` and
`ru_bq` contain multi-positive queries; `ria_news` is single-positive in the
current Nano qrels.

### Observed Group Profile

The task pages report 600 queries, 1,113 positive qrels, and 30,000 split-local
candidate documents. Query length averages 53.18 characters when weighted by
query count, so these are mostly short Russian questions or headlines. Documents
average 715.70 characters, with `ria_news` articles substantially longer than
the Wikipedia passages in `miracl_ru` and `ru_bq`.

The group includes 225 multi-positive queries, concentrated in the two
Wikipedia-style QA tasks. This makes the group more than a single-answer
retrieval check: a model should rank several answer-bearing passages when the
source qrels provide them.

### BM25 Difficulty

Using the dataset-provided BM25 candidate columns, NanoRuMTEB has
query-weighted BM25 nDCG@10 = 0.6067 and hit@10 = 0.7967. `ria_news` is the
strongest lexical task (nDCG@10 = 0.8479, hit@10 = 0.9150), likely because a
headline and its article body often share named entities and key event terms.

The QA-style tasks are harder: `miracl_ru` has nDCG@10 = 0.4590 and `ru_bq` has
0.5132. Short natural-language questions do not always repeat the exact phrasing
of the answer passage, and Russian morphology can make surface matching less
direct. Strong models should improve these tasks by connecting entity,
paraphrase, and answer evidence beyond raw term overlap.

### Training Data That May Help

Useful training data includes Russian MIRACL or Wikipedia question-passage
pairs, RuBQ-style QA retrieval data, Russian news headline-to-article pairs, and
hard negatives mined from same-topic Russian passages. Native Russian training
data is preferable to English-only data translated after the fact.

Training should exclude NanoRuMTEB evaluation queries, qrels, and positive
documents. The `ria_news` and `ru_bq` splits come from source test/evaluation
data in the metadata, so overlap audits are important before using public source
datasets for training.

### Synthetic Data Guidance

Synthetic data should be written in Russian. For Wikipedia-style tasks, generate
Russian passages first, then create short answerable questions whose evidence is
explicit in those passages. For news retrieval, generate article bodies and
headline-like queries with matching events, entities, dates, and locations.
Negatives should share entities or topic words but answer a different question
or describe a different news event.

Do not use NanoRuMTEB evaluation queries or positive documents as generation
seeds.

## Task Summary

| Task | Retrieval focus | Queries | Docs | Positive qrels | BM25 nDCG@10 | BM25 hit@10 | Query avg chars | Doc avg chars |
| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| [miracl_ru](miracl_ru.md) | Russian question to Wikipedia passage | 200 | 10,000 | 579 | 0.4590 | 0.7750 | 45.37 | 517.26 |
| [ria_news](ria_news.md) | Russian headline to news article | 200 | 10,000 | 200 | 0.8479 | 0.9150 | 61.99 | 1,145.34 |
| [ru_bq](ru_bq.md) | Russian open-domain question to Wikipedia paragraph | 200 | 10,000 | 334 | 0.5132 | 0.7000 | 52.20 | 484.49 |

## Dataset Information

| Field | Value |
| --- | --- |
| Nano set | NanoRuMTEB |
| Backing dataset | NanoRuMTEB |
| Hugging Face dataset | [hakari-bench/NanoRuMTEB](https://huggingface.co/datasets/hakari-bench/NanoRuMTEB) |
| Language | ru |
| Category | natural language |
| Subtasks | 3 |
| Total queries | 600 |
| Split-local documents | 30,000 |
| Positive qrels | 1,113 |
| Average positives / query | 1.86 |
| Queries with multiple positives | 225 |
| Query-weighted BM25 nDCG@10 | 0.7089 |
| Query-weighted BM25 hit@10 | 0.8717 |
| Query-weighted BM25 Recall@100 | 0.9373 |
| Query-weighted Dense nDCG@10 | 0.8718 |
| Query-weighted Dense hit@10 | 0.9550 |
| Query-weighted Dense Recall@100 | 0.9559 |
| Query-weighted Reranking hybrid nDCG@10 | 0.7895 |
| Query-weighted Reranking hybrid hit@10 | 0.9150 |
| Query-weighted Reranking hybrid Recall@100 | 0.9880 |
| Mean query length | 53.18 chars, weighted by query count |
| Mean document length | 715.70 chars, weighted by split-local document count |

### Public Sources

- [The Russian-focused embedders' exploration: ruMTEB benchmark and Russian embedding model design](https://aclanthology.org/2025.naacl-long.12/); 2025; DOI: `10.18653/v1/2025.naacl-long.12`.
- [MIRACL](http://miracl.ai/); source project page.
- [mteb/RiaNewsRetrieval_test_top_250_only_w_correct-v2](https://huggingface.co/datasets/mteb/RiaNewsRetrieval_test_top_250_only_w_correct-v2); source dataset.
- [ai-forever/rubq-retrieval](https://huggingface.co/datasets/ai-forever/rubq-retrieval); source dataset.

### Hugging Face Links

- Nano dataset: [hakari-bench/NanoRuMTEB](https://huggingface.co/datasets/hakari-bench/NanoRuMTEB)
- Source dataset: [mteb/MIRACLRetrievalHardNegatives](https://huggingface.co/datasets/mteb/MIRACLRetrievalHardNegatives)
- Source dataset: [mteb/RiaNewsRetrieval_test_top_250_only_w_correct-v2](https://huggingface.co/datasets/mteb/RiaNewsRetrieval_test_top_250_only_w_correct-v2)
- Source dataset: [ai-forever/rubq-retrieval](https://huggingface.co/datasets/ai-forever/rubq-retrieval)

### Source Reference Table

| Title | Year | Type | URL |
| --- | ---: | --- | --- |
| The Russian-focused embedders' exploration: ruMTEB benchmark and Russian embedding model design | 2025 | benchmark paper | https://aclanthology.org/2025.naacl-long.12/ |
| MIRACLRetrievalHardNegatives.v2 source reference | unknown | source project page | http://miracl.ai/ |
| mteb/RiaNewsRetrieval_test_top_250_only_w_correct-v2 Hugging Face dataset | unknown | source dataset | https://huggingface.co/datasets/mteb/RiaNewsRetrieval_test_top_250_only_w_correct-v2 |
| ai-forever/rubq-retrieval Hugging Face dataset | unknown | source dataset | https://huggingface.co/datasets/ai-forever/rubq-retrieval |

## Machine-Readable Metadata

<!-- benchmark-task-group-metadata:v1 -->

```yaml
benchmark_task_group_metadata:
  schema_version: 1
  document_status: reviewed_manual
  nano_set: NanoRuMTEB
  backing_dataset: NanoRuMTEB
  dataset_id: hakari-bench/NanoRuMTEB
  language: ru
  category: natural_language
  document_path: docs/benchmark_tasks/NanoRuMTEB/index.md
  source_research:
    primary_source_type: benchmark_paper
    paper_pdf_or_html_checked: true
    no_paper_note: null
  counts:
    tasks: 3
    queries: 600
    split_local_documents: 30000
    positive_qrels: 1113
  positives_per_query:
    average: 1.855
    min: 1
    median: 1.0
    max: 9
    multi_positive_tasks: 2
    multi_positive_queries: 225
  text_stats_chars:
    query_mean_weighted_by_queries: 53.181666666666665
    document_mean_weighted_by_documents: 715.6965333333334
  bm25:
    ndcg_at_10_query_weighted: 0.7089462998
    hit_at_10_query_weighted: 0.8716666667
    source: dataset_candidate_subset
    strongest_task_by_ndcg_at_10: ria_news
    weakest_task_by_ndcg_at_10: miracl_ru
  tasks:
  - name: miracl_ru
    path: docs/benchmark_tasks/NanoRuMTEB/miracl_ru.md
    retrieval_focus: russian_question_to_wikipedia_passage
    queries: 200
    documents: 10000
    positive_qrels: 579
    bm25_ndcg_at_10: 0.459
    bm25_hit_at_10: 0.775
  - name: ria_news
    path: docs/benchmark_tasks/NanoRuMTEB/ria_news.md
    retrieval_focus: russian_headline_to_news_article
    queries: 200
    documents: 10000
    positive_qrels: 200
    bm25_ndcg_at_10: 0.8479
    bm25_hit_at_10: 0.915
  - name: ru_bq
    path: docs/benchmark_tasks/NanoRuMTEB/ru_bq.md
    retrieval_focus: russian_question_to_wikipedia_paragraph
    queries: 200
    documents: 10000
    positive_qrels: 334
    bm25_ndcg_at_10: 0.5132
    bm25_hit_at_10: 0.7
  learning:
    leakage_note: exclude NanoRuMTEB evaluation queries, qrels, and positive documents;
      audit ruMTEB source dev/test overlap before training
    useful_training_data:
    - Russian MIRACL or Wikipedia question-passage pairs
    - RuBQ-style Russian QA retrieval data
    - Russian news headline-to-article pairs
    - hard negatives from same-topic Russian passages
    synthetic_data:
      document_generation: Russian Wikipedia-style passages and news articles with
        entities, dates, and evidence
      question_generation: native Russian questions or headlines grounded in the generated
        documents
      answerability: positives must answer the Russian query or describe the same
        news event
    multi_positive_training: multi_positive_objective
  links:
    nano_dataset: https://huggingface.co/datasets/hakari-bench/NanoRuMTEB
    source_urls:
    - label: ruMTEB paper
      url: https://aclanthology.org/2025.naacl-long.12/
    - label: mteb/MIRACLRetrievalHardNegatives
      url: https://huggingface.co/datasets/mteb/MIRACLRetrievalHardNegatives
    - label: mteb/RiaNewsRetrieval_test_top_250_only_w_correct-v2
      url: https://huggingface.co/datasets/mteb/RiaNewsRetrieval_test_top_250_only_w_correct-v2
    - label: ai-forever/rubq-retrieval
      url: https://huggingface.co/datasets/ai-forever/rubq-retrieval
  references:
  - title: 'The Russian-focused embedders'' exploration: ruMTEB benchmark and Russian
      embedding model design'
    url: https://aclanthology.org/2025.naacl-long.12/
    year: 2025
    doi: 10.18653/v1/2025.naacl-long.12
    is_paper: true
    source_confidence: definitive_paper_link
  candidate_subsets:
    bm25:
      query_weighted_ndcg_at_10: 0.7089462998
      query_weighted_hit_at_10: 0.8716666667
      query_weighted_recall_at_100: 0.9372780346
      source: dataset_candidate_subset
    dense:
      query_weighted_ndcg_at_10: 0.8718316974
      query_weighted_hit_at_10: 0.955
      query_weighted_recall_at_100: 0.9558936531
      source: dataset_candidate_subset
    reranking_hybrid:
      query_weighted_ndcg_at_10: 0.7894815532
      query_weighted_hit_at_10: 0.915
      query_weighted_recall_at_100: 0.987953523
      source: dataset_candidate_subset
```
