# NanoMuPLeR / sv

## Overview

`NanoMuPLeR / sv` is the Swedish split of MuPLeR-retrieval. Synthetic Swedish
EU-law questions retrieve Swedish DGT-Acquis-derived passages. Each query has a
single relevant passage, making the task a focused benchmark for multilingual
legal retrieval.

## Details

### What the Original Data Measures

The [MuPLeR-retrieval dataset card](https://huggingface.co/datasets/mteb/MuPLeR-retrieval)
defines the task as multilingual parallel legal retrieval with DGT-Acquis
passages and synthetic queries. [An overview of the European Union's highly multilingual parallel corpora](https://link.springer.com/article/10.1007/s10579-014-9277-0)
is the cited reference for the EU parallel-corpus source material.

### Observed Data Profile

The split has 200 Swedish queries, 10,000 documents, and 200 positive qrels.
Queries average 143.74 characters and documents average 656.78 characters.
The sampled records cover capital duty, state aid, procurement evaluation,
Euratom policy priorities, and pre-accession production rules.

### BM25 Difficulty

BM25 reaches nDCG@10 = 0.8563 and hit@10 = 0.9300, with 156 positives at rank 1
and 186 in the top 10. Swedish legal passages share many distinctive numeric and
institutional cues with the queries, so lexical matching is very competitive.

### Training Data That May Help

Useful data includes non-overlapping Swedish EUR-Lex or DGT-Acquis retrieval
pairs, Swedish legal QA, multilingual legal bitext, and hard negatives from
nearby EU provisions. Exclude MuPLeR evaluation pairs and parallel duplicates.

### Synthetic Data Guidance

Generate Swedish legal questions from non-evaluation EU legal passages. Keep
the legal condition, dates, percentages, and named institutions explicit; use
near negatives that share the legal domain but do not answer the query.

## Example Data

| Query | Positive document |
| --- | --- |
| Vilken kommitté bedömde resursinsatser i små interna utredningar ineffektiva och uppmanade att inarbeta urvalskriterier i handboken för operativa metoder? (154 chars) | Kommittén har sett över Olafs hantering av de minimisärenden och undersökte 45 utvalda ärenden med ekonomiska konsekvenser på under 50000 euro var. Kommittén kom fram till att det inte utgör god resursanvändning att avsätta r ... [truncated 225 chars](567 chars) |
| Varför använde beslutet genomsnittlig berörd försäljning för Frankrike istället för senaste hela året för MEGAL‑transporterad energi? (133 chars) | Den försäljning som påverkas av överträdelsen är försäljning av gas som tranporteras av E.ON och GDF genom MEGAL-ledningen i Tyskland, förutom försäljning av gas enligt E.ON:s gasprogram (E.ON Gas Release Programme) och försä ... [truncated 225 chars](676 chars) |
| Vem informerar godkännandets innehavare om vilka mindre ändringar i anmälan som godkänts eller avslagits så att avslagna ändringar upphör omedelbart? (149 chars) | När en eller flera mindre ändringar av typ IA lämnas in som en del av en anmälan ska referensmedlemsstaten informera innehavaren av godkännandet för försäljning om vilka ändringar som har godkänts eller avslagits vid dess gra ... [truncated 225 chars](788 chars) |
| Varför måste en leverantörs totala kapacitet bedömas enbart vid urval och inte omprövas vid bedömning av anbudets kvalitet? (123 chars) | Tilldelningskriterierna måste utarbetas med omsorg för att se till att dessa inte blandas ihop med urvalskriterierna. I domstolens rättspraxis erinras om betydelsen av att skilja mellan bedömningen enligt urvalskriterierna oc ... [truncated 225 chars](702 chars) |
| Vilken rådgivande EU-församling välkomnade en kommissionsenhets beslut att återuppliva observationsorganet för olika kategorier av små och medelstora företag? (158 chars) | Att känna till och förmedla villkoren för de olika kategorierna av små och medelstora företag. All gemenskapspolitik bör baseras på tydliga fakta som ger kunskap om situationen. Begreppet små och medelstora företag omfattar m ... [truncated 225 chars](756 chars) |

## Dataset Information

| Field | Value |
| --- | --- |
| Nano set | NanoMuPLeR |
| Backing dataset | NanoMuPLeR |
| Task / split | sv |
| Hugging Face dataset | [hakari-bench/NanoMuPLeR](https://huggingface.co/datasets/hakari-bench/NanoMuPLeR) |
| Source dataset | [mteb/MuPLeR-retrieval](https://huggingface.co/datasets/mteb/MuPLeR-retrieval) |
| Language | sv |
| Category | natural_language |
| Queries | 200 |
| Documents | 10,000 |
| Positive qrels | 200 |
| BM25 nDCG@10 | 0.8563 |
| BM25 hit@10 | 0.9300 |
| Query length avg chars | 143.74 |
| Document length avg chars | 656.78 |

### Public Sources

- [mteb/MuPLeR-retrieval](https://huggingface.co/datasets/mteb/MuPLeR-retrieval), source dataset card.
- [An overview of the European Union's highly multilingual parallel corpora](https://link.springer.com/article/10.1007/s10579-014-9277-0), DGT-Acquis source reference paper.
- [DGT-Acquis](https://joint-research-centre.ec.europa.eu/language-technology-resources/dgt-acquis_en), European Commission source-corpus page.

### Hugging Face Links

- Nano dataset: [hakari-bench/NanoMuPLeR](https://huggingface.co/datasets/hakari-bench/NanoMuPLeR)
- Source task dataset: [mteb/MuPLeR-retrieval](https://huggingface.co/datasets/mteb/MuPLeR-retrieval)

### Source Reference Table

| Title | Year | Type | URL |
| --- | ---: | --- | --- |
| MuPLeR: Multilingual Parallel Legal Retrieval |  | dataset card | https://huggingface.co/datasets/mteb/MuPLeR-retrieval |
| An overview of the European Union's highly multilingual parallel corpora | 2014 | source paper | https://link.springer.com/article/10.1007/s10579-014-9277-0 |
| DGT-Acquis |  | source corpus | https://joint-research-centre.ec.europa.eu/language-technology-resources/dgt-acquis_en |

## Machine-Readable Metadata

<!-- benchmark-task-metadata:v1 -->

```yaml
benchmark_task_metadata:
  schema_version: 1
  document_status: first_pass
  nano_set: NanoMuPLeR
  backing_dataset: NanoMuPLeR
  dataset_id: hakari-bench/NanoMuPLeR
  task_name: sv
  split_name: sv
  language: sv
  category: natural_language
  document_path: docs/benchmark_tasks/NanoMuPLeR/sv.md
  source_research:
    primary_source_type: dataset_card
    paper_pdf_or_html_checked: true
    no_paper_note: no standalone MuPLeR technical paper was confirmed
  counts:
    queries: 200
    documents: 10000
    positive_qrels: 200
  positives_per_query:
    average: 1.0
    min: 1
    median: 1.0
    max: 1
    multi_positive_queries: 0
    multi_positive_query_percent: 0.0
  text_stats_chars:
    query_mean: 143.74
    document_mean: 656.78
  bm25:
    ndcg_at_10: 0.8563
    hit_at_10: 0.93
    source: dataset_bm25_column
  example_count: 5
```
