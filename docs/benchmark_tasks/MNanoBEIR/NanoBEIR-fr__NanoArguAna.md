# MNanoBEIR / NanoBEIR-fr / NanoArguAna

## Overview

ArguAna is an argument retrieval benchmark where the query is an argument and
the relevant document is a counterargument. `NanoBEIR-fr__NanoArguAna` is the
French MNanoBEIR version: long French translated arguments must retrieve French
translated counterarguments with an opposing stance. The task tests
argumentative fit and stance reversal.

## Details

### What the Original Data Measures

[Retrieval of the Best Counterargument without Prior Topic
Knowledge](https://aclanthology.org/P18-1023/) studies the task of finding the
best counterargument for a given argument. The paper argues that good
counterarguments often invoke the same aspects while taking the opposite stance,
and builds argument-counterargument pairs from debate portal data.

[BEIR: A Heterogeneous Benchmark for Zero-shot Evaluation of Information
Retrieval Models](https://arxiv.org/abs/2104.08663) includes ArguAna as an
argument retrieval task. [MMTEB: Massive Multilingual Text Embedding
Benchmark](https://arxiv.org/abs/2502.13595) provides the multilingual context
for this French split.

### Observed Data Profile

The sampled French Nano task has 50 queries, 3,635 documents, and 50 positive
qrel rows. Every query has one positive counterargument. The average query
length is 1,271.18 characters, and the average document length is 1,156.98
characters.

The inspected examples cover gender roles in work, Democratic versus Republican
economic outcomes, reparations, intervention in Syria, and free higher
education. Both queries and positives are long French translated arguments with
premises, conclusions, and citations.

### BM25 Difficulty

Using the dataset-provided BM25 candidate column, BM25 reaches nDCG@10 =
0.3993 and hit@10 = 0.6800. BM25 ranks the positive first for 9 queries, and
the median first-positive rank is 5.5.

Lexical overlap is only partly useful because a counterargument discusses the
same topic while opposing the stance. Strong models should retrieve the rebuttal
that targets the same aspect, not merely a same-topic argument.

### Training Data That May Help

Useful training data includes non-overlapping argument-counterargument pairs,
stance-aware retrieval datasets, debate portal argument pairs, claim rebuttal
data, and French or multilingual argument mining corpora. Training should
exclude ArguAna, BEIR, NanoBEIR, or translated debate records likely to overlap
with these arguments.

### Synthetic Data Guidance

For document-to-query generation, start from non-evaluation counterarguments
and generate opposing arguments that share the same issue and aspect. For joint
generation, create paired pro and con arguments with explicit stance reversal
and same-topic hard negatives.

## Example Data

| Query | Positive document |
| --- | --- |
| Le public est indifférent à la réforme. Il est discutable que la réforme de la Chambre des Lords soit une priorité absolue dans le contexte économique actuel, sans parler de la capacité d'un gouvernement de coalition à initie ... [truncated 225 chars](646 chars) | La campagne pour le vote alternatif ne peut pas être comparée à une réforme de la Chambre des Lords. De plus, il ne faut pas confondre un public mal informé par la propagande politique avec de l'apathie. Souvent, les électeur ... [truncated 225 chars](471 chars) |
| L'expansion de Heathrow est cruciale pour l'économie. L'expansion de Heathrow permettrait de maintenir de nombreux emplois actuels tout en en créant de nouveaux. Actuellement, Heathrow soutient environ 250 000 emplois. En out ... [truncated 225 chars](1372 chars) | La communauté des affaires est loin d'être unie dans son supposé soutien à une troisième piste. Des enquêtes suggèrent que de nombreuses entreprises influentes ne soutiennent en réalité pas l'expansion. Une lettre exprimant d ... [truncated 225 chars](1519 chars) |
| Les gens sont submergés par trop de choix, ce qui les rend moins heureux. La publicité submerge beaucoup de gens avec le besoin incessant de choisir entre des demandes concurrentes pour leur attention – cela est connu sous le ... [truncated 225 chars](1054 chars) | Les gens sont mécontents parce qu'ils ne peuvent pas tout avoir, et non parce qu'ils ont trop de choix et que cela les stresse. En réalité, les publicités jouent un rôle crucial en s'assurant que l'argent dont disposent les g ... [truncated 225 chars](988 chars) |
| Les cyberattaques sont souvent menées par des acteurs non étatiques, tels que des cyberterroristes ou des hacktivistes (activistes sociaux qui piratent), sans aucune implication de l'État concerné. Par exemple, en 2007, une v ... [truncated 225 chars](1072 chars) | En cas d'attaques par des acteurs non étatiques, de nombreux experts en droit international s'accordent à dire que l'État peut encore riposter en légitime défense si un autre État est 'incapable ou réticent à prendre des mesu ... [truncated 225 chars](607 chars) |
| Parce que la religion favorise la certitude des croyances, la haine inspirée par le divin est facile à utiliser pour justifier et promouvoir des actions violentes et des pratiques discriminatoires. La liberté d'expression doi ... [truncated 225 chars](1319 chars) | Personne n'est forcé de commettre des actes de violence par les paroles d'autrui; c'est leur choix de le faire. De même, il y a beaucoup de gens qui pourraient avoir des opinions considérées comme homophobes mais qui seraient ... [truncated 225 chars](695 chars) |

## Dataset Information

| Field | Value |
| --- | --- |
| Nano set | MNanoBEIR |
| Backing dataset | NanoBEIR-fr |
| Task / split | NanoArguAna |
| Hugging Face dataset | [hakari-bench/NanoBEIR-fr](https://huggingface.co/datasets/hakari-bench/NanoBEIR-fr) |
| Language | fr |
| Category | natural_language |
| Queries | 50 |
| Documents | 3,635 |
| Positive qrels | 50 |
| BM25 nDCG@10 | 0.3993 |
| BM25 hit@10 | 0.6800 |
| Query length avg chars | 1,271.18 |
| Document length avg chars | 1,156.98 |

### Public Sources

- [Retrieval of the Best Counterargument without Prior Topic Knowledge](https://aclanthology.org/P18-1023/).
- [BEIR: A Heterogeneous Benchmark for Zero-shot Evaluation of Information Retrieval Models](https://arxiv.org/abs/2104.08663).
- [MMTEB: Massive Multilingual Text Embedding Benchmark](https://arxiv.org/abs/2502.13595).
- [Zeta Alpha NanoBEIR collection](https://huggingface.co/collections/zeta-alpha-ai/nanobeir).

### Hugging Face Links

- Nano dataset: [hakari-bench/NanoBEIR-fr](https://huggingface.co/datasets/hakari-bench/NanoBEIR-fr)
- Source collection: [Zeta Alpha NanoBEIR collection](https://huggingface.co/collections/zeta-alpha-ai/nanobeir)

### Source Reference Table

| Title | Year | Type | URL |
| --- | ---: | --- | --- |
| Retrieval of the Best Counterargument without Prior Topic Knowledge | 2018 | task paper | https://aclanthology.org/P18-1023/ |
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
  backing_dataset: NanoBEIR-fr
  dataset_id: hakari-bench/NanoBEIR-fr
  task_name: NanoArguAna
  split_name: NanoArguAna
  language: fr
  category: natural_language
  document_path: docs/benchmark_tasks/MNanoBEIR/NanoBEIR-fr__NanoArguAna.md
  source_research:
    primary_source_type: task_paper
    paper_pdf_or_html_checked: true
    no_paper_note: null
  counts:
    queries: 50
    documents: 3635
    positive_qrels: 50
  positives_per_query:
    average: 1.0
    min: 1
    median: 1.0
    max: 1
    multi_positive_queries: 0
    multi_positive_query_percent: 0.0
  text_stats_chars:
    query_mean: 1271.18
    document_mean: 1156.980193
  bm25:
    ndcg_at_10: 0.3993454261
    hit_at_10: 0.68
    source: dataset_bm25_column
```
