# NanoMTEB-Scandinavian / dan_fever

## Overview

DanFEVER adapts the FEVER fact-verification setup to Danish misinformation
research, pairing Danish claims with evidence from Danish Wikipedia and Den
Store Danske. The Scandinavian benchmark converts that verification data into
retrieval: a Danish factual claim is the query and the target is the evidence
snippet that supports or refutes it. In this Nano split, the compact
encyclopedic corpus and claims about sports, institutions, science, and
television make named entities, dates, places, and titles strong but not
sufficient evidence cues.

## Details

### What the Original Data Measures

[DanFEVER: claim verification dataset for Danish](https://aclanthology.org/2021.nodalida-main.47/)
introduces a Danish FEVER-style fact verification dataset for misinformation
research. A FEVER instance pairs a claim with zero or more evidence pieces and
a label: supported, refuted, or not enough information. The paper reports 6,407
annotated Danish claims created from Danish Wikipedia and Den Store Danske.

The SEB benchmark converts DanFEVER into retrieval by using the claim as the
query and the evidence text as the corpus document. In this Nano split, each
claim has one positive evidence snippet.

### Observed Data Profile

The Nano split has 200 Danish queries, 2,522 documents, and 200 positive qrels.
Every query has one positive. Queries average 59.48 characters, and documents
average 312.00 characters. Sampled claims cover sports tournaments, public
institutions, science terms, and television facts.

The corpus is compact and encyclopedic. Many positives repeat named entities,
dates, places, or titles from the claim, so surface matching is often strong.

### BM25 Difficulty

Using the dataset-provided BM25 candidate column, BM25 reaches nDCG@10 =
0.8856 and hit@10 = 0.9900. BM25 ranks 145 positives first and 198 positives in
the top 10. This is a lexically favorable retrieval task, though a few claims
still require handling paraphrase or near-synonymous Danish wording.

### Training Data That May Help

Useful training data includes non-overlapping DanFEVER training claims,
Danish FEVER-style claim/evidence pairs, Danish Wikipedia retrieval pairs, and
hard negatives from related encyclopedia pages. Training should exclude Nano
queries, qrels, and evidence snippets from this evaluation split.

### Synthetic Data Guidance

Generate Danish encyclopedia-style evidence snippets and claims that either
state the same fact, negate a detail, or replace an entity/date with a plausible
alternative. Hard negatives should share the same title, entity class, or date
range but fail to verify the exact claim.

## Example Data

| Query | Positive document |
| --- | --- |
| Albummet Blood Mountain har en sammenhængde historie og et gennemgående tema. (77 chars) | Blood Mountain er et konceptalbum af heavy metal-gruppen Mastodon. Det er Mastodons tredje studiealbum og blev udgivet i september 2006. Som det foregående album Leviathan er Blood Mountain et konceptalbum med en sammenhængen ... [truncated 225 chars](261 chars) |
| Den almindelige perlebusk får perleformede knopper og derefter hvide blomster på dens busk. (91 chars) | Almindelig perlebusk ("Exochorda racemosa") er en mellemstor, løvfældende busk med en opret vækst og iøjnefaldende klaser af hvide, perleformede knopper og senere hvide blomster. Busken er fuldt hårdfør og bruges som prydbusk ... [truncated 225 chars](236 chars) |
| .my er det malaysiske topdomæne. (32 chars) | .my er et nationalt topdomæne der er reserveret til Malaysia. (61 chars) |
| Adelen i Storbritannien er den øverste klasse i Storbritannien. (63 chars) | Adelen i Storbritannien (egentlig: Det Forenede Kongerige Storbritannien og Nordirland) er den øverste samfundsklasse i det britiske samfund og har historisk været bærer af nogle særlige titler, rettigheder og privilegier. En ... [truncated 225 chars](317 chars) |
| Den 31. oktober 1920 opdagede en astronom småplaneten (944) Hidalgo i det ydre solsystem. (89 chars) | (944) Hidalgo (oprindeligt midlertidigt navn: 1920 HZ) er en mørk småplanet med en diameter på ca. 50 km, der befinder sig i det ydre solsystem. Objektet blev opdaget den 31. oktober 1920 af Walter Baade. Walter Baade (født 2 ... [truncated 225 chars](635 chars) |

## Dataset Information

| Field | Value |
| --- | --- |
| Nano set | NanoMTEB-Scandinavian |
| Backing dataset | NanoMTEB-Scandinavian |
| Task / split | dan_fever |
| Hugging Face dataset | [hakari-bench/NanoMTEB-Scandinavian](https://huggingface.co/datasets/hakari-bench/NanoMTEB-Scandinavian) |
| Language | da |
| Category | natural_language |
| Queries | 200 |
| Documents | 2,522 |
| Positive qrels | 200 |
| BM25 nDCG@10 | 0.8856 |
| BM25 hit@10 | 0.9900 |
| BM25 Recall@100 | 1.0000 |
| BM25 candidate subset | top-500 (`bm25`) |
| Dense nDCG@10 | 0.8630 |
| Dense hit@10 | 0.9700 |
| Dense Recall@100 | 0.9700 |
| Dense candidate subset | top-500 (`harrier_oss_v1_270m`) |
| Reranking hybrid nDCG@10 | 0.8832 |
| Reranking hybrid hit@10 | 0.9750 |
| Reranking hybrid Recall@100 | 1.0000 |
| Reranking hybrid candidate subset | top-100 plus optional rank-101 safeguard (`reranking_hybrid`) |
| Reranking hybrid candidates / query | 100 |
| Reranking hybrid safeguard rows | 0 |
| Query length avg chars | 59.48 |
| Document length avg chars | 312.00 |

### Public Sources

- [The Scandinavian Embedding Benchmarks](https://arxiv.org/abs/2406.02396); 2024; Kenneth Enevoldsen et al.
- [DanFEVER: claim verification dataset for Danish](https://aclanthology.org/2021.nodalida-main.47/); 2021; Jeppe Nørregaard and Leon Derczynski.
- [strombergnlp/danfever dataset card](https://huggingface.co/datasets/strombergnlp/danfever).

### Hugging Face Links

- Nano dataset: [hakari-bench/NanoMTEB-Scandinavian](https://huggingface.co/datasets/hakari-bench/NanoMTEB-Scandinavian)
- Source dataset: [strombergnlp/danfever](https://huggingface.co/datasets/strombergnlp/danfever)

### Source Reference Table

| Title | Year | Type | URL |
| --- | ---: | --- | --- |
| The Scandinavian Embedding Benchmarks | 2024 | arXiv paper | https://arxiv.org/abs/2406.02396 |
| DanFEVER: claim verification dataset for Danish | 2021 | ACL Anthology paper | https://aclanthology.org/2021.nodalida-main.47/ |
| strombergnlp/danfever | 2021 | dataset card | https://huggingface.co/datasets/strombergnlp/danfever |

## Machine-Readable Metadata

<!-- benchmark-task-metadata:v1 -->

```yaml
benchmark_task_metadata:
  schema_version: 1
  document_status: first_pass
  nano_set: NanoMTEB-Scandinavian
  backing_dataset: NanoMTEB-Scandinavian
  dataset_id: hakari-bench/NanoMTEB-Scandinavian
  task_name: dan_fever
  split_name: dan_fever
  language: da
  category: natural_language
  document_path: docs/benchmark_tasks/NanoMTEB-Scandinavian/dan_fever.md
  source_research:
    primary_source_type: task_paper
    paper_pdf_or_html_checked: true
    no_paper_note: null
  counts:
    queries: 200
    documents: 2522
    positive_qrels: 200
  positives_per_query:
    average: 1.0
    min: 1
    median: 1.0
    max: 1
    multi_positive_queries: 0
    multi_positive_query_percent: 0.0
  text_stats_chars:
    query_mean: 59.475
    document_mean: 311.99722442505947
  bm25:
    ndcg_at_10: 0.8856498970178633
    hit_at_10: 0.99
    source: dataset_candidate_subset
  learning:
    original_train_split: available
    evaluation_split_origin: train
    train_eval_overlap_audit: not_audited
    leakage_note: exclude Nano queries, qrels, and DanFEVER evidence snippets used
      in this split
    useful_training_data:
    - non-overlapping DanFEVER claim/evidence pairs
    - Danish Wikipedia retrieval pairs
    - Danish fact verification hard negatives
    - same-entity encyclopedia negatives
    synthetic_data:
      document_generation: Danish encyclopedia-style evidence snippets with named
        entities, dates, places, and factual statements
      question_generation: Danish FEVER-style claims that preserve, negate, or alter
        evidence facts
      answerability: each positive evidence snippet should verify or contradict the
        exact claim
    multi_positive_training: single_positive_claim_evidence_focus
  links:
    nano_dataset: https://huggingface.co/datasets/hakari-bench/NanoMTEB-Scandinavian
    source_urls:
    - label: Scandinavian Embedding Benchmarks
      url: https://arxiv.org/abs/2406.02396
    - label: DanFEVER paper
      url: https://aclanthology.org/2021.nodalida-main.47/
    - label: strombergnlp/danfever
      url: https://huggingface.co/datasets/strombergnlp/danfever
    source_notes: []
  references:
  - title: 'DanFEVER: claim verification dataset for Danish'
    url: https://aclanthology.org/2021.nodalida-main.47/
    year: 2021
    doi: null
    is_paper: true
    source_confidence: definitive_paper_link
  candidate_subsets:
    bm25:
      config: bm25
      label: BM25
      source: dataset_candidate_subset
      top_k: 500
      ndcg_at_10: 0.885649897
      hit_at_10: 0.99
      recall_at_100: 1.0
      candidate_count_min: 500
      candidate_count_max: 500
      candidate_count_mean: 500.0
      query_count: 200
      query_coverage: 1.0
      relevant_coverage_at_100: 1.0
    dense:
      config: harrier_oss_v1_270m
      label: Dense
      source: dataset_candidate_subset
      top_k: 500
      ndcg_at_10: 0.8629927163
      hit_at_10: 0.97
      recall_at_100: 0.97
      candidate_count_min: 500
      candidate_count_max: 500
      candidate_count_mean: 500.0
      query_count: 200
      query_coverage: 1.0
      relevant_coverage_at_100: 0.97
    reranking_hybrid:
      config: reranking_hybrid
      label: Reranking hybrid
      source: dataset_candidate_subset
      top_k: 100
      ndcg_at_10: 0.8831514809
      hit_at_10: 0.975
      recall_at_100: 1.0
      candidate_count_min: 100
      candidate_count_max: 100
      candidate_count_mean: 100.0
      query_count: 200
      query_coverage: 1.0
      relevant_coverage_at_100: 1.0
      safeguard_positive_rows: 0
      rows_with_101_candidates: 0
```
