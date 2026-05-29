# NanoChemTEB

## Overview

NanoChemTEB is the compact chemistry-domain retrieval group. It combines two
ChemTEB question-answering retrieval tasks, `NanoChemHotpotQA` and
`NanoChemNQ`, with `NanoChemRxiv`, a chemical-literature retrieval task over
ChemRxiv-style preprint paragraphs. The shared theme is not simply English
retrieval, but retrieval under chemistry, materials, and chemical-science
terminology.

The group is small but useful for checking whether a retriever handles
scientific entities, chemical names, compounds, methods, and domain-specific
evidence. It also contrasts Wikipedia-derived QA retrieval with literature
paragraph retrieval, which have different document lengths and lexical signals.

## Details

### What the Original Group Measures

[ChemTEB: Chemical Text Embedding Benchmark](https://proceedings.mlr.press/v262/shiraee-kasmaee24a.html)
evaluates text embedding models on chemical-domain tasks, including
chemistry-focused retrieval. [ChEmbed: Enhancing Chemical Literature Search Through Domain-Specific Text Embeddings](https://arxiv.org/abs/2508.01643)
extends that domain-specific focus to chemical literature search. NanoChemTEB
packages three compact retrieval splits from this setting.

The two QA-derived tasks reuse familiar retrieval shapes from HotpotQA and
Natural Questions but filter the content toward chemistry. The ChemRxiv task is
closer to literature search: queries target paragraphs from chemical preprints,
so the model must match a scientific question to a passage that may contain
specialized terminology, reactions, materials, or methods.

### Subtask Coverage

- **NanoChemHotpotQA:** chemistry-filtered multi-hop QA retrieval over
  Wikipedia-derived passages.
- **NanoChemNQ:** chemistry-filtered Natural Questions retrieval, with shorter
  search-style questions and Wikipedia evidence.
- **NanoChemRxiv:** chemistry literature retrieval over ChemRxiv preprint
  paragraphs.

All three tasks are English natural-language retrieval tasks. Most queries have
one positive; `NanoChemNQ` contains a small number of multi-positive queries.

### Observed Group Profile

The current task pages report 245 queries, 253 positive qrels, and 30,000
split-local candidate documents. `NanoChemRxiv` dominates the group by query
count with 200 queries, while `NanoChemHotpotQA` and `NanoChemNQ` have 18 and
27 queries respectively. Query length averages 104.80 characters when weighted
by query count.

Documents average 654.24 characters when weighted by split-local document count.
The ChemRxiv documents are substantially longer on average than the
Wikipedia-derived ChemHotpotQA and ChemNQ passages, which changes the retrieval
problem from short evidence matching toward scientific paragraph matching.

### BM25 Difficulty

Using the dataset-provided BM25 candidate columns, NanoChemTEB has
query-weighted BM25 nDCG@10 = 0.7992 and hit@10 = 0.8735. This high group score
is driven mostly by `NanoChemRxiv`, where BM25 reaches nDCG@10 = 0.8718 and
hit@10 = 0.9400. Domain terms and chemical phrases often provide strong lexical
anchors in the literature retrieval setting.

`NanoChemNQ` is the hardest subtask for BM25 (nDCG@10 = 0.3616,
hit@10 = 0.4815). Its real search-style questions are shorter and can phrase
the information need differently from the evidence passage. `NanoChemHotpotQA`
is in the middle: multi-hop questions contain more lexical clues than ChemNQ,
but still require connecting question wording to supporting passages.

### Training Data That May Help

Useful training data includes non-overlapping ChemTEB retrieval pairs,
chemistry-focused question-answer evidence pairs, scientific abstract and
paragraph retrieval data, ChemRxiv or PubMed-style literature search pairs, and
hard negatives that share compounds, methods, or materials but answer a
different question. General QA retrieval can help, but domain vocabulary and
scientific passage style matter.

Training should exclude NanoChemTEB evaluation queries, qrels, and positive
documents. If ChemRxiv, ChemTEB, HotpotQA, or Natural Questions source data are
used, the exact chemistry-filtered evaluation examples should be audited for
overlap.

### Synthetic Data Guidance

Synthetic documents should resemble chemistry passages: include compounds,
reactions, catalysts, materials, measurements, experimental conditions, and
domain-specific entities. For QA-style tasks, generate questions that are
answerable from a selected non-evaluation passage. For ChemRxiv-style training,
generate scientific literature queries whose positives contain explicit
paragraph-level evidence.

Synthetic negatives should share surface chemical terminology but differ in the
method, compound, result, or relation being asked about. Do not use NanoChemTEB
evaluation queries or positive paragraphs as generation seeds.

## Task Summary

| Task | Retrieval focus | Queries | Docs | Positive qrels | BM25 nDCG@10 | BM25 hit@10 | Query avg chars | Doc avg chars |
| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| [NanoChemHotpotQA](NanoChemHotpotQA.md) | chemistry multi-hop QA to evidence passage | 18 | 10,000 | 18 | 0.6496 | 0.7222 | 104.22 | 402.40 |
| [NanoChemNQ](NanoChemNQ.md) | chemistry Natural Questions to evidence passage | 27 | 10,000 | 35 | 0.3616 | 0.4815 | 54.00 | 481.20 |
| [NanoChemRxiv](NanoChemRxiv.md) | chemistry question to ChemRxiv paragraph | 200 | 10,000 | 200 | 0.8718 | 0.9400 | 111.68 | 1,079.12 |

## Dataset Information

| Field | Value |
| --- | --- |
| Nano set | NanoChemTEB |
| Backing dataset | NanoChemTEB |
| Hugging Face dataset | [hakari-bench/NanoChemTEB](https://huggingface.co/datasets/hakari-bench/NanoChemTEB) |
| Language | en |
| Category | natural language |
| Subtasks | 3 |
| Total queries | 245 |
| Split-local documents | 30,000 |
| Positive qrels | 253 |
| Average positives / query | 1.03 |
| Queries with multiple positives | 7 |
| Query-weighted BM25 nDCG@10 | 0.8700 |
| Query-weighted BM25 hit@10 | 0.9388 |
| Query-weighted BM25 Recall@100 | 0.9752 |
| Query-weighted Dense nDCG@10 | 0.8597 |
| Query-weighted Dense hit@10 | 0.9224 |
| Query-weighted Dense Recall@100 | 0.9846 |
| Query-weighted Reranking hybrid nDCG@10 | 0.8880 |
| Query-weighted Reranking hybrid hit@10 | 0.9429 |
| Query-weighted Reranking hybrid Recall@100 | 0.9969 |
| Mean query length | 104.80 chars, weighted by query count |
| Mean document length | 654.24 chars, weighted by split-local document count |

### Public Sources

- [ChemTEB: Chemical Text Embedding Benchmark](https://proceedings.mlr.press/v262/shiraee-kasmaee24a.html); 2024.
- [ChEmbed: Enhancing Chemical Literature Search Through Domain-Specific Text Embeddings](https://arxiv.org/abs/2508.01643); 2025; DOI: `10.48550/arXiv.2508.01643`.
- [HotpotQA: A Dataset for Diverse, Explainable Multi-hop Question Answering](https://aclanthology.org/D18-1259/); 2018; DOI: `10.18653/v1/D18-1259`.
- [Natural Questions: A Benchmark for Question Answering Research](https://aclanthology.org/Q19-1026/); 2019; DOI: `10.1162/tacl_a_00276`.

### Hugging Face Links

- Nano dataset: [hakari-bench/NanoChemTEB](https://huggingface.co/datasets/hakari-bench/NanoChemTEB)

### Source Reference Table

| Title | Year | Type | URL |
| --- | ---: | --- | --- |
| ChemTEB: Chemical Text Embedding Benchmark, an Overview of Embedding Models Performance & Efficiency on a Specific Domain | 2024 | benchmark paper | https://proceedings.mlr.press/v262/shiraee-kasmaee24a.html |
| ChEmbed: Enhancing Chemical Literature Search Through Domain-Specific Text Embeddings | 2025 | benchmark paper | https://arxiv.org/abs/2508.01643 |
| HotpotQA: A Dataset for Diverse, Explainable Multi-hop Question Answering | 2018 | source task paper | https://aclanthology.org/D18-1259/ |
| Natural Questions: A Benchmark for Question Answering Research | 2019 | source task paper | https://aclanthology.org/Q19-1026/ |

## Machine-Readable Metadata

<!-- benchmark-task-group-metadata:v1 -->

```yaml
benchmark_task_group_metadata:
  schema_version: 1
  document_status: reviewed_manual
  nano_set: NanoChemTEB
  backing_dataset: NanoChemTEB
  dataset_id: hakari-bench/NanoChemTEB
  language: en
  category: natural_language
  document_path: docs/benchmark_tasks/NanoChemTEB/index.md
  source_research:
    primary_source_type: benchmark_paper
    paper_pdf_or_html_checked: true
    no_paper_note: null
  counts:
    tasks: 3
    queries: 245
    split_local_documents: 30000
    positive_qrels: 253
  positives_per_query:
    average: 1.0326530612244897
    min: 1
    median: 1.0
    max: 2
    multi_positive_tasks: 1
    multi_positive_queries: 7
  text_stats_chars:
    query_mean_weighted_by_queries: 104.79591836734531
    document_mean_weighted_by_documents: 654.2387666666667
  bm25:
    ndcg_at_10_query_weighted: 0.869990365
    hit_at_10_query_weighted: 0.9387755102
    source: dataset_candidate_subset
    strongest_task_by_ndcg_at_10: NanoChemRxiv
    weakest_task_by_ndcg_at_10: NanoChemNQ
  tasks:
  - name: NanoChemHotpotQA
    path: docs/benchmark_tasks/NanoChemTEB/NanoChemHotpotQA.md
    retrieval_focus: chemistry_multihop_question_to_evidence_passage
    queries: 18
    documents: 10000
    positive_qrels: 18
    bm25_ndcg_at_10: 0.6496
    bm25_hit_at_10: 0.7222
  - name: NanoChemNQ
    path: docs/benchmark_tasks/NanoChemTEB/NanoChemNQ.md
    retrieval_focus: chemistry_natural_question_to_evidence_passage
    queries: 27
    documents: 10000
    positive_qrels: 35
    bm25_ndcg_at_10: 0.3616
    bm25_hit_at_10: 0.4815
  - name: NanoChemRxiv
    path: docs/benchmark_tasks/NanoChemTEB/NanoChemRxiv.md
    retrieval_focus: chemistry_question_to_chemrxiv_paragraph
    queries: 200
    documents: 10000
    positive_qrels: 200
    bm25_ndcg_at_10: 0.8718
    bm25_hit_at_10: 0.94
  learning:
    leakage_note: exclude NanoChemTEB evaluation queries, qrels, and positive documents;
      audit ChemTEB, ChemRxiv, HotpotQA, and Natural Questions overlap before training
    useful_training_data:
    - chemistry-focused QA evidence retrieval pairs
    - ChemRxiv or PubMed-style literature search pairs
    - scientific paragraph retrieval data with chemistry hard negatives
    - non-overlapping HotpotQA and Natural Questions evidence pairs
    synthetic_data:
      document_generation: chemistry passages with compounds, reactions, materials,
        methods, measurements, and paragraph-level evidence
      question_generation: chemistry questions answerable from selected non-evaluation
        passages
      answerability: positives must contain explicit chemical or scientific evidence
        for the query
    multi_positive_training: multi_positive_objective
  links:
    nano_dataset: https://huggingface.co/datasets/hakari-bench/NanoChemTEB
    source_urls:
    - label: ChemTEB PMLR
      url: https://proceedings.mlr.press/v262/shiraee-kasmaee24a.html
    - label: ChEmbed arXiv
      url: https://arxiv.org/abs/2508.01643
  references:
  - title: 'ChemTEB: Chemical Text Embedding Benchmark, an Overview of Embedding Models
      Performance & Efficiency on a Specific Domain'
    url: https://proceedings.mlr.press/v262/shiraee-kasmaee24a.html
    year: 2024
    is_paper: true
    source_confidence: definitive_paper_link
  - title: 'ChEmbed: Enhancing Chemical Literature Search Through Domain-Specific
      Text Embeddings'
    url: https://arxiv.org/abs/2508.01643
    year: 2025
    doi: 10.48550/arXiv.2508.01643
    is_paper: true
    source_confidence: definitive_paper_link
  candidate_subsets:
    bm25:
      query_weighted_ndcg_at_10: 0.869990365
      query_weighted_hit_at_10: 0.9387755102
      query_weighted_recall_at_100: 0.9751603499
      source: dataset_candidate_subset
    dense:
      query_weighted_ndcg_at_10: 0.8597498592
      query_weighted_hit_at_10: 0.9224489796
      query_weighted_recall_at_100: 0.984606414
      source: dataset_candidate_subset
    reranking_hybrid:
      query_weighted_ndcg_at_10: 0.8880241301
      query_weighted_hit_at_10: 0.9428571429
      query_weighted_recall_at_100: 0.996851312
      source: dataset_candidate_subset
```
