# NanoMTEB-Spanish

## Overview

NanoMTEB-Spanish is a compact Spanish retrieval group that combines Spanish
and Spanish-English retrieval tasks from MTEB-style benchmarks. It covers
complex entity-answer QA, Spanish Wikipedia passage retrieval, Spanish
consumer-health passage and document retrieval, and product question answering
in both monolingual and cross-lingual directions. The group is therefore useful
for separating models that only handle Spanish lexical passage matching from
models that can retrieve short answers, multilingual entities, health evidence,
and cross-lingual product snippets.

The original task mix makes relevance granular in different ways. Mintaka
positives can be short entity answers, MIRACL positives are Wikipedia evidence
passages, Spanish Passage Retrieval distinguishes full health pages from answer
passages, and xPQA uses compact product answers with multiple valid snippets.
The main evaluation question is whether Spanish retrieval remains reliable when
the target is not simply a Spanish paragraph with overlapping query terms.

## Details

### What the Original Group Measures

The group is aligned with MTEB retrieval task families. `mintaka_es` adapts
Mintaka complex QA into answer-string retrieval. `miracl_es` uses the Spanish
MIRACL ad hoc retrieval setting over Wikipedia passages. The two Spanish
Passage Retrieval splits come from a health information retrieval test
collection with Spanish consumer questions and web resources. The three xPQA
splits test product question answering as candidate retrieval, including
Spanish-to-English, English-to-Spanish, and Spanish-to-Spanish directions.

The retrieval units are intentionally heterogeneous. Mintaka positives are very
short answer strings or entity names. MIRACL positives are Spanish Wikipedia
passages. Spanish Passage Retrieval has both full web pages and short
answer-bearing passages. xPQA documents are compact product answer snippets,
often informal, elliptical, and multi-positive.

### Subtask Coverage

The seven subtasks cover four main families:

- **Complex entity-answer retrieval:** `mintaka_es` maps Spanish complex
  questions to short answer strings, many of which are names or titles.
- **Spanish Wikipedia retrieval:** `miracl_es` retrieves Spanish passages for
  native Spanish information needs, with multiple relevant passages for many
  queries.
- **Spanish health retrieval:** `spanish_passage_s2_p` retrieves full health
  web pages, while `spanish_passage_s2_s` retrieves shorter answer passages for
  the same consumer-health question set.
- **Product QA retrieval:** `xpqa_eng_spa`, `xpqa_spa_eng`, and
  `xpqa_spa_spa` retrieve product answer snippets across Spanish-English,
  English-Spanish, and Spanish-Spanish directions.

The group language is marked multilingual because four tasks contain Spanish
and English either by design or through answer/entity strings. The most
important cross-lingual pressure comes from xPQA, where BM25 must bridge
Spanish questions to English product snippets or English questions to Spanish
snippets.

### Observed Group Profile

Across the seven splits, NanoMTEB-Spanish contains 1,334 queries, 4,806
positive qrels, and 25,262 split-local candidate documents. The document count
is summed across subtasks rather than deduplicated across the group. The group
average is 3.60 positives per query, with 877 multi-positive queries. The
maximum relevance set size is 20 in `spanish_passage_s2_s`.

Text length varies by task. `mintaka_es` has answer documents averaging only
14.29 characters, making it closer to entity answer selection than passage
retrieval. xPQA documents are also short, around 68 to 123 characters depending
on direction. In contrast, `spanish_passage_s2_p` uses full health web pages
averaging 2,710.85 characters, while `miracl_es` uses mid-length Wikipedia
passages averaging 555.02 characters. The query-weighted mean query length is
54.74 characters, and the document-weighted mean document length is 1,049.92
characters.

### BM25 Difficulty

The query-weighted BM25 baseline reaches nDCG@10 = 0.3351 and hit@10 = 0.5540.
The easiest split by nDCG@10 is `miracl_es` at 0.5246. Its hit@10 is high
because Spanish queries and Spanish Wikipedia passages often share named
entities, titles, and topical terms, although ordering all relevant passages
remains harder.

The hardest split is `xpqa_eng_spa` at nDCG@10 = 0.0946, with
`xpqa_spa_eng` close behind at 0.1162. These cross-lingual product QA tasks
have short snippets and little direct token overlap between question and
answer. `mintaka_es` is also difficult for BM25 because the correct answer may
be a short name such as a person, film, or organization that is not repeated in
the Spanish question. The Spanish health splits have much higher hit@10 than
xPQA, but their nDCG remains moderate because many questions have numerous
relevant pages or passages and BM25 does not always rank all of them early.

### Training Data That May Help

