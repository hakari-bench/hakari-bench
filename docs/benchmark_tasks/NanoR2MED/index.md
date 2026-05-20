# NanoR2MED

> [!NOTE]
> This page was prepared by manual review of source papers, dataset cards,
> repository metadata, and sampled benchmark data. It may contain mistakes;
> please treat it as a reference aid rather than a definitive source.

## Overview

NanoR2MED is the Nano task group for R2MED, a reasoning-driven medical retrieval
benchmark. It contains eight English retrieval tasks spanning biomedical
StackExchange-style reference search, diagnostic and examination evidence
retrieval, treatment evidence retrieval, and clinical case retrieval. The group
is deliberately difficult for lexical baselines because many queries require an
implicit medical or scientific inference before the relevant passage can be
identified.

NanoR2MED should be treated as a research evaluation resource, not as a clinical
decision system. The tasks are useful for measuring whether a retriever can find
supporting evidence for biomedical reasoning, diagnosis, examination choice,
treatment planning, and case similarity.

## Details

### What the Original Group Measures

[R2MED: A Benchmark for Reasoning-Driven Medical Retrieval](https://arxiv.org/abs/2505.14558)
introduces R2MED as a medical retrieval benchmark where relevance is not simply
semantic similarity between a query and a document. The paper describes
reasoning-driven retrieval: a model may need to infer a biological concept,
diagnosis, examination, treatment decision, or same-diagnosis case group before
it can retrieve the evidence passage. The arXiv record for the paper was first
submitted in 2025 and revised in 2026.

NanoR2MED samples the R2MED benchmark release into eight compact splits. The Q&A
reference tasks use StackExchange-style biomedical questions and linked or
supporting resources. The clinical evidence tasks use medical exam,
diagnostic, and treatment-planning questions paired with textbook, Wikipedia, or
PubMed Central passages. The clinical case tasks use patient-case descriptions
and retrieve similar cases whose relevance is mediated by diagnosis or clinical
reasoning rather than by surface symptom overlap alone.

### Subtask Coverage

The eight subtasks cover four retrieval families:

- **Biomedical Q&A reference retrieval:** `NanoR2MEDBioinformatics`,
  `NanoR2MEDBiology`, and `NanoR2MEDMedicalSciences` retrieve answer-supporting
  references for practical or conceptual questions from bioinformatics, biology,
  and medical-sciences communities.
- **Diagnostic and examination evidence retrieval:** `NanoR2MEDMedQADiag` and
  `NanoR2MEDMedXpertQAExam` turn exam-style clinical vignettes into evidence
  retrieval tasks over textbook or Wikipedia-derived medical passages.
- **Treatment evidence retrieval:** `NanoR2MEDPMCTreatment` retrieves PubMed
  Central passages that support treatment or management reasoning for structured
  case summaries.
- **Clinical case retrieval:** `NanoR2MEDPMCClinical` and
  `NanoR2MEDIIYiClinical` retrieve similar cases from PMC-derived or IIYi
  clinical records, where diagnosis and clinical similarity are the main bridge.

All eight splits are English and all use 10,000 split-local candidate documents.
Every split is multi-positive on average, but the number of positives differs:
case and Q&A tasks usually have two to four positives per query, while the
MedQA diagnosis split averages more than four positives.

### Observed Group Profile

Across the eight splits, NanoR2MED contains 876 queries, 2,678 positive qrels,
and 80,000 split-local candidate documents. The document count is a sum across
subtasks, not a deduplicated group-wide corpus size. The group average is 3.06
positives per query, and 651 queries have more than one positive document.

The query shapes vary widely. `NanoR2MEDBiology` and
`NanoR2MEDMedicalSciences` use shorter conceptual or consumer-facing questions,
while `NanoR2MEDIIYiClinical` and `NanoR2MEDPMCTreatment` use long structured
case summaries. The longest average query length is in `NanoR2MEDIIYiClinical`
at 2,584.10 characters, while the shortest is `NanoR2MEDMedicalSciences` at
477.62 characters. Documents also range from short medical textbook or
Wikipedia chunks to long translated clinical records; `NanoR2MEDIIYiClinical`
has documents averaging 5,042.31 characters.

### BM25 Difficulty

NanoR2MED is difficult for the provided BM25 candidate baseline. The
query-weighted BM25 nDCG@10 is 0.1263 and query-weighted hit@10 is 0.2979.
`NanoR2MEDPMCClinical` is the strongest split for BM25 with nDCG@10 = 0.3277,
because case reports often repeat distinctive anatomy, disease, imaging, or
symptom terms. `NanoR2MEDPMCTreatment` is the weakest with nDCG@10 = 0.0180 and
hit@10 = 0.0600, reflecting the need to infer treatment reasoning from long
case summaries before matching the supporting article passage.

The inspected examples show the same pattern. BM25 often finds related medical
or scientific vocabulary but misses the latent bridge: a practical
bioinformatics question may require a tool manual or file-format definition; a
clinical vignette may require recognizing a diagnosis before searching textbook
evidence; a treatment case may need the relevant intervention or pathway rather
than the broad disease terms. This makes NanoR2MED a useful stress test for
retrievers that combine biomedical vocabulary, clinical entity understanding,
and reasoning-oriented evidence search.

### Training Data That May Help

Useful training data should be selected by retrieval family. For the Q&A
reference splits, useful data includes non-overlapping Bioinformatics, Biology,
and Medical Sciences StackExchange answer-link pairs, biomedical concept QA,
tool-documentation retrieval, and BRIGHT-style reasoning-intensive retrieval
examples. For the diagnostic and examination splits, useful supervision includes
medical exam vignettes paired with diagnosis-supporting textbook passages,
medical entity linking from vignettes to diagnoses or tests, and hard negatives
from similar symptoms but different conditions.

For the PMC and IIYi clinical tasks, useful data includes non-overlapping
case-report similarity pairs, diagnosis-labeled clinical case matching,
PubMed Central treatment evidence retrieval, PICO-style intervention evidence,
and hard negatives that share disease or symptom terms but support a different
clinical decision. Training should exclude NanoR2MED evaluation queries, qrels,
positive documents, and same-source near duplicates. Overlap audits matter
because several subtasks originate from public benchmarks or public biomedical
corpora that may also be used for training.

### Synthetic Data Guidance

Synthetic NanoR2MED-style data should preserve the reasoning step. For
document-to-question generation, start from non-evaluation biomedical passages,
tool manuals, medical textbook sections, Wikipedia medical sections, or PMC
treatment discussions, then generate questions whose answer requires using that
passage rather than simply repeating its wording. Clinical vignettes should
include symptoms, history, labs, imaging, medications, and confounders when they
are grounded in the source evidence.

For case retrieval, synthetic data should create clusters of de-identified case
records sharing a diagnosis while varying demographics and presentation. Hard
negatives should be medically plausible and share symptoms, disease area, tool
name, or treatment vocabulary, but they should fail the actual reasoning target.
NanoR2MED evaluation queries and positive passages should not be used as seeds.

## Task Summary

| Task | Retrieval shape | Queries | Docs | Positive qrels | BM25 nDCG@10 | BM25 hit@10 | Query avg chars | Doc avg chars | Source status |
| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | --- |
| [NanoR2MEDBioinformatics](NanoR2MEDBioinformatics.md) | bioinformatics question to supporting reference | 77 | 10,000 | 226 | 0.1786 | 0.4416 | 890.32 | 666.84 | R2MED paper + dataset card |
| [NanoR2MEDBiology](NanoR2MEDBiology.md) | biology question to explanatory passage | 103 | 10,000 | 374 | 0.2513 | 0.5049 | 523.03 | 474.07 | R2MED paper + dataset card |
| [NanoR2MEDIIYiClinical](NanoR2MEDIIYiClinical.md) | translated clinical case to similar cases | 129 | 10,000 | 457 | 0.1246 | 0.3798 | 2,584.10 | 5,042.31 | R2MED paper + dataset card |
| [NanoR2MEDMedQADiag](NanoR2MEDMedQADiag.md) | diagnostic vignette to textbook evidence | 118 | 10,000 | 522 | 0.0281 | 0.1356 | 706.74 | 791.42 | R2MED paper + dataset card |
| [NanoR2MEDMedXpertQAExam](NanoR2MEDMedXpertQAExam.md) | exam vignette to examination evidence | 97 | 10,000 | 292 | 0.0245 | 0.0722 | 928.44 | 723.85 | R2MED paper + dataset card |
| [NanoR2MEDMedicalSciences](NanoR2MEDMedicalSciences.md) | medical-sciences question to reference passage | 88 | 10,000 | 244 | 0.1043 | 0.2727 | 477.62 | 678.60 | R2MED paper + dataset card |
| [NanoR2MEDPMCClinical](NanoR2MEDPMCClinical.md) | PMC case summary to similar clinical cases | 114 | 10,000 | 248 | 0.3277 | 0.6140 | 827.68 | 2,103.50 | R2MED paper + dataset card |
| [NanoR2MEDPMCTreatment](NanoR2MEDPMCTreatment.md) | treatment case summary to PMC evidence | 150 | 10,000 | 315 | 0.0180 | 0.0600 | 1,755.83 | 726.63 | R2MED paper + dataset card |

## Dataset Information

| Field | Value |
| --- | --- |
| Nano set | NanoR2MED |
| Backing dataset | NanoR2MED |
| Hugging Face dataset | [hakari-bench/NanoR2MED](https://huggingface.co/datasets/hakari-bench/NanoR2MED) |
| Language | en |
| Category | natural_language |
| Subtasks | 8 |
| Total queries | 876 |
| Split-local documents | 80,000 |
| Positive qrels | 2,678 |
| Positives per query | 3.06 average |
| Multi-positive queries | 651 |
| Query-weighted BM25 nDCG@10 | 0.1263 |
| Query-weighted BM25 hit@10 | 0.2979 |
| Mean query length | 1,174.65 chars, weighted by query count |
| Mean document length | 1,400.90 chars, weighted by split-local document count |

### Public Sources

- [R2MED: A Benchmark for Reasoning-Driven Medical Retrieval](https://arxiv.org/abs/2505.14558); 2025; Xiangxu Zhang, Lei Li, Xiao Zhou, and Zheng Liu; DOI: `10.48550/arXiv.2505.14558`.
- [R2MED project page](https://r2med.github.io/).
- [R2MED GitHub repository](https://github.com/R2MED/R2MED).

### Hugging Face Links

- Nano dataset: [hakari-bench/NanoR2MED](https://huggingface.co/datasets/hakari-bench/NanoR2MED)
- Source datasets:
  [R2MED/Bioinformatics](https://huggingface.co/datasets/R2MED/Bioinformatics),
  [R2MED/Biology](https://huggingface.co/datasets/R2MED/Biology),
  [R2MED/IIYi-Clinical](https://huggingface.co/datasets/R2MED/IIYi-Clinical),
  [R2MED/MedQA-Diag](https://huggingface.co/datasets/R2MED/MedQA-Diag),
  [R2MED/MedXpertQA-Exam](https://huggingface.co/datasets/R2MED/MedXpertQA-Exam),
  [R2MED/Medical-Sciences](https://huggingface.co/datasets/R2MED/Medical-Sciences),
  [R2MED/PMC-Clinical](https://huggingface.co/datasets/R2MED/PMC-Clinical),
  [R2MED/PMC-Treatment](https://huggingface.co/datasets/R2MED/PMC-Treatment).

### Source Reference Table

| Title | Year | Type | URL |
| --- | ---: | --- | --- |
| R2MED: A Benchmark for Reasoning-Driven Medical Retrieval | 2025 | benchmark paper | https://arxiv.org/abs/2505.14558 |
| R2MED project page | 2025 | project page | https://r2med.github.io/ |
| R2MED GitHub repository | 2025 | source repository | https://github.com/R2MED/R2MED |
| R2MED source datasets | 2025 | dataset collection | https://huggingface.co/R2MED |

## Machine-Readable Metadata

<!-- benchmark-task-group-metadata:v1 -->

```yaml
benchmark_task_group_metadata:
  schema_version: 1
  document_status: reviewed_manual
  nano_set: NanoR2MED
  backing_dataset: NanoR2MED
  dataset_id: hakari-bench/NanoR2MED
  language: en
  category: natural_language
  document_path: docs/benchmark_tasks/NanoR2MED/index.md
  source_research:
    primary_source_type: benchmark_paper_and_dataset_cards
    paper_pdf_or_html_checked: true
    paper_url: https://arxiv.org/abs/2505.14558
    no_paper_note: null
  counts:
    tasks: 8
    queries: 876
    split_local_documents: 80000
    positive_qrels: 2678
  positives_per_query:
    average: 3.057077625570776
    min: 1
    median_task_median: 2.5
    max: 19
    multi_positive_tasks: 8
    multi_positive_queries: 651
  text_stats_chars:
    query_mean_weighted_by_queries: 1174.6461187340183
    document_mean_weighted_by_documents: 1400.90165
  bm25:
    ndcg_at_10_query_weighted: 0.12628940727671234
    hit_at_10_query_weighted: 0.29794520546803654
    ndcg_at_10_unweighted_task_mean: 0.132126414825
    hit_at_10_unweighted_task_mean: 0.3100972876125
    source: dataset_bm25_column
    easiest_task_by_ndcg_at_10: NanoR2MEDPMCClinical
    hardest_task_by_ndcg_at_10: NanoR2MEDPMCTreatment
  tasks:
    - name: NanoR2MEDBioinformatics
      path: docs/benchmark_tasks/NanoR2MED/NanoR2MEDBioinformatics.md
      retrieval_shape: bioinformatics_question_to_supporting_reference
      queries: 77
      documents: 10000
      positive_qrels: 226
      bm25_ndcg_at_10: 0.1785792901
      bm25_hit_at_10: 0.4415584416
    - name: NanoR2MEDBiology
      path: docs/benchmark_tasks/NanoR2MED/NanoR2MEDBiology.md
      retrieval_shape: biology_question_to_explanatory_passage
      queries: 103
      documents: 10000
      positive_qrels: 374
      bm25_ndcg_at_10: 0.2512844907
      bm25_hit_at_10: 0.5048543689
    - name: NanoR2MEDIIYiClinical
      path: docs/benchmark_tasks/NanoR2MED/NanoR2MEDIIYiClinical.md
      retrieval_shape: translated_clinical_case_to_similar_cases
      queries: 129
      documents: 10000
      positive_qrels: 457
      bm25_ndcg_at_10: 0.1246035498
      bm25_hit_at_10: 0.3798449612
    - name: NanoR2MEDMedQADiag
      path: docs/benchmark_tasks/NanoR2MED/NanoR2MEDMedQADiag.md
      retrieval_shape: diagnostic_vignette_to_textbook_evidence
      queries: 118
      documents: 10000
      positive_qrels: 522
      bm25_ndcg_at_10: 0.0281042121
      bm25_hit_at_10: 0.1355932203
    - name: NanoR2MEDMedXpertQAExam
      path: docs/benchmark_tasks/NanoR2MED/NanoR2MEDMedXpertQAExam.md
      retrieval_shape: exam_vignette_to_examination_evidence
      queries: 97
      documents: 10000
      positive_qrels: 292
      bm25_ndcg_at_10: 0.0244625982
      bm25_hit_at_10: 0.0721649485
    - name: NanoR2MEDMedicalSciences
      path: docs/benchmark_tasks/NanoR2MED/NanoR2MEDMedicalSciences.md
      retrieval_shape: medical_sciences_question_to_reference_passage
      queries: 88
      documents: 10000
      positive_qrels: 244
      bm25_ndcg_at_10: 0.1042864669
      bm25_hit_at_10: 0.2727272727
    - name: NanoR2MEDPMCClinical
      path: docs/benchmark_tasks/NanoR2MED/NanoR2MEDPMCClinical.md
      retrieval_shape: pmc_case_summary_to_similar_clinical_cases
      queries: 114
      documents: 10000
      positive_qrels: 248
      bm25_ndcg_at_10: 0.3277008275
      bm25_hit_at_10: 0.6140350877
    - name: NanoR2MEDPMCTreatment
      path: docs/benchmark_tasks/NanoR2MED/NanoR2MEDPMCTreatment.md
      retrieval_shape: treatment_case_summary_to_pmc_evidence
      queries: 150
      documents: 10000
      positive_qrels: 315
      bm25_ndcg_at_10: 0.0179898833
      bm25_hit_at_10: 0.06
  learning:
    leakage_note: exclude NanoR2MED evaluation queries, qrels, positive passages, same-source near duplicates, and same-article clinical case duplicates where applicable
    useful_training_data:
      - non-overlapping biomedical StackExchange answer-link retrieval
      - BRIGHT-style reasoning-intensive biomedical retrieval
      - medical exam vignette to textbook evidence retrieval
      - clinical entity linking from vignette to diagnosis, examination, or treatment
      - PubMed Central treatment and case-report evidence retrieval
      - diagnosis-labeled clinical case similarity pairs
      - hard negatives sharing symptoms, disease, tool, or treatment vocabulary but differing in the reasoning target
    synthetic_data:
      document_generation: non-evaluation biomedical references, medical textbook chunks, Wikipedia medical passages, PMC evidence paragraphs, and de-identified clinical cases
      question_generation: practical bioinformatics questions, biology explanations, medical-sciences questions, diagnostic vignettes, examination vignettes, treatment-planning cases, and diagnosis-hidden case summaries
      answerability: positives must support the latent biomedical or clinical reasoning target, not merely repeat terms from the query
    multi_positive_training: preserve_multi_positive_evidence_and_case_clusters
  links:
    nano_dataset: https://huggingface.co/datasets/hakari-bench/NanoR2MED
    source_urls:
      - label: R2MED arXiv
        url: https://arxiv.org/abs/2505.14558
      - label: R2MED project page
        url: https://r2med.github.io/
      - label: R2MED GitHub
        url: https://github.com/R2MED/R2MED
      - label: R2MED/Bioinformatics
        url: https://huggingface.co/datasets/R2MED/Bioinformatics
      - label: R2MED/Biology
        url: https://huggingface.co/datasets/R2MED/Biology
      - label: R2MED/IIYi-Clinical
        url: https://huggingface.co/datasets/R2MED/IIYi-Clinical
      - label: R2MED/MedQA-Diag
        url: https://huggingface.co/datasets/R2MED/MedQA-Diag
      - label: R2MED/MedXpertQA-Exam
        url: https://huggingface.co/datasets/R2MED/MedXpertQA-Exam
      - label: R2MED/Medical-Sciences
        url: https://huggingface.co/datasets/R2MED/Medical-Sciences
      - label: R2MED/PMC-Clinical
        url: https://huggingface.co/datasets/R2MED/PMC-Clinical
      - label: R2MED/PMC-Treatment
        url: https://huggingface.co/datasets/R2MED/PMC-Treatment
    source_notes: []
  references:
    - title: "R2MED: A Benchmark for Reasoning-Driven Medical Retrieval"
      url: https://arxiv.org/abs/2505.14558
      year: 2025
      doi: 10.48550/arXiv.2505.14558
      is_paper: true
      source_confidence: definitive_paper_link
```
