# NanoMTEB-French

## Overview

NanoMTEB-French is a compact French retrieval group drawn from MTEB-French and
related MTEB retrieval tasks. It combines educational resource retrieval,
Belgian statutory article retrieval, French Wikipedia QA passage retrieval,
French Mintaka answer retrieval, Syntec collective-agreement retrieval, and
French-English product question answering. The group tests both monolingual
French retrieval and cross-lingual product QA, with task formats ranging from
long educational lessons to very short answer strings.

## Details

### What the Original Group Measures

The collection follows MTEB-French for the French retrieval-family tasks and
keeps xPQA directions that use French. Alloprof measures retrieval from French
student questions to teacher-curated educational resources. BSARD measures lay
legal question retrieval over Belgian statutory articles. FQuAD is a French
reading-comprehension dataset converted into passage retrieval. Mintaka is
complex multilingual QA converted into short-answer retrieval. Syntec measures
retrieval over a French collective bargaining agreement. The xPQA splits
measure product answer candidate retrieval in French-English and French-French
directions.

This mixture is important because the group is not a single French passage
benchmark. Some tasks reward exact named-entity and answer-span matching, while
others require mapping noisy student questions, citizen legal language, or
product questions to long explanatory or formal documents.

### Subtask Coverage

The eight subtasks cover six retrieval families:

- **Educational help retrieval:** `alloprof` retrieves long French educational
  explanations for Quebec student questions.
- **Legal and workplace retrieval:** `bsard` retrieves Belgian law articles for
  lay legal questions, while `syntec` retrieves articles from the Syntec
  collective agreement.
- **French QA passage retrieval:** `fquad` retrieves French Wikipedia passages
  that contain answer evidence.
- **Complex entity-answer retrieval:** `mintaka_fr` maps French complex
  questions to short answer strings or entity names.
- **Cross-lingual product QA retrieval:** `xpqa_eng_fra` and `xpqa_fra_eng`
  bridge French queries to English snippets or English queries to French
  snippets.
- **Monolingual product QA retrieval:** `xpqa_fra_fra` retrieves French product
  answer snippets for French product questions.

Most tasks are French-only, but the group is multilingual because Mintaka and
xPQA contain English answer strings or cross-lingual query/document directions.
The xPQA splits also contain many numeric values, product codes, and short
yes/no snippets where polarity and compatibility matter.

### Observed Group Profile

Across the eight splits, NanoMTEB-French contains 1,500 queries, 2,212
positive qrels, and 19,397 split-local candidate documents. The document count
is a sum across subtasks, not a deduplicated group-wide corpus size. The group
average is 1.47 positives per query, with 314 multi-positive queries. The only
multi-positive tasks are the three xPQA splits, each with up to five positives
per query.

Text length varies widely. Alloprof has the longest queries and documents:
student questions average 179.23 characters and lesson documents average
3,504.53 characters. BSARD queries are also long because they often include
legal category labels, while statute documents average 793.01 characters.
Mintaka and xPQA have short answer documents, with Mintaka answer strings
averaging only 14.41 characters. The query-weighted mean query length is 86.63
characters, and the document-weighted mean document length is 914.18
characters.

### BM25 Difficulty

The query-weighted BM25 baseline reaches nDCG@10 = 0.3961 and hit@10 =
0.5073. The easiest task by nDCG@10 is `fquad` at 0.8990, where questions and
Wikipedia passages often share distinctive named entities or answer-bearing
phrasing. `syntec` is also favorable for BM25 at 0.6906 because many questions
reuse terms from collective-agreement article titles or clauses.

The hardest split is `xpqa_eng_fra` at nDCG@10 = 0.1030, where French product
questions retrieve English product snippets. BSARD is also difficult at 0.1708
because citizen legal questions and statutory article language diverge
substantially. The reverse cross-lingual xPQA direction, `xpqa_fra_eng`, is
still hard but slightly easier in this Nano sample, likely because product
names, units, and technical tokens sometimes survive across languages.

### Training Data That May Help

Useful training data should be matched to each family. For Alloprof, use
non-overlapping French educational forum questions and lesson-resource pairs.
For BSARD and Syntec, use French legal, labor-law, and collective-agreement
question-to-article pairs with hard negatives from adjacent articles. For
FQuAD, use non-overlapping French Wikipedia QA and same-article negatives. For
Mintaka, use French Wikidata QA, entity-linking, and complex-question
paraphrases. For xPQA, use in-domain product QA ranking data in French and
English, preserving multiple positive answer snippets.

Training should exclude Nano evaluation queries, qrels, positive documents,
answer strings, statutes, lesson resources, agreement articles, and product
snippets. Cross-lingual product QA should be trained as answerability ranking,
not only translation or topical similarity.

