# NanoMTEB-BR / BRTaxQAR

## Overview

BRTaxQAR is a Brazilian Portuguese legal retrieval task for questions about
Brazilian personal income tax. A query is a practical tax question, while a
relevant document is supporting legal material such as legislation,
regulations, administrative guidance, or an administrative ruling. The source
BR-TaxQA-R collection extends an official 2024 tax question-and-answer resource
with references to the legal authorities needed to justify an answer. This
makes the task more demanding than FAQ matching: a relevant passage may use
formal terminology and may establish the rule without repeating the wording of
the question. In NanoMTEB-BR, the task keeps a compact query and corpus sample
for fast comparison of retrievers. It primarily measures whether a model can
connect everyday taxpayer language to authoritative Brazilian tax-law text,
while preserving distinctions among similar taxes, filing situations,
exceptions, and procedural requirements.

## Details

### What the Task Measures

The retrieval target is evidentiary support, not merely an answer that sounds
plausible. Strong systems must bridge colloquial questions and formal legal
language, retain dates and conditions, and distinguish provisions with similar
vocabulary but different applicability.

### Metric Interpretation

`nDCG@10` rewards putting all judged supporting authorities near the top and
accounts for queries with more than one relevant document. `Hit@10` answers the
simpler question of whether at least one judged authority appears in the first
ten results. Inspect both: a high hit rate with lower nDCG can indicate that the
model finds one useful source but ranks other relevant authorities poorly.

### Training and Leakage Notes

Useful supervision includes non-overlapping Portuguese legal QA, statute
retrieval, and hard negatives drawn from related provisions. Exclude the Nano
queries, qrels, and positive documents, and audit upstream BR-TaxQA-R test
material. Template-like guidance and repeated legal text can create near-match
leakage even when identifiers differ.

## Public Sources

- [BR-TaxQA-R paper](https://arxiv.org/abs/2505.15916).
- [BR-TaxQA-R source dataset](https://huggingface.co/datasets/unicamp-dl/BR-TaxQA-R).
- [NanoMTEB-BR dataset](https://huggingface.co/datasets/hakari-bench/NanoMTEB-BR).
