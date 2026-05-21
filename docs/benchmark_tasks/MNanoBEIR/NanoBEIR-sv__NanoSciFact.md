# MNanoBEIR / NanoBEIR-sv / NanoSciFact

## Overview

SciFact is scientific claim evidence retrieval. `NanoBEIR-sv__NanoSciFact`
uses Swedish translated scientific claims to retrieve Swedish translated
abstract evidence.

## Details

### What the Original Data Measures

[SciFact](https://arxiv.org/abs/2004.14974) evaluates verification of scientific
claims against abstracts. BEIR uses the retrieval part, and MMTEB supplies
multilingual context.

### Observed Data Profile

The task has 50 queries, 2,919 documents, and 56 positive qrels. Most queries
have one positive, with 4 multi-positive queries. Queries average 95.12
characters, and documents average 1,429.10 characters.

### BM25 Difficulty

BM25 reaches nDCG@10 = 0.6539 and hit@10 = 0.8200. The median first-positive
rank is 1.0, showing strong scientific term anchors but a need for evidence
discrimination.

### Training Data That May Help

Use non-overlapping scientific claim verification, biomedical abstract
retrieval, Swedish scientific QA, and multilingual evidence retrieval. Exclude
SciFact, BEIR, NanoBEIR, and translated evaluation claims.

### Synthetic Data Guidance

Generate Swedish scientific claims from abstracts. Hard negatives should share
entities or methods while not supporting the claim.

## Example Data

| Query | Positive document |
| --- | --- |
| Ly49Q styr organiseringen av neutrofilmigration till inflammationsställen genom att reglera membranraftsfunktioner. (115 chars) | Neutrofilerna genomgår snabbt polarisering och riktad rörelse för att tränga in i infektions- och inflammationsställen. Vi visar här att en inhiberande MHC I-receptor, Ly49Q, var avgörande för den snabba polariseringen och vä ... [truncated 225 chars](1025 chars) |
| Antiretroviral behandling minskar förekomsten av tuberkulos över ett brett spektrum av CD4-strata. (98 chars) | BAKGRUND Infektion med humant immunbristvirus (HIV) är den starkaste riskfaktorn för att utveckla tuberkulos och har drivit på dess återkomst, särskilt i subsahariska Afrika. År 2010 uppskattades det finnas 1,1 miljoner nya f ... [truncated 225 chars](2152 chars) |
| Snabb uppreglering och högre basala uttryck av interferoninducerade gener minskar överlevnaden hos granulära cellneuroner som är infekterade av West Nile-virus. (160 chars) | Neuronernas känslighet i hjärnan för mikrobiella infektioner är en avgörande faktor för klinisk utfall. Det finns lite kunskap om de molekylära faktorer som styr denna sårbarhet. Vi visar här att två typer av neuroner från ol ... [truncated 225 chars](1092 chars) |
| Primär screening för livmoderhalscancer med HPV-detektion har högre longitudinell känslighet än konventionell cytologi för att upptäcka cervikal intraepithelial neoplasi grad 2. (177 chars) | Bakgrund: Screening för livmoderhalscancer baserat på testning för humant papillomavirus (HPV) ökar känsligheten för upptäckt av höggradig (grad 2 eller 3) livmoderhalscancerprekancerösa förändringar, men om denna ökning inne ... [truncated 225 chars](2333 chars) |
| Hinderar interaktionen mellan TDP-43 och komplex I-proteiner ND3 och ND6 resulterar i ökad TDP-43-inducerad neuronal förlust. (125 chars) | Genetiska mutationer i TAR DNA-bindande protein 43 (TARDBP, även känt som TDP-43) orsakar amyotrofisk lateral skleros (ALS), och en ökning av TDP-43 (kodat av TARDBP) i cytoplasman är en framträdande histopatologisk egenskap ... [truncated 225 chars](1263 chars) |

## Dataset Information

| Field | Value |
| --- | --- |
| Nano set | MNanoBEIR |
| Backing dataset | NanoBEIR-sv |
| Task / split | NanoSciFact |
| Hugging Face dataset | [hakari-bench/NanoBEIR-sv](https://huggingface.co/datasets/hakari-bench/NanoBEIR-sv) |
| Language | sv |
| Category | natural_language |
| Queries | 50 |
| Documents | 2,919 |
| Positive qrels | 56 |
| Positives per query avg | 1.12 |
| Positives per query min / median / max | 1 / 1.0 / 4 |
| Multi-positive queries | 4 (8.00%) |
| BM25 nDCG@10 | 0.6539 |
| BM25 hit@10 | 0.8200 |
| Query length avg chars | 95.12 |
| Document length avg chars | 1,429.10 |

### Public Sources

- [SciFact](https://arxiv.org/abs/2004.14974), [BEIR](https://arxiv.org/abs/2104.08663), [MMTEB](https://arxiv.org/abs/2502.13595), and [NanoBEIR](https://huggingface.co/collections/zeta-alpha-ai/nanobeir).

### Hugging Face Links

- Nano dataset: [hakari-bench/NanoBEIR-sv](https://huggingface.co/datasets/hakari-bench/NanoBEIR-sv)
- Source collection: [Zeta Alpha NanoBEIR collection](https://huggingface.co/collections/zeta-alpha-ai/nanobeir)

### Source Reference Table

| Title | Year | Type | URL |
| --- | ---: | --- | --- |
| SciFact: Fact or Fiction: Verifying Scientific Claims | 2020 | task paper | https://arxiv.org/abs/2004.14974 |
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
  task_name: NanoSciFact
  split_name: NanoSciFact
  language: sv
  category: natural_language
  document_path: docs/benchmark_tasks/MNanoBEIR/NanoBEIR-sv__NanoSciFact.md
  source_research: {primary_source_type: task_paper, paper_pdf_or_html_checked: true, no_paper_note: null}
  counts: {queries: 50, documents: 2919, positive_qrels: 56}
  positives_per_query: {average: 1.12, min: 1, median: 1.0, max: 4, multi_positive_queries: 4, multi_positive_query_percent: 8.0}
  text_stats_chars: {query_mean: 95.12, document_mean: 1429.100719}
  bm25: {ndcg_at_10: 0.6538586546, hit_at_10: 0.82, source: dataset_bm25_column}
```
