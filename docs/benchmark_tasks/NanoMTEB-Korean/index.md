# NanoMTEB-Korean

## Overview

NanoMTEB-Korean is the compact Korean retrieval group for MTEB-style evaluation.
It contains five retrieval tasks: Korean RAG evidence retrieval, Korean
StrategyQA-style implicit-reasoning evidence retrieval, Korean legal article
retrieval, Korean MIRACL Wikipedia retrieval, and Korean SQuAD/KorQuAD-style
context retrieval. The group tests Korean retrieval across public reports,
Wikipedia, statutes, and multi-hop evidence.

Its value is in the contrast between direct evidence retrieval and hidden
reasoning or domain lookup. AutoRAG and SQuADKor often reward finding an
answer-bearing chunk, Ko-StrategyQA may require evidence for an implicit
reasoning step, LawIRKo requires matching formal statute text, and MIRACL keeps
the monolingual Wikipedia passage setting. The group is therefore a compact
check of Korean morphology, legal wording, evidence granularity, and
multi-positive retrieval.

## Details

### What the Original Group Measures

NanoMTEB-Korean collects Korean retrieval-family tasks packaged for MTEB. The
AutoRAG split measures answer-bearing document retrieval for Korean RAG over
publicly accessible finance, public-sector, healthcare, legal, and commerce
documents. Ko-StrategyQA adapts StrategyQA-style implicit reasoning to Korean
evidence retrieval. LawIRKo measures retrieval of Korean legal provisions from
queries naming law titles and article topics. MIRACL Korean measures
same-language Wikipedia passage retrieval, and SQuADKorV1 measures
answer-bearing Korean Wikipedia context retrieval.

The group therefore combines three common retrieval settings: exact evidence
retrieval for QA, hidden-reasoning evidence retrieval, and domain-specific
document lookup. It is small enough to inspect per task, but broad enough that a
single "Korean QA" interpretation would miss the legal and RAG-specific parts.

### Subtask Coverage

The five subtasks cover four retrieval families:

- **Korean RAG retrieval:** `autorag` retrieves public-document chunks needed to
  answer Korean RAG questions.
- **Implicit reasoning evidence retrieval:** `ko_strategy_qa` retrieves one or
  more Korean evidence passages for StrategyQA-style questions.
- **Korean legal retrieval:** `lawir_ko` retrieves statutory article text for a
  law-title and provision query.
- **Korean Wikipedia QA retrieval:** `miracl_ko` and `squad_kor_v1` retrieve
  Korean Wikipedia passages for compact fact questions.

`autorag`, `lawir_ko`, and `squad_kor_v1` are single-positive in the Nano
splits. `ko_strategy_qa` and `miracl_ko` are multi-positive, which matters
because multiple evidence paragraphs may be valid or required for a question.

### Observed Group Profile

Across the five splits, NanoMTEB-Korean contains 914 queries, 1,400 positive
qrels, and 24,493 split-local candidate documents. The document count is a sum
across subtasks, not a deduplicated group-wide corpus size. The group average is
1.53 positives per query, with 226 multi-positive queries.

The observed queries are short: the query-weighted mean is 37.24 characters.
MIRACL and Ko-StrategyQA use especially compact questions, while AutoRAG uses
longer RAG-style questions that often ask for a factual explanation. Documents
are also comparatively short, with a document-weighted mean of 301.33
characters. AutoRAG chunks are the longest on average, while MIRACL passages are
short Korean Wikipedia snippets.

### BM25 Difficulty

The query-weighted BM25 baseline reaches nDCG@10 = 0.5254 and hit@10 = 0.6893.
The easiest split is `squad_kor_v1` with nDCG@10 = 0.8812 and hit@10 = 0.9450,
where direct Korean QA questions and a small Wikipedia context corpus favor
lexical retrieval. `autorag` is also strong at nDCG@10 = 0.8051 because many
queries share domain terms, numbers, and report phrases with the positive
chunk.

The hardest split is `lawir_ko` with nDCG@10 = 0.2783 and hit@10 = 0.3950.
Legal articles have formulaic Korean wording and many cross-references, while
queries often name a law and provision title rather than repeating the article
text. `ko_strategy_qa` and `miracl_ko` sit in the middle: BM25 helps with named
entities, but hidden reasoning, Korean morphology, and multi-positive evidence
sets make exact lexical matching incomplete.