### Synthetic Data Guidance

Synthetic data should preserve the retrieval relation. Generate French student
questions with realistic school-domain wording and lesson documents; lay legal
questions paired with statutory or workplace clauses; French Wikipedia
paragraphs with extractive questions; French complex questions with short
canonical answer strings; and French-English product questions paired with
answer snippets containing explicit specifications, compatibility, dimensions,
materials, warranty, or customer-reported evidence.

Synthetic examples should not use NanoMTEB-French evaluation questions,
positive documents, source article text, or xPQA product candidates as seeds.

## Task Summary

| Task | Retrieval shape | Lang | Queries | Docs | Positive qrels | BM25 nDCG@10 | BM25 hit@10 | Query avg chars | Doc avg chars | Source status |
| --- | --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | --- |
| [alloprof](alloprof.md) | French student question to educational resource | fr | 200 | 2,556 | 200 | 0.3390 | 0.4750 | 179.23 | 3,504.53 | MTEB-French / Alloprof |
| [bsard](bsard.md) | French lay legal question to Belgian statute | fr | 200 | 10,000 | 200 | 0.1708 | 0.2850 | 144.97 | 793.01 | BSARD paper |
| [fquad](fquad.md) | French QA question to Wikipedia passage | fr | 200 | 269 | 200 | 0.8990 | 0.9550 | 56.21 | 898.31 | FQuAD paper |
| [mintaka_fr](mintaka_fr.md) | French complex question to short answer | multilingual | 200 | 1,714 | 200 | 0.3000 | 0.4000 | 71.61 | 14.41 | Mintaka paper |
| [syntec](syntec.md) | French employment question to agreement article | fr | 100 | 90 | 100 | 0.6906 | 0.8700 | 72.80 | 1,226.27 | MTEB-French |
| [xpqa_eng_fra](xpqa_eng_fra.md) | French product question to English answer snippet | multilingual | 200 | 1,674 | 451 | 0.1030 | 0.1750 | 54.61 | 137.30 | xPQA paper |
| [xpqa_fra_eng](xpqa_fra_eng.md) | English product question to French answer snippet | multilingual | 200 | 1,547 | 437 | 0.2585 | 0.3450 | 52.11 | 76.98 | xPQA paper |
| [xpqa_fra_fra](xpqa_fra_fra.md) | French product question to French answer snippet | fr | 200 | 1,547 | 424 | 0.5551 | 0.7350 | 54.61 | 76.98 | xPQA paper |

## Dataset Information

