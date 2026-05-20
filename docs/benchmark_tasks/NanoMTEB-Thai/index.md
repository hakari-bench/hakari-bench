# NanoMTEB-Thai

> [!NOTE]
> This page was prepared by manual review of source papers, dataset cards,
> repository metadata, and sampled benchmark data. It may contain mistakes;
> please treat it as a reference aid rather than a definitive source.

## Overview

NanoMTEB-Thai is a compact Thai retrieval group aligned with MTEB-style task
families. It covers cross-lingual and monolingual Belebele reading
comprehension retrieval, Thai MIRACL and Mr. TyDi Wikipedia retrieval,
Thai MKQA answer-label retrieval, Thai long-document retrieval, WebFAQ
question-answer retrieval, and Thai XQuAD context retrieval. The group is
therefore a mixture of same-language Thai retrieval, Thai-English alignment,
short answer-string retrieval, and long-document retrieval.

## Details

### What the Original Group Measures

The group draws from several multilingual retrieval sources. Belebele provides
parallel reading-comprehension passages and questions, allowing both Thai-Thai
and Thai-English retrieval directions. MIRACL and Mr. TyDi measure monolingual
Thai retrieval over Wikipedia-style evidence passages. MKQA converts
multilingual open-domain QA into retrieval of short answer labels. MLDR /
MultiLongDocRetrieval asks generated questions against very long documents.
WebFAQ uses natural FAQ question-answer pairs mined from web pages, and XQuAD
uses translated SQuAD-style questions and contexts.

The retrieval unit changes substantially across tasks. Some positives are
single short answer labels, some are small reading-comprehension passages, some
are Wikipedia passages, and one split retrieves full long documents that can
span tens of thousands of characters. This makes the group useful for testing
whether Thai retrieval quality holds across granularity, language direction,
and document length.

### Subtask Coverage

The nine subtasks cover six retrieval families:

- **Belebele reading-comprehension retrieval:** three directions test Thai
  questions to English passages, English questions to Thai passages, and
  Thai questions to Thai passages.
- **Thai Wikipedia retrieval:** `miracl_th` and `mr_tidy_thai` retrieve Thai
  evidence passages for factual questions.
- **Short answer-label retrieval:** `mkqa_th` maps Thai questions to short
  accepted answers such as names, dates, numbers, or locations.
- **Long-document retrieval:** `multi_long_doc_th` retrieves full long Thai
  documents from generated questions.
- **FAQ retrieval:** `web_faq_tha` retrieves answer snippets from broad web FAQ
  pages.
- **Translated QA context retrieval:** `xqu_ad_th` retrieves the Thai context
  paragraph that contains the answer to a translated QA question.

Most tasks are Thai, but the group is marked multilingual because several
splits intentionally mix Thai and English. The two cross-lingual Belebele
directions are the clearest case, and MKQA contains Thai questions with answer
labels in Thai, English, dates, and numeric forms.

### Observed Group Profile

Across the nine splits, NanoMTEB-Thai contains 1,800 queries, 2,077 positive
qrels, and 48,356 split-local candidate documents. The document count is a sum
across subtasks, not a deduplicated group-wide corpus size. The group average
is 1.15 positives per query, with 167 multi-positive queries. Multi-positive
labels appear in `miracl_th`, `mkqa_th`, and `mr_tidy_thai`; the largest
observed relevance set has seven positives.

The average query length is 58.65 characters, weighted by query count. Document
length is dominated by `multi_long_doc_th`, where documents average 25,993.27
characters and include noisy long web-style pages. Without that split, many
tasks use mid-length passages or short answers. `mkqa_th` is the shortest
document task, with answer labels averaging only 13.40 characters, while the
Belebele and Wikipedia-style tasks mostly use passages of a few hundred
characters.

### BM25 Difficulty

The query-weighted BM25 baseline reaches nDCG@10 = 0.4400 and hit@10 = 0.5183.
The easiest split by nDCG@10 is `xqu_ad_th` at 0.8035, helped by a small
240-document same-language context corpus and repeated passage terms. `mr_tidy_thai`,
Thai-Thai Belebele, and `web_faq_tha` are also favorable to BM25 because
queries and documents share Thai entity names or FAQ wording.

