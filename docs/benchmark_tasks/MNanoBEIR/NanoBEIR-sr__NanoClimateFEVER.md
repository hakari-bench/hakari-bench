# MNanoBEIR / NanoBEIR-sr / NanoClimateFEVER

## Overview

Climate-FEVER is an evidence retrieval task for climate-related claims.
`NanoBEIR-sr__NanoClimateFEVER` uses Serbian translated claims to retrieve
Serbian translated evidence passages.

## Details

### What the Original Data Measures

[CLIMATE-FEVER](https://arxiv.org/abs/2012.00614) extends fact-checking to
real-world climate claims and evidence documents. BEIR includes the task as
claim-evidence retrieval, while MMTEB gives the multilingual context for this
Serbian version.

### Observed Data Profile

The sampled task has 50 queries, 3,408 documents, and 148 positive qrels. Most
queries have multiple positives, averaging 2.96 positives and reaching 5.
Queries average 135.24 characters, and documents average 1,552.34 characters.

### BM25 Difficulty

BM25 reaches nDCG@10 = 0.2389 and hit@10 = 0.6400. The median first-positive
rank is 5.0, so lexical matching often finds some evidence, but complete ranking
of the relevant evidence set remains hard.

### Training Data That May Help

Helpful data includes non-overlapping climate claim verification, Serbian
scientific and policy evidence retrieval, and multilingual fact-checking data.
Training should exclude CLIMATE-FEVER, BEIR, NanoBEIR, and overlapping
translations.

### Synthetic Data Guidance

Generate Serbian climate or environmental claims from non-evaluation source
passages. Include multiple evidence passages when the source claim supports that
structure, and use hard negatives with shared climate terms but no verifying
evidence.

## Example Data

| Query | Positive document |
| --- | --- |
| Od 1970. do 1998. godine postojao je period zagrevanja koji je podigao temperature za oko 0,7 stepeni Farenhajta, što je pomoglo da se pokrene pokret alarmista za globalno zagrevanje. (183 chars) | Paleocen (izgovor: /ˈpæliəˌsiːn/, /ˈpæ-/, /-lioʊ-/) ili Paleocen, što znači "stari novi", je geološka epoha koja je trajala od oko 66 do 56 miliona godina. To je prva epoka paleogenog perioda u savremenoj kenozojskoj eri. Kao ... [truncated 225 chars](1072 chars) |
| Zapravo, trend je, iako nije statistički značajan, opadajući. (61 chars) | Solarni ciklus ili ciklus solarne magnetne aktivnosti predstavlja gotovo periodičnu 11-godišnju promenu u aktivnosti Sunca (uključujući promene u nivou solarne radijacije i izbacivanju sunčevog materijala) i izgledu (promene ... [truncated 225 chars](574 chars) |
| Lokalni i regionalni nivoi mora i dalje pokazuju tipičnu prirodnu varijabilnost — na nekim mestima se podižu, a na drugim spuštaju. (131 chars) | Srednji nivo mora (MSL) (skraćeno samo kao nivo mora) je prosečan nivo površine jednog ili više Zemljinih okeana od koga se mogu meriti visine kao što su nadmorske visine. MSL je vrsta vertikalne datume – standardizovane geod ... [truncated 225 chars](991 chars) |
| [Klimatolozi] kažu da pojedini aspekti slučaja uragana Harvey ukazuju da globalno zagrevanje pogoršava već lošu situaciju. (122 chars) | Posledice globalnog zagrevanja su ekološke i društvene promene uzrokovane (direktno ili indirektno) ljudskim emisijama gasova staklene bašte. Postoji naučni konsenzus da se klimatske promene dešavaju i da su ljudske aktivnost ... [truncated 225 chars](1310 chars) |
| Eksperiment CERN CLOUD testirao je samo jednu trećinu jednog od četiri uslova potrebnih da se globalno zagrevanje okrivi na kosmičke zrake, a druga dva uslova su već propala. (174 chars) | Pripisivanje nedavnih klimatskih promena predstavlja naučni pokušaj da se utvrde mehanizmi odgovorni za nedavne klimatske promene na Zemlji, poznate kao 'globalno zagrevanje'. Ovaj napor se fokusira na promene uočene tokom pe ... [truncated 225 chars](1922 chars) |

## Dataset Information

| Field | Value |
| --- | --- |
| Nano set | MNanoBEIR |
| Backing dataset | NanoBEIR-sr |
| Task / split | NanoClimateFEVER |
| Hugging Face dataset | [hakari-bench/NanoBEIR-sr](https://huggingface.co/datasets/hakari-bench/NanoBEIR-sr) |
| Language | sr |
| Category | natural_language |
| Queries | 50 |
| Documents | 3,408 |
| Positive qrels | 148 |
| Positives per query avg | 2.96 |
| Positives per query min / median / max | 1 / 3.0 / 5 |
| Multi-positive queries | 44 (88.00%) |
| BM25 nDCG@10 | 0.2389 |
| BM25 hit@10 | 0.6400 |
| BM25 Recall@100 | 0.5473 |
| BM25 candidate subset | top-500 (`bm25`) |
| Dense nDCG@10 | 0.2946 |
| Dense hit@10 | 0.6800 |
| Dense Recall@100 | 0.5473 |
| Dense candidate subset | top-500 (`harrier_oss_v1_270m`) |
| Reranking hybrid nDCG@10 | 0.3266 |
| Reranking hybrid hit@10 | 0.7400 |
| Reranking hybrid Recall@100 | 0.6149 |
| Reranking hybrid candidate subset | top-100 plus optional rank-101 safeguard (`reranking_hybrid`) |
| Reranking hybrid candidates / query | 100-101 |
| Reranking hybrid safeguard rows | 2 |
| Query length avg chars | 135.24 |
| Document length avg chars | 1,552.34 |

### Public Sources

- [CLIMATE-FEVER: A Dataset for Verification of Real-World Climate Claims](https://arxiv.org/abs/2012.00614).
- [BEIR: A Heterogeneous Benchmark for Zero-shot Evaluation of Information Retrieval Models](https://arxiv.org/abs/2104.08663).
- [MMTEB: Massive Multilingual Text Embedding Benchmark](https://arxiv.org/abs/2502.13595).
- [Zeta Alpha NanoBEIR collection](https://huggingface.co/collections/zeta-alpha-ai/nanobeir).

### Hugging Face Links

- Nano dataset: [hakari-bench/NanoBEIR-sr](https://huggingface.co/datasets/hakari-bench/NanoBEIR-sr)
- Source collection: [Zeta Alpha NanoBEIR collection](https://huggingface.co/collections/zeta-alpha-ai/nanobeir)

### Source Reference Table

| Title | Year | Type | URL |
| --- | ---: | --- | --- |
| CLIMATE-FEVER: A Dataset for Verification of Real-World Climate Claims | 2020 | task paper | https://arxiv.org/abs/2012.00614 |
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
  task_name: NanoClimateFEVER
  split_name: NanoClimateFEVER
  language: sr
  category: natural_language
  document_path: docs/benchmark_tasks/MNanoBEIR/NanoBEIR-sr__NanoClimateFEVER.md
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
    query_mean: 135.24
    document_mean: 1552.335681
  bm25:
    ndcg_at_10: 0.23886423275211982
    hit_at_10: 0.64
    source: dataset_candidate_subset
  candidate_subsets:
    bm25:
      config: bm25
      label: BM25
      source: dataset_candidate_subset
      top_k: 500
      ndcg_at_10: 0.2388642328
      hit_at_10: 0.64
      recall_at_100: 0.5472972973
      candidate_count_min: 500
      candidate_count_max: 500
      candidate_count_mean: 500.0
      query_count: 50
      query_coverage: 1.0
      relevant_coverage_at_100: 0.5472972973
    dense:
      config: harrier_oss_v1_270m
      label: Dense
      source: dataset_candidate_subset
      top_k: 500
      ndcg_at_10: 0.2945707372
      hit_at_10: 0.68
      recall_at_100: 0.5472972973
      candidate_count_min: 500
      candidate_count_max: 500
      candidate_count_mean: 500.0
      query_count: 50
      query_coverage: 1.0
      relevant_coverage_at_100: 0.5472972973
    reranking_hybrid:
      config: reranking_hybrid
      label: Reranking hybrid
      source: dataset_candidate_subset
      top_k: 100
      ndcg_at_10: 0.3266108085
      hit_at_10: 0.74
      recall_at_100: 0.6148648649
      candidate_count_min: 100
      candidate_count_max: 101
      candidate_count_mean: 100.04
      query_count: 50
      query_coverage: 1.0
      relevant_coverage_at_100: 0.6148648649
      safeguard_positive_rows: 2
      rows_with_101_candidates: 2
```
