# MNanoBEIR / NanoBEIR-fr / NanoSciFact

## Overview

SciFact is a scientific claim verification dataset. `NanoBEIR-fr__NanoSciFact`
is the French MNanoBEIR version: French translated scientific claims must
retrieve French translated abstracts that support or refute the claim. The task
tests evidence retrieval in research literature with domain-specific scientific
terminology.

## Details

### What the Original Data Measures

[Fact or Fiction: Verifying Scientific Claims](https://arxiv.org/abs/2004.14974)
introduces SciFact as expert-written scientific claims paired with
evidence-containing abstracts annotated with support or refute labels and
rationales. Claims are derived from citation sentences, so they are natural
assertions about scientific findings.

[BEIR: A Heterogeneous Benchmark for Zero-shot Evaluation of Information
Retrieval Models](https://arxiv.org/abs/2104.08663) includes SciFact as a
fact-checking retrieval task. [MMTEB: Massive Multilingual Text Embedding
Benchmark](https://arxiv.org/abs/2502.13595) provides the multilingual context
for this French split.

### Observed Data Profile

The sampled French Nano task has 50 queries, 2,919 documents, and 56 positive
qrel rows. Most queries have one positive abstract, while 4 queries have
multiple positives. The average query length is 119.12 characters, and the
average document length is 1,711.09 characters.

The inspected claims involve breast cancer risk, brown adipose tissue, T-cell
receptor diversity, disease models, and G-quadruplex biology. Positive
documents are French translated scientific abstracts with methods and findings.

### BM25 Difficulty

Using the dataset-provided BM25 candidate column, BM25 reaches nDCG@10 =
0.6425 and hit@10 = 0.8000. BM25 ranks a positive first for 26 queries, and
the median first-positive rank is 1.

Lexical matching is often useful because technical terms repeat, but the harder
cases require recognizing evidence despite abbreviations, different phrasing,
or experimental context. Retrieval should be read separately from the later
support/refute classification decision.

### Training Data That May Help

Useful training data includes non-overlapping SciFact-style claim-evidence
pairs, scientific fact verification data, biomedical abstract retrieval pairs,
and French or multilingual scientific NLI or evidence selection data. Training
should exclude SciFact, BEIR, NanoBEIR, or translated records likely to overlap.

### Synthetic Data Guidance

For document-to-query generation, start from non-evaluation scientific abstracts
and generate atomic French claims that are supported or refuted by the abstract.
For joint generation, include related hard negatives that share terminology but
do not provide the needed evidence.

## Example Data

| Query | Positive document |
| --- | --- |
| Ly49Q dirige l'organisation de la migration des neutrophiles vers les sites d'inflammation en régulant les fonctions des rafts membranaires. (140 chars) | Les neutrophiles subissent rapidement une polarisation et un mouvement directionnel pour infiltrer les sites d'infection et d'inflammation. Nous démontrons ici que le récepteur inhibiteur MHC I, Ly49Q, est crucial pour la pol ... [truncated 225 chars](1134 chars) |
| La thérapie antirétrovirale réduit les taux de tuberculose chez les patients ayant différents niveaux de CD4. (109 chars) | CONTEXTE L'infection par le virus de l'immunodéficience humaine (VIH) est le principal facteur de risque de développement de la tuberculose et a contribué à sa résurgence, notamment en Afrique subsaharienne. En 2010, on estim ... [truncated 225 chars](2452 chars) |
| La régulation rapide et l'expression basale plus élevée des gènes induits par les interférons diminuent la survie des neurones des cellules granulaires infectés par le virus du Nil occidental. (192 chars) | Bien que la sensibilité des neurones du cerveau aux infections microbiennes soit un facteur déterminant majeur des résultats cliniques, peu de choses sont connues sur les facteurs moléculaires régissant cette vulnérabilité. I ... [truncated 225 chars](1344 chars) |
| Le dépistage primaire du cancer du col de l'utérus avec détection du HPV présente une sensibilité longitudinale supérieure à celle de la cytologie conventionnelle pour détecter une néoplasie intraépithéliale cervicale de grad ... [truncated 225 chars](229 chars) | CONTEXTE Le dépistage du cancer du col de l'utérus basé sur le test du papillomavirus humain (HPV) augmente la sensibilité de la détection des néoplasies intraépithéliales cervicales de haut grade (grade 2 ou 3), mais il est ... [truncated 225 chars](2577 chars) |
| Empêcher l'interaction entre TDP-43 et les protéines du complexe respiratoire I ND3 et ND6 entraîne une augmentation de la perte neuronale induite par TDP-43. (158 chars) | Les mutations génétiques de la protéine TAR DNA-binding protein 43 (TARDBP, également connue sous le nom de TDP-43) provoquent la sclérose latérale amyotrophique (SLA), et une augmentation de la présence de TDP-43 (codée par ... [truncated 225 chars](1531 chars) |

## Dataset Information

| Field | Value |
| --- | --- |
| Nano set | MNanoBEIR |
| Backing dataset | NanoBEIR-fr |
| Task / split | NanoSciFact |
| Hugging Face dataset | [hakari-bench/NanoBEIR-fr](https://huggingface.co/datasets/hakari-bench/NanoBEIR-fr) |
| Language | fr |
| Category | natural_language |
| Queries | 50 |
| Documents | 2,919 |
| Positive qrels | 56 |
| Avg positives / query | 1.12 |
| Positives per query (min / median / max) | 1 / 1.00 / 4 |
| Queries with multiple positives | 4 (8.0%) |
| BM25 nDCG@10 | 0.6425 |
| BM25 hit@10 | 0.8000 |
| Query length avg chars | 119.12 |
| Document length avg chars | 1,711.09 |

### Public Sources

- [Fact or Fiction: Verifying Scientific Claims](https://arxiv.org/abs/2004.14974).
- [SciFact repository](https://github.com/allenai/scifact).
- [BEIR: A Heterogeneous Benchmark for Zero-shot Evaluation of Information Retrieval Models](https://arxiv.org/abs/2104.08663).
- [MMTEB: Massive Multilingual Text Embedding Benchmark](https://arxiv.org/abs/2502.13595).
- [Zeta Alpha NanoBEIR collection](https://huggingface.co/collections/zeta-alpha-ai/nanobeir).

### Hugging Face Links

- Nano dataset: [hakari-bench/NanoBEIR-fr](https://huggingface.co/datasets/hakari-bench/NanoBEIR-fr)
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
  backing_dataset: NanoBEIR-fr
  dataset_id: hakari-bench/NanoBEIR-fr
  task_name: NanoSciFact
  split_name: NanoSciFact
  language: fr
  category: natural_language
  document_path: docs/benchmark_tasks/MNanoBEIR/NanoBEIR-fr__NanoSciFact.md
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
    query_mean: 119.12
    document_mean: 1711.088386
  bm25:
    ndcg_at_10: 0.6425340985
    hit_at_10: 0.8
    source: dataset_bm25_column
```
