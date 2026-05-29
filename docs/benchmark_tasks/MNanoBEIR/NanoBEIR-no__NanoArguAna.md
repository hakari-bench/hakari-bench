# MNanoBEIR / NanoBEIR-no / NanoArguAna

## Overview

ArguAna is an argument-counterargument retrieval benchmark. `NanoBEIR-no__NanoArguAna`
uses Norwegian translated argumentative passages as queries and retrieves
Norwegian translated counterarguments or closely paired arguments.

## Details

### What the Original Data Measures

[ArguAna](https://aclanthology.org/P18-1023/) was introduced for argument
retrieval and matching in debate-style text. BEIR includes ArguAna as an
argument retrieval task, and MMTEB provides the multilingual benchmark context.

### Observed Data Profile

The sampled task has 50 queries, 3,635 documents, and 50 positive qrels. Every
query has exactly one positive. Queries are long translated argumentative
passages averaging 1,090.36 characters, while documents average 987.00
characters.

### BM25 Difficulty

BM25 reaches nDCG@10 = 0.3096 and hit@10 = 0.5600. Long text gives BM25 many
lexical anchors, but matching the correct counterargument requires stance and
argument-structure understanding.

### Training Data That May Help

Useful data includes non-overlapping argument retrieval, debate counterargument
pairs, stance-aware retrieval, and Norwegian or multilingual argument mining
data. Training should exclude ArguAna, BEIR, NanoBEIR, and translated argument
records likely to overlap.

### Synthetic Data Guidance

Generate Norwegian claims and counterarguments from non-evaluation debate text.
Hard negatives should address the same topic while taking a different stance or
responding to a different premise.

## Example Data

| Query | Positive document |
| --- | --- |
| Offentligheten er likegyldig overfor reformer. Det er usikkert om reform av Overhuset bør være en topprioritet i den nåværende økonomiske situasjonen, ikke å snakke om om en koalisjonsregjering ville kunne innføre og gjennomf ... [truncated 225 chars](587 chars) | AV-kampanjen kan ikke sammenlignes med reformer i Overhuset. Man bør ikke forveksle en misinformert offentlighet på grunn av politisk spin med likegyldighet. Ofte uttrykker velgere at de er likegyldige fordi de føler at de ik ... [truncated 225 chars](392 chars) |
| Utvidelse av Heathrow er avgjørende for økonomien. Utvidelse av Heathrow vil sikre mange eksisterende jobber samt skape nye. For tiden støtter Heathrow rundt 250 000 jobber. Til dette kommer hundretusener flere som er avhengi ... [truncated 225 chars](1191 chars) | Forretningsmiljøet er langt fra enig i sin antatte støtte til en tredje rullebane. Undersøkelser tyder på at mange innflytelsesrike bedrifter faktisk ikke støtter utvidelsen. Et brev som uttrykte bekymring ble underskrevet av ... [truncated 225 chars](1173 chars) |
| Mennesker blir gitt for mange valgmuligheter, noe som gjør dem mindre lykkelige. Reklame fører til at mange blir overveldet av den endeløse behovet for å velge mellom konkurrerende krav på oppmerksomheten – dette kalles valgt ... [truncated 225 chars](902 chars) | Folk er ulykkelige fordi de ikke kan få alt, ikke fordi de får for mange valg og finner det stressende. Faktisk spiller reklame en avgjørende rolle i å sikre at folk bruker pengene sine på det mest passende produktet for seg ... [truncated 225 chars](827 chars) |
| Cyberangrep blir ofte utført av ikke-statlige aktører, som for eksempel kyberterrorister eller hacktivister (sosiale aktivister som hacker), uten noen involvering fra staten. For eksempel ble Estland utsatt for et massivt cyb ... [truncated 225 chars](946 chars) | Hvis ikke-statlige aktører angriper, er mange praktikere innen internasjonal rett enige om at staten kan gjengjelde i selvforsvar hvis en annen stat er 'uvillig eller ute av stand til å ta effektive tiltak' for å håndtere ang ... [truncated 225 chars](533 chars) |
| Fordi religion gir troen en fast grunn, er guddommelig inspirert hat lett å bruke for å rettferdiggjøre og fremme voldshandlinger og diskriminerende praksis. Fri tale må stå tilbake når det er fare for at talen kan skade. Man ... [truncated 225 chars](1307 chars) | Ingen blir tvunget til å utføre voldshandlinger av andres ord; det er deres eget valg. Likewise, det finnes mange som kan ha synspunkter som kan oppfattes som homofobiske, men som ville være sjokkert over voldshandlinger. Det ... [truncated 225 chars](615 chars) |

## Dataset Information

| Field | Value |
| --- | --- |
| Nano set | MNanoBEIR |
| Backing dataset | NanoBEIR-no |
| Task / split | NanoArguAna |
| Hugging Face dataset | [hakari-bench/NanoBEIR-no](https://huggingface.co/datasets/hakari-bench/NanoBEIR-no) |
| Language | no |
| Category | natural_language |
| Queries | 50 |
| Documents | 3,635 |
| Positive qrels | 50 |
| BM25 nDCG@10 | 0.3096 |
| BM25 hit@10 | 0.5600 |
| BM25 Recall@100 | 0.8800 |
| BM25 candidate subset | top-500 (`bm25`) |
| Dense nDCG@10 | 0.3985 |
| Dense hit@10 | 0.6600 |
| Dense Recall@100 | 0.9200 |
| Dense candidate subset | top-500 (`harrier_oss_v1_270m`) |
| Reranking hybrid nDCG@10 | 0.3656 |
| Reranking hybrid hit@10 | 0.6800 |
| Reranking hybrid Recall@100 | 0.9200 |
| Reranking hybrid candidate subset | top-100 plus optional rank-101 safeguard (`reranking_hybrid`) |
| Reranking hybrid candidates / query | 100-101 |
| Reranking hybrid safeguard rows | 4 |
| Query length avg chars | 1,090.36 |
| Document length avg chars | 987.00 |

### Public Sources

- [Argument Mining for Understanding Peer Reviews](https://aclanthology.org/P18-1023/).
- [BEIR: A Heterogeneous Benchmark for Zero-shot Evaluation of Information Retrieval Models](https://arxiv.org/abs/2104.08663).
- [MMTEB: Massive Multilingual Text Embedding Benchmark](https://arxiv.org/abs/2502.13595).
- [Zeta Alpha NanoBEIR collection](https://huggingface.co/collections/zeta-alpha-ai/nanobeir).

### Hugging Face Links

- Nano dataset: [hakari-bench/NanoBEIR-no](https://huggingface.co/datasets/hakari-bench/NanoBEIR-no)
- Source collection: [Zeta Alpha NanoBEIR collection](https://huggingface.co/collections/zeta-alpha-ai/nanobeir)

### Source Reference Table

| Title | Year | Type | URL |
| --- | ---: | --- | --- |
| Argument Mining for Understanding Peer Reviews | 2018 | task paper | https://aclanthology.org/P18-1023/ |
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
  backing_dataset: NanoBEIR-no
  dataset_id: hakari-bench/NanoBEIR-no
  task_name: NanoArguAna
  split_name: NanoArguAna
  language: 'no'
  category: natural_language
  document_path: docs/benchmark_tasks/MNanoBEIR/NanoBEIR-no__NanoArguAna.md
  source_research:
    primary_source_type: task_paper
    paper_pdf_or_html_checked: true
    no_paper_note: null
  counts:
    queries: 50
    documents: 3635
    positive_qrels: 50
  positives_per_query:
    average: 1.0
    min: 1
    median: 1.0
    max: 1
    multi_positive_queries: 0
    multi_positive_query_percent: 0.0
  text_stats_chars:
    query_mean: 1090.36
    document_mean: 986.996699
  bm25:
    ndcg_at_10: 0.30955502307665733
    hit_at_10: 0.56
    source: dataset_candidate_subset
  candidate_subsets:
    bm25:
      config: bm25
      label: BM25
      source: dataset_candidate_subset
      top_k: 500
      ndcg_at_10: 0.3095550231
      hit_at_10: 0.56
      recall_at_100: 0.88
      candidate_count_min: 500
      candidate_count_max: 500
      candidate_count_mean: 500.0
      query_count: 50
      query_coverage: 1.0
      relevant_coverage_at_100: 0.88
    dense:
      config: harrier_oss_v1_270m
      label: Dense
      source: dataset_candidate_subset
      top_k: 500
      ndcg_at_10: 0.398523854
      hit_at_10: 0.66
      recall_at_100: 0.92
      candidate_count_min: 500
      candidate_count_max: 500
      candidate_count_mean: 500.0
      query_count: 50
      query_coverage: 1.0
      relevant_coverage_at_100: 0.92
    reranking_hybrid:
      config: reranking_hybrid
      label: Reranking hybrid
      source: dataset_candidate_subset
      top_k: 100
      ndcg_at_10: 0.3655920402
      hit_at_10: 0.68
      recall_at_100: 0.92
      candidate_count_min: 100
      candidate_count_max: 101
      candidate_count_mean: 100.08
      query_count: 50
      query_coverage: 1.0
      relevant_coverage_at_100: 0.92
      safeguard_positive_rows: 4
      rows_with_101_candidates: 4
```
