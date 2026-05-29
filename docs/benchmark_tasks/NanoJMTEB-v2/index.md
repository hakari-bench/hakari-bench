# NanoJMTEB-v2

## Overview

NanoJMTEB-v2 is a Japanese retrieval task group derived from JMTEB, MTEB, and
related Japanese retrieval datasets. It covers eleven retrieval settings:
Japanese casual web search, government FAQ matching, quiz-to-entity retrieval,
complex QA answer-label retrieval, MIRACL and Mr. TyDi Japanese passage
retrieval, long-document retrieval, and four Japanese NLP Journal paper
component matching tasks.

The group is useful because it is not only a Japanese version of English passage
retrieval. It includes short answer labels, noisy web snippets, official FAQ
answers, full Wikipedia-like entity pages, very long generated-question
documents, and LaTeX-like academic paper text. A model that performs well across
this group must handle Japanese tokenization, entity inference, answer-side
wording mismatch, and long-document representation.

## Details

### What the Original Group Measures

JMTEB and MTEB define Japanese retrieval tasks for embedding evaluation. In this
Nano group, the sources are mixed. JaCWIR measures broad Japanese web retrieval
from generated questions to title/description snippets. JaGovFaqs measures
question-to-answer matching over government FAQ data. JAQKET measures
quiz-question to Wikipedia entity retrieval. Mintaka Japanese measures complex
question to short answer-label retrieval. MIRACL and Mr. TyDi measure Japanese
monolingual question-passage retrieval. MultiLongDocRetrieval measures
generated-question to long-article retrieval. The NLP Journal V2 tasks measure
matching between titles, abstracts, introductions, and full articles from
Japanese NLP papers.

The observed examples confirm that these are qualitatively different retrieval
relations. `mintaka_ja` documents are short entity labels such as
`マーク・トウェイン`, while `multi_long_doc_ja` documents are full long articles.
The NLP Journal tasks often share technical vocabulary and LaTeX artifacts, but
title-to-introduction retrieval has a much shorter query side than
abstract-to-article retrieval. MIRACL and Mr. TyDi are passage-level factual
retrieval tasks with multi-positive qrels, unlike the single-positive web,
FAQ, entity, and academic component tasks.

### Subtask Coverage

The eleven subtasks cover five retrieval families:

- **Web and FAQ retrieval:** `ja_cwir` maps short generated web-search questions
  to web page title/description snippets, while `ja_gov_faqs` maps formal
  public-administration questions to FAQ answers.
- **Entity and answer retrieval:** `jaqket` maps quiz clues to full entity
  pages, and `mintaka_ja` maps complex questions to short answer labels.
- **Japanese factual passage retrieval:** `miracl_ja` and `mr_tidy_japanese`
  retrieve Japanese answer-bearing passages and include multi-positive qrels.
- **Long-document retrieval:** `multi_long_doc_ja` maps generated questions to
  long Japanese documents where the relevant span may be a small part of the
  article.
- **Academic component matching:** `nlpjournal_abs_article`,
  `nlpjournal_abs_intro`, `nlpjournal_title_abs`, and
  `nlpjournal_title_intro` link titles or abstracts to matching paper sections
  or full articles from the Japanese NLP Journal LaTeX Corpus.

All subtasks are Japanese natural-language retrieval tasks, but they vary from
single-token or short-label answer retrieval to documents averaging more than
28k characters.

### Observed Group Profile

Across the eleven splits, NanoJMTEB-v2 contains 2,200 queries, 64,140
split-local candidate documents, and 2,432 positive qrels. Every split has 200
queries. Most tasks are single-positive; only `miracl_ja` and
`mr_tidy_japanese` have multi-positive qrels. In the loaded data, MIRACL
Japanese has 78 multi-positive queries and up to 8 positives for one query,
while Mr. TyDi Japanese has 56 multi-positive queries and up to 3 positives.

Text lengths vary widely. `mintaka_ja` documents average only 9.17 characters
because the documents are answer labels. `multi_long_doc_ja` documents average
14,479.43 characters, and `nlpjournal_abs_article` full articles average
28,330.39 characters. Query lengths also differ: MIRACL and Mr. TyDi use very
short factual questions, while NLP Journal abstract queries average 494.52
characters.

### BM25 Difficulty

Because each split has 200 queries, query-weighted and unweighted BM25 means are
identical: nDCG@10 is 0.2390 and hit@10 is 0.2727. This low group average hides
a sharp split between tasks where lexical overlap is strong and tasks where
retrieval requires semantic inference.

