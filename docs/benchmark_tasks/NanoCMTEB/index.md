# NanoCMTEB

## Overview

NanoCMTEB is a compact Chinese retrieval group based on C-MTEB retrieval tasks.
It covers Chinese medical consultation retrieval, COVID policy/news retrieval,
general web passage retrieval, e-commerce product retrieval, translated MS
MARCO-style retrieval, T2Ranking passage ranking, and entertainment-video
retrieval. The group is dominated by short Chinese queries and 10,000-document
candidate pools, with several tasks containing many positives per query.

## Details

### What the Original Group Measures

The group follows C-MTEB, introduced in C-Pack as a comprehensive Chinese text
embedding benchmark. Its retrieval tasks draw from several source families:
DuReader Retrieval and T2Ranking for Chinese web search and passage ranking,
Multi-CPR for domain-specific e-commerce, entertainment-video, and medical
retrieval, mMARCO for translated MS MARCO passage ranking, and CMedQA-derived
medical consultation retrieval.

The Nano version preserves the broad C-MTEB retrieval surface but keeps each
split small. Every split has 200 queries and a 10,000-document candidate
corpus. The tasks differ sharply in document length and relevance structure:
product and video documents are short title-like strings, while T2 and COVID
documents can be long, noisy web or policy passages.

### Subtask Coverage

The eight subtasks cover five retrieval families:

- **Medical consultation retrieval:** `cmedqa` retrieves doctor-style answers
  for patient questions, while `medical` retrieves concise medical-domain
  passages for short consumer health queries.
- **Public policy and COVID retrieval:** `covid` retrieves pandemic-related
  news, government notices, and policy passages.
- **General Chinese web retrieval:** `du`, `mmarco`, and `t2` cover DuReader
  Retrieval, translated MS MARCO, and T2Ranking-style web passage ranking.
- **E-commerce retrieval:** `ecom` matches very short shopping queries to
  product-title-like documents, often with brand, model, and mixed-script
  tokens.
- **Entertainment-video retrieval:** `video` matches short video-search queries
  to compact video titles or metadata-like records.

Although the group is primarily Chinese, it is marked multilingual because
several splits contain Japanese, English, romanized names, product codes, and
translated MS MARCO artifacts. In `ecom` and `video`, mixed scripts are part of
the retrieval challenge rather than incidental noise.

### Observed Group Profile

Across the eight splits, NanoCMTEB contains 1,600 queries, 3,208 positive
qrels, and 80,000 split-local candidate documents. The document count is a sum
across subtasks and should not be interpreted as a deduplicated group-wide
corpus. The average is 2.01 positives per query, with 432 multi-positive
queries. `du` and `t2` have the largest relevance sets, with maximum positives
of 27 and 23 respectively.

Queries are very short in most tasks. `ecom`, `video`, `du`, `mmarco`, and
`t2` all average below 11 characters, while `cmedqa` is longer because queries
are patient case descriptions. Document lengths range from product or video
titles around 30 characters to long T2 and COVID passages. The query-weighted
mean query length is 17.51 characters, and the document-weighted mean document
length is 271.88 characters.

### BM25 Difficulty

The query-weighted BM25 baseline reaches nDCG@10 = 0.0510 and hit@10 = 0.0650,
which makes NanoCMTEB one of the most lexically difficult groups among the
completed indexes. The easiest split by nDCG@10 is `covid` at 0.1778, where
administrative terms, dates, and policy names sometimes give BM25 useful
anchors. The hardest split is `cmedqa` at 0.0113, where patient descriptions
and doctor answers often use different wording.

The low scores also reflect the nature of the candidate columns and source
tasks. Short Chinese queries provide little lexical context; product and video
queries may rely on aliases, brands, romanization, or mixed scripts; medical
answers often use clinical wording that differs from lay symptoms; and T2/Du
use noisy web passages with multiple relevant documents per query. For `du` and
`t2`, improvements should be judged by ranking several positives well, not only
by retrieving one exact match.

### Training Data That May Help

Useful training data should be domain-specific. For medical tasks, use
non-overlapping Chinese consultation QA, symptom-to-answer retrieval, and hard
negatives from similar diseases or body parts. For COVID and policy retrieval,
use Chinese news, government-notice QA, and city or agency-level hard
negatives. For `du` and `t2`, use Chinese web-search relevance annotations,
multi-positive passage ranking, and negatives with exact query-term overlap but
lower relevance. For `ecom` and `video`, use product or video search logs,
title alias data, brand/model normalization, mixed-script title matching, and
hard negatives that share product category, series, cast, or episode.

