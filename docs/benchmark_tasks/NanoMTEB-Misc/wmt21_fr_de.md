# NanoMTEB-Misc / wmt21_fr_de

## Overview

`NanoMTEB-Misc / wmt21_fr_de` is the WMT21 French-German direction of CLSD.
German news sentences retrieve French translation counterparts.

## Details

### What the Original Data Measures

[Cross-Lingual Semantic Discrimination for Building Better Multilingual
Embeddings](https://arxiv.org/abs/2502.08638) presents CLSD as a benchmark for
discriminating true cross-lingual equivalents from semantically close
distractors. The WMT21 French-German direction tests whether German sentence
embeddings can retrieve the matching French sentence.

The [Andrianos/clsd_wmt19_21](https://huggingface.co/datasets/Andrianos/clsd_wmt19_21)
dataset card is the source record for the WMT19/WMT21 CLSD retrieval tables.
This split reverses the previous direction: queries are German and documents
are French.

### Observed Data Profile

The split has 200 queries, 4,465 documents, and 200 positive qrel rows. Every
query has one positive. Queries average 174.99 characters and documents average
174.45 characters. The first examples are finance-news translation pairs with
numbers, markets, and COVID-era context.

### BM25 Difficulty

Using the dataset-provided BM25 candidate column, BM25 reaches nDCG@10 =
0.4283 and hit@10 = 0.6350. It ranks 45 positives at rank 1 and 127 in the top
10.

BM25 is still limited by cross-lingual mismatch, but this direction has more
shared symbols, market names, and numeric clues in the observed examples. Dense
models still need sentence-level German-French alignment to solve non-numeric
cases.

### Training Data That May Help

German-French sentence retrieval, WMT-style news bitext, multilingual
contrastive training, and CLSD hard-negative objectives should help. Hard
negatives should share people, numbers, and institutions while changing the
meaning.

### Synthetic Data Guidance

Generate German-to-French retrieval pairs from unseen parallel news sentences.
Add French distractors that keep the same entities or figures but correspond to
different statements. Include both literal and paraphrastic translations to
avoid overfitting to cognates and numbers.

## Example Data

| Query | Positive document |
| --- | --- |
| Am selben Tag kündigte das Büro des Premierministers an, dass Justin Trudeau, wie von der Opposition gefordert, zu einem noch zu bestimmenden Termin ebenfalls vor diesem Ausschuss aussagen wird. (194 chars) | Le même jour, le bureau du premier ministre a fait savoir que Justin Trudeau témoignerait lui aussi devant cette commission, comme l'exige l'opposition, à une date restant à déterminer. (185 chars) |
| Präsident Sebastian Piñera verkündete am 24. Juli eine historische Reform, die es den Chilenen erlaubt, 10 % ihrer privaten Rentenfonds vorzeitig zu entnehmen, um die durch die Covid-19-Pandemie verursachte Wirtschaftskrise z ... [truncated 225 chars](238 chars) | Le président Sebastian Piñera a promulgué le 24 juillet une réforme historique qui permet aux Chiliens le retrait anticipé de 10% de leurs fonds de retraite privés pour faire face à la crise économique entraînée par la pandém ... [truncated 225 chars](240 chars) |
| Geringfügige Anpassungen sollen mehr Kapital für Investoren freisetzen und es so „den Unternehmen leichter machen, die benötigte Finanzierung zu erhalten und in unsere Wirtschaft zu investieren“, versichert der Vizepräsident ... [truncated 225 chars](272 chars) | Des ajustements mineurs qui doivent libérer plus de capital pour les investisseurs et donc permettre aux "entreprises d'obtenir plus facilement les financements dont elles ont besoin et d'investir dans notre économie", assure ... [truncated 225 chars](292 chars) |
| Die Giganten Apple, Alphabet Inc und Amazon.com werden ihre Ergebnisse am 30. Juli vorlegen, dem gleichen Tag, an dem das Handelsministerium seine erste Schätzung für das BIP aus dem zweiten Quartal bekanntgeben wird, das nac ... [truncated 225 chars](270 chars) | Les géants Apple, Alphabet Inc et Amazon.com doivent publier leurs résultats le 30 juillet, le jour où le département du Commerce doit annoncer sa première estimation du PIB du deuxième trimestre, attendu en chute de 35% par ... [truncated 225 chars](239 chars) |
| Justin Trudeau hatte zugegeben, dass er einen Fehler gemacht hat, als er sich während der Verhandlungen zwischen seiner Regierung und UNIS nicht von den Gesprächen fernhielt. (174 chars) | Justin Trudeau avait admis avoir commis une erreur en ne se retirant pas des discussions lors des négociations entre son gouvernement et UNIS. (142 chars) |

## Dataset Information

| Field | Value |
| --- | --- |
| Nano set | NanoMTEB-Misc |
| Backing dataset | NanoMTEB-Misc |
| Task / split | wmt21_fr_de |
| Hugging Face dataset | [hakari-bench/NanoMTEB-Misc](https://huggingface.co/datasets/hakari-bench/NanoMTEB-Misc) |
| Source dataset | [Andrianos/clsd_wmt19_21](https://huggingface.co/datasets/Andrianos/clsd_wmt19_21) |
| Language | multilingual |
| Category | natural_language |
| Queries | 200 |
| Documents | 4,465 |
| Positive qrels | 200 |
| BM25 nDCG@10 | 0.4283 |
| BM25 hit@10 | 0.6350 |
| Query length avg chars | 174.99 |
| Document length avg chars | 174.45 |

### Public Sources

- [Cross-Lingual Semantic Discrimination for Building Better Multilingual Embeddings](https://arxiv.org/abs/2502.08638), CLSD task paper.
- [Andrianos/clsd_wmt19_21](https://huggingface.co/datasets/Andrianos/clsd_wmt19_21), dataset card.
- [MTEB retrieval task listing](https://embeddings-benchmark.github.io/mteb/overview/available_tasks/retrieval/), task metadata.

### Hugging Face Links

- Nano dataset: [hakari-bench/NanoMTEB-Misc](https://huggingface.co/datasets/hakari-bench/NanoMTEB-Misc)
- Source task dataset: [Andrianos/clsd_wmt19_21](https://huggingface.co/datasets/Andrianos/clsd_wmt19_21)

### Source Reference Table

| Title | Year | Type | URL |
| --- | ---: | --- | --- |
| Cross-Lingual Semantic Discrimination for Building Better Multilingual Embeddings | 2025 | task paper | https://arxiv.org/abs/2502.08638 |
| Andrianos/clsd_wmt19_21 |  | dataset card | https://huggingface.co/datasets/Andrianos/clsd_wmt19_21 |
| MTEB retrieval task listing |  | benchmark metadata | https://embeddings-benchmark.github.io/mteb/overview/available_tasks/retrieval/ |

## Machine-Readable Metadata

<!-- benchmark-task-metadata:v1 -->

```yaml
benchmark_task_metadata:
  schema_version: 1
  document_status: first_pass
  nano_set: NanoMTEB-Misc
  backing_dataset: NanoMTEB-Misc
  dataset_id: hakari-bench/NanoMTEB-Misc
  task_name: wmt21_fr_de
  split_name: wmt21_fr_de
  language: multilingual
  category: natural_language
  document_path: docs/benchmark_tasks/NanoMTEB-Misc/wmt21_fr_de.md
  source_research:
    primary_source_type: task_paper
    paper_pdf_or_html_checked: true
    no_paper_note: null
  counts:
    queries: 200
    documents: 4465
    positive_qrels: 200
  positives_per_query:
    average: 1.0
    min: 1
    median: 1.0
    max: 1
    multi_positive_queries: 0
    multi_positive_query_percent: 0.0
  text_stats_chars:
    query_mean: 174.99
    document_mean: 174.45
  bm25:
    ndcg_at_10: 0.4283
    hit_at_10: 0.635
    source: dataset_bm25_column
  example_count: 5
```
