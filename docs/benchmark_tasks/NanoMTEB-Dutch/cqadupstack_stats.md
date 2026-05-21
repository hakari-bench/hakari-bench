# NanoMTEB-Dutch / cqadupstack_stats

## Overview

`cqadupstack_stats` is the Dutch-translated Cross Validated / statistics
subforum split of CQADupStack. Queries are statistics and probability questions,
and positive documents are older duplicate questions. The task tests duplicate
retrieval for statistical concepts, formulas, tests, models, and probability
examples.

## Details

### What the Original Data Measures

[CQADupStack: A Benchmark Data Set for Community Question-Answering Research](https://doi.org/10.1145/2838931.2838934)
uses StackExchange duplicate labels to evaluate retrieval of previously asked
questions. The paper notes that exact-topic subforums such as statistics are
focused but still challenging: duplicate pairs can have only modest lexical
overlap, and the benchmark uses chronological splits to reflect real duplicate
detection.

[BEIR-NL](https://aclanthology.org/2025.bucc-1.5/) translates BEIR datasets into
Dutch. This split preserves CQADupStack's duplicate links while presenting the
statistics questions in Dutch-translated form, with formulas and notation often
unchanged.

### Observed Data Profile

The Nano split has 200 queries, 10,000 documents, and 200 positive qrel rows.
Each query has one positive. Queries average 64.27 characters and documents
average 1,097.65 characters. Examples include sampling representativeness,
variance estimates, uncorrelated but dependent variables, predicted lines in R,
and runs of coin-flip-like outcomes.

The data combines short conceptual questions with longer documents containing R
code, formulas, textbook references, and worked probability setups.

### BM25 Difficulty

Using the dataset-provided BM25 candidate column, BM25 reaches nDCG@10 = 0.2827
and hit@10 = 0.3850. Sparse matching benefits from symbols and terms such as
variance or Bernoulli, but equivalent statistical questions are often phrased
with different examples or notation.

### Training Data That May Help

Useful training data includes non-overlapping Cross Validated duplicate pairs,
Dutch-translated statistics QA, formula-aware retrieval data, and multilingual
STEM duplicate-question datasets. Exclude this Nano test split and positives.

### Synthetic Data Guidance

Generate Dutch statistics questions from non-evaluation posts while preserving
formulas and code. Create paraphrased duplicates that use different examples for
the same concept, plus hard negatives sharing notation but asking a different
statistical question.

## Example Data

| Query | Positive document |
| --- | --- |
| Schattingen van variantie uit een iid steekproef (48 chars) | Intuïtieve uitleg voor delen door (n-1) bij het berekenen van de standaarddeviatie? Vandaag kreeg ik in de klas de vraag waarom je de som van de gekwadrateerde afwijkingen deelt door $(n-1)$ in plaats van door $n$ bij het ber ... [truncated 225 chars](435 chars) |
| Hoe kan ik type II (bèta) fout, power en steekproefomvang het beste grafisch weergeven? (87 chars) | Reëel gebaseerd op machtsfunctie Probleem: Wat is een voorbeeld uit het echte leven van een machtsfunctie? Ik heb erover nagedacht, maar ik ben er niet uitgekomen. Weet iemand het? (181 chars) |
| Het weergeven van een afstandsmatrix in het vlak (48 chars) | Wat is het verschil tussen principale componentenanalyse en multidimensionale schaalverdeling? Hoe verschillen PCA en klassieke MDS? En MDS versus niet-metrische MDS? Is er een situatie waarin je de voorkeur aan de een boven ... [truncated 225 chars](280 chars) |
| Hulp bij het interpreteren van een R lineair model (50 chars) | Basisvragen over de interpretatie van resultaten van summary(lm(...~...)) in R set.seed(11) a = runif (12) b = rep(c(1,2,3),4) summary(lm(a~b))$coeff summary(lm(a~b-1))$coeff Wat betekent een p-waarde voor het intercept? Wat ... [truncated 225 chars](433 chars) |
| Hoe om te gaan met ontbrekende waarden voor PCA? (48 chars) | Vervanging van NA-waarden voor PCA-analyse Ik heb de functie `prcomp()` gebruikt om een PCA-analyse uit te voeren in R. Er zit echter een bug in die functie waardoor de parameter `na.action` niet werkt. Ik heb op stackoverflo ... [truncated 225 chars](1676 chars) |

## Dataset Information

| Field | Value |
| --- | --- |
| Nano set | NanoMTEB-Dutch |
| Backing dataset | NanoMTEB-Dutch |
| Task / split | cqadupstack_stats |
| Hugging Face dataset | [hakari-bench/NanoMTEB-Dutch](https://huggingface.co/datasets/hakari-bench/NanoMTEB-Dutch) |
| Source dataset | [clips/beir-nl-cqadupstack](https://huggingface.co/datasets/clips/beir-nl-cqadupstack) |
| Language | nl |
| Category | natural_language |
| Queries | 200 |
| Documents | 10,000 |
| Positive qrels | 200 |
| BM25 nDCG@10 | 0.2827 |
| BM25 hit@10 | 0.3850 |
| Query length avg chars | 64.27 |
| Document length avg chars | 1,097.65 |

### Public Sources

- [CQADupStack: A Benchmark Data Set for Community Question-Answering Research](https://doi.org/10.1145/2838931.2838934), 2015.
- [Author-hosted CQADupStack PDF](https://eltimster.github.io/www/pubs/adcs2015.pdf), 2015.
- [BEIR-NL: Zero-shot Information Retrieval Benchmark for the Dutch Language](https://aclanthology.org/2025.bucc-1.5/), 2025.
- [BEIR: A Heterogeneous Benchmark for Zero-shot Evaluation of Information Retrieval Models](https://arxiv.org/abs/2104.08663), 2021.
- [clips/beir-nl-cqadupstack](https://huggingface.co/datasets/clips/beir-nl-cqadupstack), source dataset card.

### Hugging Face Links

- Nano dataset: [hakari-bench/NanoMTEB-Dutch](https://huggingface.co/datasets/hakari-bench/NanoMTEB-Dutch)
- Source dataset: [clips/beir-nl-cqadupstack](https://huggingface.co/datasets/clips/beir-nl-cqadupstack)

### Source Reference Table

| Title | Year | Type | URL |
| --- | ---: | --- | --- |
| CQADupStack: A Benchmark Data Set for Community Question-Answering Research | 2015 | proceedings paper | https://doi.org/10.1145/2838931.2838934 |
| BEIR-NL: Zero-shot Information Retrieval Benchmark for the Dutch Language | 2025 | proceedings paper | https://aclanthology.org/2025.bucc-1.5/ |
| BEIR: A Heterogeneous Benchmark for Zero-shot Evaluation of Information Retrieval Models | 2021 | arXiv paper | https://arxiv.org/abs/2104.08663 |
| clips/beir-nl-cqadupstack |  | dataset card | https://huggingface.co/datasets/clips/beir-nl-cqadupstack |

## Machine-Readable Metadata

<!-- benchmark-task-metadata:v1 -->

```yaml
benchmark_task_metadata:
  schema_version: 1
  document_status: first_pass
  nano_set: NanoMTEB-Dutch
  backing_dataset: NanoMTEB-Dutch
  dataset_id: hakari-bench/NanoMTEB-Dutch
  task_name: cqadupstack_stats
  split_name: cqadupstack_stats
  language: nl
  category: natural_language
  document_path: docs/benchmark_tasks/NanoMTEB-Dutch/cqadupstack_stats.md
  source_research:
    primary_source_type: task_paper
    paper_pdf_or_html_checked: true
    paper_url: https://doi.org/10.1145/2838931.2838934
    additional_source_urls:
      - https://eltimster.github.io/www/pubs/adcs2015.pdf
      - https://aclanthology.org/2025.bucc-1.5/
      - https://arxiv.org/abs/2104.08663
      - https://huggingface.co/datasets/clips/beir-nl-cqadupstack
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
    query_mean: 64.265
    document_mean: 1097.6471
  bm25:
    ndcg_at_10: 0.2826641003
    hit_at_10: 0.385
    source: dataset_bm25_column
  learning:
    original_train_split: available
    evaluation_split_origin: "CQADupstackStats-NL test split from clips/beir-nl-cqadupstack"
    train_eval_overlap_audit: not_audited
    leakage_note: "Exclude translated CQADupStack Stats test queries and duplicate positives used by this Nano split."
    useful_training_data:
      - non-overlapping Cross Validated duplicate-question pairs
      - Dutch-translated statistics QA pairs
      - formula-aware STEM duplicate retrieval data
    synthetic_data:
      document_generation: "Dutch statistics forum questions with formulas or R code preserved."
      question_generation: "Paraphrased duplicate statistics questions using varied examples."
      answerability: "Each query should duplicate one prior statistics question, with notation-near hard negatives."
    multi_positive_training: single_positive
  example_count: 5
```
