# MNanoBEIR / NanoBEIR-sr / NanoNFCorpus

## Overview

NFCorpus is a biomedical and nutrition information retrieval task.
`NanoBEIR-sr__NanoNFCorpus` uses Serbian translated health queries to retrieve
Serbian translated scientific or medical passages.

## Details

### What the Original Data Measures

[NFCorpus](https://www.cl.uni-heidelberg.de/~riezler/publications/papers/ECIR2016.pdf)
was built from nutrition and health information needs with expert relevance
judgments. BEIR includes it as domain-specific retrieval, and MMTEB gives the
multilingual context.

### Observed Data Profile

The sampled task has 50 queries, 2,953 documents, and 1,651 positive qrels.
Nearly all queries are multi-positive, averaging 33.02 positives. Queries
average 23.08 characters; documents average 1,522.71 characters.

### BM25 Difficulty

BM25 reaches nDCG@10 = 0.2342 and hit@10 = 0.4600. The median first-positive
rank is 25.5, so Serbian biomedical retrieval is lexically difficult in this
sample despite many relevant documents.

### Training Data That May Help

Useful data includes non-overlapping biomedical retrieval, Serbian medical QA,
scientific abstract retrieval, and multi-positive relevance training. Exclude
NFCorpus, BEIR, NanoBEIR, and overlapping translated abstracts.

### Synthetic Data Guidance

Generate Serbian consumer-health or biomedical keyword queries from scientific
passages. Use multiple positives per query when several documents discuss the
same condition, intervention, or outcome.

## Example Data

| Query | Positive document |
| --- | --- |
| Zdrav čokoladni milkshake (25 chars) | Cilj Ispitati odnos između unosa trešanja i rizika od ponovljenih napada gihta kod osoba sa gihtom. Metode Sproveli smo studiju preseka slučajeva kako bismo ispitali povezanost niza pretpostavljenih faktora rizika s ponovljen ... [truncated 225 chars](1596 chars) |
| medicinska etika (16 chars) | POZADINA: Jedan od glavnih problema u kontroli holesterola u krvi putem dijetetskih mera čini se potreba za poboljšanjem pridržavanja pacijenata preporukama. CILJEVI: Ispitati brojna pitanja u vezi s preprekama i motivatorima ... [truncated 225 chars](1853 chars) |
| grah (4 chars) | Tokom proteklih 20 godina, rastući interes za biohemiju, ishranu i farmakologiju L-arginina doveo je do opsežnih studija koje istražuju njegovu nutritivnu i terapeutsku ulogu u lečenju i prevenciji metaboličkih poremećaja kod ... [truncated 225 chars](1179 chars) |
| Šta se zapravo nalazi u pilećim nuggetsima? (43 chars) | NAMENA: Utvrditi sastav pilećih nugeta iz 2 nacionalna lanca prehrambenih prodavnica. POZADINA: Pileći nugeti su postali glavna komponenta američke ishrane. Želeli smo da utvrdimo trenutni sastav ove visoko preradjene hrane. ... [truncated 225 chars](718 chars) |
| zasićena mast (13 chars) | Povećan je interes za mogućnost da ishrana majke tokom trudnoće može uticati na razvoj alergijskih oboljenja kod dece. Ova prospektivna studija ispitivala je povezanost unosa odabrane hrane bogate masnim kiselinama i specifič ... [truncated 225 chars](1942 chars) |

## Dataset Information

| Field | Value |
| --- | --- |
| Nano set | MNanoBEIR |
| Backing dataset | NanoBEIR-sr |
| Task / split | NanoNFCorpus |
| Hugging Face dataset | [hakari-bench/NanoBEIR-sr](https://huggingface.co/datasets/hakari-bench/NanoBEIR-sr) |
| Language | sr |
| Category | natural_language |
| Queries | 50 |
| Documents | 2,953 |
| Positive qrels | 1,651 |
| Positives per query avg | 33.02 |
| Positives per query min / median / max | 1 / 23.5 / 100 |
| Multi-positive queries | 47 (94.00%) |
| BM25 nDCG@10 | 0.2342 |
| BM25 hit@10 | 0.4600 |
| Query length avg chars | 23.08 |
| Document length avg chars | 1,522.71 |

### Public Sources

- [NFCorpus](https://www.cl.uni-heidelberg.de/~riezler/publications/papers/ECIR2016.pdf), [BEIR](https://arxiv.org/abs/2104.08663), [MMTEB](https://arxiv.org/abs/2502.13595), and [NanoBEIR](https://huggingface.co/collections/zeta-alpha-ai/nanobeir).

### Hugging Face Links

- Nano dataset: [hakari-bench/NanoBEIR-sr](https://huggingface.co/datasets/hakari-bench/NanoBEIR-sr)
- Source collection: [Zeta Alpha NanoBEIR collection](https://huggingface.co/collections/zeta-alpha-ai/nanobeir)

### Source Reference Table

| Title | Year | Type | URL |
| --- | ---: | --- | --- |
| NFCorpus: A Full-Text Learning to Rank Dataset for Medical Information Retrieval | 2016 | task paper | https://www.cl.uni-heidelberg.de/~riezler/publications/papers/ECIR2016.pdf |
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
  backing_dataset: NanoBEIR-sr
  dataset_id: hakari-bench/NanoBEIR-sr
  task_name: NanoNFCorpus
  split_name: NanoNFCorpus
  language: sr
  category: natural_language
  document_path: docs/benchmark_tasks/MNanoBEIR/NanoBEIR-sr__NanoNFCorpus.md
  source_research: {primary_source_type: task_paper, paper_pdf_or_html_checked: true, no_paper_note: null}
  counts: {queries: 50, documents: 2953, positive_qrels: 1651}
  positives_per_query: {average: 33.02, min: 1, median: 23.5, max: 100, multi_positive_queries: 47, multi_positive_query_percent: 94.0}
  text_stats_chars: {query_mean: 23.08, document_mean: 1522.705384}
  bm25: {ndcg_at_10: 0.2342336216, hit_at_10: 0.46, source: dataset_bm25_column}
```