`nlpjournal_abs_article` is easiest by nDCG@10 at 0.8267 because the abstract
and full article share technical terms, method names, and LaTeX vocabulary.
`nlpjournal_abs_intro` is also comparatively strong at 0.6417. In contrast,
`miracl_ja` is hardest by nDCG@10 at 0.0588, followed by
`mr_tidy_japanese`, `nlpjournal_title_abs`, and `nlpjournal_title_intro`.
The first loaded MIRACL query had its positive at BM25 rank 18, while the first
title-to-introduction query had its positive at rank 63. These examples match
the low shallow lexical scores.

BM25 is especially weak when the answer does not occur in the query, as in
Mintaka answer-label retrieval, or when a short title must retrieve a longer
academic section. It is also weak for FAQ answers that do not restate the full
question. Dense and reranker systems should improve by learning Japanese
semantic matching, entity inference, and component-level paper alignment.

### Training Data That May Help

Useful training data should be selected by retrieval family. Web and FAQ tasks
benefit from Japanese search logs, title/description retrieval, government FAQ
question-answer pairs, and public-service support data. Entity tasks benefit
from Japanese quiz QA, Wikipedia entity linking, and Wikidata-linked QA pairs.
MIRACL and Mr. TyDi benefit from Japanese Wikipedia passage retrieval and
monolingual QA evidence retrieval. MultiLongDoc requires generated-question to
long-article pairs and long-document hard negatives. NLP Journal tasks benefit
from title-abstract, abstract-introduction, and abstract-to-full-text academic
matching data.

Training should exclude NanoJMTEB-v2 queries, qrels, and positive documents.
Because these tasks use public benchmark sources, upstream JMTEB, MTEB, JAQKET,
Mintaka, MIRACL, Mr. TyDi, MLDR, and NLP Journal evaluation examples should be
treated as possible leakage sources unless overlap has been audited.

### Synthetic Data Guidance

Synthetic data should preserve the retrieval target type. Web-search examples
should use noisy Japanese title/description snippets, not clean answer
paragraphs. FAQ examples should include terse answers, URLs, dates, and
administrative language. Entity examples should ask clue-style questions without
always naming the answer. Answer-label examples should retrieve short labels,
not passages. Long-document examples should generate questions from a paragraph
but retrieve the full article. Academic examples should preserve the difference
between title, abstract, introduction, and full-article text.

Hard negatives should be close: same article family for MIRACL/Mr. TyDi,
same government program for FAQs, same research subfield for NLP Journal, and
same entity category for JAQKET or Mintaka. Do not seed synthetic examples from
NanoJMTEB-v2 evaluation queries or positive documents.

## Task Summary

| Task | Retrieval shape | Queries | Docs | Positives | BM25 nDCG@10 | BM25 hit@10 | Query avg chars | Doc avg chars | Source status |
| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | --- |
| [ja_cwir](ja_cwir.md) | generated web question to page snippet | 200 | 10,000 | 200 | 0.2431 | 0.2750 | 33.80 | 189.04 | JaCWIR/JMTEB cards |
| [ja_gov_faqs](ja_gov_faqs.md) | government FAQ question to answer | 200 | 10,000 | 200 | 0.1586 | 0.1650 | 59.97 | 193.38 | JMTEB card |
| [jaqket](jaqket.md) | quiz clue to entity page | 200 | 10,000 | 200 | 0.1743 | 0.2100 | 52.98 | 5,363.14 | JAQKET paper |
| [mintaka_ja](mintaka_ja.md) | complex question to answer label | 200 | 1,592 | 200 | 0.1312 | 0.1600 | 35.19 | 9.17 | Mintaka paper |
| [miracl_ja](miracl_ja.md) | Japanese question to Wikipedia passage | 200 | 10,000 | 373 | 0.0588 | 0.1000 | 17.50 | 194.29 | MIRACL paper |
| [mr_tidy_japanese](mr_tidy_japanese.md) | Japanese question to Mr. TyDi passage | 200 | 10,000 | 259 | 0.0711 | 0.1050 | 18.44 | 233.46 | Mr. TyDi paper |
| [multi_long_doc_ja](multi_long_doc_ja.md) | generated question to long article | 200 | 10,000 | 200 | 0.1436 | 0.1600 | 61.62 | 14,479.43 | M3/MLDR paper |
| [nlpjournal_abs_article](nlpjournal_abs_article.md) | abstract to full article | 200 | 637 | 200 | 0.8267 | 0.8900 | 494.52 | 28,330.39 | JMTEB + corpus cards |
| [nlpjournal_abs_intro](nlpjournal_abs_intro.md) | abstract to introduction | 200 | 637 | 200 | 0.6417 | 0.7400 | 494.52 | 2,148.04 | JMTEB + corpus cards |
| [nlpjournal_title_abs](nlpjournal_title_abs.md) | title to abstract | 200 | 637 | 200 | 0.0813 | 0.0850 | 27.02 | 461.52 | JMTEB + corpus cards |
| [nlpjournal_title_intro](nlpjournal_title_intro.md) | title to introduction | 200 | 637 | 200 | 0.0991 | 0.1100 | 27.02 | 2,148.04 | JMTEB + corpus cards |