| Field | Value |
| --- | --- |
| Nano set | NanoMTEB-French |
| Backing dataset | NanoMTEB-French |
| Hugging Face dataset | [hakari-bench/NanoMTEB-French](https://huggingface.co/datasets/hakari-bench/NanoMTEB-French) |
| Languages | fr, en, multilingual |
| Category | natural_language |
| Subtasks | 8 |
| Total queries | 1,500 |
| Split-local documents | 19,397 |
| Positive qrels | 2,212 |
| Positives per query | 1.47 average |
| Multi-positive queries | 314 |
| Query-weighted BM25 nDCG@10 | 0.3961 |
| Query-weighted BM25 hit@10 | 0.5073 |
| Mean query length | 86.63 chars, weighted by query count |
| Mean document length | 914.18 chars, weighted by split-local document count |

### Public Sources

- [MTEB-French: Resources for French Sentence Embedding Evaluation and Analysis](https://arxiv.org/abs/2405.20468); 2024; French benchmark source.
- [MTEB: Massive Text Embedding Benchmark](https://arxiv.org/abs/2210.07316); 2023; MTEB packaging context.
- [A Statutory Article Retrieval Dataset in French](https://arxiv.org/abs/2108.11792); 2022; BSARD source.
- [FQuAD: French Question Answering Dataset](https://arxiv.org/abs/2002.06071); 2020; French extractive QA source.
- [FQuAD2.0](https://arxiv.org/abs/2109.13209); source dataset context for `manu/fquad2_test`.
- [Mintaka](https://arxiv.org/abs/2210.01613); 2022; complex multilingual QA source.
- [xPQA](https://arxiv.org/abs/2305.09249); 2023; cross-lingual product QA source.

### Hugging Face Links

- Nano dataset: [hakari-bench/NanoMTEB-French](https://huggingface.co/datasets/hakari-bench/NanoMTEB-French)
- Source examples:
  [mteb/AlloprofRetrieval](https://huggingface.co/datasets/mteb/AlloprofRetrieval),
  [mteb/BSARDRetrieval](https://huggingface.co/datasets/mteb/BSARDRetrieval),
  [manu/fquad2_test](https://huggingface.co/datasets/manu/fquad2_test),
  [mteb/MintakaRetrieval](https://huggingface.co/datasets/mteb/MintakaRetrieval),
  [lyon-nlp/mteb-fr-retrieval-syntec-s2p](https://huggingface.co/datasets/lyon-nlp/mteb-fr-retrieval-syntec-s2p),
  [mteb/XPQARetrieval](https://huggingface.co/datasets/mteb/XPQARetrieval).

### Source Reference Table

| Title | Year | Type | URL |
| --- | ---: | --- | --- |
| MTEB-French: Resources for French Sentence Embedding Evaluation and Analysis | 2024 | benchmark paper | https://arxiv.org/abs/2405.20468 |
| MTEB: Massive Text Embedding Benchmark | 2023 | benchmark paper | https://arxiv.org/abs/2210.07316 |
| A Statutory Article Retrieval Dataset in French | 2022 | source task paper | https://arxiv.org/abs/2108.11792 |
| FQuAD: French Question Answering Dataset | 2020 | source task paper | https://arxiv.org/abs/2002.06071 |
| FQuAD2.0: French Question Answering and knowing that you know nothing | 2021 | source task paper | https://arxiv.org/abs/2109.13209 |
| Mintaka: A Complex, Natural, and Multilingual Dataset for End-to-End Question Answering | 2022 | source task paper | https://arxiv.org/abs/2210.01613 |
| xPQA: Cross-Lingual Product Question Answering across 12 Languages | 2023 | source task paper | https://arxiv.org/abs/2305.09249 |

## Machine-Readable Metadata

<!-- benchmark-task-group-metadata:v1 -->

```yaml
benchmark_task_group_metadata:
  schema_version: 1
  document_status: reviewed_manual
  nano_set: NanoMTEB-French
  backing_dataset: NanoMTEB-French
  dataset_id: hakari-bench/NanoMTEB-French
  language: multilingual
  languages:
    - fr
    - en
    - multilingual
  category: natural_language
  document_path: docs/benchmark_tasks/NanoMTEB-French/index.md
  source_research:
    primary_source_type: multiple_task_papers_and_dataset_cards
    paper_pdf_or_html_checked: true
    no_paper_note: null
  counts:
    tasks: 8
    queries: 1500
    split_local_documents: 19397
    positive_qrels: 2212
  positives_per_query:
    average: 1.4746666666666666
    min: 1
    median_task_median: 1.0
    max: 5
    multi_positive_tasks: 3
    multi_positive_queries: 314
  text_stats_chars:
    query_mean_weighted_by_queries: 86.63266666666667
    document_mean_weighted_by_documents: 914.1844615146672
  bm25:
    ndcg_at_10_query_weighted: 0.39608970838666663
    hit_at_10_query_weighted: 0.5073333333333333
    ndcg_at_10_unweighted_task_mean: 0.41449726666250003
    hit_at_10_unweighted_task_mean: 0.53
    source: dataset_bm25_column
    easiest_task_by_ndcg_at_10: fquad
    hardest_task_by_ndcg_at_10: xpqa_eng_fra
  tasks:
    - name: alloprof
      path: docs/benchmark_tasks/NanoMTEB-French/alloprof.md
      retrieval_shape: french_student_question_to_educational_resource
      language: fr
      queries: 200
      documents: 2556
      positive_qrels: 200
      bm25_ndcg_at_10: 0.3389716145
      bm25_hit_at_10: 0.475
    - name: bsard
      path: docs/benchmark_tasks/NanoMTEB-French/bsard.md
      retrieval_shape: french_lay_legal_question_to_belgian_statute
      language: fr
      queries: 200
      documents: 10000
      positive_qrels: 200
      bm25_ndcg_at_10: 0.1707572164
      bm25_hit_at_10: 0.285
    - name: fquad
      path: docs/benchmark_tasks/NanoMTEB-French/fquad.md
      retrieval_shape: french_qa_question_to_wikipedia_passage
      language: fr
      queries: 200
      documents: 269
      positive_qrels: 200
      bm25_ndcg_at_10: 0.8989719806
      bm25_hit_at_10: 0.955
    - name: mintaka_fr
      path: docs/benchmark_tasks/NanoMTEB-French/mintaka_fr.md
      retrieval_shape: french_complex_question_to_short_answer
      language: multilingual
      queries: 200
      documents: 1714
      positive_qrels: 200
      bm25_ndcg_at_10: 0.2999749748
      bm25_hit_at_10: 0.4
    - name: syntec
      path: docs/benchmark_tasks/NanoMTEB-French/syntec.md
      retrieval_shape: french_employment_question_to_agreement_article
      language: fr
      queries: 100
      documents: 90
      positive_qrels: 100
      bm25_ndcg_at_10: 0.6906106408
      bm25_hit_at_10: 0.87
    - name: xpqa_eng_fra
      path: docs/benchmark_tasks/NanoMTEB-French/xpqa_eng_fra.md
      retrieval_shape: french_product_question_to_english_answer_snippet
      language: multilingual
      queries: 200
      documents: 1674
      positive_qrels: 451
      bm25_ndcg_at_10: 0.1030484088
      bm25_hit_at_10: 0.175
    - name: xpqa_fra_eng
      path: docs/benchmark_tasks/NanoMTEB-French/xpqa_fra_eng.md
      retrieval_shape: english_product_question_to_french_answer_snippet
      language: multilingual
      queries: 200
      documents: 1547
      positive_qrels: 437
      bm25_ndcg_at_10: 0.2584987816
      bm25_hit_at_10: 0.345
    - name: xpqa_fra_fra
      path: docs/benchmark_tasks/NanoMTEB-French/xpqa_fra_fra.md
      retrieval_shape: french_product_question_to_french_answer_snippet
      language: fr
      queries: 200
      documents: 1547
      positive_qrels: 424
      bm25_ndcg_at_10: 0.5551445158
      bm25_hit_at_10: 0.735
  learning:
    leakage_note: exclude NanoMTEB-French evaluation queries, qrels, positive documents, answer strings, statutes, lesson resources, Syntec articles, xPQA product snippets, and upstream test rows from training
    useful_training_data:
      - non-overlapping French educational forum question-resource pairs
      - French legal, labor-law, and collective-agreement question-to-article pairs
      - non-overlapping FQuAD and French Wikipedia QA retrieval pairs
      - French Mintaka and Wikidata entity-answer QA pairs
      - French-English xPQA and e-commerce product QA ranking data
      - hard negatives from the same school subject, legal code, agreement article family, Wikipedia article, entity class, product model, or product category
    synthetic_data:
      document_generation: French lessons, statutes, agreement articles, Wikipedia passages, short answer strings, and product answer snippets in source-like style
      question_generation: French student questions, lay legal questions, workplace questions, extractive QA questions, complex entity questions, and French or English product questions grounded in generated documents
      answerability: positives must preserve lesson explanation, statutory or agreement support, answer-bearing evidence, entity identity, product-property answerability, and cross-lingual alignment rather than broad topic overlap
    multi_positive_training: preserve_xpqa_multi_positive_qrels
  links:
    nano_dataset: https://huggingface.co/datasets/hakari-bench/NanoMTEB-French
    source_urls:
      - label: MTEB-French arXiv
        url: https://arxiv.org/abs/2405.20468
      - label: MTEB arXiv
        url: https://arxiv.org/abs/2210.07316
      - label: BSARD arXiv
        url: https://arxiv.org/abs/2108.11792
      - label: FQuAD arXiv
        url: https://arxiv.org/abs/2002.06071
      - label: FQuAD2 arXiv
        url: https://arxiv.org/abs/2109.13209
      - label: Mintaka arXiv
        url: https://arxiv.org/abs/2210.01613
      - label: xPQA arXiv
        url: https://arxiv.org/abs/2305.09249
    source_notes: []
  references:
    - title: "MTEB-French: Resources for French Sentence Embedding Evaluation and Analysis"
      url: https://arxiv.org/abs/2405.20468
      year: 2024
      is_paper: true
      source_confidence: definitive_paper_link
    - title: "MTEB: Massive Text Embedding Benchmark"
      url: https://arxiv.org/abs/2210.07316
      year: 2023
      is_paper: true
      source_confidence: definitive_paper_link
    - title: "A Statutory Article Retrieval Dataset in French"
      url: https://arxiv.org/abs/2108.11792
      year: 2022
      is_paper: true
      source_confidence: definitive_paper_link
    - title: "FQuAD: French Question Answering Dataset"
      url: https://arxiv.org/abs/2002.06071
      year: 2020
      is_paper: true
      source_confidence: definitive_paper_link
    - title: "FQuAD2.0: French Question Answering and knowing that you know nothing"
      url: https://arxiv.org/abs/2109.13209
      year: 2021
      is_paper: true
      source_confidence: definitive_paper_link
    - title: "Mintaka: A Complex, Natural, and Multilingual Dataset for End-to-End Question Answering"
      url: https://arxiv.org/abs/2210.01613
      year: 2022
      is_paper: true
      source_confidence: definitive_paper_link
    - title: "xPQA: Cross-Lingual Product Question Answering across 12 Languages"
      url: https://arxiv.org/abs/2305.09249
      year: 2023
      is_paper: true
      source_confidence: definitive_paper_link
```
