# NanoMTEB-Polish / fiqa

## Overview

FiQA 2018 defines an opinion-oriented financial question-answering retrieval
task in which systems rank relevant documents for natural-language finance
questions. This Polish split is the translated/localized retrieval version:
short personal-finance or investing questions retrieve answer-style discussion
passages. The observed positives cover contractor incorporation, option
assignment, put-call parity, house-price affordability, and mortgage-adviser
incentives, so relevance often depends on explanatory financial reasoning and
opinion context rather than a single factual answer.

## Details

### What the Original Data Measures

The [FiQA 2018 challenge site](https://sites.google.com/view/fiqa/) describes
Task 2 as opinion-based question answering over financial data, where systems
rank relevant documents for natural-language questions and are evaluated with
top-10 IR metrics. The [WWW'18 Open Challenge paper record](https://research.universityofgalway.ie/en/publications/www18-open-challenge-financial-opinion-mining-and-question-answer/)
frames the challenge around financial opinion mining and question answering.
This Polish split is the MTEB `FiQA-PL` retrieval task rather than a separate
Polish source paper.

### Observed Data Profile

The split has 200 queries, 10,000 documents, and 534 positive qrels. Queries
average 68.51 characters and documents average 808.82 characters. The examples
include contractor incorporation, option assignment, put-call parity,
house-price affordability, and mortgage-adviser incentives. Multi-positive
judgments are frequent: 128 queries have more than one positive, with a median
of 2 positives per query.

### BM25 Difficulty

BM25 reaches nDCG@10 = 0.2353 and hit@10 = 0.4550, with 47 positives at rank 1
and 91 in the top 10. Lexical matching catches specific instruments or terms,
but finance answers are long and explanatory, and the relevant passage may use a
different framing from the question.

### Training Data That May Help

Useful data includes non-overlapping FiQA training data, financial QA pairs,
personal-finance forum answers, and Polish finance-domain retrieval pairs.
Because the task is multi-positive and opinion/explanation oriented, pairwise or
listwise supervision with hard negatives is preferable to treating each query as
single-answer fact lookup. Avoid upstream test queries, qrels, and positive
answers.

### Synthetic Data Guidance

Generate Polish financial questions and answer passages about taxes, loans,
investments, employment status, derivatives, and household finance. Synthetic
answers should contain explicit reasoning, caveats, and financial entities. Do
not seed generation from evaluation queries or positive passages.

## Example Data

| Query | Positive document |
| --- | --- |
| Podatek od akcji lub ETF (24 chars) | „Jeśli sprzedajesz akcje bez wypłat, Twój zysk podlega opodatkowaniu zgodnie z § 1001. Ale nie wszystkie zrealizowane zyski zostaną uznane za podlegające opodatkowaniu. A niektóre zyski, które prawdopodobnie nie zostaną zreal ... [truncated 225 chars](2122 chars) |
| Jaki kurs wymiany stosuje El Al przy przeliczaniu kwoty płatności końcowej na szekle? (85 chars) | „Stawka za „czeki i przelewy” jest ustalana przez każdy bank wielokrotnie w ciągu dnia w oparciu o rynek. Jest to przeciwieństwo stawki za „gotówkę/banknoty”, również ustalaną przez każdy bank, a „„stawka reprezentatywna”” (ש ... [truncated 225 chars](691 chars) |
| Ile brokerzy płacą za wymianę za transakcję? (44 chars) | Nie ma jednej odpowiedzi na to pytanie, ale są pewne ogólniki. Większość giełd rozróżnia pasywną i agresywną stronę handlu. Uczestnik pasywny to zlecenie, które znajdowało się na rynku w momencie transakcji. Jest to zlecenie, ... [truncated 225 chars](1211 chars) |
| Czy dochód freelancera uzyskany przez obywatela USA mieszkającego za granicą podlega stanowemu podatkowi dochodowemu? (117 chars) | Brak podatków stanowych, ale Włochy mają również korzystny traktat z rządem federalnym Stanów Zjednoczonych. Zastanów się nad obniżeniem podatków federalnych do 5% ;) to gruba lektura, http://www.irs.gov/businesses/internatio ... [truncated 225 chars](629 chars) |
| Ile wynosi inflacja? (20 chars) | Istnieje coś takiego jak indeks cen konsumpcyjnych (CPI). Istnieje koszyk towarów, po który ludzie, którzy prowadzą indeks, w zasadzie robią zakupy. Jest o wiele bardziej szczegółowy ze względu na dokładność, ale najważniejsz ... [truncated 225 chars](614 chars) |

## Dataset Information

| Field | Value |
| --- | --- |
| Nano set | NanoMTEB-Polish |
| Backing dataset | NanoMTEB-Polish |
| Task / split | fiqa |
| Hugging Face dataset | [hakari-bench/NanoMTEB-Polish](https://huggingface.co/datasets/hakari-bench/NanoMTEB-Polish) |
| Source dataset | [mteb/FiQA-PL](https://huggingface.co/datasets/mteb/FiQA-PL) |
| Language | pl |
| Category | natural_language |
| Queries | 200 |
| Documents | 10,000 |
| Positive qrels | 534 |
| Avg positives / query | 2.670 |
| Positives per query (min / median / max) | 1 / 2.0 / 12 |
| Queries with multiple positives | 128 (64.0%) |
| BM25 nDCG@10 | 0.2353 |
| BM25 hit@10 | 0.4550 |
| BM25 Recall@100 | 0.4906 |
| BM25 candidate subset | top-500 (`bm25`) |
| Dense nDCG@10 | 0.3890 |
| Dense hit@10 | 0.6300 |
| Dense Recall@100 | 0.6685 |
| Dense candidate subset | top-500 (`harrier_oss_v1_270m`) |
| Reranking hybrid nDCG@10 | 0.3574 |
| Reranking hybrid hit@10 | 0.6450 |
| Reranking hybrid Recall@100 | 0.6835 |
| Reranking hybrid candidate subset | top-100 plus optional rank-101 safeguard (`reranking_hybrid`) |
| Reranking hybrid candidates / query | 100-101 |
| Reranking hybrid safeguard rows | 26 |
| Query length avg chars | 68.51 |
| Document length avg chars | 808.82 |

### Public Sources

- [FiQA 2018 challenge site](https://sites.google.com/view/fiqa/), official challenge page.
- [WWW18 Open Challenge: Financial Opinion Mining and Question Answering](https://research.universityofgalway.ie/en/publications/www18-open-challenge-financial-opinion-mining-and-question-answer/), challenge paper record.
- [mteb/FiQA-PL](https://huggingface.co/datasets/mteb/FiQA-PL), Polish source dataset card.

### Hugging Face Links

- Nano dataset: [hakari-bench/NanoMTEB-Polish](https://huggingface.co/datasets/hakari-bench/NanoMTEB-Polish)
- Source task dataset: [mteb/FiQA-PL](https://huggingface.co/datasets/mteb/FiQA-PL)

### Source Reference Table

| Title | Year | Type | URL |
| --- | ---: | --- | --- |
| WWW18 Open Challenge: Financial Opinion Mining and Question Answering | 2018 | task paper | https://research.universityofgalway.ie/en/publications/www18-open-challenge-financial-opinion-mining-and-question-answer/ |
| FiQA 2018 challenge site | 2018 | project page | https://sites.google.com/view/fiqa/ |
| mteb/FiQA-PL |  | dataset card | https://huggingface.co/datasets/mteb/FiQA-PL |

## Machine-Readable Metadata

<!-- benchmark-task-metadata:v1 -->

```yaml
benchmark_task_metadata:
  schema_version: 1
  document_status: first_pass
  nano_set: NanoMTEB-Polish
  backing_dataset: NanoMTEB-Polish
  dataset_id: hakari-bench/NanoMTEB-Polish
  task_name: fiqa
  split_name: fiqa
  language: pl
  category: natural_language
  document_path: docs/benchmark_tasks/NanoMTEB-Polish/fiqa.md
  source_research:
    primary_source_type: project_page
    paper_pdf_or_html_checked: true
    no_paper_note: no standalone Polish FiQA paper was confirmed
  counts:
    queries: 200
    documents: 10000
    positive_qrels: 534
  positives_per_query:
    average: 2.67
    min: 1
    median: 2.0
    max: 12
    multi_positive_queries: 128
    multi_positive_query_percent: 64.0
  text_stats_chars:
    query_mean: 68.51
    document_mean: 808.8181
  bm25:
    ndcg_at_10: 0.23527604820742223
    hit_at_10: 0.455
    source: dataset_candidate_subset
  example_count: 5
  candidate_subsets:
    bm25:
      config: bm25
      label: BM25
      source: dataset_candidate_subset
      top_k: 500
      ndcg_at_10: 0.2352760482
      hit_at_10: 0.455
      recall_at_100: 0.4906367041
      candidate_count_min: 500
      candidate_count_max: 500
      candidate_count_mean: 500.0
      query_count: 200
      query_coverage: 1.0
      relevant_coverage_at_100: 0.4906367041
    dense:
      config: harrier_oss_v1_270m
      label: Dense
      source: dataset_candidate_subset
      top_k: 500
      ndcg_at_10: 0.3889841145
      hit_at_10: 0.63
      recall_at_100: 0.6685393258
      candidate_count_min: 500
      candidate_count_max: 500
      candidate_count_mean: 500.0
      query_count: 200
      query_coverage: 1.0
      relevant_coverage_at_100: 0.6685393258
    reranking_hybrid:
      config: reranking_hybrid
      label: Reranking hybrid
      source: dataset_candidate_subset
      top_k: 100
      ndcg_at_10: 0.3573770736
      hit_at_10: 0.645
      recall_at_100: 0.6835205993
      candidate_count_min: 100
      candidate_count_max: 101
      candidate_count_mean: 100.13
      query_count: 200
      query_coverage: 1.0
      relevant_coverage_at_100: 0.6835205993
      safeguard_positive_rows: 26
      rows_with_101_candidates: 26
```
