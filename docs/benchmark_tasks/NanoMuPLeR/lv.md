# NanoMuPLeR / lv

## Overview

`NanoMuPLeR / lv` is the Latvian split of MuPLeR-retrieval. Synthetic Latvian
legal questions are matched against Latvian DGT-Acquis-derived EU legal
passages. The task measures single-positive legal passage retrieval in a
multilingual parallel corpus setting.

## Details

### What the Original Data Measures

The [MuPLeR-retrieval dataset card](https://huggingface.co/datasets/mteb/MuPLeR-retrieval)
states that the benchmark contains DGT-Acquis passages and synthetic parallel
queries across 14 languages. [An overview of the European Union's highly multilingual parallel corpora](https://link.springer.com/article/10.1007/s10579-014-9277-0)
is the source reference for the European Union parallel resources.

### Observed Data Profile

The split has 200 Latvian queries, 10,000 documents, and 200 positive qrels.
Queries average 140.47 characters and documents average 608.95 characters.
Sampled examples cover EU import duties, state aid, procurement criteria,
Euratom research, and pre-accession reductions.

### BM25 Difficulty

BM25 is very strong: nDCG@10 = 0.8376 and hit@10 = 0.8900. It ranks 157
positives first and 178 in the top 10. The high score reflects the many shared
legal terms, numbers, and named institutions between queries and passages.

### Training Data That May Help

Useful data includes non-overlapping Latvian legal retrieval pairs, Latvian
EUR-Lex text, DGT-Acquis parallel data, and multilingual legal QA. The MuPLeR
evaluation pairs should be excluded from training and synthetic generation
seeds.

### Synthetic Data Guidance

Generate Latvian legal questions from non-evaluation EU passages. Keep precise
conditions, percentages, dates, and legal terminology, and create hard negatives
from adjacent EU provisions.

## Example Data

| Query | Positive document |
| --- | --- |
| Kura Savienības norma paredz ņemt vērā nodarbinātības veicināšanu, sociālo aizsardzību, izslēgtības apkarošanu, izglītību un veselību? (134 chars) | Tas, piemēram, ir gadījums sociālajā politikā, kur tika ietverts vispārēji piemērojams noteikums (tā sauktā sociālā klauzula), pēc kura Savienībai, nosakot un īstenojot politiku un pasākumus, ir jārēķinās ar prasībām saistībā ... [truncated 225 chars](719 chars) |
| Kā priekšlikumos plānot esošo digitālās kompetences projektu ilgtspējīgu izplatīšanu, nosaucot starpniekus un iekļaujot naratīvus un skaitliskus rādītājus? (155 chars) | Priekšlikumos jākoncentrējas uz esošo digitālās kompetences projektu, darbību vai instrumentu rezultātu efektīvu un ilgtspējīgu izplatīšanu un izmantošanu. Īpašs uzsvars jāliek uz mērķgrupu un to vajadzību precīzu noskaidroša ... [truncated 225 chars](624 chars) |
| Kura komiteja secināja, ka resursu piešķiršana maznozīmīgām iekšējām izmeklēšanām ir neefektīva un aicināja iekļaut atlases kritērijus operatīvo procedūru rokasgrāmatā? (168 chars) | Uzraudzības komiteja izvērtēja OLAF de minimis politiku un pārbaudīja 45 izvēlētas lietas, kuru aplēstā finansiālā ietekme nepārsniedz EUR 50000. Uzraudzības komiteja secināja, ka OLAF resursu piešķiršana maznozīmīgām iekšējā ... [truncated 225 chars](576 chars) |
| Kura ES konsultatīvā komiteja atbalsta Komisijas pūles iekļaut veselības un sociālās ietekmes akcīzes nodokļos par tabakas izstrādājumiem? (138 chars) | Kaut arī sākotnēji akcīzes nodokļa, ar ko apliek tabaku, galvenais mērķis bija tikai fiskāls, mūsdienu pasaulē tā funkcijas mainās, un šis nodoklis arvien vairāk kļūst par sabiedrības veselības un sociālās politikas instrumen ... [truncated 225 chars](666 chars) |
| Kurš regulējums ļāva iestādēm atzīt uzņēmumus par dominējošiem ar aptuveni 25% tirgus daļas, ņemot vērā klientu piekļuvi un finanšu spēku? (138 chars) | Saskaņā ar 1998. gada reglamentējošiem noteikumiem attiecīgajās direktīvās tika noteiktas telekomunikāciju sektora tirgus jomas, kuras bija saskaņā ar ex ante regulu, bet nebija saskaņā ar konkurences tiesību principiem notei ... [truncated 225 chars](684 chars) |

## Dataset Information

| Field | Value |
| --- | --- |
| Nano set | NanoMuPLeR |
| Backing dataset | NanoMuPLeR |
| Task / split | lv |
| Hugging Face dataset | [hakari-bench/NanoMuPLeR](https://huggingface.co/datasets/hakari-bench/NanoMuPLeR) |
| Source dataset | [mteb/MuPLeR-retrieval](https://huggingface.co/datasets/mteb/MuPLeR-retrieval) |
| Language | lv |
| Category | natural_language |
| Queries | 200 |
| Documents | 10,000 |
| Positive qrels | 200 |
| BM25 nDCG@10 | 0.8376 |
| BM25 hit@10 | 0.8900 |
| BM25 Recall@100 | 0.9700 |
| BM25 candidate subset | top-500 (`bm25`) |
| Dense nDCG@10 | 0.7910 |
| Dense hit@10 | 0.8750 |
| Dense Recall@100 | 0.9550 |
| Dense candidate subset | top-500 (`harrier_oss_v1_270m`) |
| Reranking hybrid nDCG@10 | 0.8672 |
| Reranking hybrid hit@10 | 0.9450 |
| Reranking hybrid Recall@100 | 1.0000 |
| Reranking hybrid candidate subset | top-100 plus optional rank-101 safeguard (`reranking_hybrid`) |
| Reranking hybrid candidates / query | 100 |
| Reranking hybrid safeguard rows | 0 |
| Query length avg chars | 140.47 |
| Document length avg chars | 608.95 |

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
  task_name: lv
  split_name: lv
  language: lv
  category: natural_language
  document_path: docs/benchmark_tasks/NanoMuPLeR/lv.md
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
    query_mean: 140.47
    document_mean: 608.95
  bm25:
    ndcg_at_10: 0.8376037479700317
    hit_at_10: 0.89
    source: dataset_candidate_subset
  example_count: 5
  candidate_subsets:
    bm25:
      config: bm25
      label: BM25
      source: dataset_candidate_subset
      top_k: 500
      ndcg_at_10: 0.837603748
      hit_at_10: 0.89
      recall_at_100: 0.97
      candidate_count_min: 500
      candidate_count_max: 500
      candidate_count_mean: 500.0
      query_count: 200
      query_coverage: 1.0
      relevant_coverage_at_100: 0.97
    dense:
      config: harrier_oss_v1_270m
      label: Dense
      source: dataset_candidate_subset
      top_k: 500
      ndcg_at_10: 0.7910408726
      hit_at_10: 0.875
      recall_at_100: 0.955
      candidate_count_min: 500
      candidate_count_max: 500
      candidate_count_mean: 500.0
      query_count: 200
      query_coverage: 1.0
      relevant_coverage_at_100: 0.955
    reranking_hybrid:
      config: reranking_hybrid
      label: Reranking hybrid
      source: dataset_candidate_subset
      top_k: 100
      ndcg_at_10: 0.8671887191
      hit_at_10: 0.945
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
