# NanoIFIR / NanoIFIRAila

## Overview

`NanoIFIRAila` is an instruction-following legal retrieval task. Queries are
long English legal fact patterns adapted from AILA-style Indian Supreme Court
case scenarios, and documents are full prior case judgments. The retriever must
find prior cases that satisfy the legal information need expressed in the
instruction.

## Details

### What the Original Data Measures

[IFIR: A Comprehensive Benchmark for Evaluating Instruction-Following in Expert-Domain Information Retrieval](https://arxiv.org/abs/2503.04644)
introduces expert-domain instruction-following IR across finance, law,
healthcare, and scientific literature. IFIR augments established expert-domain
IR benchmarks with detailed instructions, then reviews and refines them with
domain experts. For the legal domain, IFIR uses AILA and FIRE-style legal case
retrieval to simulate lawyers looking for prior cases under customized demands.

[Overview of the FIRE 2019 AILA Track](https://ceur-ws.org/Vol-2517/T1-1.pdf)
defines AILA as legal assistance over Indian Supreme Court material. Its
precedent retrieval task gives a factual situation in natural English and asks
systems to retrieve similar or relevant prior case documents; the track provided
2,914 prior case documents.

### Observed Data Profile

The Nano split has 40 queries, 2,914 documents, and 119 positive qrels. Queries
average 2,889.40 characters, and documents average 19,987.82 characters. The
queries are full legal narratives about appeals, criminal proceedings, land
acquisition, trial evidence, and procedural issues. Documents are long Indian
Supreme Court judgments, frequently with citations, procedural history, legal
issues, and reasoning.

Most queries are multi-positive: 30 of 40 queries have more than one relevant
case, with up to 10 positives.

### BM25 Difficulty

Using the dataset-provided BM25 candidate column, BM25 reaches nDCG@10 =
0.1051 and hit@10 = 0.2250. BM25 ranks only 4 positives first. This is hard for
lexical retrieval because both queries and documents are long, and the relevant
link is based on legal analogy, precedent value, and fact-pattern similarity
rather than simple term overlap.

### Training Data That May Help

Useful training data includes non-overlapping AILA precedent retrieval pairs,
Indian Supreme Court citation graphs, legal case similarity data, and hard
negatives from the same legal issue or statute. Training should preserve
multi-positive relevance and avoid using Nano queries, qrels, or cited positive
cases from this split.

### Synthetic Data Guidance

Generate long legal fact patterns with parties, procedural posture, disputed
issues, and the desired legal perspective. Positives should be prior judgments
with analogous facts or reasoning. Hard negatives should share statutes or broad
topics but differ on material facts, procedural posture, or legal standard.

## Example Data

| Query | Positive document |
| --- | --- |
| These appeals involve a pure question of law as to whether an award by which residue assets of a partnership firm are distributed amongst the partners on dissolution of the partnership firm requires registration. Briefly the ... [truncated 225 chars](1668 chars) | S. V. Chandra Pandian and Others v S. V. Sivalinga Nadar and Others 11 January 1993 C.As. Nos. 17491752 of 1992 The Judgment was delivered by : Hon'ble Justice A. M. Ahmadi 1. The four appellants and respondents 1 and 2 are b ... [truncated 225 chars](45845 chars) |
| The detenu P1, a French national, at the relevant time was employed as Airport Manager by A1 in L1. By an A1 flight, on September 20, 1981, he arrived at International Airport, L2 and passed through green channel indicating h ... [truncated 225 chars](4806 chars) | Kavita w/o Sunder Shankardas Devidasani and another v State of Maharashtra and Others 28 July 1981 Writ Petition (Criminal) No. 2690 of 1981. (Under article 32 of the Constitution of India) AND Writ Petition (Criminal) No. 32 ... [truncated 225 chars](19115 chars) |
| The appellant before us was examined as prime witness in the trial of T.R. on the file of the Special Judge against the first respondent. The trial ended in conviction against the first respondent and when the appeal filed by ... [truncated 225 chars](2857 chars) | R. K. Lakshmanan v A. K. Srinivasan and Another 1 August 1975 CRIMINAL APPELLATE JURISDICTION : Criminal Appeal No. 1 30 of 1975. Appeal by Special Leave from the Judgment and Order dated the 13th March, 1974 of the Kerala Hi ... [truncated 225 chars](15767 chars) |
| Appellant before us was detained. He is the Managing Director of a company, registered and incorporated as CompanyC1. It was an exporter and held a valid licence therefor. The company was to export products of alloy steel. Up ... [truncated 225 chars](3045 chars) | Rajinder Arora v Union of India and Others 10 March 2006 Appeal (Crl.) 311 of 2006 The Judgment was delivered by : S. B. Sinha, J. Leave granted. 1. The Appellant is an industrialist. He manufactures acrylic yarn, blankets an ... [truncated 225 chars](17845 chars) |
| The hearing before us now relates to certain objections filed to the Award made by a former Judge of this Court who was appointed the sole arbitrator to adjudicate upon the dispute between the parties pursuant to the Order of ... [truncated 225 chars](5936 chars) | K. P. Poulose v State Of Kerala & Anr 21 April 1975 CIVIL A PPELLATE JURISDICTION CIVIL APPEAL No. 1485 OF 1974 Appeal by special leave from the judgment and decree Dt. 29-1-73 of the Kerala High Court in A.S. No. 357 of 1972 ... [truncated 225 chars](9716 chars) |

## Dataset Information

| Field | Value |
| --- | --- |
| Nano set | NanoIFIR |
| Backing dataset | NanoIFIR |
| Task / split | NanoIFIRAila |
| Hugging Face dataset | [hakari-bench/NanoIFIR](https://huggingface.co/datasets/hakari-bench/NanoIFIR) |
| Language | en |
| Category | natural_language |
| Queries | 40 |
| Documents | 2,914 |
| Positive qrels | 119 |
| Positives per query | avg 2.98 / min 1 / median 2.0 / max 10 |
| Multi-positive queries | 30 (75.00%) |
| BM25 nDCG@10 | 0.0988 |
| BM25 hit@10 | 0.2000 |
| BM25 Recall@100 | 0.3361 |
| BM25 candidate subset | top-500 (`bm25`) |
| Dense nDCG@10 | 0.0878 |
| Dense hit@10 | 0.2750 |
| Dense Recall@100 | 0.3950 |
| Dense candidate subset | top-500 (`harrier_oss_v1_270m`) |
| Reranking hybrid nDCG@10 | 0.0798 |
| Reranking hybrid hit@10 | 0.2000 |
| Reranking hybrid Recall@100 | 0.4034 |
| Reranking hybrid candidate subset | top-100 plus optional rank-101 safeguard (`reranking_hybrid`) |
| Reranking hybrid candidates / query | 100-101 |
| Reranking hybrid safeguard rows | 21 |
| Query length avg chars | 2,889.40 |
| Document length avg chars | 19,987.82 |

### Public Sources

- [IFIR: A Comprehensive Benchmark for Evaluating Instruction-Following in Expert-Domain Information Retrieval](https://arxiv.org/abs/2503.04644); 2025; Tingyu Song et al.
- [Overview of the FIRE 2019 AILA Track: Artificial Intelligence for Legal Assistance](https://ceur-ws.org/Vol-2517/T1-1.pdf); 2019; Paheli Bhattacharya et al.

### Hugging Face Links

- Nano dataset: [hakari-bench/NanoIFIR](https://huggingface.co/datasets/hakari-bench/NanoIFIR)

### Source Reference Table

| Title | Year | Type | URL |
| --- | ---: | --- | --- |
| IFIR: A Comprehensive Benchmark for Evaluating Instruction-Following in Expert-Domain Information Retrieval | 2025 | arXiv paper | https://arxiv.org/abs/2503.04644 |
| Overview of the FIRE 2019 AILA Track: Artificial Intelligence for Legal Assistance | 2019 | CEUR paper | https://ceur-ws.org/Vol-2517/T1-1.pdf |

## Machine-Readable Metadata

<!-- benchmark-task-metadata:v1 -->

```yaml
benchmark_task_metadata:
  schema_version: 1
  document_status: first_pass
  nano_set: NanoIFIR
  backing_dataset: NanoIFIR
  dataset_id: hakari-bench/NanoIFIR
  task_name: NanoIFIRAila
  split_name: NanoIFIRAila
  language: en
  category: natural_language
  document_path: docs/benchmark_tasks/NanoIFIR/NanoIFIRAila.md
  source_research:
    primary_source_type: benchmark_paper_and_task_paper
    paper_pdf_or_html_checked: true
    no_paper_note: null
  counts:
    queries: 40
    documents: 2914
    positive_qrels: 119
  positives_per_query:
    average: 2.975
    min: 1
    median: 2.0
    max: 10
    multi_positive_queries: 30
    multi_positive_query_percent: 75.0
  text_stats_chars:
    query_mean: 2889.4
    document_mean: 19987.820178448866
  bm25:
    ndcg_at_10: 0.09884050780615407
    hit_at_10: 0.2
    source: dataset_candidate_subset
  learning:
    original_train_split: available
    evaluation_split_origin: ifir_adapted
    train_eval_overlap_audit: not_audited
    leakage_note: exclude NanoIFIRAila queries, qrels, and positive prior-case documents
    useful_training_data:
    - non-overlapping AILA precedent retrieval pairs
    - Indian Supreme Court citation graphs
    - legal case similarity datasets
    - same-statute legal hard negatives
    synthetic_data:
      document_generation: long Indian Supreme Court-style judgments with issues,
        facts, citations, and reasoning
      question_generation: legal fact patterns with explicit retrieval instructions
        and desired precedent constraints
      answerability: positives should be prior cases satisfying the legal analogy
        or instruction constraints
    multi_positive_training: preserve_multiple_relevant_prior_cases
  links:
    nano_dataset: https://huggingface.co/datasets/hakari-bench/NanoIFIR
    source_urls:
    - label: IFIR arXiv
      url: https://arxiv.org/abs/2503.04644
    - label: AILA 2019 overview
      url: https://ceur-ws.org/Vol-2517/T1-1.pdf
    source_notes: []
  references:
  - title: 'IFIR: A Comprehensive Benchmark for Evaluating Instruction-Following in
      Expert-Domain Information Retrieval'
    url: https://arxiv.org/abs/2503.04644
    year: 2025
    doi: 10.18653/v1/2025.naacl-long.511
    is_paper: true
    source_confidence: definitive_paper_link
  candidate_subsets:
    bm25:
      config: bm25
      label: BM25
      source: dataset_candidate_subset
      top_k: 500
      ndcg_at_10: 0.0988405078
      hit_at_10: 0.2
      recall_at_100: 0.3361344538
      candidate_count_min: 500
      candidate_count_max: 500
      candidate_count_mean: 500.0
      query_count: 40
      query_coverage: 1.0
      relevant_coverage_at_100: 0.3361344538
    dense:
      config: harrier_oss_v1_270m
      label: Dense
      source: dataset_candidate_subset
      top_k: 500
      ndcg_at_10: 0.0878033668
      hit_at_10: 0.275
      recall_at_100: 0.3949579832
      candidate_count_min: 500
      candidate_count_max: 500
      candidate_count_mean: 500.0
      query_count: 40
      query_coverage: 1.0
      relevant_coverage_at_100: 0.3949579832
    reranking_hybrid:
      config: reranking_hybrid
      label: Reranking hybrid
      source: dataset_candidate_subset
      top_k: 100
      ndcg_at_10: 0.0797521737
      hit_at_10: 0.2
      recall_at_100: 0.4033613445
      candidate_count_min: 100
      candidate_count_max: 101
      candidate_count_mean: 100.525
      query_count: 40
      query_coverage: 1.0
      relevant_coverage_at_100: 0.4033613445
      safeguard_positive_rows: 21
      rows_with_101_candidates: 21
```
