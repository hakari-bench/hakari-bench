# NanoMuPLeR / sl

## Overview

`NanoMuPLeR / sl` is the Slovenian split of MuPLeR-retrieval. It matches
synthetic Slovenian EU-law questions to Slovenian DGT-Acquis-derived passages.
The task tests focused legal retrieval with one positive passage per query.

## Details

### What the Original Data Measures

The [MuPLeR-retrieval dataset card](https://huggingface.co/datasets/mteb/MuPLeR-retrieval)
describes a 14-language parallel legal retrieval dataset based on DGT-Acquis
passages and synthetic questions. [An overview of the European Union's highly multilingual parallel corpora](https://link.springer.com/article/10.1007/s10579-014-9277-0)
is the cited reference for DGT-Acquis and related EU corpora.

### Observed Data Profile

The split has 200 Slovenian queries, 10,000 documents, and 200 positive qrels.
Queries average 136.35 characters and documents average 607.82 characters.
The examples ask about import taxes, state-aid compensation, procurement
criteria, Euratom priorities, and pre-accession production reductions.

### BM25 Difficulty

BM25 reaches nDCG@10 = 0.7455 and hit@10 = 0.8350, with 132 positives at rank 1
and 167 in the top 10. Lexical matching is strong due to shared dates, numbers,
and legal terminology, but not enough to solve every query.

### Training Data That May Help

Useful training data includes Slovenian EU legal retrieval pairs, Slovenian
EUR-Lex text, multilingual legal bitext, and hard negatives from adjacent EU
provisions. Avoid MuPLeR evaluation query-passage pairs.

### Synthetic Data Guidance

Generate Slovenian questions from non-evaluation EU legal passages. Preserve
formal legal relations, dates, percentages, and named institutions; add
near-topic negatives that do not answer the same condition.

## Example Data

| Query | Positive document |
| --- | --- |
| Kateri regulativni okvir je organom omogočal opredeliti podjetja kot prevladujoča pri 25% tržnem deležu, upoštevajoč dostop končnih uporabnikov in finance? (155 chars) | V skladu z regulativnim okvirom iz leta 1998 so bila področja trga telekomunikacijskega sektorja, za katera je veljala ureditev ex ante, določena v ustreznih direktivah, vendar ti trgi niso bili opredeljeni v skladu z načeli ... [truncated 225 chars](775 chars) |
| Katere države so v raziskavi zabeležile približno štiri petine podpore za omejitev manjših apoenov? (99 chars) | Bankovci in kovanci. Glede zadovoljstva s sedanjimi apoeni bankovcev in kovancev, je raziskava pokazala, da pri bankovcih spremembe niso potrebne, precejšen odstotek anketirancev (od 80 % na Finskem in v Nemčiji do 33–35 % na ... [truncated 225 chars](576 chars) |
| Kateri segment embalaže za pijačo v razpravah v EU predstavlja približno petino skupne embalaže po teži? (104 chars) | Nacionalni sistemi za ponovno uporabo embalaže upoštevajo več vrst embalaže. Nekateri od teh sistemov delujejo zelo dobro, zlasti tisti za prevozno embalažo, kakršne so gajbe in palete, pa tudi za embalaže za pijačo v gostins ... [truncated 225 chars](524 chars) |
| Kateri delež nacionalne oskrbe bonbonov trgovcem na drobno obvladuje dajalec franšize? (86 chars) | Trgovci na drobno, ki prodajajo bonbone, jih kupujejo na nacionalnem trgu pri nacionalnih proizvajalcih, ki nudijo nacionalne okuse, ali pri trgovcih na debelo, ki ob tem, da prodajajo bonbone nacionalnih proizvajalcev, uvaža ... [truncated 225 chars](740 chars) |
| Katera združitev leta 2004 ni ustvarila prevladujočega nacionalnega igralca in ni zaprla trga za spletne prodajalce pesmi ali proizvajalce naprav? (146 chars) | Medtem ko je bila industrija glasbenih posnetkov koncentrirana že pred združitvijo v letu 2004, tržni deleži družbe Sony BMG ostajajo nižji od vrednosti, ki bi načelno pomenile posamični prevladujoči položaj na katerem koli o ... [truncated 225 chars](620 chars) |

## Dataset Information

| Field | Value |
| --- | --- |
| Nano set | NanoMuPLeR |
| Backing dataset | NanoMuPLeR |
| Task / split | sl |
| Hugging Face dataset | [hakari-bench/NanoMuPLeR](https://huggingface.co/datasets/hakari-bench/NanoMuPLeR) |
| Source dataset | [mteb/MuPLeR-retrieval](https://huggingface.co/datasets/mteb/MuPLeR-retrieval) |
| Language | sl |
| Category | natural_language |
| Queries | 200 |
| Documents | 10,000 |
| Positive qrels | 200 |
| BM25 nDCG@10 | 0.7455 |
| BM25 hit@10 | 0.8350 |
| BM25 Recall@100 | 0.9000 |
| BM25 candidate subset | top-500 (`bm25`) |
| Dense nDCG@10 | 0.7428 |
| Dense hit@10 | 0.8250 |
| Dense Recall@100 | 0.9250 |
| Dense candidate subset | top-500 (`harrier_oss_v1_270m`) |
| Reranking hybrid nDCG@10 | 0.7983 |
| Reranking hybrid hit@10 | 0.8950 |
| Reranking hybrid Recall@100 | 0.9750 |
| Reranking hybrid candidate subset | top-100 plus optional rank-101 safeguard (`reranking_hybrid`) |
| Reranking hybrid candidates / query | 100-101 |
| Reranking hybrid safeguard rows | 5 |
| Query length avg chars | 136.35 |
| Document length avg chars | 607.82 |

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
  task_name: sl
  split_name: sl
  language: sl
  category: natural_language
  document_path: docs/benchmark_tasks/NanoMuPLeR/sl.md
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
    query_mean: 136.35
    document_mean: 607.82
  bm25:
    ndcg_at_10: 0.745487658907861
    hit_at_10: 0.835
    source: dataset_candidate_subset
  example_count: 5
  candidate_subsets:
    bm25:
      config: bm25
      label: BM25
      source: dataset_candidate_subset
      top_k: 500
      ndcg_at_10: 0.7454876589
      hit_at_10: 0.835
      recall_at_100: 0.9
      candidate_count_min: 500
      candidate_count_max: 500
      candidate_count_mean: 500.0
      query_count: 200
      query_coverage: 1.0
      relevant_coverage_at_100: 0.9
    dense:
      config: harrier_oss_v1_270m
      label: Dense
      source: dataset_candidate_subset
      top_k: 500
      ndcg_at_10: 0.7428244393
      hit_at_10: 0.825
      recall_at_100: 0.925
      candidate_count_min: 500
      candidate_count_max: 500
      candidate_count_mean: 500.0
      query_count: 200
      query_coverage: 1.0
      relevant_coverage_at_100: 0.925
    reranking_hybrid:
      config: reranking_hybrid
      label: Reranking hybrid
      source: dataset_candidate_subset
      top_k: 100
      ndcg_at_10: 0.7983366238
      hit_at_10: 0.895
      recall_at_100: 0.975
      candidate_count_min: 100
      candidate_count_max: 101
      candidate_count_mean: 100.025
      query_count: 200
      query_coverage: 1.0
      relevant_coverage_at_100: 0.975
      safeguard_positive_rows: 5
      rows_with_101_candidates: 5
```
