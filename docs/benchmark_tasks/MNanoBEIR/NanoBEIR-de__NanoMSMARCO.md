# MNanoBEIR / NanoBEIR-de / NanoMSMARCO

## Overview

MS MARCO is a large-scale web question answering and passage ranking benchmark
built from real search queries. `NanoBEIR-de__NanoMSMARCO` is the German
MNanoBEIR version: each query is a short German translated web-search style
question, and the system must retrieve the German translated answer-bearing
passage. The task tests short-query passage retrieval over everyday web topics.

## Details

### What the Original Data Measures

[MS MARCO: A Human Generated MAchine Reading COmprehension Dataset](https://arxiv.org/abs/1611.09268)
introduces a dataset of anonymized Bing search questions paired with passages
from web documents and human-generated answers. The paper emphasizes that these
questions are sampled from real user search logs rather than written from a
known paragraph, so they include ambiguity, fragments, definitions, and practical
information needs.

[BEIR: A Heterogeneous Benchmark for Zero-shot Evaluation of Information
Retrieval Models](https://arxiv.org/abs/2104.08663) includes MS MARCO as a
question-answering retrieval task. [MMTEB: Massive Multilingual Text Embedding
Benchmark](https://arxiv.org/abs/2502.13595) provides the multilingual
evaluation context for this German NanoBEIR split.

### Observed Data Profile

The sampled German Nano task has 50 queries, 5,043 documents, and 50 positive
qrel rows. Every query has one positive passage. The average query length is
41.02 characters, and the average document length is 363.65 characters.

The inspected queries ask practical and definitional web questions: refrigerated
storage time for cooked Italian sausage, what is good in health care, who leads
Google, alternatives to a coffee filter, and the definition of voluntary
muscles. Positive documents are concise translated web answer passages that
often explain the answer in a few sentences.

### BM25 Difficulty

Using the dataset-provided BM25 candidate column, BM25 reaches nDCG@10 =
0.2839 and hit@10 = 0.4800. Only 7 of 50 queries have the positive ranked
first, and the median first-positive rank is 12.

Sparse matching is limited because many queries are short and ask for an answer
rather than a document title. A query such as `Was ist gut in der
Gesundheitsversorgung?` requires recognizing that a passage about the right to
health and access to services answers the intent. Strong models should capture
answerability and paraphrase, not only repeated German keywords.

### Training Data That May Help

Useful training data includes non-overlapping MS MARCO passage-ranking pairs,
German or multilingual web QA retrieval pairs, search-query to answer-passage
data, and noisy user-query corpora. Because MS MARCO is widely used for
retriever training, overlap audits are important for interpreting high scores.

Training should exclude MS MARCO, BEIR, NanoBEIR, or translated records likely
to overlap with these evaluation queries or passages.

### Synthetic Data Guidance

For document-to-query generation, start from non-evaluation German web answer
passages and generate short realistic search questions. Include definitions,
how-long questions, consumer advice, names, leadership questions, and ambiguous
fragments.

For joint generation, create concise web-style passages across broad everyday
topics and pair them with German queries that the passage directly answers.

## Example Data

| Query | Positive document |
| --- | --- |
| Was ist das Ruminationssyndrom? (31 chars) | Ruminationssyndrom, auch Merykismus genannt, ist eine nicht näher bezeichnete Essstörung, die das Erbrechen von Nahrung verursacht. Obwohl es im DSM-IV nicht als spezifische Essstörung identifiziert wird, wurden bestimmte Kri ... [truncated 225 chars](272 chars) |
| Wer hat den Song "Here I Go Again" gesungen? (44 chars) | Für andere Verwendungen siehe Here I Go Again (Bedeutungsübersicht). Here I Go Again ist ein Lied der britischen Rockband Whitesnake. Ursprünglich erschien das Lied 1982 auf ihrem Album Saints & Sinners. Für das gleichnamige ... [truncated 225 chars](368 chars) |
| Wen spielt Cameron Boyce in Liv und Maddie? (43 chars) | Bereitet euch auf ordentlich Lacher vor, Leute. In einem exklusiven Vorab-Blick auf die Folge vom 19. April von Liv & Maddie mit dem Titel „Prom-A-Rooney.“ Natürlich. Im lustigen Clip sehen wir den Jessie-Star Cameron Boyce i ... [truncated 225 chars](344 chars) |
| Wo liegen die meisten großen Wüsten der Erde? (45 chars) | Die übrigen Wüsten der Erde liegen außerhalb der Polargebiete. Die größte ist die Sahara, eine subtropische Wüste in Nordafrika. (128 chars) |
| Was bedeutet "copper" für einen Polizisten? (43 chars) | Aufgrund der aktuellen Erkenntnisse scheint es, dass 'Bulle' (ein Polizist, wörtlich 'jemand, der festnimmt') älter ist als 'cop', das entweder als Verb im Sinne von 'festnehmen' oder als Substantiv im Sinne von 'Polizist' ve ... [truncated 225 chars](458 chars) |

## Dataset Information

| Field | Value |
| --- | --- |
| Nano set | MNanoBEIR |
| Backing dataset | NanoBEIR-de |
| Task / split | NanoMSMARCO |
| Hugging Face dataset | [hakari-bench/NanoBEIR-de](https://huggingface.co/datasets/hakari-bench/NanoBEIR-de) |
| Language | de |
| Category | natural_language |
| Queries | 50 |
| Documents | 5,043 |
| Positive qrels | 50 |
| BM25 nDCG@10 | 0.2839 |
| BM25 hit@10 | 0.4800 |
| Query length avg chars | 41.02 |
| Document length avg chars | 363.65 |

### Public Sources

- [MS MARCO: A Human Generated MAchine Reading COmprehension Dataset](https://arxiv.org/abs/1611.09268); 2016; Payal Bajaj, Daniel Campos, Nick Craswell, Li Deng, Jianfeng Gao, Xiaodong Liu, Rangan Majumder, Andrew McNamara, Bhaskar Mitra, Tri Nguyen, Mir Rosenberg, Xia Song, Alina Stoica, Saurabh Tiwary, Tong Wang; DOI: `10.48550/arXiv.1611.09268`.
- [MS MARCO dataset site](https://microsoft.github.io/msmarco/Datasets.html).
- [BEIR: A Heterogeneous Benchmark for Zero-shot Evaluation of Information Retrieval Models](https://arxiv.org/abs/2104.08663); 2021; Nandan Thakur, Nils Reimers, Andreas Rueckle, Abhishek Srivastava, Iryna Gurevych; DOI: `10.48550/arXiv.2104.08663`.
- [MMTEB: Massive Multilingual Text Embedding Benchmark](https://arxiv.org/abs/2502.13595); 2025; Kenneth Enevoldsen, Isaac Chung, Imene Kerboua, Marton Kardos, Ashwin Mathur, and others; DOI: `10.48550/arXiv.2502.13595`.
- [Zeta Alpha NanoBEIR collection](https://huggingface.co/collections/zeta-alpha-ai/nanobeir).

### Hugging Face Links

- Nano dataset: [hakari-bench/NanoBEIR-de](https://huggingface.co/datasets/hakari-bench/NanoBEIR-de)
- Source collection: [Zeta Alpha NanoBEIR collection](https://huggingface.co/collections/zeta-alpha-ai/nanobeir)

### Source Reference Table

| Title | Year | Type | URL |
| --- | ---: | --- | --- |
| MS MARCO: A Human Generated MAchine Reading COmprehension Dataset | 2016 | task paper | https://arxiv.org/abs/1611.09268 |
| MS MARCO dataset site |  | dataset page | https://microsoft.github.io/msmarco/Datasets.html |
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
  task_name: NanoMSMARCO
  split_name: NanoMSMARCO
  language: de
  category: natural_language
  document_path: docs/benchmark_tasks/MNanoBEIR/NanoBEIR-de__NanoMSMARCO.md
  source_research:
    primary_source_type: task_paper
    paper_pdf_or_html_checked: true
    no_paper_note: null
  counts:
    queries: 50
    documents: 5043
    positive_qrels: 50
  positives_per_query:
    average: 1.0
    min: 1
    median: 1.0
    max: 1
    multi_positive_queries: 0
    multi_positive_query_percent: 0.0
  text_stats_chars:
    query_mean: 41.02
    document_mean: 363.651795
  bm25:
    ndcg_at_10: 0.2839342646
    hit_at_10: 0.48
    source: dataset_bm25_column
  learning:
    original_train_split: available
    evaluation_split_origin: MNanoBEIR German NanoBEIR task split from hakari-bench/NanoBEIR-de
    train_eval_overlap_audit: not_audited
    leakage_note: prefer excluding MS MARCO, BEIR, or NanoBEIR records likely to overlap with these evaluation queries or passages
    useful_training_data:
      - non-overlapping MS MARCO passage-ranking pairs
      - German or multilingual web QA retrieval data
      - search query to answer-passage pairs
      - noisy real user question datasets
    synthetic_data:
      document_generation: concise German web-style answer passages across everyday domains
      question_generation: realistic short German search questions with definitions, how-long questions, names, and noisy phrasing
      answerability: positives should directly answer the user information need, not merely share keywords
    multi_positive_training: not_required_for_this_sample
  links:
    nano_dataset: https://huggingface.co/datasets/hakari-bench/NanoBEIR-de
    source_urls:
      - label: MS MARCO paper
        url: https://arxiv.org/abs/1611.09268
      - label: MS MARCO dataset site
        url: https://microsoft.github.io/msmarco/Datasets.html
      - label: BEIR paper
        url: https://arxiv.org/abs/2104.08663
      - label: MMTEB paper
        url: https://arxiv.org/abs/2502.13595
      - label: Zeta Alpha NanoBEIR collection
        url: https://huggingface.co/collections/zeta-alpha-ai/nanobeir
    source_notes:
      - German task is a multilingual NanoBEIR adaptation of the original English BEIR task
  references:
    - title: "MS MARCO: A Human Generated MAchine Reading COmprehension Dataset"
      url: https://arxiv.org/abs/1611.09268
      year: 2016
      doi: 10.48550/arXiv.1611.09268
      is_paper: true
      source_confidence: definitive_paper_link
    - title: MS MARCO dataset site
      url: https://microsoft.github.io/msmarco/Datasets.html
      year: null
      doi: null
      is_paper: false
      source_confidence: definitive_dataset_page
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
