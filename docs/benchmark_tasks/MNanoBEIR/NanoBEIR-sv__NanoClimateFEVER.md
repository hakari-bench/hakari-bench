# MNanoBEIR / NanoBEIR-sv / NanoClimateFEVER

## Overview

Climate-FEVER is an evidence retrieval task for climate-related claims.
`NanoBEIR-sv__NanoClimateFEVER` uses Swedish translated claims to retrieve
Swedish translated evidence passages.

## Details

### What the Original Data Measures

[CLIMATE-FEVER](https://arxiv.org/abs/2012.00614) evaluates retrieval of
evidence for real-world climate claims. BEIR includes it as claim-evidence
retrieval, and MMTEB provides the multilingual benchmark context for this
Swedish version.

### Observed Data Profile

The sampled task has 50 queries, 3,408 documents, and 148 positive qrels. Most
queries have multiple positives, with an average of 2.96 and a maximum of 5.
Queries average 132.16 characters, and documents average 1,538.72 characters.

### BM25 Difficulty

BM25 reaches nDCG@10 = 0.2388 and hit@10 = 0.5800. The median first-positive
rank is 7.0, so lexical overlap alone often struggles to rank the complete
evidence set.

### Training Data That May Help

Useful data includes non-overlapping climate claim verification, Swedish
scientific evidence retrieval, and multilingual fact-checking. Exclude
CLIMATE-FEVER, BEIR, NanoBEIR, and translated evaluation records.

### Synthetic Data Guidance

Generate Swedish climate claims from non-evaluation passages and pair them with
multiple evidence passages when available. Hard negatives should share climate
terms while failing to verify the claim.

## Example Data

| Query | Positive document |
| --- | --- |
| Från 1970 till 1998 fanns det en uppvärmningsperiod som höjde temperaturerna med cirka 0,7 Fahrenheit, vilket bidrog till att skapa rörelsen för global uppvärmning. (164 chars) | Paleocen (uttalas /ˈpæliəˌsiːn/ eller /ˈpæ - , - lioʊ - /) eller Paleocen, den "gamla nya", är en geologisk epok som varade från cirka . Det är den första epoken i Paleogenperioden under den moderna Cenozoiska eran. Som med m ... [truncated 225 chars](1004 chars) |
| I själva verket är trenden nedåtgående, även om det inte är statistiskt signifikant. (84 chars) | Solarcykeln eller solaktivitetscykeln är den nästan periodiska 11-årsförändringen i solens aktivitet (inklusive förändringar i nivåerna av solstrålning och utsändning av solmaterial) och utseende (förändringar i antalet och s ... [truncated 225 chars](607 chars) |
| Lokala och regionala havsnivåer fortsätter visa den vanliga naturliga variationen, stiger på vissa ställen och sjunker på andra. (128 chars) | Medelhavsnivå (MSL) (förkortat havsnivå) är en genomsnittlig nivå av jordens havsytor, från vilken höjder som höjder kan mätas. MSL är en typ av vertikal datum, en standardiserad geodetisk referenspunkt som används, till exem ... [truncated 225 chars](867 chars) |
| Klimatforskare säger att i fallet med Orkanen Harvey tyder det på att global uppvärmning förvärrar en redan dålig situation. (124 chars) | De globala uppvärmningens effekter är de miljö- och samhällsförändringar som orsakas (direkt eller indirekt) av människans utsläpp av växthusgaser. Det finns en vetenskaplig konsensus om att klimatförändringar pågår och att m ... [truncated 225 chars](1368 chars) |
| CERN:s CLOUD-experiment testade endast en tredjedel av ett av fyra krav som krävs för att skylla på kosmiska strålar för den globala uppvärmningen, och två av de andra kraven har redan misslyckats. (197 chars) | Tillskrivning av den senaste klimatförändringen är ansträngningen att vetenskapligt fastställa mekanismer som är ansvariga för de senaste klimatförändringarna på jorden, vanligtvis kända som `global uppvärmning`. Ansträngning ... [truncated 225 chars](2098 chars) |

## Dataset Information

| Field | Value |
| --- | --- |
| Nano set | MNanoBEIR |
| Backing dataset | NanoBEIR-sv |
| Task / split | NanoClimateFEVER |
| Hugging Face dataset | [hakari-bench/NanoBEIR-sv](https://huggingface.co/datasets/hakari-bench/NanoBEIR-sv) |
| Language | sv |
| Category | natural_language |
| Queries | 50 |
| Documents | 3,408 |
| Positive qrels | 148 |
| Positives per query avg | 2.96 |
| Positives per query min / median / max | 1 / 3.0 / 5 |
| Multi-positive queries | 44 (88.00%) |
| BM25 nDCG@10 | 0.2388 |
| BM25 hit@10 | 0.5800 |
| Query length avg chars | 132.16 |
| Document length avg chars | 1,538.72 |

### Public Sources

- [CLIMATE-FEVER](https://arxiv.org/abs/2012.00614), [BEIR](https://arxiv.org/abs/2104.08663), [MMTEB](https://arxiv.org/abs/2502.13595), and [NanoBEIR](https://huggingface.co/collections/zeta-alpha-ai/nanobeir).

### Hugging Face Links

- Nano dataset: [hakari-bench/NanoBEIR-sv](https://huggingface.co/datasets/hakari-bench/NanoBEIR-sv)
- Source collection: [Zeta Alpha NanoBEIR collection](https://huggingface.co/collections/zeta-alpha-ai/nanobeir)

### Source Reference Table

| Title | Year | Type | URL |
| --- | ---: | --- | --- |
| CLIMATE-FEVER: A Dataset for Verification of Real-World Climate Claims | 2020 | task paper | https://arxiv.org/abs/2012.00614 |
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
  task_name: NanoClimateFEVER
  split_name: NanoClimateFEVER
  language: sv
  category: natural_language
  document_path: docs/benchmark_tasks/MNanoBEIR/NanoBEIR-sv__NanoClimateFEVER.md
  source_research: {primary_source_type: task_paper, paper_pdf_or_html_checked: true, no_paper_note: null}
  counts: {queries: 50, documents: 3408, positive_qrels: 148}
  positives_per_query: {average: 2.96, min: 1, median: 3.0, max: 5, multi_positive_queries: 44, multi_positive_query_percent: 88.0}
  text_stats_chars: {query_mean: 132.16, document_mean: 1538.718016}
  bm25: {ndcg_at_10: 0.23884791, hit_at_10: 0.58, source: dataset_bm25_column}
```