Useful training data should match each retrieval family. For `mintaka_es`, use
non-overlapping Mintaka examples, Spanish Wikidata QA, and multilingual
entity-answer supervision. For `miracl_es`, use MIRACL Spanish training data
and Spanish Wikipedia question-passage pairs. For the health splits, use
Spanish consumer-health QA, medical FAQ passage retrieval, and document-level
health web retrieval examples with multiple positives preserved. For xPQA, use
in-domain product QA ranking data in Spanish and English, translated product
questions, and hard negatives from the same product category.

Training should exclude the Nano evaluation queries, qrels, positive documents,
answer strings, product snippets, and health passages. Multi-positive behavior
is central for MIRACL, Spanish Passage Retrieval, and xPQA, so positives should
not be collapsed into a single canonical document.

### Synthetic Data Guidance

Synthetic data should stay close to source task semantics. For Mintaka-style
data, generate Spanish complex questions over Wikidata-like entities and use
short canonical answers. For MIRACL-style data, generate Spanish
Wikipedia-like passages and native search questions with several relevant
passages per query. For health retrieval, generate Spanish layperson questions
about baby care, vaccination, emergency care, and low back pain, paired with
both full pages and concise answer passages. For xPQA, generate product
questions and answer snippets in Spanish and English, preserving yes/no
polarity, quantities, model codes, dimensions, compatibility, and customer
reported facts.

Synthetic examples should not use NanoMTEB-Spanish evaluation questions,
positive documents, answer strings, or product candidates as seeds.

## Task Summary

| Task | Retrieval shape | Lang | Queries | Docs | Positive qrels | BM25 nDCG@10 | BM25 hit@10 | Query avg chars | Doc avg chars | Source status |
| --- | --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | --- |
| [mintaka_es](mintaka_es.md) | Spanish complex question to short answer | multilingual | 200 | 1,693 | 200 | 0.2467 | 0.3050 | 66.93 | 14.29 | Mintaka paper / MTEB |
| [miracl_es](miracl_es.md) | Spanish query to Wikipedia passages | es | 200 | 10,000 | 934 | 0.5246 | 0.9300 | 47.65 | 555.02 | MIRACL paper / MTEB |
| [spanish_passage_s2_p](spanish_passage_s2_p.md) | Spanish health question to full web page | es | 167 | 7,501 | 996 | 0.4831 | 0.8922 | 67.56 | 2,710.85 | Spanish Passage Retrieval |
| [spanish_passage_s2_s](spanish_passage_s2_s.md) | Spanish health question to answer passage | es | 167 | 250 | 1,228 | 0.4893 | 0.8922 | 67.56 | 442.43 | Spanish Passage Retrieval |
| [xpqa_eng_spa](xpqa_eng_spa.md) | Spanish product question to English answer snippet | multilingual | 200 | 1,936 | 491 | 0.0946 | 0.1750 | 45.16 | 123.43 | xPQA paper |
| [xpqa_spa_eng](xpqa_spa_eng.md) | English product question to Spanish answer snippet | multilingual | 200 | 1,941 | 469 | 0.1162 | 0.1750 | 47.42 | 68.28 | xPQA paper |
| [xpqa_spa_spa](xpqa_spa_spa.md) | Spanish product question to Spanish answer snippet | es | 200 | 1,941 | 488 | 0.4409 | 0.6200 | 45.16 | 68.28 | xPQA paper |

## Dataset Information

