# NanoMTEB-Dutch / sci_fact_nl

## Overview

`sci_fact_nl` is the Dutch SciFact retrieval task from BEIR-NL and MTEB-NL.
Queries are Dutch translations of scientific claims, and documents are
translated scientific-paper abstracts. The task measures evidence retrieval for
scientific fact verification, where the relevant abstract supports or refutes a
claim.

## Details

### What the Original Data Measures

[Fact or Fiction: Verifying Scientific Claims](https://arxiv.org/abs/2004.14974)
introduces SciFact as a scientific claim verification dataset with 1.4K
expert-written claims and a corpus of 5,183 abstracts. Claims are paired with
abstracts that SUPPORT or REFUTE them, and evidence rationales are annotated.
[BEIR](https://arxiv.org/abs/2104.08663) uses SciFact as scientific-domain
retrieval: retrieve evidence abstracts for a claim.

[BEIR-NL](https://aclanthology.org/2025.bucc-1.5/) translates BEIR datasets into
Dutch. This task is thus a Dutch translated scientific evidence retrieval task,
not a natively authored Dutch scientific-claim dataset.

### Observed Data Profile

The Nano split has 200 queries, 5,183 documents, and 226 positive qrel rows.
Most claims have one positive; 16 queries have multiple positives and the
maximum is 5. Queries average 100.13 characters and are scientific claims.
Documents average 1,640.32 characters and resemble full abstracts with titles,
methods, measurements, and biomedical terminology.

Examples include claims about cardiopulmonary fitness, ADAR1 and Dicer,
headache and cognitive decline, transcript start sites, and alcohol aldehyde
dehydrogenase deficiency. These are precise scientific relations, not broad
topic searches.

### BM25 Difficulty

Using the dataset-provided BM25 candidate column, BM25 reaches nDCG@10 = 0.6160
and hit@10 = 0.7900. Lexical cues such as gene names and technical terms help,
but relevance depends on whether the abstract provides evidence for the claim.

The task is harder than ordinary keyword retrieval because abstracts can mention
the same entities while supporting a different conclusion. Dense models need
scientific relation matching and should handle translated technical terms.

### Training Data That May Help

Useful training data includes SciFact training data, non-overlapping scientific
claim verification datasets, biomedical abstract retrieval pairs, and Dutch or
multilingual scientific evidence retrieval data. The translated SciFact test
queries, qrels, abstracts, and evidence positives used here should be excluded.

Because most queries are single-positive but some have multiple positives,
training can use a single-positive objective while retaining multi-positive
labels when available.

### Synthetic Data Guidance

For document-to-query generation, use non-evaluation scientific abstracts and
generate precise Dutch claims that can be supported or refuted from the
abstract. Claims should include measurements, interventions, entities, or
biological relations.

For joint generation, create Dutch abstract-style documents with realistic
methods and findings, then generate scientific claims grounded in those
findings. Hard negatives should share terminology but imply a different result
or relation.

## Example Data

| Query | Positive document |
| --- | --- |
| Metastatische colorectale kanker behandeld met enkelvoudige fluoropyrimidinen resulteerde in verminderde werkzaamheid en lagere kwaliteit van leven in vergelijking met oxaliplatine-gebaseerde chemotherapie bij oudere patiënte ... [truncated 225 chars](227 chars) | Chemotherapieopties bij oudere en kwetsbare patiënten met metastatische colorectale kanker (MRC FOCUS2): een open-label, gerandomiseerde factorieel onderzoek ACHTERGROND Oudere en kwetsbare patiënten met kanker, hoewel vaak b ... [truncated 225 chars](3389 chars) |
| CRP is geen voorspeller van postoperatieve mortaliteit na een coronaire arteriële bypass graft (CABG) operatie. (111 chars) | Beoordeling van de kosteneffectiviteit van het gebruik van prognostische biomarkers met beslissingsmodellen: een casestudy naar prioritering van patiënten in afwachting van coronaire bypass-chirurgie DOEL De effectiviteit en ... [truncated 225 chars](3250 chars) |
| Arginine 90 in p150n is belangrijk voor de interactie met EB1. (62 chars) | Structurele basis voor de activatie van microtubulusassemblage door het EB1 en p150Glued complex. Plus-eind trackende eiwitten, zoals EB1 en het dyneïne/dynactine complex, reguleren microtubulusdynamiek. Aangenomen wordt dat ... [truncated 225 chars](1328 chars) |
| Obesitas wordt uitsluitend bepaald door omgevingsfactoren. (58 chars) | Genetica van obesitas bij volwassen adoptiekinderen en hun biologische broers en zussen. Er werd een adoptiestudie uitgevoerd naar genetische effecten op obesitas bij volwassenen, waarbij adoptiekinderen die zeer vroeg in hun ... [truncated 225 chars](1648 chars) |
| Koortsstuipen verhogen de drempel voor het ontwikkelen van epilepsie. (69 chars) | Febriele insulten in de zich ontwikkelende hersenen leiden tot blijvende verandering van neuronale excitabiliteit in limbische circuits Febriele (koortsgeïnduceerde) insulten treffen 3–5% van de zuigelingen en jonge kinderen. ... [truncated 225 chars](915 chars) |

## Dataset Information

| Field | Value |
| --- | --- |
| Nano set | NanoMTEB-Dutch |
| Backing dataset | NanoMTEB-Dutch |
| Task / split | sci_fact_nl |
| Hugging Face dataset | [hakari-bench/NanoMTEB-Dutch](https://huggingface.co/datasets/hakari-bench/NanoMTEB-Dutch) |
| Source dataset | [clips/beir-nl-scifact](https://huggingface.co/datasets/clips/beir-nl-scifact) |
| Language | nl |
| Category | natural_language |
| Queries | 200 |
| Documents | 5,183 |
| Positive qrels | 226 |
| Avg positives / query | 1.13 |
| Positives per query (min / median / max) | 1 / 1 / 5 |
| Queries with multiple positives | 16 (8.00%) |
| BM25 nDCG@10 | 0.6160 |
| BM25 hit@10 | 0.7900 |
| BM25 Recall@100 | 0.8363 |
| BM25 candidate subset | top-500 (`bm25`) |
| Dense nDCG@10 | 0.6758 |
| Dense hit@10 | 0.8300 |
| Dense Recall@100 | 0.9336 |
| Dense candidate subset | top-500 (`harrier_oss_v1_270m`) |
| Reranking hybrid nDCG@10 | 0.6709 |
| Reranking hybrid hit@10 | 0.8200 |
| Reranking hybrid Recall@100 | 0.9558 |
| Reranking hybrid candidate subset | top-100 plus optional rank-101 safeguard (`reranking_hybrid`) |
| Reranking hybrid candidates / query | 100-101 |
| Reranking hybrid safeguard rows | 10 |
| Query length avg chars | 100.13 |
| Document length avg chars | 1,640.32 |

### Public Sources

- [Fact or Fiction: Verifying Scientific Claims](https://arxiv.org/abs/2004.14974), 2020.
- [BEIR: A Heterogeneous Benchmark for Zero-shot Evaluation of Information Retrieval Models](https://arxiv.org/abs/2104.08663), 2021.
- [BEIR-NL: Zero-shot Information Retrieval Benchmark for the Dutch Language](https://aclanthology.org/2025.bucc-1.5/), 2025.
- [clips/beir-nl-scifact](https://huggingface.co/datasets/clips/beir-nl-scifact), source dataset card.

### Hugging Face Links

- Nano dataset: [hakari-bench/NanoMTEB-Dutch](https://huggingface.co/datasets/hakari-bench/NanoMTEB-Dutch)
- Source dataset: [clips/beir-nl-scifact](https://huggingface.co/datasets/clips/beir-nl-scifact)

### Source Reference Table

| Title | Year | Type | URL |
| --- | ---: | --- | --- |
| Fact or Fiction: Verifying Scientific Claims | 2020 | arXiv paper | https://arxiv.org/abs/2004.14974 |
| BEIR: A Heterogeneous Benchmark for Zero-shot Evaluation of Information Retrieval Models | 2021 | arXiv paper | https://arxiv.org/abs/2104.08663 |
| BEIR-NL: Zero-shot Information Retrieval Benchmark for the Dutch Language | 2025 | ACL paper | https://aclanthology.org/2025.bucc-1.5/ |
| clips/beir-nl-scifact |  | dataset card | https://huggingface.co/datasets/clips/beir-nl-scifact |

## Machine-Readable Metadata

<!-- benchmark-task-metadata:v1 -->

```yaml
benchmark_task_metadata:
  schema_version: 1
  document_status: first_pass
  nano_set: NanoMTEB-Dutch
  backing_dataset: NanoMTEB-Dutch
  dataset_id: hakari-bench/NanoMTEB-Dutch
  task_name: sci_fact_nl
  split_name: sci_fact_nl
  language: nl
  category: natural_language
  document_path: docs/benchmark_tasks/NanoMTEB-Dutch/sci_fact_nl.md
  source_research:
    primary_source_type: task_paper
    paper_pdf_or_html_checked: true
    paper_url: https://arxiv.org/abs/2004.14974
    additional_source_urls:
    - https://arxiv.org/abs/2104.08663
    - https://aclanthology.org/2025.bucc-1.5/
    - https://huggingface.co/datasets/clips/beir-nl-scifact
    no_paper_note: null
  counts:
    queries: 200
    documents: 5183
    positive_qrels: 226
  positives_per_query:
    average: 1.13
    min: 1
    median: 1.0
    max: 5
    multi_positive_queries: 16
    multi_positive_query_percent: 8.0
  text_stats_chars:
    query_mean: 100.13
    document_mean: 1640.316226124
  bm25:
    ndcg_at_10: 0.616037929182313
    hit_at_10: 0.79
    source: dataset_candidate_subset
  learning:
    original_train_split: available
    evaluation_split_origin: translated BEIR-NL SciFact test split from clips/beir-nl-scifact
    train_eval_overlap_audit: not_audited
    leakage_note: Exclude translated SciFact test claims, qrels, and evidence abstracts
      used by this Nano split.
    useful_training_data:
    - official SciFact training data with overlap removed
    - scientific claim verification retrieval datasets
    - biomedical abstract retrieval pairs
    - Dutch or multilingual scientific evidence pairs
    synthetic_data:
      document_generation: Dutch scientific abstracts with methods, measurements,
        entities, and findings.
      question_generation: Precise Dutch scientific claims supported or refuted by
        the abstract.
      answerability: Claims should be grounded in explicit findings, with terminology-sharing
        hard negatives.
    multi_positive_training: single_positive_question_document_focus
  links:
    nano_dataset: https://huggingface.co/datasets/hakari-bench/NanoMTEB-Dutch
    source_urls:
    - label: SciFact arXiv
      url: https://arxiv.org/abs/2004.14974
    - label: BEIR arXiv
      url: https://arxiv.org/abs/2104.08663
    - label: BEIR-NL ACL Anthology
      url: https://aclanthology.org/2025.bucc-1.5/
    - label: clips/beir-nl-scifact
      url: https://huggingface.co/datasets/clips/beir-nl-scifact
    source_notes: []
  references:
  - title: 'Fact or Fiction: Verifying Scientific Claims'
    url: https://arxiv.org/abs/2004.14974
    year: 2020
    doi: 10.48550/arXiv.2004.14974
    is_paper: true
    source_confidence: definitive_paper_link
  - title: 'BEIR: A Heterogeneous Benchmark for Zero-shot Evaluation of Information
      Retrieval Models'
    url: https://arxiv.org/abs/2104.08663
    year: 2021
    doi: 10.48550/arXiv.2104.08663
    is_paper: true
    source_confidence: definitive_paper_link
  - title: 'BEIR-NL: Zero-shot Information Retrieval Benchmark for the Dutch Language'
    url: https://aclanthology.org/2025.bucc-1.5/
    year: 2025
    doi: null
    is_paper: true
    source_confidence: definitive_paper_link
  - title: clips/beir-nl-scifact
    url: https://huggingface.co/datasets/clips/beir-nl-scifact
    year: null
    doi: null
    is_paper: false
    source_confidence: probably_correct
  candidate_subsets:
    bm25:
      config: bm25
      label: BM25
      source: dataset_candidate_subset
      top_k: 500
      ndcg_at_10: 0.6160379292
      hit_at_10: 0.79
      recall_at_100: 0.8362831858
      candidate_count_min: 500
      candidate_count_max: 500
      candidate_count_mean: 500.0
      query_count: 200
      query_coverage: 1.0
      relevant_coverage_at_100: 0.8362831858
    dense:
      config: harrier_oss_v1_270m
      label: Dense
      source: dataset_candidate_subset
      top_k: 500
      ndcg_at_10: 0.6758142619
      hit_at_10: 0.83
      recall_at_100: 0.9336283186
      candidate_count_min: 500
      candidate_count_max: 500
      candidate_count_mean: 500.0
      query_count: 200
      query_coverage: 1.0
      relevant_coverage_at_100: 0.9336283186
    reranking_hybrid:
      config: reranking_hybrid
      label: Reranking hybrid
      source: dataset_candidate_subset
      top_k: 100
      ndcg_at_10: 0.6709460898
      hit_at_10: 0.82
      recall_at_100: 0.9557522124
      candidate_count_min: 100
      candidate_count_max: 101
      candidate_count_mean: 100.05
      query_count: 200
      query_coverage: 1.0
      relevant_coverage_at_100: 0.9557522124
      safeguard_positive_rows: 10
      rows_with_101_candidates: 10
```
