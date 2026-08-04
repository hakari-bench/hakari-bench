# NanoMTEB-BR

## Overview

NanoMTEB-BR is the compact Brazilian Portuguese retrieval group derived from
the six native Retrieval tasks in MTEB-BR. It covers Brazilian tax law,
higher-education and central-bank FAQs, federal audit-court case law, medical
question answering, and general passage retrieval. Unlike translated benchmark
copies, all six tasks originate from Brazilian Portuguese sources. The group
therefore tests whether a retrieval model handles local legal and institutional
language, domain terminology, question-to-answer matching, and semantically
related passages across corpora that range from a few hundred documents to
10,000-document hard-negative pools.

## What This Group Measures

The six tasks expose different relevance relations within one language. FAQ and
medical tasks retrieve answer-bearing text for natural questions. The legal
tasks retrieve statutes, rulings, or case-law material whose relevant passages
may share specialized terminology without repeating the question. Quati tests
general passage retrieval with native Brazilian Portuguese queries and hard
negatives.

This mix makes the group useful for separating broad Portuguese semantic
quality from domain-specific retrieval behavior. A model can perform well on
short institutional FAQs while struggling with long or terminology-heavy legal
documents, or it can retrieve general passages well without ranking concise
medical answers accurately.

## Task Families

- **Tax-law retrieval:** [BRTaxQAR](BRTaxQAR.md) maps Brazilian tax questions to relevant
  statutes, regulations, administrative rulings, and related legal sources.
- **Higher-education FAQ retrieval:** [FaQuADIR](FaQuADIR.md) retrieves answers about
  Brazilian higher-education institutions and services.
- **Central-bank FAQ retrieval:** [FaqBacenRetrieval](FaqBacenRetrieval.md) retrieves public
  information from Banco Central do Brasil.
- **Public-sector case-law retrieval:** [JurisTCU](JurisTCU.md) retrieves Tribunal de Contas
  da União rulings from a hard-negative legal corpus.
- **Medical QA retrieval:** [MedPTRetrieval](MedPTRetrieval.md) retrieves Brazilian Portuguese
  answers for health and medical questions.
- **General passage retrieval:** [Quati](Quati.md) retrieves relevant native Brazilian
  Portuguese passages from a hard-negative corpus.

## Dataset Shape

| Task | Domain | Queries | Documents | Positive qrels |
| --- | --- | ---: | ---: | ---: |
| `BRTaxQAR` | Brazilian tax law | 200 | 461 | 546 |
| `FaQuADIR` | Higher-education FAQ | 200 | 243 | 201 |
| `FaqBacenRetrieval` | Central-bank FAQ | 200 | 1,654 | 201 |
| `JurisTCU` | Federal audit-court case law | 150 | 10,000 | 1,711 |
| `MedPTRetrieval` | Medical question answering | 200 | 500 | 204 |
| `Quati` | General passage retrieval | 49 | 10,000 | 892 |

All tasks use Brazilian Portuguese (`pt`) queries and documents. The FAQ and
medical tasks have relatively small document pools and are close to
single-positive retrieval. `JurisTCU` and `Quati` use larger hard-negative
pools and many relevant passages for some queries, so their scores should not
be interpreted as the same retrieval problem at a different scale.

## Evaluation and Interpretation

NanoMTEB-BR is a dedicated viewer scope and contributes six tasks to a complete
HAKARI-Bench evaluation. Like other language-focused NanoMTEB suites, it is not
an additional canonical Overall component; the six result files are still
evaluated, stored, and available for direct comparison.

The initial validation compared 29 models that had complete results on both the
official MTEB-BR Retrieval suite and NanoMTEB-BR. Ranking the models across the
same six tasks produced a Spearman correlation of 0.9860 and a Kendall
correlation of 0.9320. Twenty-eight of the 29 models remained within two Borda
rank positions. This supports using NanoMTEB-BR as a close rank-preserving proxy
for model comparison, while absolute scores remain specific to the smaller
Nano corpora and query samples.

## Training and Leakage Notes

Useful training data includes non-overlapping Brazilian Portuguese FAQ pairs,
medical QA, legal question-to-passage examples, public-sector search logs, and
general passage-retrieval supervision. Hard negatives should come from the same
institution or domain and share terminology while answering a different
question.

Training and validation pipelines should exclude the Nano evaluation queries,
qrels, positive documents, and overlapping upstream test records. Legal and
institutional sources can contain repeated templates or near-duplicate text, so
document-level deduplication alone may not prevent leakage.

## Public Sources

- [MTEB-BR: A Text Embedding Benchmark for Brazilian Portuguese](https://doi.org/10.5281/zenodo.21087217), 2026.
- [MTEB-BR source repository](https://github.com/tardellirs/mteb-br).
- [BRTaxQAR source paper](https://arxiv.org/abs/2505.15916).
- [FaQuAD source paper](https://doi.org/10.1109/BRACIS.2019.00084).
- [FaqBacen source paper](https://arxiv.org/abs/2311.11331).
- [JurisTCU source paper](https://doi.org/10.1007/s10579-025-09881-w).
- [MedPT source paper](https://arxiv.org/abs/2511.11878).
- [Quati source paper](https://aclanthology.org/2024.stil-1.19/).
- [NanoMTEB-BR dataset](https://huggingface.co/datasets/hakari-bench/NanoMTEB-BR).
