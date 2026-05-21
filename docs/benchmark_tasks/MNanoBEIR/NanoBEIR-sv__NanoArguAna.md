# MNanoBEIR / NanoBEIR-sv / NanoArguAna

## Overview

ArguAna is argument-counterargument retrieval. `NanoBEIR-sv__NanoArguAna` uses
Swedish translated argumentative passages as queries and retrieves paired
arguments or counterarguments.

## Details

### What the Original Data Measures

[ArguAna](https://aclanthology.org/P18-1023/) is used in BEIR as argument
retrieval, where relevance depends on stance and argumentative relation rather
than only topical overlap. MMTEB provides the multilingual context.

### Observed Data Profile

The task has 50 queries, 3,635 documents, and 50 positive qrels. Every query has
one positive. Queries are long, averaging 1,096.22 characters; documents average
1,006.23 characters.

### BM25 Difficulty

BM25 reaches nDCG@10 = 0.3185 and hit@10 = 0.5600. The median first-positive
rank is 6.0, so lexical overlap helps but does not capture stance or response
fit.

### Training Data That May Help

Use non-overlapping Swedish or multilingual argument mining, debate retrieval,
counterargument pairs, and stance-aware ranking. Exclude ArguAna, BEIR,
NanoBEIR, and translated overlaps.

### Synthetic Data Guidance

Generate Swedish claims and counterarguments from debate text. Hard negatives
should discuss the same topic while responding to a different premise or stance.

## Example Data

| Query | Positive document |
| --- | --- |
| Allmänheten är likgiltig inför reformer. Om reform av Overhuset bör vara en högsta prioritet i den nuvarande ekonomiska situationen är omdiskuterat, tala om om en koalitionsregering skulle kunna initiera och genomföra sådana ... [truncated 225 chars](586 chars) | AV-kampanjen kan inte jämföras med reformer av överhuset. Man bör inte förväxla en missinformerad allmänhet på grund av politisk retorik med likgiltighet. Ofta uttrycker väljare att de är likgiltiga eftersom de känner att de ... [truncated 225 chars](401 chars) |
| Utbyggnaden av Heathrow är avgörande för ekonomin. En utbyggnad av Heathrow skulle säkra många befintliga jobb samt skapa nya. För närvarande stöder Heathrow cirka 250 000 jobb. Till detta kommer hundratusentals fler som är b ... [truncated 225 chars](1246 chars) | Affärsvärlden är långt ifrån enad i sitt påstådda stöd för en tredje start- och landningsbana. Undersökningar tyder på att många inflytelserika företag faktiskt inte stöder expansionen. Ett brev som uttryckte oro undertecknad ... [truncated 225 chars](1407 chars) |
| Människor får för många valmöjligheter, vilket gör dem mindre lyckliga. Reklam gör att många människor känner sig överväldigade av det oändliga behovet att välja mellan konkurrerande krav på deras uppmärksamhet – detta kallas ... [truncated 225 chars](910 chars) | Människor är missnöjda för att de inte kan ha allt, inte för att de får för många val och tycker att det är stressande. Faktum är att reklam spelar en avgörande roll för att se till att människor använder sina pengar på det m ... [truncated 225 chars](902 chars) |
| Cyberattacker utförs ofta av icke-statliga aktörer, såsom cyberterrorister eller hacktivister (sociala aktivister som hackar), utan någon inblandning av den faktiska staten. Till exempel, i 2007 genomfördes ett massivt cybera ... [truncated 225 chars](947 chars) | Vid attacker från icke-statliga aktörer är det en allmän uppfattning bland praktiker inom internationell rätt att ett land fortfarande kan försvara sig om ett annat land "inte vill eller kan vidta effektiva åtgärder" för att ... [truncated 225 chars](567 chars) |
| Eftersom religion främjar säkerhet i tro, är gudomligt inspirerad hat lätt att använda för att rättfärdiga och främja våldsamma handlingar och diskriminerande praktiker. Yttrandefrihet måste komma i andra hand när det finns r ... [truncated 225 chars](1328 chars) | Ingen tvingas utföra våldshandlingar på grund av andras ord; det är deras eget val. Lika så finns det många människor som skulle ha åsikter som kan anses vara homofobiska men som skulle vara förskräckta över våldshandlingar. ... [truncated 225 chars](607 chars) |

## Dataset Information

| Field | Value |
| --- | --- |
| Nano set | MNanoBEIR |
| Backing dataset | NanoBEIR-sv |
| Task / split | NanoArguAna |
| Hugging Face dataset | [hakari-bench/NanoBEIR-sv](https://huggingface.co/datasets/hakari-bench/NanoBEIR-sv) |
| Language | sv |
| Category | natural_language |
| Queries | 50 |
| Documents | 3,635 |
| Positive qrels | 50 |
| BM25 nDCG@10 | 0.3185 |
| BM25 hit@10 | 0.5600 |
| Query length avg chars | 1,096.22 |
| Document length avg chars | 1,006.23 |

### Public Sources

- [ArguAna](https://aclanthology.org/P18-1023/), [BEIR](https://arxiv.org/abs/2104.08663), [MMTEB](https://arxiv.org/abs/2502.13595), and [NanoBEIR](https://huggingface.co/collections/zeta-alpha-ai/nanobeir).

### Hugging Face Links

- Nano dataset: [hakari-bench/NanoBEIR-sv](https://huggingface.co/datasets/hakari-bench/NanoBEIR-sv)
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
  backing_dataset: NanoBEIR-sv
  dataset_id: hakari-bench/NanoBEIR-sv
  task_name: NanoArguAna
  split_name: NanoArguAna
  language: sv
  category: natural_language
  document_path: docs/benchmark_tasks/MNanoBEIR/NanoBEIR-sv__NanoArguAna.md
  source_research: {primary_source_type: task_paper, paper_pdf_or_html_checked: true, no_paper_note: null}
  counts: {queries: 50, documents: 3635, positive_qrels: 50}
  positives_per_query: {average: 1.0, min: 1, median: 1.0, max: 1, multi_positive_queries: 0, multi_positive_query_percent: 0.0}
  text_stats_chars: {query_mean: 1096.22, document_mean: 1006.227235}
  bm25: {ndcg_at_10: 0.3184870928, hit_at_10: 0.56, source: dataset_bm25_column}
```
