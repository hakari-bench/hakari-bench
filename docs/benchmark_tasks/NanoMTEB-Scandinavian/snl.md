# NanoMTEB-Scandinavian / snl

## Overview

SNL Retrieval is the Scandinavian benchmark's retrieval adaptation of Store
norske leksikon article data, where headlines or headwords are paired with long
Norwegian encyclopedia entries and ingresses. No standalone SNL retrieval paper
was confirmed, so the task is best read from the dataset card and sampled data:
very short title-like queries such as person names or terms must retrieve the
matching long lexicon article. Entity normalization and exact headword matching
matter, but the long documents also require handling expansive encyclopedic
context.

## Details

### What the Original Data Measures

The SEB paper describes SNL Retrieval as web-scraped articles and ingresses from
the Norwegian lexicon Det Store Norske Leksikon. The source Hugging Face
dataset `adrlau/navjordj-SNL_summarization_copy` exposes fields such as
`headline`, `category`, `ingress`, and `article`; SEB converts paired headline
and article/ingress material into retrieval examples.

No standalone SNL Retrieval paper was found in this pass. The source is best
treated as a retrieval adaptation of a Norwegian encyclopedia summarization
resource rather than an independently designed IR dataset.

### Observed Data Profile

The Nano split has 200 Norwegian queries, 1,300 documents, and 200 positive
qrels. Every query has one positive. Queries average only 13.25 characters,
while documents average 1,982.85 characters. Sampled queries are mostly titles
or headwords, such as `Eric Clapton`, `dobbeltbrytning`, and `Andrea
Camilleri`.

Documents are long encyclopedia entries, sometimes tens of thousands of
characters. The title-like query format means entity normalization and exact
headword matching matter.

### BM25 Difficulty

Using the dataset-provided BM25 candidate column, BM25 reaches nDCG@10 =
0.8781 and hit@10 = 0.9000. BM25 ranks 170 positives first. The task is often
easy for lexical retrieval because the query is a distinctive title, but shorter
or ambiguous headwords can still be missed.

### Training Data That May Help

Useful training data includes non-overlapping SNL headline/article pairs,
Norwegian encyclopedia title-to-article retrieval, and hard negatives from
nearby categories. Training should exclude Nano queries and matching SNL article
texts from this split.

### Synthetic Data Guidance

Generate Norwegian encyclopedia entries with explicit titles, categories, and
body text. Use title, alias, and short headword queries. Include hard negatives
with the same surname, category, or concept family to reduce pure title matching.

## Example Data

