# MNanoBEIR / NanoBEIR-no / NanoHotpotQA

## Overview

HotpotQA is a multi-hop question answering benchmark. `NanoBEIR-no__NanoHotpotQA`
uses Norwegian translated questions to retrieve Norwegian translated Wikipedia
paragraphs containing supporting evidence.

## Details

### What the Original Data Measures

[HotpotQA](https://arxiv.org/abs/1809.09600) was designed for explainable
multi-hop question answering with supporting facts. BEIR treats it as evidence
retrieval, and MMTEB provides the multilingual context for this Norwegian split.

### Observed Data Profile

The sampled task has 50 queries, 5,090 documents, and 100 positive qrels. Every
query has exactly two positives. Queries average 87.30 characters; documents are
short Wikipedia paragraphs averaging 341.70 characters.

### BM25 Difficulty

BM25 reaches nDCG@10 = 0.7728 and hit@10 = 0.9600. Named entities help, but the
multi-hop structure requires finding both supporting pieces rather than only the
most obvious page.

### Training Data That May Help

Useful training data includes non-overlapping multi-hop QA retrieval pairs,
Wikipedia evidence selection data, and Norwegian or multilingual question-to-
passage retrieval. Exclude HotpotQA, BEIR, NanoBEIR, and overlapping translated
support paragraphs.

### Synthetic Data Guidance

Generate Norwegian multi-hop questions from pairs of non-evaluation passages.
Each generated query should require a bridge entity or comparison, with hard
negatives from one-hop partial matches.

## Example Data

| Query | Positive document |
| --- | --- |
| Hvilken annen skuespiller medvirket Penny Rae Bridges i en TV-sitcom sammen med? (80 chars) | Penny Rae Bridges (født 29. juli 1990) er en amerikansk skuespiller. Hun har spilt i "For Your Love", "Family Law", "Boy Meets World" og "The Parent 'Hood". Hun er mest kjent for sin rolle i "Half & Half", som den unge Mona. (224 chars) |
| Hvem ga Kaganoi Shigemochi et sverd laget av personen som grunnla Muramasa-skolen? (82 chars) | Kaganoi Shigemochi (加賀井 重望, 1561 – 27. august 1600) var en japansk samurai fra Azuchi-Momoyama-perioden som tjenestegjorde for Oda-klanen. Han styrte Kaganoi-slottet. Under slaget ved Komaki og Nagakute kjempet Shigemochi und ... [truncated 225 chars](554 chars) |
| Hvilken film er skrevet og regissert av Joby Harold med musikk av Samuel Sim? (77 chars) | Samuel Sim er en komponist for film og fjernsyn. Han fikk først anerkjennelse for sin prisbelønte musikk til BBC-dramaserien "Dunkirk". Siden da har han skrevet musikk til en bred vifte av film- og fjernsynsproduksjoner, mest ... [truncated 225 chars](468 chars) |
| Hvilken dato ble denne college football-kampen spilt på Sun Life Stadium i Miami Gardens, Florida, der Clemson slo nr. 4 Oklahoma Sooners, 37-17? (145 chars) | Clemson Tigers fotballaget representerte Clemson University i 2015-sesongen i NCAA Division I FBS. Tigers ble ledet av hovedtrener Dabo Swinney i hans syvende fulle år og åttende år totalt siden han overtok midtveis i 2008-se ... [truncated 225 chars](963 chars) |
| Hva er Devil's Food? Det er en samling med singler av en amerikansk rock and roll-band som også har vært kjent for å spille country-konserter under hvilket navn? (161 chars) | Devil's Food er en samleplate med singler av det amerikanske rock & roll-bandet Supersuckers, utgitt i april 2005 på Mid-Fi Records. (132 chars) |

## Dataset Information

| Field | Value |
| --- | --- |
| Nano set | MNanoBEIR |
| Backing dataset | NanoBEIR-no |
| Task / split | NanoHotpotQA |
| Hugging Face dataset | [hakari-bench/NanoBEIR-no](https://huggingface.co/datasets/hakari-bench/NanoBEIR-no) |
| Language | no |
| Category | natural_language |
| Queries | 50 |
| Documents | 5,090 |
| Positive qrels | 100 |
| Avg positives / query | 2.00 |
| Positives per query (min / median / max) | 2 / 2.00 / 2 |
| Queries with multiple positives | 50 (100.0%) |
| BM25 nDCG@10 | 0.7728 |
| BM25 hit@10 | 0.9600 |
| BM25 Recall@100 | 0.9400 |
| BM25 candidate subset | top-500 (`bm25`) |
| Dense nDCG@10 | 0.7574 |
| Dense hit@10 | 0.9800 |
| Dense Recall@100 | 0.9400 |
| Dense candidate subset | top-500 (`harrier_oss_v1_270m`) |
| Reranking hybrid nDCG@10 | 0.8168 |
| Reranking hybrid hit@10 | 1.0000 |
| Reranking hybrid Recall@100 | 0.9600 |
| Reranking hybrid candidate subset | top-100 plus optional rank-101 safeguard (`reranking_hybrid`) |
| Reranking hybrid candidates / query | 100 |
| Reranking hybrid safeguard rows | 0 |
| Query length avg chars | 87.30 |
| Document length avg chars | 341.70 |

### Public Sources

- [HotpotQA: A Dataset for Diverse, Explainable Multi-hop Question Answering](https://arxiv.org/abs/1809.09600).
- [BEIR: A Heterogeneous Benchmark for Zero-shot Evaluation of Information Retrieval Models](https://arxiv.org/abs/2104.08663).
- [MMTEB: Massive Multilingual Text Embedding Benchmark](https://arxiv.org/abs/2502.13595).
- [Zeta Alpha NanoBEIR collection](https://huggingface.co/collections/zeta-alpha-ai/nanobeir).

### Hugging Face Links

- Nano dataset: [hakari-bench/NanoBEIR-no](https://huggingface.co/datasets/hakari-bench/NanoBEIR-no)
- Source collection: [Zeta Alpha NanoBEIR collection](https://huggingface.co/collections/zeta-alpha-ai/nanobeir)

### Source Reference Table

| Title | Year | Type | URL |
| --- | ---: | --- | --- |
| HotpotQA: A Dataset for Diverse, Explainable Multi-hop Question Answering | 2018 | task paper | https://arxiv.org/abs/1809.09600 |
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
  task_name: NanoHotpotQA
  split_name: NanoHotpotQA
  language: 'no'
  category: natural_language
  document_path: docs/benchmark_tasks/MNanoBEIR/NanoBEIR-no__NanoHotpotQA.md
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
    query_mean: 87.3
    document_mean: 341.697839
  bm25:
    ndcg_at_10: 0.7728269575941725
    hit_at_10: 0.96
    source: dataset_candidate_subset
  candidate_subsets:
    bm25:
      config: bm25
      label: BM25
      source: dataset_candidate_subset
      top_k: 500
      ndcg_at_10: 0.7728269576
      hit_at_10: 0.96
      recall_at_100: 0.94
      candidate_count_min: 500
      candidate_count_max: 500
      candidate_count_mean: 500.0
      query_count: 50
      query_coverage: 1.0
      relevant_coverage_at_100: 0.94
    dense:
      config: harrier_oss_v1_270m
      label: Dense
      source: dataset_candidate_subset
      top_k: 500
      ndcg_at_10: 0.7573867437
      hit_at_10: 0.98
      recall_at_100: 0.94
      candidate_count_min: 500
      candidate_count_max: 500
      candidate_count_mean: 500.0
      query_count: 50
      query_coverage: 1.0
      relevant_coverage_at_100: 0.94
    reranking_hybrid:
      config: reranking_hybrid
      label: Reranking hybrid
      source: dataset_candidate_subset
      top_k: 100
      ndcg_at_10: 0.8167541335
      hit_at_10: 1.0
      recall_at_100: 0.96
      candidate_count_min: 100
      candidate_count_max: 100
      candidate_count_mean: 100.0
      query_count: 50
      query_coverage: 1.0
      relevant_coverage_at_100: 0.96
      safeguard_positive_rows: 0
      rows_with_101_candidates: 0
```