Training should exclude Nano evaluation queries, qrels, positive documents,
consultation threads, product titles, and video titles. Multi-positive labels
in `cmedqa`, `du`, `mmarco`, `t2`, and `covid` should be preserved where they
exist.

### Synthetic Data Guidance

Synthetic data should preserve the short-query nature of the group. Generate
brief Chinese search queries from longer web, policy, medical, product, or
video documents. For medical and CMedQA-style data, generate patient questions
and answer passages with symptom overlap but distinct diagnoses. For product
and video retrieval, generate compact titles with brand, model, episode,
performer, and mixed-script variants. For web and T2-style tasks, generate
multiple relevant passages per short query and hard negatives that contain the
same keywords but fail to answer the intent.

Synthetic examples should not use NanoCMTEB evaluation queries or positive
documents as seeds.

## Task Summary

| Task | Retrieval shape | Lang | Queries | Docs | Positive qrels | BM25 nDCG@10 | BM25 hit@10 | Query avg chars | Doc avg chars | Source status |
| --- | --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | --- |
| [cmedqa](cmedqa.md) | Chinese patient question to doctor answer | zh | 200 | 10,000 | 324 | 0.0113 | 0.0200 | 52.00 | 157.57 | C-MTEB / CMedQA |
| [covid](covid.md) | Chinese COVID query to news or policy passage | zh | 200 | 10,000 | 204 | 0.1778 | 0.2000 | 25.73 | 409.35 | Multi-CPR / C-MTEB |
| [du](du.md) | Chinese web query to answer-bearing passage | zh | 200 | 10,000 | 889 | 0.0399 | 0.0800 | 9.12 | 397.39 | DuReader Retrieval |
| [ecom](ecom.md) | Chinese shopping query to product title | multilingual | 200 | 10,000 | 200 | 0.0132 | 0.0150 | 6.88 | 33.09 | Multi-CPR / C-MTEB |
| [medical](medical.md) | Chinese health query to medical answer passage | zh | 200 | 10,000 | 200 | 0.0150 | 0.0150 | 18.12 | 119.70 | Multi-CPR / C-MTEB |
| [mmarco](mmarco.md) | Chinese translated MS MARCO query to passage | zh | 200 | 10,000 | 212 | 0.0902 | 0.1050 | 10.44 | 113.91 | mMARCO |
| [t2](t2.md) | Chinese search query to noisy web passage | zh | 200 | 10,000 | 979 | 0.0205 | 0.0400 | 10.74 | 913.50 | T2Ranking |
| [video](video.md) | Chinese video search query to title or metadata | zh | 200 | 10,000 | 200 | 0.0400 | 0.0450 | 7.07 | 30.52 | Multi-CPR / C-MTEB |

## Dataset Information

