# NanoMLDR / en

## Overview

`en` is the English split of NanoMLDR. It asks models to retrieve very long
English articles from paragraph-grounded questions.

## Details

### What the Original Data Measures

[M3-Embedding](https://arxiv.org/abs/2402.03216) uses MLDR to test multilingual
long-document retrieval, a setting where the model must handle documents up to
long context lengths rather than short passages. The paper reports MLDR results
with NDCG@10 and observes that BM25 is competitive on long documents, while
hybrid dense/sparse/multi-vector retrieval performs best in their experiments.

The [MLDR dataset card](https://huggingface.co/datasets/Shitao/MLDR) lists
English as Wikipedia-sourced. Questions are generated from selected paragraphs,
but the retrieval target is the full article.

### Observed Data Profile

The Nano split has 200 queries, 10,000 documents, and 200 positive qrels. Each
query has one positive. Queries average 64.06 characters, while documents
average 27,991.90 characters, making this one of the longest NanoMLDR splits.
The examples cover rare-earth elements, aviation events, aquarium conservation,
taxonomy, and constitutional law.

### BM25 Difficulty

Using the dataset-provided BM25 candidate column, BM25 reaches nDCG@10 =
0.6351 and hit@10 = 0.7250. It ranks 108 positives first, but some positives are
at rank 31 or 100. The English split rewards lexical entity matching but also
tests whether retrievers can surface a whole article when the answer is buried
deep in a long document.

### Training Data That May Help

Useful training data includes English long-document QA retrieval, Wikipedia
article retrieval, NarrativeQA-style evidence retrieval, and hard negatives from
articles sharing named entities, dates, or scientific terms.

### Synthetic Data Guidance

Synthetic data should generate questions from a specific paragraph in a long
English article, while the positive is the full article. Hard negatives should
be topically adjacent full articles that share key entities but do not contain
the answer.

## Example Data

| Query | Positive document |
| --- | --- |
| Who was the last person mentioned in the text? (46 chars) | Chronological Classics was a French compact disc reissue label. Gilles Pétard, the original owner, intended to release the complete master takes of all jazz and swing recordings that were issued on 78 rpm. By the time the lab ... [truncated 225 chars](31958 chars) |
| What is one major limitation of PCR? (36 chars) | Polymerase chain reaction (PCR) is a method widely used to rapidly make millions to billions of copies (complete copies or partial copies) of a specific DNA sample, allowing scientists to take a very small sample of DNA and a ... [truncated 225 chars](49157 chars) |
| What did Ambassador Goldberg say about the US view of Jordan? (61 chars) | United Nations Security Council Resolution 242 (S/RES/242) was adopted unanimously by the UN Security Council on November 22, 1967, in the aftermath of the Six-Day War. It was adopted under Chapter VI of the UN Charter. The r ... [truncated 225 chars](44540 chars) |
| What is the time period in which Roman stiffeners are attributed to? (68 chars) | A composite bow is a traditional bow made from horn, wood, and sinew laminated together, a form of laminated bow. The horn is on the belly, facing the archer, and sinew on the outer side of a wooden core. When the bow is draw ... [truncated 225 chars](24773 chars) |
| What is the first step in the USERec method of DNA recombination? (65 chars) | Protein engineering is the process of developing useful or valuable proteins. It is a young discipline, with much research taking place into the understanding of protein folding and recognition for protein design principles. ... [truncated 225 chars](46771 chars) |

## Dataset Information

| Field | Value |
| --- | --- |
| Nano set | NanoMLDR |
| Backing dataset | NanoMLDR |
| Task / split | en |
| Hugging Face dataset | [hakari-bench/NanoMLDR](https://huggingface.co/datasets/hakari-bench/NanoMLDR) |
| Language | en |
| Category | natural_language |
| Queries | 200 |
| Documents | 10000 |
| Positive qrels | 200 |
| BM25 nDCG@10 | 0.6351 |
| BM25 hit@10 | 0.7250 |
| Query length avg chars | 64.06 |
| Document length avg chars | 27991.90 |

### Public Sources

- [M3-Embedding](https://arxiv.org/abs/2402.03216); 2024; Jianlv Chen et al.
- [ACL Anthology version](https://aclanthology.org/2024.findings-acl.137/); 2024.
- [MLDR dataset card](https://huggingface.co/datasets/Shitao/MLDR).

### Hugging Face Links

- Nano dataset: [hakari-bench/NanoMLDR](https://huggingface.co/datasets/hakari-bench/NanoMLDR)
- Source dataset: [Shitao/MLDR](https://huggingface.co/datasets/Shitao/MLDR)

### Source Reference Table

| Title | Year | Type | URL |
| --- | ---: | --- | --- |
| M3-Embedding: Multi-Linguality, Multi-Functionality, Multi-Granularity Text Embeddings Through Self-Knowledge Distillation | 2024 | benchmark paper | https://arxiv.org/abs/2402.03216 |
| MLDR: Multilingual Long-Document Retrieval dataset | 2024 | dataset card | https://huggingface.co/datasets/Shitao/MLDR |

## Machine-Readable Metadata

<!-- benchmark-task-metadata:v1 -->

```yaml
benchmark_task_metadata:
  schema_version: 1
  document_status: first_pass
  nano_set: NanoMLDR
  backing_dataset: NanoMLDR
  dataset_id: hakari-bench/NanoMLDR
  task_name: en
  split_name: en
  language: en
  category: natural_language
  document_path: docs/benchmark_tasks/NanoMLDR/en.md
  source_research:
    primary_source_type: benchmark_paper_and_dataset_card
    paper_pdf_or_html_checked: true
    no_paper_note: null
  counts:
    queries: 200
    documents: 10000
    positive_qrels: 200
  positives_per_query:
    average: 1.0
    min: 1
    median: 1.0
    max: 1
    multi_positive_queries: 0
    multi_positive_query_percent: 0.0
  text_stats_chars:
    query_mean: 64.06
    document_mean: 27991.8974
  bm25:
    ndcg_at_10: 0.6351102290874667
    hit_at_10: 0.725
    source: dataset_bm25_column
  learning:
    original_train_split: available
    evaluation_split_origin: MLDR English split
    train_eval_overlap_audit: not_audited
    leakage_note: exclude NanoMLDR en queries, qrels, and positive documents
    useful_training_data:
      - English long-document QA retrieval pairs
      - English Wikipedia article retrieval
      - NarrativeQA-style long-document evidence retrieval
      - entity-sharing article hard negatives
    synthetic_data:
      document_generation: long English encyclopedic articles
      question_generation: paragraph-grounded fact questions
      answerability: positives should be the full article containing the answer-bearing paragraph
    multi_positive_training: single_positive
  links:
    nano_dataset: https://huggingface.co/datasets/hakari-bench/NanoMLDR
    source_urls:
      - label: M3-Embedding arXiv
        url: https://arxiv.org/abs/2402.03216
      - label: Shitao/MLDR
        url: https://huggingface.co/datasets/Shitao/MLDR
    source_notes: []
  references:
    - title: "M3-Embedding: Multi-Linguality, Multi-Functionality, Multi-Granularity Text Embeddings Through Self-Knowledge Distillation"
      url: https://arxiv.org/abs/2402.03216
      year: 2024
      is_paper: true
      source_confidence: definitive_paper_link
```
