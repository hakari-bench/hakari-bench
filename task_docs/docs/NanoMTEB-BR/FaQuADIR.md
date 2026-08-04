# NanoMTEB-BR / FaQuADIR

## Overview

FaQuADIR is a Brazilian Portuguese FAQ-style retrieval task derived from
FaQuAD, a reading-comprehension collection in the domain of Brazilian higher
education. Each query asks about an institution, academic process, service, or
policy, and the system must retrieve the answer-bearing passage from a compact
document pool. The source data was created for Portuguese question answering,
so the language reflects local institutional vocabulary rather than a
machine-translated English benchmark. In retrieval form, the task tests whether
a model can align a natural question with a concise answer passage when both
may express the same intent using different wording. Many questions are close
to single-positive lookup, making top-rank precision especially visible. The
NanoMTEB-BR version samples the source evaluation material for efficient model
comparison while retaining the higher-education domain and Brazilian
Portuguese phrasing of the original task.

## Details

### What the Task Measures

The task emphasizes question-to-answer semantic matching, including
institution-specific names, abbreviations, administrative terms, and procedural
conditions. Lexical matching can be effective for distinctive entities, but it
is less reliable when the answer paraphrases the question.

### Metric Interpretation

`nDCG@10` is most sensitive to how early the answer-bearing passage is ranked.
`Hit@10` shows whether the model retrieves a judged answer anywhere in the
first ten. Because the task is close to single-positive retrieval, missed
intent or entity distinctions can cause a full-query failure.

### Training and Leakage Notes

Helpful training data includes non-overlapping Brazilian Portuguese FAQs and
educational-domain QA pairs. Exclude Nano evaluation queries, positives, and
upstream evaluation records. Deduplicate normalized questions and answer
passages, since FAQ pages are frequently copied or lightly reformatted.

## Public Sources

- [FaQuAD paper](https://doi.org/10.1109/BRACIS.2019.00084).
- [FaQuADIR source dataset](https://huggingface.co/datasets/MTEB-BR/faquad-ir).
- [NanoMTEB-BR dataset](https://huggingface.co/datasets/hakari-bench/NanoMTEB-BR).
