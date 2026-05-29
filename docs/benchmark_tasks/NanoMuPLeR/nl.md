# NanoMuPLeR / nl

## Overview

`NanoMuPLeR / nl` is the Dutch split of MuPLeR-retrieval. It uses synthetic
Dutch EU-law questions and Dutch DGT-Acquis-derived passages. The retrieval
target is the single passage that answers the legal condition expressed by the
query.

## Details

### What the Original Data Measures

The [MuPLeR-retrieval dataset card](https://huggingface.co/datasets/mteb/MuPLeR-retrieval)
describes the dataset as multilingual parallel legal retrieval over DGT-Acquis
passages. [An overview of the European Union's highly multilingual parallel corpora](https://link.springer.com/article/10.1007/s10579-014-9277-0)
provides the source-corpus reference for the EU legal parallel texts.

### Observed Data Profile

The Dutch split has 200 queries, 10,000 documents, and 200 positive qrels.
Queries average 147.87 characters and documents average 716.33 characters.
Examples involve capital duty, state aid, procurement criteria, nuclear-safety
research priorities, and pre-accession production reductions.

### BM25 Difficulty

BM25 is the strongest observed MuPLeR split here, with nDCG@10 = 0.8909 and
hit@10 = 0.9400. It ranks 168 positives first and 188 in the top 10. Dutch
queries share many distinctive legal terms, dates, and numeric values with the
positive passages.

### Training Data That May Help

Useful data includes Dutch EUR-Lex or DGT-Acquis retrieval pairs, Belgian/Dutch
legal QA, multilingual legal bitext, and hard negatives from related EU
provisions. Evaluation positives and queries should be excluded.

### Synthetic Data Guidance

Generate Dutch legal questions grounded in non-evaluation EU passages. Preserve
the exact numeric threshold, legal actor, and condition, and create hard
negatives from passages about similar institutions or legal topics.

## Example Data

| Query | Positive document |
| --- | --- |
| Wie heeft de Commissie op 11 oktober 2004 geïnformeerd over een aandelenverwerving die gezamenlijk zeggenschap geeft over een Finse metaalcoatonderneming? (154 chars) | Op 11 oktober 2004 ontving de Commissie een aanmelding van een voorgenomen concentratie in de zin van artikel 4 van Verordening (EG) nr. 139/2004 van de Raad waarin wordt meegedeeld dat de ondernemingen Outokumpu Wasacopper O ... [truncated 225 chars](631 chars) |
| Wat is het aandeel inwoners van de Unie dat binnen drie jaar naar een derde land wil reizen? (92 chars) | Toch wensen de burgers dat de Europese dimensie wordt versterkt. Zo is uit een recente Eurobarometer-enquête naar voren gekomen dat de burgers niet op de hoogte zijn van hun rechten en dat zij op dat gebied hoge verwachtingen ... [truncated 225 chars](657 chars) |
| Welk EU-adviesorgaan steunde de derde optie van de Commissie en benadrukte dat buitengerechtelijke consumentenbeslechting met collectieve rechtsmiddelen moet samengaan? (168 chars) | Het EESC stelde eerder al dat … invoering van een groepsactie op EG-niveau … op generlei wijze afbreuk doet aan de stelsels voor buitengerechtelijke beslechting van consumentengeschillen. Het Comité steunt deze laatste voorbe ... [truncated 225 chars](583 chars) |
| Welke EU-oppositieprocedure in het Spaans behandelde weigering wegens verwarringsgevaar tussen een tweeletterig figuratief teken en beeldmerken zoals NLJEANS? (158 chars) | Gemeenschapsmerk Oppositieprocedure Ouder communautair beeldmerk dat lettercombinatie „NL” bevat Aanvragen tot inschrijving als gemeenschapsmerk van beeldmerken die termen „NLSPORT”, „NLJEANS”, „NLACTIVE” en „NLCollection” be ... [truncated 225 chars](688 chars) |
| Welke herziening 17/28 februari 1986 schiep een afzonderlijk ecologisch hoofdstuk om een lacune in het Verdrag van Rome te dichten? (131 chars) | Deze eis van een duidelijke en bijgevolg internationaal controleerbare rechtsgrond kan in politiek opzicht ook worden opgevat als een ontegenzeglijk constitutioneel signaal dat er behoefte bestaat aan een consumentenbeleid. H ... [truncated 225 chars](765 chars) |

## Dataset Information

| Field | Value |
| --- | --- |
| Nano set | NanoMuPLeR |
| Backing dataset | NanoMuPLeR |
| Task / split | nl |
| Hugging Face dataset | [hakari-bench/NanoMuPLeR](https://huggingface.co/datasets/hakari-bench/NanoMuPLeR) |
| Source dataset | [mteb/MuPLeR-retrieval](https://huggingface.co/datasets/mteb/MuPLeR-retrieval) |
| Language | nl |
| Category | natural_language |
| Queries | 200 |
| Documents | 10,000 |
| Positive qrels | 200 |
| BM25 nDCG@10 | 0.8909 |
| BM25 hit@10 | 0.9400 |
| BM25 Recall@100 | 0.9750 |
| BM25 candidate subset | top-500 (`bm25`) |
| Dense nDCG@10 | 0.8580 |
| Dense hit@10 | 0.9200 |
| Dense Recall@100 | 0.9500 |
| Dense candidate subset | top-500 (`harrier_oss_v1_270m`) |
| Reranking hybrid nDCG@10 | 0.9072 |
| Reranking hybrid hit@10 | 0.9650 |
| Reranking hybrid Recall@100 | 1.0000 |
| Reranking hybrid candidate subset | top-100 plus optional rank-101 safeguard (`reranking_hybrid`) |
| Reranking hybrid candidates / query | 100 |
| Reranking hybrid safeguard rows | 0 |
| Query length avg chars | 147.87 |
| Document length avg chars | 716.33 |

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
  task_name: nl
  split_name: nl
  language: nl
  category: natural_language
  document_path: docs/benchmark_tasks/NanoMuPLeR/nl.md
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
    query_mean: 147.87
    document_mean: 716.33
  bm25:
    ndcg_at_10: 0.8909223767598407
    hit_at_10: 0.94
    source: dataset_candidate_subset
  example_count: 5
  candidate_subsets:
    bm25:
      config: bm25
      label: BM25
      source: dataset_candidate_subset
      top_k: 500
      ndcg_at_10: 0.8909223768
      hit_at_10: 0.94
      recall_at_100: 0.975
      candidate_count_min: 500
      candidate_count_max: 500
      candidate_count_mean: 500.0
      query_count: 200
      query_coverage: 1.0
      relevant_coverage_at_100: 0.975
    dense:
      config: harrier_oss_v1_270m
      label: Dense
      source: dataset_candidate_subset
      top_k: 500
      ndcg_at_10: 0.8579836567
      hit_at_10: 0.92
      recall_at_100: 0.95
      candidate_count_min: 500
      candidate_count_max: 500
      candidate_count_mean: 500.0
      query_count: 200
      query_coverage: 1.0
      relevant_coverage_at_100: 0.95
    reranking_hybrid:
      config: reranking_hybrid
      label: Reranking hybrid
      source: dataset_candidate_subset
      top_k: 100
      ndcg_at_10: 0.9072249515
      hit_at_10: 0.965
      recall_at_100: 1.0
      candidate_count_min: 100
      candidate_count_max: 100
      candidate_count_mean: 100.0
      query_count: 200
      query_coverage: 1.0
      relevant_coverage_at_100: 1.0
      safeguard_positive_rows: 0
      rows_with_101_candidates: 0
```
