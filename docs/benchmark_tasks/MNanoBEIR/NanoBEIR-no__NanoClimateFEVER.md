# MNanoBEIR / NanoBEIR-no / NanoClimateFEVER

## Overview

CLIMATE-FEVER is a climate-science fact-checking retrieval task.
`NanoBEIR-no__NanoClimateFEVER` is the Norwegian MNanoBEIR version: Norwegian
translated climate claims must retrieve Norwegian translated evidence passages.

## Details

### What the Original Data Measures

[CLIMATE-FEVER](https://arxiv.org/abs/2012.00614) extends FEVER-style claim
verification to climate change claims and evidence. [BEIR](https://arxiv.org/abs/2104.08663)
uses it as a fact-checking retrieval task, and [MMTEB](https://arxiv.org/abs/2502.13595)
provides the multilingual embedding benchmark context for this Norwegian split.

### Observed Data Profile

The sampled Norwegian Nano task has 50 queries, 3,408 documents, and 148
positive qrel rows. Most queries have multiple positives: the average is 2.96,
with a range from 1 to 5. The average query length is 124.66 characters, and
the average document length is 1,524.22 characters.

The inspected examples include claims about brown bears in Alaska, polar ice
melt and methane release, sea-level variability, sea-ice decline, and wind-power
carbon footprints.

### BM25 Difficulty

Using the dataset-provided BM25 candidate column, BM25 reaches nDCG@10 =
0.2099 and hit@10 = 0.5000. BM25 ranks a positive first for 11 queries, and the
median first-positive rank is 11.5. This is a relatively difficult lexical
setting despite repeated climate terminology.

### Training Data That May Help

Useful training data includes non-overlapping climate claim-evidence pairs,
scientific fact-checking retrieval data, and Norwegian or multilingual climate
science QA. Training should exclude CLIMATE-FEVER, BEIR, NanoBEIR, and
translated evidence likely to overlap with the evaluation records.

### Synthetic Data Guidance

Generate Norwegian climate claims from non-evaluation evidence passages and
pair them with evidence-bearing documents. Hard negatives should share climate
terms but fail to support or refute the exact claim.

## Example Data

| Query | Positive document |
| --- | --- |
| Fra 1970 til 1998 var det en oppvarmingsperiode som økte temperaturen med omtrent 0,7 grader Fahrenheit, noe som bidro til å skape bevegelsen for klimaendringer. (161 chars) | Paleocen (uttales pronˈpæliəˌsiːn, _ ˈpæ - , _ - lioʊ - ) eller Paleocen, «den gamle nylige», er en geologisk epoke som varte fra omtrent 66 til 56 millioner år siden. Det er den første epoken i Paleogen-perioden i den modern ... [truncated 225 chars](1051 chars) |
| Faktisk går trenden nedover, selv om den ikke er signifikant. (61 chars) | Solens syklus eller solmagnetisk aktivitetssyklus er en omtrent 11-årige syklus i solens aktivitet (inkludert endringer i nivåene av solstråling og utkast av solmateriale) og utseende (endringer i antall og størrelse på solfl ... [truncated 225 chars](573 chars) |
| Lokale og regionale havnivåer fortsetter å vise den vanlige naturlige variasjonen, stiger på noen steder og synker på andre. (124 chars) | Middelhøyde over havet (MSL) (forkortet bare havnivå) er et gjennomsnittsnivå av overflaten på ett eller flere av Jordens hav, hvorfra høyder som høyder kan måles. MSL er en type vertikal datumsstandardisert geodetisk referan ... [truncated 225 chars](899 chars) |
| Klimatologer sier at aspekter ved orkanen Harvey tyder på at global oppvarming gjør en dårlig situasjon enda verre. (115 chars) | De globale oppvarmingsvirkningene er de miljømessige og sosiale endringene som skyldes (direkte eller indirekte) menneskets utslipp av drivhusgasser. Det er en vitenskapelig konsensus om at klimaendringer skjer, og at mennesk ... [truncated 225 chars](1295 chars) |
| CERN CLOUD-eksperimentet testet bare en tredjedel av ett av fire krav som er nødvendige for å skylde global oppvarming på kosmiske stråler, og to av de andre kravene har allerede sviktet. (187 chars) | Attribuering av nylig klimaendring handler om å vitenskapelig fastslå mekanismene som er ansvarlige for de nylige klimaendringene på Jorden, vanligvis kjent som `global oppvarming`. Arbeidet har fokusert på endringer som er o ... [truncated 225 chars](1979 chars) |

## Dataset Information

| Field | Value |
| --- | --- |
| Nano set | MNanoBEIR |
| Backing dataset | NanoBEIR-no |
| Task / split | NanoClimateFEVER |
| Hugging Face dataset | [hakari-bench/NanoBEIR-no](https://huggingface.co/datasets/hakari-bench/NanoBEIR-no) |
| Language | no |
| Category | natural_language |
| Queries | 50 |
| Documents | 3,408 |
| Positive qrels | 148 |
| Avg positives / query | 2.96 |
| Positives per query (min / median / max) | 1 / 3.00 / 5 |
| Queries with multiple positives | 44 (88.0%) |
| BM25 nDCG@10 | 0.2099 |
| BM25 hit@10 | 0.5000 |
| BM25 Recall@100 | 0.4730 |
| BM25 candidate subset | top-500 (`bm25`) |
| Dense nDCG@10 | 0.3053 |
| Dense hit@10 | 0.6600 |
| Dense Recall@100 | 0.5811 |
| Dense candidate subset | top-500 (`harrier_oss_v1_270m`) |
| Reranking hybrid nDCG@10 | 0.2862 |
| Reranking hybrid hit@10 | 0.6600 |
| Reranking hybrid Recall@100 | 0.6081 |
| Reranking hybrid candidate subset | top-100 plus optional rank-101 safeguard (`reranking_hybrid`) |
| Reranking hybrid candidates / query | 100-101 |
| Reranking hybrid safeguard rows | 3 |
| Query length avg chars | 124.66 |
| Document length avg chars | 1,524.22 |

### Public Sources

- [CLIMATE-FEVER](https://arxiv.org/abs/2012.00614).
- [BEIR: A Heterogeneous Benchmark for Zero-shot Evaluation of Information Retrieval Models](https://arxiv.org/abs/2104.08663).
- [MMTEB: Massive Multilingual Text Embedding Benchmark](https://arxiv.org/abs/2502.13595).
- [Zeta Alpha NanoBEIR collection](https://huggingface.co/collections/zeta-alpha-ai/nanobeir).

### Hugging Face Links

- Nano dataset: [hakari-bench/NanoBEIR-no](https://huggingface.co/datasets/hakari-bench/NanoBEIR-no)
- Source collection: [Zeta Alpha NanoBEIR collection](https://huggingface.co/collections/zeta-alpha-ai/nanobeir)

### Source Reference Table

| Title | Year | Type | URL |
| --- | ---: | --- | --- |
| CLIMATE-FEVER | 2020 | task paper | https://arxiv.org/abs/2012.00614 |
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
  task_name: NanoClimateFEVER
  split_name: NanoClimateFEVER
  language: 'no'
  category: natural_language
  document_path: docs/benchmark_tasks/MNanoBEIR/NanoBEIR-no__NanoClimateFEVER.md
  source_research:
    primary_source_type: task_paper
    paper_pdf_or_html_checked: true
    no_paper_note: null
  counts:
    queries: 50
    documents: 3408
    positive_qrels: 148
  positives_per_query:
    average: 2.96
    min: 1
    median: 3.0
    max: 5
    multi_positive_queries: 44
    multi_positive_query_percent: 88.0
  text_stats_chars:
    query_mean: 124.66
    document_mean: 1524.216843
  bm25:
    ndcg_at_10: 0.2098556167376287
    hit_at_10: 0.5
    source: dataset_candidate_subset
  candidate_subsets:
    bm25:
      config: bm25
      label: BM25
      source: dataset_candidate_subset
      top_k: 500
      ndcg_at_10: 0.2098556167
      hit_at_10: 0.5
      recall_at_100: 0.472972973
      candidate_count_min: 500
      candidate_count_max: 500
      candidate_count_mean: 500.0
      query_count: 50
      query_coverage: 1.0
      relevant_coverage_at_100: 0.472972973
    dense:
      config: harrier_oss_v1_270m
      label: Dense
      source: dataset_candidate_subset
      top_k: 500
      ndcg_at_10: 0.3053175042
      hit_at_10: 0.66
      recall_at_100: 0.5810810811
      candidate_count_min: 500
      candidate_count_max: 500
      candidate_count_mean: 500.0
      query_count: 50
      query_coverage: 1.0
      relevant_coverage_at_100: 0.5810810811
    reranking_hybrid:
      config: reranking_hybrid
      label: Reranking hybrid
      source: dataset_candidate_subset
      top_k: 100
      ndcg_at_10: 0.2862211495
      hit_at_10: 0.66
      recall_at_100: 0.6081081081
      candidate_count_min: 100
      candidate_count_max: 101
      candidate_count_mean: 100.06
      query_count: 50
      query_coverage: 1.0
      relevant_coverage_at_100: 0.6081081081
      safeguard_positive_rows: 3
      rows_with_101_candidates: 3
```
