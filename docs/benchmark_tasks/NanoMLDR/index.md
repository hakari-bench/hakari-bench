# NanoMLDR

## Overview

NanoMLDR is the Nano task group for MLDR, a multilingual long-document retrieval
benchmark. It covers 13 monolingual retrieval splits: Arabic, German, English,
Spanish, French, Hindi, Italian, Japanese, Korean, Portuguese, Russian, Thai, and
Chinese. Each query is a question generated from a paragraph inside a long
article, while the positive document is the full article rather than the short
answer-bearing paragraph.

The group is useful because it isolates a retrieval problem that is easy to
understate: the model must connect a short question to a very long document in
the same language. Success requires lexical and semantic matching, language
coverage, and enough long-context robustness to retrieve a whole article even
when only a small part of it answers the question.

## Details

### What the Original Group Measures

[M3-Embedding: Multi-Linguality, Multi-Functionality, Multi-Granularity Text Embeddings Through Self-Knowledge Distillation](https://arxiv.org/abs/2402.03216)
introduces the long-document setting behind MLDR as part of its multi-granularity
retrieval evaluation and training data. The paper describes a multilingual
long-document construction in which long articles are sampled from Wikipedia,
Wudao, and mC4, a paragraph is selected, and GPT-3.5 generates a question from
that paragraph. The [MLDR dataset card](https://huggingface.co/datasets/Shitao/MLDR)
gives the same construction and lists the 13 languages, data sources, train/dev
/ test sizes, corpus sizes, and average document lengths.

NanoMLDR therefore does not measure passage retrieval in the usual short-context
sense. The answer-bearing paragraph may be a small region inside a much longer
article. The retrieval target is still the article, which makes the task
particularly relevant for models or systems that advertise long input support,
sparse lexical retrieval, hybrid retrieval, or document-level indexing.

### Subtask Coverage

The group has one split per language. Most splits are Wikipedia-derived, while
German and Spanish also include mC4, Thai is mC4-only, and Chinese includes
Wikipedia plus Wudao. The observed Nano data follows this source distinction:
many Arabic, English, French, Hindi, Italian, Japanese, Korean, Portuguese, and
Russian examples are encyclopedia-like, while German and Thai include much
noisier web pages, product pages, forum pages, lodging pages, promotions, and
boilerplate.

All 13 current NanoMLDR splits are monolingual. The model is not translating
between languages, but it must handle very different scripts, segmentation
properties, named-entity conventions, and web noise. All observed qrels are
single-positive, so the main evaluation pressure is not choosing among multiple
acceptable relevant documents. It is finding the one full document that contains
the generated question's source paragraph.

### Observed Group Profile

Across the 13 splits, NanoMLDR contains 2,089 queries, 2,089 positive qrels, and
55,585 split-local candidate documents. The document count is a sum across
splits and should not be read as a deduplicated multilingual corpus size.

The queries are short compared with the documents. The query-weighted mean query
length is 79.20 characters, while the document-count-weighted mean document
length is 14,246.54 characters. English has the longest average documents in the
Nano sample at 27,991.90 characters, followed by Portuguese, Italian, Russian,
Spanish, Chinese, German, Arabic, Hindi, and French in the 11K to 15K range.
Japanese, Korean, and Thai have shorter character averages, but these still
represent long-document retrieval rather than passage retrieval.

The observed examples also show that source quality matters. Thai queries often
retrieve noisy mC4 pages with mixed scripts and commercial boilerplate. German
contains some clean articles but also product and forum-like documents. By
contrast, Portuguese, Spanish, and French examples often keep distinctive
article terms in the generated questions, which makes lexical matching much
easier.

### BM25 Difficulty

Using the dataset-provided BM25 candidate column, query-weighted BM25 nDCG@10 is
0.7178 and query-weighted hit@10 is 0.7946. The unweighted task means are very
similar, at 0.7169 nDCG@10 and 0.7932 hit@10.

The task-level spread is important. Portuguese is the easiest split for BM25 in
the current Nano data, with nDCG@10 = 0.9210 and hit@10 = 0.9716. Spanish and
French are also high, both above 0.87 nDCG@10. Thai is the hardest split, with
nDCG@10 = 0.3737 and hit@10 = 0.4503; its median best-positive BM25 rank in the
observed table is 24, and many positives are at rank 100 or missing from the top
100 candidate list. German and English are also harder than the Romance-language
Wikipedia-heavy splits because the sampled documents include noisy web pages or
very long articles where a small answer-bearing region can be diluted by the
rest of the document.

### Training Data That May Help

Useful training data includes MLDR-style paragraph-grounded question and full
article pairs, multilingual long-document QA retrieval, Wikipedia article
retrieval, mC4/Wudao web-document retrieval, and hard negatives drawn from
articles with overlapping entities, dates, product names, or topical vocabulary.
Training should preserve the document-level target: converting all documents to
short passages would change the task.

Training data should exclude NanoMLDR evaluation queries, qrels, and positive
documents. If using the public MLDR source dataset, train/dev/test split
boundaries and sampled article overlap should be audited before mixing source
examples into training.

### Synthetic Data Guidance

Synthetic data should mirror the original construction. Select a paragraph from
a long article or noisy web page, generate a specific question about that
paragraph, and use the full document as the positive. The negative pool should
contain same-language full documents with overlapping named entities, dates,
locations, web templates, or domain vocabulary, but without the answer-bearing
paragraph.

For Thai, German, Spanish, and Chinese, synthetic generation should include the
source-specific noise patterns visible in the original data, not only clean
encyclopedia text. For scripts without whitespace segmentation, examples should
preserve native punctuation and script conventions rather than transliterating
or simplifying the text.

## Task Summary

| Task | Retrieval shape | Queries | Docs | BM25 nDCG@10 | BM25 hit@10 | Query avg chars | Doc avg chars | Source status |
| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | --- |
| [ar](ar.md) | Arabic question to long Arabic article | 150 | 4,766 | 0.6630 | 0.7867 | 71.09 | 12,006.83 | M3-Embedding paper + MLDR dataset card |
| [de](de.md) | German question to long German article or web page | 117 | 5,046 | 0.5933 | 0.6667 | 81.46 | 12,343.20 | M3-Embedding paper + MLDR dataset card |
| [en](en.md) | English question to long English article | 200 | 10,000 | 0.6351 | 0.7250 | 64.06 | 27,991.90 | M3-Embedding paper + MLDR dataset card |
| [es](es.md) | Spanish question to long Spanish article | 176 | 3,312 | 0.8998 | 0.9489 | 120.26 | 12,539.90 | M3-Embedding paper + MLDR dataset card |
| [fr](fr.md) | French question to long French article | 152 | 3,059 | 0.8774 | 0.9211 | 119.92 | 11,534.15 | M3-Embedding paper + MLDR dataset card |
| [hi](hi.md) | Hindi question to long Hindi article | 159 | 2,858 | 0.6515 | 0.7421 | 79.18 | 11,900.81 | M3-Embedding paper + MLDR dataset card |
| [it](it.md) | Italian question to long Italian article | 158 | 3,116 | 0.7635 | 0.8354 | 98.16 | 14,374.38 | M3-Embedding paper + MLDR dataset card |
| [ja](ja.md) | Japanese question to long Japanese article | 148 | 3,112 | 0.7590 | 0.8446 | 51.70 | 5,384.62 | M3-Embedding paper + MLDR dataset card |
| [ko](ko.md) | Korean question to long Korean article | 177 | 3,087 | 0.7010 | 0.7740 | 55.27 | 5,915.24 | M3-Embedding paper + MLDR dataset card |
| [pt](pt.md) | Portuguese question to long Portuguese article | 141 | 3,028 | 0.9210 | 0.9716 | 110.99 | 14,744.68 | M3-Embedding paper + MLDR dataset card |
| [ru](ru.md) | Russian question to long Russian article | 160 | 3,125 | 0.7814 | 0.8500 | 92.89 | 14,163.52 | M3-Embedding paper + MLDR dataset card |
| [th](th.md) | Thai question to noisy long Thai web document | 151 | 3,199 | 0.3737 | 0.4503 | 85.25 | 4,994.82 | M3-Embedding paper + MLDR dataset card |
| [zh](zh.md) | Chinese question to long Chinese article or Wudao text | 200 | 7,877 | 0.6997 | 0.7950 | 20.68 | 12,307.31 | M3-Embedding paper + MLDR dataset card |

## Dataset Information

| Field | Value |
| --- | --- |
| Nano set | NanoMLDR |
| Backing dataset | NanoMLDR |
| Hugging Face dataset | [hakari-bench/NanoMLDR](https://huggingface.co/datasets/hakari-bench/NanoMLDR) |
| Language | multilingual: ar, de, en, es, fr, hi, it, ja, ko, pt, ru, th, zh |
| Category | natural_language |
| Subtasks | 13 |
| Total queries | 2,089 |
| Split-local documents | 55,585 |
| Positive qrels | 2,089 |
| Positives per query | exactly 1.00 for every subtask |
| Query-weighted BM25 nDCG@10 | 0.7178 |
| Query-weighted BM25 hit@10 | 0.7946 |
| Mean query length | 79.20 chars, weighted by query count |
| Mean document length | 14,246.54 chars, weighted by split-local document count |

### Public Sources

- [M3-Embedding: Multi-Linguality, Multi-Functionality, Multi-Granularity Text Embeddings Through Self-Knowledge Distillation](https://arxiv.org/abs/2402.03216); 2024; Jianlv Chen, Shitao Xiao, Peitian Zhang, Kun Luo, Defu Lian, and Zheng Liu.
- [ACL Anthology version](https://aclanthology.org/2024.findings-acl.137/); Findings of ACL 2024; DOI: `10.18653/v1/2024.findings-acl.137`.
- [MLDR dataset card](https://huggingface.co/datasets/Shitao/MLDR); 2024; Shitao Xiao et al.

### Hugging Face Links

- Nano dataset: [hakari-bench/NanoMLDR](https://huggingface.co/datasets/hakari-bench/NanoMLDR)
- Source dataset: [Shitao/MLDR](https://huggingface.co/datasets/Shitao/MLDR)

### Source Reference Table

| Title | Year | Type | URL |
| --- | ---: | --- | --- |
| M3-Embedding: Multi-Linguality, Multi-Functionality, Multi-Granularity Text Embeddings Through Self-Knowledge Distillation | 2024 | benchmark paper | https://arxiv.org/abs/2402.03216 |
| M3-Embedding ACL Anthology record | 2024 | proceedings record | https://aclanthology.org/2024.findings-acl.137/ |
| MLDR: Multilingual Long-Document Retrieval dataset | 2024 | dataset card | https://huggingface.co/datasets/Shitao/MLDR |

## Machine-Readable Metadata

<!-- benchmark-task-group-metadata:v1 -->

```yaml
benchmark_task_group_metadata:
  schema_version: 1
  document_status: reviewed_manual
  nano_set: NanoMLDR
  backing_dataset: NanoMLDR
  dataset_id: hakari-bench/NanoMLDR
  language: multilingual
  category: natural_language
  document_path: docs/benchmark_tasks/NanoMLDR/index.md
  source_research:
    primary_source_type: benchmark_paper_and_dataset_card
    paper_pdf_or_html_checked: true
    no_paper_note: null
  counts:
    tasks: 13
    queries: 2089
    split_local_documents: 55585
    positive_qrels: 2089
  positives_per_query:
    average: 1.0
    min: 1
    median: 1.0
    max: 1
    multi_positive_tasks: 0
    multi_positive_queries: 0
  text_stats_chars:
    query_mean_weighted_by_queries: 79.20344662517951
    document_mean_weighted_by_documents: 14246.537249257894
  bm25:
    ndcg_at_10_query_weighted: 0.7177946337582393
    hit_at_10_query_weighted: 0.7946385830540929
    ndcg_at_10_unweighted_task_mean: 0.7168650575081323
    hit_at_10_unweighted_task_mean: 0.7931845561201285
    source: dataset_bm25_column
    easiest_task_by_ndcg_at_10: pt
    hardest_task_by_ndcg_at_10: th
  tasks:
    - name: ar
      path: docs/benchmark_tasks/NanoMLDR/ar.md
      retrieval_shape: arabic_question_to_long_arabic_article
      queries: 150
      documents: 4766
      positive_qrels: 150
      bm25_ndcg_at_10: 0.6629625044353348
      bm25_hit_at_10: 0.7866666666666666
    - name: de
      path: docs/benchmark_tasks/NanoMLDR/de.md
      retrieval_shape: german_question_to_long_german_article_or_web_page
      queries: 117
      documents: 5046
      positive_qrels: 117
      bm25_ndcg_at_10: 0.593344802399522
      bm25_hit_at_10: 0.6666666666666666
    - name: en
      path: docs/benchmark_tasks/NanoMLDR/en.md
      retrieval_shape: english_question_to_long_english_article
      queries: 200
      documents: 10000
      positive_qrels: 200
      bm25_ndcg_at_10: 0.6351102290874667
      bm25_hit_at_10: 0.725
    - name: es
      path: docs/benchmark_tasks/NanoMLDR/es.md
      retrieval_shape: spanish_question_to_long_spanish_article
      queries: 176
      documents: 3312
      positive_qrels: 176
      bm25_ndcg_at_10: 0.8997918474653237
      bm25_hit_at_10: 0.9488636363636364
    - name: fr
      path: docs/benchmark_tasks/NanoMLDR/fr.md
      retrieval_shape: french_question_to_long_french_article
      queries: 152
      documents: 3059
      positive_qrels: 152
      bm25_ndcg_at_10: 0.8773643204517384
      bm25_hit_at_10: 0.9210526315789473
    - name: hi
      path: docs/benchmark_tasks/NanoMLDR/hi.md
      retrieval_shape: hindi_question_to_long_hindi_article
      queries: 159
      documents: 2858
      positive_qrels: 159
      bm25_ndcg_at_10: 0.6515063205133107
      bm25_hit_at_10: 0.7421383647798742
    - name: it
      path: docs/benchmark_tasks/NanoMLDR/it.md
      retrieval_shape: italian_question_to_long_italian_article
      queries: 158
      documents: 3116
      positive_qrels: 158
      bm25_ndcg_at_10: 0.7634699580512225
      bm25_hit_at_10: 0.8354430379746836
    - name: ja
      path: docs/benchmark_tasks/NanoMLDR/ja.md
      retrieval_shape: japanese_question_to_long_japanese_article
      queries: 148
      documents: 3112
      positive_qrels: 148
      bm25_ndcg_at_10: 0.758961534219206
      bm25_hit_at_10: 0.8445945945945946
    - name: ko
      path: docs/benchmark_tasks/NanoMLDR/ko.md
      retrieval_shape: korean_question_to_long_korean_article
      queries: 177
      documents: 3087
      positive_qrels: 177
      bm25_ndcg_at_10: 0.7010081474034279
      bm25_hit_at_10: 0.7740112994350282
    - name: pt
      path: docs/benchmark_tasks/NanoMLDR/pt.md
      retrieval_shape: portuguese_question_to_long_portuguese_article
      queries: 141
      documents: 3028
      positive_qrels: 141
      bm25_ndcg_at_10: 0.9210128865930197
      bm25_hit_at_10: 0.9716312056737588
    - name: ru
      path: docs/benchmark_tasks/NanoMLDR/ru.md
      retrieval_shape: russian_question_to_long_russian_article
      queries: 160
      documents: 3125
      positive_qrels: 160
      bm25_ndcg_at_10: 0.7813743571573165
      bm25_hit_at_10: 0.85
    - name: th
      path: docs/benchmark_tasks/NanoMLDR/th.md
      retrieval_shape: thai_question_to_noisy_long_thai_web_document
      queries: 151
      documents: 3199
      positive_qrels: 151
      bm25_ndcg_at_10: 0.3736837737601653
      bm25_hit_at_10: 0.4503311258278146
    - name: zh
      path: docs/benchmark_tasks/NanoMLDR/zh.md
      retrieval_shape: chinese_question_to_long_chinese_article_or_wudao_text
      queries: 200
      documents: 7877
      positive_qrels: 200
      bm25_ndcg_at_10: 0.6996550660686651
      bm25_hit_at_10: 0.795
  learning:
    leakage_note: exclude NanoMLDR evaluation queries, qrels, and positive documents; audit source MLDR split and article overlap before using public MLDR data for training
    useful_training_data:
      - MLDR-style paragraph-grounded question and full-article retrieval pairs
      - multilingual Wikipedia long-document retrieval
      - mC4 and Wudao web-document retrieval with source-language hard negatives
      - multilingual long-document QA and entity-overlap hard negatives
    synthetic_data:
      document_generation: long same-language articles or noisy web pages with one selected answer-bearing paragraph
      question_generation: specific paragraph-grounded questions in the same language as the document
      answerability: the full document must contain the paragraph needed to answer the generated question
    multi_positive_training: single_positive_question_document_focus
  links:
    nano_dataset: https://huggingface.co/datasets/hakari-bench/NanoMLDR
    source_urls:
      - label: M3-Embedding arXiv
        url: https://arxiv.org/abs/2402.03216
      - label: M3-Embedding ACL Anthology
        url: https://aclanthology.org/2024.findings-acl.137/
      - label: Shitao/MLDR
        url: https://huggingface.co/datasets/Shitao/MLDR
    source_notes: []
  references:
    - title: "M3-Embedding: Multi-Linguality, Multi-Functionality, Multi-Granularity Text Embeddings Through Self-Knowledge Distillation"
      url: https://arxiv.org/abs/2402.03216
      year: 2024
      doi: 10.18653/v1/2024.findings-acl.137
      is_paper: true
      source_confidence: definitive_paper_link
    - title: "MLDR: Multilingual Long-Document Retrieval dataset"
      url: https://huggingface.co/datasets/Shitao/MLDR
      year: 2024
      is_paper: false
      source_confidence: official_dataset_card
```
