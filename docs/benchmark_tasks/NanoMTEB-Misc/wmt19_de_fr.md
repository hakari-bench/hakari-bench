# NanoMTEB-Misc / wmt19_de_fr

## Overview

`NanoMTEB-Misc / wmt19_de_fr` is the WMT19 German-French direction of
Cross-Lingual Semantic Discrimination. French news sentences retrieve their
German translation counterparts from a German candidate pool.

## Details

### What the Original Data Measures

[Cross-Lingual Semantic Discrimination for Building Better Multilingual
Embeddings](https://arxiv.org/abs/2502.08638) introduces CLSD as a retrieval
benchmark built from sentence-aligned parallel data and adversarially generated
semantic distractors. The aim is to test whether multilingual embeddings can
distinguish true cross-lingual semantic equivalents from plausible but
non-equivalent alternatives.

The [clsd_wmt19_21 dataset card](https://huggingface.co/datasets/Andrianos/clsd_wmt19_21)
publishes WMT19 and WMT21 German-French/French-German variants. In this split,
the observed queries are French sentences and the positive documents are German
translations.

### Observed Data Profile

The split has 200 queries, 7,364 documents, and 200 positive qrel rows. Each
query has one positive. Queries average 159.09 characters and documents average
147.49 characters. The samples are short news sentences, headlines, and quoted
statements.

### BM25 Difficulty

Using the dataset-provided BM25 candidate column, BM25 reaches nDCG@10 =
0.2053 and hit@10 = 0.3150. It ranks 27 positives at rank 1 and 63 in the top
10.

Lexical BM25 is weak because the query and document are in different languages.
It only succeeds when names, numbers, or shared entities survive across French
and German. The task primarily rewards cross-lingual semantic alignment rather
than monolingual term overlap.

### Training Data That May Help

High-quality German-French sentence retrieval, bitext mining, translation-pair
contrastive learning, and hard negatives from semantically similar news
sentences are useful. Training should include near-translation distractors, not
only random negatives.

### Synthetic Data Guidance

Create German-French sentence pairs from non-evaluation parallel news or
translation corpora, then add distractors that preserve entities and topic but
change the predicate, stance, number, or event detail. Avoid relying on
dictionary word overlap; this split evaluates sentence-level equivalence.

## Example Data

| Query | Positive document |
| --- | --- |
| L'article 20 du traité de l'UE dispose clairement que les citoyens de l'UE peuvent exercer leur droit de vote et d'éligibilité aux élections au Parlement européen "dans l'Etat membre" dans lequel ils ont leur lieu de résidenc ... [truncated 225 chars](227 chars) | Artikel 20 des EU-Vertrages besagt klipp und klar, dass EU-Bürger „in dem Mitgliedstaat, in dem sie ihren Wohnsitz haben, das aktive und passive Wahlrecht bei den Wahlen zum Europäischen Parlament“ wahrnehmen können. (216 chars) |
| Il a de nombreux éléments pour étayer le credo qu'il ranime pour s'opposer aux sirènes des populistes et selon lequel c'est se fourvoyer que de vouloir quitter l'Europe: le changement climatique, l'imposition des entreprises ... [truncated 225 chars](331 chars) | Für sein nun wiederbelebtes Credo, dass entgegen den Sirenengesängen der Populisten der Rückzug aus Europa ein Holzweg ist, gibt es zahlreiche Belege: Klimawandel, Besteuerung der Internetkonzerne, Migration – für all diese H ... [truncated 225 chars](291 chars) |
| De fait, Soros est venu en soutien, dans les décennies passées, à de nombreuses associations et initiatives humanitaires, sociales, scientifiques et artistiques à hauteur de plusieurs millards. Cela concerne notamment des ini ... [truncated 225 chars](282 chars) | Tatsächlich hat Soros in den vergangenen Jahrzehnten mit Milliardensummen zahlreiche humanitäre, soziale, wissenschaftliche und künstlerische Vereine und Initiativen unterstützt. Darunter sind auch solche, die sich für Asylsu ... [truncated 225 chars](242 chars) |
| C'est également pour cette raison qu'elle ne participe pas au congrès du parti à Bonn. (86 chars) | Sie nimmt deshalb auch nicht an dem Parteitag in Bonn teil. (59 chars) |
| C'est la première fois depuis un demi-siècle qu'un Allemand redeviendrait le chef d'une administration bruxelloise. (115 chars) | Zum ersten Mal seit einem halben Jahrhundert wäre damit wieder ein Deutscher der oberste Chef der Brüsseler Behörde. (116 chars) |

## Dataset Information

| Field | Value |
| --- | --- |
| Nano set | NanoMTEB-Misc |
| Backing dataset | NanoMTEB-Misc |
| Task / split | wmt19_de_fr |
| Hugging Face dataset | [hakari-bench/NanoMTEB-Misc](https://huggingface.co/datasets/hakari-bench/NanoMTEB-Misc) |
| Source dataset | [Andrianos/clsd_wmt19_21](https://huggingface.co/datasets/Andrianos/clsd_wmt19_21) |
| Language | multilingual |
| Category | natural_language |
| Queries | 200 |
| Documents | 7,364 |
| Positive qrels | 200 |
| BM25 nDCG@10 | 0.2053 |
| BM25 hit@10 | 0.3150 |
| Query length avg chars | 159.09 |
| Document length avg chars | 147.49 |

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
  task_name: wmt19_de_fr
  split_name: wmt19_de_fr
  language: multilingual
  category: natural_language
  document_path: docs/benchmark_tasks/NanoMTEB-Misc/wmt19_de_fr.md
  source_research:
    primary_source_type: task_paper
    paper_pdf_or_html_checked: true
    no_paper_note: null
  counts:
    queries: 200
    documents: 7364
    positive_qrels: 200
  positives_per_query:
    average: 1.0
    min: 1
    median: 1.0
    max: 1
    multi_positive_queries: 0
    multi_positive_query_percent: 0.0
  text_stats_chars:
    query_mean: 159.09
    document_mean: 147.49
  bm25:
    ndcg_at_10: 0.2053
    hit_at_10: 0.315
    source: dataset_bm25_column
  example_count: 5
```
