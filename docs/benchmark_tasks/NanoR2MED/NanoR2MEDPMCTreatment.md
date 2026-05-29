# NanoR2MED / NanoR2MEDPMCTreatment

## Overview

R2MED's PMC-Treatment task targets treatment-planning evidence retrieval: case
summaries from MedRBench_Treat must retrieve PubMed Central passages associated
with treatment or management decisions. The Nano queries are long structured
clinical summaries with demographics, history, tests, diagnosis, management,
and outcome, while positives are shorter PMC discussion or treatment-context
paragraphs. A retriever must infer the management question latent in the case
and rank scientific evidence that supports that treatment reasoning.

## Details

### What the Original Data Measures

[R2MED: A Benchmark for Reasoning-Driven Medical Retrieval](https://arxiv.org/abs/2505.14558)
describes PMC-Treatment as one of the three clinical evidence retrieval
datasets. The source question set comes from MedRBench_Treat, and R2MED retains
the original article associated with each question as the positive document.
To build hard negatives, the paper reports crawling roughly 14,000 PubMed
Central Open Access case reports focused on diagnosis or treatment topics.

The paper's relevance pipeline uses the clinical question, answer, and
reasoning path to judge whether candidate documents support both the answer and
the reasoning process. It also emphasizes that R2MED is for research evaluation,
not clinical decision-making.

### Observed Data Profile

The Nano split has 150 queries, 10,000 documents, and 315 positive qrels. Queries
average 1,755.83 characters and are structured case summaries with demographics,
chief complaint, history, tests, diagnosis, management, and outcome. Documents
average 726.63 characters and are short PMC passages, often discussion or
treatment-context paragraphs.

Each query has 2.10 positives on average, with a median of 2 and a maximum of
5 positives. The sampled cases cover immunotherapy for renal or inflammatory
disease, renal denervation for resistant hypertension, neonatal congenital heart
disease, endovascular aortic repair, and ocular surface burns. Many positives
are not simple answer snippets; they provide background evidence that supports
the treatment decision.

### BM25 Difficulty

Using the dataset-provided BM25 candidate column, BM25 reaches nDCG@10 = 0.0180
and hit@10 = 0.0600. It ranks no positives first and finds a positive inside
the top 10 for only 9 of 150 queries. This is the hardest NanoR2MED split in
this batch for the provided sparse baseline.

Observed failures show repeated high-ranking generic treatment or case-report
passages even when the positive concerns a specific therapy. For example, BM25
retrieves broad empirical-antibiotic commentary before anti-MDA5
dermatomyositis evidence, COVID-related immunomodulation evidence, duodenal
trauma treatment background, or JAK-STAT pathway treatment discussion. Strong
retrieval likely requires treatment-plan inference and article-level context.

### Training Data That May Help

Useful training data includes non-overlapping treatment-planning QA, clinical
case-to-evidence retrieval, PubMed Central treatment and case-report retrieval,
PICO-style intervention evidence, and hard negatives with the same disease but
different treatment. Multi-positive training is useful because about half the
queries have multiple positives.

Training should exclude R2MED PMC-Treatment evaluation queries, qrels, and
positive PMC passages. If using MedRBench or PMC OA articles, audit for overlap
with the evaluated case summaries and source articles.

### Synthetic Data Guidance

For document-to-question generation, use non-evaluation PMC discussion or
treatment passages and generate structured treatment-planning case summaries
whose management question is grounded in the passage.

For joint generation, create realistic case summaries plus PMC-style evidence
paragraphs about therapy choice, complication management, procedure selection,
or follow-up. Hard negatives should share disease and treatment vocabulary but
support a different clinical decision. Do not seed generation with Nano
evaluation queries or positives.

## Example Data

| Query | Positive document |
| --- | --- |
| Case Summary: - **Patient Demographics:** 43-year-old male - **Chief Complaint:** Unexplained edema of the eyelids and lower limbs - **History of Present Illness:** Progressive edema without hematuria. Proteinuria measured at ... [truncated 225 chars](2067 chars) | Daratumumab is an antibody against CD38 used for plasma cell depletion in relapsed or refractory multiple myeloma (MM). It mediates depletion of plasma cells, which overexpress CD38, through a wide range of mechanisms includi ... [truncated 225 chars](952 chars) |
| Case Summary: - Patient Demographics: 43-year-old male - Chief Complaint: Long-standing therapy-resistant hypertension refractory to maximal medical therapy with symptoms including agitation, headaches, chest pain, sweating, ... [truncated 225 chars](1404 chars) | While the observed 24 hours systolic ambulatory BD reduction at 6-months follow-up in contemporary trials such as SPYRAL ON MED is generally considered to be modest (−1.9 mmHg),6 it seems that the observed treatment effect in ... [truncated 225 chars](664 chars) |
| Case Summary: - **Patient Demographics:** 2-day-old male neonate - **Chief Complaint:** Central cyanosis and poor breastfeeding following birth - **History of Present Illness:** - Neonate presented with central cyanosis and p ... [truncated 225 chars](2145 chars) | Helen B. Taussig and Richard J. Bing were the first to describe a rare cyanotic congenital heart defect known as the Taussig-Bing anomaly (TBA) in 1949, that includes a non-restrictive subpulmonary ventricular septal defect ( ... [truncated 225 chars](2503 chars) |
| Case Summary: - Patient Demographics: - Case 1: 87-year-old woman - Case 2: 84-year-old man - Chief Complaint: - Case 1: Persistent chest and back pain after initial treatment for a symptomatic penetrating aortic ulcer. - Cas ... [truncated 225 chars](1709 chars) | Adequate proximal seal zones are essential for durable endovascular aortic repair. Although the definition of an adequate proximal seal zone can vary depending on the underlying aortic pathology, compromised proximal seal zon ... [truncated 225 chars](660 chars) |
| Case Summary: - Patient Demographics: 43-year-old male - Chief Complaint: Redness, pain, and decreased vision in the left eye following lime exposure - History of Present Illness: - Presented with symptoms 1 day after lime ex ... [truncated 225 chars](1950 chars) | The surgical approach for severe ocular surface burns aims to reconstruct ocular surface function, address eyelid deformities, correct limbal stem cell deficiency, and alleviate conjunctival sac constriction, preparing the ey ... [truncated 225 chars](634 chars) |

## Dataset Information

| Field | Value |
| --- | --- |
| Nano set | NanoR2MED |
| Backing dataset | NanoR2MED |
| Task / split | NanoR2MEDPMCTreatment |
| Hugging Face dataset | [hakari-bench/NanoR2MED](https://huggingface.co/datasets/hakari-bench/NanoR2MED) |
| Language | en |
| Category | natural_language |
| Queries | 150 |
| Documents | 10,000 |
| Positive qrels | 315 |
| Avg positives / query | 2.10 |
| Positives per query (min / median / max) | 1 / 2 / 5 |
| Queries with multiple positives | 77 (51.33%) |
| BM25 nDCG@10 | 0.2580 |
| BM25 hit@10 | 0.4933 |
| BM25 Recall@100 | 0.5048 |
| BM25 candidate subset | top-500 (`bm25`) |
| Dense nDCG@10 | 0.3801 |
| Dense hit@10 | 0.6133 |
| Dense Recall@100 | 0.6413 |
| Dense candidate subset | top-500 (`harrier_oss_v1_270m`) |
| Reranking hybrid nDCG@10 | 0.3555 |
| Reranking hybrid hit@10 | 0.6667 |
| Reranking hybrid Recall@100 | 0.6984 |
| Reranking hybrid candidate subset | top-100 plus optional rank-101 safeguard (`reranking_hybrid`) |
| Reranking hybrid candidates / query | 100-101 |
| Reranking hybrid safeguard rows | 23 |
| Query length avg chars | 1,755.83 |
| Document length avg chars | 726.63 |

### Public Sources

- [R2MED: A Benchmark for Reasoning-Driven Medical Retrieval](https://arxiv.org/abs/2505.14558); 2025; Xiangxu Zhang, Lei Li, Xiao Zhou, and Zheng Liu; DOI: `10.48550/arXiv.2505.14558`.
- [R2MED project page](https://r2med.github.io/).
- [R2MED GitHub repository](https://github.com/R2MED/R2MED).
- [R2MED/PMC-Treatment dataset card](https://huggingface.co/datasets/R2MED/PMC-Treatment).

### Hugging Face Links

- Nano dataset: [hakari-bench/NanoR2MED](https://huggingface.co/datasets/hakari-bench/NanoR2MED)
- Source dataset: [R2MED/PMC-Treatment](https://huggingface.co/datasets/R2MED/PMC-Treatment)

### Source Reference Table

| Title | Year | Type | URL |
| --- | ---: | --- | --- |
| R2MED: A Benchmark for Reasoning-Driven Medical Retrieval | 2025 | arXiv paper | https://arxiv.org/abs/2505.14558 |
| R2MED project page | 2025 | project page | https://r2med.github.io/ |
| R2MED GitHub repository | 2025 | source repository | https://github.com/R2MED/R2MED |
| R2MED/PMC-Treatment | 2025 | dataset card | https://huggingface.co/datasets/R2MED/PMC-Treatment |

## Machine-Readable Metadata

<!-- benchmark-task-metadata:v1 -->

```yaml
benchmark_task_metadata:
  schema_version: 1
  document_status: first_pass
  nano_set: NanoR2MED
  backing_dataset: NanoR2MED
  dataset_id: hakari-bench/NanoR2MED
  task_name: NanoR2MEDPMCTreatment
  split_name: NanoR2MEDPMCTreatment
  language: en
  category: natural_language
  document_path: docs/benchmark_tasks/NanoR2MED/NanoR2MEDPMCTreatment.md
  source_research:
    primary_source_type: benchmark_paper
    paper_pdf_or_html_checked: true
    paper_url: https://arxiv.org/abs/2505.14558
    additional_source_urls:
    - https://r2med.github.io/
    - https://github.com/R2MED/R2MED
    - https://huggingface.co/datasets/R2MED/PMC-Treatment
  counts:
    queries: 150
    documents: 10000
    positive_qrels: 315
  positives_per_query:
    average: 2.1
    min: 1
    median: 2.0
    max: 5
    multi_positive_queries: 77
    multi_positive_query_percent: 51.33
  text_stats_chars:
    query_mean: 1755.826667
    document_mean: 726.6314
  bm25:
    ndcg_at_10: 0.25796156430818484
    hit_at_10: 0.49333333333333335
    source: dataset_candidate_subset
  learning:
    original_train_split: not_found
    evaluation_split_origin: R2MED benchmark release sampled into NanoR2MED
    train_eval_overlap_audit: not_audited
    leakage_note: exclude R2MED PMC-Treatment evaluation queries, qrels, and positive
      PMC passages
    useful_training_data:
    - non-overlapping treatment-planning medical QA
    - clinical case to evidence retrieval
    - PubMed Central treatment and case-report retrieval
    - hard negatives with the same disease but different treatment decision
    synthetic_data:
      document_generation: non-evaluation PMC treatment, procedure, or discussion
        passages
      question_generation: structured treatment-planning case summaries grounded in
        the passage
      hard_negatives: same disease and treatment vocabulary but different management
        implication
      answerability: the document should support the treatment decision or clinical
        management reasoning
    multi_positive_training: multi_positive_objective
  links:
    nano_dataset: https://huggingface.co/datasets/hakari-bench/NanoR2MED
    source_urls:
    - label: R2MED arXiv
      url: https://arxiv.org/abs/2505.14558
    - label: R2MED project page
      url: https://r2med.github.io/
    - label: R2MED GitHub
      url: https://github.com/R2MED/R2MED
    - label: R2MED/PMC-Treatment
      url: https://huggingface.co/datasets/R2MED/PMC-Treatment
    source_notes: []
  references:
  - title: 'R2MED: A Benchmark for Reasoning-Driven Medical Retrieval'
    url: https://arxiv.org/abs/2505.14558
    year: 2025
    doi: 10.48550/arXiv.2505.14558
    is_paper: true
    source_confidence: definitive_paper_link
  candidate_subsets:
    bm25:
      config: bm25
      label: BM25
      source: dataset_candidate_subset
      top_k: 500
      ndcg_at_10: 0.2579615643
      hit_at_10: 0.4933333333
      recall_at_100: 0.5047619048
      candidate_count_min: 500
      candidate_count_max: 500
      candidate_count_mean: 500.0
      query_count: 150
      query_coverage: 1.0
      relevant_coverage_at_100: 0.5047619048
    dense:
      config: harrier_oss_v1_270m
      label: Dense
      source: dataset_candidate_subset
      top_k: 500
      ndcg_at_10: 0.3800571081
      hit_at_10: 0.6133333333
      recall_at_100: 0.6412698413
      candidate_count_min: 500
      candidate_count_max: 500
      candidate_count_mean: 500.0
      query_count: 150
      query_coverage: 1.0
      relevant_coverage_at_100: 0.6412698413
    reranking_hybrid:
      config: reranking_hybrid
      label: Reranking hybrid
      source: dataset_candidate_subset
      top_k: 100
      ndcg_at_10: 0.355450316
      hit_at_10: 0.6666666667
      recall_at_100: 0.6984126984
      candidate_count_min: 100
      candidate_count_max: 101
      candidate_count_mean: 100.153333
      query_count: 150
      query_coverage: 1.0
      relevant_coverage_at_100: 0.6984126984
      safeguard_positive_rows: 23
      rows_with_101_candidates: 23
```
