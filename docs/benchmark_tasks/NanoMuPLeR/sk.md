# NanoMuPLeR / sk

## Overview

`NanoMuPLeR / sk` is the Slovak split of MuPLeR-retrieval. Synthetic Slovak
legal questions retrieve Slovak EU-law passages from a DGT-Acquis-derived
parallel corpus. The task is single-positive legal passage retrieval.

## Details

### What the Original Data Measures

The [MuPLeR-retrieval dataset card](https://huggingface.co/datasets/mteb/MuPLeR-retrieval)
describes DGT-Acquis-derived legal passages and synthetic parallel queries in
14 European languages. [An overview of the European Union's highly multilingual parallel corpora](https://link.springer.com/article/10.1007/s10579-014-9277-0)
serves as the cited source reference for those EU corpora.

### Observed Data Profile

The split has 200 Slovak queries, 10,000 documents, and 200 positive qrels.
Queries average 136.25 characters and documents average 628.24 characters. The
examples are EU legal questions about import taxes, state aid, procurement,
nuclear policy, and accession-era production rules.

### BM25 Difficulty

BM25 reaches nDCG@10 = 0.7041 and hit@10 = 0.7850, with 128 positives at rank 1
and 157 in the top 10. Lexical retrieval is strong but not as strong as in Dutch
or Latvian; Slovak morphology and wording variation can separate query terms
from passage terms.

### Training Data That May Help

Useful data includes non-overlapping Slovak EUR-Lex/DGT-Acquis retrieval,
Slovak legal QA, multilingual legal bitext, and hard negatives from adjacent EU
acts. Exclude MuPLeR evaluation examples and their parallel equivalents.

### Synthetic Data Guidance

Generate Slovak questions from non-evaluation EU legal passages. Preserve legal
entities, dates, treaty concepts, and numeric values; construct negatives that
share the legal topic but do not satisfy the query.

## Example Data

| Query | Positive document |
| --- | --- |
| Ktorá trojstupňová intervenčná schéma sa navrhuje spolu s podporou duševného zdravia, udržiavaním zdravého životného štýlu a prostrediami podporujúcimi sebarealizáciu? (167 chars) | Z tohto hľadiska je potrebné zdôrazniť tri zložky prevencie (primárnu, sekundárnu a terciárnu) a prispôsobiť ich danej oblasti. Je potrebné vypracovať iniciatívy pre viaceré oblasti, vrátane podpory duševného zdravia a inform ... [truncated 225 chars](500 chars) |
| Ktorý výbor vyzval na opatrenia podporované EÚ na nápravu nedostatkov kvalifikácie a etiky vedúcich po strate dôvery zamestnancov a spotrebiteľov? (146 chars) | Kríza spojená so stratou dôvery sa medzi zamestnancami a spotrebiteľmi v mnohých krajinách Európskeho spoločenstva zhoršila po odhalení chýb a nesprávneho počínania riadiacich pracovníkov a celých riadiacich štruktúr. Výbor p ... [truncated 225 chars](681 chars) |
| Ktorý orgán vysvetľuje politiku pri neriešenej judikatúre bez prejudikácie výkladu ods. 1 a 3 zmluvy regionálnymi a súdmi Spoločenstva? (135 chars) | Vzhľadom na niekoľko otázok v týchto usmerneniach je načrtnutý súčasný stav judikatúry Súdneho dvora EZVO a Súdneho dvora Európskych spoločenstiev v súlade so zodpovedajúcimi ustanoveniami v Zmluve o ES. Dozorný úrad EZVO má ... [truncated 225 chars](644 chars) |
| Ktorý dohľadový orgán poskytol samostatné riešenie na riadenie pohybu a neskôr v roku 2006 kontroloval preraďovanie tovaru medzi režimami? (138 chars) | Na začiatku projektu NCTS niekoľko členských štátov, ktoré si nechceli vypracovať vnútroštátnu aplikáciu pre oblasť tranzitu, požiadali Komisiu, aby vyvinula štandardnú aplikáciu. MCC vytvorená Komisiou je samostatným systémo ... [truncated 225 chars](817 chars) |
| Ako európske podnikové výbory zakotvujú záväzky spoločenskej zodpovednosti podnikov prostredníctvom dobrovoľného vyjednávania, vrátane subdodávateľských pracovníkov na pracovisku a dodávateľov? (193 chars) | Rozhodujúcim krokom na európskej úrovni je dobrovoľné a/alebo vyjednané stanovenie záväzkov týkajúcich sa SZP vo všetkých nadnárodných spoločnostiach, ktoré majú európsky podnikový výbor. Týmto spôsobom sa môžu do tohto dynam ... [truncated 225 chars](834 chars) |

## Dataset Information

| Field | Value |
| --- | --- |
| Nano set | NanoMuPLeR |
| Backing dataset | NanoMuPLeR |
| Task / split | sk |
| Hugging Face dataset | [hakari-bench/NanoMuPLeR](https://huggingface.co/datasets/hakari-bench/NanoMuPLeR) |
| Source dataset | [mteb/MuPLeR-retrieval](https://huggingface.co/datasets/mteb/MuPLeR-retrieval) |
| Language | sk |
| Category | natural_language |
| Queries | 200 |
| Documents | 10,000 |
| Positive qrels | 200 |
| BM25 nDCG@10 | 0.7041 |
| BM25 hit@10 | 0.7850 |
| Query length avg chars | 136.25 |
| Document length avg chars | 628.24 |

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
  task_name: sk
  split_name: sk
  language: sk
  category: natural_language
  document_path: docs/benchmark_tasks/NanoMuPLeR/sk.md
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
    query_mean: 136.25
    document_mean: 628.24
  bm25:
    ndcg_at_10: 0.7041
    hit_at_10: 0.785
    source: dataset_bm25_column
  example_count: 5
```
