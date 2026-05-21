# NanoMuPLeR / en

## Overview

`NanoMuPLeR / en` is the English split of MuPLeR-retrieval. Queries are
synthetic English legal questions, and documents are English EU-law passages
derived from DGT-Acquis. The model must retrieve the single passage that grounds
the legal condition, institution, date, threshold, or procedural rule named in
the query.

## Details

### What the Original Data Measures

The [MuPLeR-retrieval dataset card](https://huggingface.co/datasets/mteb/MuPLeR-retrieval)
states that the dataset is a multilingual parallel legal retrieval benchmark
with 10,000 DGT-Acquis passages and 200 synthetic parallel queries in each of 14
languages. [An overview of the European Union's highly multilingual parallel corpora](https://link.springer.com/article/10.1007/s10579-014-9277-0)
explains the EU parallel resources and their intended reuse, including
DGT-Acquis as a reference publication.

### Observed Data Profile

The split has 200 queries, 10,000 documents, and 200 positive qrels. Every query
has one positive. Queries average 134.87 characters and documents average 650.58
characters. Sampled questions cover capital duty, state-aid compensation,
procurement prequalification, Euratom priorities, and pre-accession production
abatement rules.

### BM25 Difficulty

BM25 reaches nDCG@10 = 0.5994 and hit@10 = 0.7100, with 99 positives at rank 1
and 142 in the top 10. The English wording is still legally specific, but the
queries are more abstractive than simple title lookup, so BM25 misses some
positives despite strong entity and number overlap.

### Training Data That May Help

Useful data includes non-overlapping English EUR-Lex and DGT-Acquis retrieval
pairs, legal QA, multilingual parallel legal alignment data, and hard negatives
from similar EU provisions. Training should exclude the MuPLeR evaluation
queries and exact positive passages.

### Synthetic Data Guidance

Generate English legal questions from non-evaluation EU passages. Preserve
article numbers, dates, percentages, treaty concepts, and institutional roles.
Synthetic negatives should come from legally adjacent passages that share terms
but do not answer the query.

## Example Data

| Query | Positive document |
| --- | --- |
| Which oversight body supplied a standalone movement-management solution while later inspecting countries' cross-regime goods controls in 2006? (142 chars) | In the beginning of the NCTS project several Member States not wishing to develop a national transit application requested the Commission to produce a standard one. MCC as supplied by the Commission is a stand alone applicati ... [truncated 225 chars](799 chars) |
| Which committee urged EU-backed measures to remedy leadership skill and ethics failings after misconduct undermined workforce and customer confidence? (150 chars) | The crisis of confidence among employees and consumers is made worse in many countries of the European Union by revelations about mistakes and impropriety on the part of managers and entire management structures. The Committe ... [truncated 225 chars](695 chars) |
| Which rationale links consensus on sector growth caps to both environmental resilience and long-term market competitiveness and youth job creation? (147 chars) | The arguments presented in the communication in support of the Agenda seem appropriate, in that they assess both the economic impact of tourism and its ability to create jobs for young people and also the necessary balance be ... [truncated 225 chars](707 chars) |
| What does the EU executive do when pro-rated, category-specific inflows exceed set thresholds over a minimum three-month period? (128 chars) | On the basis of the monitoring of imports that it is carrying out in accordance with the provisions of Council Regulation (EEC) No 3030/93, the Commission will be examining regularly whether some indicative thresholds of actu ... [truncated 225 chars](754 chars) |
| Who retains co-signing authority on the dual-signatory interest-bearing account to ensure proper disbursement? (110 chars) | In addition to these funds, there are other STABEX funds held by beneficiary ACP States. Once the Commission and the beneficiary (ACP) State have reached agreement on how the STABEX funds are to be utilised, a transfer conven ... [truncated 225 chars](745 chars) |

## Dataset Information

| Field | Value |
| --- | --- |
| Nano set | NanoMuPLeR |
| Backing dataset | NanoMuPLeR |
| Task / split | en |
| Hugging Face dataset | [hakari-bench/NanoMuPLeR](https://huggingface.co/datasets/hakari-bench/NanoMuPLeR) |
| Source dataset | [mteb/MuPLeR-retrieval](https://huggingface.co/datasets/mteb/MuPLeR-retrieval) |
| Language | en |
| Category | natural_language |
| Queries | 200 |
| Documents | 10,000 |
| Positive qrels | 200 |
| BM25 nDCG@10 | 0.5994 |
| BM25 hit@10 | 0.7100 |
| Query length avg chars | 134.87 |
| Document length avg chars | 650.58 |

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
  task_name: en
  split_name: en
  language: en
  category: natural_language
  document_path: docs/benchmark_tasks/NanoMuPLeR/en.md
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
    query_mean: 134.87
    document_mean: 650.58
  bm25:
    ndcg_at_10: 0.5994
    hit_at_10: 0.71
    source: dataset_bm25_column
  example_count: 5
```
