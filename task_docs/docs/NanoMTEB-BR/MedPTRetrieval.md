# NanoMTEB-BR / MedPTRetrieval

## Overview

MedPTRetrieval is a Brazilian Portuguese medical question-answer retrieval task
derived from MedPT. The source collection contains authentic patient questions
and clinician answers spanning many conditions and several kinds of health
intent, such as symptoms, diagnosis, treatment, and medication. Queries can be
informal, underspecified, or written with regional and everyday vocabulary,
while relevant documents use more clinical explanations. The retrieval task
asks a model to surface an answer that addresses the medical intent rather than
a passage that merely repeats a disease name. NanoMTEB-BR samples this source
into a compact corpus for fast evaluation while preserving native Brazilian
Portuguese interactions instead of translated medical text. Because most
queries have very few judged positives, the task makes incorrect intent matches
visible: answers about a related condition or a different stage of care can be
topically similar but still irrelevant.

## Details

### What the Task Measures

The task measures semantic matching between layperson health questions and
clinically informed answers. Important distinctions include symptom versus
diagnosis, contraindication versus general treatment, patient context, and the
requested type of advice.

### Metric Interpretation

`nDCG@10` rewards placing the judged answer close to rank one. `Hit@10` reports
whether one appears anywhere in the first ten. These are retrieval-quality
metrics only; they do not establish clinical correctness or authorize use as a
medical decision system.

### Training and Leakage Notes

Train with non-overlapping Portuguese medical QA and carefully selected hard
negatives for related conditions. Exclude Nano queries, qrels, positive
answers, and upstream MedPT evaluation records. Audit paraphrases and copied
web answers, and avoid treating synthetic medical content as verified advice.

## Public Sources

- [MedPT paper](https://arxiv.org/abs/2511.11878).
- [MedPT source dataset](https://huggingface.co/datasets/AKCIT/MedPT).
- [NanoMTEB-BR dataset](https://huggingface.co/datasets/hakari-bench/NanoMTEB-BR).
