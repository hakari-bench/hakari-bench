# MNanoBEIR / NanoBEIR-sr / NanoFiQA2018

## Overview

FiQA is a financial question-answer retrieval task. `NanoBEIR-sr__NanoFiQA2018`
uses Serbian translated finance questions to retrieve Serbian translated answer
passages.

## Details

### What the Original Data Measures

[FiQA](https://doi.org/10.1145/3184558.3192301) was introduced for financial
opinion and question answering data. BEIR turns it into answer-passage retrieval,
and MMTEB provides the multilingual evaluation context.

### Observed Data Profile

The sampled task has 50 queries, 4,598 documents, and 123 positive qrels. More
than half of queries have multiple positives, with an average of 2.46 and a
maximum of 15. Queries average 63.76 characters, while documents average 914.39
characters.

### BM25 Difficulty

BM25 reaches nDCG@10 = 0.1904 and hit@10 = 0.4000. The median first-positive
rank is 21.5, making this one of the harder Serbian translated NanoBEIR tasks
for lexical retrieval.

### Training Data That May Help

Helpful data includes non-overlapping financial QA, Serbian finance forum
retrieval, and answer ranking with multiple acceptable answers. Exclude FiQA,
BEIR, NanoBEIR, and translated evaluation answers.

### Synthetic Data Guidance

Generate Serbian personal-finance and investing questions from source-style
answer passages. Hard negatives should use the same financial product or tax
terms but answer a different decision problem.

## Example Data

| Query | Positive document |
| --- | --- |
| Koje vrste prinosa Vanguard navodi? (35 chars) | "Sa stranice Vanguard - Ovo se činilo najlakšim jer je S&P podatke lako pronaći. Koristim MoneyChimp da dobijem - što potvrđuje da Vanguardova stranica nudi CAGR, a ne aritmetički prosek. Napomena: Vanguard navodi 'Za prinose ... [truncated 225 chars](392 chars) |
| Poreske implikacije freelancinga (32 chars) | Ako imate prihode u SAD-u, dugovaćete porez na prihod SAD-u, osim ako postoji sporazum sa vašom zemljom koji kaže drugačije. (124 chars) |
| Šta se smatra visokim ili niskim kada je reč o jačini zvuka? (60 chars) | Dnevni volumen se obično upoređuje sa prosečnim dnevnim volumenom u poslednjih 50 dana za određenu akciju. Visok volumen se obično smatra kada je dva ili više puta veći od prosečnog dnevnog volumena te akcije u poslednjih 50 ... [truncated 225 chars](661 chars) |
| Korišćenje kreditnih kartica poena za plaćanje poreski odbitnih poslovnih troškova (82 chars) | Radi jednostavnosti, počnimo samo od keš bek-a. Generalno, keš bek sa kreditnih kartica za ličnu upotrebu nije oporeziv, ali za poslovnu upotrebu jeste (na neki način, objasniću kasnije). Razlog je što se većina ličnih kupovi ... [truncated 225 chars](3696 chars) |
| Kako da prijavim svoje poreze kao preduzetnik? (46 chars) | Za poreske svrhe, biće vam potrebno da se prijavite kao zaposleni (T4 obrasci i automatski zadržani porez), ali i kao preduzetnik. I sam sam imao istu situaciju prošle godine. "Zaposleni i samostalni radnik" je publikacija Po ... [truncated 225 chars](738 chars) |

## Dataset Information

| Field | Value |
| --- | --- |
| Nano set | MNanoBEIR |
| Backing dataset | NanoBEIR-sr |
| Task / split | NanoFiQA2018 |
| Hugging Face dataset | [hakari-bench/NanoBEIR-sr](https://huggingface.co/datasets/hakari-bench/NanoBEIR-sr) |
| Language | sr |
| Category | natural_language |
| Queries | 50 |
| Documents | 4,598 |
| Positive qrels | 123 |
| Positives per query avg | 2.46 |
| Positives per query min / median / max | 1 / 2.0 / 15 |
| Multi-positive queries | 28 (56.00%) |
| BM25 nDCG@10 | 0.1904 |
| BM25 hit@10 | 0.4000 |
| BM25 Recall@100 | 0.4959 |
| BM25 candidate subset | top-500 (`bm25`) |
| Dense nDCG@10 | 0.3094 |
| Dense hit@10 | 0.6200 |
| Dense Recall@100 | 0.6423 |
| Dense candidate subset | top-500 (`harrier_oss_v1_270m`) |
| Reranking hybrid nDCG@10 | 0.3183 |
| Reranking hybrid hit@10 | 0.6200 |
| Reranking hybrid Recall@100 | 0.6504 |
| Reranking hybrid candidate subset | top-100 plus optional rank-101 safeguard (`reranking_hybrid`) |
| Reranking hybrid candidates / query | 100-101 |
| Reranking hybrid safeguard rows | 10 |
| Query length avg chars | 63.76 |
| Document length avg chars | 914.39 |

### Public Sources

- [FiQA: Financial Opinion Mining and Question Answering](https://doi.org/10.1145/3184558.3192301).
- [BEIR: A Heterogeneous Benchmark for Zero-shot Evaluation of Information Retrieval Models](https://arxiv.org/abs/2104.08663).
- [MMTEB: Massive Multilingual Text Embedding Benchmark](https://arxiv.org/abs/2502.13595).
- [Zeta Alpha NanoBEIR collection](https://huggingface.co/collections/zeta-alpha-ai/nanobeir).

### Hugging Face Links

- Nano dataset: [hakari-bench/NanoBEIR-sr](https://huggingface.co/datasets/hakari-bench/NanoBEIR-sr)
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
  backing_dataset: NanoBEIR-sr
  dataset_id: hakari-bench/NanoBEIR-sr
  task_name: NanoFiQA2018
  split_name: NanoFiQA2018
  language: sr
  category: natural_language
  document_path: docs/benchmark_tasks/MNanoBEIR/NanoBEIR-sr__NanoFiQA2018.md
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
    query_mean: 63.76
    document_mean: 914.391475
  bm25:
    ndcg_at_10: 0.19044210242199758
    hit_at_10: 0.4
    source: dataset_candidate_subset
  candidate_subsets:
    bm25:
      config: bm25
      label: BM25
      source: dataset_candidate_subset
      top_k: 500
      ndcg_at_10: 0.1904421024
      hit_at_10: 0.4
      recall_at_100: 0.4959349593
      candidate_count_min: 500
      candidate_count_max: 500
      candidate_count_mean: 500.0
      query_count: 50
      query_coverage: 1.0
      relevant_coverage_at_100: 0.4959349593
    dense:
      config: harrier_oss_v1_270m
      label: Dense
      source: dataset_candidate_subset
      top_k: 500
      ndcg_at_10: 0.3093675016
      hit_at_10: 0.62
      recall_at_100: 0.6422764228
      candidate_count_min: 500
      candidate_count_max: 500
      candidate_count_mean: 500.0
      query_count: 50
      query_coverage: 1.0
      relevant_coverage_at_100: 0.6422764228
    reranking_hybrid:
      config: reranking_hybrid
      label: Reranking hybrid
      source: dataset_candidate_subset
      top_k: 100
      ndcg_at_10: 0.3182820515
      hit_at_10: 0.62
      recall_at_100: 0.6504065041
      candidate_count_min: 100
      candidate_count_max: 101
      candidate_count_mean: 100.2
      query_count: 50
      query_coverage: 1.0
      relevant_coverage_at_100: 0.6504065041
      safeguard_positive_rows: 10
      rows_with_101_candidates: 10
```
