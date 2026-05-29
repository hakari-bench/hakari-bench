# NanoIFIR

## Overview

NanoIFIR is the compact Nano subset of IFIR, an instruction-following retrieval
benchmark for expert-domain search. The group covers legal, clinical,
financial, medical/nutrition, precision-medicine, and scientific-evidence
retrieval. Its queries are not just keyword information needs; they are often
instructions or case descriptions that specify the role, context, or type of
evidence the retriever should return.

This group is useful for evaluating whether a model can follow nuanced
expert-domain retrieval intent. A document can be topically related but still
wrong if it does not satisfy the legal precedent need, patient profile,
financial question, clinical decision, or scientific claim instruction.

## Details

### What the Original Group Measures

[IFIR: A Comprehensive Benchmark for Evaluating Instruction-Following in Expert-Domain Information Retrieval](https://aclanthology.org/2025.naacl-long.511/)
introduces retrieval tasks where the query includes expert-domain instructions
and the retriever must respect those instructions. NanoIFIR samples seven IFIR
task families: AILA-style legal retrieval, clinical decision support, FiQA
finance, FIRE legal precedent retrieval, NFCorpus medical/nutrition retrieval,
precision-medicine clinical trial retrieval, and SciFact scientific evidence
retrieval.

The group emphasizes specialized evidence and constraints. Long legal fact
patterns must retrieve prior cases, clinical scenarios must retrieve relevant
medical literature, precision-medicine cases must match trial eligibility, and
scientific claims must retrieve supporting or refuting abstracts.

### Subtask Coverage

- **NanoIFIRAila:** long legal fact patterns retrieving relevant prior case
  judgments.
- **NanoIFIRCds:** clinical decision support queries retrieving biomedical
  article-like evidence.
- **NanoIFIRFiQA:** personal finance questions retrieving answer or advice
  passages.
- **NanoIFIRFire:** legal precedent retrieval from long case summaries and
  citation-context instructions.
- **NanoIFIRNFCorpus:** lay health and nutrition questions retrieving medical
  research documents.
- **NanoIFIRPm:** precision-medicine patient profiles retrieving relevant
  clinical trials.
- **NanoIFIRScifact:** scientific claims retrieving evidence abstracts.

All subtasks are English natural-language retrieval tasks. Every subtask has
multi-positive queries, so this group should be trained and interpreted with
multi-positive relevance in mind.

### Observed Group Profile

The task pages report 637 queries, 3,872 positive qrels, and 48,246 split-local
candidate documents. Average positives per query is 6.08, with 588
multi-positive queries. `NanoIFIRPm` is especially multi-positive, averaging
20.63 relevant clinical trials per query.

Query length varies sharply by domain. Legal tasks are much longer:
`NanoIFIRFire` averages 3,279.50 characters and `NanoIFIRAila` averages
2,889.40 characters. Finance, NFCorpus, and SciFact queries are much shorter.
Documents average 3,569.62 characters overall, but legal documents are far
longer than the finance or scientific abstract corpora.

### BM25 Difficulty

Using the dataset-provided BM25 candidate columns, NanoIFIR has query-weighted
BM25 nDCG@10 = 0.3069 and hit@10 = 0.6499. The strongest subtask is
`NanoIFIRScifact` (nDCG@10 = 0.7820, hit@10 = 1.0000), where scientific claims
and abstracts often share domain terms. `NanoIFIRFire` and `NanoIFIRPm` are in
the middle, helped by legal or biomedical terminology and many positives.

The weakest tasks are `NanoIFIRAila` (0.1051) and `NanoIFIRCds` (0.1345). These
tasks require interpreting long legal or clinical instructions and matching
evidence under constraints. BM25 can find topical documents, but it often misses
the instruction-following part of relevance.

### Training Data That May Help

Useful training data includes IFIR-style instruction-query retrieval pairs,
legal case retrieval, clinical decision support retrieval, FiQA-style finance
QA, NFCorpus-style medical literature retrieval, precision-medicine
patient-to-trial matching, and SciFact claim-evidence pairs. Because every
subtask is multi-positive, training should preserve multiple relevant documents
and use listwise or multi-positive objectives where possible.

Training should exclude NanoIFIR evaluation queries, qrels, and positive
documents. Public expert-domain sources are small and sometimes reused across
benchmarks, so source split and text-overlap audits are important before
training.

### Synthetic Data Guidance

Synthetic data should include both the expert-domain document and the
instructional query. Legal examples should include facts, issues, and requested
precedent type. Medical and precision-medicine examples should include patient
attributes, diagnosis, treatment, biomarkers, or trial criteria. Finance
examples should distinguish investment, risk, tax, and personal advice intents.
Scientific examples should include claims and evidence-bearing abstracts.

Generated positives must satisfy the instruction, not merely share topic words.
Hard negatives should be topically close but fail a key constraint, such as an
ineligible clinical trial, a case with the wrong legal issue, or a paper about a
related but different claim.

## Task Summary

| Task | Retrieval focus | Queries | Docs | Positive qrels | BM25 nDCG@10 | BM25 hit@10 | Query avg chars | Doc avg chars |
| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| [NanoIFIRAila](NanoIFIRAila.md) | legal fact pattern to prior case judgment | 40 | 2,914 | 119 | 0.1051 | 0.2250 | 2,889.40 | 19,987.81 |
| [NanoIFIRCds](NanoIFIRCds.md) | clinical case to biomedical evidence | 42 | 10,000 | 466 | 0.1345 | 0.4762 | 225.21 | 1,627.50 |
| [NanoIFIRFiQA](NanoIFIRFiQA.md) | finance question to advice passage | 200 | 10,000 | 1,010 | 0.2252 | 0.6100 | 65.79 | 788.36 |
| [NanoIFIRFire](NanoIFIRFire.md) | legal case summary to precedent document | 167 | 1,739 | 563 | 0.3704 | 0.7365 | 3,279.50 | 27,167.57 |
| [NanoIFIRNFCorpus](NanoIFIRNFCorpus.md) | health topic to medical research evidence | 86 | 3,593 | 242 | 0.2833 | 0.5698 | 37.80 | 1,589.52 |
| [NanoIFIRPm](NanoIFIRPm.md) | precision-medicine case to clinical trial | 59 | 10,000 | 1,217 | 0.3522 | 0.8136 | 145.73 | 2,233.61 |
| [NanoIFIRScifact](NanoIFIRScifact.md) | scientific claim to evidence abstract | 43 | 10,000 | 255 | 0.7820 | 1.0000 | 73.63 | 1,452.55 |

## Dataset Information

| Field | Value |
| --- | --- |
| Nano set | NanoIFIR |
| Backing dataset | NanoIFIR |
| Hugging Face dataset | [hakari-bench/NanoIFIR](https://huggingface.co/datasets/hakari-bench/NanoIFIR) |
| Language | en |
| Category | natural language |
| Subtasks | 7 |
| Total queries | 637 |
| Split-local documents | 48,246 |
| Positive qrels | 3,872 |
| Average positives / query | 6.08 |
| Queries with multiple positives | 588 |
| Query-weighted BM25 nDCG@10 | 0.3649 |
| Query-weighted BM25 hit@10 | 0.7190 |
| Query-weighted BM25 Recall@100 | 0.6345 |
| Query-weighted Dense nDCG@10 | 0.4591 |
| Query-weighted Dense hit@10 | 0.7771 |
| Query-weighted Dense Recall@100 | 0.7377 |
| Query-weighted Reranking hybrid nDCG@10 | 0.4461 |
| Query-weighted Reranking hybrid hit@10 | 0.7928 |
| Query-weighted Reranking hybrid Recall@100 | 0.7528 |
| Mean query length | 1,100.29 chars, weighted by query count |
| Mean document length | 3,569.62 chars, weighted by split-local document count |

### Public Sources

- [IFIR: A Comprehensive Benchmark for Evaluating Instruction-Following in Expert-Domain Information Retrieval](https://aclanthology.org/2025.naacl-long.511/); 2025; DOI: `10.18653/v1/2025.naacl-long.511`.
- [Overview of the FIRE 2019 AILA Track: Artificial Intelligence for Legal Assistance](https://ceur-ws.org/Vol-2517/T1-1.pdf); 2019.
- [Overview of the TREC 2015 Clinical Decision Support Track](https://trec.nist.gov/pubs/trec24/papers/Overview-CL.pdf); 2015.
- [WWW'18 Open Challenge: Financial Opinion Mining and Question Answering](https://doi.org/10.1145/3184558.3192301); 2018.

### Hugging Face Links

- Nano dataset: [hakari-bench/NanoIFIR](https://huggingface.co/datasets/hakari-bench/NanoIFIR)

### Source Reference Table

| Title | Year | Type | URL |
| --- | ---: | --- | --- |
| IFIR: A Comprehensive Benchmark for Evaluating Instruction-Following in Expert-Domain Information Retrieval | 2025 | benchmark paper | https://aclanthology.org/2025.naacl-long.511/ |
| Overview of the FIRE 2019 AILA Track: Artificial Intelligence for Legal Assistance | 2019 | source task paper | https://ceur-ws.org/Vol-2517/T1-1.pdf |
| Overview of the TREC 2015 Clinical Decision Support Track | 2015 | source task paper | https://trec.nist.gov/pubs/trec24/papers/Overview-CL.pdf |
| WWW'18 Open Challenge: Financial Opinion Mining and Question Answering | 2018 | source task paper | https://doi.org/10.1145/3184558.3192301 |

## Machine-Readable Metadata

<!-- benchmark-task-group-metadata:v1 -->

```yaml
benchmark_task_group_metadata:
  schema_version: 1
  document_status: reviewed_manual
  nano_set: NanoIFIR
  backing_dataset: NanoIFIR
  dataset_id: hakari-bench/NanoIFIR
  language: en
  category: natural_language
  document_path: docs/benchmark_tasks/NanoIFIR/index.md
  source_research:
    primary_source_type: benchmark_paper
    paper_pdf_or_html_checked: true
    no_paper_note: null
  counts:
    tasks: 7
    queries: 637
    split_local_documents: 48246
    positive_qrels: 3872
  positives_per_query:
    average: 6.078492935635793
    min: 1
    median: 4.0
    max: 47
    multi_positive_tasks: 7
    multi_positive_queries: 588
  text_stats_chars:
    query_mean_weighted_by_queries: 1100.287284144427
    document_mean_weighted_by_documents: 3569.6247564564937
  bm25:
    ndcg_at_10_query_weighted: 0.3648991461
    hit_at_10_query_weighted: 0.7189952904
    source: dataset_candidate_subset
    strongest_task_by_ndcg_at_10: NanoIFIRScifact
    weakest_task_by_ndcg_at_10: NanoIFIRAila
  tasks:
  - name: NanoIFIRAila
    path: docs/benchmark_tasks/NanoIFIR/NanoIFIRAila.md
    retrieval_focus: legal_fact_pattern_to_prior_case_judgment
    queries: 40
    documents: 2914
    positive_qrels: 119
    bm25_ndcg_at_10: 0.1051
    bm25_hit_at_10: 0.225
  - name: NanoIFIRCds
    path: docs/benchmark_tasks/NanoIFIR/NanoIFIRCds.md
    retrieval_focus: clinical_case_to_biomedical_evidence
    queries: 42
    documents: 10000
    positive_qrels: 466
    bm25_ndcg_at_10: 0.1345
    bm25_hit_at_10: 0.4762
  - name: NanoIFIRFiQA
    path: docs/benchmark_tasks/NanoIFIR/NanoIFIRFiQA.md
    retrieval_focus: finance_question_to_advice_passage
    queries: 200
    documents: 10000
    positive_qrels: 1010
    bm25_ndcg_at_10: 0.2252
    bm25_hit_at_10: 0.61
  - name: NanoIFIRFire
    path: docs/benchmark_tasks/NanoIFIR/NanoIFIRFire.md
    retrieval_focus: legal_case_summary_to_precedent_document
    queries: 167
    documents: 1739
    positive_qrels: 563
    bm25_ndcg_at_10: 0.3704
    bm25_hit_at_10: 0.7365
  - name: NanoIFIRNFCorpus
    path: docs/benchmark_tasks/NanoIFIR/NanoIFIRNFCorpus.md
    retrieval_focus: health_topic_to_medical_research_evidence
    queries: 86
    documents: 3593
    positive_qrels: 242
    bm25_ndcg_at_10: 0.2833
    bm25_hit_at_10: 0.5698
  - name: NanoIFIRPm
    path: docs/benchmark_tasks/NanoIFIR/NanoIFIRPm.md
    retrieval_focus: precision_medicine_case_to_clinical_trial
    queries: 59
    documents: 10000
    positive_qrels: 1217
    bm25_ndcg_at_10: 0.3522
    bm25_hit_at_10: 0.8136
  - name: NanoIFIRScifact
    path: docs/benchmark_tasks/NanoIFIR/NanoIFIRScifact.md
    retrieval_focus: scientific_claim_to_evidence_abstract
    queries: 43
    documents: 10000
    positive_qrels: 255
    bm25_ndcg_at_10: 0.782
    bm25_hit_at_10: 1.0
  learning:
    leakage_note: exclude NanoIFIR evaluation queries, qrels, and positive documents;
      audit expert-domain source overlap before training
    useful_training_data:
    - IFIR-style instruction-query retrieval pairs
    - legal case and precedent retrieval data
    - clinical decision support and precision-medicine trial matching data
    - FiQA-style finance question-answer retrieval data
    - NFCorpus and SciFact evidence retrieval data
    synthetic_data:
      document_generation: expert-domain legal, clinical, financial, medical, trial,
        or scientific documents with explicit constraints and evidence
      question_generation: instruction-bearing expert-domain queries grounded in the
        document and role-specific need
      answerability: positives must satisfy the instruction and domain constraints,
        not only topical overlap
    multi_positive_training: multi_positive_objective
  links:
    nano_dataset: https://huggingface.co/datasets/hakari-bench/NanoIFIR
    source_urls:
    - label: IFIR ACL Anthology
      url: https://aclanthology.org/2025.naacl-long.511/
  references:
  - title: 'IFIR: A Comprehensive Benchmark for Evaluating Instruction-Following in
      Expert-Domain Information Retrieval'
    url: https://aclanthology.org/2025.naacl-long.511/
    year: 2025
    doi: 10.18653/v1/2025.naacl-long.511
    is_paper: true
    source_confidence: definitive_paper_link
  candidate_subsets:
    bm25:
      query_weighted_ndcg_at_10: 0.3648991461
      query_weighted_hit_at_10: 0.7189952904
      query_weighted_recall_at_100: 0.6344668451
      source: dataset_candidate_subset
    dense:
      query_weighted_ndcg_at_10: 0.4591234904
      query_weighted_hit_at_10: 0.7770800628
      query_weighted_recall_at_100: 0.7377063204
      source: dataset_candidate_subset
    reranking_hybrid:
      query_weighted_ndcg_at_10: 0.446114219
      query_weighted_hit_at_10: 0.7927786499
      query_weighted_recall_at_100: 0.7527937641
      source: dataset_candidate_subset
```
