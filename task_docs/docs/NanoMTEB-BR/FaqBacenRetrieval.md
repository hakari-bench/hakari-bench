# NanoMTEB-BR / FaqBacenRetrieval

## Overview

FaqBacenRetrieval is a Brazilian Portuguese financial FAQ retrieval task built
from public information associated with Banco Central do Brasil. Queries are
questions that a consumer or financial-services user might ask, and relevant
documents are FAQ answers explaining products, rules, services, or procedures.
The source work was designed to address the shortage of Portuguese financial
question-answering data and includes language specific to Brazil's banking and
regulatory context. The retrieval task therefore combines concise FAQ matching
with terminology that can be precise and easily confused across related
topics. A strong model must identify the user's intent, preserve named products
and conditions, and rank the correct institutional answer above passages that
share common financial vocabulary. NanoMTEB-BR uses a compact evaluation
sample, allowing rapid comparison while keeping the source task's native
Brazilian Portuguese and domain-specific relevance relation.

## Details

### What the Task Measures

This task tests short-question to authoritative-answer matching in the
financial domain. Hard cases include near-duplicate intents, procedural
qualifiers, and answers whose key distinction is a small number, date, account
type, or regulatory term.

### Metric Interpretation

`nDCG@10` rewards placing the correct answer near rank one, while `Hit@10`
indicates whether any judged answer is present in the first ten. The two metrics
together distinguish precise FAQ ranking from broad topical retrieval.

### Training and Leakage Notes

Use non-overlapping Portuguese banking FAQs and intent-paraphrase data for
training. Exclude Nano queries, qrels, positive answers, and upstream evaluation
rows. Public FAQ text may be mirrored by third-party sites, so normalized text
and semantic near-duplicate audits are appropriate.

## Public Sources

- [Portuguese FAQ for Financial Services paper](https://arxiv.org/abs/2311.11331).
- [FaqBacen source dataset](https://huggingface.co/datasets/MTEB-BR/faq-bacen).
- [NanoMTEB-BR dataset](https://huggingface.co/datasets/hakari-bench/NanoMTEB-BR).