### Training Data That May Help

Useful training data includes non-overlapping Korean RAG question-to-chunk
pairs, Ko-StrategyQA training evidence, Korean Wikipedia QA retrieval pairs,
MIRACL Korean training data, Korean legal article retrieval data, and hard
negatives from the same report, article, law, or Wikipedia page. Training should
exclude NanoMTEB-Korean evaluation queries, qrels, positive documents, and
upstream dev/test examples that overlap the Nano splits.

For `ko_strategy_qa` and `miracl_ko`, multi-positive objectives or listwise
training better match the task than collapsing each query to one positive. For
LawIRKo, domain-specific legal text and adjacent-provision negatives are more
useful than generic Korean paraphrase data.

### Synthetic Data Guidance

Synthetic data should preserve Korean document genre and retrieval intent. RAG
examples should use public-report chunks with quantities, dates, policy terms,
or domain-specific facts. StrategyQA-style examples should include hidden
reasoning links and multiple evidence passages. Legal examples should use
realistic statute articles with numbered clauses and formal Korean legal
phrasing. Wikipedia examples should use answer-bearing Korean passages with
entity, date, location, and definition questions.

Hard negatives should be near misses from the same source family: adjacent law
articles, same-report chunks, related Wikipedia pages, or evidence passages for
a different reasoning step. Nano evaluation queries and positive passages should
not be used as seeds.

## Task Summary

| Task | Retrieval shape | Queries | Docs | Positive qrels | BM25 nDCG@10 | BM25 hit@10 | Query avg chars | Doc avg chars | Source status |
| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | --- |
| [autorag](autorag.md) | Korean RAG question to public-document chunk | 114 | 720 | 114 | 0.8051 | 0.9211 | 69.61 | 823.60 | AutoRAG paper + dataset card |
| [ko_strategy_qa](ko_strategy_qa.md) | Korean implicit question to evidence passages | 200 | 9,251 | 378 | 0.3694 | 0.5800 | 22.43 | 320.25 | StrategyQA + dataset card |
| [lawir_ko](lawir_ko.md) | Korean law/provision query to statute article | 200 | 3,562 | 200 | 0.2783 | 0.3950 | 50.62 | 387.21 | dataset card + MTEB |
| [miracl_ko](miracl_ko.md) | Korean question to Wikipedia passage | 200 | 10,000 | 508 | 0.4132 | 0.7050 | 21.70 | 192.21 | MIRACL + MTEB |
| [squad_kor_v1](squad_kor_v1.md) | Korean QA question to answer context | 200 | 960 | 200 | 0.8812 | 0.9450 | 35.77 | 545.20 | KorQuAD/SQuADKor source |

## Dataset Information