| Field | Value |
| --- | --- |
| Nano set | NanoCMTEB |
| Backing dataset | NanoCMTEB |
| Hugging Face dataset | [hakari-bench/NanoCMTEB](https://huggingface.co/datasets/hakari-bench/NanoCMTEB) |
| Languages | zh, multilingual |
| Category | natural_language |
| Subtasks | 8 |
| Total queries | 1,600 |
| Split-local documents | 80,000 |
| Positive qrels | 3,208 |
| Positives per query | 2.01 average |
| Multi-positive queries | 432 |
| Query-weighted BM25 nDCG@10 | 0.0510 |
| Query-weighted BM25 hit@10 | 0.0650 |
| Mean query length | 17.51 chars, weighted by query count |
| Mean document length | 271.88 chars, weighted by split-local document count |

### Public Sources

- [C-Pack: Packed Resources For General Chinese Embeddings](https://arxiv.org/abs/2309.07597); C-MTEB source.
- [Multi-CPR: A Multi Domain Chinese Dataset for Passage Retrieval](https://arxiv.org/abs/2203.03367); e-commerce, video, and medical retrieval source.
- [DuReader-retrieval: A Large-scale Chinese Benchmark for Passage Retrieval](https://aclanthology.org/2022.emnlp-main.357/); Chinese web passage retrieval source.
- [mMARCO: A Multilingual Version of the MS MARCO Passage Ranking Dataset](https://arxiv.org/abs/2108.13897); translated MS MARCO source.
- [T2Ranking: A large-scale Chinese Benchmark for Passage Ranking](https://arxiv.org/abs/2304.03679); Chinese passage ranking source.

### Hugging Face Links

- Nano dataset: [hakari-bench/NanoCMTEB](https://huggingface.co/datasets/hakari-bench/NanoCMTEB)
- Source examples:
  [mteb/CmedqaRetrieval](https://huggingface.co/datasets/mteb/CmedqaRetrieval),
  [mteb/CovidRetrieval](https://huggingface.co/datasets/mteb/CovidRetrieval),
  [mteb/DuRetrieval](https://huggingface.co/datasets/mteb/DuRetrieval),
  [mteb/EcomRetrieval](https://huggingface.co/datasets/mteb/EcomRetrieval),
  [mteb/MedicalRetrieval](https://huggingface.co/datasets/mteb/MedicalRetrieval),
  [mteb/MMarcoRetrieval](https://huggingface.co/datasets/mteb/MMarcoRetrieval),
  [mteb/T2Retrieval](https://huggingface.co/datasets/mteb/T2Retrieval),
  [mteb/VideoRetrieval](https://huggingface.co/datasets/mteb/VideoRetrieval).

### Source Reference Table

| Title | Year | Type | URL |
| --- | ---: | --- | --- |
| C-Pack: Packed Resources For General Chinese Embeddings | 2024 | benchmark paper | https://arxiv.org/abs/2309.07597 |
| Multi-CPR: A Multi Domain Chinese Dataset for Passage Retrieval | 2022 | source task paper | https://arxiv.org/abs/2203.03367 |
| DuReader-retrieval: A Large-scale Chinese Benchmark for Passage Retrieval | 2022 | source task paper | https://aclanthology.org/2022.emnlp-main.357/ |
| mMARCO: A Multilingual Version of the MS MARCO Passage Ranking Dataset | 2021 | source task paper | https://arxiv.org/abs/2108.13897 |
| T2Ranking: A large-scale Chinese Benchmark for Passage Ranking | 2023 | source task paper | https://arxiv.org/abs/2304.03679 |

## Machine-Readable Metadata

<!-- benchmark-task-group-metadata:v1 -->

```yaml
benchmark_task_group_metadata:
  schema_version: 1
  document_status: reviewed_manual
  nano_set: NanoCMTEB
  backing_dataset: NanoCMTEB
  dataset_id: hakari-bench/NanoCMTEB
  language: multilingual
  languages:
    - zh
    - multilingual
  category: natural_language
  document_path: docs/benchmark_tasks/NanoCMTEB/index.md
  source_research:
    primary_source_type: multiple_task_papers_and_dataset_cards
    paper_pdf_or_html_checked: true
    no_paper_note: null
  counts:
    tasks: 8
    queries: 1600
    split_local_documents: 80000
    positive_qrels: 3208
  positives_per_query:
    average: 2.005
    min: 1
    median_task_median: 1.0
    max: 27
    multi_positive_tasks: 5
    multi_positive_queries: 432
  text_stats_chars:
    query_mean_weighted_by_queries: 17.51375
    document_mean_weighted_by_documents: 271.877075
  bm25:
    ndcg_at_10_query_weighted: 0.05097835520376681
    hit_at_10_query_weighted: 0.065
    ndcg_at_10_unweighted_task_mean: 0.050978355203766805
    hit_at_10_unweighted_task_mean: 0.065
    source: dataset_bm25_column
    easiest_task_by_ndcg_at_10: covid
    hardest_task_by_ndcg_at_10: cmedqa
  tasks:
    - name: cmedqa
      path: docs/benchmark_tasks/NanoCMTEB/cmedqa.md
      retrieval_shape: chinese_patient_question_to_doctor_answer
      language: zh
      queries: 200
      documents: 10000
      positive_qrels: 324
      bm25_ndcg_at_10: 0.011250194130034799
      bm25_hit_at_10: 0.02
    - name: covid
      path: docs/benchmark_tasks/NanoCMTEB/covid.md
      retrieval_shape: chinese_covid_query_to_news_or_policy_passage
      language: zh
      queries: 200
      documents: 10000
      positive_qrels: 204
      bm25_ndcg_at_10: 0.17776949585626847
      bm25_hit_at_10: 0.2
    - name: du
      path: docs/benchmark_tasks/NanoCMTEB/du.md
      retrieval_shape: chinese_web_query_to_answer_bearing_passage
      language: zh
      queries: 200
      documents: 10000
      positive_qrels: 889
      bm25_ndcg_at_10: 0.03993315000492959
      bm25_hit_at_10: 0.08
    - name: ecom
      path: docs/benchmark_tasks/NanoCMTEB/ecom.md
      retrieval_shape: chinese_shopping_query_to_product_title
      language: multilingual
      queries: 200
      documents: 10000
      positive_qrels: 200
      bm25_ndcg_at_10: 0.01315464876785729
      bm25_hit_at_10: 0.015
    - name: medical
      path: docs/benchmark_tasks/NanoCMTEB/medical.md
      retrieval_shape: chinese_health_query_to_medical_answer_passage
      language: zh
      queries: 200
      documents: 10000
      positive_qrels: 200
      bm25_ndcg_at_10: 0.015
      bm25_hit_at_10: 0.015
    - name: mmarco
      path: docs/benchmark_tasks/NanoCMTEB/mmarco.md
      retrieval_shape: chinese_translated_ms_marco_query_to_passage
      language: zh
      queries: 200
      documents: 10000
      positive_qrels: 212
      bm25_ndcg_at_10: 0.09022048770790005
      bm25_hit_at_10: 0.105
    - name: t2
      path: docs/benchmark_tasks/NanoCMTEB/t2.md
      retrieval_shape: chinese_search_query_to_noisy_web_passage
      language: zh
      queries: 200
      documents: 10000
      positive_qrels: 979
      bm25_ndcg_at_10: 0.020498865163144264
      bm25_hit_at_10: 0.04
    - name: video
      path: docs/benchmark_tasks/NanoCMTEB/video.md
      retrieval_shape: chinese_video_search_query_to_title_or_metadata
      language: zh
      queries: 200
      documents: 10000
      positive_qrels: 200
      bm25_ndcg_at_10: 0.04
      bm25_hit_at_10: 0.045
  learning:
    leakage_note: exclude NanoCMTEB evaluation queries, qrels, positive documents, consultation threads, product titles, video titles, translated MS MARCO rows, and upstream dev/test rows from training
    useful_training_data:
      - Chinese medical consultation and symptom-to-answer retrieval pairs
      - Chinese COVID, public-policy, and government-notice QA retrieval pairs
      - DuReader, T2Ranking, and Chinese web search relevance annotations with multi-positive labels
      - mMARCO Chinese and multilingual MS MARCO passage ranking data with evaluation rows removed
      - Chinese e-commerce query-title and click/relevance data
      - Chinese and mixed-script entertainment video query-title pairs
      - hard negatives from the same medical specialty, policy topic, web entity, product category, brand, model, series, performer, or episode
    synthetic_data:
      document_generation: Chinese medical answers, policy notices, noisy web passages, product titles, translated web passages, T2-style long passages, and video metadata in source-like style
      question_generation: short Chinese search queries, patient questions, policy questions, shopping queries, and video title queries grounded in generated documents
      answerability: positives must preserve clinical answerability, policy answer support, passage relevance, product identity, title identity, or translated MS MARCO relevance rather than broad lexical overlap
    multi_positive_training: preserve_cmedqa_covid_du_mmarco_and_t2_multi_positive_qrels
  links:
    nano_dataset: https://huggingface.co/datasets/hakari-bench/NanoCMTEB
    source_urls:
      - label: C-Pack arXiv
        url: https://arxiv.org/abs/2309.07597
      - label: Multi-CPR arXiv
        url: https://arxiv.org/abs/2203.03367
      - label: DuReader Retrieval paper
        url: https://aclanthology.org/2022.emnlp-main.357/
      - label: mMARCO arXiv
        url: https://arxiv.org/abs/2108.13897
      - label: T2Ranking arXiv
        url: https://arxiv.org/abs/2304.03679
    source_notes: []
  references:
    - title: "C-Pack: Packed Resources For General Chinese Embeddings"
      url: https://arxiv.org/abs/2309.07597
      year: 2024
      is_paper: true
      source_confidence: definitive_paper_link
    - title: "Multi-CPR: A Multi Domain Chinese Dataset for Passage Retrieval"
      url: https://arxiv.org/abs/2203.03367
      year: 2022
      is_paper: true
      source_confidence: definitive_paper_link
    - title: "DuReader-retrieval: A Large-scale Chinese Benchmark for Passage Retrieval"
      url: https://aclanthology.org/2022.emnlp-main.357/
      year: 2022
      is_paper: true
      source_confidence: definitive_paper_link
    - title: "mMARCO: A Multilingual Version of the MS MARCO Passage Ranking Dataset"
      url: https://arxiv.org/abs/2108.13897
      year: 2021
      is_paper: true
      source_confidence: definitive_paper_link
    - title: "T2Ranking: A large-scale Chinese Benchmark for Passage Ranking"
      url: https://arxiv.org/abs/2304.03679
      year: 2023
      is_paper: true
      source_confidence: definitive_paper_link
```