The hardest split is `mkqa_th` at nDCG@10 = 0.0132. This is expected because
the positive is often a short answer label that does not appear in the question.
The cross-lingual Belebele directions are also hard for sparse retrieval:
Thai-to-English and English-to-Thai matching has little lexical overlap beyond
names and numbers. `multi_long_doc_th` is a different challenge; BM25 can find
matching terms inside long documents, but long web pages and boilerplate create
many noisy false positives.

### Training Data That May Help

Useful training data should match the retrieval family. Thai Wikipedia QA,
MIRACL Thai, Mr. TyDi Thai, and XQuAD-style question-to-context pairs help the
same-language evidence retrieval tasks. Thai-English parallel retrieval,
translated QA, and multilingual reading-comprehension pairs help the
cross-lingual Belebele directions. MKQA-like training should include
question-to-answer-label supervision where the answer text is often absent from
the query. Long-document training should use paragraph-to-document or
question-to-article pairs with noisy long negatives. WebFAQ training should use
Thai and multilingual FAQ question-answer pairs, including site-specific hard
negatives.

Training should exclude NanoMTEB-Thai evaluation queries, qrels, positive
documents, answer strings, generated long-document questions, and upstream
evaluation rows. Multi-positive labels in MIRACL, MKQA, and Mr. TyDi should be
preserved rather than collapsed.

### Synthetic Data Guidance

Synthetic data should preserve each retrieval relation. For Belebele-like data,
generate Thai or English questions from parallel passages and keep the
retrieval direction explicit. For Thai Wikipedia retrieval, generate factual
questions over Thai passages with hard negatives from related entities. For
MKQA, generate Thai open-domain questions and short canonical answer labels of
the same answer type. For long-document retrieval, generate questions from a
specific paragraph while using the full long source document as the positive.
For WebFAQ and XQuAD, generate Thai FAQ or translated QA questions with
answer-bearing passages and adjacent same-topic hard negatives.

Synthetic examples should not use NanoMTEB-Thai evaluation questions, positive
documents, answer labels, or generated long-document rows as seeds.

## Task Summary

| Task | Retrieval shape | Lang | Queries | Docs | Positive qrels | BM25 nDCG@10 | BM25 hit@10 | Query avg chars | Doc avg chars | Source status |
| --- | --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | --- |
| [belebele_eng_latn_tha_thai](belebele_eng_latn_tha_thai.md) | Thai question to English passage | multilingual | 200 | 488 | 200 | 0.0809 | 0.0950 | 57.67 | 475.51 | Belebele paper |
| [belebele_tha_thai_eng_latn](belebele_tha_thai_eng_latn.md) | English question to Thai passage | multilingual | 200 | 488 | 200 | 0.0395 | 0.0750 | 81.31 | 456.17 | Belebele paper |
| [belebele_tha_thai_tha_thai](belebele_tha_thai_tha_thai.md) | Thai question to Thai passage | th | 200 | 488 | 200 | 0.7271 | 0.8150 | 57.67 | 456.17 | Belebele paper |
| [miracl_th](miracl_th.md) | Thai query to Wikipedia passages | th | 200 | 10,000 | 343 | 0.5737 | 0.8150 | 43.59 | 471.83 | MIRACL paper |
| [mkqa_th](mkqa_th.md) | Thai question to short answer label | multilingual | 200 | 6,652 | 300 | 0.0132 | 0.0350 | 40.20 | 13.40 | MKQA paper |
| [mr_tidy_thai](mr_tidy_thai.md) | Thai question to evidence passage | th | 200 | 10,000 | 234 | 0.7291 | 0.8000 | 41.59 | 416.31 | Mr. TyDi paper |
| [multi_long_doc_th](multi_long_doc_th.md) | Thai generated question to long document | th | 200 | 10,000 | 200 | 0.3425 | 0.4000 | 107.79 | 25,993.27 | MLDR / M3-Embedding |
| [web_faq_tha](web_faq_tha.md) | Thai FAQ question to answer snippet | th | 200 | 10,000 | 200 | 0.6501 | 0.7450 | 43.88 | 224.32 | WebFAQ paper |
| [xqu_ad_th](xqu_ad_th.md) | Thai QA question to context paragraph | th | 200 | 240 | 200 | 0.8035 | 0.8850 | 54.18 | 736.76 | XQuAD paper |

## Dataset Information

