# NanoMTEB-Polish / cqadupstack_webmasters

## Overview

`cqadupstack_webmasters` is a Polish duplicate-question retrieval task from the
Webmasters split of CQADupStack. Queries ask about SEO, DNS, redirects,
favicons, indexing, and site operations. Documents are community QA posts, and
the model must retrieve duplicate or equivalent website-management questions.

## Details

### What the Original Data Measures

[CQADupStack: A Benchmark Data Set for Community Question-Answering Research](https://ir.webis.de/anthology/2015.adcs_conference-2015.3/)
introduced the duplicate-question benchmark family. The [MTEB paper](https://arxiv.org/abs/2210.07316)
includes CQADupStack among retrieval tasks, while the Polish Webmasters split is
defined by the MTEB/CLARIN dataset cards.

### Observed Data Profile

The split has 200 queries, 10,000 documents, and 882 positive qrels. Queries
average 59.75 characters and documents average 739.15 characters. Examples ask
about home navigation SEO, DNS redirects, Google search visibility, favicon best
practices, and noindex/nofollow behavior for WordPress taxonomy pages. There are
77 multi-positive queries and some very large duplicate clusters.

### BM25 Difficulty

BM25 reaches nDCG@10 = 0.2550 and hit@10 = 0.3950. It ranks 44 positives first
and 79 in the top 10. Web terms give BM25 useful anchors, but duplicate intent
can hinge on operational equivalence: a redirect symptom, indexation policy, or
SEO consequence rather than exact shared wording.

### Training Data That May Help

Useful data includes non-overlapping webmaster QA duplicates, Polish SEO and
site-administration questions, DNS support retrieval pairs, and hard negatives
sharing product names or SEO terms but asking about different actions. Exclude
evaluation queries and positives.

### Synthetic Data Guidance

Generate Polish webmaster posts about domains, redirects, indexing, metadata,
and site assets. Synthetic duplicate questions should keep the same website
state and desired outcome while changing platform, domain registrar, or SEO
terminology.

## Example Data

| Query | Positive document |
| --- | --- |
| find-new/posts&recent=1 jako strona główna: co z SEO? (53 chars) | Czy adres URL z ciągiem zapytania jest lepszy lub gorszy dla SEO niż adres bez niego? Chcę wiedzieć, czy istnieje ogromna różnica pod względem SEO między tymi adresami URL: > mysite.com/ontario/toronto/listings > > lub > > my ... [truncated 225 chars](309 chars) |
| Uniemożliwianie robotom indeksowania określonej części strony (61 chars) | Jak poprosić Google o nieindeksowanie niektórych części mojej strony? > **Możliwy duplikat:** > Uniemożliwianie robotom indeksowania określonej części strony Szukałem dzisiaj starej recenzji w mojej witrynie i zauważyłem, że ... [truncated 225 chars](963 chars) |
| Preferencje SEO dla przekierowania protokołu WWW lub HTTP://? Czy strony www mają wyższą pozycję niż strony bez www? (116 chars) | Z www czy bez www? Którego lepiej użyć Właśnie kupiłem nową domenę `www.reversehacking.com` .... Co jest lepsze dla SEO: `http://reversehacking.com` lub `http://www.reversehacking.com` Myślę, że ludzie zrobią więcej linków za ... [truncated 225 chars](355 chars) |
| Co oznacza podwójny ukośnik w adresach URL? (43 chars) | Czy jest jakiś problem z użyciem dwóch ukośników w środku adresu URL? > **Możliwy duplikat:** > Co oznacza podwójny ukośnik w adresach URL? Pracuję nad strukturą adresu URL mod_rewrite w następujący sposób: http://example.com ... [truncated 225 chars](1149 chars) |
| Dlaczego fragmenty rozszerzone Google miałyby działać u jednego autora witryny, a u innego nie? (95 chars) | rozszerzone fragmenty ignorowane przez google > **Możliwy duplikat:** > Dlaczego fragmenty rozszerzone Google miałyby działać u jednego autora witryny, a u innego nie? Mam tu do czynienia z jednym problemem. Zrobiłem fragment ... [truncated 225 chars](748 chars) |

## Dataset Information

| Field | Value |
| --- | --- |
| Nano set | NanoMTEB-Polish |
| Backing dataset | NanoMTEB-Polish |
| Task / split | cqadupstack_webmasters |
| Hugging Face dataset | [hakari-bench/NanoMTEB-Polish](https://huggingface.co/datasets/hakari-bench/NanoMTEB-Polish) |
| Source dataset | [mteb/CQADupstack-Webmasters-PL](https://huggingface.co/datasets/mteb/CQADupstack-Webmasters-PL) |
| Language | pl |
| Category | natural_language |
| Queries | 200 |
| Documents | 10,000 |
| Positive qrels | 882 |
| Avg positives / query | 4.410 |
| Positives per query (min / median / max) | 1 / 1.0 / 100 |
| Queries with multiple positives | 77 (38.5%) |
| BM25 nDCG@10 | 0.2550 |
| BM25 hit@10 | 0.3950 |
| Query length avg chars | 59.75 |
| Document length avg chars | 739.15 |

### Public Sources

- [CQADupStack: A Benchmark Data Set for Community Question-Answering Research](https://ir.webis.de/anthology/2015.adcs_conference-2015.3/), original benchmark paper record.
- [MTEB: Massive Text Embedding Benchmark](https://arxiv.org/abs/2210.07316), benchmark paper covering CQADupStack retrieval tasks.
- [CLARIN-KNEXT cqadupstack-webmasters-pl](https://huggingface.co/datasets/clarin-knext/cqadupstack-webmasters-pl), Polish source dataset card.

### Hugging Face Links

- Nano dataset: [hakari-bench/NanoMTEB-Polish](https://huggingface.co/datasets/hakari-bench/NanoMTEB-Polish)
- Source task dataset: [mteb/CQADupstack-Webmasters-PL](https://huggingface.co/datasets/mteb/CQADupstack-Webmasters-PL)

### Source Reference Table

| Title | Year | Type | URL |
| --- | ---: | --- | --- |
| CQADupStack: A Benchmark Data Set for Community Question-Answering Research | 2015 | task paper | https://ir.webis.de/anthology/2015.adcs_conference-2015.3/ |
| MTEB: Massive Text Embedding Benchmark | 2022 | benchmark paper | https://arxiv.org/abs/2210.07316 |
| CLARIN-KNEXT cqadupstack-webmasters-pl |  | dataset card | https://huggingface.co/datasets/clarin-knext/cqadupstack-webmasters-pl |

## Machine-Readable Metadata

<!-- benchmark-task-metadata:v1 -->

```yaml
benchmark_task_metadata:
  schema_version: 1
  document_status: first_pass
  nano_set: NanoMTEB-Polish
  backing_dataset: NanoMTEB-Polish
  dataset_id: hakari-bench/NanoMTEB-Polish
  task_name: cqadupstack_webmasters
  split_name: cqadupstack_webmasters
  language: pl
  category: natural_language
  document_path: docs/benchmark_tasks/NanoMTEB-Polish/cqadupstack_webmasters.md
  source_research:
    primary_source_type: dataset_card
    paper_pdf_or_html_checked: true
    no_paper_note: no standalone paper for this Polish translated split was confirmed
  counts:
    queries: 200
    documents: 10000
    positive_qrels: 882
  positives_per_query:
    average: 4.41
    min: 1
    median: 1.0
    max: 100
    multi_positive_queries: 77
    multi_positive_query_percent: 38.5
  text_stats_chars:
    query_mean: 59.75
    document_mean: 739.1547
  bm25:
    ndcg_at_10: 0.255
    hit_at_10: 0.395
    source: dataset_bm25_column
  example_count: 5
```