| Field | Value |
| --- | --- |
| Nano set | NanoMTEB-Korean |
| Backing dataset | NanoMTEB-Korean |
| Hugging Face dataset | [hakari-bench/NanoMTEB-Korean](https://huggingface.co/datasets/hakari-bench/NanoMTEB-Korean) |
| Language | ko |
| Category | natural_language |
| Subtasks | 5 |
| Total queries | 914 |
| Split-local documents | 24,493 |
| Positive qrels | 1,400 |
| Positives per query | 1.53 average |
| Multi-positive queries | 226 |
| Query-weighted BM25 nDCG@10 | 0.5254 |
| Query-weighted BM25 hit@10 | 0.6893 |
| Mean query length | 37.24 chars, weighted by query count |
| Mean document length | 301.33 chars, weighted by split-local document count |

### Public Sources

- [AutoRAG: Automated Framework for optimization of Retrieval Augmented Generation Pipeline](https://arxiv.org/abs/2410.20878); 2024.
- [Did Aristotle Use a Laptop? A Question Answering Benchmark with Implicit Reasoning Strategies](https://arxiv.org/abs/2101.02235); 2021.
- [LawIRKo source dataset](https://huggingface.co/datasets/on-and-on/lawgov_ir-ko).
- [MIRACL](http://miracl.ai/).
- [KorQuAD1.0: Korean QA Dataset for Machine Reading Comprehension](https://arxiv.org/abs/1909.07005); 2019.
- [Massive Text Embedding Benchmark (MTEB)](https://github.com/embeddings-benchmark/mteb).

### Hugging Face Links

- Nano dataset: [hakari-bench/NanoMTEB-Korean](https://huggingface.co/datasets/hakari-bench/NanoMTEB-Korean)
- Source datasets:
  [yjoonjang/markers_bm](https://huggingface.co/datasets/yjoonjang/markers_bm),
  [taeminlee/Ko-StrategyQA](https://huggingface.co/datasets/taeminlee/Ko-StrategyQA),
  [on-and-on/lawgov_ir-ko](https://huggingface.co/datasets/on-and-on/lawgov_ir-ko),
  [mteb/MIRACLRetrieval](https://huggingface.co/datasets/mteb/MIRACLRetrieval),
  [yjoonjang/squad_kor_v1](https://huggingface.co/datasets/yjoonjang/squad_kor_v1).

### Source Reference Table

| Title | Year | Type | URL |
| --- | ---: | --- | --- |
| AutoRAG: Automated Framework for optimization of Retrieval Augmented Generation Pipeline | 2024 | source task paper | https://arxiv.org/abs/2410.20878 |
| Did Aristotle Use a Laptop? A Question Answering Benchmark with Implicit Reasoning Strategies | 2021 | source task paper | https://arxiv.org/abs/2101.02235 |
| LawIRKo source reference | 2024 | dataset card | https://huggingface.co/datasets/on-and-on/lawgov_ir-ko |
| MIRACL | 2022 | benchmark page | http://miracl.ai/ |
| KorQuAD1.0: Korean QA Dataset for Machine Reading Comprehension | 2019 | source task paper | https://arxiv.org/abs/1909.07005 |
| Massive Text Embedding Benchmark (MTEB) | 2022 | benchmark repository | https://github.com/embeddings-benchmark/mteb |

## Machine-Readable Metadata

<!-- benchmark-task-group-metadata:v1 -->

```yaml
benchmark_task_group_metadata:
  schema_version: 1
  document_status: reviewed_manual
  nano_set: NanoMTEB-Korean
  backing_dataset: NanoMTEB-Korean
  dataset_id: hakari-bench/NanoMTEB-Korean
  language: ko
  category: natural_language
  document_path: docs/benchmark_tasks/NanoMTEB-Korean/index.md
  source_research:
    primary_source_type: multiple_dataset_cards_and_source_references
    paper_pdf_or_html_checked: true
    no_paper_note: null
  counts:
    tasks: 5
    queries: 914
    split_local_documents: 24493
    positive_qrels: 1400
  positives_per_query:
    average: 1.5317286652078774
    min: 1
    median_task_median: 1.0
    max: 12
    multi_positive_tasks: 2
    multi_positive_queries: 226
  text_stats_chars:
    query_mean_weighted_by_queries: 37.24398249452714
    document_mean_weighted_by_documents: 301.3260523414709
  bm25:
    ndcg_at_10_query_weighted: 0.5253808935582057
    hit_at_10_query_weighted: 0.6892778993461706
    ndcg_at_10_unweighted_task_mean: 0.54943955986
    hit_at_10_unweighted_task_mean: 0.70921052632
    source: dataset_bm25_column
    easiest_task_by_ndcg_at_10: squad_kor_v1
    hardest_task_by_ndcg_at_10: lawir_ko
  tasks:
    - name: autorag
      path: docs/benchmark_tasks/NanoMTEB-Korean/autorag.md
      retrieval_shape: korean_rag_question_to_public_document_chunk
      queries: 114
      documents: 720
      positive_qrels: 114
      bm25_ndcg_at_10: 0.8051328273
      bm25_hit_at_10: 0.9210526316
    - name: ko_strategy_qa
      path: docs/benchmark_tasks/NanoMTEB-Korean/ko_strategy_qa.md
      retrieval_shape: korean_implicit_question_to_evidence_passages
      queries: 200
      documents: 9251
      positive_qrels: 378
      bm25_ndcg_at_10: 0.3693571076
      bm25_hit_at_10: 0.58
    - name: lawir_ko
      path: docs/benchmark_tasks/NanoMTEB-Korean/lawir_ko.md
      retrieval_shape: korean_law_provision_query_to_statute_article
      queries: 200
      documents: 3562
      positive_qrels: 200
      bm25_ndcg_at_10: 0.2782674716
      bm25_hit_at_10: 0.395
    - name: miracl_ko
      path: docs/benchmark_tasks/NanoMTEB-Korean/miracl_ko.md
      retrieval_shape: korean_question_to_wikipedia_passage
      queries: 200
      documents: 10000
      positive_qrels: 508
      bm25_ndcg_at_10: 0.4132083896
      bm25_hit_at_10: 0.705
    - name: squad_kor_v1
      path: docs/benchmark_tasks/NanoMTEB-Korean/squad_kor_v1.md
      retrieval_shape: korean_qa_question_to_answer_context
      queries: 200
      documents: 960
      positive_qrels: 200
      bm25_ndcg_at_10: 0.8812320032
      bm25_hit_at_10: 0.945
  learning:
    leakage_note: exclude NanoMTEB-Korean evaluation queries, qrels, positive passages, and upstream dev/test rows that overlap the Nano splits
    useful_training_data:
      - Korean RAG question-to-chunk pairs from public reports
      - Ko-StrategyQA and Korean multi-hop evidence retrieval pairs
      - Korean Wikipedia QA retrieval and MIRACL Korean training data
      - Korean legal article retrieval and law-title-to-provision mappings
      - hard negatives from the same report, law, Wikipedia page, or reasoning chain
    synthetic_data:
      document_generation: Korean public-report chunks, evidence passages, statute articles, and Wikipedia passages in source-like style
      question_generation: Korean RAG questions, implicit reasoning questions, law-provision queries, and answerable Wikipedia questions grounded in the generated or selected document
      answerability: positives must contain the answer evidence, legal article, or reasoning support rather than only sharing Korean keywords
    multi_positive_training: preserve_strategyqa_and_miracl_multi_positive_evidence
  links:
    nano_dataset: https://huggingface.co/datasets/hakari-bench/NanoMTEB-Korean
    source_urls:
      - label: AutoRAG arXiv
        url: https://arxiv.org/abs/2410.20878
      - label: yjoonjang/markers_bm
        url: https://huggingface.co/datasets/yjoonjang/markers_bm
      - label: StrategyQA arXiv
        url: https://arxiv.org/abs/2101.02235
      - label: taeminlee/Ko-StrategyQA
        url: https://huggingface.co/datasets/taeminlee/Ko-StrategyQA
      - label: on-and-on/lawgov_ir-ko
        url: https://huggingface.co/datasets/on-and-on/lawgov_ir-ko
      - label: MIRACL
        url: http://miracl.ai/
      - label: mteb/MIRACLRetrieval
        url: https://huggingface.co/datasets/mteb/MIRACLRetrieval
      - label: KorQuAD1.0 arXiv
        url: https://arxiv.org/abs/1909.07005
      - label: yjoonjang/squad_kor_v1
        url: https://huggingface.co/datasets/yjoonjang/squad_kor_v1
    source_notes: []
  references:
    - title: "AutoRAG: Automated Framework for optimization of Retrieval Augmented Generation Pipeline"
      url: https://arxiv.org/abs/2410.20878
      year: 2024
      is_paper: true
      source_confidence: definitive_paper_link
    - title: Did Aristotle Use a Laptop? A Question Answering Benchmark with Implicit Reasoning Strategies
      url: https://arxiv.org/abs/2101.02235
      year: 2021
      is_paper: true
      source_confidence: definitive_paper_link
    - title: LawIRKo source reference
      url: https://huggingface.co/datasets/on-and-on/lawgov_ir-ko
      year: 2024
      is_paper: false
      source_confidence: dataset_source_reference
    - title: MIRACL
      url: http://miracl.ai/
      year: 2022
      is_paper: false
      source_confidence: benchmark_page
    - title: "KorQuAD1.0: Korean QA Dataset for Machine Reading Comprehension"
      url: https://arxiv.org/abs/1909.07005
      year: 2019
      is_paper: true
      source_confidence: definitive_paper_link
```
