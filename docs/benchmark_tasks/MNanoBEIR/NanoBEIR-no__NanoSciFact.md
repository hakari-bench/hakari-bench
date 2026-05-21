# MNanoBEIR / NanoBEIR-no / NanoSciFact

## Overview

SciFact is a scientific claim verification dataset. `NanoBEIR-no__NanoSciFact`
uses Norwegian translated scientific claims to retrieve Norwegian translated
abstracts that support or refute them.

## Details

### What the Original Data Measures

[Fact or Fiction: Verifying Scientific Claims](https://arxiv.org/abs/2004.14974)
introduced SciFact as expert-written scientific claims with evidence abstracts,
support/refute labels, and rationales. BEIR includes SciFact as fact-checking
retrieval, and MMTEB supplies the multilingual context.

### Observed Data Profile

The sampled task has 50 queries, 2,919 documents, and 56 positive qrels. Most
queries have one positive, while 4 queries have multiple positives. Queries
average 96.18 characters and documents average 1,424.51 characters.

### BM25 Difficulty

BM25 reaches nDCG@10 = 0.5652 and hit@10 = 0.7200. Technical terms often repeat
between claim and abstract, but evidence retrieval still needs to handle
abbreviations, biomedical phrasing, and experimental context.

### Training Data That May Help

Useful data includes non-overlapping scientific fact verification,
claim-evidence retrieval, biomedical abstract retrieval, and Norwegian or
multilingual scientific NLI. Exclude SciFact, BEIR, NanoBEIR, and overlapping
abstracts.

### Synthetic Data Guidance

Generate Norwegian atomic scientific claims from non-evaluation abstracts. Pair
them with evidence-bearing abstracts and use hard negatives from the same
discipline that share terminology but not the finding.

## Example Data

| Query | Positive document |
| --- | --- |
| Ly49Q styrer organiseringen av neutrofilmigrering til betennelsesområder ved å regulere membranraftfunksjoner. (110 chars) | Neutrofiler gjennomgår rask polarisering og rettet bevegelse for å trenge inn i infeksjons- og betennelsesområder. Her viser vi at en inhiberende MHC I-reseptor, Ly49Q, var avgjørende for rask polarisering og vevsinfiltrering ... [truncated 225 chars](969 chars) |
| Antiretroviral behandling reduserer forekomsten av tuberkulose i ulike CD4-nivåer. (82 chars) | BAKGRUNN Humant immunsviktvirus (HIV) infeksjon er den sterkeste risikofaktoren for å utvikle tuberkulose og har bidratt til en økning i forekomsten, spesielt i sub-Sahara-Afrika. I 2010 var det anslått 1,1 millioner nye tilf ... [truncated 225 chars](2211 chars) |
| Rask oppregulering og høyere basal ekspresjon av interferon-induserte gener reduserer overlevelsen av granulære celler i hjernen som er infisert med Vest-Nil-virus. (164 chars) | Selv om neuroners følsomhet for mikrobiell infeksjon i hjernen er en viktig faktor for klinisk utfall, er det lite kjent om de molekylære faktorer som styrer denne sårbarheten. Her viser vi at to typer neuroner fra forskjelli ... [truncated 225 chars](1072 chars) |
| Primær screening for livmorhalskreft med HPV-detektering har høyere langtidssensitivitet enn konvensjonell cytologi for å oppdage livmorhalscelleendringer av grad 2. (165 chars) | BAKGRUNN Screening for livmorhalskreft basert på testing for humant papillomavirus (HPV) øker følsomheten for å oppdage høygradig (grad 2 eller 3) livmorhalskreft forstadier, men om denne økningen representerer overdiagnostis ... [truncated 225 chars](2218 chars) |
| Å blokkere interaksjonen mellom TDP-43 og respiratorisk kompleks I-proteiner ND3 og ND6 fører til økt TDP-43-forårsaket nevronalt tap. (134 chars) | Genetiske mutasjoner i TAR DNA-binding protein 43 (TARDBP, også kjent som TDP-43) fører til amyotrofisk lateralsklerose (ALS). Økt tilstedeværelse av TDP-43 (kodet av TARDBP) i cytoplasma er et fremtredende histopatologisk tr ... [truncated 225 chars](1254 chars) |

## Dataset Information

| Field | Value |
| --- | --- |
| Nano set | MNanoBEIR |
| Backing dataset | NanoBEIR-no |
| Task / split | NanoSciFact |
| Hugging Face dataset | [hakari-bench/NanoBEIR-no](https://huggingface.co/datasets/hakari-bench/NanoBEIR-no) |
| Language | no |
| Category | natural_language |
| Queries | 50 |
| Documents | 2,919 |
| Positive qrels | 56 |
| Avg positives / query | 1.12 |
| Positives per query (min / median / max) | 1 / 1.00 / 4 |
| Queries with multiple positives | 4 (8.0%) |
| BM25 nDCG@10 | 0.5652 |
| BM25 hit@10 | 0.7200 |
| Query length avg chars | 96.18 |
| Document length avg chars | 1,424.51 |

### Public Sources

- [Fact or Fiction: Verifying Scientific Claims](https://arxiv.org/abs/2004.14974).
- [SciFact repository](https://github.com/allenai/scifact).
- [BEIR: A Heterogeneous Benchmark for Zero-shot Evaluation of Information Retrieval Models](https://arxiv.org/abs/2104.08663).
- [MMTEB: Massive Multilingual Text Embedding Benchmark](https://arxiv.org/abs/2502.13595).
- [Zeta Alpha NanoBEIR collection](https://huggingface.co/collections/zeta-alpha-ai/nanobeir).

### Hugging Face Links

- Nano dataset: [hakari-bench/NanoBEIR-no](https://huggingface.co/datasets/hakari-bench/NanoBEIR-no)
- Source collection: [Zeta Alpha NanoBEIR collection](https://huggingface.co/collections/zeta-alpha-ai/nanobeir)

### Source Reference Table

| Title | Year | Type | URL |
| --- | ---: | --- | --- |
| Fact or Fiction: Verifying Scientific Claims | 2020 | task paper | https://arxiv.org/abs/2004.14974 |
| SciFact repository |  | project page | https://github.com/allenai/scifact |
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
  task_name: NanoSciFact
  split_name: NanoSciFact
  language: "no"
  category: natural_language
  document_path: docs/benchmark_tasks/MNanoBEIR/NanoBEIR-no__NanoSciFact.md
  source_research:
    primary_source_type: task_paper
    paper_pdf_or_html_checked: true
    no_paper_note: null
  counts:
    queries: 50
    documents: 2919
    positive_qrels: 56
  positives_per_query:
    average: 1.12
    min: 1
    median: 1.0
    max: 4
    multi_positive_queries: 4
    multi_positive_query_percent: 8.0
  text_stats_chars:
    query_mean: 96.18
    document_mean: 1424.51456
  bm25:
    ndcg_at_10: 0.565197745
    hit_at_10: 0.72
    source: dataset_bm25_column
```