| Field | Value |
| --- | --- |
| Nano set | NanoMTEB-Thai |
| Backing dataset | NanoMTEB-Thai |
| Hugging Face dataset | [hakari-bench/NanoMTEB-Thai](https://huggingface.co/datasets/hakari-bench/NanoMTEB-Thai) |
| Languages | th, en, multilingual |
| Category | natural_language |
| Subtasks | 9 |
| Total queries | 1,800 |
| Split-local documents | 48,356 |
| Positive qrels | 2,077 |
| Positives per query | 1.15 average |
| Multi-positive queries | 167 |
| Query-weighted BM25 nDCG@10 | 0.4400 |
| Query-weighted BM25 hit@10 | 0.5183 |
| Mean query length | 58.65 chars, weighted by query count |
| Mean document length | 5,624.96 chars, weighted by split-local document count |

### Public Sources

- [MTEB: Massive Text Embedding Benchmark](https://arxiv.org/abs/2210.07316); benchmark packaging context.
- [The Belebele Benchmark](https://arxiv.org/abs/2308.16884); parallel reading-comprehension source.
- [Making a MIRACL](https://arxiv.org/abs/2210.09984); multilingual Wikipedia retrieval source.
- [MKQA](https://arxiv.org/abs/2007.15207); multilingual open-domain QA source.
- [Mr. TyDi](https://arxiv.org/abs/2108.08787); monolingual dense retrieval source.
- [M3-Embedding / MLDR](https://arxiv.org/abs/2402.03216); long-document retrieval source context.
- [WebFAQ](https://arxiv.org/abs/2502.20936); multilingual FAQ retrieval source.
- [On the Cross-lingual Transferability of Monolingual Representations](https://arxiv.org/abs/1910.11856); XQuAD source context.

### Hugging Face Links

- Nano dataset: [hakari-bench/NanoMTEB-Thai](https://huggingface.co/datasets/hakari-bench/NanoMTEB-Thai)
- Source examples:
  [mteb/belebele](https://huggingface.co/datasets/mteb/belebele),
  [mteb/MIRACLRetrievalHardNegatives](https://huggingface.co/datasets/mteb/MIRACLRetrievalHardNegatives),
  [mteb/MKQARetrieval](https://huggingface.co/datasets/mteb/MKQARetrieval),
  [mteb/mrtidy](https://huggingface.co/datasets/mteb/mrtidy),
  [mteb/MultiLongDocRetrieval](https://huggingface.co/datasets/mteb/MultiLongDocRetrieval),
  [mteb/WebFAQRetrieval](https://huggingface.co/datasets/mteb/WebFAQRetrieval),
  [google/xquad](https://huggingface.co/datasets/google/xquad).

### Source Reference Table

| Title | Year | Type | URL |
| --- | ---: | --- | --- |
| MTEB: Massive Text Embedding Benchmark | 2023 | benchmark paper | https://arxiv.org/abs/2210.07316 |
| The Belebele Benchmark: a Parallel Reading Comprehension Dataset in 122 Language Variants | 2023 | source task paper | https://arxiv.org/abs/2308.16884 |
| Making a MIRACL: Multilingual Information Retrieval Across a Continuum of Languages | 2022 | source task paper | https://arxiv.org/abs/2210.09984 |
| MKQA: A Linguistically Diverse Benchmark for Multilingual Open Domain Question Answering | 2020 | source task paper | https://arxiv.org/abs/2007.15207 |
| Mr. TyDi: A Multi-lingual Benchmark for Dense Retrieval | 2021 | source task paper | https://arxiv.org/abs/2108.08787 |
| M3-Embedding: Multi-Linguality, Multi-Functionality, Multi-Granularity Text Embeddings Through Self-Knowledge Distillation | 2024 | source task paper | https://arxiv.org/abs/2402.03216 |
| WebFAQ: A Multilingual Collection of Natural Q&A Datasets for Dense Retrieval | 2025 | source task paper | https://arxiv.org/abs/2502.20936 |
| On the Cross-lingual Transferability of Monolingual Representations | 2019 | source task paper | https://arxiv.org/abs/1910.11856 |

## Machine-Readable Metadata

<!-- benchmark-task-group-metadata:v1 -->

```yaml
benchmark_task_group_metadata:
  schema_version: 1
  document_status: reviewed_manual
  nano_set: NanoMTEB-Thai
  backing_dataset: NanoMTEB-Thai
  dataset_id: hakari-bench/NanoMTEB-Thai
  language: multilingual
  languages:
    - th
    - en
    - multilingual
  category: natural_language
  document_path: docs/benchmark_tasks/NanoMTEB-Thai/index.md
  source_research:
    primary_source_type: multiple_task_papers_and_dataset_cards
    paper_pdf_or_html_checked: true
    no_paper_note: null
  counts:
    tasks: 9
    queries: 1800
    split_local_documents: 48356
    positive_qrels: 2077
  positives_per_query:
    average: 1.153888888888889
    min: 1
    median_task_median: 1.0
    max: 7
    multi_positive_tasks: 3
    multi_positive_queries: 167
  text_stats_chars:
    query_mean_weighted_by_queries: 58.653333333333336
    document_mean_weighted_by_documents: 5624.959984336587
  bm25:
    ndcg_at_10_query_weighted: 0.43996005250000003
    hit_at_10_query_weighted: 0.5183333333333333
    ndcg_at_10_unweighted_task_mean: 0.43996005250000003
    hit_at_10_unweighted_task_mean: 0.5183333333333333
    source: dataset_bm25_column
    easiest_task_by_ndcg_at_10: xqu_ad_th
    hardest_task_by_ndcg_at_10: mkqa_th
  tasks:
    - name: belebele_eng_latn_tha_thai
      path: docs/benchmark_tasks/NanoMTEB-Thai/belebele_eng_latn_tha_thai.md
      retrieval_shape: thai_question_to_english_passage
      language: multilingual
      queries: 200
      documents: 488
      positive_qrels: 200
      bm25_ndcg_at_10: 0.0808654178
      bm25_hit_at_10: 0.095
    - name: belebele_tha_thai_eng_latn
      path: docs/benchmark_tasks/NanoMTEB-Thai/belebele_tha_thai_eng_latn.md
      retrieval_shape: english_question_to_thai_passage
      language: multilingual
      queries: 200
      documents: 488
      positive_qrels: 200
      bm25_ndcg_at_10: 0.0394649682
      bm25_hit_at_10: 0.075
    - name: belebele_tha_thai_tha_thai
      path: docs/benchmark_tasks/NanoMTEB-Thai/belebele_tha_thai_tha_thai.md
      retrieval_shape: thai_question_to_thai_passage
      language: th
      queries: 200
      documents: 488
      positive_qrels: 200
      bm25_ndcg_at_10: 0.7271309311
      bm25_hit_at_10: 0.815
    - name: miracl_th
      path: docs/benchmark_tasks/NanoMTEB-Thai/miracl_th.md
      retrieval_shape: thai_query_to_wikipedia_passages
      language: th
      queries: 200
      documents: 10000
      positive_qrels: 343
      bm25_ndcg_at_10: 0.5737129626
      bm25_hit_at_10: 0.815
    - name: mkqa_th
      path: docs/benchmark_tasks/NanoMTEB-Thai/mkqa_th.md
      retrieval_shape: thai_question_to_short_answer_label
      language: multilingual
      queries: 200
      documents: 6652
      positive_qrels: 300
      bm25_ndcg_at_10: 0.013244828
      bm25_hit_at_10: 0.035
    - name: mr_tidy_thai
      path: docs/benchmark_tasks/NanoMTEB-Thai/mr_tidy_thai.md
      retrieval_shape: thai_question_to_evidence_passage
      language: th
      queries: 200
      documents: 10000
      positive_qrels: 234
      bm25_ndcg_at_10: 0.7290643071
      bm25_hit_at_10: 0.8
    - name: multi_long_doc_th
      path: docs/benchmark_tasks/NanoMTEB-Thai/multi_long_doc_th.md
      retrieval_shape: thai_generated_question_to_long_document
      language: th
      queries: 200
      documents: 10000
      positive_qrels: 200
      bm25_ndcg_at_10: 0.3425451901
      bm25_hit_at_10: 0.4
    - name: web_faq_tha
      path: docs/benchmark_tasks/NanoMTEB-Thai/web_faq_tha.md
      retrieval_shape: thai_faq_question_to_answer_snippet
      language: th
      queries: 200
      documents: 10000
      positive_qrels: 200
      bm25_ndcg_at_10: 0.6501360545
      bm25_hit_at_10: 0.745
    - name: xqu_ad_th
      path: docs/benchmark_tasks/NanoMTEB-Thai/xqu_ad_th.md
      retrieval_shape: thai_qa_question_to_context_paragraph
      language: th
      queries: 200
      documents: 240
      positive_qrels: 200
      bm25_ndcg_at_10: 0.8034758131
      bm25_hit_at_10: 0.885
  learning:
    leakage_note: exclude NanoMTEB-Thai evaluation queries, qrels, positive passages, answer labels, generated long-document rows, FAQ answers, XQuAD contexts, and upstream dev/test rows from training
    useful_training_data:
      - Thai and English-Thai parallel reading-comprehension retrieval pairs
      - Thai MIRACL, Mr. TyDi, XQuAD, and Wikipedia QA retrieval pairs
      - MKQA-style Thai question-to-answer-label supervision
      - Thai long-document paragraph-to-document retrieval examples
      - Thai and multilingual FAQ question-answer retrieval data
      - hard negatives from the same passage topic, entity family, answer type, long-document topic, FAQ site, or adjacent QA context
    synthetic_data:
      document_generation: Thai and English passages, short answer labels, Thai Wikipedia passages, long Thai documents, FAQ answers, and XQuAD-style context paragraphs in source-like style
      question_generation: Thai and English reading-comprehension questions, Thai factual questions, Thai answer-label questions, generated long-document questions, and FAQ questions grounded in generated documents
      answerability: positives must preserve cross-lingual passage grounding, evidence passage support, answer-label identity, long-document containment, FAQ answerability, or context-level QA grounding rather than broad topic overlap
    multi_positive_training: preserve_miracl_mkqa_and_mr_tidy_multi_positive_qrels
  links:
    nano_dataset: https://huggingface.co/datasets/hakari-bench/NanoMTEB-Thai
    source_urls:
      - label: MTEB arXiv
        url: https://arxiv.org/abs/2210.07316
      - label: Belebele arXiv
        url: https://arxiv.org/abs/2308.16884
      - label: MIRACL arXiv
        url: https://arxiv.org/abs/2210.09984
      - label: MKQA arXiv
        url: https://arxiv.org/abs/2007.15207
      - label: Mr. TyDi arXiv
        url: https://arxiv.org/abs/2108.08787
      - label: M3-Embedding arXiv
        url: https://arxiv.org/abs/2402.03216
      - label: WebFAQ arXiv
        url: https://arxiv.org/abs/2502.20936
      - label: XQuAD source paper
        url: https://arxiv.org/abs/1910.11856
    source_notes: []
  references:
    - title: "MTEB: Massive Text Embedding Benchmark"
      url: https://arxiv.org/abs/2210.07316
      year: 2023
      is_paper: true
      source_confidence: definitive_paper_link
    - title: "The Belebele Benchmark: a Parallel Reading Comprehension Dataset in 122 Language Variants"
      url: https://arxiv.org/abs/2308.16884
      year: 2023
      is_paper: true
      source_confidence: definitive_paper_link
    - title: "Making a MIRACL: Multilingual Information Retrieval Across a Continuum of Languages"
      url: https://arxiv.org/abs/2210.09984
      year: 2022
      is_paper: true
      source_confidence: definitive_paper_link
    - title: "MKQA: A Linguistically Diverse Benchmark for Multilingual Open Domain Question Answering"
      url: https://arxiv.org/abs/2007.15207
      year: 2020
      is_paper: true
      source_confidence: definitive_paper_link
    - title: "Mr. TyDi: A Multi-lingual Benchmark for Dense Retrieval"
      url: https://arxiv.org/abs/2108.08787
      year: 2021
      is_paper: true
      source_confidence: definitive_paper_link
    - title: "M3-Embedding: Multi-Linguality, Multi-Functionality, Multi-Granularity Text Embeddings Through Self-Knowledge Distillation"
      url: https://arxiv.org/abs/2402.03216
      year: 2024
      is_paper: true
      source_confidence: definitive_paper_link
    - title: "WebFAQ: A Multilingual Collection of Natural Q&A Datasets for Dense Retrieval"
      url: https://arxiv.org/abs/2502.20936
      year: 2025
      is_paper: true
      source_confidence: definitive_paper_link
    - title: "On the Cross-lingual Transferability of Monolingual Representations"
      url: https://arxiv.org/abs/1910.11856
      year: 2019
      is_paper: true
      source_confidence: definitive_paper_link
```
