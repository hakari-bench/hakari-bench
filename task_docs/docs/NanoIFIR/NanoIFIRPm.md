# NanoIFIR / NanoIFIRPm

## Overview

`NanoIFIRPm` is an English precision-medicine retrieval task in NanoIFIR. The queries describe cancer patients, diagnoses, and genetic variants, and the documents are clinical trial descriptions.

This task evaluates individualized oncology trial retrieval. A relevant document should match the patient's cancer type, gene variant, and trial eligibility context, so the retriever must combine exact biomedical entity matching with semantic understanding of clinical trial suitability.

## Details

### What the Original Data Measures

IFIR uses TREC Precision Medicine for healthcare instruction-following retrieval. It expands patient information into different instruction complexity levels, starting with disease and gene variation and adding demographics, treatment history, or family history.

The TREC 2017 Precision Medicine track focuses on precision oncology. Topics include cancer type, genetic variants, demographics, and other patient factors, and systems retrieve scientific articles or clinical trials relevant to individualized treatment decisions. This Nano split uses the clinical-trial retrieval side of that setting.

### Observed Data Profile

This Nano split contains 59 queries, 10,000 documents, and 1,217 positive qrels. Queries have 20.63 positives on average, with a minimum of 1, a median of 22.0, and a maximum of 47. There are 57 multi-positive queries, or 96.61% of the split. Queries average 145.75 characters, and documents average 2,244.87 characters.

Observed queries ask for suitable clinical trials for patients with cancers and mutations such as CDKN2A, PTEN, PIK3CA E545K, NTRK1, KRAS, ROS1, BRAF V600E, NRAS Q61R, and CDK4 amplification. Documents are clinical trial descriptions with conditions, interventions, eligibility criteria, and molecular targets.

### BM25 Evaluation Profile

BM25 reaches nDCG@10 of 0.4232, hit@10 of 0.8644, and recall@100 of 0.5768 with a top-500 candidate pool. Lexical retrieval is strong because cancer types and gene symbols are distinctive and often appear in both query and trial text.

BM25 is limited by eligibility matching. A trial may mention the same cancer or mutation but fail the patient profile, stage, prior treatment, or inclusion criteria. Conversely, a relevant trial may target a pathway or molecular alteration without repeating the exact query wording.

### Dense Evaluation Profile

The dense harrier-oss-270m profile reaches nDCG@10 of 0.5448, hit@10 of 0.9153, and recall@100 of 0.6812. Dense retrieval improves over BM25 across the main metrics.

This indicates that embedding similarity helps connect patient profiles to trial descriptions beyond exact entity overlap. Dense retrieval can capture disease family, molecular target, intervention intent, and eligibility semantics that are difficult for term matching alone.

### Reranking Hybrid Evaluation Profile

The reranking_hybrid candidate subset reaches nDCG@10 of 0.5468, hit@10 of 0.8983, and recall@100 of 0.7305. It uses 100 candidates per query, with one rank-101 safeguard positive.

Hybrid retrieval has the strongest nDCG@10 and recall@100, while dense retrieval has the highest hit@10. The hybrid profile is especially useful for reranking because it preserves exact gene and cancer-type matches while expanding coverage through semantic similarity.

### Metric Interpretation for Model Researchers

`NanoIFIRPm` is a hybrid-favorable precision-medicine task. BM25 is already useful because gene symbols and cancer names are strong lexical anchors, but dense retrieval and hybrid search improve relevance coverage and ranking.

Because most queries have many suitable trials, recall@100 is important. nDCG@10 indicates whether highly suitable trials appear early. A model that improves this task likely handles both biomedical entity precision and trial-eligibility semantics.

### Query and Relevance Type Tendencies

Queries are patient-specific oncology trial search instructions. They usually include cancer type and one or more genetic alterations, and may imply suitability constraints.

Documents are clinical trial descriptions, often containing condition names, drug or intervention names, molecular targets, eligibility criteria, and study purpose. The relevance relation is suitability for the patient profile.

### Representative Failure Modes

BM25 may retrieve trials with the same gene or cancer type but wrong eligibility criteria. Dense retrieval may retrieve trials in the same disease family while missing a required mutation. Hybrid retrieval reduces these errors but still needs reranking to evaluate inclusion criteria and molecular match.

A common hard case is partial matching: a trial may match the gene but not the tumor type, or match the tumor type but target a different variant.

### Training Data That May Help

Useful training data includes non-overlapping TREC Precision Medicine topics, ClinicalTrials.gov oncology trial retrieval pairs, biomedical entity linking, gene-variant normalization, and hard negatives with the same cancer type but a different mutation or eligibility profile.

Training should exclude `NanoIFIRPm` patient queries, qrels, and positive clinical trial documents.

### Model Improvement Notes

Improving this task requires precise biomedical entity normalization and semantic eligibility matching. Models should understand cancer synonyms, gene symbols, variant notation, molecular targets, inclusion criteria, and treatment context.

For reranking, the best behavior is explicit patient-trial compatibility: the top trials should satisfy the cancer type and variant while respecting trial scope and intervention intent.

## Example Data

### Public Sources

This task is documented through the IFIR paper and the TREC 2017 Precision Medicine track overview. The Nano split is published in `hakari-bench/NanoIFIR`.

### Source Reference Table

| Source | Role |
| --- | --- |
| [IFIR: A Comprehensive Benchmark for Evaluating Instruction-Following in Expert-Domain Information Retrieval](https://arxiv.org/abs/2503.04644) | Expert-domain instruction-following IR benchmark paper. |
| [Overview of the TREC 2017 Precision Medicine Track](https://trec.nist.gov/pubs/trec26/papers/Overview-PM.pdf) | Original precision medicine retrieval overview. |
| [hakari-bench/NanoIFIR](https://huggingface.co/datasets/hakari-bench/NanoIFIR) | Nano benchmark dataset containing this split. |

### Representative Snippets

| Query Pattern | Positive Document Pattern |
| --- | --- |
| A patient with head and neck squamous cell carcinoma and a CDKN2A mutation seeking suitable trials. | A trial description for squamous cell carcinoma or related oncology interventions. |
| A prostate cancer patient with PTEN inactivation seeking trials. | A trial involving prostate cancer, pathway-targeted therapy, or relevant treatment setting. |
| A gastric cancer patient with PIK3CA E545K seeking trials. | A trial for cancers with PIK3CA activating mutations or PI3K-pathway targeting. |
| A papillary thyroid carcinoma patient with an NTRK1 mutation seeking trials. | A trial targeting NTRK, ROS1, ALK, or related molecular alterations in advanced tumors. |
| An ampullary carcinoma patient with a KRAS mutation seeking trials. | A clinical trial involving related gastrointestinal cancers, biological treatment, or chemotherapy. |
