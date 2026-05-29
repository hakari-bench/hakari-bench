# MNanoBEIR / NanoBEIR-sv / NanoFiQA2018

## Overview

FiQA is a financial question-answer retrieval task. `NanoBEIR-sv__NanoFiQA2018`
uses Swedish translated finance questions and answer passages.

## Details

### What the Original Data Measures

[FiQA](https://doi.org/10.1145/3184558.3192301) introduced financial opinion and
QA data. BEIR evaluates answer-passage retrieval, and MMTEB provides the
multilingual context.

### Observed Data Profile

The task has 50 queries, 4,598 documents, and 123 positive qrels. There are
multiple positives for 28 queries, with average 2.46 and maximum 15. Queries
average 62.24 characters, and documents average 925.72 characters.

### BM25 Difficulty

BM25 reaches nDCG@10 = 0.1159 and hit@10 = 0.2800. The median first-positive
rank is 81.0, making this a difficult lexical retrieval task.

### Training Data That May Help

Use non-overlapping Swedish financial QA, multilingual finance retrieval, and
multi-positive answer ranking. Exclude FiQA, BEIR, NanoBEIR, and translated
evaluation answers.

### Synthetic Data Guidance

Generate Swedish personal-finance questions from realistic answer passages.
Hard negatives should use the same finance terms but answer a different need.

## Example Data

| Query | Positive document |
| --- | --- |
| Vilken typ av avkastning anger Vanguard? (40 chars) | På Vanguard-sidan - Detta verkade vara det enklaste eftersom S&P-data är lätt att hitta. Jag använder MoneyChimp för att bekräfta att Vanguards sida erbjuder CAGR, inte aritmetiskt medelvärde. Vanguard anger att 'för amerikan ... [truncated 225 chars](405 chars) |
| Skattekonsekvenser vid frilansarbete (36 chars) | Om du har inkomst i USA, måste du betala amerikansk inkomstskatt på den, om det inte finns ett avtal mellan ditt land och USA som säger annat. (142 chars) |
| Vad betraktas som hög eller låg volym? (38 chars) | Den dagliga volymen jämförs vanligtvis med den genomsnittliga dagliga volymen över de senaste 50 dagarna för en aktie. Hög volym anses vanligtvis vara 2 eller fler gånger den genomsnittliga dagliga volymen över de senaste 50 ... [truncated 225 chars](720 chars) |
| Använda kreditkortspoäng för att betala skatteavdragsbara företagsutgifter (74 chars) | För enkelhetens skull, låt oss börja med att bara överväga cashback. Generellt sett är cashback från kreditkort för privat bruk inte skattepliktigt, men för företagsbruk är det skattepliktigt (sådär, jag kommer att förklara s ... [truncated 225 chars](3667 chars) |
| Hur ska jag skicka in min deklaration som kontraktör? (53 chars) | För skattemål måste du deklarera som anställd (T4-kvitton och skatt dras automatiskt), men också som företagare. Jag hade samma situation själv förra året. Publikationen "Anställd och självständigt arbetande" från Skatteverke ... [truncated 225 chars](691 chars) |

## Dataset Information

| Field | Value |
| --- | --- |
| Nano set | MNanoBEIR |
| Backing dataset | NanoBEIR-sv |
| Task / split | NanoFiQA2018 |
| Hugging Face dataset | [hakari-bench/NanoBEIR-sv](https://huggingface.co/datasets/hakari-bench/NanoBEIR-sv) |
| Language | sv |
| Category | natural_language |
| Queries | 50 |
| Documents | 4,598 |
| Positive qrels | 123 |
| Positives per query avg | 2.46 |
| Positives per query min / median / max | 1 / 2.0 / 15 |
| Multi-positive queries | 28 (56.00%) |
| BM25 nDCG@10 | 0.1159 |
| BM25 hit@10 | 0.2800 |
| BM25 Recall@100 | 0.3984 |
| BM25 candidate subset | top-500 (`bm25`) |
| Dense nDCG@10 | 0.3435 |
| Dense hit@10 | 0.6000 |
| Dense Recall@100 | 0.6748 |
| Dense candidate subset | top-500 (`harrier_oss_v1_270m`) |
| Reranking hybrid nDCG@10 | 0.2256 |
| Reranking hybrid hit@10 | 0.4600 |
| Reranking hybrid Recall@100 | 0.6911 |
| Reranking hybrid candidate subset | top-100 plus optional rank-101 safeguard (`reranking_hybrid`) |
| Reranking hybrid candidates / query | 100-101 |
| Reranking hybrid safeguard rows | 8 |
| Query length avg chars | 62.24 |
| Document length avg chars | 925.72 |

### Public Sources

- [FiQA](https://doi.org/10.1145/3184558.3192301), [BEIR](https://arxiv.org/abs/2104.08663), [MMTEB](https://arxiv.org/abs/2502.13595), and [NanoBEIR](https://huggingface.co/collections/zeta-alpha-ai/nanobeir).

### Hugging Face Links

- Nano dataset: [hakari-bench/NanoBEIR-sv](https://huggingface.co/datasets/hakari-bench/NanoBEIR-sv)
- Source collection: [Zeta Alpha NanoBEIR collection](https://huggingface.co/collections/zeta-alpha-ai/nanobeir)

### Source Reference Table

| Title | Year | Type | URL |
| --- | ---: | --- | --- |
| FiQA: Financial Opinion Mining and Question Answering | 2018 | task paper | https://doi.org/10.1145/3184558.3192301 |
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
  backing_dataset: NanoBEIR-sv
  dataset_id: hakari-bench/NanoBEIR-sv
  task_name: NanoFiQA2018
  split_name: NanoFiQA2018
  language: sv
  category: natural_language
  document_path: docs/benchmark_tasks/MNanoBEIR/NanoBEIR-sv__NanoFiQA2018.md
  source_research:
    primary_source_type: task_paper
    paper_pdf_or_html_checked: true
    no_paper_note: null
  counts:
    queries: 50
    documents: 4598
    positive_qrels: 123
  positives_per_query:
    average: 2.46
    min: 1
    median: 2.0
    max: 15
    multi_positive_queries: 28
    multi_positive_query_percent: 56.0
  text_stats_chars:
    query_mean: 62.24
    document_mean: 925.723793
  bm25:
    ndcg_at_10: 0.11590945590387575
    hit_at_10: 0.28
    source: dataset_candidate_subset
  candidate_subsets:
    bm25:
      config: bm25
      label: BM25
      source: dataset_candidate_subset
      top_k: 500
      ndcg_at_10: 0.1159094559
      hit_at_10: 0.28
      recall_at_100: 0.3983739837
      candidate_count_min: 500
      candidate_count_max: 500
      candidate_count_mean: 500.0
      query_count: 50
      query_coverage: 1.0
      relevant_coverage_at_100: 0.3983739837
    dense:
      config: harrier_oss_v1_270m
      label: Dense
      source: dataset_candidate_subset
      top_k: 500
      ndcg_at_10: 0.3435238262
      hit_at_10: 0.6
      recall_at_100: 0.674796748
      candidate_count_min: 500
      candidate_count_max: 500
      candidate_count_mean: 500.0
      query_count: 50
      query_coverage: 1.0
      relevant_coverage_at_100: 0.674796748
    reranking_hybrid:
      config: reranking_hybrid
      label: Reranking hybrid
      source: dataset_candidate_subset
      top_k: 100
      ndcg_at_10: 0.2255857258
      hit_at_10: 0.46
      recall_at_100: 0.6910569106
      candidate_count_min: 100
      candidate_count_max: 101
      candidate_count_mean: 100.16
      query_count: 50
      query_coverage: 1.0
      relevant_coverage_at_100: 0.6910569106
      safeguard_positive_rows: 8
      rows_with_101_candidates: 8
```
