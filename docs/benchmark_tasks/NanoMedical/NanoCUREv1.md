# NanoMedical / NanoCUREv1

## Overview

CURE was designed as clinical retrieval for healthcare providers at the point of
care, with expert-written queries across multiple medical domains and
evidence-bearing passages as targets. This NanoMedical split keeps that
provider-facing passage retrieval setting and is strongly multi-positive: many
clinical questions have numerous relevant passages. The observed queries ask
about diagnosis, treatment choice, contraindications, anatomy, orthodontic
movement, sleep apnea, and surgical technique, so the model must rank passages
that actually answer a practitioner question rather than merely share a medical
topic.

## Details

### What the Original Data Measures

[CURE: A Dataset for Clinical Understanding & Retrieval Evaluation](https://arxiv.org/abs/2412.06954)
introduces CURE as a clinical retrieval dataset for healthcare providers at the
point of care. The paper describes 2,000 expert-written queries across 10
medical domains, with each domain containing lay and expert questions. The
domains include dentistry and oral health, dermatology, gastroenterology,
genetics, neuroscience and neurology, orthopedic surgery, otorhinolaryngology,
plastic surgery, psychiatry and psychology, and pulmonology. The paper also
reports English monolingual evaluation and French/Spanish-to-English
cross-lingual evaluation.

The original CURE corpus contains 244,600 passages mined from 51,083 biomedical
articles. The paper says the articles came from sources such as PubMed Central
Open Access, BioMed Central, and Nature, and that a large candidate pool was
assembled using reciprocal-rank fusion over sparse and dense retrieval before
relevance annotation. Relevance labels distinguish relevant, partially relevant,
and not relevant passages. The annotation process combined healthcare
professional review with LLM-assisted annotation for broad coverage; the paper
reports annotators were physicians and nurses, and that a comparison sample
between human labels and Qwen 2.5 72B labels reached substantial agreement.

This makes CURE different from narrower biomedical benchmarks such as
TREC-COVID or SciFact. Its queries are written to resemble real clinical
information needs, and the relevant passages may be methods, findings,
definitions, or clinical implications from biomedical articles. The CURE paper's
baseline table reports English BM25 at nDCG@10 = 0.355 and Recall@100 = 0.523,
below dense models, which is consistent with a task that requires more than
surface lexical overlap.

### Observed Data Profile

The Nano split has 200 queries, 10,000 documents, and 5,181 positive qrel rows.
Unlike many small retrieval tasks, this split is strongly multi-positive: the
average query has 25.91 positive passages, the median is 18, and 171 of 200
queries have more than one positive. Queries average 75.89 characters, while
documents average 604.21 characters. Documents usually begin with an article
title followed by a passage, so successful retrieval can benefit from both title
matching and passage-level evidence matching.

The observed questions are mostly direct English clinical questions. Common
openings include `What`, `Which`, `How`, and `Is`, but the actual information
needs are specific: diagnosing obstructive sleep apnea, judging whether clear
aligners can produce extrusion, identifying contraindications for maxillofacial
fixation screws, understanding endoscopic management of epistaxis, and asking
about orthodontic white spot lesions. The positive passages often contain
specialized terminology, abbreviations, or study-design language, so a model
must connect clinical wording to article evidence rather than only match the
same phrase.

### BM25 Difficulty

Using the dataset-provided BM25 candidate column, BM25 reaches nDCG@10 = 0.3699
and hit@10 = 0.8050 on this Nano split. Because most queries have many
positives, the two numbers should be read together: BM25 finds at least one
positive in the top 10 for most queries, but it retrieves only 561 of 5,181
positive qrel rows inside the top 10. The median rank of individual positives is
69 among the provided BM25 candidates.

The failure cases show why the task is difficult. Acronyms and medical terms can
be ambiguous: `IMF` in jaw fixation queries can retrieve irrelevant engineering
or signal-processing passages about intrinsic mode functions. Queries about
clear aligners, self-etching primers, white spot lesions, or endoscopic
epistaxis retrieve many topically adjacent articles, but the labeled positives
often require the passage to express a specific benefit, limitation,
contraindication, or clinical outcome. Sparse matching is therefore useful for
getting into the right neighborhood, but semantic and domain-aware reranking are
needed to order the evidence passages well.

### Training Data That May Help

Useful training data includes non-overlapping clinical question-to-passage
pairs, biomedical evidence retrieval data, medical QA retrieval data where the
answer is grounded in article passages, and domain-specific corpora covering
dental, surgical, pulmonary, dermatology, neurology, and other clinical
specialties. Training that teaches abbreviation disambiguation, question-to-title
matching, and passage-level evidence selection should be particularly helpful.

Because CURE is a public benchmark, training should exclude CURE evaluation
queries, CURE positive passages, and near-duplicate mined passages when the goal
is a clean evaluation on this task. General biomedical pretraining or unrelated
PubMed retrieval can help, but direct memorization of CURE labels would
overstate performance.

### Synthetic Data Guidance

For document-to-question generation, start from non-evaluation biomedical
article passages and generate concise clinician-style questions that ask for one
diagnostic criterion, treatment implication, contraindication, measurement,
adverse event, or surgical consideration. The generated question should not copy
the title verbatim; it should express the clinical information need in the way a
healthcare professional might ask it.

For joint document-and-question generation, create realistic article-title plus
passage snippets in clinical specialties and pair each with multiple questions
targeting different evidence points. Include hard negatives from the same
medical topic but with a different clinical relation, for example diagnosis
versus treatment, indication versus contraindication, or adult versus pediatric
patients. Synthetic data should not be seeded with Nano evaluation queries or
positive passages.

## Example Data

| Query | Positive document |
| --- | --- |
| Which are the factors that should be taken in consideration when deciding the location of IMF screws placement? (111 chars) | The Use of MMF Screws: Surgical Technique, Indications, Contraindications, and Common Problems in Review of the Literature The anatomical site for the placement of MMF screws is chosen with respect to a given fracture locatio ... [truncated 225 chars](362 chars) |
| Which are the disadvantages of 3D printed splints in orthognathic surgery? (74 chars) | Comparison between Additive and Subtractive CAD-CAM Technique to Produce Orthognathic Surgical Splints: A Personalized Approach The findings of the present investigation would suggest that surgical splints are more accurate w ... [truncated 225 chars](470 chars) |
| Which are the advantages of endoscopic approach to treat massive arterial epistaxis? (84 chars) | Success Rate of Endoscopic Sphenopalatine Artery Ligation for the Management of Refractory Posterior Epistaxis Patients in a Tertiary Care Hospital: A Descriptive Cross-sectional Study The findings of the study conclude that ... [truncated 225 chars](613 chars) |
| What are the typical temporomandibular joint symptoms that can appear in a patient undergoing maxillomandibular advancement? (124 chars) | Temporomandibular chronic dislocation: The long-standing condition Clinically the condition is characterised by the inability to close the mouth after wide opening, and change in occlusion with open bite and/or lateral mandib ... [truncated 225 chars](356 chars) |
| What are the primary compounds used in tooth whitening products? (64 chars) | Effectiveness of sodium bicarbonate combined with hydrogen peroxide and CPP-ACPF in whitening and microhardness of enamel Most patients undergoing fixed orthodontic therapy suffer from color alterations on their teeth a few d ... [truncated 225 chars](1439 chars) |

## Dataset Information

| Field | Value |
| --- | --- |
| Nano set | NanoMedical |
| Backing dataset | NanoMedical |
| Task / split | NanoCUREv1 |
| Hugging Face dataset | [hakari-bench/NanoMedical](https://huggingface.co/datasets/hakari-bench/NanoMedical) |
| Language | en |
| Category | natural_language |
| Queries | 200 |
| Documents | 10,000 |
| Positive qrels | 5,181 |
| Positives per query | avg 25.91; min 1; median 18; max 100 |
| Multi-positive queries | 171 / 200 (85.50%) |
| BM25 nDCG@10 | 0.3699 |
| BM25 hit@10 | 0.8050 |
| Query length avg chars | 75.89 |
| Document length avg chars | 604.21 |

### Public Sources

- [CURE: A Dataset for Clinical Understanding & Retrieval Evaluation](https://arxiv.org/abs/2412.06954); 2024 arXiv / 2025 KDD; Nadia Athar Sheikh, Daniel Buades Marcos, Anne-Laure Jousse, Akintunde Oladipo, Olivier Rousseau, and Jimmy Lin.
- [KDD 2025 DOI record](https://doi.org/10.1145/3711896.3737435).
- [clinia/CUREv1](https://huggingface.co/datasets/clinia/CUREv1) Hugging Face dataset.

### Hugging Face Links

- Nano dataset: [hakari-bench/NanoMedical](https://huggingface.co/datasets/hakari-bench/NanoMedical)
- Source dataset: [clinia/CUREv1](https://huggingface.co/datasets/clinia/CUREv1)

### Source Reference Table

| Title | Year | Type | URL |
| --- | ---: | --- | --- |
| CURE: A Dataset for Clinical Understanding & Retrieval Evaluation | 2024 | arXiv paper | https://arxiv.org/abs/2412.06954 |
| CURE: A Dataset for Clinical Understanding & Retrieval Evaluation | 2025 | KDD proceedings DOI | https://doi.org/10.1145/3711896.3737435 |
| clinia/CUREv1 | 2024 | source dataset | https://huggingface.co/datasets/clinia/CUREv1 |

## Machine-Readable Metadata

<!-- benchmark-task-metadata:v1 -->

```yaml
benchmark_task_metadata:
  schema_version: 1
  document_status: first_pass
  nano_set: NanoMedical
  backing_dataset: NanoMedical
  dataset_id: hakari-bench/NanoMedical
  task_name: NanoCUREv1
  split_name: NanoCUREv1
  language: en
  category: natural_language
  document_path: docs/benchmark_tasks/NanoMedical/NanoCUREv1.md
  source_research:
    primary_source_type: task_paper
    paper_pdf_or_html_checked: true
    paper_url: https://arxiv.org/abs/2412.06954
    additional_source_urls:
      - https://doi.org/10.1145/3711896.3737435
      - https://huggingface.co/datasets/clinia/CUREv1
  counts:
    queries: 200
    documents: 10000
    positive_qrels: 5181
  positives_per_query:
    average: 25.905
    min: 1
    median: 18.0
    max: 100
    multi_positive_queries: 171
    multi_positive_query_percent: 85.5
  text_stats_chars:
    query_mean: 75.89
    document_mean: 604.2063
  bm25:
    ndcg_at_10: 0.3698959662
    hit_at_10: 0.805
    source: dataset_bm25_column
    original_paper_en_ndcg_at_10: 0.355
    original_paper_en_recall_at_100: 0.523
  learning:
    original_train_split: unavailable
    evaluation_split_origin: CURE benchmark test collection sampled into NanoMedical
    train_eval_overlap_audit: not_audited
    leakage_note: exclude CURE evaluation queries, CURE positive passages, and near-duplicate mined biomedical passages when training for clean evaluation
    useful_training_data:
      - non-overlapping clinical question-to-passage retrieval pairs
      - biomedical evidence retrieval data grounded in article passages
      - medical QA retrieval data with passage-level evidence
      - clinical abbreviation and specialty-specific hard-negative training
    synthetic_data:
      document_generation: biomedical article-title plus passage snippets from non-evaluation clinical specialties
      question_generation: concise clinician-style questions targeting diagnosis, treatment, contraindication, measurement, or clinical implication
      hard_negatives: same-topic passages with different clinical relations or patient contexts
      answerability: each question should be answerable from the selected passage without outside medical knowledge
    multi_positive_training: train with multi-positive labels and same-topic hard negatives
  links:
    nano_dataset: https://huggingface.co/datasets/hakari-bench/NanoMedical
    source_urls:
      - label: CURE arXiv
        url: https://arxiv.org/abs/2412.06954
      - label: CURE KDD DOI
        url: https://doi.org/10.1145/3711896.3737435
      - label: clinia/CUREv1
        url: https://huggingface.co/datasets/clinia/CUREv1
```
