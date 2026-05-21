# NanoMedical / NanoMedicalQA

## Overview

`NanoMedicalQA` is an English medical question-answer retrieval task. Queries
are short consumer-health questions, often following FAQ patterns such as
`What is`, `How to prevent`, `How to diagnose`, and `What are the treatments`.
Documents are answer passages from trusted medical information sources. The task
tests whether a retriever can match a medical question to the exact answer type,
not only to the same disease or parasite topic.

## Details

### What the Original Data Measures

[A question-entailment approach to question answering](https://bmcbioinformatics.biomedcentral.com/articles/10.1186/s12859-019-3119-4)
studies medical question answering through Recognizing Question Entailment
(RQE). The paper defines RQE for QA as retrieving already answered questions
whose answers are correct for a new question, then combining information
retrieval with an RQE model to rank answers. It introduces MedQuAD, a collection
of 47,457 question-answer pairs from trusted medical sources, and reports that
using reliable answer sources substantially improves medical QA.

The paper evaluates the approach on real medical questions, including the TREC
2017 LiveQA medical task, and frames the problem as fine-grained medical
question understanding plus answer retrieval. This Nano task reflects that
setting in a direct retrieval form: the query is a medical question, and the
positive document is the answer-bearing passage. The answer source is not a
scientific paper paragraph; it is consumer-facing medical guidance or FAQ text.

### Observed Data Profile

The Nano split has 200 queries, 2,007 answer documents, and exactly one positive
qrel per query. Queries average 54.23 characters, while documents average
1,102.43 characters. Many documents are several hundred characters long and
contain list formatting, prevention instructions, or multi-sentence medical
guidance.

The sampled queries are mostly templated English medical FAQ questions. They ask
for definitions, symptoms, diagnosis, prevention, and treatments for conditions
such as lymphocytic choriomeningitis, yersiniosis, head lice, ascariasis,
hookworm, toxoplasmosis, fascioliasis, body lice, and hemorrhagic fevers. The
observed documents often read like CDC fact-sheet answers, with practical
recommendations and disease-specific terminology.

### BM25 Difficulty

Using the dataset-provided BM25 candidate column, BM25 reaches nDCG@10 = 0.4736
and hit@10 = 0.7000. It ranks 47 of 200 positives first and 140 positives inside
the top 10. Sparse retrieval is helpful because disease names, organism names,
and answer-type words often overlap directly between query and document.

The main difficulty is answer-type discrimination. BM25 can find the right
disease topic but retrieve the wrong section: for head lice diagnosis it ranks
general head-lice description and treatment passages above the diagnosis
passage; for fascioliasis prevention it ranks definition and epidemiology
passages above the prevention passage; for body lice treatment it retrieves
pubic-lice treatment and body-lice definition before the actual body-lice
treatment answer. A strong model needs to distinguish definition, diagnosis,
prevention, symptoms, and treatment even when the disease name is identical.

### Training Data That May Help

Useful training data includes non-overlapping medical FAQ retrieval pairs,
consumer-health question-answer datasets, MedQuAD-style trusted-source QA pairs,
and answer-type classification or reranking data that separates definition,
symptoms, diagnosis, prevention, and treatment. Biomedical abstract retrieval can
help with terminology, but it should be complemented by consumer-facing medical
QA because these documents are guidance passages rather than research abstracts.

Training should exclude MedQuAD examples or source FAQ pages that overlap this
Nano split. Since this task contains highly templated questions, near-duplicate
question strings should also be deduplicated when using FAQ data for training.

### Synthetic Data Guidance

For document-to-question generation, start from non-evaluation medical guidance
passages and generate one question targeting the passage's answer type:
definition, cause, transmission, diagnosis, prevention, symptoms, or treatment.
The generated question should include the disease or organism name and the
specific answer type.

For joint document-and-question generation, create trusted-source style medical
FAQ passages with list-like instructions and pair them with concise questions.
Hard negatives should use the same disease name but a different answer type, for
example definition instead of treatment or prevention instead of diagnosis. Do
not seed generation with Nano evaluation queries or positive passages.

## Example Data

| Query | Positive document |
| --- | --- |
| What are the symptoms of Nocardiosis ? (38 chars) | The symptoms of nocardiosis vary depending on which part of your body is affected. Nocardiosis infection most commonly occurs in the lung. If your lungs are infected, you can experience: - Fever - Weight loss - Night sweats - ... [truncated 225 chars](823 chars) |
| What are the treatments for Parasites - Babesiosis ? (52 chars) | Effective treatments are available. People who do not have any symptoms or signs of babesiosis usually do not need to be treated. Before considering treatment, the first step is to make sure the diagnosis is correct. For more ... [truncated 225 chars](358 chars) |
| How to diagnose Parasites - Zoonotic Hookworm ? (47 chars) | Cutaneous larva migrans (CLM) is a clinical diagnosis based on the presence of the characteristic signs and symptoms, and exposure history to zoonotic hookworm. For example, the diagnosis can be made based on finding red, rai ... [truncated 225 chars](567 chars) |
| How to prevent Parasites - Lymphatic Filariasis ? (49 chars) | The best way to prevent lymphatic filariasis is to avoid mosquito bites. The mosquitoes that carry the microscopic worms usually bite between the hours of dusk and dawn. If you live in an area with lymphatic filariasis: - at ... [truncated 225 chars](1548 chars) |
| How to prevent Parasites - Hookworm ? (37 chars) | The best way to avoid hookworm infection is not to walk barefoot in areas where hookworm is common and where there may be human fecal contamination of the soil. Also, avoid other skin contact with such soil and avoid ingestin ... [truncated 225 chars](336 chars) |

## Dataset Information

| Field | Value |
| --- | --- |
| Nano set | NanoMedical |
| Backing dataset | NanoMedical |
| Task / split | NanoMedicalQA |
| Hugging Face dataset | [hakari-bench/NanoMedical](https://huggingface.co/datasets/hakari-bench/NanoMedical) |
| Language | en |
| Category | natural_language |
| Queries | 200 |
| Documents | 2,007 |
| Positive qrels | 200 |
| BM25 nDCG@10 | 0.4736 |
| BM25 hit@10 | 0.7000 |
| Query length avg chars | 54.23 |
| Document length avg chars | 1,102.43 |

### Public Sources

- [A question-entailment approach to question answering](https://bmcbioinformatics.biomedcentral.com/articles/10.1186/s12859-019-3119-4); 2019; Asma Ben Abacha and Dina Demner-Fushman.
- [DOI record](https://doi.org/10.1186/s12859-019-3119-4) for the BMC Bioinformatics article.

### Hugging Face Links

- Nano dataset: [hakari-bench/NanoMedical](https://huggingface.co/datasets/hakari-bench/NanoMedical)

### Source Reference Table

| Title | Year | Type | URL |
| --- | ---: | --- | --- |
| A question-entailment approach to question answering | 2019 | BMC Bioinformatics article | https://bmcbioinformatics.biomedcentral.com/articles/10.1186/s12859-019-3119-4 |
| A question-entailment approach to question answering | 2019 | DOI | https://doi.org/10.1186/s12859-019-3119-4 |

## Machine-Readable Metadata

<!-- benchmark-task-metadata:v1 -->

```yaml
benchmark_task_metadata:
  schema_version: 1
  document_status: first_pass
  nano_set: NanoMedical
  backing_dataset: NanoMedical
  dataset_id: hakari-bench/NanoMedical
  task_name: NanoMedicalQA
  split_name: NanoMedicalQA
  language: en
  category: natural_language
  document_path: docs/benchmark_tasks/NanoMedical/NanoMedicalQA.md
  source_research:
    primary_source_type: task_paper
    paper_pdf_or_html_checked: true
    paper_url: https://bmcbioinformatics.biomedcentral.com/articles/10.1186/s12859-019-3119-4
    additional_source_urls:
      - https://doi.org/10.1186/s12859-019-3119-4
  counts:
    queries: 200
    documents: 2007
    positive_qrels: 200
  positives_per_query:
    average: 1.0
    min: 1
    median: 1.0
    max: 1
    multi_positive_queries: 0
    multi_positive_query_percent: 0.0
  text_stats_chars:
    query_mean: 54.23
    document_mean: 1102.433981
  bm25:
    ndcg_at_10: 0.4735533647
    hit_at_10: 0.7
    source: dataset_bm25_column
  learning:
    original_train_split: available_in_source_qa_collections
    evaluation_split_origin: medical QA retrieval split sampled into NanoMedical
    train_eval_overlap_audit: not_audited
    leakage_note: exclude MedQuAD examples, overlapping trusted-source FAQ pages, and near-duplicate templated medical questions
    useful_training_data:
      - non-overlapping medical FAQ retrieval pairs
      - consumer-health question-answer datasets
      - MedQuAD-style trusted-source QA pairs
      - answer-type reranking data for definition, diagnosis, prevention, symptoms, and treatment
    synthetic_data:
      document_generation: trusted-source style medical guidance passages with clear answer type
      question_generation: concise medical FAQ questions targeting one answer type
      hard_negatives: same-disease passages with different answer types
      answerability: each question should be answerable from the paired guidance passage
    multi_positive_training: single_positive_question_answer_focus
  links:
    nano_dataset: https://huggingface.co/datasets/hakari-bench/NanoMedical
    source_urls:
      - label: BMC Bioinformatics article
        url: https://bmcbioinformatics.biomedcentral.com/articles/10.1186/s12859-019-3119-4
      - label: DOI
        url: https://doi.org/10.1186/s12859-019-3119-4
```
