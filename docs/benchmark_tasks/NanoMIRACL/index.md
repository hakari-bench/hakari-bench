# NanoMIRACL

## Overview

NanoMIRACL is the Nano task group for MIRACL, a multilingual ad hoc retrieval
benchmark over Wikipedia passages. It covers eighteen language splits: Arabic,
Bengali, German, English, Spanish, Persian, Finnish, French, Hindi, Indonesian,
Japanese, Korean, Russian, Swahili, Telugu, Thai, Yoruba, and Chinese. Each split
is monolingual: a question in a given language retrieves a Wikipedia passage in
the same language.

The group is useful because it compares the same retrieval task shape across
scripts, tokenization regimes, morphology, resource levels, and Wikipedia
coverage. It is not a translation task. A model must retrieve answer-bearing
passages in the query language, often from short entity-centric questions and
compact encyclopedia passages.

## Details

### What the Original Group Measures

[MIRACL: A Multilingual Retrieval Dataset Covering 18 Diverse Languages](https://aclanthology.org/2023.tacl-1.63/)
introduces MIRACL as a passage retrieval benchmark spanning 18 languages. The
source paper describes monolingual retrieval over Wikipedia, with native-speaker
question generation and relevance judgments. It reports more than 78k queries
and more than 726k relevance judgments in the full benchmark, covering languages
from multiple language families and resource levels.

NanoMIRACL keeps the same high-level retrieval setting in compact form. Each
language split contains natural-language questions, a split-local sample of
Wikipedia passages, one positive qrel per query in the observed Nano data, and a
dataset-provided BM25 ranking. The group therefore measures multilingual
evidence passage retrieval rather than answer generation or cross-lingual
matching.

### Subtask Coverage

The eighteen subtasks cover diverse scripts and language conditions:

- **Arabic script:** `ar` and `fa` use Arabic/Persian script with entity-rich
  factual questions.
- **Indic scripts:** `bn`, `hi`, and `te` cover Bengali, Devanagari Hindi, and
  Telugu Wikipedia retrieval.
- **Latin-script European languages:** `de`, `en`, `es`, `fi`, `fr`, and `id`
  cover German, English, Spanish, Finnish, French, and Indonesian question-to-
  passage retrieval.
- **CJK and Thai scripts:** `ja`, `ko`, `zh`, and `th` stress segmentation,
  named entities, and compact fact questions in Japanese, Korean, Chinese, and
  Thai.
- **African languages:** `sw` and `yo` cover Swahili and Yoruba. The Yoruba
  split is small and code-mixed in sampled data; the task metadata labels it as
  multilingual while the intended MIRACL split is Yoruba.
- **Slavic language:** `ru` covers Russian Wikipedia passage retrieval.

All observed splits are single-positive in the Nano version. Most splits have
200 queries; Telugu has 84 and Yoruba has 119. The corpus sizes range from 754
documents for Telugu to 2,419 documents for Korean.

### Observed Group Profile

Across the eighteen splits, NanoMIRACL contains 3,403 queries, 3,403 positive
qrels, and 29,897 split-local candidate documents. The document count is a sum
across language splits, not a deduplicated group-wide corpus size. Query length
is short overall, averaging 37.68 characters when weighted by query count.
Documents average 556.87 characters when weighted by split-local document count.

The sampled records are factual Wikipedia evidence tasks. Queries ask about
definitions, dates, locations, people, capitals, countries, institutions,
events, science topics, media, sports, and demography. Positive passages usually
begin with a Wikipedia article title followed by a paragraph containing the
answer. The difficulty is often not finding a broad topic, but ranking the
passage that answers the exact relation above neighboring passages from the same
article family or homonymous topic.

### BM25 Difficulty

Query-weighted BM25 nDCG@10 is 0.5201 and query-weighted hit@10 is 0.7875. The
language spread is meaningful. Thai is easiest by nDCG@10 in the observed Nano
data (0.6475), followed by Finnish, Telugu, Japanese, Swahili, and Indonesian.
French is hardest by nDCG@10 (0.3034), with German, Russian, and Chinese also
below the group mean.

BM25 performs well when questions contain rare entity strings that also appear
in the positive passage. Japanese, Thai, Finnish, and several other splits show
high hit@10 under this pattern. BM25 is weaker when passage selection requires
sense disambiguation, relation matching, morphology handling, or distinguishing
nearby passages with the same entity. French examples show morphology and
homonym confusion; German and Russian examples often need relation-specific
passage selection; Chinese and Korean require segmentation and short-query
matching; Yoruba includes short template-like questions with code-mixed and
diacritic variation.

### Training Data That May Help

Useful training data includes non-overlapping MIRACL training data, multilingual
Wikipedia question-to-passage retrieval pairs, open-domain QA evidence retrieval,
and hard negatives sampled from same-article or same-entity passages. Training
should remain monolingual for this group: Arabic queries should retrieve Arabic
passages, Japanese queries should retrieve Japanese passages, and so on.

Training should exclude NanoMIRACL evaluation queries, qrels, and positive
passages. Upstream MIRACL dev/test rows likely to overlap with Nano splits
should also be excluded unless an explicit overlap audit has been performed.
For low-resource or surprise-language style settings such as Yoruba, even small
overlaps can materially distort scores.

### Synthetic Data Guidance

Synthetic data should be generated from non-evaluation Wikipedia-style passages
in each target language. The generated questions should be grounded in a single
selected passage and should vary common factual forms: who, what, when, where,
how many, whether, definition, location, role, cause, and classification. Good
synthetic passages should preserve article-title style, aliases, dates, named
entities, numerals, and language-specific orthography.

Hard negatives should be passage-level, not only document-level. Useful
distractors include neighboring sections from the same article, homonymous
entities, near-identical capital/country templates, related events, and passages
sharing dates or names but not answering the query. Synthetic data should not
seed from Nano evaluation queries or positive passages.

## Task Summary

| Task | Language | Queries | Docs | BM25 nDCG@10 | BM25 hit@10 | Query avg chars | Doc avg chars | Source status |
| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | --- |
| [ar](ar.md) | ar | 200 | 1,854 | 0.5445 | 0.8100 | 30.14 | 680.47 | MIRACL paper |
| [bn](bn.md) | bn | 200 | 1,731 | 0.5103 | 0.7750 | 47.23 | 717.88 | MIRACL paper |
| [de](de.md) | de | 200 | 1,748 | 0.3665 | 0.6000 | 45.57 | 629.75 | MIRACL paper |
| [en](en.md) | en | 200 | 1,657 | 0.5432 | 0.8750 | 40.10 | 760.23 | MIRACL paper |
| [es](es.md) | es | 200 | 1,312 | 0.5110 | 0.7600 | 48.21 | 612.47 | MIRACL paper |
| [fa](fa.md) | fa | 200 | 1,858 | 0.5337 | 0.8400 | 39.99 | 489.71 | MIRACL paper |
| [fi](fi.md) | fi | 200 | 1,828 | 0.6240 | 0.8950 | 37.34 | 653.42 | MIRACL paper |
| [fr](fr.md) | fr | 200 | 1,777 | 0.3034 | 0.5700 | 43.26 | 556.73 | MIRACL paper |
| [hi](hi.md) | hi | 200 | 1,748 | 0.5497 | 0.8550 | 54.75 | 580.36 | MIRACL paper |
| [id](id.md) | id | 200 | 1,520 | 0.5705 | 0.8350 | 38.51 | 676.16 | MIRACL paper |
| [ja](ja.md) | ja | 200 | 1,846 | 0.5956 | 0.9400 | 17.47 | 297.91 | MIRACL paper |
| [ko](ko.md) | ko | 200 | 2,419 | 0.5090 | 0.7150 | 21.71 | 287.30 | MIRACL paper |
| [ru](ru.md) | ru | 200 | 1,727 | 0.4457 | 0.6750 | 45.53 | 783.43 | MIRACL paper |
| [sw](sw.md) | sw/multilingual metadata | 200 | 1,600 | 0.5782 | 0.8150 | 38.33 | 532.75 | MIRACL paper |
| [te](te.md) | te | 84 | 754 | 0.6044 | 0.8452 | 38.46 | 787.54 | MIRACL paper |
| [th](th.md) | th | 200 | 1,897 | 0.6475 | 0.9150 | 43.61 | 595.21 | MIRACL paper |
| [yo](yo.md) | yo/multilingual metadata | 119 | 921 | 0.5323 | 0.7227 | 37.69 | 397.16 | MIRACL paper |
| [zh](zh.md) | zh | 200 | 1,700 | 0.4466 | 0.7400 | 10.86 | 179.69 | MIRACL paper |

## Dataset Information

| Field | Value |
| --- | --- |
| Nano set | NanoMIRACL |
| Backing dataset | NanoMIRACL |
| Hugging Face dataset | [hakari-bench/NanoMIRACL](https://huggingface.co/datasets/hakari-bench/NanoMIRACL) |
| Language | multilingual |
| Category | natural_language |
| Subtasks | 18 |
| Total queries | 3,403 |
| Split-local documents | 29,897 |
| Positive qrels | 3,403 |
| Positives per query | exactly 1.00 for every observed query |
| Query-weighted BM25 nDCG@10 | 0.5727 |
| Query-weighted BM25 hit@10 | 0.8595 |
| Query-weighted BM25 Recall@100 | 0.9398 |
| Query-weighted Dense nDCG@10 | 0.7571 |
| Query-weighted Dense hit@10 | 0.9350 |
| Query-weighted Dense Recall@100 | 0.9417 |
| Query-weighted Reranking hybrid nDCG@10 | 0.6881 |
| Query-weighted Reranking hybrid hit@10 | 0.9350 |
| Query-weighted Reranking hybrid Recall@100 | 0.9936 |
| Mean query length | 37.68 chars, weighted by query count |
| Mean document length | 556.87 chars, weighted by split-local document count |

### Public Sources

- [MIRACL: A Multilingual Retrieval Dataset Covering 18 Diverse Languages](https://aclanthology.org/2023.tacl-1.63/); 2023; Xinyu Zhang et al.; DOI: `10.1162/tacl_a_00595`.
- [Making a MIRACL: Multilingual Information Retrieval Across a Continuum of Languages](https://arxiv.org/abs/2210.09984); 2022 arXiv version.
- [MIRACL project site](http://miracl.ai/).
- [MIRACL GitHub repository](https://github.com/project-miracl/miracl).
- [miracl/miracl-corpus](https://huggingface.co/datasets/miracl/miracl-corpus) and [miracl/miracl](https://huggingface.co/datasets/miracl/miracl) source dataset cards.

### Hugging Face Links

- Nano dataset: [hakari-bench/NanoMIRACL](https://huggingface.co/datasets/hakari-bench/NanoMIRACL)
- Source corpus: [miracl/miracl-corpus](https://huggingface.co/datasets/miracl/miracl-corpus)
- Source queries and qrels: [miracl/miracl](https://huggingface.co/datasets/miracl/miracl)

### Source Reference Table

| Title | Year | Type | URL |
| --- | ---: | --- | --- |
| MIRACL: A Multilingual Retrieval Dataset Covering 18 Diverse Languages | 2023 | benchmark paper | https://aclanthology.org/2023.tacl-1.63/ |
| Making a MIRACL: Multilingual Information Retrieval Across a Continuum of Languages | 2022 | arXiv paper | https://arxiv.org/abs/2210.09984 |
| MIRACL project site | 2023 | project page | http://miracl.ai/ |
| MIRACL GitHub repository | 2023 | repository | https://github.com/project-miracl/miracl |
| miracl/miracl-corpus | 2023 | dataset card | https://huggingface.co/datasets/miracl/miracl-corpus |
| miracl/miracl | 2023 | dataset card | https://huggingface.co/datasets/miracl/miracl |

## Machine-Readable Metadata

<!-- benchmark-task-group-metadata:v1 -->

```yaml
benchmark_task_group_metadata:
  schema_version: 1
  document_status: reviewed_manual
  nano_set: NanoMIRACL
  backing_dataset: NanoMIRACL
  dataset_id: hakari-bench/NanoMIRACL
  language: multilingual
  category: natural_language
  document_path: docs/benchmark_tasks/NanoMIRACL/index.md
  source_research:
    primary_source_type: benchmark_paper
    paper_pdf_or_html_checked: true
    no_paper_note: null
  counts:
    tasks: 18
    queries: 3403
    split_local_documents: 29897
    positive_qrels: 3403
  positives_per_query:
    average: 1.0
    min: 1
    median: 1.0
    max: 1
    multi_positive_tasks: 0
    multi_positive_queries: 0
  text_stats_chars:
    query_mean_weighted_by_queries: 37.68322070761093
    document_mean_weighted_by_documents: 556.8686157020103
  bm25:
    ndcg_at_10_query_weighted: 0.5727262131
    hit_at_10_query_weighted: 0.8594651778
    ndcg_at_10_unweighted_task_mean: 0.5231217559611111
    hit_at_10_unweighted_task_mean: 0.7879403983777777
    source: dataset_candidate_subset
    easiest_task_by_ndcg_at_10: th
    hardest_task_by_ndcg_at_10: fr
  tasks:
  - name: ar
    path: docs/benchmark_tasks/NanoMIRACL/ar.md
    retrieval_shape: arabic_question_to_arabic_wikipedia_passage
    queries: 200
    documents: 1854
    positive_qrels: 200
    bm25_ndcg_at_10: 0.5445
    bm25_hit_at_10: 0.81
  - name: bn
    path: docs/benchmark_tasks/NanoMIRACL/bn.md
    retrieval_shape: bengali_question_to_bengali_wikipedia_passage
    queries: 200
    documents: 1731
    positive_qrels: 200
    bm25_ndcg_at_10: 0.5103
    bm25_hit_at_10: 0.775
  - name: de
    path: docs/benchmark_tasks/NanoMIRACL/de.md
    retrieval_shape: german_question_to_german_wikipedia_passage
    queries: 200
    documents: 1748
    positive_qrels: 200
    bm25_ndcg_at_10: 0.3665
    bm25_hit_at_10: 0.6
  - name: en
    path: docs/benchmark_tasks/NanoMIRACL/en.md
    retrieval_shape: english_question_to_english_wikipedia_passage
    queries: 200
    documents: 1657
    positive_qrels: 200
    bm25_ndcg_at_10: 0.5432
    bm25_hit_at_10: 0.875
  - name: es
    path: docs/benchmark_tasks/NanoMIRACL/es.md
    retrieval_shape: spanish_question_to_spanish_wikipedia_passage
    queries: 200
    documents: 1312
    positive_qrels: 200
    bm25_ndcg_at_10: 0.511
    bm25_hit_at_10: 0.76
  - name: fa
    path: docs/benchmark_tasks/NanoMIRACL/fa.md
    retrieval_shape: persian_question_to_persian_wikipedia_passage
    queries: 200
    documents: 1858
    positive_qrels: 200
    bm25_ndcg_at_10: 0.5337
    bm25_hit_at_10: 0.84
  - name: fi
    path: docs/benchmark_tasks/NanoMIRACL/fi.md
    retrieval_shape: finnish_question_to_finnish_wikipedia_passage
    queries: 200
    documents: 1828
    positive_qrels: 200
    bm25_ndcg_at_10: 0.624
    bm25_hit_at_10: 0.895
  - name: fr
    path: docs/benchmark_tasks/NanoMIRACL/fr.md
    retrieval_shape: french_question_to_french_wikipedia_passage
    queries: 200
    documents: 1777
    positive_qrels: 200
    bm25_ndcg_at_10: 0.3034
    bm25_hit_at_10: 0.57
  - name: hi
    path: docs/benchmark_tasks/NanoMIRACL/hi.md
    retrieval_shape: hindi_question_to_hindi_wikipedia_passage
    queries: 200
    documents: 1748
    positive_qrels: 200
    bm25_ndcg_at_10: 0.5497
    bm25_hit_at_10: 0.855
  - name: id
    path: docs/benchmark_tasks/NanoMIRACL/id.md
    retrieval_shape: indonesian_question_to_indonesian_wikipedia_passage
    queries: 200
    documents: 1520
    positive_qrels: 200
    bm25_ndcg_at_10: 0.5705
    bm25_hit_at_10: 0.835
  - name: ja
    path: docs/benchmark_tasks/NanoMIRACL/ja.md
    retrieval_shape: japanese_question_to_japanese_wikipedia_passage
    queries: 200
    documents: 1846
    positive_qrels: 200
    bm25_ndcg_at_10: 0.5956
    bm25_hit_at_10: 0.94
  - name: ko
    path: docs/benchmark_tasks/NanoMIRACL/ko.md
    retrieval_shape: korean_question_to_korean_wikipedia_passage
    queries: 200
    documents: 2419
    positive_qrels: 200
    bm25_ndcg_at_10: 0.509
    bm25_hit_at_10: 0.715
  - name: ru
    path: docs/benchmark_tasks/NanoMIRACL/ru.md
    retrieval_shape: russian_question_to_russian_wikipedia_passage
    queries: 200
    documents: 1727
    positive_qrels: 200
    bm25_ndcg_at_10: 0.4457
    bm25_hit_at_10: 0.675
  - name: sw
    path: docs/benchmark_tasks/NanoMIRACL/sw.md
    retrieval_shape: swahili_question_to_swahili_wikipedia_passage
    queries: 200
    documents: 1600
    positive_qrels: 200
    bm25_ndcg_at_10: 0.5782
    bm25_hit_at_10: 0.815
  - name: te
    path: docs/benchmark_tasks/NanoMIRACL/te.md
    retrieval_shape: telugu_question_to_telugu_wikipedia_passage
    queries: 84
    documents: 754
    positive_qrels: 84
    bm25_ndcg_at_10: 0.6044
    bm25_hit_at_10: 0.8452
  - name: th
    path: docs/benchmark_tasks/NanoMIRACL/th.md
    retrieval_shape: thai_question_to_thai_wikipedia_passage
    queries: 200
    documents: 1897
    positive_qrels: 200
    bm25_ndcg_at_10: 0.6475
    bm25_hit_at_10: 0.915
  - name: yo
    path: docs/benchmark_tasks/NanoMIRACL/yo.md
    retrieval_shape: yoruba_question_to_yoruba_wikipedia_passage
    queries: 119
    documents: 921
    positive_qrels: 119
    bm25_ndcg_at_10: 0.5323
    bm25_hit_at_10: 0.7227
  - name: zh
    path: docs/benchmark_tasks/NanoMIRACL/zh.md
    retrieval_shape: chinese_question_to_chinese_wikipedia_passage
    queries: 200
    documents: 1700
    positive_qrels: 200
    bm25_ndcg_at_10: 0.4466
    bm25_hit_at_10: 0.74
  learning:
    leakage_note: exclude NanoMIRACL evaluation queries, qrels, positive passages,
      and overlapping MIRACL dev or test rows unless an explicit overlap audit has
      been performed
    useful_training_data:
    - non-overlapping MIRACL training data in each language
    - multilingual Wikipedia question-to-passage retrieval pairs
    - monolingual open-domain QA evidence retrieval data
    - hard negatives from same article, same entity, and homonymous passages
    - low-resource retrieval data for Swahili, Yoruba, Telugu, and other smaller splits
    synthetic_data:
      document_generation: Wikipedia-style passages with article titles, aliases,
        dates, roles, locations, counts, and definitions in each target language
      question_generation: grounded factual questions in the same language as the
        passage
      answerability: each positive should be the passage that contains the requested
        evidence, not merely a topical page
    multi_positive_training: single_positive_passage_retrieval_in_observed_nano_splits
  links:
    nano_dataset: https://huggingface.co/datasets/hakari-bench/NanoMIRACL
    source_urls:
    - label: MIRACL TACL paper
      url: https://aclanthology.org/2023.tacl-1.63/
    - label: MIRACL arXiv
      url: https://arxiv.org/abs/2210.09984
    - label: MIRACL project
      url: http://miracl.ai/
    - label: MIRACL GitHub
      url: https://github.com/project-miracl/miracl
    - label: miracl/miracl-corpus
      url: https://huggingface.co/datasets/miracl/miracl-corpus
    - label: miracl/miracl
      url: https://huggingface.co/datasets/miracl/miracl
    source_notes: []
  references:
  - title: 'MIRACL: A Multilingual Retrieval Dataset Covering 18 Diverse Languages'
    url: https://aclanthology.org/2023.tacl-1.63/
    year: 2023
    doi: 10.1162/tacl_a_00595
    is_paper: true
    source_confidence: definitive_paper_link
  - title: 'Making a MIRACL: Multilingual Information Retrieval Across a Continuum
      of Languages'
    url: https://arxiv.org/abs/2210.09984
    year: 2022
    is_paper: true
    source_confidence: definitive_paper_link
  - title: MIRACL project site
    url: http://miracl.ai/
    year: 2023
    is_paper: false
    source_confidence: probably_correct
  candidate_subsets:
    bm25:
      query_weighted_ndcg_at_10: 0.5727262131
      query_weighted_hit_at_10: 0.8594651778
      query_weighted_recall_at_100: 0.9397934651
      source: dataset_candidate_subset
    dense:
      query_weighted_ndcg_at_10: 0.7571472414
      query_weighted_hit_at_10: 0.9350161622
      query_weighted_recall_at_100: 0.9417335309
      source: dataset_candidate_subset
    reranking_hybrid:
      query_weighted_ndcg_at_10: 0.6880547774
      query_weighted_hit_at_10: 0.9349573905
      query_weighted_recall_at_100: 0.9935957469
      source: dataset_candidate_subset
```
