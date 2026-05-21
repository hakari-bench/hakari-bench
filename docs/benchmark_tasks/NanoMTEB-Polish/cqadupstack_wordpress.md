# NanoMTEB-Polish / cqadupstack_wordpress

## Overview

`cqadupstack_wordpress` is a Polish duplicate-question retrieval task from the
WordPress split of CQADupStack. Queries ask about WordPress shortcodes, post
content, hooks, author contact, sorting, and admin notices. Documents are
candidate community QA posts that may be duplicates of the query.

## Details

### What the Original Data Measures

[CQADupStack: A Benchmark Data Set for Community Question-Answering Research](https://ir.webis.de/anthology/2015.adcs_conference-2015.3/)
is the original benchmark family for community QA duplicate retrieval. The
[MTEB paper](https://arxiv.org/abs/2210.07316) includes CQADupStack as part of
its retrieval suite, while the exact Polish WordPress split comes from the
MTEB/CLARIN dataset cards.

### Observed Data Profile

The split has 200 queries, 10,000 documents, and 344 positive qrels. Queries
average 55.80 characters and documents average 1,040.60 characters. Examples
include nested shortcodes, `wp_query` ordering, `$post->post_content`, visitor
contact forms, and `transition_post_status` admin notices. The task has fewer
positives than several other CQADupStack splits, with 47 multi-positive queries.

### BM25 Difficulty

BM25 reaches nDCG@10 = 0.3139 and hit@10 = 0.4250. It ranks 53 positives first
and 85 in the top 10. WordPress function names and hooks are strong lexical
signals, but duplicate matching still requires understanding equivalent plugin
or theme-development goals.

### Training Data That May Help

Useful data includes non-overlapping WordPress Stack Exchange duplicates,
Polish WordPress support QA, plugin/theme documentation retrieval pairs, and
hard negatives sharing hooks or function names but different behavior. Avoid
evaluation queries, qrels, and positive posts.

### Synthetic Data Guidance

Generate Polish WordPress troubleshooting posts with realistic PHP snippets,
hooks, templates, shortcodes, and admin workflows. Synthetic duplicates should
refer to the same WordPress behavior while varying plugin context, code shape,
or user-facing symptom.

## Example Data

| Query | Positive document |
| --- | --- |
| Programowe wstawianie terminów hierarchicznych i ustalanie terminów dla postów powoduje usterkę? (96 chars) | Wstawianie terminów w taksonomii hierarchicznej Naprawdę mam kilka problemów z wstawianiem terminów. Oto mój scenariusz: mam taksonomię o nazwie veda_release_type: //Release Type and Region $labels = array( 'name'=> _x('Relea ... [truncated 225 chars](3822 chars) |
| Jak zwiększyć długość fragmentu w wordpressie? (46 chars) | fragment w postaciach Mam kod w functions.php: function string_limit_words($string, $word_limit) { $words = explode(' ', $string, ($word_limit + 1)); if(count($słowa) > $word_limit) array_pop($słowa); return implode(' ', $sło ... [truncated 225 chars](306 chars) |
| Strona biblioteki multimediów bardzo wolno, ładuje obrazy w pełnej jakości (74 chars) | Wordpress 3.5 Media Manager - Zmień rozmiar załadowanego obrazu Nowy menedżer mediów ładuje obrazy w PEŁNYM rozmiarze, co jest NAPRAWDĘ nieefektywne dla miniatury. Chciałbym go zastąpić miniaturą o innym rozmiarze, która jest ... [truncated 225 chars](344 chars) |
| Predefiniowane kategorie w wordpressie według parametrów GET (60 chars) | Jak dodać kategorię do: 'wp-admin/post-new.php'? Chcę mieć link do tworzenia nowego posta, który również ustawia kategorię. Próbowałem `wp-admin/post-new.php?post_category=12` i `wp-admin/post-new.php?cat=12`, ale żaden z nic ... [truncated 225 chars](390 chars) |
| Jak wyłączyć komentarze na stronie? (35 chars) | Jak usunąć możliwość komentowania lub publikowania przez użytkownika na stronie? Tworzę nową stronę internetową na Wordpress, a wszystkie moje strony mają na dole pole dodawania komentarza. Chciałbym, aby zostało to usunięte ... [truncated 225 chars](482 chars) |

## Dataset Information

| Field | Value |
| --- | --- |
| Nano set | NanoMTEB-Polish |
| Backing dataset | NanoMTEB-Polish |
| Task / split | cqadupstack_wordpress |
| Hugging Face dataset | [hakari-bench/NanoMTEB-Polish](https://huggingface.co/datasets/hakari-bench/NanoMTEB-Polish) |
| Source dataset | [mteb/CQADupstack-Wordpress-PL](https://huggingface.co/datasets/mteb/CQADupstack-Wordpress-PL) |
| Language | pl |
| Category | natural_language |
| Queries | 200 |
| Documents | 10,000 |
| Positive qrels | 344 |
| Avg positives / query | 1.720 |
| Positives per query (min / median / max) | 1 / 1.0 / 62 |
| Queries with multiple positives | 47 (23.5%) |
| BM25 nDCG@10 | 0.3139 |
| BM25 hit@10 | 0.4250 |
| Query length avg chars | 55.80 |
| Document length avg chars | 1,040.60 |

### Public Sources

- [CQADupStack: A Benchmark Data Set for Community Question-Answering Research](https://ir.webis.de/anthology/2015.adcs_conference-2015.3/), original benchmark paper record.
- [MTEB: Massive Text Embedding Benchmark](https://arxiv.org/abs/2210.07316), benchmark paper covering CQADupStack retrieval tasks.
- [CLARIN-KNEXT cqadupstack-wordpress-pl](https://huggingface.co/datasets/clarin-knext/cqadupstack-wordpress-pl), Polish source dataset card.

### Hugging Face Links

- Nano dataset: [hakari-bench/NanoMTEB-Polish](https://huggingface.co/datasets/hakari-bench/NanoMTEB-Polish)
- Source task dataset: [mteb/CQADupstack-Wordpress-PL](https://huggingface.co/datasets/mteb/CQADupstack-Wordpress-PL)

### Source Reference Table

| Title | Year | Type | URL |
| --- | ---: | --- | --- |
| CQADupStack: A Benchmark Data Set for Community Question-Answering Research | 2015 | task paper | https://ir.webis.de/anthology/2015.adcs_conference-2015.3/ |
| MTEB: Massive Text Embedding Benchmark | 2022 | benchmark paper | https://arxiv.org/abs/2210.07316 |
| CLARIN-KNEXT cqadupstack-wordpress-pl |  | dataset card | https://huggingface.co/datasets/clarin-knext/cqadupstack-wordpress-pl |

## Machine-Readable Metadata

<!-- benchmark-task-metadata:v1 -->

```yaml
benchmark_task_metadata:
  schema_version: 1
  document_status: first_pass
  nano_set: NanoMTEB-Polish
  backing_dataset: NanoMTEB-Polish
  dataset_id: hakari-bench/NanoMTEB-Polish
  task_name: cqadupstack_wordpress
  split_name: cqadupstack_wordpress
  language: pl
  category: natural_language
  document_path: docs/benchmark_tasks/NanoMTEB-Polish/cqadupstack_wordpress.md
  source_research:
    primary_source_type: dataset_card
    paper_pdf_or_html_checked: true
    no_paper_note: no standalone paper for this Polish translated split was confirmed
  counts:
    queries: 200
    documents: 10000
    positive_qrels: 344
  positives_per_query:
    average: 1.72
    min: 1
    median: 1.0
    max: 62
    multi_positive_queries: 47
    multi_positive_query_percent: 23.5
  text_stats_chars:
    query_mean: 55.795
    document_mean: 1040.6015
  bm25:
    ndcg_at_10: 0.3139
    hit_at_10: 0.425
    source: dataset_bm25_column
  example_count: 5
```
