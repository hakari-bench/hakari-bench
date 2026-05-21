# MNanoBEIR / NanoBEIR-fr / NanoClimateFEVER

## Overview

Climate-FEVER is a climate claim verification benchmark. `NanoBEIR-fr__NanoClimateFEVER`
is the French MNanoBEIR version: each query is a French translated climate
claim, and the system must retrieve French translated Wikipedia evidence
documents. The task tests claim-evidence retrieval in a climate-science setting.

## Details

### What the Original Data Measures

[CLIMATE-FEVER: A Dataset for Verification of Real-World Climate
Claims](https://arxiv.org/abs/2012.00614) introduces a climate fact-checking
dataset built from real-world climate claims and Wikipedia evidence. The
retrieval step matters because verification depends on finding evidence pages
that may discuss mechanisms, records, historical periods, or named experts
rather than merely repeating the claim.

[BEIR: A Heterogeneous Benchmark for Zero-shot Evaluation of Information
Retrieval Models](https://arxiv.org/abs/2104.08663) includes Climate-FEVER as a
fact-checking retrieval task. [MMTEB: Massive Multilingual Text Embedding
Benchmark](https://arxiv.org/abs/2502.13595) provides the multilingual context
for this French Nano split.

### Observed Data Profile

The sampled French Nano task has 50 queries, 3,408 documents, and 148 positive
qrel rows. Queries average 2.96 positives, with 44 of 50 queries having
multiple positives. The average query length is 158.84 characters, and the
average document length is 1,826.88 characters.

The inspected claims discuss existential risk, sea-level variability, human CO2
emissions, Holocene warmth, and historical warming/cooling cycles. Positive
documents are French translated Wikipedia-style pages, often long enough to
contain substantial context around the evidence-bearing topic.

### BM25 Difficulty

Using the dataset-provided BM25 candidate column, BM25 reaches nDCG@10 =
0.2789 and hit@10 = 0.7000. BM25 ranks a positive first for 12 queries, and
the median first-positive rank is 5.

Lexical matching helps when terms such as `CO2`, `niveau de la mer`, or named
periods recur, but many claims need a broader evidence page. Strong models
should connect the claim to the scientific or historical context that can verify
it, not just to matching climate vocabulary.

### Training Data That May Help

Useful training data includes non-overlapping climate fact-checking data,
scientific claim-evidence retrieval pairs, French or multilingual Wikipedia
claim verification data, and hard negatives from related climate pages. Training
should exclude Climate-FEVER, BEIR, NanoBEIR, or translated records likely to
overlap with these evaluation claims or evidence pages.

### Synthetic Data Guidance

For document-to-query generation, start from non-evaluation French climate or
environmental encyclopedia passages and generate concise claims that require
evidence. For joint generation, create related climate pages and claims where
the correct evidence page must be distinguished from topically similar pages.

## Example Data

| Query | Positive document |
| --- | --- |
| De 1970 à 1998, il y a eu une période de réchauffement qui a fait augmenter les températures d'environ 0,7 degré Fahrenheit, contribuant ainsi à l'émergence du mouvement alarmiste du réchauffement climatique. (208 chars) | Le Paléocène (prononcé /paleosɛn/), ou Paléocène, qui signifie « ancien récent », est une époque géologique qui a duré d'environ 66 à 56 millions d'années. C'est la première époque de la période Paléogène dans l'ère Cénozoïqu ... [truncated 225 chars](1248 chars) |
| En réalité, la tendance, bien qu'elle ne soit pas statistiquement significative, baisse. (88 chars) | Le cycle solaire ou cycle d'activité magnétique solaire est le cycle quasi périodique d'environ 11 ans des variations de l'activité du Soleil (y compris les changements dans les niveaux de rayonnement solaire et l'éjection de ... [truncated 225 chars](744 chars) |
| Les niveaux de la mer locaux et régionaux continuent de varier naturellement, montant dans certaines régions et baissant dans d'autres. (135 chars) | Le niveau moyen de la mer (NMM) (abréviation simplement niveau de la mer) est un niveau moyen de la surface d'un ou plusieurs des océans de la Terre à partir duquel des hauteurs telles que les altitudes peuvent être mesurées. ... [truncated 225 chars](1206 chars) |
| Les scientifiques du climat disent que certains aspects de l'ouragan Harvey suggèrent que le réchauffement climatique rend une situation déjà mauvaise encore plus difficile. (173 chars) | Les effets du réchauffement climatique sont les changements environnementaux et sociaux causés (directement ou indirectement) par les émissions humaines de gaz à effet de serre. Il existe un consensus scientifique selon leque ... [truncated 225 chars](1619 chars) |
| L'expérience CLOUD du CERN n'a testé qu'un tiers d'une des quatre exigences nécessaires pour attribuer le réchauffement climatique aux rayons cosmiques, et deux des autres exigences ont déjà échoué. (198 chars) | L'attribution des changements climatiques récents consiste à déterminer scientifiquement les mécanismes responsables des changements climatiques observés sur Terre, couramment appelés « réchauffement climatique ». Les efforts ... [truncated 225 chars](2450 chars) |

## Dataset Information

| Field | Value |
| --- | --- |
| Nano set | MNanoBEIR |
| Backing dataset | NanoBEIR-fr |
| Task / split | NanoClimateFEVER |
| Hugging Face dataset | [hakari-bench/NanoBEIR-fr](https://huggingface.co/datasets/hakari-bench/NanoBEIR-fr) |
| Language | fr |
| Category | natural_language |
| Queries | 50 |
| Documents | 3,408 |
| Positive qrels | 148 |
| Avg positives / query | 2.96 |
| Positives per query (min / median / max) | 1 / 3.00 / 5 |
| Queries with multiple positives | 44 (88.0%) |
| BM25 nDCG@10 | 0.2789 |
| BM25 hit@10 | 0.7000 |
| Query length avg chars | 158.84 |
| Document length avg chars | 1,826.88 |

### Public Sources

- [CLIMATE-FEVER: A Dataset for Verification of Real-World Climate Claims](https://arxiv.org/abs/2012.00614).
- [BEIR: A Heterogeneous Benchmark for Zero-shot Evaluation of Information Retrieval Models](https://arxiv.org/abs/2104.08663).
- [MMTEB: Massive Multilingual Text Embedding Benchmark](https://arxiv.org/abs/2502.13595).
- [Zeta Alpha NanoBEIR collection](https://huggingface.co/collections/zeta-alpha-ai/nanobeir).

### Hugging Face Links

- Nano dataset: [hakari-bench/NanoBEIR-fr](https://huggingface.co/datasets/hakari-bench/NanoBEIR-fr)
- Source collection: [Zeta Alpha NanoBEIR collection](https://huggingface.co/collections/zeta-alpha-ai/nanobeir)

### Source Reference Table

| Title | Year | Type | URL |
| --- | ---: | --- | --- |
| CLIMATE-FEVER: A Dataset for Verification of Real-World Climate Claims | 2021 | task paper | https://arxiv.org/abs/2012.00614 |
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
  backing_dataset: NanoBEIR-fr
  dataset_id: hakari-bench/NanoBEIR-fr
  task_name: NanoClimateFEVER
  split_name: NanoClimateFEVER
  language: fr
  category: natural_language
  document_path: docs/benchmark_tasks/MNanoBEIR/NanoBEIR-fr__NanoClimateFEVER.md
  source_research:
    primary_source_type: task_paper
    paper_pdf_or_html_checked: true
    no_paper_note: null
  counts:
    queries: 50
    documents: 3408
    positive_qrels: 148
  positives_per_query:
    average: 2.96
    min: 1
    median: 3.0
    max: 5
    multi_positive_queries: 44
    multi_positive_query_percent: 88.0
  text_stats_chars:
    query_mean: 158.84
    document_mean: 1826.88439
  bm25:
    ndcg_at_10: 0.278909355
    hit_at_10: 0.7
    source: dataset_bm25_column
```
