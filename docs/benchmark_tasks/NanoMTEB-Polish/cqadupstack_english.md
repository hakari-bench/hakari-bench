# NanoMTEB-Polish / cqadupstack_english

## Overview

`cqadupstack_english` is the Polish version of the CQADupStack English-language
Stack Exchange duplicate-question task. Despite the source forum being about the
English language, both queries and documents in this Nano split are Polish text.
The model must retrieve duplicate grammar, usage, punctuation, pronunciation, or
style questions from a candidate pool of community QA posts.

## Details

### What the Original Data Measures

[CQADupStack: A Benchmark Data Set for Community Question-Answering Research](https://ir.webis.de/anthology/2015.adcs_conference-2015.3/)
frames the task as community QA duplicate detection. The [MTEB paper](https://arxiv.org/abs/2210.07316)
uses CQADupStack as part of its retrieval collection, while the exact Polish
split is documented by the MTEB/CLARIN Polish dataset cards. No standalone paper
for this translated English-language forum split was confirmed.

### Observed Data Profile

The split has 200 queries, 10,000 documents, and 1,356 positive qrels. Queries
are short, averaging 46.52 characters, while documents average 488.14
characters. Examples ask about suffix series, possessives ending in `s`, BE/AE
spelling, sentence agreement, and punctuation. The high average of 6.78 positives
per query shows that duplicate clusters can be broad.

### BM25 Difficulty

BM25 reaches nDCG@10 = 0.3188 and hit@10 = 0.4850, with 59 positives at rank 1
and 97 in the top 10. Exact terms such as suffixes, punctuation marks, and
spelling variants help, but the task is difficult when the same language issue is
phrased through examples rather than shared terminology.

### Training Data That May Help

Useful data includes non-overlapping English-language-usage QA, Polish
translations of grammar questions, duplicate-question pairs, and hard negatives
where the same punctuation or suffix appears in a different grammatical issue.
Training should avoid upstream test questions, qrels, and positive posts.

### Synthetic Data Guidance

Generate Polish questions about English grammar, spelling, pronunciation, and
style, paired with source-style posts that explain the same issue using examples.
Synthetic duplicates should preserve the linguistic phenomenon while changing
the surface example sentence or terminology.

## Example Data

| Query | Positive document |
| --- | --- |
| Ogólne „to” (11 chars) | Do czego odnosi się „to” w „pada deszcz”? Chciałem pozostawić tytuł pytania bez zmian, aby nie odrywać się od zabawy `:)`. W każdym razie > pada deszcz. Co pada? Czy to niebo? Chmury? Pogoda? Deszcz? Co to jest"? Jakieś spost ... [truncated 225 chars](269 chars) |
| Jak przebić zakres dzielonych liczb? (36 chars) | Kiedy powinienem używać pauzy, pauzy i łącznika? Generalnie wiem, jak używać myślnika, ale kiedy powinienem użyć en-dash zamiast em-myślnika, a kiedy powinienem użyć myślnika zamiast em-myślnika? (195 chars) |
| Wybieranie między „z czym eksperymentować” a „z czym eksperymentować” (69 chars) | Kiedy należy kończyć zdanie przyimkiem? Jak wielu innych, często kończę zdanie przyimkiem. Tak, wzdrygam się. Zwykle przepisuję zdanie, ale czasami (w e-mailach) po prostu z tym żyję. _Do_ _z_... wiesz kim jesteś. Czy powinie ... [truncated 225 chars](303 chars) |
| Zasady dotyczące wielkich liter dla „the” (41 chars) | Zapisywanie przedimka określonego wielkimi literami w nazwach Kiedy byłem młody kilkadziesiąt lat temu, uczono mnie, że w przypadku nazw osób, miejsc i rzeczy, które zawierały przedimek określony, przedimek nie był pisany wie ... [truncated 225 chars](752 chars) |
| Jaka jest różnica między „częścią” a „częścią” ？ (48 chars) | Różnica między „częścią” a „częścią”? To pytanie może wydawać się bardzo proste, ale coś mi się myli, kiedy chcę mówić. Przeczytałem książkę zatytułowaną „re-start your English” i zobaczyłem zdanie. > to jest noga. jest częśc ... [truncated 225 chars](471 chars) |

## Dataset Information

| Field | Value |
| --- | --- |
| Nano set | NanoMTEB-Polish |
| Backing dataset | NanoMTEB-Polish |
| Task / split | cqadupstack_english |
| Hugging Face dataset | [hakari-bench/NanoMTEB-Polish](https://huggingface.co/datasets/hakari-bench/NanoMTEB-Polish) |
| Source dataset | [mteb/CQADupstack-English-PL](https://huggingface.co/datasets/mteb/CQADupstack-English-PL) |
| Language | pl |
| Category | natural_language |
| Queries | 200 |
| Documents | 10,000 |
| Positive qrels | 1,356 |
| Avg positives / query | 6.780 |
| Positives per query (min / median / max) | 1 / 1.0 / 79 |
| Queries with multiple positives | 98 (49.0%) |
| BM25 nDCG@10 | 0.3188 |
| BM25 hit@10 | 0.4850 |
| Query length avg chars | 46.52 |
| Document length avg chars | 488.14 |

### Public Sources

- [CQADupStack: A Benchmark Data Set for Community Question-Answering Research](https://ir.webis.de/anthology/2015.adcs_conference-2015.3/), original benchmark paper record.
- [MTEB: Massive Text Embedding Benchmark](https://arxiv.org/abs/2210.07316), benchmark paper covering CQADupStack retrieval tasks.
- [CLARIN-KNEXT cqadupstack-english-pl](https://huggingface.co/datasets/clarin-knext/cqadupstack-english-pl), Polish source dataset card.

### Hugging Face Links

- Nano dataset: [hakari-bench/NanoMTEB-Polish](https://huggingface.co/datasets/hakari-bench/NanoMTEB-Polish)
- Source task dataset: [mteb/CQADupstack-English-PL](https://huggingface.co/datasets/mteb/CQADupstack-English-PL)

### Source Reference Table

| Title | Year | Type | URL |
| --- | ---: | --- | --- |
| CQADupStack: A Benchmark Data Set for Community Question-Answering Research | 2015 | task paper | https://ir.webis.de/anthology/2015.adcs_conference-2015.3/ |
| MTEB: Massive Text Embedding Benchmark | 2022 | benchmark paper | https://arxiv.org/abs/2210.07316 |
| CLARIN-KNEXT cqadupstack-english-pl |  | dataset card | https://huggingface.co/datasets/clarin-knext/cqadupstack-english-pl |

## Machine-Readable Metadata

<!-- benchmark-task-metadata:v1 -->

```yaml
benchmark_task_metadata:
  schema_version: 1
  document_status: first_pass
  nano_set: NanoMTEB-Polish
  backing_dataset: NanoMTEB-Polish
  dataset_id: hakari-bench/NanoMTEB-Polish
  task_name: cqadupstack_english
  split_name: cqadupstack_english
  language: pl
  category: natural_language
  document_path: docs/benchmark_tasks/NanoMTEB-Polish/cqadupstack_english.md
  source_research:
    primary_source_type: dataset_card
    paper_pdf_or_html_checked: true
    no_paper_note: no standalone paper for this Polish translated split was confirmed
  counts:
    queries: 200
    documents: 10000
    positive_qrels: 1356
  positives_per_query:
    average: 6.78
    min: 1
    median: 1.0
    max: 79
    multi_positive_queries: 98
    multi_positive_query_percent: 49.0
  text_stats_chars:
    query_mean: 46.515
    document_mean: 488.136
  bm25:
    ndcg_at_10: 0.3188
    hit_at_10: 0.485
    source: dataset_bm25_column
  example_count: 5
```