| Field | Value |
| --- | --- |
| Nano set | NanoMTEB-Spanish |
| Backing dataset | NanoMTEB-Spanish |
| Hugging Face dataset | [hakari-bench/NanoMTEB-Spanish](https://huggingface.co/datasets/hakari-bench/NanoMTEB-Spanish) |
| Languages | es, en, multilingual |
| Category | natural_language |
| Subtasks | 7 |
| Total queries | 1,334 |
| Split-local documents | 25,262 |
| Positive qrels | 4,806 |
| Positives per query | 3.60 average |
| Multi-positive queries | 877 |
| Query-weighted BM25 nDCG@10 | 0.3351 |
| Query-weighted BM25 hit@10 | 0.5540 |
| Mean query length | 54.74 chars, weighted by query count |
| Mean document length | 1,049.92 chars, weighted by split-local document count |

### Public Sources

- [MTEB: Massive Text Embedding Benchmark](https://arxiv.org/abs/2210.07316); 2023; group packaging context.
- [Mintaka: A Complex, Natural, and Multilingual Dataset for End-to-End Question Answering](https://arxiv.org/abs/2210.01613); 2022; complex multilingual QA source.
- [Making a MIRACL](https://arxiv.org/abs/2210.09984); 2023; multilingual Wikipedia retrieval source.
- [Spanish Passage Retrieval dataset page](https://mklab.iti.gr/results/spanish-passage-retrieval-dataset/); Spanish health retrieval collection.
- [A Test Collection for Passage Retrieval Evaluation of Spanish Health-Related Resources](https://doi.org/10.1007/978-3-030-15719-7_19); ECIR 2019 paper for the health collection.
- [xPQA: Cross-Lingual Product Question Answering across 12 Languages](https://arxiv.org/abs/2305.09249); 2023; product QA retrieval source.

### Hugging Face Links

- Nano dataset: [hakari-bench/NanoMTEB-Spanish](https://huggingface.co/datasets/hakari-bench/NanoMTEB-Spanish)
- Source examples:
  [mteb/MintakaRetrieval](https://huggingface.co/datasets/mteb/MintakaRetrieval),
  [mteb/MIRACLRetrievalHardNegatives](https://huggingface.co/datasets/mteb/MIRACLRetrievalHardNegatives),
  [mteb/SpanishPassageRetrievalS2P](https://huggingface.co/datasets/mteb/SpanishPassageRetrievalS2P),
  [mteb/SpanishPassageRetrievalS2S](https://huggingface.co/datasets/mteb/SpanishPassageRetrievalS2S),
  [mteb/XPQARetrieval](https://huggingface.co/datasets/mteb/XPQARetrieval).

### Source Reference Table

| Title | Year | Type | URL |
| --- | ---: | --- | --- |
| MTEB: Massive Text Embedding Benchmark | 2023 | benchmark paper | https://arxiv.org/abs/2210.07316 |
| Mintaka: A Complex, Natural, and Multilingual Dataset for End-to-End Question Answering | 2022 | source task paper | https://arxiv.org/abs/2210.01613 |
| Making a MIRACL: Multilingual Information Retrieval Across a Continuum of Languages | 2023 | source task paper | https://arxiv.org/abs/2210.09984 |
| A Test Collection for Passage Retrieval Evaluation of Spanish Health-Related Resources | 2019 | source task paper | https://doi.org/10.1007/978-3-030-15719-7_19 |
| Spanish Passage Retrieval dataset | 2019 | project page | https://mklab.iti.gr/results/spanish-passage-retrieval-dataset/ |
| xPQA: Cross-Lingual Product Question Answering across 12 Languages | 2023 | source task paper | https://arxiv.org/abs/2305.09249 |

## Machine-Readable Metadata

<!-- benchmark-task-group-metadata:v1 -->

```yaml
benchmark_task_group_metadata:
  schema_version: 1
  document_status: reviewed_manual
  nano_set: NanoMTEB-Spanish
  backing_dataset: NanoMTEB-Spanish
  dataset_id: hakari-bench/NanoMTEB-Spanish
  language: multilingual
  languages:
    - es
    - en
    - multilingual
  category: natural_language
  document_path: docs/benchmark_tasks/NanoMTEB-Spanish/index.md
  source_research:
    primary_source_type: multiple_task_papers_and_dataset_cards
    paper_pdf_or_html_checked: true
    no_paper_note: null
  counts:
    tasks: 7
    queries: 1334
    split_local_documents: 25262
    positive_qrels: 4806
  positives_per_query:
    average: 3.6026986506746628
    min: 1
    median_task_median: 2.0
    max: 20
    multi_positive_tasks: 6
    multi_positive_queries: 877
  text_stats_chars:
    query_mean_weighted_by_queries: 54.742128935532236
    document_mean_weighted_by_documents: 1049.9211068007285
  bm25:
    ndcg_at_10_query_weighted: 0.33507480443560717
    hit_at_10_query_weighted: 0.5539730135026986
    ndcg_at_10_unweighted_task_mean: 0.34219876977142855
    hit_at_10_unweighted_task_mean: 0.5699187339714286
    source: dataset_bm25_column
    easiest_task_by_ndcg_at_10: miracl_es
    hardest_task_by_ndcg_at_10: xpqa_eng_spa
  tasks:
    - name: mintaka_es
      path: docs/benchmark_tasks/NanoMTEB-Spanish/mintaka_es.md
      retrieval_shape: spanish_complex_question_to_short_answer
      language: multilingual
      queries: 200
      documents: 1693
      positive_qrels: 200
      bm25_ndcg_at_10: 0.2467222553
      bm25_hit_at_10: 0.305
    - name: miracl_es
      path: docs/benchmark_tasks/NanoMTEB-Spanish/miracl_es.md
      retrieval_shape: spanish_query_to_wikipedia_passages
      language: es
      queries: 200
      documents: 10000
      positive_qrels: 934
      bm25_ndcg_at_10: 0.5245549493
      bm25_hit_at_10: 0.93
    - name: spanish_passage_s2_p
      path: docs/benchmark_tasks/NanoMTEB-Spanish/spanish_passage_s2_p.md
      retrieval_shape: spanish_health_question_to_full_web_page
      language: es
      queries: 167
      documents: 7501
      positive_qrels: 996
      bm25_ndcg_at_10: 0.4830697435
      bm25_hit_at_10: 0.8922155689
    - name: spanish_passage_s2_s
      path: docs/benchmark_tasks/NanoMTEB-Spanish/spanish_passage_s2_s.md
      retrieval_shape: spanish_health_question_to_answer_passage
      language: es
      queries: 167
      documents: 250
      positive_qrels: 1228
      bm25_ndcg_at_10: 0.4893086978
      bm25_hit_at_10: 0.8922155689
    - name: xpqa_eng_spa
      path: docs/benchmark_tasks/NanoMTEB-Spanish/xpqa_eng_spa.md
      retrieval_shape: spanish_product_question_to_english_answer_snippet
      language: multilingual
      queries: 200
      documents: 1936
      positive_qrels: 491
      bm25_ndcg_at_10: 0.0946244797
      bm25_hit_at_10: 0.175
    - name: xpqa_spa_eng
      path: docs/benchmark_tasks/NanoMTEB-Spanish/xpqa_spa_eng.md
      retrieval_shape: english_product_question_to_spanish_answer_snippet
      language: multilingual
      queries: 200
      documents: 1941
      positive_qrels: 469
      bm25_ndcg_at_10: 0.1162198676
      bm25_hit_at_10: 0.175
    - name: xpqa_spa_spa
      path: docs/benchmark_tasks/NanoMTEB-Spanish/xpqa_spa_spa.md
      retrieval_shape: spanish_product_question_to_spanish_answer_snippet
      language: es
      queries: 200
      documents: 1941
      positive_qrels: 488
      bm25_ndcg_at_10: 0.4408913952
      bm25_hit_at_10: 0.62
  learning:
    leakage_note: exclude NanoMTEB-Spanish evaluation queries, qrels, positive answer strings, Wikipedia passages, health pages and passages, product snippets, and upstream test rows from training
    useful_training_data:
      - non-overlapping Mintaka and Spanish Wikidata entity-answer QA pairs
      - MIRACL Spanish training data and Spanish Wikipedia passage retrieval pairs
      - Spanish consumer-health QA and medical FAQ retrieval examples
      - Spanish health document and passage retrieval data with multi-positive labels
      - xPQA product QA ranking data in Spanish and English
      - bilingual Spanish-English product question-answer pairs
      - hard negatives from the same entity family, Wikipedia topic, health topic, product category, or product model
    synthetic_data:
      document_generation: Spanish and English answer strings, Wikipedia passages, health pages, health passages, and product answer snippets in source-like style
      question_generation: Spanish complex entity questions, Spanish information needs, Spanish health questions, and Spanish or English product questions grounded in generated documents
      answerability: positives must preserve entity identity, answer-bearing passage evidence, medical answer support, product-property answerability, and cross-lingual alignment rather than broad topic overlap
    multi_positive_training: preserve_miracl_spanish_passage_and_xpqa_multi_positive_qrels
  links:
    nano_dataset: https://huggingface.co/datasets/hakari-bench/NanoMTEB-Spanish
    source_urls:
      - label: MTEB arXiv
        url: https://arxiv.org/abs/2210.07316
      - label: Mintaka arXiv
        url: https://arxiv.org/abs/2210.01613
      - label: MIRACL arXiv
        url: https://arxiv.org/abs/2210.09984
      - label: Spanish Passage Retrieval project page
        url: https://mklab.iti.gr/results/spanish-passage-retrieval-dataset/
      - label: Spanish Passage Retrieval ECIR paper
        url: https://doi.org/10.1007/978-3-030-15719-7_19
      - label: xPQA arXiv
        url: https://arxiv.org/abs/2305.09249
    source_notes: []
  references:
    - title: "MTEB: Massive Text Embedding Benchmark"
      url: https://arxiv.org/abs/2210.07316
      year: 2023
      is_paper: true
      source_confidence: definitive_paper_link
    - title: "Mintaka: A Complex, Natural, and Multilingual Dataset for End-to-End Question Answering"
      url: https://arxiv.org/abs/2210.01613
      year: 2022
      is_paper: true
      source_confidence: definitive_paper_link
    - title: "Making a MIRACL: Multilingual Information Retrieval Across a Continuum of Languages"
      url: https://arxiv.org/abs/2210.09984
      year: 2023
      is_paper: true
      source_confidence: definitive_paper_link
    - title: "A Test Collection for Passage Retrieval Evaluation of Spanish Health-Related Resources"
      url: https://doi.org/10.1007/978-3-030-15719-7_19
      year: 2019
      is_paper: true
      source_confidence: definitive_paper_link
    - title: "xPQA: Cross-Lingual Product Question Answering across 12 Languages"
      url: https://arxiv.org/abs/2305.09249
      year: 2023
      is_paper: true
      source_confidence: definitive_paper_link
```
