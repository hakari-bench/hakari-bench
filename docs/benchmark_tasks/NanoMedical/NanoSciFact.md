# NanoMedical / NanoSciFact

## Overview

SciFact was introduced for scientific claim verification: systems must find
research abstracts that support or refute expert-written claims and identify
rationale evidence. This NanoMedical task uses the retrieval part of that
benchmark: an atomic biomedical claim is the query, and the positive documents
are abstracts containing evidence for or against it. The observed claims are
compact statements about mechanisms, genes, autophagy, cytokines, or clinical
associations, so retrieval depends on scientific directionality and experimental
context, not only terminology overlap.

## Details

### What the Original Data Measures

[Fact or Fiction: Verifying Scientific Claims](https://arxiv.org/abs/2004.14974)
introduces scientific claim verification: selecting research abstracts that
support or refute a scientific claim and identifying rationales justifying the
decision. The paper constructs SciFact with 1,409 expert-written scientific
claims verified against 5,183 abstracts. Claims are written from citation
sentences in scientific papers, and abstracts are labeled as `SUPPORTS`,
`REFUTES`, or `NO INFO` with rationale sentences for evidence-bearing pairs.

The SciFact paper reports that the corpus is built from S2ORC, using a curated
set of high-quality biomedical journals and adding co-cited and distractor
abstracts to make retrieval harder. Claim writers included scientific NLP
experts, life-science undergraduates, and graduate or medical students, while
verification involved separate annotators. The paper reports 0.75 Cohen's kappa
for label agreement on reannotated claim-abstract pairs and 0.71 for rationale
sentence agreement.

Although the full SciFact task includes label prediction and rationale
selection, this Nano task focuses on evidence retrieval: given a claim, retrieve
the abstract that contains evidence for or against it. This keeps the retrieval
surface of SciFact while ignoring the final support/refute classification.

### Observed Data Profile

The Nano split has 200 claims, 5,183 abstracts, and 226 positive qrel rows.
Most claims have one positive abstract; 16 of 200 claims have multiple positives,
and the maximum is 5. Queries average 90.07 characters, while documents average
1,499.41 characters. Documents generally include an article title followed by a
long biomedical abstract.

Observed claims are compact scientific statements such as `Deleting Raptor
reduces G-CSF levels`, `Autophagy declines in aged organisms`, or `CX3CR1 on
the Th2 cells suppresses airway inflammation`. Many claims contain gene symbols,
cell types, model organisms, biomedical interventions, or direction-sensitive
relations. Relevant abstracts may not repeat the claim verbatim; they may express
the evidence through results, experimental conditions, or mechanistic language.

### BM25 Difficulty

Using the dataset-provided BM25 candidate column, BM25 reaches nDCG@10 = 0.6289
and hit@10 = 0.7850. It ranks 101 of 226 positives first and 168 positives
inside the top 10. This is a relatively strong sparse baseline because claims
often include distinctive scientific terms, gene names, organism names, or
intervention names that also occur in the relevant abstract.

The hard cases are not simple topic misses. For an insomnia claim, BM25 ranks a
clinical trial of cognitive behavioral therapy first but misses a broader
circadian-rhythm abstract labeled relevant. For an invadopodia claim, it
retrieves abstracts with `Src`, calcium channels, or cortactin before the
positive podosome-formation abstract. For plant PIN1 localization, it retrieves
other auxin and plant-development abstracts first. The task rewards retrieval
models that can match a claim to the exact evidence relation, not just the same
biomedical vocabulary cluster.

### Training Data That May Help

Useful training data includes non-overlapping scientific claim-evidence pairs,
biomedical citation-to-abstract retrieval, SciFact-style rationale data,
scientific fact verification data, and hard negatives from co-cited or same-topic
abstracts. Training should emphasize directionality, negation, causal language,
experimental model context, and gene/protein nomenclature.

For clean evaluation, training should exclude SciFact evaluation claims, their
positive abstracts, and near-duplicate claims derived from the same source
citances. Using the official SciFact training split is an in-domain supervised
setting and should be reported separately from zero-shot evaluation.

### Synthetic Data Guidance

For document-to-question generation, start from non-evaluation biomedical
abstracts and generate atomic scientific claims about one result, intervention,
mechanism, or association. Include both claims that would be supported and claims
that would be refuted by careful direction reversal or condition changes.

For joint document-and-question generation, create biomedical abstracts and
claim-like queries with same-topic hard negatives. The negatives should share
genes, diseases, or methods but differ in direction, cell type, population,
intervention, or outcome. Do not seed generation with Nano evaluation claims or
positive abstracts.

## Example Data

| Query | Positive document |
| --- | --- |
| Metastatic colorectal cancer treated with a single agent fluoropyrimidines resulted in reduced efficacy and lower quality of life when compared with oxaliplatin-based chemotherapy in elderly patients. (200 chars) | Chemotherapy options in elderly and frail patients with metastatic colorectal cancer (MRC FOCUS2): an open-label, randomised factorial trial BACKGROUND Elderly and frail patients with cancer, although often treated with chemo ... [truncated 225 chars](3063 chars) |
| CRP is not predictive of postoperative mortality following Coronary Artery Bypass Graft (CABG) surgery. (103 chars) | Assessing the cost effectiveness of using prognostic biomarkers with decision models: case study in prioritising patients waiting for coronary artery surgery OBJECTIVE To determine the effectiveness and cost effectiveness of ... [truncated 225 chars](2937 chars) |
| Arginine 90 in p150n is important for interaction with EB1. (59 chars) | Structural basis for the activation of microtubule assembly by the EB1 and p150Glued complex. Plus-end tracking proteins, such as EB1 and the dynein/dynactin complex, regulate microtubule dynamics. These proteins are thought ... [truncated 225 chars](1198 chars) |
| Obesity is determined solely by environmental factors. (54 chars) | Genetics of obesity in adult adoptees and their biological siblings. An adoption study of genetic effects on obesity in adulthood was carried out in which adoptees separated from their natural parents very early in life were ... [truncated 225 chars](1319 chars) |
| Febrile seizures increase the threshold for development of epilepsy. (68 chars) | Febrile seizures in the developing brain result in persistent modification of neuronal excitability in limbic circuits Febrile (fever-induced) seizures affect 3–5% of infants and young children. Despite the high incidence of ... [truncated 225 chars](801 chars) |

## Dataset Information

| Field | Value |
| --- | --- |
| Nano set | NanoMedical |
| Backing dataset | NanoMedical |
| Task / split | NanoSciFact |
| Hugging Face dataset | [hakari-bench/NanoMedical](https://huggingface.co/datasets/hakari-bench/NanoMedical) |
| Language | en |
| Category | natural_language |
| Queries | 200 |
| Documents | 5,183 |
| Positive qrels | 226 |
| Positives per query | avg 1.13; min 1; median 1; max 5 |
| Multi-positive queries | 16 / 200 (8.00%) |
| BM25 nDCG@10 | 0.6289 |
| BM25 hit@10 | 0.7850 |
| Query length avg chars | 90.07 |
| Document length avg chars | 1,499.41 |

### Public Sources

- [Fact or Fiction: Verifying Scientific Claims](https://arxiv.org/abs/2004.14974); 2020; David Wadden, Shanchuan Lin, Kyle Lo, Lucy Lu Wang, Madeleine van Zuylen, Arman Cohan, and Hannaneh Hajishirzi.
- [ACL Anthology record](https://aclanthology.org/2020.emnlp-main.609/).

### Hugging Face Links

- Nano dataset: [hakari-bench/NanoMedical](https://huggingface.co/datasets/hakari-bench/NanoMedical)

### Source Reference Table

| Title | Year | Type | URL |
| --- | ---: | --- | --- |
| Fact or Fiction: Verifying Scientific Claims | 2020 | arXiv paper | https://arxiv.org/abs/2004.14974 |
| Fact or Fiction: Verifying Scientific Claims | 2020 | ACL Anthology paper | https://aclanthology.org/2020.emnlp-main.609/ |

## Machine-Readable Metadata

<!-- benchmark-task-metadata:v1 -->

```yaml
benchmark_task_metadata:
  schema_version: 1
  document_status: first_pass
  nano_set: NanoMedical
  backing_dataset: NanoMedical
  dataset_id: hakari-bench/NanoMedical
  task_name: NanoSciFact
  split_name: NanoSciFact
  language: en
  category: natural_language
  document_path: docs/benchmark_tasks/NanoMedical/NanoSciFact.md
  source_research:
    primary_source_type: task_paper
    paper_pdf_or_html_checked: true
    paper_url: https://arxiv.org/abs/2004.14974
    additional_source_urls:
      - https://aclanthology.org/2020.emnlp-main.609/
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
    query_mean: 90.065
    document_mean: 1499.407293
  bm25:
    ndcg_at_10: 0.6288504435
    hit_at_10: 0.785
    source: dataset_bm25_column
  learning:
    original_train_split: available
    evaluation_split_origin: SciFact evidence retrieval split sampled into NanoMedical
    train_eval_overlap_audit: not_audited
    leakage_note: exclude SciFact evaluation claims, positive abstracts, and near-duplicate claims derived from the same source citances
    useful_training_data:
      - non-overlapping scientific claim-evidence pairs
      - biomedical citation-to-abstract retrieval data
      - SciFact-style rationale and verification data outside the evaluation split
      - same-topic biomedical hard negatives
    synthetic_data:
      document_generation: biomedical abstracts with explicit methods, findings, and outcomes
      question_generation: atomic scientific claims about one result, association, intervention, or mechanism
      hard_negatives: same-topic abstracts differing in direction, condition, population, or outcome
      answerability: the abstract should contain evidence sufficient to support or refute the claim
    multi_positive_training: mostly single-positive with limited multi-positive support
  links:
    nano_dataset: https://huggingface.co/datasets/hakari-bench/NanoMedical
    source_urls:
      - label: SciFact arXiv
        url: https://arxiv.org/abs/2004.14974
      - label: SciFact ACL Anthology
        url: https://aclanthology.org/2020.emnlp-main.609/
```