| Query | Positive document |
| --- | --- |
| Kasimir Edschmid (16 chars) | Biografi Kasimir Edschmid studerte romansk filologi i blant annet München og Paris og fikk tidlig et stort litterært kontaktnett. Under første verdenskrig arbeidet han som litteraturanmelder. Han var en av grunnleggerne av ku ... [truncated 225 chars](2627 chars) |
| Hermann Bondi (13 chars) | Biografi Bondi dro fra Wien til Cambridge i 1937 i håp om å studere med Arthur Eddington. Da andre verdenskrig brøt ut ble han internert, først på Isle of Man, senere i Canada. I denne perioden ble han kjent med Thomas Gold, ... [truncated 225 chars](1611 chars) |
| bønn (kristendom) (35 chars) | Kristenhetens viktigste bønn er Fadervår. Den brukes i alle kristne gudstjenester, og svært mange av verdens kristne ber den daglig. Bønnen kan inneholde mange ulike elementer. Bønnen kan være lovprisning og takk til Gud, Jes ... [truncated 225 chars](1823 chars) |
| Centrum-Demokraterne (20 chars) | Centrum-Demokraterne deltok i «Firkløver»-regjeringen i 1982–1988 og i koalisjonsregjeringen i 1993–1996. Partiet falt ut av Folketinget ved valget i 2001 og fikk bare 1,8 prosent av stemmene. For valgresultater, se for øvrig ... [truncated 225 chars](498 chars) |
| Joey Baron (10 chars) | Imidlertid blir han særlig forbundet med modernister som Bill Frisell og John Zorn. Baron har deltatt på en lang rekke album, og har også utgitt flere under eget navn. Utvalgte utgivelser som bandleder Raised Pleasure Dot (19 ... [truncated 225 chars](470 chars) |

## Dataset Information

| Field | Value |
| --- | --- |
| Nano set | NanoMTEB-Scandinavian |
| Backing dataset | NanoMTEB-Scandinavian |
| Task / split | snl |
| Hugging Face dataset | [hakari-bench/NanoMTEB-Scandinavian](https://huggingface.co/datasets/hakari-bench/NanoMTEB-Scandinavian) |
| Language | no |
| Category | natural_language |
| Queries | 200 |
| Documents | 1,300 |
| Positive qrels | 200 |
| BM25 nDCG@10 | 0.8781 |
| BM25 hit@10 | 0.9000 |
| Query length avg chars | 13.25 |
| Document length avg chars | 1,982.85 |

### Public Sources

- [The Scandinavian Embedding Benchmarks](https://arxiv.org/abs/2406.02396); 2024; Kenneth Enevoldsen et al.
- [adrlau/navjordj-SNL_summarization_copy dataset card](https://huggingface.co/datasets/adrlau/navjordj-SNL_summarization_copy).
- [mteb/SNLRetrieval dataset card](https://huggingface.co/datasets/mteb/SNLRetrieval).

### Hugging Face Links

- Nano dataset: [hakari-bench/NanoMTEB-Scandinavian](https://huggingface.co/datasets/hakari-bench/NanoMTEB-Scandinavian)
- Source dataset: [adrlau/navjordj-SNL_summarization_copy](https://huggingface.co/datasets/adrlau/navjordj-SNL_summarization_copy)
- MTEB source task: [mteb/SNLRetrieval](https://huggingface.co/datasets/mteb/SNLRetrieval)

### Source Reference Table

| Title | Year | Type | URL |
| --- | ---: | --- | --- |
| The Scandinavian Embedding Benchmarks | 2024 | arXiv paper | https://arxiv.org/abs/2406.02396 |
| adrlau/navjordj-SNL_summarization_copy | 2023 | dataset card | https://huggingface.co/datasets/adrlau/navjordj-SNL_summarization_copy |
| mteb/SNLRetrieval | 2024 | dataset card | https://huggingface.co/datasets/mteb/SNLRetrieval |

## Machine-Readable Metadata

<!-- benchmark-task-metadata:v1 -->

```yaml
benchmark_task_metadata:
  schema_version: 1
  document_status: first_pass
  nano_set: NanoMTEB-Scandinavian
  backing_dataset: NanoMTEB-Scandinavian
  dataset_id: hakari-bench/NanoMTEB-Scandinavian
  task_name: snl
  split_name: snl
  language: no
  category: natural_language
  document_path: docs/benchmark_tasks/NanoMTEB-Scandinavian/snl.md
  source_research:
    primary_source_type: benchmark_paper_and_dataset_card
    paper_pdf_or_html_checked: true
    no_paper_note: No standalone SNL Retrieval paper was found; SEB paper and Hugging Face source cards were checked.
  counts:
    queries: 200
    documents: 1300
    positive_qrels: 200
  positives_per_query:
    average: 1.0
    min: 1
    median: 1.0
    max: 1
    multi_positive_queries: 0
    multi_positive_query_percent: 0.0
  text_stats_chars:
    query_mean: 13.25
    document_mean: 1982.8515384615384
  bm25:
    ndcg_at_10: 0.8780559736224016
    hit_at_10: 0.9
    source: dataset_bm25_column
  learning:
    original_train_split: available
    evaluation_split_origin: test
    train_eval_overlap_audit: not_audited
    leakage_note: exclude Nano SNL titles, qrels, and matching article/ingress texts
    useful_training_data:
      - non-overlapping SNL headline/article pairs
      - Norwegian encyclopedia title-to-article retrieval pairs
      - category-neighbor hard negatives
      - Norwegian alias and headword matching data
    synthetic_data:
      document_generation: Norwegian encyclopedia entries with title, category, ingress, and article body
      question_generation: short title, alias, and headword queries
      answerability: each positive should be the article corresponding to the title-like query
    multi_positive_training: single_positive_title_article_focus
  links:
    nano_dataset: https://huggingface.co/datasets/hakari-bench/NanoMTEB-Scandinavian
    source_urls:
      - label: Scandinavian Embedding Benchmarks
        url: https://arxiv.org/abs/2406.02396
      - label: adrlau/navjordj-SNL_summarization_copy
        url: https://huggingface.co/datasets/adrlau/navjordj-SNL_summarization_copy
      - label: mteb/SNLRetrieval
        url: https://huggingface.co/datasets/mteb/SNLRetrieval
    source_notes:
      - SEB defines the retrieval formalization; source card exposes headline, ingress, category, and article fields.
  references:
    - title: "The Scandinavian Embedding Benchmarks"
      url: https://arxiv.org/abs/2406.02396
      year: 2024
      doi: 10.48550/arXiv.2406.02396
      is_paper: true
      source_confidence: benchmark_paper
```
