# NanoMuPLeR / it

## Overview

`NanoMuPLeR / it` is the Italian split of MuPLeR-retrieval. Synthetic Italian
queries retrieve Italian EU legal passages from a DGT-Acquis-derived corpus. The
task is focused legal passage retrieval rather than broad web search: each query
has one intended passage.

## Details

### What the Original Data Measures

The [MuPLeR-retrieval dataset card](https://huggingface.co/datasets/mteb/MuPLeR-retrieval)
describes multilingual parallel legal retrieval using DGT-Acquis passages and
parallel synthetic queries. [An overview of the European Union's highly multilingual parallel corpora](https://link.springer.com/article/10.1007/s10579-014-9277-0)
is the cited reference for the source EU multilingual corpora.

### Observed Data Profile

The split has 200 Italian queries, 10,000 documents, and 200 positive qrels.
Queries average 140.77 characters and documents average 726.14 characters.
The sampled data covers EU import taxes, state-aid criteria, procurement
selection versus award criteria, Euratom controls, and pre-accession reduction
rules.

### BM25 Difficulty

BM25 reaches nDCG@10 = 0.7920 and hit@10 = 0.8750, with 142 positives at rank 1
and 175 in the top 10. Italian legal text preserves many highly distinctive
terms, names, numbers, and dates, so lexical retrieval is strong but not
perfect.

### Training Data That May Help

Useful data includes non-overlapping Italian EU legal retrieval pairs, Italian
EUR-Lex questions, multilingual legal bitext, and hard negatives from related
EU legal passages. Do not train on the evaluation queries or exact positives.

### Synthetic Data Guidance

Generate Italian questions grounded in non-evaluation EU legal passages. Keep
the formal legal relation explicit, and include near negatives that share
institutions or legal fields but not the requested condition.

## Example Data

| Query | Positive document |
| --- | --- |
| Quale opposizione UE in spagnolo riguardò diniego per somiglianza tra segno figurativo di due lettere e marchi per abbigliamento? (129 chars) | «Marchio comunitario Procedura di opposizione Marchio comunitario figurativo anteriore contenente la combinazione di lettere “NL”Domande di marchi comunitari figurativi contenenti i termini “NLSPORT”, “NLJEANS”, “NLACTIVE” e ... [truncated 225 chars](553 chars) |
| Quale salume il cui nome etimologicamente deriva da termini per cacciatori e indica razioni portatili a lunga conservazione? (124 chars) | Il nome kiełbasa myśliwska indica la natura specifica del prodotto. Il carattere specifico del prodotto è testimoniato dall'etimologia del nome che deriva da myśliwy (cacciatore), myślistwo (caccia) ed indica la destinazione ... [truncated 225 chars](635 chars) |
| Quale schema d'intervento a tre livelli è proposto insieme a promuovere benessere psicologico, mantenimento stili di vita e contesti favorevoli? (144 chars) | Da questo punto di vista va posto l'accento sulla prevenzione, o sulla sua componente primaria, secondaria e terziaria più adatta al settore interessato. Devono essere sviluppati gli interventi di promozione della salute ment ... [truncated 225 chars](600 chars) |
| Quando è stata notificata alla Commissione europea la spesa cofinanziata per il controllo di patogeni alimentari nei polli da carne? (132 chars) | L’obiettivo dell’aiuto è l’attuazione del programma di controllo della salmonella negli allevamenti di polli da carne, in conformità alle disposizioni della normativa comunitaria [regolamento (CE) n. 1168/2006]. Questa malatt ... [truncated 225 chars](683 chars) |
| Quali razze ovine pure da latte di montagna forniscono il ceppo materno per l'agnello da latte legato al pascolo stagionale? (124 chars) | L'agnello da latte dei Pirenei nasce da tre razze locali da latte. Le madri sono di pura razza basco-bearnese, Manech testa nera o Manech testa rossa. Grazie alla loro conformazione fisica e morfologica, tali razze rustiche b ... [truncated 225 chars](617 chars) |

## Dataset Information

| Field | Value |
| --- | --- |
| Nano set | NanoMuPLeR |
| Backing dataset | NanoMuPLeR |
| Task / split | it |
| Hugging Face dataset | [hakari-bench/NanoMuPLeR](https://huggingface.co/datasets/hakari-bench/NanoMuPLeR) |
| Source dataset | [mteb/MuPLeR-retrieval](https://huggingface.co/datasets/mteb/MuPLeR-retrieval) |
| Language | it |
| Category | natural_language |
| Queries | 200 |
| Documents | 10,000 |
| Positive qrels | 200 |
| BM25 nDCG@10 | 0.7920 |
| BM25 hit@10 | 0.8750 |
| BM25 Recall@100 | 0.9500 |
| BM25 candidate subset | top-500 (`bm25`) |
| Dense nDCG@10 | 0.8257 |
| Dense hit@10 | 0.9200 |
| Dense Recall@100 | 0.9750 |
| Dense candidate subset | top-500 (`harrier_oss_v1_270m`) |
| Reranking hybrid nDCG@10 | 0.8422 |
| Reranking hybrid hit@10 | 0.9250 |
| Reranking hybrid Recall@100 | 0.9950 |
| Reranking hybrid candidate subset | top-100 plus optional rank-101 safeguard (`reranking_hybrid`) |
| Reranking hybrid candidates / query | 100-101 |
| Reranking hybrid safeguard rows | 1 |
| Query length avg chars | 140.77 |
| Document length avg chars | 726.14 |

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
  task_name: it
  split_name: it
  language: it
  category: natural_language
  document_path: docs/benchmark_tasks/NanoMuPLeR/it.md
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
    query_mean: 140.77
    document_mean: 726.14
  bm25:
    ndcg_at_10: 0.7919713166303611
    hit_at_10: 0.875
    source: dataset_candidate_subset
  example_count: 5
  candidate_subsets:
    bm25:
      config: bm25
      label: BM25
      source: dataset_candidate_subset
      top_k: 500
      ndcg_at_10: 0.7919713166
      hit_at_10: 0.875
      recall_at_100: 0.95
      candidate_count_min: 500
      candidate_count_max: 500
      candidate_count_mean: 500.0
      query_count: 200
      query_coverage: 1.0
      relevant_coverage_at_100: 0.95
    dense:
      config: harrier_oss_v1_270m
      label: Dense
      source: dataset_candidate_subset
      top_k: 500
      ndcg_at_10: 0.825667523
      hit_at_10: 0.92
      recall_at_100: 0.975
      candidate_count_min: 500
      candidate_count_max: 500
      candidate_count_mean: 500.0
      query_count: 200
      query_coverage: 1.0
      relevant_coverage_at_100: 0.975
    reranking_hybrid:
      config: reranking_hybrid
      label: Reranking hybrid
      source: dataset_candidate_subset
      top_k: 100
      ndcg_at_10: 0.8422302467
      hit_at_10: 0.925
      recall_at_100: 0.995
      candidate_count_min: 100
      candidate_count_max: 101
      candidate_count_mean: 100.005
      query_count: 200
      query_coverage: 1.0
      relevant_coverage_at_100: 0.995
      safeguard_positive_rows: 1
      rows_with_101_candidates: 1
```
