# NanoMedical / NanoTRECCOVID

## Overview

`NanoTRECCOVID` is an English COVID-19 scientific literature retrieval task
derived from TREC-COVID. Queries are pandemic information needs about
SARS-CoV-2 origin, transmission, testing, treatments, vaccines, public-health
interventions, and clinical outcomes. Documents are CORD-19 scientific article
records, usually represented by a title and abstract. The task tests whether a
retriever can find evidence-bearing COVID-19 literature for broad biomedical and
public-health questions.

## Details

### What the Original Data Measures

[Searching for Scientific Evidence in a Pandemic: An Overview of TREC-COVID](https://arxiv.org/abs/2104.09632)
describes TREC-COVID as an information-retrieval shared task over COVID-19
scientific literature. The challenge ran for five rounds from April to July 2020,
with 92 unique teams and 556 submissions. It used 50 topics, starting with 30 in
round 1 and adding 5 new topics per round to track emerging information needs.
The paper states that the final test collection contains 69,318 manual judgments.

The task used CORD-19, a rapidly updated corpus of COVID-19 and coronavirus
research including peer-reviewed papers and preprints from PubMed Central,
PubMed, bioRxiv, medRxiv, arXiv, the WHO COVID-19 database, Semantic Scholar,
and other sources. TREC-COVID topics have a three-part structure: a keyword
query, a natural-language question, and a longer narrative. Topics were balanced
across biological, clinical, and public-health needs, including transmission,
prevention, effects, and treatment.

The original TREC-COVID assessment used pooled participant runs and relevance
judgments with three labels: not relevant, partially relevant, and fully relevant.
Assessors included NLM MeSH indexers, medical students, and biomedical experts.
This Nano task uses the retrieval surface of TREC-COVID but reduces it to 50
question-style queries with one positive document each.

### Observed Data Profile

The Nano split has 50 queries, 10,000 documents, and 50 positive qrel rows. Each
query has exactly one positive document. Queries average 69.24 characters, while
documents average 1,208.78 characters. The sampled queries are the natural
language question form of the TREC-COVID topics, such as `what is the origin of
COVID-19`, `what evidence is there for the value of hydroxychloroquine in
treating Covid-19?`, and `What is the protein structure of the SARS-CoV-2
spike?`.

Documents are heterogeneous. Some positives are full article-title plus abstract
records, while some are very short title-only entries, such as `COVID-19 and
hypertension`. The corpus also includes historical coronavirus, influenza, public
health, and virology material, so a COVID-19 query may have relevant evidence in
both direct COVID-19 papers and older related coronavirus literature.

### BM25 Difficulty

Using the dataset-provided BM25 candidate column, BM25 reaches nDCG@10 = 0.1966
and hit@10 = 0.3200. It ranks 4 of 50 positives first and 16 positives inside
the top 10. This is a difficult sparse baseline in the Nano subset, despite the
obvious COVID-19 vocabulary, because many documents share pandemic terms and the
positive can be narrow, indirect, or title-only.

Observed failures include a seasonal-flu comparison query where BM25 retrieves
influenza pandemic and transmission papers before a COVID-19 overview; a
domestic-violence query where it retrieves general youth violence and long-term
care COVID papers before the relevant domestic-violence syndemic article; and a
Vitamin D query where it retrieves vitamin D deficiency pages before a broader
ACE2/COVID therapeutic discussion. Strong retrieval needs both pandemic
terminology matching and fine-grained topic intent matching.

### Training Data That May Help

Useful training data includes non-overlapping COVID-19 literature retrieval,
CORD-19 search logs or judgments, biomedical ad hoc retrieval, clinical and
public-health question-to-abstract data, and hard negatives from related
coronavirus or influenza literature. Relevance-feedback training can help, but it
must be reported clearly because TREC-COVID was explicitly designed to study
feedback across rounds.

For clean evaluation, training should exclude TREC-COVID Complete qrels for the
evaluation topics and any exact CORD-19 positive documents from this Nano split.
Training on prior-round judgments is a different benchmark setting and should
not be mixed with zero-shot claims.

### Synthetic Data Guidance

For document-to-question generation, start from non-evaluation COVID-19 or
coronavirus abstracts and generate question-style information needs about
transmission, testing, treatments, vaccines, risk factors, public-health
interventions, or clinical outcomes. The question should target the evidence in
the abstract rather than only repeat the article title.

For joint document-and-question generation, create pandemic-literature abstracts
and paired clinical, biological, or public-health questions. Include hard
negatives with the same COVID-19 terms but different intervention, population,
outcome, or virus family. Do not seed generation with Nano evaluation queries or
positive documents.

## Example Data

| Query | Positive document |
| --- | --- |
| what evidence is there for dexamethasone as a treatment for COVID-19? (69 chars) | The Combination of Tocilizumab and Methylprednisolone Along With Initial Lung Recruitment Strategy in Coronavirus Disease 2019 Patients Requiring Mechanical Ventilation: A Series of 21 Consecutive Cases OBJECTIVE: To describe ... [truncated 225 chars](1756 chars) |
| how long does coronavirus remain stable on surfaces? (53 chars) | Body fluids may contribute to human-to-human transmission of severe acute respiratory syndrome coronavirus 2: evidence and practical experience BACKGROUND: In December 2019, an unbelievable outbreak of pneumonia associated wi ... [truncated 225 chars](1171 chars) |
| has social distancing had an impact on slowing the spread of COVID-19? (70 chars) | Increased Detection coupled with Social Distancing and Health Capacity Planning Reduce the Burden of COVID-19 Cases and Fatalities: A Proof of Concept Study using a Stochastic Computational Simulation Model Objective: In abse ... [truncated 225 chars](1575 chars) |
| are there serological tests that detect antibodies to coronavirus? (66 chars) | Serodiagnostics for Severe Acute Respiratory Syndrome-Related Coronavirus-2: A Narrative Review Accurate serologic tests to detect host antibodies to severe acute respiratory syndrome-related coronavirus-2 (SARS-CoV-2) will b ... [truncated 225 chars](1428 chars) |
| which biomarkers predict the severe clinical course of 2019-nCOV infection? (75 chars) | Clinical Features and Predictors for Patients with Severe SARS-CoV-2 Pneumonia: a retrospective multicenter cohort study Objectives: This study was performed to investigate clinical features of patients with severe SARS-CoV-2 ... [truncated 225 chars](1517 chars) |

## Dataset Information

| Field | Value |
| --- | --- |
| Nano set | NanoMedical |
| Backing dataset | NanoMedical |
| Task / split | NanoTRECCOVID |
| Hugging Face dataset | [hakari-bench/NanoMedical](https://huggingface.co/datasets/hakari-bench/NanoMedical) |
| Language | en |
| Category | natural_language |
| Queries | 50 |
| Documents | 10,000 |
| Positive qrels | 50 |
| BM25 nDCG@10 | 0.3983 |
| BM25 hit@10 | 0.5200 |
| BM25 Recall@100 | 0.8000 |
| BM25 candidate subset | top-500 (`bm25`) |
| Dense nDCG@10 | 0.3875 |
| Dense hit@10 | 0.5200 |
| Dense Recall@100 | 0.7000 |
| Dense candidate subset | top-500 (`harrier_oss_v1_270m`) |
| Reranking hybrid nDCG@10 | 0.3193 |
| Reranking hybrid hit@10 | 0.4400 |
| Reranking hybrid Recall@100 | 0.9600 |
| Reranking hybrid candidate subset | top-100 plus optional rank-101 safeguard (`reranking_hybrid`) |
| Reranking hybrid candidates / query | 100-101 |
| Reranking hybrid safeguard rows | 2 |
| Query length avg chars | 69.24 |
| Document length avg chars | 1,208.78 |

### Public Sources

- [Searching for Scientific Evidence in a Pandemic: An Overview of TREC-COVID](https://arxiv.org/abs/2104.09632); 2021; Kirk Roberts, Tasmeer Alam, Steven Bedrick, Dina Demner-Fushman, Kyle Lo, Ian Soboroff, Ellen Voorhees, Lucy Lu Wang, and William R. Hersh.
- [TREC-COVID data archive](https://ir.nist.gov/trec-covid/).

### Hugging Face Links

- Nano dataset: [hakari-bench/NanoMedical](https://huggingface.co/datasets/hakari-bench/NanoMedical)

### Source Reference Table

| Title | Year | Type | URL |
| --- | ---: | --- | --- |
| Searching for Scientific Evidence in a Pandemic: An Overview of TREC-COVID | 2021 | arXiv paper | https://arxiv.org/abs/2104.09632 |
| TREC-COVID data archive | 2020 | benchmark archive | https://ir.nist.gov/trec-covid/ |

## Machine-Readable Metadata

<!-- benchmark-task-metadata:v1 -->

```yaml
benchmark_task_metadata:
  schema_version: 1
  document_status: first_pass
  nano_set: NanoMedical
  backing_dataset: NanoMedical
  dataset_id: hakari-bench/NanoMedical
  task_name: NanoTRECCOVID
  split_name: NanoTRECCOVID
  language: en
  category: natural_language
  document_path: docs/benchmark_tasks/NanoMedical/NanoTRECCOVID.md
  source_research:
    primary_source_type: benchmark_paper
    paper_pdf_or_html_checked: true
    paper_url: https://arxiv.org/abs/2104.09632
    additional_source_urls:
    - https://ir.nist.gov/trec-covid/
  counts:
    queries: 50
    documents: 10000
    positive_qrels: 50
  positives_per_query:
    average: 1.0
    min: 1
    median: 1.0
    max: 1
    multi_positive_queries: 0
    multi_positive_query_percent: 0.0
  text_stats_chars:
    query_mean: 69.24
    document_mean: 1208.7826
  bm25:
    ndcg_at_10: 0.3983195524616401
    hit_at_10: 0.52
    source: dataset_candidate_subset
  learning:
    original_train_split: available_as_prior_round_or_feedback_judgments
    evaluation_split_origin: TREC-COVID retrieval split sampled into NanoMedical
    train_eval_overlap_audit: not_audited
    leakage_note: exclude TREC-COVID Complete qrels for evaluation topics and exact
      CORD-19 positive documents from this Nano split for clean zero-shot evaluation
    useful_training_data:
    - non-overlapping COVID-19 literature retrieval judgments
    - biomedical ad hoc retrieval data
    - clinical and public-health question-to-abstract data
    - coronavirus and influenza hard negatives
    synthetic_data:
      document_generation: COVID-19 and coronavirus title-plus-abstract passages
      question_generation: clinical, biological, or public-health pandemic information
        needs
      hard_negatives: same-COVID-vocabulary documents with different intervention,
        population, outcome, or virus family
      answerability: the document should contain evidence responsive to the information
        need
    multi_positive_training: single_positive_question_document_focus_in_this_nano_split
  links:
    nano_dataset: https://huggingface.co/datasets/hakari-bench/NanoMedical
    source_urls:
    - label: TREC-COVID arXiv
      url: https://arxiv.org/abs/2104.09632
    - label: TREC-COVID archive
      url: https://ir.nist.gov/trec-covid/
  candidate_subsets:
    bm25:
      config: bm25
      label: BM25
      source: dataset_candidate_subset
      top_k: 500
      ndcg_at_10: 0.3983195525
      hit_at_10: 0.52
      recall_at_100: 0.8
      candidate_count_min: 500
      candidate_count_max: 500
      candidate_count_mean: 500.0
      query_count: 50
      query_coverage: 1.0
      relevant_coverage_at_100: 0.8
    dense:
      config: harrier_oss_v1_270m
      label: Dense
      source: dataset_candidate_subset
      top_k: 500
      ndcg_at_10: 0.3874516535
      hit_at_10: 0.52
      recall_at_100: 0.7
      candidate_count_min: 500
      candidate_count_max: 500
      candidate_count_mean: 500.0
      query_count: 50
      query_coverage: 1.0
      relevant_coverage_at_100: 0.7
    reranking_hybrid:
      config: reranking_hybrid
      label: Reranking hybrid
      source: dataset_candidate_subset
      top_k: 100
      ndcg_at_10: 0.3192729308
      hit_at_10: 0.44
      recall_at_100: 0.96
      candidate_count_min: 100
      candidate_count_max: 101
      candidate_count_mean: 100.04
      query_count: 50
      query_coverage: 1.0
      relevant_coverage_at_100: 0.96
      safeguard_positive_rows: 2
      rows_with_101_candidates: 2
```