## Dataset Information

| Field | Value |
| --- | --- |
| Nano set | NanoJMTEB-v2 |
| Backing dataset | NanoJMTEB-v2 |
| Hugging Face dataset | [hakari-bench/NanoJMTEB-v2](https://huggingface.co/datasets/hakari-bench/NanoJMTEB-v2) |
| Language | ja |
| Category | natural_language |
| Subtasks | 11 |
| Total queries | 2,200 |
| Split-local documents | 64,140 |
| Positive qrels | 2,432 |
| Positives per query | avg 1.1055, median 1, max 8 |
| Multi-positive subtasks | 2 of 11 |
| Multi-positive queries | 134 |
| Query-weighted BM25 nDCG@10 | 0.7465 |
| Query-weighted BM25 hit@10 | 0.8464 |
| Query-weighted BM25 Recall@100 | 0.9148 |
| Query-weighted Dense nDCG@10 | 0.7535 |
| Query-weighted Dense hit@10 | 0.8309 |
| Query-weighted Dense Recall@100 | 0.8868 |
| Query-weighted Reranking hybrid nDCG@10 | 0.7553 |
| Query-weighted Reranking hybrid hit@10 | 0.8455 |
| Query-weighted Reranking hybrid Recall@100 | 0.9365 |
| Mean query length | 120.23 chars, weighted by query count |
| Mean document length | 3,548.78 chars, weighted by split-local document count |

### Public Sources

- [MTEB: Massive Text Embedding Benchmark](https://arxiv.org/abs/2210.07316); 2022.
- [sbintuitions/JMTEB](https://huggingface.co/datasets/sbintuitions/JMTEB); Japanese embedding benchmark dataset card.
- [hotchpotch/JaCWIR](https://huggingface.co/datasets/hotchpotch/JaCWIR); Japanese Casual Web IR dataset card.
- [JAQKET: クイズを題材にした日本語 QA データセットの構築](https://www.anlp.jp/proceedings/annual_meeting/2020/pdf_dir/P2-24.pdf); 2020.
- [Mintaka: A Complex, Natural, and Multilingual Dataset for End-to-End Question Answering](https://aclanthology.org/2022.coling-1.138/); 2022.
- [Making a MIRACL: Multilingual Information Retrieval Across a Continuum of Languages](https://arxiv.org/abs/2210.09984); 2022.
- [Mr. TyDi: A Multi-lingual Benchmark for Dense Retrieval](https://arxiv.org/abs/2108.08787); 2021.
- [M3-Embedding: Multi-Linguality, Multi-Functionality, Multi-Granularity Text Embeddings Through Self-Knowledge Distillation](https://arxiv.org/abs/2402.03216); 2024.
- [言語処理学会論文誌 LaTeX コーパス](https://github.com/jenio/nlp-journal-latex-corpus); upstream corpus repository.

### Hugging Face Links

- Nano dataset: [hakari-bench/NanoJMTEB-v2](https://huggingface.co/datasets/hakari-bench/NanoJMTEB-v2)
- Source datasets:
  [mteb/JaCWIRRetrieval](https://huggingface.co/datasets/mteb/JaCWIRRetrieval),
  [mteb/JaGovFaqsRetrieval](https://huggingface.co/datasets/mteb/JaGovFaqsRetrieval),
  [mteb/jaqket](https://huggingface.co/datasets/mteb/jaqket),
  [mteb/MintakaRetrieval](https://huggingface.co/datasets/mteb/MintakaRetrieval),
  [mteb/MIRACLRetrieval](https://huggingface.co/datasets/mteb/MIRACLRetrieval),
  [mteb/mrtidy](https://huggingface.co/datasets/mteb/mrtidy),
  [mteb/MultiLongDocRetrieval](https://huggingface.co/datasets/mteb/MultiLongDocRetrieval),
  [mteb/NLPJournalAbsArticleRetrieval.V2](https://huggingface.co/datasets/mteb/NLPJournalAbsArticleRetrieval.V2),
  [mteb/NLPJournalAbsIntroRetrieval.V2](https://huggingface.co/datasets/mteb/NLPJournalAbsIntroRetrieval.V2),
  [mteb/NLPJournalTitleAbsRetrieval.V2](https://huggingface.co/datasets/mteb/NLPJournalTitleAbsRetrieval.V2),
  [mteb/NLPJournalTitleIntroRetrieval.V2](https://huggingface.co/datasets/mteb/NLPJournalTitleIntroRetrieval.V2).

### Source Reference Table

| Title | Year | Type | URL |
| --- | ---: | --- | --- |
| MTEB: Massive Text Embedding Benchmark | 2022 | benchmark paper | https://arxiv.org/abs/2210.07316 |
| sbintuitions/JMTEB | 2024 | dataset card | https://huggingface.co/datasets/sbintuitions/JMTEB |
| hotchpotch/JaCWIR |  | dataset card | https://huggingface.co/datasets/hotchpotch/JaCWIR |
| JAQKET: クイズを題材にした日本語 QA データセットの構築 | 2020 | source task paper | https://www.anlp.jp/proceedings/annual_meeting/2020/pdf_dir/P2-24.pdf |
| Mintaka: A Complex, Natural, and Multilingual Dataset for End-to-End Question Answering | 2022 | source task paper | https://aclanthology.org/2022.coling-1.138/ |
| Making a MIRACL: Multilingual Information Retrieval Across a Continuum of Languages | 2022 | source task paper | https://arxiv.org/abs/2210.09984 |
| Mr. TyDi: A Multi-lingual Benchmark for Dense Retrieval | 2021 | source task paper | https://arxiv.org/abs/2108.08787 |
| M3-Embedding: Multi-Linguality, Multi-Functionality, Multi-Granularity Text Embeddings Through Self-Knowledge Distillation | 2024 | source task paper | https://arxiv.org/abs/2402.03216 |
| 言語処理学会論文誌 LaTeX コーパス |  | source corpus repository | https://github.com/jenio/nlp-journal-latex-corpus |

## Machine-Readable Metadata

<!-- benchmark-task-group-metadata:v1 -->

```yaml
benchmark_task_group_metadata:
  schema_version: 1
  document_status: reviewed_manual
  nano_set: NanoJMTEB-v2
  backing_dataset: NanoJMTEB-v2
  dataset_id: hakari-bench/NanoJMTEB-v2
  language: ja
  category: natural_language
  document_path: docs/benchmark_tasks/NanoJMTEB-v2/index.md
  source_research:
    primary_source_type: task_papers_and_dataset_cards
    paper_pdf_or_html_checked: true
    no_paper_note: null
  counts:
    tasks: 11
    queries: 2200
    split_local_documents: 64140
    positive_qrels: 2432
  positives_per_query:
    average: 1.1054545454545455
    min: 1
    median: 1.0
    max: 8
    multi_positive_tasks: 2
    multi_positive_queries: 134
  text_stats_chars:
    query_mean_weighted_by_queries: 120.23454545454545
    document_mean_weighted_by_documents: 3548.7846738207672
  bm25:
    ndcg_at_10_query_weighted: 0.7465132991
    hit_at_10_query_weighted: 0.8463636364
    ndcg_at_10_unweighted_task_mean: 0.23903082157272726
    hit_at_10_unweighted_task_mean: 0.2727272727272727
    source: dataset_candidate_subset
    easiest_task_by_ndcg_at_10: nlpjournal_abs_article
    hardest_task_by_ndcg_at_10: miracl_ja
  tasks:
  - name: ja_cwir
    path: docs/benchmark_tasks/NanoJMTEB-v2/ja_cwir.md
    retrieval_shape: generated_web_question_to_page_snippet
    queries: 200
    documents: 10000
    positive_qrels: 200
    bm25_ndcg_at_10: 0.2431216201
    bm25_hit_at_10: 0.275
  - name: ja_gov_faqs
    path: docs/benchmark_tasks/NanoJMTEB-v2/ja_gov_faqs.md
    retrieval_shape: government_faq_question_to_answer
    queries: 200
    documents: 10000
    positive_qrels: 200
    bm25_ndcg_at_10: 0.1586009307
    bm25_hit_at_10: 0.165
  - name: jaqket
    path: docs/benchmark_tasks/NanoJMTEB-v2/jaqket.md
    retrieval_shape: quiz_clue_to_entity_page
    queries: 200
    documents: 10000
    positive_qrels: 200
    bm25_ndcg_at_10: 0.1743146674
    bm25_hit_at_10: 0.21
  - name: mintaka_ja
    path: docs/benchmark_tasks/NanoJMTEB-v2/mintaka_ja.md
    retrieval_shape: complex_question_to_answer_label
    queries: 200
    documents: 1592
    positive_qrels: 200
    bm25_ndcg_at_10: 0.1311528332
    bm25_hit_at_10: 0.16
  - name: miracl_ja
    path: docs/benchmark_tasks/NanoJMTEB-v2/miracl_ja.md
    retrieval_shape: japanese_question_to_wikipedia_passage
    queries: 200
    documents: 10000
    positive_qrels: 373
    bm25_ndcg_at_10: 0.0587521649
    bm25_hit_at_10: 0.1
  - name: mr_tidy_japanese
    path: docs/benchmark_tasks/NanoJMTEB-v2/mr_tidy_japanese.md
    retrieval_shape: japanese_question_to_mr_tydi_passage
    queries: 200
    documents: 10000
    positive_qrels: 259
    bm25_ndcg_at_10: 0.0710585196
    bm25_hit_at_10: 0.105
  - name: multi_long_doc_ja
    path: docs/benchmark_tasks/NanoJMTEB-v2/multi_long_doc_ja.md
    retrieval_shape: generated_question_to_long_article
    queries: 200
    documents: 10000
    positive_qrels: 200
    bm25_ndcg_at_10: 0.1435515931
    bm25_hit_at_10: 0.16
  - name: nlpjournal_abs_article
    path: docs/benchmark_tasks/NanoJMTEB-v2/nlpjournal_abs_article.md
    retrieval_shape: abstract_to_full_article
    queries: 200
    documents: 637
    positive_qrels: 200
    bm25_ndcg_at_10: 0.8266619326
    bm25_hit_at_10: 0.89
  - name: nlpjournal_abs_intro
    path: docs/benchmark_tasks/NanoJMTEB-v2/nlpjournal_abs_intro.md
    retrieval_shape: abstract_to_introduction
    queries: 200
    documents: 637
    positive_qrels: 200
    bm25_ndcg_at_10: 0.6416981491
    bm25_hit_at_10: 0.74
  - name: nlpjournal_title_abs
    path: docs/benchmark_tasks/NanoJMTEB-v2/nlpjournal_title_abs.md
    retrieval_shape: title_to_abstract
    queries: 200
    documents: 637
    positive_qrels: 200
    bm25_ndcg_at_10: 0.0813092975
    bm25_hit_at_10: 0.085
  - name: nlpjournal_title_intro
    path: docs/benchmark_tasks/NanoJMTEB-v2/nlpjournal_title_intro.md
    retrieval_shape: title_to_introduction
    queries: 200
    documents: 637
    positive_qrels: 200
    bm25_ndcg_at_10: 0.0991173291
    bm25_hit_at_10: 0.11
  source_links:
  - label: MTEB paper
    url: https://arxiv.org/abs/2210.07316
  - label: JMTEB dataset card
    url: https://huggingface.co/datasets/sbintuitions/JMTEB
  - label: JaCWIR dataset card
    url: https://huggingface.co/datasets/hotchpotch/JaCWIR
  - label: JAQKET paper
    url: https://www.anlp.jp/proceedings/annual_meeting/2020/pdf_dir/P2-24.pdf
  - label: Mintaka paper
    url: https://aclanthology.org/2022.coling-1.138/
  - label: MIRACL paper
    url: https://arxiv.org/abs/2210.09984
  - label: Mr. TyDi paper
    url: https://arxiv.org/abs/2108.08787
  - label: M3-Embedding paper
    url: https://arxiv.org/abs/2402.03216
  - label: NLP Journal LaTeX Corpus
    url: https://github.com/jenio/nlp-journal-latex-corpus
  candidate_subsets:
    bm25:
      query_weighted_ndcg_at_10: 0.7465132991
      query_weighted_hit_at_10: 0.8463636364
      query_weighted_recall_at_100: 0.914751025
      source: dataset_candidate_subset
    dense:
      query_weighted_ndcg_at_10: 0.753517748
      query_weighted_hit_at_10: 0.8309090909
      query_weighted_recall_at_100: 0.8868210849
      source: dataset_candidate_subset
    reranking_hybrid:
      query_weighted_ndcg_at_10: 0.7553409282
      query_weighted_hit_at_10: 0.8454545455
      query_weighted_recall_at_100: 0.9365340927
      source: dataset_candidate_subset
```
