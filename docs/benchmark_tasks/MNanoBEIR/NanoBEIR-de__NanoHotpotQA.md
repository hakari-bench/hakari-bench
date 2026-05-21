# MNanoBEIR / NanoBEIR-de / NanoHotpotQA

## Overview

HotpotQA is a multi-hop question answering benchmark built from Wikipedia.
`NanoBEIR-de__NanoHotpotQA` is the German MNanoBEIR version: each query is a
German translated multi-hop question, and the system must retrieve German
translated supporting Wikipedia passages. The task tests whether a retriever
can surface all required evidence pages, not just a single obvious entity page.

## Details

### What the Original Data Measures

[HotpotQA: A Dataset for Diverse, Explainable Multi-hop Question
Answering](https://arxiv.org/abs/1809.09600) introduces a Wikipedia QA dataset
designed to require reasoning over multiple supporting documents. The paper
builds bridge questions from the Wikipedia hyperlink graph and comparison
questions over similar entities, with sentence-level supporting facts.

[BEIR: A Heterogeneous Benchmark for Zero-shot Evaluation of Information
Retrieval Models](https://arxiv.org/abs/2104.08663) includes HotpotQA as a
question-answering retrieval task where supporting Wikipedia evidence must be
retrieved. [MMTEB: Massive Multilingual Text Embedding Benchmark](https://arxiv.org/abs/2502.13595)
provides the multilingual benchmark context for this German Nano split.

### Observed Data Profile

The sampled German Nano task has 50 queries, 5,090 documents, and 100 positive
qrel rows. Every query has exactly two positives, so complete retrieval means
finding both supporting passages. The average query length is 99.82 characters,
and the average document length is 386.24 characters.

The inspected queries include comparison and bridge questions: which magazine
is published in more countries, a question starting from an actress in "Friday
Night Lights", a Gambino-family crime question, a question about the meaning of
`Jal Pari`, and a film-credit question. Positive documents are short German
translated Wikipedia-style entity descriptions.

### BM25 Difficulty

Using the dataset-provided BM25 candidate column, BM25 reaches nDCG@10 =
0.7743 and hit@10 = 1.0000. BM25 ranks a positive first for 38 of 50 queries,
and every query has a positive in the top 10.

The real difficulty is retrieving both positives. A system that finds only the
most lexically obvious entity page can still miss the second evidence page
needed for the reasoning chain or comparison. German translation also mixes
translated and original names, so a strong retriever should preserve bridge
relations, comparison framing, and entity aliases.

### Training Data That May Help

Useful training data includes non-overlapping HotpotQA examples with supporting
facts, multi-hop QA retrieval datasets, Wikipedia hyperlink graph retrieval
pairs, and German or multilingual question-to-multiple-document supervision.
Training should exclude HotpotQA, BEIR, NanoBEIR, or translated records likely
to overlap with these evaluation questions or supporting pages.

### Synthetic Data Guidance

For document-to-query generation, start from pairs of non-evaluation
Wikipedia-style passages connected by a hyperlink, shared type, or comparison
attribute, then generate German questions requiring both passages. Synthetic
questions answerable from only one passage are less useful for this task.

## Example Data

| Query | Positive document |
| --- | --- |
| Mit welchem anderen Schauspieler spielte Penny Rae Bridges in einer Fernseh-Sitcom? (83 chars) | Penny Rae Bridges (geboren am 29. Juli 1990) ist eine amerikanische Schauspielerin. Sie hat in folgenden Serien mitgespielt: "For Your Love", "Family Law", "Boy Meets World" und "The Parent 'Hood". Bekannt wurde sie durch ihr ... [truncated 225 chars](269 chars) |
| Wer hat Kaganoi Shigemochi ein Schwert überreicht, das vom Gründer der Muramasa-Schule hergestellt wurde? (105 chars) | Kaganoi Shigemochi (加賀井 重望, 1561 – 27. August 1600) war ein japanischer Samurai der Azuchi-Momoyama-Zeit, der dem Oda-Clan diente. Er herrschte über die Burg Kaganoi. Während der Schlacht von Komaki und Nagakute kämpfte Shige ... [truncated 225 chars](611 chars) |
| Welcher Film wurde von Joby Harold geschrieben und inszeniert und hat Musik von Samuel Sim? (91 chars) | Samuel Sim ist ein Film- und Fernsehkomponist. Er erlangte erstmals Anerkennung durch seine preisgekrönte Filmmusik zur BBC-Dramaserie "Dunkirk". Seitdem hat er die Musik für eine Vielzahl von Film- und Fernsehproduktionen ko ... [truncated 225 chars](509 chars) |
| Wann fand dieses College-Football-Spiel im Sun Life Stadium in Miami Gardens, Florida statt, bei dem die Clemson Tigers die auf Platz 4 platzierten Oklahoma Sooners mit 37-17 besiegten? (185 chars) | Das Football-Team der Clemson Tigers aus dem Jahr 2015 vertrat die Clemson University in der Saison 2015 der NCAA Division I FBS. Die Tigers wurden von Head Coach Dabo Swinney angeführt, der in seinem siebten vollständigen Ja ... [truncated 225 chars](1192 chars) |
| Wie heißt die Sammlung von Singles der amerikanischen Rock-’n’-Roll-Band, die auch unter welchem Namen Country-Shows spielt? (124 chars) | Devil's Food ist ein Sampler der amerikanischen Rock 'n' Roll-Band Supersuckers, erschienen im April 2005 bei Mid-Fi Records. (125 chars) |

## Dataset Information

| Field | Value |
| --- | --- |
| Nano set | MNanoBEIR |
| Backing dataset | NanoBEIR-de |
| Task / split | NanoHotpotQA |
| Hugging Face dataset | [hakari-bench/NanoBEIR-de](https://huggingface.co/datasets/hakari-bench/NanoBEIR-de) |
| Language | de |
| Category | natural_language |
| Queries | 50 |
| Documents | 5,090 |
| Positive qrels | 100 |
| Avg positives / query | 2.00 |
| Positives per query (min / median / max) | 2 / 2.00 / 2 |
| Queries with multiple positives | 50 (100.0%) |
| BM25 nDCG@10 | 0.7743 |
| BM25 hit@10 | 1.0000 |
| Query length avg chars | 99.82 |
| Document length avg chars | 386.24 |

### Public Sources

- [HotpotQA: A Dataset for Diverse, Explainable Multi-hop Question Answering](https://arxiv.org/abs/1809.09600); 2018; Zhilin Yang, Peng Qi, Saizheng Zhang, Yoshua Bengio, William W. Cohen, Ruslan Salakhutdinov, Christopher D. Manning; DOI: `10.18653/v1/D18-1259`.
- [HotpotQA official site](https://hotpotqa.github.io/).
- [BEIR: A Heterogeneous Benchmark for Zero-shot Evaluation of Information Retrieval Models](https://arxiv.org/abs/2104.08663); 2021; Nandan Thakur, Nils Reimers, Andreas Rueckle, Abhishek Srivastava, Iryna Gurevych; DOI: `10.48550/arXiv.2104.08663`.
- [MMTEB: Massive Multilingual Text Embedding Benchmark](https://arxiv.org/abs/2502.13595); 2025; Kenneth Enevoldsen, Isaac Chung, Imene Kerboua, Marton Kardos, Ashwin Mathur, and others; DOI: `10.48550/arXiv.2502.13595`.
- [Zeta Alpha NanoBEIR collection](https://huggingface.co/collections/zeta-alpha-ai/nanobeir).

### Hugging Face Links

- Nano dataset: [hakari-bench/NanoBEIR-de](https://huggingface.co/datasets/hakari-bench/NanoBEIR-de)
- Source collection: [Zeta Alpha NanoBEIR collection](https://huggingface.co/collections/zeta-alpha-ai/nanobeir)

### Source Reference Table

| Title | Year | Type | URL |
| --- | ---: | --- | --- |
| HotpotQA: A Dataset for Diverse, Explainable Multi-hop Question Answering | 2018 | task paper | https://arxiv.org/abs/1809.09600 |
| HotpotQA official site |  | project page | https://hotpotqa.github.io/ |
| BEIR: A Heterogeneous Benchmark for Zero-shot Evaluation of Information Retrieval Models | 2021 | benchmark paper | https://arxiv.org/abs/2104.08663 |
| MMTEB: Massive Multilingual Text Embedding Benchmark | 2025 | benchmark paper | https://arxiv.org/abs/2502.13595 |
| NanoBEIR: Smaller BEIR dataset subsets | 2024 | dataset collection | https://huggingface.co/collections/zeta-alpha-ai/nanobeir |

## Machine-Readable Metadata

<!-- benchmark-task-metadata:v1 -->

```yaml
benchmark_task_metadata:
  schema_version: 1
  document_status: first_pass
  nano_set: MNanoBEIR
  backing_dataset: NanoBEIR-de
  dataset_id: hakari-bench/NanoBEIR-de
  task_name: NanoHotpotQA
  split_name: NanoHotpotQA
  language: de
  category: natural_language
  document_path: docs/benchmark_tasks/MNanoBEIR/NanoBEIR-de__NanoHotpotQA.md
  source_research:
    primary_source_type: task_paper
    paper_pdf_or_html_checked: true
    no_paper_note: null
  counts:
    queries: 50
    documents: 5090
    positive_qrels: 100
  positives_per_query:
    average: 2.0
    min: 2
    median: 2.0
    max: 2
    multi_positive_queries: 50
    multi_positive_query_percent: 100.0
  text_stats_chars:
    query_mean: 99.82
    document_mean: 386.235953
  bm25:
    ndcg_at_10: 0.7743150467
    hit_at_10: 1.0
    source: dataset_bm25_column
  learning:
    original_train_split: available
    evaluation_split_origin: MNanoBEIR German NanoBEIR task split from hakari-bench/NanoBEIR-de
    train_eval_overlap_audit: not_audited
    leakage_note: prefer excluding HotpotQA, BEIR, or NanoBEIR records likely to overlap with these evaluation questions or supporting pages
    useful_training_data:
      - non-overlapping HotpotQA examples with supporting facts
      - German or multilingual multi-hop QA retrieval datasets
      - Wikipedia hyperlink graph retrieval pairs
      - question-to-multiple-document supervision
    synthetic_data:
      document_generation: paired German Wikipedia-style entity passages connected by hyperlinks, shared types, dates, locations, occupations, creators, or memberships
      question_generation: German bridge and comparison questions that require both generated passages
      answerability: positives should be both documents needed for the reasoning path, not a single answer-bearing passage
    multi_positive_training: required
  links:
    nano_dataset: https://huggingface.co/datasets/hakari-bench/NanoBEIR-de
    source_urls:
      - label: HotpotQA paper
        url: https://arxiv.org/abs/1809.09600
      - label: HotpotQA official site
        url: https://hotpotqa.github.io/
      - label: BEIR paper
        url: https://arxiv.org/abs/2104.08663
      - label: MMTEB paper
        url: https://arxiv.org/abs/2502.13595
      - label: Zeta Alpha NanoBEIR collection
        url: https://huggingface.co/collections/zeta-alpha-ai/nanobeir
    source_notes:
      - German task is a multilingual NanoBEIR adaptation of the original English BEIR task
  references:
    - title: "HotpotQA: A Dataset for Diverse, Explainable Multi-hop Question Answering"
      url: https://arxiv.org/abs/1809.09600
      year: 2018
      doi: 10.18653/v1/D18-1259
      is_paper: true
      source_confidence: definitive_paper_link
    - title: HotpotQA official site
      url: https://hotpotqa.github.io/
      year: null
      doi: null
      is_paper: false
      source_confidence: definitive_project_page
    - title: "BEIR: A Heterogeneous Benchmark for Zero-shot Evaluation of Information Retrieval Models"
      url: https://arxiv.org/abs/2104.08663
      year: 2021
      doi: 10.48550/arXiv.2104.08663
      is_paper: true
      source_confidence: benchmark_context_paper
    - title: "MMTEB: Massive Multilingual Text Embedding Benchmark"
      url: https://arxiv.org/abs/2502.13595
      year: 2025
      doi: 10.48550/arXiv.2502.13595
      is_paper: true
      source_confidence: benchmark_context_paper
    - title: "NanoBEIR: Smaller BEIR dataset subsets"
      url: https://huggingface.co/collections/zeta-alpha-ai/nanobeir
      year: 2024
      doi: null
      is_paper: false
      source_confidence: dataset_collection
```
