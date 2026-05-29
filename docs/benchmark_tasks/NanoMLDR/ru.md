# NanoMLDR / ru

## Overview

`ru` is the Russian split of NanoMLDR. Russian questions retrieve long Russian
articles containing the answer-bearing paragraph.

## Details

### What the Original Data Measures

[M3-Embedding](https://arxiv.org/abs/2402.03216) presents MLDR as a
multilingual long-document retrieval benchmark and reports NDCG@10 across 13
languages. The [MLDR dataset card](https://huggingface.co/datasets/Shitao/MLDR)
lists Russian as Wikipedia-sourced.

### Observed Data Profile

The Nano split has 160 queries, 3,125 documents, and 160 positive qrels. Each
query has one positive. Queries average 92.89 characters and documents average
14,163.52 characters. Examples include city history, geometry, literary motifs,
Palestinian politics, and ancient Macedonian history.

### BM25 Difficulty

Using the dataset-provided BM25 candidate column, BM25 reaches nDCG@10 =
0.7814 and hit@10 = 0.8500. It ranks 115 positives first, with a median best
rank of 1. Russian lexical matching is strong for named entities and
specialized phrases, but some broad cultural questions fall lower.

### Training Data That May Help

Useful training data includes Russian Wikipedia question-article retrieval,
Russian long-document QA, multilingual MLDR training data, and hard negatives
from same-topic Russian articles.

### Synthetic Data Guidance

Synthetic data should generate Russian questions from answer-bearing paragraphs
inside long articles. Hard negatives should share names, dates, or concepts but
omit the relevant answer.

## Example Data

| Query | Positive document |
| --- | --- |
| Кто был автором первого учебника "Курс паровозов", изданного в 1870 году? (73 chars) | История паровоза началась с изобретения первого парового двигателя. Предыстория Впервые силу пара для движения повозки предложил И. Ньютон в 1680 году. Тележка Ньютона была реактивной. Французский инженер Николя Кюньо в 1769 ... [truncated 225 chars](20939 chars) |
| Каким образом Аверченко изображает главных российских политиков Троцкого и Ленина в своих произведениях? (104 chars) | Арка́дий Тимофе́евич Аве́рченко (, Севастополь — 12 марта 1925, Прага) — русский писатель, сатирик, драматург и театральный критик, редактор журналов «Сатирикон» (1908—1913) и «Новый Сатирикон» (1913—1918). Биография Дореволю ... [truncated 225 chars](18971 chars) |
| Какие факторы привели к появлению границы часовых поясов, где применяемое время изменяется сразу на 2 часа, в северных малонаселенных регионах в 1961-1969 годах? (161 chars) | Понятие часово́й по́яс имеет два основных значения: Географи́ческий часовой пояс — условная полоса на земной поверхности шириной ровно 15° (±7,5° относительно среднего меридиана). Средним меридианом нулевого часового пояса сч ... [truncated 225 chars](29926 chars) |
| Какие стены в здании являются самонесущими, а какие - ненесущими? (65 chars) | Зда́ние — результат строительства, представляющий собой объемное надземное строительное сооружение, включающую в себя помещения, предназначенные для проживания и (или) деятельности людей, размещения производства, хранения про ... [truncated 225 chars](28813 chars) |
| Какие издания включены в сборник "Счастье ремесла: Избранные стихотворения"? (76 chars) | Дави́д Самуи́лович Само́йлов (настоящая фамилия — Ка́уфман; 1 июня 1920, Москва — 23 февраля 1990, Таллин) — русский советский поэт и переводчик. Один из крупнейших представителей поколения поэтов, ушедших со студенческой ска ... [truncated 225 chars](17470 chars) |

## Dataset Information

| Field | Value |
| --- | --- |
| Nano set | NanoMLDR |
| Backing dataset | NanoMLDR |
| Task / split | ru |
| Hugging Face dataset | [hakari-bench/NanoMLDR](https://huggingface.co/datasets/hakari-bench/NanoMLDR) |
| Language | ru |
| Category | natural_language |
| Queries | 160 |
| Documents | 3125 |
| Positive qrels | 160 |
| BM25 nDCG@10 | 0.8664 |
| BM25 hit@10 | 0.9125 |
| BM25 Recall@100 | 0.9625 |
| BM25 candidate subset | top-500 (`bm25`) |
| Dense nDCG@10 | 0.5992 |
| Dense hit@10 | 0.6750 |
| Dense Recall@100 | 0.8125 |
| Dense candidate subset | top-500 (`harrier_oss_v1_270m`) |
| Reranking hybrid nDCG@10 | 0.6969 |
| Reranking hybrid hit@10 | 0.7937 |
| Reranking hybrid Recall@100 | 0.9625 |
| Reranking hybrid candidate subset | top-100 plus optional rank-101 safeguard (`reranking_hybrid`) |
| Reranking hybrid candidates / query | 100-101 |
| Reranking hybrid safeguard rows | 6 |
| Query length avg chars | 92.89 |
| Document length avg chars | 14163.52 |

### Public Sources

- [M3-Embedding](https://arxiv.org/abs/2402.03216); 2024; Jianlv Chen et al.
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
  task_name: ru
  split_name: ru
  language: ru
  category: natural_language
  document_path: docs/benchmark_tasks/NanoMLDR/ru.md
  source_research:
    primary_source_type: benchmark_paper_and_dataset_card
    paper_pdf_or_html_checked: true
    no_paper_note: null
  counts:
    queries: 160
    documents: 3125
    positive_qrels: 160
  positives_per_query:
    average: 1.0
    min: 1
    median: 1.0
    max: 1
    multi_positive_queries: 0
    multi_positive_query_percent: 0.0
  text_stats_chars:
    query_mean: 92.89375
    document_mean: 14163.52224
  bm25:
    ndcg_at_10: 0.8663508637332049
    hit_at_10: 0.9125
    source: dataset_candidate_subset
  learning:
    original_train_split: available
    evaluation_split_origin: MLDR Russian split
    train_eval_overlap_audit: not_audited
    leakage_note: exclude NanoMLDR ru queries, qrels, and positive documents
    useful_training_data:
    - Russian long-document QA retrieval pairs
    - Russian Wikipedia article retrieval
    - multilingual MLDR training data outside this Nano split
    - same-topic Russian hard negatives
    synthetic_data:
      document_generation: long Russian encyclopedic articles
      question_generation: paragraph-grounded Russian questions
      answerability: positives should be full articles containing the answer-bearing
        paragraph
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
  - title: 'M3-Embedding: Multi-Linguality, Multi-Functionality, Multi-Granularity
      Text Embeddings Through Self-Knowledge Distillation'
    url: https://arxiv.org/abs/2402.03216
    year: 2024
    is_paper: true
    source_confidence: definitive_paper_link
  candidate_subsets:
    bm25:
      config: bm25
      label: BM25
      source: dataset_candidate_subset
      top_k: 500
      ndcg_at_10: 0.8663508637
      hit_at_10: 0.9125
      recall_at_100: 0.9625
      candidate_count_min: 500
      candidate_count_max: 500
      candidate_count_mean: 500.0
      query_count: 160
      query_coverage: 1.0
      relevant_coverage_at_100: 0.9625
    dense:
      config: harrier_oss_v1_270m
      label: Dense
      source: dataset_candidate_subset
      top_k: 500
      ndcg_at_10: 0.5991692659
      hit_at_10: 0.675
      recall_at_100: 0.8125
      candidate_count_min: 500
      candidate_count_max: 500
      candidate_count_mean: 500.0
      query_count: 160
      query_coverage: 1.0
      relevant_coverage_at_100: 0.8125
    reranking_hybrid:
      config: reranking_hybrid
      label: Reranking hybrid
      source: dataset_candidate_subset
      top_k: 100
      ndcg_at_10: 0.6968523958
      hit_at_10: 0.79375
      recall_at_100: 0.9625
      candidate_count_min: 100
      candidate_count_max: 101
      candidate_count_mean: 100.0375
      query_count: 160
      query_coverage: 1.0
      relevant_coverage_at_100: 0.9625
      safeguard_positive_rows: 6
      rows_with_101_candidates: 6
```
