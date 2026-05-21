# NanoMTEB-Spanish / xpqa_eng_spa

## Overview

`xpqa_eng_spa` is an xPQA retrieval split where Spanish product questions are
matched to English product-answer candidates. The task models cross-lingual
product QA: a Spanish user asks about an item, and the retriever must find the
English candidate that contains the answer.

## Details

### What the Original Data Measures

[xPQA: Cross-Lingual Product Question Answering across 12 Languages](https://arxiv.org/abs/2305.09249)
introduces a product QA dataset for non-English questions answered from English
product information. The paper defines candidate ranking as selecting the best
English candidate containing enough information to answer the question, and it
reports that in-domain product data is critical because rankers trained on
other domains transfer poorly.

### Observed Data Profile

The Nano split has 200 mostly Spanish queries, 1,936 mostly English candidate
documents, and 491 positive qrels. Queries average 45.16 characters, documents
average 123.43 characters, and 63.5% of queries have multiple positives.
Examples include questions about transfer rates, washing an item, guitar model
type, mirror pricing, and whether a rack set includes a mat.

The documents are short product review or answer snippets, often informal and
elliptical. Some positives are English, while a sampled positive for mirror
pricing is Spanish, so the corpus is mostly but not perfectly English.

### BM25 Difficulty

Using the dataset-provided BM25 candidate column, BM25 reaches nDCG@10 =
0.0946 and hit@10 = 0.1750. The median best rank is 98.0. This is a hard
lexical baseline because many Spanish queries must retrieve English snippets
with little direct token overlap.

### Training Data That May Help

Useful training data includes xPQA train examples, bilingual product QA pairs,
Spanish-to-English product candidate ranking data, and in-domain e-commerce
hard negatives from the same product category. Training should exclude xPQA
test examples, Nano queries, qrels, and positive candidates.

### Synthetic Data Guidance

Generate Spanish product questions and English product snippets that answer
them. Include specifications, compatibility, quantities, sizes, washing
instructions, model variants, and customer-review wording. Use multiple
positives when several snippets answer the same question.

## Example Data

| Query | Positive document |
| --- | --- |
| el pack de 3 cintas, ¿es una de cada tamaño o las 3 del mismo tamaño? (69 chars) | gm climbing pack of 3 16mm nylon sling runner 120cm / 48inch (gray) (67 chars) |
| que son tallas grandes o justas? (32 chars) | The waist-tightening and slim-fitting design hides your proud flesh at your waist and instead forms a curve there. (114 chars) |
| és el modelo acústico o electro acústico? (41 chars) | martin drs2 dreadnought acoustic-electric guitar (48 chars) |
| como se que tamaño pedir,? (26 chars) | i encourage people to measure your wrist before purchasing; for reference my wrist is 5.5 inches around. (104 chars) |
| si compro un pack vendran 12 unidades? (38 chars) | "unit_count": [{"type": {"value": "count"}, "value": 12}] (57 chars) |

## Dataset Information

| Field | Value |
| --- | --- |
| Nano set | NanoMTEB-Spanish |
| Backing dataset | NanoMTEB-Spanish |
| Task / split | xpqa_eng_spa |
| Hugging Face dataset | [hakari-bench/NanoMTEB-Spanish](https://huggingface.co/datasets/hakari-bench/NanoMTEB-Spanish) |
| Language | es, en |
| Category | natural_language |
| Queries | 200 |
| Documents | 1936 |
| Positive qrels | 491 |
| Avg positives / query | 2.46 |
| Positives per query (min / median / max) | 1 / 2.0 / 5 |
| Queries with multiple positives | 127 (63.50%) |
| BM25 nDCG@10 | 0.0946 |
| BM25 hit@10 | 0.1750 |
| Query length avg chars | 45.16 |
| Document length avg chars | 123.43 |

### Public Sources

- [xPQA: Cross-Lingual Product Question Answering across 12 Languages](https://arxiv.org/abs/2305.09249); 2023; Xiaoyu Shen et al.
- [mteb/XPQARetrieval dataset card](https://huggingface.co/datasets/mteb/XPQARetrieval).
- [MTEB: Massive Text Embedding Benchmark](https://arxiv.org/abs/2210.07316); 2023; Niklas Muennighoff et al.

### Hugging Face Links

- Nano dataset: [hakari-bench/NanoMTEB-Spanish](https://huggingface.co/datasets/hakari-bench/NanoMTEB-Spanish)
- Source dataset: [mteb/XPQARetrieval](https://huggingface.co/datasets/mteb/XPQARetrieval)

### Source Reference Table

| Title | Year | Type | URL |
| --- | ---: | --- | --- |
| xPQA: Cross-Lingual Product Question Answering across 12 Languages | 2023 | arXiv paper | https://arxiv.org/abs/2305.09249 |
| MTEB: Massive Text Embedding Benchmark | 2023 | arXiv paper | https://arxiv.org/abs/2210.07316 |
| mteb/XPQARetrieval | 2025 | dataset card | https://huggingface.co/datasets/mteb/XPQARetrieval |

## Machine-Readable Metadata

<!-- benchmark-task-metadata:v1 -->

```yaml
benchmark_task_metadata:
  schema_version: 1
  document_status: first_pass
  nano_set: NanoMTEB-Spanish
  backing_dataset: NanoMTEB-Spanish
  dataset_id: hakari-bench/NanoMTEB-Spanish
  task_name: xpqa_eng_spa
  split_name: xpqa_eng_spa
  language: multilingual
  category: natural_language
  document_path: docs/benchmark_tasks/NanoMTEB-Spanish/xpqa_eng_spa.md
  source_research:
    primary_source_type: task_paper
    paper_pdf_or_html_checked: true
    no_paper_note: null
  counts:
    queries: 200
    documents: 1936
    positive_qrels: 491
  positives_per_query:
    average: 2.455
    min: 1
    median: 2.0
    max: 5
    multi_positive_queries: 127
    multi_positive_query_percent: 63.5
  text_stats_chars:
    query_mean: 45.16
    document_mean: 123.42923553719008
  bm25:
    ndcg_at_10: 0.0946244797
    hit_at_10: 0.175
    source: dataset_bm25_column
  learning:
    original_train_split: available
    evaluation_split_origin: test
    train_eval_overlap_audit: not_audited
    leakage_note: exclude xPQA test examples, Nano queries, qrels, and positive product candidates
    useful_training_data:
      - xPQA train examples
      - bilingual Spanish-to-English product QA pairs
      - e-commerce candidate ranking data
      - hard negatives from the same product category
    synthetic_data:
      document_generation: English product snippets with specifications, compatibility, quantities, sizes, instructions, and review-like evidence
      question_generation: Spanish product questions asking about those properties
      answerability: each positive snippet should contain enough information to answer the product question
    multi_positive_training: multi_positive_objective
  links:
    nano_dataset: https://huggingface.co/datasets/hakari-bench/NanoMTEB-Spanish
    source_urls:
      - label: xPQA arXiv
        url: https://arxiv.org/abs/2305.09249
      - label: mteb/XPQARetrieval
        url: https://huggingface.co/datasets/mteb/XPQARetrieval
      - label: MTEB arXiv
        url: https://arxiv.org/abs/2210.07316
    source_notes: []
  references:
    - title: "xPQA: Cross-Lingual Product Question Answering across 12 Languages"
      url: https://arxiv.org/abs/2305.09249
      year: 2023
      doi: 10.48550/arXiv.2305.09249
      is_paper: true
      source_confidence: definitive_paper_link
```
