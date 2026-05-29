# NanoMTEB-Polish / cqadupstack_android

## Overview

The Android split inherits CQADupStack's duplicate-question retrieval framing:
relevant documents are posts that ask the same Android problem, not arbitrary
answers about the same topic. In the Polish task, translated Android titles are
matched against longer translated candidate posts. The observed questions cover
calling workflows, home-button behavior, emulator speed, localization, and
hardware-button workarounds; many queries have multiple duplicate positives, so
the retriever must group equivalent device, OS, app, and developer issues even
when wording differs.

## Details

### What the Original Data Measures

[CQADupStack: A Benchmark Data Set for Community Question-Answering Research](https://ir.webis.de/anthology/2015.adcs_conference-2015.3/)
introduced CQADupStack as a benchmark for duplicate-question retrieval in
community QA. The [MTEB paper](https://arxiv.org/abs/2210.07316) includes
CQADupStack among retrieval datasets and notes that its domain-specific splits
cluster together. For this Polish task, the exact source is the MTEB/CLARIN
Polish Android dataset card rather than a separate Polish task paper.

### Observed Data Profile

The split has 200 queries, 10,000 documents, and 809 positive qrels. Queries
average 59.26 characters and documents average 626.68 characters. The examples
cover Android calling workflows, home-button behavior, emulator performance,
localization, and hardware-button workarounds. Many queries have multiple
duplicates, with 88 multi-positive queries and as many as 100 positives for one
query.

### BM25 Difficulty

Using the dataset-provided BM25 candidate column, BM25 reaches nDCG@10 =
0.3407 and hit@10 = 0.5100. It ranks 66 positives first and 102 positives in
the top 10. Lexical overlap helps when device or API names repeat, but the task
often requires recognizing paraphrased duplicate intent, such as "lock screen"
versus a broken power button or call-card dialing prefixes.

### Training Data That May Help

Useful training data includes non-overlapping Android support QA, Stack
Exchange duplicate-question pairs, Polish technical support questions, and
translated or native paraphrase pairs in the mobile-development domain. Upstream
test queries, qrels, and positive posts should be excluded from training because
memorizing duplicate clusters can directly inflate retrieval scores.

### Synthetic Data Guidance

Generate Polish Android support questions paired with realistic posts about
settings, apps, devices, permissions, and development tooling. Document-to-
question generation should use non-evaluation Android posts; joint generation
should create both a source-style post and several duplicate phrasings that
preserve the same technical problem while changing device names or symptoms.

## Example Data

| Query | Positive document |
| --- | --- |
| Dlaczego urządzenie z Androidem ROM jest specyficzne? (53 chars) | Dlaczego nie ma ogólnych instalatorów systemu operacyjnego telefonu? Jestem przyzwyczajony do instalowania i usuwania różnych systemów operacyjnych na moich komputerach, nawet mając kilka naraz. Zazwyczaj instalacja nowego sy ... [truncated 225 chars](1811 chars) |
| Jak mogę zapisać plik, zamiast go otwierać? (43 chars) | Jak pobrać plik audio ze strony internetowej? Czy istnieje sposób na pobranie pliku audio, takiego jak plik mp3 z przeglądarki systemu Android na urządzenie, aby móc go później słuchać, gdy będę offline? Czy jest sposób na za ... [truncated 225 chars](347 chars) |
| Jak przechwycić strumień wideo z ekranu telefonu z systemem Android i wyświetlić go na laptopie? (96 chars) | Jak wyświetlić ekran mojego telefonu z systemem Android do prezentacji? Jak wyświetlić ekran mojego Droid Incredible, aby móc zademonstrować smartfon w pokoju pełnym ludzi? Czy ktoś wie, jak mogę połączyć telefon z komputerem ... [truncated 225 chars](241 chars) |
| „Niezgodny z innymi aplikacjami korzystającymi z tego samego wspólnego identyfikatora użytkownika” podczas instalowania usługi Google Play? (139 chars) | „Niezgodny z innymi aplikacjami korzystającymi z tego samego wspólnego identyfikatora użytkownika” podczas instalowania usługi Google Play? Muszę uruchomić Google Plus, a Google Plus potrzebuje usługi Google Play. Za każdym r ... [truncated 225 chars](778 chars) |
| Jak mogę kontrolować zarówno głośność, jak i pomijanie utworów na moim urządzeniu z Androidem za pomocą słuchawek? (114 chars) | Sterowanie słuchawkami w SGS-III > **Możliwe powielenie:** > Jak mogę sterować zarówno głośnością, jak i pomijaniem utworów na moim urządzeniu z Androidem za pomocą > słuchawek? Więc niedawno dostałem SIII i porzuciłem iPhone ... [truncated 225 chars](674 chars) |

## Dataset Information

| Field | Value |
| --- | --- |
| Nano set | NanoMTEB-Polish |
| Backing dataset | NanoMTEB-Polish |
| Task / split | cqadupstack_android |
| Hugging Face dataset | [hakari-bench/NanoMTEB-Polish](https://huggingface.co/datasets/hakari-bench/NanoMTEB-Polish) |
| Source dataset | [mteb/CQADupstack-Android-PL](https://huggingface.co/datasets/mteb/CQADupstack-Android-PL) |
| Language | pl |
| Category | natural_language |
| Queries | 200 |
| Documents | 10,000 |
| Positive qrels | 809 |
| Avg positives / query | 4.045 |
| Positives per query (min / median / max) | 1 / 1.0 / 100 |
| Queries with multiple positives | 88 (44.0%) |
| BM25 nDCG@10 | 0.3379 |
| BM25 hit@10 | 0.5100 |
| BM25 Recall@100 | 0.4030 |
| BM25 candidate subset | top-500 (`bm25`) |
| Dense nDCG@10 | 0.4139 |
| Dense hit@10 | 0.6400 |
| Dense Recall@100 | 0.5006 |
| Dense candidate subset | top-500 (`harrier_oss_v1_270m`) |
| Reranking hybrid nDCG@10 | 0.4121 |
| Reranking hybrid hit@10 | 0.6250 |
| Reranking hybrid Recall@100 | 0.5105 |
| Reranking hybrid candidate subset | top-100 plus optional rank-101 safeguard (`reranking_hybrid`) |
| Reranking hybrid candidates / query | 100-101 |
| Reranking hybrid safeguard rows | 25 |
| Query length avg chars | 59.26 |
| Document length avg chars | 626.68 |

### Public Sources

- [CQADupStack: A Benchmark Data Set for Community Question-Answering Research](https://ir.webis.de/anthology/2015.adcs_conference-2015.3/), original benchmark paper record.
- [MTEB: Massive Text Embedding Benchmark](https://arxiv.org/abs/2210.07316), benchmark paper covering CQADupStack retrieval tasks.
- [CLARIN-KNEXT cqadupstack-android-pl](https://huggingface.co/datasets/clarin-knext/cqadupstack-android-pl), Polish source dataset card.

### Hugging Face Links

- Nano dataset: [hakari-bench/NanoMTEB-Polish](https://huggingface.co/datasets/hakari-bench/NanoMTEB-Polish)
- Source task dataset: [mteb/CQADupstack-Android-PL](https://huggingface.co/datasets/mteb/CQADupstack-Android-PL)

### Source Reference Table

| Title | Year | Type | URL |
| --- | ---: | --- | --- |
| CQADupStack: A Benchmark Data Set for Community Question-Answering Research | 2015 | task paper | https://ir.webis.de/anthology/2015.adcs_conference-2015.3/ |
| MTEB: Massive Text Embedding Benchmark | 2022 | benchmark paper | https://arxiv.org/abs/2210.07316 |
| CLARIN-KNEXT cqadupstack-android-pl |  | dataset card | https://huggingface.co/datasets/clarin-knext/cqadupstack-android-pl |

## Machine-Readable Metadata

<!-- benchmark-task-metadata:v1 -->

```yaml
benchmark_task_metadata:
  schema_version: 1
  document_status: first_pass
  nano_set: NanoMTEB-Polish
  backing_dataset: NanoMTEB-Polish
  dataset_id: hakari-bench/NanoMTEB-Polish
  task_name: cqadupstack_android
  split_name: cqadupstack_android
  language: pl
  category: natural_language
  document_path: docs/benchmark_tasks/NanoMTEB-Polish/cqadupstack_android.md
  source_research:
    primary_source_type: dataset_card
    paper_pdf_or_html_checked: true
    no_paper_note: no standalone paper for this Polish translated split was confirmed
  counts:
    queries: 200
    documents: 10000
    positive_qrels: 809
  positives_per_query:
    average: 4.045
    min: 1
    median: 1.0
    max: 100
    multi_positive_queries: 88
    multi_positive_query_percent: 44.0
  text_stats_chars:
    query_mean: 59.255
    document_mean: 626.6791
  bm25:
    ndcg_at_10: 0.3378736307871178
    hit_at_10: 0.51
    source: dataset_candidate_subset
  example_count: 5
  candidate_subsets:
    bm25:
      config: bm25
      label: BM25
      source: dataset_candidate_subset
      top_k: 500
      ndcg_at_10: 0.3378736308
      hit_at_10: 0.51
      recall_at_100: 0.4029666255
      candidate_count_min: 500
      candidate_count_max: 500
      candidate_count_mean: 500.0
      query_count: 200
      query_coverage: 1.0
      relevant_coverage_at_100: 0.4029666255
    dense:
      config: harrier_oss_v1_270m
      label: Dense
      source: dataset_candidate_subset
      top_k: 500
      ndcg_at_10: 0.4138900715
      hit_at_10: 0.64
      recall_at_100: 0.500618047
      candidate_count_min: 500
      candidate_count_max: 500
      candidate_count_mean: 500.0
      query_count: 200
      query_coverage: 1.0
      relevant_coverage_at_100: 0.500618047
    reranking_hybrid:
      config: reranking_hybrid
      label: Reranking hybrid
      source: dataset_candidate_subset
      top_k: 100
      ndcg_at_10: 0.4121211029
      hit_at_10: 0.625
      recall_at_100: 0.5105067985
      candidate_count_min: 100
      candidate_count_max: 101
      candidate_count_mean: 100.125
      query_count: 200
      query_coverage: 1.0
      relevant_coverage_at_100: 0.5105067985
      safeguard_positive_rows: 25
      rows_with_101_candidates: 25
```
