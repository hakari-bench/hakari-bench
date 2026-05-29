# NanoRuMTEB / miracl_ru

## Overview

`miracl_ru` is the Russian MIRACL retrieval task as included in ruMTEB. Queries
are short Russian natural-language questions and the documents are Russian
Wikipedia passages. The retriever must return answer-bearing passages, often
among several relevant passages from the same entity page. The task measures
native-language factual retrieval over Wikipedia rather than translation from
English or broad topical classification.

## Details

### What the Original Data Measures

[MIRACL: A Multilingual Retrieval Dataset Covering 18 Diverse Languages](https://arxiv.org/abs/2210.09984)
introduces MIRACL as a multilingual passage retrieval benchmark over Wikipedia
for 18 languages, including Russian, with queries and relevance assessments
created by native-speaker annotators. The paper emphasizes that queries are not
simply written from the answer passage; annotators first generated questions
from prompts and then judged retrieved Wikipedia passages, which makes the
relevance relation closer to ad hoc search than paragraph-derived QA.

[The Russian-focused embedders' exploration: ruMTEB benchmark and Russian
embedding model design](https://arxiv.org/abs/2408.12503) includes
MIRACLRetrieval as one of three ruMTEB retrieval tasks and evaluates retrieval
with nDCG@10. The Nano task uses the MTEB hard-negative MIRACL Russian dev split,
where candidate documents were pooled from BM25 and multilingual dense systems.

### Observed Data Profile

The Nano split has 200 queries, 10,000 documents, and 579 positive qrel rows.
Queries average 45.37 characters and are usually direct Russian fact questions
or yes/no questions about people, places, works, dates, and definitions.
Documents average 517.26 characters and are passage-like snippets from Russian
Wikipedia. Most queries have multiple positives: 136 of 200 queries have more
than one positive qrel, with up to 10 positives for a single query.

The sampled data shows several answer styles. Some positives directly state the
answer in the first sentence, such as whether China is a socialist state. Others
require selecting a later passage from an entity article, such as a specific
paragraph about "Энигма" equipment or a sentence that says Tolstoy wrote "Война
и мир" over six years.

### BM25 Difficulty

Using the dataset-provided BM25 candidate column, BM25 reaches nDCG@10 = 0.4590
and hit@10 = 0.7750. This is a relatively strong lexical baseline for a
Wikipedia fact-retrieval task: entity names and quoted titles often put the
right article near the top, and BM25 ranks at least one positive in the top 10
for 155 of 200 queries.

The remaining failures are instructive. BM25 sometimes retrieves the correct
article lead but misses a later answer-bearing passage, as in questions about
Jan Harold Brunvand's wife or Roald Amundsen's achievements. It also overweights
prominent terms from a question, retrieving "Доктор Кто" for a question about a
book containing the character Rada, instead of the passage about "Макар Чудра"
and "Табор уходит в небо".

### Training Data That May Help

Useful training data includes the non-overlapping MIRACL Russian train data,
Russian Wikipedia question-to-passage pairs, native Russian QA retrieval pairs,
and multilingual retrieval data that preserves same-language query-passage
matching. Training should exclude the MIRACL Russian dev queries, qrels, and
positive passages used by this evaluation split.

For this multi-positive task, training with multiple relevant passages per query
or listwise distillation is preferable to collapsing each query to one positive.
Entity-rich Russian search logs or QA data can help when overlap with evaluated
MIRACL dev passages is removed.

### Synthetic Data Guidance

For document-to-question generation, use non-evaluation Russian Wikipedia
passages and generate native Russian fact questions, yes/no questions, and
definition questions that are answerable from the selected passage. The generated
questions should include realistic inflection, abbreviations, titles, and entity
aliases.

For joint generation, create Wikipedia-style Russian passages plus short search
questions that target a specific fact in the passage. Include several positives
when multiple passages from the same entity answer the same query. Do not seed
synthetic data with MIRACL dev queries or Nano positive passages.

## Example Data

| Query | Positive document |
| --- | --- |
| «Агенты "Щ.И.Т."» - это драматический сериал? (45 chars) | Агенты «Щ.И.Т.» «Аге́нты „Щ.И.Т.“» () — американский супергеройский телесериал, созданный Джоссом Уидоном и основанный на одноимённом комиксе компании Marvel о вымышленной организации по борьбе с преступностью, является часть ... [truncated 225 chars](420 chars) |
| Китай социалистическое государство? (35 chars) | Китай Официально, Китайская Народная Республика — унитарная республика, социалистическое государство демократической диктатуры народа. Основным законом государства является конституция, принятая в 1982 году. Высший орган госу ... [truncated 225 chars](574 chars) |
| Занималось Бюро шифров взломом шифров немецкой Энигмы? (54 chars) | Бюро шифров Главным ведомством Бюро и отделением, ответственным за криптоанализ немецких систем шифрования, стало BS4, позже основной задачей отделения стал взлом немецкой шифровальной машины «Энигма». Начальником немецкого о ... [truncated 225 chars](677 chars) |
| Сколько лет Лев Николаевич Толстой писал роман «Война́ и мир»? (62 chars) | Война и мир Толстой писал роман на протяжении 6 лет, с 1863 по 1869 годы. По историческим сведениям, он вручную переписал его 8 раз, а отдельные эпизоды писатель переписывал более 26 раз. Исследователь Зайденшнур Э. Е. насчит ... [truncated 225 chars](307 chars) |
| Сколько дней длился Евромайдан в Украине? (41 chars) | Евромайдан События в период с 21 ноября 2013 года по 22 февраля 2014 года после смены власти на Украине в украинском праве официально назывались «массовые акции гражданского протеста в Украине с 21 ноября 2013 года по 21 февр ... [truncated 225 chars](280 chars) |

## Dataset Information

| Field | Value |
| --- | --- |
| Nano set | NanoRuMTEB |
| Backing dataset | NanoRuMTEB |
| Task / split | miracl_ru |
| Hugging Face dataset | [hakari-bench/NanoRuMTEB](https://huggingface.co/datasets/hakari-bench/NanoRuMTEB) |
| Language | ru |
| Category | natural_language |
| Queries | 200 |
| Documents | 10,000 |
| Positive qrels | 579 |
| Avg positives / query | 2.90 |
| Positives per query (min / median / max) | 1 / 2 / 10 |
| Queries with multiple positives | 136 (68.00%) |
| BM25 nDCG@10 | 0.5154 |
| BM25 hit@10 | 0.8250 |
| BM25 Recall@100 | 0.9326 |
| BM25 candidate subset | top-500 (`bm25`) |
| Dense nDCG@10 | 0.7938 |
| Dense hit@10 | 0.9550 |
| Dense Recall@100 | 0.9585 |
| Dense candidate subset | top-500 (`harrier_oss_v1_270m`) |
| Reranking hybrid nDCG@10 | 0.6646 |
| Reranking hybrid hit@10 | 0.9050 |
| Reranking hybrid Recall@100 | 0.9948 |
| Reranking hybrid candidate subset | top-100 plus optional rank-101 safeguard (`reranking_hybrid`) |
| Reranking hybrid candidates / query | 100-101 |
| Reranking hybrid safeguard rows | 1 |
| Query length avg chars | 45.37 |
| Document length avg chars | 517.26 |

### Public Sources

- [MIRACL: A Multilingual Retrieval Dataset Covering 18 Diverse Languages](https://arxiv.org/abs/2210.09984); 2023; Xinyu Zhang et al.; DOI: `10.1162/tacl_a_00595`.
- [The Russian-focused embedders' exploration: ruMTEB benchmark and Russian embedding model design](https://arxiv.org/abs/2408.12503); 2025; Artem Snegirev, Maria Tikhonova, Anna Maksimova, Alena Fenogenova, and Aleksandr Abramov; DOI: `10.18653/v1/2025.naacl-long.12`.
- [MIRACL project page](http://miracl.ai/).
- [MTEB MIRACLRetrievalHardNegatives dataset card](https://huggingface.co/datasets/mteb/MIRACLRetrievalHardNegatives).

### Hugging Face Links

- Nano dataset: [hakari-bench/NanoRuMTEB](https://huggingface.co/datasets/hakari-bench/NanoRuMTEB)
- Source dataset: [mteb/MIRACLRetrievalHardNegatives](https://huggingface.co/datasets/mteb/MIRACLRetrievalHardNegatives)

### Source Reference Table

| Title | Year | Type | URL |
| --- | ---: | --- | --- |
| MIRACL: A Multilingual Retrieval Dataset Covering 18 Diverse Languages | 2023 | arXiv paper | https://arxiv.org/abs/2210.09984 |
| The Russian-focused embedders' exploration: ruMTEB benchmark and Russian embedding model design | 2025 | arXiv paper | https://arxiv.org/abs/2408.12503 |
| MIRACL project page | 2023 | project page | http://miracl.ai/ |
| mteb/MIRACLRetrievalHardNegatives | 2025 | dataset card | https://huggingface.co/datasets/mteb/MIRACLRetrievalHardNegatives |

## Machine-Readable Metadata

<!-- benchmark-task-metadata:v1 -->

```yaml
benchmark_task_metadata:
  schema_version: 1
  document_status: first_pass
  nano_set: NanoRuMTEB
  backing_dataset: NanoRuMTEB
  dataset_id: hakari-bench/NanoRuMTEB
  task_name: miracl_ru
  split_name: miracl_ru
  language: ru
  category: natural_language
  document_path: docs/benchmark_tasks/NanoRuMTEB/miracl_ru.md
  source_research:
    primary_source_type: task_paper
    paper_pdf_or_html_checked: true
    paper_url: https://arxiv.org/abs/2210.09984
    additional_source_urls:
    - https://arxiv.org/abs/2408.12503
    - https://aclanthology.org/2025.naacl-long.12/
    - http://miracl.ai/
    - https://huggingface.co/datasets/mteb/MIRACLRetrievalHardNegatives
  counts:
    queries: 200
    documents: 10000
    positive_qrels: 579
  positives_per_query:
    average: 2.895
    min: 1
    median: 2.0
    max: 10
    multi_positive_queries: 136
    multi_positive_query_percent: 68.0
  text_stats_chars:
    query_mean: 45.365
    document_mean: 517.2626
  bm25:
    ndcg_at_10: 0.5154199212966255
    hit_at_10: 0.825
    source: dataset_candidate_subset
  learning:
    original_train_split: available
    evaluation_split_origin: MIRACL Russian dev split through MIRACLRetrievalHardNegatives.v2
    train_eval_overlap_audit: not_audited
    leakage_note: exclude MIRACL Russian dev queries, qrels, and positive passages
      used by this task
    useful_training_data:
    - non-overlapping MIRACL Russian train retrieval pairs
    - native Russian Wikipedia question-passage retrieval pairs
    - same-language multilingual retrieval data with Russian passages
    - Russian entity search and factual QA pairs with overlap removed
    synthetic_data:
      document_generation: non-evaluation Russian Wikipedia-style passages about entities,
        events, works, and definitions
      question_generation: short native Russian fact, yes-no, and definition questions
        answerable from those passages
      answerability: questions should be grounded in explicit facts in one or more
        selected passages
    multi_positive_training: multi_positive_objective
  links:
    nano_dataset: https://huggingface.co/datasets/hakari-bench/NanoRuMTEB
    source_urls:
    - label: MIRACL arXiv
      url: https://arxiv.org/abs/2210.09984
    - label: ruMTEB arXiv
      url: https://arxiv.org/abs/2408.12503
    - label: MIRACL project page
      url: http://miracl.ai/
    - label: MIRACLRetrievalHardNegatives
      url: https://huggingface.co/datasets/mteb/MIRACLRetrievalHardNegatives
    source_notes: []
  references:
  - title: 'MIRACL: A Multilingual Retrieval Dataset Covering 18 Diverse Languages'
    url: https://arxiv.org/abs/2210.09984
    year: 2023
    doi: 10.1162/tacl_a_00595
    is_paper: true
    source_confidence: definitive_paper_link
  - title: 'The Russian-focused embedders'' exploration: ruMTEB benchmark and Russian
      embedding model design'
    url: https://arxiv.org/abs/2408.12503
    year: 2025
    doi: 10.18653/v1/2025.naacl-long.12
    is_paper: true
    source_confidence: definitive_paper_link
  candidate_subsets:
    bm25:
      config: bm25
      label: BM25
      source: dataset_candidate_subset
      top_k: 500
      ndcg_at_10: 0.5154199213
      hit_at_10: 0.825
      recall_at_100: 0.932642487
      candidate_count_min: 500
      candidate_count_max: 500
      candidate_count_mean: 500.0
      query_count: 200
      query_coverage: 1.0
      relevant_coverage_at_100: 0.932642487
    dense:
      config: harrier_oss_v1_270m
      label: Dense
      source: dataset_candidate_subset
      top_k: 500
      ndcg_at_10: 0.7937963237
      hit_at_10: 0.955
      recall_at_100: 0.9585492228
      candidate_count_min: 500
      candidate_count_max: 500
      candidate_count_mean: 500.0
      query_count: 200
      query_coverage: 1.0
      relevant_coverage_at_100: 0.9585492228
    reranking_hybrid:
      config: reranking_hybrid
      label: Reranking hybrid
      source: dataset_candidate_subset
      top_k: 100
      ndcg_at_10: 0.6645751775
      hit_at_10: 0.905
      recall_at_100: 0.9948186528
      candidate_count_min: 100
      candidate_count_max: 101
      candidate_count_mean: 100.005
      query_count: 200
      query_coverage: 1.0
      relevant_coverage_at_100: 0.9948186528
      safeguard_positive_rows: 1
      rows_with_101_candidates: 1
```
