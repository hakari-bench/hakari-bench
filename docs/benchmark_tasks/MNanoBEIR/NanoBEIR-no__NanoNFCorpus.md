# MNanoBEIR / NanoBEIR-no / NanoNFCorpus

## Overview

NFCorpus is a biomedical and nutrition-focused retrieval benchmark.
`NanoBEIR-no__NanoNFCorpus` uses Norwegian translated health queries to retrieve
Norwegian translated biomedical documents.

## Details

### What the Original Data Measures

[NFCorpus](https://www.cl.uni-heidelberg.de/~riezler/publications/papers/ECIR2016.pdf)
was built for medical information retrieval over nutrition and health claims.
[BEIR](https://arxiv.org/abs/2104.08663) includes it as a biomedical retrieval
task, and [MMTEB](https://arxiv.org/abs/2502.13595) provides the multilingual
benchmark context.

### Observed Data Profile

The sampled Norwegian Nano task has 50 queries, 2,953 documents, and 1,651
positive qrels. It is highly multi-positive, averaging 33.02 positives per
query. Queries are short health phrases averaging 24.16 characters; documents
are biomedical abstracts averaging 1,494.75 characters.

### BM25 Difficulty

BM25 reaches nDCG@10 = 0.3256 and hit@10 = 0.6600. Short queries and long
technical abstracts make the task sensitive to domain vocabulary and synonymy,
although exact biomedical terms can give BM25 useful anchors.

### Training Data That May Help

Useful training data includes non-overlapping biomedical IR, nutrition QA,
clinical abstract retrieval, and Norwegian or multilingual health retrieval.
Training should exclude NFCorpus, BEIR, NanoBEIR, and overlapping medical
abstracts.

### Synthetic Data Guidance

Generate Norwegian health search phrases from non-evaluation biomedical
abstracts. Include short layperson queries and technical queries, with hard
negatives that share symptoms, foods, or organisms but address a different
finding.

## Example Data

| Query | Positive document |
| --- | --- |
| Sunn sjokolademelk (18 chars) | Mål: Å undersøke forholdet mellom inntak av kirsebær og risikoen for gjentatte giktangrep hos individer med gikt. Metoder: Vi gjennomførte en case-crossover-studie for å undersøke sammenhenger mellom en rekke påståtte risikof ... [truncated 225 chars](1617 chars) |
| Medisinsk etikk (15 chars) | BAKGRUNN: En av de største utfordringene ved å kontrollere serumkolesterol gjennom diettintervensjoner ser ut til å være behovet for å forbedre pasientens overholdelse. MÅL: For å utforske de mange spørsmålene om hindringer o ... [truncated 225 chars](1855 chars) |
| bikubear (8 chars) | De siste 20 årene har økt interesse for L-arginins biokjemi, ernæring og farmakologi ført til omfattende studier for å utforske dets ernæringsmessige og terapeutiske roller i behandling og forebygging av menneskelige metabols ... [truncated 225 chars](1210 chars) |
| Hva er egentlig i kyllingnuggets? (33 chars) | PURPOSE: Å fastslå innholdet i kyllingnuggets fra to nasjonale matkjeder. BACKGROUND: Kyllingnuggets har blitt en viktig del av den amerikanske dietten. Vi ønsket å fastslå den nåværende sammensetningen av denne sterkt bearbe ... [truncated 225 chars](716 chars) |
| mettet fett (11 chars) | Interessen for muligheten av at mors kosthold under graviditet kan påvirke utviklingen av allergiske lidelser hos barn har økt. Denne prospektive studien undersøkte sammenhengen mellom mors inntak av utvalgte matvarer rike på ... [truncated 225 chars](1897 chars) |

## Dataset Information

| Field | Value |
| --- | --- |
| Nano set | MNanoBEIR |
| Backing dataset | NanoBEIR-no |
| Task / split | NanoNFCorpus |
| Hugging Face dataset | [hakari-bench/NanoBEIR-no](https://huggingface.co/datasets/hakari-bench/NanoBEIR-no) |
| Language | no |
| Category | natural_language |
| Queries | 50 |
| Documents | 2,953 |
| Positive qrels | 1,651 |
| Avg positives / query | 33.02 |
| Positives per query (min / median / max) | 1 / 23.50 / 100 |
| Queries with multiple positives | 47 (94.0%) |
| BM25 nDCG@10 | 0.2618 |
| BM25 hit@10 | 0.6400 |
| BM25 Recall@100 | 0.1187 |
| BM25 candidate subset | top-500 (`bm25`) |
| Dense nDCG@10 | 0.2334 |
| Dense hit@10 | 0.5800 |
| Dense Recall@100 | 0.1878 |
| Dense candidate subset | top-500 (`harrier_oss_v1_270m`) |
| Reranking hybrid nDCG@10 | 0.2722 |
| Reranking hybrid hit@10 | 0.6800 |
| Reranking hybrid Recall@100 | 0.1841 |
| Reranking hybrid candidate subset | top-100 plus optional rank-101 safeguard (`reranking_hybrid`) |
| Reranking hybrid candidates / query | 100-101 |
| Reranking hybrid safeguard rows | 6 |
| Query length avg chars | 24.16 |
| Document length avg chars | 1,494.75 |

### Public Sources

- [NFCorpus: A Full-Text Learning to Rank Dataset for Medical Information Retrieval](https://www.cl.uni-heidelberg.de/~riezler/publications/papers/ECIR2016.pdf).
- [BEIR: A Heterogeneous Benchmark for Zero-shot Evaluation of Information Retrieval Models](https://arxiv.org/abs/2104.08663).
- [MMTEB: Massive Multilingual Text Embedding Benchmark](https://arxiv.org/abs/2502.13595).
- [Zeta Alpha NanoBEIR collection](https://huggingface.co/collections/zeta-alpha-ai/nanobeir).

### Hugging Face Links

- Nano dataset: [hakari-bench/NanoBEIR-no](https://huggingface.co/datasets/hakari-bench/NanoBEIR-no)
- Source collection: [Zeta Alpha NanoBEIR collection](https://huggingface.co/collections/zeta-alpha-ai/nanobeir)

### Source Reference Table

| Title | Year | Type | URL |
| --- | ---: | --- | --- |
| NFCorpus: A Full-Text Learning to Rank Dataset for Medical Information Retrieval | 2016 | task paper | https://www.cl.uni-heidelberg.de/~riezler/publications/papers/ECIR2016.pdf |
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
  backing_dataset: NanoBEIR-no
  dataset_id: hakari-bench/NanoBEIR-no
  task_name: NanoNFCorpus
  split_name: NanoNFCorpus
  language: 'no'
  category: natural_language
  document_path: docs/benchmark_tasks/MNanoBEIR/NanoBEIR-no__NanoNFCorpus.md
  source_research:
    primary_source_type: task_paper
    paper_pdf_or_html_checked: true
    no_paper_note: null
  counts:
    queries: 50
    documents: 2953
    positive_qrels: 1651
  positives_per_query:
    average: 33.02
    min: 1
    median: 23.5
    max: 100
    multi_positive_queries: 47
    multi_positive_query_percent: 94.0
  text_stats_chars:
    query_mean: 24.16
    document_mean: 1494.748053
  bm25:
    ndcg_at_10: 0.2617713792315164
    hit_at_10: 0.64
    source: dataset_candidate_subset
  candidate_subsets:
    bm25:
      config: bm25
      label: BM25
      source: dataset_candidate_subset
      top_k: 500
      ndcg_at_10: 0.2617713792
      hit_at_10: 0.64
      recall_at_100: 0.1187159297
      candidate_count_min: 500
      candidate_count_max: 500
      candidate_count_mean: 500.0
      query_count: 50
      query_coverage: 1.0
      relevant_coverage_at_100: 0.1187159297
    dense:
      config: harrier_oss_v1_270m
      label: Dense
      source: dataset_candidate_subset
      top_k: 500
      ndcg_at_10: 0.2333593401
      hit_at_10: 0.58
      recall_at_100: 0.1877649909
      candidate_count_min: 500
      candidate_count_max: 500
      candidate_count_mean: 500.0
      query_count: 50
      query_coverage: 1.0
      relevant_coverage_at_100: 0.1877649909
    reranking_hybrid:
      config: reranking_hybrid
      label: Reranking hybrid
      source: dataset_candidate_subset
      top_k: 100
      ndcg_at_10: 0.2722359413
      hit_at_10: 0.68
      recall_at_100: 0.1841308298
      candidate_count_min: 100
      candidate_count_max: 101
      candidate_count_mean: 100.12
      query_count: 50
      query_coverage: 1.0
      relevant_coverage_at_100: 0.1841308298
      safeguard_positive_rows: 6
      rows_with_101_candidates: 6
```
